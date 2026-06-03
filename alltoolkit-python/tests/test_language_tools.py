"""
语言工具模块测试
"""

import unittest
import json
import tempfile
import shutil
import os
import sys
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.language_tools import (
    LANGUAGE_PERSONAS,
    load_rotation_config,
    save_rotation_config,
    rotate_language,
    get_language_persona,
    get_current_persona,
    suggest_language_for_project,
    get_rotation_summary,
)


# 测试用配置数据
SAMPLE_CONFIG = {
    "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
    "current_index": 2,
    "last_language": "Swift",
    "updated_at": "2026-06-04T00:00:00+08:00",
}

EXPECTED_SEQUENCE = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]


class TestLanguagePersonas(unittest.TestCase):
    """语言画像测试"""

    def test_all_languages_have_persona(self):
        """所有语言都有画像"""
        for lang in EXPECTED_SEQUENCE:
            persona = get_language_persona(lang)
            self.assertIsNotNone(persona, f"Missing persona for {lang}")

    def test_persona_has_required_fields(self):
        """画像包含必要字段"""
        required = ["emoji", "tagline", "strengths", "typical_projects", "key_concepts", "code_example", "resources", "quirks"]
        for lang in EXPECTED_SEQUENCE:
            persona = get_language_persona(lang)
            for field in required:
                self.assertIn(field, persona, f"Missing '{field}' in {lang} persona")

    def test_rust_persona_specifics(self):
        """Rust 画像特定内容"""
        persona = get_language_persona("Rust")
        self.assertEqual(persona["emoji"], "🦀")
        self.assertIn("内存安全", persona["tagline"])
        self.assertTrue(any("Ownership" in str(c) for c in persona["key_concepts"]))

    def test_go_persona_specifics(self):
        """Go 画像特定内容"""
        persona = get_language_persona("Go")
        self.assertEqual(persona["emoji"], "🐹")
        self.assertIn("goroutine", persona["key_concepts"])

    def test_swift_persona_specifics(self):
        """Swift 画像特定内容"""
        persona = get_language_persona("Swift")
        self.assertEqual(persona["emoji"], "🦅")
        self.assertIn("optional", persona["key_concepts"])

    def test_kotlin_persona_specifics(self):
        """Kotlin 画像特定内容"""
        persona = get_language_persona("Kotlin")
        self.assertEqual(persona["emoji"], "🧃")
        self.assertIn("coroutine", persona["key_concepts"])

    def test_typescript_persona_specifics(self):
        """TypeScript 画像特定内容"""
        persona = get_language_persona("TypeScript")
        self.assertEqual(persona["emoji"], "🔷")
        self.assertIn("generic", persona["key_concepts"])

    def test_javascript_persona_specifics(self):
        """JavaScript 画像特定内容"""
        persona = get_language_persona("JavaScript")
        self.assertEqual(persona["emoji"], "🟨")
        self.assertIn("event loop", persona["key_concepts"])

    def test_java_persona_specifics(self):
        """Java 画像特定内容"""
        persona = get_language_persona("Java")
        self.assertEqual(persona["emoji"], "☕")
        self.assertIn("JVM", persona["key_concepts"])

    def test_c_cpp_persona_specifics(self):
        """C/C++ 画像特定内容"""
        persona = get_language_persona("C/C++")
        self.assertEqual(persona["emoji"], "⚙️")
        self.assertIn("指针", str(persona["key_concepts"]))

    def test_unknown_language_returns_none(self):
        """未知语言返回 None"""
        self.assertIsNone(get_language_persona("Ruby"))
        self.assertIsNone(get_language_persona("Pascal"))


class TestRotationConfig(unittest.TestCase):
    """轮换配置测试"""

    def setUp(self):
        """创建临时测试目录"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "language_rotation.json")

    def tearDown(self):
        """清理临时目录"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_save_and_load_config(self):
        """测试保存和加载配置"""
        save_rotation_config(SAMPLE_CONFIG, self.test_file)
        loaded = load_rotation_config(self.test_file)

        self.assertEqual(loaded["languages"], SAMPLE_CONFIG["languages"])
        self.assertEqual(loaded["current_index"], SAMPLE_CONFIG["current_index"])
        self.assertEqual(loaded["last_language"], SAMPLE_CONFIG["last_language"])

    def test_load_nonexistent_raises(self):
        """加载不存在的文件报错"""
        with self.assertRaises(FileNotFoundError):
            load_rotation_config("/nonexistent/path/config.json")


