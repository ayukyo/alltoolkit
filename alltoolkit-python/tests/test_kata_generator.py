"""
AllToolkit Kata Generator 测试套件
"""

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.kata_generator import (
    generate_kata,
    preview_kata,
    list_katas_by_language,
    available_difficulties,
    KATA_DATABASE,
    _select_kata,
    _format_kata_markdown,
    _file_ext,
)


_INITIAL_YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
INITIAL_TEST_DATA = {
    "languages": [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ],
    "current_index": 3,
    "last_language": "Swift",
    "updated_at": f"{_INITIAL_YESTERDAY}T02:10:00+08:00",
}


def _make_temp_json():
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_kata_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)
    return path


class TestFileExt(unittest.TestCase):
    def test_file_ext_rust(self):
        self.assertEqual(_file_ext("Rust"), "rust")

    def test_file_ext_go(self):
        self.assertEqual(_file_ext("Go"), "go")

    def test_file_ext_cpp(self):
        self.assertEqual(_file_ext("C/C++"), "cpp")

    def test_file_ext_unknown(self):
        self.assertEqual(_file_ext("Forth"), "text")


class TestSelectKata(unittest.TestCase):
    def test_select_returns_kt_kata(self):
        kata = _select_kata("Kotlin")
        self.assertIn("id", kata)
        self.assertIn("title", kata)
        self.assertIn("difficulty", kata)
        self.assertIn("description", kata)
        self.assertIn("starter_code", kata)
        self.assertIn("hints", kata)
        self.assertIn("solution", kata)

    def test_select_with_difficulty_easy(self):
        kata = _select_kata("Rust", difficulty="easy")
        self.assertEqual(kata["difficulty"], "easy")

    def test_select_with_difficulty_invalid_falls_back(self):
        kata = _select_kata("Go", difficulty="impossible")
        # 无此难度 → 回退到随机
        self.assertIn("difficulty", kata)

    def test_select_unknown_language_raises(self):
        with self.assertRaises(ValueError):
            _select_kata("Pascal")

    def test_all_languages_have_katas(self):
        for lang in KATA_DATABASE:
            self.assertGreater(len(KATA_DATABASE[lang]), 0)


class TestFormatKataMarkdown(unittest.TestCase):
    def test_format_contains_title(self):
        kata = KATA_DATABASE["Rust"][0]
        md = _format_kata_markdown(kata, "Rust")
        self.assertIn(kata["title"], md)

    def test_format_contains_difficulty(self):
        kata = KATA_DATABASE["Go"][0]
        md = _format_kata_markdown(kata, "Go")
        self.assertIn(kata["difficulty"].upper(), md)

    def test_format_contains_starter_code(self):
        kata = KATA_DATABASE["Swift"][0]
        md = _format_kata_markdown(kata, "Swift")
        self.assertIn(kata["starter_code"], md)

    def test_format_contains_solution(self):
        kata = KATA_DATABASE["Kotlin"][0]
        md = _format_kata_markdown(kata, "Kotlin")
        self.assertIn(kata["solution"], md)

    def test_format_shows_next_language(self):
        kata = KATA_DATABASE["TypeScript"][0]
        md = _format_kata_markdown(kata, "TypeScript", next_language="JavaScript")
        self.assertIn("JavaScript", md)
        self.assertIn("下一个语言", md)


class TestAvailableDifficulties(unittest.TestCase):
    def test_difficulties_returns_three_levels(self):
        diffs = available_difficulties()
        self.assertEqual(set(diffs), {"easy", "medium", "hard"})


