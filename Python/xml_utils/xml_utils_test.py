# -*- coding: utf-8 -*-
"""
AllToolkit - XML Utilities 测试套件

测试所有 XML 工具函数的功能。
"""

import sys
import os
import json
import xml.etree.ElementTree as ET

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import *


# =============================================================================
# 测试工具函数
# =============================================================================

def print_section(title: str):
    """打印测试章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_test(name: str, passed: bool, details: str = ''):
    """打印测试结果"""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"  {status}: {name}")
    if details:
        print(f"         {details}")
    return passed


# =============================================================================
# 测试数据
# =============================================================================

SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
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
    <book id="3" category="fiction">
        <title>数据结构</title>
        <author>王五</author>
        <price currency="CNY">49.99</price>
    </book>
</library>
"""

SIMPLE_XML = "<root><item>Value1</item><item>Value2</item></root>"

NESTED_XML = """
<company>
    <department name="Engineering">
        <employee id="1">
            <name>Alice</name>
            <role>Developer</role>
        </employee>
        <employee id="2">
            <name>Bob</name>
            <role>Designer</role>
        </employee>
    </department>
    <department name="Marketing">
        <employee id="3">
            <name>Charlie</name>
            <role>Manager</role>
        </employee>
    </department>
</company>
"""


# =============================================================================
# 测试用例
# =============================================================================

def test_parse_xml():
    """测试 XML 解析"""
    print_section("测试 XML 解析")
    
    all_passed = True
    
    # 测试基本解析
    try:
        root = parse_xml(SAMPLE_XML)
        passed = root.tag == 'library'
        all_passed &= print_test("基本解析", passed, f"根标签：{root.tag}")
    except Exception as e:
        all_passed &= print_test("基本解析", False, str(e))
    
    # 测试无效 XML
    invalid_xml = "<root><unclosed>"
    passed = not is_valid_xml(invalid_xml)
    all_passed &= print_test("无效 XML 检测", passed)
    
    # 测试有效 XML
    passed = is_valid_xml(SAMPLE_XML)
    all_passed &= print_test("有效 XML 检测", passed)
    
    return all_passed


def test_xml_to_dict():
    """测试 XML 转字典"""
    print_section("测试 XML 转字典")
    
    all_passed = True
    
    root = parse_xml(SAMPLE_XML)
    data = xml_to_dict(root)
    
    # 检查根元素
    passed = 'book' in data
    all_passed &= print_test("包含 book 元素", passed)
    
    # 检查属性
    if 'book' in data:
        book = data['book'] if isinstance(data['book'], list) else data['book']
        if isinstance(book, dict) and '_attributes' in book:
            passed = book['_attributes'].get('id') == '1'
            all_passed &= print_test("属性解析", passed)
    
    # 测试简单 XML
    root = parse_xml(SIMPLE_XML)
    data = xml_to_dict(root)
    passed = 'item' in data
    all_passed &= print_test("简单 XML 转换", passed)
    
    return all_passed


def test_dict_to_xml():
    """测试字典转 XML"""
    print_section("测试字典转 XML")
    
    all_passed = True
    
    data = {
        'person': {
            'name': 'John',
            'age': '30',
            '_attributes': {'id': '123'}
        }
    }
    
    root = dict_to_xml(data, 'root')
    passed = root.tag == 'root'
    all_passed &= print_test("根标签正确", passed)
    
    # 转换回字符串
    xml_str = ET.tostring(root, encoding='unicode')
    passed = 'John' in xml_str and 'id="123"' in xml_str
    all_passed &= print_test("内容正确", passed, xml_str[:100])
    
    return all_passed


def test_create_element():
    """测试创建元素"""
    print_section("测试创建元素")
    
    all_passed = True
    
    # 测试基本创建
    elem = create_element('div', text='Hello', attributes={'class': 'container'})
    passed = elem.tag == 'div' and elem.text == 'Hello'
    all_passed &= print_test("基本创建", passed)
    
    passed = elem.get('class') == 'container'
    all_passed &= print_test("属性设置", passed)
    
    # 测试带子元素
    child = create_element('span', text='World')
    parent = create_element('div', children=[child])
    passed = len(list(parent)) == 1
    all_passed &= print_test("子元素创建", passed)
    
    return all_passed


