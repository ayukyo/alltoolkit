"""
wheel_picker_utils - 转盘选择器工具

功能：
- 创建可配置的选择转盘
- 支持等概率和加权概率选择
- 支持多轮选择和排除已选
- 支持历史记录和统计
- 支持自定义颜色和视觉效果
- 零外部依赖
"""

import random
import math
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple, Union
from collections import Counter


class WheelPicker:
    """转盘选择器"""
    
    def __init__(
        self,
        items: List[str],
        weights: Optional[List[float]] = None,
        colors: Optional[List[str]] = None,
        title: str = "选择转盘"
    ):
        """
        初始化转盘选择器
        
        Args:
            items: 选择项列表
            weights: 权重列表（可选），默认等权重
            colors: 颜色列表（可选），默认自动分配
            title: 转盘标题
        """
        if not items:
            raise ValueError("选择项列表不能为空")
        
        self.items = items.copy()
        self.title = title
        self._selected_history: List[Dict[str, Any]] = []
        self._excluded_items: set = set()
        
        # 设置权重
        if weights is None:
            # 等权重，归一化
            total = len(items)
            self.weights = [1.0 / total] * len(items)
        else:
            if len(weights) != len(items):
                raise ValueError("权重数量必须与选择项数量相同")
            total = sum(weights)
            if total <= 0:
                raise ValueError("权重总和必须大于0")
            self.weights = [w / total for w in weights]
        
        # 设置颜色
        if colors is None:
            self.colors = self._generate_colors(len(items))
        else:
            if len(colors) != len(items):
                raise ValueError("颜色数量必须与选择项数量相同")
            self.colors = colors.copy()
    
    def _generate_colors(self, count: int) -> List[str]:
        """自动生成颜色列表"""
        base_colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
            "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F",
            "#BB8FCE", "#85C1E9", "#F8B500", "#00CED1",
            "#FF69B4", "#32CD32", "#FFD700", "#6495ED"
        ]
        
        if count <= len(base_colors):
            return base_colors[:count]
        
        # 如果需要更多颜色，循环使用并稍微变化
        result = []
        for i in range(count):
            base_idx = i % len(base_colors)
            # 添加轻微变化
            variation = (i // len(base_colors)) * 20
            base_color = base_colors[base_idx]
            result.append(self._shift_color(base_color, variation))
        
        return result
    
    def _shift_color(self, hex_color: str, shift: int) -> str:
        """颜色微调"""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        r = min(255, max(0, r + shift))
        g = min(255, max(0, g - shift // 2))
        b = min(255, max(0, b + shift // 2))
        
        return f"#{r:02X}{g:02X}{b:02X}"
    
    def spin(
        self,
        exclude_previous: bool = False,
        exclude_count: int = 0,
        deterministic: bool = False,
        seed: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        旋转转盘进行选择
        
        Args:
            exclude_previous: 是否排除之前选择过的项目
            exclude_count: 排除最近N次选择的项目
            deterministic: 是否使用确定性算法（相同seed相同结果）
            seed: 确定性模式的种子
        
        Returns:
            选择结果字典，包含选中项、概率、角度等信息
        """
        # 获取可用项目
        available_items = []
        available_weights = []
        available_colors = []
        
        excluded_set = set()
        if exclude_previous:
            excluded_set = self._excluded_items.copy()
        elif exclude_count > 0:
            recent = [h["item"] for h in self._selected_history[-exclude_count:]]
            excluded_set = set(recent)
        
        for i, item in enumerate(self.items):
            if item not in excluded_set:
                available_items.append(item)
                available_weights.append(self.weights[i])
                available_colors.append(self.colors[i])
        
        if not available_items:
            # 如果所有项目都被排除，重置并重新选择
            available_items = self.items.copy()
            available_weights = self.weights.copy()
            available_colors = self.colors.copy()
            excluded_set = set()
        
        # 计算有效权重
        total_weight = sum(available_weights)
        normalized_weights = [w / total_weight for w in available_weights]
        
        # 选择
        if deterministic:
            if seed is None:
                seed = datetime.now().isoformat()
            hash_val = int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
            rand_val = hash_val / (16 ** 8)
        else:
            rand_val = random.random()
        
        # 累积概率选择
        cumulative = 0.0
        selected_idx = 0
        for i, weight in enumerate(normalized_weights):
            cumulative += weight
            if rand_val <= cumulative:
                selected_idx = i
                break
        
        selected_item = available_items[selected_idx]
        selected_weight = normalized_weights[selected_idx]
        selected_color = available_colors[selected_idx]
        
        # 计算角度（用于可视化）
        start_angle = sum(normalized_weights[:selected_idx]) * 360
        end_angle = start_angle + selected_weight * 360
        center_angle = start_angle + selected_weight * 180
        
        result = {
            "item": selected_item,
            "probability": selected_weight,
            "color": selected_color,
            "start_angle": start_angle,
            "end_angle": end_angle,
            "center_angle": center_angle,
            "spin_rotation": center_angle + random.randint(720, 1080),  # 多转几圈
            "timestamp": datetime.now().isoformat(),
            "seed": seed if deterministic else None,
            "available_count": len(available_items),
            "excluded_count": len(excluded_set)
        }
        
        # 记录历史
        self._selected_history.append(result)
        if exclude_previous:
            self._excluded_items.add(selected_item)
        
        return result
    
    def spin_multiple(
        self,
        count: int,
        unique: bool = True,
        exclude_previous: bool = False
    ) -> List[Dict[str, Any]]:
        """
        多次旋转
        
        Args:
            count: 选择次数
            unique: 是否保证选择结果唯一
            exclude_previous: 是否排除之前选择过的项目
        
        Returns:
            选择结果列表
        """
        results = []
        
        if unique:
            # 确保选择结果唯一
            available_count = len(self.items)
            if exclude_previous:
                available_count -= len(self._excluded_items)
            
            actual_count = min(count, available_count)
            
            for _ in range(actual_count):
                result = self.spin(exclude_previous=exclude_previous or unique)
                results.append(result)
        else:
            # 可重复选择
            for _ in range(count):
                result = self.spin(exclude_previous=exclude_previous)
                results.append(result)
        
        return results
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        获取选择历史
        
        Args:
            limit: 返回的记录数量限制
        
        Returns:
            历史记录列表
        """
        if limit is None:
            return self._selected_history.copy()
        return self._selected_history[-limit:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取选择统计
        
        Returns:
            统计信息字典
        """
        if not self._selected_history:
            return {
                "total_spins": 0,
                "distribution": {},
                "most_frequent": None,
                "least_frequent": None,
                "expected_distribution": {item: weight for item, weight in zip(self.items, self.weights)}
            }
        
        # 计算实际分布
        item_counts = Counter(h["item"] for h in self._selected_history)
        total = len(self._selected_history)
        actual_distribution = {item: count / total for item, count in item_counts.items()}
        
        # 计算偏差
        expected_distribution = {item: weight for item, weight in zip(self.items, self.weights)}
        deviation = {}
        for item in self.items:
            expected = expected_distribution.get(item, 0)
            actual = actual_distribution.get(item, 0)
            deviation[item] = abs(expected - actual)
        
        most_frequent = item_counts.most_common(1)[0] if item_counts else None
        least_frequent = min(item_counts.items(), key=lambda x: x[1]) if item_counts else None
        
        return {
            "total_spins": total,
            "distribution": dict(item_counts),
            "probability_distribution": actual_distribution,
            "expected_distribution": expected_distribution,
            "deviation": deviation,
            "most_frequent": most_frequent,
            "least_frequent": least_frequent,
            "average_deviation": sum(deviation.values()) / len(deviation) if deviation else 0
        }
    
    def reset_history(self):
        """重置历史记录"""
        self._selected_history.clear()
        self._excluded_items.clear()
    
    def reset_exclusions(self):
        """重置排除列表"""
        self._excluded_items.clear()
    
    def get_wheel_config(self) -> Dict[str, Any]:
        """
        获取转盘配置（用于可视化）
        
        Returns:
            转盘配置字典
        """
        segments = []
        cumulative_angle = 0
        
        for i, item in enumerate(self.items):
            angle = self.weights[i] * 360
            segments.append({
                "item": item,
                "weight": self.weights[i],
                "color": self.colors[i],
                "start_angle": cumulative_angle,
                "end_angle": cumulative_angle + angle,
                "center_angle": cumulative_angle + angle / 2
            })
            cumulative_angle += angle
        
        return {
            "title": self.title,
            "segments": segments,
            "item_count": len(self.items),
            "total_weight": sum(self.weights),
            "is_weighted": len(set(self.weights)) > 1
        }
    
    def add_item(
        self,
        item: str,
        weight: float = 1.0,
        color: Optional[str] = None
    ):
        """
        添加新选择项
        
        Args:
            item: 选择项名称
            weight: 权重
            color: 颜色
        """
        if item in self.items:
            raise ValueError(f"选择项 '{item}' 已存在")
        
        self.items.append(item)
        
        # 重新计算权重
        total_old = sum(w for i, w in enumerate(self.weights) if i < len(self.items) - 1)
        total_new = total_old + weight
        
        # 更新所有权重
        new_weights = []
        for i, w in enumerate(self.weights):
            if i < len(self.items) - 1:
                new_weights.append(w * total_old / total_new)
            else:
                new_weights.append(weight / total_new)
        
        self.weights = [weight / total_new for weight in ([w * total_old for w in self.weights[:-1]] + [weight])]
        
        # 添加颜色
        if color is None:
            self.colors.append(self._generate_colors(1)[0])
        else:
            self.colors.append(color)
    
    def remove_item(self, item: str):
        """
        移除选择项
        
        Args:
            item: 选择项名称
        """
        if item not in self.items:
            raise ValueError(f"选择项 '{item}' 不存在")
        
        idx = self.items.index(item)
        self.items.pop(idx)
        self.weights.pop(idx)
        self.colors.pop(idx)
        self._excluded_items.discard(item)
        
        # 重新归一化权重
        if self.weights:
            total = sum(self.weights)
            self.weights = [w / total for w in self.weights]
    
    def update_weight(self, item: str, weight: float):
        """
        更新选择项权重
        
        Args:
            item: 选择项名称
            weight: 新权重
        """
        if item not in self.items:
            raise ValueError(f"选择项 '{item}' 不存在")
        
        idx = self.items.index(item)
        old_weight = self.weights[idx]
        total_old = sum(self.weights)
        total_new = total_old - old_weight + weight
        
        for i in range(len(self.weights)):
            if i == idx:
                self.weights[i] = weight / total_new
            else:
                self.weights[i] = self.weights[i] * total_old / total_new
    
    def __str__(self) -> str:
        """字符串表示"""
        weighted_str = "加权" if len(set(self.weights)) > 1 else "等权重"
        return f"WheelPicker({self.title}, {len(self.items)}项, {weighted_str})"
    
    def __repr__(self) -> str:
        return self.__str__()


def create_simple_wheel(items: List[str], title: str = "选择转盘") -> WheelPicker:
    """
    创建简单等权重转盘
    
    Args:
        items: 选择项列表
        title: 转盘标题
    
    Returns:
        WheelPicker 实例
    """
    return WheelPicker(items, title=title)


def create_weighted_wheel(
    items: List[str],
    weights: List[float],
    title: str = "加权选择转盘"
) -> WheelPicker:
    """
    创建加权转盘
    
    Args:
        items: 选择项列表
        weights: 权重列表
        title: 转盘标题
    
    Returns:
        WheelPicker 实例
    """
    return WheelPicker(items, weights=weights, title=title)


def quick_pick(items: List[str], count: int = 1, unique: bool = True) -> List[str]:
    """
    快速选择（不保留历史）
    
    Args:
        items: 选择项列表
        count: 选择数量
        unique: 是否唯一
    
    Returns:
        选择结果列表
    """
    if unique:
        if count > len(items):
            count = len(items)
        return random.sample(items, count)
    else:
        return random.choices(items, k=count)


def weighted_pick(
    items: List[str],
    weights: List[float],
    count: int = 1,
    unique: bool = False
) -> List[str]:
    """
    加权快速选择
    
    Args:
        items: 选择项列表
        weights: 权重列表
        count: 选择数量
        unique: 是否唯一（加权模式下唯一选择较复杂）
    
    Returns:
        选择结果列表
    """
    if len(items) != len(weights):
        raise ValueError("选择项和权重数量必须相同")
    
    if unique:
        # 加权唯一选择：使用不放回抽样
        result = []
        remaining_items = items.copy()
        remaining_weights = weights.copy()
        
        for _ in range(min(count, len(items))):
            total = sum(remaining_weights)
            normalized = [w / total for w in remaining_weights]
            
            cumulative = 0.0
            rand_val = random.random()
            selected_idx = 0
            
            for i, w in enumerate(normalized):
                cumulative += w
                if rand_val <= cumulative:
                    selected_idx = i
                    break
            
            result.append(remaining_items[selected_idx])
            remaining_items.pop(selected_idx)
            remaining_weights.pop(selected_idx)
        
        return result
    else:
        total = sum(weights)
        normalized = [w / total for w in weights]
        return random.choices(items, weights=normalized, k=count)


def pair_up(items: List[str], randomize: bool = True) -> List[Tuple[str, str]]:
    """
    将列表项配对
    
    Args:
        items: 选择项列表
        randomize: 是否随机配对
    
    Returns:
        配对列表
    """
    if len(items) < 2:
        return []
    
    working_list = items.copy()
    if randomize:
        random.shuffle(working_list)
    
    pairs = []
    while len(working_list) >= 2:
        pairs.append((working_list.pop(), working_list.pop()))
    
    # 如果有剩余项，单独返回
    if working_list:
        pairs.append((working_list[0], None))
    
    return pairs


def group_items(
    items: List[str],
    group_count: int,
    randomize: bool = True,
    balance: bool = True
) -> List[List[str]]:
    """
    将列表项分组
    
    Args:
        items: 选择项列表
        group_count: 组数
        randomize: 是否随机分组
        balance: 是否平衡每组人数
    
    Returns:
        分组列表
    """
    if group_count <= 0:
        raise ValueError("组数必须大于0")
    
    if group_count > len(items):
        # 如果组数超过项目数，每组最多一个
        return [[item] for item in items[:group_count]]
    
    working_list = items.copy()
    if randomize:
        random.shuffle(working_list)
    
    groups: List[List[str]] = [[] for _ in range(group_count)]
    
    if balance:
        # 平衡分配
        base_count = len(items) // group_count
        extra = len(items) % group_count
        
        idx = 0
        for i in range(group_count):
            group_size = base_count + (1 if i < extra else 0)
            groups[i] = working_list[idx:idx + group_size]
            idx += group_size
    else:
        # 简单轮流分配
        for i, item in enumerate(working_list):
            groups[i % group_count].append(item)
    
    return groups


def round_robin_picker(
    items: List[str],
    rounds: int = 1
) -> List[str]:
    """
    轮转选择器（公平轮流选择）
    
    Args:
        items: 选择项列表
        rounds: 轮次
    
    Returns:
        选择序列
    """
    result = []
    for _ in range(rounds):
        result.extend(items)
    return result


def deterministic_pick(
    items: List[str],
    seed: str,
    weights: Optional[List[float]] = None
) -> str:
    """
    确定性选择（相同种子产生相同结果）
    
    Args:
        items: 选择项列表
        seed: 种子字符串
        weights: 权重列表
    
    Returns:
        选择结果
    """
    hash_val = int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
    
    if weights is None:
        idx = hash_val % len(items)
    else:
        total = sum(weights)
        normalized = [w / total for w in weights]
        rand_val = hash_val / (16 ** 8)
        
        cumulative = 0.0
        idx = 0
        for i, w in enumerate(normalized):
            cumulative += w
            if rand_val <= cumulative:
                idx = i
                break
    
    return items[idx]


def shuffle_with_seed(items: List[str], seed: str) -> List[str]:
    """
    使用种子随机打乱列表
    
    Args:
        items: 选择项列表
        seed: 种子字符串
    
    Returns:
        打乱后的列表
    """
    hash_val = int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
    result = items.copy()
    
    # 使用 Fisher-Yates 算法，用哈希值模拟随机
    for i in range(len(result) - 1, 0, -1):
        # 为每个交换生成一个新的"随机"值
        swap_hash = int(hashlib.md5(f"{seed}_{i}".encode()).hexdigest()[:8], 16)
        j = swap_hash % (i + 1)
        result[i], result[j] = result[j], result[i]
    
    return result


def generate_rotation_schedule(
    items: List[str],
    days: int,
    start_date: Optional[str] = None,
    shuffle: bool = True
) -> List[Dict[str, Any]]:
    """
    生成轮转排班表
    
    Args:
        items: 选择项列表（如人员）
        days: 天数
        start_date: 开始日期（YYYY-MM-DD格式）
        shuffle: 是否随机打乱起始顺序
    
    Returns:
        排班表列表
    """
    from datetime import datetime, timedelta
    
    if start_date is None:
        start = datetime.now()
    else:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    
    working_list = items.copy()
    if shuffle:
        random.shuffle(working_list)
    
    schedule = []
    for day in range(days):
        date = start + timedelta(days=day)
        idx = day % len(working_list)
        
        schedule.append({
            "date": date.strftime("%Y-%m-%d"),
            "day_of_week": date.strftime("%A"),
            "item": working_list[idx],
            "rotation_position": idx,
            "is_first_rotation": idx == 0
        })
    
    return schedule


class TournamentWheel:
    """锦标赛转盘（适合竞赛场景）"""
    
    def __init__(self, participants: List[str], title: str = "锦标赛"):
        """
        初始化锦标赛转盘
        
        Args:
            participants: 参赛者列表
            title: 标题
        """
        self.participants = participants.copy()
        self.title = title
        self.wheel = WheelPicker(participants, title=title)
        self.matches: List[Dict[str, Any]] = []
    
    def generate_matches(
        self,
        rounds: int = 1,
        randomize: bool = True
    ) -> List[Dict[str, Any]]:
        """
        生成对阵表
        
        Args:
            rounds: 轮次
            randomize: 是否随机对阵
        
        Returns:
            对阵表
        """
        self.matches = []
        
        for round_num in range(1, rounds + 1):
            if randomize:
                shuffled = random.sample(self.participants, len(self.participants))
            else:
                shuffled = self.participants.copy()
            
            pairs = pair_up(shuffled, randomize=False)
            
            for match_idx, (p1, p2) in enumerate(pairs):
                if p2 is None:
                    # 没有对手，自动晋级
                    self.matches.append({
                        "round": round_num,
                        "match_number": match_idx + 1,
                        "player1": p1,
                        "player2": p2,
                        "status": "auto_advance",
                        "winner": p1
                    })
                else:
                    self.matches.append({
                        "round": round_num,
                        "match_number": match_idx + 1,
                        "player1": p1,
                        "player2": p2,
                        "status": "pending",
                        "winner": None
                    })
        
        return self.matches
    
    def pick_winner(self, round_num: int, match_number: int) -> str:
        """
        随机选择比赛赢家
        
        Args:
            round_num: 轮次
            match_number: 比赛编号
        
        Returns:
            赢家名称
        """
        for match in self.matches:
            if match["round"] == round_num and match["match_number"] == match_number:
                if match["status"] == "pending" and match["player2"]:
                    result = self.wheel.spin()
                    # 只选择两名参赛者之一
                    winner = random.choice([match["player1"], match["player2"]])
                    match["winner"] = winner
                    match["status"] = "completed"
                    return winner
                elif match["status"] == "auto_advance":
                    return match["winner"]
        
        raise ValueError(f"未找到轮次 {round_num} 的比赛 {match_number}")
    
    def get_bracket(self) -> Dict[str, Any]:
        """
        获取对阵图
        
        Returns:
            对阵图数据
        """
        return {
            "title": self.title,
            "participants": self.participants,
            "participant_count": len(self.participants),
            "matches": self.matches,
            "rounds": max(m["round"] for m in self.matches) if self.matches else 0,
            "pending_matches": len([m for m in self.matches if m["status"] == "pending"]),
            "completed_matches": len([m for m in self.matches if m["status"] == "completed"])
        }


class PrizeWheel:
    """奖品转盘（适合抽奖场景）"""
    
    def __init__(
        self,
        prizes: List[str],
        weights: Optional[List[float]] = None,
        allow_repeat: bool = False
    ):
        """
        初始化奖品转盘
        
        Args:
            prizes: 奖品列表
            weights: 奖品权重（概率）
            allow_repeat: 是否允许重复抽取同一奖品
        """
        self.wheel = WheelPicker(prizes, weights=weights, title="奖品转盘")
        self.allow_repeat = allow_repeat
        self.winners: List[Dict[str, Any]] = []
        self.available_prizes = prizes.copy()
    
    def draw(self, participant: Optional[str] = None) -> Dict[str, Any]:
        """
        抽奖
        
        Args:
            participant: 参与者名称（可选）
        
        Returns:
            抽奖结果
        """
        if not self.available_prizes and not self.allow_repeat:
            return {
                "success": False,
                "message": "所有奖品已抽完",
                "prize": None,
                "participant": participant
            }
        
        result = self.wheel.spin(exclude_previous=not self.allow_repeat)
        
        winner_record = {
            "prize": result["item"],
            "probability": result["probability"],
            "participant": participant,
            "timestamp": result["timestamp"],
            "success": True
        }
        
        self.winners.append(winner_record)
        
        # 如果不允许重复，移除已抽奖品
        if not self.allow_repeat:
            self.available_prizes.remove(result["item"])
        
        return winner_record
    
    def draw_multiple(
        self,
        participants: List[str],
        unique_per_person: bool = True
    ) -> List[Dict[str, Any]]:
        """
        多人抽奖
        
        Args:
            participants: 参与者列表
            unique_per_person: 每人只能获得一个奖品
        
        Returns:
        抽奖结果列表
        """
        results = []
        for participant in participants:
            if not self.available_prizes:
                results.append({
                    "success": False,
                    "message": "奖品已抽完",
                    "participant": participant
                })
                break
            
            result = self.draw(participant)
            results.append(result)
            
            if unique_per_person and result["success"]:
                # 已获得奖品的参与者不再参与后续抽奖
                pass
        
        return results
    
    def get_winners(self) -> List[Dict[str, Any]]:
        """获取中奖名单"""
        return self.winners.copy()
    
    def get_remaining_prizes(self) -> List[str]:
        """获取剩余奖品"""
        return self.available_prizes.copy()


class DecisionWheel:
    """决策转盘（适合日常决策场景）"""
    
    # 预设决策模板
    PRESETS = {
        "food": ["火锅", "烧烤", "炒菜", "快餐", "面食", "寿司", "披萨", "汉堡"],
        "movie_genre": ["动作", "喜剧", "科幻", "恐怖", "爱情", "动画", "悬疑", "纪录片"],
        "activity": ["看电影", "逛街", "运动", "游戏", "阅读", "做饭", "散步", "休息"],
        "travel": ["海边", "山区", "城市", "古镇", "温泉", "露营", "自驾游", "民宿"],
        "exercise": ["跑步", "游泳", "瑜伽", "篮球", "足球", "羽毛球", "健身", "骑行"],
        "drink": ["咖啡", "茶", "果汁", "奶茶", "可乐", "啤酒", "红酒", "水"],
        "music_genre": ["流行", "摇滚", "古典", "爵士", "电子", "民谣", "说唱", "蓝调"]
    }
    
    def __init__(self, options: Optional[List[str]] = None, preset: Optional[str] = None):
        """
        初始化决策转盘
        
        Args:
            options: 自定义选项列表
            preset: 预设模板名称
        """
        if preset:
            if preset not in self.PRESETS:
                raise ValueError(f"未知预设模板: {preset}")
            self.options = self.PRESETS[preset].copy()
            self.preset_name = preset
        elif options:
            self.options = options.copy()
            self.preset_name = None
        else:
            raise ValueError("请提供选项列表或预设模板名称")
        
        self.wheel = WheelPicker(self.options, title="决策转盘")
        self.decision_history: List[Dict[str, Any]] = []
    
    def make_decision(
        self,
        exclude_recent: int = 0,
        person: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        做出决策
        
        Args:
            exclude_recent: 排除最近N次的选择
            person: 做决策的人
        
        Returns:
            决策结果
        """
        result = self.wheel.spin(exclude_count=exclude_recent)
        
        decision_record = {
            "decision": result["item"],
            "probability": result["probability"],
            "person": person,
            "timestamp": result["timestamp"],
            "preset": self.preset_name,
            "options_count": len(self.options)
        }
        
        self.decision_history.append(decision_record)
        return decision_record
    
    def get_presets(self) -> Dict[str, List[str]]:
        """获取所有预设模板"""
        return self.PRESETS.copy()
    
    def add_option(self, option: str):
        """添加选项"""
        if option not in self.options:
            self.options.append(option)
            self.wheel.add_item(option)
    
    def remove_option(self, option: str):
        """移除选项"""
        if option in self.options:
            self.options.remove(option)
            self.wheel.remove_item(option)
    
    def get_decision_stats(self) -> Dict[str, Any]:
        """获取决策统计"""
        if not self.decision_history:
            return {"total_decisions": 0}
        
        decision_counts = Counter(d["decision"] for d in self.decision_history)
        
        return {
            "total_decisions": len(self.decision_history),
            "distribution": dict(decision_counts),
            "most_common": decision_counts.most_common(1)[0],
            "least_common": min(decision_counts.items(), key=lambda x: x[1]),
            "preset_used": self.preset_name
        }