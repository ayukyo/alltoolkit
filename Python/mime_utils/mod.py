"""
MIME 类型工具模块
================

提供 MIME 类型的查询、检测和判断功能。
零外部依赖，纯 Python 实现。

功能：
- 根据文件扩展名获取 MIME 类型
- 根据 MIME 类型获取文件扩展名
- 判断文件类型（图片、视频、音频、文档、压缩包等）
- 通过魔数（Magic Bytes）检测文件真实 MIME 类型
- 生成安全的 Content-Disposition 头
"""

import struct
from typing import Optional, Tuple, List, Dict, Set, BinaryIO


# ==================== MIME 类型映射表 ====================

# 扩展名 -> MIME 类型
EXTENSION_TO_MIME: Dict[str, str] = {
    # 图片
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.bmp': 'image/bmp',
    '.tiff': 'image/tiff',
    '.tif': 'image/tiff',
    '.heic': 'image/heic',
    '.heif': 'image/heif',
    '.avif': 'image/avif',
    
    # 视频
    '.mp4': 'video/mp4',
    '.mpeg': 'video/mpeg',
    '.mpg': 'video/mpeg',
    '.avi': 'video/x-msvideo',
    '.mov': 'video/quicktime',
    '.wmv': 'video/x-ms-wmv',
    '.flv': 'video/x-flv',
    '.webm': 'video/webm',
    '.mkv': 'video/x-matroska',
    '.3gp': 'video/3gpp',
    '.ts': 'video/mp2t',
    
    # 音频
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.ogg': 'audio/ogg',
    '.flac': 'audio/flac',
    '.aac': 'audio/aac',
    '.m4a': 'audio/mp4',
    '.wma': 'audio/x-ms-wma',
    '.aiff': 'audio/aiff',
    '.opus': 'audio/opus',
    
    # 文档
    '.pdf': 'application/pdf',
    '.doc': 'application/msword',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.xls': 'application/vnd.ms-excel',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.ppt': 'application/vnd.ms-powerpoint',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    '.odt': 'application/vnd.oasis.opendocument.text',
    '.ods': 'application/vnd.oasis.opendocument.spreadsheet',
    '.odp': 'application/vnd.oasis.opendocument.presentation',
    '.rtf': 'application/rtf',
    
    # 文本
    '.txt': 'text/plain',
    '.html': 'text/html',
    '.htm': 'text/html',
    '.css': 'text/css',
    '.js': 'text/javascript',
    '.json': 'application/json',
    '.xml': 'application/xml',
    '.yaml': 'application/x-yaml',
    '.yml': 'application/x-yaml',
    '.csv': 'text/csv',
    '.md': 'text/markdown',
    
    # 压缩包
    '.zip': 'application/zip',
    '.tar': 'application/x-tar',
    '.gz': 'application/gzip',
    '.bz2': 'application/x-bzip2',
    '.7z': 'application/x-7z-compressed',
    '.rar': 'application/vnd.rar',
    
    # 代码
    '.py': 'text/x-python',
    '.java': 'text/x-java-source',
    '.c': 'text/x-c',
    '.cpp': 'text/x-c++',
    '.h': 'text/x-c',
    '.hpp': 'text/x-c++',
    '.cs': 'text/x-csharp',
    '.go': 'text/x-go',
    '.rs': 'text/x-rust',
    '.rb': 'text/x-ruby',
    '.php': 'text/x-php',
    '.sh': 'text/x-shellscript',
    '.bash': 'text/x-shellscript',
    '.swift': 'text/x-swift',
    '.kt': 'text/x-kotlin',
    
    # 可执行文件
    '.exe': 'application/x-msdownload',
    '.dll': 'application/x-msdownload',
    '.so': 'application/x-sharedlib',
    '.dylib': 'application/x-mach-binary',
    '.app': 'application/octet-stream',
    '.dmg': 'application/x-apple-diskimage',
    '.deb': 'application/vnd.debian.binary-package',
    '.rpm': 'application/x-rpm',
    
    # 字体
    '.ttf': 'font/ttf',
    '.otf': 'font/otf',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.eot': 'application/vnd.ms-fontobject',
    
    # 其他
    '.bin': 'application/octet-stream',
    '.dat': 'application/octet-stream',
    '.iso': 'application/x-iso9660-image',
    '.dmg': 'application/x-apple-diskimage',
    '.apk': 'application/vnd.android.package-archive',
    '.ipa': 'application/octet-stream',
}

