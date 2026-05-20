# -*- coding: utf-8 -*-
"""
AllToolkit - Either Utils 使用示例

展示 Either 单子的各种实际应用场景。
"""

from typing import List, Dict, Any, Optional
import math
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Either, Left, Right, left, right,
    from_optional, from_exception, try_catch,
    sequence, sequence_first_error, traverse, partition_eithers,
    cond_either, bimap, ensure, ensure_pred,
    EitherChain, chain, chain_error,
    all_rights, all_lefts, get_or_else
)


# =============================================================================
# 示例 1: 基础用法
# =============================================================================

def example_basics():
    """基础用法示例"""
    print("\n" + "="*60)
    print("示例 1: 基础用法")
    print("="*60)
    
    # 创建 Either
    success: Either[str, int] = Right(42)
    failure: Either[str, int] = Left("Something went wrong")
    
    print(f"成功: {success}")
    print(f"失败: {failure}")
    
    # 获取值
    print(f"成功值: {success.get_or_else(0)}")
    print(f"失败默认值: {failure.get_or_else(0)}")
    
    # 检查类型
    print(f"成功是 Right: {success.is_right()}")
    print(f"失败是 Left: {failure.is_left()}")
    
    # 布尔转换
    print(f"Right 可用作 True: {bool(success)}")
    print(f"Left 可用作 False: {bool(failure)}")


# =============================================================================
# 示例 2: 映射操作
# =============================================================================

def example_map_operations():
    """映射操作示例"""
    print("\n" + "="*60)
    print("示例 2: 映射操作")
    print("="*60)
    
    # map - 只对 Right 操作
    result1 = Right(5).map(lambda x: x * 2)
    print(f"Right(5).map(x => x*2): {result1}")
    
    result2: Either[str, int] = Left("error").map(lambda x: x * 2)
    print(f"Left('error').map(x => x*2): {result2}")
    
    # map_left - 只对 Left 操作
    result3 = Left(404).map_left(lambda e: f"HTTP Error {e}")
    print(f"Left(404).map_left(e => 'HTTP Error e'): {result3}")
    
    # flat_map - 链式操作
    def safe_divide(n: int) -> Either[str, float]:
        return Right(100 / n) if n != 0 else Left("Division by zero")
    
    result4 = Right(2).flat_map(safe_divide)
    print(f"Right(2).flat_map(safe_divide): {result4}")
    
    result5: Either[str, float] = Right(0).flat_map(safe_divide)
    print(f"Right(0).flat_map(safe_divide): {result5}")
    
    # 双向映射
    transform = bimap(str.upper, lambda x: x * 2)
    print(f"bimap 对 Right(5): {transform(Right(5))}")
    print(f"bimap 对 Left('error'): {transform(Left('error'))}")


# =============================================================================
# 示例 3: 错误处理
# =============================================================================

def example_error_handling():
    """错误处理示例"""
    print("\n" + "="*60)
    print("示例 3: 错误处理")
    print("="*60)
    
    # 安全解析
    def safe_int(s: str) -> Either[str, int]:
        try:
            return Right(int(s))
        except ValueError:
            return Left(f"Cannot parse '{s}' as integer")
    
    print(f"safe_int('42'): {safe_int('42')}")
    print(f"safe_int('abc'): {safe_int('abc')}")
    
    # 使用 try_catch 装饰器
    @try_catch
    def divide(a: int, b: int) -> float:
        return a / b
    
    print(f"divide(10, 2): {divide(10, 2)}")
    print(f"divide(10, 0): {divide(10, 0)}")
    
    # from_exception
    result = from_exception(lambda: int("abc"), str)
    print(f"from_exception(int('abc'), str): {result}")
    
    # fold - 处理两种情况
    message = safe_int("abc").fold(
        lambda e: f"❌ 错误: {e}",
        lambda v: f"✅ 成功: 值为 {v}"
    )
    print(f"fold 处理结果: {message}")


# =============================================================================
# 示例 4: 验证
# =============================================================================

def example_validation():
    """验证示例"""
    print("\n" + "="*60)
    print("示例 4: 验证")
    print("="*60)
    
    # 使用 ensure 确保条件
    def validate_positive(n: int) -> Either[str, int]:
        return ensure(n, n > 0, "Number must be positive")
    
    print(f"validate_positive(5): {validate_positive(5)}")
    print(f"validate_positive(-5): {validate_positive(-5)}")
    
    # 使用 ensure_pred 进行复杂验证
    def validate_email(email: str) -> Either[str, str]:
        return ensure_pred(
            email,
            lambda e: "@" in e and "." in e,
            lambda e: f"'{e}' is not a valid email"
        )
    
    print(f"validate_email('user@example.com'): {validate_email('user@example.com')}")
    print(f"validate_email('invalid'): {validate_email('invalid')}")
    
    # 链式验证
    def validate_user(name: str, age: int) -> Either[List[str], Dict[str, Any]]:
        errors: List[str] = []
        
        if not name:
            errors.append("Name is required")
        elif len(name) < 2:
            errors.append("Name must be at least 2 characters")
        
        if age < 0:
            errors.append("Age cannot be negative")
        elif age > 150:
            errors.append("Age seems unrealistic")
        
        if errors:
            return Left(errors)
        return Right({"name": name, "age": age})
    
    print(f"验证有效用户: {validate_user('Alice', 25)}")
    print(f"验证无效用户: {validate_user('', -5)}")


