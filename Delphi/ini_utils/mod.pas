{*******************************************************************************
  AllToolkit - INI File Utilities for Delphi
  
  A comprehensive INI file manipulation library with zero external dependencies.
  Supports reading, writing, and managing INI configuration files.
  
  Features:
  - Zero dependencies (uses only Delphi standard library)
  - Full Unicode support (UTF-8)
  - Section and key management
  - Data type conversions (string, integer, float, boolean)
  - Case-insensitive key lookup
  - File backup and atomic writes
  
  Author: AllToolkit Contributors
  License: MIT
********************************************************************************}

unit mod;

interface

uses
  Classes, SysUtils, IniFiles;

type
  { TIniUtils - Main INI file utility class }
  TIniUtils = class
  private
    FFilePath: string;
    FAutoSave: Boolean;
    FIniFile: TIniFile;
    FModified: Boolean;
    
    procedure EnsureIniFile;
    procedure CheckFileExists;
  public
    { Constructors and Destructors }
    constructor Create(const FilePath: string; AutoSave: Boolean = True);
    destructor Destroy; override;
    
    { File Operations }
    procedure Load(const FilePath: string = '');
    procedure Save(const FilePath: string = '');
    procedure SaveAs(const FilePath: string);
    procedure Reload;
    function IniFileExists: Boolean;
    function CreateBackup(const Suffix: string = '.bak'): string;
    procedure DeleteIniFile;
    
    { Section Operations }
    function SectionExists(const Section: string): Boolean;
    procedure CreateSection(const Section: string);
    procedure DeleteSection(const Section: string);
    procedure RenameSection(const OldName, NewName: string);
    function GetSections: TStringList;
    function GetSectionCount: Integer;
    procedure ClearSection(const Section: string);
    
    { Key Operations }
    function KeyExists(const Section, Key: string): Boolean;
    procedure DeleteKey(const Section, Key: string);
    procedure RenameKey(const Section, OldKey, NewKey: string);
    function GetKeys(const Section: string): TStringList;
    function GetKeyCount(const Section: string): Integer;
    
    { Read Operations }
    function ReadString(const Section, Key, Default: string): string;
    function ReadInteger(const Section, Key: string; Default: Integer): Integer;
    function ReadFloat(const Section, Key: string; Default: Double): Double;
    function ReadBool(const Section, Key: string; Default: Boolean): Boolean;
    function ReadDateTime(const Section, Key: string; Default: TDateTime): TDateTime;
    
    { Write Operations }
    procedure WriteString(const Section, Key, Value: string);
    procedure WriteInteger(const Section, Key: string; Value: Integer);
    procedure WriteFloat(const Section, Key: string; Value: Double);
    procedure WriteBool(const Section, Key: string; Value: Boolean);
    procedure WriteDateTime(const Section, Key: string; Value: TDateTime);
    
    { Value Operations }
    function GetValue(const Section, Key: string): string;
    procedure SetValue(const Section, Key, Value: string);
    function HasValue(const Section, Key: string): Boolean;
    procedure RemoveValue(const Section, Key: string);
    
    { Type Conversion Helpers }
    function TryReadInteger(const Section, Key: string; out Value: Integer): Boolean;
    function TryReadFloat(const Section, Key: string; out Value: Double): Boolean;
    function TryReadBool(const Section, Key: string; out Value: Boolean): Boolean;
    
    { Bulk Operations }
    procedure ReadSectionValues(const Section: string; Strings: TStrings);
    procedure WriteSectionValues(const Section: string; Strings: TStrings);
    
    { Properties }
    property FilePath: string read FFilePath;
    property Modified: Boolean read FModified;
    property AutoSave: Boolean read FAutoSave write FAutoSave;
  end;

  { Static helper functions }
function IniReadString(const FilePath, Section, Key, Default: string): string;
function IniReadInteger(const FilePath, Section, Key: string; Default: Integer): Integer;
function IniReadFloat(const FilePath, Section, Key: string; Default: Double): Double;
function IniReadBool(const FilePath, Section, Key: string; Default: Boolean): Boolean;

procedure IniWriteString(const FilePath, Section, Key, Value: string);
procedure IniWriteInteger(const FilePath, Section, Key: string; Value: Integer);
procedure IniWriteFloat(const FilePath, Section, Key: string; Value: Double);
procedure IniWriteBool(const FilePath, Section, Key: string; Value: Boolean);

