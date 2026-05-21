"""
Verb Conjugation Utils Tests
"""

import unittest
from mod import (
    Language, Tense, Person, Mood,
    get_verb_info, conjugate, conjugate_all_forms,
    is_irregular_verb, list_irregular_verbs,
    get_participle_forms, get_past_forms,
    generate_verb_table, detect_verb_type,
    create_sentence, suggest_spelling, compare_verbs,
    conjugate_english_present_simple,
    conjugate_english_past_simple,
    conjugate_english_present_perfect,
)


class TestVerbInfo(unittest.TestCase):
    """测试动词信息获取"""
    
    def test_irregular_verb_info(self):
        """测试不规则动词信息"""
        info = get_verb_info("go")
        self.assertEqual(info.infinitive, "go")
        self.assertEqual(info.past_simple, "went")
        self.assertEqual(info.past_participle, "gone")
        self.assertTrue(info.is_irregular)
    
    def test_regular_verb_info(self):
        """测试规则动词信息"""
        info = get_verb_info("work")
        self.assertEqual(info.infinitive, "work")
        self.assertEqual(info.past_simple, "worked")
        self.assertEqual(info.past_participle, "worked")
        self.assertTrue(info.is_regular)
    
    def test_verb_ends_with_e(self):
        """测试以 e 结尾的动词"""
        info = get_verb_info("create")
        self.assertEqual(info.past_simple, "created")
        self.assertEqual(info.past_participle, "created")
        self.assertEqual(info.present_participle, "creating")
    
    def test_verb_ends_with_y_consonant(self):
        """测试以 y 结尾（前面是辅音）的动词"""
        info = get_verb_info("try")
        self.assertEqual(info.past_simple, "tried")
        self.assertEqual(info.past_participle, "tried")
        self.assertEqual(info.third_person_singular, "tries")
    
    def test_verb_ends_with_ss(self):
        """测试以 ss 结尾的动词"""
        info = get_verb_info("pass")
        self.assertEqual(info.third_person_singular, "passes")
    
    def test_verb_cvc_pattern(self):
        """测试 CVC 结构的动词"""
        info = get_verb_info("stop")
        self.assertEqual(info.past_simple, "stopped")
        self.assertEqual(info.present_participle, "stopping")


class TestConjugation(unittest.TestCase):
    """测试动词变位"""
    
    def test_present_simple_third_singular(self):
        """测试现在简单时第三人称单数"""
        result = conjugate("walk", Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR)
        self.assertEqual(result.conjugated, "walks")
        
        result = conjugate("go", Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR)
        self.assertEqual(result.conjugated, "goes")
        
        result = conjugate("try", Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR)
        self.assertEqual(result.conjugated, "tries")
    
    def test_present_simple_other_persons(self):
        """测试现在简单时其他人称"""
        result = conjugate("walk", Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR)
        self.assertEqual(result.conjugated, "walk")
        
        result = conjugate("walk", Tense.PRESENT_SIMPLE, Person.FIRST_PLURAL)
        self.assertEqual(result.conjugated, "walk")
        
        result = conjugate("walk", Tense.PRESENT_SIMPLE, Person.THIRD_PLURAL)
        self.assertEqual(result.conjugated, "walk")
    
    def test_present_continuous(self):
        """测试现在进行时"""
        result = conjugate("walk", Tense.PRESENT_CONTINUOUS, Person.FIRST_SINGULAR)
        self.assertEqual(result.conjugated, "am walking")
        
        result = conjugate("walk", Tense.PRESENT_CONTINUOUS, Person.THIRD_SINGULAR)
        self.assertEqual(result.conjugated, "is walking")
        
        result = conjugate("walk", Tense.PRESENT_CONTINUOUS, Person.THIRD_PLURAL)
        self.assertEqual(result.conjugated, "are walking")
    
    def test_past_simple(self):
        """测试过去简单时"""
        result = conjugate("walk", Tense.PAST_SIMPLE, Person.FIRST_SINGULAR)
        self.assertEqual(result.conjugated, "walked")
        
        result = conjugate("go", Tense.PAST_SIMPLE, Person.FIRST_SINGULAR)
        self.assertEqual(result.conjugated, "went")
        
        result = conjugate("be", Tense.PAST_SIMPLE, Person.FIRST_SINGULAR)
        self.assertEqual(result.conjugated, "was")
        
        result = conjugate("be", Tense.PAST_SIMPLE, Person.THIRD_PLURAL)
        self.assertEqual(result.conjugated, "were")
    
    def test_past_continuous(self):
        """测试过去进行时"""
        result = conjugate("walk", Tense.PAST_CONTINUOUS, Person.FIRST_SINGULAR)
        self.assertEqual(result.conjugated, "was walking")
        
        result = conjugate("walk", Tense.PAST_CONTINUOUS, Person.THIRD_PLURAL)
        self.assertEqual(result.conjugated, "were walking")
    
    def test_future_simple(self):
        """测试将来简单时"""
        result = conjugate("walk", Tense.FUTURE_SIMPLE, Person.FIRST_SINGULAR)
        self.assertEqual(result.conjugated, "will walk")
    
    def test_future_continuous(self):
        """测试将来进行时"""
        result = conjugate("walk", Tense.FUTURE_CONTINUOUS, Person.FIRST_SINGULAR)
        self.assertEqual(result.conjugated, "will be walking")
    
    def test_present_perfect(self):
        """测试现在完成时"""
        result = conjugate("walk", Tense.PRESENT_PERFECT, Person.FIRST_SINGULAR)
        self.assertEqual(result.conjugated, "have walked")
        
        result = conjugate("walk", Tense.PRESENT_PERFECT, Person.THIRD_SINGULAR)
        self.assertEqual(result.conjugated, "has walked")
        
        result = conjugate("go", Tense.PRESENT_PERFECT, Person.FIRST_SINGULAR)
        self.assertEqual(result.conjugated, "have gone")
    
    def test_past_perfect(self):
        """测试过去完成时"""
        result = conjugate("walk", Tense.PAST_PERFECT, Person.FIRST_SINGULAR)
        self.assertEqual(result.conjugated, "had walked")
    
    def test_future_perfect(self):
        """测试将来完成时"""
        result = conjugate("walk", Tense.FUTURE_PERFECT, Person.FIRST_SINGULAR)
        self.assertEqual(result.conjugated, "will have walked")
    
    def test_conditional(self):
        """测试条件句"""
        result = conjugate("walk", Tense.CONDITIONAL, Person.FIRST_SINGULAR)
        self.assertEqual(result.conjugated, "would walk")
    
    def test_conditional_perfect(self):
        """测试条件完成时"""
        result = conjugate("walk", Tense.CONDITIONAL_PERFECT, Person.FIRST_SINGULAR)
        self.assertEqual(result.conjugated, "would have walked")
    
    def test_imperative(self):
        """测试祈使句"""
        result = conjugate("walk", Tense.IMPERATIVE)
        self.assertEqual(result.conjugated, "walk")
    
    def test_gerund(self):
        """测试动名词"""
        result = conjugate("walk", Tense.GERUND)
        self.assertEqual(result.conjugated, "walking")
    
    def test_participle(self):
        """测试分词"""
        result = conjugate("walk", Tense.PARTICIPLE)
        self.assertEqual(result.conjugated, "walked")
        
        result = conjugate("go", Tense.PARTICIPLE)
        self.assertEqual(result.conjugated, "gone")


