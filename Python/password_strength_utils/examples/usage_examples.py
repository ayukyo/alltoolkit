"""
密码强度工具集使用示例
展示如何使用密码强度分析、生成、验证等功能
"""

import sys
sys.path.insert(0, '..')

from password_strength_utils.mod import (
    PasswordStrength, PasswordGenerator, PasswordValidator,
    PasswordCrackEstimator, PasswordEntropy, CommonPasswordChecker,
    PatternDetector, StrengthLevel,
    check_password, generate_password, generate_passphrase, is_strong_password
)


def example_basic_analysis():
    """基本密码分析示例"""
    print("\n" + "=" * 60)
    print("1. 基本密码分析")
    print("=" * 60)
    
    passwords = [
        "123456",
        "password",
        "Password1",
        "Tr0ub4dor&3",
        "correct-horse-battery-staple"
    ]
    
    for pwd in passwords:
        result = check_password(pwd)
        print(f"\n密码: {pwd}")
        print(f"强度级别: {result.level.name}")
        print(f"得分: {result.score}/100")
        print(f"熵值: {result.entropy:.2f} 位")
        print(f"预估破解时间: {result.crack_time}")
        if result.issues:
            print(f"问题: {', '.join(i.value for i in result.issues)}")


def example_detailed_analysis():
    """详细密码分析示例"""
    print("\n" + "=" * 60)
    print("2. 详细密码分析")
    print("=" * 60)
    
    analyzer = PasswordStrength(
        min_length=10,
        require_uppercase=True,
        require_lowercase=True,
        require_digit=True,
        require_special=True,
        min_score=70
    )
    
    password = "MySecure@Pass2024"
    result = analyzer.analyze(password)
    
    print(f"\n密码: {password}")
    print(f"强度级别: {result.level.name}")
    print(f"得分: {result.score}/100")
    print(f"熵值: {result.entropy:.2f} 位")
    print(f"破解时间: {result.crack_time}")
    print(f"\n建议:")
    for suggestion in result.suggestions:
        print(f"  - {suggestion}")
    
    # 验证密码
    valid, errors = analyzer.validate(password)
    print(f"\n验证结果: {'通过' if valid else '不通过'}")
    if errors:
        for error in errors:
            print(f"  - {error}")


def example_crack_time_estimation():
    """破解时间估算示例"""
    print("\n" + "=" * 60)
    print("3. 破解时间估算（多种攻击场景）")
    print("=" * 60)
    
    passwords = ["123456", "Password1", "Tr0ub4dor&3", "xY7!kL2@mN9#pQ4$"]
    
    for pwd in passwords:
        print(f"\n密码: {pwd}")
        scenarios = PasswordCrackEstimator.estimate_all_scenarios(pwd)
        for scenario, time in scenarios.items():
            print(f"  {scenario}: {time}")


def example_entropy_calculation():
    """熵值计算示例"""
    print("\n" + "=" * 60)
    print("4. 熵值计算")
    print("=" * 60)
    
    passwords = [
        "a",          # 单字符
        "abc",        # 纯小写
        "ABC",        # 纯大写
        "Abc",        # 混合大小写
        "Abc1",       # 加数字
        "Abc1!",      # 加特殊字符
        "Abc1!中文",  # 加扩展字符
    ]
    
    for pwd in passwords:
        entropy = PasswordEntropy.calculate(pwd)
        charset = PasswordEntropy._get_charset_size(pwd)
        print(f"密码 '{pwd}': 熵={entropy:.2f} 位, 字符集大小={charset}")


def example_pattern_detection():
    """模式检测示例"""
    print("\n" + "=" * 60)
    print("5. 模式检测")
    print("=" * 60)
    
    test_passwords = [
        "abcdef123",      # 连续字母和数字
        "aaabbbccc",      # 重复字符
        "qwerty123",      # 键盘模式
        "password1990",   # 日期和字典单词
        "admin123",       # 常见密码变体
    ]
    
    for pwd in test_passwords:
        print(f"\n密码: {pwd}")
        
        # 连续字符
        sequential = PatternDetector.detect_sequential(pwd)
        if sequential:
            print(f"  连续字符: {sequential}")
        
        # 重复字符
        repeated = PatternDetector.detect_repeated(pwd)
        if repeated:
            print(f"  重复字符: {repeated}")
        
        # 键盘模式
        keyboard = PatternDetector.detect_keyboard_pattern(pwd)
        if keyboard:
            print(f"  键盘模式: {keyboard}")
        
        # 日期模式
        dates = PatternDetector.detect_date_pattern(pwd)
        if dates:
            print(f"  日期模式: {dates}")
        
        # 字典单词
        words = PatternDetector.detect_dictionary_word(pwd)
        if words:
            print(f"  字典单词: {words}")


def example_common_password_check():
    """常见密码检测示例"""
    print("\n" + "=" * 60)
    print("6. 常见密码检测")
    print("=" * 60)
    
    passwords = [
        "123456",
        "password",
        "admin123",
        "qwerty",
        "MyUniqueP@ssw0rd",
        "PASSWORD",  # 大写变体
        "drowssap",  # 反向
    ]
    
    for pwd in passwords:
        is_common = CommonPasswordChecker.is_common(pwd)
        variants = CommonPasswordChecker.check_variants(pwd)
        
        status = "常见弱密码 ⚠️" if is_common else "非常见密码 ✓"
        print(f"\n密码 '{pwd}': {status}")
        
        if variants:
            print(f"  变体类型: {', '.join(variants)}")


