"""
AllToolkit - Python Git Utilities

零依赖 Git 仓库操作工具库。
完全使用 Python 标准库实现（subprocess, os, pathlib, re, json），无需任何外部依赖。
通过调用 git 命令行工具实现所有功能。

Author: AllToolkit
License: MIT
Version: 1.0.0
"""

import subprocess
import os
import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


def _parse_git_date(date_str: str) -> datetime:
    """
    解析 Git 日期字符串（兼容 Python 3.6）
    
    Git 日期格式：2026-04-11 07:11:23 +0800
    """
    try:
        # 尝试去掉时区部分并解析
        date_part = date_str[:19]  # "2026-04-11 07:11:23"
        return datetime.strptime(date_part, '%Y-%m-%d %H:%M:%S')
    except (ValueError, IndexError, TypeError):
        return datetime.now()


# =============================================================================
# 枚举与数据类
# =============================================================================

class GitStatus(Enum):
    """文件状态"""
    UNTRACKED = "untracked"
    UNMODIFIED = "unmodified"
    MODIFIED = "modified"
    ADDED = "added"
    DELETED = "deleted"
    RENAMED = "renamed"
    COPIED = "copied"
    UPDATED_BUT_UNMERGED = "updated_but_unmerged"


class MergeStrategy(Enum):
    """合并策略"""
    RECURSIVE = "recursive"
    RESOLVE = "resolve"
    OCTOPUS = "octopus"
    OURS = "ours"
    SUBTREE = "subtree"


@dataclass
class GitStatusFile:
    """单个文件的状态"""
    path: str
    status: GitStatus
    staged: bool = False
    old_path: Optional[str] = None  # 重命名时的旧路径
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'path': self.path,
            'status': self.status.value,
            'staged': self.staged,
            'old_path': self.old_path,
        }


@dataclass
class GitStatusResult:
    """git status 结果"""
    branch: str
    ahead: int = 0
    behind: int = 0
    staged_changes: List[GitStatusFile] = field(default_factory=list)
    unstaged_changes: List[GitStatusFile] = field(default_factory=list)
    untracked_files: List[GitStatusFile] = field(default_factory=list)
    is_clean: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'branch': self.branch,
            'ahead': self.ahead,
            'behind': self.behind,
            'staged_changes': [f.to_dict() for f in self.staged_changes],
            'unstaged_changes': [f.to_dict() for f in self.unstaged_changes],
            'untracked_files': [f.to_dict() for f in self.untracked_files],
            'is_clean': self.is_clean,
        }


@dataclass
class GitCommit:
    """提交信息"""
    hash: str
    short_hash: str
    author: str
    author_email: str
    date: datetime
    message: str
    parent_hashes: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'hash': self.hash,
            'short_hash': self.short_hash,
            'author': self.author,
            'author_email': self.author_email,
            'date': self.date.isoformat(),
            'message': self.message,
            'parent_hashes': self.parent_hashes,
        }


@dataclass
class GitBranch:
    """分支信息"""
    name: str
    is_current: bool = False
    is_remote: bool = False
    upstream: Optional[str] = None
    ahead: int = 0
    behind: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'is_current': self.is_current,
            'is_remote': self.is_remote,
            'upstream': self.upstream,
            'ahead': self.ahead,
            'behind': self.behind,
        }


@dataclass
class GitTag:
    """标签信息"""
    name: str
    commit_hash: str
    message: Optional[str] = None
    tagger: Optional[str] = None
    date: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'commit_hash': self.commit_hash,
            'message': self.message,
            'tagger': self.tagger,
            'date': self.date.isoformat() if self.date else None,
        }


@dataclass
class GitDiff:
    """差异信息"""
    file_path: str
    changes_added: int = 0
    changes_removed: int = 0
    patch: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'file_path': self.file_path,
            'changes_added': self.changes_added,
            'changes_removed': self.changes_removed,
            'patch': self.patch,
        }


@dataclass
class GitRemote:
    """远程仓库信息"""
    name: str
    fetch_url: str
    push_url: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'fetch_url': self.fetch_url,
            'push_url': self.push_url,
        }


