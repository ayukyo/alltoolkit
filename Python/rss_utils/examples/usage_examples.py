"""
RSS Utils - Usage Examples

This file demonstrates how to use the RSS Utils module for parsing,
validating, and generating RSS/Atom feeds.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


def example_parse_rss():
    """Example: Parse an RSS feed."""
    print("=" * 60)
    print("Example 1: Parse RSS Feed")
    print("=" * 60)
    
    rss_content = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
<channel>
    <title>Technology Blog</title>
    <link>https://techblog.example.com</link>
    <description>Latest tech news and tutorials</description>
    <language>en</language>
    <copyright>Copyright 2024 Tech Blog</copyright>
    <lastBuildDate>Mon, 15 Jan 2024 12:00:00 GMT</lastBuildDate>
    <item>
        <title>Introduction to Python Async</title>
        <link>https://techblog.example.com/python-async</link>
        <description>Learn the basics of asynchronous programming in Python</description>
        <author>editor@techblog.example.com (Jane Doe)</author>
        <pubDate>Mon, 15 Jan 2024 10:30:00 GMT</pubDate>
        <category>Python</category>
        <category>Programming</category>
        <guid>https://techblog.example.com/python-async</guid>
    </item>
    <item>
        <title>JavaScript ES2024 Features</title>
        <link>https://techblog.example.com/js-es2024</link>
        <description>What's new in JavaScript ES2024</description>
        <author>editor@techblog.example.com (John Smith)</author>
        <pubDate>Sun, 14 Jan 2024 14:00:00 GMT</pubDate>
        <category>JavaScript</category>
        <category>Programming</category>
    </item>
    <item>
        <title>Docker Best Practices</title>
        <link>https://techblog.example.com/docker-best-practices</link>
        <description>Optimize your Docker containers for production</description>
        <pubDate>Sat, 13 Jan 2024 09:00:00 GMT</pubDate>
        <category>DevOps</category>
        <enclosure url="https://techblog.example.com/podcasts/docker.mp3" 
                   type="audio/mpeg" length="5600000" />
    </item>
</channel>
</rss>"""
    
    feed = parse(rss_content)
    
    print(f"Feed Title: {feed.title}")
    print(f"Feed Link: {feed.link}")
    print(f"Feed Description: {feed.description}")
    print(f"Feed Language: {feed.language}")
    print(f"Feed Type: {feed.feed_type}")
    print(f"Number of Entries: {len(feed.entries)}")
    print()
    
    for i, entry in enumerate(feed.entries, 1):
        print(f"Entry {i}:")
        print(f"  Title: {entry.title}")
        print(f"  Link: {entry.link}")
        print(f"  Author: {entry.author or 'N/A'}")
        print(f"  Categories: {', '.join(entry.categories) or 'N/A'}")
        if entry.enclosure_url:
            print(f"  Enclosure: {entry.enclosure_url}")
            print(f"  Type: {entry.enclosure_type}")
        print()


def example_parse_atom():
    """Example: Parse an Atom feed."""
    print("=" * 60)
    print("Example 2: Parse Atom Feed")
    print("=" * 60)
    
    atom_content = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <title>Developer News</title>
    <subtitle>Daily updates for developers</subtitle>
    <link href="https://devnews.example.com/atom.xml" rel="self" />
    <link href="https://devnews.example.com" />
    <updated>2024-01-15T12:00:00Z</updated>
    <author>
        <name>Dev News Team</name>
        <email>team@devnews.example.com</email>
    </author>
    <entry>
        <title>New Framework Released</title>
        <link href="https://devnews.example.com/new-framework" />
        <id>https://devnews.example.com/new-framework</id>
        <updated>2024-01-15T10:30:00Z</updated>
        <published>2024-01-15T08:00:00Z</published>
        <summary>A new web framework promises 10x faster development</summary>
        <category term="frameworks" />
        <category term="web" />
    </entry>
    <entry>
        <title>API Versioning Strategies</title>
        <link href="https://devnews.example.com/api-versioning" />
        <id>https://devnews.example.com/api-versioning</id>
        <updated>2024-01-14T15:00:00Z</updated>
        <published>2024-01-14T12:00:00Z</published>
        <summary>Best practices for API versioning in large systems</summary>
        <author>
            <name>Alice Developer</name>
            <email>alice@devnews.example.com</email>
        </author>
        <category term="api" />
    </entry>
