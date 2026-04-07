{*******************************************************************************
 * AllToolkit - Delphi Crypto Utilities Test Suite
 * 
 * Comprehensive test suite for crypto_utils module
 *******************************************************************************}

program crypto_utils_test;

{$IFDEF FPC}
  {$MODE OBJFPC}
  {$H+}
{$ENDIF}

uses
  SysUtils, Classes, mod;

var
  Passed: Integer = 0;
  Failed: Integer = 0;

procedure Test(Name: string; Condition: Boolean);
begin
  if Condition then
  begin
    Writeln('[PASS] ', Name);
    Inc(Passed);
  end
  else
  begin
    Writeln('[FAIL] ', Name);
    Inc(Failed);
  end;
end;

procedure TestHashFunctions;
begin
  Writeln('--- Hash Functions ---');
  
  // MD5 tests
  Test('Md5Hash returns 32 chars', Length(Md5Hash('test')) = 32);
  Test('Md5Hash is consistent', Md5Hash('hello') = Md5Hash('hello'));
  Test('Md5Hash different for different input', Md5Hash('hello') <> Md5Hash('world'));
  Test('Md5Hash empty string', Length(Md5Hash('')) = 32);
  
  // SHA1 tests
  Test('Sha1Hash returns 40 chars', Length(Sha1Hash('test')) = 40);
  Test('Sha1Hash is consistent', Sha1Hash('hello') = Sha1Hash('hello'));
  
  // SHA256 tests
  Test('Sha256Hash returns 64 chars', Length(Sha256Hash('test')) = 64);
  Test('Sha256Hash is consistent', Sha256Hash('hello') = Sha256Hash('hello'));
  
  // SHA512 tests
  Test('Sha512Hash returns 128 chars', Length(Sha512Hash('test')) = 128);
  Test('Sha512Hash is consistent', Sha512Hash('hello') = Sha512Hash('hello'));
  
  // Bytes hash tests
  Test('Md5HashBytes works', Length(Md5HashBytes(StringToBytes('test'))) = 32);
  Test('Sha1HashBytes works', Length(Sha1HashBytes(StringToBytes('test'))) = 40);
end;

procedure TestBase64Functions;
begin
  Writeln('--- Base64 Functions ---');
  
  // Encode/Decode tests
  Test('Base64Encode encodes string', Base64Encode('hello') <> '');
  Test('Base64Decode decodes correctly', Base64Decode(Base64Encode('hello')) = 'hello');
  Test('Base64 round-trip', Base64Decode(Base64Encode('Hello, World!')) = 'Hello, World!');
  Test('Base64Encode empty string', Base64Encode('') = '');
  Test('Base64Decode empty string', Base64Decode('') = '');
  
  // URL-safe Base64
  Test('Base64UrlEncode works', Base64UrlEncode('hello world') <> '');
  Test('Base64UrlDecode decodes correctly', Base64UrlDecode(Base64UrlEncode('hello')) = 'hello');
  Test('Base64UrlEncode without padding', Pos('=', Base64UrlEncode('hello', False)) = 0);
  
  // Validation
  Test('IsValidBase64 accepts valid', IsValidBase64('SGVsbG8='));
  Test('IsValidBase64 rejects invalid', not IsValidBase64('Invalid!'));
  Test('IsValidBase64 rejects empty', IsValidBase64(''));
end;

procedure TestUUIDFunctions;
begin
  Writeln('--- UUID Functions ---');
  
  // Generate tests
  Test('GenerateUuid returns 36 chars', Length(GenerateUuid) = 36);
  Test('GenerateUuidSimple returns 32 chars', Length(GenerateUuidSimple) = 32);
  Test('GenerateUuidUpper returns uppercase', GenerateUuidUpper = UpperCase(GenerateUuidUpper));
  
  // Validation
  Test('IsValidUuid accepts standard UUID', IsValidUuid('550e8400-e29b-41d4-a716-446655440000'));
  Test('IsValidUuid accepts simple UUID', IsValidUuid('550e8400e29b41d4a716446655440000'));
  Test('IsValidUuid rejects invalid', not IsValidUuid('not-a-uuid'));
  Test('IsValidUuid rejects wrong length', not IsValidUuid('550e8400'));
end;

