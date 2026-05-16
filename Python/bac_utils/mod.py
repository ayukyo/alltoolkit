"""
Blood Alcohol Content (BAC) Calculator Utils

A comprehensive BAC calculator with zero external dependencies.
Uses the Widmark formula and provides impairment level assessments.

Features:
- BAC calculation based on Widmark formula
- Time-to-sober estimation
- Impairment level descriptions
- Legal limit comparisons for multiple countries
- Drink tracking and metabolization calculation
"""

from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class Gender(Enum):
    """Gender for BAC calculation (affects alcohol distribution ratio)."""
    MALE = "male"
    FEMALE = "female"


class ImpairmentLevel(Enum):
    """Impairment levels based on BAC."""
    SOBER = "sober"                    # 0.00% - 0.02%
    MILD = "mild"                      # 0.02% - 0.05%
    MODERATE = "moderate"              # 0.05% - 0.10%
    SIGNIFICANT = "significant"        # 0.10% - 0.15%
    SEVERE = "severe"                  # 0.15% - 0.20%
    DANGEROUS = "dangerous"            # 0.20% - 0.30%
    LIFE_THREATENING = "life_threatening"  # 0.30%+


@dataclass
class Drink:
    """Represents an alcoholic drink."""
    name: str
    alcohol_grams: float  # Total alcohol in grams
    consumed_at: Optional[datetime] = None
    
    @classmethod
    def from_standard(cls, name: str, units: float = 1.0, consumed_at: Optional[datetime] = None) -> 'Drink':
        """
        Create a drink from standard drink units.
        One standard drink = 10g alcohol (US: 14g, UK: 8g)
        Default uses international standard (10g).
        """
        return cls(name=name, alcohol_grams=units * 10.0, consumed_at=consumed_at)
    
    @classmethod
    def from_beer(cls, volume_ml: float, abv: float = 5.0, name: str = "Beer", 
                  consumed_at: Optional[datetime] = None) -> 'Drink':
        """Create a drink from beer volume and ABV (Alcohol By Volume)."""
        # Alcohol (g) = volume (ml) * ABV% * 0.789 (density of ethanol)
        alcohol_grams = volume_ml * (abv / 100) * 0.789
        return cls(name=name, alcohol_grams=alcohol_grams, consumed_at=consumed_at)
    
    @classmethod
    def from_wine(cls, volume_ml: float, abv: float = 12.0, name: str = "Wine",
                  consumed_at: Optional[datetime] = None) -> 'Drink':
        """Create a drink from wine volume and ABV."""
        alcohol_grams = volume_ml * (abv / 100) * 0.789
        return cls(name=name, alcohol_grams=alcohol_grams, consumed_at=consumed_at)
    
    @classmethod
    def from_spirit(cls, volume_ml: float, abv: float = 40.0, name: str = "Spirit",
                    consumed_at: Optional[datetime] = None) -> 'Drink':
        """Create a drink from spirit volume and ABV."""
        alcohol_grams = volume_ml * (abv / 100) * 0.789
        return cls(name=name, alcohol_grams=alcohol_grams, consumed_at=consumed_at)


@dataclass
class BACResult:
    """Result of BAC calculation."""
    bac: float                  # Blood Alcohol Content (percentage)
    impairment: ImpairmentLevel
    description: str
    time_to_sober: float        # Hours until BAC reaches 0.00%
    time_to_drive: float        # Hours until legal driving limit
    is_legal_to_drive: bool
    confidence: str             # Confidence level of estimate


