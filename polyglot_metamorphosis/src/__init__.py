"""Polyglot Metamorphosis — AST-aware code transformation across languages."""

from .metamorphosis import (
    LANGUAGE_CYCLE,
    LANGUAGE_TRAITS,
    advance_rotation,
    detect_language,
    extract_code_concepts,
    generate_metamorphic_mapping,
    get_current_language,
    load_rotation_config,
    save_rotation_config,
    transform_example,
)

__all__ = [
    "LANGUAGE_CYCLE",
    "LANGUAGE_TRAITS",
    "advance_rotation",
    "detect_language",
    "extract_code_concepts",
    "generate_metamorphic_mapping",
    "get_current_language",
    "load_rotation_config",
    "save_rotation_config",
    "transform_example",
]
