"""
AllToolkit - Template Utils Basic Usage Examples

Simple examples demonstrating common template operations.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    render, render_file, register_filter, set_globals,
    TemplateEngine, TemplateConfig,
)


def main():
    print("=" * 60)
    print("AllToolkit - Template Utils Basic Examples")
    print("=" * 60)
    print()
    
    # 1. Simple Variable Substitution
    print("1. Simple Variable Substitution")
    print("-" * 40)
    template = "Hello, {{ name }}!"
    result = render(template, {"name": "World"})
    print(f"  Template: {template}")
    print(f"  Result: {result}")
    print()
    
    # 2. Multiple Variables
    print("2. Multiple Variables")
    print("-" * 40)
    template = "{{ greeting }}, {{ name }}! You are {{ age }} years old."
    context = {"greeting": "Hello", "name": "Alice", "age": 30}
    result = render(template, context)
    print(f"  Result: {result}")
    print()
    
    # 3. Built-in Filters
    print("3. Built-in Filters")
    print("-" * 40)
    
    filters_demo = [
        ("upper", "{{ name | upper }}", {"name": "hello"}),
        ("lower", "{{ name | lower }}", {"name": "HELLO"}),
        ("capitalize", "{{ name | capitalize }}", {"name": "hello world"}),
        ("title", "{{ name | title }}", {"name": "hello world"}),
        ("strip", "{{ name | strip }}", {"name": "  hello  "}),
        ("length", "{{ items | length }}", {"items": [1, 2, 3, 4, 5]}),
        ("first", "{{ items | first }}", {"items": ["a", "b", "c"]}),
        ("last", "{{ items | last }}", {"items": ["a", "b", "c"]}),
    ]
    
    for filter_name, template, context in filters_demo:
        result = render(template, context)
        print(f"  {filter_name}: {result}")
    print()
    
    # 4. Chained Filters
    print("4. Chained Filters")
    print("-" * 40)
    template = "{{ name | lower | capitalize }}"
    result = render(template, {"name": "HELLO WORLD"})
    print(f"  Template: {template}")
    print(f"  Result: {result}")
    print()
    
    # 5. Default Filter
    print("5. Default Filter (for missing values)")
    print("-" * 40)
    template = "Name: {{ name | default:'Unknown' }}"
    result = render(template, {})
    print(f"  Result: {result}")
    print()
    
    # 6. Conditional: if/else
    print("6. Conditional: if/else")
    print("-" * 40)
    template = "{% if active %}Active{% else %}Inactive{% endif %}"
    
    result_true = render(template, {"active": True})
    result_false = render(template, {"active": False})
    print(f"  active=True: {result_true}")
    print(f"  active=False: {result_false}")
    print()
    
    # 7. Conditional: if/elif/else
    print("7. Conditional: if/elif/else")
    print("-" * 40)
    template = """
{% if level == 1 %}Beginner
{% elif level == 2 %}Intermediate
{% elif level == 3 %}Advanced
{% else %}Unknown{% endif %}
""".strip()
    
    for level in [1, 2, 3, 4]:
        result = render(template, {"level": level})
        print(f"  level={level}: {result}")
    print()
    
    # 8. For Loop
    print("8. For Loop")
    print("-" * 40)
    template = "{% for item in items %}{{ item }}{% endfor %}"
    result = render(template, {"items": ["a", "b", "c", "d"]})
    print(f"  Result: {result}")
    print()
    
    # 9. For Loop with Separator
    print("9. For Loop with Separator")
    print("-" * 40)
    template = "{% for item in items %}{{ item }}{% if not loop.last %}, {% endif %}{% endfor %}"
    result = render(template, {"items": ["apple", "banana", "cherry"]})
    print(f"  Result: {result}")
    print()
    
    # 10. For Loop with Index
    print("10. For Loop with Index")
    print("-" * 40)
    template = "{% for item in items %}{{ loop.index }}. {{ item }}\n{% endfor %}"
    result = render(template, {"items": ["First", "Second", "Third"]})
    print(f"  Result:\n{result}")
    print()
    
    # 11. Nested Access
    print("11. Nested Access (Dot Notation)")
    print("-" * 40)
    template = "User: {{ user.name }}, Email: {{ user.email }}, City: {{ user.address.city }}"
    context = {
        "user": {
            "name": "Bob",
            "email": "bob@example.com",
            "address": {"city": "Shanghai"}
        }
    }
    result = render(template, context)
    print(f"  Result: {result}")
    print()
    
    # 12. Comparison Operators
    print("12. Comparison Operators")
    print("-" * 40)
    template = "{% if count > 5 %}Many{% elif count == 5 %}Exactly 5{% else %}Few{% endif %}"
    for count in [3, 5, 10]:
        result = render(template, {"count": count})
        print(f"  count={count}: {result}")
    print()
    
    # 13. Logical Operators
    print("13. Logical Operators (and/or/not)")
    print("-" * 40)
    template = "{% if a and b %}Both{% elif a or b %}One{% else %}Neither{% endif %}"
    test_cases = [
        {"a": True, "b": True},
        {"a": True, "b": False},
        {"a": False, "b": False},
    ]
    for ctx in test_cases:
        result = render(template, ctx)
        print(f"  a={ctx['a']}, b={ctx['b']}: {result}")
    print()
    
    # 14. 'in' Operator
    print("14. 'in' Operator")
    print("-" * 40)
    template = "{% if item in items %}Found{% else %}Not found{% endif %}"
    result1 = render(template, {"item": "b", "items": ["a", "b", "c"]})
    result2 = render(template, {"item": "d", "items": ["a", "b", "c"]})
    print(f"  'b' in ['a','b','c']: {result1}")
    print(f"  'd' in ['a','b','c']: {result2}")
    print()
    
    # 15. Custom Filter
    print("15. Custom Filter")
    print("-" * 40)
    
    def reverse(s):
        return str(s)[::-1]
    
    def currency(value):
        return f"¥{float(value):,.2f}"
    
    register_filter("reverse", reverse)
    register_filter("currency", currency)
    
    template1 = "{{ name | reverse }}"
    result1 = render(template1, {"name": "hello"})
    print(f"  reverse: {result1}")
    
    template2 = "Price: {{ price | currency }}"
    result2 = render(template2, {"price": 1234.56})
    print(f"  currency: {result2}")
    print()
    
    # 16. Global Variables
    print("16. Global Variables")
    print("-" * 40)
    set_globals(site_name="MySite", version="1.0.0")
    template = "Welcome to {{ site_name }} v{{ version }}"
    result = render(template)
    print(f"  Result: {result}")
    print()
    
    # 17. Auto-escaping
    print("17. Auto-escaping")
    print("-" * 40)
    engine_safe = TemplateEngine(autoescape=True)
    template = "{{ content }}"
    dangerous = "<script>alert('XSS')</script>"
    result = engine_safe.render(template, {"content": dangerous})
    print(f"  Input: {dangerous}")
    print(f"  Output (escaped): {result}")
    print()
    
    # 18. Dictionary Iteration
    print("18. Dictionary Iteration")
    print("-" * 40)
    template = "{% for key, value in data %}{{ key }}: {{ value }}\n{% endfor %}"
    context = {"data": {"name": "Alice", "age": 30, "city": "NYC"}}
    result = render(template, context)
    print(f"  Result:\n{result}")
    print()
    
    # 19. Tuple Unpacking in Loop
    print("19. Tuple Unpacking in Loop")
    print("-" * 40)
    template = "{% for name, age in people %}{{ name }} is {{ age }}\n{% endfor %}"
    context = {"people": [("Alice", 30), ("Bob", 25), ("Charlie", 35)]}
    result = render(template, context)
    print(f"  Result:\n{result}")
    print()
    
    # 20. Complex Template
    print("20. Complex Template (Email)")
    print("-" * 40)
    email_template = """
Subject: Welcome {{ user.name | upper }}!

Dear {{ user.name }},

{% if user.premium %}
感谢您成为 Premium 会员！
{% else %}
感谢您的注册！
{% endif %}

账户详情：
{% for field, value in user.fields %}
- {{ field | capitalize }}: {{ value }}
{% endfor %}

此致，
{{ company }} 团队
""".strip()
    
    context = {
        "user": {
            "name": "alice",
            "premium": True,
            "fields": [("email", "alice@example.com"), ("joined", "2024-01-01")]
        },
        "company": "Acme"
    }
    result = render(email_template, context)
    print(f"  Result:\n{result}")
    print()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
