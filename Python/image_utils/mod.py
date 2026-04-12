"""
AllToolkit - Python Image Utilities

功能完整的图像处理工具模块，支持图像格式转换、缩放、裁剪、旋转、
压缩、缩略图生成、信息读取、批量处理、水印添加、图像合并等功能。

使用 Pillow 库（如果可用），否则优雅降级使用标准库功能。

Author: AllToolkit
License: MIT
"""

import os
import io
import struct
from typing import Union, Optional, Tuple, List, Dict, Any, BinaryIO
from pathlib import Path


# =============================================================================
# Pillow 检测与导入
# =============================================================================

_PILLOW_AVAILABLE = False
Image = None
ImageOps = None
ImageDraw = None
ImageFont = None
ImageFilter = None

try:
    from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
    _PILLOW_AVAILABLE = True
except ImportError:
    pass


# =============================================================================
# 图像信息读取（标准库实现）
# =============================================================================

class ImageInfo:
    """
    图像信息容器类。
    
    Attributes:
        width: 图像宽度（像素）
        height: 图像高度（像素）
        format: 图像格式（PNG, JPEG, GIF, etc.）
        mode: 颜色模式（RGB, RGBA, L, etc.）
        file_size: 文件大小（字节）
        has_alpha: 是否有透明通道
        bit_depth: 位深度
    """
    
    def __init__(self, width: int = 0, height: int = 0, format: str = "UNKNOWN",
                 mode: str = "UNKNOWN", file_size: int = 0, has_alpha: bool = False,
                 bit_depth: int = 8):
        self.width = width
        self.height = height
        self.format = format
        self.mode = mode
        self.file_size = file_size
        self.has_alpha = has_alpha
        self.bit_depth = bit_depth
    
    def __repr__(self) -> str:
        return (f"ImageInfo({self.width}x{self.height}, {self.format}, "
                f"{self.mode}, {self.file_size} bytes)")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典。"""
        return {
            'width': self.width,
            'height': self.height,
            'format': self.format,
            'mode': self.mode,
            'file_size': self.file_size,
            'has_alpha': self.has_alpha,
            'bit_depth': self.bit_depth,
        }


def _read_png_info(data: bytes) -> Optional[ImageInfo]:
    """读取 PNG 文件信息（标准库实现）。"""
    if len(data) < 24 or data[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    
    # 解析 IHDR 块
    width = struct.unpack('>I', data[16:20])[0]
    height = struct.unpack('>I', data[20:24])[0]
    
    # 颜色类型：0=灰度，2=RGB，3=索引，4=灰度+alpha，6=RGBA
    color_type = data[25]
    mode_map = {0: 'L', 2: 'RGB', 3: 'P', 4: 'LA', 6: 'RGBA'}
    mode = mode_map.get(color_type, 'UNKNOWN')
    
    # 位深度
    bit_depth = data[24]
    
    return ImageInfo(
        width=width,
        height=height,
        format='PNG',
        mode=mode,
        has_alpha=color_type in (4, 6),
        bit_depth=bit_depth,
    )


def _read_jpeg_info(data: bytes) -> Optional[ImageInfo]:
    """读取 JPEG 文件信息（标准库实现）。"""
    if len(data) < 2 or data[:2] != b'\xff\xd8':
        return None
    
    width = height = 0
    pos = 2
    
    while pos < len(data) - 1:
        if data[pos] != 0xff:
            pos += 1
            continue
        
        marker = data[pos + 1]
        
        # SOF 标记（Start Of Frame）
        if marker in (0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7,
                      0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf):
            if pos + 9 < len(data):
                height = struct.unpack('>H', data[pos + 5:pos + 7])[0]
                width = struct.unpack('>H', data[pos + 7:pos + 9])[0]
                break
        
        # 跳过当前块
        if marker not in (0x00, 0x01, 0xd0, 0xd1, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8):
            if pos + 3 < len(data):
                length = struct.unpack('>H', data[pos + 2:pos + 4])[0]
                pos += 2 + length
            else:
                break
        else:
            pos += 2
    
    if width and height:
        return ImageInfo(width=width, height=height, format='JPEG', mode='RGB')
    return None


def _read_gif_info(data: bytes) -> Optional[ImageInfo]:
    """读取 GIF 文件信息（标准库实现）。"""
    if len(data) < 13 or data[:6] not in (b'GIF87a', b'GIF89a'):
        return None
    
    width = struct.unpack('<H', data[6:8])[0]
    height = struct.unpack('<H', data[8:10])[0]
    
    return ImageInfo(width=width, height=height, format='GIF', mode='P')


def _read_bmp_info(data: bytes) -> Optional[ImageInfo]:
    """读取 BMP 文件信息（标准库实现）。"""
    if len(data) < 26 or data[:2] != b'BM':
        return None
    
    width = struct.unpack('<I', data[18:22])[0]
    height = struct.unpack('<I', data[22:26])[0]
    
    # 高度可能为负（表示从上到下）
    height = abs(height)
    
    # 位深度
    bit_depth = struct.unpack('<H', data[28:30])[0]
    
    mode_map = {1: '1', 4: 'P', 8: 'P', 16: 'RGB', 24: 'RGB', 32: 'RGBA'}
    mode = mode_map.get(bit_depth, 'RGB')
    
    return ImageInfo(
        width=width,
        height=height,
        format='BMP',
        mode=mode,
        bit_depth=bit_depth,
    )


def _read_webp_info(data: bytes) -> Optional[ImageInfo]:
    """读取 WebP 文件信息（标准库实现）。"""
    if len(data) < 30 or data[:4] != b'RIFF' or data[8:12] != b'WEBP':
        return None
    
    # VP8 格式
    if data[12:16] == b'VP8 ':
        # 解析 VP8 帧头
        pos = 23
        if pos + 9 < len(data) and data[pos] == 0x9d:
            width = struct.unpack('<H', data[pos + 6:pos + 8])[0] & 0x3fff
            height = struct.unpack('<H', data[pos + 8:pos + 10])[0] & 0x3fff
            return ImageInfo(width=width, height=height, format='WebP', mode='RGB')
    
    # VP8L 格式（无损/带 alpha）
    elif data[12:16] == b'VP8L':
        if len(data) > 29:
            bits = struct.unpack('<I', data[21:25])[0]
            width = (bits & 0x3fff) + 1
            height = ((bits >> 14) & 0x3fff) + 1
            has_alpha = (bits >> 28) & 1
            return ImageInfo(
                width=width,
                height=height,
                format='WebP',
                mode='RGBA' if has_alpha else 'RGB',
                has_alpha=bool(has_alpha),
            )
    
    # VP8X 格式（扩展）
    elif data[12:16] == b'VP8X':
        if len(data) > 26:
            width = struct.unpack('<I', data[18:21] + b'\x00')[0] + 1
            height = struct.unpack('<I', data[21:24] + b'\x00')[0] + 1
            has_alpha = bool(data[16] & 0x10)
            return ImageInfo(
                width=width,
                height=height,
                format='WebP',
                mode='RGBA' if has_alpha else 'RGB',
                has_alpha=has_alpha,
            )
    
    return None


def get_image_info(source: Union[str, bytes, BinaryIO]) -> ImageInfo:
    """
    获取图像信息（尺寸、格式、颜色模式等）。
    
    支持格式：PNG, JPEG, GIF, BMP, WebP
    
    Args:
        source: 图像源，可以是：
            - 文件路径（字符串或 Path）
            - 图像数据（bytes）
            - 文件对象（BinaryIO）
    
    Returns:
        ImageInfo: 图像信息对象
    
    Raises:
        ValueError: 无法识别的图像格式
        FileNotFoundError: 文件不存在
        IOError: 读取失败
    
    Example:
        >>> info = get_image_info('photo.png')
        >>> print(f"{info.width}x{info.height} {info.format}")
        1920x1080 PNG
        
        >>> with open('photo.jpg', 'rb') as f:
        ...     info = get_image_info(f)
        >>> info.has_alpha
        False
    """
    # 读取图像数据
    if isinstance(source, (str, Path)):
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在：{source}")
        file_size = path.stat().st_size
        with open(source, 'rb') as f:
            data = f.read(4096)  # 只需读取头部
    elif isinstance(source, bytes):
        data = source[:4096]
        file_size = len(source)
    elif hasattr(source, 'read'):
        pos = source.tell() if hasattr(source, 'tell') else 0
        data = source.read(4096)
        file_size = 0
        if hasattr(source, 'seek'):
            source.seek(pos)
    else:
        raise TypeError(f"不支持的源类型：{type(source)}")
    
    # 使用 Pillow（如果可用）
    if _PILLOW_AVAILABLE:
        try:
            img = Image.open(io.BytesIO(data) if isinstance(data, bytes) else data)
            return ImageInfo(
                width=img.width,
                height=img.height,
                format=img.format or 'UNKNOWN',
                mode=img.mode,
                file_size=file_size,
                has_alpha=img.mode in ('RGBA', 'LA', 'PA'),
            )
        except Exception:
            pass  # 降级到标准库实现
    
    # 标准库实现
    if isinstance(data, bytes):
        # PNG
        if data[:8] == b'\x89PNG\r\n\x1a\n':
            info = _read_png_info(data)
            if info:
                info.file_size = file_size
                return info
        
        # JPEG
        if data[:2] == b'\xff\xd8':
            info = _read_jpeg_info(data)
            if info:
                info.file_size = file_size
                return info
        
        # GIF
        if data[:6] in (b'GIF87a', b'GIF89a'):
            info = _read_gif_info(data)
            if info:
                info.file_size = file_size
                return info
        
        # BMP
        if data[:2] == b'BM':
            info = _read_bmp_info(data)
            if info:
                info.file_size = file_size
                return info
        
        # WebP
        if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
            info = _read_webp_info(data)
            if info:
                info.file_size = file_size
                return info
    
    raise ValueError("无法识别的图像格式")


# =============================================================================
# 图像格式转换
# =============================================================================

def convert_format(source: Union[str, bytes], output_format: str,
                   output_path: Optional[str] = None,
                   quality: int = 95) -> Optional[bytes]:
    """
    转换图像格式。
    
    支持格式：PNG, JPEG, GIF, BMP, WebP, TIFF
    
    Args:
        source: 源图像（文件路径或 bytes）
        output_format: 目标格式（PNG, JPEG, GIF, BMP, WebP, TIFF）
        output_path: 输出文件路径（可选，如果为 None 则返回 bytes）
        quality: JPEG/WebP 质量（1-100），默认 95
    
    Returns:
        bytes 或 None: 如果指定 output_path 则返回 None，否则返回图像数据
    
    Raises:
        ValueError: 不支持的格式
        FileNotFoundError: 源文件不存在
        IOError: 转换失败
    
    Example:
        >>> # 转换为 JPEG
        >>> convert_format('input.png', 'JPEG', 'output.jpg')
        
        >>> # 获取转换后的数据
        >>> data = convert_format('input.png', 'WebP')
    """
    valid_formats = {'PNG', 'JPEG', 'JPG', 'GIF', 'BMP', 'WEBP', 'TIFF', 'TIF'}
    
    if output_format not in valid_formats:
        raise ValueError(f"不支持的格式：{output_format}")
    
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库：pip install Pillow")
    
    if output_format == 'JPG':
        output_format = 'JPEG'
    elif output_format == 'TIF':
        output_format = 'TIFF'
    
    # 加载图像
    if isinstance(source, bytes):
        img = Image.open(io.BytesIO(source))
    else:
        img = Image.open(source)
    
    # 转换
    output = io.BytesIO()
    
    # 处理透明度（JPEG 不支持）
    if output_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'PA'):
        # 创建白色背景
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'RGBA':
            background.paste(img, mask=img.split()[3])
        else:
            background.paste(img.convert('RGBA'), mask=img.convert('RGBA').split()[3])
        img = background
    
    save_kwargs = {}
    if output_format in ('JPEG', 'WEBP'):
        save_kwargs['quality'] = quality
        save_kwargs['optimize'] = True
    elif output_format == 'PNG':
        save_kwargs['optimize'] = True
    
    img.save(output, format=output_format, **save_kwargs)
    
    if output_path:
        with open(output_path, 'wb') as f:
            f.write(output.getvalue())
        return None
    else:
        return output.getvalue()


# =============================================================================
# 图像缩放/调整大小
# =============================================================================

def resize_image(source: Union[str, bytes], width: int, height: int,
                 output_path: Optional[str] = None,
                 method: str = 'lanczos',
                 maintain_aspect: bool = False) -> Optional[bytes]:
    """
    调整图像大小。
    
    Args:
        source: 源图像
        width: 目标宽度
        height: 目标高度
        output_path: 输出路径（可选）
        method: 缩放算法（'nearest', 'bilinear', 'bicubic', 'lanczos'）
        maintain_aspect: 是否保持宽高比
    
    Returns:
        bytes 或 None: 转换后的图像数据
    
    Raises:
        ValueError: 无效参数
        RuntimeError: Pillow 不可用
    
    Example:
        >>> resize_image('input.jpg', 800, 600, 'output.jpg')
        >>> resize_image('input.jpg', 400, 400, maintain_aspect=True)
    """
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库：pip install Pillow")
    
    method_map = {
        'nearest': Image.NEAREST,
        'bilinear': Image.BILINEAR,
        'bicubic': Image.BICUBIC,
        'lanczos': Image.LANCZOS,
    }
    
    resample = method_map.get(method.lower(), Image.LANCZOS)
    
    # 加载图像
    if isinstance(source, bytes):
        img = Image.open(io.BytesIO(source))
    else:
        img = Image.open(source)
    
    # 保持宽高比
    if maintain_aspect:
        img.thumbnail((width, height), resample)
    else:
        img = img.resize((width, height), resample)
    
    # 保存
    output = io.BytesIO()
    img.save(output, format=img.format or 'PNG')
    
    if output_path:
        with open(output_path, 'wb') as f:
            f.write(output.getvalue())
        return None
    return output.getvalue()


def scale_image(source: Union[str, bytes], scale_factor: float,
                output_path: Optional[str] = None) -> Optional[bytes]:
    """
    按比例缩放图像。
    
    Args:
        source: 源图像
        scale_factor: 缩放因子（0.5=缩小一半，2.0=放大两倍）
        output_path: 输出路径（可选）
    
    Returns:
        bytes 或 None
    
    Example:
        >>> scale_image('input.jpg', 0.5, 'half_size.jpg')  # 缩小到 50%
        >>> scale_image('input.jpg', 2.0)  # 放大到 200%
    """
    if scale_factor <= 0:
        raise ValueError("缩放因子必须为正数")
    
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库：pip install Pillow")
    
    # 加载图像
    if isinstance(source, bytes):
        img = Image.open(io.BytesIO(source))
    else:
        img = Image.open(source)
    
    new_width = int(img.width * scale_factor)
    new_height = int(img.height * scale_factor)
    
    return resize_image(source, new_width, new_height, output_path)


# =============================================================================
# 图像裁剪
# =============================================================================

def crop_image(source: Union[str, bytes], box: Tuple[int, int, int, int],
               output_path: Optional[str] = None) -> Optional[bytes]:
    """
    裁剪图像。
    
    Args:
        source: 源图像
        box: 裁剪区域 (left, upper, right, lower)
        output_path: 输出路径（可选）
    
    Returns:
        bytes 或 None
    
    Raises:
        ValueError: 无效的裁剪区域
    
    Example:
        >>> # 裁剪左上角 100x100 区域
        >>> crop_image('input.jpg', (0, 0, 100, 100), 'cropped.jpg')
    """
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库：pip install Pillow")
    
    if len(box) != 4:
        raise ValueError("裁剪区域必须是 (left, upper, right, lower)")
    
    # 加载图像
    if isinstance(source, bytes):
        img = Image.open(io.BytesIO(source))
    else:
        img = Image.open(source)
    
    # 验证裁剪区域
    left, upper, right, lower = box
    if not (0 <= left < right <= img.width and 0 <= upper < lower <= img.height):
        raise ValueError(f"裁剪区域超出图像范围：{img.width}x{img.height}")
    
    cropped = img.crop(box)
    
    # 保存
    output = io.BytesIO()
    cropped.save(output, format=img.format or 'PNG')
    
    if output_path:
        with open(output_path, 'wb') as f:
            f.write(output.getvalue())
        return None
    return output.getvalue()


def center_crop(source: Union[str, bytes], width: int, height: int,
                output_path: Optional[str] = None) -> Optional[bytes]:
    """
    从中心裁剪图像。
    
    Args:
        source: 源图像
        width: 裁剪宽度
        height: 裁剪高度
        output_path: 输出路径（可选）
    
    Returns:
        bytes 或 None
    
    Example:
        >>> center_crop('input.jpg', 400, 400, 'square.jpg')  # 正方形裁剪
    """
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库：pip install Pillow")
    
    # 加载图像
    if isinstance(source, bytes):
        img = Image.open(io.BytesIO(source))
    else:
        img = Image.open(source)
    
    # 计算中心裁剪区域
    left = (img.width - width) // 2
    upper = (img.height - height) // 2
    right = left + width
    lower = upper + height
    
    # 确保不超出边界
    left = max(0, left)
    upper = max(0, upper)
    right = min(img.width, right)
    lower = min(img.height, lower)
    
    return crop_image(source, (left, upper, right, lower), output_path)


# =============================================================================
# 图像旋转
# =============================================================================

def rotate_image(source: Union[str, bytes], angle: float,
                 output_path: Optional[str] = None,
                 expand: bool = False,
                 fill_color: Tuple[int, ...] = (0, 0, 0, 0)) -> Optional[bytes]:
    """
    旋转图像。
    
    Args:
        source: 源图像
        angle: 旋转角度（逆时针，度）
        output_path: 输出路径（可选）
        expand: 是否扩展画布以容纳整个旋转后的图像
        fill_color: 填充颜色（默认透明）
    
    Returns:
        bytes 或 None
    
    Example:
        >>> rotate_image('input.jpg', 90, 'rotated.jpg')  # 旋转 90 度
        >>> rotate_image('input.jpg', 45, expand=True)  # 旋转 45 度并扩展
    """
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库：pip install Pillow")
    
    # 加载图像
    if isinstance(source, bytes):
        img = Image.open(io.BytesIO(source))
    else:
        img = Image.open(source)
    
    rotated = img.rotate(angle, expand=expand, fillcolor=fill_color,
                         resample=Image.BICUBIC)
    
    # 保存
    output = io.BytesIO()
    rotated.save(output, format=img.format or 'PNG')
    
    if output_path:
        with open(output_path, 'wb') as f:
            f.write(output.getvalue())
        return None
    return output.getvalue()


def flip_image(source: Union[str, bytes], direction: str = 'vertical',
               output_path: Optional[str] = None) -> Optional[bytes]:
    """
    翻转图像。
    
    Args:
        source: 源图像
        direction: 翻转方向（'vertical', 'horizontal', 'both'）
        output_path: 输出路径（可选）
    
    Returns:
        bytes 或 None
    
    Example:
        >>> flip_image('input.jpg', 'horizontal', 'mirrored.jpg')
        >>> flip_image('input.jpg', 'vertical')
    """
    if direction.lower() not in ('vertical', 'horizontal', 'both'):
        raise ValueError("direction 必须是 'vertical', 'horizontal' 或 'both'")
    
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库：pip install Pillow")
    
    # 加载图像
    if isinstance(source, bytes):
        img = Image.open(io.BytesIO(source))
    else:
        img = Image.open(source)
    
    if direction.lower() == 'vertical':
        flipped = img.transpose(Image.FLIP_TOP_BOTTOM)
    elif direction.lower() == 'horizontal':
        flipped = img.transpose(Image.FLIP_LEFT_RIGHT)
    else:  # both
        flipped = img.transpose(Image.ROTATE_180)
    
    # 保存
    output = io.BytesIO()
    flipped.save(output, format=img.format or 'PNG')
    
    if output_path:
        with open(output_path, 'wb') as f:
            f.write(output.getvalue())
        return None
    return output.getvalue()


# =============================================================================
# 图像压缩
# =============================================================================

def compress_image(source: Union[str, bytes], output_path: Optional[str] = None,
                   quality: int = 85, max_size: Optional[int] = None,
                   max_dimensions: Optional[Tuple[int, int]] = None) -> Optional[bytes]:
    """
    压缩图像。
    
    Args:
        source: 源图像
        output_path: 输出路径（可选）
        quality: JPEG/WebP 质量（1-100）
        max_size: 最大文件大小（字节），如果超过则降低质量
        max_dimensions: 最大尺寸 (width, height)
    
    Returns:
        bytes 或 None
    
    Example:
        >>> compress_image('input.jpg', 'compressed.jpg', quality=75)
        >>> compress_image('input.jpg', max_size=100000)  # 限制在 100KB
    """
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库：pip install Pillow")
    
    # 加载图像
    if isinstance(source, bytes):
        img = Image.open(io.BytesIO(source))
        original_data = source
    else:
        img = Image.open(source)
        with open(source, 'rb') as f:
            original_data = f.read()
    
    # 调整尺寸（如果需要）
    if max_dimensions:
        img.thumbnail(max_dimensions, Image.LANCZOS)
    
    # 确定格式
    fmt = img.format or 'JPEG'
    if fmt.upper() not in ('JPEG', 'PNG', 'WEBP'):
        fmt = 'JPEG'
    
    # 压缩
    output = io.BytesIO()
    save_kwargs = {'optimize': True}
    
    if fmt.upper() in ('JPEG', 'WEBP'):
        save_kwargs['quality'] = quality
    elif fmt.upper() == 'PNG':
        save_kwargs['compress_level'] = 9
    
    img.save(output, format=fmt, **save_kwargs)
    result = output.getvalue()
    
    # 如果指定了最大大小且超过，则迭代降低质量
    if max_size and len(result) > max_size and fmt.upper() in ('JPEG', 'WEBP'):
        current_quality = quality
        while len(result) > max_size and current_quality > 10:
            current_quality -= 5
            output = io.BytesIO()
            img.save(output, format=fmt, quality=current_quality, optimize=True)
            result = output.getvalue()
    
    if output_path:
        with open(output_path, 'wb') as f:
            f.write(result)
        return None
    return result


# =============================================================================
# 缩略图生成
# =============================================================================

def generate_thumbnail(source: Union[str, bytes], size: Tuple[int, int],
                       output_path: Optional[str] = None,
                       maintain_aspect: bool = True) -> Optional[bytes]:
    """
    生成缩略图。
    
    Args:
        source: 源图像
        size: 目标尺寸 (width, height)
        output_path: 输出路径（可选）
        maintain_aspect: 是否保持宽高比
    
    Returns:
        bytes 或 None
    
    Example:
        >>> generate_thumbnail('photo.jpg', (200, 200), 'thumb.jpg')
        >>> generate_thumbnail('photo.jpg', (100, 100))  # 返回 bytes
    """
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库：pip install Pillow")
    
    # 加载图像
    if isinstance(source, bytes):
        img = Image.open(io.BytesIO(source))
    else:
        img = Image.open(source)
    
    # 创建缩略图
    img.thumbnail(size, Image.LANCZOS)
    
    # 如果需要固定尺寸且保持宽高比，添加边框
    if maintain_aspect and img.size != size:
        thumb = Image.new('RGBA', size, (255, 255, 255, 0))
        x = (size[0] - img.width) // 2
        y = (size[1] - img.height) // 2
        thumb.paste(img, (x, y))
        img = thumb
    
    # 保存
    output = io.BytesIO()
    img.save(output, format='JPEG' if img.mode == 'RGB' else 'PNG')
    
    if output_path:
        with open(output_path, 'wb') as f:
            f.write(output.getvalue())
        return None
    return output.getvalue()


# =============================================================================
# 水印添加
# =============================================================================

def add_watermark(source: Union[str, bytes], text: str,
                  output_path: Optional[str] = None,
                  position: str = 'bottom-right',
                  font_size: int = 24,
                  color: Tuple[int, int, int, int] = (255, 255, 255, 128),
                  margin: int = 10) -> Optional[bytes]:
    """
    添加文字水印。
    
    Args:
        source: 源图像
        text: 水印文字
        output_path: 输出路径（可选）
        position: 位置（'top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'）
        font_size: 字体大小
        color: 字体颜色 (R, G, B, A)
        margin: 边距（像素）
    
    Returns:
        bytes 或 None
    
    Example:
        >>> add_watermark('photo.jpg', '© 2024', 'watermarked.jpg')
        >>> add_watermark('photo.jpg', 'CONFIDENTIAL', position='center', 
        ...               font_size=48, color=(255, 0, 0, 100))
    """
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库：pip install Pillow")
    
    # 加载图像
    if isinstance(source, bytes):
        img = Image.open(io.BytesIO(source)).convert('RGBA')
    else:
        img = Image.open(source).convert('RGBA')
    
    # 创建透明图层
    txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    # 尝试加载字体
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    except (IOError, OSError):
        try:
            font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", font_size)
        except (IOError, OSError):
            font = ImageFont.load_default()
    
    # 获取文字边界框
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # 计算位置
    positions = {
        'top-left': (margin, margin),
        'top-right': (img.width - text_width - margin, margin),
        'bottom-left': (margin, img.height - text_height - margin),
        'bottom-right': (img.width - text_width - margin, img.height - text_height - margin),
        'center': ((img.width - text_width) // 2, (img.height - text_height) // 2),
    }
    
    pos = positions.get(position.lower(), positions['bottom-right'])
    
    # 绘制文字
    draw.text(pos, text, font=font, fill=color)
    
    # 合并
    watermarked = Image.alpha_composite(img, txt_layer)
    
    # 保存
    output = io.BytesIO()
    watermarked.save(output, format='PNG')
    
    if output_path:
        with open(output_path, 'wb') as f:
            f.write(output.getvalue())
        return None
    return output.getvalue()


def add_image_watermark(source: Union[str, bytes], watermark_path: str,
                        output_path: Optional[str] = None,
                        position: str = 'bottom-right',
                        opacity: float = 0.5,
                        scale: float = 0.2,
                        margin: int = 10) -> Optional[bytes]:
    """
    添加图片水印。
    
    Args:
        source: 源图像
        watermark_path: 水印图片路径
        output_path: 输出路径（可选）
        position: 位置（同 add_watermark）
        opacity: 不透明度（0.0-1.0）
        scale: 水印相对大小（相对于源图像宽度）
        margin: 边距
    
    Returns:
        bytes 或 None
    
    Example:
        >>> add_image_watermark('photo.jpg', 'logo.png', 'watermarked.jpg')
    """
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库：pip install Pillow")
    
    # 加载图像
    if isinstance(source, bytes):
        img = Image.open(io.BytesIO(source)).convert('RGBA')
    else:
        img = Image.open(source).convert('RGBA')
    
    watermark = Image.open(watermark_path).convert('RGBA')
    
    # 调整水印大小
    new_width = int(img.width * scale)
    new_height = int(watermark.height * (new_width / watermark.width))
    watermark = watermark.resize((new_width, new_height), Image.LANCZOS)
    
    # 应用透明度
    if opacity < 1.0:
        alpha = watermark.split()[3]
        alpha = alpha.point(lambda p: int(p * opacity))
        watermark.putalpha(alpha)
    
    # 计算位置
    positions = {
        'top-left': (margin, margin),
        'top-right': (img.width - new_width - margin, margin),
        'bottom-left': (margin, img.height - new_height - margin),
        'bottom-right': (img.width - new_width - margin, img.height - new_height - margin),
        'center': ((img.width - new_width) // 2, (img.height - new_height) // 2),
    }
    
    pos = positions.get(position.lower(), positions['bottom-right'])
    
    # 合并
    img.paste(watermark, pos, watermark)
    
    # 保存
    output = io.BytesIO()
    img.save(output, format='PNG')
    
    if output_path:
        with open(output_path, 'wb') as f:
            f.write(output.getvalue())
        return None
    return output.getvalue()


# =============================================================================
# 图像合并/拼接
# =============================================================================

def merge_images(images: List[Union[str, bytes]], direction: str = 'horizontal',
                 output_path: Optional[str] = None,
                 gap: int = 0,
                 background_color: Tuple[int, int, int, int] = (255, 255, 255, 255)) -> Optional[bytes]:
    """
    合并/拼接多张图像。
    
    Args:
        images: 图像列表（路径或 bytes）
        direction: 拼接方向（'horizontal', 'vertical'）
        output_path: 输出路径（可选）
        gap: 图像间距（像素）
        background_color: 背景颜色
    
    Returns:
        bytes 或 None
    
    Raises:
        ValueError: 图像列表为空
    
    Example:
        >>> merge_images(['a.jpg', 'b.jpg', 'c.jpg'], 'horizontal', 'panorama.jpg')
        >>> merge_images(['top.png', 'bottom.png'], 'vertical')
    """
    if not images:
        raise ValueError("图像列表不能为空")
    
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库：pip install Pillow")
    
    # 加载所有图像
    loaded_images = []
    for img_source in images:
        if isinstance(img_source, bytes):
            img = Image.open(io.BytesIO(img_source)).convert('RGBA')
        else:
            img = Image.open(img_source).convert('RGBA')
        loaded_images.append(img)
    
    if direction.lower() == 'horizontal':
        total_width = sum(img.width for img in loaded_images) + gap * (len(loaded_images) - 1)
        max_height = max(img.height for img in loaded_images)
        
        result = Image.new('RGBA', (total_width, max_height), background_color)
        
        x_offset = 0
        for img in loaded_images:
            y_offset = (max_height - img.height) // 2
            result.paste(img, (x_offset, y_offset))
            x_offset += img.width + gap
    
    elif direction.lower() == 'vertical':
        max_width = max(img.width for img in loaded_images)
        total_height = sum(img.height for img in loaded_images) + gap * (len(loaded_images) - 1)
        
        result = Image.new('RGBA', (max_width, total_height), background_color)
        
        y_offset = 0
        for img in loaded_images:
            x_offset = (max_width - img.width) // 2
            result.paste(img, (x_offset, y_offset))
            y_offset += img.height + gap
    else:
        raise ValueError("direction 必须是 'horizontal' 或 'vertical'")
    
    # 保存
    output = io.BytesIO()
    result.save(output, format='PNG')
    
    if output_path:
        with open(output_path, 'wb') as f:
            f.write(output.getvalue())
        return None
    return output.getvalue()


def create_grid(images: List[Union[str, bytes]], cols: int,
                output_path: Optional[str] = None,
                cell_size: Optional[Tuple[int, int]] = None,
                gap: int = 0,
                background_color: Tuple[int, int, int, int] = (255, 255, 255, 255)) -> Optional[bytes]:
    """
    创建图像网格。
    
    Args:
        images: 图像列表
        cols: 列数
        output_path: 输出路径（可选）
        cell_size: 单元格大小 (width, height)，如果为 None 则使用最大图像尺寸
        gap: 间距
        background_color: 背景颜色
    
    Returns:
        bytes 或 None
    
    Example:
        >>> create_grid(['img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg'], 
        ...             cols=2, output_path='grid.png')
    """
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库：pip install Pillow")
    
    if not images:
        raise ValueError("图像列表不能为空")
    
    # 加载所有图像
    loaded_images = []
    for img_source in images:
        if isinstance(img_source, bytes):
            img = Image.open(io.BytesIO(img_source)).convert('RGBA')
        else:
            img = Image.open(img_source).convert('RGBA')
        
        # 调整到单元格大小
        if cell_size:
            img.thumbnail(cell_size, Image.LANCZOS)
        
        loaded_images.append(img)
    
    # 计算行列
    rows = (len(loaded_images) + cols - 1) // cols
    
    # 确定单元格大小
    if cell_size is None:
        max_width = max(img.width for img in loaded_images)
        max_height = max(img.height for img in loaded_images)
        cell_size = (max_width, max_height)
    
    # 创建结果图像
    total_width = cols * cell_size[0] + gap * (cols - 1)
    total_height = rows * cell_size[1] + gap * (rows - 1)
    
    result = Image.new('RGBA', (total_width, total_height), background_color)
    
    # 放置图像
    for idx, img in enumerate(loaded_images):
        row = idx // cols
        col = idx % cols
        
        x = col * (cell_size[0] + gap)
        y = row * (cell_size[1] + gap)
        
        # 居中放置
        x += (cell_size[0] - img.width) // 2
        y += (cell_size[1] - img.height) // 2
        
        result.paste(img, (x, y))
    
    # 保存
    output = io.BytesIO()
    result.save(output, format='PNG')
    
    if output_path:
        with open(output_path, 'wb') as f:
            f.write(output.getvalue())
        return None
    return output.getvalue()


# =============================================================================
# 批量处理
# =============================================================================

def batch_process(input_pattern: str, output_dir: str,
                  process_func, *args, **kwargs) -> Dict[str, Any]:
    """
    批量处理图像。
    
    Args:
        input_pattern: 输入文件模式（如 '*.jpg'）
        output_dir: 输出目录
        process_func: 处理函数（接收 source, output_path 参数）
        *args, **kwargs: 传递给处理函数的参数
    
    Returns:
        处理结果统计
    
    Example:
        >>> def resize_func(source, output_path):
        ...     return resize_image(source, 800, 600, output_path)
        >>> batch_process('*.jpg', 'output/', resize_func)
    """
    import glob
    
    results = {
        'processed': 0,
        'failed': 0,
        'errors': [],
    }
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取文件列表
    files = glob.glob(input_pattern)
    
    for file_path in files:
        try:
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{name}_processed{ext}")
            
            process_func(file_path, output_path, *args, **kwargs)
            results['processed'] += 1
        except Exception as e:
            results['failed'] += 1
            results['errors'].append(f"{file_path}: {str(e)}")
    
    return results


def batch_resize(input_dir: str, output_dir: str, width: int, height: int,
                 pattern: str = '*.*', maintain_aspect: bool = False) -> Dict[str, Any]:
    """
    批量调整图像大小。
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        width: 目标宽度
        height: 目标高度
        pattern: 文件匹配模式
        maintain_aspect: 是否保持宽高比
    
    Returns:
        处理结果统计
    
    Example:
        >>> batch_resize('photos/', 'thumbnails/', 200, 200)
    """
    import glob
    
    results = {
        'processed': 0,
        'failed': 0,
        'errors': [],
    }
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 支持的图像扩展名
    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
    
    for file_path in glob.glob(os.path.join(input_dir, pattern)):
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in image_exts:
            continue
        
        try:
            filename = os.path.basename(file_path)
            output_path = os.path.join(output_dir, filename)
            
            resize_image(file_path, width, height, output_path, maintain_aspect=maintain_aspect)
            results['processed'] += 1
        except Exception as e:
            results['failed'] += 1
            results['errors'].append(f"{file_path}: {str(e)}")
    
    return results


def batch_convert(input_dir: str, output_dir: str, target_format: str,
                  pattern: str = '*.*', quality: int = 90) -> Dict[str, Any]:
    """
    批量转换图像格式。
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        target_format: 目标格式
        pattern: 文件匹配模式
        quality: 质量（JPEG/WebP）
    
    Returns:
        处理结果统计
    
    Example:
        >>> batch_convert('photos/', 'converted/', 'webp')
    """
    import glob
    
    results = {
        'processed': 0,
        'failed': 0,
        'errors': [],
    }
    
    os.makedirs(output_dir, exist_ok=True)
    
    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
    
    for file_path in glob.glob(os.path.join(input_dir, pattern)):
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in image_exts:
            continue
        
        try:
            filename = os.path.basename(file_path)
            name, _ = os.path.splitext(filename)
            
            ext_map = {
                'jpg': '.jpg', 'jpeg': '.jpg', 'png': '.png',
                'gif': '.gif', 'bmp': '.bmp', 'webp': '.webp',
                'tiff': '.tiff', 'tif': '.tiff',
            }
            new_ext = ext_map.get(target_format.lower(), f'.{target_format.lower()}')
            
            output_path = os.path.join(output_dir, f"{name}{new_ext}")
            
            convert_format(file_path, target_format, output_path, quality)
            results['processed'] += 1
        except Exception as e:
            results['failed'] += 1
            results['errors'].append(f"{file_path}: {str(e)}")
    
    return results


# =============================================================================
# 便捷函数（模块级）
# =============================================================================

def open_image(source: Union[str, bytes]):
    """打开图像并返回 Pillow Image 对象（如果 Pillow 可用）。"""
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库")
    if isinstance(source, bytes):
        return Image.open(io.BytesIO(source))
    return Image.open(source)


def save_image(img, output_path: str, format: Optional[str] = None, **kwargs):
    """保存 Pillow Image 对象到文件。"""
    if not _PILLOW_AVAILABLE:
        raise RuntimeError("需要 Pillow 库")
    img.save(output_path, format=format, **kwargs)


# =============================================================================
# 模块信息
# =============================================================================

def get_version() -> str:
    """获取模块版本。"""
    return "1.0.0"


def is_pillow_available() -> bool:
    """检查 Pillow 是否可用。"""
    return _PILLOW_AVAILABLE


def get_supported_formats() -> List[str]:
    """获取支持的图像格式列表。"""
    if _PILLOW_AVAILABLE:
        formats = ['PNG', 'JPEG', 'GIF', 'BMP', 'WebP', 'TIFF', 'ICO', 'PPM']
        # 添加 Pillow 支持的其他格式
        if hasattr(Image, 'registered_extensions'):
            for ext, fmt in Image.registered_extensions().items():
                if fmt not in formats:
                    formats.append(fmt)
        return sorted(formats)
    else:
        return ['PNG', 'JPEG', 'GIF', 'BMP', 'WebP']  # 标准库支持


# =============================================================================
# 主程序入口（用于测试）
# =============================================================================

if __name__ == '__main__':
    print(f"Image Utils v{get_version()}")
    print(f"Pillow 可用：{is_pillow_available()}")
    print(f"支持的格式：{', '.join(get_supported_formats())}")
    
    # 简单测试
    print("\n运行基本测试...")
    
    # 测试图像信息读取（创建一个简单的测试）
    try:
        # 创建一个测试 PNG 数据（1x1 红色像素）
        test_png = (
            b'\x89PNG\r\n\x1a\n'
            b'\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02'
            b'\x00\x00\x00\x90wS\xde'
            b'\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N'
            b'\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        info = get_image_info(test_png)
        print(f"✓ 图像信息读取：{info}")
    except Exception as e:
        print(f"✗ 图像信息读取失败：{e}")
    
    print("\n模块加载成功！")
