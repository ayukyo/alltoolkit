#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Compression Utilities Module

Comprehensive compression utilities for Python with zero external dependencies.
Provides ZIP, GZIP, BZ2, LZMA, TAR operations and more.

Author: AllToolkit
License: MIT
"""

import zipfile
import gzip
import bz2
import lzma
import tarfile
import os
import shutil
from pathlib import Path
from typing import Union, List, Optional, Dict, Any, Tuple
from datetime import datetime
import io
import stat


# =============================================================================
# Type Aliases
# =============================================================================

FilePath = Union[str, Path]
CompressionLevel = int  # 0-9 for most algorithms


# =============================================================================
# Constants
# =============================================================================

DEFAULT_COMPRESSION_LEVEL = 6
MAX_COMPRESSION_LEVEL = 9
MIN_COMPRESSION_LEVEL = 0

ZIP_COMPRESSION_METHODS = {
    'store': zipfile.ZIP_STORED,
    'deflate': zipfile.ZIP_DEFLATED,
    'bzip2': zipfile.ZIP_BZIP2,
    'lzma': zipfile.ZIP_LZMA,
}

TAR_COMPRESSION_MODES = {
    None: 'w',
    '': 'w',
    'gz': 'w:gz',
    'bz2': 'w:bz2',
    'xz': 'w:xz',
}


# =============================================================================
# ZIP Operations
# =============================================================================

def create_zip(
    output_path: FilePath,
    source_paths: List[FilePath],
    compression: str = 'deflate',
    compression_level: int = DEFAULT_COMPRESSION_LEVEL,
    base_path: Optional[FilePath] = None,
    include_hidden: bool = False,
) -> Dict[str, Any]:
    """
    Create a ZIP archive from files and/or directories.
    
    Args:
        output_path: Path to the output ZIP file
        source_paths: List of files and/or directories to compress
        compression: Compression method ('store', 'deflate', 'bzip2', 'lzma')
        compression_level: Compression level (0-9)
        base_path: Base path to strip from archive paths
        include_hidden: Whether to include hidden files (starting with .)
        
    Returns:
        Dict with statistics: {'files': count, 'compressed_size': bytes, 'original_size': bytes}
        
    Example:
        >>> result = create_zip('archive.zip', ['file1.txt', 'dir1/'])
        >>> print(f"Compressed {result['files']} files")
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    method = ZIP_COMPRESSION_METHODS.get(compression, zipfile.ZIP_DEFLATED)
    
    files_added = 0
    original_size = 0
    compressed_size = 0
    
    # compresslevel parameter was added in Python 3.7
    import sys
    if sys.version_info >= (3, 7):
        zf_kwargs = {'compression': method, 'compresslevel': compression_level}
    else:
        zf_kwargs = {'compression': method}
    
    with zipfile.ZipFile(output_path, 'w', **zf_kwargs) as zf:
        for source in source_paths:
            source = Path(source)
            if not source.exists():
                raise FileNotFoundError(f"Source path not found: {source}")
            
            if source.is_file():
                arcname = source.name if base_path is None else str(source.relative_to(Path(base_path)))
                original_size += source.stat().st_size
                zf.write(source, arcname)
                files_added += 1
            elif source.is_dir():
                for root, dirs, files in os.walk(source):
                    if not include_hidden:
                        dirs[:] = [d for d in dirs if not d.startswith('.')]
                        files = [f for f in files if not f.startswith('.')]
                    
                    for file in files:
                        file_path = Path(root) / file
                        if base_path:
                            arcname = str(file_path.relative_to(Path(base_path)))
                        else:
                            arcname = str(file_path.relative_to(source))
                        original_size += file_path.stat().st_size
                        zf.write(file_path, arcname)
                        files_added += 1
    
    compressed_size = output_path.stat().st_size
    
    return {
        'files': files_added,
        'compressed_size': compressed_size,
        'original_size': original_size,
        'ratio': f"{(1 - compressed_size / original_size) * 100:.1f}%" if original_size > 0 else "N/A",
    }


