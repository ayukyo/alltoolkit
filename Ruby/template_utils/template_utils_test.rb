#!/usr/bin/env ruby
# frozen_string_literal: true

# Template Engine Utilities Test Suite
# Comprehensive tests for the template engine

require_relative 'mod'

class TemplateUtilsTest
  def self.run
    puts "Running TemplateUtils tests..."
    puts "=" * 50

    tests = [
      :test_variable_interpolation,
      :test_filters,
      :test_conditionals,
      :test_loops,
      :test_comments,
      :test_partials,
      :test_nested_objects,
      :test_complex_templates
    ]

    passed = 0
    failed = 0

    tests.each do |test|
      begin
        new.send(test)
        puts "✓ #{test}"
        passed += 1
      rescue => e
        puts "✗ #{test}: #{e.message}"
        failed += 1
      end
    end

    puts "=" * 50
    puts "Results: #{passed} passed, #{failed} failed"
    exit(failed > 0 ? 1 : 0)
  end

  def assert_equal(expected, actual, msg = nil)
    return if expected == actual
    raise "#{msg || 'Assertion failed'}: expected #{expected.inspect}, got #{actual.inspect}"
  end

  def test_variable_interpolation
    template = "Hello, {{ name }}!"
    result = AllToolkit::TemplateUtils.render(template, { name: "World" })
    assert_equal("Hello, World!", result)

    template = "{{ greeting }}, {{ name }}!"
    result = AllToolkit::TemplateUtils.render(template, { greeting: "Hi", name: "Alice" })
    assert_equal("Hi, Alice!", result)

    template = "Number: {{ num }}"
    result = AllToolkit::TemplateUtils.render(template, { num: 42 })
    assert_equal("Number: 42", result)

    template = "Missing: {{ missing }}"
    result = AllToolkit::TemplateUtils.render(template, {})
    assert_equal("Missing: ", result)
  end

  def test_filters
    template = "{{ name | upcase }}"
    result = AllToolkit::TemplateUtils.render(template, { name: "hello" })
    assert_equal("HELLO", result)

    template = "{{ name | downcase }}"
    result = AllToolkit::TemplateUtils.render(template, { name: "WORLD" })
    assert_equal("world", result)

    template = "{{ name | capitalize }}"
    result = AllToolkit::TemplateUtils.render(template, { name: "hello world" })
    assert_equal("Hello world", result)

    template = "{{ name | titleize }}"
    result = AllToolkit::TemplateUtils.render(template, { name: "hello world" })
    assert_equal("Hello World", result)

    template = "{{ text | truncate: 10 }}"
    result = AllToolkit::TemplateUtils.render(template, { text: "This is a very long text" })
    assert_equal("This is a ...", result)

    template = "{{ empty | default: \"N/A\" }}"
    result = AllToolkit::TemplateUtils.render(template, { empty: "" })
    assert_equal("N/A", result)

    template = "{{ nil_val | default: \"N/A\" }}"
    result = AllToolkit::TemplateUtils.render(template, { nil_val: nil })
    assert_equal("N/A", result)

    template = "{{ num | number_with_delimiter }}"
    result = AllToolkit::TemplateUtils.render(template, { num: 1234567 })
    assert_equal("1,234,567", result)

    template = "{{ items | join: \", \" }}"
    result = AllToolkit::TemplateUtils.render(template, { items: ["a", "b", "c"] })
    assert_equal("a, b, c", result)

    template = "{{ text | strip }}"
    result = AllToolkit::TemplateUtils.render(template, { text: "  hello  " })
    assert_equal("hello", result)

    template = "{{ items | size }}"
    result = AllToolkit::TemplateUtils.render(template, { items: [1, 2, 3, 4, 5] })
    assert_equal("5", result)

    template = "{{ text | escape_html }}"
    result = AllToolkit::TemplateUtils.render(template, { text: "<script>alert('xss')</script>" })
    assert_equal("&lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;", result)

    template = "{{ html | strip_html }}"
    result = AllToolkit::TemplateUtils.render(template, { html: "<p>Hello</p>" })
    assert_equal("Hello", result)

    template = "{{ items | first }}"
    result = AllToolkit::TemplateUtils.render(template, { items: ["a", "b", "c"] })
    assert_equal("a", result)

    template = "{{ items | last }}"
    result = AllToolkit::TemplateUtils.render(template, { items: ["a", "b", "c"] })
    assert_equal("c", result)

    template = "{{ text | reverse }}"
    result = AllToolkit::TemplateUtils.render(template, { text: "hello" })
    assert_equal("olleh", result)

    template = "{{ text | replace: \"world\", \"Ruby\" }}"
    result = AllToolkit::TemplateUtils.render(template, { text: "Hello world" })
    assert_equal("Hello Ruby", result)

    template = "{{ num | round: 2 }}"
    result = AllToolkit::TemplateUtils.render(template, { num: 3.14159 })
    assert_equal("3.14", result)

    template = "{{ text | split: \",\" | size }}"
    result = AllToolkit::TemplateUtils.render(template, { text: "a,b,c" })
    assert_equal("3", result)
  end

  def test_conditionals
    template = "{% if show %}Visible{% endif %}"
    result = AllToolkit::TemplateUtils.render(template, { show: true })
    assert_equal("Visible", result)

    template = "{% if show %}Visible{% endif %}"
    result = AllToolkit::TemplateUtils.render(template, { show: false })
    assert_equal("", result)

    template = "{% if user %}Hello{% else %}Guest{% endif %}"
    result = AllToolkit::TemplateUtils.render(template, { user: "Alice" })
    assert_equal("Hello", result)

    template = "{% if user %}Hello{% else %}Guest{% endif %}"
    result = AllToolkit::TemplateUtils.render(template, {})
    assert_equal("Guest", result)

    template = "{% if count > 5 %}Many{% else %}Few{% endif %}"
    result = AllToolkit::TemplateUtils.render(template, { count: 10 })
    assert_equal("Many", result)

    template = "{% if count > 5 %}Many{% else %}Few{% endif %}"
    result = AllToolkit::TemplateUtils.render(template, { count: 3 })
    assert_equal("Few", result)

    template = "{% if name == \"Alice\" %}Hi Alice{% endif %}"
    result = AllToolkit::TemplateUtils.render(template, { name: "Alice" })
    assert_equal("Hi Alice", result)

    template = "{% if name != \"Bob\" %}Not Bob{% endif %}"
    result = AllToolkit::TemplateUtils.render(template, { name: "Alice" })
    assert_equal("Not Bob", result)

    template = "{% if not hidden %}Shown{% endif %}"
    result = AllToolkit::TemplateUtils.render(template, { hidden: false })
    assert_equal("Shown", result)

    template = "{% if items %}Has items{% endif %}"
    result = AllToolkit::TemplateUtils.render(template, { items: [1, 2, 3] })
    assert_equal("Has items", result)

    template = "{% if items %}Has items{% endif %}"
    result = AllToolkit::TemplateUtils.render(template, { items: [] })
    assert_equal("", result)
  end

  def test_loops
    template = "{% for item in items %}{{ item }}{% endfor %}"
    result = AllToolkit::TemplateUtils.render(template, { items: ["a", "b", "c"] })
    assert_equal("abc", result)

    template = "{% for num in numbers %}{{ num }},{% endfor %}"
    result = AllToolkit::TemplateUtils.render(template, { numbers: [1, 2, 3] })
    assert_equal("1,2,3,", result)

    template = "{% for item in items %}{{ item | upcase }}{% endfor %}"
    result = AllToolkit::TemplateUtils.render(template, { items: ["a", "b"] })
    assert_equal("AB", result)

    template = "Items: {% for item in items %}{{ item }} {% endfor %}"
    result = AllToolkit::TemplateUtils.render(template, { items: ["x", "y"] })
    assert_equal("Items: x y ", result)

    template = "{% for item in empty %}X{% endfor %}Done"
    result = AllToolkit::TemplateUtils.render(template, { empty: [] })
    assert_equal("Done", result)
  end

  def test_comments
    template = "Hello{# this is a comment #} World"
    result = AllToolkit::TemplateUtils.render(template, {})
    assert_equal("Hello World", result)

    template = "{# multi\nline\ncomment #}Done"
    result = AllToolkit::TemplateUtils.render(template, {})
    assert_equal("Done", result)

    template = "{# comment with {{ var }} #}End"
    result = AllToolkit::TemplateUtils.render(template, { var: "test" })
    assert_equal("End", result)
  end

  def test_partials
    partials = {
      "header" => "<header>Welcome</header>",
      "footer" => "<footer>Copyright</footer>"
    }
    template = "{% include 'header' %}Content{% include 'footer' %}"
    result = AllToolkit::TemplateUtils.render(template, {}, partials)
    assert_equal("<header>Welcome</header>Content<footer>Copyright</footer>", result)

    template = "{% include 'missing' %}"
    result = AllToolkit::TemplateUtils.render(template, {}, {})
    assert_equal("", result)
  end

  def test_nested_objects
    user = { name: "Alice", email: "alice@example.com" }
    template = "{{ user.name }} ({{ user.email }})"
    result = AllToolkit::TemplateUtils.render(template, { user: user })
    assert_equal("Alice (alice@example.com)", result)

    data = { items: [{ name: "a" }, { name: "b" }] }
    template = "{% for item in items %}{{ item.name }}{% endfor %}"
    result = AllToolkit::TemplateUtils.render(template, data)
    assert_equal("ab", result)
  end

  def test_complex_templates
    template = <<~TEMPLATE
      Hello {{ name | capitalize }}!
      {% if items %}
      Your items:
      {% for item in items %}
      - {{ item | upcase }}
      {% endfor %}
      {% else %}
      No items.
      {% endif %}
    TEMPLATE

    context = {
      name: "alice",
      items: ["apple", "banana"]
    }

    result = AllToolkit::TemplateUtils.render(template, context)
    expected = <<~EXPECTED
      Hello Alice!
      
      Your items:
      
      - APPLE
      
      - BANANA
      
    EXPECTED

    assert_equal(expected, result)

    # Test with empty items
    context = { name: "bob", items: [] }
    result = AllToolkit::TemplateUtils.render(template, context)
    expected = <<~EXPECTED
      Hello Bob!
      
      No items.
      
    EXPECTED

    assert_equal(expected, result)
  end
end

TemplateUtilsTest.run if __FILE__ == $0