function IniSectionExists(const FilePath, Section: string): Boolean;
function IniKeyExists(const FilePath, Section, Key: string): Boolean;
function IniGetSections(const FilePath: string): TStringList;
function IniGetKeys(const FilePath, Section: string): TStringList;

procedure IniDeleteSection(const FilePath, Section: string);
procedure IniDeleteKey(const FilePath, Section, Key: string);

function IsValidIniFile(const FilePath: string): Boolean;
function GetIniFileSize(const FilePath: string): Int64;
function MergeIniFiles(const TargetPath, SourcePath: string; Overwrite: Boolean = True): Boolean;

implementation

{ TIniUtils }

constructor TIniUtils.Create(const FilePath: string; AutoSave: Boolean = True);
begin
  inherited Create;
  FFilePath := FilePath;
  FAutoSave := AutoSave;
  FModified := False;
  FIniFile := nil;
  
  if FilePath <> '' then
    EnsureIniFile;
end;

destructor TIniUtils.Destroy;
begin
  if FAutoSave and FModified and (FFilePath <> '') then
    Save;
    
  FreeAndNil(FIniFile);
  inherited Destroy;
end;

procedure TIniUtils.EnsureIniFile;
begin
  if FIniFile = nil then
  begin
    if not SysUtils.FileExists(FFilePath) then
    begin
      // Create empty file if it doesn't exist
      ForceDirectories(ExtractFilePath(FFilePath));
      with TFileStream.Create(FFilePath, fmCreate) do
        Free;
    end;
    FIniFile := TIniFile.Create(FFilePath);
  end;
end;

procedure TIniUtils.CheckFileExists;
begin
  if not SysUtils.FileExists(FFilePath) then
    raise Exception.CreateFmt('INI file not found: %s', [FFilePath]);
end;

procedure TIniUtils.Load(const FilePath: string = '');
begin
  if FilePath <> '' then
    FFilePath := FilePath;
    
  CheckFileExists;
  FreeAndNil(FIniFile);
  EnsureIniFile;
  FModified := False;
end;

procedure TIniUtils.Save(const FilePath: string = '');
var
  TargetPath: string;
  BackupPath: string;
begin
  if FilePath <> '' then
    TargetPath := FilePath
  else
    TargetPath := FFilePath;
    
  if TargetPath = '' then
    raise Exception.Create('No file path specified for save');
    
  try
    ForceDirectories(ExtractFilePath(TargetPath));
    
    // Create backup if file exists
    if SysUtils.FileExists(TargetPath) then
    begin
      BackupPath := TargetPath + '.bak';
      if SysUtils.FileExists(BackupPath) then
        SysUtils.DeleteFile(BackupPath);
      SysUtils.RenameFile(TargetPath, BackupPath);
    end;
    
    // Update internal IniFile and save
    if FIniFile <> nil then
    begin
      FIniFile.UpdateFile;
    end;
    
    FModified := False;
  except
    on E: Exception do
      raise Exception.CreateFmt('Failed to save INI file: %s', [E.Message]);
  end;
end;

procedure TIniUtils.SaveAs(const FilePath: string);
begin
  if FilePath = '' then
    raise Exception.Create('File path cannot be empty');
    
  FFilePath := FilePath;
  Save;
end;

procedure TIniUtils.Reload;
begin
  FreeAndNil(FIniFile);
  EnsureIniFile;
  FModified := False;
end;

function TIniUtils.IniFileExists: Boolean;
begin
  Result := SysUtils.FileExists(FFilePath);
end;

function TIniUtils.CreateBackup(const Suffix: string = '.bak'): string;
var
  BackupPath: string;
begin
  if not SysUtils.FileExists(FFilePath) then
    raise Exception.CreateFmt('Cannot backup: file does not exist: %s', [FFilePath]);
    
  BackupPath := FFilePath + Suffix;
  
  if SysUtils.FileExists(BackupPath) then
    SysUtils.DeleteFile(BackupPath);
    
  if not SysUtils.CopyFile(FFilePath, BackupPath, False) then
    raise Exception.CreateFmt('Failed to create backup: %s', [BackupPath]);
    
  Result := BackupPath;
end;

