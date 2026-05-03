// Package sitemap_utils provides a zero-dependency sitemap generator for Go.
// Supports standard XML sitemaps, sitemap indexes, and multi-language URLs.
// Complies with sitemap.org protocol specification.
//
// Author: AllToolkit
// Date: 2026-05-04
package sitemap_utils

import (
	"bytes"
	"compress/gzip"
	"encoding/xml"
	"fmt"
	"io"
	"os"
	"strings"
	"time"
)

// Constants for sitemap limits (per sitemap.org spec)
const (
	MaxURLsPerSitemap   = 50000
	MaxSitemapSize      = 50 * 1024 * 1024 // 50 MB uncompressed
	MaxSitemapsPerIndex = 50000
)

// ChangeFreq represents how frequently a URL is likely to change
type ChangeFreq string

const (
	Always    ChangeFreq = "always"
	Hourly    ChangeFreq = "hourly"
	Daily     ChangeFreq = "daily"
	Weekly    ChangeFreq = "weekly"
	Monthly   ChangeFreq = "monthly"
	Yearly    ChangeFreq = "yearly"
	Never     ChangeFreq = "never"
)

// URL represents a single URL entry in a sitemap
type URL struct {
	Loc        string      `xml:"loc"`                   // Required: URL location (max 2048 chars)
	LastMod    *time.Time  `xml:"lastmod,omitempty"`     // Optional: Last modification time
	ChangeFreq *ChangeFreq `xml:"changefreq,omitempty"`  // Optional: Change frequency
	Priority   *float64    `xml:"priority,omitempty"`    // Optional: Priority (0.0 to 1.0)
	Alternates []Alternate `xml:"xhtml:link,omitempty"` // Optional: Alternate language versions
}

// Alternate represents an alternate language version of a URL
type Alternate struct {
	Hreflang string `xml:"hreflang,attr"`
	Href     string `xml:"href,attr"`
}

// Sitemap represents a collection of URLs
type Sitemap struct {
	URLs []URL `xml:"url"`
}

// sitemapXML is the XML structure for a sitemap
type sitemapXML struct {
	XMLName xml.Name `xml:"urlset"`
	Xmlns   string   `xml:"xmlns,attr"`
	URLs    []URL    `xml:"url"`
}

// sitemapIndexXML is the XML structure for a sitemap index
type sitemapIndexXML struct {
	XMLName  xml.Name `xml:"sitemapindex"`
	Xmlns    string   `xml:"xmlns,attr"`
	Sitemaps []sitemapEntry `xml:"sitemap"`
}

// sitemapEntry represents a sitemap entry in the index
type sitemapEntry struct {
	Loc     string     `xml:"loc"`
	LastMod *time.Time `xml:"lastmod,omitempty"`
}

// Generator creates and manages sitemaps
type Generator struct {
	urls       []URL
	maxURLs    int
	compress   bool
	pretty     bool
	baseURL    string
}

// GeneratorOption configures the generator
type GeneratorOption func(*Generator)

// NewGenerator creates a new sitemap generator
func NewGenerator(opts ...GeneratorOption) *Generator {
	g := &Generator{
		urls:    make([]URL, 0),
		maxURLs: MaxURLsPerSitemap,
		compress: false,
		pretty:   false,
		baseURL:  "",
	}
	for _, opt := range opts {
		opt(g)
	}
	return g
}

// WithMaxURLs sets the maximum URLs per sitemap
func WithMaxURLs(max int) GeneratorOption {
	return func(g *Generator) {
		if max > 0 && max <= MaxURLsPerSitemap {
			g.maxURLs = max
		}
	}
}

// WithCompression enables gzip compression
func WithCompression(enable bool) GeneratorOption {
	return func(g *Generator) {
		g.compress = enable
	}
}

// WithPrettyPrint enables pretty XML formatting
func WithPrettyPrint(enable bool) GeneratorOption {
	return func(g *Generator) {
		g.pretty = enable
	}
}

// WithBaseURL sets the base URL for relative paths
func WithBaseURL(baseURL string) GeneratorOption {
	return func(g *Generator) {
		g.baseURL = strings.TrimSuffix(baseURL, "/")
	}
}

// AddURL adds a single URL to the sitemap
func (g *Generator) AddURL(url URL) error {
	if len(g.urls) >= g.maxURLs {
		return fmt.Errorf("maximum URLs (%d) reached", g.maxURLs)
	}
	
	// Validate and normalize URL
	loc := strings.TrimSpace(url.Loc)
	if loc == "" {
		return fmt.Errorf("URL location cannot be empty")
	}
	if len(loc) > 2048 {
		return fmt.Errorf("URL location exceeds 2048 characters")
	}
	
	// Prepend base URL if URL is relative
	if g.baseURL != "" && !strings.HasPrefix(loc, "http://") && !strings.HasPrefix(loc, "https://") {
		loc = g.baseURL + "/" + strings.TrimPrefix(loc, "/")
	}
	
	// Validate priority
	if url.Priority != nil {
		if *url.Priority < 0 || *url.Priority > 1 {
			return fmt.Errorf("priority must be between 0.0 and 1.0")
		}
	}
	
	url.Loc = loc
	g.urls = append(g.urls, url)
	return nil
}

