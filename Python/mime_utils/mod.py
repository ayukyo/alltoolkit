"""
MIME 类型处理工具模块

提供 MIME 类型的查询、转换和判断功能。
零外部依赖，纯 Python 标准库实现。

功能：
- 根据文件扩展名获取 MIME 类型
- 根据 MIME 类型获取文件扩展名
- 判断 MIME 类型类别（图片、视频、音频、文档等）
- 解析和生成 Content-Type 头
- 生成 Content-Disposition 头
"""

import mimetypes
from typing import Optional, Tuple, List, Dict, Set
from urllib.parse import quote


# 初始化 mimetypes
mimetypes.init()

# 扩展 MIME 类型映射（补充标准库不包含的类型）
EXTENDED_MIME_TYPES: Dict[str, str] = {
    # 文档类型
    '.md': 'text/markdown',
    '.markdown': 'text/markdown',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    '.doc': 'application/msword',
    '.xls': 'application/vnd.ms-excel',
    '.ppt': 'application/vnd.ms-powerpoint',
    
    # 压缩文件
    '.7z': 'application/x-7z-compressed',
    '.rar': 'application/vnd.rar',
    '.tar': 'application/x-tar',
    '.gz': 'application/gzip',
    '.bz2': 'application/x-bzip2',
    '.xz': 'application/x-xz',
    
    # 音频类型
    '.m4a': 'audio/mp4',
    '.aac': 'audio/aac',
    '.flac': 'audio/flac',
    '.wma': 'audio/x-ms-wma',
    '.ogg': 'audio/ogg',
    '.opus': 'audio/opus',
    
    # 视频类型
    '.mkv': 'video/x-matroska',
    '.avi': 'video/x-msvideo',
    '.mov': 'video/quicktime',
    '.wmv': 'video/x-ms-wmv',
    '.flv': 'video/x-flv',
    '.webm': 'video/webm',
    
    # 字体类型
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
    '.otf': 'font/otf',
    '.eot': 'application/vnd.ms-fontobject',
    
    # 代码文件
    '.js': 'application/javascript',
    '.mjs': 'application/javascript',
    '.ts': 'application/typescript',
    '.jsx': 'text/jsx',
    '.tsx': 'text/tsx',
    '.vue': 'text/x-vue',
    '.py': 'text/x-python',
    '.rb': 'text/x-ruby',
    '.go': 'text/x-go',
    '.rs': 'text/x-rust',
    '.java': 'text/x-java',
    '.kt': 'text/x-kotlin',
    '.swift': 'text/x-swift',
    '.c': 'text/x-c',
    '.cpp': 'text/x-c++',
    '.h': 'text/x-c',
    '.hpp': 'text/x-c++',
    '.cs': 'text/x-csharp',
    '.php': 'text/x-php',
    '.sh': 'text/x-shellscript',
    '.bash': 'text/x-shellscript',
    '.zsh': 'text/x-shellscript',
    '.ps1': 'text/x-powershell',
    '.lua': 'text/x-lua',
    '.r': 'text/x-r',
    '.sql': 'application/sql',
    
    # 配置文件
    '.json': 'application/json',
    '.yaml': 'application/x-yaml',
    '.yml': 'application/x-yaml',
    '.toml': 'application/toml',
    '.ini': 'text/plain',
    '.conf': 'text/plain',
    '.env': 'text/plain',
    
    # 数据文件
    '.csv': 'text/csv',
    '.xml': 'application/xml',
    '.svg': 'image/svg+xml',
    
    # 其他
    '.wasm': 'application/wasm',
    '.webmanifest': 'application/manifest+json',
    '.map': 'application/json',
    '.ics': 'text/calendar',
    '.vcf': 'text/vcard',
    '.epub': 'application/epub+zip',
    '.mobi': 'application/x-mobipocket-ebook',
    '.torrent': 'application/x-bittorrent',
    '.dmg': 'application/x-apple-diskimage',
    '.iso': 'application/x-iso9660-image',
    '.apk': 'application/vnd.android.package-archive',
    '.ipa': 'application/octet-stream',
}

