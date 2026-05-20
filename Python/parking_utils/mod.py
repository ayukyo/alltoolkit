"""
parking_utils/mod.py - Parking Lot Management Utilities Module

A comprehensive parking lot management utility module providing parking space
allocation, vehicle tracking, pricing calculations, and optimization algorithms
with zero external dependencies.

Author: AllToolkit
Version: 1.0.0
License: MIT
"""

from typing import List, Dict, Optional, Tuple, Set
from datetime import datetime, timedelta
from enum import Enum
import math


# ============================================================================
# Module Metadata
# ============================================================================

PARKING_UTILS_VERSION = "1.0.0"
PARKING_UTILS_AUTHOR = "AllToolkit"


# ============================================================================
# Enums and Constants
# ============================================================================

class VehicleType(Enum):
    """Vehicle type classification."""
    MOTORCYCLE = "motorcycle"
    COMPACT = "compact"
    STANDARD = "standard"
    LARGE = "large"
    OVERSIZED = "oversized"


class ParkingSpaceType(Enum):
    """Parking space type classification."""
    MOTORCYCLE = "motorcycle"
    COMPACT = "compact"
    STANDARD = "standard"
    LARGE = "large"
    OVERSIZED = "oversized"
    ELECTRIC = "electric"
    HANDICAP = "handicap"


class ParkingStatus(Enum):
    """Parking space status."""
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"


class PricingModel(Enum):
    """Pricing model types."""
    HOURLY = "hourly"
    DAILY_MAX = "daily_max"
    FLAT_RATE = "flat_rate"
    TIERED = "tiered"
    FREE_FIRST_HOUR = "free_first_hour"


# Vehicle type to minimum space type mapping
VEHICLE_SPACE_REQUIREMENTS = {
    VehicleType.MOTORCYCLE: ParkingSpaceType.MOTORCYCLE,
    VehicleType.COMPACT: ParkingSpaceType.COMPACT,
    VehicleType.STANDARD: ParkingSpaceType.STANDARD,
    VehicleType.LARGE: ParkingSpaceType.LARGE,
    VehicleType.OVERSIZED: ParkingSpaceType.OVERSIZED,
}

# Space type hierarchy (smaller types can fit in larger spaces)
SPACE_HIERARCHY = [
    ParkingSpaceType.MOTORCYCLE,
    ParkingSpaceType.COMPACT,
    ParkingSpaceType.STANDARD,
    ParkingSpaceType.LARGE,
    ParkingSpaceType.OVERSIZED,
]


# ============================================================================
# Parking Space Class
# ============================================================================

class ParkingSpace:
    """Represents a single parking space."""
    
    def __init__(
        self,
        space_id: str,
        space_type: ParkingSpaceType,
        level: int = 0,
        row: int = 0,
        column: int = 0,
        has_ev_charger: bool = False,
        is_handicap: bool = False
    ):
        self.space_id = space_id
        self.space_type = space_type
        self.level = level
        self.row = row
        self.column = column
        self.has_ev_charger = has_ev_charger
        self.is_handicap = is_handicap
        self.status = ParkingStatus.AVAILABLE
        self.vehicle_id: Optional[str] = None
        self.entry_time: Optional[datetime] = None
        self.reserved_until: Optional[datetime] = None
    
    def is_available(self) -> bool:
        """Check if space is available for parking."""
        return self.status == ParkingStatus.AVAILABLE
    
    def can_fit_vehicle(self, vehicle_type: VehicleType) -> bool:
        """Check if this space can accommodate a vehicle type."""
        if not self.is_available():
            return False
        
        # Find minimum required space type
        required_type = VEHICLE_SPACE_REQUIREMENTS.get(vehicle_type)
        if required_type is None:
            return False
        
        # Check hierarchy - vehicle can fit in equal or larger spaces
        required_index = SPACE_HIERARCHY.index(required_type)
        space_index = SPACE_HIERARCHY.index(self.space_type)
        
        # Space must be equal or larger than required
        return space_index >= required_index
    
    def occupy(self, vehicle_id: str, entry_time: datetime) -> bool:
        """Occupy the space with a vehicle."""
        if not self.is_available():
            return False
        self.status = ParkingStatus.OCCUPIED
        self.vehicle_id = vehicle_id
        self.entry_time = entry_time
        return True
    
    def vacate(self) -> Optional[Tuple[str, datetime, datetime]]:
        """Vacate the space and return parking info."""
        if self.status != ParkingStatus.OCCUPIED:
            return None
        
        info = (self.vehicle_id, self.entry_time, datetime.now())
        self.status = ParkingStatus.AVAILABLE
        self.vehicle_id = None
        self.entry_time = None
        return info
    
    def reserve(self, until: datetime) -> bool:
        """Reserve the space until a specific time."""
        if not self.is_available():
            return False
        self.status = ParkingStatus.RESERVED
        self.reserved_until = until
        return True
    
    def release_reservation(self) -> bool:
        """Release a reservation."""
        if self.status != ParkingStatus.RESERVED:
            return False
        self.status = ParkingStatus.AVAILABLE
        self.reserved_until = None
        return True
    
    def set_maintenance(self) -> bool:
        """Put space in maintenance mode."""
        self.status = ParkingStatus.MAINTENANCE
        return True
    
    def end_maintenance(self) -> bool:
        """End maintenance and make space available."""
        if self.status == ParkingStatus.MAINTENANCE:
            self.status = ParkingStatus.AVAILABLE
            return True
        return False
    
    def get_distance_from_entrance(self, entrance_level: int, entrance_row: int, entrance_column: int) -> int:
        """Calculate distance from entrance."""
        level_dist = abs(self.level - entrance_level) * 10
        row_dist = abs(self.row - entrance_row)
        col_dist = abs(self.column - entrance_column)
        return level_dist + row_dist + col_dist
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "space_id": self.space_id,
            "space_type": self.space_type.value,
            "level": self.level,
            "row": self.row,
            "column": self.column,
            "has_ev_charger": self.has_ev_charger,
            "is_handicap": self.is_handicap,
            "status": self.status.value,
            "vehicle_id": self.vehicle_id,
            "entry_time": self.entry_time.isoformat() if self.entry_time else None,
        }


