#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VCard Utilities - 基础使用示例

演示 VCard 工具模块的基本功能。

Author: AllToolkit
"""

import os
import sys

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 直接导入模块文件
import importlib.util
spec = importlib.util.spec_from_file_location("mod", os.path.join(parent_dir, "mod.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# 使用导入的模块
create_vcard = mod.create_vcard
parse_vcard = mod.parse_vcard
save_vcard = mod.save_vcard
validate_vcard = mod.validate_vcard
vcard_to_string = mod.vcard_to_string
vcard_to_dict = mod.vcard_to_dict
dict_to_vcard = mod.dict_to_vcard
quick_business_card = mod.quick_business_card
quick_personal_card = mod.quick_personal_card
get_contact_summary = mod.get_contact_summary
get_module_info = mod.get_module_info


def example_basic_vcard():
    """基本 VCard 创建示例。"""
    print("=" * 50)
    print("1. 基本 VCard 创建")
    print("=" * 50)
    
    # 创建基本名片
    card = create_vcard("张三")
    
    # 转换为字符串
    vcard_str = vcard_to_string(card)
    print(vcard_str)
    
    return card


def example_full_vcard():
    """完整 VCard 创建示例。"""
    print("\n" + "=" * 50)
    print("2. 完整 VCard 创建")
    print("=" * 50)
    
    # 创建带完整信息的名片
    card = create_vcard(
        full_name="李四",
        family_name="李",
        given_name="四",
        organization="科技有限公司",
        title="软件工程师",
        phones=[
            {"number": "13800138000", "type": "cell"},
            {"number": "010-12345678", "type": "work"},
            {"number": "010-87654321", "type": "fax"}
        ],
        emails=[
            {"address": "lisi@techcorp.com", "type": "work"},
            {"address": "lisi@home.com", "type": "home"}
        ],
        addresses=[
            {
                "street": "中关村科技园区1号楼",
                "city": "北京",
                "region": "北京市",
                "postal_code": "100080",
                "country": "中国",
                "type": "work"
            }
        ],
        urls=["https://techcorp.com", "https://lisi.dev"],
        birthday="1990-05-20",
        note="技术专家，负责核心系统开发"
    )
    
    # 转换为字符串
    vcard_str = vcard_to_string(card)
    print(vcard_str)
    
    # 验证
    valid, errors = validate_vcard(card)
    print(f"\n验证结果: {valid}")
    if errors:
        print(f"错误: {errors}")
    
    return card


def example_quick_cards():
    """快速创建示例。"""
    print("\n" + "=" * 50)
    print("3. 快速名片创建")
    print("=" * 50)
    
    # 快速商务名片
    business_card = quick_business_card(
        name="王五",
        company="金融集团",
        title="项目经理",
        phone="13900139000",
        email="wangwu@finance.com",
        website="https://finance.com"
    )
    
    print("商务名片:")
    print(vcard_to_string(business_card))
    
    # 快速个人名片
    personal_card = quick_personal_card(
        name="小明",
        phone="13800138000",
        email="xiaoming@example.com",
        birthday="1995-03-15"
    )
    
    print("\n个人名片:")
    print(vcard_to_string(personal_card))


def example_parse_vcard():
    """解析 VCard 示例。"""
    print("\n" + "=" * 50)
    print("4. VCard 解析")
    print("=" * 50)
    
    # VCard 字符串
    vcard_str = """BEGIN:VCARD
VERSION:3.0
FN:赵六
N:赵;六;;;;
ORG:电子商务公司;
TITLE:产品经理
TEL;TYPE=cell:13800138000
EMAIL;TYPE=work:zhaoliu@ecommerce.com
URL:https://ecommerce.com
NOTE:负责产品规划
END:VCARD"""
    
    # 解析
    card = parse_vcard(vcard_str)
    
    print(f"姓名: {card.full_name}")
    print(f"组织: {card.organization.name if card.organization else 'N/A'}")
    print(f"职位: {card.title}")
    print(f"电话: {card.phones[0].number if card.phones else 'N/A'}")
    print(f"邮箱: {card.emails[0].address if card.emails else 'N/A'}")
    print(f"备注: {card.note}")
    
    return card


def example_dict_conversion():
    """字典转换示例。"""
    print("\n" + "=" * 50)
    print("5. 字典转换")
    print("=" * 50)
    
    # 创建名片
    card = create_vcard(
        full_name="钱七",
        phones=[{"number": "13800138000", "type": "cell"}],
        emails=[{"address": "qianqi@example.com"}]
    )
    
    # VCard → 字典
    data = vcard_to_dict(card)
    print("VCard → 字典:")
    print(f"  full_name: {data['full_name']}")
    print(f"  phones: {data['phones']}")
    print(f"  emails: {data['emails']}")
    
    # 字典 → VCard
    new_card = dict_to_vcard(data)
    print("\n字典 → VCard:")
    print(f"  姓名: {new_card.full_name}")


def example_save_vcard():
    """保存 VCard 示例。"""
    print("\n" + "=" * 50)
    print("6. VCard 保存")
    print("=" * 50)
    
    # 创建名片
    card = create_vcard(
        full_name="孙八",
        phones=[{"number": "13800138000"}],
        emails=[{"address": "sunba@example.com"}]
    )
    
    # 保存到临时文件
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        vcf_path = os.path.join(temp_dir, "sunba.vcf")
        save_vcard(card, vcf_path)
        
        print(f"已保存到: {vcf_path}")
        
        # 读取并解析
        with open(vcf_path, 'r') as f:
            content = f.read()
        
        print("\n文件内容:")
        print(content)


def example_contact_summary():
    """联系人摘要示例。"""
    print("\n" + "=" * 50)
    print("7. 联系人摘要")
    print("=" * 50)
    
    # 创建名片
    card = create_vcard(
        full_name="周九",
        organization="科技公司",
        title="技术总监",
        phones=[
            {"number": "13800138000", "type": "cell"},
            {"number": "010-12345678", "type": "work"}
        ],
        emails=[{"address": "zhoujiu@tech.com", "type": "work"}]
    )
    
    # 获取摘要
    summary = get_contact_summary(card)
    print(summary)


def example_module_info():
    """模块信息示例。"""
    print("\n" + "=" * 50)
    print("8. 模块信息")
    print("=" * 50)
    
    info = get_module_info()
    for key, value in info.items():
        print(f"{key}: {value}")


def main():
    """运行所有示例。"""
    print("VCard Utilities 使用示例")
    print("=" * 50)
    
    example_basic_vcard()
    example_full_vcard()
    example_quick_cards()
    example_parse_vcard()
    example_dict_conversion()
    example_save_vcard()
    example_contact_summary()
    example_module_info()
    
    print("\n" + "=" * 50)
    print("所有示例完成！")
    print("=" * 50)


if __name__ == '__main__':
    main()