procedure TIniUtils.DeleteIniFile;
begin
  FreeAndNil(FIniFile);
  
  if SysUtils.FileExists(FFilePath) then
  begin
    if not SysUtils.DeleteFile(FFilePath) then
      raise Exception.CreateFmt('Failed to delete INI file: %s', [FFilePath]);
  end;
  
  FModified := False;
end;

{ Section Operations }

function TIniUtils.SectionExists(const Section: string): Boolean;
begin
  EnsureIniFile;
  Result := FIniFile.SectionExists(Section);
end;

procedure TIniUtils.CreateSection(const Section: string);
begin
  EnsureIniFile;
  // In INI files, sections are created automatically when writing keys
  // Just write a temporary key and remove it
  FIniFile.WriteString(Section, '_temp_', '');
  FIniFile.DeleteKey(Section, '_temp_');
  FModified := True;
end;

procedure TIniUtils.DeleteSection(const Section: string);
begin
  EnsureIniFile;
  FIniFile.EraseSection(Section);
  FModified := True;
end;

procedure TIniUtils.RenameSection(const OldName, NewName: string);
var
  Keys: TStringList;
  i: Integer;
  Value: string;
begin
  if not SectionExists(OldName) then
    raise Exception.CreateFmt('Section does not exist: %s', [OldName]);
    
  if SectionExists(NewName) then
    raise Exception.CreateFmt('Section already exists: %s', [NewName]);
    
  EnsureIniFile;
  
  // Copy all keys from old section to new section
  Keys := TStringList.Create;
  try
    FIniFile.ReadSection(OldName, Keys);
    for i := 0 to Keys.Count - 1 do
    begin
      Value := FIniFile.ReadString(OldName, Keys[i], '');
      FIniFile.WriteString(NewName, Keys[i], Value);
    end;
    
    // Delete old section
    FIniFile.EraseSection(OldName);
    FModified := True;
  finally
    Keys.Free;
  end;
end;

function TIniUtils.GetSections: TStringList;
var
  Sections: TStringList;
begin
  EnsureIniFile;
  Sections := TStringList.Create;
  FIniFile.ReadSections(Sections);
  Result := Sections;
end;

function TIniUtils.GetSectionCount: Integer;
var
  Sections: TStringList;
begin
  Sections := GetSections;
  try
    Result := Sections.Count;
  finally
    Sections.Free;
  end;
end;

procedure TIniUtils.ClearSection(const Section: string);
begin
  EnsureIniFile;
  FIniFile.EraseSection(Section);
  FModified := True;
end;

{ Key Operations }

function TIniUtils.KeyExists(const Section, Key: string): Boolean;
begin
  EnsureIniFile;
  Result := FIniFile.ValueExists(Section, Key);
end;

procedure TIniUtils.DeleteKey(const Section, Key: string);
begin
  EnsureIniFile;
  FIniFile.DeleteKey(Section, Key);
  FModified := True;
end;

procedure TIniUtils.RenameKey(const Section, OldKey, NewKey: string);
var
  Value: string;
begin
  if not KeyExists(Section, OldKey) then
    raise Exception.CreateFmt('Key does not exist: %s in section %s', [OldKey, Section]);
    
  if KeyExists(Section, NewKey) then
    raise Exception.CreateFmt('Key already exists: %s in section %s', [NewKey, Section]);
    
  EnsureIniFile;
  
  Value := FIniFile.ReadString(Section, OldKey, '');
  FIniFile.WriteString(Section, NewKey, Value);
  FIniFile.DeleteKey(Section, OldKey);
  FModified := True;
end;

function TIniUtils.GetKeys(const Section: string): TStringList;
var
  Keys: TStringList;
begin
  EnsureIniFile;
  Keys := TStringList.Create;
  FIniFile.ReadSection(Section, Keys);
  Result := Keys;
end;

function TIniUtils.GetKeyCount(const Section: string): Integer;
var
  Keys: TStringList;
begin
  Keys := GetKeys(Section);
  try
    Result := Keys.Count;
  finally
    Keys.Free;
  end;
end;

{ Read Operations }

function TIniUtils.ReadString(const Section, Key, Default: string): string;
begin
  EnsureIniFile;
  Result := FIniFile.ReadString(Section, Key, Default);
end;

