package timezone_utils

import (
	"testing"
	"time"
)

func TestGetTimezone(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		wantErr  bool
	}{
		{"UTC", "UTC", false},
		{"New York", "America/New_York", false},
		{"Tokyo", "Asia/Tokyo", false},
		{"Shanghai", "Asia/Shanghai", false},
		{"London", "Europe/London", false},
		{"Invalid", "Invalid/Zone", true},
		{"Empty", "", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			tz, err := GetTimezone(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("GetTimezone() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if tz.Name != tt.input {
					t.Errorf("GetTimezone().Name = %v, want %v", tz.Name, tt.input)
				}
			 if tz.Offset == 0 && tt.input == "UTC" {
					// UTC offset is 0, correct
				}
			}
		})
	}
}

func TestGetTimezoneInfo(t *testing.T) {
	info, err := GetTimezoneInfo("America/New_York")
	if err != nil {
		t.Fatalf("GetTimezoneInfo() error = %v", err)
	}

	if info.Name != "America/New_York" {
		t.Errorf("Name = %v, want America/New_York", info.Name)
	}
	if info.Continent != "America" {
		t.Errorf("Continent = %v, want America", info.Continent)
	}
	if info.Offset == 0 {
		t.Errorf("Offset should not be 0 for New York")
	}
}

func TestConvert(t *testing.T) {
	// Create a time in New York
	nyTime := time.Date(2026, 5, 31, 12, 0, 0, 0, time.FixedZone("EST", -5*3600))
	
	// Convert to Tokyo
	tokyoTime, err := Convert(nyTime, "America/New_York", "Asia/Tokyo")
	if err != nil {
		t.Fatalf("Convert() error = %v", err)
	}
	
	// NYC is UTC-5, Tokyo is UTC+9, difference is 14 hours
	// 12:00 EST + 14 hours = 02:00 next day in Tokyo
	if tokyoTime.Hour() != 2 {
		t.Errorf("Convert() hour = %v, want 2", tokyoTime.Hour())
	}
}

func TestNow(t *testing.T) {
	now, err := Now("Asia/Shanghai")
	if err != nil {
		t.Fatalf("Now() error = %v", err)
	}
	
	if now.Location().String() != "Asia/Shanghai" {
		t.Errorf("Now().Location() = %v, want Asia/Shanghai", now.Location())
	}
}

func TestToUTC(t *testing.T) {
	// Create a time in Shanghai (UTC+8)
	shanghaiTime := time.Date(2026, 5, 31, 20, 0, 0, 0, time.FixedZone("CST", 8*3600))
	
	utcTime, err := ToUTC(shanghaiTime, "Asia/Shanghai")
	if err != nil {
		t.Fatalf("ToUTC() error = %v", err)
	}
	
	// 20:00 CST (UTC+8) = 12:00 UTC
	if utcTime.UTC().Hour() != 12 {
		t.Errorf("ToUTC() hour = %v, want 12", utcTime.UTC().Hour())
	}
}

func TestFromUTC(t *testing.T) {
	utcTime := time.Date(2026, 5, 31, 12, 0, 0, 0, time.UTC)
	
	shanghaiTime, err := FromUTC(utcTime, "Asia/Shanghai")
	if err != nil {
		t.Fatalf("FromUTC() error = %v", err)
	}
	
	// 12:00 UTC = 20:00 in Shanghai (UTC+8)
	if shanghaiTime.Hour() != 20 {
		t.Errorf("FromUTC() hour = %v, want 20", shanghaiTime.Hour())
	}
}

func TestGetOffset(t *testing.T) {
	offset, err := GetOffset("America/New_York", "Asia/Tokyo")
	if err != nil {
		t.Fatalf("GetOffset() error = %v", err)
	}
	
	// NYC is UTC-4 (DST in May), Tokyo is UTC+9, difference is 13 hours
	expectedHours := 13.0
	if offset.Hours() != expectedHours {
		t.Errorf("GetOffset() = %v hours, want %v hours", offset.Hours(), expectedHours)
	}
}

