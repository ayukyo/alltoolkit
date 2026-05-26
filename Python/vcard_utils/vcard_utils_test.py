#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - VCard Utilities Test Suite

Comprehensive test suite for vcard_utils module.

Author: AllToolkit
License: MIT
"""

import unittest
import tempfile
import os
from datetime import date
from pathlib import Path

# Import the module
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vcard_utils.mod import (
    create_vcard,
    parse_vcard,
    parse_vcards,
    save_vcard,
    save_vcards,
    validate_vcard,
    vcard_to_string,
    vcard_to_dict,
    dict_to_vcard,
    quick_business_card,
    quick_personal_card,
    get_contact_summary,
    get_supported_versions,
    get_supported_properties,
    get_module_info,
    VCard,
    VCardName,
    VCardPhone,
    VCardEmail,
    VCardAddress,
    VCardOrganization,
    VCardFileNotFoundError,
    VCardFormatError,
)


class TestVCardCreation(unittest.TestCase):
    """测试 VCard 创建功能。"""
    
    def test_create_basic_vcard(self):
        """测试创建基本 VCard。"""
        card = create_vcard("张三")
        self.assertEqual(card.full_name, "张三")
        self.assertEqual(card.version, "3.0")
        self.assertTrue(card.uid)
    
    def test_create_vcard_with_details(self):
        """测试创建带详细信息的 VCard。"""
        card = create_vcard(
            full_name="李四",
            family_name="李",
            given_name="四",
            organization="科技公司",
            title="工程师",
            phones=[{"number": "13800138000", "type": "cell"}],
            emails=[{"address": "lisi@example.com", "type": "work"}],
            birthday="1990-05-20"
        )
        
        self.assertEqual(card.full_name, "李四")
        self.assertEqual(card.name.family_name, "李")
        self.assertEqual(card.name.given_name, "四")
        self.assertEqual(card.organization.name, "科技公司")
        self.assertEqual(card.title, "工程师")
        self.assertEqual(len(card.phones), 1)
        self.assertEqual(len(card.emails), 1)
        self.assertEqual(card.birthday, date(1990, 5, 20))
    
    def test_create_vcard_with_multiple_contacts(self):
        """测试创建多个联系方式的 VCard。"""
        card = create_vcard(
            full_name="王五",
            phones=[
                {"number": "13800138000", "type": "cell"},
                {"number": "010-12345678", "type": "work"},
                {"number": "010-87654321", "type": "fax"}
            ],
            emails=[
                {"address": "wangwu@work.com", "type": "work"},
                {"address": "wangwu@home.com", "type": "home"}
            ]
        )
        
        self.assertEqual(len(card.phones), 3)
        self.assertEqual(len(card.emails), 2)
    
    def test_quick_business_card(self):
        """测试快速创建商务名片。"""
        card = quick_business_card(
            name="赵六",
            company="大公司",
            title="经理",
            phone="13900139000",
            email="zhaoliu@bigcorp.com",
            website="https://bigcorp.com"
        )
        
        self.assertEqual(card.full_name, "赵六")
        self.assertEqual(card.organization.name, "大公司")
        self.assertEqual(card.title, "经理")
        self.assertEqual(len(card.urls), 1)
    
    def test_quick_personal_card(self):
        """测试快速创建个人名片。"""
        card = quick_personal_card(
            name="小明",
            phone="13800138000",
            email="xiaoming@example.com",
            birthday="1995-03-15"
        )
        
        self.assertEqual(card.full_name, "小明")
        self.assertEqual(card.birthday, date(1995, 3, 15))


class TestVCardToString(unittest.TestCase):
    """测试 VCard 转字符串功能。"""
    
    def test_basic_vcard_string(self):
        """测试基本 VCard 字符串转换。"""
        card = create_vcard("测试用户")
        vcard_str = vcard_to_string(card)
        
        self.assertIn("BEGIN:VCARD", vcard_str)
        self.assertIn("END:VCARD", vcard_str)
        self.assertIn("VERSION:3.0", vcard_str)
        self.assertIn("FN:测试用户", vcard_str)
    
    def test_vcard_string_with_organization(self):
        """测试带组织信息的 VCard 字符串。"""
        card = create_vcard(
            full_name="张三",
            organization="测试公司",
            title="开发工程师"
        )
        vcard_str = vcard_to_string(card)
        
        self.assertIn("ORG:测试公司", vcard_str)
        self.assertIn("TITLE:开发工程师", vcard_str)
    
    def test_vcard_string_with_contacts(self):
        """测试带联系方式的 VCard 字符串。"""
        card = create_vcard(
            full_name="李四",
            phones=[{"number": "13800138000", "type": "cell"}],
            emails=[{"address": "test@example.com", "type": "work"}]
        )
        vcard_str = vcard_to_string(card)
        
        self.assertIn("TEL;", vcard_str)
        self.assertIn("13800138000", vcard_str)
        self.assertIn("EMAIL;", vcard_str)
        self.assertIn("test@example.com", vcard_str)
    
    def test_vcard_string_with_birthday(self):
        """测试带生日的 VCard 字符串。"""
        card = create_vcard(
            full_name="王五",
            birthday="1990-01-01"
        )
        vcard_str = vcard_to_string(card)
        
        self.assertIn("BDAY:1990-01-01", vcard_str)


class TestVCardParsing(unittest.TestCase):
    """测试 VCard 解析功能。"""
    
    def test_parse_basic_vcard(self):
        """测试解析基本 VCard。"""
        vcard_str = """BEGIN:VCARD