</feed>"""
    
    feed = parse(atom_content)
    
    print(f"Feed Title: {feed.title}")
    print(f"Feed Description: {feed.description}")
    print(f"Feed Type: {feed.feed_type}")
    print(f"Number of Entries: {len(feed.entries)}")
    print()
    
    for i, entry in enumerate(feed.entries, 1):
        print(f"Entry {i}:")
        print(f"  Title: {entry.title}")
        print(f"  Link: {entry.link}")
        print(f"  Author: {entry.author or 'N/A'}")
        print(f"  Published: {entry.published or 'N/A'}")
        print(f"  Updated: {entry.updated or 'N/A'}")
        print()


def example_generate_rss():
    """Example: Generate an RSS feed."""
    print("=" * 60)
    print("Example 3: Generate RSS Feed")
    print("=" * 60)
    
    entries = [
        FeedEntry(
            title="Getting Started with Machine Learning",
            link="https://myblog.example.com/ml-intro",
            description="A beginner's guide to machine learning concepts and tools",
            author="author@myblog.example.com (Data Scientist)",
            published=datetime(2024, 1, 15, 10, 30, 0),
            categories=["Machine Learning", "Tutorial"],
            guid="https://myblog.example.com/ml-intro"
        ),
        FeedEntry(
            title="Web Security Best Practices",
            link="https://myblog.example.com/security-best-practices",
            description="Essential security practices for modern web applications",
            author="author@myblog.example.com (Security Expert)",
            published=datetime(2024, 1, 14, 14, 0, 0),
            categories=["Security", "Web Development"],
            guid="https://myblog.example.com/security-best-practices"
        ),
        FeedEntry(
            title="Podcast: Tech Trends 2024",
            link="https://myblog.example.com/tech-trends-2024",
            description="Discussion about emerging technology trends",
            published=datetime(2024, 1, 13, 9, 0, 0),
            categories=["Podcast", "Technology"],
            enclosure_url="https://myblog.example.com/audio/tech-trends.mp3",
            enclosure_type="audio/mpeg",
            enclosure_length=15000000
        ),
    ]
    
    rss = generate_rss(
        title="My Tech Blog",
        link="https://myblog.example.com",
        description="Insights on technology and development",
        entries=entries,
        language="en",
        copyright="Copyright 2024 My Tech Blog",
        managing_editor="editor@myblog.example.com (Editor)",
        categories=["Technology", "Programming"],
        image_url="https://myblog.example.com/logo.png"
    )
    
    print("Generated RSS Feed:")
    print("-" * 40)
    print(rss[:500])
    print("...")
    print()
    
    return rss


def example_generate_atom():
    """Example: Generate an Atom feed."""
    print("=" * 60)
    print("Example 4: Generate Atom Feed")
    print("=" * 60)
    
    entries = [
        FeedEntry(
            title="Cloud Architecture Patterns",
            link="https://myblog.example.com/cloud-patterns",
            description="Common patterns for cloud-native applications",
            id="https://myblog.example.com/cloud-patterns",
            published=datetime(2024, 1, 15, 8, 0, 0),
            updated=datetime(2024, 1, 15, 10, 0, 0),
            author="Cloud Architect",
            categories=["Cloud", "Architecture"]
        ),
        FeedEntry(
            title="Microservices Communication",
            link="https://myblog.example.com/microservices-comm",
            description="Effective communication strategies for microservices",
            id="https://myblog.example.com/microservices-comm",
            published=datetime(2024, 1, 14, 11, 0, 0),
            categories=["Microservices", "Architecture"]
        ),
    ]
    
    atom = generate_atom(
        title="Architecture Blog",
        link="https://myblog.example.com/feed.atom",
        entries=entries,
        subtitle="Software architecture insights",
        author_name="Architecture Team",
        author_email="arch@myblog.example.com",
        categories=["Architecture", "Software Design"]
    )
    
    print("Generated Atom Feed:")
    print("-" * 40)
    print(atom[:500])
    print("...")
    print()


def example_validate_feed():
    """Example: Validate feed content."""
    print("=" * 60)
    print("Example 5: Validate Feed")
    print("=" * 60)
    
    # Valid feed
    valid_rss = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
    <title>Valid Feed</title>
    <link>https://example.com</link>
    <description>A valid feed</description>
    <item>
        <title>Item</title>
        <link>https://example.com/item</link>
    </item>
</channel>
</rss>"""
    
    is_valid, errors = validate(valid_rss)
    print(f"Valid feed: is_valid={is_valid}, errors={errors}")
    
    # Invalid feed
    invalid_rss = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
    <title>Invalid Feed</title>
    <link>https://example.com</link>
