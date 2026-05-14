"""
Cycling Utilities - Comprehensive cycling calculation toolkit.

Provides utilities for cycling-related calculations including:
- Speed, distance, time calculations
- Power estimation and training zones
- Calorie expenditure
- Gear ratio and cadence calculations
- Elevation gain and climbing metrics
"""

from typing import Optional, Tuple, List
from dataclasses import dataclass
from enum import Enum
import math


class TerrainType(Enum):
    """Terrain types affecting cycling resistance."""
    FLAT = "flat"
    ROLLING = "rolling"
    HILLY = "hilly"
    MOUNTAINOUS = "mountainous"


class RidingPosition(Enum):
    """Riding positions affecting aerodynamic drag."""
    TOPS = "tops"  # Hands on top of handlebars
    HOODS = "hoods"  # Hands on brake hoods
    DROPS = "drops"  # Hands on drop handlebars
    AERO = "aero"  # Aerodynamic position (triathlon/TT)


@dataclass
class CyclingResult:
    """Result container for cycling calculations."""
    value: float
    unit: str
    description: str


@dataclass
class GearConfig:
    """Bicycle gear configuration."""
    front_teeth: List[int]  # Chainring teeth (e.g., [50, 34] for compact)
    rear_teeth: List[int]   # Cassette teeth (e.g., [11, 12, 13, ..., 28])
    crank_length_mm: float = 172.5  # Crank arm length in mm
    wheel_diameter_mm: float = 622  # ISO 622mm (700c) wheel diameter
    tire_width_mm: float = 25  # Tire width for total wheel diameter


@dataclass
class RiderProfile:
    """Rider physical profile for power and calorie calculations."""
    weight_kg: float
    height_cm: Optional[float] = None
    age_years: Optional[int] = None
    gender: Optional[str] = None  # 'male' or 'female'
    ftp_watts: Optional[float] = None  # Functional Threshold Power


