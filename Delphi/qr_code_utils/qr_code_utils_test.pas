{ AllToolkit QR Code Utils Test Suite }
program qr_code_utils_test;

{$IFDEF FPC}
  {$MODE DELPHI}
{$ENDIF}

uses
  SysUtils, mod;

var
  Passed: Integer = 0;
  Failed: Integer = 0;

procedure Test(const TestName: string; Condition: Boolean);
begin
  if Condition then
  begin
    Writeln('[PASS] ', TestName);
    Inc(Passed);
  end
  else
  begin
    Writeln('[FAIL] ', TestName);
    Inc(Failed);
  end;
end;

procedure TestGetMode;
begin
  Writeln; Writeln('=== Test GetMode ===');
  Test('Numeric mode', TQRCodeUtils.GetMode('123456') = qmNumeric);
  Test('Alphanumeric mode', TQRCodeUtils.GetMode('HELLO') = qmAlphanumeric);
  Test('Byte mode', TQRCodeUtils.GetMode('Hello') = qmByte);
end;

procedure TestGetQRCodeSize;
begin
  Writeln; Writeln('=== Test GetQRCodeSize ===');
  Test('Version 1 size', TQRCodeUtils.GetQRCodeSize(1) = 21);
  Test('Version 5 size', TQRCodeUtils.GetQRCodeSize(5) = 37);
  Test('Version 10 size', TQRCodeUtils.GetQRCodeSize(10) = 57);
end;

procedure TestCanEncode;
begin
  Writeln; Writeln('=== Test CanEncode ===');
  Test('Short numeric V1', TQRCodeUtils.CanEncode('12345', 1, ecM));
  Test('Long numeric needs higher', not TQRCodeUtils.CanEncode('12345678901234567890', 1, ecM));
  Test('Alphanumeric V1', TQRCodeUtils.CanEncode('HELLO', 1, ecM));
end;

procedure TestGetMaxCapacity;
begin
  Writeln; Writeln('=== Test GetMaxCapacity ===');
  Test('V1 Numeric capacity', TQRCodeUtils.GetMaxCapacity(1, ecM, qmNumeric) > 0);
  Test('V2 > V1 capacity', TQRCodeUtils.GetMaxCapacity(2, ecM, qmNumeric) > TQRCodeUtils.GetMaxCapacity(1, ecM, qmNumeric));
end;

procedure TestGetRecommendedVersion;
begin
  Writeln; Writeln('=== Test GetRecommendedVersion ===');
  Test('Short data V1', TQRCodeUtils.GetRecommendedVersion('123', ecM) = 1);
  Test('Empty data returns -1', TQRCodeUtils.GetRecommendedVersion('', ecM) = -1);
end;

procedure TestValidateData;
begin
  Writeln; Writeln('=== Test ValidateData ===');
  Test('Valid data', TQRCodeUtils.ValidateData('Hello'));
  Test('Empty data fails', not TQRCodeUtils.ValidateData(''));
end;

procedure TestErrorLevelConversion;
begin
  Writeln; Writeln('=== Test ErrorLevel Conversion ===');
  Test('ecL to string', TQRCodeUtils.ErrorLevelToString(ecL) = 'L');
  Test('ecM to string', TQRCodeUtils.ErrorLevelToString(ecM) = 'M');
  Test('String L to ecL', TQRCodeUtils.StringToErrorLevel('L') = ecL);
  Test('Invalid defaults to M', TQRCodeUtils.StringToErrorLevel('X') = ecM);
end;

procedure TestGenerate;
var
  QRCode: TQRCode;
begin
  Writeln; Writeln('=== Test Generate ===');
  try
    QRCode := TQRCodeUtils.Generate('TEST', ecM);
    Test('Generate returns valid version', QRCode.Version > 0);
    Test('Generate returns valid width', QRCode.Width > 0);
    Test('Matrix initialized', Length(QRCode.Matrix) > 0);
  except
    on E: Exception do
      Test('Generate exception: ' + E.Message, False);
  end;
end;

procedure TestGenerateText;
var
  Text: string;
begin
  Writeln; Writeln('=== Test GenerateText ===');
  Text := TQRCodeUtils.GenerateText('A', '#', ' ', ecM);
  Test('GenerateText non-empty', Length(Text) > 0);
  Test('GenerateText has dark modules', Pos('#', Text) > 0);
end;

procedure TestGenerateSVG;
var
  SVG: string;
begin
  Writeln; Writeln('=== Test GenerateSVG ===');
  SVG := TQRCodeUtils.GenerateSVG('TEST', 4, ecM);
  Test('GenerateSVG non-empty', Length(SVG) > 0);
  Test('GenerateSVG has XML', Pos('<?xml', SVG) > 0);
  Test('GenerateSVG has svg tag', Pos('<svg', SVG) > 0);
end;

procedure TestEncodeNumeric;
begin
  Writeln; Writeln('=== Test EncodeNumeric ===');
  Test('EncodeNumeric non-empty', Length(TQRCodeUtils.EncodeNumeric('123')) > 0);
  Test('EncodeNumeric empty for alpha', TQRCodeUtils.EncodeNumeric('ABC') = '');
end;

procedure TestEncodeAlphanumeric;
begin
  Writeln; Writeln('=== Test EncodeAlphanumeric ===');
  Test('EncodeAlphanumeric non-empty', Length(TQRCodeUtils.EncodeAlphanumeric('HELLO')) > 0);
end;

procedure TestGetCapacityInfo;
var
  Info: string;
begin
  Writeln; Writeln('=== Test GetCapacityInfo ===');
  Info := TQRCodeUtils.GetCapacityInfo('TEST', ecM);
  Test('GetCapacityInfo non-empty', Length(Info) > 0);
  Test('GetCapacityInfo has Mode', Pos('Mode:', Info) > 0);
end;

begin
  Writeln('========================================');
  Writeln('AllToolkit QR Code Utils Test Suite');
  Writeln('========================================');

  TestGetMode;
  TestGetQRCodeSize;
  TestCanEncode;
  TestGetMaxCapacity;
  TestGetRecommendedVersion;
  TestValidateData;
  TestErrorLevelConversion;
  TestGenerate;
  TestGenerateText;
  TestGenerateSVG;
  TestEncodeNumeric;
  TestEncodeAlphanumeric;
  TestGetCapacityInfo;

  Writeln;
  Writeln('========================================');
  Writeln('Results: ', Passed, ' passed, ', Failed, ' failed');
  Writeln('========================================');

  if Failed > 0 then
    Halt(1);
end.
