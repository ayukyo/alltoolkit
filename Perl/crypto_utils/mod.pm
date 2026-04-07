#!/usr/bin/perl
# Perl Crypto Utilities Module
# Zero-dependency cryptographic utility functions for Perl
# Supports: MD5, SHA1, SHA256, SHA512, HMAC, Base64, Hex encoding, UUID, Random generation

package AllToolkit::CryptoUtils;

use strict;
use warnings;
use utf8;
use Digest::MD5;
use Digest::SHA;
use Digest::HMAC_SHA1;
use Digest::HMAC_SHA256;
use MIME::Base64;
use Encode;

our $VERSION = '1.0.0';

# Character sets for random generation
our $LOWERCASE    = 'abcdefghijklmnopqrstuvwxyz';
our $UPPERCASE    = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
our $DIGITS       = '0123456789';
our $SPECIAL      = '!@#$%^&*()-_=+[]{}|;:,.<>?';
our $HEX_CHARS    = '0123456789abcdef';
our $HEX_UPPER    = '0123456789ABCDEF';
our $ALPHANUMERIC = $LOWERCASE . $UPPERCASE . $DIGITS;
our $ALL_CHARS    = $ALPHANUMERIC . $SPECIAL;

# ============================================================================
# Hash Functions
# ============================================================================

sub md5_hash {
    my ($input) = @_;
    return undef unless defined $input;
    my $bytes = encode_utf8($input);
    return Digest::MD5::md5_hex($bytes);
}

sub sha1_hash {
    my ($input) = @_;
    return undef unless defined $input;
    my $bytes = encode_utf8($input);
    return Digest::SHA::sha1_hex($bytes);
}

sub sha256_hash {
    my ($input) = @_;
    return undef unless defined $input;
    my $bytes = encode_utf8($input);
    return Digest::SHA::sha256_hex($bytes);
}

sub sha512_hash {
    my ($input) = @_;
    return undef unless defined $input;
    my $bytes = encode_utf8($input);
    return Digest::SHA::sha512_hex($bytes);
}

sub sha256_file {
    my ($filepath) = @_;
    return undef unless defined $filepath && -f $filepath;
    
    open(my $fh, '<:raw', $filepath) or return undef;
    my $sha = Digest::SHA->new(256);
    $sha->addfile($fh);
    close($fh);
    
    return $sha->hexdigest;
}

