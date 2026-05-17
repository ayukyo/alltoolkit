#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Voting Utilities Test Module

Comprehensive tests for voting utilities.

Author: AllToolkit
License: MIT
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from voting_utils.mod import (
    VotingMethod, PollStatus, Candidate, Ballot, Poll, VoteCount, ElectionResult,
    plurality_vote, approval_vote, borda_count, ranked_choice_vote, 
    condorcet_vote, score_vote, stv_vote, count_votes,
    create_poll, create_ballot, generate_test_ballots,
    get_voting_method_info, validate_poll_config, get_supported_methods
)


class TestCandidate(unittest.TestCase):
    """Test Candidate class."""
    
    def test_candidate_creation(self):
        """Test creating a candidate."""
        c = Candidate(id="c1", name="Option A", description="First option")
        self.assertEqual(c.id, "c1")
        self.assertEqual(c.name, "Option A")
        self.assertEqual(c.description, "First option")
    
    def test_candidate_hash(self):
        """Test candidate hashing."""
        c1 = Candidate(id="c1", name="A")
        c2 = Candidate(id="c1", name="B")
        c3 = Candidate(id="c2", name="A")
        
        # Same ID should hash equal
        self.assertEqual(hash(c1), hash(c2))
        # Different ID should hash different
        self.assertNotEqual(hash(c1), hash(c3))
    
    def test_candidate_equality(self):
        """Test candidate equality."""
        c1 = Candidate(id="c1", name="A")
        c2 = Candidate(id="c1", name="B")
        c3 = Candidate(id="c2", name="A")
        
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)


class TestBallot(unittest.TestCase):
    """Test Ballot class."""
    
    def test_ballot_creation(self):
        """Test creating a ballot."""
        b = Ballot(
            voter_id="v1",
            poll_id="p1",
            choices=["c1", "c2"]
        )
        self.assertEqual(b.voter_id, "v1")
        self.assertEqual(b.poll_id, "p1")
        self.assertEqual(b.choices, ["c1", "c2"])
        self.assertIsNotNone(b.timestamp)
        self.assertIsNotNone(b.signature)
    
    def test_ballot_validation(self):
        """Test ballot signature validation."""
        b = Ballot(
            voter_id="v1",
            poll_id="p1",
            choices=["c1"]
        )
        self.assertTrue(b.validate())
        
        # Modify and check validation fails
        b.choices.append("c2")
        self.assertFalse(b.validate())
    
    def test_ballot_with_rankings(self):
        """Test ballot with rankings."""
        rankings = {"c1": 1, "c2": 2, "c3": 3}
        b = Ballot(
            voter_id="v1",
            poll_id="p1",
            choices=["c1"],
            rankings=rankings
        )
        self.assertEqual(b.rankings, rankings)
        self.assertTrue(b.validate())


class TestPoll(unittest.TestCase):
    """Test Poll class."""
    
    def test_poll_creation(self):
        """Test creating a poll."""
        candidates = [
            Candidate(id="c1", name="A"),
            Candidate(id="c2", name="B"),
            Candidate(id="c3", name="C")
        ]
        
        poll = Poll(
            id="poll1",
            title="Test Poll",
            candidates=candidates
        )
        
        self.assertEqual(poll.title, "Test Poll")
        self.assertEqual(len(poll.candidates), 3)
        self.assertEqual(poll.method, VotingMethod.PLURALITY)
        self.assertEqual(poll.status, PollStatus.DRAFT)
    
    def test_poll_get_candidate(self):
        """Test finding candidate by ID."""
        candidates = [
            Candidate(id="c1", name="A"),
            Candidate(id="c2", name="B")
        ]
        poll = Poll(id="p1", title="Test", candidates=candidates)
        
        c = poll.get_candidate_by_id("c1")
        self.assertEqual(c.name, "A")
        
        c = poll.get_candidate_by_id("c3")
        self.assertIsNone(c)
    
    def test_poll_validate_ballot(self):
        """Test ballot validation."""
        candidates = [Candidate(id="c1", name="A"), Candidate(id="c2", name="B")]
        poll = Poll(id="p1", title="Test", candidates=candidates)
        
        # Valid ballot
        b = Ballot(voter_id="v1", poll_id="p1", choices=["c1"])
        valid, msg = poll.validate_ballot(b)
        self.assertTrue(valid)
        
        # Wrong poll ID
        b = Ballot(voter_id="v1", poll_id="p2", choices=["c1"])
        valid, msg = poll.validate_ballot(b)
        self.assertFalse(valid)
        
        # Invalid candidate
        b = Ballot(voter_id="v1", poll_id="p1", choices=["c3"])
        valid, msg = poll.validate_ballot(b)
        self.assertFalse(valid)
    
    def test_poll_auto_id_generation(self):
        """Test automatic ID generation."""
        poll = Poll(id="", title="Test", candidates=[Candidate(id="c1", name="A")])
        self.assertIsNotNone(poll.id)
        self.assertEqual(len(poll.id), 12)


