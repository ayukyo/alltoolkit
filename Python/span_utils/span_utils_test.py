"""
Span Utils 测试文件

测试区间操作工具的所有功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Span, BoundType,
    span, closed_span, open_span, point_span,
    empty_span, infinite_span, positive_span, negative_span, non_negative_span,
    merge_spans, intersection_of, subtract_span, subtract_spans,
    union_spans, span_difference, span_union_all, find_gaps, cover_spans,
    split_span, split_span_into_chunks, span_to_integers, normalize_spans,
    count_overlapping, max_overlap_count
)


def test_span_creation():
    """测试区间创建"""
    print("测试区间创建...")
    
    # 闭区间
    s1 = closed_span(1, 10)
    assert str(s1) == "[1, 10]"  # 整数输入会显示为整数
    assert s1.start == 1
    assert s1.end == 10
    
    # 开区间
    s2 = open_span(1, 10)
    assert str(s2) == "(1, 10)"
    
    # 单点区间
    s3 = point_span(5)
    assert str(s3) == "[5, 5]"
    assert s3.is_point()
    
    # 使用 span 函数
    s4 = span(0, 100)
    assert str(s4) == "[0, 100]"
    
    s5 = span(0, 100, closed=False)
    assert str(s5) == "(0, 100)"
    
    # 浮点数输入
    s6 = closed_span(1.5, 10.5)
    assert str(s6) == "[1.5, 10.5]"
    
    # 常用区间
    assert positive_span().start == 0
    assert non_negative_span().start == 0
    assert negative_span().end == 0
    
    print("✓ 区间创建测试通过")


def test_span_contains():
    """测试区间包含检查"""
    print("测试区间包含检查...")
    
    s = closed_span(1, 10)
    
    # 闭区间测试
    assert 1 in s
    assert 5 in s
    assert 10 in s
    assert 0 not in s
    assert 11 not in s
    
    # 开区间测试
    s_open = open_span(1, 10)
    assert 1 not in s_open
    assert 5 in s_open
    assert 10 not in s_open
    
    # 左闭右开
    s_right_open = Span(1, 10, BoundType.CLOSED, BoundType.OPEN)
    assert 1 in s_right_open
    assert 10 not in s_right_open
    
    print("✓ 区间包含检查测试通过")


def test_span_operations():
    """测试区间基本操作"""
    print("测试区间基本操作...")
    
    s = closed_span(1, 10)
    
    # 长度
    assert s.length() == 9
    
    # clamp
    assert s.clamp(0) == 1
    assert s.clamp(5) == 5
    assert s.clamp(15) == 10
    
    # expand
    s2 = s.expand(2)
    assert s2.start == -1
    assert s2.end == 12
    
    # shrink
    s3 = s.shrink(2)
    assert s3.start == 3
    assert s3.end == 8
    
    # shrink to invalid
    s4 = s.shrink(10)
    assert s4 is None
    
    print("✓ 区间基本操作测试通过")


def test_span_overlap():
    """测试区间重叠检查"""
    print("测试区间重叠检查...")
    
    # 重叠
    s1 = closed_span(1, 5)
    s2 = closed_span(3, 8)
    assert s1.overlaps(s2)
    assert s2.overlaps(s1)
    
    # 不重叠
    s3 = closed_span(1, 5)
    s4 = closed_span(6, 10)
    assert not s3.overlaps(s4)
    
    # 边界接触（闭区间）
    s5 = closed_span(1, 5)
    s6 = closed_span(5, 10)
    assert s5.overlaps(s6)  # [1,5] 和 [5,10] 在 5 点接触
    
    # 边界接触（开区间）
    s7 = open_span(1, 5)
    s8 = closed_span(5, 10)
    assert not s7.overlaps(s8)  # (1,5) 和 [5,10] 不接触
    
    print("✓ 区间重叠检查测试通过")


def test_span_intersection():
    """测试区间交集"""
    print("测试区间交集...")
    
    # 有交集
    s1 = closed_span(1, 10)
    s2 = closed_span(5, 15)
    inter = s1.intersection(s2)
    assert inter is not None
    assert inter.start == 5
    assert inter.end == 10
    
    # 无交集
    s3 = closed_span(1, 5)
    s4 = closed_span(6, 10)
    assert s3.intersection(s4) is None
    
    # 包含关系
    s5 = closed_span(1, 20)
    s6 = closed_span(5, 10)
    inter2 = s5.intersection(s6)
    assert inter2 == s6
    
    print("✓ 区间交集测试通过")


def test_merge_spans():
    """测试区间合并"""
    print("测试区间合并...")
    
    # 重叠合并
    spans = [closed_span(1, 5), closed_span(3, 8), closed_span(10, 15)]
    merged = merge_spans(spans)
    assert len(merged) == 2
    assert merged[0].start == 1
    assert merged[0].end == 8
    assert merged[1].start == 10
    assert merged[1].end == 15
    
    # 相邻合并
    spans2 = [closed_span(1, 5), closed_span(5, 10)]
    merged2 = merge_spans(spans2)
    assert len(merged2) == 1
    assert merged2[0].start == 1
    assert merged2[0].end == 10
    
    # 无重叠
    spans3 = [closed_span(1, 5), closed_span(10, 15), closed_span(20, 25)]
    merged3 = merge_spans(spans3)
    assert len(merged3) == 3
    
    # 空列表
    assert merge_spans([]) == []
    
    print("✓ 区间合并测试通过")


def test_subtract_span():
    """测试区间减法"""
    print("测试区间减法...")
    
    # 中间减去 - 返回带边界的区间
    s1 = closed_span(1, 20)
    s2 = closed_span(5, 10)
    result = subtract_span(s1, s2)
    assert len(result) == 2
    # 左边剩余: [1, 5) 因为 5 被减去了
    assert result[0].start == 1
    assert result[0].end == 5
    assert result[0].left_bound == BoundType.CLOSED
    assert result[0].right_bound == BoundType.OPEN
    # 右边剩余: (10, 20] 因为 10 被减去了
    assert result[1].start == 10
    assert result[1].end == 20
    assert result[1].left_bound == BoundType.OPEN
    assert result[1].right_bound == BoundType.CLOSED
    
    # 左边减去
    s3 = closed_span(1, 10)
    s4 = closed_span(1, 5)
    result2 = subtract_span(s3, s4)
    assert len(result2) == 1
    # 剩余: (5, 10]
    assert result2[0].start == 5
    assert result2[0].end == 10
    assert result2[0].left_bound == BoundType.OPEN
    assert result2[0].right_bound == BoundType.CLOSED
    
    # 右边减去
    s5 = closed_span(1, 10)
    s6 = closed_span(5, 10)
    result3 = subtract_span(s5, s6)
    assert len(result3) == 1
    # 剩余: [1, 5)
    assert result3[0].start == 1
    assert result3[0].end == 5
    assert result3[0].left_bound == BoundType.CLOSED
    assert result3[0].right_bound == BoundType.OPEN
    
    # 完全减去
    s7 = closed_span(1, 10)
    s8 = closed_span(0, 20)
    assert subtract_span(s7, s8) == []
    
    # 不重叠
    s9 = closed_span(1, 10)
    s10 = closed_span(20, 30)
    result4 = subtract_span(s9, s10)
    assert len(result4) == 1
    assert result4[0] == s9
    
    print("✓ 区间减法测试通过")


def test_subtract_spans():
    """测试多区间减法"""
    print("测试多区间减法...")
    
    s = closed_span(1, 100)
    subtractors = [closed_span(10, 20), closed_span(30, 40), closed_span(60, 70)]
    result = subtract_spans(s, subtractors)
    
    assert len(result) == 4
    # 检查结果的端点
    assert result[0].start == 1 and result[0].end == 10
    assert result[1].start == 20 and result[1].end == 30
    assert result[2].start == 40 and result[2].end == 60
    assert result[3].start == 70 and result[3].end == 100
    
    print("✓ 多区间减法测试通过")


def test_find_gaps():
    """测试间隙查找"""
    print("测试间隙查找...")
    
    spans = [closed_span(1, 5), closed_span(10, 15), closed_span(20, 25)]
    
    # 无范围限制
    gaps = find_gaps(spans)
    assert len(gaps) == 2
    assert gaps[0] == closed_span(5, 10)
    assert gaps[1] == closed_span(15, 20)
    
    # 有范围限制
    overall = closed_span(0, 30)
    gaps2 = find_gaps(spans, overall)
    assert len(gaps2) == 4
    assert gaps2[0] == closed_span(0, 1)
    assert gaps2[-1] == closed_span(25, 30)
    
    print("✓ 间隙查找测试通过")


def test_split_span():
    """测试区间分割"""
    print("测试区间分割...")
    
    s = closed_span(1, 10)
    
    # 在中间分割
    result = split_span(s, 5)
    assert len(result) == 2
    assert result[0] == closed_span(1, 5)
    assert result[1] == closed_span(5, 10)
    
    # 在边界分割
    result2 = split_span(s, 0)
    assert len(result2) == 1
    assert result2[0] == s
    
    result3 = split_span(s, 15)
    assert len(result3) == 1
    assert result3[0] == s
    
    print("✓ 区间分割测试通过")


def test_split_into_chunks():
    """测试等块分割"""
    print("测试等块分割...")
    
    s = closed_span(0, 100)
    chunks = split_span_into_chunks(s, 30)
    
    assert len(chunks) == 4
    assert chunks[0] == closed_span(0, 30)
    assert chunks[1] == closed_span(30, 60)
    assert chunks[2] == closed_span(60, 90)
    assert chunks[3] == closed_span(90, 100)
    
    print("✓ 等块分割测试通过")


def test_span_to_integers():
    """测试区间转整数"""
    print("测试区间转整数...")
    
    s = closed_span(2, 6)
    ints = span_to_integers(s)
    
    assert ints == [2, 3, 4, 5, 6]
    
    # 非整数边界
    s2 = closed_span(2.5, 6.5)
    ints2 = span_to_integers(s2)
    assert ints2 == [3, 4, 5, 6]
    
    print("✓ 区间转整数测试通过")


def test_count_overlapping():
    """测试重叠计数"""
    print("测试重叠计数...")
    
    spans = [closed_span(1, 10), closed_span(5, 15), closed_span(8, 20)]
    
    assert count_overlapping(spans, 2) == 1
    assert count_overlapping(spans, 6) == 2
    assert count_overlapping(spans, 9) == 3
    assert count_overlapping(spans, 17) == 1
    assert count_overlapping(spans, 25) == 0
    
    print("✓ 重叠计数测试通过")


def test_max_overlap():
    """测试最大重叠"""
    print("测试最大重叠...")
    
    spans = [closed_span(1, 10), closed_span(5, 15), closed_span(8, 20)]
    count, region = max_overlap_count(spans)
    
    assert count == 3
    assert region is not None
    
    # 无重叠的情况
    spans2 = [closed_span(1, 5), closed_span(10, 15), closed_span(20, 25)]
    count2, region2 = max_overlap_count(spans2)
    assert count2 == 1
    
    print("✓ 最大重叠测试通过")


def test_intersection_of():
    """测试多区间交集"""
    print("测试多区间交集...")
    
    spans = [closed_span(1, 20), closed_span(5, 15), closed_span(8, 12)]
    result = intersection_of(spans)
    
    assert result is not None
    assert result.start == 8
    assert result.end == 12
    
    # 无交集
    spans2 = [closed_span(1, 5), closed_span(10, 15)]
    assert intersection_of(spans2) is None
    
    # 空列表
    assert intersection_of([]) is None
    
    print("✓ 多区间交集测试通过")


def test_cover_spans():
    """测试区间覆盖"""
    print("测试区间覆盖...")
    
    spans = [closed_span(5, 10), closed_span(1, 3), closed_span(15, 20)]
    result = cover_spans(spans)
    
    assert result.start == 1
    assert result.end == 20
    
    # 空列表
    assert cover_spans([]) is None
    
    print("✓ 区间覆盖测试通过")


def test_span_difference():
    """测试区间差集"""
    print("测试区间差集...")
    
    set1 = [closed_span(1, 20)]
    set2 = [closed_span(5, 10), closed_span(15, 18)]
    result = span_difference(set1, set2)
    
    assert len(result) == 3
    # 检查端点
    assert result[0].start == 1 and result[0].end == 5
    assert result[1].start == 10 and result[1].end == 15
    assert result[2].start == 18 and result[2].end == 20
    
    print("✓ 区间差集测试通过")


def test_span_equality():
    """测试区间相等性"""
    print("测试区间相等性...")
    
    s1 = closed_span(1, 10)
    s2 = closed_span(1, 10)
    s3 = open_span(1, 10)
    s4 = closed_span(2, 10)
    
    assert s1 == s2
    assert s1 != s3
    assert s1 != s4
    
    # 哈希
    spans_set = {s1, s2, s3}
    assert len(spans_set) == 2
    
    print("✓ 区间相等性测试通过")


def test_empty_span():
    """测试空区间"""
    print("测试空区间...")
    
    e = empty_span()
    assert e.is_empty()
    assert e.length() == 0
    
    # 单点区间不是空区间
    p = point_span(5)
    assert not p.is_empty()
    
    # 开区间起点等于终点是空区间
    e2 = open_span(5, 5)
    assert e2.is_empty()
    
    print("✓ 空区间测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Span Utils 测试套件")
    print("=" * 50)
    
    test_span_creation()
    test_span_contains()
    test_span_operations()
    test_span_overlap()
    test_span_intersection()
    test_merge_spans()
    test_subtract_span()
    test_subtract_spans()
    test_find_gaps()
    test_split_span()
    test_split_into_chunks()
    test_span_to_integers()
    test_count_overlapping()
    test_max_overlap()
    test_intersection_of()
    test_cover_spans()
    test_span_difference()
    test_span_equality()
    test_empty_span()
    
    print("=" * 50)
    print("所有测试通过! ✓")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()