# MIME 类型到扩展名的反向映射（手动指定优先顺序）
MIME_TO_EXTENSIONS: Dict[str, List[str]] = {
    # 图片类型（常见扩展名优先）
    'image/jpeg': ['.jpeg', '.jpg', '.jpe'],
    'image/png': ['.png'],
    'image/gif': ['.gif'],
    'image/webp': ['.webp'],
    'image/svg+xml': ['.svg', '.svgz'],
    'image/bmp': ['.bmp'],
    'image/tiff': ['.tiff', '.tif'],
    'image/x-icon': ['.ico'],
    
    # 文档类型
    'application/pdf': ['.pdf'],
    'application/json': ['.json'],
    'text/markdown': ['.md', '.markdown'],
    'text/plain': ['.txt'],
    'text/html': ['.html', '.htm'],
    'text/css': ['.css'],
    'text/csv': ['.csv'],
    'application/xml': ['.xml'],
    'application/rtf': ['.rtf'],
    
    # Office 文档
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
    'application/msword': ['.doc'],
    'application/vnd.ms-excel': ['.xls'],
    'application/vnd.ms-powerpoint': ['.ppt'],
    
    # 音频类型
    'audio/mpeg': ['.mp3', '.mpeg'],
    'audio/mp4': ['.m4a', '.mp4a'],
    'audio/wav': ['.wav'],
    'audio/flac': ['.flac'],
    'audio/ogg': ['.ogg'],
    'audio/aac': ['.aac'],
    
    # 视频类型
    'video/mp4': ['.mp4', '.m4v'],
    'video/webm': ['.webm'],
    'video/x-matroska': ['.mkv'],
    'video/quicktime': ['.mov'],
    'video/x-msvideo': ['.avi'],
    'video/x-ms-wmv': ['.wmv'],
    'video/mpeg': ['.mpeg', '.mpg'],
    
    # 压缩文件
    'application/zip': ['.zip'],
    'application/x-7z-compressed': ['.7z'],
    'application/vnd.rar': ['.rar'],
    'application/x-tar': ['.tar'],
    'application/gzip': ['.gz'],
    'application/x-bzip2': ['.bz2'],
    'application/x-xz': ['.xz'],
    
    # 代码文件
    'application/javascript': ['.js', '.mjs'],
    'application/typescript': ['.ts'],
    'text/x-python': ['.py'],
    'text/x-java': ['.java'],
    'text/x-c': ['.c', '.h'],
    'text/x-c++': ['.cpp', '.hpp'],
    'text/x-csharp': ['.cs'],
    'text/x-go': ['.go'],
    'text/x-rust': ['.rs'],
    'text/x-ruby': ['.rb'],
    'text/x-php': ['.php'],
    'text/x-shellscript': ['.sh', '.bash'],
    'application/sql': ['.sql'],
    
    # 配置文件
    'application/x-yaml': ['.yaml', '.yml'],
    'application/toml': ['.toml'],
    
    # 字体
    'font/woff': ['.woff'],
    'font/woff2': ['.woff2'],
    'font/ttf': ['.ttf'],
    'font/otf': ['.otf'],
}

# 补充其他映射
for ext, mime in EXTENDED_MIME_TYPES.items():
    if mime not in MIME_TO_EXTENSIONS:
        MIME_TO_EXTENSIONS[mime] = []
    if ext not in MIME_TO_EXTENSIONS[mime]:
        MIME_TO_EXTENSIONS[mime].append(ext)

