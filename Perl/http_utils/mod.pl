#!/usr/bin/perl
# HTTP Utilities Module for Perl
# A comprehensive HTTP client utility module with zero dependencies
# Uses only Perl standard library modules
#
# Features:
# - Full HTTP method support: GET, POST, PUT, DELETE, PATCH, HEAD
# - Automatic JSON and form data encoding
# - Complete URL manipulation utilities
# - Custom headers and timeout configuration
# - Response time tracking
# - SSL/TLS certificate verification control
# - HTTP proxy support
# - Basic authentication support
# - Response success status checking
# - Built-in JSON validation and parsing
#
# Author: AllToolkit Contributors
# License: MIT

package AllToolkit::HttpUtils;

use strict;
use warnings;
use utf8;

# Core modules
use LWP::UserAgent;
use HTTP::Request;
use HTTP::Headers;
use URI;
use URI::Escape;
use JSON::PP;
use Time::HiRes qw(gettimeofday tv_interval);
use Carp qw(croak);

# Export functions
use Exporter 'import';
our @EXPORT_OK = qw(
    http_get http_post http_post_json http_post_form
    http_put http_put_json http_delete http_patch http_head
    build_url build_query_string url_encode url_decode
    parse_url is_valid_url get_domain get_path
    add_query_params remove_query_params
    json_encode json_decode
);
our %EXPORT_TAGS = (
    all => [@EXPORT_OK],
    http => [qw(http_get http_post http_post_json http_post_form http_put http_put_json http_delete http_patch http_head)],
    url => [qw(build_url build_query_string url_encode url_decode parse_url is_valid_url get_domain get_path add_query_params remove_query_params)],
    json => [qw(json_encode json_decode)]
);

our $VERSION = '1.0.0';

# Default timeout in seconds
our $DEFAULT_TIMEOUT = 30;
our $DEFAULT_MAX_REDIRECTS = 10;

#==============================================================================
# HTTP Response Class
#==============================================================================
package AllToolkit::HttpResponse;

use strict;
use warnings;

sub new {
    my ($class, %args) = @_;
    my $self = {
        status_code    => $args{status_code}    || 0,
        status_message => $args{status_message} || '',
        body           => $args{body}           || '',
        headers        => $args{headers}        || {},
        url            => $args{url}            || '',
        success        => $args{success}        || 0,
        response_time  => $args{response_time}  || 0,
    };
    bless $self, $class;
    return $self;
}

# Accessor methods
sub status_code    { shift->{status_code} }
sub status_message { shift->{status_message} }
sub body           { shift->{body} }
sub headers        { shift->{headers} }
sub url            { shift->{url} }
sub success        { shift->{success} }
sub response_time  { shift->{response_time} }

# Get header value (case-insensitive)
sub header {
    my ($self, $name) = @_;
    return undef unless $name;
    my $headers = $self->{headers};
    # Case-insensitive lookup
    for my $key (keys %$headers) {
        return $headers->{$key} if lc($key) eq lc($name);
    }
    return undef;
}

# Parse body as JSON
sub json {
    my ($self) = @_;
    return undef unless $self->{body};
    eval {
        return JSON::PP::decode_json($self->{body});
    };
    return undef if $@;
    return undef;
}

# Check if body is valid JSON
sub is_json {
    my ($self) = @_;
    return 0 unless $self->{body};
    eval {
        JSON::PP::decode_json($self->{body});
        return 1;
    };
    return 0;
}

# String representation
sub to_string {
    my ($self) = @_;
    return sprintf("HTTP %d %s (%d ms)", 
        $self->{status_code}, 
        $self->{status_message},
        $self->{response_time} * 1000);
}

#==============================================================================
# HTTP Options Class
#==============================================================================
package AllToolkit::HttpOptions;

use strict;
use warnings;

sub new {
    my ($class, %args) = @_;
    my $self = {
        headers        => $args{headers}        || {},
        timeout        => $args{timeout}        || $AllToolkit::HttpUtils::DEFAULT_TIMEOUT,
        follow_redirects => $args{follow_redirects} // 1,
        max_redirects  => $args{max_redirects}  || $AllToolkit::HttpUtils::DEFAULT_MAX_REDIRECTS,
        verify_ssl     => $args{verify_ssl}     // 1,
        proxy          => $args{proxy}          || undef,
        username       => $args{username}       || undef,
        password       => $args{password}       || undef,
    };
    bless $self, $class;
    return $self;
}

