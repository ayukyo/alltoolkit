"""
Porter Stemmer 工具使用示例

演示 Porter Stemmer 的各种应用场景：
1. 基本词干提取
2. 批量处理
3. 文本处理
4. 搜索索引
5. 文本相似度
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import PorterStemmer, stem, stem_words, stem_text


def example_basic_stemming():
    """基本词干提取示例"""
    print("=" * 60)
    print("基本词干提取示例")
    print("=" * 60)
    
    stemmer = PorterStemmer()
    
    # 单个单词
    words = [
        'running', 'runs', 'ran',
        'happiness', 'happy',
        'jumps', 'jumping', 'jumped',
        'cats', 'boxes', 'churches',
        'easily', 'quickly', 'slowly',
        'information', 'retrieval', 'computer',
    ]
    
    print("\n单词 -> 词干:")
    print("-" * 40)
    for word in words:
        result = stemmer.stem(word)
        print(f"  {word:20s} -> {result}")
    
    print("\n使用便捷函数:")
    print(f"  stem('running') = {stem('running')}")
    print(f"  stem('happiness') = {stem('happiness')}")


def example_batch_processing():
    """批量处理示例"""
    print("\n" + "=" * 60)
    print("批量处理示例")
    print("=" * 60)
    
    stemmer = PorterStemmer()
    
    # 批量处理单词列表
    words = [
        'running', 'swimming', 'jumping', 'eating',
        'happiness', 'sadness', 'kindness', 'darkness',
        'computer', 'programming', 'development', 'management',
    ]
    
    print("\n批量词干提取:")
    print("-" * 40)
    stems = stemmer.stem_words(words)
    for word, stem_result in zip(words, stems):
        print(f"  {word:20s} -> {stem_result}")
    
    # 使用便捷函数
    print("\n使用 stem_words() 便捷函数:")
    stems = stem_words(['cats', 'dogs', 'birds'])
    print(f"  {stems}")


def example_text_processing():
    """文本处理示例"""
    print("\n" + "=" * 60)
    print("文本处理示例")
    print("=" * 60)
    
    stemmer = PorterStemmer()
    
    text = "The cats were running and jumping happily through the houses"
    
    print(f"\n原文: {text}")
    result = stemmer.stem_text(text)
    print(f"处理后: {result}")
    
    # 更长的文本
    longer_text = """
    Information retrieval is the activity of obtaining information system 
    resources relevant to an information need from a collection of those 
    resources. The searches can be based on full-text or other content-based 
    indexing.
    """
    
    print("\n长文本处理:")
    print("-" * 40)
    print(f"原文:\n{longer_text.strip()}")
    print("-" * 40)
    result = stemmer.stem_text(longer_text)
    print(f"处理后:\n{result.strip()}")


def example_search_indexing():
    """搜索索引示例"""
    print("\n" + "=" * 60)
    print("搜索索引示例")
    print("=" * 60)
    
    stemmer = PorterStemmer()
    
    # 文档集合
    documents = {
        1: "The quick brown fox jumps over the lazy dog",
        2: "A fast dog runs faster than the fox",
        3: "Quick thinking helps solve problems quickly",
        4: "The dog was jumping and running in circles",
    }
    
    # 构建倒排索引
    index = {}
    for doc_id, text in documents.items():
        words = text.lower().split()
        stems = stemmer.stem_words(words)
        
        for stem in set(stems):
            if stem not in index:
                index[stem] = []
            index[stem].append(doc_id)
    
    print("\n文档集合:")
    for doc_id, text in documents.items():
        print(f"  [{doc_id}] {text}")
    
    print("\n倒排索引 (词干 -> 文档ID):")
    for stem in sorted(index.keys())[:10]:
        print(f"  {stem:15s} -> {index[stem]}")
    
    # 搜索示例
    print("\n搜索示例:")
    queries = ['running', 'quick', 'dog', 'jump']
    for query in queries:
        query_stem = stemmer.stem(query)
        matching_docs = index.get(query_stem, [])
        print(f"  查询 '{query}' (词干: '{query_stem}') -> 文档: {matching_docs}")


def example_text_similarity():
    """文本相似度示例"""
    print("\n" + "=" * 60)
    print("文本相似度示例")
    print("=" * 60)
    
    stemmer = PorterStemmer()
    
    def jaccard_similarity(text1: str, text2: str) -> float:
        """计算 Jaccard 相似度（基于词干）"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        stems1 = stemmer.get_unique_stems(list(words1))
        stems2 = stemmer.get_unique_stems(list(words2))
        
        intersection = stems1 & stems2
        union = stems1 | stems2
        
        return len(intersection) / len(union) if union else 0.0
    
    # 相似文本对
    text_pairs = [
        ("The cats are running fast", "A cat runs quickly"),
        ("Information retrieval systems", "Retrieving information from systems"),
        ("Programming is fun", "I enjoy cooking"),
        ("The quick brown fox", "A fast brown fox"),
    ]
    
    print("\n文本相似度 (基于词干):")
    print("-" * 40)
    for text1, text2 in text_pairs:
        similarity = jaccard_similarity(text1, text2)
        print(f"\n  文本1: \"{text1}\"")
        print(f"  文本2: \"{text2}\"")
        print(f"  相似度: {similarity:.2%}")
        
        # 显示词干
        stems1 = stemmer.get_unique_stems(text1.lower().split())
        stems2 = stemmer.get_unique_stems(text2.lower().split())
        print(f"  词干1: {sorted(stems1)}")
        print(f"  词干2: {sorted(stems2)}")


