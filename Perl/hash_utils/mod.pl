#!/usr/bin/env perl

package AllToolkit::HashUtils;

use strict;
use warnings;
use utf8;
use Exporter 'import';
use Digest::MD5;
use Digest::SHA;
use MIME::Base64;
use Encode;

our @EXPORT_OK = qw(
    md5 md5_file md5_hex
    sha1 sha1_file sha1_hex
    sha256 sha256_file sha256_hex
    sha512 sha512_file sha512_hex
    hmac_sha256 hmac_sha1
    base64_encode base64_decode
    base64_url_encode base64_url_decode
    hex_encode hex_decode
    crc32 crc32_file
    hash_file hash_string
    is_valid_md5 is_valid_sha1 is_valid_sha256 is_valid_sha512
    random_bytes random_hex
    hash_equals
);

our %EXPORT_TAGS = (
    all => [@EXPORT_OK],
    md5 => [qw(md5 md5_file md5_hex)],
    sha => [qw(sha1 sha1_file sha1_hex sha256 sha256_file sha256_hex sha512 sha512_file sha512_hex)],
    hmac => [qw(hmac_sha256 hmac_sha1)],
    base64 => [qw(base64_encode base64_decode base64_url_encode base64_url_decode)],
    hex => [qw(hex_encode hex_decode)],
    crc => [qw(crc32 crc32_file)],
    util => [qw(hash_file hash_string is_valid_md5 is_valid_sha1 is_valid_sha256 is_valid_sha512 random_bytes random_hex hash_equals)],
);

=encoding utf8

=head1 NAME

AllToolkit::HashUtils - Comprehensive hash and digest utilities for Perl

=head1 SYNOPSIS

    use AllToolkit::HashUtils qw(:all);
    
    # MD5 hashing
    my $hash = md5("Hello, World!");
    my $hex = md5_hex("Hello, World!");
    my $file_hash = md5_file("/path/to/file");
    
    # SHA hashing
    my $sha256_hash = sha256("Hello, World!");
    my $sha256_hex = sha256_hex("Hello, World!");
    
    # HMAC
    my $hmac = hmac_sha256("message", "secret_key");
    
    # Base64 encoding
    my $encoded = base64_encode("Hello, World!");
    my $decoded = base64_decode($encoded);
    
    # URL-safe Base64
    my $url_safe = base64_url_encode("user+name/file");
    
    # CRC32
    my $crc = crc32("Hello, World!");

=head1 DESCRIPTION

This module provides comprehensive hash and digest utilities including MD5, SHA1,
SHA256, SHA512, HMAC, Base64 encoding/decoding, CRC32, and various helper functions.
All functions are zero-dependency (using only Perl core modules).

=cut

#==============================================================================
# MD5 Functions
#==============================================================================

=head1 MD5 FUNCTIONS

=head2 md5($data)

Calculate MD5 hash of string and return binary digest.

    my $binary_hash = md5("Hello, World!");

=cut

sub md5 {
    my ($data) = @_;
    return undef unless defined $data;
    return Digest::MD5::md5($data);
}

=head2 md5_hex($data)

Calculate MD5 hash of string and return hex string (32 characters).

    my $hex_hash = md5_hex("Hello, World!");
    # Returns: "65a8e27d8879283831b664bd8b7f0ad4"

=cut

sub md5_hex {
    my ($data) = @_;
    return undef unless defined $data;
    return Digest::MD5::md5_hex($data);
}

=head2 md5_file($filepath)

Calculate MD5 hash of file contents and return hex string.

    my $file_hash = md5_file("/path/to/file");

=cut

sub md5_file {
    my ($filepath) = @_;
    return undef unless defined $filepath && -f $filepath;
    
    my $md5 = Digest::MD5->new;
    open(my $fh, '<:raw', $filepath) or return undef;
    $md5->addfile($fh);
    close($fh);
    return $md5->hexdigest;
}

#==============================================================================
# SHA1 Functions
#==============================================================================

=head1 SHA1 FUNCTIONS

=head2 sha1($data)

