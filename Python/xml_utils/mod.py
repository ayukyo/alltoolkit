# -*- coding: utf-8 -*-
"""
AllToolkit - XML Utilities 📄

零依赖 XML 处理工具库，提供解析、创建、查询、转换等功能。
完全使用 Python 标准库实现（xml.etree.ElementTree, re, json），无需任何外部依赖。

Author: AllToolkit Team
License: MIT
Version: 1.0.0
"""

import xml.etree.ElementTree as ET
import json
import re
from typing import Dict, Any, Optional, List, Union, Tuple
from io import StringIO


# =============================================================================
# 常量定义
# =============================================================================

SUPPORTED_FORMATS = ['xml', 'json', 'dict']

XML_DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>'


# =============================================================================
# XML 解析工具
# =============================================================================

def parse_xml(xml_string: str) -> ET.Element:
    """
    解析 XML 字符串为 ElementTree
    
    Args:
        xml_string: XML 格式的字符串
    
    Returns:
        ElementTree 根元素
    
    Raises:
        ET.ParseError: 当 XML 格式无效时
    """
    return ET.fromstring(xml_string)


def parse_xml_file(file_path: str) -> ET.Element:
    """
    解析 XML 文件
    
    Args:
        file_path: XML 文件路径
    
    Returns:
        ElementTree 根元素
    
    Raises:
        FileNotFoundError: 文件不存在
        ET.ParseError: XML 格式无效
    """
    tree = ET.parse(file_path)
    return tree.getroot()


def xml_to_dict(element: ET.Element, include_attributes: bool = True, max_depth: int = 100) -> Dict[str, Any]:
    """
    将 XML Element 转换为字典
    
    Args:
        element: XML Element
        include_attributes: 是否包含属性
        max_depth: 最大递归深度（防止无限递归）
    
    Returns:
        嵌套字典结构
    
    Note:
        优化版本：添加深度限制防止栈溢出，
        改进空元素和纯文本元素的边界处理。
    """
    # 边界处理：空元素或超过最大深度
    if element is None:
        return {}
    
    def _convert(elem: ET.Element, depth: int) -> Union[Dict[str, Any], str]:
        # 深度限制保护
        if depth > max_depth:
            return {'_error': 'max_depth_exceeded', '_tag': elem.tag}
        
        result = {}
        
        # 处理文本内容
        text = (elem.text or '').strip()
        if text:
            result['_text'] = text
        
        # 处理属性
        if include_attributes and elem.attrib:
            result['_attributes'] = dict(elem.attrib)
        
        # 处理子元素
        children = {}
        child_count = 0
        for child in elem:
            child_count += 1
            child_dict = _convert(child, depth + 1)
            
            if child.tag in children:
                # 如果已存在，转换为列表
                if not isinstance(children[child.tag], list):
                    children[child.tag] = [children[child.tag]]
                children[child.tag].append(child_dict)
            else:
                children[child.tag] = child_dict
        
        result.update(children)
        
        # 优化：如果没有子元素和属性，直接返回文本
        if len(result) == 1 and '_text' in result:
            return result['_text']
        
        # 边界处理：空元素返回空字典而非 None
        if not result:
            return {}
        
        return result
    
    return _convert(element, 0)


def dict_to_xml(data: Dict[str, Any], root_tag: str = 'root') -> ET.Element:
    """
    将字典转换为 XML Element
    
    Args:
        data: 字典数据
        root_tag: 根元素标签名
    
    Returns:
        XML Element
    """
    def _build_element(tag: str, value: Any) -> ET.Element:
        elem = ET.Element(tag)
        
        if isinstance(value, dict):
            # 处理特殊键
            if '_text' in value:
                elem.text = str(value['_text'])
            if '_attributes' in value:
                for k, v in value['_attributes'].items():
                    elem.set(k, str(v))
            
            # 处理子元素
            for k, v in value.items():
                if k not in ('_text', '_attributes'):
                    elem.append(_build_element(k, v))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    elem.append(_build_element(tag, item))
                else:
                    child = ET.Element(tag)
                    child.text = str(item)
                    elem.append(child)
        else:
            elem.text = str(value)
        
        return elem
    
    return _build_element(root_tag, data)


