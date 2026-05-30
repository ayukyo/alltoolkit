// Package timezone_utils provides timezone conversion and lookup utilities.
// Zero external dependencies - uses only Go standard library.
package timezone_utils

import (
	"errors"
	"fmt"
	"strings"
	"time"
)

// Common errors
var (
	ErrInvalidTimezone   = errors.New("invalid timezone")
	ErrInvalidLocation   = errors.New("invalid location")
	ErrTimeOutOfRange    = errors.New("time out of supported range")
)

// Timezone represents a timezone with its offset and location info
type Timezone struct {
	Name     string        // e.g., "America/New_York"
	Offset   time.Duration // offset from UTC
	Location *time.Location
}

// TimezoneInfo provides detailed timezone information
type TimezoneInfo struct {
	Name           string        `json:"name"`
	Offset         time.Duration `json:"offset"`
	OffsetString   string        `json:"offset_string"`  // e.g., "-05:00"
	UTCOffset      int           `json:"utc_offset"`      // offset in seconds
	IsUTC          bool          `json:"is_utc"`
	Isdst          bool          `json:"is_dst"`          // daylight saving time
	 DSTSavings    int           `json:"dst_savings"`     // DST offset in seconds
	Location       string        `json:"location"`       // city/region
	Continent      string        `json:"continent"`
	Country        string        `json:"country"`
	Coordinates    string        `json:"coordinates"`
}

// ==================== Timezone Lookup ====================

// GetTimezone returns a Timezone struct for the given timezone name
func GetTimezone(name string) (*Timezone, error) {
	if name == "" {
		return nil, ErrInvalidTimezone
	}

	// Handle UTC alias
	if strings.ToUpper(name) == "UTC" {
		return &Timezone{
			Name:     "UTC",
			Offset:   0,
			Location: time.UTC,
		}, nil
	}

	loc, err := time.LoadLocation(name)
	if err != nil {
		return nil, fmt.Errorf("%w: %s", ErrInvalidTimezone, name)
	}

	// Get current offset
	now := time.Now()
	_, offset := now.In(loc).Zone()

	return &Timezone{
		Name:     name,
		Offset:   time.Duration(offset) * time.Second,
		Location: loc,
	}, nil
}

// GetTimezoneInfo returns detailed information about a timezone
func GetTimezoneInfo(name string) (*TimezoneInfo, error) {
	tz, err := GetTimezone(name)
	if err != nil {
		return nil, err
	}

	now := time.Now()
	inZone := now.In(tz.Location)
	_, offset := inZone.Zone()

	// Parse continent/country from name
	parts := strings.Split(name, "/")
	var continent, country, location string
	if len(parts) >= 2 {
		continent = parts[0]
		location = strings.Join(parts[1:], "/")
		if len(parts) >= 3 {
			country = parts[len(parts)-1]
		}
	}

	// Determine if DST is active
	jan := time.Date(now.Year(), time.January, 15, 12, 0, 0, 0, tz.Location)
	jul := time.Date(now.Year(), time.July, 15, 12, 0, 0, 0, tz.Location)
	_, janOffset := jan.Zone()
	_, julOffset := jul.Zone()
	isDST := offset != janOffset || offset != julOffset
	dstSavings := 0
	if isDST {
		if offset > janOffset {
			dstSavings = offset - janOffset
		} else {
			dstSavings = offset - julOffset
		}
		if dstSavings < 0 {
			dstSavings = -dstSavings
		}
	}

	// Format offset string
	absOffset := time.Duration(offset) * time.Second
	hours := int(absOffset.Hours())
	minutes := int(absOffset.Minutes()) % 60
	offsetStr := fmt.Sprintf("%+03d:%02d", hours, minutes)

	return &TimezoneInfo{
		Name:         name,
		Offset:       absOffset,
		OffsetString: offsetStr,
		UTCOffset:    offset,
		IsUTC:        strings.ToUpper(name) == "UTC",
		Isdst:        isDST,
		DSTSavings:   dstSavings,
		Location:     location,
		Continent:    continent,
		Country:      country,
	}, nil
}

// ==================== Conversion ====================

// Convert converts a time from one timezone to another
func Convert(t time.Time, fromZone, toZone string) (time.Time, error) {
	fromTz, err := GetTimezone(fromZone)
	if err != nil {
		return time.Time{}, fmt.Errorf("invalid source timezone: %w", err)
	}

	toTz, err := GetTimezone(toZone)
	if err != nil {
		return time.Time{}, fmt.Errorf("invalid target timezone: %w", err)
	}

	// Interpret t as being in the source timezone, then convert to target timezone
	return t.In(fromTz.Location).In(toTz.Location), nil
}

