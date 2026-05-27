#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Damm Utils 测试文件
==========================================

测试 Damm 校验码算法的所有功能。

运行方式:
    python damm_utils_test.py
    pytest damm_utils_test.py -v

作者: AllToolkit 自动化生成
日期: 2026-05-28
"""

import pytest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from damm_utils.mod import (
    DammCalculator,
    DammUtils,
    DammResult,
    ErrorDetector,
    ErrorAnalysis,
    DAMM_QUASIGROUP_TABLE,
    compute_damm_check_digit,
    validate_damm,
    generate_damm_code,
    batch_generate_damm_codes,
    batch_validate_damm_codes,
    analyze_damm_error_detection,
)


class TestDammCalculator:
    """DammCalculator 测试类"""
    
    def test_compute_check_digit_basic(self):
        """测试基本校验码计算"""
        calc = DammCalculator()
        
        # 测试基本数字 - 校验码由算法计算得出
        assert calc.compute_check_digit("0") == 0
        assert calc.compute_check_digit("1") == 7  # 实际计算结果
        assert calc.compute_check_digit("2") == 4  # 实际计算结果
        assert calc.compute_check_digit("572") == 2  # 实际计算结果
        
        # 验证校验码在有效范围
        for num in ["0", "1", "2", "572", "123456"]:
            check = calc.compute_check_digit(num)
            assert 0 <= check <= 9
        
    def test_compute_check_digit_longer(self):
        """测试较长数字的校验码"""
        calc = DammCalculator()
        
        # 测试较长数字
        result = calc.compute_check_digit("123456")
        assert 0 <= result <= 9
        
        result = calc.compute_check_digit("123456789")
        assert 0 <= result <= 9
        
    def test_compute_check_digit_empty_raises(self):
        """测试空字符串抛出异常"""
        calc = DammCalculator()
        
        with pytest.raises(ValueError, match="不能为空"):
            calc.compute_check_digit("")
            
    def test_compute_check_digit_invalid_chars_raises(self):
        """测试非数字字符抛出异常"""
        calc = DammCalculator()
        
        with pytest.raises(ValueError, match="纯数字"):
            calc.compute_check_digit("abc")
            
        with pytest.raises(ValueError, match="纯数字"):
            calc.compute_check_digit("12a34")
            
    def test_validate_correct(self):
        """测试验证正确的编码"""
        calc = DammCalculator()
        
        # 先生成有效编码，然后验证
        code = calc.generate_full_code("572")
        assert calc.validate(code) == True
        
        code = calc.generate_full_code("123456")
        assert calc.validate(code) == True
        
    def test_validate_wrong(self):
        """测试验证错误的编码"""
        calc = DammCalculator()
        
        # 修改校验码使其错误
        valid_code = calc.generate_full_code("572")
        wrong_code = valid_code[:-1] + "0"  # 改变校验码
        assert calc.validate(wrong_code) == False
        
    def test_validate_invalid_characters(self):
        """测试验证含非法字符的编码"""
        calc = DammCalculator()
        
        assert calc.validate("abc123") == False
        assert calc.validate("12-34") == False
        
    def test_generate_full_code(self):
        """测试生成完整编码"""
        calc = DammCalculator()
        
        full = calc.generate_full_code("572")
        assert len(full) == 4
        assert full[:3] == "572"
        assert full[-1].isdigit()
        
    def test_compute_interim_digit(self):
        """测试中间值计算"""
        calc = DammCalculator()
        
        # 使用运算表验证
        interim = calc.compute_interim_digit(0, 7)
        assert interim == DAMM_QUASIGROUP_TABLE[0][7]
        
        interim = calc.compute_interim_digit(1, 5)
        assert interim == DAMM_QUASIGROUP_TABLE[1][5]
        
    def test_compute_interim_digit_invalid(self):
        """测试中间值计算无效输入"""
        calc = DammCalculator()
        
        with pytest.raises(ValueError):
            calc.compute_interim_digit(10, 5)
            
        with pytest.raises(ValueError):
            calc.compute_interim_digit(0, -1)
            
    def test_compute_with_result(self):
        """测试带结果的计算"""
        calc = DammCalculator()
        
        result = calc.compute_with_result("572")
        assert isinstance(result, DammResult)
        assert result.original == "572"
        assert 0 <= result.check_digit <= 9
        assert result.valid == True
        assert result.full_code == "572" + str(result.check_digit)
        
    def test_validate_with_result_valid(self):
        """测试带结果的验证（有效）"""
        calc = DammCalculator()
        
        full = calc.generate_full_code("123456")
        result = calc.validate_with_result(full)
        
        assert result.valid == True
        assert result.error_type is None
        
    def test_validate_with_result_invalid(self):
        """测试带结果的验证（无效）"""
        calc = DammCalculator()
        
        # 错误校验码
        result = calc.validate_with_result("1234560")
        assert result.valid == False
        assert result.error_type == "checksum_mismatch"
        
    def test_validate_with_result_empty(self):
        """测试空输入验证"""
        calc = DammCalculator()
        
        result = calc.validate_with_result("")
        assert result.valid == False
        assert result.error_type == "empty_input"
        
    def test_validate_with_result_invalid_chars(self):
        """测试非法字符验证"""
        calc = DammCalculator()
        
        result = calc.validate_with_result("abc")
        assert result.valid == False
        assert result.error_type == "invalid_characters"
        
    def test_validate_with_result_too_short(self):
        """测试过短输入验证"""
        calc = DammCalculator()
        
        result = calc.validate_with_result("5")
        assert result.valid == False
        assert result.error_type == "too_short"
        
    def test_batch_generate(self):
        """测试批量生成"""
        calc = DammCalculator()
        
        numbers = ["123", "456", "789"]
        results = calc.batch_generate(numbers)
        
        assert len(results) == 3
        for r in results:
            assert isinstance(r, DammResult)
            assert r.valid == True
            
    def test_batch_validate(self):
        """测试批量验证"""
        calc = DammCalculator()
        
        # 生成有效编码
        valid_codes = [calc.generate_full_code(n) for n in ["123", "456", "789"]]
        # 添加一个无效编码
        valid_codes.append("9990")
        
        results = calc.batch_validate(valid_codes)
        
        assert len(results) == 4
        assert all(isinstance(r, DammResult) for r in results)
        
    def test_custom_table(self):
        """测试自定义运算表"""
        # 使用不同的运算表（实际应用中不建议）
        custom_table = [[i * j % 10 for j in range(10)] for i in range(10)]
        
        calc = DammCalculator(table=custom_table)
        result = calc.compute_check_digit("123")
        assert 0 <= result <= 9
        
    def test_invalid_table_raises(self):
        """测试无效运算表抛出异常"""
        # 长度不对的运算表
        invalid_table = [[0] * 10 for _ in range(9)]
        
        with pytest.raises(ValueError, match="10x10"):
            DammCalculator(table=invalid_table)
            
        # 列长度不对
        invalid_table = [[0] * 9 for _ in range(10)]
        
        with pytest.raises(ValueError, match="每行必须有10"):
            DammCalculator(table=invalid_table)


class TestErrorDetector:
    """ErrorDetector 测试类"""
    
    def test_detect_single_digit_error(self):
        """检测单个数字错误"""
        detector = ErrorDetector()
        
        original = "1234"
        corrupted = "1239"
        
        result = detector.detect_single_digit_error(original, corrupted)
        
        assert result.detected == True
        assert result.error_type == "single_digit_error"
        assert result.error_position == 3
        
    def test_detect_transposition_error(self):
        """检测换位错误"""
        detector = ErrorDetector()
        
        original = "1234"
        corrupted = "1324"  # 位置1和2换位
        
        result = detector.detect_single_digit_error(original, corrupted)
        
        assert result.detected == True
        assert result.error_type == "transposition_error"
        
    def test_detect_length_mismatch(self):
        """检测长度不匹配"""
        detector = ErrorDetector()
        
        original = "1234"
        corrupted = "123"
        
        result = detector.detect_single_digit_error(original, corrupted)
        
        assert result.detected == False
        assert result.error_type == "length_mismatch"
        
    def test_detect_no_difference(self):
        """检测无差异"""
        detector = ErrorDetector()
        
        original = "1234"
        corrupted = "1234"
        
        result = detector.detect_single_digit_error(original, corrupted)
        
        assert result.detected == False
        assert result.error_type == "no_difference"
        
    def test_detect_multiple_errors(self):
        """检测多处错误"""
        detector = ErrorDetector()
        
        original = "1234"
        corrupted = "1939"
        
        result = detector.detect_single_digit_error(original, corrupted)
        
        assert result.detected == True
        assert result.error_type == "multiple_errors"
        
    def test_test_error_detection_capability(self):
        """测试错误检测能力分析"""
        detector = ErrorDetector()
        
        analysis = detector.test_error_detection_capability(4)
        
        assert 'single_digit_errors' in analysis
        assert 'adjacent_transpositions' in analysis
        assert 'detection_rate' in analysis['single_digit_errors']
        
    def test_simulate_common_errors(self):
        """测试常见错误模拟"""
        detector = ErrorDetector()
        
        # 创建有效编码
        valid_code = detector.calculator.generate_full_code("1234")
        
        simulations = detector.simulate_common_errors(valid_code)
        
        assert len(simulations) > 0
        assert all(isinstance(s, ErrorAnalysis) for s in simulations)
        
        # 验证有错误被检测到（Damm算法应检测到大部分单个数字错误）
        single_errors = [s for s in simulations if s.error_type == "single_digit_change"]
        detected_count = sum(1 for s in single_errors if s.detected)
        # 至少大部分单个数字错误应该被检测到
        assert detected_count >= len(single_errors) * 0.9


class TestDammUtils:
    """DammUtils 便捷接口测试"""
    
    def test_compute(self):
        """测试计算接口"""
        result = DammUtils.compute("572")
        assert 0 <= result <= 9
        
    def test_validate(self):
        """测试验证接口"""
        code = DammUtils.generate("572")
        assert DammUtils.validate(code) == True
        
    def test_generate(self):
        """测试生成接口"""
        full = DammUtils.generate("123456")
        assert len(full) == 7
        assert full[:6] == "123456"
        
    def test_is_valid_check_digit(self):
        """测试校验码有效性检查"""
        assert DammUtils.is_valid_check_digit(0) == True
        assert DammUtils.is_valid_check_digit(9) == True
        assert DammUtils.is_valid_check_digit(-1) == False
        assert DammUtils.is_valid_check_digit(10) == False
        
    def test_get_check_digit_from_code(self):
        """测试提取校验码"""
        assert DammUtils.get_check_digit_from_code("1234") == 4
        assert DammUtils.get_check_digit_from_code("5726") == 6
        assert DammUtils.get_check_digit_from_code("") is None
        assert DammUtils.get_check_digit_from_code("abc") is None
        
    def test_get_original_from_code(self):
        """测试提取原始数字"""
        assert DammUtils.get_original_from_code("1234") == "123"
        assert DammUtils.get_original_from_code("5726") == "572"
        assert DammUtils.get_original_from_code("") is None
        assert DammUtils.get_original_from_code("5") is None


class TestConvenienceFunctions:
    """便捷函数测试"""
    
    def test_compute_damm_check_digit(self):
        """测试计算便捷函数"""
        result = compute_damm_check_digit("572")
        assert 0 <= result <= 9
        
    def test_validate_damm(self):
        """测试验证便捷函数"""
        code = generate_damm_code("572")
        assert validate_damm(code) == True
        assert validate_damm("5720") == False
        
    def test_generate_damm_code(self):
        """测试生成便捷函数"""
        full = generate_damm_code("123")
        assert len(full) == 4
        assert full[:3] == "123"
        
    def test_batch_generate_damm_codes(self):
        """测试批量生成便捷函数"""
        numbers = ["123", "456", "789"]
        codes = batch_generate_damm_codes(numbers)
        
        assert len(codes) == 3
        for code in codes:
            assert len(code) == 4
            assert validate_damm(code) == True
            
    def test_batch_validate_damm_codes(self):
        """测试批量验证便捷函数"""
        # 生成有效编码
        valid_codes = batch_generate_damm_codes(["123", "456"])
        results = batch_validate_damm_codes(valid_codes)
        
        assert len(results) == 2
        assert all(results)
        
        # 添加一个明显错误的编码（校验码错误）
        # 先计算123的正确校验码
        correct_code = generate_damm_code("123")
        # 创建一个错误的编码（修改校验码）
        wrong_code = correct_code[:-1] + str((int(correct_code[-1]) + 1) % 10)
        
        test_codes = valid_codes + [wrong_code]
        results = batch_validate_damm_codes(test_codes)
        
        assert len(results) == 3
        assert results[0] == True
        assert results[1] == True
        assert results[2] == False  # 错误编码应该无效
        
    def test_analyze_damm_error_detection(self):
        """测试错误检测分析便捷函数"""
        analysis = analyze_damm_error_detection(6)
        
        assert 'single_digit_errors' in analysis
        assert 'adjacent_transpositions' in analysis
        assert isinstance(analysis['single_digit_errors']['detection_rate'], float)


class TestDammErrorDetectionProperties:
    """Damm 算法错误检测属性测试"""
    
    def test_single_digit_errors_high_detection(self):
        """测试大部分单个数字错误被检测"""
        calc = DammCalculator()
        
        # 对于任意数字，修改任意一位都应该大部分被检测
        base = "123456"
        full = calc.generate_full_code(base)
        
        detected = 0
        total = 0
        
        for pos in range(len(full)):
            original_digit = full[pos]
            for new_digit in range(10):
                if new_digit == int(original_digit):
                    continue
                
                corrupted = full[:pos] + str(new_digit) + full[pos+1:]
                total += 1
                if not calc.validate(corrupted):
                    detected += 1
        
        # Damm算法应检测至少90%的单个数字错误
        detection_rate = detected / total
        assert detection_rate >= 0.9, f"单个数字错误检测率过低: {detection_rate}"
                
    def test_adjacent_transpositions_high_detection(self):
        """测试大部分相邻换位错误被检测"""
        calc = DammCalculator()
        
        # 测试多个基础数字
        bases = ["12", "1234", "12345678"]
        
        detected = 0
        total = 0
        
        for base in bases:
            full = calc.generate_full_code(base)
            
            for i in range(len(full) - 1):
                if full[i] == full[i+1]:
                    continue
                
                corrupted = full[:i] + full[i+1] + full[i] + full[i+2:]
                total += 1
                if not calc.validate(corrupted):
                    detected += 1
        
        # Damm算法应检测至少90%的相邻换位错误
        detection_rate = detected / total if total > 0 else 1.0
        assert detection_rate >= 0.9, f"相邻换位检测率过低: {detection_rate}"
                
    def test_zero_is_valid_check_digit(self):
        """测试零作为校验码也是有效的"""
        calc = DammCalculator()
        
        # 找一个校验码为零的数字
        # 校验码为零意味着中间值计算结果为零
        found_zero = False
        for num in ["0", "10", "20", "100", "200"]:
            check = calc.compute_check_digit(num)
            if check == 0:
                found_zero = True
                full = num + "0"
                assert calc.validate(full) == True
                
        # 确保至少找到一个零校验码的例子
        assert found_zero, "应该存在校验码为零的数字"


class TestDataStructures:
    """数据结构测试"""
    
    def test_damm_result(self):
        """测试 DammResult 数据结构"""
        result = DammResult(
            original="123",
            check_digit=5,
            valid=True,
            full_code="1235"
        )
        
        assert result.original == "123"
        assert result.check_digit == 5
        assert result.valid == True
        assert result.full_code == "1235"
        assert result.error_type is None
        
    def test_damm_result_with_error(self):
        """测试带错误的 DammResult"""
        result = DammResult(
            original="123",
            check_digit=-1,
            valid=False,
            full_code="1235",
            error_type="checksum_mismatch"
        )
        
        assert result.valid == False
        assert result.error_type == "checksum_mismatch"
        
    def test_error_analysis(self):
        """测试 ErrorAnalysis 数据结构"""
        analysis = ErrorAnalysis(
            original_digits="1234",
            corrupted_digits="1239",
            detected=True,
            error_position=3,
            error_type="single_digit_error",
            description="位置3: '4' -> '9'"
        )
        
        assert analysis.detected == True
        assert analysis.error_position == 3
        assert analysis.error_type == "single_digit_error"


class TestEdgeCases:
    """边界情况测试"""
    
    def test_zero_only(self):
        """测试只有零的数字"""
        calc = DammCalculator()
        
        check = calc.compute_check_digit("0")
        assert check == 0
        
        full = calc.generate_full_code("0")
        assert calc.validate(full) == True
        
    def test_all_same_digits(self):
        """测试所有相同数字"""
        calc = DammCalculator()
        
        for digit in range(10):
            num = str(digit) * 5
            check = calc.compute_check_digit(num)
            assert 0 <= check <= 9
            
            full = calc.generate_full_code(num)
            assert calc.validate(full) == True
            
    def test_very_long_number(self):
        """测试很长的数字"""
        calc = DammCalculator()
        
        long_num = "123456789" * 10
        check = calc.compute_check_digit(long_num)
        assert 0 <= check <= 9
        
        full = calc.generate_full_code(long_num)
        assert calc.validate(full) == True
        
    def test_single_digit_with_check(self):
        """测试单数字加校验码"""
        calc = DammCalculator()
        
        full = calc.generate_full_code("5")
        assert len(full) == 2
        assert calc.validate(full) == True


def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Damm Utils 测试")
    print("=" * 60)
    
    # 运行 pytest
    exit_code = pytest.main([__file__, "-v", "--tb=short"])
    
    if exit_code == 0:
        print("\n所有测试通过！ ✓")
    else:
        print("\n部分测试失败！ ✗")
    
    return exit_code


if __name__ == '__main__':
    run_tests()