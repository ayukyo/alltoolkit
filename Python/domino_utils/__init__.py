"""
Domino Utils - Complete domino game utilities toolkit.

This module provides comprehensive tools for domino game programming,
including tile representation, chain building, puzzle solving, and game logic.

Usage:
    from domino_utils import Domino, DominoSet, DominoChain, DominoSolver
    
    # Create a domino
    d = Domino(3, 5)  # [3|5]
    
    # Create a standard double-six set
    set = DominoSet(6)  # 28 tiles
    
    # Build a chain
    chain = DominoChain()
    chain.add(Domino(3, 5))
    chain.add(Domino(5, 2))
    
    # Solve domino solitaire
    tiles = [Domino(3, 5), Domino(5, 2), Domino(2, 4)]
    result = DominoSolver.solve_domino_solitaire(tiles)
"""

from domino_utils.domino_utils import (
    Domino,
    DominoSet,
    DominoChain,
    DominoHand,
    DominoSolver,
    DominoGame,
    domino,
    domino_set,
    find_chain,
    longest_chain,
    can_chain_all,
    deal_hands,
)

__all__ = [
    'Domino',
    'DominoSet',
    'DominoChain',
    'DominoHand',
    'DominoSolver',
    'DominoGame',
    'domino',
    'domino_set',
    'find_chain',
    'longest_chain',
    'can_chain_all',
    'deal_hands',
]

__version__ = '1.0.0'