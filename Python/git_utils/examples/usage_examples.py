#!/usr/bin/env python3
"""
AllToolkit - Git Utils 使用示例

本文件展示 git_utils 模块的各种使用场景。
"""

import sys
from pathlib import Path

# 添加父目录到路径以便导入
sys.path.insert(0, str(Path(__file__).parent.parent))

from mod import (
    GitUtils,
    is_repository,
    status,
    log,
    branch,
    current_branch,
    get_stats,
    GitStatus,
    GitCommit,
)


def example_basic_info():
    """示例 1: 基本信息查询"""
    print("=" * 50)
    print("示例 1: 基本信息查询")
    print("=" * 50)
    
    git = GitUtils()
    
    if not git.is_repository():
        print("当前目录不是 Git 仓库")
        return
    
    print(f"仓库根目录：{git.get_root()}")
    print(f".git 目录：{git.get_git_dir()}")
    print(f"当前分支：{git.current_branch()}")
    print(f"Git 版本：{git.get_version()}")
    print()


def example_status_check():
    """示例 2: 状态检查"""
    print("=" * 50)
    print("示例 2: 状态检查")
    print("=" * 50)
    
    git = GitUtils()
    result = git.status()
    
    print(f"分支：{result.branch}")
    print(f"领先远程：{result.ahead} 个提交")
    print(f"落后远程：{result.behind} 个提交")
    print(f"状态：{'✓ 干净' if result.is_clean else '✗ 有更改'}")
    
    if not result.is_clean:
        if result.staged_changes:
            print("\n暂存的更改:")
            for f in result.staged_changes:
                print(f"  {f.status.value}: {f.path}")
        
        if result.unstaged_changes:
            print("\n未暂存的更改:")
            for f in result.unstaged_changes:
                print(f"  {f.status.value}: {f.path}")
        
        if result.untracked_files:
            print("\n未跟踪的文件:")
            for f in result.untracked_files:
                print(f"  {f.path}")
    
    print()


def example_commit_history():
    """示例 3: 提交历史"""
    print("=" * 50)
    print("示例 3: 提交历史")
    print("=" * 50)
    
    git = GitUtils()
    commits = git.log(max_count=10)
    
    if not commits:
        print("没有提交历史")
        return
    
    print(f"最近 {len(commits)} 次提交:\n")
    
    for i, commit in enumerate(commits, 1):
        print(f"{i}. {commit.short_hash}")
        print(f"   作者：{commit.author} <{commit.author_email}>")
        print(f"   时间：{commit.date.strftime('%Y-%m-%d %H:%M')}")
        print(f"   信息：{commit.message}")
        print()


def example_branch_management():
    """示例 4: 分支管理"""
    print("=" * 50)
    print("示例 4: 分支管理")
    print("=" * 50)
    
    git = GitUtils()
    branches = git.branch(list_all=False)
    
    print("本地分支:")
    for b in branches:
        marker = "●" if b.is_current else "○"
        upstream = f" → {b.upstream}" if b.upstream else ""
        ahead_behind = ""
        if b.ahead or b.behind:
            ahead_behind = f" (+{b.ahead}/-{b.behind})"
        print(f"  {marker} {b.name}{upstream}{ahead_behind}")
    
    print()
    
    # 远程分支
    remote_branches = git.branch(list_all=True)
    remote_only = [b for b in remote_branches if b.is_remote]
    
    if remote_only:
        print("远程分支:")
        for b in remote_only[:5]:  # 只显示前 5 个
            print(f"  ○ {b.name}")
        if len(remote_only) > 5:
            print(f"  ... 还有 {len(remote_only) - 5} 个")
    
    print()


def example_repository_stats():
    """示例 5: 仓库统计"""
    print("=" * 50)
    print("示例 5: 仓库统计")
    print("=" * 50)
    
    git = GitUtils()
    stats = git.get_stats()
    
    print(f"📊 仓库统计信息")
    print(f"   提交总数：   {stats.total_commits:,}")
    print(f"   分支总数：   {stats.total_branches}")
    print(f"   标签总数：   {stats.total_tags}")
    print(f"   文件总数：   {stats.total_files:,}")
    print(f"   贡献者数：   {stats.contributors}")
    
    if stats.first_commit_date:
        print(f"   首次提交：   {stats.first_commit_date.strftime('%Y-%m-%d')}")
    if stats.last_commit_date:
        print(f"   最后提交：   {stats.last_commit_date.strftime('%Y-%m-%d')}")
    
    print()


def example_diff_view():
    """示例 6: 查看差异"""
    print("=" * 50)
    print("示例 6: 查看差异")
    print("=" * 50)
    
    git = GitUtils()
    
    # 未暂存的差异
    diffs = git.diff(staged=False)
    if diffs:
        print("未暂存的差异:")
        for d in diffs:
            print(f"  {d.file_path}: +{d.changes_added} -{d.changes_removed}")
    else:
        print("未暂存的差异：无")
    
    # 暂存的差异
    diffs_staged = git.diff(staged=True)
    if diffs_staged:
        print("\n暂存的差异:")
        for d in diffs_staged:
            print(f"  {d.file_path}: +{d.changes_added} -{d.changes_removed}")
    else:
        print("暂存的差异：无")
    
    print()