# MIME 类别分组
MIME_CATEGORIES: Dict[str, Set[str]] = {
    'image': {
        'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml',
        'image/bmp', 'image/tiff', 'image/x-icon', 'image/ico', 'image/avif',
        'image/heic', 'image/heif', 'image/jxl'
    },
    'video': {
        'video/mp4', 'video/mpeg', 'video/quicktime', 'video/x-msvideo',
        'video/x-ms-wmv', 'video/x-flv', 'video/webm', 'video/x-matroska',
        'video/3gpp', 'video/3gpp2', 'video/mp2t'
    },
    'audio': {
        'audio/mpeg', 'audio/mp3', 'audio/mp4', 'audio/aac', 'audio/flac',
        'audio/wav', 'audio/x-wav', 'audio/ogg', 'audio/opus', 'audio/vorbis',
        'audio/x-ms-wma', 'audio/midi', 'audio/x-midi'
    },
    'document': {
        'application/pdf', 'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/vnd.ms-excel', 'application/vnd.ms-powerpoint',
        'application/rtf', 'text/rtf', 'application/epub+zip',
        'application/x-mobipocket-ebook'
    },
    'text': {
        'text/plain', 'text/html', 'text/css', 'text/csv', 'text/xml',
        'text/javascript', 'text/markdown', 'text/calendar', 'text/vcard',
        'application/javascript', 'application/json', 'application/xml',
        'application/x-yaml', 'application/toml', 'application/sql'
    },
    'archive': {
        'application/zip', 'application/x-zip-compressed',
        'application/x-rar-compressed', 'application/vnd.rar',
        'application/x-7z-compressed', 'application/x-tar',
        'application/gzip', 'application/x-bzip2', 'application/x-xz',
        'application/x-compress'
    },
    'code': {
        'application/javascript', 'application/typescript', 'application/sql',
        'text/x-python', 'text/x-ruby', 'text/x-go', 'text/x-rust',
        'text/x-java', 'text/x-kotlin', 'text/x-swift', 'text/x-c',
        'text/x-c++', 'text/x-csharp', 'text/x-php', 'text/x-shellscript',
        'text/x-powershell', 'text/x-lua', 'text/x-r', 'text/jsx', 'text/tsx',
        'text/x-vue'
    },
    'binary': {
        'application/octet-stream', 'application/wasm',
        'application/vnd.android.package-archive'
    }
}


def get_mime_type(filename_or_ext: str, default: str = 'application/octet-stream') -> str:
    """
    根据文件名或扩展名获取 MIME 类型
    
    Args:
        filename_or_ext: 文件名或扩展名（带或不带点）
        default: 未找到时的默认返回值
        
    Returns:
        MIME 类型字符串
        
    Examples:
        >>> get_mime_type('image.png')
        'image/png'
        >>> get_mime_type('.jpg')
        'image/jpeg'
        >>> get_mime_type('document')
        'application/octet-stream'
    """
    # 提取扩展名
    if '.' not in filename_or_ext:
        ext = '.' + filename_or_ext if not filename_or_ext.startswith('.') else filename_or_ext
    else:
        ext = '.' + filename_or_ext.rsplit('.', 1)[-1]
    
    ext = ext.lower()
    
    # 先查扩展映射
    if ext in EXTENDED_MIME_TYPES:
        return EXTENDED_MIME_TYPES[ext]
    
    # 再查标准库
    mime_type, _ = mimetypes.guess_type(f'file{ext}')
    
    return mime_type if mime_type else default


def get_extension(mime_type: str, default: str = '.bin') -> str:
    """
    根据 MIME 类型获取主要文件扩展名
    
    Args:
        mime_type: MIME 类型字符串
        default: 未找到时的默认返回值
        
    Returns:
        文件扩展名（带点）
        
    Examples:
        >>> get_extension('image/png')
        '.png'
        >>> get_extension('application/json')
        '.json'
    """
    mime_type = mime_type.lower().split(';')[0].strip()
    
    # 先查扩展映射
    if mime_type in MIME_TO_EXTENSIONS:
        return MIME_TO_EXTENSIONS[mime_type][0]
    
    # 查标准库
    ext = mimetypes.guess_extension(mime_type)
    
    return ext if ext else default


def get_extensions(mime_type: str) -> List[str]:
    """
    根据 MIME 类型获取所有可能的文件扩展名
    
    Args:
        mime_type: MIME 类型字符串
        
    Returns:
        文件扩展名列表（带点）
        
    Examples:
        >>> get_extensions('image/jpeg')
        ['.jpeg', '.jpg', '.jpe']
    """
    mime_type = mime_type.lower().split(';')[0].strip()
    
    extensions = []
    
    # 查扩展映射
    if mime_type in MIME_TO_EXTENSIONS:
        extensions.extend(MIME_TO_EXTENSIONS[mime_type])
    
    # 查标准库
    std_exts = mimetypes.guess_all_extensions(mime_type)
    for ext in std_exts:
        if ext not in extensions:
            extensions.append(ext)
    
    return extensions


def is_category(mime_type: str, category: str) -> bool:
    """
    判断 MIME 类型是否属于某类别
    
    Args:
        mime_type: MIME 类型字符串
        category: 类别名称（image/video/audio/document/text/archive/code/binary）
        
    Returns:
        是否属于该类别
        
    Examples:
        >>> is_category('image/png', 'image')
        True
        >>> is_category('video/mp4', 'video')
        True
        >>> is_category('image/png', 'video')
        False
    """
    mime_type = mime_type.lower().split(';')[0].strip()
    category = category.lower()
    
    if category not in MIME_CATEGORIES:
        return False
    
    return mime_type in MIME_CATEGORIES[category]


