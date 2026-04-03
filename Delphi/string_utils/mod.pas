{*******************************************************************************
  AllToolkit - Delphi String Utilities
  
  一个零依赖的字符串处理工具库，适用于 Delphi 7+ 和 Free Pascal
  
  功能包括：
  - 空值检查与处理
  - 大小写转换
  - 子串操作
  - 空白字符处理
  - 字符串验证（邮箱、URL、数字等）
  - 命名风格转换（驼峰、蛇形、短横线等）
  - 随机字符串生成
  - 编码解码（Base64、URL编码）
  - 字符串填充与对齐
  
  作者：AllToolkit Contributors
  许可证：MIT
********************************************************************************}

unit mod;

interface

uses
  SysUtils, Classes;

const
  // 字符集常量
  LOWERCASE_CHARS = 'abcdefghijklmnopqrstuvwxyz';
  UPPERCASE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  DIGIT_CHARS = '0123456789';
  ALPHANUMERIC_CHARS = LOWERCASE_CHARS + UPPERCASE_CHARS + DIGIT_CHARS;
  SPECIAL_CHARS = '!@#$%^&*()-_=+[]{}|;:,.<>?';
  ALL_CHARS = ALPHANUMERIC_CHARS + SPECIAL_CHARS;
  HEX_CHARS = '0123456789ABCDEF';

{===============================================================================
  空值检查
===============================================================================}
function IsBlank(const S: string): Boolean;
function IsNotBlank(const S: string): Boolean;
function IsEmpty(const S: string): Boolean;

{===============================================================================
  空白字符处理
===============================================================================}
function TrimString(const S: string): string;
function TrimLeft(const S: string): string;
function TrimRight(const S: string): string;
function RemoveWhitespace(const S: string): string;
function NormalizeWhitespace(const S: string): string;

{===============================================================================
  大小写转换
===============================================================================}
function ToLower(const S: string): string;
function ToUpper(const S: string): string;
function Capitalize(const S: string): string;
function Uncapitalize(const S: string): string;
function ToTitleCase(const S: string): string;
function SwapCase(const S: string): string;

{===============================================================================
  子串操作
===============================================================================}
function Substring(const S: string; Start: Integer; Len: Integer = 0): string;
function SubstringFrom(const S: string; Start: Integer): string;
function SubstringTo(const S: string; EndPos: Integer): string;
function SubstringBetween(const S, Open, Close: string): string;
function SubstringAfter(const S, Separator: string): string;
function SubstringBefore(const S, Separator: string): string;
function SubstringAfterLast(const S, Separator: string): string;
function SubstringBeforeLast(const S, Separator: string): string;
function Truncate(const S: string; MaxLength: Integer; const Suffix: string = '...'): string;

{===============================================================================
  前缀后缀操作
===============================================================================}
function StartsWith(const S, Prefix: string; IgnoreCase: Boolean = False): Boolean;
function EndsWith(const S, Suffix: string; IgnoreCase: Boolean = False): Boolean;
function RemovePrefix(const S, Prefix: string): string;
function RemoveSuffix(const S, Suffix: string): string;

{===============================================================================
  查找与计数
===============================================================================}
function CountMatches(const S, Sub: string; IgnoreCase: Boolean = False): Integer;
function Contains(const S, Sub: string; IgnoreCase: Boolean = False): Boolean;
function IndexOf(const S, Sub: string; StartPos: Integer = 1): Integer;
function LastIndexOf(const S, Sub: string): Integer;

{===============================================================================
  替换操作
===============================================================================}
function ReplaceAll(const S, OldSub, NewSub: string; IgnoreCase: Boolean = False): string;
function ReplaceFirst(const S, OldSub, NewSub: string): string;
function ReplaceLast(const S, OldSub, NewSub: string): string;

{===============================================================================
  填充与对齐
===============================================================================}
function PadLeft(const S: string; TotalWidth: Integer; PadChar: Char = ' '): string;
function PadRight(const S: string; TotalWidth: Integer; PadChar: Char = ' '): string;
function Center(const S: string; TotalWidth: Integer; PadChar: Char = ' '): string;

{===============================================================================
  反转与重复
===============================================================================}
function Reverse(const S: string): string;
function RepeatString(const S: string; Count: Integer): string;

