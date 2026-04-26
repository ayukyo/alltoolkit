"""
命令行参数解析工具
================

零外部依赖的命令行参数解析器，支持：
- 短选项 (-v) 和长选项 (--verbose)
- 选项参数 (--file=foo.txt 或 --file foo.txt)
- 位置参数
- 子命令
- 自动生成帮助信息
- 参数验证和类型转换
- 默认值支持

作者: AllToolkit 自动生成
日期: 2026-04-26
"""

import sys
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum


class ArgType(Enum):
    """参数类型"""
    FLAG = "flag"           # 布尔标志，无参数
    OPTION = "option"       # 带参数的选项
    POSITIONAL = "positional"  # 位置参数


@dataclass
class Argument:
    """参数定义"""
    name: str                                    # 参数名
    short: Optional[str] = None                  # 短选项 (如 'v' 代表 -v)
    long: Optional[str] = None                   # 长选项 (如 'verbose' 代表 --verbose)
    help_text: str = ""                          # 帮助文本
    arg_type: ArgType = ArgType.FLAG              # 参数类型
    required: bool = False                       # 是否必需
    default: Any = None                           # 默认值
    type_converter: Optional[Callable] = None    # 类型转换函数
    choices: Optional[List[Any]] = None           # 可选值列表
    multiple: bool = False                        # 是否允许多个值
    dest: Optional[str] = None                    # 结果中的键名
    
    def get_dest(self) -> str:
        """获取结果中的键名"""
        if self.dest:
            return self.dest
        if self.long:
            return self.long.replace("-", "_")
        if self.short:
            return self.short
        return self.name.replace("-", "_")


@dataclass
class Command:
    """子命令定义"""
    name: str                                    # 命令名
    help_text: str = ""                          # 帮助文本
    arguments: List[Argument] = field(default_factory=list)  # 参数列表
    subcommands: Dict[str, 'Command'] = field(default_factory=dict)  # 子命令
    handler: Optional[Callable] = None           # 处理函数


