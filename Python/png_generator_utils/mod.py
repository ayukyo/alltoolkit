# -*- coding: utf-8 -*-
"""
PNG Generator Utils - PNG 图片生成工具 🖼️

纯 Python 标准库实现的 PNG 图片生成器，支持基础图形、文本、渐变。

功能:
- 纯标准库实现（zlib, struct, io），零外部依赖
- 支持 Grayscale、RGB、RGBA 颜色模式
- 绘制几何图形：点、线、矩形、圆形、三角形
- 填充与描边控制
- 简单的文字渲染（等宽字体位图）
- 渐变填充
- PNG 文件输出到文件或 BytesIO

Author: AllToolkit
Version: 1.0.0
License: MIT
"""

import zlib
import struct
import io
import math
from typing import List, Tuple, Union, Optional


# =============================================================================
# 常量
# =============================================================================

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

COLOR_GRAY = 0       # 灰度，1 byte/pixel
COLOR_RGB  = 2       # RGB，3 bytes/pixel
COLOR_INDEXED = 3   # 索引色（不支持）
COLOR_GRAY_ALPHA = 4 # 灰度+Alpha，2 bytes/pixel
COLOR_RGB_ALPHA = 6  # RGBA，4 bytes/pixel

FILTER_NONE = 0
FILTER_SUB  = 1
FILTER_UP   = 2
FILTER_AVERAGE = 3
FILTER_PAETH = 4


# =============================================================================
# 内部工具
# =============================================================================

def _chunk(chunk_type: bytes, data: bytes) -> bytes:
    """打包 PNG chunk（含 CRC）"""
    length = struct.pack('>I', len(data))
    crc = struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)
    return length + chunk_type + data + crc


def _write_u32be(value: int) -> bytes:
    return struct.pack('>I', value)


def _paeth_predictor(a: int, b: int, c: int) -> int:
    """Paeth 预测器 — PNG 过滤算法核心"""
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    elif pb <= pc:
        return b
    return c


