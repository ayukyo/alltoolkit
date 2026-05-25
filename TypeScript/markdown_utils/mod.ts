/**
 * Markdown Utilities - Zero-dependency Markdown parsing and processing toolkit
 * 
 * Features:
 * - Parse Markdown to structured AST
 * - Extract headings with hierarchy
 * - Extract links and images
 * - Generate Table of Contents (TOC)
 * - Convert Markdown to plain text
 * - Extract and highlight code blocks
 * - Calculate word count and reading time
 * - Slugify headings for anchor links
 * 
 * @module markdown_utils
 * @version 1.0.0
 */

// ============================================================================
// Types and Interfaces
// ============================================================================

export interface MarkdownNode {
  type: string;
  content?: string;
  children?: MarkdownNode[];
  level?: number;
  href?: string;
  title?: string;
  alt?: string;
  language?: string;
  code?: string;
  ordered?: boolean;
  items?: string[];
  text?: string;
  depth?: number;
}

export interface Heading {
  level: number;
  text: string;
  slug: string;
  line: number;
}

export interface Link {
  text: string;
  href: string;
  title?: string;
  line: number;
}

export interface Image {
  alt: string;
  src: string;
  title?: string;
  line: number;
}

export interface CodeBlock {
  language: string;
  code: string;
  line: number;
  isInline: boolean;
}

export interface TableOfContents {
  level: number;
  text: string;
  slug: string;
  children: TableOfContents[];
}

export interface MarkdownStats {
  characters: number;
  words: number;
  lines: number;
  paragraphs: number;
  codeBlocks: number;
  images: number;
  links: number;
  headings: number;
  readingTimeMinutes: number;
}

export interface ParseOptions {
  parseFrontMatter?: boolean;
  extractCodeBlocks?: boolean;
  maxHeadingDepth?: number;
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Slugify a string for use as anchor link
 * @param text - Text to slugify
 * @returns URL-safe slug
 */
export function slugify(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\w\u4e00-\u9fa5\s-]/g, '') // Keep alphanumeric, Chinese, spaces, hyphens
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}

/**
 * Escape HTML special characters
 * @param text - Text to escape
 * @returns Escaped text
 */
