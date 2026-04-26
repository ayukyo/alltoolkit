"""
pluralize_utils 测试文件

测试英文单词单复数转换功能。
"""

import unittest
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pluralize_utils.mod import (
    singular_to_plural,
    plural_to_singular,
    is_plural,
    get_plural_form,
    batch_pluralize,
    batch_singularize,
    get_article,
    format_count,
    IRREGULAR_PLURALS,
    UNCOUNTABLE_WORDS,
)


class TestSingularToPlural(unittest.TestCase):
    """测试单数转复数功能"""
    
    def test_regular_nouns(self):
        """测试规则名词"""
        self.assertEqual(singular_to_plural('cat'), 'cats')
        self.assertEqual(singular_to_plural('dog'), 'dogs')
        self.assertEqual(singular_to_plural('book'), 'books')
        self.assertEqual(singular_to_plural('pen'), 'pens')
        self.assertEqual(singular_to_plural('table'), 'tables')
    
    def test_ending_with_s_x_z_ch_sh(self):
        """测试以 s, x, z, ch, sh 结尾的名词"""
        self.assertEqual(singular_to_plural('bus'), 'buses')
        self.assertEqual(singular_to_plural('box'), 'boxes')
        self.assertEqual(singular_to_plural('quiz'), 'quizzes')
        self.assertEqual(singular_to_plural('church'), 'churches')
        self.assertEqual(singular_to_plural('brush'), 'brushes')
        self.assertEqual(singular_to_plural('class'), 'classes')
        self.assertEqual(singular_to_plural('glass'), 'glasses')
    
    def test_ending_with_y(self):
        """测试以 y 结尾的名词"""
        # 辅音 + y -> ies
        self.assertEqual(singular_to_plural('city'), 'cities')
        self.assertEqual(singular_to_plural('story'), 'stories')
        self.assertEqual(singular_to_plural('baby'), 'babies')
        self.assertEqual(singular_to_plural('party'), 'parties')
        # 元音 + y -> ys
        self.assertEqual(singular_to_plural('day'), 'days')
        self.assertEqual(singular_to_plural('boy'), 'boys')
        self.assertEqual(singular_to_plural('toy'), 'toys')
        self.assertEqual(singular_to_plural('key'), 'keys')
    
    def test_ending_with_o(self):
        """测试以 o 结尾的名词"""
        # -oes 结尾
        self.assertEqual(singular_to_plural('potato'), 'potatoes')
        self.assertEqual(singular_to_plural('tomato'), 'tomatoes')
        self.assertEqual(singular_to_plural('hero'), 'heroes')
        self.assertEqual(singular_to_plural('echo'), 'echoes')
        # -os 结尾
        self.assertEqual(singular_to_plural('photo'), 'photos')
        self.assertEqual(singular_to_plural('piano'), 'pianos')
        self.assertEqual(singular_to_plural('radio'), 'radios')
    
    def test_ending_with_f_fe(self):
        """测试以 f/fe 结尾的名词"""
        self.assertEqual(singular_to_plural('knife'), 'knives')
        self.assertEqual(singular_to_plural('wife'), 'wives')
        self.assertEqual(singular_to_plural('life'), 'lives')
        self.assertEqual(singular_to_plural('leaf'), 'leaves')
        self.assertEqual(singular_to_plural('wolf'), 'wolves')
        self.assertEqual(singular_to_plural('shelf'), 'shelves')
        # 不变的
        self.assertEqual(singular_to_plural('roof'), 'roofs')
        self.assertEqual(singular_to_plural('chief'), 'chiefs')
        self.assertEqual(singular_to_plural('belief'), 'beliefs')
    
    def test_irregular_nouns(self):
        """测试不规则变化名词"""
        self.assertEqual(singular_to_plural('man'), 'men')
        self.assertEqual(singular_to_plural('woman'), 'women')
        self.assertEqual(singular_to_plural('child'), 'children')
        self.assertEqual(singular_to_plural('person'), 'people')
        self.assertEqual(singular_to_plural('foot'), 'feet')
        self.assertEqual(singular_to_plural('tooth'), 'teeth')
        self.assertEqual(singular_to_plural('goose'), 'geese')
        self.assertEqual(singular_to_plural('mouse'), 'mice')
        self.assertEqual(singular_to_plural('ox'), 'oxen')
    
    def test_latin_greek_nouns(self):
        """测试拉丁/希腊源名词"""
        self.assertEqual(singular_to_plural('analysis'), 'analyses')
        self.assertEqual(singular_to_plural('basis'), 'bases')
        self.assertEqual(singular_to_plural('crisis'), 'crises')
        self.assertEqual(singular_to_plural('phenomenon'), 'phenomena')
        self.assertEqual(singular_to_plural('criterion'), 'criteria')
        self.assertEqual(singular_to_plural('datum'), 'data')
        self.assertEqual(singular_to_plural('medium'), 'media')
        self.assertEqual(singular_to_plural('curriculum'), 'curricula')
        self.assertEqual(singular_to_plural('appendix'), 'appendices')
        self.assertEqual(singular_to_plural('index'), 'indices')
        self.assertEqual(singular_to_plural('matrix'), 'matrices')
        self.assertEqual(singular_to_plural('focus'), 'foci')
        self.assertEqual(singular_to_plural('fungus'), 'fungi')
        self.assertEqual(singular_to_plural('nucleus'), 'nuclei')
        self.assertEqual(singular_to_plural('stimulus'), 'stimuli')
        self.assertEqual(singular_to_plural('syllabus'), 'syllabi')
    
    def test_uncountable_nouns(self):
        """测试不可数名词"""
        self.assertEqual(singular_to_plural('sheep'), 'sheep')
        self.assertEqual(singular_to_plural('deer'), 'deer')
        self.assertEqual(singular_to_plural('fish'), 'fish')
        self.assertEqual(singular_to_plural('species'), 'species')
        self.assertEqual(singular_to_plural('series'), 'series')
        self.assertEqual(singular_to_plural('moose'), 'moose')
        self.assertEqual(singular_to_plural('information'), 'information')
        self.assertEqual(singular_to_plural('news'), 'news')
    
    def test_case_preservation(self):
        """测试大小写保持"""
        self.assertEqual(singular_to_plural('Cat'), 'Cats')
        self.assertEqual(singular_to_plural('CAT'), 'CATS')
        self.assertEqual(singular_to_plural('Child'), 'Children')
        self.assertEqual(singular_to_plural('MAN'), 'MEN')
    
    def test_with_count(self):
        """测试带数量参数"""
        self.assertEqual(singular_to_plural('cat', count=1), 'cat')
        self.assertEqual(singular_to_plural('cat', count=2), 'cats')
        self.assertEqual(singular_to_plural('cat', count=0), 'cats')
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(singular_to_plural(''), '')
    
    def test_hyphenated_words(self):
        """测试连字符复合词"""
        self.assertEqual(singular_to_plural('brother-in-law'), 'brothers-in-law')
        self.assertEqual(singular_to_plural('mother-in-law'), 'mothers-in-law')
        self.assertEqual(singular_to_plural('passer-by'), 'passers-by')
    
    def test_pronouns(self):
        """测试代词"""
        self.assertEqual(singular_to_plural('he'), 'they')
        self.assertEqual(singular_to_plural('she'), 'they')
        self.assertEqual(singular_to_plural('it'), 'they')
        self.assertEqual(singular_to_plural('this'), 'these')
        self.assertEqual(singular_to_plural('that'), 'those')


