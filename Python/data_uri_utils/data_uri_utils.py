"""
Data URI Utilities - Data URI 编码/解码工具

功能：
- 将文件编码为 Data URI 格式
- 从 Data URI 解码提取数据
- 自动检测 MIME 类型
- 支持文本和二进制数据
- Base64 编码支持
- Data URI 验证和解析
"""

import base64
import mimetypes
import os
import re
from dataclasses import dataclass
from typing import Optional, Tuple, Union


@dataclass
class DataURI:
    """Data URI 解析结果"""
    mime_type: str
    encoding: Optional[str]  # 'base64' or None
    data: bytes
    original_size: int  # 原始数据大小
    encoded_size: int   # 编码后大小
    
    @property
    def is_base64(self) -> bool:
        return self.encoding == 'base64'
    
    @property
    def is_text(self) -> bool:
        return self.mime_type.startswith('text/') or self.mime_type in (
            'application/json',
            'application/xml',
            'application/javascript',
        )
    
    def decode_text(self, encoding: str = 'utf-8') -> str:
        """将数据解码为文本"""
        return self.data.decode(encoding)
    
    def __repr__(self) -> str:
        return (
            f"DataURI(mime_type={self.mime_type!r}, "
            f"encoding={self.encoding!r}, "
            f"size={self.original_size} bytes)"
        )


# 常用 MIME 类型映射
MIME_MAP = {
    # 图片
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.bmp': 'image/bmp',
    # 文档
    '.pdf': 'application/pdf',
    '.doc': 'application/msword',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.xls': 'application/vnd.ms-excel',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    # 音频
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.ogg': 'audio/ogg',
    '.m4a': 'audio/mp4',
    # 视频
    '.mp4': 'video/mp4',
    '.webm': 'video/webm',
    '.avi': 'video/x-msvideo',
    '.mov': 'video/quicktime',
    # 文本/代码
    '.txt': 'text/plain',
    '.html': 'text/html',
    '.htm': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.mjs': 'application/javascript',
    '.json': 'application/json',
    '.xml': 'application/xml',
    '.csv': 'text/csv',
    '.md': 'text/markdown',
    '.rtf': 'application/rtf',
    # 字体
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
    '.otf': 'font/otf',
    '.eot': 'application/vnd.ms-fontobject',
    # 压缩
    '.zip': 'application/zip',
    '.gz': 'application/gzip',
    '.tar': 'application/x-tar',
    '.rar': 'application/vnd.rar',
    '.7z': 'application/x-7z-compressed',
    # 其他
    '.bin': 'application/octet-stream',
}


def get_mime_type(file_path: str) -> str:
    """
    根据文件扩展名获取 MIME 类型
    
    Args:
        file_path: 文件路径
        
    Returns:
        MIME 类型字符串
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    # 优先使用自定义映射
    if ext in MIME_MAP:
        return MIME_MAP[ext]
    
    # 使用 mimetypes 模块
    mime_type, _ = mimetypes.guess_type(file_path)
    
    return mime_type or 'application/octet-stream'


def encode_file(
    file_path: str,
    mime_type: Optional[str] = None,
    use_base64: bool = True,
) -> str:
    """
    将文件编码为 Data URI
    
    Args:
        file_path: 文件路径
        mime_type: MIME 类型（可选，自动检测）
        use_base64: 是否使用 base64 编码（对二进制文件默认 True）
        
    Returns:
        Data URI 字符串
        
    Raises:
        FileNotFoundError: 文件不存在
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    # 获取 MIME 类型
    if mime_type is None:
        mime_type = get_mime_type(file_path)
    
    # 读取文件内容
    with open(file_path, 'rb') as f:
        data = f.read()
    
    return encode_data(data, mime_type, use_base64)


def encode_data(
    data: Union[bytes, str],
    mime_type: str = 'application/octet-stream',
    use_base64: bool = True,
) -> str:
    """
    将数据编码为 Data URI
    
    Args:
        data: 要编码的数据（字节或字符串）
        mime_type: MIME 类型
        use_base64: 是否使用 base64 编码
        
    Returns:
        Data URI 字符串
    """
    # 转换为字节
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # 判断是否为文本类型
    is_text_mime = (
        mime_type.startswith('text/') or
        mime_type in ('application/json', 'application/javascript', 'application/xml')
    )
    
    # 文本类型且不需要 base64
    if is_text_mime and not use_base64:
        # URL 编码特殊字符
        text = data.decode('utf-8')
        # 对于简单 ASCII 文本，直接编码
        encoded = text  # 简化处理，实际可使用 urllib.parse.quote
        return f"data:{mime_type},{encoded}"
    
    # 使用 base64 编码
    encoded = base64.b64encode(data).decode('ascii')
    return f"data:{mime_type};base64,{encoded}"


