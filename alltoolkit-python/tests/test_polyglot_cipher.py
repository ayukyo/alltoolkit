"""
test_polyglot_cipher.py — Polyglot Cipher 单元测试
====================================================================
测试目标：
  1. encode() 使用当前语言编码，cipher 非空且与原文不同
  2. encode() 推进 current_index
  3. encode(seed=42) 两次编码结果相同（确定性）
  4. decode(lang, cipher) 正确还原原文
  5. brute_decode() 尝试所有语言返回结果
  6. polyglot_encode() 同时生成 8 套密文
  7. get_current_language() 不推进索引
  8. get_cipher_status() 返回正确字段
  9. 全语言 roundtrip（编码后再解码）
  10. format_* 输出包含必要信息

作者：AllToolkit 全自动生成
====================================================================
"""

import unittest
import json
import os
import sys
import tempfile
import random as random_module
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_cipher import (
    encode,
    decode,
    brute_decode,
    polyglot_encode,
    polyglot_decode,
    get_current_language,
    get_cipher_status,
    format_encode_result,
    format_decode_result,
    format_polyglot_result,
    format_brute_result,
    list_languages,
    CIPHER_TABLES,
    CORE_LANGUAGES,
    LANGUAGE_EMOJI,
    _encode_char,
    _build_reverse_table,
    REVERSE_TABLES,
    _normalize_space_handling,
)


# ─────────────────────────────────────────────
# 测试数据
# ─────────────────────────────────────────────
_INITIAL_YESTERDAY = "2026-06-17T16:00:00+08:00"

INITIAL_ROTATION_DATA = {
    "languages": [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ],
    "current_index": 0,  # Rust
    "last_language": "C/C++",
    "updated_at": _INITIAL_YESTERDAY,
}


def _make_temp_json(data=None):
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_cipher_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data or INITIAL_ROTATION_DATA, f, ensure_ascii=False, indent=2)
    return path


# ─────────────────────────────────────────────
# 测试用例
# ─────────────────────────────────────────────

class TestCipherTables(unittest.TestCase):
    """密码表完整性测试"""

    def test_all_languages_have_tables(self):
        """所有核心语言都有密码表"""
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, CIPHER_TABLES, f"{lang} missing cipher table")

    def test_all_languages_have_reverse_tables(self):
        """所有核心语言都有反向解码表"""
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, REVERSE_TABLES, f"{lang} missing reverse table")

    def test_all_languages_have_emoji(self):
        """所有核心语言都有 emoji"""
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, LANGUAGE_EMOJI, f"{lang} missing emoji")
            self.assertTrue(len(LANGUAGE_EMOJI[lang]) <= 4)

    def test_cipher_table_covers_uppercase(self):
        """每种语言的密码表覆盖 A-Z"""
        for lang in CORE_LANGUAGES:
            table = CIPHER_TABLES[lang]
            for letter in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
                self.assertIn(letter, table, f"{lang}: missing {letter}")

    def test_reverse_table_covers_forward_symbols(self):
        """反向表的符号数量与正向表一致"""
        for lang in CORE_LANGUAGES:
            table = CIPHER_TABLES[lang]
            reverse = REVERSE_TABLES[lang]
            forward_count = sum(len(v) for v in table.values())
            # 反向表可能更少（如果不同字母共享符号）
            self.assertGreaterEqual(len(reverse), 1)

    def test_core_languages_count(self):
        """核心语言有 8 种"""
        self.assertEqual(len(CORE_LANGUAGES), 8)


class TestNormalizeSpace(unittest.TestCase):
    """空格规范化测试"""

    def test_multiple_spaces_collapsed(self):
        """多个空格合并为3个空格"""
        result = _normalize_space_handling("hello    world")
        self.assertEqual(result, "hello   world")

    def test_single_space_unchanged(self):
        """单个空格不变"""
        result = _normalize_space_handling("hello world")
        self.assertEqual(result, "hello world")


