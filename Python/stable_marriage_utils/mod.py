"""
Stable Marriage Utils - Gale-Shapley Algorithm Implementation

This module implements the classic Stable Marriage Problem algorithm and related utilities.
The Stable Marriage Problem involves finding a stable matching between two equally sized
sets of elements (traditionally men and women) based on preferences.

Applications:
- College admissions matching
- Hospital residency programs (NRMP)
- Stable roommates problem
- Job matching markets
- Resource allocation

Time Complexity: O(n²) for n participants on each side
Space Complexity: O(n²) for preference storage

References:
- Gale, D. and Shapley, L. S. (1962). "College Admissions and the Stability of Marriage"
- https://en.wikipedia.org/wiki/Gale%E2%80%93Shapley_algorithm
"""

from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict


class StableMarriage:
    """
    Solver for the Stable Marriage Problem using the Gale-Shapley algorithm.
    
    The algorithm guarantees:
    1. Everyone gets matched (if equal sizes)
    2. The matching is stable (no blocking pair exists)
    3. Men-optimal solution (men get their best possible stable partner)
    """
    
    def __init__(self, men_preferences: Dict[str, List[str]], 
                 women_preferences: Dict[str, List[str]]):
        """
        Initialize the Stable Marriage solver.
        
        Args:
            men_preferences: Dict mapping each man to his ranked list of women (first = most preferred)
            women_preferences: Dict mapping each woman to her ranked list of men (first = most preferred)
        
        Example:
            >>> men = {
            ...     'A': ['Y', 'X', 'Z'],
            ...     'B': ['X', 'Y', 'Z'],
            ...     'C': ['Y', 'X', 'Z']
            ... }
            >>> women = {
            ...     'X': ['A', 'B', 'C'],
            ...     'Y': ['B', 'A', 'C'],
            ...     'Z': ['A', 'B', 'C']
            ... }
            >>> sm = StableMarriage(men, women)
        """
        self.men_preferences = {m: list(w) for m, w in men_preferences.items()}
        self.women_preferences = {w: list(m) for w, m in women_preferences.items()}
        self.men = list(men_preferences.keys())
        self.women = list(women_preferences.keys())
        
        # Pre-compute women's ranking for O(1) lookup
        self.women_rankings = {}
        for woman, pref_list in women_preferences.items():
            self.women_rankings[woman] = {man: rank for rank, man in enumerate(pref_list)}
        
        self._validate_preferences()
    
    def _validate_preferences(self) -> None:
        """Validate that preference lists are consistent."""
        if len(self.men) != len(self.women):
            raise ValueError(f"Number of men ({len(self.men)}) must equal number of women ({len(self.women)})")
        
        for man in self.men:
            if set(self.men_preferences[man]) != set(self.women):
                raise ValueError(f"Man {man}'s preferences don't include all women")
        
        for woman in self.women:
            if set(self.women_preferences[woman]) != set(self.men):
                raise ValueError(f"Woman {woman}'s preferences don't include all men")
    
    def solve(self) -> Dict[str, str]:
        """
        Solve the Stable Marriage Problem using the Gale-Shapley algorithm.
        
        Returns men-optimal stable matching: each man gets matched with his best
        possible partner among all stable matchings.
        
        Returns:
            Dict mapping each man to his matched woman
        
        Example:
            >>> result = sm.solve()
            >>> result
            {'A': 'Y', 'B': 'X', 'C': 'Z'}
        """
        # Current matching state
        free_men = list(self.men)  # Men still looking for a partner
        engaged = {}  # woman -> man mapping
        proposals = defaultdict(int)  # Track how many proposals each man has made
        
        while free_men:
            man = free_men[0]
            
            # Get next woman to propose to
            if proposals[man] >= len(self.women):
                # Should never happen if preferences are valid
                free_men.pop(0)
                continue
            
            woman = self.men_preferences[man][proposals[man]]
            proposals[man] += 1
            
            if woman not in engaged:
                # Woman is free, accept proposal
                engaged[woman] = man
                free_men.pop(0)
            else:
                # Woman is engaged, see if she prefers this new man
                current_man = engaged[woman]
                current_rank = self.women_rankings[woman][current_man]
                new_rank = self.women_rankings[woman][man]
                
                if new_rank < current_rank:
                    # She prefers the new man
                    engaged[woman] = man
                    free_men.pop(0)
                    free_men.append(current_man)  # Old man becomes free
                # else: she keeps current man, proposer stays free
        
        # Convert woman->man to man->woman
        return {man: woman for woman, man in engaged.items()}
    
    def solve_women_optimal(self) -> Dict[str, str]:
        """
        Solve for women-optimal stable matching.
        
        Returns:
            Dict mapping each man to his matched woman (women get their best stable partner)
        """
        # Swap roles: women propose to men
        swapped = StableMarriage(self.women_preferences, self.men_preferences)
        woman_to_man = swapped.solve()  # Women's optimal
        # Convert back: the result is woman->man, we need man->woman
        return {man: woman for woman, man in woman_to_man.items()}
    
    def is_stable(self, matching: Dict[str, str]) -> bool:
        """
        Check if a matching is stable.
        
        A matching is stable if no blocking pair exists:
        there is no man m and woman w such that m prefers w to his current partner
        AND w prefers m to her current partner.
        
        Args:
            matching: Dict mapping each man to his matched woman
        
        Returns:
            True if stable, False otherwise
        """
        # Build reverse mapping
        woman_to_man = {w: m for m, w in matching.items()}
        
        for man in self.men:
            current_woman = matching[man]
            current_rank = self.men_preferences[man].index(current_woman)
            
            # Check women this man prefers over his current partner
            for preferred_woman in self.men_preferences[man][:current_rank]:
                preferred_woman_current_man = woman_to_man[preferred_woman]
                preferred_woman_current_rank = self.women_rankings[preferred_woman][preferred_woman_current_man]
                man_rank = self.women_rankings[preferred_woman][man]
                
                # If preferred woman also prefers this man, it's a blocking pair
                if man_rank < preferred_woman_current_rank:
                    return False
        
        return True
    
    def find_blocking_pairs(self, matching: Dict[str, str]) -> List[Tuple[str, str]]:
        """
        Find all blocking pairs in a matching.
        
        Args:
            matching: Dict mapping each man to his matched woman
        
        Returns:
            List of (man, woman) tuples that form blocking pairs
        """
        blocking_pairs = []
        woman_to_man = {w: m for m, w in matching.items()}
        
        for man in self.men:
            current_woman = matching[man]
            current_rank = self.men_preferences[man].index(current_woman)
            
            for preferred_woman in self.men_preferences[man][:current_rank]:
                preferred_woman_current_man = woman_to_man[preferred_woman]
                preferred_woman_current_rank = self.women_rankings[preferred_woman][preferred_woman_current_man]
                man_rank = self.women_rankings[preferred_woman][man]
                
                if man_rank < preferred_woman_current_rank:
                    blocking_pairs.append((man, preferred_woman))
        
        return blocking_pairs
    
    def calculate_satisfaction(self, matching: Dict[str, str]) -> Dict[str, any]:
        """
        Calculate satisfaction metrics for a matching.
        
        Lower scores are better (1 = first choice, 2 = second choice, etc.)
        
        Args:
            matching: Dict mapping each man to his matched woman
        
        Returns:
            Dict with satisfaction metrics for both sides
        """
        men_scores = {}
        women_scores = {}
        woman_to_man = {w: m for m, w in matching.items()}
        
        for man, woman in matching.items():
            men_scores[man] = self.men_preferences[man].index(woman) + 1
            women_scores[woman] = self.women_preferences[woman].index(man) + 1
        
        return {
            'men_scores': men_scores,
            'women_scores': women_scores,
            'men_avg': sum(men_scores.values()) / len(men_scores),
            'women_avg': sum(women_scores.values()) / len(women_scores),
            'total_avg': (sum(men_scores.values()) + sum(women_scores.values())) / (2 * len(men_scores)),
            'men_best': min(men_scores.values()),
            'women_best': min(women_scores.values()),
            'men_worst': max(men_scores.values()),
            'women_worst': max(women_scores.values()),
        }
    
    def count_stable_matchings(self) -> int:
        """
        Count the number of possible stable matchings.
        
        Uses the Irving-Leather algorithm approach (simplified for counting).
        
        Returns:
            Number of stable matchings
        
        Note:
            This can be exponential in worst case, but typically much smaller.
            Maximum known is O(n! / 2) but rare in practice.
        """
        # For small instances, enumerate all possible stable matchings
        # Using a rotation-based approach
        if len(self.men) > 8:
            # Too large to enumerate practically
            return -1  # Indicate "too many to count"
        
        from itertools import permutations
        
        count = 0
        for perm in permutations(self.women):
            matching = {man: woman for man, woman in zip(self.men, perm)}
            if self.is_stable(matching):
                count += 1
        
        return count
    
    def find_all_stable_matchings(self) -> List[Dict[str, str]]:
        """
        Find all stable matchings (only for small instances).
        
        Returns:
            List of all stable matchings
        """
        from itertools import permutations
        
        if len(self.men) > 8:
            return []  # Too large to enumerate
        
        stable = []
        for perm in permutations(self.women):
            matching = {man: woman for man, woman in zip(self.men, perm)}
            if self.is_stable(matching):
                stable.append(matching)
        
        return stable


