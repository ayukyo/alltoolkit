"""
Grade Utilities 使用示例

展示如何使用成绩计算工具的各种功能
"""

from mod import (
    Course, GradeRecord, GradeConverter, GPACalculator,
    GradeAnalyzer, GradePredictor, TranscriptFormatter,
    calculate_gpa, calculate_weighted_average, get_grade_level
)


def example_basic_gpa():
    """基础 GPA 计算"""
    print("=" * 60)
    print("示例 1: 基础 GPA 计算")
    print("=" * 60)
    
    # 方式 1: 使用便捷函数
    scores = [90, 85, 78, 92, 88]
    gpa = calculate_gpa(scores)
    print(f"成绩: {scores}")
    print(f"GPA: {gpa}")
    
    # 带学分加权
    scores_with_credits = [90, 85, 78, 92, 88]
    credits = [4, 3, 3, 2, 2]
    weighted_gpa = calculate_gpa(scores_with_credits, credits)
    print(f"\n带学分加权:")
    print(f"成绩: {scores_with_credits}")
    print(f"学分: {credits}")
    print(f"GPA: {weighted_gpa}")
    
    print()


def example_weighted_average():
    """加权平均分计算"""
    print("=" * 60)
    print("示例 2: 加权平均分计算")
    print("=" * 60)
    
    scores = [92, 88, 85, 78, 95]
    credits = [4, 3, 3, 2, 1]
    
    avg = calculate_weighted_average(scores, credits)
    print(f"成绩: {scores}")
    print(f"学分: {credits}")
    print(f"加权平均分: {avg}")
    print()


def example_grade_conversion():
    """成绩转换"""
    print("=" * 60)
    print("示例 3: 成绩转换")
    print("=" * 60)
    
    test_scores = [95, 87, 75, 62, 55]
    
    print(f"{'分数':>6} | {'4.0 GPA':>10} | {'5.0 GPA':>10} | {'字母':>6} | {'等级':>8}")
    print("-" * 55)
    
    for score in test_scores:
        gpa_4 = GradeConverter.percentage_to_gpa(score, 4.0)
        gpa_5 = GradeConverter.percentage_to_gpa(score, 5.0)
        letter = GradeConverter.percentage_to_letter(score)
        chinese = GradeConverter.percentage_to_chinese(score)
        print(f"{score:>6} | {gpa_4:>10.1f} | {gpa_5:>10.1f} | {letter:>6} | {chinese:>8}")
    
    print()


def example_course_management():
    """课程管理"""
    print("=" * 60)
    print("示例 4: 课程管理与成绩记录")
    print("=" * 60)
    
    # 创建学生成绩记录
    student = GradeRecord(
        student_id="2023001",
        student_name="张三"
    )
    
    # 添加课程
    courses = [
        Course(name="高等数学", score=92, credit=5, semester="2023-1", course_type="required"),
        Course(name="大学英语", score=88, credit=4, semester="2023-1", course_type="required"),
        Course(name="程序设计", score=95, credit=3, semester="2023-1", course_type="required"),
        Course(name="体育", score=85, credit=1, semester="2023-1", course_type="elective"),
        Course(name="线性代数", score=90, credit=3, semester="2023-2", course_type="required"),
        Course(name="数据结构", score=87, credit=4, semester="2023-2", course_type="required"),
        Course(name="音乐鉴赏", score=92, credit=2, semester="2023-2", course_type="elective"),
    ]
    
    for course in courses:
        student.add_course(course)
    
    # 计算总学分
    total_credits = sum(c.credit for c in student.courses)
    print(f"学生: {student.student_name} ({student.student_id})")
    print(f"总学分: {total_credits}")
    print(f"课程数: {len(student.courses)}")
    
    # 按学期查看
    print("\n按学期统计:")
    for semester in student.get_semesters():
        sem_courses = student.get_courses_by_semester(semester)
        gpa = GPACalculator.calculate_weighted_gpa(sem_courses)
        print(f"  {semester}: {len(sem_courses)} 门课, GPA: {gpa:.2f}")
    
    print()


