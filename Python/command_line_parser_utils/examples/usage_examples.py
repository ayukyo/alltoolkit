"""
命令行参数解析工具 - 使用示例
============================

演示如何使用 command_line_parser_utils 创建功能完整的命令行工具。
"""

import sys
import os
from typing import List, Optional

# 添加父目录到导入路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入模块
from mod import (
    CommandLineParser,
    Argument,
    ArgType,
    create_parser,
    int_converter,
    float_converter,
    bool_converter,
    list_converter,
    range_converter,
)


def example_basic_flags():
    """示例1: 基本布尔标志选项"""
    print("=" * 60)
    print("示例1: 基本布尔标志选项")
    print("=" * 60)
    
    parser = create_parser(
        prog="myapp",
        description="一个简单的应用程序"
    )
    
    # 添加布尔标志
    parser.add_argument(short="v", long="verbose", help_text="显示详细输出")
    parser.add_argument(short="q", long="quiet", help_text="静默模式")
    parser.add_argument(short="d", long="debug", help_text="调试模式")
    
    # 模拟命令行参数
    args = ["-v", "--debug"]
    result = parser.parse(args)
    
    print(f"解析参数: {args}")
    print(f"verbose: {result['verbose']}")
    print(f"quiet: {result.get('quiet', False)}")
    print(f"debug: {result['debug']}")
    print()


def example_options_with_values():
    """示例2: 带值的选项"""
    print("=" * 60)
    print("示例2: 带值的选项")
    print("=" * 60)
    
    parser = create_parser(prog="filetool", description="文件处理工具")
    
    parser.add_argument(
        short="i",
        long="input",
        arg_type=ArgType.OPTION,
        required=True,
        help_text="输入文件路径"
    )
    parser.add_argument(
        short="o",
        long="output",
        arg_type=ArgType.OPTION,
        help_text="输出文件路径"
    )
    parser.add_argument(
        long="format",
        arg_type=ArgType.OPTION,
        choices=["json", "xml", "yaml", "csv"],
        default="json",
        help_text="输出格式"
    )
    parser.add_argument(
        short="j",
        long="jobs",
        arg_type=ArgType.OPTION,
        type_converter=int_converter,
        default=4,
        help_text="并行任务数"
    )
    
    args = ["-i", "data.txt", "--output=result.json", "--format=yaml", "-j", "8"]
    result = parser.parse(args)
    
    print(f"解析参数: {args}")
    print(f"输入文件: {result['input']}")
    print(f"输出文件: {result['output']}")
    print(f"格式: {result['format']}")
    print(f"并行数: {result['jobs']}")
    print()


def example_positional_args():
    """示例3: 位置参数"""
    print("=" * 60)
    print("示例3: 位置参数")
    print("=" * 60)
    
    parser = create_parser(prog="cp", description="复制文件")
    
    parser.add_argument(
        name="source",
        arg_type=ArgType.POSITIONAL,
        required=True,
        help_text="源文件"
    )
    parser.add_argument(
        name="destination",
        arg_type=ArgType.POSITIONAL,
        required=True,
        help_text="目标位置"
    )
    parser.add_argument(
        short="r",
        long="recursive",
        help_text="递归复制目录"
    )
    parser.add_argument(
        short="f",
        long="force",
        help_text="强制覆盖"
    )
    
    args = ["file1.txt", "file2.txt", "-rf"]
    result = parser.parse(args)
    
    print(f"解析参数: {args}")
    print(f"源文件: {result['source']}")
    print(f"目标: {result['destination']}")
    print(f"递归: {result['recursive']}")
    print(f"强制: {result['force']}")
    print()


def example_multiple_values():
    """示例4: 多值参数"""
    print("=" * 60)
    print("示例4: 多值参数")
    print("=" * 60)
    
    parser = create_parser(prog="compile", description="编译器")
    
    parser.add_argument(
        short="I",
        long="include",
        arg_type=ArgType.OPTION,
        multiple=True,
        help_text="包含目录 (可多次指定)"
    )
    parser.add_argument(
        short="D",
        long="define",
        arg_type=ArgType.OPTION,
        multiple=True,
        help_text="宏定义 (可多次指定)"
    )
    parser.add_argument(
        long="libs",
        arg_type=ArgType.OPTION,
        type_converter=list_converter(","),
        help_text="链接库 (逗号分隔)"
    )
    
    args = [
        "-I", "/usr/include",
        "-I", "/usr/local/include",
        "-DDEBUG",
        "-DVERSION=2",
        "--libs=zlib,openssl,curl"
    ]
    result = parser.parse(args)
    
    print(f"解析参数: {args}")
    print(f"包含目录: {result['include']}")
    print(f"宏定义: {result['define']}")
    print(f"链接库: {result['libs']}")
    print()


