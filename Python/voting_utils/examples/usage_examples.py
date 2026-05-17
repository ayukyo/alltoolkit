#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Voting Utilities Usage Examples

Examples demonstrating various voting methods and poll management.

Author: AllToolkit
License: MIT
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from voting_utils.mod import (
    VotingMethod, create_poll, create_ballot, count_votes, 
    generate_test_ballots, get_voting_method_info
)


def example_plurality_voting():
    """Example: Basic plurality voting (first-past-the-post)."""
    print("\n=== Example 1: Plurality Voting ===\n")
    
    # Create a poll for favorite color
    poll = create_poll(
        "Favorite Color Poll",
        ["Red", "Blue", "Green", "Yellow"],
        method=VotingMethod.PLURALITY,
        description="Vote for your favorite color!"
    )
    
    print(f"Poll: {poll.title}")
    print(f"Method: {poll.method.value}")
    print(f"Candidates: {[c.name for c in poll.candidates]}")
    
    # Create ballots manually
    ballots = [
        create_ballot(poll.id, "voter1", choices=[poll.candidates[0].id]),
        create_ballot(poll.id, "voter2", choices=[poll.candidates[0].id]),
        create_ballot(poll.id, "voter3", choices=[poll.candidates[1].id]),
        create_ballot(poll.id, "voter4", choices=[poll.candidates[0].id]),
        create_ballot(poll.id, "voter5", choices=[poll.candidates[2].id]),
    ]
    
    # Count votes
    result = count_votes(poll, ballots)
    
    print(f"\nTotal votes: {result.total_votes}")
    print(f"Winner: {result.get_winner().name}")
    print("\nFull results:")
    for count in result.counts:
        print(f"  {count.rank}. {count.candidate_name}: {count.votes} votes ({count.percentage:.1f}%)")


def example_approval_voting():
    """Example: Approval voting."""
    print("\n=== Example 2: Approval Voting ===\n")
    
    # Create a poll for pizza toppings (multiple can be approved)
    poll = create_poll(
        "Pizza Topping Selection",
        ["Pepperoni", "Mushrooms", "Olives", "Bacon", "Extra Cheese"],
        method=VotingMethod.APPROVAL,
        max_choices=3,
        description="Approve up to 3 toppings you'd like"
    )
    
    print(f"Poll: {poll.title}")
    print(f"Max approvals per voter: {poll.max_choices}")
    
    # Generate test ballots with random approvals
    ballots = generate_test_ballots(poll, 50)
    
    # Count votes
    result = count_votes(poll, ballots)
    
    print(f"\nTotal voters: {result.total_votes}")
    print(f"Total approvals: {result.metadata.get('total_approvals', 0)}")
    print(f"Winner(s): {[w.name for w in result.winners]}")
    
    print("\nApproval counts:")
    for count in result.counts:
        print(f"  {count.rank}. {count.candidate_name}: approved by {count.votes} voters ({count.percentage:.1f}%)")


def example_ranked_choice():
    """Example: Ranked choice voting (instant runoff)."""
    print("\n=== Example 3: Ranked Choice Voting (IRV) ===\n")
    
    # Create a poll for best programming language
    poll = create_poll(
        "Best Programming Language 2026",
        ["Python", "JavaScript", "Go", "Rust", "Java"],
        method=VotingMethod.RANKED_CHOICE,
        description="Rank your top programming languages"
    )
    
    # Get method info
    info = get_voting_method_info(VotingMethod.RANKED_CHOICE)
    print(f"Method: {info['name']}")
    print(f"Description: {info['description']}")
    
    # Create ballots with rankings
    # Simulate a scenario where Python leads but doesn't have majority initially
    ballots = []
    
    # 35 voters: Python > JavaScript > Go
    for i in range(35):
        rankings = {
            poll.candidates[0].id: 1,  # Python first
            poll.candidates[1].id: 2,  # JavaScript second
            poll.candidates[2].id: 3,  # Go third
        }
        ballots.append(create_ballot(poll.id, f"v{i}", rankings=rankings))
    
    # 25 voters: JavaScript > Python > Go
    for i in range(35, 60):
        rankings = {
            poll.candidates[1].id: 1,  # JavaScript first
            poll.candidates[0].id: 2,  # Python second
            poll.candidates[2].id: 3,  # Go third
        }
        ballots.append(create_ballot(poll.id, f"v{i}", rankings=rankings))
    
    # 20 voters: Go > Rust > JavaScript
    for i in range(60, 80):
        rankings = {
            poll.candidates[2].id: 1,  # Go first
            poll.candidates[3].id: 2,  # Rust second
            poll.candidates[1].id: 3,  # JavaScript third
        }
        ballots.append(create_ballot(poll.id, f"v{i}", rankings=rankings))
    
    # 20 voters: Rust > Go > Python
    for i in range(80, 100):
        rankings = {
            poll.candidates[3].id: 1,  # Rust first
            poll.candidates[2].id: 2,  # Go second
            poll.candidates[0].id: 3,  # Python third
        }
        ballots.append(create_ballot(poll.id, f"v{i}", rankings=rankings))
    
    # Count votes
    result = count_votes(poll, ballots)
    
    print(f"\nWinner: {result.get_winner().name}")
    print(f"Number of rounds: {len(result.rounds) if result.rounds else 1}")
    
    if result.rounds:
        print("\nRound-by-round results:")
        for round_info in result.rounds:
            print(f"  Round {round_info['round']}:")
            for cid, votes in round_info['counts'].items():
                cand = poll.get_candidate_by_id(cid)
                print(f"    {cand.name}: {votes} votes")
            print(f"    Majority threshold: {round_info['majority_threshold']}")
            print(f"    Has majority: {round_info['has_majority']}")