# ============================================================================
# Vehicle Class
# ============================================================================

class Vehicle:
    """Represents a vehicle."""
    
    def __init__(
        self,
        vehicle_id: str,
        vehicle_type: VehicleType,
        license_plate: Optional[str] = None,
        owner_id: Optional[str] = None,
        is_handicap_permitted: bool = False,
        needs_ev_charging: bool = False
    ):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate or vehicle_id
        self.owner_id = owner_id
        self.is_handicap_permitted = is_handicap_permitted
        self.needs_ev_charging = needs_ev_charging
    
    def get_required_space_types(self) -> List[ParkingSpaceType]:
        """Get acceptable space types for this vehicle."""
        required_type = VEHICLE_SPACE_REQUIREMENTS.get(self.vehicle_type)
        if required_type is None:
            return []
        
        required_index = SPACE_HIERARCHY.index(required_type)
        # Vehicle can fit in equal or larger spaces
        return SPACE_HIERARCHY[required_index:]
    
    def can_use_space(self, space: ParkingSpace) -> bool:
        """Check if vehicle can use a specific space."""
        # Check type compatibility
        if not space.can_fit_vehicle(self.vehicle_type):
            return False
        
        # Check handicap requirement
        if self.is_handicap_permitted and space.is_handicap:
            return True  # Handicap permitted vehicles can use handicap spaces
        
        # Handicap spaces are restricted unless vehicle has permit
        if space.is_handicap and not self.is_handicap_permitted:
            return False
        
        # EV charging requirement
        if self.needs_ev_charging and not space.has_ev_charger:
            return False
        
        return True
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "vehicle_id": self.vehicle_id,
            "vehicle_type": self.vehicle_type.value,
            "license_plate": self.license_plate,
            "owner_id": self.owner_id,
            "is_handicap_permitted": self.is_handicap_permitted,
            "needs_ev_charging": self.needs_ev_charging,
        }


# ============================================================================
# Parking Lot Class
# ============================================================================