// AddURLs adds multiple URLs to the sitemap
func (g *Generator) AddURLs(urls []URL) error {
	for _, u := range urls {
		if err := g.AddURL(u); err != nil {
			return err
		}
	}
	return nil
}

// AddSimpleURL adds a URL with just the location
func (g *Generator) AddSimpleURL(loc string) error {
	return g.AddURL(URL{Loc: loc})
}

// AddURLWithDetails adds a URL with full details
func (g *Generator) AddURLWithDetails(loc string, lastMod *time.Time, freq ChangeFreq, priority float64) error {
	url := URL{
		Loc:        loc,
		LastMod:    lastMod,
		ChangeFreq: &freq,
		Priority:   &priority,
	}
	return g.AddURL(url)
}

// AddAlternateURL adds a URL with alternate language versions
func (g *Generator) AddAlternateURL(loc string, alternates []Alternate, lastMod *time.Time) error {
	url := URL{
		Loc:        loc,
		LastMod:    lastMod,
		Alternates: alternates,
	}
	return g.AddURL(url)
}

// Count returns the number of URLs in the generator
func (g *Generator) Count() int {
	return len(g.urls)
}

// Clear removes all URLs from the generator
func (g *Generator) Clear() {
	g.urls = make([]URL, 0)
}

// ToXML generates the sitemap XML
func (g *Generator) ToXML() ([]byte, error) {
	if len(g.urls) == 0 {
		return nil, fmt.Errorf("no URLs in sitemap")
	}
	
	sitemap := sitemapXML{
		Xmlns: "http://www.sitemaps.org/schemas/sitemap/0.9",
		URLs:  g.urls,
	}
	
	var output []byte
	var err error
	
	if g.pretty {
		output, err = xml.MarshalIndent(sitemap, "", "  ")
	} else {
		output, err = xml.Marshal(sitemap)
	}
	
	if err != nil {
		return nil, fmt.Errorf("failed to marshal sitemap: %w", err)
	}
	
	// Add XML header
	header := []byte(`<?xml version="1.0" encoding="UTF-8"?>` + "\n")
	result := append(header, output...)
	
	// Add xhtml namespace if there are alternates
	for _, u := range g.urls {
		if len(u.Alternates) > 0 {
			result = g.addXHTMLNamespace(result)
			break
		}
	}
	
	return result, nil
}

// addXHTMLNamespace adds xhtml namespace to the urlset element
func (g *Generator) addXHTMLNamespace(xmlData []byte) []byte {
	return bytes.Replace(xmlData, 
		[]byte(`<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">`),
		[]byte(`<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">`),
		1)
}

// ToFile writes the sitemap to a file
func (g *Generator) ToFile(filename string) error {
	xmlData, err := g.ToXML()
	if err != nil {
		return err
	}
	
	if g.compress {
		return g.writeGzippedFile(filename, xmlData)
	}
	
	return os.WriteFile(filename, xmlData, 0644)
}

// writeGzippedFile writes compressed data to a file
func (g *Generator) writeGzippedFile(filename string, data []byte) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()
	
	gz := gzip.NewWriter(file)
	defer gz.Close()
	
	_, err = gz.Write(data)
	return err
}

// ToWriter writes the sitemap to an io.Writer
func (g *Generator) ToWriter(w io.Writer) error {
	xmlData, err := g.ToXML()
	if err != nil {
		return err
	}
	
	if g.compress {
		gz := gzip.NewWriter(w)
		defer gz.Close()
		_, err = gz.Write(xmlData)
		return err
	}
	
	_, err = w.Write(xmlData)
	return err
}

// Split splits URLs into multiple sitemaps if necessary
func (g *Generator) Split() [][]URL {
	var result [][]URL
	for i := 0; i < len(g.urls); i += g.maxURLs {
		end := i + g.maxURLs
		if end > len(g.urls) {
			end = len(g.urls)
		}
		result = append(result, g.urls[i:end])
	}
	return result
}

// IndexGenerator creates sitemap index files
type IndexGenerator struct {
	sitemaps []sitemapEntry
	compress bool
	pretty   bool
}