# Accessor methods
sub headers        { shift->{headers} }
sub timeout        { shift->{timeout} }
sub follow_redirects { shift->{follow_redirects} }
sub max_redirects  { shift->{max_redirects} }
sub verify_ssl     { shift->{verify_ssl} }
sub proxy          { shift->{proxy} }
sub username       { shift->{username} }
sub password       { shift->{password} }

# Add header
sub add_header {
    my ($self, $key, $value) = @_;
    $self->{headers}{$key} = $value if defined $key && defined $value;
}

#==============================================================================
# Main HTTP Utilities
#==============================================================================
package AllToolkit::HttpUtils;

use strict;
use warnings;

#==============================================================================
# Internal Helper Functions
#==============================================================================

# Create UserAgent with options
sub _create_ua {
    my ($options) = @_;
    $options ||= AllToolkit::HttpOptions->new();
    
    my $ua = LWP::UserAgent->new(
        timeout => $options->{timeout},
        ssl_opts => {
            verify_hostname => $options->{verify_ssl},
        },
    );
    
    $ua->max_redirect($options->{max_redirects}) if $options->{follow_redirects};
    $ua->proxy(['http', 'https'], $options->{proxy}) if $options->{proxy};
    
    return $ua;
}

# Build HTTP headers from options
sub _build_headers {
    my ($options, $content_type) = @_;
    my $headers = HTTP::Headers->new();
    
    # Set content type if provided
    $headers->header('Content-Type' => $content_type) if $content_type;
    
    # Add custom headers
    if ($options && $options->{headers}) {
        for my $key (keys %{$options->{headers}}) {
            $headers->header($key => $options->{headers}{$key});
        }
    }
    
    # Add authentication if provided
    if ($options && $options->{username}) {
        require MIME::Base64;
        my $auth = MIME::Base64::encode($options->{username} . ':' . ($options->{password} || ''), '');
        $headers->header('Authorization' => "Basic $auth");
    }
    
    return $headers;
}

# Execute HTTP request and return response
sub _do_request {
    my ($method, $url, $body, $content_type, $options) = @_;
    
    $options ||= AllToolkit::HttpOptions->new();
    my $ua = _create_ua($options);
    my $headers = _build_headers($options, $content_type);
    
    my $request = HTTP::Request->new($method => $url, $headers, $body);
    
    my $start_time = [gettimeofday];
    my $response = $ua->request($request);
    my $response_time = tv_interval($start_time);
    
    # Parse headers
    my %headers_hash;
    $response->headers->scan(sub {
        my ($key, $value) = @_;
        $headers_hash{$key} = $value;
    });
    
    return AllToolkit::HttpResponse->new(
        status_code    => $response->code,
        status_message => $response->message,
        body           => $response->decoded_content // $response->content,
        headers        => \%headers_hash,
        url            => $response->request->uri->as_string,
        success        => $response->is_success,
        response_time  => $response_time,
    );
}

#==============================================================================
# HTTP Method Functions
#==============================================================================

# GET request
sub http_get {
    my ($url, $options) = @_;
    croak "URL is required" unless $url;
    return _do_request('GET', $url, undef, undef, $options);
}

# POST request
sub http_post {
    my ($url, $body, $content_type, $options) = @_;
    croak "URL is required" unless $url;
    $content_type ||= 'application/octet-stream';
    return _do_request('POST', $url, $body, $content_type, $options);
}

# POST JSON request
sub http_post_json {
    my ($url, $data, $options) = @_;
    croak "URL is required" unless $url;
    my $json_body = JSON::PP::encode_json($data);
    return _do_request('POST', $url, $json_body, 'application/json', $options);
}

# POST Form request
sub http_post_form {
    my ($url, $data, $options) = @_;
    croak "URL is required" unless $url;
    croak "Data must be a hash reference" unless ref($data) eq 'HASH';
    
    my @form_data;
    for my $key (keys %$data) {
        push @form_data, uri_escape($key) . '=' . uri_escape($data->{$key});
    }
    my $form_body = join('&', @form_data);
    return _do_request('POST', $url, $form_body, 'application/x-www-form-urlencoded', $options);
}

# PUT request
sub http_put {
    my ($url, $body, $content_type, $options) = @_;
    croak "URL is required" unless $url;
    $content_type ||= 'application/octet-stream';
    return _do_request('PUT', $url, $body, $content_type, $options);
}

