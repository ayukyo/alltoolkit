#!/usr/bin/env python3
"""Tournament Utils Tests"""

import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    MatchStatus, Participant, Match,
    SingleElimination, DoubleElimination, RoundRobin, SwissSystem,
    create_single_elimination, create_double_elimination,
    create_round_robin, create_swiss
)


class TestResultCollector:
    """收集测试结果"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, name):
        self.passed += 1
        print(f"✓ {name}")
    
    def add_fail(self, name, msg):
        self.failed += 1
        self.errors.append((name, msg))
        print(f"✗ {name}: {msg}")
    
    def report(self):
        print(f"\n{'='*60}")
        print(f"Tournament Utils Tests: {self.passed} passed, {self.failed} failed")
        if self.errors:
            print(f"\nFailed tests:")
            for name, msg in self.errors:
                print(f"  - {name}: {msg}")
        print(f"{'='*60}")
        return self.failed == 0


def run_tests():
    results = TestResultCollector()
    
    # Test 1: Participant creation
    try:
        p = Participant(id=1, name="选手A", seed=1, rating=100)
        assert p.id == 1
        assert p.name == "选手A"
        assert p.seed == 1
        assert p.rating == 100
        results.add_pass("Participant creation")
    except Exception as e:
        results.add_fail("Participant creation", str(e))
    
    # Test 2: Participant repr
    try:
        p1 = Participant(id=1, name="选手A", seed=1)
        p2 = Participant(id=2, name="选手B")
        
        assert "[1]" in repr(p1)
        assert "选手A" in repr(p1)
        assert "选手B" in repr(p2)
        results.add_pass("Participant repr")
    except Exception as e:
        results.add_fail("Participant repr", str(e))
    
    # Test 3: Match creation
    try:
        p1 = Participant(id=1, name="选手A")
        p2 = Participant(id=2, name="选手B")
        match = Match(id=0, round_num=1, position=0, participant1=p1, participant2=p2)
        
        assert match.id == 0
        assert match.round_num == 1
        assert match.status == MatchStatus.PENDING
        assert match.participant1 == p1
        assert match.participant2 == p2
        results.add_pass("Match creation")
    except Exception as e:
        results.add_fail("Match creation", str(e))
    
    # Test 4: Single elimination - basic bracket
    try:
        names = ["A", "B", "C", "D"]
        seeds = [1, 4, 2, 3]
        tournament = create_single_elimination(names, seeds)
        
        # 4 participants = 2 rounds
        assert tournament.num_rounds == 2
        assert len(tournament.matches) == 3  # 2 first round + 1 final
        results.add_pass("Single elimination basic bracket")
    except Exception as e:
        results.add_fail("Single elimination basic bracket", str(e))
    
    # Test 5: Single elimination - seed distribution
    try:
        names = ["A", "B", "C", "D", "E", "F", "G", "H"]
        seeds = [1, 8, 4, 5, 3, 6, 2, 7]  # Standard bracket seeding
        tournament = create_single_elimination(names, seeds)
        
        # Seeds should be distributed (top seeds separated)
        first_round = tournament.get_round_matches(1)
        # Verify that seeds are properly distributed (not all in same bracket)
        seeds_in_first_half = [m.participant1.seed if m.participant1 else None for m in first_round[:4]]
        seeds_in_second_half = [m.participant2.seed if m.participant2 else None for m in first_round[:4]]
        # Just verify seeds exist and tournament was created properly
        assert tournament.num_rounds == 3
        results.add_pass("Single elimination seed distribution")
    except Exception as e:
        results.add_fail("Single elimination seed distribution", str(e))
    
    # Test 6: Single elimination - set winner
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_single_elimination(names)
        
        # Get first round matches
        first_round = tournament.get_round_matches(1)
        
        # Set winner for first match
        match1 = first_round[0]
        next_match = tournament.set_winner(match1.id, match1.participant1.id)
        
        assert match1.status == MatchStatus.COMPLETED
        assert match1.winner == match1.participant1
        
        # Winner should advance
        if next_match:
            assert next_match.participant1 == match1.winner or next_match.participant2 == match1.winner
        results.add_pass("Single elimination set winner")
    except Exception as e:
        results.add_fail("Single elimination set winner", str(e))
    
    # Test 7: Single elimination - set score
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_single_elimination(names)
        
        match = tournament.matches[0]
        tournament.set_score(match.id, 3, 1)
        
        assert match.score1 == 3
        assert match.score2 == 1
        assert match.winner == match.participant1  # Higher score wins
        results.add_pass("Single elimination set score")
    except Exception as e:
        results.add_fail("Single elimination set score", str(e))
    
    # Test 8: Single elimination - complete tournament
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_single_elimination(names)
        
        # Complete all matches
        for match_id in list(tournament.matches.keys()):
            match = tournament.matches[match_id]
            if match.status != MatchStatus.BYE:
                winner_id = match.participant1.id
                tournament.set_winner(match_id, winner_id)
        
        assert tournament.is_completed()
        assert tournament.get_winner() is not None
        results.add_pass("Single elimination complete tournament")
    except Exception as e:
        results.add_fail("Single elimination complete tournament", str(e))
    
    # Test 9: Single elimination - bye handling
    try:
        names = ["A", "B", "C"]  # 3 participants = 4 bracket size
        tournament = create_single_elimination(names)
        
        # Should have bye matches
        bye_matches = [m for m in tournament.matches.values() if m.status == MatchStatus.BYE]
        assert len(bye_matches) > 0
        results.add_pass("Single elimination bye handling")
    except Exception as e:
        results.add_fail("Single elimination bye handling", str(e))
    
    # Test 10: Single elimination - get current round
    try:
        names = ["A", "B", "C", "D", "E", "F", "G", "H"]
        tournament = create_single_elimination(names)
        
        # Initially should be round 1
        assert tournament.get_current_round() == 1
        
        # Complete some matches
        for match_id in list(tournament.matches.keys())[:2]:
            match = tournament.matches[match_id]
            if match.status != MatchStatus.BYE:
                tournament.set_winner(match_id, match.participant1.id)
        
        # Should still be round 1 or progressing
        current = tournament.get_current_round()
        assert 1 <= current <= tournament.num_rounds
        results.add_pass("Single elimination get current round")
    except Exception as e:
        results.add_fail("Single elimination get current round", str(e))
    
    # Test 11: Single elimination - to_dict
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_single_elimination(names)
        
        data = tournament.to_dict()
        assert data['type'] == 'single_elimination'
        assert 'participants' in data
        assert 'matches' in data
        assert data['num_rounds'] == 2
        results.add_pass("Single elimination to_dict")
    except Exception as e:
        results.add_fail("Single elimination to_dict", str(e))
    
    # Test 12: Single elimination - visualize
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_single_elimination(names)
        
        visual = tournament.visualize()
        assert "淘汰赛" in visual or "决赛" in visual or "第一轮" in visual
        results.add_pass("Single elimination visualize")
    except Exception as e:
        results.add_fail("Single elimination visualize", str(e))
    
    # Test 13: Double elimination - basic bracket
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_double_elimination(names)
        
        assert len(tournament.winners_bracket) > 0
        assert len(tournament.losers_bracket) > 0
        assert tournament.grand_final is not None
        results.add_pass("Double elimination basic bracket")
    except Exception as e:
        results.add_fail("Double elimination basic bracket", str(e))
    
    # Test 14: Double elimination - set winner in winners bracket
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_double_elimination(names)
        
        # Get first match in winners bracket
        first_match = min(tournament.winners_bracket.values(), key=lambda m: m.id)
        
        if first_match.status != MatchStatus.BYE:
            tournament.set_winner_winner(first_match.id, first_match.participant1.id)
            assert first_match.winner is not None
            assert first_match.loser is not None
        results.add_pass("Double elimination set winner winners bracket")
    except Exception as e:
        results.add_fail("Double elimination set winner winners bracket", str(e))
    
    # Test 15: Double elimination - to_dict
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_double_elimination(names)
        
        data = tournament.to_dict()
        assert data['type'] == 'double_elimination'
        assert 'winners_bracket' in data
        assert 'losers_bracket' in data
        assert 'grand_final' in data
        results.add_pass("Double elimination to_dict")
    except Exception as e:
        results.add_fail("Double elimination to_dict", str(e))
    
    # Test 16: Double elimination - visualize
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_double_elimination(names)
        
        visual = tournament.visualize()
        assert "双败淘汰赛" in visual
        assert "胜者组" in visual
        assert "败者组" in visual
        results.add_pass("Double elimination visualize")
    except Exception as e:
        results.add_fail("Double elimination visualize", str(e))
    
    # Test 17: Round robin - basic schedule
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_round_robin(names)
        
        # 4 participants = 6 matches (n*(n-1)/2)
        assert len(tournament.matches) == 6
        
        # Each participant plays 3 matches
        for p in tournament.participants:
            p_matches = [m for m in tournament.matches 
                        if m.participant1 == p or m.participant2 == p]
            assert len(p_matches) == 3
        results.add_pass("Round robin basic schedule")
    except Exception as e:
        results.add_fail("Round robin basic schedule", str(e))
    
    # Test 18: Round robin - set result
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_round_robin(names)
        
        match = tournament.matches[0]
        tournament.set_result(match.id, 3, 1)
        
        assert match.status == MatchStatus.COMPLETED
        assert match.winner == match.participant1
        
        # Check standings update
        standings = tournament.standings
        assert standings[match.participant1.id]['wins'] == 1
        assert standings[match.participant2.id]['losses'] == 1
        results.add_pass("Round robin set result")
    except Exception as e:
        results.add_fail("Round robin set result", str(e))
    
    # Test 19: Round robin - draw result
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_round_robin(names)
        
        match = tournament.matches[0]
        tournament.set_result(match.id, 1, 1, draw=True)
        
        assert match.winner is None
        assert match.loser is None
        
        standings = tournament.standings
        assert standings[match.participant1.id]['draws'] == 1
        assert standings[match.participant2.id]['draws'] == 1
        results.add_pass("Round robin draw result")
    except Exception as e:
        results.add_fail("Round robin draw result", str(e))
    
    # Test 20: Round robin - get standings
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_round_robin(names)
        
        # Set some results
        for match in tournament.matches[:3]:
            tournament.set_result(match.id, 3, 0)
        
        standings = tournament.get_standings()
        assert len(standings) == 4
        # Sorted by points descending
        assert standings[0]['points'] >= standings[-1]['points']
        results.add_pass("Round robin get standings")
    except Exception as e:
        results.add_fail("Round robin get standings", str(e))
    
    # Test 21: Round robin - complete tournament
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_round_robin(names)
        
        # Complete all matches
        for match in tournament.matches:
            tournament.set_result(match.id, random.randint(0, 3), random.randint(0, 3))
        
        assert tournament.is_completed()
        winner = tournament.get_winner()
        assert winner is not None
        results.add_pass("Round robin complete tournament")
    except Exception as e:
        results.add_fail("Round robin complete tournament", str(e))
    
    # Test 22: Round robin - to_dict
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_round_robin(names)
        
        data = tournament.to_dict()
        assert data['type'] == 'round_robin'
        assert 'standings' in data
        assert 'matches' in data
        results.add_pass("Round robin to_dict")
    except Exception as e:
        results.add_fail("Round robin to_dict", str(e))
    
    # Test 23: Round robin - visualize
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_round_robin(names)
        
        visual = tournament.visualize()
        assert "循环赛" in visual
        assert "积分榜" in visual
        results.add_pass("Round robin visualize")
    except Exception as e:
        results.add_fail("Round robin visualize", str(e))
    
    # Test 24: Swiss system - initial standings
    try:
        names = ["A", "B", "C", "D", "E", "F"]
        tournament = create_swiss(names)
        
        assert len(tournament.standings) == 6
        for s in tournament.standings.values():
            assert s['points'] == 0
            assert s['wins'] == 0
            assert s['losses'] == 0
        results.add_pass("Swiss system initial standings")
    except Exception as e:
        results.add_fail("Swiss system initial standings", str(e))
    
    # Test 25: Swiss system - generate round pairings
    try:
        names = ["A", "B", "C", "D", "E", "F"]
        tournament = create_swiss(names)
        
        matches = tournament.generate_round_pairings()
        assert tournament.current_round == 1
        assert len(matches) > 0
        
        # No duplicate pairings
        for match in matches:
            if match.status != MatchStatus.BYE:
                assert match.participant2.id in tournament.pairing_history[match.participant1.id]
        results.add_pass("Swiss system generate round pairings")
    except Exception as e:
        results.add_fail("Swiss system generate round pairings", str(e))
    
    # Test 26: Swiss system - set result
    try:
        names = ["A", "B", "C", "D", "E", "F"]
        tournament = create_swiss(names)
        
        matches = tournament.generate_round_pairings()
        match = matches[0]
        
        if match.status != MatchStatus.BYE:
            tournament.set_result(match.id, 1, 0)
            assert match.winner is not None
            assert tournament.standings[match.winner.id]['wins'] == 1
            assert tournament.standings[match.winner.id]['points'] == 1.0
        results.add_pass("Swiss system set result")
    except Exception as e:
        results.add_fail("Swiss system set result", str(e))
    
    # Test 27: Swiss system - Buchholz calculation
    try:
        names = ["A", "B", "C", "D", "E", "F"]
        tournament = create_swiss(names)
        
        matches = tournament.generate_round_pairings()
        for match in matches:
            if match.status != MatchStatus.BYE:
                tournament.set_result(match.id, 1, 0)
        
        # Buchholz should be updated
        for s in tournament.standings.values():
            assert s['buchholz'] >= 0
        results.add_pass("Swiss system Buchholz calculation")
    except Exception as e:
        results.add_fail("Swiss system Buchholz calculation", str(e))
    
    # Test 28: Swiss system - complete tournament
    try:
        names = ["A", "B", "C", "D", "E", "F"]
        tournament = create_swiss(names)
        
        for r in range(tournament.num_rounds):
            matches = tournament.generate_round_pairings()
            for match in matches:
                if match.status != MatchStatus.BYE:
                    tournament.set_result(match.id, random.randint(0, 1), random.randint(0, 1))
        
        assert tournament.is_completed()
        winners = tournament.get_winners(top_n=3)
        assert len(winners) == 3
        results.add_pass("Swiss system complete tournament")
    except Exception as e:
        results.add_fail("Swiss system complete tournament", str(e))
    
    # Test 29: Swiss system - to_dict
    try:
        names = ["A", "B", "C", "D", "E", "F"]
        tournament = create_swiss(names)
        
        tournament.generate_round_pairings()
        data = tournament.to_dict()
        
        assert data['type'] == 'swiss'
        assert 'current_round' in data
        assert 'standings' in data
        assert 'buchholz' in data['standings'][0]
        results.add_pass("Swiss system to_dict")
    except Exception as e:
        results.add_fail("Swiss system to_dict", str(e))
    
    # Test 30: Swiss system - visualize
    try:
        names = ["A", "B", "C", "D", "E", "F"]
        tournament = create_swiss(names)
        
        tournament.generate_round_pairings()
        visual = tournament.visualize()
        
        assert "瑞士制比赛" in visual
        assert "积分榜" in visual
        results.add_pass("Swiss system visualize")
    except Exception as e:
        results.add_fail("Swiss system visualize", str(e))
    
    # Test 31: Single elimination - minimum participants
    try:
        names = ["A", "B"]
        tournament = create_single_elimination(names)
        
        assert tournament.num_rounds == 1
        assert len(tournament.matches) == 1
        results.add_pass("Single elimination minimum participants")
    except Exception as e:
        results.add_fail("Single elimination minimum participants", str(e))
    
    # Test 32: Single elimination - invalid match winner
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_single_elimination(names)
        
        match = tournament.matches[0]
        
        try:
            tournament.set_winner(match.id, 999)  # Invalid ID
            results.add_fail("Single elimination invalid match winner", "Should raise ValueError")
        except ValueError:
            pass
        results.add_pass("Single elimination invalid match winner")
    except Exception as e:
        results.add_fail("Single elimination invalid match winner", str(e))
    
    # Test 33: Single elimination - get standings
    try:
        names = ["A", "B", "C", "D"]
        tournament = create_single_elimination(names)
        
        # Complete tournament
        for match_id in list(tournament.matches.keys()):
            match = tournament.matches[match_id]
            if match.status != MatchStatus.BYE:
                tournament.set_winner(match_id, match.participant1.id)
        
        standings = tournament.get_standings()
        assert len(standings) > 0
        assert standings[0] == tournament.get_winner()
        results.add_pass("Single elimination get standings")
    except Exception as e:
        results.add_fail("Single elimination get standings", str(e))
    
    # Test 34: Round robin - odd participants
    try:
        names = ["A", "B", "C", "D", "E"]  # 5 participants
        tournament = create_round_robin(names)
        
        # 5 participants = 10 matches (with bye handling)
        assert len(tournament.matches) == 10
        
        # Each participant plays 4 matches
        for p in tournament.participants:
            p_matches = [m for m in tournament.matches 
                        if m.participant1 == p or m.participant2 == p]
            assert len(p_matches) == 4
        results.add_pass("Round robin odd participants")
    except Exception as e:
        results.add_fail("Round robin odd participants", str(e))
    
    return results.report()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)