export function escapeHtml(text: string): string {
  const htmlEntities: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  };
  return text.replace(/[&<>"']/g, (char) => htmlEntities[char] || char);
}

/**
 * Unescape HTML entities
 * @param text - Text with HTML entities
 * @returns Unescaped text
 */
export function unescapeHtml(text: string): string {
  const htmlEntities: Record<string, string> = {
    '&amp;': '&',
    '&lt;': '<',
    '&gt;': '>',
    '&quot;': '"',
    '&#39;': "'",
    '&#x27;': "'",
    '&#x2F;': '/',
    '&nbsp;': ' ',
  };
  return text.replace(/&(?:amp|lt|gt|quot|#39|#x27|#x2F|nbsp);/g, 
    (entity) => htmlEntities[entity] || entity);
}

/**
 * Count words in text (supports Chinese and English)
 * @param text - Text to count
 * @returns Word count
 */
export function countWords(text: string): number {
  // Count Chinese characters
  const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
  // Count English words and numbers
  const englishAndNumbers = (text.match(/[a-zA-Z0-9]+/g) || []).length;
  return chineseChars + englishAndNumbers;
}

/**
 * Calculate reading time in minutes
 * @param wordCount - Number of words
 * @param wordsPerMinute - Reading speed (default: 200 for Chinese, 250 for English)
 * @returns Reading time in minutes
 */
export function calculateReadingTime(wordCount: number, wordsPerMinute: number = 225): number {
  return Math.max(1, Math.ceil(wordCount / wordsPerMinute));
}

// ============================================================================
// Extraction Functions
// ============================================================================

/**
 * Extract all headings from Markdown text
 * @param markdown - Markdown text
 * @returns Array of Heading objects
 */
export function extractHeadings(markdown: string): Heading[] {
  const headings: Heading[] = [];
  const lines = markdown.split('\n');
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // ATX-style headings (# Heading)
    const atxMatch = line.match(/^(#{1,6})\s+(.+?)(?:\s+#+)?$/);
    if (atxMatch) {
      headings.push({
        level: atxMatch[1].length,
        text: atxMatch[2].trim(),
        slug: slugify(atxMatch[2].trim()),
        line: i + 1,
      });
      continue;
    }
    
    // Setext-style headings (underlined with = or -)
    if (i < lines.length - 1 && line.trim()) {
      const nextLine = lines[i + 1];
      if (/^=+$/.test(nextLine.trim())) {
        headings.push({
          level: 1,
          text: line.trim(),
          slug: slugify(line.trim()),
          line: i + 1,
        });
      } else if (/^-+$/.test(nextLine.trim())) {
        headings.push({
          level: 2,
          text: line.trim(),
          slug: slugify(line.trim()),
          line: i + 1,
        });
      }
    }
  }
  
  return headings;
}

/**
 * Extract all links from Markdown text
 * @param markdown - Markdown text
 * @returns Array of Link objects
 */
export function extractLinks(markdown: string): Link[] {
  const links: Link[] = [];
  const lines = markdown.split('\n');
  
  // Inline link pattern: [text](url "title")
  const inlineLinkRegex = /\[([^\]]*)\]\(([^)]+?)(?:\s+"([^"]+)")?\)/g;
  // Reference link pattern: [text][ref] or [ref] (not inline links)
  const refLinkRegex = /\[([^\]]*)\]\[([^\]]+)\]/g;
  // Shortcut reference link pattern: [ref] (without second bracket)
  const shortcutRefRegex = /\[([^\]]+)\](?!\[|\()/g;
  // Reference definition pattern: [ref]: url "title"
  const refDefRegex = /^\s*\[([^\]]+)\]:\s*(.+?)(?:\s+"([^"]+)")?\s*$/gm;
  
  // Build reference definitions map
  const refDefs: Map<string, { href: string; title?: string }> = new Map();
  let refMatch;
  while ((refMatch = refDefRegex.exec(markdown)) !== null) {
    refDefs.set(refMatch[1].toLowerCase(), {
      href: refMatch[2].trim(),
      title: refMatch[3],
    });
  }
  
  // Extract inline links
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    let match;
    const inlineRegexCopy = new RegExp(inlineLinkRegex.source, 'g');
    
    while ((match = inlineRegexCopy.exec(line)) !== null) {
      // Skip if it's an image (preceded by !)
      if (match.index > 0 && line[match.index - 1] === '!') continue;
      
      links.push({
        text: match[1],
        href: match[2],
        title: match[3],
        line: i + 1,
      });
    }
  }
  
  // Extract reference links (with explicit ref)
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    let match;
    const refRegexCopy = new RegExp(refLinkRegex.source, 'g');
    
    while ((match = refRegexCopy.exec(line)) !== null) {
      // Skip if it's an image (preceded by !)
      if (match.index > 0 && line[match.index - 1] === '!') continue;
      
      const text = match[1];
      const ref = match[2].toLowerCase();
      
      const def = refDefs.get(ref);
      if (def) {
        links.push({
          text: text,
          href: def.href,
          title: def.title,
          line: i + 1,
        });
      }
    }
  }
  
  // Extract shortcut reference links
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    let match;
    const shortcutRegexCopy = new RegExp(shortcutRefRegex.source, 'g');
    
    // Skip reference definition lines
    if (/^\s*\[([^\]]+)\]:/.test(line)) continue;
    
    while ((match = shortcutRegexCopy.exec(line)) !== null) {
      // Skip if it's an image (preceded by !)
      if (match.index > 0 && line[match.index - 1] === '!') continue;
      
      // Skip if preceded by [text] (part of [text][ref] format)
      // Check if there's a closing bracket immediately before
      if (match.index > 0 && line[match.index - 1] === ']') continue;
      
      const ref = match[1].toLowerCase();
      const def = refDefs.get(ref);
      if (def) {
        links.push({
          text: match[1],
          href: def.href,
          title: def.title,
          line: i + 1,
        });
      }
    }
  }
  
  return links;
}

