package main

import (
	"fmt"
	"strings"

	url_utils "github.com/ayukyo/alltoolkit/Go/url_utils"
)

func main() {
	fmt.Println("=== URL Utilities Examples ===")
	fmt.Println()

	// 1. Basic Parsing
	fmt.Println("--- 1. Basic Parsing ---")
	exampleURL := "https://user:pass@sub.example.com:8080/api/v1/users?key=value&a=1#section"
	info, err := url_utils.Parse(exampleURL)
	if err != nil {
		fmt.Printf("Parse error: %v\n", err)
	} else {
		fmt.Printf("URL: %s\n", exampleURL)
		fmt.Printf("  Scheme: %s\n", info.Scheme)
		fmt.Printf("  Host: %s\n", info.Host)
		fmt.Printf("  Port: %s\n", info.Port)
		fmt.Printf("  Path: %s\n", info.Path)
		fmt.Printf("  Fragment: %s\n", info.Fragment)
		fmt.Printf("  User: %s\n", info.User)
		fmt.Printf("  Password: %s\n", info.Password)
		fmt.Printf("  Domain: %s\n", info.Domain)
		fmt.Printf("  TLD: %s\n", info.TLD)
		fmt.Printf("  Subdomain: %s\n", info.Subdomain)
		fmt.Printf("  IsHTTPS: %v\n", info.IsHTTPS)
		fmt.Printf("  IsIP: %v\n", info.IsIP)
		fmt.Printf("  IsDefaultPort: %v\n", info.IsDefaultPort)
	}
	fmt.Println()

	// 2. URL Normalization
	fmt.Println("--- 2. URL Normalization ---")
	rawURLs := []string{
		"HTTP://EXAMPLE.COM/",
		"https://www.example.com:443/path/",
		"http://example.com:80/?utm_source=google&a=2&b=1",
		"http://example.com//path///to///resource",
		"http://example.com/index.html",
	}
	for _, raw := range rawURLs {
		normalized, _ := url_utils.Normalize(raw)
		fmt.Printf("Raw:      %s\n", raw)
		fmt.Printf("Normalized: %s\n", normalized)
		fmt.Println()
	}
	fmt.Println()

	// 3. Canonical URL
	fmt.Println("--- 3. Canonical URL ---")
	urls := []string{
		"HTTPS://WWW.EXAMPLE.COM:443/PATH/?utm_source=x&id=123&a=2&b=1#section",
		"http://example.com/index.html?b=2&a=1",
	}
	for _, u := range urls {
		canonical, _ := url_utils.Canonical(u)
		fmt.Printf("Original: %s\n", u)
		fmt.Printf("Canonical: %s\n", canonical)
		fmt.Println()
	}
	fmt.Println()

	// 4. Query Parameter Operations
	fmt.Println("--- 4. Query Parameter Operations ---")
	testURL := "https://example.com/api?key1=value1&key2=value2"
	
	// Get single param
	val, _ := url_utils.GetQueryParam(testURL, "key1")
	fmt.Printf("GetQueryParam('key1'): %s\n", val)
	
	// Set param
	newURL, _ := url_utils.SetQueryParam(testURL, "key1", "newValue")
	fmt.Printf("SetQueryParam('key1', 'newValue'): %s\n", newURL)
	
	// Add param
	newURL, _ = url_utils.AddQueryParam(testURL, "key3", "value3")
	fmt.Printf("AddQueryParam('key3', 'value3'): %s\n", newURL)
	
	// Remove param
	newURL, _ = url_utils.RemoveQueryParam(testURL, "key2")
	fmt.Printf("RemoveQueryParam('key2'): %s\n", newURL)
	fmt.Println()

	// 5. QueryBuilder
	fmt.Println("--- 5. QueryBuilder ---")
	qb := url_utils.NewQueryBuilder()
	qb.Add("search", "golang")
	qb.Add("page", "1")
	qb.Add("limit", "10")
	qb.Add("sort", "desc")
	
	fmt.Printf("Build: %s\n", qb.Build())
	fmt.Printf("BuildSorted: %s\n", qb.BuildSorted())
	
	// Parse existing query string
	parsedQB, _ := url_utils.ParseQuery("a=1&b=2&c=3")
	fmt.Printf("Parsed: %s\n", parsedQB.Build())
	fmt.Println()

	// 6. URLBuilder
	fmt.Println("--- 6. URLBuilder ---")
	builder := url_utils.NewURLBuilder()
	builder.SetScheme("https")
	builder.SetHost("api.example.com")
	builder.SetPath("/v1/users")
	builder.AddQueryParam("id", "123")
	builder.AddQueryParam("format", "json")
	builder.SetFragment("profile")
	
	fmt.Printf("Built URL: %s\n", builder.Build())
	fmt.Println()

	// URLBuilder from existing URL
	fmt.Println("URLBuilder from existing URL:")
	fromBuilder, _ := url_utils.FromURL("https://example.com:8080/path?key=value")
	fromBuilder.SetScheme("http")
	fromBuilder.SetPort("3000")
	fmt.Printf("Modified URL: %s\n", fromBuilder.Build())
	fmt.Println()

	// 7. URL Extraction Functions
	fmt.Println("--- 7. URL Extraction Functions ---")
	testURL2 := "https://sub.api.example.com/v2/users/123?token=abc#profile"
	
	domain, _ := url_utils.ExtractDomain(testURL2)
	fmt.Printf("ExtractDomain: %s\n", domain)
	
	rootDomain, _ := url_utils.ExtractRootDomain(testURL2)
	fmt.Printf("ExtractRootDomain: %s\n", rootDomain)
	
	subdomain, _ := url_utils.ExtractSubdomain(testURL2)
	fmt.Printf("ExtractSubdomain: %s\n", subdomain)
	
	path, _ := url_utils.ExtractPath(testURL2)
	fmt.Printf("ExtractPath: %s\n", path)
	
	query, _ := url_utils.ExtractQuery(testURL2)
	fmt.Printf("ExtractQuery: %s\n", query)
	
	fragment, _ := url_utils.ExtractFragment(testURL2)
	fmt.Printf("ExtractFragment: %s\n", fragment)
	
	ext, _ := url_utils.GetFileExtension("https://example.com/image.png")
	fmt.Printf("GetFileExtension: %s\n", ext)
	fmt.Println()

	// 8. URL Validation
	fmt.Println("--- 8. URL Validation ---")
	testURLs := []string{
		"https://example.com",
		"http://invalid",
		"ftp://files.example.com",
		"",
		"not-a-url",
	}
	for _, u := range testURLs {
		fmt.Printf("%s -> IsValid: %v, IsValidHTTP: %v, IsSecure: %v\n", 
			u, url_utils.IsValid(u), url_utils.IsValidHTTP(u), url_utils.IsSecure(u))
	}
	fmt.Println()

	// 9. URL Comparison
	fmt.Println("--- 9. URL Comparison ---")
	url1 := "https://example.com/path"
	url2 := "https://example.com/path?key=value"
	
	equals, _ := url_utils.Equals(url1, url2)
	fmt.Printf("Equals(%s, %s): %v\n", url1, url2, equals)
	
	diff, _ := url_utils.Compare(url1, url2)
	fmt.Printf("Compare results:\n")
	fmt.Printf("  SchemeDiff: %v\n", diff.SchemeDiff)
	fmt.Printf("  HostDiff: %v\n", diff.HostDiff)
	fmt.Printf("  PathDiff: %v\n", diff.PathDiff)
	fmt.Printf("  QueryDiff: %v\n", diff.QueryDiff)
	fmt.Printf("  FragmentDiff: %v\n", diff.FragmentDiff)
	
	sameDomain, _ := url_utils.IsSameDomain("https://sub.example.com", "https://example.com")
	fmt.Printf("IsSameDomain(sub.example.com, example.com): %v\n", sameDomain)
	
	sameHost, _ := url_utils.IsSameHost("https://sub.example.com", "https://example.com")
	fmt.Printf("IsSameHost(sub.example.com, example.com): %v\n", sameHost)
	fmt.Println()

	// 10. URL Transformations
	fmt.Println("--- 10. URL Transformations ---")
	httpURL := "http://example.com/path"
	httpsURL, _ := url_utils.ToHTTPS(httpURL)
	fmt.Printf("ToHTTPS(%s): %s\n", httpURL, httpsURL)
	
	backToHTTP, _ := url_utils.ToHTTP(httpsURL)
	fmt.Printf("ToHTTP(%s): %s\n", httpsURL, backToHTTP)
	
	// Add timestamp
	withTS, _ := url_utils.AddTimestamp(httpURL)
	fmt.Printf("AddTimestamp: %s\n", withTS)
	
	// Add cache buster
	withCB, _ := url_utils.AddCacheBuster(httpURL)
	fmt.Printf("AddCacheBuster: %s\n", withCB)
	
	// Clean URL
	cleaned, _ := url_utils.Clean("https://example.com/index.html?utm_source=google&id=1#section")
	fmt.Printf("Clean: %s\n", cleaned)
	fmt.Println()

	// 11. URL Join and Resolve
	fmt.Println("--- 11. URL Join and Resolve ---")
	base := "https://example.com/api"
	
	// Join paths
	joined, _ := url_utils.Join(base, "v1", "users", "123")
	fmt.Printf("Join(%s, v1, users, 123): %s\n", base, joined)
	
	// Resolve relative URL
	resolved, _ := url_utils.Resolve(base, "/path/to/resource")
	fmt.Printf("Resolve(%s, /path/to/resource): %s\n", base, resolved)
	
	resolved, _ = url_utils.Resolve(base, "?query=value")
	fmt.Printf("Resolve(%s, ?query=value): %s\n", base, resolved)
	fmt.Println()

	// 12. Special URL Checks
	fmt.Println("--- 12. Special URL Checks ---")
	uuidURL := "https://example.com/users/550e8400-e29b-41d4-a716-446655440000"
	slugURL := "https://example.com/blog/my-awesome-post"
	
	fmt.Printf("IsUUID(%s): %v\n", uuidURL, url_utils.IsUUID(uuidURL))
	fmt.Printf("IsSlug(%s): %v\n", slugURL, url_utils.IsSlug(slugURL))
	fmt.Println()

	// 13. Normalize with Custom Options
	fmt.Println("--- 13. Normalize with Custom Options ---")
	customURL := "https://www.example.com:443/path?utm_source=x&id=1#section"
	
	// Remove WWW
	noWWW, _ := url_utils.NormalizeWithOptions(customURL, url_utils.NormalizeOptions{url_utils.NormalizeRemoveWWW})
	fmt.Printf("RemoveWWW: %s\n", noWWW)
	
	// Add WWW
	addWWW, _ := url_utils.NormalizeWithOptions("https://example.com", url_utils.NormalizeOptions{url_utils.NormalizeAddWWW})
	fmt.Printf("AddWWW: %s\n", addWWW)
	
	// Remove fragment
	noFrag, _ := url_utils.NormalizeWithOptions(customURL, url_utils.NormalizeOptions{url_utils.NormalizeRemoveFragment})
	fmt.Printf("RemoveFragment: %s\n", noFrag)
	
	// Add trailing slash
	addSlash, _ := url_utils.NormalizeWithOptions("https://example.com/path", url_utils.NormalizeOptions{url_utils.NormalizeAddTrailingSlash})
	fmt.Printf("AddTrailingSlash: %s\n", addSlash)
	fmt.Println()

	// 14. Working with Different URL Types
	fmt.Println("--- 14. Working with Different URL Types ---")
	
	// IPv4 URL
	ipURL := "http://192.168.1.1:8080/api"
	ipInfo, _ := url_utils.Parse(ipURL)
	fmt.Printf("IPv4 URL: %s\n", ipURL)
	fmt.Printf("  Host: %s (IsIP: %v)\n", ipInfo.Host, ipInfo.IsIP)
	
	// URL with authentication
	authURL := "https://admin:password@api.example.com/secure"
	authInfo, _ := url_utils.Parse(authURL)
	fmt.Printf("Auth URL: %s\n", authURL)
	fmt.Printf("  User: %s, Password: %s\n", authInfo.User, authInfo.Password)
	
	// Two-part TLD
	tldURL := "https://sub.example.co.uk/path"
	tldInfo, _ := url_utils.Parse(tldURL)
	fmt.Printf("Two-part TLD URL: %s\n", tldURL)
	fmt.Printf("  Domain: %s, TLD: %s, Subdomain: %s\n", tldInfo.Domain, tldInfo.TLD, tldInfo.Subdomain)
	fmt.Println()

	// Summary
	fmt.Println("=== Summary ===")
	fmt.Println("url_utils provides comprehensive URL processing utilities:")
	fmt.Println("- Parsing with detailed URL information extraction")
	fmt.Println("- Normalization with multiple customizable options")
	fmt.Println("- Query parameter manipulation (get, set, add, remove)")
	fmt.Println("- URL building and modification")
	fmt.Println("- URL comparison and validation")
	fmt.Println("- Domain, subdomain, path, query extraction")
	fmt.Println("- Scheme conversion (HTTP/HTTPS)")
	fmt.Println("- Cache busting and timestamp addition")
	fmt.Println("- File extension handling")
	fmt.Println("- UUID and slug detection")
	fmt.Println()
	fmt.Println("All functions work with zero external dependencies!")
}

// Helper to print query params
func printQueryParams(u string) {
	info, _ := url_utils.Parse(u)
	if len(info.Query) > 0 {
		var params []string
		for k, v := range info.Query {
			params = append(params, fmt.Sprintf("%s=%v", k, strings.Join(v, ",")))
		}
		fmt.Printf("Query params: %s\n", strings.Join(params, "&"))
	}
}