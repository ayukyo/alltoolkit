"""
Grade Utilities 测试

测试所有核心功能
"""

import unittest
from mod import (
    Course, GradeRecord, GradeConverter, GPACalculator,
    GradeAnalyzer, GradePredictor, TranscriptFormatter,
    calculate_gpa, calculate_weighted_average, get_grade_level, get_letter_grade
)


class TestCourse(unittest.TestCase):
    """测试 Course 类"""
    
    def test_create_course(self):
        """测试创建课程"""
        course = Course(name="数学", score=85, credit=4.0, semester="2023-1")
        self.assertEqual(course.name, "数学")
        self.assertEqual(course.score, 85)
        self.assertEqual(course.credit, 4.0)
        self.assertEqual(course.semester, "2023-1")
    
    def test_negative_score_raises(self):
        """测试负数成绩抛出异常"""
        with self.assertRaises(ValueError):
            Course(name="测试", score=-10)
    
    def test_negative_credit_raises(self):
        """测试负数学分抛出异常"""
        with self.assertRaises(ValueError):
            Course(name="测试", score=80, credit=-1)


class TestGradeConverter(unittest.TestCase):
    """测试成绩转换器"""
    
    def test_percentage_to_gpa_4(self):
        """测试百分制转 4.0 GPA"""
        self.assertEqual(GradeConverter.percentage_to_gpa(95, 4.0), 4.0)
        self.assertEqual(GradeConverter.percentage_to_gpa(87, 4.0), 3.7)
        self.assertEqual(GradeConverter.percentage_to_gpa(80, 4.0), 3.0)
        self.assertEqual(GradeConverter.percentage_to_gpa(65, 4.0), 1.5)  # 65 在 64-67 区间
        self.assertEqual(GradeConverter.percentage_to_gpa(55, 4.0), 0.0)
    
    def test_percentage_to_gpa_5(self):
        """测试百分制转 5.0 GPA"""
        self.assertEqual(GradeConverter.percentage_to_gpa(98, 5.0), 5.0)
        self.assertEqual(GradeConverter.percentage_to_gpa(92, 5.0), 4.5)
        self.assertEqual(GradeConverter.percentage_to_gpa(82, 5.0), 3.5)
        self.assertEqual(GradeConverter.percentage_to_gpa(55, 5.0), 0.0)
    
    def test_percentage_to_letter(self):
        """测试百分制转字母等级"""
        self.assertEqual(GradeConverter.percentage_to_letter(95), 'A')
        self.assertEqual(GradeConverter.percentage_to_letter(85), 'B')
        self.assertEqual(GradeConverter.percentage_to_letter(75), 'C')
        self.assertEqual(GradeConverter.percentage_to_letter(65), 'D')
        self.assertEqual(GradeConverter.percentage_to_letter(50), 'F')
    
    def test_percentage_to_chinese(self):
        """测试百分制转中文等级"""
        self.assertEqual(GradeConverter.percentage_to_chinese(95), '优秀')
        self.assertEqual(GradeConverter.percentage_to_chinese(85), '良好')
        self.assertEqual(GradeConverter.percentage_to_chinese(75), '中等')
        self.assertEqual(GradeConverter.percentage_to_chinese(65), '及格')
        self.assertEqual(GradeConverter.percentage_to_chinese(50), '不及格')
    
    def test_letter_to_gpa(self):
        """测试字母等级转 GPA"""
        self.assertEqual(GradeConverter.letter_to_gpa('A'), 4.0)
        self.assertEqual(GradeConverter.letter_to_gpa('B+'), 3.3)
        self.assertEqual(GradeConverter.letter_to_gpa('C'), 2.0)
        self.assertEqual(GradeConverter.letter_to_gpa('F'), 0.0)
    
    def test_gpa_to_percentage(self):
        """测试 GPA 转百分制"""
        # 4.0 制
        self.assertEqual(GradeConverter.gpa_to_percentage(4.0, 4.0), 95.0)
        self.assertGreater(GradeConverter.gpa_to_percentage(3.0, 4.0), 70)
        
        # 5.0 制
        self.assertEqual(GradeConverter.gpa_to_percentage(5.0, 5.0), 100.0)
        self.assertEqual(GradeConverter.gpa_to_percentage(4.0, 5.0), 80.0)
    
    def test_invalid_score_raises(self):
        """测试无效成绩抛出异常"""
        with self.assertRaises(ValueError):
            GradeConverter.percentage_to_gpa(150, 4.0)
        
        with self.assertRaises(ValueError):
            GradeConverter.percentage_to_gpa(-10, 4.0)


