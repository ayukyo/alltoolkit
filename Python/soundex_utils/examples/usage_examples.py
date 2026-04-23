"""
SOUNDEX 工具模块使用示例

演示 SOUNDEX 编码、姓名匹配、相似度计算等功能的实际应用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    SoundexEncoder,
    SoundexRefinedEncoder,
    SoundexSQL,
    encode,
    similarity,
    matches,
    find_similar,
    group_by_sound,
    COMMON_NAMES,
)


def example_basic_usage():
    """基本使用示例"""
    print("\n" + "=" * 50)
    print("示例 1: 基本使用")
    print("=" * 50)
    
    encoder = SoundexEncoder()
    
    # 编码单个姓名
    names = ["Smith", "Smythe", "Schmidt", "Johnson", "Williams"]
    print("\n姓名编码:")
    for name in names:
        code = encoder.encode(name)
        print(f"  {name:15} -> {code}")


def example_name_matching():
    """姓名匹配示例"""
    print("\n" + "=" * 50)
    print("示例 2: 姓名匹配")
    print("=" * 50)
    
    encoder = SoundexEncoder()
    
    # 发音相似的姓名
    print("\n发音相似的姓名（相同编码）:")
    
    test_groups = [
        ["Smith", "Smythe", "Schmidt"],
        ["Johnson", "Johnston"],
        ["Brown", "Browne"],
        ["Mueller", "Miller", "Muller"],
    ]
    
    for group in test_groups:
        codes = set(encoder.encode(name) for name in group)
        if len(codes) == 1:
            print(f"  {' / '.join(group)} -> {list(codes)[0]}")
        else:
            print(f"  {' / '.join(group)} -> 编码不同: {codes}")


def example_similarity_search():
    """相似度搜索示例"""
    print("\n" + "=" * 50)
    print("示例 3: 相似度搜索")
    print("=" * 50)
    
    # 模拟数据库中的姓名
    database_names = [
        "Smith", "Smythe", "Schmidt", "Johnson", "Johnston", "Johnsonn",
        "Williams", "Wilson", "Brown", "Browne", "Davis", "Davies",
        "Miller", "Mueller", "Muller", "Taylor", "Anderson", "Thomas",
        "Garcia", "Martinez", "Robinson", "Clark", "Clarke", "Lewis",
    ]
    
    search_name = "Smyth"
    
    print(f"\n搜索 '{search_name}' 的相似姓名:")
    results = find_similar(search_name, database_names, threshold=0.5)
    
    for name, score in results:
        print(f"  {name:15} 相似度: {score:.2f}")


def example_grouping():
    """姓名分组示例"""
    print("\n" + "=" * 50)
    print("示例 4: 姓名分组")
    print("=" * 50)
    
    # 模拟客户列表
    customers = [
        "John Smith", "J. Smith", "Jon Smythe", "Johann Schmidt",
        "Robert Johnson", "Rob Johnson", "R. Johnston",
        "William Brown", "W. Browne", "Bill Brown",
        "Maria Garcia", "M. Garcia", "Marie Garcia",
    ]
    
    # 提取姓氏并分组
    surnames = [name.split()[-1] for name in customers]
    groups = group_by_sound(surnames)
    
    print("\n按发音分组的姓氏:")
    for code, names in sorted(groups.items()):
        if len(names) > 1:
            print(f"  {code}: {', '.join(sorted(set(names)))}")


def example_database_query():
    """数据库查询示例"""
    print("\n" + "=" * 50)
    print("示例 5: 数据库查询辅助")
    print("=" * 50)
    
    # 生成 SQL 查询
    print("\n生成 SOUNDEX 相关 SQL:")
    
    # WHERE 子句
    where = SoundexSQL.where_clause("last_name", "Smith")
    print(f"\nWHERE 子句:\n  {where}")
    
    # 创建索引
    create_index = SoundexSQL.create_index_sql("users", "last_name")
    print(f"\n创建索引:\n  {create_index}")
    
    # 完整查询示例
    print("\n完整查询示例:")
    print(f"""
  SELECT * FROM users
  WHERE {where}
  ORDER BY created_at DESC;
