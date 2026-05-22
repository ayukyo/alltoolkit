"""
Decision Matrix Utilities - 加权决策矩阵工具

功能：
- 创建决策矩阵（选项 x 标准）
- 加权评分计算
- 多种评分方法（加权平均、TOPSIS、层次分析法简化版）
- 敏感性分析
- 雷达图数据生成
- 决策报告生成

零外部依赖，仅使用 Python 标准库
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any, Callable
from enum import Enum
import math
import json


class ScoreMethod(Enum):
    """评分方法"""
    WEIGHTED_AVERAGE = "weighted_average"  # 加权平均
    WEIGHTED_SUM = "weighted_sum"           # 加权求和
    TOPSIS = "topsis"                       # TOPSIS法
    AHP_SIMPLIFIED = "ahp_simplified"       # 简化层次分析法


class CriteriaType(Enum):
    """标准类型"""
    BENEFIT = "benefit"     # 效益型（越大越好）
    COST = "cost"           # 成本型（越小越好）


@dataclass
class Criteria:
    """决策标准"""
    name: str
    weight: float  # 权重（0-1 或任意数值）
    criteria_type: CriteriaType = CriteriaType.BENEFIT
    description: str = ""
    min_value: Optional[float] = None  # 最小值（用于归一化）
    max_value: Optional[float] = None  # 最大值（用于归一化）
    
    def __post_init__(self):
        if self.weight < 0:
            raise ValueError(f"权重不能为负数: {self.weight}")
    
    def normalize_weight(self, total_weight: float) -> float:
        """归一化权重"""
        if total_weight <= 0:
            return 0
        return self.weight / total_weight


@dataclass
class Option:
    """决策选项"""
    name: str
    description: str = ""
    scores: Dict[str, float] = field(default_factory=dict)  # 标准名称 -> 分数
    metadata: Dict[str, Any] = field(default_factory=dict)   # 额外元数据
    
    def set_score(self, criteria_name: str, score: float) -> 'Option':
        """设置标准分数"""
        self.scores[criteria_name] = score
        return self
    
    def get_score(self, criteria_name: str) -> Optional[float]:
        """获取标准分数"""
        return self.scores.get(criteria_name)


@dataclass
class DecisionResult:
    """决策结果"""
    option_name: str
    total_score: float
    normalized_score: float
    rank: int
    criteria_scores: Dict[str, float]  # 各标准的归一化得分
    weighted_scores: Dict[str, float]  # 各标准的加权得分
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SensitivityResult:
    """敏感性分析结果"""
    criteria_name: str
    original_weight: float
    weight_range: Tuple[float, float]
    winner_changes: List[Tuple[float, str]]  # (权重值, 获胜选项)


class DecisionMatrix:
    """决策矩阵"""
    
    def __init__(self, name: str = "决策矩阵", description: str = ""):
        self.name = name
        self.description = description
        self.criteria: Dict[str, Criteria] = {}
        self.options: Dict[str, Option] = {}
        self._criteria_order: List[str] = []
        self._options_order: List[str] = []
    
    def add_criteria(self, criteria: Criteria) -> 'DecisionMatrix':
        """添加决策标准"""
        if criteria.name in self.criteria:
            raise ValueError(f"标准已存在: {criteria.name}")
        self.criteria[criteria.name] = criteria
        self._criteria_order.append(criteria.name)
        return self
    
    def add_criteria_simple(self, name: str, weight: float, 
                           criteria_type: CriteriaType = CriteriaType.BENEFIT,
                           description: str = "") -> 'DecisionMatrix':
        """简化添加标准"""
        return self.add_criteria(Criteria(
            name=name,
            weight=weight,
            criteria_type=criteria_type,
            description=description
        ))
    
    def add_option(self, option: Option) -> 'DecisionMatrix':
        """添加决策选项"""
        if option.name in self.options:
            raise ValueError(f"选项已存在: {option.name}")
        self.options[option.name] = option
        self._options_order.append(option.name)
        return self
    
    def add_option_simple(self, name: str, 
                         scores: Dict[str, float],
                         description: str = "") -> 'DecisionMatrix':
        """简化添加选项"""
        option = Option(name=name, description=description)
        for criteria_name, score in scores.items():
            option.set_score(criteria_name, score)
        return self.add_option(option)
    
    def set_score(self, option_name: str, criteria_name: str, score: float) -> 'DecisionMatrix':
        """设置选项在特定标准下的分数"""
        if option_name not in self.options:
            raise ValueError(f"选项不存在: {option_name}")
        if criteria_name not in self.criteria:
            raise ValueError(f"标准不存在: {criteria_name}")
        self.options[option_name].set_score(criteria_name, score)
        return self
    
    def get_total_weight(self) -> float:
        """获取总权重"""
        return sum(c.weight for c in self.criteria.values())
    
    def get_normalized_weights(self) -> Dict[str, float]:
        """获取归一化权重"""
        total = self.get_total_weight()
        return {name: c.normalize_weight(total) for name, c in self.criteria.items()}
    
    def _normalize_scores(self) -> Dict[str, Dict[str, float]]:
        """归一化所有分数（Min-Max归一化）"""
        normalized = {}
        
        for opt_name, option in self.options.items():
            normalized[opt_name] = {}
        
        for crit_name, criteria in self.criteria.items():
            scores = []
            for option in self.options.values():
                if crit_name in option.scores:
                    scores.append(option.scores[crit_name])
            
            if not scores:
                continue
            
            min_score = min(scores)
            max_score = max(scores)
            
            # 处理所有分数相同的情况
            if max_score == min_score:
                for opt_name in self.options:
                    normalized[opt_name][crit_name] = 1.0
            else:
                for opt_name, option in self.options.items():
                    if crit_name in option.scores:
                        score = option.scores[crit_name]
                        if criteria.criteria_type == CriteriaType.BENEFIT:
                            # 效益型：越大越好
                            normalized[opt_name][crit_name] = (score - min_score) / (max_score - min_score)
                        else:
                            # 成本型：越小越好
                            normalized[opt_name][crit_name] = (max_score - score) / (max_score - min_score)
        
        return normalized
    
    def calculate_weighted_average(self) -> List[DecisionResult]:
        """使用加权平均法计算"""
        normalized = self._normalize_scores()
        weights = self.get_normalized_weights()
        results = []
        
        for opt_name, option in self.options.items():
            criteria_scores = normalized.get(opt_name, {})
            weighted_scores = {}
            total = 0.0
            
            for crit_name, weight in weights.items():
                norm_score = criteria_scores.get(crit_name, 0)
                weighted_score = norm_score * weight
                weighted_scores[crit_name] = weighted_score
                total += weighted_score
            
            results.append(DecisionResult(
                option_name=opt_name,
                total_score=total,
                normalized_score=total,
                rank=0,
                criteria_scores=criteria_scores,
                weighted_scores=weighted_scores
            ))
        
        # 排序并设置排名
        results.sort(key=lambda x: x.total_score, reverse=True)
        for i, result in enumerate(results):
            result.rank = i + 1
        
        return results
    
    def calculate_weighted_sum(self) -> List[DecisionResult]:
        """使用加权求和法计算（不归一化分数）"""
        weights = self.get_normalized_weights()
        results = []
        
        # 获取每个标准的最大可能值
        max_scores = {}
        for crit_name in self.criteria:
            scores = [opt.scores.get(crit_name, 0) for opt in self.options.values()]
            max_scores[crit_name] = max(scores) if scores else 1
        
        for opt_name, option in self.options.items():
            criteria_scores = dict(option.scores)
            weighted_scores = {}
            total = 0.0
            
            for crit_name, weight in weights.items():
                score = option.scores.get(crit_name, 0)
                weighted_score = score * weight
                weighted_scores[crit_name] = weighted_score
                total += weighted_score
            
            # 归一化最终得分
            max_possible = sum(max_scores.get(crit_name, 1) * weight 
                             for crit_name, weight in weights.items())
            normalized_score = total / max_possible if max_possible > 0 else 0
            
            results.append(DecisionResult(
                option_name=opt_name,
                total_score=total,
                normalized_score=normalized_score,
                rank=0,
                criteria_scores=criteria_scores,
                weighted_scores=weighted_scores
            ))
        
        # 排序并设置排名
        results.sort(key=lambda x: x.total_score, reverse=True)
        for i, result in enumerate(results):
            result.rank = i + 1
        
        return results
    
    def calculate_topsis(self) -> List[DecisionResult]:
        """使用TOPSIS法计算"""
        if not self.criteria or not self.options:
            return []
        
        # 构建决策矩阵
        crit_names = list(self.criteria.keys())
        opt_names = list(self.options.keys())
        
        # 构建原始矩阵
        matrix = []
        for opt_name in opt_names:
            row = []
            for crit_name in crit_names:
                score = self.options[opt_name].scores.get(crit_name, 0)
                row.append(score)
            matrix.append(row)
        
        # 步骤1: 标准化矩阵（向量归一化）
        n_rows = len(matrix)
        n_cols = len(crit_names)
        
        # 计算每列的平方和
        col_sums = [0] * n_cols
        for row in matrix:
            for j, val in enumerate(row):
                col_sums[j] += val * val
        
        col_norms = [math.sqrt(s) if s > 0 else 1 for s in col_sums]
        
        # 标准化矩阵
        normalized_matrix = []
        for i, row in enumerate(matrix):
            norm_row = [row[j] / col_norms[j] if col_norms[j] > 0 else 0 for j in range(n_cols)]
            normalized_matrix.append(norm_row)
        
        # 步骤2: 加权标准化矩阵
        weights = self.get_normalized_weights()
        weighted_matrix = []
        for i, row in enumerate(normalized_matrix):
            weighted_row = [row[j] * weights.get(crit_names[j], 0) for j in range(n_cols)]
            weighted_matrix.append(weighted_row)
        
        # 步骤3: 确定正理想解和负理想解
        ideal_best = []  # 正理想解
        ideal_worst = []  # 负理想解
        
        for j, crit_name in enumerate(crit_names):
            col_values = [weighted_matrix[i][j] for i in range(n_rows)]
            if self.criteria[crit_name].criteria_type == CriteriaType.BENEFIT:
                ideal_best.append(max(col_values))
                ideal_worst.append(min(col_values))
            else:
                ideal_best.append(min(col_values))
                ideal_worst.append(max(col_values))
        
        # 步骤4: 计算每个选项与理想解的距离
        results = []
        for i, opt_name in enumerate(opt_names):
            row = weighted_matrix[i]
            
            # 到正理想解的距离
            dist_best = math.sqrt(sum((row[j] - ideal_best[j]) ** 2 for j in range(n_cols)))
            # 到负理想解的距离
            dist_worst = math.sqrt(sum((row[j] - ideal_worst[j]) ** 2 for j in range(n_cols)))
            
            # 相对贴近度
            total_dist = dist_best + dist_worst
            score = dist_worst / total_dist if total_dist > 0 else 0
            
            # 构建结果
            criteria_scores = {}
            weighted_scores = {}
            for j, crit_name in enumerate(crit_names):
                criteria_scores[crit_name] = normalized_matrix[i][j]
                weighted_scores[crit_name] = weighted_matrix[i][j]
            
            results.append(DecisionResult(
                option_name=opt_name,
                total_score=score,
                normalized_score=score,
                rank=0,
                criteria_scores=criteria_scores,
                weighted_scores=weighted_scores,
                details={
                    "distance_to_ideal": dist_best,
                    "distance_to_anti_ideal": dist_worst
                }
            ))
        
        # 排序并设置排名
        results.sort(key=lambda x: x.total_score, reverse=True)
        for i, result in enumerate(results):
            result.rank = i + 1
        
        return results
    
    def calculate(self, method: ScoreMethod = ScoreMethod.WEIGHTED_AVERAGE) -> List[DecisionResult]:
        """使用指定方法计算决策结果"""
        if method == ScoreMethod.WEIGHTED_AVERAGE:
            return self.calculate_weighted_average()
        elif method == ScoreMethod.WEIGHTED_SUM:
            return self.calculate_weighted_sum()
        elif method == ScoreMethod.TOPSIS:
            return self.calculate_topsis()
        elif method == ScoreMethod.AHP_SIMPLIFIED:
            return self._calculate_ahp_simplified()
        else:
            raise ValueError(f"未知的评分方法: {method}")
    
    def _calculate_ahp_simplified(self) -> List[DecisionResult]:
        """简化版层次分析法（AHP）"""
        # 简化版：使用加权几何平均，并对零值做特殊处理
        weights = self.get_normalized_weights()
        normalized = self._normalize_scores()
        
        results = []
        
        for opt_name, option in self.options.items():
            criteria_scores = normalized.get(opt_name, {})
            weighted_scores = {}
            
            # 使用加权几何平均，但避免零值问题
            product = 1.0
            for crit_name, weight in weights.items():
                norm_score = criteria_scores.get(crit_name, 0.001)  # 最小值避免零值问题
                if norm_score <= 0:
                    norm_score = 0.001  # 给一个最小值避免零值
                product *= (norm_score ** weight)
                weighted_scores[crit_name] = criteria_scores.get(crit_name, 0) * weight
            
            results.append(DecisionResult(
                option_name=opt_name,
                total_score=product,
                normalized_score=product,
                rank=0,
                criteria_scores=criteria_scores,
                weighted_scores=weighted_scores
            ))
        
        # 归一化最终得分
        total_score = sum(r.total_score for r in results)
        if total_score > 0:
            for r in results:
                r.normalized_score = r.total_score / total_score
        
        # 排序并设置排名
        results.sort(key=lambda x: x.total_score, reverse=True)
        for i, result in enumerate(results):
            result.rank = i + 1
        
        return results
    
    def sensitivity_analysis(self, criteria_name: str, 
                           weight_range: Tuple[float, float] = (0.1, 0.9),
                           steps: int = 9) -> SensitivityResult:
        """敏感性分析：调整某个标准的权重，观察结果变化"""
        if criteria_name not in self.criteria:
            raise ValueError(f"标准不存在: {criteria_name}")
        
        original_criteria = self.criteria[criteria_name]
        original_weight = original_criteria.weight
        winner_changes = []
        
        # 计算其他标准的原始总权重
        other_total = sum(c.weight for n, c in self.criteria.items() if n != criteria_name)
        
        # 临时存储
        temp_options = {name: Option(name=name, scores=opt.scores.copy()) 
                       for name, opt in self.options.items()}
        
        for i in range(steps + 1):
            # 计算当前权重
            weight = weight_range[0] + (weight_range[1] - weight_range[0]) * i / steps
            
            # 调整权重（保持其他权重比例）
            self.criteria[criteria_name].weight = weight
            if other_total > 0:
                remaining = 1.0 - weight
                for n, c in self.criteria.items():
                    if n != criteria_name:
                        c.weight = (c.weight / other_total) * remaining if other_total > 0 else remaining / (len(self.criteria) - 1)
            
            # 计算结果
            results = self.calculate_weighted_average()
            winner = results[0].option_name if results else ""
            winner_changes.append((weight, winner))
        
        # 恢复原始权重
        self.criteria[criteria_name].weight = original_weight
        for n, c in self.criteria.items():
            if n != criteria_name:
                c.weight = temp_options.get(n, Option(name="")).scores.get(n, c.weight)
        
        return SensitivityResult(
            criteria_name=criteria_name,
            original_weight=original_weight,
            weight_range=weight_range,
            winner_changes=winner_changes
        )
    
    def get_winner(self, method: ScoreMethod = ScoreMethod.WEIGHTED_AVERAGE) -> Optional[DecisionResult]:
        """获取最优选项"""
        results = self.calculate(method)
        return results[0] if results else None
    
    def get_ranking(self, method: ScoreMethod = ScoreMethod.WEIGHTED_AVERAGE) -> List[Tuple[str, float, int]]:
        """获取排名列表"""
        results = self.calculate(method)
        return [(r.option_name, r.total_score, r.rank) for r in results]
    
    def get_radar_chart_data(self) -> Dict[str, Any]:
        """生成雷达图数据"""
        normalized = self._normalize_scores()
        weights = self.get_normalized_weights()
        
        labels = list(self.criteria.keys())
        datasets = []
        
        for opt_name, option in self.options.items():
            data = []
            for crit_name in labels:
                score = normalized.get(opt_name, {}).get(crit_name, 0)
                data.append(round(score * 100, 1))  # 转换为百分比
            
            datasets.append({
                "label": opt_name,
                "data": data
            })
        
        return {
            "labels": labels,
            "datasets": datasets,
            "weights": {name: round(w * 100, 1) for name, w in weights.items()}
        }
    
    def to_report(self, method: ScoreMethod = ScoreMethod.WEIGHTED_AVERAGE) -> str:
        """生成文本报告"""
        results = self.calculate(method)
        weights = self.get_normalized_weights()
        
        lines = [
            f"{'='*60}",
            f"决策矩阵报告: {self.name}",
            f"{'='*60}",
            f"",
            f"评价标准 (权重):",
        ]
        
        for name, w in weights.items():
            crit = self.criteria[name]
            type_str = "效益" if crit.criteria_type == CriteriaType.BENEFIT else "成本"
            lines.append(f"  - {name}: {w*100:.1f}% ({type_str})")
        
        lines.extend([
            f"",
            f"评分方法: {method.value}",
            f"",
            f"{'='*60}",
            f"排名结果:",
            f"{'='*60}",
        ])
        
        for result in results:
            lines.extend([
                f"",
                f"第{result.rank}名: {result.option_name}",
                f"  总分: {result.total_score:.4f}",
                f"  归一化分数: {result.normalized_score:.4f}",
                f"  各标准得分:",
            ])
            for crit_name, score in result.weighted_scores.items():
                lines.append(f"    - {crit_name}: {score:.4f}")
        
        lines.extend([
            f"",
            f"{'='*60}",
            f"详细分数矩阵:",
            f"{'='*60}",
        ])
        
        # 表头
        header = f"{'选项':<15}"
        for crit_name in self.criteria:
            header += f"{crit_name[:10]:>12}"
        lines.append(header)
        
        # 数据行
        for opt_name, option in self.options.items():
            row = f"{opt_name[:15]:<15}"
            for crit_name in self.criteria:
                score = option.scores.get(crit_name, 0)
                row += f"{score:>12.2f}"
            lines.append(row)
        
        return "\n".join(lines)
    
    def to_json(self) -> str:
        """导出为JSON"""
        data = {
            "name": self.name,
            "description": self.description,
            "criteria": [
                {
                    "name": c.name,
                    "weight": c.weight,
                    "type": c.criteria_type.value,
                    "description": c.description
                }
                for c in self.criteria.values()
            ],
            "options": [
                {
                    "name": o.name,
                    "description": o.description,
                    "scores": o.scores,
                    "metadata": o.metadata
                }
                for o in self.options.values()
            ]
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'DecisionMatrix':
        """从JSON导入"""
        data = json.loads(json_str)
        matrix = cls(name=data.get("name", ""), description=data.get("description", ""))
        
        for c in data.get("criteria", []):
            criteria = Criteria(
                name=c["name"],
                weight=c["weight"],
                criteria_type=CriteriaType(c.get("type", "benefit")),
                description=c.get("description", "")
            )
            matrix.add_criteria(criteria)
        
        for o in data.get("options", []):
            option = Option(
                name=o["name"],
                description=o.get("description", ""),
                metadata=o.get("metadata", {})
            )
            for crit_name, score in o.get("scores", {}).items():
                option.set_score(crit_name, score)
            matrix.add_option(option)
        
        return matrix
    
    def copy(self) -> 'DecisionMatrix':
        """创建副本"""
        new_matrix = DecisionMatrix(name=self.name, description=self.description)
        
        for crit in self.criteria.values():
            new_matrix.add_criteria(Criteria(
                name=crit.name,
                weight=crit.weight,
                criteria_type=crit.criteria_type,
                description=crit.description,
                min_value=crit.min_value,
                max_value=crit.max_value
            ))
        
        for opt in self.options.values():
            new_option = Option(
                name=opt.name,
                description=opt.description,
                scores=opt.scores.copy(),
                metadata=opt.metadata.copy()
            )
            new_matrix.add_option(new_option)
        
        return new_matrix
    
    def __repr__(self) -> str:
        return f"DecisionMatrix(name='{self.name}', criteria={len(self.criteria)}, options={len(self.options)})"


# 预定义决策模板
class DecisionTemplates:
    """决策矩阵模板"""
    
    @staticmethod
    def car_purchase() -> DecisionMatrix:
        """购车决策模板"""
        matrix = DecisionMatrix(
            name="购车决策",
            description="评估不同车型的综合价值"
        )
        
        # 添加评价标准
        matrix.add_criteria_simple("价格", 0.25, CriteriaType.COST, "车辆价格（越低越好）")
        matrix.add_criteria_simple("燃油经济性", 0.20, CriteriaType.BENEFIT, "油耗表现")
        matrix.add_criteria_simple("安全性", 0.20, CriteriaType.BENEFIT, "安全评级")
        matrix.add_criteria_simple("舒适性", 0.15, CriteriaType.BENEFIT, "乘坐舒适度")
        matrix.add_criteria_simple("品牌口碑", 0.10, CriteriaType.BENEFIT, "品牌形象")
        matrix.add_criteria_simple("保值率", 0.10, CriteriaType.BENEFIT, "二手车保值能力")
        
        return matrix
    
    @staticmethod
    def job_selection() -> DecisionMatrix:
        """工作选择模板"""
        matrix = DecisionMatrix(
            name="工作选择",
            description="评估不同工作机会的综合价值"
        )
        
        matrix.add_criteria_simple("薪资", 0.25, CriteriaType.BENEFIT, "月薪水平")
        matrix.add_criteria_simple("发展空间", 0.20, CriteriaType.BENEFIT, "职业发展机会")
        matrix.add_criteria_simple("工作环境", 0.15, CriteriaType.BENEFIT, "办公环境和文化")
        matrix.add_criteria_simple("通勤时间", 0.15, CriteriaType.COST, "每天通勤时间")
        matrix.add_criteria_simple("福利待遇", 0.15, CriteriaType.BENEFIT, "保险、假期等福利")
        matrix.add_criteria_simple("工作稳定性", 0.10, CriteriaType.BENEFIT, "公司稳定性")
        
        return matrix
    
    @staticmethod
    def house_purchase() -> DecisionMatrix:
        """购房决策模板"""
        matrix = DecisionMatrix(
            name="购房决策",
            description="评估不同房产的综合价值"
        )
        
        matrix.add_criteria_simple("价格", 0.30, CriteriaType.COST, "房屋总价")
        matrix.add_criteria_simple("地段", 0.25, CriteriaType.BENEFIT, "地理位置便利性")
        matrix.add_criteria_simple("面积", 0.15, CriteriaType.BENEFIT, "房屋面积")
        matrix.add_criteria_simple("学区", 0.10, CriteriaType.BENEFIT, "学区质量")
        matrix.add_criteria_simple("小区环境", 0.10, CriteriaType.BENEFIT, "小区配套设施")
        matrix.add_criteria_simple("房龄", 0.10, CriteriaType.COST, "房屋建成年份")
        
        return matrix
    
    @staticmethod
    def product_comparison() -> DecisionMatrix:
        """产品对比模板"""
        matrix = DecisionMatrix(
            name="产品对比",
            description="对比不同产品的综合价值"
        )
        
        matrix.add_criteria_simple("价格", 0.30, CriteriaType.COST, "产品价格")
        matrix.add_criteria_simple("质量", 0.25, CriteriaType.BENEFIT, "产品质量")
        matrix.add_criteria_simple("功能", 0.20, CriteriaType.BENEFIT, "功能完整性")
        matrix.add_criteria_simple("品牌", 0.15, CriteriaType.BENEFIT, "品牌知名度")
        matrix.add_criteria_simple("售后服务", 0.10, CriteriaType.BENEFIT, "售后服务质量")
        
        return matrix
    
    @staticmethod
    def travel_destination() -> DecisionMatrix:
        """旅游目的地选择模板"""
        matrix = DecisionMatrix(
            name="旅游目的地选择",
            description="评估不同旅游目的地的吸引力"
        )
        
        matrix.add_criteria_simple("费用", 0.25, CriteriaType.COST, "旅行总费用")
        matrix.add_criteria_simple("景点", 0.25, CriteriaType.BENEFIT, "景点丰富度")
        matrix.add_criteria_simple("美食", 0.15, CriteriaType.BENEFIT, "美食体验")
        matrix.add_criteria_simple("交通便利", 0.15, CriteriaType.BENEFIT, "交通便捷程度")
        matrix.add_criteria_simple("住宿", 0.10, CriteriaType.BENEFIT, "住宿条件")
        matrix.add_criteria_simple("安全性", 0.10, CriteriaType.BENEFIT, "安全程度")
        
        return matrix


# 便捷函数
def create_decision_matrix(name: str = "决策矩阵", 
                          criteria: Optional[List[Tuple[str, float, str]]] = None,
                          options: Optional[List[Tuple[str, Dict[str, float]]]] = None) -> DecisionMatrix:
    """
    快速创建决策矩阵
    
    Args:
        name: 矩阵名称
        criteria: 标准列表 [(名称, 权重, 类型), ...]
                  类型: "benefit" 或 "cost"
        options: 选项列表 [(名称, {标准: 分数, ...}), ...]
    
    Returns:
        DecisionMatrix 实例
    
    Example:
        matrix = create_decision_matrix(
            name="手机选择",
            criteria=[
                ("价格", 0.3, "cost"),
                ("性能", 0.3, "benefit"),
                ("拍照", 0.2, "benefit"),
                ("续航", 0.2, "benefit")
            ],
            options=[
                ("手机A", {"价格": 3000, "性能": 90, "拍照": 85, "续航": 80}),
                ("手机B", {"价格": 4000, "性能": 95, "拍照": 90, "续航": 85})
            ]
        )
    """
    dm = DecisionMatrix(name=name)
    
    if criteria:
        for name, weight, ctype in criteria:
            ct = CriteriaType.BENEFIT if ctype == "benefit" else CriteriaType.COST
            dm.add_criteria_simple(name, weight, ct)
    
    if options:
        for opt_name, scores in options:
            dm.add_option_simple(opt_name, scores)
    
    return dm


def compare_options(criteria: List[Tuple[str, float, str]], 
                   options: Dict[str, Dict[str, float]],
                   method: ScoreMethod = ScoreMethod.WEIGHTED_AVERAGE) -> List[DecisionResult]:
    """
    快速比较选项
    
    Args:
        criteria: 标准列表 [(名称, 权重, 类型), ...]
        options: 选项 {名称: {标准: 分数, ...}, ...}
        method: 评分方法
    
    Returns:
        排序后的决策结果列表
    
    Example:
        results = compare_options(
            criteria=[("价格", 0.5, "cost"), ("性能", 0.5, "benefit")],
            options={
                "产品A": {"价格": 100, "性能": 80},
                "产品B": {"价格": 150, "性能": 95}
            }
        )
        print(f"推荐: {results[0].option_name}")
    """
    matrix = DecisionMatrix()
    
    for name, weight, ctype in criteria:
        ct = CriteriaType.BENEFIT if ctype == "benefit" else CriteriaType.COST
        matrix.add_criteria_simple(name, weight, ct)
    
    for opt_name, scores in options.items():
        matrix.add_option_simple(opt_name, scores)
    
    return matrix.calculate(method)


# 单例快捷函数
def weighted_score(scores: Dict[str, float], 
                  weights: Dict[str, float],
                  criteria_types: Optional[Dict[str, str]] = None) -> float:
    """
    快速计算加权得分
    
    Args:
        scores: 各标准得分
        weights: 各标准权重
        criteria_types: 各标准类型 {"标准名": "benefit/cost"}
    
    Returns:
        加权得分 (0-1)
    
    Example:
        score = weighted_score(
            scores={"价格": 100, "性能": 80},
            weights={"价格": 0.5, "性能": 0.5},
            criteria_types={"价格": "cost", "性能": "benefit"}
        )
    """
    # 归一化权重
    total_weight = sum(weights.values())
    norm_weights = {k: v/total_weight for k, v in weights.items()}
    
    # 归一化分数
    min_scores = {k: min(v.get(k, 0) for v in [scores]) for k in scores}
    max_scores = {k: max(v.get(k, 0) for v in [scores]) for k in scores}
    
    total = 0.0
    for crit_name, weight in norm_weights.items():
        if crit_name not in scores:
            continue
        
        score = scores[crit_name]
        min_s = min_scores.get(crit_name, 0)
        max_s = max_scores.get(crit_name, 1)
        
        # 归一化
        if max_s == min_s:
            norm_score = 1.0
        else:
            ctype = (criteria_types or {}).get(crit_name, "benefit")
            if ctype == "cost":
                norm_score = (max_s - score) / (max_s - min_s)
            else:
                norm_score = (score - min_s) / (max_s - min_s)
        
        total += norm_score * weight
    
    return total


if __name__ == "__main__":
    # 简单测试
    print("决策矩阵工具测试")
    print("=" * 60)
    
    # 使用模板创建购车决策
    matrix = DecisionTemplates.car_purchase()
    
    # 添加选项
    matrix.add_option_simple("车型A", {
        "价格": 15,      # 万元
        "燃油经济性": 85,
        "安全性": 90,
        "舒适性": 80,
        "品牌口碑": 75,
        "保值率": 70
    })
    
    matrix.add_option_simple("车型B", {
        "价格": 20,
        "燃油经济性": 90,
        "安全性": 95,
        "舒适性": 85,
        "品牌口碑": 90,
        "保值率": 85
    })
    
    matrix.add_option_simple("车型C", {
        "价格": 12,
        "燃油经济性": 70,
        "安全性": 80,
        "舒适性": 70,
        "品牌口碑": 65,
        "保值率": 60
    })
    
    # 计算结果
    print("\n加权平均法:")
    results = matrix.calculate(ScoreMethod.WEIGHTED_AVERAGE)
    for r in results:
        print(f"  {r.rank}. {r.option_name}: {r.total_score:.4f}")
    
    print("\nTOPSIS法:")
    results = matrix.calculate(ScoreMethod.TOPSIS)
    for r in results:
        print(f"  {r.rank}. {r.option_name}: {r.total_score:.4f}")
    
    # 生成报告
    print("\n" + matrix.to_report())