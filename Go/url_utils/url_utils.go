// Package url_utils provides comprehensive URL processing utilities.
// Includes URL normalization, parsing, validation, query parameter handling,
// URL building, and common URL operations with zero external dependencies.
package url_utils

import (
	"encoding/hex"
	"errors"
	"net/url"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"time"
)

// Common errors
var (
	ErrInvalidURL       = errors.New("invalid URL")
	ErrEmptyURL         = errors.New("empty URL")
	ErrInvalidScheme    = errors.New("invalid or missing scheme")
	ErrInvalidHost      = errors.New("invalid host")
	ErrInvalidPort      = errors.New("invalid port")
	ErrInvalidQueryParam = errors.New("invalid query parameter")
	ErrURLTooLong       = errors.New("URL exceeds maximum length")
)

// Default port mappings for common schemes
var defaultPorts = map[string]string{
	"http":   "80",
	"https":  "443",
	"ftp":    "21",
	"sftp":   "22",
	"ssh":    "22",
	"telnet": "23",
	"smtp":   "25",
	"dns":    "53",
	"pop3":   "110",
	"imap":   "143",
	"ldap":   "389",
	"mysql":  "3306",
	"pgsql":  "5432",
	"redis":  "6379",
	"mongodb":"27017",
}

// Common regex patterns
var (
	domainRegex   = regexp.MustCompile(`^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$`)
	ipv4Regex     = regexp.MustCompile(`^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$`)
	uuidRegex     = regexp.MustCompile(`^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$`)
	slugRegex     = regexp.MustCompile(`^[a-z0-9]+(?:-[a-z0-9]+)*$`)
)

// URLInfo contains parsed URL information
type URLInfo struct {
	Scheme      string
	Host        string
	Port        string
	Path        string
	Query       url.Values
	Fragment    string
	User        string
	Password    string
	IsDefaultPort bool
	IsIP        bool
	IsHTTPS     bool
	Subdomain   string
	Domain      string
	TLD         string
}

// NormalizeOption defines options for URL normalization
type NormalizeOption int

const (
	NormalizeDefault NormalizeOption = iota
	NormalizeLowercaseScheme
	NormalizeLowercaseHost
	NormalizeRemoveDefaultPort
	NormalizeRemoveWWW
	NormalizeAddWWW
	NormalizeRemoveTrailingSlash
	NormalizeAddTrailingSlash
	NormalizeSortQuery
	NormalizeRemoveFragment
	NormalizeRemoveDuplicateSlashes
	NormalizeDecodeUnreserved
	NormalizeEncodeReserved
	NormalizeRemoveIndexPage
	NormalizeRemoveUTM
)

// NormalizeOptions is a collection of normalization options
type NormalizeOptions []NormalizeOption

// DefaultNormalizeOptions returns the default normalization options
func DefaultNormalizeOptions() NormalizeOptions {
	return NormalizeOptions{
		NormalizeLowercaseScheme,
		NormalizeLowercaseHost,
		NormalizeRemoveDefaultPort,
		NormalizeRemoveTrailingSlash,
		NormalizeSortQuery,
		NormalizeRemoveDuplicateSlashes,
	}
}

// Parse parses a URL string and returns URLInfo
func Parse(rawURL string) (*URLInfo, error) {
	if rawURL == "" {
		return nil, ErrEmptyURL
	}

	// Add scheme if missing
	if !strings.Contains(rawURL, "://") {
		rawURL = "http://" + rawURL
	}

	parsed, err := url.Parse(rawURL)
	if err != nil {
		return nil, ErrInvalidURL
	}

	if parsed.Host == "" {
		return nil, ErrInvalidHost
	}

	info := &URLInfo{
		Scheme:   parsed.Scheme,
		Path:     parsed.Path,
		Query:    parsed.Query(),
		Fragment: parsed.Fragment,
		IsHTTPS:  parsed.Scheme == "https",
	}

	// Set default path to "/" if empty
	if info.Path == "" {
		info.Path = "/"
	}

	// Extract host and port
	host, port := extractHostPort(parsed.Host)
	info.Host = host
	info.Port = port

	// Check if using default port
	defaultPort := defaultPorts[info.Scheme]
	info.IsDefaultPort = (port == "" || port == defaultPort)

	// Check if host is IP
	info.IsIP = ipv4Regex.MatchString(host)

	// Extract user info
	if parsed.User != nil {
		info.User = parsed.User.Username()
		info.Password, _ = parsed.User.Password()
	}

	// Parse domain parts
	if !info.IsIP {
		info.Domain, info.TLD, info.Subdomain = parseDomainParts(host)
	}

	return info, nil
}