# MIME 类型 -> 扩展名（优先扩展名在前）
MIME_TO_EXTENSIONS: Dict[str, List[str]] = {}
for ext, mime in EXTENSION_TO_MIME.items():
    if mime not in MIME_TO_EXTENSIONS:
        MIME_TO_EXTENSIONS[mime] = []
    MIME_TO_EXTENSIONS[mime].append(ext)

# 按 MIME 类型分类
MIME_CATEGORIES: Dict[str, Set[str]] = {
    'image': {
        'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml',
        'image/x-icon', 'image/bmp', 'image/tiff', 'image/heic', 'image/heif', 'image/avif'
    },
    'video': {
        'video/mp4', 'video/mpeg', 'video/x-msvideo', 'video/quicktime',
        'video/x-ms-wmv', 'video/x-flv', 'video/webm', 'video/x-matroska',
        'video/3gpp', 'video/mp2t'
    },
    'audio': {
        'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/flac', 'audio/aac',
        'audio/mp4', 'audio/x-ms-wma', 'audio/aiff', 'audio/opus'
    },
    'document': {
        'application/pdf', 'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/vnd.oasis.opendocument.text',
        'application/vnd.oasis.opendocument.spreadsheet',
        'application/vnd.oasis.opendocument.presentation',
        'application/rtf'
    },
    'text': {
        'text/plain', 'text/html', 'text/css', 'text/javascript', 'text/csv',
        'text/markdown', 'text/xml', 'application/json', 'application/xml',
        'application/x-yaml'
    },
    'archive': {
        'application/zip', 'application/x-tar', 'application/gzip',
        'application/x-bzip2', 'application/x-7z-compressed', 'application/vnd.rar'
    },
    'code': {
        'text/x-python', 'text/x-java-source', 'text/x-c', 'text/x-c++',
        'text/x-csharp', 'text/x-go', 'text/x-rust', 'text/x-ruby',
        'text/x-php', 'text/x-shellscript', 'text/x-swift', 'text/x-kotlin'
    },
    'executable': {
        'application/x-msdownload', 'application/x-sharedlib',
        'application/x-mach-binary', 'application/octet-stream',
        'application/vnd.android.package-archive'
    },
    'font': {
        'font/ttf', 'font/otf', 'font/woff', 'font/woff2',
        'application/vnd.ms-fontobject'
    }
}

# 魔数签名表（前几字节 -> MIME 类型）
MAGIC_SIGNATURES: List[Tuple[bytes, str, int]] = [
    # 图片
    (b'\xff\xd8\xff', 'image/jpeg', 3),
    (b'\x89PNG\r\n\x1a\n', 'image/png', 8),
    (b'GIF87a', 'image/gif', 6),
    (b'GIF89a', 'image/gif', 6),
    (b'RIFF', 'image/webp', 4),  # 需要进一步检查
    (b'\x00\x00\x01\x00', 'image/x-icon', 4),
    (b'BM', 'image/bmp', 2),
    (b'II*\x00', 'image/tiff', 4),  # Little-endian TIFF
    (b'MM\x00*', 'image/tiff', 4),  # Big-endian TIFF
    
    # 视频
    (b'\x00\x00\x00\x1cftypisom', 'video/mp4', 12),
    (b'\x00\x00\x00\x20ftypisom', 'video/mp4', 12),
    (b'\x00\x00\x00\x18ftypmp42', 'video/mp4', 12),
    (b'ftyp', 'video/mp4', 4),  # MP4 容器
    (b'\x1aE\xdf\xa3', 'video/webm', 4),  # WebM/MKV
    (b'RIFF', 'video/avi', 4),  # AVI 也用 RIFF
    (b'\x00\x00\x01\xba', 'video/mpeg', 4),
    (b'FLV\x01', 'video/x-flv', 4),
    
    # 音频
    (b'ID3', 'audio/mpeg', 3),  # MP3 with ID3 tag
    (b'\xff\xfb', 'audio/mpeg', 2),  # MP3 frame sync
    (b'\xff\xfa', 'audio/mpeg', 2),  # MP3 frame sync
    (b'\xff\xf3', 'audio/mpeg', 2),  # MP3 frame sync
    (b'\xff\xf2', 'audio/mpeg', 2),  # MP3 frame sync
    (b'RIFF', 'audio/wav', 4),  # WAV 也用 RIFF
    (b'OggS', 'audio/ogg', 4),
    (b'fLaC', 'audio/flac', 4),
    
    # 文档
    (b'%PDF', 'application/pdf', 4),
    (b'PK\x03\x04', 'application/zip', 4),  # ZIP (也用于 docx, xlsx 等)
    (b'\x50\x4b\x03\x04', 'application/zip', 4),
    
    # 压缩包
    (b'\x1f\x8b', 'application/gzip', 2),
    (b'BZ', 'application/x-bzip2', 2),
    (b'7z\xbc\xaf\x27\x1c', 'application/x-7z-compressed', 6),
    (b'Rar!\x1a\x07', 'application/vnd.rar', 7),
    
    # 可执行文件
    (b'MZ', 'application/x-msdownload', 2),  # Windows PE
    (b'\x7fELF', 'application/x-sharedlib', 4),  # Linux ELF
    (b'\xca\xfe\xba\xbe', 'application/x-mach-binary', 4),  # macOS Mach-O
    (b'\xcf\xfa\xed\xfe', 'application/x-mach-binary', 4),  # macOS Mach-O 64-bit
    
    # 其他
    (b'\x00\x00\x00', 'video/quicktime', 3),  # MOV 可能以此开头
]


