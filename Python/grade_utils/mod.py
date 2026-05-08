"""
Grade Utilities - 成绩计算工具

提供完整的成绩处理功能，包括：
- GPA 计算 (4.0制、5.0制、多种标准)
- 加权平均分计算
- 成绩等级转换 (A-F、优良好中差、百分制互转)
- 学分绩点计算
- 成绩分布统计
- 多学期成绩追踪
- 成绩趋势分析
- 成绩排名计算

零外部依赖，纯 Python 实现。
"""

from typing import List, Dict, Tuple, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from statistics import mean, stdev
from datetime import date
import math


class GradeSystem(Enum):
    """成绩制度类型"""
    PERCENTAGE = "percentage"  # 百分制 (0-100)
    GPA_4_0 = "gpa_4_0"         # 4.0 制 GPA
    GPA_5_0 = "gpa_5_0"         # 5.0 制 GPA
    LETTER = "letter"           # 字母等级 (A-F)
    CHINESE = "chinese"         # 中文等级 (优良好中差)


@dataclass
class Course:
    """课程成绩"""
    name: str                    # 课程名称
    score: float                 # 成绩分数
    credit: float = 1.0          # 学分
    semester: str = ""           # 学期标识 (如 "2023-2024-1")
    course_type: str = "required"  # 课程类型 (required/elective)
    
    def __post_init__(self):
        """验证数据"""
        if self.score < 0:
            raise ValueError(f"成绩不能为负数: {self.score}")
        if self.credit < 0:
            raise ValueError(f"学分不能为负数: {self.credit}")


@dataclass
class GradeRecord:
    """成绩记录（可追踪多学期）"""
    student_id: str = ""
    student_name: str = ""
    courses: List[Course] = field(default_factory=list)
    
    def add_course(self, course: Course):
        """添加课程"""
        self.courses.append(course)
    
    def get_courses_by_semester(self, semester: str) -> List[Course]:
        """按学期获取课程"""
        return [c for c in self.courses if c.semester == semester]
    
    def get_semesters(self) -> List[str]:
        """获取所有学期"""
        return sorted(set(c.semester for c in self.courses if c.semester))


