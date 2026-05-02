#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Maze Utilities Module
===================================
A comprehensive maze generation and solving utility module for Python 
with zero external dependencies.

Features:
    - Multiple maze generation algorithms (DFS, Prim, Kruskal, Eller)
    - Maze solving algorithms (DFS, BFS, A*, Dead-end filling)
    - Maze representation and conversion
    - Pathfinding utilities
    - Maze analysis and metrics
    - ASCII art visualization
    - Maze import/export (text format)

Author: AllToolkit Contributors
License: MIT
"""

import random
from typing import List, Tuple, Optional, Set, Dict
from dataclasses import dataclass
from enum import Enum
from collections import deque


# ============================================================================
# Constants and Enums
# ============================================================================

class Cell(Enum):
    """Maze cell types."""
    WALL = '#'
    PATH = ' '
    START = 'S'
    END = 'E'
    VISITED = '.'
    SOLUTION = '*'


class Direction(Enum):
    """Movement directions."""
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)


# Direction mappings
DIRECTIONS = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
OPPOSITE = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class MazeCell:
    """Represents a single maze cell."""
    x: int
    y: int
    is_wall: bool = True
    is_start: bool = False
    is_end: bool = False
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        if isinstance(other, MazeCell):
            return self.x == other.x and self.y == other.y
        return False


@dataclass
class MazeSolution:
    """Maze solution result."""
    path: List[Tuple[int, int]]
    steps: int
    algorithm: str
    visited_cells: Set[Tuple[int, int]]
    time_ms: float = 0.0
    
    def to_directions(self) -> List[str]:
        """Convert path to direction strings."""
        directions = []
        for i in range(1, len(self.path)):
            dx = self.path[i][0] - self.path[i-1][0]
            dy = self.path[i][1] - self.path[i-1][1]
            if dx == 1:
                directions.append('E')
            elif dx == -1:
                directions.append('W')
            elif dy == 1:
                directions.append('S')
            elif dy == -1:
                directions.append('N')
        return directions


@dataclass
class MazeMetrics:
    """Maze analysis metrics."""
    width: int
    height: int
    total_cells: int
    path_cells: int
    wall_cells: int
    dead_ends: int
    branching_points: int
    longest_path: int
    shortest_path: int
    difficulty_score: float


# ============================================================================
# Maze Class
# ============================================================================

class Maze:
    """
    Represents a maze with generation and solving capabilities.
    
    The maze uses a grid representation where:
    - '#' represents walls
    - ' ' represents paths
    - 'S' represents the start
    - 'E' represents the end
    """
    
    def __init__(self, width: int, height: int, seed: Optional[int] = None):
        """
        Initialize a maze.
        
        Args:
            width: Number of columns (should be odd for proper maze)
            height: Number of rows (should be odd for proper maze)
            seed: Optional random seed for reproducibility
        """
        # Ensure odd dimensions for proper maze walls
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        
        if seed is not None:
            random.seed(seed)
        
        # Initialize grid with all walls
        self.grid: List[List[str]] = [
            [Cell.WALL.value for _ in range(self.width)]
            for _ in range(self.height)
        ]
        
        self.start: Tuple[int, int] = (1, 1)
        self.end: Tuple[int, int] = (self.width - 2, self.height - 2)
        
        # Solution tracking
        self._solution: Optional[MazeSolution] = None
    
    def __str__(self) -> str:
        """Return ASCII representation of the maze."""
        return self.to_ascii()
    
    def __repr__(self) -> str:
        return f"Maze(width={self.width}, height={self.height})"
    
    def to_ascii(self, show_solution: bool = False) -> str:
        """
        Convert maze to ASCII string.
        
        Args:
            show_solution: Whether to show the solution path
        
        Returns:
            ASCII representation of the maze
        """
        grid_copy = [row[:] for row in self.grid]
        
        # Mark start and end
        sx, sy = self.start
        ex, ey = self.end
        grid_copy[sy][sx] = Cell.START.value
        grid_copy[ey][ex] = Cell.END.value
        
        # Show solution if available and requested
        if show_solution and self._solution:
            for x, y in self._solution.path:
                if (x, y) != self.start and (x, y) != self.end:
                    grid_copy[y][x] = Cell.SOLUTION.value
        
        return '\n'.join(''.join(row) for row in grid_copy)
    
    def to_dict(self) -> Dict:
        """Convert maze to dictionary representation."""
        return {
            'width': self.width,
            'height': self.height,
            'grid': self.grid,
            'start': self.start,
            'end': self.end,
        }
    
    def get_cell(self, x: int, y: int) -> str:
        """Get the value at a specific cell."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return Cell.WALL.value
    
    def set_cell(self, x: int, y: int, value: str):
        """Set the value at a specific cell."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = value
    
    def is_path(self, x: int, y: int) -> bool:
        """Check if a cell is a path."""
        return self.get_cell(x, y) in [Cell.PATH.value, Cell.START.value, Cell.END.value]
    
    def is_wall(self, x: int, y: int) -> bool:
        """Check if a cell is a wall."""
        return self.get_cell(x, y) == Cell.WALL.value
    
    def get_neighbors(self, x: int, y: int, wall_distance: int = 1) -> List[Tuple[int, int]]:
        """
        Get neighboring cells at specified distance.
        
        Args:
            x: Cell x coordinate
            y: Cell y coordinate
            wall_distance: Distance to check (1 for immediate, 2 for wall-separated)
        
        Returns:
            List of valid neighbor coordinates
        """
        neighbors = []
        for direction in DIRECTIONS:
            dx, dy = direction.value
            nx, ny = x + dx * wall_distance, y + dy * wall_distance
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))
        return neighbors
    
    def get_unvisited_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get unvisited (wall) neighbors for maze generation."""
        unvisited = []
        for nx, ny in self.get_neighbors(x, y, 2):
            if self.is_wall(nx, ny):
                unvisited.append((nx, ny))
        return unvisited
    
    # ========================================================================
    # Generation Methods
    # ========================================================================
    
    def generate_dfs(self) -> 'Maze':
        """
        Generate maze using Depth-First Search (recursive backtracker).
        
        This creates a maze with long winding corridors and few branches.
        
        Returns:
            Self for chaining
        """
        # Start from the start position
        stack = [self.start]
        self.set_cell(self.start[0], self.start[1], Cell.PATH.value)
        
        while stack:
            x, y = stack[-1]
            neighbors = self.get_unvisited_neighbors(x, y)
            
            if neighbors:
                # Choose random neighbor
                nx, ny = random.choice(neighbors)
                
                # Remove wall between current and chosen cell
                wx, wy = (x + nx) // 2, (y + ny) // 2
                self.set_cell(wx, wy, Cell.PATH.value)
                self.set_cell(nx, ny, Cell.PATH.value)
                
                stack.append((nx, ny))
            else:
                stack.pop()
        
        # Ensure end is accessible
        self.set_cell(self.end[0], self.end[1], Cell.PATH.value)
        
        return self
    
    def generate_prim(self) -> 'Maze':
        """
        Generate maze using Prim's algorithm.
        
        This creates a maze with more branches and shorter corridors.
        
        Returns:
            Self for chaining
        """
        # Initialize with start
        self.set_cell(self.start[0], self.start[1], Cell.PATH.value)
        
        # Add walls around start to the frontier
        frontier: Set[Tuple[int, int]] = set()
        for nx, ny in self.get_neighbors(self.start[0], self.start[1], 2):
            if self.is_wall(nx, ny):
                frontier.add((nx, ny))
        
        while frontier:
            # Choose random frontier cell
            x, y = random.choice(list(frontier))
            frontier.remove((x, y))
            
            # Find visited neighbors
            visited_neighbors = []
            for nx, ny in self.get_neighbors(x, y, 2):
                if self.is_path(nx, ny):
                    visited_neighbors.append((nx, ny))
            
            if visited_neighbors:
                # Connect to a random visited neighbor
                vx, vy = random.choice(visited_neighbors)
                wx, wy = (x + vx) // 2, (y + vy) // 2
                self.set_cell(wx, wy, Cell.PATH.value)
                self.set_cell(x, y, Cell.PATH.value)
                
                # Add new frontier cells
                for nx, ny in self.get_neighbors(x, y, 2):
                    if self.is_wall(nx, ny):
                        frontier.add((nx, ny))
        
        # Ensure end is accessible
        self.set_cell(self.end[0], self.end[1], Cell.PATH.value)
        
        return self
    
    def generate_kruskal(self) -> 'Maze':
        """
        Generate maze using Kruskal's algorithm.
        
        This creates a maze with uniform branch distribution.
        
        Returns:
            Self for chaining
        """
        # Create cells at odd coordinates
        cells: List[Tuple[int, int]] = []
        for y in range(1, self.height, 2):
            for x in range(1, self.width, 2):
                cells.append((x, y))
                self.set_cell(x, y, Cell.PATH.value)
        
        # Create walls between cells
        walls: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        for x, y in cells:
            for nx, ny in self.get_neighbors(x, y, 2):
                if (nx, ny) in cells:
                    walls.append(((x, y), (nx, ny)))
        
        # Shuffle walls
        random.shuffle(walls)
        
        # Union-Find data structure
        parent: Dict[Tuple[int, int], Tuple[int, int]] = {cell: cell for cell in cells}
        
        def find(cell: Tuple[int, int]) -> Tuple[int, int]:
            if parent[cell] != cell:
                parent[cell] = find(parent[cell])
            return parent[cell]
        
        def union(cell1: Tuple[int, int], cell2: Tuple[int, int]):
            root1, root2 = find(cell1), find(cell2)
            if root1 != root2:
                parent[root1] = root2
        
        # Process walls
        for (x1, y1), (x2, y2) in walls:
            if find((x1, y1)) != find((x2, y2)):
                # Remove wall between cells
                wx, wy = (x1 + x2) // 2, (y1 + y2) // 2
                self.set_cell(wx, wy, Cell.PATH.value)
                union((x1, y1), (x2, y2))
        
        return self
    
    def generate_eller(self) -> 'Maze':
        """
        Generate maze using Eller's algorithm.
        
        This creates a maze row by row, allowing for infinite maze generation.
        
        Returns:
            Self for chaining
        """
        # Initialize first row
        row = 1
        sets: Dict[int, Set[Tuple[int, int]]] = {}
        set_id = 0
        
        # Create cells for first row
        for x in range(1, self.width, 2):
            self.set_cell(x, row, Cell.PATH.value)
            sets[set_id] = {(x, row)}
            set_id += 1
        
        # Process each row
        while row < self.height - 2:
            # Randomly join adjacent cells in same row
            for x in range(1, self.width - 2, 2):
                if random.random() < 0.5:
                    # Find sets for current and next cell
                    for sid, s in sets.items():
                        if (x, row) in s:
                            current_set = sid
                        if (x + 2, row) in s:
                            next_set = sid
                    
                    if current_set != next_set:
                        # Remove wall and merge sets
                        self.set_cell(x + 1, row, Cell.PATH.value)
                        sets[current_set] |= sets[next_set]
                        del sets[next_set]
            
            # Create vertical connections
            new_sets: Dict[int, Set[Tuple[int, int]]] = {}
            new_set_id = 0
            
            for sid, s in sets.items():
                # Choose random cells to extend downward
                cells_to_extend = random.sample(list(s), random.randint(1, len(s)))
                for x, y in cells_to_extend:
                    self.set_cell(x, row + 1, Cell.PATH.value)
                    self.set_cell(x, row + 2, Cell.PATH.value)
                    new_sets[new_set_id] = {(x, row + 2)}
                    new_set_id += 1
                
                # Ensure at least one connection per set
                if not cells_to_extend and s:
                    x, y = random.choice(list(s))
                    self.set_cell(x, row + 1, Cell.PATH.value)
                    self.set_cell(x, row + 2, Cell.PATH.value)
                    new_sets[new_set_id] = {(x, row + 2)}
                    new_set_id += 1
            
            # Fill remaining cells in new row
            for x in range(1, self.width, 2):
                if self.is_wall(x, row + 2):
                    self.set_cell(x, row + 2, Cell.PATH.value)
                    new_sets[new_set_id] = {(x, row + 2)}
                    new_set_id += 1
            
            sets = new_sets
            row += 2
        
        # Final row - connect all remaining sets
        for x in range(1, self.width - 2, 2):
            self.set_cell(x + 1, self.height - 2, Cell.PATH.value)
        
        return self
    
    # ========================================================================
    # Solving Methods
    # ========================================================================
    
    def solve_dfs(self) -> Optional[MazeSolution]:
        """
        Solve maze using Depth-First Search.
        
        Returns:
            MazeSolution if path found, None otherwise
        """
        stack = [(self.start, [self.start])]
        visited: Set[Tuple[int, int]] = {self.start}
        
        while stack:
            (x, y), path = stack.pop()
            
            if (x, y) == self.end:
                self._solution = MazeSolution(
                    path=path,
                    steps=len(path) - 1,
                    algorithm='DFS',
                    visited_cells=visited
                )
                return self._solution
            
            for dx, dy in [d.value for d in DIRECTIONS]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited and self.is_path(nx, ny):
                    visited.add((nx, ny))
                    stack.append(((nx, ny), path + [(nx, ny)]))
        
        return None
    
    def solve_bfs(self) -> Optional[MazeSolution]:
        """
        Solve maze using Breadth-First Search.
        
        This finds the shortest path.
        
        Returns:
            MazeSolution if path found, None otherwise
        """
        queue = deque([(self.start, [self.start])])
        visited: Set[Tuple[int, int]] = {self.start}
        
        while queue:
            (x, y), path = queue.popleft()
            
            if (x, y) == self.end:
                self._solution = MazeSolution(
                    path=path,
                    steps=len(path) - 1,
                    algorithm='BFS',
                    visited_cells=visited
                )
                return self._solution
            
            for dx, dy in [d.value for d in DIRECTIONS]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited and self.is_path(nx, ny):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        
        return None
    
    def solve_a_star(self) -> Optional[MazeSolution]:
        """
        Solve maze using A* algorithm.
        
        This is efficient for finding shortest paths.
        
        Returns:
            MazeSolution if path found, None otherwise
        """
        def heuristic(x: int, y: int) -> int:
            """Manhattan distance to end."""
            return abs(x - self.end[0]) + abs(y - self.end[1])
        
        # Priority queue (simplified with list)
        open_set: List[Tuple[int, Tuple[int, int], List[Tuple[int, int]]]] = [
            (heuristic(*self.start), self.start, [self.start])
        ]
        visited: Set[Tuple[int, int]] = {self.start}
        g_score: Dict[Tuple[int, int], int] = {self.start: 0}
        
        while open_set:
            # Find node with lowest f score
            open_set.sort(key=lambda x: x[0])
            f, (x, y), path = open_set.pop(0)
            
            if (x, y) == self.end:
                self._solution = MazeSolution(
                    path=path,
                    steps=len(path) - 1,
                    algorithm='A*',
                    visited_cells=visited
                )
                return self._solution
            
            for dx, dy in [d.value for d in DIRECTIONS]:
                nx, ny = x + dx, y + dy
                if self.is_path(nx, ny):
                    new_g = g_score[(x, y)] + 1
                    
                    if (nx, ny) not in g_score or new_g < g_score[(nx, ny)]:
                        g_score[(nx, ny)] = new_g
                        f_score = new_g + heuristic(nx, ny)
                        open_set.append((f_score, (nx, ny), path + [(nx, ny)]))
                        visited.add((nx, ny))
        
        return None
    
    def solve_dead_end_filling(self) -> Optional[MazeSolution]:
        """
        Solve maze using dead-end filling algorithm.
        
        This works by filling in dead ends until only the solution remains.
        
        Returns:
            MazeSolution if path found, None otherwise
        """
        # Create a copy of the grid
        grid_copy = [row[:] for row in self.grid]
        
        def is_dead_end(x: int, y: int) -> bool:
            """Check if a cell is a dead end (has exactly one path neighbor)."""
            if grid_copy[y][x] != Cell.PATH.value:
                return False
            if (x, y) == self.start or (x, y) == self.end:
                return False
            
            path_neighbors = 0
            for dx, dy in [d.value for d in DIRECTIONS]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if grid_copy[ny][nx] in [Cell.PATH.value, Cell.START.value, Cell.END.value]:
                        path_neighbors += 1
            
            return path_neighbors == 1
        
        # Fill dead ends iteratively
        changed = True
        while changed:
            changed = False
            for y in range(self.height):
                for x in range(self.width):
                    if is_dead_end(x, y):
                        grid_copy[y][x] = Cell.WALL.value
                        changed = True
        
        # Find remaining path
        path: List[Tuple[int, int]] = []
        visited: Set[Tuple[int, int]] = set()
        
        # Trace path from start
        current = self.start
        while current != self.end:
            path.append(current)
            visited.add(current)
            
            for dx, dy in [d.value for d in DIRECTIONS]:
                nx, ny = current[0] + dx, current[1] + dy
                if (nx, ny) not in visited and 0 <= nx < self.width and 0 <= ny < self.height:
                    if grid_copy[ny][nx] in [Cell.PATH.value, Cell.END.value]:
                        current = (nx, ny)
                        break
        
        path.append(self.end)
        
        self._solution = MazeSolution(
            path=path,
            steps=len(path) - 1,
            algorithm='Dead-End Filling',
            visited_cells=set(path)
        )
        
        return self._solution
    
    # ========================================================================
    # Analysis Methods
    # ========================================================================
    
    def analyze(self) -> MazeMetrics:
        """
        Analyze maze and return metrics.
        
        Returns:
            MazeMetrics with analysis results
        """
        path_cells = 0
        wall_cells = 0
        dead_ends = 0
        branching_points = 0
        
        for y in range(self.height):
            for x in range(self.width):
                if self.is_path(x, y):
                    path_cells += 1
                    
                    # Count path neighbors
                    path_neighbors = sum(
                        1 for dx, dy in [d.value for d in DIRECTIONS]
                        if self.is_path(x + dx, y + dy)
                    )
                    
                    if (x, y) not in [self.start, self.end]:
                        if path_neighbors == 1:
                            dead_ends += 1
                        elif path_neighbors > 2:
                            branching_points += 1
                else:
                    wall_cells += 1
        
        # Calculate path lengths
        bfs_solution = self.solve_bfs()
        dfs_solution = self.solve_dfs()
        
        shortest_path = bfs_solution.steps if bfs_solution else 0
        longest_path = dfs_solution.steps if dfs_solution else 0
        
        # Difficulty score (0-100)
        # Higher score = more difficult
        difficulty = (
            (dead_ends / path_cells) * 30 +  # Dead ends add difficulty
            (branching_points / path_cells) * 20 +  # Branching adds difficulty
            (shortest_path / (self.width + self.height)) * 50  # Path length
        )
        
        return MazeMetrics(
            width=self.width,
            height=self.height,
            total_cells=self.width * self.height,
            path_cells=path_cells,
            wall_cells=wall_cells,
            dead_ends=dead_ends,
            branching_points=branching_points,
            longest_path=longest_path,
            shortest_path=shortest_path,
            difficulty_score=min(100, difficulty)
        )
    
    def find_dead_ends(self) -> List[Tuple[int, int]]:
        """
        Find all dead ends in the maze.
        
        Returns:
            List of dead end coordinates
        """
        dead_ends = []
        
        for y in range(self.height):
            for x in range(self.width):
                if self.is_path(x, y) and (x, y) not in [self.start, self.end]:
                    path_neighbors = sum(
                        1 for dx, dy in [d.value for d in DIRECTIONS]
                        if self.is_path(x + dx, y + dy)
                    )
                    if path_neighbors == 1:
                        dead_ends.append((x, y))
        
        return dead_ends
    
    def find_branching_points(self) -> List[Tuple[int, int]]:
        """
        Find all branching points (junctions) in the maze.
        
        Returns:
            List of branching point coordinates
        """
        branches = []
        
        for y in range(self.height):
            for x in range(self.width):
                if self.is_path(x, y):
                    path_neighbors = sum(
                        1 for dx, dy in [d.value for d in DIRECTIONS]
                        if self.is_path(x + dx, y + dy)
                    )
                    if path_neighbors > 2:
                        branches.append((x, y))
        
        return branches