# Legal driving limits by country (BAC percentage)
LEGAL_LIMITS: Dict[str, float] = {
    "CN": 0.02,    # China
    "US": 0.08,    # United States (most states)
    "UK": 0.08,    # United Kingdom
    "DE": 0.05,    # Germany
    "FR": 0.05,    # France
    "JP": 0.03,    # Japan
    "AU": 0.05,    # Australia
    "CA": 0.08,    # Canada
    "NZ": 0.05,    # New Zealand
    "SE": 0.02,    # Sweden
    "NO": 0.02,    # Norway
    "RU": 0.03,    # Russia
    "BR": 0.00,    # Brazil (zero tolerance)
    "IN": 0.03,    # India
    "KR": 0.03,    # South Korea
    "TW": 0.03,    # Taiwan
    "SG": 0.08,    # Singapore
    "HK": 0.05,    # Hong Kong
    "IT": 0.05,    # Italy
    "ES": 0.05,    # Spain
    "NL": 0.05,    # Netherlands
    "PL": 0.02,    # Poland
    "CZ": 0.00,    # Czech Republic (zero tolerance)
    "HU": 0.00,    # Hungary (zero tolerance)
}

# Widmark factors (alcohol distribution ratio)
WIDMARK_MALE = 0.68
WIDMARK_FEMALE = 0.55

# Metabolism rate (BAC reduction per hour)
# Average: 0.015% per hour, range: 0.01-0.02%
METABOLISM_RATE_MIN = 0.01
METABOLISM_RATE_AVG = 0.015
METABOLISM_RATE_MAX = 0.02


def get_widmark_factor(gender: Gender) -> float:
    """Get the Widmark factor for alcohol distribution."""
    return WIDMARK_MALE if gender == Gender.MALE else WIDMARK_FEMALE


def calculate_bac(
    weight_kg: float,
    gender: Gender,
    alcohol_grams: float,
    hours_since_first_drink: float,
    metabolism_rate: float = METABOLISM_RATE_AVG
) -> float:
    """
    Calculate Blood Alcohol Content using the Widmark formula.
    
    BAC = (Alcohol in grams) / (Weight in grams × r) × 100 - (Metabolism × Hours)
    
    Args:
        weight_kg: Body weight in kilograms
        gender: Male or Female (affects distribution ratio)
        alcohol_grams: Total alcohol consumed in grams
        hours_since_first_drink: Time since first drink in hours
        metabolism_rate: BAC reduction per hour (default 0.015%)
    
    Returns:
        BAC as a percentage (e.g., 0.08 means 0.08%)
    """
    if weight_kg <= 0 or hours_since_first_drink < 0:
        return 0.0
    
    widmark_factor = get_widmark_factor(gender)
    weight_grams = weight_kg * 1000
    
    # Calculate raw BAC
    bac = (alcohol_grams / (weight_grams * widmark_factor)) * 100
    
    # Apply metabolism (body eliminates alcohol over time)
    bac_eliminated = metabolism_rate * hours_since_first_drink
    bac = max(0, bac - bac_eliminated)
    
    return bac


def calculate_bac_from_drinks(
    weight_kg: float,
    gender: Gender,
    drinks: List[Drink],
    current_time: Optional[datetime] = None,
    metabolism_rate: float = METABOLISM_RATE_AVG
) -> float:
    """
    Calculate current BAC from a list of drinks with timestamps.
    
    Args:
        weight_kg: Body weight in kilograms
        gender: Male or Female
        drinks: List of Drink objects with consumption times
        current_time: Current time (defaults to now)
        metabolism_rate: BAC reduction per hour
    
    Returns:
        Current BAC as a percentage
    """
    if current_time is None:
        current_time = datetime.now()
    
    total_bac = 0.0
    widmark_factor = get_widmark_factor(gender)
    weight_grams = weight_kg * 1000
    
    for drink in drinks:
        # Calculate hours since this drink was consumed
        if drink.consumed_at is None:
            hours = 0.0  # Just consumed
        else:
            hours = (current_time - drink.consumed_at).total_seconds() / 3600
        
        if hours < 0:
            continue  # Drink not yet consumed
        
        # Calculate BAC from this drink
        drink_bac = (drink.alcohol_grams / (weight_grams * widmark_factor)) * 100
        
        # Apply metabolism
        drink_bac = max(0, drink_bac - metabolism_rate * hours)
        
        total_bac += drink_bac
    
    return total_bac


