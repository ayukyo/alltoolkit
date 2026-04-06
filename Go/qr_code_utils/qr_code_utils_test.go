package qr_code_utils

import (
	"strings"
	"testing"
)

// TestEncode 测试基础编码功能
func TestEncode(t *testing.T) {
	tests := []struct {
		name    string
		data    string
		wantErr bool
	}{
		{"简单文本", "Hello, World!", false},
		{"数字", "1234567890", false},
		{"字母数字", "HELLO123", false},
		{"中文", "你好世界", false},
		{"URL", "https://example.com/path?query=value", false},
		{"空字符串", "", true},
		{"长文本", "This is a longer text that should still be encodable with QR codes version 1 or 2.", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			qr, err := Encode(tt.data)
			if (err != nil) != tt.wantErr {
				t.Errorf("Encode() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr && qr == nil {
				t.Error("Encode() returned nil QRCode without error")
			}
		})
	}
}

// TestEncodeWithOptions 测试带选项的编码
func TestEncodeWithOptions(t *testing.T) {
	tests := []struct {
		name    string
		data    string
		opts    *EncodeOptions
		wantErr bool
	}{
		{
			name: "默认选项",
			data: "Test",
			opts: DefaultEncodeOptions(),
		},
		{
			name: "低纠错级别",
			data: "Test",
			opts: &EncodeOptions{Level: ECLevelL, Mode: ModeByte},
		},
		{
			name: "高纠错级别",
			data: "Test",
			opts: &EncodeOptions{Level: ECLevelH, Mode: ModeByte},
		},
		{
			name: "数字模式",
			data: "1234567890",
			opts: &EncodeOptions{Level: ECLevelM, Mode: ModeNumeric},
		},
		{
			name: "字母数字模式",
			data: "HELLO WORLD",
			opts: &EncodeOptions{Level: ECLevelM, Mode: ModeAlphanumeric},
		},
		{
			name: "字节模式",
			data: "Hello, World!",
			opts: &EncodeOptions{Level: ECLevelM, Mode: ModeByte},
		},
		{
			name: "nil选项",
			data: "Test",
			opts: nil,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			qr, err := EncodeWithOptions(tt.data, tt.opts)
			if (err != nil) != tt.wantErr {
				t.Errorf("EncodeWithOptions() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if err != nil {
				return
			}
			if qr == nil {
				t.Error("EncodeWithOptions() returned nil QRCode")
				return
			}
			// 验证基本属性
			if qr.Size <= 0 {
				t.Error("QRCode size should be positive")
			}
			if qr.Version < 1 || qr.Version > 40 {
				t.Errorf("QRCode version %d out of range [1,40]", qr.Version)
			}
			if len(qr.Modules) != qr.Size {
				t.Errorf("Modules row count %d != Size %d", len(qr.Modules), qr.Size)
			}
		})
	}
}

// TestQRCodeProperties 测试 QRCode 属性
func TestQRCodeProperties(t *testing.T) {
	qr, err := Encode("Test")
	if err != nil {
		t.Fatalf("Failed to encode: %v", err)
	}

	// 测试 GetSize
	if qr.GetSize() != qr.Size {
		t.Error("GetSize() should return qr.Size")
	}

	// 测试 GetVersion
	if qr.GetVersion() != qr.Version {
		t.Error("GetVersion() should return qr.Version")
	}

	// 测试 GetErrorCorrectionLevel
	if qr.GetErrorCorrectionLevel() != qr.Level {
		t.Error("GetErrorCorrectionLevel() should return qr.Level")
	}
}

// TestToASCII 测试 ASCII 输出
func TestToASCII(t *testing.T) {
	qr, err := Encode("Hi")
	if err != nil {
		t.Fatalf("Failed to encode: %v", err)
	}

	ascii := qr.ToASCII()
	if ascii == "" {
		t.Error("ToASCII() returned empty string")
	}

	// 检查是否包含 Unicode 块字符
	if !strings.Contains(ascii, "█") && !strings.Contains(ascii, " ") {
		t.Error("ASCII output should contain block characters or spaces")
	}

	// 测试带边框
	asciiWithBorder := qr.ToASCIIWithBorder(2)
	if asciiWithBorder == "" {
		t.Error("ToASCIIWithBorder() returned empty string")
	}

	// 测试负边框
	asciiNegBorder := qr.ToASCIIWithBorder(-1)
	if asciiNegBorder == "" {
		t.Error("ToASCIIWithBorder(-1) returned empty string")
	}
}

// TestToSmallASCII 测试紧凑 ASCII 输出
func TestToSmallASCII(t *testing.T) {
	qr, err := Encode("Test")
	if err != nil {
		t.Fatalf("Failed to encode: %v", err)
	}

	small := qr.ToSmallASCII()
	if small == "" {
		t.Error("ToSmallASCII() returned empty string")
	}
}

