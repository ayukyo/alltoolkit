#!/usr/bin/perl
# URL Utilities Example
# 展示 URL 工具模块的各种用法

use strict;
use warnings;
use utf8;
use FindBin;
use lib "$FindBin::Bin/../url_utils";
use mod;

print "=" x 60 . "\n";
print "URL Utilities Example - Perl\n";
print "=" x 60 . "\n\n";

# ==================== 1. URL 编码与解码 ====================
print "1. URL 编码与解码\n";
print "-" x 40 . "\n";

my $text = "Hello World! 你好世界 @#$%^&*()";
print "原始文本: $text\n";

my $encoded = mod::url_encode($text);
print "编码后:   $encoded\n";

my $decoded = mod::url_decode($encoded);
print "解码后:   $decoded\n";

# 组件编码（对保留字符也编码）
my $component = "a+b=c&d=e";
print "\n组件编码示例:\n";
print "原始:     $component\n";
print "编码后:   " . mod::url_encode_component($component) . "\n";

# ==================== 2. 查询字符串处理 ====================
print "\n\n2. 查询字符串处理\n";
print "-" x 40 . "\n";

# 解析查询字符串
my $query = "name=John%20Doe&age=30&city=New%20York&tag=perl&tag=programming";
print "查询字符串: $query\n\n";

my $params = mod::parse_query_string($query);
print "解析结果:\n";
foreach my $key (sort keys %$params) {
    my $value = $params->{$key};
    if (ref $value eq 'ARRAY') {
        print "  $key = [" . join(", ", @$value) . "]\n";
    } else {
        print "  $key = $value\n";
    }
}

# 构建查询字符串
print "\n构建查询字符串:\n";
my $new_params = {
    search => "perl tutorial",
    page   => 1,
    sort   => "relevance"
};
my $new_query = mod::build_query_string($new_params);
print "参数: { search => 'perl tutorial', page => 1, sort => 'relevance' }\n";
print "结果: $new_query\n";

# 排序构建
my $sorted_query = mod::build_query_string($new_params, { sort => 1 });
print "排序后: $sorted_query\n";

# ==================== 3. URL 解析与构建 ====================
print "\n\n3. URL 解析与构建\n";
print "-" x 40 . "\n";

# 解析复杂 URL
my $complex_url = 'https://user:password@api.example.com:8080/v1/users?active=true&role=admin#section2';
print "解析 URL: $complex_url\n\n";

my $parsed = mod::parse_url($complex_url);
print "组件分解:\n";
print "  协议:   $parsed->{scheme}\n"   if $parsed->{scheme};
print "  用户:   $parsed->{userinfo}\n" if $parsed->{userinfo};
print "  主机:   $parsed->{host}\n"     if $parsed->{host};
print "  端口:   $parsed->{port}\n"     if $parsed->{port};
print "  路径:   $parsed->{path}\n"     if $parsed->{path};
print "  查询:   $parsed->{query}\n"    if $parsed->{query};
print "  锚点:   $parsed->{fragment}\n" if $parsed->{fragment};

# 从组件构建 URL
print "\n从组件构建 URL:\n";
my $built_url = mod::build_url({
    scheme => 'https',
    host   => 'github.com',
    path   => '/ayukyo/alltoolkit',
    query  => { tab => 'readme', lang => 'perl' }
});
print "构建结果: $built_url\n";

# ==================== 4. URL 验证与工具 ====================
print "\n\n4. URL 验证与工具\n";
print "-" x 40 . "\n";

my @urls_to_test = (
    "https://example.com",
    "http://localhost:3000/api",
    "ftp://files.example.com",
    "not-a-valid-url",
    "just-some-text",
    "",
);

print "URL 验证测试:\n";
foreach my $url (@urls_to_test) {
    my $valid = mod::is_valid_url($url);
    my $status = $valid ? "✓ 有效" : "✗ 无效";
    print "  '$url' -> $status\n";
}

# 提取域名和路径
print "\n提取域名和路径:\n";
my $test_url = "https://www.perl.org/documentation/";
print "URL: $test_url\n";
print "  域名: " . mod::get_domain($test_url) . "\n";
print "  路径: " . mod::get_path($test_url) . "\n";

# ==================== 5. 参数操作 ====================
print "\n\n5. 参数操作\n";
print "-" x 40 . "\n";

# 添加参数
my $base_url = "https://api.example.com/search";
print "基础 URL: $base_url\n";

my $with_params = mod::add_query_params($base_url, {
    q     => "perl programming",
    page  => 1,
    limit => 10
});
print "添加参数后: $with_params\n";

# 继续添加参数
my $with_more = mod::add_query_params($with_params, { sort => "relevance" });
print "再添加 sort: $with_more\n";

# 移除参数
my $removed = mod::remove_query_params($with_more, ["page", "limit"]);
print "移除 page 和 limit: $removed\n";

# ==================== 6. URL 规范化 ====================
print "\n\n6. URL 规范化\n";
print "-" x 40 . "\n";

my @urls_to_normalize = (
    "HTTPS://EXAMPLE.COM:443/path",
    "http://Example.COM:80/Page",
    "https://example.com/./path/../other",
);

print "URL 规范化:\n";
foreach my $url (@urls_to_normalize) {
    my $normalized = mod::normalize_url($url);
    print "  原始: $url\n";
    print "  规范: $normalized\n\n";
}

# ==================== 7. 实用场景示例 ====================
print "\n7. 实用场景示例\n";
print "-" x 40 . "\n";

# 场景 1: 构建带分页的 API URL
print "场景 1: 构建分页 API URL\n";
sub build_api_url {
    my ($base, $endpoint, $params) = @_;
    return mod::build_url({
        scheme => 'https',
        host   => $base,
        path   => $endpoint,
        query  => $params
    });
}

my $api_url = build_api_url('api.example.com', '/v1/users', {
    page  => 2,
    limit => 20,
    sort  => 'created_at'
});
print "API URL: $api_url\n";

# 场景 2: 处理回调 URL
print "\n场景 2: 处理回调 URL\n";
my $callback = "https://myapp.com/callback?code=abc123&state=xyz&session=temp";
print "原始回调: $callback\n";

# 移除敏感参数
my $clean_callback = mod::remove_query_params($callback, ["session"]);
print "清理后:   $clean_callback\n";

# 场景 3: 验证和规范化用户输入的 URL
print "\n场景 3: 验证用户输入\n";
my $user_input = "HTTPS://Example.COM:443/Path";
if (mod::is_valid_url($user_input)) {
    my $canonical = mod::normalize_url($user_input);
    print "输入: $user_input\n";
    print "规范: $canonical\n";
} else {
    print "无效的 URL: $user_input\n";
}

print "\n" . "=" x 60 . "\n";
print "示例运行完成!\n";
print "=" x 60 . "\n";
