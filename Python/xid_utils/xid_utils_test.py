"""
XID Utils 单元测试
"""

import time
import threading
from datetime import datetime, timezone
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    XID,
    XIDError,
    XIDGenerator,
    generate,
    from_string,
    from_bytes,
    is_valid,
    extract_timestamp,
    extract_datetime,
    compare,
    batch_generate,
    parse_info,
    min_xid,
    max_xid,
)


def test_basic_generation():
    """测试基本生成"""
    print("测试基本生成...")
    
    # 生成XID
    xid = generate()
    
    # 验证长度
    assert len(xid) == 12, f"XID长度应为12，实际为{len(xid)}"
    
    # 验证字符串表示
    s = str(xid)
    assert len(s) == 20, f"XID字符串长度应为20，实际为{len(s)}"
    
    # 验证字符串只包含有效字符
    valid_chars = set('0123456789ABCDEFGHIJKLMNOPQRSTUV')
    assert all(c in valid_chars for c in s), f"XID包含无效字符: {s}"
    
    print(f"  ✓ 生成的XID: {s}")
    print("  ✓ 基本生成测试通过")


def test_timestamp_extraction():
    """测试时间戳提取"""
    print("测试时间戳提取...")
    
    # 记录生成前的时间
    before = int(time.time())
    xid = generate()
    after = int(time.time())
    
    # 验证时间戳
    ts = extract_timestamp(xid)
    assert before <= ts <= after, f"时间戳{ts}不在预期范围[{before}, {after}]内"
    
    # 验证datetime
    dt = extract_datetime(xid)
    assert dt.year >= 2020, f"日期{dt}似乎不正确"
    
    print(f"  ✓ 时间戳: {ts}")
    print(f"  ✓ 日期时间: {dt.isoformat()}")
    print("  ✓ 时间戳提取测试通过")


def test_parse_info():
    """测试解析信息"""
    print("测试解析信息...")
    
    xid = generate()
    info = parse_info(xid)
    
    # 验证返回的字典
    assert 'string' in info
    assert 'bytes' in info
    assert 'timestamp' in info
    assert 'datetime' in info
    assert 'machine_id' in info
    assert 'process_id' in info
    assert 'counter' in info
    
    print(f"  ✓ 解析信息: {info}")
    print("  ✓ 解析信息测试通过")


def test_from_string():
    """测试从字符串解析"""
    print("测试从字符串解析...")
    
    # 生成XID
    original = generate()
    s = str(original)
    
    # 从字符串解析
    parsed = from_string(s)
    
    # 验证相等
    assert original == parsed, "原始XID和解析后的XID不相等"
    
    # 测试小写
    parsed_lower = from_string(s.lower())
    assert original == parsed_lower, "小写字符串解析失败"
    
    print(f"  ✓ 字符串解析: {s}")
    print("  ✓ 从字符串解析测试通过")


def test_from_bytes():
    """测试从字节创建"""
    print("测试从字节创建...")
    
    # 生成XID
    original = generate()
    b = original.bytes
    
    # 从字节创建
    recreated = from_bytes(b)
    
    # 验证相等
    assert original == recreated, "原始XID和重新创建的XID不相等"
    
    # 测试全零字节
    zero_xid = from_bytes(b'\x00' * 12)
    assert str(zero_xid) == '00000000000000000000'
    
    # 测试全1字节 (Base32Hex编码后末尾有4位填充)
    max_xid = from_bytes(b'\xFF' * 12)
    assert str(max_xid) == 'VVVVVVVVVVVVVVVVVVVG'  # 末尾G是因为96位非5的倍数
    
    print(f"  ✓ 字节创建成功")
    print("  ✓ 从字节创建测试通过")


def test_is_valid():
    """测试验证函数"""
    print("测试验证函数...")
    
    # 有效的XID
    xid = generate()
    assert is_valid(str(xid)), "有效XID验证失败"
    
    # 无效的XID
    assert not is_valid(''), "空字符串应该无效"
    assert not is_valid('short'), "短字符串应该无效"
    assert not is_valid('x' * 20), "包含无效字符的字符串应该无效"
    assert not is_valid('12345'), "长度不足的字符串应该无效"
    assert not is_valid(None), "None应该无效"
    assert not is_valid(123), "数字应该无效"
    
    # 边界情况
    assert is_valid('00000000000000000000'), "全零XID应该有效"
    assert is_valid('VVVVVVVVVVVVVVVVVVVV'), "全V XID应该有效"
    
    print("  ✓ 验证函数测试通过")


