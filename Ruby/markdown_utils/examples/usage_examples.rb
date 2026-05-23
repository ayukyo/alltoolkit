#!/usr/bin/env ruby
# frozen_string_literal: true

require_relative 'mod'

puts "=" * 60
puts "MarkdownUtils Usage Examples"
puts "=" * 60
puts

# Example 1: Convert Markdown to HTML
puts "1. Convert Markdown to HTML"
puts "-" * 40
markdown = <<~MARKDOWN
  # Hello World
  
  This is a **bold** statement with *italic* text.
  
  ## Features
  
  - Item 1
  - Item 2
  - Item 3
  
  [Click here](https://example.com) for more info.
  
  ```ruby
  puts "Hello, World!"
  ```
MARKDOWN

html = AllToolkit::MarkdownUtils.to_html(markdown)
puts html
puts

# Example 2: Extract headings
puts "2. Extract Headings"
puts "-" * 40
markdown = <<~MARKDOWN
  # Main Title
  
  ## Chapter 1
  
  ### Section 1.1
  
  ### Section 1.2
  
  ## Chapter 2
  
  ### Section 2.1
MARKDOWN

headings = AllToolkit::MarkdownUtils.extract_headings(markdown)
headings.each do |h|
  puts "#{'  ' * (h[:level] - 1)}Level #{h[:level]}: #{h[:text]} (##{h[:anchor]})"
end
puts

# Example 3: Generate Table of Contents
puts "3. Generate Table of Contents"
puts "-" * 40
toc = AllToolkit::MarkdownUtils.generate_toc(markdown)
puts toc
puts

# Example 4: Extract links
puts "4. Extract Links"
puts "-" * 40
markdown = <<~MARKDOWN
  Check out [OpenAI](https://openai.com) and [GitHub](https://github.com).
  
  Also visit [Ruby](https://ruby-lang.org) for more.
MARKDOWN

links = AllToolkit::MarkdownUtils.extract_links(markdown)
links.each do |link|
  puts "  Text: #{link[:text]}"
  puts "  URL:  #{link[:url]}"
  puts
end

# Example 5: Extract images
puts "5. Extract Images"
puts "-" * 40
markdown = <<~MARKDOWN
  ![Logo](logo.png "Company Logo")
  
  Here is a screenshot:
  
  ![Screenshot](https://example.com/screenshot.png)
MARKDOWN

images = AllToolkit::MarkdownUtils.extract_images(markdown)
images.each do |img|
  puts "  Alt:   #{img[:alt]}"
  puts "  URL:   #{img[:url]}"
  puts "  Title: #{img[:title]}" if img[:title]
  puts
end

# Example 6: Extract code blocks
puts "6. Extract Code Blocks"
puts "-" * 40
markdown = <<~MARKDOWN
  Here is some Ruby code:
  
  ```ruby
  def greet(name)
    puts "Hello, #{name}!"
  end
  ```
  
  And some Python:
  
  ```python
  def greet(name):
      print(f"Hello, {name}!")
  ```
  
  Use `inline_code` for short snippets.
MARKDOWN

blocks = AllToolkit::MarkdownUtils.extract_code_blocks(markdown)
blocks.each do |block|
  if block[:inline]
    puts "  [Inline] #{block[:code]}"
  else
    puts "  [#{block[:language] || 'plain'}] #{block[:code].lines.first.strip}..."
  end
end
puts

# Example 7: Extract tables
puts "7. Extract Tables"
puts "-" * 40
markdown = <<~MARKDOWN
  | Name  | Age | City     |
  |-------|-----|----------|
  | Alice | 30  | New York |
  | Bob   | 25  | London   |
  | Carol | 28  | Paris    |
MARKDOWN

tables = AllToolkit::MarkdownUtils.extract_tables(markdown)
tables.each do |table|
  puts "  Headers: #{table[:headers].join(', ')}"
  puts "  Alignments: #{table[:alignments].map { |a| a || 'default' }.join(', ')}"
  puts "  Rows: #{table[:rows].length}"
  table[:rows].each do |row|
    puts "    - #{row.join(' | ')}"
  end
end
puts

# Example 8: Get statistics
puts "8. Document Statistics"
puts "-" * 40
markdown = <<~MARKDOWN
  # Sample Document
  
  This is a sample markdown document with **various** formatting.
  
  ## Links
  
  Check [GitHub](https://github.com) and [OpenAI](https://openai.com).
  
  ## Images
  
  ![Logo](logo.png)
  ![Banner](banner.png)
  
  ## Code
  
  ```javascript
  console.log("Hello!");
  ```
  
  - Item 1
  - Item 2
  - Item 3
MARKDOWN

stats = AllToolkit::MarkdownUtils.stats(markdown)
puts "  Characters: #{stats[:characters]}"
puts "  Characters (no spaces): #{stats[:characters_no_spaces]}"
puts "  Words: #{stats[:words]}"
puts "  Lines: #{stats[:lines]}"
puts "  Paragraphs: #{stats[:paragraphs]}"
puts "  Headings: #{stats[:headings]}"
puts "  Links: #{stats[:links]}"
puts "  Images: #{stats[:images]}"
puts "  Code blocks: #{stats[:code_blocks]}"
puts "  Tables: #{stats[:tables]}"
puts "  Reading time: ~#{stats[:reading_time_minutes]} min"
puts

# Example 9: Convert to plain text
puts "9. Convert to Plain Text"
puts "-" * 40
markdown = <<~MARKDOWN
  # Important Notice
  
  This is **bold** and *italic* text.
  
  [Click here](https://example.com) for details.
  
  ```
  Code block
  ```
  
  > A wise quote
MARKDOWN

plain = AllToolkit::MarkdownUtils.to_plain_text(markdown)
puts plain
puts

# Example 10: Validate Markdown
puts "10. Validate Markdown"
puts "-" * 40
samples = [
  "# Valid Title\n\nContent here",
  "",
  nil,
  "Just plain text",
  "**Bold** and *italic*"
]

samples.each do |sample|
  result = AllToolkit::MarkdownUtils.valid_markdown?(sample)
  display = sample.nil? ? 'nil' : (sample.empty? ? 'empty' : sample[0..30])
  puts "  #{display.inspect}: #{result ? 'Valid' : 'Invalid'}"
end
puts

# Example 11: Complex document conversion
puts "11. Complex Document Conversion"
puts "-" * 40
complex_markdown = <<~MARKDOWN
  # Project Documentation
  
  Welcome to our project! This guide will help you get started.
  
  ## Table of Contents
  
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Usage](#usage)
  
  ## Introduction
  
  This project demonstrates **markdown processing** in Ruby.
  
  ### Features
  
  - Fast parsing
  - Zero dependencies
  - Comprehensive API
  
  ## Installation
  
  Add this line to your application's Gemfile:
  
  ```ruby
  gem 'markdown_utils'
  ```
  
  Then execute:
  
  ```bash
  $ bundle install
  ```
  
  ## Usage
  
  > Note: Make sure to require the module first.
  
  | Method | Description |
  |--------|-------------|
  | `to_html` | Convert to HTML |
  | `extract_headings` | Get all headings |
  
  For more information, visit [our website](https://example.com).
  
  ---
  
  *Last updated: 2024*
MARKDOWN

html_output = AllToolkit::MarkdownUtils.to_html(complex_markdown)
puts html_output[0..500] + "..."
puts

puts "=" * 60
puts "All examples completed successfully!"
puts "=" * 60