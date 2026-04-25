"""
Lorem Ipsum Text Generator
==========================

A zero-dependency Lorem Ipsum text generator for creating placeholder content.
Supports words, sentences, paragraphs, and custom generation patterns.

Features:
- Generate words, sentences, paragraphs
- Customizable word count ranges
- Consistent seeding for reproducible output
- Multiple output formats
- No external dependencies

Author: AllToolkit
Date: 2026-04-25
"""

import random
import re
from typing import List, Optional, Union


# Classic Lorem Ipsum word pool
LOREM_WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
    "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
    "velit", "esse", "cillum", "fugiat", "nulla", "pariatur", "excepteur", "sint",
    "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
    "deserunt", "mollit", "anim", "id", "est", "laborum", "perspiciatis", "unde",
    "omnis", "iste", "natus", "error", "voluptatem", "accusantium", "doloremque",
    "laudantium", "totam", "rem", "aperiam", "eaque", "ipsa", "quae", "ab", "illo",
    "inventore", "veritatis", "quasi", "architecto", "beatae", "vitae", "dicta",
    "explicabo", "nemo", "ipsam", "quia", "voluptas", "aspernatur", "aut", "odit",
    "fugit", "consequuntur", "magni", "dolores", "eos", "ratione", "sequi",
    "nesciunt", "neque", "porro", "quisquam", "dolorem", "adipisci", "numquam",
    "eius", "modi", "tempora", "magnam", "quaerat", "adipisci", "velit", "esse",
    "quam", "nihil", "molestiae", "illum", "fugiat", "quo", "voluptas", "nulla",
    "pariatur", "at", "vero", "accusamus", "iusto", "dignissimos", "ducimus",
    "blanditiis", "praesentium", "voluptatum", "deleniti", "atque", "corrupti",
    "quos", "dolores", "quas", "molestias", "excepturi", "occaecati", "cupiditate",
    "non", "provident", "similique", "sunt", "culpa", "officia", "deserunt",
    "mollitia", "animi", "laborum", "dolorum", "fuga", "harum", "quidem", "rerum",
    "facilis", "expedita", "distinctio", "nam", "libero", "tempore", "cum", "soluta",
    "nobis", "eligendi", "optio", "cumque", "impedit", "quo", "minus", "quod",
    "maxime", "placeat", "facere", "possimus", "omnis", "voluptas", "assumenda",
    "repudiandae", "recusandae", "necessitatibus", "saepe", "eveniet", "et",
    "perferendis", "doloribus", "asperiores", "repellat"
]

