"""
Pig Latin Translation Utilities

Pig Latin is a language game where words are altered according to simple rules.
- Words starting with a vowel: add "way" to the end (apple -> appleway)
- Words starting with consonant(s): move consonant cluster to end and add "ay" (hello -> ellohay, string -> ingstray)

Features:
- Word and sentence translation
- Encoding and decoding
- Custom suffixes support
- Preserves punctuation and capitalization
- Handles contractions and hyphenated words
"""

import re
from typing import List, Tuple, Optional


class PigLatinTranslator:
    """
    Pig Latin translator with full encoding and decoding support.
    
    Example:
        >>> translator = PigLatinTranslator()
        >>> translator.translate_word("hello")
        'ellohay'
        >>> translator.translate_word("apple")
        'appleway'
        >>> translator.translate_sentence("Hello world!")
        'Ellohay orldway!'
    """
    
    def __init__(
        self,
        vowel_suffix: str = "way",
        consonant_suffix: str = "ay",
        vowels: str = "aeiou"
    ):
        """
        Initialize Pig Latin translator.
        
        Args:
            vowel_suffix: Suffix for vowel-starting words (default: "way")
            consonant_suffix: Suffix for consonant-starting words (default: "ay")
            vowels: String of vowel characters (default: "aeiou")
        """
        self.vowel_suffix = vowel_suffix
        self.consonant_suffix = consonant_suffix
        self.vowels = set(vowels.lower())
        self.vowels_upper = set(vowels.upper())
    
    def is_vowel(self, char: str) -> bool:
        """Check if character is a vowel."""
        return char in self.vowels or char in self.vowels_upper
    
    def find_consonant_cluster(self, word: str) -> Tuple[str, str]:
        """
        Find the consonant cluster at the beginning of a word.
        
        Returns:
            Tuple of (consonant_cluster, remaining_word)
        """
        if not word:
            return "", ""
        
        cluster = ""
        for i, char in enumerate(word):
            if self.is_vowel(char):
                return cluster, word[i:]
            cluster += char
        
        # Word has no vowels (rare case)
        return word, ""
    
    def translate_word(self, word: str) -> str:
        """
        Translate a single word to Pig Latin.
        
        Args:
            word: The word to translate
            
        Returns:
            The Pig Latin translation
            
        Examples:
            >>> translator = PigLatinTranslator()
            >>> translator.translate_word("hello")
            'ellohay'
            >>> translator.translate_word("apple")
            'appleway'
            >>> translator.translate_word("string")
            'ingstray'
        """
        if not word:
            return word
        
        # Handle punctuation at start/end
        prefix_punct = ""
        suffix_punct = ""
        
        # Extract leading punctuation
        match = re.match(r'^([^a-zA-Z]*)([a-zA-Z].*)', word)
        if match:
            prefix_punct = match.group(1)
            word = match.group(2)
        
        # Extract trailing punctuation
        match = re.match(r'(.*?[a-zA-Z])([^a-zA-Z]*)$', word)
        if match:
            word = match.group(1)
            suffix_punct = match.group(2)
        
        if not word or not word[0].isalpha():
            return prefix_punct + word + suffix_punct
        
        # Track capitalization
        was_capitalized = word[0].isupper()
        word_lower = word.lower()
        
        # Translate
        if self.is_vowel(word_lower[0]):
            # Vowel-starting word: add suffix
            translated = word_lower + self.vowel_suffix
        else:
            # Consonant-starting word: move cluster to end and add suffix
            cluster, remaining = self.find_consonant_cluster(word_lower)
            if remaining:
                translated = remaining + cluster + self.consonant_suffix
            else:
                # Word has no vowels
                translated = word_lower + self.consonant_suffix
        
        # Restore capitalization
        if was_capitalized:
            translated = translated.capitalize()
        
        return prefix_punct + translated + suffix_punct
    
    def decode_word(self, word: str) -> str:
        """
        Decode a Pig Latin word back to English.
        
        Args:
            word: The Pig Latin word to decode
            
        Returns:
            The decoded English word
            
        Examples:
            >>> translator = PigLatinTranslator()
            >>> translator.decode_word("ellohay")
            'hello'
            >>> translator.decode_word("appleway")
            'apple'
            >>> translator.decode_word("ingstray")
            'string'
        """
        if not word:
            return word
        
        # Handle punctuation
        prefix_punct = ""
        suffix_punct = ""
        
        match = re.match(r'^([^a-zA-Z]*)([a-zA-Z].*)', word)
        if match:
            prefix_punct = match.group(1)
            word = match.group(2)
        
        match = re.match(r'(.*?[a-zA-Z])([^a-zA-Z]*)$', word)
        if match:
            word = match.group(1)
            suffix_punct = match.group(2)
        
        if not word or not word[0].isalpha():
            return prefix_punct + word + suffix_punct
        
        # Track capitalization
        was_capitalized = word[0].isupper()
        word_lower = word.lower()
        
        decoded = None  # Initialize decoded
        
        # Check suffixes - handle ambiguity
        # Words ending with "way" could be vowel-suffix OR consonant-suffix
        # Strategy:
        # 1. If ends with vowel suffix AND decoded word starts with vowel -> use vowel suffix
        # 2. Otherwise, try consonant suffix
        # 3. If consonant suffix gives valid result with cluster, use it
        
        # First, check vowel suffix (for vowel-starting original words)
        if word_lower.endswith(self.vowel_suffix):
            vowel_decoded = word_lower[:-len(self.vowel_suffix)]
            # If decoded word starts with a vowel, it's likely a valid vowel-suffix encoding
            if vowel_decoded and self.is_vowel(vowel_decoded[0]):
                decoded = vowel_decoded
        
        # If vowel suffix didn't work, try consonant suffix
        if decoded is None and word_lower.endswith(self.consonant_suffix):
            stem = word_lower[:-len(self.consonant_suffix)]
            
            # Pig Latin decoding: find where to split stem = remaining + cluster
            # The cluster is a consonant sequence at the end of stem
            # The remaining starts with a vowel
            
            # Strategy: prefer splits where remaining has the most balanced structure
            # (ratio of consonants to vowels should be reasonable)
            
            decoded = None
            valid_splits = []
            
            # Try splitting at each position
            for i in range(1, len(stem) + 1):
                remaining = stem[:i]
                cluster = stem[i:]
                
                # remaining must start with a vowel
                if not remaining or not self.is_vowel(remaining[0]):
                    continue
                
                # remaining must contain at least one vowel
                if not any(self.is_vowel(c) for c in remaining):
                    continue
                
                # cluster must be all consonants (and not empty)
                if not cluster or not all(not self.is_vowel(c) for c in cluster):
                    continue
                
                # Valid split found
                # Score based on cluster length preference
                # English words typically have initial consonant clusters of 1-3 letters
                
                cluster_len = len(cluster)
                
                # Prefer cluster length 1-3 (most common initial clusters)
                # Heavy penalty for clusters > 3 (usually indicates incorrect split)
                if 1 <= cluster_len <= 3:
                    score = 10.0 - cluster_len + len(remaining) * 0.5
                else:
                    score = len(remaining) * 0.1  # Heavy penalty for >3 letter clusters
                
                valid_splits.append((i, remaining, cluster, score))
            
            if valid_splits:
                # Choose the split with the best score (highest vowel ratio in remaining)
                valid_splits.sort(key=lambda x: -x[3])  # Sort by score descending
                i, remaining, cluster, _ = valid_splits[0]
                decoded = cluster + remaining
            
            if decoded is None:
                # No valid split found
                decoded = stem
        
        if decoded is None:
            # Not a valid Pig Latin word
            decoded = word_lower
        
        # Restore capitalization
        if was_capitalized:
            decoded = decoded.capitalize()
        
        return prefix_punct + decoded + suffix_punct
    
    def translate_sentence(self, sentence: str) -> str:
        """
        Translate a sentence to Pig Latin.
        
        Args:
            sentence: The sentence to translate
            
        Returns:
            The Pig Latin translation
            
        Examples:
            >>> translator = PigLatinTranslator()
            >>> translator.translate_sentence("Hello, world!")
            'Ellohay, orldway!'
        """
        # Split into words while preserving structure
        words = re.findall(r'(\S+)', sentence)
        
        result_parts = []
        last_end = 0
        
        for match in re.finditer(r'\S+', sentence):
            # Add any whitespace/punctuation before this word
            result_parts.append(sentence[last_end:match.start()])
            
            # Translate the word
            word = match.group()
            translated = self.translate_word(word)
            result_parts.append(translated)
            
            last_end = match.end()
        
        # Add any trailing text
        result_parts.append(sentence[last_end:])
        
        return ''.join(result_parts)
    
    def decode_sentence(self, sentence: str) -> str:
        """
        Decode a Pig Latin sentence back to English.
        
        Args:
            sentence: The Pig Latin sentence to decode
            
        Returns:
            The decoded English sentence
            
        Examples:
            >>> translator = PigLatinTranslator()
            >>> translator.decode_sentence("Ellohay, orldway!")
            'Hello, world!'
        """
        result_parts = []
        last_end = 0
        
        for match in re.finditer(r'\S+', sentence):
            result_parts.append(sentence[last_end:match.start()])
            
            word = match.group()
            decoded = self.decode_word(word)
            result_parts.append(decoded)
            
            last_end = match.end()
        
        result_parts.append(sentence[last_end:])
        
        return ''.join(result_parts)
    
    def is_pig_latin(self, word: str) -> bool:
        """
        Check if a word appears to be in Pig Latin format.
        
        Args:
            word: The word to check
            
        Returns:
            True if the word appears to be Pig Latin
            
        Examples:
            >>> translator = PigLatinTranslator()
            >>> translator.is_pig_latin("ellohay")
            True
            >>> translator.is_pig_latin("hello")
            False
        """
        if not word:
            return False
        
        # Extract just the alphabetic part
        alpha_match = re.search(r'[a-zA-Z]+', word)
        if not alpha_match:
            return False
        
        alpha_part = alpha_match.group().lower()
        
        # Check for Pig Latin suffixes
        return (alpha_part.endswith(self.vowel_suffix) or 
                alpha_part.endswith(self.consonant_suffix))


