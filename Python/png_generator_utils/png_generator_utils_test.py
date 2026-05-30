# -*- coding: utf-8 -*-
"""
PNG Generator Utils - 测试用例
"""

import unittest
import os
import struct
import zlib
from io import BytesIO
from mod import (
    PNGCanvas,
    create_canvas,
    solid_png,
    bar_chart_png,
    PNG_SIGNATURE,
    COLOR_RGB,
    COLOR_RGB_ALPHA,
    _chunk,
    _paeth_predictor,
    _filter_row,
)


class TestPaethPredictor(unittest.TestCase):
    def test_paeth_basic(self):
        # a=10, b=20, c=5 → p=10+20-5=25
        # pa=15, pb=5, pc=20 → min is pb=5 → return b=20
        self.assertEqual(_paeth_predictor(10, 20, 5), 20)
    
    def test_paeth_equal(self):
        # when all equal, should return a
        self.assertEqual(_paeth_predictor(5, 5, 5), 5)
    
    def test_paeth_a_smallest(self):
        # when a is smallest, return a
        self.assertEqual(_paeth_predictor(1, 10, 10), 1)


class TestChunk(unittest.TestCase):
    def test_chunk_format(self):
        data = b'test'
        chunk = _chunk(b'IHDR', data)
        length = struct.unpack('>I', chunk[0:4])[0]
        chunk_type = chunk[4:8]
        chunk_data = chunk[8:-4]
        crc = struct.unpack('>I', chunk[-4:])[0]
        
        self.assertEqual(length, 4)
        self.assertEqual(chunk_type, b'IHDR')
        self.assertEqual(chunk_data, data)
        self.assertEqual(crc, zlib.crc32(b'IHDR' + data) & 0xffffffff)


class TestFilterRow(unittest.TestCase):
    def test_filter_none(self):
        row = b'\x01\x02\x03'
        result = _filter_row(row, b'', 0)
        self.assertEqual(result, b'\x00\x01\x02\x03')
    
    def test_filter_sub(self):
        row = bytes([10, 20, 30])
        result = _filter_row(row, b'', 1)
        self.assertEqual(result[0], 1)  # filter type
        self.assertEqual(result[1], 10)       # 10 - 0
        self.assertEqual(result[2], (20 - 10) & 0xff)  # 20 - left(10)
        self.assertEqual(result[3], (30 - 20) & 0xff)  # 30 - left(20)


