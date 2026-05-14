/**
 * Markdown Utilities - Zero-dependency markdown parser and converter
 * 
 * Features:
 * - Parse markdown to HTML
 * - Convert HTML to markdown (basic)
 * - Extract metadata (headings, links, images)
 * - Support for common markdown elements
 * - Customizable rendering options
 * 
 * @module markdown_utils
 */

/**
 * Markdown parser class
 */
class MarkdownParser {
    constructor(options = {}) {
        this.options = {
            gfm: true, // GitHub Flavored Markdown
            breaks: true, // Convert \n to <br>
            sanitize: false, // HTML sanitization (basic)
            ...options
        };
    }

    /**
     * Parse markdown text to HTML
     * @param {string} markdown - Markdown text
     * @returns {string} HTML output
     */
    parse(markdown) {
        if (!markdown || typeof markdown !== 'string') {
            return '';
        }

        let html = markdown;

        // Escape HTML (basic sanitization)
        if (this.options.sanitize) {
            html = this._escapeHtml(html);
        }

        // Code blocks (must be first to prevent other parsing inside)
        html = this._parseCodeBlocks(html);
        
        // Inline code
        html = this._parseInlineCode(html);

        // Headers
        html = this._parseHeaders(html);

        // Horizontal rules
        html = this._parseHorizontalRules(html);

        // Blockquotes
        html = this._parseBlockquotes(html);

        // Lists
        html = this._parseLists(html);

        // Tables (GFM)
        if (this.options.gfm) {
            html = this._parseTables(html);
        }

        // Paragraphs
        html = this._parseParagraphs(html);

        // Inline elements
        html = this._parseInlineElements(html);

        // Strikethrough (GFM)
        if (this.options.gfm) {
            html = this._parseStrikethrough(html);
        }

        // Task lists (GFM)
        if (this.options.gfm) {
            html = this._parseTaskLists(html);
        }

        return html.trim();
    }

    /**
     * Parse code blocks
     */
    _parseCodeBlocks(text) {
        // Fenced code blocks with language
        text = text.replace(/```(\w*)\n([\s\S]*?)```/g, (match, lang, code) => {
            const langClass = lang ? ` class="language-${lang}"` : '';
            return `<pre><code${langClass}>${this._escapeHtml(code.trim())}</code></pre>`;
        });

        // Indented code blocks
        text = text.replace(/^( {4}|\t)(.+)$/gm, (match, indent, code) => {
            // Only if not already in a code block
            if (!text.includes('<pre>')) {
                return `<code>${this._escapeHtml(code)}</code>`;
            }
            return match;
        });

        return text;
    }

