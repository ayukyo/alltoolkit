#!/usr/bin/env perl

=pod

=head1 NAME

AllToolkit::FileUtils - Zero-dependency file utilities for Perl

=head1 SYNOPSIS

    use lib 'Perl/file_utils';
    use mod;
    
    # Read file contents
    my $content = mod::read_file('/path/to/file.txt');
    
    # Write file contents
    mod::write_file('/path/to/file.txt', 'Hello, World!');

=head1 DESCRIPTION

A comprehensive file utility module providing common file operations
with zero external dependencies. Uses only Perl standard library.

=cut

package mod;

use strict;
use warnings;
use utf8;

our $VERSION = '1.0.0';

# Read entire file contents as string
sub read_file {
    my ($filepath, $encoding) = @_;
    $encoding ||= 'UTF-8';
    return undef unless defined $filepath;
    
    my $content = '';
    open(my $fh, "<:encoding($encoding)", $filepath) or return undef;
    { local $/; $content = <$fh>; }
    close($fh);
    return $content;
}

# Read file contents as array of lines
sub read_file_lines {
    my ($filepath, $encoding) = @_;
    $encoding ||= 'UTF-8';
    return undef unless defined $filepath;
    
    open(my $fh, "<:encoding($encoding)", $filepath) or return undef;
    my @lines = <$fh>;
    close($fh);
    chomp(@lines);
    return \@lines;
}

# Read file contents as binary data
sub read_file_binary {
    my ($filepath) = @_;
    return undef unless defined $filepath;
    
    my $content = '';
    open(my $fh, '<:raw', $filepath) or return undef;
    { local $/; $content = <$fh>; }
    close($fh);
    return $content;
}

# Write string content to file
sub write_file {
    my ($filepath, $content, $encoding) = @_;
    $encoding ||= 'UTF-8';
    return undef unless defined $filepath && defined $content;
    
    my $dir = get_dirname($filepath);
    ensure_dir($dir) if $dir && $dir ne '.' && $dir ne '/';
    
    open(my $fh, ">:encoding($encoding)", $filepath) or return undef;
    print $fh $content;
    close($fh);
    return 1;
}

# Write binary data to file
sub write_file_binary {
    my ($filepath, $data) = @_;
    return undef unless defined $filepath && defined $data;
    
    my $dir = get_dirname($filepath);
    ensure_dir($dir) if $dir && $dir ne '.' && $dir ne '/';
    
    open(my $fh, '>:raw', $filepath) or return undef;
    print $fh $data;
    close($fh);
    return 1;
}

# Append content to file
sub append_file {
    my ($filepath, $content, $encoding) = @_;
    $encoding ||= 'UTF-8';
    return undef unless defined $filepath && defined $content;
    
    my $dir = get_dirname($filepath);
    ensure_dir($dir) if $dir && $dir ne '.' && $dir ne '/';
    
    open(my $fh, ">>:encoding($encoding)", $filepath) or return undef;
    print $fh $content;
    close($fh);
    return 1;
}

# Check if file exists
sub file_exists {
    my ($filepath) = @_;
    return 0 unless defined $filepath;
    return -e $filepath ? 1 : 0;
}

# Check if directory exists
sub dir_exists {
    my ($dirpath) = @_;
    return 0 unless defined $dirpath;
    return (-e $dirpath && -d $dirpath) ? 1 : 0;
}

# Get file size in bytes
sub file_size {
    my ($filepath) = @_;
    return undef unless defined $filepath && -f $filepath;
    return -s $filepath;
}

# Get file modification time
sub file_mtime {
    my ($filepath) = @_;
    return undef unless defined $filepath && -e $filepath;
    return (stat($filepath))[9];
}

# Get file access time
sub file_atime {
    my ($filepath) = @_;
    return undef unless defined $filepath && -e $filepath;
    return (stat($filepath))[8];
}

# Get file creation/change time
sub file_ctime {
    my ($filepath) = @_;
    return undef unless defined $filepath && -e $filepath;
    return (stat($filepath))[10];
}