@dataclass
class GitLogStats:
    """仓库统计信息"""
    total_commits: int
    total_branches: int
    total_tags: int
    total_files: int
    first_commit_date: Optional[datetime] = None
    last_commit_date: Optional[datetime] = None
    contributors: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'total_commits': self.total_commits,
            'total_branches': self.total_branches,
            'total_tags': self.total_tags,
            'total_files': self.total_files,
            'first_commit_date': self.first_commit_date.isoformat() if self.first_commit_date else None,
            'last_commit_date': self.last_commit_date.isoformat() if self.last_commit_date else None,
            'contributors': self.contributors,
        }


# =============================================================================
# 异常类
# =============================================================================

class GitError(Exception):
    """Git 操作异常"""
    def __init__(self, message: str, command: Optional[str] = None, 
                 returncode: Optional[int] = None, stderr: Optional[str] = None):
        self.message = message
        self.command = command
        self.returncode = returncode
        self.stderr = stderr
        super().__init__(self.message)
    
    def __str__(self) -> str:
        parts = [self.message]
        if self.command:
            parts.append(f"Command: {self.command}")
        if self.returncode is not None:
            parts.append(f"Return code: {self.returncode}")
        if self.stderr:
            parts.append(f"Error: {self.stderr}")
        return " | ".join(parts)


class GitNotInstalledError(GitError):
    """Git 未安装"""
    pass


class GitNotRepositoryError(GitError):
    """不在 Git 仓库中"""
    pass


class GitCommandError(GitError):
    """Git 命令执行失败"""
    pass


# =============================================================================
# Git 工具类
# =============================================================================

