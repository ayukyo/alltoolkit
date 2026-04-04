using System;
using AllToolkit.StringUtils;

namespace AllToolkit.Examples
{
    /// <summary>
    /// StringUtils 使用示例
    /// </summary>
    class StringUtilsExample
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== StringUtils 使用示例 ===\n");

            Example1_Trim();
            Example2_Split();
            Example3_Replace();
            Example4_CaseConversion();
            Example5_Validation();
            Example6_Substring();
            Example7_JoinAndRepeat();
            Example8_Cleanup();
        }

        static void Example1_Trim()
        {
            Console.WriteLine("1. 字符串修剪");
            Console.WriteLine("--------------");
            
            string text = "   hello world   ";
            Console.WriteLine($"原始: '{text}'");
            Console.WriteLine($"Trim: '{StringUtils.Trim(text)}'");
            Console.WriteLine($"TrimLeft: '{StringUtils.TrimLeft(text)}'");
            Console.WriteLine($"TrimRight: '{StringUtils.TrimRight(text)}'");
            Console.WriteLine($"TrimChars: '{StringUtils.TrimChars("...hello...", new[] { '.' })}'");
            Console.WriteLine();
        }

        static void Example2_Split()
        {
            Console.WriteLine("2. 字符串分割");
            Console.WriteLine("--------------");
            
            string csv = "apple,banana,cherry";
            var fruits = StringUtils.Split(csv, ",");
            Console.WriteLine($"Split '{csv}': [{string.Join(", ", fruits)}]");
            
            var limited = StringUtils.Split(csv, ",", 2);
            Console.WriteLine($"Split (max 2): [{string.Join(", ", limited)}]");
            
            var byChar = StringUtils.SplitChar("a,b,c", ',');
            Console.WriteLine($"SplitChar: [{string.Join(", ", byChar)}]");
            Console.WriteLine();
        }

        static void Example3_Replace()
        {
            Console.WriteLine("3. 字符串替换");
            Console.WriteLine("--------------");
            
            string text = "hello world world";
            Console.WriteLine($"原始: '{text}'");
            Console.WriteLine($"Replace all: '{StringUtils.Replace(text, "world", "C#")}'");
            Console.WriteLine($"ReplaceFirst: '{StringUtils.ReplaceFirst(text, "world", "C#")}'");
            Console.WriteLine($"ReplaceN (2): '{StringUtils.ReplaceN(text, "world", "C#", 2)}'");
            Console.WriteLine();
        }

        static void Example4_CaseConversion()
        {
            Console.WriteLine("4. 大小写转换");
            Console.WriteLine("--------------");
            
            string text = "hello world";
            Console.WriteLine($"原始: '{text}'");
            Console.WriteLine($"ToUpper: '{StringUtils.ToUpper(text)}'");
            Console.WriteLine($"ToLower: '{StringUtils.ToLower(text)}'");
            Console.WriteLine($"ToTitleCase: '{StringUtils.ToTitleCase(text)}'");
            
            string camel = "helloWorldExample";
            Console.WriteLine($"ToSnakeCase: '{StringUtils.ToSnakeCase(camel)}'");
            Console.WriteLine($"ToCamelCase: '{StringUtils.ToCamelCase("hello_world")}'");
            Console.WriteLine();
        }

        static void Example5_Validation()
        {
            Console.WriteLine("5. 字符串验证");
            Console.WriteLine("--------------");
            
            Console.WriteLine($"IsBlank('   '): {StringUtils.IsBlank("   ")}");
            Console.WriteLine($"IsNotBlank('hello'): {StringUtils.IsNotBlank("hello")}");
            Console.WriteLine($"IsNumeric('123.45'): {StringUtils.IsNumeric("123.45")}");
            Console.WriteLine($"IsInteger('-42'): {StringUtils.IsInteger("-42")}");
            Console.WriteLine($"IsEmail('test@example.com'): {StringUtils.IsEmail("test@example.com")}");
            Console.WriteLine($"IsAlphanumeric('abc123'): {StringUtils.IsAlphanumeric("abc123")}");
            Console.WriteLine();
        }

        static void Example6_Substring()
        {
            Console.WriteLine("6. 子字符串操作");
            Console.WriteLine("----------------");
            
            string text = "hello world";
            Console.WriteLine($"原始: '{text}'");
            Console.WriteLine($"Left(5): '{StringUtils.Left(text, 5)}'");
            Console.WriteLine($"Right(5): '{StringUtils.Right(text, 5)}'");
            Console.WriteLine($"DropLeft(6): '{StringUtils.DropLeft(text, 6)}'");
            Console.WriteLine($"DropRight(6): '{StringUtils.DropRight(text, 6)}'");
            Console.WriteLine($"Substring(6, 5): '{StringUtils.Substring(text, 6, 5)}'");
            Console.WriteLine();
        }

        static void Example7_JoinAndRepeat()
        {
            Console.WriteLine("7. 字符串连接与重复");
            Console.WriteLine("--------------------");
            
            var parts = new[] { "apple", "banana", "cherry" };
            Console.WriteLine($"Join: '{StringUtils.Join(", ", parts)}'");
            Console.WriteLine($"Repeat('ab', 3): '{StringUtils.Repeat("ab", 3)}'");
            Console.WriteLine($"Reverse('hello'): '{StringUtils.Reverse("hello")}'");
            Console.WriteLine();
        }

        static void Example8_Cleanup()
        {
            Console.WriteLine("8. 字符串清理");
            Console.WriteLine("--------------");
            
            string messy = "  hello   world  ";
            Console.WriteLine($"原始: '{messy}'");
            Console.WriteLine($"NormalizeWhitespace: '{StringUtils.NormalizeWhitespace(messy)}'");
            Console.WriteLine($"RemoveWhitespace: '{StringUtils.RemoveWhitespace(messy)}'");
            Console.WriteLine($"Truncate(8): '{StringUtils.Truncate("hello world", 8)}'");
            Console.WriteLine($"TruncateWithEllipsis(8): '{StringUtils.TruncateWithEllipsis("hello world", 8)}'");
            Console.WriteLine();
        }
    }
}