VERSION:3.0
FN:张三
END:VCARD"""
        
        card = parse_vcard(vcard_str)
        self.assertEqual(card.full_name, "张三")
        self.assertEqual(card.version, "3.0")
    
    def test_parse_vcard_with_details(self):
        """测试解析带详细信息的 VCard。"""
        vcard_str = """BEGIN:VCARD
VERSION:3.0
FN:李四
N:李;四;;;;
ORG:测试公司;
TITLE:工程师
TEL;TYPE=cell:13800138000
EMAIL:test@example.com
ADR:;;测试街道;北京;北京;100000;中国
END:VCARD"""
        
        card = parse_vcard(vcard_str)
        
        self.assertEqual(card.full_name, "李四")
        self.assertEqual(card.name.family_name, "李")
        self.assertEqual(card.name.given_name, "四")
        self.assertEqual(card.organization.name, "测试公司")
        self.assertEqual(card.title, "工程师")
        self.assertEqual(len(card.phones), 1)
        self.assertEqual(card.phones[0].number, "13800138000")
        self.assertEqual(len(card.emails), 1)
        self.assertEqual(len(card.addresses), 1)
    
    def test_parse_invalid_vcard(self):
        """测试解析无效 VCard。"""
        invalid_str = "INVALID VCARD"
        
        with self.assertRaises(VCardFormatError):
            parse_vcard(invalid_str)
    
    def test_parse_vcard_from_file(self):
        """测试从文件解析 VCard。"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write("BEGIN:VCARD\nVERSION:3.0\nFN:文件测试\nEND:VCARD")
            temp_path = f.name
        
        try:
            card = parse_vcard(temp_path)
            self.assertEqual(card.full_name, "文件测试")
        finally:
            os.unlink(temp_path)
    
    def test_parse_vcards_multiple(self):
        """测试解析多个 VCard。"""
        vcard_str = """BEGIN:VCARD
VERSION:3.0
FN:张三
END:VCARD
BEGIN:VCARD
VERSION:3.0
FN:李四
END:VCARD"""
        
        cards = parse_vcards(vcard_str)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0].full_name, "张三")
        self.assertEqual(cards[1].full_name, "李四")


