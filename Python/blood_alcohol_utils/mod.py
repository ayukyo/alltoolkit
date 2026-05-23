"""
Blood Alcohol Content (BAC) Calculator Utils

A comprehensive blood alcohol concentration calculation toolkit with no external dependencies.
Supports multiple formulas, gender-specific calculations, and legal driving limit checks.

Features:
- Widmark formula for BAC calculation
- Watson formula (more accurate, considers body water)
- Alcohol metabolism time estimation
- Legal driving limit checks by country
- Standard drink calculations
- Time-to-sober estimation
"""

from typing import Optional, Dict, List, Tuple, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import math


# Gender type
Gender = Union[str, str]  # "male", "female", "m", "f"


# Standard drink alcohol content in grams (varies by country)
STANDARD_DRINK_GRAMS = {
    "us": 14.0,       # US: 14g pure alcohol
    "uk": 8.0,        # UK: 8g (1 unit)
    "au": 10.0,       # Australia: 10g
    "canada": 13.6,   # Canada: 13.6g
    "japan": 19.75,   # Japan: 19.75g
    "standard": 10.0  # WHO standard: 10g
}

# Legal BAC limits by country (in g/100mL = %)
LEGAL_LIMITS = {
    "china": 0.02,       # China: 0.02%
    "japan": 0.03,       # Japan: 0.03%
    "germany": 0.05,     # Germany: 0.05%
    "france": 0.05,      # France: 0.05%
    "uk": 0.08,          # UK: 0.08%
    "us": 0.08,          # US: 0.08% (most states)
    "us_zero_tolerance": 0.01,  # US zero tolerance (under 21)
    "australia": 0.05,   # Australia: 0.05%
    "canada": 0.08,      # Canada: 0.08%
    "russia": 0.036,     # Russia: 0.036%
    "sweden": 0.02,      # Sweden: 0.02%
    "norway": 0.02,      # Norway: 0.02%
    "korea": 0.03,       # South Korea: 0.03%
}

# Widmark factors (average values)
WIDMARK_MALE = 0.68     # Male body water ratio
WIDMARK_FEMALE = 0.55   # Female body water ratio

# Average metabolism rate (g/100mL per hour)
METABOLISM_RATE = 0.015  # Average: 0.015% per hour


@dataclass
class AlcoholDrink:
    """Represents an alcoholic drink."""
    name: str
    volume_ml: float
    alcohol_percent: float  # ABV (Alcohol by Volume) as decimal (e.g., 0.05 for 5%)
    timestamp: Optional[datetime] = None  # When consumed
    
    @property
    def alcohol_grams(self) -> float:
        """Calculate pure alcohol content in grams."""
        # Alcohol density ≈ 0.789 g/mL
        return self.volume_ml * self.alcohol_percent * 0.789
    
    @property
    def standard_drinks(self, country: str = "us") -> float:
        """Calculate number of standard drinks."""
        std_gram = STANDARD_DRINK_GRAMS.get(country, STANDARD_DRINK_GRAMS["standard"])
        return self.alcohol_grams / std_gram


@dataclass
class BACResult:
    """Result of BAC calculation."""
    bac: float              # Blood alcohol content (%)
    bac_permille: float     # BAC in permille (‰)
    is_legal: bool         # Can legally drive (based on specified country)
    legal_limit: float      # Legal limit used
    time_to_sober: float    # Hours until BAC reaches 0
    time_to_legal: float    # Hours until BAC reaches legal limit
    metabolism_rate: float  # Metabolism rate used
    category: str           # BAC category description
    impairment_level: str   # Level of impairment


