"""
BBCode Utilities - Zero-dependency BBCode parser and converter

Supports common BBCode tags with parsing, validation, and conversion to HTML or plain text.

Features:
- Parse BBCode to structured AST
- Convert BBCode to HTML
- Convert BBCode to plain text
- Validate BBCode syntax
- Support for nested tags
- Custom tag handlers
- Tag whitelisting for security

Author: AllToolkit
Date: 2026-05-11
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Tuple, Any
from enum import Enum


class BBCodeNodeType(Enum):
    """Types of nodes in the BBCode AST"""
    TEXT = "text"
    TAG = "tag"


@dataclass
class BBCodeNode:
    """A node in the BBCode AST"""
    type: BBCodeNodeType
    content: str = ""  # For TEXT nodes
    tag_name: str = ""  # For TAG nodes
    attributes: Dict[str, str] = field(default_factory=dict)
    children: List[Any] = field(default_factory=list)  # List[BBCodeNode]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary representation"""
        if self.type == BBCodeNodeType.TEXT:
            return {"type": "text", "content": self.content}
        return {
            "type": "tag",
            "tag": self.tag_name,
            "attributes": self.attributes,
            "children": [child.to_dict() for child in self.children]
        }


# Default supported BBCode tags with their HTML equivalents
DEFAULT_TAGS = {
    "b": {"html": "<strong>{content}</strong>", "desc": "Bold text"},
    "i": {"html": "<em>{content}</em>", "desc": "Italic text"},
    "u": {"html": "<u>{content}</u>", "desc": "Underline"},
    "s": {"html": "<del>{content}</del>", "desc": "Strikethrough"},
    "url": {"html": '<a href="{url}">{content}</a>', "default_attr": "url", "desc": "Hyperlink"},
    "img": {"html": '<img src="{content}" alt="Image">', "self_closing": True, "desc": "Image"},
    "quote": {"html": '<blockquote>{content}</blockquote>', "desc": "Quote"},
    "code": {"html": "<pre><code>{content}</code></pre>", "desc": "Code block"},
    "size": {"html": '<span style="font-size:{size}px">{content}</span>', "default_attr": "size", "desc": "Font size"},
    "color": {"html": '<span style="color:{color}">{content}</span>', "default_attr": "color", "desc": "Text color"},
    "center": {"html": '<div style="text-align:center">{content}</div>', "desc": "Center align"},
    "left": {"html": '<div style="text-align:left">{content}</div>', "desc": "Left align"},
    "right": {"html": '<div style="text-align:right">{content}</div>', "desc": "Right align"},
    "list": {"html": "<ul>{content}</ul>", "desc": "Unordered list"},
    "olist": {"html": "<ol>{content}</ol>", "desc": "Ordered list"},
    "*": {"html": "<li>{content}</li>", "inline_text": True, "desc": "List item"},
    "li": {"html": "<li>{content}</li>", "desc": "List item"},
    "table": {"html": "<table>{content}</table>", "desc": "Table"},
    "tr": {"html": "<tr>{content}</tr>", "desc": "Table row"},
    "td": {"html": "<td>{content}</td>", "desc": "Table cell"},
    "th": {"html": "<th>{content}</th>", "desc": "Table header"},
    "spoiler": {"html": '<details><summary>Spoiler</summary>{content}</details>', "desc": "Spoiler"},
    "hr": {"html": "<hr>", "self_closing": True, "desc": "Horizontal rule"},
    "br": {"html": "<br>", "self_closing": True, "desc": "Line break"},
    "email": {"html": '<a href="mailto:{email}">{content}</a>', "default_attr": "email", "desc": "Email link"},
    "font": {"html": '<span style="font-family:{font}">{content}</span>', "default_attr": "font", "desc": "Font family"},
    "sub": {"html": "<sub>{content}</sub>", "desc": "Subscript"},
    "sup": {"html": "<sup>{content}</sup>", "desc": "Superscript"},
}


