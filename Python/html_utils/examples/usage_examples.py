#!/usr/bin/env python3
"""
AllToolkit - HTML Utilities Usage Examples

Comprehensive examples demonstrating various use cases for the HTML utilities module.
Zero dependencies - uses only Python standard library.
"""

import sys
import os
from typing import List, Dict

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    parse_html, find_elements, find_by_id, find_by_class,
    extract_links, extract_images, extract_title, extract_meta,
    sanitize_html, html_to_text,
    generate_tag, generate_link, generate_image, generate_table, generate_form,
    minify_html, prettify_html,
    count_tags, get_dom_depth, validate_html_structure
)


def example_basic_parsing():
    """Example 1: Basic HTML Parsing"""
    print("=" * 60)
    print("示例 1: 基本 HTML 解析")
    print("=" * 60)
    
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>示例页面</title>
        </head>
        <body>
            <div id="main" class="container">
                <h1>欢迎来到我的网站</h1>
                <p>这是一个示例段落。</p>
                <ul>
                    <li>项目 1</li>
                    <li>项目 2</li>
                    <li>项目 3</li>
                </ul>
            </div>
        </body>
    </html>
    """
    
    # 解析 HTML
    root = parse_html(html)
    
    # 获取页面标题
    title = extract_title(html)
    print(f"\n📄 页面标题：{title}")
    
    # 查找所有段落
    paragraphs = find_elements(root, tag="p")
    print(f"\n📝 段落数量：{len(paragraphs)}")
    for i, p in enumerate(paragraphs, 1):
        print(f"   段落 {i}: {p.get_text().strip()}")
    
    # 查找所有列表项
    items = find_elements(root, tag="li")
    print(f"\n📋 列表项数量：{len(items)}")
    for item in items:
        print(f"   • {item.get_text().strip()}")
    
    # 统计标签
    counts = count_tags(html)
    print(f"\n📊 标签统计：{dict(list(counts.items())[:5])}...")


def example_link_extraction():
    """Example 2: Link Extraction"""
    print("\n" + "=" * 60)
    print("示例 2: 链接提取")
    print("=" * 60)
    
    html = """
    <nav>
        <a href="/" title="首页">首页</a>
        <a href="/about" title="关于我们">关于我们</a>
        <a href="/products" class="active">产品</a>
        <a href="/contact">联系我们</a>
        <a href="https://blog.example.com" target="_blank">博客</a>
    </nav>
    
    <article>
        <p>查看更多：<a href="/article/123">文章详情</a></p>
        <p>相关资源：<a href="https://docs.example.com" title="文档">官方文档</a></p>
    </article>
    """
    
    # 提取所有链接
    links = extract_links(html)
    
    print(f"\n🔗 找到 {len(links)} 个链接:\n")
    for i, link in enumerate(links, 1):
        print(f"{i}. {link['text']}")
        print(f"   URL: {link['href']}")
        if link['title']:
            print(f"   标题：{link['title']}")
        print()
    
    # 查找外部链接
    external_links = [l for l in links if l['href'].startswith('http')]
    print(f"📡 外部链接：{len(external_links)} 个")
    
    # 查找内部链接
    internal_links = [l for l in links if not l['href'].startswith('http')]
    print(f"🏠 内部链接：{len(internal_links)} 个")


def example_image_extraction():
    """Example 3: Image Extraction"""
    print("\n" + "=" * 60)
    print("示例 3: 图片提取")
    print("=" * 60)
    
    html = """
    <div class="gallery">
        <img src="/images/photo1.jpg" alt="风景照片" title="美丽的风景">
        <img src="/images/photo2.jpg" alt="人物照片">
        <img src="/images/photo3.png" alt="产品图片" title="产品展示">
        <img src="https://cdn.example.com/banner.jpg" alt="广告横幅">
    </div>
    
    <article>
        <figure>
            <img src="/images/article-cover.jpg" alt="文章封面">
            <figcaption>文章封面图</figcaption>
        </figure>
    </article>
    """
    
    images = extract_images(html)
    
    print(f"\n🖼️  找到 {len(images)} 张图片:\n")
    for i, img in enumerate(images, 1):
        print(f"{i}. {img['alt'] or '无描述'}")
        print(f"   源：{img['src']}")
        if img['title']:
            print(f"   标题：{img['title']}")
        print()


def example_html_sanitization():
    """Example 4: HTML Sanitization"""
    print("=" * 60)
    print("示例 4: HTML 清理（XSS 防护）")
    print("=" * 60)
    
    dangerous_html = """
    <div class="user-comment">
        <p>这是一条正常的评论。</p>
        
        <!-- 危险的脚本注入尝试 -->
        <script>alert('XSS 攻击!');</script>
        
        <!-- 事件处理器注入 -->
        <img src="x" onerror="alert('XSS!')" alt="测试">
        
        <!-- JavaScript URL -->
        <a href="javascript:alert('XSS!')">点击这里</a>
        
        <!-- 隐藏的 iframe -->
        <iframe src="https://malicious.com"></iframe>
        
        <p>这也是正常内容。</p>
    </div>
    """
    
    print("\n⚠️  原始 HTML（包含危险内容）:")
    print(dangerous_html[:200] + "...")
    
    # 清理 HTML
    safe_html = sanitize_html(dangerous_html)
    
    print("\n✅ 清理后的 HTML（安全）:")
    print(safe_html)
    
    # 验证清理结果
    print("\n🔍 安全检查:")
    print(f"   包含 <script>: {'❌ 是' if '<script>' in safe_html else '✅ 否'}")
    print(f"   包含 onclick: {'❌ 是' if 'onclick' in safe_html else '✅ 否'}")
    print(f"   包含 onerror: {'❌ 是' if 'onerror' in safe_html else '✅ 否'}")
    print(f"   包含 javascript: {'❌ 是' if 'javascript:' in safe_html else '✅ 否'}")
    print(f"   包含 <iframe>: {'❌ 是' if '<iframe>' in safe_html else '✅ 否'}")


def example_html_generation():
    """Example 5: HTML Generation"""
    print("\n" + "=" * 60)
    print("示例 5: HTML 生成")
    print("=" * 60)
    
    # 生成产品表格
    print("\n📊 生成产品表格:")
    headers = ["产品 ID", "产品名称", "价格", "库存"]
    rows = [
        ["P001", "无线鼠标", "¥99", "150"],
        ["P002", "机械键盘", "¥399", "80"],
        ["P003", "USB 集线器", "¥59", "200"],
        ["P004", "显示器支架", "¥199", "45"]
    ]
    table = generate_table(headers, rows, {"class": "product-table", "id": "products"})
    print(table[:300] + "...")
    
    # 生成联系表单
    print("\n📝 生成联系表单:")
    fields = [
        {"type": "text", "name": "name", "label": "姓名", "attributes": {"required": "required"}},
        {"type": "email", "name": "email", "label": "邮箱", "attributes": {"required": "required"}},
        {"type": "tel", "name": "phone", "label": "电话"},
        {
            "type": "select",
            "name": "subject",
            "label": "主题",
            "options": [
                {"value": "", "text": "请选择主题"},
                {"value": "support", "text": "技术支持"},
                {"value": "sales", "text": "销售咨询"},
                {"value": "feedback", "text": "意见反馈"}
            ]
        },
        {"type": "textarea", "name": "message", "label": "留言"},
        {"type": "submit", "name": "submit", "value": "发送消息"}
    ]
    form = generate_form("/contact/submit", method="post", fields=fields)
    print(form[:400] + "...")
    
    # 生成导航链接
    print("\n🔗 生成导航链接:")
    nav_items = [
        generate_link("/", "首页", title="返回首页"),
        generate_link("/products", "产品", title="浏览产品"),
        generate_link("/about", "关于", title="关于我们"),
        generate_link("/contact", "联系", title="联系我们")
    ]
    nav_html = " | ".join(nav_items)
    print(nav_html)


def example_html_formatting():
    """Example 6: HTML Formatting"""
    print("\n" + "=" * 60)
    print("示例 6: HTML 格式化")
    print("=" * 60)
    
    # 紧凑的 HTML
    compact_html = "<div><ul><li>项 1</li><li>项 2</li><li>项 3</li></ul><p>段落内容</p></div>"
    
    print("\n📦 原始紧凑 HTML:")
    print(compact_html)
    
    # 美化
    pretty_html = prettify_html(compact_html)
    print("\n✨ 美化后:")
    print(pretty_html)
    
    # 压缩
    multi_line_html = """
    <div class="container">
        <h1>标题</h1>
        <!-- 这是一个注释 -->
        <p>这是一个段落。</p>
    </div>
    """
    
    print("\n📄 多行 HTML:")
    print(multi_line_html.strip())
    
    minified = minify_html(multi_line_html)
    print("\n🗜️ 压缩后:")
    print(minified)
    print(f"\n   原始长度：{len(multi_line_html)} 字符")
    print(f"   压缩长度：{len(minified)} 字符")
    print(f"   压缩率：{(1 - len(minified)/len(multi_line_html))*100:.1f}%")


def example_html_to_text():
    """Example 7: HTML to Text Conversion"""
    print("\n" + "=" * 60)
    print("示例 7: HTML 转纯文本")
    print("=" * 60)
    
    html = """
    <article>
        <header>
            <h1>文章标题</h1>
            <time>2024 年 1 月 15 日</time>
        </header>
        <div class="content">
            <p>这是第一段内容，包含一些<strong>粗体文字</strong>和<em>斜体文字</em>。</p>
            <p>这是第二段，包含一个<a href="https://example.com">链接</a>。</p>
            <ul>
                <li>列表项 1</li>
                <li>列表项 2</li>
                <li>列表项 3</li>
            </ul>
            <blockquote>这是一段引用文字。</blockquote>
        </div>
        <!-- 这是注释，不会出现在文本中 -->
        <footer>
            <p>作者：张三</p>
        </footer>
    </article>
    """
    
    text = html_to_text(html)
    
    print("\n📝 转换后的纯文本:\n")
    print(text)
    
    print(f"\n📊 统计:")
    print(f"   HTML 长度：{len(html)} 字符")
    print(f"   文本长度：{len(text)} 字符")


def example_dom_analysis():
    """Example 8: DOM Structure Analysis"""
    print("\n" + "=" * 60)
    print("示例 8: DOM 结构分析")
    print("=" * 60)
    
    html = """
    <html>
        <head>
            <title>分析示例</title>
            <meta name="description" content="页面描述">
            <meta property="og:title" content="社交标题">
        </head>
        <body>
            <header>
                <nav>
                    <ul>
                        <li><a href="/">首页</a></li>
                        <li><a href="/about">关于</a></li>
                    </ul>
                </nav>
            </header>
            <main>
                <article>
                    <h1>文章</h1>
                    <p>内容...</p>
                </article>
            </main>
            <footer>
                <p>版权信息</p>
            </footer>
        </body>
    </html>
    """
    
    root = parse_html(html)
    
    # 获取元数据
    print("\n📋 元数据:")
    title = extract_title(html)
    print(f"   标题：{title}")
    
    desc = extract_meta(html, name="description")
    print(f"   描述：{desc}")
    
    og_title = extract_meta(html, property="og:title")
    print(f"   OG 标题：{og_title}")
    
    # DOM 统计
    print("\n📊 DOM 统计:")
    counts = count_tags(html)
    print(f"   标签总数：{sum(counts.values())}")
    print(f"   不同标签数：{len(counts)}")
    print(f"   最多的标签：{max(counts.items(), key=lambda x: x[1])}")
    
    depth = get_dom_depth(root)
    print(f"   DOM 深度：{depth}")
    
    # 结构验证
    print("\n✅ 结构验证:")
    validation = validate_html_structure(html)
    print(f"   结构有效：{'是' if validation['valid'] else '否'}")
    if validation['issues']:
        print(f"   问题：{validation['issues']}")


def example_real_world_scraping():
    """Example 9: Real-world Web Scraping Simulation"""
    print("\n" + "=" * 60)
    print("示例 9: 真实场景 - 网页内容提取")
    print("=" * 60)
    
    # 模拟博客页面 HTML
    blog_html = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>Python 编程技巧 - 技术博客</title>
        <meta name="description" content="分享 Python 编程的最佳实践和技巧">
        <meta name="keywords" content="Python, 编程，技巧，教程">
    </head>
    <body>
        <header class="site-header">
            <h1><a href="/">技术博客</a></h1>
            <nav>
                <a href="/python">Python</a>
                <a href="/javascript">JavaScript</a>
                <a href="/about">关于</a>
            </nav>
        </header>
        
        <main class="content">
            <article class="post">
                <header class="post-header">
                    <h2 class="post-title">10 个实用的 Python 编程技巧</h2>
                    <div class="post-meta">
                        <span class="author">作者：张三</span>
                        <time datetime="2024-01-15">2024 年 1 月 15 日</time>
                    </div>
                </header>
                
                <img src="/images/python-tips.jpg" alt="Python 编程技巧封面" class="post-cover">
                
                <div class="post-content">
                    <p>Python 是一门优雅而强大的编程语言...</p>
                    <h3>技巧 1: 列表推导式</h3>
                    <p>使用列表推导式可以简化代码...</p>
                    <pre><code>squares = [x**2 for x in range(10)]</code></pre>
                    <h3>技巧 2: 上下文管理器</h3>
                    <p>使用 with 语句自动管理资源...</p>
                </div>
                
                <footer class="post-footer">
                    <div class="tags">
                        <a href="/tag/python" class="tag">Python</a>
                        <a href="/tag/tips" class="tag">技巧</a>
                    </div>
                    <a href="/comments" class="comments-link">评论 (15)</a>
                </footer>
            </article>
            
            <aside class="sidebar">
                <div class="widget">
                    <h3>热门文章</h3>
                    <ul>
                        <li><a href="/post/1">Python 入门指南</a></li>
                        <li><a href="/post/2">Django 教程</a></li>
                        <li><a href="/post/3">数据科学基础</a></li>
                    </ul>
                </div>
            </aside>
        </main>
        
        <footer class="site-footer">
            <p>&copy; 2024 技术博客</p>
        </footer>
    </body>
    </html>
    """
    
    root = parse_html(blog_html)
    
    print("\n📰 博客文章信息:\n")
    
    # 提取标题
    post_titles = find_by_class(root, "post-title")
    if post_titles:
        print(f"📝 文章标题：{post_titles[0].get_text().strip()}")
    
    # 提取作者
    authors = find_by_class(root, "author")
    if authors:
        print(f"👤 作者：{authors[0].get_text().strip()}")
    
    # 提取封面图
    cover_images = find_by_class(root, "post-cover")
    if cover_images:
        print(f"🖼️  封面：{cover_images[0].get_attribute('src')}")
    
    # 提取标签
    tags = find_by_class(root, "tag")
    print(f"🏷️  标签：{', '.join(t.get_text().strip() for t in tags)}")
    
    # 提取热门文章
    print("\n🔥 热门文章:")
    sidebar = find_by_class(root, "sidebar")
    if sidebar:
        hot_links = find_elements(sidebar[0], tag="a")
        for link in hot_links[:3]:
            href = link.get_attribute("href")
            text = link.get_text().strip()
            if href and text:
                print(f"   • {text}")
    
    # 提取所有链接统计
    all_links = extract_links(blog_html)
    internal = len([l for l in all_links if not l['href'].startswith('http')])
    external = len([l for l in all_links if l['href'].startswith('http')])
    print(f"\n🔗 链接统计：内部 {internal} 个，外部 {external} 个")