// ConvertString converts a time string from one timezone to another
func ConvertString(timeStr, format, fromZone, toZone string) (string, error) {
	fromTz, err := GetTimezone(fromZone)
	if err != nil {
		return "", fmt.Errorf("invalid source timezone: %w", err)
	}

	toTz, err := GetTimezone(toZone)
	if err != nil {
		return "", fmt.Errorf("invalid target timezone: %w", err)
	}

	// Parse the time in source timezone
	t, err := time.ParseInLocation(format, timeStr, fromTz.Location)
	if err != nil {
		return "", fmt.Errorf("invalid time format: %w", err)
	}

	// Convert to target timezone
	converted := t.In(toTz.Location)
	return converted.Format(format), nil
}

// ToUTC converts a time to UTC
func ToUTC(t time.Time, fromZone string) (time.Time, error) {
	return Convert(t, fromZone, "UTC")
}

// FromUTC converts a UTC time to a specific timezone
func FromUTC(t time.Time, toZone string) (time.Time, error) {
	return Convert(t, "UTC", toZone)
}

// ==================== Current Time ====================

// Now returns the current time in the specified timezone
func Now(zone string) (time.Time, error) {
	tz, err := GetTimezone(zone)
	if err != nil {
		return time.Time{}, err
	}
	return time.Now().In(tz.Location), nil
}

// Today returns today's date in the specified timezone (midnight)
func Today(zone string) (time.Time, error) {
	tz, err := GetTimezone(zone)
	if err != nil {
		return time.Time{}, err
	}
	now := time.Now().In(tz.Location)
	return time.Date(now.Year(), now.Month(), now.Day(), 0, 0, 0, 0, tz.Location), nil
}

// ==================== Offset Calculation ====================

// GetOffset calculates the offset between two timezones at a given time
func GetOffset(zone1, zone2 string, atTime ...time.Time) (time.Duration, error) {
	tz1, err := GetTimezone(zone1)
	if err != nil {
		return 0, err
	}
	tz2, err := GetTimezone(zone2)
	if err != nil {
		return 0, err
	}

	var t time.Time
	if len(atTime) > 0 {
		t = atTime[0]
	} else {
		t = time.Now()
	}

	_, offset1 := t.In(tz1.Location).Zone()
	_, offset2 := t.In(tz2.Location).Zone()

	return time.Duration(offset2-offset1) * time.Second, nil
}

// GetOffsetString returns a human-readable offset string
func GetOffsetString(zone1, zone2 string) (string, error) {
	offset, err := GetOffset(zone1, zone2)
	if err != nil {
		return "", err
	}

	absOffset := offset
	sign := "+"
	if offset < 0 {
		absOffset = -offset
		sign = "-"
	}

	hours := int(absOffset.Hours())
	minutes := int(absOffset.Minutes()) % 60

	if hours == 0 && minutes == 0 {
		return "UTC", nil
	}

	if minutes == 0 {
		return fmt.Sprintf("UTC%s%d", sign, hours), nil
	}

	return fmt.Sprintf("UTC%s%d:%02d", sign, hours, minutes), nil
}

// ==================== Timezone List ====================

// CommonTimezones returns a list of common timezone names
func CommonTimezones() []string {
	return []string{
		// UTC
		"UTC",
		// Americas
		"America/New_York",
		"America/Chicago",
		"America/Denver",
		"America/Los_Angeles",
		"America/Anchorage",
		"America/Phoenix",
		"America/Toronto",
		"America/Vancouver",
		"America/Mexico_City",
		"America/Sao_Paulo",
		"America/Buenos_Aires",
		// Europe
		"Europe/London",
		"Europe/Paris",
		"Europe/Berlin",
		"Europe/Rome",
		"Europe/Madrid",
		"Europe/Amsterdam",
		"Europe/Moscow",
		// Asia
		"Asia/Tokyo",
		"Asia/Seoul",
		"Asia/Shanghai",
		"Asia/Hong_Kong",
		"Asia/Singapore",
		"Asia/Dubai",
		"Asia/Kolkata",
		"Asia/Bangkok",
		"Asia/Jakarta",
		"Asia/Manila",
		"Asia/Taipei",
		// Oceania
		"Australia/Sydney",
		"Australia/Melbourne",
		"Australia/Perth",
		"Pacific/Auckland",
		"Pacific/Honolulu",
		// Africa
		"Africa/Cairo",
		"Africa/Johannesburg",
		"Africa/Lagos",
	}
}

