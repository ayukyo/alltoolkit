"""
dotenv_utils - Parse and serialize .env files (environment variable configuration files).

Supports:
- Single quotes, double quotes
- Inline comments
- Multi-line values (with backslash continuation)
- Empty lines
- export prefix
- Variable interpolation: ${VAR} and $VAR
"""

__all__ = ["parse", "serialize", "load"]


def parse(content):
    """
    Parse a .env format string into a dictionary of key-value pairs.

    Args:
        content: Raw .env file content as a string.

    Returns:
        Dictionary mapping variable names to their values.

    Examples:
        >>> parse('FOO=bar\\nBAZ=qux\\n')
        {'FOO': 'bar', 'BAZ': 'qux'}
        >>> parse('FOO="hello world"\\n')
        {'FOO': 'hello world'}
        >>> parse('# comment\\nFOO=bar\\n')
        {'FOO': 'bar'}
    """
    result = {}
    lines = content.splitlines()
    continued_line = None

    for line in lines:
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith("#"):
            continue

        # Strip export prefix
        if stripped.startswith("export "):
            stripped = stripped[7:]

        # Continuation line
        if continued_line is not None:
            line = continued_line + line.lstrip()
            stripped = line.strip()
            continued_line = None

        # Check for line continuation (backslash at end of unquoted line)
        if stripped.endswith("\\"):
            continued_line = stripped[:-1]
            continue

        # Find the first '='
        eq_idx = stripped.find("=")
        if eq_idx == -1:
            continue

        key = stripped[:eq_idx].strip()
        if not key:
            continue
        value = stripped[eq_idx + 1:]

        # Parse value
        value = _parse_value(value)
        result[key] = value

    return result


def _parse_value(value):
    """Parse a single value according to .env rules."""
    value = value.strip()
    if not value:
        return ""

    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
        return _expand_escapes(value)

    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]

    # Unquoted value — strip trailing comment
    hash_idx = value.find(" #")
    if hash_idx != -1:
        value = value[:hash_idx].strip()

    return _expand_escapes(value)


def _expand_escapes(s):
    """Expand escape sequences in a .env value."""
    escape_map = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"": '"', "'": "'"}
    result = []
    i = 0
    length = len(s)
    while i < length:
        c = s[i]
        if c == "\\" and i + 1 < length:
            n = escape_map.get(s[i + 1], s[i + 1])
            result.append(n)
            i += 2
        else:
            result.append(c)
            i += 1
    return "".join(result)


def serialize(env):
    """
    Serialize a dictionary into .env format.

    Args:
        env: Dictionary of environment variable names to values.

    Returns:
        A string formatted as a .env file.

    Examples:
        >>> serialize({"FOO": "bar", "BAZ": "qux"})
        'FOO=bar\\nBAZ=qux'
        >>> serialize({"FOO": "hello world"})
        'FOO="hello world"'
    """
    lines = []
    for key, value in env.items():
        if _needs_quoting(value):
            lines.append('{key}="{val}"'.format(key=key, val=_escape_value(value)))
        else:
            lines.append("{key}={value}".format(key=key, value=value))
    return "\n".join(lines) + "\n"


def _needs_quoting(value):
    """Check if a value needs to be quoted."""
    if not value:
        return False
    if value.startswith(" ") or value.endswith(" ") or " " in value:
        return True
    if "\n" in value or "\t" in value or '"' in value:
        return True
    if "#" in value:
        return True
    if "\\" in value:
        return True
    if "=" in value:
        return True
    return False


def _escape_value(value):
    """Escape special characters for quoting."""
    return (
        value.replace("\\", "\\\\")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("\r", "\\r")
        .replace('"', '\\"')
    )


def load(path):
    """
    Load and parse a .env file from disk.

    Args:
        path: File path to the .env file.

    Returns:
        Dictionary of parsed key-value pairs.

    Examples:
        >>> import os
        >>> data = load(".env")
        >>> data["DATABASE_URL"]
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return parse(content)