class TestPluralToSingular(unittest.TestCase):
    """测试复数转单数功能"""
    
    def test_regular_nouns(self):
        """测试规则名词"""
        self.assertEqual(plural_to_singular('cats'), 'cat')
        self.assertEqual(plural_to_singular('dogs'), 'dog')
        self.assertEqual(plural_to_singular('books'), 'book')
    
    def test_ending_with_es(self):
        """测试以 es 结尾的名词"""
        self.assertEqual(plural_to_singular('boxes'), 'box')
        self.assertEqual(plural_to_singular('buses'), 'bus')
        self.assertEqual(plural_to_singular('churches'), 'church')
        self.assertEqual(plural_to_singular('brushes'), 'brush')
        self.assertEqual(plural_to_singular('classes'), 'class')
    
    def test_ending_with_ies(self):
        """测试以 ies 结尾的名词"""
        self.assertEqual(plural_to_singular('cities'), 'city')
        self.assertEqual(plural_to_singular('stories'), 'story')
        self.assertEqual(plural_to_singular('babies'), 'baby')
        self.assertEqual(plural_to_singular('parties'), 'party')
    
    def test_ending_with_ves(self):
        """测试以 ves 结尾的名词"""
        self.assertEqual(plural_to_singular('knives'), 'knife')
        self.assertEqual(plural_to_singular('wives'), 'wife')
        self.assertEqual(plural_to_singular('lives'), 'life')
        self.assertEqual(plural_to_singular('leaves'), 'leaf')
        self.assertEqual(plural_to_singular('wolves'), 'wolf')
    
    def test_irregular_nouns(self):
        """测试不规则变化名词"""
        self.assertEqual(plural_to_singular('men'), 'man')
        self.assertEqual(plural_to_singular('women'), 'woman')
        self.assertEqual(plural_to_singular('children'), 'child')
        self.assertEqual(plural_to_singular('people'), 'person')
        self.assertEqual(plural_to_singular('feet'), 'foot')
        self.assertEqual(plural_to_singular('teeth'), 'tooth')
        self.assertEqual(plural_to_singular('geese'), 'goose')
        self.assertEqual(plural_to_singular('mice'), 'mouse')
    
    def test_latin_greek_nouns(self):
        """测试拉丁/希腊源名词"""
        self.assertEqual(plural_to_singular('analyses'), 'analysis')
        self.assertEqual(plural_to_singular('bases'), 'basis')  # 也可以是 base 的复数
        self.assertEqual(plural_to_singular('crises'), 'crisis')
        self.assertEqual(plural_to_singular('phenomena'), 'phenomenon')
        self.assertEqual(plural_to_singular('criteria'), 'criterion')
        self.assertEqual(plural_to_singular('data'), 'datum')
        self.assertEqual(plural_to_singular('media'), 'medium')
        self.assertEqual(plural_to_singular('curricula'), 'curriculum')
        self.assertEqual(plural_to_singular('foci'), 'focus')
        self.assertEqual(plural_to_singular('fungi'), 'fungus')
        self.assertEqual(plural_to_singular('nuclei'), 'nucleus')
        self.assertEqual(plural_to_singular('stimuli'), 'stimulus')
    
    def test_uncountable_nouns(self):
        """测试不可数名词"""
        self.assertEqual(plural_to_singular('sheep'), 'sheep')
        self.assertEqual(plural_to_singular('deer'), 'deer')
        self.assertEqual(plural_to_singular('fish'), 'fish')
        self.assertEqual(plural_to_singular('information'), 'information')
    
    def test_case_preservation(self):
        """测试大小写保持"""
        self.assertEqual(plural_to_singular('Cats'), 'Cat')
        self.assertEqual(plural_to_singular('CATS'), 'CAT')
        self.assertEqual(plural_to_singular('Children'), 'Child')
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(plural_to_singular(''), '')


