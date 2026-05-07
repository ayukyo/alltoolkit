"""
CUID2 Utils 测试套件

测试覆盖：
- ID 生成（单次、批量）
- 格式验证
- 唯一性保证
- 线程安全
- 边界值测试
- 性能测试
"""

import sys
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cuid2_utils.mod import (
    Cuid2,
    SecureCuid2,
    PrefixedCuid2,
    create_id,
    create_id_batch,
    create_prefixed_id,
    is_cuid2,
    BASE36_CHARS,
    BASE62_CHARS
)


class TestResult:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_true(self, condition, message=""):
        if condition:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"断言失败: {message}")
    
    def assert_false(self, condition, message=""):
        self.assert_true(not condition, message)
    
    def assert_equal(self, actual, expected, message=""):
        self.assert_true(actual == expected, f"{message} - 期望: {expected}, 实际: {actual}")
    
    def assert_not_equal(self, actual, expected, message=""):
        self.assert_true(actual != expected, f"{message} - 不应等于 {expected}")
    
    def assert_in(self, item, container, message=""):
        self.assert_true(item in container, f"{message} - {item} 不在 {container} 中")
    
    def assert_is_none(self, value, message=""):
        self.assert_true(value is None, f"{message} - 期望 None, 实际: {value}")
    
    def assert_is_not_none(self, value, message=""):
        self.assert_true(value is not None, f"{message} - 期望非 None")
    
    def assert_raises(self, exception_class, func, message=""):
        try:
            func()
            self.failed += 1
            self.errors.append(f"{message} - 期望抛出 {exception_class.__name__}")
        except exception_class:
            self.passed += 1
    
    def assert_len(self, obj, expected_len, message=""):
        self.assert_equal(len(obj), expected_len, message)


def test_basic_generation():
    """测试基本 ID 生成"""
    result = TestResult()
    
    # 测试默认长度
    cuid = Cuid2()
    id1 = cuid.generate()
    result.assert_len(id1, 24, "默认长度应为 24")
    
    # 测试自定义长度
    cuid_short = Cuid2(length=10)
    id2 = cuid_short.generate()
    result.assert_len(id2, 10, "自定义长度应为 10")
    
    # 测试最大长度
    cuid_long = Cuid2(length=32)
    id3 = cuid_long.generate()
    result.assert_len(id3, 32, "最大长度应为 32")
    
    # 测试最小长度
    cuid_min = Cuid2(length=2)
    id4 = cuid_min.generate()
    result.assert_len(id4, 2, "最小长度应为 2")
    
    return result


def test_validity():
    """测试 ID 验证"""
    result = TestResult()
    cuid = Cuid2()
    
    # 测试有效 ID
    valid_id = cuid.generate()
    result.assert_true(cuid.is_valid(valid_id), "生成的 ID 应该有效")
    
    # 测试无效 ID - 空字符串
    result.assert_false(cuid.is_valid(""), "空字符串应无效")
    
    # 测试无效 ID - 过短
    result.assert_false(cuid.is_valid("a"), "长度为 1 应无效")
    
    # 测试无效 ID - 过长
    result.assert_false(cuid.is_valid("a" * 33), "长度超过 32 应无效")
    
    # 测试无效 ID - 非法字符
    result.assert_false(cuid.is_valid("abc!@#"), "含特殊字符应无效")
    
    # 测试有效 ID - 边界长度
    result.assert_true(cuid.is_valid("ab"), "最小有效长度")
    result.assert_true(cuid.is_valid("a" * 32), "最大有效长度")
    
    # 测试大小写
    upper_id = valid_id.upper()
    result.assert_true(cuid.is_valid(upper_id), "大写应该有效（Base36 不区分大小写）")
    
    return result


def test_uniqueness():
    """测试唯一性"""
    result = TestResult()
    cuid = Cuid2()
    
    # 生成大量 ID 并检查唯一性
    ids = set()
    count = 10000
    
    for _ in range(count):
        new_id = cuid.generate()
        result.assert_false(new_id in ids, f"ID 应该唯一: {new_id}")
        ids.add(new_id)
    
    result.assert_equal(len(ids), count, f"应生成 {count} 个唯一 ID")
    
    return result


