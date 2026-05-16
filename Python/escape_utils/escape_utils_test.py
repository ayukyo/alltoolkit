"""
转义工具模块测试
"""

import pytest
from mod import (
    # HTML
    escape_html, unescape_html,
    # XML
    escape_xml, unescape_xml,
    # URL
    escape_url, unescape_url,
    escape_url_query, unescape_url_query,
    # JSON
    escape_json_string, unescape_json_string,
    # Shell
    escape_shell, escape_shell_args,
    # Regex
    escape_regex,
    # Glob
    escape_glob,
    # C
    escape_c_string, unescape_c_string,
    # SQL
    escape_sql_string,
    # 综合
    escape, unescape, batch_escape, batch_unescape,
    needs_escape, detect_escapes,
    escape_for_attribute, escape_for_css, escape_for_javascript,
)


class TestHtmlEscape:
    """HTML 转义测试"""
    
    def test_basic_escape(self):
        """测试基本 HTML 转义"""
        assert escape_html('<script>') == '&lt;script&gt;'
        assert escape_html('&') == '&amp;'
        assert escape_html('"test"') == '&quot;test&quot;'
        assert escape_html("'test'") == '&apos;test&apos;'
    
    def test_complex_escape(self):
        """测试复杂 HTML 转义"""
        input_text = '<div class="test">Hello & World</div>'
        expected = '&lt;div class=&quot;test&quot;&gt;Hello &amp; World&lt;/div&gt;'
        assert escape_html(input_text) == expected
    
    def test_no_escape(self):
        """测试不需要转义的字符串"""
        assert escape_html('Hello World') == 'Hello World'
        assert escape_html('123') == '123'
    
    def test_basic_unescape(self):
        """测试基本 HTML 反转义"""
        assert unescape_html('&lt;script&gt;') == '<script>'
        assert unescape_html('&amp;') == '&'
        assert unescape_html('&quot;test&quot;') == '"test"'
    
    def test_numeric_entity_decimal(self):
        """测试十进制数字实体"""
        assert unescape_html('&#65;') == 'A'
        assert unescape_html('&#128512;') == '😀'
    
    def test_numeric_entity_hex(self):
        """测试十六进制数字实体"""
        assert unescape_html('&#x41;') == 'A'
        assert unescape_html('&#X41;') == 'A'  # 大写 X
        assert unescape_html('&#x1F600;') == '😀'
    
    def test_extended_entities(self):
        """测试扩展实体"""
        assert unescape_html('&copy;') == '©'
        assert unescape_html('&euro;') == '€'
        assert unescape_html('&nbsp;') == ' '
    
    def test_escape_unescape_roundtrip(self):
        """测试转义反转义往返"""
        original = '<script>alert("XSS")</script>'
        escaped = escape_html(original)
        unescaped = unescape_html(escaped)
        assert unescaped == original
    
    def test_mixed_entities(self):
        """测试混合实体"""
        text = '&lt;div&gt;Hello&#64;&amp;&#x26;World&lt;/div&gt;'
        result = unescape_html(text)
        assert '<div>' in result
        assert '&' in result
        assert '@' in result


class TestXmlEscape:
    """XML 转义测试"""
    
    def test_basic_escape(self):
        """测试基本 XML 转义"""
        assert escape_xml('<test>') == '&lt;test&gt;'
        assert escape_xml('&') == '&amp;'
    
    def test_attribute_escape(self):
        """测试属性转义"""
        text = 'Hello\tWorld\nTest'
        result = escape_xml(text, is_attribute=True)
        assert '&#9;' in result  # tab
        assert '&#10;' in result  # newline
    
    def test_unescape(self):
        """测试 XML 反转义"""
        assert unescape_xml('&lt;test&gt;') == '<test>'
        assert unescape_xml('&amp;') == '&'
        assert unescape_xml('&#9;') == '\t'
    
    def test_numeric_entity(self):
        """测试数字实体"""
        assert unescape_xml('&#65;') == 'A'
        assert unescape_xml('&#x41;') == 'A'


