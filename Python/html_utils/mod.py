"""
AllToolkit - Python HTML Utilities

A zero-dependency HTML parsing, manipulation, and generation utility module.
Supports HTML parsing, element extraction, attribute manipulation, content sanitization,
and HTML generation using only Python standard library.

Author: AllToolkit
License: MIT
"""

from html.parser import HTMLParser
from html import escape, unescape
from typing import Optional, List, Dict, Any, Tuple, Set, Callable
from dataclasses import dataclass, field
from enum import Enum
import re


class HTMLElementType(Enum):
    """Types of HTML elements."""
    TAG = "tag"
    TEXT = "text"
    COMMENT = "comment"
    DOCTYPE = "doctype"


@dataclass
class HTMLElement:
    """Represents an HTML element."""
    tag: str
    attributes: Dict[str, str] = field(default_factory=dict)
    children: List['HTMLElement'] = field(default_factory=list)
    text: str = ""
    element_type: HTMLElementType = HTMLElementType.TAG
    parent: Optional['HTMLElement'] = None
    
    def __repr__(self) -> str:
        if self.element_type == HTMLElementType.TEXT:
            return f"Text('{self.text[:50]}...')" if len(self.text) > 50 else f"Text('{self.text}')"
        elif self.element_type == HTMLElementType.COMMENT:
            return f"Comment('{self.text[:50]}...')" if len(self.text) > 50 else f"Comment('{self.text}')"
        return f"<{self.tag}{self._attrs_str()}>"
    
    def _attrs_str(self) -> str:
        if not self.attributes:
            return ""
        attrs = " ".join(f'{k}="{v}"' for k, v in self.attributes.items())
        return f" {attrs}"
    
    def get_attribute(self, name: str, default: Any = None) -> Any:
        """Get an attribute value."""
        return self.attributes.get(name, default)
    
    def set_attribute(self, name: str, value: str) -> None:
        """Set an attribute value."""
        self.attributes[name] = value
    
    def remove_attribute(self, name: str) -> bool:
        """Remove an attribute. Returns True if it existed."""
        if name in self.attributes:
            del self.attributes[name]
            return True
        return False
    
    def has_class(self, class_name: str) -> bool:
        """Check if element has a specific CSS class."""
        classes = self.attributes.get("class", "").split()
        return class_name in classes
    
    def add_class(self, class_name: str) -> None:
        """Add a CSS class."""
        classes = set(self.attributes.get("class", "").split())
        classes.add(class_name)
        self.attributes["class"] = " ".join(sorted(classes))
    
    def remove_class(self, class_name: str) -> bool:
        """Remove a CSS class. Returns True if it existed."""
        classes = self.attributes.get("class", "").split()
        if class_name in classes:
            classes.remove(class_name)
            self.attributes["class"] = " ".join(classes)
            return True
        return False
    
    def get_text(self, include_children: bool = True) -> str:
        """Get text content of the element."""
        if self.element_type == HTMLElementType.TEXT:
            return self.text
        if not include_children:
            return self.text
        text_parts = [self.text]
        for child in self.children:
            text_parts.append(child.get_text())
        return "".join(text_parts)
    
    def to_html(self, indent: int = 0, pretty: bool = False) -> str:
        """Convert element to HTML string."""
        if self.element_type == HTMLElementType.TEXT:
            return escape(self.text)
        elif self.element_type == HTMLElementType.COMMENT:
            return f"<!-- {self.text} -->"
        elif self.element_type == HTMLElementType.DOCTYPE:
            return f"<!DOCTYPE {self.text}>"
        
        # Self-closing tags
        self_closing = {"area", "base", "br", "col", "embed", "hr", "img", 
                       "input", "link", "meta", "param", "source", "track", "wbr"}
        
        indent_str = "  " * indent if pretty else ""
        attrs_str = self._attrs_str()
        
        if self.tag.lower() in self_closing:
            return f"{indent_str}<{self.tag}{attrs_str}>"
        
        content = self.text
        for child in self.children:
            content += child.to_html(indent + 1, pretty) if pretty else child.to_html()
        
        if pretty and content:
            content = "\n" + content + "\n" + indent_str
        
        return f"{indent_str}<{self.tag}{attrs_str}>{content}</{self.tag}>"