def example_grade_analysis():
    """成绩分析"""
    print("=" * 60)
    print("示例 5: 成绩分析")
    print("=" * 60)
    
    courses = [
        Course(name="高等数学", score=92, credit=5, course_type="required"),
        Course(name="大学英语", score=88, credit=4, course_type="required"),
        Course(name="程序设计", score=95, credit=3, course_type="required"),
        Course(name="体育", score=78, credit=1, course_type="elective"),
        Course(name="线性代数", score=85, credit=3, course_type="required"),
        Course(name="数据结构", score=82, credit=4, course_type="required"),
        Course(name="音乐鉴赏", score=90, credit=2, course_type="elective"),
        Course(name="离散数学", score=75, credit=3, course_type="required"),
        Course(name="概率统计", score=88, credit=3, course_type="required"),
        Course(name="美术鉴赏", score=95, credit=2, course_type="elective"),
    ]
    
    # 成绩分布
    dist = GradeAnalyzer.get_distribution(courses)
    print("成绩分布:")
    for level, count in dist.items():
        bar = "█" * count
        print(f"  {level}: {bar} ({count})")
    
    # 统计信息
    stats = GradeAnalyzer.get_statistics(courses)
    print(f"\n统计信息:")
    print(f"  最高分: {stats['max']}")
    print(f"  最低分: {stats['min']}")
    print(f"  平均分: {stats['mean']}")
    print(f"  中位数: {stats['median']}")
    print(f"  标准差: {stats['std']}")
    
    # 按课程类型比较
    print("\n按课程类型:")
    by_type = GradeAnalyzer.compare_by_type(courses)
    for course_type, type_stats in by_type.items():
        print(f"  {course_type}: 平均分 {type_stats['mean']}, GPA {type_stats['gpa']:.2f}")
    
    print()


def example_trend_analysis():
    """趋势分析"""
    print("=" * 60)
    print("示例 6: 学期成绩趋势分析")
    print("=" * 60)
    
    semesters_data = {
        "大一上": [
            Course(name="高等数学", score=78, credit=5, semester="大一上"),
            Course(name="大学英语", score=80, credit=4, semester="大一上"),
            Course(name="程序设计", score=85, credit=3, semester="大一上"),
        ],
        "大一下": [
            Course(name="线性代数", score=82, credit=3, semester="大一下"),
            Course(name="数据结构", score=88, credit=4, semester="大一下"),
            Course(name="离散数学", score=85, credit=3, semester="大一下"),
        ],
        "大二上": [
            Course(name="算法设计", score=90, credit=4, semester="大二上"),
            Course(name="操作系统", score=88, credit=4, semester="大二上"),
            Course(name="计算机网络", score=92, credit=3, semester="大二上"),
        ],
        "大二下": [
            Course(name="数据库原理", score=91, credit=4, semester="大二下"),
            Course(name="编译原理", score=89, credit=3, semester="大二下"),
            Course(name="软件工程", score=93, credit=3, semester="大二下"),
        ],
    }
    
    trend = GradeAnalyzer.analyze_trend(semesters_data, 4.0)
    
    print(f"成绩趋势: {trend['trend']}")
    print(f"平均变化: {'+' if trend['avg_change'] > 0 else ''}{trend['avg_change']:.3f}")
    print(f"最新 GPA: {trend['latest_gpa']:.2f}")
    print(f"最佳 GPA: {trend['best_gpa']:.2f}")
    print(f"最差 GPA: {trend['worst_gpa']:.2f}")
    
    print("\n各学期 GPA:")
    for record in trend['history']:
        print(f"  {record['semester']}: {record['gpa']:.2f}")
    
    print()