class TestGenerateKata(unittest.TestCase):
    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_generate_returns_language(self):
        result = generate_kata(json_path=self.test_path)
        self.assertEqual(result["language"], "Kotlin")
        self.assertIn("next_language", result)

    def test_generate_returns_kt_kata(self):
        result = generate_kata(json_path=self.test_path)
        self.assertIn("kotlin", KATA_DATABASE["Kotlin"][0]["id"])

    def test_generate_returns_markdown(self):
        result = generate_kata(json_path=self.test_path)
        self.assertIn("markdown", result)
        self.assertIn("🏋️", result["markdown"])
        self.assertIn("Kotlin", result["markdown"])

    def test_generate_updates_json(self):
        generate_kata(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 索引从 3 → 4 (TypeScript)
        self.assertEqual(data["current_index"], 4)
        self.assertEqual(data["last_language"], "Kotlin")

    def test_generate_updates_timestamp(self):
        generate_kata(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertNotEqual(data["updated_at"], INITIAL_TEST_DATA["updated_at"])

    def test_generate_index_wraps(self):
        # 从 index=7 开始，连续生成 3 次
        with open(self.test_path, "w", encoding="utf-8") as f:
            data = INITIAL_TEST_DATA.copy()
            data["current_index"] = 7
            json.dump(data, f, ensure_ascii=False, indent=2)
        # C/C++(7) → Rust(0) → Go(1) → Swift(2)
        result1 = generate_kata(json_path=self.test_path)
        self.assertEqual(result1["language"], "C/C++")
        self.assertEqual(result1["next_language"], "Rust")
        result2 = generate_kata(json_path=self.test_path)
        self.assertEqual(result2["language"], "Rust")
        result3 = generate_kata(json_path=self.test_path)
        self.assertEqual(result3["language"], "Go")

    def test_generate_with_seed_is_deterministic(self):
        result1 = generate_kata(json_path=self.test_path, seed=42)
        # 重置 JSON
        with open(self.test_path, "w", encoding="utf-8") as f:
            json.dump(INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)
        result2 = generate_kata(json_path=self.test_path, seed=42)
        self.assertEqual(result1["kata"]["id"], result2["kata"]["id"])

    def test_generate_with_difficulty_filter(self):
        result = generate_kata(json_path=self.test_path, difficulty="easy")
        self.assertEqual(result["kata"]["difficulty"], "easy")


class TestPreviewKata(unittest.TestCase):
    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_preview_returns_kata(self):
        result = preview_kata(json_path=self.test_path)
        self.assertIn("kata", result)
        self.assertIn("markdown", result)

    def test_preview_uses_current_language(self):
        result = preview_kata(json_path=self.test_path)
        self.assertEqual(result["language"], "Kotlin")

    def test_preview_does_not_change_index(self):
        with open(self.test_path, "r", encoding="utf-8") as f:
            before = json.load(f)["current_index"]
        preview_kata(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            after = json.load(f)["current_index"]
        self.assertEqual(before, after)

    def test_preview_with_explicit_language(self):
        result = preview_kata(language="Rust", json_path=self.test_path)
        self.assertEqual(result["language"], "Rust")

    def test_preview_with_seed_is_deterministic(self):
        result1 = preview_kata(json_path=self.test_path, seed=99)
        result2 = preview_kata(json_path=self.test_path, seed=99)
        self.assertEqual(result1["kata"]["id"], result2["kata"]["id"])


class TestListKatasByLanguage(unittest.TestCase):
    def test_list_all_languages(self):
        result = list_katas_by_language()
        self.assertIn("Rust", result)
        self.assertIn("Kotlin", result)
        self.assertIn("C/C++", result)

    def test_list_specific_language(self):
        result = list_katas_by_language("Rust")
        self.assertEqual(result["language"], "Rust")
        self.assertGreater(result["count"], 0)
        self.assertIn("katas", result)

    def test_list_unknown_language(self):
        # 返回空列表
        result = list_katas_by_language("Pascal")
        self.assertEqual(result["count"], 0)


class TestKATADatabase(unittest.TestCase):
    def test_all_languages_have_ids(self):
        for lang, katas in KATA_DATABASE.items():
            for kata in katas:
                self.assertIn("id", kata, f"{lang} kata missing id")
                # IDs use language prefixes (first 4 chars, or known abbreviations)
                known_prefixes = {
                    "TypeScript": "ts", "JavaScript": "js", "C/C++": "cpp"
                }
                prefix = known_prefixes.get(lang, lang[:4].lower())
                self.assertTrue(
                    kata["id"].startswith(prefix),
                    f"{lang} kata id format: {kata['id']} (expected prefix '{prefix}')"
                )

    def test_all_languages_have_title(self):
        for lang, katas in KATA_DATABASE.items():
            for kata in katas:
                self.assertIn("title", kata)
                self.assertTrue(len(kata["title"]) > 0)

    def test_all_languages_have_description(self):
        for lang, katas in KATA_DATABASE.items():
            for kata in katas:
                self.assertIn("description", kata)
                self.assertTrue(len(kata["description"]) > 10)

    def test_all_languages_have_starter_code(self):
        for lang, katas in KATA_DATABASE.items():
            for kata in katas:
                self.assertIn("starter_code", kata)
                self.assertTrue(len(kata["starter_code"]) > 5)

    def test_all_languages_have_hints(self):
        for lang, katas in KATA_DATABASE.items():
            for kata in katas:
                self.assertIn("hints", kata)
                self.assertIsInstance(kata["hints"], list)
                self.assertGreater(len(kata["hints"]), 0)

    def test_all_languages_have_solution(self):
        for lang, katas in KATA_DATABASE.items():
            for kata in katas:
                self.assertIn("solution", kata)
                self.assertTrue(len(kata["solution"]) > 5)

    def test_difficulties_are_valid(self):
        valid = {"easy", "medium", "hard"}
        for lang, katas in KATA_DATABASE.items():
            for kata in katas:
                self.assertIn(kata["difficulty"], valid,
                              f"{lang}/{kata['id']} has invalid difficulty: {kata['difficulty']}")


class TestKATAGeneratorIntegration(unittest.TestCase):
    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_full_rotation_cycle(self):
        # 从 index=3(Kotlin) 开始，完整轮换 8 种语言
        expected_langs = [
            "Kotlin", "TypeScript", "JavaScript",
            "Java", "C/C++", "Rust", "Go", "Swift",
        ]
        for expected in expected_langs:
            result = generate_kata(json_path=self.test_path)
            self.assertEqual(result["language"], expected)
            self.assertIn("markdown", result)
            self.assertTrue(result["json_updated"])

    def test_preview_then_generate_preserves_order(self):
        # preview 不影响索引，generate 正常轮换
        preview_kata(json_path=self.test_path)
        preview_kata(json_path=self.test_path)
        result = generate_kata(json_path=self.test_path)
        self.assertEqual(result["language"], "Kotlin")  # 索引仍为 3

    def test_markdown_contains_all_parts(self):
        result = generate_kata(json_path=self.test_path)
        md = result["markdown"]
        self.assertIn("🏋️", md)
        self.assertIn("难度", md)
        self.assertIn("起始代码", md)
        self.assertIn("提示", md)
        self.assertIn("参考解答", md)
        self.assertIn(result["next_language"], md)


if __name__ == "__main__":
    unittest.main(verbosity=2)