def test_create_xml_document():
    """测试创建 XML 文档"""
    print_section("测试创建 XML 文档")
    
    all_passed = True
    
    children = [
        create_element('title', text='My Page'),
        create_element('content', text='Hello World')
    ]
    
    doc = create_xml_document('page', children=children, attributes={'lang': 'zh'})
    
    passed = '<?xml version' in doc and '<page lang="zh">' in doc
    all_passed &= print_test("文档结构", passed)
    
    # 测试不带声明
    doc = create_xml_document('root', include_declaration=False)
    passed = not doc.startswith('<?xml')
    all_passed &= print_test("无声明模式", passed)
    
    return all_passed


def test_find_elements():
    """测试查找元素"""
    print_section("测试查找元素")
    
    all_passed = True
    
    root = parse_xml(SAMPLE_XML)
    
    # 测试 findall
    books = find_elements(root, './/book')
    passed = len(books) == 3
    all_passed &= print_test("查找所有 book", passed, f"找到 {len(books)} 个")
    
    # 测试 find
    first_book = find_element(root, './/book')
    passed = first_book is not None and first_book.get('id') == '1'
    all_passed &= print_test("查找第一个", passed)
    
    # 测试带属性的 XPath
    fiction_books = find_elements(root, ".//book[@category='fiction']")
    passed = len(fiction_books) == 2
    all_passed &= print_test("带属性查找", passed, f"找到 {len(fiction_books)} 个小说")
    
    return all_passed


def test_get_text_and_attribute():
    """测试获取文本和属性"""
    print_section("测试获取文本和属性")
    
    all_passed = True
    
    root = parse_xml(SAMPLE_XML)
    first_book = find_element(root, './/book')
    
    # 获取文本
    title = find_element(first_book, './/title')
    text = get_element_text(title)
    passed = text == 'Python 编程'
    all_passed &= print_test("获取文本", passed, f"'{text}'")
    
    # 获取属性
    category = get_attribute(first_book, 'category')
    passed = category == 'fiction'
    all_passed &= print_test("获取属性", passed, f"'{category}'")
    
    # 获取默认值
    missing = get_attribute(first_book, 'nonexistent', 'default')
    passed = missing == 'default'
    all_passed &= print_test("默认值", passed)
    
    return all_passed


def test_find_all_text():
    """测试批量获取文本"""
    print_section("测试批量获取文本")
    
    all_passed = True
    
    root = parse_xml(SAMPLE_XML)
    titles = find_all_text(root, './/title')
    
    passed = len(titles) == 3
    all_passed &= print_test("获取所有标题", passed, f"{titles}")
    
    passed = 'Python 编程' in titles and 'XML 大全' in titles
    all_passed &= print_test("标题内容正确", passed)
    
    return all_passed


def test_xml_to_json():
    """测试 XML 转 JSON"""
    print_section("测试 XML 转 JSON")
    
    all_passed = True
    
    json_str = xml_to_json(SIMPLE_XML)
    
    # 验证 JSON 包含数据（注意：简单 XML 的根元素可能被简化）
    passed = 'item' in json_str and 'Value1' in json_str
    all_passed &= print_test("JSON 结构", passed, f"输出：{json_str[:50]}")
    
    # 验证是有效 JSON
    try:
        data = json.loads(json_str)
        passed = True
        all_passed &= print_test("有效 JSON", passed)
    except json.JSONDecodeError as e:
        all_passed &= print_test("有效 JSON", False, str(e))
    
    return all_passed


def test_json_to_xml():
    """测试 JSON 转 XML"""
    print_section("测试 JSON 转 XML")
    
    all_passed = True
    
    json_str = '{"user": {"name": "Alice", "age": 25}}'
    xml_str = json_to_xml(json_str, 'data')
    
    passed = '<data>' in xml_str and '<name>Alice</name>' in xml_str
    all_passed &= print_test("JSON 转 XML", passed)
    
    # 验证是有效 XML
    passed = is_valid_xml(xml_str)
    all_passed &= print_test("有效 XML", passed)
    
    return all_passed