class TestPluralityVoting(unittest.TestCase):
    """Test plurality voting method."""
    
    def test_basic_plurality(self):
        """Test basic plurality counting."""
        candidates = [
            Candidate(id="c1", name="A"),
            Candidate(id="c2", name="B"),
            Candidate(id="c3", name="C")
        ]
        poll = Poll(id="p1", title="Test", candidates=candidates, method=VotingMethod.PLURALITY)
        
        ballots = [
            Ballot(voter_id="v1", poll_id="p1", choices=["c1"]),
            Ballot(voter_id="v2", poll_id="p1", choices=["c1"]),
            Ballot(voter_id="v3", poll_id="p1", choices=["c2"]),
        ]
        
        result = plurality_vote(poll, ballots)
        
        self.assertEqual(result.method, VotingMethod.PLURALITY)
        self.assertEqual(result.total_votes, 3)
        self.assertEqual(len(result.winners), 1)
        self.assertEqual(result.winners[0].id, "c1")
        
        # Check counts
        counts = {c.candidate_id: c.votes for c in result.counts}
        self.assertEqual(counts["c1"], 2)
        self.assertEqual(counts["c2"], 1)
        self.assertEqual(counts["c3"], 0)
    
    def test_plurality_tie(self):
        """Test plurality with tie."""
        candidates = [
            Candidate(id="c1", name="A"),
            Candidate(id="c2", name="B")
        ]
        poll = Poll(id="p1", title="Test", candidates=candidates)
        
        ballots = [
            Ballot(voter_id="v1", poll_id="p1", choices=["c1"]),
            Ballot(voter_id="v2", poll_id="p1", choices=["c2"]),
        ]
        
        result = plurality_vote(poll, ballots)
        
        # Winner should be first in sorted list (alphabetically or by ID)
        self.assertEqual(result.counts[0].votes, 1)
        self.assertEqual(result.counts[1].votes, 1)


class TestApprovalVoting(unittest.TestCase):
    """Test approval voting method."""
    
    def test_basic_approval(self):
        """Test basic approval voting."""
        candidates = [
            Candidate(id="c1", name="A"),
            Candidate(id="c2", name="B"),
            Candidate(id="c3", name="C")
        ]
        poll = Poll(id="p1", title="Test", candidates=candidates, 
                    method=VotingMethod.APPROVAL, max_choices=3)
        
        ballots = [
            Ballot(voter_id="v1", poll_id="p1", choices=["c1", "c2"]),
            Ballot(voter_id="v2", poll_id="p1", choices=["c1", "c3"]),
            Ballot(voter_id="v3", poll_id="p1", choices=["c2"]),
        ]
        
        result = approval_vote(poll, ballots)
        
        self.assertEqual(result.method, VotingMethod.APPROVAL)
        
        # Check counts (approvals)
        counts = {c.candidate_id: c.votes for c in result.counts}
        self.assertEqual(counts["c1"], 2)
        self.assertEqual(counts["c2"], 2)
        self.assertEqual(counts["c3"], 1)
    
    def test_approval_max_choices(self):
        """Test approval with max choices limit."""
        candidates = [
            Candidate(id="c1", name="A"),
            Candidate(id="c2", name="B"),
            Candidate(id="c3", name="C")
        ]
        poll = Poll(id="p1", title="Test", candidates=candidates, 
                    method=VotingMethod.APPROVAL, max_choices=2)
        
        # Valid ballots within limit
        ballots = [
            Ballot(voter_id="v1", poll_id="p1", choices=["c1", "c2"]),
            Ballot(voter_id="v2", poll_id="p1", choices=["c1"]),
        ]
        
        # Validate should reject ballots over limit
        b_over = Ballot(voter_id="v3", poll_id="p1", choices=["c1", "c2", "c3"])
        valid, msg = poll.validate_ballot(b_over)
        self.assertFalse(valid)