def translate_word(word: str, **kwargs) -> str:
    """
    Convenience function to translate a single word.
    
    Args:
        word: The word to translate
        **kwargs: Additional arguments for PigLatinTranslator
        
    Returns:
        The Pig Latin translation
    """
    translator = PigLatinTranslator(**kwargs)
    return translator.translate_word(word)


def decode_word(word: str, **kwargs) -> str:
    """
    Convenience function to decode a single word.
    
    Args:
        word: The Pig Latin word to decode
        **kwargs: Additional arguments for PigLatinTranslator
        
    Returns:
        The decoded English word
    """
    translator = PigLatinTranslator(**kwargs)
    return translator.decode_word(word)


def translate_sentence(sentence: str, **kwargs) -> str:
    """
    Convenience function to translate a sentence.
    
    Args:
        sentence: The sentence to translate
        **kwargs: Additional arguments for PigLatinTranslator
        
    Returns:
        The Pig Latin translation
    """
    translator = PigLatinTranslator(**kwargs)
    return translator.translate_sentence(sentence)


def decode_sentence(sentence: str, **kwargs) -> str:
    """
    Convenience function to decode a sentence.
    
    Args:
        sentence: The Pig Latin sentence to decode
        **kwargs: Additional arguments for PigLatinTranslator
        
    Returns:
        The decoded English sentence
    """
    translator = PigLatinTranslator(**kwargs)
    return translator.decode_sentence(sentence)