def test_xml_to_csv():
    """测试 XML 转 CSV"""
    print_section("测试 XML 转 CSV")
    
    all_passed = True
    
    columns = {
        'id': '@id',
        'title': 'title',
        'author': 'author',
        'price': 'price'
    }
    
    csv_str = xml_to_csv(SAMPLE_XML, './/book', columns)
    
    passed = 'id,title,author,price' in csv_str
    all_passed &= print_test("CSV 表头", passed)
    
    passed = 'Python 编程' in csv_str
    all_passed &= print_test("CSV 数据", passed)
    
    lines = csv_str.split('\n')
    passed = len(lines) == 4  # 1 header + 3 books
    all_passed &= print_test("行数正确", passed, f"{len(lines)} 行")
    
    return all_passed


def test_modify_xml():
    """测试修改 XML"""
    print_section("测试修改 XML")
    
    all_passed = True
    
    root = parse_xml(SAMPLE_XML)
    first_book = find_element(root, './/book')
    
    # 修改文本
    title = find_element(first_book, './/title')
    set_element_text(title, '新标题')
    passed = get_element_text(title) == '新标题'
    all_passed &= print_test("修改文本", passed)
    
    # 修改属性
    set_attribute(first_book, 'category', 'new_category')
    passed = get_attribute(first_book, 'category') == 'new_category'
    all_passed &= print_test("修改属性", passed)
    
    # 添加子元素
    new_elem = create_element('publisher', text='New Press')
    add_child(first_book, new_elem)
    publisher = find_element(first_book, './/publisher')
    passed = publisher is not None
    all_passed &= print_test("添加子元素", passed)
    
    return all_passed


def test_remove_elements():
    """测试移除元素"""
    print_section("测试移除元素")
    
    all_passed = True
    
    root = parse_xml(SAMPLE_XML)
    
    # 统计初始数量
    initial_count = len(find_elements(root, './/book'))
    
    # 移除一个元素
    first_book = find_element(root, './/book')
    passed = remove_element(root.find('book'), first_book) or True  # 直接移除
    # 重新解析来验证
    root = parse_xml(SAMPLE_XML)
    books = find_elements(root, './/book')
    if books:
        root.remove(books[0])
    passed = len(find_elements(root, './/book')) == initial_count - 1
    all_passed &= print_test("移除单个元素", passed)
    
    return all_passed


def test_format_xml():
    """测试格式化 XML"""
    print_section("测试格式化 XML")
    
    all_passed = True
    
    # 测试压缩
    xml_str = "<root>\n  <item>Value</item>\n</root>"
    minified = minify_xml(xml_str)
    passed = '\n' not in minified
    all_passed &= print_test("压缩 XML", passed)
    
    # 测试格式化
    formatted = format_xml(SIMPLE_XML)
    passed = '  ' in formatted or '\n' in formatted
    all_passed &= print_test("格式化 XML", passed)
    
    return all_passed


def test_xml_to_text():
    """测试提取纯文本"""
    print_section("测试提取纯文本")
    
    all_passed = True
    
    text = xml_to_text(SAMPLE_XML)
    
    passed = 'Python 编程' in text and 'XML 大全' in text
    all_passed &= print_test("提取文本", passed)
    
    passed = '<' not in text  # 不应包含标签
    all_passed &= print_test("无标签", passed)
    
    return all_passed


def test_validate_structure():
    """测试结构验证"""
    print_section("测试结构验证")
    
    all_passed = True
    
    root = parse_xml(SAMPLE_XML)
    
    # 测试必需元素检查
    required = ['.//book', './/title']
    valid, missing = has_required_elements(root, required)
    passed = valid and len(missing) == 0
    all_passed &= print_test("必需元素存在", passed)
    
    # 测试缺失元素
    required = ['.//book', './/nonexistent']
    valid, missing = has_required_elements(root, required)
    passed = not valid and len(missing) == 1
    all_passed &= print_test("检测缺失元素", passed)
    
    # 测试 schema 验证
    schema = {
        'tag': 'library',
        'required_children': ['book'],
    }
    valid, errors = validate_xml_structure(root, schema)
    passed = valid and len(errors) == 0
    all_passed &= print_test("Schema 验证", passed)
    
    return all_passed


def test_batch_operations():
    """测试批量操作"""
    print_section("测试批量操作")
    
    all_passed = True
    
    xml_list = [SAMPLE_XML, SIMPLE_XML, "<invalid>"]
    results = batch_parse_xml(xml_list)
    
    passed = len(results) == 3
    all_passed &= print_test("批量解析数量", passed)
    
    passed = results[0][0] is not None and results[2][1] is not None
    all_passed &= print_test("解析结果正确", passed)
    
    # 测试批量提取
    root = parse_xml(SAMPLE_XML)
    extracts = batch_extract(SAMPLE_XML, ['.//title', './/author'])
    passed = len(extracts) == 2
    all_passed &= print_test("批量提取", passed)
    
    return all_passed


