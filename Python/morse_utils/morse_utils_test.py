"""
Comprehensive tests for Morse Code Utility Module

Tests cover:
- Basic encoding/decoding
- Edge cases (empty strings, special characters)
- Custom symbols
- Prosigns
- Timing calculations
- Analysis functions
"""

import unittest
from mod import (
    MorseEncoder, MorseDecoder, encode, decode, is_morse,
    calculate_speed, get_timing_sequence, text_to_visual,
    get_morse_reference, analyze_morse, sos, hello_world,
    MORSE_CODE, PROSIGNS
)


class TestMorseEncoder(unittest.TestCase):
    """Test MorseEncoder class."""
    
    def setUp(self):
        self.encoder = MorseEncoder()
    
    def test_encode_single_char(self):
        """Test encoding single characters."""
        self.assertEqual(self.encoder.encode_char('A'), '.-')
        self.assertEqual(self.encoder.encode_char('a'), '.-')  # Case insensitive
        self.assertEqual(self.encoder.encode_char('S'), '...')
        self.assertEqual(self.encoder.encode_char('O',), '---')
        self.assertEqual(self.encoder.encode_char('0'), '-----')
        self.assertEqual(self.encoder.encode_char('9'), '----.')
    
    def test_encode_word(self):
        """Test encoding words."""
        self.assertEqual(self.encoder.encode('SOS'), '... --- ...')
        self.assertEqual(self.encoder.encode('HELLO'), '.... . .-.. .-.. ---')
        self.assertEqual(self.encoder.encode('WORLD'), '.-- --- .-. .-.. -..')
    
    def test_encode_sentence(self):
        """Test encoding sentences with spaces."""
        result = self.encoder.encode('HELLO WORLD')
        self.assertEqual(result, '.... . .-.. .-.. --- / .-- --- .-. .-.. -..')
    
    def test_encode_numbers(self):
        """Test encoding numbers."""
        self.assertEqual(self.encoder.encode('123'), '.---- ..--- ...--')
        self.assertEqual(self.encoder.encode('2024'), '..--- ----- ..--- ....-')
    
    def test_encode_punctuation(self):
        """Test encoding punctuation."""
        self.assertEqual(self.encoder.encode('HI!'), '.... .. -.-.--')
        self.assertEqual(self.encoder.encode('YES.'), '-.-- . ... .-.-.-')
        self.assertEqual(self.encoder.encode('A,B'), '.- --..-- -...')
    
    def test_encode_empty(self):
        """Test encoding empty string."""
        self.assertEqual(self.encoder.encode(''), '')
    
    def test_encode_unknown_char(self):
        """Test encoding with unknown characters."""
        # Unknown characters should be skipped
        result = self.encoder.encode('A#B')
        self.assertEqual(result, '.- -...')  # # is skipped
    
    def test_custom_symbols(self):
        """Test encoding with custom symbols."""
        custom_encoder = MorseEncoder(dot_symbol='○', dash_symbol='▬')
        self.assertEqual(custom_encoder.encode('SOS'), '○○○ ▬▬▬ ○○○')
        self.assertEqual(custom_encoder.encode('A'), '○▬')
    
    def test_encode_prosign(self):
        """Test encoding prosigns."""
        self.assertEqual(self.encoder.encode_prosign('AR'), '.-.-.')
        self.assertEqual(self.encoder.encode_prosign('SK'), '...-.-')
        self.assertEqual(self.encoder.encode_prosign('BT'), '-...-')
        self.assertEqual(self.encoder.encode_prosign('UNKNOWN'), '')