</channel>
</rss>"""
    
    is_valid, errors = validate(invalid_rss)
    print(f"Invalid feed: is_valid={is_valid}, errors={errors}")
    print()


def example_extract_links():
    """Example: Extract links from feed."""
    print("=" * 60)
    print("Example 6: Extract Links")
    print("=" * 60)
    
    rss = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
    <title>Link Demo</title>
    <link>https://example.com</link>
    <description>Demo</description>
    <item>
        <title>Article 1</title>
        <link>https://example.com/article/1</link>
    </item>
    <item>
        <title>Article 2</title>
        <link>https://example.com/article/2</link>
    </item>
    <item>
        <title>Article 3</title>
        <link>https://example.com/article/3</link>
    </item>
</channel>
</rss>"""
    
    links = extract_links(rss)
    print(f"Found {len(links)} links:")
    for link in links:
        print(f"  - {link}")
    print()


def example_find_entries():
    """Example: Find entries by keyword."""
    print("=" * 60)
    print("Example 7: Find Entries")
    print("=" * 60)
    
    rss = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
    <title>Search Demo</title>
    <link>https://example.com</link>
    <description>Demo</description>
    <item>
        <title>Python Programming Guide</title>
        <link>https://example.com/python-guide</link>
        <description>Comprehensive guide to Python programming</description>
    </item>
    <item>
        <title>JavaScript for Beginners</title>
        <link>https://example.com/js-beginners</link>
        <description>Getting started with JavaScript</description>
    </item>
    <item>
        <title>Advanced Python Techniques</title>
        <link>https://example.com/python-advanced</link>
        <description>Advanced techniques for Python developers</description>
    </item>
    <item>
        <title>Python vs JavaScript</title>
        <link>https://example.com/python-vs-js</link>
        <description>Comparing Python and JavaScript</description>
    </item>
</channel>
</rss>"""
    
    # Search in titles
    print("Entries with 'Python' in title:")
    results = find_entries(rss, "Python", fields=["title"])
    for entry in results:
        print(f"  - {entry.title}")
    print()
    
    # Search in all fields
    print("Entries with 'guide' anywhere:")
    results = find_entries(rss, "guide")
    for entry in results:
        print(f"  - {entry.title}: {entry.description}")
    print()


def example_merge_feeds():
    """Example: Merge multiple feeds."""
    print("=" * 60)
    print("Example 8: Merge Feeds")
    print("=" * 60)
    
    feed1 = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
    <title>Tech News</title>
    <link>https://tech.example.com</link>
    <description>Tech news</description>
    <item>
        <title>AI Breakthrough</title>
        <link>https://tech.example.com/ai</link>
        <pubDate>Mon, 15 Jan 2024 12:00:00 GMT</pubDate>
    </item>
    <item>
        <title>New Processor Released</title>
        <link>https://tech.example.com/cpu</link>
        <pubDate>Sun, 14 Jan 2024 10:00:00 GMT</pubDate>
    </item>
</channel>
</rss>"""
    
    feed2 = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
    <title>Science News</title>
    <link>https://science.example.com</link>
    <description>Science news</description>
    <item>
        <title>Mars Discovery</title>
        <link>https://science.example.com/mars</link>
        <pubDate>Mon, 15 Jan 2024 14:00:00 GMT</pubDate>
    </item>
    <item>
        <title>Ocean Life Study</title>
        <link>https://science.example.com/ocean</link>
        <pubDate>Sat, 13 Jan 2024 08:00:00 GMT</pubDate>
    </item>