""")


def example_deduplication():
    """数据去重示例"""
    print("\n" + "=" * 50)
    print("示例 6: 数据去重")
    print("=" * 50)
    
    # 模拟可能重复的记录
    records = [
        {"id": 1, "name": "John Smith", "email": "john.smith@example.com"},
        {"id": 2, "name": "Jon Smythe", "email": "jon.s@example.com"},
        {"id": 3, "name": "J. Smith", "email": "jsmith@example.com"},
        {"id": 4, "name": "Robert Johnson", "email": "r.johnson@example.com"},
        {"id": 5, "name": "Rob Johnston", "email": "rob.j@example.com"},
        {"id": 6, "name": "Maria Garcia", "email": "maria.g@example.com"},
    ]
    
    encoder = SoundexEncoder()
    
    print("\n检测可能的重复记录:")
    
    # 提取姓氏
    for i, rec in enumerate(records):
        surname = rec["name"].split()[-1]
        rec["surname_code"] = encoder.encode(surname)
    
    # 按编码分组
    code_groups = {}
    for rec in records:
        code = rec["surname_code"]
        if code not in code_groups:
            code_groups[code] = []
        code_groups[code].append(rec)
    
    # 显示可能的重复
    for code, group in sorted(code_groups.items()):
        if len(group) > 1:
            print(f"\n  编码 {code} (可能的重复):")
            for rec in group:
                print(f"    - ID {rec['id']}: {rec['name']} ({rec['email']})")


def example_genealogy():
    """家谱研究示例"""
    print("\n" + "=" * 50)
    print("示例 7: 家谱研究")
    print("=" * 50)
    
    encoder = SoundexEncoder()
    
    # 模拟历史记录中的姓名变体
    historical_records = [
        "Schmidt", "Schmitt", "Schmid", "Schmitz", "Smid", "Smit",
        "Smith", "Smyth", "Smythe", "Schmidtt",
    ]
    
    print("\n历史记录中的姓名变体:")
    codes = {}
    for name in historical_records:
        code = encoder.encode(name)
        if code not in codes:
            codes[code] = []
        codes[code].append(name)
    
    for code, names in sorted(codes.items()):
        print(f"  {code}: {', '.join(names)}")
    
    print("\nSOUNDEX 对于家谱研究的价值:")
    print("  - 追踪姓氏在不同地区/时代的拼写变体")
    print("  - 索引和搜索历史记录")
    print("  - 连接可能相关的家族分支")


def example_customer_service():
    """客户服务示例"""
    print("\n" + "=" * 50)
    print("示例 8: 客户服务姓名查找")
    print("=" * 50)
    
    # 模拟客户数据库
    customers = [
        {"name": "Jennifer Williams", "account": "ACC001"},
        {"name": "Jenny Wilson", "account": "ACC002"},
        {"name": "Jen Williamson", "account": "ACC003"},
        {"name": "Michael Brown", "account": "ACC004"},
        {"name": "Mike Browne", "account": "ACC005"},
        {"name": "Michelle Brown", "account": "ACC006"},
    ]
    
    encoder = SoundexEncoder()
    
    # 客户来电，只记得大概发音
    caller_name = "Jenifer Willaims"  # 拼写可能有误
    
    print(f"\n来电者自称: {caller_name}")
    print("\n可能的匹配客户:")
    
    caller_first, caller_last = caller_name.split()
    
    for customer in customers:
        first, last = customer["name"].split()
        
        # 检查名字和姓氏的相似度
        first_sim = encoder.similarity(caller_first, first)
        last_sim = encoder.similarity(caller_last, last)
        
        # 综合相似度（可以加权）
        overall = (first_sim + last_sim) / 2
        
        if overall > 0.5:
            print(f"  {customer['name']:20} 账户: {customer['account']}  相似度: {overall:.2f}")


def example_unicode_names():
    """国际化姓名示例"""
    print("\n" + "=" * 50)
    print("示例 9: 国际化姓名处理")
    print("=" * 50)
    
    encoder = SoundexEncoder()
    
    # 各种语言的姓名
    international_names = [
        ("Müller", "德语"),
        ("François", "法语"),
        ("Sørensen", "丹麦语"),
        ("García", "西班牙语"),
        ("Björk", "瑞典语"),
        ("Kowalski", "波兰语"),
        ("O'Connor", "爱尔兰语"),
        ("Van der Berg", "荷兰语"),
    ]
    
    print("\n国际化姓名编码:")
    for name, lang in international_names:
        code = encoder.encode(name)
        print(f"  {name:15} ({lang:8}) -> {code}")


def example_refined_encoder():
    """改进编码器示例"""
    print("\n" + "=" * 50)
    print("示例 10: 改进 SOUNDEX 编码器")
    print("=" * 50)
    
    std_encoder = SoundexEncoder()
    ref_encoder = SoundexRefinedEncoder()
    
    # 比较两种编码器
    names = ["Smith", "Smythe", "Schmidt", "Johnson", "Williams"]
    
    print("\n标准 vs 改进编码器:")
    print(f"  {'姓名':12} {'标准':8} {'改进':8}")
    print("  " + "-" * 30)
    
    for name in names:
        std = std_encoder.encode(name)
        ref = ref_encoder.encode(name)
        print(f"  {name:12} {std:8} {ref:8}")


def example_custom_length():
    """自定义编码长度示例"""
    print("\n" + "=" * 50)
    print("示例 11: 自定义编码长度")
    print("=" * 50)
    
    name = "Washington"
    
    print(f"\n'{name}' 的不同长度编码:")
    
    for length in [4, 6, 8, 10]:
        encoder = SoundexEncoder(length=length)
        code = encoder.encode(name)
        print(f"  长度 {length}: {code}")


def run_all_examples():
    """运行所有示例"""
    print("=" * 60)
    print("SOUNDEX 工具模块使用示例")
    print("=" * 60)
    
    examples = [
        example_basic_usage,
        example_name_matching,
        example_similarity_search,
        example_grouping,
        example_database_query,
        example_deduplication,
        example_genealogy,
        example_customer_service,
        example_unicode_names,
        example_refined_encoder,
        example_custom_length,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n示例 {example.__name__} 出错: {e}")
    
    print("\n" + "=" * 60)
    print("所有示例演示完成")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()