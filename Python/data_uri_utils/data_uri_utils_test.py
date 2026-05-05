"""
Data URI Utilities 测试用例

运行: python data_uri_utils_test.py
"""

import os
import tempfile
import unittest

from data_uri_utils import (
    DataURI,
    batch_encode,
    create_html_embed,
    decode_data_uri,
    decode_to_file,
    encode_data,
    encode_file,
    estimate_size,
    get_extension,
    get_info,
    get_mime_type,
    html_to_data_uri,
    is_data_uri,
    json_to_data_uri,
    svg_to_data_uri,
    text_to_data_uri,
)


class TestMIMETypeDetection(unittest.TestCase):
    """MIME 类型检测测试"""
    
    def test_image_types(self):
        """测试图片 MIME 类型"""
        self.assertEqual(get_mime_type('test.png'), 'image/png')
        self.assertEqual(get_mime_type('test.jpg'), 'image/jpeg')
        self.assertEqual(get_mime_type('test.jpeg'), 'image/jpeg')
        self.assertEqual(get_mime_type('test.gif'), 'image/gif')
        self.assertEqual(get_mime_type('test.svg'), 'image/svg+xml')
        self.assertEqual(get_mime_type('test.webp'), 'image/webp')
    
    def test_document_types(self):
        """测试文档 MIME 类型"""
        self.assertEqual(get_mime_type('test.pdf'), 'application/pdf')
        self.assertEqual(get_mime_type('test.json'), 'application/json')
        self.assertEqual(get_mime_type('test.xml'), 'application/xml')
    
    def test_text_types(self):
        """测试文本 MIME 类型"""
        self.assertEqual(get_mime_type('test.txt'), 'text/plain')
        self.assertEqual(get_mime_type('test.html'), 'text/html')
        self.assertEqual(get_mime_type('test.css'), 'text/css')
        self.assertEqual(get_mime_type('test.csv'), 'text/csv')
    
    def test_unknown_type(self):
        """测试未知类型"""
        self.assertEqual(get_mime_type('test.xyz'), 'application/octet-stream')


class TestExtensionMapping(unittest.TestCase):
    """扩展名映射测试"""
    
    def test_get_extension(self):
        """测试获取扩展名"""
        self.assertEqual(get_extension('image/png'), '.png')
        self.assertEqual(get_extension('image/jpeg'), '.jpg')
        self.assertEqual(get_extension('application/json'), '.json')
        self.assertEqual(get_extension('text/plain'), '.txt')


class TestEncodeData(unittest.TestCase):
    """数据编码测试"""
    
    def test_encode_binary_data(self):
        """测试二进制数据编码"""
        data = b'\x89PNG\r\n\x1a\n'  # PNG 文件头
        uri = encode_data(data, 'image/png', use_base64=True)
        
        self.assertTrue(uri.startswith('data:image/png;base64,'))
        self.assertTrue(is_data_uri(uri))
    
    def test_encode_text_data(self):
        """测试文本数据编码"""
        text = "Hello, World!"
        uri = text_to_data_uri(text)
        
        self.assertTrue(uri.startswith('data:text/plain,'))
        self.assertIn('Hello', uri)
    
    def test_encode_json(self):
        """测试 JSON 编码"""
        json_str = '{"key": "value"}'
        uri = json_to_data_uri(json_str)
        
        self.assertTrue(uri.startswith('data:application/json;base64,'))
    
    def test_encode_html(self):
        """测试 HTML 编码"""
        html = '<html><body>Test</body></html>'
        uri = html_to_data_uri(html)
        
        self.assertTrue(uri.startswith('data:text/html;base64,'))
    
    def test_encode_svg(self):
        """测试 SVG 编码"""
        svg = '<svg><circle cx="50" cy="50" r="40"/></svg>'
        uri = svg_to_data_uri(svg)
        
        self.assertTrue(uri.startswith('data:image/svg+xml;base64,'))