def example_subcommands():
    """示例5: 子命令"""
    print("=" * 60)
    print("示例5: 子命令 (类似 git)")
    print("=" * 60)
    
    parser = create_parser(prog="git", description="分布式版本控制系统")
    
    # 全局选项
    parser.add_argument(short="v", long="verbose", help_text="详细输出")
    
    # 添加 commit 子命令
    commit_cmd = parser.add_command("commit", help_text="提交更改")
    commit_cmd.arguments.append(Argument(
        name="message",
        short="m",
        long="message",
        arg_type=ArgType.OPTION,
        required=True,
        help_text="提交信息"
    ))
    commit_cmd.arguments.append(Argument(
        name="all",
        short="a",
        long="all",
        arg_type=ArgType.FLAG,
        help_text="提交所有更改"
    ))
    
    # 添加 push 子命令
    push_cmd = parser.add_command("push", help_text="推送到远程")
    push_cmd.arguments.append(Argument(
        name="remote",
        arg_type=ArgType.POSITIONAL,
        help_text="远程名称"
    ))
    push_cmd.arguments.append(Argument(
        name="branch",
        arg_type=ArgType.POSITIONAL,
        help_text="分支名称"
    ))
    push_cmd.arguments.append(Argument(
        name="force",
        short="f",
        long="force",
        arg_type=ArgType.FLAG,
        help_text="强制推送"
    ))
    
    # 测试 commit 命令
    args = ["commit", "-m", "Initial commit", "-a"]
    result = parser.parse(args)
    
    print(f"解析参数: {args}")
    print(f"命令: {result.command}")
    print(f"子命令路径: {result.subcommand_path}")
    print(f"提交信息: {result.command_args['message']}")
    print(f"提交全部: {result.command_args['all']}")
    print()
    
    # 测试 push 命令
    args = ["push", "origin", "main", "--force"]
    result = parser.parse(args)
    
    print(f"解析参数: {args}")
    print(f"命令: {result.command}")
    print(f"远程: {result.command_args['remote']}")
    print(f"分支: {result.command_args['branch']}")
    print(f"强制: {result.command_args['force']}")
    print()


def example_type_conversion():
    """示例6: 类型转换"""
    print("=" * 60)
    print("示例6: 类型转换")
    print("=" * 60)
    
    parser = create_parser(prog="server", description="服务器配置")
    
    parser.add_argument(
        short="p",
        long="port",
        arg_type=ArgType.OPTION,
        type_converter=int_converter,
        default=8080,
        help_text="端口号"
    )
    parser.add_argument(
        long="ratio",
        arg_type=ArgType.OPTION,
        type_converter=float_converter,
        help_text="压缩比率 (0.0-1.0)"
    )
    parser.add_argument(
        long="debug",
        arg_type=ArgType.OPTION,
        type_converter=bool_converter,
        help_text="启用调试 (true/false)"
    )
    parser.add_argument(
        long="threads",
        arg_type=ArgType.OPTION,
        type_converter=range_converter,
        help_text="线程范围 (如 1-10)"
    )
    
    args = ["--port=3000", "--ratio=0.85", "--debug=true", "--threads=4-16"]
    result = parser.parse(args)
    
    print(f"解析参数: {args}")
    print(f"端口 (int): {result['port']} (类型: {type(result['port']).__name__})")
    print(f"比率 (float): {result['ratio']} (类型: {type(result['ratio']).__name__})")
    print(f"调试 (bool): {result['debug']} (类型: {type(result['debug']).__name__})")
    print(f"线程范围 (tuple): {result['threads']} (类型: {type(result['threads']).__name__})")
    print()


def example_help_generation():
    """示例7: 帮助信息生成"""
    print("=" * 60)
    print("示例7: 帮助信息生成")
    print("=" * 60)
    
    parser = create_parser(
        prog="mytool",
        description="一个功能强大的命令行工具",
        version="2.0.0"
    )
    
    parser.add_argument(
        short="v",
        long="verbose",
        help_text="显示详细输出"
    )
    parser.add_argument(
        short="f",
        long="file",
        arg_type=ArgType.OPTION,
        required=True,
        help_text="输入文件路径"
    )
    parser.add_argument(
        long="format",
        arg_type=ArgType.OPTION,
        choices=["json", "yaml", "toml"],
        default="json",
        help_text="输出格式"
    )
    parser.add_argument(
        short="j",
        long="jobs",
        arg_type=ArgType.OPTION,
        type_converter=int_converter,
        default=4,
        help_text="并行任务数"
    )
    parser.add_argument(
        name="output",
        arg_type=ArgType.POSITIONAL,
        help_text="输出文件"
    )
    
    # 添加子命令
    init_cmd = parser.add_command("init", help_text="初始化项目")
    build_cmd = parser.add_command("build", help_text="构建项目")
    
    print("\n" + parser.format_help())
    print("\n用法摘要:")
    print(parser.format_usage())
    print()


