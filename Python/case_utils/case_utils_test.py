"""
Case Utils 测试文件

测试命名风格转换工具的所有功能。
"""

import unittest
from mod import CaseUtils, to_camel_case, to_pascal_case, to_snake_case, to_kebab_case, detect_case, convert_case


class TestCaseUtils(unittest.TestCase):
    """CaseUtils 类测试"""
    
    def test_split_words(self):
        """测试单词拆分"""
        self.assertEqual(CaseUtils.split_words("helloWorld"), ['hello', 'World'])
        self.assertEqual(CaseUtils.split_words("hello_world"), ['hello', 'world'])
        self.assertEqual(CaseUtils.split_words("HelloWorld"), ['Hello', 'World'])
        self.assertEqual(CaseUtils.split_words("HELLO_WORLD"), ['HELLO', 'WORLD'])
        self.assertEqual(CaseUtils.split_words("hello-world"), ['hello', 'world'])
        self.assertEqual(CaseUtils.split_words("hello.world"), ['hello', 'world'])
        self.assertEqual(CaseUtils.split_words("hello world"), ['hello', 'world'])
        self.assertEqual(CaseUtils.split_words("HelloWorld123"), ['Hello', 'World', '123'])
        self.assertEqual(CaseUtils.split_words("XMLHttpRequest"), ['XML', 'Http', 'Request'])
        self.assertEqual(CaseUtils.split_words(""), [])
    
    def test_to_camel_case(self):
        """测试转换为 camelCase"""
        self.assertEqual(CaseUtils.to_camel_case("hello_world"), "helloWorld")
        self.assertEqual(CaseUtils.to_camel_case("HelloWorld"), "helloWorld")
        self.assertEqual(CaseUtils.to_camel_case("HELLO_WORLD"), "helloWorld")
        self.assertEqual(CaseUtils.to_camel_case("hello-world"), "helloWorld")
        self.assertEqual(CaseUtils.to_camel_case("hello.world"), "helloWorld")
        self.assertEqual(CaseUtils.to_camel_case("Hello World"), "helloWorld")
        self.assertEqual(CaseUtils.to_camel_case("xml_http_request"), "xmlHttpRequest")
        self.assertEqual(CaseUtils.to_camel_case(""), "")
    
    def test_to_pascal_case(self):
        """测试转换为 PascalCase"""
        self.assertEqual(CaseUtils.to_pascal_case("hello_world"), "HelloWorld")
        self.assertEqual(CaseUtils.to_pascal_case("helloWorld"), "HelloWorld")
        self.assertEqual(CaseUtils.to_pascal_case("HELLO_WORLD"), "HelloWorld")
        self.assertEqual(CaseUtils.to_pascal_case("hello-world"), "HelloWorld")
        self.assertEqual(CaseUtils.to_pascal_case("hello.world"), "HelloWorld")
        self.assertEqual(CaseUtils.to_pascal_case("Hello World"), "HelloWorld")
        self.assertEqual(CaseUtils.to_pascal_case("xml_http_request"), "XmlHttpRequest")
        self.assertEqual(CaseUtils.to_pascal_case(""), "")
    
    def test_to_snake_case(self):
        """测试转换为 snake_case"""
        self.assertEqual(CaseUtils.to_snake_case("helloWorld"), "hello_world")
        self.assertEqual(CaseUtils.to_snake_case("HelloWorld"), "hello_world")
        self.assertEqual(CaseUtils.to_snake_case("HELLO_WORLD"), "hello_world")
        self.assertEqual(CaseUtils.to_snake_case("hello-world"), "hello_world")
        self.assertEqual(CaseUtils.to_snake_case("hello.world"), "hello_world")
        self.assertEqual(CaseUtils.to_snake_case("Hello World"), "hello_world")
        self.assertEqual(CaseUtils.to_snake_case("xmlHttpRequest"), "xml_http_request")
        self.assertEqual(CaseUtils.to_snake_case(""), "")
    
    def test_to_screaming_snake_case(self):
        """测试转换为 SCREAMING_SNAKE_CASE"""
        self.assertEqual(CaseUtils.to_screaming_snake_case("helloWorld"), "HELLO_WORLD")
        self.assertEqual(CaseUtils.to_screaming_snake_case("HelloWorld"), "HELLO_WORLD")
        self.assertEqual(CaseUtils.to_screaming_snake_case("hello_world"), "HELLO_WORLD")
        self.assertEqual(CaseUtils.to_screaming_snake_case("hello-world"), "HELLO_WORLD")
        self.assertEqual(CaseUtils.to_screaming_snake_case("hello.world"), "HELLO_WORLD")
        self.assertEqual(CaseUtils.to_screaming_snake_case(""), "")
    
    def test_to_kebab_case(self):
        """测试转换为 kebab-case"""
        self.assertEqual(CaseUtils.to_kebab_case("helloWorld"), "hello-world")
        self.assertEqual(CaseUtils.to_kebab_case("HelloWorld"), "hello-world")
        self.assertEqual(CaseUtils.to_kebab_case("hello_world"), "hello-world")
        self.assertEqual(CaseUtils.to_kebab_case("HELLO_WORLD"), "hello-world")
        self.assertEqual(CaseUtils.to_kebab_case("hello.world"), "hello-world")
        self.assertEqual(CaseUtils.to_kebab_case("Hello World"), "hello-world")
        self.assertEqual(CaseUtils.to_kebab_case(""), "")
    
    def test_to_train_case(self):
        """测试转换为 Train-Case"""
        self.assertEqual(CaseUtils.to_train_case("helloWorld"), "Hello-World")
        self.assertEqual(CaseUtils.to_train_case("hello_world"), "Hello-World")
        self.assertEqual(CaseUtils.to_train_case("HELLO_WORLD"), "Hello-World")
        self.assertEqual(CaseUtils.to_train_case(""), "")
    
    def test_to_dot_case(self):
        """测试转换为 dot.case"""
        self.assertEqual(CaseUtils.to_dot_case("helloWorld"), "hello.world")
        self.assertEqual(CaseUtils.to_dot_case("hello_world"), "hello.world")
        self.assertEqual(CaseUtils.to_dot_case("hello-world"), "hello.world")
        self.assertEqual(CaseUtils.to_dot_case(""), "")
    
    def test_to_title_case(self):
        """测试转换为 Title Case"""
        self.assertEqual(CaseUtils.to_title_case("helloWorld"), "Hello World")
        self.assertEqual(CaseUtils.to_title_case("hello_world"), "Hello World")
        self.assertEqual(CaseUtils.to_title_case("hello-world"), "Hello World")
        self.assertEqual(CaseUtils.to_title_case("HELLO_WORLD"), "Hello World")
        self.assertEqual(CaseUtils.to_title_case(""), "")
    
    def test_to_sentence_case(self):
        """测试转换为 Sentence case"""
        self.assertEqual(CaseUtils.to_sentence_case("helloWorld"), "Hello world")
        self.assertEqual(CaseUtils.to_sentence_case("HELLO_WORLD"), "Hello world")
        self.assertEqual(CaseUtils.to_sentence_case("hello_world"), "Hello world")
        self.assertEqual(CaseUtils.to_sentence_case(""), "")
    
    def test_to_path_case(self):
        """测试转换为 path/case"""
        self.assertEqual(CaseUtils.to_path_case("helloWorld"), "hello/world")
        self.assertEqual(CaseUtils.to_path_case("hello_world"), "hello/world")
        self.assertEqual(CaseUtils.to_path_case("hello-world"), "hello/world")
        self.assertEqual(CaseUtils.to_path_case(""), "")
    
    def test_detect_case(self):
        """测试命名风格检测"""
        self.assertEqual(CaseUtils.detect_case("helloWorld"), "camel")
        self.assertEqual(CaseUtils.detect_case("HelloWorld"), "pascal")
        self.assertEqual(CaseUtils.detect_case("hello_world"), "snake")
        self.assertEqual(CaseUtils.detect_case("HELLO_WORLD"), "screaming_snake")
        self.assertEqual(CaseUtils.detect_case("hello-world"), "kebab")
        self.assertEqual(CaseUtils.detect_case("Hello-World"), "train")
        self.assertEqual(CaseUtils.detect_case("hello.world"), "dot")
        self.assertEqual(CaseUtils.detect_case("Hello World"), "title")
        self.assertEqual(CaseUtils.detect_case("hello"), "unknown")
        self.assertIsNone(CaseUtils.detect_case(""))
    
    def test_convert(self):
        """测试通用转换方法"""
        self.assertEqual(CaseUtils.convert("hello_world", "camel"), "helloWorld")
        self.assertEqual(CaseUtils.convert("hello_world", "camelCase"), "helloWorld")
        self.assertEqual(CaseUtils.convert("helloWorld", "snake"), "hello_world")
        self.assertEqual(CaseUtils.convert("helloWorld", "snake_case"), "hello_world")
        self.assertEqual(CaseUtils.convert("hello_world", "pascal"), "HelloWorld")
        self.assertEqual(CaseUtils.convert("hello_world", "kebab"), "hello-world")
        self.assertEqual(CaseUtils.convert("hello_world", "kebab-case"), "hello-world")
        self.assertEqual(CaseUtils.convert("hello_world", "dot"), "hello.world")
        self.assertEqual(CaseUtils.convert("hello_world", "title"), "Hello World")
        
        with self.assertRaises(ValueError):
            CaseUtils.convert("hello", "invalid_case")
    
    def test_convert_all(self):
        """测试转换为所有格式"""
        result = CaseUtils.convert_all("helloWorld")
        
        self.assertEqual(result['camelCase'], "helloWorld")
        self.assertEqual(result['PascalCase'], "HelloWorld")
        self.assertEqual(result['snake_case'], "hello_world")
        self.assertEqual(result['SCREAMING_SNAKE_CASE'], "HELLO_WORLD")
        self.assertEqual(result['kebab-case'], "hello-world")
        self.assertEqual(result['Train-Case'], "Hello-World")
        self.assertEqual(result['dot.case'], "hello.world")
        self.assertEqual(result['Title Case'], "Hello World")
        self.assertEqual(result['Sentence case'], "Hello world")
        self.assertEqual(result['path/case'], "hello/world")
    
    def test_is_valid_identifier(self):
        """测试命名风格验证"""
        self.assertTrue(CaseUtils.is_valid_identifier("helloWorld", "camel"))
        self.assertFalse(CaseUtils.is_valid_identifier("hello_world", "camel"))
        self.assertTrue(CaseUtils.is_valid_identifier("HelloWorld", "pascal"))
        self.assertFalse(CaseUtils.is_valid_identifier("helloWorld", "pascal"))
        self.assertTrue(CaseUtils.is_valid_identifier("hello_world", "snake"))
        self.assertTrue(CaseUtils.is_valid_identifier("HELLO_WORLD", "screaming_snake"))
        self.assertTrue(CaseUtils.is_valid_identifier("hello-world", "kebab"))
    
    def test_batch_convert(self):
        """测试批量转换"""
        inputs = ["hello_world", "fooBar", "BazQux"]
        results = CaseUtils.batch_convert(inputs, "camel")
        
        self.assertEqual(results, ["helloWorld", "fooBar", "bazQux"])
    
    def test_to_plural_snake(self):
        """测试复数 snake_case"""
        self.assertEqual(CaseUtils.to_plural_snake("userAccount"), "user_accounts")
        self.assertEqual(CaseUtils.to_plural_snake("category"), "categories")
        self.assertEqual(CaseUtils.to_plural_snake("box"), "boxes")
        self.assertEqual(CaseUtils.to_plural_snake("item"), "items")
        self.assertEqual(CaseUtils.to_plural_snake(""), "")


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_to_camel_case_function(self):
        self.assertEqual(to_camel_case("hello_world"), "helloWorld")
    
    def test_to_pascal_case_function(self):
        self.assertEqual(to_pascal_case("hello_world"), "HelloWorld")
    
    def test_to_snake_case_function(self):
        self.assertEqual(to_snake_case("helloWorld"), "hello_world")
    
    def test_to_kebab_case_function(self):
        self.assertEqual(to_kebab_case("helloWorld"), "hello-world")
    
    def test_detect_case_function(self):
        self.assertEqual(detect_case("helloWorld"), "camel")
    
    def test_convert_case_function(self):
        self.assertEqual(convert_case("hello_world", "camel"), "helloWorld")


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(CaseUtils.to_camel_case(""), "")
        self.assertEqual(CaseUtils.to_snake_case(""), "")
        self.assertEqual(CaseUtils.split_words(""), [])
    
    def test_single_word(self):
        """测试单个单词"""
        self.assertEqual(CaseUtils.to_camel_case("hello"), "hello")
        self.assertEqual(CaseUtils.to_pascal_case("hello"), "Hello")
        self.assertEqual(CaseUtils.to_snake_case("hello"), "hello")
    
    def test_numbers(self):
        """测试包含数字"""
        self.assertEqual(CaseUtils.to_snake_case("version2Update"), "version_2_update")
        self.assertEqual(CaseUtils.to_camel_case("version_2_update"), "version2Update")
    
    def test_consecutive_uppercase(self):
        """测试连续大写字母"""
        self.assertEqual(CaseUtils.to_snake_case("XMLHttpRequest"), "xml_http_request")
        self.assertEqual(CaseUtils.to_snake_case("IOError"), "io_error")
        self.assertEqual(CaseUtils.to_camel_case("XML_HTTP_REQUEST"), "xmlHttpRequest")
    
    def test_multiple_separators(self):
        """测试多个分隔符"""
        self.assertEqual(CaseUtils.to_camel_case("hello__world"), "helloWorld")
        self.assertEqual(CaseUtils.to_camel_case("hello--world"), "helloWorld")
        self.assertEqual(CaseUtils.to_camel_case("hello..world"), "helloWorld")
    
    def test_mixed_separators(self):
        """测试混合分隔符"""
        self.assertEqual(CaseUtils.to_snake_case("hello-world.test"), "hello_world_test")
        self.assertEqual(CaseUtils.to_kebab_case("hello_world.test"), "hello-world-test")


if __name__ == "__main__":
    unittest.main(verbosity=2)