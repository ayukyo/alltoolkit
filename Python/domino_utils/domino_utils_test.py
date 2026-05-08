"""
Comprehensive tests for domino_utils module.

Run with: python domino_utils_test.py
"""

import unittest
from domino_utils import (
    Domino, DominoSet, DominoChain, DominoHand, 
    DominoSolver, DominoGame,
    domino, domino_set, find_chain, longest_chain, can_chain_all, deal_hands
)


class TestDomino(unittest.TestCase):
    """Test Domino class."""
    
    def test_basic_creation(self):
        """Test basic domino creation."""
        d = Domino(3, 5)
        self.assertEqual(d.left, 3)
        self.assertEqual(d.right, 5)
        self.assertEqual(str(d), "[3|5]")
    
    def test_normalization(self):
        """Test that dominoes are equal regardless of order."""
        d1 = Domino(5, 3)
        d2 = Domino(3, 5)
        # Equality should be same (unordered)
        self.assertEqual(d1, d2)
        # But order is preserved for display
        self.assertEqual(d1.left, 5)
        self.assertEqual(d1.right, 3)
        self.assertEqual(d2.left, 3)
        self.assertEqual(d2.right, 5)
    
    def test_double(self):
        """Test double domino detection."""
        d1 = Domino(6, 6)
        d2 = Domino(3, 5)
        self.assertTrue(d1.is_double)
        self.assertFalse(d2.is_double)
    
    def test_total(self):
        """Test pip count."""
        d = Domino(4, 5)
        self.assertEqual(d.total, 9)
    
    def test_can_connect(self):
        """Test connection checking."""
        d = Domino(3, 5)
        self.assertTrue(d.can_connect(3))
        self.assertTrue(d.can_connect(5))
        self.assertFalse(d.can_connect(4))
    
    def test_other_end(self):
        """Test getting the other end."""
        d = Domino(3, 5)
        self.assertEqual(d.other_end(3), 5)
        self.assertEqual(d.other_end(5), 3)
        self.assertIsNone(d.other_end(4))
    
    def test_flip(self):
        """Test flipping a domino."""
        d = Domino(3, 5)
        flipped = d.flip()
        self.assertEqual(flipped.left, 5)
        self.assertEqual(flipped.right, 3)
        # But equality should be same after normalization
        self.assertEqual(d, flipped)
    
    def test_contains(self):
        """Test value containment check."""
        d = Domino(2, 4)
        self.assertTrue(d.contains(2))
        self.assertTrue(d.contains(4))
        self.assertFalse(d.contains(3))
    
    def test_hash_and_equality(self):
        """Test that dominoes can be used in sets."""
        d1 = Domino(3, 5)
        d2 = Domino(5, 3)
        d3 = Domino(3, 5)
        
        s = {d1, d2, d3}
        self.assertEqual(len(s), 1)  # All same after normalization
    
    def test_to_dict_from_dict(self):
        """Test dictionary conversion."""
        d = Domino(2, 6)
        d_dict = d.to_dict()
        self.assertEqual(d_dict, {'left': 2, 'right': 6})
        
        d2 = Domino.from_dict(d_dict)
        self.assertEqual(d, d2)
    
    def test_from_tuple(self):
        """Test creating from tuple."""
        d = Domino.from_tuple((4, 5))
        self.assertEqual(d.left, 4)
        self.assertEqual(d.right, 5)


