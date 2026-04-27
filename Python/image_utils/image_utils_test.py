"""
AllToolkit - Image Utilities 单元测试

测试 image_utils 模块的所有功能。

运行方式：
    python image_utils_test.py

依赖：
    - Pillow (推荐，用于完整测试)
    - 或仅使用标准库（有限测试）
"""

import os
import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# 导入被测试模块

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    ImageInfo,
    get_image_info,
    convert_format,
    resize_image,
    scale_image,
    crop_image,
    center_crop,
    rotate_image,
    flip_image,
    compress_image,
    generate_thumbnail,
    add_watermark,
    add_image_watermark,
    merge_images,
    create_grid,
    batch_resize,
    batch_convert,
    get_version,
    is_pillow_available,
    get_supported_formats,
)


class TestImageInfo(unittest.TestCase):
    """测试 ImageInfo 类。"""
    
    def test_create_image_info(self):
        """测试创建 ImageInfo 对象。"""
        info = ImageInfo(1920, 1080, 'PNG', 'RGB', 102400, True, 8)
        
        self.assertEqual(info.width, 1920)
        self.assertEqual(info.height, 1080)
        self.assertEqual(info.format, 'PNG')
        self.assertEqual(info.mode, 'RGB')
        self.assertEqual(info.file_size, 102400)
        self.assertTrue(info.has_alpha)
        self.assertEqual(info.bit_depth, 8)
    
    def test_image_info_repr(self):
        """测试 ImageInfo 的字符串表示。"""
        info = ImageInfo(800, 600, 'JPEG', 'RGB')
        repr_str = repr(info)
        
        self.assertIn('800x600', repr_str)
        self.assertIn('JPEG', repr_str)
    
    def test_image_info_to_dict(self):
        """测试 ImageInfo 转换为字典。"""
        info = ImageInfo(100, 200, 'GIF', 'P', 5000, False, 4)
        d = info.to_dict()
        
        self.assertIsInstance(d, dict)
        self.assertEqual(d['width'], 100)
        self.assertEqual(d['height'], 200)
        self.assertEqual(d['format'], 'GIF')
        self.assertEqual(d['mode'], 'P')
        self.assertEqual(d['file_size'], 5000)
        self.assertFalse(d['has_alpha'])
        self.assertEqual(d['bit_depth'], 4)


class TestGetImageInfo(unittest.TestCase):
    """测试 get_image_info 函数。"""
    
    def setUp(self):
        """创建测试临时目录。"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """清理临时目录。"""
        shutil.rmtree(self.temp_dir)
    
    def test_png_info(self):
        """测试 PNG 图像信息读取。"""
        # 创建简单的 PNG 数据（1x1 红色像素）
        png_data = (
            b'\x89PNG\r\n\x1a\n'
            b'\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02'
            b'\x00\x00\x00\x90wS\xde'
            b'\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N'
            b'\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        
        info = get_image_info(png_data)
        
        self.assertEqual(info.format, 'PNG')
        self.assertEqual(info.width, 1)
        self.assertEqual(info.height, 1)
    
    def test_jpeg_info(self):
        """测试 JPEG 图像信息读取。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库测试 JPEG")
        
        from PIL import Image
        import io
        
        # 使用 Pillow 创建 JPEG 测试
        img = Image.new('RGB', (10, 10), color='red')
        output = io.BytesIO()
        img.save(output, format='JPEG')
        jpeg_data = output.getvalue()
        
        info = get_image_info(jpeg_data)
        
        self.assertEqual(info.format, 'JPEG')
        self.assertEqual(info.width, 10)
        self.assertEqual(info.height, 10)
    
    def test_gif_info(self):
        """测试 GIF 图像信息读取。"""
        # 最小 GIF 数据
        gif_data = (
            b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!'
            b'\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00'
            b'\x02\x02D\x01\x00;'
        )
        
        info = get_image_info(gif_data)
        
        self.assertEqual(info.format, 'GIF')
        self.assertEqual(info.width, 1)
        self.assertEqual(info.height, 1)
    
    def test_bmp_info(self):
        """测试 BMP 图像信息读取。"""
        # 最小 BMP 数据（1x1 像素）
        bmp_data = (
            b'BM\x36\x00\x00\x00\x00\x00\x00\x00\x36\x00\x00\x00\x0c\x00\x00\x00'
            b'\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x13\x0b\x00\x00\x13\x0b\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\xff\xff\xff\x00'
        )
        
        info = get_image_info(bmp_data)
        
        self.assertEqual(info.format, 'BMP')
        self.assertEqual(info.width, 1)
        self.assertEqual(info.height, 1)
    
    def test_webp_info(self):
        """测试 WebP 图像信息读取。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库测试 WebP")
        
        # 使用 Pillow 创建 WebP 测试
        from PIL import Image
        import io
        
        img = Image.new('RGB', (100, 100), color='red')
        output = io.BytesIO()
        img.save(output, format='WEBP')
        webp_data = output.getvalue()
        
        info = get_image_info(webp_data)
        
        self.assertEqual(info.format, 'WebP')
        self.assertEqual(info.width, 100)
        self.assertEqual(info.height, 100)
    
    def test_file_path_input(self):
        """测试文件路径输入。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        
        # 创建测试图像
        test_path = os.path.join(self.temp_dir, 'test.png')
        img = Image.new('RGB', (50, 50), color='blue')
        img.save(test_path)
        
        info = get_image_info(test_path)
        
        self.assertEqual(info.width, 50)
        self.assertEqual(info.height, 50)
        self.assertEqual(info.format, 'PNG')
    
    def test_file_not_found(self):
        """测试文件不存在错误。"""
        with self.assertRaises(FileNotFoundError):
            get_image_info('/nonexistent/path/image.png')
    
    def test_invalid_format(self):
        """测试无效格式错误。"""
        with self.assertRaises(ValueError):
            get_image_info(b'not an image file')


