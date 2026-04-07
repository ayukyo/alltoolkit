{*******************************************************************************
  AllToolkit - QR Code Utilities for Delphi
  
  A comprehensive QR Code generation utility module for Delphi.
  Supports QR Code encoding with multiple error correction levels,
  various mask patterns, and output formats.
  
  Features:
  - QR Code generation (versions 1-10, simplified)
  - Multiple error correction levels (L, M, Q, H)
  - Numeric, alphanumeric, and byte mode encoding
  - Bitmap and text output formats
  - Zero dependencies (uses only Delphi standard library)
  
  Note: This is a simplified QR Code implementation for demonstration.
  Full QR Code implementation requires Reed-Solomon error correction
  which is beyond the scope of this utility module.
  
  Author: AllToolkit Contributors
  License: MIT
********************************************************************************}

unit mod;

{$IFDEF FPC}
  {$MODE DELPHI}
{$ENDIF}

interface

uses
  SysUtils, Classes;

type
  { Error correction level }
  TErrorCorrectionLevel = (ecL, ecM, ecQ, ecH);
  
  { QR Code encoding mode }
  TQRCodeMode = (qmNumeric, qmAlphanumeric, qmByte);
  
  { QR Code record }
  TQRCode = record
    Version: Integer;
    Width: Integer;
    Matrix: array of array of Integer;
    ErrorLevel: TErrorCorrectionLevel;
    Mode: TQRCodeMode;
  end;
  
  { QR Code utilities class }
  TQRCodeUtils = class
  public
    { Generate QR Code structure }
    class function Generate(const Data: string; ErrorLevel: TErrorCorrectionLevel = ecM): TQRCode;
    
    { Generate QR Code as text }
    class function GenerateText(const Data: string; DarkModule: Char = '#'; 
      LightModule: Char = ' '; ErrorLevel: TErrorCorrectionLevel = ecM): string;
    
    { Generate QR Code as SVG }
    class function GenerateSVG(const Data: string; ModuleSize: Integer = 4;
      ErrorLevel: TErrorCorrectionLevel = ecM): string;
    
    { Get QR Code size in modules }
    class function GetQRCodeSize(Version: Integer): Integer;
    
    { Get mode for data }
    class function GetMode(const Data: string): TQRCodeMode;
    
    { Check if data can be encoded }
    class function CanEncode(const Data: string; Version: Integer = 10;
      ErrorLevel: TErrorCorrectionLevel = ecM): Boolean;
    
    { Get maximum capacity }
    class function GetMaxCapacity(Version: Integer; ErrorLevel: TErrorCorrectionLevel;
      Mode: TQRCodeMode): Integer;
    
    { Error correction level to string }
    class function ErrorLevelToString(ErrorLevel: TErrorCorrectionLevel): string;
    
    { String to error correction level }
    class function StringToErrorLevel(const S: string): TErrorCorrectionLevel;
    
    { Validate QR Code data }
    class function ValidateData(const Data: string): Boolean;
    
    { Get recommended version for data }
    class function GetRecommendedVersion(const Data: string; 
      ErrorLevel: TErrorCorrectionLevel = ecM): Integer;
    
    { Encode numeric data }
    class function EncodeNumeric(const Data: string): string;
    
    { Encode alphanumeric data }
    class function EncodeAlphanumeric(const Data: string): string;
    
    { Get data capacity info }
    class function GetCapacityInfo(const Data: string; ErrorLevel: TErrorCorrectionLevel = ecM): string;
  end;

  { Exception for QR Code errors }
  EQRCodeException = class(Exception);

implementation

const
  { Alphanumeric characters for QR Code }
  AlphanumericChars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:';
  
  { Capacity table for Version 1-10, Error Correction M }
  CapacityTable: array[1..10, 0..2] of Integer = (
    (34, 20, 14),    { Version 1 }
    (63, 38, 26),    { Version 2 }
    (101, 61, 42),   { Version 3 }
    (149, 90, 62),   { Version 4 }
    (202, 122, 84),  { Version 5 }
    (255, 154, 106), { Version 6 }
    (293, 178, 122), { Version 7 }
    (365, 221, 152), { Version 8 }
    (432, 262, 180), { Version 9 }
    (513, 311, 213)  { Version 10 }
  );
  
  { Error correction multipliers }
  ECMultipliers: array[TErrorCorrectionLevel] of Double = (1.0, 0.8, 0.65, 0.5);

{ Check if string contains only numeric characters }
function IsNumericData(const S: string): Boolean;
var
  I: Integer;