// ParseString parses a URL string and returns the standard url.URL
func ParseString(rawURL string) (*url.URL, error) {
	if rawURL == "" {
		return nil, ErrEmptyURL
	}

	// Add scheme if missing
	if !strings.Contains(rawURL, "://") {
		rawURL = "http://" + rawURL
	}

	parsed, err := url.Parse(rawURL)
	if err != nil {
		return nil, err
	}

	// Check for empty host
	if parsed.Host == "" {
		return nil, ErrInvalidHost
	}

	return parsed, nil
}

// extractHostPort separates host and port from host:port string
func extractHostPort(hostPort string) (host, port string) {
	// Handle IPv6 addresses
	if strings.HasPrefix(hostPort, "[") {
		end := strings.Index(hostPort, "]")
		if end == -1 {
			return hostPort, ""
		}
		host = hostPort[1:end]
		if end+1 < len(hostPort) && hostPort[end+1] == ':' {
			port = hostPort[end+2:]
		}
		return host, port
	}

	// Handle IPv4 or domain
	parts := strings.Split(hostPort, ":")
	if len(parts) == 2 {
		// Check if the second part is a valid port
		if _, err := strconv.Atoi(parts[1]); err == nil {
			return parts[0], parts[1]
		}
	}
	return hostPort, ""
}

// parseDomainParts extracts domain, TLD, and subdomain from a hostname
func parseDomainParts(host string) (domain, tld, subdomain string) {
	parts := strings.Split(host, ".")
	if len(parts) < 2 {
		return host, "", ""
	}

	// Handle common multi-part TLDs
	tld = parts[len(parts)-1]
	
	// Check for two-part TLDs (e.g., co.uk, com.au)
	commonTwoPartTLDs := map[string]bool{
		"co.uk": true, "com.au": true, "co.nz": true, "co.jp": true,
		"com.br": true, "co.in": true, "com.cn": true, "co.za": true,
	}
	
	if len(parts) >= 3 {
		potentialTwoPartTLD := parts[len(parts)-2] + "." + parts[len(parts)-1]
		if commonTwoPartTLDs[potentialTwoPartTLD] {
			tld = potentialTwoPartTLD
			if len(parts) >= 4 {
				domain = parts[len(parts)-3]
				subdomain = strings.Join(parts[:len(parts)-3], ".")
			} else {
				domain = parts[len(parts)-3]
			}
			return domain, tld, subdomain
		}
	}

	domain = parts[len(parts)-2]
	if len(parts) > 2 {
		subdomain = strings.Join(parts[:len(parts)-2], ".")
	}

	return domain, tld, subdomain
}

// Normalize normalizes a URL using default options
func Normalize(rawURL string) (string, error) {
	return NormalizeWithOptions(rawURL, DefaultNormalizeOptions())
}