// NewIndexGenerator creates a new sitemap index generator
func NewIndexGenerator() *IndexGenerator {
	return &IndexGenerator{
		sitemaps: make([]sitemapEntry, 0),
		compress: false,
		pretty:   false,
	}
}

// WithIndexCompression enables compression for index generator
func WithIndexCompression(enable bool) func(*IndexGenerator) {
	return func(ig *IndexGenerator) {
		ig.compress = enable
	}
}

// WithIndexPrettyPrint enables pretty printing for index generator
func WithIndexPrettyPrint(enable bool) func(*IndexGenerator) {
	return func(ig *IndexGenerator) {
		ig.pretty = enable
	}
}

// AddSitemap adds a sitemap to the index
func (ig *IndexGenerator) AddSitemap(loc string, lastMod *time.Time) error {
	if len(ig.sitemaps) >= MaxSitemapsPerIndex {
		return fmt.Errorf("maximum sitemaps (%d) reached", MaxSitemapsPerIndex)
	}
	
	loc = strings.TrimSpace(loc)
	if loc == "" {
		return fmt.Errorf("sitemap location cannot be empty")
	}
	
	ig.sitemaps = append(ig.sitemaps, sitemapEntry{
		Loc:     loc,
		LastMod: lastMod,
	})
	return nil
}

// Count returns the number of sitemaps in the index
func (ig *IndexGenerator) Count() int {
	return len(ig.sitemaps)
}

// ToXML generates the sitemap index XML
func (ig *IndexGenerator) ToXML() ([]byte, error) {
	if len(ig.sitemaps) == 0 {
		return nil, fmt.Errorf("no sitemaps in index")
	}
	
	index := sitemapIndexXML{
		Xmlns:    "http://www.sitemaps.org/schemas/sitemap/0.9",
		Sitemaps: ig.sitemaps,
	}
	
	var output []byte
	var err error
	
	if ig.pretty {
		output, err = xml.MarshalIndent(index, "", "  ")
	} else {
		output, err = xml.Marshal(index)
	}
	
	if err != nil {
		return nil, fmt.Errorf("failed to marshal sitemap index: %w", err)
	}
	
	header := []byte(`<?xml version="1.0" encoding="UTF-8"?>` + "\n")
	return append(header, output...), nil
}

// ToFile writes the sitemap index to a file
func (ig *IndexGenerator) ToFile(filename string) error {
	xmlData, err := ig.ToXML()
	if err != nil {
		return err
	}
	
	if ig.compress {
		file, err := os.Create(filename)
		if err != nil {
			return err
		}
		defer file.Close()
		
		gz := gzip.NewWriter(file)
		defer gz.Close()
		_, err = gz.Write(xmlData)
		return err
	}
	
	return os.WriteFile(filename, xmlData, 0644)
}

// Parser parses existing sitemap files
type Parser struct{}

// NewParser creates a new sitemap parser
func NewParser() *Parser {
	return &Parser{}
}

// Parse parses sitemap XML data
func (p *Parser) Parse(data []byte) (*Sitemap, error) {
	// Handle gzip compression
	if len(data) > 2 && data[0] == 0x1f && data[1] == 0x8b {
		return p.parseGzipped(data)
	}
	
	var sitemap sitemapXML
	if err := xml.Unmarshal(data, &sitemap); err != nil {
		return nil, fmt.Errorf("failed to parse sitemap: %w", err)
	}
	
	return &Sitemap{URLs: sitemap.URLs}, nil
}

// parseGzipped parses a gzipped sitemap
func (p *Parser) parseGzipped(data []byte) (*Sitemap, error) {
	gz, err := gzip.NewReader(bytes.NewReader(data))
	if err != nil {
		return nil, fmt.Errorf("failed to create gzip reader: %w", err)
	}
	defer gz.Close()
	
	decoded, err := io.ReadAll(gz)
	if err != nil {
		return nil, fmt.Errorf("failed to decompress sitemap: %w", err)
	}
	
	return p.Parse(decoded)
}

// ParseFile parses a sitemap file
func (p *Parser) ParseFile(filename string) (*Sitemap, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, fmt.Errorf("failed to read file: %w", err)
	}
	return p.Parse(data)
}

// ParseIndex parses a sitemap index file
func (p *Parser) ParseIndex(data []byte) ([]sitemapEntry, error) {
	var index sitemapIndexXML
	if err := xml.Unmarshal(data, &index); err != nil {
		return nil, fmt.Errorf("failed to parse sitemap index: %w", err)
	}
	return index.Sitemaps, nil
}

// ParseIndexFile parses a sitemap index file
func (p *Parser) ParseIndexFile(filename string) ([]sitemapEntry, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, fmt.Errorf("failed to read file: %w", err)
	}
	return p.ParseIndex(data)
}

