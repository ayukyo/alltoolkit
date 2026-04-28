"""
Name Generator Utils - Random name generation utilities.

Provides generators for random names including:
- First names (male/female/unisex)
- Last names
- Full names
- Fantasy names
- Username generation
- Code names/codename generation

Compatible with Python 3.6+.
Zero external dependencies.
"""

from .generator import (
    NameGenerator,
    generate_first_name,
    generate_last_name,
    generate_full_name,
    generate_username,
    generate_codename,
    generate_fantasy_name,
    generate_company_name,
    generate_pet_name,
)

__all__ = [
    'NameGenerator',
    'generate_first_name',
    'generate_last_name',
    'generate_full_name',
    'generate_username',
    'generate_codename',
    'generate_fantasy_name',
    'generate_company_name',
    'generate_pet_name',
]

__version__ = '1.0.0'