# Extended word pool for more variety
EXTENDED_WORDS = [
    "efficitur", "tincidunt", "ligula", "lectus", "sagittis", "turpis", "neque",
    "auctor", "cras", "justo", "habitant", "morbi", "tristique", "senectus",
    "netus", "malesuada", "fames", "ac", "turpis", "egestas", "integer", "aliquet",
    "massa", "lorem", "eleifend", "mi", "nulla", "facilisi", "etiam", "dignissim",
    "tortor", "risus", "praesent", "elementum", "facilisis", "leo", "vel",
    "porttitor", "consequat", "mauris", "augue", "neque", "gravida", "fermentum",
    "orci", "faucibus", "scelerisque", "eleifend", "congue", "nisl", "tortor",
    "pretium", "viverra", "suspendisse", "potenti", "vulputate", "euismod",
    "consequat", "semper", "viverra", "nam", "laoreet", "sapien", "augue",
    "blandit", "cursus", "risus", "pretium", "imperdiet", "curabitur", "lacinia",
    "tortor", "quis", "arcu", "facilisis", "luctus", "ultrices", "posuere",
    "cubilia", "curae", "donec", "dapibus", "ultricies", "leo", "risus", "tristique",
    "senectus", "feugiat", "risus", "pharetra", "convallis", "sem", "pharetra",
    "hendrerit", "velit", "gravida", "ornare", "massa", "tincidunt", "nunc",
    "pulvinar", "sapien", "et", "ligula", "ullamcorper", "malesuada", "proin",
    "libero", "nunc", "feugiat", "pretium", "nec", "nisl", "consequat", "sem",
    "fringilla", "tortor", "rhoncus", "est", "pellentesque", "elit", "ullamcorper",
    "viverra", "nisl", "nulla", "facilisi", "etiam", "vel", "erat", "velit",
    "scelerisque", "in", "dictum", "non", "consectetur", "risus", "nulla",
    "facilisi", "maecenas", "ultricies", "lacus", "sed", "arcu", "non", "sodales",
    "neque", "condimentum", "eget", "dolores", "iaculis", "nunc", "sed", "augue",
    "lacus", "viverra", "vitae", "congue", "eu", "consequat", "ac", "felis",
    "donec", "odio", "pellentesque", "dictum", "stadium", "tempor", "commodo",
    "ullamcorper", "lacus", "nec", "elementum", "nibh", "tellus", "molestie",
    "nunc", "non", "blandit", "massa", "enim", "nec", "dui", "nunc", "mattis",
    "enim", "ut", "tellus", "elementum", "sagittis", "vitae", "et", "leo",
    "duis", "ut", "diam", "quam", "nulla", "porttitor", "massa", "id", "neque",
    "aliquam", "vestibulum", "morbi", "blandit", "cursus", "risus", "at",
    "ultrices", "mi", "tempus", "imperdiet", "nulla", "malesuada", "pellentesque",
    "elit", "eget", "gravida", "cum", "sociis", "natoque", "penatibus", "et",
    "magnis", "dis", "parturient", "montes", "nascetur", "ridiculus", "mus",
    "mauris", "vel", "ultrices", "erat", "tincidunt", "dui", "ut", "ornare",
    "lectus", "sit", "est", "vel", "rhoncus", "est", "pellentesque", "elit"
]