def get_impairment_level(bac: float) -> Tuple[ImpairmentLevel, str]:
    """
    Get impairment level and description based on BAC.
    
    Args:
        bac: Blood Alcohol Content as percentage
    
    Returns:
        Tuple of (ImpairmentLevel, description string)
    """
    descriptions = {
        ImpairmentLevel.SOBER: (
            "Sober state. No significant impairment. "
            "Normal behavior, judgment, and coordination."
        ),
        ImpairmentLevel.MILD: (
            "Mild impairment. Relaxation and slight euphoria. "
            "Talkativeness increases. May feel 'buzzed'."
        ),
        ImpairmentLevel.MODERATE: (
            "Moderate impairment. Reduced inhibition and judgment. "
            "Coordination begins to decline. Reaction time increases. "
            "LEGAL DRIVING LIMIT in many countries."
        ),
        ImpairmentLevel.SIGNIFICANT: (
            "Significant impairment. Slurred speech, impaired balance. "
            "Memory and judgment affected. Dangerous to drive. "
            "Risk of aggressive behavior."
        ),
        ImpairmentLevel.SEVERE: (
            "Severe impairment. Motor control severely affected. "
            "Confusion, dizziness, nausea likely. "
            "Memory blackouts possible. NEEDS MEDICAL ATTENTION."
        ),
        ImpairmentLevel.DANGEROUS: (
            "DANGEROUS level. Severe motor impairment. "
            "Vomiting, loss of consciousness possible. "
            "Breathing may be affected. SEEK MEDICAL HELP."
        ),
        ImpairmentLevel.LIFE_THREATENING: (
            "LIFE-THREATENING. Risk of coma or death. "
            "Severe respiratory depression. "
            "CALL EMERGENCY SERVICES IMMEDIATELY."
        ),
    }
    
    if bac < 0.02:
        level = ImpairmentLevel.SOBER
    elif bac < 0.05:
        level = ImpairmentLevel.MILD
    elif bac < 0.10:
        level = ImpairmentLevel.MODERATE
    elif bac < 0.15:
        level = ImpairmentLevel.SIGNIFICANT
    elif bac < 0.20:
        level = ImpairmentLevel.SEVERE
    elif bac < 0.30:
        level = ImpairmentLevel.DANGEROUS
    else:
        level = ImpairmentLevel.LIFE_THREATENING
    
    return level, descriptions[level]


def time_to_sober(bac: float, metabolism_rate: float = METABOLISM_RATE_AVG) -> float:
    """
    Calculate hours until BAC reaches 0.00%.
    
    Args:
        bac: Current Blood Alcohol Content
        metabolism_rate: BAC reduction per hour
    
    Returns:
        Hours until sober (BAC = 0.00%)
    """
    if bac <= 0:
        return 0.0
    return bac / metabolism_rate


def time_to_legal_limit(
    bac: float,
    country_code: str = "US",
    metabolism_rate: float = METABOLISM_RATE_AVG
) -> float:
    """
    Calculate hours until BAC is at or below legal driving limit.
    
    Args:
        bac: Current Blood Alcohol Content
        country_code: ISO country code (e.g., "US", "CN", "UK")
        metabolism_rate: BAC reduction per hour
    
    Returns:
        Hours until legal to drive (0 if already legal)
    """
    limit = LEGAL_LIMITS.get(country_code.upper(), 0.08)
    
    if bac <= limit:
        return 0.0
    
    return (bac - limit) / metabolism_rate


