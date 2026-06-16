"""
test_polyglot_genome.py — Polyglot Genome 单元测试
====================================================================
测试目标：
  1. get_genome_crossing_report() 读取 language_rotation.json，取当前语言
  2. 交叉报告生成后，language_rotation.json 的 current_index 前移一位
  3. 8 次轮换后回到 Rust（完整循环）
  4. 基因组适性值计算正确（3链 × 4因子 = 12位点）
  5. 范式/系统/生态三条链结构正确
  6. get_language_genome() 返回正确结构
  7. get_genome_preview() 不推进索引
  8. format_genome_console() 输出包含关键信息
  9. format_genome_markdown() 输出包含关键信息
  10. cross_genomes() 交叉运算正确
  11. _cross_gene() 显性基因优先
  12. 突变率约 15%
  13. 所有 8 种语言基因组存在且格式正确
  14. list_all_genomes() 返回全部 8 种语言

作者：AllToolkit 全自动生成
====================================================================
"""

import unittest
import unittest.mock
import json
import os
import sys
import tempfile
import math
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_genome import (
    get_genome_crossing_report,
    get_genome_preview,
    get_language_genome,
    cross_genomes,
    format_genome_console,
    format_genome_markdown,
    list_all_genomes,
    _cross_gene,
    _compute_fitness,
    _fitness_label,
    _format_dna_chain,
    _build_genome_ascii,
    LANGUAGE_GENOMES,
    CHAIN_LABELS,
    PARADIGM_KEYS,
    SYSTEM_KEYS,
    ECOSYSTEM_KEYS,
    GENE_EXPRESSION,
)


# ─────────────────────────────────────────────
# 测试数据
# ─────────────────────────────────────────────
_INITIAL_YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

INITIAL_ROTATION_DATA = {
    "languages": [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ],
    "current_index": 0,  # Rust
    "last_language": "C/C++",
    "updated_at": f"{_INITIAL_YESTERDAY}T02:10:00+08:00",
}

# 固定测试时间：2026-06-15 10:00
_FIXED_TIME = datetime(2026, 6, 15, 10, 0, 0)


def _make_temp_json(data: dict = None) -> str:
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_genome_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data or INITIAL_ROTATION_DATA, f, ensure_ascii=False, indent=2)
    return path


# ─────────────────────────────────────────────
# 测试用例
# ─────────────────────────────────────────────

class TestGeneCrossFunction(unittest.TestCase):
    """基因交叉函数测试"""

    def test_cross_gene_dominant_wins(self):
        """显性基因 ✓ 优先于其他"""
        self.assertEqual(_cross_gene("✓", "~"), "✓")
        self.assertEqual(_cross_gene("✓", "✗"), "✓")
        self.assertEqual(_cross_gene("✓", "?"), "✓")

    def test_cross_gene_same_priority(self):
        """相同优先级保持不变"""
        self.assertEqual(_cross_gene("~", "~"), "~")
        self.assertEqual(_cross_gene("?", "?"), "?")
        self.assertEqual(_cross_gene("✗", "✗"), "✗")

    def test_cross_gene_tilde_beats_low(self):
        """~ 中性基因优先于 ✗ 和 ?"""
        self.assertEqual(_cross_gene("~", "✗"), "~")
        self.assertEqual(_cross_gene("~", "?"), "~")

    def test_cross_gene_recessive_beats_question(self):
        """✗ 优先于 ?（显隐性强于未知变异）"""
        self.assertEqual(_cross_gene("✗", "?"), "✗")

    def test_cross_gene_mutation_rate(self):
        """约 15% 触发突变"""
        count = 0
        trials = 1000
        for _ in range(trials):
            result = _cross_gene("✓", "~", force_mutation=True)
            if result == "?":
                count += 1
        # 15% ± 5%
        rate = count / trials
        self.assertGreater(rate, 0.10)
        self.assertLess(rate, 0.20)