class BBCodeParser:
    """
    BBCode parser that converts BBCode text to structured AST.
    
    Example:
        parser = BBCodeParser()
        ast = parser.parse("[b]Hello [i]World[/i][/b]")
        html = parser.to_html(ast)
        text = parser.to_text(ast)
    """
    
    # Regex patterns for BBCode parsing
    OPEN_TAG = re.compile(r'\[([a-zA-Z*]+)(?:=([^\]]+))?\]', re.IGNORECASE)
    CLOSE_TAG = re.compile(r'\[/([a-zA-Z*]+)\]', re.IGNORECASE)
    
    def __init__(self, allowed_tags=None):
        """
        Initialize parser with allowed tags.
        
        Args:
            allowed_tags: Dictionary of allowed tags and their configurations.
                         If None, uses DEFAULT_TAGS.
        """
        self.allowed_tags = allowed_tags if allowed_tags is not None else DEFAULT_TAGS.copy()
        self.custom_handlers = {}  # type: Dict[str, Callable]
    
    def register_handler(self, tag_name, handler):
        """
        Register a custom handler for a tag.
        
        Args:
            tag_name: Name of the tag (lowercase)
            handler: Function that takes (content, attributes, children) and returns string
        """
        self.custom_handlers[tag_name.lower()] = handler
    
    def parse(self, text):
        """
        Parse BBCode text into an AST.
        
        Args:
            text: BBCode formatted text
            
        Returns:
            Root BBCodeNode containing the parsed AST
        """
        root = BBCodeNode(type=BBCodeNodeType.TAG, tag_name="root")
        self._parse_recursive(text, root)
        return root
    
    def _parse_recursive(self, text, parent):
        """Recursively parse BBCode text into nodes"""
        pos = 0
        text_len = len(text)
        
        while pos < text_len:
            # Find next tag
            open_match = self.OPEN_TAG.search(text, pos)
            close_match = self.CLOSE_TAG.search(text, pos)
            
            # Determine which comes first
            if close_match and (not open_match or close_match.start() < open_match.start()):
                # Close tag comes first - return to parent
                tag_name = close_match.group(1).lower()
                if tag_name == parent.tag_name.lower():
                    # Add any remaining text before returning
                    if pos < close_match.start():
                        parent.children.append(BBCodeNode(
                            type=BBCodeNodeType.TEXT,
                            content=text[pos:close_match.start()]
                        ))
                    return
                else:
                    # Mismatched close tag - treat as text
                    parent.children.append(BBCodeNode(
                        type=BBCodeNodeType.TEXT,
                        content=text[pos:close_match.end()]
                    ))
                    pos = close_match.end()
                continue
            
            if not open_match:
                # No more tags - add remaining text
                if pos < text_len:
                    parent.children.append(BBCodeNode(
                        type=BBCodeNodeType.TEXT,
                        content=text[pos:]
                    ))
                break
            
            # Add text before tag
            if pos < open_match.start():
                parent.children.append(BBCodeNode(
                    type=BBCodeNodeType.TEXT,
                    content=text[pos:open_match.start()]
                ))
            
            tag_name = open_match.group(1).lower()
            attr_value = open_match.group(2)
            
            # Check if tag is allowed
            if tag_name not in self.allowed_tags:
                # For unknown tags, skip the tag itself but parse content
                # Find matching close tag for the unknown tag
                close_pos = self._find_close_tag(text, open_match.end(), tag_name)
                if close_pos != -1:
                    # Parse the content inside unknown tag
                    inner_text = text[open_match.end():close_pos]
                    self._parse_recursive(inner_text, parent)
                    pos = close_pos + len("[/{}]".format(tag_name))
                else:
                    # No close tag - skip just the open tag, continue parsing
                    pos = open_match.end()
                continue
            
            tag_config = self.allowed_tags.get(tag_name, {})
            
            # Handle self-closing tags
            if tag_config.get("self_closing"):
                node = BBCodeNode(
                    type=BBCodeNodeType.TAG,
                    tag_name=tag_name
                )
                if attr_value:
                    default_attr = tag_config.get("default_attr", "value")
                    node.attributes[default_attr] = attr_value
                # Content for self-closing is the attr value (like img)
                if attr_value and tag_name == "img":
                    node.children.append(BBCodeNode(type=BBCodeNodeType.TEXT, content=attr_value))
                parent.children.append(node)
                pos = open_match.end()
                continue
            
            # Handle inline_text tags (like [*] in lists)
            if tag_config.get("inline_text"):
                node = BBCodeNode(
                    type=BBCodeNodeType.TAG,
                    tag_name=tag_name
                )
                # Find the next tag position to get inline text content
                next_tag = self.OPEN_TAG.search(text, open_match.end())
                next_close = self.CLOSE_TAG.search(text, open_match.end())
                
                if next_tag and (not next_close or next_tag.start() < next_close.start()):
                    # Next open tag comes first - content is text until that tag
                    inline_content = text[open_match.end():next_tag.start()].strip()
                elif next_close:
                    # Close tag comes first - content is text until close tag (for parent)
                    inline_content = text[open_match.end():next_close.start()].strip()
                else:
                    # No more tags - rest is content
                    inline_content = text[open_match.end():].strip()
                
                if inline_content:
                    node.children.append(BBCodeNode(type=BBCodeNodeType.TEXT, content=inline_content))
                
                parent.children.append(node)
                # Update position based on content
                if next_tag and (not next_close or next_tag.start() < next_close.start()):
                    pos = next_tag.start()
                elif next_close:
                    pos = next_close.start()
                else:
                    pos = text_len
                continue
            
            # Find matching close tag
            close_pos = self._find_close_tag(text, open_match.end(), tag_name)
            
            if close_pos == -1:
                # No close tag - treat as text
                parent.children.append(BBCodeNode(
                    type=BBCodeNodeType.TEXT,
                    content=open_match.group(0)
                ))
                pos = open_match.end()
                continue
            
            # Create tag node
            node = BBCodeNode(
                type=BBCodeNodeType.TAG,
                tag_name=tag_name
            )
            
            # Set attributes
            if attr_value:
                default_attr = tag_config.get("default_attr", "value")
                node.attributes[default_attr] = attr_value
            
            # Recursively parse content
            inner_text = text[open_match.end():close_pos]
            self._parse_recursive(inner_text, node)
            
            parent.children.append(node)
            pos = close_pos + len("[/{}]".format(tag_name))
        
    def _find_close_tag(self, text, start, tag_name):
        """Find the position of the matching close tag, handling nesting"""
        depth = 1
        pos = start
        open_pattern = re.compile(r'\[{}(?:=[^\]]+)?\]'.format(tag_name), re.IGNORECASE)
        close_pattern = re.compile(r'\[/{}\]'.format(tag_name), re.IGNORECASE)
        
        while pos < len(text) and depth > 0:
            next_open = open_pattern.search(text, pos)
            next_close = close_pattern.search(text, pos)
            
            if next_close is None:
                return -1
            
            if next_open and next_open.start() < next_close.start():
                depth += 1
                pos = next_open.end()
            else:
                depth -= 1
                if depth == 0:
                    return next_close.start()
                pos = next_close.end()
        
        return -1 if depth > 0 else pos
    
    def to_html(self, node, strip_disallowed=True):
        """
        Convert AST node to HTML.
        
        Args:
            node: Root node to convert
            strip_disallowed: Whether to strip tags not in allowed_tags
            
        Returns:
            HTML string
        """
        if node.type == BBCodeNodeType.TEXT:
            return self._escape_html(node.content)
        
        if node.tag_name == "root":
            return "".join(self.to_html(child, strip_disallowed) for child in node.children)
        
        tag_config = self.allowed_tags.get(node.tag_name, {})
        
        if strip_disallowed and node.tag_name not in self.allowed_tags:
            return "".join(self.to_html(child, strip_disallowed) for child in node.children)
        
        # Check for custom handler
        if node.tag_name in self.custom_handlers:
            content = "".join(self.to_html(child, strip_disallowed) for child in node.children)
            return self.custom_handlers[node.tag_name](content, node.attributes, node.children)
        
        # Build content
        if tag_config.get("self_closing"):
            template = tag_config.get("html", "")
            return template
        
        content = "".join(self.to_html(child, strip_disallowed) for child in node.children)
        template = tag_config.get("html", "{content}")
        
        # Prepare template variables
        variables = {
            "content": content,
            **node.attributes
        }
        
        try:
            return template.format(**variables)
        except KeyError:
            # If template has variables not in attributes, use defaults
            return content
    
    def to_text(self, node):
        """
        Convert AST node to plain text, stripping BBCode tags.
        
        Args:
            node: Root node to convert
            
        Returns:
            Plain text string
        """
        if node.type == BBCodeNodeType.TEXT:
            return node.content
        
        if node.tag_name == "root":
            return "".join(self.to_text(child) for child in node.children)
        
        # Special handling for certain tags
        if node.tag_name == "br":
            return "\n"
        if node.tag_name == "hr":
            return "\n---\n"
        if node.tag_name == "img":
            url = node.attributes.get("url", "")
            return "[Image: {}]".format(url) if url else "[Image]"
        if node.tag_name == "url":
            url = node.attributes.get("url", "")
            text = "".join(self.to_text(child) for child in node.children)
            return text if text else url
        
        # Default: just return children's text
        return "".join(self.to_text(child) for child in node.children)
    
    def to_dict(self, node):
        """Convert AST to dictionary representation"""
        return node.to_dict()
    
    def _escape_html(self, text):
        """Escape special HTML characters"""
        replacements = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    def validate(self, text):
        """
        Validate BBCode syntax.
        
        Args:
            text: BBCode text to validate
            
        Returns:
            Tuple of (is_valid, list of errors)
        """
        errors = []
        tag_stack = []
        
        # Find all tags
        pos = 0
        while pos < len(text):
            open_match = self.OPEN_TAG.search(text, pos)
            close_match = self.CLOSE_TAG.search(text, pos)
            
            if not open_match and not close_match:
                break
            
            # Process whichever comes first
            if close_match and (not open_match or close_match.start() < open_match.start()):
                tag_name = close_match.group(1).lower()
                
                # Check if tag is in allowed list
                if tag_name in self.allowed_tags:
                    tag_config = self.allowed_tags[tag_name]
                    if not tag_config.get("self_closing"):
                        if not tag_stack:
                            errors.append("Unexpected closing tag: [/{}]".format(tag_name))
                        elif tag_stack[-1] != tag_name:
                            errors.append("Mismatched tags: expected [/{}], got [/{}]".format(tag_stack[-1], tag_name))
                        else:
                            tag_stack.pop()
                
                pos = close_match.end()
            else:
                tag_name = open_match.group(1).lower()
                
                if tag_name in self.allowed_tags:
                    tag_config = self.allowed_tags[tag_name]
                    if not tag_config.get("self_closing"):
                        tag_stack.append(tag_name)
                
                pos = open_match.end()
        
        # Check for unclosed tags
        for tag in tag_stack:
            errors.append("Unclosed tag: [{}]".format(tag))
        
        return len(errors) == 0, errors


