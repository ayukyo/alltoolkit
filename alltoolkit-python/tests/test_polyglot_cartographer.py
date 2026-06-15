"""
AllToolkit polyglot_cartographer 测试套件
"""

import unittest
import json
import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_cartographer import (
    generate_map,
    format_map_markdown,
    format_map_console,
    CARTOGRAPHER_DB,
    DEFAULT_LANGUAGE_ROTATION_JSON,
)


EXPECTED_LANGUAGES = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# 初始测试数据：current_index=3 → 当前语言 Kotlin
_INITIAL_YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
INITIAL_TEST_DATA = {
    "languages": EXPECTED_LANGUAGES,
    "current_index": 3,
    "last_language": "Swift",
    "updated_at": f"{_INITIAL_YESTERDAY}T02:10:00+08:00",
}


def _make_temp_json():
    """每个测试用例使用独立的临时文件，避免状态污染"""
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_cartographer_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)
    return path


class TestPolyglotCartographer(unittest.TestCase):
    """polyglot_cartographer 单元测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    # ── CARTOGRAPHER_DB ────────────────────────

    def test_all_languages_in_db(self):
        """所有 8 种语言都在数据库中"""
        for lang in EXPECTED_LANGUAGES:
            self.assertIn(lang, CARTOGRAPHER_DB)

    def test_db_has_required_keys(self):
        """数据库每种语言包含所有必要字段"""
        required = {
            "emoji", "ecosystem_map", "entry_point",
            "naming_conventions", "dependency_style",
            "project_sketch", "key_locations", "trivia",
        }
        for lang, data in CARTOGRAPHER_DB.items():
            self.assertTrue(
                required.issubset(data.keys()),
                f"{lang} 缺少字段，缺少：{required - data.keys()}"
            )

    def test_naming_conventions_has_required_categories(self):
        """每种语言的 naming_conventions 包含主要类别"""
        required_categories = {"file", "function", "variable", "type"}
        for lang, data in CARTOGRAPHER_DB.items():
            naming = data.get("naming_conventions", {})
            self.assertTrue(
                required_categories.issubset(naming.keys()),
                f"{lang} 的 naming_conventions 缺少类别，缺少：{required_categories - naming.keys()}"
            )

    def test_project_sketch_not_empty(self):
        """每种语言都有非空项目草图"""
        for lang, data in CARTOGRAPHER_DB.items():
            sketch = data.get("project_sketch", [])
            self.assertTrue(len(sketch) > 3, f"{lang} 的 project_sketch 为空或太少")

    def test_key_locations_not_empty(self):
        """每种语言都有关键位置标注"""
        for lang, data in CARTOGRAPHER_DB.items():
            locs = data.get("key_locations", [])
            self.assertTrue(len(locs) >= 3, f"{lang} 的 key_locations 少于 3 条")

    # ── generate_map ────────────────────────────

    def test_generate_map_returns_all_fields(self):
        """generate_map 返回所有必要字段"""
        result = generate_map(json_path=self.test_path)
        required = {
            "language", "emoji", "ecosystem_map", "entry_point",
            "naming_conventions", "dependency_style",
            "project_sketch", "key_locations", "trivia", "generated_at",
        }
        self.assertTrue(
            required.issubset(result.keys()),
            f"缺少字段：{required - result.keys()}"
        )

    def test_generate_map_current_language(self):
        """当前语言应为 Kotlin（index=3）"""
        result = generate_map(json_path=self.test_path)
        self.assertEqual(result["language"], "Kotlin")
        self.assertEqual(result["emoji"], "🟣")

    def test_generate_map_ecosystem_map_not_empty(self):
        """ecosystem_map 非空"""
        result = generate_map(json_path=self.test_path)
        self.assertTrue(len(result["ecosystem_map"]) > 50)

    def test_generate_map_naming_conventions_dict(self):
        """naming_conventions 是字典"""
        result = generate_map(json_path=self.test_path)
        self.assertIsInstance(result["naming_conventions"], dict)
        self.assertIn("file", result["naming_conventions"])

    def test_generate_map_project_sketch_list(self):
        """project_sketch 是列表"""
        result = generate_map(json_path=self.test_path)
        self.assertIsInstance(result["project_sketch"], list)
        self.assertTrue(len(result["project_sketch"]) > 3)

    def test_generate_map_key_locations_list(self):
        """key_locations 是列表"""
        result = generate_map(json_path=self.test_path)
        self.assertIsInstance(result["key_locations"], list)
        self.assertTrue(len(result["key_locations"]) >= 3)

    def test_generate_map_trivia_not_empty(self):
        """trivia 非空"""
        result = generate_map(json_path=self.test_path)
        self.assertTrue(len(result["trivia"]) > 20)

    def test_generate_map_generated_at_format(self):
        """generated_at 格式正确"""
        result = generate_map(json_path=self.test_path)
        # 验证格式，不崩溃
        dt = datetime.strptime(result["generated_at"].replace("+08:00", ""), "%Y-%m-%dT%H:%M:%S")
        self.assertIsInstance(dt, datetime)

    # ── format_map_markdown ────────────────────

    def test_format_markdown_contains_language(self):
        """Markdown 报告包含语言名称"""
        result = generate_map(json_path=self.test_path)
        md = format_map_markdown(result=result)
        self.assertIn("Kotlin", md)

    def test_format_markdown_contains_sections(self):
        """Markdown 报告包含主要章节"""
        result = generate_map(json_path=self.test_path)
        md = format_map_markdown(result=result)
        self.assertIn("生态系统拓扑图", md)
        self.assertIn("入口点定位", md)
        self.assertIn("命名Convention光谱", md)
        self.assertIn("依赖管理方式", md)
        self.assertIn("典型项目目录草图", md)
        self.assertIn("语言必去之地", md)
        self.assertIn("代码地理趣闻", md)

    def test_format_markdown_contains_naming_details(self):
        """Markdown 报告包含命名惯例详情"""
        result = generate_map(json_path=self.test_path)
        md = format_map_markdown(result=result)
        self.assertIn("文件", md)
        self.assertIn("函数", md)
        self.assertIn("类型", md)

    def test_format_markdown_contains_key_location(self):
        """Markdown 报告包含关键位置标注"""
        result = generate_map(json_path=self.test_path)
        md = format_map_markdown(result=result)
        self.assertIn("build.gradle", md)

    # ── format_map_console ─────────────────────

    def test_format_console_contains_language(self):
        """Console 报告包含语言名称"""
        result = generate_map(json_path=self.test_path)
        console = format_map_console(result=result)
        self.assertIn("Kotlin", console)

    def test_format_console_contains_naming(self):
        """Console 报告包含命名惯例"""
        result = generate_map(json_path=self.test_path)
        console = format_map_console(result=result)
        self.assertIn("文件", console)
        self.assertIn("函数", console)

    def test_format_console_contains_project_sketch(self):
        """Console 报告包含项目草图"""
        result = generate_map(json_path=self.test_path)
        console = format_map_console(result=result)
        self.assertIn("build.gradle", console)

    def test_format_console_contains_trivia(self):
        """Console 报告包含趣闻"""
        result = generate_map(json_path=self.test_path)
        console = format_map_console(result=result)
        self.assertIn("趣闻", console)

    # ── 全语言验证 ──────────────────────────────

    def test_all_languages_have_valid_emoji(self):
        """每种语言都有 emoji"""
        for lang in EXPECTED_LANGUAGES:
            emoji = CARTOGRAPHER_DB[lang]["emoji"]
            self.assertTrue(len(emoji) > 0)

    def test_all_languages_have_entry_point(self):
        """每种语言都有入口点描述"""
        for lang in EXPECTED_LANGUAGES:
            ep = CARTOGRAPHER_DB[lang]["entry_point"]
            self.assertTrue(len(ep) > 5)

    def test_all_languages_have_dependency_style(self):
        """每种语言都有依赖管理方式描述"""
        for lang in EXPECTED_LANGUAGES:
            dep = CARTOGRAPHER_DB[lang]["dependency_style"]
            self.assertTrue(len(dep) > 20)

    def test_all_languages_have_unique_entry_point(self):
        """每种语言的入口点描述各不相同（不重复）"""
        eps = set()
        for lang in EXPECTED_LANGUAGES:
            ep = CARTOGRAPHER_DB[lang]["entry_point"]
            self.assertNotIn(ep, eps, f"{lang} 的 entry_point 与其他语言重复")
            eps.add(ep)


class TestPolyglotCartographerIntegration(unittest.TestCase):
    """polyglot_cartographer 集成测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_generate_map_for_all_languages(self):
        """为每种语言生成报告，验证都有内容"""
        data = json.load(open(self.test_path, encoding="utf-8"))
        languages = data["languages"]

        for lang in languages:
            # 临时修改 JSON 的 current_index
            with open(self.test_path, "w", encoding="utf-8") as f:
                idx = languages.index(lang)
                data["current_index"] = idx
                json.dump(data, f, ensure_ascii=False, indent=2)

            result = generate_map(json_path=self.test_path)
            self.assertEqual(result["language"], lang)
            self.assertIn("ecosystem_map", result)
            self.assertTrue(len(result["ecosystem_map"]) > 50)
            self.assertIn("naming_conventions", result)
            self.assertTrue(len(result["project_sketch"]) > 3)
            self.assertTrue(len(result["key_locations"]) >= 3)

    def test_markdown_and_console_format_differ(self):
        """Markdown 和 Console 格式输出内容不同（格式不同）"""
        result = generate_map(json_path=self.test_path)
        md = format_map_markdown(result=result)
        console = format_map_console(result=result)
        # 两者内容应不完全相同（格式不同）
        self.assertNotEqual(md, console)

    def test_key_locations_are_tuples(self):
        """key_locations 每项都是 (文件名, 描述) 元组"""
        for lang in EXPECTED_LANGUAGES:
            locs = CARTOGRAPHER_DB[lang]["key_locations"]
            for loc in locs:
                self.assertIsInstance(loc, (list, tuple), f"{lang} 的 key_locations 包含非元组项")
                self.assertEqual(len(loc), 2, f"{lang} 的 key_locations 元组长度不为 2")


if __name__ == "__main__":
    unittest.main(verbosity=2)