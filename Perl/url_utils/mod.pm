#!/usr/bin/perl
# URL Utilities Module for Perl
# 零依赖，仅使用 Perl 标准库
#
# 功能：URL 编码/解码、查询参数解析与构建、URL 验证与解析
#
# 使用方法：
#   use lib 'Perl/url_utils';
#   use mod;
#
#   my $encoded = mod::url_encode("Hello World!");
#   my $decoded = mod::url_decode("Hello%20World%21");

package mod;

use strict;
use warnings;
use utf8;

# 版本号
our $VERSION = '1.0.0';

# 导出所有函数
use Exporter 'import';
our @EXPORT = qw(
    url_encode
    url_decode
    url_encode_component
    url_decode_component
    parse_query_string
    build_query_string
    parse_url
    build_url
    is_valid_url
    get_domain
    get_path
    add_query_params
    remove_query_params
    normalize_url
);

our @EXPORT_OK = @EXPORT;

# URL 保留字符（RFC 3986）
my $URL_RESERVED = q{!$&'()*+,;=:@/?#[]};
my $URL_UNRESERVED = q{A-Za-z0-9._~-};

=pod

=head1 URL 编码与解码

=head2 url_encode($string)

对字符串进行 URL 编码（空格编码为 %20）。

参数：
    $string - 要编码的字符串

返回：
    编码后的 URL 字符串

示例：
    my $encoded = mod::url_encode("Hello World!");
    # 结果: "Hello%20World%21"

=cut

sub url_encode {
    my ($string) = @_;
    return '' unless defined $string;
    
    # 将字符串转换为字节序列并编码
    $string =~ s/([^$URL_UNRESERVED])/'%' . sprintf('%02X', ord($1))/ge;
    return $string;
}

=pod

=head2 url_decode($string)

对 URL 编码的字符串进行解码。

参数：
    $string - 要解码的 URL 字符串

返回：
    解码后的原始字符串

示例：
    my $decoded = mod::url_decode("Hello%20World%21");
    # 结果: "Hello World!"

=cut

sub url_decode {
    my ($string) = @_;
    return '' unless defined $string;
    
    $string =~ s/%([0-9A-Fa-f]{2})/chr(hex($1))/ge;
    return $string;
}

=pod

=head2 url_encode_component($string)

对 URL 组件进行编码（适合编码 URL 中的参数值，空格编码为 %20）。

参数：
    $string - 要编码的字符串

返回：
    编码后的 URL 组件字符串

示例：
    my $encoded = mod::url_encode_component("a+b=c");
    # 结果: "a%2Bb%3Dc"

=cut

sub url_encode_component {
    my ($string) = @_;
    return '' unless defined $string;
    
    # 对更多字符进行编码（包括保留字符）
    $string =~ s/([^$URL_UNRESERVED])/'%' . sprintf('%02X', ord($1))/ge;
    return $string;
}

=pod

=head2 url_decode_component($string)

对 URL 组件编码的字符串进行解码。

参数：
    $string - 要解码的 URL 组件字符串

返回：
    解码后的原始字符串

示例：
    my $decoded = mod::url_decode_component("a%2Bb%3Dc");
    # 结果: "a+b=c"

=cut

sub url_decode_component {
    my ($string) = @_;
    return url_decode($string);
}

=pod

=head1 查询字符串处理

=head2 parse_query_string($query_string)

解析 URL 查询字符串为哈希引用。

参数：
    $query_string - 查询字符串（如 "a=1&b=2" 或 "?a=1&b=2"）

返回：
    哈希引用，包含解析后的参数

示例：
    my $params = mod::parse_query_string("name=John&age=30");
    # 结果: { name => "John", age => "30" }
    
    # 支持数组参数
    my $params2 = mod::parse_query_string("tag=a&tag=b");
    # 结果: { tag => ["a", "b"] }

=cut

sub parse_query_string {
    my ($query_string) = @_;
    return {} unless defined $query_string && $query_string ne '';
    
    # 移除开头的 ? 或 &
    $query_string =~ s/^[?&]+//;
    
    my %params;
    my @pairs = split /&/, $query_string;
    
    foreach my $pair (@pairs) {
        next if $pair eq '';
        
        my ($key, $value) = split /=/, $pair, 2;
        $key = url_decode($key // '');
        $value = url_decode($value // '');
        
        # 处理数组参数（同名参数多次出现）
        if (exists $params{$key}) {
            if (ref $params{$key} eq 'ARRAY') {
                push @{$params{$key}}, $value;
            } else {
                $params{$key} = [$params{$key}, $value];
            }
        } else {
            $params{$key} = $value;
        }
    }
    
    return \%params;
}

=pod

=head2 build_query_string($params, $options)

从哈希引用构建 URL 查询字符串。

参数：
    $params  - 哈希引用，包含参数键值对
    $options - 可选配置哈希
        - skip_empty: 是否跳过空值（默认 0）
        - sort: 是否按键名排序（默认 0）

返回：
    查询字符串（不带开头的 ?）

示例：
    my $qs = mod::build_query_string({ name => "John", age => 30 });
    # 结果: "name=John&age=30"
    
    my $qs2 = mod::build_query_string({ a => 1, b => 2 }, { sort => 1 });
    # 结果: "a=1&b=2" (按键名排序)

=cut

sub build_query_string {
    my ($params, $options) = @_;
    $options //= {};
    return '' unless defined $params && %$params;
    
    my @pairs;
    my @keys = $options->{sort} ? sort keys %$params : keys %$params;
    
    foreach my $key (@keys) {
        my $value = $params->{$key};
        
        # 跳过空值（如果启用）
        next if $options->{skip_empty} && (!defined $value || $value eq '');
        
        my $encoded_key = url_encode_component($key);
        
        if (ref $value eq 'ARRAY') {
            # 数组参数
            foreach my $v (@$value) {
                $v = '' unless defined $v;
                next if $options->{skip_empty} && $v eq '';
                push @pairs, "$encoded_key=" . url_encode_component($v);
            }
        } else {
            $value = '' unless defined $value;
            push @pairs, "$encoded_key=" . url_encode_component($value);
        }
    }
    
    return join('&', @pairs);
}

=pod

=head1 URL 解析与构建

=head2 parse_url($url)

解析 URL 为组件哈希引用。

参数：
    $url - 要解析的 URL 字符串

返回：
    哈希引用，包含以下字段：
    - scheme: 协议（如 http, https）
    - userinfo: 用户信息（如 user:pass）
    - host: 主机名
    - port: 端口号
    - path: 路径
    - query: 查询字符串
    - fragment: 锚点（#后面的部分）

示例：
    my $parsed = mod::parse_url("https://user:pass@example.com:8080/path?a=1#anchor");
    # 结果包含各个组件

=cut

sub parse_url {
    my ($url) = @_;
    return undef unless defined $url && $url ne '';
    
    # URL 正则匹配（RFC 3986 简化版）
    my $pattern = qr{^
        (?:(?<scheme>[a-zA-Z][a-zA-Z0-9+.-]*)://)?
        (?:(?<userinfo>[^@/?#]*)@)?
        (?<host>[^:/?#]*)
        (?::(?<port>\d+))?
        (?<path>[^?#]*)
        (?:\?(?<query>[^#]*))?
        (?:\#(?<fragment>.*))?
    $}x;
    
    if ($url =~ $pattern) {
        return {
            scheme   => $+{scheme} // '',
            userinfo => $+{userinfo} // '',
            host     => $+{host} // '',
            port     => $+{port} // '',
            path     => $+{path} // '',
            query    => $+{query} // '',
            fragment => $+{fragment} // '',
        };
    }
    
    return undef;
}

=pod

=head2 build_url($components)

从组件哈希引用构建完整 URL。

参数：
    $components - 哈希引用，包含 URL 组件
        - scheme: 协议
        - userinfo: 用户信息
        - host: 主机名
        - port: 端口号
        - path: 路径
        - query: 查询字符串或哈希引用
        - fragment: 锚点

返回：
    完整的 URL 字符串

示例：
    my $url = mod::build_url({
        scheme => 'https',
        host   => 'example.com',
        path   => '/path',
        query  => { a => 1 }
    });
    # 结果: "https://example.com/path?a=1"

=cut

sub build_url {
    my ($components) = @_;
    return '' unless defined $components;
    
    my $url = '';
    
    # 协议
    if ($components->{scheme}) {
        $url .= $components->{scheme} . '://';
    }
    
    # 用户信息
    if ($components->{userinfo}) {
        $url .= $components->{userinfo} . '@';
    }
    
    # 主机
    $url .= $components->{host} if $components->{host};
    
    # 端口
    if ($components->{port}) {
        $url .= ':' . $components->{port};
    }
    
    # 路径
    my $path = $components->{path} // '';
    $url .= $path;
    
    # 查询字符串
    if ($components->{query}) {
        my $qs;
        if (ref $components->{query} eq 'HASH') {
            $qs = build_query_string($components->{query});
        } else {
            $qs = $components->{query};
        }
        $url .= '?' . $qs if $qs;
    }
    
    # 锚点
    if ($components->{fragment}) {
        $url .= '#' . $components->{fragment};
    }
    
    return $url;
}

=pod

=head1 URL 验证与工具

=head2 is_valid_url($url)

验证字符串是否为有效的 URL。

参数：
    $url - 要验证的字符串

返回：
    1 表示有效，0 表示无效

示例：
    my $valid1 = mod::is_valid_url("https://example.com");  # 1
    my $valid2 = mod::is_valid_url("not-a-url");            # 0

=cut

sub is_valid_url {
    my ($url) = @_;
    return 0 unless defined $url && $url ne '';
    
    # 更严格的 URL 验证正则
    # 要求至少包含协议或看起来像域名（包含点）
    my $url_pattern = qr{^
        (?:[a-zA-Z][a-zA-Z0-9+.-]*://)?
        (?:[^@/?#]*@)?
        (?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}
        (?::\d+)?
        (?:/[^?#]*)?
        (?:\?[^#]*)?
        (?:\#.*)?
    $}x;
    
    return $url =~ $url_pattern ? 1 : 0;
}

=pod

=head2 get_domain($url)

从 URL 中提取域名。

参数：
    $url - URL 字符串

返回：
    域名（如 example.com）

示例：
    my $domain = mod::get_domain("https://www.example.com/path");
    # 结果: "www.example.com"

=cut

sub get_domain {
    my ($url) = @_;
    return '' unless defined $url;
    
    my $parsed = parse_url($url);
    return $parsed ? $parsed->{host} : '';
}

=pod

=head2 get_path($url)

从 URL 中提取路径。

参数：
    $url - URL 字符串

返回：
    路径（如 /path/to/resource）

示例：
    my $path = mod::get_path("https://example.com/path?a=1");
    # 结果: "/path"

=cut

sub get_path {
    my ($url) = @_;
    return '' unless defined $url;
    
    my $parsed = parse_url($url);
    return $parsed ? $parsed->{path} : '';
}

=pod

=head2 add_query_params($url, $params)

向 URL 添加查询参数。

参数：
    $url    - 原始 URL
    $params - 哈希引用，要添加的参数

返回：
    新的 URL 字符串

示例：
    my $new_url = mod::add_query_params(
        "https://example.com/path",
        { a => 1, b => 2 }
    );
    # 结果: "https://example.com/path?a=1&b=2"

=cut

sub add_query_params {
    my ($url, $params) = @_;
    return $url unless defined $url && defined $params && %$params;
    
    my $parsed = parse_url($url);
    return $url unless $parsed;
    
    # 解析现有参数
    my $existing_params = parse_query_string($parsed->{query});
    
    # 合并新参数
    foreach my $key (keys %$params) {
        $existing_params->{$key} = $params->{$key};
    }
    
    # 重建 URL
    $parsed->{query} = $existing_params;
    return build_url($parsed);
}

=pod

=head2 remove_query_params($url, $keys)

从 URL 中移除指定的查询参数。

参数：
    $url  - 原始 URL
    $keys - 数组引用，要移除的参数键名

返回：
    新的 URL 字符串

示例：
    my $new_url = mod::remove_query_params(
        "https://example.com/path?a=1&b=2&c=3",
        ["b"]
    );
    # 结果: "https://example.com/path?a=1&c=3"

=cut

sub remove_query_params {
    my ($url, $keys) = @_;
    return $url unless defined $url && defined $keys && @$keys;
    
    my $parsed = parse_url($url);
    return $url unless $parsed && $parsed->{query};
    
    # 解析现有参数
    my $params = parse_query_string($parsed->{query});
    
    # 移除指定键
    my %keys_to_remove = map { $_ => 1 } @$keys;
    foreach my $key (keys %keys_to_remove) {
        delete $params->{$key};
    }
    
    # 重建 URL
    if (%$params) {
        $parsed->{query} = $params;
    } else {
        $parsed->{query} = '';
    }
    
    return build_url($parsed);
}

=pod

=head2 normalize_url($url)

规范化 URL（统一格式）。

参数：
    $url - URL 字符串

返回：
    规范化后的 URL

示例：
    my $normalized = mod::normalize_url("HTTPS://EXAMPLE.COM:80/Path/../Other");
    # 结果: "https://example.com/Other"

=cut

sub normalize_url {
    my ($url) = @_;
    return '' unless defined $url;
    
    my $parsed = parse_url($url);
    return $url unless $parsed;
    
    # 规范化协议（小写）
    $parsed->{scheme} = lc($parsed->{scheme}) if $parsed->{scheme};
    
    # 规范化主机（小写）
    $parsed->{host} = lc($parsed->{host}) if $parsed->{host};
    
    # 移除默认端口
    if ($parsed->{port}) {
        if (($parsed->{scheme} eq 'http' && $parsed->{port} eq '80') ||
            ($parsed->{scheme} eq 'https' && $parsed->{port} eq '443')) {
            $parsed->{port} = '';
        }
    }
    
    # 规范化路径（处理 . 和 ..）
    if ($parsed->{path}) {
        my @parts = split '/', $parsed->{path};
        my @normalized;
        foreach my $part (@parts) {
            next if $part eq '.';
            if ($part eq '..') {
                pop @normalized if @normalized;
            } else {
                push @normalized, $part;
            }
        }
        $parsed->{path} = '/' . join('/', @normalized);
    }
    
    return build_url($parsed);
}

1;

__END__

=head1 DESCRIPTION

URL Utilities Module - 提供 URL 编码/解码、查询参数处理、URL 解析与构建等功能。

=head1 AUTHOR

AllToolkit Contributors

=head1 LICENSE

MIT License

=cut