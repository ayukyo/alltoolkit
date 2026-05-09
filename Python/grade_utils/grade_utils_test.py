#!/usr/bin/env python3
"""Grade Utils Tests"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    GradeSystem, Course, GradeRecord, GradeConverter, GPACalculator,
    GradeAnalyzer, GradePredictor, TranscriptFormatter,
    calculate_gpa, calculate_weighted_average, get_grade_level, get_letter_grade
)


class TestOutcomeCollector:
    """收集测试结果"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, name):
        self.passed += 1
        print(f"✓ {name}")
    
    def add_fail(self, name, msg):
        self.failed += 1
        self.errors.append((name, msg))
        print(f"✗ {name}: {msg}")
    
    def report(self):
        print(f"\n{'='*60}")
        print(f"Grade Utils Tests: {self.passed} passed, {self.failed} failed")
        if self.errors:
            print(f"\nFailed tests:")
            for name, msg in self.errors:
                print(f"  - {name}: {msg}")
        print(f"{'='*60}")
        return self.failed == 0


def run_tests():
    results = TestOutcomeCollector()
    
    # Test 1: Course creation
    try:
        course = Course(name="数学", score=90, credit=4)
        assert course.name == "数学"
        assert course.score == 90
        assert course.credit == 4
        assert course.course_type == "required"
        results.add_pass("Course creation")
    except Exception as e:
        results.add_fail("Course creation", str(e))
    
    # Test 2: Course validation - negative score
    try:
        try:
            Course(name="Test", score=-10, credit=1)
            results.add_fail("Course validation - negative score", "Should raise ValueError")
        except ValueError:
            pass
        results.add_pass("Course validation - negative score")
    except Exception as e:
        results.add_fail("Course validation - negative score", str(e))
    
    # Test 3: Course validation - negative credit
    try:
        try:
            Course(name="Test", score=90, credit=-1)
            results.add_fail("Course validation - negative credit", "Should raise ValueError")
        except ValueError:
            pass
        results.add_pass("Course validation - negative credit")
    except Exception as e:
        results.add_fail("Course validation - negative credit", str(e))
    
    # Test 4: GradeConverter - percentage to GPA 4.0
    try:
        assert GradeConverter.percentage_to_gpa(95, 4.0) == 4.0
        assert GradeConverter.percentage_to_gpa(87, 4.0) == 3.7
        assert GradeConverter.percentage_to_gpa(82, 4.0) == 3.3
        assert GradeConverter.percentage_to_gpa(78, 4.0) == 3.0
        assert GradeConverter.percentage_to_gpa(75, 4.0) == 2.7
        assert GradeConverter.percentage_to_gpa(72, 4.0) == 2.3
        assert GradeConverter.percentage_to_gpa(68, 4.0) == 2.0
        assert GradeConverter.percentage_to_gpa(64, 4.0) == 1.5
        assert GradeConverter.percentage_to_gpa(60, 4.0) == 1.0
        assert GradeConverter.percentage_to_gpa(55, 4.0) == 0.0
        results.add_pass("GradeConverter percentage to GPA 4.0")
    except Exception as e:
        results.add_fail("GradeConverter percentage to GPA 4.0", str(e))
    
    # Test 5: GradeConverter - percentage to GPA 5.0
    try:
        assert GradeConverter.percentage_to_gpa(98, 5.0) == 5.0
        assert GradeConverter.percentage_to_gpa(92, 5.0) == 4.5
        assert GradeConverter.percentage_to_gpa(87, 5.0) == 4.0
        assert GradeConverter.percentage_to_gpa(82, 5.0) == 3.5
        assert GradeConverter.percentage_to_gpa(77, 5.0) == 3.0
        assert GradeConverter.percentage_to_gpa(72, 5.0) == 2.5
        assert GradeConverter.percentage_to_gpa(67, 5.0) == 2.0
        assert GradeConverter.percentage_to_gpa(62, 5.0) == 1.5
        assert GradeConverter.percentage_to_gpa(55, 5.0) == 0.0
        results.add_pass("GradeConverter percentage to GPA 5.0")
    except Exception as e:
        results.add_fail("GradeConverter percentage to GPA 5.0", str(e))
    
    # Test 6: GradeConverter - percentage to letter
    try:
        assert GradeConverter.percentage_to_letter(95) == 'A'
        assert GradeConverter.percentage_to_letter(85) == 'B'
        assert GradeConverter.percentage_to_letter(75) == 'C'
        assert GradeConverter.percentage_to_letter(65) == 'D'
        assert GradeConverter.percentage_to_letter(55) == 'F'
        results.add_pass("GradeConverter percentage to letter")
    except Exception as e:
        results.add_fail("GradeConverter percentage to letter", str(e))
    
    # Test 7: GradeConverter - percentage to Chinese
    try:
        assert GradeConverter.percentage_to_chinese(95) == '优秀'
        assert GradeConverter.percentage_to_chinese(85) == '良好'
        assert GradeConverter.percentage_to_chinese(75) == '中等'
        assert GradeConverter.percentage_to_chinese(65) == '及格'
        assert GradeConverter.percentage_to_chinese(55) == '不及格'
        results.add_pass("GradeConverter percentage to Chinese")
    except Exception as e:
        results.add_fail("GradeConverter percentage to Chinese", str(e))
    
    # Test 8: GradeConverter - letter to GPA
    try:
        assert GradeConverter.letter_to_gpa('A+') == 4.0
        assert GradeConverter.letter_to_gpa('A') == 4.0
        assert GradeConverter.letter_to_gpa('B+') == 3.3
        assert GradeConverter.letter_to_gpa('B') == 3.0
        assert GradeConverter.letter_to_gpa('C') == 2.0
        assert GradeConverter.letter_to_gpa('F') == 0.0
        results.add_pass("GradeConverter letter to GPA")
    except Exception as e:
        results.add_fail("GradeConverter letter to GPA", str(e))
    
    # Test 9: GradeConverter - GPA to percentage
    try:
        perc = GradeConverter.gpa_to_percentage(4.0, 4.0)
        assert perc == 95.0
        
        perc = GradeConverter.gpa_to_percentage(3.0, 4.0)
        assert 75 <= perc <= 85
        
        perc = GradeConverter.gpa_to_percentage(5.0, 5.0)
        assert perc == 100
        results.add_pass("GradeConverter GPA to percentage")
    except Exception as e:
        results.add_fail("GradeConverter GPA to percentage", str(e))
    
    # Test 10: GPACalculator - weighted GPA
    try:
        courses = [
            Course(name="数学", score=90, credit=4),
            Course(name="英语", score=85, credit=3),
            Course(name="物理", score=78, credit=2),
        ]
        gpa = GPACalculator.calculate_weighted_gpa(courses, 4.0)
        assert 3.0 <= gpa <= 4.0
        results.add_pass("GPACalculator weighted GPA")
    except Exception as e:
        results.add_fail("GPACalculator weighted GPA", str(e))
    
    # Test 11: GPACalculator - weighted average
    try:
        courses = [
            Course(name="数学", score=90, credit=4),
            Course(name="英语", score=80, credit=2),
        ]
        avg = GPACalculator.calculate_weighted_average(courses)
        # (90*4 + 80*2) / 6 = 86.67
        assert 85 <= avg <= 88
        results.add_pass("GPACalculator weighted average")
    except Exception as e:
        results.add_fail("GPACalculator weighted average", str(e))
    
    # Test 12: GPACalculator - credit points
    try:
        courses = [
            Course(name="数学", score=90, credit=4),
            Course(name="英语", score=80, credit=2),
        ]
        result = GPACalculator.calculate_credit_points(courses, 4.0)
        assert result['total_credits'] == 6
        assert result['total_points'] > 0
        assert result['average_gpa'] > 0
        results.add_pass("GPACalculator credit points")
    except Exception as e:
        results.add_fail("GPACalculator credit points", str(e))
    
    # Test 13: GradeAnalyzer - distribution
    try:
        courses = [
            Course(name="课程1", score=95, credit=1),
            Course(name="课程2", score=85, credit=1),
            Course(name="课程3", score=75, credit=1),
            Course(name="课程4", score=65, credit=1),
            Course(name="课程5", score=55, credit=1),
        ]
        dist = GradeAnalyzer.get_distribution(courses)
        assert dist['优秀'] == 1
        assert dist['良好'] == 1
        assert dist['中等'] == 1
        assert dist['及格'] == 1
        assert dist['不及格'] == 1
        results.add_pass("GradeAnalyzer distribution")
    except Exception as e:
        results.add_fail("GradeAnalyzer distribution", str(e))
    
    # Test 14: GradeAnalyzer - statistics
    try:
        courses = [
            Course(name="课程1", score=90, credit=1),
            Course(name="课程2", score=80, credit=1),
            Course(name="课程3", score=70, credit=1),
        ]
        stats = GradeAnalyzer.get_statistics(courses)
        assert stats['max'] == 90
        assert stats['min'] == 70
        assert stats['mean'] == 80
        assert stats['count'] == 3
        results.add_pass("GradeAnalyzer statistics")
    except Exception as e:
        results.add_fail("GradeAnalyzer statistics", str(e))
    
    # Test 15: GradeAnalyzer - rank
    try:
        courses = [
            Course(name="课程1", score=90, credit=1),
            Course(name="课程2", score=80, credit=1),
            Course(name="课程3", score=70, credit=1),
        ]
        target = courses[1]  # score=80
        rank_info = GradeAnalyzer.get_rank(target, courses)
        assert rank_info['rank'] == 2
        assert rank_info['total'] == 3
        assert rank_info['percentile'] == 66.7
        results.add_pass("GradeAnalyzer rank")
    except Exception as e:
        results.add_fail("GradeAnalyzer rank", str(e))
    
    # Test 16: GradeAnalyzer - compare by type
    try:
        courses = [
            Course(name="必修1", score=90, credit=4, course_type="required"),
            Course(name="必修2", score=80, credit=3, course_type="required"),
            Course(name="选修1", score=85, credit=2, course_type="elective"),
        ]
        comparison = GradeAnalyzer.compare_by_type(courses)
        assert 'required' in comparison
        assert 'elective' in comparison
        assert comparison['required']['mean'] == 85
        results.add_pass("GradeAnalyzer compare by type")
    except Exception as e:
        results.add_fail("GradeAnalyzer compare by type", str(e))
    
    # Test 17: GradeAnalyzer - trend analysis
    try:
        semesters_data = {
            "2023-1": [Course(name="课程", score=80, credit=1)],
            "2023-2": [Course(name="课程", score=85, credit=1)],
            "2024-1": [Course(name="课程", score=90, credit=1)],
        }
        trend = GradeAnalyzer.analyze_trend(semesters_data, 4.0)
        assert trend['trend'] == '上升'
        assert trend['avg_change'] > 0
        results.add_pass("GradeAnalyzer trend analysis")
    except Exception as e:
        results.add_fail("GradeAnalyzer trend analysis", str(e))
    
    # Test 18: GradePredictor - predict final
    try:
        result = GradePredictor.predict_final(80, 90, 0.3)
        # (90 - 80*0.7) / 0.3 = (90 - 56)/0.3 = 113.33
        expected = round((90 - 80 * 0.7) / 0.3, 2)
        assert result['needed_final'] == expected
        results.add_pass("GradePredictor predict final")
    except Exception as e:
        results.add_fail("GradePredictor predict final", str(e))
    
    # Test 19: GradePredictor - predict GPA
    try:
        result = GradePredictor.predict_gpa(3.0, 20, 3.5, 60)
        # (3.5*60 - 3.0*40) / 20 = (210 - 120)/20 = 4.5
        needed = round((3.5 * 60 - 3.0 * 40) / 20, 3)
        assert result['needed_gpa'] == needed
        results.add_pass("GradePredictor predict GPA")
    except Exception as e:
        results.add_fail("GradePredictor predict GPA", str(e))
    
    # Test 20: GradeRecord
    try:
        record = GradeRecord(student_id="001", student_name="张三")
        record.add_course(Course(name="数学", score=90, credit=4, semester="2023-1"))
        record.add_course(Course(name="英语", score=85, credit=3, semester="2023-2"))
        
        assert len(record.courses) == 2
        assert len(record.get_courses_by_semester("2023-1")) == 1
        assert "2023-1" in record.get_semesters()
        results.add_pass("GradeRecord")
    except Exception as e:
        results.add_fail("GradeRecord", str(e))
    
    # Test 21: TranscriptFormatter - summary
    try:
        record = GradeRecord(student_id="001", student_name="张三")
        record.add_course(Course(name="数学", score=90, credit=4))
        record.add_course(Course(name="英语", score=80, credit=3))
        
        summary = TranscriptFormatter.format_summary(record, 4.0)
        assert "张三" in summary
        assert "001" in summary
        assert "GPA" in summary
        results.add_pass("TranscriptFormatter summary")
    except Exception as e:
        results.add_fail("TranscriptFormatter summary", str(e))
    
    # Test 22: TranscriptFormatter - course list
    try:
        courses = [
            Course(name="数学", score=90, credit=4),
            Course(name="英语", score=80, credit=3),
        ]
        list_str = TranscriptFormatter.format_course_list(courses, 4.0)
        assert "数学" in list_str
        assert "英语" in list_str
        results.add_pass("TranscriptFormatter course list")
    except Exception as e:
        results.add_fail("TranscriptFormatter course list", str(e))
    
    # Test 23: Convenience function - calculate_gpa
    try:
        gpa = calculate_gpa([90, 80, 70], [4, 3, 2], 4.0)
        assert 3.0 <= gpa <= 4.0
        results.add_pass("Convenience calculate_gpa")
    except Exception as e:
        results.add_fail("Convenience calculate_gpa", str(e))
    
    # Test 24: Convenience function - calculate_weighted_average
    try:
        avg = calculate_weighted_average([90, 80], [4, 2])
        # (90*4 + 80*2) / 6 = 86.67
        assert 85 <= avg <= 88
        results.add_pass("Convenience calculate_weighted_average")
    except Exception as e:
        results.add_fail("Convenience calculate_weighted_average", str(e))
    
    # Test 25: Convenience function - get_grade_level
    try:
        assert get_grade_level(95) == '优秀'
        assert get_grade_level(85) == '良好'
        assert get_grade_level(55) == '不及格'
        results.add_pass("Convenience get_grade_level")
    except Exception as e:
        results.add_fail("Convenience get_grade_level", str(e))
    
    # Test 26: Convenience function - get_letter_grade
    try:
        assert get_letter_grade(95) == 'A'
        assert get_letter_grade(85) == 'B'
        assert get_letter_grade(55) == 'F'
        results.add_pass("Convenience get_letter_grade")
    except Exception as e:
        results.add_fail("Convenience get_letter_grade", str(e))
    
    # Test 27: Empty courses handling
    try:
        gpa = GPACalculator.calculate_weighted_gpa([], 4.0)
        assert gpa == 0.0
        
        avg = GPACalculator.calculate_weighted_average([])
        assert avg == 0.0
        
        stats = GradeAnalyzer.get_statistics([])
        assert stats['count'] == 0
        results.add_pass("Empty courses handling")
    except Exception as e:
        results.add_fail("Empty courses handling", str(e))
    
    # Test 28: Invalid GPA scale
    try:
        try:
            GradeConverter.percentage_to_gpa(90, 3.0)
            results.add_fail("Invalid GPA scale", "Should raise ValueError")
        except ValueError:
            pass
        results.add_pass("Invalid GPA scale")
    except Exception as e:
        results.add_fail("Invalid GPA scale", str(e))
    
    # Test 29: Invalid percentage value
    try:
        try:
            GradeConverter.percentage_to_gpa(150, 4.0)
            results.add_fail("Invalid percentage value", "Should raise ValueError")
        except ValueError:
            pass
        results.add_pass("Invalid percentage value")
    except Exception as e:
        results.add_fail("Invalid percentage value", str(e))
    
    # Test 30: Default credits in convenience functions
    try:
        gpa = calculate_gpa([90, 80, 70])  # No credits, defaults to 1 each
        assert gpa > 0
        
        avg = calculate_weighted_average([90, 80, 70])
        assert avg == 80  # Equal weights
        results.add_pass("Default credits in convenience functions")
    except Exception as e:
        results.add_fail("Default credits in convenience functions", str(e))
    
    return results.report()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)