# -*- coding: utf-8 -*-
"""
AllToolkit - XML Utilities 示例 1: 基础用法

演示 XML 解析、查询、创建等基本操作。
"""

import sys
import os
# 添加父目录到路径（mod.py 在上一级目录）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import *


def main():
    print("="*60)
    print("  XML Utilities 基础用法示例")
    print("="*60)
    
    # ==================== 1. 解析 XML ====================
    print("\n【1】解析 XML 字符串")
    print("-"*40)
    
    xml_str = """<?xml version="1.0" encoding="UTF-8"?>
    <library>
        <book id="1" category="fiction">
            <title>Python 编程</title>
            <author>张三</author>
            <price currency="CNY">59.99</price>
        </book>
        <book id="2" category="tech">
            <title>XML 大全</title>
            <author>李四</author>
            <price currency="CNY">79.99</price>
        </book>
    </library>
    """
    
    # 解析
    root = parse_xml(xml_str)
    print(f"根元素标签：{root.tag}")
    
    # 验证有效性
    print(f"XML 有效：{is_valid_xml(xml_str)}")
    
    
    # ==================== 2. 查询元素 ====================
    print("\n【2】查询元素")
    print("-"*40)
    
    # 查找所有 book 元素
    books = find_elements(root, './/book')
    print(f"找到 {len(books)} 本书")
    
    # 查找第一个 book
    first_book = find_element(root, './/book')
    print(f"第一本书 ID: {get_attribute(first_book, 'id')}")
    print(f"第一本书分类：{get_attribute(first_book, 'category')}")
    
    # 获取所有标题
    titles = find_all_text(root, './/title')
    print(f"所有标题：{titles}")
    
    # 带条件查找
    fiction_books = find_elements(root, ".//book[@category='fiction']")
    print(f"小说类书籍：{len(fiction_books)} 本")
    
    
    # ==================== 3. 创建 XML ====================
    print("\n【3】创建 XML 元素")
    print("-"*40)
    
    # 创建简单元素
    elem = create_element('div', text='Hello World', attributes={'class': 'container'})
    print(f"创建元素：{quick_xml('span', '内联文本', style='color:red')}")
    
    # 创建带子元素的文档
    children = [
        create_element('title', text='我的页面'),
        create_element('content', text='欢迎访问'),
    ]
    doc = create_xml_document('page', children=children, attributes={'lang': 'zh-CN'})
    print("创建文档:")
    print(doc)
    
    
    # ==================== 4. XML 转字典 ====================
    print("\n【4】XML 转字典")
    print("-"*40)
    
    data = xml_to_dict(root)
    print("转换结果:")
    for key, value in data.items():
        print(f"  {key}: {value}")
    
    
    # ==================== 5. 修改 XML ====================
    print("\n【5】修改 XML")
    print("-"*40)
    
    # 修改文本
    title = find_element(first_book, './/title')
    old_text = get_element_text(title)
    set_element_text(title, 'Python 编程（第 2 版）')
    print(f"修改标题：'{old_text}' → '{get_element_text(title)}'")
    
    # 修改属性
    old_cat = get_attribute(first_book, 'category')
    set_attribute(first_book, 'category', 'programming')
    print(f"修改分类：'{old_cat}' → '{get_attribute(first_book, 'category')}'")
    
    # 添加新元素
    new_elem = create_element('publisher', text='科技出版社')
    add_child(first_book, new_elem)
    publisher = find_element(first_book, './/publisher')
    print(f"添加出版社：{get_element_text(publisher)}")
    
    
    # ==================== 6. 统计信息 ====================
    print("\n【6】统计信息")
    print("-"*40)
    
    root = parse_xml(xml_str)  # 重新解析
    print(f"book 元素数量：{count_elements(root, 'book')}")
    print(f"所有标签：{get_all_tags(root)}")
    
    
    # ==================== 7. 格式化 ====================
    print("\n【7】格式化 XML")
    print("-"*40)
    
    compact_xml = "<root><item>A</item><item>B</item></root>"
    print(f"压缩前：{compact_xml}")
    print(f"格式化后:")
    print(format_xml(compact_xml))
    
    pretty_xml = """<root>
        <item>Value</item>
    </root>"""
    print(f"\n原始:\n{pretty_xml}")
    print(f"\n压缩后：{minify_xml(pretty_xml)}")
    
    
    # ==================== 8. 提取纯文本 ====================
    print("\n【8】提取纯文本")
    print("-"*40)
    
    text = xml_to_text(xml_str)
    print(f"提取的文本：{text[:100]}...")
    
    
    print("\n" + "="*60)
    print("  示例完成！")
    print("="*60)


if __name__ == '__main__':
    main()