class TestGPACalculator(unittest.TestCase):
    """测试 GPA 计算器"""
    
    def setUp(self):
        """设置测试数据"""
        self.courses = [
            Course(name="数学", score=90, credit=4),
            Course(name="英语", score=85, credit=3),
            Course(name="物理", score=80, credit=3),
            Course(name="化学", score=75, credit=2),
        ]
    
    def test_calculate_weighted_gpa(self):
        """测试计算加权 GPA"""
        gpa = GPACalculator.calculate_weighted_gpa(self.courses, 4.0)
        self.assertGreater(gpa, 0)
        self.assertLess(gpa, 4.0)
    
    def test_calculate_weighted_average(self):
        """测试计算加权平均分"""
        avg = GPACalculator.calculate_weighted_average(self.courses)
        # (90*4 + 85*3 + 80*3 + 75*2) / 12 = 83.75
        self.assertAlmostEqual(avg, 83.75, places=2)
    
    def test_calculate_credit_points(self):
        """测试计算学分绩点"""
        result = GPACalculator.calculate_credit_points(self.courses, 4.0)
        self.assertEqual(result["total_credits"], 12)
        self.assertGreater(result["total_points"], 0)
        self.assertGreater(result["average_gpa"], 0)
    
    def test_exclude_failed(self):
        """测试排除不及格课程"""
        courses_with_fail = self.courses + [Course(name="体育", score=50, credit=1)]
        
        gpa_with_fail = GPACalculator.calculate_weighted_gpa(courses_with_fail, 4.0, True)
        gpa_without_fail = GPACalculator.calculate_weighted_gpa(courses_with_fail, 4.0, False)
        
        # 排除不及格后 GPA 应该更高
        self.assertGreater(gpa_without_fail, gpa_with_fail)
    
    def test_empty_courses(self):
        """测试空课程列表"""
        gpa = GPACalculator.calculate_weighted_gpa([], 4.0)
        self.assertEqual(gpa, 0.0)
        
        avg = GPACalculator.calculate_weighted_average([])
        self.assertEqual(avg, 0.0)


class TestGradeAnalyzer(unittest.TestCase):
    """测试成绩分析器"""
    
    def setUp(self):
        """设置测试数据"""
        self.courses = [
            Course(name="数学", score=95, credit=4),
            Course(name="英语", score=85, credit=3),
            Course(name="物理", score=88, credit=3),
            Course(name="化学", score=72, credit=2),
            Course(name="历史", score=55, credit=2),
        ]
    
    def test_get_distribution(self):
        """测试成绩分布"""
        dist = GradeAnalyzer.get_distribution(self.courses)
        self.assertEqual(dist["优秀"], 1)  # 95
        self.assertEqual(dist["良好"], 2)  # 85, 88
        self.assertEqual(dist["中等"], 1)  # 72
        self.assertEqual(dist["及格"], 0)
        self.assertEqual(dist["不及格"], 1)  # 55
    
    def test_get_statistics(self):
        """测试成绩统计"""
        stats = GradeAnalyzer.get_statistics(self.courses)
        self.assertEqual(stats["count"], 5)
        self.assertEqual(stats["max"], 95)
        self.assertEqual(stats["min"], 55)
        self.assertGreater(stats["mean"], 0)
        self.assertGreater(stats["std"], 0)
    
    def test_get_rank(self):
        """测试排名计算"""
        target = self.courses[1]  # 英语 85 分
        rank_info = GradeAnalyzer.get_rank(target, self.courses)
        
        self.assertEqual(rank_info["rank"], 3)  # 第三名 (95, 88, 85...)
        self.assertEqual(rank_info["total"], 5)
        self.assertEqual(rank_info["percentile"], 60.0)  # 3/5 * 100
    
    def test_analyze_trend(self):
        """测试趋势分析"""
        semesters_data = {
            "2022-1": [
                Course(name="数学", score=80, credit=4, semester="2022-1"),
                Course(name="英语", score=75, credit=3, semester="2022-1"),
            ],
            "2022-2": [
                Course(name="数学", score=85, credit=4, semester="2022-2"),
                Course(name="英语", score=80, credit=3, semester="2022-2"),
            ],
            "2023-1": [
                Course(name="数学", score=90, credit=4, semester="2023-1"),
                Course(name="英语", score=88, credit=3, semester="2023-1"),
            ],
        }
        
        trend = GradeAnalyzer.analyze_trend(semesters_data, 4.0)
        self.assertEqual(trend["trend"], "上升")
        self.assertGreater(trend["avg_change"], 0)
    
    def test_compare_by_type(self):
        """测试按类型比较"""
        courses = [
            Course(name="数学", score=90, credit=4, course_type="required"),
            Course(name="物理", score=85, credit=3, course_type="required"),
            Course(name="音乐", score=95, credit=2, course_type="elective"),
            Course(name="美术", score=88, credit=2, course_type="elective"),
        ]
        
        result = GradeAnalyzer.compare_by_type(courses)
        self.assertIn("required", result)
        self.assertIn("elective", result)
        self.assertEqual(result["required"]["count"], 2)
        self.assertEqual(result["elective"]["count"], 2)


