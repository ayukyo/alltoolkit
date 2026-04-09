# -*- coding: utf-8 -*-
"""
AllToolkit - XML Utilities 示例 3: 实际应用场景

演示 RSS 生成、配置文件处理、数据验证等实际应用场景。
"""

import sys
import os
# 添加父目录到路径（mod.py 在上一级目录）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import *


def create_rss_feed():
    """创建 RSS 订阅源"""
    print("\n【1】创建 RSS 订阅源")
    print("-"*40)
    
    # 博客文章数据
    posts = [
        {
            'title': 'Python XML 处理完全指南',
            'link': 'https://blog.example.com/python-xml',
            'description': '详细介绍如何使用 Python 处理 XML 数据',
            'pub_date': '2024-01-15',
            'author': '张三'
        },
        {
            'title': 'Web 开发最佳实践',
            'link': 'https://blog.example.com/web-best-practices',
            'description': '分享现代 Web 开发的经验和技巧',
            'pub_date': '2024-01-10',
            'author': '李四'
        },
        {
            'title': '数据库优化技巧',
            'link': 'https://blog.example.com/db-optimization',
            'description': '提升数据库性能的实用方法',
            'pub_date': '2024-01-05',
            'author': '王五'
        },
    ]
    
    # 创建 RSS 项目
    items = []
    for post in posts:
        item = create_element('item', children=[
            create_element('title', text=post['title']),
            create_element('link', text=post['link']),
            create_element('description', text=post['description']),
            create_element('pubDate', text=post['pub_date']),
            create_element('author', text=post['author']),
        ])
        items.append(item)
    
    # 创建 channel
    channel = create_element('channel', children=[
        create_element('title', text='技术博客'),
        create_element('link', text='https://blog.example.com'),
        create_element('description', text='分享编程技术和经验'),
        create_element('language', text='zh-cn'),
    ] + items)
    
    # 创建完整 RSS 文档
    rss = create_xml_document('rss', children=[channel], attributes={'version': '2.0'})
    
    print("生成的 RSS 订阅源:")
    print(format_xml(rss)[:500] + "...")
    
    return rss


