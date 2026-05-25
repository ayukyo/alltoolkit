"""
RSS Utils - A comprehensive RSS/Atom feed parser and generator.

This module provides utilities for parsing, validating, and generating RSS 2.0
and Atom feeds without any external dependencies.

Features:
- Parse RSS 2.0 feeds
- Parse Atom feeds
- Generate RSS 2.0 feeds
- Generate Atom feeds
- Validate feed structure
- Extract feed entries with metadata
"""

import re
from html.parser import HTMLParser
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
from xml.etree import ElementTree as ET
from urllib.parse import urljoin, urlparse


class FeedEntry:
    """Represents a single entry in an RSS/Atom feed."""
    
    def __init__(
        self,
        title: str = "",
        link: str = "",
        description: str = "",
        author: str = "",
        email: str = "",
        published: Optional[datetime] = None,
        updated: Optional[datetime] = None,
        guid: str = "",
        categories: List[str] = None,
        enclosure_url: str = "",
        enclosure_type: str = "",
        enclosure_length: int = 0,
        content: str = "",
        id: str = ""
    ):
        self.title = title
        self.link = link
        self.description = description
        self.author = author
        self.email = email
        self.published = published
        self.updated = updated
        self.guid = guid
        self.categories = categories or []
        self.enclosure_url = enclosure_url
        self.enclosure_type = enclosure_type
        self.enclosure_length = enclosure_length
        self.content = content
        self.id = id or guid
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary."""
        return {
            "title": self.title,
            "link": self.link,
            "description": self.description,
            "author": self.author,
            "email": self.email,
            "published": self.published.isoformat() if self.published else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "guid": self.guid,
            "categories": self.categories,
            "enclosure_url": self.enclosure_url,
            "enclosure_type": self.enclosure_type,
            "enclosure_length": self.enclosure_length,
            "content": self.content,
            "id": self.id
        }
    
    def __repr__(self) -> str:
        return f"FeedEntry(title={self.title!r}, link={self.link!r})"


class FeedInfo:
    """Represents feed metadata."""
    
    def __init__(
        self,
        title: str = "",
        link: str = "",
        description: str = "",
        language: str = "",
        copyright: str = "",
        managing_editor: str = "",
        webmaster: str = "",
        published: Optional[datetime] = None,
        last_updated: Optional[datetime] = None,
        categories: List[str] = None,
        generator: str = "",
        image_url: str = "",
        image_title: str = "",
        image_link: str = "",
        feed_type: str = "rss",
        entries: List[FeedEntry] = None
    ):
        self.title = title
        self.link = link
        self.description = description
        self.language = language
        self.copyright = copyright
        self.managing_editor = managing_editor
        self.webmaster = webmaster
        self.published = published
        self.last_updated = last_updated
        self.categories = categories or []
        self.generator = generator
        self.image_url = image_url
        self.image_title = image_title
        self.image_link = image_link
        self.feed_type = feed_type
        self.entries = entries or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert feed info to dictionary."""
        return {
            "title": self.title,
            "link": self.link,
            "description": self.description,
            "language": self.language,
            "copyright": self.copyright,
            "managing_editor": self.managing_editor,
            "webmaster": self.webmaster,
            "published": self.published.isoformat() if self.published else None,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "categories": self.categories,
            "generator": self.generator,
            "image_url": self.image_url,
            "image_title": self.image_title,
            "image_link": self.image_link,
            "feed_type": self.feed_type,
            "entries": [e.to_dict() for e in self.entries]
        }
    
    def __repr__(self) -> str:
        return f"FeedInfo(title={self.title!r}, entries={len(self.entries)})"