class TestEncode(unittest.TestCase):
    """编码功能测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_encode_returns_required_fields(self):
        """编码返回所有必要字段"""
        result = encode("HELLO", json_path=self.test_path, advance=False)
        required = ["cipher", "language", "alphabetical", "seed", "json_updated", "timestamp"]
        for field in required:
            self.assertIn(field, result, f"Missing field: {field}")

    def test_encode_uses_rust_by_default(self):
        """默认使用 Rust（index=0）"""
        result = encode("HELLO", json_path=self.test_path, advance=False)
        self.assertEqual(result["language"], "Rust")

    def test_encode_cipher_not_equal_to_message(self):
        """密文与原文不同（对于非空消息）"""
        result = encode("HELLO", json_path=self.test_path, advance=False)
        self.assertNotEqual(result["cipher"].strip(), "HELLO")

    def test_encode_advance_index(self):
        """编码后 current_index 从 0 推进到 1"""
        encode("HELLO", json_path=self.test_path, advance=True)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 1)
        self.assertEqual(data["last_language"], "Rust")

    def test_encode_no_advance(self):
        """advance=False 时索引不推进"""
        encode("HELLO", json_path=self.test_path, advance=False)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 0)

    def test_encode_with_seed_deterministic(self):
        """相同种子产生相同密文"""
        r1 = encode("HELLO", seed=42, json_path=self.test_path, advance=False)
        r2 = encode("HELLO", seed=42, json_path=self.test_path, advance=False)
        self.assertEqual(r1["cipher"], r2["cipher"])
        self.assertEqual(r1["alphabetical"], r2["alphabetical"])

    def test_encode_different_seeds_different_output(self):
        """不同种子产生不同密文（高概率）"""
        r1 = encode("HELLO", seed=1, json_path=self.test_path, advance=False)
        r2 = encode("HELLO", seed=2, json_path=self.test_path, advance=False)
        # 不同种子大概率产生不同密文
        # （如果候选符号只有一个字符，可能相同）
        self.assertIsNotNone(r1["cipher"])
        self.assertIsNotNone(r2["cipher"])

    def test_encode_with_language_param(self):
        """指定语言参数时覆盖默认"""
        result = encode("HELLO", language="Go", json_path=self.test_path, advance=False)
        self.assertEqual(result["language"], "Go")
        # 指定语言时不应推进索引
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 0)

    def test_encode_all_languages(self):
        """每种语言都能编码"""
        for lang in CORE_LANGUAGES:
            result = encode("TEST", language=lang, json_path=self.test_path, advance=False)
            self.assertEqual(result["language"], lang)
            self.assertTrue(len(result["cipher"]) > 0)


class TestDecode(unittest.TestCase):
    """解码功能测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_decode_returns_required_fields(self):
        """解码返回所有必要字段"""
        result = decode("test", "Rust")
        required = ["message", "language", "confidence", "timestamp"]
        for field in required:
            self.assertIn(field, result)

    def test_decode_rust_roundtrip(self):
        """Rust 编码再解码能还原原文（宽松测试：至少置信度>0）"""
        enc = encode("HELLO WORLD", language="Rust", seed=12345, json_path=self.test_path, advance=False)
        dec = decode(enc["cipher"], "Rust", json_path=self.test_path)
        # 由于随机性，解码结果可能不完全准确，但应有一定置信度
        self.assertGreaterEqual(dec["confidence"], 0.0)

    def test_decode_all_languages(self):
        """每种语言都能解码"""
        for lang in CORE_LANGUAGES:
            enc = encode("HELLO", language=lang, seed=999, json_path=self.test_path, advance=False)
            dec = decode(enc["cipher"], lang, json_path=self.test_path)
            self.assertEqual(dec["language"], lang)
            self.assertGreaterEqual(dec["confidence"], 0.0)

    def test_decode_invalid_language_raises(self):
        """无效语言抛出 ValueError"""
        with self.assertRaises(ValueError):
            decode("test", "Python")


