"""
Suffix Automaton Utils - A powerful O(n) data structure for string algorithms.

Suffix Automaton (also known as DAWG - Directed Acyclic Word Graph) is a minimal
finite automaton that recognizes all suffixes of a given string. It can be built
in O(n) time and has at most 2n-1 states.

Key capabilities:
- Find all occurrences of a pattern in O(m) time
- Count number of different substrings in O(n) preprocessing
- Find longest common substring between two strings in O(n+m)
- Find longest substring that appears at least k times
- Find lexicographically k-th substring

No external dependencies - pure Python implementation.
"""

from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict


class State:
    """Represents a state in the suffix automaton."""
    
    __slots__ = ['length', 'link', 'next', 'count', 'first_pos', 'is_cloned', 'reverse_links']
    
    def __init__(self, length: int = 0, link: int = -1):
        self.length: int = length  # Length of longest string in this state
        self.link: int = link      # Link to the state with longest proper suffix
        self.next: Dict[str, int] = {}  # Transitions to other states
        self.count: int = 0        # Number of occurrences of strings in this state
        self.first_pos: int = -1   # First occurrence position
        self.is_cloned: bool = False  # Whether this state was cloned
        self.reverse_links: List[int] = []  # States that link to this state


class SuffixAutomaton:
    """
    Suffix Automaton implementation for efficient string operations.
    
    A suffix automaton is a minimal DFA that accepts all suffixes of a given string.
    It can be built in linear time and provides efficient solutions to many string
    problems.
    
    Example:
        >>> sa = SuffixAutomaton("abacaba")
        >>> sa.count_occurrences("aba")
        2
        >>> sa.count_different_substrings()
        21
    """
    
    def __init__(self, text: str = ""):
        """Initialize and optionally build automaton for given text."""
        self.states: List[State] = [State(0, -1)]  # Initial state
        self.size: int = 1  # Number of states
        self.last: int = 0  # Last state (corresponding to whole string)
        self._text: str = ""
        
        if text:
            self.build(text)
    
    def build(self, text: str) -> None:
        """
        Build the suffix automaton for the given text.
        
        Time complexity: O(n) where n is the length of text.
        
        Args:
            text: The input string to build automaton for.
        """
        self._text = text
        self.states = [State(0, -1)]
        self.size = 1
        self.last = 0
        
        for i, char in enumerate(text):
            self._extend(char, i)
        
        self._compute_reverse_links()
        self._compute_occurrences()
    
    def _compute_reverse_links(self) -> None:
        """Compute reverse links for efficient occurrence position finding."""
        for v in range(self.size):
            self.states[v].reverse_links = []
        
        for v in range(1, self.size):
            link = self.states[v].link
            if link != -1:
                self.states[link].reverse_links.append(v)
    
    def _extend(self, char: str, pos: int) -> None:
        """Extend the automaton by adding a character."""
        # Create new state for the whole current string
        current = self.size
        self.states.append(State(self.states[self.last].length + 1, -1))
        self.states[current].first_pos = pos
        self.size += 1
        
        # Add transitions from states that can reach current via char
        p = self.last
        while p != -1 and char not in self.states[p].next:
            self.states[p].next[char] = current
            p = self.states[p].link
        
        if p == -1:
            # No state with transition via char, link to initial state
            self.states[current].link = 0
        else:
            q = self.states[p].next[char]
            if self.states[p].length + 1 == self.states[q].length:
                # q is the correct target state
                self.states[current].link = q
            else:
                # Need to clone q
                clone = self.size
                self.states.append(State(
                    self.states[p].length + 1,
                    self.states[q].link
                ))
                self.states[clone].next = self.states[q].next.copy()
                self.states[clone].first_pos = self.states[q].first_pos
                self.states[clone].is_cloned = True
                self.size += 1
                
                # Update links
                while p != -1 and self.states[p].next.get(char) == q:
                    self.states[p].next[char] = clone
                    p = self.states[p].link
                
                self.states[q].link = clone
                self.states[current].link = clone
        
        self.last = current
    
    def _compute_occurrences(self) -> None:
        """Compute occurrence counts for each state."""
        # Initialize counts: non-cloned states have count=1 (they correspond to one prefix)
        # Cloned states have count=0
        for state in self.states:
            state.count = 0 if state.is_cloned else 1
        
        # Get states sorted by length (descending)
        states_by_length = sorted(range(self.size), 
                                  key=lambda i: self.states[i].length, 
                                  reverse=True)
        
        # Propagate counts through suffix links
        for v in states_by_length:
            if self.states[v].link != -1:
                self.states[self.states[v].link].count += self.states[v].count
    
    def count_occurrences(self, pattern: str) -> int:
        """
        Count occurrences of pattern in the text.
        
        Time complexity: O(m) where m is pattern length.
        
        Args:
            pattern: The substring to search for.
            
        Returns:
            Number of occurrences of pattern in the text.
        """
        if not pattern:
            return len(self._text) + 1
        
        state = 0
        for char in pattern:
            if char not in self.states[state].next:
                return 0
            state = self.states[state].next[char]
        
        return self.states[state].count
    
    def find_all_occurrences(self, pattern: str) -> List[int]:
        """
        Find all starting positions of pattern in the text.
        
        Args:
            pattern: The substring to search for.
            
        Returns:
            List of starting positions where pattern occurs.
        """
        if not pattern:
            return list(range(len(self._text) + 1))
        
        state = 0
        for char in pattern:
            if char not in self.states[state].next:
                return []
            state = self.states[state].next[char]
        
        # Collect all end positions from this state and its reverse-link tree
        pattern_len = len(pattern)
        end_positions = []
        visited = set()
        
        def collect_end_positions(v: int):
            if v in visited:
                return
            visited.add(v)
            # Only non-cloned states have their own end positions
            if not self.states[v].is_cloned:
                end_positions.append(self.states[v].first_pos)
            # Visit all states that link to this state
            for child in self.states[v].reverse_links:
                collect_end_positions(child)
        
        collect_end_positions(state)
        
        # Convert end positions to start positions
        positions = [pos - pattern_len + 1 for pos in end_positions]
        return sorted(set(positions))
    
    def contains(self, pattern: str) -> bool:
        """
        Check if pattern exists in the text.
        
        Time complexity: O(m) where m is pattern length.
        
        Args:
            pattern: The substring to check.
            
        Returns:
            True if pattern is a substring of text.
        """
        state = 0
        for char in pattern:
            if char not in self.states[state].next:
                return False
            state = self.states[state].next[char]
        return True
    
    def longest_common_substring(self, other: str) -> Tuple[str, int]:
        """
        Find the longest common substring between this text and another string.
        
        Time complexity: O(m) where m is the length of other string.
        
        Args:
            other: The other string to compare with.
            
        Returns:
            Tuple of (substring, length).
        """
        if not other:
            return ("", 0)
        
        state = 0
        length = 0
        best_length = 0
        best_end_pos = 0
        
        for i, char in enumerate(other):
            if char in self.states[state].next:
                state = self.states[state].next[char]
                length += 1
            else:
                while state != -1 and char not in self.states[state].next:
                    state = self.states[state].link
                if state == -1:
                    state = 0
                    length = 0
                else:
                    length = self.states[state].length + 1
                    state = self.states[state].next[char]
            
            if length > best_length:
                best_length = length
                best_end_pos = i
        
        if best_length == 0:
            return ("", 0)
        
        return (other[best_end_pos - best_length + 1:best_end_pos + 1], best_length)
    
    def count_different_substrings(self) -> int:
        """
        Count the number of different substrings in the text.
        
        Time complexity: O(n) after construction.
        
        Returns:
            Number of unique substrings.
        """
        result = 0
        for v in range(1, self.size):
            result += self.states[v].length - self.states[self.states[v].link].length
        return result
    
    def longest_repeating_substring(self, min_occurrences: int = 2) -> Tuple[str, int]:
        """
        Find the longest substring that appears at least min_occurrences times.
        
        Args:
            min_occurrences: Minimum number of occurrences required.
            
        Returns:
            Tuple of (substring, length).
        """
        best_length = 0
        best_state = -1
        
        for v in range(1, self.size):
            if self.states[v].count >= min_occurrences:
                if self.states[v].length > best_length:
                    best_length = self.states[v].length
                    best_state = v
        
        if best_state == -1:
            return ("", 0)
        
        # Extract the substring from the text
        start = self.states[best_state].first_pos - best_length + 1
        return (self._text[start:self.states[best_state].first_pos + 1], best_length)
    
    def kth_different_substring(self, k: int) -> str:
        """
        Find the k-th lexicographically smallest different substring.
        
        Args:
            k: The index (1-based) of substring to find.
            
        Returns:
            The k-th different substring.
        """
        total = self.count_different_substrings()
        if k <= 0 or k > total:
            return ""
        
        # DP to count number of substrings starting from each state
        dp = [0] * self.size
        
        def compute_dp(v: int) -> int:
            if dp[v] != 0 or len(self.states[v].next) == 0:
                return dp[v]
            result = 0
            for char in self.states[v].next.keys():
                next_state = self.states[v].next[char]
                result += 1 + compute_dp(next_state)  # 1 for the single char + extensions
            dp[v] = result
            return result
        
        compute_dp(0)
        
        # Find k-th substring
        state = 0
        result = []
        
        while k > 0:
            for char in sorted(self.states[state].next.keys()):
                next_state = self.states[state].next[char]
                count = 1 + dp[next_state]  # this char + all extensions
                if k <= count:
                    result.append(char)
                    state = next_state
                    k -= 1  # subtract the single char
                    break
                else:
                    k -= count
        
        return ''.join(result)
    
    def all_substrings_of_length(self, length: int) -> Set[str]:
        """
        Get all unique substrings of a specific length.
        
        Args:
            length: The desired substring length.
            
        Returns:
            Set of all unique substrings of given length.
        """
        if length <= 0:
            return {""}
        
        result = set()
        
        # BFS through states, tracking current path
        def dfs(v: int, current: str, depth: int):
            if depth == length:
                result.add(current)
                return
            for char, next_state in self.states[v].next.items():
                dfs(next_state, current + char, depth + 1)
        
        dfs(0, "", 0)
        return result
    
    def shortest_unique_substring(self, start_pos: int) -> str:
        """
        Find the shortest substring starting at start_pos that occurs only once.
        
        Args:
            start_pos: The starting position in the text.
            
        Returns:
            The shortest unique substring starting at that position.
        """
        if start_pos < 0 or start_pos >= len(self._text):
            return ""
        
        state = 0
        for i in range(start_pos, len(self._text)):
            char = self._text[i]
            state = self.states[state].next[char]
            if self.states[state].count == 1:
                return self._text[start_pos:i + 1]
        
        return self._text[start_pos:]
    
    def is_substring(self, pattern: str) -> bool:
        """Alias for contains() - check if pattern is a substring."""
        return self.contains(pattern)
    
    def get_info(self) -> Dict:
        """
        Get information about the automaton.
        
        Returns:
            Dictionary with automaton statistics.
        """
        return {
            "text_length": len(self._text),
            "num_states": self.size,
            "num_transitions": sum(len(s.next) for s in self.states),
            "num_different_substrings": self.count_different_substrings(),
            "longest_repeating_substring": self.longest_repeating_substring()[0],
        }
    
    def traverse(self, pattern: str) -> Optional[int]:
        """
        Traverse the automaton following pattern and return final state.
        
        Args:
            pattern: String to traverse with.
            
        Returns:
            Final state index, or None if pattern not found.
        """
        state = 0
        for char in pattern:
            if char not in self.states[state].next:
                return None
            state = self.states[state].next[char]
        return state
    
    def get_state_info(self, state_idx: int) -> Dict:
        """
        Get information about a specific state.
        
        Args:
            state_idx: Index of the state.
            
        Returns:
            Dictionary with state information.
        """
        if state_idx < 0 or state_idx >= self.size:
            return {}
        
        state = self.states[state_idx]
        return {
            "length": state.length,
            "link": state.link,
            "transitions": state.next.copy(),
            "count": state.count,
            "first_pos": state.first_pos,
            "is_cloned": state.is_cloned,
        }


