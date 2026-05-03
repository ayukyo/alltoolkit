package sitemap_utils

import (
	"bytes"
	"compress/gzip"
	"fmt"
	"io"
	"os"
	"strings"
	"testing"
	"time"
)

func TestNewGenerator(t *testing.T) {
	g := NewGenerator()
	if g == nil {
		t.Fatal("NewGenerator returned nil")
	}
	if g.Count() != 0 {
		t.Errorf("Expected 0 URLs, got %d", g.Count())
	}
	if g.maxURLs != MaxURLsPerSitemap {
		t.Errorf("Expected maxURLs %d, got %d", MaxURLsPerSitemap, g.maxURLs)
	}
}

func TestGeneratorWithOptions(t *testing.T) {
	g := NewGenerator(
		WithMaxURLs(100),
		WithCompression(true),
		WithPrettyPrint(true),
		WithBaseURL("https://example.com"),
	)
	
	if g.maxURLs != 100 {
		t.Errorf("Expected maxURLs 100, got %d", g.maxURLs)
	}
	if !g.compress {
		t.Error("Expected compression enabled")
	}
	if !g.pretty {
		t.Error("Expected pretty print enabled")
	}
	if g.baseURL != "https://example.com" {
		t.Errorf("Expected baseURL 'https://example.com', got '%s'", g.baseURL)
	}
}

func TestAddURL(t *testing.T) {
	g := NewGenerator()
	
	err := g.AddURL(URL{Loc: "https://example.com/page1"})
	if err != nil {
		t.Fatalf("AddURL failed: %v", err)
	}
	
	if g.Count() != 1 {
		t.Errorf("Expected 1 URL, got %d", g.Count())
	}
}

func TestAddEmptyURL(t *testing.T) {
	g := NewGenerator()
	
	err := g.AddURL(URL{Loc: ""})
	if err == nil {
		t.Error("Expected error for empty URL")
	}
}

func TestAddLongURL(t *testing.T) {
	g := NewGenerator()
	
	longURL := "https://example.com/" + strings.Repeat("a", 2100)
	err := g.AddURL(URL{Loc: longURL})
	if err == nil {
		t.Error("Expected error for URL exceeding 2048 characters")
	}
}

func TestAddInvalidPriority(t *testing.T) {
	g := NewGenerator()
	
	priority := -0.5
	err := g.AddURL(URL{Loc: "https://example.com", Priority: &priority})
	if err == nil {
		t.Error("Expected error for invalid priority")
	}
	
	priority = 1.5
	err = g.AddURL(URL{Loc: "https://example.com", Priority: &priority})
	if err == nil {
		t.Error("Expected error for invalid priority")
	}
}

func TestAddURLWithBaseURL(t *testing.T) {
	g := NewGenerator(WithBaseURL("https://example.com"))
	
	err := g.AddURL(URL{Loc: "/page1"})
	if err != nil {
		t.Fatalf("AddURL failed: %v", err)
	}
	
	urls := g.urls
	if len(urls) != 1 {
		t.Fatal("Expected 1 URL")
	}
	
	expected := "https://example.com/page1"
	if urls[0].Loc != expected {
		t.Errorf("Expected '%s', got '%s'", expected, urls[0].Loc)
	}
}

func TestAddURLs(t *testing.T) {
	g := NewGenerator()
	
	urls := []URL{
		{Loc: "https://example.com/page1"},
		{Loc: "https://example.com/page2"},
		{Loc: "https://example.com/page3"},
	}
	
	err := g.AddURLs(urls)
	if err != nil {
		t.Fatalf("AddURLs failed: %v", err)
	}
	
	if g.Count() != 3 {
		t.Errorf("Expected 3 URLs, got %d", g.Count())
	}
}

func TestAddSimpleURL(t *testing.T) {
	g := NewGenerator()
	
	err := g.AddSimpleURL("https://example.com")
	if err != nil {
		t.Fatalf("AddSimpleURL failed: %v", err)
	}
	
	if g.Count() != 1 {
		t.Errorf("Expected 1 URL, got %d", g.Count())
	}
}

