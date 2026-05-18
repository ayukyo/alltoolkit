"""
Nautical Utilities - A collection of nautical and maritime conversion tools.

Features:
- Speed conversions (knots, mph, kph, m/s)
- Distance conversions (nautical miles, statute miles, kilometers)
- Beaufort scale wind classification
- Compass direction utilities (degrees to cardinal/intercardinal)
- Maritime flag alphabet (International Code of Signals)
- Latitude/Longitude formatting and parsing
- Depth unit conversions (fathoms, feet, meters)
- Maritime time zone handling

Zero external dependencies - uses only Python standard library.
"""

from typing import Tuple, Optional, Dict, List
from dataclasses import dataclass
from enum import Enum


# =============================================================================
# CONSTANTS
# =============================================================================

# Conversion factors
KNOTS_TO_MPH = 1.15078
KNOTS_TO_KPH = 1.852
KNOTS_TO_MS = 0.514444  # meters per second

NAUTICAL_MILE_TO_MILES = 1.15078
NAUTICAL_MILE_TO_KM = 1.852

FATHOM_TO_FEET = 6
FATHOM_TO_METERS = 1.8288

# Earth measurements
EARTH_RADIUS_NM = 3440.065  # nautical miles
EARTH_RADIUS_KM = 6371.0


class BeaufortScale(Enum):
    """Beaufort Wind Scale classification."""
    CALM = 0
    LIGHT_AIR = 1
    LIGHT_BREEZE = 2
    GENTLE_BREEZE = 3
    MODERATE_BREEZE = 4
    FRESH_BREEZE = 5
    STRONG_BREEZE = 6
    NEAR_GALE = 7
    GALE = 8
    STRONG_GALE = 9
    STORM = 10
    VIOLENT_STORM = 11
    HURRICANE = 12


# Beaufort scale data: (min_knots, max_knots_exclusive, description, sea_conditions)
# max_knots is exclusive (min_k <= knots < max_k)
BEAUFORT_DATA: Dict[int, Tuple[float, float, str, str]] = {
    0: (0, 1, "Calm", "Sea like a mirror"),
    1: (1, 4, "Light Air", "Ripples with appearance of scales; no foam crests"),
    2: (4, 7, "Light Breeze", "Small wavelets; crests of glassy appearance, not breaking"),
    3: (7, 11, "Gentle Breeze", "Large wavelets; crests begin to break, scattered whitecaps"),
    4: (11, 17, "Moderate Breeze", "Small waves, becoming longer; numerous whitecaps"),
    5: (17, 22, "Fresh Breeze", "Moderate waves, taking longer form; many whitecaps; some spray"),
    6: (22, 28, "Strong Breeze", "Large waves forming; whitecaps everywhere; more spray"),
    7: (28, 34, "Near Gale", "Sea heaps up; white foam from breaking waves begins to be blown in streaks"),
    8: (34, 41, "Gale", "Moderately high waves of greater length; edges of crests break into spindrift"),
    9: (41, 48, "Strong Gale", "High waves; sea begins to roll; spray may affect visibility"),
    10: (48, 56, "Storm", "Very high waves with overhanging crests; sea surface white"),
    11: (56, 64, "Violent Storm", "Exceptionally high waves; sea covered with white foam"),
    12: (64, float('inf'), "Hurricane", "Air filled with foam; sea white with driving spray")
}

