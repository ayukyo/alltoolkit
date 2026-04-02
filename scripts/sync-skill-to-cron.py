#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同步 SKILL 到定时任务脚本

功能：
1. 读取 novel-writer 和 short-story-writer 的 SKILL.md
2. 提取关键流程信息（读取文件数、自检项、核心要求、禁止规则等）
3. 更新 cron/jobs.json 中对应任务的 message

使用：
python3 ~/.openclaw/workspace/scripts/sync-skill-to-cron.py
"""

import json
import re
import sys
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class SkillInfo:
    """SKILL信息数据类"""
    read_files: str = "3 个文件"
    read_files_detail: str = "大纲 + 圣经 + 最新章"
    check_items: str = "5 项"
    check_items_detail: str = "字数/钩子/重复/人称/圣经更新"
    core_requirements: str = "3 条"
    core_requirements_detail: str = "字数/钩子/承接"
    forbidden_rules: str = "3 条"
    forbidden_rules_detail: str = "空洞升华/说教式结尾/AI 式描写"


# 路径配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
SKILL_NOVEL_WRITER = WORKSPACE / "skills" / "novel-writer" / "SKILL.md"
SKILL_SHORT_STORY = WORKSPACE / "skills" / "short-story-writer" / "SKILL.md"
CRON_JOBS = Path.home() / ".openclaw" / "cron" / "jobs.json"


def extract_pattern(content: str, pattern: str, group: int = 1) -> Optional[str]:
    """安全地提取正则匹配结果"""
    match = re.search(pattern, content)
    return match.group(group) if match else None


def extract_list_items(content: str, start_pattern: str, end_marker: str = "```") -> str:
    """提取列表项内容"""
    match = re.search(rf"{start_pattern}.*?\n(.*?){end_marker}", content, re.DOTALL)
    if not match:
        return ""

    items = match.group(1).strip()
    # 清理列表标记
    items = re.sub(r"^\s*(?:\d+\.|-|\[\s*\])\s*", "", items, flags=re.MULTILINE)
    items = items.replace("\n", "/")
    return items[:100]


def extract_skill_info(skill_path: Path) -> SkillInfo:
    """从 SKILL.md 提取关键信息"""
    content = skill_path.read_text(encoding='utf-8')
    info = SkillInfo()

    # 提取读取文件数
    if count := extract_pattern(content, r"读取\s*(\d+)\s*个文件"):
        info.read_files = f"{count}个文件"

    # 提取读取文件详情
    if files := extract_list_items(content, r"读取.*?文件[：:]"):
        info.read_files_detail = files

    # 提取自检项数
    if count := extract_pattern(content, r"只检查\s*(\d+)\s*项"):
        info.check_items = f"{count}项"

    # 提取自检项详情
    if items := extract_list_items(content, r"只检查.*?项[：:]"):
        info.check_items_detail = items

    # 提取核心要求数
    if count := extract_pattern(content, r"核心要求.*?\(\s*只\s*(\d+)\s*条\s*\)"):
        info.core_requirements = f"{count}条"

    # 提取核心要求详情
    if reqs := extract_list_items(content, r"核心要求.*?\n"):
        info.core_requirements_detail = reqs

    # 提取禁止规则数
    if count := extract_pattern(content, r"禁止规则.*?\(\s*只\s*(\d+)\s*条\s*\)"):
        info.forbidden_rules = f"{count}条"

    # 提取禁止规则详情
    if rules := extract_list_items(content, r"禁止规则.*?\n"):
        info.forbidden_rules_detail = rules

    return info


def generate_message(skill_name: str, book_name: str, task_type: str = "续写") -> str:
    """生成定时任务 message"""

    if task_type == "续写":
        return f"""使用 {skill_name} SKILL 续写《{book_name}》。

**任务：** 批量续写 5 章（第 N+1 到 N+5 章）

**按 SKILL 流程执行：**
1. 读取 4 个文件（大纲 + 圣经 + 最新章 + 全部摘要）
2. 写前确认（章节号/阶段任务/上章钩子）
3. 逐章续写（4500-5500 字/章）
4. 写后自检 7 项
5. 更新圣经和摘要
6. 保存

**汇报格式：**
【第 X 批完成】（共 5 章：第 A-E 章）
书名：{book_name}
总字数：XXXXX 字
自检：通过
钩子：一句话说明"""

    elif task_type == "中篇":
        return f"""使用 {skill_name} SKILL，基于当前热点创作一篇中篇小说。

**按 SKILL 流程执行：**
1. 搜索热点→生成大纲
2. 分 3 批写作（每批 5 章）
3. 每章 1800-2200 字
4. 写后自检 7 项
5. 全部完成后生成简介

**参数：**
- 总字数：3 万字（±2000 字）
- 章节数：15 章
- 批次：3 批（每批 5 章）

**汇报格式：**
【第 X 批完成】（第 Y-Z 章）
字数：XXXX 字
进度：X/3 批（XX%）
自检：通过"""

    else:
        return f"""使用 {skill_name} SKILL。

按 SKILL 流程执行。"""


def update_cron_jobs() -> bool:
    """更新定时任务"""
    if not CRON_JOBS.exists():
        print(f"❌ 文件不存在：{CRON_JOBS}", file=sys.stderr)
        return False

    try:
        data = json.loads(CRON_JOBS.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误：{e}", file=sys.stderr)
        return False

    updated = False
    current_time_ms = int(time.time() * 1000)

    job_configs: List[tuple[str, str, str, str]] = [
        ('替身女友续写', 'novel-writer', '《专业替身女友今天失业了吗》', '续写'),
        ('下班后别找我续写', 'novel-writer', '《下班后别找我》', '续写'),
        ('每日中篇小说创作', 'short-story-writer', '', '中篇'),
    ]

    for job in data.get('jobs', []):
        job_name = job.get('name', '')

        for config_name, skill_name, book_name, task_type in job_configs:
            if config_name in job_name:
                new_message = generate_message(skill_name, book_name, task_type)
                old_message = job.get('payload', {}).get('message', '')

                if new_message != old_message:
                    job['payload']['message'] = new_message
                    job['updatedAtMs'] = current_time_ms
                    updated = True
                    print(f"✅ 更新：{job_name}")
                break

    if updated:
        CRON_JOBS.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"\n✅ 已保存到：{CRON_JOBS}")
    else:
        print("\nℹ️ 无需更新")

    return True


def print_skill_info(name: str, info: SkillInfo) -> None:
    """打印SKILL信息"""
    print(f"\n📋 {name} SKILL 信息:")
    for key, value in vars(info).items():
        print(f"   {key}: {value}")


def main() -> int:
    """主函数"""
    print("=" * 60)
    print("同步 SKILL 到定时任务")
    print("=" * 60)
    print()

    # 检查 SKILL 文件
    for skill_path in [SKILL_NOVEL_WRITER, SKILL_SHORT_STORY]:
        if not skill_path.exists():
            print(f"❌ 文件不存在：{skill_path}", file=sys.stderr)
            return 1
        print(f"✅ 读取 SKILL：{skill_path}")

    print()

    # 提取并打印信息
    novel_info = extract_skill_info(SKILL_NOVEL_WRITER)
    short_info = extract_skill_info(SKILL_SHORT_STORY)

    print_skill_info("novel-writer", novel_info)
    print_skill_info("short-story-writer", short_info)

    # 更新定时任务
    print("\n🔄 更新定时任务...")
    if not update_cron_jobs():
        return 1

    print()
    print("=" * 60)
    print("✅ 同步完成")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
