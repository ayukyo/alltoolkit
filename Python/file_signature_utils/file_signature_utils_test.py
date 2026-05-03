"""
文件签名/魔数检测工具测试

测试覆盖:
- 常见文件格式检测（图片、视频、音频、文档、压缩包）
- 扩展名验证
- MIME 类型检测
- 批量检测
- 类型判断函数
- 边界值处理
"""

import os
import sys
import tempfile
import unittest

# 添加父目录到路径以导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from file_signature_utils.mod import (
    FileType,
    detect_file_type,
    detect_extension,
    detect_mime_type,
    verify_extension,
    batch_detect,
    is_type,
    is_image,
    is_video,
    is_audio,
    is_document,
    is_archive,
    is_executable,
    get_supported_types,
    get_extension_mime_map,
    analyze_file,
)


class TestFileType(unittest.TestCase):
    """FileType 类测试"""
    
    def test_file_type_creation(self):
        """测试 FileType 创建"""
        ft = FileType('jpg', 'image/jpeg', 'JPEG Image')
        self.assertEqual(ft.extension, 'jpg')
        self.assertEqual(ft.mime_type, 'image/jpeg')
        self.assertEqual(ft.description, 'JPEG Image')
        self.assertEqual(ft.confidence, 1.0)
    
    def test_file_type_with_confidence(self):
        """测试带置信度的 FileType"""
        ft = FileType('json', 'application/json', 'JSON Data', confidence=0.8)
        self.assertEqual(ft.confidence, 0.8)
    
    def test_file_type_repr(self):
        """测试 FileType repr"""
        ft = FileType('png', 'image/png', 'PNG Image')
        repr_str = repr(ft)
        self.assertIn('png', repr_str)
        self.assertIn('image/png', repr_str)
    
    def test_file_type_equality(self):
        """测试 FileType 相等比较"""
        ft1 = FileType('jpg', 'image/jpeg', 'JPEG')
        ft2 = FileType('jpg', 'image/jpeg', 'JPEG Image')
        ft3 = FileType('png', 'image/png', 'PNG')
        self.assertEqual(ft1, ft2)
        self.assertNotEqual(ft1, ft3)
    
    def test_file_type_hash(self):
        """测试 FileType 哈希"""
        ft1 = FileType('jpg', 'image/jpeg', 'JPEG')
        ft2 = FileType('jpg', 'image/jpeg', 'JPEG Image')
        # 相同扩展名和 MIME 类型应该有相同哈希
        self.assertEqual(hash(ft1), hash(ft2))
        # 可以用在集合中
        s = {ft1, ft2}
        self.assertEqual(len(s), 1)
    
    def test_file_type_to_dict(self):
        """测试 FileType 转换为字典"""
        ft = FileType('gif', 'image/gif', 'GIF Image', confidence=0.9)
        d = ft.to_dict()
        self.assertEqual(d['extension'], 'gif')
        self.assertEqual(d['mime_type'], 'image/gif')
        self.assertEqual(d['description'], 'GIF Image')
        self.assertEqual(d['confidence'], 0.9)


class TestDetectImageFormats(unittest.TestCase):
    """图片格式检测测试"""
    
    def test_jpeg_detection(self):
        """测试 JPEG 检测"""
        # JPEG 起始字节
        jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF'
        ft = detect_file_type(jpeg_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'jpg')
        self.assertEqual(ft.mime_type, 'image/jpeg')
    
    def test_png_detection(self):
        """测试 PNG 检测"""
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
        ft = detect_file_type(png_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'png')
        self.assertEqual(ft.mime_type, 'image/png')
    
    def test_gif87a_detection(self):
        """测试 GIF87a 检测"""
        gif_data = b'GIF87a'
        ft = detect_file_type(gif_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'gif')
        self.assertEqual(ft.mime_type, 'image/gif')
    
    def test_gif89a_detection(self):
        """测试 GIF89a 检测"""
        gif_data = b'GIF89a'
        ft = detect_file_type(gif_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'gif')
        self.assertEqual(ft.mime_type, 'image/gif')
    
    def test_bmp_detection(self):
        """测试 BMP 检测"""
        bmp_data = b'BM\x36\x00\x00\x00'
        ft = detect_file_type(bmp_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'bmp')
        self.assertEqual(ft.mime_type, 'image/bmp')
    
    def test_tiff_little_endian_detection(self):
        """测试 TIFF 小端序检测"""
        tiff_data = b'II*\x00'
        ft = detect_file_type(tiff_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'tiff')
        self.assertEqual(ft.mime_type, 'image/tiff')
    
    def test_tiff_big_endian_detection(self):
        """测试 TIFF 大端序检测"""
        tiff_data = b'MM\x00*'
        ft = detect_file_type(tiff_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'tiff')
        self.assertEqual(ft.mime_type, 'image/tiff')
    
    def test_webp_detection(self):
        """测试 WebP 检测"""
        webp_data = b'RIFF\x00\x00\x00\x00WEBP'
        ft = detect_file_type(webp_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'webp')
        self.assertEqual(ft.mime_type, 'image/webp')
    
    def test_ico_detection(self):
        """测试 ICO 检测"""
        ico_data = b'\x00\x00\x01\x00\x01\x00'
        ft = detect_file_type(ico_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'ico')
        self.assertEqual(ft.mime_type, 'image/x-icon')
    
    def test_psd_detection(self):
        """测试 PSD 检测"""
        psd_data = b'8BPS\x00\x01'
        ft = detect_file_type(psd_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'psd')
        self.assertEqual(ft.mime_type, 'image/vnd.adobe.photoshop')