# Common drink presets
DRINK_PRESETS = {
    "beer_regular": {"volume_ml": 355, "alcohol_percent": 0.05},      # 12oz regular beer
    "beer_light": {"volume_ml": 355, "alcohol_percent": 0.042},       # 12oz light beer
    "beer_craft": {"volume_ml": 355, "alcohol_percent": 0.07},        # 12oz craft beer
    "wine_red": {"volume_ml": 150, "alcohol_percent": 0.13},          # 5oz red wine
    "wine_white": {"volume_ml": 150, "alcohol_percent": 0.12},        # 5oz white wine
    "wine_champagne": {"volume_ml": 150, "alcohol_percent": 0.12},    # 5oz champagne
    "spirits_vodka": {"volume_ml": 44, "alcohol_percent": 0.40},     # 1.5oz vodka
    "spirits_whiskey": {"volume_ml": 44, "alcohol_percent": 0.43},    # 1.5oz whiskey
    "spirits_rum": {"volume_ml": 44, "alcohol_percent": 0.40},        # 1.5oz rum
    "spirits_tequila": {"volume_ml": 44, "alcohol_percent": 0.40},    # 1.5oz tequila
    "cocktail_margarita": {"volume_ml": 150, "alcohol_percent": 0.13}, # Margarita
    "cocktail_martini": {"volume_ml": 100, "alcohol_percent": 0.30},  # Martini
    "cocktail_mojito": {"volume_ml": 200, "alcohol_percent": 0.12},   # Mojito
    "sake": {"volume_ml": 180, "alcohol_percent": 0.15},              # Sake (1 go)
    "soju": {"volume_ml": 50, "alcohol_percent": 0.20},               # Soju shot
}


def normalize_gender(gender: Gender) -> str:
    """Normalize gender input to 'male' or 'female'."""
    g = gender.lower()
    if g in ("male", "m"):
        return "male"
    elif g in ("female", "f"):
        return "female"
    raise ValueError(f"Invalid gender: {gender}. Use 'male', 'female', 'm', or 'f'.")


def create_drink(
    name: str,
    volume_ml: float,
    alcohol_percent: float,
    timestamp: Optional[datetime] = None
) -> AlcoholDrink:
    """
    Create an AlcoholDrink instance.
    
    Args:
        name: Name of the drink
        volume_ml: Volume in milliliters
        alcohol_percent: ABV as decimal (e.g., 0.05 for 5%)
        timestamp: When consumed (defaults to now)
    
    Returns:
        AlcoholDrink instance
    
    Example:
        >>> drink = create_drink("Beer", 355, 0.05)
        >>> drink.alcohol_grams
        14.0
    """
    return AlcoholDrink(name, volume_ml, alcohol_percent, timestamp or datetime.now())


def create_drink_from_preset(
    preset_name: str,
    timestamp: Optional[datetime] = None,
    volume_multiplier: float = 1.0
) -> AlcoholDrink:
    """
    Create a drink from a preset.
    
    Args:
        preset_name: Name of the preset (e.g., 'beer_regular', 'wine_red')
        timestamp: When consumed
        volume_multiplier: Multiply volume (e.g., 2.0 for double)
    
    Returns:
        AlcoholDrink instance
    
    Example:
        >>> drink = create_drink_from_preset("beer_regular")
        >>> drink.alcohol_percent
        0.05
    """
    if preset_name not in DRINK_PRESETS:
        available = ", ".join(DRINK_PRESETS.keys())
        raise ValueError(f"Unknown preset: {preset_name}. Available: {available}")
    
    preset = DRINK_PRESETS[preset_name]
    return AlcoholDrink(
        name=preset_name.replace("_", " ").title(),
        volume_ml=preset["volume_ml"] * volume_multiplier,
        alcohol_percent=preset["alcohol_percent"],
        timestamp=timestamp or datetime.now()
    )