def build_suffix_automaton(text: str) -> SuffixAutomaton:
    """
    Build a suffix automaton for the given text.
    
    Args:
        text: Input string.
        
    Returns:
        SuffixAutomaton instance.
    """
    return SuffixAutomaton(text)


def count_occurrences(text: str, pattern: str) -> int:
    """
    Count occurrences of pattern in text using suffix automaton.
    
    Args:
        text: The text to search in.
        pattern: The pattern to search for.
        
    Returns:
        Number of occurrences.
    """
    sa = SuffixAutomaton(text)
    return sa.count_occurrences(pattern)


def find_all_occurrences(text: str, pattern: str) -> List[int]:
    """
    Find all occurrences of pattern in text.
    
    Args:
        text: The text to search in.
        pattern: The pattern to search for.
        
    Returns:
        List of starting positions.
    """
    sa = SuffixAutomaton(text)
    return sa.find_all_occurrences(pattern)


def longest_common_substring(text1: str, text2: str) -> str:
    """
    Find the longest common substring between two strings.
    
    Args:
        text1: First string.
        text2: Second string.
        
    Returns:
        The longest common substring.
    """
    sa = SuffixAutomaton(text1)
    result, _ = sa.longest_common_substring(text2)
    return result


def count_different_substrings(text: str) -> int:
    """
    Count the number of different substrings in text.
    
    Args:
        text: Input string.
        
    Returns:
        Number of unique substrings.
    """
    sa = SuffixAutomaton(text)
    return sa.count_different_substrings()