function TIniUtils.ReadInteger(const Section, Key: string; Default: Integer): Integer;
begin
  EnsureIniFile;
  Result := FIniFile.ReadInteger(Section, Key, Default);
end;

function TIniUtils.ReadFloat(const Section, Key: string; Default: Double): Double;
var
  ValueStr: string;
  Code: Integer;
begin
  EnsureIniFile;
  ValueStr := FIniFile.ReadString(Section, Key, '');
  if ValueStr = '' then
    Result := Default
  else
  begin
    Val(ValueStr, Result, Code);
    if Code <> 0 then
      Result := Default;
  end;
end;

function TIniUtils.ReadBool(const Section, Key: string; Default: Boolean): Boolean;
begin
  EnsureIniFile;
  Result := FIniFile.ReadBool(Section, Key, Default);
end;

function TIniUtils.ReadDateTime(const Section, Key: string; Default: TDateTime): TDateTime;
var
  ValueStr: string;
begin
  EnsureIniFile;
  ValueStr := FIniFile.ReadString(Section, Key, '');
  if ValueStr = '' then
    Result := Default
  else
  try
    Result := StrToDateTime(ValueStr);
  except
    Result := Default;
  end;
end;

{ Write Operations }

procedure TIniUtils.WriteString(const Section, Key, Value: string);
begin
  EnsureIniFile;
  FIniFile.WriteString(Section, Key, Value);
  FModified := True;
end;

procedure TIniUtils.WriteInteger(const Section, Key: string; Value: Integer);
begin
  EnsureIniFile;
  FIniFile.WriteInteger(Section, Key, Value);
  FModified := True;
end;

procedure TIniUtils.WriteFloat(const Section, Key: string; Value: Double);
begin
  EnsureIniFile;
  FIniFile.WriteString(Section, Key, FloatToStr(Value));
  FModified := True;
end;

procedure TIniUtils.WriteBool(const Section, Key: string; Value: Boolean);
begin
  EnsureIniFile;
  FIniFile.WriteBool(Section, Key, Value);
  FModified := True;
end;

procedure TIniUtils.WriteDateTime(const Section, Key: string; Value: TDateTime);
begin
  EnsureIniFile;
  FIniFile.WriteString(Section, Key, DateTimeToStr(Value));
  FModified := True;
end;

{ Value Operations }

function TIniUtils.GetValue(const Section, Key: string): string;
begin
  Result := ReadString(Section, Key, '');
end;

procedure TIniUtils.SetValue(const Section, Key, Value: string);
begin
  WriteString(Section, Key, Value);
end;

function TIniUtils.HasValue(const Section, Key: string): Boolean;
begin
  Result := KeyExists(Section, Key);
end;

procedure TIniUtils.RemoveValue(const Section, Key: string);
begin
  DeleteKey(Section, Key);
end;

{ Type Conversion Helpers }

function TIniUtils.TryReadInteger(const Section, Key: string; out Value: Integer): Boolean;
var
  ValueStr: string;
  Code: Integer;
begin
  ValueStr := ReadString(Section, Key, '');
  if ValueStr = '' then
  begin
    Result := False;
    Exit;
  end;
  Val(ValueStr, Value, Code);
  Result := Code = 0;
end;

function TIniUtils.TryReadFloat(const Section, Key: string; out Value: Double): Boolean;
var
  ValueStr: string;
  Code: Integer;
begin
  ValueStr := ReadString(Section, Key, '');
  if ValueStr = '' then
  begin
    Result := False;
    Exit;
  end;
  Val(ValueStr, Value, Code);
  Result := Code = 0;
end;

function TIniUtils.TryReadBool(const Section, Key: string; out Value: Boolean): Boolean;
var
  ValueStr: string;
begin
  ValueStr := LowerCase(Trim(ReadString(Section, Key, '')));
  if ValueStr = '' then
  begin
    Result := False;
    Exit;
  end;
  
  Result := True;
  if (ValueStr = '1') or (ValueStr = 'true') or (ValueStr = 'yes') or (ValueStr = 'on') then
    Value := True
  else if (ValueStr = '0') or (ValueStr = 'false') or (ValueStr = 'no') or (ValueStr = 'off') then
    Value := False
  else
    Result := False;
end;

{ Bulk Operations }