def test_comparison():
    """测试比较操作"""
    print("测试比较操作...")
    
    # 生成两个XID（有时间差）
    xid1 = generate()
    time.sleep(0.01)
    xid2 = generate()
    
    # 验证比较
    assert xid1 < xid2, "第一个XID应该小于第二个"
    assert xid2 > xid1, "第二个XID应该大于第一个"
    assert xid1 == xid1, "XID应该等于自己"
    assert xid1 <= xid1, "XID应该小于等于自己"
    assert xid1 >= xid1, "XID应该大于等于自己"
    
    # 测试compare函数
    assert compare(xid1, xid2) == -1
    assert compare(xid2, xid1) == 1
    assert compare(xid1, xid1) == 0
    
    # 测试字符串参数
    assert compare(str(xid1), str(xid2)) == -1
    
    print("  ✓ 比较操作测试通过")


def test_sorting():
    """测试排序"""
    print("测试排序...")
    
    # 生成多个XID（有小延迟）
    xids = []
    for _ in range(20):
        xids.append(generate())
        time.sleep(0.001)  # 小延迟确保时间差异
    
    # 打乱顺序
    import random
    shuffled = xids.copy()
    random.shuffle(shuffled)
    
    # 排序
    sorted_xids = sorted(shuffled)
    
    # 验证排序结果
    assert sorted_xids == xids, "排序后的XID应该按生成顺序排列"
    
    print(f"  ✓ 排序{len(xids)}个XID成功")
    print("  ✓ 排序测试通过")


def test_batch_generation():
    """测试批量生成"""
    print("测试批量生成...")
    
    # 批量生成
    xids = batch_generate(100)
    
    # 验证数量
    assert len(xids) == 100, f"批量生成数量应为100，实际为{len(xids)}"
    
    # 验证唯一性
    strings = [str(x) for x in xids]
    assert len(strings) == len(set(strings)), "批量生成的XID应该唯一"
    
    print(f"  ✓ 批量生成100个XID，全部唯一")
    print("  ✓ 批量生成测试通过")


def test_thread_safety():
    """测试线程安全"""
    print("测试线程安全...")
    
    results = []
    lock = threading.Lock()
    
    def generate_xids():
        for _ in range(100):
            xid = generate()
            with lock:
                results.append(str(xid))
    
    # 创建多个线程
    threads = [threading.Thread(target=generate_xids) for _ in range(10)]
    
    # 启动线程
    for t in threads:
        t.start()
    
    # 等待完成
    for t in threads:
        t.join()
    
    # 验证结果
    assert len(results) == 1000, f"应生成1000个XID，实际为{len(results)}"
    
    # 验证唯一性
    unique = len(set(results))
    assert unique == 1000, f"所有XID应唯一，实际有{1000 - unique}个重复"
    
    print(f"  ✓ 10个线程各生成100个XID，共{len(results)}个，全部唯一")
    print("  ✓ 线程安全测试通过")


def test_min_max_xid():
    """测试最小/最大XID"""
    print("测试最小/最大XID...")
    
    ts = 1609459200  # 2021-01-01 00:00:00 UTC
    
    # 创建最小XID
    min_xid_obj = min_xid(ts)
    assert min_xid_obj.timestamp == ts
    
    # 创建最大XID
    max_xid_obj = max_xid(ts)
    assert max_xid_obj.timestamp == ts
    
    # 验证最小 < 最大
    assert min_xid_obj < max_xid_obj
    
    # 验证机器ID和进程ID
    assert min_xid_obj.machine_id == b'\x00\x00\x00'
    assert min_xid_obj.process_id == 0
    assert max_xid_obj.machine_id == b'\xFF\xFF\xFF'
    assert max_xid_obj.process_id == 0xFFFF
    
    print(f"  ✓ 最小XID: {min_xid_obj}")
    print(f"  ✓ 最大XID: {max_xid_obj}")
    print("  ✓ 最小/最大XID测试通过")