func TestGetOffsetString(t *testing.T) {
	offsetStr, err := GetOffsetString("America/New_York", "Asia/Tokyo")
	if err != nil {
		t.Fatalf("GetOffsetString() error = %v", err)
	}
	
	// Tokyo is +9, NYC is UTC-4 (DST in May), so Tokyo is 13 hours ahead
	if offsetStr != "UTC+13" {
		t.Errorf("GetOffsetString() = %v, want UTC+13", offsetStr)
	}
}

func TestIsDST(t *testing.T) {
	// Test with a known DST timezone
	isDST, err := IsDST("America/New_York")
	if err != nil {
		t.Fatalf("IsDST() error = %v", err)
	}
	// May is during DST in New York
	t.Logf("IsDST for New York in May: %v", isDST)
}

func TestCommonTimezones(t *testing.T) {
	zones := CommonTimezones()
	
	if len(zones) == 0 {
		t.Error("CommonTimezones() returned empty list")
	}
	
	// Check that expected zones are present
	expected := []string{"UTC", "America/New_York", "Asia/Tokyo", "Europe/London"}
	for _, exp := range expected {
		found := false
		for _, z := range zones {
			if z == exp {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("CommonTimezones() missing %v", exp)
		}
	}
}

func TestFindTimezoneByCity(t *testing.T) {
	results, err := FindTimezoneByCity("tokyo")
	if err != nil {
		t.Fatalf("FindTimezoneByCity() error = %v", err)
	}
	
	if len(results) == 0 {
		t.Error("FindTimezoneByCity() returned empty for 'tokyo'")
	}
	
	found := false
	for _, r := range results {
		if r == "Asia/Tokyo" {
			found = true
			break
		}
	}
	if !found {
		t.Error("FindTimezoneByCity() should find Asia/Tokyo for 'tokyo'")
	}
}

func TestIsValidTimezone(t *testing.T) {
	if !IsValidTimezone("America/New_York") {
		t.Error("IsValidTimezone() should return true for valid timezone")
	}
	
	if IsValidTimezone("Invalid/Zone") {
		t.Error("IsValidTimezone() should return false for invalid timezone")
	}
}

func TestFormatInTimezone(t *testing.T) {
	tm := time.Date(2026, 5, 31, 14, 30, 0, 0, time.UTC)
	
	result, err := FormatInTimezone(tm, "Asia/Shanghai", "2006-01-02 15:04:05")
	if err != nil {
		t.Fatalf("FormatInTimezone() error = %v", err)
	}
	
	// 14:30 UTC = 22:30 Shanghai
	if result != "2026-05-31 22:30:00" {
		t.Errorf("FormatInTimezone() = %v, want 2026-05-31 22:30:00", result)
	}
}

func TestParseInTimezone(t *testing.T) {
	result, err := ParseInTimezone("2026-05-31 22:30:00", "2006-01-02 15:04:05", "Asia/Shanghai")
	if err != nil {
		t.Fatalf("ParseInTimezone() error = %v", err)
	}
	
	// 22:30 Shanghai = 14:30 UTC
	if result.UTC().Hour() != 14 || result.UTC().Minute() != 30 {
		t.Errorf("ParseInTimezone() = %v, want 14:30 UTC", result.UTC())
	}
}

func TestGetUTCOffset(t *testing.T) {
	offset, err := GetUTCOffset("Asia/Tokyo")
	if err != nil {
		t.Fatalf("GetUTCOffset() error = %v", err)
	}
	
	if offset != "+09:00" {
		t.Errorf("GetUTCOffset() = %v, want +09:00", offset)
	}
}

func TestConvertString(t *testing.T) {
	result, err := ConvertString("2026-05-31 22:30:00", "2006-01-02 15:04:05", "Asia/Shanghai", "America/New_York")
	if err != nil {
		t.Fatalf("ConvertString() error = %v", err)
	}
	
	// 22:30 Shanghai (UTC+8) = 14:30 UTC = 10:30 New York (UTC-4 DST in May)
	if result != "2026-05-31 10:30:00" {
		t.Errorf("ConvertString() = %v, want 2026-05-31 10:30:00", result)
	}
}