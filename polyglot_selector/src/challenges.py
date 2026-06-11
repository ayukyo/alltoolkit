"""Challenge generator for each programming language."""

import random
from typing import NamedTuple, Dict, List, Tuple


LANGUAGE_FEATURES: Dict[str, List[str]] = {
    "Rust": ["ownership", "borrowing", "lifetimes", "pattern_matching", "macros"],
    "Go": ["goroutines", "channels", "defer", "interfaces", "slices"],
    "Swift": ["optionals", "protocols", "closures", "generics", "async/await"],
    "Kotlin": ["coroutines", "extensions", "null_safety", "data classes", "sealed classes"],
    "TypeScript": ["generics", "decorators", "mapped types", "infer", "utility types"],
    "JavaScript": ["closures", "prototypes", "async", "destructuring", "modules"],
    "Java": ["generics", "streams", "annotations", "interfaces", "concurrency"],
    "C/C++": ["pointers", "templates", "memory management", "STL", "move semantics"],
}

CHALLENGE_TYPES: List[Tuple[str, str]] = [
    ("algorithm", "用 {lang} 实现一个 {feature} 相关的算法题"),
    ("system", "用 {lang} 编写一个展示 {feature} 的系统程序"),
    ("web", "用 {lang} 创建一个利用 {feature} 的 Web 应用"),
    ("concurrency", "用 {lang} 展示 {feature} 的并发模式"),
    ("idiomatic", "用 {lang} 惯用法实现 {feature} 的最佳实践"),
]


class Challenge(NamedTuple):
    """Represents a generated programming challenge."""
    language: str
    challenge_type: str
    feature: str
    description: str


def generate_challenge(language: str, seed: int = None) -> Challenge:
    """Generate a random challenge for the given language.

    Args:
        language: Programming language name.
        seed: Optional random seed for reproducibility in tests.

    Returns:
        A Challenge namedtuple with language, type, feature, and description.
    """
    if seed is not None:
        rng = random.Random(seed)
    else:
        rng = random.Random()

    if language not in LANGUAGE_FEATURES:
        raise ValueError("Unsupported language: {}".format(language))

    features = LANGUAGE_FEATURES[language]
    feature = rng.choice(features)
    template, typ = rng.choice(CHALLENGE_TYPES)

    typ, template = rng.choice(CHALLENGE_TYPES)
    description = template.format(lang=language, feature=feature)
    return Challenge(language=language, challenge_type=typ, feature=feature, description=description)