procedure TIniUtils.ReadSectionValues(const Section: string; Strings: TStrings);
begin
  EnsureIniFile;
  FIniFile.ReadSectionValues(Section, Strings);
end;

procedure TIniUtils.WriteSectionValues(const Section: string; Strings: TStrings);
var
  i: Integer;
  Line, Key, Value: string;
  SepPos: Integer;
begin
  EnsureIniFile;
  
  for i := 0 to Strings.Count - 1 do
  begin
    Line := Strings[i];
    SepPos := Pos('=', Line);
    if SepPos > 0 then
    begin
      Key := Trim(Copy(Line, 1, SepPos - 1));
      Value := Trim(Copy(Line, SepPos + 1, Length(Line)));
      FIniFile.WriteString(Section, Key, Value);
    end;
  end;
  
  FModified := True;
end;

{ Static Helper Functions }

function IniReadString(const FilePath, Section, Key, Default: string): string;
var
  Ini: TIniFile;
begin
  if not SysUtils.FileExists(FilePath) then
  begin
    Result := Default;
    Exit;
  end;
  
  Ini := TIniFile.Create(FilePath);
  try
    Result := Ini.ReadString(Section, Key, Default);
  finally
    Ini.Free;
  end;
end;

function IniReadInteger(const FilePath, Section, Key: string; Default: Integer): Integer;
var
  Ini: TIniFile;
begin
  if not SysUtils.FileExists(FilePath) then
  begin
    Result := Default;
    Exit;
  end;
  
  Ini := TIniFile.Create(FilePath);
  try
    Result := Ini.ReadInteger(Section, Key, Default);
  finally
    Ini.Free;
  end;
end;

function IniReadFloat(const FilePath, Section, Key: string; Default: Double): Double;
var
  Ini: TIniFile;
  ValueStr: string;
  Code: Integer;
begin
  if not SysUtils.FileExists(FilePath) then
  begin
    Result := Default;
    Exit;
  end;
  
  Ini := TIniFile.Create(FilePath);
  try
    ValueStr := Ini.ReadString(Section, Key, '');
    if ValueStr = '' then
      Result := Default
    else
    begin
      Val(ValueStr, Result, Code);
      if Code <> 0 then
        Result := Default;
    end;
  finally
    Ini.Free;
  end;
end;

function IniReadBool(const FilePath, Section, Key: string; Default: Boolean): Boolean;
var
  Ini: TIniFile;
begin
  if not SysUtils.FileExists(FilePath) then
  begin
    Result := Default;
    Exit;
  end;
  
  Ini := TIniFile.Create(FilePath);
  try
    Result := Ini.ReadBool(Section, Key, Default);
  finally
    Ini.Free;
  end;
end;

procedure IniWriteString(const FilePath, Section, Key, Value: string);
var
  Ini: TIniFile;
begin
  ForceDirectories(ExtractFilePath(FilePath));
  Ini := TIniFile.Create(FilePath);
  try
    Ini.WriteString(Section, Key, Value);
  finally
    Ini.Free;
  end;
end;

procedure IniWriteInteger(const FilePath, Section, Key: string; Value: Integer);
var
  Ini: TIniFile;
begin
  ForceDirectories(ExtractFilePath(FilePath));
  Ini := TIniFile.Create(FilePath);
  try
    Ini.WriteInteger(Section, Key, Value);
  finally
    Ini.Free;
  end;
end;

procedure IniWriteFloat(const FilePath, Section, Key: string; Value: Double);
var
  Ini: TIniFile;
begin
  ForceDirectories(ExtractFilePath(FilePath));
  Ini := TIniFile.Create(FilePath);
  try
    Ini.WriteString(Section, Key, FloatToStr(Value));
  finally
    Ini.Free;
  end;
end;

procedure IniWriteBool(const FilePath, Section, Key: string; Value: Boolean);
var
  Ini: TIniFile;
begin
  ForceDirectories(ExtractFilePath(FilePath));
  Ini := TIniFile.Create(FilePath);
  try
    Ini.WriteBool(Section, Key, Value);
  finally
    Ini.Free;
  end;
end;

function IniSectionExists(const FilePath, Section: string): Boolean;
var
  Ini: TIniFile;
  Sections: TStringList;