class TestDetectVideoFormats(unittest.TestCase):
    """视频格式检测测试"""
    
    def test_mp4_detection(self):
        """测试 MP4 检测"""
        # ftyp box at offset 4
        mp4_data = b'\x00\x00\x00\x20ftypisom'
        ft = detect_file_type(mp4_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'mp4')
        self.assertEqual(ft.mime_type, 'video/mp4')
    
    def test_mov_detection(self):
        """测试 MOV 检测"""
        mov_data = b'\x00\x00\x00\x14ftypqt  '
        ft = detect_file_type(mov_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'mov')
        self.assertEqual(ft.mime_type, 'video/quicktime')
    
    def test_avi_detection(self):
        """测试 AVI 检测"""
        avi_data = b'RIFF\x00\x00\x00\x00AVI '
        ft = detect_file_type(avi_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'avi')
        self.assertEqual(ft.mime_type, 'video/x-msvideo')
    
    def test_mkv_detection(self):
        """测试 MKV 检测"""
        mkv_data = b'\x1aE\xdf\xa3'
        ft = detect_file_type(mkv_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'mkv')
        self.assertEqual(ft.mime_type, 'video/x-matroska')
    
    def test_flv_detection(self):
        """测试 FLV 检测"""
        flv_data = b'FLV\x01\x00\x00\x00\x00'
        ft = detect_file_type(flv_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'flv')
        self.assertEqual(ft.mime_type, 'video/x-flv')
    
    def test_mpeg_detection(self):
        """测试 MPEG 检测"""
        mpeg_data = b'\x00\x00\x01\xba'
        ft = detect_file_type(mpeg_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'mpg')
        self.assertEqual(ft.mime_type, 'video/mpeg')


class TestDetectAudioFormats(unittest.TestCase):
    """音频格式检测测试"""
    
    def test_mp3_with_id3_detection(self):
        """测试带 ID3 标签的 MP3 检测"""
        mp3_data = b'ID3\x03\x00\x00\x00'
        ft = detect_file_type(mp3_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'mp3')
        self.assertEqual(ft.mime_type, 'audio/mpeg')
    
    def test_mp3_frame_detection(self):
        """测试 MP3 帧同步检测"""
        mp3_data = b'\xff\xfb\x90\x00'
        ft = detect_file_type(mp3_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'mp3')
        self.assertEqual(ft.mime_type, 'audio/mpeg')
    
    def test_flac_detection(self):
        """测试 FLAC 检测"""
        flac_data = b'fLaC\x00\x00\x00\x00'
        ft = detect_file_type(flac_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'flac')
        self.assertEqual(ft.mime_type, 'audio/flac')
    
    def test_ogg_detection(self):
        """测试 OGG 检测"""
        ogg_data = b'OggS\x00\x02\x00\x00'
        ft = detect_file_type(ogg_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'ogg')
        self.assertEqual(ft.mime_type, 'audio/ogg')
    
    def test_wav_detection(self):
        """测试 WAV 检测"""
        wav_data = b'RIFF\x00\x00\x00\x00WAVE'
        ft = detect_file_type(wav_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'wav')
        self.assertEqual(ft.mime_type, 'audio/wav')
    
    def test_midi_detection(self):
        """测试 MIDI 检测"""
        midi_data = b'MThd\x00\x00\x00\x06'
        ft = detect_file_type(midi_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'mid')
        self.assertEqual(ft.mime_type, 'audio/midi')