@dataclass
class ParseResult:
    """解析结果"""
    args: Dict[str, Any]                         # 解析后的参数
    positional: List[str]                        # 位置参数
    command: Optional[str] = None                # 子命令名
    subcommand_path: List[str] = field(default_factory=list)  # 子命令路径
    command_args: Optional['ParseResult'] = None # 子命令参数
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取参数值"""
        return self.args.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        return self.args[key]
    
    def __contains__(self, key: str) -> bool:
        return key in self.args


class CommandLineParser:
    """命令行参数解析器"""
    
    def __init__(self, 
                 prog: Optional[str] = None,
                 description: str = "",
                 version: Optional[str] = None):
        """
        初始化解析器
        
        Args:
            prog: 程序名，默认从sys.argv获取
            description: 程序描述
            version: 版本号
        """
        self.prog = prog or sys.argv[0]
        self.description = description
        self.version = version
        self.arguments: List[Argument] = []
        self.commands: Dict[str, Command] = {}
        self._short_options: Dict[str, Argument] = {}
        self._long_options: Dict[str, Argument] = {}
        self._positional: List[Argument] = []
        
    def add_argument(self, 
                     name: Optional[str] = None,
                     short: Optional[str] = None,
                     long: Optional[str] = None,
                     help_text: str = "",
                     arg_type: Optional[ArgType] = None,
                     required: bool = False,
                     default: Any = None,
                     type_converter: Optional[Callable] = None,
                     choices: Optional[List[Any]] = None,
                     multiple: bool = False,
                     dest: Optional[str] = None) -> 'CommandLineParser':
        """
        添加参数
        
        Args:
            name: 参数名（位置参数用）
            short: 短选项（如 'v'）
            long: 长选项（如 'verbose'）
            help_text: 帮助文本
            arg_type: 参数类型
            required: 是否必需
            default: 默认值
            type_converter: 类型转换函数
            choices: 可选值列表
            multiple: 是否允许多值
            dest: 结果键名
            
        Returns:
            self，支持链式调用
        """
        # 自动推断参数类型
        if arg_type is None:
            if name and not short and not long:
                arg_type = ArgType.POSITIONAL
            elif default is not None and not isinstance(default, bool):
                arg_type = ArgType.OPTION
            elif type_converter is not None:
                arg_type = ArgType.OPTION
            elif choices is not None:
                arg_type = ArgType.OPTION
            elif multiple and (short or long):
                arg_type = ArgType.OPTION
            else:
                arg_type = ArgType.FLAG
            
        # 自动生成长选项名
        if name and not long and not short:
            long = name.replace("_", "-")
            
        arg = Argument(
            name=name or long or short or "",
            short=short,
            long=long,
            help_text=help_text,
            arg_type=arg_type,
            required=required,
            default=default,
            type_converter=type_converter,
            choices=choices,
            multiple=multiple,
            dest=dest
        )
        
        self.arguments.append(arg)
        
        # 建立索引
        if arg.short:
            self._short_options[arg.short] = arg
        if arg.long:
            self._long_options[arg.long] = arg
        if arg.arg_type == ArgType.POSITIONAL:
            self._positional.append(arg)
            
        return self
    
    def add_command(self,
                    name: str,
                    help_text: str = "",
                    handler: Optional[Callable] = None) -> 'Command':
        """
        添加子命令
        
        Args:
            name: 命令名
            help_text: 帮助文本
            handler: 处理函数
            
        Returns:
            Command对象，可继续添加参数
        """
        cmd = Command(name=name, help_text=help_text, handler=handler)
        self.commands[name] = cmd
        return cmd
    
    def _parse_value(self, value: str, arg: Argument) -> Any:
        """解析并转换参数值"""
        # 类型转换
        if arg.type_converter:
            try:
                value = arg.type_converter(value)
            except (ValueError, TypeError) as e:
                raise ValueError(f"参数 '{arg.name}' 的值 '{value}' 无法转换为指定类型: {e}")
        
        # 选项值验证
        if arg.choices and value not in arg.choices:
            raise ValueError(f"参数 '{arg.name}' 的值 '{value}' 不在允许的选项中: {arg.choices}")
            
        return value
    
    def _split_option(self, opt: str) -> Tuple[str, Optional[str]]:
        """
        分离选项和值
        例如: --file=foo.txt -> ('file', 'foo.txt')
              -f=bar.txt -> ('f', 'bar.txt')
              --verbose -> ('verbose', None)
        """
        if opt.startswith("--"):
            opt_body = opt[2:]
        elif opt.startswith("-"):
            opt_body = opt[1:]
        else:
            return opt, None
            
        if "=" in opt_body:
            name, value = opt_body.split("=", 1)
            return name, value
        return opt_body, None
    
    def _is_option(self, arg: str) -> bool:
        """检查是否是选项"""
        return arg.startswith("-") and arg != "-" and arg != "--"
    
    def parse(self, args: Optional[List[str]] = None) -> ParseResult:
        """
        解析命令行参数
        
        Args:
            args: 参数列表，默认使用sys.argv[1:]
            
        Returns:
            ParseResult对象
        """
        if args is None:
            args = sys.argv[1:]
            
        result: Dict[str, Any] = {}
        positional: List[str] = []
        
        # 初始化默认值
        for arg in self.arguments:
            if arg.default is not None:
                result[arg.get_dest()] = arg.default if not arg.multiple else [arg.default]
            elif arg.multiple:
                result[arg.get_dest()] = []
                
        i = 0
        while i < len(args):
            arg = args[i]
            
            # 处理 -- 分隔符
            if arg == "--":
                positional.extend(args[i+1:])
                break
                
            # 检查是否是子命令
            if arg in self.commands and not positional:
                cmd_result = self._parse_command(self.commands[arg], args[i+1:])
                cmd_result.subcommand_path = [arg]
                return ParseResult(
                    args=result,
                    positional=positional,
                    command=arg,
                    subcommand_path=[arg],
                    command_args=cmd_result
                )
                
            # 处理选项
            if self._is_option(arg):
                name, inline_value = self._split_option(arg)
                
                # 查找参数定义
                arg_def = None
                if arg.startswith("--"):
                    arg_def = self._long_options.get(name)
                elif arg.startswith("-") and len(name) == 1:
                    arg_def = self._short_options.get(name)
                elif arg.startswith("-"):
                    # 处理组合短选项 -abc -> -a -b -c，或带参数的选项 -DDEBUG
                    # 首先检查第一个字符是否是已知选项
                    first_char = name[0]
                    first_char_def = self._short_options.get(first_char)
                    
                    if first_char_def and first_char_def.arg_type != ArgType.FLAG:
                        # 第一个字符是需要参数的选项，剩余部分是参数值
                        if len(name) > 1:
                            inline_value = name[1:]  # 剩余部分作为参数
                            arg_def = first_char_def
                            name = first_char
                        else:
                            # 只有选项名，参数需要从下一个位置获取
                            arg_def = first_char_def
                            name = first_char
                            inline_value = None
                    else:
                        # 处理组合短选项 -abc -> -a -b -c
                        for j, char in enumerate(name):
                            char_def = self._short_options.get(char)
                            if char_def:
                                if char_def.arg_type == ArgType.FLAG:
                                    dest = char_def.get_dest()
                                    if char_def.multiple:
                                        result[dest].append(True)
                                    else:
                                        result[dest] = True
                                else:
                                    # 需要参数的选项，如果后面还有字符，作为参数
                                    if j == len(name) - 1:
                                        arg_def = char_def
                                        name = char
                                        break
                                    else:
                                        # 后面的字符作为参数值
                                        inline_value = name[j+1:]
                                        arg_def = char_def
                                        name = char
                                        break
                            else:
                                # 未知的字符，跳过
                                pass
                        if arg_def is None:
                            i += 1
                            continue
                        
                if arg_def is None:
                    raise ValueError(f"未知选项: {arg}")
                    
                dest = arg_def.get_dest()
                
                if arg_def.arg_type == ArgType.FLAG:
                    # 布尔标志
                    if arg_def.multiple:
                        result[dest].append(True)
                    else:
                        result[dest] = True
                    i += 1
                else:
                    # 需要参数的选项
                    if inline_value is not None:
                        value = self._parse_value(inline_value, arg_def)
                    elif i + 1 < len(args) and not self._is_option(args[i + 1]):
                        value = self._parse_value(args[i + 1], arg_def)
                        i += 1
                    else:
                        raise ValueError(f"选项 {arg} 需要参数")
                        
                    if arg_def.multiple:
                        result[dest].append(value)
                    else:
                        result[dest] = value
                    i += 1
            else:
                # 位置参数
                positional.append(arg)
                i += 1
                
        # 处理位置参数映射
        consumed_indices = set()
        for idx, arg_def in enumerate(self._positional):
            if idx < len(positional):
                dest = arg_def.get_dest()
                if arg_def.multiple:
                    # 多值位置参数：收集从当前位置开始的所有剩余位置参数
                    values = []
                    for j in range(idx, len(positional)):
                        if j not in consumed_indices:
                            values.append(self._parse_value(positional[j], arg_def))
                            consumed_indices.add(j)
                    result[dest] = values
                else:
                    value = self._parse_value(positional[idx], arg_def)
                    result[dest] = value
                    consumed_indices.add(idx)
                
        # 清理已映射的位置参数
        positional = [p for i, p in enumerate(positional) if i not in consumed_indices]
        
        # 检查必需参数
        for arg in self.arguments:
            if arg.required and arg.get_dest() not in result:
                if arg.short:
                    raise ValueError(f"缺少必需参数: -{arg.short}")
                elif arg.long:
                    raise ValueError(f"缺少必需参数: --{arg.long}")
                else:
                    raise ValueError(f"缺少必需参数: {arg.name}")
                    
        return ParseResult(args=result, positional=positional)
    
    def _parse_command(self, cmd: Command, args: List[str]) -> ParseResult:
        """解析子命令参数"""
        result: Dict[str, Any] = {}
        positional: List[str] = []
        
        # 建立命令的参数索引
        short_opts: Dict[str, Argument] = {}
        long_opts: Dict[str, Argument] = {}
        positional_args: List[Argument] = []
        
        for arg in cmd.arguments:
            if arg.short:
                short_opts[arg.short] = arg
            if arg.long:
                long_opts[arg.long] = arg
            if arg.arg_type == ArgType.POSITIONAL:
                positional_args.append(arg)
            if arg.default is not None:
                result[arg.get_dest()] = arg.default if not arg.multiple else [arg.default]
            elif arg.multiple:
                result[arg.get_dest()] = []
                
        i = 0
        while i < len(args):
            arg = args[i]
            
            # 检查子命令的子命令
            if arg in cmd.subcommands:
                sub_cmd_result = self._parse_command(cmd.subcommands[arg], args[i+1:])
                sub_cmd_result.subcommand_path = [arg]
                return ParseResult(
                    args=result,
                    positional=positional,
                    command=arg,
                    subcommand_path=[arg],
                    command_args=sub_cmd_result
                )
            
            if arg == "--":
                positional.extend(args[i+1:])
                break
                
            if self._is_option(arg):
                name, inline_value = self._split_option(arg)
                
                arg_def = None
                if arg.startswith("--"):
                    arg_def = long_opts.get(name)
                elif arg.startswith("-") and len(name) == 1:
                    arg_def = short_opts.get(name)
                    
                if arg_def is None:
                    raise ValueError(f"命令 '{cmd.name}' 的未知选项: {arg}")
                    
                dest = arg_def.get_dest()
                
                if arg_def.arg_type == ArgType.FLAG:
                    if arg_def.multiple:
                        result[dest].append(True)
                    else:
                        result[dest] = True
                    i += 1
                else:
                    if inline_value is not None:
                        value = self._parse_value(inline_value, arg_def)
                    elif i + 1 < len(args) and not self._is_option(args[i + 1]):
                        value = self._parse_value(args[i + 1], arg_def)
                        i += 1
                    else:
                        raise ValueError(f"选项 {arg} 需要参数")
                        
                    if arg_def.multiple:
                        result[dest].append(value)
                    else:
                        result[dest] = value
                    i += 1
            else:
                positional.append(arg)
                i += 1
                
        # 处理位置参数映射
        for idx, arg_def in enumerate(positional_args):
            if idx < len(positional):
                value = self._parse_value(positional[idx], arg_def)
                dest = arg_def.get_dest()
                if arg_def.multiple:
                    if dest not in result:
                        result[dest] = []
                    result[dest].append(value)
                else:
                    result[dest] = value
                positional[idx] = None
                
        positional = [p for p in positional if p is not None]
        
        # 检查必需参数
        for arg in cmd.arguments:
            if arg.required and arg.get_dest() not in result:
                if arg.short:
                    raise ValueError(f"缺少必需参数: -{arg.short}")
                elif arg.long:
                    raise ValueError(f"缺少必需参数: --{arg.long}")
                else:
                    raise ValueError(f"缺少必需参数: {arg.name}")
                    
        return ParseResult(args=result, positional=positional)
    
    def format_help(self, command_path: Optional[List[str]] = None) -> str:
        """
        生成帮助信息
        
        Args:
            command_path: 子命令路径
            
        Returns:
            格式化的帮助文本
        """
        lines = []
        
        # 标题
        prog_name = self.prog
        if command_path:
            prog_name = f"{self.prog} {' '.join(command_path)}"
            
        lines.append(f"用法: {prog_name} [选项]")
        
        if self.description:
            lines.append("")
            lines.append(self.description)
            
        # 选项
        if self.arguments:
            lines.append("")
            lines.append("选项:")
            max_len = 0
            opts = []
            for arg in self.arguments:
                if arg.arg_type == ArgType.POSITIONAL:
                    continue
                parts = []
                if arg.short:
                    parts.append(f"-{arg.short}")
                if arg.long:
                    if parts:
                        parts.append(f", --{arg.long}")
                    else:
                        parts.append(f"--{arg.long}")
                if arg.arg_type == ArgType.OPTION:
                    parts.append(f" <{arg.name or arg.long or arg.short}>")
                opt_str = "".join(parts)
                opts.append((opt_str, arg.help_text, arg.default, arg.choices, arg.required))
                max_len = max(max_len, len(opt_str))
                
            for opt_str, help_text, default, choices, required in opts:
                req_marker = " (必需)" if required else ""
                line = f"  {opt_str.ljust(max_len + 4)}"
                if help_text:
                    line += help_text
                if default is not None:
                    line += f" [默认: {default}]"
                if choices:
                    line += f" [选项: {', '.join(map(str, choices))}]"
                line += req_marker
                lines.append(line)
                
        # 位置参数
        pos_args = [arg for arg in self.arguments if arg.arg_type == ArgType.POSITIONAL]
        if pos_args:
            lines.append("")
            lines.append("位置参数:")
            for arg in pos_args:
                req_marker = " (必需)" if arg.required else ""
                line = f"  {arg.name}"
                if arg.help_text:
                    line += f"  {arg.help_text}"
                line += req_marker
                lines.append(line)
                
        # 子命令
        if self.commands:
            lines.append("")
            lines.append("子命令:")
            max_cmd_len = max(len(cmd) for cmd in self.commands)
            for name, cmd in self.commands.items():
                line = f"  {name.ljust(max_cmd_len + 4)}"
                if cmd.help_text:
                    line += cmd.help_text
                lines.append(line)
                
        if self.version:
            lines.append("")
            lines.append(f"版本: {self.version}")
            
        return "\n".join(lines)
    
    def format_usage(self) -> str:
        """生成用法摘要"""
        parts = [f"用法: {self.prog}"]
        
        has_optional = any(arg.arg_type != ArgType.POSITIONAL and not arg.required for arg in self.arguments)
        has_required = any(arg.arg_type != ArgType.POSITIONAL and arg.required for arg in self.arguments)
        has_positional = any(arg.arg_type == ArgType.POSITIONAL for arg in self.arguments)
        
        if has_optional or has_required:
            parts.append("[选项]")
            
        for arg in self._positional:
            if arg.required:
                parts.append(f"<{arg.name}>")
            else:
                parts.append(f"[{arg.name}]")
                
        if self.commands:
            parts.append("<命令>")
            
        return " ".join(parts)


def create_parser(prog: Optional[str] = None,
                  description: str = "",
                  version: Optional[str] = None) -> CommandLineParser:
    """
    创建命令行解析器的便捷函数
    
    Args:
        prog: 程序名
        description: 描述
        version: 版本
        
    Returns:
        CommandLineParser实例
    """
    return CommandLineParser(prog=prog, description=description, version=version)


# 常用类型转换器
def int_converter(value: str) -> int:
    """整数转换器"""
    return int(value)


def float_converter(value: str) -> float:
    """浮点数转换器"""
    return float(value)


def bool_converter(value: str) -> bool:
    """布尔值转换器"""
    if value.lower() in ('true', '1', 'yes', 'on'):
        return True
    if value.lower() in ('false', '0', 'no', 'off'):
        return False
    raise ValueError(f"无法将 '{value}' 转换为布尔值")


def list_converter(separator: str = ",") -> Callable[[str], List[str]]:
    """
    列表转换器工厂
    
    Args:
        separator: 分隔符
        
    Returns:
        转换函数
    """
    def converter(value: str) -> List[str]:
        return [v.strip() for v in value.split(separator)]
    return converter


def range_converter(value: str) -> Tuple[int, int]:
    """
    范围转换器
    支持格式: "1-10", "5:20", "start,end"
    """
    for sep in ['-', ':', ',']:
        if sep in value:
            parts = value.split(sep, 1)
            return (int(parts[0].strip()), int(parts[1].strip()))
    raise ValueError(f"无效的范围格式: {value}")


# 导出
__all__ = [
    'CommandLineParser',
    'Argument',
    'Command',
    'ParseResult',
    'ArgType',
    'create_parser',
    'int_converter',
    'float_converter',
    'bool_converter',
    'list_converter',
    'range_converter',
]