class LoremGenerator:
    """
    Lorem Ipsum text generator with configurable options.
    
    Usage:
        gen = LoremGenerator(seed=42)
        print(gen.words(5))
        print(gen.sentences(3))
        print(gen.paragraphs(2))
    """
    
    def __init__(
        self,
        seed: Optional[int] = None,
        use_extended: bool = False
    ):
        """
        Initialize the Lorem generator.
        
        Args:
            seed: Random seed for reproducible output
            use_extended: Use extended word pool for more variety
        """
        self.rng = random.Random(seed)
        self.word_pool = EXTENDED_WORDS if use_extended else LOREM_WORDS
        self._cache: dict = {}
    
    def _get_word(self) -> str:
        """Get a random word from the pool."""
        return self.rng.choice(self.word_pool)
    
    def _get_words(self, count: int) -> List[str]:
        """Get a list of random words."""
        return [self._get_word() for _ in range(count)]
    
    def words(
        self,
        count: int = 5,
        as_list: bool = False,
        capitalize_first: bool = True
    ) -> Union[str, List[str]]:
        """
        Generate random words.
        
        Args:
            count: Number of words to generate
            as_list: Return as list instead of string
            capitalize_first: Capitalize the first word
        
        Returns:
            Space-separated words string or list of words
        """
        word_list = self._get_words(count)
        
        if capitalize_first and word_list:
            word_list[0] = word_list[0].capitalize()
        
        if as_list:
            return word_list
        return ' '.join(word_list)
    
    def sentence(
        self,
        min_words: int = 8,
        max_words: int = 15
    ) -> str:
        """
        Generate a single sentence.
        
        Args:
            min_words: Minimum words in sentence
            max_words: Maximum words in sentence
        
        Returns:
            A complete sentence with proper capitalization and punctuation
        """
        count = self.rng.randint(min_words, max_words)
        word_list = self._get_words(count)
        
        # Capitalize first word
        if word_list:
            word_list[0] = word_list[0].capitalize()
        
        # Add random punctuation
        punctuation = self.rng.choice(['.', '.', '.', '!', '?'])
        
        return ' '.join(word_list) + punctuation
    
    def sentences(
        self,
        count: int = 3,
        min_words: int = 8,
        max_words: int = 15,
        as_list: bool = False
    ) -> Union[str, List[str]]:
        """
        Generate multiple sentences.
        
        Args:
            count: Number of sentences to generate
            min_words: Minimum words per sentence
            max_words: Maximum words per sentence
            as_list: Return as list instead of string
        
        Returns:
            Space-separated sentences string or list of sentences
        """
        sentence_list = [
            self.sentence(min_words, max_words) 
            for _ in range(count)
        ]
        
        if as_list:
            return sentence_list
        return ' '.join(sentence_list)
    
    def paragraph(
        self,
        min_sentences: int = 4,
        max_sentences: int = 7,
        min_words: int = 8,
        max_words: int = 15
    ) -> str:
        """
        Generate a single paragraph.
        
        Args:
            min_sentences: Minimum sentences in paragraph
            max_sentences: Maximum sentences in paragraph
            min_words: Minimum words per sentence
            max_words: Maximum words per sentence
        
        Returns:
            A paragraph of lorem ipsum text
        """
        count = self.rng.randint(min_sentences, max_sentences)
        return self.sentences(count, min_words, max_words)
    
    def paragraphs(
        self,
        count: int = 2,
        min_sentences: int = 4,
        max_sentences: int = 7,
        min_words: int = 8,
        max_words: int = 15,
        as_list: bool = False,
        separator: str = '\n\n'
    ) -> Union[str, List[str]]:
        """
        Generate multiple paragraphs.
        
        Args:
            count: Number of paragraphs to generate
            min_sentences: Minimum sentences per paragraph
            max_sentences: Maximum sentences per paragraph
            min_words: Minimum words per sentence
            max_words: Maximum words per sentence
            as_list: Return as list instead of string
            separator: Paragraph separator (default: double newline)
        
        Returns:
            Separator-joined paragraphs string or list of paragraphs
        """
        paragraph_list = [
            self.paragraph(min_sentences, max_sentences, min_words, max_words)
            for _ in range(count)
        ]
        
        if as_list:
            return paragraph_list
        return separator.join(paragraph_list)
    
    def title(
        self,
        min_words: int = 3,
        max_words: int = 6
    ) -> str:
        """
        Generate a title-style text.
        
        Args:
            min_words: Minimum words in title
            max_words: Maximum words in title
        
        Returns:
            Title-cased text without ending punctuation
        """
        count = self.rng.randint(min_words, max_words)
        word_list = self._get_words(count)
        
        # Title case each word
        title_words = [word.capitalize() for word in word_list]
        
        return ' '.join(title_words)
    
    def headline(self, min_words: int = 4, max_words: int = 8) -> str:
        """
        Generate a headline.
        
        Args:
            min_words: Minimum words
            max_words: Maximum words
        
        Returns:
            A headline string
        """
        return self.title(min_words, max_words)
    
    def html_paragraphs(
        self,
        count: int = 2,
        min_sentences: int = 4,
        max_sentences: int = 7,
        wrap_tag: str = 'p'
    ) -> str:
        """
        Generate HTML-wrapped paragraphs.
        
        Args:
            count: Number of paragraphs
            min_sentences: Minimum sentences per paragraph
            max_sentences: Maximum sentences per paragraph
            wrap_tag: HTML tag to wrap each paragraph
        
        Returns:
            HTML string with wrapped paragraphs
        """
        paragraphs = self.paragraphs(count, min_sentences, max_sentences, as_list=True)
        
        wrapped = [f'<{wrap_tag}>{p}</{wrap_tag}>' for p in paragraphs]
        return '\n'.join(wrapped)
    
    def list_items(
        self,
        count: int = 5,
        min_words: int = 3,
        max_words: int = 8,
        ordered: bool = False
    ) -> str:
        """
        Generate a list of items.
        
        Args:
            count: Number of list items
            min_words: Minimum words per item
            max_words: Maximum words per item
            ordered: Use ordered list (1. 2. 3.) instead of bullet points
        
        Returns:
            Formatted list string
        """
        items = []
        for i in range(count):
            word_count = self.rng.randint(min_words, max_words)
            text = self.words(word_count, capitalize_first=True)
            if ordered:
                items.append(f'{i + 1}. {text}')
            else:
                items.append(f'• {text}')
        
        return '\n'.join(items)
    
    def buzzword(self) -> str:
        """Generate a single buzzword/keyword."""
        return self._get_word().capitalize()
    
    def buzzwords(self, count: int = 5) -> str:
        """
        Generate comma-separated buzzwords.
        
        Args:
            count: Number of buzzwords
        
        Returns:
            Comma-separated buzzwords string
        """
        words = [self._get_word().capitalize() for _ in range(count)]
        return ', '.join(words)
    
    def email(self, domain: str = "example.com") -> str:
        """
        Generate a fake email address.
        
        Args:
            domain: Email domain
        
        Returns:
            Fake email address
        """
        name = self._get_word()
        number = self.rng.randint(1, 999)
        return f"{name}{number}@{domain}"
    
    def username(self) -> str:
        """Generate a fake username."""
        name = self._get_word()
        number = self.rng.randint(1, 9999)
        return f"{name}{number}"
    
    def url(self, domain: str = "example.com") -> str:
        """
        Generate a fake URL.
        
        Args:
            domain: URL domain
        
        Returns:
            Fake URL string
        """
        path1 = self._get_word()
        path2 = self._get_word()
        return f"https://{domain}/{path1}/{path2}"
    
    def phone(self) -> str:
        """Generate a fake phone number."""
        area = self.rng.randint(200, 999)
        prefix = self.rng.randint(200, 999)
        line = self.rng.randint(1000, 9999)
        return f"({area}) {prefix}-{line}"
    
    def address(self) -> str:
        """Generate a fake address."""
        number = self.rng.randint(100, 9999)
        street = self._get_word().capitalize()
        suffix = self.rng.choice(['St', 'Ave', 'Blvd', 'Rd', 'Dr', 'Ln'])
        city = self._get_word().capitalize() + self._get_word().capitalize()
        state = ''.join(self.rng.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 2))
        zip_code = self.rng.randint(10000, 99999)
        
        return f"{number} {street} {suffix}, {city}, {state} {zip_code}"
    
    def name(self) -> str:
        """Generate a fake name."""
        first = self._get_word().capitalize()
        last = self._get_word().capitalize()
        return f"{first} {last}"
    
    def company(self) -> str:
        """Generate a fake company name."""
        words = [
            self._get_word().capitalize(),
            self._get_word().capitalize()
        ]
        suffix = self.rng.choice(['Inc', 'LLC', 'Corp', 'Ltd', 'Co', 'Group'])
        return f"{' '.join(words)} {suffix}"
    
    def reset_seed(self, seed: Optional[int] = None) -> None:
        """
        Reset the random seed.
        
        Args:
            seed: New random seed (None for random seed)
        """
        self.rng = random.Random(seed)


