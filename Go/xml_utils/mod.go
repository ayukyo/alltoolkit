// Package xml_utils provides comprehensive XML parsing and manipulation utilities.
// Zero dependencies, uses only Go standard library (encoding/xml).
package xml_utils

import (
	"bytes"
	"encoding/xml"
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
	"strings"
)

// XmlNode represents a node in the XML document tree.
type XmlNode struct {
	Tag        string
	Attributes map[string]string
	Content    string
	Children   []*XmlNode
	Parent     *XmlNode
	IsRoot     bool
}

// XmlDocument represents an XML document.
type XmlDocument struct {
	rootNode *XmlNode
	version  string
	encoding string
}

// ParseError represents an XML parsing error.
type ParseError struct {
	Message string
	Line    int
	Column  int
}

func (e *ParseError) Error() string {
	return fmt.Sprintf("XML parse error at line %d, column %d: %s", e.Line, e.Column, e.Message)
}

// ParseString parses XML from a string and returns an XmlDocument.
func ParseString(xmlString string) (*XmlDocument, error) {
	return ParseReader(strings.NewReader(xmlString))
}

// ParseFile parses XML from a file and returns an XmlDocument.
func ParseFile(filename string) (*XmlDocument, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	return ParseReader(file)
}

// ParseReader parses XML from an io.Reader and returns an XmlDocument.
func ParseReader(reader io.Reader) (*XmlDocument, error) {
	decoder := xml.NewDecoder(reader)
	doc := &XmlDocument{
		version:  "1.0",
		encoding: "UTF-8",
	}

	var current *XmlNode
	var stack []*XmlNode

	for {
		token, err := decoder.Token()
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, &ParseError{
				Message: err.Error(),
				Line:    int(decoder.InputOffset()),
			}
		}

		switch t := token.(type) {
		case xml.ProcInst:
			if t.Target == "xml" {
				content := string(t.Inst)
				if v := extractAttr(content, "version"); v != "" {
					doc.version = v
				}
				if e := extractAttr(content, "encoding"); e != "" {
					doc.encoding = e
				}
			}

		case xml.StartElement:
			node := &XmlNode{
				Tag:        t.Name.Local,
				Attributes: make(map[string]string),
				Children:   make([]*XmlNode, 0),
			}

			for _, attr := range t.Attr {
				node.Attributes[attr.Name.Local] = attr.Value
			}

			if current != nil {
				node.Parent = current
				current.Children = append(current.Children, node)
			} else {
				node.IsRoot = true
				doc.rootNode = node
			}

			current = node
			stack = append(stack, node)

		case xml.EndElement:
			if len(stack) > 0 {
				stack = stack[:len(stack)-1]
				if len(stack) > 0 {
					current = stack[len(stack)-1]
				} else {
					current = nil
				}
			}

		case xml.CharData:
			if current != nil {
				text := strings.TrimSpace(string(t))
				if text != "" {
					current.Content = text
				}
			}
		}
	}

	if doc.rootNode == nil {
		return nil, &ParseError{Message: "no root element found"}
	}

	return doc, nil
}

func extractAttr(content, name string) string {
	re := regexp.MustCompile(name + `=["']([^"']+)["']`)
	matches := re.FindStringSubmatch(content)
	if len(matches) > 1 {
		return matches[1]
	}
	return ""
}
// NewDocument creates a new XML document with the given root element name.
func NewDocument(rootName string) *XmlDocument {
	root := &XmlNode{
		Tag:        rootName,
		Attributes: make(map[string]string),
		Children:   make([]*XmlNode, 0),
		IsRoot:     true,
	}
	return &XmlDocument{
		rootNode: root,
		version:  "1.0",
		encoding: "UTF-8",
	}
}

// Root returns the root element of the document.
func (d *XmlDocument) Root() *XmlNode {
	return d.rootNode
}

// SetVersion sets the XML version declaration.
func (d *XmlDocument) SetVersion(version string) {
	d.version = version
}

// SetEncoding sets the XML encoding declaration.
func (d *XmlDocument) SetEncoding(encoding string) {
	d.encoding = encoding
}

// ToXML converts the document to a compact XML string.
func (d *XmlDocument) ToXML() string {
	var buf bytes.Buffer
	d.writeTo(&buf, "")
	return buf.String()
}

// ToPrettyXML converts the document to a pretty-printed XML string.
func (d *XmlDocument) ToPrettyXML(indent ...string) string {
	indentStr := "  "
	if len(indent) > 0 {
		indentStr = indent[0]
	}
	var buf bytes.Buffer
	d.writeTo(&buf, indentStr)
	return buf.String()
}

// writeTo writes the document to a buffer.
func (d *XmlDocument) writeTo(buf *bytes.Buffer, indent string) {
	if d.version != "" {
		buf.WriteString(fmt.Sprintf(`<?xml version="%s" encoding="%s"?>`+"\n", d.version, d.encoding))
	}
	if d.rootNode != nil {
		d.rootNode.writeTo(buf, "", indent)
	}
}