def test_xid_generator():
    """测试自定义生成器"""
    print("测试自定义生成器...")
    
    # 创建自定义生成器
    machine_id = b'\xAB\xCD\xEF'
    process_id = 12345
    
    generator = XIDGenerator(machine_id=machine_id, process_id=process_id)
    
    # 生成XID
    xid = generator.generate()
    
    # 验证机器ID和进程ID
    assert xid.machine_id == machine_id, f"机器ID不匹配"
    assert xid.process_id == process_id, f"进程ID不匹配"
    
    # 测试错误情况
    try:
        XIDGenerator(machine_id=b'\x00\x00')  # 错误长度
        assert False, "应该抛出异常"
    except XIDError:
        pass
    
    try:
        XIDGenerator(process_id=70000)  # 超出范围
        assert False, "应该抛出异常"
    except XIDError:
        pass
    
    print(f"  ✓ 自定义机器ID: {machine_id.hex()}")
    print(f"  ✓ 自定义进程ID: {process_id}")
    print("  ✓ 自定义生成器测试通过")


def test_properties():
    """测试XID属性"""
    print("测试XID属性...")
    
    xid = generate()
    
    # 测试bytes属性
    b = xid.bytes
    assert isinstance(b, bytes) and len(b) == 12
    
    # 测试timestamp属性
    ts = xid.timestamp
    assert isinstance(ts, int) and ts > 0
    
    # 测试datetime属性
    dt = xid.datetime
    assert isinstance(dt, datetime)
    assert dt.tzinfo is not None  # 应该有timezone信息
    
    # 测试machine_id属性
    mid = xid.machine_id
    assert isinstance(mid, bytes) and len(mid) == 3
    
    # 测试process_id属性
    pid = xid.process_id
    assert isinstance(pid, int) and 0 <= pid <= 0xFFFF
    
    # 测试counter属性
    counter = xid.counter
    assert isinstance(counter, int) and 0 <= counter <= 0xFFFFFF
    
    print(f"  ✓ 时间戳: {ts}")
    print(f"  ✓ 日期时间: {dt.isoformat()}")
    print(f"  ✓ 机器ID: {mid.hex()}")
    print(f"  ✓ 进程ID: {pid}")
    print(f"  ✓ 计数器: {counter}")
    print("  ✓ 属性测试通过")


def test_hashable():
    """测试可哈希性"""
    print("测试可哈希性...")
    
    xid1 = generate()
    xid2 = generate()
    
    # 测试hash
    assert isinstance(hash(xid1), int)
    
    # 测试用作字典键
    d = {xid1: "first", xid2: "second"}
    assert d[xid1] == "first"
    assert d[xid2] == "second"
    
    # 测试用作集合元素
    s = {xid1, xid2, xid1}
    assert len(s) == 2
    
    print("  ✓ 可哈希性测试通过")


def test_repr():
    """测试字符串表示"""
    print("测试字符串表示...")
    
    xid = generate()
    
    # 测试__str__
    s = str(xid)
    assert len(s) == 20
    
    # 测试__repr__
    r = repr(xid)
    assert r.startswith("XID('") and r.endswith("')")
    
    # 测试__bytes__
    b = bytes(xid)
    assert len(b) == 12
    
    print(f"  ✓ str: {s}")
    print(f"  ✓ repr: {r}")
    print("  ✓ 字符串表示测试通过")


def test_error_handling():
    """测试错误处理"""
    print("测试错误处理...")
    
    # 无效字节长度
    try:
        from_bytes(b'\x00' * 11)
        assert False, "应该抛出XIDError"
    except XIDError as e:
        assert "12 bytes" in str(e)
    
    # 无效字符串长度
    try:
        from_string("short")
        assert False, "应该抛出XIDError"
    except XIDError as e:
        assert "20 characters" in str(e)
    
    # 无效字符
    try:
        from_string("0" * 19 + "!")  # ! 不是有效字符
        assert False, "应该抛出XIDError"
    except XIDError as e:
        assert "Invalid character" in str(e)
    
    # 无效类型
    try:
        XID(12345)  # 数字类型无效
        assert False, "应该抛出XIDError"
    except XIDError as e:
        assert "Invalid XID value type" in str(e)
    
    print("  ✓ 所有错误情况正确处理")
    print("  ✓ 错误处理测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("XID Utils 测试套件")
    print("=" * 60)
    print()
    
    tests = [
        test_basic_generation,
        test_timestamp_extraction,
        test_parse_info,
        test_from_string,
        test_from_bytes,
        test_is_valid,
        test_comparison,
        test_sorting,
        test_batch_generation,
        test_thread_safety,
        test_min_max_xid,
        test_xid_generator,
        test_properties,
        test_hashable,
        test_repr,
        test_error_handling,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
            print()
        except Exception as e:
            failed += 1
            print(f"  ✗ 测试失败: {e}")
            print()
    
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)