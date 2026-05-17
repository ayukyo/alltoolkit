#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diffie-Hellman Utils Test - Diffie-Hellman 密钥交换测试

测试模块：diffie_hellman_utils
测试用例数：30+
测试覆盖：密钥生成、密钥交换、密钥派生、验证、ECDH、便捷函数
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    DiffieHellman, ECDHKey,
    create_dh_pair, perform_key_exchange
)


def test_result_collector():
    """测试结果收集器"""
    results = []
    
    def add_result(test_name: str, passed: bool, message: str = ""):
        results.append({
            "name": test_name,
            "passed": passed,
            "message": message
        })
    
    return results, add_result


def test_key_generation(results, add_result):
    """测试密钥生成"""
    # test 1: 默认 2048 位密钥
    dh = DiffieHellman()
    private = dh.generate_private_key()
    add_result("generate_private_key default", private > 0 and private < dh.prime)
    
    # test 2: 公钥生成
    public = dh.generate_public_key()
    add_result("generate_public_key", public > 0 and public < dh.prime)
    
    # test 3: 使用私钥生成公钥
    dh2 = DiffieHellman()
    dh2.generate_public_key(private_key=12345)
    add_result("generate_public_key with private", dh2.get_private_key() == 12345)
    
    # test 4: 无私钥时公钥异常
    dh3 = DiffieHellman()
    try:
        dh3.generate_public_key()
        add_result("generate_public_key no private exception", False, "Should raise ValueError")
    except ValueError:
        add_result("generate_public_key no private exception", True)
    
    # test 5: 1024 位密钥
    dh1024 = DiffieHellman(key_bits=1024)
    private = dh1024.generate_private_key()
    public = dh1024.generate_public_key()
    add_result("DiffieHellman 1024 bit", 
               dh1024.key_bits == 1024 and private > 0 and public > 0)
    
    # test 6: 256 位密钥（仅测试用途）
    dh256 = DiffieHellman(key_bits=256)
    private = dh256.generate_private_key()
    public = dh256.generate_public_key()
    add_result("DiffieHellman 256 bit", 
               dh256.key_bits == 256 and private > 0 and public > 0)


def test_key_exchange(results, add_result):
    """测试密钥交换"""
    # test 7: 基础密钥交换
    alice = DiffieHellman()
    alice_private = alice.generate_private_key()
    alice_public = alice.generate_public_key()
    
    bob = DiffieHellman()
    bob_private = bob.generate_private_key()
    bob_public = bob.generate_public_key()
    
    alice_shared = alice.compute_shared_key(bob_public)
    bob_shared = bob.compute_shared_key(alice_public)
    
    add_result("key_exchange basic", alice_shared == bob_shared, 
               f"Shared keys should match: {alice_shared == bob_shared}")
    
    # test 8: 验证函数
    verified = DiffieHellman.verify_key_exchange(alice_shared, bob_shared)
    add_result("verify_key_exchange", verified, f"Verification should pass")
    
    # test 9: 无私钥时共享密钥异常
    dh = DiffieHellman()
    other_public = 12345
    try:
        dh.compute_shared_key(other_public)
        add_result("compute_shared_key no private exception", False, "Should raise ValueError")
    except ValueError:
        add_result("compute_shared_key no private exception", True)
    
    # test 10: 无效公钥异常
    dh = DiffieHellman()
    dh.generate_private_key()
    try:
        dh.compute_shared_key(0)  # 无效公钥
        add_result("compute_shared_key invalid public exception", False, "Should raise ValueError")
    except ValueError:
        add_result("compute_shared_key invalid public exception", True)
    
    try:
        dh.compute_shared_key(dh.prime)  # 超出范围的公钥
        add_result("compute_shared_key out of range exception", False, "Should raise ValueError")
    except ValueError:
        add_result("compute_shared_key out of range exception", True)