class TestRotateLanguage(unittest.TestCase):
    """轮换语言测试"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "language_rotation.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_rotate_rust_next_is_go(self):
        """从 Rust 轮换，下一个语言是 Go"""
        config = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 0,  # Rust
            "last_language": "JavaScript",
            "updated_at": "2026-06-04T00:00:00+08:00",
        }
        result = rotate_language(config, self.test_file)

        self.assertEqual(result["current_language"], "Rust")
        self.assertEqual(result["current_index"], 0)
        self.assertEqual(result["next_language"], "Go")
        self.assertEqual(result["next_index"], 1)

    def test_rotate_updates_config_file(self):
        """轮换后配置文件中 current_index 更新"""
        config = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 3,  # Kotlin
            "last_language": "TypeScript",
            "updated_at": "2026-06-04T00:00:00+08:00",
        }
        rotate_language(config, self.test_file)

        with open(self.test_file, "r", encoding="utf-8") as f:
            saved = json.load(f)

        # Kotlin(3) -> next_index = 4
        self.assertEqual(saved["current_index"], 4)
        self.assertEqual(saved["last_language"], "Kotlin")
        self.assertIn("updated_at", saved)

    def test_rotate_full_cycle(self):
        """完整循环一圈"""
        languages = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]

        for i in range(len(languages)):
            config = {
                "languages": languages,
                "current_index": i,
                "last_language": languages[i - 1],
                "updated_at": "2026-06-04T00:00:00+08:00",
            }
            result = rotate_language(config, self.test_file)

            expected_current = languages[i]
            expected_next = languages[(i + 1) % len(languages)]
            expected_next_idx = (i + 1) % len(languages)

            self.assertEqual(result["current_language"], expected_current,
                            f"At index {i}: expected {expected_current}, got {result['current_language']}")
            self.assertEqual(result["next_language"], expected_next)
            self.assertEqual(result["next_index"], expected_next_idx)

    def test_rotation_sequence_preserved(self):
        """轮换后语言顺序保持不变"""
        config = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 5,
            "last_language": "TypeScript",
            "updated_at": "2026-06-04T00:00:00+08:00",
        }
        result = rotate_language(config, self.test_file)

        self.assertEqual(result["rotation_sequence"], EXPECTED_SEQUENCE)

    def test_result_contains_all_fields(self):
        """结果包含所有必要字段"""
        config = {
            "languages": ["Rust", "Go", "Swift"],
            "current_index": 0,
            "last_language": "JavaScript",
            "updated_at": "2026-06-04T00:00:00+08:00",
        }
        result = rotate_language(config, self.test_file)

        for field in ["current_language", "current_index", "next_language", "next_index", "rotation_sequence", "updated_config"]:
            self.assertIn(field, result)

    def test_force_language_rust(self):
        """强制选择 Rust（本次必须选 Rust）"""
        config = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 3,  # Kotlin
            "last_language": "TypeScript",
            "updated_at": "2026-06-04T00:00:00+08:00",
        }
        result = rotate_language(config, self.test_file, force_language="Rust")

        self.assertEqual(result["current_language"], "Rust")
        self.assertEqual(result["current_index"], 0)

        # 保存后 current_index 变成 next_index = (0+1)%8 = 1 → Go
        with open(self.test_file, "r", encoding="utf-8") as f:
            saved = json.load(f)
        self.assertEqual(saved["current_index"], 1)  # Go
        self.assertEqual(saved["last_language"], "Rust")

    def test_force_language_updates_next_correctly(self):
        """强制选择 Rust 后，下一个语言正确"""
        config = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 3,
            "last_language": "TypeScript",
            "updated_at": "2026-06-04T00:00:00+08:00",
        }
        result = rotate_language(config, self.test_file, force_language="Rust")

        # Rust(0) -> next_index = 1 -> Go
        self.assertEqual(result["next_language"], "Go")
        self.assertEqual(result["next_index"], 1)

    def test_force_language_invalid(self):
        """强制选择未知语言报错"""
        config = {
            "languages": ["Rust", "Go", "Swift"],
            "current_index": 0,
            "last_language": "JavaScript",
            "updated_at": "2026-06-04T00:00:00+08:00",
        }
        with self.assertRaises(ValueError):
            rotate_language(config, self.test_file, force_language="Ruby")


class TestGetCurrentPersona(unittest.TestCase):
    """当前语言画像测试"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "language_rotation.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_get_current_persona_rust(self):
        """index=0 时获取 Rust 画像"""
        config = {
            "languages": ["Rust", "Go", "Swift"],
            "current_index": 0,
            "last_language": "C/C++",
            "updated_at": "2026-06-04T00:00:00+08:00",
        }
        save_rotation_config(config, self.test_file)

        result = get_current_persona(load_rotation_config(self.test_file))

        self.assertEqual(result["language"], "Rust")
        self.assertEqual(result["index"], 0)
        self.assertIn("emoji", result["persona"])

    def test_get_current_persona_go(self):
        """index=1 时获取 Go 画像"""
        config = {
            "languages": ["Rust", "Go", "Swift"],
            "current_index": 1,
            "last_language": "Rust",
            "updated_at": "2026-06-04T00:00:00+08:00",
        }
        save_rotation_config(config, self.test_file)

        result = get_current_persona(load_rotation_config(self.test_file))

        self.assertEqual(result["language"], "Go")
        self.assertEqual(result["index"], 1)


