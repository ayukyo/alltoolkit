#!/usr/bin/perl
# HTTP Utilities Example
# Demonstrates usage of AllToolkit::HttpUtils

use strict;
use warnings;
use utf8;

use FindBin;
use lib "$FindBin::Bin/../http_utils";

use AllToolkit::HttpUtils qw(:all);

print "=" x 60 . "\n";
print "Perl HTTP Utilities - Usage Examples\n";
print "=" x 60 . "\n\n";

#==============================================================================
# Example 1: URL Encoding/Decoding
#==============================================================================

print "Example 1: URL Encoding/Decoding\n";
print "-" x 40 . "\n";

my $text = "hello world! special chars: + = & ?";
my $encoded = url_encode($text);
my $decoded = url_decode($encoded);

print "Original: $text\n";
print "Encoded:  $encoded\n";
print "Decoded:  $decoded\n\n";

#==============================================================================
# Example 2: Build Query String
#==============================================================================

print "Example 2: Build Query String\n";
print "-" x 40 . "\n";

my $params = {
    q => "perl programming",
    page => 1,
    limit => 20
};

my $query = build_query_string($params);
print "Query string: $query\n\n";

#==============================================================================
# Example 3: Build Full URL
#==============================================================================

print "Example 3: Build Full URL\n";
print "-" x 40 . "\n";

my $base_url = "https://api.example.com/search";
my $full_url = build_url($base_url, $params);
print "Base URL: $base_url\n";
print "Full URL: $full_url\n\n";

#==============================================================================
# Example 4: Parse URL
#==============================================================================

print "Example 4: Parse URL\n";
print "-" x 40 . "\n";

my $url_to_parse = "https://user:pass@api.example.com:8080/v1/users?page=1&limit=10#section";
my $parsed = parse_url($url_to_parse);

print "URL: $url_to_parse\n";
print "  Scheme:   $parsed->{scheme}\n";
print "  Host:     $parsed->{host}\n";
print "  Port:     $parsed->{port}\n";
print "  Path:     $parsed->{path}\n";
print "  Username: $parsed->{username}\n";
print "  Password: $parsed->{password}\n";
print "  Fragment: $parsed->{fragment}\n";
print "  Query params:\n";
for my $key (sort keys %{$parsed->{query_params}}) {
    print "    $key = $parsed->{query_params}{$key}\n";
}
print "\n";

#==============================================================================
# Example 5: URL Validation
#==============================================================================

print "Example 5: URL Validation\n";
print "-" x 40 . "\n";

my @urls = (
    "https://example.com",
    "http://localhost:3000",
    "not-a-valid-url",
    "ftp://files.example.com",
);

for my $test_url (@urls) {
    my $valid = is_valid_url($test_url) ? "Valid" : "Invalid";
    print "$test_url -> $valid\n";
}
print "\n";

#==============================================================================
# Example 6: JSON Encoding/Decoding
#==============================================================================

print "Example 6: JSON Encoding/Decoding\n";
print "-" x 40 . "\n";

my $user_data = {
    name => "John Doe",
    email => "john@example.com",
    age => 30,
    roles => ["admin", "user"]
};

my $json_string = json_encode($user_data);
print "JSON encoded:\n$json_string\n\n";

my $decoded_data = json_decode($json_string);
print "Decoded data:\n";
print "  Name:  $decoded_data->{name}\n";
print "  Email: $decoded_data->{email}\n";
print "  Age:   $decoded_data->{age}\n";
print "  Roles: " . join(", ", @{$decoded_data->{roles}}) . "\n\n";

#==============================================================================
# Example 7: Query Parameter Manipulation
#==============================================================================

print "Example 7: Query Parameter Manipulation\n";
print "-" x 40 . "\n";

my $original_url = "https://example.com?existing=value";
my $new_url = add_query_params($original_url, { new_param => "new_value" });
print "Original: $original_url\n";
print "With new: $new_url\n";

my $clean_url = remove_query_params($new_url, ["existing"]);
print "Removed:  $clean_url\n\n";

#==============================================================================
# Example 8: Domain and Path Extraction
#==============================================================================

print "Example 8: Domain and Path Extraction\n";
print "-" x 40 . "\n";

my $api_url = "https://api.github.com/users/octocat/repos";
print "URL: $api_url\n";
print "Domain: " . get_domain($api_url) . "\n";
print "Path:   " . get_path($api_url) . "\n\n";

#==============================================================================
# Example 9: HTTP Options
#==============================================================================

print "Example 9: HTTP Options\n";
print "-" x 40 . "\n";

my $http_options = AllToolkit::HttpOptions->new(
    timeout => 60,
    headers => {
        'Authorization' => 'Bearer token123',
        'X-API-Key' => 'secret'
    },
    follow_redirects => 1,
    max_redirects => 5,
    verify_ssl => 1
);

print "HTTP Options:\n";
print "  Timeout: $http_options->{timeout}s\n";
print "  Follow redirects: $http_options->{follow_redirects}\n";
print "  Max redirects: $http_options->{max_redirects}\n";
print "  Verify SSL: $http_options->{verify_ssl}\n";
print "  Headers:\n";
for my $key (keys %{$http_options->{headers}}) {
    print "    $key: $http_options->{headers}{$key}\n";
}
print "\n";

#==============================================================================
# Example 10: HTTP Response Object
#==============================================================================

print "Example 10: HTTP Response Object\n";
print "-" x 40 . "\n";

my $mock_response = AllToolkit::HttpResponse->new(
    status_code    => 200,
    status_message => 'OK',
    body           => '{"id": 1, "name": "Test User"}',
    headers        => {
        'Content-Type' => 'application/json',
        'X-Request-ID' => 'abc123'
    },
    url            => 'https://api.example.com/users/1',
    success        => 1,
    response_time  => 0.234
);

print "Response:\n";
print "  Status:  $mock_response->{status_code} $mock_response->{status_message}\n";
print "  Success: $mock_response->{success}\n";
print "  Time:    " . sprintf("%.3f", $mock_response->{response_time}) . "s\n";
print "  URL:     $mock_response->{url}\n";
print "  Body:    $mock_response->{body}\n";

if ($mock_response->is_json()) {
    my $data = $mock_response->json();
    print "  Parsed:  ID=$data->{id}, Name=$data->{name}\n";
}
print "\n";

#==============================================================================
# Example 11: Complete API Request Simulation
#==============================================================================

print "Example 11: Complete API Request Simulation\n";
print "-" x 40 . "\n";

print "# This would make an actual HTTP request:\n";
print "# my \$response = http_get('https://api.example.com/users');\n";
print "#\n";
print "# POST JSON data:\n";
print "# my \$response = http_post_json('https://api.example.com/users', {\n";
print "#     name => 'John',\n";
print "#     email => 'john\@example.com'\n";
print "# });\n";
print "#\n";
print "# POST Form data:\n";
print "# my \$response = http_post_form('https://api.example.com/login', {\n";
print "#     username => 'admin',\n";
print "#     password => 'secret'\n";
print "# });\n";
print "\n";

print "=" x 60 . "\n";
print "Examples completed!\n";
print "=" x 60 . "\n";