def example_borda_count():
    """Example: Borda count voting."""
    print("\n=== Example 4: Borda Count ===\n")
    
    # Create a poll for best movie
    poll = create_poll(
        "Best Movie of the Year",
        ["The Adventure", "Love Story", "Sci-Fi Epic", "Comedy Hit"],
        method=VotingMethod.BORDA
    )
    
    print(f"Poll: {poll.title}")
    
    # Create ballots with rankings
    ballots = generate_test_ballots(poll, 30)
    
    # Count votes
    result = count_votes(poll, ballots)
    
    print(f"\nWinner: {result.get_winner().name}")
    print(f"Max possible Borda score: {result.metadata['max_borda_score']}")
    
    print("\nBorda scores:")
    for count in result.counts:
        print(f"  {count.rank}. {count.candidate_name}: {count.votes} points ({count.percentage:.1f}% of max)")


def example_condorcet():
    """Example: Condorcet voting."""
    print("\n=== Example 5: Condorcet Voting ===\n")
    
    # Create a poll
    poll = create_poll(
        "Best Restaurant in Town",
        ["Pizza Place", "Sushi Bar", "Steak House", "Thai Corner"],
        method=VotingMethod.CONDORCET
    )
    
    print(f"Poll: {poll.title}")
    
    # Generate ballots
    ballots = generate_test_ballots(poll, 25)
    
    result = count_votes(poll, ballots)
    
    print(f"\nCondorcet winner exists: {result.metadata['condorcet_winner_exists']}")
    print(f"Resolution method: {result.metadata['resolution_method']}")
    print(f"Winner: {result.get_winner().name}")
    
    # Show pairwise matrix if available
    if result.pairwise_matrix:
        print("\nPairwise comparison matrix (wins):")
        cands = {c.id: c.name for c in poll.candidates}
        print("    " + "  ".join(cands.values()))
        for cid1, row in result.pairwise_matrix.items():
            row_str = cands[cid1] + ": "
            for cid2, wins in row.items():
                if cid1 != cid2:
                    row_str += f"{wins:>3} "
            print(row_str)


def example_score_voting():
    """Example: Score/range voting."""
    print("\n=== Example 6: Score Voting ===\n")
    
    # Create a poll with score range 0-10
    poll = create_poll(
        "Rate the Service Quality",
        ["Staff Friendliness", "Speed", "Cleanliness", "Value"],
        method=VotingMethod.SCORE,
        min_score=0,
        max_score=10
    )
    
    print(f"Poll: {poll.title}")
    print(f"Score range: {poll.min_score} to {poll.max_score}")
    
    # Create ballots with scores
    ballots = generate_test_ballots(poll, 20)
    
    result = count_votes(poll, ballots)
    
    print(f"\nWinner: {result.get_winner().name}")
    
    print("\nAverage scores:")
    for count in result.counts:
        # Calculate average from total and percentage
        avg = (count.percentage / 100) * poll.max_score
        print(f"  {count.rank}. {count.candidate_name}: avg {avg:.1f}/10 (total: {count.votes})")


def example_stv():
    """Example: Single Transferable Vote for multi-seat."""
    print("\n=== Example 7: STV (Multi-Seat Election) ===\n")
    
    # Create a poll to elect 3 committee members
    poll = create_poll(
        "Elect Committee Members",
        ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"],
        method=VotingMethod.STV,
        seats=3,
        description="Elect 3 members to the committee"
    )
    
    print(f"Poll: {poll.title}")
    print(f"Seats to fill: {poll.seats}")
    
    # Generate ballots
    ballots = generate_test_ballots(poll, 100)
    
    result = count_votes(poll, ballots)
    
    print(f"\nDroop quota: {result.metadata['droop_quota']}")
    print(f"Elected: {[w.name for w in result.winners]}")
    
    if result.rounds:
        print("\nElection rounds:")
        for round_info in result.rounds:
            print(f"  Round {round_info['round']}:")
            print(f"    Elected so far: {[poll.get_candidate_by_id(cid).name for cid in round_info['elected_so_far']]}")
            if round_info['new_elected']:
                print(f"    Newly elected: {[poll.get_candidate_by_id(cid).name for cid in round_info['new_elected']]}")
            if round_info['eliminated_this_round']:
                print(f"    Eliminated: {[poll.get_candidate_by_id(cid).name for cid in round_info['eliminated_this_round']]}")


