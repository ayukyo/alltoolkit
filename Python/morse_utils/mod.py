"""
Morse Code Encoder/Decoder Utility Module

A comprehensive morse code toolkit with zero external dependencies.
Supports encoding text to morse code and decoding morse code back to text.

Features:
- Text to Morse code encoding
- Morse code to text decoding
- Audio generation (simple beep patterns)
- Multiple output formats (dots/dashes, visual representation)
- Support for letters, numbers, and common punctuation
- Prosign support (special morse code sequences)
"""

# International Morse Code mapping
MORSE_CODE = {
    # Letters
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    # Numbers
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    # Punctuation
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
    '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-', '@': '.--.-.',
}

# Reverse mapping for decoding
MORSE_TO_CHAR = {v: k for k, v in MORSE_CODE.items()}

# Prosigns (procedure signals) - commonly used in amateur radio
PROSIGNS = {
    'AA': '.-.-',      # End of message
    'AR': '.-.-.',     # End of transmission
    'AS': '.-...',     # Wait
    'BT': '-...-',     # Break/pause
    'BK': '-...-.',    # Break (invitation to transmit)
    'CL': '-.-..',     # Closing station
    'CT': '-.-.-',     # Start copying
    'DO': '-..---',    # Change to next frequency
    'KN': '-.--.',     # Invite named station to transmit
    'SK': '...-.-',    # End of work (silent key)
    'SN': '...-.',     # Understood
    'VA': '...-.-',    # Same as SK
}

REVERSE_PROSIGNS = {v: k for k, v in PROSIGNS.items()}


class MorseEncoder:
    """Encode text to Morse code."""
    
    def __init__(self, dot_symbol: str = '.', dash_symbol: str = '-',
                 char_separator: str = ' ', word_separator: str = ' / '):
        """
        Initialize encoder with custom symbols.
        
        Args:
            dot_symbol: Symbol to use for dots (default: '.')
            dash_symbol: Symbol to use for dashes (default: '-')
            char_separator: Separator between characters (default: ' ')
            word_separator: Separator between words (default: ' / ')
        """
        self.dot_symbol = dot_symbol
        self.dash_symbol = dash_symbol
        self.char_separator = char_separator
        self.word_separator = word_separator
        self._symbol_map = {'.': dot_symbol, '-': dash_symbol}
    
    def encode_char(self, char: str) -> str:
        """Encode a single character to Morse code."""
        char = char.upper()
        if char in MORSE_CODE:
            morse = MORSE_CODE[char]
            return ''.join(self._symbol_map.get(c, c) for c in morse)
        elif char == ' ':
            return ''  # Handled by word separator
        else:
            return ''  # Unknown characters are skipped
    
    def encode(self, text: str) -> str:
        """
        Encode text to Morse code.
        
        Args:
            text: The text to encode
            
        Returns:
            Morse code string
        """
        if not text:
            return ''
        
        result = []
        words = text.split(' ')
        
        for i, word in enumerate(words):
            if not word:
                continue
            
            encoded_chars = []
            for char in word:
                encoded = self.encode_char(char)
                if encoded:
                    encoded_chars.append(encoded)
            
            if encoded_chars:
                result.append(self.char_separator.join(encoded_chars))
        
        return self.word_separator.join(result)
    
    def encode_prosign(self, prosign: str) -> str:
        """Encode a prosign abbreviation."""
        prosign = prosign.upper()
        if prosign in PROSIGNS:
            morse = PROSIGNS[prosign]
            return ''.join(self._symbol_map.get(c, c) for c in morse)
        return ''