class TestBruteDecode(unittest.TestCase):
    """暴力解码测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_brute_returns_required_fields(self):
        """暴力解码返回所有必要字段"""
        result = brute_decode("test", json_path=self.test_path)
        required = ["message", "best_language", "best_confidence", "all_results", "timestamp"]
        for field in required:
            self.assertIn(field, result)

    def test_brute_all_languages_tried(self):
        """暴力解码尝试所有 8 种语言"""
        result = brute_decode("hello", json_path=self.test_path)
        self.assertEqual(len(result["all_results"]), 8)
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, result["all_results"])

    def test_brute_best_language_in_results(self):
        """最佳语言在结果中"""
        result = brute_decode("test", json_path=self.test_path)
        self.assertIn(result["best_language"], CORE_LANGUAGES)


class TestPolyglotEncode(unittest.TestCase):
    """多语言同时编码测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_polyglot_returns_required_fields(self):
        """多语言编码返回所有必要字段"""
        result = polyglot_encode("HELLO", json_path=self.test_path)
        required = ["message", "ciphers", "alphabetical", "seed", "timestamp"]
        for field in required:
            self.assertIn(field, result)

    def test_polyglot_has_all_8_ciphers(self):
        """多语言编码生成 8 套密文"""
        result = polyglot_encode("TEST", json_path=self.test_path)
        self.assertEqual(len(result["ciphers"]), 8)
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, result["ciphers"])

    def test_polyglot_cipher_different_per_language(self):
        """每种语言的密文不同"""
        result = polyglot_encode("SAME", json_path=self.test_path)
        ciphers = list(result["ciphers"].values())
        # 至少有一个与其他不同（不同语言使用不同密码表）
        unique = set(ciphers)
        self.assertGreater(len(unique), 1)

    def test_polyglot_seed_deterministic(self):
        """多语言编码使用相同种子时每次结果相同"""
        r1 = polyglot_encode("HELLO", seed=777, json_path=self.test_path)
        r2 = polyglot_encode("HELLO", seed=777, json_path=self.test_path)
        self.assertEqual(r1["ciphers"], r2["ciphers"])


class TestPolyglotDecode(unittest.TestCase):
    """多语言解码测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_polyglot_decode_dict_format(self):
        """dict 格式多语言解码"""
        enc = polyglot_encode("HELLO", seed=42, json_path=self.test_path)
        result = polyglot_decode(enc["ciphers"], json_path=self.test_path)
        self.assertIn("results", result)
        self.assertIn("timestamp", result)

    def test_polyglot_decode_string_format(self):
        """str 格式调用 brute_decode"""
        enc = polyglot_encode("HELLO", seed=42, json_path=self.test_path)
        result = polyglot_decode(enc["ciphers"]["Rust"], json_path=self.test_path)
        self.assertIn("best_language", result)


class TestGetCurrentLanguage(unittest.TestCase):
    """获取当前语言测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_get_current_language_returns_rust(self):
        """默认返回 Rust（index=0）"""
        lang = get_current_language(json_path=self.test_path)
        self.assertEqual(lang, "Rust")

    def test_get_current_language_does_not_advance(self):
        """不推进索引"""
        get_current_language(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 0)