# ============================================================================
# Factory Functions
# ========================================================================

def create_maze(width: int, height: int, algorithm: str = 'dfs', seed: Optional[int] = None) -> Maze:
    """
    Create a maze with specified parameters.
    
    Args:
        width: Maze width
        height: Maze height
        algorithm: Generation algorithm ('dfs', 'prim', 'kruskal', 'eller')
        seed: Optional random seed
    
    Returns:
        Generated Maze
    
    Examples:
        >>> maze = create_maze(21, 21, 'dfs')
        >>> print(maze)
    """
    maze = Maze(width, height, seed)
    
    algorithm = algorithm.lower()
    
    if algorithm == 'dfs':
        maze.generate_dfs()
    elif algorithm == 'prim':
        maze.generate_prim()
    elif algorithm == 'kruskal':
        maze.generate_kruskal()
    elif algorithm == 'eller':
        maze.generate_eller()
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    
    return maze


def solve_maze(maze: Maze, algorithm: str = 'bfs') -> Optional[MazeSolution]:
    """
    Solve a maze with specified algorithm.
    
    Args:
        maze: Maze to solve
        algorithm: Solving algorithm ('dfs', 'bfs', 'a_star', 'dead_end_filling')
    
    Returns:
        MazeSolution if found, None otherwise
    
    Examples:
        >>> maze = create_maze(21, 21)
        >>> solution = solve_maze(maze, 'bfs')
        >>> print(solution.steps)
    """
    algorithm = algorithm.lower()
    
    if algorithm == 'dfs':
        return maze.solve_dfs()
    elif algorithm == 'bfs':
        return maze.solve_bfs()
    elif algorithm == 'a_star':
        return maze.solve_a_star()
    elif algorithm == 'dead_end_filling':
        return maze.solve_dead_end_filling()
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")