class TestFitnessComputation(unittest.TestCase):
    """适性值计算测试"""

    def test_fitness_all_dominant(self):
        """全部显性基因 → 1.0"""
        genome = {
            "paradigm":  ["✓", "✓", "✓", "✓"],
            "system":    ["✓", "✓", "✓", "✓"],
            "ecosystem": ["✓", "✓", "✓", "✓"],
        }
        self.assertAlmostEqual(_compute_fitness(genome), 1.0, places=2)

    def test_fitness_all_recessive(self):
        """全部隐性基因 → 0.1"""
        genome = {
            "paradigm":  ["✗", "✗", "✗", "✗"],
            "system":    ["✗", "✗", "✗", "✗"],
            "ecosystem": ["✗", "✗", "✗", "✗"],
        }
        self.assertAlmostEqual(_compute_fitness(genome), 0.1, places=2)

    def test_fitness_mixed(self):
        """混合基因 → 正确计算"""
        genome = {
            "paradigm":  ["✓", "~", "✗", "?"],
            "system":    ["✓", "✓", "~", "~"],
            "ecosystem": ["?", "?", "?", "?"],
        }
        # (1+0.5+0.1+0.3 + 1+1+0.5+0.5 + 0.3*4) / 12
        expected = (1+0.5+0.1+0.3 + 1+1+0.5+0.5 + 0.3*4) / 12
        self.assertAlmostEqual(_compute_fitness(genome), expected, places=2)

    def test_fitness_label_gold(self):
        """≥0.85 → 黄金基因"""
        self.assertEqual(_fitness_label(0.85), "🏆 黄金基因")
        self.assertEqual(_fitness_label(0.95), "🏆 黄金基因")

    def test_fitness_label_quality(self):
        """≥0.70 → 优质基因"""
        self.assertEqual(_fitness_label(0.70), "✨ 优质基因")
        self.assertEqual(_fitness_label(0.84), "✨ 优质基因")

    def test_fitness_label_normal(self):
        """≥0.55 → 普通基因"""
        self.assertEqual(_fitness_label(0.55), "🔄 普通基因")
        self.assertEqual(_fitness_label(0.69), "🔄 普通基因")

    def test_fitness_label_defect(self):
        """≥0.40 → 缺陷基因"""
        self.assertEqual(_fitness_label(0.40), "⚠️ 缺陷基因")
        self.assertEqual(_fitness_label(0.54), "⚠️ 缺陷基因")

    def test_fitness_label_experimental(self):
        """<0.40 → 实验基因"""
        self.assertEqual(_fitness_label(0.39), "🧪 实验基因")
        self.assertEqual(_fitness_label(0.0), "🧪 实验基因")


class TestLanguageGenomes(unittest.TestCase):
    """语言基因组库测试"""

    def test_all_8_languages_have_genome(self):
        """8 种核心语言都有基因组"""
        expected = ["Rust", "Go", "Swift", "Kotlin",
                    "TypeScript", "JavaScript", "Java", "C/C++"]
        for lang in expected:
            self.assertIn(lang, LANGUAGE_GENOMES, f"{lang} missing genome")

    def test_each_genome_has_3_chains(self):
        """每种语言基因组有 3 条链"""
        for lang, genome in LANGUAGE_GENOMES.items():
            self.assertEqual(len(genome), 3)
            self.assertIn("paradigm", genome)
            self.assertIn("system", genome)
            self.assertIn("ecosystem", genome)

    def test_each_chain_has_4_genes(self):
        """每条链有 4 个基因"""
        valid_genes = {"✓", "~", "✗", "?"}
        for lang, genome in LANGUAGE_GENOMES.items():
            for chain in ["paradigm", "system", "ecosystem"]:
                self.assertEqual(len(genome[chain]), 4, f"{lang}.{chain} must have 4 genes")
                for g in genome[chain]:
                    self.assertIn(g, valid_genes, f"{lang}.{chain} contains invalid gene: {g}")

    def test_chain_labels_exist(self):
        """3 条链都有中文标签"""
        for chain in ["paradigm", "system", "ecosystem"]:
            self.assertIn(chain, CHAIN_LABELS)
            self.assertTrue(len(CHAIN_LABELS[chain]) > 0)