class GradeConverter:
    """成绩转换器"""
    
    # 百分制转 GPA 4.0 标准
    PERCENTAGE_TO_GPA_4 = {
        (90, 100): 4.0,
        (85, 89): 3.7,
        (82, 84): 3.3,
        (78, 81): 3.0,
        (75, 77): 2.7,
        (72, 74): 2.3,
        (68, 71): 2.0,
        (64, 67): 1.5,
        (60, 63): 1.0,
        (0, 59): 0.0
    }
    
    # 百分制转 GPA 5.0 标准
    PERCENTAGE_TO_GPA_5 = {
        (95, 100): 5.0,
        (90, 94): 4.5,
        (85, 89): 4.0,
        (80, 84): 3.5,
        (75, 79): 3.0,
        (70, 74): 2.5,
        (65, 69): 2.0,
        (60, 64): 1.5,
        (0, 59): 0.0
    }
    
    # 百分制转字母等级
    PERCENTAGE_TO_LETTER = {
        (90, 100): 'A',
        (80, 89): 'B',
        (70, 79): 'C',
        (60, 69): 'D',
        (0, 59): 'F'
    }
    
    # 百分制转中文等级
    PERCENTAGE_TO_CHINESE = {
        (90, 100): '优秀',
        (80, 89): '良好',
        (70, 79): '中等',
        (60, 69): '及格',
        (0, 59): '不及格'
    }
    
    # 字母等级转 GPA 4.0
    LETTER_TO_GPA_4 = {
        'A+': 4.0, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'D-': 0.7,
        'F': 0.0
    }
    
    @classmethod
    def _find_in_range(cls, value: float, mapping: Dict) -> Optional[float]:
        """在区间映射中查找值"""
        for (low, high), result in mapping.items():
            if low <= value <= high:
                return result
        return None
    
    @classmethod
    def percentage_to_gpa(cls, score: float, gpa_scale: float = 4.0) -> float:
        """
        百分制转 GPA
        
        Args:
            score: 百分制成绩 (0-100)
            gpa_scale: GPA 制度 (4.0 或 5.0)
        
        Returns:
            GPA 值
        """
        if score < 0 or score > 100:
            raise ValueError(f"百分制成绩应在 0-100 之间: {score}")
        
        if gpa_scale == 4.0:
            result = cls._find_in_range(score, cls.PERCENTAGE_TO_GPA_4)
        elif gpa_scale == 5.0:
            result = cls._find_in_range(score, cls.PERCENTAGE_TO_GPA_5)
        else:
            raise ValueError(f"不支持的 GPA 制度: {gpa_scale}")
        
        return result if result is not None else 0.0
    
    @classmethod
    def percentage_to_letter(cls, score: float) -> str:
        """百分制转字母等级"""
        if score < 0 or score > 100:
            raise ValueError(f"百分制成绩应在 0-100 之间: {score}")
        result = cls._find_in_range(score, cls.PERCENTAGE_TO_LETTER)
        return result if result else 'F'
    
    @classmethod
    def percentage_to_chinese(cls, score: float) -> str:
        """百分制转中文等级"""
        if score < 0 or score > 100:
            raise ValueError(f"百分制成绩应在 0-100 之间: {score}")
        result = cls._find_in_range(score, cls.PERCENTAGE_TO_CHINESE)
        return result if result else '不及格'
    
    @classmethod
    def letter_to_gpa(cls, letter: str) -> float:
        """字母等级转 GPA 4.0"""
        return cls.LETTER_TO_GPA_4.get(letter.upper(), 0.0)
    
    @classmethod
    def gpa_to_percentage(cls, gpa: float, gpa_scale: float = 4.0) -> float:
        """
        GPA 转百分制（近似值）
        
        Args:
            gpa: GPA 值
            gpa_scale: GPA 制度 (4.0 或 5.0)
        
        Returns:
            近似百分制成绩
        """
        if gpa_scale == 4.0:
            if gpa >= 4.0:
                return 95.0
            elif gpa >= 3.7:
                return 87.0 + (gpa - 3.7) * 8 / 0.3
            elif gpa >= 3.3:
                return 83.0 + (gpa - 3.3) * 4 / 0.4
            elif gpa >= 3.0:
                return 79.0 + (gpa - 3.0) * 4 / 0.3
            elif gpa >= 2.7:
                return 73.5 + (gpa - 2.7) * 5.5 / 0.3
            elif gpa >= 2.3:
                return 70.0 + (gpa - 2.3) * 3.5 / 0.4
            elif gpa >= 2.0:
                return 67.0 + (gpa - 2.0) * 3 / 0.3
            elif gpa >= 1.5:
                return 62.0 + (gpa - 1.5) * 5 / 0.5
            elif gpa >= 1.0:
                return 60.0 + (gpa - 1.0) * 2 / 0.5
            else:
                return gpa * 60
        elif gpa_scale == 5.0:
            return min(100, max(0, gpa * 20))
        else:
            raise ValueError(f"不支持的 GPA 制度: {gpa_scale}")


