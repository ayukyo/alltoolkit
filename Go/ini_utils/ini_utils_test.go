package ini_utils

import (
	"os"
	"path/filepath"
	"testing"
)

func TestNew(t *testing.T) {
	ini := New()
	if ini == nil {
		t.Fatal("New() returned nil")
	}
	if len(ini.sections) != 0 {
		t.Error("New IniFile should have no sections")
	}
}

func TestParse(t *testing.T) {
	input := `[database]
host=localhost
port=3306

[app]
name=test
enabled=true`
	
	ini, err := Parse(input)
	if err != nil {
		t.Fatalf("Parse() error = %v", err)
	}
	
	if ini.Get("database", "host", "") != "localhost" {
		t.Error("Failed to parse database host")
	}
	
	if ini.GetInt("database", "port", 0) != 3306 {
		t.Error("Failed to parse database port")
	}
}

func TestGetSet(t *testing.T) {
	ini := New()
	
	// Test global key
	ini.Set("", "key1", "value1")
	if got := ini.Get("", "key1", ""); got != "value1" {
		t.Errorf("Get() = %v, want value1", got)
	}
	
	// Test section key
	ini.Set("section1", "key2", "value2")
	if got := ini.Get("section1", "key2", ""); got != "value2" {
		t.Errorf("Get() = %v, want value2", got)
	}
	
	// Test default value
	if got := ini.Get("", "nonexistent", "default"); got != "default" {
		t.Errorf("Get() default = %v, want default", got)
	}
}

func TestGetInt(t *testing.T) {
	ini := New()
	ini.Set("", "num", "42")
	
	if got := ini.GetInt("", "num", 0); got != 42 {
		t.Errorf("GetInt() = %v, want 42", got)
	}
	
	// Test invalid int returns default
	ini.Set("", "invalid", "notanumber")
	if got := ini.GetInt("", "invalid", 99); got != 99 {
		t.Errorf("GetInt() invalid = %v, want 99", got)
	}
}

func TestGetBool(t *testing.T) {
	ini := New()
	
	// Test various true values
	trueValues := []string{"true", "yes", "1", "on", "enabled"}
	for _, v := range trueValues {
		ini.Set("", "test", v)
		if !ini.GetBool("", "test", false) {
			t.Errorf("GetBool(%s) should be true", v)
		}
	}
	
	// Test false values
	falseValues := []string{"false", "no", "0", "off", "disabled"}
	for _, v := range falseValues {
		ini.Set("", "test", v)
		if ini.GetBool("", "test", true) {
			t.Errorf("GetBool(%s) should be false", v)
		}
	}
}

func TestHasSection(t *testing.T) {
	ini := New()
	ini.Set("section1", "key", "value")
	
	if !ini.HasSection("section1") {
		t.Error("HasSection() should return true for existing section")
	}
	
	if ini.HasSection("nonexistent") {
		t.Error("HasSection() should return false for nonexistent section")
	}
}

func TestHasKey(t *testing.T) {
	ini := New()
	ini.Set("section1", "key1", "value")
	
	if !ini.HasKey("section1", "key1") {
		t.Error("HasKey() should return true for existing key")
	}
	
	if ini.HasKey("section1", "nonexistent") {
		t.Error("HasKey() should return false for nonexistent key")
	}
}

func TestDeleteKey(t *testing.T) {
	ini := New()
	ini.Set("section1", "key1", "value")
	
	ini.DeleteKey("section1", "key1")
	
	if ini.HasKey("section1", "key1") {
		t.Error("DeleteKey() should remove the key")
	}
}

func TestDeleteSection(t *testing.T) {
	ini := New()
	ini.Set("section1", "key", "value")
	
	ini.DeleteSection("section1")
	
	if ini.HasSection("section1") {
		t.Error("DeleteSection() should remove the section")
	}
}

func TestLoadFileAndSaveToFile(t *testing.T) {
	// Create temp directory
	tempDir := t.TempDir()
	tempFile := filepath.Join(tempDir, "test.ini")
	
	// Create and save
	ini := New()
	ini.Set("database", "host", "localhost")
	ini.Set("database", "port", "3306")
	ini.Set("app", "name", "testapp")
	
	err := ini.SaveToFile(tempFile)
	if err != nil {
		t.Fatalf("SaveToFile() error = %v", err)
	}
	
	// Load and verify
	loaded, err := LoadFile(tempFile)
	if err != nil {
		t.Fatalf("LoadFile() error = %v", err)
	}
	
	if loaded.Get("database", "host", "") != "localhost" {
		t.Error("LoadFile() did not load database host correctly")
	}
	
	if loaded.Get("app", "name", "") != "testapp" {
		t.Error("LoadFile() did not load app name correctly")
	}
}

func TestToString(t *testing.T) {
	ini := New()
	ini.Set("section1", "key1", "value1")
	
	str := ini.ToString()
	if str == "" {
		t.Error("ToString() should not return empty string")
	}
	
	// Should contain the key-value
	if !contains(str, "key1=value1") {
		t.Error("ToString() should contain key1=value1")
	}
}

func TestToPrettyString(t *testing.T) {
	ini := New()
	ini.Set("section1", "key1", "value1")
	ini.Set("section1", "key2", "value2")
	
	str := ini.ToPrettyString()
	if str == "" {
		t.Error("ToPrettyString() should not return empty string")
	}
}

func TestGetSections(t *testing.T) {
	ini := New()
	ini.Set("section1", "key", "value")
	ini.Set("section2", "key", "value")
	
	sections := ini.GetSections()
	if len(sections) != 2 {
		t.Errorf("GetSections() returned %d sections, want 2", len(sections))
	}
}

func TestGetKeys(t *testing.T) {
	ini := New()
	ini.Set("section1", "key1", "value1")
	ini.Set("section1", "key2", "value2")
	
	keys := ini.GetKeys("section1")
	if len(keys) != 2 {
		t.Errorf("GetKeys() returned %d keys, want 2", len(keys))
	}
}

func TestDefaultOptions(t *testing.T) {
	opts := DefaultOptions()
	if opts.Delimiter != "=" {
		t.Errorf("Default Delimiter = %v, want =", opts.Delimiter)
	}
	if opts.CommentChar != ";" {
		t.Errorf("Default CommentChar = %v, want ;", opts.CommentChar)
	}
}

// Helper function
func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(s) > 0 && containsHelper(s, substr))
}

func containsHelper(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}