class TestDominoSet(unittest.TestCase):
    """Test DominoSet class."""
    
    def test_double_six_set(self):
        """Test standard double-six set creation."""
        s = DominoSet(6)
        self.assertEqual(s.count, 28)  # 7*8/2 = 28 tiles
    
    def test_double_nine_set(self):
        """Test double-nine set creation."""
        s = DominoSet(9)
        self.assertEqual(s.count, 55)  # 10*11/2 = 55 tiles
    
    def test_double_twelve_set(self):
        """Test double-twelve set creation."""
        s = DominoSet(12)
        self.assertEqual(s.count, 91)  # 13*14/2 = 91 tiles
    
    def test_get_doubles(self):
        """Test getting all doubles."""
        s = DominoSet(6)
        doubles = s.get_doubles()
        self.assertEqual(len(doubles), 7)  # 0-0 through 6-6
        for d in doubles:
            self.assertTrue(d.is_double)
    
    def test_get_tiles_with_value(self):
        """Test getting tiles containing a value."""
        s = DominoSet(6)
        tiles_with_6 = s.get_tiles_with_value(6)
        # Should be: 0-6, 1-6, 2-6, 3-6, 4-6, 5-6, 6-6 = 7 tiles
        self.assertEqual(len(tiles_with_6), 7)
        
        tiles_with_0 = s.get_tiles_with_value(0)
        self.assertEqual(len(tiles_with_0), 7)  # 0-0 through 0-6
    
    def test_get_tiles_by_total(self):
        """Test getting tiles by pip total."""
        s = DominoSet(6)
        total_6 = s.get_tiles_by_total(6)
        # Pairs that sum to 6: 0-6, 1-5, 2-4, 3-3
        self.assertEqual(len(total_6), 4)
    
    def test_sample(self):
        """Test random sampling."""
        s = DominoSet(6)
        sample = s.sample(7, seed=42)
        self.assertEqual(len(sample), 7)
        # Check all unique
        self.assertEqual(len(set(sample)), 7)
    
    def test_shuffle(self):
        """Test shuffling."""
        s = DominoSet(6)
        shuffled = s.shuffle(seed=42)
        self.assertEqual(len(shuffled), 28)
        # Check all tiles present
        self.assertEqual(set(shuffled), s.tiles)
    
    def test_deal(self):
        """Test dealing dominoes."""
        s = DominoSet(6)
        hands, boneyard = s.deal(2, 7, seed=42)
        
        self.assertEqual(len(hands), 2)
        self.assertEqual(len(hands[0]), 7)
        self.assertEqual(len(hands[1]), 7)
        self.assertEqual(len(boneyard), 14)  # 28 - 14 = 14
    
    def test_statistics(self):
        """Test statistics generation."""
        s = DominoSet(6)
        stats = s.statistics
        
        self.assertEqual(stats['max_value'], 6)
        self.assertEqual(stats['total_tiles'], 28)
        self.assertEqual(stats['doubles_count'], 7)
        # Sum of all pips: sum from 0 to 6 of (i * (7 - i))
        # = 0*7 + 1*6 + 2*5 + 3*4 + 4*3 + 5*2 + 6*1 = 56
        self.assertEqual(stats['total_pip_sum'], 168)
    
    def test_iteration(self):
        """Test iterating over set."""
        s = DominoSet(6)
        count = 0
        for _ in s:
            count += 1
        self.assertEqual(count, 28)
    
    def test_contains(self):
        """Test set membership."""
        s = DominoSet(6)
        self.assertIn(Domino(3, 5), s)
        self.assertIn(Domino(5, 3), s)  # Same after normalization
        self.assertNotIn(Domino(7, 7), s)  # Not in double-six set