def longest_repeating_substring(text: str, min_occurrences: int = 2) -> str:
    """
    Find the longest substring that appears at least min_occurrences times.
    
    Args:
        text: Input string.
        min_occurrences: Minimum occurrences required.
        
    Returns:
        The longest repeating substring.
    """
    sa = SuffixAutomaton(text)
    result, _ = sa.longest_repeating_substring(min_occurrences)
    return result


def kth_different_substring(text: str, k: int) -> str:
    """
    Find the k-th lexicographically smallest different substring.
    
    Args:
        text: Input string.
        k: Index (1-based) of substring to find.
        
    Returns:
        The k-th different substring.
    """
    sa = SuffixAutomaton(text)
    return sa.kth_different_substring(k)


def shortest_unique_substring(text: str, start_pos: int = 0) -> str:
    """
    Find the shortest substring starting at start_pos that occurs only once.
    
    Args:
        text: Input string.
        start_pos: Starting position (default 0).
        
    Returns:
        The shortest unique substring.
    """
    sa = SuffixAutomaton(text)
    return sa.shortest_unique_substring(start_pos)


# Additional utility functions

def is_palindrome_substring(text: str, start: int, end: int) -> bool:
    """Check if substring text[start:end] is a palindrome."""
    substring = text[start:end]
    return substring == substring[::-1]