def example_password_generation():
    """密码生成示例"""
    print("\n" + "=" * 60)
    print("7. 密码生成")
    print("=" * 60)
    
    # 默认生成
    print("\n默认密码 (16位):")
    for i in range(3):
        pwd = generate_password()
        result = check_password(pwd)
        print(f"  {pwd} [{result.level.name}, {result.score}/100]")
    
    # 自定义长度
    print("\n不同长度的密码:")
    for length in [8, 12, 20, 32]:
        pwd = generate_password(length=length)
        print(f"  {length}位: {pwd}")
    
    # 不含特殊字符
    print("\n不含特殊字符的密码:")
    pwd = generate_password(use_special=False)
    print(f"  {pwd}")
    
    # 包含混淆字符
    print("\n包含混淆字符的密码:")
    gen = PasswordGenerator(length=16, exclude_ambiguous=False)
    pwd = gen.generate()
    print(f"  {pwd}")


def example_passphrase_generation():
    """密码短语生成示例"""
    print("\n" + "=" * 60)
    print("8. 密码短语生成")
    print("=" * 60)
    
    gen = PasswordGenerator()
    
    # 默认密码短语
    print("\n4词密码短语:")
    for i in range(3):
        phrase = gen.generate_passphrase(word_count=4)
        result = check_password(phrase)
        print(f"  {phrase} [{result.level.name}]")
    
    # 带数字
    print("\n带数字的密码短语:")
    phrase = gen.generate_passphrase(word_count=4, add_number=True)
    print(f"  {phrase}")
    
    # 首字母大写
    print("\n首字母大写的密码短语:")
    phrase = gen.generate_passphrase(word_count=4, capitalize=True)
    print(f"  {phrase}")
    
    # 更多单词
    print("\n6词密码短语:")
    phrase = gen.generate_passphrase(word_count=6)
    print(f"  {phrase}")


def example_password_validation():
    """密码验证示例"""
    print("\n" + "=" * 60)
    print("9. 密码验证")
    print("=" * 60)
    
    validator = PasswordValidator()
    
    passwords = [
        ("short", {}),
        ("password123", {}),
        ("StrongPassword1!", {"min_entropy": 50}),
        ("VeryStr0ng!Pass", {"min_score": 80}),
    ]
    
    for pwd, kwargs in passwords:
        valid, errors = validator.validate(pwd, exclude_common=True, **kwargs)
        
        print(f"\n密码 '{pwd}':")
        print(f"  验证结果: {'✓ 通过' if valid else '✗ 不通过'}")
        if errors:
            for error in errors:
                print(f"    - {error}")
    
    # 强度摘要
    print("\n强度摘要示例:")
    summary = validator.get_strength_summary("MySecure@Pass2024")
    print(summary)


def example_strong_password_check():
    """强密码判断示例"""
    print("\n" + "=" * 60)
    print("10. 快速强密码判断")
    print("=" * 60)
    
    passwords = [
        "123456",
        "password",
        "Password1",
        "Tr0ub4dor&3",
        "xY7!kL2@mN9#pQ4$wE5&",
    ]
    
    print(f"\n判断标准: min_score=60")
    for pwd in passwords:
        result = is_strong_password(pwd, min_score=60)
        status = "✓ 强密码" if result else "✗ 弱密码"
        print(f"  {pwd}: {status}")
    
    print(f"\n判断标准: min_score=80")
    for pwd in passwords:
        result = is_strong_password(pwd, min_score=80)
        status = "✓ 强密码" if result else "✗ 弱密码"
        print(f"  {pwd}: {status}")


def example_full_workflow():
    """完整工作流示例"""
    print("\n" + "=" * 60)
    print("11. 完整工作流: 生成 → 分析 → 验证")
    print("=" * 60)
    
    # 配置
    analyzer = PasswordStrength(
        min_length=12,
        require_uppercase=True,
        require_lowercase=True,
        require_digit=True,
        require_special=True,
        min_score=75
    )
    
    gen = PasswordGenerator(
        length=16,
        use_lowercase=True,
        use_uppercase=True,
        use_digits=True,
        use_special=True,
        exclude_ambiguous=True
    )
    
    # 生成多个密码
    print("\n生成5个候选密码:")
    passwords = gen.generate_multiple(5)
    
    # 分析并筛选
    valid_passwords = []
    for pwd in passwords:
        result = analyzer.analyze(pwd)
        print(f"\n  {pwd}")
        print(f"    强度: {result.level.name} ({result.score}/100)")
        print(f"    熵值: {result.entropy:.2f} 位")
        print(f"    破解时间: {result.crack_time}")
        
        if result.is_strong:
            valid_passwords.append(pwd)
    
    # 最终推荐
    print(f"\n符合要求的密码 ({len(valid_passwords)}/5):")
    for pwd in valid_passwords:
        print(f"  ✓ {pwd}")
    
    if valid_passwords:
        print(f"\n推荐使用: {valid_passwords[0]}")


def main():
    """运行所有示例"""
    example_basic_analysis()
    example_detailed_analysis()
    example_crack_time_estimation()
    example_entropy_calculation()
    example_pattern_detection()
    example_common_password_check()
    example_password_generation()
    example_passphrase_generation()
    example_password_validation()
    example_strong_password_check()
    example_full_workflow()
    
    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()