class CyclingUtils:
    """Comprehensive cycling calculation utilities."""

    # Air density at sea level (kg/m³)
    AIR_DENSITY = 1.225

    # Gravitational acceleration (m/s²)
    GRAVITY = 9.80665

    # Drag coefficients by riding position
    DRAG_COEFFICIENTS = {
        RidingPosition.TOPS: 1.15,
        RidingPosition.HOODS: 1.0,
        RidingPosition.DROPS: 0.88,
        RidingPosition.AERO: 0.75,
    }

    # Default frontal area by position (m²)
    FRONTAL_AREAS = {
        RidingPosition.TOPS: 0.55,
        RidingPosition.HOODS: 0.50,
        RidingPosition.DROPS: 0.45,
        RidingPosition.AERO: 0.35,
    }

    # Rolling resistance coefficients by surface
    ROLLING_RESISTANCE = {
        'asphalt': 0.004,
        'concrete': 0.003,
        'gravel': 0.012,
        'grass': 0.025,
        'sand': 0.050,
        'offroad': 0.020,
        'track': 0.002,
    }

    # Training zones based on FTP percentage
    TRAINING_ZONES = {
        1: (0.0, 0.55, "Active Recovery", "Very easy, conversational pace"),
        2: (0.55, 0.75, "Endurance", "Comfortable, all-day pace"),
        3: (0.75, 0.90, "Tempo", "Moderately hard, sustained effort"),
        4: (0.90, 1.05, "Threshold", "Hard, race pace, limited conversation"),
        5: (1.05, 1.20, "VO2 Max", "Very hard, 3-8 minute efforts"),
        6: (1.20, 1.50, "Anaerobic", "Extremely hard, 30s-3min efforts"),
        7: (1.50, 3.0, "Sprint", "Maximum effort, under 30 seconds"),
    }

    def __init__(
        self,
        rider: Optional[RiderProfile] = None,
        bike_weight_kg: float = 8.5,
        gear_config: Optional[GearConfig] = None
    ):
        """Initialize cycling utilities with optional rider profile.

        Args:
            rider: Rider physical profile
            bike_weight_kg: Bicycle weight in kilograms (default: 8.5kg)
            gear_config: Bicycle gear configuration
        """
        self.rider = rider
        self.bike_weight_kg = bike_weight_kg
        self.gear_config = gear_config or GearConfig(
            front_teeth=[50, 34],
            rear_teeth=[11, 12, 13, 14, 15, 17, 19, 21, 24, 28]
        )

    @property
    def total_weight(self) -> float:
        """Total weight of rider + bike in kg."""
        if self.rider:
            return self.rider.weight_kg + self.bike_weight_kg
        return self.bike_weight_kg

    # ==================== Speed/Distance/Time ====================

    def calculate_speed(
        self,
        distance_km: float,
        time_hours: float
    ) -> CyclingResult:
        """Calculate average speed from distance and time.

        Args:
            distance_km: Distance in kilometers
            time_hours: Time in hours

        Returns:
            CyclingResult with speed in km/h
        """
        if time_hours <= 0:
            raise ValueError("Time must be positive")
        speed = distance_km / time_hours
        return CyclingResult(
            value=speed,
            unit="km/h",
            description=f"Average speed for {distance_km}km in {time_hours}h"
        )

    def calculate_time(
        self,
        distance_km: float,
        speed_kmh: float
    ) -> CyclingResult:
        """Calculate time needed for a given distance at a constant speed.

        Args:
            distance_km: Distance in kilometers
            speed_kmh: Speed in km/h

        Returns:
            CyclingResult with time in hours
        """
        if speed_kmh <= 0:
            raise ValueError("Speed must be positive")
        time = distance_km / speed_kmh
        hours = int(time)
        minutes = int((time - hours) * 60)
        return CyclingResult(
            value=time,
            unit="hours",
            description=f"Time needed: {hours}h {minutes}min for {distance_km}km at {speed_kmh}km/h"
        )

    def calculate_distance(
        self,
        speed_kmh: float,
        time_hours: float
    ) -> CyclingResult:
        """Calculate distance covered at a given speed for a given time.

        Args:
            speed_kmh: Speed in km/h
            time_hours: Time in hours

        Returns:
            CyclingResult with distance in km
        """
        distance = speed_kmh * time_hours
        return CyclingResult(
            value=distance,
            unit="km",
            description=f"Distance covered: {distance:.2f}km at {speed_kmh}km/h for {time_hours}h"
        )

    def pace_to_speed(self, pace_min_km: float) -> CyclingResult:
        """Convert pace (min/km) to speed (km/h).

        Args:
            pace_min_km: Pace in minutes per kilometer

        Returns:
            CyclingResult with speed in km/h
        """
        if pace_min_km <= 0:
            raise ValueError("Pace must be positive")
        speed = 60 / pace_min_km
        return CyclingResult(
            value=speed,
            unit="km/h",
            description=f"Speed equivalent of {pace_min_km} min/km pace"
        )

    def speed_to_pace(self, speed_kmh: float) -> CyclingResult:
        """Convert speed (km/h) to pace (min/km).

        Args:
            speed_kmh: Speed in km/h

        Returns:
            CyclingResult with pace in min/km
        """
        if speed_kmh <= 0:
            raise ValueError("Speed must be positive")
        pace = 60 / speed_kmh
        return CyclingResult(
            value=pace,
            unit="min/km",
            description=f"Pace equivalent of {speed_kmh} km/h speed"
        )

    # ==================== Power Calculations ====================

    def calculate_power(
        self,
        speed_kmh: float,
        gradient_percent: float = 0,
        wind_speed_kmh: float = 0,
        riding_position: RidingPosition = RidingPosition.HOODS,
        surface: str = 'asphalt',
        drivetrain_loss_percent: float = 3
    ) -> CyclingResult:
        """Calculate required power to maintain a given speed.

        Uses the cycling power equation considering:
        - Aerodynamic drag
        - Rolling resistance
        - Gravitational resistance (climbing)
        - Drivetrain losses

        Args:
            speed_kmh: Speed in km/h
            gradient_percent: Road gradient in percent (positive = uphill)
            wind_speed_kmh: Headwind speed in km/h (positive = headwind)
            riding_position: Rider's aerodynamic position
            surface: Road surface type
            drivetrain_loss_percent: Drivetrain power loss percentage

        Returns:
            CyclingResult with power in watts
        """
        # Convert to SI units
        speed_ms = speed_kmh / 3.6
        wind_ms = wind_speed_kmh / 3.6
        gradient = gradient_percent / 100

        # Get coefficients
        cd = self.DRAG_COEFFICIENTS[riding_position]
        fa = self.FRONTAL_AREAS[riding_position]
        crr = self.ROLLING_RESISTANCE.get(surface, 0.004)

        # Effective speed (considering wind)
        effective_speed_ms = speed_ms + wind_ms

        # Aerodynamic power: P_air = 0.5 * ρ * Cd * A * v² * (v + v_wind)
        power_air = 0.5 * self.AIR_DENSITY * cd * fa * effective_speed_ms * speed_ms ** 2

        # Rolling resistance power: P_roll = m * g * Crr * v
        power_roll = self.total_weight * self.GRAVITY * crr * speed_ms

        # Gravitational power (climbing): P_grav = m * g * slope * v
        power_grav = self.total_weight * self.GRAVITY * gradient * speed_ms

        # Total power at wheel
        power_wheel = power_air + power_roll + power_grav

        # Add drivetrain losses
        power_pedal = power_wheel / (1 - drivetrain_loss_percent / 100)

        return CyclingResult(
            value=power_pedal,
            unit="W",
            description=f"Power required for {speed_kmh}km/h on {gradient_percent}% grade ({riding_position.value} position)"
        )

    def estimate_speed_from_power(
        self,
        power_watts: float,
        gradient_percent: float = 0,
        wind_speed_kmh: float = 0,
        riding_position: RidingPosition = RidingPosition.HOODS,
        surface: str = 'asphalt',
        drivetrain_loss_percent: float = 3,
        tolerance: float = 0.01
    ) -> CyclingResult:
        """Estimate speed achievable at a given power output.

        Uses iterative binary search to solve the power equation.

        Args:
            power_watts: Power output in watts
            gradient_percent: Road gradient in percent
            wind_speed_kmh: Headwind speed in km/h
            riding_position: Rider's aerodynamic position
            surface: Road surface type
            drivetrain_loss_percent: Drivetrain power loss percentage
            tolerance: Convergence tolerance for speed (km/h)

        Returns:
            CyclingResult with estimated speed in km/h
        """
        # Binary search for speed
        low, high = 0.0, 120.0  # Speed range in km/h

        while high - low > tolerance:
            mid = (low + high) / 2
            result = self.calculate_power(
                mid, gradient_percent, wind_speed_kmh,
                riding_position, surface, drivetrain_loss_percent
            )
            if result.value < power_watts:
                low = mid
            else:
                high = mid

        speed = (low + high) / 2
        return CyclingResult(
            value=speed,
            unit="km/h",
            description=f"Estimated speed at {power_watts}W on {gradient_percent}% grade"
        )

    def calculate_power_to_weight_ratio(self, power_watts: float) -> CyclingResult:
        """Calculate power-to-weight ratio (watts per kg).

        Args:
            power_watts: Power output in watts

        Returns:
            CyclingResult with power-to-weight ratio
        """
        if self.rider is None:
            raise ValueError("Rider profile required for power-to-weight calculation")

        ratio = power_watts / self.rider.weight_kg
        return CyclingResult(
            value=ratio,
            unit="W/kg",
            description=f"Power-to-weight ratio for {power_watts}W"
        )

    def get_training_zone(self, power_watts: float) -> Tuple[int, str, str]:
        """Get training zone based on power output.

        Args:
            power_watts: Power output in watts

        Returns:
            Tuple of (zone_number, zone_name, zone_description)
        """
        if self.rider is None or self.rider.ftp_watts is None:
            raise ValueError("Rider profile with FTP required for training zones")

        ftp = self.rider.ftp_watts
        ratio = power_watts / ftp

        for zone, (low, high, name, desc) in self.TRAINING_ZONES.items():
            if low <= ratio < high:
                return (zone, name, desc)

        # Zone 7 (Sprint) if above
        return (7, "Sprint", "Maximum effort, under 30 seconds")

    # ==================== Calorie Calculations ====================

    def calculate_calories(
        self,
        power_watts: float,
        duration_hours: float,
        efficiency_percent: float = 24
    ) -> CyclingResult:
        """Calculate calories burned based on power output.

        Args:
            power_watts: Average power output in watts
            duration_hours: Duration in hours
            efficiency_percent: Gross metabolic efficiency (typically 20-25%)

        Returns:
            CyclingResult with calories burned
        """
        if efficiency_percent <= 0 or efficiency_percent > 100:
            raise ValueError("Efficiency must be between 0 and 100")

        # Energy output in Joules
        energy_joules = power_watts * duration_hours * 3600

        # Convert to kilocalories (1 kcal = 4184 J)
        # Account for metabolic efficiency
        efficiency = efficiency_percent / 100
        calories = energy_joules / 4184 / efficiency

        return CyclingResult(
            value=calories,
            unit="kcal",
            description=f"Calories burned at {power_watts}W for {duration_hours}h"
        )

    def estimate_calories_from_hr(
        self,
        avg_hr: float,
        duration_hours: float,
        use_gender: Optional[str] = None
    ) -> CyclingResult:
        """Estimate calories burned from heart rate (Keytel equation).

        Args:
            avg_hr: Average heart rate in bpm
            duration_hours: Duration in hours
            use_gender: Override gender for calculation

        Returns:
            CyclingResult with estimated calories
        """
        if self.rider is None:
            raise ValueError("Rider profile required for HR-based calorie estimation")

        gender = use_gender or self.rider.gender
        if gender is None:
            raise ValueError("Gender required for HR-based calorie estimation")

        weight = self.rider.weight_kg
        age = self.rider.age_years

        if age is None:
            raise ValueError("Age required for HR-based calorie estimation")

        # Keytel equation (simplified)
        # Male: (-55.0969 + 0.6309 × HR + 0.1988 × weight + 0.2017 × age) / 4.184 × duration
        # Female: (-20.4022 + 0.4472 × HR - 0.1263 × weight + 0.074 × age) / 4.184 × duration

        if gender.lower() == 'male':
            calories = ((-55.0969 + 0.6309 * avg_hr + 0.1988 * weight + 0.2017 * age) / 4.184) * 60 * duration_hours
        else:
            calories = ((-20.4022 + 0.4472 * avg_hr - 0.1263 * weight + 0.074 * age) / 4.184) * 60 * duration_hours

        return CyclingResult(
            value=max(calories, 0),
            unit="kcal",
            description=f"Estimated calories from HR {avg_hr}bpm for {duration_hours}h"
        )

    # ==================== Gear Calculations ====================

    def calculate_gear_ratio(
        self,
        front_teeth: int,
        rear_teeth: int
    ) -> CyclingResult:
        """Calculate gear ratio from chainring and cog teeth.

        Args:
            front_teeth: Number of teeth on front chainring
            rear_teeth: Number of teeth on rear cog

        Returns:
            CyclingResult with gear ratio
        """
        if rear_teeth <= 0:
            raise ValueError("Rear teeth must be positive")

        ratio = front_teeth / rear_teeth
        return CyclingResult(
            value=ratio,
            unit=":1",
            description=f"Gear ratio: {front_teeth}T front × {rear_teeth}T rear"
        )

    def calculate_development(
        self,
        front_teeth: int,
        rear_teeth: int,
        wheel_diameter_mm: Optional[float] = None,
        tire_width_mm: Optional[float] = None
    ) -> CyclingResult:
        """Calculate development (distance traveled per crank revolution).

        Args:
            front_teeth: Number of teeth on front chainring
            rear_teeth: Number of teeth on rear cog
            wheel_diameter_mm: Override wheel diameter
            tire_width_mm: Override tire width

        Returns:
            CyclingResult with development in meters
        """
        if rear_teeth <= 0:
            raise ValueError("Rear teeth must be positive")

        # Use gear config values if not overridden
        wheel_d = wheel_diameter_mm or self.gear_config.wheel_diameter_mm
        tire_w = tire_width_mm or self.gear_config.tire_width_mm

        # Calculate effective wheel diameter (wheel + 2 × tire height)
        # Tire height ≈ tire width for road tires
        effective_diameter_mm = wheel_d + (2 * tire_w)
        effective_diameter_m = effective_diameter_mm / 1000

        # Circumference
        circumference_m = math.pi * effective_diameter_m

        # Development = circumference × gear ratio
        ratio = front_teeth / rear_teeth
        development = circumference_m * ratio

        return CyclingResult(
            value=development,
            unit="m",
            description=f"Development: {development:.2f}m per crank revolution"
        )

    def calculate_speed_from_cadence(
        self,
        cadence_rpm: float,
        front_teeth: int,
        rear_teeth: int,
        wheel_diameter_mm: Optional[float] = None,
        tire_width_mm: Optional[float] = None
    ) -> CyclingResult:
        """Calculate speed from cadence and gear selection.

        Args:
            cadence_rpm: Pedaling cadence in revolutions per minute
            front_teeth: Number of teeth on front chainring
            rear_teeth: Number of teeth on rear cog
            wheel_diameter_mm: Override wheel diameter
            tire_width_mm: Override tire width

        Returns:
            CyclingResult with speed in km/h
        """
        # Get development
        dev_result = self.calculate_development(
            front_teeth, rear_teeth,
            wheel_diameter_mm, tire_width_mm
        )

        # Speed = development × cadence
        # Convert from m/min to km/h
        speed_kmh = dev_result.value * cadence_rpm * 60 / 1000

        return CyclingResult(
            value=speed_kmh,
            unit="km/h",
            description=f"Speed at {cadence_rpm}rpm with {front_teeth}×{rear_teeth} gear"
        )

    def calculate_cadence_from_speed(
        self,
        speed_kmh: float,
        front_teeth: int,
        rear_teeth: int,
        wheel_diameter_mm: Optional[float] = None,
        tire_width_mm: Optional[float] = None
    ) -> CyclingResult:
        """Calculate required cadence for a given speed and gear.

        Args:
            speed_kmh: Target speed in km/h
            front_teeth: Number of teeth on front chainring
            rear_teeth: Number of teeth on rear cog
            wheel_diameter_mm: Override wheel diameter
            tire_width_mm: Override tire width

        Returns:
            CyclingResult with cadence in rpm
        """
        # Get development
        dev_result = self.calculate_development(
            front_teeth, rear_teeth,
            wheel_diameter_mm, tire_width_mm
        )

        # Speed in m/min
        speed_m_min = speed_kmh * 1000 / 60

        # Cadence = speed / development
        cadence = speed_m_min / dev_result.value

        return CyclingResult(
            value=cadence,
            unit="rpm",
            description=f"Cadence needed for {speed_kmh}km/h with {front_teeth}×{rear_teeth} gear"
        )

    def get_all_gear_ratios(self) -> List[Tuple[int, int, float]]:
        """Get all possible gear ratios for the configured drivetrain.

        Returns:
            List of (front_teeth, rear_teeth, ratio) sorted by ratio
        """
        ratios = []
        for front in self.gear_config.front_teeth:
            for rear in self.gear_config.rear_teeth:
                ratio = front / rear
                ratios.append((front, rear, ratio))

        return sorted(ratios, key=lambda x: x[2])

    def get_all_developments(self) -> List[Tuple[int, int, float]]:
        """Get all possible developments for the configured drivetrain.

        Returns:
            List of (front_teeth, rear_teeth, development_m) sorted by development
        """
        developments = []
        for front in self.gear_config.front_teeth:
            for rear in self.gear_config.rear_teeth:
                result = self.calculate_development(front, rear)
                developments.append((front, rear, result.value))

        return sorted(developments, key=lambda x: x[2])

    # ==================== Climbing Calculations ====================

    def calculate_gradient(
        self,
        distance_km: float,
        elevation_gain_m: float
    ) -> CyclingResult:
        """Calculate gradient percentage from distance and elevation gain.

        Args:
            distance_km: Horizontal distance in kilometers
            elevation_gain_m: Elevation gain in meters

        Returns:
            CyclingResult with gradient percentage
        """
        if distance_km <= 0:
            raise ValueError("Distance must be positive")

        gradient = (elevation_gain_m / (distance_km * 1000)) * 100
        return CyclingResult(
            value=gradient,
            unit="%",
            description=f"Gradient for {elevation_gain_m}m gain over {distance_km}km"
        )

    def calculate_elevation_gain(
        self,
        distance_km: float,
        gradient_percent: float
    ) -> CyclingResult:
        """Calculate elevation gain from distance and gradient.

        Args:
            distance_km: Distance in kilometers
            gradient_percent: Gradient percentage

        Returns:
            CyclingResult with elevation gain in meters
        """
        elevation = distance_km * 1000 * (gradient_percent / 100)
        return CyclingResult(
            value=elevation,
            unit="m",
            description=f"Elevation gain for {distance_km}km at {gradient_percent}% grade"
        )

    def calculate_vam(
        self,
        elevation_gain_m: float,
        time_hours: float
    ) -> CyclingResult:
        """Calculate VAM (Velocità Ascensionale Media) - average climbing speed.

        VAM is the rate of altitude gain in meters per hour.

        Args:
            elevation_gain_m: Elevation gain in meters
            time_hours: Time in hours

        Returns:
            CyclingResult with VAM in m/h
        """
        if time_hours <= 0:
            raise ValueError("Time must be positive")

        vam = elevation_gain_m / time_hours
        return CyclingResult(
            value=vam,
            unit="m/h",
            description=f"VAM: {elevation_gain_m}m elevation gain in {time_hours}h"
        )

    def calculate_climbing_difficulty(
        self,
        distance_km: float,
        elevation_gain_m: float
    ) -> CyclingResult:
        """Calculate climbing difficulty score (FIETS index inspired).

        The score combines gradient and length to assess overall difficulty.

        Args:
            distance_km: Distance in kilometers
            elevation_gain_m: Elevation gain in meters

        Returns:
            CyclingResult with difficulty score
        """
        if distance_km <= 0:
            raise ValueError("Distance must be positive")

        # FIETS-style formula
        # Score = (H² / D × 10) + (H - 1000) if H > 1000
        # Simplified version: gradient² × distance

        gradient = elevation_gain_m / (distance_km * 1000)
        score = (gradient ** 2) * distance_km * 100

        return CyclingResult(
            value=score,
            unit="points",
            description=f"Climbing difficulty score for {distance_km}km at {gradient*100:.1f}% avg grade"
        )

    # ==================== Efficiency & Training ====================

    def calculate_np(
        self,
        power_samples: List[float],
        sample_interval_seconds: float = 1.0
    ) -> CyclingResult:
        """Calculate Normalized Power (NP) from power samples.

        Normalized Power accounts for variability in power output
        to estimate the physiological cost of a ride.

        Args:
            power_samples: List of power readings in watts
            sample_interval_seconds: Time between samples

        Returns:
            CyclingResult with Normalized Power in watts
        """
        if len(power_samples) < 30:
            raise ValueError("Need at least 30 power samples for NP calculation")

        # Step 1: 30-second rolling average
        window = int(30 / sample_interval_seconds)
        rolling_avg = []
        for i in range(len(power_samples) - window + 1):
            avg = sum(power_samples[i:i + window]) / window
            rolling_avg.append(avg)

        # Step 2: Raise to 4th power
        fourth_powers = [p ** 4 for p in rolling_avg]

        # Step 3: Average of 4th powers
        avg_fourth = sum(fourth_powers) / len(fourth_powers)

        # Step 4: 4th root
        np = avg_fourth ** 0.25

        return CyclingResult(
            value=np,
            unit="W",
            description=f"Normalized Power from {len(power_samples)} samples"
        )

    def calculate_tss(
        self,
        np_or_avg_power: float,
        duration_hours: float,
        ftp: Optional[float] = None
    ) -> CyclingResult:
        """Calculate Training Stress Score (TSS).

        Args:
            np_or_avg_power: Normalized Power or average power in watts
            duration_hours: Duration in hours
            ftp: Override FTP (uses rider FTP if not provided)

        Returns:
            CyclingResult with TSS
        """
        if ftp is None:
            if self.rider is None or self.rider.ftp_watts is None:
                raise ValueError("FTP required for TSS calculation")
            ftp = self.rider.ftp_watts

        if ftp <= 0:
            raise ValueError("FTP must be positive")

        # TSS = (duration × NP × IF) / (FTP × 3600) × 100
        # where IF (Intensity Factor) = NP / FTP

        if np_or_avg_power > 0:
            intensity_factor = np_or_avg_power / ftp
            tss = (duration_hours * 3600 * np_or_avg_power * intensity_factor) / (ftp * 3600) * 100
        else:
            tss = 0

        return CyclingResult(
            value=tss,
            unit="TSS",
            description=f"Training Stress Score for {duration_hours}h at {np_or_avg_power:.0f}W (IF: {np_or_avg_power/ftp:.2f})"
        )

    def calculate_if(
        self,
        np_or_avg_power: float,
        ftp: Optional[float] = None
    ) -> CyclingResult:
        """Calculate Intensity Factor (IF).

        IF = Normalized Power / FTP
        Represents relative intensity of a workout.

        Args:
            np_or_avg_power: Normalized Power or average power in watts
            ftp: Override FTP (uses rider FTP if not provided)

        Returns:
            CyclingResult with Intensity Factor
        """
        if ftp is None:
            if self.rider is None or self.rider.ftp_watts is None:
                raise ValueError("FTP required for IF calculation")
            ftp = self.rider.ftp_watts

        if ftp <= 0:
            raise ValueError("FTP must be positive")

        if_val = np_or_avg_power / ftp

        return CyclingResult(
            value=if_val,
            unit="IF",
            description=f"Intensity Factor: {np_or_avg_power}W / {ftp}W FTP"
        )


