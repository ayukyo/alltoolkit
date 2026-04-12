# Git Utils 🌿

**Python Git 仓库操作工具库**

零依赖、生产就绪的 Git 仓库操作工具，通过调用 git 命令行实现所有功能。

---

## ✨ 特性

- **零依赖** - 仅使用 Python 标准库（subprocess, pathlib, re, json）
- **全面覆盖** - 支持状态查询、提交历史、分支/标签管理、远程操作等
- **类型安全** - 完整的类型注解和数据类
- **错误处理** - 清晰的异常层次结构
- **跨平台** - 支持 Linux、macOS、Windows
- **模块级函数** - 提供便捷的函数式接口

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 或者从 AllToolkit 克隆
git clone https://github.com/ayukyo/alltoolkit.git
cd alltoolkit/Python/git_utils
```

**依赖要求：**
- Python 3.7+
- Git 命令行工具已安装并在 PATH 中

---

## 🚀 快速开始

### 基本使用

```python
from git_utils.mod import GitUtils

# 初始化（默认为当前目录）
git = GitUtils()

# 检查是否为仓库
if git.is_repository():
    print(f"仓库根目录：{git.get_root()}")
    print(f"当前分支：{git.current_branch()}")
    
    # 获取状态
    status = git.status()
    print(f"状态：{'干净' if status.is_clean else '有更改'}")
    
    # 获取提交历史
    commits = git.log(max_count=5)
    for commit in commits:
        print(f"{commit.short_hash}: {commit.message}")
```

### 模块级函数

```python
from git_utils.mod import (
    is_repository,
    status,
    log,
    branch,
    current_branch,
    get_stats,
)

# 直接使用
if is_repository():
    print(f"分支：{current_branch()}")
    
    stats = get_stats()
    print(f"提交数：{stats.total_commits}")
    print(f"贡献者：{stats.contributors}")
```

---

## 📖 API 参考

### GitUtils 类

#### 初始化

```python
git = GitUtils(repo_path=None)  # 默认为当前目录
```

#### 仓库信息

| 方法 | 描述 | 返回 |
|------|------|------|
| `is_repository()` | 检查是否为 Git 仓库 | `bool` |
| `get_root()` | 获取仓库根目录 | `Path` |
| `get_git_dir()` | 获取 .git 目录 | `Path` |
| `get_version()` | 获取 Git 版本 | `str` |

#### 状态与差异

| 方法 | 描述 | 返回 |
|------|------|------|
| `status()` | 获取仓库状态 | `GitStatusResult` |
| `diff(path, staged, ref1, ref2)` | 获取差异统计 | `List[GitDiff]` |
| `diff_patch(path, staged, ref1, ref2)` | 获取补丁格式差异 | `str` |

#### 提交历史

| 方法 | 描述 | 返回 |
|------|------|------|
| `log(max_count, branch, since, until, author)` | 获取提交历史 | `List[GitCommit]` |
| `show(ref)` | 显示提交详情 | `GitCommit` |

#### 分支操作

| 方法 | 描述 | 返回 |
|------|------|------|
| `branch(list_all)` | 获取分支列表 | `List[GitBranch]` |
| `current_branch()` | 获取当前分支 | `str` |
| `create_branch(name, start_point, force)` | 创建分支 | `bool` |
| `checkout(branch_or_commit, create)` | 切换分支 | `bool` |
| `merge(branch, strategy, no_ff, message)` | 合并分支 | `bool` |

#### 标签操作

| 方法 | 描述 | 返回 |
|------|------|------|
| `tag(pattern)` | 获取标签列表 | `List[str]` |
| `create_tag(name, message, commit, annotated)` | 创建标签 | `bool` |
| `delete_tag(name)` | 删除标签 | `bool` |

#### 远程操作

| 方法 | 描述 | 返回 |
|------|------|------|
| `remote(verbose)` | 获取远程列表 | `List[GitRemote]` |
| `add_remote(name, url)` | 添加远程 | `bool` |
| `remove_remote(name)` | 移除远程 | `bool` |
| `fetch(remote, all_remotes, prune)` | 获取更新 | `bool` |
| `pull(remote, branch, rebase)` | 拉取更新 | `bool` |
| `push(remote, branch, force, set_upstream)` | 推送更新 | `bool` |

#### 暂存区操作

| 方法 | 描述 | 返回 |
|------|------|------|
| `add(pathspec, all_files)` | 添加文件 | `bool` |
| `restore(pathspec, staged, worktree)` | 恢复文件 | `bool` |
| `reset(mode, commit)` | 重置仓库 | `bool` |
| `clean(force, dry_run, directories)` | 清理未跟踪文件 | `bool` |

#### 提交操作

| 方法 | 描述 | 返回 |
|------|------|------|
| `commit(message, all_files, amend, no_verify)` | 创建提交 | `bool` |

#### 配置与统计

| 方法 | 描述 | 返回 |
|------|------|------|
| `config(key, value, global_config)` | 获取/设置配置 | `Optional[str]` |
| `get_stats()` | 获取仓库统计 | `GitLogStats` |

---

## 📊 数据结构

### GitStatusResult

仓库状态：

```python
@dataclass
class GitStatusResult:
    branch: str                      # 当前分支
    ahead: int = 0                   # 领先远程的提交数
    behind: int = 0                  # 落后远程的提交数
    staged_changes: List[GitStatusFile]  # 暂存的更改
    unstaged_changes: List[GitStatusFile]  # 未暂存的更改
    untracked_files: List[GitStatusFile]   # 未跟踪的文件
    is_clean: bool = True            # 是否干净