class TestDetectDocumentFormats(unittest.TestCase):
    """文档格式检测测试"""
    
    def test_pdf_detection(self):
        """测试 PDF 检测"""
        pdf_data = b'%PDF-1.4\n%'
        ft = detect_file_type(pdf_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'pdf')
        self.assertEqual(ft.mime_type, 'application/pdf')
    
    def test_xml_detection(self):
        """测试 XML 检测"""
        xml_data = b'<?xml version="1.0"?>'
        ft = detect_file_type(xml_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'xml')
        self.assertEqual(ft.mime_type, 'text/xml')
    
    def test_html_detection(self):
        """测试 HTML 检测"""
        html_data = b'<!DOCTYPE html><html>'
        ft = detect_file_type(html_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'html')
        self.assertEqual(ft.mime_type, 'text/html')
    
    def test_json_detection(self):
        """测试 JSON 检测"""
        json_data = b'{"name": "test"}'
        ft = detect_file_type(json_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'json')
        self.assertEqual(ft.mime_type, 'application/json')
    
    def test_json_array_detection(self):
        """测试 JSON 数组检测"""
        json_data = b'[1, 2, 3]'
        ft = detect_file_type(json_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'json')
        self.assertEqual(ft.mime_type, 'application/json')
    
    def test_office_ole_detection(self):
        """测试 Office OLE 格式检测"""
        ole_data = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
        ft = detect_file_type(ole_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'doc')
        self.assertEqual(ft.mime_type, 'application/msword')


class TestDetectArchiveFormats(unittest.TestCase):
    """压缩格式检测测试"""
    
    def test_zip_detection(self):
        """测试 ZIP 检测"""
        zip_data = b'PK\x03\x04\x00\x00\x00\x00'
        ft = detect_file_type(zip_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'zip')
        self.assertEqual(ft.mime_type, 'application/zip')
    
    def test_rar_detection(self):
        """测试 RAR 检测"""
        rar_data = b'Rar!\x1a\x07\x00\x00'
        ft = detect_file_type(rar_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'rar')
        self.assertEqual(ft.mime_type, 'application/x-rar-compressed')
    
    def test_gzip_detection(self):
        """测试 GZIP 检测"""
        gzip_data = b'\x1f\x8b\x08\x00\x00\x00'
        ft = detect_file_type(gzip_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'gz')
        self.assertEqual(ft.mime_type, 'application/gzip')
    
    def test_bz2_detection(self):
        """测试 BZIP2 检测"""
        bz2_data = b'BZh9\x00\x00\x00'
        ft = detect_file_type(bz2_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'bz2')
        self.assertEqual(ft.mime_type, 'application/x-bzip2')
    
    def test_xz_detection(self):
        """测试 XZ 检测"""
        xz_data = b'\xfd7zXZ\x00\x00\x00'
        ft = detect_file_type(xz_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'xz')
        self.assertEqual(ft.mime_type, 'application/x-xz')
    
    def test_7z_detection(self):
        """测试 7-Zip 检测"""
        seven_z_data = b'7z\xbc\xaf\x27\x1c'
        ft = detect_file_type(seven_z_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, '7z')
        self.assertEqual(ft.mime_type, 'application/x-7z-compressed')


class TestDetectExecutableFormats(unittest.TestCase):
    """可执行文件格式检测测试"""
    
    def test_windows_exe_detection(self):
        """测试 Windows EXE 检测"""
        # 简化的 MZ 头
        exe_data = b'MZ\x90\x00' + b'\x00' * 56 + b'\x00\x00\x00\x00'
        ft = detect_file_type(exe_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'exe')
        self.assertEqual(ft.mime_type, 'application/x-msdos-program')
    
    def test_elf_detection(self):
        """测试 ELF 检测"""
        elf_data = b'\x7fELF\x02\x01\x01\x00'
        ft = detect_file_type(elf_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'elf')
        self.assertEqual(ft.mime_type, 'application/x-elf')
    
    def test_java_class_detection(self):
        """测试 Java Class 检测"""
        class_data = b'\xca\xfe\xba\xbe\x00\x00\x00\x34'
        ft = detect_file_type(class_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'class')
        self.assertEqual(ft.mime_type, 'application/java-vm')


