{*******************************************************************************
  AllToolkit - INI File Utilities Test Suite for Delphi
  
  Comprehensive test suite for the INI file utilities module.
  Tests all major functionality including file operations, sections,
  keys, and data type conversions.
  
  Run with: fpc ini_utils_test.pas && ./ini_utils_test
  Or:       dcc32 ini_utils_test.pas && ./ini_utils_test.exe
********************************************************************************}

program ini_utils_test;

uses
  SysUtils, Classes, IniFiles, mod;

var
  TestCount: Integer = 0;
  PassCount: Integer = 0;
  FailCount: Integer = 0;
  TempDir: string;

procedure TestResult(TestName: string; Condition: Boolean);
begin
  TestCount := TestCount + 1;
  if Condition then
  begin
    PassCount := PassCount + 1;
    WriteLn('[PASS] ', TestName);
  end
  else
  begin
    FailCount := FailCount + 1;
    WriteLn('[FAIL] ', TestName);
  end;
end;

procedure Setup;
begin
  Randomize;
  TempDir := GetTempDir + 'alltoolkit_test_' + IntToStr(Random(10000)) + PathDelim;
  ForceDirectories(TempDir);
  WriteLn('Test directory: ', TempDir);
  WriteLn('');
end;

{ Test: File Operations }
procedure TestFileOperations;
var
  Ini: TIniUtils;
  FilePath: string;
  BackupPath: string;
begin
  WriteLn('=== File Operations Tests ===');
  
  // Test 1: Create new INI file
  FilePath := TempDir + 'test1.ini';
  Ini := TIniUtils.Create(FilePath, False);
  try
    Ini.WriteString('Section1', 'Key1', 'Value1');
    Ini.Save;
    TestResult('Create new INI file', SysUtils.FileExists(FilePath));
  finally
    Ini.Free;
  end;
  
  // Test 2: File exists check
  Ini := TIniUtils.Create(FilePath, False);
  try
    TestResult('File exists check', Ini.IniFileExists);
  finally
    Ini.Free;
  end;
  
  // Test 3: Create backup
  Ini := TIniUtils.Create(FilePath, False);
  try
    BackupPath := Ini.CreateBackup;
    TestResult('Create backup file', SysUtils.FileExists(BackupPath));
  finally
    Ini.Free;
  end;
  
  // Test 4: Save As
  Ini := TIniUtils.Create(FilePath, False);
  try
    Ini.WriteString('Section1', 'Key1', 'Value1');
    Ini.SaveAs(TempDir + 'test1_copy.ini');
    TestResult('Save As creates new file', SysUtils.FileExists(TempDir + 'test1_copy.ini'));
  finally
    Ini.Free;
  end;
  
  WriteLn('');
end;

{ Test: Section Operations }
procedure TestSectionOperations;
var
  Ini: TIniUtils;
  FilePath: string;
  Sections: TStringList;
begin
  WriteLn('=== Section Operations Tests ===');
  
  FilePath := TempDir + 'test2.ini';
  Ini := TIniUtils.Create(FilePath, False);
  try
    // Test 1: Create section
    Ini.WriteString('Database', 'Host', 'localhost');
    Ini.WriteString('Database', 'Port', '3306');
    Ini.WriteString('Application', 'Name', 'TestApp');
    Ini.Save;
    
    TestResult('Section exists', Ini.SectionExists('Database'));
    
    // Test 2: Get sections
    Sections := Ini.GetSections;
    try
      TestResult('Get sections count', Sections.Count = 2);
    finally
      Sections.Free;
    end;
    
    // Test 3: Get section count
    TestResult('Get section count', Ini.GetSectionCount = 2);
    
    // Test 4: Rename section
    Ini.RenameSection('Database', 'DBConfig');
    TestResult('Rename section - old name gone', not Ini.SectionExists('Database'));
    TestResult('Rename section - new name exists', Ini.SectionExists('DBConfig'));
    TestResult('Rename section - data preserved', Ini.ReadString('DBConfig', 'Host', '') = 'localhost');
    
    // Test 5: Clear section
    Ini.ClearSection('DBConfig');
    TestResult('Clear section - section still exists', Ini.SectionExists('DBConfig'));
    TestResult('Clear section - keys removed', Ini.GetKeyCount('DBConfig') = 0);
    
    // Test 6: Delete section
    Ini.DeleteSection('DBConfig');
    TestResult('Delete section', not Ini.SectionExists('DBConfig'));
    
  finally
    Ini.Free;
  end;
  
  WriteLn('');
end;