class TestRankedChoiceVoting(unittest.TestCase):
    """Test ranked choice (IRV) voting."""
    
    def test_basic_ranked_choice(self):
        """Test basic ranked choice with clear winner."""
        candidates = [
            Candidate(id="c1", name="A"),
            Candidate(id="c2", name="B"),
            Candidate(id="c3", name="C")
        ]
        poll = Poll(id="p1", title="Test", candidates=candidates, method=VotingMethod.RANKED_CHOICE)
        
        # A has majority in first round
        ballots = [
            Ballot(voter_id="v1", poll_id="p1", choices=[], rankings={"c1": 1, "c2": 2, "c3": 3}),
            Ballot(voter_id="v2", poll_id="p1", choices=[], rankings={"c1": 1, "c2": 2, "c3": 3}),
            Ballot(voter_id="v3", poll_id="p1", choices=[], rankings={"c2": 1, "c1": 2, "c3": 3}),
            Ballot(voter_id="v4", poll_id="p1", choices=[], rankings={"c3": 1, "c2": 2, "c1": 3}),
            Ballot(voter_id="v5", poll_id="p1", choices=[], rankings={"c1": 1, "c3": 2, "c2": 3}),
        ]
        
        result = ranked_choice_vote(poll, ballots)
        
        self.assertEqual(result.method, VotingMethod.RANKED_CHOICE)
        self.assertIsNotNone(result.rounds)
        self.assertEqual(len(result.rounds), 1)  # Should win in first round (majority)
        self.assertEqual(result.winners[0].id, "c1")
    
    def test_ranked_choice_elimination(self):
        """Test ranked choice with elimination rounds."""
        candidates = [
            Candidate(id="c1", name="A"),
            Candidate(id="c2", name="B"),
            Candidate(id="c3", name="C")
        ]
        poll = Poll(id="p1", title="Test", candidates=candidates, method=VotingMethod.RANKED_CHOICE)
        
        # No majority first round, C eliminated, votes transfer
        ballots = [
            Ballot(voter_id="v1", poll_id="p1", choices=[], rankings={"c1": 1, "c2": 2, "c3": 3}),
            Ballot(voter_id="v2", poll_id="p1", choices=[], rankings={"c2": 1, "c1": 2, "c3": 3}),
            Ballot(voter_id="v3", poll_id="p1", choices=[], rankings={"c2": 1, "c3": 2, "c1": 3}),
            Ballot(voter_id="v4", poll_id="p1", choices=[], rankings={"c3": 1, "c1": 2, "c2": 3}),
        ]
        
        result = ranked_choice_vote(poll, ballots)
        
        # Should have multiple rounds
        self.assertGreater(len(result.rounds), 1)
        
        # Check that someone won
        self.assertEqual(len(result.winners), 1)


class TestBordaCount(unittest.TestCase):
    """Test Borda count voting."""
    
    def test_basic_borda(self):
        """Test basic Borda count."""
        candidates = [
            Candidate(id="c1", name="A"),
            Candidate(id="c2", name="B"),
            Candidate(id="c3", name="C")
        ]
        poll = Poll(id="p1", title="Test", candidates=candidates, method=VotingMethod.BORDA)
        
        ballots = [
            Ballot(voter_id="v1", poll_id="p1", choices=[], rankings={"c1": 1, "c2": 2, "c3": 3}),
            Ballot(voter_id="v2", poll_id="p1", choices=[], rankings={"c2": 1, "c1": 2, "c3": 3}),
            Ballot(voter_id="v3", poll_id="p1", choices=[], rankings={"c1": 1, "c3": 2, "c2": 3}),
        ]
        
        result = borda_count(poll, ballots)
        
        self.assertEqual(result.method, VotingMethod.BORDA)
        
        # Borda scores: n-rank, so 1st gets 2, 2nd gets 1, 3rd gets 0
        # c1: 2+1+2 = 5
        # c2: 1+2+0 = 3
        # c3: 0+0+1 = 1
        
        counts = {c.candidate_id: c.votes for c in result.counts}
        self.assertEqual(counts["c1"], 5)
        self.assertEqual(counts["c2"], 3)
        self.assertEqual(counts["c3"], 1)
        self.assertEqual(result.winners[0].id, "c1")