class TestIsPlural(unittest.TestCase):
    """测试判断复数功能"""
    
    def test_regular_plurals(self):
        """测试规则复数"""
        self.assertTrue(is_plural('cats'))
        self.assertTrue(is_plural('dogs'))
        self.assertTrue(is_plural('boxes'))
        self.assertTrue(is_plural('cities'))
    
    def test_singular_nouns(self):
        """测试单数名词"""
        self.assertFalse(is_plural('cat'))
        self.assertFalse(is_plural('dog'))
        self.assertFalse(is_plural('box'))
        self.assertFalse(is_plural('city'))
    
    def test_irregular_plurals(self):
        """测试不规则复数"""
        self.assertTrue(is_plural('men'))
        self.assertTrue(is_plural('women'))
        self.assertTrue(is_plural('children'))
        self.assertTrue(is_plural('people'))
        self.assertTrue(is_plural('feet'))
        self.assertTrue(is_plural('teeth'))
    
    def test_uncountable_nouns(self):
        """测试不可数名词"""
        self.assertFalse(is_plural('sheep'))
        self.assertFalse(is_plural('deer'))
        self.assertFalse(is_plural('fish'))
        self.assertFalse(is_plural('information'))
    
    def test_latin_plurals(self):
        """测试拉丁复数"""
        self.assertTrue(is_plural('data'))
        self.assertTrue(is_plural('media'))
        self.assertTrue(is_plural('criteria'))
        self.assertTrue(is_plural('phenomena'))
        self.assertTrue(is_plural('analyses'))
    
    def test_words_ending_with_s_but_singular(self):
        """测试以 s 结尾但为单数的词"""
        self.assertFalse(is_plural('news'))
        self.assertFalse(is_plural('politics'))
        self.assertFalse(is_plural('mathematics'))
        self.assertFalse(is_plural('physics'))
        self.assertFalse(is_plural('series'))
        self.assertFalse(is_plural('species'))


class TestGetPluralForm(unittest.TestCase):
    """测试根据数量获取正确形式"""
    
    def test_count_one(self):
        """测试数量为1"""
        self.assertEqual(get_plural_form('cat', 1), 'cat')
        self.assertEqual(get_plural_form('cats', 1), 'cat')
        self.assertEqual(get_plural_form('box', 1), 'box')
    
    def test_count_other(self):
        """测试其他数量"""
        self.assertEqual(get_plural_form('cat', 0), 'cats')
        self.assertEqual(get_plural_form('cat', 2), 'cats')
        self.assertEqual(get_plural_form('cat', 100), 'cats')
        self.assertEqual(get_plural_form('box', 2), 'boxes')


