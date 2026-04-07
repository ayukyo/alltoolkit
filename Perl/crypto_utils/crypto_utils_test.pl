#!/usr/bin/perl
# Crypto Utils Test Suite for Perl
# Comprehensive tests for AllToolkit::CryptoUtils

use strict;
use warnings;
use utf8;
use lib '.';
use mod;

# Test counters
my ($passed, $failed) = (0, 0);

sub test {
    my ($name, $condition) = @_;
    if ($condition) {
        print "[PASS] $name\n";
        $passed++;
    } else {
        print "[FAIL] $name\n";
        $failed++;
    }
}

sub test_equal {
    my ($name, $got, $expected) = @_;
    if (defined $got && defined $expected && $got eq $expected) {
        print "[PASS] $name\n";
        $passed++;
    } else {
        print "[FAIL] $name\n";
        print "       Expected: " . (defined $expected ? "'$expected'" : "undef") . "\n";
        print "       Got:      " . (defined $got ? "'$got'" : "undef") . "\n";
        $failed++;
    }
}

print "=" x 60 . "\n";
print "Crypto Utils Test Suite\n";
print "=" x 60 . "\n\n";

# Hash Function Tests
print "--- Hash Function Tests ---\n";

test_equal("md5_hash - hello world", 
    mod::md5_hash("hello world"),
    "5eb63bbbe01eeed093cb22bb8f5acdc3");

test_equal("md5_hash - empty string",
    mod::md5_hash(""),
    "d41d8cd98f00b204e9800998ecf8427e");

test("md5_hash - undef returns undef", !defined mod::md5_hash(undef));

test_equal("sha1_hash - hello world",
    mod::sha1_hash("hello world"),
    "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed");

test("sha1_hash returns 40 chars", length(mod::sha1_hash("test")) == 40);

test_equal("sha256_hash - hello world",
    mod::sha256_hash("hello world"),
    "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9");

test("sha256_hash returns 64 chars", length(mod::sha256_hash("test")) == 64);
test("sha512_hash returns 128 chars", length(mod::sha512_hash("test")) == 128);

my $unicode_hash = mod::sha256_hash("你好世界");
test("sha256_hash - unicode works", defined $unicode_hash && length($unicode_hash) == 64);

# HMAC Tests
print "\n--- HMAC Tests ---\n";

my $hmac = mod::hmac_sha256("message", "secret");
test("hmac_sha256 returns 64 chars", defined $hmac && length($hmac) == 64);
test("hmac_sha256 is consistent", mod::hmac_sha256("message", "secret") eq mod::hmac_sha256("message", "secret"));
test("verify_hmac_sha256 - valid", mod::verify_hmac_sha256("message", "secret", $hmac) == 1);
test("verify_hmac_sha256 - invalid", mod::verify_hmac_sha256("message", "secret", "invalid_hmac") == 0);
test("verify_hmac_sha256 - wrong key", mod::verify_hmac_sha256("message", "wrong_key", $hmac) == 0);

# Base64 Tests
print "\n--- Base64 Tests ---\n";

test_equal("base64_encode - Hello, World!", mod::base64_encode("Hello, World!"), "SGVsbG8sIFdvcmxkIQ==");

my $encoded = mod::base64_encode("test");
my $decoded = mod::base64_decode($encoded);
test_equal("base64 roundtrip", $decoded, "test");

test_equal("base64_encode - empty string", mod::base64_encode(""), "");
test("base64 unicode roundtrip", mod::base64_decode(mod::base64_encode("你好世界")) eq "你好世界");

my $url_encoded = mod::base64_urlsafe_encode("hello+world/test");
test("base64_urlsafe_encode replaces + and /", $url_encoded !~ /[+/]/);

my $url_decoded = mod::base64_urlsafe_decode($url_encoded);
test_equal("base64_urlsafe roundtrip", $url_decoded, "hello+world/test");
test("base64_urlsafe_encode without padding has no =", mod::base64_urlsafe_encode("test", 0) !~ /=/);

# Hex Encoding Tests
print "\n--- Hex Encoding Tests ---\n";

test_equal("hex_encode - hello", mod::hex_encode("hello"), "68656c6c6f");
test_equal("hex_decode - 68656c6c6f", mod::hex_decode("68656c6c6f"), "hello");

my $hex_round = mod::hex_decode(mod::hex_encode("test data 123"));
test_equal("hex roundtrip", $hex_round, "test data 123");