class GitUtils:
    """
    Git 仓库操作工具类
    
    提供零依赖的 Git 操作，通过调用 git 命令行实现。
    所有方法都支持指定仓库路径，默认为当前目录。
    
    Example:
        >>> git = GitUtils()
        >>> status = git.status()
        >>> print(f"Current branch: {status.branch}")
        
        >>> commits = git.log(max_count=5)
        >>> for commit in commits:
        ...     print(f"{commit.short_hash}: {commit.message}")
    """
    
    def __init__(self, repo_path: Optional[Union[str, Path]] = None):
        """
        初始化 Git 工具
        
        Args:
            repo_path: Git 仓库路径，默认为当前目录
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self._git_executable: Optional[str] = None
    
    def _check_git_installed(self) -> str:
        """检查 Git 是否已安装"""
        if self._git_executable:
            return self._git_executable
        
        try:
            result = subprocess.run(
                ['git', '--version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=5
            )
            if result.returncode == 0:
                self._git_executable = 'git'
                return 'git'
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        raise GitNotInstalledError("Git is not installed or not in PATH")
    
    def _is_repository(self) -> bool:
        """检查当前路径是否为 Git 仓库"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=str(self.repo_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def _require_repository(self):
        """确保在 Git 仓库中"""
        if not self._is_repository():
            raise GitNotRepositoryError(
                f"Not a git repository: {self.repo_path}"
            )
    
    def _run_git(self, *args: str, capture_output: bool = True, 
                 check: bool = True, timeout: int = 30) -> subprocess.CompletedProcess:
        """
        运行 Git 命令
        
        Args:
            *args: Git 命令参数
            capture_output: 是否捕获输出
            check: 是否检查返回码
            timeout: 超时时间（秒）
            
        Returns:
            subprocess.CompletedProcess 结果
            
        Raises:
            GitCommandError: 命令执行失败
        """
        self._check_git_installed()
        
        cmd = ['git'] + list(args)
        
        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.repo_path),
                stdout=subprocess.PIPE if capture_output else None,
                stderr=subprocess.PIPE if capture_output else None,
                universal_newlines=True,
                timeout=timeout,
                check=False
            )
            
            if check and result.returncode != 0:
                raise GitCommandError(
                    f"Git command failed",
                    command=' '.join(cmd),
                    returncode=result.returncode,
                    stderr=result.stderr.strip()
                )
            
            return result
            
        except subprocess.TimeoutExpired as e:
            raise GitCommandError(
                f"Git command timed out after {timeout}s",
                command=' '.join(cmd),
                stderr=str(e)
            )
        except FileNotFoundError:
            raise GitNotInstalledError("Git is not installed or not in PATH")
    
    # ==========================================================================
    # 仓库信息
    # ==========================================================================
    
    def is_repository(self) -> bool:
        """
        检查是否为 Git 仓库
        
        Returns:
            bool: 是否为 Git 仓库
        """
        return self._is_repository()
    
    def get_root(self) -> Path:
        """
        获取仓库根目录
        
        Returns:
            Path: 仓库根目录路径
        """
        self._require_repository()
        result = self._run_git('rev-parse', '--show-toplevel')
        return Path(result.stdout.strip()).resolve()
    
    def get_git_dir(self) -> Path:
        """
        获取 .git 目录路径
        
        Returns:
            Path: .git 目录路径
        """
        self._require_repository()
        result = self._run_git('rev-parse', '--git-dir')
        git_dir = Path(result.stdout.strip())
        # 如果是相对路径，相对于仓库根目录解析
        if not git_dir.is_absolute():
            git_dir = self.repo_path / git_dir
        return git_dir.resolve()
    
    # ==========================================================================
    # 状态与差异
    # ==========================================================================
    
    def status(self) -> GitStatusResult:
        """
        获取仓库状态
        
        Returns:
            GitStatusResult: 状态结果
        """
        self._require_repository()
        
        # 获取分支信息
        branch_result = self._run_git('rev-parse', '--abbrev-ref', 'HEAD')
        branch = branch_result.stdout.strip()
        
        result = GitStatusResult(branch=branch)
        
        # 获取远程跟踪信息
        try:
            ahead_behind = self._run_git(
                'rev-list', '--left-right', '--count', f'HEAD...@{{upstream}}',
                check=False
            )
            if ahead_behind.returncode == 0:
                parts = ahead_behind.stdout.strip().split()
                if len(parts) == 2:
                    result.ahead = int(parts[0])
                    result.behind = int(parts[1])
        except GitCommandError:
            pass  # 没有上游分支
        
        # 获取状态输出
        status_result = self._run_git(
            'status', '--porcelain=v1', '-z', '--untracked-files=all'
        )
        
        entries = [e for e in status_result.stdout.split('\x00') if e]
        
        for entry in entries:
            if not entry:
                continue
            
            # 格式：XY filename 或 XY oldname -> newname
            # 前两个字符是状态，后面是空格和文件名
            if len(entry) < 3:
                continue
            
            status_chars = entry[:2]
            path = entry[3:]  # 跳过 "XY " 前缀
            
            staged = status_chars[0] != ' ' and status_chars[0] != '?'
            
            if status_chars.startswith('??'):
                # 未跟踪文件
                result.untracked_files.append(GitStatusFile(
                    path=path,
                    status=GitStatus.UNTRACKED,
                    staged=False
                ))
            elif status_chars.startswith('R'):
                # 重命名
                if ' -> ' in path:
                    old_path, new_path = path.split(' -> ', 1)
                else:
                    old_path, new_path = path, path
                result.staged_changes.append(GitStatusFile(
                    path=new_path,
                    status=GitStatus.RENAMED,
                    staged=staged,
                    old_path=old_path
                ))
            else:
                # 其他状态
                status_char = status_chars[1] if status_chars[0] == ' ' else status_chars[0]
                status_map = {
                    'M': GitStatus.MODIFIED,
                    'A': GitStatus.ADDED,
                    'D': GitStatus.DELETED,
                    'C': GitStatus.COPIED,
                    'U': GitStatus.UPDATED_BUT_UNMERGED,
                    ' ': GitStatus.UNMODIFIED,
                }
                status = status_map.get(status_char, GitStatus.MODIFIED)
                
                if staged:
                    result.staged_changes.append(GitStatusFile(
                        path=path,
                        status=status,
                        staged=True
                    ))
                else:
                    result.unstaged_changes.append(GitStatusFile(
                        path=path,
                        status=status,
                        staged=False
                    ))
        
        result.is_clean = (
            len(result.staged_changes) == 0 and
            len(result.unstaged_changes) == 0 and
            len(result.untracked_files) == 0
        )
        
        return result
    
    def diff(self, path: Optional[str] = None, staged: bool = False,
             ref1: Optional[str] = None, ref2: Optional[str] = None) -> List[GitDiff]:
        """
        获取差异
        
        Args:
            path: 文件路径，None 表示所有文件
            staged: 是否比较暂存区
            ref1: 第一个引用
            ref2: 第二个引用
            
        Returns:
            List[GitDiff]: 差异列表
        """
        self._require_repository()
        
        args = ['diff', '--numstat']
        
        if staged:
            args.append('--cached')
        
        if ref1 and ref2:
            args.extend([ref1, ref2])
        elif ref1:
            args.append(ref1)
        
        if path:
            args.extend(['--', path])
        
        result = self._run_git(*args)
        
        diffs = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 3:
                added = int(parts[0]) if parts[0] != '-' else 0
                removed = int(parts[1]) if parts[1] != '-' else 0
                file_path = parts[2]
                diffs.append(GitDiff(
                    file_path=file_path,
                    changes_added=added,
                    changes_removed=removed
                ))
        
        return diffs
    
    def diff_patch(self, path: Optional[str] = None, staged: bool = False,
                   ref1: Optional[str] = None, ref2: Optional[str] = None) -> str:
        """
        获取补丁格式的差异
        
        Args:
            path: 文件路径
            staged: 是否比较暂存区
            ref1: 第一个引用
            ref2: 第二个引用
            
        Returns:
            str: 补丁文本
        """
        self._require_repository()
        
        args = ['diff']
        
        if staged:
            args.append('--cached')
        
        if ref1 and ref2:
            args.extend([ref1, ref2])
        elif ref1:
            args.append(ref1)
        
        if path:
            args.extend(['--', path])
        
        result = self._run_git(*args)
        return result.stdout
    
    # ==========================================================================
    # 提交历史
    # ==========================================================================
    
    def log(self, max_count: int = 10, branch: Optional[str] = None,
            since: Optional[str] = None, until: Optional[str] = None,
            author: Optional[str] = None) -> List[GitCommit]:
        """
        获取提交历史
        
        Args:
            max_count: 最大返回数量
            branch: 分支名
            since: 起始时间
            until: 结束时间
            author: 作者名
            
        Returns:
            List[GitCommit]: 提交列表
        """
        self._require_repository()
        
        args = ['log', f'-n{max_count}', '--format=%H|%h|%an|%ae|%ai|%P|%s']
        
        if branch:
            args.append(branch)
        
        if since:
            args.extend(['--since', since])
        
        if until:
            args.extend(['--until', until])
        
        if author:
            args.extend(['--author', author])
        
        result = self._run_git(*args)
        
        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('|', 6)
            if len(parts) >= 5:
                parents = parts[5].split() if len(parts) > 5 and parts[5] else []
                date = _parse_git_date(parts[4])
                
                commits.append(GitCommit(
                    hash=parts[0],
                    short_hash=parts[1] if len(parts) > 1 else parts[0][:7],
                    author=parts[2] if len(parts) > 2 else "",
                    author_email=parts[3] if len(parts) > 3 else "",
                    date=date,
                    message=parts[6] if len(parts) > 6 else (parts[5] if len(parts) > 5 and parents else ""),
                    parent_hashes=parents
                ))
        
        return commits
    
    def show(self, ref: str = 'HEAD') -> GitCommit:
        """
        显示提交详情
        
        Args:
            ref: 引用（commit hash、分支名、标签等）
            
        Returns:
            GitCommit: 提交信息
        """
        self._require_repository()
        
        result = self._run_git(
            'show', '-s', '--format=%H|%h|%an|%ae|%ai|%P|%s', ref
        )
        
        line = result.stdout.strip()
        parts = line.split('|', 6)
        
        parents = parts[5].split() if len(parts) > 5 and parts[5] else []
        date = _parse_git_date(parts[4])
        
        return GitCommit(
            hash=parts[0],
            short_hash=parts[1],
            author=parts[2],
            author_email=parts[3],
            date=date,
            message=parts[6] if len(parts) > 6 else "",
            parent_hashes=parents
        )
    
    # ==========================================================================
    # 分支操作
    # ==========================================================================
    
    def branch(self, list_all: bool = False) -> List[GitBranch]:
        """
        获取分支列表
        
        Args:
            list_all: 是否包含远程分支
            
        Returns:
            List[GitBranch]: 分支列表
        """
        self._require_repository()
        
        args = ['branch']
        if list_all:
            args.append('-a')
        args.append('-v')
        
        result = self._run_git(*args)
        
        branches = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            
            # 解析分支行
            is_current = line.startswith('*')
            line = line.lstrip('* ').strip()
            
            # 提取分支名和上游信息
            parts = line.split()
            if not parts:
                continue
            
            name = parts[0]
            upstream = None
            ahead = 0
            behind = 0
            
            # 解析上游信息
            upstream_match = re.search(r'\[(.*?)\]', line)
            if upstream_match:
                upstream_info = upstream_match.group(1)
                if ':' in upstream_info:
                    upstream = upstream_info.split(':')[0]
                    if 'ahead' in upstream_info:
                        ahead_match = re.search(r'ahead (\d+)', upstream_info)
                        if ahead_match:
                            ahead = int(ahead_match.group(1))
                    if 'behind' in upstream_info:
                        behind_match = re.search(r'behind (\d+)', upstream_info)
                        if behind_match:
                            behind = int(behind_match.group(1))
                else:
                    upstream = upstream_info
            
            is_remote = name.startswith('remotes/')
            if is_remote:
                name = name[8:]  # 移除 'remotes/' 前缀
            
            branches.append(GitBranch(
                name=name,
                is_current=is_current,
                is_remote=is_remote,
                upstream=upstream,
                ahead=ahead,
                behind=behind
            ))
        
        return branches
    
    def current_branch(self) -> str:
        """
        获取当前分支名
        
        Returns:
            str: 分支名
        """
        self._require_repository()
        result = self._run_git('rev-parse', '--abbrev-ref', 'HEAD')
        return result.stdout.strip()
    
    def create_branch(self, name: str, start_point: Optional[str] = None,
                      force: bool = False) -> bool:
        """
        创建新分支
        
        Args:
            name: 分支名
            start_point: 起始点（commit hash 或分支名）
            force: 是否强制创建
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        args = ['branch']
        if force:
            args.append('-f')
        args.append(name)
        
        if start_point:
            args.append(start_point)
        
        try:
            self._run_git(*args)
            return True
        except GitCommandError:
            return False
    
    def checkout(self, branch_or_commit: str, create: bool = False) -> bool:
        """
        切换分支或提交
        
        Args:
            branch_or_commit: 分支名或 commit hash
            create: 是否创建新分支
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        args = ['checkout']
        if create:
            args.append('-b')
        args.append(branch_or_commit)
        
        try:
            self._run_git(*args)
            return True
        except GitCommandError:
            return False
    
    def merge(self, branch: str, strategy: Optional[MergeStrategy] = None,
              no_ff: bool = False, message: Optional[str] = None) -> bool:
        """
        合并分支
        
        Args:
            branch: 要合并的分支
            strategy: 合并策略
            no_ff: 是否禁用快进
            message: 合并提交信息
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        args = ['merge']
        
        if strategy:
            args.extend(['-s', strategy.value])
        
        if no_ff:
            args.append('--no-ff')
        
        if message:
            args.extend(['-m', message])
        
        args.append(branch)
        
        try:
            self._run_git(*args, timeout=120)
            return True
        except GitCommandError:
            return False
    
    # ==========================================================================
    # 标签操作
    # ==========================================================================
    
    def tag(self, list_tags: bool = True, pattern: Optional[str] = None) -> List[str]:
        """
        获取标签列表
        
        Args:
            list_tags: 是否列出标签
            pattern: 匹配模式
            
        Returns:
            List[str]: 标签名列表
        """
        self._require_repository()
        
        args = ['tag', '-l'] if list_tags else ['tag']
        if pattern:
            args.append(pattern)
        
        result = self._run_git(*args)
        return [t.strip() for t in result.stdout.strip().split('\n') if t.strip()]
    
    def create_tag(self, name: str, message: Optional[str] = None,
                   commit: Optional[str] = None, annotated: bool = False) -> bool:
        """
        创建标签
        
        Args:
            name: 标签名
            message: 标签信息
            commit: 目标 commit
            annotated: 是否为注解标签
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        args = ['tag']
        
        if annotated or message:
            args.append('-a')
        
        if message:
            args.extend(['-m', message])
        
        args.append(name)
        
        if commit:
            args.append(commit)
        
        try:
            self._run_git(*args)
            return True
        except GitCommandError:
            return False
    
    def delete_tag(self, name: str) -> bool:
        """
        删除标签
        
        Args:
            name: 标签名
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        try:
            self._run_git('tag', '-d', name)
            return True
        except GitCommandError:
            return False
    
    # ==========================================================================
    # 远程操作
    # ==========================================================================
    
    def remote(self, verbose: bool = True) -> List[GitRemote]:
        """
        获取远程仓库列表
        
        Args:
            verbose: 是否显示详细信息
            
        Returns:
            List[GitRemote]: 远程仓库列表
        """
        self._require_repository()
        
        args = ['remote']
        if verbose:
            args.append('-v')
        
        result = self._run_git(*args)
        
        remotes = []
        current_remote = None
        fetch_url = None
        
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            
            if verbose:
                parts = line.split()
                if len(parts) >= 3:
                    name = parts[0]
                    url = parts[1]
                    direction = parts[2]
                    
                    if current_remote != name:
                        if current_remote:
                            remotes.append(GitRemote(
                                name=current_remote,
                                fetch_url=fetch_url or "",
                                push_url=""
                            ))
                        current_remote = name
                        fetch_url = url if direction == '(fetch)' else None
                    else:
                        if direction == '(push)':
                            remotes.append(GitRemote(
                                name=current_remote,
                                fetch_url=fetch_url or url,
                                push_url=url
                            ))
                            current_remote = None
            else:
                remotes.append(GitRemote(
                    name=line.strip(),
                    fetch_url="",
                    push_url=""
                ))
        
        if current_remote:
            remotes.append(GitRemote(
                name=current_remote,
                fetch_url=fetch_url or "",
                push_url=""
            ))
        
        return remotes
    
    def add_remote(self, name: str, url: str) -> bool:
        """
        添加远程仓库
        
        Args:
            name: 远程名
            url: URL
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        try:
            self._run_git('remote', 'add', name, url)
            return True
        except GitCommandError:
            return False
    
    def remove_remote(self, name: str) -> bool:
        """
        移除远程仓库
        
        Args:
            name: 远程名
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        try:
            self._run_git('remote', 'remove', name)
            return True
        except GitCommandError:
            return False
    
    def fetch(self, remote: Optional[str] = None, all_remotes: bool = False,
              prune: bool = False) -> bool:
        """
        获取远程更新
        
        Args:
            remote: 远程名
            all_remotes: 是否获取所有远程
            prune: 是否清理删除的分支
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        args = ['fetch']
        
        if all_remotes:
            args.append('--all')
        
        if prune:
            args.append('--prune')
        
        if remote and not all_remotes:
            args.append(remote)
        
        try:
            self._run_git(*args, timeout=120)
            return True
        except GitCommandError:
            return False
    
    def pull(self, remote: str = 'origin', branch: Optional[str] = None,
             rebase: bool = False) -> bool:
        """
        拉取远程更新
        
        Args:
            remote: 远程名
            branch: 分支名
            rebase: 是否使用 rebase
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        args = ['pull']
        
        if rebase:
            args.append('--rebase')
        
        args.append(remote)
        
        if branch:
            args.append(branch)
        
        try:
            self._run_git(*args, timeout=300)
            return True
        except GitCommandError:
            return False
    
    def push(self, remote: str = 'origin', branch: Optional[str] = None,
             force: bool = False, set_upstream: bool = False) -> bool:
        """
        推送本地更新
        
        Args:
            remote: 远程名
            branch: 分支名
            force: 是否强制推送
            set_upstream: 是否设置上游
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        args = ['push']
        
        if force:
            args.append('--force')
        
        if set_upstream:
            args.append('-u')
        
        args.append(remote)
        
        if branch:
            args.append(branch)
        
        try:
            self._run_git(*args, timeout=300)
            return True
        except GitCommandError:
            return False
    
    # ==========================================================================
    # 暂存区操作
    # ==========================================================================
    
    def add(self, pathspec: Union[str, List[str]], all_files: bool = False) -> bool:
        """
        添加文件到暂存区
        
        Args:
            pathspec: 文件路径或模式
            all_files: 是否添加所有修改的文件
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        args = ['add']
        
        if all_files:
            args.append('-A')
        elif isinstance(pathspec, list):
            args.extend(pathspec)
        elif pathspec:
            args.append(pathspec)
        
        try:
            self._run_git(*args)
            return True
        except GitCommandError:
            return False
    
    def restore(self, pathspec: Union[str, List[str]], staged: bool = False,
                worktree: bool = False) -> bool:
        """
        恢复文件
        
        Args:
            pathspec: 文件路径
            staged: 是否从暂存区恢复
            worktree: 是否恢复工作树
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        args = ['restore']
        
        if staged:
            args.append('--staged')
        
        if worktree:
            args.append('--worktree')
        
        if isinstance(pathspec, list):
            args.extend(pathspec)
        elif pathspec:
            args.append(pathspec)
        
        try:
            self._run_git(*args)
            return True
        except GitCommandError:
            return False
    
    def reset(self, mode: str = 'mixed', commit: Optional[str] = None) -> bool:
        """
        重置仓库
        
        Args:
            mode: 重置模式 (soft, mixed, hard)
            commit: 目标 commit
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        args = ['reset']
        
        if mode in ['soft', 'mixed', 'hard']:
            args.append(f'--{mode}')
        
        if commit:
            args.append(commit)
        
        try:
            self._run_git(*args)
            return True
        except GitCommandError:
            return False
    
    def clean(self, force: bool = False, dry_run: bool = False,
              directories: bool = False) -> bool:
        """
        清理未跟踪的文件
        
        Args:
            force: 是否强制清理
            dry_run: 是否仅显示
            directories: 是否包括目录
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        args = ['clean']
        
        if dry_run:
            args.append('-n')
        elif force:
            args.append('-f')
        
        if directories:
            args.append('-d')
        
        try:
            self._run_git(*args)
            return True
        except GitCommandError:
            return False
    
    # ==========================================================================
    # 提交操作
    # ==========================================================================
    
    def commit(self, message: str, all_files: bool = False,
               amend: bool = False, no_verify: bool = False) -> bool:
        """
        创建提交
        
        Args:
            message: 提交信息
            all_files: 是否自动添加所有修改
            amend: 是否修改上一次提交
            no_verify: 是否跳过钩子
            
        Returns:
            bool: 是否成功
        """
        self._require_repository()
        
        args = ['commit']
        
        args.extend(['-m', message])
        
        if all_files:
            args.append('-a')
        
        if amend:
            args.append('--amend')
        
        if no_verify:
            args.append('--no-verify')
        
        try:
            self._run_git(*args)
            return True
        except GitCommandError:
            return False
    
    # ==========================================================================
    # 仓库统计
    # ==========================================================================
    
    def get_stats(self) -> GitLogStats:
        """
        获取仓库统计信息
        
        Returns:
            GitLogStats: 统计信息
        """
        self._require_repository()
        
        # 总提交数
        total_commits = 0
        try:
            result = self._run_git('rev-list', '--count', 'HEAD')
            total_commits = int(result.stdout.strip())
        except GitCommandError:
            pass
        
        # 分支数
        branches = self.branch()
        total_branches = len(branches)
        
        # 标签数
        tags = self.tag()
        total_tags = len(tags)
        
        # 文件数
        total_files = 0
        try:
            result = self._run_git('ls-files')
            total_files = len([l for l in result.stdout.strip().split('\n') if l])
        except GitCommandError:
            pass
        
        # 首次和最后提交时间
        first_commit_date = None
        last_commit_date = None
        
        if total_commits > 0:
            try:
                result = self._run_git(
                    'log', '--format=%ai', '--reverse', '-n1'
                )
                date_str = result.stdout.strip()
                if date_str:
                    first_commit_date = _parse_git_date(date_str)
            except GitCommandError:
                pass
            
            try:
                result = self._run_git(
                    'log', '--format=%ai', '-n1'
                )
                date_str = result.stdout.strip()
                if date_str:
                    last_commit_date = _parse_git_date(date_str)
            except GitCommandError:
                pass
        
        # 贡献者数（使用 set 去重）
        contributors = 0
        try:
            result = self._run_git(
                'log', '--format=%ae'
            )
            emails = set(l.strip() for l in result.stdout.strip().split('\n') if l.strip())
            contributors = len(emails)
        except GitCommandError:
            pass
        
        return GitLogStats(
            total_commits=total_commits,
            total_branches=total_branches,
            total_tags=total_tags,
            total_files=total_files,
            first_commit_date=first_commit_date,
            last_commit_date=last_commit_date,
            contributors=contributors
        )
    
    # ==========================================================================
    # 工具方法
    # ==========================================================================
    
    def get_version(self) -> str:
        """
        获取 Git 版本
        
        Returns:
            str: 版本字符串
        """
        self._check_git_installed()
        result = self._run_git('--version')
        return result.stdout.strip()
    
    def config(self, key: str, value: Optional[str] = None,
               global_config: bool = False) -> Optional[str]:
        """
        获取或设置配置
        
        Args:
            key: 配置键
            value: 配置值（None 表示获取）
            global_config: 是否全局配置
            
        Returns:
            Optional[str]: 配置值（获取时）
        """
        self._check_git_installed()
        
        args = ['config']
        
        if global_config:
            args.append('--global')
        
        args.append(key)
        
        if value is not None:
            args.append(value)
            self._run_git(*args)
            return None
        else:
            try:
                result = self._run_git(*args)
                return result.stdout.strip()
            except GitCommandError:
                return None