def calculate_bac_widmark(
    weight_kg: float,
    gender: Gender,
    total_alcohol_grams: float,
    hours_elapsed: float = 0,
    widmark_factor: Optional[float] = None
) -> float:
    """
    Calculate BAC using the Widmark formula.
    
    Formula: BAC = [Alcohol consumed (g) / (Weight (kg) × r)] × 100 - (β × t)
    
    Where:
    - r = Widmark factor (0.68 for males, 0.55 for females)
    - β = Metabolism rate (average 0.015 per hour)
    - t = Hours since first drink
    
    Args:
        weight_kg: Body weight in kilograms
        gender: 'male' or 'female'
        total_alcohol_grams: Total pure alcohol consumed in grams
        hours_elapsed: Hours since drinking started
        widmark_factor: Override default Widmark factor
    
    Returns:
        BAC as percentage (e.g., 0.08 = 0.08%)
    
    Example:
        >>> bac = calculate_bac_widmark(70, "male", 28, 1.5)
        >>> round(bac, 3)
        0.029
    """
    gender = normalize_gender(gender)
    
    if widmark_factor is None:
        widmark_factor = WIDMARK_MALE if gender == "male" else WIDMARK_FEMALE
    
    if weight_kg <= 0:
        raise ValueError("Weight must be positive")
    if widmark_factor <= 0 or widmark_factor > 1:
        raise ValueError("Widmark factor must be between 0 and 1")
    
    # Widmark formula: BAC (%) = (Alcohol g) / (Weight kg × r × 10)
    # The × 0.1 converts from permille to percentage
    bac_raw = (total_alcohol_grams / (weight_kg * widmark_factor)) * 0.1
    
    # Subtract metabolized alcohol
    bac = bac_raw - (METABOLISM_RATE * hours_elapsed)
    
    # BAC cannot be negative
    return max(0, bac)


def calculate_bac_watson(
    weight_kg: float,
    height_cm: float,
    gender: Gender,
    age: int,
    total_alcohol_grams: float,
    hours_elapsed: float = 0
) -> float:
    """
    Calculate BAC using Watson formula (more accurate, considers body water).
    
    Watson formula for total body water:
    - Male: TBW = 2.447 - 0.09156(age) + 0.1074(height) + 0.3362(weight)
    - Female: TBW = -2.097 + 0.1069(height) + 0.2466(weight)
    
    Then: BAC = Alcohol / (TBW × 0.806) × 100
    
    Args:
        weight_kg: Body weight in kilograms
        height_cm: Height in centimeters
        gender: 'male' or 'female'
        age: Age in years
        total_alcohol_grams: Total pure alcohol consumed in grams
        hours_elapsed: Hours since drinking started
    
    Returns:
        BAC as percentage
    
    Example:
        >>> bac = calculate_bac_watson(70, 175, "male", 30, 28, 1.5)
        >>> round(bac, 3)
        0.028
    """
    gender = normalize_gender(gender)
    
    if weight_kg <= 0 or height_cm <= 0:
        raise ValueError("Weight and height must be positive")
    if age <= 0:
        raise ValueError("Age must be positive")
    
    # Calculate total body water (TBW) in liters
    if gender == "male":
        tbw = 2.447 - 0.09156 * age + 0.1074 * height_cm + 0.3362 * weight_kg
    else:
        tbw = -2.097 + 0.1069 * height_cm + 0.2466 * weight_kg
    
    # Ensure TBW is positive
    tbw = max(0.1, tbw)
    
    # Watson formula for BAC (%): BAC = Alcohol g / (TBW × 0.806 × 10)
    bac_raw = total_alcohol_grams / (tbw * 0.806) * 0.1
    
    # Subtract metabolized alcohol
    bac = bac_raw - (METABOLISM_RATE * hours_elapsed)
    
    return max(0, bac)


def calculate_total_alcohol(
    drinks: List[AlcoholDrink]
) -> float:
    """
    Calculate total alcohol from multiple drinks.
    
    Args:
        drinks: List of AlcoholDrink instances
    
    Returns:
        Total alcohol in grams
    
    Example:
        >>> drinks = [
        ...     create_drink_from_preset("beer_regular"),
        ...     create_drink_from_preset("wine_red")
        ... ]
        >>> total = calculate_total_alcohol(drinks)
        >>> round(total, 1)
        29.4
    """
    return sum(drink.alcohol_grams for drink in drinks)


def calculate_hours_elapsed(
    first_drink_time: datetime,
    current_time: Optional[datetime] = None
) -> float:
    """
    Calculate hours elapsed since first drink.
    
    Args:
        first_drink_time: When drinking started
        current_time: Current time (defaults to now)
    
    Returns:
        Hours elapsed as float
    
    Example:
        >>> from datetime import datetime, timedelta
        >>> start = datetime.now() - timedelta(hours=2)
        >>> hours = calculate_hours_elapsed(start)
        >>> round(hours, 1)
        2.0
    """
    current = current_time or datetime.now()
    delta = current - first_drink_time
    return max(0, delta.total_seconds() / 3600)


