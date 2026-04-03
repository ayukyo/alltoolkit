{*******************************************************************************
 * AllToolkit - Delphi File Utilities
 *
 * A zero-dependency file operation utility library using only Delphi standard library.
 * Provides file read/write, path operations, directory management and other common functions.
 *
 * Version: 1.0.0
 * Author: AllToolkit Contributors
 * License: MIT
 *******************************************************************************}

unit FileUtils;

interface

uses
  SysUtils, Classes;

type
  { File size format }
  TFileSizeFormat = (fsfBytes, fsfKB, fsfMB, fsfGB, fsfAuto);

  { File info record }
  TFileInfo = record
    Name: string;
    FullPath: string;
    Size: Int64;
    CreationTime: TDateTime;
    ModificationTime: TDateTime;
    AccessTime: TDateTime;
    IsDirectory: Boolean;
    IsReadOnly: Boolean;
    IsHidden: Boolean;
  end;

  { File info array }
  TFileInfoArray = array of TFileInfo;

  { Path utilities class }
  TPathUtils = class
  public
    class function Combine(const Path1, Path2: string): string;
    class function CombineMultiple(const Paths: array of string): string;
    class function GetFileName(const Path: string): string;
    class function GetFileNameWithoutExtension(const Path: string): string;
    class function GetExtension(const Path: string): string;
    class function GetDirectory(const Path: string): string;
    class function GetFullPath(const Path: string): string;
    class function HasExtension(const Path: string): Boolean;
    class function IsPathRooted(const Path: string): Boolean;
    class function IsValidFileName(const FileName: string): Boolean;
    class function ChangeExtension(const Path, NewExt: string): string;
    class function HasExtensionIn(const Path: string; const Extensions: array of string): Boolean;
  end;

  { File utilities class }
  TFileUtils = class
  public
    class function Exists(const Path: string): Boolean;
    class function IsEmpty(const Path: string): Boolean;
    class function ReadAllText(const Path: string; const DefaultValue: string = ''): string;
    class function ReadAllLines(const Path: string): TStringList;
    class function TryReadAllText(const Path: string; out Content: string): Boolean;
    class procedure WriteAllText(const Path: string; const Content: string; Append: Boolean = False);
    class procedure WriteAllLines(const Path: string; const Lines: TStringList);
    class function TryWriteAllText(const Path: string; const Content: string; Append: Boolean = False): Boolean;
    class procedure Copy(const SourcePath, DestPath: string; Overwrite: Boolean = True);
    class procedure Move(const SourcePath, DestPath: string; Overwrite: Boolean = True);
    class procedure Delete(const Path: string; Force: Boolean = False);
    class function TryDelete(const Path: string): Boolean;
    class function GetSize(const Path: string): Int64;
    class function GetSizeString(const Path: string; Format: TFileSizeFormat = fsfAuto): string;
    class function FormatSize(const Size: Int64; Format: TFileSizeFormat = fsfAuto): string;
    class function GetCreationTime(const Path: string): TDateTime;
    class function GetModificationTime(const Path: string): TDateTime;
    class function GetAccessTime(const Path: string): TDateTime;
    class function GetTempFileName(const Extension: string = '.tmp'): string;
    class function GetTempPath: string;
    class function GetUniqueFileName(const Path: string): string;
  end;

  { Directory utilities class }
  TDirectoryUtils = class
  public
    class function Exists(const Path: string): Boolean;
    class procedure Create(const Path: string);
    class procedure CreateRecursive(const Path: string);
    class function TryCreate(const Path: string): Boolean;
    class procedure Delete(const Path: string; Recursive: Boolean = False);
    class procedure DeleteRecursive(const Path: string);
    class function TryDelete(const Path: string; Recursive: Boolean = False): Boolean;
    class procedure Move(const SourcePath, DestPath: string);
    class function GetFiles(const Path: string; const Pattern: string = '*.*'; Recursive: Boolean = False): TStringList;
    class function GetDirectories(const Path: string; Recursive: Boolean = False): TStringList;
    class function GetFileInfos(const Path: string; const Pattern: string = '*.*'; Recursive: Boolean = False): TFileInfoArray;
    class function GetCurrentDirectory: string;
    class procedure SetCurrentDirectory(const Path: string);
    class function GetParent(const Path: string): string;
    class function IsEmpty(const Path: string): Boolean;
    class function GetHomeDirectory: string;
    class function GetApplicationDirectory: string;
  end;

  { File filter class }
  TFileFilter = class
  public
    class function MatchesPattern(const FileName, Pattern: string): Boolean;
    class function MatchesPatterns(const FileName: string; const Patterns: array of string): Boolean;
    class function IsTextFile(const FileName: string): Boolean;
    class function IsImageFile(const FileName: string): Boolean;
    class function IsAudioFile(const FileName: string): Boolean;
    class function IsVideoFile(const FileName: string): Boolean;
    class function IsArchiveFile(const FileName: string): Boolean;
  end;