// URLBuilder helps construct URLs with parameters
type URLBuilder struct {
	baseURL   string
	paths     []string
	params    map[string]string
}

// NewURLBuilder creates a new URL builder
func NewURLBuilder(baseURL string) *URLBuilder {
	return &URLBuilder{
		baseURL: strings.TrimSuffix(baseURL, "/"),
		paths:   make([]string, 0),
		params:  make(map[string]string),
	}
}

// Path appends a path segment
func (b *URLBuilder) Path(path string) *URLBuilder {
	path = strings.Trim(path, "/")
	if path != "" {
		b.paths = append(b.paths, path)
	}
	return b
}

// Param adds a query parameter
func (b *URLBuilder) Param(key, value string) *URLBuilder {
	b.params[key] = value
	return b
}

// Build constructs the final URL
func (b *URLBuilder) Build() string {
	var sb strings.Builder
	sb.WriteString(b.baseURL)
	
	if len(b.paths) > 0 {
		sb.WriteString("/")
		sb.WriteString(strings.Join(b.paths, "/"))
	}
	
	if len(b.params) > 0 {
		sb.WriteString("?")
		first := true
		for key, value := range b.params {
			if !first {
				sb.WriteString("&")
			}
			sb.WriteString(key)
			sb.WriteString("=")
			sb.WriteString(value)
			first = false
		}
	}
	
	return sb.String()
}

// Reset clears the builder for reuse
func (b *URLBuilder) Reset() *URLBuilder {
	b.paths = make([]string, 0)
	b.params = make(map[string]string)
	return b
}

// BatchGenerator helps create multiple sitemaps for large sites
type BatchGenerator struct {
	generators []*Generator
	maxURLs    int
	currentIdx int
	compress   bool
	pretty     bool
	baseURL    string
}

// NewBatchGenerator creates a new batch generator
func NewBatchGenerator(maxURLs int, opts ...GeneratorOption) *BatchGenerator {
	bg := &BatchGenerator{
		generators: make([]*Generator, 0),
		maxURLs:    maxURLs,
		currentIdx: 0,
		compress:   false,
		pretty:     false,
		baseURL:    "",
	}
	
	for _, opt := range opts {
		g := &Generator{}
		opt(g)
		bg.compress = g.compress
		bg.pretty = g.pretty
		bg.baseURL = g.baseURL
	}
	
	// Create first generator
	bg.newGenerator()
	return bg
}

// newGenerator creates a new sitemap generator
func (bg *BatchGenerator) newGenerator() {
	opts := []GeneratorOption{WithMaxURLs(bg.maxURLs)}
	if bg.compress {
		opts = append(opts, WithCompression(true))
	}
	if bg.pretty {
		opts = append(opts, WithPrettyPrint(true))
	}
	if bg.baseURL != "" {
		opts = append(opts, WithBaseURL(bg.baseURL))
	}
	bg.generators = append(bg.generators, NewGenerator(opts...))
}

// AddURL adds a URL to the batch
func (bg *BatchGenerator) AddURL(url URL) error {
	// Check if current generator is full
	if bg.generators[bg.currentIdx].Count() >= bg.maxURLs {
		bg.newGenerator()
		bg.currentIdx++
	}
	
	return bg.generators[bg.currentIdx].AddURL(url)
}

// TotalCount returns total URLs across all generators
func (bg *BatchGenerator) TotalCount() int {
	total := 0
	for _, g := range bg.generators {
		total += g.Count()
	}
	return total
}

// SitemapCount returns the number of sitemaps
func (bg *BatchGenerator) SitemapCount() int {
	return len(bg.generators)
}

// ToFiles writes all sitemaps to files with the given prefix
func (bg *BatchGenerator) ToFiles(prefix string) ([]string, error) {
	filenames := make([]string, 0, len(bg.generators))
	
	for i, g := range bg.generators {
		var filename string
		if bg.compress {
			filename = fmt.Sprintf("%s-%d.xml.gz", prefix, i+1)
		} else {
			filename = fmt.Sprintf("%s-%d.xml", prefix, i+1)
		}
		
		if err := g.ToFile(filename); err != nil {
			return filenames, err
		}
		filenames = append(filenames, filename)
	}
	
	return filenames, nil
}

// CreateIndex creates a sitemap index for all sitemaps
func (bg *BatchGenerator) CreateIndex(indexURL string) ([]byte, error) {
	ig := NewIndexGenerator()
	
	for i := range bg.generators {
		loc := fmt.Sprintf("%s-%d.xml", indexURL, i+1)
		if bg.compress {
			loc += ".gz"
		}
		if err := ig.AddSitemap(loc, nil); err != nil {
			return nil, err
		}
	}
	
	return ig.ToXML()
}