class TestCondorcetVoting(unittest.TestCase):
    """Test Condorcet voting."""
    
    def test_condorcet_winner(self):
        """Test with clear Condorcet winner."""
        candidates = [
            Candidate(id="c1", name="A"),
            Candidate(id="c2", name="B"),
            Candidate(id="c3", name="C")
        ]
        poll = Poll(id="p1", title="Test", candidates=candidates, method=VotingMethod.CONDORCET)
        
        # A beats everyone pairwise
        ballots = [
            Ballot(voter_id="v1", poll_id="p1", choices=[], rankings={"c1": 1, "c2": 2, "c3": 3}),
            Ballot(voter_id="v2", poll_id="p1", choices=[], rankings={"c1": 1, "c3": 2, "c2": 3}),
            Ballot(voter_id="v3", poll_id="p1", choices=[], rankings={"c2": 1, "c1": 2, "c3": 3}),
        ]
        
        result = condorcet_vote(poll, ballots)
        
        self.assertEqual(result.method, VotingMethod.CONDORCET)
        self.assertTrue(result.metadata["condorcet_winner_exists"])
        self.assertEqual(result.winners[0].id, "c1")
    
    def test_condorcet_cycle(self):
        """Test Condorcet cycle (no clear winner)."""
        candidates = [
            Candidate(id="c1", name="A"),
            Candidate(id="c2", name="B"),
            Candidate(id="c3", name="C")
        ]
        poll = Poll(id="p1", title="Test", candidates=candidates, method=VotingMethod.CONDORCET)
        
        # Create a Condorcet cycle: A>B, B>C, C>A (each by 2-1)
        # Use 9 voters for cleaner numbers
        ballots = [
            # 3 voters: A > B > C (A beats B 3-0, A beats C 3-0)
            Ballot(voter_id="v1", poll_id="p1", choices=[], rankings={"c1": 1, "c2": 2, "c3": 3}),
            Ballot(voter_id="v2", poll_id="p1", choices=[], rankings={"c1": 1, "c2": 2, "c3": 3}),
            Ballot(voter_id="v3", poll_id="p1", choices=[], rankings={"c1": 1, "c2": 2, "c3": 3}),
            # 3 voters: B > C > A (B beats C 3-0, B beats A 3-0)
            Ballot(voter_id="v4", poll_id="p1", choices=[], rankings={"c2": 1, "c3": 2, "c1": 3}),
            Ballot(voter_id="v5", poll_id="p1", choices=[], rankings={"c2": 1, "c3": 2, "c1": 3}),
            Ballot(voter_id="v6", poll_id="p1", choices=[], rankings={"c2": 1, "c3": 2, "c1": 3}),
            # 3 voters: C > A > B (C beats A 3-0, C beats B 3-0)
            Ballot(voter_id="v7", poll_id="p1", choices=[], rankings={"c3": 1, "c1": 2, "c2": 3}),
            Ballot(voter_id="v8", poll_id="p1", choices=[], rankings={"c3": 1, "c1": 2, "c2": 3}),
            Ballot(voter_id="v9", poll_id="p1", choices=[], rankings={"c3": 1, "c1": 2, "c2": 3}),
        ]
        
        # Pairwise results:
        # A vs B: 6 voters prefer A (v1-v3, v7-v9), 3 prefer B (v4-v6) -> A wins 6-3
        # B vs C: 6 voters prefer B (v1-v3, v4-v6), 3 prefer C (v7-v9) -> B wins 6-3
        # A vs C: 3 voters prefer A (v1-v3), 6 prefer C (v4-v6, v7-v9) -> C wins 6-3
        # Cycle: A>B, B>C, C>A - no Condorcet winner
        
        result = condorcet_vote(poll, ballots)
        
        # No Condorcet winner, should use Copeland
        self.assertFalse(result.metadata["condorcet_winner_exists"])
        self.assertEqual(result.metadata["resolution_method"], "copeland")
        
        # Should still have a winner via Copeland (each wins 1 pairwise, ties resolved by copeland)
        self.assertEqual(len(result.winners), 1)


