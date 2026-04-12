"""
AllToolkit - Python Template Utils Test Suite

Comprehensive tests for template utilities covering:
- Variable substitution
- Filters
- Conditional blocks (if/elif/else/endif)
- Loop blocks (for/endfor)
- Template inheritance (extends/block/endblock)
- Template includes
- Auto-escaping
- Custom filters
- Edge cases and error handling

Run: python template_utils_test.py -v
"""

import unittest
import sys
import os
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    TemplateEngine, TemplateConfig, TemplateError,
    TemplateSyntaxError, TemplateRenderError, TemplateNotFoundError,
    render, render_file, register_filter, set_globals, set_loader,
    get_engine,
)


class TestTemplateConfig(unittest.TestCase):
    """Tests for TemplateConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = TemplateConfig()
        self.assertEqual(config.var_start, "{{")
        self.assertEqual(config.var_end, "}}")
        self.assertEqual(config.block_start, "{%")
        self.assertEqual(config.block_end, "%}")
        self.assertEqual(config.max_render_depth, 50)
        self.assertEqual(config.max_loop_iterations, 1000)
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = TemplateConfig(
            var_start="${",
            var_end="}",
            max_loop_iterations=100,
        )
        self.assertEqual(config.var_start, "${")
        self.assertEqual(config.var_end, "}")
        self.assertEqual(config.max_loop_iterations, 100)


class TestVariableSubstitution(unittest.TestCase):
    """Tests for variable substitution."""
    
    def setUp(self):
        self.engine = TemplateEngine()
    
    def test_simple_variable(self):
        """Test simple variable substitution."""
        template = "Hello, {{ name }}!"
        result = self.engine.render(template, {"name": "World"})
        self.assertEqual(result, "Hello, World!")
    
    def test_multiple_variables(self):
        """Test multiple variable substitutions."""
        template = "{{ greeting }}, {{ name }}! You are {{ age }} years old."
        context = {"greeting": "Hello", "name": "Alice", "age": 30}
        result = self.engine.render(template, context)
        self.assertEqual(result, "Hello, Alice! You are 30 years old.")
    
    def test_missing_variable(self):
        """Test missing variable renders as empty string."""
        template = "Hello, {{ name }}!"
        result = self.engine.render(template, {})
        self.assertEqual(result, "Hello, !")
    
    def test_none_variable(self):
        """Test None variable renders as empty string."""
        template = "Value: {{ value }}"
        result = self.engine.render(template, {"value": None})
        self.assertEqual(result, "Value: ")
    
    def test_nested_access(self):
        """Test dot notation for nested access."""
        template = "User: {{ user.name }}, Email: {{ user.email }}"
        context = {"user": {"name": "Bob", "email": "bob@example.com"}}
        result = self.engine.render(template, context)
        self.assertEqual(result, "User: Bob, Email: bob@example.com")
    
    def test_attribute_access(self):
        """Test attribute access on objects."""
        class Person:
            def __init__(self, name):
                self.name = name
        
        template = "Hello, {{ person.name }}!"
        context = {"person": Person("Charlie")}
        result = self.engine.render(template, context)
        self.assertEqual(result, "Hello, Charlie!")
    
    def test_numeric_values(self):
        """Test numeric values."""
        template = "Count: {{ count }}, Price: {{ price }}"
        context = {"count": 42, "price": 19.99}
        result = self.engine.render(template, context)
        self.assertEqual(result, "Count: 42, Price: 19.99")
    
    def test_boolean_values(self):
        """Test boolean values."""
        template = "Active: {{ active }}, Disabled: {{ disabled }}"
        context = {"active": True, "disabled": False}
        result = self.engine.render(template, context)
        self.assertEqual(result, "Active: True, Disabled: False")


class TestFilters(unittest.TestCase):
    """Tests for template filters."""
    
    def setUp(self):
        self.engine = TemplateEngine()
    
    def test_upper_filter(self):
        """Test upper filter."""
        template = "{{ name | upper }}"
        result = self.engine.render(template, {"name": "hello"})
        self.assertEqual(result, "HELLO")
    
    def test_lower_filter(self):
        """Test lower filter."""
        template = "{{ name | lower }}"
        result = self.engine.render(template, {"name": "HELLO"})
        self.assertEqual(result, "hello")
    
    def test_capitalize_filter(self):
        """Test capitalize filter."""
        template = "{{ name | capitalize }}"
        result = self.engine.render(template, {"name": "hello world"})
        self.assertEqual(result, "Hello world")
    
    def test_title_filter(self):
        """Test title filter."""
        template = "{{ name | title }}"
        result = self.engine.render(template, {"name": "hello world"})
        self.assertEqual(result, "Hello World")
    
    def test_strip_filter(self):
        """Test strip filter."""
        template = "{{ name | strip }}"
        result = self.engine.render(template, {"name": "  hello  "})
        self.assertEqual(result, "hello")
    
    def test_length_filter(self):
        """Test length filter."""
        template = "{{ items | length }}"
        result = self.engine.render(template, {"items": [1, 2, 3, 4, 5]})
        self.assertEqual(result, "5")
    
    def test_first_filter(self):
        """Test first filter."""
        template = "{{ items | first }}"
        result = self.engine.render(template, {"items": ["a", "b", "c"]})
        self.assertEqual(result, "a")
    
    def test_last_filter(self):
        """Test last filter."""
        template = "{{ items | last }}"
        result = self.engine.render(template, {"items": ["a", "b", "c"]})
        self.assertEqual(result, "c")
    
    def test_chained_filters(self):
        """Test chaining multiple filters."""
        template = "{{ name | lower | capitalize }}"
        result = self.engine.render(template, {"name": "HELLO"})
        self.assertEqual(result, "Hello")
    
    def test_default_filter(self):
        """Test default filter for missing values."""
        template = "{{ name | default:'Unknown' }}"
        result = self.engine.render(template, {})
        self.assertEqual(result, "Unknown")
    
    def test_escape_filter(self):
        """Test escape filter for HTML."""
        template = "{{ content | escape }}"
        result = self.engine.render(template, {"content": "<script>alert('XSS')</script>"})
        self.assertEqual(result, "&lt;script&gt;alert(&#39;XSS&#39;)&lt;/script&gt;")
    
    def test_custom_filter(self):
        """Test custom filter registration."""
        def reverse(s):
            return str(s)[::-1]
        
        self.engine.register_filter("reverse", reverse)
        template = "{{ name | reverse }}"
        result = self.engine.render(template, {"name": "hello"})
        self.assertEqual(result, "olleh")
    
    def test_truncate_filter(self):
        """Test truncate filter."""
        template = "{{ text | truncate }}"
        result = self.engine.render(template, {"text": "a" * 100})
        self.assertTrue(result.endswith("..."))
        self.assertEqual(len(result), 53)  # 50 chars + "..."


class TestConditionals(unittest.TestCase):
    """Tests for conditional blocks."""
    
    def setUp(self):
        self.engine = TemplateEngine()
    
    def test_simple_if(self):
        """Test simple if statement."""
        template = "{% if show %}Visible{% endif %}"
        result = self.engine.render(template, {"show": True})
        self.assertEqual(result, "Visible")
    
    def test_if_false(self):
        """Test if with false condition."""
        template = "{% if show %}Visible{% endif %}"
        result = self.engine.render(template, {"show": False})
        self.assertEqual(result, "")
    
    def test_if_else(self):
        """Test if-else statement."""
        template = "{% if active %}Active{% else %}Inactive{% endif %}"
        result = self.engine.render(template, {"active": True})
        self.assertEqual(result, "Active")
        
        result = self.engine.render(template, {"active": False})
        self.assertEqual(result, "Inactive")
    
    def test_if_elif_else(self):
        """Test if-elif-else statement."""
        template = """{% if level == 1 %}Beginner
{% elif level == 2 %}Intermediate
{% elif level == 3 %}Advanced
{% else %}Unknown{% endif %}"""
        result = self.engine.render(template, {"level": 2})
        self.assertEqual(result.strip(), "Intermediate")
    
    def test_comparison_operators(self):
        """Test comparison operators in conditions."""
        template = "{% if count > 5 %}Many{% else %}Few{% endif %}"
        result = self.engine.render(template, {"count": 10})
        self.assertEqual(result, "Many")
        
        result = self.engine.render(template, {"count": 3})
        self.assertEqual(result, "Few")
    
    def test_equality_operators(self):
        """Test equality operators."""
        template = "{% if name == 'Alice' %}Hello Alice{% endif %}"
        result = self.engine.render(template, {"name": "Alice"})
        self.assertEqual(result, "Hello Alice")
        
        template = "{% if name != 'Bob' %}Not Bob{% endif %}"
        result = self.engine.render(template, {"name": "Alice"})
        self.assertEqual(result, "Not Bob")
    
    def test_logical_and(self):
        """Test logical AND operator."""
        template = "{% if a and b %}Both{% else %}Not both{% endif %}"
        result = self.engine.render(template, {"a": True, "b": True})
        self.assertEqual(result, "Both")
        
        result = self.engine.render(template, {"a": True, "b": False})
        self.assertEqual(result, "Not both")
    
    def test_logical_or(self):
        """Test logical OR operator."""
        template = "{% if a or b %}At least one{% else %}Neither{% endif %}"
        result = self.engine.render(template, {"a": False, "b": True})
        self.assertEqual(result, "At least one")
        
        result = self.engine.render(template, {"a": False, "b": False})
        self.assertEqual(result, "Neither")
    
    def test_not_operator(self):
        """Test NOT operator."""
        template = "{% if not disabled %}Enabled{% endif %}"
        result = self.engine.render(template, {"disabled": False})
        self.assertEqual(result, "Enabled")
    
    def test_in_operator(self):
        """Test 'in' operator."""
        template = "{% if item in items %}Found{% else %}Not found{% endif %}"
        result = self.engine.render(template, {"item": "b", "items": ["a", "b", "c"]})
        self.assertEqual(result, "Found")
        
        result = self.engine.render(template, {"item": "d", "items": ["a", "b", "c"]})
        self.assertEqual(result, "Not found")
    
    def test_truthy_check(self):
        """Test truthy value check."""
        template = "{% if name %}Has name{% else %}No name{% endif %}"
        result = self.engine.render(template, {"name": "Alice"})
        self.assertEqual(result, "Has name")
        
        result = self.engine.render(template, {"name": ""})
        self.assertEqual(result, "No name")


class TestLoops(unittest.TestCase):
    """Tests for loop blocks."""
    
    def setUp(self):
        self.engine = TemplateEngine()
    
    def test_simple_for_loop(self):
        """Test simple for loop."""
        template = "{% for item in items %}{{ item }}{% endfor %}"
        result = self.engine.render(template, {"items": ["a", "b", "c"]})
        self.assertEqual(result, "abc")
    
    def test_for_loop_with_separator(self):
        """Test for loop with separator."""
        template = "{% for item in items %}{{ item }}{% if not loop.last %}, {% endif %}{% endfor %}"
        result = self.engine.render(template, {"items": ["a", "b", "c"]})
        self.assertEqual(result, "a, b, c")
    
    def test_for_loop_index(self):
        """Test loop index variable."""
        template = "{% for item in items %}{{ loop.index }}{% endfor %}"
        result = self.engine.render(template, {"items": ["a", "b", "c"]})
        self.assertEqual(result, "123")
    
    def test_for_loop_first_last(self):
        """Test loop first/last variables."""
        template = "{% for item in items %}{% if loop.first %}F{% endif %}{% if loop.last %}L{% endif %}{% endfor %}"
        result = self.engine.render(template, {"items": ["a", "b", "c"]})
        self.assertEqual(result, "FL")
    
    def test_for_loop_unpack(self):
        """Test for loop with tuple unpacking."""
        template = "{% for key, value in items %}{{ key }}={{ value }},{% endfor %}"
        result = self.engine.render(template, {"items": [("a", 1), ("b", 2)]})
        self.assertEqual(result, "a=1,b=2,")
    
    def test_for_loop_dict(self):
        """Test for loop over dictionary."""
        template = "{% for key, value in items %}{{ key }}:{{ value }},{% endfor %}"
        result = self.engine.render(template, {"items": {"a": 1, "b": 2}})
        # Dict order may vary
        self.assertIn("a:1,", result)
        self.assertIn("b:2,", result)
    
    def test_for_loop_empty(self):
        """Test for loop over empty list."""
        template = "{% for item in items %}{{ item }}{% endfor %}"
        result = self.engine.render(template, {"items": []})
        self.assertEqual(result, "")
    
    def test_for_loop_none(self):
        """Test for loop over None."""
        template = "{% for item in items %}{{ item }}{% endfor %}"
        result = self.engine.render(template, {"items": None})
        self.assertEqual(result, "")
    
    def test_nested_loops(self):
        """Test nested for loops."""
        template = "{% for row in matrix %}{% for cell in row %}{{ cell }}{% endfor %}-{% endfor %}"
        result = self.engine.render(template, {"matrix": [[1, 2], [3, 4]]})
        self.assertEqual(result, "12-34-")


class TestTemplateInheritance(unittest.TestCase):
    """Tests for template inheritance."""
    
    def setUp(self):
        self.engine = TemplateEngine()
        self.temp_dir = tempfile.mkdtemp()
        
        # Set up loader
        def loader(name):
            path = os.path.join(self.temp_dir, name)
            with open(path, 'r') as f:
                return f.read()
        
        self.engine.set_loader(loader)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_extends_and_block(self):
        """Test template inheritance with blocks."""
        # Create base template
        base_path = os.path.join(self.temp_dir, "base.html")
        with open(base_path, 'w') as f:
            f.write("""
