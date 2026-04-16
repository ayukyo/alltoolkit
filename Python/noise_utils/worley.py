"""
Worley/Cellular Noise Implementation

Cellular noise algorithm by Steven Worley.
Creates cell-like patterns useful for Voronoi diagrams,
stone textures, and organic effects.
"""

import math
import random
from typing import List, Tuple, Optional, Callable


class WorleyNoise:
    """
    Worley/Cellular Noise Generator
    
    Creates cell-like patterns based on distance to nearest points.
    Supports multiple distance metrics and output modes.
    
    Example:
        noise = WorleyNoise(seed=42, num_points=10)
        # Get distance to nearest point
        value = noise.noise2d(x=1.5, y=2.3)
        # Get all distance values
        distances = noise.get_distances(x=1.5, y=2.3)
    """
    
    def __init__(
        self,
        seed: Optional[int] = None,
        num_points: int = 8,
        distance_metric: str = 'euclidean'
    ):
        """
        Initialize Worley Noise generator.
        
        Args:
            seed: Random seed for reproducibility
            num_points: Number of feature points per cell
            distance_metric: 'euclidean', 'manhattan', or 'chebyshev'
        """
        self.seed = seed
        self.num_points = num_points
        self.distance_metric = distance_metric
        self._rng = random.Random(seed)
        
        # Pre-generate feature points for each cell
        self._points_cache = {}
    
    def _distance_func(self, metric: str) -> Callable[[float, float, float, float], float]:
        """Get distance function by name."""
        def euclidean(x1, y1, x2, y2):
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
        def manhattan(x1, y1, x2, y2):
            return abs(x2 - x1) + abs(y2 - y1)
        
        def chebyshev(x1, y1, x2, y2):
            return max(abs(x2 - x1), abs(y2 - y1))
        
        funcs = {
            'euclidean': euclidean,
            'manhattan': manhattan,
            'chebyshev': chebyshev
        }
        
        return funcs.get(metric, euclidean)
    
    def _get_cell_points(self, cell_x: int, cell_y: int) -> List[Tuple[float, float]]:
        """Generate feature points for a cell."""
        key = (cell_x, cell_y)
        
        if key not in self._points_cache:
            # Seed based on cell coordinates
            cell_seed = hash((cell_x, cell_y, self.seed)) & 0xFFFFFFFF
            rng = random.Random(cell_seed)
            
            points = []
            for _ in range(self.num_points):
                px = cell_x + rng.random()
                py = cell_y + rng.random()
                points.append((px, py))
            
            self._points_cache[key] = points
        
        return self._points_cache[key]
    
    def get_distances(self, x: float, y: float) -> List[float]:
        """
        Get sorted distances to all nearby feature points.
        
        Args:
            x, y: Coordinates
            
        Returns:
            Sorted list of distances (nearest first)
        """
        cell_x = int(math.floor(x))
        cell_y = int(math.floor(y))
        
        distances = []
        distance_func = self._distance_func(self.distance_metric)
        
        # Check 3x3 neighborhood of cells
        for i in range(-1, 2):
            for j in range(-1, 2):
                nx = cell_x + i
                ny = cell_y + j
                
                points = self._get_cell_points(nx, ny)
                for px, py in points:
                    d = distance_func(x, y, px, py)
                    distances.append(d)
        
        distances.sort()
        return distances
    
    def noise2d(
        self, 
        x: float, 
        y: float,
        mode: str = 'F1'
    ) -> float:
        """
        Generate Worley noise value.
        
        Args:
            x, y: Coordinates
            mode: Output mode:
                'F1' - distance to nearest point
                'F2' - distance to second nearest
                'F2-F1' - difference between first two distances
                'F1*F2' - product of first two distances
                
        Returns:
            Noise value (typically 0 to ~1.5 for F1)
        """
        distances = self.get_distances(x, y)
        
        if len(distances) < 2:
            return 0.0
        
        if mode == 'F1':
            return distances[0]
        elif mode == 'F2':
            return distances[1]
        elif mode == 'F2-F1':
            return distances[1] - distances[0]
        elif mode == 'F1*F2':
            return distances[0] * distances[1]
        else:
            return distances[0]
    
    def __call__(self, x: float, y: float, mode: str = 'F1') -> float:
        """Convenient callable interface."""
        return self.noise2d(x, y, mode)


def worley_noise(
    x: float,
    y: float,
    seed: Optional[int] = None,
    num_points: int = 8,
    distance_metric: str = 'euclidean',
    mode: str = 'F1'
) -> float:
    """
    Generate Worley/cellular noise.
    
    Args:
        x, y: Coordinates
        seed: Optional seed for reproducibility
        num_points: Feature points per cell
        distance_metric: 'euclidean', 'manhattan', 'chebyshev'
        mode: 'F1', 'F2', 'F2-F1', or 'F1*F2'
        
    Returns:
        Noise value
    """
    noise = WorleyNoise(
        seed=seed,
        num_points=num_points,
        distance_metric=distance_metric
    )
    return noise.noise2d(x, y, mode)