# Singleton instance for convenience functions
_default_generator = LoremGenerator()


def words(count: int = 5, as_list: bool = False, seed: Optional[int] = None) -> Union[str, List[str]]:
    """
    Generate random words.
    
    Args:
        count: Number of words
        as_list: Return as list
        seed: Random seed for reproducibility
    
    Returns:
        Space-separated words or list
    """
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.words(count, as_list)


def sentence(min_words: int = 8, max_words: int = 15, seed: Optional[int] = None) -> str:
    """
    Generate a single sentence.
    
    Args:
        min_words: Minimum words
        max_words: Maximum words
        seed: Random seed
    
    Returns:
        Generated sentence
    """
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.sentence(min_words, max_words)


def sentences(
    count: int = 3,
    min_words: int = 8,
    max_words: int = 15,
    as_list: bool = False,
    seed: Optional[int] = None
) -> Union[str, List[str]]:
    """
    Generate multiple sentences.
    
    Args:
        count: Number of sentences
        min_words: Minimum words per sentence
        max_words: Maximum words per sentence
        as_list: Return as list
        seed: Random seed
    
    Returns:
        Generated sentences
    """
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.sentences(count, min_words, max_words, as_list)


def paragraph(
    min_sentences: int = 4,
    max_sentences: int = 7,
    min_words: int = 8,
    max_words: int = 15,
    seed: Optional[int] = None
) -> str:
    """
    Generate a single paragraph.
    
    Args:
        min_sentences: Minimum sentences
        max_sentences: Maximum sentences
        min_words: Minimum words per sentence
        max_words: Maximum words per sentence
        seed: Random seed
    
    Returns:
        Generated paragraph
    """
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.paragraph(min_sentences, max_sentences, min_words, max_words)