# =============================================================================
# XML 创建工具
# =============================================================================

def create_element(tag: str, text: Optional[str] = None, 
                   attributes: Optional[Dict[str, str]] = None,
                   children: Optional[List[ET.Element]] = None) -> ET.Element:
    """
    创建 XML 元素
    
    Args:
        tag: 标签名
        text: 文本内容
        attributes: 属性字典
        children: 子元素列表
    
    Returns:
        创建的 XML Element
    """
    elem = ET.Element(tag)
    
    if text:
        elem.text = text
    
    if attributes:
        for k, v in attributes.items():
            elem.set(k, str(v))
    
    if children:
        for child in children:
            elem.append(child)
    
    return elem


def create_xml_document(root_tag: str, 
                        children: Optional[List[ET.Element]] = None,
                        attributes: Optional[Dict[str, str]] = None,
                        include_declaration: bool = True) -> str:
    """
    创建完整的 XML 文档字符串
    
    Args:
        root_tag: 根元素标签
        children: 子元素列表
        attributes: 根元素属性
        include_declaration: 是否包含 XML 声明
    
    Returns:
        XML 文档字符串
    """
    root = create_element(root_tag, attributes=attributes, children=children)
    
    declaration = XML_DECLARATION + '\n' if include_declaration else ''
    return declaration + ET.tostring(root, encoding='unicode')


# =============================================================================
# XML 查询工具
# =============================================================================

def find_elements(root: ET.Element, xpath: str) -> List[ET.Element]:
    """
    使用 XPath 查找元素
    
    Args:
        root: 根元素
        xpath: XPath 表达式
    
    Returns:
        匹配的元素列表
    """
    return root.findall(xpath)


def find_element(root: ET.Element, xpath: str) -> Optional[ET.Element]:
    """
    查找单个元素
    
    Args:
        root: 根元素
        xpath: XPath 表达式
    
    Returns:
        匹配的第一个元素，未找到返回 None
    """
    return root.find(xpath)


def get_element_text(element: ET.Element, default: str = '') -> str:
    """
    获取元素文本内容
    
    Args:
        element: XML 元素
        default: 默认值
    
    Returns:
        文本内容
    """
    return (element.text or '').strip() if element is not None else default


def get_attribute(element: ET.Element, attr_name: str, default: str = '') -> str:
    """
    获取元素属性值
    
    Args:
        element: XML 元素
        attr_name: 属性名
        default: 默认值
    
    Returns:
        属性值
    """
    return element.get(attr_name, default) if element is not None else default


def find_all_text(root: ET.Element, xpath: str) -> List[str]:
    """
    查找所有匹配元素的文本内容
    
    Args:
        root: 根元素
        xpath: XPath 表达式
    
    Returns:
        文本内容列表
    """
    elements = find_elements(root, xpath)
    return [get_element_text(elem) for elem in elements]


# =============================================================================
# XML 转换工具
# =============================================================================

def xml_to_json(xml_string: str, indent: int = 2) -> str:
    """
    将 XML 转换为 JSON 字符串
    
    Args:
        xml_string: XML 字符串
        indent: JSON 缩进空格数
    
    Returns:
        JSON 字符串
    """
    root = parse_xml(xml_string)
    data = xml_to_dict(root)
    return json.dumps(data, indent=indent, ensure_ascii=False)


def json_to_xml(json_string: str, root_tag: str = 'root') -> str:
    """
    将 JSON 转换为 XML 字符串
    
    Args:
        json_string: JSON 字符串
        root_tag: 根元素标签
    
    Returns:
        XML 字符串
    """
    data = json.loads(json_string)
    root = dict_to_xml(data, root_tag)
    return ET.tostring(root, encoding='unicode')


