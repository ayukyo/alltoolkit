"""
Kaomoji Utils 测试文件

测试日式颜文字工具集的各项功能。
"""

import pytest
from mod import (
    get_all_emotions,
    get_by_emotion,
    get_random,
    search,
    get_details,
    get_random_entry,
    count,
    count_total,
    happy, sad, love, angry, surprised, cute, shy, cat, bear, flower,
    HAPPY, SAD, LOVE, ANGRY, SURPRISED, CUTE, SHY, WINK, TABLE_FLIP, CAT, BEAR, FLOWER, FIGHT, MAGIC, RUN,
    KAOMOJI_DATABASE,
    KaomojiEntry,
)


class TestBasicFunctions:
    """测试基本功能"""
    
    def test_get_all_emotions(self):
        """测试获取所有情绪类别"""
        emotions = get_all_emotions()
        assert isinstance(emotions, list)
        assert len(emotions) > 0
        # 检查是否包含常见情绪
        assert "happy" in emotions
        assert "sad" in emotions
        assert "love" in emotions
        assert "angry" in emotions
    
    def test_get_by_emotion(self):
        """测试按情绪获取颜文字"""
        # 测试有效情绪
        happy_kaomoji = get_by_emotion("happy")
        assert isinstance(happy_kaomoji, list)
        assert len(happy_kaomoji) > 0
        assert all(isinstance(k, str) for k in happy_kaomoji)
        
        # 测试大小写不敏感
        happy_upper = get_by_emotion("HAPPY")
        assert happy_upper == happy_kaomoji
        
        # 测试无效情绪
        with pytest.raises(ValueError):
            get_by_emotion("invalid_emotion")
    
    def test_get_random(self):
        """测试随机获取颜文字"""
        # 测试不带情绪参数
        kaomoji = get_random()
        assert isinstance(kaomoji, str)
        assert len(kaomoji) > 0
        
        # 测试带情绪参数
        kaomoji = get_random("happy")
        assert isinstance(kaomoji, str)
        assert kaomoji in get_by_emotion("happy")
        
        # 测试无效情绪
        with pytest.raises(ValueError):
            get_random("invalid_emotion")
    
    def test_count(self):
        """测试统计功能"""
        counts = count()
        assert isinstance(counts, dict)
        assert len(counts) > 0
        # 检查每个类别都有数量
        for emotion, cnt in counts.items():
            assert isinstance(cnt, int)
            assert cnt > 0
    
    def test_count_total(self):
        """测试总数统计"""
        total = count_total()
        assert isinstance(total, int)
        assert total > 0
        # 验证总数等于各分类数量之和
        assert total == sum(count().values())


class TestSearch:
    """测试搜索功能"""
    
    def test_search_by_keyword(self):
        """测试按关键词搜索"""
        # 搜索 happy
        results = search("happy")
        assert isinstance(results, list)
        assert len(results) > 0
        
        # 搜索 love
        results = search("love")
        assert isinstance(results, list)
        assert len(results) > 0
        
        # 搜索 cat
        results = search("cat")
        assert isinstance(results, list)
        assert len(results) > 0
    
    def test_search_case_insensitive(self):
        """测试搜索大小写不敏感"""
        results_lower = search("happy")
        results_upper = search("HAPPY")
        results_mixed = search("Happy")
        
        # 所有搜索结果应该相同
        assert results_lower == results_upper == results_mixed
    
    def test_search_in_description(self):
        """测试在描述中搜索"""
        # 搜索中文描述
        results = search("猫")
        assert isinstance(results, list)
        # 应该找到猫咪相关的颜文字
        
        results = search("开心")
        assert isinstance(results, list)
    
    def test_search_in_kaomoji(self):
        """测试在颜文字中搜索"""
        # 搜索颜文字中的特殊字符
        results = search("♥")
        assert isinstance(results, list)
        
        results = search("♡")
        assert isinstance(results, list)
    
    def test_search_no_results(self):
        """测试无结果的搜索"""
        results = search("xyznonexistent123")
        assert isinstance(results, list)
        assert len(results) == 0
    
    def test_search_deduplication(self):
        """测试搜索结果去重"""
        results = search("happy")
        # 确保没有重复
        assert len(results) == len(set(results))


class TestDetails:
    """测试详情功能"""
    
    def test_get_details(self):
        """测试获取颜文字详情"""
        # 测试已知颜文字
        details = get_details(HAPPY)
        assert details is not None
        assert isinstance(details, KaomojiEntry)
        assert details.kaomoji == HAPPY
        assert details.emotion == "happy"
        assert isinstance(details.keywords, list)
        assert len(details.keywords) > 0
        assert isinstance(details.description, str)
    
    def test_get_details_not_found(self):
        """测试获取不存在的颜文字详情"""
        details = get_details("不存在")
        assert details is None
    
    def test_get_random_entry(self):
        """测试获取随机条目"""
        entry = get_random_entry()
        assert isinstance(entry, KaomojiEntry)
        assert isinstance(entry.kaomoji, str)
        assert isinstance(entry.emotion, str)
        assert isinstance(entry.keywords, list)
        assert isinstance(entry.description, str)
        
        # 测试带情绪参数
        entry = get_random_entry("happy")
        assert entry.emotion == "happy"
        
        # 测试无效情绪
        with pytest.raises(ValueError):
            get_random_entry("invalid_emotion")