# Maritime flag alphabet (International Code of Signals)
MARITIME_FLAGS: Dict[str, str] = {
    'A': "Alpha - Diver below; keep clear",
    'B': "Bravo - Carrying dangerous cargo",
    'C': "Charlie - Yes (affirmative)",
    'D': "Delta - Keep clear; maneuvering with difficulty",
    'E': "Echo - Altering course to starboard",
    'F': "Foxtrot - Disabled; communicate with me",
    'G': "Golf - Require a pilot",
    'H': "Hotel - Pilot on board",
    'I': "India - Altering course to port",
    'J': "Juliet - On fire; keep clear",
    'K': "Kilo - Wish to communicate",
    'L': "Lima - Stop instantly",
    'M': "Mike - Vessel stopped; no way",
    'N': "November - No (negative)",
    'O': "Oscar - Man overboard",
    'P': "Papa - About to sail; all aboard",
    'Q': "Quebec - Request pratique (health clearance)",
    'R': "Romeo - No single-letter meaning assigned",
    'S': "Sierra - Engines going astern",
    'T': "Tango - Keep clear; engaged in trawling",
    'U': "Uniform - Standing into danger",
    'V': "Victor - Require assistance",
    'W': "Whiskey - Require medical assistance",
    'X': "X-ray - Stop your intention; watch me",
    'Y': "Yankee - Dragging anchor",
    'Z': "Zulu - Require a tug"
}

# Cardinal and intercardinal directions
COMPASS_POINTS: Dict[str, Tuple[float, float]] = {
    'N': (348.75, 11.25),
    'NNE': (11.25, 33.75),
    'NE': (33.75, 56.25),
    'ENE': (56.25, 78.75),
    'E': (78.75, 101.25),
    'ESE': (101.25, 123.75),
    'SE': (123.75, 146.25),
    'SSE': (146.25, 168.75),
    'S': (168.75, 191.25),
    'SSW': (191.25, 213.75),
    'SW': (213.75, 236.25),
    'WSW': (236.25, 258.75),
    'W': (258.75, 281.25),
    'WNW': (281.25, 303.75),
    'NW': (303.75, 326.25),
    'NNW': (326.25, 348.75)
}


# =============================================================================
# SPEED CONVERSIONS
# =============================================================================

def knots_to_mph(knots: float) -> float:
    """Convert knots to miles per hour."""
    return knots * KNOTS_TO_MPH


def knots_to_kph(knots: float) -> float:
    """Convert knots to kilometers per hour."""
    return knots * KNOTS_TO_KPH


def knots_to_ms(knots: float) -> float:
    """Convert knots to meters per second."""
    return knots * KNOTS_TO_MS


def mph_to_knots(mph: float) -> float:
    """Convert miles per hour to knots."""
    return mph / KNOTS_TO_MPH


def kph_to_knots(kph: float) -> float:
    """Convert kilometers per hour to knots."""
    return kph / KNOTS_TO_KPH


def ms_to_knots(ms: float) -> float:
    """Convert meters per second to knots."""
    return ms / KNOTS_TO_MS