def test_batch_generation():
    """测试批量生成"""
    result = TestResult()
    cuid = Cuid2()
    
    # 测试批量生成
    ids = cuid.generate_batch(100)
    result.assert_len(ids, 100, "应生成 100 个 ID")
    
    # 测试所有 ID 唯一
    unique_ids = set(ids)
    result.assert_equal(len(unique_ids), 100, "批量生成的 ID 应全部唯一")
    
    # 测试所有 ID 有效
    for id_val in ids:
        result.assert_true(cuid.is_valid(id_val), f"批量 ID 应有效: {id_val}")
    
    # 测试自定义长度批量生成
    ids_long = cuid.generate_batch(50, length=32)
    for id_val in ids_long:
        result.assert_len(id_val, 32, "批量生成自定义长度")
    
    return result


def test_shortcuts():
    """测试快捷函数"""
    result = TestResult()
    
    # 测试 create_id
    id1 = create_id()
    result.assert_len(id1, 24, "create_id 默认长度")
    
    # 测试 create_id 自定义长度
    id2 = create_id(length=16)
    result.assert_len(id2, 16, "create_id 自定义长度")
    
    # 测试 create_id_batch
    ids = create_id_batch(50)
    result.assert_len(ids, 50, "create_id_batch 数量")
    
    # 测试 is_cuid2
    result.assert_true(is_cuid2(id1), "is_cuid2 应验证有效 ID")
    result.assert_false(is_cuid2("invalid!"), "is_cuid2 应拒绝无效 ID")
    
    return result


def test_fingerprint():
    """测试指纹功能"""
    result = TestResult()
    
    # 测试默认指纹
    cuid1 = Cuid2()
    fp1 = cuid1.fingerprint
    result.assert_true(len(fp1) > 0, "应生成默认指纹")
    
    # 测试相同指纹生成相同值
    cuid2 = Cuid2(fingerprint="test_fingerprint_123")
    cuid3 = Cuid2(fingerprint="test_fingerprint_123")
    result.assert_equal(cuid2.fingerprint, cuid3.fingerprint, "相同指纹应相同")
    
    # 测试自定义指纹
    cuid4 = Cuid2(fingerprint="custom_fp")
    result.assert_equal(cuid4.fingerprint, "custom_fp", "应使用自定义指纹")
    
    return result


def test_thread_safety():
    """测试线程安全"""
    result = TestResult()
    cuid = Cuid2()
    
    ids = []
    lock = threading.Lock()
    
    def generate_ids():
        for _ in range(100):
            new_id = cuid.generate()
            with lock:
                ids.append(new_id)
    
    # 创建多个线程
    threads = []
    for _ in range(10):
        t = threading.Thread(target=generate_ids)
        threads.append(t)
        t.start()
    
    # 等待所有线程完成
    for t in threads:
        t.join()
    
    # 检查唯一性
    unique_ids = set(ids)
    result.assert_equal(len(unique_ids), 1000, "多线程生成的 ID 应全部唯一")
    
    return result


def test_secure_cuid2():
    """测试安全 CUID2"""
    result = TestResult()
    
    # 测试默认长度（32）
    secure = SecureCuid2()
    id1 = secure.generate()
    result.assert_len(id1, 32, "SecureCuid2 默认长度应为 32")
    
    # 测试最小长度强制为 16
    secure_short = SecureCuid2(length=8)
    id2 = secure_short.generate()
    result.assert_len(id2, 16, "SecureCuid2 最小长度应为 16")
    
    # 测试唯一性
    ids = set()
    for _ in range(1000):
        new_id = secure.generate()
        result.assert_false(new_id in ids, "SecureCuid2 应生成唯一 ID")
        ids.add(new_id)
    
    return result