def test_key_derivation(results, add_result):
    """测试密钥派生"""
    alice = DiffieHellman()
    alice.generate_private_key()
    alice.generate_public_key()
    
    bob = DiffieHellman()
    bob.generate_private_key()
    bob.generate_public_key()
    
    alice_shared = alice.compute_shared_key(bob.get_public_key())
    
    # test 11: 派生密钥默认长度
    key = alice.derive_key()
    add_result("derive_key default", len(key) == 32, f"Expected 32 bytes, got {len(key)}")
    
    # test 12: 自定义密钥长度
    key16 = alice.derive_key(key_length=16)
    add_result("derive_key custom length", len(key16) == 16, f"Expected 16 bytes, got {len(key16)}")
    
    # test 13: 自定义哈希算法
    key = alice.derive_key(hash_algorithm="sha512")
    add_result("derive_key sha512", len(key) == 32, f"Should still return requested length")
    
    # test 14: 无共享密钥时派生异常
    dh = DiffieHellman()
    dh.generate_private_key()
    dh.generate_public_key()
    try:
        dh.derive_key()
        add_result("derive_key no shared exception", False, "Should raise ValueError")
    except ValueError:
        add_result("derive_key no shared exception", True)


def test_import_export(results, add_result):
    """测试公钥导入导出"""
    dh = DiffieHellman()
    dh.generate_private_key()
    dh.generate_public_key()
    
    # test 15: 导出公钥
    exported = dh.export_public_key()
    add_result("export_public_key", len(exported) > 0 and exported.startswith(dh.export_public_key()[:10]))
    
    # test 16: 导入公钥
    imported = dh.import_public_key(exported)
    add_result("import_public_key", imported == dh.get_public_key(), 
               f"Imported should match original")
    
    # test 17: 无公钥时导出异常
    dh2 = DiffieHellman()
    try:
        dh2.export_public_key()
        add_result("export_public_key no key exception", False, "Should raise ValueError")
    except ValueError:
        add_result("export_public_key no key exception", True)


def test_clear_sensitive(results, add_result):
    """测试清除敏感数据"""
    dh = DiffieHellman()
    dh.generate_private_key()
    dh.generate_public_key()
    
    bob = DiffieHellman()
    bob.generate_private_key()
    bob.generate_public_key()
    
    dh.compute_shared_key(bob.get_public_key())
    
    # test 18: 清除敏感数据
    dh.clear_sensitive_data()
    add_result("clear_sensitive_data", 
               dh.get_private_key() is None and dh.get_shared_key() is None, 
               f"Private and shared should be cleared")


def test_eckey(results, add_result):
    """测试 ECDH 简化实现"""
    ecdh = ECDHKey()
    
    # test 19: 生成私钥
    private = ecdh.generate_private_key()
    add_result("ECDHKey generate_private_key", private > 0)
    
    # test 20: 生成公钥
    public = ecdh.generate_public_key()
    add_result("ECDHKey generate_public_key", public > 0 and public < ecdh.PRIME)
    
    # test 21: 共享密钥
    ecdh2 = ECDHKey()
    ecdh2.generate_private_key()
    pub2 = ecdh2.generate_public_key()
    
    shared1 = ecdh.compute_shared_key(pub2)
    shared2 = ecdh2.compute_shared_key(ecdh._public_key)
    
    add_result("ECDHKey shared key", shared1 == shared2, f"Shared keys should match")
    
    # test 22: 派生密钥
    key = ecdh.derive_key()
    add_result("ECDHKey derive_key", len(key) == 32, f"Expected 32 bytes")