class StableRoommates:
    """
    Solver for the Stable Roommates Problem.
    
    Unlike Stable Marriage, this deals with a single group where everyone
    ranks everyone else. Not all instances have a stable solution.
    
    Uses Irving's algorithm which runs in O(n²) time.
    """
    
    def __init__(self, preferences: Dict[str, List[str]]):
        """
        Initialize the Stable Roommates solver.
        
        Args:
            preferences: Dict mapping each person to their ranked list of others
        """
        self.preferences = {p: list(others) for p, others in preferences.items()}
        self.people = list(preferences.keys())
        self.n = len(self.people)
        
        if self.n % 2 != 0:
            raise ValueError("Number of people must be even for stable roommates")
        
        self._validate_preferences()
        
        # Build ranking lookup for O(1) preference checks
        self.rankings = {}
        for person, prefs in self.preferences.items():
            self.rankings[person] = {other: rank for rank, other in enumerate(prefs)}
    
    def _validate_preferences(self) -> None:
        """Validate preference lists."""
        for person in self.people:
            others = set(self.preferences[person])
            expected = set(self.people) - {person}
            if others != expected:
                raise ValueError(f"Person {person}'s preferences are invalid")
    
    def solve(self) -> Optional[Dict[str, str]]:
        """
        Solve the Stable Roommates Problem using Irving's algorithm.
        
        Returns:
            Dict mapping each person to their roommate, or None if no stable solution exists
        
        Example:
            >>> prefs = {
            ...     'A': ['B', 'C', 'D'],
            ...     'B': ['A', 'D', 'C'],
            ...     'C': ['D', 'A', 'B'],
            ...     'D': ['C', 'B', 'A']
            ... }
            >>> sr = StableRoommates(prefs)
            >>> sr.solve()
            {'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'}
        """
        # Work with a copy of preferences
        pref = {p: list(self.preferences[p]) for p in self.people}
        
        # Phase 1: Proposal phase
        # Each person holds one proposal at a time
        holds = {p: None for p in self.people}
        
        for proposer in self.people:
            person = proposer
            while pref[person]:
                # Propose to most preferred remaining
                target = pref[person][0]
                
                if holds[target] is None:
                    # Target accepts
                    holds[target] = person
                    break
                else:
                    # Target compares with current holder
                    current_holder = holds[target]
                    if self.rankings[target][person] < self.rankings[target][current_holder]:
                        # Target prefers new proposer
                        holds[target] = person
                        # Reject old holder - remove target from their list
                        pref[current_holder].remove(target)
                        # Old holder must continue proposing
                        person = current_holder
                    else:
                        # Target rejects new proposer
                        pref[person].remove(target)
                        # New proposer continues
        
        # Check Phase 1 success
        for p in self.people:
            if not pref[p]:
                return None  # Empty list means no stable solution
        
        # Phase 2: Build reduced preference lists
        # Each person keeps only those who hold them + those they prefer over holder
        for p in self.people:
            if holds[p] is not None:
                # p's reduced list: everyone up to and including holder
                holder_rank = self.rankings[p][holds[p]]
                pref[p] = [q for q in self.preferences[p] 
                          if self.rankings[p][q] <= holder_rank]
        
        # Phase 3: Rotation elimination
        max_iter = self.n * self.n + 10
        for iteration in range(max_iter):
            # Check if done
            if all(len(pref[p]) == 1 for p in self.people):
                break
            
            # Find a rotation
            rotation = self._find_rotation(pref)
            if rotation is None or len(rotation) < 2:
                break
            
            # Eliminate rotation
            for i, p in enumerate(rotation):
                # p's second choice
                if len(pref[p]) >= 2:
                    second_choice = pref[p][1]
                    # Remove p's first choice from second_choice's list
                    first_choice = pref[p][0]
                    if first_choice in pref[second_choice]:
                        pref[second_choice].remove(first_choice)
            
            # Check for empty lists
            for p in self.people:
                if not pref[p]:
                    return None
        
        # Final check
        if all(len(pref[p]) == 1 for p in self.people):
            result = {p: pref[p][0] for p in self.people}
            # Verify mutual matching
            for p, q in result.items():
                if result[q] != p:
                    return None
            return result
        
        return None
    
    def _find_rotation(self, pref: Dict[str, List[str]]) -> Optional[List[str]]:
        """Find a rotation in the preference lists."""
        # Find someone with more than one preference
        start = None
        for p in self.people:
            if len(pref[p]) > 1:
                start = p
                break
        
        if start is None:
            return None
        
        rotation = []
        visited = {}
        current = start
        
        max_steps = self.n * 2
        for _ in range(max_steps):
            if current in visited:
                # Found cycle - extract rotation
                idx = visited[current]
                return rotation[idx:]
            
            visited[current] = len(rotation)
            rotation.append(current)
            
            if len(pref[current]) < 2:
                return None
            
            # Go to second choice
            second = pref[current][1]
            current = second
        
        return None
    
    def is_stable(self, matching: Dict[str, str]) -> bool:
        """
        Check if a roommate matching is stable.
        
        A matching is stable if no blocking pair exists.
        """
        for person1 in self.people:
            roommate1 = matching.get(person1)
            if roommate1 is None:
                return False
            
            person1_rank = self.rankings[person1][roommate1]
            
            # Check people person1 prefers over current roommate
            for preferred in self.preferences[person1][:person1_rank]:
                preferred_roommate = matching.get(preferred)
                if preferred_roommate is None:
                    continue
                    
                if self.rankings[preferred][person1] < self.rankings[preferred][preferred_roommate]:
                    return False
        
        return True


