#!/usr/bin/env ruby
# frozen_string_literal: true

# HTTP Utils Test Suite
# Run with: ruby http_utils_test.rb

require_relative 'mod'

# Simple test framework
module TestFramework
  class << self
    attr_accessor :passed, :failed, :tests

    def run
      @passed = 0
      @failed = 0
      @tests = []

      yield

      puts "\n" + "=" * 60
      puts "Test Results: #{@passed} passed, #{@failed} failed, #{@passed + @failed} total"
      puts "=" * 60

      exit(@failed > 0 ? 1 : 0)
    end

    def test(name)
      @tests << name
      yield
      @passed += 1
      puts "  ✓ #{name}"
    rescue StandardError => e
      @failed += 1
      puts "  ✗ #{name}: #{e.message}"
    end

    def assert(condition, message = 'Assertion failed')
      raise message unless condition
    end

    def assert_equal(expected, actual, message = nil)
      msg = message || "Expected #{expected.inspect}, got #{actual.inspect}"
      raise msg unless expected == actual
    end

    def assert_not_nil(value, message = 'Expected non-nil value')
      raise message if value.nil?
    end

    def assert_nil(value, message = 'Expected nil value')
      raise message unless value.nil?
    end

    def assert_true(value, message = 'Expected true')
      raise message unless value == true
    end

    def assert_false(value, message = 'Expected false')
      raise message unless value == false
    end
  end
end

