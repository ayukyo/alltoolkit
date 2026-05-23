#!/usr/bin/env ruby
# frozen_string_literal: true

module AllToolkit
  module MarkdownUtils
    # Markdown element types
    ELEMENT_TYPES = %i[heading paragraph code_block blockquote list link image table hr text].freeze

    # Heading levels
    HEADING_LEVELS = (1..6).freeze

    # List types
    LIST_TYPES = %i[ordered unordered].freeze

    # Regex patterns for Markdown elements
    PATTERNS = {
      heading: /^(#{1,6})\s+(.+)$/,
      heading_alt: /^([^\n]+)\n([=-]+)$/,
      code_block: /^```(\w*)\n([\s\S]*?)```$/,
      inline_code: /`([^`]+)`/,
      bold: /\*\*([^*]+)\*\*/,
      italic: /[*_]([^*_]+)[*_]/,
      bold_italic: /\*\*\*([^*]+)\*\*\*/,
      strikethrough: /~~([^~]+)~~/,
      link: /\[([^\]]+)\]\(([^)]+)\)/,
      image: /!\[([^\]]*)\]\(([^)]+)\)/,
      blockquote: /^>\s+(.+)$/,
      unordered_list: /^[\*\-\+]\s+(.+)$/,
      ordered_list: /^(\d+)\.\s+(.+)$/,
      hr: /^(-{3,}|\*{3,}|_{3,})$/,
      table: /^\|(.+)\|$/,
      table_separator: /^\|[\s\-:|]+\|$/
    }.freeze

    class << self
      # Convert Markdown to HTML
      def to_html(markdown)
        return '' if markdown.nil? || markdown.empty?

        html = markdown.dup
        html = process_code_blocks(html)
        html = process_tables(html)
        html = process_headings(html)
        html = process_lists(html)
        html = process_blockquotes(html)
        html = process_horizontal_rules(html)
        html = process_paragraphs(html)
        html = process_inline_elements(html)
        html
      end

      # Extract all headings from Markdown
      # @param markdown [String] The Markdown content
      # @return [Array<Hash>] Array of heading info with :level, :text, :anchor
      def extract_headings(markdown)
        return [] if markdown.nil? || markdown.empty?

        headings = []
        lines = markdown.split("\n")
        i = 0

        while i < lines.length
          line = lines[i]
          
          # Standard heading format: # Heading
          if (match = line.match(/^(#{1,6})\s+(.+)$/))
            level = match[1].length
            text = match[2].strip
            headings << {
              level: level,
              text: text,
              anchor: generate_anchor(text)
            }
          # Alternative format: Heading\n=== or Heading\n---
          elsif i + 1 < lines.length && (alt_match = lines[i + 1].match(/^([=-]+)$/))
            level = alt_match[1].start_with?('=') ? 1 : 2
            text = line.strip
            headings << {
              level: level,
              text: text,
              anchor: generate_anchor(text)
            }
            i += 1 # Skip the next line
          end
          i += 1
        end

        headings
      end

      # Generate Table of Contents from Markdown
      # @param markdown [String] The Markdown content
      # @param max_level [Integer] Maximum heading level to include (1-6)
      # @return [String] Markdown formatted TOC
      def generate_toc(markdown, max_level = 6)
        headings = extract_headings(markdown)
        return '' if headings.empty?

        filtered = headings.select { |h| h[:level] <= max_level }
        return '' if filtered.empty?

        toc_lines = ['# Table of Contents', '']
        
        filtered.each do |heading|
          indent = '  ' * (heading[:level] - 1)
          toc_lines << "#{indent}- [#{heading[:text]}](##{heading[:anchor]})"
        end

        toc_lines << ''
        toc_lines.join("\n")
      end

      # Extract all links from Markdown
      # @param markdown [String] The Markdown content
      # @return [Array<Hash>] Array of link info with :text, :url
      def extract_links(markdown)
        return [] if markdown.nil? || markdown.empty?

        links = []
        # Don't match images (which start with !)
        markdown.scan(/(?<!\!)\[([^\]]+)\]\(([^)]+)\)/) do |text, url|
          links << { text: text, url: url }
        end

        # Also extract reference-style links
        markdown.scan(/^\[([^\]]+)\]:\s*(.+)$/) do |text, url|
          links << { text: text, url: url.strip, type: :reference }
        end

        links
      end

      # Extract all images from Markdown
      # @param markdown [String] The Markdown content
      # @return [Array<Hash>] Array of image info with :alt, :url, :title
      def extract_images(markdown)
        return [] if markdown.nil? || markdown.empty?

        images = []
        markdown.scan(/!\[([^\]]*)\]\(([^)]+)(?:\s+"([^"]+)")?\)/) do |alt, url, title|
          images << { alt: alt, url: url, title: title }
        end

        # Also extract reference-style images
        markdown.scan(/^!\[([^\]]*)\]:\s*(.+)$/) do |alt, url|
          images << { alt: alt, url: url.strip, type: :reference }
        end

        images
      end

      # Extract all code blocks from Markdown
      # @param markdown [String] The Markdown content
      # @return [Array<Hash>] Array of code block info with :language, :code
      def extract_code_blocks(markdown)
        return [] if markdown.nil? || markdown.empty?

        code_blocks = []
        markdown.scan(/```(\w*)\n([\s\S]*?)```/) do |language, code|
          code_blocks << { 
            language: language.empty? ? nil : language, 
            code: code.chomp 
          }
        end

        # Also extract inline code
        markdown.scan(/`([^`]+)`/) do |code|
          code_blocks << { language: nil, code: code, inline: true }
        end

        code_blocks
      end

      # Extract all tables from Markdown
      # @param markdown [String] The Markdown content
      # @return [Array<Hash>] Array of table info with :headers, :rows, :alignments
      def extract_tables(markdown)
        return [] if markdown.nil? || markdown.empty?

        tables = []
        lines = markdown.split("\n")
        i = 0

        while i < lines.length
          line = lines[i]
          
          # Check if line is a table row
          if line.match?(/^\|(.+)\|$/)
            headers = parse_table_row(line)
            i += 1
            
            # Check for separator/alignment row
            if i < lines.length && lines[i].match?(/^\|[\s\-:|]+\|$/)
              alignments = parse_table_alignment(lines[i])
              i += 1
            else
              alignments = []
            end

            # Collect data rows
            rows = []
            while i < lines.length && lines[i].match?(/^\|(.+)\|$/)
              rows << parse_table_row(lines[i])
              i += 1
            end

            tables << {
              headers: headers,
              alignments: alignments,
              rows: rows
            }
          else
            i += 1
          end
        end

        tables
      end

      # Get statistics about the Markdown content
      # @param markdown [String] The Markdown content
      # @return [Hash] Statistics including character, word, line counts, etc.
      def stats(markdown)
        return empty_stats if markdown.nil? || markdown.empty?

        {
          characters: markdown.length,
          characters_no_spaces: markdown.gsub(/\s/, '').length,
          words: count_words(markdown),
          lines: markdown.split("\n").length,
          paragraphs: count_paragraphs(markdown),
          headings: extract_headings(markdown).length,
          links: extract_links(markdown).length,
          images: extract_images(markdown).length,
          code_blocks: markdown.scan(/```/).length / 2,
          tables: extract_tables(markdown).length,
          reading_time_minutes: (count_words(markdown) / 200.0).ceil
        }
      end

      # Strip all Markdown formatting to get plain text
      # @param markdown [String] The Markdown content
      # @return [String] Plain text without Markdown formatting
      def to_plain_text(markdown)
        return '' if markdown.nil? || markdown.empty?

        text = markdown.dup

        # Remove code blocks
        text.gsub!(/```[\s\S]*?```/, '')
        text.gsub!(/`[^`]+`/, '')

        # Remove images
        text.gsub!(/!\[[^\]]*\]\([^)]+\)/, '')
        text.gsub!(/!\[[^\]]*\]:\s*.+/, '')

        # Remove links but keep text
        text.gsub!(/\[([^\]]+)\]\([^)]+\)/, '\1')
        text.gsub!(/\[([^\]]+)\]:\s*.+/, '')

        # Remove formatting
        text.gsub!(/\*\*\*([^*]+)\*\*\*/, '\1')
        text.gsub!(/\*\*([^*]+)\*\*/, '\1')
        text.gsub!(/[*_]([^*_]+)[*_]/, '\1')
        text.gsub!(/~~([^~]+)~~/, '\1')

        # Remove headings markers
        text.gsub!(/^#{1,6}\s+/, '')
        text.gsub!(/^([^\n]+)\n[=-]+$/, '\1')

        # Remove blockquote markers
        text.gsub!(/^>\s+/, '')

        # Remove list markers
        text.gsub!(/^[\*\-\+]\s+/, '')
        text.gsub!(/^\d+\.\s+/, '')

        # Remove horizontal rules
        text.gsub!(/^[-*_]{3,}$/, '')

        # Remove table formatting
        text.gsub!(/\|/, ' ')
        text.gsub!(/^[\s\-:|]+$/, '')

        # Clean up whitespace
        text.gsub!(/\n{3,}/, "\n\n")
        text.strip

        text
      end

      # Check if content is valid Markdown
      # @param content [String] The content to check
      # @return [Boolean] True if content appears to be valid Markdown
      def valid_markdown?(content)
        return false if content.nil? || content.empty?

        # Basic validation checks
        has_text = content.strip.length > 0
        has_markdown_elements = content.match?(/[#*_`\[\]>|-]/)

        has_text && has_markdown_elements
      end

      # Highlight Markdown syntax with HTML spans
      # @param markdown [String] The Markdown content
      # @param theme [Hash] Color theme for highlighting
      # @return [String] HTML with syntax highlighting
      def highlight(markdown, theme: nil)
        return '' if markdown.nil? || markdown.empty?

        theme ||= default_highlight_theme
        html = escape_html(markdown)

        # Highlight code blocks
        html.gsub!(/```(\w*)\n/) { |m| "<span class=\"md-code-block\">```#{Regexp.last_match(1]}</span>\n" }
        html.gsub!(/```$/, '<span class="md-code-block">```</span>')

        # Highlight inline code
        html.gsub!(/`([^`]+)`/, '<span class="md-code">`\1`</span>')

        # Highlight headings
        html.gsub!(/^(#{1,6})(\s+.+)$/, '<span class="md-heading">\1</span>\2')

        # Highlight bold
        html.gsub!(/\*\*([^*]+)\*\*/, '<span class="md-bold">**\1**</span>')

        # Highlight italic
        html.gsub!(/[*_]([^*_]+)[*_]/, '<span class="md-italic">*\1*</span>')

        # Highlight links
        html.gsub!(/\[([^\]]+)\]\(([^)]+)\)/, '<span class="md-link">[\1](\2)</span>')

        # Highlight images
        html.gsub!(/!\[([^\]]*)\]\(([^)]+)\)/, '<span class="md-image">![\1](\2)</span>')

        html
      end

      # Convert plain text to Markdown
      # @param text [String] Plain text content
      # @param options [Hash] Conversion options
      # @return [String] Markdown formatted text
      def from_plain_text(text, options = {})
        return '' if text.nil? || text.empty?

        markdown = text.dup
        lines = markdown.split("\n")
        result = []

        lines.each do |line|
          line = line.strip
          
          if options[:auto_links]
            # Auto-detect URLs and convert to links
            line.gsub!(%r{(https?://[^\s]+)}, '[\1](\1)')
          end

          result << line
        end

        result.join("\n")
      end

      private

      def process_code_blocks(html)
        # Preserve code blocks from further processing
        html.gsub(/```(\w*)\n([\s\S]*?)```/) do
          lang = Regexp.last_match(1)
          code = Regexp.last_match(2)
          escaped_code = escape_html(code)
          "<pre><code#{lang.empty? ? '' : " class=\"language-#{lang}\""}>#{escaped_code}</code></pre>"
        end
      end

      def process_tables(html)
        lines = html.split("\n")
        result = []
        in_table = false
        table_lines = []

        lines.each do |line|
          if line.match?(/^\|(.+)\|$/)
            in_table = true
            table_lines << line
          elsif in_table && line.strip.empty?
            # End of table
            result << convert_table(table_lines) if table_lines.any? { |l| !l.match?(/^\|[\s\-:|]+\|$/) }
            result << ''
            in_table = false
            table_lines = []
            result << line
          else
            if in_table
              result << convert_table(table_lines) if table_lines.any? { |l| !l.match?(/^\|[\s\-:|]+\|$/) }
              in_table = false
              table_lines = []
            end
            result << line
          end
        end

        # Handle table at end of content
        if in_table && table_lines.any? { |l| !l.match?(/^\|[\s\-:|]+\|$/) }
          result << convert_table(table_lines)
        end

        result.join("\n")
      end

      def convert_table(lines)
        return '' if lines.empty?

        headers = parse_table_row(lines[0])
        alignments = lines[1] && lines[1].match?(/^\|[\s\-:|]+\|$/) ? parse_table_alignment(lines[1]) : []
        start_idx = alignments.empty? ? 1 : 2

        rows = lines[start_idx..-1].map { |l| parse_table_row(l) }

        html = ['<table>']
        html << '  <thead>'
        html << '    <tr>'
        headers.each_with_index do |cell, i|
          align = alignments[i] ? " style=\"text-align:#{alignments[i]}\"" : ''
          html << "      <th#{align}>#{process_inline_elements(cell.strip)}</th>"
        end
        html << '    </tr>'
        html << '  </thead>'
        html << '  <tbody>'
        
        rows.each do |row|
          html << '    <tr>'
          row.each_with_index do |cell, i|
            align = alignments[i] ? " style=\"text-align:#{alignments[i]}\"" : ''
            html << "      <td#{align}>#{process_inline_elements(cell.strip)}</td>"
          end
          html << '    </tr>'
        end

        html << '  </tbody>'
        html << '</table>'
        html.join("\n")
      end

      def parse_table_row(line)
        line.split('|').map(&:strip)[1..-1] || []
      end

      def parse_table_alignment(line)
        cells = line.split('|').map(&:strip)[1..-1] || []
        cells.map do |cell|
          if cell.match?(/^:-+:/)
            'center'
          elsif cell.match?(/^:-+/)
            'left'
          elsif cell.match?(/-+:$/)
            'right'
          else
            nil
          end
        end
      end

      def process_headings(html)
        lines = html.split("\n")
        result = []
        i = 0

        while i < lines.length
          line = lines[i]
          
          if (match = line.match(/^(#{1,6})\s+(.+)$/))
            level = match[1].length
            text = process_inline_elements(match[2].strip)
            result << "<h#{level}>#{text}</h#{level}>"
          elsif i + 1 < lines.length && (lines[i + 1].match?(/^[=-]+$/))
            # Alternative heading format
            level = lines[i + 1].start_with?('=') ? 1 : 2
            text = process_inline_elements(line.strip)
            result << "<h#{level}>#{text}</h#{level}>"
            i += 1
          else
            result << line
          end
          i += 1
        end

        result.join("\n")
      end

      def process_lists(html)
        lines = html.split("\n")
        result = []
        in_list = false
        list_type = nil
        list_items = []

        lines.each do |line|
          if (match = line.match(/^(\s*)[\*\-\+]\s+(.+)$/))
            in_list = true
            list_type ||= :ul
            indent = match[1].length
            text = process_inline_elements(match[2])
            list_items << { text: text, indent: indent }
          elsif (match = line.match(/^(\s*)(\d+)\.\s+(.+)$/))
            in_list = true
            list_type ||= :ol
            indent = match[1].length
            text = process_inline_elements(match[3])
            list_items << { text: text, indent: indent }
          else
            if in_list
              result << convert_list(list_items, list_type)
              list_items = []
              list_type = nil
              in_list = false
            end
            result << line
          end
        end

        # Handle list at end
        if in_list
          result << convert_list(list_items, list_type)
        end

        result.join("\n")
      end

      def convert_list(items, type)
        return '' if items.empty?

        tag = type == :ul ? 'ul' : 'ol'
        lines = ["<#{tag}>"]
        
        items.each do |item|
          lines << "  <li>#{item[:text]}</li>"
        end
        
        lines << "</#{tag}>"
        lines.join("\n")
      end

      def process_blockquotes(html)
        lines = html.split("\n")
        result = []
        quote_lines = []
        in_quote = false

        lines.each do |line|
          if (match = line.match(/^>\s+(.+)$/))
            in_quote = true
            quote_lines << process_inline_elements(match[1])
          else
            if in_quote
              result << '<blockquote>'
              result << "  #{quote_lines.join('<br>')}"
              result << '</blockquote>'
              quote_lines = []
              in_quote = false
            end
            result << line
          end
        end

        if in_quote
          result << '<blockquote>'
          result << "  #{quote_lines.join('<br>')}"
          result << '</blockquote>'
        end

        result.join("\n")
      end

      def process_horizontal_rules(html)
        html.gsub(/^[-*_]{3,}$/, '<hr>')
      end

      def process_paragraphs(html)
        lines = html.split("\n")
        result = []
        paragraph_lines = []

        lines.each do |line|
          if line.strip.empty? || line.match?(/^<(h[1-6]|ul|ol|li|blockquote|pre|table|hr|thead|tbody|th|td)/)
            if paragraph_lines.any?
              result << '<p>' + paragraph_lines.join('<br>') + '</p>'
              paragraph_lines = []
            end
            result << line
          elsif line.strip.empty?
            if paragraph_lines.any?
              result << '<p>' + paragraph_lines.join('<br>') + '</p>'
              paragraph_lines = []
            end
          else
            paragraph_lines << line.strip
          end
        end

        if paragraph_lines.any?
          result << '<p>' + paragraph_lines.join('<br>') + '</p>'
        end

        result.join("\n")
      end

      def process_inline_elements(text)
        return text if text.nil? || text.empty?

        # Process in order: bold-italic, bold, italic, strikethrough, inline code, images, links
        result = text.dup

        # Escape HTML first
        result = escape_html(result)

        # Images (before links since they start with !)
        result.gsub!(/!\[([^\]]*)\]\(([^)]+)\)/, '<img src="\2" alt="\1">')

        # Links
        result.gsub!(/\[([^\]]+)\]\(([^)]+)\)/, '<a href="\2">\1</a>')

        # Bold-italic (must be before bold and italic)
        result.gsub!(/\*\*\*([^*]+)\*\*\*/, '<strong><em>\1</em></strong>')

        # Bold
        result.gsub!(/\*\*([^*]+)\*\*/, '<strong>\1</strong>')

        # Italic
        result.gsub!(/[*_]([^*_]+)[*_]/, '<em>\1</em>')

        # Strikethrough
        result.gsub!(/~~([^~]+)~~/, '<del>\1</del>')

        # Inline code (must be last to avoid processing inside code)
        result.gsub!(/`([^`]+)`/, '<code>\1</code>')

        result
      end

      def escape_html(text)
        text.gsub('&', '&amp;')
            .gsub('<', '&lt;')
            .gsub('>', '&gt;')
      end

      def generate_anchor(text)
        text.downcase
            .gsub(/[^a-z0-9\s-]/, '')
            .gsub(/\s+/, '-')
            .gsub(/-+/, '-')
            .gsub(/^-|-$/, '')
      end

      def count_words(text)
        text.split(/\s+/).reject(&:empty?).length
      end

      def count_paragraphs(markdown)
        markdown.split(/\n{2,}/).reject { |p| p.strip.empty? }.length
      end

      def empty_stats
        {
          characters: 0,
          characters_no_spaces: 0,
          words: 0,
          lines: 0,
          paragraphs: 0,
          headings: 0,
          links: 0,
          images: 0,
          code_blocks: 0,
          tables: 0,
          reading_time_minutes: 0
        }
      end

      def default_highlight_theme
        {
          heading: '#1a73e8',
          bold: '#d73a49',
          italic: '#6f42c1',
          code: '#005cc5',
          link: '#0366d6',
          image: '#22863a'
        }
      end
    end
  end
end