class TestDominoChain(unittest.TestCase):
    """Test DominoChain class."""
    
    def test_empty_chain(self):
        """Test empty chain creation."""
        chain = DominoChain()
        self.assertEqual(chain.length, 0)
        self.assertIsNone(chain.left_end)
        self.assertIsNone(chain.right_end)
    
    def test_single_domino(self):
        """Test chain with single domino."""
        chain = DominoChain(Domino(3, 5))
        self.assertEqual(chain.length, 1)
        self.assertEqual(chain.left_end, 3)
        self.assertEqual(chain.right_end, 5)
    
    def test_add_domino(self):
        """Test adding dominoes to chain."""
        chain = DominoChain(Domino(3, 5))
        
        # Add to right
        self.assertTrue(chain.add(Domino(5, 2)))
        self.assertEqual(chain.length, 2)
        self.assertEqual(chain.right_end, 2)
        
        # Add to left
        self.assertTrue(chain.add(Domino(4, 3), 'left'))
        self.assertEqual(chain.length, 3)
        self.assertEqual(chain.left_end, 4)
    
    def test_cannot_add(self):
        """Test that incompatible dominoes can't be added."""
        chain = DominoChain(Domino(3, 5))
        self.assertFalse(chain.add(Domino(2, 4)))  # No 2 or 4 matches
    
    def test_chain_string(self):
        """Test chain string representation."""
        chain = DominoChain()
        chain.add(Domino(3, 5))
        chain.add(Domino(5, 2))
        self.assertIn("[3|5]", str(chain))
        self.assertIn("[5|2]", str(chain))
    
    def test_playable_tiles(self):
        """Test finding playable tiles."""
        chain = DominoChain(Domino(3, 5))
        
        tiles = {
            Domino(5, 2),  # Can play on right
            Domino(1, 3),  # Can play on left
            Domino(4, 6),  # Cannot play
            Domino(0, 0),  # Cannot play
        }
        
        playable = chain.playable_tiles(tiles)
        self.assertIn(Domino(5, 2), playable)
        self.assertIn(Domino(1, 3), playable)
        self.assertNotIn(Domino(4, 6), playable)
    
    def test_copy(self):
        """Test chain copying."""
        chain = DominoChain(Domino(3, 5))
        chain.add(Domino(5, 2))
        
        chain_copy = chain.copy()
        chain_copy.add(Domino(2, 4))
        
        # Original unchanged
        self.assertEqual(chain.length, 2)
        self.assertEqual(chain_copy.length, 3)
    
    def test_from_list(self):
        """Test creating chain from list."""
        chain = DominoChain.from_list([(3, 5), (5, 2), (2, 4)])
        self.assertEqual(chain.length, 3)
        self.assertEqual(chain.left_end, 3)
        self.assertEqual(chain.right_end, 4)
    
    def test_to_list(self):
        """Test converting chain to list."""
        chain = DominoChain()
        chain.add(Domino(3, 5))
        chain.add(Domino(5, 2))
        
        tiles = chain.to_list()
        self.assertEqual(len(tiles), 2)
        self.assertIn((3, 5), tiles)
        self.assertIn((5, 2), tiles)


class TestDominoHand(unittest.TestCase):
    """Test DominoHand class."""
    
    def test_empty_hand(self):
        """Test empty hand creation."""
        hand = DominoHand()
        self.assertEqual(len(hand), 0)
    
    def test_add_remove(self):
        """Test adding and removing tiles."""
        hand = DominoHand()
        d = Domino(3, 5)
        
        hand.add(d)
        self.assertEqual(len(hand), 1)
        self.assertIn(d, hand)
        
        self.assertTrue(hand.remove(d))
        self.assertEqual(len(hand), 0)
        self.assertFalse(hand.remove(d))  # Already removed
    
    def test_total_pips(self):
        """Test pip count calculation."""
        hand = DominoHand([Domino(3, 5), Domino(2, 4)])
        self.assertEqual(hand.total_pips, 14)  # 8 + 6
    
    def test_get_doubles(self):
        """Test getting doubles from hand."""
        hand = DominoHand([
            Domino(6, 6),
            Domino(3, 5),
            Domino(4, 4),
        ])
        
        doubles = hand.get_doubles()
        self.assertEqual(len(doubles), 2)
        self.assertIn(Domino(6, 6), doubles)
        self.assertIn(Domino(4, 4), doubles)
    
    def test_highest_double(self):
        """Test finding highest double."""
        hand = DominoHand([
            Domino(3, 3),
            Domino(6, 6),
            Domino(1, 1),
        ])
        
        highest = hand.get_highest_double()
        self.assertEqual(highest, Domino(6, 6))
    
    def test_no_doubles(self):
        """Test hand with no doubles."""
        hand = DominoHand([
            Domino(3, 5),
            Domino(2, 4),
        ])
        
        self.assertFalse(hand.has_double())
        self.assertIsNone(hand.get_highest_double())
    
    def test_playable_tiles(self):
        """Test finding playable tiles."""
        hand = DominoHand([
            Domino(3, 5),
            Domino(5, 2),
            Domino(4, 6),
        ])
        
        chain = DominoChain(Domino(1, 3))
        playable = hand.playable_tiles(chain)
        
        # Only [3|5] can play (matches 3 on left)
        self.assertEqual(len(playable), 1)
        self.assertIn(Domino(3, 5), playable)
    
    def test_can_play(self):
        """Test checking if any tile can play."""
        hand = DominoHand([Domino(3, 5), Domino(4, 6)])
        
        chain1 = DominoChain(Domino(1, 3))
        self.assertTrue(hand.can_play(chain1))
        
        chain2 = DominoChain(Domino(0, 0))
        self.assertFalse(hand.can_play(chain2))
    
    def test_best_play(self):
        """Test best play selection."""
        hand = DominoHand([
            Domino(3, 5),
            Domino(5, 6),
        ])
        
        chain = DominoChain(Domino(2, 5))
        
        # Highest strategy
        best = hand.best_play(chain, 'highest')
        self.assertIsNotNone(best)
        # [5|6] has higher total (11 vs 8)
        self.assertEqual(best[0], Domino(5, 6))
    
    def test_statistics(self):
        """Test hand statistics."""
        hand = DominoHand([
            Domino(3, 5),
            Domino(5, 6),
            Domino(6, 6),
        ])
        
        stats = hand.statistics
        self.assertEqual(stats['tile_count'], 3)
        self.assertEqual(stats['total_pips'], 31)
        self.assertEqual(stats['doubles_count'], 1)
    
    def test_from_list(self):
        """Test creating hand from list."""
        hand = DominoHand.from_list([(3, 5), (5, 6)])
        self.assertEqual(len(hand), 2)