class HospitalResidents:
    """
    Solver for the Hospital/Residents Problem (many-to-one matching).
    
    Extension of Stable Marriage where:
    - One side (hospitals) can have multiple slots
    - Hospitals have capacities, residents have no capacity (always 1)
    
    Applications:
    - Medical residency matching (NRMP)
    - College admissions
    - School choice programs
    """
    
    def __init__(self, residents: Dict[str, List[str]], 
                 hospitals: Dict[str, Tuple[int, List[str]]]):
        """
        Initialize the Hospital/Residents solver.
        
        Args:
            residents: Dict mapping resident ID to ranked hospital preferences
            hospitals: Dict mapping hospital ID to (capacity, ranked resident preferences)
        
        Example:
            >>> residents = {
            ...     'R1': ['H1', 'H2', 'H3'],
            ...     'R2': ['H2', 'H1', 'H3'],
            ...     'R3': ['H1', 'H3', 'H2']
            ... }
            >>> hospitals = {
            ...     'H1': (2, ['R1', 'R3', 'R2']),  # capacity 2
            ...     'H2': (1, ['R2', 'R1', 'R3']),  # capacity 1
            ...     'H3': (1, ['R3', 'R2', 'R1'])   # capacity 1
            ... }
        """
        self.residents = residents
        self.hospitals = hospitals
        self.hospital_capacities = {h: cap for h, (cap, _) in hospitals.items()}
        self.hospital_preferences = {h: prefs for h, (_, prefs) in hospitals.items()}
        
        # Pre-compute hospital rankings
        self.hospital_rankings = {}
        for hospital, prefs in self.hospital_preferences.items():
            self.hospital_rankings[hospital] = {r: rank for rank, r in enumerate(prefs)}
    
    def solve(self) -> Dict[str, List[str]]:
        """
        Solve using resident-proposing algorithm.
        
        Returns:
            Dict mapping each hospital to list of matched residents
        """
        # State tracking
        free_residents = list(self.residents.keys())
        hospital_matches = {h: [] for h in self.hospitals}
        proposals = defaultdict(int)  # resident -> number of proposals made
        
        while free_residents:
            resident = free_residents[0]
            
            if proposals[resident] >= len(self.residents[resident]):
                # Resident has been rejected by all hospitals
                free_residents.pop(0)
                continue
            
            hospital = self.residents[resident][proposals[resident]]
            proposals[resident] += 1
            
            capacity = self.hospital_capacities[hospital]
            current_matches = hospital_matches[hospital]
            
            if len(current_matches) < capacity:
                # Hospital has space
                current_matches.append(resident)
                free_residents.pop(0)
            else:
                # Hospital is full, see if they prefer this resident
                worst_current = max(current_matches, 
                                   key=lambda r: self.hospital_rankings[hospital][r])
                worst_rank = self.hospital_rankings[hospital][worst_current]
                new_rank = self.hospital_rankings[hospital][resident]
                
                if new_rank < worst_rank:
                    # Replace worst resident
                    current_matches.remove(worst_current)
                    current_matches.append(resident)
                    free_residents.pop(0)
                    free_residents.append(worst_current)
        
        return hospital_matches
    
    def solve_hospital_optimal(self) -> Dict[str, List[str]]:
        """
        Solve using hospital-proposing algorithm.
        
        Not guaranteed to be stable in the same sense as resident-proposing,
        but hospitals get better outcomes.
        """
        # Hospital-proposing version
        hospital_queues = {h: list(prefs) for h, (_, prefs) in self.hospitals.items()}
        hospital_matches = {h: [] for h in self.hospitals}
        resident_match = {r: None for r in self.residents}
        
        has_active = True
        while has_active:
            has_active = False
            
            for hospital in self.hospitals:
                current = hospital_matches[hospital]
                capacity = self.hospital_capacities[hospital]
                
                while len(current) < capacity and hospital_queues[hospital]:
                    has_active = True
                    resident = hospital_queues[hospital].pop(0)
                    
                    if resident_match[resident] is None:
                        # Resident is free
                        resident_match[resident] = hospital
                        current.append(resident)
                    else:
                        # Resident is matched, see if they prefer this hospital
                        current_hospital = resident_match[resident]
                        current_rank = self.residents[resident].index(current_hospital)
                        new_rank = self.residents[resident].index(hospital)
                        
                        if new_rank < current_rank:
                            # Resident prefers new hospital
                            hospital_matches[current_hospital].remove(resident)
                            resident_match[resident] = hospital
                            current.append(resident)
        
        return hospital_matches
    
    def is_stable(self, matching: Dict[str, List[str]]) -> bool:
        """
        Check if the matching is stable.
        
        A matching is stable if no (resident, hospital) pair exists such that:
        - Resident prefers hospital over their current match
        - Hospital either has capacity OR prefers resident over some current match
        """
        resident_to_hospital = {}
        for hospital, residents in matching.items():
            for resident in residents:
                resident_to_hospital[resident] = hospital
        
        for resident, preferences in self.residents.items():
            current_hospital = resident_to_hospital.get(resident)
            if current_hospital is None:
                current_rank = len(preferences)  # Unmatched, worst
            else:
                current_rank = preferences.index(current_hospital)
            
            # Check hospitals resident prefers over current
            for hospital in preferences[:current_rank]:
                hospital_current = matching[hospital]
                capacity = self.hospital_capacities[hospital]
                
                if len(hospital_current) < capacity:
                    # Hospital has space and resident prefers it
                    return False
                
                # Check if hospital would prefer this resident
                worst_current = max(hospital_current, 
                                   key=lambda r: self.hospital_rankings[hospital][r])
                if self.hospital_rankings[hospital][resident] < self.hospital_rankings[hospital][worst_current]:
                    return False
        
        return True