class MorseDecoder:
    """Decode Morse code to text."""
    
    def __init__(self, dot_symbol: str = '.', dash_symbol: str = '-',
                 char_separator: str = ' ', word_separator: str = '/'):
        """
        Initialize decoder with custom symbols.
        
        Args:
            dot_symbol: Symbol used for dots (default: '.')
            dash_symbol: Symbol used for dashes (default: '-')
            char_separator: Separator between characters (default: ' ')
            word_separator: Separator between words (default: '/')
        """
        self.dot_symbol = dot_symbol
        self.dash_symbol = dash_symbol
        self.char_separator = char_separator
        self.word_separator = word_separator
        self._reverse_symbol_map = {dot_symbol: '.', dash_symbol: '-'}
    
    def normalize_morse(self, morse: str) -> str:
        """Convert custom symbols to standard dots and dashes."""
        return ''.join(self._reverse_symbol_map.get(c, c) for c in morse)
    
    def decode_char(self, morse: str) -> str:
        """Decode a single Morse code sequence to character."""
        normalized = self.normalize_morse(morse)
        
        if normalized in MORSE_TO_CHAR:
            return MORSE_TO_CHAR[normalized]
        elif normalized in REVERSE_PROSIGNS:
            return f'<{REVERSE_PROSIGNS[normalized]}>'
        else:
            return '?'  # Unknown morse sequence
    
    def decode(self, morse: str) -> str:
        """
        Decode Morse code to text.
        
        Args:
            morse: The Morse code string to decode
            
        Returns:
            Decoded text string
        """
        if not morse:
            return ''
        
        # Normalize the word separator (handle ' / ' as well as '/')
        morse = morse.strip()
        # Replace ' / ' with '/' for consistent handling
        morse = morse.replace(' / ', '/').replace(' /', '/').replace('/ ', '/')
        
        # Split by word separator
        words = morse.split(self.word_separator)
        result = []
        
        for word in words:
            if not word:
                continue
            
            # Split by character separator (default is space)
            chars = word.split(self.char_separator) if self.char_separator else [word]
            decoded_chars = [self.decode_char(c.strip()) for c in chars if c.strip()]
            if decoded_chars:
                result.append(''.join(decoded_chars))
        
        return ' '.join(result)


def encode(text: str, dot: str = '.', dash: str = '-') -> str:
    """
    Quick encode text to Morse code.
    
    Args:
        text: Text to encode
        dot: Symbol for dots
        dash: Symbol for dashes
        
    Returns:
        Morse code string
    """
    encoder = MorseEncoder(dot_symbol=dot, dash_symbol=dash)
    return encoder.encode(text)


def decode(morse: str, dot: str = '.', dash: str = '-') -> str:
    """
    Quick decode Morse code to text.
    
    Args:
        morse: Morse code to decode
        dot: Symbol used for dots
        dash: Symbol used for dashes
        
    Returns:
        Decoded text string
    """
    decoder = MorseDecoder(dot_symbol=dot, dash_symbol=dash)
    return decoder.decode(morse)


def is_morse(text: str) -> bool:
    """
    Check if a string appears to be Morse code.
    
    Args:
        text: String to check
        
    Returns:
        True if the string appears to be Morse code
    """
    # Morse code typically contains only dots, dashes, spaces, and slashes
    morse_chars = set('.-_/ ')
    return all(c in morse_chars for c in text.strip())


def calculate_speed(wpm: int = 15) -> dict:
    """
    Calculate Morse code timing based on words per minute.
    
    Standard timing (PARIS method):
    - Dot duration = 1 unit
    - Dash duration = 3 units
    - Space between elements = 1 unit
    - Space between characters = 3 units
    - Space between words = 7 units
    
    Args:
        wpm: Words per minute (standard word is "PARIS" = 50 units)
        
    Returns:
        Dictionary with timing values in milliseconds
    """
    # PARIS is 50 time units, so wpm = 60s / (50 * unit_time)
    unit_ms = 1200 / wpm  # milliseconds per unit
    
    return {
        'wpm': wpm,
        'unit_ms': unit_ms,
        'dot_ms': unit_ms,
        'dash_ms': unit_ms * 3,
        'element_gap_ms': unit_ms,
        'char_gap_ms': unit_ms * 3,
        'word_gap_ms': unit_ms * 7,
    }