class ParkingLot:
    """Represents a parking lot with multiple spaces."""
    
    def __init__(
        self,
        lot_id: str,
        name: str,
        levels: int = 1,
        rows_per_level: int = 10,
        columns_per_row: int = 10,
        entrance_position: Tuple[int, int, int] = (0, 0, 0)
    ):
        self.lot_id = lot_id
        self.name = name
        self.levels = levels
        self.rows_per_level = rows_per_level
        self.columns_per_row = columns_per_row
        self.entrance_level, self.entrance_row, self.entrance_column = entrance_position
        self.spaces: Dict[str, ParkingSpace] = {}
        self.pricing_config: Dict = {}
        self._initialize_spaces()
    
    def _initialize_spaces(self):
        """Initialize all parking spaces."""
        space_id_counter = 1
        
        # Create motorcycle spaces (first row of each level)
        for level in range(self.levels):
            for col in range(0, min(5, self.columns_per_row)):
                space_id = f"{self.lot_id}-M{level}{col:02d}"
                space = ParkingSpace(
                    space_id=space_id,
                    space_type=ParkingSpaceType.MOTORCYCLE,
                    level=level,
                    row=0,
                    column=col
                )
                self.spaces[space_id] = space
        
        # Create handicap spaces (second row of each level)
        for level in range(self.levels):
            for col in range(0, min(3, self.columns_per_row)):
                space_id = f"{self.lot_id}-H{level}{col:02d}"
                space = ParkingSpace(
                    space_id=space_id,
                    space_type=ParkingSpaceType.STANDARD,
                    level=level,
                    row=1,
                    column=col,
                    is_handicap=True
                )
                self.spaces[space_id] = space
        
        # Create electric spaces (third row of each level)
        for level in range(self.levels):
            for col in range(0, min(3, self.columns_per_row)):
                space_id = f"{self.lot_id}-E{level}{col:02d}"
                space = ParkingSpace(
                    space_id=space_id,
                    space_type=ParkingSpaceType.STANDARD,
                    level=level,
                    row=2,
                    column=col,
                    has_ev_charger=True
                )
                self.spaces[space_id] = space
        
        # Create remaining standard spaces
        for level in range(self.levels):
            for row in range(3, self.rows_per_level):
                for col in range(self.columns_per_row):
                    space_id = f"{self.lot_id}-S{level}{row:02d}{col:02d}"
                    space = ParkingSpace(
                        space_id=space_id,
                        space_type=ParkingSpaceType.STANDARD,
                        level=level,
                        row=row,
                        column=col
                    )
                    self.spaces[space_id] = space
    
    def set_pricing(self, pricing_config: Dict):
        """Set pricing configuration."""
        self.pricing_config = pricing_config
    
    def get_available_spaces(self) -> List[ParkingSpace]:
        """Get all available spaces."""
        return [s for s in self.spaces.values() if s.is_available()]
    
    def get_available_spaces_for_vehicle(self, vehicle: Vehicle) -> List[ParkingSpace]:
        """Get available spaces suitable for a vehicle."""
        available = self.get_available_spaces()
        return [s for s in available if vehicle.can_use_space(s)]
    
    def find_best_space(
        self,
        vehicle: Vehicle,
        strategy: str = "closest"
    ) -> Optional[ParkingSpace]:
        """Find the best parking space for a vehicle."""
        suitable_spaces = self.get_available_spaces_for_vehicle(vehicle)
        
        if not suitable_spaces:
            return None
        
        if strategy == "closest":
            # Find closest to entrance
            def distance_key(space):
                return space.get_distance_from_entrance(
                    self.entrance_level,
                    self.entrance_row,
                    self.entrance_column
                )
            suitable_spaces.sort(key=distance_key)
            return suitable_spaces[0]
        
        elif strategy == "smallest":
            # Find smallest suitable space
            def size_key(space):
                return SPACE_HIERARCHY.index(space.space_type)
            suitable_spaces.sort(key=size_key)
            return suitable_spaces[0]
        
        elif strategy == "largest":
            # Find largest suitable space
            def size_key(space):
                return -SPACE_HIERARCHY.index(space.space_type)
            suitable_spaces.sort(key=size_key)
            return suitable_spaces[0]
        
        elif strategy == "random":
            import random
            return random.choice(suitable_spaces)
        
        return suitable_spaces[0]
    
    def park_vehicle(
        self,
        vehicle: Vehicle,
        entry_time: datetime,
        strategy: str = "closest"
    ) -> Optional[str]:
        """Park a vehicle and return the space ID."""
        space = self.find_best_space(vehicle, strategy)
        if space is None:
            return None
        
        if space.occupy(vehicle.vehicle_id, entry_time):
            return space.space_id
        return None
    
    def unpark_vehicle(self, vehicle_id: str) -> Optional[Tuple[str, datetime, datetime]]:
        """Unpark a vehicle and return parking info."""
        for space in self.spaces.values():
            if space.vehicle_id == vehicle_id:
                return space.vacate()
        return None
    
    def get_space_by_vehicle(self, vehicle_id: str) -> Optional[ParkingSpace]:
        """Find the space occupied by a vehicle."""
        for space in self.spaces.values():
            if space.vehicle_id == vehicle_id:
                return space
        return None
    
    def get_occupancy_stats(self) -> Dict:
        """Get occupancy statistics."""
        total = len(self.spaces)
        occupied = sum(1 for s in self.spaces.values() if s.status == ParkingStatus.OCCUPIED)
        available = sum(1 for s in self.spaces.values() if s.status == ParkingStatus.AVAILABLE)
        reserved = sum(1 for s in self.spaces.values() if s.status == ParkingStatus.RESERVED)
        maintenance = sum(1 for s in self.spaces.values() if s.status == ParkingStatus.MAINTENANCE)
        
        return {
            "total_spaces": total,
            "occupied": occupied,
            "available": available,
            "reserved": reserved,
            "maintenance": maintenance,
            "occupancy_rate": occupied / total if total > 0 else 0,
        }
    
    def get_space_type_stats(self) -> Dict[ParkingSpaceType, Dict]:
        """Get statistics by space type."""
        stats = {}
        for space_type in ParkingSpaceType:
            type_spaces = [s for s in self.spaces.values() if s.space_type == space_type]
            total = len(type_spaces)
            occupied = sum(1 for s in type_spaces if s.status == ParkingStatus.OCCUPIED)
            stats[space_type] = {
                "total": total,
                "occupied": occupied,
                "available": total - occupied,
                "occupancy_rate": occupied / total if total > 0 else 0,
            }
        return stats
    
    def reserve_space(self, space_id: str, until: datetime) -> bool:
        """Reserve a specific space."""
        space = self.spaces.get(space_id)
        if space:
            return space.reserve(until)
        return False
    
    def set_maintenance(self, space_id: str) -> bool:
        """Put a space in maintenance."""
        space = self.spaces.get(space_id)
        if space:
            return space.set_maintenance()
        return False
    
    def end_maintenance(self, space_id: str) -> bool:
        """End maintenance for a space."""
        space = self.spaces.get(space_id)
        if space:
            return space.end_maintenance()
        return False
    
    def calculate_parking_fee(
        self,
        entry_time: datetime,
        exit_time: datetime,
        vehicle_type: VehicleType,
        space_type: ParkingSpaceType,
        is_handicap: bool = False
    ) -> float:
        """Calculate parking fee based on duration and configuration."""
        duration = exit_time - entry_time
        hours = duration.total_seconds() / 3600
        
        # Default pricing configuration
        default_config = {
            PricingModel.HOURLY: {
                ParkingSpaceType.MOTORCYCLE: 1.0,
                ParkingSpaceType.COMPACT: 2.0,
                ParkingSpaceType.STANDARD: 3.0,
                ParkingSpaceType.LARGE: 4.0,
                ParkingSpaceType.OVERSIZED: 5.0,
            },
            "daily_max": 25.0,
            "overnight_fee": 5.0,
            "lost_ticket_fee": 50.0,
        }
        
        config = self.pricing_config or default_config
        
        # Calculate fee
        hourly_rate = config.get(PricingModel.HOURLY, {}).get(space_type, 3.0)
        daily_max = config.get("daily_max", hourly_rate * 24)
        
        # Calculate days and hours
        days = int(hours // 24)
        remaining_hours = hours % 24
        
        fee = 0.0
        
        # Daily max for each full day
        fee += days * daily_max
        
        # Remaining hours
        if remaining_hours > 0:
            hour_fee = remaining_hours * hourly_rate
            # Cap at daily max
            fee += min(hour_fee, daily_max)
        
        # Overnight fee for overnight parking
        entry_hour = entry_time.hour
        exit_hour = exit_time.hour
        if entry_hour >= 22 or exit_hour <= 6:
            fee += config.get("overnight_fee", 0)
        
        # Handicap discount (50%)
        if is_handicap:
            fee *= 0.5
        
        return round(fee, 2)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "lot_id": self.lot_id,
            "name": self.name,
            "levels": self.levels,
            "rows_per_level": self.rows_per_level,
            "columns_per_row": self.columns_per_row,
            "entrance_position": (self.entrance_level, self.entrance_row, self.entrance_column),
            "occupancy_stats": self.get_occupancy_stats(),
            "total_spaces": len(self.spaces),
        }


