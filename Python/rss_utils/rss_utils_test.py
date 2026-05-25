"""
Test suite for RSS Utils module.
"""

import unittest
from datetime import datetime
from mod import (
    FeedEntry,
    FeedInfo,
    RSSParser,
    AtomParser,
    RSSGenerator,
    AtomGenerator,
    parse,
    validate,
    generate_rss,
    generate_atom,
    extract_links,
    find_entries,
    merge_feeds,
)


class TestFeedEntry(unittest.TestCase):
    """Tests for FeedEntry class."""
    
    def test_init_defaults(self):
        """Test default initialization."""
        entry = FeedEntry()
        self.assertEqual(entry.title, "")
        self.assertEqual(entry.link, "")
        self.assertEqual(entry.description, "")
        self.assertEqual(entry.categories, [])
    
    def test_init_with_values(self):
        """Test initialization with values."""
        dt = datetime(2024, 1, 15, 10, 30, 0)
        entry = FeedEntry(
            title="Test Title",
            link="https://example.com/test",
            description="Test description",
            author="John Doe",
            published=dt,
            categories=["tech", "python"]
        )
        self.assertEqual(entry.title, "Test Title")
        self.assertEqual(entry.link, "https://example.com/test")
        self.assertEqual(entry.description, "Test description")
        self.assertEqual(entry.author, "John Doe")
        self.assertEqual(entry.published, dt)
        self.assertEqual(entry.categories, ["tech", "python"])
    
    def test_to_dict(self):
        """Test to_dict method."""
        dt = datetime(2024, 1, 15, 10, 30, 0)
        entry = FeedEntry(
            title="Test",
            link="https://example.com",
            published=dt,
            categories=["test"]
        )
        d = entry.to_dict()
        self.assertEqual(d["title"], "Test")
        self.assertEqual(d["link"], "https://example.com")
        self.assertEqual(d["published"], dt.isoformat())
        self.assertEqual(d["categories"], ["test"])


class TestFeedInfo(unittest.TestCase):
    """Tests for FeedInfo class."""
    
    def test_init_defaults(self):
        """Test default initialization."""
        info = FeedInfo()
        self.assertEqual(info.title, "")
        self.assertEqual(info.link, "")
        self.assertEqual(info.feed_type, "rss")
        self.assertEqual(info.entries, [])
    
    def test_init_with_entries(self):
        """Test initialization with entries."""
        entries = [FeedEntry(title="Entry 1"), FeedEntry(title="Entry 2")]
        info = FeedInfo(title="My Feed", entries=entries)
        self.assertEqual(info.title, "My Feed")
        self.assertEqual(len(info.entries), 2)
    
    def test_to_dict(self):
        """Test to_dict method."""
        info = FeedInfo(title="Test Feed", link="https://example.com")
        d = info.to_dict()
        self.assertEqual(d["title"], "Test Feed")
        self.assertEqual(d["link"], "https://example.com")


class TestRSSParser(unittest.TestCase):
    """Tests for RSSParser class."""
    
    SIMPLE_RSS = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
<channel>
    <title>Test Feed</title>
    <link>https://example.com</link>
    <description>A test RSS feed</description>
    <language>en</language>
    <item>
        <title>First Post</title>
        <link>https://example.com/first</link>
        <description>This is the first post</description>
        <pubDate>Mon, 15 Jan 2024 10:30:00 GMT</pubDate>
        <category>Tech</category>
    </item>
    <item>
        <title>Second Post</title>
        <link>https://example.com/second</link>
        <description>This is the second post</description>
        <author>john@example.com (John Doe)</author>
    </item>
</channel>
</rss>"""

    def test_parse_date(self):
        """Test date parsing."""
        # RSS date format
        dt = RSSParser.parse_date("Mon, 15 Jan 2024 10:30:00 GMT")
        self.assertIsNotNone(dt)
        self.assertEqual(dt.year, 2024)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.day, 15)
        
        # ISO 8601 format
        dt = RSSParser.parse_date("2024-01-15T10:30:00Z")
        self.assertIsNotNone(dt)
        
        # None for invalid
        dt = RSSParser.parse_date("")
        self.assertIsNone(dt)
        dt = RSSParser.parse_date("invalid")
        self.assertIsNone(dt)
    
    def test_parse_simple_rss(self):
        """Test parsing a simple RSS feed."""
        feed = RSSParser.parse(self.SIMPLE_RSS)
        
        self.assertEqual(feed.title, "Test Feed")
        self.assertEqual(feed.link, "https://example.com")
        self.assertEqual(feed.description, "A test RSS feed")
        self.assertEqual(feed.language, "en")
        self.assertEqual(len(feed.entries), 2)
    
    def test_parse_entries(self):
        """Test parsing RSS entries."""
        feed = RSSParser.parse(self.SIMPLE_RSS)
        
        entry1 = feed.entries[0]
        self.assertEqual(entry1.title, "First Post")
        self.assertEqual(entry1.link, "https://example.com/first")
        self.assertEqual(entry1.description, "This is the first post")
        self.assertEqual(entry1.categories, ["Tech"])
        self.assertIsNotNone(entry1.published)
        
        entry2 = feed.entries[1]
        self.assertEqual(entry2.title, "Second Post")
        self.assertEqual(entry2.author, "john@example.com (John Doe)")
    
    def test_parse_with_image(self):
        """Test parsing RSS with image."""
        rss = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
    <title>Feed with Image</title>
    <link>https://example.com</link>
    <description>Test</description>
    <image>
        <url>https://example.com/logo.png</url>
        <title>Logo</title>
        <link>https://example.com</link>
    </image>
</channel>
</rss>"""
        feed = RSSParser.parse(rss)
        self.assertEqual(feed.image_url, "https://example.com/logo.png")
        self.assertEqual(feed.image_title, "Logo")