class TestUrlEscape:
    """URL 编码测试"""
    
    def test_basic_encode(self):
        """测试基本 URL 编码"""
        assert escape_url('hello') == 'hello'
        assert escape_url('hello world') == 'hello+world'
        assert escape_url('hello world', plus_space=False) == 'hello%20world'
    
    def test_special_chars(self):
        """测试特殊字符编码"""
        assert escape_url('test@example.com') == 'test%40example.com'
        assert escape_url('a/b/c') == 'a%2Fb%2Fc'
    
    def test_unicode(self):
        """测试 Unicode 编码"""
        result = escape_url('你好')
        assert '%E4' in result  # UTF-8 编码开始
    
    def test_safe_chars(self):
        """测试安全字符"""
        assert escape_url('test-file.txt') == 'test-file.txt'
        assert escape_url('user_name') == 'user_name'
    
    def test_custom_safe(self):
        """测试自定义安全字符"""
        assert escape_url('test@example.com', safe='@') == 'test@example.com'
    
    def test_basic_decode(self):
        """测试基本 URL 解码"""
        assert unescape_url('hello+world') == 'hello world'
        assert unescape_url('hello%20world') == 'hello world'
        assert unescape_url('test%40example.com') == 'test@example.com'
    
    def test_unicode_decode(self):
        """测试 Unicode 解码"""
        result = unescape_url('%E4%BD%A0%E5%A5%BD')
        assert result == '你好'
    
    def test_encode_decode_roundtrip(self):
        """测试编码解码往返"""
        original = 'Hello 世界! @#$'
        encoded = escape_url(original)
        decoded = unescape_url(encoded)
        assert decoded == original
    
    def test_query_encode(self):
        """测试查询字符串编码"""
        params = {'name': '张三', 'age': '25'}
        result = escape_url_query(params)
        assert 'name=' in result
        assert 'age=25' in result
    
    def test_query_with_list(self):
        """测试列表参数"""
        params = {'tags': ['a', 'b', 'c']}
        result = escape_url_query(params)
        assert 'tags=a' in result
        assert 'tags=b' in result
        assert 'tags=c' in result
    
    def test_query_decode(self):
        """测试查询字符串解码"""
        query = 'name=%E5%BC%A0%E4%B8%89&age=25'
        result = unescape_url_query(query)
        assert result['name'] == '张三'
        assert result['age'] == '25'
    
    def test_query_decode_repeated(self):
        """测试重复参数解码"""
        query = 'tag=a&tag=b&tag=c'
        result = unescape_url_query(query)
        assert result['tag'] == ['a', 'b', 'c']
    
    def test_query_decode_empty(self):
        """测试空查询字符串"""
        assert unescape_url_query('') == {}
        assert unescape_url_query('?') == {}


class TestJsonEscape:
    """JSON 字符串转义测试"""
    
    def test_basic_escape(self):
        """测试基本 JSON 转义"""
        assert escape_json_string('hello') == 'hello'
        assert escape_json_string('Hello\\nWorld') == 'Hello\\\\nWorld'
        assert escape_json_string('"test"') == '\\\"test\\\"'
    
    def test_control_chars(self):
        """测试控制字符"""
        assert '\\b' in escape_json_string('\b')
        assert '\\n' in escape_json_string('\n')
        assert '\\r' in escape_json_string('\r')
        assert '\\t' in escape_json_string('\t')
    
    def test_ensure_ascii(self):
        """测试 ASCII 模式"""
        result = escape_json_string('你好', ensure_ascii=True)
        assert '\\u' in result
        
        result = escape_json_string('你好', ensure_ascii=False)
        assert '你好' == result
    
    def test_unicode_escape(self):
        """测试 Unicode 转义"""
        result = escape_json_string('😀', ensure_ascii=True)
        assert '\\u' in result
    
    def test_basic_unescape(self):
        """测试基本 JSON 反转义"""
        assert unescape_json_string('hello') == 'hello'
        assert unescape_json_string('Hello\\\\nWorld') == 'Hello\\nWorld'
    
    def test_unicode_unescape(self):
        """测试 Unicode 反转义"""
        assert unescape_json_string('\\u0041') == 'A'
        assert unescape_json_string('\\u4F60\\u597D') == '你好'
    
    def test_escape_unescape_roundtrip(self):
        """测试转义反转义往返"""
        original = 'Hello\\nWorld\\t"测试"'
        escaped = escape_json_string(original)
        unescaped = unescape_json_string(escaped)
        assert unescaped == original