class TestNegativeForms(unittest.TestCase):
    """测试否定形式"""
    
    def test_present_simple_negative(self):
        """测试现在简单时否定"""
        result = conjugate("walk", Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR, negative=True)
        self.assertEqual(result.negative, "do not walk")
        
        result = conjugate("walk", Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR, negative=True)
        self.assertEqual(result.negative, "does not walk")
    
    def test_past_simple_negative(self):
        """测试过去简单时否定"""
        result = conjugate("walk", Tense.PAST_SIMPLE, Person.FIRST_SINGULAR, negative=True)
        self.assertEqual(result.negative, "did not walk")
        
        result = conjugate("go", Tense.PAST_SIMPLE, Person.FIRST_SINGULAR, negative=True)
        self.assertEqual(result.negative, "did not go")
    
    def test_present_continuous_negative(self):
        """测试现在进行时否定"""
        result = conjugate("walk", Tense.PRESENT_CONTINUOUS, Person.FIRST_SINGULAR, negative=True)
        self.assertEqual(result.negative, "am not walking")
    
    def test_present_perfect_negative(self):
        """测试现在完成时否定"""
        result = conjugate("walk", Tense.PRESENT_PERFECT, Person.FIRST_SINGULAR, negative=True)
        self.assertEqual(result.negative, "have not walked")
    
    def test_future_negative(self):
        """测试将来时否定"""
        result = conjugate("walk", Tense.FUTURE_SIMPLE, Person.FIRST_SINGULAR, negative=True)
        self.assertEqual(result.negative, "will not walk")


class TestInterrogativeForms(unittest.TestCase):
    """测试疑问形式"""
    
    def test_present_simple_interrogative(self):
        """测试现在简单时疑问"""
        result = conjugate("walk", Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR, interrogative=True)
        self.assertEqual(result.interrogative, "Do I walk")
        
        result = conjugate("walk", Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR, interrogative=True)
        self.assertEqual(result.interrogative, "Does he/she/it walk")
    
    def test_past_simple_interrogative(self):
        """测试过去简单时疑问"""
        result = conjugate("walk", Tense.PAST_SIMPLE, Person.FIRST_SINGULAR, interrogative=True)
        self.assertEqual(result.interrogative, "Did I walk")
    
    def test_present_continuous_interrogative(self):
        """测试现在进行时疑问"""
        result = conjugate("walk", Tense.PRESENT_CONTINUOUS, Person.FIRST_SINGULAR, interrogative=True)
        self.assertEqual(result.interrogative, "am I walking")
    
    def test_present_perfect_interrogative(self):
        """测试现在完成时疑问"""
        result = conjugate("walk", Tense.PRESENT_PERFECT, Person.FIRST_SINGULAR, interrogative=True)
        self.assertEqual(result.interrogative, "have I walked")