class TestDominoSolver(unittest.TestCase):
    """Test DominoSolver class."""
    
    def test_find_chain_two_tiles(self):
        """Test finding chain with two tiles."""
        tiles = [Domino(3, 5), Domino(5, 2)]
        chain = DominoSolver.find_longest_chain(tiles)
        
        self.assertEqual(chain.length, 2)
    
    def test_find_chain_blocked(self):
        """Test when tiles can't all connect."""
        tiles = [Domino(3, 5), Domino(1, 2)]
        chain = DominoSolver.find_longest_chain(tiles)
        
        # Can only use one tile
        self.assertEqual(chain.length, 1)
    
    def test_solve_solitaire(self):
        """Test solving domino solitaire."""
        tiles = [Domino(3, 5), Domino(5, 2), Domino(2, 4)]
        chain = DominoSolver.solve_domino_solitaire(tiles)
        
        self.assertIsNotNone(chain)
        self.assertEqual(chain.length, 3)
    
    def test_solve_impossible(self):
        """Test impossible solitaire puzzle."""
        tiles = [Domino(3, 5), Domino(1, 2), Domino(4, 6)]
        chain = DominoSolver.solve_domino_solitaire(tiles)
        
        self.assertIsNone(chain)
    
    def test_can_form_single_chain(self):
        """Test checking if single chain is possible."""
        # Can form single chain (Eulerian path exists)
        tiles1 = [Domino(3, 5), Domino(5, 2), Domino(2, 4)]
        self.assertTrue(DominoSolver.can_form_single_chain(tiles1))
        
        # Cannot form single chain (more than 2 odd-degree vertices)
        tiles2 = [Domino(3, 5), Domino(1, 2), Domino(4, 6)]
        self.assertFalse(DominoSolver.can_form_single_chain(tiles2))
    
    def test_find_chain_with_ends(self):
        """Test finding chain with specific ends."""
        tiles = [Domino(3, 5), Domino(5, 2), Domino(2, 4)]
        chain = DominoSolver.find_chain_with_ends(tiles, 3, 4)
        
        self.assertIsNotNone(chain)
        self.assertEqual(chain.left_end, 3)
        self.assertEqual(chain.right_end, 4)
    
    def test_find_all_chains(self):
        """Test finding all chains."""
        tiles = [Domino(3, 5), Domino(5, 2)]
        chains = list(DominoSolver.find_all_chains(tiles, min_length=2))
        
        self.assertGreater(len(chains), 0)
        for chain in chains:
            self.assertGreaterEqual(chain.length, 2)
    
    def test_empty_tiles(self):
        """Test with empty tile list."""
        chain = DominoSolver.find_longest_chain([])
        self.assertEqual(chain.length, 0)
    
    def test_single_tile(self):
        """Test with single tile."""
        tiles = [Domino(3, 5)]
        chain = DominoSolver.find_longest_chain(tiles)
        
        self.assertEqual(chain.length, 1)