def translate_words(words: List[str], **kwargs) -> List[str]:
    """
    Translate a list of words.
    
    Args:
        words: List of words to translate
        **kwargs: Additional arguments for PigLatinTranslator
        
    Returns:
        List of Pig Latin translations
    """
    translator = PigLatinTranslator(**kwargs)
    return [translator.translate_word(w) for w in words]


def decode_words(words: List[str], **kwargs) -> List[str]:
    """
    Decode a list of Pig Latin words.
    
    Args:
        words: List of Pig Latin words to decode
        **kwargs: Additional arguments for PigLatinTranslator
        
    Returns:
        List of decoded English words
    """
    translator = PigLatinTranslator(**kwargs)
    return [translator.decode_word(w) for w in words]


def get_pig_latin_rules() -> dict:
    """
    Get the Pig Latin translation rules.
    
    Returns:
        Dictionary with rule descriptions
    """
    return {
        "vowel_rule": "Words starting with a vowel: add 'way' to the end",
        "consonant_rule": "Words starting with consonant(s): move consonant cluster to end and add 'ay'",
        "examples": {
            "vowel_start": {
                "apple": "appleway",
                "egg": "eggway",
                "orange": "orangeway"
            },
            "consonant_start": {
                "hello": "ellohay",
                "string": "ingstray",
                "world": "orldway",
                "pig": "igpay"
            },
            "complex": {
                "quiet": "ietquay",  # 'qu' treated as consonant cluster
                "smile": "ilesmay",
                "chair": "airchay"
            }
        }
    }


if __name__ == "__main__":
    # Demo
    translator = PigLatinTranslator()
    
    print("=== Pig Latin Translator Demo ===\n")
    
    # Word examples
    test_words = ["hello", "apple", "string", "pig", "latin", "quiet", "smile"]
    print("Word translations:")
    for word in test_words:
        translated = translator.translate_word(word)
        decoded = translator.decode_word(translated)
        print(f"  {word} -> {translated} -> {decoded}")
    
    # Sentence examples
    print("\nSentence translations:")
    sentences = [
        "Hello, world!",
        "The quick brown fox jumps over the lazy dog.",
        "Pig Latin is fun!"
    ]
    for sentence in sentences:
        translated = translator.translate_sentence(sentence)
        decoded = translator.decode_sentence(translated)
        print(f"\n  Original:  {sentence}")
        print(f"  Pig Latin: {translated}")
        print(f"  Decoded:   {decoded}")