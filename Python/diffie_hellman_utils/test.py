#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Diffie-Hellman 工具模块测试

测试覆盖:
- 密钥生成
- 公钥计算
- 共享密钥计算
- 密钥派生
- 密钥交换验证
- 边界条件处理
- 安全性验证
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from diffie_hellman_utils.mod import (
    DiffieHellman,
    ECDHKey,
    create_dh_pair,
    perform_key_exchange
)


def test_basic_key_exchange():
    """测试基本密钥交换"""
    print("测试 1: 基本密钥交换")
    
    # Alice 和 Bob 各自创建实例
    alice = DiffieHellman(key_bits=2048)
    bob = DiffieHellman(key_bits=2048)
    
    # 生成密钥对
    alice_private = alice.generate_private_key()
    alice_public = alice.generate_public_key()
    
    bob_private = bob.generate_private_key()
    bob_public = bob.generate_public_key()
    
    # 验证密钥已生成
    assert alice_private is not None
    assert alice_public is not None
    assert bob_private is not None
    assert bob_public is not None
    
    # 计算共享密钥
    alice_shared = alice.compute_shared_key(bob_public)
    bob_shared = bob.compute_shared_key(alice_public)
    
    # 验证双方共享密钥相同
    assert alice_shared == bob_shared
    assert DiffieHellman.verify_key_exchange(alice_shared, bob_shared)
    
    print("  ✓ 基本密钥交换成功")


def test_different_key_sizes():
    """测试不同密钥长度"""
    print("\n测试 2: 不同密钥长度")
    
    for bits in [256, 1024, 2048]:
        alice = DiffieHellman(key_bits=bits)
        bob = DiffieHellman(key_bits=bits)
        
        alice.generate_private_key()
        alice_public = alice.generate_public_key()
        
        bob.generate_private_key()
        bob_public = bob.generate_public_key()
        
        alice_shared = alice.compute_shared_key(bob_public)
        bob_shared = bob.compute_shared_key(alice_public)
        
        assert alice_shared == bob_shared, f"{bits}位密钥交换失败"
        print(f"  ✓ {bits}位密钥交换成功")


def test_key_derivation():
    """测试密钥派生"""
    print("\n测试 3: 密钥派生")
    
    dh = DiffieHellman(key_bits=2048)
    dh.generate_private_key()
    dh.generate_public_key()
    
    # 模拟共享密钥
    shared_key = dh.compute_shared_key(secrets.randbelow(dh.prime - 2) + 2)
    
    # 派生不同长度的密钥
    for length in [16, 24, 32, 64]:
        derived = dh.derive_key(key_length=length)
        assert len(derived) == length, f"派生密钥长度错误: {len(derived)} != {length}"
        print(f"  ✓ 派生 {length} 字节密钥: {derived.hex()[:16]}...")


def test_export_import():
    """测试公钥导入导出"""
    print("\n测试 4: 公钥导入导出")
    
    dh = DiffieHellman(key_bits=2048)
    dh.generate_private_key()
    original_public = dh.generate_public_key()
    
    # 导出
    exported = dh.export_public_key()
    assert exported.startswith(hex(original_public)[2:][:10])
    
    # 导入
    imported = dh.import_public_key(exported)
    assert imported == original_public
    
    print(f"  ✓ 公钥导出成功 (长度: {len(exported)})")
    print(f"  ✓ 公钥导入成功，验证通过")


def test_clear_sensitive_data():
    """测试敏感数据清除"""
    print("\n测试 5: 敏感数据清除")
    
    dh = DiffieHellman(key_bits=2048)
    dh.generate_private_key()
    dh.generate_public_key()
    
    # 清除前验证数据存在
    assert dh._private_key is not None
    assert dh._public_key is not None
    
    # 清除
    dh.clear_sensitive_data()
    
    # 清除后验证数据为空
    assert dh._private_key is None
    assert dh._shared_key is None
    
    print("  ✓ 敏感数据已清除")


def test_invalid_inputs():
    """测试无效输入处理"""
    print("\n测试 6: 无效输入处理")
    
    dh = DiffieHellman(key_bits=2048)
    
    # 没有私钥时生成公钥
    try:
        dh.generate_public_key()
        assert False, "应该抛出异常"
    except ValueError as e:
        print(f"  ✓ 正确抛出异常: {e}")
    
    # 没有私钥时计算共享密钥
    try:
        dh.compute_shared_key(123)
        assert False, "应该抛出异常"
    except ValueError as e:
        print(f"  ✓ 正确抛出异常: {e}")
    
    # 生成私钥
    dh.generate_private_key()
    
    # 无效的对方公钥
    try:
        dh.compute_shared_key(0)  # 太小
        assert False, "应该抛出异常"
    except ValueError as e:
        print(f"  ✓ 正确抛出异常: 无效公钥（太小）")
    
    try:
        dh.compute_shared_key(dh.prime)  # 太大
        assert False, "应该抛出异常"
    except ValueError as e:
        print(f"  ✓ 正确抛出异常: 无效公钥（太大）")


