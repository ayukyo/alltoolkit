#!/usr/bin/env ruby
# frozen_string_literal: true

# Archive Utilities - A comprehensive file archiving and compression utility module for Ruby
# Provides ZIP and TAR archive creation, extraction, and management with zero dependencies.

require 'zip'
require 'rubygems/package'
require 'zlib'
require 'fileutils'
require 'pathname'


module AllToolkit
  # Archive entry information
  class ArchiveEntry
    attr_reader :name, :size, :compressed_size, :mtime, :is_directory

    def initialize(name:, size: 0, compressed_size: 0, mtime: nil, is_directory: false)
      @name = name
      @size = size
      @compressed_size = compressed_size
      @mtime = mtime
      @is_directory = is_directory
    end

    def compression_ratio
      return 0.0 if @size == 0
      (1.0 - (@compressed_size.to_f / @size)) * 100
    end

    def to_s
      "#{@name} (#{@size} bytes)"
    end
  end

  # Archive statistics
  class ArchiveStats
    attr_reader :entry_count, :total_size, :total_compressed_size, :compression_ratio

    def initialize(entries)
      @entry_count = entries.length
      @total_size = entries.sum(&:size)
      @total_compressed_size = entries.sum(&:compressed_size)
      @compression_ratio = @total_size > 0 ? (1.0 - (@total_compressed_size.to_f / @total_size)) * 100 : 0.0
    end

    def to_s
      "Entries: #{@entry_count}, Total: #{@total_size} bytes, Compressed: #{@total_compressed_size} bytes, Ratio: #{@compression_ratio.round(2)}%"
    end
  end

  # Main Archive Utilities module
  module ArchiveUtils
    class ArchiveError < StandardError; end
    class InvalidArchiveError < ArchiveError; end
    class ExtractionError < ArchiveError; end

    DEFAULT_COMPRESSION = Zlib::BEST_COMPRESSION
    BUFFER_SIZE = 8192

    # ============================================================================
    # ZIP Archive Operations
    # ============================================================================

    # Create a ZIP archive from files or directories
    def self.create_zip(zipfile_path, sources, options = {})
      compression = options[:compression] || DEFAULT_COMPRESSION
      base_dir = options[:base_dir]
      exclude_patterns = options[:exclude] || []
      preserve_paths = options.fetch(:preserve_paths, true)
      sources = [sources] if sources.is_a?(String)

      Zip::File.open(zipfile_path, Zip::File::CREATE) do |zipfile|
        sources.each do |source|
          add_to_zip(zipfile, source, base_dir, exclude_patterns, preserve_paths, compression)
        end
      end
      zipfile_path
    rescue => e
      raise ArchiveError, "Failed to create ZIP archive: #{e.message}"
    end

    # Extract a ZIP archive to a directory
    def self.extract_zip(zipfile_path, destination = '.', options = {})
      password = options[:password]
      only_patterns = options[:only]
      overwrite = options.fetch(:overwrite, true)
      extracted = []


      Zip::File.open(zipfile_path) do |zipfile|
        zipfile.each do |entry|
          next if entry.directory?
          if only_patterns && !matches_any_pattern?(entry.name, only_patterns)
            next
          end
          dest_path = File.join(destination, entry.name)
          next if !overwrite && File.exist?(dest_path)
          FileUtils.mkdir_p(File.dirname(dest_path))
          entry.extract(dest_path) { |_| password || '' }
          extracted << dest_path
        end
      end
      extracted
    rescue => e
      raise ExtractionError, "Failed to extract ZIP archive: #{e.message}"
    end

    # List contents of a ZIP archive
    def self.list_zip(zipfile_path)
      entries = []
      Zip::File.open(zipfile_path) do |zipfile|
        zipfile.each do |entry|
          entries << ArchiveEntry.new(
            name: entry.name,
            size: entry.size,
            compressed_size: entry.compressed_size,
            mtime: entry.time,
            is_directory: entry.directory?
          )
        end
      end
      entries
    rescue Zip::Error => e
      raise InvalidArchiveError, "Invalid ZIP archive: #{e.message}"
    end


    # Get statistics for a ZIP archive
    def self.zip_stats(zipfile_path)
      entries = list_zip(zipfile_path)
      ArchiveStats.new(entries)
    end

    # Test a ZIP archive for integrity
    def self.valid_zip?(zipfile_path)
      Zip::File.open(zipfile_path) do |zipfile|
        zipfile.each { |entry| return false unless entry.verify_crc }
      end
      true
    rescue
      false
    end


    # Add files to an existing ZIP archive
    def self.add_to_zip_archive(zipfile_path, sources, options = {})
      compression = options[:compression] || DEFAULT_COMPRESSION
      base_dir = options[:base_dir]
      exclude_patterns = options[:exclude] || []
      preserve_paths = options.fetch(:preserve_paths, true)
      sources = [sources] if sources.is_a?(String)

      Zip::File.open(zipfile_path, Zip::File::CREATE) do |zipfile|
        sources.each { |source| add_to_zip(zipfile, source, base_dir, exclude_patterns, preserve_paths, compression) }
      end
      zipfile_path
    rescue => e
      raise ArchiveError, "Failed to add to ZIP archive: #{e.message}"
    end

    # ============================================================================
    # TAR Archive Operations
    # ============================================================================

    # Create a TAR archive
    def self.create_tar(tarfile_path, sources, options = {})
      base_dir = options[:base_dir]
      exclude_patterns = options[:exclude] || []
      preserve_paths = options.fetch(:preserve_paths, true)
      gzip = options.fetch(:gzip, tarfile_path.end_with?('.gz', '.tgz'))
      sources = [sources] if sources.is_a?(String)

      tar_io = StringIO.new
      Gem::Package::TarWriter.new(tar_io) do |tar|
        sources.each { |source| add_to_tar(tar, source, base_dir, exclude_patterns, preserve_paths) }
      end

      File.open(tarfile_path, 'wb') do |file|
        if gzip
          file.write(Zlib::Deflate.deflate(tar_io.string, DEFAULT_COMPRESSION))
        else
          file.write(tar_io.string)
        end
      end
      tarfile_path
    rescue => e
      raise ArchiveError, "Failed to create TAR archive: #{e.message}"
    end

    # Extract a TAR archive
    def self.extract_tar(tarfile_path, destination = '.', options = {})
      only_patterns = options[:only]
      overwrite = options.fetch(:overwrite, true)
      gzip = tarfile_path.end_with?('.gz', '.tgz')
      extracted = []

      tar_data = File.binread(tarfile_path)
      tar_data = Zlib::Inflate.inflate(tar_data) if gzip

      Gem::Package::TarReader.new(StringIO.new(tar_data)) do |tar|
        tar.each do |entry|
          next unless entry.file?
          if only_patterns && !matches_any_pattern?(entry.full_name, only_patterns)
            next
          end
          dest_path = File.join(destination, entry.full_name)
          next if !overwrite && File.exist?(dest_path)
          FileUtils.mkdir_p(File.dirname(dest_path))
          File.binwrite(dest_path, entry.read)
          extracted << dest_path
        end
      end
      extracted
    rescue => e
      raise ExtractionError, "Failed to extract TAR archive: #{e.message}"
    end

    # List contents of a TAR archive
    def self.list_tar(tarfile_path)
      entries = []
      gzip = tarfile_path.end_with?('.gz', '.tgz')
      tar_data = File.binread(tarfile_path)
      tar_data = Zlib::Inflate.inflate(tar_data) if gzip

      Gem::Package::TarReader.new(StringIO.new(tar_data)) do |tar|
        tar.each do |entry|
          entries << ArchiveEntry.new(
            name: entry.full_name,
            size: entry.header.size,
            compressed_size: entry.header.size,
            mtime: entry.header.mtime,
            is_directory: entry.directory?
          )
        end
      end
      entries
    rescue => e
      raise InvalidArchiveError, "Invalid TAR archive: #{e.message}"
    end

    # Get statistics for a TAR archive
    def self.tar_stats(tarfile_path)
      entries = list_tar(tarfile_path)
      ArchiveStats.new(entries)
    end

    # ============================================================================
    # Utility Methods
    # ============================================================================

    # Auto-detect archive type and extract
    def self.extract(archive_path, destination = '.', options = {})
      case File.extname(archive_path).downcase
      when '.zip'
        extract_zip(archive_path, destination, options)
      when '.tar', '.gz', '.tgz'
        extract_tar(archive_path, destination, options)
      else
        raise ArchiveError, "Unknown archive format: #{archive_path}"
      end
    end

    # Auto-detect archive type and list
    def self.list(archive_path)
      case File.extname(archive_path).downcase
      when '.zip'
        list_zip(archive_path)
      when '.tar', '.gz', '.tgz'
        list_tar(archive_path)
      else
        raise ArchiveError, "Unknown archive format: #{archive_path}"
      end
    end

    # Get statistics for any archive type
    def self.stats(archive_path)
      case File.extname(archive_path).downcase
      when '.zip'
        zip_stats(archive_path)
      when '.tar', '.gz', '.tgz'
        tar_stats(archive_path)
      else
        raise ArchiveError, "Unknown archive format: #{archive_path}"
      end
    end

    # Compress a single file with gzip
    def self.gzip_file(source_path, dest_path = nil)
      dest_path ||= "#{source_path}.gz"
      Zlib::GzipWriter.open(dest_path) do |gz|
        gz.write(File.binread(source_path))
      end
      dest_path
    end

    # Decompress a gzip file
    def self.gunzip_file(source_path, dest_path = nil)
      dest_path ||= source_path.chomp('.gz')
      Zlib::GzipReader.open(source_path) do |gz|
        File.binwrite(dest_path, gz.read)
      end
      dest_path
    end

    private

    def self.add_to_zip(zipfile, source, base_dir, exclude_patterns, preserve_paths, compression)
      return if excluded?(source, exclude_patterns)

      if File.directory?(source)
        Dir.glob(File.join(source, '**', '*')).each do |file|
          next if File.directory?(file)
          next if excluded?(file, exclude_patterns)
          add_file_to_zip(zipfile, file, base_dir || source, preserve_paths, compression)
        end
      else
        add_file_to_zip(zipfile, source, base_dir, preserve_paths, compression)
      end
    end

    def self.add_file_to_zip(zipfile, file_path, base_dir, preserve_paths, compression)
      entry_name = if preserve_paths && base_dir
                   Pathname.new(file_path).relative_path_from(Pathname.new(base_dir)).to_s
                 else
                   File.basename(file_path)
                 end
      zipfile.add(entry_name, file_path) do |entry|
        entry.compression_level = compression
      end
    end

    def self.add_to_tar(tar, source, base_dir, exclude_patterns, preserve_paths)
      return if excluded?(source, exclude_patterns)

      if File.directory?(source)
        Dir.glob(File.join(source, '**', '*')).each do |file|
          next if excluded?(file, exclude_patterns)
          add_file_to_tar(tar, file, base_dir || source, preserve_paths)
        end
      else
        add_file_to_tar(tar, source, base_dir, preserve_paths)
      end
    end

    def self.add_file_to_tar(tar, file_path, base_dir, preserve_paths)
      entry_name = if preserve_paths && base_dir
               Pathname.new(file_path).relative_path_from(Pathname.new(base_dir)).to_s
             else
               File.basename(file_path)
             end
      tar.add_file(entry_name, File.stat(file_path)) do |io|
        io.write(File.binread(file_path))
      end
    end

    def self.excluded?(path, patterns)
      patterns.any? { |pattern| File.fnmatch(pattern, path, File::FNM_PATHNAME | File::FNM_DOTMATCH) }
    end

    def self.matches_any_pattern?(name, patterns)
      patterns.any? { |pattern| File.fnmatch(pattern, name, File::FNM_PATHNAME) }
    end
  end
end

# Convenience method
def ArchiveUtils
  AllToolkit::ArchiveUtils
end