{ Test: Key Operations }
procedure TestKeyOperations;
var
  Ini: TIniUtils;
  FilePath: string;
  Keys: TStringList;
begin
  WriteLn('=== Key Operations Tests ===');
  
  FilePath := TempDir + 'test3.ini';
  Ini := TIniUtils.Create(FilePath, False);
  try
    // Setup
    Ini.WriteString('Settings', 'Username', 'admin');
    Ini.WriteString('Settings', 'Password', 'secret');
    Ini.WriteString('Settings', 'Timeout', '30');
    
    // Test 1: Key exists
    TestResult('Key exists', Ini.KeyExists('Settings', 'Username'));
    
    // Test 2: Get keys
    Keys := Ini.GetKeys('Settings');
    try
      TestResult('Get keys count', Keys.Count = 3);
    finally
      Keys.Free;
    end;
    
    // Test 3: Get key count
    TestResult('Get key count', Ini.GetKeyCount('Settings') = 3);
    
    // Test 4: Rename key
    Ini.RenameKey('Settings', 'Password', 'Pass');
    TestResult('Rename key - old key gone', not Ini.KeyExists('Settings', 'Password'));
    TestResult('Rename key - new key exists', Ini.KeyExists('Settings', 'Pass'));
    TestResult('Rename key - value preserved', Ini.ReadString('Settings', 'Pass', '') = 'secret');
    
    // Test 5: Delete key
    Ini.DeleteKey('Settings', 'Pass');
    TestResult('Delete key', not Ini.KeyExists('Settings', 'Pass'));
    
  finally
    Ini.Free;
  end;
  
  WriteLn('');
end;

{ Test: Read/Write Operations }
procedure TestReadWriteOperations;
var
  Ini: TIniUtils;
  FilePath: string;
  IntVal: Integer;
  FloatVal: Double;
  BoolVal: Boolean;
begin
  WriteLn('=== Read/Write Operations Tests ===');
  
  FilePath := TempDir + 'test4.ini';
  Ini := TIniUtils.Create(FilePath, False);
  try
    // Test 1: String read/write
    Ini.WriteString('Data', 'Name', 'John Doe');
    TestResult('Read/Write string', Ini.ReadString('Data', 'Name', '') = 'John Doe');
    
    // Test 2: Integer read/write
    Ini.WriteInteger('Data', 'Age', 30);
    TestResult('Read/Write integer', Ini.ReadInteger('Data', 'Age', 0) = 30);
    
    // Test 3: Float read/write
    Ini.WriteFloat('Data', 'Score', 95.5);
    TestResult('Read/Write float', Abs(Ini.ReadFloat('Data', 'Score', 0) - 95.5) < 0.001);
    
    // Test 4: Boolean read/write
    Ini.WriteBool('Data', 'Active', True);
    TestResult('Read/Write boolean', Ini.ReadBool('Data', 'Active', False) = True);
    
    // Test 5: DateTime read/write
    Ini.WriteDateTime('Data', 'Created', EncodeDate(2024, 1, 15));
    TestResult('Read/Write datetime', Ini.ReadDateTime('Data', 'Created', 0) = EncodeDate(2024, 1, 15));
    
    // Test 6: Default values
    TestResult('Default string', Ini.ReadString('Data', 'NonExistent', 'default') = 'default');
    TestResult('Default integer', Ini.ReadInteger('Data', 'NonExistent', 42) = 42);
    TestResult('Default float', Ini.ReadFloat('Data', 'NonExistent', 3.14) = 3.14);
    TestResult('Default boolean', Ini.ReadBool('Data', 'NonExistent', True) = True);
    
    // Test 7: TryRead functions - success
    TestResult('TryRead integer success', Ini.TryReadInteger('Data', 'Age', IntVal) and (IntVal = 30));
    TestResult('TryRead float success', Ini.TryReadFloat('Data', 'Score', FloatVal) and (Abs(FloatVal - 95.5) < 0.001));
    TestResult('TryRead bool success', Ini.TryReadBool('Data', 'Active', BoolVal) and BoolVal);
    
    // Test 8: TryRead functions - failure
    TestResult('TryRead integer failure', not Ini.TryReadInteger('Data', 'NonExistent', IntVal));
    TestResult('TryRead float failure', not Ini.TryReadFloat('Data', 'NonExistent', FloatVal));
    TestResult('TryRead bool failure', not Ini.TryReadBool('Data', 'NonExistent', BoolVal));
    
  finally
    Ini.Free;
  end;
  
  WriteLn('');
end;

{ Test: Value Operations }
procedure TestValueOperations;
var
  Ini: TIniUtils;
  FilePath: string;
begin
  WriteLn('=== Value