class TestConvertFormat(unittest.TestCase):
    """测试格式转换功能。"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_png_to_jpeg(self):
        """测试 PNG 转 JPEG。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        # 创建 PNG 图像
        img = Image.new('RGB', (100, 100), color='green')
        png_data = io.BytesIO()
        img.save(png_data, format='PNG')
        
        # 转换为 JPEG
        output_path = os.path.join(self.temp_dir, 'output.jpg')
        result = convert_format(png_data.getvalue(), 'JPEG', output_path)
        
        self.assertIsNone(result)  # 保存到文件时返回 None
        self.assertTrue(os.path.exists(output_path))
        
        # 验证输出
        info = get_image_info(output_path)
        self.assertEqual(info.format, 'JPEG')
    
    def test_return_bytes(self):
        """测试返回 bytes。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (50, 50), color='red')
        png_data = io.BytesIO()
        img.save(png_data, format='PNG')
        
        # 转换为 WebP 并返回 bytes
        result = convert_format(png_data.getvalue(), 'WebP')
        
        self.assertIsInstance(result, bytes)
        self.assertGreater(len(result), 0)
    
    def test_invalid_format(self):
        """测试无效格式。"""
        with self.assertRaises(ValueError):
            convert_format(b'data', 'INVALID_FORMAT')
    
    def test_no_pillow(self):
        """测试无 Pillow 时的错误。"""
        # 临时禁用 Pillow
        import mod
        original = mod._PILLOW_AVAILABLE
        mod._PILLOW_AVAILABLE = False
        
        try:
            with self.assertRaises(RuntimeError):
                convert_format(b'data', 'PNG')
        finally:
            mod._PILLOW_AVAILABLE = original


class TestResizeImage(unittest.TestCase):
    """测试图像缩放功能。"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_resize_exact(self):
        """测试精确尺寸缩放。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (200, 100), color='blue')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        # 缩放到 100x50
        result = resize_image(img_data.getvalue(), 100, 50)
        
        info = get_image_info(result)
        self.assertEqual(info.width, 100)
        self.assertEqual(info.height, 50)
    
    def test_resize_maintain_aspect(self):
        """测试保持宽高比缩放。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (200, 100), color='yellow')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        # 缩放到 100x100 但保持宽高比
        result = resize_image(img_data.getvalue(), 100, 100, maintain_aspect=True)
        
        info = get_image_info(result)
        # 应该保持 2:1 比例，所以是 100x50
        self.assertEqual(info.width, 100)
        self.assertLessEqual(info.height, 100)


