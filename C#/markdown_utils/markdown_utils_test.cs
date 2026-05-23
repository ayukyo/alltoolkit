using System;
using System.Collections.Generic;
using System.Linq;
using AllToolkit;

namespace MarkdownUtilsTests
{
    class Program
    {
        static int TestsPassed = 0;
        static int TestsFailed = 0;

        static void Main(string[] args)
        {
            Console.WriteLine("=" * 60);
            Console.WriteLine("MarkdownUtils Test Suite (C#)");
            Console.WriteLine("=" * 60);
            Console.WriteLine();

            // Test 1: ToHtml - Basic heading
            Test("ToHtml - Basic heading", () =>
            {
                var html = MarkdownUtils.ToHtml("# Hello World");
                Assert(html.Contains("<h1>"), "Expected <h1> tag");
                Assert(html.Contains("Hello World"), "Expected 'Hello World'");
                Assert(html.Contains("</h1>"), "Expected closing tag");
                return true;
            });

            // Test 2: ToHtml - Bold text
            Test("ToHtml - Bold text", () =>
            {
                var html = MarkdownUtils.ToHtml("This is **bold** text");
                Assert(html.Contains("<strong>"), "Expected <strong> tag");
                return true;
            });

            // Test 3: ToHtml - Italic text
            Test("ToHtml - Italic text", () =>
            {
                var html = MarkdownUtils.ToHtml("This is *italic* text");
                Assert(html.Contains("<em>"), "Expected <em> tag");
                return true;
            });

            // Test 4: ToHtml - Links
            Test("ToHtml - Links", () =>
            {
                var html = MarkdownUtils.ToHtml("[OpenAI](https://openai.com)");
                Assert(html.Contains("<a href=\"https://openai.com\">"), "Expected <a> tag with href");
                Assert(html.Contains("OpenAI</a>"), "Expected link text");
                return true;
            });

            // Test 5: ToHtml - Images
            Test("ToHtml - Images", () =>
            {
                var html = MarkdownUtils.ToHtml("![Alt text](https://example.com/image.png)");
                Assert(html.Contains("<img"), "Expected <img> tag");
                Assert(html.Contains("src=\"https://example.com/image.png\""), "Expected src attribute");
                Assert(html.Contains("alt=\"Alt text\""), "Expected alt attribute");
                return true;
            });

            // Test 6: ToHtml - Code blocks
            Test("ToHtml - Code blocks", () =>
            {
                var html = MarkdownUtils.ToHtml("```csharp\nConsole.WriteLine(\"Hello\");\n```");
                Assert(html.Contains("<pre><code"), "Expected <pre><code> tags");
                Assert(html.Contains("language-csharp"), "Expected language class");
                return true;
            });

            // Test 7: ToHtml - Inline code
            Test("ToHtml - Inline code", () =>
            {
                var html = MarkdownUtils.ToHtml("Use the `Console.WriteLine` method");
                Assert(html.Contains("<code>"), "Expected <code> tag");
                return true;
            });

            // Test 8: ToHtml - Blockquotes
            Test("ToHtml - Blockquotes", () =>
            {
                var html = MarkdownUtils.ToHtml("> This is a quote");
                Assert(html.Contains("<blockquote>"), "Expected <blockquote> tag");
                return true;
            });

            // Test 9: ToHtml - Horizontal rules
            Test("ToHtml - Horizontal rules", () =>
            {
                var html = MarkdownUtils.ToHtml("Content\n\n---\n\nMore content");
                Assert(html.Contains("<hr>"), "Expected <hr> tag");
                return true;
            });

            // Test 10: ToHtml - Tables
            Test("ToHtml - Tables", () =>
            {
                var markdown = "| Name | Age |\n|------|-----|\n| Alice | 30 |\n| Bob | 25 |";
                var html = MarkdownUtils.ToHtml(markdown);
                Assert(html.Contains("<table>"), "Expected <table> tag");
                Assert(html.Contains("<thead>"), "Expected <thead> tag");
                Assert(html.Contains("<tbody>"), "Expected <tbody> tag");
                return true;
            });

            // Test 11: ExtractHeadings - Basic extraction
            Test("ExtractHeadings - Basic extraction", () =>
            {
                var markdown = "# Main Title\n## Section 1\n### Subsection";
                var headings = MarkdownUtils.ExtractHeadings(markdown);
                Assert(headings.Count == 3, "Expected 3 headings");
                Assert(headings[0].Level == 1, "Wrong first heading level");
                Assert(headings[0].Text == "Main Title", "Wrong first heading text");
                return true;
            });

            // Test 12: ExtractHeadings - Anchor generation
            Test("ExtractHeadings - Anchor generation", () =>
            {
                var markdown = "# Hello World!\n## This is a Test";
                var headings = MarkdownUtils.ExtractHeadings(markdown);
                Assert(headings[0].Anchor == "hello-world", "Wrong anchor format");
                Assert(headings[1].Anchor == "this-is-a-test", "Wrong second anchor");
                return true;
            });

            // Test 13: GenerateToc - Basic TOC
            Test("GenerateToc - Basic TOC", () =>
            {
                var markdown = "# Title\n## Section 1\n## Section 2\n### Subsection";
                var toc = MarkdownUtils.GenerateToc(markdown);
                Assert(toc.Contains("Table of Contents"), "Expected TOC header");
                Assert(toc.Contains("#title"), "Expected link to Title");
                return true;
            });

            // Test 14: GenerateToc - Max level filtering
            Test("GenerateToc - Max level filtering", () =>
            {
                var markdown = "# H1\n## H2\n### H3\n#### H4";
                var toc = MarkdownUtils.GenerateToc(markdown, 2);
                Assert(!toc.Contains("h3"), "Should not contain h3");
                Assert(!toc.Contains("h4"), "Should not contain h4");
                return true;
            });

            // Test 15: ExtractLinks - Basic extraction
            Test("ExtractLinks - Basic extraction", () =>
            {
                var markdown = "Check out [OpenAI](https://openai.com) and [Google](https://google.com)";
                var links = MarkdownUtils.ExtractLinks(markdown);
                Assert(links.Count == 2, "Expected 2 links");
                Assert(links[0].Text == "OpenAI", "Wrong first link text");
                Assert(links[0].Url == "https://openai.com", "Wrong first link URL");
                return true;
            });

            // Test 16: ExtractLinks - Don't extract images
            Test("ExtractLinks - Don't extract images", () =>
            {
                var markdown = "![Image](img.png) and [Link](url.com)";
                var links = MarkdownUtils.ExtractLinks(markdown);
                Assert(links.Count == 1, "Expected 1 link (not image)");
                Assert(links[0].Text == "Link", "Wrong link text");
                return true;
            });

            // Test 17: ExtractImages - Basic extraction
            Test("ExtractImages - Basic extraction", () =>
            {
                var markdown = "![Logo](logo.png) and ![Icon](icon.png)";
                var images = MarkdownUtils.ExtractImages(markdown);
                Assert(images.Count == 2, "Expected 2 images");
                Assert(images[0].Alt == "Logo", "Wrong first image alt");
                Assert(images[0].Url == "logo.png", "Wrong first image URL");
                return true;
            });

            // Test 18: ExtractCodeBlocks - Fenced code blocks
            Test("ExtractCodeBlocks - Fenced code blocks", () =>
            {
                var markdown = "```csharp\nConsole.WriteLine(\"Hello\");\n```\n```python\nprint(\"World\")\n```";
                var blocks = MarkdownUtils.ExtractCodeBlocks(markdown);
                var codeBlocks = blocks.Where(b => !b.Inline).ToList();
                Assert(codeBlocks.Count == 2, "Expected 2 code blocks");
                Assert(codeBlocks[0].Language == "csharp", "Wrong first language");
                return true;
            });

            // Test 19: ExtractTables - Basic table
            Test("ExtractTables - Basic table", () =>
            {
                var markdown = "| A | B |\n|---|---|\n| 1 | 2 |";
                var tables = MarkdownUtils.ExtractTables(markdown);
                Assert(tables.Count == 1, "Expected 1 table");
                Assert(tables[0].Headers.Length == 2, "Wrong header count");
                Assert(tables[0].Rows.Count == 1, "Wrong row count");
                return true;
            });

            // Test 20: GetStats - Basic statistics
            Test("GetStats - Basic statistics", () =>
            {
                var markdown = "# Title\n\nThis is a paragraph.\n\n- Item 1\n- Item 2\n\n![Image](img.png)\n\n[Link](url.com)";
                var stats = MarkdownUtils.GetStats(markdown);
                Assert(stats.Words > 0, "Expected words > 0");
                Assert(stats.Headings == 1, "Wrong heading count");
                Assert(stats.Links == 1, "Wrong link count");
                Assert(stats.Images == 1, "Wrong image count");
                return true;
            });

            // Test 21: ToPlainText - Basic conversion
            Test("ToPlainText - Basic conversion", () =>
            {
                var markdown = "# **Bold** Title\n\nThis is *italic* text with [link](url).\n\n```\ncode\n```";
                var plain = MarkdownUtils.ToPlainText(markdown);
                Assert(!plain.Contains("#"), "Should not contain #");
                Assert(!plain.Contains("**"), "Should not contain **");
                Assert(!plain.Contains("*"), "Should not contain *");
                return true;
            });

            // Test 22: ToPlainText - Preserve link text
            Test("ToPlainText - Preserve link text", () =>
            {
                var markdown = "Click [here](https://example.com) for info";
                var plain = MarkdownUtils.ToPlainText(markdown);
                Assert(plain.Contains("here"), "Should contain 'here'");
                Assert(!plain.Contains("https://"), "Should not contain URL");
                return true;
            });

            // Test 23: IsValidMarkdown
            Test("IsValidMarkdown - Validation", () =>
            {
                Assert(MarkdownUtils.IsValidMarkdown("# Title\n\nContent"), "Should be valid");
                Assert(!MarkdownUtils.IsValidMarkdown(""), "Empty should be invalid");
                Assert(!MarkdownUtils.IsValidMarkdown(null), "Null should be invalid");
                return true;
            });

            // Test 24: ToHtml - Strikethrough
            Test("ToHtml - Strikethrough", () =>
            {
                var html = MarkdownUtils.ToHtml("This is ~~deleted~~ text");
                Assert(html.Contains("<del>"), "Expected <del> tag");
                Assert(html.Contains("deleted"), "Expected 'deleted' text");
                return true;
            });

            // Summary
            Console.WriteLine();
            Console.WriteLine("=" * 60);
            Console.WriteLine($"Tests completed: {TestsPassed + TestsFailed}");
            Console.WriteLine($"Passed: {TestsPassed}");
            Console.WriteLine($"Failed: {TestsFailed}");
            Console.WriteLine("=" * 60);

            if (TestsFailed == 0)
            {
                Console.WriteLine("All tests passed!");
            }
        }

        static void Test(string name, Func<bool> test)
        {
            Console.Write($"{name}... ");
            try
            {
                if (test())
                {
                    Console.WriteLine("\x1b[32mPASSED\x1b[0m");
                    TestsPassed++;
                }
                else
                {
                    Console.WriteLine("\x1b[31mFAILED\x1b[0m");
                    TestsFailed++;
                }
            }
            catch (Exception e)
            {
                Console.WriteLine("\x1b[31mFAILED\x1b[0m");
                Console.WriteLine($"  Error: {e.Message}");
                TestsFailed++;
            }
        }

        static void Assert(bool condition, string message)
        {
            if (!condition)
            {
                throw new Exception(message);
            }
        }
    }
}