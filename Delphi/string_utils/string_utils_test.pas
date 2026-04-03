{*******************************************************************************
  AllToolkit - Delphi String Utilities Tests
  
  测试套件：验证所有字符串工具函数的正确性
  
  运行方式：
  - Delphi: 在IDE中打开并运行
  - Free Pascal: fpc string_utils_test.pas && ./string_utils_test
********************************************************************************}

program string_utils_test;

{$IFDEF FPC}
  {$MODE DELPHI}
{$ENDIF}

uses
  SysUtils, Classes, mod;

var
  Passed, Failed: Integer;

procedure Test(const Name: string; Condition: Boolean);
begin
  if Condition then
  begin
    WriteLn('  [PASS] ', Name);
    Inc(Passed);
  end
  else
  begin
    WriteLn('  [FAIL] ', Name);
    Inc(Failed);
  end;
end;

procedure Test_IsBlank;
begin
  WriteLn('Testing IsBlank...');
  Test('IsBlank empty string', IsBlank(''));
  Test('IsBlank whitespace only', IsBlank('   '));
  Test('IsBlank tab and newline', IsBlank(#9#10#13));
  Test('IsBlank non-blank', not IsBlank('hello'));
  Test('IsBlank with content', not IsBlank('  hello  '));
end;

procedure Test_IsNotBlank;
begin
  WriteLn('Testing IsNotBlank...');
  Test('IsNotBlank with content', IsNotBlank('hello'));
  Test('IsNotBlank empty', not IsNotBlank(''));
  Test('IsNotBlank whitespace', not IsNotBlank('   '));
end;

procedure Test_IsEmpty;
begin
  WriteLn('Testing IsEmpty...');
  Test('IsEmpty empty string', IsEmpty(''));
  Test('IsEmpty non-empty', not IsEmpty('hello'));
  Test('IsEmpty whitespace', not IsEmpty('   '));
end;

procedure Test_Trimming;
begin
  WriteLn('Testing Trim functions...');
  Test('TrimString', TrimString('  hello  ') = 'hello');
  Test('TrimLeft', TrimLeft('  hello  ') = 'hello  ');
  Test('TrimRight', TrimRight('  hello  ') = '  hello');
  Test('RemoveWhitespace', RemoveWhitespace('h e l l o') = 'hello');
  Test('NormalizeWhitespace', NormalizeWhitespace('hello   world') = 'hello world');
end;

procedure Test_CaseConversion;
begin
  WriteLn('Testing Case Conversion...');
  Test('ToLower', ToLower('HELLO') = 'hello');
  Test('ToUpper', ToUpper('hello') = 'HELLO');
  Test('Capitalize', Capitalize('hello') = 'Hello');
  Test('Uncapitalize', Uncapitalize('Hello') = 'hello');
  Test('ToTitleCase', ToTitleCase('hello world') = 'Hello World');
  Test('SwapCase', SwapCase('Hello') = 'hELLO');
end;

procedure Test_Substring;
begin
  WriteLn('Testing Substring functions...');
  Test('Substring', Substring('hello world', 1, 5) = 'hello');
  Test('SubstringFrom', SubstringFrom('hello world', 7) = 'world');
  Test('SubstringTo', SubstringTo('hello world', 5) = 'hello');
  Test('SubstringBetween', SubstringBetween('hello [world] end', '[', ']') = 'world');
  Test('SubstringAfter', SubstringAfter('hello/world', '/') = 'world');
  Test('SubstringBefore', SubstringBefore('hello/world', '/') = 'hello');
  Test('SubstringAfterLast', SubstringAfterLast('a/b/c', '/') = 'c');
  Test('SubstringBeforeLast', SubstringBeforeLast('a/b/c', '/') = 'a/b');
  Test('Truncate', Truncate('hello world', 8) = 'hello...');
end;

procedure Test_PrefixSuffix;
begin
  WriteLn('Testing Prefix/Suffix...');
  Test('StartsWith', StartsWith('hello world', 'hello'));
  Test('StartsWith ignore case', StartsWith('Hello World', 'hello', True));
  Test('EndsWith', EndsWith('hello world', 'world'));
  Test('EndsWith ignore case', EndsWith('Hello World', 'WORLD', True));
  Test('RemovePrefix', RemovePrefix('hello world', 'hello ') = 'world');
  Test('RemoveSuffix', RemoveSuffix('hello world', ' world') = 'hello');
end;

procedure Test_FindCount;
begin
  WriteLn('Testing Find and Count...');
  Test('CountMatches', CountMatches('hello hello', 'hello') = 2);
  Test('Contains', Contains('hello world', 'world'));
  Test('IndexOf', IndexOf('hello world', 'world') = 7);
  Test('LastIndexOf', LastIndexOf('hello hello', 'hello') = 7);
end;

procedure Test_Replace;
begin
  WriteLn('Testing Replace...');
  Test('ReplaceAll', ReplaceAll('hello hello', 'hello', 'hi') = 'hi hi');
  Test('ReplaceFirst', ReplaceFirst('hello hello', 'hello', 'hi') = 'hi hello');
  Test('ReplaceLast', ReplaceLast('hello hello', 'hello', 'hi') = 'hello hi');
end;

procedure Test_Padding;
begin
  WriteLn('Testing Padding...');
  Test('PadLeft', PadLeft('5', 3, '0') = '005');
  Test('PadRight', PadRight('5', 3, '0') = '500');
  Test('Center', Center('hi', 6, '-') = '--hi--');
end;

procedure Test_ReverseRepeat;
begin
  WriteLn('Testing Reverse and Repeat...');
  Test('Reverse', Reverse('hello') = 'olleh');
  Test('RepeatString', RepeatString('ab', 3) = 'ababab');
end;

procedure Test_NamingConventions;
begin
  WriteLn('Testing Naming Conventions...');
  Test('ToCamelCase', ToCamelCase('hello_world') = 'helloWorld');
  Test('ToPascalCase', ToPascalCase('hello_world') = 'HelloWorld');
  Test('ToSnakeCase', ToSnakeCase('HelloWorld') = 'hello_world');
  Test('ToKebabCase', ToKebabCase('HelloWorld') = 'hello-world');
end;

procedure Test_Validation;
begin
  WriteLn('Testing Validation...');
  Test('IsValidEmail', IsValidEmail('test@example.com'));
  Test('IsValidUrl', IsValidUrl('https://example.com'));
  Test('IsNumeric', IsNumeric('123.45'));
  Test('IsInteger', IsInteger('123'));
  Test('IsAlpha', IsAlpha('abc'));
  Test('IsAlphanumeric', IsAlphanumeric('abc123'));
end;

procedure Test_Encoding;
begin
  WriteLn('Testing Encoding...');
  Test('Base64Encode', Base64Encode('hello') = 'aGVsbG8=');
  Test('Base64Decode', Base64Decode('aGVsbG8=') = 'hello');
  Test('UrlEncode', UrlEncode('hello world') = 'hello+world');
  Test('UrlDecode', UrlDecode('hello+world') = 'hello world');
  Test('HtmlEscape', HtmlEscape('<div>') = '&lt;div&gt;');
  Test('HtmlUnescape', HtmlUnescape('&lt;div&gt;') = '<div>');
end;

procedure Test_Utilities;
begin
  WriteLn('Testing Utilities...');
  Test('DefaultIfBlank', DefaultIfBlank('', 'default') = 'default');
  Test('DefaultIfEmpty', DefaultIfEmpty('', 'default') = 'default');
  Test('Slugify', Slugify('Hello World') = 'hello-world');
  Test('StripHtml', StripHtml('<p>hello</p>') = 'hello');
end;

procedure Test_SplitJoin;
var
  List: TStringList;
begin
  WriteLn('Testing Split and Join...');
  List := Split('a,b,c', ',');
  Test('Split count', List.Count = 3);
  Test('Split first', List[0] = 'a');
  List.Free;
  
  List := TStringList.Create;
  List.Add('a');
  List.Add('b');
  List.Add('c');
  Test('Join', Join(List, ',') = 'a,b,c');
  List.Free;
end;

begin
  WriteLn('========================================');
  WriteLn('  AllToolkit - String Utilities Tests');
  WriteLn('========================================');
  WriteLn;
  
  Passed := 0;
  Failed := 0;
  
  Test_IsBlank;
  Test_IsNotBlank;
  Test_IsEmpty;
  Test_Trimming;
  Test_CaseConversion;
  Test_Substring;
  Test_PrefixSuffix;
  Test_FindCount;
  Test_Replace;
  Test_Padding;
  Test_ReverseRepeat;
  Test_NamingConventions;
  Test_Validation;
  Test_Encoding;
  Test_Utilities;
  Test_SplitJoin;
  
  WriteLn;
  WriteLn('========================================');
  WriteLn('  Results: ', Passed, ' passed, ', Failed, ' failed');
  WriteLn('========================================');
  
  if Failed > 0 then
    Halt(1);
end.