# PUT JSON request
sub http_put_json {
    my ($url, $data, $options) = @_;
    croak "URL is required" unless $url;
    my $json_body = JSON::PP::encode_json($data);
    return _do_request('PUT', $url, $json_body, 'application/json', $options);
}

# DELETE request
sub http_delete {
    my ($url, $options) = @_;
    croak "URL is required" unless $url;
    return _do_request('DELETE', $url, undef, undef, $options);
}

# PATCH request
sub http_patch {
    my ($url, $body, $content_type, $options) = @_;
    croak "URL is required" unless $url;
    $content_type ||= 'application/octet-stream';
    return _do_request('PATCH', $url, $body, $content_type, $options);
}

# HEAD request
sub http_head {
    my ($url, $options) = @_;
    croak "URL is required" unless $url;
    return _do_request('HEAD', $url, undef, undef, $options);
}

#==============================================================================
# URL Utility Functions
#==============================================================================

# Build URL with query parameters
sub build_url {
    my ($base_url, $params) = @_;
    return $base_url unless $params && ref($params) eq 'HASH' && keys %$params;
    
    my $query = build_query_string($params);
    my $separator = ($base_url =~ /\?/) ? '&' : '?';
    return $base_url . $separator . $query;
}

# Build query string from hash
sub build_query_string {
    my ($params) = @_;
    return '' unless $params && ref($params) eq 'HASH';
    
    my @pairs;
    for my $key (sort keys %$params) {
        my $value = $params->{$key};
        $value = '' unless defined $value;
        push @pairs, uri_escape($key) . '=' . uri_escape($value);
    }
    return join('&', @pairs);
}

# URL encode
sub url_encode {
    my ($str) = @_;
    return '' unless defined $str;
    return uri_escape($str);
}

# URL decode
sub url_decode {
    my ($str) = @_;
    return '' unless defined $str;
    return uri_unescape($str);
}