class HTMLTreeBuilder(HTMLParser):
    """
    Build a tree structure from HTML content.
    """
    
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = HTMLElement(tag="root", element_type=HTMLElementType.TAG)
        self._stack: List[HTMLElement] = [self.root]
        self._current: HTMLElement = self.root
    
    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        element = HTMLElement(
            tag=tag.lower(),
            attributes={k: (v if v is not None else "") for k, v in attrs},
            parent=self._current
        )
        self._current.children.append(element)
        self._stack.append(element)
        self._current = element
    
    def handle_endtag(self, tag: str) -> None:
        if len(self._stack) > 1:
            self._stack.pop()
            self._current = self._stack[-1]
    
    def handle_data(self, data: str) -> None:
        if data.strip():
            text_element = HTMLElement(
                tag="#text",
                text=data,
                element_type=HTMLElementType.TEXT,
                parent=self._current
            )
            self._current.children.append(text_element)
    
    def handle_comment(self, data: str) -> None:
        comment_element = HTMLElement(
            tag="#comment",
            text=data,
            element_type=HTMLElementType.COMMENT,
            parent=self._current
        )
        self._current.children.append(comment_element)
    
    def handle_decl(self, decl: str) -> None:
        if decl.upper().startswith("DOCTYPE"):
            doctype = decl[7:].strip()
            doctype_element = HTMLElement(
                tag="!DOCTYPE",
                text=doctype,
                element_type=HTMLElementType.DOCTYPE,
                parent=self._current
            )
            self._current.children.append(doctype_element)
    
    def get_tree(self) -> HTMLElement:
        """Get the root of the tree."""
        return self.root


def parse_html(html_content: str) -> HTMLElement:
    """
    Parse HTML content and return a tree structure.
    
    Args:
        html_content: HTML string to parse
        
    Returns:
        HTMLElement representing the root of the tree
    """
    builder = HTMLTreeBuilder()
    builder.feed(html_content)
    return builder.get_tree()


def find_elements(root: HTMLElement, tag: Optional[str] = None,
                  attributes: Optional[Dict[str, str]] = None,
                  text: Optional[str] = None) -> List[HTMLElement]:
    """
    Find elements matching criteria.
    
    Args:
        root: Root element to search from
        tag: Tag name to match (case-insensitive)
        attributes: Dict of attribute name/value pairs to match
        text: Text content to match (substring)
        
    Returns:
        List of matching elements
    """
    results = []
    
    def _search(element: HTMLElement) -> None:
        match = True
        
        if tag is not None and element.tag.lower() != tag.lower():
            match = False
        
        if attributes is not None:
            for attr_name, attr_value in attributes.items():
                if element.attributes.get(attr_name) != attr_value:
                    match = False
                    break
        
        if text is not None and element.element_type == HTMLElementType.TEXT:
            if text not in element.text:
                match = False
        elif text is not None:
            if text not in element.get_text():
                match = False
        
        if match and element.tag != "root":
            results.append(element)
        
        for child in element.children:
            _search(child)
    
    _search(root)
    return results


def find_by_id(root: HTMLElement, element_id: str) -> Optional[HTMLElement]:
    """
    Find an element by its ID attribute.
    
    Args:
        root: Root element to search from
        element_id: ID to find
        
    Returns:
        Matching element or None
    """
    results = find_elements(root, attributes={"id": element_id})
    return results[0] if results else None


def find_by_class(root: HTMLElement, class_name: str) -> List[HTMLElement]:
    """
    Find elements by CSS class name.
    
    Args:
        root: Root element to search from
        class_name: Class name to find
        
    Returns:
        List of matching elements
    """
    results = []
    
    def _search(element: HTMLElement) -> None:
        if element.has_class(class_name):
            results.append(element)
        for child in element.children:
            _search(child)
    
    _search(root)
    return results