def maze_from_string(text: str) -> Maze:
    """
    Create a maze from a text string.
    
    Args:
        text: ASCII maze representation
    
    Returns:
        Maze object
    
    Examples:
        >>> text = '''
        ... #####
        ... #S  #
        ... # #E#
        ... #####
        ... '''
        >>> maze = maze_from_string(text)
    """
    lines = [line for line in text.strip().split('\n') if line]
    
    if not lines:
        raise ValueError("Empty maze string")
    
    height = len(lines)
    width = max(len(line) for line in lines)
    
    maze = Maze(width, height)
    
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            maze.set_cell(x, y, char)
            
            if char == Cell.START.value:
                maze.start = (x, y)
            elif char == Cell.END.value:
                maze.end = (x, y)
    
    return maze


def compare_solvers(maze: Maze) -> Dict[str, MazeSolution]:
    """
    Compare all solving algorithms on a maze.
    
    Args:
        maze: Maze to solve
    
    Returns:
        Dictionary of algorithm name to MazeSolution
    
    Examples:
        >>> maze = create_maze(21, 21)
        >>> results = compare_solvers(maze)
        >>> for name, sol in results.items():
        ...     print(f"{name}: {sol.steps} steps")
    """
    results = {}
    
    for algorithm in ['dfs', 'bfs', 'a_star', 'dead_end_filling']:
        solution = solve_maze(maze, algorithm)
        if solution:
            results[algorithm] = solution
    
    return results