# ==================== 核心函数 ====================

def get_mime_type(extension: str, default: str = 'application/octet-stream') -> str:
    """
    根据文件扩展名获取 MIME 类型
    
    Args:
        extension: 文件扩展名（可以带或不带点）
        default: 未找到时的默认值
    
    Returns:
        MIME 类型字符串
    
    Examples:
        >>> get_mime_type('.jpg')
        'image/jpeg'
        >>> get_mime_type('png')
        'image/png'
        >>> get_mime_type('.unknown', 'text/plain')
        'text/plain'
    """
    ext = extension.lower()
    if not ext.startswith('.'):
        ext = '.' + ext
    return EXTENSION_TO_MIME.get(ext, default)


def get_extensions(mime_type: str) -> List[str]:
    """
    根据 MIME 类型获取文件扩展名列表
    
    Args:
        mime_type: MIME 类型字符串
    
    Returns:
        扩展名列表，未找到返回空列表
    
    Examples:
        >>> get_extensions('image/jpeg')
        ['.jpg', '.jpeg']
        >>> get_extensions('video/mp4')
        ['.mp4']
        >>> get_extensions('unknown/type')
        []
    """
    mime = mime_type.lower()
    return MIME_TO_EXTENSIONS.get(mime, []).copy()


def get_primary_extension(mime_type: str, default: str = '.bin') -> str:
    """
    根据 MIME 类型获取首选扩展名
    
    Args:
        mime_type: MIME 类型字符串
        default: 未找到时的默认值
    
    Returns:
        首选扩展名
    
    Examples:
        >>> get_primary_extension('image/jpeg')
        '.jpg'
        >>> get_primary_extension('unknown/type')
        '.bin'
    """
    extensions = get_extensions(mime_type)
    return extensions[0] if extensions else default


def detect_mime_from_content(data: bytes, default: str = 'application/octet-stream') -> str:
    """
    通过魔数（Magic Bytes）检测文件的 MIME 类型
    
    Args:
        data: 文件内容的前若干字节（至少 12 字节）
        default: 未识别时的默认值
    
    Returns:
        检测到的 MIME 类型
    
    Examples:
        >>> detect_mime_from_content(b'\\xff\\xd8\\xff\\x00...')
        'image/jpeg'
        >>> detect_mime_from_content(b'%PDF-1.4...')
        'application/pdf'
    """
    if len(data) < 2:
        return default
    
    # 特殊处理 RIFF 格式（WAV、AVI、WebP）
    if data[:4] == b'RIFF' and len(data) >= 12:
        riff_type = data[8:12]
        if riff_type == b'WAVE':
            return 'audio/wav'
        elif riff_type == b'AVI ':
            return 'video/avi'
        elif riff_type == b'WEBP':
            return 'image/webp'
    
    # 特殊处理 MP4/MOV（ftyp 检查）
    if len(data) >= 12:
        # 检查 ftyp box
        if data[4:8] == b'ftyp':
            ftyp = data[8:12]
            if ftyp in (b'isom', b'mp41', b'mp42', b'M4V ', b'M4A ', b'avc1'):
                return 'video/mp4'
            elif ftyp in (b'M4A ', b'f4a '):
                return 'audio/mp4'
            elif ftyp in (b'qt  ', b'MSNV'):
                return 'video/quicktime'
    
    # 检查其他签名
    for signature, mime, sig_len in MAGIC_SIGNATURES:
        if len(data) >= sig_len and data[:sig_len] == signature:
            # 跳过已经处理的 RIFF
            if signature == b'RIFF':
                continue
            return mime
    
    return default


