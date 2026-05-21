package url_utils

import (
	"testing"
)

func TestParse(t *testing.T) {
	tests := []struct {
		name         string
		input        string
		wantScheme   string
		wantHost     string
		wantPath     string
		wantErr      bool
	}{
		{"Simple HTTP", "http://example.com", "http", "example.com", "/", false},
		{"Simple HTTPS", "https://example.com", "https", "example.com", "/", false},
		{"With path", "https://example.com/path/to/resource", "https", "example.com", "/path/to/resource", false},
		{"With query", "https://example.com?key=value", "https", "example.com", "/", false},
		{"With fragment", "https://example.com#section", "https", "example.com", "/", false},
		{"With port", "https://example.com:8080", "https", "example.com", "/", false},
		{"No scheme", "example.com", "http", "example.com", "/", false},
		{"Subdomain", "https://sub.example.com", "https", "sub.example.com", "/", false},
		{"IPv4", "http://192.168.1.1", "http", "192.168.1.1", "/", false},
		{"IPv4 with port", "http://192.168.1.1:8080", "http", "192.168.1.1", "/", false},
		{"Empty", "", "", "", "", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			info, err := Parse(tt.input)
			if tt.wantErr {
				if err == nil {
					t.Error("Parse() expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("Parse() unexpected error: %v", err)
				return
			}
			if info.Scheme != tt.wantScheme {
				t.Errorf("Parse().Scheme = %v, want %v", info.Scheme, tt.wantScheme)
			}
			if info.Host != tt.wantHost {
				t.Errorf("Parse().Host = %v, want %v", info.Host, tt.wantHost)
			}
			if info.Path != tt.wantPath {
				t.Errorf("Parse().Path = %v, want %v", info.Path, tt.wantPath)
			}
		})
	}
}

func TestNormalize(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		want     string
	}{
		{"Lowercase scheme", "HTTP://example.com", "http://example.com"},
		{"Lowercase host", "http://Example.COM", "http://example.com"},
		{"Remove default port HTTP", "http://example.com:80", "http://example.com"},
		{"Remove default port HTTPS", "https://example.com:443", "https://example.com"},
		{"Remove trailing slash", "http://example.com/", "http://example.com"},
		{"Remove duplicate slashes", "http://example.com//path///test", "http://example.com/path/test"},
		{"Remove trailing slash and sort query", "http://example.com/?b=2&a=1", "http://example.com?a=1&b=2"},
		{"Keep non-default port", "http://example.com:8080", "http://example.com:8080"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := Normalize(tt.input)
			if err != nil {
				t.Errorf("Normalize() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("Normalize() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestNormalizeWithOptions(t *testing.T) {
	// Test remove www (with trailing slash removal too for consistent behavior)
	got, err := NormalizeWithOptions("http://www.example.com/", NormalizeOptions{NormalizeRemoveWWW, NormalizeRemoveTrailingSlash})
	if err != nil {
		t.Errorf("NormalizeWithOptions() error: %v", err)
	}
	if got != "http://example.com" {
		t.Errorf("NormalizeWithOptions() remove www = %v, want http://example.com", got)
	}

	// Test add www (adds trailing slash by default for root path)
	got, err = NormalizeWithOptions("http://example.com", NormalizeOptions{NormalizeAddWWW})
	if err != nil {
		t.Errorf("NormalizeWithOptions() error: %v", err)
	}
	if got != "http://www.example.com" {
		t.Errorf("NormalizeWithOptions() add www = %v, want http://www.example.com", got)
	}

	// Test remove fragment
	got, err = NormalizeWithOptions("http://example.com/#section", NormalizeOptions{NormalizeRemoveFragment, NormalizeRemoveTrailingSlash})
	if err != nil {
		t.Errorf("NormalizeWithOptions() error: %v", err)
	}
	if got != "http://example.com" {
		t.Errorf("NormalizeWithOptions() remove fragment = %v, want http://example.com", got)
	}

	// Test remove index.html
	got, err = NormalizeWithOptions("http://example.com/index.html", NormalizeOptions{NormalizeRemoveIndexPage, NormalizeRemoveTrailingSlash})
	if err != nil {
		t.Errorf("NormalizeWithOptions() error: %v", err)
	}
	if got != "http://example.com" {
		t.Errorf("NormalizeWithOptions() remove index = %v, want http://example.com", got)
	}

	// Test remove UTM params
	got, err = NormalizeWithOptions("http://example.com/?utm_source=google&id=123", NormalizeOptions{NormalizeRemoveUTM, NormalizeRemoveTrailingSlash})
	if err != nil {
		t.Errorf("NormalizeWithOptions() error: %v", err)
	}
	if got != "http://example.com?id=123" {
		t.Errorf("NormalizeWithOptions() remove UTM = %v, want http://example.com?id=123", got)
	}

	// Test add trailing slash
	got, err = NormalizeWithOptions("http://example.com/path", NormalizeOptions{NormalizeAddTrailingSlash})
	if err != nil {
		t.Errorf("NormalizeWithOptions() error: %v", err)
	}
	if got != "http://example.com/path/" {
		t.Errorf("NormalizeWithOptions() add trailing slash = %v, want http://example.com/path/", got)
	}
}

func TestValidate(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  bool
	}{
		{"Valid HTTP", "http://example.com", true},
		{"Valid HTTPS", "https://example.com", true},
		{"Valid with path", "https://example.com/path", true},
		{"Valid with query", "https://example.com?key=value", true},
		{"Invalid empty", "", false},
		{"Invalid no host", "http://", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := Validate(tt.input)
			got := err == nil
			if got != tt.want {
				t.Errorf("Validate() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestIsValidHTTP(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  bool
	}{
		{"Valid HTTP", "http://example.com", true},
		{"Valid HTTPS", "https://example.com", true},
		{"Invalid FTP", "ftp://example.com", false},
		{"Invalid empty", "", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := IsValidHTTP(tt.input); got != tt.want {
				t.Errorf("IsValidHTTP() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestResolve(t *testing.T) {
	tests := []struct {
		name     string
		base     string
		relative string
		want     string
	}{
		{"Relative path", "https://example.com", "/path", "https://example.com/path"},
		{"Relative path with base path", "https://example.com/base/", "../path", "https://example.com/path"},
		{"Absolute URL", "https://example.com", "https://other.com", "https://other.com"},
		{"Query only", "https://example.com/path", "?query=value", "https://example.com/path?query=value"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := Resolve(tt.base, tt.relative)
			if err != nil {
				t.Errorf("Resolve() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("Resolve() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestJoin(t *testing.T) {
	tests := []struct {
		name      string
		base      string
		segments  []string
		want      string
	}{
		{"Single segment", "https://example.com", []string{"path"}, "https://example.com/path"},
		{"Multiple segments", "https://example.com", []string{"a", "b", "c"}, "https://example.com/a/b/c"},
		{"With base path", "https://example.com/base", []string{"path"}, "https://example.com/base/path"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := Join(tt.base, tt.segments...)
			if err != nil {
				t.Errorf("Join() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("Join() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestQueryBuilder(t *testing.T) {
	qb := NewQueryBuilder()
	qb.Add("key1", "value1")
	qb.Add("key2", "value2")
	qb.Add("key1", "value3")

	result := qb.Build()
	if result == "" {
		t.Error("QueryBuilder.Build() returned empty string")
	}

	// Test Get
	if qb.Get("key1") != "value1" {
		t.Errorf("QueryBuilder.Get() = %v, want value1", qb.Get("key1"))
	}

	// Test GetAll
	all := qb.GetAll("key1")
	if len(all) != 2 {
		t.Errorf("QueryBuilder.GetAll() length = %v, want 2", len(all))
	}

	// Test Has
	if !qb.Has("key1") {
		t.Error("QueryBuilder.Has() = false, want true")
	}

	// Test Set
	qb.Set("key1", "newvalue")
	if qb.Get("key1") != "newvalue" {
		t.Errorf("QueryBuilder.Set() failed, got %v, want newvalue", qb.Get("key1"))
	}

	// Test Del
	qb.Del("key1")
	if qb.Has("key1") {
		t.Error("QueryBuilder.Del() failed, key still exists")
	}

	// Test BuildSorted
	qb = NewQueryBuilder()
	qb.Add("z", "1")
	qb.Add("a", "2")
	qb.Add("m", "3")
	sorted := qb.BuildSorted()
	if sorted != "a=2&m=3&z=1" {
		t.Errorf("QueryBuilder.BuildSorted() = %v, want a=2&m=3&z=1", sorted)
	}
}

func TestParseQuery(t *testing.T) {
	qb, err := ParseQuery("key1=value1&key2=value2")
	if err != nil {
		t.Errorf("ParseQuery() error: %v", err)
		return
	}

	if qb.Get("key1") != "value1" {
		t.Errorf("ParseQuery().Get() = %v, want value1", qb.Get("key1"))
	}
}

func TestURLBuilder(t *testing.T) {
	// Build from scratch
	url := NewURLBuilder().
		SetScheme("https").
		SetHost("example.com").
		SetPath("/api/v1").
		AddQueryParam("key", "value").
		SetFragment("section").
		Build()

	if url == "" {
		t.Error("URLBuilder.Build() returned empty string")
	}

	// Verify components
	info, err := Parse(url)
	if err != nil {
		t.Errorf("Parse built URL error: %v", err)
		return
	}

	if info.Scheme != "https" {
		t.Errorf("URLBuilder scheme = %v, want https", info.Scheme)
	}
	if info.Host != "example.com" {
		t.Errorf("URLBuilder host = %v, want example.com", info.Host)
	}
	if info.Path != "/api/v1" {
		t.Errorf("URLBuilder path = %v, want /api/v1", info.Path)
	}
	if info.Fragment != "section" {
		t.Errorf("URLBuilder fragment = %v, want section", info.Fragment)
	}
}

func TestURLBuilderWithAuth(t *testing.T) {
	url := NewURLBuilder().
		SetScheme("https").
		SetHost("example.com").
		SetUser("user").
		SetPassword("pass").
		Build()

	if url == "" {
		t.Error("URLBuilder.Build() returned empty string")
	}

	info, err := Parse(url)
	if err != nil {
		t.Errorf("Parse built URL error: %v", err)
		return
	}

	if info.User != "user" {
		t.Errorf("URLBuilder user = %v, want user", info.User)
	}
	if info.Password != "pass" {
		t.Errorf("URLBuilder password = %v, want pass", info.Password)
	}
}

func TestFromURL(t *testing.T) {
	builder, err := FromURL("https://example.com:8080/path?key=value#section")
	if err != nil {
		t.Errorf("FromURL() error: %v", err)
		return
	}

	url := builder.Build()
	if url == "" {
		t.Error("FromURL().Build() returned empty string")
	}

	info, _ := Parse(url)
	if info.Scheme != "https" {
		t.Errorf("FromURL scheme = %v, want https", info.Scheme)
	}
	if info.Host != "example.com" {
		t.Errorf("FromURL host = %v, want example.com", info.Host)
	}
	if info.Port != "8080" {
		t.Errorf("FromURL port = %v, want 8080", info.Port)
	}
}

func TestEquals(t *testing.T) {
	tests := []struct {
		name  string
		url1  string
		url2  string
		want  bool
	}{
		{"Same URL", "http://example.com", "http://example.com", true},
		{"Different case scheme", "HTTP://example.com", "http://example.com", true},
		{"Different case host", "http://Example.COM", "http://example.com", true},
		{"Different default port", "http://example.com:80", "http://example.com", true},
		{"Different trailing slash", "http://example.com/", "http://example.com", true},
		{"Different hosts", "http://example.com", "http://other.com", false},
		{"Different schemes", "http://example.com", "https://example.com", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := Equals(tt.url1, tt.url2)
			if err != nil {
				t.Errorf("Equals() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("Equals() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestExtractDomain(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{"Simple domain", "https://example.com/path", "example.com"},
		{"With subdomain", "https://sub.example.com/path", "example.com"},
		{"Multiple subdomains", "https://a.b.c.example.com/path", "example.com"},
		{"IPv4", "http://192.168.1.1", "192.168.1.1"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ExtractDomain(tt.input)
			if err != nil {
				t.Errorf("ExtractDomain() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("ExtractDomain() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestExtractSubdomain(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{"No subdomain", "https://example.com", ""},
		{"One subdomain", "https://sub.example.com", "sub"},
		{"Multiple subdomains", "https://a.b.c.example.com", "a.b.c"},
		{"WWW", "https://www.example.com", "www"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ExtractSubdomain(tt.input)
			if err != nil {
				t.Errorf("ExtractSubdomain() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("ExtractSubdomain() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestExtractPath(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{"Root path", "https://example.com", "/"},
		{"Simple path", "https://example.com/path", "/path"},
		{"Nested path", "https://example.com/a/b/c", "/a/b/c"},
		{"With query", "https://example.com/path?key=value", "/path"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ExtractPath(tt.input)
			if err != nil {
				t.Errorf("ExtractPath() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("ExtractPath() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestExtractQuery(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{"No query", "https://example.com", ""},
		{"Simple query", "https://example.com?key=value", "key=value"},
		{"Multiple params", "https://example.com?a=1&b=2", "a=1&b=2"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ExtractQuery(tt.input)
			if err != nil {
				t.Errorf("ExtractQuery() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("ExtractQuery() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestQueryParamOperations(t *testing.T) {
	// Test GetQueryParam
	val, err := GetQueryParam("https://example.com?key=value", "key")
	if err != nil {
		t.Errorf("GetQueryParam() error: %v", err)
	}
	if val != "value" {
		t.Errorf("GetQueryParam() = %v, want value", val)
	}

	// Test SetQueryParam
	url, err := SetQueryParam("https://example.com?key=old", "key", "new")
	if err != nil {
		t.Errorf("SetQueryParam() error: %v", err)
	}
	val, _ = GetQueryParam(url, "key")
	if val != "new" {
		t.Errorf("SetQueryParam() result = %v, want new", val)
	}

	// Test AddQueryParam
	url, err = AddQueryParam("https://example.com?key=val1", "key", "val2")
	if err != nil {
		t.Errorf("AddQueryParam() error: %v", err)
	}
	vals, _ := GetQueryParams(url, "key")
	if len(vals) != 2 {
		t.Errorf("AddQueryParam() result length = %v, want 2", len(vals))
	}

	// Test RemoveQueryParam
	url, err = RemoveQueryParam("https://example.com?key=value&other=test", "key")
	if err != nil {
		t.Errorf("RemoveQueryParam() error: %v", err)
	}
	val, _ = GetQueryParam(url, "key")
	if val != "" {
		t.Errorf("RemoveQueryParam() key still exists")
	}
}

func TestIsSameDomain(t *testing.T) {
	tests := []struct {
		name  string
		url1  string
		url2  string
		want  bool
	}{
		{"Same domain", "https://example.com", "https://example.com/path", true},
		{"Subdomain same root", "https://sub.example.com", "https://example.com", true},
		{"Different domain", "https://example.com", "https://other.com", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := IsSameDomain(tt.url1, tt.url2)
			if err != nil {
				t.Errorf("IsSameDomain() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("IsSameDomain() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestIsSameHost(t *testing.T) {
	tests := []struct {
		name  string
		url1  string
		url2  string
		want  bool
	}{
		{"Same host", "https://example.com", "https://example.com/path", true},
		{"Different subdomain", "https://sub.example.com", "https://example.com", false},
		{"Different host", "https://example.com", "https://other.com", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := IsSameHost(tt.url1, tt.url2)
			if err != nil {
				t.Errorf("IsSameHost() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("IsSameHost() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestToHTTPS(t *testing.T) {
	url, err := ToHTTPS("http://example.com/path")
	if err != nil {
		t.Errorf("ToHTTPS() error: %v", err)
		return
	}
	if url != "https://example.com/path" {
		t.Errorf("ToHTTPS() = %v, want https://example.com/path", url)
	}
}

func TestToHTTP(t *testing.T) {
	url, err := ToHTTP("https://example.com/path")
	if err != nil {
		t.Errorf("ToHTTP() error: %v", err)
		return
	}
	if url != "http://example.com/path" {
		t.Errorf("ToHTTP() = %v, want http://example.com/path", url)
	}
}

func TestIsSecure(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  bool
	}{
		{"HTTPS", "https://example.com", true},
		{"HTTP", "http://example.com", false},
		{"Invalid", "not-a-url", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := IsSecure(tt.input); got != tt.want {
				t.Errorf("IsSecure() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestAddTimestamp(t *testing.T) {
	url, err := AddTimestamp("https://example.com/path")
	if err != nil {
		t.Errorf("AddTimestamp() error: %v", err)
		return
	}

	val, err := GetQueryParam(url, "_t")
	if err != nil {
		t.Errorf("GetQueryParam() error: %v", err)
		return
	}
	if val == "" {
		t.Error("AddTimestamp() did not add timestamp")
	}
}

func TestAddCacheBuster(t *testing.T) {
	url, err := AddCacheBuster("https://example.com/path")
	if err != nil {
		t.Errorf("AddCacheBuster() error: %v", err)
		return
	}

	val, err := GetQueryParam(url, "_cb")
	if err != nil {
		t.Errorf("GetQueryParam() error: %v", err)
		return
	}
	if val == "" {
		t.Error("AddCacheBuster() did not add cache buster")
	}
}

func TestGetFileExtension(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{"HTML", "https://example.com/page.html", "html"},
		{"JS", "https://example.com/script.js", "js"},
		{"CSS", "https://example.com/styles.css", "css"},
		{"No extension", "https://example.com/path", ""},
		{"With query", "https://example.com/image.png?v=1", "png"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := GetFileExtension(tt.input)
			if err != nil {
				t.Errorf("GetFileExtension() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("GetFileExtension() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestRemoveFileExtension(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{"HTML", "https://example.com/page.html", "https://example.com/page"},
		{"JS", "https://example.com/script.js", "https://example.com/script"},
		{"No extension", "https://example.com/path", "https://example.com/path"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := RemoveFileExtension(tt.input)
			if err != nil {
				t.Errorf("RemoveFileExtension() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("RemoveFileExtension() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestClean(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{"Remove UTM", "https://example.com?utm_source=google&id=123#section", "https://example.com?id=123"},
		{"Remove index.html", "https://example.com/index.html", "https://example.com"},
		{"Clean everything", "HTTPS://Example.COM:443//path?utm_source=x#frag", "https://example.com/path"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := Clean(tt.input)
			if err != nil {
				t.Errorf("Clean() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("Clean() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestCanonical(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{"Simple", "HTTP://EXAMPLE.COM/", "http://example.com"},
		{"With query", "http://example.com/?b=2&a=1", "http://example.com?a=1&b=2"},
		{"With UTM", "http://example.com/?utm_source=google&id=1", "http://example.com?id=1"},
		{"With index", "http://example.com/index.html", "http://example.com"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := Canonical(tt.input)
			if err != nil {
				t.Errorf("Canonical() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("Canonical() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestCompare(t *testing.T) {
	tests := []struct {
		name          string
		url1          string
		url2          string
		wantDiffCount int
	}{
		{"Same URL", "https://example.com", "https://example.com", 0},
		{"Different scheme", "http://example.com", "https://example.com", 1},
		{"Different host", "https://example.com", "https://other.com", 1},
		{"Different path", "https://example.com/a", "https://example.com/b", 1},
		{"Different query", "https://example.com?a=1", "https://example.com?b=2", 1},
		{"Different fragment", "https://example.com#a", "https://example.com#b", 1},
		{"All different", "http://a.com/a?a=1#a", "https://b.com/b?b=2#b", 5},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			diff, err := Compare(tt.url1, tt.url2)
			if err != nil {
				t.Errorf("Compare() error: %v", err)
				return
			}

			diffCount := 0
			if diff.SchemeDiff {
				diffCount++
			}
			if diff.HostDiff {
				diffCount++
			}
			if diff.PathDiff {
				diffCount++
			}
			if diff.QueryDiff {
				diffCount++
			}
			if diff.FragmentDiff {
				diffCount++
			}

			if diffCount != tt.wantDiffCount {
				t.Errorf("Compare() diff count = %v, want %v", diffCount, tt.wantDiffCount)
			}
		})
	}
}

func TestIsUUID(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  bool
	}{
		{"With UUID", "https://example.com/users/550e8400-e29b-41d4-a716-446655440000", true},
		{"No UUID", "https://example.com/users/123", false},
		{"UUID in middle", "https://example.com/550e8400-e29b-41d4-a716-446655440000/profile", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := IsUUID(tt.input); got != tt.want {
				t.Errorf("IsUUID() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestIsSlug(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  bool
	}{
		{"Valid slug", "https://example.com/blog/my-awesome-post", true},
		{"Numbers only (valid)", "https://example.com/blog/123", true},
		{"With uppercase", "https://example.com/blog/My-Post", false},
		{"With special chars", "https://example.com/blog/test@invalid", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := IsSlug(tt.input); got != tt.want {
				t.Errorf("IsSlug() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestExtractFragment(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{"With fragment", "https://example.com#section", "section"},
		{"No fragment", "https://example.com", ""},
		{"Nested fragment", "https://example.com/path#section-1", "section-1"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ExtractFragment(tt.input)
			if err != nil {
				t.Errorf("ExtractFragment() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("ExtractFragment() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestGetScheme(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{"HTTP", "http://example.com", "http"},
		{"HTTPS", "https://example.com", "https"},
		{"FTP", "ftp://example.com", "ftp"},
		{"No scheme", "example.com", "http"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := GetScheme(tt.input)
			if err != nil {
				t.Errorf("GetScheme() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("GetScheme() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestGetHost(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{"Simple", "https://example.com", "example.com"},
		{"With port", "https://example.com:8080", "example.com"},
		{"Subdomain", "https://sub.example.com", "sub.example.com"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := GetHost(tt.input)
			if err != nil {
				t.Errorf("GetHost() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("GetHost() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestGetPort(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{"Default port", "https://example.com", ""},
		{"Custom port", "https://example.com:8080", "8080"},
		{"HTTP default", "http://example.com:80", ""},
		{"HTTP custom", "http://example.com:3000", "3000"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := GetPort(tt.input)
			if err != nil {
				t.Errorf("GetPort() error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("GetPort() = %v, want %v", got, tt.want)
			}
		})
	}
}

// Benchmarks
func BenchmarkNormalize(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Normalize("https://WWW.Example.COM:443/path/to/resource/?utm_source=google&key=value&a=1&b=2#section")
	}
}

func BenchmarkParse(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Parse("https://user:pass@example.com:8080/path?query=value#fragment")
	}
}

func BenchmarkQueryBuilder(b *testing.B) {
	for i := 0; i < b.N; i++ {
		qb := NewQueryBuilder()
		qb.Add("key1", "value1")
		qb.Add("key2", "value2")
		qb.Add("key3", "value3")
		qb.Build()
	}
}

func BenchmarkURLBuilder(b *testing.B) {
	for i := 0; i < b.N; i++ {
		NewURLBuilder().
			SetScheme("https").
			SetHost("example.com").
			SetPath("/api/v1/resource").
			AddQueryParam("key1", "value1").
			AddQueryParam("key2", "value2").
			SetFragment("section").
			Build()
	}
}

func BenchmarkCanonical(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Canonical("HTTPS://WWW.EXAMPLE.COM:443/path/?utm_source=x&id=123&a=2&b=1#section")
	}
}