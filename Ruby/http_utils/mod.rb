#!/usr/bin/env ruby
# frozen_string_literal: true

# HTTP Utilities for Ruby
# Zero dependencies - uses only Ruby standard library
#
# @author AllToolkit
# @version 1.0.0

require 'net/http'
require 'net/https'
require 'uri'
require 'json'
require 'cgi'

module AllToolkit
  # HTTP request/response utilities
  module HttpUtils
    # HTTP Response wrapper class
    class Response
      attr_reader :status_code, :status_message, :headers, :body, :url, :response_time

      def initialize(status_code:, status_message:, headers:, body:, url:, response_time:)
        @status_code = status_code
        @status_message = status_message
        @headers = headers
        @body = body
        @url = url
        @response_time = response_time
      end

      # Check if request was successful (2xx status code)
      # @return [Boolean] true if status code is 200-299
      def success?
        @status_code >= 200 && @status_code < 300
      end

      # Parse response body as JSON
      # @return [Hash, Array, nil] parsed JSON or nil if parsing fails
      def json
        JSON.parse(@body)
      rescue JSON::ParserError
        nil
      end

      # Check if response body is valid JSON
      # @return [Boolean] true if body is valid JSON
      def json?
        !json.nil?
      end

      # Get response header (case-insensitive)
      # @param name [String] header name
      # @return [String, nil] header value or nil
      def header(name)
        @headers.find { |k, _| k.downcase == name.downcase }&.last
      end
    end

    # HTTP Request options
    class Options
      attr_accessor :headers, :timeout, :follow_redirects, :max_redirects, :verify_ssl

      def initialize
        @headers = {}
        @timeout = 30
        @follow_redirects = true
        @max_redirects = 10
        @verify_ssl = true
      end
    end

    # Error class for HTTP operations
    class HttpError < StandardError
      attr_reader :response

      def initialize(message, response = nil)
        super(message)
        @response = response
      end
    end

    # ============================================================================
    # HTTP Methods
    # ============================================================================

    # Send GET request
    # @param url [String] request URL
    # @param options [Options, Hash] request options
    # @return [Response] HTTP response
    def self.get(url, options = nil)
      request(:get, url, nil, nil, options)
    end

    # Send POST request
    # @param url [String] request URL
    # @param body [String] request body
    # @param content_type [String] content type header
    # @param options [Options, Hash] request options
    # @return [Response] HTTP response
    def self.post(url, body = nil, content_type = nil, options = nil)
      request(:post, url, body, content_type, options)
    end

    # Send POST request with JSON data
    # @param url [String] request URL
    # @param data [Hash, Array] data to send as JSON
    # @param options [Options, Hash] request options
    # @return [Response] HTTP response
    def self.post_json(url, data, options = nil)
      post(url, data.to_json, 'application/json', options)
    end

    # Send POST request with form data
    # @param url [String] request URL
    # @param data [Hash] form data
    # @param options [Options, Hash] request options
    # @return [Response] HTTP response
    def self.post_form(url, data, options = nil)
      body = data.map { |k, v| "#{url_encode(k.to_s)}=#{url_encode(v.to_s)}" }.join('&')
      post(url, body, 'application/x-www-form-urlencoded', options)
    end

    # Send PUT request
    # @param url [String] request URL
    # @param body [String] request body
    # @param content_type [String] content type header
    # @param options [Options, Hash] request options
    # @return [Response] HTTP response
    def self.put(url, body = nil, content_type = nil, options = nil)
      request(:put, url, body, content_type, options)
    end

    # Send PUT request with JSON data
    # @param url [String] request URL
    # @param data [Hash, Array] data to send as JSON
    # @param options [Options, Hash] request options
    # @return [Response] HTTP response
    def self.put_json(url, data, options = nil)
      put(url, data.to_json, 'application/json', options)
    end

    # Send DELETE request
    # @param url [String] request URL
    # @param options [Options, Hash] request options
    # @return [Response] HTTP response
    def self.delete(url, options = nil)
      request(:delete, url, nil, nil, options)
    end

    # Send PATCH request
    # @param url [String] request URL
    # @param body [String] request body
    # @param content_type [String] content type header
    # @param options [Options, Hash] request options
    # @return [Response] HTTP response
    def self.patch(url, body = nil, content_type = nil, options = nil)
      request(:patch, url, body, content_type, options)
    end

    # Send HEAD request
    # @param url [String] request URL
    # @param options [Options, Hash] request options
    # @return [Response] HTTP response
    def self.head(url, options = nil)
      request(:head, url, nil, nil, options)
    end

    # ============================================================================
    # URL Utilities
    # ============================================================================

    # URL encode a string (spaces become %20)
    # @param str [String] string to encode
    # @return [String] encoded string
    def self.url_encode(str)
      CGI.escape(str.to_s)
    end

    # URL decode a string
    # @param str [String] string to decode
    # @return [String] decoded string
    def self.url_decode(str)
      CGI.unescape(str.to_s)
    end

    # Build query string from hash
    # @param params [Hash] parameters
    # @return [String] query string (without leading ?)
    def self.build_query_string(params)
      return '' if params.nil? || params.empty?

      params.map { |k, v| "#{url_encode(k.to_s)}=#{url_encode(v.to_s)}" }.join('&')
    end

    # Build URL with query parameters
    # @param base_url [String] base URL
    # @param params [Hash] query parameters
    # @return [String] complete URL
    def self.build_url(base_url, params = nil)
      return base_url if params.nil? || params.empty?

      query = build_query_string(params)
      separator = base_url.include?('?') ? '&' : '?'
      "#{base_url}#{separator}#{query}"
    end

    # Parse URL into components
    # @param url [String] URL to parse
    # @return [Hash] URL components
    def self.parse_url(url)
      uri = URI.parse(url)
      {
        scheme: uri.scheme,
        host: uri.host,
        port: uri.port,
        path: uri.path,
        query: uri.query,
        fragment: uri.fragment,
        userinfo: uri.userinfo
      }
    rescue URI::Error
      nil
    end

    # Parse query string into hash
    # @param query_string [String] query string
    # @return [Hash] parsed parameters
    def self.parse_query_string(query_string)
      return {} if query_string.nil? || query_string.empty?

      CGI.parse(query_string).transform_values { |v| v.length == 1 ? v.first : v }
    end

    # Validate URL format
    # @param url [String] URL to validate
    # @return [Boolean] true if valid
    def self.valid_url?(url)
      uri = URI.parse(url)
      uri.is_a?(URI::HTTP) || uri.is_a?(URI::HTTPS)
    rescue URI::Error
      false
    end

    # Extract domain from URL
    # @param url [String] URL
    # @return [String, nil] domain or nil
    def self.get_domain(url)
      parsed = parse_url(url)
      parsed ? parsed[:host] : nil
    end

    # Extract path from URL
    # @param url [String] URL
    # @return [String, nil] path or nil
    def self.get_path(url)
      parsed = parse_url(url)
      parsed ? parsed[:path] : nil
    end

    # Add query parameters to URL
    # @param url [String] base URL
    # @param params [Hash] parameters to add
    # @return [String] updated URL
    def self.add_query_params(url, params)
      build_url(url, params)
    end

    # ============================================================================
    # Private Methods
    # ============================================================================

    private

    # Internal request method
    def self.request(method, url, body = nil, content_type = nil, options = nil)
      opts = normalize_options(options)
      uri = URI.parse(url)

      start_time = Time.now

      http = Net::HTTP.new(uri.host, uri.port)
      http.use_ssl = uri.scheme == 'https'
      http.verify_mode = opts[:verify_ssl] ? OpenSSL::SSL::VERIFY_PEER : OpenSSL::SSL::VERIFY_NONE
      http.open_timeout = opts[:timeout]
      http.read_timeout = opts[:timeout]

      request_class = case method
                      when :get then Net::HTTP::Get
                      when :post then Net::HTTP::Post
                      when :put then Net::HTTP::Put
                      when :delete then Net::HTTP::Delete
                      when :patch then Net::HTTP::Patch
                      when :head then Net::HTTP::Head
                      else Net::HTTP::Get
                      end

      request = request_class.new(uri.request_uri)

      # Set content type
      request['Content-Type'] = content_type if content_type

      # Set custom headers
      opts[:headers].each { |k, v| request[k.to_s] = v.to_s } if opts[:headers]

      # Set body
      request.body = body if body

      response = http.request(request)
      response_time = ((Time.now - start_time) * 1000).round

      Response.new(
        status_code: response.code.to_i,
        status_message: response.message,
        headers: response.to_hash.transform_values { |v| v.first },
        body: response.body,
        url: url,
        response_time: response_time
      )
    rescue StandardError => e
      Response.new(
        status_code: 0,
        status_message: e.message,
        headers: {},
        body: '',
        url: url,
        response_time: 0
      )
    end

    # Normalize options to hash
    def self.normalize_options(options)
      return default_options if options.nil?
      return options.to_h if options.is_a?(Options)

      opts = default_options
      opts.merge!(options) if options.is_a?(Hash)
      opts
    end

    # Default options
    def self.default_options
      {
        headers: {},
        timeout: 30,
        follow_redirects: true,
        max_redirects: 10,
        verify_ssl: true
      }
    end
  end
end

# Convenience module for direct import
HttpUtils = AllToolkit::HttpUtils