def get_category(mime_type: str) -> Optional[str]:
    """
    获取 MIME 类型的所属类别
    
    Args:
        mime_type: MIME 类型字符串
        
    Returns:
        类别名称，未知则返回 None
        
    Examples:
        >>> get_category('image/png')
        'image'
        >>> get_category('application/pdf')
        'document'
    """
    mime_type = mime_type.lower().split(';')[0].strip()
    
    for category, types in MIME_CATEGORIES.items():
        if mime_type in types:
            return category
    
    return None


def is_image(mime_type: str) -> bool:
    """判断是否为图片类型"""
    return is_category(mime_type, 'image')


def is_video(mime_type: str) -> bool:
    """判断是否为视频类型"""
    return is_category(mime_type, 'video')


def is_audio(mime_type: str) -> bool:
    """判断是否为音频类型"""
    return is_category(mime_type, 'audio')


def is_document(mime_type: str) -> bool:
    """判断是否为文档类型"""
    return is_category(mime_type, 'document')


def is_text(mime_type: str) -> bool:
    """判断是否为文本类型"""
    return is_category(mime_type, 'text')


def is_archive(mime_type: str) -> bool:
    """判断是否为压缩包类型"""
    return is_category(mime_type, 'archive')


def is_code(mime_type: str) -> bool:
    """判断是否为代码文件类型"""
    return is_category(mime_type, 'code')


def is_binary(mime_type: str) -> bool:
    """判断是否为二进制类型"""
    return is_category(mime_type, 'binary')


def parse_content_type(content_type: str) -> Tuple[str, Dict[str, str]]:
    """
    解析 Content-Type 头
    
    Args:
        content_type: Content-Type 字符串，如 'text/html; charset=utf-8'
        
    Returns:
        元组：(mime_type, params)
        
    Examples:
        >>> parse_content_type('text/html; charset=utf-8')
        ('text/html', {'charset': 'utf-8'})
        >>> parse_content_type('multipart/form-data; boundary=----WebKitFormBoundary')
        ('multipart/form-data', {'boundary': '----WebKitFormBoundary'})
    """
    parts = content_type.split(';')
    mime_type = parts[0].strip().lower()
    
    params = {}
    for part in parts[1:]:
        part = part.strip()
        if '=' in part:
            key, value = part.split('=', 1)
            key = key.strip().lower()
            value = value.strip()
            # 移除引号
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            params[key] = value
    
    return mime_type, params


def build_content_type(
    mime_type: str,
    charset: Optional[str] = None,
    boundary: Optional[str] = None,
    **params: str
) -> str:
    """
    构建 Content-Type 头
    
    Args:
        mime_type: MIME 类型
        charset: 字符编码
        boundary: multipart 边界字符串
        **params: 其他参数
        
    Returns:
        Content-Type 字符串
        
    Examples:
        >>> build_content_type('text/html', charset='utf-8')
        'text/html; charset=utf-8'
        >>> build_content_type('multipart/form-data', boundary='----WebKitFormBoundary')
        'multipart/form-data; boundary=----WebKitFormBoundary'
    """
    parts = [mime_type]
    
    if charset:
        parts.append(f'charset={charset}')
    
    if boundary:
        parts.append(f'boundary={boundary}')
    
    for key, value in params.items():
        # 如果值包含特殊字符，用引号包裹
        if any(c in value for c in ' ;"\''):
            parts.append(f'{key}="{value}"')
        else:
            parts.append(f'{key}={value}')
    
    return '; '.join(parts)


def build_content_disposition(
    filename: str,
    disposition: str = 'attachment',
    encode_filename: bool = True
) -> str:
    """
    构建 Content-Disposition 头
    
    Args:
        filename: 文件名
        disposition: 处置方式（attachment/inline）
        encode_filename: 是否编码文件名（推荐 True，兼容中文等）
        
    Returns:
        Content-Disposition 字符串
        
    Examples:
        >>> build_content_disposition('report.pdf')
        'attachment; filename="report.pdf"'
        >>> build_content_disposition('报告.pdf', encode_filename=True)
        'attachment; filename="%E6%8A%A5%E5%91%8A.pdf"; filename*=UTF-8\'\'%E6%8A%A5%E5%91%8A.pdf'
    """
    if encode_filename:
        # RFC 5987 编码方式，兼容中文等
        encoded = quote(filename, safe='')
        return f"{disposition}; filename=\"{encoded}\"; filename*=UTF-8''{encoded}"
    else:
        return f'{disposition}; filename="{filename}"'