class TestVCardSaving(unittest.TestCase):
    """测试 VCard 保存功能。"""
    
    def test_save_single_vcard(self):
        """测试保存单个 VCard。"""
        card = create_vcard("保存测试")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = os.path.join(temp_dir, "test.vcf")
            save_vcard(card, temp_path)
            
            # 验证文件存在
            self.assertTrue(os.path.exists(temp_path))
            
            # 验证内容
            with open(temp_path, 'r') as f:
                content = f.read()
            
            self.assertIn("BEGIN:VCARD", content)
            self.assertIn("FN:保存测试", content)
    
    def test_save_multiple_vcards(self):
        """测试保存多个 VCard。"""
        cards = [
            create_vcard("张三"),
            create_vcard("李四"),
            create_vcard("王五")
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = os.path.join(temp_dir, "contacts.vcf")
            save_vcards(cards, temp_path)
            
            # 验证文件存在
            self.assertTrue(os.path.exists(temp_path))
            
            # 验证内容
            with open(temp_path, 'r') as f:
                content = f.read()
            
            self.assertIn("张三", content)
            self.assertIn("李四", content)
            self.assertIn("王五", content)


class TestVCardValidation(unittest.TestCase):
    """测试 VCard 验证功能。"""
    
    def test_validate_valid_vcard(self):
        """测试验证有效 VCard。"""
        card = create_vcard("张三")
        valid, errors = validate_vcard(card)
        
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_vcard_missing_fn(self):
        """测试验证缺少 FN 的 VCard。"""
        card = VCard()
        valid, errors = validate_vcard(card)
        
        self.assertFalse(valid)
        self.assertTrue(any("FN" in e for e in errors))
    
    def test_validate_vcard_invalid_email(self):
        """测试验证无效邮箱。"""
        card = create_vcard("张三")
        card.emails.append(VCardEmail(address="invalid-email"))
        
        valid, errors = validate_vcard(card)
        self.assertFalse(valid)
    
    def test_validate_vcard_invalid_version(self):
        """测试验证无效版本。"""
        card = create_vcard("张三")
        card.version = "5.0"
        
        valid, errors = validate_vcard(card)
        self.assertFalse(valid)


class TestVCardConversion(unittest.TestCase):
    """测试 VCard 转换功能。"""
    
    def test_vcard_to_dict(self):
        """测试 VCard 转字典。"""
        card = create_vcard(
            full_name="张三",
            phones=[{"number": "13800138000"}]
        )
        
        data = vcard_to_dict(card)
        
        self.assertEqual(data['full_name'], "张三")
        self.assertEqual(len(data['phones']), 1)
        self.assertEqual(data['phones'][0]['number'], "13800138000")
    
    def test_dict_to_vcard(self):
        """测试字典转 VCard。"""
        data = {
            'full_name': '李四',
            'phones': [{'number': '13900139000', 'type': 'cell'}],
            'emails': [{'address': 'lisi@example.com'}]
        }
        
        card = dict_to_vcard(data)
        
        self.assertEqual(card.full_name, "李四")
        self.assertEqual(len(card.phones), 1)
        self.assertEqual(len(card.emails), 1)


class TestVCardUtilities(unittest.TestCase):
    """测试 VCard 工具功能。"""
    
    def test_get_contact_summary(self):
        """测试获取联系人摘要。"""
        card = create_vcard(
            full_name="张三",
            organization="测试公司",
            title="工程师",
            phones=[{"number": "13800138000", "type": "cell"}]
        )
        
        summary = get_contact_summary(card)
        
        self.assertIn("张三", summary)
        self.assertIn("测试公司", summary)
        self.assertIn("13800138000", summary)
    
    def test_get_supported_versions(self):
        """测试获取支持的版本。"""
        versions = get_supported_versions()
        
        self.assertIn("2.1", versions)
        self.assertIn("3.0", versions)
        self.assertIn("4.0", versions)
    
    def test_get_supported_properties(self):
        """测试获取支持的属性。"""
        properties = get_supported_properties()
        
        self.assertIn("FN", properties)
        self.assertIn("TEL", properties)
        self.assertIn("EMAIL", properties)
    
    def test_get_module_info(self):
        """测试获取模块信息。"""
        info = get_module_info()
        
        self.assertEqual(info['name'], 'vcard_utils')
        self.assertTrue(info['version'])


class TestVCardName(unittest.TestCase):
    """测试 VCardName 数据类。"""
    
    def test_name_string(self):
        """测试姓名字符串。"""
        name = VCardName(family_name="张", given_name="三")
        self.assertEqual(str(name), "张 三")
    
    def test_name_vcard_format(self):
        """测试姓名 VCard 格式。"""
        name = VCardName(
            family_name="张",
            given_name="三",
            additional_names=["小明"],
            honorific_prefixes=["Dr."]
        )
        
        vcard_format = name.to_vcard_format()
        self.assertIn("张", vcard_format)
        self.assertIn("三", vcard_format)


class TestVCardAddress(unittest.TestCase):
    """测试 VCardAddress 数据类。"""
    
    def test_address_string(self):
        """测试地址字符串。"""
        addr = VCardAddress(
            street="测试街道",
            city="北京",
            country="中国"
        )
        
        self.assertIn("测试街道", str(addr))
        self.assertIn("北京", str(addr))
    
    def test_address_vcard_format(self):
        """测试地址 VCard 格式。"""
        addr = VCardAddress(
            street="测试街道",
            city="北京",
            postal_code="100000"
        )
        
        vcard_format = addr.to_vcard_format()
        self.assertIn("测试街道", vcard_format)
        self.assertIn("北京", vcard_format)


class TestVCardRoundTrip(unittest.TestCase):
    """测试 VCard 循环转换。"""
    
    def test_create_parse_roundtrip(self):
        """测试创建-解析循环。"""
        original = create_vcard(
            full_name="循环测试",
            phones=[{"number": "13800138000", "type": "cell"}],
            emails=[{"address": "test@example.com"}]
        )
        
        vcard_str = vcard_to_string(original)
        parsed = parse_vcard(vcard_str)
        
        self.assertEqual(parsed.full_name, original.full_name)
        self.assertEqual(len(parsed.phones), len(original.phones))
        self.assertEqual(len(parsed.emails), len(original.emails))
    
    def test_dict_roundtrip(self):
        """测试字典循环。"""
        original = create_vcard(
            full_name="字典循环",
            phones=[{"number": "13900139000"}]
        )
        
        data = vcard_to_dict(original)
        restored = dict_to_vcard(data)
        
        self.assertEqual(restored.full_name, original.full_name)


class TestVCardFileNotFound(unittest.TestCase):
    """测试文件不存在异常。"""
    
    def test_parse_nonexistent_file(self):
        """测试解析不存在的文件。"""
        with self.assertRaises(VCardFileNotFoundError):
            parse_vcard("/nonexistent/path/to/file.vcf")


if __name__ == '__main__':
    unittest.main(verbosity=2)