def calculate_bac_result(
    weight_kg: float,
    gender: Gender,
    alcohol_grams: float,
    hours_since_first_drink: float,
    country_code: str = "US",
    metabolism_rate: float = METABOLISM_RATE_AVG
) -> BACResult:
    """
    Calculate comprehensive BAC result with all information.
    
    Args:
        weight_kg: Body weight in kilograms
        gender: Male or Female
        alcohol_grams: Total alcohol consumed in grams
        hours_since_first_drink: Time since first drink
        country_code: Country code for legal limit
        metabolism_rate: BAC reduction per hour
    
    Returns:
        BACResult with all calculated values
    """
    bac = calculate_bac(weight_kg, gender, alcohol_grams, hours_since_first_drink, metabolism_rate)
    impairment, description = get_impairment_level(bac)
    legal_limit = LEGAL_LIMITS.get(country_code.upper(), 0.08)
    
    # Determine confidence based on input quality
    confidence = "Medium"  # Default
    if metabolism_rate == METABOLISM_RATE_AVG:
        confidence = "Medium (using average metabolism rate)"
    elif metabolism_rate < METABOLISM_RATE_AVG:
        confidence = "Low (slow metabolism assumed)"
    else:
        confidence = "Medium-High (fast metabolism assumed)"
    
    return BACResult(
        bac=round(bac, 4),
        impairment=impairment,
        description=description,
        time_to_sober=round(time_to_sober(bac, metabolism_rate), 2),
        time_to_drive=round(time_to_legal_limit(bac, country_code, metabolism_rate), 2),
        is_legal_to_drive=bac <= legal_limit,
        confidence=confidence
    )


def estimate_alcohol_content(
    volume_ml: float,
    abv: float
) -> float:
    """
    Calculate alcohol content in grams from volume and ABV.
    
    Args:
        volume_ml: Volume in milliliters
        abv: Alcohol by volume percentage (e.g., 5.0 for 5%)
    
    Returns:
        Alcohol content in grams
    """
    # Density of ethanol = 0.789 g/ml
    return volume_ml * (abv / 100) * 0.789


def get_legal_limit(country_code: str) -> float:
    """
    Get legal driving BAC limit for a country.
    
    Args:
        country_code: ISO country code
    
    Returns:
        Legal BAC limit as percentage
    """
    return LEGAL_LIMITS.get(country_code.upper(), 0.08)


def list_zero_tolerance_countries() -> List[str]:
    """List countries with zero tolerance for drunk driving."""
    return [code for code, limit in LEGAL_LIMITS.items() if limit == 0.00]


def format_bac(bac: float) -> str:
    """Format BAC as a human-readable string."""
    return f"{bac:.3f}%"


def format_time_hours(hours: float) -> str:
    """Format hours as a human-readable time string."""
    if hours <= 0:
        return "Now"
    
    h = int(hours)
    m = int((hours - h) * 60)
    
    if h == 0:
        return f"{m} minutes"
    elif h == 1:
        return f"1 hour" + (f" {m} min" if m > 0 else "")
    else:
        return f"{h} hours" + (f" {m} min" if m > 0 else "")


def calculate_drinks_by_bac(
    target_bac: float,
    weight_kg: float,
    gender: Gender,
    hours: float = 0.0,
    metabolism_rate: float = METABOLISM_RATE_AVG
) -> float:
    """
    Calculate how many standard drinks needed to reach a target BAC.
    
    WARNING: This is for educational purposes only. Never use to 
    determine if you can drive safely.
    
    Args:
        target_bac: Target BAC percentage
        weight_kg: Body weight in kilograms
        gender: Male or Female
        hours: Time over which drinks are consumed
        metabolism_rate: BAC reduction per hour
    
    Returns:
        Number of standard drinks (10g alcohol each)
    """
    widmark_factor = get_widmark_factor(gender)
    weight_grams = weight_kg * 1000
    
    # Calculate alcohol needed (reverse Widmark formula)
    # BAC = (Alcohol / (Weight × r)) × 100 - (Metabolism × Hours)
    # Alcohol = ((BAC + Metabolism × Hours) / 100) × Weight × r
    adjusted_bac = target_bac + metabolism_rate * hours
    alcohol_grams = (adjusted_bac / 100) * weight_grams * widmark_factor
    
    # Convert to standard drinks (10g each)
    return alcohol_grams / 10.0


