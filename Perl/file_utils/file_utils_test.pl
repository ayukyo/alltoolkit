#!/usr/bin/env perl

use strict;
use warnings;
use utf8;

use FindBin;
use lib $FindBin::Bin;
use mod;

# Test counter
my $tests_run = 0;
my $tests_passed = 0;

# Helper function for tests
sub test {
    my ($name, $condition) = @_;
    $tests_run++;
    if ($condition) {
        $tests_passed++;
        print "[PASS] $name\n";
    } else {
        print "[FAIL] $name\n";
    }
}

# Setup test directory
my $test_dir = '/tmp/alltoolkit_perl_test_' . $$;
mod::ensure_dir($test_dir);

print "=== Perl FileUtils Test Suite ===\n\n";

# Test file operations
my $test_file = mod::join_path($test_dir, 'test.txt');
my $content = "Hello, World!\nLine 2\nLine 3";

# Test write_file
mod::write_file($test_file, $content);
test("write_file creates file", mod::file_exists($test_file));

# Test read_file
my $read_content = mod::read_file($test_file);
test("read_file returns correct content", $read_content eq $content);

# Test read_file_lines
my $lines = mod::read_file_lines($test_file);
test("read_file_lines returns array ref", ref($lines) eq 'ARRAY');
test("read_file_lines has correct line count", scalar(@$lines) == 3);
test("read_file_lines first line correct", $lines->[0] eq 'Hello, World!');

# Test file_size
test("file_size returns correct size", mod::file_size($test_file) == length($content));

# Test append_file
mod::append_file($test_file, "\nLine 4");
my $appended_content = mod::read_file($test_file);
test("append_file adds content", index($appended_content, "Line 4") >= 0);

# Test file_exists and dir_exists
test("file_exists returns true for existing file", mod::file_exists($test_file));
test("file_exists returns false for non-existent file", !mod::file_exists('/nonexistent/file.txt'));
test("dir_exists returns true for existing dir", mod::dir_exists($test_dir));
test("dir_exists returns false for non-existent dir", !mod::dir_exists('/nonexistent/dir'));

# Test is_file and is_dir
test("is_file returns true for file", mod::is_file($test_file));
test("is_file returns false for dir", !mod::is_file($test_dir));
test("is_dir returns true for dir", mod::is_dir($test_dir));
test("is_dir returns false for file", !mod::is_dir($test_file));

# Test is_readable and is_writable
test("is_readable returns true for readable file", mod::is_readable($test_file));
test("is_writable returns true for writable file", mod::is_writable($test_file));

# Test path functions
test("get_extension returns correct extension", mod::get_extension('file.txt') eq 'txt');
test("get_extension returns empty for no extension", mod::get_extension('file') eq '');
test("get_basename returns correct name", mod::get_basename('/path/to/file.txt') eq 'file');
test("get_dirname returns correct dir", mod::get_dirname('/path/to/file.txt') eq '/path/to');
test("join_path joins correctly", mod::join_path('a', 'b', 'c') eq 'a/b/c');
test("normalize_path converts backslashes", mod::normalize_path('a\\b\\c') eq 'a/b/c');

# Test directory operations
my $subdir = mod::join_path($test_dir, 'subdir');
mod::ensure_dir($subdir);
test("ensure_dir creates directory", mod::dir_exists($subdir));

# Test list_files
my $file_in_subdir = mod::join_path($subdir, 'test2.txt');
mod::write_file($file_in_subdir, 'test');
my $files = mod::list_files($test_dir);
test("list_files returns files", ref($files) eq 'ARRAY');
test("list_files includes test.txt", scalar(grep { $_ eq 'test.txt' } @$files) == 1);

# Test list_dirs
my $dirs = mod::list_dirs($test_dir);
test("list_dirs returns directories", ref($dirs) eq 'ARRAY');
test("list_dirs includes subdir", scalar(grep { $_ eq 'subdir' } @$dirs) == 1);

# Test list_all
my $all = mod::list_all($test_dir);
test("list_all returns all entries", ref($all) eq 'ARRAY');

# Test copy_file
my $copy_dest = mod::join_path($test_dir, 'copy.txt');
mod::copy_file($test_file, $copy_dest);
test("copy_file creates copy", mod::file_exists($copy_dest));
test("copy_file copies content correctly", mod::read_file($copy_dest) eq mod::read_file($test_file));

# Test move_file
my $move_dest = mod::join_path($test_dir, 'moved.txt');
mod::move_file($copy_dest, $move_dest);
test("move_file moves file", mod::file_exists($move_dest));
test("move_file removes source", !mod::file_exists($copy_dest));

# Test format_size
test("format_size formats bytes", mod::format_size(512) eq '512.00 B');
test("format_size formats KB", mod::format_size(1536) eq '1.50 KB');
test("format_size formats MB", mod::format_size(1572864) eq '1.50 MB');

# Test touch
my $touch_file = mod::join_path($test_dir, 'touch.txt');
mod::touch($touch_file);
test("touch creates empty file", mod::file_exists($touch_file));
test("touch creates file with zero size", mod::file_size($touch_file) == 0);

# Test find_files
my $deep_dir = mod::join_path($subdir, 'deep');
mod::ensure_dir($deep_dir);
my $deep_file = mod::join_path($deep_dir, 'found.txt');
mod::write_file($deep_file, 'deep content');
my $found = mod::find_files($test_dir, '\.txt$');
test("find_files finds files recursively", ref($found) eq 'ARRAY');
test("find_files finds multiple files", scalar(@$found) >= 3);

# Test remove operations
mod::remove_file($move_dest);
test("remove_file deletes file", !mod::file_exists($move_dest));

# Cleanup
mod::remove_dir_recursive($test_dir);
test("remove_dir_recursive removes directory", !mod::dir_exists($test_dir));

# Test temp functions
test("get_temp_dir returns valid path", defined(mod::get_temp_dir()));
my $temp_file = mod::get_temp_file('test', '.txt');
test("get_temp_file returns path with prefix", index($temp_file, 'test_') >= 0);
test("get_temp_file returns path with suffix", index($temp_file, '.txt') >= 0);

# Summary
print "\n=== Test Summary ===\n";
print "Tests run: $tests_run\n";
print "Tests passed: $tests_passed\n";
print "Tests failed: " . ($tests_run - $tests_passed) . "\n";

exit($tests_passed == $tests_run ? 0 : 1);