class TestShellEscape:
    """Shell 转义测试"""
    
    def test_basic_escape(self):
        """测试基本 Shell 转义"""
        assert escape_shell('hello') == 'hello'
        assert escape_shell('hello world') == "'hello world'"
        assert escape_shell('$HOME') == "'$HOME'"
    
    def test_single_quotes(self):
        """测试单引号处理"""
        result = escape_shell("it's a test")
        assert '"' in result  # 应使用双引号
    
    def test_empty_string(self):
        """测试空字符串"""
        assert escape_shell('') == "''"
    
    def test_special_chars(self):
        """测试特殊字符"""
        assert escape_shell('test&command') == "'test&command'"
        assert escape_shell('a | b') == "'a | b'"
    
    def test_windows_style(self):
        """测试 Windows 风格"""
        result = escape_shell('test.txt', style='windows')
        assert result == 'test.txt'  # 不需要转义
    
        result = escape_shell('test file.txt', style='windows')
        assert '"' in result
    
    def test_args_escape(self):
        """测试参数列表转义"""
        result = escape_shell_args(['echo', 'hello world'])
        assert result == "echo 'hello world'"
    
    def test_args_empty(self):
        """测试空参数列表"""
        result = escape_shell_args([])
        assert result == ''


class TestRegexEscape:
    """正则表达式转义测试"""
    
    def test_basic_escape(self):
        """测试基本正则转义"""
        assert escape_regex('hello') == 'hello'
        assert escape_regex('a.b') == 'a\\.b'
        assert escape_regex('a*b+c') == 'a\\*b\\+c'
    
    def test_special_chars(self):
        """测试特殊字符"""
        result = escape_regex('test[0-9]')
        assert '\\[' in result
        assert '\\]' in result
    
    def test_all_meta_chars(self):
        """测试所有元字符"""
        test = '\\.^$*+?{}[]|()'
        result = escape_regex(test)
        # 每个字符都应该被转义
        for char in test:
            if char == '\\':
                continue  # 第一个反斜杠本身就是转义字符
            assert '\\' + char in result or result.count('\\') > len(test)


class TestGlobEscape:
    """Glob 模式转义测试"""
    
    def test_basic_escape(self):
        """测试基本 Glob 转义"""
        assert escape_glob('file.txt') == 'file.txt'
        assert escape_glob('file*.txt') == 'file\\*.txt'
        assert escape_glob('file?.txt') == 'file\\?.txt'
    
    def test_brackets(self):
        """测试方括号"""
        result = escape_glob('file[0-9].txt')
        assert '\\[' in result
        assert '\\]' in result