class TestDecodeDataURI(unittest.TestCase):
    """Data URI 解码测试"""
    
    def test_decode_base64(self):
        """测试 base64 解码"""
        original = b'Hello, Data URI!'
        uri = encode_data(original, 'text/plain', use_base64=True)
        
        decoded = decode_data_uri(uri)
        
        self.assertEqual(decoded.data, original)
        self.assertEqual(decoded.mime_type, 'text/plain')
        self.assertEqual(decoded.encoding, 'base64')
        self.assertTrue(decoded.is_base64)
    
    def test_decode_text_plain(self):
        """测试纯文本解码"""
        text = "Simple text"
        uri = text_to_data_uri(text)
        
        decoded = decode_data_uri(uri)
        
        self.assertEqual(decoded.decode_text(), text)
    
    def test_decode_json(self):
        """测试 JSON 解码"""
        json_str = '{"test": 123}'
        uri = json_to_data_uri(json_str)
        
        decoded = decode_data_uri(uri)
        
        self.assertEqual(decoded.decode_text(), json_str)
        self.assertTrue(decoded.is_text)
    
    def test_decode_invalid_uri(self):
        """测试无效 URI"""
        with self.assertRaises(ValueError):
            decode_data_uri('not a data uri')
        
        with self.assertRaises(ValueError):
            decode_data_uri('http://example.com')
    
    def test_decode_missing_data(self):
        """测试缺少数据的 URI"""
        with self.assertRaises(ValueError):
            decode_data_uri('data:text/plain;base64')