def test_convenience_functions():
    """测试便捷函数"""
    print("\n测试 7: 便捷函数")
    
    # create_dh_pair
    dh1, priv1, pub1 = create_dh_pair(key_bits=1024)
    assert priv1 is not None
    assert pub1 is not None
    print("  ✓ create_dh_pair 工作正常")
    
    # perform_key_exchange
    dh2, priv2, pub2 = create_dh_pair(key_bits=1024)
    shared1, shared2 = perform_key_exchange(dh1, dh2)
    assert shared1 == shared2
    print("  ✓ perform_key_exchange 工作正常")


def test_multiple_exchanges():
    """测试多次密钥交换"""
    print("\n测试 8: 多次密钥交换（不同参与方）")
    
    # Alice 与多个参与方交换
    alice = DiffieHellman(key_bits=2048)
    alice.generate_private_key()
    alice_public = alice.generate_public_key()
    
    for i in range(3):
        other = DiffieHellman(key_bits=2048)
        other.generate_private_key()
        other_public = other.generate_public_key()
        
        alice_shared = alice.compute_shared_key(other_public)
        other_shared = other.compute_shared_key(alice_public)
        
        assert alice_shared == other_shared
        print(f"  ✓ 与参与方 {i+1} 密钥交换成功")


def test_reproducibility():
    """测试可重复性（使用相同私钥）"""
    print("\n测试 9: 可重复性测试")
    
    # 使用相同的私钥应产生相同的公钥
    dh1 = DiffieHellman(key_bits=2048)
    dh2 = DiffieHellman(key_bits=2048)
    
    private_key = secrets.randbelow(dh1.prime - 2) + 1
    
    pub1 = dh1.generate_public_key(private_key)
    pub2 = dh2.generate_public_key(private_key)
    
    assert pub1 == pub2
    print("  ✓ 相同私钥产生相同公钥")
    
    # 使用相同的对方公钥应产生相同的共享密钥
    dh3 = DiffieHellman(key_bits=2048)
    dh3.generate_private_key()
    other_pub = dh3.generate_public_key()
    
    shared1 = dh1.compute_shared_key(other_pub)
    shared2 = dh2.compute_shared_key(other_pub)
    
    assert shared1 == shared2
    print("  ✓ 相同条件产生相同共享密钥")


def test_ecdh_basic():
    """测试简化 ECDH 实现"""
    print("\n测试 10: 简化 ECDH 实现")
    
    alice = ECDHKey()
    bob = ECDHKey()
    
    alice_priv = alice.generate_private_key()
    alice_pub = alice.generate_public_key()
    
    bob_priv = bob.generate_private_key()
    bob_pub = bob.generate_public_key()
    
    alice_shared = alice.compute_shared_key(bob_pub)
    bob_shared = bob.compute_shared_key(alice_pub)
    
    assert alice_shared == bob_shared
    print("  ✓ 简化 ECDH 密钥交换成功")
    
    # 派生密钥
    key = alice.derive_key(32)
    assert len(key) == 32
    print(f"  ✓ ECDH 派生密钥: {key.hex()[:16]}...")


def test_performance():
    """测试性能"""
    print("\n测试 11: 性能测试")
    import time
    
    # 256 位快速测试
    start = time.time()
    for _ in range(100):
        dh = DiffieHellman(key_bits=256)
        dh.generate_private_key()
        dh.generate_public_key()
    elapsed = time.time() - start
    print(f"  256位: 100次密钥生成耗时 {elapsed:.3f}秒")
    
    # 1024 位
    start = time.time()
    for _ in range(50):
        dh = DiffieHellman(key_bits=1024)
        dh.generate_private_key()
        dh.generate_public_key()
    elapsed = time.time() - start
    print(f"  1024位: 50次密钥生成耗时 {elapsed:.3f}秒")
    
    # 2048 位（只测少量）
    start = time.time()
    for _ in range(10):
        dh = DiffieHellman(key_bits=2048)
        dh.generate_private_key()
        dh.generate_public_key()
    elapsed = time.time() - start
    print(f"  2048位: 10次密钥生成耗时 {elapsed:.3f}秒")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Diffie-Hellman 工具模块测试")
    print("=" * 50)
    
    # 导入 secrets 模块
    global secrets
    import secrets
    
    tests = [
        test_basic_key_exchange,
        test_different_key_sizes,
        test_key_derivation,
        test_export_import,
        test_clear_sensitive_data,
        test_invalid_inputs,
        test_convenience_functions,
        test_multiple_exchanges,
        test_reproducibility,
        test_ecdh_basic,
        test_performance,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ 测试失败: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)