def paragraphs(
    count: int = 2,
    min_sentences: int = 4,
    max_sentences: int = 7,
    min_words: int = 8,
    max_words: int = 15,
    as_list: bool = False,
    seed: Optional[int] = None
) -> Union[str, List[str]]:
    """
    Generate multiple paragraphs.
    
    Args:
        count: Number of paragraphs
        min_sentences: Minimum sentences per paragraph
        max_sentences: Maximum sentences per paragraph
        min_words: Minimum words per sentence
        max_words: Maximum words per sentence
        as_list: Return as list
        seed: Random seed
    
    Returns:
        Generated paragraphs
    """
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.paragraphs(count, min_sentences, max_sentences, min_words, max_words, as_list)


def title(min_words: int = 3, max_words: int = 6, seed: Optional[int] = None) -> str:
    """
    Generate a title.
    
    Args:
        min_words: Minimum words
        max_words: Maximum words
        seed: Random seed
    
    Returns:
        Generated title
    """
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.title(min_words, max_words)


def headline(min_words: int = 4, max_words: int = 8, seed: Optional[int] = None) -> str:
    """
    Generate a headline.
    
    Args:
        min_words: Minimum words
        max_words: Maximum words
        seed: Random seed
    
    Returns:
        Generated headline
    """
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.headline(min_words, max_words)


def html_paragraphs(
    count: int = 2,
    min_sentences: int = 4,
    max_sentences: int = 7,
    wrap_tag: str = 'p',
    seed: Optional[int] = None
) -> str:
    """
    Generate HTML-wrapped paragraphs.
    
    Args:
        count: Number of paragraphs
        min_sentences: Minimum sentences per paragraph
        max_sentences: Maximum sentences per paragraph
        wrap_tag: HTML tag wrapper
        seed: Random seed
    
    Returns:
        HTML string
    """
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.html_paragraphs(count, min_sentences, max_sentences, wrap_tag)


def list_items(
    count: int = 5,
    min_words: int = 3,
    max_words: int = 8,
    ordered: bool = False,
    seed: Optional[int] = None
) -> str:
    """
    Generate a list of items.
    
    Args:
        count: Number of items
        min_words: Minimum words per item
        max_words: Maximum words per item
        ordered: Use ordered list
        seed: Random seed
    
    Returns:
        Formatted list string
    """
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.list_items(count, min_words, max_words, ordered)


def buzzword(seed: Optional[int] = None) -> str:
    """Generate a single buzzword."""
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.buzzword()


def buzzwords(count: int = 5, seed: Optional[int] = None) -> str:
    """Generate comma-separated buzzwords."""
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.buzzwords(count)


def email(domain: str = "example.com", seed: Optional[int] = None) -> str:
    """Generate a fake email address."""
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.email(domain)


def username(seed: Optional[int] = None) -> str:
    """Generate a fake username."""
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.username()