def test_prefixed_cuid2():
    """测试带前缀的 CUID2"""
    result = TestResult()
    
    # 测试生成
    prefixed = PrefixedCuid2(prefix="user")
    id1 = prefixed.generate()
    result.assert_true(id1.startswith("user_"), "应带前缀")
    
    # 测试前缀验证
    result.assert_true(prefixed.is_valid(id1), "应验证有效带前缀 ID")
    result.assert_false(prefixed.is_valid("order_abc123"), "不同前缀应无效")
    result.assert_false(prefixed.is_valid("invalid"), "无下划线应无效")
    
    # 测试提取前缀
    prefix = prefixed.extract_prefix(id1)
    result.assert_equal(prefix, "user", "应提取正确前缀")
    
    # 测试提取 CUID
    cuid_part = prefixed.extract_cuid(id1)
    result.assert_is_not_none(cuid_part, "应能提取 CUID 部分")
    result.assert_true(is_cuid2(cuid_part), "CUID 部分应有效")
    
    # 测试无效前缀
    result.assert_raises(ValueError, lambda: PrefixedCuid2(prefix=""))
    result.assert_raises(ValueError, lambda: PrefixedCuid2(prefix="invalid!"))
    
    # 测试快捷函数
    order_id = create_prefixed_id("order")
    result.assert_true(order_id.startswith("order_"), "快捷函数应生成带前缀 ID")
    
    return result


def test_length_validation():
    """测试长度验证"""
    result = TestResult()
    
    # 测试过短
    result.assert_raises(ValueError, lambda: Cuid2(length=1))
    
    # 测试过长
    result.assert_raises(ValueError, lambda: Cuid2(length=33))
    
    # 测试边界值
    try:
        Cuid2(length=2)
        result.passed += 1
    except ValueError:
        result.failed += 1
        result.errors.append("长度 2 应该有效")
    
    try:
        Cuid2(length=32)
        result.passed += 1
    except ValueError:
        result.failed += 1
        result.errors.append("长度 32 应该有效")
    
    return result


def test_get_info():
    """测试 ID 信息获取"""
    result = TestResult()
    cuid = Cuid2()
    
    id1 = cuid.generate()
    info = cuid.get_info(id1)
    
    result.assert_equal(info["id"], id1, "信息中 ID 应正确")
    result.assert_equal(info["length"], 24, "长度信息应正确")
    result.assert_true(info["valid"], "有效性应正确")
    result.assert_equal(info["format"], "cuid2", "格式应为 cuid2")
    result.assert_equal(info["encoding"], "base36", "编码应为 base36")
    
    return result


def test_character_set():
    """测试字符集"""
    result = TestResult()
    
    # 验证 Base36 字符集
    result.assert_equal(len(BASE36_CHARS), 36, "Base36 应有 36 个字符")
    
    # 验证所有生成的 ID 只使用 Base36 字符
    cuid = Cuid2()
    for _ in range(100):
        id_val = cuid.generate().lower()
        for char in id_val:
            result.assert_in(char, BASE36_CHARS, f"字符 {char} 应在 Base36 中")
    
    return result


def test_edge_cases():
    """测试边界情况"""
    result = TestResult()
    cuid = Cuid2()
    
    # 测试快速连续生成（同一毫秒）
    ids = [cuid.generate() for _ in range(100)]
    unique_ids = set(ids)
    result.assert_equal(len(unique_ids), 100, "同一毫秒内生成的 ID 应唯一")
    
    # 测试批量生成空列表
    empty_batch = cuid.generate_batch(0)
    result.assert_len(empty_batch, 0, "批量生成 0 个应返回空列表")
    
    # 测试非常大的批量
    large_batch = cuid.generate_batch(1000)
    result.assert_len(large_batch, 1000, "大批量生成")
    
    # 验证大批量唯一性
    unique_large = set(large_batch)
    result.assert_equal(len(unique_large), 1000, "大批量应全部唯一")
    
    return result


def test_performance():
    """测试性能"""
    result = TestResult()
    cuid = Cuid2()
    
    # 测试生成 10000 个 ID 的时间
    start_time = time.time()
    ids = cuid.generate_batch(10000)
    elapsed = time.time() - start_time
    
    # 应该在合理时间内完成（每秒至少 10000 个）
    result.assert_true(elapsed < 5.0, f"生成 10000 个 ID 应在 5 秒内完成，实际: {elapsed:.3f}s")
    result.assert_len(ids, 10000, "应生成正确数量")
    
    return result


