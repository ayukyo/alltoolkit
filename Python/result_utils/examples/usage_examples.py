# -*- coding: utf-8 -*-
"""
AllToolkit - Result Utils 使用示例

展示 Result/Either 类型的各种用法和最佳实践。
"""

from mod import (
    Ok, Error, Result, Left, Right, Either,
    ok, error, left, right,
    from_optional, from_exception,
    try_call, try_call_with,
    collect_results, partition_results, first_ok,
    safe_get, safe_index, safe_divide,
    safe_parse_int, safe_parse_float,
    ResultContext,
    pretty_result, result_trace,
    is_ok, is_error, is_result
)


def example_basic_usage():
    """基本用法示例"""
    print("=" * 60)
    print("基本用法示例")
    print("=" * 60)
    
    # 创建 Result
    success = Ok(42)
    failure = Error("something went wrong")
    
    print(f"成功结果: {success}")
    print(f"失败结果: {failure}")
    
    # 检查类型
    print(f"success.is_ok(): {success.is_ok()}")
    print(f"failure.is_error(): {failure.is_error()}")
    
    # 获取值
    print(f"success.unwrap(): {success.unwrap()}")
    print(f"failure.unwrap_error(): {failure.unwrap_error()}")
    
    # 安全解包
    print(f"failure.unwrap_or(0): {failure.unwrap_or(0)}")
    
    print()


def example_map_operations():
    """映射操作示例"""
    print("=" * 60)
    print("映射操作示例")
    print("=" * 60)
    
    # map - 对成功值应用函数
    result = Ok(10)
    doubled = result.map(lambda x: x * 2)
    print(f"Ok(10).map(x * 2) = {doubled}")
    
    # map 对 Error 不起作用
    result2 = Error("error")
    mapped_error = result2.map(lambda x: x * 2)
    print(f"Error('error').map(x * 2) = {mapped_error}")
    
    # map_error - 对错误值应用函数
    error_wrapped = result2.map_error(lambda e: f"Wrapped: {e}")
    print(f"Error('error').map_error(wrap) = {error_wrapped}")
    
    print()


def example_chain_operations():
    """链式操作示例"""
    print("=" * 60)
    print("链式操作示例")
    print("=" * 60)
    
    def validate_positive(n: int) -> Result[int, str]:
        if n > 0:
            return Ok(n)
        return Error(f"{n} is not positive")
    
    def double(n: int) -> Result[int, str]:
        return Ok(n * 2)
    
    # 成功链
    result = Ok(5).and_then(validate_positive).and_then(double)
    print(f"Ok(5).and_then(validate).and_then(double) = {result}")
    
    # 失败链
    result2 = Ok(-5).and_then(validate_positive).and_then(double)
    print(f"Ok(-5).and_then(validate).and_then(double) = {result2}")
    
    # or_else - 错误恢复
    result3 = Error("primary failed").or_else(lambda e: Ok("fallback"))
    print(f"Error.or_else(fallback) = {result3}")
    
    print()


def example_from_exception():
    """异常转换示例"""
    print("=" * 60)
    print("异常转换示例")
    print("=" * 60)
    
    # 使用装饰器将异常函数转换为 Result 函数
    @from_exception
    def divide(a: float, b: float) -> float:
        return a / b
    
    result1 = divide(10, 2)
    print(f"divide(10, 2) = {pretty_result(result1)}")
    
    result2 = divide(10, 0)
    print(f"divide(10, 0) = {pretty_result(result2)}")
    
    # 使用 try_call
    result3 = try_call(int, "42")
    print(f"try_call(int, '42') = {pretty_result(result3)}")
    
    result4 = try_call(int, "not a number")
    print(f"try_call(int, 'abc') = {pretty_result(result4)}")
    
    print()