def extract_links(html_content: str) -> List[Dict[str, str]]:
    """
    Extract all links from HTML content.
    
    Args:
        html_content: HTML string to parse
        
    Returns:
        List of dicts with 'href', 'text', and 'title' keys
    """
    root = parse_html(html_content)
    links = find_elements(root, tag="a")
    
    results = []
    for link in links:
        href = link.get_attribute("href", "")
        title = link.get_attribute("title", "")
        text = link.get_text().strip()
        results.append({
            "href": href,
            "text": text,
            "title": title
        })
    
    return results


def extract_images(html_content: str) -> List[Dict[str, str]]:
    """
    Extract all images from HTML content.
    
    Args:
        html_content: HTML string to parse
        
    Returns:
        List of dicts with 'src', 'alt', and 'title' keys
    """
    root = parse_html(html_content)
    images = find_elements(root, tag="img")
    
    results = []
    for img in images:
        src = img.get_attribute("src", "")
        alt = img.get_attribute("alt", "")
        title = img.get_attribute("title", "")
        results.append({
            "src": src,
            "alt": alt,
            "title": title
        })
    
    return results


def sanitize_html(html_content: str, allowed_tags: Optional[Set[str]] = None,
                  allowed_attributes: Optional[Dict[str, Set[str]]] = None,
                  remove_scripts: bool = True) -> str:
    """
    Sanitize HTML by removing dangerous tags and attributes.
    
    Args:
        html_content: HTML string to sanitize
        allowed_tags: Set of allowed tag names (None = allow all safe tags)
        allowed_attributes: Dict mapping tag names to sets of allowed attributes
        remove_scripts: Whether to remove script tags and event handlers
        
    Returns:
        Sanitized HTML string
    """
    # Default safe tags
    if allowed_tags is None:
        allowed_tags = {
            "p", "br", "hr", "h1", "h2", "h3", "h4", "h5", "h6",
            "ul", "ol", "li", "dl", "dt", "dd",
            "strong", "b", "em", "i", "u", "s", "strike",
            "a", "img", "blockquote", "code", "pre",
            "table", "thead", "tbody", "tr", "th", "td",
            "div", "span", "section", "article", "header", "footer"
        }
    
    # Default allowed attributes per tag
    if allowed_attributes is None:
        allowed_attributes = {
            "a": {"href", "title", "target", "rel"},
            "img": {"src", "alt", "title", "width", "height"},
            "*": {"class", "id", "style"}
        }
    
    # Event handler pattern
    event_pattern = re.compile(r'^on\w+$', re.IGNORECASE)
    
    root = parse_html(html_content)
    
    def _sanitize_element(element: HTMLElement) -> Optional[HTMLElement]:
        # Skip script, style, and other dangerous tags
        dangerous_tags = {"script", "style", "iframe", "object", "embed", "form", "input"}
        if remove_scripts and element.tag.lower() in dangerous_tags:
            return None
        
        # Check if tag is allowed
        if element.tag != "root" and element.tag.lower() not in allowed_tags:
            # Keep children but remove this tag
            result_children = []
            for child in element.children:
                sanitized = _sanitize_element(child)
                if sanitized:
                    result_children.append(sanitized)
            if element.element_type == HTMLElementType.TEXT:
                return element
            if not result_children:
                return None
            # Return children directly
            if len(result_children) == 1:
                return result_children[0]
            # Create a container
            container = HTMLElement(tag="span")
            container.children = result_children
            return container
        
        # Create sanitized element
        sanitized = HTMLElement(
            tag=element.tag,
            text=element.text,
            element_type=element.element_type
        )
        
        # Filter attributes
        for attr_name, attr_value in element.attributes.items():
            # Remove event handlers
            if remove_scripts and event_pattern.match(attr_name):
                continue
            
            # Check if attribute is allowed
            tag_allowed = allowed_attributes.get(element.tag.lower(), set())
            global_allowed = allowed_attributes.get("*", set())
            all_allowed = tag_allowed | global_allowed
            
            if not allowed_attributes or attr_name in all_allowed:
                # Additional safety: remove javascript: URLs
                if attr_name.lower() in {"href", "src", "action"}:
                    if attr_value.lower().strip().startswith("javascript:"):
                        continue
                sanitized.attributes[attr_name] = attr_value
        
        # Sanitize children
        for child in element.children:
            sanitized_child = _sanitize_element(child)
            if sanitized_child:
                sanitized.children.append(sanitized_child)
        
        return sanitized
    
    sanitized_root = _sanitize_element(root)
    if sanitized_root:
        # Skip the root wrapper
        content = ""
        for child in sanitized_root.children:
            content += child.to_html()
        return content
    return ""