def xml_to_csv(xml_string: str, row_xpath: str, column_xpaths: Dict[str, str]) -> str:
    """
    将 XML 转换为 CSV 格式
    
    Args:
        xml_string: XML 字符串
        row_xpath: 行元素的 XPath
        column_xpaths: 列名到 XPath 的映射（@attr 表示属性）
    
    Returns:
        CSV 字符串
    
    Example:
        columns = {'ID': '@id', 'Name': 'name', 'Price': 'price'}
        csv = xml_to_csv(xml, './/product', columns)
    """
    root = parse_xml(xml_string)
    rows = find_elements(root, row_xpath)
    
    # 构建 CSV
    lines = []
    
    # 表头
    headers = list(column_xpaths.keys())
    lines.append(','.join(headers))
    
    # 数据行
    for row in rows:
        values = []
        for col_name, xpath in column_xpaths.items():
            # 处理属性（@attr 语法）
            if xpath.startswith('@'):
                attr_name = xpath[1:]
                value = row.get(attr_name, '')
            else:
                elem = find_element(row, xpath)
                value = get_element_text(elem, '')
            
            # 处理包含逗号或引号的值
            if ',' in value or '"' in value or '\n' in value:
                value = '"' + value.replace('"', '""') + '"'
            values.append(value)
        lines.append(','.join(values))
    
    return '\n'.join(lines)


# =============================================================================
# XML 修改工具
# =============================================================================

def set_element_text(element: ET.Element, text: str) -> ET.Element:
    """
    设置元素文本
    
    Args:
        element: XML 元素
        text: 新文本
    
    Returns:
        修改后的元素
    """
    element.text = text
    return element


def set_attribute(element: ET.Element, attr_name: str, attr_value: str) -> ET.Element:
    """
    设置元素属性
    
    Args:
        element: XML 元素
        attr_name: 属性名
        attr_value: 属性值
    
    Returns:
        修改后的元素
    """
    element.set(attr_name, attr_value)
    return element


def add_child(parent: ET.Element, child: ET.Element, index: Optional[int] = None) -> ET.Element:
    """
    添加子元素
    
    Args:
        parent: 父元素
        child: 子元素
        index: 插入位置（None 表示追加）
    
    Returns:
        添加的子元素
    """
    if index is not None:
        parent.insert(index, child)
    else:
        parent.append(child)
    return child


def remove_element(parent: ET.Element, child: ET.Element) -> bool:
    """
    移除子元素
    
    Args:
        parent: 父元素
        child: 要移除的子元素
    
    Returns:
        是否成功移除
    """
    try:
        parent.remove(child)
        return True
    except ValueError:
        return False


def remove_elements_by_xpath(root: ET.Element, xpath: str) -> int:
    """
    根据 XPath 批量移除元素
    
    Args:
        root: 根元素
        xpath: XPath 表达式
    
    Returns:
        移除的元素数量
    """
    elements = find_elements(root, xpath)
    count = 0
    
    # 需要找到父元素来移除
    for elem in elements:
        # 查找父元素
        for parent in root.iter():
            if elem in list(parent):
                parent.remove(elem)
                count += 1
                break
    
    return count


# =============================================================================
# XML 验证工具
# =============================================================================

def is_valid_xml(xml_string: str) -> bool:
    """
    检查 XML 是否有效
    
    Args:
        xml_string: XML 字符串
    
    Returns:
        是否有效
    """
    try:
        ET.fromstring(xml_string)
        return True
    except ET.ParseError:
        return False


def has_required_elements(root: ET.Element, required_xpaths: List[str]) -> Tuple[bool, List[str]]:
    """
    检查是否包含所有必需元素
    
    Args:
        root: 根元素
        required_xpaths: 必需的 XPath 列表
    
    Returns:
        (是否全部存在，缺失的 XPath 列表)
    """
    missing = []
    for xpath in required_xpaths:
        if find_element(root, xpath) is None:
            missing.append(xpath)
    
    return len(missing) == 0, missing