def extract_zip(
    zip_path: FilePath,
    extract_to: FilePath = '.',
    password: Optional[str] = None,
    members: Optional[List[str]] = None,
) -> List[str]:
    """
    Extract files from a ZIP archive.
    
    Args:
        zip_path: Path to the ZIP file
        extract_to: Directory to extract files to
        password: Password for encrypted ZIP files
        members: Specific members to extract (None = all)
        
    Returns:
        List of extracted file paths
        
    Example:
        >>> files = extract_zip('archive.zip', 'output/')
        >>> print(f"Extracted {len(files)} files")
    """
    zip_path = Path(zip_path)
    extract_to = Path(extract_to)
    extract_to.mkdir(parents=True, exist_ok=True)
    
    extracted = []
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        names_to_extract = members if members else zf.namelist()
        
        for name in names_to_extract:
            try:
                zf.extract(name, extract_to, pwd=password.encode() if password else None)
                extracted.append(str(extract_to / name))
            except Exception as e:
                print(f"Warning: Could not extract {name}: {e}")
    
    return extracted


def list_zip_contents(zip_path: FilePath) -> List[Dict[str, Any]]:
    """
    List contents of a ZIP archive with detailed information.
    
    Args:
        zip_path: Path to the ZIP file
        
    Returns:
        List of dicts with file info: {'name', 'size', 'compressed_size', 'datetime'}
        
    Example:
        >>> contents = list_zip_contents('archive.zip')
        >>> for item in contents:
        ...     print(f"{item['name']}: {item['size']} bytes")
    """
    zip_path = Path(zip_path)
    contents = []
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for info in zf.infolist():
            contents.append({
                'name': info.filename,
                'size': info.file_size,
                'compressed_size': info.compress_size,
                'datetime': datetime(*info.date_time).isoformat(),
                'is_dir': info.filename.endswith('/'),
            })
    
    return contents


def add_to_zip(
    zip_path: FilePath,
    source_paths: List[FilePath],
    compression: str = 'deflate',
    compression_level: int = DEFAULT_COMPRESSION_LEVEL,
) -> int:
    """
    Add files to an existing ZIP archive.
    
    Args:
        zip_path: Path to the ZIP file
        source_paths: Files/directories to add
        compression: Compression method
        compression_level: Compression level
        
    Returns:
        Number of files added
    """
    zip_path = Path(zip_path)
    if not zip_path.exists():
        return create_zip(zip_path, source_paths, compression, compression_level)['files']
    
    method = ZIP_COMPRESSION_METHODS.get(compression, zipfile.ZIP_DEFLATED)
    files_added = 0
    
    # Read existing contents
    existing = {}
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for name in zf.namelist():
            existing[name] = zf.read(name)
    
    # Create new archive (compresslevel requires Python 3.7+)
    import sys
    if sys.version_info >= (3, 7):
        zf_kwargs = {'compression': method, 'compresslevel': compression_level}
    else:
        zf_kwargs = {'compression': method}
    
    with zipfile.ZipFile(zip_path, 'w', **zf_kwargs) as zf:
        # Add existing files
        for name, data in existing.items():
            zf.writestr(name, data)
        
        # Add new files
        for source in source_paths:
            source = Path(source)
            if source.is_file():
                zf.write(source, source.name)
                files_added += 1
            elif source.is_dir():
                for root, dirs, files in os.walk(source):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = str(file_path.relative_to(source))
                        zf.write(file_path, arcname)
                        files_added += 1
    
    return files_added


# =============================================================================
# GZIP Operations
# =============================================================================

def gzip_compress(
    input_path: FilePath,
    output_path: Optional[FilePath] = None,
    compression_level: int = DEFAULT_COMPRESSION_LEVEL,
    keep_original: bool = True,
) -> str:
    """
    Compress a file using GZIP.
    
    Args:
        input_path: Path to the file to compress
        output_path: Output path (default: input_path + '.gz')
        compression_level: Compression level (0-9)
        keep_original: Whether to keep the original file
        
    Returns:
        Path to the compressed file
        
    Example:
        >>> gz_path = gzip_compress('document.txt')
        >>> print(f"Compressed to: {gz_path}")
    """
    input_path = Path(input_path)
    if output_path is None:
        output_path = Path(str(input_path) + '.gz')
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(input_path, 'rb') as f_in:
        with gzip.open(output_path, 'wb', compresslevel=compression_level) as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    if not keep_original:
        input_path.unlink()
    
    return str(output_path)