class RSSParser:
    """Parser for RSS 2.0 feeds."""
    
    # Common RSS date formats
    DATE_FORMATS = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S GMT",
        "%a, %d %b %Y %H:%M:%S",
        "%d %b %Y %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
    ]
    
    @staticmethod
    def parse_date(date_str: str) -> Optional[datetime]:
        """Parse a date string into a datetime object."""
        if not date_str:
            return None
        
        date_str = date_str.strip()
        
        # Try ISO 8601 format first
        if 'T' in date_str:
            # Handle timezone offset
            date_str = re.sub(r'([+-]\d{2}):(\d{2})$', r'\1\2', date_str)
            date_str = re.sub(r'([+-]\d{2})(\d{2})$', r'\1:\2', date_str)
            
            for fmt in ["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"]:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
        
        # Try RSS formats
        for fmt in RSSParser.DATE_FORMATS:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None
    
    @staticmethod
    def get_text(element: Optional[ET.Element], path: str = "", default: str = "") -> str:
        """Get text content from an element."""
        if element is None:
            return default
        
        if path:
            child = element.find(path)
            if child is not None and child.text:
                return child.text.strip()
            return default
        
        return element.text.strip() if element.text else default
    
    @staticmethod
    def get_attr(element: Optional[ET.Element], attr: str, default: str = "") -> str:
        """Get attribute value from an element."""
        if element is None:
            return default
        return element.get(attr, default)
    
    @classmethod
    def parse(cls, content: str) -> FeedInfo:
        """Parse RSS content and return FeedInfo."""
        # Remove BOM and clean XML
        content = content.lstrip('\ufeff').strip()
        
        # Remove XML declaration for parsing
        content = re.sub(r'<\?xml[^>]*\?>', '', content, count=1)
        
        try:
            root = ET.fromstring(content)
        except ET.ParseError:
            # Try to fix common issues
            content = content.replace('&', '&amp;')
            content = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', content)
            root = ET.fromstring(content)
        
        # Find channel element
        channel = root.find('channel')
        if channel is None:
            channel = root
        
        feed_info = FeedInfo(feed_type="rss")
        
        # Parse channel info
        feed_info.title = cls.get_text(channel, 'title')
        feed_info.link = cls.get_text(channel, 'link')
        feed_info.description = cls.get_text(channel, 'description')
        feed_info.language = cls.get_text(channel, 'language')
        feed_info.copyright = cls.get_text(channel, 'copyright')
        feed_info.managing_editor = cls.get_text(channel, 'managingEditor')
        feed_info.webmaster = cls.get_text(channel, 'webMaster')
        feed_info.generator = cls.get_text(channel, 'generator')
        
        # Parse dates
        pub_date = cls.get_text(channel, 'pubDate')
        last_build = cls.get_text(channel, 'lastBuildDate')
        feed_info.published = cls.parse_date(pub_date)
        feed_info.last_updated = cls.parse_date(last_build)
        
        # Parse categories
        for cat in channel.findall('category'):
            cat_text = cat.text.strip() if cat.text else ""
            if cat_text:
                feed_info.categories.append(cat_text)
        
        # Parse image
        image = channel.find('image')
        if image is not None:
            feed_info.image_url = cls.get_text(image, 'url')
            feed_info.image_title = cls.get_text(image, 'title')
            feed_info.image_link = cls.get_text(image, 'link')
        
        # Parse items
        for item in channel.findall('item'):
            entry = FeedEntry()
            entry.title = cls.get_text(item, 'title')
            entry.link = cls.get_text(item, 'link')
            entry.description = cls.get_text(item, 'description')
            entry.author = cls.get_text(item, 'author')
            entry.guid = cls.get_text(item, 'guid')
            
            # Parse dates
            pub_date = cls.get_text(item, 'pubDate')
            entry.published = cls.parse_date(pub_date)
            
            # Parse categories
            for cat in item.findall('category'):
                cat_text = cat.text.strip() if cat.text else ""
                if cat_text:
                    entry.categories.append(cat_text)
            
            # Parse enclosure
            enclosure = item.find('enclosure')
            if enclosure is not None:
                entry.enclosure_url = cls.get_attr(enclosure, 'url')
                entry.enclosure_type = cls.get_attr(enclosure, 'type')
                try:
                    entry.enclosure_length = int(cls.get_attr(enclosure, 'length', '0'))
                except ValueError:
                    entry.enclosure_length = 0
            
            # Parse content:encoded
            content_elem = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
            if content_elem is not None and content_elem.text:
                entry.content = content_elem.text
            
            feed_info.entries.append(entry)
        
        return feed_info