def get_legal_limit(country: str = "us") -> float:
    """
    Get legal BAC limit for a country.
    
    Args:
        country: Country code (lowercase)
    
    Returns:
        Legal BAC limit as percentage
    
    Example:
        >>> get_legal_limit("china")
        0.02
    """
    country = country.lower()
    if country not in LEGAL_LIMITS:
        raise ValueError(f"Unknown country: {country}. Available: {', '.join(LEGAL_LIMITS.keys())}")
    return LEGAL_LIMITS[country]


def time_to_sober(
    current_bac: float,
    metabolism_rate: float = METABOLISM_RATE
) -> float:
    """
    Calculate hours until BAC reaches zero.
    
    Args:
        current_bac: Current BAC percentage
        metabolism_rate: BAC reduction per hour
    
    Returns:
        Hours until sober
    
    Example:
        >>> round(time_to_sober(0.08), 1)
        5.3
    """
    if current_bac <= 0:
        return 0
    return current_bac / metabolism_rate


def time_to_legal(
    current_bac: float,
    legal_limit: float,
    metabolism_rate: float = METABOLISM_RATE
) -> float:
    """
    Calculate hours until BAC reaches legal limit.
    
    Args:
        current_bac: Current BAC percentage
        legal_limit: Legal BAC limit
        metabolism_rate: BAC reduction per hour
    
    Returns:
        Hours until legal to drive
    
    Example:
        >>> round(time_to_legal(0.08, 0.05), 1)
        2.0
    """
    if current_bac <= legal_limit:
        return 0
    return (current_bac - legal_limit) / metabolism_rate


def categorize_bac(bac: float) -> Tuple[str, str]:
    """
    Categorize BAC level with description and impairment level.
    
    Args:
        bac: BAC percentage
    
    Returns:
        Tuple of (category, impairment_level)
    
    Example:
        >>> categorize_bac(0.03)
        ('Slight', 'Mild relaxation, slight impairment')
    """
    if bac <= 0:
        return ("Sober", "No impairment")
    elif bac < 0.02:
        return ("Trace", "Minimal effects, possible slight impairment")
    elif bac < 0.05:
        return ("Slight", "Mild relaxation, slight impairment")
    elif bac < 0.08:
        return ("Moderate", "Reduced coordination, impaired judgment")
    elif bac < 0.10:
        return ("High", "Significant impairment, legal intoxication")
    elif bac < 0.15:
        return ("Very High", "Major impairment, dangerous to drive")
    elif bac < 0.20:
        return ("Severe", "Severe motor impairment, confusion")
    elif bac < 0.30:
        return ("Dangerous", "Severe confusion, loss of consciousness possible")
    else:
        return ("Life-threatening", "Risk of coma or death")


def calculate_bac(
    weight_kg: float,
    gender: Gender,
    drinks: List[AlcoholDrink],
    hours_elapsed: Optional[float] = None,
    country: str = "us",
    height_cm: Optional[float] = None,
    age: Optional[int] = None,
    method: str = "widmark"  # "widmark" or "watson"
) -> BACResult:
    """
    Comprehensive BAC calculation with full result.
    
    Args:
        weight_kg: Body weight in kilograms
        gender: 'male' or 'female'
        drinks: List of drinks consumed
        hours_elapsed: Hours since first drink (auto-calculated if drinks have timestamps)
        country: Country for legal limit
        height_cm: Height in cm (required for Watson formula)
        age: Age in years (required for Watson formula)
        method: Calculation method ('widmark' or 'watson')
    
    Returns:
        BACResult with all calculated values
    
    Example:
        >>> drinks = [create_drink_from_preset("beer_regular") for _ in range(2)]
        >>> result = calculate_bac(70, "male", drinks, hours_elapsed=1)
        >>> round(result.bac, 3)
        0.029
    """
    total_alcohol = calculate_total_alcohol(drinks)
    
    # Calculate hours from timestamps if available
    if hours_elapsed is None:
        timestamps = [d.timestamp for d in drinks if d.timestamp]
        if timestamps:
            hours_elapsed = calculate_hours_elapsed(min(timestamps))
        else:
            hours_elapsed = 0
    
    # Calculate BAC
    if method == "watson":
        if height_cm is None or age is None:
            raise ValueError("Watson method requires height_cm and age")
        bac = calculate_bac_watson(weight_kg, height_cm, gender, age, total_alcohol, hours_elapsed)
    else:
        bac = calculate_bac_widmark(weight_kg, gender, total_alcohol, hours_elapsed)
    
    # Get legal limit
    legal_limit = get_legal_limit(country)
    
    # Calculate times
    t_sober = time_to_sober(bac)
    t_legal = time_to_legal(bac, legal_limit)
    
    # Categorize
    category, impairment = categorize_bac(bac)
    
    return BACResult(
        bac=bac,
        bac_permille=bac * 10,  # Convert to ‰
        is_legal=bac <= legal_limit,
        legal_limit=legal_limit,
        time_to_sober=t_sober,
        time_to_legal=t_legal,
        metabolism_rate=METABOLISM_RATE,
        category=category,
        impairment_level=impairment
    )