class TestAtomParser(unittest.TestCase):
    """Tests for AtomParser class."""
    
    SIMPLE_ATOM = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <title>Test Atom Feed</title>
    <subtitle>An Atom feed for testing</subtitle>
    <link href="https://example.com/feed.xml" rel="self" />
    <link href="https://example.com" />
    <updated>2024-01-15T10:30:00Z</updated>
    <author>
        <name>John Doe</name>
        <email>john@example.com</email>
    </author>
    <entry>
        <title>First Entry</title>
        <link href="https://example.com/first" />
        <id>https://example.com/first</id>
        <updated>2024-01-15T10:30:00Z</updated>
        <published>2024-01-15T08:00:00Z</published>
        <summary>This is the first entry</summary>
        <category term="tech" />
    </entry>
    <entry>
        <title>Second Entry</title>
        <link href="https://example.com/second" />
        <id>https://example.com/second</id>
        <updated>2024-01-14T10:30:00Z</updated>
        <summary>This is the second entry</summary>
    </entry>
</feed>"""

    def test_parse_date(self):
        """Test date parsing."""
        dt = AtomParser.parse_date("2024-01-15T10:30:00Z")
        self.assertIsNotNone(dt)
        self.assertEqual(dt.year, 2024)
        
        dt = AtomParser.parse_date("")
        self.assertIsNone(dt)
    
    def test_parse_simple_atom(self):
        """Test parsing a simple Atom feed."""
        feed = AtomParser.parse(self.SIMPLE_ATOM)
        
        self.assertEqual(feed.title, "Test Atom Feed")
        self.assertEqual(feed.description, "An Atom feed for testing")
        self.assertEqual(feed.feed_type, "atom")
        self.assertEqual(len(feed.entries), 2)
    
    def test_parse_entries(self):
        """Test parsing Atom entries."""
        feed = AtomParser.parse(self.SIMPLE_ATOM)
        
        entry1 = feed.entries[0]
        self.assertEqual(entry1.title, "First Entry")
        self.assertEqual(entry1.link, "https://example.com/first")
        self.assertEqual(entry1.description, "This is the first entry")
        self.assertEqual(entry1.categories, ["tech"])
        self.assertIsNotNone(entry1.published)
        self.assertIsNotNone(entry1.updated)
        
        entry2 = feed.entries[1]
        self.assertEqual(entry2.title, "Second Entry")


class TestRSSGenerator(unittest.TestCase):
    """Tests for RSSGenerator class."""
    
    def test_escape_xml(self):
        """Test XML escaping."""
        self.assertEqual(RSSGenerator.escape_xml("hello"), "hello")
        self.assertEqual(RSSGenerator.escape_xml("<tag>"), "&lt;tag&gt;")
        self.assertEqual(RSSGenerator.escape_xml("a & b"), "a &amp; b")
        self.assertEqual(RSSGenerator.escape_xml('"quote"'), "&quot;quote&quot;")
    
    def test_format_date(self):
        """Test date formatting."""
        dt = datetime(2024, 1, 15, 10, 30, 0)
        formatted = RSSGenerator.format_date(dt)
        self.assertIn("Mon", formatted)
        self.assertIn("Jan", formatted)
        self.assertIn("2024", formatted)
    
    def test_generate_simple(self):
        """Test generating a simple RSS feed."""
        entries = [
            FeedEntry(
                title="First Post",
                link="https://example.com/first",
                description="First post content"
            ),
            FeedEntry(
                title="Second Post",
                link="https://example.com/second",
                description="Second post content"
            )
        ]
        
        rss = generate_rss(
            title="My Feed",
            link="https://example.com",
            description="A test feed",
            entries=entries
        )
        
        self.assertIn('<?xml version="1.0"', rss)
        self.assertIn('<rss version="2.0">', rss)
        self.assertIn("<title>My Feed</title>", rss)
        self.assertIn("<link>https://example.com</link>", rss)
        self.assertIn("<item>", rss)
        self.assertIn("<title>First Post</title>", rss)
    
    def test_generate_with_categories(self):
        """Test generating RSS with categories."""
        entries = [
            FeedEntry(
                title="Test",
                link="https://example.com",
                description="Test",
                categories=["tech", "python"]
            )
        ]
        
        rss = generate_rss(
            title="Feed",
            link="https://example.com",
            description="Test",
            entries=entries,
            categories=["blog"]
        )
        
        self.assertIn("<category>blog</category>", rss)
        self.assertIn("<category>tech</category>", rss)
        self.assertIn("<category>python</category>", rss)


class TestAtomGenerator(unittest.TestCase):
    """Tests for AtomGenerator class."""
    
    def test_escape_xml(self):
        """Test XML escaping."""
        self.assertEqual(AtomGenerator.escape_xml("hello"), "hello")
        self.assertEqual(AtomGenerator.escape_xml("<tag>"), "&lt;tag&gt;")
    
    def test_generate_simple(self):
        """Test generating a simple Atom feed."""
        entries = [
            FeedEntry(
                title="First Post",
                link="https://example.com/first",
                description="First post content",
                id="https://example.com/first"
            )
        ]
        
        atom = generate_atom(
            title="My Feed",
            link="https://example.com/feed",
            entries=entries,
            subtitle="A test feed"
        )
        
        self.assertIn('<?xml version="1.0"', atom)
        self.assertIn('xmlns="http://www.w3.org/2005/Atom"', atom)
        self.assertIn("<title>My Feed</title>", atom)
        self.assertIn("<subtitle>A test feed</subtitle>", atom)
        self.assertIn("<entry>", atom)
        self.assertIn("<title>First Post</title>", atom)
    
    def test_generate_with_author(self):
        """Test generating Atom with author."""
        entries = [FeedEntry(title="Test", link="https://example.com")]
        
        atom = generate_atom(
            title="Feed",
            link="https://example.com",
            entries=entries,
            author_name="John Doe",
            author_email="john@example.com"
        )
        
        self.assertIn("<author>", atom)
        self.assertIn("<name>John Doe</name>", atom)
        self.assertIn("<email>john@example.com</email>", atom)


class TestParseFunction(unittest.TestCase):
    """Tests for the parse function."""
    
    def test_parse_rss(self):
        """Test parsing RSS content."""
        rss = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
    <title>Test</title>
    <link>https://example.com</link>
    <description>Test feed</description>
    <item>
        <title>Item</title>
        <link>https://example.com/item</link>
    </item>
</channel>
</rss>"""
        
        feed = parse(rss)
        self.assertEqual(feed.feed_type, "rss")
        self.assertEqual(feed.title, "Test")
        self.assertEqual(len(feed.entries), 1)
    
    def test_parse_atom(self):
        """Test parsing Atom content."""
        atom = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <title>Test</title>
    <link href="https://example.com" />
    <entry>
        <title>Entry</title>
        <link href="https://example.com/entry" />
        <id>https://example.com/entry</id>
        <updated>2024-01-15T10:00:00Z</updated>
    </entry>
