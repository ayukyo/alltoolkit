package xml_utils

import (
	"strings"
	"testing"
)

func TestParseString(t *testing.T) {
	xml := `<?xml version="1.0" encoding="UTF-8"?>
<root>
	<item id="1">First</item>
	<item id="2">Second</item>
</root>`

	doc, err := ParseString(xml)
	if err != nil {
		t.Fatalf("Failed to parse XML: %v", err)
	}
	if doc.rootNode == nil {
		t.Fatal("Root node is nil")
	}
	if doc.rootNode.Tag != "root" {
		t.Errorf("Expected root tag 'root', got '%s'", doc.rootNode.Tag)
	}
}

func TestParseSimple(t *testing.T) {
	xml := `<root><item>value</item></root>`
	doc, err := ParseString(xml)
	if err != nil {
		t.Fatalf("Failed to parse: %v", err)
	}
	if doc.rootNode.Tag != "root" {
		t.Errorf("Expected 'root', got '%s'", doc.rootNode.Tag)
	}
}

func TestNewDocument(t *testing.T) {
	doc := NewDocument("configuration")
	if doc.rootNode.Tag != "configuration" {
		t.Errorf("Expected 'configuration', got '%s'", doc.rootNode.Tag)
	}
}

func TestToXML(t *testing.T) {
	doc := NewDocument("root")
	doc.Root().SetText("content")
	xml := doc.ToXML()
	if !strings.Contains(xml, "<root>") {
		t.Error("XML should contain <root>")
	}
}

func TestCreateElement(t *testing.T) {
	doc := NewDocument("root")
	child := doc.Root().CreateElement("child")
	child.SetText("Hello")
	if len(doc.Root().Children) != 1 {
		t.Errorf("Expected 1 child, got %d", len(doc.Root().Children))
	}
}

func TestSetAndGetAttr(t *testing.T) {
	doc := NewDocument("root")
	doc.Root().SetAttr("id", "123")
	if doc.Root().GetAttr("id") != "123" {
		t.Errorf("Expected '123', got '%s'", doc.Root().GetAttr("id"))
	}
}

func TestFindAll(t *testing.T) {
	xml := `<root><item>First</item><item>Second</item><item>Third</item></root>`
	doc, _ := ParseString(xml)
	items := doc.FindAll("item")
	if len(items) != 3 {
		t.Errorf("Expected 3 items, got %d", len(items))
	}
}

func TestIsValidXML(t *testing.T) {
	if !IsValidXML(`<root></root>`) {
		t.Error("Should be valid XML")
	}
	if IsValidXML("<invalid") {
		t.Error("Should be invalid XML")
	}
}

func TestStripXML(t *testing.T) {
	xml := `<root><item>Hello</item> <item>World</item></root>`
	text := StripXML(xml)
	if text != "Hello World" {
		t.Errorf("Expected 'Hello World', got '%s'", text)
	}
}