class TestUtilityFunctions(unittest.TestCase):
    """测试辅助函数"""
    
    def test_is_irregular_verb(self):
        """测试不规则动词检测"""
        self.assertTrue(is_irregular_verb("go"))
        self.assertTrue(is_irregular_verb("be"))
        self.assertFalse(is_irregular_verb("walk"))
        self.assertFalse(is_irregular_verb("work"))
    
    def test_list_irregular_verbs(self):
        """测试不规则动词列表"""
        verbs = list_irregular_verbs()
        self.assertGreater(len(verbs), 50)
        verb_infinitives = [v.infinitive for v in verbs]
        self.assertIn("be", verb_infinitives)
        self.assertIn("go", verb_infinitives)
        self.assertIn("have", verb_infinitives)
    
    def test_get_participle_forms(self):
        """测试获取分词形式"""
        present, past = get_participle_forms("walk")
        self.assertEqual(present, "walking")
        self.assertEqual(past, "walked")
        
        present, past = get_participle_forms("go")
        self.assertEqual(present, "going")
        self.assertEqual(past, "gone")
    
    def test_get_past_forms(self):
        """测试获取过去形式"""
        past_simple, past_participle = get_past_forms("go")
        self.assertEqual(past_simple, "went")
        self.assertEqual(past_participle, "gone")
    
    def test_conjugate_all_forms(self):
        """测试获取所有形式"""
        forms = conjugate_all_forms("walk")
        self.assertIn("present_simple", forms)
        self.assertIn("past_simple", forms)
        self.assertIn("present_perfect", forms)
        self.assertIn("infinitive", forms)
        self.assertIn("gerund", forms)
    
    def test_detect_verb_type(self):
        """测试动词类型检测"""
        type_info = detect_verb_type("work")
        self.assertFalse(type_info["is_auxiliary"])
        self.assertTrue(type_info["is_regular"])
        
        type_info = detect_verb_type("be")
        self.assertTrue(type_info["is_auxiliary"])
        self.assertTrue(type_info["is_irregular"])


class TestSentenceCreation(unittest.TestCase):
    """测试句子创建"""
    
    def test_create_simple_sentence(self):
        """测试创建简单句"""
        sentence = create_sentence("write", Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR)
        self.assertEqual(sentence, "I write")
        
        sentence = create_sentence("write", Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR)
        self.assertEqual(sentence, "he/she/it writes")
    
    def test_create_sentence_with_subject(self):
        """测试带主语的句子"""
        sentence = create_sentence("write", Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR, subject="John")
        self.assertEqual(sentence, "John write")
    
    def test_create_sentence_with_object(self):
        """测试带宾语的句子"""
        sentence = create_sentence("write", Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR, object="a letter")
        self.assertEqual(sentence, "I write a letter")
    
    def test_create_negative_sentence(self):
        """测试否定句"""
        sentence = create_sentence("write", Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR, negative=True)
        self.assertEqual(sentence, "I do not write")
    
    def test_create_interrogative_sentence(self):
        """测试疑问句"""
        sentence = create_sentence("write", Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR, interrogative=True)
        self.assertEqual(sentence, "Do I write?")


class TestSpellingSuggestions(unittest.TestCase):
    """测试拼写建议"""
    
    def test_exact_match(self):
        """测试完全匹配"""
        suggestions = suggest_spelling("go")
        self.assertIn("go", suggestions)
    
    def test_near_match(self):
        """测试近似匹配"""
        suggestions = suggest_spelling("ga")
        self.assertIn("go", suggestions)
    
    def test_no_match(self):
        """测试无匹配"""
        suggestions = suggest_spelling("xyzabc")
        self.assertEqual(len(suggestions), 0)


class TestVerbComparison(unittest.TestCase):
    """测试动词比较"""
    
    def test_compare_same_irregularity(self):
        """测试相同不规则性"""
        comparison = compare_verbs("go", "have")
        self.assertTrue(comparison["same_irregularity"])
    
    def test_compare_different_irregularity(self):
        """测试不同不规则性"""
        comparison = compare_verbs("go", "work")
        self.assertFalse(comparison["same_irregularity"])


class TestVerbTable(unittest.TestCase):
    """测试动词表格"""
    
    def test_generate_table(self):
        """测试生成表格"""
        table = generate_verb_table("walk")
        self.assertIn("walk", table.lower())
        self.assertIn("walked", table.lower())
        self.assertIn("walking", table.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)