def get_bac_warning(bac: float) -> List[str]:
    """
    Get warning messages for a given BAC level.
    
    Args:
        bac: Blood Alcohol Content
    
    Returns:
        List of warning messages
    """
    warnings = []
    
    if bac >= 0.30:
        warnings.append("⚠️ LIFE-THREATENING: Risk of coma or death. Seek emergency help immediately!")
    if bac >= 0.20:
        warnings.append("⚠️ SEVERE: Dangerous level. Do not attempt to drive or operate machinery.")
    if bac >= 0.15:
        warnings.append("⚠️ HIGH IMPAIRMENT: Risk of blackout. Do not make important decisions.")
    if bac >= 0.08:
        warnings.append("⚠️ ILLEGAL TO DRIVE: You are above the legal limit in most countries.")
    if bac >= 0.05:
        warnings.append("⚠️ IMPAIRED: Reaction time and judgment affected. Avoid driving.")
    if bac >= 0.03:
        warnings.append("ℹ️ NOTE: Some countries have lower legal limits. Check local laws.")
    
    return warnings


# Convenience functions for common scenarios

def beer_bac(
    weight_kg: float,
    gender: Gender,
    beer_count: int,
    hours: float,
    volume_ml: float = 330,
    abv: float = 5.0
) -> float:
    """Calculate BAC from beer consumption."""
    alcohol_grams = beer_count * estimate_alcohol_content(volume_ml, abv)
    return calculate_bac(weight_kg, gender, alcohol_grams, hours)


def wine_bac(
    weight_kg: float,
    gender: Gender,
    glass_count: int,
    hours: float,
    volume_ml: float = 150,
    abv: float = 12.0
) -> float:
    """Calculate BAC from wine consumption."""
    alcohol_grams = glass_count * estimate_alcohol_content(volume_ml, abv)
    return calculate_bac(weight_kg, gender, alcohol_grams, hours)


def spirit_bac(
    weight_kg: float,
    gender: Gender,
    shot_count: int,
    hours: float,
    volume_ml: float = 45,
    abv: float = 40.0
) -> float:
    """Calculate BAC from spirit consumption."""
    alcohol_grams = shot_count * estimate_alcohol_content(volume_ml, abv)
    return calculate_bac(weight_kg, gender, alcohol_grams, hours)


if __name__ == "__main__":
    # Demo usage
    print("=" * 60)
    print("Blood Alcohol Content (BAC) Calculator Demo")
    print("=" * 60)
    
    # Example 1: Simple calculation
    print("\n📊 Example 1: 70kg male, 3 beers over 2 hours")
    bac = beer_bac(70, Gender.MALE, 3, 2)
    print(f"   BAC: {format_bac(bac)}")
    
    # Example 2: Full result
    print("\n📊 Example 2: 55kg female, 2 glasses of wine over 1.5 hours")
    alcohol = 2 * estimate_alcohol_content(150, 12.0)  # 2 glasses of wine
    result = calculate_bac_result(55, Gender.FEMALE, alcohol, 1.5, "CN")
    print(f"   BAC: {format_bac(result.bac)}")
    print(f"   Impairment: {result.impairment.value}")
    print(f"   Time to sober: {format_time_hours(result.time_to_sober)}")
    print(f"   Can legally drive (China): {'Yes' if result.is_legal_to_drive else 'No'}")
    
    # Example 3: Using Drink objects
    print("\n📊 Example 3: Mixed drinks with timestamps")
    now = datetime.now()
    drinks = [
        Drink.from_beer(500, 5.0, "Large Beer", now - timedelta(hours=3)),
        Drink.from_wine(150, 12.0, "Red Wine", now - timedelta(hours=1.5)),
        Drink.from_spirit(45, 40.0, "Whiskey", now - timedelta(minutes=30)),
    ]
    bac = calculate_bac_from_drinks(80, Gender.MALE, drinks, now)
    print(f"   Current BAC: {format_bac(bac)}")
    
    print("\n" + "=" * 60)