// TestToBitmap 测试位图输出
func TestToBitmap(t *testing.T) {
	qr, err := Encode("Test")
	if err != nil {
		t.Fatalf("Failed to encode: %v", err)
	}

	bitmap := qr.ToBitmap()
	if len(bitmap) != qr.Size {
		t.Errorf("Bitmap rows %d != Size %d", len(bitmap), qr.Size)
	}

	for i, row := range bitmap {
		if len(row) != qr.Size {
			t.Errorf("Bitmap row %d length %d != Size %d", i, len(row), qr.Size)
		}
	}
}

// TestToStringPattern 测试字符串模式输出
func TestToStringPattern(t *testing.T) {
	qr, err := Encode("AB")
	if err != nil {
		t.Fatalf("Failed to encode: %v", err)
	}

	pattern := qr.ToStringPattern()
	if pattern == "" {
		t.Error("ToStringPattern() returned empty string")
	}

	// 应该只包含 0、1 和换行
	for _, c := range pattern {
		if c != '0' && c != '1' && c != '\n' {
			t.Errorf("Pattern contains invalid character: %c", c)
		}
	}
}

// TestToBase64 测试 Base64 输出
func TestToBase64(t *testing.T) {
	qr, err := Encode("Test")
	if err != nil {
		t.Fatalf("Failed to encode: %v", err)
	}

	base64 := qr.ToBase64()
	if base64 == "" {
		t.Error("ToBase64() returned empty string")
	}
}

// TestIsBlack 测试模块检查
func TestIsBlack(t *testing.T) {
	qr, err := Encode("Test")
	if err != nil {
		t.Fatalf("Failed to encode: %v", err)
	}

	// 测试有效坐标
	isBlack := qr.IsBlack(0, 0)
	_ = isBlack // 只需要确保不 panic

	// 测试无效坐标（应该返回 false）
	if qr.IsBlack(-1, 0) != false {
		t.Error("IsBlack(-1, 0) should return false")
	}
	if qr.IsBlack(0, -1) != false {
		t.Error("IsBlack(0, -1) should return false")
	}
	if qr.IsBlack(qr.Size, 0) != false {
		t.Error("IsBlack(Size, 0) should return false")
	}
	if qr.IsBlack(0, qr.Size) != false {
		t.Error("IsBlack(0, Size) should return false")
	}
}

// TestString 测试字符串表示
func TestString(t *testing.T) {
	qr, err := Encode("Test")
	if err != nil {
		t.Fatalf("Failed to encode: %v", err)
	}

	s := qr.String()
	if s == "" {
		t.Error("String() returned empty string")
	}

	// 应该包含版本和尺寸信息
	if !strings.Contains(s, "v") {
		t.Error("String() should contain version info")
	}
}

// TestErrorCorrectionLevels 测试不同纠错级别
func TestErrorCorrectionLevels(t *testing.T) {
	data := "Hello, World!"
	levels := []ErrorCorrectionLevel{ECLevelL, ECLevelM, ECLevelQ, ECLevelH}

	for _, level := range levels {
		opts := &EncodeOptions{Level: level, Mode: ModeByte}
		qr, err := EncodeWithOptions(data, opts)
		if err != nil {
			t.Errorf("Failed to encode with level %d: %v", level, err)
			continue
		}
		if qr.Level != level {
			t.Errorf("QRCode level %d != expected %d", qr.Level, level)
		}
	}
}

// TestEncodingModes 测试不同编码模式
func TestEncodingModes(t *testing.T) {
	tests := []struct {
		mode EncodingMode
		data string
	}{
		{ModeNumeric, "1234567890"},
		{ModeAlphanumeric, "HELLO WORLD 123"},
		{ModeByte, "Hello, World!"},
	}

	for _, tt := range tests {
		opts := &EncodeOptions{Level: ECLevelM, Mode: tt.mode}
		qr, err := EncodeWithOptions(tt.data, opts)
		if err != nil {
			t.Errorf("Failed to encode mode %d: %v", tt.mode, err)
			continue
		}
		if qr.Mode != tt.mode {
			t.Errorf("QRCode mode %d != expected %d", qr.Mode, tt.mode)
		}
	}
}

// TestDifferentDataTypes 测试不同数据类型
func TestDifferentDataTypes(t *testing.T) {
	tests := []struct {
		name string
		data string
	}{
		{"纯数字", "12345678901234567890"},
		{"字母数字混合", "ABC123DEF456"},
		{"特殊字符", "Hello!@#$%^&*()"},
		{"Unicode", "Hello 世界 🌍"},
		{"URL", "https://github.com/ayukyo/alltoolkit"},
		{"JSON", `{"name":"test","value":123}`},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			qr, err := Encode(tt.data)
			if err != nil {
				t.Errorf("Failed to encode %s: %v", tt.name, err)
				return
			}
			if qr == nil {
				t.Error("Encode() returned nil")
			}
		})
	}
}