# Get file permissions (mode)
sub file_mode {
    my ($filepath) = @_;
    return undef unless defined $filepath && -e $filepath;
    return (stat($filepath))[2];
}

# Check if file is readable
sub is_readable {
    my ($filepath) = @_;
    return 0 unless defined $filepath;
    return -r $filepath ? 1 : 0;
}

# Check if file is writable
sub is_writable {
    my ($filepath) = @_;
    return 0 unless defined $filepath;
    return -w $filepath ? 1 : 0;
}

# Check if file is executable
sub is_executable {
    my ($filepath) = @_;
    return 0 unless defined $filepath;
    return -x $filepath ? 1 : 0;
}

# Check if path is a regular file
sub is_file {
    my ($filepath) = @_;
    return 0 unless defined $filepath;
    return -f $filepath ? 1 : 0;
}

# Check if path is a directory
sub is_dir {
    my ($filepath) = @_;
    return 0 unless defined $filepath;
    return -d $filepath ? 1 : 0;
}

# Check if path is a symbolic link
sub is_symlink {
    my ($filepath) = @_;
    return 0 unless defined $filepath;
    return -l $filepath ? 1 : 0;
}

# List files in directory (non-recursive)
sub list_files {
    my ($dirpath, $pattern) = @_;
    return undef unless defined $dirpath && -d $dirpath;
    
    opendir(my $dh, $dirpath) or return undef;
    my @entries = readdir($dh);
    closedir($dh);
    
    my @files = grep { $_ ne '.' && $_ ne '..' && -f join_path($dirpath, $_) } @entries;
    @files = grep { /$pattern/ } @files if $pattern;
    
    return wantarray ? @files : \@files;
}

# List subdirectories in directory
sub list_dirs {
    my ($dirpath) = @_;
    return undef unless defined $dirpath && -d $dirpath;
    
    opendir(my $dh, $dirpath) or return undef;
    my @entries = readdir($dh);
    closedir($dh);
    
    my @dirs = grep { $_ ne '.' && $_ ne '..' && -d join_path($dirpath, $_) } @entries;
    return wantarray ? @dirs : \@dirs;
}

# List all entries in directory
sub list_all {
    my ($dirpath) = @_;
    return undef unless defined $dirpath && -d $dirpath;
    
    opendir(my $dh, $dirpath) or return undef;
    my @entries = grep { $_ ne '.' && $_ ne '..' } readdir($dh);
    closedir($dh);
    
    return wantarray ? @entries : \@entries;
}

# Ensure directory exists (create if needed)
sub ensure_dir {
    my ($dirpath, $mode) = @_;
    $mode ||= 0755;
    return undef unless defined $dirpath;
    return 1 if -d $dirpath;
    
    my $parent = get_dirname($dirpath);
    if ($parent && $parent ne '.' && $parent ne '/' && !-d $parent) {
        ensure_dir($parent, $mode) or return undef;
    }
    
    mkdir($dirpath, $mode) or return undef;
    return 1;
}

# Remove a file
sub remove_file {
    my ($filepath) = @_;
    return 0 unless defined $filepath && -f $filepath;
    return unlink($filepath) ? 1 : 0;
}

# Remove an empty directory
sub remove_dir {
    my ($dirpath) = @_;
    return 0 unless defined $dirpath && -d $dirpath;
    return rmdir($dirpath) ? 1 : 0;
}

# Remove directory recursively
sub remove_dir_recursive {
    my ($dirpath) = @_;
    return 0 unless defined $dirpath && -d $dirpath;
    
    my $entries = list_all($dirpath);
    for my $entry (@$entries) {
        my $fullpath = join_path($dirpath, $entry);
        if (-d $fullpath) {
            remove_dir_recursive($fullpath) or return 0;
        } else {
            remove_file($fullpath) or return 0;
        }
    }
    return remove_dir($dirpath);
}

