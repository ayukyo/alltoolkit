"""
Metaphone Utils 使用示例

演示如何使用 Metaphone 和 Double Metaphone 编码进行语音匹配。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metaphone_utils.mod import (
    Metaphone,
    DoubleMetaphone,
    PhoneticMatcher,
    metaphone,
    double_metaphone,
    sounds_like,
    phonetic_similarity,
    COMMON_NAMES,
)


def example_basic_encoding():
    """基本编码示例"""
    print("\n" + "="*50)
    print("基本编码示例")
    print("="*50)
    
    # 使用便捷函数
    print("\n1. Metaphone 编码:")
    words = ['Smith', 'Smyth', 'Schmidt', 'phone', 'fone', 'knight', 'night']
    for word in words:
        code = metaphone(word)
        print(f"   {word:15} -> {code}")
    
    print("\n2. Double Metaphone 编码 (主编码, 替代编码):")
    for word in words:
        primary, alternate = double_metaphone(word)
        print(f"   {word:15} -> ({primary}, {alternate})")


def example_phonetic_matching():
    """语音匹配示例"""
    print("\n" + "="*50)
    print("语音匹配示例")
    print("="*50)
    
    # 创建匹配器
    matcher = PhoneticMatcher()
    
    print("\n1. 判断两个词是否发音相似:")
    pairs = [
        ('Smith', 'Smyth'),
        ('Smith', 'Schmidt'),
        ('phone', 'fone'),
        ('knight', 'night'),
        ('write', 'right'),
        ('through', 'threw'),
        ('apple', 'orange'),
        ('cat', 'dog'),
    ]
    
    for w1, w2 in pairs:
        like = sounds_like(w1, w2)
        sim = phonetic_similarity(w1, w2)
        status = "✓ 相似" if like else "✗ 不同"
        print(f"   {w1:12} vs {w2:12} -> {status} (相似度: {sim:.2f})")


def example_spell_checking():
    """拼写检查示例"""
    print("\n" + "="*50)
    print("拼写检查示例")
    print("="*50)
    
    matcher = PhoneticMatcher()
    
    # 常见英语单词字典
    dictionary = [
        'their', 'there', "they're", 'write', 'right', 'night', 'knight',
        'phone', 'home', 'house', 'mouse', 'green', 'screen', 'scene',
        'blue', 'blew', 'through', 'threw', 'knew', 'new', 'knight',
        'weight', 'wait', 'eight', 'ate', 'flower', 'flour',
    ]
    
    print("\n拼写建议 (输入可能的拼写错误):")
    misspellings = ['thier', 'rite', 'nite', 'fone', 'grren', 'blu']
    
    for word in misspellings:
        suggestions = matcher.suggest(word, dictionary, max_suggestions=3)
        print(f"   '{word}' -> {suggestions}")


def example_name_matching():
    """姓名匹配示例"""
    print("\n" + "="*50)
    print("姓名匹配示例")
    print("="*50)
    
    matcher = PhoneticMatcher()
    
    # 姓名变体数据库
    name_groups = [
        ['Smith', 'Smyth', 'Schmidt', 'Schmitt', 'Smythe'],
        ['Johnson', 'Johnston', 'Johnstone', 'Jonson'],
        ['Williams', 'Williamson', 'Willioms'],
        ['Brown', 'Browne', 'Braun'],
        ['Davis', 'Davies', 'David'],
        ['Catherine', 'Katherine', 'Kathryn', 'Cathryn'],
    ]
    
    print("\n同一姓氏的不同拼写变体:")
    for group in name_groups:
        print(f"\n   组: {group}")
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                sim = matcher.similarity(group[i], group[j])
                if sim >= 0.6:
                    print(f"      {group[i]} <-> {group[j]}: {sim:.2f}")


def example_duplicate_detection():
    """重复检测示例"""
    print("\n" + "="*50)
    print("重复记录检测示例")
    print("="*50)
    
    matcher = PhoneticMatcher()
    
    # 模拟客户数据库
    customers = [
        'John Smith', 'Jon Smith', 'John Smyth', 'Johnny Smith',
        'William Johnson', 'Bill Johnson', 'Will Johnson', 'Billy Johnson',
        'Robert Williams', 'Rob Williams', 'Bob Williams', 'Robbie Williams',
        'James Brown', 'Jim Brown', 'Jimmy Brown',
        'Michael Davis', 'Mike Davis', 'Mick Davis',
        'David Wilson', 'Dave Wilson', 'Davey Wilson',
        'Richard Taylor', 'Rick Taylor', 'Dick Taylor', 'Ricky Taylor',
    ]
    
    print("\n检测可能的重复记录:")
    
    # 按姓氏分组
    by_lastname = {}
    for name in customers:
        parts = name.split()
        if len(parts) >= 2:
            lastname = parts[-1]
            if lastname not in by_lastname:
                by_lastname[lastname] = []
            by_lastname[lastname].append(name)
    
    # 在每个姓氏组内检测重复
    for lastname, names in by_lastname.items():
        if len(names) > 1:
            print(f"\n   姓氏 '{lastname}':")
            for i in range(len(names)):
                for j in range(i + 1, len(names)):
                    sim = matcher.similarity(names[i], names[j])
                    if sim >= 0.7:
                        print(f"      可能重复: '{names[i]}' <-> '{names[j]}' (相似度: {sim:.2f})")


def example_search_index():
    """搜索索引示例"""
    print("\n" + "="*50)
    print("语音搜索索引示例")
    print("="*50)
    
    matcher = PhoneticMatcher()
    
    # 产品目录
    products = [
        'iPhone', 'iFone', 'Samsung', 'Sammsung', 'Galaxy',
        'MacBook', 'Macbook', 'Mac Book', 'ThinkPad', 'Thinkpad',
        'PlayStation', 'Playstation', 'Xbox', 'X-Box', 'Nintendo',
        'Kindle', 'Kindle Fire', 'iPad', 'i-Pad', 'iPod', 'i-Pod',
    ]
    
    print("\n构建语音索引:")
    index = matcher.build_index(products)
    
    print("\n索引内容 (编码 -> 产品列表):")
    for code, items in sorted(index.items()):
        if len(items) > 1:
            print(f"   {code}: {items}")
    
    print("\n模糊搜索演示:")
    queries = ['ifone', 'samsung', 'mackbook', 'x-box', 'ipad']
    for query in queries:
        similar = matcher.find_similar(query, products, threshold=0.7)
        print(f"   搜索 '{query}':")
        for product, score in similar[:3]:
            print(f"      -> {product} (相似度: {score:.2f})")


def example_fuzzy_dedup():
    """模糊去重示例"""
    print("\n" + "="*50)
    print("模糊去重示例")
    print("="*50)
    
    matcher = PhoneticMatcher()
    
    # 带有可能重复的单词列表
    words = [
        'their', 'there', "they're", 'apple', 'appel', 'aple',
        'banana', 'bannana', 'bannana', 'orange', 'orrange',
        'computer', 'computter', 'compter', 'keyboard', 'keybord',
        'mouse', 'mousse', 'screen', 'scren', 'phone', 'fone',
    ]
    
    print("\n原始列表长度:", len(words))
    
    # 使用语音编码去重
    seen_codes = {}
    unique_words = []
    
    for word in words:
        primary, alternate = double_metaphone(word)
        
        # 检查是否已有相似编码
        found = False
        for code in [primary, alternate]:
            if code and code in seen_codes:
                found = True
                break
        
        if not found:
            unique_words.append(word)
            if primary:
                seen_codes[primary] = word
            if alternate and alternate != primary:
                seen_codes[alternate] = word
    
    print("去重后列表长度:", len(unique_words))
    print("去重后单词:", unique_words)
    
    # 显示被合并的相似词
    print("\n相似词组合:")
    code_groups = {}
    for word in words:
        code = metaphone(word)
        if code not in code_groups:
            code_groups[code] = []
        if word not in code_groups[code]:
            code_groups[code].append(word)
    
    for code, group in sorted(code_groups.items()):
        if len(group) > 1:
            print(f"   {code}: {group}")


def example_phonetic_search_engine():
    """语音搜索引擎示例"""
    print("\n" + "="*50)
    print("简单语音搜索引擎示例")
    print("="*50)
    
    class PhoneticSearchEngine:
        """简单的语音搜索引擎"""
        
        def __init__(self):
            self.matcher = PhoneticMatcher()
            self.documents = []
            self.word_index = {}
        
        def index(self, documents):
            """索引文档"""
            self.documents = documents
            all_words = set()
            
            for doc_id, text in documents:
                words = text.lower().split()
                for word in words:
                    # 清理标点
                    word = ''.join(c for c in word if c.isalnum())
                    if word:
                        all_words.add(word)
                        
            self.word_index = self.matcher.build_index(list(all_words))
        
        def search(self, query, threshold=0.8):
            """搜索"""
            query_words = query.lower().split()
            results = []
            
            for doc_id, text in self.documents:
                doc_words = set(
                    ''.join(c for c in w if c.isalnum())
                    for w in text.lower().split()
                )
                
                score = 0
                for q_word in query_words:
                    q_word = ''.join(c for c in q_word if c.isalnum())
                    if not q_word:
                        continue
                    
                    for doc_word in doc_words:
                        if self.matcher.sounds_like(q_word, doc_word):
                            sim = self.matcher.similarity(q_word, doc_word)
                            score += sim
                
                if score > 0:
                    results.append((doc_id, score))
            
            results.sort(key=lambda x: -x[1])
            return results
    
    # 创建搜索引擎
    engine = PhoneticSearchEngine()
    
    # 索引文档
    documents = [
        (1, "The quick brown fox jumps over the lazy dog"),
        (2, "A quick brown dog ran through the park"),
        (3, "The lazy cat slept all day long"),
        (4, "Quick thinking saved the day"),
        (5, "The brown bear hibernates in winter"),
    ]
    
    engine.index(documents)
    
    print("\n索引的文档:")
    for doc_id, text in documents:
        print(f"   [{doc_id}] {text}")
    
    print("\n搜索演示:")
    queries = ['quik', 'broun', 'layzi', 'thinc']
    
    for query in queries:
        print(f"\n   搜索: '{query}'")
        results = engine.search(query)
        for doc_id, score in results[:3]:
            print(f"      [{doc_id}] (score: {score:.2f}) {documents[doc_id-1][1][:50]}...")


def example_custom_encoder():
    """自定义编码器示例"""
    print("\n" + "="*50)
    print("自定义编码器配置示例")
    print("="*50)
    
    # 使用不同的最大长度
    print("\n1. 不同最大长度的编码:")
    for max_len in [2, 4, 6, 8]:
        encoder = Metaphone(max_length=max_len)
        code = encoder.encode('internationalization')
        print(f"   长度 {max_len}: '{code}'")
    
    # 使用单一 Metaphone vs Double Metaphone
    print("\n2. 单一 Metaphone vs Double Metaphone:")
    
    single = PhoneticMatcher(use_double=False)
    double = PhoneticMatcher(use_double=True)
    
    test_pairs = [
        ('Smith', 'Schmidt'),
        ('Johnson', 'Johnston'),
        ('Catherine', 'Katherine'),
    ]
    
    for w1, w2 in test_pairs:
        sim_single = single.similarity(w1, w2)
        sim_double = double.similarity(w1, w2)
        print(f"   {w1} vs {w2}:")
        print(f"      单一 Metaphone: {sim_single:.2f}")
        print(f"      Double Metaphone: {sim_double:.2f}")


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("Metaphone Utils - 语音编码工具示例")
    print("="*60)
    
    example_basic_encoding()
    example_phonetic_matching()
    example_spell_checking()
    example_name_matching()
    example_duplicate_detection()
    example_search_index()
    example_fuzzy_dedup()
    example_phonetic_search_engine()
    example_custom_encoder()
    
    print("\n" + "="*60)
    print("示例演示完成！")
    print("="*60)


if __name__ == '__main__':
    main()