def html_to_text(html_content: str, preserve_links: bool = False) -> str:
    """
    Convert HTML to plain text.
    
    Args:
        html_content: HTML string to convert
        preserve_links: Whether to preserve link text and URLs
        
    Returns:
        Plain text string
    """
    root = parse_html(html_content)
    
    def _extract_text(element: HTMLElement) -> str:
        if element.element_type == HTMLElementType.TEXT:
            return element.text
        if element.element_type == HTMLElementType.COMMENT:
            return ""
        
        text_parts = [element.text]
        
        for child in element.children:
            text_parts.append(_extract_text(child))
        
        # Add newlines for block elements
        block_elements = {"p", "div", "br", "h1", "h2", "h3", "h4", "h5", "h6",
                         "li", "tr", "blockquote", "pre", "hr"}
        if element.tag.lower() in block_elements:
            if element.tag.lower() == "br":
                text_parts.append("\n")
            elif element.tag.lower() == "hr":
                text_parts.append("\n---\n")
            else:
                text_parts.append("\n")
        
        return "".join(text_parts)
    
    text = _extract_text(root)
    # Clean up whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = text.strip()
    return text


def generate_tag(tag: str, content: str = "", attributes: Optional[Dict[str, str]] = None,
                 self_closing: bool = False) -> str:
    """
    Generate an HTML tag string.
    
    Args:
        tag: Tag name
        content: Inner content
        attributes: Dict of attributes
        self_closing: Whether this is a self-closing tag
        
    Returns:
        HTML tag string
    """
    attrs_str = ""
    if attributes:
        attrs_str = " " + " ".join(f'{k}="{escape(v, quote=True)}"' for k, v in attributes.items())
    
    self_closing_tags = {"area", "base", "br", "col", "embed", "hr", "img",
                        "input", "link", "meta", "param", "source", "track", "wbr"}
    
    if self_closing or tag.lower() in self_closing_tags:
        return f"<{tag}{attrs_str}>"
    
    return f"<{tag}{attrs_str}>{content}</{tag}>"


def generate_link(href: str, text: str, title: Optional[str] = None,
                  target: Optional[str] = None) -> str:
    """
    Generate an anchor tag.
    
    Args:
        href: Link URL
        text: Link text
        title: Optional title attribute
        target: Optional target attribute
        
    Returns:
        HTML anchor tag
    """
    attrs = {"href": href}
    if title:
        attrs["title"] = title
    if target:
        attrs["target"] = target
    return generate_tag("a", escape(text), attrs)


def generate_image(src: str, alt: str = "", title: Optional[str] = None,
                   width: Optional[int] = None, height: Optional[int] = None) -> str:
    """
    Generate an image tag.
    
    Args:
        src: Image URL
        alt: Alt text
        title: Optional title attribute
        width: Optional width
        height: Optional height
        
    Returns:
        HTML image tag
    """
    attrs = {"src": src, "alt": alt}
    if title:
        attrs["title"] = title
    if width:
        attrs["width"] = str(width)
    if height:
        attrs["height"] = str(height)
    return generate_tag("img", attributes=attrs, self_closing=True)


