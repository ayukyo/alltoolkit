#!/usr/bin/env ruby
# frozen_string_literal: true

# Template Engine Utilities for Ruby
# A lightweight, zero-dependency template engine with variable interpolation,
# conditionals, loops, and filters.
#
# Features:
# - Variable interpolation: {{ variable }}
# - Conditionals: {% if condition %} ... {% endif %}
# - Loops: {% for item in items %} ... {% endfor %}
# - Filters: {{ variable | upcase }}, {{ variable | default: "N/A" }}
# - Partials/Include: {% include "template_name" %}
# - Comments: {# This is a comment #}
#
# Example:
#   template = "Hello, {{ name | upcase }}!"
#   result = TemplateUtils.render(template, { name: "world" })
#   # => "Hello, WORLD!"
#
# @author AllToolkit
# @version 1.0.0

module AllToolkit
  # Template rendering error
  class TemplateError < StandardError; end

  # Template not found error
  class TemplateNotFoundError < TemplateError; end

  # Template syntax error
  class TemplateSyntaxError < TemplateError; end

  # Template rendering context
  class Context
    attr_reader :data, :partials

    def initialize(data = {}, partials = {})
      @data = data.transform_keys(&:to_s)
      @partials = partials.transform_keys(&:to_s)
    end

    def get(key)
      @data[key.to_s]
    end

    def has?(key)
      @data.key?(key.to_s)
    end

    def nest(local_data = {})
      Context.new(@data.merge(local_data.transform_keys(&:to_s)), @partials)
    end

    def partial(name)
      @partials[name.to_s]
    end
  end

  # Built-in filters for template variables
  module Filters
    def self.upcase(value)
      value.to_s.upcase
    end

    def self.downcase(value)
      value.to_s.downcase
    end

    def self.capitalize(value)
      value.to_s.capitalize
    end

    def self.titleize(value)
      value.to_s.split.map(&:capitalize).join(" ")
    end

    def self.strip_html(value)
      value.to_s.gsub(/<[^>]+>/, "")
    end

    def self.escape_html(value)
      value.to_s
            .gsub("&", "&amp;")
            .gsub("<", "&lt;")
            .gsub(">", "&gt;")
            .gsub('"', "&quot;")
            .gsub("'", "&#39;")
    end

    def self.url_encode(value)
      require "cgi"
      CGI.escape(value.to_s)
    end

    def self.truncate(value, length = 50, suffix = "...")
      str = value.to_s
      return str if str.length <= length
      str[0...length] + suffix
    end

    def self.default(value, default_value = "")
      return default_value if value.nil? || (value.respond_to?(:empty?) && value.empty?)
      value
    end

    def self.number_with_delimiter(value)
      value.to_s.reverse.gsub(/(\d{3})(?=\d)/, '\\1,').reverse
    end

    def self.round(value, precision = 0)
      num = Float(value)
      precision.zero? ? num.round : num.round(precision)
    end

    def self.size(value)
      value.respond_to?(:size) ? value.size : value.to_s.size
    end

    def self.join(value, separator = ", ")
      Array(value).join(separator)
    end

    def self.split(value, separator = " ")
      value.to_s.split(separator)
    end

    def self.reverse(value)
      value.respond_to?(:reverse) ? value.reverse : value.to_s.reverse
    end

    def self.first(value)
      value.respond_to?(:first) ? value.first : value.to_s[0]
    end

    def self.last(value)
      value.respond_to?(:last) ? value.last : value.to_s[-1]
    end

    def self.strip(value)
      value.to_s.strip
    end

    def self.replace(value, search, replacement)
      value.to_s.gsub(search, replacement)
    end

    def self.apply(name, value, args = [])
      return value unless respond_to?(name)
      method(name).call(value, *args)
    end
  end

  # Template parser and renderer
  class Template
    TAG_PATTERN = /\{\%\s*(.+?)\s*\%\}/m
    VAR_PATTERN = /\{\{\s*(.+?)\s*\}\}/m
    COMMENT_PATTERN = /\{\#.*?\#\}/m

    attr_reader :source

    def initialize(source)
      @source = source.to_s
    end

    def render(context = {})
      ctx = context.is_a?(Context) ? context : Context.new(context)
      result = @source.dup

      result = result.gsub(COMMENT_PATTERN, "")
      result = process_control_structures(result, ctx)
      result = process_variables(result, ctx)

      result
    end

    private

    def process_control_structures(text, ctx)
      result = text.dup

      loop do
        match = result.match(/\{\%\s*if\s+(.+?)\s*\%\}(.*?)\{\%\s*endif\s*\%\}/m)
        break unless match

        condition = match[1].strip
        content = match[2]
        full_match = match[0]

        if content.include?("{% else %}")
          parts = content.split("{% else %}", 2)
          if_part = parts[0]
          else_part = parts[1]
        else
          if_part = content
          else_part = ""
        end

        if evaluate_condition(condition, ctx)
          result = result.sub(full_match, if_part)
        else
          result = result.sub(full_match, else_part)
        end
      end

      loop do
        match = result.match(/\{\%\s*for\s+(\w+)\s+in\s+(\w+)\s*\%\}(.*?)\{\%\s*endfor\s*\%\}/m)
        break unless match

        var_name = match[1]
        collection_name = match[2]
        loop_body = match[3]
        full_match = match[0]

        collection = ctx.get(collection_name)
        collection = [] unless collection.is_a?(Array)

        output = collection.map do |item|
          loop_ctx = ctx.nest({ var_name => item })
          Template.new(loop_body).render(loop_ctx)
        end.join

        result = result.sub(full_match, output)
      end

      result = result.gsub(/\{\%\s*include\s+["'](.+?)["']\s*\%\}/) do
        partial_name = $1
        partial = ctx.partial(partial_name)
        partial || ""
      end

      result
    end

    def process_variables(text, ctx)
      text.gsub(VAR_PATTERN) do
        expr = $1.strip
        evaluate_expression(expr, ctx)
      end
    end

    def evaluate_expression(expr, ctx)
      parts = expr.split("|").map(&:strip)
      var_expr = parts.shift
      value = get_value(var_expr, ctx)

      parts.each do |filter_expr|
        filter_name, args = parse_filter(filter_expr)
        value = Filters.apply(filter_name, value, args)
      end

      value.to_s
    end

    def parse_filter(filter_expr)
      if filter_expr.include?(":")
        name, arg_str = filter_expr.split(":", 2)
        name = name.strip
        args = parse_filter_args(arg_str.strip)
      else
        name = filter_expr
        args = []
      end
      [name, args]
    end

    def parse_filter_args(arg_str)
      args = []
      arg_str.split(",").each do |arg|
        arg = arg.strip
        if arg.start_with?('"') && arg.end_with?('"')
          args << arg[1...-1]
        elsif arg.start_with?("'") && arg.end_with?("'")
          args << arg[1...-1]
        elsif arg =~ /^\d+$/
          args << arg.to_i
        elsif arg =~ /^\d+\.\d+$/
          args << arg.to_f
        elsif arg == "true"
          args << true
        elsif arg == "false"
          args << false
        elsif arg == "nil" || arg == "null"
          args << nil
        else
          args << arg
        end
      end
      args
    end

    def get_value(expr, ctx)
      expr = expr.strip

      if expr.start_with?('"') && expr.end_with?('"')
        return expr[1...-1]
      end
      if expr.start_with?("'") && expr.end_with?("'")
        return expr[1...-1]
      end
      if expr =~ /^\d+$/
        return expr.to_i
      end
      if expr =~ /^\d+\.\d+$/
        return expr.to_f
      end
      if expr == "true"
        return true
      end
      if expr == "false"
        return false
      end
      if expr == "nil" || expr == "null"
        return nil
      end

      if expr.include?(".")
        parts = expr.split(".")
        value = ctx.get(parts[0])
        parts[1..-1].each do |part|
          return nil if value.nil?
          value = value.respond_to?(:[]) ? value[part] : value.send(part) rescue nil
        end
        return value
      end

      ctx.get(expr)
    end

    def evaluate_condition(condition, ctx)
      condition = condition.strip

      if condition.include?("==")
        left, right = condition.split("==", 2).map(&:strip)
        return get_value(left, ctx) == get_value(right, ctx)
      end

      if condition.include?("!=")
        left, right = condition.split("!=", 2).map(&:strip)
        return get_value(left, ctx) != get_value(right, ctx)
      end

      if condition.include?(">=")
        left, right = condition.split(">=", 2).map(&:strip)
        return get_value(left, ctx).to_f >= get_value(right, ctx).to_f
      end

      if condition.include?("<=")
        left, right = condition.split("<=", 2).map(&:strip)
        return get_value(left, ctx).to_f <= get_value(right, ctx).to_f
      end

      if condition.include?(">")
        left, right = condition.split(">", 2).map(&:strip)
        return get_value(left, ctx).to_f > get_value(right, ctx).to_f
      end

      if condition.include?("<")
        left, right = condition.split("<", 2).map(&:strip)
        return get_value(left, ctx).to_f < get_value(right, ctx).to_f
      end

      if condition.start_with?("not ")
        return !evaluate_condition(condition[4..-1], ctx)
      end

      value = get_value(condition, ctx)
      return false if value.nil?
      return value if value == true || value == false
      return !value.empty? if value.respond_to?(:empty?)
      true
    end
  end

  # Main module for template utilities
  module TemplateUtils
    extend self

    # Render a template with the given context
    # @param template [String] the template source
    # @param context [Hash] the rendering context
    # @param partials [Hash] partial templates for includes
    # @return [String] the rendered output
    def render(template, context = {}, partials = {})
      ctx = Context.new(context, partials)
      Template.new(template).render(ctx)
    end

    # Create a new template object
    # @param source [String] the template source
    # @return [Template] the template object
    def template(source)
      Template.new(source)
    end

    # Register a custom filter
    # @param name [Symbol, String] the filter name
    # @param block [Proc] the filter implementation
    def register_filter(name, &block)
      Filters.define_singleton_method(name, &block)
    end

    # Check if a string is a valid template
    # @param template [String] the template to validate
    # @return [Boolean] true if valid
    def valid?(template)
      Template.new(template)
      true
    rescue TemplateSyntaxError
      false
    end
  end
end

# Convenience method at top level
def render_template(template, context = {}, partials = {})
  AllToolkit::TemplateUtils.render(template, context, partials)
end
