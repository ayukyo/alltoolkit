#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Markdown Document Generator Example
=================================================
演示如何使用 markdown_utils 生成结构化文档。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import *


def generate_api_doc():
    """生成 API 文档"""
    print("\n" + "="*60)
    print("示例 1: API 文档生成")
    print("="*60)
    
    # 文档标题
    doc = []
    doc.append(create_heading("API 参考文档", 1))
    doc.append("")
    doc.append("本文档描述了用户管理 API 的使用方法。")
    doc.append("")
    
    # 概述
    doc.append(create_heading("概述", 2))
    doc.append("用户管理 API 提供用户的增删改查功能。")
    doc.append("")
    
    # 认证说明
    doc.append(create_blockquote("⚠️ 所有请求需要在 Header 中包含认证 Token"))
    doc.append("")
    
    # API 列表表格
    doc.append(create_heading("API 列表", 2))
    
    api_table = create_table(
        ["方法", "端点", "描述", "认证"],
        [
            ["GET", "/users", "获取用户列表", "是"],
            ["POST", "/users", "创建用户", "是"],
            ["GET", "/users/:id", "获取用户详情", "是"],
            ["PUT", "/users/:id", "更新用户", "是"],
            ["DELETE", "/users/:id", "删除用户", "是"],
        ],
        ["left", "left", "left", "center"]
    )
    doc.append(api_table)
    doc.append("")
    
    # 代码示例
    doc.append(create_heading("使用示例", 2))
    
    doc.append(create_heading("获取用户列表", 3))
    code_example = """import requests

response = requests.get(
    "https://api.example.com/users",
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)

users = response.json()
for user in users:
    print(f"{user['name']} - {user['email']}")"""
    doc.append(create_code_block(code_example, "python"))
    doc.append("")
    
    doc.append(create_heading("创建用户", 3))
    code_example = """import requests

data = {
    "name": "张三",
    "email": "zhangsan@example.com",
    "age": 28
}

response = requests.post(
    "https://api.example.com/users",
    json=data,
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)

if response.status_code == 201:
    print("创建成功!")
else:
    print(f"错误：{response.text}")"""
    doc.append(create_code_block(code_example, "python"))
    doc.append("")
    
    # 错误码表格
    doc.append(create_heading("错误码", 2))
    
    error_table = create_table(
        ["状态码", "错误", "说明"],
        [
            ["400", "Bad Request", "请求参数错误"],
            ["401", "Unauthorized", "认证失败"],
            ["403", "Forbidden", "权限不足"],
            ["404", "Not Found", "资源不存在"],
            ["500", "Internal Server Error", "服务器错误"],
        ],
        ["left", "left", "left"]
    )
    doc.append(error_table)
    doc.append("")
    
    # 合并文档
    full_doc = "\n".join(doc)
    
    print(full_doc)
    
    # 验证文档
    is_valid, issues = validate_markdown(full_doc)
    print(f"\n文档验证：{'✓ 有效' if is_valid else '✗ 无效'}")
    if issues:
        print(f"问题：{issues}")
    
    # 统计信息
    stats = word_count(full_doc)
    print(f"\n文档统计:")
    print(f"  行数：{stats['line_count']}")
    print(f"  字数：{stats['word_count']}")
    
    return full_doc


