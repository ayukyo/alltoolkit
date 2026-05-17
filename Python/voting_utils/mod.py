#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Voting Utilities Module

Comprehensive voting and poll utilities for Python with zero external dependencies.
Supports multiple voting methods including plurality, ranked choice (instant runoff),
Borda count, approval voting, and proportional representation calculations.

Author: AllToolkit
License: MIT
"""

import random
import hashlib
from typing import List, Dict, Any, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


# =============================================================================
# Enums
# =============================================================================

class VotingMethod(Enum):
    """Voting method types."""
    PLURALITY = "plurality"           # Single choice, most votes wins
    APPROVAL = "approval"              # Multiple choices allowed
    RANKED_CHOICE = "ranked_choice"    # Instant runoff voting (IRV)
    BORDA = "borda"                    # Borda count method
    STV = "stv"                        # Single transferable vote (proportional)
    CONDORCET = "condorcet"            # Condorcet method (pairwise comparison)
    SCORE = "score"                    # Score/range voting


class PollStatus(Enum):
    """Poll status."""
    DRAFT = "draft"
    OPEN = "open"
    CLOSED = "closed"
    TALLYING = "tallying"
    FINALIZED = "finalized"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class Candidate:
    """Poll candidate/option."""
    id: str
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, Candidate):
            return self.id == other.id
        return False


@dataclass
class Ballot:
    """A single voter's ballot."""
    voter_id: str
    poll_id: str
    choices: List[str]  # For plurality/approval: list of candidate ids
    rankings: Optional[Dict[str, int]] = None  # For ranked methods: {candidate_id: rank}
    scores: Optional[Dict[str, int]] = None  # For score voting: {candidate_id: score}
    timestamp: Optional[float] = None
    signature: Optional[str] = None  # Hash for verification
    
    def __post_init__(self):
        if self.timestamp is None:
            import time
            self.timestamp = time.time()
        if self.signature is None:
            self.signature = self._generate_signature()
    
    def _generate_signature(self) -> str:
        """Generate ballot signature for verification."""
        data = f"{self.voter_id}:{self.poll_id}:{','.join(self.choices)}"
        if self.rankings:
            data += f":{','.join(f'{k}={v}' for k, v in sorted(self.rankings.items()))}"
        if self.scores:
            data += f":{','.join(f'{k}={v}' for k, v in sorted(self.scores.items()))}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def validate(self) -> bool:
        """Validate ballot integrity."""
        return self.signature == self._generate_signature()