class TestDetectDatabaseFormats(unittest.TestCase):
    """数据库格式检测测试"""
    
    def test_sqlite_detection(self):
        """测试 SQLite 检测"""
        sqlite_data = b'SQLite format 3\x00'
        ft = detect_file_type(sqlite_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'sqlite')
        self.assertEqual(ft.mime_type, 'application/x-sqlite3')


class TestDetectFontFormats(unittest.TestCase):
    """字体格式检测测试"""
    
    def test_ttf_detection(self):
        """测试 TrueType 字体检测"""
        ttf_data = b'\x00\x01\x00\x00\x00\x01'
        ft = detect_file_type(ttf_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'ttf')
        self.assertEqual(ft.mime_type, 'font/ttf')
    
    def test_otf_detection(self):
        """测试 OpenType 字体检测"""
        otf_data = b'OTTO\x00\x01'
        ft = detect_file_type(otf_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'otf')
        self.assertEqual(ft.mime_type, 'font/otf')
    
    def test_woff_detection(self):
        """测试 WOFF 检测"""
        woff_data = b'wOFF\x00\x01\x00\x00'
        ft = detect_file_type(woff_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'woff')
        self.assertEqual(ft.mime_type, 'font/woff')
    
    def test_woff2_detection(self):
        """测试 WOFF2 检测"""
        woff2_data = b'wOF2\x00\x01\x00\x00'
        ft = detect_file_type(woff2_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'woff2')
        self.assertEqual(ft.mime_type, 'font/woff2')


class TestDetectCertificateFormats(unittest.TestCase):
    """证书格式检测测试"""
    
    def test_pem_detection(self):
        """测试 PEM 证书检测"""
        pem_data = b'-----BEGIN CERTIFICATE-----\n'
        ft = detect_file_type(pem_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'pem')
        self.assertEqual(ft.mime_type, 'application/x-pem-file')


class TestDetectScriptFormats(unittest.TestCase):
    """脚本格式检测测试"""
    
    def test_shell_script_detection(self):
        """测试 Shell 脚本检测"""
        sh_data = b'#!/bin/bash\necho hello'
        ft = detect_file_type(sh_data)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'sh')
        self.assertEqual(ft.mime_type, 'text/x-shellscript')


class TestHelperFunctions(unittest.TestCase):
    """辅助函数测试"""
    
    def test_detect_extension(self):
        """测试扩展名检测"""
        png_data = b'\x89PNG\r\n\x1a\n'
        ext = detect_extension(png_data)
        self.assertEqual(ext, 'png')
    
    def test_detect_mime_type(self):
        """测试 MIME 类型检测"""
        jpg_data = b'\xff\xd8\xff\xe0'
        mime = detect_mime_type(jpg_data)
        self.assertEqual(mime, 'image/jpeg')
    
    def test_detect_extension_unknown(self):
        """测试未知数据的扩展名检测"""
        unknown_data = b'\x00\x01\x02\x03\x04\x05'
        ext = detect_extension(unknown_data)
        self.assertIsNone(ext)
    
    def test_detect_mime_type_unknown(self):
        """测试未知数据的 MIME 类型检测"""
        unknown_data = b'\x00\x01\x02\x03\x04\x05'
        mime = detect_mime_type(unknown_data)
        self.assertIsNone(mime)


class TestVerifyExtension(unittest.TestCase):
    """扩展名验证测试"""
    
    def test_verify_matching_extension(self):
        """测试匹配的扩展名"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.flush()
            match, declared, actual = verify_extension(f.name)
            self.assertTrue(match)
            self.assertEqual(declared, 'png')
            self.assertEqual(actual, 'png')
            os.unlink(f.name)
    
    def test_verify_mismatched_extension(self):
        """测试不匹配的扩展名"""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.flush()
            match, declared, actual = verify_extension(f.name)
            self.assertFalse(match)
            self.assertEqual(declared, 'txt')
            self.assertEqual(actual, 'png')
            os.unlink(f.name)
    
    def test_verify_no_extension(self):
        """测试无扩展名的文件"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.flush()
            match, declared, actual = verify_extension(f.name)
            self.assertFalse(match)
            self.assertIsNone(declared)
            self.assertEqual(actual, 'png')
            os.unlink(f.name)