class GPACalculator:
    """GPA 计算器"""
    
    @staticmethod
    def calculate_weighted_gpa(
        courses: List[Course],
        gpa_scale: float = 4.0,
        include_failed: bool = True
    ) -> float:
        """
        计算加权 GPA
        
        Args:
            courses: 课程列表
            gpa_scale: GPA 制度 (4.0 或 5.0)
            include_failed: 是否包含不及格课程
        
        Returns:
            加权 GPA
        """
        total_points = 0.0
        total_credits = 0.0
        
        for course in courses:
            # 检查是否为百分制
            if 0 <= course.score <= 100:
                gpa = GradeConverter.percentage_to_gpa(course.score, gpa_scale)
                if not include_failed and course.score < 60:
                    continue
            else:
                # 假设已经是 GPA
                gpa = course.score
            
            total_points += gpa * course.credit
            total_credits += course.credit
        
        if total_credits == 0:
            return 0.0
        
        return round(total_points / total_credits, 3)
    
    @staticmethod
    def calculate_weighted_average(courses: List[Course]) -> float:
        """
        计算加权平均分
        
        Args:
            courses: 课程列表
        
        Returns:
            加权平均分
        """
        total_score = 0.0
        total_credits = 0.0
        
        for course in courses:
            total_score += course.score * course.credit
            total_credits += course.credit
        
        if total_credits == 0:
            return 0.0
        
        return round(total_score / total_credits, 2)
    
    @staticmethod
    def calculate_credit_points(
        courses: List[Course],
        gpa_scale: float = 4.0
    ) -> Dict[str, float]:
        """
        计算学分绩点
        
        Returns:
            包含总学分、总绩点、平均绩点的字典
        """
        total_credits = sum(c.credit for c in courses)
        total_points = sum(
            GradeConverter.percentage_to_gpa(c.score, gpa_scale) * c.credit
            for c in courses
        )
        
        return {
            "total_credits": total_credits,
            "total_points": round(total_points, 2),
            "average_gpa": round(total_points / total_credits, 3) if total_credits > 0 else 0.0
        }