# ============================================================================
# Utility Functions
# ============================================================================

def print_maze_with_solution(maze: Maze) -> None:
    """
    Print maze with solution path highlighted.
    
    Args:
        maze: Maze to print
    """
    if maze._solution:
        print(maze.to_ascii(show_solution=True))
    else:
        print("No solution available. Solve the maze first.")


def get_path_directions(solution: MazeSolution) -> List[str]:
    """
    Convert solution path to direction strings.
    
    Args:
        solution: Maze solution
    
    Returns:
        List of direction strings ('N', 'S', 'E', 'W')
    
    Examples:
        >>> maze = create_maze(7, 7)
        >>> sol = solve_maze(maze)
        >>> directions = get_path_directions(sol)
    """
    return solution.to_directions()


def generate_maze_collection(count: int, min_size: int = 11, max_size: int = 31) -> List[Maze]:
    """
    Generate a collection of mazes with various sizes.
    
    Args:
        count: Number of mazes to generate
        min_size: Minimum maze size
        max_size: Maximum maze size
    
    Returns:
        List of generated mazes
    
    Examples:
        >>> mazes = generate_maze_collection(5)
        >>> len(mazes)
        5
    """
    mazes = []
    algorithms = ['dfs', 'prim', 'kruskal', 'eller']
    
    for i in range(count):
        size = random.randint(min_size, max_size)
        if size % 2 == 0:
            size += 1
        algorithm = algorithms[i % len(algorithms)]
        maze = create_maze(size, size, algorithm)
        mazes.append(maze)
    
    return mazes


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=== Maze Generation Demo ===")
    
    # Generate mazes with different algorithms
    algorithms = ['DFS', 'Prim', 'Kruskal', 'Eller']
    
    for algo in algorithms:
        print(f"\n--- {algo} Algorithm ---")
        maze = create_maze(15, 15, algo.lower())
        print(maze)
    
    print("\n=== Maze Solving Demo ===")
    
    maze = create_maze(21, 21, 'dfs')
    print("\nOriginal Maze:")
    print(maze)
    
    # Solve with different algorithms
    results = compare_solvers(maze)
    
    for name, solution in results.items():
        print(f"\n--- {name} Solution ({solution.steps} steps) ---")
        print_maze_with_solution(maze)
    
    print("\n=== Maze Analysis Demo ===")
    metrics = maze.analyze()
    print(f"Width: {metrics.width}, Height: {metrics.height}")
    print(f"Path cells: {metrics.path_cells}, Wall cells: {metrics.wall_cells}")
    print(f"Dead ends: {metrics.dead_ends}, Branching points: {metrics.branching_points}")
    print(f"Shortest path: {metrics.shortest_path}, Longest path: {metrics.longest_path}")
    print(f"Difficulty score: {metrics.difficulty_score:.1f}/100")