// SaveToFile saves the document to a file.
func (d *XmlDocument) SaveToFile(filename string, pretty bool) error {
	content := d.ToXML()
	if pretty {
		content = d.ToPrettyXML()
	}
	return os.WriteFile(filename, []byte(content), 0644)
}

// Find finds the first element matching the given path.
func (d *XmlDocument) Find(path string) *XmlNode {
	if d.rootNode == nil {
		return nil
	}
	parts := strings.Split(path, "/")
	return d.rootNode.find(parts, 0)
}

// FindAll finds all elements matching the given tag name anywhere in the document.
func (d *XmlDocument) FindAll(tagName string) []*XmlNode {
	if d.rootNode == nil {
		return []*XmlNode{}
	}
	return d.rootNode.findAll(tagName)
}

// FindByAttr finds the first element with the given attribute value.
func (d *XmlDocument) FindByAttr(tagName, attrName, attrValue string) *XmlNode {
	if d.rootNode == nil {
		return nil
	}
	return d.rootNode.findByAttr(tagName, attrName, attrValue)
}
// ==================== Node Methods ====================

// GetTagName returns the element tag name.
func (n *XmlNode) GetTagName() string {
	return n.Tag
}

// SetTagName sets the element tag name.
func (n *XmlNode) SetTagName(name string) {
	n.Tag = name
}

// Text returns the text content of the node.
func (n *XmlNode) Text() string {
	return n.Content
}

// SetText sets the text content of the node.
func (n *XmlNode) SetText(text string) {
	n.Content = text
}

// GetAttr returns the value of an attribute.
func (n *XmlNode) GetAttr(name string) string {
	if n.Attributes == nil {
		return ""
	}
	return n.Attributes[name]
}

// SetAttr sets an attribute value.
func (n *XmlNode) SetAttr(name, value string) {
	if n.Attributes == nil {
		n.Attributes = make(map[string]string)
	}
	n.Attributes[name] = value
}

// HasAttr checks if the node has an attribute.
func (n *XmlNode) HasAttr(name string) bool {
	if n.Attributes == nil {
		return false
	}
	_, exists := n.Attributes[name]
	return exists
}

// RemoveAttr removes an attribute.
func (n *XmlNode) RemoveAttr(name string) {
	if n.Attributes != nil {
		delete(n.Attributes, name)
	}
}

// Attrs returns all attributes as a map.
func (n *XmlNode) Attrs() map[string]string {
	if n.Attributes == nil {
		return make(map[string]string)
	}
	result := make(map[string]string)
	for k, v := range n.Attributes {
		result[k] = v
	}
	return result
}

// CreateElement creates a new child element.
func (n *XmlNode) CreateElement(tagName string) *XmlNode {
	child := &XmlNode{
		Tag:        tagName,
		Attributes: make(map[string]string),
		Children:   make([]*XmlNode, 0),
		Parent:     n,
	}
	n.Children = append(n.Children, child)
	return child
}

// AddChild adds a child node.
func (n *XmlNode) AddChild(child *XmlNode) {
	child.Parent = n
	n.Children = append(n.Children, child)
}

// RemoveChild removes a child node.
func (n *XmlNode) RemoveChild(child *XmlNode) bool {
	for i, c := range n.Children {
		if c == child {
			n.Children = append(n.Children[:i], n.Children[i+1:]...)
			child.Parent = nil
			return true
		}
	}
	return false
}

// Children returns all child nodes.
func (n *XmlNode) GetChildren() []*XmlNode {
	return n.Children
}

// ChildCount returns the number of child nodes.
func (n *XmlNode) ChildCount() int {
	return len(n.Children)
}

// Parent returns the parent node.
func (n *XmlNode) GetParent() *XmlNode {
	return n.Parent
}
// find recursively finds a node by path parts.
func (n *XmlNode) find(parts []string, index int) *XmlNode {
	if index >= len(parts) {
		return n
	}
	
	for _, child := range n.Children {
		if child.Tag == parts[index] {
			result := child.find(parts, index+1)
			if result != nil {
				return result
			}
		}
	}
	return nil
}

// findAll finds all nodes with the given tag name.
func (n *XmlNode) findAll(tagName string) []*XmlNode {
	var results []*XmlNode
	if n.Tag == tagName {
		results = append(results, n)
	}
	for _, child := range n.Children {
		results = append(results, child.findAll(tagName)...)
	}
	return results
}

// findByAttr finds a node by attribute value.
func (n *XmlNode) findByAttr(tagName, attrName, attrValue string) *XmlNode {
	if n.Tag == tagName {
		if n.GetAttr(attrName) == attrValue {
			return n
		}
	}
	for _, child := range n.Children {
		result := child.findByAttr(tagName, attrName, attrValue)
		if result != nil {
			return result
		}
	}
	return nil
}

