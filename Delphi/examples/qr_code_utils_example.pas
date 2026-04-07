{ AllToolkit QR Code Utils Example }
program qr_code_utils_example;

{$IFDEF FPC}
  {$MODE DELPHI}
{$ENDIF}

uses
  SysUtils, Classes, mod;

procedure Example1_BasicGeneration;
var
  QRCode: TQRCode;
begin
  Writeln('=== Example 1: Basic QR Code Generation ===');
  
  QRCode := TQRCodeUtils.Generate('HELLO', ecM);
  Writeln('Data: HELLO');
  Writeln('Version: ', QRCode.Version);
  Writeln('Size: ', QRCode.Width, 'x', QRCode.Width);
  Writeln('Mode: ', Ord(QRCode.Mode));
  Writeln('Error Level: ', TQRCodeUtils.ErrorLevelToString(QRCode.ErrorLevel));
  Writeln;
end;

procedure Example2_TextOutput;
var
  TextQR: string;
begin
  Writeln('=== Example 2: Text Output ===');
  
  TextQR := TQRCodeUtils.GenerateText('TEST', '#', ' ', ecM);
  Writeln('QR Code as text:');
  Writeln(TextQR);
end;

procedure Example3_SVGOutput;
var
  SVG: string;
  FileName: string;
  F: TextFile;
begin
  Writeln('=== Example 3: SVG Output ===');
  
  SVG := TQRCodeUtils.GenerateSVG('https://example.com', 4, ecM);
  FileName := 'qrcode_example.svg';
  
  AssignFile(F, FileName);
  Rewrite(F);
  Write(F, SVG);
  CloseFile(F);
  
  Writeln('SVG saved to: ', FileName);
  Writeln('SVG size: ', Length(SVG), ' bytes');
  Writeln;
end;

procedure Example4_DifferentErrorLevels;
begin
  Writeln('=== Example 4: Different Error Correction Levels ===');
  
  Writeln('Level L (Low):    Max capacity = ', 
    TQRCodeUtils.GetMaxCapacity(1, ecL, qmAlphanumeric));
  Writeln('Level M (Medium): Max capacity = ', 
    TQRCodeUtils.GetMaxCapacity(1, ecM, qmAlphanumeric));
  Writeln('Level Q (Quartile): Max capacity = ', 
    TQRCodeUtils.GetMaxCapacity(1, ecQ, qmAlphanumeric));
  Writeln('Level H (High):   Max capacity = ', 
    TQRCodeUtils.GetMaxCapacity(1, ecH, qmAlphanumeric));
  Writeln;
end;

procedure Example5_EncodingModes;
begin
  Writeln('=== Example 5: Encoding Modes ===');
  
  Writeln('Numeric "123456": Mode = ', Ord(TQRCodeUtils.GetMode('123456')));
  Writeln('Alphanumeric "ABC123": Mode = ', Ord(TQRCodeUtils.GetMode('ABC123')));
  Writeln('Byte "Hello World": Mode = ', Ord(TQRCodeUtils.GetMode('Hello World')));
  Writeln;
end;

procedure Example6_CapacityInfo;
begin
  Writeln('=== Example 6: Capacity Information ===');
  
  Writeln(TQRCodeUtils.GetCapacityInfo('SHORT', ecM));
  Writeln(TQRCodeUtils.GetCapacityInfo('https://www.example.com/page', ecM));
  Writeln;
end;

procedure Example7_VersionComparison;
var
  I: Integer;
begin
  Writeln('=== Example 7: Version Comparison ===');
  Writeln('Version | Numeric | Alpha | Byte');
  Writeln('--------|---------|-------|-----');
  
  for I := 1 to 5 do
  begin
    Writeln(Format('   %d    |   %3d   |  %3d  | %3d', [
      I,
      TQRCodeUtils.GetMaxCapacity(I, ecM, qmNumeric),
      TQRCodeUtils.GetMaxCapacity(I, ecM, qmAlphanumeric),
      TQRCodeUtils.GetMaxCapacity(I, ecM, qmByte)
    ]));
  end;
  Writeln;
end;

procedure Example8_CanEncodeCheck;
begin
  Writeln('=== Example 8: Can Encode Check ===');
  
  if TQRCodeUtils.CanEncode('HELLO', 1, ecM) then
    Writeln('"HELLO" can be encoded in Version 1');
  
  if not TQRCodeUtils.CanEncode(StringOfChar('A', 100), 1, ecM) then
    Writeln('100 characters cannot be encoded in Version 1');
  
  Writeln;
end;

procedure Example9_EncodeNumeric;
var
  Encoded: string;
begin
  Writeln('=== Example 9: Encode Numeric ===');
  
  Encoded := TQRCodeUtils.EncodeNumeric('123456789');
  Writeln('Numeric "123456789" encoded: ', Encoded);
  Writeln;
end;

procedure Example10_EncodeAlphanumeric;
var
  Encoded: string;
begin
  Writeln('=== Example 10: Encode Alphanumeric ===');
  
  Encoded := TQRCodeUtils.EncodeAlphanumeric('HELLO');
  Writeln('Alphanumeric "HELLO" encoded: ', Encoded);
  Writeln;
end;

procedure Example11_CustomCharacters;
var
  TextQR: string;
begin
  Writeln('=== Example 11: Custom Characters ===');
  
  TextQR := TQRCodeUtils.GenerateText('QR', 'X', '.', ecM);
  Writeln('QR Code with X and . :');
  Writeln(TextQR);
end;

procedure Example12_URLQRCode;
begin
  Writeln('=== Example 12: URL QR Code ===');
  
  Writeln('URL: https://github.com/ayukyo/alltoolkit');
  Writeln('Capacity: ', TQRCodeUtils.GetCapacityInfo('https://github.com/ayukyo/alltoolkit', ecM));
  Writeln;
end;

begin
  Writeln('========================================');
  Writeln('AllToolkit QR Code Utils Examples');
  Writeln('========================================');
  Writeln;

  Example1_BasicGeneration;
  Example2_TextOutput;
  Example3_SVGOutput;
  Example4_DifferentErrorLevels;
  Example5_EncodingModes;
  Example6_CapacityInfo;
  Example7_VersionComparison;
  Example8_CanEncodeCheck;
  Example9_EncodeNumeric;
  Example10_EncodeAlphanumeric;
  Example11_CustomCharacters;
  Example12_URLQRCode;

  Writeln('========================================');
  Writeln('All examples completed!');
  Writeln('========================================');

  Readln;
end.