class TestCrossGenomes(unittest.TestCase):
    """基因组交叉测试"""

    def test_cross_rust_go(self):
        """Rust × Go 交叉有结果"""
        result = cross_genomes("Rust", "Go")
        self.assertIn("offspring_genome", result)
        self.assertIn("fitness_score", result)
        self.assertIn("dominance_report", result)
        self.assertIn("mutation_report", result)

    def test_cross_offspring_has_3_chains(self):
        """子代基因组有 3 条链"""
        result = cross_genomes("Rust", "Go")
        offspring = result["offspring_genome"]
        self.assertEqual(len(offspring), 3)
        self.assertIn("paradigm", offspring)
        self.assertIn("system", offspring)
        self.assertIn("ecosystem", offspring)

    def test_cross_offspring_fitness_valid(self):
        """子代适性值在 0~1 之间"""
        result = cross_genomes("Rust", "Go")
        fitness = result["fitness_score"]
        self.assertGreaterEqual(fitness, 0.0)
        self.assertLessEqual(fitness, 1.0)

    def test_cross_dominance_report_complete(self):
        """显性分析报告包含所有链"""
        result = cross_genomes("TypeScript", "JavaScript")
        for chain in ["paradigm", "system", "ecosystem"]:
            self.assertIn(chain, result["dominance_report"])
            dom = result["dominance_report"][chain]
            self.assertIn("winner", dom)
            self.assertIn("a_genes", dom)
            self.assertIn("b_genes", dom)
            self.assertIn("offspring_genes", dom)

    def test_cross_all_language_pairs(self):
        """所有语言两两交叉都能执行"""
        langs = list(LANGUAGE_GENOMES.keys())
        for i, lang_a in enumerate(langs):
            for lang_b in langs[i+1:]:
                result = cross_genomes(lang_a, lang_b)
                self.assertIsInstance(result, dict)
                self.assertIn("offspring_genome", result)


class TestGetLanguageGenome(unittest.TestCase):
    """获取语言基因组测试"""

    def test_get_rust_genome(self):
        """获取 Rust 基因组"""
        result = get_language_genome("Rust")
        self.assertEqual(result["language"], "Rust")
        self.assertIn("genome", result)
        self.assertIn("fitness_score", result)
        self.assertIn("fitness_label", result)
        self.assertIn("genome_ascii", result)

    def test_get_all_language_genomes(self):
        """所有语言基因组都能获取"""
        for lang in LANGUAGE_GENOMES:
            result = get_language_genome(lang)
            self.assertEqual(result["language"], lang)

    def test_invalid_language_raises(self):
        """无效语言抛出 ValueError"""
        with self.assertRaises(ValueError):
            get_language_genome("Python")


class TestGenomeCrossingReport(unittest.TestCase):
    """基因组交叉报告主 API 测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_report_returns_all_required_fields(self):
        """报告返回所有必要字段"""
        result = get_genome_crossing_report(
            json_path=self.test_path, now=_FIXED_TIME
        )
        required = [
            "language_a", "language_b",
            "genome_a", "genome_b",
            "crossing_result",
            "json_updated", "timestamp",
        ]
        for field in required:
            self.assertIn(field, result, f"Missing field: {field}")

    def test_report_language_a_is_rust(self):
        """当前语言为 Rust（index=0）"""
        result = get_genome_crossing_report(
            json_path=self.test_path, now=_FIXED_TIME
        )
        self.assertEqual(result["language_a"], "Rust")

    def test_report_language_b_is_go(self):
        """下一个语言为 Go"""
        result = get_genome_crossing_report(
            json_path=self.test_path, now=_FIXED_TIME
        )
        self.assertEqual(result["language_b"], "Go")

    def test_report_json_advances_index(self):
        """报告生成后，current_index 前移一位"""
        get_genome_crossing_report(json_path=self.test_path, now=_FIXED_TIME)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 1)  # Rust(0) → Go(1)

    def test_report_json_updates_timestamp(self):
        """报告生成后，updated_at 更新"""
        with open(self.test_path, "r", encoding="utf-8") as f:
            before = json.load(f)["updated_at"]
        get_genome_crossing_report(json_path=self.test_path, now=_FIXED_TIME)
        with open(self.test_path, "r", encoding="utf-8") as f:
            after = json.load(f)["updated_at"]
        self.assertNotEqual(before, after)

    def test_report_json_records_last_language(self):
        """last_language 记录上一轮换的语言"""
        get_genome_crossing_report(json_path=self.test_path, now=_FIXED_TIME)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["last_language"], "Rust")


class TestGenomePreview(unittest.TestCase):
    """基因组预览（不推进索引）测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_preview_does_not_advance_index(self):
        """预览不改变 current_index"""
        with open(self.test_path, "r", encoding="utf-8") as f:
            before = json.load(f)["current_index"]
        get_genome_preview(json_path=self.test_path, now=_FIXED_TIME)
        with open(self.test_path, "r", encoding="utf-8") as f:
            after = json.load(f)["current_index"]
        self.assertEqual(before, after)

    def test_preview_returns_correct_fields(self):
        """预览返回正确字段"""
        result = get_genome_preview(json_path=self.test_path, now=_FIXED_TIME)
        self.assertIn("language", result)
        self.assertIn("genome", result)
        self.assertIn("timestamp", result)


