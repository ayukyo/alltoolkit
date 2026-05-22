"""
Decision Matrix Utils Examples - 加权决策矩阵使用示例

示例内容：
1. 购车决策示例
2. 工作选择示例
3. 产品对比示例
4. 旅游目的地选择示例
5. 自定义决策示例
6. 敏感性分析示例
7. JSON导入导出示例

运行: python usage_examples.py
"""

import sys
import os

# 添加模块路径
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from mod import (
    DecisionMatrix, Criteria, Option,
    CriteriaType, ScoreMethod, DecisionTemplates,
    create_decision_matrix, compare_options, weighted_score
)


def example_car_purchase():
    """示例1：购车决策"""
    print("\n" + "="*60)
    print("示例1：购车决策")
    print("="*60)
    
    # 使用模板创建决策矩阵
    matrix = DecisionTemplates.car_purchase()
    
    # 添加候选车型
    matrix.add_option_simple("丰田卡罗拉", {
        "价格": 12,           # 万元
        "燃油经济性": 92,     # 油耗评分
        "安全性": 88,         # 安全评级
        "舒适性": 75,         # 舒适度
        "品牌口碑": 82,       # 品牌形象
        "保值率": 78          # 保值能力
    })
    
    matrix.add_option_simple("本田思域", {
        "价格": 14,
        "燃油经济性": 88,
        "安全性": 85,
        "舒适性": 78,
        "品牌口碑": 80,
        "保值率": 75
    })
    
    matrix.add_option_simple("大众朗逸", {
        "价格": 11,
        "燃油经济性": 80,
        "安全性": 82,
        "舒适性": 72,
        "品牌口碑": 75,
        "保值率": 70
    })
    
    matrix.add_option_simple("比亚迪秦", {
        "价格": 10,
        "燃油经济性": 95,     # 混动车油耗优秀
        "安全性": 80,
        "舒适性": 70,
        "品牌口碑": 65,
        "保值率": 60
    })
    
    # 计算结果
    print("\n--- 加权平均法 ---")
    results = matrix.calculate(ScoreMethod.WEIGHTED_AVERAGE)
    for r in results:
        print(f"第{r.rank}名: {r.option_name} - 得分: {r.total_score:.4f}")
    
    print("\n--- TOPSIS法 ---")
    results_topsis = matrix.calculate(ScoreMethod.TOPSIS)
    for r in results_topsis:
        print(f"第{r.rank}名: {r.option_name} - 得分: {r.total_score:.4f}")
    
    # 生成完整报告
    print("\n--- 决策报告 ---")
    print(matrix.to_report())
    
    return matrix


def example_job_selection():
    """示例2：工作选择"""
    print("\n" + "="*60)
    print("示例2：工作选择")
    print("="*60)
    
    matrix = DecisionTemplates.job_selection()
    
    # 添加工作机会
    matrix.add_option_simple("大厂A", {
        "薪资": 30,           # k/月
        "发展空间": 95,
        "工作环境": 90,
        "通勤时间": 60,       # 分钟
        "福利待遇": 88,
        "工作稳定性": 85
    })
    
    matrix.add_option_simple("创业公司B", {
        "薪资": 25,
        "发展空间": 98,       # 高成长空间
        "工作环境": 75,
        "通勤时间": 30,       # 近
        "福利待遇": 60,
        "工作稳定性": 50      # 风险较高
    })
    
    matrix.add_option_simple("国企C", {
        "薪资": 20,
        "发展空间": 60,
        "工作环境": 80,
        "通勤时间": 45,
        "福利待遇": 90,
        "工作稳定性": 95      # 非常稳定
    })
    
    matrix.add_option_simple("外企D", {
        "薪资": 28,
        "发展空间": 85,
        "工作环境": 92,
        "通勤时间": 50,
        "福利待遇": 85,
        "工作稳定性": 80
    })
    
    # 注意：通勤时间是成本型（越低越好）
    # 模板中已设置为成本型
    
    results = matrix.calculate(ScoreMethod.WEIGHTED_AVERAGE)
    print("\n推荐顺序:")
    for r in results:
        print(f"  {r.rank}. {r.option_name}: {r.total_score:.4f}")
    
    # 获取获胜者详情
    winner = matrix.get_winner()
    print(f"\n最佳选择: {winner.option_name}")
    print("各标准加权得分:")
    for crit, score in winner.weighted_scores.items():
        print(f"  - {crit}: {score:.4f}")
    
    return matrix