# Convenience functions
def stable_marriage(men_preferences: Dict[str, List[str]], 
                    women_preferences: Dict[str, List[str]]) -> Dict[str, str]:
    """
    Convenience function to solve the Stable Marriage Problem.
    
    Args:
        men_preferences: Dict mapping each man to his ranked list of women
        women_preferences: Dict mapping each woman to her ranked list of men
    
    Returns:
        Dict mapping each man to his matched woman
    
    Example:
        >>> men = {'A': ['Y', 'X'], 'B': ['X', 'Y']}
        >>> women = {'X': ['A', 'B'], 'Y': ['B', 'A']}
        >>> stable_marriage(men, women)
        {'A': 'Y', 'B': 'X'}
    """
    solver = StableMarriage(men_preferences, women_preferences)
    return solver.solve()


def stable_roommates(preferences: Dict[str, List[str]]) -> Optional[Dict[str, str]]:
    """
    Convenience function to solve the Stable Roommates Problem.
    
    Args:
        preferences: Dict mapping each person to their ranked list of others
    
    Returns:
        Dict mapping each person to their roommate, or None if no stable solution
    
    Example:
        >>> prefs = {'A': ['B', 'C', 'D'], 'B': ['A', 'D', 'C'], 
        ...          'C': ['D', 'A', 'B'], 'D': ['C', 'B', 'A']}
        >>> stable_roommates(prefs)
        {'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'}
    """
    solver = StableRoommates(preferences)
    return solver.solve()