```

### GitStatusFile

文件状态：

```python
@dataclass
class GitStatusFile:
    path: str                        # 文件路径
    status: GitStatus                # 状态枚举
    staged: bool = False             # 是否已暂存
    old_path: Optional[str] = None   # 重命名时的旧路径
```

### GitStatus

文件状态枚举：

```python
class GitStatus(Enum):
    UNTRACKED = "untracked"                    # 未跟踪
    UNMODIFIED = "unmodified"                  # 未修改
    MODIFIED = "modified"                      # 已修改
    ADDED = "added"                            # 已添加
    DELETED = "deleted"                        # 已删除
    RENAMED = "renamed"                        # 已重命名
    COPIED = "copied"                          # 已复制
    UPDATED_BUT_UNMERGED = "updated_but_unmerged"  # 已更新但未合并
```

### GitCommit

提交信息：

```python
@dataclass
class GitCommit:
    hash: str                      # 完整 commit hash
    short_hash: str                # 短 hash（7 位）
    author: str                    # 作者名
    author_email: str              # 作者邮箱
    date: datetime                 # 提交时间
    message: str                   # 提交信息
    parent_hashes: List[str]       # 父提交 hashes
```

### GitBranch

分支信息：

```python
@dataclass
class GitBranch:
    name: str                      # 分支名
    is_current: bool = False       # 是否当前分支
    is_remote: bool = False        # 是否远程分支
    upstream: Optional[str] = None # 上游分支
    ahead: int = 0                 # 领先数
    behind: int = 0                # 落后数
```

### GitDiff

差异信息：

```python
@dataclass
class GitDiff:
    file_path: str                 # 文件路径
    changes_added: int = 0         # 新增行数
    changes_removed: int = 0       # 删除行数
    patch: str = ""                # 补丁内容
```

### GitLogStats

仓库统计：

```python
@dataclass
class GitLogStats:
    total_commits: int             # 总提交数
    total_branches: int            # 总分支数
    total_tags: int                # 总标签数
    total_files: int               # 总文件数
    first_commit_date: Optional[datetime]  # 首次提交时间
    last_commit_date: Optional[datetime]   # 最后提交时间
    contributors: int              # 贡献者数
```

---

## 💡 使用示例

### 1. 仓库状态检查

```python
from git_utils.mod import GitUtils

git = GitUtils('/path/to/repo')

if not git.is_repository():
    print("不是 Git 仓库")
    exit(1)

status = git.status()
print(f"分支：{status.branch}")
print(f"领先：{status.ahead}, 落后：{status.behind}")

