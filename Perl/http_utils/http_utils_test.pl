#!/usr/bin/perl
# HTTP Utilities Test Suite
# Comprehensive tests for AllToolkit::HttpUtils

use strict;
use warnings;
use utf8;

use FindBin;
use lib "$FindBin::Bin";

use AllToolkit::HttpUtils qw(:all);

# Test counter
my $tests_run = 0;
my $tests_passed = 0;

#==============================================================================
# Test Helper Functions
#==============================================================================

sub test {
    my ($name, $condition) = @_;
    $tests_run++;
    if ($condition) {
        $tests_passed++;
        print "✓ PASS: $name\n";
    } else {
        print "✗ FAIL: $name\n";
    }
}

sub test_equal {
    my ($name, $got, $expected) = @_;
    test($name, defined($got) && defined($expected) && $got eq $expected);
}

sub test_true {
    my ($name, $value) = @_;
    test($name, $value);
}

sub test_false {
    my ($name, $value) = @_;
    test($name, !$value);
}

sub test_defined {
    my ($name, $value) = @_;
    test($name, defined($value));
}

sub test_undefined {
    my ($name, $value) = @_;
    test($name, !defined($value));
}

#==============================================================================
# URL Encoding/Decoding Tests
#==============================================================================

print "\n=== URL Encoding/Decoding Tests ===
";

test_equal("url_encode: simple string", 
    url_encode("hello world"), "hello%20world");

test_equal("url_encode: special characters", 
    url_encode("a+b=c"), "a%2Bb%3Dc");

test_equal("url_encode: empty string", 
    url_encode(""), "");

test_equal("url_encode: undef returns empty", 
    url_encode(undef), "");

test_equal("url_decode: simple encoded", 
    url_decode("hello%20world"), "hello world");

test_equal("url_decode: special characters", 
    url_decode("a%2Bb%3Dc"), "a+b=c");

test_equal("url_decode: empty string", 
    url_decode(""), "");

#==============================================================================
# Query String Tests
#==============================================================================

print "\n=== Query String Tests ===
";

test_equal("build_query_string: simple params",
    build_query_string({ a => 1, b => 2 }), "a=1&b=2");

test_equal("build_query_string: with spaces",
    build_query_string({ q => "hello world" }), "q=hello%20world");

test_equal("build_query_string: empty hash",
    build_query_string({}), "");

test_equal("build_query_string: undef returns empty",
    build_query_string(undef), "");

#==============================================================================
# URL Building Tests
#==============================================================================

print "\n=== URL Building Tests ===
";

test_equal("build_url: add params to base",
    build_url("https://example.com", { a => 1 }),
    "https://example.com?a=1");

test_equal("build_url: add to existing query",
    build_url("https://example.com?x=1", { y => 2 }),
    "https://example.com?x=1&y=2");

test_equal("build_url: empty params",
    build_url("https://example.com", {}),
    "https://example.com");

#==============================================================================
# URL Validation Tests
#==============================================================================

print "\n=== URL Validation Tests ===
";

test_true("is_valid_url: valid http URL",
    is_valid_url("http://example.com"));

test_true("is_valid_url: valid https URL",
    is_valid_url("https://example.com"));

test_true("is_valid_url: URL with path",
    is_valid_url("https://example.com/path"));

test_false("is_valid_url: invalid URL (no scheme)",
    is_valid_url("example.com"));

test_false("is_valid_url: invalid URL (no host)",
    is_valid_url("http://"));

test_false("is_valid_url: empty string",
    is_valid_url(""));

test_false("is_valid_url: undef",
    is_valid_url(undef));

#==============================================================================
# URL Parsing Tests
#==============================================================================

print "\n=== URL Parsing Tests ===
";

my $parsed = parse_url("https://example.com:8080/path?a=1&b=2#section");
test_defined("parse_url: returns hash ref", $parsed);
test_equal("parse_url: scheme", $parsed->{scheme}, "https");
test_equal("parse_url: host", $parsed->{host}, "example.com");
test_equal("parse_url: port", $parsed->{port}, 8080);
test_equal("parse_url: path", $parsed->{path}, "/path");
test_equal("parse_url: fragment", $parsed->{fragment}, "section");

my $query_params = $parsed->{query_params};
test_defined("parse_url: query_params exists", $query_params);
test_equal("parse_url: query param a", $query_params->{a}, "1");
test_equal("parse_url: query param b", $query_params->{b}, "2");

# Test URL with auth
$parsed = parse_url("https://user:pass@example.com/path");
test_equal("parse_url: username", $parsed->{username}, "user");
test_equal("parse_url: password", $parsed->{password}, "pass");