func TestAddURLWithDetails(t *testing.T) {
	g := NewGenerator()
	
	now := time.Now()
	err := g.AddURLWithDetails("https://example.com", &now, Daily, 0.8)
	if err != nil {
		t.Fatalf("AddURLWithDetails failed: %v", err)
	}
	
	if g.Count() != 1 {
		t.Errorf("Expected 1 URL, got %d", g.Count())
	}
	
	url := g.urls[0]
	if url.ChangeFreq == nil || *url.ChangeFreq != Daily {
		t.Error("Expected Daily change frequency")
	}
	if url.Priority == nil || *url.Priority != 0.8 {
		t.Error("Expected priority 0.8")
	}
}

func TestToXML(t *testing.T) {
	g := NewGenerator()
	
	now := time.Now()
	priority := 0.9
	freq := Weekly
	
	url := URL{
		Loc:        "https://example.com",
		LastMod:    &now,
		ChangeFreq: &freq,
		Priority:   &priority,
	}
	
	err := g.AddURL(url)
	if err != nil {
		t.Fatalf("AddURL failed: %v", err)
	}
	
	xmlData, err := g.ToXML()
	if err != nil {
		t.Fatalf("ToXML failed: %v", err)
	}
	
	// Verify XML header
	if !strings.HasPrefix(string(xmlData), "<?xml") {
		t.Error("Expected XML header")
	}
	
	// Verify urlset namespace
	if !strings.Contains(string(xmlData), "xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"") {
		t.Error("Expected sitemap namespace")
	}
	
	// Verify URL is present
	if !strings.Contains(string(xmlData), "https://example.com") {
		t.Error("Expected URL in sitemap")
	}
}

func TestToXMLEmpty(t *testing.T) {
	g := NewGenerator()
	
	_, err := g.ToXML()
	if err == nil {
		t.Error("Expected error for empty sitemap")
	}
}

func TestToXMLWithAlternates(t *testing.T) {
	g := NewGenerator()
	
	alternates := []Alternate{
		{Hreflang: "en", Href: "https://example.com/en"},
		{Hreflang: "es", Href: "https://example.com/es"},
	}
	
	err := g.AddAlternateURL("https://example.com", alternates, nil)
	if err != nil {
		t.Fatalf("AddAlternateURL failed: %v", err)
	}
	
	xmlData, err := g.ToXML()
	if err != nil {
		t.Fatalf("ToXML failed: %v", err)
	}
	
	// Verify xhtml namespace is added
	if !strings.Contains(string(xmlData), "xmlns:xhtml=\"http://www.w3.org/1999/xhtml\"") {
		t.Error("Expected xhtml namespace for alternates")
	}
}

func TestToFile(t *testing.T) {
	g := NewGenerator()
	
	err := g.AddURL(URL{Loc: "https://example.com"})
	if err != nil {
		t.Fatalf("AddURL failed: %v", err)
	}
	
	filename := "test_sitemap.xml"
	defer os.Remove(filename)
	
	err = g.ToFile(filename)
	if err != nil {
		t.Fatalf("ToFile failed: %v", err)
	}
	
	// Verify file exists
	if _, err := os.Stat(filename); err != nil {
		t.Errorf("File not created: %v", err)
	}
	
	// Read and verify content
	data, err := os.ReadFile(filename)
	if err != nil {
		t.Fatalf("Failed to read file: %v", err)
	}
	
	if !strings.Contains(string(data), "https://example.com") {
		t.Error("Expected URL in file")
	}
}

func TestToFileGzipped(t *testing.T) {
	g := NewGenerator(WithCompression(true))
	
	err := g.AddURL(URL{Loc: "https://example.com"})
	if err != nil {
		t.Fatalf("AddURL failed: %v", err)
	}
	
	filename := "test_sitemap.xml.gz"
	defer os.Remove(filename)
	
	err = g.ToFile(filename)
	if err != nil {
		t.Fatalf("ToFile failed: %v", err)
	}
	
	// Verify file exists
	if _, err := os.Stat(filename); err != nil {
		t.Errorf("File not created: %v", err)
	}
	
	// Read and decompress
	data, err := os.ReadFile(filename)
	if err != nil {
		t.Fatalf("Failed to read file: %v", err)
	}
	
	gz, err := gzip.NewReader(bytes.NewReader(data))
	if err != nil {
		t.Fatalf("Failed to create gzip reader: %v", err)
	}
	defer gz.Close()
	
	decompressed, err := io.ReadAll(gz)
	if err != nil {
		t.Fatalf("Failed to decompress: %v", err)
	}
	
	if !strings.Contains(string(decompressed), "https://example.com") {
		t.Error("Expected URL in decompressed content")
	}
}