def example_advanced_search():
    """Example 10: Advanced Element Search"""
    print("\n" + "=" * 60)
    print("示例 10: 高级元素查找")
    print("=" * 60)
    
    html = """
    <div class="products">
        <div class="product" data-category="electronics" data-price="999">
            <h3>笔记本电脑</h3>
            <span class="price">¥9999</span>
            <span class="stock in-stock">有货</span>
        </div>
        <div class="product" data-category="electronics" data-price="299">
            <h3>无线耳机</h3>
            <span class="price">¥299</span>
            <span class="stock in-stock">有货</span>
        </div>
        <div class="product" data-category="books" data-price="59">
            <h3>Python 编程</h3>
            <span class="price">¥59</span>
            <span class="stock out-of-stock">缺货</span>
        </div>
        <div class="product" data-category="electronics" data-price="1999">
            <h3>平板电脑</h3>
            <span class="price">¥1999</span>
            <span class="stock in-stock">有货</span>
        </div>
    </div>
    """
    
    root = parse_html(html)
    
    print("\n🔍 查找演示:\n")
    
    # 查找所有产品
    all_products = find_by_class(root, "product")
    print(f"📦 所有产品：{len(all_products)} 个")
    
    # 查找有货的产品
    in_stock = find_by_class(root, "in-stock")
    print(f"✅ 有货产品：{len(in_stock)} 个")
    
    # 查找电子产品
    electronics = find_elements(root, attributes={"data-category": "electronics"})
    print(f"💻 电子产品：{len(electronics)} 个")
    
    # 查找价格低于 1000 的产品（需要后处理）
    print("\n💰 价格分析:")
    for product in all_products:
        name_elem = find_elements(product, tag="h3")
        price_elem = find_elements(product, tag="span", attributes={"class": "price"})
        
        if name_elem and price_elem:
            name = name_elem[0].get_text().strip()
            price_str = price_elem[0].get_text().strip()
            # 提取数字
            import re
            price_match = re.search(r'¥(\d+)', price_str)
            if price_match:
                price = int(price_match.group(1))
                print(f"   {name}: {price_str} {'✅' if price < 1000 else '❌'}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("AllToolkit - HTML Utilities 使用示例")
    print("=" * 60)
    
    try:
        example_basic_parsing()
        example_link_extraction()
        example_image_extraction()
        example_html_sanitization()
        example_html_generation()
        example_html_formatting()
        example_html_to_text()
        example_dom_analysis()
        example_real_world_scraping()
        example_advanced_search()
        
        print("\n" + "=" * 60)
        print("✅ 所有示例运行完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 示例运行出错：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
