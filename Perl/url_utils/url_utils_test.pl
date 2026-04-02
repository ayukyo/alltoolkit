#!/usr/bin/perl
# URL Utilities Test Suite
# 使用 Perl 标准测试框架

use strict;
use warnings;
use utf8;
use FindBin;
use lib "$FindBin::Bin";
use mod;

# 测试计数器
my $tests_run = 0;
my $tests_passed = 0;
my $tests_failed = 0;

# 测试辅助函数
sub test {
    my ($name, $condition) = @_;
    $tests_run++;
    if ($condition) {
        print "✓ $name\n";
        $tests_passed++;
    } else {
        print "✗ $name\n";
        $tests_failed++;
    }
}

sub test_eq {
    my ($name, $got, $expected) = @_;
    $tests_run++;
    if ($got eq $expected) {
        print "✓ $name\n";
        $tests_passed++;
    } else {
        print "✗ $name\n";
        print "  Expected: $expected\n";
        print "  Got:      $got\n";
        $tests_failed++;
    }
}

sub test_hash_eq {
    my ($name, $got, $expected) = @_;
    $tests_run++;
    my $match = 1;
    foreach my $key (keys %$expected) {
        if (!exists $got->{$key} || $got->{$key} ne $expected->{$key}) {
            $match = 0;
            last;
        }
    }
    if ($match) {
        print "✓ $name\n";
        $tests_passed++;
    } else {
        print "✗ $name\n";
        $tests_failed++;
    }
}

print "=" x 50 . "\n";
print "URL Utilities Test Suite\n";
print "=" x 50 . "\n\n";

# ==================== URL 编码测试 ====================
print "Testing url_encode...\n";
test_eq("url_encode: simple string", url_encode("hello"), "hello");
test_eq("url_encode: with space", url_encode("hello world"), "hello%20world");
test_eq("url_encode: special chars", url_encode("a+b=c"), "a%2Bb%3Dc");
test_eq("url_encode: empty string", url_encode(""), "");
test_eq("url_encode: undefined", url_encode(undef), "");

# ==================== URL 解码测试 ====================
print "\nTesting url_decode...\n";
test_eq("url_decode: simple string", url_decode("hello"), "hello");
test_eq("url_decode: encoded space", url_decode("hello%20world"), "hello world");
test_eq("url_decode: special chars", url_decode("a%2Bb%3Dc"), "a+b=c");
test_eq("url_decode: mixed case", url_decode("Hello%20World"), "Hello World");

# ==================== 编码解码对称性测试 ====================
print "\nTesting encode/decode symmetry...\n";
my $original = "Hello World! @#$%^&*()";
my $encoded = url_encode($original);
my $decoded = url_decode($encoded);
test_eq("encode/decode symmetry", $decoded, $original);

# ==================== 查询字符串解析测试 ====================
print "\nTesting parse_query_string...\n";
my $params1 = parse_query_string("a=1&b=2");
test_hash_eq("parse_query_string: simple", $params1, { a => "1", b => "2" });

my $params2 = parse_query_string("?a=1&b=2");
test_hash_eq("parse_query_string: with leading ?", $params2, { a => "1", b => "2" });

my $params3 = parse_query_string("name=John%20Doe");
test_eq("parse_query_string: decoded value", $params3->{name}, "John Doe");

my $params4 = parse_query_string("");
test("parse_query_string: empty", keys %$params4 == 0);

# ==================== 查询字符串构建测试 ====================
print "\nTesting build_query_string...\n";
test_eq("build_query_string: simple", 
    build_query_string({ a => 1, b => 2 }), 
    "a=1&b=2");

test_eq("build_query_string: with space", 
    build_query_string({ name => "John Doe" }), 
    "name=John%20Doe");

my $qs_sorted = build_query_string({ z => 1, a => 2, m => 3 }, { sort => 1 });
test("build_query_string: sorted", $qs_sorted =~ /^a=2/);

