"""
Stable Marriage Utils - Usage Examples

This file demonstrates various use cases for the stable matching algorithms:
1. Classic Stable Marriage Problem
2. Stable Roommates Problem
3. Hospital/Residents Problem (many-to-one matching)
4. Real-world application examples
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stable_marriage_utils.mod import (
    StableMarriage, StableRoommates, HospitalResidents,
    stable_marriage, stable_roommates, hospital_residents
)


def example_basic_stable_marriage():
    """
    Example 1: Basic Stable Marriage Problem
    
    The classic problem: match N men with N women such that
    no unmatched pair would both prefer each other over their current partners.
    """
    print("=" * 60)
    print("Example 1: Basic Stable Marriage Problem")
    print("=" * 60)
    
    # Define preferences for 4 men and 4 women
    men_preferences = {
        'Alice': ['Bob', 'Charlie', 'David', 'Eve'],
        'Frank': ['Bob', 'Eve', 'Charlie', 'David'],
        'Grace': ['Eve', 'Bob', 'Charlie', 'David'],
        'Henry': ['Bob', 'Charlie', 'Eve', 'David']
    }
    
    women_preferences = {
        'Bob': ['Alice', 'Frank', 'Grace', 'Henry'],
        'Charlie': ['Grace', 'Henry', 'Alice', 'Frank'],
        'David': ['Alice', 'Henry', 'Frank', 'Grace'],
        'Eve': ['Frank', 'Alice', 'Grace', 'Henry']
    }
    
    # Note: Using gender-neutral names to avoid confusion
    # In the classical formulation: men propose to women
    
    # Solve for men-optimal matching
    sm = StableMarriage(men_preferences, women_preferences)
    men_optimal = sm.solve()
    
    print("\nMen-optimal matching (proposers get best stable partner):")
    for proposer, acceptor in sorted(men_optimal.items()):
        print(f"  {proposer} <-> {acceptor}")
    
    # Solve for women-optimal matching
    women_optimal = sm.solve_women_optimal()
    
    print("\nWomen-optimal matching (acceptors get best stable partner):")
    for proposer, acceptor in sorted(women_optimal.items()):
        print(f"  {proposer} <-> {acceptor}")
    
    # Verify stability
    print(f"\nIs men-optimal stable? {sm.is_stable(men_optimal)}")
    print(f"Is women-optimal stable? {sm.is_stable(women_optimal)}")
    
    # Calculate satisfaction metrics
    satisfaction = sm.calculate_satisfaction(men_optimal)
    print(f"\nSatisfaction metrics for men-optimal:")
    print(f"  Men average rank: {satisfaction['men_avg']:.2f}")
    print(f"  Women average rank: {satisfaction['women_avg']:.2f}")
    print(f"  Overall average: {satisfaction['total_avg']:.2f}")


def example_college_admissions():
    """
    Example 2: College Admissions (Hospital/Residents)
    
    Real-world application: matching students to colleges
    with limited capacity at each college.
    """
    print("\n" + "=" * 60)
    print("Example 2: College Admissions Matching")
    print("=" * 60)
    
    # Students rank colleges
    students = {
        'Student_A': ['MIT', 'Stanford', 'Berkeley', 'CMU'],
        'Student_B': ['Stanford', 'MIT', 'Berkeley', 'CMU'],
        'Student_C': ['Berkeley', 'CMU', 'MIT', 'Stanford'],
        'Student_D': ['MIT', 'Berkeley', 'Stanford', 'CMU'],
        'Student_E': ['CMU', 'Berkeley', 'MIT', 'Stanford'],
        'Student_F': ['Stanford', 'CMU', 'Berkeley', 'MIT']
    }
    
    # Colleges rank students and have capacities
    colleges = {
        'MIT': (2, ['Student_A', 'Student_B', 'Student_D', 'Student_C', 'Student_E', 'Student_F']),
        'Stanford': (2, ['Student_B', 'Student_A', 'Student_F', 'Student_D', 'Student_C', 'Student_E']),
        'Berkeley': (1, ['Student_C', 'Student_D', 'Student_E', 'Student_A', 'Student_B', 'Student_F']),
        'CMU': (1, ['Student_E', 'Student_C', 'Student_F', 'Student_D', 'Student_A', 'Student_B'])
    }
    
    hr = HospitalResidents(students, colleges)
    result = hr.solve()
    
    print("\nCollege admission results:")
    for college, admitted in sorted(result.items()):
        capacity = colleges[college][0]
        print(f"  {college} (capacity {capacity}): {', '.join(admitted) if admitted else 'No admissions'}")
    
    print(f"\nIs the matching stable? {hr.is_stable(result)}")
    
    # Check student assignments
    student_to_college = {}
    for college, students_list in result.items():
        for student in students_list:
            student_to_college[student] = college
    
    print("\nStudent assignments:")
    for student in sorted(students.keys()):
        college = student_to_college.get(student, 'Not admitted')
        preference = students[student].index(college) + 1 if college in students[student] else 'N/A'
        print(f"  {student} -> {college} (preference #{preference})")


def example_medical_residency():
    """
    Example 3: Medical Residency Matching (NRMP-style)
    
    Simulates the National Resident Matching Program algorithm.
    """
    print("\n" + "=" * 60)
    print("Example 3: Medical Residency Matching")
    print("=" * 60)
    
    # Residents rank hospitals
    residents = {
        'Dr_Smith': ['County_General', 'Mercy', 'University'],
        'Dr_Jones': ['University', 'County_General', 'Mercy'],
        'Dr_Brown': ['Mercy', 'University', 'County_General'],
        'Dr_Davis': ['County_General', 'Mercy', 'University'],
        'Dr_Wilson': ['University', 'Mercy', 'County_General']
    }
    
    # Hospitals rank residents and have residency slots
    hospitals = {
        'County_General': (2, ['Dr_Smith', 'Dr_Davis', 'Dr_Jones', 'Dr_Brown', 'Dr_Wilson']),
        'Mercy': (1, ['Dr_Brown', 'Dr_Davis', 'Dr_Smith', 'Dr_Wilson', 'Dr_Jones']),
        'University': (2, ['Dr_Jones', 'Dr_Wilson', 'Dr_Brown', 'Dr_Smith', 'Dr_Davis'])
    }
    
    hr = HospitalResidents(residents, hospitals)
    result = hr.solve()
    
    print("\nResidency Match Results:")
    for hospital, matched_residents in sorted(result.items()):
        capacity = hospitals[hospital][0]
        print(f"  {hospital} ({len(matched_residents)}/{capacity} slots filled):")
        for resident in matched_residents:
            rank = hospitals[hospital][1].index(resident) + 1
            print(f"    - {resident} (hospital rank #{rank})")
    
    # Resident-optimal vs Hospital-optimal
    print("\nComparing Resident-optimal vs Hospital-optimal:")
    resident_optimal = result
    hospital_optimal = hr.solve_hospital_optimal()
    
    print("\n  Resident-optimal (residents propose):")
    for h, r in sorted(resident_optimal.items()):
        print(f"    {h}: {r}")
    
    print("\n  Hospital-optimal (hospitals propose):")
    for h, r in sorted(hospital_optimal.items()):
        print(f"    {h}: {r}")


def example_stable_roommates():
    """
    Example 4: Stable Roommates Problem
    
    Match roommates when everyone can be paired with anyone.
    Unlike stable marriage, this problem may have no solution.
    """
    print("\n" + "=" * 60)
    print("Example 4: Stable Roommates Matching")
    print("=" * 60)
    
    # 4 people, each ranks the other 3
    preferences = {
        'Alice': ['Bob', 'Charlie', 'David'],
        'Bob': ['Alice', 'David', 'Charlie'],
        'Charlie': ['David', 'Alice', 'Bob'],
        'David': ['Charlie', 'Bob', 'Alice']
    }
    
    sr = StableRoommates(preferences)
    result = sr.solve()
    
    if result:
        print("\nStable roommates found!")
        for person, roommate in sorted(result.items()):
            print(f"  {person} <-> {roommate}")
        print(f"\nIs matching stable? {sr.is_stable(result)}")
    else:
        print("\nNo stable matching exists for this preference set.")
    
    # Another example that may have no stable solution
    print("\nTrying another preference set:")
    preferences2 = {
        'A': ['B', 'C', 'D'],
        'B': ['C', 'A', 'D'],
        'C': ['A', 'B', 'D'],
        'D': ['A', 'B', 'C']
    }
    
    sr2 = StableRoommates(preferences2)
    result2 = sr2.solve()
    
    if result2:
        print("  Stable matching found:")
        for p, r in sorted(result2.items()):
            print(f"    {p} <-> {r}")
    else:
        print("  No stable matching exists (this is a known unsolvable instance)")


def example_job_matching():
    """
    Example 5: Job Matching Application
    
    Matching candidates to job positions.
    """
    print("\n" + "=" * 60)
    print("Example 5: Job Matching Application")
    print("=" * 60)
    
    # Candidates rank jobs
    candidates = {
        'Dev_Alice': ['Backend', 'Frontend', 'FullStack'],
        'Dev_Bob': ['FullStack', 'Backend', 'Frontend'],
        'Dev_Charlie': ['Frontend', 'FullStack', 'Backend']
    }
    
    # Jobs rank candidates with headcount
    jobs = {
        'Backend': (1, ['Dev_Alice', 'Dev_Bob', 'Dev_Charlie']),
        'Frontend': (1, ['Dev_Charlie', 'Dev_Alice', 'Dev_Bob']),
        'FullStack': (1, ['Dev_Bob', 'Dev_Charlie', 'Dev_Alice'])
    }
    
    hr = HospitalResidents(candidates, jobs)
    result = hr.solve()
    
    print("\nJob Matching Results:")
    for job, assigned in sorted(result.items()):
        if assigned:
            print(f"  {job}: {assigned[0]}")
        else:
            print(f"  {job}: No candidate matched")
    
    # Calculate satisfaction
    print("\nCandidate satisfaction:")
    candidate_to_job = {}
    for job, assigned in result.items():
        for candidate in assigned:
            candidate_to_job[candidate] = job
    
    for candidate in candidates:
        job = candidate_to_job.get(candidate)
        if job:
            pref_rank = candidates[candidate].index(job) + 1
            print(f"  {candidate} -> {job} (preference #{pref_rank})")
        else:
            print(f"  {candidate} -> Unmatched")


def example_analysis_tools():
    """
    Example 6: Using analysis tools
    """
    print("\n" + "=" * 60)
    print("Example 6: Matching Analysis Tools")
    print("=" * 60)
    
    men = {
        'A': ['X', 'Y', 'Z'],
        'B': ['Y', 'X', 'Z'],
        'C': ['X', 'Y', 'Z']
    }
    women = {
        'X': ['B', 'A', 'C'],
        'Y': ['A', 'B', 'C'],
        'Z': ['A', 'B', 'C']
    }
    
    sm = StableMarriage(men, women)
    
    # Find all stable matchings
    print("\nFinding all stable matchings:")
    all_stable = sm.find_all_stable_matchings()
    print(f"  Number of stable matchings: {len(all_stable)}")
    
    for i, matching in enumerate(all_stable, 1):
        print(f"\n  Matching {i}:")
        for m, w in sorted(matching.items()):
            print(f"    {m} <-> {w}")
        
        satisfaction = sm.calculate_satisfaction(matching)
        print(f"    Men avg rank: {satisfaction['men_avg']:.2f}")
        print(f"    Women avg rank: {satisfaction['women_avg']:.2f}")
    
    # Check for blocking pairs in a non-stable matching
    print("\nAnalyzing an unstable matching:")
    unstable = {'A': 'Y', 'B': 'Z', 'C': 'X'}
    print(f"  Matching: {unstable}")
    print(f"  Is stable: {sm.is_stable(unstable)}")
    
    blocking = sm.find_blocking_pairs(unstable)
    if blocking:
        print(f"  Blocking pairs: {blocking}")
        for man, woman in blocking:
            print(f"    {man} and {woman} would both prefer each other")


def example_quick_convenience():
    """
    Example 7: Quick convenience functions
    """
    print("\n" + "=" * 60)
    print("Example 7: Quick Convenience Functions")
    print("=" * 60)
    
    # Quick stable marriage
    men = {'A': ['X', 'Y'], 'B': ['Y', 'X']}
    women = {'X': ['A', 'B'], 'Y': ['B', 'A']}
    
    result = stable_marriage(men, women)
    print(f"\nQuick stable marriage: {result}")
    
    # Quick stable roommates
    prefs = {
        'P1': ['P2', 'P3', 'P4'],
        'P2': ['P1', 'P4', 'P3'],
        'P3': ['P4', 'P1', 'P2'],
        'P4': ['P3', 'P2', 'P1']
    }
    result = stable_roommates(prefs)
    print(f"Quick stable roommates: {result}")
    
    # Quick hospital/residents
    residents = {'R1': ['H1', 'H2'], 'R2': ['H2', 'H1']}
    hospitals = {'H1': (1, ['R1', 'R2']), 'H2': (1, ['R2', 'R1'])}
    result = hospital_residents(residents, hospitals)
    print(f"Quick hospital/residents: {result}")


def main():
    """Run all examples."""
    example_basic_stable_marriage()
    example_college_admissions()
    example_medical_residency()
    example_stable_roommates()
    example_job_matching()
    example_analysis_tools()
    example_quick_convenience()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()