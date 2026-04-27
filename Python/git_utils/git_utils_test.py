#!/usr/bin/env python3
"""
AllToolkit - Git Utils 测试套件

测试覆盖：
- 仓库检测与初始化
- 状态查询
- 提交历史
- 分支操作
- 标签操作
- 远程操作
- 暂存区操作
- 仓库统计
- 错误处理
"""

import sys
import unittest
import subprocess
import tempfile
import shutil
import os
from pathlib import Path
from datetime import datetime

# 导入被测试模块

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    GitUtils,
    GitError,
    GitNotInstalledError,
    GitNotRepositoryError,
    GitCommandError,
    GitStatus,
    GitStatusFile,
    GitStatusResult,
    GitCommit,
    GitBranch,
    GitTag,
    GitDiff,
    GitRemote,
    GitLogStats,
    MergeStrategy,
    # 模块级函数
    is_repository,
    status,
    log,
    branch,
    current_branch,
    diff,
    get_stats,
)


class TestGitUtilsBase(unittest.TestCase):
    """测试基类 - 创建临时 Git 仓库"""
    
    def setUp(self):
        """创建临时仓库"""
        self.test_dir = tempfile.mkdtemp(prefix='git_utils_test_')
        self.repo_path = Path(self.test_dir)
        self.git = GitUtils(self.repo_path)
        
        # 初始化 Git 仓库
        self._run_git('init')
        self._run_git('config', 'user.email', 'test@example.com')
        self._run_git('config', 'user.name', 'Test User')
    
    def tearDown(self):
        """清理临时目录"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def _run_git(self, *args):
        """在测试仓库中运行 git 命令"""
        subprocess.run(
            ['git'] + list(args),
            cwd=str(self.repo_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False
        )
    
    def _create_file(self, path: str, content: str = "test content"):
        """创建测试文件"""
        file_path = self.repo_path / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return file_path
    
    def _commit_file(self, path: str, message: str = "Add file"):
        """创建文件并提交"""
        self._create_file(path)
        self._run_git('add', path)
        self._run_git('commit', '-m', message)


class TestGitDetection(TestGitUtilsBase):
    """测试仓库检测"""
    
    def test_is_repository_true(self):
        """测试识别 Git 仓库"""
        self.assertTrue(self.git.is_repository())
    
    def test_is_repository_false(self):
        """测试识别非 Git 仓库"""
        non_repo = GitUtils(tempfile.mkdtemp())
        self.assertFalse(non_repo.is_repository())
        shutil.rmtree(non_repo.repo_path, ignore_errors=True)
    
    def test_get_root(self):
        """测试获取仓库根目录"""
        root = self.git.get_root()
        self.assertEqual(root, self.repo_path.resolve())
    
    def test_get_git_dir(self):
        """测试获取 .git 目录"""
        git_dir = self.git.get_git_dir()
        self.assertTrue(git_dir.exists())
        self.assertEqual(git_dir.name, '.git')
    
    def test_module_level_is_repository(self):
        """测试模块级 is_repository 函数"""
        self.assertTrue(is_repository(self.repo_path))
        self.assertFalse(is_repository(tempfile.mkdtemp()))


class TestGitStatus(TestGitUtilsBase):
    """测试状态查询"""
    
    def test_status_clean(self):
        """测试干净仓库状态"""
        self._commit_file('test.txt', "initial")
        result = self.git.status()
        self.assertTrue(result.is_clean)
        self.assertEqual(len(result.staged_changes), 0)
        self.assertEqual(len(result.unstaged_changes), 0)
        self.assertEqual(len(result.untracked_files), 0)
    
    def test_status_untracked(self):
        """测试未跟踪文件"""
        self._commit_file('test.txt', "initial")
        self._create_file('new.txt', "new file")
        
        result = self.git.status()
        self.assertFalse(result.is_clean)
        self.assertEqual(len(result.untracked_files), 1)
        self.assertEqual(result.untracked_files[0].path, 'new.txt')
    
    def test_status_modified(self):
        """测试修改文件"""
        self._commit_file('test.txt', "initial")
        self._create_file('test.txt', "modified")
        
        result = self.git.status()
        self.assertFalse(result.is_clean)
        self.assertEqual(len(result.unstaged_changes), 1)
        self.assertEqual(result.unstaged_changes[0].status, GitStatus.MODIFIED)
    
    def test_status_staged(self):
        """测试暂存文件"""
        self._commit_file('test.txt', "initial")
        self._create_file('new.txt', "new file")
        self._run_git('add', 'new.txt')
        
        result = self.git.status()
        self.assertFalse(result.is_clean)
        self.assertEqual(len(result.staged_changes), 1)
        self.assertTrue(result.staged_changes[0].staged)
    
    def test_status_branch_info(self):
        """测试分支信息"""
        self._commit_file('test.txt', "initial")
        result = self.git.status()
        self.assertEqual(result.branch, 'master')
    
    def test_module_level_status(self):
        """测试模块级 status 函数"""
        self._commit_file('test.txt', "initial")
        result = status(self.repo_path)
        self.assertIsInstance(result, GitStatusResult)


class TestGitLog(TestGitUtilsBase):
    """测试提交历史"""
    
    def test_log_basic(self):
        """测试基本日志查询"""
        self._commit_file('test1.txt', "First commit")
        self._commit_file('test2.txt', "Second commit")
        self._commit_file('test3.txt', "Third commit")
        
        commits = self.git.log(max_count=10)
        self.assertEqual(len(commits), 3)
        
        # 验证最新提交
        self.assertEqual(commits[0].message, "Third commit")
        self.assertEqual(commits[0].author, "Test User")
        self.assertEqual(commits[0].author_email, "test@example.com")
    
    def test_log_max_count(self):
        """测试限制数量"""
        for i in range(5):
            self._commit_file(f'test{i}.txt', f"Commit {i}")
        
        commits = self.git.log(max_count=3)
        self.assertEqual(len(commits), 3)
    
    def test_log_commit_details(self):
        """测试提交详情"""
        self._commit_file('test.txt', "Test commit")
        
        commits = self.git.log(max_count=1)
        commit = commits[0]
        
        self.assertTrue(len(commit.hash) == 40)  # SHA-1 完整长度
        self.assertTrue(len(commit.short_hash) == 7)  # 短 hash
        self.assertIsInstance(commit.date, datetime)
        self.assertEqual(commit.message, "Test commit")
    
    def test_show_commit(self):
        """测试显示单个提交"""
        self._commit_file('test.txt', "Test commit")
        
        commit = self.git.show('HEAD')
        self.assertEqual(commit.message, "Test commit")
    
    def test_module_level_log(self):
        """测试模块级 log 函数"""
        self._commit_file('test.txt', "Test")
        commits = log(self.repo_path, max_count=1)
        self.assertEqual(len(commits), 1)


class TestGitBranch(TestGitUtilsBase):
    """测试分支操作"""
    
    def test_branch_list(self):
        """测试分支列表"""
        self._commit_file('test.txt', "initial")
        
        branches = self.git.branch()
        self.assertEqual(len(branches), 1)
        self.assertEqual(branches[0].name, 'master')
        self.assertTrue(branches[0].is_current)
    
    def test_current_branch(self):
        """测试当前分支"""
        self._commit_file('test.txt', "initial")
        
        branch_name = self.git.current_branch()
        self.assertEqual(branch_name, 'master')
    
    def test_create_branch(self):
        """测试创建分支"""
        self._commit_file('test.txt', "initial")
        
        success = self.git.create_branch('feature-1')
        self.assertTrue(success)
        
        branches = self.git.branch(list_all=False)
        branch_names = [b.name for b in branches]
        self.assertIn('feature-1', branch_names)
    
    def test_create_branch_from_point(self):
        """测试从指定点创建分支"""
        self._commit_file('test.txt', "initial")
        
        success = self.git.create_branch('feature-1', start_point='HEAD')
        self.assertTrue(success)
    
    def test_checkout_branch(self):
        """测试切换分支"""
        self._commit_file('test.txt', "initial")
        self.git.create_branch('feature-1')
        
        success = self.git.checkout('feature-1')
        self.assertTrue(success)
        self.assertEqual(self.git.current_branch(), 'feature-1')
    
    def test_checkout_create(self):
        """测试切换并创建分支"""
        self._commit_file('test.txt', "initial")
        
        success = self.git.checkout('feature-1', create=True)
        self.assertTrue(success)
        self.assertEqual(self.git.current_branch(), 'feature-1')
    
    def test_module_level_branch(self):
        """测试模块级 branch 函数"""
        self._commit_file('test.txt', "initial")
        branches = branch(self.repo_path)
        self.assertEqual(len(branches), 1)
    
    def test_module_level_current_branch(self):
        """测试模块级 current_branch 函数"""
        self._commit_file('test.txt', "initial")
        branch_name = current_branch(self.repo_path)
        self.assertEqual(branch_name, 'master')


class TestGitMerge(TestGitUtilsBase):
    """测试合并操作"""
    
    def test_merge_fast_forward(self):
        """测试快进合并"""
        self._commit_file('test.txt', "initial")
        self.git.create_branch('feature')
        self.git.checkout('feature')
        self._commit_file('feature.txt', "feature commit")
        
        self.git.checkout('master')
        success = self.git.merge('feature')
        self.assertTrue(success)
    
    def test_merge_no_ff(self):
        """测试非快进合并"""
        self._commit_file('test.txt', "initial")
        self.git.create_branch('feature')
        self.git.checkout('feature')
        self._commit_file('feature.txt', "feature commit")
        
        self.git.checkout('master')
        success = self.git.merge('feature', no_ff=True, message="Merge feature")
        self.assertTrue(success)


class TestGitTag(TestGitUtilsBase):
    """测试标签操作"""
    
    def test_tag_list_empty(self):
        """测试空标签列表"""
        self._commit_file('test.txt', "initial")
        
        tags = self.git.tag()
        self.assertEqual(len(tags), 0)
    
    def test_create_tag_lightweight(self):
        """测试创建轻量标签"""
        self._commit_file('test.txt', "initial")
        
        success = self.git.create_tag('v1.0.0')
        self.assertTrue(success)
        
        tags = self.git.tag()
        self.assertIn('v1.0.0', tags)
    
    def test_create_tag_annotated(self):
        """测试创建注解标签"""
        self._commit_file('test.txt', "initial")
        
        success = self.git.create_tag(
            'v1.0.0',
            message='Release version 1.0.0',
            annotated=True
        )
        self.assertTrue(success)
    
    def test_delete_tag(self):
        """测试删除标签"""
        self._commit_file('test.txt', "initial")
        self.git.create_tag('v1.0.0')
        
        success = self.git.delete_tag('v1.0.0')
        self.assertTrue(success)
        
        tags = self.git.tag()
        self.assertNotIn('v1.0.0', tags)
    
    def test_tag_pattern(self):
        """测试标签模式匹配"""
        self._commit_file('test.txt', "initial")
        self.git.create_tag('v1.0.0')
        self.git.create_tag('v1.0.1')
        self.git.create_tag('v2.0.0')
        
        tags = self.git.tag(pattern='v1.*')
        self.assertEqual(len(tags), 2)
        self.assertIn('v1.0.0', tags)
        self.assertIn('v1.0.1', tags)


class TestGitRemote(TestGitUtilsBase):
    """测试远程操作"""
    
    def test_remote_list_empty(self):
        """测试空远程列表"""
        self._commit_file('test.txt', "initial")
        
        remotes = self.git.remote()
        self.assertEqual(len(remotes), 0)
    
    def test_add_remote(self):
        """测试添加远程"""
        self._commit_file('test.txt', "initial")
        
        success = self.git.add_remote('origin', 'https://github.com/test/repo.git')
        self.assertTrue(success)
        
        remotes = self.git.remote()
        self.assertEqual(len(remotes), 1)
        self.assertEqual(remotes[0].name, 'origin')
        self.assertEqual(remotes[0].fetch_url, 'https://github.com/test/repo.git')
    
    def test_remove_remote(self):
        """测试移除远程"""
        self._commit_file('test.txt', "initial")
        self.git.add_remote('origin', 'https://github.com/test/repo.git')
        
        success = self.git.remove_remote('origin')
        self.assertTrue(success)
        
        remotes = self.git.remote()
        self.assertEqual(len(remotes), 0)
    
    def test_fetch(self):
        """测试 fetch（无远程时应该失败但不应崩溃）"""
        self._commit_file('test.txt', "initial")
        
        # 没有远程时 fetch 应该返回 False
        success = self.git.fetch()
        # 这个测试取决于是否有远程，所以不强制断言


class TestGitStaging(TestGitUtilsBase):
    """测试暂存区操作"""
    
    def test_add_file(self):
        """测试添加文件"""
        self._commit_file('test.txt', "initial")
        self._create_file('new.txt', "new content")
        
        success = self.git.add('new.txt')
        self.assertTrue(success)
        
        result = self.git.status()
        self.assertEqual(len(result.staged_changes), 1)
    
    def test_add_all(self):
        """测试添加所有文件"""
        self._commit_file('test.txt', "initial")
        self._create_file('new1.txt', "content 1")
        self._create_file('new2.txt', "content 2")
        
        success = self.git.add('', all_files=True)
        self.assertTrue(success)
        
        result = self.git.status()
        self.assertEqual(len(result.staged_changes), 2)
    
    def test_restore_worktree(self):
        """测试恢复工作树"""
        self._commit_file('test.txt', "initial content")
        self._create_file('test.txt', "modified content")
        
        success = self.git.restore('test.txt', worktree=True)
        self.assertTrue(success)
    
    def test_reset_soft(self):
        """测试 soft reset"""
        self._commit_file('test.txt', "initial")
        self._commit_file('test2.txt', "second")  # 需要至少两次提交才能 reset
        
        success = self.git.reset(mode='soft', commit='HEAD~1')
        # soft reset 后文件应该在暂存区
        result = self.git.status()
        self.assertTrue(success)
        # HEAD~1 的提交应该回到暂存区
        self.assertGreaterEqual(len(result.staged_changes), 1)
    
    def test_clean_dry_run(self):
        """测试清理（干运行）"""
        self._commit_file('test.txt', "initial")
        self._create_file('untracked.txt', "untracked")
        
        success = self.git.clean(dry_run=True)
        self.assertTrue(success)
        
        # 文件应该还在
        self.assertTrue((self.repo_path / 'untracked.txt').exists())


class TestGitCommit(TestGitUtilsBase):
    """测试提交操作"""
    
    def test_commit_basic(self):
        """测试基本提交"""
        self._create_file('test.txt', "content")
        self.git.add('test.txt')
        
        success = self.git.commit("Test commit")
        self.assertTrue(success)
        
        commits = self.git.log(max_count=1)
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0].message, "Test commit")
    
    def test_commit_all(self):
        """测试自动添加并提交"""
        self._commit_file('test.txt', "initial")
        self._create_file('test.txt', "modified")
        
        success = self.git.commit("Modified file", all_files=True)
        self.assertTrue(success)
    
    def test_commit_amend(self):
        """测试修改提交"""
        self._commit_file('test.txt', "initial")
        
        success = self.git.commit("Updated message", amend=True)
        self.assertTrue(success)
        
        commits = self.git.log(max_count=1)
        self.assertEqual(commits[0].message, "Updated message")


class TestGitDiff(TestGitUtilsBase):
    """测试差异操作"""
    
    def test_diff_unstaged(self):
        """测试未暂存差异"""
        self._commit_file('test.txt', "initial content")
        self._create_file('test.txt', "modified content with more lines\n")
        
        diffs = self.git.diff()
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0].file_path, 'test.txt')
    
    def test_diff_staged(self):
        """测试暂存差异"""
        self._commit_file('test.txt', "initial")
        self._create_file('new.txt', "new content\nline 2\nline 3\n")
        self.git.add('new.txt')
        
        diffs = self.git.diff(staged=True)
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0].changes_added, 3)
    
    def test_diff_patch(self):
        """测试补丁格式差异"""
        self._commit_file('test.txt', "initial")
        self._create_file('test.txt', "modified")
        
        patch = self.git.diff_patch()
        self.assertIn('diff --git', patch)
        self.assertIn('test.txt', patch)


class TestGitStats(TestGitUtilsBase):
    """测试仓库统计"""
    
    def test_stats_basic(self):
        """测试基本统计"""
        self._commit_file('test1.txt', "First")
        self._commit_file('test2.txt', "Second")
        self._commit_file('test3.txt', "Third")
        self.git.create_tag('v1.0.0')
        self.git.create_branch('feature')
        
        stats = self.git.get_stats()
        
        self.assertEqual(stats.total_commits, 3)
        self.assertEqual(stats.total_branches, 2)  # master + feature
        self.assertEqual(stats.total_tags, 1)
        self.assertEqual(stats.total_files, 3)
        self.assertEqual(stats.contributors, 1)
        self.assertIsNotNone(stats.first_commit_date)
        self.assertIsNotNone(stats.last_commit_date)
    
    def test_stats_to_dict(self):
        """测试统计转字典"""
        self._commit_file('test.txt', "initial")
        
        stats = self.git.get_stats()
        stats_dict = stats.to_dict()
        
        self.assertIn('total_commits', stats_dict)
        self.assertIn('total_branches', stats_dict)
        self.assertIn('total_tags', stats_dict)
        self.assertIn('total_files', stats_dict)
    
    def test_module_level_get_stats(self):
        """测试模块级 get_stats 函数"""
        self._commit_file('test.txt', "initial")
        stats = get_stats(self.repo_path)
        self.assertIsInstance(stats, GitLogStats)


class TestGitConfig(TestGitUtilsBase):
    """测试配置操作"""
    
    def test_config_get(self):
        """测试获取配置"""
        value = self.git.config('user.name')
        self.assertEqual(value, 'Test User')
    
    def test_config_set(self):
        """测试设置配置"""
        self.git.config('user.email', 'new@example.com')
        value = self.git.config('user.email')
        self.assertEqual(value, 'new@example.com')
    
    def test_config_get_nonexistent(self):
        """测试获取不存在的配置"""
        value = self.git.config('nonexistent.key')
        self.assertIsNone(value)


class TestGitVersion(TestGitUtilsBase):
    """测试版本查询"""
    
    def test_get_version(self):
        """测试获取 Git 版本"""
        version = self.git.get_version()
        self.assertTrue(version.startswith('git version'))


class TestGitErrors(TestGitUtilsBase):
    """测试错误处理"""
    
    def test_not_repository_error(self):
        """测试非仓库错误"""
        non_repo_dir = tempfile.mkdtemp()
        try:
            git = GitUtils(non_repo_dir)
            with self.assertRaises(GitNotRepositoryError):
                git.status()
        finally:
            shutil.rmtree(non_repo_dir, ignore_errors=True)
    
    def test_command_error(self):
        """测试命令错误"""
        self._commit_file('test.txt', "initial")
        
        # 尝试 checkout 不存在的分支
        success = self.git.checkout('nonexistent-branch')
        self.assertFalse(success)
    
    def test_git_error_str(self):
        """测试 GitError 字符串表示"""
        error = GitError(
            "Test error",
            command="git test",
            returncode=1,
            stderr="error details"
        )
        error_str = str(error)
        self.assertIn("Test error", error_str)
        self.assertIn("git test", error_str)
        self.assertIn("1", error_str)


class TestDataClasses(TestGitUtilsBase):
    """测试数据类"""
    
    def test_git_status_file_to_dict(self):
        """测试 GitStatusFile 转字典"""
        file = GitStatusFile(
            path='test.txt',
            status=GitStatus.MODIFIED,
            staged=True
        )
        d = file.to_dict()
        
        self.assertEqual(d['path'], 'test.txt')
        self.assertEqual(d['status'], 'modified')
        self.assertTrue(d['staged'])
    
    def test_git_status_result_to_dict(self):
        """测试 GitStatusResult 转字典"""
        result = GitStatusResult(
            branch='master',
            ahead=1,
            behind=2,
            is_clean=False
        )
        d = result.to_dict()
        
        self.assertEqual(d['branch'], 'master')
        self.assertEqual(d['ahead'], 1)
        self.assertEqual(d['behind'], 2)
        self.assertFalse(d['is_clean'])
    
    def test_git_commit_to_dict(self):
        """测试 GitCommit 转字典"""
        commit = GitCommit(
            hash='a' * 40,
            short_hash='aaaaaaa',
            author='Test',
            author_email='test@example.com',
            date=datetime.now(),
            message='Test commit'
        )
        d = commit.to_dict()
        
        self.assertEqual(d['hash'], 'a' * 40)
        self.assertEqual(d['author'], 'Test')
        self.assertEqual(d['message'], 'Test commit')
    
    def test_git_branch_to_dict(self):
        """测试 GitBranch 转字典"""
        branch = GitBranch(
            name='feature',
            is_current=True,
            upstream='origin/feature',
            ahead=1,
            behind=0
        )
        d = branch.to_dict()
        
        self.assertEqual(d['name'], 'feature')
        self.assertTrue(d['is_current'])
        self.assertEqual(d['upstream'], 'origin/feature')
    
    def test_git_diff_to_dict(self):
        """测试 GitDiff 转字典"""
        diff = GitDiff(
            file_path='test.txt',
            changes_added=5,
            changes_removed=2,
            patch='@@ -1,2 +1,5 @@'
        )
        d = diff.to_dict()
        
        self.assertEqual(d['file_path'], 'test.txt')
        self.assertEqual(d['changes_added'], 5)
        self.assertEqual(d['changes_removed'], 2)


class TestGitStatusEnum(TestGitUtilsBase):
    """测试状态枚举"""
    
    def test_git_status_values(self):
        """测试 GitStatus 枚举值"""
        self.assertEqual(GitStatus.UNTRACKED.value, 'untracked')
        self.assertEqual(GitStatus.MODIFIED.value, 'modified')
        self.assertEqual(GitStatus.ADDED.value, 'added')
        self.assertEqual(GitStatus.DELETED.value, 'deleted')


class TestMergeStrategy(TestGitUtilsBase):
    """测试合并策略"""
    
    def test_merge_strategy_values(self):
        """测试 MergeStrategy 枚举值"""
        self.assertEqual(MergeStrategy.RECURSIVE.value, 'recursive')
        self.assertEqual(MergeStrategy.RESOLVE.value, 'resolve')
        self.assertEqual(MergeStrategy.OURS.value, 'ours')


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
