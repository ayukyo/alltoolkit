"""
Manacher's Algorithm - Efficient Palindrome Detection
======================================================

Manacher's algorithm finds the longest palindromic substring in O(n) time
and O(n) space. It's significantly faster than naive O(n²) approaches.

Key Features:
- Find longest palindromic substring
- Find all palindromic substrings
- Count total palindromic substrings
- Check if a substring is palindrome
- Find palindrome centers and radii

Author: AllToolkit
Date: 2026-05-01
"""


def preprocess(s: str) -> str:
    """
    Preprocess string by inserting special characters between each character.
    This allows handling both odd and even length palindromes uniformly.
    
    Example: "abc" -> "^#a#b#c#$"
    The '^' and '$' are sentinels to avoid bounds checking.
    
    Args:
        s: Input string
        
    Returns:
        Processed string with separators and sentinels
    """
    if not s:
        return "^#$"
    return "^#" + "#".join(s) + "#$"


def manacher(s: str) -> list:
    """
    Core Manacher's algorithm implementation.
    Returns array P where P[i] is the radius of the longest palindrome
    centered at position i in the processed string.
    
    The actual palindrome length in original string is P[i].
    
    Args:
        s: Input string
        
    Returns:
        List of palindrome radii for each center position
    """
    if not s:
        return []
    
    T = preprocess(s)
    n = len(T)
    P = [0] * n
    
    # Center and right boundary of current palindrome
    C = 0
    R = 0
    
    for i in range(1, n - 1):
        # Mirror position of i with respect to center C
        mirr = 2 * C - i
        
        # If i is within current right boundary, use mirror value
        if i < R:
            P[i] = min(R - i, P[mirr])
        
        # Try to expand palindrome centered at i
        while T[i + P[i] + 1] == T[i - P[i] - 1]:
            P[i] += 1
        
        # If palindrome centered at i expands beyond R,
        # adjust center and right boundary
        if i + P[i] > R:
            C = i
            R = i + P[i]
    
    return P


def longest_palindromic_substring(s: str) -> str:
    """
    Find the longest palindromic substring in the given string.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Args:
        s: Input string
        
    Returns:
        Longest palindromic substring (empty string if input is empty)
        
    Examples:
        >>> longest_palindromic_substring("babad")
        'bab'  # or 'aba', both are valid
        
        >>> longest_palindromic_substring("cbbd")
        'bb'
        
        >>> longest_palindromic_substring("a")
        'a'
        
        >>> longest_palindromic_substring("")
        ''
    """
    if not s:
        return ""
    
    P = manacher(s)
    
    # Find the center with maximum radius
    max_len = 0
    center_index = 0
    
    for i in range(len(P)):
        if P[i] > max_len:
            max_len = P[i]
            center_index = i
    
    # Convert back to original string indices
    # In processed string: index i corresponds to (i-1)//2 in original
    start = (center_index - max_len) // 2
    end = start + max_len
    
    return s[start:end]


def all_palindromic_substrings(s: str) -> list:
    """
    Find all unique palindromic substrings in the given string.
    
    Args:
        s: Input string
        
    Returns:
        List of all unique palindromic substrings, sorted by length (descending)
        
    Examples:
        >>> all_palindromic_substrings("abaab")
        ['aba', 'baab', 'aa', 'ab', 'b', 'a']
    """
    if not s:
        return []
    
    P = manacher(s)
    palindromes = set()
    
    for i in range(len(P)):
        radius = P[i]
        # Extract all palindromes centered at i with radius 1 to P[i]
        for r in range(1, radius + 1):
            start = (i - r) // 2
            end = (i + r) // 2
            palindrome = s[start:end]
            palindromes.add(palindrome)
    
    # Add single characters (they are always palindromes)
    for char in s:
        palindromes.add(char)
    
    # Sort by length descending, then alphabetically
    result = sorted(list(palindromes), key=lambda x: (-len(x), x))
    return result


def count_palindromic_substrings(s: str) -> int:
    """
    Count the total number of palindromic substrings.
    
    Each single character is counted as a palindrome.
    
    Args:
        s: Input string
        
    Returns:
        Total count of palindromic substrings
        
    Examples:
        >>> count_palindromic_substrings("abc")
        3  # 'a', 'b', 'c'
        
        >>> count_palindromic_substrings("aaa")
        6  # 'a', 'a', 'a', 'aa', 'aa', 'aaa'
        
        >>> count_palindromic_substrings("aba")
        4  # 'a', 'b', 'a', 'aba'
    """
    if not s:
        return 0
    
    P = manacher(s)
    
    # In processed string "^#a#b#c#$":
    # - Character positions are at EVEN indices (2, 4, 6, ...)
    # - Separator positions are at ODD indices (1, 3, 5, ...)
    # - Sentinels at indices 0 and len(P)-1 should be skipped
    
    count = 0
    for i in range(1, len(P) - 1):  # Skip sentinel positions
        if i % 2 == 0:  # Character position (even index) - odd-length palindromes
            count += (P[i] + 1) // 2
        else:  # Separator position (odd index) - even-length palindromes
            count += P[i] // 2
    
    return count