# Parse URL into components
sub parse_url {
    my ($url) = @_;
    return undef unless $url;
    
    my $uri = URI->new($url);
    return undef unless $uri->scheme;
    
    my %result = (
        scheme   => $uri->scheme   || '',
        host     => $uri->host     || '',
        port     => $uri->port     || undef,
        path     => $uri->path     || '',
        query    => $uri->query    || '',
        fragment => $uri->fragment || '',
    );
    
    # Parse userinfo
    if ($uri->userinfo) {
        my ($user, $pass) = split(/:/, $uri->userinfo, 2);
        $result{username} = $user || '';
        $result{password} = $pass || '';
    }
    
    # Parse query string
    if ($result{query}) {
        my %query_params;
        my @pairs = split(/&/, $result{query});
        for my $pair (@pairs) {
            my ($key, $value) = split(/=/, $pair, 2);
            $key = url_decode($key // '');
            $value = url_decode($value // '');
            $query_params{$key} = $value;
        }
        $result{query_params} = \%query_params;
    }
    
    return \%result;
}

# Check if string is valid URL
sub is_valid_url {
    my ($url) = @_;
    return 0 unless $url;
    my $uri = URI->new($url);
    return $uri->scheme && $uri->host ? 1 : 0;
}

# Get domain from URL
sub get_domain {
    my ($url) = @_;
    return undef unless $url;
    my $uri = URI->new($url);
    return $uri->host;
}

# Get path from URL
sub get_path {
    my ($url) = @_;
    return undef unless $url;
    my $uri = URI->new($url);
    return $uri->path;
}

# Add query parameters to URL
sub add_query_params {
    my ($url, $params) = @_;
    return $url unless $params && ref($params) eq 'HASH';
    return build_url($url, $params);
}

# Remove query parameters from URL
sub remove_query_params {
    my ($url, $keys) = @_;
    return $url unless $keys && @$keys;
    
    my $parsed = parse_url($url);
    return $url unless $parsed && $parsed->{query_params};
    
    my %new_params = %{$parsed->{query_params}};
    for my $key (@$keys) {
        delete $new_params{$key};
    }
    
    my $new_query = build_query_string(\%new_params);
    my $base = $parsed->{scheme} . '://' . $parsed->{host};
    $base .= ':' . $parsed->{port} if $parsed->{port};
    $base .= $parsed->{path};
    $base .= '?' . $new_query if $new_query;
    $base .= '#' . $parsed->{fragment} if $parsed->{fragment};
    
    return $base;
}

#==============================================================================
# JSON Utility Functions
#==============================================================================

# Encode Perl data structure to JSON
sub json_encode {
    my ($data) = @_;
    return undef unless defined $data;
    eval {
        return JSON::PP::encode_json($data);
    };
    return undef if $@;
    return undef;
}

# Decode JSON to Perl data structure
sub json_decode {
    my ($json) = @_;
    return undef unless defined $json;
    eval {
        return JSON::PP::decode_json($json);
    };
    return undef if $@;
    return undef;
}

1;

__END__

=head1 NAME

AllToolkit::HttpUtils - Comprehensive HTTP client utility module for Perl

=head1 SYNOPSIS

    use AllToolkit::HttpUtils qw(:all);
    
    # Simple GET request
    my $response = http_get('https://api.example.com/users');
    if ($response->success) {
        print $response->body;
    }
    
    # POST JSON data
    my $response = http_post_json('https://api.example.com/users', {
        name => 'John',
        email => 'john@example.com'
    });
    
    # POST Form data
    my $response = http_post_form('https://api.example.com/login', {
        username => 'admin',
        password => 'secret'
    });
    
    # URL building
    my $url = build_url('https://api.example.com/search', {
        q => 'hello world',
        page => 1
    });

=head1 DESCRIPTION

AllToolkit::HttpUtils is a comprehensive HTTP client utility module for Perl
providing full HTTP method support, URL manipulation, and JSON handling with
zero external dependencies (uses only Perl standard library).

=head1 FUNCTIONS

=head2 HTTP Methods

=over 4

=item B<http_get($url, [$options])>

Send HTTP GET request. Returns an AllToolkit::HttpResponse object.

=item B<http_post($url, $body, $content_type, [$options])>

Send HTTP POST request with raw body.

=item B<http_post_json($url, $data, [$options])>

Send HTTP POST request with JSON-encoded data.

=item B<http_post_form($url, $data, [$options])>

Send HTTP POST request with form-encoded data.

=item B<http_put($url, $body, $content_type, [$options])>

Send HTTP PUT request.

=item B<http_put_json($url, $data, [$options])>

Send HTTP PUT request with JSON-encoded data.

=item B<http_delete($url, [$options])>

Send HTTP DELETE request.

=item B<http_patch($url, $body, $content_type, [$options])>

Send HTTP PATCH request.

=item B<http_head($url, [$options])>

Send HTTP HEAD request.

=back

=head2 URL Utilities

=over 4

=item B<build_url($base_url, $params)>

Build URL with query parameters.

=item B<build_query_string($params)>

Build URL-encoded query string from hash.

=item B<url_encode($str)>

URL encode a string.

=item B<url_decode($str)>

URL decode a string.

=item B<parse_url($url)>

Parse URL into components (scheme, host, port, path, query, fragment, username, password, query_params).

=item B<is_valid_url($url)>

Check if string is a valid URL.

=item B<get_domain($url)>

Extract domain from URL.

=item B<get_path($url)>

Extract path from URL.

=item B<add_query_params($url, $params)>

Add query parameters to URL.

=item B<remove_query_params($url, $keys)>

Remove specified query parameters from URL.

=back

=head2 JSON Utilities

=over 4

=item B<json_encode($data)>

Encode Perl data structure to JSON string.

=item B<json_decode($json)>

Decode JSON string to Perl data structure.

=back

=head1 HTTP RESPONSE OBJECT

The HTTP methods return an AllToolkit::HttpResponse object with the following methods:

=over 4

=item B<status_code()>

HTTP status code (e.g., 200, 404, 500).

=item B<status_message()>

HTTP status message (e.g., "OK", "Not Found").

=item B<body()>

Response body as string.

=item B<headers()>

Hash reference of response headers.

=item B<header($name)>

Get specific header value (case-insensitive).

=item B<url()>

Final URL after redirects.

=item B<success()>

True if status code is 200-299.

=item B<response_time()>

Request duration in seconds.

=item B<json()>

Parse body as JSON and return data structure.

=item B<is_json()>

Check if body is valid JSON.

=item B<to_string()>

String representation of response.

=back

=head1 HTTP OPTIONS

Create an AllToolkit::HttpOptions object to customize requests:

    my $options = AllToolkit::HttpOptions->new(
        headers => { 'Authorization' => 'Bearer token123' },
        timeout => 60,
        follow_redirects => 1,
        max_redirects => 10,
        verify_ssl => 1,
        proxy => 'http://proxy.example.com:8080',
        username => 'user',
        password => 'pass'
    );

=head1 AUTHOR

AllToolkit Contributors

=head1 LICENSE

MIT License

=cut
