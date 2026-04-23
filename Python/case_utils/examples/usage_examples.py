"""
Case Utils 使用示例

演示命名风格转换工具的各种用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import CaseUtils, to_camel_case, to_pascal_case, to_snake_case, to_kebab_case


def example_basic_conversions():
    """基本转换示例"""
    print("=" * 60)
    print("1. 基本转换示例")
    print("=" * 60)
    
    # 各种命名风格的字符串
    examples = [
        "hello_world",      # snake_case
        "HelloWorld",       # PascalCase
        "helloWorld",       # camelCase
        "HELLO_WORLD",      # SCREAMING_SNAKE_CASE
        "hello-world",      # kebab-case
    ]
    
    for example in examples:
        print(f"\n输入: {example!r}")
        print(f"  风格: {CaseUtils.detect_case(example)}")
        print(f"  camelCase: {CaseUtils.to_camel_case(example)}")
        print(f"  PascalCase: {CaseUtils.to_pascal_case(example)}")
        print(f"  snake_case: {CaseUtils.to_snake_case(example)}")
        print(f"  kebab-case: {CaseUtils.to_kebab_case(example)}")


def example_convert_method():
    """使用 convert() 方法"""
    print("\n" + "=" * 60)
    print("2. 使用 convert() 方法")
    print("=" * 60)
    
    text = "user_account_id"
    
    print(f"\n输入: {text!r}")
    print(f"  -> camelCase: {CaseUtils.convert(text, 'camel')}")
    print(f"  -> PascalCase: {CaseUtils.convert(text, 'pascal')}")
    print(f"  -> snake_case: {CaseUtils.convert(text, 'snake')}")
    print(f"  -> SCREAMING_SNAKE: {CaseUtils.convert(text, 'screaming_snake')}")
    print(f"  -> kebab-case: {CaseUtils.convert(text, 'kebab')}")
    print(f"  -> Train-Case: {CaseUtils.convert(text, 'train')}")
    print(f"  -> dot.case: {CaseUtils.convert(text, 'dot')}")
    print(f"  -> Title Case: {CaseUtils.convert(text, 'title')}")
    print(f"  -> Sentence case: {CaseUtils.convert(text, 'sentence')}")
    print(f"  -> path/case: {CaseUtils.convert(text, 'path')}")


def example_convert_all():
    """一次性转换为所有格式"""
    print("\n" + "=" * 60)
    print("3. 使用 convert_all() 获取所有格式")
    print("=" * 60)
    
    text = "xmlHttpRequest"
    result = CaseUtils.convert_all(text)
    
    print(f"\n输入: {text!r}")
    for case_type, value in result.items():
        print(f"  {case_type}: {value}")


def example_detect_case():
    """检测命名风格"""
    print("\n" + "=" * 60)
    print("4. 检测命名风格")
    print("=" * 60)
    
    examples = [
        ("helloWorld", "camelCase 风格"),
        ("HelloWorld", "PascalCase 风格"),
        ("hello_world", "snake_case 风格"),
        ("HELLO_WORLD", "SCREAMING_SNAKE_CASE 风格"),
        ("hello-world", "kebab-case 风格"),
        ("Hello-World", "Train-Case 风格"),
        ("hello.world", "dot.case 风格"),
        ("Hello World", "Title Case 风格"),
    ]
    
    for text, description in examples:
        detected = CaseUtils.detect_case(text)
        print(f"  {text!r:20} -> {detected:15} ({description})")


def example_batch_convert():
    """批量转换"""
    print("\n" + "=" * 60)
    print("5. 批量转换")
    print("=" * 60)
    
    # 数据库列名转换为驼峰
    db_columns = [
        "user_id",
        "first_name",
        "last_name",
        "email_address",
        "created_at",
        "is_active",
    ]
    
    camel_case_columns = CaseUtils.batch_convert(db_columns, "camel")
    
    print("\n数据库列名 -> JavaScript 属性名:")
    for snake, camel in zip(db_columns, camel_case_columns):
        print(f"  {snake:20} -> {camel}")
    
    # 转换为常量名
    constant_names = CaseUtils.batch_convert(db_columns, "constant")
    
    print("\n数据库列名 -> 常量名:")
    for snake, const in zip(db_columns, constant_names):
        print(f"  {snake:20} -> {const}")


def example_validation():
    """验证命名风格"""
    print("\n" + "=" * 60)
    print("6. 验证命名风格")
    print("=" * 60)
    
    examples = [
        ("helloWorld", "camel"),
        ("hello_world", "camel"),
        ("HelloWorld", "pascal"),
        ("hello_world", "snake"),
        ("HELLO_WORLD", "screaming_snake"),
        ("hello-world", "kebab"),
    ]
    
    for text, expected_case in examples:
        is_valid = CaseUtils.is_valid_identifier(text, expected_case)
        status = "✓ 符合" if is_valid else "✗ 不符合"
        print(f"  {text!r:20} {status} {expected_case}")


def example_plural():
    """复数形式转换"""
    print("\n" + "=" * 60)
    print("7. 复数形式转换")
    print("=" * 60)
    
    examples = [
        "userAccount",
        "category",
        "box",
        "item",
        "person",
    ]
    
    for text in examples:
        plural = CaseUtils.to_plural_snake(text)
        print(f"  {text!r:20} -> {plural}")


def example_convenience_functions():
    """使用便捷函数"""
    print("\n" + "=" * 60)
    print("8. 使用便捷函数")
    print("=" * 60)
    
    text = "user_account"
    
    print(f"\n输入: {text!r}")
    print(f"  to_camel_case(): {to_camel_case(text)}")
    print(f"  to_pascal_case(): {to_pascal_case(text)}")
    print(f"  to_snake_case(): {to_snake_case(text)}")
    print(f"  to_kebab_case(): {to_kebab_case(text)}")
    print(f"  detect_case(): {detect_case(text)}")


def example_real_world():
    """实际应用示例"""
    print("\n" + "=" * 60)
    print("9. 实际应用场景")
    print("=" * 60)
    
    # 场景1: API 响应转换为前端格式
    print("\n场景1: API 响应字段名转换")
    api_response = {
        "user_id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email_address": "john@example.com",
        "is_active": True,
        "created_at": "2024-01-01",
    }
    
    def transform_keys(obj, target_case):
        """递归转换字典键名"""
        if isinstance(obj, dict):
            return {CaseUtils.convert(k, target_case): transform_keys(v, target_case) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [transform_keys(item, target_case) for item in obj]
        return obj
    
    js_style = transform_keys(api_response, "camel")
    print(f"  后端 API: {list(api_response.keys())}")
    print(f"  前端 JS:  {list(js_style.keys())}")
    
    # 场景2: 生成数据库列名
    print("\n场景2: 类属性转数据库列名")
    class_attributes = [
        "userId",
        "firstName", 
        "lastName",
        "emailAddress",
        "isActive",
    ]
    
    db_columns = [CaseUtils.to_snake_case(attr) for attr in class_attributes]
    print(f"  类属性: {class_attributes}")
    print(f"  数据库列: {db_columns}")
    
    # 场景3: 生成常量定义
    print("\n场景3: 生成常量定义")
    config_keys = ["apiKey", "apiSecret", "apiEndpoint", "timeout"]
    
    for key in config_keys:
        const_name = CaseUtils.to_screaming_snake_case(key)
        print(f"  const {const_name} = process.env.{const_name};")


def main():
    """运行所有示例"""
    example_basic_conversions()
    example_convert_method()
    example_convert_all()
    example_detect_case()
    example_batch_convert()
    example_validation()
    example_plural()
    example_convenience_functions()
    example_real_world()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()