/**
 * Extract all images from Markdown text
 * @param markdown - Markdown text
 * @returns Array of Image objects
 */
export function extractImages(markdown: string): Image[] {
  const images: Image[] = [];
  const lines = markdown.split('\n');
  
  // Inline image pattern: ![alt](src "title")
  const inlineImageRegex = /!\[([^\]]*)\]\(([^)]+?)(?:\s+"([^"]+)")?\)/g;
  // Reference image pattern: ![alt][ref]
  const refImageRegex = /!\[([^\]]*)\]\[([^\]]*)\]/g;
  // Reference definition pattern
  const refDefRegex = /^\s*\[([^\]]+)\]:\s*(.+?)(?:\s+"([^"]+)")?\s*$/gm;
  
  // Build reference definitions map
  const refDefs: Map<string, { href: string; title?: string }> = new Map();
  let refMatch;
  while ((refMatch = refDefRegex.exec(markdown)) !== null) {
    refDefs.set(refMatch[1].toLowerCase(), {
      href: refMatch[2].trim(),
      title: refMatch[3],
    });
  }
  
  // Extract inline images
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    let match;
    
    while ((match = inlineImageRegex.exec(line)) !== null) {
      images.push({
        alt: match[1],
        src: match[2],
        title: match[3],
        line: i + 1,
      });
    }
  }
  
  // Extract reference images
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    let match;
    
    while ((match = refImageRegex.exec(line)) !== null) {
      const alt = match[1];
      const ref = (match[2] || match[1]).toLowerCase();
      const def = refDefs.get(ref);
      
      if (def) {
        images.push({
          alt: alt,
          src: def.href,
          title: def.title,
          line: i + 1,
        });
      }
    }
  }
  
  return images;
}

/**
 * Extract all code blocks from Markdown text
 * @param markdown - Markdown text
 * @returns Array of CodeBlock objects
 */