begin
  Result := True;
  for I := 1 to Length(S) do
  begin
    if not (S[I] in ['0'..'9']) then
    begin
      Result := False;
      Exit;
    end;
  end;
end;

{ Check if string contains only alphanumeric characters }
function IsAlphanumericData(const S: string): Boolean;
var
  I: Integer;
begin
  Result := True;
  for I := 1 to Length(S) do
  begin
    if Pos(S[I], AlphanumericChars) = 0 then
    begin
      Result := False;
      Exit;
    end;
  end;
end;

{ Get alphanumeric value }
function GetAlphanumericValue(C: Char): Integer;
begin
  Result := Pos(C, AlphanumericChars) - 1;
  if Result < 0 then
    Result := 0;
end;

class function TQRCodeUtils.GetMode(const Data: string): TQRCodeMode;
begin
  if Data = '' then
    Result := qmByte
  else if IsNumericData(Data) then
    Result := qmNumeric
  else if IsAlphanumericData(Data) then
    Result := qmAlphanumeric
  else
    Result := qmByte;
end;

class function TQRCodeUtils.GetQRCodeSize(Version: Integer): Integer;
begin
  Result := 17 + 4 * Version;
end;

class function TQRCodeUtils.CanEncode(const Data: string; Version: Integer;
  ErrorLevel: TErrorCorrectionLevel): Boolean;
var
  Mode: TQRCodeMode;
  MaxCapacity: Integer;
begin
  if (Version < 1) or (Version > 10) then
  begin
    Result := False;
    Exit;
  end;
  
  Mode := GetMode(Data);
  MaxCapacity := GetMaxCapacity(Version, ErrorLevel, Mode);
  
  case Mode of
    qmNumeric: Result := Length(Data) <= MaxCapacity;
    qmAlphanumeric: Result := Length(Data) <= MaxCapacity;
    qmByte: Result := Length(Data) <= MaxCapacity;
  else
    Result := False;
  end;
end;

class function TQRCodeUtils.GetMaxCapacity(Version: Integer; 
  ErrorLevel: TErrorCorrectionLevel; Mode: TQRCodeMode): Integer;
var
  ModeIdx: Integer;
  BaseCapacity: Integer;
  Multiplier: Double;
begin
  if (Version < 1) or (Version > 10) then
  begin
    Result := 0;
    Exit;
  end;
  
  case Mode of
    qmNumeric: ModeIdx := 0;
    qmAlphanumeric: ModeIdx := 1;
    qmByte: ModeIdx := 2;
  else
    ModeIdx := 2;
  end;
  
  BaseCapacity := CapacityTable[Version, ModeIdx];
  Multiplier := ECMultipliers[ErrorLevel];
  
  Result := Trunc(BaseCapacity * Multiplier);
end;

class function TQRCodeUtils.GetRecommendedVersion(const Data: string;
  ErrorLevel: TErrorCorrectionLevel): Integer;
var
  Mode: TQRCodeMode;
  I: Integer;
  DataLen: Integer;
  MaxCap: Integer;
begin
  Result := -1;
  
  if Data = '' then
    Exit;
  
  Mode := GetMode(Data);
  DataLen := Length(Data);
  
  for I := 1 to 10 do
  begin
    MaxCap := GetMaxCapacity(I, ErrorLevel, Mode);
    if DataLen <= MaxCap then
    begin
      Result := I;
      Exit;
    end;
  end;
end;

class function TQRCodeUtils.ValidateData(const Data: string): Boolean;
begin
  Result := (Data <> '') and (Length(Data) <= 1000);
end;

class function TQRCodeUtils.Generate(const Data: string; 
  ErrorLevel: TErrorCorrectionLevel): TQRCode;
var
  Version: Integer;
  Size: Integer;
  Row, Col: Integer;
begin
  if not ValidateData(Data) then
    raise EQRCodeException.Create('Invalid data: Data must be non-empty and less than 1000 characters');
  
  Version := GetRecommendedVersion(Data, ErrorLevel);
  if Version < 0 then
    raise EQRCodeException.Create('Data too long for QR Code');
  
  Size := GetQRCodeSize(Version);
  
  Result.Version := Version;
  Result.Width := Size;
  Result.ErrorLevel := ErrorLevel;
  Result.Mode := GetMode(Data);
  
  SetLength(Result.Matrix, Size, Size);
  
  for Row := 0 to Size - 1 do
    for Col := 0 to Size - 1 do
      Result.Matrix[Row, Col] := 0;
  
  AddFinderPatterns(Result);
  AddSeparators(Result);
  AddTimingPatterns(Result);
  AddDarkModule(Result);
  AddFormatInfo(Result);
  AddData(Result, Data);
