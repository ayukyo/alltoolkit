package case_utils

import (
	"testing"
)

func TestToCamelCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello_world", "helloWorld"},
		{"HelloWorld", "helloWorld"},
		{"hello-world", "helloWorld"},
		{"HELLO_WORLD", "helloWorld"},
		{"hello", "hello"},
		{"Hello", "hello"},
		{"helloWorld", "helloWorld"},
		{"hello_world_test", "helloWorldTest"},
		{"HTMLParser", "htmlParser"},
		{"parseHTMLResponse", "parseHtmlResponse"},
		{"XMLHttpRequest", "xmlHttpRequest"},
		{"kebab-case-example", "kebabCaseExample"},
		{"dot.case.example", "dotCaseExample"},
		{"path/case/example", "pathCaseExample"},
		{"APIEndpoint", "apiEndpoint"},
		{"getUserID", "getUserId"},
		{"", ""},
	}

	for _, test := range tests {
		result := ToCamelCase(test.input)
		if result != test.expected {
			t.Errorf("ToCamelCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToPascalCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello_world", "HelloWorld"},
		{"hello-world", "HelloWorld"},
		{"HELLO_WORLD", "HelloWorld"},
		{"hello", "Hello"},
		{"helloWorld", "HelloWorld"},
		{"hello_world_test", "HelloWorldTest"},
		{"HTMLParser", "HtmlParser"},
		{"parseHTMLResponse", "ParseHtmlResponse"},
		{"kebab-case-example", "KebabCaseExample"},
		{"", ""},
	}

	for _, test := range tests {
		result := ToPascalCase(test.input)
		if result != test.expected {
			t.Errorf("ToPascalCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToSnakeCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"helloWorld", "hello_world"},
		{"HelloWorld", "hello_world"},
		{"hello-world", "hello_world"},
		{"HELLO_WORLD", "hello_world"},
		{"hello", "hello"},
		{"Hello", "hello"},
		{"helloWorldTest", "hello_world_test"},
		{"HTMLParser", "html_parser"},
		{"parseHTMLResponse", "parse_html_response"},
		{"", ""},
	}

	for _, test := range tests {
		result := ToSnakeCase(test.input)
		if result != test.expected {
			t.Errorf("ToSnakeCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToKebabCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"helloWorld", "hello-world"},
		{"HelloWorld", "hello-world"},
		{"hello_world", "hello-world"},
		{"HELLO_WORLD", "hello-world"},
		{"hello", "hello"},
		{"helloWorldTest", "hello-world-test"},
		{"HTMLParser", "html-parser"},
		{"", ""},
	}

	for _, test := range tests {
		result := ToKebabCase(test.input)
		if result != test.expected {
			t.Errorf("ToKebabCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToScreamingSnakeCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"helloWorld", "HELLO_WORLD"},
		{"HelloWorld", "HELLO_WORLD"},
		{"hello_world", "HELLO_WORLD"},
		{"hello-world", "HELLO_WORLD"},
		{"hello", "HELLO"},
		{"helloWorldTest", "HELLO_WORLD_TEST"},
		{"", ""},
	}

	for _, test := range tests {
		result := ToScreamingSnakeCase(test.input)
		if result != test.expected {
			t.Errorf("ToScreamingSnakeCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToUpperCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"helloWorld", "HELLOWORLD"},
		{"HelloWorld", "HELLOWORLD"},
		{"hello_world", "HELLOWORLD"},
		{"hello", "HELLO"},
		{"", ""},
	}

	for _, test := range tests {
		result := ToUpperCase(test.input)
		if result != test.expected {
			t.Errorf("ToUpperCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToLowerCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"HelloWorld", "helloworld"},
		{"HELLO_WORLD", "helloworld"},
		{"hello_world", "helloworld"},
		{"HELLO", "hello"},
		{"", ""},
	}

	for _, test := range tests {
		result := ToLowerCase(test.input)
		if result != test.expected {
			t.Errorf("ToLowerCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToTitleCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello_world", "Hello World"},
		{"helloWorld", "Hello World"},
		{"HELLO_WORLD", "Hello World"},
		{"hello-world", "Hello World"},
		{"hello", "Hello"},
		{"", ""},
	}

	for _, test := range tests {
		result := ToTitleCase(test.input)
		if result != test.expected {
			t.Errorf("ToTitleCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToSentenceCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello_world", "Hello world"},
		{"helloWorld", "Hello world"},
		{"HELLO_WORLD", "Hello world"},
		{"hello-world", "Hello world"},
		{"hello", "Hello"},
		{"", ""},
	}

	for _, test := range tests {
		result := ToSentenceCase(test.input)
		if result != test.expected {
			t.Errorf("ToSentenceCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToDotCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"helloWorld", "hello.world"},
		{"HelloWorld", "hello.world"},
		{"hello_world", "hello.world"},
		{"hello-world", "hello.world"},
		{"helloWorldTest", "hello.world.test"},
		{"", ""},
	}

	for _, test := range tests {
		result := ToDotCase(test.input)
		if result != test.expected {
			t.Errorf("ToDotCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToPathCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"helloWorld", "hello/world"},
		{"HelloWorld", "hello/world"},
		{"hello_world", "hello/world"},
		{"hello-world", "hello/world"},
		{"helloWorldTest", "hello/world/test"},
		{"", ""},
	}

	for _, test := range tests {
		result := ToPathCase(test.input)
		if result != test.expected {
			t.Errorf("ToPathCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestToTrainCase(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"helloWorld", "Hello-World"},
		{"HelloWorld", "Hello-World"},
		{"hello_world", "Hello-World"},
		{"hello-world", "Hello-World"},
		{"helloWorldTest", "Hello-World-Test"},
		{"", ""},
	}

	for _, test := range tests {
		result := ToTrainCase(test.input)
		if result != test.expected {
			t.Errorf("ToTrainCase(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestDetectCase(t *testing.T) {
	tests := []struct {
		input    string
		expected CaseType
	}{
		{"helloWorld", CaseCamel},
		{"HelloWorld", CasePascal},
		{"hello_world", CaseSnake},
		{"hello-world", CaseKebab},
		{"HELLO_WORLD", CaseScreamingSnake},
		{"HELLO", CaseUpper},
		{"hello", CaseLower},
		{"Hello World", CaseTitle},
		{"", CaseUnknown},
	}

	for _, test := range tests {
		result := DetectCase(test.input)
		if result != test.expected {
			t.Errorf("DetectCase(%q) = %v, expected %v", test.input, result, test.expected)
		}
	}
}

func TestConvert(t *testing.T) {
	tests := []struct {
		input    string
		to       CaseType
		expected string
	}{
		{"hello_world", CaseCamel, "helloWorld"},
		{"hello_world", CasePascal, "HelloWorld"},
		{"HelloWorld", CaseSnake, "hello_world"},
		{"HelloWorld", CaseKebab, "hello-world"},
		{"helloWorld", CaseScreamingSnake, "HELLO_WORLD"},
		{"helloWorld", CaseUpper, "HELLOWORLD"},
		{"HelloWorld", CaseLower, "helloworld"},
		{"hello_world", CaseTitle, "Hello World"},
	}

	for _, test := range tests {
		result := Convert(test.input, test.to)
		if result != test.expected {
			t.Errorf("Convert(%q, %v) = %q, expected %q", test.input, test.to, result, test.expected)
		}
	}
}

func TestCaseTypeString(t *testing.T) {
	tests := []struct {
		caseType CaseType
		expected string
	}{
		{CaseCamel, "camelCase"},
		{CasePascal, "PascalCase"},
		{CaseSnake, "snake_case"},
		{CaseKebab, "kebab-case"},
		{CaseScreamingSnake, "SCREAMING_SNAKE_CASE"},
		{CaseUpper, "UPPERCASE"},
		{CaseLower, "lowercase"},
		{CaseTitle, "Title Case"},
		{CaseUnknown, "unknown"},
	}

	for _, test := range tests {
		result := test.caseType.String()
		if result != test.expected {
			t.Errorf("CaseType(%d).String() = %q, expected %q", test.caseType, result, test.expected)
		}
	}
}

func TestToConstantCase(t *testing.T) {
	// ToConstantCase should be same as ToScreamingSnakeCase
	input := "helloWorld"
	if ToConstantCase(input) != ToScreamingSnakeCase(input) {
		t.Errorf("ToConstantCase should equal ToScreamingSnakeCase")
	}
}

// Benchmark tests
func BenchmarkToCamelCase(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ToCamelCase("hello_world_test_case")
	}
}

func BenchmarkToSnakeCase(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ToSnakeCase("helloWorldTestCase")
	}
}

func BenchmarkDetectCase(b *testing.B) {
	for i := 0; i < b.N; i++ {
		DetectCase("helloWorldTestCase")
	}
}