def convert_speed(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert between speed units.
    
    Args:
        value: The speed value to convert
        from_unit: Source unit ('knots', 'mph', 'kph', 'm/s', 'ms')
        to_unit: Target unit ('knots', 'mph', 'kph', 'm/s', 'ms')
    
    Returns:
        Converted speed value
    
    Example:
        >>> convert_speed(10, 'knots', 'mph')
        11.5078
    """
    from_unit = from_unit.lower().replace('/', '')
    to_unit = to_unit.lower().replace('/', '')
    
    # Convert to knots first
    if from_unit == 'knots':
        knots = value
    elif from_unit == 'mph':
        knots = mph_to_knots(value)
    elif from_unit == 'kph':
        knots = kph_to_knots(value)
    elif from_unit in ('ms', 'm/s'):
        knots = ms_to_knots(value)
    else:
        raise ValueError(f"Unknown unit: {from_unit}")
    
    # Convert from knots to target unit
    if to_unit == 'knots':
        return knots
    elif to_unit == 'mph':
        return knots_to_mph(knots)
    elif to_unit == 'kph':
        return knots_to_kph(knots)
    elif to_unit in ('ms', 'm/s'):
        return knots_to_ms(knots)
    else:
        raise ValueError(f"Unknown unit: {to_unit}")


# =============================================================================
# DISTANCE CONVERSIONS
# =============================================================================

def nautical_miles_to_miles(nm: float) -> float:
    """Convert nautical miles to statute miles."""
    return nm * NAUTICAL_MILE_TO_MILES


def nautical_miles_to_km(nm: float) -> float:
    """Convert nautical miles to kilometers."""
    return nm * NAUTICAL_MILE_TO_KM


def miles_to_nautical_miles(miles: float) -> float:
    """Convert statute miles to nautical miles."""
    return miles / NAUTICAL_MILE_TO_MILES


def km_to_nautical_miles(km: float) -> float:
    """Convert kilometers to nautical miles."""
    return km / NAUTICAL_MILE_TO_KM


def convert_distance(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert between distance units.
    
    Args:
        value: The distance value to convert
        from_unit: Source unit ('nm', 'nautical_miles', 'miles', 'km', 'kilometers')
        to_unit: Target unit ('nm', 'nautical_miles', 'miles', 'km', 'kilometers')
    
    Returns:
        Converted distance value
    
    Example:
        >>> convert_distance(100, 'nm', 'km')
        185.2
    """
    from_unit = from_unit.lower().replace('_', '')
    to_unit = to_unit.lower().replace('_', '')
    
    # Normalize unit names
    if from_unit in ('nm', 'nauticalmiles'):
        from_unit = 'nm'
    if to_unit in ('nm', 'nauticalmiles'):
        to_unit = 'nm'
    if from_unit in ('kilometers', 'kilometer'):
        from_unit = 'km'
    if to_unit in ('kilometers', 'kilometer'):
        to_unit = 'km'
    
    # Convert to nautical miles first
    if from_unit == 'nm':
        nm = value
    elif from_unit == 'miles':
        nm = miles_to_nautical_miles(value)
    elif from_unit == 'km':
        nm = km_to_nautical_miles(value)
    else:
        raise ValueError(f"Unknown unit: {from_unit}")
    
    # Convert from nautical miles to target unit
    if to_unit == 'nm':
        return nm
    elif to_unit == 'miles':
        return nautical_miles_to_miles(nm)
    elif to_unit == 'km':
        return nautical_miles_to_km(nm)
    else:
        raise ValueError(f"Unknown unit: {to_unit}")


# =============================================================================
# DEPTH CONVERSIONS
# =============================================================================

def fathoms_to_feet(fathoms: float) -> float:
    """Convert fathoms to feet."""
    return fathoms * FATHOM_TO_FEET


def fathoms_to_meters(fathoms: float) -> float:
    """Convert fathoms to meters."""
    return fathoms * FATHOM_TO_METERS


def feet_to_fathoms(feet: float) -> float:
    """Convert feet to fathoms."""
    return feet / FATHOM_TO_FEET


def meters_to_fathoms(meters: float) -> float:
    """Convert meters to fathoms."""
    return meters / FATHOM_TO_METERS


# =============================================================================
# BEAUFORT SCALE
# =============================================================================

def get_beaufort_scale(knots: float) -> Tuple[int, str, str]:
    """
    Get Beaufort scale number for given wind speed in knots.
    
    Args:
        knots: Wind speed in knots
    
    Returns:
        Tuple of (scale_number, description, sea_conditions)
    
    Example:
        >>> get_beaufort_scale(25)
        (6, 'Strong Breeze', 'Large waves forming; whitecaps everywhere; more spray')
    """
    for scale, (min_k, max_k, desc, sea) in BEAUFORT_DATA.items():
        if min_k <= knots < max_k:
            return (scale, desc, sea)
    return (12, "Hurricane", BEAUFORT_DATA[12][3])


def get_beaufort_range(scale: int) -> Tuple[float, float]:
    """
    Get the wind speed range for a Beaufort scale number.
    
    Args:
        scale: Beaufort scale number (0-12)
    
    Returns:
        Tuple of (min_knots, max_knots_inclusive)
        Note: max_knots is the highest value in this scale.
    
    Example:
        >>> get_beaufort_range(5)
        (17, 21)
        >>> get_beaufort_range(11)
        (56, 63)
    """
    if scale < 0 or scale > 12:
        raise ValueError("Beaufort scale must be between 0 and 12")
    min_k, max_k_exclusive, _, _ = BEAUFORT_DATA[scale]
    # Return the inclusive max (one less than the exclusive max)
    max_k_inclusive = max_k_exclusive - 1 if max_k_exclusive != float('inf') else float('inf')
    return (min_k, max_k_inclusive)


def describe_wind(knots: float) -> Dict[str, any]:
    """
    Get comprehensive wind information.
    
    Args:
        knots: Wind speed in knots
    
    Returns:
        Dictionary with wind details including speeds in various units,
        Beaufort scale, and description
    
    Example:
        >>> describe_wind(25)
        {
            'knots': 25,
            'mph': 28.77,
            'kph': 46.3,
            'm/s': 12.86,
            'beaufort': 6,
            'description': 'Strong Breeze',
            'sea_conditions': 'Large waves forming...'
        }
    """
    scale, desc, sea = get_beaufort_scale(knots)
    return {
        'knots': knots,
        'mph': round(knots_to_mph(knots), 2),
        'kph': round(knots_to_kph(knots), 2),
        'm/s': round(knots_to_ms(knots), 2),
        'beaufort': scale,
        'description': desc,
        'sea_conditions': sea
    }


# =============================================================================
# COMPASS DIRECTIONS
# =============================================================================

def degrees_to_cardinal(degrees: float) -> str:
    """
    Convert compass degrees to cardinal direction.
    
    Args:
        degrees: Compass heading in degrees (0-360)
    
    Returns:
        Cardinal direction abbreviation (N, NNE, NE, ENE, E, etc.)
    
    Example:
        >>> degrees_to_cardinal(45)
        'NE'
        >>> degrees_to_cardinal(0)
        'N'
    """
    degrees = degrees % 360
    
    # Special case for North
    if degrees >= 348.75 or degrees < 11.25:
        return 'N'
    
    for direction, (start, end) in COMPASS_POINTS.items():
        if direction != 'N':  # Already handled
            if start <= degrees < end:
                return direction
    
    return 'N'  # Default fallback


def degrees_to_full_name(degrees: float) -> str:
    """
    Convert compass degrees to full cardinal direction name.
    
    Args:
        degrees: Compass heading in degrees (0-360)
    
    Returns:
        Full cardinal direction name
    
    Example:
        >>> degrees_to_full_name(45)
        'Northeast'
    """
    names = {
        'N': 'North',
        'NNE': 'North-Northeast',
        'NE': 'Northeast',
        'ENE': 'East-Northeast',
        'E': 'East',
        'ESE': 'East-Southeast',
        'SE': 'Southeast',
        'SSE': 'South-Southeast',
        'S': 'South',
        'SSW': 'South-Southwest',
        'SW': 'Southwest',
        'WSW': 'West-Southwest',
        'W': 'West',
        'WNW': 'West-Northwest',
        'NW': 'Northwest',
        'NNW': 'North-Northwest'
    }
    return names.get(degrees_to_cardinal(degrees), 'North')


def cardinal_to_degrees(cardinal: str) -> float:
    """
    Convert cardinal direction to degrees.
    
    Args:
        cardinal: Cardinal direction (N, NNE, NE, ENE, E, etc.)
    
    Returns:
        Compass heading in degrees
    
    Example:
        >>> cardinal_to_degrees('NE')
        45.0
        >>> cardinal_to_degrees('S')
        180.0
    """
    cardinal = cardinal.upper()
    degrees_map = {
        'N': 0.0, 'NNE': 22.5, 'NE': 45.0, 'ENE': 67.5,
        'E': 90.0, 'ESE': 112.5, 'SE': 135.0, 'SSE': 157.5,
        'S': 180.0, 'SSW': 202.5, 'SW': 225.0, 'WSW': 247.5,
        'W': 270.0, 'WNW': 292.5, 'NW': 315.0, 'NNW': 337.5
    }
    if cardinal not in degrees_map:
        raise ValueError(f"Unknown cardinal direction: {cardinal}")
    return degrees_map[cardinal]


def normalize_heading(degrees: float) -> float:
    """
    Normalize a heading to 0-360 degrees.
    
    Args:
        degrees: Any angle in degrees
    
    Returns:
        Normalized heading (0-360)
    
    Example:
        >>> normalize_heading(450)
        90.0
        >>> normalize_heading(-90)
        270.0
    """
    return degrees % 360


def heading_difference(heading1: float, heading2: float) -> float:
    """
    Calculate the shortest angle between two headings.
    
    Args:
        heading1: First heading in degrees
        heading2: Second heading in degrees
    
    Returns:
        Shortest angle between headings (0-180)
    
    Example:
        >>> heading_difference(10, 350)
        20.0
    """
    diff = abs(normalize_heading(heading1) - normalize_heading(heading2))
    return min(diff, 360 - diff)


# =============================================================================
# LATITUDE/LONGITUDE
# =============================================================================

@dataclass
class Coordinate:
    """Represents a latitude or longitude coordinate."""
    degrees: int
    minutes: float
    seconds: float = 0.0
    direction: str = 'N'  # N, S, E, W
    
    def to_decimal(self) -> float:
        """Convert to decimal degrees."""
        decimal = self.degrees + self.minutes / 60 + self.seconds / 3600
        if self.direction in ('S', 'W'):
            decimal = -decimal
        return decimal
    
    @classmethod
    def from_decimal(cls, decimal: float, is_latitude: bool = True) -> 'Coordinate':
        """Create from decimal degrees."""
        direction = 'N' if decimal >= 0 else 'S' if is_latitude else 'E' if decimal >= 0 else 'W'
        decimal = abs(decimal)
        degrees = int(decimal)
        minutes_float = (decimal - degrees) * 60
        minutes = int(minutes_float)
        seconds = (minutes_float - minutes) * 60
        return cls(degrees=degrees, minutes=minutes, seconds=seconds, direction=direction)
    
    def to_dms_string(self) -> str:
        """Convert to degrees-minutes-seconds string."""
        return f"{self.degrees}°{self.minutes:.0f}'{self.seconds:.1f}\"{self.direction}"
    
    def to_dm_string(self) -> str:
        """Convert to degrees-minutes string (common marine format)."""
        return f"{self.degrees}°{self.minutes:.3f}'{self.direction}"


def parse_coordinate(coord_string: str) -> Tuple[float, Optional[str]]:
    """
    Parse a coordinate string to decimal degrees.
    
    Supports formats:
    - Decimal degrees: "45.5", "-122.3"
    - Degrees minutes: "45°30.5'N", "122 18.5 W"
    - Degrees minutes seconds: "45°30'30\"N", "122 18 30 W"
    
    Args:
        coord_string: Coordinate string
    
    Returns:
        Tuple of (decimal_degrees, direction_letter or None)
    
    Example:
        >>> parse_coordinate("45°30'N")
        (45.5, 'N')
    """
    import re
    
    coord_string = coord_string.strip().upper()
    
    # Check for direction
    direction = None
    for d in ['N', 'S', 'E', 'W']:
        if d in coord_string:
            direction = d
            coord_string = coord_string.replace(d, '').strip()
            break
    
    # Replace degree/minute/second symbols with spaces
    coord_string = re.sub(r'[°\'"]', ' ', coord_string)
    parts = coord_string.split()
    
    if len(parts) == 1:
        # Decimal degrees
        decimal = float(parts[0])
    elif len(parts) == 2:
        # Degrees and minutes
        decimal = float(parts[0]) + float(parts[1]) / 60
    elif len(parts) >= 3:
        # Degrees, minutes, and seconds
        decimal = float(parts[0]) + float(parts[1]) / 60 + float(parts[2]) / 3600
    else:
        raise ValueError(f"Invalid coordinate format: {coord_string}")
    
    if direction in ('S', 'W'):
        decimal = -decimal
    
    return decimal, direction


def format_latitude(decimal: float, format: str = 'dms') -> str:
    """
    Format a latitude value.
    
    Args:
        decimal: Latitude in decimal degrees
        format: Output format ('dms', 'dm', 'decimal')
    
    Returns:
        Formatted latitude string
    
    Example:
        >>> format_latitude(45.5084)
        "45°30'30.2\"N"
    """
    coord = Coordinate.from_decimal(decimal, is_latitude=True)
    if format == 'dms':
        return coord.to_dms_string()
    elif format == 'dm':
        return coord.to_dm_string()
    else:
        return f"{decimal:.6f}°"


def format_longitude(decimal: float, format: str = 'dms') -> str:
    """
    Format a longitude value.
    
    Args:
        decimal: Longitude in decimal degrees
        format: Output format ('dms', 'dm', 'decimal')
    
    Returns:
        Formatted longitude string
    
    Example:
        >>> format_longitude(-122.3)
        "122°18'0.0\"W"
    """
    coord = Coordinate.from_decimal(decimal, is_latitude=False)
    if format == 'dms':
        return coord.to_dms_string()
    elif format == 'dm':
        return coord.to_dm_string()
    else:
        return f"{decimal:.6f}°"


# =============================================================================
# MARITIME FLAGS
# =============================================================================

def get_maritime_flag_meaning(letter: str) -> str:
    """
    Get the meaning of a maritime flag signal.
    
    Args:
        letter: Single letter (A-Z)
    
    Returns:
        Meaning of the flag signal
    
    Example:
        >>> get_maritime_flag_meaning('A')
        'Alpha - Diver below; keep clear'
    """
    letter = letter.upper()
    if letter not in MARITIME_FLAGS:
        raise ValueError(f"Unknown flag: {letter}")
    return MARITIME_FLAGS[letter]


def encode_maritime_message(message: str) -> List[Dict[str, str]]:
    """
    Encode a message using maritime flag alphabet.
    
    Args:
        message: Message to encode (letters A-Z)
    
    Returns:
        List of dictionaries with letter and meaning
    
    Example:
        >>> encode_maritime_message("SOS")
        [{'letter': 'S', 'meaning': '...'}, {'letter': 'O', 'meaning': '...'}, ...]
    """
    result = []
    for char in message.upper():
        if char in MARITIME_FLAGS:
            result.append({
                'letter': char,
                'meaning': MARITIME_FLAGS[char]
            })
    return result


def get_distress_signals() -> Dict[str, str]:
    """
    Get common maritime distress signals.
    
    Returns:
        Dictionary of distress signal names and descriptions
    """
    return {
        'MAYDAY': "Voice distress signal - grave and imminent danger",
        'PAN-PAN': "Voice urgency signal - urgency message",
        'SECURITE': "Voice safety signal - safety message",
        'SOS': "Morse code distress signal (... --- ...)",
        'NC': "International Code: distress flag combination",
        'RED_ENSIGN_UPSIDE_DOWN': "Distress signal (inverted flag)",
        'ORANGE_SMOKE': "Visual distress signal",
        'RED_FLARE': "Visual distress signal",
        'SLOW_REPEATED_RADIO': "Alarm signal (on radio)"
    }


# =============================================================================
# NAVIGATION UTILITIES
# =============================================================================

def calculate_distance_nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points in nautical miles.
    
    Uses the Haversine formula.
    
    Args:
        lat1: Latitude of first point (decimal degrees)
        lon1: Longitude of first point (decimal degrees)
        lat2: Latitude of second point (decimal degrees)
        lon2: Longitude of second point (decimal degrees)
    
    Returns:
        Distance in nautical miles
    
    Example:
        >>> calculate_distance_nm(37.7749, -122.4194, 34.0522, -118.2437)  # SF to LA
        298.5  # approximately
    """
    import math
    
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon1_rad = math.radians(lon1)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Distance in nautical miles
    distance = EARTH_RADIUS_NM * c
    return round(distance, 2)


def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the initial bearing from point 1 to point 2.
    
    Args:
        lat1: Latitude of first point (decimal degrees)
        lon1: Longitude of first point (decimal degrees)
        lat2: Latitude of second point (decimal degrees)
        lon2: Longitude of second point (decimal degrees)
    
    Returns:
        Initial bearing in degrees (0-360)
    
    Example:
        >>> calculate_bearing(37.7749, -122.4194, 34.0522, -118.2437)
        137.5  # approximately (SE direction)
    """
    import math
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlon = math.radians(lon2 - lon1)
    
    x = math.sin(dlon) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon)
    
    bearing = math.degrees(math.atan2(x, y))
    return normalize_heading(bearing)