# ==================== URL 解析测试 ====================
print "\nTesting parse_url...\n";
my $parsed1 = parse_url("https://example.com/path?a=1#anchor");
test_eq("parse_url: scheme", $parsed1->{scheme}, "https");
test_eq("parse_url: host", $parsed1->{host}, "example.com");
test_eq("parse_url: path", $parsed1->{path}, "/path");
test_eq("parse_url: query", $parsed1->{query}, "a=1");
test_eq("parse_url: fragment", $parsed1->{fragment}, "anchor");

my $parsed2 = parse_url('https://user:pass@example.com:8080/path');
test_eq("parse_url: userinfo", $parsed2->{userinfo}, 'user:pass');
test_eq("parse_url: port", $parsed2->{port}, '8080');

# ==================== URL 构建测试 ====================
print "\nTesting build_url...\n";
my $url1 = build_url({
    scheme => 'https',
    host   => 'example.com',
    path   => '/path',
    query  => { a => 1 }
});
test_eq("build_url: simple", $url1, "https://example.com/path?a=1");

my $url2 = build_url({
    scheme   => 'https',
    host     => 'example.com',
    fragment => 'section'
});
test_eq("build_url: with fragment", $url2, "https://example.com#section");

# ==================== URL 验证测试 ====================
print "\nTesting is_valid_url...\n";
test("is_valid_url: https", is_valid_url("https://example.com"));
test("is_valid_url: http", is_valid_url("http://example.com"));
test("is_valid_url: with path", is_valid_url("https://example.com/path"));
test("is_valid_url: with query", is_valid_url("https://example.com?a=1"));
test("is_valid_url: invalid (no false positive)", !is_valid_url("not a url"));
test("is_valid_url: empty invalid", !is_valid_url(""));

# ==================== 域名提取测试 ====================
print "\nTesting get_domain...\n";
test_eq("get_domain: simple", get_domain("https://example.com/path"), "example.com");
test_eq("get_domain: with www", get_domain("https://www.example.com"), "www.example.com");
test_eq("get_domain: with port", get_domain("https://example.com:8080"), "example.com");

# ==================== 路径提取测试 ====================
print "\nTesting get_path...\n";
test_eq("get_path: simple", get_path("https://example.com/path"), "/path");
test_eq("get_path: with query", get_path("https://example.com/path?a=1"), "/path");
test_eq("get_path: root", get_path("https://example.com"), "");

# ==================== 添加参数测试 ====================
print "\nTesting add_query_params...\n";
my $new_url1 = add_query_params("https://example.com/path", { a => 1 });
test_eq("add_query_params: to plain URL", $new_url1, "https://example.com/path?a=1");

my $new_url2 = add_query_params("https://example.com/path?a=1", { b => 2 });
test("add_query_params: to URL with params", $new_url2 =~ /a=1/ && $new_url2 =~ /b=2/);

# ==================== 移除参数测试 ====================
print "\nTesting remove_query_params...\n";
my $removed1 = remove_query_params("https://example.com?a=1&b=2", ["a"]);
test_eq("remove_query_params: remove one", $removed1, "https://example.com?b=2");

my $removed2 = remove_query_params("https://example.com?a=1", ["a"]);
test_eq("remove_query_params: remove all", $removed2, "https://example.com");

# ==================== URL 规范化测试 ====================
print "\nTesting normalize_url...\n";
test_eq("normalize_url: lowercase scheme", normalize_url("HTTPS://example.com"), "https://example.com");
test_eq("normalize_url: lowercase host", normalize_url("https://EXAMPLE.COM"), "https://example.com");

# 移除默认端口测试
my $norm1 = normalize_url("https://example.com:443/path");
test("normalize_url: remove default https port", $norm1 !~ /:443/);

my $norm2 = normalize_url("http://example.com:80/path");
test("normalize_url: remove default http port", $norm2 !~ /:80/);

# ==================== 测试结果汇总 ====================
print "\n" . "=" x 50 . "\n";
print "Test Results: $tests_passed/$tests_run passed\n";
if ($tests_failed > 0) {
    print "FAILED: $tests_failed tests\n";
    exit 1;
} else {
    print "All tests passed!\n";
    exit 0;
}