func TestSplit(t *testing.T) {
	g := NewGenerator(WithMaxURLs(3))
	
	for i := 0; i < 10; i++ {
		err := g.AddURL(URL{Loc: fmt.Sprintf("https://example.com/page%d", i)})
		if err != nil {
			// When max is reached, we can't add more - test the split of existing URLs
			break
		}
	}
	
	// With max 3, we should have 3 URLs
	if g.Count() != 3 {
		t.Errorf("Expected 3 URLs (max limit), got %d", g.Count())
	}
	
	split := g.Split()
	// Should be 1 split (3 URLs in one batch)
	if len(split) != 1 {
		t.Errorf("Expected 1 split, got %d", len(split))
	}
	
	if len(split[0]) != 3 {
		t.Errorf("Expected 3 URLs in split, got %d", len(split[0]))
	}
}

func TestClear(t *testing.T) {
	g := NewGenerator()
	
	g.AddURL(URL{Loc: "https://example.com"})
	if g.Count() != 1 {
		t.Fatal("Expected 1 URL before clear")
	}
	
	g.Clear()
	if g.Count() != 0 {
		t.Error("Expected 0 URLs after clear")
	}
}

func TestIndexGenerator(t *testing.T) {
	ig := NewIndexGenerator()
	
	now := time.Now()
	
	err := ig.AddSitemap("https://example.com/sitemap1.xml", &now)
	if err != nil {
		t.Fatalf("AddSitemap failed: %v", err)
	}
	
	err = ig.AddSitemap("https://example.com/sitemap2.xml", nil)
	if err != nil {
		t.Fatalf("AddSitemap failed: %v", err)
	}
	
	if ig.Count() != 2 {
		t.Errorf("Expected 2 sitemaps, got %d", ig.Count())
	}
}

func TestIndexGeneratorToXML(t *testing.T) {
	ig := NewIndexGenerator()
	
	now := time.Now()
	ig.AddSitemap("https://example.com/sitemap1.xml", &now)
	
	xmlData, err := ig.ToXML()
	if err != nil {
		t.Fatalf("ToXML failed: %v", err)
	}
	
	// Verify XML header
	if !strings.HasPrefix(string(xmlData), "<?xml") {
		t.Error("Expected XML header")
	}
	
	// Verify sitemapindex namespace
	if !strings.Contains(string(xmlData), "sitemapindex") {
		t.Error("Expected sitemapindex element")
	}
	
	// Verify sitemap location
	if !strings.Contains(string(xmlData), "https://example.com/sitemap1.xml") {
		t.Error("Expected sitemap location")
	}
}

func TestIndexGeneratorToFile(t *testing.T) {
	ig := NewIndexGenerator()
	
	ig.AddSitemap("https://example.com/sitemap1.xml", nil)
	
	filename := "test_sitemap_index.xml"
	defer os.Remove(filename)
	
	err := ig.ToFile(filename)
	if err != nil {
		t.Fatalf("ToFile failed: %v", err)
	}
	
	if _, err := os.Stat(filename); err != nil {
		t.Errorf("File not created: %v", err)
	}
}

func TestParser(t *testing.T) {
	p := NewParser()
	if p == nil {
		t.Fatal("NewParser returned nil")
	}
}

func TestParserParse(t *testing.T) {
	p := NewParser()
	
	xmlData := []byte(`<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>`)
	
	sitemap, err := p.Parse(xmlData)
	if err != nil {
		t.Fatalf("Parse failed: %v", err)
	}
	
	if len(sitemap.URLs) != 1 {
		t.Errorf("Expected 1 URL, got %d", len(sitemap.URLs))
	}
	
	if sitemap.URLs[0].Loc != "https://example.com" {
		t.Errorf("Expected 'https://example.com', got '%s'", sitemap.URLs[0].Loc)
	}
}

func TestParserParseGzipped(t *testing.T) {
	// Create gzipped sitemap data
	xmlData := []byte(`<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com</loc>
  </url>
</urlset>`)
	
	var buf bytes.Buffer
	gz := gzip.NewWriter(&buf)
	gz.Write(xmlData)
	gz.Close()
	
	p := NewParser()
	sitemap, err := p.Parse(buf.Bytes())
	if err != nil {
		t.Fatalf("Parse failed: %v", err)
	}
	
	if len(sitemap.URLs) != 1 {
		t.Errorf("Expected 1 URL, got %d", len(sitemap.URLs))
	}
}