class TestFormatGenomeConsole(unittest.TestCase):
    """控制台格式化测试"""

    def test_console_format_contains_languages(self):
        """格式输出包含两种语言名称"""
        result = get_genome_crossing_report(now=_FIXED_TIME)
        output = format_genome_console(result)
        self.assertIn("Polyglot Genome", output)
        self.assertIn(result["language_a"], output)
        self.assertIn(result["language_b"], output)

    def test_console_format_contains_chains(self):
        """格式输出包含 3 条链标签"""
        result = get_genome_crossing_report(now=_FIXED_TIME)
        output = format_genome_console(result)
        self.assertIn("范式基因链", output)
        self.assertIn("系统基因链", output)
        self.assertIn("生态基因链", output)

    def test_console_format_contains_fitness(self):
        """格式输出包含适性值"""
        result = get_genome_crossing_report(now=_FIXED_TIME)
        output = format_genome_console(result)
        self.assertIn("适性", output)


class TestFormatGenomeMarkdown(unittest.TestCase):
    """Markdown 格式化测试"""

    def test_markdown_format_contains_languages(self):
        """Markdown 输出包含语言名称"""
        result = get_genome_crossing_report(now=_FIXED_TIME)
        output = format_genome_markdown(result)
        self.assertIn("语言基因组交叉报告", output)
        self.assertIn(result["language_a"], output)

    def test_markdown_format_contains_genome_table(self):
        """Markdown 输出包含基因组表格"""
        result = get_genome_crossing_report(now=_FIXED_TIME)
        output = format_genome_markdown(result)
        self.assertIn("范式", output)
        self.assertIn("系统", output)
        self.assertIn("生态", output)


class TestListAllGenomes(unittest.TestCase):
    """列出所有基因组测试"""

    def test_list_all_returns_8_languages(self):
        """返回 8 种语言"""
        result = list_all_genomes()
        self.assertEqual(len(result), 8)

    def test_list_all_contains_all_languages(self):
        """返回包含所有核心语言"""
        expected = ["Rust", "Go", "Swift", "Kotlin",
                    "TypeScript", "JavaScript", "Java", "C/C++"]
        result = list_all_genomes()
        for lang in expected:
            self.assertIn(lang, result)


class TestGenomeRotationCycle(unittest.TestCase):
    """完整轮换一圈测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_full_rotation_cycle(self):
        """8 次轮换后回到 Rust"""
        languages_seen = []
        for i in range(8):
            result = get_genome_crossing_report(
                json_path=self.test_path, now=_FIXED_TIME
            )
            languages_seen.append(result["language_a"])

        expected = ["Rust", "Go", "Swift", "Kotlin",
                    "TypeScript", "JavaScript", "Java", "C/C++"]
        self.assertEqual(languages_seen, expected)

    def test_no_repeated_language_in_one_cycle(self):
        """一轮（8次）中每种语言只出现一次"""
        languages_seen = []
        for i in range(8):
            result = get_genome_crossing_report(
                json_path=self.test_path, now=_FIXED_TIME
            )
            languages_seen.append(result["language_a"])

        self.assertEqual(len(set(languages_seen)), 8)


class TestGenomeHelperFunctions(unittest.TestCase):
    """辅助函数测试"""

    def test_format_dna_chain(self):
        """DNA 链格式化正确"""
        chain = ["✓", "~", "✗", "?"]
        result = _format_dna_chain(chain)
        self.assertEqual(result, "✓ ~ ✗ ?")

    def test_build_genome_ascii(self):
        """ASCII 基因组图生成"""
        genome = {
            "paradigm":  ["✓", "~", "✗", "?"],
            "system":    ["✓", "✓", "~", "~"],
            "ecosystem": ["?", "?", "?", "?"],
        }
        result = _build_genome_ascii(genome)
        self.assertIsInstance(result, str)
        self.assertIn("范式", result)
        self.assertIn("系统", result)
        self.assertIn("生态", result)
        self.assertIn("①", result)
        self.assertIn("②", result)
        self.assertIn("③", result)
        self.assertIn("④", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