def _filter_row(row: bytes, prev: bytes, ftype: int) -> bytes:
    """对一行像素应用过滤"""
    if ftype == FILTER_NONE:
        return bytes([ftype]) + row
    elif ftype == FILTER_SUB:
        out = bytearray([ftype])
        for i in range(len(row)):
            left = row[i - 1] if i >= 1 else 0
            out.append((row[i] - left) & 0xff)
        return bytes(out)
    elif ftype == FILTER_UP:
        out = bytearray([ftype])
        for i in range(len(row)):
            up = prev[i] if prev else 0
            out.append((row[i] - up) & 0xff)
        return bytes(out)
    elif ftype == FILTER_AVERAGE:
        out = bytearray([ftype])
        for i in range(len(row)):
            left = row[i - 1] if i >= 1 else 0
            up = prev[i] if prev else 0
            out.append((row[i] - (left + up) // 2) & 0xff)
        return bytes(out)
    elif ftype == FILTER_PAETH:
        out = bytearray([ftype])
        for i in range(len(row)):
            left = row[i - 1] if i >= 1 else 0
            up = prev[i] if prev else 0
            up_left = prev[i - 1] if prev and i >= 1 else 0
            out.append((row[i] - _paeth_predictor(left, up, up_left)) & 0xff)
        return bytes(out)
    return bytes([ftype]) + row


# =============================================================================
# 简单等宽字体位图（5x5 字符）
# =============================================================================

# 5x5 bitmaps for digits 0-9, A-Z, space, dash, dot
_FONT_DATA = {
    '0': (0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110),
    '1': (0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110),
    '2': (0b01110, 0b10001, 0b00001, 0b00110, 0b01000, 0b10000, 0b11111),
    '3': (0b01110, 0b10001, 0b00001, 0b00110, 0b00001, 0b10001, 0b01110),
    '4': (0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010),
    '5': (0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b10001, 0b01110),
    '6': (0b01110, 0b10000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110),
    '7': (0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000),
    '8': (0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110),
    '9': (0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00001, 0b01110),
    'A': (0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001),
    'B': (0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110),
    'C': (0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110),
    'D': (0b11100, 0b10010, 0b10001, 0b10001, 0b10001, 0b10010, 0b11100),
    'E': (0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111),
    'F': (0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000),
    'G': (0b01110, 0b10001, 0b10000, 0b10111, 0b10001, 0b10001, 0b01111),
    'H': (0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001),
    'I': (0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110),
    'J': (0b00111, 0b00001, 0b00001, 0b00001, 0b00001, 0b10001, 0b01110),
    'K': (0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001),
    'L': (0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111),
    'M': (0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001),
    'N': (0b10001, 0b11001, 0b10101, 0b10101, 0b10011, 0b10001, 0b10001),
    'O': (0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    'P': (0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000),
    'Q': (0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101),
    'R': (0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001),
    'S': (0b01110, 0b10001, 0b10000, 0b01110, 0b00001, 0b10001, 0b01110),
    'T': (0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100),
    'U': (0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    'V': (0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100),
    'W': (0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b10101, 0b01010),
    'X': (0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001),
    'Y': (0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100),
    'Z': (0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111),
    ' ': (0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000),
    '-': (0b00000, 0b00000, 0b00000, 0b11111, 0b00000, 0b00000, 0b00000),
    '.': (0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00100, 0b00100),
    ':': (0b00100, 0b00100, 0b00000, 0b00000, 0b00000, 0b00100, 0b00100),
    '!': (0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00000, 0b00100),
    '?': (0b01110, 0b10001, 0b00001, 0b00110, 0b00100, 0b00000, 0b00100),
    '/': (0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b00000, 0b00000),
    '+': (0b00000, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0b00000),
    '=': (0b00000, 0b00000, 0b11111, 0b00000, 0b11111, 0b00000, 0b00000),
    '(': (0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010),
    ')': (0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000),
    '%': (0b01100, 0b10010, 0b00010, 0b00100, 0b01000, 0b10001, 0b00110),
    '#': (0b01010, 0b01010, 0b11111, 0b01010, 0b11111, 0b01010, 0b01010),
}


# =============================================================================
# PNGCanvas 类
# =============================================================================

class PNGCanvas:
    """
    PNG 画布，支持 RGB 和 RGBA 模式
    
    Args:
        width:  画布宽度（像素）
        height: 画布高度（像素）
        color:  背景色，RGB三元组或RGBA四元组，默认为白色
        alpha:  是否支持透明（RGBA模式）
    """

    def __init__(
        self,
        width: int,
        height: int,
        color: Union[Tuple[int, int, int], Tuple[int, int, int, int]] = (255, 255, 255),
        alpha: bool = False
    ):
        if width < 1 or height < 1:
            raise ValueError("Width and height must be positive integers")
        
        self.width = width
        self.height = height
        self.alpha = alpha
        self.color_type = COLOR_RGB_ALPHA if alpha else COLOR_RGB
        self.bytes_per_pixel = 4 if alpha else 3
        
        # 初始化画布为背景色
        if len(color) == 3:
            fill = color + (255,) if alpha else color
        else:
            fill = color if alpha else color[:3]
        
        self.pixels = [
            [list(fill) for _ in range(width)]
            for __ in range(height)
        ]

    # -------------------------------------------------------------------------
    # 底层像素操作
    # -------------------------------------------------------------------------

    def _set_pixel(self, x: int, y: int, rgb: Tuple[int, int, int], a: int = 255):
        """设置单个像素"""
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.alpha:
                self.pixels[y][x] = [max(0, min(255, v)) for v in rgb] + [max(0, min(255, a))]
            else:
                self.pixels[y][x] = [max(0, min(255, v)) for v in rgb]

    def _get_pixel(self, x: int, y: int) -> Tuple[int, ...]:
        """获取单个像素"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return tuple(self.pixels[y][x])
        return tuple()

    # -------------------------------------------------------------------------
    # 几何图形
    # -------------------------------------------------------------------------

    def set_pixel(self, x: int, y: int, color: Union[Tuple[int, int, int], Tuple[int, int, int, int]]):
        """设置单个像素"""
        if len(color) == 4 and self.alpha:
            self._set_pixel(x, y, color[:3], color[3])
        else:
            self._set_pixel(x, y, color[:3] if len(color) == 4 and not self.alpha else color)

    def draw_point(self, x: int, y: int, color: Tuple[int, int, int]):
        """画一个点"""
        self._set_pixel(x, y, color)

    def draw_line(self, x0: int, y0: int, x1: int, y1: int, color: Tuple[int, int, int], stroke: int = 1):
        """Bresenham 画线算法"""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        
        x, y = x0, y0
        for _ in range(max(dx, -dx, dy, -dy) + 1):
            for sw in range(-stroke // 2, stroke // 2 + 1):
                if stroke == 1:
                    self._set_pixel(x, y, color)
                else:
                    self._set_pixel(x + sw, y, color)
                    self._set_pixel(x, y + sw, color)
            if 2 * err >= dy:
                err += dy
                x += sx
            if 2 * err <= dx:
                err += dx
                y += sy

    def draw_rect(
        self,
        x: int, y: int,
        w: int, h: int,
        color: Tuple[int, int, int],
        fill: bool = False,
        stroke: int = 1
    ):
        """画矩形（x,y 为左上角）"""
        if fill:
            for ry in range(y, y + h):
                for rx in range(x, x + w):
                    self._set_pixel(rx, ry, color)
        else:
            for rx in range(x, x + w):
                for sw in range(-stroke // 2, stroke // 2 + 1):
                    self._set_pixel(rx, y + sw, color)
                    self._set_pixel(rx, y + h - 1 + sw, color)
            for ry in range(y, y + h):
                for sw in range(-stroke // 2, stroke // 2 + 1):
                    self._set_pixel(x + sw, ry, color)
                    self._set_pixel(x + w - 1 + sw, ry, color)

    def draw_circle(self, cx: int, cy: int, r: int, color: Tuple[int, int, int], fill: bool = False):
        """中点圆算法画圆"""
        if r <= 0:
            return
        x, y = r, 0
        err = 0
        
        def plot_circle_points(bx: int, by: int):
            for dx_, dy_ in [(bx, by), (-bx, by), (bx, -by), (-bx, -by),
                              (by, bx), (-by, bx), (by, -bx), (-by, -bx)]:
                self._set_pixel(cx + dx_, cy + dy_, color)
        
        if fill:
            # 扫描线填充
            for ry in range(cy - r, cy + r + 1):
                for rx in range(cx - r, cx + r + 1):
                    if (rx - cx) ** 2 + (ry - cy) ** 2 <= r * r:
                        self._set_pixel(rx, ry, color)
        else:
            while x >= y:
                plot_circle_points(x, y)
                err += 2 * y + 1
                y += 1
                if err >= 0:
                    x -= 1
                    err -= 2 * x

    def draw_triangle(
        self,
        x0: int, y0: int,
        x1: int, y1: int,
        x2: int, y2: int,
        color: Tuple[int, int, int],
        fill: bool = False
    ):
        """画三角形"""
        # 包围盒
        min_x = min(x0, x1, x2)
        max_x = max(x0, x1, x2)
        min_y = min(y0, y1, y2)
        max_y = max(y0, y1, y2)
        
        def sign(p1x: int, p1y: int, p2x: int, p2y: int, p3x: int, p3y: int) -> int:
            return (p1x - p3x) * (p2y - p3y) - (p2x - p3x) * (p1y - p3y)
        
        for ry in range(min_y, max_y + 1):
            for rx in range(min_x, max_x + 1):
                nd = [
                    sign(rx, ry, x0, y0, x1, y1),
                    sign(rx, ry, x1, y1, x2, y2),
                    sign(rx, ry, x2, y2, x0, y0)
                ]
                if (nd[0] >= 0 and nd[1] >= 0 and nd[2] >= 0) or (nd[0] <= 0 and nd[1] <= 0 and nd[2] <= 0):
                    self._set_pixel(rx, ry, color)

    def draw_ellipse(self, cx: int, cy: int, rx: int, ry: int, color: Tuple[int, int, int], fill: bool = False):
        """中点椭圆算法"""
        if rx <= 0 or ry <= 0:
            return
        
        def plot_ellipse_points(bx: int, by: int):
            for dx_, dy_ in [(bx, by), (-bx, by), (bx, -by), (-bx, -by)]:
                self._set_pixel(cx + dx_, cy + dy_, color)
        
        x, y = 0, ry
        rx2 = rx * rx
        ry2 = ry * ry
        p1 = ry2 - rx2 * ry + rx2 // 4
        
        # Region 1
        while 2 * ry2 * x < 2 * rx2 * y:
            if not fill:
                plot_ellipse_points(x, y)
            else:
                for dx_ in range(-x, x + 1):
                    self._set_pixel(cx + dx_, cy + y, color)
                    self._set_pixel(cx + dx_, cy - y, color)
            x += 1
            if p1 < 0:
                p1 += 2 * ry2 * x + ry2
            else:
                y -= 1
                p1 += 2 * ry2 * x - 2 * rx2 * y + ry2
        
        # Region 2
        p2 = float(ry2) * (x + 0.5) ** 2 + float(rx2) * (y - 1) ** 2 - float(rx2) * ry2
        while y >= 0:
            if not fill:
                plot_ellipse_points(x, y)
            else:
                for dx_ in range(-x, x + 1):
                    self._set_pixel(cx + dx_, cy + y, color)
                    self._set_pixel(cx + dx_, cy - y, color)
            y -= 1
            if p2 > 0:
                p2 -= 2 * rx2 * y + rx2
            else:
                x += 1
                p2 += 2 * ry2 * x - 2 * rx2 * y + rx2

    # -------------------------------------------------------------------------
    # 渐变
    # -------------------------------------------------------------------------

    def fill_gradient_linear(
        self,
        x: int, y: int,
        w: int, h: int,
        color_start: Tuple[int, int, int],
        color_end: Tuple[int, int, int],
        angle: float = 0.0
    ):
        """线性渐变填充（角度单位：度）"""
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        for ry in range(y, y + h):
            for rx in range(x, x + w):
                dx = rx - x
                dy = ry - y
                t = (dx * cos_a + dy * sin_a) / math.sqrt(w * w + h * h) if w or h else 0
                t = max(0.0, min(1.0, t))
                r = int(color_start[0] + (color_end[0] - color_start[0]) * t)
                g = int(color_start[1] + (color_end[1] - color_start[1]) * t)
                b = int(color_start[2] + (color_end[2] - color_start[2]) * t)
                self._set_pixel(rx, ry, (r, g, b))

    def fill_gradient_radial(
        self,
        cx: int, cy: int,
        radius: int,
        color_center: Tuple[int, int, int],
        color_edge: Tuple[int, int, int]
    ):
        """径向渐变填充"""
        for ry in range(max(0, cy - radius), min(self.height, cy + radius + 1)):
            for rx in range(max(0, cx - radius), min(self.width, cx + radius + 1)):
                dist = math.sqrt((rx - cx) ** 2 + (ry - cy) ** 2)
                t = min(1.0, dist / radius) if radius > 0 else 1.0
                r = int(color_center[0] + (color_edge[0] - color_center[0]) * t)
                g = int(color_center[1] + (color_edge[1] - color_center[1]) * t)
                b = int(color_center[2] + (color_edge[2] - color_center[2]) * t)
                self._set_pixel(rx, ry, (r, g, b))

    # -------------------------------------------------------------------------
    # 文字
    # -------------------------------------------------------------------------

    def draw_char(self, cx: int, cy: int, char: str, color: Tuple[int, int, int], scale: int = 1):
        """在画布上绘制单个字符（5x5 位图字体）"""
        ch = char.upper()
        if ch not in _FONT_DATA:
            return
        rows = _FONT_DATA[ch]
        
        for row_idx, row_val in enumerate(rows):
            for col_idx in range(5):
                if (row_val >> (4 - col_idx)) & 1:
                    for sy in range(scale):
                        for sx in range(scale):
                            self._set_pixel(cx + col_idx * scale + sx, cy + row_idx * scale + sy, color)

    def draw_text(self, x: int, y: int, text: str, color: Tuple[int, int, int], scale: int = 1):
        """绘制文本字符串"""
        for i, ch in enumerate(text):
            self.draw_char(x + i * 6 * scale, y, ch, color, scale)

    def draw_text_centered(self, text: str, color: Tuple[int, int, int], scale: int = 1):
        """居中绘制文本"""
        total_width = len(text) * 6 * scale
        x = max(0, (self.width - total_width) // 2)
        y = max(0, (self.height - 7 * scale) // 2)
        self.draw_text(x, y, text, color, scale)

    # -------------------------------------------------------------------------
    # 条形图
    # -------------------------------------------------------------------------

    def draw_bar_chart(
        self,
        x: int, y: int,
        w: int, h: int,
        data: List[float],
        labels: Optional[List[str]] = None,
        bar_color: Tuple[int, int, int] = (70, 130, 180),
        bg_color: Optional[Tuple[int, int, int]] = None
    ):
        """绘制水平条形图"""
        if bg_color:
            self.draw_rect(x, y, w, h, bg_color, fill=True)
        
        if not data:
            return
        
        max_val = max(data) if max(data) != 0 else 1
        n = len(data)
        bar_area_h = h - (7 * scale if labels else 0)
        bar_h = max(2, bar_area_h // n - 2)
        
        for i, val in enumerate(data):
            bar_w = int((val / max_val) * (w - 10))
            bar_y = y + i * (bar_h + 2)
            self.draw_rect(x + 5, bar_y, bar_w, bar_h, bar_color, fill=True)
            
            if labels and i < len(labels):
                label_x = x + 5
                self.draw_text(label_x, bar_y + bar_h - 7 * scale, labels[i], (50, 50, 50), scale)

    # -------------------------------------------------------------------------
    # 编码 & 输出
    # -------------------------------------------------------------------------

    def _encode_rows(self) -> bytes:
        """将像素数据编码为 PNG 行字节流"""
        raw_rows = []
        prev_row = b''
        
        for row in self.pixels:
            raw = bytearray()
            for pixel in row:
                raw.extend(pixel)
            filtered = _filter_row(bytes(raw), prev_row, FILTER_SUB)
            raw_rows.append(filtered)
            prev_row = bytes(raw)
        
        return b''.join(raw_rows)

    def encode(self) -> bytes:
        """编码为 PNG 字节串"""
        buf = io.BytesIO()
        
        # Signature
        buf.write(PNG_SIGNATURE)
        
        # IHDR
        ihdr_data = struct.pack('>IIBBBBB',
            self.width, self.height,
            8,          # bit depth
            self.color_type,
            0,          # compression
            0,          # filter
            0           # interlace
        )
        buf.write(_chunk(b'IHDR', ihdr_data))
        
        # IDAT
        raw_data = self._encode_rows()
        compressed = zlib.compress(raw_data, 9)
        buf.write(_chunk(b'IDAT', compressed))
        
        # IEND
        buf.write(_chunk(b'IEND', b''))
        
        return buf.getvalue()

    def save(self, filepath: str):
        """保存到文件"""
        with open(filepath, 'wb') as f:
            f.write(self.encode())

    def to_bytes(self) -> bytes:
        """返回 PNG 字节串"""
        return self.encode()


# =============================================================================
# 快捷函数
# =============================================================================

def create_canvas(
    width: int,
    height: int,
    bg: Tuple[int, int, int] = (255, 255, 255),
    alpha: bool = False
) -> PNGCanvas:
    """创建 PNG 画布"""
    return PNGCanvas(width, height, bg, alpha)


def solid_png(width: int, height: int, color: Tuple[int, int, int]) -> bytes:
    """生成纯色 PNG"""
    canvas = PNGCanvas(width, height, color, alpha=False)
    # 将背景色设为中心心
    canvas.fill_gradient_radial(width // 2, height // 2, max(width, height) // 2,
                                 color, tuple(max(0, c - 30) for c in color))
    return canvas.encode()


def bar_chart_png(
    data: List[float],
    labels: Optional[List[str]] = None,
    width: int = 400,
    height: int = 300,
    bar_color: Tuple[int, int, int] = (70, 130, 180),
    title: str = ""
) -> bytes:
    """生成条形图 PNG"""
    canvas = PNGCanvas(width, height, (248, 248, 248))
    
    margin = 40
    chart_w = width - 2 * margin
    chart_h = height - 2 * margin - (30 if title else 0)
    
    if not data:
        return canvas.encode()
    
    max_val = max(data) if max(data) != 0 else 1
    n = len(data)
    bar_w = max(2, (chart_w - (n - 1) * 4) // n)
    bar_area_h = chart_h - 20
    
    if title:
        canvas.draw_text_centered(title, (40, 40, 40), scale=2)
    
    for i, val in enumerate(data):
        bar_height = int((val / max_val) * bar_area_h)
        bx = margin + i * (bar_w + 4)
        by = margin + bar_area_h - bar_height
        canvas.draw_rect(bx, by, bar_w, bar_height, bar_color, fill=True)
        
        if labels and i < len(labels):
            canvas.draw_text(bx, margin + bar_area_h + 2, labels[i], (80, 80, 80), scale=1)
    
    return canvas.encode()