class TestScoreVoting(unittest.TestCase):
    """Test score/range voting."""
    
    def test_basic_score(self):
        """Test basic score voting."""
        candidates = [
            Candidate(id="c1", name="A"),
            Candidate(id="c2", name="B"),
            Candidate(id="c3", name="C")
        ]
        poll = Poll(id="p1", title="Test", candidates=candidates, 
                    method=VotingMethod.SCORE, min_score=0, max_score=5)
        
        ballots = [
            Ballot(voter_id="v1", poll_id="p1", choices=[], scores={"c1": 5, "c2": 3, "c3": 0}),
            Ballot(voter_id="v2", poll_id="p1", choices=[], scores={"c1": 4, "c2": 4, "c3": 1}),
            Ballot(voter_id="v3", poll_id="p1", choices=[], scores={"c1": 5, "c2": 2, "c3": 2}),
        ]
        
        result = score_vote(poll, ballots)
        
        self.assertEqual(result.method, VotingMethod.SCORE)
        
        # Total scores: c1=14, c2=9, c3=3
        counts = {c.candidate_id: c.votes for c in result.counts}
        self.assertEqual(counts["c1"], 14)
        self.assertEqual(counts["c2"], 9)
        self.assertEqual(counts["c3"], 3)
        self.assertEqual(result.winners[0].id, "c1")


class TestSTVVoting(unittest.TestCase):
    """Test Single Transferable Vote."""
    
    def test_basic_stv(self):
        """Test basic STV for single seat (same as IRV)."""
        candidates = [
            Candidate(id="c1", name="A"),
            Candidate(id="c2", name="B"),
            Candidate(id="c3", name="C")
        ]
        poll = Poll(id="p1", title="Test", candidates=candidates, 
                    method=VotingMethod.STV, seats=1)
        
        ballots = [
            Ballot(voter_id="v1", poll_id="p1", choices=[], rankings={"c1": 1, "c2": 2, "c3": 3}),
            Ballot(voter_id="v2", poll_id="p1", choices=[], rankings={"c1": 1, "c2": 2, "c3": 3}),
            Ballot(voter_id="v3", poll_id="p1", choices=[], rankings={"c2": 1, "c1": 2, "c3": 3}),
        ]
        
        result = stv_vote(poll, ballots)
        
        self.assertEqual(result.method, VotingMethod.STV)
        self.assertEqual(len(result.winners), 1)
        self.assertEqual(result.metadata["seats"], 1)
    
    def test_multi_seat_stv(self):
        """Test STV for multiple seats."""
        candidates = [
            Candidate(id="c1", name="A"),
            Candidate(id="c2", name="B"),
            Candidate(id="c3", name="C"),
            Candidate(id="c4", name="D")
        ]
        poll = Poll(id="p1", title="Test", candidates=candidates, 
                    method=VotingMethod.STV, seats=2)
        
        ballots = []
        for i in range(10):
            rankings = {}
            shuffled = ["c1", "c2", "c3", "c4"]
            import random
            random.shuffle(shuffled)
            for rank, cid in enumerate(shuffled, 1):
                rankings[cid] = rank
            ballots.append(Ballot(voter_id=f"v{i}", poll_id="p1", choices=[], rankings=rankings))
        
        result = stv_vote(poll, ballots)
        
        self.assertEqual(result.method, VotingMethod.STV)
        self.assertEqual(len(result.winners), 2)
        self.assertEqual(result.metadata["seats"], 2)