def decode_data_uri(data_uri: str) -> DataURI:
    """
    从 Data URI 解码数据
    
    Args:
        data_uri: Data URI 字符串
        
    Returns:
        DataURI 对象
        
    Raises:
        ValueError: 无效的 Data URI
    """
    # 验证格式
    if not data_uri.startswith('data:'):
        raise ValueError("无效的 Data URI: 必须以 'data:' 开头")
    
    # 解析头部
    # 格式: data:[<mediatype>][;base64],<data>
    header_end = data_uri.find(',')
    if header_end == -1:
        raise ValueError("无效的 Data URI: 缺少数据部分")
    
    header = data_uri[5:header_end]  # 去掉 'data:'
    data_part = data_uri[header_end + 1:]
    
    # 解析 MIME 类型和编码
    parts = header.split(';')
    mime_type = parts[0] if parts[0] else 'text/plain'
    encoding = None
    
    if len(parts) > 1:
        for part in parts[1:]:
            if part == 'base64':
                encoding = 'base64'
                break
    
    # 解码数据
    if encoding == 'base64':
        try:
            data = base64.b64decode(data_part)
        except Exception as e:
            raise ValueError(f"Base64 解码失败: {e}")
    else:
        # 对于文本数据，需要处理 URL 编码
        from urllib.parse import unquote
        data = unquote(data_part).encode('utf-8')
    
    return DataURI(
        mime_type=mime_type,
        encoding=encoding,
        data=data,
        original_size=len(data),
        encoded_size=len(data_part),
    )


def decode_to_file(
    data_uri: str,
    output_path: str,
    mime_type: Optional[str] = None,
) -> str:
    """
    将 Data URI 解码并保存为文件
    
    Args:
        data_uri: Data URI 字符串
        output_path: 输出文件路径（可以是目录）
        mime_type: 强制指定 MIME 类型（可选）
        
    Returns:
        实际保存的文件路径
    """
    parsed = decode_data_uri(data_uri)
    
    # 如果强制指定 MIME 类型
    if mime_type:
        parsed.mime_type = mime_type
    
    # 确定输出路径
    if os.path.isdir(output_path):
        # 根据 MIME 类型推断扩展名
        ext = get_extension(parsed.mime_type)
        output_path = os.path.join(output_path, f"decoded_file{ext}")
    
    # 确保目录存在
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # 写入文件
    with open(output_path, 'wb') as f:
        f.write(parsed.data)
    
    return output_path


def get_extension(mime_type: str) -> str:
    """
    根据 MIME 类型获取文件扩展名
    
    Args:
        mime_type: MIME 类型
        
    Returns:
        文件扩展名（带点，如 '.png'）
    """
    # 反向查找
    for ext, mt in MIME_MAP.items():
        if mt == mime_type:
            return ext
    
    # 使用 mimetypes 模块
    ext = mimetypes.guess_extension(mime_type)
    if ext:
        return ext
    
    return '.bin'


def is_data_uri(text: str) -> bool:
    """
    检查字符串是否为有效的 Data URI
    
    Args:
        text: 要检查的字符串
        
    Returns:
        是否为有效的 Data URI
    """
    if not text or not text.startswith('data:'):
        return False
    
    try:
        # 尝试解析
        decode_data_uri(text)
        return True
    except ValueError:
        return False


def get_info(data_uri: str) -> dict:
    """
    获取 Data URI 的详细信息
    
    Args:
        data_uri: Data URI 字符串
        
    Returns:
        包含详细信息的字典
    """
    parsed = decode_data_uri(data_uri)
    
    return {
        'mime_type': parsed.mime_type,
        'encoding': parsed.encoding,
        'original_size': parsed.original_size,
        'encoded_size': parsed.encoded_size,
        'overhead_ratio': parsed.encoded_size / parsed.original_size if parsed.original_size > 0 else 0,
        'is_base64': parsed.is_base64,
        'is_text': parsed.is_text,
        'extension': get_extension(parsed.mime_type),
    }


def estimate_size(
    data_size: int,
    mime_type: str = 'application/octet-stream',
    use_base64: bool = True,
) -> int:
    """
    估算 Data URI 编码后的大小
    
    Args:
        data_size: 原始数据大小（字节）
        mime_type: MIME 类型
        use_base64: 是否使用 base64 编码
        
    Returns:
        估算的 Data URI 大小
    """
    # 头部大小: "data:" + mime_type + ";base64," 或 ","
    header_size = 5 + len(mime_type)
    if use_base64:
        header_size += 8  # ";base64,"
    else:
        header_size += 1  # ","
    
    # 数据部分大小
    if use_base64:
        # base64 编码会使数据增大约 33%
        data_encoded_size = (data_size + 2) // 3 * 4
    else:
        # URL 编码最坏情况是每个字符 3 倍
        data_encoded_size = data_size * 3
    
    return header_size + data_encoded_size