class TestCEscape:
    """C 语言字符串转义测试"""
    
    def test_basic_escape(self):
        """测试基本 C 转义"""
        assert escape_c_string('hello') == 'hello'
        assert escape_c_string('\\n') == '\\\\n'
        assert escape_c_string('\\t') == '\\\\t'
    
    def test_control_chars(self):
        """测试控制字符"""
        assert '\\b' in escape_c_string('\b')
        assert '\\n' in escape_c_string('\n')
        assert '\\r' in escape_c_string('\r')
        assert '\\t' in escape_c_string('\t')
    
    def test_quotes(self):
        """测试引号"""
        assert escape_c_string('"test"') == '\\\"test\\\"'
        assert escape_c_string("'test'") == "\\'test\\'"
    
    def test_basic_unescape(self):
        """测试基本 C 反转义"""
        assert unescape_c_string('hello') == 'hello'
        assert unescape_c_string('\\\\n') == '\\n'
    
    def test_hex_unescape(self):
        """测试十六进制反转义"""
        assert unescape_c_string('\\x41') == 'A'
        assert unescape_c_string('\\x61') == 'a'
    
    def test_octal_unescape(self):
        """测试八进制反转义"""
        # 使用原始字符串避免 Python 解释器的八进制解析
        assert unescape_c_string(r'\101') == 'A'  # 101 octal = 65 decimal
    
    def test_escape_unescape_roundtrip(self):
        """测试转义反转义往返"""
        original = 'Hello\\nWorld\\t"Test"'
        escaped = escape_c_string(original)
        unescaped = unescape_c_string(escaped)
        assert unescaped == original


class TestSqlEscape:
    """SQL 字符串转义测试"""
    
    def test_standard_style(self):
        """测试标准 SQL 风格"""
        assert escape_sql_string("O'Brien") == "O''Brien"
        assert escape_sql_string("test's value") == "test''s value"
    
    def test_mysql_style(self):
        """测试 MySQL 风格"""
        result = escape_sql_string("O'Brien", style='mysql')
        assert "'" in result
    
    def test_postgres_style(self):
        """测试 PostgreSQL 风格"""
        assert escape_sql_string("O'Brien", style='postgres') == "O''Brien"


class TestGenericEscape:
    """综合转义测试"""
    
    def test_escape_function(self):
        """测试综合转义函数"""
        assert escape('<test>', 'html') == '&lt;test&gt;'
        assert escape('hello world', 'url') == 'hello+world'
        assert escape('a.b', 'regex') == 'a\\.b'
    
    def test_unescape_function(self):
        """测试综合反转义函数"""
        assert unescape('&lt;test&gt;', 'html') == '<test>'
        assert unescape('hello+world', 'url') == 'hello world'
    
    def test_unknown_format(self):
        """测试未知格式"""
        with pytest.raises(ValueError):
            escape('test', 'unknown')
        
        with pytest.raises(ValueError):
            unescape('test', 'unknown')
    
    def test_batch_escape(self):
        """测试批量转义"""
        texts = ['<a>', '<b>', '<c>']
        result = batch_escape(texts, 'html')
        assert result == ['&lt;a&gt;', '&lt;b&gt;', '&lt;c&gt;']
    
    def test_batch_unescape(self):
        """测试批量反转义"""
        texts = ['&lt;a&gt;', '&lt;b&gt;', '&lt;c&gt;']
        result = batch_unescape(texts, 'html')
        assert result == ['<a>', '<b>', '<c>']


class TestNeedsEscape:
    """检测函数测试"""
    
    def test_html_needs(self):
        """测试 HTML 检测"""
        assert needs_escape('<test>', 'html') is True
        assert needs_escape('hello', 'html') is False
        assert needs_escape('&', 'html') is True
    
    def test_url_needs(self):
        """测试 URL 检测"""
        assert needs_escape('hello world', 'url') is True
        assert needs_escape('hello', 'url') is False
        assert needs_escape('test@example', 'url') is True
    
    def test_shell_needs(self):
        """测试 Shell 检测"""
        assert needs_escape('hello world', 'shell') is True
        assert needs_escape('hello', 'shell') is False
        assert needs_escape('$HOME', 'shell') is True
    
    def test_regex_needs(self):
        """测试正则检测"""
        assert needs_escape('a.b', 'regex') is True
        assert needs_escape('abc', 'regex') is False
    
    def test_glob_needs(self):
        """测试 Glob 检测"""
        assert needs_escape('file*.txt', 'glob') is True
        assert needs_escape('file.txt', 'glob') is False