class GradeAnalyzer:
    """成绩分析器"""
    
    @staticmethod
    def get_distribution(courses: List[Course]) -> Dict[str, int]:
        """
        获取成绩分布
        
        Returns:
            各等级的人数分布
        """
        distribution = {
            '优秀': 0,
            '良好': 0,
            '中等': 0,
            '及格': 0,
            '不及格': 0
        }
        
        for course in courses:
            level = GradeConverter.percentage_to_chinese(course.score)
            distribution[level] += 1
        
        return distribution
    
    @staticmethod
    def get_statistics(courses: List[Course]) -> Dict[str, float]:
        """
        获取成绩统计信息
        
        Returns:
            最高分、最低分、平均分、标准差等
        """
        if not courses:
            return {
                "max": 0,
                "min": 0,
                "mean": 0,
                "median": 0,
                "std": 0,
                "count": 0
            }
        
        scores = [c.score for c in courses]
        sorted_scores = sorted(scores)
        n = len(sorted_scores)
        
        # 计算中位数
        if n % 2 == 0:
            median = (sorted_scores[n//2 - 1] + sorted_scores[n//2]) / 2
        else:
            median = sorted_scores[n//2]
        
        return {
            "max": max(scores),
            "min": min(scores),
            "mean": round(mean(scores), 2),
            "median": round(median, 2),
            "std": round(stdev(scores), 2) if len(scores) > 1 else 0,
            "count": len(scores)
        }
    
    @staticmethod
    def get_rank(
        target: Course,
        all_courses: List[Course]
    ) -> Dict[str, Union[int, float]]:
        """
        计算排名信息
        
        Args:
            target: 目标课程
            all_courses: 所有课程（包括目标课程）
        
        Returns:
            排名信息字典
        """
        sorted_courses = sorted(
            all_courses, 
            key=lambda c: c.score, 
            reverse=True
        )
        
        rank = sorted_courses.index(target) + 1
        total = len(sorted_courses)
        percentile = round((total - rank + 1) / total * 100, 1)
        
        return {
            "rank": rank,
            "total": total,
            "percentile": percentile
        }
    
    @staticmethod
    def analyze_trend(
        semesters_data: Dict[str, List[Course]],
        gpa_scale: float = 4.0
    ) -> Dict[str, Union[float, str, List]]:
        """
        分析成绩趋势
        
        Args:
            semesters_data: 按学期分组的课程数据
            gpa_scale: GPA 制度
        
        Returns:
            趋势分析结果
        """
        sorted_semesters = sorted(semesters_data.keys())
        
        gpas = []
        for semester in sorted_semesters:
            courses = semesters_data[semester]
            if courses:
                gpa = GPACalculator.calculate_weighted_gpa(courses, gpa_scale)
                gpas.append({"semester": semester, "gpa": gpa})
        
        if len(gpas) < 2:
            return {
                "trend": "数据不足",
                "change": 0,
                "history": gpas
            }
        
        # 计算趋势
        changes = []
        for i in range(1, len(gpas)):
            changes.append(gpas[i]["gpa"] - gpas[i-1]["gpa"])
        
        avg_change = mean(changes)
        
        if avg_change > 0.1:
            trend = "上升"
        elif avg_change < -0.1:
            trend = "下降"
        else:
            trend = "稳定"
        
        return {
            "trend": trend,
            "avg_change": round(avg_change, 3),
            "latest_gpa": gpas[-1]["gpa"],
            "best_gpa": max(g["gpa"] for g in gpas),
            "worst_gpa": min(g["gpa"] for g in gpas),
            "history": gpas
        }
    
    @staticmethod
    def compare_by_type(
        courses: List[Course]
    ) -> Dict[str, Dict[str, float]]:
        """
        按课程类型比较成绩
        
        Returns:
            按课程类型分组的统计信息
        """
        by_type: Dict[str, List[Course]] = {}
        
        for course in courses:
            course_type = course.course_type
            if course_type not in by_type:
                by_type[course_type] = []
            by_type[course_type].append(course)
        
        result = {}
        for course_type, type_courses in by_type.items():
            result[course_type] = GradeAnalyzer.get_statistics(type_courses)
            result[course_type]["gpa"] = GPACalculator.calculate_weighted_gpa(type_courses)
        
        return result


class GradePredictor:
    """成绩预测器（简单线性回归）"""
    
    @staticmethod
    def predict_final(
        current_score: float,
        target_score: float,
        final_weight: float = 0.3
    ) -> Dict[str, float]:
        """
        预测期末需要多少分才能达到目标
        
        Args:
            current_score: 当前成绩
            target_score: 目标总成绩
            final_weight: 期末考试占比
        
        Returns:
            预测结果
        """
        # 目标 = 当前 * (1 - 期末占比) + 期末 * 期末占比
        # 期末 = (目标 - 当前 * (1 - 期末占比)) / 期末占比
        
        current_weight = 1 - final_weight
        needed_final = (target_score - current_score * current_weight) / final_weight
        
        return {
            "current_score": current_score,
            "target_score": target_score,
            "needed_final": round(needed_final, 2),
            "possible": 0 <= needed_final <= 100,
            "current_weight": current_weight,
            "final_weight": final_weight
        }
    
    @staticmethod
    def predict_gpa(
        current_gpa: float,
        remaining_credits: float,
        target_gpa: float,
        total_credits: float
    ) -> Dict[str, float]:
        """
        预测剩余课程需要达到的 GPA
        
        Args:
            current_gpa: 当前 GPA
            remaining_credits: 剩余学分
            target_gpa: 目标 GPA
            total_credits: 总学分
        
        Returns:
            预测结果
        """
        completed_credits = total_credits - remaining_credits
        
        if completed_credits <= 0:
            return {
                "needed_gpa": target_gpa,
                "possible": True
            }
        
        # 总绩点 = 当前GPA * 已修学分 + 剩余GPA * 剩余学分
        # 剩余GPA = (目标GPA * 总学分 - 当前GPA * 已修学分) / 剩余学分
        
        current_points = current_gpa * completed_credits
        target_points = target_gpa * total_credits
        needed_points = target_points - current_points
        needed_gpa = needed_points / remaining_credits
        
        return {
            "current_gpa": current_gpa,
            "target_gpa": target_gpa,
            "needed_gpa": round(needed_gpa, 3),
            "possible": 0 <= needed_gpa <= 4.0,
            "completed_credits": completed_credits,
            "remaining_credits": remaining_credits
        }


class TranscriptFormatter:
    """成绩单格式化器"""
    
    @staticmethod
    def format_summary(
        record: GradeRecord,
        gpa_scale: float = 4.0
    ) -> str:
        """格式化成绩单摘要"""
        stats = GradeAnalyzer.get_statistics(record.courses)
        gpa = GPACalculator.calculate_weighted_gpa(record.courses, gpa_scale)
        dist = GradeAnalyzer.get_distribution(record.courses)
        credits = GPACalculator.calculate_credit_points(record.courses, gpa_scale)
        
        lines = [
            "=" * 50,
            f"成绩单摘要",
            "=" * 50,
        ]
        
        if record.student_name:
            lines.append(f"学生姓名: {record.student_name}")
        if record.student_id:
            lines.append(f"学号: {record.student_id}")
        
        lines.extend([
            "-" * 50,
            f"课程总数: {stats['count']}",
            f"总学分: {credits['total_credits']}",
            f"平均分: {stats['mean']}",
            f"GPA: {gpa}",
            "-" * 50,
            "成绩分布:",
            f"  优秀: {dist['优秀']} 门",
            f"  良好: {dist['良好']} 门",
            f"  中等: {dist['中等']} 门",
            f"  及格: {dist['及格']} 门",
            f"  不及格: {dist['不及格']} 门",
            "-" * 50,
            f"最高分: {stats['max']}",
            f"最低分: {stats['min']}",
            f"标准差: {stats['std']}",
            "=" * 50
        ])
        
        return "\n".join(lines)
    
    @staticmethod
    def format_course_list(
        courses: List[Course],
        gpa_scale: float = 4.0
    ) -> str:
        """格式化课程列表"""
        lines = [
            f"{'课程名称':<20} {'成绩':>6} {'学分':>6} {'绩点':>6} {'等级':>6}",
            "-" * 50
        ]
        
        for course in sorted(courses, key=lambda c: c.name):
            gpa = GradeConverter.percentage_to_gpa(course.score, gpa_scale)
            level = GradeConverter.percentage_to_chinese(course.score)
            lines.append(
                f"{course.name:<20} {course.score:>6.1f} {course.credit:>6.1f} "
                f"{gpa:>6.2f} {level:>6}"
            )
        
        return "\n".join(lines)


# 便捷函数
def calculate_gpa(
    scores: List[float],
    credits: Optional[List[float]] = None,
    gpa_scale: float = 4.0
) -> float:
    """
    快速计算 GPA
    
    Args:
        scores: 成绩列表
        credits: 学分列表（可选，默认均为1）
        gpa_scale: GPA 制度 (4.0 或 5.0)
    
    Returns:
        GPA 值
    """
    if credits is None:
        credits = [1.0] * len(scores)
    
    courses = [
        Course(name=f"课程{i+1}", score=s, credit=c)
        for i, (s, c) in enumerate(zip(scores, credits))
    ]
    
    return GPACalculator.calculate_weighted_gpa(courses, gpa_scale)


def calculate_weighted_average(
    scores: List[float],
    credits: Optional[List[float]] = None
) -> float:
    """
    快速计算加权平均分
    
    Args:
        scores: 成绩列表
        credits: 学分列表（可选，默认均为1）
    
    Returns:
        加权平均分
    """
    if credits is None:
        credits = [1.0] * len(scores)
    
    courses = [
        Course(name=f"课程{i+1}", score=s, credit=c)
        for i, (s, c) in enumerate(zip(scores, credits))
    ]
    
    return GPACalculator.calculate_weighted_average(courses)


def get_grade_level(score: float) -> str:
    """快速获取成绩等级"""
    return GradeConverter.percentage_to_chinese(score)


def get_letter_grade(score: float) -> str:
    """快速获取字母等级"""
    return GradeConverter.percentage_to_letter(score)


# 导出
__all__ = [
    'GradeSystem',
    'Course',
    'GradeRecord',
    'GradeConverter',
    'GPACalculator',
    'GradeAnalyzer',
    'GradePredictor',
    'TranscriptFormatter',
    'calculate_gpa',
    'calculate_weighted_average',
    'get_grade_level',
    'get_letter_grade',
]