</feed>"""
        
        feed = parse(atom)
        self.assertEqual(feed.feed_type, "atom")
        self.assertEqual(feed.title, "Test")
        self.assertEqual(len(feed.entries), 1)


class TestValidateFunction(unittest.TestCase):
    """Tests for the validate function."""
    
    def test_validate_valid_rss(self):
        """Test validating valid RSS."""
        rss = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
    <title>Test</title>
    <link>https://example.com</link>
    <description>Test</description>
    <item>
        <title>Item</title>
        <link>https://example.com/item</link>
    </item>
</channel>
</rss>"""
        
        is_valid, errors = validate(rss)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_empty(self):
        """Test validating empty content."""
        is_valid, errors = validate("")
        self.assertFalse(is_valid)
        self.assertIn("Empty content", errors)
    
    def test_validate_no_entries(self):
        """Test validating RSS without entries."""
        rss = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
    <title>Test</title>
    <link>https://example.com</link>
    <description>Test</description>
</channel>
</rss>"""
        
        is_valid, errors = validate(rss)
        self.assertFalse(is_valid)
        self.assertIn("No entries found in feed", errors)


class TestExtractLinks(unittest.TestCase):
    """Tests for extract_links function."""
    
    def test_extract_links(self):
        """Test extracting links from feed."""
        rss = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
    <title>Test</title>
    <link>https://example.com</link>
    <description>Test</description>
    <item>
        <title>Item 1</title>
        <link>https://example.com/1</link>
    </item>
    <item>
        <title>Item 2</title>
        <link>https://example.com/2</link>
    </item>
</channel>
</rss>"""
        
        links = extract_links(rss)
        self.assertEqual(len(links), 3)
        self.assertIn("https://example.com", links)
        self.assertIn("https://example.com/1", links)
        self.assertIn("https://example.com/2", links)