def generate_readme():
    """生成 README 文件"""
    print("\n" + "="*60)
    print("示例 2: README 生成")
    print("="*60)
    
    readme = []
    
    # 项目标题和徽章
    readme.append(create_heading("MyProject", 1))
    readme.append("")
    readme.append(create_image("Build Status", "https://img.shields.io/badge/build-passing-brightgreen", "Build Status"))
    readme.append(create_image("License", "https://img.shields.io/badge/license-MIT-blue", "License"))
    readme.append("")
    
    # 简介
    readme.append(create_heading("简介", 2))
    readme.append("MyProject 是一个功能强大的工具，用于解决实际问题。")
    readme.append("")
    readme.append(create_blockquote("✨ 特点：简单易用、高性能、跨平台"))
    readme.append("")
    
    # 安装说明
    readme.append(create_heading("安装", 2))
    readme.append(create_list([
        "克隆仓库：`git clone https://github.com/user/myproject.git`",
        "进入目录：`cd myproject`",
        "安装依赖：`pip install -r requirements.txt`",
        "运行测试：`python -m pytest`",
    ]))
    readme.append("")
    
    # 快速开始
    readme.append(create_heading("快速开始", 2))
    code = """from myproject import MyProject

# 初始化
project = MyProject(config="default")

# 运行
result = project.run()
print(result)"""
    readme.append(create_code_block(code, "python"))
    readme.append("")
    
    # 功能特性
    readme.append(create_heading("功能特性", 2))
    
    features_table = create_table(
        ["功能", "状态", "版本"],
        [
            ["用户认证", "✅ 已完成", "1.0.0"],
            ["数据同步", "✅ 已完成", "1.1.0"],
            ["云端备份", "🚧 进行中", "2.0.0"],
            ["AI 分析", "📋 计划中", "2.1.0"],
        ],
        ["left", "center", "center"]
    )
    readme.append(features_table)
    readme.append("")
    
    # 贡献指南
    readme.append(create_heading("贡献指南", 2))
    readme.append("欢迎贡献代码！请遵循以下步骤：")
    readme.append("")
    readme.append(create_list([
        "Fork 本项目",
        "创建特性分支 (`git checkout -b feature/AmazingFeature`)",
        "提交更改 (`git commit -m 'Add some AmazingFeature'`)",
        "推送到分支 (`git push origin feature/AmazingFeature`)",
        "开启 Pull Request",
    ], ordered=True))
    readme.append("")
    
    # 许可证
    readme.append(create_heading("许可证", 2))
    readme.append("本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情")
    readme.append("")
    
    # 联系方式
    readme.append(create_heading("联系方式", 2))
    readme.append(f"作者：{create_link('Your Name', 'mailto:your.email@example.com')}")
    readme.append("")
    readme.append(create_horizontal_rule())
    readme.append("")
    readme.append("*如果这个项目对你有帮助，请给一个 ⭐️ Star!*")
    
    full_readme = "\n".join(readme)
    
    print(full_readme)
    
    # 提取链接
    links = extract_links(full_readme)
    print(f"\n文档中的链接:")
    for link in links:
        if not link.is_image:
            print(f"  - {link.text}: {link.url}")
    
    return full_readme


def generate_changelog():
    """生成变更日志"""
    print("\n" + "="*60)
    print("示例 3: 变更日志生成")
    print("="*60)
    
    changelog = []
    
    changelog.append(create_heading("变更日志", 1))
    changelog.append("")
    changelog.append("本项目的所有重要变更都将记录在此文件中。")
    changelog.append("")
    changelog.append(create_horizontal_rule())
    changelog.append("")
    
    # 版本 2.0.0
    changelog.append(create_heading("[2.0.0] - 2026-04-09", 2))
    changelog.append("")
    changelog.append(create_heading("新增", 3))
    changelog.append(create_list([
        "添加用户管理模块",
        "支持 OAuth 2.0 认证",
        "新增数据导出功能",
        "添加 API 速率限制",
    ]))
    changelog.append("")
    
    changelog.append(create_heading("改进", 3))
    changelog.append(create_list([
        "优化数据库查询性能，提升 50%",
        "改进错误处理机制",
        "更新文档和示例代码",
    ]))
    changelog.append("")
    
    changelog.append(create_heading("修复", 3))
    changelog.append(create_list([
        "修复登录会话过期问题",
        "修复数据同步时的竞态条件",
        "修复移动端显示问题",
    ]))
    changelog.append("")
    changelog.append(create_horizontal_rule())
    changelog.append("")
    
    # 版本 1.1.0
    changelog.append(create_heading("[1.1.0] - 2026-03-15", 2))
    changelog.append("")
    changelog.append(create_heading("新增", 3))
    changelog.append(create_list([
        "添加暗色主题支持",
        "新增多语言支持 (中文、英文)",
    ]))
    changelog.append("")
    
    changelog.append(create_heading("修复", 3))
    changelog.append(create_list([
        "修复文件上传大小限制问题",
        "修复时区显示错误",
    ]))
    changelog.append("")
    changelog.append(create_horizontal_rule())
    changelog.append("")
    
    # 版本 1.0.0
    changelog.append(create_heading("[1.0.0] - 2026-02-01", 2))
    changelog.append("")
    changelog.append(create_heading("新增", 3))
    changelog.append(create_list([
        "初始版本发布",
        "核心功能实现",
        "基础文档编写",
    ]))
    changelog.append("")
    
    full_changelog = "\n".join(changelog)
    
    print(full_changelog)
    
    # 提取版本信息
    headings = extract_headings(full_changelog)
    versions = [h for h in headings if h.level == 2 and h.text.startswith("[")]
    print(f"\n版本历史:")
    for v in versions:
        print(f"  - {v.text}")
    
    return full_changelog


def main():
    """运行所有示例"""
    print("\n" + "#"*60)
    print("# AllToolkit - Markdown 文档生成示例")
    print("#"*60)
    
    generate_api_doc()
    generate_readme()
    generate_changelog()
    
    print("\n" + "="*60)
    print("所有示例完成!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