func TestParserParseFile(t *testing.T) {
	// Create test file
	g := NewGenerator()
	g.AddURL(URL{Loc: "https://example.com"})
	
	filename := "test_parse.xml"
	defer os.Remove(filename)
	
	g.ToFile(filename)
	
	p := NewParser()
	sitemap, err := p.ParseFile(filename)
	if err != nil {
		t.Fatalf("ParseFile failed: %v", err)
	}
	
	if len(sitemap.URLs) != 1 {
		t.Errorf("Expected 1 URL, got %d", len(sitemap.URLs))
	}
}

func TestParserParseIndex(t *testing.T) {
	p := NewParser()
	
	xmlData := []byte(`<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap1.xml</loc>
  </sitemap>
</sitemapindex>`)
	
	sitemaps, err := p.ParseIndex(xmlData)
	if err != nil {
		t.Fatalf("ParseIndex failed: %v", err)
	}
	
	if len(sitemaps) != 1 {
		t.Errorf("Expected 1 sitemap, got %d", len(sitemaps))
	}
	
	if sitemaps[0].Loc != "https://example.com/sitemap1.xml" {
		t.Errorf("Expected 'https://example.com/sitemap1.xml', got '%s'", sitemaps[0].Loc)
	}
}

func TestURLBuilder(t *testing.T) {
	builder := NewURLBuilder("https://example.com")
	
	url := builder.Path("products").Path("item").Param("id", "123").Build()
	expected := "https://example.com/products/item?id=123"
	
	if url != expected {
		t.Errorf("Expected '%s', got '%s'", expected, url)
	}
}

func TestURLBuilderMultipleParams(t *testing.T) {
	builder := NewURLBuilder("https://example.com")
	
	url := builder.Path("search").Param("q", "test").Param("page", "1").Build()
	
	if !strings.HasPrefix(url, "https://example.com/search?") {
		t.Error("Expected base URL and path")
	}
	if !strings.Contains(url, "q=test") {
		t.Error("Expected q parameter")
	}
	if !strings.Contains(url, "page=1") {
		t.Error("Expected page parameter")
	}
}

func TestURLBuilderReset(t *testing.T) {
	builder := NewURLBuilder("https://example.com")
	
	builder.Path("page1").Param("a", "1")
	url1 := builder.Build()
	
	builder.Reset()
	url2 := builder.Path("page2").Build()
	
	if url1 == url2 {
		t.Error("Expected different URLs after reset")
	}
	if strings.Contains(url2, "page1") {
		t.Error("Expected reset to clear paths")
	}
}

func TestBatchGenerator(t *testing.T) {
	bg := NewBatchGenerator(3)
	
	// Add more URLs than max
	for i := 0; i < 10; i++ {
		err := bg.AddURL(URL{Loc: "https://example.com/page" + string(rune('0'+i))})
		if err != nil {
			t.Fatalf("AddURL failed: %v", err)
		}
	}
	
	// Should have 4 sitemaps (3 full + 1 with 1 URL)
	if bg.SitemapCount() != 4 {
		t.Errorf("Expected 4 sitemaps, got %d", bg.SitemapCount())
	}
	
	// Total should be 10
	if bg.TotalCount() != 10 {
		t.Errorf("Expected 10 total URLs, got %d", bg.TotalCount())
	}
}

func TestBatchGeneratorToFiles(t *testing.T) {
	bg := NewBatchGenerator(2)
	
	bg.AddURL(URL{Loc: "https://example.com/page1"})
	bg.AddURL(URL{Loc: "https://example.com/page2"})
	bg.AddURL(URL{Loc: "https://example.com/page3"})
	
	filenames, err := bg.ToFiles("test_batch")
	if err != nil {
		t.Fatalf("ToFiles failed: %v", err)
	}
	
	defer func() {
		for _, f := range filenames {
			os.Remove(f)
		}
	}()
	
	if len(filenames) != 2 {
		t.Errorf("Expected 2 files, got %d", len(filenames))
	}
	
	for _, f := range filenames {
		if _, err := os.Stat(f); err != nil {
			t.Errorf("File %s not created", f)
		}
	}
}