def hospital_residents(residents: Dict[str, List[str]], 
                       hospitals: Dict[str, Tuple[int, List[str]]]) -> Dict[str, List[str]]:
    """
    Convenience function to solve the Hospital/Residents Problem.
    
    Args:
        residents: Dict mapping resident ID to hospital preferences
        hospitals: Dict mapping hospital ID to (capacity, resident preferences)
    
    Returns:
        Dict mapping each hospital to list of matched residents
    """
    solver = HospitalResidents(residents, hospitals)
    return solver.solve()


if __name__ == "__main__":
    # Demo
    print("=== Stable Marriage Demo ===")
    men = {
        'Alice': ['Bob', 'Charlie', 'David'],
        'Emma': ['Charlie', 'Bob', 'David'],
        'Frank': ['Bob', 'Charlie', 'David']
    }
    women = {
        'Bob': ['Alice', 'Emma', 'Frank'],
        'Charlie': ['Emma', 'Alice', 'Frank'],
        'David': ['Alice', 'Frank', 'Emma']
    }
    
    # Note: Using gender-neutral names for clarity
    # men = proposers, women = acceptors in classical formulation
    
    sm = StableMarriage(men, women)
    result = sm.solve()
    print(f"Men-optimal matching: {result}")
    print(f"Is stable: {sm.is_stable(result)}")
    
    satisfaction = sm.calculate_satisfaction(result)
    print(f"Satisfaction: {satisfaction}")
    
    women_optimal = sm.solve_women_optimal()
    print(f"Women-optimal matching: {women_optimal}")