// NormalizeWithOptions normalizes a URL with specified options
func NormalizeWithOptions(rawURL string, options NormalizeOptions) (string, error) {
	if rawURL == "" {
		return "", ErrEmptyURL
	}

	// Parse URL
	parsed, err := ParseString(rawURL)
	if err != nil {
		return "", err
	}

	// Apply normalization options
	removeTrailingSlash := false
	for _, opt := range options {
		switch opt {
		case NormalizeLowercaseScheme:
			parsed.Scheme = strings.ToLower(parsed.Scheme)
		case NormalizeLowercaseHost:
			parsed.Host = strings.ToLower(parsed.Host)
		case NormalizeRemoveDefaultPort:
			parsed.Host = removeDefaultPort(parsed.Scheme, parsed.Host)
		case NormalizeRemoveWWW:
			if strings.HasPrefix(parsed.Host, "www.") {
				parsed.Host = parsed.Host[4:]
			}
		case NormalizeAddWWW:
			if !strings.HasPrefix(parsed.Host, "www.") && !ipv4Regex.MatchString(parsed.Host) {
				parsed.Host = "www." + parsed.Host
			}
		case NormalizeRemoveTrailingSlash:
			removeTrailingSlash = true
			parsed.Path = strings.TrimSuffix(parsed.Path, "/")
		case NormalizeAddTrailingSlash:
			if parsed.Path != "" && !strings.HasSuffix(parsed.Path, "/") {
				parsed.Path += "/"
			}
		case NormalizeSortQuery:
			parsed.RawQuery = sortQueryString(parsed.RawQuery)
		case NormalizeRemoveFragment:
			parsed.Fragment = ""
		case NormalizeRemoveDuplicateSlashes:
			for strings.Contains(parsed.Path, "//") {
				parsed.Path = strings.ReplaceAll(parsed.Path, "//", "/")
			}
		case NormalizeDecodeUnreserved:
			parsed.Path = decodeUnreserved(parsed.Path)
			parsed.RawQuery = decodeUnreservedQuery(parsed.RawQuery)
		case NormalizeEncodeReserved:
			parsed.Path = encodePath(parsed.Path)
		case NormalizeRemoveIndexPage:
			parsed.Path = removeIndexPage(parsed.Path)
		case NormalizeRemoveUTM:
			parsed.RawQuery = removeUTMParams(parsed.RawQuery)
		}
	}

	// Build result manually to handle trailing slash removal
	result := buildURL(parsed, removeTrailingSlash)
	return result, nil
}

// buildURL builds a URL string from parsed components
func buildURL(parsed *url.URL, removeTrailingSlash bool) string {
	var result strings.Builder

	// Scheme
	if parsed.Scheme != "" {
		result.WriteString(parsed.Scheme)
		result.WriteString("://")
	}

	// User info
	if parsed.User != nil {
		result.WriteString(parsed.User.Username())
		if password, ok := parsed.User.Password(); ok && password != "" {
			result.WriteString(":")
			result.WriteString(password)
		}
		result.WriteString("@")
	}

	// Host
	result.WriteString(parsed.Host)

	// Path - handle trailing slash removal
	path := parsed.Path
	if path == "" {
		// If removeTrailingSlash is false and path was empty originally, 
		// we don't add "/" - let the URL be without trailing slash
		// This matches common expectations for "http://example.com"
	} else if removeTrailingSlash && path == "/" {
		path = ""
	}
	result.WriteString(path)

	// Query
	if parsed.RawQuery != "" {
		result.WriteString("?")
		result.WriteString(parsed.RawQuery)
	}

	// Fragment
	if parsed.Fragment != "" {
		result.WriteString("#")
		result.WriteString(parsed.Fragment)
	}

	return result.String()
}

// removeDefaultPort removes the port if it's the default for the scheme
func removeDefaultPort(scheme, host string) string {
	hostPart, port := extractHostPort(host)
	if port == "" {
		return host
	}
	defaultPort, ok := defaultPorts[strings.ToLower(scheme)]
	if ok && port == defaultPort {
		return hostPart
	}
	return host
}

// sortQueryString sorts query parameters alphabetically
func sortQueryString(query string) string {
	if query == "" {
		return ""
	}
	values, err := url.ParseQuery(query)
	if err != nil {
		return query
	}
	return encodeSortedValues(values)
}