def test_different_lengths():
    """测试不同长度"""
    result = TestResult()
    
    for length in [2, 4, 8, 12, 16, 20, 24, 28, 32]:
        cuid = Cuid2(length=length)
        id_val = cuid.generate()
        result.assert_len(id_val, length, f"长度 {length} 应正确")
        result.assert_true(cuid.is_valid(id_val), f"长度 {length} 的 ID 应有效")
    
    return result


def test_concurrent_fingerprints():
    """测试不同指纹生成不同 ID"""
    result = TestResult()
    
    cuid1 = Cuid2(fingerprint="fp1")
    cuid2 = Cuid2(fingerprint="fp2")
    
    # 生成 ID
    ids1 = cuid1.generate_batch(100)
    ids2 = cuid2.generate_batch(100)
    
    # 不同指纹应生成不同的 ID
    result.assert_true(set(ids1) != set(ids2), "不同指纹应生成不同 ID")
    
    return result


def test_deterministic_fingerprint():
    """测试确定性指纹"""
    result = TestResult()
    
    # 相同指纹应可重复
    cuid = Cuid2(fingerprint="test_deterministic")
    
    ids1 = cuid.generate_batch(100)
    # 由于时间戳和随机数，ID 会不同，但指纹一致
    result.assert_equal(cuid.fingerprint, "test_deterministic", "指纹应一致")
    
    return result


def test_base62_encoding():
    """测试 Base62 编码表"""
    result = TestResult()
    
    result.assert_equal(len(BASE62_CHARS), 62, "Base62 应有 62 个字符")
    
    # 验证包含数字、大写字母、小写字母
    has_digit = any(c.isdigit() for c in BASE62_CHARS)
    has_upper = any(c.isupper() for c in BASE62_CHARS)
    has_lower = any(c.islower() for c in BASE62_CHARS)
    
    result.assert_true(has_digit, "Base62 应包含数字")
    result.assert_true(has_upper, "Base62 应包含大写字母")
    result.assert_true(has_lower, "Base62 应包含小写字母")
    
    return result


def test_uppercase_validation():
    """测试大写字母验证"""
    result = TestResult()
    cuid = Cuid2()
    
    # 生成 ID 并转为大写
    id1 = cuid.generate()
    id_upper = id1.upper()
    
    # 大写版本应该也是有效的
    result.assert_true(cuid.is_valid(id_upper), "大写 ID 应有效")
    
    return result


def run_all_tests():
    """运行所有测试"""
    tests = [
        ("基本生成", test_basic_generation),
        ("有效性验证", test_validity),
        ("唯一性", test_uniqueness),
        ("批量生成", test_batch_generation),
        ("快捷函数", test_shortcuts),
        ("指纹功能", test_fingerprint),
        ("线程安全", test_thread_safety),
        ("安全 CUID2", test_secure_cuid2),
        ("带前缀 CUID2", test_prefixed_cuid2),
        ("长度验证", test_length_validation),
        ("信息获取", test_get_info),
        ("字符集", test_character_set),
        ("边界情况", test_edge_cases),
        ("性能", test_performance),
        ("不同长度", test_different_lengths),
        ("不同指纹", test_concurrent_fingerprints),
        ("确定性指纹", test_deterministic_fingerprint),
        ("Base62 编码", test_base62_encoding),
        ("大写验证", test_uppercase_validation),
    ]
    
    total_passed = 0
    total_failed = 0
    all_errors = []
    
    print("=" * 60)
    print("CUID2 Utils 测试套件")
    print("=" * 60)
    
    for name, test_func in tests:
        try:
            result = test_func()
            total_passed += result.passed
            total_failed += result.failed
            all_errors.extend(result.errors)
            
            status = "✅" if result.failed == 0 else "❌"
            print(f"{status} {name}: {result.passed} 通过, {result.failed} 失败")
        except Exception as e:
            total_failed += 1
            print(f"❌ {name}: 异常 - {str(e)}")
    
    print("=" * 60)
    print(f"总计: {total_passed} 通过, {total_failed} 失败")
    print("=" * 60)
    
    if all_errors:
        print("\n错误详情:")
        for error in all_errors[:10]:  # 只显示前 10 个错误
            print(f"  - {error}")
        if len(all_errors) > 10:
            print(f"  ... 还有 {len(all_errors) - 10} 个错误")
    
    return total_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)