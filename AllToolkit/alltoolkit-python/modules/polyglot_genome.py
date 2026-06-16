"""
polyglot_genome.py — 编程语言基因组序列仪 (Polyglot Genome Sequencer)
====================================================================
将每种编程语言映射为独特的 DNA 基因组序列，
在语言轮换时执行「基因交叉」运算，生成遗传分析报告。

核心创意：语言不是工具，而是「物种」——
每种语言有其独特的基因密码（Paradigm-DNA），
当两种语言的基因链接触时，会产生「适者生存」的分析：
哪些基因强强联合，哪些基因冲突，哪些基因突变。

基因组成（每种语言 3 条链，每链 4 遗传因子）：
  - 🔹 范式基因链（Paradigm DNA）：OOP/FP/Procedural/Declarative/Actor/Functional...
  - 🔸 系统基因链（System DNA）：Memory/Concurrency/Type/Compilation...
  - 🔶 生态基因链（Ecosystem DNA）：Tooling/Community/Library/Platform...

基因交叉（Crossing）运算：
  - 显性基因：冲突时取强势方
  - 隐性基因：弱强联合时表现
  - 突变：某些组合触发新特性表达

与 language_rotation.json 深度集成：
  1. 读取 language_rotation.json，获取 current_index 和当前语言
  2. 执行基因组交叉运算，生成遗传分析报告
  3. 更新 current_index 前移一位，更新 updated_at

语言轮换顺序（8 种核心语言）：
  Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust（循环）

Distinct from existing modules:
  - polyglot_pulse:         语言脉搏（活跃度/心电图）
  - polyglot_resonator:     语言共振（频率/波形图）
  - polyglot_sentinel:      学习健康（雷达图/平衡监测）
  - polyglot_archetype_canvas: 语言角色原神（命之座/运势）
  - polyglot_companion:     学习伴侣
  - polyglot_quiz:         语言身份猜谜
  - polyglot_codex:        韬略宝鉴
  - polyglot_ink:          每日墨讯
  - polyglot_snippet_vault: 片段知识库
  - polyglot_cartographer:  语言生态系统地图

Polyglot Genome 的独特视角：
  不是教你写代码，不是练习题，而是——
  把语言当作生物物种，用遗传学的眼光看语言的「基因优势」。
  Rust 的所有权基因 + Go 的并发基因 → 最强系统语言组合
  JavaScript 的动态基因 × Java 的类型基因 → TypeScript 的基因突变

作者：AllToolkit 全自动生成
依赖：仅 Python 标准库（json, datetime, pathlib, random）
====================================================================
"""

import json
import os
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ─────────────────────────────────────────────
# 路径配置
# ─────────────────────────────────────────────
_MODULE_DIR = Path(__file__).parent.parent              # alltoolkit-python/
_WORKSPACE_ROOT = _MODULE_DIR.parent                   # workspace/
DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")


# ─────────────────────────────────────────────
# 语言基因组定义（每种语言 3 条链，每链 4 遗传因子）
# 基因符号字典：Paradigm / System / Ecosystem
# ─────────────────────────────────────────────

# 范式基因（Paradigm DNA）— 4 个因子位置
PARADIGM_KEYS = ["structural", "object_oriented", "functional", "declarative"]

# 系统基因（System DNA）— 4 个因子位置
SYSTEM_KEYS = ["memory_safety", "concurrency", "typing", "compilation"]

# 生态基因（Ecosystem DNA）— 4 个因子位置
ECOSYSTEM_KEYS = ["tooling", "community", "library", "platform"]

# 遗传因子定义
GENETIC_FACTORS: Dict[str, List[str]] = {
    # 范式
    "structural":      ["✓", "~", "✗", "?"],   # 结构化
    "object_oriented": ["✓", "~", "✗", "?"],   # 面向对象
    "functional":      ["✓", "~", "✗", "?"],   # 函数式
    "declarative":      ["✓", "~", "✗", "?"],   # 声明式
    # 系统
    "memory_safety":   ["✓", "~", "✗", "?"],   # 内存安全
    "concurrency":     ["✓", "~", "✗", "?"],   # 并发模型
    "typing":           ["✓", "~", "✗", "?"],   # 类型系统
    "compilation":      ["✓", "~", "✗", "?"],   # 编译方式
    # 生态
    "tooling":         ["✓", "~", "✗", "?"],   # 工具链成熟度
    "community":       ["✓", "~", "✗", "?"],   # 社区活跃度
    "library":         ["✓", "~", "✗", "?"],   # 库生态
    "platform":        ["✓", "~", "✗", "?"],   # 平台支持
}

