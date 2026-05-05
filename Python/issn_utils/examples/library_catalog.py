#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ISSN Utilities - 图书馆目录示例
模拟图书馆系统中ISSN的使用场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    is_valid_issn, is_issn8, is_issn13,
    format_issn, clean_issn,
    issn8_to_issn13, issn13_to_issn8,
    compare_issns, find_issns_in_text,
    validate_issns, parse_issn,
)


class JournalCatalog:
    """模拟图书馆期刊目录"""
    
    def __init__(self):
        self.journals = {}
    
    def add_journal(self, issn: str, title: str, publisher: str, 
                    year_start: int = None, frequency: str = None):
        """添加期刊到目录"""
        if not is_valid_issn(issn):
            raise ValueError(f"无效的ISSN: {issn}")
        
        # 统一使用ISSN-8作为内部存储键
        key = clean_issn(issn) if is_issn8(issn) else issn13_to_issn8(issn)
        
        info = parse_issn(issn)
        self.journals[key] = {
            'title': title,
            'publisher': publisher,
            'issn8': info['issn8'],
            'issn13': info['issn13'],
            'issn_l': info['issn_l'],
            'year_start': year_start,
            'frequency': frequency,
        }
        
        return key
    
    def find_journal(self, issn: str):
        """根据ISSN查找期刊"""
        if not is_valid_issn(issn):
            return None
        
        key = clean_issn(issn) if is_issn8(issn) else issn13_to_issn8(issn)
        return self.journals.get(key)
    
    def search_by_title(self, keyword: str):
        """按标题关键词搜索"""
        results = []
        for journal in self.journals.values():
            if keyword.lower() in journal['title'].lower():
                results.append(journal)
        return results
    
    def is_same_journal(self, issn1: str, issn2: str):
        """判断两个ISSN是否指向同一期刊"""
        return compare_issns(issn1, issn2)


def demo_catalog():
    """演示图书馆目录功能"""
    print("\n【图书馆期刊目录演示】")
    
    catalog = JournalCatalog()
    
    # 添加期刊
    journals_data = [
        ("0028-0836", "Nature", "Nature Publishing Group", 1869, "Weekly"),
        ("0001-0782", "Communications of the ACM", "ACM", 1957, "Monthly"),
        ("0036-8075", "Science", "AAAS", 1880, "Weekly"),
        ("0018-9448", "IEEE Transactions on Information Theory", "IEEE", 1963, "Bimonthly"),
    ]
    
    print("\n  添加期刊:")
    for issn, title, publisher, year, freq in journals_data:
        key = catalog.add_journal(issn, title, publisher, year, freq)
        print(f"    ✓ {title} (ISSN: {format_issn(issn)})")
    
    # 查找期刊
    print("\n  ISSN查找:")
    search_issns = ["0028-0836", "9770028083002"]  # ISSN-8 和 ISSN-13
    for issn in search_issns:
        journal = catalog.find_journal(issn)
        if journal:
            print(f"    找到: {journal['title']}")
            print(f"      ISSN-8: {format_issn(journal['issn8'])}")
            print(f"      ISSN-13: {format_issn(journal['issn13'])}")
        else:
            print(f"    未找到: {issn}")
    
    # 关键词搜索
    print("\n  关键词搜索 'IEEE':")
    results = catalog.search_by_title("IEEE")
    for j in results:
        print(f"    {j['title']}")
    
    # ISSN对比
    print("\n  ISSN对比:")
    print(f"    '0028-0836' 和 '9770028083002' 是否同一期刊: ", end="")
    print(catalog.is_same_journal("0028-0836", "9770028083002"))


def demo_text_extraction():
    """演示文本中提取ISSN"""
    print("\n【文本ISSN提取演示】")
    
    text = """
    本图书馆订阅以下期刊：
    1. Nature (ISSN: 0028-0836)
    2. Science (ISSN 0036-8075)
    3. IEEE Transactions on Information Theory, ISSN-L: 0018-9448
    4. Communications of the ACM (0001-0782)
    
    请查阅 ISSN-L: 0028-0836 的在线版本。
    """
    
    print(f"\n  原文:\n{text}")
    
    found = find_issns_in_text(text)
    print(f"\n  提取到 {len(found)} 个ISSN:")
    for issn in found:
        info = parse_issn(issn)
        print(f"    {format_issn(issn)} - 类型: {info['type']}")


def demo_batch_validation():
    """演示批量验证"""
    print("\n【批量ISSN验证演示】")
    
    issns = [
        "0028-0836",     # 有效
        "0001-0782",     # 有效
        "9770028083002", # 有效 ISSN-13
        "invalid",       # 无效
        "0028-0837",     # 无效（错误检验位）
        "2434-561X",     # 有效（X检验位）
    ]
    
    print("\n  输入ISSN列表:")
    for issn in issns:
        print(f"    {issn}")
    
    results = validate_issns(issns)
    
    print("\n  验证结果:")
    valid_count = 0
    invalid_count = 0
    for issn, info in results.items():
        if info['valid']:
            valid_count += 1
            print(f"    ✓ {issn:15s} - {info['type']}")
        else:
            invalid_count += 1
            print(f"    ✗ {issn:15s} - 无效")
    
    print(f"\n  统计: {valid_count} 有效, {invalid_count} 无效")


def main():
    print("=" * 60)
    print("ISSN Utilities - 图书馆目录示例")
    print("=" * 60)
    
    demo_catalog()
    demo_text_extraction()
    demo_batch_validation()
    
    print("\n" + "=" * 60)
    print("完成！")


if __name__ == "__main__":
    main()