def create_html_embed(
    file_path: str,
    tag_type: str = 'auto',
    alt_text: str = '',
    css_class: str = '',
) -> str:
    """
    创建 HTML 嵌入标签
    
    Args:
        file_path: 文件路径
        tag_type: 标签类型 ('auto', 'img', 'audio', 'video', 'source', 'link', 'object')
        alt_text: alt 文本（用于图片）
        css_class: CSS 类名
        
    Returns:
        HTML 标签字符串
    """
    mime_type = get_mime_type(file_path)
    data_uri = encode_file(file_path)
    
    # 自动推断标签类型
    if tag_type == 'auto':
        if mime_type.startswith('image/'):
            tag_type = 'img'
        elif mime_type.startswith('audio/'):
            tag_type = 'audio'
        elif mime_type.startswith('video/'):
            tag_type = 'video'
        elif mime_type == 'text/css':
            tag_type = 'link'
        elif mime_type == 'application/javascript':
            tag_type = 'script'
        else:
            tag_type = 'object'
    
    class_attr = f' class="{css_class}"' if css_class else ''
    alt_attr = f' alt="{alt_text}"' if alt_text else ''
    
    if tag_type == 'img':
        return f'<img src="{data_uri}"{alt_attr}{class_attr}>'
    elif tag_type == 'audio':
        return f'<audio controls{class_attr}><source src="{data_uri}" type="{mime_type}"></audio>'
    elif tag_type == 'video':
        return f'<video controls{class_attr}><source src="{data_uri}" type="{mime_type}"></video>'
    elif tag_type == 'source':
        return f'<source src="{data_uri}" type="{mime_type}">'
    elif tag_type == 'link':
        return f'<link rel="stylesheet" href="{data_uri}"{class_attr}>'
    elif tag_type == 'script':
        return f'<script src="{data_uri}"></script>'
    elif tag_type == 'object':
        return f'<object data="{data_uri}" type="{mime_type}"{class_attr}></object>'
    else:
        return f'<a href="{data_uri}"{class_attr}>Download</a>'


def batch_encode(
    file_paths: list,
    use_base64: bool = True,
    max_size: Optional[int] = None,
) -> dict:
    """
    批量编码文件为 Data URI
    
    Args:
        file_paths: 文件路径列表
        use_base64: 是否使用 base64 编码
        max_size: 最大文件大小限制（字节），超过则跳过
        
    Returns:
        包含成功和失败结果的字典
    """
    results = {
        'success': {},
        'failed': {},
        'skipped': {},
    }
    
    for path in file_paths:
        try:
            # 检查文件大小
            if max_size:
                size = os.path.getsize(path)
                if size > max_size:
                    results['skipped'][path] = f'文件过大 ({size} > {max_size})'
                    continue
            
            data_uri = encode_file(path, use_base64=use_base64)
            results['success'][path] = data_uri
            
        except FileNotFoundError:
            results['failed'][path] = '文件不存在'
        except PermissionError:
            results['failed'][path] = '无权限读取文件'
        except Exception as e:
            results['failed'][path] = str(e)
    
    return results


# 常用数据快捷函数

def text_to_data_uri(text: str, mime_type: str = 'text/plain') -> str:
    """将文本转换为 Data URI"""
    return encode_data(text.encode('utf-8'), mime_type, use_base64=False)


def json_to_data_uri(json_str: str) -> str:
    """将 JSON 字符串转换为 Data URI"""
    return encode_data(json_str.encode('utf-8'), 'application/json', use_base64=True)


def html_to_data_uri(html: str) -> str:
    """将 HTML 转换为 Data URI"""
    return encode_data(html.encode('utf-8'), 'text/html', use_base64=True)


def svg_to_data_uri(svg: str) -> str:
    """将 SVG 字符串转换为 Data URI"""
    return encode_data(svg.encode('utf-8'), 'image/svg+xml', use_base64=True)


if __name__ == '__main__':
    # 演示用法
    print("=== Data URI Utilities 演示 ===\n")
    
    # 1. 文本编码
    text = "Hello, Data URI!"
    text_uri = text_to_data_uri(text)
    print(f"文本 Data URI: {text_uri[:50]}...")
    
    # 2. JSON 编码
    json_str = '{"name": "test", "value": 123}'
    json_uri = json_to_data_uri(json_str)
    print(f"\nJSON Data URI: {json_uri[:50]}...")
    
    # 3. SVG 编码
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><circle cx="50" cy="50" r="40" fill="red"/></svg>'
    svg_uri = svg_to_data_uri(svg)
    print(f"\nSVG Data URI: {svg_uri[:50]}...")
    
    # 4. 解码
    decoded = decode_data_uri(json_uri)
    print(f"\n解码 JSON:")
    print(f"  MIME: {decoded.mime_type}")
    print(f"  数据: {decoded.decode_text()}")
    print(f"  原始大小: {decoded.original_size} bytes")
    
    # 5. 信息查询
    info = get_info(json_uri)
    print(f"\nData URI 信息:")
    for k, v in info.items():
        print(f"  {k}: {v}")
    
    # 6. 大小估算
    estimated = estimate_size(1000, 'image/png', use_base64=True)
    print(f"\n1000 字节数据编码后预估大小: {estimated} bytes")
    
    # 7. 验证
    print(f"\n是否为有效 Data URI: {is_data_uri(json_uri)}")
    print(f"无效 URI 检测: {is_data_uri('not a data uri')}")