def generate_table(headers: List[str], rows: List[List[str]],
                   attributes: Optional[Dict[str, str]] = None) -> str:
    """
    Generate an HTML table.
    
    Args:
        headers: List of header cell texts
        rows: List of rows, each row is a list of cell texts
        attributes: Optional table attributes
        
    Returns:
        HTML table string
    """
    table_attrs = attributes or {}
    html = generate_tag("table", attributes=table_attrs)
    
    # Header row
    html += "<tr>"
    for header in headers:
        html += generate_tag("th", escape(str(header)))
    html += "</tr>"
    
    # Data rows
    for row in rows:
        html += "<tr>"
        for cell in row:
            html += generate_tag("td", escape(str(cell)))
        html += "</tr>"
    
    html += "</table>"
    return html


def generate_form(action: str, method: str = "post",
                  fields: Optional[List[Dict[str, Any]]] = None,
                  attributes: Optional[Dict[str, str]] = None) -> str:
    """
    Generate an HTML form.
    
    Args:
        action: Form action URL
        method: HTTP method (get/post)
        fields: List of field definitions (type, name, label, value, etc.)
        attributes: Optional form attributes
        
    Returns:
        HTML form string
    """
    form_attrs = attributes or {"action": action, "method": method}
    html = generate_tag("form", attributes=form_attrs)
    
    if fields:
        for field_def in fields:
            field_type = field_def.get("type", "text")
            field_name = field_def.get("name", "")
            field_label = field_def.get("label", "")
            field_value = field_def.get("value", "")
            field_attrs = field_def.get("attributes", {})
            
            field_attrs["name"] = field_name
            if field_value:
                field_attrs["value"] = str(field_value)
            
            if field_label:
                html += generate_tag("label", escape(field_label), {"for": field_name})
            
            # Add type attribute for input fields
            if field_type not in ("textarea", "select"):
                field_attrs["type"] = field_type
            
            if field_type == "textarea":
                html += generate_tag("textarea", escape(str(field_value)), field_attrs)
            elif field_type == "select":
                options = field_def.get("options", [])
                select_html = ""
                for opt in options:
                    opt_value = opt.get("value", "")
                    opt_text = opt.get("text", opt_value)
                    opt_attrs = {"value": opt_value}
                    if opt_value == str(field_value):
                        opt_attrs["selected"] = "selected"
                    select_html += generate_tag("option", escape(opt_text), opt_attrs)
                html += generate_tag("select", select_html, field_attrs)
            else:
                html += generate_tag("input", attributes=field_attrs, self_closing=True)
    
    html += "</form>"
    return html


def minify_html(html_content: str) -> str:
    """
    Minify HTML by removing unnecessary whitespace.
    
    Args:
        html_content: HTML string to minify
        
    Returns:
        Minified HTML string
    """
    # Remove comments
    html = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    
    # Remove whitespace between tags
    html = re.sub(r'>\s+<', '><', html)
    
    # Remove leading/trailing whitespace per line
    html = re.sub(r'^\s+|\s+$', '', html, flags=re.MULTILINE)
    
    return html.strip()