{===============================================================================
  分割与连接
===============================================================================}
function Split(const S: string; const Delimiter: string; Limit: Integer = 0): TStringList;
function SplitLines(const S: string): TStringList;
function Join(const Strings: TStringList; const Delimiter: string): string;

{===============================================================================
  命名风格转换
===============================================================================}
function ToCamelCase(const S: string): string;
function ToPascalCase(const S: string): string;
function ToSnakeCase(const S: string): string;
function ToKebabCase(const S: string): string;

{===============================================================================
  验证函数
===============================================================================}
function IsValidEmail(const S: string): Boolean;
function IsValidUrl(const S: string): Boolean;
function IsNumeric(const S: string): Boolean;
function IsInteger(const S: string): Boolean;
function IsAlpha(const S: string): Boolean;
function IsAlphanumeric(const S: string): Boolean;

{===============================================================================
  随机生成
===============================================================================}
function RandomString(Length: Integer; const Chars: string = ALPHANUMERIC_CHARS): string;
function RandomAlphanumeric(Length: Integer): string;
function RandomNumeric(Length: Integer): string;
function RandomPassword(Length: Integer): string;

{===============================================================================
  编码解码
===============================================================================}
function Base64Encode(const S: string): string;
function Base64Decode(const S: string): string;
function UrlEncode(const S: string): string;
function UrlDecode(const S: string): string;
function HtmlEscape(const S: string): string;
function HtmlUnescape(const S: string): string;

{===============================================================================
  其他工具
===============================================================================}
function DefaultIfBlank(const S, DefaultValue: string): string;
function DefaultIfEmpty(const S, DefaultValue: string): string;
function Slugify(const S: string; const Separator: string = '-'): string;
function StripHtml(const S: string): string;

implementation

{===============================================================================
  空值检查
===============================================================================}

function IsBlank(const S: string): Boolean;
var
  I: Integer;