def gzip_decompress(
    input_path: FilePath,
    output_path: Optional[FilePath] = None,
    keep_original: bool = True,
) -> str:
    """
    Decompress a GZIP file.
    
    Args:
        input_path: Path to the GZIP file
        output_path: Output path (default: input_path without '.gz')
        keep_original: Whether to keep the original file
        
    Returns:
        Path to the decompressed file
    """
    input_path = Path(input_path)
    if output_path is None:
        output_path = Path(input_path.stem)  # Remove .gz
        if output_path.suffix == '':
            output_path = Path(str(input_path)[:-3])
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with gzip.open(input_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    if not keep_original:
        input_path.unlink()
    
    return str(output_path)


def gzip_compress_bytes(data: bytes, compression_level: int = DEFAULT_COMPRESSION_LEVEL) -> bytes:
    """Compress bytes data using GZIP."""
    return gzip.compress(data, compresslevel=compression_level)


def gzip_decompress_bytes(data: bytes) -> bytes:
    """Decompress GZIP bytes data."""
    return gzip.decompress(data)


# =============================================================================
# BZ2 Operations
# =============================================================================

def bz2_compress(
    input_path: FilePath,
    output_path: Optional[FilePath] = None,
    compression_level: int = DEFAULT_COMPRESSION_LEVEL,
    keep_original: bool = True,
) -> str:
    """
    Compress a file using BZ2.
    
    Args:
        input_path: Path to the file to compress
        output_path: Output path (default: input_path + '.bz2')
        compression_level: Compression level (1-9)
        keep_original: Whether to keep the original file
        
    Returns:
        Path to the compressed file
    """
    input_path = Path(input_path)
    if output_path is None:
        output_path = Path(str(input_path) + '.bz2')
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(input_path, 'rb') as f_in:
        with bz2.open(output_path, 'wb', compresslevel=compression_level) as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    if not keep_original:
        input_path.unlink()
    
    return str(output_path)


def bz2_decompress(
    input_path: FilePath,
    output_path: Optional[FilePath] = None,
    keep_original: bool = True,
) -> str:
    """
    Decompress a BZ2 file.
    
    Args:
        input_path: Path to the BZ2 file
        output_path: Output path (default: input_path without '.bz2')
        keep_original: Whether to keep the original file
        
    Returns:
        Path to the decompressed file
    """
    input_path = Path(input_path)
    if output_path is None:
        output_path = Path(str(input_path)[:-4])  # Remove .bz2
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with bz2.open(input_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    if not keep_original:
        input_path.unlink()
    
    return str(output_path)


def bz2_compress_bytes(data: bytes, compression_level: int = DEFAULT_COMPRESSION_LEVEL) -> bytes:
    """Compress bytes data using BZ2."""
    return bz2.compress(data, compresslevel=compression_level)


def bz2_decompress_bytes(data: bytes) -> bytes:
    """Decompress BZ2 bytes data."""
    return bz2.decompress(data)


# =============================================================================
# LZMA/XZ Operations
# =============================================================================

def lzma_compress(
    input_path: FilePath,
    output_path: Optional[FilePath] = None,
    compression_level: int = DEFAULT_COMPRESSION_LEVEL,
    keep_original: bool = True,
) -> str:
    """
    Compress a file using LZMA.
    
    Args:
        input_path: Path to the file to compress
        output_path: Output path (default: input_path + '.xz')
        compression_level: Compression level (0-9)
        keep_original: Whether to keep the original file
        
    Returns:
        Path to the compressed file
    """
    input_path = Path(input_path)
    if output_path is None:
        output_path = Path(str(input_path) + '.xz')
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(input_path, 'rb') as f_in:
        with lzma.open(output_path, 'wb', preset=compression_level) as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    if not keep_original:
        input_path.unlink()
    
    return str(output_path)


def lzma_decompress(
    input_path: FilePath,
    output_path: Optional[FilePath] = None,
    keep_original: bool = True,
) -> str:
    """
    Decompress an LZMA/XZ file.
    
    Args:
        input_path: Path to the LZMA/XZ file
        output_path: Output path (default: input_path without '.xz')
        keep_original: Whether to keep the original file
        
    Returns:
        Path to the decompressed file
    """
    input_path = Path(input_path)
    if output_path is None:
        output_path = Path(str(input_path)[:-3])  # Remove .xz
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with lzma.open(input_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    if not keep_original:
        input_path.unlink()
    
    return str(output_path)


def lzma_compress_bytes(data: bytes, compression_level: int = DEFAULT_COMPRESSION_LEVEL) -> bytes:
    """Compress bytes data using LZMA."""
    return lzma.compress(data, preset=compression_level)


def lzma_decompress_bytes(data: bytes) -> bytes:
    """Decompress LZMA bytes data."""
    return lzma.decompress(data)


# =============================================================================
# TAR Operations
# =============================================================================

def create_tar(
    output_path: FilePath,
    source_paths: List[FilePath],
    compression: Optional[str] = None,
    base_path: Optional[FilePath] = None,
) -> Dict[str, Any]:
    """
    Create a TAR archive from files and/or directories.
    
    Args:
        output_path: Path to the output TAR file
        source_paths: List of files and/or directories to compress
        compression: Compression type (None, 'gz', 'bz2', 'xz')
        base_path: Base path to strip from archive paths
        
    Returns:
        Dict with statistics: {'files': count, 'size': bytes}
        
    Example:
        >>> result = create_tar('archive.tar.gz', ['dir1/'], compression='gz')
        >>> print(f"Created archive with {result['files']} files")
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    mode = TAR_COMPRESSION_MODES.get(compression, 'w')
    
    files_added = 0
    total_size = 0
    
    with tarfile.open(output_path, mode) as tf:
        for source in source_paths:
            source = Path(source)
            if not source.exists():
                raise FileNotFoundError(f"Source path not found: {source}")
            
            if base_path:
                arcname = str(source.relative_to(Path(base_path)))
            else:
                arcname = source.name
            
            tf.add(source, arcname)
            
            if source.is_file():
                files_added += 1
                total_size += source.stat().st_size
            elif source.is_dir():
                for root, dirs, files in os.walk(source):
                    for file in files:
                        files_added += 1
                        total_size += (Path(root) / file).stat().st_size
    
    return {
        'files': files_added,
        'size': output_path.stat().st_size,
        'original_size': total_size,
    }


def extract_tar(
    tar_path: FilePath,
    extract_to: FilePath = '.',
    members: Optional[List[str]] = None,
) -> List[str]:
    """
    Extract files from a TAR archive.
    
    Args:
        tar_path: Path to the TAR file
        extract_to: Directory to extract files to
        members: Specific members to extract (None = all)
        
    Returns:
        List of extracted file paths
    """
    tar_path = Path(tar_path)
    extract_to = Path(extract_to)
    extract_to.mkdir(parents=True, exist_ok=True)
    
    extracted = []
    
    with tarfile.open(tar_path, 'r:*') as tf:
        names_to_extract = members if members else tf.getnames()
        
        for name in names_to_extract:
            try:
                tf.extract(name, extract_to)
                extracted.append(str(extract_to / name))
            except Exception as e:
                print(f"Warning: Could not extract {name}: {e}")
    
    return extracted


def list_tar_contents(tar_path: FilePath) -> List[Dict[str, Any]]:
    """
    List contents of a TAR archive with detailed information.
    
    Args:
        tar_path: Path to the TAR file
        
    Returns:
        List of dicts with file info
    """
    tar_path = Path(tar_path)
    contents = []
    
    with tarfile.open(tar_path, 'r:*') as tf:
        for member in tf.getmembers():
            contents.append({
                'name': member.name,
                'size': member.size,
                'is_dir': member.isdir(),
                'is_file': member.isfile(),
                'mode': oct(member.mode),
                'datetime': datetime.fromtimestamp(member.mtime).isoformat(),
                'uid': member.uid,
                'gid': member.gid,
            })
    
    return contents


def append_to_tar(
    tar_path: FilePath,
    source_paths: List[FilePath],
    compression: Optional[str] = None,
) -> int:
    """
    Append files to an existing TAR archive.
    
    Note: This recreates the archive as TAR doesn't support true appending.
    
    Args:
        tar_path: Path to the TAR file
        source_paths: Files/directories to append
        compression: Compression type
        
    Returns:
        Number of files added
    """
    tar_path = Path(tar_path)
    if not tar_path.exists():
        return create_tar(tar_path, source_paths, compression)['files']
    
    # Read existing contents to temp
    temp_tar = tar_path.with_suffix(tar_path.suffix + '.tmp')
    mode = TAR_COMPRESSION_MODES.get(compression, 'w')
    
    files_added = 0
    
    # Copy existing archive
    shutil.copy2(tar_path, temp_tar)
    
    with tarfile.open(temp_tar, 'r:*') as tf_in:
        existing_names = tf_in.getnames()
    
    with tarfile.open(tar_path, mode) as tf_out:
        # Add existing files
        with tarfile.open(temp_tar, 'r:*') as tf_in:
            for name in existing_names:
                member = tf_in.getmember(name)
                if member.isfile():
                    f = tf_in.extractfile(member)
                    if f:
                        tf_out.addfile(member, f)
                else:
                    tf_out.addfile(member)
        
        # Add new files
        for source in source_paths:
            source = Path(source)
            tf_out.add(source)
            if source.is_file():
                files_added += 1
            elif source.is_dir():
                for root, dirs, files in os.walk(source):
                    files_added += len(files)
    
    temp_tar.unlink()
    
    return files_added


# =============================================================================
# Utility Functions
# =============================================================================

def get_compression_ratio(original_size: int, compressed_size: int) -> str:
    """
    Calculate compression ratio as a percentage.
    
    Args:
        original_size: Original file size in bytes
        compressed_size: Compressed file size in bytes
        
    Returns:
        Compression ratio as percentage string
    """
    if original_size == 0:
        return "N/A"
    ratio = (1 - compressed_size / original_size) * 100
    return f"{ratio:.1f}%"


def format_size(size_bytes: int) -> str:
    """
    Format byte size to human-readable string.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., '1.5 MB')
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_file_info(file_path: FilePath) -> Dict[str, Any]:
    """
    Get detailed file information.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dict with file info
    """
    file_path = Path(file_path)
    stat_info = file_path.stat()
    
    return {
        'name': file_path.name,
        'path': str(file_path.absolute()),
        'size': stat_info.st_size,
        'size_formatted': format_size(stat_info.st_size),
        'created': datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
        'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
        'is_file': file_path.is_file(),
        'is_dir': file_path.is_dir(),
    }


def compare_compression_methods(
    input_path: FilePath,
    methods: List[str] = ['gzip', 'bz2', 'lzma'],
) -> Dict[str, Dict[str, Any]]:
    """
    Compare different compression methods on a file.
    
    Args:
        input_path: Path to the file to compress
        methods: List of compression methods to compare
        
    Returns:
        Dict with results for each method
    """
    input_path = Path(input_path)
    original_size = input_path.stat().st_size
    original_data = input_path.read_bytes()
    
    results = {}
    
    for method in methods:
        if method == 'gzip':
            compressed = gzip_compress_bytes(original_data)
        elif method == 'bz2':
            compressed = bz2_compress_bytes(original_data)
        elif method == 'lzma':
            compressed = lzma_compress_bytes(original_data)
        else:
            continue
        
        results[method] = {
            'compressed_size': len(compressed),
            'ratio': get_compression_ratio(original_size, len(compressed)),
            'size_formatted': format_size(len(compressed)),
        }
    
    results['original'] = {
        'size': original_size,
        'size_formatted': format_size(original_size),
    }
    
    return results


# =============================================================================
# Streaming Compression Classes
# =============================================================================

class StreamingCompressor:
    """Stream compressor for large files."""
    
    def __init__(self, algorithm: str = 'gzip', compression_level: int = DEFAULT_COMPRESSION_LEVEL):
        """
        Initialize streaming compressor.
        
        Args:
            algorithm: Compression algorithm ('gzip', 'bz2', 'lzma')
            compression_level: Compression level
        """
        self.algorithm = algorithm
        self.compression_level = compression_level
        self._compressor = None
        self._buffer = io.BytesIO()
        self._init_compressor()
    
    def _init_compressor(self):
        """Initialize the appropriate compressor."""
        if self.algorithm == 'gzip':
            self._compressor = gzip.GzipFile(fileobj=self._buffer, mode='wb', compresslevel=self.compression_level)
        elif self.algorithm == 'bz2':
            self._compressor = bz2.BZ2Compressor()
        elif self.algorithm == 'lzma':
            self._compressor = lzma.LZMACompressor(preset=self.compression_level)
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
    
    def write(self, data: bytes) -> bytes:
        """Write data to compressor and return compressed chunk."""
        if self.algorithm == 'gzip':
            self._compressor.write(data)
            return b''
        else:
            return self._compressor.compress(data)
    
    def flush(self) -> bytes:
        """Flush the compressor and return remaining compressed data."""
        if self.algorithm == 'gzip':
            self._compressor.close()
            return self._buffer.getvalue()
        else:
            return self._compressor.flush()
    
    def reset(self):
        """Reset the compressor for reuse."""
        self._buffer = io.BytesIO()
        self._init_compressor()


class StreamingDecompressor:
    """Stream decompressor for large files."""
    
    def __init__(self, algorithm: str = 'gzip'):
        """
        Initialize streaming decompressor.
        
        Args:
            algorithm: Compression algorithm ('gzip', 'bz2', 'lzma')
        """
        self.algorithm = algorithm
        self._decompressor = None
        self._init_decompressor()
    
    def _init_decompressor(self):
        """Initialize the appropriate decompressor."""
        if self.algorithm == 'gzip':
            self._buffer = io.BytesIO()
            self._decompressor = gzip.GzipFile(fileobj=self._buffer, mode='rb')
        elif self.algorithm == 'bz2':
            self._decompressor = bz2.BZ2Decompressor()
        elif self.algorithm == 'lzma':
            self._decompressor = lzma.LZMADecompressor()
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
    
    def write(self, data: bytes) -> bytes:
        """Write compressed data to decompressor and return decompressed chunk."""
        if self.algorithm == 'gzip':
            self._buffer.write(data)
            self._buffer.seek(0)
            self._decompressor = gzip.GzipFile(fileobj=self._buffer, mode='rb')
            return self._decompressor.read()
        else:
            return self._decompressor.decompress(data)
    
    def flush(self) -> bytes:
        """Flush the decompressor and return remaining data."""
        if self.algorithm == 'gzip':
            return self._decompressor.read()
        else:
            try:
                return self._decompressor.flush()
            except Exception:
                return b''
    
    def reset(self):
        """Reset the decompressor for reuse."""
        self._init_decompressor()


# =============================================================================
# Module Info
# =============================================================================

def get_module_info() -> Dict[str, Any]:
    """Get module information."""
    return {
        'name': 'Compression Utilities',
        'version': '1.0.0',
        'description': 'Comprehensive compression utilities for Python',
        'supported_formats': ['ZIP', 'GZIP', 'BZ2', 'LZMA/XZ', 'TAR'],
        'zero_dependencies': True,
        'python_version': '3.6+',
    }


if __name__ == '__main__':
    # Quick demo
    print("Compression Utilities Module")
    print("=" * 60)
    print(get_module_info())
    print("\nSupported formats: ZIP, GZIP, BZ2, LZMA/XZ, TAR")
    print("Zero external dependencies - uses Python standard library only")
