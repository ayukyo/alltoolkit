#!/usr/bin/env python3
"""
URL Utilities 使用示例
演示各种 URL 处理功能
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    URLParser, URLBuilder, URLEncoder, URLNormalizer, URLValidator, URLUtils,
    QueryStringParser,
    parse_url, build_url, encode_url, decode_url, normalize_url,
    validate_url, is_safe_url, clean_url, get_domain, get_query_params,
    set_query_param, remove_query_param
)


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def demo_url_parsing():
    """演示 URL 解析"""
    print_section("URL 解析")
    
    # 解析复杂 URL
    url = "https://admin:secret@api.example.com:8080/v1/users?page=1&limit=10#results"
    print(f"\n原始 URL: {url}")
    
    info = parse_url(url)
    print(f"\n解析结果:")
    print(f"  协议 (scheme): {info.scheme}")
    print(f"  主机名 (hostname): {info.hostname}")
    print(f"  端口 (port): {info.port}")
    print(f"  路径 (path): {info.path}")
    print(f"  查询字符串 (query): {info.query}")
    print(f"  片段 (fragment): {info.fragment}")
    print(f"  用户名 (username): {info.username}")
    print(f"  密码 (password): {info.password}")
    
    # 转换为字典
    print(f"\n字典格式:")
    for key, value in info.to_dict().items():
        if value:
            print(f"  {key}: {value}")
    
    # URL 验证
    print(f"\nURL 验证:")
    valid, errors = validate_url(url)
    print(f"  有效性: {'✓ 有效' if valid else '✗ 无效'}")
    if errors:
        print(f"  错误: {errors}")


def demo_url_building():
    """演示 URL 构建"""
    print_section("URL 构建")
    
    # 方式1: 链式调用
    print("\n方式1: 链式调用")
    url = (URLBuilder()
            .scheme("https")
            .host("api.example.com")
            .port(443)
            .path("/v1/users")
            .query_param("page", "1")
            .query_param("limit", "10")
            .query_param("sort", "name")
            .fragment("results")
            .build())
    print(f"  构建的 URL: {url}")
    
    # 方式2: 批量设置查询参数
    print("\n方式2: 批量设置查询参数")
    url = (URLBuilder()
            .scheme("https")
            .host("search.example.com")
            .path("/search")
            .query_params({
                "q": "python url parsing",
                "page": "1",
                "per_page": "20",
                "tags": ["web", "api", "http"]
            })
            .build())
    print(f"  构建的 URL: {url}")
    
    # 方式3: 带认证信息
    print("\n方式3: 带认证信息")
    url = (URLBuilder()
            .scheme("https")
            .host("secure.example.com")
            .user("admin", "password123")
            .path("/admin/dashboard")
            .build())
    print(f"  构建的 URL: {url}")
    
    # 方式4: 从基础 URL 开始
    print("\n方式4: 从基础 URL 开始")
    url = (URLBuilder("https://example.com/api/v1")
            .query_param("token", "abc123")
            .fragment("data")
            .build())
    print(f"  构建的 URL: {url}")


def demo_url_encoding():
    """演示 URL 编码"""
    print_section("URL 编码")
    
    # 基础编码
    print("\n基础编码/解码:")
    original = "hello world! @#$%^&*()"
    encoded = encode_url(original)
    decoded = decode_url(encoded)
    print(f"  原始: {original}")
    print(f"  编码: {encoded}")
    print(f"  解码: {decoded}")
    
    # 路径编码
    print("\n路径编码 (保留斜杠):")
    path = "/path with spaces/and special chars!/file.txt"
    encoded_path = URLEncoder.encode_path(path)
    print(f"  原始: {path}")
    print(f"  编码: {encoded_path}")
    
    # 查询参数编码
    print("\n查询参数编码:")
    value = "a=1&b=2&c=hello world"
    encoded_value = URLEncoder.encode_query(value)
    print(f"  原始: {value}")
    print(f"  编码: {encoded_value}")
    
    # Unicode 编码
    print("\nUnicode 编码:")
    unicode_text = "你好世界 🌍"
    encoded_unicode = encode_url(unicode_text)
    decoded_unicode = decode_url(encoded_unicode)
    print(f"  原始: {unicode_text}")
    print(f"  编码: {encoded_unicode}")
    print(f"  解码: {decoded_unicode}")


def demo_query_string():
    """演示查询字符串处理"""
    print_section("查询字符串处理")
    
    # 解析查询字符串
    print("\n解析查询字符串:")
    query_string = "q=python&page=1&tags=web&tags=api&tags=http"
    params = QueryStringParser.parse(query_string)
    print(f"  原始: {query_string}")
    print(f"  解析结果: {params}")
    
    # 获取单个参数
    print("\n获取单个参数:")
    print(f"  q = {QueryStringParser.get_param(query_string, 'q')}")
    print(f"  page = {QueryStringParser.get_param(query_string, 'page')}")
    print(f"  missing = {QueryStringParser.get_param(query_string, 'missing', 'default')}")
    
    # 获取多值参数
    print("\n获取多值参数:")
    tags = QueryStringParser.get_params(query_string, "tags")
    print(f"  tags = {tags}")
    
    # 修改参数
    print("\n修改参数:")
    modified = QueryStringParser.set_param(query_string, "page", "2")
    print(f"  设置 page=2: {modified}")
    
    removed = QueryStringParser.remove_param(query_string, "page")
    print(f"  移除 page: {removed}")
    
    # 检查参数存在
    print("\n检查参数存在:")
    print(f"  q 存在: {QueryStringParser.has_param(query_string, 'q')}")
    print(f"  missing 存在: {QueryStringParser.has_param(query_string, 'missing')}")
    
    # 构建查询字符串
    print("\n构建查询字符串:")
    params = {
        "search": "python",
        "page": ["1"],
        "limit": ["20"],
        "tags": ["web", "api"]
    }
    built = QueryStringParser.build(params)
    print(f"  参数: {params}")
    print(f"  构建: {built}")


def demo_url_normalization():
    """演示 URL 规范化"""
    print_section("URL 规范化")
    
    # 规范化示例
    urls = [
        "HTTPS://EXAMPLE.COM/Path/",
        "https://example.com:443/path",
        "https://example.com/path//to///page",
        "https://example.com?b=2&a=1&c=3",
        "https://example.com/page?utm_source=google&ref=twitter&id=123",
    ]
    
    for url in urls:
        normalized = normalize_url(url)
        print(f"\n原始: {url}")
        print(f"规范: {normalized}")
    
    # 移除追踪参数
    print("\n移除追踪参数:")
    url = "https://example.com/page?utm_source=google&utm_medium=cpc&utm_campaign=spring&real_param=value&fbclid=xyz123"
    cleaned = clean_url(url)
    print(f"  原始: {url}")
    print(f"  清理: {cleaned}")
    
    # 相对 URL 解析
    print("\n相对 URL 解析:")
    base = "https://example.com/docs/api/v1/"
    relatives = [
        "page.html",
        "../v2/page.html",
        "/absolute/path",
        "https://other.com/page",
    ]
    for rel in relatives:
        resolved = URLNormalizer.resolve(base, rel)
        print(f"  {rel} → {resolved}")


def demo_url_validation():
    """演示 URL 验证"""
    print_section("URL 验证")
    
    # URL 有效性验证
    print("\nURL 有效性验证:")
    test_urls = [
        "https://example.com",
        "http://localhost:3000/api",
        "ftp://ftp.example.com:21/files",
        "javascript:alert('xss')",
        "not a url",
        "http://192.168.1.1:8080",
        "http://[::1]:8080",
    ]
    
    for url in test_urls:
        valid, errors = validate_url(url)
        status = "✓ 有效" if valid else "✗ 无效"
        print(f"  {url}")
        print(f"    {status}")
        if errors:
            print(f"    错误: {errors}")
    
    # 安全 URL 检查
    print("\n安全 URL 检查:")
    safety_urls = [
        "https://example.com/page",
        "https://user:pass@example.com/secure",  # 包含凭证
        "javascript:alert('xss')",  # 危险 scheme
        "http://192.168.1.1/admin",  # 私有 IP
        "data:text/html,<script>alert(1)</script>",  # 数据 URL
    ]
    
    for url in safety_urls:
        safe = is_safe_url(url)
        print(f"  {url}")
        print(f"    {'✓ 安全' if safe else '✗ 不安全'}")
    
    # 允许私有 IP
    print("\n允许私有 IP:")
    url = "http://192.168.1.1/admin"
    print(f"  {url}")
    print(f"  默认: {'✓ 安全' if is_safe_url(url) else '✗ 不安全'}")
    print(f"  允许私有 IP: {'✓ 安全' if is_safe_url(url, allow_private_ip=True) else '✗ 不安全'}")
    
    # 同源检查
    print("\n同源检查:")
    origins = [
        ("https://example.com/a", "https://example.com/b"),
        ("https://example.com", "http://example.com"),
        ("https://example.com", "https://api.example.com"),
        ("https://example.com:443", "https://example.com"),
    ]
    for url1, url2 in origins:
        same = URLValidator.is_same_origin(url1, url2)
        print(f"  {url1}")
        print(f"  {url2}")
        print(f"    {'✓ 同源' if same else '✗ 不同源'}")


def demo_url_utils():
    """演示 URL 工具函数"""
    print_section("URL 工具函数")
    
    url = "https://blog.example.com/articles/2024/python-tutorial.html?ref=home&page=1"
    
    # 提取信息
    print(f"\nURL: {url}")
    print(f"\n提取信息:")
    print(f"  域名: {get_domain(url)}")
    print(f"  根域名: {URLUtils.extract_root_domain(url)}")
    print(f"  顶级域名: {URLUtils.extract_tld(url)}")
    print(f"  路径: {URLUtils.extract_path(url)}")
    print(f"  文件名: {URLUtils.extract_filename(url)}")
    print(f"  扩展名: {URLUtils.extract_extension(url)}")
    print(f"  路径深度: {URLUtils.get_url_depth(url)}")
    print(f"  查询参数: {get_query_params(url)}")
    
    # 修改 URL
    print("\n修改 URL:")
    print(f"  更改协议: {URLUtils.change_scheme(url, 'http')}")
    print(f"  确保协议: {URLUtils.ensure_scheme('example.com/path')}")
    print(f"  基础 URL: {URLUtils.get_base_url(url)}")
    print(f"  设置参数: {set_query_param(url, 'new', 'value')}")
    print(f"  移除参数: {remove_query_param(url, 'ref')}")
    
    # 分割和重组
    print("\n分割和重组:")
    parts = URLUtils.split_url(url)
    print(f"  分割: {parts}")
    reconstructed = URLUtils.unsplit(parts)
    print(f"  重组: {reconstructed}")
    
    # 子域名检查
    print("\n子域名检查:")
    print(f"  blog.example.com 是 example.com 的子域名: {URLUtils.is_subdomain(url, 'example.com')}")
    print(f"  blog.example.com 是 other.com 的子域名: {URLUtils.is_subdomain(url, 'other.com')}")
    
    # 批量解析
    print("\n批量解析相对 URL:")
    base = "https://example.com/docs/"
    relatives = ["page1.html", "page2.html", "/api/v1"]
    resolved = URLUtils.batch_resolve(relatives, base)
    for rel, abs_url in resolved.items():
        print(f"  {rel} → {abs_url}")


def demo_real_world_scenarios():
    """演示实际应用场景"""
    print_section("实际应用场景")
    
    # 场景1: URL 清理
    print("\n场景1: 清理分享链接中的追踪参数")
    shared_url = "https://example.com/article/123?utm_source=twitter&utm_medium=social&utm_campaign=spring&fbclid=IwAR123456&ref=email"
    cleaned = clean_url(shared_url)
    print(f"  原始: {shared_url}")
    print(f"  清理: {cleaned}")
    
    # 场景2: API 请求构建
    print("\n场景2: 构建 API 请求 URL")
    api_url = (URLBuilder()
               .scheme("https")
               .host("api.example.com")
               .path("/v1/users")
               .query_params({
                   "page": "1",
                   "limit": "20",
                   "sort": "created_at",
                   "order": "desc",
                   "fields": ["id", "name", "email"]
               })
               .build())
    print(f"  构建的 API URL: {api_url}")
    
    # 场景3: URL 验证和清理
    print("\n场景3: 用户输入 URL 验证和清理")
    user_input = "  HTTPS://Example.COM:443/Path/  "
    user_input = user_input.strip()  # 去除首尾空格
    valid, errors = validate_url(user_input)
    if valid:
        normalized = normalize_url(user_input)
        print(f"  用户输入: {user_input}")
        print(f"  规范化后: {normalized}")
    else:
        print(f"  无效 URL: {errors}")
    
    # 场景4: 安全检查
    print("\n场景4: 安全 URL 检查 (防止 SSRF)")
    test_urls = [
        "https://example.com/api/data",
        "http://localhost:8080/admin",
        "http://169.254.169.254/latest/meta-data",
        "http://internal.company.com/secret",
    ]
    for url in test_urls:
        valid, _ = validate_url(url)
        safe = is_safe_url(url) if valid else False
        print(f"  {url}")
        print(f"    有效: {'是' if valid else '否'}, 安全: {'是' if safe else '否'}")
    
    # 场景5: URL 比较
    print("\n场景5: 判断两个 URL 是否指向同一资源")
    urls_to_compare = [
        ("https://example.com/path?b=2&a=1", "https://example.com/path?a=1&b=2"),
        ("https://example.com:443/path", "https://example.com/path"),
        ("https://example.com/path#section", "https://example.com/path"),
    ]
    for url1, url2 in urls_to_compare:
        norm1 = normalize_url(url1)
        norm2 = normalize_url(url2)
        same = norm1 == norm2
        print(f"  URL 1: {url1}")
        print(f"  URL 2: {url2}")
        print(f"  规范化后相同: {'是' if same else '否'}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("  URL Utilities 使用示例")
    print("=" * 60)
    
    demo_url_parsing()
    demo_url_building()
    demo_url_encoding()
    demo_query_string()
    demo_url_normalization()
    demo_url_validation()
    demo_url_utils()
    demo_real_world_scenarios()
    
    print("\n" + "=" * 60)
    print("  示例演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()