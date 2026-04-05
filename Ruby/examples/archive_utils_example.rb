#!/usr/bin/env ruby
# frozen_string_literal: true

# Archive Utilities Example
# Demonstrates ZIP and TAR archive operations

require_relative '../archive_utils/mod'
require 'fileutils'
require 'tempfile'

puts "=" * 60
puts "ArchiveUtils Example - Ruby Archive Operations"
puts "=" * 60
puts

# Create a temporary directory for our examples
temp_dir = Dir.mktmpdir('archive_example')
puts "Working directory: #{temp_dir}"
puts

# Create some sample files
puts "Creating sample files..."
File.write(File.join(temp_dir, 'document.txt'), 'This is a sample document.')
File.write(File.join(temp_dir, 'data.json'), '{"key": "value", "number": 42}')
File.write(File.join(temp_dir, 'readme.md'), '# README\n\nThis is a readme file.')

# Create a subdirectory with files
subdir = File.join(temp_dir, 'subdir')
FileUtils.mkdir_p(subdir)
File.write(File.join(subdir, 'nested.txt'), 'Nested file content.')
puts "Created: document.txt, data.json, readme.md, subdir/nested.txt"
puts

# ============================================================================
# ZIP Archive Examples
# ============================================================================

puts "-" * 60
puts "ZIP Archive Operations"
puts "-" * 60

# Example 1: Create a ZIP archive
puts "\n1. Creating ZIP archive..."
zip_path = File.join(temp_dir, 'archive.zip')
AllToolkit::ArchiveUtils.create_zip(zip_path, [
  File.join(temp_dir, 'document.txt'),
  File.join(temp_dir, 'data.json'),
  File.join(temp_dir, 'readme.md')
])
puts "   Created: #{zip_path}"
puts "   Size: #{File.size(zip_path)} bytes"

# Example 2: List ZIP contents
puts "\n2. Listing ZIP contents..."
entries = AllToolkit::ArchiveUtils.list_zip(zip_path)
entries.each do |entry|
  puts "   - #{entry.name} (#{entry.size} bytes, #{entry.compression_ratio.round(1)}% compressed)"
end

# Example 3: Get ZIP statistics
puts "\n3. ZIP statistics..."
stats = AllToolkit::ArchiveUtils.zip_stats(zip_path)
puts "   #{stats}"

# Example 4: Validate ZIP
puts "\n4. Validating ZIP..."
valid = AllToolkit::ArchiveUtils.valid_zip?(zip_path)
puts "   Valid: #{valid}"

# Example 5: Extract ZIP
puts "\n5. Extracting ZIP..."
extract_dir = File.join(temp_dir, 'extracted_zip')
extracted = AllToolkit::ArchiveUtils.extract_zip(zip_path, extract_dir)
puts "   Extracted #{extracted.length} files to: #{extract_dir}"
extracted.each { |f| puts "   - #{File.basename(f)}" }

# Example 6: ZIP with directories
puts "\n6. Creating ZIP with directory..."
zip_with_dir = File.join(temp_dir, 'with_dir.zip')
AllToolkit::ArchiveUtils.create_zip(zip_with_dir, temp_dir)
entries = AllToolkit::ArchiveUtils.list_zip(zip_with_dir)
puts "   Entries: #{entries.length}"

# Example 7: ZIP with exclude patterns
puts "\n7. Creating ZIP with exclusions..."
zip_filtered = File.join(temp_dir, 'filtered.zip')
AllToolkit::ArchiveUtils.create_zip(zip_filtered, temp_dir, exclude: ['*.json', '*.md'])
entries = AllToolkit::ArchiveUtils.list_zip(zip_filtered)
puts "   Entries (excluding .json and .md): #{entries.length}"

# ============================================================================
# TAR Archive Examples
# ============================================================================

puts "\n" + "-" * 60
puts "TAR Archive Operations"
puts "-" * 60

# Example 8: Create a TAR archive
puts "\n8. Creating TAR archive..."
tar_path = File.join(temp_dir, 'archive.tar')
AllToolkit::ArchiveUtils.create_tar(tar_path, [
  File.join(temp_dir, 'document.txt'),
  File.join(temp_dir, 'readme.md')
])
puts "   Created: #{tar_path}"
puts "   Size: #{File.size(tar_path)} bytes"

# Example 9: Create a compressed TAR (.tar.gz)
puts "\n9. Creating compressed TAR (.tar.gz)..."
tar_gz_path = File.join(temp_dir, 'archive.tar.gz')
AllToolkit::ArchiveUtils.create_tar(tar_gz_path, [
  File.join(temp_dir, 'document.txt'),
  File.join(temp_dir, 'data.json'),
  File.join(temp_dir, 'readme.md')
], gzip: true)
puts "   Created: #{tar_gz_path}"
puts "   Size: #{File.size(tar_gz_path)} bytes (compressed)"

# Example 10: List TAR contents
puts "\n10. Listing TAR contents..."
entries = AllToolkit::ArchiveUtils.list_tar(tar_path)
entries.each { |e| puts "   - #{e.name} (#{e.size} bytes)" }

# Example 11: Extract TAR
puts "\n11. Extracting TAR..."
tar_extract_dir = File.join(temp_dir, 'extracted_tar')
extracted = AllToolkit::ArchiveUtils.extract_tar(tar_path, tar_extract_dir)
puts "   Extracted #{extracted.length} files"

# Example 12: Extract compressed TAR
puts "\n12. Extracting compressed TAR..."
tar_gz_extract_dir = File.join(temp_dir, 'extracted_tar_gz')
extracted = AllToolkit::ArchiveUtils.extract_tar(tar_gz_path, tar_gz_extract_dir)
puts "   Extracted #{extracted.length} files"

# ============================================================================
# Utility Examples
# ============================================================================

puts "\n" + "-" * 60
puts "Utility Operations"
puts "-" * 60

# Example 13: Auto-extract (detects format)
puts "\n13. Auto-extract ZIP..."
auto_dir = File.join(temp_dir, 'auto_extracted')
extracted = AllToolkit::ArchiveUtils.extract(zip_path, auto_dir)
puts "   Auto-extracted #{extracted.length} files"

# Example 14: Auto-list (detects format)
puts "\n14. Auto-list TAR..."
entries = AllToolkit::ArchiveUtils.list(tar_path)
puts "   Found #{entries.length} entries"

# Example 15: Gzip single file
puts "\n15. Gzip single file..."
text_file = File.join(temp_dir, 'document.txt')
gzipped = File.join(temp_dir, 'document.txt.gz')
AllToolkit::ArchiveUtils.gzip_file(text_file, gzipped)
puts "   Gzipped: #{gzipped} (#{File.size(gzipped)} bytes)"

# Example 16: Gunzip file
puts "\n16. Gunzip file..."
ungzipped = File.join(temp_dir, 'document_ungzipped.txt')
AllToolkit::ArchiveUtils.gunzip_file(gzipped, ungzipped)
puts "   Ungzipped: #{ungzipped}"
puts "   Content: #{File.read(ungzipped)[0..50]}..."

# ============================================================================
# Cleanup
# ============================================================================

puts "\n" + "=" * 60
puts "Cleanup"
puts "=" * 60
FileUtils.rm_rf(temp_dir)
puts "Removed temporary directory: #{temp_dir}"

puts
puts "Example completed successfully!"
