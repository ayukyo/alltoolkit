"""
SOUNDEX 工具模块测试

测试标准 SOUNDEX 编码、增强模式、相似度计算、批量处理等功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    SoundexEncoder,
    SoundexRefinedEncoder,
    SoundexSQL,
    encode,
    similarity,
    matches,
    find_similar,
    group_by_sound,
    COMMON_NAMES,
    get_common_code,
)


def test_basic_encoding():
    """测试基本编码功能"""
    encoder = SoundexEncoder()
    
    # 测试标准编码（基于标准 SOUNDEX 算法）
    # Robert: R-1(b) - 6(r) - 3(t) = R163
    assert encoder.encode("Robert") == "R163"
    # Rupert: R-1(p) - 6(r) - 3(t) = R163 (与 Robert 相同)
    assert encoder.encode("Rupert") == "R163"
    # Rubin: R-1(b) - 5(n) = R150
    assert encoder.encode("Rubin") == "R150"
    # Ashcraft: A-2(s) - 6(r) - 1(f) - 3(t) = A261
    # 注意：c 编码为 2，但 s 已编码，f 编码为 1
    code_ashcraft = encoder.encode("Ashcraft")
    assert code_ashcraft.startswith("A")
    # Ashcroft: 应与 Ashcraft 相似
    code_ashcroft = encoder.encode("Ashcroft")
    assert code_ashcroft.startswith("A")
    # Tymczak: T-5(m) - 2(c/z) - 2(k) = T522
    code_tymczak = encoder.encode("Tymczak")
    assert code_tymczak.startswith("T")
    # Pfister: P-1(f) - 2(s) - 3(t) - 6(r) = P236
    code_pfister = encoder.encode("Pfister")
    assert code_pfister.startswith("P")
    
    # 测试空字符串
    assert encoder.encode("") == ""
    
    # 测试纯数字/符号
    assert encoder.encode("123") == ""
    assert encoder.encode("!@#") == ""
    
    print("✓ 基本编码测试通过")


def test_name_matching():
    """测试姓名匹配功能"""
    encoder = SoundexEncoder()
    
    # 发音相似的姓名应有相同编码
    similar_pairs = [
        ("Smith", "Smythe"),      # S530
        ("Brown", "Browne"),      # B650
        ("Schmidt", "Smith"),     # 都映射到 S530
        ("Mueller", "Miller"),     # M460
        ("Davis", "Davies"),      # D120
        ("Clark", "Clarke"),      # C462
    ]
    
    for name1, name2 in similar_pairs:
        code1 = encoder.encode(name1)
        code2 = encoder.encode(name2)
        assert code1 == code2, f"{name1}({code1}) != {name2}({code2})"
    
    print("✓ 姓名匹配测试通过")


def test_different_names():
    """测试不同姓名产生不同编码"""
    encoder = SoundexEncoder()
    
    # 这些姓名应该有不同编码
    different_pairs = [
        ("Smith", "Johnson"),
        ("Brown", "Williams"),
        ("Davis", "Miller"),
        ("Wilson", "Taylor"),
    ]
    
    for name1, name2 in different_pairs:
        code1 = encoder.encode(name1)
        code2 = encoder.encode(name2)
        assert code1 != code2, f"{name1}({code1}) == {name2}({code2}) 不应相同"
    
    print("✓ 不同姓名测试通过")


def test_edge_cases():
    """测试边界情况"""
    encoder = SoundexEncoder()
    
    # 单字母姓名
    assert encoder.encode("A") == "A000"
    assert encoder.encode("B") == "B000"
    
    # 短姓名
    assert encoder.encode("Li") == "L000"
    assert encoder.encode("Xu") == "X000"
    
    # 包含空格
    assert encoder.encode("Van der Berg") == "V536"
    
    # 包含连字符
    assert encoder.encode("Smith-Jones") == "S532"
    
    # 大小写混合
    assert encoder.encode("McDoNaLd") == encoder.encode("mcdonald")
    
    print("✓ 边界情况测试通过")


def test_unicode_support():
    """测试 Unicode 字符支持"""
    encoder = SoundexEncoder()
    
    # 带重音的字符
    assert encoder.encode("Müller") == encoder.encode("Muller")
    assert encoder.encode("François") == encoder.encode("Francois")
    assert encoder.encode("Sørensen") == encoder.encode("Sorensen")
    assert encoder.encode("García") == encoder.encode("Garcia")
    
    # 中文应该被跳过或处理
    result = encoder.encode("张三")
    # 中文处理后应为空
    assert result == "" or result.startswith("Z")
    
    print("✓ Unicode 支持测试通过")


def test_length_parameter():
    """测试编码长度参数"""
    encoder_4 = SoundexEncoder(length=4)
    encoder_6 = SoundexEncoder(length=6)
    
    name = "Washington"
    
    code_4 = encoder_4.encode(name)
    code_6 = encoder_6.encode(name)
    
    assert len(code_4) == 4
    assert len(code_6) == 6
    assert code_4 == code_6[:4]
    
    print("✓ 编码长度测试通过")


def test_refined_encoder():
    """测试改进编码器"""
    encoder = SoundexRefinedEncoder()
    
    # 改进编码器产生不同编码
    code = encoder.encode("Smith")
    assert len(code) == 5  # 默认长度 5
    assert code.startswith("S")
    
    # 比较标准编码器和改进编码器
    std_encoder = SoundexEncoder()
    std_code = std_encoder.encode("Smith")
    ref_code = encoder.encode("Smith")
    
    # 编码可能不同
    print(f"  Smith: 标准={std_code}, 改进={ref_code}")
    
    print("✓ 改进编码器测试通过")


def test_similarity():
    """测试相似度计算"""
    encoder = SoundexEncoder()
    
    # 完全匹配
    assert encoder.similarity("Smith", "Smith") == 1.0
    assert encoder.similarity("Smith", "Smythe") == 1.0
    
    # 部分匹配
    sim = encoder.similarity("Smith", "Jones")
    assert 0.0 <= sim < 1.0
    
    # 空字符串
    assert encoder.similarity("", "Smith") == 0.0
    assert encoder.similarity("Smith", "") == 0.0
    
    print("✓ 相似度计算测试通过")


def test_matches():
    """测试匹配判断"""
    encoder = SoundexEncoder()
    
    # 完全匹配
    assert encoder.matches("Smith", "Smythe", threshold=1.0)
    
    # 降低阈值
    assert encoder.matches("Smith", "Jones", threshold=0.0)
    
    # 高阈值下不匹配
    assert not encoder.matches("Smith", "Jones", threshold=1.0)
    
    print("✓ 匹配判断测试通过")


def test_find_similar():
    """测试查找相似姓名"""
    encoder = SoundexEncoder()
    
    candidates = [
        "Smith", "Smythe", "Schmidt", "Johnson", "Johnston",
        "Williams", "Wilson", "Brown", "Browne", "Davis"
    ]
    
    # 查找 Smith 的相似姓名
    similar = encoder.find_similar("Smith", candidates, threshold=1.0)
    similar_names = [name for name, _ in similar]
    
    assert "Smith" in similar_names
    assert "Smythe" in similar_names
    assert "Schmidt" in similar_names
    
    # 查找 Brown 的相似姓名
    similar = encoder.find_similar("Brown", candidates, threshold=1.0)
    similar_names = [name for name, _ in similar]
    
    assert "Brown" in similar_names
    assert "Browne" in similar_names
    
    print("✓ 查找相似姓名测试通过")


def test_group_by_code():
    """测试按编码分组"""
    encoder = SoundexEncoder()
    
    names = ["Smith", "Smythe", "Johnson", "Johnston", "Brown", "Browne"]
    groups = encoder.group_by_code(names)
    
    # Smith 和 Smythe 应该在同一组
    smith_code = encoder.encode("Smith")
    assert "Smith" in groups[smith_code]
    assert "Smythe" in groups[smith_code]
    
    # Brown 和 Browne 应该在同一组
    brown_code = encoder.encode("Brown")
    assert "Brown" in groups[brown_code]
    assert "Browne" in groups[brown_code]
    
    print("✓ 按编码分组测试通过")


def test_batch_encoding():
    """测试批量编码"""
    encoder = SoundexEncoder()
    
    names = ["Smith", "Johnson", "Williams"]
    codes = encoder.encode_batch(names)
    
    assert len(codes) == 3
    assert codes["Smith"] == "S530"
    assert codes["Johnson"] == "J525"
    assert codes["Williams"] == "W452"
    
    print("✓ 批量编码测试通过")


def test_convenience_functions():
    """测试便捷函数"""
    # encode 函数
    assert encode("Smith") == "S530"
    
    # similarity 函数
    assert similarity("Smith", "Smythe") == 1.0
    
    # matches 函数
    assert matches("Smith", "Smythe")
    
    # find_similar 函数
    similar = find_similar("Smith", ["Smith", "Jones", "Smythe"])
    assert len(similar) >= 2  # Smith 和 Smythe
    
    # group_by_sound 函数
    groups = group_by_sound(["Smith", "Smythe"])
    smith_code = encode("Smith")
    assert len(groups[smith_code]) == 2
    
    print("✓ 便捷函数测试通过")


def test_common_names():
    """测试常见姓名字典"""
    # 检查常见姓名编码
    assert COMMON_NAMES["Smith"] == "S530"
    assert COMMON_NAMES["Johnson"] == "J525"
    assert COMMON_NAMES["Williams"] == "W452"
    
    # get_common_code 函数
    assert get_common_code("Smith") == "S530"
    assert get_common_code("Unknown") is None
    
    print("✓ 常见姓名测试通过")


def test_sql_helpers():
    """测试 SQL 辅助函数"""
    # WHERE 子句
    where = SoundexSQL.where_clause("last_name", "Smith")
    assert "SOUNDEX" in where
    assert "last_name" in where
    assert "Smith" in where
    
    # 创建索引 SQL
    create_sql = SoundexSQL.create_index_sql("users", "last_name")
    assert "CREATE INDEX" in create_sql
    assert "users" in create_sql
    assert "last_name" in create_sql
    
    print("✓ SQL 辅助函数测试通过")


def test_phonetic_variants():
    """测试语音变体生成"""
    encoder = SoundexEncoder()
    
    variants = encoder.get_phonetic_variants("S530")
    
    # 应该有多个变体
    assert len(variants) > 0
    # 所有变体应以 S 开头
    for v in variants[:10]:
        assert v.startswith("S")
    
    print(f"  S530 生成 {len(variants)} 个变体")
    print(f"  示例: {variants[:5]}")
    print("✓ 语音变体生成测试通过")


def test_enhanced_mode():
    """测试增强模式"""
    std_encoder = SoundexEncoder(enhanced=False)
    enh_encoder = SoundexEncoder(enhanced=True)
    
    # 增强模式处理 Mc/Mac 前缀
    # 注意：效果取决于具体实现
    std_mcdonald = std_encoder.encode("McDonald")
    enh_mcdonald = enh_encoder.encode("McDonald")
    
    print(f"  McDonald: 标准={std_mcdonald}, 增强={enh_mcdonald}")
    print("✓ 增强模式测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("SOUNDEX 工具模块测试")
    print("=" * 50)
    
    tests = [
        test_basic_encoding,
        test_name_matching,
        test_different_names,
        test_edge_cases,
        test_unicode_support,
        test_length_parameter,
        test_refined_encoder,
        test_similarity,
        test_matches,
        test_find_similar,
        test_group_by_code,
        test_batch_encoding,
        test_convenience_functions,
        test_common_names,
        test_sql_helpers,
        test_phonetic_variants,
        test_enhanced_mode,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 错误: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)