</channel>
</rss>"""
    
    merged = merge_feeds(
        [feed1, feed2],
        title="Combined News Feed",
        link="https://aggregated.example.com",
        description="Tech and Science news combined"
    )
    
    print(f"Merged Feed: {merged.title}")
    print(f"Description: {merged.description}")
    print(f"Total Entries: {len(merged.entries)}")
    print()
    print("Entries (sorted by date, newest first):")
    for entry in merged.entries:
        print(f"  - {entry.title} ({entry.published or 'no date'})")
    print()


def example_roundtrip():
    """Example: Round-trip parsing and generation."""
    print("=" * 60)
    print("Example 9: Round-Trip Parsing")
    print("=" * 60)
    
    # Generate RSS
    original_entries = [
        FeedEntry(
            title="Original Post",
            link="https://example.com/original",
            description="This is the original post",
            author="Original Author",
            categories=["original"]
        )
    ]
    
    generated_rss = generate_rss(
        title="Original Feed",
        link="https://example.com",
        description="The original feed",
        entries=original_entries
    )
    
    print("Generated RSS (first 300 chars):")
    print(generated_rss[:300])
    print("...")
    print()
    
    # Parse it back
    parsed_feed = parse(generated_rss)
    
    print("Parsed back:")
    print(f"  Title: {parsed_feed.title}")
    print(f"  Description: {parsed_feed.description}")
    print(f"  Entry count: {len(parsed_feed.entries)}")
    if parsed_feed.entries:
        print(f"  First entry title: {parsed_feed.entries[0].title}")
        print(f"  First entry author: {parsed_feed.entries[0].author}")
    print()


def example_custom_feed_entry():
    """Example: Create custom feed entries."""
    print("=" * 60)
    print("Example 10: Custom Feed Entry")
    print("=" * 60)
    
    # Create entries with various fields
    entry = FeedEntry(
        title="Complete Guide to Web Development",
        link="https://example.com/web-dev-guide",
        description="A comprehensive guide covering HTML, CSS, and JavaScript",
        author="Web Expert",
        email="expert@example.com",
        published=datetime(2024, 1, 15, 10, 0, 0),
        updated=datetime(2024, 1, 15, 12, 0, 0),
        guid="https://example.com/web-dev-guide",
        categories=["Web Development", "HTML", "CSS", "JavaScript"],
        content="<p>This is the full HTML content of the article...</p>"
    )
    
    print("Custom Feed Entry:")
    print(f"  Title: {entry.title}")
    print(f"  Link: {entry.link}")
    print(f"  Author: {entry.author} <{entry.email}>")
    print(f"  Categories: {', '.join(entry.categories)}")
    print(f"  Published: {entry.published}")
    print(f"  Updated: {entry.updated}")
    print(f"  GUID: {entry.guid}")
    print(f"  Content snippet: {entry.content[:50]}...")
    print()
    
    # Convert to dictionary
    print("As dictionary:")
    import json
    print(json.dumps(entry.to_dict(), indent=2, default=str))


def main():
    """Run all examples."""
    example_parse_rss()
    example_parse_atom()
    example_generate_rss()
    example_generate_atom()
    example_validate_feed()
    example_extract_links()
    example_find_entries()
    example_merge_feeds()
    example_roundtrip()
    example_custom_feed_entry()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()