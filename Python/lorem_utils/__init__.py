"""
Lorem Ipsum Generator Module
=============================

A zero-dependency Lorem Ipsum text generator for creating placeholder content.
"""

from .lorem_utils import (
    LoremGenerator,
    words, sentence, sentences, paragraph, paragraphs,
    title, headline, html_paragraphs, list_items,
    buzzword, buzzwords, email, username, url, phone,
    address, name, company, generate,
    LOREM_WORDS, EXTENDED_WORDS
)

__all__ = [
    'LoremGenerator',
    'words', 'sentence', 'sentences', 'paragraph', 'paragraphs',
    'title', 'headline', 'html_paragraphs', 'list_items',
    'buzzword', 'buzzwords', 'email', 'username', 'url', 'phone',
    'address', 'name', 'company', 'generate',
    'LOREM_WORDS', 'EXTENDED_WORDS'
]

__version__ = '1.0.0'