    /**
     * Parse inline code
     */
    _parseInlineCode(text) {
        return text.replace(/`([^`]+)`/g, '<code>$1</code>');
    }

    /**
     * Parse headers
     */
    _parseHeaders(text) {
        return text.replace(/^(#{1,6})\s+(.+)$/gm, (match, hashes, content) => {
            const level = hashes.length;
            return `<h${level}>${content.trim()}</h${level}>`;
        });
    }

    /**
     * Parse horizontal rules
     */
    _parseHorizontalRules(text) {
        return text.replace(/^(-{3,}|\*{3,}|_{3,})$/gm, '<hr>');
    }

    /**
     * Parse blockquotes
     */
    _parseBlockquotes(text) {
        return text.replace(/^(>|&gt;)\s+(.+)$/gm, '<blockquote>$2</blockquote>');
    }

    /**
     * Parse lists
     */
    _parseLists(text) {
        // Unordered lists
        text = text.replace(/^([-*+])\s+(.+)$/gm, '<li>$2</li>');
        text = text.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

        // Ordered lists
        text = text.replace(/^(\d+)\.\s+(.+)$/gm, '<li>$2</li>');
        text = text.replace(/(<li>.*<\/li>\n?)+/g, (match) => {
            if (match.includes('<ul>')) return match;
            return `<ol>${match}</ol>`;
        });

        return text;
    }

    /**
     * Parse tables (GFM)
     */
    _parseTables(text) {
        const lines = text.split('\n');
        let result = [];
        let inTable = false;
        let tableLines = [];

        for (let line of lines) {
            if (line.match(/^\|(.+)\|$/)) {
                inTable = true;
                tableLines.push(line);
            } else {
                if (inTable) {
                    result.push(this._renderTable(tableLines));
                    tableLines = [];
                    inTable = false;
                }
                result.push(line);
            }
        }

        if (inTable) {
            result.push(this._renderTable(tableLines));
        }

        return result.join('\n');
    }

    /**
     * Render a table
     */
    _renderTable(lines) {
        if (lines.length < 2) return lines.join('\n');

        const headerCells = lines[0].split('|').filter(c => c.trim());
        const separator = lines[1];
        const bodyLines = lines.slice(2);

        // Parse alignment
        const alignments = separator.split('|')
            .filter(c => c.trim())
            .map(cell => {
                cell = cell.trim();
                if (cell.startsWith(':') && cell.endsWith(':')) return 'center';
                if (cell.endsWith(':')) return 'right';
                return 'left';
            });

        let html = '<table>\n<thead>\n<tr>\n';
        headerCells.forEach((cell, i) => {
            const align = alignments[i] || 'left';
            const alignAttr = align !== 'left' ? ` style="text-align:${align}"` : '';
            html += `<th${alignAttr}>${cell.trim()}</th>\n`;
        });
        html += '</tr>\n</thead>\n';

        if (bodyLines.length > 0) {
            html += '<tbody>\n';
            bodyLines.forEach(line => {
                const cells = line.split('|').filter(c => c.trim());
                if (cells.length > 0) {
                    html += '<tr>\n';
                    cells.forEach((cell, i) => {
                        const align = alignments[i] || 'left';
                        const alignAttr = align !== 'left' ? ` style="text-align:${align}"` : '';
                        html += `<td${alignAttr}>${cell.trim()}</td>\n`;
                    });
                    html += '</tr>\n';
                }
            });
            html += '</tbody>\n';
        }

        html += '</table>';
        return html;
    }

    /**
     * Parse paragraphs
     */
    _parseParagraphs(text) {
        const blocks = text.split(/\n\n+/);
        return blocks.map(block => {
            block = block.trim();
            if (!block) return '';
            
            // Don't wrap if already wrapped in block element
            if (block.match(/^<(h[1-6]|ul|ol|li|blockquote|pre|table|hr)/)) {
                return block;
            }
            
            return `<p>${block}</p>`;
        }).join('\n\n');
    }

    /**
     * Parse inline elements
     */
    _parseInlineElements(text) {
        // Images (must be before links!)
        text = text.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1">');

        // Links
        text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

        // Bold
        text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        text = text.replace(/__([^_]+)__/g, '<strong>$1</strong>');

        // Italic
        text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');
        text = text.replace(/_([^_]+)_/g, '<em>$1</em>');

        // Line breaks
        if (this.options.breaks) {
            text = text.replace(/\n/g, '<br>\n');
        }

        return text;
    }

    /**
     * Parse strikethrough (GFM)
     */
    _parseStrikethrough(text) {
        return text.replace(/~~(.+?)~~/g, '<del>$1</del>');
    }

    /**
     * Parse task lists (GFM)
     */
    _parseTaskLists(text) {
        return text.replace(/<li>\[([ xX])\]\s*(.+?)<\/li>/g, (match, checked, content) => {
            const isChecked = checked.toLowerCase() === 'x';
            const checkedAttr = isChecked ? ' checked' : '';
            return `<li><input type="checkbox" disabled${checkedAttr}> ${content}</li>`;
        });
    }

    /**
     * Escape HTML special characters
     */
    _escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
}

/**
 * Extract metadata from markdown
 * @param {string} markdown - Markdown text
 * @returns {Object} Metadata object with headings, links, images
 */
function extractMetadata(markdown) {
    if (!markdown || typeof markdown !== 'string') {
        return { headings: [], links: [], images: [] };
    }

    const headings = [];
    const links = [];
    const images = [];

    // Extract headings
    const headingRegex = /^(#{1,6})\s+(.+)$/gm;
    let match;
    while ((match = headingRegex.exec(markdown)) !== null) {
        headings.push({
            level: match[1].length,
            text: match[2].trim(),
            line: markdown.substring(0, match.index).split('\n').length
        });
    }

    // Extract links
    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    while ((match = linkRegex.exec(markdown)) !== null) {
        links.push({
            text: match[1],
            url: match[2],
            position: match.index
        });
    }

    // Extract images
    const imageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
    while ((match = imageRegex.exec(markdown)) !== null) {
        images.push({
            alt: match[1],
            url: match[2],
            position: match.index
        });
    }

    return { headings, links, images };
}

/**
 * Generate table of contents from markdown
 * @param {string} markdown - Markdown text
 * @param {Object} options - Options (maxLevel, numbered)
 * @returns {string} Markdown TOC
 */
function generateTOC(markdown, options = {}) {
    const { maxLevel = 6, numbered = false } = options;
    const metadata = extractMetadata(markdown);
    
    const tocItems = metadata.headings
        .filter(h => h.level <= maxLevel)
        .map((h, i) => {
            const indent = '  '.repeat(h.level - 1);
            const anchor = h.text.toLowerCase()
                .replace(/[^\w\s-]/g, '')
                .replace(/\s+/g, '-');
            const number = numbered ? `${i + 1}. ` : '- ';
            return `${indent}${number}[${h.text}](#${anchor})`;
        });

    return tocItems.join('\n');
}

/**
 * Convert HTML to markdown (basic conversion)
 * @param {string} html - HTML text
 * @returns {string} Markdown output
 */
