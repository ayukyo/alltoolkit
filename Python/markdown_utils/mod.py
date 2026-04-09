#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Markdown Utilities Module
======================================
A comprehensive Markdown parsing, generation, and manipulation utility module 
for Python with zero external dependencies.

Features:
    - Markdown to HTML conversion
    - HTML to Markdown conversion
    - Markdown element parsing and extraction
    - Table generation and parsing
    - Link and image extraction
    - Heading hierarchy analysis
    - Code block handling
    - List manipulation
    - Markdown validation
    - Content transformation

Author: AllToolkit Contributors
License: MIT
"""

import re
from typing import Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Type Aliases
# ============================================================================

MarkdownText = str
HtmlText = str
LineNumber = int


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class HeadingInfo:
    """Heading information extracted from Markdown."""
    level: int  # 1-6
    text: str
    line_number: LineNumber
    anchor: str
    
    def to_markdown(self) -> str:
        """Convert back to Markdown."""
        return f"{'#' * self.level} {self.text}"


@dataclass
class LinkInfo:
    """Link information extracted from Markdown."""
    text: str
    url: str
    title: Optional[str]
    line_number: LineNumber
    is_image: bool = False
    
    def to_markdown(self) -> str:
        """Convert back to Markdown."""
        if self.is_image:
            title_part = f' "{self.title}"' if self.title else ""
            return f"![{self.text}]({self.url}{title_part})"
        else:
            title_part = f' "{self.title}"' if self.title else ""
            return f"[{self.text}]({self.url}{title_part})"


@dataclass
class CodeBlockInfo:
    """Code block information extracted from Markdown."""
    language: str
    code: str
    line_number: LineNumber
    is_inline: bool = False
    
    def to_markdown(self) -> str:
        """Convert back to Markdown."""
        if self.is_inline:
            return f"`{self.code}`"
        else:
            return f"```{self.language}\n{self.code}\n```"


@dataclass
class TableInfo:
    """Table information extracted from Markdown."""
    headers: List[str]
    rows: List[List[str]]
    alignments: List[str]  # 'left', 'center', 'right'
    line_number: LineNumber
    
    def to_markdown(self) -> str:
        """Convert back to Markdown."""
        lines = []
        
        # Header row
        header_line = "| " + " | ".join(self.headers) + " |"
        lines.append(header_line)
        
        # Separator row
        sep_parts = []
        for align in self.alignments:
            if align == 'center':
                sep_parts.append(":---:")
            elif align == 'right':
                sep_parts.append("---:")
            else:
                sep_parts.append(":---")
        sep_line = "|" + "|".join(sep_parts) + "|"
        lines.append(sep_line)
        
        # Data rows
        for row in self.rows:
            row_line = "| " + " | ".join(row) + " |"
            lines.append(row_line)
        
        return "\n".join(lines)


# ============================================================================
# HTML Entity Handling
# ============================================================================

HTML_ENTITIES = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    '`': '&#96;',
}

HTML_ENTITIES_REVERSE = {v: k for k, v in HTML_ENTITIES.items()}


def escape_html(text: str) -> str:
    """
    Escape HTML special characters.
    
    Args:
        text: Plain text to escape
        
    Returns:
        HTML-escaped text
        
    Example:
        >>> escape_html("<script>alert('XSS')</script>")
        "&lt;script&gt;alert(&#39;XSS&#39;)&lt;/script&gt;"
    """
    result = text
    for char, entity in HTML_ENTITIES.items():
        result = result.replace(char, entity)
    return result


def unescape_html(text: str) -> str:
    """
    Unescape HTML entities.
    
    Args:
        text: HTML-escaped text
        
    Returns:
        Plain text
        
    Example:
        >>> unescape_html("&lt;div&gt;")
        "<div>"
    """
    result = text
    for entity, char in HTML_ENTITIES_REVERSE.items():
        result = result.replace(entity, char)
    return result


# ============================================================================
# Markdown to HTML Conversion
# ============================================================================

def markdown_to_html(markdown: MarkdownText, extensions: List[str] = None) -> HtmlText:
    """
    Convert Markdown text to HTML.
    
    Args:
        markdown: Markdown text to convert
        extensions: List of extensions to enable ('toc', 'tables', 'fenced_code')
        
    Returns:
        HTML string
        
    Example:
        >>> markdown_to_html("# Hello")
        "<h1>Hello</h1>"
    """
    if extensions is None:
        extensions = ['tables', 'fenced_code']
    
    html = markdown
    
    # Store code blocks to protect them from other transformations
    code_blocks = []
    
    def store_code_block(match):
        code_blocks.append(match.group(0))
        return f"\x00CODE{len(code_blocks) - 1}\x00"
    
    # Store fenced code blocks
    html = re.sub(r'```[\s\S]*?```', store_code_block, html)
    
    # Store inline code
    html = re.sub(r'`[^`]+`', store_code_block, html)
    
    # Headers (must be processed first)
    html = re.sub(r'^######\s+(.+)$', r'<h6>\1</h6>', html, flags=re.MULTILINE)
    html = re.sub(r'^#####\s+(.+)$', r'<h5>\1</h5>', html, flags=re.MULTILINE)
    html = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Bold and Italic
    html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'___(.+?)___', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)
    
    # Strikethrough
    html = re.sub(r'~~(.+?)~~', r'<del>\1</del>', html)
    
    # Images (before links)
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)(?:\s+"([^"]*)")?\)', 
                  r'<img src="\2" alt="\1" title="\3"/>', html)
    
    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)(?:\s+"([^"]*)")?\)', 
                  r'<a href="\2" title="\3">\1</a>', html)
    
    # Reference-style links
    def replace_ref_link(match):
        text = match.group(1)
        ref = match.group(2)
        # Find the reference definition
        ref_match = re.search(rf'^\[{ref}\]:\s*(\S+)(?:\s+"([^"]*)")?', html, re.MULTILINE)
        if ref_match:
            url = ref_match.group(1)
            title = ref_match.group(2) or ''
            return f'<a href="{url}" title="{title}">{text}</a>'
        return match.group(0)
    
    html = re.sub(r'\[([^\]]+)\]\[([^\]]*)\]', replace_ref_link, html)
    
    # Tables
    if 'tables' in extensions:
        html = re.sub(r'\|(.+)\|', lambda m: _convert_table_row(m.group(1)), html)
    
    # Horizontal rules
    html = re.sub(r'^(\*{3,}|-{3,}|_{3,})$', r'<hr/>', html, flags=re.MULTILINE)
    
    # Blockquotes
    html = re.sub(r'^>\s*(.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # Unordered lists
    html = re.sub(r'^[\*\-]\s+(.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>\n?)+', lambda m: f'<ul>\n{m.group(0)}</ul>', html)
    
    # Ordered lists
    html = re.sub(r'^\d+\.\s+(.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # Line breaks
    html = re.sub(r'  $', '<br/>', html, flags=re.MULTILINE)
    
    # Paragraphs (simple version)
    lines = html.split('\n')
    result_lines = []
    in_paragraph = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_paragraph:
                result_lines.append('</p>')
                in_paragraph = False
            result_lines.append('')
        elif stripped.startswith('<h') or stripped.startswith('<ul') or \
             stripped.startswith('<ol') or stripped.startswith('<li') or \
             stripped.startswith('<blockquote') or stripped.startswith('<hr') or \
             stripped.startswith('\x00CODE'):
            if in_paragraph:
                result_lines.append('</p>')
                in_paragraph = False
            result_lines.append(line)
        else:
            if not in_paragraph and stripped:
                result_lines.append('<p>')
                in_paragraph = True
            result_lines.append(line)
    
    if in_paragraph:
        result_lines.append('</p>')
    
    html = '\n'.join(result_lines)
    
    # Restore code blocks
    for i, code in enumerate(code_blocks):
        if code.startswith('```'):
            # Fenced code block
            lines = code.strip('`').strip().split('\n', 1)
            lang = lines[0].strip() if lines else ''
            code_content = lines[1] if len(lines) > 1 else ''
            code_content = escape_html(code_content)
            html = html.replace(f'\x00CODE{i}\x00', f'<pre><code class="language-{lang}">{code_content}</code></pre>')
        else:
            # Inline code
            code_content = escape_html(code.strip('`'))
            html = html.replace(f'\x00CODE{i}\x00', f'<code>{code_content}</code>')
    
    return html.strip()


def _convert_table_row(content: str) -> str:
    """Convert a table row to HTML."""
    cells = [c.strip() for c in content.split('|')]
    cells = [c for c in cells if c]  # Remove empty cells
    
    if not cells:
        return ''
    
    # Check if this is a separator row
    if all(re.match(r'^:?-+:?$', c) for c in cells):
        return ''  # Skip separator in HTML output
    
    cell_type = 'th' if any(c.startswith('<th>') for c in cells) else 'td'
    html_cells = ''.join(f'<{cell_type}>{c}</{cell_type}>' for c in cells)
    return f'<tr>{html_cells}</tr>'


# ============================================================================
# HTML to Markdown Conversion
# ============================================================================

def html_to_markdown(html: HtmlText) -> MarkdownText:
    """
    Convert HTML text to Markdown.
    
    Args:
        html: HTML text to convert
        
    Returns:
        Markdown string
        
    Example:
        >>> html_to_markdown("<h1>Hello</h1>")
        "# Hello"
    """
    markdown = html
    
    # Remove DOCTYPE and html tags
    markdown = re.sub(r'<!DOCTYPE[^>]*>', '', markdown, flags=re.IGNORECASE)
    markdown = re.sub(r'</?html[^>]*>', '', markdown, flags=re.IGNORECASE)
    markdown = re.sub(r'</?head[^>]*>[\s\S]*?</head>', '', markdown, flags=re.IGNORECASE)
    markdown = re.sub(r'</?body[^>]*>', '', markdown, flags=re.IGNORECASE)
    
    # Headers
    for i in range(6, 0, -1):
        markdown = re.sub(rf'<h{i}[^>]*>(.+?)</h{i}>', lambda m: f"{'#' * i} {m.group(1)}", 
                         markdown, flags=re.IGNORECASE | re.DOTALL)
    
    # Bold and Italic
    markdown = re.sub(r'<strong>(.+?)</strong>', r'**\1**', markdown, flags=re.IGNORECASE | re.DOTALL)
    markdown = re.sub(r'<b>(.+?)</b>', r'**\1**', markdown, flags=re.IGNORECASE | re.DOTALL)
    markdown = re.sub(r'<em>(.+?)</em>', r'*\1*', markdown, flags=re.IGNORECASE | re.DOTALL)
    markdown = re.sub(r'<i>(.+?)</i>', r'*\1*', markdown, flags=re.IGNORECASE | re.DOTALL)
    
    # Strikethrough
    markdown = re.sub(r'<del>(.+?)</del>', r'~~\1~~', markdown, flags=re.IGNORECASE | re.DOTALL)
    markdown = re.sub(r'<s>(.+?)</s>', r'~~\1~~', markdown, flags=re.IGNORECASE | re.DOTALL)
    
    # Links
    markdown = re.sub(r'<a\s+href="([^"]+)"(?:\s+title="([^"]*)")?>(.+?)</a>', 
                     r'[\3](\1 "\2")', markdown, flags=re.IGNORECASE | re.DOTALL)
    markdown = re.sub(r'\s*""$', '', markdown)  # Clean up empty titles
    
    # Images
    markdown = re.sub(r'<img\s+src="([^"]+)"\s+alt="([^"]*)"(?:\s+title="([^"]*)")?\s*/?>', 
                     r'![\2](\1 "\3")', markdown, flags=re.IGNORECASE)
    
    # Code blocks
    markdown = re.sub(r'<pre><code(?:\s+class="language-(\w+)")?>(.+?)</code></pre>', 
                     r'```\1\n\2\n```', markdown, flags=re.IGNORECASE | re.DOTALL)
    markdown = re.sub(r'<code>(.+?)</code>', r'`\1`', markdown, flags=re.IGNORECASE | re.DOTALL)
    
    # Lists
    markdown = re.sub(r'<ul[^>]*>(.+?)</ul>', r'\1', markdown, flags=re.IGNORECASE | re.DOTALL)
    markdown = re.sub(r'<ol[^>]*>(.+?)</ol>', r'\1', markdown, flags=re.IGNORECASE | re.DOTALL)
    markdown = re.sub(r'<li[^>]*>(.+?)</li>', r'- \1', markdown, flags=re.IGNORECASE | re.DOTALL)
    
    # Blockquotes
    markdown = re.sub(r'<blockquote[^>]*>(.+?)</blockquote>', 
                     lambda m: '\n'.join(f'> {l}' for l in m.group(1).split('\n')), 
                     markdown, flags=re.IGNORECASE | re.DOTALL)
    
    # Horizontal rules
    markdown = re.sub(r'<hr\s*/?>', '---', markdown, flags=re.IGNORECASE)
    
    # Line breaks
    markdown = re.sub(r'<br\s*/?>', '  \n', markdown, flags=re.IGNORECASE)
    
    # Paragraphs
    markdown = re.sub(r'<p[^>]*>(.+?)</p>', r'\1\n', markdown, flags=re.IGNORECASE | re.DOTALL)
    
    # Tables
    markdown = re.sub(r'<table[^>]*>(.+?)</table>', 
                     lambda m: _convert_html_table(m.group(1)), 
                     markdown, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove remaining tags
    markdown = re.sub(r'<[^>]+>', '', markdown)
    
    # Unescape HTML entities
    markdown = unescape_html(markdown)
    
    # Clean up whitespace
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    
    return markdown.strip()


def _convert_html_table(html: str) -> str:
    """Convert HTML table to Markdown."""
    rows = re.findall(r'<tr[^>]*>(.+?)</tr>', html, re.IGNORECASE | re.DOTALL)
    if not rows:
        return ''
    
    markdown_rows = []
    
    for i, row in enumerate(rows):
        cells = re.findall(r'<t[hd][^>]*>(.+?)</t[hd]>', row, re.IGNORECASE | re.DOTALL)
        if cells:
            markdown_rows.append('| ' + ' | '.join(cells) + ' |')
            
            # Add separator after header
            if i == 0:
                separator = '| ' + ' | '.join(['---'] * len(cells)) + ' |'
                markdown_rows.append(separator)
    
    return '\n'.join(markdown_rows)


# ============================================================================
# Markdown Parsing and Extraction
# ============================================================================

def extract_headings(markdown: MarkdownText) -> List[HeadingInfo]:
    """
    Extract all headings from Markdown text.
    
    Args:
        markdown: Markdown text to parse
        
    Returns:
        List of HeadingInfo objects
        
    Example:
        >>> extract_headings("# Hello\\n## World")
        [HeadingInfo(level=1, text='Hello', ...), HeadingInfo(level=2, text='World', ...)]
    """
    headings = []
    lines = markdown.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            anchor = _generate_anchor(text)
            headings.append(HeadingInfo(
                level=level,
                text=text,
                line_number=line_num,
                anchor=anchor
            ))
    
    return headings


def extract_links(markdown: MarkdownText, include_images: bool = True) -> List[LinkInfo]:
    """
    Extract all links from Markdown text.
    
    Args:
        markdown: Markdown text to parse
        include_images: Whether to include image links
        
    Returns:
        List of LinkInfo objects
        
    Example:
        >>> extract_links("[Google](https://google.com)")
        [LinkInfo(text='Google', url='https://google.com', ...)]
    """
    links = []
    lines = markdown.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        # Images
        if include_images:
            for match in re.finditer(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)', line):
                links.append(LinkInfo(
                    text=match.group(1),
                    url=match.group(2),
                    title=match.group(3),
                    line_number=line_num,
                    is_image=True
                ))
        
        # Links (not images)
        for match in re.finditer(r'(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)', line):
            links.append(LinkInfo(
                text=match.group(1),
                url=match.group(2),
                title=match.group(3),
                line_number=line_num,
                is_image=False
            ))
    
    return links


def extract_code_blocks(markdown: MarkdownText) -> List[CodeBlockInfo]:
    """
    Extract all code blocks from Markdown text.
    
    Args:
        markdown: Markdown text to parse
        
    Returns:
        List of CodeBlockInfo objects
        
    Example:
        >>> extract_code_blocks("```python\\nprint('hello')\\n```")
        [CodeBlockInfo(language='python', code="print('hello')", ...)]
    """
    code_blocks = []
    lines = markdown.split('\n')
    
    # Fenced code blocks
    in_block = False
    block_start = 0
    language = ''
    block_lines = []
    
    for line_num, line in enumerate(lines, 1):
        if not in_block:
            match = re.match(r'^```(\w*)', line)
            if match:
                in_block = True
                block_start = line_num
                language = match.group(1)
                block_lines = []
        else:
            if line.strip() == '```':
                code_blocks.append(CodeBlockInfo(
                    language=language,
                    code='\n'.join(block_lines),
                    line_number=block_start,
                    is_inline=False
                ))
                in_block = False
            else:
                block_lines.append(line)
    
    # Inline code
    for line_num, line in enumerate(lines, 1):
        for match in re.finditer(r'`([^`]+)`', line):
            code_blocks.append(CodeBlockInfo(
                language='',
                code=match.group(1),
                line_number=line_num,
                is_inline=True
            ))
    
    return code_blocks


def extract_tables(markdown: MarkdownText) -> List[TableInfo]:
    """
    Extract all tables from Markdown text.
    
    Args:
        markdown: Markdown text to parse
        
    Returns:
        List of TableInfo objects
        
    Example:
        >>> extract_tables("| A | B |\\n|---|---|\\n| 1 | 2 |")
        [TableInfo(headers=['A', 'B'], rows=[['1', '2']], ...)]
    """
    tables = []
    lines = markdown.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts a table
        if re.match(r'^\|.*\|$', line):
            # Parse header
            headers = [h.strip() for h in line.strip('|').split('|')]
            
            # Check for separator line
            if i + 1 < len(lines) and re.match(r'^[\s|:-]+$', lines[i + 1]):
                sep_line = lines[i + 1]
                alignments = []
                for cell in sep_line.strip('|').split('|'):
                    cell = cell.strip()
                    if cell.startswith(':') and cell.endswith(':'):
                        alignments.append('center')
                    elif cell.endswith(':'):
                        alignments.append('right')
                    else:
                        alignments.append('left')
                
                # Parse data rows
                rows = []
                j = i + 2
                while j < len(lines) and re.match(r'^\|.*\|$', lines[j]):
                    row = [c.strip() for c in lines[j].strip('|').split('|')]
                    rows.append(row)
                    j += 1
                
                tables.append(TableInfo(
                    headers=headers,
                    rows=rows,
                    alignments=alignments,
                    line_number=i + 1
                ))
                
                i = j
                continue
        
        i += 1
    
    return tables


def _generate_anchor(text: str) -> str:
    """Generate a URL-safe anchor from heading text."""
    anchor = text.lower()
    anchor = re.sub(r'[^\w\s-]', '', anchor)
    anchor = re.sub(r'[-\s]+', '-', anchor)
    anchor = anchor.strip('-')
    return anchor


# ============================================================================
# Markdown Generation Utilities
# ============================================================================

def create_table(headers: List[str], rows: List[List[str]], 
                 alignments: List[str] = None) -> str:
    """
    Create a Markdown table.
    
    Args:
        headers: List of header texts
        rows: List of row data (each row is a list of strings)
        alignments: List of alignments ('left', 'center', 'right')
        
    Returns:
        Markdown table string
        
    Example:
        >>> create_table(['Name', 'Age'], [['Alice', '30'], ['Bob', '25']])
        "| Name | Age |\\n|:---|:---|\\n| Alice | 30 |\\n| Bob | 25 |"
    """
    if alignments is None:
        alignments = ['left'] * len(headers)
    
    # Ensure alignments match headers
    while len(alignments) < len(headers):
        alignments.append('left')
    
    lines = []
    
    # Header row
    lines.append("| " + " | ".join(headers) + " |")
    
    # Separator row
    sep_parts = []
    for align in alignments[:len(headers)]:
        if align == 'center':
            sep_parts.append(":---:")
        elif align == 'right':
            sep_parts.append("---:")
        else:
            sep_parts.append(":---")
    lines.append("|" + "|".join(sep_parts) + "|")
    
    # Data rows
    for row in rows:
        # Pad row to match headers
        while len(row) < len(headers):
            row.append('')
        lines.append("| " + " | ".join(row[:len(headers)]) + " |")
    
    return "\n".join(lines)


def create_link(text: str, url: str, title: str = None) -> str:
    """
    Create a Markdown link.
    
    Args:
        text: Link text
        url: Link URL
        title: Optional link title
        
    Returns:
        Markdown link string
        
    Example:
        >>> create_link("Google", "https://google.com")
        "[Google](https://google.com)"
    """
    if title:
        return f'[{text}]({url} "{title}")'
    return f"[{text}]({url})"


def create_image(alt: str, url: str, title: str = None) -> str:
    """
    Create a Markdown image.
    
    Args:
        alt: Alt text
        url: Image URL
        title: Optional title
        
    Returns:
        Markdown image string
        
    Example:
        >>> create_image("Logo", "logo.png")
        "![Logo](logo.png)"
    """
    if title:
        return f'![{alt}]({url} "{title}")'
    return f"![{alt}]({url})"


def create_code_block(code: str, language: str = '') -> str:
    """
    Create a fenced code block.
    
    Args:
        code: Code content
        language: Programming language
        
    Returns:
        Markdown code block string
        
    Example:
        >>> create_code_block("print('hello')", "python")
        "```python\\nprint('hello')\\n```"
    """
    return f"```{language}\n{code}\n```"


def create_inline_code(code: str) -> str:
    """
    Create inline code.
    
    Args:
        code: Code content
        
    Returns:
        Markdown inline code string
        
    Example:
        >>> create_inline_code("print('hello')")
        "`print('hello')`"
    """
    return f"`{code}`"


def create_list(items: List[str], ordered: bool = False, start: int = 1) -> str:
    """
    Create a Markdown list.
    
    Args:
        items: List of items
        ordered: Whether to create ordered list
        start: Starting number for ordered lists
        
    Returns:
        Markdown list string
        
    Example:
        >>> create_list(['A', 'B', 'C'])
        "- A\\n- B\\n- C"
    """
    lines = []
    for i, item in enumerate(items):
        if ordered:
            lines.append(f"{start + i}. {item}")
        else:
            lines.append(f"- {item}")
    return "\n".join(lines)


def create_blockquote(text: str) -> str:
    """
    Create a blockquote.
    
    Args:
        text: Quote text
        
    Returns:
        Markdown blockquote string
        
    Example:
        >>> create_blockquote("Hello")
        "> Hello"
    """
    lines = text.split('\n')
    return '\n'.join(f"> {line}" for line in lines)


def create_horizontal_rule(style: str = 'dash') -> str:
    """
    Create a horizontal rule.
    
    Args:
        style: Style of the rule ('dash', 'asterisk', 'underscore')
        
    Returns:
        Markdown horizontal rule string
        
    Example:
        >>> create_horizontal_rule()
        "---"
    """
    styles = {
        'dash': '---',
        'asterisk': '***',
        'underscore': '___'
    }
    return styles.get(style, '---')


def create_heading(text: str, level: int = 1) -> str:
    """
    Create a heading.
    
    Args:
        text: Heading text
        level: Heading level (1-6)
        
    Returns:
        Markdown heading string
        
    Example:
        >>> create_heading("Hello", 1)
        "# Hello"
    """
    level = max(1, min(6, level))
    return f"{'#' * level} {text}"


# ============================================================================
# Markdown Validation
# ============================================================================

def validate_markdown(markdown: MarkdownText) -> Tuple[bool, List[str]]:
    """
    Validate Markdown syntax and return issues found.
    
    Args:
        markdown: Markdown text to validate
        
    Returns:
        Tuple of (is_valid, list of issues)
        
    Example:
        >>> validate_markdown("**bold")
        (False, ["Unclosed bold marker at line 1"])
    """
    issues = []
    lines = markdown.split('\n')
    
    # Check for unclosed formatting
    for line_num, line in enumerate(lines, 1):
        # Check bold/italic markers
        if line.count('**') % 2 != 0:
            issues.append(f"Unclosed bold marker at line {line_num}")
        if re.search(r'(?<!\*)\*(?!\*)(?:(?!\*|$).)*$', line) and line.count('*') % 2 != 0:
            issues.append(f"Unclosed italic marker at line {line_num}")
        
        # Check code blocks
        if line.count('`') % 2 != 0 and '```' not in line:
            issues.append(f"Unclosed inline code marker at line {line_num}")
        
        # Check link syntax
        link_matches = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', line)
        for match in link_matches:
            if not match[1]:
                issues.append(f"Empty link URL at line {line_num}")
        
        # Check image syntax
        img_matches = re.findall(r'!\[([^\]]*)\]\(([^)]*)\)', line)
        for match in img_matches:
            if not match[1]:
                issues.append(f"Empty image URL at line {line_num}")
    
    # Check heading hierarchy
    headings = extract_headings(markdown)
    if headings:
        prev_level = 0
        for heading in headings:
            if heading.level > prev_level + 1:
                issues.append(
                    f"Heading level skip: h{prev_level} to h{heading.level} "
                    f"at line {heading.line_number}"
                )
            prev_level = heading.level
    
    # Check for fenced code blocks
    in_block = False
    block_start = 0
    for line_num, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            if not in_block:
                in_block = True
                block_start = line_num
            else:
                in_block = False
    
    if in_block:
        issues.append(f"Unclosed code block starting at line {block_start}")
    
    return len(issues) == 0, issues


# ============================================================================
# Markdown Transformation
# ============================================================================

def transform_headings(markdown: MarkdownText, offset: int = 0) -> MarkdownText:
    """
    Transform heading levels by an offset.
    
    Args:
        markdown: Markdown text to transform
        offset: Level offset (positive to increase, negative to decrease)
        
    Returns:
        Transformed Markdown string
        
    Example:
        >>> transform_headings("# Hello", 1)
        "## Hello"
    """
    lines = markdown.split('\n')
    result = []
    
    for line in lines:
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            new_level = max(1, min(6, level + offset))
            result.append(f"{'#' * new_level} {match.group(2)}")
        else:
            result.append(line)
    
    return '\n'.join(result)


def remove_formatting(markdown: MarkdownText, keep: List[str] = None) -> MarkdownText:
    """
    Remove Markdown formatting.
    
    Args:
        markdown: Markdown text to clean
        keep: List of formatting types to keep ('headers', 'links', 'code', 'lists')
        
    Returns:
        Plain text or partially formatted text
        
    Example:
        >>> remove_formatting("**bold** and *italic*")
        "bold and italic"
    """
    if keep is None:
        keep = []
    
    result = markdown
    
    # Remove bold/italic
    if 'formatting' not in keep:
        result = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', result)
        result = re.sub(r'___(.+?)___', r'\1', result)
        result = re.sub(r'\*\*(.+?)\*\*', r'\1', result)
        result = re.sub(r'__(.+?)__', r'\1', result)
        result = re.sub(r'\*(.+?)\*', r'\1', result)
        result = re.sub(r'_(.+?)_', r'\1', result)
        result = re.sub(r'~~(.+?)~~', r'\1', result)
    
    # Remove links
    if 'links' not in keep:
        result = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', result)
    
    # Remove images
    if 'images' not in keep:
        result = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', result)
    
    # Remove code
    if 'code' not in keep:
        result = re.sub(r'```[\s\S]*?```', '', result)
        result = re.sub(r'`([^`]+)`', r'\1', result)
    
    # Remove headers
    if 'headers' not in keep:
        result = re.sub(r'^#{1,6}\s+(.+)$', r'\1', result, flags=re.MULTILINE)
    
    # Remove blockquotes
    if 'quotes' not in keep:
        result = re.sub(r'^>\s*', '', result, flags=re.MULTILINE)
    
    # Remove list markers
    if 'lists' not in keep:
        result = re.sub(r'^[\*\-]\s+', '', result, flags=re.MULTILINE)
        result = re.sub(r'^\d+\.\s+', '', result, flags=re.MULTILINE)
    
    # Remove horizontal rules
    result = re.sub(r'^[\*\-_]{3,}$', '', result, flags=re.MULTILINE)
    
    return result


def word_count(markdown: MarkdownText) -> Dict[str, int]:
    """
    Count words and characters in Markdown text.
    
    Args:
        markdown: Markdown text to analyze
        
    Returns:
        Dictionary with word_count, char_count, line_count
        
    Example:
        >>> word_count("# Hello World")
        {'word_count': 2, 'char_count': 11, 'line_count': 1}
    """
    # Remove formatting for accurate word count
    plain = remove_formatting(markdown)
    
    # Count words
    words = re.findall(r'\b\w+\b', plain)
    
    return {
        'word_count': len(words),
        'char_count': len(plain.replace(' ', '').replace('\n', '')),
        'line_count': len(markdown.split('\n'))
    }


# ============================================================================
# Utility Functions
# ============================================================================

def join_markdown(*documents: MarkdownText, separator: str = '\n\n---\n\n') -> MarkdownText:
    """
    Join multiple Markdown documents.
    
    Args:
        documents: Markdown documents to join
        separator: Separator to use between documents
        
    Returns:
        Combined Markdown string
        
    Example:
        >>> join_markdown("# Doc1", "# Doc2")
        "# Doc1\\n\\n---\\n\\n# Doc2"
    """
    return separator.join(doc for doc in documents if doc.strip())


def split_by_heading(markdown: MarkdownText, max_level: int = 2) -> Dict[str, str]:
    """
    Split Markdown document by headings.
    
    Args:
        markdown: Markdown text to split
        max_level: Maximum heading level to split on
        
    Returns:
        Dictionary mapping heading text to section content
        
    Example:
        >>> split_by_heading("# A\\nContent A\\n# B\\nContent B")
        {'A': 'Content A', 'B': 'Content B'}
    """
    sections = {}
    lines = markdown.split('\n')
    
    current_heading = None
    current_content = []
    
    for line in lines:
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match and len(match.group(1)) <= max_level:
            # Save previous section
            if current_heading:
                sections[current_heading] = '\n'.join(current_content).strip()
            
            # Start new section
            current_heading = match.group(2).strip()
            current_content = []
        elif current_heading:
            current_content.append(line)
    
    # Save last section
    if current_heading:
        sections[current_heading] = '\n'.join(current_content).strip()
    
    return sections


def strip_comments(markdown: MarkdownText) -> MarkdownText:
    """
    Remove HTML comments from Markdown.
    
    Args:
        markdown: Markdown text
        
    Returns:
        Markdown without comments
        
    Example:
        >>> strip_comments("Hello <!-- comment --> World")
        "Hello  World"
    """
    return re.sub(r'<!--[\s\S]*?-->', '', markdown)