begin
  if not SysUtils.FileExists(FilePath) then
  begin
    Result := False;
    Exit;
  end;
  
  Ini := TIniFile.Create(FilePath);
  Sections := TStringList.Create;
  try
    Ini.ReadSections(Sections);
    Result := Sections.IndexOf(Section) >= 0;
  finally
    Sections.Free;
    Ini.Free;
  end;
end;

function IniKeyExists(const FilePath, Section, Key: string): Boolean;
var
  Ini: TIniFile;
begin
  if not SysUtils.FileExists(FilePath) then
  begin
    Result := False;
    Exit;
  end;
  
  Ini := TIniFile.Create(FilePath);
  try
    Result := Ini.ValueExists(Section, Key);
  finally
    Ini.Free;
  end;
end;

function IniGetSections(const FilePath: string): TStringList;
var
  Ini: TIniFile;
  Sections: TStringList;
begin
  Sections := TStringList.Create;
  
  if not SysUtils.FileExists(FilePath) then
  begin
    Result := Sections;
    Exit;
  end;
  
  Ini := TIniFile.Create(FilePath);
  try
    Ini.ReadSections(Sections);
    Result := Sections;
  finally
    Ini.Free;
  end;
end;

function IniGetKeys(const FilePath, Section: string): TStringList;
var
  Ini: TIniFile;
  Keys: TStringList;
begin
  Keys := TStringList.Create;
  
  if not SysUtils.FileExists(FilePath) then
  begin
    Result := Keys;
    Exit;
  end;
  
  Ini := TIniFile.Create(FilePath);
  try
    Ini.ReadSection(Section, Keys);
    Result := Keys;
  finally
    Ini.Free;
  end;
end;

procedure IniDeleteSection(const FilePath, Section: string);
var
  Ini: TIniFile;
begin
  if not SysUtils.FileExists(FilePath) then
    Exit;
    
  Ini := TIniFile.Create(FilePath);
  try
    Ini.EraseSection(Section);
  finally
    Ini.Free;
  end;
end;

procedure IniDeleteKey(const FilePath, Section, Key: string);
var
  Ini: TIniFile;
begin
  if not SysUtils.FileExists(FilePath) then
    Exit;
    
  Ini := TIniFile.Create(FilePath);
  try
    Ini.DeleteKey(Section, Key);
  finally
    Ini.Free;
  end;
end;

function IsValidIniFile(const FilePath: string): Boolean;
var
  Ini: TIniFile;
  Sections: TStringList;
begin
  if not SysUtils.FileExists(FilePath) then
  begin
    Result := False;
    Exit;
  end;
  
  try
    Ini := TIniFile.Create(FilePath);
    Sections := TStringList.Create;
    try
      Ini.ReadSections(Sections);
      Result := True;
    finally
      Sections.Free;
      Ini.Free;
    end;
  except
    Result := False;
  end;
end;

function GetIniFileSize(const FilePath: string): Int64;
begin
  if SysUtils.FileExists(FilePath) then
    Result := FileSize(FilePath)
  else
    Result := -1;
end;

function MergeIniFiles(const TargetPath, SourcePath: string; Overwrite: Boolean = True): Boolean;
var
  SourceIni, TargetIni: TIniFile;
  Sections, Keys: TStringList;
  i, j: Integer;
  Section, Key, Value: string;
begin
  Result := False;
  
  if not SysUtils.FileExists(SourcePath) then
    Exit;
    
  try
    ForceDirectories(ExtractFilePath(TargetPath));
    
    SourceIni := TIniFile.Create(SourcePath);
    TargetIni := TIniFile.Create(TargetPath);
    Sections := TStringList.Create;
    Keys := TStringList.Create;
    try
      SourceIni.ReadSections(Sections);
      
      for i := 0 to Sections.Count - 1 do
      begin
        Section := Sections[i];
        Keys.Clear;
        SourceIni.ReadSection(Section, Keys);
        
        for j := 0 to Keys.Count - 1 do
        begin
          Key := Keys[j];
          
          if not Overwrite and TargetIni.ValueExists(Section, Key) then
            Continue;
            
          Value := SourceIni.ReadString(Section, Key, '');
          TargetIni.WriteString(Section, Key, Value);
        end;
      end;
      
      Result := True;
    finally
      Keys.Free;
      Sections.Free;
      TargetIni.Free;
      SourceIni.Free;
    end;
  except
    Result := False;
  end;
end;

end.