def example_compare_methods():
    """Example: Compare different methods on same ballots."""
    print("\n=== Example 8: Comparing Methods ===\n")
    
    # Create a poll
    poll = create_poll(
        "Favorite Season",
        ["Spring", "Summer", "Fall", "Winter"],
        method=VotingMethod.PLURALITY
    )
    
    # Generate base ballots
    ballots = generate_test_ballots(poll, 50)
    
    print(f"Poll: {poll.title}")
    print(f"Total voters: {len(ballots)}")
    
    # Test each method
    methods = [
        VotingMethod.PLURALITY,
        VotingMethod.APPROVAL,
        VotingMethod.RANKED_CHOICE,
        VotingMethod.BORDA,
        VotingMethod.CONDORCET,
        VotingMethod.SCORE,
    ]
    
    print("\nResults by method:")
    for method in methods:
        poll.method = method
        # Regenerate ballots appropriate for each method
        test_ballots = generate_test_ballots(poll, 50)
        result = count_votes(poll, test_ballots)
        winner = result.get_winner()
        print(f"  {method.value}: {winner.name if winner else 'None'}")


def example_method_info():
    """Example: Get information about voting methods."""
    print("\n=== Example 9: Voting Method Information ===\n")
    
    methods = [
        VotingMethod.PLURALITY,
        VotingMethod.APPROVAL,
        VotingMethod.RANKED_CHOICE,
        VotingMethod.BORDA,
        VotingMethod.CONDORCET,
        VotingMethod.SCORE,
        VotingMethod.STV,
    ]
    
    for method in methods:
        info = get_voting_method_info(method)
        print(f"\n{info['name']}")
        print(f"  Description: {info['description']}")
        print(f"  Pros: {', '.join(info['pros'][:2])}")
        print(f"  Cons: {', '.join(info['cons'][:2])}")


def example_full_workflow():
    """Example: Full poll workflow."""
    print("\n=== Example 10: Full Poll Workflow ===\n")
    
    # Step 1: Create poll
    print("Step 1: Creating poll...")
    poll = create_poll(
        "Team Lunch Decision",
        ["Italian", "Chinese", "Mexican", "Indian"],
        method=VotingMethod.RANKED_CHOICE,
        description="Decide where to go for team lunch"
    )
    print(f"  Created poll: {poll.title} (ID: {poll.id})")
    
    # Step 2: Collect ballots
    print("\nStep 2: Collecting ballots...")
    ballots = []
    team_members = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
    
    # Simulate team preferences
    preferences = [
        [0, 1, 2, 3],  # Alice: Italian > Chinese > Mexican > Indian
        [0, 2, 1, 3],  # Bob: Italian > Mexican > Chinese > Indian
        [1, 0, 2, 3],  # Charlie: Chinese > Italian > Mexican > Indian
        [1, 3, 0, 2],  # Diana: Chinese > Indian > Italian > Mexican
        [2, 0, 1, 3],  # Eve: Mexican > Italian > Chinese > Indian
        [2, 1, 0, 3],  # Frank: Mexican > Chinese > Italian > Indian
        [3, 2, 1, 0],  # Grace: Indian > Mexican > Chinese > Italian
        [3, 1, 0, 2],  # Henry: Indian > Chinese > Italian > Mexican
    ]
    
    for i, (member, prefs) in enumerate(zip(team_members, preferences)):
        rankings = {}
        for rank, pref_idx in enumerate(prefs, 1):
            rankings[poll.candidates[pref_idx].id] = rank
        ballot = create_ballot(poll.id, member.lower(), rankings=rankings)
        ballots.append(ballot)
    
    print(f"  Collected {len(ballots)} ballots")
    
    # Step 3: Count votes
    print("\nStep 3: Counting votes...")
    result = count_votes(poll, ballots)
    
    # Step 4: Display results
    print("\nStep 4: Results")
    print(result.to_summary())
    
    # Step 5: Decision
    print("\nStep 5: Decision")
    winner = result.get_winner()
    print(f"  The team will go to: {winner.name}!")


def main():
    """Run all examples."""
    print("=" * 60)
    print("AllToolkit - Voting Utilities Examples")
    print("=" * 60)
    
    example_plurality_voting()
    example_approval_voting()
    example_ranked_choice()
    example_borda_count()
    example_condorcet()
    example_score_voting()
    example_stv()
    example_compare_methods()
    example_method_info()
    example_full_workflow()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()