// encodeSortedValues encodes values with sorted keys
func encodeSortedValues(values url.Values) string {
	if values == nil {
		return ""
	}

	keys := make([]string, 0, len(values))
	for k := range values {
		keys = append(keys, k)
	}
	sort.Strings(keys)

	var parts []string
	for _, k := range keys {
		for _, v := range values[k] {
			parts = append(parts, url.QueryEscape(k)+"="+url.QueryEscape(v))
		}
	}
	return strings.Join(parts, "&")
}

// decodeUnreserved decodes unreserved characters in a path
func decodeUnreserved(s string) string {
	result := make([]byte, 0, len(s))
	i := 0
	for i < len(s) {
		if s[i] == '%' && i+2 < len(s) {
			if b, err := hex.DecodeString(s[i+1 : i+3]); err == nil {
				if isUnreserved(b[0]) {
					result = append(result, b[0])
					i += 3
					continue
				}
			}
		}
		result = append(result, s[i])
		i++
	}
	return string(result)
}

// decodeUnreservedQuery decodes unreserved characters in query string
func decodeUnreservedQuery(s string) string {
	if s == "" {
		return ""
	}
	values, err := url.ParseQuery(s)
	if err != nil {
		return s
	}
	return encodeSortedValues(values)
}

// isUnreserved checks if a character is unreserved per RFC 3986
func isUnreserved(c byte) bool {
	return (c >= 'a' && c <= 'z') ||
		(c >= 'A' && c <= 'Z') ||
		(c >= '0' && c <= '9') ||
		c == '-' || c == '.' || c == '_' || c == '~'
}

// encodePath encodes path with proper percent-encoding
func encodePath(path string) string {
	return url.PathEscape(path)
}

// removeIndexPage removes common index pages from the path
func removeIndexPage(path string) string {
	indexPages := []string{"/index.html", "/index.htm", "/index.php", "/index.asp", "/index.aspx", "/default.html", "/default.htm", "/default.asp", "/default.aspx"}
	for _, page := range indexPages {
		if strings.HasSuffix(path, page) {
			return path[:len(path)-len(page)]
		}
	}
	return path
}

// removeUTMParams removes UTM tracking parameters from query string
func removeUTMParams(query string) string {
	if query == "" {
		return ""
	}
	values, err := url.ParseQuery(query)
	if err != nil {
		return query
	}
	for key := range values {
		if strings.HasPrefix(strings.ToLower(key), "utm_") {
			delete(values, key)
		}
	}
	return encodeSortedValues(values)
}

// Validate validates a URL string
func Validate(rawURL string) error {
	_, err := ParseString(rawURL)
	return err
}

// IsValid checks if a URL string is valid
func IsValid(rawURL string) bool {
	return Validate(rawURL) == nil
}

// IsValidHTTP checks if a URL is a valid HTTP/HTTPS URL
func IsValidHTTP(rawURL string) bool {
	parsed, err := ParseString(rawURL)
	if err != nil {
		return false
	}
	return parsed.Scheme == "http" || parsed.Scheme == "https"
}

// IsAbsolute checks if a URL is absolute (has scheme)
func IsAbsolute(rawURL string) bool {
	return strings.Contains(rawURL, "://")
}

// IsRelative checks if a URL is relative (no scheme)
func IsRelative(rawURL string) bool {
	return !IsAbsolute(rawURL)
}

// Resolve resolves a relative URL against a base URL
func Resolve(base, relative string) (string, error) {
	baseURL, err := url.Parse(base)
	if err != nil {
		return "", err
	}

	relativeURL, err := url.Parse(relative)
	if err != nil {
		return "", err
	}

	return baseURL.ResolveReference(relativeURL).String(), nil
}

// Join joins URL path segments
func Join(base string, segments ...string) (string, error) {
	parsed, err := url.Parse(base)
	if err != nil {
		return "", err
	}

	parts := []string{parsed.Path}
	parts = append(parts, segments...)

	// Clean and join paths
	result := strings.Join(parts, "/")
	// Remove duplicate slashes
	for strings.Contains(result, "//") {
		result = strings.ReplaceAll(result, "//", "/")
	}
	// Remove trailing slash
	result = strings.TrimSuffix(result, "/")
	if result == "" {
		result = "/"
	}

	parsed.Path = result
	return parsed.String(), nil
}