class TestPNGCanvas(unittest.TestCase):
    def setUp(self):
        self.canvas = PNGCanvas(100, 100, (255, 255, 255))

    def test_init_invalid_size(self):
        with self.assertRaises(ValueError):
            PNGCanvas(0, 10)
        with self.assertRaises(ValueError):
            PNGCanvas(10, -1)

    def test_init_rgb(self):
        c = PNGCanvas(10, 10, (200, 100, 50), alpha=False)
        self.assertEqual(c.color_type, COLOR_RGB)
        self.assertEqual(c.pixels[0][0], [200, 100, 50])

    def test_init_rgba(self):
        c = PNGCanvas(10, 10, (200, 100, 50, 128), alpha=True)
        self.assertEqual(c.color_type, COLOR_RGB_ALPHA)
        self.assertEqual(c.pixels[0][0], [200, 100, 50, 128])

    def test_set_pixel(self):
        self.canvas.set_pixel(5, 5, (255, 0, 0))
        self.assertEqual(self.canvas.pixels[5][5], [255, 0, 0])

    def test_set_pixel_out_of_bounds(self):
        # Should not raise
        self.canvas.set_pixel(999, 999, (255, 0, 0))
        self.canvas.set_pixel(-1, -1, (255, 0, 0))

    def test_draw_point(self):
        self.canvas.draw_point(10, 10, (0, 255, 0))
        self.assertEqual(self.canvas.pixels[10][10], [0, 255, 0])

    def test_draw_line(self):
        self.canvas.draw_line(0, 0, 10, 10, (0, 0, 255))
        # Just verify it doesn't crash and pixels are set
        self.assertEqual(self.canvas.pixels[0][0], [0, 0, 255])

    def test_draw_rect_outline(self):
        self.canvas.draw_rect(5, 5, 10, 10, (255, 0, 0), fill=False)
        self.assertEqual(self.canvas.pixels[5][5], [255, 0, 0])   # top-left
        self.assertEqual(self.canvas.pixels[5][14], [255, 0, 0])  # top-right
        self.assertEqual(self.canvas.pixels[14][5], [255, 0, 0])  # bottom-left

    def test_draw_rect_filled(self):
        self.canvas.draw_rect(5, 5, 3, 3, (0, 255, 0), fill=True)
        for ry in range(5, 8):
            for rx in range(5, 8):
                self.assertEqual(self.canvas.pixels[ry][rx], [0, 255, 0])

    def test_draw_circle(self):
        self.canvas.draw_circle(50, 50, 5, (255, 0, 0))
        self.assertEqual(self.canvas.pixels[50][45], [255, 0, 0])  # left point of circle

    def test_draw_triangle(self):
        self.canvas.draw_triangle(10, 5, 20, 5, 15, 20, (100, 150, 200))
        # Centroid area should be filled
        cx = (10 + 20 + 15) // 3
        cy = (5 + 5 + 20) // 3
        self.assertEqual(self.canvas.pixels[cy][cx], [100, 150, 200])

    def test_draw_ellipse(self):
        self.canvas.draw_ellipse(50, 50, 10, 5, (0, 200, 0))
        self.assertEqual(self.canvas.pixels[50][40], [0, 200, 0])  # leftmost point

    def test_fill_gradient_linear(self):
        self.canvas.fill_gradient_linear(0, 0, 100, 100,
                                          (255, 0, 0), (0, 0, 255), angle=0.0)
        # Should not raise
        self.assertEqual(len(self.canvas.pixels), 100)

    def test_fill_gradient_radial(self):
        self.canvas.fill_gradient_radial(50, 50, 40, (255, 255, 255), (0, 0, 0))
        # Center pixel should be close to center color
        self.assertEqual(self.canvas.pixels[50][50], [255, 255, 255])
        # Edge should be closer to edge color
        corner_x = 50 + 40
        corner_y = 50 + 40
        self.assertEqual(self.canvas.pixels[corner_y][corner_x], [0, 0, 0])

    def test_draw_char(self):
        self.canvas.draw_char(0, 0, 'A', (0, 0, 0), scale=1)
        # 'A' bitmap row 0: 0b01110 → col 1 (leftmost bit set)
        # bit at col 1 is set → pixel should be dark
        self.assertEqual(self.canvas.pixels[0][1], [0, 0, 0])
        # col 0 is background white
        self.assertEqual(self.canvas.pixels[0][0], [255, 255, 255])

    def test_draw_text(self):
        self.canvas.draw_text(0, 0, "HI", (0, 0, 0), scale=1)
        self.assertEqual(self.canvas.pixels[0][0], [0, 0, 0])

    def test_encode_png_signature(self):
        data = self.canvas.encode()
        self.assertTrue(data.startswith(PNG_SIGNATURE))


class TestPNGEncode(unittest.TestCase):
    def test_encode_basic(self):
        c = PNGCanvas(2, 2, (255, 255, 255))
        data = c.encode()
        self.assertTrue(data.startswith(PNG_SIGNATURE))
        self.assertIn(b'IHDR', data)
        self.assertIn(b'IDAT', data)
        self.assertIn(b'IEND', data)

    def test_encode_rgba(self):
        c = PNGCanvas(2, 2, (255, 0, 0, 128), alpha=True)
        data = c.encode()
        self.assertTrue(data.startswith(PNG_SIGNATURE))

    def test_save_to_bytesio(self):
        c = PNGCanvas(50, 50, (100, 150, 200))
        buf = BytesIO()
        buf.write(c.encode())
        buf.seek(0)
        # 验证可读取
        data = buf.read()
        self.assertTrue(data.startswith(PNG_SIGNATURE))

    def test_draw_and_encode(self):
        c = PNGCanvas(200, 100, (240, 240, 240))
        c.draw_rect(10, 10, 50, 30, (70, 130, 180), fill=True)
        c.draw_line(10, 10, 60, 40, (255, 0, 0))
        c.draw_circle(150, 50, 20, (0, 200, 0))
        data = c.encode()
        self.assertTrue(data.startswith(PNG_SIGNATURE))
        self.assertGreater(len(data), 100)


class TestBarChartPNG(unittest.TestCase):
    def test_bar_chart_basic(self):
        data = [10, 20, 30]
        labels = ["A", "B", "C"]
        result = bar_chart_png(data, labels=labels)
        self.assertTrue(result.startswith(PNG_SIGNATURE))

    def test_bar_chart_empty_data(self):
        result = bar_chart_png([])
        self.assertTrue(result.startswith(PNG_SIGNATURE))


class TestSolidPNG(unittest.TestCase):
    def test_solid_png(self):
        result = solid_png(100, 100, (255, 0, 0))
        self.assertTrue(result.startswith(PNG_SIGNATURE))


class TestCreateCanvas(unittest.TestCase):
    def test_create_canvas(self):
        c = create_canvas(50, 50, (0, 0, 0))
        self.assertEqual(c.width, 50)
        self.assertEqual(c.height, 50)
        self.assertEqual(c.pixels[0][0], [0, 0, 0])


if __name__ == '__main__':
    unittest.main()