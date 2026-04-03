{*******************************************************************************
  AllToolkit - Delphi String Utilities Example
  
  演示 Delphi String Utils 的各种用法
  
  编译运行：
  - Delphi IDE: 打开并运行
  - Free Pascal: fpc string_utils_example.pas && ./string_utils_example
********************************************************************************}

program string_utils_example;

{$IFDEF FPC}
  {$MODE DELPHI}
{$ENDIF}

uses
  SysUtils, Classes, mod;

procedure PrintHeader(const Title: string);
begin
  WriteLn;
  WriteLn('----------------------------------------');
  WriteLn('  ', Title);
  WriteLn('----------------------------------------');
end;

procedure Example_BlankCheck;
var
  Input: string;
begin
  PrintHeader('空值检查');
  
  Input := '';
  WriteLn('Input: ""');
  WriteLn('  IsBlank: ', IsBlank(Input));
  WriteLn('  IsEmpty: ', IsEmpty(Input));
  WriteLn('  IsNotBlank: ', IsNotBlank(Input));
  
  Input := '   ';
  WriteLn('Input: "   "');
  WriteLn('  IsBlank: ', IsBlank(Input));
  WriteLn('  IsEmpty: ', IsEmpty(Input));
  
  Input := 'hello';
  WriteLn('Input: "hello"');
  WriteLn('  IsBlank: ', IsBlank(Input));
  WriteLn('  IsNotBlank: ', IsNotBlank(Input));
end;

procedure Example_Trimming;
begin
  PrintHeader('空白字符处理');
  
  WriteLn('TrimString("  hello  "): "', TrimString('  hello  '), '"');
  WriteLn('TrimLeft("  hello  "): "', TrimLeft('  hello  '), '"');
  WriteLn('TrimRight("  hello  "): "', TrimRight('  hello  '), '"');
  WriteLn('RemoveWhitespace("h e l l o"): "', RemoveWhitespace('h e l l o'), '"');
  WriteLn('NormalizeWhitespace("hello   world"): "', NormalizeWhitespace('hello   world'), '"');
end;

procedure Example_CaseConversion;
begin
  PrintHeader('大小写转换');
  
  WriteLn('ToLower("HELLO"): ', ToLower('HELLO'));
  WriteLn('ToUpper("hello"): ', ToUpper('hello'));
  WriteLn('Capitalize("hello"): ', Capitalize('hello'));
  WriteLn('Uncapitalize("Hello"): ', Uncapitalize('Hello'));
  WriteLn('ToTitleCase("hello world"): ', ToTitleCase('hello world'));
  WriteLn('SwapCase("Hello"): ', SwapCase('Hello'));
end;

procedure Example_Substring;
begin
  PrintHeader('子串操作');
  
  WriteLn('Substring("hello world", 1, 5): ', Substring('hello world', 1, 5));
  WriteLn('SubstringFrom("hello world", 7): ', SubstringFrom('hello world', 7));
  WriteLn('SubstringTo("hello world", 5): ', SubstringTo('hello world', 5));
  WriteLn('SubstringBetween("[hello]", "[", "]"): ', SubstringBetween('[hello]', '[', ']'));
  WriteLn('SubstringAfter("path/file.txt", "/"): ', SubstringAfter('path/file.txt', '/'));
  WriteLn('SubstringBefore("path/file.txt", "/"): ', SubstringBefore('path/file.txt', '/'));
  WriteLn('SubstringAfterLast("a/b/c", "/"): ', SubstringAfterLast('a/b/c', '/'));
  WriteLn('SubstringBeforeLast("a/b/c", "/"): ', SubstringBeforeLast('a/b/c', '/'));
  WriteLn('Truncate("very long text", 10): ', Truncate('very long text', 10));
end;

procedure Example_PrefixSuffix;
begin
  PrintHeader('前缀后缀操作');
  
  WriteLn('StartsWith("hello world", "hello"): ', StartsWith('hello world', 'hello'));
  WriteLn('EndsWith("hello world", "world"): ', EndsWith('hello world', 'world'));
  WriteLn('RemovePrefix("hello world", "hello "): ', RemovePrefix('hello world', 'hello '));
  WriteLn('RemoveSuffix("hello world", " world"): ', RemoveSuffix('hello world', ' world'));
end;

procedure Example_FindReplace;
begin
  PrintHeader('查找与替换');
  
  WriteLn('CountMatches("hello hello", "hello"): ', CountMatches('hello hello', 'hello'));
  WriteLn('Contains("hello world", "world"): ', Contains('hello world', 'world'));
  WriteLn('IndexOf("hello world", "world"): ', IndexOf('hello world', 'world'));
  WriteLn('ReplaceAll("hello hello", "hello", "hi"): ', ReplaceAll('hello hello', 'hello', 'hi'));
  WriteLn('ReplaceFirst("hello hello", "hello", "hi"): ', ReplaceFirst('hello hello', 'hello', 'hi'));