def example_module_functions():
    """示例 7: 模块级函数"""
    print("=" * 50)
    print("示例 7: 模块级函数（便捷使用）")
    print("=" * 50)
    
    # 直接使用模块级函数
    if is_repository():
        print(f"✓ 是 Git 仓库")
        print(f"当前分支：{current_branch()}")
        
        # 获取状态
        s = status()
        print(f"状态：{'干净' if s.is_clean else '有更改'}")
        
        # 获取提交
        commits = log(max_count=3)
        print(f"最近提交：{len(commits)} 个")
        
        # 获取统计
        stats = get_stats()
        print(f"总提交数：{stats.total_commits}")
    else:
        print("✗ 不是 Git 仓库")
    
    print()


def example_data_export():
    """示例 8: 数据导出"""
    print("=" * 50)
    print("示例 8: 数据导出为字典/JSON")
    print("=" * 50)
    
    git = GitUtils()
    
    # 状态导出
    status_result = git.status()
    status_dict = status_result.to_dict()
    print(f"状态字典键：{list(status_dict.keys())}")
    
    # 提交导出
    commits = git.log(max_count=3)
    if commits:
        commit_dict = commits[0].to_dict()
        print(f"提交字典键：{list(commit_dict.keys())}")
    
    # 统计导出
    stats = git.get_stats()
    stats_dict = stats.to_dict()
    print(f"统计字典键：{list(stats_dict.keys())}")
    
    # 可以序列化为 JSON
    import json
    json_str = json.dumps(stats_dict, indent=2)
    print(f"\n统计 JSON (前 200 字符):\n{json_str[:200]}...")
    
    print()


def example_error_handling():
    """示例 9: 错误处理"""
    print("=" * 50)
    print("示例 9: 错误处理")
    print("=" * 50)
    
    from mod import (
        GitError,
        GitNotInstalledError,
        GitNotRepositoryError,
        GitCommandError,
    )
    
    # 尝试在非仓库目录操作
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    try:
        git = GitUtils(temp_dir)
        git.status()
    except GitNotRepositoryError as e:
        print(f"✓ 捕获到非仓库错误：{e.message}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    # 尝试 checkout 不存在的分支
    git = GitUtils()
    if git.is_repository():
        success = git.checkout('nonexistent-branch-xyz')
        if not success:
            print("✓ checkout 失败已处理（返回 False）")
    
    print()


def example_workflow_ci_check():
    """示例 10: CI/CD 检查工作流"""
    print("=" * 50)
    print("示例 10: CI/CD 检查工作流")
    print("=" * 50)
    
    git = GitUtils()
    
    if not git.is_repository():
        print("❌ 不是 Git 仓库")
        return
    
    errors = []
    warnings = []
    
    # 检查 1: 工作区是否干净
    status_result = git.status()
    if not status_result.is_clean:
        errors.append(f"工作区有未提交的更改")
    
    # 检查 2: 是否在正确分支
    current = git.current_branch()
    if current not in ['main', 'master', 'develop']:
        warnings.append(f"当前分支为 '{current}'，可能不是主分支")
    
    # 检查 3: 是否落后远程
    if status_result.behind > 0:
        warnings.append(f"落后远程 {status_result.behind} 个提交")
    
    # 检查 4: 是否有暂存的更改
    if status_result.staged_changes:
        warnings.append(f"有 {len(status_result.staged_changes)} 个暂存的更改未提交")
    
    # 输出结果
    if errors:
        print("❌ 错误:")
        for e in errors:
            print(f"   - {e}")
    
    if warnings:
        print("⚠️  警告:")
        for w in warnings:
            print(f"   - {w}")
    
    if not errors and not warnings:
        print("✅ CI 检查通过")
    
    print()


def example_author_analysis():
    """示例 11: 作者分析"""
    print("=" * 50)
    print("示例 11: 提交作者分析")
    print("=" * 50)
    
    git = GitUtils()
    commits = git.log(max_count=100)
    
    if not commits:
        print("没有提交历史")
        return
    
    # 按作者分组
    from collections import defaultdict, Counter
    
    by_author = defaultdict(list)
    for commit in commits:
        by_author[commit.author].append(commit)
    
    # 按提交数排序
    sorted_authors = sorted(
        by_author.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )
    
    print("作者贡献统计:")
    for author, author_commits in sorted_authors:
        percentage = len(author_commits) / len(commits) * 100
        print(f"  {author}: {len(author_commits)} 次提交 ({percentage:.1f}%)")
    
    # 提交信息词频分析
    words = []
    for commit in commits:
        words.extend(commit.message.lower().split())
    
    # 过滤常见词
    stop_words = {'the', 'a', 'an', 'fix', 'update', 'add', 'remove', 'merge'}
    filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
    
    word_counts = Counter(filtered_words)
    print("\n提交信息高频词:")
    for word, count in word_counts.most_common(5):
        print(f"  {word}: {count} 次")
    
    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("AllToolkit Git Utils 使用示例")
    print("=" * 60 + "\n")
    
    examples = [
        example_basic_info,
        example_status_check,
        example_commit_history,
        example_branch_management,
        example_repository_stats,
        example_diff_view,
        example_module_functions,
        example_data_export,
        example_error_handling,
        example_workflow_ci_check,
        example_author_analysis,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"示例执行出错：{e}")
            print()
    
    print("=" * 60)
    print("所有示例执行完毕")
    print("=" * 60)


if __name__ == '__main__':
    main()
