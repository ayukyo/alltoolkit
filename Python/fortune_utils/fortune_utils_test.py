"""
AllToolkit - Fortune Utilities Tests

Comprehensive tests for the fortune_utils module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Fortune, FortuneResult, FortuneDatabase, FortuneGenerator,
    fortune, fortune_result, daily_fortune, inspirational_quote,
    programming_quote, wisdom_quote, humor_quote, chinese_proverb,
    motivational_quote, riddle, riddle_question, unix_fortune,
    search_fortunes, categories, fortune_count, get_database,
    format_fortune, format_fortune_result, to_cookie_format, from_cookie_format,
)


def test_fortune_data_class():
    """Test Fortune data class."""
    f = Fortune(text="Test fortune", category="test", author="Author")
    assert f.text == "Test fortune"
    assert f.category == "test"
    assert f.author == "Author"
    
    # Test to_dict
    d = f.to_dict()
    assert d['text'] == "Test fortune"
    assert d['category'] == "test"
    assert d['author'] == "Author"
    
    print("✓ Fortune data class tests passed")


def test_fortune_result_data_class():
    """Test FortuneResult data class."""
    f = Fortune(text="Test", category="test")
    result = FortuneResult(fortune=f, index=0, total_in_category=10)
    
    assert result.fortune == f
    assert result.index == 0
    assert result.total_in_category == 10
    
    # Test to_dict
    d = result.to_dict()
    assert d['text'] == "Test"
    assert d['index'] == 0
    
    print("✓ FortuneResult data class tests passed")


def test_fortune_database():
    """Test FortuneDatabase class."""
    db = FortuneDatabase()
    
    # Test categories
    cats = db.get_categories()
    assert 'unix' in cats
    assert 'inspirational' in cats
    assert 'programming' in cats
    assert 'wisdom' in cats
    assert 'humor' in cats
    assert 'chinese' in cats
    assert 'riddle' in cats
    assert 'motivational' in cats
    
    # Test count
    assert db.count() > 0
    assert db.count('unix') > 0
    assert db.count('inspirational') > 0
    assert db.count('nonexistent') == 0
    
    # Test random
    result = db.random()
    assert result.fortune.text
    assert result.index >= 0
    
    # Test random with category
    result = db.random('programming')
    assert result.fortune.category == 'programming'
    
    # Test get
    f = db.get(0, 'unix')
    assert f is not None
    assert f.text
    
    # Test get out of bounds
    f = db.get(99999, 'unix')
    assert f is None
    
    # Test search
    results = db.search('success')
    assert len(results) > 0
    
    # Test add fortune
    db.add_fortune(Fortune(text="Custom fortune", category="custom"))
    assert db.count('custom') > 0
    
    print("✓ FortuneDatabase tests passed")


def test_daily_fortune():
    """Test daily fortune functionality."""
    db = FortuneDatabase()
    
    # Get daily fortune twice - should be the same
    r1 = db.random_daily()
    r2 = db.random_daily()
    assert r1.fortune.text == r2.fortune.text
    
    # Test with seed
    r1 = db.random_daily(seed="test1")
    r2 = db.random_daily(seed="test2")
    # Different seeds should potentially give different results
    # (though not guaranteed)
    
    print("✓ Daily fortune tests passed")


def test_riddles():
    """Test riddle functionality."""
    db = FortuneDatabase()
    
    result = db.random('riddle')
    assert result.fortune.category == 'riddle'
    
    # Test answer retrieval
    answer = db.get_riddle_answer(result.fortune.text)
    assert answer is not None
    
    print("✓ Riddle tests passed")


def test_convenience_functions():
    """Test all convenience functions."""
    # Test fortune
    f = fortune()
    assert len(f) > 0
    
    # Test fortune with category
    f = fortune('programming')
    assert len(f) > 0
    
    # Test fortune_result
    result = fortune_result('inspirational')
    assert result.fortune.text
    assert result.fortune.author  # Inspirational quotes have authors
    
    # Test daily_fortune
    result = daily_fortune()
    assert result.fortune.text
    
    # Test specialized functions
    q = inspirational_quote()
    assert len(q) > 0
    
    q = programming_quote()
    assert len(q) > 0
    
    q = wisdom_quote()
    assert len(q) > 0
    
    q = humor_quote()
    assert len(q) > 0
    
    q = chinese_proverb()
    assert len(q) > 0
    
    q = motivational_quote()
    assert len(q) > 0
    
    # Test riddle
    question, answer = riddle()
    assert len(question) > 0
    assert len(answer) > 0
    
    q = riddle_question()
    assert len(q) > 0
    
    # Test unix_fortune
    f = unix_fortune()
    assert len(f) > 0
    
    # Test search_fortunes
    results = search_fortunes('code')
    assert len(results) > 0
    
    # Test categories
    cats = categories()
    assert len(cats) > 0
    
    # Test fortune_count
    count = fortune_count()
    assert count > 0
    
    count = fortune_count('unix')
    assert count > 0
    
    # Test get_database
    db = get_database()
    assert isinstance(db, FortuneDatabase)
    
    print("✓ Convenience functions tests passed")


def test_fortune_generator():
    """Test FortuneGenerator class."""
    gen = FortuneGenerator(seed=42)
    
    # Test random
    result = gen.random()
    assert result.fortune.text
    
    # Test reproducibility with seed
    gen1 = FortuneGenerator(seed=42)
    gen2 = FortuneGenerator(seed=42)
    r1 = gen1.random()
    r2 = gen2.random()
    assert r1.fortune.text == r2.fortune.text
    
    # Test add_fortune
    gen.add_fortune("My custom fortune", category="custom", author="Me")
    result = gen.random('custom')
    assert result.fortune.text == "My custom fortune"
    
    # Test add_fortunes_from_list
    gen.add_fortunes_from_list(["F1", "F2", "F3"], category="batch")
    assert gen.count('batch') >= 3
    
    # Test search
    results = gen.search("custom")
    assert len(results) > 0
    
    print("✓ FortuneGenerator tests passed")


def test_format_functions():
    """Test formatting functions."""
    f = Fortune(text="Test fortune", author="Test Author", category="test")
    
    # Test simple format
    s = format_fortune(f, 'simple')
    assert s == "Test fortune"
    
    # Test quote format
    s = format_fortune(f, 'quote')
    assert '"Test fortune"' in s
    assert "Test Author" in s
    
    # Test card format
    s = format_fortune(f, 'card')
    assert "Test fortune" in s
    assert "Test Author" in s
    
    # Test json format
    s = format_fortune(f, 'json')
    assert '"text"' in s
    assert '"Test fortune"' in s
    
    # Test FortuneResult formatting
    result = FortuneResult(fortune=f, index=0, total_in_category=10)
    
    s = format_fortune_result(result, 'simple')
    assert s == "Test fortune"
    
    s = format_fortune_result(result, 'full')
    assert "Fortune #1" in s
    assert "Category: test" in s
    
    print("✓ Format functions tests passed")


def test_cookie_format():
    """Test cookie format conversion."""
    # Test to_cookie_format
    fortunes = ["Fortune 1", "Fortune 2", "Fortune 3"]
    cookie = to_cookie_format(fortunes)
    assert "Fortune 1" in cookie
    assert "Fortune 2" in cookie
    assert "Fortune 3" in cookie
    assert "%" in cookie
    
    # Test from_cookie_format
    parsed = from_cookie_format(cookie)
    assert parsed == fortunes
    
    # Test with custom delimiter
    cookie = to_cookie_format(fortunes, delimiter="---")
    assert "---" in cookie
    
    parsed = from_cookie_format(cookie, delimiter="---")
    assert parsed == fortunes
    
    print("✓ Cookie format tests passed")


def test_edge_cases():
    """Test edge cases and error handling."""
    db = FortuneDatabase()
    
    # Test empty search
    results = db.search('xyznonexistent123')
    assert len(results) == 0
    
    # Test invalid category in count
    count = db.count('nonexistent_category')
    assert count == 0
    
    # Test get from empty category
    f = db.get(0, 'nonexistent')
    assert f is None
    
    print("✓ Edge cases tests passed")


def test_categories_content():
    """Test that each category has expected content."""
    db = FortuneDatabase()
    
    # Unix fortunes should not have authors (traditional)
    unix = db.get_all('unix')
    for f in unix[:5]:  # Check first 5
        assert f.text
        assert f.author is None  # Unix fortunes don't have authors
    
    # Inspirational should have authors
    inspirational = db.get_all('inspirational')
    for f in inspirational[:5]:
        assert f.text
        assert f.author  # Should have author
    
    # Programming should have authors
    programming = db.get_all('programming')
    for f in programming[:5]:
        assert f.text
        assert f.author  # Should have author
    
    # Chinese proverbs should not have authors
    chinese = db.get_all('chinese')
    for f in chinese[:5]:
        assert f.text
        assert f.author is None
    
    print("✓ Categories content tests passed")


def run_all_tests():
    """Run all tests."""
    print("\n=== Running Fortune Utilities Tests ===\n")
    
    test_fortune_data_class()
    test_fortune_result_data_class()
    test_fortune_database()
    test_daily_fortune()
    test_riddles()
    test_convenience_functions()
    test_fortune_generator()
    test_format_functions()
    test_cookie_format()
    test_edge_cases()
    test_categories_content()
    
    print("\n=== All Tests Passed! ===\n")
    
    # Print sample fortunes
    print("=== Sample Fortunes ===\n")
    
    print("Unix Fortune:")
    print(f"  {unix_fortune()}")
    
    print("\nInspirational Quote:")
    print(f"  {inspirational_quote()}")
    
    print("\nProgramming Quote:")
    print(f"  {programming_quote()}")
    
    print("\nWisdom Quote:")
    print(f"  {wisdom_quote()}")
    
    print("\nHumor Quote:")
    print(f"  {humor_quote()}")
    
    print("\nChinese Proverb:")
    print(f"  {chinese_proverb()}")
    
    print("\nMotivational Quote:")
    print(f"  {motivational_quote()}")
    
    print("\nRiddle:")
    q, a = riddle()
    print(f"  Question: {q}")
    print(f"  Answer: {a}")
    
    print("\nDaily Fortune:")
    result = daily_fortune()
    print(f"  {result.fortune.text}")
    if result.fortune.author:
        print(f"    — {result.fortune.author}")
    
    # Print statistics
    print("\n=== Fortune Database Statistics ===\n")
    for cat in categories():
        count = fortune_count(cat)
        print(f"  {cat}: {count} fortunes")
    print(f"\n  Total: {fortune_count()} fortunes")


if __name__ == "__main__":
    run_all_tests()