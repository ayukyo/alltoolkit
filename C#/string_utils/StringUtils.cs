using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace AllToolkit.StringUtils
{
    /// <summary>
    /// 字符串工具类 - 提供常用的字符串处理功能
    /// 零依赖，仅使用 .NET 标准库
    /// </summary>
    public static class StringUtils
    {
        #region 字符串修剪

        public static string TrimLeft(string str)
        {
            if (string.IsNullOrEmpty(str)) return str;
            return str.TrimStart();
        }

        public static string TrimRight(string str)
        {
            if (string.IsNullOrEmpty(str)) return str;
            return str.TrimEnd();
        }

        public static string Trim(string str)
        {
            if (string.IsNullOrEmpty(str)) return str;
            return str.Trim();
        }

        public static string TrimChars(string str, char[] chars)
        {
            if (string.IsNullOrEmpty(str) || chars == null || chars.Length == 0) return str;
            return str.Trim(chars);
        }

        #endregion

        #region 字符串分割

        public static string[] Split(string str, string separator)
        {
            if (string.IsNullOrEmpty(str)) return new string[0];
            if (string.IsNullOrEmpty(separator)) return new[] { str };
            return str.Split(new[] { separator }, StringSplitOptions.None);
        }

        public static string[] Split(string str, string separator, int maxSplits)
        {
            if (string.IsNullOrEmpty(str)) return new string[0];
            if (string.IsNullOrEmpty(separator) || maxSplits <= 0) return new[] { str };
            return str.Split(new[] { separator }, maxSplits, StringSplitOptions.None);
        }

        public static string[] SplitChar(string str, char separator)
        {
            if (string.IsNullOrEmpty(str)) return new string[0];
            return str.Split(separator);
        }

        #endregion

        #region 字符串替换

        public static string Replace(string str, string oldValue, string newValue)
        {
            if (string.IsNullOrEmpty(str) || string.IsNullOrEmpty(oldValue)) return str;
            return str.Replace(oldValue, newValue ?? "");
        }

        public static string ReplaceFirst(string str, string oldValue, string newValue)
        {
            if (string.IsNullOrEmpty(str) || string.IsNullOrEmpty(oldValue)) return str;
            int index = str.IndexOf(oldValue, StringComparison.Ordinal);
            if (index < 0) return str;
            return str.Substring(0, index) + (newValue ?? "") + str.Substring(index + oldValue.Length);
        }

        public static string ReplaceN(string str, string oldValue, string newValue, int count)
        {
            if (string.IsNullOrEmpty(str) || string.IsNullOrEmpty(oldValue) || count <= 0) return str;
            var sb = new StringBuilder();
            int startIndex = 0;
            int replaced = 0;
            while (replaced < count)
            {
                int index = str.IndexOf(oldValue, startIndex, StringComparison.Ordinal);
                if (index < 0) break;
                sb.Append(str.Substring(startIndex, index - startIndex));
                sb.Append(newValue ?? "");
                startIndex = index + oldValue.Length;
                replaced++;
            }
            sb.Append(str.Substring(startIndex));
            return sb.ToString();
        }

        #endregion

        #region 字符串查找

        public static int Count(string str, string substring)
        {
            if (string.IsNullOrEmpty(str) || string.IsNullOrEmpty(substring)) return 0;
            int count = 0;
            int index = 0;
            while ((index = str.IndexOf(substring, index, StringComparison.Ordinal)) != -1)
            {
                count++;
                index += substring.Length;
            }
            return count;
        }

        public static bool StartsWith(string str, string prefix)
        {
            if (string.IsNullOrEmpty(str) || string.IsNullOrEmpty(prefix)) return false;
            return str.StartsWith(prefix, StringComparison.Ordinal);
        }

        public static bool EndsWith(string str, string suffix)
        {
            if (string.IsNullOrEmpty(str) || string.IsNullOrEmpty(suffix)) return false;
            return str.EndsWith(suffix, StringComparison.Ordinal);
        }

        public static bool Contains(string str, string substring)
        {
            if (string.IsNullOrEmpty(str) || string.IsNullOrEmpty(substring)) return false;
            return str.Contains(substring, StringComparison.Ordinal);
        }

        #endregion

        #region 大小写转换

        public static string ToUpper(string str)
        {
            if (string.IsNullOrEmpty(str)) return str;
            return str.ToUpperInvariant();
        }

        public static string ToLower(string str)
        {
            if (string.IsNullOrEmpty(str)) return str;
            return str.ToLowerInvariant();
        }

        public static string ToTitleCase(string str)
        {
            if (string.IsNullOrEmpty(str)) return str;
            var words = str.Split(' ');
            for (int i = 0; i < words.Length; i++)
            {
                if (words[i].Length > 0)
                {
                    words[i] = char.ToUpperInvariant(words[i][0]) + words[i].Substring(1).ToLowerInvariant();
                }
            }
            return string.Join(" ", words);
        }

        public static string ToSnakeCase(string str)
        {
            if (string.IsNullOrEmpty(str)) return str;
            var sb = new StringBuilder();
            for (int i = 0; i < str.Length; i++)
            {
                char c = str[i];
                if (char.IsUpper(c))
                {
                    if (i > 0) sb.Append('_');
                    sb.Append(char.ToLowerInvariant(c));
                }
                else
                {
                    sb.Append(c);
                }
            }
            return sb.ToString();
        }

        public static string ToCamelCase(string str)
        {
            if (string.IsNullOrEmpty(str)) return str;
            var words = str.Split(new[] { '_', ' ', '-' }, StringSplitOptions.RemoveEmptyEntries);
            if (words.Length == 0) return str;
            var sb = new StringBuilder(words[0].ToLowerInvariant());
            for (int i = 1; i < words.Length; i++)
            {
                if (words[i].Length > 0)
                {
                    sb.Append(char.ToUpperInvariant(words[i][0]));
                    sb.Append(words[i].Substring(1).ToLowerInvariant());
                }
            }
            return sb.ToString();
        }

        #endregion

        #region 字符串验证

        public static bool IsNullOrEmpty(string str)
        {
            return string.IsNullOrEmpty(str);
        }

        public static bool IsNullOrWhiteSpace(string str)
        {
            return string.IsNullOrWhiteSpace(str);
        }

        public static bool IsBlank(string str)
        {
            return string.IsNullOrWhiteSpace(str);
        }

        public static bool IsNotBlank(string str)
        {
            return !string.IsNullOrWhiteSpace(str);
        }

        public static bool IsNumeric(string str)
        {
            if (string.IsNullOrEmpty(str)) return false;
            return str.All(c => char.IsDigit(c) || c == '.' || c == '-' || c == '+');
        }

        public static bool IsInteger(string str)
        {
            if (string.IsNullOrEmpty(str)) return false;
            return int.TryParse(str, out _);
        }

        public static bool IsFloat(string str)
        {
            if (string.IsNullOrEmpty(str)) return false;
            return double.TryParse(str, out _);
        }

        public static bool IsAlpha(string str)
        {
            if (string.IsNullOrEmpty(str)) return false;
            return str.All(char.IsLetter);
        }

        public static bool IsAlphanumeric(string str)
        {
            if (string.IsNullOrEmpty(str)) return false;
            return str.All(char.IsLetterOrDigit);
        }

        public static bool IsEmail(string str)
        {
            if (string.IsNullOrEmpty(str)) return false;
            const string pattern = @"^[^@\s]+@[^@\s]+\.[^@\s]+$";
            return Regex.IsMatch(str, pattern);
        }

        #endregion

        #region 子字符串操作

        public static string Substring(string str, int startIndex)
        {
            if (string.IsNullOrEmpty(str)) return str;
            if (startIndex < 0) startIndex = 0;
            if (startIndex >= str.Length) return "";
            return str.Substring(startIndex);
        }

        public static string Substring(string str, int startIndex, int length)
        {
            if (string.IsNullOrEmpty(str)) return str;
            if (startIndex < 0) startIndex = 0;
            if (startIndex >= str.Length) return "";
            if (length <= 0) return "";
            if (startIndex + length > str.Length) length = str.Length - startIndex;
            return str.Substring(startIndex, length);
        }

        public static string Left(string str, int length)
        {
            if (string.IsNullOrEmpty(str) || length <= 0) return "";
            if (length >= str.Length) return str;
            return str.Substring(0, length);
        }

        public static string Right(string str, int length)
        {
            if (string.IsNullOrEmpty(str) || length <= 0) return "";
            if (length >= str.Length) return str;
            return str.Substring(str.Length - length);
        }

        public static string DropLeft(string str, int length)
        {
            if (string.IsNullOrEmpty(str)) return str;
            if (length <= 0) return str;
            if (length >= str.Length) return "";
            return str.Substring(length);
        }

        public static string DropRight(string str, int length)
        {
            if (string.IsNullOrEmpty(str)) return str;
            if (length <= 0) return str;
            if (length >= str.Length) return "";
            return str.Substring(0, str.Length - length);
        }

        #endregion

        #region 字符串重复与连接

        public static string Repeat(string str, int count)
        {
            if (string.IsNullOrEmpty(str) || count <= 0) return "";
            if (count == 1) return str;
            var sb = new StringBuilder(str.Length * count);
            for (int i = 0; i < count; i++)
            {
                sb.Append(str);
            }
            return sb.ToString();
        }

        public static string Join(string separator, IEnumerable<string> values)
        {
            if (values == null) return "";
            return string.Join(separator, values);
        }

        public static string Join(string separator, params string[] values)
        {
            if (values == null) return "";
            return string.Join(separator, values);
        }

        #endregion

        #region 字符串清理

        public static string RemoveWhitespace(string str)
        {
            if (string.IsNullOrEmpty(str)) return str;
            return new string(str.Where(c => !char.IsWhiteSpace(c)).ToArray());
        }

        public static string RemoveChars(string str, char[] chars)
        {
            if (string.IsNullOrEmpty(str) || chars == null || chars.Length == 0) return str;
            var charSet = new HashSet<char>(chars);
            return new string(str.Where(c => !charSet.Contains(c)).ToArray());
        }

        public static string NormalizeWhitespace(string str)
        {
            if (string.IsNullOrEmpty(str)) return str;
            var sb = new StringBuilder();
            bool lastWasWhitespace = false;
            foreach (char c in str)
            {
                if (char.IsWhiteSpace(c))
                {
                    if (!lastWasWhitespace)
                    {
                        sb.Append(' ');
                        lastWasWhitespace = true;
                    }
                }
                else
                {
                    sb.Append(c);
                    lastWasWhitespace = false;
                }
            }
            return sb.ToString().Trim();
        }

        #endregion

        #region 字符串截断

        public static string Truncate(string str, int maxLength)
        {
            if (string.IsNullOrEmpty(str) || maxLength <= 0) return "";
            if (str.Length <= maxLength) return str;
            return str.Substring(0, maxLength);
        }

        public static string TruncateWithEllipsis(string str, int maxLength)
        {
            if (string.IsNullOrEmpty(str) || maxLength <= 3) return "...";
            if (str.Length <= maxLength) return str;
            return str.Substring(0, maxLength - 3) + "...";
        }

        #endregion

        #region 字符串填充

        public static string PadLeft(string str, int totalWidth, char paddingChar = ' ')
        {
            if (str == null) str = "";
            if (totalWidth <= str.Length) return str;
            return str.PadLeft(totalWidth, paddingChar);
        }

        public static string PadRight(string str, int totalWidth, char paddingChar = ' ')
        {
            if (str == null) str = "";
            if (totalWidth <= str.Length) return str;
            return str.PadRight(totalWidth, paddingChar);
        }

        public static string Center(string str, int totalWidth, char paddingChar = ' ')
        {
            if (str == null) str = "";
            if (totalWidth <= str.Length) return str;
            int leftPadding = (totalWidth - str.Length) / 2;
            int rightPadding = totalWidth - str.Length - leftPadding;
            return new string(paddingChar, leftPadding) + str + new string(paddingChar, rightPadding);
        }

        #endregion

        #region 字符串反转

        public static string Reverse(string str)
        {
            if (string.IsNullOrEmpty(str)) return str;
            char[] charArray = str.ToCharArray();
            Array.Reverse(charArray);
            return new string(charArray);
        }

        #endregion

        #region 字符串比较

        public static bool EqualsIgnoreCase(string str1, string str2)
        {
            return string.Equals(str1, str2, StringComparison.OrdinalIgnoreCase);
        }

        public static int Compare(string str1, string str2)
        {
            return string.Compare(str1, str2, StringComparison.Ordinal);
        }

        public static int CompareIgnoreCase(string str1, string str2)
        {
            return string.Compare(str1, str2, StringComparison.OrdinalIgnoreCase);
        }

        #endregion
    }
}
