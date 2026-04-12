"""
AllToolkit - Python Emoji Utilities Examples

Comprehensive examples demonstrating emoji_utils functionality.
Run: python examples/usage_examples.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    EmojiUtils,
    EmojiCategory,
    extract_emojis,
    count_emojis,
    analyze,
    remove_emojis,
    replace_emojis,
    has_emoji,
    to_unicode_escape,
    from_unicode_escape,
    strip_skin_tone,
    emoji_to_text,
    text_to_emoji,
    filter_by_category,
    get_emoji_positions,
    reverse,
)


def print_section(title: str):
    """Print section header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def example_basic_extraction():
    """Demonstrate basic emoji extraction."""
    print_section("1. Basic Emoji Extraction")
    
    utils = EmojiUtils()
    text = "Hello 👋 World 🌍! Today is great 🌟🎉"
    
    print(f"Input: {text}\n")
    
    emojis = utils.extract_emojis(text)
    print(f"Extracted emojis: {emojis}")
    
    count = utils.count_emojis(text)
    print(f"Total count: {count}")
    
    unique = utils.get_unique_emojis(text)
    print(f"Unique emojis: {unique}")
    
    counts = utils.get_emoji_counts(text)
    print(f"Emoji counts: {counts}")


def example_detection():
    """Demonstrate emoji detection."""
    print_section("2. Emoji Detection")
    
    utils = EmojiUtils()
    
    test_cases = [
        ("Hello 👋", True),
        ("Hello World", False),
        ("😀😃😄", True),
        ("", False),
    ]
    
    for text, expected in test_cases:
        result = utils.has_emoji(text)
        status = "✓" if result == expected else "✗"
        print(f"  {status} has_emoji('{text}'): {result}")
    
    print("\nChecking individual characters:")
    for char in ['😀', 'A', '🌍', '1', '❤️']:
        result = utils.is_emoji(char)
        print(f"  is_emoji('{char}'): {result}")


def example_removal():
    """Demonstrate emoji removal and replacement."""
    print_section("3. Emoji Removal & Replacement")
    
    utils = EmojiUtils()
    text = "Great job! 👏👏👏 Keep it up! 💪"
    
    print(f"Original: {text}\n")
    
    removed = utils.remove_emojis(text)
    print(f"Removed:  {removed}")
    
    replaced = utils.replace_emojis(text, "[emoji]")
    print(f"Replaced: {replaced}")
    
    replaced_stars = utils.replace_emojis(text, "⭐")
    print(f"Stars:    {replaced_stars}")


def example_unicode():
    """Demonstrate Unicode conversion."""
    print_section("4. Unicode Conversion")
    
    utils = EmojiUtils()
    
    emojis = ['😀', '👋', '🌍', '❤️', '🎉']
    
    print("Emoji to Unicode:")
    for emoji in emojis:
        unicode_str = utils.to_unicode_escape(emoji)
        print(f"  {emoji} → {unicode_str}")
    
    print("\nUnicode to Emoji:")
    unicode_strings = ['U+1F600', 'U+1F44B', 'U+1F30D']
    for unicode_str in unicode_strings:
        emoji = utils.from_unicode_escape(unicode_str)
        print(f"  {unicode_str} → {emoji}")


def example_skin_tones():
    """Demonstrate skin tone handling."""
    print_section("5. Skin Tone Handling")
    
    utils = EmojiUtils()
    
    # Base emoji
    base = "👋"
    print(f"Base emoji: {base}")
    
    # Get variants
    variants = utils.get_skin_tone_variants(base)
    print("\nSkin tone variants:")
    for tone, variant in variants.items():
        print(f"  {tone:15} → {variant}")
    
    # Strip skin tone
    print("\nStripping skin tones:")
    for tone, variant in variants.items():
        stripped = utils.strip_skin_tone(variant)
        print(f"  {variant} → {stripped}")


def example_analysis():
    """Demonstrate comprehensive analysis."""
    print_section("6. Comprehensive Analysis")
    
    utils = EmojiUtils()
    text = "Love it! ❤️❤️❤️ Great work 👏 Amazing 🌟 #blessed 🙏"
    
    print(f"Input: {text}\n")
    
    analysis = utils.analyze(text)
    
    print("Analysis Results:")
    print(f"  Total emojis:    {analysis.total_emojis}")
    print(f"  Unique emojis:   {analysis.unique_emojis}")
    print(f"  Emoji density:   {analysis.emoji_density}%")
    
    print("\n  Emoji counts:")
    for emoji, count in analysis.emoji_counts.items():
        print(f"    {emoji}: {count}")
    
    print("\n  Categories:")
    for category, count in analysis.categories.items():
        print(f"    {category}: {count}")
    
    print("\n  Emoji details:")
    for info in analysis.emoji_info:
        print(f"    {info.char}: {info.name} ({info.category.value})")