def example_grade_prediction():
    """成绩预测"""
    print("=" * 60)
    print("示例 7: 成绩预测")
    print("=" * 60)
    
    # 预测期末需要多少分
    print("场景: 平时成绩 82 分 (占 70%)，期末占 30%")
    print("目标: 总成绩达到 85 分")
    result = GradePredictor.predict_final(82, 85, 0.3)
    print(f"  需要期末成绩: {result['needed_final']:.1f} 分")
    print(f"  是否可行: {'是' if result['possible'] else '否'}")
    
    print("\n场景: 平时成绩 75 分 (占 70%)，期末占 30%")
    print("目标: 总成绩达到 90 分")
    result = GradePredictor.predict_final(75, 90, 0.3)
    print(f"  需要期末成绩: {result['needed_final']:.1f} 分")
    print(f"  是否可行: {'是' if result['possible'] else '否 (超过100分)'}")
    
    # 预测毕业 GPA
    print("\n场景: 当前 GPA 3.2，已修 90 学分，剩余 30 学分")
    print("目标: 毕业时 GPA 达到 3.5")
    result = GradePredictor.predict_gpa(3.2, 30, 3.5, 120)
    print(f"  剩余课程需要 GPA: {result['needed_gpa']:.2f}")
    print(f"  是否可行: {'是' if result['possible'] else '否 (需要超过4.0)'}")
    
    print()


def example_transcript():
    """成绩单生成"""
    print("=" * 60)
    print("示例 8: 成绩单生成")
    print("=" * 60)
    
    student = GradeRecord(
        student_id="2021001234",
        student_name="李明"
    )
    
    courses = [
        Course(name="高等数学", score=92, credit=5, semester="2021-1"),
        Course(name="大学英语I", score=88, credit=4, semester="2021-1"),
        Course(name="程序设计基础", score=95, credit=3, semester="2021-1"),
        Course(name="体育I", score=85, credit=1, semester="2021-1"),
        Course(name="线性代数", score=90, credit=3, semester="2021-2"),
        Course(name="大学英语II", score=86, credit=4, semester="2021-2"),
        Course(name="数据结构", score=91, credit=4, semester="2021-2"),
        Course(name="体育II", score=82, credit=1, semester="2021-2"),
        Course(name="离散数学", score=88, credit=3, semester="2022-1"),
        Course(name="算法设计", score=93, credit=4, semester="2022-1"),
        Course(name="操作系统", score=87, credit=4, semester="2022-1"),
        Course(name="计算机网络", score=90, credit=3, semester="2022-1"),
    ]
    
    for course in courses:
        student.add_course(course)
    
    # 打印成绩单摘要
    print(TranscriptFormatter.format_summary(student))
    
    # 打印课程列表
    print("\n课程详情:")
    print(TranscriptFormatter.format_course_list(student.courses))
    
    print()


def example_ranking():
    """排名计算"""
    print("=" * 60)
    print("示例 9: 成绩排名计算")
    print("=" * 60)
    
    # 模拟班级成绩
    class_scores = [
        Course(name="学生A", score=95),
        Course(name="学生B", score=88),
        Course(name="学生C", score=92),
        Course(name="学生D", score=78),
        Course(name="学生E", score=85),
        Course(name="学生F", score=90),
        Course(name="学生G", score=82),
        Course(name="学生H", score=88),
        Course(name="学生I", score=76),
        Course(name="学生J", score=91),
    ]
    
    # 查找学生F的排名
    target = class_scores[5]  # 学生F，90分
    rank_info = GradeAnalyzer.get_rank(target, class_scores)
    
    print(f"{target.name} 的排名信息:")
    print(f"  排名: 第 {rank_info['rank']} 名")
    print(f"  总人数: {rank_info['total']} 人")
    print(f"  百分位: 前 {rank_info['percentile']}%")
    
    print()


def main():
    """运行所有示例"""
    example_basic_gpa()
    example_weighted_average()
    example_grade_conversion()
    example_course_management()
    example_grade_analysis()
    example_trend_analysis()
    example_grade_prediction()
    example_transcript()
    example_ranking()
    
    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()