@dataclass
class Poll:
    """Poll definition."""
    id: str
    title: str
    candidates: List[Candidate]  # Must be before any default fields
    description: Optional[str] = None
    method: VotingMethod = VotingMethod.PLURALITY
    status: PollStatus = PollStatus.DRAFT
    max_choices: int = 1  # For approval voting
    min_score: int = 0  # For score voting
    max_score: int = 5  # For score voting
    seats: int = 1  # For STV (multi-seat elections)
    created_at: Optional[float] = None
    closes_at: Optional[float] = None
    allow_anonymous: bool = False
    require_verification: bool = False
    
    def __post_init__(self):
        if self.created_at is None:
            import time
            self.created_at = time.time()
        if self.id is None or self.id == "":
            self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique poll ID."""
        import time
        data = f"{self.title}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:12]
    
    def get_candidate_by_id(self, candidate_id: str) -> Optional[Candidate]:
        """Find candidate by ID."""
        for c in self.candidates:
            if c.id == candidate_id:
                return c
        return None
    
    def validate_ballot(self, ballot: Ballot) -> Tuple[bool, str]:
        """Validate a ballot against poll rules."""
        # Check poll ID matches
        if ballot.poll_id != self.id:
            return False, "Poll ID mismatch"
        
        # Check all choices are valid candidates
        for choice in ballot.choices:
            if self.get_candidate_by_id(choice) is None:
                return False, f"Invalid candidate: {choice}"
        
        # Check max choices for approval voting
        if self.method == VotingMethod.APPROVAL and len(ballot.choices) > self.max_choices:
            return False, f"Too many choices (max: {self.max_choices})"
        
        # Check rankings for ranked methods
        if self.method in [VotingMethod.RANKED_CHOICE, VotingMethod.BORDA, VotingMethod.STV]:
            if ballot.rankings is None:
                return False, "Rankings required for this voting method"
            for cid in ballot.rankings:
                if self.get_candidate_by_id(cid) is None:
                    return False, f"Invalid candidate in rankings: {cid}"
        
        # Check scores for score voting
        if self.method == VotingMethod.SCORE:
            if ballot.scores is None:
                return False, "Scores required for score voting"
            for cid, score in ballot.scores.items():
                if self.get_candidate_by_id(cid) is None:
                    return False, f"Invalid candidate in scores: {cid}"
                if score < self.min_score or score > self.max_score:
                    return False, f"Score out of range: {score}"
        
        return True, "Valid"


@dataclass
class VoteCount:
    """Vote count for a candidate."""
    candidate_id: str
    candidate_name: str
    votes: int = 0
    percentage: float = 0.0
    rank: int = 0
    eliminated: bool = False
    transferred_votes: int = 0  # For STV/IRV


@dataclass
class ElectionResult:
    """Election/poll result."""
    poll_id: str
    poll_title: str
    method: VotingMethod
    winners: List[Candidate]
    counts: List[VoteCount]
    total_votes: int
    rounds: Optional[List[Dict[str, Any]]] = None  # For multi-round methods
    pairwise_matrix: Optional[Dict[str, Dict[str, int]]] = None  # For Condorcet
    finalized_at: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.finalized_at is None:
            import time
            self.finalized_at = time.time()
    
    def get_winner(self) -> Optional[Candidate]:
        """Get the winner (first place)."""
        if self.winners:
            return self.winners[0]
        return None
    
    def to_summary(self) -> str:
        """Generate text summary of results."""
        lines = [
            f"=== {self.poll_title} ===",
            f"Method: {self.method.value}",
            f"Total Votes: {self.total_votes}",
            "",
            "Results:",
        ]
        for count in sorted(self.counts, key=lambda c: c.rank):
            status = " [WINNER]" if count.candidate_id in [w.id for w in self.winners] else ""
            if count.eliminated:
                status = " [ELIMINATED]"
            lines.append(f"  {count.rank}. {count.candidate_name}: {count.votes} ({count.percentage:.1f}%){status}")
        
        return "\n".join(lines)


# =============================================================================
# Voting Methods Implementation
# =============================================================================

def plurality_vote(poll: Poll, ballots: List[Ballot]) -> ElectionResult:
    """
    Plurality voting (first-past-the-post).
    
    Each voter selects one candidate. The candidate with the most votes wins.
    
    Args:
        poll: Poll definition
        ballots: List of submitted ballots
        
    Returns:
        ElectionResult with winner and vote counts
    """
    # Count votes
    counts = defaultdict(int)
    for ballot in ballots:
        for choice in ballot.choices:
            counts[choice] += 1
    
    total_votes = len(ballots)
    
    # Build result counts
    vote_counts = []
    for candidate in poll.candidates:
        vc = VoteCount(
            candidate_id=candidate.id,
            candidate_name=candidate.name,
            votes=counts.get(candidate.id, 0),
            percentage=(counts.get(candidate.id, 0) / total_votes * 100) if total_votes > 0 else 0
        )
        vote_counts.append(vc)
    
    # Sort by votes
    vote_counts.sort(key=lambda vc: vc.votes, reverse=True)
    
    # Assign ranks
    for i, vc in enumerate(vote_counts):
        vc.rank = i + 1
    
    # Determine winner
    winner = poll.get_candidate_by_id(vote_counts[0].candidate_id)
    
    return ElectionResult(
        poll_id=poll.id,
        poll_title=poll.title,
        method=VotingMethod.PLURALITY,
        winners=[winner] if winner else [],
        counts=vote_counts,
        total_votes=total_votes
    )


def approval_vote(poll: Poll, ballots: List[Ballot]) -> ElectionResult:
    """
    Approval voting.
    
    Each voter can approve multiple candidates. The candidate with the most
    approvals wins. This method tends to elect consensus candidates.
    
    Args:
        poll: Poll definition
        ballots: List of submitted ballots
        
    Returns:
        ElectionResult with winner and approval counts
    """
    # Count approvals
    counts = defaultdict(int)
    for ballot in ballots:
        for choice in ballot.choices:
            counts[choice] += 1
    
    total_ballots = len(ballots)
    
    # Build result counts
    vote_counts = []
    for candidate in poll.candidates:
        approvals = counts.get(candidate.id, 0)
        vc = VoteCount(
            candidate_id=candidate.id,
            candidate_name=candidate.name,
            votes=approvals,
            percentage=(approvals / total_ballots * 100) if total_ballots > 0 else 0
        )
        vote_counts.append(vc)
    
    # Sort by approvals
    vote_counts.sort(key=lambda vc: vc.votes, reverse=True)
    
    # Assign ranks
    for i, vc in enumerate(vote_counts):
        vc.rank = i + 1
    
    # Determine winner (candidate with most approvals)
    winner = poll.get_candidate_by_id(vote_counts[0].candidate_id)
    
    return ElectionResult(
        poll_id=poll.id,
        poll_title=poll.title,
        method=VotingMethod.APPROVAL,
        winners=[winner] if winner else [],
        counts=vote_counts,
        total_votes=total_ballots,
        metadata={"total_approvals": sum(counts.values())}
    )


def borda_count(poll: Poll, ballots: List[Ballot]) -> ElectionResult:
    """
    Borda count voting.
    
    Each voter ranks all candidates. Points are assigned based on position:
    n-1 points for first choice, n-2 for second, etc. The candidate with
    the highest total points wins.
    
    Args:
        poll: Poll definition
        ballots: List of submitted ballots
        
    Returns:
        ElectionResult with winner and Borda scores
    """
    n = len(poll.candidates)
    
    # Calculate Borda scores
    scores = defaultdict(int)
    for ballot in ballots:
        if ballot.rankings:
            for candidate_id, rank in ballot.rankings.items():
                # Borda points: n - rank (1st gets n-1, 2nd gets n-2, etc.)
                points = n - rank
                scores[candidate_id] += points
    
    total_ballots = len(ballots)
    
    # Build result counts (using Borda scores as "votes")
    vote_counts = []
    for candidate in poll.candidates:
        borda_score = scores.get(candidate.id, 0)
        max_possible = total_ballots * (n - 1)
        vc = VoteCount(
            candidate_id=candidate.id,
            candidate_name=candidate.name,
            votes=borda_score,
            percentage=(borda_score / max_possible * 100) if max_possible > 0 else 0
        )
        vote_counts.append(vc)
    
    # Sort by Borda score
    vote_counts.sort(key=lambda vc: vc.votes, reverse=True)
    
    # Assign ranks
    for i, vc in enumerate(vote_counts):
        vc.rank = i + 1
    
    # Determine winner
    winner = poll.get_candidate_by_id(vote_counts[0].candidate_id)
    
    return ElectionResult(
        poll_id=poll.id,
        poll_title=poll.title,
        method=VotingMethod.BORDA,
        winners=[winner] if winner else [],
        counts=vote_counts,
        total_votes=total_ballots,
        metadata={"max_borda_score": (n - 1) * total_ballots}
    )


def ranked_choice_vote(poll: Poll, ballots: List[Ballot]) -> ElectionResult:
    """
    Ranked choice voting (Instant Runoff Voting - IRV).
    
    Voters rank candidates by preference. If no candidate has a majority,
    the lowest-ranked candidate is eliminated and their votes are transferred
    to voters' next preferences. Process repeats until a candidate has majority.
    
    Args:
        poll: Poll definition
        ballots: List of submitted ballots
        
    Returns:
        ElectionResult with winner and round-by-round results
    """
    rounds = []
    active_candidates = set(c.id for c in poll.candidates)
    total_votes = len(ballots)
    
    # Create mutable ballot copies with current rankings
    ballot_rankings = []
    for ballot in ballots:
        if ballot.rankings:
            # Sort by rank and filter active candidates
            sorted_choices = sorted(
                [(cid, rank) for cid, rank in ballot.rankings.items() if cid in active_candidates],
                key=lambda x: x[1]
            )
            ballot_rankings.append([cid for cid, _ in sorted_choices])
        else:
            ballot_rankings.append([])
    
    round_num = 1
    while True:
        # Count current top choices
        counts = defaultdict(int)
        for choices in ballot_rankings:
            if choices:
                counts[choices[0]] += 1
        
        # Build round result
        round_counts = {}
        for cid in active_candidates:
            round_counts[cid] = counts.get(cid, 0)
        
        # Find max votes
        max_votes = max(round_counts.values()) if round_counts else 0
        majority_threshold = total_votes / 2
        
        rounds.append({
            "round": round_num,
            "counts": round_counts.copy(),
            "active_candidates": list(active_candidates),
            "max_votes": max_votes,
            "majority_threshold": majority_threshold,
            "has_majority": max_votes > majority_threshold
        })
        
        # Check if winner found
        if max_votes > majority_threshold:
            # Find winner
            winner_id = max(round_counts, key=round_counts.get)
            break
        
        # Eliminate candidate with fewest votes
        min_votes = min(round_counts.values()) if round_counts else 0
        
        # Handle tie (eliminate randomly or lowest first-choice support)
        candidates_to_eliminate = [cid for cid, v in round_counts.items() if v == min_votes]
        
        if len(candidates_to_eliminate) == len(active_candidates):
            # All tied - pick randomly
            winner_id = random.choice(list(active_candidates))
            break
        
        # Eliminate one candidate
        eliminated_id = candidates_to_eliminate[0]
        active_candidates.remove(eliminated_id)
        
        # Transfer votes - remove eliminated from ballots
        for choices in ballot_rankings:
            if eliminated_id in choices:
                choices.remove(eliminated_id)
        
        round_num += 1
    
    # Build final result counts
    vote_counts = []
    final_counts = rounds[-1]["counts"]
    for i, candidate in enumerate(poll.candidates):
        is_winner = candidate.id == winner_id
        vc = VoteCount(
            candidate_id=candidate.id,
            candidate_name=candidate.name,
            votes=final_counts.get(candidate.id, 0),
            percentage=(final_counts.get(candidate.id, 0) / total_votes * 100) if total_votes > 0 else 0,
            eliminated=candidate.id not in active_candidates and not is_winner
        )
        vote_counts.append(vc)
    
    # Sort by final votes
    vote_counts.sort(key=lambda vc: vc.votes, reverse=True)
    
    # Assign ranks
    rank = 1
    for vc in vote_counts:
        if not vc.eliminated:
            vc.rank = rank
            rank += 1
        else:
            vc.rank = len(poll.candidates)
    
    winner = poll.get_candidate_by_id(winner_id)
    
    return ElectionResult(
        poll_id=poll.id,
        poll_title=poll.title,
        method=VotingMethod.RANKED_CHOICE,
        winners=[winner] if winner else [],
        counts=vote_counts,
        total_votes=total_votes,
        rounds=rounds
    )


def condorcet_vote(poll: Poll, ballots: List[Ballot]) -> ElectionResult:
    """
    Condorcet voting (pairwise comparison).
    
    Each candidate is compared head-to-head against every other candidate.
    A Condorcet winner beats all other candidates in pairwise comparisons.
    If no Condorcet winner exists (cycle), various methods can resolve it.
    
    Args:
        poll: Poll definition
        ballots: List of submitted ballots
        
    Returns:
        ElectionResult with winner and pairwise matrix
    """
    n = len(poll.candidates)
    
    # Build pairwise comparison matrix
    # pairwise_matrix[a][b] = number of ballots where a is preferred over b
    pairwise_matrix: Dict[str, Dict[str, int]] = {}
    for c1 in poll.candidates:
        pairwise_matrix[c1.id] = {}
        for c2 in poll.candidates:
            if c1.id != c2.id:
                pairwise_matrix[c1.id][c2.id] = 0
    
    # Process each ballot
    for ballot in ballots:
        if ballot.rankings:
            for c1 in poll.candidates:
                for c2 in poll.candidates:
                    if c1.id != c2.id:
                        rank1 = ballot.rankings.get(c1.id, n + 1)
                        rank2 = ballot.rankings.get(c2.id, n + 1)
                        if rank1 < rank2:
                            pairwise_matrix[c1.id][c2.id] += 1
    
    # Find Condorcet winner
    condorcet_winner_id = None
    is_condorcet_winner = False  # Track whether winner was found via Condorcet or Copeland
    for candidate in poll.candidates:
        wins_all = True
        for other in poll.candidates:
            if candidate.id != other.id:
                wins = pairwise_matrix[candidate.id][other.id]
                loses = pairwise_matrix[other.id][candidate.id]
                if wins <= loses:
                    wins_all = False
                    break
        if wins_all:
            condorcet_winner_id = candidate.id
            is_condorcet_winner = True
            break
    
    # If no Condorcet winner, use Copeland's method (most pairwise wins)
    if condorcet_winner_id is None:
        copeland_scores = {}
        for candidate in poll.candidates:
            wins = 0
            for other in poll.candidates:
                if candidate.id != other.id:
                    if pairwise_matrix[candidate.id][other.id] > pairwise_matrix[other.id][candidate.id]:
                        wins += 1
            copeland_scores[candidate.id] = wins
        
        # Find candidate with most wins
        condorcet_winner_id = max(copeland_scores, key=copeland_scores.get)
    
    # Build result counts
    vote_counts = []
    total_votes = len(ballots)
    
    # Calculate Copeland scores for all candidates
    copeland_scores = {}
    for candidate in poll.candidates:
        wins = 0
        ties = 0
        for other in poll.candidates:
            if candidate.id != other.id:
                w = pairwise_matrix[candidate.id][other.id]
                l = pairwise_matrix[other.id][candidate.id]
                if w > l:
                    wins += 1
                elif w == l:
                    ties += 1
        copeland_scores[candidate.id] = wins
    
    for candidate in poll.candidates:
        vc = VoteCount(
            candidate_id=candidate.id,
            candidate_name=candidate.name,
            votes=copeland_scores[candidate.id],
            percentage=(copeland_scores[candidate.id] / (n - 1) * 100),
        )
        vote_counts.append(vc)
    
    # Sort by Copeland score
    vote_counts.sort(key=lambda vc: vc.votes, reverse=True)
    
    # Assign ranks
    for i, vc in enumerate(vote_counts):
        vc.rank = i + 1
    
    winner = poll.get_candidate_by_id(condorcet_winner_id)
    
    return ElectionResult(
        poll_id=poll.id,
        poll_title=poll.title,
        method=VotingMethod.CONDORCET,
        winners=[winner] if winner else [],
        counts=vote_counts,
        total_votes=total_votes,
        pairwise_matrix=pairwise_matrix,
        metadata={
            "condorcet_winner_exists": is_condorcet_winner,
            "resolution_method": "copeland" if not is_condorcet_winner else "condorcet"
        }
    )


def score_vote(poll: Poll, ballots: List[Ballot]) -> ElectionResult:
    """
    Score voting (range voting).
    
    Each voter gives each candidate a score within a range (e.g., 0-5).
    The candidate with the highest average (or total) score wins.
    
    Args:
        poll: Poll definition
        ballots: List of submitted ballots
        
    Returns:
        ElectionResult with winner and average scores
    """
    # Calculate total scores
    scores = defaultdict(int)
    score_counts = defaultdict(int)  # Number of voters who scored each candidate
    
    for ballot in ballots:
        if ballot.scores:
            for candidate_id, score in ballot.scores.items():
                scores[candidate_id] += score
                score_counts[candidate_id] += 1
    
    total_ballots = len(ballots)
    
    # Build result counts
    vote_counts = []
    for candidate in poll.candidates:
        total_score = scores.get(candidate.id, 0)
        num_scorers = score_counts.get(candidate.id, 0)
        avg_score = total_score / num_scorers if num_scorers > 0 else 0
        vc = VoteCount(
            candidate_id=candidate.id,
            candidate_name=candidate.name,
            votes=int(total_score),  # Use total score as "votes"
            percentage=(avg_score / poll.max_score * 100),
        )
        vote_counts.append(vc)
    
    # Sort by average score (stored in percentage calculation)
    vote_counts.sort(key=lambda vc: vc.votes / max(1, score_counts.get(vc.candidate_id, 1)), reverse=True)
    
    # Assign ranks
    for i, vc in enumerate(vote_counts):
        vc.rank = i + 1
    
    # Determine winner (highest total score)
    winner = poll.get_candidate_by_id(vote_counts[0].candidate_id)
    
    return ElectionResult(
        poll_id=poll.id,
        poll_title=poll.title,
        method=VotingMethod.SCORE,
        winners=[winner] if winner else [],
        counts=vote_counts,
        total_votes=total_ballots,
        metadata={
            "min_score": poll.min_score,
            "max_score": poll.max_score,
            "score_range": f"{poll.min_score}-{poll.max_score}"
        }
    )


def stv_vote(poll: Poll, ballots: List[Ballot]) -> ElectionResult:
    """
    Single Transferable Vote (STV) for multi-seat elections.
    
    Uses the Droop quota: quota = floor(votes / (seats + 1)) + 1
    Candidates reaching quota are elected. Surplus votes are transferred.
    
    Args:
        poll: Poll definition
        ballots: List of submitted ballots
        
    Returns:
        ElectionResult with winners (multiple for multi-seat)
    """
    seats = poll.seats
    total_votes = len(ballots)
    droop_quota = total_votes // (seats + 1) + 1
    
    rounds = []
    elected: List[str] = []
    eliminated: List[str] = []
    active_candidates = set(c.id for c in poll.candidates)
    
    # Track vote value for each ballot (starts at 1.0)
    ballot_weights = [1.0 for _ in ballots]
    
    # Create ballot preference lists
    ballot_rankings = []
    for ballot in ballots:
        if ballot.rankings:
            sorted_choices = sorted(
                [(cid, rank) for cid, rank in ballot.rankings.items()],
                key=lambda x: x[1]
            )
            ballot_rankings.append([cid for cid, _ in sorted_choices])
        else:
            ballot_rankings.append([])
    
    round_num = 1
    while len(elected) < seats and len(active_candidates) > seats - len(elected):
        # Count current weighted votes
        counts: Dict[str, float] = defaultdict(float)
        for i, choices in enumerate(ballot_rankings):
            for choice in choices:
                if choice in active_candidates and choice not in elected:
                    counts[choice] += ballot_weights[i]
                    break
        
        round_counts = {cid: counts.get(cid, 0) for cid in active_candidates if cid not in elected}
        
        # Find candidates reaching quota
        new_elected = [cid for cid, v in round_counts.items() if v >= droop_quota]
        
        rounds.append({
            "round": round_num,
            "counts": round_counts.copy(),
            "quota": droop_quota,
            "elected_so_far": elected.copy(),
            "new_elected": new_elected,
            "eliminated_this_round": [],
        })
        
        # Elect candidates reaching quota
        for cid in new_elected:
            if len(elected) < seats:
                elected.append(cid)
                
                # Transfer surplus votes
                surplus = round_counts[cid] - droop_quota
                if surplus > 0:
                    transfer_value = surplus / round_counts[cid]
                    
                    # Transfer from ballots that helped elect this candidate
                    for i, choices in enumerate(ballot_rankings):
                        if choices and choices[0] == cid:
                            ballot_weights[i] = transfer_value
        
        # If no new elections, eliminate lowest candidate
        if not new_elected and len(elected) < seats:
            remaining = {cid: v for cid, v in round_counts.items() if cid not in elected}
            if remaining:
                min_votes = min(remaining.values())
                candidates_to_eliminate = [cid for cid, v in remaining.items() if v == min_votes]
                
                # Eliminate one (handle ties by eliminating randomly)
                to_eliminate = candidates_to_eliminate[0]
                eliminated.append(to_eliminate)
                active_candidates.remove(to_eliminate)
                rounds[-1]["eliminated_this_round"] = [to_eliminate]
                
                # Set weight to 0 for eliminated candidates, transfer to next
                for i, choices in enumerate(ballot_rankings):
                    if choices and choices[0] == to_eliminate:
                        choices.remove(to_eliminate)
        
        round_num += 1
    
    # Fill remaining seats if needed
    while len(elected) < seats:
        remaining = [cid for cid in active_candidates if cid not in elected]
        if not remaining:
            break
        # Pick candidate with most remaining votes
        counts = defaultdict(float)
        for i, choices in enumerate(ballot_rankings):
            for choice in choices:
                if choice in remaining:
                    counts[choice] += ballot_weights[i]
                    break
        if counts:
            next_elected = max(counts, key=counts.get)
            elected.append(next_elected)
        else:
            break
    
    # Build result counts
    vote_counts = []
    final_counts = rounds[-1]["counts"] if rounds else {}
    
    for candidate in poll.candidates:
        is_winner = candidate.id in elected
        vc = VoteCount(
            candidate_id=candidate.id,
            candidate_name=candidate.name,
            votes=int(final_counts.get(candidate.id, 0)),
            percentage=(final_counts.get(candidate.id, 0) / total_votes * 100) if total_votes > 0 else 0,
            eliminated=candidate.id in eliminated
        )
        vote_counts.append(vc)
    
    # Sort: winners first, then by votes
    vote_counts.sort(key=lambda vc: (vc.candidate_id in elected, vc.votes), reverse=True)
    
    # Assign ranks
    for i, vc in enumerate(vote_counts):
        if vc.candidate_id in elected:
            vc.rank = elected.index(vc.candidate_id) + 1
        else:
            vc.rank = len(elected) + i - sum(1 for vc2 in vote_counts[:i] if vc2.candidate_id in elected) + 1
    
    winners = [poll.get_candidate_by_id(cid) for cid in elected]
    
    return ElectionResult(
        poll_id=poll.id,
        poll_title=poll.title,
        method=VotingMethod.STV,
        winners=winners,
        counts=vote_counts,
        total_votes=total_votes,
        rounds=rounds,
        metadata={
            "seats": seats,
            "droop_quota": droop_quota,
            "elected_count": len(elected)
        }
    )


# =============================================================================
# Main Vote Function
# =============================================================================

def count_votes(poll: Poll, ballots: List[Ballot]) -> ElectionResult:
    """
    Count votes using the poll's specified voting method.
    
    Args:
        poll: Poll definition with voting method specified
        ballots: List of submitted ballots
        
    Returns:
        ElectionResult based on the voting method
        
    Raises:
        ValueError: If invalid ballots or unsupported method
    """
    # Validate all ballots
    for ballot in ballots:
        valid, msg = poll.validate_ballot(ballot)
        if not valid:
            raise ValueError(f"Invalid ballot from {ballot.voter_id}: {msg}")
    
    # Route to appropriate counting method
    method_handlers = {
        VotingMethod.PLURALITY: plurality_vote,
        VotingMethod.APPROVAL: approval_vote,
        VotingMethod.RANKED_CHOICE: ranked_choice_vote,
        VotingMethod.BORDA: borda_count,
        VotingMethod.CONDORCET: condorcet_vote,
        VotingMethod.SCORE: score_vote,
        VotingMethod.STV: stv_vote,
    }
    
    handler = method_handlers.get(poll.method)
    if handler is None:
        raise ValueError(f"Unsupported voting method: {poll.method}")
    
    return handler(poll, ballots)


# =============================================================================
# Poll Management
# =============================================================================

def create_poll(
    title: str,
    candidates: List[str],
    method: VotingMethod = VotingMethod.PLURALITY,
    description: Optional[str] = None,
    **kwargs
) -> Poll:
    """
    Create a new poll.
    
    Args:
        title: Poll title
        candidates: List of candidate names
        method: Voting method to use
        description: Optional description
        **kwargs: Additional poll options (max_choices, seats, etc.)
        
    Returns:
        Poll object ready for voting
        
    Example:
        >>> poll = create_poll("Best Pizza", ["Margherita", "Pepperoni", "Hawaiian"])
        >>> poll.method = VotingMethod.RANKED_CHOICE
    """
    # Create candidate objects
    candidate_objects = []
    for i, name in enumerate(candidates):
        cid = hashlib.sha256(f"{title}:{name}:{i}".encode()).hexdigest()[:8]
        candidate_objects.append(Candidate(id=cid, name=name))
    
    poll_id = hashlib.sha256(f"{title}:{len(candidates)}".encode()).hexdigest()[:12]
    
    return Poll(
        id=poll_id,
        title=title,
        description=description,
        candidates=candidate_objects,
        method=method,
        **kwargs
    )


def create_ballot(
    poll_id: str,
    voter_id: str,
    choices: Optional[List[str]] = None,
    rankings: Optional[Dict[str, int]] = None,
    scores: Optional[Dict[str, int]] = None
) -> Ballot:
    """
    Create a new ballot.
    
    Args:
        poll_id: ID of the poll
        voter_id: Voter identifier
        choices: List of candidate IDs (for plurality/approval)
        rankings: Dict of {candidate_id: rank} (for ranked methods)
        scores: Dict of {candidate_id: score} (for score voting)
        
    Returns:
        Ballot object
        
    Example:
        >>> ballot = create_ballot(poll.id, "voter1", choices=["c1"])
    """
    return Ballot(
        voter_id=voter_id,
        poll_id=poll_id,
        choices=choices or [],
        rankings=rankings,
        scores=scores
    )


def generate_test_ballots(poll: Poll, num_ballots: int = 100, 
                          distribution: str = "random") -> List[Ballot]:
    """
    Generate test ballots for simulation.
    
    Args:
        poll: Poll to generate ballots for
        num_ballots: Number of ballots to generate
        distribution: Distribution pattern ("random", "uniform", "biased")
        
    Returns:
        List of generated ballots
    """
    ballots = []
    candidate_ids = [c.id for c in poll.candidates]
    
    for i in range(num_ballots):
        voter_id = f"test_voter_{i}"
        
        if poll.method == VotingMethod.PLURALITY:
            # Single choice
            choice = random.choice(candidate_ids)
            ballot = create_ballot(poll.id, voter_id, choices=[choice])
        
        elif poll.method == VotingMethod.APPROVAL:
            # Multiple approvals
            num_approvals = random.randint(1, min(poll.max_choices, len(candidate_ids)))
            choices = random.sample(candidate_ids, num_approvals)
            ballot = create_ballot(poll.id, voter_id, choices=choices)
        
        elif poll.method in [VotingMethod.RANKED_CHOICE, VotingMethod.BORDA, VotingMethod.STV]:
            # Full ranking
            shuffled = candidate_ids.copy()
            random.shuffle(shuffled)
            rankings = {cid: rank for rank, cid in enumerate(shuffled, 1)}
            ballot = create_ballot(poll.id, voter_id, rankings=rankings)
        
        elif poll.method == VotingMethod.SCORE:
            # Score each candidate
            scores = {cid: random.randint(poll.min_score, poll.max_score) for cid in candidate_ids}
            ballot = create_ballot(poll.id, voter_id, scores=scores)
        
        else:
            ballot = create_ballot(poll.id, voter_id, choices=[random.choice(candidate_ids)])
        
        ballots.append(ballot)
    
    return ballots


def get_voting_method_info(method: VotingMethod) -> Dict[str, Any]:
    """
    Get information about a voting method.
    
    Args:
        method: Voting method
        
    Returns:
        Dict with method info (name, description, pros, cons)
    """
    info = {
        VotingMethod.PLURALITY: {
            "name": "Plurality Voting (First-Past-The-Post)",
            "description": "Each voter selects one candidate. Most votes wins.",
            "pros": ["Simple to understand", "Fast to count", "Familiar to voters"],
            "cons": ["Vote splitting", "Doesn't capture preferences", "Can elect minority-preferred candidate"],
            "requires_rankings": False,
            "requires_scores": False,
        },
        VotingMethod.APPROVAL: {
            "name": "Approval Voting",
            "description": "Each voter can approve multiple candidates. Most approvals wins.",
            "pros": ["Simple", "Encourages consensus", "No vote splitting"],
            "cons": ["May elect bland candidates", "Strategic voting issues"],
            "requires_rankings": False,
            "requires_scores": False,
        },
        VotingMethod.RANKED_CHOICE: {
            "name": "Ranked Choice Voting (Instant Runoff)",
            "description": "Voters rank candidates. Eliminations and transfers until majority winner.",
            "pros": ["Captures preferences", "Eliminates spoiler effect", "Majority winner"],
            "cons": ["More complex", "Can be exhausting", "Center squeeze effect"],
            "requires_rankings": True,
            "requires_scores": False,
        },
        VotingMethod.BORDA: {
            "name": "Borda Count",
            "description": "Voters rank candidates. Points assigned by position. Highest total wins.",
            "pros": ["Consensus-oriented", "Captures full preferences", "Deterministic"],
            "cons": ["Strategic manipulation", "Clone problems", "Narrow vs broad preference"],
            "requires_rankings": True,
            "requires_scores": False,
        },
        VotingMethod.CONDORCET: {
            "name": "Condorcet Voting",
            "description": "Pairwise comparisons. Winner beats all others head-to-head.",
            "pros": ["Strongest candidate", "No strategic voting needed", "Head-to-head wins"],
            "cons": ["May have no winner (cycles)", "Complex resolution methods"],
            "requires_rankings": True,
            "requires_scores": False,
        },
        VotingMethod.SCORE: {
            "name": "Score Voting (Range Voting)",
            "description": "Voters score each candidate. Highest average score wins.",
            "pros": ["Expressive", "Simple", "Encourages honest ratings"],
            "cons": ["Strategic exaggeration", "Requires more voter effort"],
            "requires_rankings": False,
            "requires_scores": True,
        },
        VotingMethod.STV: {
            "name": "Single Transferable Vote",
            "description": "Multi-seat proportional representation with transfers.",
            "pros": ["Proportional representation", "Minority representation", "Fair multi-seat"],
            "cons": ["Complex counting", "Fractional transfers", "May be confusing"],
            "requires_rankings": True,
            "requires_scores": False,
        },
    }
    
    return info.get(method, {"name": method.value, "description": "Unknown method"})


# =============================================================================
# Utility Functions
# =============================================================================

def validate_poll_config(poll: Poll) -> Tuple[bool, List[str]]:
    """
    Validate poll configuration.
    
    Args:
        poll: Poll to validate
        
    Returns:
        Tuple of (is_valid, list of issues)
    """
    issues = []
    
    if not poll.title:
        issues.append("Poll title is required")
    
    if len(poll.candidates) < 2:
        issues.append("At least 2 candidates required")
    
    if poll.method == VotingMethod.APPROVAL and poll.max_choices < 1:
        issues.append("Approval voting requires max_choices >= 1")
    
    if poll.method == VotingMethod.SCORE and poll.max_score <= poll.min_score:
        issues.append("Score voting requires max_score > min_score")
    
    if poll.method == VotingMethod.STV and poll.seats < 1:
        issues.append("STV requires at least 1 seat")
    
    if poll.method == VotingMethod.STV and poll.seats >= len(poll.candidates):
        issues.append("STV requires fewer seats than candidates")
    
    return len(issues) == 0, issues


def get_supported_methods() -> List[VotingMethod]:
    """
    Get list of supported voting methods.
    
    Returns:
        List of VotingMethod enums
    """
    return list(VotingMethod)


# =============================================================================
# Main (for testing)
# =============================================================================

if __name__ == '__main__':
    print("Testing voting utilities...")
    
    # Create a poll
    poll = create_poll(
        "Favorite Programming Language",
        ["Python", "JavaScript", "Go", "Rust", "Java"],
        method=VotingMethod.RANKED_CHOICE
    )
    
    print(f"Poll: {poll.title} (ID: {poll.id})")
    print(f"Candidates: {[c.name for c in poll.candidates]}")
    
    # Generate test ballots
    ballots = generate_test_ballots(poll, 100)
    
    # Count votes
    result = count_votes(poll, ballots)
    
    print("\n" + result.to_summary())
    
    # Test different methods
    print("\n--- Testing Different Methods ---")
    
    for method in [VotingMethod.PLURALITY, VotingMethod.APPROVAL, VotingMethod.BORDA, 
                   VotingMethod.CONDORCET, VotingMethod.SCORE]:
        poll.method = method
        ballots = generate_test_ballots(poll, 50)
        result = count_votes(poll, ballots)
        winner = result.get_winner()
        print(f"{method.value}: Winner = {winner.name if winner else 'None'}")
    
    print("\nAll tests passed!")