class TestFindEntries(unittest.TestCase):
    """Tests for find_entries function."""
    
    RSS = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
    <title>Test</title>
    <link>https://example.com</link>
    <description>Test</description>
    <item>
        <title>Python Programming</title>
        <link>https://example.com/1</link>
        <description>Learn Python basics</description>
    </item>
    <item>
        <title>JavaScript Tips</title>
        <link>https://example.com/2</link>
        <description>Advanced JavaScript techniques</description>
    </item>
    <item>
        <title>Python Advanced</title>
        <link>https://example.com/3</link>
        <description>Advanced Python topics</description>
    </item>
</channel>
</rss>"""

    def test_find_in_title(self):
        """Test finding entries by title."""
        results = find_entries(self.RSS, "Python", fields=["title"])
        self.assertEqual(len(results), 2)
    
    def test_find_in_description(self):
        """Test finding entries by description."""
        results = find_entries(self.RSS, "Advanced", fields=["description"])
        self.assertEqual(len(results), 2)
    
    def test_find_in_all_fields(self):
        """Test finding entries in all fields."""
        results = find_entries(self.RSS, "Python")
        self.assertEqual(len(results), 2)
    
    def test_find_no_match(self):
        """Test finding with no matches."""
        results = find_entries(self.RSS, "Ruby")
        self.assertEqual(len(results), 0)


class TestMergeFeeds(unittest.TestCase):
    """Tests for merge_feeds function."""
    
    RSS1 = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
    <title>Feed 1</title>
    <link>https://example1.com</link>
    <description>First feed</description>
    <item>
        <title>Item 1</title>
        <link>https://example1.com/1</link>
        <pubDate>Mon, 15 Jan 2024 10:00:00 GMT</pubDate>
    </item>
</channel>
</rss>"""

    RSS2 = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
    <title>Feed 2</title>
    <link>https://example2.com</link>
    <description>Second feed</description>
    <item>
        <title>Item 2</title>
        <link>https://example2.com/1</link>
        <pubDate>Tue, 16 Jan 2024 10:00:00 GMT</pubDate>
    </item>
</channel>
</rss>"""

    def test_merge_feeds(self):
        """Test merging feeds."""
        merged = merge_feeds([self.RSS1, self.RSS2])
        self.assertEqual(len(merged.entries), 2)
    
    def test_merge_sorted(self):
        """Test merging feeds with sorting."""
        merged = merge_feeds([self.RSS1, self.RSS2], sort_by_date=True)
        # Newer item should be first
        self.assertEqual(merged.entries[0].title, "Item 2")
        self.assertEqual(merged.entries[1].title, "Item 1")
    
    def test_merge_custom_title(self):
        """Test merging with custom title."""
        merged = merge_feeds(
            [self.RSS1, self.RSS2],
            title="Combined Feed",
            description="All feeds combined"
        )
        self.assertEqual(merged.title, "Combined Feed")
        self.assertEqual(merged.description, "All feeds combined")


class TestRoundTrip(unittest.TestCase):
    """Tests for round-trip parsing and generation."""
    
    def test_rss_roundtrip(self):
        """Test RSS round-trip."""
        original_entries = [
            FeedEntry(
                title="Test Entry",
                link="https://example.com/test",
                description="Test description",
                author="Test Author",
                categories=["test"]
            )
        ]
        
        # Generate RSS
        rss = generate_rss(
            title="Test Feed",
            link="https://example.com",
            description="Test",
            entries=original_entries
        )
        
        # Parse it back
        feed = parse(rss)
        
        self.assertEqual(feed.title, "Test Feed")
        self.assertEqual(feed.link, "https://example.com")
        self.assertEqual(len(feed.entries), 1)
        self.assertEqual(feed.entries[0].title, "Test Entry")
        self.assertEqual(feed.entries[0].link, "https://example.com/test")
    
    def test_atom_roundtrip(self):
        """Test Atom round-trip."""
        original_entries = [
            FeedEntry(
                title="Test Entry",
                link="https://example.com/test",
                description="Test description",
                id="https://example.com/test",
                categories=["test"]
            )
        ]
        
        # Generate Atom
        atom = generate_atom(
            title="Test Feed",
            link="https://example.com/feed",
            entries=original_entries
        )
        
        # Parse it back
        feed = parse(atom)
        
        self.assertEqual(feed.title, "Test Feed")
        self.assertEqual(len(feed.entries), 1)
        self.assertEqual(feed.entries[0].title, "Test Entry")


if __name__ == "__main__":
    unittest.main()