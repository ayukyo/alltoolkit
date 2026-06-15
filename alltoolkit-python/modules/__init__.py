"""
AllToolkit - Python 全能工具箱
模块导出
"""

from .dev_metrics import (
    measure_cyclomatic_complexity,
    measure_cognitive_complexity,
    analyze_structure,
    calculate_quality_score,
    suggest_improvements,
    analyze_code,
    analyze_file,
    analyze_directory,
)

from .language_tools import (
    rotate_and_get_next,
    get_rotation_status,
    get_language_badge,
    get_all_badges,
    get_streak_info,
)

from .kata_generator import (
    generate_kata,
    preview_kata,
    list_katas_by_language,
    available_difficulties,
)

from .polyglot_codex import (
    rotate_and_get_codex,
    get_codex_preview,
    format_codex_markdown,
    format_codex_console,
)

from .polyglot_ink import (
    rotate_and_get_ink,
    get_ink_preview,
    format_ink_console,
    format_ink_markdown,
)

from .polyglot_snippet_vault import (
    get_snippet,
    search_snippets,
    get_vault_stats,
    get_supported_categories,
    format_snippet_console,
    format_snippet_markdown,
    SNIPPET_DB,
    CORE_LANGUAGES,
    CATEGORY_LABELS,
    Category,
)

from .polyglot_quiz import (
    generate_quiz,
    check_answer,
    get_quiz_stats,
    record_attempt,
    rotate_and_get_quiz,
    format_quiz_console,
    format_quiz_markdown,
    format_stats_console,
    QUIZ_DB,
    LANGUAGE_METADATA,
    CORE_LANGUAGES as QUIZ_CORE_LANGUAGES,
)

from .polyglot_cartographer import (
    generate_map,
    format_map_markdown,
    format_map_console,
    CARTOGRAPHER_DB,
)

__version__ = "1.4.0"
__all__ = [
    "measure_cyclomatic_complexity",
    "measure_cognitive_complexity",
    "analyze_structure",
    "calculate_quality_score",
    "suggest_improvements",
    "analyze_code",
    "analyze_file",
    "analyze_directory",
    "rotate_and_get_next",
    "get_rotation_status",
    "get_language_badge",
    "get_all_badges",
    "get_streak_info",
    "generate_kata",
    "preview_kata",
    "list_katas_by_language",
    "available_difficulties",
    "rotate_and_get_codex",
    "get_codex_preview",
    "format_codex_markdown",
    "format_codex_console",
    "rotate_and_get_ink",
    "get_ink_preview",
    "format_ink_console",
    "format_ink_markdown",
    "get_snippet",
    "search_snippets",
    "get_vault_stats",
    "get_supported_categories",
    "format_snippet_console",
    "format_snippet_markdown",
    "SNIPPET_DB",
    "CORE_LANGUAGES",
    "CATEGORY_LABELS",
    "Category",
    "generate_quiz",
    "check_answer",
    "get_quiz_stats",
    "record_attempt",
    "rotate_and_get_quiz",
    "format_quiz_console",
    "format_quiz_markdown",
    "format_stats_console",
    "QUIZ_DB",
    "LANGUAGE_METADATA",
    "generate_map",
    "format_map_markdown",
    "format_map_console",
    "CARTOGRAPHER_DB",
]