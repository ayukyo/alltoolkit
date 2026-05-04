"""
permission_utils - Unix 文件权限处理工具

提供完整的 Unix 文件权限解析、转换、计算功能，零外部依赖。
支持符号模式、数字模式、chmod 风格命令解析。

功能:
- 权限模式解析 (数字/符号/chmod 风格)
- 权限验证与检查
- umask 计算
- 权限比较与差异分析
- 权限推荐 (基于文件类型)
"""

import os
import stat
from typing import Optional, Dict, List, Tuple, Set, Union
from dataclasses import dataclass
from enum import IntFlag


class PermissionBit(IntFlag):
    """权限位标志"""
    # 其他用户权限
    OTHER_EXECUTE = stat.S_IXOTH   # 0o001
    OTHER_WRITE = stat.S_IWOTH      # 0o002
    OTHER_READ = stat.S_IROTH       # 0o004
    # 组权限
    GROUP_EXECUTE = stat.S_IXGRP    # 0o010
    GROUP_WRITE = stat.S_IWGRP      # 0o020
    GROUP_READ = stat.S_IRGRP       # 0o040
    # 所有者权限
    OWNER_EXECUTE = stat.S_IXUSR    # 0o100
    OWNER_WRITE = stat.S_IWUSR      # 0o200
    OWNER_READ = stat.S_IRUSR       # 0o400
    # 特殊权限
    STICKY_BIT = stat.S_ISVTX       # 0o1000
    SETGID = stat.S_ISGID           # 0o2000
    SETUID = stat.S_ISUID           # 0o4000


@dataclass
class PermissionInfo:
    """权限信息数据类"""
    mode: int  # 完整权限模式 (包含特殊位)
    owner_read: bool
    owner_write: bool
    owner_execute: bool
    group_read: bool
    group_write: bool
    group_execute: bool
    other_read: bool
    other_write: bool
    other_execute: bool
    setuid: bool
    setgid: bool
    sticky: bool
    
    @property
    def octal(self) -> str:
        """返回八进制表示 (4位，包含特殊位)"""
        return f"{self.mode:04o}"
    
    @property
    def octal_short(self) -> str:
        """返回八进制表示 (3位，不含特殊位)"""
        return f"{self.mode & 0o777:03o}"
    
    @property
    def symbolic(self) -> str:
        """返回符号表示 (如 rwxr-xr-x)"""
        return PermissionUtils.to_symbolic(self.mode)