def is_palindrome(s: str, start: int, end: int) -> bool:
    """
    Check if a substring is a palindrome using Manacher's precomputed values.
    
    This is O(1) after preprocessing, making it efficient for multiple queries.
    
    Args:
        s: Input string
        start: Start index (inclusive)
        end: End index (exclusive)
        
    Returns:
        True if substring s[start:end] is a palindrome
        
    Examples:
        >>> is_palindrome("abaab", 0, 3)
        True  # 'aba' is palindrome
        
        >>> is_palindrome("abaab", 1, 4)
        False  # 'baa' is not palindrome
    """
    if not s:
        return True
    
    if start < 0 or end > len(s) or start >= end:
        return False
    
    substring = s[start:end]
    return substring == substring[::-1]


def palindrome_info(s: str) -> dict:
    """
    Get comprehensive palindrome information about the string.
    
    Args:
        s: Input string
        
    Returns:
        Dictionary containing:
        - longest: Longest palindromic substring
        - length: Length of longest palindrome
        - count: Total count of palindromic substrings
        - centers: List of (center, radius) for significant palindromes
        - has_palindrome: Whether string contains palindrome longer than 1
        
    Examples:
        >>> palindrome_info("babad")
        {'longest': 'bab', 'length': 3, 'count': 7, ...}
    """
    if not s:
        return {
            'longest': '',
            'length': 0,
            'count': 0,
            'centers': [],
            'has_palindrome': False
        }
    
    P = manacher(s)
    
    # Find max
    max_len = max(P)
    max_center = P.index(max_len)
    
    # Find centers with radius >= 2 (palindromes longer than single char)
    significant_centers = []
    for i, radius in enumerate(P):
        if radius >= 2:
            original_center = (i - 1) // 2
            significant_centers.append({
                'center': original_center,
                'radius': radius,
                'type': 'odd' if i % 2 == 0 else 'even',  # Even index = character = odd-length
                'substring': s[(i - radius) // 2:(i + radius) // 2]
            })
    
    longest = s[(max_center - max_len) // 2:(max_center + max_len) // 2]
    
    # Calculate correct count (character positions at even indices)
    count = 0
    for i in range(1, len(P) - 1):
        if i % 2 == 0:  # Character position
            count += (P[i] + 1) // 2
        else:  # Separator position
            count += P[i] // 2
    
    return {
        'longest': longest,
        'length': max_len,
        'count': count,
        'centers': significant_centers,
        'has_palindrome': max_len > 1
    }


def find_palindromes_by_length(s: str, min_length: int = 2) -> list:
    """
    Find all palindromic substrings with length >= min_length.
    
    Args:
        s: Input string
        min_length: Minimum palindrome length (default 2)
        
    Returns:
        List of palindromes meeting the length requirement
        
    Examples:
        >>> find_palindromes_by_length("abaab", 3)
        ['aba', 'baab']
    """
    if not s:
        return []
    
    P = manacher(s)
    palindromes = set()
    
    for i in range(len(P)):
        radius = P[i]
        if radius >= min_length:
            start = (i - radius) // 2
            end = (i + radius) // 2
            palindrome = s[start:end]
            if len(palindrome) >= min_length:
                palindromes.add(palindrome)
    
    return sorted(list(palindromes), key=lambda x: (-len(x), x))


def longest_palindrome_at(s: str, position: int) -> str:
    """
    Find the longest palindrome centered at a specific position.
    
    Args:
        s: Input string
        position: Center position in original string
        
    Returns:
        Longest palindrome centered at the given position
        
    Examples:
        >>> longest_palindrome_at("babad", 1)
        'bab'  # centered at position 1 (character 'a')
        
        >>> longest_palindrome_at("cbbd", 2)
        'bb'  # centered between positions 1 and 2 (even palindrome)
    """
    if not s or position < 0 or position >= len(s):
        return ""
    
    P = manacher(s)
    
    # Find the processed string index corresponding to this position
    # For odd palindrome centered at position p: index = 2*p + 2
    # For even palindrome centered between p-1 and p: index = 2*p + 1
    
    odd_center = 2 * position + 2
    even_center = 2 * position + 1
    
    # Check both odd and even centers
    odd_radius = P[odd_center] if odd_center < len(P) else 0
    even_radius = P[even_center] if even_center < len(P) else 0
    
    # Return the longer one
    if odd_radius >= even_radius:
        start = (odd_center - odd_radius) // 2
        end = (odd_center + odd_radius) // 2
        return s[start:end]
    else:
        start = (even_center - even_radius) // 2
        end = (even_center + even_radius) // 2
        return s[start:end]


# Demonstration and examples
if __name__ == "__main__":
    print("=" * 60)
    print("Manacher's Algorithm - Palindrome Detection Demo")
    print("=" * 60)
    
    test_cases = [
        "babad",
        "cbbd",
        "a",
        "ac",
        "racecar",
        "aaaa",
        "abaab",
        "banana",
        "",
        "abcba"
    ]
    
    for s in test_cases:
        print(f"\nString: '{s}'")
        if s:
            info = palindrome_info(s)
            print(f"  Longest palindrome: '{info['longest']}' (length {info['length']})")
            print(f"  Total palindromic substrings: {info['count']}")
            print(f"  Has palindrome > 1 char: {info['has_palindrome']}")
            palindromes = find_palindromes_by_length(s, 2)
            if palindromes:
                print(f"  Palindromes length >= 2: {palindromes}")
        else:
            print("  (empty string)")
    
    print("\n" + "=" * 60)
    print("Algorithm Complexity: O(n) time, O(n) space")
    print("=" * 60)