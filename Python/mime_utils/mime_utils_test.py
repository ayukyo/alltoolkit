"""
MIME 工具模块测试

运行测试: python -m pytest mime_utils_test.py -v
或直接运行: python mime_utils_test.py
"""

import unittest
from mod import (
    get_mime_type, get_extension, get_extensions,
    is_category, get_category,
    is_image, is_video, is_audio, is_document, is_text,
    is_archive, is_code, is_binary,
    parse_content_type, build_content_type,
    build_content_disposition,
    guess_type_from_content,
    get_mime_info,
    MimeTypeRegistry,
)


class TestGetMimeType(unittest.TestCase):
    """测试 get_mime_type 函数"""
    
    def test_common_extensions(self):
        """测试常见扩展名"""
        self.assertEqual(get_mime_type('image.png'), 'image/png')
        self.assertEqual(get_mime_type('image.jpg'), 'image/jpeg')
        self.assertEqual(get_mime_type('image.jpeg'), 'image/jpeg')
        self.assertEqual(get_mime_type('document.pdf'), 'application/pdf')
        self.assertEqual(get_mime_type('video.mp4'), 'video/mp4')
        self.assertEqual(get_mime_type('audio.mp3'), 'audio/mpeg')
    
    def test_extension_with_dot(self):
        """测试带点的扩展名"""
        self.assertEqual(get_mime_type('.png'), 'image/png')
        self.assertEqual(get_mime_type('.jpg'), 'image/jpeg')
        self.assertEqual(get_mime_type('.json'), 'application/json')
    
    def test_extension_without_dot(self):
        """测试不带点的扩展名"""
        self.assertEqual(get_mime_type('png'), 'image/png')
        self.assertEqual(get_mime_type('json'), 'application/json')
    
    def test_extended_types(self):
        """测试扩展 MIME 类型"""
        self.assertEqual(get_mime_type('.md'), 'text/markdown')
        self.assertEqual(get_mime_type('.docx'), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        self.assertEqual(get_mime_type('.7z'), 'application/x-7z-compressed')
        self.assertEqual(get_mime_type('.m4a'), 'audio/mp4')
        self.assertEqual(get_mime_type('.woff2'), 'font/woff2')
    
    def test_unknown_extension(self):
        """测试未知扩展名"""
        self.assertEqual(get_mime_type('file.unknown'), 'application/octet-stream')
        self.assertEqual(get_mime_type('unknown'), 'application/octet-stream')
    
    def test_custom_default(self):
        """测试自定义默认值"""
        self.assertEqual(get_mime_type('file.unknown', default='custom/default'), 'custom/default')


class TestGetExtension(unittest.TestCase):
    """测试 get_extension 函数"""
    
    def test_common_types(self):
        """测试常见 MIME 类型"""
        self.assertEqual(get_extension('image/png'), '.png')
        self.assertEqual(get_extension('image/jpeg'), '.jpeg')
        self.assertEqual(get_extension('application/pdf'), '.pdf')
        self.assertEqual(get_extension('application/json'), '.json')
    
    def test_extended_types(self):
        """测试扩展 MIME 类型"""
        self.assertEqual(get_extension('text/markdown'), '.md')
        self.assertEqual(get_extension('font/woff2'), '.woff2')
    
    def test_unknown_type(self):
        """测试未知 MIME 类型"""
        self.assertEqual(get_extension('unknown/type'), '.bin')
    
    def test_custom_default(self):
        """测试自定义默认值"""
        self.assertEqual(get_extension('unknown/type', default='.unknown'), '.unknown')


class TestGetExtensions(unittest.TestCase):
    """测试 get_extensions 函数"""
    
    def test_multiple_extensions(self):
        """测试返回多个扩展名"""
        exts = get_extensions('image/jpeg')
        self.assertIn('.jpeg', exts)
        self.assertIn('.jpg', exts)
    
    def test_single_extension(self):
        """测试单一扩展名"""
        exts = get_extensions('image/png')
        self.assertIn('.png', exts)


class TestCategoryFunctions(unittest.TestCase):
    """测试类别判断函数"""
    
    def test_is_category(self):
        """测试 is_category 函数"""
        self.assertTrue(is_category('image/png', 'image'))
        self.assertTrue(is_category('video/mp4', 'video'))
        self.assertTrue(is_category('audio/mpeg', 'audio'))
        self.assertFalse(is_category('image/png', 'video'))
    
    def test_get_category(self):
        """测试 get_category 函数"""
        self.assertEqual(get_category('image/png'), 'image')
        self.assertEqual(get_category('video/mp4'), 'video')
        self.assertEqual(get_category('audio/mpeg'), 'audio')
        self.assertIsNone(get_category('unknown/type'))
    
    def test_convenience_functions(self):
        """测试便捷函数"""
        self.assertTrue(is_image('image/png'))
        self.assertFalse(is_image('video/mp4'))
        
        self.assertTrue(is_video('video/mp4'))
        self.assertFalse(is_video('image/png'))
        
        self.assertTrue(is_audio('audio/mpeg'))
        self.assertFalse(is_audio('video/mp4'))
        
        self.assertTrue(is_document('application/pdf'))
        self.assertTrue(is_text('text/plain'))
        self.assertTrue(is_archive('application/zip'))
        self.assertTrue(is_code('application/javascript'))
        self.assertTrue(is_binary('application/octet-stream'))


class TestContentTypeFunctions(unittest.TestCase):
    """测试 Content-Type 相关函数"""
    
    def test_parse_content_type_simple(self):
        """测试解析简单 Content-Type"""
        mime, params = parse_content_type('text/html')
        self.assertEqual(mime, 'text/html')
        self.assertEqual(params, {})
    
    def test_parse_content_type_with_charset(self):
        """测试解析带 charset 的 Content-Type"""
        mime, params = parse_content_type('text/html; charset=utf-8')
        self.assertEqual(mime, 'text/html')
        self.assertEqual(params, {'charset': 'utf-8'})
    
    def test_parse_content_type_multiple_params(self):
        """测试解析多参数 Content-Type"""
        mime, params = parse_content_type('multipart/form-data; boundary=----WebKitFormBoundary; charset=utf-8')
        self.assertEqual(mime, 'multipart/form-data')
        self.assertEqual(params['boundary'], '----WebKitFormBoundary')
        self.assertEqual(params['charset'], 'utf-8')
    
    def test_parse_content_type_quoted_values(self):
        """测试解析带引号的参数值"""
        mime, params = parse_content_type('text/html; charset="utf-8"')
        self.assertEqual(params['charset'], 'utf-8')
    
    def test_build_content_type_simple(self):
        """测试构建简单 Content-Type"""
        result = build_content_type('text/html')
        self.assertEqual(result, 'text/html')
    
    def test_build_content_type_with_charset(self):
        """测试构建带 charset 的 Content-Type"""
        result = build_content_type('text/html', charset='utf-8')
        self.assertEqual(result, 'text/html; charset=utf-8')
    
    def test_build_content_type_with_boundary(self):
        """测试构建带 boundary 的 Content-Type"""
        result = build_content_type('multipart/form-data', boundary='----WebKitFormBoundary')
        self.assertEqual(result, 'multipart/form-data; boundary=----WebKitFormBoundary')
    
    def test_build_content_type_with_params(self):
        """测试构建带额外参数的 Content-Type"""
        result = build_content_type('application/json', charset='utf-8', version='1.0')
        self.assertIn('charset=utf-8', result)
        self.assertIn('version=1.0', result)


class TestContentDisposition(unittest.TestCase):
    """测试 Content-Disposition 相关函数"""
    
    def test_attachment_simple(self):
        """测试简单附件"""
        result = build_content_disposition('report.pdf')
        self.assertIn('attachment', result)
        self.assertIn('filename', result)
    
    def test_inline(self):
        """测试内联显示"""
        result = build_content_disposition('image.png', disposition='inline')
        self.assertIn('inline', result)
    
    def test_chinese_filename(self):
        """测试中文文件名"""
        result = build_content_disposition('报告.pdf', encode_filename=True)
        self.assertIn('attachment', result)
        self.assertIn('filename*', result)  # RFC 5987 编码
    
    def test_no_encode(self):
        """测试不编码文件名"""
        result = build_content_disposition('report.pdf', encode_filename=False)
        self.assertIn('filename="report.pdf"', result)


class TestGuessTypeFromContent(unittest.TestCase):
    """测试根据内容猜测 MIME 类型"""
    
    def test_png_signature(self):
        """测试 PNG 签名"""
        content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
        self.assertEqual(guess_type_from_content(content), 'image/png')
    
    def test_jpeg_signature(self):
        """测试 JPEG 签名"""
        content = b'\xff\xd8\xff\xe0\x00\x10JFIF'
        self.assertEqual(guess_type_from_content(content), 'image/jpeg')
    
    def test_gif_signature(self):
        """测试 GIF 签名"""
        content = b'GIF89a\x00\x00\x00\x00'
        self.assertEqual(guess_type_from_content(content), 'image/gif')
    
    def test_pdf_signature(self):
        """测试 PDF 签名"""
        content = b'%PDF-1.4\n'
        self.assertEqual(guess_type_from_content(content), 'application/pdf')
    
    def test_zip_signature(self):
        """测试 ZIP 签名"""
        content = b'PK\x03\x04\x00\x00\x00\x00'
        self.assertEqual(guess_type_from_content(content), 'application/zip')
    
    def test_text_content(self):
        """测试文本内容"""
        content = b'Hello, World!'
        self.assertEqual(guess_type_from_content(content), 'text/plain')
    
    def test_empty_content(self):
        """测试空内容"""
        self.assertIsNone(guess_type_from_content(b''))


class TestGetMimeInfo(unittest.TestCase):
    """测试 get_mime_info 函数"""
    
    def test_image_info(self):
        """测试图片信息"""
        info = get_mime_info('image/png')
        self.assertEqual(info['mime_type'], 'image/png')
        self.assertEqual(info['category'], 'image')
        self.assertTrue(info['is_image'])
        self.assertFalse(info['is_video'])
        self.assertTrue(info['inline_displayable'])
    
    def test_video_info(self):
        """测试视频信息"""
        info = get_mime_info('video/mp4')
        self.assertEqual(info['category'], 'video')
        self.assertTrue(info['is_video'])
        self.assertFalse(info['inline_displayable'])
    
    def test_document_info(self):
        """测试文档信息"""
        info = get_mime_info('application/pdf')
        self.assertEqual(info['category'], 'document')
        self.assertTrue(info['is_document'])
        self.assertTrue(info['inline_displayable'])
    
    def test_unknown_type(self):
        """测试未知类型"""
        info = get_mime_info('application/x-unknown')
        self.assertEqual(info['mime_type'], 'application/x-unknown')
        self.assertIsNone(info['category'])


class TestMimeTypeRegistry(unittest.TestCase):
    """测试 MimeTypeRegistry 类"""
    
    def test_register_and_get(self):
        """测试注册和获取"""
        registry = MimeTypeRegistry()
        registry.register('.custom', 'application/x-custom')
        
        self.assertEqual(registry.get_mime_type('file.custom'), 'application/x-custom')
        self.assertEqual(registry.get_extension('application/x-custom'), '.custom')
    
    def test_unregister(self):
        """测试注销"""
        registry = MimeTypeRegistry()
        registry.register('.custom', 'application/x-custom')
        
        self.assertTrue(registry.unregister_extension('.custom'))
        self.assertEqual(registry.get_mime_type('file.custom'), 'application/octet-stream')
    
    def test_fallback_to_global(self):
        """测试回退到全局函数"""
        registry = MimeTypeRegistry()
        
        # 未注册的类型应回退到全局
        self.assertEqual(registry.get_mime_type('image.png'), 'image/png')
        self.assertEqual(registry.get_extension('image/png'), '.png')
    
    def test_list_all(self):
        """测试列出所有映射"""
        registry = MimeTypeRegistry()
        registry.register('.a', 'type/a')
        registry.register('.b', 'type/b')
        
        all_mappings = registry.list_all()
        self.assertEqual(all_mappings['.a'], 'type/a')
        self.assertEqual(all_mappings['.b'], 'type/b')


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        self.assertEqual(get_mime_type('IMAGE.PNG'), 'image/png')
        self.assertEqual(get_mime_type('.PNG'), 'image/png')
        self.assertEqual(get_extension('IMAGE/PNG'), '.png')
    
    def test_mime_type_with_params(self):
        """测试带参数的 MIME 类型"""
        self.assertEqual(get_category('image/png; charset=utf-8'), 'image')
        ext = get_extension('image/png; charset=utf-8')
        self.assertEqual(ext, '.png')
    
    def test_multiple_params_in_content_type(self):
        """测试多参数 Content-Type"""
        mime, params = parse_content_type('multipart/form-data; boundary=----ABC; charset=utf-8')
        self.assertEqual(mime, 'multipart/form-data')
        self.assertEqual(params['boundary'], '----ABC')
        self.assertEqual(params['charset'], 'utf-8')


if __name__ == '__main__':
    unittest.main(verbosity=2)