// QueryBuilder helps build query strings
type QueryBuilder struct {
	values url.Values
}

// NewQueryBuilder creates a new QueryBuilder
func NewQueryBuilder() *QueryBuilder {
	return &QueryBuilder{
		values: make(url.Values),
	}
}

// Add adds a query parameter
func (qb *QueryBuilder) Add(key, value string) *QueryBuilder {
	qb.values.Add(key, value)
	return qb
}

// Set sets a query parameter (replaces existing)
func (qb *QueryBuilder) Set(key, value string) *QueryBuilder {
	qb.values.Set(key, value)
	return qb
}

// Del deletes a query parameter
func (qb *QueryBuilder) Del(key string) *QueryBuilder {
	qb.values.Del(key)
	return qb
}

// Get gets the first value for a key
func (qb *QueryBuilder) Get(key string) string {
	return qb.values.Get(key)
}

// GetAll gets all values for a key
func (qb *QueryBuilder) GetAll(key string) []string {
	return qb.values[key]
}

// Has checks if a key exists
func (qb *QueryBuilder) Has(key string) bool {
	_, ok := qb.values[key]
	return ok
}

// Build builds the query string
func (qb *QueryBuilder) Build() string {
	return qb.values.Encode()
}

// BuildSorted builds a sorted query string (deterministic order)
func (qb *QueryBuilder) BuildSorted() string {
	return encodeSortedValues(qb.values)
}

// ParseQuery parses a query string and returns a QueryBuilder
func ParseQuery(query string) (*QueryBuilder, error) {
	values, err := url.ParseQuery(query)
	if err != nil {
		return nil, err
	}
	return &QueryBuilder{values: values}, nil
}

// URLBuilder helps build URLs
type URLBuilder struct {
	scheme   string
	host     string
	port     string
	path     string
	query    *QueryBuilder
	fragment string
	user     string
	password string
}

// NewURLBuilder creates a new URLBuilder
func NewURLBuilder() *URLBuilder {
	return &URLBuilder{
		query: NewQueryBuilder(),
	}
}

// SetScheme sets the scheme (http, https, etc.)
func (b *URLBuilder) SetScheme(scheme string) *URLBuilder {
	b.scheme = strings.ToLower(scheme)
	return b
}

// SetHost sets the host
func (b *URLBuilder) SetHost(host string) *URLBuilder {
	b.host = strings.ToLower(host)
	return b
}

// SetPort sets the port
func (b *URLBuilder) SetPort(port string) *URLBuilder {
	b.port = port
	return b
}

// SetPath sets the path
func (b *URLBuilder) SetPath(path string) *URLBuilder {
	if !strings.HasPrefix(path, "/") {
		path = "/" + path
	}
	b.path = path
	return b
}

// AddPath appends to the path
func (b *URLBuilder) AddPath(segments ...string) *URLBuilder {
	parts := []string{b.path}
	parts = append(parts, segments...)
	b.path = strings.Join(parts, "/")
	for strings.Contains(b.path, "//") {
		b.path = strings.ReplaceAll(b.path, "//", "/")
	}
	return b
}

// SetFragment sets the fragment
func (b *URLBuilder) SetFragment(fragment string) *URLBuilder {
	b.fragment = fragment
	return b
}

// SetUser sets the username
func (b *URLBuilder) SetUser(user string) *URLBuilder {
	b.user = user
	return b
}

// SetPassword sets the password
func (b *URLBuilder) SetPassword(password string) *URLBuilder {
	b.password = password
	return b
}

// AddQueryParam adds a query parameter
func (b *URLBuilder) AddQueryParam(key, value string) *URLBuilder {
	b.query.Add(key, value)
	return b
}

// SetQueryParam sets a query parameter
func (b *URLBuilder) SetQueryParam(key, value string) *URLBuilder {
	b.query.Set(key, value)
	return b
}