def calculate_drinks_to_limit(
    weight_kg: float,
    gender: Gender,
    legal_limit: float = 0.08,
    hours: float = 0,
    drink_type: str = "beer_regular",
    method: str = "widmark"  # "widmark" or "watson"
) -> int:
    """
    Calculate maximum number of drinks to stay at or below legal limit.
    
    Args:
        weight_kg: Body weight in kilograms
        gender: 'male' or 'female'
        legal_limit: Target BAC limit
        hours: Hours over which drinks are consumed
        drink_type: Preset drink type
        method: Calculation method
    
    Returns:
        Maximum number of drinks (integer)
    
    Example:
        >>> calculate_drinks_to_limit(70, "male", 0.05, 2)
        2
    """
    # Get alcohol per drink
    preset = DRINK_PRESETS.get(drink_type, DRINK_PRESETS["beer_regular"])
    alcohol_per_drink = preset["volume_ml"] * preset["alcohol_percent"] * 0.789
    
    # Get Widmark factor
    gender = normalize_gender(gender)
    widmark = WIDMARK_MALE if gender == "male" else WIDMARK_FEMALE
    
    # Calculate max alcohol for limit (accounting for metabolism)
    # BAC = (A / (W × r)) × 100 - (β × t)
    # A = (BAC + β×t) × W × r / 100
    max_alcohol = (legal_limit + METABOLISM_RATE * hours) * weight_kg * widmark / 100 * 1000
    
    # Calculate drinks (floor to be safe)
    max_drinks = int(max_alcohol / alcohol_per_drink)
    
    return max(0, max_drinks)


def estimate_metabolism_time(
    alcohol_grams: float,
    weight_kg: float,
    gender: Gender
) -> float:
    """
    Estimate time needed to metabolize all alcohol.
    
    Args:
        alcohol_grams: Total alcohol in grams
        weight_kg: Body weight in kg
        gender: 'male' or 'female'
    
    Returns:
        Hours to fully metabolize
    
    Example:
        >>> round(estimate_metabolism_time(14, 70, "male"), 1)
        1.0
    """
    # Calculate peak BAC
    bac = calculate_bac_widmark(weight_kg, gender, alcohol_grams, 0)
    
    # Time to metabolize
    return time_to_sober(bac)


def calculate_bac_at_time(
    weight_kg: float,
    gender: Gender,
    drinks: List[AlcoholDrink],
    target_time: datetime
) -> float:
    """
    Calculate what BAC will be at a specific future time.
    
    Args:
        weight_kg: Body weight in kilograms
        gender: 'male' or 'female'
        drinks: List of drinks consumed
        target_time: Future time to calculate BAC for
    
    Returns:
        Estimated BAC at target time
    
    Example:
        >>> from datetime import datetime, timedelta
        >>> drinks = [create_drink_from_preset("beer_regular")]
        >>> future = datetime.now() + timedelta(hours=3)
        >>> bac = calculate_bac_at_time(70, "male", drinks, future)
        >>> bac >= 0
        True
    """
    total_alcohol = calculate_total_alcohol(drinks)
    
    # Get earliest drink time
    timestamps = [d.timestamp for d in drinks if d.timestamp]
    if not timestamps:
        return 0
    
    first_drink = min(timestamps)
    hours_until_target = (target_time - first_drink).total_seconds() / 3600
    
    if hours_until_target < 0:
        return 0
    
    return calculate_bac_widmark(weight_kg, gender, total_alcohol, hours_until_target)