# Convenience functions for quick calculations

def calculate_speed(distance_km: float, time_hours: float) -> float:
    """Quick speed calculation in km/h."""
    return CyclingUtils().calculate_speed(distance_km, time_hours).value


def calculate_time(distance_km: float, speed_kmh: float) -> float:
    """Quick time calculation in hours."""
    return CyclingUtils().calculate_time(distance_km, speed_kmh).value


def calculate_distance(speed_kmh: float, time_hours: float) -> float:
    """Quick distance calculation in km."""
    return CyclingUtils().calculate_distance(speed_kmh, time_hours).value


def calculate_power(
    speed_kmh: float,
    weight_kg: float = 75,
    gradient_percent: float = 0
) -> float:
    """Quick power estimation in watts."""
    rider = RiderProfile(weight_kg=weight_kg)
    return CyclingUtils(rider=rider).calculate_power(
        speed_kmh, gradient_percent
    ).value


def calculate_calories(power_watts: float, duration_hours: float) -> float:
    """Quick calorie estimation in kcal."""
    return CyclingUtils().calculate_calories(power_watts, duration_hours).value


def calculate_gear_ratio(front_teeth: int, rear_teeth: int) -> float:
    """Quick gear ratio calculation."""
    return CyclingUtils().calculate_gear_ratio(front_teeth, rear_teeth).value


def calculate_speed_from_cadence(
    cadence_rpm: float,
    front_teeth: int,
    rear_teeth: int
) -> float:
    """Quick speed from cadence calculation in km/h."""
    return CyclingUtils().calculate_speed_from_cadence(
        cadence_rpm, front_teeth, rear_teeth
    ).value


# Module-level exports
__all__ = [
    'CyclingUtils',
    'CyclingResult',
    'GearConfig',
    'RiderProfile',
    'TerrainType',
    'RidingPosition',
    'calculate_speed',
    'calculate_time',
    'calculate_distance',
    'calculate_power',
    'calculate_calories',
    'calculate_gear_ratio',
    'calculate_speed_from_cadence',
]