test_undefined("parse_url: invalid URL returns undef",
    parse_url("not-a-url"));

#==============================================================================
# Domain/Path Extraction Tests
#==============================================================================

print "\n=== Domain/Path Extraction Tests ===
";

test_equal("get_domain: extract domain",
    get_domain("https://api.example.com/v1/users"), "api.example.com");

test_equal("get_path: extract path",
    get_path("https://example.com/path/to/resource"), "/path/to/resource");

test_undefined("get_domain: invalid URL returns undef",
    get_domain("not-a-url"));

#==============================================================================
# JSON Tests
#==============================================================================

print "\n=== JSON Tests ===
";

my $data = { name => "John", age => 30 };
my $json = json_encode($data);
test_defined("json_encode: returns string", $json);
test_true("json_encode: contains name", index($json, '"name"') >= 0);
test_true("json_encode: contains John", index($json, '"John"') >= 0);

my $decoded = json_decode($json);
test_defined("json_decode: returns data", $decoded);
test_equal("json_decode: name field", $decoded->{name}, "John");
test_equal("json_decode: age field", $decoded->{age}, 30);

test_undefined("json_decode: invalid JSON returns undef",
    json_decode("not valid json"));

test_undefined("json_encode: undef returns undef",
    json_encode(undef));

# Test array encoding
my $arr = [1, 2, 3];
$json = json_encode($arr);
test_true("json_encode: array contains 1", index($json, '1') >= 0);

#==============================================================================
# Query Parameter Manipulation Tests
#==============================================================================

print "\n=== Query Parameter Manipulation Tests ===
";

my $url = add_query_params("https://example.com", { a => 1, b => 2 });
test_true("add_query_params: adds params",
    index($url, "a=1") >= 0 && index($url, "b=2") >= 0);

$url = remove_query_params("https://example.com?a=1&b=2&c=3", ["b"]);
test_true("remove_query_params: removes param",
    index($url, "b=2") < 0);
 Tests ===
";

my $options = AllToolkit::HttpOptions->new();
test_defined("HttpOptions: created", $options);
test_equal("HttpOptions: default timeout", $options->timeout, 30);
test_true("HttpOptions: follow_redirects default", $options->follow_redirects);
test_true("HttpOptions: verify_ssl default", $options->verify_ssl);

$options = AllToolkit::HttpOptions->new(
    timeout => 60,
    headers => { 'X-Custom' => 'value' }
);
test_equal("HttpOptions: custom timeout", $options->timeout, 60);
test_defined("HttpOptions: custom header", $options->headers->{'X-Custom'});

$options->add_header('Authorization', 'Bearer token');
test_equal("HttpOptions: added header", $options->headers->{'Authorization'}, 'Bearer token');

#==============================================================================
# HTTP Response Tests (Mock)
#==============================================================================

print "\n=== HTTP Response Tests ===
";

my $response = AllToolkit::HttpResponse->new(
    status_code    => 200,
    status_message => 'OK',
    body           => '{"success": true}',
    headers        => { 'Content-Type' => 'application/json' },
    url            => 'https://example.com/api',
    success        => 1,
    response_time  => 0.123,
);

test_equal("HttpResponse: status_code", $response->status_code, 200);
test_equal("HttpResponse: status_message", $response->status_message, 'OK');
test_equal("HttpResponse: body", $response->body, '{"success": true}');
test_equal("HttpResponse: url", $response->url, 'https://example.com/api');
test_true("HttpResponse: success", $response->success);
test_equal("HttpResponse: header", $response->header('Content-Type'), 'application/json');
test_equal("HttpResponse: header case insensitive", $response->header('content-type'), 'application/json');

my $json_data = $response->json();
test_defined("HttpResponse: json parsed", $json_data);
test_true("HttpResponse: is_json", $response->is_json());

$response = AllToolkit::HttpResponse->new(
    status_code => 404,
    success     => 0,
);
test_false("HttpResponse: not success for 404", $response->success);

#==============================================================================
# Summary
#==============================================================================

print "\n" . '=' x 50 . "\n";
print "Test Summary\n";
print '=' x 50 . "\n";
printf("Total:  %d\n", $tests_run);
printf("Passed: %d\n", $tests_passed);
printf("Failed: %d\n", $tests_run - $tests_passed);

if ($tests_passed == $tests_run) {
    print "\n✓ All tests passed!\n";
    exit 0;
} else {
    print "\n✗ Some tests failed!\n";
    exit 1;
}