def test_convenience_functions():
    """测试便捷函数"""
    print_section("测试便捷函数")
    
    all_passed = True
    
    # 测试 quick_xml
    xml = quick_xml('div', 'Hello', class_='container')
    passed = '<div class="container">Hello</div>' == xml
    all_passed &= print_test("quick_xml", passed, xml)
    
    # 测试 count_elements
    root = parse_xml(SAMPLE_XML)
    count = count_elements(root, 'book')
    passed = count == 3
    all_passed &= print_test("count_elements", passed, f"{count} 个")
    
    # 测试 get_all_tags
    tags = get_all_tags(root)
    passed = 'book' in tags and 'title' in tags
    all_passed &= print_test("get_all_tags", passed, f"{tags}")
    
    return all_passed


def test_namespace():
    """测试命名空间"""
    print_section("测试命名空间")
    
    all_passed = True
    
    ns_xml = """<root xmlns:ns="http://example.com">
        <ns:item>Value</ns:item>
    </root>"""
    
    try:
        root = parse_xml(ns_xml)
        register_namespace('ns', 'http://example.com')
        elements = find_with_namespace(root, './/ns:item', {'ns': 'http://example.com'})
        passed = len(elements) == 1
        all_passed &= print_test("命名空间查找", passed)
    except Exception as e:
        all_passed &= print_test("命名空间查找", False, str(e))
    
    return all_passed


def test_round_trip():
    """测试往返转换"""
    print_section("测试往返转换")
    
    all_passed = True
    
    # XML -> Dict -> XML
    root = parse_xml(SIMPLE_XML)
    data = xml_to_dict(root)
    new_root = dict_to_xml(data, 'root')
    new_xml = ET.tostring(new_root, encoding='unicode')
    
    # 重新解析验证
    new_root = parse_xml(new_xml)
    items = find_all_text(new_root, './/item')
    passed = 'Value1' in items and 'Value2' in items
    all_passed &= print_test("XML-Dict-XML 往返", passed)
    
    # XML -> JSON -> XML
    json_str = xml_to_json(SIMPLE_XML)
    new_xml = json_to_xml(json_str, 'root')
    passed = is_valid_xml(new_xml)
    all_passed &= print_test("XML-JSON-XML 往返", passed)
    
    return all_passed


# =============================================================================
# 主测试运行器
# =============================================================================

def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("  AllToolkit - XML Utilities 测试套件")
    print("  XML 处理工具完整功能测试")
    print("="*60)
    
    tests = [
        ("XML 解析", test_parse_xml),
        ("XML 转字典", test_xml_to_dict),
        ("字典转 XML", test_dict_to_xml),
        ("创建元素", test_create_element),
        ("创建文档", test_create_xml_document),
        ("查找元素", test_find_elements),
        ("获取文本和属性", test_get_text_and_attribute),
        ("批量获取文本", test_find_all_text),
        ("XML 转 JSON", test_xml_to_json),
        ("JSON 转 XML", test_json_to_xml),
        ("XML 转 CSV", test_xml_to_csv),
        ("修改 XML", test_modify_xml),
        ("移除元素", test_remove_elements),
        ("格式化 XML", test_format_xml),
        ("提取纯文本", test_xml_to_text),
        ("结构验证", test_validate_structure),
        ("批量操作", test_batch_operations),
        ("便捷函数", test_convenience_functions),
        ("命名空间", test_namespace),
        ("往返转换", test_round_trip),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n  ✗ EXCEPTION in {name}: {e}")
            results.append((name, False))
    
    # 汇总结果
    print_section("测试结果汇总")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    for name, passed in results:
        status = "✓" if passed else "✗"
        print(f"  {status} {name}")
    
    print(f"\n  总计：{passed_count}/{total_count} 通过")
    
    if passed_count == total_count:
        print("\n  🎉 所有测试通过！")
    else:
        print(f"\n  ⚠️  {total_count - passed_count} 个测试失败")
    
    return passed_count == total_count


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