def time_to_destination(distance_nm: float, speed_knots: float) -> float:
    """
    Calculate time to destination.
    
    Args:
        distance_nm: Distance in nautical miles
        speed_knots: Speed in knots
    
    Returns:
        Time in hours
    
    Example:
        >>> time_to_destination(100, 20)
        5.0
    """
    if speed_knots <= 0:
        raise ValueError("Speed must be greater than 0")
    return distance_nm / speed_knots


def fuel_consumption(distance_nm: float, consumption_rate: float, speed_knots: float) -> float:
    """
    Calculate fuel consumption for a voyage.
    
    Args:
        distance_nm: Distance in nautical miles
        consumption_rate: Fuel consumption rate (liters per hour)
        speed_knots: Speed in knots
    
    Returns:
        Total fuel consumption in liters
    
    Example:
        >>> fuel_consumption(100, 10, 20)  # 100nm at 20 knots, 10 L/h
        50.0
    """
    hours = time_to_destination(distance_nm, speed_knots)
    return hours * consumption_rate


# =============================================================================
# SUMMARY
# =============================================================================

def get_nautical_summary() -> Dict[str, any]:
    """
    Get a summary of nautical utilities and their capabilities.
    
    Returns:
        Dictionary with module information
    """
    return {
        'module': 'nautical_utils',
        'version': '1.0.0',
        'description': 'Nautical and maritime conversion tools',
        'features': [
            'Speed conversions (knots, mph, kph, m/s)',
            'Distance conversions (nautical miles, miles, km)',
            'Depth conversions (fathoms, feet, meters)',
            'Beaufort wind scale classification',
            'Compass direction utilities',
            'Latitude/Longitude formatting',
            'Maritime flag alphabet',
            'Navigation calculations'
        ],
        'constants': {
            'knots_to_mph': KNOTS_TO_MPH,
            'knots_to_kph': KNOTS_TO_KPH,
            'nautical_mile_to_km': NAUTICAL_MILE_TO_KM,
            'fathom_to_feet': FATHOM_TO_FEET
        }
    }


if __name__ == "__main__":
    # Quick demo
    print("=== Nautical Utilities Demo ===\n")
    
    # Speed conversions
    print(f"10 knots = {knots_to_mph(10):.2f} mph")
    print(f"10 knots = {knots_to_kph(10):.2f} kph")
    print()
    
    # Beaufort scale
    wind = describe_wind(25)
    print(f"Wind at 25 knots: Beaufort {wind['beaufort']} ({wind['description']})")
    print()
    
    # Compass
    print(f"45 degrees = {degrees_to_cardinal(45)} ({degrees_to_full_name(45)})")
    print()
    
    # Maritime flags
    print(f"Flag 'A' means: {get_maritime_flag_meaning('A')}")
    print()
    
    # Navigation
    print(f"Distance from SF to LA: ~{calculate_distance_nm(37.7749, -122.4194, 34.0522, -118.2437)} nm")
    print(f"Time to travel 100nm at 20 knots: {time_to_destination(100, 20)} hours")