def example_real_world_cli():
    """示例8: 真实世界CLI应用"""
    print("=" * 60)
    print("示例8: 真实世界CLI应用 - 构建工具")
    print("=" * 60)
    
    def run_build(result):
        """模拟构建命令"""
        print(f"\n构建配置:")
        print(f"  目标: {result['target']}")
        print(f"  并行任务: {result['jobs']}")
        print(f"  清理: {result.get('clean', False)}")
        print(f"  详细: {result.get('verbose', False)}")
        return 0
    
    def run_test(result):
        """模拟测试命令"""
        print(f"\n测试配置:")
        print(f"  覆盖率: {result.get('coverage', False)}")
        print(f"  并行: {result.get('parallel', False)}")
        print(f"  过滤器: {result.get('filter', 'all')}")
        return 0
    
    parser = create_parser(
        prog="buildtool",
        description="现代化构建工具",
        version="1.0.0"
    )
    
    # 全局选项
    parser.add_argument(short="v", long="verbose", help_text="详细输出")
    parser.add_argument(short="q", long="quiet", help_text="静默模式")
    
    # build 命令
    build_cmd = parser.add_command("build", help_text="构建项目")
    build_cmd.arguments.append(Argument(
        name="target",
        arg_type=ArgType.POSITIONAL,
        help_text="构建目标"
    ))
    build_cmd.arguments.append(Argument(
        name="jobs",
        short="j",
        long="jobs",
        arg_type=ArgType.OPTION,
        type_converter=int_converter,
        default=4,
        help_text="并行任务数"
    ))
    build_cmd.arguments.append(Argument(
        name="clean",
        long="clean",
        arg_type=ArgType.FLAG,
        help_text="清理后构建"
    ))
    build_cmd.arguments.append(Argument(
        name="config",
        long="config",
        arg_type=ArgType.OPTION,
        choices=["debug", "release", "test"],
        default="debug",
        help_text="构建配置"
    ))
    
    # test 命令
    test_cmd = parser.add_command("test", help_text="运行测试")
    test_cmd.arguments.append(Argument(
        name="coverage",
        long="coverage",
        arg_type=ArgType.FLAG,
        help_text="生成覆盖率报告"
    ))
    test_cmd.arguments.append(Argument(
        name="parallel",
        long="parallel",
        arg_type=ArgType.FLAG,
        help_text="并行运行测试"
    ))
    test_cmd.arguments.append(Argument(
        name="filter",
        long="filter",
        arg_type=ArgType.OPTION,
        default="all",
        help_text="测试过滤器"
    ))
    
    # 模拟构建命令（全局选项 -v 放在子命令之前）
    args = ["-v", "build", "myapp", "--config=release", "-j", "8", "--clean"]
    result = parser.parse(args)
    
    print(f"命令行: {' '.join(args)}")
    print(f"\n解析结果:")
    print(f"  主命令: {result.command}")
    print(f"  全局详细模式: {result['verbose']}")
    
    if result.command_args:
        print(f"\n命令参数:")
        for key, value in result.command_args.args.items():
            print(f"  {key}: {value}")
    print()


def example_combined_short_flags():
    """示例9: 组合短选项"""
    print("=" * 60)
    print("示例9: 组合短选项 (类似 ls -la)")
    print("=" * 60)
    
    parser = create_parser(prog="ls", description="列出目录内容")
    
    parser.add_argument(short="a", long="all", help_text="显示隐藏文件")
    parser.add_argument(short="l", long="long", help_text="长格式")
    parser.add_argument(short="h", long="human-readable", help_text="人类可读大小")
    parser.add_argument(short="t", long="time", help_text="按时间排序")
    parser.add_argument(short="r", long="reverse", help_text="反向排序")
    parser.add_argument(short="R", long="recursive", help_text="递归列出")
    parser.add_argument(name="path", arg_type=ArgType.POSITIONAL, default=".")
    
    # 组合选项
    args = ["-laRh", "/home/user"]
    result = parser.parse(args)
    
    print(f"解析参数: {args}")
    print(f"显示全部: {result['all']}")
    print(f"长格式: {result['long']}")
    print(f"人类可读: {result['human_readable']}")
    print(f"递归: {result['recursive']}")
    print(f"路径: {result['path']}")
    print()


def main():
    """运行所有示例"""
    example_basic_flags()
    example_options_with_values()
    example_positional_args()
    example_multiple_values()
    example_subcommands()
    example_type_conversion()
    example_help_generation()
    example_real_world_cli()
    example_combined_short_flags()
    
    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()