class TestScaleImage(unittest.TestCase):
    """测试比例缩放功能。"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_scale_down(self):
        """测试缩小。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (200, 100), color='cyan')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        # 缩小到 50%
        result = scale_image(img_data.getvalue(), 0.5)
        
        info = get_image_info(result)
        self.assertEqual(info.width, 100)
        self.assertEqual(info.height, 50)
    
    def test_scale_up(self):
        """测试放大。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (100, 50), color='magenta')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        # 放大到 200%
        result = scale_image(img_data.getvalue(), 2.0)
        
        info = get_image_info(result)
        self.assertEqual(info.width, 200)
        self.assertEqual(info.height, 100)
    
    def test_invalid_scale_factor(self):
        """测试无效缩放因子。"""
        with self.assertRaises(ValueError):
            scale_image(b'data', 0)
        
        with self.assertRaises(ValueError):
            scale_image(b'data', -1)


class TestCropImage(unittest.TestCase):
    """测试裁剪功能。"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_crop_region(self):
        """测试区域裁剪。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (100, 100), color='white')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        # 裁剪左上角 50x50
        result = crop_image(img_data.getvalue(), (0, 0, 50, 50))
        
        info = get_image_info(result)
        self.assertEqual(info.width, 50)
        self.assertEqual(info.height, 50)
    
    def test_center_crop(self):
        """测试中心裁剪。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (100, 100), color='gray')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        # 中心裁剪 60x60
        result = center_crop(img_data.getvalue(), 60, 60)
        
        info = get_image_info(result)
        self.assertEqual(info.width, 60)
        self.assertEqual(info.height, 60)
    
    def test_invalid_crop_box(self):
        """测试无效裁剪区域。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (50, 50), color='black')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        with self.assertRaises(ValueError):
            crop_image(img_data.getvalue(), (0, 0, 100, 100))  # 超出边界


class TestRotateImage(unittest.TestCase):
    """测试旋转功能。"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_rotate_90(self):
        """测试旋转 90 度。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (100, 50), color='red')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        # 旋转 90 度
        result = rotate_image(img_data.getvalue(), 90)
        
        info = get_image_info(result)
        # 旋转后宽高交换
        self.assertEqual(info.width, 50)
        self.assertEqual(info.height, 100)
    
    def test_rotate_45_expand(self):
        """测试旋转 45 度并扩展。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (100, 100), color='blue')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        # 旋转 45 度并扩展
        result = rotate_image(img_data.getvalue(), 45, expand=True)
        
        info = get_image_info(result)
        # 扩展后尺寸应该更大
        self.assertGreater(info.width, 100)
        self.assertGreater(info.height, 100)


class TestFlipImage(unittest.TestCase):
    """测试翻转功能。"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_flip_vertical(self):
        """测试垂直翻转。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (50, 50), color='green')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        result = flip_image(img_data.getvalue(), 'vertical')
        
        info = get_image_info(result)
        self.assertEqual(info.width, 50)
        self.assertEqual(info.height, 50)
    
    def test_flip_horizontal(self):
        """测试水平翻转。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (50, 50), color='yellow')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        result = flip_image(img_data.getvalue(), 'horizontal')
        
        info = get_image_info(result)
        self.assertEqual(info.width, 50)
        self.assertEqual(info.height, 50)
    
    def test_flip_invalid_direction(self):
        """测试无效翻转方向。"""
        with self.assertRaises(ValueError):
            flip_image(b'data', 'diagonal')


class TestCompressImage(unittest.TestCase):
    """测试压缩功能。"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_compress_quality(self):
        """测试质量压缩。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (200, 200), color='purple')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        original_size = len(img_data.getvalue())
        
        # 压缩为 JPEG
        result = compress_image(img_data.getvalue(), quality=50)
        
        self.assertIsInstance(result, bytes)
        # 通常压缩后会更小（但不保证，取决于图像内容）
    
    def test_compress_max_size(self):
        """测试最大大小限制。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (500, 500), color='orange')
        img_data = io.BytesIO()
        img.save(img_data, format='JPEG', quality=95)
        
        # 压缩到 10KB
        result = compress_image(img_data.getvalue(), max_size=10000)
        
        # 验证大小
        self.assertLessEqual(len(result), 10000)