class TestSuggestLanguageForProject(unittest.TestCase):
    """项目语言推荐测试"""

    def test_suggest_web(self):
        """web 项目推荐"""
        suggestions = suggest_language_for_project("web")
        self.assertIsInstance(suggestions, list)
        lang_names = [s["language"] for s in suggestions]
        self.assertIn("TypeScript", lang_names)
        self.assertIn("JavaScript", lang_names)

    def test_suggest_mobile(self):
        """mobile 项目推荐"""
        suggestions = suggest_language_for_project("mobile")
        lang_names = [s["language"] for s in suggestions]
        self.assertIn("Swift", lang_names)
        self.assertIn("Kotlin", lang_names)

    def test_suggest_cli(self):
        """cli 项目推荐"""
        suggestions = suggest_language_for_project("cli")
        lang_names = [s["language"] for s in suggestions]
        self.assertIn("Rust", lang_names)
        self.assertIn("Go", lang_names)

    def test_suggest_backend(self):
        """backend 项目推荐"""
        suggestions = suggest_language_for_project("backend")
        lang_names = [s["language"] for s in suggestions]
        self.assertIn("Go", lang_names)
        self.assertIn("Java", lang_names)

    def test_suggest_returns_persona(self):
        """推荐结果包含完整画像"""
        suggestions = suggest_language_for_project("ios")
        self.assertGreater(len(suggestions), 0)
        first = suggestions[0]
        self.assertIn("persona", first)
        self.assertIn("emoji", first["persona"])