def get_timing_sequence(text: str, wpm: int = 15) -> list:
    """
    Generate a timing sequence for playing Morse code.
    
    Args:
        text: Text to encode
        wpm: Words per minute
        
    Returns:
        List of tuples: (is_tone, duration_ms)
    """
    timing = calculate_speed(wpm)
    encoder = MorseEncoder()
    sequence = []
    
    words = text.upper().split(' ')
    
    for word_idx, word in enumerate(words):
        if not word:
            continue
        
        for char_idx, char in enumerate(word):
            morse = encoder.encode_char(char)
            
            if not morse:
                continue
            
            for elem_idx, elem in enumerate(morse):
                # Add the dot or dash tone
                if elem == '.':
                    sequence.append((True, timing['dot_ms']))
                elif elem == '-':
                    sequence.append((True, timing['dash_ms']))
                
                # Add gap between elements (not after last element)
                if elem_idx < len(morse) - 1:
                    sequence.append((False, timing['element_gap_ms']))
            
            # Add gap between characters (not after last character)
            if char_idx < len(word) - 1:
                sequence.append((False, timing['char_gap_ms']))
        
        # Add gap between words (not after last word)
        if word_idx < len(words) - 1:
            sequence.append((False, timing['word_gap_ms']))
    
    return sequence


def text_to_visual(text: str, width: int = 40) -> str:
    """
    Convert text to a visual Morse code representation.
    
    Args:
        text: Text to encode
        width: Maximum characters per line
        
    Returns:
        Visual representation string
    """
    encoder = MorseEncoder(dot_symbol='●', dash_symbol='—')
    morse = encoder.encode(text)
    
    # Wrap to specified width
    lines = []
    while len(morse) > width:
        # Find a good break point
        break_point = morse.rfind('/', 0, width)
        if break_point == -1:
            break_point = morse.rfind(' ', 0, width)
        if break_point == -1:
            break_point = width
        
        lines.append(morse[:break_point].strip())
        morse = morse[break_point:].strip()
    
    if morse:
        lines.append(morse)
    
    return '\n'.join(lines)


def get_morse_reference() -> dict:
    """
    Get the complete Morse code reference.
    
    Returns:
        Dictionary with all Morse code mappings
    """
    return {
        'letters': {k: v for k, v in MORSE_CODE.items() if k.isalpha()},
        'numbers': {k: v for k, v in MORSE_CODE.items() if k.isdigit()},
        'punctuation': {k: v for k, v in MORSE_CODE.items() if not k.isalnum()},
        'prosigns': PROSIGNS.copy(),
    }


def analyze_morse(morse: str) -> dict:
    """
    Analyze a Morse code string.
    
    Args:
        morse: Morse code string to analyze
        
    Returns:
        Dictionary with analysis results
    """
    decoder = MorseDecoder()
    normalized = decoder.normalize_morse(morse)
    
    chars = morse.split(' ')
    
    return {
        'decoded': decoder.decode(morse),
        'total_elements': len([c for c in normalized if c in '.-']),
        'dot_count': normalized.count('.'),
        'dash_count': normalized.count('-'),
        'character_count': len([c for c in chars if c.strip()]),
        'word_count': len([w for w in morse.split('/') if w.strip()]),
        'valid': all(decoder.decode_char(c.strip()) != '?' for c in chars if c.strip()),
    }


# Convenience functions for common use cases
def sos() -> str:
    """Get the SOS distress signal in Morse code."""
    return '... --- ...'


def hello_world() -> str:
    """Get 'HELLO WORLD' in Morse code."""
    return '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'


if __name__ == '__main__':
    # Demo
    print("=== Morse Code Utility Demo ===\n")
    
    # Encode example
    text = "HELLO WORLD"
    encoded = encode(text)
    print(f"Encode '{text}': {encoded}")
    
    # Decode example
    morse = "... --- ..."
    decoded = decode(morse)
    print(f"Decode '{morse}': {decoded}")
    
    # Visual representation
    print(f"\nVisual representation of 'SOS':")
    print(text_to_visual("SOS"))
    
    # Timing information
    print(f"\nTiming at 15 WPM:")
    timing = calculate_speed(15)
    for k, v in timing.items():
        print(f"  {k}: {v:.1f} ms" if isinstance(v, float) else f"  {k}: {v}")
    
    # Analysis
    print(f"\nAnalysis of '... --- ...':")
    analysis = analyze_morse('... --- ...')
    for k, v in analysis.items():
        print(f"  {k}: {v}")