class TestGenerateThumbnail(unittest.TestCase):
    """测试缩略图生成功能。"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_generate_thumbnail(self):
        """测试生成缩略图。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (800, 600), color='teal')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        # 生成 100x100 缩略图
        result = generate_thumbnail(img_data.getvalue(), (100, 100))
        
        info = get_image_info(result)
        self.assertLessEqual(info.width, 100)
        self.assertLessEqual(info.height, 100)
    
    def test_thumbnail_maintain_aspect(self):
        """测试缩略图保持宽高比。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (400, 200), color='navy')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        # 生成 100x100 缩略图，保持宽高比
        result = generate_thumbnail(img_data.getvalue(), (100, 100), maintain_aspect=True)
        
        info = get_image_info(result)
        # 应该保持 2:1 比例
        self.assertEqual(info.width / info.height, 2.0)


class TestAddWatermark(unittest.TestCase):
    """测试水印添加功能。"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_add_text_watermark(self):
        """测试添加文字水印。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (200, 200), color='white')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        # 添加水印
        result = add_watermark(img_data.getvalue(), '© Test')
        
        self.assertIsInstance(result, bytes)
        self.assertGreater(len(result), 0)
    
    def test_watermark_positions(self):
        """测试不同位置的水印。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (200, 200), color='white')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        positions = ['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center']
        
        for pos in positions:
            result = add_watermark(img_data.getvalue(), 'Test', position=pos)
            self.assertIsInstance(result, bytes)


class TestMergeImages(unittest.TestCase):
    """测试图像合并功能。"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_merge_horizontal(self):
        """测试水平合并。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        # 创建测试图像
        img1 = Image.new('RGB', (100, 50), color='red')
        img2 = Image.new('RGB', (100, 50), color='blue')
        
        data1 = io.BytesIO()
        data2 = io.BytesIO()
        img1.save(data1, format='PNG')
        img2.save(data2, format='PNG')
        
        # 水平合并
        result = merge_images([data1.getvalue(), data2.getvalue()], 'horizontal')
        
        info = get_image_info(result)
        self.assertEqual(info.width, 200)  # 100 + 100
        self.assertEqual(info.height, 50)
    
    def test_merge_vertical(self):
        """测试垂直合并。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img1 = Image.new('RGB', (50, 100), color='green')
        img2 = Image.new('RGB', (50, 100), color='yellow')
        
        data1 = io.BytesIO()
        data2 = io.BytesIO()
        img1.save(data1, format='PNG')
        img2.save(data2, format='PNG')
        
        # 垂直合并
        result = merge_images([data1.getvalue(), data2.getvalue()], 'vertical')
        
        info = get_image_info(result)
        self.assertEqual(info.width, 50)
        self.assertEqual(info.height, 200)  # 100 + 100
    
    def test_merge_with_gap(self):
        """测试带间距合并。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img1 = Image.new('RGB', (50, 50), color='cyan')
        img2 = Image.new('RGB', (50, 50), color='magenta')
        
        data1 = io.BytesIO()
        data2 = io.BytesIO()
        img1.save(data1, format='PNG')
        img2.save(data2, format='PNG')
        
        # 带 10 像素间距合并
        result = merge_images([data1.getvalue(), data2.getvalue()], 'horizontal', gap=10)
        
        info = get_image_info(result)
        self.assertEqual(info.width, 110)  # 50 + 10 + 50
    
    def test_merge_empty_list(self):
        """测试空列表合并。"""
        with self.assertRaises(ValueError):
            merge_images([])


class TestCreateGrid(unittest.TestCase):
    """测试网格创建功能。"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_create_2x2_grid(self):
        """测试创建 2x2 网格。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        # 创建 4 张测试图像
        images = []
        colors = ['red', 'green', 'blue', 'yellow']
        for color in colors:
            img = Image.new('RGB', (50, 50), color=color)
            data = io.BytesIO()
            img.save(data, format='PNG')
            images.append(data.getvalue())
        
        # 创建 2x2 网格
        result = create_grid(images, cols=2)
        
        info = get_image_info(result)
        # 2 列 x 50 像素 = 100 像素宽
        self.assertEqual(info.width, 100)
        # 2 行 x 50 像素 = 100 像素高
        self.assertEqual(info.height, 100)