class TestFileOperations(unittest.TestCase):
    """文件操作测试"""
    
    def setUp(self):
        """创建临时目录和文件"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """清理临时文件"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_encode_file(self):
        """测试文件编码"""
        # 创建测试文件
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('Test content')
        
        uri = encode_file(test_file)
        
        self.assertTrue(uri.startswith('data:text/plain'))
        self.assertTrue(is_data_uri(uri))
    
    def test_encode_binary_file(self):
        """测试二进制文件编码"""
        test_file = os.path.join(self.temp_dir, 'test.bin')
        with open(test_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03\x04\x05')
        
        uri = encode_file(test_file)
        
        self.assertTrue(uri.startswith('data:application/octet-stream;base64,'))
    
    def test_encode_nonexistent_file(self):
        """测试编码不存在的文件"""
        with self.assertRaises(FileNotFoundError):
            encode_file('/nonexistent/file.txt')
    
    def test_decode_to_file(self):
        """测试解码到文件"""
        # 创建 Data URI
        original = b'Test content for file'
        uri = encode_data(original, 'text/plain', use_base64=True)
        
        # 解码到文件
        output_path = os.path.join(self.temp_dir, 'output.txt')
        result_path = decode_to_file(uri, output_path)
        
        # 验证
        with open(result_path, 'rb') as f:
            content = f.read()
        
        self.assertEqual(content, original)


class TestUtilityFunctions(unittest.TestCase):
    """工具函数测试"""
    
    def test_is_data_uri_valid(self):
        """测试有效 Data URI 检测"""
        uri = encode_data(b'test', 'text/plain', use_base64=True)
        self.assertTrue(is_data_uri(uri))
    
    def test_is_data_uri_invalid(self):
        """测试无效 Data URI 检测"""
        self.assertFalse(is_data_uri('not a data uri'))
        self.assertFalse(is_data_uri('http://example.com'))
        self.assertFalse(is_data_uri(''))
        self.assertFalse(is_data_uri(None))
    
    def test_get_info(self):
        """测试获取 Data URI 信息"""
        original = b'Hello World'
        uri = encode_data(original, 'text/plain', use_base64=True)
        
        info = get_info(uri)
        
        self.assertEqual(info['mime_type'], 'text/plain')
        self.assertEqual(info['encoding'], 'base64')
        self.assertEqual(info['original_size'], len(original))
        self.assertTrue(info['is_base64'])
        self.assertTrue(info['is_text'])
        self.assertEqual(info['extension'], '.txt')
    
    def test_estimate_size(self):
        """测试大小估算"""
        original_size = 1000
        
        # Base64 编码
        estimated_base64 = estimate_size(original_size, 'image/png', use_base64=True)
        
        # 实际编码后的 URI
        test_data = b'x' * original_size
        actual_uri = encode_data(test_data, 'image/png', use_base64=True)
        
        # 估算应该接近实际值（允许一定误差）
        self.assertLess(abs(estimated_base64 - len(actual_uri)), 50)


class TestBatchOperations(unittest.TestCase):
    """批量操作测试"""
    
    def setUp(self):
        """创建临时目录和文件"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """清理临时文件"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_batch_encode_success(self):
        """测试批量编码成功"""
        # 创建多个测试文件
        files = []
        for i in range(3):
            path = os.path.join(self.temp_dir, f'test{i}.txt')
            with open(path, 'w') as f:
                f.write(f'Content {i}')
            files.append(path)
        
        results = batch_encode(files)
        
        self.assertEqual(len(results['success']), 3)
        self.assertEqual(len(results['failed']), 0)
        self.assertEqual(len(results['skipped']), 0)
    
    def test_batch_encode_with_failures(self):
        """测试批量编码包含失败"""
        files = [
            os.path.join(self.temp_dir, 'exists.txt'),
            '/nonexistent/file.txt',
        ]
        
        # 创建存在的文件
        with open(files[0], 'w') as f:
            f.write('test')
        
        results = batch_encode(files)
        
        self.assertEqual(len(results['success']), 1)
        self.assertEqual(len(results['failed']), 1)
    
    def test_batch_encode_with_size_limit(self):
        """测试批量编码大小限制"""
        # 创建一个大文件
        large_file = os.path.join(self.temp_dir, 'large.txt')
        with open(large_file, 'wb') as f:
            f.write(b'x' * 1000)
        
        results = batch_encode([large_file], max_size=100)
        
        self.assertEqual(len(results['skipped']), 1)
        self.assertEqual(len(results['success']), 0)


class TestHTMLEmbed(unittest.TestCase):
    """HTML 嵌入测试"""
    
    def setUp(self):
        """创建临时目录和文件"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """清理临时文件"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_img_embed(self):
        """测试创建图片嵌入"""
        # 创建测试图片
        img_path = os.path.join(self.temp_dir, 'test.png')
        with open(img_path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n' + b'x' * 100)
        
        html = create_html_embed(img_path, alt_text='Test Image')
        
        self.assertIn('<img src="data:image/png;base64,', html)
        self.assertIn('alt="Test Image"', html)
    
    def test_create_audio_embed(self):
        """测试创建音频嵌入"""
        audio_path = os.path.join(self.temp_dir, 'test.mp3')
        with open(audio_path, 'wb') as f:
            f.write(b'ID3' + b'x' * 100)
        
        html = create_html_embed(audio_path, tag_type='audio')
        
        self.assertIn('<audio controls', html)
        self.assertIn('type="audio/mpeg"', html)
    
    def test_create_auto_embed(self):
        """测试自动推断标签类型"""
        # 图片
        img_path = os.path.join(self.temp_dir, 'auto.png')
        with open(img_path, 'wb') as f:
            f.write(b'\x89PNG')
        
        html = create_html_embed(img_path)
        self.assertIn('<img', html)


class TestDataURIClass(unittest.TestCase):
    """DataURI 类测试"""
    
    def test_datauri_properties(self):
        """测试 DataURI 属性"""
        data = b'Hello'
        uri = encode_data(data, 'text/plain', use_base64=True)
        parsed = decode_data_uri(uri)
        
        self.assertTrue(parsed.is_base64)
        self.assertTrue(parsed.is_text)
        self.assertEqual(parsed.original_size, 5)
    
    def test_datauri_repr(self):
        """测试 DataURI 表示"""
        uri = encode_data(b'test', 'application/json', use_base64=True)
        parsed = decode_data_uri(uri)
        
        repr_str = repr(parsed)
        
        self.assertIn('application/json', repr_str)
        self.assertIn('base64', repr_str)


if __name__ == '__main__':
    unittest.main(verbosity=2)