<html>
<head>{% block title %}Default Title{% endblock %}</head>
<body>{% block content %}Default Content{% endblock %}</body>
</html>
""".strip())
        
        # Create child template
        child_path = os.path.join(self.temp_dir, "child.html")
        with open(child_path, 'w') as f:
            f.write("""
{% extends "base.html" %}
{% block title %}Custom Title{% endblock %}
{% block content %}Custom Content{% endblock %}
""".strip())
        
        result = self.engine.render_file("child.html", {})
        self.assertIn("Custom Title", result)
        self.assertIn("Custom Content", result)
        self.assertNotIn("Default Title", result)
        self.assertNotIn("Default Content", result)
    
    def test_partial_override(self):
        """Test overriding only some blocks."""
        # Create base template
        base_path = os.path.join(self.temp_dir, "base2.html")
        with open(base_path, 'w') as f:
            f.write("""
<title>{% block title %}Default{% endblock %}</title>
<div>{% block content %}Default Content{% endblock %}</div>
""".strip())
        
        # Create child template (override only title)
        child_path = os.path.join(self.temp_dir, "child2.html")
        with open(child_path, 'w') as f:
            f.write("""
{% extends "base2.html" %}
{% block title %}Custom{% endblock %}
""".strip())
        
        result = self.engine.render_file("child2.html", {})
        self.assertIn("Custom", result)
        self.assertIn("Default Content", result)


class TestIncludes(unittest.TestCase):
    """Tests for template includes."""
    
    def setUp(self):
        self.engine = TemplateEngine()
        self.temp_dir = tempfile.mkdtemp()
        
        def loader(name):
            path = os.path.join(self.temp_dir, name)
            with open(path, 'r') as f:
                return f.read()
        
        self.engine.set_loader(loader)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_include(self):
        """Test including a template."""
        # Create partial
        partial_path = os.path.join(self.temp_dir, "header.html")
        with open(partial_path, 'w') as f:
            f.write("Header: {{ title }}")
        
        # Create main template
        main_path = os.path.join(self.temp_dir, "main.html")
        with open(main_path, 'w') as f:
            f.write("{% include 'header.html' %}\nContent")
        
        result = self.engine.render_file("main.html", {"title": "My Site"})
        self.assertEqual(result, "Header: My Site\nContent")
    
    def test_include_with_loop(self):
        """Test including template inside a loop."""
        # Create item partial
        item_path = os.path.join(self.temp_dir, "item.html")
        with open(item_path, 'w') as f:
            f.write("- {{ item }}\n")
        
        # Create main template
        main_path = os.path.join(self.temp_dir, "list.html")
        with open(main_path, 'w') as f:
            f.write("{% for item in items %}{% include 'item.html' %}{% endfor %}")
        
        result = self.engine.render_file("list.html", {"items": ["a", "b", "c"]})
        self.assertEqual(result, "- a\n- b\n- c\n")


class TestAutoescape(unittest.TestCase):
    """Tests for auto-escaping."""
    
    def test_autoescape_enabled(self):
        """Test auto-escaping when enabled."""
        engine = TemplateEngine(autoescape=True)
        template = "{{ content }}"
        result = engine.render(template, {"content": "<script>alert('XSS')</script>"})
        self.assertIn("&lt;", result)
        self.assertIn("&gt;", result)
        self.assertNotIn("<script>", result)
    
    def test_autoescape_disabled(self):
        """Test no auto-escaping when disabled."""
        engine = TemplateEngine(autoescape=False)
        template = "{{ content }}"
        result = engine.render(template, {"content": "<script>alert('XSS')</script>"})
        self.assertEqual(result, "<script>alert('XSS')</script>")


class TestModuleFunctions(unittest.TestCase):
    """Tests for module-level convenience functions."""
    
    def tearDown(self):
        # Reset default engine
        global _default_engine
        import mod
        mod._default_engine = None
    
    def test_render_function(self):
        """Test module-level render function."""
        result = render("Hello, {{ name }}!", {"name": "World"})
        self.assertEqual(result, "Hello, World!")
    
    def test_register_filter_function(self):
        """Test module-level filter registration."""
        register_filter("double", lambda x: str(x) * 2)
        result = render("{{ value | double }}", {"value": "ab"})
        self.assertEqual(result, "abab")
    
    def test_set_globals_function(self):
        """Test module-level set_globals function."""
        set_globals(site_name="MySite")
        result = render("Welcome to {{ site_name }}")
        self.assertEqual(result, "Welcome to MySite")


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""
    
    def setUp(self):
        self.engine = TemplateEngine()
    
    def test_empty_template(self):
        """Test empty template."""
        result = self.engine.render("", {})
        self.assertEqual(result, "")
    
    def test_template_no_variables(self):
        """Test template with no variables."""
        result = self.engine.render("Plain text", {})
        self.assertEqual(result, "Plain text")
    
    def test_unclosed_if(self):
        """Test error on unclosed if block."""
        template = "{% if show %}Content"
        with self.assertRaises(TemplateSyntaxError):
            self.engine.render(template, {"show": True})
    
    def test_unclosed_for(self):
        """Test error on unclosed for loop."""
        template = "{% for item in items %}{{ item }}"
        with self.assertRaises(TemplateSyntaxError):
            self.engine.render(template, {"items": [1, 2, 3]})
    
    def test_unknown_filter(self):
        """Test error on unknown filter."""
        template = "{{ value | unknown_filter }}"
        with self.assertRaises(TemplateRenderError):
            self.engine.render(template, {"value": "test"})
    
    def test_special_characters_in_content(self):
        """Test special characters in template content."""
        template = "Price: ${{ price }}, Email: {{ email }}"
        result = self.engine.render(template, {"price": "100", "email": "test@example.com"})
        self.assertEqual(result, "Price: $100, Email: test@example.com")
    
    def test_whitespace_handling(self):
        """Test whitespace handling in tags."""
        template = "{{  name  }}"  # Extra spaces
        result = self.engine.render(template, {"name": "Alice"})
        self.assertEqual(result, "Alice")
    
    def test_very_long_output(self):
        """Test rendering with very long output."""
        template = "{% for i in items %}{{ i }}{% endfor %}"
        result = self.engine.render(template, {"items": list(range(1000))})
        self.assertEqual(len(result), sum(len(str(i)) for i in range(1000)))


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple features."""
    
    def setUp(self):
        self.engine = TemplateEngine()
    
    def test_email_template(self):
        """Test a realistic email template."""
        template = """
Subject: Welcome {{ user.name | upper }}!

Dear {{ user.name }},

{% if user.premium %}
Thank you for becoming a Premium member!
{% else %}
Thank you for signing up!
{% endif %}

Your account details:
{% for field, value in user.fields %}
- {{ field | capitalize }}: {{ value }}
{% endfor %}

Best regards,
{{ company }} team
""".strip()
        
        context = {
            "user": {
                "name": "alice",
                "premium": True,
                "fields": [("email", "alice@example.com"), ("joined", "2024-01-01")]
            },
            "company": "Acme"
        }
        
        result = self.engine.render(template, context)
        
        self.assertIn("Welcome ALICE!", result)
        self.assertIn("Dear alice,", result)
        self.assertIn("Premium member", result)
        self.assertIn("- Email: alice@example.com", result)
        self.assertIn("Acme team", result)
    
    def test_html_table(self):
        """Test generating an HTML table."""
        template = """
<table>
<thead>
<tr>{% for header in headers %}<th>{{ header }}</th>{% endfor %}</tr>
</thead>
<tbody>
{% for row in rows %}
<tr>{% for cell in row %}<td>{{ cell }}</td>{% endfor %}</tr>
{% endfor %}
</tbody>
</table>
""".strip()
        
        context = {
            "headers": ["Name", "Age", "City"],
            "rows": [
                ["Alice", 30, "NYC"],
                ["Bob", 25, "LA"],
            ]
        }
        
        result = self.engine.render(template, context)
        
        self.assertIn("<th>Name</th>", result)
        self.assertIn("<td>Alice</td>", result)
        self.assertIn("<td>Bob</td>", result)
    
    def test_config_generation(self):
        """Test generating configuration files."""
        template = """
# Auto-generated config
app_name = {{ app_name }}
version = {{ version }}

{% if debug %}
debug_mode = true
log_level = DEBUG
{% else %}
debug_mode = false
log_level = INFO
{% endif %}

{% for port in ports %}
listen_{{ loop.index }} = {{ port }}
{% endfor %}
""".strip()
        
        context = {
            "app_name": "MyApp",
            "version": "1.0.0",
            "debug": False,
            "ports": [8080, 8443]
        }
        
        result = self.engine.render(template, context)
        
        self.assertIn("app_name = MyApp", result)
        self.assertIn("debug_mode = false", result)
        self.assertIn("log_level = INFO", result)
        self.assertIn("listen_1 = 8080", result)
        self.assertIn("listen_2 = 8443", result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