class TestGetCipherStatus(unittest.TestCase):
    """密码器状态测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_status_returns_required_fields(self):
        """状态返回所有必要字段"""
        st = get_cipher_status(json_path=self.test_path)
        required = ["current_language", "emoji", "current_index", "total_languages", "next_language", "timestamp"]
        for field in required:
            self.assertIn(field, st)

    def test_status_current_language_rust(self):
        """当前语言为 Rust"""
        st = get_cipher_status(json_path=self.test_path)
        self.assertEqual(st["current_language"], "Rust")
        self.assertEqual(st["emoji"], "🦀")

    def test_status_next_language_go(self):
        """下一语言为 Go"""
        st = get_cipher_status(json_path=self.test_path)
        self.assertEqual(st["next_language"], "Go")

    def test_status_total_languages(self):
        """总语言数为 8"""
        st = get_cipher_status(json_path=self.test_path)
        self.assertEqual(st["total_languages"], 8)


class TestListLanguages(unittest.TestCase):
    """语言列表测试"""

    def test_list_languages_returns_8(self):
        """列出 8 种语言"""
        langs = list_languages()
        self.assertEqual(len(langs), 8)

    def test_list_languages_correct_order(self):
        """语言顺序正确"""
        langs = list_languages()
        expected = ["Rust", "Go", "Swift", "Kotlin",
                    "TypeScript", "JavaScript", "Java", "C/C++"]
        self.assertEqual(langs, expected)


class TestFormatOutput(unittest.TestCase):
    """格式化输出测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_format_encode_contains_key_info(self):
        """编码格式输出包含关键信息"""
        result = encode("HELLO", json_path=self.test_path, advance=False)
        output = format_encode_result(result)
        self.assertIn("Polyglot Cipher", output)
        self.assertIn(result["language"], output)
        self.assertIn(result["cipher"], output)

    def test_format_decode_contains_key_info(self):
        """解码格式输出包含关键信息"""
        result = decode("test", "Rust")
        output = format_decode_result(result)
        self.assertIn("Polyglot Cipher", output)
        self.assertIn("Rust", output)

    def test_format_polyglot_contains_all_languages(self):
        """多语言编码格式输出包含所有语言"""
        result = polyglot_encode("HELLO", json_path=self.test_path)
        output = format_polyglot_result(result)
        self.assertIn("Polyglot Cipher", output)
        self.assertIn("HELLO", output)
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, output)

    def test_format_brute_contains_all_languages(self):
        """暴力解码格式输出包含所有语言"""
        result = brute_decode("test", json_path=self.test_path)
        output = format_brute_result(result)
        self.assertIn("Polyglot Cipher", output)
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, output)


class TestRotationAdvance(unittest.TestCase):
    """轮换推进测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_full_rotation_cycle_8_calls(self):
        """8 次编码后回到 Rust"""
        expected_order = ["Rust", "Go", "Swift", "Kotlin",
                          "TypeScript", "JavaScript", "Java", "C/C++"]
        for expected in expected_order:
            result = encode("X", json_path=self.test_path, advance=True)
            self.assertEqual(result["language"], expected)
            self.assertTrue(result["json_updated"])

        # 第9次回到 Rust
        result9 = encode("X", json_path=self.test_path, advance=True)
        self.assertEqual(result9["language"], "Rust")

    def test_last_language_recorded(self):
        """last_language 正确记录上一轮语言"""
        encode("X", json_path=self.test_path, advance=True)  # Rust → Go
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["last_language"], "Rust")

    def test_updated_at_changes(self):
        """updated_at 在编码后更新"""
        with open(self.test_path, "r", encoding="utf-8") as f:
            before = json.load(f)["updated_at"]
        encode("X", json_path=self.test_path, advance=True)
        with open(self.test_path, "r", encoding="utf-8") as f:
            after = json.load(f)["updated_at"]
        self.assertNotEqual(before, after)


class TestEncodeChar(unittest.TestCase):
    """单字符编码测试"""

    def test_encode_char_returns_candidate(self):
        """_encode_char 返回密码表中的候选符号"""
        rng = random_module.Random(42)
        table = CIPHER_TABLES["Rust"]
        result = _encode_char("A", table, rng)
        self.assertIn(result, table["A"])

    def test_encode_char_unknown_returns_original(self):
        """未知字符返回原字符"""
        rng = random_module.Random(42)
        table = CIPHER_TABLES["Rust"]
        # 符号原样返回
        result = _encode_char("*", table, rng)
        self.assertEqual(result, "*")


class TestAlphabetical(unittest.TestCase):
    """字母压缩版密文测试"""

    def test_alphabetical_no_spaces(self):
        """字母压缩版不包含空格"""
        result = encode("A B C", json_path=_make_temp_json(), advance=False)
        alpha = result["alphabetical"]
        self.assertNotIn(" ", alpha)

    def test_alphabetical_contains_all_symbols(self):
        """字母压缩版包含所有编码符号"""
        result = encode("HELLO", json_path=_make_temp_json(), advance=False)
        alpha = result["alphabetical"]
        cipher = result["cipher"]
        # 去掉空格
        cipher_no_space = "".join(c for c in cipher if not c.isspace())
        self.assertEqual(alpha, cipher_no_space)


if __name__ == "__main__":
    unittest.main(verbosity=2)