# =============================================================================
# 示例 5: 链式操作
# =============================================================================

def example_chain_operations():
    """链式操作示例"""
    print("\n" + "="*60)
    print("示例 5: 链式操作")
    print("="*60)
    
    # 使用 EitherChain 进行流畅的链式操作
    result = (chain(10)
        .map(lambda x: x * 2)
        .filter(lambda x: x > 15, "Value too small")
        .map(lambda x: x + 1)
        .build())
    
    print(f"chain(10).map(x*2).filter(x>15).map(x+1): {result}")
    
    # 从错误开始的链
    result2 = (chain_error("initial error")
        .map(lambda x: x * 2)
        .recover(Right(100))
        .build())
    
    print(f"从错误恢复: {result2}")
    
    # 实际计算链
    def safe_sqrt(n: float) -> Either[str, float]:
        if n < 0:
            return Left(f"Cannot sqrt negative number {n}")
        return Right(math.sqrt(n))
    
    def safe_divide(a: float, b: float) -> Either[str, float]:
        if b == 0:
            return Left("Division by zero")
        return Right(a / b)
    
    # 计算 sqrt(100/4) = sqrt(25) = 5
    result3 = (chain(100)
        .flat_map(lambda x: safe_divide(x, 4))
        .flat_map(safe_sqrt)
        .build())
    
    print(f"计算 sqrt(100/4): {result3}")
    
    # 失败的计算
    result4 = (chain(100)
        .flat_map(lambda x: safe_divide(x, 0))
        .flat_map(safe_sqrt)
        .build())
    
    print(f"计算 sqrt(100/0): {result4}")


# =============================================================================
# 示例 6: 批量操作
# =============================================================================

def example_batch_operations():
    """批量操作示例"""
    print("\n" + "="*60)
    print("示例 6: 批量操作")
    print("="*60)
    
    def safe_int(s: str) -> Either[str, int]:
        try:
            return Right(int(s))
        except ValueError:
            return Left(f"Invalid: '{s}'")
    
    # sequence - 收集所有错误或所有成功
    inputs = ["1", "2", "3"]
    result1 = sequence([safe_int(s) for s in inputs])
    print(f"sequence 成功: {result1}")
    
    inputs2 = ["1", "abc", "3", "xyz"]
    result2 = sequence([safe_int(s) for s in inputs2])
    print(f"sequence 失败: {result2}")
    
    # traverse - 直接遍历
    result3 = traverse(safe_int, ["10", "20", "30"])
    print(f"traverse 成功: {result3}")
    
    result4 = traverse(safe_int, ["10", "bad", "30"])
    print(f"traverse 失败: {result4}")
    
    # partition_eithers - 分离成功和失败
    eithers = [safe_int("1"), safe_int("abc"), safe_int("2"), safe_int("xyz")]
    lefts, rights = partition_eithers(eithers)
    print(f"分离结果: 成功={rights}, 失败={lefts}")
    
    # all_rights 和 all_lefts
    print(f"所有成功值: {all_rights(eithers)}")
    print(f"所有失败值: {all_lefts(eithers)}")


# =============================================================================
# 示例 7: 条件分支
# =============================================================================

def example_conditional():
    """条件分支示例"""
    print("\n" + "="*60)
    print("示例 7: 条件分支")
    print("="*60)
    
    # cond_either - 函数式条件
    classify_number = cond_either(
        (lambda x: x > 0, lambda x: Right("正数")),
        (lambda x: x < 0, lambda x: Right("负数")),
        (lambda x: True, lambda x: Left("零不被允许")),
    )
    
    print(f"classify_number(5): {classify_number(5)}")
    print(f"classify_number(-5): {classify_number(-5)}")
    print(f"classify_number(0): {classify_number(0)}")
    
    # filter 结合 map
    def process_score(score: int) -> Either[str, str]:
        return (Right(score)
            .filter(lambda s: s >= 0, "Score cannot be negative")
            .filter(lambda s: s <= 100, "Score cannot exceed 100")
            .map(lambda s: "优秀" if s >= 90 else "良好" if s >= 70 else "及格"))
    
    print(f"process_score(95): {process_score(95)}")
    print(f"process_score(-5): {process_score(-5)}")
    print(f"process_score(150): {process_score(150)}")


# =============================================================================
# 示例 8: 实际应用 - HTTP 请求模拟
# =============================================================================