def guess_type_from_content(content: bytes) -> Optional[str]:
    """
    根据文件内容前几个字节猜测 MIME 类型（魔数检测）
    
    Args:
        content: 文件内容（至少前几个字节）
        
    Returns:
        猜测的 MIME 类型，无法识别则返回 None
        
    Examples:
        >>> guess_type_from_content(b'\\x89PNG\\r\\n\\x1a\\n')
        'image/png'
        >>> guess_type_from_content(b'%PDF')
        'application/pdf'
    """
    if not content:
        return None
    
    # 魔数签名表
    signatures = [
        # 图片
        (b'\x89PNG\r\n\x1a\n', 'image/png'),
        (b'\xff\xd8\xff', 'image/jpeg'),
        (b'GIF87a', 'image/gif'),
        (b'GIF89a', 'image/gif'),
        (b'RIFF', 'image/webp'),  # 需要进一步确认，先标记为 webp
        (b'BM', 'image/bmp'),
        (b'II*\x00', 'image/tiff'),  # TIFF little endian
        (b'MM\x00*', 'image/tiff'),  # TIFF big endian
        (b'\x00\x00\x01\x00', 'image/x-icon'),  # ICO
        
        # 文档
        (b'%PDF', 'application/pdf'),
        (b'PK\x03\x04', 'application/zip'),  # ZIP, DOCX, XLSX 等
        
        # 视频
        (b'\x00\x00\x00\x1cftyp', 'video/mp4'),  # MP4
        (b'\x00\x00\x00\x20ftyp', 'video/mp4'),
        (b'\x1aE\xdf\xa3', 'video/webm'),  # WebM/MKV
        (b'RIFF', 'video/webp'),  # 可能是 AVI 或 WebP
        
        # 音频
        (b'ID3', 'audio/mpeg'),  # MP3 with ID3
        (b'\xff\xfb', 'audio/mpeg'),  # MP3 frame sync
        (b'\xff\xfa', 'audio/mpeg'),
        (b'\xff\xf3', 'audio/mpeg'),
        (b'\xff\xf2', 'audio/mpeg'),
        (b'fLaC', 'audio/flac'),
        (b'OggS', 'audio/ogg'),
        
        # 压缩包
        (b'Rar!\x1a\x07', 'application/vnd.rar'),
        (b'7z\xbc\xaf\x27\x1c', 'application/x-7z-compressed'),
        (b'\x1f\x8b', 'application/gzip'),
        (b'BZh', 'application/x-bzip2'),
        
        # 可执行文件
        (b'MZ', 'application/x-dosexec'),  # Windows EXE
        (b'\x7fELF', 'application/x-elf'),  # Linux ELF
        
        # 其他
        (b'\x00\x00\x01\x00', 'image/x-icon'),
    ]
    
    # 特殊检测：SVG（XML格式）
    if content.startswith(b'<?xml') or content.startswith(b'<svg'):
        try:
            text = content[:100].decode('utf-8', errors='ignore').lower()
            if '<svg' in text:
                return 'image/svg+xml'
        except:
            pass
    
    # 匹配签名
    for sig, mime in signatures:
        if content.startswith(sig):
            # ZIP 文件进一步检测
            if sig == b'PK\x03\x04':
                try:
                    # 检查是否为 Office 文档
                    if len(content) > 100:
                        content_str = content[:200].decode('utf-8', errors='ignore')
                        if 'word/' in content_str or 'document.xml' in content_str:
                            return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                        if 'xl/' in content_str or 'workbook.xml' in content_str:
                            return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        if 'ppt/' in content_str or 'presentation.xml' in content_str:
                            return 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
                except:
                    pass
                return 'application/zip'
            return mime
    
    # 检查是否为文本
    try:
        content[:1000].decode('utf-8')
        return 'text/plain'
    except:
        pass
    
    return None