# ✓ = 显性（强表达） ~ = 中性  ✗ = 隐性（弱表达）  ? = 未知/变异


# 语言基因组库（3链 × 4因子 = 12 基因位点）
LANGUAGE_GENOMES: Dict[str, Dict[str, List[str]]] = {
    "Rust": {
        "paradigm":  ["✓", "~", "✓", "~"],   # 强结构+强函数式
        "system":    ["✓", "✓", "✓", "✓"],   # 全强系统基因
        "ecosystem": ["~", "✓", "~", "~"],   # 中等生态
    },
    "Go": {
        "paradigm":  ["~", "~", "✓", "~"],   # 轻量函数式
        "system":    ["~", "✓", "~", "✓"],   # 强并发+编译
        "ecosystem": ["✓", "✓", "✓", "~"],   # 强工具+社区
    },
    "Swift": {
        "paradigm":  ["~", "✓", "✓", "~"],   # OOP+函数式
        "system":    ["✓", "~", "✓", "✓"],   # 内存安全+强类型
        "ecosystem": ["~", "✓", "✓", "✓"],   # Apple生态强
    },
    "Kotlin": {
        "paradigm":  ["~", "✓", "✓", "~"],   # OOP+函数式
        "system":    ["~", "~", "✓", "~"],   # JVM类型系统
        "ecosystem": ["~", "✓", "✓", "~"],   # Android生态
    },
    "TypeScript": {
        "paradigm":  ["✓", "✓", "~", "✓"],   # 结构化+OOP+声明式
        "system":    ["~", "~", "✓", "~"],   # 渐进式类型
        "ecosystem": ["✓", "✓", "✓", "✓"],   # JS生态全覆盖
    },
    "JavaScript": {
        "paradigm":  ["✓", "~", "~", "✓"],   # 结构化+声明式
        "system":    ["✗", "~", "✗", "~"],   # 动态弱类型
        "ecosystem": ["✓", "✓", "✓", "✓"],   # 最强生态
    },
    "Java": {
        "paradigm":  ["~", "✓", "~", "~"],   # 纯OOP
        "system":    ["✗", "~", "✓", "~"],   # JVM类型系统，无内存安全
        "ecosystem": ["✓", "✓", "✓", "✓"],   # 成熟生态
    },
    "C/C++": {
        "paradigm":  ["✓", "~", "~", "~"],   # 纯结构化
        "system":    ["✗", "~", "~", "✓"],   # 手动内存，无类型安全
        "ecosystem": ["✓", "✓", "✓", "~"],   # 系统级生态
    },
}

# 基因表达强度映射
GENE_EXPRESSION: Dict[str, float] = {
    "✓": 1.0,   # 显性
    "~": 0.5,   # 中性
    "✗": 0.1,   # 隐性
    "?": 0.3,   # 变异
}

# 链名称（中文标签）
CHAIN_LABELS: Dict[str, str] = {
    "paradigm":  "🧬 范式基因链",
    "system":    "⚙️  系统基因链",
    "ecosystem": "🌐 生态基因链",
}


# ─────────────────────────────────────────────
# 基因交叉运算
# ─────────────────────────────────────────────

def _cross_gene(a: str, b: str, force_mutation: bool = False) -> str:
    """
    两个基因位点交叉，返回显性表达。
    
    规则：
      - ✓ > ~ > ✗ > ?（显性优先）
      - 相同则保持
      - force_mutation=True 时有 15% 概率触发突变（→ ?）
    """
    if force_mutation and random.random() < 0.15:
        return "?"
    
    priority = {"✓": 4, "~": 3, "✗": 2, "?": 1}
    if priority.get(a, 0) >= priority.get(b, 0):
        return a
    return b


def _compute_fitness(genome: Dict[str, List[str]]) -> float:
    """
    根据 3 条链的基因计算语言「基因适性值」（0.0 ~ 1.0）。
    """
    total = 0.0
    count = 0
    for chain_name, genes in genome.items():
        for gene in genes:
            total += GENE_EXPRESSION.get(gene, 0.3)
            count += 1
    return total / count if count > 0 else 0.0