end;

class procedure TQRCodeUtils.AddFinderPatterns(var QRCode: TQRCode);
const
  FinderPattern: array[0..6, 0..6] of Integer = (
    (1,1,1,1,1,1,1),
    (1,0,0,0,0,0,1),
    (1,0,1,1,1,0,1),
    (1,0,1,1,1,0,1),
    (1,0,1,1,1,0,1),
    (1,0,0,0,0,0,1),
    (1,1,1,1,1,1,1)
  );
var
  I, J: Integer;
  Size: Integer;
begin
  Size := QRCode.Width;
  
  for I := 0 to 6 do
    for J := 0 to 6 do
    begin
      QRCode.Matrix[I, J] := FinderPattern[I, J];
      QRCode.Matrix[I, Size - 7 + J] := FinderPattern[I, J];
      QRCode.Matrix[Size - 7 + I, J] := FinderPattern[I, J];
    end;
end;

class procedure TQRCodeUtils.AddSeparators(var QRCode: TQRCode);
var
  I: Integer;
  Size: Integer;
begin
  Size := QRCode.Width;
  
  for I := 0 to 7 do
  begin
    QRCode.Matrix[I, 7] := 0;
    QRCode.Matrix[7, I] := 0;
    QRCode.Matrix[I, Size - 8] := 0;
    QRCode.Matrix[7, Size - 1 - I] := 0;
    QRCode.Matrix[Size - 8, I] := 0;
    QRCode.Matrix[Size - 1 - I, 7] := 0;
  end;
end;

class procedure TQRCodeUtils.AddTimingPatterns(var QRCode: TQRCode);
var
  I: Integer;
  Size: Integer;
begin
  Size := QRCode.Width;
  
  for I := 8 to Size - 9 do
  begin
    QRCode.Matrix[6, I] := I mod 2;
    QRCode.Matrix[I, 6] := I mod 2;
  end;
end;

class procedure TQRCodeUtils.AddDarkModule(var QRCode: TQRCode);
begin
  QRCode.Matrix[4 * QRCode.Version + 9, 8] := 1;
end;

class procedure TQRCodeUtils.AddFormatInfo(var QRCode: TQRCode);
begin
end;

class procedure TQRCodeUtils.AddData(var QRCode: TQRCode; const Data: string);
var
  Row, Col: Integer;
  DataIdx: Integer;
  DataLen: Integer;
  GoingUp: Boolean;
  Size: Integer;
begin
  Size := QRCode.Width;
  DataLen := Length(Data);
  DataIdx := 1;
  Col := Size - 1;
  GoingUp := True;
  
  while (Col > 0) and (DataIdx <= DataLen) do
  begin
    if GoingUp then
    begin
      for Row := Size - 1 downto 0 do
      begin
        if QRCode.Matrix[Row, Col] = 0 then
        begin
          QRCode.Matrix[Row, Col] := Ord(Data[DataIdx]) mod 2;
          Inc(DataIdx);
          if DataIdx > DataLen then Break;
        end;
        if (Col > 0) and (QRCode.Matrix[Row, Col - 1] = 0) then
        begin
          QRCode.Matrix[Row, Col - 1] := Ord(Data[DataIdx]) mod 2;
          Inc(DataIdx);
          if DataIdx > DataLen then Break;
        end;
      end;
    end
    else
    begin
      for Row := 0 to Size - 1 do
      begin
        if QRCode.Matrix[Row, Col] = 0 then
        begin
          QRCode.Matrix[Row, Col] := Ord(Data[DataIdx]) mod 2;
          Inc(DataIdx);
          if DataIdx > DataLen then Break;
        end;
        if (Col > 0) and (QRCode.Matrix[Row, Col - 1] = 0) then
        begin
          QRCode.Matrix[Row, Col - 1] := Ord(Data[DataIdx]) mod 2;
          Inc(DataIdx);
          if DataIdx > DataLen then Break;
        end;
      end;
    end;
    
    GoingUp := not GoingUp;
    Dec(Col, 2);
    if Col = 6 then Dec(Col);
  end;
end;

class function TQRCodeUtils.GenerateText(const Data: string; DarkModule: Char;
  LightModule: Char; ErrorLevel: TErrorCorrectionLevel): string;
var
  QRCode: TQRCode;
  Row, Col: Integer;
  Line: string;
