#!/usr/bin/env perl

=head1 NAME

file_utils_example.pl - Example usage of AllToolkit::FileUtils

=head1 DESCRIPTION

Demonstrates common file operations using the FileUtils module.

=cut

use strict;
use warnings;
use utf8;

use FindBin;
use lib $FindBin::Bin . '/../file_utils';
use mod;

print "=== AllToolkit FileUtils Examples ===\n\n";

# Setup
my $example_dir = '/tmp/alltoolkit_example_' . $$;
mod::ensure_dir($example_dir);

# Example 1: Basic file operations
print "1. Basic File Operations\n";
my $file1 = mod::join_path($example_dir, 'example1.txt');
mod::write_file($file1, "Hello, World!\nThis is a test file.");
print "   Created: $file1\n";
print "   Size: " . mod::file_size($file1) . " bytes\n";
print "   Content:\n" . mod::read_file($file1) . "\n";

# Example 2: Reading file lines
print "\n2. Reading File Lines\n";
my $lines = mod::read_file_lines($file1);
print "   Number of lines: " . scalar(@$lines) . "\n";
for (my $i = 0; $i < @$lines; $i++) {
    print "   Line $i: $lines->[$i]\n";
}

# Example 3: Appending to file
print "\n3. Appending to File\n";
mod::append_file($file1, "\nAppended line.");
print "   New size: " . mod::file_size($file1) . " bytes\n";

# Example 4: File checks
print "\n4. File Checks\n";
print "   file_exists: " . (mod::file_exists($file1) ? 'yes' : 'no') . "\n";
print "   is_readable: " . (mod::is_readable($file1) ? 'yes' : 'no') . "\n";
print "   is_writable: " . (mod::is_writable($file1) ? 'yes' : 'no') . "\n";

# Example 5: Path manipulation
print "\n5. Path Manipulation\n";
my $path = '/home/user/documents/file.txt';
print "   Path: $path\n";
print "   Extension: " . mod::get_extension($path) . "\n";
print "   Basename: " . mod::get_basename($path) . "\n";
print "   Dirname: " . mod::get_dirname($path) . "\n";

# Example 6: Directory operations
print "\n6. Directory Operations\n";
my $subdir = mod::join_path($example_dir, 'subdir');
mod::ensure_dir($subdir);
print "   Created directory: $subdir\n";

# Create some files in subdir
mod::write_file(mod::join_path($subdir, 'file_a.txt'), 'A');
mod::write_file(mod::join_path($subdir, 'file_b.txt'), 'B');

# List files
my $files = mod::list_files($subdir);
print "   Files in subdir: " . join(', ', @$files) . "\n";

# Example 7: File copy and move
print "\n7. File Copy and Move\n";
my $src = mod::join_path($example_dir, 'source.txt');
my $dst_copy = mod::join_path($example_dir, 'copy.txt');
my $dst_move = mod::join_path($example_dir, 'moved.txt');

mod::write_file($src, "Source content");
mod::copy_file($src, $dst_copy);
print "   Copied $src to $dst_copy\n";

mod::move_file($dst_copy, $dst_move);
print "   Moved $dst_copy to $dst_move\n";

# Example 8: File size formatting
print "\n8. File Size Formatting\n";
print "   512 bytes: " . mod::format_size(512) . "\n";
print "   1536 bytes: " . mod::format_size(1536) . "\n";
print "   1572864 bytes: " . mod::format_size(1572864) . "\n";
print "   1073741824 bytes: " . mod::format_size(1073741824) . "\n";

# Example 9: Temporary files
print "\n9. Temporary Files\n";
my $temp_dir = mod::get_temp_dir();
print "   Temp directory: $temp_dir\n";

my $temp_file = mod::get_temp_file('example', '.txt');
print "   Temp file: $temp_file\n";

# Example 10: Recursive file finding
print "\n10. Recursive File Finding\n";
my $found = mod::find_files($example_dir, '\.txt$');
print "   Found " . scalar(@$found) . " .txt files:\n";
for my $f (@$found) {
    print "     - $f\n";
}

# Cleanup
print "\n=== Cleanup ===\n";
mod::remove_dir_recursive($example_dir);
print "Removed example directory: $example_dir\n";

print "\n=== Examples Complete ===\n";