def url(domain: str = "example.com", seed: Optional[int] = None) -> str:
    """Generate a fake URL."""
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.url(domain)


def phone(seed: Optional[int] = None) -> str:
    """Generate a fake phone number."""
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.phone()


def address(seed: Optional[int] = None) -> str:
    """Generate a fake address."""
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.address()


def name(seed: Optional[int] = None) -> str:
    """Generate a fake name."""
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.name()


def company(seed: Optional[int] = None) -> str:
    """Generate a fake company name."""
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    return gen.company()


# Convenience function for generating any type
def generate(
    content_type: str = "paragraph",
    count: int = 1,
    seed: Optional[int] = None,
    **kwargs
) -> str:
    """
    Generate content by type.
    
    Args:
        content_type: Type of content (words, sentence, sentences, paragraph, 
                      paragraphs, title, headline, html_paragraphs, list_items,
                      buzzwords, email, username, url, phone, address, name, company)
        count: Count parameter (meaning varies by type)
        seed: Random seed
        **kwargs: Additional arguments passed to the generator
    
    Returns:
        Generated content string
    """
    gen = LoremGenerator(seed) if seed is not None else _default_generator
    
    type_mapping = {
        'words': lambda: gen.words(count, **kwargs),
        'sentence': lambda: gen.sentence(**kwargs),
        'sentences': lambda: gen.sentences(count, **kwargs),
        'paragraph': lambda: gen.paragraph(**kwargs),
        'paragraphs': lambda: gen.paragraphs(count, **kwargs),
        'title': lambda: gen.title(**kwargs),
        'headline': lambda: gen.headline(**kwargs),
        'html_paragraphs': lambda: gen.html_paragraphs(count, **kwargs),
        'list_items': lambda: gen.list_items(count, **kwargs),
        'buzzword': lambda: gen.buzzword(),
        'buzzwords': lambda: gen.buzzwords(count),
        'email': lambda: gen.email(**kwargs),
        'username': lambda: gen.username(),
        'url': lambda: gen.url(**kwargs),
        'phone': lambda: gen.phone(),
        'address': lambda: gen.address(),
        'name': lambda: gen.name(),
        'company': lambda: gen.company(),
    }
    
    content_type = content_type.lower()
    if content_type not in type_mapping:
        raise ValueError(
            f"Unknown content type: {content_type}. "
            f"Valid types: {list(type_mapping.keys())}"
        )
    
    return type_mapping[content_type]()


if __name__ == "__main__":
    # Demo output
    print("=" * 60)
    print("Lorem Ipsum Generator Demo")
    print("=" * 60)
    
    gen = LoremGenerator(seed=42)
    
    print("\n📝 Words (5):")
    print(gen.words(5))
    
    print("\n📝 Sentence:")
    print(gen.sentence())
    
    print("\n📝 Sentences (2):")
    print(gen.sentences(2))
    
    print("\n📝 Paragraph:")
    print(gen.paragraph())
    
    print("\n📝 Paragraphs (2):")
    print(gen.paragraphs(2))
    
    print("\n📝 Title:")
    print(gen.title())
    
    print("\n📝 Headline:")
    print(gen.headline())
    
    print("\n📝 HTML Paragraphs (2):")
    print(gen.html_paragraphs(2))
    
    print("\n📝 List Items (3, ordered):")
    print(gen.list_items(3, ordered=True))
    
    print("\n📝 List Items (3, unordered):")
    print(gen.list_items(3, ordered=False))
    
    print("\n📝 Fake Data:")
    print(f"  Name: {gen.name()}")
    print(f"  Email: {gen.email()}")
    print(f"  Username: {gen.username()}")
    print(f"  Phone: {gen.phone()}")
    print(f"  URL: {gen.url()}")
    print(f"  Address: {gen.address()}")
    print(f"  Company: {gen.company()}")
    print(f"  Buzzwords: {gen.buzzwords(4)}")
    
    print("\n" + "=" * 60)