def test_convenience_functions(results, add_result):
    """测试便捷函数"""
    # test 23: create_dh_pair
    dh, private, public = create_dh_pair(key_bits=1024)
    add_result("create_dh_pair", 
               dh is not None and private > 0 and public > 0, 
               f"Should return valid pair")
    
    # test 24: perform_key_exchange
    alice, priv1, pub1 = create_dh_pair(key_bits=256)
    bob, priv2, pub2 = create_dh_pair(key_bits=256)
    
    shared1, shared2 = perform_key_exchange(alice, bob)
    add_result("perform_key_exchange", shared1 == shared2, f"Shared keys should match")
    
    # test 25: 无公钥时交换异常
    alice2 = DiffieHellman(key_bits=256)
    alice2.generate_private_key()  # 没有生成公钥
    bob2, _, _ = create_dh_pair(key_bits=256)
    
    try:
        perform_key_exchange(alice2, bob2)
        add_result("perform_key_exchange no public exception", False, "Should raise ValueError")
    except ValueError:
        add_result("perform_key_exchange no public exception", True)


def test_repr(results, add_result):
    """测试对象表示"""
    dh = DiffieHellman()
    
    # test 26: 未初始化时 repr
    repr_str = repr(dh)
    add_result("repr uninitialized", 
               "has_private=False" in repr_str and "has_public=False" in repr_str)
    
    # test 27: 已初始化时 repr
    dh.generate_private_key()
    dh.generate_public_key()
    repr_str = repr(dh)
    add_result("repr initialized", 
               "has_private=True" in repr_str and "has_public=True" in repr_str)


def test_custom_params(results, add_result):
    """测试自定义参数"""
    # test 28: 自定义素数和生成元
    small_prime = 23  # 小素数用于测试
    small_generator = 5
    dh = DiffieHellman(prime=small_prime, generator=small_generator)
    
    private = dh.generate_private_key()
    public = dh.generate_public_key()
    
    add_result("DiffieHellman custom params", 
               dh.prime == small_prime and dh.generator == small_generator and 
               0 < private < small_prime and 0 < public < small_prime)
    
    # test 29: 自定义参数的密钥交换
    dh2 = DiffieHellman(prime=small_prime, generator=small_generator)
    dh2.generate_private_key()
    dh2.generate_public_key()
    
    shared1 = dh.compute_shared_key(dh2.get_public_key())
    shared2 = dh2.compute_shared_key(dh.get_public_key())
    
    add_result("custom params key exchange", shared1 == shared2)


def test_multiple_exchanges(results, add_result):
    """测试多次密钥交换"""
    alice = DiffieHellman()
    alice.generate_private_key()
    alice.generate_public_key()
    
    # test 30: 与多个参与者交换
    bobs_publics = []
    bobs_shareds = []
    
    for i in range(3):
        bob = DiffieHellman()
        bob.generate_private_key()
        bob.generate_public_key()
        bobs_publics.append(bob.get_public_key())
        bobs_shareds.append(bob.compute_shared_key(alice.get_public_key()))
    
    # Alice 与每个 Bob 计算共享密钥
    alice_shareds = [alice.compute_shared_key(pub) for pub in bobs_publics]
    
    add_result("multiple exchanges", 
               all(a == b for a, b in zip(alice_shareds, bobs_shareds)),
               f"All shared keys should match")


def main():
    """运行所有测试"""
    results, add_result = test_result_collector()
    
    # 运行各测试组
    test_key_generation(results, add_result)
    test_key_exchange(results, add_result)
    test_key_derivation(results, add_result)
    test_import_export(results, add_result)
    test_clear_sensitive(results, add_result)
    test_eckey(results, add_result)
    test_convenience_functions(results, add_result)
    test_repr(results, add_result)
    test_custom_params(results, add_result)
    test_multiple_exchanges(results, add_result)
    
    # 输出结果
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    
    print("=" * 60)
    print("Diffie-Hellman Utils Test Results")
    print("=" * 60)
    
    for r in results:
        status = "✅" if r["passed"] else "❌"
        print(f"{status} {r['name']}: {r['message']}")
    
    print("-" * 60)
    print(f"Summary: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=" * 60)
    
    return passed, total


if __name__ == "__main__":
    passed, total = main()
    sys.exit(0 if passed == total else 1)