class TestHelperFunctions(unittest.TestCase):
    """Test helper functions."""
    
    def test_create_poll(self):
        """Test poll creation helper."""
        poll = create_poll(
            "Test Poll",
            ["Option A", "Option B", "Option C"],
            method=VotingMethod.APPROVAL
        )
        
        self.assertEqual(poll.title, "Test Poll")
        self.assertEqual(len(poll.candidates), 3)
        self.assertEqual(poll.method, VotingMethod.APPROVAL)
        self.assertIsNotNone(poll.id)
    
    def test_create_ballot(self):
        """Test ballot creation helper."""
        ballot = create_ballot(
            poll_id="p1",
            voter_id="v1",
            choices=["c1", "c2"]
        )
        
        self.assertEqual(ballot.poll_id, "p1")
        self.assertEqual(ballot.voter_id, "v1")
        self.assertEqual(ballot.choices, ["c1", "c2"])
    
    def test_generate_test_ballots(self):
        """Test test ballot generation."""
        poll = create_poll("Test", ["A", "B", "C"], method=VotingMethod.PLURALITY)
        ballots = generate_test_ballots(poll, 50)
        
        self.assertEqual(len(ballots), 50)
        for b in ballots:
            self.assertEqual(b.poll_id, poll.id)
            self.assertEqual(len(b.choices), 1)
    
    def test_generate_ranked_ballots(self):
        """Test generating ranked ballots."""
        poll = create_poll("Test", ["A", "B", "C"], method=VotingMethod.RANKED_CHOICE)
        ballots = generate_test_ballots(poll, 10)
        
        for b in ballots:
            self.assertIsNotNone(b.rankings)
            self.assertEqual(len(b.rankings), 3)
    
    def test_get_voting_method_info(self):
        """Test method info retrieval."""
        info = get_voting_method_info(VotingMethod.PLURALITY)
        
        self.assertIn("name", info)
        self.assertIn("description", info)
        self.assertIn("pros", info)
        self.assertIn("cons", info)
    
    def test_validate_poll_config(self):
        """Test poll config validation."""
        # Valid poll
        poll = create_poll("Test", ["A", "B"])
        valid, issues = validate_poll_config(poll)
        self.assertTrue(valid)
        self.assertEqual(len(issues), 0)
        
        # Invalid: too few candidates
        candidates = [Candidate(id="c1", name="A")]
        poll = Poll(id="p1", title="Test", candidates=candidates)
        valid, issues = validate_poll_config(poll)
        self.assertFalse(valid)
        self.assertIn("At least 2 candidates required", issues)
    
    def test_get_supported_methods(self):
        """Test getting supported methods."""
        methods = get_supported_methods()
        
        self.assertIn(VotingMethod.PLURALITY, methods)
        self.assertIn(VotingMethod.RANKED_CHOICE, methods)
        self.assertIn(VotingMethod.STV, methods)


class TestCountVotes(unittest.TestCase):
    """Test unified count_votes function."""
    
    def test_count_votes_routing(self):
        """Test count_votes routes to correct method."""
        poll = create_poll("Test", ["A", "B"], method=VotingMethod.PLURALITY)
        ballots = generate_test_ballots(poll, 20)
        
        result = count_votes(poll, ballots)
        self.assertEqual(result.method, VotingMethod.PLURALITY)
        
        poll.method = VotingMethod.APPROVAL
        ballots = generate_test_ballots(poll, 20)
        result = count_votes(poll, ballots)
        self.assertEqual(result.method, VotingMethod.APPROVAL)
    
    def test_count_votes_invalid_ballot(self):
        """Test count_votes rejects invalid ballots."""
        poll = create_poll("Test", ["A", "B"])
        
        # Ballot with invalid candidate
        ballot = Ballot(voter_id="v1", poll_id=poll.id, choices=["invalid_id"])
        
        with self.assertRaises(ValueError):
            count_votes(poll, [ballot])


class TestElectionResult(unittest.TestCase):
    """Test ElectionResult class."""
    
    def test_result_summary(self):
        """Test result summary generation."""
        poll = create_poll("Test", ["A", "B", "C"])
        ballots = generate_test_ballots(poll, 10)
        result = count_votes(poll, ballots)
        
        summary = result.to_summary()
        
        self.assertIn("Test", summary)
        self.assertIn("plurality", summary)
        self.assertIn("Total Votes: 10", summary)
    
    def test_get_winner(self):
        """Test getting winner from result."""
        poll = create_poll("Test", ["A", "B"])
        ballots = generate_test_ballots(poll, 5)
        result = count_votes(poll, ballots)
        
        winner = result.get_winner()
        self.assertIsNotNone(winner)


if __name__ == '__main__':
    unittest.main(verbosity=2)