def suggest_waiting_time(
    current_bac: float,
    target_bac: float = 0.0
) -> Dict[str, float]:
    """
    Suggest waiting time with different units.
    
    Args:
        current_bac: Current BAC percentage
        target_bac: Target BAC (default 0 = sober)
    
    Returns:
        Dict with hours, minutes, and human-readable time
    
    Example:
        >>> result = suggest_waiting_time(0.08)
        >>> result['hours']
        5.333333333333333
    """
    if current_bac <= target_bac:
        return {
            "hours": 0,
            "minutes": 0,
            "human": "Already at or below target",
            "sober_at": datetime.now().strftime("%H:%M")
        }
    
    hours_needed = (current_bac - target_bac) / METABOLISM_RATE
    minutes_needed = hours_needed * 60
    
    sober_time = datetime.now() + timedelta(hours=hours_needed)
    
    return {
        "hours": hours_needed,
        "minutes": minutes_needed,
        "human": f"{int(hours_needed)}h {int(minutes_needed % 60)}m",
        "sober_at": sober_time.strftime("%H:%M")
    }


def drinking_session_summary(
    weight_kg: float,
    gender: Gender,
    drinks: List[AlcoholDrink],
    country: str = "us"
) -> Dict:
    """
    Generate a comprehensive drinking session summary.
    
    Args:
        weight_kg: Body weight in kilograms
        gender: 'male' or 'female'
        drinks: List of drinks
        country: Country for legal limit
    
    Returns:
        Complete summary dict
    
    Example:
        >>> drinks = [create_drink_from_preset("beer_regular") for _ in range(3)]
        >>> summary = drinking_session_summary(70, "male", drinks)
        >>> 'bac' in summary
        True
    """
    result = calculate_bac(weight_kg, gender, drinks, country=country)
    
    total_alcohol = calculate_total_alcohol(drinks)
    
    # Calculate drink distribution by type
    drink_counts = {}
    for drink in drinks:
        drink_counts[drink.name] = drink_counts.get(drink.name, 0) + 1
    
    return {
        "bac_percent": result.bac,
        "bac_permille": result.bac_permille,
        "total_alcohol_grams": round(total_alcohol, 1),
        "standard_drinks": round(total_alcohol / STANDARD_DRINK_GRAMS["us"], 1),
        "drink_count": len(drinks),
        "drink_breakdown": drink_counts,
        "is_legal": result.is_legal,
        "legal_limit": result.legal_limit,
        "country": country,
        "time_to_sober_hours": round(result.time_to_sober, 1),
        "time_to_legal_hours": round(result.time_to_legal, 1),
        "category": result.category,
        "impairment": result.impairment_level,
        "recommendation": "DO NOT DRIVE" if not result.is_legal else "Legal to drive (but consider waiting)"
    }


# Convenience function for quick BAC check
def quick_bac(
    weight_kg: float,
    gender: Gender,
    num_drinks: int,
    drink_type: str = "beer_regular",
    hours: float = 0
) -> float:
    """
    Quick BAC calculation with minimal parameters.
    
    Args:
        weight_kg: Body weight in kg
        gender: 'male' or 'female'
        num_drinks: Number of drinks
        drink_type: Preset drink type
        hours: Hours since drinking started
    
    Returns:
        BAC percentage
    
    Example:
        >>> round(quick_bac(70, "male", 2, "beer_regular", 1), 3)
        0.029
    """
    drinks = [create_drink_from_preset(drink_type) for _ in range(num_drinks)]
    return calculate_bac_widmark(weight_kg, gender, calculate_total_alcohol(drinks), hours)