# ============================================================================
# Parking Transaction Class
# ============================================================================

class ParkingTransaction:
    """Represents a parking transaction."""
    
    def __init__(
        self,
        transaction_id: str,
        vehicle: Vehicle,
        space: ParkingSpace,
        entry_time: datetime,
        exit_time: Optional[datetime] = None,
        fee: Optional[float] = None
    ):
        self.transaction_id = transaction_id
        self.vehicle = vehicle
        self.space = space
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.fee = fee
        self.is_active = exit_time is None
    
    def complete(self, exit_time: datetime, fee: float):
        """Complete the transaction."""
        self.exit_time = exit_time
        self.fee = fee
        self.is_active = False
    
    def get_duration_hours(self) -> float:
        """Get parking duration in hours."""
        end_time = self.exit_time or datetime.now()
        duration = end_time - self.entry_time
        return duration.total_seconds() / 3600
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "transaction_id": self.transaction_id,
            "vehicle_id": self.vehicle.vehicle_id,
            "space_id": self.space.space_id,
            "entry_time": self.entry_time.isoformat(),
            "exit_time": self.exit_time.isoformat() if self.exit_time else None,
            "fee": self.fee,
            "is_active": self.is_active,
            "duration_hours": self.get_duration_hours(),
        }


# ============================================================================
# Parking Manager Class
# ============================================================================