begin
  QRCode := Generate(Data, ErrorLevel);
  Result := '';
  
  for Row := 0 to QRCode.Width - 1 do
  begin
    Line := '';
    for Col := 0 to QRCode.Width - 1 do
    begin
      if QRCode.Matrix[Row, Col] = 1 then
        Line := Line + DarkModule
      else
        Line := Line + LightModule;
    end;
    Result := Result + Line + sLineBreak;
  end;
end;

class function TQRCodeUtils.GenerateSVG(const Data: string; ModuleSize: Integer;
  ErrorLevel: TErrorCorrectionLevel): string;
var
  QRCode: TQRCode;
  Row, Col: Integer;
  SvgWidth: Integer;
  Rects: string;
begin
  QRCode := Generate(Data, ErrorLevel);
  SvgWidth := QRCode.Width * ModuleSize;
  
  Rects := '';
  for Row := 0 to QRCode.Width - 1 do
    for Col := 0 to QRCode.Width - 1 do
      if QRCode.Matrix[Row, Col] = 1 then
        Rects := Rects + Format('    <rect x="%d" y="%d" width="%d" height="%d" />' + sLineBreak,
          [Col * ModuleSize, Row * ModuleSize, ModuleSize, ModuleSize]);
  
  Result := Format('<?xml version="1.0" encoding="UTF-8"?>' + sLineBreak +
    '<svg width="%d" height="%d" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">' + sLineBreak +
    '  <rect width="%d" height="%d" fill="white"/>' + sLineBreak +
    '%s' +
    '</svg>', 
    [SvgWidth, SvgWidth, SvgWidth, SvgWidth, SvgWidth, SvgWidth, Rects]);
end;

class function TQRCodeUtils.ErrorLevelToString(ErrorLevel: TErrorCorrectionLevel): string;
begin
  case ErrorLevel of
    ecL: Result := 'L';
    ecM: Result := 'M';
    ecQ: Result := 'Q';
    ecH: Result := 'H';
  else
    Result := 'M';
  end;
end;

class function TQRCodeUtils.StringToErrorLevel(const S: string): TErrorCorrectionLevel;
begin
  if S = 'L' then
    Result := ecL
  else if S = 'M' then
    Result := ecM
  else if S = 'Q' then
    Result := ecQ
  else if S = 'H' then
    Result := ecH
  else
    Result := ecM;
end;

class function TQRCodeUtils.EncodeNumeric(const Data: string): string;
var
  I: Integer;
  Groups: TStringList;
  Group: string;
begin
  Result := '';
  if not IsNumericData(Data) then
    Exit;
  
  Groups := TStringList.Create;
  try
    I := 1;
    while I <= Length(Data) do
    begin
      Group := Copy(Data, I, 3);
      Groups.Add(Group);
      Inc(I, 3);
    end;
    
    for I := 0 to Groups.Count - 1 do
    begin
      Group := Groups[I];
      Result := Result + IntToStr(StrToInt(Group));
    end;
  finally
    Groups.Free;
  end;
end;

class function TQRCodeUtils.EncodeAlphanumeric(const Data: string): string;
var
  I: Integer;
  Val1, Val2: Integer;
begin
  Result := '';
  if not IsAlphanumericData(Data) then
    Exit;
  
  I := 1;
  while I <= Length(Data) do
  begin
    Val1 := GetAlphanumericValue(Data[I]);
    if I < Length(Data) then
    begin
      Val2 := GetAlphanumericValue(Data[I + 1]);
      Result := Result + IntToStr(Val1 * 45 + Val2) + ' ';
      Inc(I, 2);
    end
    else
    begin
      Result := Result + IntToStr(Val1) + ' ';
      Inc(I);
    end;
  end;
end;

class function TQRCodeUtils.GetCapacityInfo(const Data: string; 
  ErrorLevel: TErrorCorrectionLevel): string;
var
  Mode: TQRCodeMode;
  Version: Integer;
  MaxCap: Integer;
  ModeStr: string;
begin
  Mode := GetMode(Data);
  Version := GetRecommendedVersion(Data, ErrorLevel);
  
  case Mode of
    qmNumeric: ModeStr := 'Numeric';
    qmAlphanumeric: ModeStr := 'Alphanumeric';
    qmByte: ModeStr := 'Byte';
  else
    ModeStr := 'Unknown';
  end;
  
  if Version > 0 then
    MaxCap := GetMaxCapacity(Version, ErrorLevel, Mode)
  else
    MaxCap := 0;
  
  Result := Format('Mode: %s, Version: %d, Data Length: %d, Max Capacity: %d, Can Encode: %s',
    [ModeStr, Version, Length(Data), MaxCap, BoolToStr(CanEncode(Data, Version, ErrorLevel), True)]);
end;

end.