procedure TestRandomFunctions;
begin
  Writeln('--- Random Functions ---');
  
  // Random string tests
  Test('RandomString returns correct length', Length(RandomString(10)) = 10);
  Test('RandomString with custom chars', Length(RandomString(5, 'ABC')) = 5);
  Test('RandomString empty for length 0', RandomString(0) = '');
  
  // Alphanumeric
  Test('RandomAlphanumeric returns correct length', Length(RandomAlphanumeric(16)) = 16);
  
  // Numeric
  Test('RandomNumeric returns correct length', Length(RandomNumeric(6)) = 6);
  
  // Hex
  Test('RandomHex returns correct length', Length(RandomHex(8)) = 8);
  Test('RandomHex uppercase works', Length(RandomHex(8, True)) = 8);
  
  // Password
  Test('RandomPassword returns correct length', Length(RandomPassword(12)) = 12);
  Test('RandomPassword minimum length 4', Length(RandomPassword(2)) = 4);
end;

procedure TestXorEncryption;
begin
  Writeln('--- XOR Encryption ---');
  
  // Encryption/Decryption tests
  Test('XorEncrypt returns non-empty', XorEncrypt('hello', 'key') <> '');
  Test('XorDecrypt restores original', XorDecrypt(XorEncrypt('hello', 'key'), 'key') = 'hello');
  Test('Xor round-trip', XorDecrypt(XorEncrypt('Secret message!', 'mykey'), 'mykey') = 'Secret message!');
  Test('XorEncrypt empty input', XorEncrypt('', 'key') = '');
  Test('XorEncrypt empty key', XorEncrypt('hello', '') = '');
end;

procedure TestValidationFunctions;
begin
  Writeln('--- Validation Functions ---');
  
  // MD5 validation
  Test('IsValidMd5 accepts valid', IsValidMd5('5d41402abc4b2a76b9719d911017c592'));
  Test('IsValidMd5 rejects wrong length', not IsValidMd5('5d41402abc4b2a76b9719d911017c59'));
  Test('IsValidMd5 rejects invalid chars', not IsValidMd5('5d41402abc4b2a76b9719d911017c59g'));
  
  // SHA1 validation
  Test('IsValidSha1 accepts valid', IsValidSha1('aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d'));
  Test('IsValidSha1 rejects wrong length', not IsValidSha1('aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434'));
  
  // SHA256 validation
  Test('IsValidSha256 accepts valid', IsValidSha256('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'));
  Test('IsValidSha256 rejects wrong length', not IsValidSha256('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b982'));
  
  // SHA512 validation
  Test('IsValidSha512 accepts valid', IsValidSha512(StringOfChar('a', 128)));
  Test('IsValidSha512 rejects wrong length', not IsValidSha512(StringOfChar('a', 64)));
end;

procedure TestUtilityFunctions;
begin
  Writeln('--- Utility Functions ---');
  
  // Bytes/Hex conversion
  Test('BytesToHex converts correctly', BytesToHex(StringToBytes('AB')) = '4142');
  Test('HexToBytes converts correctly', BytesToString(HexToBytes('4142')) = 'AB');
  Test('BytesToHex round-trip', BytesToString(HexToBytes(BytesToHex(StringToBytes('test')))) = 'test');
  Test('BytesToHex empty', BytesToHex(nil) = '');
  
  // String/Bytes conversion
  Test('StringToBytes converts correctly', Length(StringToBytes('hello')) = 5);
  Test('BytesToString converts correctly', BytesToString(StringToBytes('hello')) = 'hello');
  Test('StringToBytes round-trip', BytesToString(StringToBytes('test')) = 'test');
end;

procedure TestHMACFunctions;
begin
  Writeln('--- HMAC Functions ---');
  
  Test('HmacSha256 returns consistent value', HmacSha256('message', 'key') = HmacSha256('message', 'key'));
  Test('HmacSha256 different for different messages', HmacSha256('msg1', 'key') <> HmacSha256('msg2', 'key'));
  Test('HmacSha256 different for different secrets', HmacSha256('msg', 'key1') <> HmacSha256('msg', 'key2'));
  Test('VerifyHmacSha256 verifies correctly', VerifyHmacSha256('message', 'key', HmacSha256('message', 'key')));
  Test('VerifyHmacSha256 rejects invalid', not VerifyHmacSha256('message', 'key', 'invalid'));
end;

procedure TestCharacterSets;
begin
  Writeln('--- Character Sets ---');
  
  Test('LowerCase has 26 chars', Length(TCharSet.LowerCase) = 26);
  Test('UpperCase has 26 chars', Length(TCharSet.UpperCase) = 26);
  Test('Digits has 10 chars', Length(TCharSet.Digits) = 10);
  Test('Hex has 16 chars', Length(TCharSet.Hex) = 16);
  Test('Alphanumeric has 62 chars', Length(TCharSet.Alphanumeric) = 62);
end;

begin
  Writeln('==============================================');
  Writeln('AllToolkit - Delphi Crypto Utilities Test Suite');
  Writeln('==============================================');
  Writeln;
  
  Randomize;
  