# Run tests
TestFramework.run do
  puts "\n=== URL Encoding/Decoding Tests ==="

  TestFramework.test 'url_encode encodes spaces as %20' do
    result = HttpUtils.url_encode('hello world')
    TestFramework.assert_equal 'hello+world', result
  end

  TestFramework.test 'url_encode encodes special characters' do
    result = HttpUtils.url_encode('a+b=c&d?e')
    TestFramework.assert_equal 'a%2Bb%3Dc%26d%3Fe', result
  end

  TestFramework.test 'url_decode decodes encoded string' do
    result = HttpUtils.url_decode('hello+world')
    TestFramework.assert_equal 'hello world', result
  end

  TestFramework.test 'url_decode decodes special characters' do
    result = HttpUtils.url_decode('a%2Bb%3Dc%26d%3Fe')
    TestFramework.assert_equal 'a+b=c&d?e', result
  end

  TestFramework.test 'url_encode handles empty string' do
    result = HttpUtils.url_encode('')
    TestFramework.assert_equal '', result
  end

  TestFramework.test 'url_decode handles empty string' do
    result = HttpUtils.url_decode('')
    TestFramework.assert_equal '', result
  end

  puts "\n=== Query String Tests ==="

  TestFramework.test 'build_query_string builds from hash' do
    result = HttpUtils.build_query_string({ 'a' => '1', 'b' => '2' })
    TestFramework.assert result.include?('a=1')
    TestFramework.assert result.include?('b=2')
    TestFramework.assert result.include?('&')
  end

  TestFramework.test 'build_query_string encodes values' do
    result = HttpUtils.build_query_string({ 'key' => 'hello world' })
    TestFramework.assert_equal 'key=hello+world', result
  end

  TestFramework.test 'build_query_string handles empty hash' do
    result = HttpUtils.build_query_string({})
    TestFramework.assert_equal '', result
  end

  TestFramework.test 'build_query_string handles nil' do
    result = HttpUtils.build_query_string(nil)
    TestFramework.assert_equal '', result
  end

  TestFramework.test 'parse_query_string parses simple query' do
    result = HttpUtils.parse_query_string('a=1&b=2')
    TestFramework.assert_equal '1', result['a']
    TestFramework.assert_equal '2', result['b']
  end

  TestFramework.test 'parse_query_string handles empty string' do
    result = HttpUtils.parse_query_string('')
    TestFramework.assert_equal({}, result)
  end

  TestFramework.test 'parse_query_string handles nil' do
    result = HttpUtils.parse_query_string(nil)
    TestFramework.assert_equal({}, result)
  end

  puts "\n=== URL Building Tests ==="

  TestFramework.test 'build_url adds query to base URL' do
    result = HttpUtils.build_url('http://example.com', { 'a' => '1' })
    TestFramework.assert_equal 'http://example.com?a=1', result
  end

  TestFramework.test 'build_url appends to existing query' do
    result = HttpUtils.build_url('http://example.com?x=1', { 'a' => '2' })
    TestFramework.assert_equal 'http://example.com?x=1&a=2', result
  end

  TestFramework.test 'build_url returns base when no params' do
    result = HttpUtils.build_url('http://example.com', {})
    TestFramework.assert_equal 'http://example.com', result
  end

  puts "\n=== URL Parsing Tests ==="

  TestFramework.test 'parse_url extracts components' do
    result = HttpUtils.parse_url('https://example.com:8080/path?query=1#frag')
    TestFramework.assert_not_nil result
    TestFramework.assert_equal 'https', result[:scheme]
    TestFramework.assert_equal 'example.com', result[:host]
    TestFramework.assert_equal 8080, result[:port]
    TestFramework.assert_equal '/path', result[:path]
    TestFramework.assert_equal 'query=1', result[:query]
    TestFramework.assert_equal 'frag', result[:fragment]
  end

  TestFramework.test 'parse_url handles simple URL' do
    result = HttpUtils.parse_url('http://example.com')
    TestFramework.assert_not_nil result
    TestFramework.assert_equal 'http', result[:scheme]
    TestFramework.assert_equal 'example.com', result[:host]
  end

  TestFramework.test 'parse_url returns nil for invalid URL' do
    result = HttpUtils.parse_url('not a url')
    TestFramework.assert_nil result
  end

  puts "\n=== URL Validation Tests ==="

  TestFramework.test 'valid_url? returns true for http URL' do
    result = HttpUtils.valid_url?('http://example.com')
    TestFramework.assert_true result
  end

  TestFramework.test 'valid_url? returns true for https URL' do
    result = HttpUtils.valid_url?('https://example.com')
    TestFramework.assert_true result
  end

  TestFramework.test 'valid_url? returns false for invalid URL' do
    result = HttpUtils.valid_url?('not a url')
    TestFramework.assert_false result
  end

  TestFramework.test 'valid_url? returns false for ftp URL' do
    result = HttpUtils.valid_url?('ftp://example.com')
    TestFramework.assert_false result
  end

  puts "\n=== URL Component Extraction Tests ==="

  TestFramework.test 'get_domain extracts domain' do
    result = HttpUtils.get_domain('https://example.com/path')
    TestFramework.assert_equal 'example.com', result
  end

  TestFramework.test 'get_domain returns nil for invalid URL' do
    result = HttpUtils.get_domain('not a url')
    TestFramework.assert_nil result
  end

  TestFramework.test 'get_path extracts path' do
    result = HttpUtils.get_path('https://example.com/path/to/resource')
    TestFramework.assert_equal '/path/to/resource', result
  end

  TestFramework.test 'get_path returns nil for invalid URL' do
    result = HttpUtils.get_path('not a url')
    TestFramework.assert_nil result
  end

  puts "\n=== Options Class Tests ==="

  TestFramework.test 'Options has default values' do
    opts = HttpUtils::Options.new
    TestFramework.assert_equal({}, opts.headers)
    TestFramework.assert_equal 30, opts.timeout
    TestFramework.assert_equal true, opts.follow_redirects
    TestFramework.assert_equal 10, opts.max_redirects
    TestFramework.assert_equal true, opts.verify_ssl
  end

  TestFramework.test 'Options can be modified' do
    opts = HttpUtils::Options.new
    opts.timeout = 60
    opts.headers = { 'Authorization' => 'Bearer token' }
    TestFramework.assert_equal 60, opts.timeout
    TestFramework.assert_equal({ 'Authorization' => 'Bearer token' }, opts.headers)
  end

  puts "\n=== Response Class Tests ==="

  TestFramework.test 'Response stores all attributes' do
    response = HttpUtils::Response.new(
      status_code: 200,
      status_message: 'OK',
      headers: { 'Content-Type' => 'application/json' },
      body: '{"key":"value"}',
      url: 'https://example.com',
      response_time: 100
    )
    TestFramework.assert_equal 200, response.status_code
    TestFramework.assert_equal 'OK', response.status_message
    TestFramework.assert_equal '{"key":"value"}', response.body
    TestFramework.assert_equal 100, response.response_time
  end

  TestFramework.test 'success? returns true for 2xx status' do
    response = HttpUtils::Response.new(
      status_code: 200, status_message: 'OK', headers: {}, body: '', url: '', response_time: 0
    )
    TestFramework.assert_true response.success?
  end

  TestFramework.test 'success? returns false for 4xx status' do
    response = HttpUtils::Response.new(
      status_code: 404, status_message: 'Not Found', headers: {}, body: '', url: '', response_time: 0
    )
    TestFramework.assert_false response.success?
  end

  TestFramework.test 'success? returns false for 5xx status' do
    response = HttpUtils::Response.new(
      status_code: 500, status_message: 'Error', headers: {}, body: '', url: '', response_time: 0
    )
    TestFramework.assert_false response.success?
  end

  TestFramework.test 'json parses valid JSON' do
    response = HttpUtils::Response.new(
      status_code: 200, status_message: 'OK', headers: {},
      body: '{"key":"value"}', url: '', response_time: 0
    )
    TestFramework.assert_equal({ 'key' => 'value' }, response.json)
  end

  TestFramework.test 'json returns nil for invalid JSON' do
    response = HttpUtils::Response.new(
      status_code: 200, status_message: 'OK', headers: {},
      body: 'not json', url: '', response_time: 0
    )
    TestFramework.assert_nil response.json
  end

  TestFramework.test 'json? returns true for valid JSON' do
    response = HttpUtils::Response.new(
      status_code: 200, status_message: 'OK', headers: {},
      body: '{"key":"value"}', url: '', response_time: 0
    )
    TestFramework.assert_true response.json?
  end

  TestFramework.test 'json? returns false for invalid JSON' do
    response = HttpUtils::Response.new(
      status_code: 200, status_message: 'OK', headers: {},
      body: 'not json', url: '', response_time: 0
    )
    TestFramework.assert_false response.json?
  end

  TestFramework.test 'header finds header case-insensitively' do
    response = HttpUtils::Response.new(
      status_code: 200, status_message: 'OK',
      headers: { 'Content-Type' => 'application/json', 'X-Custom' => 'value' },
      body: '', url: '', response_time: 0
    )
    TestFramework.assert_equal 'application/json', response.header('content-type')
    TestFramework.assert_equal 'value', response.header('X-CUSTOM')
  end

  TestFramework.test 'header returns nil for missing header' do
    response = HttpUtils::Response.new(
      status_code: 200, status_message: 'OK', headers: {}, body: '', url: '', response_time: 0
    )
    TestFramework.assert_nil response.header('missing')
  end

  puts "\n=== Add Query Params Tests ==="

  TestFramework.test 'add_query_params is alias for build_url' do
    result = HttpUtils.add_query_params('http://example.com', { 'a' => '1' })
    TestFramework.assert_equal 'http://example.com?a=1', result
  end
end
