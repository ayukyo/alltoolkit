#!/usr/bin/perl
# Crypto Utils Example for Perl
# Demonstrates usage of AllToolkit::CryptoUtils

use strict;
use warnings;
use utf8;
use lib '../crypto_utils';
use mod;

print "=" x 60 . "\n";
print "Crypto Utils Example\n";
print "=" x 60 . "\n\n";

# ============================================================================
# Example 1: Hash Functions
# ============================================================================
print "--- Example 1: Hash Functions ---\n";

my $message = "hello world";

print "Message: '$message'\n";
print "MD5:     " . mod::md5_hash($message) . "\n";
print "SHA1:    " . mod::sha1_hash($message) . "\n";
print "SHA256:  " . mod::sha256_hash($message) . "\n";
print "SHA512:  " . mod::sha512_hash($message) . "\n";

# Unicode hashing
my $chinese = "你好世界";
print "\nChinese text: '$chinese'\n";
print "SHA256: " . mod::sha256_hash($chinese) . "\n";

# ============================================================================
# Example 2: HMAC for API Authentication
# ============================================================================
print "\n--- Example 2: HMAC for API Authentication ---\n";

my $api_payload = '{"user_id":123,"action":"purchase"}';
my $api_secret = "my_secret_key_123";

my $signature = mod::hmac_sha256($api_payload, $api_secret);
print "Payload:   $api_payload\n";
print "Secret:    $api_secret\n";
print "Signature: $signature\n";

# Verify signature
my $is_valid = mod::verify_hmac_sha256($api_payload, $api_secret, $signature);
print "Verification: " . ($is_valid ? "VALID" : "INVALID") . "\n";

# Try with wrong secret
my $wrong_valid = mod::verify_hmac_sha256($api_payload, "wrong_secret", $signature);
print "Wrong secret: " . ($wrong_valid ? "VALID" : "INVALID") . "\n";

# ============================================================================
# Example 3: Base64 Encoding
# ============================================================================
print "\n--- Example 3: Base64 Encoding ---\n";

my $text = "Hello, World! 你好世界";
my $base64 = mod::base64_encode($text);
my $decoded = mod::base64_decode($base64);

print "Original: $text\n";
print "Base64:   $base64\n";
print "Decoded:  $decoded\n";
print "Match:    " . ($text eq $decoded ? "YES" : "NO") . "\n";

# URL-safe Base64
my $unsafe = "user+name/file@domain.com";
my $urlsafe = mod::base64_urlsafe_encode($unsafe);
my $urldecoded = mod::base64_urlsafe_decode($urlsafe);

print "\nURL-safe Base64:\n";
print "Original: $unsafe\n";
print "Encoded:  $urlsafe\n";
print "Decoded:  $urldecoded\n";

# ============================================================================
# Example 4: Hex Encoding
# ============================================================================
print "\n--- Example 4: Hex Encoding ---\n";

my $data = "Binary data: \x00\x01\x02\x03";
my $hex = mod::hex_encode($data);
my $hex_decoded = mod::hex_decode($hex);

print "Original: $data\n";
print "Hex:      $hex\n";
print "Decoded:  $hex_decoded\n";

# ============================================================================
# Example 5: UUID Generation
# ============================================================================
print "\n--- Example 5: UUID Generation ---\n";

print "Standard UUID v4:\n";
for my $i (1..3) {
    my $uuid = mod::uuid_v4();
    print "  $uuid (valid: " . (mod::is_valid_uuid($uuid) ? "YES" : "NO") . ")\n";
}

print "\nSimple UUID (no hyphens):\n";
for my $i (1..3) {
    print "  " . mod::uuid_v4_simple() . "\n";
}

print "\nUppercase UUID:\n";
print "  " . mod::uuid_v4_upper() . "\n";

# ============================================================================
# Example 6: Random String Generation
# ============================================================================
print "\n--- Example 6: Random String Generation ---\n";

print "Random alphanumeric (16 chars): " . mod::random_alphanumeric(16) . "\n";
print "Random numeric (6 digits):      " . mod::random_numeric(6) . "\n";
print "Random hex (8 chars):           " . mod::random_hex(8) . "\n";
print "Random hex upper (8 chars):     " . mod::random_hex_upper(8) . "\n";

print "\nSecure passwords:\n";
for my $i (1..3) {
    print "  " . mod::random_password(16) . "\n";
}

# ============================================================================
# Example 7: XOR Encryption (Simple)
# ============================================================================
print "\n--- Example 7: XOR Encryption ---\n";

my $secret_msg = "This is a secret message!";
my $xor_key = "my_encryption_key";

my $encrypted = mod::xor_encrypt($secret_msg, $xor_key);
my $decrypted = mod::xor_decrypt($encrypted, $xor_key);

print "Original:  $secret_msg\n";
print "Key:       $xor_key\n";
print "Encrypted: $encrypted\n";
print "Decrypted: $decrypted\n";

# ============================================================================
# Example 8: URL Encoding
# ============================================================================
print "\n--- Example 8: URL Encoding ---\n";

my $url_params = "q=hello world&special=a+b=c";
my $url_encoded = mod::url_encode($url_params);
my $url_decoded = mod::url_decode($url_encoded);

print "Original: $url_params\n";
print "Encoded:  $url_encoded\n";
print "Decoded:  $url_decoded\n";

# ============================================================================
# Example 9: Validation
# ============================================================================
print "\n--- Example 9: Validation ---\n";

my @hashes = (
    "5eb63bbbe01eeed093cb22bb8f5acdc3",  # Valid MD5
    "invalid",                            # Invalid
    "d41d8cd98f00b204e9800998ecf8427e",  # Valid MD5 (empty string)
);

print "MD5 validation:\n";
for my $hash (@hashes) {
    print "  '$hash' -> " . (mod::is_valid_md5($hash) ? "VALID" : "INVALID") . "\n";
}

my @uuids = (
    "550e8400-e29b-41d4-a716-446655440000",
    "not-a-uuid",
    "12345678-1234-1234-1234-123456789abc",
);

print "\nUUID validation:\n";
for my $uuid (@uuids) {
    print "  '$uuid' -> " . (mod::is_valid_uuid($uuid) ? "VALID" : "INVALID") . "\n";
}

# ============================================================================
# Example 10: File Hashing
# ============================================================================
print "\n--- Example 10: File Hashing ---\n";

# Create a temporary file
my $temp_file = "/tmp/crypto_test_$$.txt";
open(my $fh, '>:utf8', $temp_file) or die "Cannot create temp file: $!";
print $fh "Test content for hashing\n";
close($fh);

my $file_hash = mod::sha256_file($temp_file);
print "File: $temp_file\n";
print "SHA256: $file_hash\n";

# Clean up
unlink($temp_file);

print "\n" . "=" x 60 . "\n";
print "Examples completed!\n";
print "=" x 60 . "\n";