class ParkingManager:
    """Manages multiple parking lots and transactions."""
    
    def __init__(self):
        self.lots: Dict[str, ParkingLot] = {}
        self.vehicles: Dict[str, Vehicle] = {}
        self.transactions: Dict[str, ParkingTransaction] = {}
        self.active_transactions: Dict[str, str] = {}  # vehicle_id -> transaction_id
    
    def add_lot(self, lot: ParkingLot):
        """Add a parking lot."""
        self.lots[lot.lot_id] = lot
    
    def remove_lot(self, lot_id: str) -> bool:
        """Remove a parking lot."""
        if lot_id in self.lots:
            del self.lots[lot_id]
            return True
        return False
    
    def register_vehicle(self, vehicle: Vehicle):
        """Register a vehicle."""
        self.vehicles[vehicle.vehicle_id] = vehicle
    
    def unregister_vehicle(self, vehicle_id: str) -> bool:
        """Unregister a vehicle."""
        if vehicle_id in self.vehicles:
            del self.vehicles[vehicle_id]
            return True
        return False
    
    def park_vehicle(
        self,
        lot_id: str,
        vehicle_id: str,
        entry_time: datetime,
        strategy: str = "closest"
    ) -> Optional[str]:
        """Park a vehicle in a specific lot."""
        lot = self.lots.get(lot_id)
        vehicle = self.vehicles.get(vehicle_id)
        
        if not lot or not vehicle:
            return None
        
        # Check if vehicle is already parked
        if vehicle_id in self.active_transactions:
            return None
        
        # Find and occupy space
        space_id = lot.park_vehicle(vehicle, entry_time, strategy)
        if space_id is None:
            return None
        
        # Create transaction
        space = lot.spaces[space_id]
        transaction_id = f"TX-{vehicle_id}-{entry_time.strftime('%Y%m%d%H%M%S')}"
        transaction = ParkingTransaction(
            transaction_id=transaction_id,
            vehicle=vehicle,
            space=space,
            entry_time=entry_time
        )
        
        self.transactions[transaction_id] = transaction
        self.active_transactions[vehicle_id] = transaction_id
        
        return transaction_id
    
    def unpark_vehicle(
        self,
        vehicle_id: str,
        exit_time: datetime
    ) -> Optional[ParkingTransaction]:
        """Unpark a vehicle and complete transaction."""
        transaction_id = self.active_transactions.get(vehicle_id)
        if transaction_id is None:
            return None
        
        transaction = self.transactions[transaction_id]
        # Extract lot_id from space_id (format: "LOT-001-X...")
        space_parts = transaction.space.space_id.split("-")
        lot_id = space_parts[0] + "-" + space_parts[1] if len(space_parts) > 1 else space_parts[0]
        lot = self.lots.get(lot_id)
        
        if lot is None:
            return None
        
        # Calculate fee
        fee = lot.calculate_parking_fee(
            transaction.entry_time,
            exit_time,
            transaction.vehicle.vehicle_type,
            transaction.space.space_type,
            transaction.vehicle.is_handicap_permitted
        )
        
        # Complete transaction
        transaction.complete(exit_time, fee)
        
        # Vacate space
        lot.unpark_vehicle(vehicle_id)
        
        # Remove from active transactions
        del self.active_transactions[vehicle_id]
        
        return transaction
    
    def get_vehicle_location(self, vehicle_id: str) -> Optional[Tuple[str, str]]:
        """Get the location of a parked vehicle."""
        transaction_id = self.active_transactions.get(vehicle_id)
        if transaction_id is None:
            return None
        
        transaction = self.transactions[transaction_id]
        return (transaction.space.space_id, transaction.entry_time.isoformat())
    
    def get_lot_availability(self, lot_id: str) -> Optional[Dict]:
        """Get availability info for a lot."""
        lot = self.lots.get(lot_id)
        if lot:
            return {
                "lot_id": lot_id,
                "occupancy_stats": lot.get_occupancy_stats(),
                "space_type_stats": lot.get_space_type_stats(),
            }
        return None
    
    def find_available_lot_for_vehicle(self, vehicle: Vehicle) -> Optional[str]:
        """Find a lot with available spaces for a vehicle."""
        for lot_id, lot in self.lots.items():
            available = lot.get_available_spaces_for_vehicle(vehicle)
            if available:
                return lot_id
        return None
    
    def get_revenue_stats(self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> Dict:
        """Get revenue statistics."""
        completed_transactions = [
            t for t in self.transactions.values()
            if not t.is_active and t.fee is not None
        ]
        
        # Filter by time range
        if start_time:
            completed_transactions = [
                t for t in completed_transactions
                if t.entry_time >= start_time
            ]
        if end_time:
            completed_transactions = [
                t for t in completed_transactions
                if t.exit_time and t.exit_time <= end_time
            ]
        
        total_revenue = sum(t.fee for t in completed_transactions)
        total_transactions = len(completed_transactions)
        average_fee = total_revenue / total_transactions if total_transactions > 0 else 0
        
        return {
            "total_revenue": total_revenue,
            "total_transactions": total_transactions,
            "average_fee": average_fee,
            "active_transactions": len(self.active_transactions),
        }
    
    def get_all_occupancy(self) -> Dict:
        """Get occupancy for all lots."""
        return {
            lot_id: lot.get_occupancy_stats()
            for lot_id, lot in self.lots.items()
        }


# ============================================================================
# Pricing Calculator Functions
# ============================================================================

def calculate_hourly_parking_fee(
    hours: float,
    hourly_rate: float,
    daily_max: Optional[float] = None,
    overnight_fee: Optional[float] = None,
    is_handicap: bool = False
) -> float:
    """Calculate parking fee based on hourly rate."""
    days = int(hours // 24)
    remaining_hours = hours % 24
    
    fee = 0.0
    
    # Daily rate for full days
    if daily_max:
        fee += days * daily_max
        remaining_fee = remaining_hours * hourly_rate
        fee += min(remaining_fee, daily_max)
    else:
        fee += hours * hourly_rate
    
    # Overnight fee
    if overnight_fee and (hours >= 24 or remaining_hours >= 8):
        fee += overnight_fee
    
    # Handicap discount
    if is_handicap:
        fee *= 0.5
    
    return round(fee, 2)


def calculate_tiered_parking_fee(
    hours: float,
    tiers: List[Tuple[float, float]],
    is_handicap: bool = False
) -> float:
    """Calculate parking fee with tiered pricing.
    
    tiers: List of (hour_threshold, rate) pairs.
    Example: [(1, 0), (3, 5), (24, 10)] means:
    - First hour: free
    - Hours 1-3: $5/hour
    - Hours 3-24: $10/hour
    """
    fee = 0.0
    previous_threshold = 0.0
    
    for threshold, rate in tiers:
        if hours <= threshold:
            fee += (hours - previous_threshold) * rate
            break
        else:
            fee += (threshold - previous_threshold) * rate
            previous_threshold = threshold
    
    # If hours exceeds last threshold, use last rate
    if hours > tiers[-1][0]:
        fee += (hours - tiers[-1][0]) * tiers[-1][1]
    
    # Handicap discount
    if is_handicap:
        fee *= 0.5
    
    return round(fee, 2)


def calculate_flat_rate_fee(
    flat_rate: float,
    is_handicap: bool = False
) -> float:
    """Calculate flat rate parking fee."""
    fee = flat_rate
    if is_handicap:
        fee *= 0.5
    return round(fee, 2)


def calculate_free_first_hour_fee(
    hours: float,
    hourly_rate: float,
    daily_max: Optional[float] = None,
    is_handicap: bool = False
) -> float:
    """Calculate fee with first hour free."""
    if hours <= 1:
        return 0.0
    
    return calculate_hourly_parking_fee(
        hours - 1,
        hourly_rate,
        daily_max,
        is_handicap=is_handicap
    )


# ============================================================================
# Utility Functions
# ============================================================================

def format_duration(hours: float) -> str:
    """Format parking duration as human-readable string."""
    if hours < 1:
        minutes = int(hours * 60)
        return f"{minutes} minutes"
    
    days = int(hours // 24)
    remaining_hours = int(hours % 24)
    
    if days == 0:
        return f"{remaining_hours} hours"
    elif remaining_hours == 0:
        return f"{days} days"
    else:
        return f"{days} days, {remaining_hours} hours"


def estimate_parking_duration(
    entry_time: datetime,
    expected_exit_time: Optional[datetime] = None
) -> float:
    """Estimate parking duration in hours."""
    if expected_exit_time:
        duration = expected_exit_time - entry_time
        return duration.total_seconds() / 3600
    return 2.0  # Default 2 hours


def find_parking_optimization_score(
    space: ParkingSpace,
    vehicle: Vehicle,
    entrance_position: Tuple[int, int, int],
    weight_distance: float = 0.5,
    weight_size: float = 0.3,
    weight_features: float = 0.2
) -> float:
    """Calculate optimization score for a space.
    
    Higher score = better match.
    """
    # Distance score (closer = higher)
    distance = space.get_distance_from_entrance(*entrance_position)
    max_distance = 100  # Assume max distance
    distance_score = 1 - (distance / max_distance)
    
    # Size efficiency score (smaller fit = higher)
    required_type = VEHICLE_SPACE_REQUIREMENTS.get(vehicle.vehicle_type)
    if required_type:
        required_index = SPACE_HIERARCHY.index(required_type)
        space_index = SPACE_HIERARCHY.index(space.space_type)
        size_score = 1 - (space_index - required_index) / len(SPACE_HIERARCHY)
    else:
        size_score = 0
    
    # Features score (EV charger, handicap)
    feature_score = 0
    if vehicle.needs_ev_charging and space.has_ev_charger:
        feature_score += 0.5
    if vehicle.is_handicap_permitted and space.is_handicap:
        feature_score += 0.5
    
    # Combined score
    total_score = (
        weight_distance * distance_score +
        weight_size * size_score +
        weight_features * feature_score
    )
    
    return round(total_score, 3)


def generate_parking_report(manager: ParkingManager) -> Dict:
    """Generate a comprehensive parking report."""
    all_occupancy = manager.get_all_occupancy()
    revenue_stats = manager.get_revenue_stats()
    
    lot_details = []
    for lot_id, lot in manager.lots.items():
        lot_details.append({
            "lot_id": lot_id,
            "name": lot.name,
            "occupancy_rate": all_occupancy[lot_id]["occupancy_rate"],
            "available_spaces": all_occupancy[lot_id]["available"],
            "total_spaces": all_occupancy[lot_id]["total_spaces"],
        })
    
    return {
        "timestamp": datetime.now().isoformat(),
        "total_lots": len(manager.lots),
        "total_registered_vehicles": len(manager.vehicles),
        "lot_details": lot_details,
        "revenue_stats": revenue_stats,
        "active_parking_count": len(manager.active_transactions),
    }


def simulate_parking_scenario(
    lot: ParkingLot,
    vehicle_count: int,
    duration_hours_range: Tuple[float, float] = (1, 8),
    vehicle_type_distribution: Optional[Dict[VehicleType, float]] = None
) -> Dict:
    """Simulate a parking scenario for analysis."""
    import random
    
    # Default vehicle type distribution
    if vehicle_type_distribution is None:
        vehicle_type_distribution = {
            VehicleType.MOTORCYCLE: 0.1,
            VehicleType.COMPACT: 0.2,
            VehicleType.STANDARD: 0.5,
            VehicleType.LARGE: 0.15,
            VehicleType.OVERSIZED: 0.05,
        }
    
    # Initialize distribution
    distribution_sum = sum(vehicle_type_distribution.values())
    vehicle_type_distribution = {
        k: v / distribution_sum for k, v in vehicle_type_distribution.items()
    }
    
    # Create vehicles
    vehicles = []
    for i in range(vehicle_count):
        # Random vehicle type based on distribution
        rand_val = random.random()
        cumulative = 0
        vehicle_type = VehicleType.STANDARD
        for v_type, prob in vehicle_type_distribution.items():
            cumulative += prob
            if rand_val <= cumulative:
                vehicle_type = v_type
                break
        
        # Random features
        is_handicap = random.random() < 0.05
        needs_ev = random.random() < 0.1
        
        vehicle = Vehicle(
            vehicle_id=f"SIM-{i}",
            vehicle_type=vehicle_type,
            is_handicap_permitted=is_handicap,
            needs_ev_charging=needs_ev
        )
        vehicles.append(vehicle)
    
    # Simulate parking
    base_time = datetime.now()
    successful_parks = 0
    failed_parks = 0
    total_revenue = 0.0
    
    for vehicle in vehicles:
        entry_time = base_time + timedelta(minutes=random.randint(0, 60))
        space_id = lot.park_vehicle(vehicle, entry_time, "closest")
        
        if space_id:
            successful_parks += 1
            # Simulate exit
            duration_hours = random.uniform(*duration_hours_range)
            exit_time = entry_time + timedelta(hours=duration_hours)
            
            space = lot.spaces[space_id]
            fee = lot.calculate_parking_fee(
                entry_time,
                exit_time,
                vehicle.vehicle_type,
                space.space_type,
                vehicle.is_handicap_permitted
            )
            total_revenue += fee
            lot.unpark_vehicle(vehicle.vehicle_id)
        else:
            failed_parks += 1
    
    return {
        "total_vehicles": vehicle_count,
        "successful_parks": successful_parks,
        "failed_parks": failed_parks,
        "success_rate": successful_parks / vehicle_count,
        "total_revenue": total_revenue,
        "average_revenue_per_vehicle": total_revenue / successful_parks if successful_parks > 0 else 0,
        "final_occupancy": lot.get_occupancy_stats(),
    }


# ============================================================================
# Validation Functions
# ============================================================================

def validate_vehicle_id(vehicle_id: str) -> bool:
    """Validate vehicle ID format."""
    if not vehicle_id:
        return False
    if len(vehicle_id) < 3 or len(vehicle_id) > 50:
        return False
    # Allow alphanumeric and hyphens
    return all(c.isalnum() or c == '-' for c in vehicle_id)


def validate_space_id(space_id: str) -> bool:
    """Validate space ID format."""
    if not space_id:
        return False
    if len(space_id) < 3 or len(space_id) > 20:
        return False
    return all(c.isalnum() or c == '-' for c in space_id)


def validate_pricing_config(config: Dict) -> bool:
    """Validate pricing configuration."""
    if not isinstance(config, dict):
        return False
    
    # Check for valid pricing model
    valid_keys = [
        PricingModel.HOURLY.value,
        PricingModel.DAILY_MAX.value,
        PricingModel.FLAT_RATE.value,
        PricingModel.TIERED.value,
        PricingModel.FREE_FIRST_HOUR.value,
        "daily_max",
        "overnight_fee",
        "lost_ticket_fee",
    ]
    
    return all(key in valid_keys or isinstance(key, ParkingSpaceType) for key in config.keys())


def check_parking_capacity(
    lot: ParkingLot,
    vehicle_type: VehicleType
) -> int:
    """Check how many spaces are available for a vehicle type."""
    required_type = VEHICLE_SPACE_REQUIREMENTS.get(vehicle_type)
    if required_type is None:
        return 0
    
    required_index = SPACE_HIERARCHY.index(required_type)
    
    available_count = 0
    for space in lot.spaces.values():
        if space.is_available():
            space_index = SPACE_HIERARCHY.index(space.space_type)
            if space_index >= required_index:
                available_count += 1
    
    return available_count


def estimate_wait_time(
    lot: ParkingLot,
    vehicle_type: VehicleType,
    current_parked: int,
    avg_stay_hours: float = 2.0
) -> float:
    """Estimate wait time for parking (in minutes)."""
    available = check_parking_capacity(lot, vehicle_type)
    
    if available > 0:
        return 0.0
    
    # Calculate based on expected exits
    occupied_for_type = sum(
        1 for s in lot.spaces.values()
        if s.status == ParkingStatus.OCCUPIED and
        SPACE_HIERARCHY.index(s.space_type) >= SPACE_HIERARCHY.index(VEHICLE_SPACE_REQUIREMENTS.get(vehicle_type, ParkingSpaceType.STANDARD))
    )
    
    # Estimate wait based on average stay
    # Assumes uniform distribution of departure times
    estimated_wait = (avg_stay_hours / 2) * 60  # Convert to minutes
    
    return estimated_wait