Calculate SHA1 hash of string and return binary digest.

    my $binary_hash = sha1("Hello, World!");

=cut

sub sha1 {
    my ($data) = @_;
    return undef unless defined $data;
    return Digest::SHA::sha1($data);
}

=head2 sha1_hex($data)

Calculate SHA1 hash of string and return hex string (40 characters).

    my $hex_hash = sha1_hex("Hello, World!");

=cut

sub sha1_hex {
    my ($data) = @_;
    return undef unless defined $data;
    return Digest::SHA::sha1_hex($data);
}

=head2 sha1_file($filepath)

Calculate SHA1 hash of file contents and return hex string.

    my $file_hash = sha1_file("/path/to/file");

=cut

sub sha1_file {
    my ($filepath) = @_;
    return undef unless defined $filepath && -f $filepath;
    return Digest::SHA::sha1_file($filepath);
}

#==============================================================================
# SHA256 Functions
#==============================================================================

=head1 SHA256 FUNCTIONS

=head2 sha256($data)

Calculate SHA256 hash of string and return binary digest.

    my $binary_hash = sha256("Hello, World!");

=cut

sub sha256 {
    my ($data) = @_;
    return undef unless defined $data;
    return Digest::SHA::sha256($data);
}

=head2 sha256_hex($data)

Calculate SHA256 hash of string and return hex string (64 characters).

    my $hex_hash = sha256_hex("Hello, World!");
    # Returns: "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"

=cut

sub sha256_hex {
    my ($data) = @_;
    return undef unless defined $data;
    return Digest::SHA::sha256_hex($data);
}

=head2 sha256_file($filepath)

Calculate SHA256 hash of file contents and return hex string.

    my $file_hash = sha256_file("/path/to/file");

=cut

sub sha256_file {
    my ($filepath) = @_;
    return undef unless defined $filepath && -f $filepath;
    return Digest::SHA::sha256_file($filepath);
}

#==============================================================================
# SHA512 Functions
#==============================================================================

=head1 SHA512 FUNCTIONS

=head2 sha512($data)

Calculate SHA512 hash of string and return binary digest.

    my $binary_hash = sha512("Hello, World!");

=cut

sub sha512 {
    my ($data) = @_;
    return undef unless defined $data;
    return Digest::SHA::sha512($data);
}

=head2 sha512_hex($data)

Calculate SHA512 hash of string and return hex string (128 characters).

    my $hex_hash = sha512_hex("Hello, World!");

=cut

sub sha512_hex {
    my ($data) = @_;
    return undef unless defined $data;
    return Digest::SHA::sha512_hex($data);
}

=head2 sha512_file($filepath)

Calculate SHA512 hash of file contents and return hex string.

    my $file_hash = sha512_file("/path/to/file");

=cut

sub sha512_file {
    my ($filepath) = @_;
    return undef unless defined $filepath && -f $filepath;
    return Digest::SHA::sha512_file($filepath);
}

#==============================================================================
# HMAC Functions
#==============================================================================

=head1 HMAC FUNCTIONS

=head2 hmac_sha256($data, $key)

Calculate HMAC-SHA256 of data with given key.

    my $hmac = hmac_sha256("message", "secret_key");
    # Returns binary digest

=cut

sub hmac_sha256 {
    my ($data, $key) = @_;
    return undef unless defined $data && defined $key;
    return Digest::SHA::hmac_sha256($data, $key);
}

=head2 hmac_sha1($data, $key)

Calculate HMAC-SHA1 of data with given key.

    my $hmac = hmac_sha1("message", "secret_key");
    # Returns binary digest

=cut

sub hmac_sha1 {
    my ($data, $key) = @_;
    return undef unless defined $data && defined $key;
    return Digest::SHA::hmac_sha1($data, $key);
}

#==============================================================================
# Base64 Functions
#==============================================================================

=head1 BASE64 FUNCTIONS

=head2 base64_encode($data)

Encode data to Base64 string.

    my $encoded = base64_encode("Hello, World!");
    # Returns: "SGVsbG8sIFdvcmxkIQ=="

=cut

sub