class PermissionUtils:
    """权限处理工具类"""
    
    # 权限字符映射
    CHAR_MAP = {
        'r': stat.S_IROTH,
        'w': stat.S_IWOTH,
        'x': stat.S_IXOTH,
        's': stat.S_IXOTH,  # setuid/setgid 时的执行位
        't': stat.S_IXOTH,  # sticky 时的执行位
    }
    
    # 特殊位映射
    SPECIAL_BITS = {
        'u': stat.S_ISUID,
        'g': stat.S_ISGID,
        't': stat.S_ISVTX,
    }
    
    # 文件类型推荐权限
    RECOMMENDED_PERMISSIONS = {
        'file': 0o644,           # 普通文件
        'executable': 0o755,      # 可执行文件
        'dir': 0o755,             # 目录
        'private_file': 0o600,    # 私有文件
        'private_dir': 0o700,     # 私有目录
        'script': 0o755,          # 脚本文件
        'config': 0o600,          # 配置文件
        'secret': 0o600,          # 敏感文件
        'log': 0o644,             # 日志文件
        'temp': 0o600,            # 临时文件
        'shared_file': 0o664,     # 共享文件
        'shared_dir': 0o2775,     # 共享目录 (setgid)
    }
    
    @staticmethod
    def parse(mode: Union[int, str]) -> PermissionInfo:
        """
        解析权限模式，返回详细信息
        
        Args:
            mode: 权限模式，可以是:
                - 整数 (如 0o755, 493)
                - 八进制字符串 (如 "755", "0755")
                - 符号字符串 (如 "rwxr-xr-x")
                
        Returns:
            PermissionInfo 对象
        """
        if isinstance(mode, int):
            perm_mode = mode
        elif isinstance(mode, str):
            mode = mode.strip()
            # 尝试解析为八进制
            if mode.isdigit():
                perm_mode = int(mode, 8) if not mode.startswith('0') else int(mode, 8)
            else:
                # 解析符号模式
                perm_mode = PermissionUtils.from_symbolic(mode)
        else:
            raise TypeError(f"不支持的权限类型: {type(mode)}")
        
        return PermissionInfo(
            mode=perm_mode,
            owner_read=bool(perm_mode & stat.S_IRUSR),
            owner_write=bool(perm_mode & stat.S_IWUSR),
            owner_execute=bool(perm_mode & stat.S_IXUSR),
            group_read=bool(perm_mode & stat.S_IRGRP),
            group_write=bool(perm_mode & stat.S_IWGRP),
            group_execute=bool(perm_mode & stat.S_IXGRP),
            other_read=bool(perm_mode & stat.S_IROTH),
            other_write=bool(perm_mode & stat.S_IWOTH),
            other_execute=bool(perm_mode & stat.S_IXOTH),
            setuid=bool(perm_mode & stat.S_ISUID),
            setgid=bool(perm_mode & stat.S_ISGID),
            sticky=bool(perm_mode & stat.S_ISVTX),
        )
    
    @staticmethod
    def from_symbolic(symbolic: str) -> int:
        """
        将符号权限转换为数字模式
        
        Args:
            symbolic: 符号权限字符串 (如 "rwxr-xr-x" 或 "rwsr-xr-x")
            
        Returns:
            权限数字模式
        """
        symbolic = symbolic.strip()
        
        if len(symbolic) != 9:
            raise ValueError(f"无效的符号权限: {symbolic}")
        
        mode = 0
        # 所有者权限 (字符 0-2)
        if symbolic[0] == 'r':
            mode |= stat.S_IRUSR
        if symbolic[1] == 'w':
            mode |= stat.S_IWUSR
        if symbolic[2] in ('x', 's'):
            mode |= stat.S_IXUSR
        if symbolic[2] in ('s', 'S'):
            mode |= stat.S_ISUID
        
        # 组权限 (字符 3-5)
        if symbolic[3] == 'r':
            mode |= stat.S_IRGRP
        if symbolic[4] == 'w':
            mode |= stat.S_IWGRP
        if symbolic[5] in ('x', 's'):
            mode |= stat.S_IXGRP
        if symbolic[5] in ('s', 'S'):
            mode |= stat.S_ISGID
        
        # 其他用户权限 (字符 6-8)
        if symbolic[6] == 'r':
            mode |= stat.S_IROTH
        if symbolic[7] == 'w':
            mode |= stat.S_IWOTH
        if symbolic[8] in ('x', 't'):
            mode |= stat.S_IXOTH
        if symbolic[8] in ('t', 'T'):
            mode |= stat.S_ISVTX
        
        return mode
    
    @staticmethod
    def to_symbolic(mode: int, include_special: bool = True) -> str:
        """
        将数字权限转换为符号表示
        
        Args:
            mode: 权限数字模式
            include_special: 是否显示特殊权限位
            
        Returns:
            符号权限字符串 (如 "rwxr-xr-x")
        """
        def get_char(perm: int, read_bit: int, write_bit: int, exec_bit: int,
                     special_bit: int = 0, special_char: str = '') -> str:
            chars = []
            chars.append('r' if perm & read_bit else '-')
            chars.append('w' if perm & write_bit else '-')
            
            if include_special and (perm & special_bit):
                chars.append(special_char if perm & exec_bit else special_char.upper())
            else:
                chars.append('x' if perm & exec_bit else '-')
            return ''.join(chars)
        
        owner = get_char(mode, stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR,
                        stat.S_ISUID, 's')
        group = get_char(mode, stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
                        stat.S_ISGID, 's')
        other = get_char(mode, stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH,
                        stat.S_ISVTX, 't')
        
        return owner + group + other
    
    @staticmethod
    def parse_chmod_mode(chmod_str: str, current_mode: int = 0o644) -> int:
        """
        解析 chmod 风格的权限字符串
        
        支持格式:
        - "755" / "0755" - 绝对模式
        - "u+x" - 给所有者添加执行权限
        - "g-w" - 移除组写权限
        - "o=r" - 设置其他用户只读
        - "a+x" / "+x" - 所有人添加执行权限
        - "u=rwx,go=rx" - 复合模式
        
        Args:
            chmod_str: chmod 风格的权限字符串
            current_mode: 当前权限模式 (用于相对修改)
            
        Returns:
            新的权限模式
        """
        chmod_str = chmod_str.strip()
        
        # 空字符串返回当前模式
        if not chmod_str:
            return current_mode
        
        # 绝对数字模式
        if chmod_str.isdigit():
            return int(chmod_str, 8)
        
        # 解析符号模式
        mode = current_mode
        
        # 分割多个规则 (逗号分隔)
        rules = chmod_str.split(',')
        
        for rule in rules:
            rule = rule.strip()
            
            # 解析 who
            who_chars = set()
            i = 0
            while i < len(rule) and rule[i] in 'ugoa':
                who_chars.add(rule[i])
                i += 1
            
            # 默认为 'a' (all)
            if not who_chars:
                who_chars = {'a'}
            
            # 展开 'a' 为 'ugo'
            if 'a' in who_chars:
                who_chars = {'u', 'g', 'o'}
            
            # 获取操作符
            if i >= len(rule):
                raise ValueError(f"无效的 chmod 模式: {chmod_str}")
            
            op = rule[i]
            i += 1
            
            # 获取权限值
            perm_str = rule[i:] if i < len(rule) else ''
            
            # 计算权限值
            perm_value = 0
            for p in perm_str:
                if p == 'r':
                    perm_value |= 4
                elif p == 'w':
                    perm_value |= 2
                elif p == 'x':
                    perm_value |= 1
                elif p == 's':
                    perm_value |= 8  # 特殊位标记
                elif p == 't':
                    perm_value |= 16  # sticky 位标记
            
            # 应用到各个用户类别
            for who in who_chars:
                shift = {'u': 6, 'g': 3, 'o': 0}[who]
                
                # 计算基础权限位
                base_perm = (perm_value & 7) << shift
                
                # 应用操作
                if op == '+':
                    mode |= base_perm
                    if perm_value & 8:  # setuid/setgid
                        if who == 'u':
                            mode |= stat.S_ISUID
                        elif who == 'g':
                            mode |= stat.S_ISGID
                    if perm_value & 16 and who == 'o':  # sticky
                        mode |= stat.S_ISVTX
                elif op == '-':
                    mode &= ~base_perm
                    if perm_value & 8:
                        if who == 'u':
                            mode &= ~stat.S_ISUID
                        elif who == 'g':
                            mode &= ~stat.S_ISGID
                    if perm_value & 16 and who == 'o':
                        mode &= ~stat.S_ISVTX
                elif op == '=':
                    # 清除该类别的权限
                    mask = 7 << shift
                    mode &= ~mask
                    # 设置新权限
                    mode |= base_perm
        
        return mode
    
    @staticmethod
    def apply_umask(mode: int, umask: Optional[int] = None) -> int:
        """
        应用 umask 到权限模式
        
        Args:
            mode: 原始权限模式
            umask: umask 值，默认使用当前系统的 umask
            
        Returns:
            应用 umask 后的权限模式
        """
        if umask is None:
            umask = os.umask(0o022)
            os.umask(umask)
        
        return mode & ~umask
    
    @staticmethod
    def get_umask() -> int:
        """获取当前系统的 umask 值"""
        current = os.umask(0)
        os.umask(current)
        return current
    
    @staticmethod
    def compare(mode1: int, mode2: int) -> Dict[str, any]:
        """
        比较两个权限模式的差异
        
        Args:
            mode1: 第一个权限模式
            mode2: 第二个权限模式
            
        Returns:
            包含差异信息的字典
        """
        diff = mode1 ^ mode2
        added = mode2 & ~mode1
        removed = mode1 & ~mode2
        
        return {
            'equal': mode1 == mode2,
            'difference': diff,
            'difference_octal': f"{diff:04o}",
            'added': added,
            'added_octal': f"{added:04o}",
            'added_symbolic': PermissionUtils.to_symbolic(added),
            'removed': removed,
            'removed_octal': f"{removed:04o}",
            'removed_symbolic': PermissionUtils.to_symbolic(removed),
            'mode1_symbolic': PermissionUtils.to_symbolic(mode1),
            'mode2_symbolic': PermissionUtils.to_symbolic(mode2),
        }
    
    @staticmethod
    def is_more_restrictive(mode1: int, mode2: int) -> bool:
        """
        判断 mode1 是否比 mode2 更严格
        
        Args:
            mode1: 第一个权限模式
            mode2: 第二个权限模式
            
        Returns:
            True 如果 mode1 比 mode2 更严格
        """
        # mode1 必须是 mode2 的子集
        return (mode1 & mode2) == mode1 and mode1 < mode2
    
    @staticmethod
    def get_least_privilege(modes: List[int]) -> int:
        """
        获取多个权限模式的交集 (最小权限)
        
        Args:
            modes: 权限模式列表
            
        Returns:
            所有模式的交集
        """
        if not modes:
            return 0
        
        result = modes[0]
        for mode in modes[1:]:
            result &= mode
        return result
    
    @staticmethod
    def get_most_privilege(modes: List[int]) -> int:
        """
        获取多个权限模式的并集 (最大权限)
        
        Args:
            modes: 权限模式列表
            
        Returns:
            所有模式的并集
        """
        if not modes:
            return 0
        
        result = modes[0]
        for mode in modes[1:]:
            result |= mode
        return result
    
    @staticmethod
    def recommend(file_type: str, is_executable: bool = False,
                  is_private: bool = False, is_shared: bool = False) -> int:
        """
        根据文件类型推荐权限
        
        Args:
            file_type: 文件类型 (file/dir/script/config/secret/log)
            is_executable: 是否可执行
            is_private: 是否私有
            is_shared: 是否共享
            
        Returns:
            推荐的权限模式
        """
        if is_private:
            key = f'private_{file_type}'
            if key in PermissionUtils.RECOMMENDED_PERMISSIONS:
                return PermissionUtils.RECOMMENDED_PERMISSIONS[key]
        
        if is_shared:
            key = f'shared_{file_type}'
            if key in PermissionUtils.RECOMMENDED_PERMISSIONS:
                return PermissionUtils.RECOMMENDED_PERMISSIONS[key]
        
        if is_executable and file_type == 'file':
            return PermissionUtils.RECOMMENDED_PERMISSIONS['executable']
        
        if file_type in PermissionUtils.RECOMMENDED_PERMISSIONS:
            return PermissionUtils.RECOMMENDED_PERMISSIONS[file_type]
        
        return 0o644  # 默认权限
    
    @staticmethod
    def check_permission(path: str, mode: int) -> Dict[str, bool]:
        """
        检查路径的权限状态
        
        Args:
            path: 文件路径
            mode: 期望的权限模式
            
        Returns:
            各权限检查结果的字典
        """
        result = {
            'exists': os.path.exists(path),
            'is_file': os.path.isfile(path) if os.path.exists(path) else False,
            'is_dir': os.path.isdir(path) if os.path.exists(path) else False,
            'can_read': False,
            'can_write': False,
            'can_execute': False,
            'actual_mode': None,
            'expected_mode': mode,
            'match': False,
        }
        
        if result['exists']:
            try:
                actual_mode = os.stat(path).st_mode
                result['actual_mode'] = stat.S_IMODE(actual_mode)
                result['match'] = result['actual_mode'] == mode
                result['can_read'] = os.access(path, os.R_OK)
                result['can_write'] = os.access(path, os.W_OK)
                result['can_execute'] = os.access(path, os.X_OK)
            except OSError:
                pass
        
        return result
    
    @staticmethod
    def explain(mode: int) -> str:
        """
        解释权限模式的含义
        
        Args:
            mode: 权限模式
            
        Returns:
            人类可读的解释文本
        """
        info = PermissionUtils.parse(mode)
        lines = [
            f"权限模式: {info.octal} ({info.octal_short})",
            f"符号表示: {info.symbolic}",
            "",
            "所有者权限:",
            f"  读: {'是' if info.owner_read else '否'}",
            f"  写: {'是' if info.owner_write else '否'}",
            f"  执行: {'是' if info.owner_execute else '否'}",
            "",
            "组权限:",
            f"  读: {'是' if info.group_read else '否'}",
            f"  写: {'是' if info.group_write else '否'}",
            f"  执行: {'是' if info.group_execute else '否'}",
            "",
            "其他用户权限:",
            f"  读: {'是' if info.other_read else '否'}",
            f"  写: {'是' if info.other_write else '否'}",
            f"  执行: {'是' if info.other_execute else '否'}",
        ]
        
        # 特殊权限
        special = []
        if info.setuid:
            special.append("setuid (以所有者身份执行)")
        if info.setgid:
            special.append("setgid (以组身份执行)")
        if info.sticky:
            special.append("sticky (只有所有者可删除)")
        
        if special:
            lines.extend(["", "特殊权限:"])
            lines.extend([f"  {s}" for s in special])
        
        return "\n".join(lines)
    
    @staticmethod
    def to_chmod_command(mode: int) -> str:
        """
        生成 chmod 命令
        
        Args:
            mode: 权限模式
            
        Returns:
            chmod 命令字符串
        """
        return f"chmod {mode:04o} <file>"
    
    @staticmethod
    def diff_summary(mode1: int, mode2: int) -> str:
        """
        生成权限差异摘要
        
        Args:
            mode1: 第一个权限模式
            mode2: 第二个权限模式
            
        Returns:
            人类可读的差异摘要
        """
        if mode1 == mode2:
            return "权限相同"
        
        comparison = PermissionUtils.compare(mode1, mode2)
        lines = [
            f"权限变化: {comparison['mode1_symbolic']} -> {comparison['mode2_symbolic']}",
            f"数字变化: {mode1:04o} -> {mode2:04o}",
        ]
        
        if comparison['added']:
            lines.append(f"新增权限: {comparison['added_symbolic']} ({comparison['added_octal']})")
        
        if comparison['removed']:
            lines.append(f"移除权限: {comparison['removed_symbolic']} ({comparison['removed_octal']})")
        
        return "\n".join(lines)