def get_mime_info(mime_type: str) -> Dict[str, any]:
    """
    获取 MIME 类型的详细信息
    
    Args:
        mime_type: MIME 类型字符串
        
    Returns:
        包含类型信息的字典
        
    Examples:
        >>> info = get_mime_info('image/png')
        >>> info['category']
        'image'
        >>> info['extensions']
        ['.png']
    """
    mime_type = mime_type.lower().split(';')[0].strip()
    
    extensions = get_extensions(mime_type)
    category = get_category(mime_type)
    
    # 判断是否为文本可读
    text_readable = category in ('text', 'code') or mime_type.startswith('text/')
    
    # 判断是否可内联显示
    inline_displayable = category in ('image', 'text', 'code') or mime_type == 'application/pdf'
    
    return {
        'mime_type': mime_type,
        'extensions': extensions,
        'primary_extension': extensions[0] if extensions else None,
        'category': category,
        'is_image': is_image(mime_type),
        'is_video': is_video(mime_type),
        'is_audio': is_audio(mime_type),
        'is_document': is_document(mime_type),
        'is_text': is_text(mime_type),
        'is_archive': is_archive(mime_type),
        'is_code': is_code(mime_type),
        'is_binary': is_binary(mime_type),
        'text_readable': text_readable,
        'inline_displayable': inline_displayable,
    }


class MimeTypeRegistry:
    """
    MIME 类型注册表
    
    允许注册自定义 MIME 类型映射
    
    Examples:
        >>> registry = MimeTypeRegistry()
        >>> registry.register('.custom', 'application/x-custom')
        >>> registry.get_mime_type('file.custom')
        'application/x-custom'
    """
    
    def __init__(self):
        self._ext_to_mime: Dict[str, str] = {}
        self._mime_to_ext: Dict[str, List[str]] = {}
    
    def register(self, extension: str, mime_type: str) -> None:
        """
        注册扩展名到 MIME 类型的映射
        
        Args:
            extension: 文件扩展名（带或不带点）
            mime_type: MIME 类型
        """
        if not extension.startswith('.'):
            extension = '.' + extension
        
        extension = extension.lower()
        mime_type = mime_type.lower()
        
        self._ext_to_mime[extension] = mime_type
        
        if mime_type not in self._mime_to_ext:
            self._mime_to_ext[mime_type] = []
        if extension not in self._mime_to_ext[mime_type]:
            self._mime_to_ext[mime_type].append(extension)
    
    def unregister_extension(self, extension: str) -> bool:
        """注销扩展名映射"""
        if not extension.startswith('.'):
            extension = '.' + extension
        
        extension = extension.lower()
        
        if extension in self._ext_to_mime:
            mime_type = self._ext_to_mime.pop(extension)
            if mime_type in self._mime_to_ext:
                self._mime_to_ext[mime_type] = [
                    ext for ext in self._mime_to_ext[mime_type] if ext != extension
                ]
            return True
        return False
    
    def get_mime_type(self, filename_or_ext: str, default: str = 'application/octet-stream') -> str:
        """根据文件名或扩展名获取 MIME 类型"""
        if '.' not in filename_or_ext:
            ext = '.' + filename_or_ext
        else:
            ext = '.' + filename_or_ext.rsplit('.', 1)[-1]
        
        ext = ext.lower()
        
        # 先查注册表
        if ext in self._ext_to_mime:
            return self._ext_to_mime[ext]
        
        # 回退到全局函数
        return get_mime_type(filename_or_ext, default)
    
    def get_extension(self, mime_type: str, default: str = '.bin') -> str:
        """根据 MIME 类型获取扩展名"""
        mime_type = mime_type.lower().split(';')[0].strip()
        
        # 先查注册表
        if mime_type in self._mime_to_ext and self._mime_to_ext[mime_type]:
            return self._mime_to_ext[mime_type][0]
        
        # 回退到全局函数
        return get_extension(mime_type, default)
    
    def get_extensions(self, mime_type: str) -> List[str]:
        """根据 MIME 类型获取所有扩展名"""
        mime_type = mime_type.lower().split(';')[0].strip()
        
        extensions = list(self._mime_to_ext.get(mime_type, []))
        
        # 合并全局结果
        for ext in get_extensions(mime_type):
            if ext not in extensions:
                extensions.append(ext)
        
        return extensions
    
    def list_all(self) -> Dict[str, str]:
        """列出所有已注册的映射"""
        return dict(self._ext_to_mime)


# 模块级默认注册表实例
default_registry = MimeTypeRegistry()