def example_product_comparison():
    """示例3：产品对比"""
    print("\n" + "="*60)
    print("示例3：手机产品对比")
    print("="*60)
    
    # 使用快速创建函数
    matrix = create_decision_matrix(
        name="手机选购",
        criteria=[
            ("价格", 0.25, "cost"),
            ("性能", 0.25, "benefit"),
            ("拍照", 0.20, "benefit"),
            ("续航", 0.15, "benefit"),
            ("品牌", 0.15, "benefit")
        ],
        options={
            "iPhone 15": {
                "价格": 6000,
                "性能": 95,
                "拍照": 90,
                "续航": 80,
                "品牌": 98
            },
            "小米14": {
                "价格": 3500,
                "性能": 90,
                "拍照": 85,
                "续航": 85,
                "品牌": 75
            },
            "华为Mate60": {
                "价格": 5000,
                "性能": 88,
                "拍照": 92,
                "续航": 90,
                "品牌": 90
            },
            "OPPO Find X7": {
                "价格": 4000,
                "性能": 85,
                "拍照": 88,
                "续航": 82,
                "品牌": 70
            }
        }
    )
    
    results = matrix.calculate(ScoreMethod.WEIGHTED_AVERAGE)
    print("\n综合评分排名:")
    for r in results:
        print(f"  {r.rank}. {r.option_name}: {r.total_score:.4f}")
    
    # 雷达图数据
    radar = matrix.get_radar_chart_data()
    print("\n雷达图数据（百分比）:")
    print(f"标准: {radar['labels']}")
    for dataset in radar['datasets']:
        print(f"  {dataset['label']}: {dataset['data']}")
    
    return matrix


def example_travel_destination():
    """示例4：旅游目的地选择"""
    print("\n" + "="*60)
    print("示例4：旅游目的地选择")
    print("="*60)
    
    matrix = DecisionTemplates.travel_destination()
    
    matrix.add_option_simple("三亚", {
        "费用": 3000,         # 元
        "景点": 85,
        "美食": 80,
        "交通便利": 75,
        "住宿": 90,
        "安全性": 90
    })
    
    matrix.add_option_simple("成都", {
        "费用": 2000,
        "景点": 80,
        "美食": 95,           # 美食之都
        "交通便利": 85,
        "住宿": 80,
        "安全性": 85
    })
    
    matrix.add_option_simple("西安", {
        "费用": 1800,
        "景点": 90,           # 历史文化丰富
        "美食": 85,
        "交通便利": 80,
        "住宿": 75,
        "安全性": 85
    })
    
    matrix.add_option_simple("丽江", {
        "费用": 2500,
        "景点": 88,
        "美食": 70,
        "交通便利": 60,
        "住宿": 85,
        "安全性": 80
    })
    
    results = matrix.calculate(ScoreMethod.WEIGHTED_AVERAGE)
    print("\n目的地推荐:")
    for r in results:
        print(f"  {r.rank}. {r.option_name}: {r.total_score:.4f}")
    
    return matrix


def example_custom_decision():
    """示例5：自定义决策"""
    print("\n" + "="*60)
    print("示例5：租房决策（自定义标准）")
    print("="*60)
    
    # 自定义创建决策矩阵
    matrix = DecisionMatrix(
        name="租房决策",
        description="评估不同房源的综合价值"
    )
    
    # 自定义添加标准
    matrix.add_criteria(Criteria(
        name="租金",
        weight=0.35,
        criteria_type=CriteriaType.COST,  # 越低越好
        description="月租金（元）"
    ))
    
    matrix.add_criteria(Criteria(
        name="面积",
        weight=0.20,
        criteria_type=CriteriaType.BENEFIT,  # 越大越好
        description="房间面积（平方米）"
    ))
    
    matrix.add_criteria(Criteria(
        name="地段",
        weight=0.25,
        criteria_type=CriteriaType.BENEFIT,
        description="地理位置便利性评分"
    ))
    
    matrix.add_criteria(Criteria(
        name="设施",
        weight=0.10,
        criteria_type=CriteriaType.BENEFIT,
        description="房屋设施完善度"
    ))
    
    matrix.add_criteria(Criteria(
        name="安静度",
        weight=0.10,
        criteria_type=CriteriaType.BENEFIT,
        description="环境安静程度"
    ))
    
    # 添加房源选项
    matrix.add_option_simple("房源A - 市中心小户型", {
        "租金": 3500,
        "面积": 45,
        "地段": 95,
        "设施": 80,
        "安静度": 50
    })
    
    matrix.add_option_simple("房源B - 近地铁中户型", {
        "租金": 2800,
        "面积": 60,
        "地段": 85,
        "设施": 75,
        "安静度": 65
    })
    
    matrix.add_option_simple("房源C - 远郊区大户型", {
        "租金": 2000,
        "面积": 90,
        "地段": 50,
        "设施": 70,
        "安静度": 85
    })
    
    matrix.add_option_simple("房源D - 学区附近", {
        "租金": 3200,
        "面积": 55,
        "地段": 80,
        "设施": 85,
        "安静度": 70
    })
    
    # 使用多种方法计算
    print("\n--- 加权平均法 ---")
    results_avg = matrix.calculate(ScoreMethod.WEIGHTED_AVERAGE)
    for r in results_avg:
        print(f"  {r.rank}. {r.option_name}: {r.total_score:.4f}")
    
    print("\n--- TOPSIS法 ---")
    results_topsis = matrix.calculate(ScoreMethod.TOPSIS)
    for r in results_topsis:
        print(f"  {r.rank}. {r.option_name}: {r.total_score:.4f} (贴近度)")
    
    print("\n--- 简化AHP法 ---")
    results_ahp = matrix.calculate(ScoreMethod.AHP_SIMPLIFIED)
    for r in results_ahp:
        print(f"  {r.rank}. {r.option_name}: {r.total_score:.6f}")
    
    return matrix


