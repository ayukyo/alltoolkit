# -*- coding: utf-8 -*-
"""
AllToolkit - XML Utilities 示例 2: 数据转换

演示 XML 与 JSON、CSV 之间的转换。
"""

import sys
import os
import json
# 添加父目录到路径（mod.py 在上一级目录）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import *


def main():
    print("="*60)
    print("  XML Utilities 数据转换示例")
    print("="*60)
    
    
    # ==================== 1. XML 转 JSON ====================
    print("\n【1】XML 转 JSON")
    print("-"*40)
    
    xml_str = """
    <person>
        <name>张三</name>
        <age>28</age>
        <email>zhangsan@example.com</email>
        <address>
            <city>北京</city>
            <district>朝阳区</district>
            <street>建国路 88 号</street>
        </address>
        <skills>
            <skill>Python</skill>
            <skill>JavaScript</skill>
            <skill>SQL</skill>
        </skills>
    </person>
    """
    
    print("原始 XML:")
    print(xml_str.strip())
    
    # 转换为 JSON
    json_str = xml_to_json(xml_str, indent=2)
    print("\n转换后的 JSON:")
    print(json_str)
    
    # 验证 JSON 有效性
    data = json.loads(json_str)
    print(f"\n✓ JSON 解析成功")
    print(f"  姓名：{data.get('name', data.get('person', {}).get('name', 'N/A'))}")
    print(f"  技能：{data.get('skills', data.get('person', {}).get('skills', 'N/A'))}")
    
    
    # ==================== 2. JSON 转 XML ====================
    print("\n【2】JSON 转 XML")
    print("-"*40)
    
    json_data = {
        'product': {
            '_attributes': {'id': 'P001'},
            'name': '智能手机',
            'brand': '华为',
            'price': '4999',
            'specs': {
                'screen': '6.5 英寸',
                'memory': '256GB',
                'camera': '4800 万像素'
            },
            'colors': {
                'color': ['黑色', '白色', '蓝色']
            }
        }
    }
    
    print("原始 JSON:")
    print(json.dumps(json_data, indent=2, ensure_ascii=False))
    
    # 转换为 XML
    xml_result = json_to_xml(json.dumps(json_data, ensure_ascii=False), 'catalog')
    print("\n转换后的 XML:")
    print(format_xml(xml_result))
    
    
    # ==================== 3. XML 转 CSV ====================
    print("\n【3】XML 转 CSV")
    print("-"*40)
    
    products_xml = """
    <products>
        <product id="1">
            <name>iPhone 15</name>
            <brand>Apple</brand>
            <price>6999</price>
            <stock>100</stock>
        </product>
        <product id="2">
            <name>Galaxy S24</name>
            <brand>Samsung</brand>
            <price>5999</price>
            <stock>150</stock>
        </product>
        <product id="3">
            <name>Mi 14</name>
            <brand>Xiaomi</brand>
            <price>3999</price>
            <stock>200</stock>
        </product>
    </products>
    """
    
    print("原始 XML:")
    print(products_xml.strip())
    
    # 定义列映射
    columns = {
        'ID': '@id',
        '产品名称': 'name',
        '品牌': 'brand',
        '价格': 'price',
        '库存': 'stock'
    }
    
    # 转换为 CSV
    csv_data = xml_to_csv(products_xml, './/product', columns)
    print("\n转换后的 CSV:")
    print(csv_data)
    
    # 保存为文件示例
    print("\n💡 提示：可将 CSV 数据写入文件")
    print("  with open('products.csv', 'w', encoding='utf-8') as f:")
    print("      f.write(csv_data)")
    
    
    # ==================== 4. 复杂嵌套转换 ====================
    print("\n【4】复杂嵌套结构转换")
    print("-"*40)
    
    complex_xml = """
    <company>
        <department name="技术部">
            <employees>
                <employee id="E001">
                    <name>Alice</name>
                    <position>工程师</position>
                    <salary>25000</salary>
                </employee>
                <employee id="E002">
                    <name>Bob</name>
                    <position>设计师</position>
                    <salary>22000</salary>
                </employee>
            </employees>
        </department>
        <department name="市场部">
            <employees>
                <employee id="E003">
                    <name>Charlie</name>
                    <position>经理</position>
                    <salary>30000</salary>
                </employee>
            </employees>
        </department>
    </company>
    """
    
    print("复杂 XML 结构:")
    print(format_xml(complex_xml))
    
    # 转换为 JSON
    json_result = xml_to_json(complex_xml)
    print("\n转换为 JSON:")
    print(json_result)
    
    # 提取部门信息为 CSV
    dept_columns = {
        '部门名称': '@name',
        '员工数量': 'count(employees/employee)'  # 注意：ElementTree XPath 支持有限
    }
    
    # 手动统计员工数
    root = parse_xml(complex_xml)
    print("\n部门统计:")
    for dept in find_elements(root, './/department'):
        dept_name = get_attribute(dept, 'name')
        emp_count = len(find_elements(dept, './/employee'))
        print(f"  {dept_name}: {emp_count} 人")
    
    
    # ==================== 5. 往返转换验证 ====================
    print("\n【5】往返转换验证")
    print("-"*40)
    
    original_xml = """
    <data>
        <item key="a">Value A</item>
        <item key="b">Value B</item>
    </data>
    """
    
    print("原始 XML:")
    print(original_xml.strip())
    
    # XML → JSON → XML
    json_intermediate = xml_to_json(original_xml)
    back_to_xml = json_to_xml(json_intermediate, 'data')
    
    print("\nXML → JSON → XML 结果:")
    print(back_to_xml)
    
    # 验证数据完整性
    new_root = parse_xml(back_to_xml)
    items = find_all_text(new_root, './/item')
    print(f"\n数据完整性检查：{items}")
    print(f"✓ 转换成功：{'Value A' in items and 'Value B' in items}")
    
    
    print("\n" + "="*60)
    print("  示例完成！")
    print("="*60)


if __name__ == '__main__':
    main()