export function extractCodeBlocks(markdown: string): CodeBlock[] {
  const codeBlocks: CodeBlock[] = [];
  const lines = markdown.split('\n');
  
  // Fenced code blocks (``` or ~~~)
  let inCodeBlock = false;
  let codeBlockStart = 0;
  let codeBlockLang = '';
  let codeContent: string[] = [];
  let fenceChar = '';
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    if (!inCodeBlock) {
      // Check for fence start
      const fenceMatch = line.match(/^(`{3,}|~{3,})\s*(.*)$/);
      if (fenceMatch) {
        inCodeBlock = true;
        codeBlockStart = i + 1;
        fenceChar = fenceMatch[1][0];
        codeBlockLang = fenceMatch[2].trim();
        codeContent = [];
        continue;
      }
      
      // Inline code (single backticks)
      const inlineMatches = line.matchAll(/`([^`]+)`/g);
      for (const match of inlineMatches) {
        codeBlocks.push({
          language: '',
          code: match[1],
          line: i + 1,
          isInline: true,
        });
      }
    } else {
      // Check for fence end
      if (line.startsWith(fenceChar.repeat(3)) && !line.match(/^[`~]{4,}/)) {
        codeBlocks.push({
          language: codeBlockLang,
          code: codeContent.join('\n'),
          line: codeBlockStart,
          isInline: false,
        });
        inCodeBlock = false;
        codeBlockLang = '';
        codeContent = [];
      } else {
        codeContent.push(line);
      }
    }
  }
  
  // Indented code blocks (4 spaces or tab)
  let inIndentedBlock = false;
  let indentedStart = 0;
  let indentedContent: string[] = [];
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    if (line.startsWith('    ') || line.startsWith('\t')) {
      if (!inIndentedBlock) {
        inIndentedBlock = true;
        indentedStart = i + 1;
        indentedContent = [];
      }
      indentedContent.push(line.slice(line.match(/^(\s+)/)![0].length));
    } else if (inIndentedBlock && line.trim() === '') {
      indentedContent.push('');
    } else if (inIndentedBlock) {
      codeBlocks.push({
        language: '',
        code: indentedContent.join('\n'),
        line: indentedStart,
        isInline: false,
      });
      inIndentedBlock = false;
    }
  }
  
  // Handle trailing indented block
  if (inIndentedBlock && indentedContent.length > 0) {
    codeBlocks.push({
      language: '',
      code: indentedContent.join('\n'),
      line: indentedStart,
      isInline: false,
    });
  }
  
  return codeBlocks;
}

// ============================================================================
// Table of Contents Generation
// ============================================================================

/**
 * Generate a Table of Contents from Markdown headings
 * @param markdown - Markdown text
 * @param maxDepth - Maximum heading depth to include (default: 6)
 * @returns Table of Contents structure
 */
export function generateTOC(markdown: string, maxDepth: number = 6): TableOfContents[] {
  const headings = extractHeadings(markdown).filter(h => h.level <= maxDepth);
  const root: TableOfContents[] = [];
  const stack: { level: number; node: TableOfContents }[] = [];
  
  for (const heading of headings) {
    const node: TableOfContents = {
      level: heading.level,
      text: heading.text,
      slug: heading.slug,
      children: [],
    };
    
    // Find the appropriate parent
    while (stack.length > 0 && stack[stack.length - 1].level >= heading.level) {
      stack.pop();
    }
    
    if (stack.length === 0) {
      root.push(node);
    } else {
      stack[stack.length - 1].node.children.push(node);
    }
    
    stack.push({ level: heading.level, node });
  }
  
  return root;
}

/**
 * Generate TOC as Markdown string
 * @param toc - Table of Contents structure
 * @param indent - Indentation string (default: '  ')
 * @returns Markdown-formatted TOC
 */
export function tocToMarkdown(toc: TableOfContents[], indent: string = '  '): string {
  const lines: string[] = [];
  
  function render(nodes: TableOfContents[], depth: number): void {
    for (const node of nodes) {
      const prefix = indent.repeat(depth);
      lines.push(`${prefix}- [${node.text}](#${node.slug})`);
      if (node.children.length > 0) {
        render(node.children, depth + 1);
      }
    }
  }
  
  render(toc, 0);
  return lines.join('\n');
}

// ============================================================================
// Markdown to Plain Text Conversion
// ============================================================================

/**
 * Convert Markdown to plain text
 * @param markdown - Markdown text
 * @returns Plain text without Markdown formatting
 */
export function toPlainText(markdown: string): string {
  let text = markdown;
  
  // Remove front matter
  text = text.replace(/^---\n[\s\S]*?\n---\n/, '');
  
  // Remove code blocks (fenced)
  text = text.replace(/```[\s\S]*?```/g, '');
  text = text.replace(/~~~[\s\S]*?~~~/g, '');
  
  // Remove inline code
  text = text.replace(/`[^`]+`/g, '');
  
  // Remove images
  text = text.replace(/!\[([^\]]*)\]\([^)]+\)/g, '');
  text = text.replace(/!\[([^\]]*)\]\[[^\]]*\]/g, '');
  
  // Convert links to just text
  text = text.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
  text = text.replace(/\[([^\]]+)\]\[[^\]]*\]/g, '$1');
  
  // Remove headings markers
  text = text.replace(/^#{1,6}\s+/gm, '');
  
  // Remove emphasis markers
  text = text.replace(/[*_]{1,3}([^*_]+)[*_]{1,3}/g, '$1');
  
  // Remove strikethrough
  text = text.replace(/~~([^~]+)~~/g, '$1');
  
  // Remove blockquote markers
  text = text.replace(/^>\s+/gm, '');
  
  // Remove list markers
  text = text.replace(/^\s*[-*+]\s+/gm, '');
  text = text.replace(/^\s*\d+\.\s+/gm, '');
  
  // Remove horizontal rules
  text = text.replace(/^[-*_]{3,}$/gm, '');
  
  // Remove HTML tags
  text = text.replace(/<[^>]+>/g, '');
  
  // Clean up whitespace
  text = text.replace(/\n{3,}/g, '\n\n');
  text = text.trim();
  
  return text;
}

// ============================================================================
// Markdown Statistics
// ============================================================================

/**
 * Calculate statistics for Markdown text
 * @param markdown - Markdown text
 * @returns Markdown statistics
 */
export function calculateStats(markdown: string): MarkdownStats {
  const plainText = toPlainText(markdown);
  const codeBlocks = extractCodeBlocks(markdown);
  const links = extractLinks(markdown);
  const images = extractImages(markdown);
  const headings = extractHeadings(markdown);
  
  const lines = markdown.split('\n');
  const paragraphs = plainText.split(/\n\s*\n/).filter(p => p.trim().length > 0).length;
  const wordCount = countWords(plainText);
  
  return {
    characters: plainText.length,
    words: wordCount,
    lines: lines.length,
    paragraphs: paragraphs,
    codeBlocks: codeBlocks.filter(cb => !cb.isInline).length,
    images: images.length,
    links: links.length,
    headings: headings.length,
    readingTimeMinutes: calculateReadingTime(wordCount),
  };
}

// ============================================================================
// Front Matter Parsing
// ============================================================================

export interface FrontMatter {
  data: Record<string, unknown>;
  content: string;
  format: 'yaml' | 'toml' | 'json' | 'none';
}

/**
 * Parse front matter from Markdown
 * @param markdown - Markdown text
 * @returns Front matter data and remaining content
 */
export function parseFrontMatter(markdown: string): FrontMatter {
  // YAML front matter (---)
  const yamlMatch = markdown.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (yamlMatch) {
    const data = parseSimpleYaml(yamlMatch[1]);
    return { data, content: yamlMatch[2], format: 'yaml' };
  }
  
  // TOML front matter (+++)
  const tomlMatch = markdown.match(/^\+\+\+\n([\s\S]*?)\n\+\+\+\n([\s\S]*)$/);
  if (tomlMatch) {
    const data = parseSimpleToml(tomlMatch[1]);
    return { data, content: tomlMatch[2], format: 'toml' };
  }
  
  // JSON front matter
  const jsonMatch = markdown.match(/^\{\n([\s\S]*?)\n\}\n([\s\S]*)$/);
  if (jsonMatch) {
    try {
      const data = JSON.parse('{' + jsonMatch[1] + '}');
      return { data, content: jsonMatch[2], format: 'json' };
    } catch {
      // Fall through
    }
  }
  
  return { data: {}, content: markdown, format: 'none' };
}

/**
 * Simple YAML parser for front matter (no external dependencies)
 */
function parseSimpleYaml(yaml: string): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  const lines = yaml.split('\n');
  
  for (const line of lines) {
    const match = line.match(/^(\s*)([^:\s]+):\s*(.*)$/);
    if (match) {
      const [, indent, key, value] = match;
      
      if (indent.length === 0) {
        // Top-level key
        if (value === '' || value === '~' || value === 'null') {
          result[key] = null;
        } else if (value === 'true') {
          result[key] = true;
        } else if (value === 'false') {
          result[key] = false;
        } else if (/^\d+$/.test(value)) {
          result[key] = parseInt(value, 10);
        } else if (/^\d+\.\d+$/.test(value)) {
          result[key] = parseFloat(value);
        } else if (/^["'](.*)["']$/.test(value)) {
          result[key] = value.slice(1, -1);
        } else {
          result[key] = value;
        }
      }
    }
  }
  
  return result;
}

/**
 * Simple TOML parser for front matter (no external dependencies)
 */
function parseSimpleToml(toml: string): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  const lines = toml.split('\n');
  
  for (const line of lines) {
    const match = line.match(/^([^=]+)=(.*)$/);
    if (match) {
      const key = match[1].trim();
      let value = match[2].trim();
      
      // Remove comments
      const commentIndex = value.indexOf('#');
      if (commentIndex > 0) {
        value = value.slice(0, commentIndex).trim();
      }
      
      // Parse value
      if (/^["'](.*)["']$/.test(value)) {
        result[key] = value.slice(1, -1);
      } else if (value === 'true') {
        result[key] = true;
      } else if (value === 'false') {
        result[key] = false;
      } else if (/^\d+$/.test(value)) {
        result[key] = parseInt(value, 10);
      } else if (/^\d+\.\d+$/.test(value)) {
        result[key] = parseFloat(value);
      } else {
        result[key] = value;
      }
    }
  }
  
  return result;
}

// ============================================================================
// Markdown Validation
// ============================================================================

export interface ValidationError {
  line: number;
  column: number;
  message: string;
  severity: 'error' | 'warning';
}

/**
 * Validate Markdown for common issues
 * @param markdown - Markdown text
 * @returns Array of validation errors/warnings
 */
export function validate(markdown: string): ValidationError[] {
  const errors: ValidationError[] = [];
  const lines = markdown.split('\n');
  
  let inCodeBlock = false;
  let fenceChar = '';
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;
    
    // Track code blocks
    const fenceMatch = line.match(/^(`{3,}|~{3,})/);
    if (fenceMatch) {
      if (!inCodeBlock) {
        inCodeBlock = true;
        fenceChar = fenceMatch[1][0];
      } else if (line.startsWith(fenceChar.repeat(3))) {
        inCodeBlock = false;
      }
      continue;
    }
    
    if (inCodeBlock) continue;
    
    // Check for missing space after #
    const headingMatch = line.match(/^(#{1,6})([^#\s])/);
    if (headingMatch) {
      errors.push({
        line: lineNum,
        column: headingMatch[1].length + 1,
        message: `Missing space after ${headingMatch[1]}`,
        severity: 'warning',
      });
    }
    
    // Check for empty links
    if (/\[\]\([^)]*\)/.test(line)) {
      errors.push({
        line: lineNum,
        column: line.indexOf('[](') + 1,
        message: 'Empty link text',
        severity: 'warning',
      });
    }
    
    // Check for empty images
    if (/!\[\]\([^)]*\)/.test(line)) {
      errors.push({
        line: lineNum,
        column: line.indexOf('![](') + 1,
        message: 'Empty image alt text',
        severity: 'warning',
      });
    }
    
    // Check for unclosed inline code
    const backtickCount = (line.match(/`/g) || []).length;
    if (backtickCount % 2 !== 0) {
      errors.push({
        line: lineNum,
        column: line.lastIndexOf('`') + 1,
        message: 'Unclosed inline code',
        severity: 'error',
      });
    }
    
    // Check for unclosed emphasis
    const asterisks = (line.match(/(?<!\*)\*(?!\*)/g) || []).length;
    const underscores = (line.match(/(?<!_)_(?!_)/g) || []).length;
    if (asterisks % 2 !== 0) {
      errors.push({
        line: lineNum,
        column: 1,
        message: 'Unbalanced emphasis markers (*)',
        severity: 'warning',
      });
    }
    if (underscores % 2 !== 0) {
      errors.push({
        line: lineNum,
        column: 1,
        message: 'Unbalanced emphasis markers (_)',
        severity: 'warning',
      });
    }
    
    // Check for very long lines
    if (line.length > 120) {
      errors.push({
        line: lineNum,
        column: 120,
        message: `Line too long (${line.length} characters)`,
        severity: 'warning',
      });
    }
    
    // Check for trailing whitespace
    if (/[ \t]+$/.test(line)) {
      errors.push({
        line: lineNum,
        column: line.trimEnd().length + 1,
        message: 'Trailing whitespace',
        severity: 'warning',
      });
    }
  }
  
  // Check for unclosed code block
  if (inCodeBlock) {
    errors.push({
      line: lines.length,
      column: 1,
      message: 'Unclosed code block',
      severity: 'error',
    });
  }
  
  return errors;
}

// ============================================================================
// HTML Rendering (Basic)
// ============================================================================

/**
 * Convert Markdown to HTML (basic implementation)
 * @param markdown - Markdown text
 * @returns HTML string
 */
export function toHtml(markdown: string): string {
  let html = markdown;
  
  // Remove front matter
  html = html.replace(/^---\n[\s\S]*?\n---\n/, '');
  
  // Code blocks (must be first to prevent inner processing)
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
    const langClass = lang ? ` class="language-${lang}"` : '';
    return `<pre><code${langClass}>${escapeHtml(code)}</code></pre>`;
  });
  
  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
  
  // Headings
  html = html.replace(/^######\s+(.+)$/gm, '<h6>$1</h6>');
  html = html.replace(/^#####\s+(.+)$/gm, '<h5>$1</h5>');
  html = html.replace(/^####\s+(.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^###\s+(.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^##\s+(.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^#\s+(.+)$/gm, '<h1>$1</h1>');
  
  // Bold and italic (order matters)
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/___(.+?)___/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/__(.+?)__/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
  html = html.replace(/_(.+?)_/g, '<em>$1</em>');
  
  // Strikethrough
  html = html.replace(/~~(.+?)~~/g, '<del>$1</del>');
  
  // Images
  html = html.replace(/!\[([^\]]*)\]\(([^)]+?)(?:\s+"([^"]+)")?\)/g, 
    (_, alt, src, title) => `<img src="${src}" alt="${alt}"${title ? ` title="${title}"` : ''}>`);
  
  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+?)(?:\s+"([^"]+)")?\)/g, 
    (_, text, href, title) => `<a href="${href}"${title ? ` title="${title}"` : ''}>${text}</a>`);
  
  // Horizontal rules
  html = html.replace(/^[-*_]{3,}$/gm, '<hr>');
  
  // Blockquotes
  html = html.replace(/^>\s+(.+)$/gm, '<blockquote>$1</blockquote>');
  
  // Unordered lists
  html = html.replace(/^[-*+]\s+(.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');
  
  // Ordered lists
  html = html.replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');
  
  // Paragraphs
  html = html.replace(/\n\n/g, '</p><p>');
  html = '<p>' + html + '</p>';
  
  // Clean up empty paragraphs
  html = html.replace(/<p>\s*<\/p>/g, '');
  html = html.replace(/<p>\s*(<h[1-6]>)/g, '$1');
  html = html.replace(/(<\/h[1-6]>)\s*<\/p>/g, '$1');
  html = html.replace(/<p>\s*(<pre>)/g, '$1');
  html = html.replace(/(<\/pre>)\s*<\/p>/g, '$1');
  html = html.replace(/<p>\s*(<ul>)/g, '$1');
  html = html.replace(/(<\/ul>)\s*<\/p>/g, '$1');
  html = html.replace(/<p>\s*(<blockquote>)/g, '$1');
  html = html.replace(/(<\/blockquote>)\s*<\/p>/g, '$1');
  html = html.replace(/<p>\s*(<hr>)/g, '$1');
  html = html.replace(/(<hr>)\s*<\/p>/g, '$1');
  
  return html;
}

// ============================================================================
// Export All
// ============================================================================

export default {
  // Utility functions
  slugify,
  escapeHtml,
  unescapeHtml,
  countWords,
  calculateReadingTime,
  
  // Extraction functions
  extractHeadings,
  extractLinks,
  extractImages,
  extractCodeBlocks,
  
  // TOC functions
  generateTOC,
  tocToMarkdown,
  
  // Conversion functions
  toPlainText,
  toHtml,
  
  // Statistics
  calculateStats,
  
  // Front matter
  parseFrontMatter,
  
  // Validation
  validate,
};