begin
  if S = '' then
  begin
    Result := True;
    Exit;
  end;
  for I := 1 to Length(S) do
    if not (S[I] in [' ', #9, #10, #13, #0]) then
    begin
      Result := False;
      Exit;
    end;
  Result := True;
end;

function IsNotBlank(const S: string): Boolean;
begin
  Result := not IsBlank(S);
end;

function IsEmpty(const S: string): Boolean;
begin
  Result := S = '';
end;

{===============================================================================
  空白字符处理
===============================================================================}

function TrimString(const S: string): string;
begin
  Result := Trim(S);
end;

function TrimLeft(const S: string): string;
var
  I: Integer;
begin
  I := 1;
  while (I <= Length(S)) and (S[I] in [' ', #9, #10, #13]) do
    Inc(I);
  Result := Copy(S, I, MaxInt);
end;

function TrimRight(const S: string): string;
var
  I: Integer;
begin
  I := Length(S);
  while (I > 0) and (S[I] in [' ', #9, #10, #13]) do
    Dec(I);
  Result := Copy(S, 1, I);
end;

function RemoveWhitespace(const S: string): string;
var
  I: Integer;
  SB: string;
begin
  SB := '';
  for I := 1 to Length(S) do
    if not (S[I] in [' ', #9, #10, #13, #0]) then
      SB := SB + S[I];
  Result := SB;
end;

function NormalizeWhitespace(const S: string): string;
var
  I: Integer;
  SB: string;
  InSpace: Boolean;
begin
  SB := '';
  InSpace := False;
  for I := 1 to Length(S) do
  begin
    if S[I] in [' ', #9, #10, #13] then
    begin
      if not InSpace and (SB <> '') then
      begin
        SB := SB + ' ';
        InSpace := True;
      end;
    end
    else
    begin
      SB := SB + S[I];
      InSpace := False;
    end;
  end;
  if (SB <> '') and (SB[Length(SB)] = ' ') then
    SB := Copy(SB, 1, Length(SB) - 1);
  Result := SB;
end;

{===============================================================================
  大小写转换
===============================================================================}

function ToLower(const S: string): string;
begin
  Result := AnsiLowerCase(S);
end;

function ToUpper(const S: string): string;
begin
  Result := AnsiUpperCase(S);
end;

function Capitalize(const S: string): string;
begin
  if S = '' then
    Result := ''
  else
    Result := AnsiUpperCase(S[1]) + Copy(S, 2, MaxInt);
end;

function Uncapitalize(const S: string): string;
begin
  if S = '' then
    Result := ''
  else
    Result := AnsiLowerCase(S[1]) + Copy(S, 2, MaxInt);
end;

function ToTitleCase(const S: string): string;
var
  I: Integer;
  InWord: Boolean;
  SB: string;
begin
  SB := '';
  InWord := False;
  for I := 1 to Length(S) do
  begin
    if S[I] in [' ', #9, #10, #13, '_', '-'] then
    begin
      InWord := False;
      SB := SB + S[I];
    end
    else
    begin
      if InWord then
        SB := SB + AnsiLowerCase(S[I])
      else
        SB := SB + AnsiUpperCase(S[I]);
      InWord := True;
    end;
  end;
  Result := SB;
end;

function SwapCase(const S: string): string;
var
  I: Integer;
  SB: string;
begin
  SB := '';
  for I := 1 to Length(S) do
  begin
    if S[I] in ['a'..'z'] then
      SB := SB + AnsiUpperCase(S[I])
    else if S[I] in ['A'..'Z'] then
      SB := SB + AnsiLowerCase(S[I])
    else
      SB := SB + S[I];
  end;
  Result := SB;
end;

{===============================================================================
  子串操作
===============================================================================}

function Substring(const S: string; Start: Integer; Len: Integer = 0): string;
begin
  if Start < 1 then
    Start := 1;
  if Len <= 0 then
    Result := Copy(S, Start, MaxInt)
  else
    Result := Copy(S, Start, Len);
end;

function SubstringFrom(const S: string; Start: Integer): string;
begin
  Result := Substring(S, Start, 0);
end;

function SubstringTo(const S: string; EndPos: Integer): string;
begin
  if EndPos < 1 then
    Result := ''
  else
    Result := Copy(S, 1, EndPos);
end;

function SubstringBetween(const S, Open, Close: string): string;
var
  StartPos, EndPos: Integer;
begin
  StartPos := Pos(Open, S);
  if StartPos = 0 then
  begin
    Result := '';
    Exit;
  end;
  StartPos := StartPos + Length(Open);
  EndPos := Pos(Close, Copy(S, StartPos, MaxInt));
  if EndPos = 0 then
  begin
    Result := '';
    Exit;
  end;
  Result := Copy(S, StartPos, EndPos - 1);
end;

function SubstringAfter(const S, Separator: string): string;
var
  PosSep: Integer;
begin
  PosSep := Pos(Separator, S);
  if PosSep = 0 then
    Result := S
  else
    Result := Copy(S, PosSep + Length(Separator), MaxInt);
end;

function SubstringBefore(const S, Separator: string): string;
var
  PosSep: Integer;
begin
  PosSep := Pos(Separator, S);
  if PosSep = 0 then
    Result := S
  else
    Result := Copy(S, 1, PosSep - 1);
end;

function SubstringAfterLast(const S, Separator: string): string;
var
  LastPos: Integer;
  I: Integer;
begin
  LastPos := 0;
  for I := 1 to Length(S) - Length(Separator) + 1 do
    if Copy(S, I, Length(Separator)) = Separator then
      LastPos := I;
  if LastPos = 0 then
    Result := S
  else
    Result := Copy(S, LastPos + Length(Separator), MaxInt);
end;

function SubstringBeforeLast(const S, Separator: string): string;
var
  LastPos: Integer;
  I: Integer;
begin
  LastPos := 0;
  for I := 1 to Length(S) - Length(Separator) + 1 do
    if Copy(S, I, Length(Separator)) = Separator then
      LastPos := I;
  if LastPos = 0 then
    Result := S
  else
    Result := Copy(S, 1, LastPos - 1);
end;

function Truncate(const S: string; MaxLength: Integer; const Suffix: string = '...'): string;
begin
  if Length(S) <= MaxLength then
    Result := S
  else
    Result := Copy(S, 1, MaxLength - Length(Suffix)) + Suffix;
end;

{===============================================================================
  前缀后缀操作
===============================================================================}

function StartsWith(const S, Prefix: string; IgnoreCase: Boolean = False): Boolean;
var
  Sub: string;
begin
  if Length(Prefix) > Length(S) then
  begin
    Result := False;
    Exit;
  end;
  Sub := Copy(S, 1, Length(Prefix));
  if IgnoreCase then
    Result := AnsiSameText(Sub, Prefix)
  else
    Result := Sub = Prefix;
end;

function EndsWith(const S, Suffix: string; IgnoreCase: Boolean = False): Boolean;
var
  Sub: string;
begin
  if Length(Suffix) > Length(S) then
  begin
    Result := False;
    Exit;
  end;
  Sub := Copy(S, Length(S) - Length(Suffix) + 1, Length(Suffix));
  if IgnoreCase then
    Result := AnsiSameText(Sub, Suffix)
  else
    Result := Sub = Suffix;
end;

function RemovePrefix(const S, Prefix: string): string;
begin
  if StartsWith(S, Prefix, False) then
    Result := Copy(S, Length(Prefix) + 1, MaxInt)
  else
    Result := S;
end;

function RemoveSuffix(const S, Suffix: string): string;
begin
  if EndsWith(S, Suffix, False) then
    Result := Copy(S, 1, Length(S) - Length(Suffix))
  else
    Result := S;
end;

{===============================================================================
  查找与计数
===============================================================================}

function CountMatches(const S, Sub: string; IgnoreCase: Boolean = False): Integer;
var
  Count, PosIdx: Integer;
  SearchS, SearchSub: string;
begin
  if Sub = '' then
  begin
    Result := 0;
    Exit;
  end;
  if IgnoreCase then
  begin
    SearchS := AnsiLowerCase(S);
    SearchSub := AnsiLowerCase(Sub);
  end
  else
  begin
    SearchS := S;
    SearchSub := Sub;
  end;
  Count := 0;
  PosIdx := 1;
  while PosIdx <= Length(SearchS) do
  begin
    PosIdx := Pos(SearchSub, Copy(SearchS, PosIdx, MaxInt));
    if PosIdx = 0 then
      Break;
    Inc(Count);
    PosIdx := PosIdx + Length(SearchSub);
  end;
  Result := Count;
end;

function Contains(const S, Sub: string; IgnoreCase: Boolean = False): Boolean;
begin
  if IgnoreCase then
    Result := Pos(AnsiLowerCase(Sub), AnsiLowerCase(S)) > 0
  else
    Result := Pos(Sub, S) > 0;
end;

function IndexOf(const S, Sub: string; StartPos: Integer = 1): Integer;
var
  P: Integer;
begin
  if (StartPos < 1) or (StartPos > Length(S)) then
  begin
    Result := 0;
    Exit;
  end;
  P := Pos(Sub, Copy(S, StartPos, MaxInt));
  if P = 0 then
    Result := 0
  else
    Result := P + StartPos - 1;
end;

function LastIndexOf(const S, Sub: string): Integer;
var
  LastPos, P: Integer;
begin
  if Sub = '' then
  begin
    Result := 0;
    Exit;
  end;
  LastPos := 0;
  P := Pos(Sub, S);
  while P > 0 do
  begin
    LastPos := P;
    P := Pos(Sub, Copy(S, P + 1, MaxInt));
    if P > 0 then
      P := P + LastPos;
  end;
  Result := LastPos;
end;

{===============================================================================
  替换操作
===============================================================================}

function ReplaceAll(const S, OldSub, NewSub: string; IgnoreCase: Boolean = False): string;
var
  SearchS, SearchOld: string;
  P: Integer;
begin
  if IgnoreCase then
  begin
    SearchS := AnsiLowerCase(S);
    SearchOld := AnsiLowerCase(OldSub);
  end
  else
  begin
    SearchS := S;
    SearchOld := OldSub;
  end;
  Result := S;
  P := Pos(SearchOld, SearchS);
  while P > 0 do
  begin
    Delete(Result, P, Length(OldSub));
    Insert(NewSub, Result, P);
    SearchS := AnsiLowerCase(Result);
    P := Pos(SearchOld, Copy(SearchS, P + Length(NewSub), MaxInt));
    if P > 0 then
      P := P + P + Length(NewSub) - 1;
  end;
end;

function ReplaceFirst(const S, OldSub, NewSub: string): string;
var
  P: Integer;
begin
  Result := S;
  P := Pos(OldSub, Result);
  if P > 0 then
  begin
    Delete(Result, P, Length(OldSub));
    Insert(NewSub, Result, P);
  end;
end;

function ReplaceLast(const S, OldSub, NewSub: string): string;
var
  P: Integer;
begin
  Result := S;
  P := LastIndexOf(S, OldSub);
  if P > 0 then
  begin
    Delete(Result, P, Length(OldSub));
    Insert(NewSub, Result, P);
  end;
end;

{===============================================================================
  填充与对齐
===============================================================================}

function PadLeft(const S: string; TotalWidth: Integer; PadChar: Char = ' '): string;
var
  PadLen: Integer;
begin
  PadLen := TotalWidth - Length(S);
  if PadLen > 0 then
    Result := StringOfChar(PadChar, PadLen) + S
  else
    Result := S;
end;

function PadRight(const S: string; TotalWidth: Integer; PadChar: Char = ' '): string;
var
  PadLen: Integer;
begin
  PadLen := TotalWidth - Length(S);
  if PadLen > 0 then
    Result := S + StringOfChar(PadChar, PadLen)
  else
    Result := S;
end;

function Center(const S: string; TotalWidth: Integer; PadChar: Char = ' '): string;
var
  PadLen, LeftPad: Integer;
begin
  PadLen := TotalWidth - Length(S);
  if PadLen > 0 then
  begin
    LeftPad := PadLen div 2;
    Result := StringOfChar(PadChar, LeftPad) + S + StringOfChar(PadChar, PadLen - LeftPad);
  end
  else
    Result := S;
end;

{===============================================================================
  反转与重复
===============================================================================}

function Reverse(const S: string): string;
var
  I: Integer;
  SB: string;
begin
  SB := '';
  for I := Length(S) downto 1 do
    SB := SB + S[I];
  Result := SB;
end;

function RepeatString(const S: string; Count: Integer): string;
var
  SB: string;
  I: Integer;
begin
  if Count <= 0 then
  begin
    Result := '';
    Exit;
  end;
  SB := '';
  for I := 1 to Count do
    SB := SB + S;
  Result := SB;
end;

{===============================================================================
  分割与连接
===============================================================================}

function Split(const S: string; const Delimiter: string; Limit: Integer = 0): TStringList;
var
  List: TStringList;
  P, LastP: Integer;
  Sub: string;
  Count: Integer;
begin
  List := TStringList.Create;
  if S = '' then
  begin
    Result := List;
    Exit;
  end;
  if Delimiter = '' then
  begin
    List.Add(S);
    Result := List;
    Exit;
  end;
  Count := 0;
  LastP := 1;
  P := Pos(Delimiter, S);
  while (P > 0) and ((Limit = 0) or (Count < Limit - 1)) do
  begin
    Sub := Copy(S, LastP, P - LastP);
    List.Add(Sub);
    Inc(Count);
    LastP := P + Length(Delimiter);
    P := Pos(Delimiter, Copy(S, LastP, MaxInt));
    if P > 0 then
      P := P + LastP - 1;
  end;
  Sub := Copy(S, LastP, MaxInt);
  List.Add(Sub);
  Result := List;
end;

function SplitLines(const S: string): TStringList;
begin
  Result := Split(S, #10);
end;

function Join(const Strings: TStringList; const Delimiter: string): string;
var
  I: Integer;
  SB: string;
begin
  if Strings.Count = 0 then
  begin
    Result := '';
    Exit;
  end;
  SB := Strings[0];
  for I := 1 to Strings.Count - 1 do
    SB := SB + Delimiter + Strings[I];
  Result := SB;
end;

{===============================================================================
  命名风格转换
===============================================================================}

function ToCamelCase(const S: string): string;
var
  I: Integer;
  SB: string;
  NextUpper: Boolean;
begin
  SB := '';
  NextUpper := False;
  for I := 1 to Length(S) do
  begin
    if S[I] in ['_', '-', ' '] then
      NextUpper := True
    else if NextUpper then
    begin
      SB := SB + AnsiUpperCase(S[I]);
      NextUpper := False;
    end
    else
      SB := SB + AnsiLowerCase(S[I]);
  end;
  if SB <> '' then
    SB := AnsiLowerCase(SB[1]) + Copy(SB, 2, MaxInt);
  Result := SB;
end;

function ToPascalCase(const S: string): string;
var
  I: Integer;
  SB: string;
  NextUpper: Boolean;
begin
  SB := '';
  NextUpper := True;
  for I := 1 to Length(S) do
  begin
    if S[I] in ['_', '-', ' '] then
      NextUpper := True
    else if NextUpper then
    begin
      SB := SB + AnsiUpperCase(S[I]);
      NextUpper := False;
    end
    else
      SB := SB + AnsiLowerCase(S[I]);
  end;
  Result := SB;
end;

function ToSnakeCase(const S: string): string;
var
  I: Integer;
  SB: string;
  PrevLower: Boolean;
begin
  SB := '';
  PrevLower := False;
  for I := 1 to Length(S) do
  begin
    if S[I] in ['A'..'Z'] then
    begin
      if PrevLower then
        SB := SB + '_';
      SB := SB + AnsiLowerCase(S[I]);
      PrevLower := False;
    end
    else if S[I] in ['a'..'z', '0'..'9'] then
    begin
      SB := SB + S[I];
      PrevLower := True;
    end
    else if S[I] in ['-', ' '] then
    begin
      SB := SB + '_';
      PrevLower := False;
    end;
  end;
  Result := SB;
end;

function ToKebabCase(const S: string): string;
var
  I: Integer;
  SB: string;
  PrevLower: Boolean;
begin
  SB := '';
  PrevLower := False;
  for I := 1 to Length(S) do
  begin
    if S[I] in ['A'..'Z'] then
    begin
      if PrevLower then
        SB := SB + '-';
      SB := SB + AnsiLowerCase(S[I]);
      PrevLower := False;
    end
    else if S[I] in ['a'..'z', '0'..'9'] then
    begin
      SB := SB + S[I];
      PrevLower := True;
    end
    else if S[I] in ['_', ' '] then
    begin
      SB := SB + '-';
      PrevLower := False;
    end;
  end;
  Result := SB;
end;

{===============================================================================
  验证函数
===============================================================================}

function IsValidEmail(const S: string): Boolean;
var
  AtPos, DotPos: Integer;
begin
  AtPos := Pos('@', S);
  if AtPos < 2 then
  begin
    Result := False;
    Exit;
  end;
  DotPos := Pos('.', Copy(S, AtPos + 1, MaxInt));
  if DotPos < 2 then
  begin
    Result := False;
    Exit;
  end;
  Result := True;
end;

function IsValidUrl(const S: string): Boolean;
begin
  Result := StartsWith(S, 'http://', True) or StartsWith(S, 'https://', True);
end;

function IsNumeric(const S: string): Boolean;
var
  I: Integer;
  HasDot: Boolean;
begin
  if S = '' then
  begin
    Result := False;
    Exit;
  end;
  HasDot := False;
  for I := 1 to Length(S) do
  begin
    if S[I] = '.' then
    begin
      if HasDot then
      begin
        Result := False;
        Exit;
      end;
      HasDot := True;
    end
    else if not (S[I] in ['0'..'9', '-', '+']) then
    begin
      if not ((I = 1) and (S[I] in ['-', '+'])) then
      begin
        Result := False;
        Exit;
      end;
    end;
  end;
  Result := True;
end;

function IsInteger(const S: string): Boolean;
var
  I: Integer;
begin
  if S = '' then
  begin
    Result := False;
    Exit;
  end;
  for I := 1 to Length(S) do
  begin
    if not (S[I] in ['0'..'9', '-', '+']) then
    begin
      Result := False;
      Exit;
    end;
  end;
  Result := True;
end;

function IsAlpha(const S: string): Boolean;
var
  I: Integer;
begin
  if S = '' then
  begin
    Result := False;
    Exit;
  end;
  for I := 1 to Length(S) do
    if not (S[I] in ['a'..'z', 'A'..'Z']) then
    begin
      Result := False;
      Exit;
    end;
  Result := True;
end;

function IsAlphanumeric(const S: string): Boolean;
var
  I: Integer;
begin
  if S = '' then
  begin
    Result := False;
    Exit;
  end;
  for I := 1 to Length(S) do
    if not (S[I] in ['a'..'z', 'A'..'Z', '0'..'9']) then
    begin
      Result := False;
      Exit;
    end;
  Result := True;
end;

{===============================================================================
  随机生成
===============================================================================}

function RandomString(Length: Integer; const Chars: string = ALPHANUMERIC_CHARS): string;
var
  I: Integer;
  SB: string;
  CharSetLen: Integer;
begin
  if (Length <= 0) or (Chars = '') then
  begin
    Result := '';
    Exit;
  end;
  Randomize;
  SB := '';
  CharSetLen := Length(Chars);
  for I := 1 to Length do
    SB := SB + Chars[Random(CharSetLen) + 1];
  Result := SB;
end;

function RandomAlphanumeric(Length: Integer): string;
begin
  Result := RandomString(Length, ALPHANUMERIC_CHARS);
end;

function RandomNumeric(Length: Integer): string;
begin
  Result := RandomString(Length, DIGIT_CHARS);
end;

function RandomPassword(Length: Integer): string;
var
  SB: string;
  I: Integer;
begin
  if Length < 4 then
    Length := 4;
  SB := '';
  // Ensure at least one of each character type
  SB := SB + LOWERCASE_CHARS[Random(26) + 1];
  SB := SB + UPPERCASE_CHARS[Random(26) + 1];
  SB := SB + DIGIT_CHARS[Random(10) + 1];
  SB := SB + SPECIAL_CHARS[Random(Length(SPECIAL_CHARS)) + 1];
  // Fill remaining with random chars
  for I := 5 to Length do
    SB := SB + ALL_CHARS[Random(Length(ALL_CHARS)) + 1];
  // Shuffle the result
  Result := '';
  while SB <> '' do
  begin
    I := Random(Length(SB)) + 1;
    Result := Result + SB[I];
    Delete(SB, I, 1);
  end;
end;

{===============================================================================
  编码解码
===============================================================================}

function Base64Encode(const S: string): string;
const
  BASE64_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
var
  I: Integer;
  B1, B2, B3: Byte;
  SB: string;
  Len: Integer;
begin
  if S = '' then
  begin
    Result := '';
    Exit;
  end;
  SB := '';
  Len := Length(S);
  I := 1;
  while I <= Len do
  begin
    B1 := Ord(S[I]);
    Inc(I);
    if I <= Len then
      B2 := Ord(S[I])
    else
      B2 := 0;
    Inc(I);
    if I <= Len then
      B3 := Ord(S[I])
    else
      B3 := 0;
    Inc(I);
    SB := SB + BASE64_CHARS[(B1 shr 2) + 1];
    SB := SB + BASE64_CHARS[(((B1 and 3) shl 4) or (B2 shr 4)) + 1];
    if I - 1 <= Len then
      SB := SB + BASE64_CHARS[(((B2 and 15) shl 2) or (B3 shr 6)) + 1]
    else
      SB := SB + '=';
    if I - 2 <= Len then
      SB := SB + BASE64_CHARS[(B3 and 63) + 1]
    else
      SB := SB + '=';
  end;
  Result := SB;
end;

function Base64Decode(const S: string): string;
const
  BASE64_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
  
  function CharToVal(C: Char): Integer;
  var
    P: Integer;
  begin
    P := Pos(C, BASE64_CHARS);
    if P > 0 then
      Result := P - 1
    else
      Result := -1;
  end;

var
  I: Integer;
  C1, C2, C3, C4: Integer;
  B1, B2, B3: Byte;
  SB: string;
  Len: Integer;
begin
  if S = '' then
  begin
    Result := '';
    Exit;
  end;
  SB := '';
  Len := Length(S);
  I := 1;
  while I <= Len do
  begin
    C1 := CharToVal(S[I]);
    Inc(I);
    if I > Len then Break;
    C2 := CharToVal(S[I]);
    Inc(I);
    if I > Len then Break;
    C3 := CharToVal(S[I]);
    Inc(I);
    if I > Len then Break;
    C4 := CharToVal(S[I]);
    Inc(I);
    if (C1 < 0) or (C2 < 0) then Break;
    B1 := (C1 shl 2) or (C2 shr 4);
    SB := SB + Chr(B1);
    if C3 >= 0 then
    begin
      B2 := ((C2 and 15) shl 4) or (C3 shr 2);
      SB := SB + Chr(B2);
    end;
    if C4 >= 0 then
    begin
      B3 := ((C3 and 3) shl 6) or C4;
      SB := SB + Chr(B3);
    end;
  end;
  Result := SB;
end;

function UrlEncode(const S: string): string;
const
  HEX_CHARS = '0123456789ABCDEF';
var
  I: Integer;
  C: Char;
  SB: string;
begin
  SB := '';
  for I := 1 to Length(S) do
  begin
    C := S[I];
    if C in ['A'..'Z', 'a'..'z', '0'..'9', '-', '_', '.', '~'] then
      SB := SB + C
    else if C = ' ' then
      SB := SB + '+'
    else
      SB := SB + '%' + HEX_CHARS[Ord(C) shr 4 + 1] + HEX_CHARS[Ord(C) and 15 + 1];
  end;
  Result := SB;
end;

function UrlDecode(const S: string): string;
const
  HEX_CHARS = '0123456789ABCDEF';
  
  function HexToInt(const Hex: string): Integer;
  var
    I, Val: Integer;
  begin
    Result := 0;
    for I := 1 to Length(Hex) do
    begin
      Val := Pos(UpCase(Hex[I]), HEX_CHARS) - 1;
      if Val < 0 then
      begin
        Result := -1;
        Exit;
      end;
      Result := Result * 16 + Val;
    end;
  end;

var
  I: Integer;
  SB: string;
  HexVal: Integer;
begin
  SB := '';
  I := 1;
  while I <= Length(S) do
  begin
    if S[I] = '%' then
    begin
      if I + 2 <= Length(S) then
      begin
        HexVal := HexToInt(Copy(S, I + 1, 2));
        if HexVal >= 0 then
        begin
          SB := SB + Chr(HexVal);
          I := I + 3;
          Continue;
        end;
      end;
      SB := SB + S[I];
    end
    else if S[I] = '+' then
      SB := SB + ' '
    else
      SB := SB + S[I];
    Inc(I);
  end;
  Result := SB;
end;

function HtmlEscape(const S: string): string;
var
  I: Integer;
  SB: string;
begin
  SB := '';
  for I := 1 to Length(S) do
  begin
    case S[I] of
      '&': SB := SB + '&amp;';
      '<': SB := SB + '&lt;';
      '>': SB := SB + '&gt;';
      '"': SB := SB + '&quot;';
      '''': SB := SB + '&#x27;';
      else SB := SB + S[I];
    end;
  end;
  Result := SB;
end;

function HtmlUnescape(const S: string): string;
var
  SB: string;
  I: Integer;
begin
  SB := S;
  SB := ReplaceAll(SB, '&amp;', '&');
  SB := ReplaceAll(SB, '&lt;', '<');
  SB := ReplaceAll(SB, '&gt;', '>');
  SB := ReplaceAll(SB, '&quot;', '"');
  SB := ReplaceAll(SB, '&#x27;', '''');
  SB := ReplaceAll(SB, '&#39;', '''');
  Result := SB;
end;

{===============================================================================
  其他工具
===============================================================================}

function DefaultIfBlank(const S, DefaultValue: string): string;
begin
  if IsBlank(S) then
    Result := DefaultValue
  else
    Result := S;
end;

function DefaultIfEmpty(const S, DefaultValue: string): string;
begin
  if IsEmpty(S) then
    Result := DefaultValue
  else
    Result := S;
end;

function Slugify(const S: string; const Separator: string = '-'): string;
var
  I: Integer;
  SB: string;
  PrevSep: Boolean;
begin
  SB := '';
  PrevSep := True;
  for I := 1 to Length(S) do
  begin
    if S[I] in ['a'..'z', '0'..'9'] then
    begin
      SB := SB + S[I];
      PrevSep := False;
    end
    else if S[I] in ['A'..'Z'] then
    begin
      SB := SB + AnsiLowerCase(S[I]);
      PrevSep := False;
    end
    else if not PrevSep then
    begin
      SB := SB + Separator;
      PrevSep := True;
    end;
  end;
  // Remove trailing separator
  if (SB <> '') and (Copy(SB, Length(SB) - Length(Separator) + 1, Length(Separator)) = Separator) then
    SB := Copy(SB, 1, Length(SB) - Length(Separator));
  Result := SB;
end;

function StripHtml(const S: string): string;
var
  SB: string;
  I: Integer;
  InTag: Boolean;
begin
  SB := '';
  InTag := False;
  for I := 1 to Length(S) do
  begin
    if S[I] = '<' then
      InTag := True
    else if S[I] = '>' then
      InTag := False
    else if not InTag then
      SB := SB + S[I];
  end;
  Result := SB;
end;

end.