// Build builds the URL
func (b *URLBuilder) Build() string {
	var result strings.Builder

	// Scheme
	if b.scheme != "" {
		result.WriteString(b.scheme)
		result.WriteString("://")
	} else {
		result.WriteString("http://")
	}

	// User info
	if b.user != "" {
		result.WriteString(url.QueryEscape(b.user))
		if b.password != "" {
			result.WriteString(":")
			result.WriteString(url.QueryEscape(b.password))
		}
		result.WriteString("@")
	}

	// Host
	result.WriteString(b.host)

	// Port
	if b.port != "" {
		// Check if non-default port
		defaultPort := defaultPorts[b.scheme]
		if b.port != defaultPort {
			result.WriteString(":")
			result.WriteString(b.port)
		}
	}

	// Path
	if b.path != "" {
		result.WriteString(b.path)
	} else {
		result.WriteString("/")
	}

	// Query
	queryString := b.query.Build()
	if queryString != "" {
		result.WriteString("?")
		result.WriteString(queryString)
	}

	// Fragment
	if b.fragment != "" {
		result.WriteString("#")
		result.WriteString(url.QueryEscape(b.fragment))
	}

	return result.String()
}

// FromURL creates a URLBuilder from an existing URL
func FromURL(rawURL string) (*URLBuilder, error) {
	parsed, err := Parse(rawURL)
	if err != nil {
		return nil, err
	}

	builder := NewURLBuilder()
	builder.SetScheme(parsed.Scheme)
	builder.SetHost(parsed.Host)
	if !parsed.IsDefaultPort && parsed.Port != "" {
		builder.SetPort(parsed.Port)
	}
	builder.SetPath(parsed.Path)
	builder.SetFragment(parsed.Fragment)
	if parsed.User != "" {
		builder.SetUser(parsed.User)
	}
	if parsed.Password != "" {
		builder.SetPassword(parsed.Password)
	}

	// Add query params
	for key, values := range parsed.Query {
		for _, value := range values {
			builder.AddQueryParam(key, value)
		}
	}

	return builder, nil
}

// Equals compares two URLs for equality (after normalization)
func Equals(url1, url2 string) (bool, error) {
	norm1, err := Normalize(url1)
	if err != nil {
		return false, err
	}
	norm2, err := Normalize(url2)
	if err != nil {
		return false, err
	}
	return norm1 == norm2, nil
}

// ExtractDomain extracts the domain from a URL
func ExtractDomain(rawURL string) (string, error) {
	info, err := Parse(rawURL)
	if err != nil {
		return "", err
	}
	if info.IsIP {
		return info.Host, nil
	}
	return info.Domain + "." + info.TLD, nil
}

// ExtractRootDomain extracts the root domain (domain + TLD)
func ExtractRootDomain(rawURL string) (string, error) {
	info, err := Parse(rawURL)
	if err != nil {
		return "", err
	}
	if info.IsIP {
		return info.Host, nil
	}
	return info.Domain + "." + info.TLD, nil
}

// ExtractSubdomain extracts the subdomain from a URL
func ExtractSubdomain(rawURL string) (string, error) {
	info, err := Parse(rawURL)
	if err != nil {
		return "", err
	}
	return info.Subdomain, nil
}

// ExtractPath extracts the path from a URL
func ExtractPath(rawURL string) (string, error) {
	parsed, err := ParseString(rawURL)
	if err != nil {
		return "", err
	}
	path := parsed.Path
	if path == "" {
		path = "/"
	}
	return path, nil
}

// ExtractQuery extracts the query string from a URL
func ExtractQuery(rawURL string) (string, error) {
	parsed, err := ParseString(rawURL)
	if err != nil {
		return "", err
	}
	return parsed.RawQuery, nil
}

// ExtractFragment extracts the fragment from a URL
func ExtractFragment(rawURL string) (string, error) {
	parsed, err := ParseString(rawURL)
	if err != nil {
		return "", err
	}
	return parsed.Fragment, nil
}