def example_safe_operations():
    """安全操作示例"""
    print("=" * 60)
    print("安全操作示例")
    print("=" * 60)
    
    # 安全字典访问
    data = {"name": "Alice", "age": 30}
    
    name = safe_get(data, "name", "not found")
    print(f"safe_get(data, 'name') = {pretty_result(name)}")
    
    email = safe_get(data, "email", "missing")
    print(f"safe_get(data, 'email') = {pretty_result(email)}")
    
    # 安全列表访问
    items = [1, 2, 3, 4, 5]
    
    item = safe_index(items, 2, "index error")
    print(f"safe_index([1,2,3,4,5], 2) = {pretty_result(item)}")
    
    out_of_bounds = safe_index(items, 10, "out of bounds")
    print(f"safe_index(items, 10) = {pretty_result(out_of_bounds)}")
    
    # 安全除法
    division = safe_divide(100, 5)
    print(f"safe_divide(100, 5) = {pretty_result(division)}")
    
    zero_div = safe_divide(100, 0)
    print(f"safe_divide(100, 0) = {pretty_result(zero_div)}")
    
    # 安全解析
    num = safe_parse_int("12345")
    print(f"safe_parse_int('12345') = {pretty_result(num)}")
    
    invalid = safe_parse_int("not a number")
    print(f"safe_parse_int('abc') = {pretty_result(invalid)}")
    
    print()


def example_collect_results():
    """收集结果示例"""
    print("=" * 60)
    print("收集结果示例")
    print("=" * 60)
    
    # collect_results - 全成功返回列表，否则返回错误列表
    all_ok = [Ok(1), Ok(2), Ok(3)]
    collected = collect_results(all_ok)
    print(f"collect_results([Ok(1), Ok(2), Ok(3)]) = {pretty_result(collected)}")
    
    mixed = [Ok(1), Error("e1"), Ok(2), Error("e2")]
    collected2 = collect_results(mixed)
    print(f"collect_results(mixed) = {collected2}")
    
    # partition_results - 分离成功和失败
    values, errors = partition_results(mixed)
    print(f"partition_results(mixed) -> values={values}, errors={errors}")
    
    # first_ok - 获取第一个成功
    results = [Error("e1"), Error("e2"), Ok(42), Ok(43)]
    first = first_ok(results)
    print(f"first_ok([...]) = {pretty_result(first)}")
    
    print()


def example_either_type():
    """Either 类型示例"""
    print("=" * 60)
    print("Either 类型示例")
    print("=" * 60)
    
    # Either 可以表示二元状态
    # 传统用法：Left = 失败/错误，Right = 成功/值
    
    success = Right(42)
    failure = Left("error")
    
    print(f"成功: {success}")
    print(f"失败: {failure}")
    
    # fold - 根据类型应用不同函数
    message = success.fold(
        left_fn=lambda e: f"Error: {e}",
        right_fn=lambda v: f"Success: {v}"
    )
    print(f"fold result: {message}")
    
    # swap - 交换左右
    swapped = success.swap()
    print(f"Right(42).swap() = {swapped}")
    
    # 其他用途：表示选择或分支
    # 例如：配置选项 Left(默认值) vs Right(用户值)
    default_config = Left({"timeout": 30})
    user_config = Right({"timeout": 60, "retry": 3})
    
    # 合并配置
    merged = user_config.fold(
        left_fn=lambda c: c,
        right_fn=lambda c: c  # 用户配置优先
    )
    print(f"配置: {merged}")
    
    print()


def example_error_handling_pattern():
    """错误处理模式示例"""
    print("=" * 60)
    print("错误处理模式 - 替代 try-except")
    print("=" * 60)
    
    # 传统方式
    def traditional_divide(a, b):
        try:
            result = a / b
            return result
        except ZeroDivisionError:
            return None
    
    # Result 方式 - 更明确的类型
    def result_divide(a: float, b: float) -> Result[float, str]:
        if b == 0:
            return Error("division by zero")
        return Ok(a / b)
    
    # 使用 Result 可以链式处理
    result = result_divide(10, 2).map(lambda x: x * 3)
    print(f"result_divide(10, 2).map(x * 3) = {pretty_result(result)}")
    
    # 错误恢复
    result2 = result_divide(10, 0).unwrap_or(0)
    print(f"result_divide(10, 0).unwrap_or(0) = {result2}")
    
    # 验证链
    def validate_input(s: str) -> Result[int, str]:
        return safe_parse_int(s, f"'{s}' is not a valid integer")
    
    def validate_range(n: int) -> Result[int, str]:
        if 1 <= n <= 100:
            return Ok(n)
        return Error(f"{n} is out of range [1, 100]")
    
    def process(n: int) -> Result[str, str]:
        return Ok(f"processed: {n}")
    
    # 完整验证链
    final = validate_input("50").and_then(validate_range).and_then(process)
    print(f"验证链成功: {pretty_result(final)}")
    
    final2 = validate_input("abc").and_then(validate_range).and_then(process)
    print(f"验证链失败(解析): {final2}")
    
    final3 = validate_input("200").and_then(validate_range).and_then(process)
    print(f"验证链失败(范围): {final3}")
    
    print()