end;

procedure Example_Padding;
begin
  PrintHeader('填充与对齐');
  
  WriteLn('PadLeft("5", 3, "0"): ', PadLeft('5', 3, '0'));
  WriteLn('PadRight("5", 3, "0"): ', PadRight('5', 3, '0'));
  WriteLn('Center("hi", 6, "-"): ', Center('hi', 6, '-'));
end;

procedure Example_NamingConventions;
begin
  PrintHeader('命名风格转换');
  
  WriteLn('ToCamelCase("hello_world"): ', ToCamelCase('hello_world'));
  WriteLn('ToCamelCase("hello-world"): ', ToCamelCase('hello-world'));
  WriteLn('ToPascalCase("hello_world"): ', ToPascalCase('hello_world'));
  WriteLn('ToSnakeCase("HelloWorld"): ', ToSnakeCase('HelloWorld'));
  WriteLn('ToKebabCase("HelloWorld"): ', ToKebabCase('HelloWorld'));
end;

procedure Example_Validation;
begin
  PrintHeader('字符串验证');
  
  WriteLn('IsValidEmail("test@example.com"): ', IsValidEmail('test@example.com'));
  WriteLn('IsValidEmail("invalid"): ', IsValidEmail('invalid'));
  WriteLn('IsValidUrl("https://example.com"): ', IsValidUrl('https://example.com'));
  WriteLn('IsNumeric("123.45"): ', IsNumeric('123.45'));
  WriteLn('IsInteger("123"): ', IsInteger('123'));
  WriteLn('IsAlpha("abc"): ', IsAlpha('abc'));
  WriteLn('IsAlphanumeric("abc123"): ', IsAlphanumeric('abc123'));
end;

procedure Example_Encoding;
begin
  PrintHeader('编码解码');
  
  WriteLn('Base64Encode("hello"): ', Base64Encode('hello'));
  WriteLn('Base64Decode("aGVsbG8="): ', Base64Decode('aGVsbG8='));
  WriteLn('UrlEncode("hello world"): ', UrlEncode('hello world'));
  WriteLn('UrlDecode("hello+world"): ', UrlDecode('hello+world'));
  WriteLn('HtmlEscape("<div>"): ', HtmlEscape('<div>'));
  WriteLn('HtmlUnescape("&lt;div&gt;"): ', HtmlUnescape('&lt;div&gt;'));
end;

procedure Example_Random;
begin
  PrintHeader('随机生成');
  
  WriteLn('RandomString(10): ', RandomString(10));
  WriteLn('RandomAlphanumeric(10): ', RandomAlphanumeric(10));
  WriteLn('RandomNumeric(10): ', RandomNumeric(10));
  WriteLn('RandomPassword(16): ', RandomPassword(16));
end;

procedure Example_SplitJoin;
var
  List: TStringList;
  I: Integer;
begin
  PrintHeader('分割与连接');
  
  List := Split('apple,banana,cherry', ',');
  WriteLn('Split("apple,banana,cherry", ","):');
  for I := 0 to List.Count - 1 do
    WriteLn('  [', I, '] = ', List[I]);
  List.Free;
  
  List := TStringList.Create;
  List.Add('apple');
  List.Add('banana');
  List.Add('cherry');
  WriteLn('Join: ', Join(List, ' | '));
  List.Free;
end;

procedure Example_Utilities;
begin
  PrintHeader('其他工具');
  
  WriteLn('DefaultIfBlank("", "default"): ', DefaultIfBlank('', 'default'));
  WriteLn('DefaultIfBlank("value", "default"): ', DefaultIfBlank('value', 'default'));
  WriteLn('Slugify("Hello World"): ', Slugify('Hello World'));
  WriteLn('StripHtml("<p>hello</p>"): ', StripHtml('<p>hello</p>'));
  WriteLn('Reverse("hello"): ', Reverse('hello'));
  WriteLn('RepeatString("ab", 3): ', RepeatString('ab', 3));
end;

begin
  WriteLn('========================================');
  WriteLn('  AllToolkit - String Utilities Demo');
  WriteLn('========================================');
  
  Example_BlankCheck;
  Example_Trimming;
  Example_CaseConversion;
  Example_Substring;
  Example_PrefixSuffix;
  Example_FindReplace;
  Example_Padding;
  Example_NamingConventions;
  Example_Validation;
  Example_Encoding;
  Example_Random;
  Example_SplitJoin;
  Example_Utilities;
  
  WriteLn;
  WriteLn('========================================');
  WriteLn('  Demo Complete!');
  WriteLn('========================================');
end.