// GetQueryParam gets a specific query parameter value
func GetQueryParam(rawURL, key string) (string, error) {
	parsed, err := ParseString(rawURL)
	if err != nil {
		return "", err
	}
	return parsed.Query().Get(key), nil
}

// GetQueryParams gets all values for a query parameter
func GetQueryParams(rawURL, key string) ([]string, error) {
	parsed, err := ParseString(rawURL)
	if err != nil {
		return nil, err
	}
	return parsed.Query()[key], nil
}

// SetQueryParam sets a query parameter in a URL
func SetQueryParam(rawURL, key, value string) (string, error) {
	parsed, err := ParseString(rawURL)
	if err != nil {
		return "", err
	}
	query := parsed.Query()
	query.Set(key, value)
	parsed.RawQuery = query.Encode()
	return parsed.String(), nil
}

// AddQueryParam adds a query parameter to a URL
func AddQueryParam(rawURL, key, value string) (string, error) {
	parsed, err := ParseString(rawURL)
	if err != nil {
		return "", err
	}
	query := parsed.Query()
	query.Add(key, value)
	parsed.RawQuery = query.Encode()
	return parsed.String(), nil
}

// RemoveQueryParam removes a query parameter from a URL
func RemoveQueryParam(rawURL, key string) (string, error) {
	parsed, err := ParseString(rawURL)
	if err != nil {
		return "", err
	}
	query := parsed.Query()
	query.Del(key)
	parsed.RawQuery = query.Encode()
	return parsed.String(), nil
}

// IsSameDomain checks if two URLs have the same domain
func IsSameDomain(url1, url2 string) (bool, error) {
	domain1, err := ExtractRootDomain(url1)
	if err != nil {
		return false, err
	}
	domain2, err := ExtractRootDomain(url2)
	if err != nil {
		return false, err
	}
	return domain1 == domain2, nil
}

// IsSameHost checks if two URLs have the same host
func IsSameHost(url1, url2 string) (bool, error) {
	info1, err := Parse(url1)
	if err != nil {
		return false, err
	}
	info2, err := Parse(url2)
	if err != nil {
		return false, err
	}
	return info1.Host == info2.Host, nil
}

// GetScheme returns the scheme of a URL
func GetScheme(rawURL string) (string, error) {
	info, err := Parse(rawURL)
	if err != nil {
		return "", err
	}
	return info.Scheme, nil
}

// GetHost returns the host of a URL
func GetHost(rawURL string) (string, error) {
	info, err := Parse(rawURL)
	if err != nil {
		return "", err
	}
	return info.Host, nil
}

// GetPort returns the port of a URL (empty if default)
func GetPort(rawURL string) (string, error) {
	info, err := Parse(rawURL)
	if err != nil {
		return "", err
	}
	// Return empty if it's a default port
	if info.IsDefaultPort {
		return "", nil
	}
	return info.Port, nil
}

// ToHTTPS converts a URL to HTTPS
func ToHTTPS(rawURL string) (string, error) {
	builder, err := FromURL(rawURL)
	if err != nil {
		return "", err
	}
	return builder.SetScheme("https").Build(), nil
}

// ToHTTP converts a URL to HTTP
func ToHTTP(rawURL string) (string, error) {
	builder, err := FromURL(rawURL)
	if err != nil {
		return "", err
	}
	return builder.SetScheme("http").Build(), nil
}

// IsSecure checks if a URL uses HTTPS
func IsSecure(rawURL string) bool {
	info, err := Parse(rawURL)
	if err != nil {
		return false
	}
	return info.IsHTTPS
}

// AddTimestamp adds a timestamp query parameter
func AddTimestamp(rawURL string) (string, error) {
	return AddQueryParam(rawURL, "_t", strconv.FormatInt(time.Now().Unix(), 10))
}

// AddCacheBuster adds a cache-busting parameter
func AddCacheBuster(rawURL string) (string, error) {
	return AddQueryParam(rawURL, "_cb", strconv.FormatInt(time.Now().UnixNano(), 10))
}

