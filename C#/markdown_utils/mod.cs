using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace AllToolkit
{
    /// <summary>
    /// Markdown processing utilities with zero external dependencies.
    /// </summary>
    public static class MarkdownUtils
    {
        #region Constants

        private static readonly Regex HeadingRegex = new Regex(@"^#{1,6}\s+(.+)$", RegexOptions.Multiline);
        private static readonly Regex HeadingAltRegex = new Regex(@"^([^\n]+)\n([=-]+)$", RegexOptions.Multiline);
        private static readonly Regex LinkRegex = new Regex(@"(?<!\!)\[([^\]]+)\]\(([^)]+)\)");
        private static readonly Regex ImageRegex = new Regex(@"!\[([^\]]*)\]\(([^)]+)(?:\s+\"([^\"]+)\")?\)");
        private static readonly Regex CodeBlockRegex = new Regex(@"```(\w*)\n([\s\S]*?)```");
        private static readonly Regex InlineCodeRegex = new Regex(@"`([^`]+)`");
        private static readonly Regex BoldRegex = new Regex(@"\*\*([^*]+)\*\*");
        private static readonly Regex ItalicRegex = new Regex(@"[*_]([^*_]+)[*_]");
        private static readonly Regex StrikethroughRegex = new Regex(@"~~([^~]+)~~");
        private static readonly Regex BlockquoteRegex = new Regex(@"^>\s+(.+)$", RegexOptions.Multiline);
        private static readonly Regex UnorderedListRegex = new Regex(@"^[\*\-\+]\s+(.+)$", RegexOptions.Multiline);
        private static readonly Regex OrderedListRegex = new Regex(@"^(\d+)\.\s+(.+)$", RegexOptions.Multiline);
        private static readonly Regex HorizontalRuleRegex = new Regex(@"^[-*_]{3,}$", RegexOptions.Multiline);
        private static readonly Regex TableRegex = new Regex(@"^\|(.+)\|$", RegexOptions.Multiline);
        private static readonly Regex TableSeparatorRegex = new Regex(@"^\|[\s\-:|]+\|$", RegexOptions.Multiline);

        #endregion

        #region Public Methods

        /// <summary>
        /// Convert Markdown to HTML.
        /// </summary>
        public static string ToHtml(string markdown)
        {
            if (string.IsNullOrEmpty(markdown)) return string.Empty;

            var html = markdown;

            // Process code blocks first (preserve content)
            html = ProcessCodeBlocks(html);

            // Process tables
            html = ProcessTables(html);

            // Process headings
            html = ProcessHeadings(html);

            // Process lists
            html = ProcessLists(html);

            // Process blockquotes
            html = ProcessBlockquotes(html);

            // Process horizontal rules
            html = ProcessHorizontalRules(html);

            // Process paragraphs
            html = ProcessParagraphs(html);

            // Process inline elements
            html = ProcessInlineElements(html);

            return html;
        }

        /// <summary>
        /// Extract all headings from Markdown.
        /// </summary>
        public static List<HeadingInfo> ExtractHeadings(string markdown)
        {
            if (string.IsNullOrEmpty(markdown)) return new List<HeadingInfo>();

            var headings = new List<HeadingInfo>();
            var lines = markdown.Split('\n');

            for (int i = 0; i < lines.Length; i++)
            {
                var line = lines[i].Trim();

                // Standard heading format
                var match = HeadingRegex.Match(line);
                if (match.Success)
                {
                    var level = line.TakeWhile(c => c == '#').Count();
                    var text = match.Groups[1].Value.Trim();
                    headings.Add(new HeadingInfo
                    {
                        Level = level,
                        Text = text,
                        Anchor = GenerateAnchor(text)
                    });
                    continue;
                }

                // Alternative heading format
                if (i + 1 < lines.Length)
                {
                    var nextLine = lines[i + 1].Trim();
                    if (nextLine.All(c => c == '=' || c == '-') && nextLine.Length >= 3)
                    {
                        var level = nextLine[0] == '=' ? 1 : 2;
                        var text = line.Trim();
                        headings.Add(new HeadingInfo
                        {
                            Level = level,
                            Text = text,
                            Anchor = GenerateAnchor(text)
                        });
                        i++; // Skip the underline
                    }
                }
            }

            return headings;
        }

        /// <summary>
        /// Generate Table of Contents from Markdown.
        /// </summary>
        public static string GenerateToc(string markdown, int maxLevel = 6)
        {
            var headings = ExtractHeadings(markdown);
            if (headings.Count == 0) return string.Empty;

            var filtered = headings.Where(h => h.Level <= maxLevel).ToList();
            if (filtered.Count == 0) return string.Empty;

            var toc = new StringBuilder();
            toc.AppendLine("# Table of Contents");
            toc.AppendLine();

            foreach (var heading in filtered)
            {
                var indent = new string(' ', (heading.Level - 1) * 2);
                toc.AppendLine($"{indent}- [{heading.Text}](#{heading.Anchor})");
            }

            toc.AppendLine();
            return toc.ToString();
        }

        /// <summary>
        /// Extract all links from Markdown.
        /// </summary>
        public static List<LinkInfo> ExtractLinks(string markdown)
        {
            if (string.IsNullOrEmpty(markdown)) return new List<LinkInfo>();

            var links = new List<LinkInfo>();
            var matches = LinkRegex.Matches(markdown);

            foreach (Match match in matches)
            {
                links.Add(new LinkInfo
                {
                    Text = match.Groups[1].Value,
                    Url = match.Groups[2].Value
                });
            }

            return links;
        }

        /// <summary>
        /// Extract all images from Markdown.
        /// </summary>
        public static List<ImageInfo> ExtractImages(string markdown)
        {
            if (string.IsNullOrEmpty(markdown)) return new List<ImageInfo>();

            var images = new List<ImageInfo>();
            var matches = ImageRegex.Matches(markdown);

            foreach (Match match in matches)
            {
                images.Add(new ImageInfo
                {
                    Alt = match.Groups[1].Value,
                    Url = match.Groups[2].Value,
                    Title = match.Groups[3].Success ? match.Groups[3].Value : null
                });
            }

            return images;
        }

        /// <summary>
        /// Extract all code blocks from Markdown.
        /// </summary>
        public static List<CodeBlockInfo> ExtractCodeBlocks(string markdown)
        {
            if (string.IsNullOrEmpty(markdown)) return new List<CodeBlockInfo>();

            var blocks = new List<CodeBlockInfo>();

            // Fenced code blocks
            var matches = CodeBlockRegex.Matches(markdown);
            foreach (Match match in matches)
            {
                blocks.Add(new CodeBlockInfo
                {
                    Language = match.Groups[1].Value,
                    Code = match.Groups[2].Value.TrimEnd('\n'),
                    Inline = false
                });
            }

            // Inline code
            var inlineMatches = InlineCodeRegex.Matches(markdown);
            foreach (Match match in inlineMatches)
            {
                blocks.Add(new CodeBlockInfo
                {
                    Code = match.Groups[1].Value,
                    Inline = true
                });
            }

            return blocks;
        }

        /// <summary>
        /// Extract all tables from Markdown.
        /// </summary>
        public static List<TableInfo> ExtractTables(string markdown)
        {
            if (string.IsNullOrEmpty(markdown)) return new List<TableInfo>();

            var tables = new List<TableInfo>();
            var lines = markdown.Split('\n');
            var i = 0;

            while (i < lines.Length)
            {
                var line = lines[i].Trim();

                if (IsTableRow(line))
                {
                    var table = new TableInfo();
                    table.Headers = ParseTableRow(line);

                    i++;
                    if (i < lines.Length && IsTableSeparator(lines[i].Trim()))
                    {
                        table.Alignments = ParseTableAlignment(lines[i].Trim());
                        i++;
                    }

                    table.Rows = new List<string[]>();
                    while (i < lines.Length && IsTableRow(lines[i].Trim()))
                    {
                        table.Rows.Add(ParseTableRow(lines[i].Trim()));
                        i++;
                    }

                    tables.Add(table);
                }
                else
                {
                    i++;
                }
            }

            return tables;
        }

        /// <summary>
        /// Get statistics about the Markdown content.
        /// </summary>
        public static MarkdownStats GetStats(string markdown)
        {
            if (string.IsNullOrEmpty(markdown))
            {
                return new MarkdownStats();
            }

            return new MarkdownStats
            {
                Characters = markdown.Length,
                CharactersNoSpaces = markdown.Replace(" ", "").Replace("\t", "").Replace("\n", "").Replace("\r", "").Length,
                Words = CountWords(markdown),
                Lines = markdown.Split('\n').Length,
                Paragraphs = CountParagraphs(markdown),
                Headings = ExtractHeadings(markdown).Count,
                Links = ExtractLinks(markdown).Count,
                Images = ExtractImages(markdown).Count,
                CodeBlocks = CodeBlockRegex.Matches(markdown).Count,
                Tables = ExtractTables(markdown).Count,
                ReadingTimeMinutes = Math.Max(1, CountWords(markdown) / 200)
            };
        }

        /// <summary>
        /// Strip all Markdown formatting to get plain text.
        /// </summary>
        public static string ToPlainText(string markdown)
        {
            if (string.IsNullOrEmpty(markdown)) return string.Empty;

            var text = markdown;

            // Remove code blocks
            text = CodeBlockRegex.Replace(text, string.Empty);
            text = InlineCodeRegex.Replace(text, string.Empty);

            // Remove images
            text = ImageRegex.Replace(text, string.Empty);

            // Remove links but keep text
            text = LinkRegex.Replace(text, "$1");

            // Remove formatting
            text = BoldRegex.Replace(text, "$1");
            text = ItalicRegex.Replace(text, "$1");
            text = StrikethroughRegex.Replace(text, "$1");

            // Remove heading markers
            text = HeadingRegex.Replace(text, "$1");

            // Remove blockquote markers
            text = BlockquoteRegex.Replace(text, "$1");

            // Remove list markers
            text = UnorderedListRegex.Replace(text, "$1");
            text = OrderedListRegex.Replace(text, "$2");

            // Remove horizontal rules
            text = HorizontalRuleRegex.Replace(text, string.Empty);

            // Remove table formatting
            text = TableRegex.Replace(text, m => m.Groups[1].Value.Replace("|", " "));
            text = TableSeparatorRegex.Replace(text, string.Empty);

            // Clean up whitespace
            text = Regex.Replace(text, @"\n{3,}", "\n\n");
            text = text.Trim();

            return text;
        }

        /// <summary>
        /// Check if content is valid Markdown.
        /// </summary>
        public static bool IsValidMarkdown(string content)
        {
            if (string.IsNullOrEmpty(content)) return false;

            var hasText = content.Trim().Length > 0;
            var hasMarkdownElements = Regex.IsMatch(content, @"[#*_`\[\]>|-]");

            return hasText && hasMarkdownElements;
        }

        #endregion

        #region Private Methods

        private static string ProcessCodeBlocks(string html)
        {
            return CodeBlockRegex.Replace(html, m =>
            {
                var lang = m.Groups[1].Value;
                var code = EscapeHtml(m.Groups[2].Value.TrimEnd('\n'));
                var langClass = string.IsNullOrEmpty(lang) ? string.Empty : $" class=\"language-{lang}\"";
                return $"<pre><code{langClass}>{code}</code></pre>";
            });
        }

        private static string ProcessTables(string html)
        {
            var lines = html.Split('\n');
            var result = new List<string>();
            var inTable = false;
            var tableLines = new List<string>();

            foreach (var line in lines)
            {
                var trimmed = line.Trim();

                if (IsTableRow(trimmed))
                {
                    inTable = true;
                    tableLines.Add(trimmed);
                }
                else if (inTable && string.IsNullOrWhiteSpace(trimmed))
                {
                    if (tableLines.Any(l => !IsTableSeparator(l)))
                    {
                        result.Add(ConvertTable(tableLines));
                    }
                    result.Add(string.Empty);
                    inTable = false;
                    tableLines.Clear();
                    result.Add(line);
                }
                else
                {
                    if (inTable)
                    {
                        if (tableLines.Any(l => !IsTableSeparator(l)))
                        {
                            result.Add(ConvertTable(tableLines));
                        }
                        inTable = false;
                        tableLines.Clear();
                    }
                    result.Add(line);
                }
            }

            if (inTable && tableLines.Any(l => !IsTableSeparator(l)))
            {
                result.Add(ConvertTable(tableLines));
            }

            return string.Join("\n", result);
        }

        private static string ConvertTable(List<string> lines)
        {
            if (lines.Count == 0) return string.Empty;

            var headers = ParseTableRow(lines[0]);
            var alignments = lines.Count > 1 && IsTableSeparator(lines[1])
                ? ParseTableAlignment(lines[1])
                : new string[headers.Length];
            var startIdx = alignments.Length > 0 ? 2 : 1;

            var rows = lines.Skip(startIdx).Select(ParseTableRow).ToList();

            var html = new StringBuilder();
            html.AppendLine("<table>");
            html.AppendLine("  <thead>");
            html.AppendLine("    <tr>");

            for (int i = 0; i < headers.Length; i++)
            {
                var align = alignments.Length > i ? GetAlignmentStyle(alignments[i]) : string.Empty;
                html.AppendLine($"      <th{align}>{ProcessInlineElements(headers[i].Trim())}</th>");
            }

            html.AppendLine("    </tr>");
            html.AppendLine("  </thead>");
            html.AppendLine("  <tbody>");

            foreach (var row in rows)
            {
                html.AppendLine("    <tr>");
                for (int i = 0; i < row.Length; i++)
                {
                    var align = alignments.Length > i ? GetAlignmentStyle(alignments[i]) : string.Empty;
                    html.AppendLine($"      <td{align}>{ProcessInlineElements(row[i].Trim())}</td>");
                }
                html.AppendLine("    </tr>");
            }

            html.AppendLine("  </tbody>");
            html.AppendLine("</table>");

            return html.ToString();
        }

        private static string[] ParseTableRow(string line)
        {
            return line.Split('|')
                .Skip(1)
                .Take(line.Split('|').Length - 2)
                .Select(s => s.Trim())
                .ToArray();
        }

        private static string[] ParseTableAlignment(string line)
        {
            var cells = ParseTableRow(line);
            return cells.Select(c =>
            {
                if (c.StartsWith(":") && c.EndsWith(":")) return "center";
                if (c.StartsWith(":")) return "left";
                if (c.EndsWith(":")) return "right";
                return null;
            }).ToArray();
        }

        private static string GetAlignmentStyle(string alignment)
        {
            return alignment == null ? string.Empty : $" style=\"text-align:{alignment}\"";
        }

        private static bool IsTableRow(string line)
        {
            return line.StartsWith("|") && line.EndsWith("|");
        }

        private static bool IsTableSeparator(string line)
        {
            return IsTableRow(line) && line.All(c => c == '|' || c == '-' || c == ':' || c == ' ');
        }

        private static string ProcessHeadings(string html)
        {
            var lines = html.Split('\n');
            var result = new List<string>();

            for (int i = 0; i < lines.Length; i++)
            {
                var line = lines[i].Trim();

                var match = HeadingRegex.Match(line);
                if (match.Success)
                {
                    var level = line.TakeWhile(c => c == '#').Count();
                    var text = ProcessInlineElements(match.Groups[1].Value.Trim());
                    result.Add($"<h{level}>{text}</h{level}>");
                }
                else if (i + 1 < lines.Length)
                {
                    var nextLine = lines[i + 1].Trim();
                    if (nextLine.All(c => c == '=' || c == '-') && nextLine.Length >= 3)
                    {
                        var level = nextLine[0] == '=' ? 1 : 2;
                        var text = ProcessInlineElements(line);
                        result.Add($"<h{level}>{text}</h{level}>");
                        i++;
                    }
                    else
                    {
                        result.Add(lines[i]);
                    }
                }
                else
                {
                    result.Add(lines[i]);
                }
            }

            return string.Join("\n", result);
        }

        private static string ProcessLists(string html)
        {
            var lines = html.Split('\n');
            var result = new List<string>();

            foreach (var line in lines)
            {
                var trimmed = line.Trim();

                var unorderedMatch = UnorderedListRegex.Match(trimmed);
                if (unorderedMatch.Success)
                {
                    var text = ProcessInlineElements(unorderedMatch.Groups[1].Value);
                    result.Add($"<ul>\n<li>{text}</li>\n</ul>");
                    continue;
                }

                var orderedMatch = OrderedListRegex.Match(trimmed);
                if (orderedMatch.Success)
                {
                    var text = ProcessInlineElements(orderedMatch.Groups[2].Value);
                    result.Add($"<ol>\n<li>{text}</li>\n</ol>");
                    continue;
                }

                result.Add(line);
            }

            return string.Join("\n", result);
        }

        private static string ProcessBlockquotes(string html)
        {
            return BlockquoteRegex.Replace(html, m =>
            {
                var text = ProcessInlineElements(m.Groups[1].Value);
                return $"<blockquote>{text}</blockquote>";
            });
        }

        private static string ProcessHorizontalRules(string html)
        {
            return HorizontalRuleRegex.Replace(html, "<hr>");
        }

        private static string ProcessParagraphs(string html)
        {
            var lines = html.Split('\n');
            var result = new List<string>();
            var paragraphBuffer = new StringBuilder();

            foreach (var line in lines)
            {
                var trimmed = line.Trim();

                if (trimmed.StartsWith("<") || string.IsNullOrWhiteSpace(trimmed))
                {
                    if (paragraphBuffer.Length > 0)
                    {
                        result.Add($"<p>{paragraphBuffer.ToString()}</p>");
                        paragraphBuffer.Clear();
                    }
                    result.Add(line);
                }
                else
                {
                    if (paragraphBuffer.Length > 0)
                    {
                        paragraphBuffer.Append("<br>");
                    }
                    paragraphBuffer.Append(trimmed);
                }
            }

            if (paragraphBuffer.Length > 0)
            {
                result.Add($"<p>{paragraphBuffer.ToString()}</p>");
            }

            return string.Join("\n", result);
        }

        private static string ProcessInlineElements(string text)
        {
            if (string.IsNullOrEmpty(text)) return text;

            // Escape HTML first
            var result = EscapeHtml(text);

            // Bold-italic first
            result = Regex.Replace(result, @"\*\*\*([^*]+)\*\*\*", "<strong><em>$1</em></strong>");

            // Bold
            result = BoldRegex.Replace(result, "<strong>$1</strong>");

            // Italic
            result = ItalicRegex.Replace(result, "<em>$1</em>");

            // Strikethrough
            result = StrikethroughRegex.Replace(result, "<del>$1</del>");

            // Inline code
            result = InlineCodeRegex.Replace(result, "<code>$1</code>");

            // Images (before links)
            result = ImageRegex.Replace(result, m =>
            {
                var alt = m.Groups[1].Value;
                var url = m.Groups[2].Value;
                return $"<img src=\"{url}\" alt=\"{alt}\">";
            });

            // Links
            result = LinkRegex.Replace(result, "<a href=\"$2\">$1</a>");

            return result;
        }

        private static string EscapeHtml(string text)
        {
            return text.Replace("&", "&amp;")
                       .Replace("<", "&lt;")
                       .Replace(">", "&gt;")
                       .Replace("\"", "&quot;");
        }

        private static string GenerateAnchor(string text)
        {
            return Regex.Replace(text.ToLower(), @"[^a-z0-9\s-]", string.Empty)
                       .Replace(" ", "-")
                       .Replace("--", "-")
                       .Trim('-');
        }

        private static int CountWords(string text)
        {
            return text.Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries).Length;
        }

        private static int CountParagraphs(string text)
        {
            return text.Split(new[] { "\n\n" }, StringSplitOptions.RemoveEmptyEntries)
                       .Count(p => !string.IsNullOrWhiteSpace(p));
        }

        #endregion

        #region Data Classes

        public class HeadingInfo
        {
            public int Level { get; set; }
            public string Text { get; set; }
            public string Anchor { get; set; }
        }

        public class LinkInfo
        {
            public string Text { get; set; }
            public string Url { get; set; }
        }

        public class ImageInfo
        {
            public string Alt { get; set; }
            public string Url { get; set; }
            public string Title { get; set; }
        }

        public class CodeBlockInfo
        {
            public string Language { get; set; }
            public string Code { get; set; }
            public bool Inline { get; set; }
        }

        public class TableInfo
        {
            public string[] Headers { get; set; }
            public string[] Alignments { get; set; }
            public List<string[]> Rows { get; set; }
        }

        public class MarkdownStats
        {
            public int Characters { get; set; }
            public int CharactersNoSpaces { get; set; }
            public int Words { get; set; }
            public int Lines { get; set; }
            public int Paragraphs { get; set; }
            public int Headings { get; set; }
            public int Links { get; set; }
            public int Images { get; set; }
            public int CodeBlocks { get; set; }
            public int Tables { get; set; }
            public int ReadingTimeMinutes { get; set; }
        }

        #endregion
    }
}