class TestConvenienceFunctions:
    """测试便捷函数"""
    
    def test_emotion_functions(self):
        """测试情绪快捷函数"""
        assert isinstance(happy(), str)
        assert isinstance(sad(), str)
        assert isinstance(love(), str)
        assert isinstance(angry(), str)
        assert isinstance(surprised(), str)
        assert isinstance(cute(), str)
        assert isinstance(shy(), str)
        assert isinstance(cat(), str)
        assert isinstance(bear(), str)
        assert isinstance(flower(), str)
    
    def test_emotion_functions_return_valid_kaomoji(self):
        """测试快捷函数返回的颜文字在正确类别中"""
        happy_list = get_by_emotion("happy")
        assert happy() in happy_list
        
        sad_list = get_by_emotion("sad")
        assert sad() in sad_list
        
        love_list = get_by_emotion("love")
        assert love() in love_list
        
        cat_list = get_by_emotion("cat")
        assert cat() in cat_list


class TestConstants:
    """测试常量"""
    
    def test_predefined_constants(self):
        """测试预定义常量"""
        assert isinstance(HAPPY, str)
        assert isinstance(SAD, str)
        assert isinstance(LOVE, str)
        assert isinstance(ANGRY, str)
        assert isinstance(SURPRISED, str)
        assert isinstance(CUTE, str)
        assert isinstance(SHY, str)
        assert isinstance(WINK, str)
        assert isinstance(TABLE_FLIP, str)
        assert isinstance(CAT, str)
        assert isinstance(BEAR, str)
        assert isinstance(FLOWER, str)
        assert isinstance(FIGHT, str)
        assert isinstance(MAGIC, str)
        assert isinstance(RUN, str)
    
    def test_constants_in_correct_category(self):
        """测试常量在正确的类别中"""
        assert HAPPY in get_by_emotion("happy")
        assert SAD in get_by_emotion("sad")
        assert LOVE in get_by_emotion("love")
        assert ANGRY in get_by_emotion("angry")
        assert SURPRISED in get_by_emotion("surprised")
        assert CUTE in get_by_emotion("cute")
        assert SHY in get_by_emotion("shy")
        assert WINK in get_by_emotion("wink")
        assert TABLE_FLIP in get_by_emotion("table_flip")
        assert CAT in get_by_emotion("cat")
        assert BEAR in get_by_emotion("bear")
        assert FLOWER in get_by_emotion("flower")
        assert FIGHT in get_by_emotion("fight")
        assert MAGIC in get_by_emotion("magic")
        assert RUN in get_by_emotion("run")


class TestDataIntegrity:
    """测试数据完整性"""
    
    def test_database_not_empty(self):
        """测试数据库不为空"""
        assert len(KAOMOJI_DATABASE) > 0
    
    def test_all_entries_valid(self):
        """测试所有条目有效"""
        for emotion, entries in KAOMOJI_DATABASE.items():
            assert isinstance(emotion, str)
            assert len(emotion) > 0
            assert isinstance(entries, list)
            assert len(entries) > 0
            
            for entry in entries:
                assert isinstance(entry, KaomojiEntry)
                assert isinstance(entry.kaomoji, str)
                assert len(entry.kaomoji) > 0
                assert isinstance(entry.emotion, str)
                assert entry.emotion == emotion
                assert isinstance(entry.keywords, list)
                assert len(entry.keywords) > 0
                assert isinstance(entry.description, str)
    
    def test_all_emotions_have_entries(self):
        """测试所有情绪都有条目"""
        emotions = get_all_emotions()
        for emotion in emotions:
            entries = get_by_emotion(emotion)
            assert len(entries) > 0, f"情绪 '{emotion}' 没有条目"
    
    def test_no_duplicate_kaomoji_in_category(self):
        """测试类别内没有重复颜文字"""
        for emotion, entries in KAOMOJI_DATABASE.items():
            kaomoji_list = [e.kaomoji for e in entries]
            assert len(kaomoji_list) == len(set(kaomoji_list)), \
                f"情绪 '{emotion}' 中存在重复颜文字"


class TestEdgeCases:
    """测试边缘情况"""
    
    def test_multiple_random_calls(self):
        """测试多次随机调用"""
        # 多次调用应该不会出错
        for _ in range(100):
            kaomoji = get_random()
            assert isinstance(kaomoji, str)
            assert len(kaomoji) > 0
    
    def test_empty_keyword_search(self):
        """测试空关键词搜索"""
        results = search("")
        # 空关键词应该返回空列表或者所有结果
        # 根据实现可能不同
    
    def test_special_characters_in_kaomoji(self):
        """测试颜文字中的特殊字符"""
        # 确保所有颜文字都能正常处理
        for emotion, entries in KAOMOJI_DATABASE.items():
            for entry in entries:
                # 确保颜文字可以正常打印
                _ = str(entry.kaomoji)
                # 确保颜文字可以正常编码
                _ = entry.kaomoji.encode('utf-8')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])