using System;
using System.Collections.Generic;
using AllToolkit;

namespace MarkdownUtilsExamples
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=" * 60);
            Console.WriteLine("MarkdownUtils Usage Examples (C#)");
            Console.WriteLine("=" * 60);
            Console.WriteLine();

            // Example 1: Convert Markdown to HTML
            Console.WriteLine("1. Convert Markdown to HTML");
            Console.WriteLine("-" * 40);
            var markdown1 = @"# Hello World

This is a **bold** statement with *italic* text.

## Features

- Item 1
- Item 2
- Item 3

[Click here](https://example.com) for more info.

```csharp
Console.WriteLine(""Hello, World!"");
```";

            var html1 = MarkdownUtils.ToHtml(markdown1);
            Console.WriteLine(html1);
            Console.WriteLine();

            // Example 2: Extract headings
            Console.WriteLine("2. Extract Headings");
            Console.WriteLine("-" * 40);
            var markdown2 = @"# Main Title

## Chapter 1

### Section 1.1

### Section 1.2

## Chapter 2

### Section 2.1";

            var headings = MarkdownUtils.ExtractHeadings(markdown2);
            foreach (var h in headings)
            {
                var indent = new string(' ', (h.Level - 1) * 2);
                Console.WriteLine($"{indent}Level {h.Level}: {h.Text} (#{h.Anchor})");
            }
            Console.WriteLine();

            // Example 3: Generate Table of Contents
            Console.WriteLine("3. Generate Table of Contents");
            Console.WriteLine("-" * 40);
            var toc = MarkdownUtils.GenerateToc(markdown2);
            Console.WriteLine(toc);

            // Example 4: Extract links
            Console.WriteLine("4. Extract Links");
            Console.WriteLine("-" * 40);
            var markdown4 = @"Check out [OpenAI](https://openai.com) and [GitHub](https://github.com).

Also visit [Ruby](https://ruby-lang.org) for more.";

            var links = MarkdownUtils.ExtractLinks(markdown4);
            foreach (var link in links)
            {
                Console.WriteLine($"  Text: {link.Text}");
                Console.WriteLine($"  URL:  {link.Url}");
                Console.WriteLine();
            }

            // Example 5: Extract images
            Console.WriteLine("5. Extract Images");
            Console.WriteLine("-" * 40);
            var markdown5 = @"![Logo](logo.png ""Company Logo"")

Here is a screenshot:

![Screenshot](https://example.com/screenshot.png)";

            var images = MarkdownUtils.ExtractImages(markdown5);
            foreach (var img in images)
            {
                Console.WriteLine($"  Alt:   {img.Alt}");
                Console.WriteLine($"  URL:   {img.Url}");
                if (img.Title != null)
                {
                    Console.WriteLine($"  Title: {img.Title}");
                }
                Console.WriteLine();
            }

            // Example 6: Extract code blocks
            Console.WriteLine("6. Extract Code Blocks");
            Console.WriteLine("-" * 40);
            var markdown6 = @"Here is some C# code:

```csharp
public void Greet(string name)
{
    Console.WriteLine($""Hello, {name}!"");
}
```

And some Python:

```python
def greet(name):
    print(f""Hello, {name}!"")
```

Use `inline_code` for short snippets.";

            var blocks = MarkdownUtils.ExtractCodeBlocks(markdown6);
            foreach (var block in blocks)
            {
                if (block.Inline)
                {
                    Console.WriteLine($"  [Inline] {block.Code}");
                }
                else
                {
                    var lang = block.Language ?? "plain";
                    Console.WriteLine($"  [{lang}] {block.Code.Split('\n')[0]}...");
                }
            }
            Console.WriteLine();

            // Example 7: Extract tables
            Console.WriteLine("7. Extract Tables");
            Console.WriteLine("-" * 40);
            var markdown7 = @"| Name  | Age | City     |
|-------|-----|----------|
| Alice | 30  | New York |
| Bob   | 25  | London   |
| Carol | 28  | Paris    |";

            var tables = MarkdownUtils.ExtractTables(markdown7);
            foreach (var table in tables)
            {
                Console.WriteLine($"  Headers: {string.Join(", ", table.Headers)}");
                Console.WriteLine($"  Rows: {table.Rows.Count}");
                foreach (var row in table.Rows)
                {
                    Console.WriteLine($"    - {string.Join(" | ", row)}");
                }
            }
            Console.WriteLine();

            // Example 8: Get statistics
            Console.WriteLine("8. Document Statistics");
            Console.WriteLine("-" * 40);
            var markdown8 = @"# Sample Document

This is a sample markdown document with **various** formatting.

## Links

Check [GitHub](https://github.com) and [OpenAI](https://openai.com).

## Images

![Logo](logo.png)
![Banner](banner.png)

## Code

```javascript
console.log(""Hello!"");
```

- Item 1
- Item 2
- Item 3";

            var stats = MarkdownUtils.GetStats(markdown8);
            Console.WriteLine($"  Characters: {stats.Characters}");
            Console.WriteLine($"  Characters (no spaces): {stats.CharactersNoSpaces}");
            Console.WriteLine($"  Words: {stats.Words}");
            Console.WriteLine($"  Lines: {stats.Lines}");
            Console.WriteLine($"  Paragraphs: {stats.Paragraphs}");
            Console.WriteLine($"  Headings: {stats.Headings}");
            Console.WriteLine($"  Links: {stats.Links}");
            Console.WriteLine($"  Images: {stats.Images}");
            Console.WriteLine($"  Code blocks: {stats.CodeBlocks}");
            Console.WriteLine($"  Tables: {stats.Tables}");
            Console.WriteLine($"  Reading time: ~{stats.ReadingTimeMinutes} min");
            Console.WriteLine();

            // Example 9: Convert to plain text
            Console.WriteLine("9. Convert to Plain Text");
            Console.WriteLine("-" * 40);
            var markdown9 = @"# Important Notice

This is **bold** and *italic* text.

[Click here](https://example.com) for details.

```
Code block
```

> A wise quote";

            var plain = MarkdownUtils.ToPlainText(markdown9);
            Console.WriteLine(plain);
            Console.WriteLine();

            // Example 10: Validate Markdown
            Console.WriteLine("10. Validate Markdown");
            Console.WriteLine("-" * 40);
            var samples = new[] {
                "# Valid Title\n\nContent here",
                "",
                null,
                "Just plain text",
                "**Bold** and *italic*"
            };

            foreach (var sample in samples)
            {
                var isValid = MarkdownUtils.IsValidMarkdown(sample);
                var display = sample == null ? "null" : (sample == "" ? "empty" : sample.Substring(0, Math.Min(30, sample.Length)));
                Console.WriteLine($"  \"{display}\": {isValid}");
            }
            Console.WriteLine();

            Console.WriteLine("=" * 60);
            Console.WriteLine("All examples completed successfully!");
            Console.WriteLine("=" * 60);
        }
    }
}