def cross_genomes(lang_a: str, lang_b: str) -> Dict[str, Any]:
    """
    对两种语言的基因组执行交叉运算，返回：
      - offspring_genome: 交叉后的子代基因组
      - fitness_score: 适性值
      - dominance_report: 每条链的显性分析
      - mutation_report: 突变位点列表
      - synergy_genes: 协同增强的基因
      - conflict_genes: 冲突的基因
    """
    ga = LANGUAGE_GENOMES.get(lang_a, {})
    gb = LANGUAGE_GENOMES.get(lang_b, {})

    offspring = {}
    dominance_report = {}
    mutation_report = []
    synergy_genes = []
    conflict_genes = []

    for chain in ["paradigm", "system", "ecosystem"]:
        genes_a = ga.get(chain, ["?", "?", "?", "?"])
        genes_b = gb.get(chain, ["?", "?", "?", "?"])
        
        crossed = []
        dom_count_a = 0
        dom_count_b = 0
        
        for i in range(4):
            gene_a = genes_a[i]
            gene_b = genes_b[i]
            
            # 强制突变：约 15%
            force_mut = random.random() < 0.15
            result = _cross_gene(gene_a, gene_b, force_mutation=force_mut)
            
            if force_mut and result == "?":
                mutation_report.append({
                    "chain": chain,
                    "position": i,
                    "parent_a": gene_a,
                    "parent_b": gene_b,
                })
            
            if result == gene_a and result == gene_b and result == "✓":
                synergy_genes.append(f"{chain}:{i}")
            elif result != gene_a and result != gene_b:
                conflict_genes.append(f"{chain}:{i}")
            
            if GENE_EXPRESSION.get(gene_a, 0) > GENE_EXPRESSION.get(gene_b, 0):
                dom_count_a += 1
            elif GENE_EXPRESSION.get(gene_b, 0) > GENE_EXPRESSION.get(gene_a, 0):
                dom_count_b += 1
            
            crossed.append(result)
        
        offspring[chain] = crossed
        
        winner = lang_a if dom_count_a > dom_count_b else lang_b if dom_count_b > dom_count_a else "equal"
        dominance_report[chain] = {
            "winner": winner,
            "a_genes": genes_a,
            "b_genes": genes_b,
            "offspring_genes": crossed,
        }

    fitness = _compute_fitness(offspring)

    return {
        "offspring_genome": offspring,
        "fitness_score": round(fitness, 3),
        "fitness_label": _fitness_label(fitness),
        "dominance_report": dominance_report,
        "mutation_report": mutation_report,
        "synergy_genes": synergy_genes,
        "conflict_genes": conflict_genes,
    }


def _fitness_label(score: float) -> str:
    """将适性值映射为描述标签。"""
    if score >= 0.85:
        return "🏆 黄金基因"
    elif score >= 0.70:
        return "✨ 优质基因"
    elif score >= 0.55:
        return "🔄 普通基因"
    elif score >= 0.40:
        return "⚠️ 缺陷基因"
    else:
        return "🧪 实验基因"


def _format_dna_chain(chain_genes: List[str]) -> str:
    """将 4 个基因格式化为 DNA 链视觉字符串。"""
    return " ".join(chain_genes)


def _build_genome_ascii(genome: Dict[str, List[str]]) -> str:
    """为基因组生成 ASCII 双螺旋图。"""
    lines = []
    
    # 列标题
    paradigm = genome.get("paradigm", ["?", "?", "?", "?"])
    system = genome.get("system", ["?", "?", "?", "?"])
    ecosystem = genome.get("ecosystem", ["?", "?", "?", "?"])
    
    # 双螺旋骨架（简化为 4 个位点）
    #    P       S       E
    #   ╭─╮     ╭─╮     ╭─╮
    #   │✓│────│~│────│✓│
    #   ╰─╯     ╰─╯     ╰─╯
    
    lines.append("       🧬 范式链      ⚙️ 系统链      🌐 生态链")
    lines.append("      ╭───┬───┬───╮  ╭───┬───┬───╮  ╭───┬───┬───╮")
    
    positions = ["①", "②", "③", "④"]
    for i in range(4):
        p = paradigm[i]
        s = system[i]
        e = ecosystem[i]
        lines.append(f"  {positions[i]}  │{p} │{s} │{e} │")
        if i < 3:
            lines.append("      ├───┼───┼───┤  ├───┼───┼───┤  ├───┼───┼───┤")
    
    lines.append("      ╰───┴───┴───╯  ╰───┴───┴───╯  ╰───┴───┴───╯")
    
    return "\n".join(lines)


