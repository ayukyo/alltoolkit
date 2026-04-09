#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compression Utils - Batch Compression Example

Demonstrates batch compression of multiple files and directories.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path (compression_utils folder)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    create_zip, create_tar, gzip_compress,
    format_size, get_compression_ratio,
    get_file_info,
)


def batch_compress_directory(
    source_dir: Path,
    output_dir: Path,
    formats: list = ['zip', 'tar.gz'],
    include_patterns: list = None,
    exclude_patterns: list = None,
) -> dict:
    """
    Batch compress a directory into multiple formats.
    
    Args:
        source_dir: Directory to compress
        output_dir: Directory for output archives
        formats: List of formats to create ('zip', 'tar', 'tar.gz', 'tar.bz2', 'tar.xz')
        include_patterns: Patterns to include (e.g., ['*.txt', '*.py'])
        exclude_patterns: Patterns to exclude (e.g., ['*.pyc', '__pycache__'])
        
    Returns:
        Dict with results for each format
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    
    # Get directory name for archive naming
    dir_name = source_dir.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for fmt in formats:
        if fmt == 'zip':
            output_path = output_dir / f"{dir_name}_{timestamp}.zip"
            result = create_zip(output_path, [source_dir])
            results['zip'] = {
                'path': str(output_path),
                'size': result['compressed_size'],
                'ratio': result['ratio'],
            }
            
        elif fmt == 'tar':
            output_path = output_dir / f"{dir_name}_{timestamp}.tar"
            result = create_tar(output_path, [source_dir])
            results['tar'] = {
                'path': str(output_path),
                'size': result['size'],
                'ratio': get_compression_ratio(result['original_size'], result['size']),
            }
            
        elif fmt == 'tar.gz':
            output_path = output_dir / f"{dir_name}_{timestamp}.tar.gz"
            result = create_tar(output_path, [source_dir], compression='gz')
            results['tar.gz'] = {
                'path': str(output_path),
                'size': result['size'],
                'ratio': get_compression_ratio(result['original_size'], result['size']),
            }
            
        elif fmt == 'tar.bz2':
            output_path = output_dir / f"{dir_name}_{timestamp}.tar.bz2"
            result = create_tar(output_path, [source_dir], compression='bz2')
            results['tar.bz2'] = {
                'path': str(output_path),
                'size': result['size'],
                'ratio': get_compression_ratio(result['original_size'], result['size']),
            }
            
        elif fmt == 'tar.xz':
            output_path = output_dir / f"{dir_name}_{timestamp}.tar.xz"
            result = create_tar(output_path, [source_dir], compression='xz')
            results['tar.xz'] = {
                'path': str(output_path),
                'size': result['size'],
                'ratio': get_compression_ratio(result['original_size'], result['size']),
            }
    
    return results


def compress_log_files(log_dir: Path, output_dir: Path, max_age_days: int = 7):
    """
    Compress old log files.
    
    Args:
        log_dir: Directory containing log files
        output_dir: Directory for compressed logs
        max_age_days: Only compress files older than this
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    now = datetime.now()
    compressed_count = 0
    total_saved = 0
    
    for log_file in log_dir.glob("*.log"):
        # Check file age
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        age = (now - mtime).days
        
        if age >= max_age_days:
            # Compress the file
            gz_path = gzip_compress(log_file, output_dir / f"{log_file.name}.gz")
            
            original_size = log_file.stat().st_size
            compressed_size = Path(gz_path).unlink() if False else Path(gz_path).stat().st_size
            saved = original_size - compressed_size
            
            print(f"  Compressed: {log_file.name} ({age} days old)")
            print(f"    Saved: {format_size(saved)}")
            
            compressed_count += 1
            total_saved += saved
            
            # Remove original
            log_file.unlink()
    
    print(f"\nCompressed {compressed_count} files, saved {format_size(total_saved)}")


def create_backup(source_paths: list, backup_dir: Path, keep_versions: int = 3):
    """
    Create versioned backups.
    
    Args:
        source_paths: Files/directories to backup
        backup_dir: Directory for backups
        keep_versions: Number of backup versions to keep
    """
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"backup_{timestamp}.zip"
    backup_path = backup_dir / backup_name
    
    print(f"Creating backup: {backup_name}")
    
    result = create_zip(backup_path, source_paths, compression='deflate')
    
    print(f"  Files: {result['files']}")
    print(f"  Size: {format_size(result['compressed_size'])}")
    print(f"  Ratio: {result['ratio']}")
    
    # Cleanup old backups
    backups = sorted(backup_dir.glob("backup_*.zip"), reverse=True)
    for old_backup in backups[keep_versions:]:
        print(f"  Removing old backup: {old_backup.name}")
        old_backup.unlink()


def demo_batch_compression():
    """Demonstrate batch compression."""
    print("\n" + "="*60)
    print("Batch Compression Demo")
    print("="*60)
    
    # Create test directory structure
    test_dir = Path("demo_batch")
    test_dir.mkdir(exist_ok=True)
    
    # Create some files
    for i in range(10):
        (test_dir / f"file{i}.txt").write_text(f"Content for file {i}. " * 100)
    
    sub_dir = test_dir / "subdir"
    sub_dir.mkdir()
    for i in range(5):
        (sub_dir / f"subfile{i}.txt").write_text(f"Subfile {i} content. " * 50)
    
    # Get original size
    original_size = sum(f.stat().st_size for f in test_dir.rglob("*") if f.is_file())
    print(f"\nOriginal directory size: {format_size(original_size)}")
    
    # Batch compress
    output_dir = Path("demo_batch_output")
    results = batch_compress_directory(
        test_dir,
        output_dir,
        formats=['zip', 'tar.gz', 'tar.bz2', 'tar.xz'],
    )
    
    print("\nCompression results:")
    print("-" * 50)
    for fmt, data in results.items():
        print(f"  {fmt:8}: {format_size(data['size']):>10} ({data['ratio']:>6})")
        print(f"           {data['path']}")
    
    # Find best compression
    best = min(results.items(), key=lambda x: x[1]['size'])
    print(f"\nBest compression: {best[0]} ({best[1]['ratio']})")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    shutil.rmtree(output_dir)
    print("\nCleanup complete.")


def demo_backup_script():
    """Demonstrate backup creation."""
    print("\n" + "="*60)
    print("Backup Script Demo")
    print("="*60)
    
    # Create test files
    test_dir = Path("demo_backup_source")
    test_dir.mkdir(exist_ok=True)
    
    for i in range(5):
        (test_dir / f"important_file{i}.txt").write_text(f"Important data {i}. " * 200)
    
    backup_dir = Path("demo_backups")
    
    # Create backup
    create_backup(
        [test_dir],
        backup_dir,
        keep_versions=2,
    )
    
    # Show backup directory
    print("\nBackup directory contents:")
    for backup in sorted(backup_dir.glob("*.zip")):
        print(f"  - {backup.name}: {format_size(backup.stat().st_size)}")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    shutil.rmtree(backup_dir)
    print("\nCleanup complete.")


def main():
    """Run all demos."""
    print("\n" + "="*60)
    print("Compression Utils - Batch Compression Examples")
    print("="*60)
    
    demo_batch_compression()
    demo_backup_script()
    
    print("\n" + "="*60)
    print("All batch demos completed!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