function htmlToMarkdown(html) {
    if (!html || typeof html !== 'string') {
        return '';
    }

    let md = html;

    // Headers
    for (let i = 1; i <= 6; i++) {
        const regex = new RegExp(`<h${i}[^>]*>(.*?)</h${i}>`, 'gi');
        md = md.replace(regex, (match, content) => {
            return `${'#'.repeat(i)} ${content.trim()}\n\n`;
        });
    }

    // Paragraphs
    md = md.replace(/<p[^>]*>(.*?)<\/p>/gis, '$1\n\n');

    // Links
    md = md.replace(/<a[^>]*href="([^"]*)"[^>]*>(.*?)<\/a>/gi, '[$2]($1)');

    // Images
    md = md.replace(/<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*\/?>/gi, '![$2]($1)');
    md = md.replace(/<img[^>]*alt="([^"]*)"[^>]*src="([^"]*)"[^>]*\/?>/gi, '![$1]($2)');

    // Bold
    md = md.replace(/<(strong|b)[^>]*>(.*?)<\/(strong|b)>/gi, '**$2**');

    // Italic
    md = md.replace(/<(em|i)[^>]*>(.*?)<\/(em|i)>/gi, '*$2*');

    // Strikethrough
    md = md.replace(/<(del|s)[^>]*>(.*?)<\/(del|s)>/gi, '~~$2~~');

    // Code blocks
    md = md.replace(/<pre><code[^>]*>(.*?)<\/code><\/pre>/gis, '```\n$1\n```');
    md = md.replace(/<code>(.*?)<\/code>/gi, '`$1`');

    // Lists
    md = md.replace(/<li[^>]*>(.*?)<\/li>/gi, '- $1\n');
    md = md.replace(/<ul[^>]*>(.*?)<\/ul>/gis, '$1\n');
    md = md.replace(/<ol[^>]*>(.*?)<\/ol>/gis, '$1\n');

    // Blockquotes
    md = md.replace(/<blockquote[^>]*>(.*?)<\/blockquote>/gis, '> $1\n\n');

    // Horizontal rules
    md = md.replace(/<hr\s*\/?>/gi, '\n---\n\n');

    // Line breaks
    md = md.replace(/<br\s*\/?>/gi, '\n');

    // Remove remaining HTML tags
    md = md.replace(/<[^>]+>/g, '');

    // Clean up whitespace
    md = md.replace(/\n{3,}/g, '\n\n');
    md = md.trim();

    return md;
}

/**
 * Count words in markdown (excluding syntax)
 * @param {string} markdown - Markdown text
 * @returns {number} Word count
 */
function countWords(markdown) {
    if (!markdown || typeof markdown !== 'string') {
        return 0;
    }

    // Remove code blocks
    let text = markdown.replace(/```[\s\S]*?```/g, '');
    text = text.replace(/`[^`]+`/g, '');

    // Remove markdown syntax
    text = text.replace(/[#*_~\[\]()]/g, '');
    text = text.replace(/[-=]{3,}/g, '');

    // Count words
    const words = text.trim().split(/\s+/).filter(w => w.length > 0);
    return words.length;
}

/**
 * Estimate reading time
 * @param {string} markdown - Markdown text
 * @param {number} wpm - Words per minute (default 200)
 * @returns {Object} Reading time info
 */
function estimateReadingTime(markdown, wpm = 200) {
    const words = countWords(markdown);
    const minutes = Math.ceil(words / wpm);
    return {
        words,
        minutes,
        text: `${minutes} min read`
    };
}

/**
 * Strip markdown formatting
 * @param {string} markdown - Markdown text
 * @returns {string} Plain text
 */
function stripMarkdown(markdown) {
    if (!markdown || typeof markdown !== 'string') {
        return '';
    }

    let text = markdown;

    // Remove code blocks
    text = text.replace(/```[\s\S]*?```/g, '');
    text = text.replace(/`[^`]+`/g, '');

    // Remove images
    text = text.replace(/!\[([^\]]*)\]\([^)]+\)/g, '');

    // Remove links but keep text
    text = text.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');

    // Remove headers
    text = text.replace(/^#+\s+/gm, '');

    // Remove emphasis
    text = text.replace(/[*_]{1,3}([^*_]+)[*_]{1,3}/g, '$1');

    // Remove strikethrough
    text = text.replace(/~~(.+?)~~/g, '$1');

    // Remove horizontal rules
    text = text.replace(/^[-*_]{3,}$/gm, '');

    // Remove blockquote markers
    text = text.replace(/^>\s+/gm, '');

    // Remove list markers
    text = text.replace(/^[-*+]\s+/gm, '');
    text = text.replace(/^\d+\.\s+/gm, '');

    // Clean up
    text = text.replace(/\n{3,}/g, '\n\n');
    return text.trim();
}

// Export functions
module.exports = {
    MarkdownParser,
    parse: (markdown, options) => new MarkdownParser(options).parse(markdown),
    extractMetadata,
    generateTOC,
    htmlToMarkdown,
    countWords,
    estimateReadingTime,
    stripMarkdown
};