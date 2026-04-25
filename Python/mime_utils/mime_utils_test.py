"""
MIME 类型工具模块测试
==================

运行测试: python -m mime_utils_test
"""

import os
import sys
import tempfile
import unittest

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mime_utils.mod import (
    get_mime_type,
    get_extensions,
    get_primary_extension,
    detect_mime_from_content,
    detect_mime_from_file,
    is_image,
    is_video,
    is_audio,
    is_document,
    is_text,
    is_archive,
    is_code,
    is_executable,
    is_font,
    get_category,
    get_mime_info,
    parse_mime_type,
    build_mime_type,
    content_disposition,
    guess_type,
    guess_extension,
    MimeTypeDetector,
)


class TestGetMimeType(unittest.TestCase):
    """测试 get_mime_type 函数"""
    
    def test_with_dot(self):
        """测试带点的扩展名"""
        self.assertEqual(get_mime_type('.jpg'), 'image/jpeg')
        self.assertEqual(get_mime_type('.png'), 'image/png')
        self.assertEqual(get_mime_type('.pdf'), 'application/pdf')
    
    def test_without_dot(self):
        """测试不带点的扩展名"""
        self.assertEqual(get_mime_type('jpg'), 'image/jpeg')
        self.assertEqual(get_mime_type('png'), 'image/png')
        self.assertEqual(get_mime_type('mp4'), 'video/mp4')
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        self.assertEqual(get_mime_type('.JPG'), 'image/jpeg')
        self.assertEqual(get_mime_type('PNG'), 'image/png')
        self.assertEqual(get_mime_type('.Mp4'), 'video/mp4')
    
    def test_default(self):
        """测试默认值"""
        self.assertEqual(get_mime_type('.unknown'), 'application/octet-stream')
        self.assertEqual(get_mime_type('.unknown', 'text/plain'), 'text/plain')
    
    def test_all_known_types(self):
        """测试所有已知类型"""
        # 图片
        self.assertEqual(get_mime_type('.gif'), 'image/gif')
        self.assertEqual(get_mime_type('.webp'), 'image/webp')
        self.assertEqual(get_mime_type('.svg'), 'image/svg+xml')
        self.assertEqual(get_mime_type('.bmp'), 'image/bmp')
        
        # 视频
        self.assertEqual(get_mime_type('.avi'), 'video/x-msvideo')
        self.assertEqual(get_mime_type('.mov'), 'video/quicktime')
        self.assertEqual(get_mime_type('.webm'), 'video/webm')
        
        # 音频
        self.assertEqual(get_mime_type('.mp3'), 'audio/mpeg')
        self.assertEqual(get_mime_type('.wav'), 'audio/wav')
        self.assertEqual(get_mime_type('.flac'), 'audio/flac')
        
        # 文档
        self.assertEqual(get_mime_type('.doc'), 'application/msword')
        self.assertEqual(get_mime_type('.docx'), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        
        # 文本
        self.assertEqual(get_mime_type('.txt'), 'text/plain')
        self.assertEqual(get_mime_type('.html'), 'text/html')
        self.assertEqual(get_mime_type('.json'), 'application/json')
        
        # 压缩包
        self.assertEqual(get_mime_type('.zip'), 'application/zip')
        self.assertEqual(get_mime_type('.tar'), 'application/x-tar')
        self.assertEqual(get_mime_type('.gz'), 'application/gzip')


class TestGetExtensions(unittest.TestCase):
    """测试 get_extensions 函数"""
    
    def test_image_jpeg(self):
        """测试 JPEG 扩展名"""
        exts = get_extensions('image/jpeg')
        self.assertIn('.jpg', exts)
        self.assertIn('.jpeg', exts)
    
    def test_single_extension(self):
        """测试单一扩展名"""
        self.assertEqual(get_extensions('image/png'), ['.png'])
    
    def test_unknown_mime(self):
        """测试未知 MIME 类型"""
        self.assertEqual(get_extensions('unknown/type'), [])
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        exts = get_extensions('IMAGE/JPEG')
        self.assertIn('.jpg', exts)


class TestGetPrimaryExtension(unittest.TestCase):
    """测试 get_primary_extension 函数"""
    
    def test_known_mime(self):
        """测试已知 MIME 类型"""
        self.assertEqual(get_primary_extension('image/jpeg'), '.jpg')
        self.assertEqual(get_primary_extension('image/png'), '.png')
    
    def test_unknown_mime(self):
        """测试未知 MIME 类型"""
        self.assertEqual(get_primary_extension('unknown/type'), '.bin')
        self.assertEqual(get_primary_extension('unknown/type', '.txt'), '.txt')


class TestDetectMimeFromContent(unittest.TestCase):
    """测试 detect_mime_from_content 函数"""
    
    def test_jpeg(self):
        """测试 JPEG 检测"""
        data = b'\xff\xd8\xff\xe0\x00\x10JFIF'
        self.assertEqual(detect_mime_from_content(data), 'image/jpeg')
    
    def test_png(self):
        """测试 PNG 检测"""
        data = b'\x89PNG\r\n\x1a\n'
        self.assertEqual(detect_mime_from_content(data), 'image/png')
    
    def test_gif(self):
        """测试 GIF 检测"""
        data = b'GIF87a'
        self.assertEqual(detect_mime_from_content(data), 'image/gif')
        
        data = b'GIF89a'
        self.assertEqual(detect_mime_from_content(data), 'image/gif')
    
    def test_pdf(self):
        """测试 PDF 检测"""
        data = b'%PDF-1.4'
        self.assertEqual(detect_mime_from_content(data), 'application/pdf')
    
    def test_zip(self):
        """测试 ZIP 检测"""
        data = b'PK\x03\x04'
        self.assertEqual(detect_mime_from_content(data), 'application/zip')
    
    def test_gzip(self):
        """测试 GZIP 检测"""
        data = b'\x1f\x8b\x08'
        self.assertEqual(detect_mime_from_content(data), 'application/gzip')
    
    def test_mp3_with_id3(self):
        """测试 MP3 (带 ID3 标签) 检测"""
        data = b'ID3\x03\x00'
        self.assertEqual(detect_mime_from_content(data), 'audio/mpeg')
    
    def test_mp3_frame(self):
        """测试 MP3 帧同步检测"""
        data = b'\xff\xfb\x90\x00'
        self.assertEqual(detect_mime_from_content(data), 'audio/mpeg')
    
    def test_wav(self):
        """测试 WAV 检测"""
        data = b'RIFF\x00\x00\x00\x00WAVE'
        self.assertEqual(detect_mime_from_content(data), 'audio/wav')
    
    def test_avi(self):
        """测试 AVI 检测"""
        data = b'RIFF\x00\x00\x00\x00AVI '
        self.assertEqual(detect_mime_from_content(data), 'video/avi')
    
    def test_webp(self):
        """测试 WebP 检测"""
        data = b'RIFF\x00\x00\x00\x00WEBP'
        self.assertEqual(detect_mime_from_content(data), 'image/webp')
    
    def test_ogg(self):
        """测试 OGG 检测"""
        data = b'OggS\x00'
        self.assertEqual(detect_mime_from_content(data), 'audio/ogg')
    
    def test_flac(self):
        """测试 FLAC 检测"""
        data = b'fLaC\x00'
        self.assertEqual(detect_mime_from_content(data), 'audio/flac')
    
    def test_unknown(self):
        """测试未知类型"""
        data = b'unknown format'
        self.assertEqual(detect_mime_from_content(data), 'application/octet-stream')
        self.assertEqual(detect_mime_from_content(data, 'text/plain'), 'text/plain')
    
    def test_short_data(self):
        """测试过短数据"""
        self.assertEqual(detect_mime_from_content(b''), 'application/octet-stream')
        self.assertEqual(detect_mime_from_content(b'a'), 'application/octet-stream')


class TestDetectMimeFromFile(unittest.TestCase):
    """测试 detect_mime_from_file 函数"""
    
    def test_file_detection(self):
        """测试文件检测"""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF')
            f.flush()
            temp_path = f.name
        
        try:
            result = detect_mime_from_file(temp_path)
            self.assertEqual(result, 'image/jpeg')
        finally:
            os.unlink(temp_path)
    
    def test_nonexistent_file(self):
        """测试不存在文件"""
        result = detect_mime_from_file('/nonexistent/file.xyz')
        self.assertEqual(result, 'application/octet-stream')


class TestTypeChecks(unittest.TestCase):
    """测试类型判断函数"""
    
    def test_is_image(self):
        """测试图片判断"""
        self.assertTrue(is_image('image/jpeg'))
        self.assertTrue(is_image('image/png'))
        self.assertTrue(is_image('IMAGE/GIF'))  # 大小写不敏感
        self.assertFalse(is_image('video/mp4'))
        self.assertFalse(is_image('text/plain'))
    
    def test_is_video(self):
        """测试视频判断"""
        self.assertTrue(is_video('video/mp4'))
        self.assertTrue(is_video('video/webm'))
        self.assertFalse(is_video('image/jpeg'))
    
    def test_is_audio(self):
        """测试音频判断"""
        self.assertTrue(is_audio('audio/mpeg'))
        self.assertTrue(is_audio('audio/wav'))
        self.assertFalse(is_audio('video/mp4'))
    
    def test_is_document(self):
        """测试文档判断"""
        self.assertTrue(is_document('application/pdf'))
        self.assertTrue(is_document('application/msword'))
        self.assertFalse(is_document('image/jpeg'))
    
    def test_is_text(self):
        """测试文本判断"""
        self.assertTrue(is_text('text/plain'))
        self.assertTrue(is_text('text/html'))
        self.assertTrue(is_text('application/json'))
        self.assertFalse(is_text('image/jpeg'))
    
    def test_is_archive(self):
        """测试压缩包判断"""
        self.assertTrue(is_archive('application/zip'))
        self.assertTrue(is_archive('application/gzip'))
        self.assertFalse(is_archive('application/pdf'))
    
    def test_is_code(self):
        """测试代码判断"""
        self.assertTrue(is_code('text/x-python'))
        self.assertTrue(is_code('text/x-java-source'))
        self.assertFalse(is_code('text/plain'))
    
    def test_is_executable(self):
        """测试可执行文件判断"""
        self.assertTrue(is_executable('application/x-msdownload'))
        self.assertTrue(is_executable('application/x-sharedlib'))
        self.assertFalse(is_executable('application/pdf'))
    
    def test_is_font(self):
        """测试字体判断"""
        self.assertTrue(is_font('font/ttf'))
        self.assertTrue(is_font('font/woff'))
        self.assertFalse(is_font('application/pdf'))


class TestGetCategory(unittest.TestCase):
    """测试 get_category 函数"""
    
    def test_known_categories(self):
        """测试已知类别"""
        self.assertEqual(get_category('image/jpeg'), 'image')
        self.assertEqual(get_category('video/mp4'), 'video')
        self.assertEqual(get_category('audio/mpeg'), 'audio')
        self.assertEqual(get_category('application/pdf'), 'document')
        self.assertEqual(get_category('text/plain'), 'text')
        self.assertEqual(get_category('application/zip'), 'archive')
    
    def test_unknown_category(self):
        """测试未知类别"""
        self.assertIsNone(get_category('unknown/type'))
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        self.assertEqual(get_category('IMAGE/JPEG'), 'image')
        self.assertEqual(get_category('VIDEO/MP4'), 'video')


class TestGetMimeInfo(unittest.TestCase):
    """测试 get_mime_info 函数"""
    
    def test_image_jpeg(self):
        """测试 JPEG 信息"""
        info = get_mime_info('image/jpeg')
        self.assertEqual(info['mime_type'], 'image/jpeg')
        self.assertIn('.jpg', info['extensions'])
        self.assertEqual(info['primary_extension'], '.jpg')
        self.assertEqual(info['category'], 'image')
        self.assertTrue(info['is_image'])
        self.assertFalse(info['is_video'])
    
    def test_unknown_type(self):
        """测试未知类型"""
        info = get_mime_info('unknown/type')
        self.assertEqual(info['mime_type'], 'unknown/type')
        self.assertEqual(info['extensions'], [])
        self.assertEqual(info['primary_extension'], '.bin')
        self.assertIsNone(info['category'])


class TestParseMimeType(unittest.TestCase):
    """测试 parse_mime_type 函数"""
    
    def test_simple(self):
        """测试简单 MIME 类型"""
        mime, params = parse_mime_type('text/html')
        self.assertEqual(mime, 'text/html')
        self.assertEqual(params, {})
    
    def test_with_charset(self):
        """测试带字符集"""
        mime, params = parse_mime_type('text/html; charset=utf-8')
        self.assertEqual(mime, 'text/html')
        self.assertEqual(params, {'charset': 'utf-8'})
    
    def test_multiple_params(self):
        """测试多参数"""
        mime, params = parse_mime_type('text/html; charset=utf-8; lang=en')
        self.assertEqual(mime, 'text/html')
        self.assertEqual(params, {'charset': 'utf-8', 'lang': 'en'})
    
    def test_quoted_values(self):
        """测试引号值"""
        mime, params = parse_mime_type('text/html; charset="utf-8"')
        self.assertEqual(mime, 'text/html')
        self.assertEqual(params, {'charset': 'utf-8'})
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        mime, params = parse_mime_type('TEXT/HTML; CHARSET=UTF-8')
        self.assertEqual(mime, 'text/html')
        self.assertEqual(params, {'charset': 'UTF-8'})


class TestBuildMimeType(unittest.TestCase):
    """测试 build_mime_type 函数"""
    
    def test_no_params(self):
        """测试无参数"""
        self.assertEqual(build_mime_type('text/html'), 'text/html')
    
    def test_with_params(self):
        """测试带参数"""
        result = build_mime_type('text/html', {'charset': 'utf-8'})
        self.assertEqual(result, 'text/html; charset=utf-8')
    
    def test_multiple_params(self):
        """测试多参数"""
        result = build_mime_type('text/html', {'charset': 'utf-8', 'lang': 'en'})
        # 参数顺序不确定，所以检查包含
        self.assertIn('text/html;', result)
        self.assertIn('charset=utf-8', result)
        self.assertIn('lang=en', result)


class TestContentDisposition(unittest.TestCase):
    """测试 content_disposition 函数"""
    
    def test_attachment(self):
        """测试附件模式"""
        result = content_disposition('report.pdf')
        self.assertEqual(result, 'attachment; filename="report.pdf"')
    
    def test_inline(self):
        """测试内联模式"""
        result = content_disposition('image.png', inline=True)
        self.assertEqual(result, 'inline; filename="image.png"')
    
    def test_special_chars(self):
        """测试特殊字符"""
        result = content_disposition('file name.txt')
        self.assertIn('attachment;', result)
        self.assertIn('file name.txt', result)
    
    def test_unicode(self):
        """测试 Unicode 文件名"""
        result = content_disposition('中文文件.txt')
        self.assertIn('attachment;', result)
        self.assertIn('filename=', result)
        # RFC 5987 编码
        self.assertIn("filename*=", result)
    
    def test_quotes_escape(self):
        """测试引号转义"""
        result = content_disposition('file"test.txt')
        self.assertIn('\\"', result)


class TestGuessType(unittest.TestCase):
    """测试 guess_type 函数"""
    
    def test_filename(self):
        """测试文件名"""
        self.assertEqual(guess_type('document.pdf'), 'application/pdf')
        self.assertEqual(guess_type('image.jpg'), 'image/jpeg')
    
    def test_path(self):
        """测试路径"""
        self.assertEqual(guess_type('/path/to/file.png'), 'image/png')
        self.assertEqual(guess_type('C:\\Users\\test\\video.mp4'), 'video/mp4')
    
    def test_unknown(self):
        """测试未知类型"""
        self.assertEqual(guess_type('file.unknown'), 'application/octet-stream')
        self.assertEqual(guess_type('file.unknown', 'text/plain'), 'text/plain')


class TestGuessExtension(unittest.TestCase):
    """测试 guess_extension 函数"""
    
    def test_known(self):
        """测试已知类型"""
        self.assertEqual(guess_extension('image/jpeg'), '.jpg')
        self.assertEqual(guess_extension('image/png'), '.png')
    
    def test_unknown(self):
        """测试未知类型"""
        self.assertEqual(guess_extension('unknown/type'), '.bin')
        self.assertEqual(guess_extension('unknown/type', '.txt'), '.txt')


class TestMimeTypeDetector(unittest.TestCase):
    """测试 MimeTypeDetector 类"""
    
    def test_detect_jpeg(self):
        """测试 JPEG 检测"""
        detector = MimeTypeDetector()
        data = b'\xff\xd8\xff\xe0\x00\x10JFIF'
        self.assertEqual(detector.detect(data), 'image/jpeg')
    
    def test_detect_with_extension(self):
        """测试带扩展名检测"""
        detector = MimeTypeDetector()
        data = b'unknown format'
        result = detector.detect(data, extension='.pdf')
        self.assertEqual(result, 'application/pdf')
    
    def test_file_cache(self):
        """测试文件缓存"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.flush()
            temp_path = f.name
        
        try:
            detector = MimeTypeDetector()
            result1 = detector.detect_file(temp_path)
            self.assertEqual(result1, 'image/png')
            
            # 检查缓存
            self.assertIn(temp_path, detector._cache)
            
            # 清除缓存
            detector.clear_cache()
            self.assertNotIn(temp_path, detector._cache)
        finally:
            os.unlink(temp_path)


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(get_mime_type(''), 'application/octet-stream')
        self.assertEqual(get_extensions(''), [])
    
    def test_whitespace(self):
        """测试空白字符"""
        self.assertEqual(get_mime_type('  .jpg  '), 'application/octet-stream')
    
    def test_parse_malformed(self):
        """测试解析畸形 MIME 类型"""
        mime, params = parse_mime_type('text/html; =value')
        self.assertEqual(mime, 'text/html')
    
    def test_double_dots(self):
        """测试双点扩展名"""
        self.assertEqual(get_mime_type('..jpg'), 'application/octet-stream')


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)