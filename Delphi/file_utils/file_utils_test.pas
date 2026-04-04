{*******************************************************************************
 * AllToolkit - Delphi File Utilities Test Suite
 *
 * Comprehensive test suite for FileUtils module.
 * Tests cover normal scenarios, edge cases, and error handling.
 *
 * Version: 1.0.0
 * Author: AllToolkit Contributors
 * License: MIT
 *******************************************************************************}

program FileUtilsTest;

uses
  SysUtils, Classes, FileUtils;

var
  TestCount: Integer = 0;
  PassCount: Integer = 0;
  FailCount: Integer = 0;
  TempDir: string;

procedure TestStart(const TestName: string);
begin
  Inc(TestCount);
  Write(Format('[%2d] %-50s ', [TestCount, TestName]));
end;

procedure TestPass;
begin
  Inc(PassCount);
  Writeln('[PASS]');
end;

procedure TestFail(const Msg: string);
begin
  Inc(FailCount);
  Writeln('[FAIL] ', Msg);
end;

procedure TestAssert(Condition: Boolean; const Msg: string);
begin
  if Condition then
    TestPass
  else
    TestFail(Msg);
end;

{==============================================================================}
{ TPathUtils Tests }
{==============================================================================}

procedure Test_PathUtils_Combine;
var
  Result: string;