// writeTo writes the node to a buffer.
func (n *XmlNode) writeTo(buf *bytes.Buffer, prefix, indent string) {
	if indent != "" {
		buf.WriteString(prefix)
	}
	
	buf.WriteString("<" + n.Tag)
	
	// Write attributes
	for key, value := range n.Attributes {
		buf.WriteString(fmt.Sprintf(` %s="%s"`, key, escapeXML(value)))
	}
	
	if len(n.Children) == 0 && n.Content == "" {
		buf.WriteString("/>")
		if indent != "" {
			buf.WriteString("\n")
		}
		return
	}
	
	buf.WriteString(">")
	
	if len(n.Children) == 0 {
		buf.WriteString(escapeXML(n.Content))
		buf.WriteString("</" + n.Tag + ">")
		if indent != "" {
			buf.WriteString("\n")
		}
		return
	}
	
	if indent != "" {
		buf.WriteString("\n")
	}
	
	for _, child := range n.Children {
		child.writeTo(buf, prefix+indent, indent)
	}
	
	if indent != "" {
		buf.WriteString(prefix)
	}
	buf.WriteString("</" + n.Tag + ">")
	if indent != "" {
		buf.WriteString("\n")
	}
}

// escapeXML escapes special XML characters.
func escapeXML(s string) string {
	s = strings.ReplaceAll(s, "&", "&amp;")
	s = strings.ReplaceAll(s, "<", "&lt;")
	s = strings.ReplaceAll(s, ">", "&gt;")
	s = strings.ReplaceAll(s, "\"", "&quot;")
	s = strings.ReplaceAll(s, "'", "&apos;")
	return s
}
// ==================== Utility Functions ====================

// IsValidXML checks if a string is valid XML.
func IsValidXML(xmlString string) bool {
	_, err := ParseString(xmlString)
	return err == nil
}

// StripXML removes all XML tags and returns plain text.
func StripXML(xmlString string) string {
	doc, err := ParseString(xmlString)
	if err != nil {
		return ""
	}
	return extractText(doc.rootNode)
}

// extractText recursively extracts text from a node.
func extractText(n *XmlNode) string {
	var result strings.Builder
	if n.Content != "" {
		result.WriteString(n.Content + " ")
	}
	for _, child := range n.Children {
		result.WriteString(extractText(child))
	}
	return strings.TrimSpace(result.String())
}

// ToMap converts the XML document to a nested map structure.
func (d *XmlDocument) ToMap() map[string]interface{} {
	if d.rootNode == nil {
		return nil
	}
	return nodeToMap(d.rootNode)
}

// nodeToMap converts a node to a map.
func nodeToMap(n *XmlNode) map[string]interface{} {
	result := make(map[string]interface{})
	
	// Add attributes with @ prefix
	for key, value := range n.Attributes {
		result["@"+key] = value
	}
	
	// Add text content
	if n.Content != "" {
		result["#text"] = n.Content
	}
	
	// Add children
	for _, child := range n.Children {
		childMap := nodeToMap(child)
		if existing, ok := result[child.Tag]; ok {
			// Multiple children with same tag - convert to array
			if arr, isArr := existing.([]map[string]interface{}); isArr {
				result[child.Tag] = append(arr, childMap)
			} else {
				result[child.Tag] = []map[string]interface{}{existing.(map[string]interface{}), childMap}
			}
		} else {
			result[child.Tag] = childMap
		}
	}
	
	return result
}

// GetTextByTag returns the text content of the first element with the given tag.
func (d *XmlDocument) GetTextByTag(tagName string) string {
	node := d.Find(tagName)
	if node != nil {
		return node.Text()
	}
	return ""
}

// GetAttrByTag returns the attribute value of the first element with the given tag.
func (d *XmlDocument) GetAttrByTag(tagName, attrName string) string {
	node := d.Find(tagName)
	if node != nil {
		return node.GetAttr(attrName)
	}
	return ""
}

// GetIntAttr returns an attribute as integer.
func (n *XmlNode) GetIntAttr(name string, defaultValue int) int {
	val := n.GetAttr(name)
	if val == "" {
		return defaultValue
	}
	result, err := strconv.Atoi(val)
	if err != nil {
		return defaultValue
	}
	return result
}

// GetFloatAttr returns an attribute as float64.
func (n *XmlNode) GetFloatAttr(name string, defaultValue float64) float64 {
	val := n.GetAttr(name)
	if val == "" {
		return defaultValue
	}
	result, err := strconv.ParseFloat(val, 64)
	if err != nil {
		return defaultValue
	}
	return result
}

// GetBoolAttr returns an attribute as bool.
func (n *XmlNode) GetBoolAttr(name string, defaultValue bool) bool {
	val := n.GetAttr(name)
	if val == "" {
		return defaultValue
	}
	result, err := strconv.ParseBool(val)
	if err != nil {
		return defaultValue
	}
	return result
}
