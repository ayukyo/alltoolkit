"""
permission_utils 使用示例

展示权限解析、转换、比较等功能的实际应用。
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from permission_utils.mod import (
    PermissionUtils, parse, to_symbolic, to_octal,
    compare, recommend
)


def example_basic_parsing():
    """示例: 基本权限解析"""
    print("=" * 60)
    print("示例 1: 基本权限解析")
    print("=" * 60)
    
    # 解析不同格式的权限
    modes = [
        0o755,           # 八进制数字
        "644",           # 八进制字符串
        "rwxr-xr-x",     # 符号字符串
        "rw-r--r--",     # 另一个符号字符串
    ]
    
    for mode in modes:
        info = parse(mode)
        print(f"\n解析 '{mode}':")
        print(f"  八进制: {info.octal}")
        print(f"  符号: {info.symbolic}")
        print(f"  所有者: {'读' if info.owner_read else '-'}{'写' if info.owner_write else '-'}{'执行' if info.owner_execute else '-'}")
        print(f"  组: {'读' if info.group_read else '-'}{'写' if info.group_write else '-'}{'执行' if info.group_execute else '-'}")
        print(f"  其他: {'读' if info.other_read else '-'}{'写' if info.other_write else '-'}{'执行' if info.other_execute else '-'}")


def example_chmod_style_parsing():
    """示例: chmod 风格解析"""
    print("\n" + "=" * 60)
    print("示例 2: chmod 风格权限解析")
    print("=" * 60)
    
    chmod_examples = [
        ("755", 0o644),         # 绝对模式
        ("u+x", 0o644),         # 给所有者添加执行权限
        ("g+w", 0o644),         # 给组添加写权限
        ("o-w", 0o777),         # 移除其他用户的写权限
        ("a+x", 0o644),         # 所有人添加执行权限
        ("+x", 0o644),          # 默认所有人添加执行权限
        ("u=rwx,go=rx", 0o000), # 复合模式
        ("go-wx", 0o777),       # 移除组和其他用户的写和执行权限
    ]
    
    for chmod_str, current in chmod_examples:
        result = PermissionUtils.parse_chmod_mode(chmod_str, current)
        print(f"\nchmod {chmod_str} (从 {current:04o})")
        print(f"  结果: {result:04o} ({to_symbolic(result)})")


def example_special_permissions():
    """示例: 特殊权限 (setuid, setgid, sticky)"""
    print("\n" + "=" * 60)
    print("示例 3: 特殊权限处理")
    print("=" * 60)
    
    special_modes = [
        (0o4755, "setuid - 以所有者身份执行"),
        (0o2755, "setgid - 以组身份执行"),
        (0o1755, "sticky - 只有所有者可删除"),
        (0o7777, "全部特殊权限"),
    ]
    
    for mode, description in special_modes:
        info = parse(mode)
        print(f"\n{description}:")
        print(f"  权限: {info.octal} ({info.symbolic})")
        print(f"  setuid: {'是' if info.setuid else '否'}")
        print(f"  setgid: {'是' if info.setgid else '否'}")
        print(f"  sticky: {'是' if info.sticky else '否'}")


def example_permission_comparison():
    """示例: 权限比较"""
    print("\n" + "=" * 60)
    print("示例 4: 权限比较")
    print("=" * 60)
    
    mode_pairs = [
        (0o644, 0o755),
        (0o755, 0o750),
        (0o644, 0o644),
    ]
    
    for mode1, mode2 in mode_pairs:
        print(f"\n比较 {mode1:04o} vs {mode2:04o}:")
        print(PermissionUtils.diff_summary(mode1, mode2))


def example_umask_calculation():
    """示例: umask 计算"""
    print("\n" + "=" * 60)
    print("示例 5: umask 计算")
    print("=" * 60)
    
    umasks = [0o022, 0o002, 0o077, 0o027]
    base_permission = 0o666  # 默认文件权限
    
    for umask in umasks:
        result = PermissionUtils.apply_umask(base_permission, umask)
        print(f"\numask {umask:03o}:")
        print(f"  基础权限: {base_permission:04o} ({to_symbolic(base_permission)})")
        print(f"  结果权限: {result:04o} ({to_symbolic(result)})")
    
    print(f"\n当前系统 umask: {PermissionUtils.get_umask():03o}")


def example_recommended_permissions():
    """示例: 推荐权限"""
    print("\n" + "=" * 60)
    print("示例 6: 推荐权限")
    print("=" * 60)
    
    file_types = [
        ('file', {}),
        ('executable', {}),
        ('dir', {}),
        ('script', {}),
        ('config', {}),
        ('secret', {}),
        ('log', {}),
        ('file', {'is_private': True}),
        ('dir', {'is_private': True}),
        ('file', {'is_shared': True}),
        ('dir', {'is_shared': True}),
    ]
    
    print("\n文件类型推荐权限:")
    for file_type, kwargs in file_types:
        perm = recommend(file_type, **kwargs)
        extra = f" ({', '.join(f'{k}={v}' for k, v in kwargs.items())})" if kwargs else ""
        print(f"  {file_type}{extra}: {perm:04o} ({to_symbolic(perm)})")


def example_permission_explanation():
    """示例: 权限解释"""
    print("\n" + "=" * 60)
    print("示例 7: 权限解释")
    print("=" * 60)
    
    modes = [0o755, 0o644, 0o700, 0o4755]
    
    for mode in modes:
        print(f"\n{'─' * 40}")
        print(PermissionUtils.explain(mode))


def example_permission_security():
    """示例: 权限安全检查"""
    print("\n" + "=" * 60)
    print("示例 8: 权限安全检查")
    print("=" * 60)
    
    # 检查权限是否过于宽松
    def check_security(mode):
        info = parse(mode)
        warnings = []
        
        if info.other_write:
            warnings.append("⚠️ 其他用户有写权限")
        if info.other_execute and info.owner_write:
            warnings.append("⚠️ 其他用户可执行且所有者可写 - 可能被利用")
        if info.group_write and info.other_read:
            warnings.append("⚠️ 组可写且其他用户可读")
        if mode == 0o777:
            warnings.append("🚨 完全开放权限 - 极其危险!")
        
        return warnings
    
    test_modes = [
        (0o755, "标准目录"),
        (0o644, "标准文件"),
        (0o777, "完全开放"),
        (0o666, "所有人可写"),
        (0o757, "其他用户可写可执行"),
    ]
    
    for mode, description in test_modes:
        warnings = check_security(mode)
        status = "✅ 安全" if not warnings else "\n    ".join(warnings)
        print(f"\n{description} ({mode:04o}):")
        print(f"  {status}")


def example_permission_aggregation():
    """示例: 权限聚合"""
    print("\n" + "=" * 60)
    print("示例 9: 权限聚合计算")
    print("=" * 60)
    
    modes = [0o755, 0o644, 0o750, 0o700]
    
    print(f"输入权限: {[f'{m:04o}' for m in modes]}")
    
    least = PermissionUtils.get_least_privilege(modes)
    most = PermissionUtils.get_most_privilege(modes)
    
    print(f"\n最小权限 (交集): {least:04o} ({to_symbolic(least)})")
    print(f"最大权限 (并集): {most:04o} ({to_symbolic(most)})")


def example_generate_chmod_commands():
    """示例: 生成 chmod 命令"""
    print("\n" + "=" * 60)
    print("示例 10: 生成 chmod 命令")
    print("=" * 60)
    
    permissions = [0o755, 0o644, 0o600, 0o700, 0o4755]
    
    print("\nchmod 命令生成:")
    for perm in permissions:
        cmd = PermissionUtils.to_chmod_command(perm)
        info = parse(perm)
        print(f"  {cmd:<30} # {info.symbolic}")


def main():
    """运行所有示例"""
    example_basic_parsing()
    example_chmod_style_parsing()
    example_special_permissions()
    example_permission_comparison()
    example_umask_calculation()
    example_recommended_permissions()
    example_permission_explanation()
    example_permission_security()
    example_permission_aggregation()
    example_generate_chmod_commands()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()