# 便捷函数
def parse(mode: Union[int, str]) -> PermissionInfo:
    """解析权限模式的便捷函数"""
    return PermissionUtils.parse(mode)


def to_symbolic(mode: int) -> str:
    """转换为符号表示的便捷函数"""
    return PermissionUtils.to_symbolic(mode)


def to_octal(mode: int, include_special: bool = True) -> str:
    """转换为八进制表示的便捷函数"""
    if include_special:
        return f"{mode:04o}"
    return f"{mode & 0o777:03o}"


def compare(mode1: int, mode2: int) -> Dict[str, any]:
    """比较两个权限模式的便捷函数"""
    return PermissionUtils.compare(mode1, mode2)


def recommend(file_type: str, **kwargs) -> int:
    """获取推荐权限的便捷函数"""
    return PermissionUtils.recommend(file_type, **kwargs)


if __name__ == "__main__":
    # 简单演示
    print("=== Permission Utils Demo ===\n")
    
    # 解析不同格式
    print("1. 解析不同格式:")
    print(f"   数字: {parse(0o755)}")
    print(f"   八进制字符串: {parse('644')}")
    print(f"   符号: {parse('rwxr-xr-x')}")
    
    print("\n2. 权限解释:")
    print(PermissionUtils.explain(0o755))
    
    print("\n3. chmod 风格解析:")
    print(f"   'u+x' 从 644: {PermissionUtils.parse_chmod_mode('u+x', 0o644):04o}")
    print(f"   'go-w' 从 755: {PermissionUtils.parse_chmod_mode('go-w', 0o755):04o}")
    print(f"   'a+x' 从 644: {PermissionUtils.parse_chmod_mode('a+x', 0o644):04o}")
    print(f"   'u=rwx,go=rx' 从 000: {PermissionUtils.parse_chmod_mode('u=rwx,go=rx', 0):04o}")
    
    print("\n4. 权限比较:")
    print(PermissionUtils.diff_summary(0o644, 0o755))
    
    print("\n5. 推荐权限:")
    print(f"   普通文件: {PermissionUtils.recommend('file'):04o}")
    print(f"   可执行文件: {PermissionUtils.recommend('executable'):04o}")
    print(f"   目录: {PermissionUtils.recommend('dir'):04o}")
    print(f"   私有文件: {PermissionUtils.recommend('file', is_private=True):04o}")