def detect_mime_from_file(file_path: str, default: str = 'application/octet-stream') -> str:
    """
    通过读取文件内容检测 MIME 类型
    
    Args:
        file_path: 文件路径
        default: 未识别时的默认值
    
    Returns:
        检测到的 MIME 类型
    
    Examples:
        >>> detect_mime_from_file('/path/to/image.jpg')
        'image/jpeg'
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read(64)  # 读取前 64 字节足够检测大多数格式
        return detect_mime_from_content(data, default)
    except (IOError, OSError):
        return default


def detect_mime_from_fileobj(file_obj: BinaryIO, default: str = 'application/octet-stream') -> str:
    """
    通过读取文件对象检测 MIME 类型
    
    Args:
        file_obj: 二进制文件对象
        default: 未识别时的默认值
    
    Returns:
        检测到的 MIME 类型
    """
    try:
        pos = file_obj.tell()
        data = file_obj.read(64)
        file_obj.seek(pos)
        return detect_mime_from_content(data, default)
    except (IOError, OSError):
        return default


def is_image(mime_type: str) -> bool:
    """判断是否为图片类型"""
    return mime_type.lower() in MIME_CATEGORIES['image']


def is_video(mime_type: str) -> bool:
    """判断是否为视频类型"""
    return mime_type.lower() in MIME_CATEGORIES['video']


def is_audio(mime_type: str) -> bool:
    """判断是否为音频类型"""
    return mime_type.lower() in MIME_CATEGORIES['audio']


def is_document(mime_type: str) -> bool:
    """判断是否为文档类型"""
    return mime_type.lower() in MIME_CATEGORIES['document']


def is_text(mime_type: str) -> bool:
    """判断是否为文本类型"""
    return mime_type.lower() in MIME_CATEGORIES['text']


def is_archive(mime_type: str) -> bool:
    """判断是否为压缩包类型"""
    return mime_type.lower() in MIME_CATEGORIES['archive']


def is_code(mime_type: str) -> bool:
    """判断是否为代码类型"""
    return mime_type.lower() in MIME_CATEGORIES['code']


def is_executable(mime_type: str) -> bool:
    """判断是否为可执行文件类型"""
    return mime_type.lower() in MIME_CATEGORIES['executable']


def is_font(mime_type: str) -> bool:
    """判断是否为字体类型"""
    return mime_type.lower() in MIME_CATEGORIES['font']


def get_category(mime_type: str) -> Optional[str]:
    """
    获取 MIME 类型所属的类别
    
    Args:
        mime_type: MIME 类型字符串
    
    Returns:
        类别名称，如 'image', 'video' 等；未找到返回 None
    
    Examples:
        >>> get_category('image/jpeg')
        'image'
        >>> get_category('application/pdf')
        'document'
        >>> get_category('unknown/type')
        None
    """
    mime = mime_type.lower()
    for category, types in MIME_CATEGORIES.items():
        if mime in types:
            return category
    return None


def get_mime_info(mime_type: str) -> Dict[str, any]:
    """
    获取 MIME 类型的详细信息
    
    Args:
        mime_type: MIME 类型字符串
    
    Returns:
        包含信息的字典
    
    Examples:
        >>> info = get_mime_info('image/jpeg')
        >>> info['extensions']
        ['.jpg', '.jpeg']
        >>> info['category']
        'image'
    """
    mime = mime_type.lower()
    return {
        'mime_type': mime,
        'extensions': get_extensions(mime),
        'primary_extension': get_primary_extension(mime),
        'category': get_category(mime),
        'is_image': is_image(mime),
        'is_video': is_video(mime),
        'is_audio': is_audio(mime),
        'is_document': is_document(mime),
        'is_text': is_text(mime),
        'is_archive': is_archive(mime),
        'is_code': is_code(mime),
        'is_executable': is_executable(mime),
        'is_font': is_font(mime),
    }


def parse_mime_type(mime_type: str) -> Tuple[str, Dict[str, str]]:
    """
    解析 MIME 类型字符串，提取类型、子类型和参数
    
    Args:
        mime_type: MIME 类型字符串（可能包含参数）
    
    Returns:
        (主类型, 参数字典)
    
    Examples:
        >>> parse_mime_type('text/html; charset=utf-8')
        ('text/html', {'charset': 'utf-8'})
        >>> parse_mime_type('application/json')
        ('application/json', {})
    """
    parts = mime_type.split(';')
    main_type = parts[0].strip().lower()
    params = {}
    
    for part in parts[1:]:
        if '=' in part:
            key, value = part.split('=', 1)
            params[key.strip().lower()] = value.strip().strip('"')
    
    return main_type, params


def build_mime_type(mime_type: str, params: Optional[Dict[str, str]] = None) -> str:
    """
    构建 MIME 类型字符串
    
    Args:
        mime_type: 主 MIME 类型
        params: 参数字典
    
    Returns:
        完整的 MIME 类型字符串
    
    Examples:
        >>> build_mime_type('text/html', {'charset': 'utf-8'})
        'text/html; charset=utf-8'
    """
    if not params:
        return mime_type
    
    param_str = '; '.join(f'{k}={v}' for k, v in params.items())
    return f'{mime_type}; {param_str}'


def content_disposition(filename: str, inline: bool = False) -> str:
    """
    生成 Content-Disposition 头的值
    
    Args:
        filename: 文件名
        inline: True 为 inline，False 为 attachment
    
    Returns:
        Content-Disposition 值
    
    Examples:
        >>> content_disposition('report.pdf')
        'attachment; filename="report.pdf"'
        >>> content_disposition('image.png', inline=True)
        'inline; filename="image.png"'
        >>> content_disposition('中文文件.txt')
        "attachment; filename=\"中文文件.txt\"; filename*=UTF-8''%E4%B8%AD%E6%96%87%E6%96%87%E4%BB%B6.txt"
    """
    from urllib.parse import quote
    
    disposition = 'inline' if inline else 'attachment'
    
    # ASCII 安全的文件名
    safe_filename = filename.replace('"', '\\"')
    
    # 检查是否需要 RFC 5987 编码
    try:
        filename.encode('ascii')
        return f'{disposition}; filename="{safe_filename}"'
    except UnicodeEncodeError:
        encoded = quote(filename, safe='')
        return f'{disposition}; filename="{safe_filename}"; filename*=UTF-8\'\'{encoded}'


def guess_type(filename: str, default: str = 'application/octet-stream') -> str:
    """
    根据文件名猜测 MIME 类型（兼容 mimetypes.guess_type）
    
    Args:
        filename: 文件名或路径
        default: 未找到时的默认值
    
    Returns:
        MIME 类型字符串
    
    Examples:
        >>> guess_type('document.pdf')
        'application/pdf'
        >>> guess_type('/path/to/image.jpg')
        'image/jpeg'
    """
    import os
    _, ext = os.path.splitext(filename)
    return get_mime_type(ext, default)


# 兼容标准库 mimetypes 模块的别名
def guess_extension(mime_type: str, default: str = '.bin') -> str:
    """
    根据 MIME 类型猜测扩展名（兼容 mimetypes.guess_extension）
    
    Args:
        mime_type: MIME 类型字符串
        default: 未找到时的默认值
    
    Returns:
        扩展名
    
    Examples:
        >>> guess_extension('image/jpeg')
        '.jpg'
    """
    return get_primary_extension(mime_type, default)


# ==================== 便捷类 ====================

class MimeTypeDetector:
    """
    MIME 类型检测器类
    
    提供链式调用和缓存功能
    """
    
    def __init__(self):
        self._cache: Dict[str, str] = {}
    
    def detect(self, data: bytes, extension: Optional[str] = None) -> str:
        """
        检测 MIME 类型，优先使用内容检测，可结合扩展名
        
        Args:
            data: 文件内容字节
            extension: 可选的文件扩展名
        
        Returns:
            MIME 类型
        """
        # 先尝试内容检测
        content_mime = detect_mime_from_content(data)
        
        if content_mime != 'application/octet-stream':
            return content_mime
        
        # 内容检测失败，尝试扩展名
        if extension:
            return get_mime_type(extension)
        
        return 'application/octet-stream'
    
    def detect_file(self, file_path: str) -> str:
        """
        检测文件的 MIME 类型
        
        Args:
            file_path: 文件路径
        
        Returns:
            MIME 类型
        """
        if file_path in self._cache:
            return self._cache[file_path]
        
        result = detect_mime_from_file(file_path)
        self._cache[file_path] = result
        return result
    
    def clear_cache(self) -> None:
        """清除缓存"""
        self._cache.clear()


# ==================== 导出 ====================

__all__ = [
    # 常量
    'EXTENSION_TO_MIME',
    'MIME_TO_EXTENSIONS',
    'MIME_CATEGORIES',
    
    # 核心函数
    'get_mime_type',
    'get_extensions',
    'get_primary_extension',
    'detect_mime_from_content',
    'detect_mime_from_file',
    'detect_mime_from_fileobj',
    
    # 类型判断
    'is_image',
    'is_video',
    'is_audio',
    'is_document',
    'is_text',
    'is_archive',
    'is_code',
    'is_executable',
    'is_font',
    'get_category',
    
    # 信息函数
    'get_mime_info',
    'parse_mime_type',
    'build_mime_type',
    'content_disposition',
    
    # 兼容函数
    'guess_type',
    'guess_extension',
    
    # 类
    'MimeTypeDetector',
]