class TestGetRotationSummary(unittest.TestCase):
    """轮换概览测试"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "language_rotation.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_summary_contains_current_language(self):
        """概览包含当前语言"""
        config = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 0,
            "last_language": "C/C++",
            "updated_at": "2026-06-04T00:00:00+08:00",
        }
        save_rotation_config(config, self.test_file)

        import modules.language_tools as lt
        original_path = lt._get_rotation_file_path
        lt._get_rotation_file_path = lambda: self.test_file

        try:
            summary = get_rotation_summary()
        finally:
            lt._get_rotation_file_path = original_path

        self.assertIn("Rust", summary)
        self.assertIn("▶", summary)

    def test_summary_shows_next_language(self):
        """概览显示下一个语言"""
        config = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 0,
            "last_language": "C/C++",
            "updated_at": "2026-06-04T00:00:00+08:00",
        }
        save_rotation_config(config, self.test_file)

        import modules.language_tools as lt
        original_path = lt._get_rotation_file_path
        lt._get_rotation_file_path = lambda: self.test_file

        try:
            summary = get_rotation_summary()
        finally:
            lt._get_rotation_file_path = original_path

        self.assertIn("Go", summary)
        self.assertIn("next", summary)

    def test_summary_nonexistent_file(self):
        """文件不存在时返回提示"""
        import modules.language_tools as lt
        original_path = lt._get_rotation_file_path
        lt._get_rotation_file_path = lambda: "/nonexistent/file.json"

        try:
            summary = get_rotation_summary()
        finally:
            lt._get_rotation_file_path = original_path

        self.assertIn("未找到", summary)


class TestRealRotationCycle(unittest.TestCase):
    """真实轮换周期测试（模拟 cron 场景）"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "language_rotation.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_cron_scenario_this_hour_rust_next_go(self):
        """
        Cron 场景：本次必须选 Rust，下次选 Go
        模拟当前 current_index=2（实际配置文件值）
        任务要求强制选 Rust，轮换后 index 更新为 1（Go）
        """
        # 模拟实际配置文件状态（current_index=2，即 Swift）
        config = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 2,  # Swift（实际文件中的值）
            "last_language": "Go",
            "updated_at": "2026-06-04T06:00:00+08:00",
        }
        save_rotation_config(config, self.test_file)

        # 加载配置
        loaded = load_rotation_config(self.test_file)
        # 强制选 Rust（本次必选）
        result = rotate_language(loaded, self.test_file, force_language="Rust")

        # 本次选 Rust
        self.assertEqual(result["current_language"], "Rust")
        self.assertEqual(result["current_index"], 0)
        # 下次选 Go
        self.assertEqual(result["next_language"], "Go")
        self.assertEqual(result["next_index"], 1)

        # 验证配置文件中 current_index 已更新为 1（Go）
        with open(self.test_file, "r", encoding="utf-8") as f:
            saved = json.load(f)
        self.assertEqual(saved["current_index"], 1)  # Go
        self.assertEqual(saved["last_language"], "Rust")
        self.assertIn("updated_at", saved)

    def test_normal_rotation_rust_to_go(self):
        """
        正常轮换（不强制）：Rust -> Go -> Swift ...
        """
        config = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 0,  # Rust
            "last_language": "C/C++",
            "updated_at": "2026-06-04T00:00:00+08:00",
        }
        save_rotation_config(config, self.test_file)

        loaded = load_rotation_config(self.test_file)
        result = rotate_language(loaded, self.test_file)

        self.assertEqual(result["current_language"], "Rust")
        self.assertEqual(result["next_language"], "Go")

        with open(self.test_file, "r", encoding="utf-8") as f:
            saved = json.load(f)
        self.assertEqual(saved["current_index"], 1)  # Go

    def test_full_8_language_cycle_with_force(self):
        """
        完整 8 语言循环测试（force_language 模式下每个语言都走一遍）
        """
        languages = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]

        # 从 index=5 (JavaScript) 出发，强制轮换 8 次回到原点
        initial_config = {
            "languages": languages,
            "current_index": 5,
            "last_language": "TypeScript",
            "updated_at": "2026-06-04T00:00:00+08:00",
        }
        save_rotation_config(initial_config, self.test_file)

        expected_order = ["JavaScript", "Java", "C/C++", "Rust", "Go", "Swift", "Kotlin", "TypeScript"]

        for i, expected_lang in enumerate(expected_order):
            loaded = load_rotation_config(self.test_file)
            result = rotate_language(loaded, self.test_file, force_language=expected_lang)

            self.assertEqual(result["current_language"], expected_lang,
                            f"Step {i}: expected {expected_lang}, got {result['current_language']}")
            self.assertEqual(result["current_index"], languages.index(expected_lang))

            # 验证文件已更新
            with open(self.test_file, "r", encoding="utf-8") as f:
                saved = json.load(f)
            next_expected = expected_order[(i + 1) % len(expected_order)]
            self.assertEqual(saved["current_index"], languages.index(next_expected),
                            f"Step {i}: next_index should be {languages.index(next_expected)}, got {saved['current_index']}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