# Copy file
sub copy_file {
    my ($src, $dst) = @_;
    return 0 unless defined $src && defined $dst && -f $src;
    
    my $dir = get_dirname($dst);
    ensure_dir($dir) if $dir && $dir ne '.' && $dir ne '/';
    
    my $content = read_file_binary($src);
    return 0 unless defined $content;
    return write_file_binary($dst, $content);
}

# Move file
sub move_file {
    my ($src, $dst) = @_;
    return 0 unless defined $src && defined $dst && -e $src;
    
    my $dir = get_dirname($dst);
    ensure_dir($dir) if $dir && $dir ne '.' && $dir ne '/';
    
    return rename($src, $dst) ? 1 : 0;
}

# Get file extension
sub get_extension {
    my ($filepath) = @_;
    return '' unless defined $filepath;
    
    if ($filepath =~ /\.([^.]+)$/) {
        return lc($1);
    }
    return '';
}

# Get file basename (without extension)
sub get_basename {
    my ($filepath) = @_;
    return '' unless defined $filepath;
    
    my @parts = split(/[\\\/]/, $filepath);
    my $name = $parts[-1] || '';
    $name =~ s/\.[^.]+$//;
    return $name;
}

# Get directory name
sub get_dirname {
    my ($filepath) = @_;
    return '.' unless defined $filepath;
    
    if ($filepath =~ /^(.*)[\\\/]/) {
        return $1 || '/';
    }
    return '.';
}

# Join path components
sub join_path {
    my @parts = @_;
    return '' unless @parts;
    
    my $sep = '/';
    my $path = shift @parts;
    for my $part (@parts) {
        $path =~ s/[\\\/]+$//;
        $part =~ s/^[\\\/]+//;
        $path = $path . $sep . $part;
    }
    return $path;
}

# Normalize path
sub normalize_path {
    my ($filepath) = @_;
    return '' unless defined $filepath;
    
    $filepath =~ s/\\/\//g;
    $filepath =~ s/\/+/\//g;
    
    return $filepath;
}

# Get temporary directory
sub get_temp_dir {
    return $ENV{TMPDIR} || $ENV{TEMP} || $ENV{TMP} || '/tmp';
}

# Get temporary file path
sub get_temp_file {
    my ($prefix, $suffix) = @_;
    $prefix ||= 'tmp';
    $suffix ||= '';
    
    my $tempdir = get_temp_dir();
    my $filename = $prefix . '_' . time() . '_' . int(rand(10000)) . $suffix;
    return join_path($tempdir, $filename);
}

# Touch file (create or update timestamp)
sub touch {
    my ($filepath) = @_;
    return 0 unless defined $filepath;
    
    if (-e $filepath) {
        my $now = time();
        utime($now, $now, $filepath);
        return 1;
    } else {
        write_file($filepath, '');
        return 1;
    }
}

# Truncate file
sub truncate_file {
    my ($filepath, $size) = @_;
    $size ||= 0;
    return 0 unless defined $filepath;
    
    open(my $fh, '+<', $filepath) or return 0;
    truncate($fh, $size) or return 0;
    close($fh);
    return 1;
}

# Format file size
sub format_size {
    my ($size) = @_;
    return '0 B' unless defined $size && $size >= 0;
    
    my @units = ('B', 'KB', 'MB', 'GB', 'TB');
    my $unit = 0;
    
    while ($size >= 1024 && $unit < @units - 1) {
        $size /= 1024;
        $unit++;
    }
    
    return sprintf('%.2f %s', $size, $units[$unit]);
}

# Find files recursively
sub find_files {
    my ($dirpath, $pattern) = @_;
    return undef unless defined $dirpath && -d $dirpath;
    
    my @found;
    my $entries = list_all($dirpath);
    
    for my $entry (@$entries) {
        my $fullpath = join_path($dirpath, $entry);
        if (-d $fullpath) {
            my $subfound = find_files($fullpath, $pattern);
            push @found, @$subfound if $subfound;
        } elsif (-f $fullpath) {
            if (!$pattern || $entry =~ /$pattern/) {
                push @found, $fullpath;
            }
        }
    }
    
    return \@found;
}

1;