class TestBatchOperations(unittest.TestCase):
    """测试批量操作"""
    
    def test_batch_pluralize(self):
        """测试批量转复数"""
        result = batch_pluralize(['cat', 'dog', 'box', 'city'])
        self.assertEqual(result, ['cats', 'dogs', 'boxes', 'cities'])
    
    def test_batch_singularize(self):
        """测试批量转单数"""
        result = batch_singularize(['cats', 'dogs', 'boxes', 'cities'])
        self.assertEqual(result, ['cat', 'dog', 'box', 'city'])
    
    def test_empty_list(self):
        """测试空列表"""
        self.assertEqual(batch_pluralize([]), [])
        self.assertEqual(batch_singularize([]), [])


class TestGetArticle(unittest.TestCase):
    """测试冠词功能"""
    
    def test_consonant_start(self):
        """测试辅音开头的词"""
        self.assertEqual(get_article('cat'), 'a')
        self.assertEqual(get_article('dog'), 'a')
        self.assertEqual(get_article('book'), 'a')
    
    def test_vowel_start(self):
        """测试元音开头的词"""
        self.assertEqual(get_article('apple'), 'an')
        self.assertEqual(get_article('orange'), 'an')
        self.assertEqual(get_article('elephant'), 'an')
    
    def test_with_count(self):
        """测试带数量"""
        self.assertEqual(get_article('cat', 1), 'a')
        self.assertEqual(get_article('apple', 1), 'an')
        self.assertEqual(get_article('cat', 2), '')
        self.assertEqual(get_article('cat', 0), '')
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        self.assertEqual(get_article('Apple'), 'an')
        self.assertEqual(get_article('ORANGE'), 'an')
        self.assertEqual(get_article('Cat'), 'a')


class TestFormatCount(unittest.TestCase):
    """测试格式化数量功能"""
    
    def test_single_item(self):
        """测试单个项目"""
        self.assertEqual(format_count('cat', 1), 'a cat')
        self.assertEqual(format_count('apple', 1), 'an apple')
        self.assertEqual(format_count('dog', 1), 'a dog')
    
    def test_multiple_items(self):
        """测试多个项目"""
        self.assertEqual(format_count('cat', 0), '0 cats')
        self.assertEqual(format_count('cat', 2), '2 cats')
        self.assertEqual(format_count('box', 5), '5 boxes')
        self.assertEqual(format_count('city', 10), '10 cities')
    
    def test_without_article(self):
        """测试不包含冠词"""
        self.assertEqual(format_count('cat', 1, include_article=False), 'cat')
        self.assertEqual(format_count('apple', 1, include_article=False), 'apple')
    
    def test_irregular_nouns(self):
        """测试不规则名词"""
        self.assertEqual(format_count('child', 2), '2 children')
        self.assertEqual(format_count('person', 5), '5 people')
        self.assertEqual(format_count('man', 3), '3 men')


class TestRoundTrip(unittest.TestCase):
    """测试往返转换"""
    
    def test_singular_plural_singular(self):
        """测试单数->复数->单数"""
        words = ['cat', 'dog', 'box', 'city', 'knife', 'child', 'man', 'person']
        for word in words:
            plural = singular_to_plural(word)
            singular = plural_to_singular(plural)
            self.assertEqual(singular, word, f"Failed for {word} -> {plural} -> {singular}")
    
    def test_plural_singular_plural(self):
        """测试复数->单数->复数"""
        words = ['cats', 'dogs', 'boxes', 'cities', 'knives', 'children', 'men', 'people']
        for word in words:
            singular = plural_to_singular(word)
            plural = singular_to_plural(singular)
            self.assertEqual(plural, word, f"Failed for {word} -> {singular} -> {plural}")


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def test_single_letter(self):
        """测试单字母"""
        # 'a' 加 's' -> 'as'
        self.assertEqual(singular_to_plural('a'), 'as')
        # 'x' 以 'x' 结尾，加 'es' -> 'xes'
        self.assertEqual(singular_to_plural('x'), 'xes')
        # 大写 'X' -> 'XES'
        self.assertEqual(singular_to_plural('X'), 'XES')
    
    def test_numbers_in_word(self):
        """测试包含数字的词"""
        self.assertEqual(singular_to_plural('MP3'), 'MP3s')
        self.assertEqual(singular_to_plural('PDF'), 'PDFs')
    
    def test_already_plural(self):
        """测试已经是复数的词"""
        # 注意：singular_to_plural 函数假设输入是单数形式
        # 如果输入已经是复数（如 'cats'），它会被当作以 -s 结尾的单数词处理
        # 'cats' -> 'cats' + 'es' = 'catses'（因为以 -s 结尾加 -es）
        self.assertEqual(singular_to_plural('cats'), 'catses')  # 以 -s 结尾加 -es
    
    def test_unicode(self):
        """测试Unicode字符"""
        # 简单处理，Unicode字符会加s
        self.assertEqual(singular_to_plural('café'), 'cafés')


if __name__ == '__main__':
    unittest.main(verbosity=2)