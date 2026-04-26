"""
命令行参数解析工具测试
====================

测试所有功能：选项解析、位置参数、子命令、帮助生成等。
"""

import unittest
import sys
from io import StringIO
from typing import List

# 导入模块
from mod import (
    CommandLineParser,
    Argument,
    Command,
    ParseResult,
    ArgType,
    create_parser,
    int_converter,
    float_converter,
    bool_converter,
    list_converter,
    range_converter,
)


class TestBasicParsing(unittest.TestCase):
    """基础解析测试"""
    
    def test_flag_option(self):
        """测试布尔标志选项"""
        parser = create_parser(prog="test")
        parser.add_argument(short="v", long="verbose", help_text="详细输出")
        
        # 测试短选项
        result = parser.parse(["-v"])
        self.assertTrue(result["verbose"])
        
        # 测试长选项
        result = parser.parse(["--verbose"])
        self.assertTrue(result["verbose"])
        
        # 测试未提供时
        result = parser.parse([])
        self.assertIsNone(result.get("verbose"))
        
    def test_option_with_value(self):
        """测试带参数的选项"""
        parser = create_parser(prog="test")
        parser.add_argument(
            short="f", 
            long="file", 
            arg_type=ArgType.OPTION,
            help_text="输入文件"
        )
        
        # 短选项 + 值
        result = parser.parse(["-f", "test.txt"])
        self.assertEqual(result["file"], "test.txt")
        
        # 长选项 + 值
        result = parser.parse(["--file", "data.txt"])
        self.assertEqual(result["file"], "data.txt")
        
        # 长选项 + 等号
        result = parser.parse(["--file=output.txt"])
        self.assertEqual(result["file"], "output.txt")
        
    def test_combined_short_flags(self):
        """测试组合短选项 -abc"""
        parser = create_parser(prog="test")
        parser.add_argument(short="a", long="all", help_text="显示所有")
        parser.add_argument(short="l", long="long", help_text="长格式")
        parser.add_argument(short="h", long="human", help_text="人类可读")
        
        result = parser.parse(["-alh"])
        self.assertTrue(result["all"])
        self.assertTrue(result["long"])
        self.assertTrue(result["human"])
        
    def test_positional_args(self):
        """测试位置参数"""
        parser = create_parser(prog="test")
        parser.add_argument(name="input", arg_type=ArgType.POSITIONAL, help_text="输入文件")
        parser.add_argument(name="output", arg_type=ArgType.POSITIONAL, help_text="输出文件")
        
        result = parser.parse(["file1.txt", "file2.txt"])
        self.assertEqual(result["input"], "file1.txt")
        self.assertEqual(result["output"], "file2.txt")
        self.assertEqual(result.positional, [])
        
    def test_positional_with_options(self):
        """测试位置参数和选项混合"""
        parser = create_parser(prog="test")
        parser.add_argument(short="v", long="verbose")
        parser.add_argument(name="file", arg_type=ArgType.POSITIONAL)
        
        result = parser.parse(["-v", "test.txt"])
        self.assertTrue(result["verbose"])
        self.assertEqual(result["file"], "test.txt")
        
        result = parser.parse(["test.txt", "-v"])
        self.assertTrue(result["verbose"])
        self.assertEqual(result["file"], "test.txt")


class TestTypeConversion(unittest.TestCase):
    """类型转换测试"""
    
    def test_int_conversion(self):
        """测试整数转换"""
        parser = create_parser(prog="test")
        parser.add_argument(
            short="n", 
            long="count",
            arg_type=ArgType.OPTION,
            type_converter=int_converter
        )
        
        result = parser.parse(["-n", "42"])
        self.assertEqual(result["count"], 42)
        self.assertIsInstance(result["count"], int)
        
        result = parser.parse(["--count=100"])
        self.assertEqual(result["count"], 100)
        
    def test_float_conversion(self):
        """测试浮点数转换"""
        parser = create_parser(prog="test")
        parser.add_argument(
            short="r",
            long="rate",
            arg_type=ArgType.OPTION,
            type_converter=float_converter
        )
        
        result = parser.parse(["-r", "3.14"])
        self.assertAlmostEqual(result["rate"], 3.14, places=2)
        
    def test_bool_conversion(self):
        """测试布尔转换"""
        parser = create_parser(prog="test")
        parser.add_argument(
            long="enabled",
            arg_type=ArgType.OPTION,
            type_converter=bool_converter
        )
        
        result = parser.parse(["--enabled=true"])
        self.assertTrue(result["enabled"])
        
        result = parser.parse(["--enabled", "no"])
        self.assertFalse(result["enabled"])
        
    def test_list_conversion(self):
        """测试列表转换"""
        parser = create_parser(prog="test")
        parser.add_argument(
            long="tags",
            arg_type=ArgType.OPTION,
            type_converter=list_converter(",")
        )
        
        result = parser.parse(["--tags=a,b,c"])
        self.assertEqual(result["tags"], ["a", "b", "c"])
        
    def test_range_conversion(self):
        """测试范围转换"""
        parser = create_parser(prog="test")
        parser.add_argument(
            long="range",
            arg_type=ArgType.OPTION,
            type_converter=range_converter
        )
        
        result = parser.parse(["--range=1-10"])
        self.assertEqual(result["range"], (1, 10))
        
        result = parser.parse(["--range=5:15"])
        self.assertEqual(result["range"], (5, 15))