def example_word_grouping():
    """单词分组示例"""
    print("\n" + "=" * 60)
    print("单词分组示例")
    print("=" * 60)
    
    stemmer = PorterStemmer()
    
    # 相关单词列表
    words = [
        'run', 'running', 'runs', 'ran', 'runner', 'runners',
        'jump', 'jumping', 'jumps', 'jumped', 'jumper',
        'happy', 'happiness', 'happily', 'happier', 'happiest',
        'write', 'writing', 'writes', 'wrote', 'writer',
        'compute', 'computing', 'computer', 'computers', 'computation',
    ]
    
    print("\n原始单词列表:")
    print(f"  {words}")
    
    # 按词干分组
    groups = stemmer.group_by_stem(words)
    
    print("\n按词干分组:")
    print("-" * 40)
    for stem, group_words in sorted(groups.items()):
        print(f"  '{stem}': {group_words}")
    
    # 获取唯一词干
    unique_stems = stemmer.get_unique_stems(words)
    print(f"\n唯一词干数量: {len(unique_stems)}")
    print(f"唯一词干: {sorted(unique_stems)}")


def example_information_extraction():
    """信息提取示例"""
    print("\n" + "=" * 60)
    print("信息提取示例")
    print("=" * 60)
    
    stemmer = PorterStemmer()
    
    # 从文本中提取关键词词干
    def extract_keywords(text: str, stop_stems: set) -> list:
        """提取关键词（排除停用词）"""
        words = text.lower().split()
        stems_with_words = [(stemmer.stem(w), w) for w in words]
        
        # 过滤停用词
        keywords = [(s, w) for s, w in stems_with_words 
                    if s not in stop_stems and len(s) > 2]
        
        return keywords
    
    # 停用词词干
    stop_stems = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 
                  'been', 'be', 'have', 'has', 'had', 'do', 'does', 
                  'did', 'will', 'would', 'could', 'should', 'may', 
                  'might', 'must', 'shall', 'can', 'need', 'dare', 
                  'ought', 'us', 'we', 'our', 'you', 'your', 'he', 
                  'she', 'it', 'they', 'them', 'their', 'this', 'that',
                  'these', 'those', 'and', 'or', 'but', 'if', 'then',
                  'else', 'when', 'up', 'down', 'in', 'out', 'on', 'off',
                  'over', 'under', 'again', 'further', 'then', 'onc'}
    
    text = """
    Natural language processing is a subfield of linguistics, computer 
    science, and artificial intelligence concerned with the interactions 
    between computers and human language. It focuses on how to program 
    computers to process and analyze large amounts of natural language data.
    """
    
    print(f"\n原文:\n{text.strip()}")
    print("\n关键词提取:")
    print("-" * 40)
    
    keywords = extract_keywords(text, stop_stems)
    for stem, word in keywords[:15]:
        print(f"  {word:20s} -> {stem}")


def example_comparison_table():
    """词干对比表示例"""
    print("\n" + "=" * 60)
    print("词干对比表")
    print("=" * 60)
    
    stemmer = PorterStemmer()
    
    # 常见词形变化
    word_groups = [
        ['connect', 'connected', 'connecting', 'connection', 'connections'],
        ['relate', 'related', 'relating', 'relation', 'relations', 'relational'],
        ['compute', 'computed', 'computing', 'computer', 'computers', 'computation'],
        ['organize', 'organized', 'organizing', 'organization', 'organizations'],
        ['analyze', 'analyzed', 'analyzing', 'analysis', 'analyses', 'analytical'],
    ]
    
    print("\n词形变化对比:")
    print("-" * 60)
    
    for group in word_groups:
        stems = [stemmer.stem(w) for w in group]
        print(f"\n  原词: {group}")
        print(f"  词干: {stems}")
        print(f"  唯一: {list(set(stems))}")


def main():
    """运行所有示例"""
    example_basic_stemming()
    example_batch_processing()
    example_text_processing()
    example_search_indexing()
    example_text_similarity()
    example_word_grouping()
    example_information_extraction()
    example_comparison_table()
    
    print("\n" + "=" * 60)
    print("示例完成")
    print("=" * 60)


if __name__ == '__main__':
    main()