class TestDetectEscapes:
    """转义格式检测测试"""
    
    def test_html_detection(self):
        """测试 HTML 检测"""
        result = detect_escapes('&lt;div&gt;')
        assert 'html' in result
    
    def test_url_detection(self):
        """测试 URL 检测"""
        result = detect_escapes('hello%20world')
        assert 'url' in result
    
    def test_json_detection(self):
        """测试 JSON 检测"""
        result = detect_escapes('Hello\\nWorld')
        assert 'json' in result
    
    def test_c_detection(self):
        """测试 C 检测"""
        result = detect_escapes('Hello\\nWorld')
        assert 'c' in result  # JSON 和 C 都有 \\n
    
    def test_multiple_detection(self):
        """测试多重检测"""
        text = '&lt;test%20value&#64;'
        result = detect_escapes(text)
        assert 'html' in result
        assert 'url' in result
    
    def test_no_detection(self):
        """测试无检测"""
        result = detect_escapes('hello world')
        assert result == []


class TestHelperFunctions:
    """辅助函数测试"""
    
    def test_escape_for_attribute(self):
        """测试属性转义"""
        result = escape_for_attribute('test"value')
        assert '&quot;' in result
    
    def test_escape_for_attribute_xml(self):
        """测试 XML 属性转义"""
        result = escape_for_attribute('test\tvalue', attr_type='xml')
        assert '&#9;' in result
    
    def test_escape_for_css(self):
        """测试 CSS 转义"""
        result = escape_for_css('test<style>')
        assert '\\' in result
    
    def test_escape_for_javascript(self):
        """测试 JavaScript 转义"""
        result = escape_for_javascript('test\n"value"')
        assert '\\n' in result
        assert '\\\"' in result


class TestEdgeCases:
    """边界情况测试"""
    
    def test_empty_string(self):
        """测试空字符串"""
        assert escape_html('') == ''
        assert escape_url('') == ''
        assert escape_json_string('') == ''
    
    def test_none_handling(self):
        """测试 None 值处理"""
        # Shell 转义支持空字符串
        assert escape_shell('') == "''"
    
    def test_unicode_string(self):
        """测试 Unicode 字符串"""
        text = '你好世界🎉'
        
        # HTML 不转义 Unicode
        assert escape_html(text) == text
        
        # URL 编码 Unicode
        result = escape_url(text)
        assert '%' in result
        
        # JSON 可以选择
        assert escape_json_string(text, ensure_ascii=False) == text
        assert '\\u' in escape_json_string(text, ensure_ascii=True)
    
    def test_long_string(self):
        """测试长字符串"""
        long_text = 'a' * 10000 + '<test>' + 'b' * 10000
        result = escape_html(long_text)
        assert '&lt;test&gt;' in result
    
    def test_mixed_content(self):
        """测试混合内容"""
        text = '<div>Hello &amp; World</div>'
        # 先反转义再转义
        unescaped = unescape_html(text)
        escaped = escape_html(unescaped)
        # 注意：反转义后 <div> 会变成真正的标签，再转义后会被转义
        assert unescaped == '<div>Hello & World</div>'
        assert escaped == '&lt;div&gt;Hello &amp; World&lt;/div&gt;'
    
    def test_double_escape(self):
        """测试双重转义"""
        text = '<test>'
        first = escape_html(text)
        second = escape_html(first)
        # 第二次转义会把 & 也转义
        assert '&amp;lt;' in second


class TestPerformance:
    """性能测试"""
    
    def test_large_html_escape(self):
        """测试大量 HTML 转义"""
        text = '<div>' * 1000 + 'content' + '</div>' * 1000
        result = escape_html(text)
        assert '&lt;div&gt;' in result
    
    def test_large_url_encode(self):
        """测试大量 URL 编码"""
        text = 'hello world ' * 1000
        result = escape_url(text)
        assert '+' in result or '%20' in result
    
    def test_large_json_escape(self):
        """测试大量 JSON 转义"""
        text = 'test\n' * 1000
        result = escape_json_string(text)
        assert '\\n' in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])