// IsUUID checks if a URL path contains a UUID
func IsUUID(rawURL string) bool {
	path, err := ExtractPath(rawURL)
	if err != nil {
		return false
	}
	// Check path segments for UUID
	segments := strings.Split(path, "/")
	for _, seg := range segments {
		if uuidRegex.MatchString(seg) {
			return true
		}
	}
	return false
}

// IsSlug checks if a URL path segment is a slug
func IsSlug(rawURL string) bool {
	path, err := ExtractPath(rawURL)
	if err != nil {
		return false
	}
	segments := strings.Split(strings.Trim(path, "/"), "/")
	if len(segments) > 0 {
		lastSeg := segments[len(segments)-1]
		return slugRegex.MatchString(lastSeg)
	}
	return false
}

// GetFileExtension extracts the file extension from a URL path
func GetFileExtension(rawURL string) (string, error) {
	path, err := ExtractPath(rawURL)
	if err != nil {
		return "", err
	}
	// Remove query string if present
	if idx := strings.Index(path, "?"); idx != -1 {
		path = path[:idx]
	}
	// Get last segment
	segments := strings.Split(path, "/")
	lastSeg := segments[len(segments)-1]
	if idx := strings.LastIndex(lastSeg, "."); idx != -1 {
		return lastSeg[idx+1:], nil
	}
	return "", nil
}

// RemoveFileExtension removes the file extension from a URL path
func RemoveFileExtension(rawURL string) (string, error) {
	parsed, err := ParseString(rawURL)
	if err != nil {
		return "", err
	}

	path := parsed.Path
	if idx := strings.LastIndex(path, "."); idx != -1 {
		// Check if it looks like a file extension (not a domain)
		if !strings.Contains(path[idx:], "/") {
			parsed.Path = path[:idx]
		}
	}

	return parsed.String(), nil
}

// Clean removes unnecessary parts from a URL
func Clean(rawURL string) (string, error) {
	return NormalizeWithOptions(rawURL, NormalizeOptions{
		NormalizeLowercaseScheme,
		NormalizeLowercaseHost,
		NormalizeRemoveDefaultPort,
		NormalizeRemoveDuplicateSlashes,
		NormalizeRemoveIndexPage,
		NormalizeRemoveUTM,
		NormalizeRemoveFragment,
		NormalizeRemoveTrailingSlash,
	})
}

// Canonical returns a canonical URL (most normalized form)
func Canonical(rawURL string) (string, error) {
	return NormalizeWithOptions(rawURL, NormalizeOptions{
		NormalizeLowercaseScheme,
		NormalizeLowercaseHost,
		NormalizeRemoveDefaultPort,
		NormalizeRemoveTrailingSlash,
		NormalizeSortQuery,
		NormalizeRemoveDuplicateSlashes,
		NormalizeDecodeUnreserved,
		NormalizeRemoveUTM,
		NormalizeRemoveIndexPage,
	})
}

// Diff compares two URLs and returns the differences
type URLDiff struct {
	SchemeDiff   bool
	HostDiff     bool
	PortDiff     bool
	PathDiff     bool
	QueryDiff    bool
	FragmentDiff bool
	UserDiff     bool
}

// Compare compares two URLs and returns the differences
func Compare(url1, url2 string) (*URLDiff, error) {
	info1, err := Parse(url1)
	if err != nil {
		return nil, err
	}
	info2, err := Parse(url2)
	if err != nil {
		return nil, err
	}

	diff := &URLDiff{
		SchemeDiff:   info1.Scheme != info2.Scheme,
		HostDiff:      info1.Host != info2.Host,
		PortDiff:      info1.Port != info2.Port,
		PathDiff:      info1.Path != info2.Path,
		FragmentDiff:  info1.Fragment != info2.Fragment,
		UserDiff:      info1.User != info2.User,
	}

	// Compare query params
	query1 := encodeSortedValues(info1.Query)
	query2 := encodeSortedValues(info2.Query)
	diff.QueryDiff = query1 != query2

	return diff, nil
}