if not status.is_clean:
    print("\n暂存的更改:")
    for f in status.staged_changes:
        print(f"  {f.status.value}: {f.path}")
    
    print("\n未暂存的更改:")
    for f in status.unstaged_changes:
        print(f"  {f.status.value}: {f.path}")
    
    print("\n未跟踪的文件:")
    for f in status.untracked_files:
        print(f"  {f.path}")
```

### 2. 提交历史分析

```python
from git_utils.mod import GitUtils, GitCommit

git = GitUtils()

# 获取最近 10 次提交
commits = git.log(max_count=10)

# 按作者分组
from collections import defaultdict
by_author = defaultdict(list)
for commit in commits:
    by_author[commit.author].append(commit)

for author, author_commits in by_author.items():
    print(f"\n{author} ({len(author_commits)} commits):")
    for commit in author_commits:
        print(f"  {commit.short_hash}: {commit.message}")

# 获取特定时间的提交
last_week = git.log(since='1 week ago')
print(f"\n本周提交：{len(last_week)}")
```

### 3. 分支管理

```python
from git_utils.mod import GitUtils

git = GitUtils()

# 列出所有分支
branches = git.branch(list_all=True)
for b in branches:
    marker = "*" if b.is_current else " "
    upstream = f" ({b.upstream})" if b.upstream else ""
    print(f"{marker} {b.name}{upstream}")

# 创建并切换新分支
if git.create_branch('feature/new-feature'):
    git.checkout('feature/new-feature')
    print("已创建并切换到 feature/new-feature")

# 合并分支
if git.merge('feature/new-feature', no_ff=True, message='Merge feature'):
    print("合并成功")
else:
    print("合并失败，可能有冲突")
```

### 4. 标签管理

```python
from git_utils.mod import GitUtils

git = GitUtils()

# 创建发布标签
git.create_tag(
    'v1.0.0',
    message='Release version 1.0.0',
    annotated=True
)

# 列出所有标签
tags = git.tag()
print(f"标签：{', '.join(tags)}")

# 匹配模式
v1_tags = git.tag(pattern='v1.*')
print(f"v1.x 标签：{', '.join(v1_tags)}")

# 删除标签
git.delete_tag('v1.0.0-beta')
```

### 5. 远程操作

```python
from git_utils.mod import GitUtils

git = GitUtils()

# 添加远程
git.add_remote('origin', 'https://github.com/user/repo.git')
git.add_remote('upstream', 'https://github.com/original/repo.git')

# 列出远程
remotes = git.remote()
for r in remotes:
    print(f"{r.name}: {r.fetch_url}")

# 获取更新
git.fetch(all_remotes=True, prune=True)

# 拉取并推送
if git.pull('origin', rebase=True):
    print("拉取成功")

if git.push('origin', set_upstream=True):
    print("推送成功")
```

### 6. 暂存区操作

```python
from git_utils.mod import GitUtils

git = GitUtils()

# 添加特定文件
git.add('src/main.py')

# 添加所有修改
git.add('', all_files=True)

# 查看暂存区差异
diffs = git.diff(staged=True)
for d in diffs:
    print(f"{d.file_path}: +{d.changes_added} -{d.changes_removed}")

# 恢复暂存的文件
git.restore('src/main.py', staged=True)

# 清理未跟踪文件
git.clean(dry_run=True)  # 先预览
git.clean(force=True, directories=True)  # 再执行
```

### 7. 仓库统计

```python
from git_utils.mod import GitUtils

git = GitUtils()

stats = git.get_stats()

print(f"=== 仓库统计 ===")
print(f"提交总数：{stats.total_commits}")
print(f"分支数：{stats.total_branches}")
print(f"标签数：{stats.total_tags}")
print(f"文件数：{stats.total_files}")
print(f"贡献者：{stats.contributors}")
print(f"首次提交：{stats.first_commit_date}")
print(f"最后提交：{stats.last_commit_date}")

# 转换为字典（用于 JSON 序列化）
stats_dict = stats.to_dict()
import json
print(json.dumps(stats_dict, indent=2))
```

### 8. 配置管理

```python
from git_utils.mod import GitUtils

git = GitUtils()