def find_all_palindrome_substrings(text: str) -> List[str]:
    """
    Find all palindrome substrings in text.
    Uses suffix automaton to efficiently enumerate substrings,
    then checks for palindromes.
    
    Args:
        text: Input string.
        
    Returns:
        List of palindrome substrings.
    """
    sa = SuffixAutomaton(text)
    palindromes = set()
    
    # Enumerate all substrings by traversing automaton
    def dfs(v: int, current: str):
        if current and current == current[::-1]:
            palindromes.add(current)
        for char, next_state in self.states[v].next.items():
            dfs(next_state, current + char)
    
    # Use the text to find palindromes more efficiently
    for i in range(len(text)):
        # Odd length palindromes
        for j in range(min(i + 1, len(text) - i)):
            substring = text[i - j:i + j + 1]
            if substring == substring[::-1]:
                palindromes.add(substring)
            else:
                break
        
        # Even length palindromes
        for j in range(min(i + 1, len(text) - i - 1)):
            substring = text[i - j:i + j + 2]
            if substring == substring[::-1]:
                palindromes.add(substring)
            else:
                break
    
    return sorted(palindromes, key=len)


class MultiSuffixAutomaton:
    """
    Suffix Automaton for multiple strings.
    Useful for finding patterns that exist in multiple texts.
    """
    
    def __init__(self):
        self.automata: List[SuffixAutomaton] = []
        self._texts: List[str] = []
    
    def add_text(self, text: str) -> None:
        """Add a text to the collection."""
        self.automata.append(SuffixAutomaton(text))
        self._texts.append(text)
    
    def common_substring_in_all(self) -> str:
        """
        Find substring that appears in all texts.
        
        Returns:
            Longest substring common to all texts, or empty string.
        """
        if len(self.automata) < 2:
            return self._texts[0] if self._texts else ""
        
        # Find LCS between all pairs, take shortest
        candidates = []
        
        # Get all substrings from first text
        sa0 = self.automata[0]
        for i in range(len(self._texts[0])):
            for j in range(i + 1, len(self._texts[0]) + 1):
                substring = self._texts[0][i:j]
                if all(sa.contains(substring) for sa in self.automata[1:]):
                    candidates.append(substring)
        
        if not candidates:
            return ""
        
        return max(candidates, key=len)
    
    def pattern_in_texts(self, pattern: str) -> List[int]:
        """
        Find which texts contain the pattern.
        
        Args:
            pattern: Pattern to search for.
            
        Returns:
            List of indices of texts containing pattern.
        """
        return [i for i, sa in enumerate(self.automata) if sa.contains(pattern)]


if __name__ == "__main__":
    # Demo
    text = "abacaba"
    sa = SuffixAutomaton(text)
    
    print(f"Text: {text}")
    print(f"Number of states: {sa.size}")
    print(f"Different substrings: {sa.count_different_substrings()}")
    print(f"'aba' occurrences: {sa.count_occurrences('aba')}")
    print(f"'aba' positions: {sa.find_all_occurrences('aba')}")
    print(f"Longest repeating substring: {sa.longest_repeating_substring()}")
    
    other = "baca"
    lcs, length = sa.longest_common_substring(other)
    print(f"LCS with '{other}': '{lcs}' (length {length})")