class TestMorseDecoder(unittest.TestCase):
    """Test MorseDecoder class."""
    
    def setUp(self):
        self.decoder = MorseDecoder()
    
    def test_decode_single_char(self):
        """Test decoding single characters."""
        self.assertEqual(self.decoder.decode_char('.-'), 'A')
        self.assertEqual(self.decoder.decode_char('...'), 'S')
        self.assertEqual(self.decoder.decode_char('---'), 'O')
        self.assertEqual(self.decoder.decode_char('-----'), '0')
    
    def test_decode_word(self):
        """Test decoding words."""
        self.assertEqual(self.decoder.decode('... --- ...'), 'SOS')
        self.assertEqual(self.decoder.decode('.... . .-.. .-.. ---'), 'HELLO')
    
    def test_decode_sentence(self):
        """Test decoding sentences with word separators."""
        result = self.decoder.decode('.... . .-.. .-.. --- / .-- --- .-. .-.. -..')
        self.assertEqual(result, 'HELLO WORLD')
    
    def test_decode_numbers(self):
        """Test decoding numbers."""
        self.assertEqual(self.decoder.decode('.---- ..--- ...--'), '123')
        self.assertEqual(self.decoder.decode('----- -----'), '00')
    
    def test_decode_empty(self):
        """Test decoding empty string."""
        self.assertEqual(self.decoder.decode(''), '')
    
    def test_decode_unknown(self):
        """Test decoding unknown morse sequences."""
        # Unknown sequences should return '?'
        self.assertEqual(self.decoder.decode_char('..........'), '?')  # Invalid
    
    def test_custom_symbols(self):
        """Test decoding with custom symbols."""
        custom_decoder = MorseDecoder(dot_symbol='○', dash_symbol='▬')
        self.assertEqual(custom_decoder.decode('○○○ ▬▬▬ ○○○'), 'SOS')
        self.assertEqual(custom_decoder.decode('○▬'), 'A')
    
    def test_normalize_morse(self):
        """Test morse normalization."""
        decoder = MorseDecoder(dot_symbol='○', dash_symbol='▬')
        self.assertEqual(decoder.normalize_morse('○▬○'), '.-.')


class TestEncodeDecodeRoundtrip(unittest.TestCase):
    """Test that encode-decode roundtrips correctly."""
    
    def test_roundtrip_letters(self):
        """Test roundtrip with letters."""
        texts = ['HELLO', 'WORLD', 'MORSE', 'CODE', 'TEST']
        for text in texts:
            encoded = encode(text)
            decoded = decode(encoded)
            self.assertEqual(decoded, text)
    
    def test_roundtrip_numbers(self):
        """Test roundtrip with numbers."""
        texts = ['1234567890', '000', '999']
        for text in texts:
            encoded = encode(text)
            decoded = decode(encoded)
            self.assertEqual(decoded, text)
    
    def test_roundtrip_mixed(self):
        """Test roundtrip with mixed content."""
        texts = ['ABC123', 'TEST2024', 'SOS']
        for text in texts:
            encoded = encode(text)
            decoded = decode(encoded)
            self.assertEqual(decoded, text)
    
    def test_roundtrip_custom_symbols(self):
        """Test roundtrip with custom symbols."""
        text = 'HELLO'
        encoded = encode(text, dot='○', dash='▬')
        decoded = decode(encoded, dot='○', dash='▬')
        self.assertEqual(decoded, text)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_is_morse(self):
        """Test Morse code detection."""
        self.assertTrue(is_morse('... --- ...'))
        self.assertTrue(is_morse('.- .-.. .-.. ---'))
        self.assertTrue(is_morse('.-/'))
        self.assertFalse(is_morse('HELLO'))
        self.assertFalse(is_morse('Hello World'))
    
    def test_calculate_speed(self):
        """Test speed calculation."""
        # Standard PARIS method: 50 units per word
        timing_15wpm = calculate_speed(15)
        self.assertEqual(timing_15wpm['wpm'], 15)
        self.assertAlmostEqual(timing_15wpm['unit_ms'], 80.0, places=1)
        self.assertAlmostEqual(timing_15wpm['dot_ms'], 80.0, places=1)
        self.assertAlmostEqual(timing_15wpm['dash_ms'], 240.0, places=1)
        
        timing_20wpm = calculate_speed(20)
        self.assertAlmostEqual(timing_20wpm['unit_ms'], 60.0, places=1)
    
    def test_get_timing_sequence(self):
        """Test timing sequence generation."""
        sequence = get_timing_sequence('SOS', wpm=15)
        
        # SOS = ... --- ... (3+3+3 elements, gaps between)
        # Should start with tone (dot), alternate tone/gap
        self.assertTrue(sequence[0][0])  # First is tone
        self.assertEqual(sequence[0][1], 80.0)  # Dot duration
        self.assertFalse(sequence[1][0])  # Second is gap
        self.assertEqual(sequence[1][1], 80.0)  # Gap duration
    
    def test_text_to_visual(self):
        """Test visual representation."""
        visual = text_to_visual('SOS')
        self.assertIn('●', visual)
        self.assertIn('—', visual)
    
    def test_get_morse_reference(self):
        """Test morse reference dictionary."""
        ref = get_morse_reference()
        
        self.assertIn('letters', ref)
        self.assertIn('numbers', ref)
        self.assertIn('punctuation', ref)
        self.assertIn('prosigns', ref)
        
        # Check some known values
        self.assertEqual(ref['letters']['A'], '.-')
        self.assertEqual(ref['numbers']['1'], '.----')
        self.assertIn('.', ref['punctuation'])
    
    def test_analyze_morse(self):
        """Test morse analysis."""
        analysis = analyze_morse('... --- ...')
        
        self.assertEqual(analysis['decoded'], 'SOS')
        self.assertEqual(analysis['dot_count'], 6)
        self.assertEqual(analysis['dash_count'], 3)
        self.assertEqual(analysis['valid'], True)
    
    def test_sos(self):
        """Test SOS distress signal."""
        self.assertEqual(sos(), '... --- ...')
    
    def test_hello_world(self):
        """Test HELLO WORLD example."""
        expected = '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'
        self.assertEqual(hello_world(), expected)


