"""
文件签名/魔数检测工具 (File Signature / Magic Number Detection Utils)

通过文件头部魔数检测文件真实类型，即使扩展名被更改也能正确识别。
支持 100+ 种常见文件格式，零外部依赖。

功能:
- 检测文件类型（通过魔数）
- 验证文件扩展名与实际类型是否匹配
- 获取文件的 MIME 类型
- 批量检测多个文件
- 支持字节流和文件路径两种输入方式
"""

import os
from typing import Optional, List, Dict, Tuple, Union, BinaryIO

# 文件签名数据库（魔数 -> 文件类型信息）
# 格式: (magic_bytes, offset, extension, mime_type, description)
_FILE_SIGNATURES = [
    # 图片格式
    (b'\xff\xd8\xff', 0, 'jpg', 'image/jpeg', 'JPEG Image'),
    (b'\x89PNG\r\n\x1a\n', 0, 'png', 'image/png', 'PNG Image'),
    (b'GIF87a', 0, 'gif', 'image/gif', 'GIF Image (87a)'),
    (b'GIF89a', 0, 'gif', 'image/gif', 'GIF Image (89a)'),
    (b'BM', 0, 'bmp', 'image/bmp', 'BMP Image'),
    (b'II*\x00', 0, 'tiff', 'image/tiff', 'TIFF Image (Little-endian)'),
    (b'MM\x00*', 0, 'tiff', 'image/tiff', 'TIFF Image (Big-endian)'),
    (b'RIFF', 0, 'webp', 'image/webp', 'WebP Image'),  # 需要进一步检查
    (b'\x00\x00\x01\x00', 0, 'ico', 'image/x-icon', 'ICO Icon'),
    (b'\x00\x00\x02\x00', 0, 'cur', 'image/x-cursor', 'CUR Cursor'),
    (b'8BPS', 0, 'psd', 'image/vnd.adobe.photoshop', 'Adobe Photoshop'),
    (b'P1', 0, 'pbm', 'image/x-portable-bitmap', 'Portable Bitmap'),
    (b'P2', 0, 'pgm', 'image/x-portable-graymap', 'Portable Graymap'),
    (b'P3', 0, 'ppm', 'image/x-portable-pixmap', 'Portable Pixmap'),
    (b'P4', 0, 'pbm', 'image/x-portable-bitmap', 'Portable Bitmap (Binary)'),
    (b'P5', 0, 'pgm', 'image/x-portable-graymap', 'Portable Graymap (Binary)'),
    (b'P6', 0, 'ppm', 'image/x-portable-pixmap', 'Portable Pixmap (Binary)'),
    (b'P7', 0, 'pam', 'image/x-portable-arbitrarymap', 'Portable Arbitrary Map'),
    (b'HEIC', 4, 'heic', 'image/heic', 'HEIF Image'),  # 实际位置在 ftyp 后
    
    # 视频格式
    (b'\x1aE\xdf\xa3', 0, 'mkv', 'video/x-matroska', 'Matroska Video'),
    (b'ftyp', 4, 'mp4', 'video/mp4', 'MP4 Video'),  # ftyp box
    (b'ftyp', 4, 'mov', 'video/quicktime', 'QuickTime Movie'),
    (b'ftyp', 4, '3gp', 'video/3gpp', '3GPP Video'),
    (b'\x00\x00\x01\xba', 0, 'mpg', 'video/mpeg', 'MPEG Video'),
    (b'\x00\x00\x01\xb3', 0, 'mpg', 'video/mpeg', 'MPEG Video'),
    (b'FLV\x01', 0, 'flv', 'video/x-flv', 'Flash Video'),
    (b'RIFF', 0, 'avi', 'video/x-msvideo', 'AVI Video'),  # 需要进一步检查 AVI
    (b'\x30\x26\xb2\x75\x8e\x66\xcf\x11', 0, 'wmv', 'video/x-ms-wmv', 'Windows Media Video'),
    (b'\x1a\x45\xdf\xa3', 0, 'webm', 'video/webm', 'WebM Video'),
    
    # 音频格式
    (b'ID3', 0, 'mp3', 'audio/mpeg', 'MP3 Audio (ID3)'),
    (b'\xff\xfb', 0, 'mp3', 'audio/mpeg', 'MP3 Audio'),
    (b'\xff\xfa', 0, 'mp3', 'audio/mpeg', 'MP3 Audio'),
    (b'\xff\xf3', 0, 'mp3', 'audio/mpeg', 'MP3 Audio'),
    (b'\xff\xf2', 0, 'mp3', 'audio/mpeg', 'MP3 Audio'),
    (b'fLaC', 0, 'flac', 'audio/flac', 'FLAC Audio'),
    (b'OggS', 0, 'ogg', 'audio/ogg', 'OGG Audio'),
    (b'RIFF', 0, 'wav', 'audio/wav', 'WAV Audio'),  # 需要进一步检查 WAVE
    (b'ftypM4A', 0, 'm4a', 'audio/mp4', 'M4A Audio'),
    (b'ftypM4B', 0, 'm4b', 'audio/mp4', 'M4B Audio'),
    (b'\x30\x26\xb2\x75\x8e\x66\xcf\x11', 0, 'wma', 'audio/x-ms-wma', 'Windows Media Audio'),
    (b'FORM', 0, 'aiff', 'audio/aiff', 'AIFF Audio'),
    (b'MAC\x20', 0, 'ape', 'audio/x-ape', 'APE Audio'),
    (b'MThd', 0, 'mid', 'audio/midi', 'MIDI Audio'),
    
    # 文档格式
    (b'%PDF', 0, 'pdf', 'application/pdf', 'PDF Document'),
    (b'PK\x03\x04', 0, 'docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'Office Document (ZIP-based)'),
    (b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1', 0, 'doc', 'application/msword', 'Microsoft Office Document (OLE)'),
    (b'Binary\x20', 0, 'doc', 'application/msword', 'Word 2.0 Document'),
    
    # 电子书格式
    (b'PK\x03\x04', 0, 'epub', 'application/epub+zip', 'EPUB eBook'),
    (b'mobi', 0x3c, 'mobi', 'application/x-mobipocket-ebook', 'MobiPocket eBook'),
    
    # 压缩格式
    (b'PK\x03\x04', 0, 'zip', 'application/zip', 'ZIP Archive'),
    (b'Rar!\x1a\x07', 0, 'rar', 'application/x-rar-compressed', 'RAR Archive'),
    (b'\x1f\x8b', 0, 'gz', 'application/gzip', 'GZIP Archive'),
    (b'BZh', 0, 'bz2', 'application/x-bzip2', 'BZIP2 Archive'),
    (b'BZ', 0, 'bz2', 'application/x-bzip2', 'BZIP2 Archive'),
    (b'\xfd7zXZ\x00', 0, 'xz', 'application/x-xz', 'XZ Archive'),
    (b'\x04\x22\x4d\x18', 0, 'lz4', 'application/x-lz4', 'LZ4 Archive'),
    (b'\x28\xb5\x2f\xfd', 0, 'zst', 'application/x-zstd', 'Zstandard Archive'),
    (b'\x1f\x9d', 0, 'z', 'application/x-compress', 'UNIX Compress'),
    (b'MSDOS', 0, 'arj', 'application/x-arj', 'ARJ Archive'),
    (b'\x60\xea', 0, 'arj', 'application/x-arj', 'ARJ Archive'),
    (b'7z\xbc\xaf\x27\x1c', 0, '7z', 'application/x-7z-compressed', '7-Zip Archive'),
    (b'\x1a\x45\xdf\xa3', 0, 'tar.xz', 'application/x-tar+xz', 'TAR XZ Archive'),
    
    # 可执行文件
    (b'MZ', 0, 'exe', 'application/x-msdos-program', 'Windows Executable'),
    (b'\x7fELF', 0, 'elf', 'application/x-elf', 'Linux ELF Executable'),
    (b'\xca\xfe\xba\xbe', 0, 'class', 'application/java-vm', 'Java Class'),
    (b'\xca\xfe\xba\xbe', 0, 'dex', 'application/x-dex', 'Android DEX'),
    (b'dex\n', 0, 'dex', 'application/x-dex', 'Android DEX'),
    (b'Mach-O', 0, 'macho', 'application/x-mach-binary', 'macOS Mach-O'),
    (b'\xcf\xfa\xed\xfe', 0, 'macho', 'application/x-mach-binary', 'macOS Mach-O (32-bit)'),
    (b'\xcf\xfa\xed\xfe', 0, 'dylib', 'application/x-mach-binary', 'macOS Dynamic Library'),
    (b'\xfe\xed\xfa\xce', 0, 'macho', 'application/x-mach-binary', 'macOS Mach-O (Big-endian)'),
    
    # 脚本和代码
    (b'#!/', 0, 'sh', 'text/x-shellscript', 'Shell Script'),
    (b'#!', 0, 'script', 'text/x-script', 'Script File'),
    (b'<?xml', 0, 'xml', 'text/xml', 'XML Document'),
    (b'<html', 0, 'html', 'text/html', 'HTML Document'),
    (b'<HTML', 0, 'html', 'text/html', 'HTML Document'),
    (b'<!DOCTYPE', 0, 'html', 'text/html', 'HTML Document'),
    (b'%!PS', 0, 'ps', 'application/postscript', 'PostScript Document'),
    (b'%PDF', 0, 'pdf', 'application/pdf', 'PDF Document'),
    
    # 数据格式
    (b'\x89HDF\r\n\x1a\n', 0, 'hdf', 'application/x-hdf', 'HDF5 Data'),
    (b'\x93NUMPY', 0, 'npy', 'application/x-numpy', 'NumPy Array'),
    (b'MATLAB', 0, 'mat', 'application/x-matlab-data', 'MATLAB Data'),
    (b'SQLite format 3', 0, 'sqlite', 'application/x-sqlite3', 'SQLite Database'),
    (b'PMIG', 0, 'pml', 'application/x-pml', 'PML Data'),
    
    # 数据库
    (b'\x00\x00\x00\x00', 0, 'db', 'application/octet-stream', 'Database File'),
    
    # 密钥和证书
    (b'-----BEGIN', 0, 'pem', 'application/x-pem-file', 'PEM Certificate'),
    (b'\x30\x82', 0, 'der', 'application/x-x509-ca-cert', 'DER Certificate'),
    (b'SSH PRIVATE KEY', 0, 'pem', 'application/x-pem-file', 'SSH Private Key'),
    (b'OPENSSH PRIVATE KEY', 0, 'pem', 'application/x-pem-file', 'OpenSSH Private Key'),
    (b'PuTTY-User-Key-File', 0, 'ppk', 'application/x-putty-user-key-file', 'PuTTY Private Key'),
    (b'GPG key', 0, 'gpg', 'application/pgp-keys', 'GPG Key'),
    
    # 字体格式
    (b'\x00\x01\x00\x00', 0, 'ttf', 'font/ttf', 'TrueType Font'),
    (b'OTTO', 0, 'otf', 'font/otf', 'OpenType Font'),
    (b'wOFF', 0, 'woff', 'font/woff', 'Web Open Font Format'),
    (b'wOF2', 0, 'woff2', 'font/woff2', 'Web Open Font Format 2'),
    (b'true', 0, 'ttf', 'font/ttf', 'TrueType Font'),
    (b'typ1', 0, 'ttf', 'font/ttf', 'TrueType Font'),
    
    # 虚拟磁盘
    (b'VMDK', 0, 'vmdk', 'application/x-vmdk', 'VMware Virtual Disk'),
    (b'VHD', 0, 'vhd', 'application/x-vhd', 'Virtual Hard Disk'),
    (b'VHDX', 0, 'vhdx', 'application/x-vhdx', 'VHDX Virtual Disk'),
    (b'conectix', 0, 'vhd', 'application/x-vhd', 'Virtual Hard Disk'),
    
    # 镜像文件
    (b'CD001', 0x8001, 'iso', 'application/x-iso9660-image', 'ISO 9660 Image'),
    (b'CD001', 0x8801, 'iso', 'application/x-iso9660-image', 'ISO 9660 Image'),
    (b'DMG', 0, 'dmg', 'application/x-apple-diskimage', 'Apple Disk Image'),
    
    # 系统文件
    (b'REGEDIT4', 0, 'reg', 'text/x-ms-regedit', 'Windows Registry'),
    (b'Windows Registry Editor', 0, 'reg', 'text/x-ms-regedit', 'Windows Registry'),
    (b'\xeb\x3c\x90', 0, 'img', 'application/octet-stream', 'Disk Image'),
    
    # 邮件格式
    (b'From ', 0, 'eml', 'message/rfc822', 'Email Message'),
    (b'Return-Path:', 0, 'eml', 'message/rfc822', 'Email Message'),
    (b'Received:', 0, 'eml', 'message/rfc822', 'Email Message'),
    
    # 备份文件
    (b'BUP\x02', 0, 'bup', 'application/x-bup', 'Backup File'),
    
    # 游戏资源
    (b'PK\x03\x04', 0, 'jar', 'application/java-archive', 'Java Archive'),
    (b'PK\x03\x04', 0, 'apk', 'application/vnd.android.package-archive', 'Android Package'),
    (b'PK\x03\x04', 0, 'ipa', 'application/octet-stream', 'iOS App'),
    
    # 代码库
    (b'DIRC', 0, 'git', 'application/x-git', 'Git Index'),
    
    # 其他
    (b'\x00\x00\x00\x1cftyp', 0, 'heic', 'image/heic', 'HEIF Image'),
    (b'\x00\x00\x00\x20ftyp', 0, 'heic', 'image/heic', 'HEIF Image'),
    (b'ftypheic', 4, 'heic', 'image/heic', 'HEIF Image'),
    (b'ftypheix', 4, 'heic', 'image/heic', 'HEIF Image'),
    (b'ftypmif1', 4, 'heic', 'image/heic', 'HEIF Image'),
]


class FileType:
    """文件类型信息"""
    
    def __init__(
        self,
        extension: str,
        mime_type: str,
        description: str,
        confidence: float = 1.0
    ):
        self.extension = extension
        self.mime_type = mime_type
        self.description = description
        self.confidence = confidence
    
    def __repr__(self) -> str:
        return (
            f"FileType(extension='{self.extension}', "
            f"mime_type='{self.mime_type}', "
            f"description='{self.description}', "
            f"confidence={self.confidence:.2f})"
        )
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FileType):
            return False
        return (
            self.extension == other.extension and
            self.mime_type == other.mime_type
        )
    
    def __hash__(self) -> int:
        return hash((self.extension, self.mime_type))
    
    def to_dict(self) -> Dict[str, any]:
        """转换为字典"""
        return {
            'extension': self.extension,
            'mime_type': self.mime_type,
            'description': self.description,
            'confidence': self.confidence
        }


def _read_file_header(file_path: str, length: int = 64) -> bytes:
    """读取文件头部字节"""
    try:
        with open(file_path, 'rb') as f:
            return f.read(length)
    except (IOError, OSError):
        return b''


def _match_signature(data: bytes, signature: bytes, offset: int) -> bool:
    """检查数据是否匹配签名"""
    if offset < 0:
        return False
    if len(data) < offset + len(signature):
        return False
    return data[offset:offset + len(signature)] == signature


def _check_riff_type(data: bytes, expected_type: bytes) -> bool:
    """检查 RIFF 文件类型（AVI、WAV、WebP 等）"""
    if len(data) < 12:
        return False
    if data[0:4] != b'RIFF':
        return False
    return data[8:12] == expected_type


def detect_file_type(
    source: Union[str, bytes, BinaryIO],
    max_bytes: int = 1024
) -> Optional[FileType]:
    """
    检测文件类型
    
    Args:
        source: 文件路径、字节流或文件对象
        max_bytes: 最大读取字节数（用于文件路径时）
    
    Returns:
        FileType 对象，如果无法识别则返回 None
    
    Example:
        >>> detect_file_type('/path/to/image.jpg')
        FileType(extension='jpg', mime_type='image/jpeg', ...)
        >>> detect_file_type(b'\\x89PNG\\r\\n\\x1a\\n...')
        FileType(extension='png', mime_type='image/png', ...)
    """
    # 获取文件数据
    if isinstance(source, str):
        data = _read_file_header(source, max_bytes)
        if not data:
            return None
    elif isinstance(source, bytes):
        data = source
    elif hasattr(source, 'read'):
        # 文件对象
        pos = source.tell()
        data = source.read(max_bytes)
        source.seek(pos)
    else:
        raise TypeError(f"Unsupported source type: {type(source)}")
    
    if not data:
        return None
    
    # 特殊处理 RIFF 格式（AVI、WAV、WebP）
    if data[:4] == b'RIFF':
        if len(data) >= 12:
            riff_type = data[8:12]
            if riff_type == b'AVI ':
                return FileType('avi', 'video/x-msvideo', 'AVI Video')
            elif riff_type == b'WAVE':
                return FileType('wav', 'audio/wav', 'WAV Audio')
            elif riff_type == b'WEBP':
                return FileType('webp', 'image/webp', 'WebP Image')
    
    # 特殊处理 ZIP 格式（需要区分 ZIP、JAR、APK、DOCX 等）
    if data[:4] == b'PK\x03\x04':
        # 尝试检测 ZIP 内部的特定文件
        if b'META-INF/MANIFEST.MF' in data or b'META-INF/' in data:
            return FileType('jar', 'application/java-archive', 'Java Archive')
        # 默认返回 ZIP
        return FileType('zip', 'application/zip', 'ZIP Archive')
    
    # 特殊处理 MP4/MOV/3GP 格式
    if len(data) >= 8 and data[4:8] == b'ftyp':
        ftyp_brand = data[8:12] if len(data) >= 12 else b''
        if ftyp_brand in (b'isom', b'mp41', b'mp42', b'M4V ', b'M4A ', b'M4P '):
            return FileType('mp4', 'video/mp4', 'MP4 Video')
        elif ftyp_brand in (b'qt  ',):
            return FileType('mov', 'video/quicktime', 'QuickTime Movie')
        elif ftyp_brand in (b'3gp5', b'3gp4', b'3gg5'):
            return FileType('3gp', 'video/3gpp', '3GPP Video')
        elif ftyp_brand in (b'heic', b'heix', b'mif1'):
            return FileType('heic', 'image/heic', 'HEIF Image')
        elif ftyp_brand in (b'M4A ', b'M4B '):
            return FileType('m4a', 'audio/mp4', 'M4A Audio')
        else:
            return FileType('mp4', 'video/mp4', 'MP4 Video')
    
    # 特殊处理 MP3（多种帧头）
    if len(data) >= 2:
        # ID3 标签
        if data[:3] == b'ID3':
            return FileType('mp3', 'audio/mpeg', 'MP3 Audio (ID3)')
        # MP3 帧同步
        if data[0] == 0xff and (data[1] & 0xe0) == 0xe0:
            return FileType('mp3', 'audio/mpeg', 'MP3 Audio')
    
    # 特殊处理 ELF 可执行文件
    if data[:4] == b'\x7fELF':
        return FileType('elf', 'application/x-elf', 'Linux ELF Executable')
    
    # 特殊处理 Windows 可执行文件
    if data[:2] == b'MZ':
        # 检查是否是 PE 文件
        if len(data) >= 64:
            pe_offset = int.from_bytes(data[60:64], 'little')
            if len(data) >= pe_offset + 4:
                if data[pe_offset:pe_offset+4] == b'PE\x00\x00':
                    return FileType('exe', 'application/x-msdos-program', 'Windows Executable')
        return FileType('exe', 'application/x-msdos-program', 'Windows Executable')
    
    # 特殊处理 macOS Mach-O 文件
    if data[:4] in (b'\xfe\xed\xfa\xce', b'\xfe\xed\xfa\xcf',
                    b'\xce\xfa\xed\xfe', b'\xcf\xfa\xed\xfe'):
        return FileType('macho', 'application/x-mach-binary', 'macOS Mach-O')
    
    # 特殊处理 SQLite 数据库
    if data[:16] == b'SQLite format 3\x00':
        return FileType('sqlite', 'application/x-sqlite3', 'SQLite Database')
    
    # 特殊处理 PDF
    if data[:4] == b'%PDF':
        return FileType('pdf', 'application/pdf', 'PDF Document')
    
    # 遍历签名数据库
    for signature, offset, extension, mime_type, description in _FILE_SIGNATURES:
        if _match_signature(data, signature, offset):
            return FileType(extension, mime_type, description)
    
    # 检查文本文件
    try:
        text = data[:512].decode('utf-8', errors='strict')
        # 检查 JSON
        text_stripped = text.strip()
        if text_stripped.startswith('{') or text_stripped.startswith('['):
            return FileType('json', 'application/json', 'JSON Data', confidence=0.8)
        # 检查 HTML
        if text_stripped.lower().startswith('<!doctype html') or \
           text_stripped.lower().startswith('<html'):
            return FileType('html', 'text/html', 'HTML Document', confidence=0.8)
        # 检查 XML
        if text_stripped.startswith('<?xml'):
            return FileType('xml', 'text/xml', 'XML Document', confidence=0.9)
        # 检查脚本
        if text_stripped.startswith('#!'):
            return FileType('sh', 'text/x-shellscript', 'Shell Script', confidence=0.7)
    except UnicodeDecodeError:
        pass
    
    return None


def detect_extension(source: Union[str, bytes, BinaryIO]) -> Optional[str]:
    """
    检测文件扩展名
    
    Args:
        source: 文件路径、字节流或文件对象
    
    Returns:
        文件扩展名（小写），如果无法识别则返回 None
    
    Example:
        >>> detect_extension('/path/to/image.jpg')
        'jpg'
        >>> detect_extension(b'\\x89PNG\\r\\n\\x1a\\n...')
        'png'
    """
    file_type = detect_file_type(source)
    return file_type.extension if file_type else None


def detect_mime_type(source: Union[str, bytes, BinaryIO]) -> Optional[str]:
    """
    检测文件 MIME 类型
    
    Args:
        source: 文件路径、字节流或文件对象
    
    Returns:
        MIME 类型字符串，如果无法识别则返回 None
    
    Example:
        >>> detect_mime_type('/path/to/image.jpg')
        'image/jpeg'
    """
    file_type = detect_file_type(source)
    return file_type.mime_type if file_type else None


def verify_extension(file_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    验证文件扩展名与实际类型是否匹配
    
    Args:
        file_path: 文件路径
    
    Returns:
        (是否匹配, 声明扩展名, 实际扩展名)
    
    Example:
        >>> verify_extension('/path/to/fake.txt')  # 实际是 PNG
        (False, 'txt', 'png')
        >>> verify_extension('/path/to/real.png')
        (True, 'png', 'png')
    """
    # 获取声明的扩展名
    _, ext = os.path.splitext(file_path)
    declared_ext = ext.lower().lstrip('.') if ext else None
    
    # 检测实际类型
    actual_type = detect_file_type(file_path)
    actual_ext = actual_type.extension if actual_type else None
    
    # 比较
    match = declared_ext == actual_ext if declared_ext and actual_ext else False
    
    return (match, declared_ext, actual_ext)


def batch_detect(
    file_paths: List[str],
    max_bytes: int = 1024
) -> Dict[str, Optional[FileType]]:
    """
    批量检测文件类型
    
    Args:
        file_paths: 文件路径列表
        max_bytes: 每个文件最大读取字节数
    
    Returns:
        文件路径到 FileType 的映射
    
    Example:
        >>> batch_detect(['/path/to/file1', '/path/to/file2'])
        {'/path/to/file1': FileType(...), '/path/to/file2': FileType(...)}
    """
    results = {}
    for file_path in file_paths:
        results[file_path] = detect_file_type(file_path, max_bytes)
    return results


def is_type(
    source: Union[str, bytes, BinaryIO],
    expected_extension: str
) -> bool:
    """
    检查文件是否为指定类型
    
    Args:
        source: 文件路径、字节流或文件对象
        expected_extension: 期望的扩展名
    
    Returns:
        是否匹配
    
    Example:
        >>> is_type('/path/to/image.jpg', 'jpg')
        True
        >>> is_type('/path/to/fake.txt', 'png')
        False  # 声明是 txt，实际是 png
    """
    file_type = detect_file_type(source)
    if not file_type:
        return False
    return file_type.extension.lower() == expected_extension.lower()


def is_image(source: Union[str, bytes, BinaryIO]) -> bool:
    """检查是否为图片文件"""
    file_type = detect_file_type(source)
    if not file_type:
        return False
    return file_type.mime_type.startswith('image/')


def is_video(source: Union[str, bytes, BinaryIO]) -> bool:
    """检查是否为视频文件"""
    file_type = detect_file_type(source)
    if not file_type:
        return False
    return file_type.mime_type.startswith('video/')


def is_audio(source: Union[str, bytes, BinaryIO]) -> bool:
    """检查是否为音频文件"""
    file_type = detect_file_type(source)
    if not file_type:
        return False
    return file_type.mime_type.startswith('audio/')


def is_document(source: Union[str, bytes, BinaryIO]) -> bool:
    """检查是否为文档文件"""
    file_type = detect_file_type(source)
    if not file_type:
        return False
    doc_types = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument',
        'application/vnd.ms-',
        'text/',
    ]
    return any(file_type.mime_type.startswith(t) for t in doc_types)


def is_archive(source: Union[str, bytes, BinaryIO]) -> bool:
    """检查是否为压缩文件"""
    file_type = detect_file_type(source)
    if not file_type:
        return False
    archive_extensions = {
        'zip', 'rar', 'gz', 'bz2', 'xz', '7z', 'tar', 'tgz',
        'tar.gz', 'tar.bz2', 'tar.xz', 'lz4', 'zst', 'arj'
    }
    return file_type.extension in archive_extensions


def is_executable(source: Union[str, bytes, BinaryIO]) -> bool:
    """检查是否为可执行文件"""
    file_type = detect_file_type(source)
    if not file_type:
        return False
    exe_extensions = {
        'exe', 'elf', 'macho', 'dylib', 'dll', 'so',
        'class', 'dex', 'apk', 'ipa'
    }
    return file_type.extension in exe_extensions


def get_supported_types() -> Dict[str, List[str]]:
    """
    获取支持的文件类型列表
    
    Returns:
        按类别分组的文件类型字典
    
    Example:
        >>> get_supported_types()
        {'images': ['jpg', 'png', ...], 'videos': [...], ...}
    """
    return {
        'images': [
            'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp',
            'ico', 'psd', 'pbm', 'pgm', 'ppm', 'pam', 'heic'
        ],
        'videos': [
            'mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv', 'webm',
            'mpg', 'mpeg', '3gp'
        ],
        'audio': [
            'mp3', 'flac', 'wav', 'ogg', 'm4a', 'm4b', 'wma',
            'aiff', 'ape', 'mid', 'midi'
        ],
        'documents': [
            'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
            'odt', 'ods', 'odp', 'epub', 'mobi'
        ],
        'archives': [
            'zip', 'rar', 'gz', 'bz2', 'xz', '7z', 'tar',
            'tgz', 'lz4', 'zst', 'arj'
        ],
        'executables': [
            'exe', 'dll', 'so', 'elf', 'macho', 'dylib',
            'class', 'jar', 'apk', 'ipa', 'dex'
        ],
        'fonts': [
            'ttf', 'otf', 'woff', 'woff2'
        ],
        'databases': [
            'sqlite', 'db', 'hdf', 'npy', 'mat'
        ],
        'certificates': [
            'pem', 'der', 'crt', 'key', 'ppk', 'gpg'
        ],
        'disk_images': [
            'iso', 'img', 'dmg', 'vmdk', 'vhd', 'vhdx'
        ],
        'code': [
            'sh', 'py', 'js', 'ts', 'java', 'c', 'cpp', 'go',
            'rs', 'rb', 'php', 'swift', 'kt'
        ],
        'data': [
            'json', 'xml', 'yaml', 'yml', 'toml', 'ini', 'csv'
        ]
    }


def get_extension_mime_map() -> Dict[str, str]:
    """
    获取扩展名到 MIME 类型的映射
    
    Returns:
        扩展名到 MIME 类型的字典
    
    Example:
        >>> get_extension_mime_map()
        {'jpg': 'image/jpeg', 'png': 'image/png', ...}
    """
    mime_map = {}
    seen_extensions = set()
    
    for _, _, extension, mime_type, _ in _FILE_SIGNATURES:
        if extension not in seen_extensions:
            mime_map[extension] = mime_type
            seen_extensions.add(extension)
    
    # 添加额外的常见 MIME 类型
    additional = {
        'json': 'application/json',
        'xml': 'text/xml',
        'html': 'text/html',
        'css': 'text/css',
        'js': 'text/javascript',
        'py': 'text/x-python',
        'java': 'text/x-java-source',
        'c': 'text/x-c',
        'cpp': 'text/x-c++',
        'go': 'text/x-go',
        'rs': 'text/x-rust',
        'rb': 'text/x-ruby',
        'php': 'text/x-php',
        'swift': 'text/x-swift',
        'kt': 'text/x-kotlin',
        'sh': 'text/x-shellscript',
        'yaml': 'text/yaml',
        'yml': 'text/yaml',
        'toml': 'text/x-toml',
        'ini': 'text/x-ini',
        'csv': 'text/csv',
        'txt': 'text/plain',
        'md': 'text/markdown',
        'svg': 'image/svg+xml',
    }
    
    mime_map.update(additional)
    return mime_map


def analyze_file(file_path: str) -> Dict[str, any]:
    """
    全面分析文件
    
    Args:
        file_path: 文件路径
    
    Returns:
        包含详细信息的字典
    
    Example:
        >>> analyze_file('/path/to/image.jpg')
        {
            'file_type': FileType(...),
            'size': 1024,
            'extension_match': True,
            'declared_extension': 'jpg',
            'actual_extension': 'jpg',
            'is_image': True,
            'is_video': False,
            'is_audio': False,
            'is_document': False,
            'is_archive': False,
            'is_executable': False
        }
    """
    file_type = detect_file_type(file_path)
    match, declared, actual = verify_extension(file_path)
    
    # 获取文件大小
    try:
        size = os.path.getsize(file_path)
    except OSError:
        size = None
    
    return {
        'file_type': file_type,
        'file_type_dict': file_type.to_dict() if file_type else None,
        'size': size,
        'extension_match': match,
        'declared_extension': declared,
        'actual_extension': actual,
        'is_image': is_image(file_path) if file_type else False,
        'is_video': is_video(file_path) if file_type else False,
        'is_audio': is_audio(file_path) if file_type else False,
        'is_document': is_document(file_path) if file_type else False,
        'is_archive': is_archive(file_path) if file_type else False,
        'is_executable': is_executable(file_path) if file_type else False,
    }