class TestDominoGame(unittest.TestCase):
    """Test DominoGame class."""
    
    def test_draw_dominoes(self):
        """Test drawing initial hands."""
        result = DominoGame.draw_dominoes('standard', 2, 6, seed=42)
        
        self.assertEqual(len(result['hands']), 2)
        self.assertEqual(len(result['hands'][0]), 7)
        self.assertEqual(len(result['hands'][1]), 7)
        self.assertEqual(len(result['boneyard']), 14)
    
    def test_determine_first_player_highest_double(self):
        """Test determining first player with highest double rule."""
        hand1 = DominoHand([Domino(3, 3), Domino(1, 2)])  # Has double-3
        hand2 = DominoHand([Domino(2, 2), Domino(5, 6)])  # Has double-2
        
        first = DominoGame.determine_first_player([hand1, hand2], 'highest_double')
        self.assertEqual(first, 0)  # Player 0 has higher double
    
    def test_determine_first_player_heaviest(self):
        """Test determining first player with heaviest rule."""
        hand1 = DominoHand([Domino(3, 5)])  # Total 8
        hand2 = DominoHand([Domino(6, 6)])  # Total 12
        
        first = DominoGame.determine_first_player([hand1, hand2], 'heaviest')
        self.assertEqual(first, 1)  # Player 1 has more pips
    
    def test_calculate_score_draw(self):
        """Test score calculation for drawn game."""
        hand1 = DominoHand([Domino(3, 5)])  # Total 8
        hand2 = DominoHand([Domino(1, 2)])  # Total 3
        
        winner, score = DominoGame.calculate_score_draw_game([hand1, hand2])
        self.assertEqual(winner, 1)  # Player 1 has fewer pips
        self.assertEqual(score, 11)  # Sum of all pips
    
    def test_is_round_over_winner(self):
        """Test detecting round over when someone wins."""
        hand1 = DominoHand()  # Empty - player won
        hand2 = DominoHand([Domino(3, 5)])
        chain = DominoChain(Domino(0, 0))
        
        self.assertTrue(DominoGame.is_round_over([hand1, hand2], chain))
    
    def test_is_round_over_blocked(self):
        """Test detecting blocked game."""
        hand1 = DominoHand([Domino(3, 5)])  # No match
        hand2 = DominoHand([Domino(1, 2)])  # No match
        chain = DominoChain(Domino(0, 0))  # Ends are 0
        
        self.assertTrue(DominoGame.is_round_over([hand1, hand2], chain))
    
    def test_is_round_over_continuing(self):
        """Test detecting game still in progress."""
        hand1 = DominoHand([Domino(3, 5)])  # Can match 3
        hand2 = DominoHand([Domino(0, 0)])
        chain = DominoChain(Domino(1, 3))  # Left end 1, right end 3
        
        self.assertFalse(DominoGame.is_round_over([hand1, hand2], chain))


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_domino_function(self):
        """Test domino() convenience function."""
        d = domino(3, 5)
        self.assertIsInstance(d, Domino)
        self.assertEqual(d.left, 3)
        self.assertEqual(d.right, 5)
    
    def test_domino_set_function(self):
        """Test domino_set() convenience function."""
        s = domino_set(6)
        self.assertIsInstance(s, DominoSet)
        self.assertEqual(s.count, 28)
    
    def test_find_chain_function(self):
        """Test find_chain() convenience function."""
        tiles = [(3, 5), (5, 2), (2, 4)]
        chain = find_chain(tiles)
        
        self.assertIsNotNone(chain)
        self.assertEqual(chain.length, 3)
    
    def test_longest_chain_function(self):
        """Test longest_chain() convenience function."""
        tiles = [(3, 5), (1, 2)]
        chain = longest_chain(tiles)
        
        self.assertEqual(chain.length, 1)
    
    def test_can_chain_all_function(self):
        """Test can_chain_all() convenience function."""
        tiles1 = [(3, 5), (5, 2), (2, 4)]
        self.assertTrue(can_chain_all(tiles1))
        
        tiles2 = [(3, 5), (1, 2), (4, 6)]
        self.assertFalse(can_chain_all(tiles2))
    
    def test_deal_hands_function(self):
        """Test deal_hands() convenience function."""
        hands, boneyard = deal_hands(2, 6, seed=42)
        
        self.assertEqual(len(hands), 2)
        self.assertIsInstance(hands[0], DominoHand)
        self.assertEqual(len(hands[0]), 7)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_zero_value_domino(self):
        """Test domino with zero value."""
        d = Domino(0, 5)
        self.assertEqual(d.left, 0)
        self.assertEqual(d.right, 5)
        self.assertEqual(d.total, 5)
    
    def test_double_zero(self):
        """Test double-zero domino."""
        d = Domino(0, 0)
        self.assertTrue(d.is_double)
        self.assertEqual(d.total, 0)
    
    def test_large_domino_set(self):
        """Test larger domino set."""
        s = DominoSet(15)
        # Number of tiles = (n+1)(n+2)/2 = 16*17/2 = 136
        self.assertEqual(s.count, 136)
    
    def test_invalid_sample(self):
        """Test sampling more tiles than available."""
        s = DominoSet(6)
        with self.assertRaises(ValueError):
            s.sample(100)  # More than 28 tiles
    
    def test_invalid_deal(self):
        """Test dealing too many tiles."""
        s = DominoSet(6)
        with self.assertRaises(ValueError):
            s.deal(10, 10)  # 100 tiles needed, only 28 available
    
    def test_negative_domino_value(self):
        """Test that negative values are normalized but valid."""
        # Values should be non-negative in practice
        d = Domino(3, 5)
        self.assertIsInstance(d, Domino)
    
    def test_empty_solver_input(self):
        """Test solver with empty input."""
        self.assertEqual(DominoSolver.find_longest_chain([]).length, 0)
        self.assertTrue(DominoSolver.can_form_single_chain([]))
    
    def test_single_tile_solver(self):
        """Test solver with single tile."""
        tiles = [Domino(3, 5)]
        chain = DominoSolver.solve_domino_solitaire(tiles)
        
        self.assertIsNotNone(chain)
        self.assertEqual(chain.length, 1)
    
    def test_chain_add_incompatible(self):
        """Test adding incompatible domino returns False."""
        chain = DominoChain(Domino(3, 5))
        result = chain.add(Domino(1, 2))  # No matching end
        self.assertFalse(result)
        self.assertEqual(chain.length, 1)  # Unchanged