class TestBatchDetect(unittest.TestCase):
    """批量检测测试"""
    
    def test_batch_detect_multiple_files(self):
        """测试批量检测多个文件"""
        files = []
        # 创建临时测试文件
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f1:
            f1.write(b'\x89PNG\r\n\x1a\n')
            files.append(f1.name)
        
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f2:
            f2.write(b'\xff\xd8\xff\xe0')
            files.append(f2.name)
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f3:
            f3.write(b'%PDF-1.4\n')
            files.append(f3.name)
        
        try:
            results = batch_detect(files)
            self.assertEqual(len(results), 3)
            self.assertEqual(results[files[0]].extension, 'png')
            self.assertEqual(results[files[1]].extension, 'jpg')
            self.assertEqual(results[files[2]].extension, 'pdf')
        finally:
            for f in files:
                os.unlink(f)


class TestTypeCheckFunctions(unittest.TestCase):
    """类型检查函数测试"""
    
    def test_is_type(self):
        """测试 is_type 函数"""
        png_data = b'\x89PNG\r\n\x1a\n'
        self.assertTrue(is_type(png_data, 'png'))
        self.assertTrue(is_type(png_data, 'PNG'))  # 大小写不敏感
        self.assertFalse(is_type(png_data, 'jpg'))
    
    def test_is_image(self):
        """测试 is_image 函数"""
        self.assertTrue(is_image(b'\x89PNG\r\n\x1a\n'))
        self.assertTrue(is_image(b'\xff\xd8\xff\xe0'))
        self.assertTrue(is_image(b'GIF89a'))
        self.assertFalse(is_image(b'%PDF-1.4'))
    
    def test_is_video(self):
        """测试 is_video 函数"""
        mp4_data = b'\x00\x00\x00\x20ftypisom'
        self.assertTrue(is_video(mp4_data))
        self.assertTrue(is_video(b'\x1aE\xdf\xa3'))  # MKV
        self.assertFalse(is_video(b'\x89PNG\r\n\x1a\n'))
    
    def test_is_audio(self):
        """测试 is_audio 函数"""
        self.assertTrue(is_audio(b'ID3\x03\x00'))
        self.assertTrue(is_audio(b'fLaC\x00'))
        self.assertTrue(is_audio(b'OggS\x00'))
        self.assertFalse(is_audio(b'\x89PNG\r\n\x1a\n'))
    
    def test_is_document(self):
        """测试 is_document 函数"""
        self.assertTrue(is_document(b'%PDF-1.4'))
        self.assertTrue(is_document(b'<?xml version="1.0"?>'))
        self.assertFalse(is_document(b'\x89PNG\r\n\x1a\n'))
    
    def test_is_archive(self):
        """测试 is_archive 函数"""
        self.assertTrue(is_archive(b'PK\x03\x04'))
        self.assertTrue(is_archive(b'Rar!\x1a\x07'))
        self.assertTrue(is_archive(b'\x1f\x8b'))
        self.assertFalse(is_archive(b'\x89PNG\r\n\x1a\n'))
    
    def test_is_executable(self):
        """测试 is_executable 函数"""
        self.assertTrue(is_executable(b'\x7fELF'))
        self.assertTrue(is_executable(b'\xca\xfe\xba\xbe'))
        # MZ 需要 PE 签名检查
        self.assertFalse(is_executable(b'\x89PNG\r\n\x1a\n'))


class TestGetSupportedTypes(unittest.TestCase):
    """获取支持类型测试"""
    
    def test_get_supported_types(self):
        """测试获取支持的类型"""
        types = get_supported_types()
        self.assertIsInstance(types, dict)
        self.assertIn('images', types)
        self.assertIn('videos', types)
        self.assertIn('audio', types)
        self.assertIn('documents', types)
        self.assertIn('archives', types)
        self.assertIn('executables', types)
        self.assertIn('jpg', types['images'])
        self.assertIn('png', types['images'])
        self.assertIn('mp4', types['videos'])
    
    def test_get_extension_mime_map(self):
        """测试获取扩展名 MIME 映射"""
        mime_map = get_extension_mime_map()
        self.assertIsInstance(mime_map, dict)
        self.assertEqual(mime_map['jpg'], 'image/jpeg')
        self.assertEqual(mime_map['png'], 'image/png')
        self.assertEqual(mime_map['pdf'], 'application/pdf')


