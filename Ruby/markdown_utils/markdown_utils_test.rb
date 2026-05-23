#!/usr/bin/env ruby
# frozen_string_literal: true

require_relative 'mod'

module AllToolkit
  module MarkdownUtils
    class << self
      def run_tests
        tests_passed = 0
        tests_failed = 0

        puts '=' * 60
        puts 'MarkdownUtils Test Suite'
        puts '=' * 60
        puts

        # Test 1: to_html - Basic heading
        result = test('to_html - Basic heading') do
          html = MarkdownUtils.to_html('# Hello World')
          raise "Expected <h1> tag" unless html.include?('<h1>')
          raise "Expected 'Hello World'" unless html.include?('Hello World')
          raise "Expected closing tag" unless html.include?('</h1>')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 2: to_html - Multiple heading levels
        result = test('to_html - Multiple heading levels') do
          html = MarkdownUtils.to_html("# H1\n## H2\n### H3")
          raise "Missing h1" unless html.include?('<h1>')
          raise "Missing h2" unless html.include?('<h2>')
          raise "Missing h3" unless html.include?('<h3>')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 3: to_html - Bold text
        result = test('to_html - Bold text') do
          html = MarkdownUtils.to_html('This is **bold** text')
          raise "Expected <strong> tag" unless html.include?('<strong>')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 4: to_html - Italic text
        result = test('to_html - Italic text') do
          html = MarkdownUtils.to_html('This is *italic* text')
          raise "Expected <em> tag" unless html.include?('<em>')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 5: to_html - Links
        result = test('to_html - Links') do
          html = MarkdownUtils.to_html('[OpenAI](https://openai.com)')
          raise "Expected <a> tag" unless html.include?('<a href="https://openai.com">')
          raise "Expected link text" unless html.include?('OpenAI')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 6: to_html - Images
        result = test('to_html - Images') do
          html = MarkdownUtils.to_html('![Alt text](https://example.com/image.png)')
          raise "Expected <img> tag" unless html.include?('<img')
          raise "Expected src attribute" unless html.include?('src="https://example.com/image.png"')
          raise "Expected alt attribute" unless html.include?('alt="Alt text"')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 7: to_html - Code blocks
        result = test('to_html - Code blocks') do
          html = MarkdownUtils.to_html("```ruby\nputs 'hello'\n```")
          raise "Expected <pre><code> tags" unless html.include?('<pre><code')
          raise "Expected language class" unless html.include?('language-ruby')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 8: to_html - Inline code
        result = test('to_html - Inline code') do
          html = MarkdownUtils.to_html('Use the `console.log` function')
          raise "Expected <code> tag" unless html.include?('<code>')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 9: to_html - Unordered lists
        result = test('to_html - Unordered lists') do
          html = MarkdownUtils.to_html("- Item 1\n- Item 2\n- Item 3")
          raise "Expected <ul> tag" unless html.include?('<ul>')
          raise "Expected <li> tags" unless html.include?('<li>')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 10: to_html - Ordered lists
        result = test('to_html - Ordered lists') do
          html = MarkdownUtils.to_html("1. First\n2. Second\n3. Third")
          raise "Expected <ol> tag" unless html.include?('<ol>')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 11: to_html - Blockquotes
        result = test('to_html - Blockquotes') do
          html = MarkdownUtils.to_html('> This is a quote')
          raise "Expected <blockquote> tag" unless html.include?('<blockquote>')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 12: to_html - Horizontal rules
        result = test('to_html - Horizontal rules') do
          html = MarkdownUtils.to_html('Content\n\n---\n\nMore content')
          raise "Expected <hr> tag" unless html.include?('<hr>')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 13: to_html - Tables
        result = test('to_html - Tables') do
          markdown = "| Name | Age |\n|------|-----|\n| Alice | 30 |\n| Bob | 25 |"
          html = MarkdownUtils.to_html(markdown)
          raise "Expected <table> tag" unless html.include?('<table>')
          raise "Expected <thead> tag" unless html.include?('<thead>')
          raise "Expected <tbody> tag" unless html.include?('<tbody>')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 14: extract_headings - Basic extraction
        result = test('extract_headings - Basic extraction') do
          markdown = "# Main Title\n## Section 1\n### Subsection"
          headings = MarkdownUtils.extract_headings(markdown)
          raise "Expected 3 headings" unless headings.length == 3
          raise "Wrong first heading level" unless headings[0][:level] == 1
          raise "Wrong first heading text" unless headings[0][:text] == 'Main Title'
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 15: extract_headings - Anchor generation
        result = test('extract_headings - Anchor generation') do
          markdown = "# Hello World!\n## This is a Test"
          headings = MarkdownUtils.extract_headings(markdown)
          raise "Wrong anchor format" unless headings[0][:anchor] == 'hello-world'
          raise "Wrong second anchor" unless headings[1][:anchor] == 'this-is-a-test'
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 16: generate_toc - Basic TOC
        result = test('generate_toc - Basic TOC') do
          markdown = "# Title\n## Section 1\n## Section 2\n### Subsection"
          toc = MarkdownUtils.generate_toc(markdown)
          raise "Expected TOC header" unless toc.include?('Table of Contents')
          raise "Expected link to Title" unless toc.include?('#title')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 17: generate_toc - Max level filtering
        result = test('generate_toc - Max level filtering') do
          markdown = "# H1\n## H2\n### H3\n#### H4"
          toc = MarkdownUtils.generate_toc(markdown, 2)
          raise "Should not contain h3" if toc.include?('h3')
          raise "Should not contain h4" if toc.include?('h4')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 18: extract_links - Basic extraction
        result = test('extract_links - Basic extraction') do
          markdown = "Check out [OpenAI](https://openai.com) and [Google](https://google.com)"
          links = MarkdownUtils.extract_links(markdown)
          raise "Expected 2 links" unless links.length == 2
          raise "Wrong first link text" unless links[0][:text] == 'OpenAI'
          raise "Wrong first link URL" unless links[0][:url] == 'https://openai.com'
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 19: extract_links - Don't extract images
        result = test('extract_links - Dont extract images') do
          markdown = "![Image](img.png) and [Link](url.com)"
          links = MarkdownUtils.extract_links(markdown)
          raise "Expected 1 link (not image)" unless links.length == 1
          raise "Wrong link text" unless links[0][:text] == 'Link'
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 20: extract_images - Basic extraction
        result = test('extract_images - Basic extraction') do
          markdown = "![Logo](logo.png) and ![Icon](icon.png)"
          images = MarkdownUtils.extract_images(markdown)
          raise "Expected 2 images" unless images.length == 2
          raise "Wrong first image alt" unless images[0][:alt] == 'Logo'
          raise "Wrong first image URL" unless images[0][:url] == 'logo.png'
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 21: extract_code_blocks - Fenced code blocks
        result = test('extract_code_blocks - Fenced code blocks') do
          markdown = "```ruby\nputs 'hello'\n```\n```python\nprint('world')\n```"
          blocks = MarkdownUtils.extract_code_blocks(markdown)
          code_blocks = blocks.reject { |b| b[:inline] }
          raise "Expected 2 code blocks" unless code_blocks.length == 2
          raise "Wrong first language" unless code_blocks[0][:language] == 'ruby'
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 22: extract_code_blocks - Inline code
        result = test('extract_code_blocks - Inline code') do
          markdown = "Use `code` and `more code` here"
          blocks = MarkdownUtils.extract_code_blocks(markdown)
          inline_blocks = blocks.select { |b| b[:inline] }
          raise "Expected 2 inline blocks" unless inline_blocks.length == 2
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 23: extract_tables - Basic table
        result = test('extract_tables - Basic table') do
          markdown = "| A | B |\n|---|---|\n| 1 | 2 |"
          tables = MarkdownUtils.extract_tables(markdown)
          raise "Expected 1 table" unless tables.length == 1
          raise "Wrong headers" unless tables[0][:headers] == ['A', 'B']
          raise "Wrong row count" unless tables[0][:rows].length == 1
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 24: extract_tables - Alignment detection
        result = test('extract_tables - Alignment detection') do
          markdown = "| Left | Center | Right |\n|:-----|:------:|-------:|\n| L | C | R |"
          tables = MarkdownUtils.extract_tables(markdown)
          raise "Expected alignments" unless tables[0][:alignments]
          raise "Wrong left align" unless tables[0][:alignments][0] == 'left'
          raise "Wrong center align" unless tables[0][:alignments][1] == 'center'
          raise "Wrong right align" unless tables[0][:alignments][2] == 'right'
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 25: stats - Basic statistics
        result = test('stats - Basic statistics') do
          markdown = "# Title\n\nThis is a paragraph.\n\n- Item 1\n- Item 2\n\n![Image](img.png)\n\n[Link](url.com)"
          stats = MarkdownUtils.stats(markdown)
          raise "Wrong word count" unless stats[:words] > 0
          raise "Wrong heading count" unless stats[:headings] == 1
          raise "Wrong link count" unless stats[:links] == 1
          raise "Wrong image count" unless stats[:images] == 1
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 26: stats - Reading time
        result = test('stats - Reading time') do
          # Generate ~400 words
          words = Array.new(400) { "word" }.join(' ')
          markdown = "# Article\n\n#{words}"
          stats = MarkdownUtils.stats(markdown)
          raise "Expected reading time >= 2 minutes" unless stats[:reading_time_minutes] >= 2
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 27: to_plain_text - Basic conversion
        result = test('to_plain_text - Basic conversion') do
          markdown = "# **Bold** Title\n\nThis is *italic* text with [link](url).\n\n```\ncode\n```"
          plain = MarkdownUtils.to_plain_text(markdown)
          raise "Should not contain #" if plain.include?('#')
          raise "Should not contain **" if plain.include?('**')
          raise "Should not contain *" if plain.include?('*')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 28: to_plain_text - Preserve link text
        result = test('to_plain_text - Preserve link text') do
          markdown = "Click [here](https://example.com) for info"
          plain = MarkdownUtils.to_plain_text(markdown)
          raise "Should contain 'here'" unless plain.include?('here')
          raise "Should not contain URL" if plain.include?('https://')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 29: valid_markdown? - Valid markdown
        result = test('valid_markdown? - Valid markdown') do
          raise "Should be valid" unless MarkdownUtils.valid_markdown?("# Title\n\nContent")
          raise "Empty should be invalid" if MarkdownUtils.valid_markdown?('')
          raise "Nil should be invalid" if MarkdownUtils.valid_markdown?(nil)
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 30: to_html - Strikethrough
        result = test('to_html - Strikethrough') do
          html = MarkdownUtils.to_html('This is ~~deleted~~ text')
          raise "Expected <del> tag" unless html.include?('<del>')
          raise "Expected 'deleted' text" unless html.include?('deleted')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 31: to_html - Complex document
        result = test('to_html - Complex document') do
          markdown = <<~MARKDOWN
            # Main Title
            
            This is an **introduction** paragraph with *various* formatting.
            
            ## Features
            
            - Feature one
            - Feature two
            - Feature three
            
            ### Code Example
            
            ```ruby
            def hello
              puts "Hello, World!"
            end
            ```
            
            > This is a blockquote
            
            Check out [our website](https://example.com) for more info.
          MARKDOWN
          
          html = MarkdownUtils.to_html(markdown)
          raise "Missing h1" unless html.include?('<h1>')
          raise "Missing h2" unless html.include?('<h2>')
          raise "Missing h3" unless html.include?('<h3>')
          raise "Missing strong" unless html.include?('<strong>')
          raise "Missing em" unless html.include?('<em>')
          raise "Missing ul" unless html.include?('<ul>')
          raise "Missing pre/code" unless html.include?('<pre>')
          raise "Missing blockquote" unless html.include?('<blockquote>')
          raise "Missing link" unless html.include?('<a href')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 32: Alternative heading format
        result = test('to_html - Alternative heading format') do
          markdown = "Main Title\n==========\n\nSubtitle\n--------"
          html = MarkdownUtils.to_html(markdown)
          raise "Expected h1 for === format" unless html.include?('<h1>')
          raise "Expected h2 for --- format" unless html.include?('<h2>')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Test 33: HTML escaping
        result = test('to_html - HTML escaping') do
          markdown = "Use `<div>` tags and & symbols"
          html = MarkdownUtils.to_html(markdown)
          raise "Should escape <" unless html.include?('&lt;')
          raise "Should escape >" unless html.include?('&gt;')
          raise "Should escape &" unless html.include?('&amp;')
          true
        end
        result ? tests_passed += 1 : tests_failed += 1

        # Summary
        puts
        puts '=' * 60
        puts "Tests completed: #{tests_passed + tests_failed}"
        puts "Passed: #{tests_passed}"
        puts "Failed: #{tests_failed}"
        puts '=' * 60

        tests_failed == 0
      end

      def test(name)
        print "#{name}... "
        begin
          result = yield
          if result
            puts "\e[32mPASSED\e[0m"
            true
          else
            puts "\e[31mFAILED\e[0m"
            false
          end
        rescue => e
          puts "\e[31mFAILED\e[0m"
          puts "  Error: #{e.message}"
          false
        end
      end
    end
  end
end

# Run tests if executed directly
if __FILE__ == $PROGRAM_NAME
  AllToolkit::MarkdownUtils.run_tests
end