def prettify_html(html_content: str, indent_size: int = 2) -> str:
    """
    Prettify HTML with proper indentation.
    
    Args:
        html_content: HTML string to prettify
        indent_size: Number of spaces per indent level
        
    Returns:
        Prettified HTML string
    """
    # Simple prettification using parser
    root = parse_html(html_content)
    
    def _prettify(element: HTMLElement, level: int = 0) -> str:
        indent = " " * (indent_size * level)
        next_indent = " " * (indent_size * (level + 1))
        
        if element.element_type == HTMLElementType.TEXT:
            text = element.text.strip()
            return text if text else ""
        elif element.element_type == HTMLElementType.COMMENT:
            return f"{indent}<!-- {element.text} -->"
        elif element.element_type == HTMLElementType.DOCTYPE:
            return f"{indent}<!DOCTYPE {element.text}>"
        
        self_closing = {"area", "base", "br", "col", "embed", "hr", "img",
                       "input", "link", "meta", "param", "source", "track", "wbr"}
        
        attrs_str = element._attrs_str()
        
        if element.tag.lower() in self_closing:
            return f"{indent}<{element.tag}{attrs_str}>"
        
        # Get content
        content_parts = []
        if element.text.strip():
            content_parts.append(element.text.strip())
        
        for child in element.children:
            child_html = _prettify(child, level + 1)
            if child_html:
                content_parts.append(child_html)
        
        if not content_parts:
            return f"{indent}<{element.tag}{attrs_str}></{element.tag}>"
        
        content = "\n".join(content_parts)
        return f"{indent}<{element.tag}{attrs_str}>\n{next_indent}{content}\n{indent}</{element.tag}>"
    
    result_parts = []
    for child in root.children:
        html = _prettify(child)
        if html:
            result_parts.append(html)
    
    return "\n".join(result_parts)


# Convenience functions for common operations

def extract_title(html_content: str) -> Optional[str]:
    """Extract the page title from HTML."""
    root = parse_html(html_content)
    titles = find_elements(root, tag="title")
    if titles:
        return titles[0].get_text().strip()
    return None


def extract_meta(html_content: str, name: Optional[str] = None,
                 property: Optional[str] = None) -> Optional[str]:
    """Extract meta tag content by name or property."""
    root = parse_html(html_content)
    metas = find_elements(root, tag="meta")
    
    for meta in metas:
        if name and meta.get_attribute("name") == name:
            return meta.get_attribute("content")
        if property and meta.get_attribute("property") == property:
            return meta.get_attribute("content")
    
    return None


def count_tags(html_content: str) -> Dict[str, int]:
    """Count occurrences of each tag in HTML."""
    root = parse_html(html_content)
    counts: Dict[str, int] = {}
    
    def _count(element: HTMLElement) -> None:
        if element.tag != "root":
            counts[element.tag] = counts.get(element.tag, 0) + 1
        for child in element.children:
            _count(child)
    
    _count(root)
    return counts


def get_dom_depth(root: HTMLElement) -> int:
    """Get the maximum depth of the DOM tree."""
    if not root.children:
        return 0
    
    max_child_depth = 0
    for child in root.children:
        child_depth = get_dom_depth(child)
        max_child_depth = max(max_child_depth, child_depth)
    
    return 1 + max_child_depth


def validate_html_structure(html_content: str) -> Dict[str, Any]:
    """
    Validate basic HTML structure.
    
    Returns:
        Dict with validation results
    """
    root = parse_html(html_content)
    issues = []
    
    # Check for unclosed tags (parser handles most, but we can check structure)
    tag_stack: List[str] = []
    
    def _check(element: HTMLElement) -> None:
        if element.element_type != HTMLElementType.TAG:
            return
        
        # Self-closing tags
        self_closing = {"area", "base", "br", "col", "embed", "hr", "img",
                       "input", "link", "meta", "param", "source", "track", "wbr"}
        
        if element.tag.lower() not in self_closing:
            tag_stack.append(element.tag)
        
        for child in element.children:
            _check(child)
        
        if element.tag.lower() not in self_closing and tag_stack:
            tag_stack.pop()
    
    _check(root)
    
    if tag_stack:
        issues.append(f"Unclosed tags: {', '.join(tag_stack)}")
    
    # Check for duplicate IDs
    ids_seen: Set[str] = set()
    duplicate_ids = []
    
    def _find_ids(element: HTMLElement) -> None:
        element_id = element.get_attribute("id")
        if element_id:
            if element_id in ids_seen:
                duplicate_ids.append(element_id)
            ids_seen.add(element_id)
        for child in element.children:
            _find_ids(child)
    
    _find_ids(root)
    
    if duplicate_ids:
        issues.append(f"Duplicate IDs: {', '.join(set(duplicate_ids))}")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "depth": get_dom_depth(root),
        "tag_count": sum(count_tags(html_content).values())
    }