# 获取配置
name = git.config('user.name')
email = git.config('user.email')
print(f"{name} <{email}>")

# 设置配置
git.config('user.name', 'New Name')
git.config('user.email', 'new@example.com')

# 全局配置
git.config('core.editor', 'vim', global_config=True)
```

### 9. 错误处理

```python
from git_utils.mod import (
    GitUtils,
    GitError,
    GitNotInstalledError,
    GitNotRepositoryError,
    GitCommandError,
)

try:
    git = GitUtils('/not/a/repo')
    git.status()
except GitNotRepositoryError as e:
    print(f"错误：{e.message}")

try:
    git = GitUtils()
    git.checkout('nonexistent-branch')
except GitCommandError as e:
    print(f"命令失败：{e.command}")
    print(f"返回码：{e.returncode}")
    print(f"错误：{e.stderr}")

try:
    git = GitUtils()
    git.get_version()
except GitNotInstalledError:
    print("Git 未安装或不在 PATH 中")
```

---

## 🧪 测试

运行测试套件：

```bash
cd /path/to/AllToolkit/Python/git_utils
python git_utils_test.py
```

测试覆盖：

- ✅ 仓库检测与初始化
- ✅ 状态查询（干净、未跟踪、修改、暂存）
- ✅ 提交历史（基本查询、限制数量、详情）
- ✅ 分支操作（列表、创建、切换、合并）
- ✅ 标签操作（创建、列表、删除、模式匹配）
- ✅ 远程操作（添加、移除、fetch）
- ✅ 暂存区操作（add、restore、reset、clean）
- ✅ 提交操作（基本、all_files、amend）
- ✅ 差异操作（unstaged、staged、patch）
- ✅ 仓库统计
- ✅ 配置管理
- ✅ 错误处理
- ✅ 数据类序列化

---

## 📁 文件结构

```
git_utils/
├── mod.py                      # 主模块
├── git_utils_test.py           # 测试套件
├── README.md                   # 本文档
└── examples/
    └── usage_examples.py       # 使用示例
```

---

## 🔧 高级用法

### 自定义 Git 路径

```python
import os
os.environ['GIT_EXEC_PATH'] = '/custom/git/path'

from git_utils.mod import GitUtils
git = GitUtils()
```

### 批量操作多个仓库

```python
from git_utils.mod import GitUtils, is_repository
from pathlib import Path

repos = Path('/path/to/repos')
results = []

for repo_dir in repos.iterdir():
    if repo_dir.is_dir() and is_repository(repo_dir):
        git = GitUtils(repo_dir)
        stats = git.get_stats()
        results.append({
            'name': repo_dir.name,
            'commits': stats.total_commits,
            'branches': stats.total_branches,
        })

# 排序输出
results.sort(key=lambda x: x['commits'], reverse=True)
for r in results:
    print(f"{r['name']}: {r['commits']} commits")
```

### 与 CI/CD 集成

```python
from git_utils.mod import GitUtils

git = GitUtils()

# 检查是否有未提交的更改
status = git.status()
if not status.is_clean:
    print("错误：工作区有未提交的更改")
    exit(1)

# 获取当前分支
branch = git.current_branch()
if branch != 'main':
    print(f"警告：当前分支为 {branch}，不是 main")

# 检查是否落后远程
if status.behind > 0:
    print(f"警告：落后远程 {status.behind} 个提交")
    exit(1)

print("CI 检查通过")
```

---

## 📝 注意事项

1. **Git 依赖**: 需要系统安装 Git 命令行工具
2. **性能**: 大量操作时建议复用 GitUtils 实例
3. **超时**: 网络操作（fetch/pull/push）默认超时 120-300 秒
4. **编码**: 默认使用 UTF-8 编码
5. **兼容性**: Python 3.7+，Git 2.0+

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- 报告 Bug
- 请求新功能
- 改进文档
- 添加测试用例

---

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE)

---

## 🔗 相关链接

- [AllToolkit 主项目](../../README.md)
- [Python 工具列表](../README.md)
- [Git 官方文档](https://git-scm.com/doc)

---

**最后更新**: 2026-04-11
