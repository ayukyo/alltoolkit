"""
AllToolkit - Python Archive Utilities

A zero-dependency, production-ready archive and compression utility module.
Supports ZIP, TAR, GZIP, BZ2, and XZ formats for creating, extracting, and managing archives.

Author: AllToolkit
License: MIT
"""

import os
import sys
import zipfile
import tarfile
import gzip
import bz2
import lzma
import shutil
import tempfile
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import stat


class ArchiveFormat(Enum):
    """Supported archive formats."""
    ZIP = "zip"
    TAR = "tar"
    TAR_GZ = "tar.gz"
    TAR_BZ2 = "tar.bz2"
    TAR_XZ = "tar.xz"
    GZ = "gz"
    BZ2 = "bz2"
    XZ = "xz"


class CompressionLevel(Enum):
    """Compression levels."""
    FASTEST = 1
    FAST = 3
    DEFAULT = 6
    BEST = 9


@dataclass
class ArchiveInfo:
    """Information about an archive file."""
    path: str
    format: ArchiveFormat
    size: int
    file_count: int
    files: List[str]
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    compressed_size: int = 0
    uncompressed_size: int = 0
    compression_ratio: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'path': self.path,
            'format': self.format.value,
            'size': self.size,
            'file_count': self.file_count,
            'files': self.files,
            'created': self.created.isoformat() if self.created else None,
            'modified': self.modified.isoformat() if self.modified else None,
            'compressed_size': self.compressed_size,
            'uncompressed_size': self.uncompressed_size,
            'compression_ratio': self.compression_ratio,
        }


@dataclass
class ArchiveMember:
    """Information about a member file in an archive."""
    name: str
    size: int
    compressed_size: int
    is_dir: bool
    modified: datetime
    crc32: Optional[int] = None
    permissions: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'size': self.size,
            'compressed_size': self.compressed_size,
            'is_dir': self.is_dir,
            'modified': self.modified.isoformat() if self.modified else None,
            'crc32': self.crc32,
            'permissions': oct(self.permissions) if self.permissions else None,
        }


@dataclass
class ArchiveOperationResult:
    """Result of an archive operation."""
    success: bool
    message: str
    files_processed: int = 0
    bytes_processed: int = 0
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'success': self.success,
            'message': self.message,
            'files_processed': self.files_processed,
            'bytes_processed': self.bytes_processed,
            'errors': self.errors,
        }