# ─────────────────────────────────────────────
# 辅助函数
# ─────────────────────────────────────────────

def _read_json(path: str) -> Optional[Dict[str, Any]]:
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def _write_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_language_genome(language: str) -> Dict[str, Any]:
    """获取指定语言的完整基因组数据。"""
    if language not in LANGUAGE_GENOMES:
        raise ValueError(f"Language '{language}' not in genome library")
    
    genome = LANGUAGE_GENOMES[language]
    fitness = _compute_fitness(genome)
    
    return {
        "language": language,
        "genome": genome,
        "fitness_score": round(fitness, 3),
        "fitness_label": _fitness_label(fitness),
        "genome_ascii": _build_genome_ascii(genome),
    }


# ─────────────────────────────────────────────
# 主 API
# ─────────────────────────────────────────────

def get_genome_crossing_report(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    生成语言基因组交叉报告。

    步骤：
      1. 读取 language_rotation.json，获取 current_index
      2. 取当前语言 lang_a 和下一个语言 lang_b
      3. 执行基因组交叉运算
      4. 推进 current_index，更新 updated_at

    Returns:
        {
            "language_a": str,        # 当前语言
            "language_b": str,        # 下一个语言
            "genome_a": {...},        # lang_a 基因组
            "genome_b": {...},        # lang_b 基因组
            "crossing_result": {...}, # 交叉结果
            "json_updated": bool,
            "timestamp": str,
        }
    """
    if now is None:
        now = datetime.now()

    # 读取 language_rotation.json
    data = _read_json(json_path)
    if data is None:
        raise FileNotFoundError(f"Cannot find {json_path}")

    languages = data["languages"]
    idx = data.get("current_index", 0) % len(languages)
    next_idx = (idx + 1) % len(languages)

    lang_a = languages[idx]
    lang_b = languages[next_idx]

    # 获取两种语言的基因组
    genome_a = get_language_genome(lang_a)
    genome_b = get_language_genome(lang_b)

    # 执行基因交叉
    crossing = cross_genomes(lang_a, lang_b)

    # 更新 language_rotation.json
    data["current_index"] = next_idx
    data["last_language"] = lang_a
    data["updated_at"] = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
    _write_json(json_path, data)

    return {
        "language_a": lang_a,
        "language_b": lang_b,
        "genome_a": genome_a,
        "genome_b": genome_b,
        "crossing_result": crossing,
        "json_updated": True,
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


def get_genome_preview(
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    预览基因组数据（不推进索引）。
    """
    if now is None:
        now = datetime.now()

    data = _read_json(json_path)
    if data is None:
        raise FileNotFoundError(f"Cannot find {json_path}")

    languages = data["languages"]
    idx = data.get("current_index", 0) % len(languages)
    lang = languages[idx]

    genome = get_language_genome(lang)

    return {
        "language": lang,
        "genome": genome,
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


def format_genome_console(report: Dict[str, Any]) -> str:
    """将基因组报告格式化为友好的控制台输出。"""
    lang_a = report["language_a"]
    lang_b = report["language_b"]
    ga = report["genome_a"]
    gb = report["genome_b"]
    cr = report["crossing_result"]

    lines = [
        f"  ╔══════════════════════════════════════════════════════════╗",
        f"  ║  🧬 Polyglot Genome — 编程语言基因组序列仪                ║",
        f"  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  交叉实验：{lang_a} × {lang_b:<8}                          ║",
        f"  ╠══════════════════════════════════════════════════════════╣",
    ]

    # 父本基因组 A
    lines.append(f"  ║  🧬 父本 A：{lang_a}（{ga['fitness_label']} {ga['fitness_score']}）        ║")
    for chain in ["paradigm", "system", "ecosystem"]:
        label = CHAIN_LABELS[chain]
        genes = ga["genome"][chain]
        line_str = _format_dna_chain(genes)
        lines.append(f"  ║      {label}: {line_str}            ║")

    lines.append(f"  ╠══════════════════════════════════════════════════════════╣")

    # 父本基因组 B
    lines.append(f"  ║  🧬 父本 B：{lang_b}（{gb['fitness_label']} {gb['fitness_score']}）        ║")
    for chain in ["paradigm", "system", "ecosystem"]:
        label = CHAIN_LABELS[chain]
        genes = gb["genome"][chain]
        line_str = _format_dna_chain(genes)
        lines.append(f"  ║      {label}: {line_str}            ║")

    lines.append(f"  ╠══════════════════════════════════════════════════════════╣")

    # 交叉结果
    fitness = cr["fitness_score"]
    fitness_label = cr["fitness_label"]
    lines.append(f"  ║  🧪 子代基因组（{fitness_label} 适性: {fitness}）        ║")

    offspring_genome = cr["offspring_genome"]
    for chain in ["paradigm", "system", "ecosystem"]:
        label = CHAIN_LABELS[chain]
        genes = offspring_genome[chain]
        line_str = _format_dna_chain(genes)
        lines.append(f"  ║      {label}: {line_str}            ║")

    lines.append(f"  ╠══════════════════════════════════════════════════════════╣")

    # 突变
    mutations = cr["mutation_report"]
    if mutations:
        lines.append(f"  ║  ⚠️ 突变位点：{len(mutations)} 处                                ║")
        for m in mutations[:3]:
            chain_label = CHAIN_LABELS[m["chain"]].split()[0]
            lines.append(
                f"  ║    · {chain_label} 第{m['position']+1}位: {m['parent_a']}+{m['parent_b']} → ?                ║"
            )
    else:
        lines.append(f"  ║  ✅ 无突变位点（稳定遗传）                           ║")

    # 协同与冲突
    synergy = cr["synergy_genes"]
    conflicts = cr["conflict_genes"]
    if synergy:
        lines.append(f"  ║  ✨ 协同增强：{len(synergy)} 处                               ║")
    if conflicts:
        lines.append(f"  ║  ⚡ 基因冲突：{len(conflicts)} 处                              ║")

    lines.append(f"  ╠══════════════════════════════════════════════════════════╣")
    lines.append(f"  ║  📋 显性分析                                         ║")
    for chain in ["paradigm", "system", "ecosystem"]:
        dom = cr["dominance_report"][chain]
        winner = dom["winner"]
        lines.append(
            f"  ║    {CHAIN_LABELS[chain]}: {winner} 显性              ║"
        )

    lines += [
        f"  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  ⏭️  轮换: {lang_a} → {lang_b}                              ║",
        f"  ╚══════════════════════════════════════════════════════════╝",
    ]

    return "\n".join(lines)


def format_genome_markdown(report: Dict[str, Any]) -> str:
    """将基因组报告格式化为 Markdown。"""
    lang_a = report["language_a"]
    lang_b = report["language_b"]
    ga = report["genome_a"]
    gb = report["genome_b"]
    cr = report["crossing_result"]

    lines = [
        f"# 🧬 语言基因组交叉报告",
        "",
        f"**时刻**：{report['timestamp']}（北京时间）",
        "",
        f"## 🧬 父本 A：{lang_a}",
        "",
        f"- **适性值**：{ga['fitness_score']} — {ga['fitness_label']}",
        "",
        f"| 基因链 | ① | ② | ③ | ④ |",
        f"|--------|---|---|---|---|---|",
    ]

    for chain in ["paradigm", "system", "ecosystem"]:
        label = CHAIN_LABELS[chain].split()[1]  # 取中文名
        genes = ga["genome"][chain]
        lines.append(f"| {label} | {' | '.join(genes)} |")

    lines += [
        "",
        f"## 🧬 父本 B：{lang_b}",
        "",
        f"- **适性值**：{gb['fitness_score']} — {gb['fitness_label']}",
        "",
        f"| 基因链 | ① | ② | ③ | ④ |",
        f"|--------|---|---|---|---|---|",
    ]

    for chain in ["paradigm", "system", "ecosystem"]:
        label = CHAIN_LABELS[chain].split()[1]
        genes = gb["genome"][chain]
        lines.append(f"| {label} | {' | '.join(genes)} |")

    # 子代
    offspring_genome = cr["offspring_genome"]
    lines += [
        "",
        f"## 🧪 子代基因组",
        "",
        f"- **适性值**：{cr['fitness_score']} — {cr['fitness_label']}",
        "",
        f"| 基因链 | ① | ② | ③ | ④ |",
        f"|--------|---|---|---|---|---|",
    ]

    for chain in ["paradigm", "system", "ecosystem"]:
        label = CHAIN_LABELS[chain].split()[1]
        genes = offspring_genome[chain]
        lines.append(f"| {label} | {' | '.join(genes)} |")

    # 突变
    mutations = cr["mutation_report"]
    if mutations:
        lines += [
            "",
            f"## ⚠️ 突变位点（共 {len(mutations)} 处）",
            "",
        ]
        for m in mutations:
            chain_label = CHAIN_LABELS[m["chain"]].split()[1]
            lines.append(
                f"- {chain_label} 第{m['position']+1}位：{m['parent_a']} + {m['parent_b']} → **?**（突变）"
            )

    # 协同与冲突
    synergy = cr["synergy_genes"]
    conflicts = cr["conflict_genes"]
    if synergy:
        lines += [
            "",
            f"## ✨ 协同增强（共 {len(synergy)} 处）",
            "",
        ]
        for s in synergy:
            chain_name, pos = s.split(":")
            label = CHAIN_LABELS[chain_name].split()[1]
            lines.append(f"- {label} 第{int(pos)+1}位：显性 × 显性 → 强强联合")

    if conflicts:
        lines += [
            "",
            f"## ⚡ 基因冲突（共 {len(conflicts)} 处）",
            "",
        ]
        for c in conflicts:
            chain_name, pos = c.split(":")
            label = CHAIN_LABELS[chain_name].split()[1]
            lines.append(f"- {label} 第{int(pos)+1}位：异源基因 → 新特性表达")

    # 显性分析
    lines += [
        "",
        f"## 📋 显性分析",
        "",
    ]
    for chain in ["paradigm", "system", "ecosystem"]:
        dom = cr["dominance_report"][chain]
        label = CHAIN_LABELS[chain].split()[1]
        lines.append(f"- **{label}**：{dom['winner']} 链占优")

    lines += [
        "",
        f"---",
        f"⏭️ 轮换：**{lang_a}** → **{lang_b}**",
    ]

    return "\n".join(lines)


def list_all_genomes() -> Dict[str, Dict[str, Any]]:
    """列出所有语言的基因组数据。"""
    result = {}
    for lang in LANGUAGE_GENOMES:
        result[lang] = get_language_genome(lang)
    return result


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Polyglot Genome — 编程语言基因组序列仪")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("cross", help="执行基因交叉（推进轮换）")
    sub.add_parser("preview", help="预览当前语言基因组（不推进）")
    sub.add_parser("list", help="列出所有语言基因组")

    lg = sub.add_parser("genome", help="查看指定语言的完整基因组")
    lg.add_argument("language", help="语言名称")

    args = parser.parse_args()

    if args.cmd == "cross":
        result = get_genome_crossing_report()
        print(format_genome_console(result))
    elif args.cmd == "preview":
        result = get_genome_preview()
        print(f"\n🧬 当前语言：{result['language']}\n")
        genome = result["genome"]
        print(f"  适性值：{genome['fitness_score']} — {genome['fitness_label']}")
        print()
        print(genome["genome_ascii"])
    elif args.cmd == "list":
        all_genomes = list_all_genomes()
        print(f"\n🧬 所有语言基因组\n")
        print(f"{'语言':<14} {'适性值':<8} {'标签':<12} {'范式链':<16} {'系统链':<16} {'生态链'}")
        print("-" * 80)
        for lang, data in sorted(all_genomes.items()):
            g = data["genome"]
            p = " ".join(g["paradigm"])
            s = " ".join(g["system"])
            e = " ".join(g["ecosystem"])
            print(f"{lang:<14} {data['fitness_score']:<8} {data['fitness_label']:<12} {p:<16} {s:<16} {e}")
    elif args.cmd == "genome":
        result = get_language_genome(args.language)
        print(f"\n🧬 {args.language} 基因组\n")
        print(f"  适性值：{result['fitness_score']} — {result['fitness_label']}")
        print()
        print(result["genome_ascii"])
    else:
        parser.print_help()