class TestGradePredictor(unittest.TestCase):
    """测试成绩预测器"""
    
    def test_predict_final_needed(self):
        """测试预测期末所需成绩"""
        # 当前 80 分 (占 70%)，目标 85 分，期末占 30%
        # 85 = 80 * 0.7 + x * 0.3
        # x = (85 - 56) / 0.3 = 96.67
        result = GradePredictor.predict_final(80, 85, 0.3)
        self.assertAlmostEqual(result["needed_final"], 96.67, places=1)
        self.assertTrue(result["possible"])
    
    def test_predict_final_impossible(self):
        """测试无法达到目标的情况"""
        result = GradePredictor.predict_final(60, 90, 0.3)
        # (90 - 60*0.7) / 0.3 = (90 - 42) / 0.3 = 160
        self.assertFalse(result["possible"])
    
    def test_predict_gpa_needed(self):
        """测试预测所需 GPA"""
        # 当前 GPA 3.0 (已修 60 学分)，目标 GPA 3.5 (总共 120 学分)
        # 3.5 * 120 = 3.0 * 60 + x * 60
        # x = (420 - 180) / 60 = 4.0
        result = GradePredictor.predict_gpa(3.0, 60, 3.5, 120)
        self.assertAlmostEqual(result["needed_gpa"], 4.0, places=2)
        self.assertTrue(result["possible"])
    
    def test_predict_gpa_impossible(self):
        """测试 GPA 目标无法达到"""
        result = GradePredictor.predict_gpa(2.0, 60, 4.0, 120)
        self.assertFalse(result["possible"])


class TestTranscriptFormatter(unittest.TestCase):
    """测试成绩单格式化器"""
    
    def test_format_summary(self):
        """测试格式化摘要"""
        record = GradeRecord(
            student_id="2023001",
            student_name="张三"
        )
        record.add_course(Course(name="数学", score=90, credit=4))
        record.add_course(Course(name="英语", score=85, credit=3))
        
        summary = TranscriptFormatter.format_summary(record)
        
        self.assertIn("张三", summary)
        self.assertIn("2023001", summary)
        self.assertIn("课程总数: 2", summary)
        self.assertIn("GPA:", summary)
    
    def test_format_course_list(self):
        """测试格式化课程列表"""
        courses = [
            Course(name="数学", score=90, credit=4),
            Course(name="英语", score=85, credit=3),
        ]
        
        output = TranscriptFormatter.format_course_list(courses)
        
        self.assertIn("数学", output)
        self.assertIn("英语", output)
        self.assertIn("优秀", output)  # 90 分优秀
        self.assertIn("良好", output)  # 85 分良好


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_calculate_gpa_simple(self):
        """测试简单 GPA 计算"""
        gpa = calculate_gpa([90, 85, 80])
        self.assertGreater(gpa, 3.0)
    
    def test_calculate_gpa_with_credits(self):
        """测试带学分的 GPA 计算"""
        gpa = calculate_gpa([90, 80], [4, 2])
        # 90(4.0)*4 + 80(3.0)*2 = 16 + 6 = 22 / 6 ≈ 3.67
        self.assertGreater(gpa, 3.5)
    
    def test_calculate_weighted_average_simple(self):
        """测试简单加权平均"""
        avg = calculate_weighted_average([90, 80, 70])
        self.assertEqual(avg, 80.0)
    
    def test_calculate_weighted_average_with_credits(self):
        """测试带学分的加权平均"""
        avg = calculate_weighted_average([90, 80], [4, 2])
        # (90*4 + 80*2) / 6 = 520 / 6 ≈ 86.67
        self.assertAlmostEqual(avg, 86.67, places=1)
    
    def test_get_grade_level(self):
        """测试获取成绩等级"""
        self.assertEqual(get_grade_level(95), "优秀")
        self.assertEqual(get_grade_level(85), "良好")
        self.assertEqual(get_grade_level(55), "不及格")
    
    def test_get_letter_grade(self):
        """测试获取字母等级"""
        self.assertEqual(get_letter_grade(95), "A")
        self.assertEqual(get_letter_grade(75), "C")
        self.assertEqual(get_letter_grade(55), "F")


class TestGradeRecord(unittest.TestCase):
    """测试成绩记录"""
    
    def test_add_course(self):
        """测试添加课程"""
        record = GradeRecord()
        record.add_course(Course(name="数学", score=90))
        self.assertEqual(len(record.courses), 1)
    
    def test_get_courses_by_semester(self):
        """测试按学期获取课程"""
        record = GradeRecord()
        record.add_course(Course(name="数学", score=90, semester="2023-1"))
        record.add_course(Course(name="英语", score=85, semester="2023-1"))
        record.add_course(Course(name="物理", score=80, semester="2023-2"))
        
        courses = record.get_courses_by_semester("2023-1")
        self.assertEqual(len(courses), 2)
    
    def test_get_semesters(self):
        """测试获取所有学期"""
        record = GradeRecord()
        record.add_course(Course(name="数学", score=90, semester="2023-2"))
        record.add_course(Course(name="英语", score=85, semester="2023-1"))
        record.add_course(Course(name="物理", score=80, semester="2022-2"))
        
        semesters = record.get_semesters()
        self.assertEqual(semesters, ["2022-2", "2023-1", "2023-2"])


if __name__ == '__main__':
    unittest.main(verbosity=2)