class TestMorseCodeDictionary(unittest.TestCase):
    """Test Morse code dictionary completeness."""
    
    def test_all_letters_present(self):
        """Test that all letters are present."""
        for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            self.assertIn(char, MORSE_CODE, f"Missing letter: {char}")
    
    def test_all_numbers_present(self):
        """Test that all numbers are present."""
        for char in '0123456789':
            self.assertIn(char, MORSE_CODE, f"Missing number: {char}")
    
    def test_morse_patterns_valid(self):
        """Test that all morse patterns are valid."""
        for char, pattern in MORSE_CODE.items():
            for symbol in pattern:
                self.assertIn(symbol, '.-', 
                             f"Invalid symbol '{symbol}' in pattern for '{char}'")
    
    def test_no_duplicate_patterns(self):
        """Test that no two characters have the same pattern."""
        patterns = list(MORSE_CODE.values())
        unique_patterns = set(patterns)
        self.assertEqual(len(patterns), len(unique_patterns), 
                        "Duplicate patterns found")


class TestProsigns(unittest.TestCase):
    """Test prosign functionality."""
    
    def test_prosigns_defined(self):
        """Test that common prosigns are defined."""
        self.assertIn('AR', PROSIGNS)  # End of transmission
        self.assertIn('SK', PROSIGNS)  # End of work
        self.assertIn('BT', PROSIGNS)  # Break
    
    def test_prosign_patterns_valid(self):
        """Test that all prosign patterns are valid."""
        for name, pattern in PROSIGNS.items():
            for symbol in pattern:
                self.assertIn(symbol, '.-', 
                             f"Invalid symbol in prosign {name}")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_multiple_spaces(self):
        """Test handling multiple spaces in input."""
        result = encode('A  B')  # Multiple spaces
        # Multiple spaces should result in word separators
        self.assertIn('.-', result)
        self.assertIn('-...', result)
    
    def test_only_spaces(self):
        """Test handling only spaces."""
        result = encode('   ')
        self.assertEqual(result, '')
    
    def test_mixed_case(self):
        """Test handling mixed case."""
        result = encode('HeLLo')
        decoded = decode(result)
        self.assertEqual(decoded, 'HELLO')
    
    def test_leading_trailing_spaces(self):
        """Test handling leading/trailing spaces."""
        result = encode(' HELLO ')
        # Should handle gracefully
        self.assertIn('.... . .-.. .-.. ---', result)


class TestPerformance(unittest.TestCase):
    """Test performance with larger inputs."""
    
    def test_long_text(self):
        """Test encoding/decoding long text."""
        # Generate a long text
        text = 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG ' * 10
        
        encoded = encode(text)
        self.assertTrue(len(encoded) > 0)
        
        decoded = decode(encoded)
        self.assertEqual(decoded, text.strip())
    
    def test_many_characters(self):
        """Test encoding all available characters."""
        all_chars = ''.join(MORSE_CODE.keys())
        
        encoded = encode(all_chars)
        self.assertTrue(len(encoded) > 0)
        
        decoded = decode(encoded)
        # All characters should be decodable
        self.assertEqual(len(decoded), len(all_chars))


if __name__ == '__main__':
    unittest.main(verbosity=2)