implementation

{==============================================================================}
{ TPathUtils Implementation }
{==============================================================================}

class function TPathUtils.Combine(const Path1, Path2: string): string;
var
  P1, P2: string;
begin
  P1 := Trim(Path1);
  P2 := Trim(Path2);
  if P1 = '' then Exit(P2);
  if P2 = '' then Exit(P1);
  while (P1 <> '') and (P1[Length(P1)] in ['\', '/']) do
    P1 := Copy(P1, 1, Length(P1) - 1);
  while (P2 <> '') and (P2[1] in ['\', '/']) do
    P2 := Copy(P2, 2, Length(P2) - 1);
  if P1 = '' then Result := P2
  else if P2 = '' then Result := P1
  else Result := P1 + PathDelim + P2;
end;

class function TPathUtils.CombineMultiple(const Paths: array of string): string;
var
  I: Integer;
begin
  if Length(Paths) = 0 then begin Result := ''; Exit; end;
  Result := Paths[0];
  for I := 1 to High(Paths) do
    Result := Combine(Result, Paths[I]);
end;

class function TPathUtils.GetFileName(const Path: string): string;
begin
  Result := ExtractFileName(Path);
end;

class function TPathUtils.GetFileNameWithoutExtension(const Path: string): string;
begin
  Result := ChangeFileExt(ExtractFileName(Path), '');
end;

class function TPathUtils.GetExtension(const Path: string): string;
begin
  Result := ExtractFileExt(Path);
  if (Result <> '') and (Result[1] = '.') then
    Result := LowerCase(Copy(Result, 2, Length(Result) - 1))
  else
    Result := LowerCase(Result);
end;

class function TPathUtils.GetDirectory(const Path: string): string;
begin
  Result := ExtractFilePath(Path);
  if (Result <> '') and (Result[Length(Result)] in ['\', '/']) then
    Result := Copy(Result, 1, Length(Result) - 1);
end;

class function TPathUtils.GetFullPath(const Path: string): string;
begin
  Result := ExpandFileName(Path);
end;

class function TPathUtils.HasExtension(const Path: string): Boolean;
begin
  Result := ExtractFileExt(Path) <> '';
end;

class function TPathUtils.IsPathRooted(const Path: string): Boolean;
begin
  Result := (Path <> '') and ((Path[1] = '\') or (Path[1] = '/') or
            (Length(Path) >= 2) and (Path[2] = ':'));
end;

class function TPathUtils.IsValidFileName(const FileName: string): Boolean;
const
  InvalidChars: set of Char = ['\', '/', ':', '*', '?', '"', '<', '>', '|'];
var
  I: Integer;
begin
  Result := FileName <> '';
  if Result then
    for I := 1 to Length(FileName) do
      if FileName[I] in InvalidChars then
      begin
        Result := False;
        Break;
      end;
end;

class function TPathUtils.ChangeExtension(const Path, NewExt: string): string;
begin
  Result := ChangeFileExt(Path, NewExt);
end;

class function TPathUtils.HasExtensionIn(const Path: string; const Extensions: array of string): Boolean;
var
  Ext: string;
  I: Integer;
begin
  Ext := GetExtension(Path);
  Result := False;
  for I := 0 to High(Extensions) do
    if LowerCase(Extensions[I]) = Ext then
    begin
      Result := True;
      Break;
    end;
end;

{==============================================================================}
{ TFileUtils Implementation }
{==============================================================================}

class function TFileUtils.Exists(const Path: string): Boolean;
begin
  Result := FileExists(Path);
end;

class function TFileUtils.IsEmpty(const Path: string): Boolean;
begin
  Result := Exists(Path) and (GetSize(Path) = 0);
end;

class function TFileUtils.ReadAllText(const Path: string; const DefaultValue: string = ''): string;
var
  SL: TStringList;
begin
  if not Exists(Path) then
  begin
    Result := DefaultValue;
    Exit;
  end;
  SL := TStringList.Create;
  try
    SL.LoadFromFile(Path);
    Result := SL.Text;
  except
    Result := DefaultValue;
  end;
  SL.Free;
end;

class function TFileUtils.ReadAllLines(const Path: string): TStringList;
var
  SL: TStringList;
begin
  SL := TStringList.Create;
  try
    if Exists(Path) then
      SL.LoadFromFile(Path);
    Result := SL;
  except
    Result := SL;
  end;
end;

class function TFileUtils.TryReadAllText(const Path: string; out Content: string): Boolean;
begin
  try
    Content := ReadAllText(Path);
    Result := True;
  except
    Content := '';
    Result := False;
  end;
end;

class procedure TFileUtils.WriteAllText(const Path: string; const Content: string; Append: Boolean = False);
var
  SL: TStringList;
  Mode: Word;
begin
  SL := TStringList.Create;
  try
    if Append and Exists(Path) then
    begin
      SL.LoadFromFile(Path);
      SL.Add(Content);
    end
    else
      SL.Text := Content;
    SL.SaveToFile(Path);
  finally
    SL.Free;
  end;
end;

class procedure TFileUtils.WriteAllLines(const Path: string; const Lines: TStringList);
begin
  if Lines <> nil then
    Lines.SaveToFile(Path);
end;

class function TFileUtils.TryWriteAllText(const Path: string; const Content: string; Append: Boolean = False): Boolean;
begin
  try
    WriteAllText(Path, Content, Append);
    Result := True;
  except
    Result := False;
  end;
end;

class procedure TFileUtils.Copy(const SourcePath, DestPath: string; Overwrite: Boolean = True);
begin
  if Exists(SourcePath) then
  begin
    if not Overwrite and Exists(DestPath) then
      Exit;
    SysUtils.CopyFile(SourcePath, DestPath, not Overwrite);
  end;
end;

class procedure TFileUtils.Move(const SourcePath, DestPath: string; Overwrite: Boolean = True);
begin
  if Exists(SourcePath) then
  begin
    if Exists(DestPath) then
    begin
      if not Overwrite then Exit;
      SysUtils.DeleteFile(DestPath);
    end;
    SysUtils.RenameFile(SourcePath, DestPath);
  end;
end;

class procedure TFileUtils.Delete(const Path: string; Force: Boolean = False);
begin
  if Exists(Path) then
    SysUtils.DeleteFile(Path);
end;

class function TFileUtils.TryDelete(const Path: string): Boolean;
begin
  try
    Delete(Path);
    Result := True;
  except
    Result := False;
  end;
end;

class function TFileUtils.GetSize(const Path: string): Int64;
var
  SR: TSearchRec;
begin
  Result := -1;
  if FindFirst(Path, faAnyFile, SR) = 0 then
  begin
    Result := SR.Size;
    FindClose(SR);
  end;
end;

class function TFileUtils.GetSizeString(const Path: string; Format: TFileSizeFormat = fsfAuto): string;
var
  Size: Int64;
begin
  Size := GetSize(Path);
  if Size < 0 then
    Result := 'N/A'
  else
    Result := FormatSize(Size, Format);
end;

class function TFileUtils.FormatSize(const Size: Int64; Format: TFileSizeFormat = fsfAuto): string;
const
  KB = 1024;
  MB = 1024 * KB;
  GB = 1024 * MB;
begin
  case Format of
    fsfBytes: Result := IntToStr(Size) + ' B';
    fsfKB: Result := FormatFloat('0.00', Size / KB) + ' KB';
    fsfMB: Result := FormatFloat('0.00', Size / MB) + ' MB';
    fsfGB: Result := FormatFloat('0.00', Size / GB) + ' GB';
    fsfAuto:
      begin
        if Size < KB then
          Result := IntToStr(Size) + ' B'
        else if Size < MB then
          Result := FormatFloat('0.00', Size / KB) + ' KB'
        else if Size < GB then
          Result := FormatFloat('0.00', Size / MB) + ' MB'
        else
          Result := FormatFloat('0.00', Size / GB) + ' GB';
      end;
  end;
end;

class function TFileUtils.GetCreationTime(const Path: string): TDateTime;
var
  SR: TSearchRec;
begin
  Result := 0;
  if FindFirst(Path, faAnyFile, SR) = 0 then
  begin
    Result := FileDateToDateTime(SR.Time);
    FindClose(SR);
  end;
end;

class function TFileUtils.GetModificationTime(const Path: string): TDateTime;
var
  SR: TSearchRec;
begin
  Result := 0;
  if FindFirst(Path, faAnyFile, SR) = 0 then
  begin
    Result := FileDateToDateTime(SR.Time);
    FindClose(SR);
  end;
end;

class function TFileUtils.GetAccessTime(const Path: string): TDateTime;
begin
  Result := GetModificationTime(Path);
end;

class function TFileUtils.GetTempFileName(const Extension: string = '.tmp'): string;
var
  TempDir, TempName: string;
  I: Integer;
begin
  TempDir := GetTempPath;
  Randomize;
  repeat
    TempName := Format('%stmp_%d_%d%s', [TempDir, Random(100000), Random(100000), Extension]);
  until not Exists(TempName);
  Result := TempName;
end;

class function TFileUtils.GetTempPath: string;
begin
  Result := SysUtils.GetTempDir;
  if (Result <> '') and (Result[Length(Result)] <> PathDelim) then
    Result := Result + PathDelim;
end;

class function TFileUtils.GetUniqueFileName(const Path: string): string;
var
  Dir, Name, Ext: string;
  I: Integer;
  NewPath: string;
begin
  if not Exists(Path) then
  begin
    Result := Path;
    Exit;
  end;
  Dir := ExtractFilePath(Path);
  Name := ChangeFileExt(ExtractFileName(Path), '');
  Ext := ExtractFileExt(Path);
  I := 1;
  repeat
    NewPath := Format('%s%s_%d%s', [Dir, Name, I, Ext]);
    Inc(I);
  until not Exists(NewPath);
  Result := NewPath;
end;

{==============================================================================}
{ TDirectoryUtils Implementation }
{==============================================================================}

class function TDirectoryUtils.Exists(const Path: string): Boolean;
begin
  Result := DirectoryExists(Path);
end;

class procedure TDirectoryUtils.Create(const Path: string);
begin
  if not Exists(Path) then
    CreateDir(Path);
end;

class procedure TDirectoryUtils.CreateRecursive(const Path: string);
begin
  if not Exists(Path) then
    ForceDirectories(Path);
end;

class function TDirectoryUtils.TryCreate(const Path: string): Boolean;
begin
  try
    CreateRecursive(Path);
    Result := True;
  except
    Result := False;
  end;
end;

class procedure TDirectoryUtils.Delete(const Path: string; Recursive: Boolean = False);
begin
  if Exists(Path) then
  begin
    if Recursive then
      DeleteRecursive(Path)
    else
      RemoveDir(Path);
  end;
end;

class procedure TDirectoryUtils.DeleteRecursive(const Path: string);
var
  SR: TSearchRec;
  FullPath: string;
begin
  if not Exists(Path) then Exit;
  
  if FindFirst(Path + PathDelim + '*.*', faAnyFile, SR) = 0 then
  begin
    repeat
      if (SR.Name <> '.') and (SR.Name <> '..') then
      begin
        FullPath := Path + PathDelim + SR.Name;
        if (SR.Attr and faDirectory) <> 0 then
          DeleteRecursive(FullPath)
        else
          SysUtils.DeleteFile(FullPath);
      end;
    until FindNext(SR) <> 0;
    FindClose(SR);
  end;
  RemoveDir(Path);
end;

class function TDirectoryUtils.TryDelete(const Path: string; Recursive: Boolean = False): Boolean;
begin
  try
    Delete(Path, Recursive);
    Result := True;
  except
    Result := False;
  end;
end;

class procedure TDirectoryUtils.Move(const SourcePath, DestPath: string);
begin
  if Exists(SourcePath) then
  begin
    if Exists(DestPath) then
      DeleteRecursive(DestPath);
    RenameFile(SourcePath, DestPath);
  end;
end;

class function TDirectoryUtils.GetFiles(const Path: string; const Pattern: string = '*.*'; Recursive: Boolean = False): TStringList;
var
  ResultList: TStringList;
  
  procedure SearchDir(const Dir: string; const Pat: string);
  var
    SR: TSearchRec;
    FullPath: string;
  begin
    if FindFirst(Dir + PathDelim + Pat, faAnyFile - faDirectory, SR) = 0 then
    begin
      repeat
        FullPath := Dir + PathDelim + SR.Name;
        ResultList.Add(FullPath);
      until FindNext(SR) <> 0;
      FindClose(SR);
    end;
    
    if Recursive then
    begin
      if FindFirst(Dir + PathDelim + '*.*', faDirectory, SR) = 0 then
      begin
        repeat
          if (SR.Name <> '.') and (SR.Name <> '..') then
            SearchDir(Dir + PathDelim + SR.Name, Pat);
        until FindNext(SR) <> 0;
        FindClose(SR);
      end;
    end;
  end;
  
begin
  ResultList := TStringList.Create;
  if Exists(Path) then
    SearchDir(Path, Pattern);
  Result := ResultList;
end;

class function TDirectoryUtils.GetDirectories(const Path: string; Recursive: Boolean = False): TStringList;
var
  ResultList: TStringList;
  
  procedure SearchDir(const Dir: string);
  var
    SR: TSearchRec;
    FullPath: string;
  begin
    if FindFirst(Dir + PathDelim + '*.*', faDirectory, SR) = 0 then
    begin
      repeat
        if (SR.Name <> '.') and (SR.Name <> '..') then
        begin
          FullPath := Dir + PathDelim + SR.Name;
          ResultList.Add(FullPath);
          if Recursive then
            SearchDir(FullPath);
        end;
      until FindNext(SR) <> 0;
      FindClose(SR);
    end;
  end;
  
begin
  ResultList := TStringList.Create;
  if Exists(Path) then
    SearchDir(Path);
  Result := ResultList;
end;

class function TDirectoryUtils.GetFileInfos(const Path: string; const Pattern: string = '*.*'; Recursive: Boolean = False): TFileInfoArray;
var
  ResultArray: TFileInfoArray;
  Count: Integer;
  
  procedure SearchDir(const Dir: string; const Pat: string);
  var
    SR: TSearchRec;
    FullPath: string;
  begin
    if FindFirst(Dir + PathDelim + Pat, faAnyFile, SR) = 0 then
    begin
      repeat
        if (SR.Name <> '.') and (SR.Name <> '..') then
        begin
          FullPath := Dir + PathDelim + SR.Name;
          Inc(Count);
          SetLength(ResultArray, Count);
          with ResultArray[Count - 1] do
          begin
            Name := SR.Name;
            FullPath := FullPath;
            Size := SR.Size;
            CreationTime := FileDateToDateTime(SR.Time);
            ModificationTime := FileDateToDateTime(SR.Time);
            AccessTime := FileDateToDateTime(SR.Time);
            IsDirectory := (SR.Attr and faDirectory) <> 0;
            IsReadOnly := (SR.Attr and faReadOnly) <> 0;
            IsHidden := (SR.Attr and faHidden) <> 0;
          end;
          
          if Recursive and ((SR.Attr and faDirectory) <> 0) then
            SearchDir(FullPath, Pat);
        end;
      until FindNext(SR) <> 0;
      FindClose(SR);
    end;
  end;
  
begin
  Count := 0;
  ResultArray := nil;
  if Exists(Path) then
    SearchDir(Path, Pattern);
  Result := ResultArray;
end;

class function TDirectoryUtils.GetCurrentDirectory: string;
begin
  Result := GetCurrentDir;
end;

class procedure TDirectoryUtils.SetCurrentDirectory(const Path: string);
begin
  SetCurrentDir(Path);
end;

class function TDirectoryUtils.GetParent(const Path: string): string;
begin
  Result := ExtractFilePath(ExcludeTrailingPathDelimiter(Path));
end;

class function TDirectoryUtils.IsEmpty(const Path: string): Boolean;
var
  SR: TSearchRec;
begin
  Result := True;
  if not Exists(Path) then Exit;
  
  if FindFirst(Path + PathDelim + '*.*', faAnyFile, SR) = 0 then
  begin
    repeat
      if (SR.Name <> '.') and (SR.Name <> '..') then
      begin
        Result := False;
        Break;
      end;
    until FindNext(SR) <> 0;
    FindClose(SR);
  end;
end;

class function TDirectoryUtils.GetHomeDirectory: string;
begin
  Result := GetCurrentDir;
end;

class function TDirectoryUtils.GetApplicationDirectory: string;
begin
  Result := ExtractFilePath(ParamStr(0));
end;

{==============================================================================}
{ TFileFilter Implementation }
{==============================================================================}

class function TFileFilter.MatchesPattern(const FileName, Pattern: string): Boolean;
var
  P, F: Integer;
  PatLen, FileLen: Integer;
  
  function MatchPattern(PatPos, FilePos: Integer): Boolean;
  begin
    while PatPos <= PatLen do
    begin
      case Pattern[PatPos] of
        '*':
          begin
            Inc(PatPos);
            if PatPos > PatLen then
            begin
              Result := True;
              Exit;
            end;
            while FilePos <= FileLen do
            begin
              if MatchPattern(PatPos, FilePos) then
              begin
                Result := True;
                Exit;
              end;
              Inc(FilePos);
            end;
            Result := False;
            Exit;
          end;
        '?':
          begin
            if FilePos > FileLen then
            begin
              Result := False;
              Exit;
            end;
            Inc(PatPos);
            Inc(FilePos);
          end;
      else
        if (FilePos > FileLen) or (LowerCase(FileName[FilePos]) <> LowerCase(Pattern[PatPos])) then
        begin
          Result := False;
          Exit;
        end;
        Inc(PatPos);
        Inc(FilePos);
      end;
    end;
    Result := FilePos > FileLen;
  end;
  
begin
  PatLen := Length(Pattern);
  FileLen := Length(FileName);
  Result := MatchPattern(1, 1);
end;

class function TFileFilter.MatchesPatterns(const FileName: string; const Patterns: array of string): Boolean;
var
  I: Integer;
begin
  Result := False;
  for I := 0 to High(Patterns) do
    if MatchesPattern(FileName, Patterns[I]) then
    begin
      Result := True;
      Break;
    end;
end;

class function TFileFilter.IsTextFile(const FileName: string): Boolean;
const
  TextExts: array[0..9] of string = ('txt', 'md', 'csv', 'json', 'xml', 'html', 'htm', 'css', 'js', 'pas');
var
  Ext: string;
  I: Integer;
begin
  Ext := LowerCase(ExtractFileExt(FileName));
  if (Ext <> '') and (Ext[1] = '.') then
    Ext := Copy(Ext, 2, Length(Ext) - 1);
  Result := False;
  for I := 0 to High(TextExts) do
    if TextExts[I] = Ext then
    begin
      Result := True;
      Break;
    end;
end;

class function TFileFilter.IsImageFile(const FileName: string): Boolean;
const
  ImageExts: array[0..7] of string = ('jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp', 'ico');
var
  Ext: string;
  I: Integer;
begin
  Ext := LowerCase(ExtractFileExt(FileName));
  if (Ext <> '') and (Ext[1] = '.') then
    Ext := Copy(Ext, 2, Length(Ext) - 1);
  Result := False;
  for I := 0 to High(ImageExts) do
    if ImageExts[I] = Ext then
    begin
      Result := True;
      Break;
    end;
end;

class function TFileFilter.IsAudioFile(const FileName: string): Boolean;
const
  AudioExts: array[0..7] of string = ('mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a', 'wma', 'opus');
var
  Ext: string;
  I: Integer;
begin
  Ext := LowerCase(ExtractFileExt(FileName));
  if (Ext <> '') and (Ext[1] = '.') then
    Ext := Copy(Ext, 2, Length(Ext) - 1);
  Result := False;
  for I := 0 to High(AudioExts) do
    if AudioExts[I] = Ext then
    begin
      Result := True;
      Break;
    end;
end;

class function TFileFilter.IsVideoFile(const FileName: string): Boolean;
const
  VideoExts: array[0..7] of string = ('mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'm4v');
var
  Ext: string;
  I: Integer;
begin
  Ext := LowerCase(ExtractFileExt(FileName));
  if (Ext <> '') and (Ext[1] = '.') then
    Ext := Copy(Ext, 2, Length(Ext) - 1);
  Result := False;
  for I := 0 to High(VideoExts) do
    if VideoExts[I] = Ext then
    begin
      Result := True;
      Break;
    end;
end;

class function TFileFilter.IsArchiveFile(const FileName: string): Boolean;
const
  ArchiveExts: array[0..7] of string = ('zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'xz', 'lz4');
var
  Ext: string;
  I: Integer;
begin
  Ext := LowerCase(ExtractFileExt(FileName));
  if (Ext <> '') and (Ext[1] = '.') then
    Ext := Copy(Ext, 2, Length(Ext) - 1);
  Result := False;
  for I := 0 to High(ArchiveExts) do
    if ArchiveExts[I] = Ext then
    begin
      Result := True;
      Break;
    end;
end;

end.
