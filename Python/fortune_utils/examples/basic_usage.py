"""
Fortune Utilities - Basic Usage Examples

Run this file to see examples of all fortune_utils features.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    fortune, fortune_result, daily_fortune,
    inspirational_quote, programming_quote, wisdom_quote,
    humor_quote, chinese_proverb, motivational_quote,
    riddle, riddle_question, unix_fortune,
    search_fortunes, categories, fortune_count,
    FortuneDatabase, FortuneGenerator, Fortune,
    format_fortune, format_fortune_result,
    to_cookie_format, from_cookie_format,
)


def main():
    print("=" * 60)
    print("Fortune Utilities - Examples")
    print("=" * 60)
    
    # 1. Basic Fortune
    print("\n1. Basic Fortune:")
    print(f"   {fortune()}")
    
    # 2. Category-specific Fortunes
    print("\n2. Category-specific Fortunes:")
    for cat in ['unix', 'programming', 'inspirational', 'wisdom']:
        print(f"   [{cat}] {fortune(cat)[:50]}...")
    
    # 3. Inspirational Quote (with author)
    print("\n3. Inspirational Quote:")
    result = fortune_result('inspirational')
    print(f"   \"{result.fortune.text}\"")
    print(f"       — {result.fortune.author}")
    
    # 4. Programming Quote
    print("\n4. Programming Quote:")
    print(f"   {programming_quote()}")
    
    # 5. Wisdom Quote
    print("\n5. Wisdom Quote:")
    print(f"   {wisdom_quote()}")
    
    # 6. Humor Quote
    print("\n6. Humor Quote:")
    print(f"   {humor_quote()}")
    
    # 7. Chinese Proverb
    print("\n7. Chinese Proverb:")
    print(f"   {chinese_proverb()}")
    
    # 8. Motivational Quote
    print("\n8. Motivational Quote:")
    print(f"   {motivational_quote()}")
    
    # 9. Riddle
    print("\n9. Riddle:")
    question, answer = riddle()
    print(f"   Question: {question}")
    print(f"   Answer: {answer}")
    
    # 10. Unix Fortune
    print("\n10. Unix Fortune:")
    print(f"    {unix_fortune()}")
    
    # 11. Daily Fortune
    print("\n11. Daily Fortune (same all day):")
    result1 = daily_fortune()
    result2 = daily_fortune()
    print(f"    First call:  {result1.fortune.text[:40]}...")
    print(f"    Second call: {result2.fortune.text[:40]}...")
    print(f"    Same result: {result1.fortune.text == result2.fortune.text}")
    
    # 12. Search Fortunes
    print("\n12. Search Fortunes:")
    results = search_fortunes("success")
    print(f"    Found {len(results)} fortunes matching 'success'")
    for f in results[:3]:
        print(f"    - {f.text[:50]}...")
    
    # 13. Categories and Counts
    print("\n13. Categories and Counts:")
    print(f"    Available categories: {', '.join(categories())}")
    print(f"    Total fortunes: {fortune_count()}")
    
    # 14. FortuneDatabase Class
    print("\n14. FortuneDatabase Class:")
    db = FortuneDatabase()
    print(f"    Categories: {db.get_categories()}")
    print(f"    Count 'inspirational': {db.count('inspirational')}")
    result = db.random('programming')
    print(f"    Random programming: {result.fortune.text[:40]}...")
    
    # 15. FortuneGenerator with Custom Fortunes
    print("\n15. FortuneGenerator with Custom Fortunes:")
    gen = FortuneGenerator(seed=42)
    gen.add_fortune("Custom fortune 1", category="custom", author="Me")
    gen.add_fortune("Custom fortune 2", category="custom")
    gen.add_fortunes_from_list(["F1", "F2", "F3"], category="batch")
    print(f"    Custom count: {gen.count('custom')}")
    print(f"    Batch count: {gen.count('batch')}")
    result = gen.random('custom')
    print(f"    Random custom: {result.fortune.text}")
    
    # 16. Formatting Styles
    print("\n16. Formatting Styles:")
    f = Fortune(text="A great fortune", author="Great Author", category="test")
    
    print("    Simple:")
    print(f"      {format_fortune(f, 'simple')}")
    
    print("    Quote:")
    print(f"      {format_fortune(f, 'quote')}")
    
    print("    Card:")
    print(format_fortune(f, 'card'))
    
    print("    JSON:")
    print(format_fortune(f, 'json'))
    
    # 17. Full Result Format
    print("\n17. Full Result Format:")
    result = fortune_result('wisdom')
    print(format_fortune_result(result, 'full'))
    
    # 18. Unix Fortune Cookie Format
    print("\n18. Unix Fortune Cookie Format:")
    fortunes = ["Fortune 1", "Fortune 2", "Fortune 3"]
    cookie = to_cookie_format(fortunes)
    print("    Export:")
    print(cookie)
    
    parsed = from_cookie_format(cookie)
    print(f"    Import: {parsed}")
    
    # 19. Statistics
    print("\n19. Fortune Statistics:")
    print("    Category Counts:")
    for cat in categories():
        count = fortune_count(cat)
        print(f"      {cat}: {count}")
    
    print("\n" + "=" * 60)
    print("Examples Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()