def validate_xml_structure(root: ET.Element, schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    验证 XML 结构是否符合简单 schema
    
    Schema 格式:
    {
        'tag': 'root',
        'required_children': ['child1', 'child2'],
        'optional_children': ['opt1'],
        'required_attributes': ['id'],
        'children_schema': {
            'child1': {'required_attributes': ['name']}
        }
    }
    
    Args:
        root: 根元素
        schema: Schema 定义
    
    Returns:
        (是否有效，错误列表)
    """
    errors = []
    
    # 检查标签名
    if 'tag' in schema and root.tag != schema['tag']:
        errors.append(f"根标签错误：期望 '{schema['tag']}', 实际 '{root.tag}'")
    
    # 检查必需子元素
    if 'required_children' in schema:
        child_tags = [child.tag for child in root]
        for required in schema['required_children']:
            if required not in child_tags:
                errors.append(f"缺少必需子元素：{required}")
    
    # 检查必需属性
    if 'required_attributes' in schema:
        for attr in schema['required_attributes']:
            if attr not in root.attrib:
                errors.append(f"根元素缺少必需属性：{attr}")
    
    # 递归检查子元素 schema
    if 'children_schema' in schema:
        for child in root:
            if child.tag in schema['children_schema']:
                child_schema = schema['children_schema'][child.tag]
                valid, child_errors = validate_xml_structure(child, child_schema)
                errors.extend([f"{child.tag}: {e}" for e in child_errors])
    
    return len(errors) == 0, errors


# =============================================================================
# XML 格式化工具
# =============================================================================

def format_xml(xml_string: str, indent: str = '  ') -> str:
    """
    格式化 XML 字符串（美化输出）
    
    Args:
        xml_string: XML 字符串
        indent: 缩进字符串
    
    Returns:
        格式化后的 XML 字符串
    """
    try:
        root = parse_xml(xml_string)
        # Python 3.9+ 支持 ET.indent，旧版本使用自定义格式化
        if hasattr(ET, 'indent'):
            ET.indent(root, space=indent)
            return ET.tostring(root, encoding='unicode')
        else:
            # 简单的格式化实现
            xml_str = ET.tostring(root, encoding='unicode')
            return _simple_indent(xml_str, indent)
    except ET.ParseError:
        return xml_string


def _simple_indent(xml_string: str, indent: str = '  ') -> str:
    """
    简单的 XML 格式化（用于 Python 3.8 及以下）
    
    Args:
        xml_string: XML 字符串
        indent: 缩进字符串
    
    Returns:
        格式化后的 XML 字符串
    """
    result = []
    depth = 0
    
    # 分割标签
    import re
    parts = re.split(r'(<[^>]+>)', xml_string)
    
    for part in parts:
        if not part.strip():
            continue
        
        # 处理结束标签
        if part.startswith('</'):
            depth = max(0, depth - 1)
            result.append(indent * depth + part)
        # 处理自闭合标签
        elif part.startswith('<') and part.endswith('/>'):
            result.append(indent * depth + part)
        # 处理开始标签
        elif part.startswith('<') and not part.startswith('<?'):
            result.append(indent * depth + part)
            depth += 1
        # 处理文本内容
        elif part.strip():
            result.append(indent * depth + part.strip())
        # XML 声明
        elif part.startswith('<?'):
            result.append(part)
    
    return '\n'.join(result)


def minify_xml(xml_string: str) -> str:
    """
    压缩 XML 字符串（移除空白）
    
    Args:
        xml_string: XML 字符串
    
    Returns:
        压缩后的 XML 字符串
    """
    # 移除 XML 声明前后的空白
    xml_string = xml_string.strip()
    
    # 移除标签间的空白和换行
    xml_string = re.sub(r'>\s+<', '><', xml_string)
    
    return xml_string


def xml_to_text(xml_string: str) -> str:
    """
    提取 XML 中的所有文本内容
    
    Args:
        xml_string: XML 字符串
    
    Returns:
        纯文本内容
    """
    root = parse_xml(xml_string)
    texts = []
    
    for elem in root.iter():
        if elem.text:
            texts.append(elem.text.strip())
        if elem.tail:
            texts.append(elem.tail.strip())
    
    return ' '.join(filter(None, texts))


# =============================================================================
# 批量处理工具
# =============================================================================

def batch_parse_xml(xml_strings: List[str]) -> List[Tuple[Optional[ET.Element], Optional[str]]]:
    """
    批量解析 XML 字符串
    
    Args:
        xml_strings: XML 字符串列表
    
    Returns:
        (Element, None) 或 (None, 错误信息) 的列表
    """
    results = []
    for xml_str in xml_strings:
        try:
            elem = parse_xml(xml_str)
            results.append((elem, None))
        except ET.ParseError as e:
            results.append((None, str(e)))
    return results


def batch_extract(xml_string: str, xpaths: List[str]) -> Dict[str, List[str]]:
    """
    批量提取多个 XPath 的值
    
    Args:
        xml_string: XML 字符串
        xpaths: XPath 列表
    
    Returns:
        {xpath: [值 1, 值 2, ...]} 字典
    """
    root = parse_xml(xml_string)
    results = {}
    
    for xpath in xpaths:
        elements = find_elements(root, xpath)
        results[xpath] = [get_element_text(elem) for elem in elements]
    
    return results


# =============================================================================
# 命名空间工具
# =============================================================================

def register_namespace(prefix: str, uri: str):
    """
    注册 XML 命名空间
    
    Args:
        prefix: 命名空间前缀
        uri: 命名空间 URI
    """
    ET.register_namespace(prefix, uri)


def find_with_namespace(root: ET.Element, tag: str, namespace: Dict[str, str]) -> List[ET.Element]:
    """
    在命名空间中查找元素
    
    Args:
        root: 根元素
        tag: 标签名
        namespace: 命名空间映射 {prefix: uri}
    
    Returns:
        匹配的元素列表
    """
    return root.findall(tag, namespace)


# =============================================================================
# 便捷函数
# =============================================================================

def quick_xml(tag: str, text: str = '', **attrs) -> str:
    """
    快速创建简单 XML 元素
    
    Args:
        tag: 标签名
        text: 文本内容
        **attrs: 属性键值对（class_ 会自动转换为 class）
    
    Returns:
        XML 字符串
    
    Example:
        quick_xml('div', 'Hello', class_='container', id='main')
        → <div class="container" id="main">Hello</div>
    """
    # 处理 Python 关键字参数（class_ → class, for_ → for 等）
    processed_attrs = {}
    for k, v in attrs.items():
        # 移除末尾的下划线（Python 关键字转义）
        attr_name = k.rstrip('_')
        processed_attrs[attr_name] = v
    
    elem = create_element(tag, text=text, attributes=processed_attrs if processed_attrs else None)
    return ET.tostring(elem, encoding='unicode')


def xml_tree(root: ET.Element) -> str:
    """
    将 ElementTree 转换为格式化的字符串
    
    Args:
        root: 根元素
    
    Returns:
        格式化的 XML 字符串
    """
    ET.indent(root, space='  ')
    return ET.tostring(root, encoding='unicode')


def count_elements(root: ET.Element, tag: Optional[str] = None) -> int:
    """
    统计元素数量
    
    Args:
        root: 根元素
        tag: 指定标签名（None 表示统计所有）
    
    Returns:
        元素数量
    """
    if tag:
        return len(find_elements(root, f'.//{tag}'))
    return sum(1 for _ in root.iter())


def get_all_tags(root: ET.Element) -> List[str]:
    """
    获取所有唯一的标签名
    
    Args:
        root: 根元素
    
    Returns:
        标签名列表
    """
    return list(set(elem.tag for elem in root.iter()))


# =============================================================================
# 模块导出
# =============================================================================

__all__ = [
    # 解析
    'parse_xml',
    'parse_xml_file',
    'xml_to_dict',
    'dict_to_xml',
    
    # 创建
    'create_element',
    'create_xml_document',
    
    # 查询
    'find_elements',
    'find_element',
    'get_element_text',
    'get_attribute',
    'find_all_text',
    
    # 转换
    'xml_to_json',
    'json_to_xml',
    'xml_to_csv',
    
    # 修改
    'set_element_text',
    'set_attribute',
    'add_child',
    'remove_element',
    'remove_elements_by_xpath',
    
    # 验证
    'is_valid_xml',
    'has_required_elements',
    'validate_xml_structure',
    
    # 格式化
    'format_xml',
    'minify_xml',
    'xml_to_text',
    
    # 批量处理
    'batch_parse_xml',
    'batch_extract',
    
    # 命名空间
    'register_namespace',
    'find_with_namespace',
    
    # 便捷函数
    'quick_xml',
    'xml_tree',
    'count_elements',
    'get_all_tags',
    
    # 常量
    'XML_DECLARATION',
    'SUPPORTED_FORMATS',
]