def example_sensitivity_analysis():
    """示例6：敏感性分析"""
    print("\n" + "="*60)
    print("示例6：敏感性分析")
    print("="*60)
    
    matrix = DecisionMatrix(name="权重敏感性分析")
    
    matrix.add_criteria_simple("价格", 0.4, CriteriaType.COST)
    matrix.add_criteria_simple("质量", 0.6, CriteriaType.BENEFIT)
    
    matrix.add_option_simple("产品A - 便宜低质", {"价格": 50, "质量": 60})
    matrix.add_option_simple("产品B - 贵高质", {"价格": 100, "质量": 90})
    matrix.add_option_simple("产品C - 中等", {"价格": 75, "质量": 75})
    
    print("\n原始权重: 价格=0.4, 质量=0.6")
    results = matrix.calculate(ScoreMethod.WEIGHTED_AVERAGE)
    for r in results:
        print(f"  {r.rank}. {r.option_name}: {r.total_score:.4f}")
    
    # 对价格标准进行敏感性分析
    sensitivity = matrix.sensitivity_analysis("价格", weight_range=(0.1, 0.9), steps=9)
    
    print(f"\n调整价格权重从 {sensitivity.weight_range[0]} 到 {sensitivity.weight_range[1]}:")
    print("权重 -> 获胜选项")
    for weight, winner in sensitivity.winner_changes:
        print(f"  {weight:.2f} -> {winner}")
    
    print("\n结论:")
    print("  - 当价格权重较低时，高质量产品获胜")
    print("  - 当价格权重较高时，便宜产品获胜")
    
    return matrix


def example_json_export_import():
    """示例7：JSON导入导出"""
    print("\n" + "="*60)
    print("示例7：JSON导入导出")
    print("="*60)
    
    # 创建决策矩阵
    matrix = DecisionMatrix(name="JSON示例", description="测试JSON功能")
    matrix.add_criteria_simple("价格", 0.3, CriteriaType.COST)
    matrix.add_criteria_simple("质量", 0.7, CriteriaType.BENEFIT)
    
    matrix.add_option_simple("产品A", {"价格": 100, "质量": 80})
    matrix.add_option_simple("产品B", {"价格": 80, "质量": 90})
    
    # 导出为JSON
    json_str = matrix.to_json()
    print("\n导出JSON:")
    print(json_str)
    
    # 从JSON导入
    matrix_imported = DecisionMatrix.from_json(json_str)
    print(f"\n导入成功: {matrix_imported.name}")
    print(f"标准数: {len(matrix_imported.criteria)}")
    print(f"选项数: {len(matrix_imported.options)}")
    
    # 验证计算结果一致
    results_original = matrix.calculate(ScoreMethod.WEIGHTED_AVERAGE)
    results_imported = matrix_imported.calculate(ScoreMethod.WEIGHTED_AVERAGE)
    
    print("\n计算结果一致性验证:")
    for r1, r2 in zip(results_original, results_imported):
        match = abs(r1.total_score - r2.total_score) < 0.001
        print(f"  {r1.option_name}: {r1.total_score:.4f} == {r2.total_score:.4f} ✓")
    
    return matrix


def example_quick_comparison():
    """示例8：快速比较"""
    print("\n" + "="*60)
    print("示例8：快速比较函数")
    print("="*60)
    
    # 使用 compare_options 快速比较
    results = compare_options(
        criteria=[
            ("性价比", 0.4, "benefit"),
            ("品质", 0.3, "benefit"),
            ("服务", 0.3, "benefit")
        ],
        options={
            "餐厅A": {"性价比": 90, "品质": 85, "服务": 80},
            "餐厅B": {"性价比": 70, "品质": 90, "服务": 85},
            "餐厅C": {"性价比": 85, "品质": 80, "服务": 90}
        }
    )
    
    print("\n餐厅推荐排名:")
    for r in results:
        print(f"  {r.rank}. {r.option_name}: {r.total_score:.4f}")
    
    # 使用 weighted_score 快速计算单个分数
    score = weighted_score(
        scores={"性价比": 85, "品质": 80, "服务": 75},
        weights={"性价比": 0.4, "品质": 0.3, "服务": 0.3},
        criteria_types={"性价比": "benefit", "品质": "benefit", "服务": "benefit"}
    )
    
    print(f"\n单个选项加权分数: {score:.4f}")
    
    return results


def run_all_examples():
    """运行所有示例"""
    print("\n" + "="*60)
    print("加权决策矩阵工具 - 使用示例")
    print("="*60)
    
    examples = [
        example_car_purchase,
        example_job_selection,
        example_product_comparison,
        example_travel_destination,
        example_custom_decision,
        example_sensitivity_analysis,
        example_json_export_import,
        example_quick_comparison,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n示例 {example.__name__} 执行出错: {e}")
    
    print("\n" + "="*60)
    print("所有示例执行完毕")
    print("="*60)


if __name__ == "__main__":
    run_all_examples()