sub hash_file {
    my ($filepath, $algorithm) = @_;
    return undef unless defined $filepath && -f $filepath;
    $algorithm = lc($algorithm // 'sha256');
    
    my %alg_map = ('md5' => 1, 'sha1' => 1, 'sha256' => 1, 'sha512' => 1);
    return undef unless exists $alg_map{$algorithm};
    
    open(my $fh, '<:raw', $filepath) or return undef;
    
    if ($algorithm eq 'md5') {
        my $md5 = Digest::MD5->new;
        $md5->addfile($fh);
        close($fh);
        return $md5->hexdigest;
    } else {
        my $num = $algorithm eq 'sha1' ? 1 : ($algorithm eq 'sha256' ? 256 : 512);
        my $sha = Digest::SHA->new($num);
        $sha->addfile($fh);
        close($fh);
        return $sha->hexdigest;
    }
}

# ============================================================================
# HMAC Functions
# ============================================================================

sub hmac_sha1 {
    my ($message, $key) = @_;
    return undef unless defined $message && defined $key;
    my $msg_bytes = encode_utf8($message);
    my $key_bytes = encode_utf8($key);
    return Digest::HMAC_SHA1::hmac_sha1_hex($msg_bytes, $key_bytes);
}

sub hmac_sha256 {
    my ($message, $key) = @_;
    return undef unless defined $message && defined $key;
    my $msg_bytes = encode_utf8($message);
    my $key_bytes = encode_utf8($key);
    return Digest::HMAC_SHA256::hmac_sha256_hex($msg_bytes, $key_bytes);
}

sub verify_hmac_sha256 {
    my ($message, $key, $hmac) = @_;
    return 0 unless defined $message && defined $key && defined $hmac;
    my $computed = hmac_sha256($message, $key);
    return $computed eq $hmac ? 1 : 0;
}

# ============================================================================
# Base64 Encoding
# ============================================================================

sub base64_encode {
    my ($input) = @_;
    return undef unless defined $input;
    my $bytes = encode_utf8($input);
    return MIME::Base64::encode_base64($bytes, '');
}

sub base64_decode {
    my ($input) = @_;
    return undef unless defined $input;
    my $bytes = MIME::Base64::decode_base64($input);
    return decode_utf8($bytes);
}

sub base64_encode_bytes {
    my ($bytes) = @_;
    return undef unless defined $bytes;
    return MIME::Base64::encode_base64($bytes, '');
}

sub base64_decode_bytes {
    my ($input) = @_;
    return undef unless defined $input;
    return MIME::Base64::decode_base64($input);
}

sub base64_urlsafe_encode {
    my ($input, $padding) = @_;
    return undef unless defined $input;
    $padding = 1 unless defined $padding;
    
    my $bytes = encode_utf8($input);
    my $encoded = MIME::Base64::encode_base64($bytes, '');
    $encoded =~ tr/+/\-/;
    $encoded =~ tr/\//_/;
    $encoded =~ s/=+$// unless $padding;
    return $encoded;
}

sub base64_urlsafe_decode {
    my ($input) = @_;
    return undef unless defined $input;
    my $decoded = $input;
    $decoded =~ tr/\-/+/;
    $decoded =~ tr/_/\//;
    # Add padding if needed
    my $len = length($decoded);
    my $pad = (4 - ($len % 4)) % 4;
    $decoded .= '=' x $pad if $pad;
    my $bytes = MIME::Base64::decode_base64($decoded);
    return decode_utf8($bytes);
}

# ============================================================================
# Hex Encoding
# ============================================================================

sub hex_encode {
    my ($input) = @_;
    return undef unless defined $input;
    my $bytes = encode_utf8($input);
    return unpack('H*', $bytes);
}

sub hex_decode {
    my ($input) = @_;
    return undef unless defined $input;
    return undef if $input =~ /[^0-9a-fA-F]/;
    return undef if length($input) % 2 != 0;
    my $bytes = pack('H*', $input);
    return decode_utf8($bytes);
}

sub bytes_to_hex {
    my ($bytes) = @_;
    return undef unless defined $bytes;
    return unpack('H*', $bytes);
}

sub hex_to_bytes {
    my ($hex) = @_;
    return undef unless defined $hex;
    return undef if $hex =~ /[^0-9a-fA-F]/;
    return undef if length($hex) % 2 != 0;
    return pack('H*', $hex);
}

# ============================================================================
# UUID Generation
# ============================================================================

sub uuid_v4 {
    my @chars = split //, $HEX_CHARS;
    my @uuid;
    
    # Generate 16 random bytes
    for my $i (0..15) {
        $uuid[$i] = $chars[int(rand(16))];
    }
    
    # Set version (4) and variant bits
    $uuid[12] = '4';
    $uuid[16] = $chars[8 + int(rand(4))]; # 8, 9, a, or b
    
    return sprintf('%s%s%s%s%s%s%s%s-%s%s%s%s-%s%s%s%s-%s%s%s%s-%s%s%s%s%s%s%s%s%s%s%s%s',
        @uuid[0..31]);
}

sub uuid_v4_simple {
    my $uuid = uuid_v4();
    $uuid =~ s/-//g;
    return $uuid;
}

sub uuid_v4_upper {
    my $uuid = uuid_v4();
    return uc($uuid);
}

sub is_valid_uuid {
    my ($uuid) = @_;
    return 0 unless defined $uuid;
    return $uuid =~ /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/ ? 1 : 0;
}

# ============================================================================
# Random Generation
# ============================================================================

sub _random_bytes {
    my ($length) = @_;
    my $bytes = '';
    for my $i (0..$length-1) {
        $bytes .= chr(int(rand(256)));
    }
    return $bytes;
}

sub random_string {
    my ($length, $chars) = @_;
    return undef unless defined $length && $length > 0;
    $chars = $ALPHANUMERIC unless defined $chars;
    
    my @char_list = split //, $chars;
    my $result = '';
    for my $i (0..$length-1) {
        $result .= $char_list[int(rand(scalar @char_list))];
    }
    return $result;
}

sub random_alphanumeric {
    my ($length) = @_;
    return random_string($length, $ALPHANUMERIC);
}

sub random_numeric {
    my ($length) = @_;
    return random_string($length, $DIGITS);
}

sub random_hex {
    my ($length) = @_;
    return random_string($length, $HEX_CHARS);
}

sub random_hex_upper {
    my ($length) = @_;
    return random_string($length, $HEX_UPPER);
}

sub random_password {
    my ($length) = @_;
    return undef unless defined $length && $length >= 4;
    
    my @password;
    push @password, substr($UPPERCASE, int(rand(length($UPPERCASE))), 1);
    push @password, substr($LOWERCASE, int(rand(length($LOWERCASE))), 1);
    push @password, substr($DIGITS, int(rand(length($DIGITS))), 1);
    push @password, substr($SPECIAL, int(rand(length($SPECIAL))), 1);
    
    for my $i (4..$length-1) {
        my $char_set = $ALL_CHARS;
        push @password, substr($char_set, int(rand(length($char_set))), 1);
    }
    
    # Shuffle the password
    for my $i (0..$#password) {
        my $j = int(rand($#password + 1));
        ($password[$i], $password[$j]) = ($password[$j], $password[$i]);
    }
    
    return join('', @password);
}

# ============================================================================
# XOR Encryption
# ============================================================================

sub xor_encrypt {
    my ($input, $key) = @_;
    return undef unless defined $input && defined $key;
    return undef if length($key) == 0;
    
    my @input_bytes = unpack('C*', encode_utf8($input));
    my @key_bytes = unpack('C*', encode_utf8($key));
    my @result;
    
    for my $i (0..$#input_bytes) {
        push @result, $input_bytes[$i] ^ $key_bytes[$i % scalar(@key_bytes)];
    }
    
    my $encrypted = pack('C*', @result);
    return base64_encode_bytes($encrypted);
}

sub xor_decrypt {
    my ($encrypted, $key) = @_;
    return undef unless defined $encrypted && defined $key;
    return undef if length($key) == 0;
    
    my $encrypted_bytes = base64_decode_bytes($encrypted);
    return undef unless defined $encrypted_bytes;
    
    my @input_bytes = unpack('C*', $encrypted_bytes);
    my @key_bytes = unpack('C*', encode_utf8($key));
    my @result;
    
    for my $i (0..$#input_bytes) {
        push @result, $input_bytes[$i] ^ $key_bytes[$i % scalar(@key_bytes)];
    }
    
    my $decrypted = pack('C*', @result);
    return decode_utf8($decrypted);
}

# ============================================================================
# URL Encoding
# ============================================================================

sub url_encode {
    my ($input) = @_;
    return undef unless defined $input;
    my $bytes = encode_utf8($input);
    $bytes =~ s/([^A-Za-z0-9_.~\-])/sprintf('%%%02X', ord($1))/eg;
    return $bytes;
}

sub url_decode {
    my ($input) = @_;
    return undef unless defined $input;
    $input =~ s/%([0-9A-Fa-f]{2})/chr(hex($1))/eg;
    return decode_utf8($input);
}

# ============================================================================
# Validation
# ============================================================================

sub is_valid_md5 {
    my ($hash) = @_;
    return 0 unless defined $hash;
    return length($hash) == 32 && $hash =~ /^[0-9a-fA-F]+$/ ? 1 : 0;
}

sub is_valid_sha1 {
    my ($hash) = @_;
    return 0 unless defined $hash;
    return length($hash) == 40 && $hash =~ /^[0-9a-fA-F]+$/ ? 1 : 0;
}

sub is_valid_sha256 {
    my ($hash) = @_;
    return 0 unless defined $hash;
    return length($hash) == 64 && $hash =~ /^[0-9a-fA-F]+$/ ? 1 : 0;
}

sub is_valid_sha512 {
    my ($hash) = @_;
    return 0 unless defined $hash;
    return length($hash) == 128 && $hash =~ /^[0-9a-fA-F]+$/ ? 1 : 0;
}

sub is_valid_base64 {
    my ($input) = @_;
    return 0 unless defined $input;
    return $input =~ /^[A-Za-z0-9+\/]+={0,2}$/ ? 1 : 0;
}

sub is_valid_hex {
    my ($input) = @_;
    return 0 unless defined $input;
    return $input =~ /^[0-9a-fA-F]+$/ && length($input) % 2 == 0 ? 1 : 0;
}

# ============================================================================
# Module Export
# ============================================================================

package mod;

# Hash functions
*md5_hash = \&AllToolkit::CryptoUtils::md5_hash;
*sha1_hash = \&AllToolkit::CryptoUtils::sha1_hash;
*sha256_hash = \&AllToolkit::CryptoUtils::sha256_hash;
*sha512_hash = \&AllToolkit::CryptoUtils::sha512_hash;
*sha256_file = \&AllToolkit::CryptoUtils::sha256_file;
*hash_file = \&AllToolkit::CryptoUtils::hash_file;

# HMAC functions
*hmac_sha1 = \&AllToolkit::CryptoUtils::hmac_sha1;
*hmac_sha256 = \&AllToolkit::CryptoUtils::hmac_sha256;
*verify_hmac_sha256 = \&AllToolkit::CryptoUtils::verify_hmac_sha256;

# Base64 functions
*base64_encode = \&AllToolkit::CryptoUtils::base64_encode;
*base64_decode = \&AllToolkit::CryptoUtils::base64_decode;
*base64_encode_bytes = \&AllToolkit::CryptoUtils::base64_encode_bytes;
*base64_decode_bytes = \&AllToolkit::CryptoUtils::base64_decode_bytes;
*base64_urlsafe_encode = \&AllToolkit::CryptoUtils::base64_urlsafe_encode;
*base64_urlsafe_decode = \&AllToolkit::CryptoUtils::base64_urlsafe_decode;

# Hex functions
*hex_encode = \&AllToolkit::CryptoUtils::hex_encode;
*hex_decode = \&AllToolkit::CryptoUtils::hex_decode;
*bytes_to_hex = \&AllToolkit::CryptoUtils::bytes_to_hex;
*hex_to_bytes = \&AllToolkit::CryptoUtils::hex_to_bytes;

# UUID functions
*uuid_v4 = \&AllToolkit::CryptoUtils::uuid_v4;
*uuid_v4_simple = \&AllToolkit::CryptoUtils::uuid_v4_simple;
*uuid_v4_upper = \&AllToolkit::CryptoUtils::uuid_v4_upper;
*is_valid_uuid = \&AllToolkit::CryptoUtils::is_valid_uuid;

# Random functions
*random_string = \&AllToolkit::CryptoUtils::random_string;
*random_alphanumeric = \&AllToolkit::CryptoUtils::random_alphanumeric;
*random_numeric = \&AllToolkit::CryptoUtils::random_numeric;
*random_hex = \&AllToolkit::CryptoUtils::random_hex;
*random_hex_upper = \&AllToolkit::CryptoUtils::random_hex_upper;
*random_password = \&AllToolkit::CryptoUtils::random_password;

# XOR functions
*xor_encrypt = \&AllToolkit::CryptoUtils::xor_encrypt;
*xor_decrypt = \&AllToolkit::CryptoUtils::xor_decrypt;

# URL functions
*url_encode = \&AllToolkit::CryptoUtils::url_encode;
*url_decode = \&AllToolkit::CryptoUtils::url_decode;

# Validation functions
*is_valid_md5 = \&AllToolkit::CryptoUtils::is_valid_md5;
*is_valid_sha1 = \&AllToolkit::CryptoUtils::is_valid_sha1;
*is_valid_sha256 = \&AllToolkit::CryptoUtils::is_valid_sha256;
*is_valid_sha512 = \&AllToolkit::CryptoUtils::is_valid_sha512;
*is_valid_base64 = \&AllToolkit::CryptoUtils::is_valid_base64;
*is_valid_hex = \&AllToolkit::CryptoUtils::is_valid_hex;

1;

__END__

=head1 NAME

AllToolkit::CryptoUtils - Comprehensive cryptographic utility module for Perl

=head1 SYNOPSIS

    use lib 'Perl/crypto_utils';
    use mod;
    
    # Hash functions
    my $md5 = mod::md5_hash("hello world");
    my $sha256 = mod::sha256_hash("hello world");
    
    # HMAC
    my $hmac = mod::hmac_sha256("message", "secret_key");
    
    # Base64 encoding
    my $encoded = mod::base64_encode("Hello, World!");
    my $decoded = mod::base64_decode($encoded);
    
    # UUID generation
    my $uuid = mod::uuid_v4();
    
    # Random string generation
    my $password = mod::random_password(16);

=head1 DESCRIPTION

This module provides a comprehensive set of cryptographic utility functions
including hash algorithms, HMAC, Base64 encoding, UUID generation, and secure
random string generation. All functions use only Perl core modules.

=head1 FUNCTIONS

=head2 Hash Functions

=over 4

=item B<md5_hash($input)>

Calculate MD5 hash of input string. Returns 32-character hexadecimal string.

=item B<sha1_hash($input)>

Calculate SHA1 hash of input string. Returns 40-character hexadecimal string.

=item B<sha256_hash($input)>

Calculate SHA256 hash of input string. Returns 64-character hexadecimal string.

=item B<sha512_hash($input)>

Calculate SHA512 hash of input string. Returns 128-character hexadecimal string.

=item B<sha256_file($filepath)>

Calculate SHA256 hash of file contents.

=item B<hash_file($filepath, $algorithm)>

Calculate hash of file with specified algorithm ('md5', 'sha1', 'sha256', 'sha512').

=back

=head2 HMAC Functions

=over 4

=item B<hmac_sha1($message, $key)>

Calculate HMAC-SHA1 of message with secret key.

=item B<hmac_sha256($message, $key)>

Calculate HMAC-SHA256 of message with secret key.

=item B<verify_hmac_sha256($message, $key, $hmac)>

Verify HMAC-SHA256 signature. Returns 1 if valid, 0 if invalid.

=back

=head2 Base64 Functions

=over 4

=item B<base64_encode($input)>

Encode string to Base64.

=item B<base64_decode($input)>

Decode Base64 string.

=item B<base64_urlsafe_encode($input, $padding)>

Encode string to URL-safe Base64 (RFC 4648).

=item B<base64_urlsafe_decode($input)>

Decode URL-safe Base64 string.

=back

=head2 Hex Functions

=over 4

=item B<hex_encode($input)>

Encode string to hexadecimal.

=item B<hex_decode($input)>

Decode hexadecimal string.

=back

=head2 UUID Functions

=over 4

=item B<uuid_v4()>

Generate UUID version 4 (random).

=item B<uuid_v4_simple()>

Generate UUID without hyphens.

=item B<is_valid_uuid($uuid)>

Validate UUID format.

=back

=head2 Random Functions

=over 4

=item B<random_string($length, $chars)>

Generate random string from character set.

=item B<random_alphanumeric($length)>

Generate random alphanumeric string.

=item B<random_password($length)>

Generate secure password with mixed characters.

=back

=head2 Encryption Functions

=over 4

=item B<xor_encrypt($input, $key)>

Simple XOR encryption (returns Base64).

=item B<xor_decrypt($encrypted, $key)>

Decrypt XOR encrypted data.

=back

=head2 Validation Functions

=over 4

=item B<is_valid_md5($hash)>

Validate MD5 hash format.

=item B<is_valid_sha256($hash)>

Validate SHA256 hash format.

=item B<is_valid_base64($input)>

Validate Base64 format.

=item B<is_valid_hex($input)>

Validate hexadecimal format.

=back

=head1 AUTHOR

AllToolkit Contributors

=head1 LICENSE

MIT License

=cut