test("hex_decode - invalid hex returns undef", !defined mod::hex_decode("xyz"));
test("hex_decode - odd length returns undef", !defined mod::hex_decode("abc"));

# UUID Tests
print "\n--- UUID Tests ---\n";

my $uuid = mod::uuid_v4();
test("uuid_v4 returns 36 characters", defined $uuid && length($uuid) == 36);
test("uuid_v4 has correct format", $uuid =~ /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);
test("uuid_v4 generates unique values", mod::uuid_v4() ne mod::uuid_v4());

my $simple_uuid = mod::uuid_v4_simple();
test("uuid_v4_simple returns 32 characters", defined $simple_uuid && length($simple_uuid) == 32);
test("uuid_v4_simple has no hyphens", $simple_uuid !~ /-/);
test("is_valid_uuid - valid UUID", mod::is_valid_uuid($uuid) == 1);
test("is_valid_uuid - invalid UUID", mod::is_valid_uuid("not-a-uuid") == 0);

# Random String Tests
print "\n--- Random String Tests ---\n";

my $random = mod::random_string(16);
test("random_string returns correct length", defined $random && length($random) == 16);
test("random_string generates different values", mod::random_string(16) ne mod::random_string(16));

my $alphanumeric = mod::random_alphanumeric(20);
test("random_alphanumeric returns correct length", defined $alphanumeric && length($alphanumeric) == 20);
test("random_alphanumeric contains only alphanumeric", $alphanumeric =~ /^[a-zA-Z0-9]+$/);

my $numeric = mod::random_numeric(10);
test("random_numeric returns correct length", defined $numeric && length($numeric) == 10);
test("random_numeric contains only digits", $numeric =~ /^[0-9]+$/);

my $hex = mod::random_hex(16);
test("random_hex returns correct length", defined $hex && length($hex) == 16);
test("random_hex contains only hex chars", $hex =~ /^[0-9a-f]+$/);

my $hex_upper = mod::random_hex_upper(16);
test("random_hex_upper returns uppercase", $hex_upper =~ /^[0-9A-F]+$/);

my $password = mod::random_password(16);
test("random_password returns correct length", defined $password && length($password) == 16);
test("random_password contains uppercase", $password =~ /[A-Z]/);
test("random_password contains lowercase", $password =~ /[a-z]/);
test("random_password contains digit", $password =~ /[0-9]/);
test("random_password contains special", $password =~ /[!@#\$%\^&*()\-_=+\[\]{}|;:,.<>\?]/);

# XOR Encryption Tests
print "\n--- XOR Encryption Tests ---\n";

my $xor_encrypted = mod::xor_encrypt("secret message", "my_key");
test("xor_encrypt returns Base64", defined $xor_encrypted && $xor_encrypted =~ /^[A-Za-z0-9+\/=]+$/);

my $xor_decrypted = mod::xor_decrypt($xor_encrypted, "my_key");
test_equal("xor_decrypt roundtrip", $xor_decrypted, "secret message");

test("xor_decrypt with wrong key fails", mod::xor_decrypt($xor_encrypted, "wrong_key") ne "secret message");
test("xor_encrypt with empty key returns undef", !defined mod::xor_encrypt("test", ""));

# URL Encoding Tests
print "\n--- URL Encoding Tests ---\n";

test_equal("url_encode - space", mod::url_encode("hello world"), "hello%20world");
test_equal("url_encode - special chars", mod::url_encode("a+b=c"), "a%2Bb%3Dc");

my $url_decoded = mod::url_decode("hello%20world");
test_equal("url_decode - space", $url_decoded, "hello world");

my $url_round = mod::url_decode(mod::url_encode("test data 123!"));
test_equal("url roundtrip", $url_round, "test data 123!");

test("url_decode - unicode roundtrip", mod::url_decode(mod::url_encode("你好世界")) eq "你好世界");

# Validation Tests
print "\n--- Validation Tests ---\n";

test("is_valid_md5 - valid", mod::is_valid_md5("5eb63bbbe01eeed093cb22bb8f5acdc3") == 1);
test("is_valid_md5 - invalid length", mod::is_valid_md5("5eb63bbb") == 0);
test("is_valid_md5 - invalid chars", mod::is_valid_md5("xyz63bbbe01eeed093cb22bb8f5acdc3") == 0);

test("is_valid_sha256 - valid", mod::is_valid_sha256("b94d27b9934d3e