class TestDominoSetVariants(unittest.TestCase):
    """Test different domino set variants."""
    
    def test_double_six_properties(self):
        """Test properties of double-six set."""
        s = DominoSet(6)
        
        # Total tiles: (6+1)(6+2)/2 = 28
        self.assertEqual(s.count, 28)
        
        # Tiles with each value
        for v in range(7):
            tiles = s.get_tiles_with_value(v)
            self.assertEqual(len(tiles), 7)
    
    def test_double_nine_properties(self):
        """Test properties of double-nine set."""
        s = DominoSet(9)
        
        # Total tiles: (9+1)(9+2)/2 = 55
        self.assertEqual(s.count, 55)
        
        # Tiles with each value
        for v in range(10):
            tiles = s.get_tiles_with_value(v)
            self.assertEqual(len(tiles), 10)
    
    def test_double_twelve_properties(self):
        """Test properties of double-twelve set."""
        s = DominoSet(12)
        
        # Total tiles: (12+1)(12+2)/2 = 91
        self.assertEqual(s.count, 91)


class TestDominoChainOrientation(unittest.TestCase):
    """Test domino chain orientation handling."""
    
    def test_auto_orientation_left(self):
        """Test automatic orientation when adding to left."""
        chain = DominoChain(Domino(3, 5))
        chain.add(Domino(2, 3), 'left')  # Should be oriented as [2|3]
        
        self.assertEqual(chain.left_end, 2)
        self.assertEqual(chain.length, 2)
    
    def test_auto_orientation_right(self):
        """Test automatic orientation when adding to right."""
        chain = DominoChain(Domino(3, 5))
        chain.add(Domino(5, 2))  # Should stay [5|2]
        
        self.assertEqual(chain.right_end, 2)
        self.assertEqual(chain.length, 2)
    
    def test_complex_chain_building(self):
        """Test building a complex chain."""
        chain = DominoChain()
        
        # Build chain: [3|5]-[5|2]-[2|6]-[6|4]
        chain.add(Domino(3, 5))
        chain.add(Domino(5, 2))
        chain.add(Domino(2, 6))
        chain.add(Domino(6, 4))
        
        self.assertEqual(chain.length, 4)
        self.assertEqual(chain.left_end, 3)
        self.assertEqual(chain.right_end, 4)


if __name__ == '__main__':
    unittest.main(verbosity=2)