def example_categories():
    """Demonstrate category filtering."""
    print_section("7. Category Filtering")
    
    utils = EmojiUtils()
    text = "😀🐕🍎🚗⚽🌸"
    
    print(f"Input: {text}\n")
    print("Filtering by category:")
    
    categories = [
        (EmojiCategory.SMILEY, "Smiley"),
        (EmojiCategory.ANIMAL, "Animal"),
        (EmojiCategory.FOOD, "Food"),
        (EmojiCategory.TRAVEL, "Travel"),
        (EmojiCategory.ACTIVITY, "Activity"),
        (EmojiCategory.NATURE, "Nature"),
    ]
    
    for category, name in categories:
        filtered = utils.filter_by_category(text, category)
        if filtered:
            print(f"  {name:12} → {' '.join(filtered)}")


def example_positions():
    """Demonstrate position tracking."""
    print_section("8. Position Tracking")
    
    utils = EmojiUtils()
    text = "Hi 👋 there 🌍!"
    
    print(f"Input: {text}\n")
    print("Emoji positions (start, end, emoji):")
    
    positions = utils.get_emoji_positions(text)
    for start, end, emoji in positions:
        context = text[max(0, start-2):min(len(text), end+2)]
        print(f"  [{start:2}:{end:2}] {emoji}  (context: '{context}')")


def example_reverse():
    """Demonstrate text reversal with emoji preservation."""
    print_section("9. Text Reversal (Emoji-Safe)")
    
    utils = EmojiUtils()
    
    test_cases = [
        "Hello 👋",
        "😀😃😄",
        "A👋B🌍C",
        "Start 🎉 End",
    ]
    
    for text in test_cases:
        reversed_text = utils.reverse(text)
        print(f"  '{text}' → '{reversed_text}'")


def example_text_conversion():
    """Demonstrate text/emoji conversion."""
    print_section("10. Text/Emoji Conversion")
    
    utils = EmojiUtils()
    
    print("Emoji to text:")
    emojis = ['😀', '❤️', '👍', '🌍', '🎉']
    for emoji in emojis:
        text = utils.emoji_to_text(emoji)
        shortcode = utils.emoji_to_text(emoji, use_shortcodes=True)
        print(f"  {emoji} → '{text}' ({shortcode})")
    
    print("\nText to emoji:")
    texts = ['smile', 'heart', 'thumbs up', 'wave', 'party']
    for text in texts:
        emoji = utils.text_to_emoji(text)
        if emoji:
            print(f"  '{text}' → {emoji}")


def example_real_world():
    """Demonstrate real-world use cases."""
    print_section("11. Real-World Use Cases")
    
    utils = EmojiUtils()
    
    # Use case 1: Social media analysis
    print("\n📱 Social Media Analysis:")
    posts = [
        "Love this product! ❤️❤️❤️",
        "Great service 👍",
        "Not happy 😞",
        "Amazing! 🎉🎉🎉",
    ]
    
    for post in posts:
        analysis = utils.analyze(post)
        sentiment = "positive" if analysis.emoji_density > 5 else "neutral"
        print(f"  Post: {post[:30]}...")
        print(f"    Emojis: {analysis.total_emojis}, Density: {analysis.emoji_density}%, Sentiment: {sentiment}")
    
    # Use case 2: Content filtering
    print("\n🔒 Content Filtering:")
    messages = [
        "Hello! How are you?",
        "Hey! 👋 What's up?",
        "Check this out! 🔥🔥🔥",
    ]
    
    for msg in messages:
        if utils.has_emoji(msg):
            clean = utils.remove_emojis(msg)
            print(f"  Original: {msg}")
            print(f"  Clean:    {clean}")
    
    # Use case 3: Emoji statistics
    print("\n📊 Emoji Statistics:")
    text = "😀😃😄😀😁😀😆😅😂🤣"
    analysis = utils.analyze(text)
    print(f"  Text: {text}")
    print(f"  Most used: {max(analysis.emoji_counts.items(), key=lambda x: x[1])}")
    print(f"  Variety: {analysis.unique_emojis} unique out of {analysis.total_emojis} total")


def example_module_functions():
    """Demonstrate module-level convenience functions."""
    print_section("12. Module-Level Functions")
    
    text = "Hello 👋 World 🌍!"
    
    print(f"Input: {text}\n")
    print("Using module-level functions:")
    print(f"  extract_emojis(text): {extract_emojis(text)}")
    print(f"  count_emojis(text):   {count_emojis(text)}")
    print(f"  has_emoji(text):      {has_emoji(text)}")
    print(f"  remove_emojis(text):  {remove_emojis(text)}")
    
    analysis = analyze(text)
    print(f"  analyze(text):        {analysis.total_emojis} emojis, {analysis.unique_emojis} unique")


def main():
    """Run all examples."""
    print("\n" + "🎭" * 30)
    print("   AllToolkit - Emoji Utilities Examples")
    print("🎭" * 30)
    
    examples = [
        example_basic_extraction,
        example_detection,
        example_removal,
        example_unicode,
        example_skin_tones,
        example_analysis,
        example_categories,
        example_positions,
        example_reverse,
        example_text_conversion,
        example_real_world,
        example_module_functions,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n❌ Error in {example.__name__}: {e}")
    
    print("\n" + "🎭" * 30)
    print("   Examples Complete!")
    print("🎭" * 30 + "\n")


if __name__ == '__main__':
    main()