class TestValidation(unittest.TestCase):
    """验证测试"""
    
    def test_required_arg(self):
        """测试必需参数"""
        parser = create_parser(prog="test")
        parser.add_argument(
            short="f",
            long="file",
            arg_type=ArgType.OPTION,
            required=True
        )
        
        # 不提供必需参数应抛出异常
        with self.assertRaises(ValueError):
            parser.parse([])
            
        result = parser.parse(["-f", "test.txt"])
        self.assertEqual(result["file"], "test.txt")
        
    def test_choices_validation(self):
        """测试选项值验证"""
        parser = create_parser(prog="test")
        parser.add_argument(
            long="level",
            arg_type=ArgType.OPTION,
            choices=["debug", "info", "warn", "error"]
        )
        
        result = parser.parse(["--level=debug"])
        self.assertEqual(result["level"], "debug")
        
        # 无效值应抛出异常
        with self.assertRaises(ValueError):
            parser.parse(["--level=trace"])
            
    def test_unknown_option(self):
        """测试未知选项"""
        parser = create_parser(prog="test")
        
        with self.assertRaises(ValueError):
            parser.parse(["--unknown"])


class TestDefaultValues(unittest.TestCase):
    """默认值测试"""
    
    def test_default_value(self):
        """测试默认值"""
        parser = create_parser(prog="test")
        parser.add_argument(
            long="mode",
            arg_type=ArgType.OPTION,
            default="normal"
        )
        
        result = parser.parse([])
        self.assertEqual(result["mode"], "normal")
        
        result = parser.parse(["--mode=fast"])
        self.assertEqual(result["mode"], "fast")
        
    def test_multiple_values(self):
        """测试多值参数"""
        parser = create_parser(prog="test")
        parser.add_argument(
            short="I",
            long="include",
            arg_type=ArgType.OPTION,
            multiple=True
        )
        
        result = parser.parse(["-I", "/usr/include", "-I", "/usr/local/include"])
        self.assertEqual(result["include"], ["/usr/include", "/usr/local/include"])


class TestSubcommands(unittest.TestCase):
    """子命令测试"""
    
    def test_basic_subcommand(self):
        """测试基本子命令"""
        parser = create_parser(prog="git", description="版本控制工具")
        
        # 添加全局选项
        parser.add_argument(short="v", long="verbose")
        
        # 添加commit子命令
        commit_cmd = parser.add_command("commit", help_text="提交更改")
        commit_cmd.arguments.append(Argument(
            name="message",
            short="m",
            long="message",
            arg_type=ArgType.OPTION,
            required=True
        ))
        commit_cmd.arguments.append(Argument(
            name="all",
            short="a",
            long="all",
            arg_type=ArgType.FLAG
        ))
        
        result = parser.parse(["commit", "-m", "Initial commit", "-a"])
        
        self.assertEqual(result.command, "commit")
        self.assertEqual(result.command_args["message"], "Initial commit")
        self.assertTrue(result.command_args["all"])
        
    def test_subcommand_path(self):
        """测试子命令路径"""
        parser = create_parser(prog="tool")
        
        # 创建嵌套子命令
        remote_cmd = parser.add_command("remote")
        remote_cmd.arguments.append(Argument(
            name="verbose",
            short="v",
            arg_type=ArgType.FLAG
        ))
        
        result = parser.parse(["remote", "-v"])
        self.assertEqual(result.command, "remote")
        self.assertEqual(result.subcommand_path, ["remote"])


class TestHelpGeneration(unittest.TestCase):
    """帮助生成测试"""
    
    def test_format_help(self):
        """测试帮助信息格式化"""
        parser = create_parser(
            prog="myapp",
            description="一个示例应用程序",
            version="1.0.0"
        )
        parser.add_argument(short="v", long="verbose", help_text="详细输出")
        parser.add_argument(short="f", long="file", arg_type=ArgType.OPTION, help_text="输入文件")
        parser.add_argument(
            long="level",
            arg_type=ArgType.OPTION,
            choices=["debug", "info", "warn"],
            default="info",
            help_text="日志级别"
        )
        
        help_text = parser.format_help()
        
        self.assertIn("用法:", help_text)
        self.assertIn("myapp", help_text)
        self.assertIn("详细输出", help_text)
        self.assertIn("输入文件", help_text)
        self.assertIn("debug, info, warn", help_text)
        self.assertIn("1.0.0", help_text)
        
    def test_format_usage(self):
        """测试用法摘要"""
        parser = create_parser(prog="myapp")
        parser.add_argument(short="v", long="verbose")
        parser.add_argument(name="input", arg_type=ArgType.POSITIONAL, required=True)
        parser.add_argument(name="output", arg_type=ArgType.POSITIONAL)
        
        usage = parser.format_usage()
        
        self.assertIn("用法:", usage)
        self.assertIn("[选项]", usage)
        self.assertIn("<input>", usage)