class TestBatchOperations(unittest.TestCase):
    """测试批量操作功能。"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.input_dir = os.path.join(self.temp_dir, 'input')
        self.output_dir = os.path.join(self.temp_dir, 'output')
        os.makedirs(self.input_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_batch_resize(self):
        """测试批量缩放。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        
        # 创建测试图像
        for i in range(3):
            img = Image.new('RGB', (200, 200), color='white')
            img.save(os.path.join(self.input_dir, f'test{i}.jpg'))
        
        # 批量缩放
        result = batch_resize(self.input_dir, self.output_dir, 100, 100)
        
        self.assertEqual(result['processed'], 3)
        self.assertEqual(result['failed'], 0)
        
        # 验证输出
        for i in range(3):
            output_path = os.path.join(self.output_dir, f'test{i}.jpg')
            self.assertTrue(os.path.exists(output_path))
            info = get_image_info(output_path)
            self.assertEqual(info.width, 100)
            self.assertEqual(info.height, 100)
    
    def test_batch_convert(self):
        """测试批量转换。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        
        # 创建测试图像
        for i in range(2):
            img = Image.new('RGB', (100, 100), color='blue')
            img.save(os.path.join(self.input_dir, f'img{i}.png'))
        
        # 批量转换为 JPEG
        result = batch_convert(self.input_dir, self.output_dir, 'jpg')
        
        self.assertEqual(result['processed'], 2)
        self.assertEqual(result['failed'], 0)
        
        # 验证输出
        for i in range(2):
            output_path = os.path.join(self.output_dir, f'img{i}.jpg')
            self.assertTrue(os.path.exists(output_path))
            info = get_image_info(output_path)
            self.assertEqual(info.format, 'JPEG')


class TestModuleInfo(unittest.TestCase):
    """测试模块信息函数。"""
    
    def test_get_version(self):
        """测试获取版本号。"""
        version = get_version()
        self.assertIsInstance(version, str)
        self.assertRegex(version, r'^\d+\.\d+\.\d+$')
    
    def test_is_pillow_available(self):
        """测试 Pillow 可用性检测。"""
        available = is_pillow_available()
        self.assertIsInstance(available, bool)
    
    def test_get_supported_formats(self):
        """测试获取支持的格式列表。"""
        formats = get_supported_formats()
        self.assertIsInstance(formats, list)
        self.assertGreater(len(formats), 0)
        
        # 应该包含基本格式
        basic_formats = ['PNG', 'JPEG', 'GIF', 'BMP']
        for fmt in basic_formats:
            self.assertIn(fmt, formats)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况。"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_very_small_image(self):
        """测试极小图像。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (1, 1), color='red')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        # 应该能正常处理
        info = get_image_info(img_data.getvalue())
        self.assertEqual(info.width, 1)
        self.assertEqual(info.height, 1)
    
    def test_large_image(self):
        """测试大图像。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGB', (4000, 3000), color='white')
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        info = get_image_info(img_data.getvalue())
        self.assertEqual(info.width, 4000)
        self.assertEqual(info.height, 3000)
    
    def test_rgba_image(self):
        """测试 RGBA 图像。"""
        if not is_pillow_available():
            self.skipTest("需要 Pillow 库")
        
        from PIL import Image
        import io
        
        img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        
        info = get_image_info(img_data.getvalue())
        self.assertTrue(info.has_alpha)


def run_tests():
    """运行所有测试。"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestImageInfo,
        TestGetImageInfo,
        TestConvertFormat,
        TestResizeImage,
        TestScaleImage,
        TestCropImage,
        TestRotateImage,
        TestFlipImage,
        TestCompressImage,
        TestGenerateThumbnail,
        TestAddWatermark,
        TestMergeImages,
        TestCreateGrid,
        TestBatchOperations,
        TestModuleInfo,
        TestEdgeCases,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 打印摘要
    print("\n" + "=" * 60)
    print("测试摘要")
    print("=" * 60)
    print(f"运行测试数：{result.testsRun}")
    print(f"成功：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败：{len(result.failures)}")
    print(f"错误：{len(result.errors)}")
    print(f"跳过：{len(result.skipped)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n出错的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Image Utilities 单元测试")
    print("=" * 60)
    print(f"Pillow 可用：{is_pillow_available()}")
    print(f"支持的格式：{', '.join(get_supported_formats())}")
    print("=" * 60)
    print()
    
    success = run_tests()
    sys.exit(0 if success else 1)