// GetTimezonesByContinent returns timezones grouped by continent
func GetTimezonesByContinent() map[string][]string {
	return map[string][]string{
		"Americas": {
			"America/New_York",
			"America/Los_Angeles",
			"America/Chicago",
			"America/Denver",
			"America/Toronto",
			"America/Vancouver",
			"America/Mexico_City",
			"America/Sao_Paulo",
		},
		"Europe": {
			"Europe/London",
			"Europe/Paris",
			"Europe/Berlin",
			"Europe/Rome",
			"Europe/Madrid",
			"Europe/Amsterdam",
			"Europe/Moscow",
		},
		"Asia": {
			"Asia/Tokyo",
			"Asia/Seoul",
			"Asia/Shanghai",
			"Asia/Hong_Kong",
			"Asia/Singapore",
			"Asia/Dubai",
			"Asia/Kolkata",
			"Asia/Bangkok",
			"Asia/Taipei",
		},
		"Oceania": {
			"Australia/Sydney",
			"Australia/Melbourne",
			"Australia/Perth",
			"Pacific/Auckland",
			"Pacific/Honolulu",
		},
		"Africa": {
			"Africa/Cairo",
			"Africa/Johannesburg",
			"Africa/Lagos",
		},
	}
}

// FindTimezoneByCity searches for timezones matching a city name
func FindTimezoneByCity(city string) ([]string, error) {
	city = strings.ToLower(city)
	var results []string

	for _, tz := range CommonTimezones() {
		tzLower := strings.ToLower(tz)
		if strings.Contains(tzLower, city) {
			results = append(results, tz)
		}
	}

	return results, nil
}

// ==================== DST Handling ====================

// IsDST checks if daylight saving time is active in a timezone
func IsDST(zone string, atTime ...time.Time) (bool, error) {
	tz, err := GetTimezone(zone)
	if err != nil {
		return false, err
	}

	var t time.Time
	if len(atTime) > 0 {
		t = atTime[0]
	} else {
		t = time.Now()
	}

	// Compare offsets in January and July
	jan := time.Date(t.Year(), time.January, 15, 12, 0, 0, 0, tz.Location)
	jul := time.Date(t.Year(), time.July, 15, 12, 0, 0, 0, tz.Location)
	_, janOffset := jan.Zone()
	_, julOffset := jul.Zone()
	_, currentOffset := t.In(tz.Location).Zone()

	// If current offset matches neither Jan nor Jul offset, DST is active
	if currentOffset != janOffset && currentOffset != julOffset {
		return true, nil
	}
	if janOffset != julOffset && currentOffset == janOffset {
		// Northern hemisphere: Jan offset means winter (no DST) if current matches
		// This logic is simplified; actual DST detection is complex
	}

	return currentOffset != janOffset && currentOffset != julOffset, nil
}

// NextDSTChange returns when DST changes next for a timezone
func NextDSTChange(zone string, fromTime ...time.Time) (time.Time, error) {
	tz, err := GetTimezone(zone)
	if err != nil {
		return time.Time{}, err
	}

	var t time.Time
	if len(fromTime) > 0 {
		t = fromTime[0]
	} else {
		t = time.Now()
	}

	// Simplified DST change detection
	// Look for offset changes in the next year
	for i := 0; i < 366; i++ {
		current := t.AddDate(0, 0, i)
		_, currentOffset := current.In(tz.Location).Zone()
		next := current.Add(time.Hour)
		_, nextOffset := next.In(tz.Location).Zone()

		if currentOffset != nextOffset {
			return next, nil
		}
	}

	return time.Time{}, nil
}

// ==================== Scheduling Helpers ====================

// FormatInTimezone formats a time in a specific timezone
func FormatInTimezone(t time.Time, zone, format string) (string, error) {
	tz, err := GetTimezone(zone)
	if err != nil {
		return "", err
	}
	return t.In(tz.Location).Format(format), nil
}

// ParseInTimezone parses a time string in a specific timezone
func ParseInTimezone(timeStr, format, zone string) (time.Time, error) {
	tz, err := GetTimezone(zone)
	if err != nil {
		return time.Time{}, err
	}
	return time.ParseInLocation(format, timeStr, tz.Location)
}

// ==================== Convenience Functions ====================

// GetUTCOffset returns the UTC offset for a timezone as a string
func GetUTCOffset(zone string) (string, error) {
	info, err := GetTimezoneInfo(zone)
	if err != nil {
		return "", err
	}
	return info.OffsetString, nil
}

// IsValidTimezone checks if a timezone name is valid
func IsValidTimezone(zone string) bool {
	_, err := GetTimezone(zone)
	return err == nil
}

// ListTimezones returns all loaded available timezones
func ListTimezones() []string {
	// Return common timezones as not all systems have full timezone data
	return CommonTimezones()
}