class TestAnalyzeFile(unittest.TestCase):
    """文件分析测试"""
    
    def test_analyze_image_file(self):
        """测试分析图片文件"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')
            f.flush()
            
            result = analyze_file(f.name)
            
            self.assertIsNotNone(result['file_type'])
            self.assertEqual(result['actual_extension'], 'png')
            self.assertEqual(result['declared_extension'], 'png')
            self.assertTrue(result['extension_match'])
            self.assertTrue(result['is_image'])
            self.assertFalse(result['is_video'])
            self.assertFalse(result['is_audio'])
            self.assertEqual(result['size'], 16)
            
            os.unlink(f.name)
    
    def test_analyze_fake_file(self):
        """测试分析伪装文件（扩展名与实际类型不符）"""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.flush()
            
            result = analyze_file(f.name)
            
            self.assertEqual(result['declared_extension'], 'txt')
            self.assertEqual(result['actual_extension'], 'png')
            self.assertFalse(result['extension_match'])
            self.assertTrue(result['is_image'])
            
            os.unlink(f.name)


class TestEdgeCases(unittest.TestCase):
    """边界值测试"""
    
    def test_empty_data(self):
        """测试空数据"""
        ft = detect_file_type(b'')
        self.assertIsNone(ft)
    
    def test_short_data(self):
        """测试非常短的数据"""
        ft = detect_file_type(b'\xff')
        self.assertIsNone(ft)
    
    def test_unknown_format(self):
        """测试未知格式"""
        unknown_data = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09'
        ft = detect_file_type(unknown_data)
        self.assertIsNone(ft)
    
    def test_file_not_found(self):
        """测试文件不存在"""
        ft = detect_file_type('/nonexistent/path/to/file.xyz')
        self.assertIsNone(ft)
    
    def test_unicode_filename(self):
        """测试 Unicode 文件名"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False, prefix='测试_') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.flush()
            
            ft = detect_file_type(f.name)
            self.assertIsNotNone(ft)
            self.assertEqual(ft.extension, 'png')
            
            os.unlink(f.name)
    
    def test_binary_garbage(self):
        """测试二进制垃圾数据"""
        garbage = bytes(range(256))
        ft = detect_file_type(garbage)
        # 可能匹配到某些签名，也可能不匹配
        # 这里只测试不会崩溃
        self.assertTrue(ft is None or isinstance(ft, FileType))
    
    def test_large_data(self):
        """测试大数据"""
        # 创建一个大的 PNG 数据
        large_png = b'\x89PNG\r\n\x1a\n' + b'\x00' * 10000
        ft = detect_file_type(large_png)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.extension, 'png')


class TestFileObjectInput(unittest.TestCase):
    """文件对象输入测试"""
    
    def test_file_object_input(self):
        """测试文件对象作为输入"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.flush()
            
            with open(f.name, 'rb') as fp:
                ft = detect_file_type(fp)
                self.assertIsNotNone(ft)
                self.assertEqual(ft.extension, 'png')
            
            os.unlink(f.name)
    
    def test_file_object_position_preserved(self):
        """测试文件对象位置保持不变"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'\x89PNG\r\n\x1a\n' + b'\x00' * 100)
            f.flush()
            
            with open(f.name, 'rb') as fp:
                fp.seek(10)
                pos_before = fp.tell()
                detect_file_type(fp)
                pos_after = fp.tell()
                self.assertEqual(pos_before, pos_after)
            
            os.unlink(f.name)


class TestConfidenceScores(unittest.TestCase):
    """置信度分数测试"""
    
    def test_binary_format_high_confidence(self):
        """测试二进制格式高置信度"""
        png_data = b'\x89PNG\r\n\x1a\n'
        ft = detect_file_type(png_data)
        self.assertEqual(ft.confidence, 1.0)
    
    def test_text_format_lower_confidence(self):
        """测试文本格式较低置信度"""
        json_data = b'{"key": "value"}'
        ft = detect_file_type(json_data)
        self.assertEqual(ft.confidence, 0.8)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestFileType,
        TestDetectImageFormats,
        TestDetectVideoFormats,
        TestDetectAudioFormats,
        TestDetectDocumentFormats,
        TestDetectArchiveFormats,
        TestDetectExecutableFormats,
        TestDetectDatabaseFormats,
        TestDetectFontFormats,
        TestDetectCertificateFormats,
        TestDetectScriptFormats,
        TestHelperFunctions,
        TestVerifyExtension,
        TestBatchDetect,
        TestTypeCheckFunctions,
        TestGetSupportedTypes,
        TestAnalyzeFile,
        TestEdgeCases,
        TestFileObjectInput,
        TestConfidenceScores,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    run_tests()