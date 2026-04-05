#!/usr/bin/env ruby
# frozen_string_literal: true

# Archive Utilities Test Suite
# Comprehensive tests for ZIP and TAR archive operations

require_relative 'mod'
require 'fileutils'
require 'tempfile'

class ArchiveUtilsTest
  def initialize
    @test_dir = Dir.mktmpdir('archive_test')
    @test_count = 0
    @passed = 0
    @failed = 0
  end

  def run_all
    puts "=" * 60
    puts "ArchiveUtils Test Suite"
    puts "=" * 60
    puts

    # ZIP Tests
    test_zip_creation
    test_zip_extraction
    test_zip_listing
    test_zip_stats
    test_zip_validation
    test_zip_with_directories
    test_zip_exclude_patterns

    # TAR Tests
    test_tar_creation
    test_tar_extraction
    test_tar_gzipped
    test_tar_listing

    # Utility Tests
    test_auto_extract
    test_gzip_operations

    puts
    puts "=" * 60
    puts "Results: #{@passed} passed, #{@failed} failed, #{@test_count} total"
    puts "=" * 60

    cleanup
    @failed == 0
  end

  private

  def test(name)
    @test_count += 1
    print "Test #{@test_count}: #{name}... "
    begin
      yield
      puts "PASSED"
      @passed += 1
      true
    rescue => e
      puts "FAILED: #{e.message}"
      @failed += 1
      false
    end
  end

  def cleanup
    FileUtils.rm_rf(@test_dir) if File.exist?(@test_dir)
  end


  def create_test_file(name, content = "Test content #{rand(1000)}")
    path = File.join(@test_dir, name)
    FileUtils.mkdir_p(File.dirname(path))
    File.write(path, content)
    path
  end


  # ZIP Tests
  def test_zip_creation
    test("ZIP creation") do
      file1 = create_test_file('file1.txt', 'Hello World')
      file2 = create_test_file('file2.txt', 'Ruby Archive Utils')
      zip_path = File.join(@test_dir, 'test.zip')

      AllToolkit::ArchiveUtils.create_zip(zip_path, [file1, file2])

      raise "ZIP not created" unless File.exist?(zip_path)
      raise "ZIP is empty" unless File.size(zip_path) > 0
    end
  end

  def test_zip_extraction
    test("ZIP extraction") do
      file1 = create_test_file('orig1.txt', 'Test Data 1')
      file2 = create_test_file('orig2.txt', 'Test Data 2')
      zip_path = File.join(@test_dir, 'extract_test.zip')
      extract_dir = File.join(@test_dir, 'extracted')

      AllToolkit::ArchiveUtils.create_zip(zip_path, [file1, file2])
      extracted = AllToolkit::ArchiveUtils.extract_zip(zip_path, extract_dir)

      raise "No files extracted" if extracted.empty?
      raise "Wrong file count" unless extracted.length == 2
    end
  end


  def test_zip_listing
    test("ZIP listing") do
      file1 = create_test_file('list1.txt', 'Content 1')
      file2 = create_test_file('list2.txt', 'Content 2')
      zip_path = File.join(@test_dir, 'list_test.zip')

      AllToolkit::ArchiveUtils.create_zip(zip_path, [file1, file2])
      entries = AllToolkit::ArchiveUtils.list_zip(zip_path)

      raise "No entries found" if entries.empty?
      raise "Wrong entry count" unless entries.length == 2
      raise "Entry missing name" unless entries.all? { |e| e.name.include?('.txt') }
    end
  end

  def test_zip_stats
    test("ZIP stats") do
      file1 = create_test_file('stat1.txt', 'A' * 100)
      file2 = create_test_file('stat2.txt', 'B' * 200)
      zip_path = File.join(@test_dir, 'stats_test.zip')

      AllToolkit::ArchiveUtils.create_zip(zip_path, [file1, file2])
      stats = AllToolkit::ArchiveUtils.zip_stats(zip_path)

      raise "Wrong entry count" unless stats.entry_count == 2
      raise "Wrong total size" unless stats.total_size == 300
    end
  end

  def test_zip_validation
    test("ZIP validation") do
      file = create_test_file('valid.txt', 'Valid content')
      zip_path = File.join(@test_dir, 'valid_test.zip')

      AllToolkit::ArchiveUtils.create_zip(zip_path, [file])
      valid = AllToolkit::ArchiveUtils.valid_zip?(zip_path)

      raise "Should be valid" unless valid

      # Test invalid file
      invalid_path = File.join(@test_dir, 'invalid.zip')
      File.write(invalid_path, 'Not a zip file')
      invalid = AllToolkit::ArchiveUtils.valid_zip?(invalid_path)
      raise "Should be invalid" if invalid
    end
  end

  def test_zip_with_directories
    test("ZIP with directories") do
      dir = File.join(@test_dir, 'source_dir')
      FileUtils.mkdir_p(dir)
      File.write(File.join(dir, 'nested.txt'), 'Nested content')
      zip_path = File.join(@test_dir, 'dir_test.zip')

      AllToolkit::ArchiveUtils.create_zip(zip_path, [dir])
      entries = AllToolkit::ArchiveUtils.list_zip(zip_path)

      raise "No entries" if entries.empty?
      raise "No nested file" unless entries.any? { |e| e.name.include?('nested.txt') }
    end
  end


  def test_zip_exclude_patterns
    test("ZIP exclude patterns") do
      file1 = create_test_file('keep.txt', 'Keep me')
      file2 = create_test_file('skip.log', 'Skip me')
      zip_path = File.join(@test_dir, 'exclude_test.zip')

      AllToolkit::ArchiveUtils.create_zip(zip_path, [file1, file2], exclude: ['*.log'])
      entries = AllToolkit::ArchiveUtils.list_zip(zip_path)

      raise "Should have 1 entry" unless entries.length == 1
      raise "Wrong file kept" unless entries.first.name.include?('keep.txt')
    end
  end

  # TAR Tests
  def test_tar_creation
    test("TAR creation") do
      file1 = create_test_file('tar1.txt', 'TAR Content 1')
      file2 = create_test_file('tar2.txt', 'TAR Content 2')
      tar_path = File.join(@test_dir, 'test.tar')

      AllToolkit::ArchiveUtils.create_tar(tar_path, [file1, file2])

      raise "TAR not created" unless File.exist?(tar_path)
      raise "TAR is empty" unless File.size(tar_path) > 0
    end
  end

  def test_tar_extraction
    test("TAR extraction") do
      file1 = create_test_file('tar_orig1.txt', 'TAR Data 1')
      file2 = create_test_file('tar_orig2.txt', 'TAR Data 2')
      tar_path = File.join(@test_dir, 'tar_extract_test.tar')
      extract_dir = File.join(@test_dir, 'tar_extracted')

      AllToolkit::ArchiveUtils.create_tar(tar_path, [file1, file2])
      extracted = AllToolkit::ArchiveUtils.extract_tar(tar_path, extract_dir)

      raise "No files extracted" if extracted.empty?
    end
  end

  def test_tar_gzipped
    test("TAR.GZ creation and extraction") do
      file = create_test_file('gzipped.txt', 'Gzipped content here')
      tar_gz_path = File.join(@test_dir, 'test.tar.gz')
      extract_dir = File.join(@test_dir, 'gz_extracted')

      AllToolkit::ArchiveUtils.create_tar(tar_gz_path, [file], gzip: true)
      extracted = AllToolkit::ArchiveUtils.extract_tar(tar_gz_path, extract_dir)

      raise "Not extracted" if extracted.empty?
    end
  end

  def test_tar_listing
    test("TAR listing") do
      file1 = create_test_file('tarlist1.txt', 'Content')
      file2 = create_test_file('tarlist2.txt', 'More content')
      tar_path = File.join(@test_dir, 'tar_list_test.tar')

      AllToolkit::ArchiveUtils.create_tar(tar_path, [file1, file2])
      entries = AllToolkit::ArchiveUtils.list_tar(tar_path)

      raise "No entries" if entries.empty?
      raise "Wrong count" unless entries.length >= 2
    end
  end

  # Utility Tests
  def test_auto_extract
    test("Auto extract ZIP") do
      file = create_test_file('auto.txt', 'Auto extract test')
      zip_path = File.join(@test_dir, 'auto_test.zip')
      extract_dir = File.join(@test_dir, 'auto_extracted')

      AllToolkit::ArchiveUtils.create_zip(zip_path, [file])
      extracted = AllToolkit::ArchiveUtils.extract(zip_path, extract_dir)

      raise "Auto extract failed" if extracted.empty?
    end
  end


  def test_gzip_operations
    test("Gzip file operations") do
      file = create_test_file('to_gzip.txt', 'Gzip me')
      gz_path = File.join(@test_dir, 'test.gz')
      
      AllToolkit::ArchiveUtils.gzip_file(file, gz_path)
      raise "Not gzipped" unless File.exist?(gz_path)
      
      unzipped = File.join(@test_dir, 'ungzipped.txt')
      AllToolkit::ArchiveUtils.gunzip_file(gz_path, unzipped)
      raise "Not unzipped" unless File.exist?(unzipped)
    end
  end
end

# Run tests if executed directly
if __FILE__ == $0
  test = ArchiveUtilsTest.new
  exit(test.run_all ? 0 : 1)
end