def example_http_request():
    """HTTP 请求模拟示例"""
    print("\n" + "="*60)
    print("示例 8: HTTP 请求模拟")
    print("="*60)
    
    # 模拟 HTTP 响应
    def mock_http_request(url: str) -> Either[int, Dict[str, Any]]:
        """模拟 HTTP 请求"""
        if not url.startswith("http"):
            return Left(400)  # Bad Request
        
        if url == "http://api.example.com/error":
            return Left(500)  # Internal Server Error
        
        if url == "http://api.example.com/users":
            return Right({"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]})
        
        return Left(404)  # Not Found
    
    # 处理响应
    def handle_response(response: Either[int, Dict]) -> Either[str, str]:
        return response.fold(
            lambda code: Left(f"请求失败，状态码: {code}"),
            lambda data: Right(f"成功获取 {len(data)} 个用户")
        )
    
    # 测试不同 URL
    urls = [
        "http://api.example.com/users",
        "http://api.example.com/error",
        "ftp://invalid.url",
        "http://api.example.com/unknown",
    ]
    
    for url in urls:
        response = mock_http_request(url)
        result = handle_response(response)
        print(f"URL: {url} => {result}")


# =============================================================================
# 示例 9: 实际应用 - 数据库操作模拟
# =============================================================================

def example_database_operations():
    """数据库操作模拟示例"""
    print("\n" + "="*60)
    print("示例 9: 数据库操作模拟")
    print("="*60)
    
    # 模拟数据库
    mock_db = {
        1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
        2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
        3: {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
    }
    
    def find_user(user_id: int) -> Either[str, Dict[str, Any]]:
        """查找用户"""
        return from_optional(
            mock_db.get(user_id),
            f"User {user_id} not found"
        )
    
    def get_user_email(user_id: int) -> Either[str, str]:
        """获取用户邮箱"""
        return (find_user(user_id)
            .map(lambda user: user["email"])
            .filter(lambda email: "@" in email, "Invalid email format"))
    
    # 测试
    print(f"获取用户 1 邮箱: {get_user_email(1)}")
    print(f"获取用户 999 邮箱: {get_user_email(999)}")
    
    # 批量查询
    user_ids = [1, 2, 999, 3]
    results = traverse(find_user, user_ids)
    
    print(f"批量查询结果: {results}")
    
    # 分离成功和失败
    individual_results = [find_user(id) for id in user_ids]
    found_users = all_rights(individual_results)
    missing_ids = all_lefts(individual_results)
    
    print(f"找到的用户数: {len(found_users)}")
    print(f"缺失的用户: {missing_ids}")


# =============================================================================
# 示例 10: 组合模式 - 多步骤操作
# =============================================================================

def example_composed_operations():
    """组合多步骤操作示例"""
    print("\n" + "="*60)
    print("示例 10: 组合多步骤操作")
    print("="*60)
    
    # 定义一系列操作
    def parse_input(s: str) -> Either[str, int]:
        """解析输入"""
        try:
            n = int(s)
            if n < 0:
                return Left("输入必须为正数")
            return Right(n)
        except ValueError:
            return Left(f"无法解析 '{s}'")
    
    def validate_range(n: int) -> Either[str, int]:
        """验证范围"""
        return ensure_pred(n, lambda x: 1 <= x <= 100, lambda x: f"{x} 超出范围 [1-100]")
    
    def compute_result(n: int) -> Either[str, float]:
        """计算结果"""
        try:
            return Right(math.sqrt(n) * 10)
        except Exception as e:
            return Left(str(e))
    
    def format_output(result: float) -> Either[str, str]:
        """格式化输出"""
        return Right(f"计算结果: {result:.2f}")
    
    # 组合所有步骤
    def process_user_input(input_str: str) -> Either[str, str]:
        """处理用户输入的完整流程"""
        return (parse_input(input_str)
            .flat_map(validate_range)
            .flat_map(compute_result)
            .flat_map(format_output))
    
    # 测试不同输入
    test_inputs = ["25", "-5", "abc", "150", "100"]
    
    for input_str in test_inputs:
        result = process_user_input(input_str)
        print(f"输入 '{input_str}': {result}")
    
    # 使用 EitherChain 的流畅语法
    def process_with_chain(input_str: str) -> Either[str, str]:
        return (EitherChain(parse_input(input_str))
            .flat_map(validate_range)
            .flat_map(compute_result)
            .on_success(lambda r: print(f"  [日志] 成功计算: {r:.2f}"))
            .on_failure(lambda e: print(f"  [日志] 失败: {e}"))
            .map(lambda r: f"最终结果: {r:.2f}")
            .build())
    
    print("\n使用 EitherChain 处理 '25':")
    result = process_with_chain("25")
    print(f"结果: {result}")


# =============================================================================
# 主函数
# =============================================================================

def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("AllToolkit - Either Utils 使用示例")
    print("="*60)
    
    example_basics()
    example_map_operations()
    example_error_handling()
    example_validation()
    example_chain_operations()
    example_batch_operations()
    example_conditional()
    example_http_request()
    example_database_operations()
    example_composed_operations()
    
    print("\n" + "="*60)
    print("所有示例完成!")
    print("="*60)


if __name__ == "__main__":
    main()