def parse(text, allowed_tags=None):
    """Parse BBCode text to AST"""
    parser = BBCodeParser(allowed_tags)
    return parser.parse(text)


def to_html(text, allowed_tags=None):
    """Convert BBCode text directly to HTML"""
    parser = BBCodeParser(allowed_tags)
    ast = parser.parse(text)
    return parser.to_html(ast)


def to_text(text, allowed_tags=None):
    """Convert BBCode text directly to plain text"""
    parser = BBCodeParser(allowed_tags)
    ast = parser.parse(text)
    return parser.to_text(ast)


def validate(text, allowed_tags=None):
    """Validate BBCode syntax"""
    parser = BBCodeParser(allowed_tags)
    return parser.validate(text)


def get_supported_tags():
    """Get dictionary of all supported tags with descriptions"""
    return DEFAULT_TAGS.copy()


def create_safe_parser():
    """Create a parser with only safe, basic tags (no URLs or images)"""
    safe_tags = {
        "b": DEFAULT_TAGS["b"],
        "i": DEFAULT_TAGS["i"],
        "u": DEFAULT_TAGS["u"],
        "s": DEFAULT_TAGS["s"],
        "quote": DEFAULT_TAGS["quote"],
        "code": DEFAULT_TAGS["code"],
        "list": DEFAULT_TAGS["list"],
        "olist": DEFAULT_TAGS["olist"],
        "*": DEFAULT_TAGS["*"],
    }
    return BBCodeParser(safe_tags)


# Convenience function for quick conversion
def bbcode(text, output_format="html"):
    """
    Quick BBCode conversion.
    
    Args:
        text: BBCode formatted text
        output_format: "html", "text", or "ast" (JSON-like dict as string)
        
    Returns:
        Converted string
    """
    import json
    
    parser = BBCodeParser()
    ast = parser.parse(text)
    
    if output_format == "html":
        return parser.to_html(ast)
    elif output_format == "text":
        return parser.to_text(ast)
    elif output_format == "ast":
        return json.dumps(parser.to_dict(ast), indent=2)
    else:
        raise ValueError("Unknown output format: {}".format(output_format))