def process_config_file():
    """处理配置文件"""
    print("\n【2】处理配置文件")
    print("-"*40)
    
    config_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <application>
        <database>
            <host>localhost</host>
            <port>5432</port>
            <name>myapp_db</name>
            <user>admin</user>
            <password encrypted="true">xxx123</password>
        </database>
        <server>
            <host>0.0.0.0</host>
            <port>8080</port>
            <workers>4</workers>
            <debug>false</debug>
        </server>
        <logging>
            <level>INFO</level>
            <file>/var/log/myapp.log</file>
            <max_size>100MB</max_size>
            <rotation>daily</rotation>
        </logging>
        <features>
            <feature name="user_auth" enabled="true"/>
            <feature name="api_v2" enabled="true"/>
            <feature name="dark_mode" enabled="false"/>
        </features>
    </application>
    """
    
    root = parse_xml(config_xml)
    
    # 读取数据库配置
    db = find_element(root, './/database')
    print("数据库配置:")
    print(f"  主机：{get_element_text(find_element(db, 'host'))}")
    print(f"  端口：{get_element_text(find_element(db, 'port'))}")
    print(f"  数据库：{get_element_text(find_element(db, 'name'))}")
    
    # 读取服务器配置
    server = find_element(root, './/server')
    print("\n服务器配置:")
    print(f"  监听：{get_element_text(find_element(server, 'host'))}:{get_element_text(find_element(server, 'port'))}")
    print(f"  工作进程：{get_element_text(find_element(server, 'workers'))}")
    
    # 读取功能开关
    print("\n功能开关:")
    for feature in find_elements(root, './/feature'):
        name = get_attribute(feature, 'name')
        enabled = get_attribute(feature, 'enabled')
        status = "✓ 开启" if enabled == 'true' else "✗ 关闭"
        print(f"  {name}: {status}")
    
    # 修改配置
    level = find_element(root, './/level')
    set_element_text(level, 'DEBUG')
    print(f"\n日志级别已修改为：{get_element_text(level)}")


def validate_data():
    """数据验证"""
    print("\n【3】数据验证")
    print("-"*40)
    
    # 有效的用户数据
    valid_user = """
    <user id="U001">
        <name>张三</name>
        <email>zhangsan@example.com</email>
        <phone>13800138000</phone>
        <age>28</age>
    </user>
    """
    
    # 无效的用户数据（缺少必需字段）
    invalid_user = """
    <user id="U002">
        <name>李四</name>
        <age>25</age>
    </user>
    """
    
    # 定义验证规则
    schema = {
        'tag': 'user',
        'required_children': ['name', 'email', 'phone'],
        'required_attributes': ['id'],
    }
    
    # 验证有效数据
    print("验证有效用户数据:")
    root = parse_xml(valid_user)
    valid, errors = validate_xml_structure(root, schema)
    if valid:
        print("  ✓ 验证通过")
    else:
        for err in errors:
            print(f"  ✗ {err}")
    
    # 验证无效数据
    print("\n验证无效用户数据:")
    root = parse_xml(invalid_user)
    valid, errors = validate_xml_structure(root, schema)
    if valid:
        print("  ✓ 验证通过")
    else:
        for err in errors:
            print(f"  ✗ {err}")
    
    # 检查必需元素
    print("\n检查必需元素:")
    required = ['.//name', './/email', './/phone']
    valid, missing = has_required_elements(root, required)
    if not valid:
        print(f"  缺失元素：{missing}")


def batch_process():
    """批量处理 XML 数据"""
    print("\n【4】批量处理")
    print("-"*40)
    
    # 模拟多个 XML 文档
    xml_documents = [
        "<article><title>文章 1</title><author>作者 A</author></article>",
        "<article><title>文章 2</title><author>作者 B</author></article>",
        "<article><title>文章 3</title><author>作者 C</author></article>",
        "<invalid>",  # 无效 XML
    ]
    
    print("批量解析 XML 文档:")
    results = batch_parse_xml(xml_documents)
    
    for i, (root, error) in enumerate(results):
        if error:
            print(f"  文档 {i+1}: ✗ 解析失败 - {error}")
        else:
            title = get_element_text(find_element(root, './/title'))
            author = get_element_text(find_element(root, './/author'))
            print(f"  文档 {i+1}: ✓ {title} by {author}")
    
    # 批量提取数据
    print("\n批量提取数据:")
    valid_xml = """
    <articles>
        <article><title>标题 A</title><category>技术</category></article>
        <article><title>标题 B</title><category>生活</category></article>
        <article><title>标题 C</title><category>技术</category></article>
    </articles>
    """
    
    xpaths = ['.//title', './/category']
    extracted = batch_extract(valid_xml, xpaths)
    
    for xpath, values in extracted.items():
        print(f"  {xpath}: {values}")


def generate_sitemap():
    """生成网站地图"""
    print("\n【5】生成网站地图 (Sitemap)")
    print("-"*40)
    
    # 网站页面数据
    pages = [
        {'loc': 'https://example.com/', 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': 'https://example.com/about', 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': 'https://example.com/products', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://example.com/blog', 'priority': '0.7', 'changefreq': 'daily'},
        {'loc': 'https://example.com/contact', 'priority': '0.5', 'changefreq': 'yearly'},
    ]
    
    # 创建 URL 元素
    url_elements = []
    for page in pages:
        url = create_element('url', children=[
            create_element('loc', text=page['loc']),
            create_element('changefreq', text=page['changefreq']),
            create_element('priority', text=page['priority']),
        ])
        url_elements.append(url)
    
    # 创建 sitemap
    sitemap = create_xml_document('urlset', children=url_elements, 
                                   attributes={'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'})
    
    print("生成的 Sitemap:")
    print(format_xml(sitemap))


def main():
    print("="*60)
    print("  XML Utilities 实际应用场景示例")
    print("="*60)
    
    create_rss_feed()
    process_config_file()
    validate_data()
    batch_process()
    generate_sitemap()
    
    print("\n" + "="*60)
    print("  示例完成！")
    print("="*60)


if __name__ == '__main__':
    main()