class AtomParser:
    """Parser for Atom feeds."""
    
    NS = {'atom': 'http://www.w3.org/2005/Atom'}
    
    @staticmethod
    def parse_date(date_str: str) -> Optional[datetime]:
        """Parse ISO 8601 date string."""
        if not date_str:
            return None
        
        date_str = date_str.strip()
        
        # Handle Z suffix (UTC timezone)
        if date_str.endswith('Z'):
            date_str = date_str[:-1] + '+0000'
        
        # Handle timezone offset formats - convert +HH:MM to +HHMM for %z
        date_str = re.sub(r'([+-]\d{2}):(\d{2})$', r'\1\2', date_str)
        
        for fmt in ["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None
    
    @staticmethod
    def get_text(element: Optional[ET.Element], path: str = "", default: str = "") -> str:
        """Get text content from an element."""
        if element is None:
            return default
        
        if path:
            child = element.find(path)
            if child is not None and child.text:
                return child.text.strip()
            return default
        
        return element.text.strip() if element.text else default
    
    @staticmethod
    def get_attr(element: Optional[ET.Element], attr: str, default: str = "") -> str:
        """Get attribute value from an element."""
        if element is None:
            return default
        return element.get(attr, default)
    
    @classmethod
    def parse(cls, content: str) -> FeedInfo:
        """Parse Atom content and return FeedInfo."""
        content = content.lstrip('\ufeff').strip()
        
        try:
            root = ET.fromstring(content)
        except ET.ParseError:
            content = content.replace('&', '&amp;')
            content = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', content)
            root = ET.fromstring(content)
        
        feed_info = FeedInfo(feed_type="atom")
        
        # Parse feed info
        title = root.find('atom:title', cls.NS)
        if title is not None:
            feed_info.title = title.text.strip() if title.text else ""
        
        subtitle = root.find('atom:subtitle', cls.NS)
        if subtitle is not None:
            feed_info.description = subtitle.text.strip() if subtitle.text else ""
        
        # Parse link
        for link in root.findall('atom:link', cls.NS):
            rel = link.get('rel', 'alternate')
            if rel == 'alternate' or rel == 'self':
                feed_info.link = link.get('href', '')
                break
        
        # Parse generator
        generator = root.find('atom:generator', cls.NS)
        if generator is not None:
            feed_info.generator = generator.text.strip() if generator.text else ""
        
        # Parse dates
        updated = root.find('atom:updated', cls.NS)
        if updated is not None:
            feed_info.last_updated = cls.parse_date(updated.text or "")
        
        # Parse entries
        for entry_elem in root.findall('atom:entry', cls.NS):
            entry = FeedEntry()
            
            # Title
            title = entry_elem.find('atom:title', cls.NS)
            if title is not None:
                entry.title = title.text.strip() if title.text else ""
            
            # Link
            for link in entry_elem.findall('atom:link', cls.NS):
                rel = link.get('rel', 'alternate')
                if rel == 'alternate':
                    entry.link = link.get('href', '')
                    break
            
            # Content
            content_elem = entry_elem.find('atom:content', cls.NS)
            if content_elem is not None and content_elem.text:
                entry.content = content_elem.text
            
            # Summary (description)
            summary = entry_elem.find('atom:summary', cls.NS)
            if summary is not None and summary.text:
                entry.description = summary.text.strip()
            
            # Author
            author = entry_elem.find('atom:author', cls.NS)
            if author is not None:
                name = author.find('atom:name', cls.NS)
                if name is not None and name.text:
                    entry.author = name.text.strip()
                email = author.find('atom:email', cls.NS)
                if email is not None and email.text:
                    entry.email = email.text.strip()
            
            # ID
            id_elem = entry_elem.find('atom:id', cls.NS)
            if id_elem is not None and id_elem.text:
                entry.id = id_elem.text.strip()
                entry.guid = entry.id
            
            # Dates
            published = entry_elem.find('atom:published', cls.NS)
            if published is not None:
                entry.published = cls.parse_date(published.text or "")
            
            updated = entry_elem.find('atom:updated', cls.NS)
            if updated is not None:
                entry.updated = cls.parse_date(updated.text or "")
            
            # Categories
            for cat in entry_elem.findall('atom:category', cls.NS):
                term = cat.get('term', '')
                if term:
                    entry.categories.append(term)
            
            feed_info.entries.append(entry)
        
        return feed_info


class RSSGenerator:
    """Generator for RSS 2.0 feeds."""
    
    @staticmethod
    def escape_xml(text: str) -> str:
        """Escape special XML characters."""
        if not text:
            return ""
        text = str(text)
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&apos;')
        return text
    
    @staticmethod
    def format_date(dt: Optional[datetime]) -> str:
        """Format datetime for RSS."""
        if dt is None:
            return ""
        return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    @classmethod
    def generate(
        cls,
        title: str,
        link: str,
        description: str,
        entries: List[FeedEntry],
        language: str = "en",
        copyright: str = "",
        managing_editor: str = "",
        webmaster: str = "",
        image_url: str = "",
        categories: List[str] = None,
        generator: str = "RSS Utils",
        encoding: str = "utf-8"
    ) -> str:
        """Generate an RSS 2.0 feed."""
        categories = categories or []
        
        lines = [
            '<?xml version="1.0" encoding="' + encoding + '"?>',
            '<rss version="2.0">',
            '<channel>'
        ]
        
        # Channel info
        lines.append(f'<title>{cls.escape_xml(title)}</title>')
        lines.append(f'<link>{cls.escape_xml(link)}</link>')
        lines.append(f'<description>{cls.escape_xml(description)}</description>')
        
        if language:
            lines.append(f'<language>{cls.escape_xml(language)}</language>')
        if copyright:
            lines.append(f'<copyright>{cls.escape_xml(copyright)}</copyright>')
        if managing_editor:
            lines.append(f'<managingEditor>{cls.escape_xml(managing_editor)}</managingEditor>')
        if webmaster:
            lines.append(f'<webMaster>{cls.escape_xml(webmaster)}</webMaster>')
        if generator:
            lines.append(f'<generator>{cls.escape_xml(generator)}</generator>')
        
        lines.append(f'<lastBuildDate>{cls.format_date(datetime.utcnow())}</lastBuildDate>')
        
        # Image
        if image_url:
            lines.append('<image>')
            lines.append(f'<url>{cls.escape_xml(image_url)}</url>')
            lines.append(f'<title>{cls.escape_xml(title)}</title>')
            lines.append(f'<link>{cls.escape_xml(link)}</link>')
            lines.append('</image>')
        
        # Categories
        for cat in categories:
            lines.append(f'<category>{cls.escape_xml(cat)}</category>')
        
        # Items
        for entry in entries:
            lines.append('<item>')
            
            if entry.title:
                lines.append(f'<title>{cls.escape_xml(entry.title)}</title>')
            if entry.link:
                lines.append(f'<link>{cls.escape_xml(entry.link)}</link>')
            if entry.description:
                lines.append(f'<description>{cls.escape_xml(entry.description)}</description>')
            if entry.author:
                lines.append(f'<author>{cls.escape_xml(entry.author)}</author>')
            if entry.guid:
                lines.append(f'<guid>{cls.escape_xml(entry.guid)}</guid>')
            elif entry.link:
                lines.append(f'<guid>{cls.escape_xml(entry.link)}</guid>')
            if entry.published:
                lines.append(f'<pubDate>{cls.format_date(entry.published)}</pubDate>')
            if entry.enclosure_url:
                lines.append(
                    f'<enclosure url="{cls.escape_xml(entry.enclosure_url)}" '
                    f'type="{cls.escape_xml(entry.enclosure_type)}" '
                    f'length="{entry.enclosure_length}" />'
                )
            
            for cat in entry.categories:
                lines.append(f'<category>{cls.escape_xml(cat)}</category>')
            
            lines.append('</item>')
        
        lines.append('</channel>')
        lines.append('</rss>')
        
        return '\n'.join(lines)


class AtomGenerator:
    """Generator for Atom feeds."""
    
    NS = 'http://www.w3.org/2005/Atom'
    
    @staticmethod
    def escape_xml(text: str) -> str:
        """Escape special XML characters."""
        if not text:
            return ""
        text = str(text)
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&apos;')
        return text
    
    @staticmethod
    def format_date(dt: Optional[datetime]) -> str:
        """Format datetime for Atom (ISO 8601)."""
        if dt is None:
            return ""
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    @classmethod
    def generate(
        cls,
        title: str,
        link: str,
        entries: List[FeedEntry],
        subtitle: str = "",
        author_name: str = "",
        author_email: str = "",
        id_base: str = "",
        categories: List[str] = None,
        generator: str = "RSS Utils",
        encoding: str = "utf-8"
    ) -> str:
        """Generate an Atom feed."""
        categories = categories or []
        
        lines = [
            '<?xml version="1.0" encoding="' + encoding + '"?>',
            f'<feed xmlns="{cls.NS}">'
        ]
        
        # Feed info
        lines.append(f'<title>{cls.escape_xml(title)}</title>')
        
        if subtitle:
            lines.append(f'<subtitle>{cls.escape_xml(subtitle)}</subtitle>')
        
        lines.append(f'<link href="{cls.escape_xml(link)}" rel="self" type="application/atom+xml" />')
        lines.append(f'<link href="{cls.escape_xml(link)}" />')
        
        if id_base:
            lines.append(f'<id>{cls.escape_xml(id_base)}</id>')
        else:
            lines.append(f'<id>{cls.escape_xml(link)}</id>')
        
        lines.append(f'<updated>{cls.format_date(datetime.utcnow())}</updated>')
        
        if generator:
            lines.append(f'<generator>{cls.escape_xml(generator)}</generator>')
        
        # Author
        if author_name or author_email:
            lines.append('<author>')
            if author_name:
                lines.append(f'<name>{cls.escape_xml(author_name)}</name>')
            if author_email:
                lines.append(f'<email>{cls.escape_xml(author_email)}</email>')
            lines.append('</author>')
        
        # Categories
        for cat in categories:
            lines.append(f'<category term="{cls.escape_xml(cat)}" />')
        
        # Entries
        for entry in entries:
            lines.append('<entry>')
            
            if entry.title:
                lines.append(f'<title>{cls.escape_xml(entry.title)}</title>')
            
            if entry.link:
                lines.append(f'<link href="{cls.escape_xml(entry.link)}" />')
            
            entry_id = entry.id or entry.guid or entry.link
            if entry_id:
                lines.append(f'<id>{cls.escape_xml(entry_id)}</id>')
            
            if entry.updated:
                lines.append(f'<updated>{cls.format_date(entry.updated)}</updated>')
            elif entry.published:
                lines.append(f'<updated>{cls.format_date(entry.published)}</updated>')
            else:
                lines.append(f'<updated>{cls.format_date(datetime.utcnow())}</updated>')
            
            if entry.published:
                lines.append(f'<published>{cls.format_date(entry.published)}</published>')
            
            if entry.author:
                lines.append('<author>')
                lines.append(f'<name>{cls.escape_xml(entry.author)}</name>')
                if entry.email:
                    lines.append(f'<email>{cls.escape_xml(entry.email)}</email>')
                lines.append('</author>')
            
            if entry.description:
                lines.append(f'<summary>{cls.escape_xml(entry.description)}</summary>')
            
            if entry.content:
                lines.append(f'<content type="html">{cls.escape_xml(entry.content)}</content>')
            
            for cat in entry.categories:
                lines.append(f'<category term="{cls.escape_xml(cat)}" />')
            
            lines.append('</entry>')
        
        lines.append('</feed>')
        
        return '\n'.join(lines)


def parse(content: str) -> FeedInfo:
    """
    Parse RSS or Atom feed content and return FeedInfo.
    
    Args:
        content: Raw XML content of the feed
        
    Returns:
        FeedInfo object with feed metadata and entries
    """
    content = content.strip()
    
    # Detect feed type
    if '<rss' in content.lower() or '<channel>' in content.lower():
        return RSSParser.parse(content)
    elif '<feed' in content.lower():
        return AtomParser.parse(content)
    else:
        # Try RSS first, then Atom
        try:
            return RSSParser.parse(content)
        except Exception:
            return AtomParser.parse(content)


def validate(content: str) -> Tuple[bool, List[str]]:
    """
    Validate RSS/Atom feed content.
    
    Args:
        content: Raw XML content of the feed
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    if not content or not content.strip():
        errors.append("Empty content")
        return False, errors
    
    content = content.strip()
    
    # Check for XML declaration
    if not content.startswith('<?xml') and not content.startswith('<'):
        errors.append("Missing XML declaration or root element")
    
    # Check for root element
    if '<rss' not in content.lower() and '<feed' not in content.lower():
        errors.append("Missing RSS or Atom root element")
    
    # Try to parse
    try:
        feed_info = parse(content)
        
        if not feed_info.title:
            errors.append("Missing feed title")
        
        if not feed_info.entries:
            errors.append("No entries found in feed")
        
    except Exception as e:
        errors.append(f"Parse error: {str(e)}")
    
    return len(errors) == 0, errors


def generate_rss(
    title: str,
    link: str,
    description: str,
    entries: List[FeedEntry],
    **kwargs
) -> str:
    """
    Generate an RSS 2.0 feed.
    
    Args:
        title: Feed title
        link: Feed URL
        description: Feed description
        entries: List of FeedEntry objects
        **kwargs: Additional feed options (language, copyright, etc.)
        
    Returns:
        RSS XML string
    """
    return RSSGenerator.generate(title, link, description, entries, **kwargs)


def generate_atom(
    title: str,
    link: str,
    entries: List[FeedEntry],
    **kwargs
) -> str:
    """
    Generate an Atom feed.
    
    Args:
        title: Feed title
        link: Feed URL
        entries: List of FeedEntry objects
        **kwargs: Additional feed options (subtitle, author_name, etc.)
        
    Returns:
        Atom XML string
    """
    return AtomGenerator.generate(title, link, entries, **kwargs)


def extract_links(content: str) -> List[str]:
    """
    Extract all links from a feed.
    
    Args:
        content: Raw XML content of the feed
        
    Returns:
        List of URLs found in the feed
    """
    feed_info = parse(content)
    links = []
    
    if feed_info.link:
        links.append(feed_info.link)
    
    for entry in feed_info.entries:
        if entry.link and entry.link not in links:
            links.append(entry.link)
    
    return links


def find_entries(content: str, keyword: str, fields: List[str] = None) -> List[FeedEntry]:
    """
    Find entries containing a keyword.
    
    Args:
        content: Raw XML content of the feed
        keyword: Keyword to search for
        fields: Fields to search in (title, description, content). Default: all
        
    Returns:
        List of matching FeedEntry objects
    """
    if fields is None:
        fields = ['title', 'description', 'content']
    
    feed_info = parse(content)
    keyword_lower = keyword.lower()
    results = []
    
    for entry in feed_info.entries:
        found = False
        
        if 'title' in fields and keyword_lower in entry.title.lower():
            found = True
        elif 'description' in fields and keyword_lower in entry.description.lower():
            found = True
        elif 'content' in fields and keyword_lower in entry.content.lower():
            found = True
        
        if found:
            results.append(entry)
    
    return results


def merge_feeds(feeds: List[str], title: str = "Merged Feed", link: str = "",
                description: str = "Merged feed", sort_by_date: bool = True) -> FeedInfo:
    """
    Merge multiple feeds into one.
    
    Args:
        feeds: List of raw XML feed contents
        title: Title for merged feed
        link: Link for merged feed
        description: Description for merged feed
        sort_by_date: Whether to sort entries by date (newest first)
        
    Returns:
        Merged FeedInfo object
    """
    merged = FeedInfo(title=title, link=link, description=description)
    all_entries = []
    
    for feed_content in feeds:
        try:
            feed_info = parse(feed_content)
            all_entries.extend(feed_info.entries)
        except Exception:
            continue
    
    if sort_by_date:
        all_entries.sort(
            key=lambda e: e.published or e.updated or datetime.min,
            reverse=True
        )
    
    merged.entries = all_entries
    return merged


# Convenience exports
__all__ = [
    'FeedEntry',
    'FeedInfo',
    'RSSParser',
    'AtomParser',
    'RSSGenerator',
    'AtomGenerator',
    'parse',
    'validate',
    'generate_rss',
    'generate_atom',
    'extract_links',
    'find_entries',
    'merge_feeds',
]