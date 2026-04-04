#!/usr/bin/env ruby
# frozen_string_literal: true

# Template Engine Utilities Example
# Demonstrates various features of the template engine

require_relative '../template_utils/mod'

puts "=" * 60
puts "Template Engine Utilities - Examples"
puts "=" * 60

# Example 1: Basic variable interpolation
puts "\n1. Basic Variable Interpolation"
puts "-" * 40
template = "Hello, {{ name }}! Welcome to {{ place }}."
context = { name: "Alice", place: "Ruby World" }
result = AllToolkit::TemplateUtils.render(template, context)
puts "Template: #{template}"
puts "Context:  #{context}"
puts "Result:   #{result}"

# Example 2: Filters
puts "\n2. Filters"
puts "-" * 40
template = <<~TEMPLATE
Name: {{ name | upcase }}
Description: {{ desc | truncate: 20 }}
Price: ${{ price | round: 2 }}
Items: {{ items | join: ", " }}
Count: {{ items | size }}
TEMPLATE

context = {
  name: "product",
  desc: "This is a very long description that will be truncated",
  price: 19.999,
  items: ["red", "green", "blue"]
}
result = AllToolkit::TemplateUtils.render(template, context)
puts "Template:\n#{template}"
puts "Result:\n#{result}"

# Example 3: Conditionals
puts "\n3. Conditionals"
puts "-" * 40
template = <<~TEMPLATE
{% if user %}
Hello, {{ user }}!
{% else %}
Welcome, guest!
{% endif %}

{% if items %}
You have {{ items | size }} items.
{% else %}
Your cart is empty.
{% endif %}
TEMPLATE

context = { user: "Alice", items: ["a", "b", "c"] }
result = AllToolkit::TemplateUtils.render(template, context)
puts "Template:\n#{template}"
puts "Context: #{context}"
puts "Result:\n#{result}"

# Empty cart example
context = { user: nil, items: [] }
result = AllToolkit::TemplateUtils.render(template, context)
puts "\nContext: #{context}"
puts "Result:\n#{result}"

# Example 4: Loops
puts "\n4. Loops"
puts "-" * 40
template = <<~TEMPLATE
Products:
{% for product in products %}
- {{ product.name }}: ${{ product.price | round: 2 }}
{% endfor %}

Total: {{ products | size }} products
TEMPLATE

context = {
  products: [
    { name: "Apple", price: 1.5 },
    { name: "Banana", price: 0.75 },
    { name: "Cherry", price: 2.99 }
  ]
}
result = AllToolkit::TemplateUtils.render(template, context)
puts "Template:\n#{template}"
puts "Result:\n#{result}"

# Example 5: Comments
puts "\n5. Comments"
puts "-" * 40
template = <<~TEMPLATE
{# This is a comment and won't appear in output #}
Visible text
{# Comments can span
multiple lines #}
More visible text
TEMPLATE

result = AllToolkit::TemplateUtils.render(template, {})
puts "Template:\n#{template}"
puts "Result:\n#{result}"

# Example 6: Partials/Include
puts "\n6. Partials/Include"
puts "-" * 40
partials = {
  "header" => "=== {{ title | upcase }} ===",
  "footer" => "--- Generated at {{ time }} ---",
  "item_row" => "- {{ name }}: {{ status | default: 'pending' }}"
}

template = <<~TEMPLATE
{% include 'header' %}

Items:
{% for item in items %}
{% include 'item_row' %}
{% endfor %}

{% include 'footer' %}
TEMPLATE

context = {
  title: "report",
  time: "2024-01-15",
  items: [
    { name: "Task 1", status: "done" },
    { name: "Task 2", status: nil },
    { name: "Task 3", status: "in progress" }
  ]
}
result = AllToolkit::TemplateUtils.render(template, context, partials)
puts "Template:\n#{template}"
puts "Partials: #{partials.keys}"
puts "Result:\n#{result}"

# Example 7: HTML Escaping
puts "\n7. HTML Escaping"
puts "-" * 40
template = <<~TEMPLATE
Original: {{ html }}
Escaped:  {{ html | escape_html }}
Stripped: {{ html | strip_html }}
TEMPLATE

context = { html: "<script>alert('XSS')</script><p>Safe content</p>" }
result = AllToolkit::TemplateUtils.render(template, context)
puts "Template:\n#{template}"
puts "Result:\n#{result}"

# Example 8: Complex Example - Email Template
puts "\n8. Complex Example - Email Template"
puts "-" * 40
email_template = <<~TEMPLATE
Subject: {{ subject | titleize }}

Dear {{ customer.name | capitalize }},

Thank you for your order!

Order Details:
{% for item in order.items %}
- {{ item.name }} x{{ item.qty }} @ ${{ item.price | round: 2 }} = ${{ item.qty | times: item.price | round: 2 }}
{% endfor %}

{% if order.discount > 0 %}
Discount: -${{ order.discount | round: 2 }}
{% endif %}

Total: ${{ order.total | round: 2 }}

{% if order.total > 100 %}
Congratulations! You qualify for free shipping!
{% else %}
Shipping: ${{ order.shipping | round: 2 }}
{% endif %}

Best regards,
{{ company.name }}
{{ company.email }}
TEMPLATE

# Custom filter for multiplication
AllToolkit::TemplateUtils.register_filter(:times) do |value, multiplier|
  value.to_f * multiplier.to_f
end

context = {
  subject: "order confirmation",
  customer: { name: "john doe" },
  order: {
    items: [
      { name: "Widget", qty: 2, price: 29.99 },
      { name: "Gadget", qty: 1, price: 49.99 },
      { name: "Thingama", qty: 3, price: 9.99 }
    ],
    discount: 10.00,
    total: 139.94,
    shipping: 9.99
  },
  company: {
    name: "Acme Corp",
    email: "support@acme.com"
  }
}

result = AllToolkit::TemplateUtils.render(email_template, context)
puts "Template:\n#{email_template}"
puts "Result:\n#{result}"

# Example 9: Comparison Operators
puts "\n9. Comparison Operators"
puts "-" * 40
template = <<~TEMPLATE
{% if score >= 90 %}A{% elsif score >= 80 %}B{% elsif score >= 70 %}C{% else %}F{% endif %} Grade
Score: {{ score }}/100
{% if score == 100 %}Perfect!{% endif %}
{% if score != 0 %}Not zero{% endif %}
{% if score < 60 %}Failing{% else %}Passing{% endif %}
TEMPLATE

context = { score: 85 }
result = AllToolkit::TemplateUtils.render(template, context)
puts "Template:\n#{template}"
puts "Context: #{context}"
puts "Result:\n#{result}"

# Example 10: Using top-level convenience method
puts "\n10. Convenience Method"
puts "-" * 40
template = "Quick render: {{ msg | upcase }}"
result = render_template(template, { msg: "hello world" })
puts "Template: #{template}"
puts "Result:   #{result}"

puts "\n" + "=" * 60
puts "All examples completed!"
puts "=" * 60