# =============================================================================
# 模块级函数（便捷使用）
# =============================================================================

def is_repository(path: Optional[Union[str, Path]] = None) -> bool:
    """检查路径是否为 Git 仓库"""
    git = GitUtils(path)
    return git.is_repository()


def status(path: Optional[Union[str, Path]] = None) -> GitStatusResult:
    """获取仓库状态"""
    git = GitUtils(path)
    return git.status()


def log(path: Optional[Union[str, Path]] = None, max_count: int = 10) -> List[GitCommit]:
    """获取提交历史"""
    git = GitUtils(path)
    return git.log(max_count=max_count)


def branch(path: Optional[Union[str, Path]] = None) -> List[GitBranch]:
    """获取分支列表"""
    git = GitUtils(path)
    return git.branch()


def current_branch(path: Optional[Union[str, Path]] = None) -> str:
    """获取当前分支"""
    git = GitUtils(path)
    return git.current_branch()


def diff(path: Optional[Union[str, Path]] = None, staged: bool = False) -> List[GitDiff]:
    """获取差异"""
    git = GitUtils(path)
    return git.diff(staged=staged)


def get_stats(path: Optional[Union[str, Path]] = None) -> GitLogStats:
    """获取仓库统计"""
    git = GitUtils(path)
    return git.get_stats()


# =============================================================================
# CLI 入口
# =============================================================================

if __name__ == '__main__':
    import sys
    
    git = GitUtils()
    
    if not git.is_repository():
        print("Error: Not a git repository", file=sys.stderr)
        sys.exit(1)
    
    # 显示基本信息
    print(f"Repository: {git.get_root()}")
    print(f"Current branch: {git.current_branch()}")
    print(f"Git version: {git.get_version()}")
    print()
    
    # 显示状态
    status_result = git.status()
    print(f"Status: {'Clean' if status_result.is_clean else 'Has changes'}")
    if not status_result.is_clean:
        print(f"  Staged: {len(status_result.staged_changes)}")
        print(f"  Unstaged: {len(status_result.unstaged_changes)}")
        print(f"  Untracked: {len(status_result.untracked_files)}")
    print()
    
    # 显示统计
    stats = git.get_stats()
    print(f"Statistics:")
    print(f"  Commits: {stats.total_commits}")
    print(f"  Branches: {stats.total_branches}")
    print(f"  Tags: {stats.total_tags}")
    print(f"  Files: {stats.total_files}")
    print(f"  Contributors: {stats.contributors}")