class TestParseResult(unittest.TestCase):
    """解析结果测试"""
    
    def test_get_method(self):
        """测试get方法"""
        parser = create_parser(prog="test")
        parser.add_argument(long="name", arg_type=ArgType.OPTION, default="default")
        
        result = parser.parse([])
        
        self.assertEqual(result.get("name"), "default")
        self.assertEqual(result.get("missing", "fallback"), "fallback")
        
    def test_dict_access(self):
        """测试字典式访问"""
        parser = create_parser(prog="test")
        parser.add_argument(long="key", arg_type=ArgType.OPTION)
        
        result = parser.parse(["--key=value"])
        
        self.assertEqual(result["key"], "value")
        self.assertIn("key", result)
        self.assertNotIn("missing", result)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_double_dash_separator(self):
        """测试 -- 分隔符"""
        parser = create_parser(prog="test")
        parser.add_argument(short="v", long="verbose")
        
        result = parser.parse(["-v", "--", "not-an-option", "another"])
        
        self.assertTrue(result["verbose"])
        self.assertEqual(result.positional, ["not-an-option", "another"])
        
    def test_empty_args(self):
        """测试空参数列表"""
        parser = create_parser(prog="test")
        parser.add_argument(short="v", long="verbose")
        
        result = parser.parse([])
        
        self.assertIsNone(result.get("verbose"))
        self.assertEqual(result.positional, [])
        
    def test_dest_override(self):
        """测试目标键名覆盖"""
        parser = create_parser(prog="test")
        parser.add_argument(long="very-long-option-name", dest="short_name", arg_type=ArgType.OPTION)
        
        result = parser.parse(["--very-long-option-name=value"])
        
        self.assertEqual(result["short_name"], "value")
        self.assertNotIn("very_long_option_name", result.args)


class TestRealWorldScenarios(unittest.TestCase):
    """真实场景测试"""
    
    def test_ls_like_command(self):
        """测试类似ls的命令"""
        parser = create_parser(prog="ls", description="列出目录内容")
        parser.add_argument(short="a", long="all", help_text="显示隐藏文件")
        parser.add_argument(short="l", long="long", help_text="长格式")
        parser.add_argument(short="h", long="human-readable", help_text="人类可读大小")
        parser.add_argument(short="t", long="time", help_text="按时间排序")
        parser.add_argument(short="r", long="reverse", help_text="反向排序")
        parser.add_argument(name="directory", arg_type=ArgType.POSITIONAL, default=".")
        
        result = parser.parse(["-la", "/home/user"])
        
        self.assertTrue(result["all"])
        self.assertTrue(result["long"])
        self.assertIsNone(result.get("human_readable"))
        self.assertEqual(result["directory"], "/home/user")
        
    def test_grep_like_command(self):
        """测试类似grep的命令"""
        parser = create_parser(prog="grep", description="搜索文本模式")
        parser.add_argument(short="i", long="ignore-case", help_text="忽略大小写")
        parser.add_argument(short="v", long="invert-match", help_text="反向匹配")
        parser.add_argument(short="n", long="line-number", help_text="显示行号")
        parser.add_argument(short="c", long="count", help_text="只显示匹配行数")
        parser.add_argument(short="r", long="recursive", help_text="递归搜索")
        parser.add_argument(
            short="e",
            long="regexp",
            arg_type=ArgType.OPTION,
            multiple=True,
            help_text="匹配模式"
        )
        parser.add_argument(name="pattern", arg_type=ArgType.POSITIONAL, required=True)
        parser.add_argument(name="files", arg_type=ArgType.POSITIONAL, multiple=True)
        
        result = parser.parse(["-in", "error", "*.log"])
        
        self.assertTrue(result["ignore_case"])
        self.assertTrue(result["line_number"])
        self.assertEqual(result["pattern"], "error")
        self.assertEqual(result["files"], ["*.log"])  # multiple=True 收集剩余位置参数
        
    def test_build_tool_command(self):
        """测试构建工具命令"""
        parser = create_parser(prog="build", description="构建系统")
        parser.add_argument(
            long="target",
            arg_type=ArgType.OPTION,
            choices=["debug", "release", "test"],
            default="debug",
            help_text="构建目标"
        )
        parser.add_argument(
            long="jobs",
            short="j",
            arg_type=ArgType.OPTION,
            type_converter=int_converter,
            default=4,
            help_text="并行任务数"
        )
        parser.add_argument(long="clean", help_text="清理后构建")
        parser.add_argument(long="verbose", short="v", help_text="详细输出")
        
        result = parser.parse(["--target=release", "-j", "8", "--clean"])
        
        self.assertEqual(result["target"], "release")
        self.assertEqual(result["jobs"], 8)
        self.assertTrue(result["clean"])
        self.assertIsNone(result.get("verbose"))


if __name__ == "__main__":
    unittest.main(verbosity=2)