begin
  TestStart('TPathUtils.Combine - normal paths');
  Result := TPathUtils.Combine('C:\Users', 'Documents');
  TestAssert(Result = 'C:\Users\Documents', 'Expected C:\Users\Documents, got ' + Result);

  TestStart('TPathUtils.Combine - with trailing slash');
  Result := TPathUtils.Combine('C:\Users\', 'Documents');
  TestAssert(Result = 'C:\Users\Documents', 'Expected C:\Users\Documents, got ' + Result);

  TestStart('TPathUtils.Combine - with leading slash');
  Result := TPathUtils.Combine('C:\Users', '\Documents');
  TestAssert(Result = 'C:\Users\Documents', 'Expected C:\Users\Documents, got ' + Result);

  TestStart('TPathUtils.Combine - empty first path');
  Result := TPathUtils.Combine('', 'Documents');
  TestAssert(Result = 'Documents', 'Expected Documents, got ' + Result);

  TestStart('TPathUtils.Combine - empty second path');
  Result := TPathUtils.Combine('C:\Users', '');
  TestAssert(Result = 'C:\Users', 'Expected C:\Users, got ' + Result);

  TestStart('TPathUtils.Combine - both paths empty');
  Result := TPathUtils.Combine('', '');
  TestAssert(Result = '', 'Expected empty string, got ' + Result);
end;

procedure Test_PathUtils_GetFileName;
begin
  TestStart('TPathUtils.GetFileName - with extension');
  TestAssert(TPathUtils.GetFileName('C:\Users\test.txt') = 'test.txt', 'Wrong filename');

  TestStart('TPathUtils.GetFileName - no extension');
  TestAssert(TPathUtils.GetFileName('C:\Users\test') = 'test', 'Wrong filename');

  TestStart('TPathUtils.GetFileName - relative path');
  TestAssert(TPathUtils.GetFileName('test.txt') = 'test.txt', 'Wrong filename');

  TestStart('TPathUtils.GetFileName - empty path');
  TestAssert(TPathUtils.GetFileName('') = '', 'Expected empty string');
end;

procedure Test_PathUtils_GetFileNameWithoutExtension;
begin
  TestStart('TPathUtils.GetFileNameWithoutExtension - with extension');
  TestAssert(TPathUtils.GetFileNameWithoutExtension('C:\Users\test.txt') = 'test', 'Wrong result');

  TestStart('TPathUtils.GetFileNameWithoutExtension - no extension');
  TestAssert(TPathUtils.GetFileNameWithoutExtension('C:\Users\test') = 'test', 'Wrong result');

  TestStart('TPathUtils.GetFileNameWithoutExtension - multiple dots');
  TestAssert(TPathUtils.GetFileNameWithoutExtension('C:\Users\test.backup.txt') = 'test.backup', 'Wrong result');
end;

procedure Test_PathUtils_GetExtension;
begin
  TestStart('TPathUtils.GetExtension - normal extension');
  TestAssert(TPathUtils.GetExtension('C:\Users\test.txt') = 'txt', 'Wrong extension');

  TestStart('TPathUtils.GetExtension - uppercase extension');
  TestAssert(TPathUtils.GetExtension('C:\Users\test.TXT') = 'txt', 'Should be lowercase');

  TestStart('TPathUtils.GetExtension - no extension');
  TestAssert(TPathUtils.GetExtension('C:\Users\test') = '', 'Expected empty string');

  TestStart('TPathUtils.GetExtension - multiple dots');
  TestAssert(TPathUtils.GetExtension('C:\Users\test.backup.txt') = 'txt', 'Wrong extension');
end;

procedure Test_PathUtils_GetDirectory;
begin
  TestStart('TPathUtils.GetDirectory - absolute path');
  TestAssert(TPathUtils.GetDirectory('C:\Users\test.txt') = 'C:\Users', 'Wrong directory');

  TestStart('TPathUtils.GetDirectory - relative path');
  TestAssert(TPathUtils.GetDirectory('Users\test.txt') = 'Users', 'Wrong directory');

  TestStart('TPathUtils.GetDirectory - just filename');
  TestAssert(TPathUtils.GetDirectory('test.txt') = '', 'Expected empty string');
end;

procedure Test_PathUtils_HasExtension;
begin
  TestStart('TPathUtils.HasExtension - has extension');
  TestAssert(TPathUtils.HasExtension('test.txt'), 'Should have extension');

  TestStart('TPathUtils.HasExtension - no extension');
  TestAssert(not TPathUtils.HasExtension('test'), 'Should not have extension');

  TestStart('TPathUtils.HasExtension - empty string');
  TestAssert(not TPathUtils.HasExtension(''), 'Empty string should not have extension');
end;

procedure Test_PathUtils_IsPathRooted;
begin
  TestStart('TPathUtils.IsPathRooted - absolute Windows path');
  TestAssert(TPathUtils.IsPathRooted('C:\Users'), 'Should be rooted');

  TestStart('TPathUtils.IsPathRooted - UNC path');
  TestAssert(TPathUtils.IsPathRooted('\\server\share'), 'Should be rooted');

  TestStart('TPathUtils.IsPathRooted - relative path');
  TestAssert(not TPathUtils.IsPathRooted('Users\test'), 'Should not be rooted');

  TestStart('TPathUtils.IsPathRooted - Unix path');
  TestAssert(TPathUtils.IsPathRooted('/usr/bin'), 'Should be rooted');

  TestStart('TPathUtils.IsPathRooted - empty string');
  TestAssert(not TPathUtils.IsPathRooted(''), 'Empty string should not be rooted');
end;

procedure Test_PathUtils_IsValidFileName;
begin
  TestStart('TPathUtils.IsValidFileName - valid name');
  TestAssert(TPathUtils.IsValidFileName('test.txt'), 'Should be valid');

  TestStart('TPathUtils.IsValidFileName - with invalid char');
  TestAssert(not TPathUtils.IsValidFileName('test<file>.txt'), 'Should be invalid');

  TestStart('TPathUtils.IsValidFileName - empty string');
  TestAssert(not TPathUtils.IsValidFileName(''), 'Empty should be invalid');

  TestStart('TPathUtils.IsValidFileName - colon in name');
  TestAssert(not TPathUtils.IsValidFileName('test:name.txt'), 'Should be invalid');
end;

procedure Test_PathUtils_ChangeExtension;
begin
  TestStart('TPathUtils.ChangeExtension - change extension');
  TestAssert(TPathUtils.ChangeExtension('test.txt', '.pdf') = 'test.pdf', 'Wrong result');

  TestStart('TPathUtils.ChangeExtension - add extension');
  TestAssert(TPathUtils.ChangeExtension('test', '.txt') = 'test.txt', 'Wrong result');

  TestStart('TPathUtils.ChangeExtension - remove extension');
  TestAssert(TPathUtils.ChangeExtension('test.txt', '') = 'test', 'Wrong result');
end;

procedure Test_PathUtils_HasExtensionIn;
begin
  TestStart('TPathUtils.HasExtensionIn - match first');
  TestAssert(TPathUtils.HasExtensionIn('test.txt', ['txt', 'pdf']), 'Should match');

  TestStart('TPathUtils.HasExtensionIn - match second');
  TestAssert(TPathUtils.HasExtensionIn('test.pdf', ['txt', 'pdf']), 'Should match');

  TestStart('TPathUtils.HasExtensionIn - no match');
  TestAssert(not TPathUtils.HasExtensionIn('test.doc', ['txt', 'pdf']), 'Should not match');

  TestStart('TPathUtils.HasExtensionIn - case insensitive');
  TestAssert(TPathUtils.HasExtensionIn('test.TXT', ['txt', 'pdf']), 'Should match case-insensitive');
end;

{==============================================================================}
{ TFileUtils Tests }
{