def example_context_manager():
    """上下文管理器示例"""
    print("=" * 60)
    print("ResultContext 上下文管理器")
    print("=" * 60)
    
    # 自动捕获异常
    with ResultContext() as ctx:
        value = int("42")
        ctx.set_ok(value)
    
    print(f"成功上下文: {pretty_result(ctx.get_result())}")
    
    with ResultContext() as ctx:
        value = int("not a number")  # 抛出 ValueError
        ctx.set_ok(value)  # 这行不会执行
    
    print(f"异常上下文: {pretty_result(ctx.get_result())}")
    
    print()


def example_api_response_pattern():
    """API 响应模式示例"""
    print("=" * 60)
    print("模拟 API 响应处理")
    print("=" * 60)
    
    def fetch_user(user_id: int) -> Result[dict, str]:
        """模拟获取用户"""
        if user_id <= 0:
            return Error("invalid user id")
        if user_id == 999:
            return Error("user not found")
        return Ok({"id": user_id, "name": f"User{user_id}", "email": f"user{user_id}@example.com"})
    
    def validate_email(user: dict) -> Result[dict, str]:
        """验证邮箱"""
        if "@" not in user.get("email", ""):
            return Error("invalid email format")
        return Ok(user)
    
    def send_notification(user: dict) -> Result[str, str]:
        """发送通知"""
        return Ok(f"Notification sent to {user['email']}")
    
    # 处理流程
    def notify_user(user_id: int) -> Result[str, str]:
        return fetch_user(user_id).and_then(validate_email).and_then(send_notification)
    
    # 成功流程
    result1 = notify_user(1)
    print(f"notify_user(1): {pretty_result(result1)}")
    
    # 用户不存在
    result2 = notify_user(999)
    print(f"notify_user(999): {pretty_result(result2)}")
    
    # 无效 ID
    result3 = notify_user(-1)
    print(f"notify_user(-1): {pretty_result(result3)}")
    
    print()


def example_file_processing():
    """文件处理模式示例"""
    print("=" * 60)
    print("文件处理模式（模拟）")
    print("=" * 60)
    
    def read_file(filename: str) -> Result[str, str]:
        """模拟读取文件"""
        if filename.endswith(".txt"):
            return Ok(f"content of {filename}")
        return Error(f"unsupported file type: {filename}")
    
    def parse_content(content: str) -> Result[list, str]:
        """模拟解析内容"""
        lines = content.split("\n")
        if len(lines) > 0:
            return Ok(lines)
        return Error("empty file")
    
    def process_lines(lines: list) -> Result[int, str]:
        """处理行"""
        return Ok(len(lines))
    
    # 处理流程
    result = read_file("data.txt").and_then(parse_content).and_then(process_lines)
    print(f"处理 data.txt: {pretty_result(result)}")
    
    result2 = read_file("data.pdf").and_then(parse_content).and_then(process_lines)
    print(f"处理 data.pdf: {pretty_result(result2)}")
    
    print()


def main():
    """运行所有示例"""
    example_basic_usage()
    example_map_operations()
    example_chain_operations()
    example_from_exception()
    example_safe_operations()
    example_collect_results()
    example_either_type()
    example_error_handling_pattern()
    example_context_manager()
    example_api_response_pattern()
    example_file_processing()
    
    print("=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()