func TestBatchGeneratorCreateIndex(t *testing.T) {
	bg := NewBatchGenerator(2, WithBaseURL("https://example.com"))
	
	bg.AddURL(URL{Loc: "/page1"})
	bg.AddURL(URL{Loc: "/page2"})
	bg.AddURL(URL{Loc: "/page3"})
	
	indexXML, err := bg.CreateIndex("https://example.com/sitemap")
	if err != nil {
		t.Fatalf("CreateIndex failed: %v", err)
	}
	
	// Verify index contains 2 sitemap references
	if !strings.Contains(string(indexXML), "sitemap-1.xml") {
		t.Error("Expected sitemap-1.xml reference")
	}
	if !strings.Contains(string(indexXML), "sitemap-2.xml") {
		t.Error("Expected sitemap-2.xml reference")
	}
}

func TestMaxURLsLimit(t *testing.T) {
	g := NewGenerator(WithMaxURLs(3))
	
	// Add URLs up to limit
	for i := 0; i < 3; i++ {
		err := g.AddURL(URL{Loc: "https://example.com/page" + string(rune('0'+i))})
		if err != nil {
			t.Fatalf("AddURL failed: %v", err)
		}
	}
	
	// Try to add one more (should fail)
	err := g.AddURL(URL{Loc: "https://example.com/page4"})
	if err == nil {
		t.Error("Expected error when exceeding max URLs")
	}
}

func TestChangeFreqConstants(t *testing.T) {
	frequencies := []ChangeFreq{Always, Hourly, Daily, Weekly, Monthly, Yearly, Never}
	
	expected := []string{"always", "hourly", "daily", "weekly", "monthly", "yearly", "never"}
	
	for i, freq := range frequencies {
		if string(freq) != expected[i] {
			t.Errorf("Expected '%s', got '%s'", expected[i], string(freq))
		}
	}
}

func TestPrettyPrint(t *testing.T) {
	g := NewGenerator(WithPrettyPrint(true))
	
	g.AddURL(URL{Loc: "https://example.com/page1"})
	g.AddURL(URL{Loc: "https://example.com/page2"})
	
	xmlData, err := g.ToXML()
	if err != nil {
		t.Fatalf("ToXML failed: %v", err)
	}
	
	// Pretty printed XML should have indentation
	if !bytes.Contains(xmlData, []byte("  <url>")) {
		t.Error("Expected indented XML elements")
	}
}

func TestToWriter(t *testing.T) {
	g := NewGenerator()
	
	g.AddURL(URL{Loc: "https://example.com"})
	
	var buf bytes.Buffer
	err := g.ToWriter(&buf)
	if err != nil {
		t.Fatalf("ToWriter failed: %v", err)
	}
	
	if !strings.Contains(buf.String(), "https://example.com") {
		t.Error("Expected URL in output")
	}
}

func TestToWriterGzipped(t *testing.T) {
	g := NewGenerator(WithCompression(true))
	
	g.AddURL(URL{Loc: "https://example.com"})
	
	var buf bytes.Buffer
	err := g.ToWriter(&buf)
	if err != nil {
		t.Fatalf("ToWriter failed: %v", err)
	}
	
	// Should be gzip compressed (starts with gzip magic bytes)
	data := buf.Bytes()
	if len(data) < 2 || data[0] != 0x1f || data[1] != 0x8b {
		t.Error("Expected gzip compressed output")
	}
}

func TestInvalidMaxURLs(t *testing.T) {
	// Test negative max URLs (should use default)
	g := NewGenerator(WithMaxURLs(-1))
	if g.maxURLs != MaxURLsPerSitemap {
		t.Errorf("Expected default maxURLs for negative value")
	}
	
	// Test too large max URLs (should use default)
	g = NewGenerator(WithMaxURLs(100000))
	if g.maxURLs != MaxURLsPerSitemap {
		t.Errorf("Expected default maxURLs for too large value")
	}
}

func TestWhitespaceTrimming(t *testing.T) {
	g := NewGenerator()
	
	err := g.AddURL(URL{Loc: "  https://example.com/page  "})
	if err != nil {
		t.Fatalf("AddURL failed: %v", err)
	}
	
	// URL should be trimmed
	if g.urls[0].Loc != "https://example.com/page" {
		t.Errorf("Expected trimmed URL, got '%s'", g.urls[0].Loc)
	}
}