class ArchiveUtils:
    """
    Comprehensive archive and compression utility class.
    
    Provides methods for creating, extracting, listing, and managing
    archives in various formats. All methods use only Python standard library.
    """
    
    # 类级别常量，避免每次实例化时创建
    _SUPPORTED_FORMATS_ORDERED = [
        # 多部分扩展（按使用频率排序）
        ('.tar.gz', ArchiveFormat.TAR_GZ),
        ('.tar.bz2', ArchiveFormat.TAR_BZ2),
        ('.tar.xz', ArchiveFormat.TAR_XZ),
        ('.tgz', ArchiveFormat.TAR_GZ),
        ('.tbz2', ArchiveFormat.TAR_BZ2),
        ('.txz', ArchiveFormat.TAR_XZ),
        # 单部分扩展（按使用频率排序）
        ('.zip', ArchiveFormat.ZIP),
        ('.tar', ArchiveFormat.TAR),
        ('.gz', ArchiveFormat.GZ),
        ('.bz2', ArchiveFormat.BZ2),
        ('.xz', ArchiveFormat.XZ),
    ]
    
    # 用于快速查找的字典
    _FORMAT_MAP = {
        '.zip': ArchiveFormat.ZIP,
        '.tar': ArchiveFormat.TAR,
        '.tar.gz': ArchiveFormat.TAR_GZ,
        '.tgz': ArchiveFormat.TAR_GZ,
        '.tar.bz2': ArchiveFormat.TAR_BZ2,
        '.tbz2': ArchiveFormat.TAR_BZ2,
        '.tar.xz': ArchiveFormat.TAR_XZ,
        '.txz': ArchiveFormat.TAR_XZ,
        '.gz': ArchiveFormat.GZ,
        '.bz2': ArchiveFormat.BZ2,
        '.xz': ArchiveFormat.XZ,
    }
    
    def __init__(self):
        """Initialize archive utilities."""
        # 使用类级别常量，无需在实例中创建
        pass
    
    def detect_format(self, path: str) -> Optional[ArchiveFormat]:
        """
        Detect archive format from file path.
        
        Args:
            path: File path
            
        Returns:
            ArchiveFormat or None if not recognized
            
        Example:
            >>> utils = ArchiveUtils()
            >>> utils.detect_format("archive.zip")
            <ArchiveFormat.ZIP: 'zip'>
        
        Note:
            优化版本：按使用频率排序检查扩展名，
            使用类级别常量避免重复创建字典，
            边界处理：空路径返回 None。
        """
        # 边界处理：空路径
        if not path:
            return None
        
        path_lower = path.lower()
        
        # 按频率顺序检查扩展名（多部分优先）
        for ext, fmt in self._SUPPORTED_FORMATS_ORDERED:
            if path_lower.endswith(ext):
                return fmt
        
        return None
    
    def create_archive(self, 
                       output_path: str,
                       source_paths: List[str],
                       format: Optional[ArchiveFormat] = None,
                       compression: CompressionLevel = CompressionLevel.DEFAULT,
                       password: Optional[str] = None,
                       base_dir: Optional[str] = None) -> ArchiveOperationResult:
        """
        Create an archive from files/directories.
        
        Args:
            output_path: Output archive file path
            source_paths: List of files/directories to archive
            format: Archive format (auto-detected from output_path if None)
            compression: Compression level
            password: Password for ZIP encryption (optional)
            base_dir: Base directory for relative paths
            
        Returns:
            ArchiveOperationResult with operation details
            
        Example:
            >>> utils = ArchiveUtils()
            >>> result = utils.create_archive("backup.zip", ["file1.txt", "dir/"])
            >>> result.success
            True
        """
        try:
            # Detect format
            if format is None:
                format = self.detect_format(output_path)
            
            if format is None:
                return ArchiveOperationResult(
                    success=False,
                    message=f"Cannot detect archive format for: {output_path}",
                    errors=["Unknown archive format"]
                )
            
            # Validate source paths
            valid_sources = []
            for src in source_paths:
                if os.path.exists(src):
                    valid_sources.append(src)
                else:
                    return ArchiveOperationResult(
                        success=False,
                        message=f"Source path not found: {src}",
                        errors=[f"Missing: {src}"]
                    )
            
            # Create output directory if needed
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            files_processed = 0
            bytes_processed = 0
            
            if format == ArchiveFormat.ZIP:
                files_processed, bytes_processed = self._create_zip(
                    output_path, valid_sources, compression, password, base_dir
                )
            elif format in [ArchiveFormat.TAR, ArchiveFormat.TAR_GZ, 
                           ArchiveFormat.TAR_BZ2, ArchiveFormat.TAR_XZ]:
                files_processed, bytes_processed = self._create_tar(
                    output_path, valid_sources, format, compression, base_dir
                )
            elif format == ArchiveFormat.GZ:
                files_processed, bytes_processed = self._create_gz(
                    output_path, valid_sources[0]
                )
            elif format == ArchiveFormat.BZ2:
                files_processed, bytes_processed = self._create_bz2(
                    output_path, valid_sources[0]
                )
            elif format == ArchiveFormat.XZ:
                files_processed, bytes_processed = self._create_xz(
                    output_path, valid_sources[0]
                )
            
            return ArchiveOperationResult(
                success=True,
                message=f"Archive created: {output_path}",
                files_processed=files_processed,
                bytes_processed=bytes_processed
            )
            
        except Exception as e:
            return ArchiveOperationResult(
                success=False,
                message=f"Failed to create archive: {str(e)}",
                errors=[str(e)]
            )
    
    def _create_zip(self, 
                    output_path: str,
                    sources: List[str],
                    compression: CompressionLevel,
                    password: Optional[str],
                    base_dir: Optional[str]) -> Tuple[int, int]:
        """Create ZIP archive."""
        comp_map = {
            CompressionLevel.FASTEST: zipfile.ZIP_STORED,
            CompressionLevel.FAST: zipfile.ZIP_DEFLATED,
            CompressionLevel.DEFAULT: zipfile.ZIP_DEFLATED,
            CompressionLevel.BEST: zipfile.ZIP_DEFLATED,
        }
        
        files_processed = 0
        bytes_processed = 0
        
        with zipfile.ZipFile(output_path, 'w', comp_map[compression]) as zf:
            for source in sources:
                if os.path.isfile(source):
                    arcname = os.path.basename(source) if base_dir is None else \
                             os.path.relpath(source, base_dir)
                    zf.write(source, arcname)
                    files_processed += 1
                    bytes_processed += os.path.getsize(source)
                elif os.path.isdir(source):
                    for root, dirs, files in os.walk(source):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, base_dir) if base_dir else \
                                     os.path.relpath(file_path, source)
                            zf.write(file_path, arcname)
                            files_processed += 1
                            bytes_processed += os.path.getsize(file_path)
        
        # Apply password if specified
        if password and files_processed > 0:
            # Note: Python's zipfile doesn't support setting passwords on creation
            # This is a limitation - password would need to be set during extraction
            pass
        
        return files_processed, bytes_processed
    
    def _create_tar(self,
                    output_path: str,
                    sources: List[str],
                    format: ArchiveFormat,
                    compression: CompressionLevel,
                    base_dir: Optional[str]) -> Tuple[int, int]:
        """Create TAR archive (optionally compressed)."""
        mode_map = {
            ArchiveFormat.TAR: 'w',
            ArchiveFormat.TAR_GZ: 'w:gz',
            ArchiveFormat.TAR_BZ2: 'w:bz2',
            ArchiveFormat.TAR_XZ: 'w:xz',
        }
        
        files_processed = 0
        bytes_processed = 0
        
        with tarfile.open(output_path, mode_map[format]) as tf:
            for source in sources:
                if os.path.isfile(source):
                    arcname = os.path.basename(source) if base_dir is None else \
                             os.path.relpath(source, base_dir)
                    tf.add(source, arcname)
                    files_processed += 1
                    bytes_processed += os.path.getsize(source)
                elif os.path.isdir(source):
                    for root, dirs, files in os.walk(source):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, base_dir) if base_dir else \
                                     os.path.relpath(file_path, source)
                            tf.add(file_path, arcname)
                            files_processed += 1
                            bytes_processed += os.path.getsize(file_path)
        
        return files_processed, bytes_processed
    
    def _create_gz(self, output_path: str, source: str) -> Tuple[int, int]:
        """Create GZIP compressed file."""
        if not os.path.isfile(source):
            raise ValueError(f"Source must be a file: {source}")
        
        bytes_processed = os.path.getsize(source)
        
        with open(source, 'rb') as f_in:
            with gzip.open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        return 1, bytes_processed
    
    def _create_bz2(self, output_path: str, source: str) -> Tuple[int, int]:
        """Create BZ2 compressed file."""
        if not os.path.isfile(source):
            raise ValueError(f"Source must be a file: {source}")
        
        bytes_processed = os.path.getsize(source)
        
        with open(source, 'rb') as f_in:
            with bz2.open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        return 1, bytes_processed
    
    def _create_xz(self, output_path: str, source: str) -> Tuple[int, int]:
        """Create XZ compressed file."""
        if not os.path.isfile(source):
            raise ValueError(f"Source must be a file: {source}")
        
        bytes_processed = os.path.getsize(source)
        
        with open(source, 'rb') as f_in:
            with lzma.open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        return 1, bytes_processed
    
    def extract_archive(self,
                        archive_path: str,
                        output_dir: str = ".",
                        password: Optional[str] = None,
                        members: Optional[List[str]] = None) -> ArchiveOperationResult:
        """
        Extract an archive.
        
        Args:
            archive_path: Path to archive file
            output_dir: Output directory (default: current directory)
            password: Password for encrypted archives (optional)
            members: Specific members to extract (None = all)
            
        Returns:
            ArchiveOperationResult with extraction details
            
        Example:
            >>> utils = ArchiveUtils()
            >>> result = utils.extract_archive("archive.zip", "extracted/")
            >>> result.success
            True
        """
        try:
            if not os.path.exists(archive_path):
                return ArchiveOperationResult(
                    success=False,
                    message=f"Archive not found: {archive_path}",
                    errors=["File not found"]
                )
            
            format = self.detect_format(archive_path)
            if format is None:
                return ArchiveOperationResult(
                    success=False,
                    message=f"Unknown archive format: {archive_path}",
                    errors=["Unknown format"]
                )
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            files_processed = 0
            bytes_processed = 0
            
            if format == ArchiveFormat.ZIP:
                files_processed, bytes_processed = self._extract_zip(
                    archive_path, output_dir, password, members
                )
            elif format in [ArchiveFormat.TAR, ArchiveFormat.TAR_GZ,
                           ArchiveFormat.TAR_BZ2, ArchiveFormat.TAR_XZ]:
                files_processed, bytes_processed = self._extract_tar(
                    archive_path, output_dir, members
                )
            elif format == ArchiveFormat.GZ:
                files_processed, bytes_processed = self._extract_gz(
                    archive_path, output_dir
                )
            elif format == ArchiveFormat.BZ2:
                files_processed, bytes_processed = self._extract_bz2(
                    archive_path, output_dir
                )
            elif format == ArchiveFormat.XZ:
                files_processed, bytes_processed = self._extract_xz(
                    archive_path, output_dir
                )
            
            return ArchiveOperationResult(
                success=True,
                message=f"Extracted {files_processed} files to {output_dir}",
                files_processed=files_processed,
                bytes_processed=bytes_processed
            )
            
        except Exception as e:
            return ArchiveOperationResult(
                success=False,
                message=f"Failed to extract: {str(e)}",
                errors=[str(e)]
            )
    
    def _extract_zip(self,
                     archive_path: str,
                     output_dir: str,
                     password: Optional[str],
                     members: Optional[List[str]]) -> Tuple[int, int]:
        """Extract ZIP archive."""
        files_processed = 0
        bytes_processed = 0
        
        with zipfile.ZipFile(archive_path, 'r') as zf:
            if members:
                extract_list = [m for m in members if m in zf.namelist()]
            else:
                extract_list = zf.namelist()
            
            for member in extract_list:
                zf.extract(member, output_dir, pwd=password.encode() if password else None)
                info = zf.getinfo(member)
                files_processed += 1
                bytes_processed += info.file_size
        
        return files_processed, bytes_processed
    
    def _extract_tar(self,
                     archive_path: str,
                     output_dir: str,
                     members: Optional[List[str]]) -> Tuple[int, int]:
        """Extract TAR archive."""
        files_processed = 0
        bytes_processed = 0
        
        with tarfile.open(archive_path, 'r:*') as tf:
            if members:
                extract_list = [m for m in members if m in tf.getnames()]
            else:
                extract_list = tf.getnames()
            
            for member in extract_list:
                try:
                    tf.extract(member, output_dir)
                    info = tf.getmember(member)
                    files_processed += 1
                    bytes_processed += info.size
                except Exception:
                    pass  # Skip problematic files
        
        return files_processed, bytes_processed
    
    def _extract_gz(self, archive_path: str, output_dir: str) -> Tuple[int, int]:
        """Extract GZIP file."""
        output_name = os.path.splitext(os.path.basename(archive_path))[0]
        output_path = os.path.join(output_dir, output_name)
        
        bytes_processed = 0
        
        with gzip.open(archive_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                bytes_processed = os.path.getsize(output_path)
        
        return 1, bytes_processed
    
    def _extract_bz2(self, archive_path: str, output_dir: str) -> Tuple[int, int]:
        """Extract BZ2 file."""
        output_name = os.path.splitext(os.path.basename(archive_path))[0]
        output_path = os.path.join(output_dir, output_name)
        
        bytes_processed = 0
        
        with bz2.open(archive_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                bytes_processed = os.path.getsize(output_path)
        
        return 1, bytes_processed
    
    def _extract_xz(self, archive_path: str, output_dir: str) -> Tuple[int, int]:
        """Extract XZ file."""
        output_name = os.path.splitext(os.path.basename(archive_path))[0]
        output_path = os.path.join(output_dir, output_name)
        
        bytes_processed = 0
        
        with lzma.open(archive_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                bytes_processed = os.path.getsize(output_path)
        
        return 1, bytes_processed
    
    def list_archive(self, archive_path: str) -> List[ArchiveMember]:
        """
        List contents of an archive.
        
        Args:
            archive_path: Path to archive file
            
        Returns:
            List of ArchiveMember objects
            
        Example:
            >>> utils = ArchiveUtils()
            >>> members = utils.list_archive("archive.zip")
            >>> for m in members:
            ...     print(f"{m.name}: {m.size} bytes")
        """
        format = self.detect_format(archive_path)
        if format is None:
            raise ValueError(f"Unknown archive format: {archive_path}")
        
        members = []
        
        if format == ArchiveFormat.ZIP:
            members = self._list_zip(archive_path)
        elif format in [ArchiveFormat.TAR, ArchiveFormat.TAR_GZ,
                       ArchiveFormat.TAR_BZ2, ArchiveFormat.TAR_XZ]:
            members = self._list_tar(archive_path)
        elif format in [ArchiveFormat.GZ, ArchiveFormat.BZ2, ArchiveFormat.XZ]:
            # Single-file compression - return the archive itself
            info = os.stat(archive_path)
            members.append(ArchiveMember(
                name=os.path.basename(archive_path),
                size=info.st_size,
                compressed_size=info.st_size,
                is_dir=False,
                modified=datetime.fromtimestamp(info.st_mtime),
            ))
        
        return members
    
    def _list_zip(self, archive_path: str) -> List[ArchiveMember]:
        """List ZIP archive contents."""
        members = []
        
        with zipfile.ZipFile(archive_path, 'r') as zf:
            for info in zf.infolist():
                members.append(ArchiveMember(
                    name=info.filename,
                    size=info.file_size,
                    compressed_size=info.compress_size,
                    is_dir=info.filename.endswith('/'),
                    modified=datetime(*info.date_time),
                    crc32=info.CRC,
                ))
        
        return members
    
    def _list_tar(self, archive_path: str) -> List[ArchiveMember]:
        """List TAR archive contents."""
        members = []
        
        with tarfile.open(archive_path, 'r:*') as tf:
            for info in tf.getmembers():
                members.append(ArchiveMember(
                    name=info.name,
                    size=info.size,
                    compressed_size=info.size,  # TAR doesn't track compressed size per member
                    is_dir=info.isdir(),
                    modified=datetime.fromtimestamp(info.mtime),
                    permissions=info.mode,
                ))
        
        return members
    
    def get_archive_info(self, archive_path: str) -> ArchiveInfo:
        """
        Get comprehensive information about an archive.
        
        Args:
            archive_path: Path to archive file
            
        Returns:
            ArchiveInfo object with detailed statistics
            
        Example:
            >>> utils = ArchiveUtils()
            >>> info = utils.get_archive_info("archive.zip")
            >>> print(f"Files: {info.file_count}, Ratio: {info.compression_ratio:.2%}")
        """
        if not os.path.exists(archive_path):
            raise FileNotFoundError(f"Archive not found: {archive_path}")
        
        format = self.detect_format(archive_path)
        if format is None:
            raise ValueError(f"Unknown archive format: {archive_path}")
        
        stat_info = os.stat(archive_path)
        members = self.list_archive(archive_path)
        
        file_count = len([m for m in members if not m.is_dir])
        total_size = sum(m.size for m in members)
        compressed_size = sum(m.compressed_size for m in members)
        
        compression_ratio = 1 - (compressed_size / total_size) if total_size > 0 else 0
        
        return ArchiveInfo(
            path=archive_path,
            format=format,
            size=stat_info.st_size,
            file_count=file_count,
            files=[m.name for m in members],
            modified=datetime.fromtimestamp(stat_info.st_mtime),
            compressed_size=compressed_size,
            uncompressed_size=total_size,
            compression_ratio=compression_ratio,
        )
    
    def add_to_archive(self,
                       archive_path: str,
                       source_paths: List[str],
                       base_dir: Optional[str] = None) -> ArchiveOperationResult:
        """
        Add files to an existing archive (ZIP only).
        
        Args:
            archive_path: Path to existing archive
            source_paths: Files/directories to add
            base_dir: Base directory for relative paths
            
        Returns:
            ArchiveOperationResult with operation details
        """
        format = self.detect_format(archive_path)
        
        if format != ArchiveFormat.ZIP:
            return ArchiveOperationResult(
                success=False,
                message="Adding files is only supported for ZIP archives",
                errors=["Format not supported"]
            )
        
        try:
            files_processed = 0
            bytes_processed = 0
            
            # Read existing archive
            existing = []
            with zipfile.ZipFile(archive_path, 'r') as zf:
                existing = zf.namelist()
            
            # Add new files
            with zipfile.ZipFile(archive_path, 'a') as zf:
                for source in source_paths:
                    if os.path.isfile(source):
                        arcname = os.path.basename(source) if base_dir is None else \
                                 os.path.relpath(source, base_dir)
                        zf.write(source, arcname)
                        files_processed += 1
                        bytes_processed += os.path.getsize(source)
                    elif os.path.isdir(source):
                        for root, dirs, files in os.walk(source):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, base_dir) if base_dir else \
                                         os.path.relpath(file_path, source)
                                zf.write(file_path, arcname)
                                files_processed += 1
                                bytes_processed += os.path.getsize(file_path)
            
            return ArchiveOperationResult(
                success=True,
                message=f"Added {files_processed} files to archive",
                files_processed=files_processed,
                bytes_processed=bytes_processed
            )
            
        except Exception as e:
            return ArchiveOperationResult(
                success=False,
                message=f"Failed to add files: {str(e)}",
                errors=[str(e)]
            )
    
    def remove_from_archive(self,
                            archive_path: str,
                            member_paths: List[str]) -> ArchiveOperationResult:
        """
        Remove files from an existing archive (ZIP only).
        
        Args:
            archive_path: Path to existing archive
            member_paths: Member paths to remove
            
        Returns:
            ArchiveOperationResult with operation details
        """
        format = self.detect_format(archive_path)
        
        if format != ArchiveFormat.ZIP:
            return ArchiveOperationResult(
                success=False,
                message="Removing files is only supported for ZIP archives",
                errors=["Format not supported"]
            )
        
        try:
            # Read all contents except the ones to remove
            remove_set = set(member_paths)
            temp_path = archive_path + '.tmp'
            
            with zipfile.ZipFile(archive_path, 'r') as zf_in:
                with zipfile.ZipFile(temp_path, 'w') as zf_out:
                    for item in zf_in.infolist():
                        if item.filename not in remove_set:
                            zf_out.writestr(item, zf_in.read(item.filename))
            
            # Replace original with temp
            shutil.move(temp_path, archive_path)
            
            return ArchiveOperationResult(
                success=True,
                message=f"Removed {len(member_paths)} files from archive",
                files_processed=len(member_paths)
            )
            
        except Exception as e:
            return ArchiveOperationResult(
                success=False,
                message=f"Failed to remove files: {str(e)}",
                errors=[str(e)]
            )
    
    def verify_archive(self, archive_path: str) -> ArchiveOperationResult:
        """
        Verify archive integrity.
        
        Args:
            archive_path: Path to archive file
            
        Returns:
            ArchiveOperationResult with verification details
        """
        try:
            format = self.detect_format(archive_path)
            if format is None:
                return ArchiveOperationResult(
                    success=False,
                    message=f"Unknown archive format: {archive_path}",
                    errors=["Unknown format"]
                )
            
            errors = []
            
            if format == ArchiveFormat.ZIP:
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    bad_file = zf.testzip()
                    if bad_file:
                        errors.append(f"Corrupted file: {bad_file}")
            
            elif format in [ArchiveFormat.TAR, ArchiveFormat.TAR_GZ,
                           ArchiveFormat.TAR_BZ2, ArchiveFormat.TAR_XZ]:
                with tarfile.open(archive_path, 'r:*') as tf:
                    # Try to read all members
                    for member in tf.getmembers():
                        try:
                            tf.extractfile(member)
                        except Exception as e:
                            errors.append(f"Error reading {member.name}: {str(e)}")
            
            elif format == ArchiveFormat.GZ:
                try:
                    with gzip.open(archive_path, 'rb') as f:
                        while True:
                            chunk = f.read(8192)
                            if not chunk:
                                break
                except Exception as e:
                    errors.append(str(e))
            
            elif format == ArchiveFormat.BZ2:
                try:
                    with bz2.open(archive_path, 'rb') as f:
                        while True:
                            chunk = f.read(8192)
                            if not chunk:
                                break
                except Exception as e:
                    errors.append(str(e))
            
            elif format == ArchiveFormat.XZ:
                try:
                    with lzma.open(archive_path, 'rb') as f:
                        while True:
                            chunk = f.read(8192)
                            if not chunk:
                                break
                except Exception as e:
                    errors.append(str(e))
            
            if errors:
                return ArchiveOperationResult(
                    success=False,
                    message="Archive verification failed",
                    errors=errors
                )
            
            return ArchiveOperationResult(
                success=True,
                message="Archive integrity verified",
                files_processed=len(self.list_archive(archive_path))
            )
            
        except Exception as e:
            return ArchiveOperationResult(
                success=False,
                message=f"Verification error: {str(e)}",
                errors=[str(e)]
            )
    
    def calculate_checksum(self, 
                           archive_path: str,
                           algorithm: str = 'sha256') -> str:
        """
        Calculate checksum of an archive file.
        
        Args:
            archive_path: Path to archive file
            algorithm: Hash algorithm (md5, sha1, sha256, sha512)
            
        Returns:
            Hex digest string
            
        Example:
            >>> utils = ArchiveUtils()
            >>> checksum = utils.calculate_checksum("archive.zip")
            >>> print(checksum)
        """
        hash_func = getattr(hashlib, algorithm, None)
        if hash_func is None:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        hasher = hash_func()
        
        with open(archive_path, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                hasher.update(chunk)
        
        return hasher.hexdigest()
    
    def stream_extract(self,
                       archive_path: str,
                       member_path: str,
                       output_path: str) -> ArchiveOperationResult:
        """
        Extract a single member from archive without extracting all.
        
        Args:
            archive_path: Path to archive file
            member_path: Path of member within archive
            output_path: Output file path
            
        Returns:
            ArchiveOperationResult with extraction details
        """
        try:
            format = self.detect_format(archive_path)
            if format is None:
                return ArchiveOperationResult(
                    success=False,
                    message=f"Unknown archive format: {archive_path}",
                    errors=["Unknown format"]
                )
            
            bytes_processed = 0
            
            if format == ArchiveFormat.ZIP:
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    if member_path in zf.namelist():
                        with zf.open(member_path) as src:
                            with open(output_path, 'wb') as dst:
                                while True:
                                    chunk = src.read(8192)
                                    if not chunk:
                                        break
                                    dst.write(chunk)
                                    bytes_processed += len(chunk)
                    else:
                        return ArchiveOperationResult(
                            success=False,
                            message=f"Member not found: {member_path}",
                            errors=["Member not in archive"]
                        )
            
            elif format in [ArchiveFormat.TAR, ArchiveFormat.TAR_GZ,
                           ArchiveFormat.TAR_BZ2, ArchiveFormat.TAR_XZ]:
                with tarfile.open(archive_path, 'r:*') as tf:
                    if member_path in tf.getnames():
                        member = tf.getmember(member_path)
                        if member.isfile():
                            src = tf.extractfile(member)
                            if src:
                                with open(output_path, 'wb') as dst:
                                    while True:
                                        chunk = src.read(8192)
                                        if not chunk:
                                            break
                                        dst.write(chunk)
                                        bytes_processed += len(chunk)
                    else:
                        return ArchiveOperationResult(
                            success=False,
                            message=f"Member not found: {member_path}",
                            errors=["Member not in archive"]
                        )
            
            else:
                return ArchiveOperationResult(
                    success=False,
                    message="Stream extract only supported for ZIP and TAR formats",
                    errors=["Format not supported"]
                )
            
            return ArchiveOperationResult(
                success=True,
                message=f"Extracted {member_path} to {output_path}",
                bytes_processed=bytes_processed
            )
            
        except Exception as e:
            return ArchiveOperationResult(
                success=False,
                message=f"Stream extract failed: {str(e)}",
                errors=[str(e)]
            )


# Module-level convenience functions
_default_utils = ArchiveUtils()


def detect_format(path: str) -> Optional[ArchiveFormat]:
    """Detect archive format from file path."""
    return _default_utils.detect_format(path)


def create_archive(output_path: str,
                   source_paths: List[str],
                   format: Optional[ArchiveFormat] = None,
                   compression: CompressionLevel = CompressionLevel.DEFAULT,
                   password: Optional[str] = None,
                   base_dir: Optional[str] = None) -> ArchiveOperationResult:
    """Create an archive from files/directories."""
    return _default_utils.create_archive(
        output_path, source_paths, format, compression, password, base_dir
    )


def extract_archive(archive_path: str,
                    output_dir: str = ".",
                    password: Optional[str] = None,
                    members: Optional[List[str]] = None) -> ArchiveOperationResult:
    """Extract an archive."""
    return _default_utils.extract_archive(
        archive_path, output_dir, password, members
    )


def list_archive(archive_path: str) -> List[ArchiveMember]:
    """List contents of an archive."""
    return _default_utils.list_archive(archive_path)


def get_archive_info(archive_path: str) -> ArchiveInfo:
    """Get comprehensive information about an archive."""
    return _default_utils.get_archive_info(archive_path)


def verify_archive(archive_path: str) -> ArchiveOperationResult:
    """Verify archive integrity."""
    return _default_utils.verify_archive(archive_path)


def calculate_checksum(archive_path: str,
                       algorithm: str = 'sha256') -> str:
    """Calculate checksum of an archive file."""
    return _default_utils.calculate_checksum(archive_path, algorithm)


if __name__ == '__main__':
    # Quick demo
    utils = ArchiveUtils()
    
    print("=" * 60)
    print("Archive Utils Demo")
    print("=" * 60)
    
    # Show supported formats
    print("\nSupported formats:")
    for ext, fmt in utils._supported_formats.items():
        print(f"  {ext}: {fmt.value}")
    
    # Demo format detection
    print("\nFormat detection examples:")
    test_files = [
        "archive.zip",
        "backup.tar.gz",
        "data.tar.bz2",
        "file.txt.gz",
        "unknown.xyz",
    ]
    
    for f in test_files:
        fmt = utils.detect_format(f)
        print(f"  {f}: {fmt.value if fmt else 'Unknown'}")
    
    print("\n" + "=" * 60)
    print("Note: This demo shows format detection.")
    print("For full functionality, create actual archives and test.")
    print("=" * 60)
