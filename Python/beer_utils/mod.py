#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Beer Brewing Utilities Module
==========================================
Comprehensive beer brewing calculation utilities.
Zero external dependencies - pure Python implementation.

Features:
    - ABV (Alcohol by Volume) calculations
    - IBU (International Bitterness Units) calculation
    - SRM (Standard Reference Method) color calculation
    - OG/FG (Original/Final Gravity) and attenuation
    - Plato to Specific Gravity conversion
    - Grain bill calculations
    - Hop utilization tables
    - Carbonation (volumes and grams/liter)
    - Boil-off rate adjustments
    - Recipe scaling

Author: AllToolkit Contributors
License: MIT
"""

from typing import Optional, Dict, List, Tuple


# ============================================================================
# Constants
# ============================================================================

# Standard gravity values
WATER_SG = 1.000

# Base acid content for acidity calculation
DEFAULT_MASH_PH = 5.4
DEFAULT_BOIL_PH = 5.2

# Carbonation levels (volumes CO2)
CARBONATION_STYLES = {
    "american_ale": 2.5,
    "british_ale": 1.7,
    "belgian_strong": 2.8,
    "wheat_beer": 3.5,
    "lager": 2.5,
    "stout": 2.0,
    "pilsner": 2.4,
    "ipa": 2.4,
    "fruit_beer": 3.0,
    "gose": 3.5,
}

# SRM to RGB color approximation table
SRM_COLORS = {
    1: (255, 255, 255),
    2: (255, 255, 204),
    3: (255, 255, 153),
    4: (255, 255, 102),
    5: (255, 255, 51),
    6: (255, 230, 0),
    7: (255, 204, 0),
    8: (255, 179, 0),
    9: (255, 153, 0),
    10: (255, 128, 0),
    11: (255, 102, 0),
    12: (255, 77, 0),
    13: (255, 51, 0),
    14: (230, 0, 0),
    15: (204, 0, 0),
    16: (178, 0, 0),
    17: (153, 0, 0),
    18: (128, 0, 0),
    19: (102, 0, 0),
    20: (76, 0, 0),
    25: (51, 0, 0),
    30: (25, 0, 0),
    35: (13, 0, 0),
    40: (0, 0, 0),
}


# ============================================================================
# Gravity & ABV Functions
# ============================================================================

def calc_abv(og: float, fg: float, precision: int = 1) -> float:
    """
    Calculate Alcohol by Volume (ABV) from Original and Final Gravity.
    
    Args:
        og: Original Gravity (e.g., 1.050)
        fg: Final Gravity (e.g., 1.010)
        precision: Decimal places to round to
        
    Returns:
        ABV percentage
        
    Example:
        >>> calc_abv(1.050, 1.010)
        5.2
    """
    if og <= fg or og <= 1.0 or fg < 1.0:
        return 0.0
    abv = (og - fg) * 131.25
    return round(abv, precision)


def calc_abv_from_plato(oPlato: float, fPlato: float, precision: int = 1) -> float:
    """
    Calculate ABV using Plato units.
    
    Args:
        oPlato: Original Plato (e.g., 12.5)
        fPlato: Final Plato (e.g., 2.5)
        precision: Decimal places to round to
        
    Returns:
        ABV percentage
    """
    og = plato_to_sg(oPlato)
    fg = plato_to_sg(fPlato)
    return calc_abv(og, fg, precision)


def sg_to_plato(sg: float) -> float:
    """
    Convert Specific Gravity to Plato.
    
    Args:
        sg: Specific Gravity (e.g., 1.050)
        
    Returns:
        Plato degrees
        
    Example:
        >>> sg_to_plato(1.050)
        12.3
    """
    if sg <= 1.0:
        return 0.0
    plato = (-1 * 616.868) + (1111.14 * sg) - (630.272 * sg**2) + (135.997 * sg**3)
    return round(plato, 1)


def plato_to_sg(plato: float) -> float:
    """
    Convert Plato to Specific Gravity.
    
    Args:
        plato: Plato degrees (e.g., 12.0)
        
    Returns:
        Specific Gravity
        
    Example:
        >>> round(plato_to_sg(12.0), 3)
        1.048
    """
    if plato <= 0:
        return 1.0
    sg = 1 + (plato / (258.6 - (plato / 258.2) * 227.1))
    return round(sg, 3)


def calc_attenuation(og: float, fg: float, precision: int = 1) -> float:
    """
    Calculate Apparent Attenuation percentage.
    
    Args:
        og: Original Gravity
        fg: Final Gravity
        precision: Decimal places to round to
        
    Returns:
        Attenuation percentage
        
    Example:
        >>> calc_attenuation(1.050, 1.010)
        78.0
    """
    if og <= 1.0 or fg >= og:
        return 0.0
    atten = ((og - fg) / (og - 1.0)) * 100
    return round(atten, precision)


def calc_real_attenuation(og: float, fg: float, precision: int = 1) -> float:
    """
    Calculate Real (True) Attenuation using Plato.
    
    Args:
        og: Original Gravity
        fg: Final Gravity
        precision: Decimal places to round to
        
    Returns:
        Real attenuation percentage
    """
    oPlato = sg_to_plato(og)
    fPlato = sg_to_plato(fg)
    if oPlato <= 0:
        return 0.0
    atten = ((oPlato - fPlato) / oPlato) * 100
    return round(atten, precision)


def calc_fg_from_attenuation(og: float, attenuation: float) -> float:
    """
    Estimate Final Gravity from Original Gravity and target attenuation.
    
    Args:
        og: Original Gravity
        attenuation: Target attenuation percentage (e.g., 75.0)
        
    Returns:
        Estimated Final Gravity
        
    Example:
        >>> round(calc_fg_from_attenuation(1.050, 75.0), 3)
        1.013
    """
    if og <= 1.0 or attenuation < 0 or attenuation > 100:
        return og
    fg = og - ((og - 1.0) * (attenuation / 100))
    return round(fg, 3)


# ============================================================================
# Hop & IBU Functions
# ============================================================================

def calc_ibu(
    hop_alpha: float,
    hop_weight: float,
    boil_time: float,
    og: float,
    volume: float,
    method: str = "tinseth"
) -> float:
    """
    Calculate International Bitterness Units (IBU).
    
    Uses Tinseth formula by default. Also supports:
    - "rager": Rager formula
    - "garetz": Garetz formula
    
    Args:
        hop_alpha: Hop alpha acid percentage (e.g., 5.5 for 5.5%)
        hop_weight: Hop weight in grams
        boil_time: Boil time in minutes
        og: Original Gravity of wort
        volume: Final volume in liters
        method: Calculation method ("tinseth", "rager", "garetz")
        
    Returns:
        IBU value
        
    Example:
        >>> calc_ibu(5.5, 28, 60, 1.050, 20)
        32.4
    """
    if hop_alpha <= 0 or hop_weight <= 0 or boil_time <= 0 or volume <= 0:
        return 0.0
    
    if method == "tinseth":
        # Tinseth formula
        bigness_factor = 1.65 * 0.000125 ** (og - 1.0)
        boil_time_factor = (1 - 2.71828 ** (-0.04 * boil_time)) / 4.15
        ibus = bigness_factor * boil_time_factor * (hop_alpha / 100) * (hop_weight * 1000) / volume
        
    elif method == "rager":
        # Rager formula
        aa_use = hop_alpha * (hop_weight * 1000) / (volume * 100)
        utilization = 18.13 + 13.86 * (1 - 2.71828 ** (-0.05 * boil_time))
        if og > 1.050:
            gravity_adjust = og / 1.050
            utilization *= (1.0 / gravity_adjust)
        ibus = aa_use * utilization / 100
        
    else:
        # Default to Tinseth
        bigness_factor = 1.65 * 0.000125 ** (og - 1.0)
        boil_time_factor = (1 - 2.71828 ** (-0.04 * boil_time)) / 4.15
        ibus = bigness_factor * boil_time_factor * (hop_alpha / 100) * (hop_weight * 1000) / volume
    
    return round(ibus, 1)


def calc_hop_utilization(boil_time: float, og: float) -> float:
    """
    Calculate hop utilization percentage.
    
    Args:
        boil_time: Boil time in minutes
        og: Original Gravity
        
    Returns:
        Utilization percentage
    """
    bigness_factor = 1.65 * 0.000125 ** (og - 1.0)
    boil_time_factor = (1 - 2.71828 ** (-0.04 * boil_time)) / 4.15
    return round(bigness_factor * boil_time_factor * 100, 1)


def ibu_category(ibu: float) -> str:
    """
    Get beer style category based on IBU.
    
    Args:
        ibu: IBU value
        
    Returns:
        Bitterness category name
    """
    if ibu < 10:
        return "no perceived hop bitterness"
    elif ibu < 20:
        return "low hop bitterness"
    elif ibu < 30:
        return "moderate hop bitterness"
    elif ibu < 45:
        return "notable hop bitterness"
    elif ibu < 60:
        return "strong hop bitterness"
    elif ibu < 80:
        return "very strong hop bitterness"
    else:
        return "extreme hop bitterness"


# ============================================================================
# Color & SRM Functions
# ============================================================================

def calc_srm(lovibond: float, degree: float = 1.0) -> float:
    """
    Convert Lovibond to SRM (Standard Reference Method).
    
    Args:
        lovibond: Grain/color rating in degrees Lovibond
        degree: Adjustment factor for large hop additions
        
    Returns:
        SRM value
        
    Example:
        >>> calc_srm(10.0)
        9.1
    """
    if lovibond <= 0:
        return 0.0
    # Standard conversion: SRM ≈ 0.7 * Lovibond + 2 (Morey-inspired for homebrew)
    srm = 0.7 * lovibond + 2
    if srm < 1.0:
        srm = 1.0
    return round(srm, 1)


def srm_to_rgb(srm: float) -> Tuple[int, int, int]:
    """
    Convert SRM value to approximate RGB color.
    
    Args:
        srm: SRM value
        
    Returns:
        Tuple of (R, G, B) values
    """
    if srm <= 0:
        return (255, 255, 255)
    if srm >= 40:
        return SRM_COLORS[40]
    
    srm_int = int(srm)
    if srm_int in SRM_COLORS:
        return SRM_COLORS[srm_int]
    
    # Interpolate between closest values
    lower = max(1, srm_int - 1)
    upper = min(40, srm_int + 1)
    if lower == upper:
        return SRM_COLORS[lower]
    
    t = srm - srm_int
    r1, g1, b1 = SRM_COLORS[lower]
    r2, g2, b2 = SRM_COLORS[upper]
    
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    
    return (max(0, min(255, r)), (max(0, min(255, g))), (max(0, min(255, b))))


def srm_to_hex(srm: float) -> str:
    """
    Convert SRM value to approximate HEX color.
    
    Args:
        srm: SRM value
        
    Returns:
        HEX color string (e.g., "#FF6600")
    """
    r, g, b = srm_to_rgb(srm)
    return f"#{r:02X}{g:02X}{b:02X}"


def srm_to_style(srm: float) -> str:
    """
    Get beer color description from SRM.
    
    Args:
        srm: SRM value
        
    Returns:
        Color description
    """
    if srm < 2:
        return "pale straw"
    elif srm < 3:
        return "yellow"
    elif srm < 4:
        return "gold"
    elif srm < 6:
        return "amber"
    elif srm < 8:
        return "deep amber"
    elif srm < 10:
        return "copper"
    elif srm < 13:
        return "deep copper"
    elif srm < 17:
        return "brown"
    elif srm < 20:
        return "dark brown"
    elif srm < 25:
        return "very dark brown"
    elif srm < 30:
        return "very dark brown (almost black)"
    else:
        return "black"


def calc_color_mcu(weight_lbs: float, lovibond: float, volume: float) -> float:
    """
    Calculate Color in Morey Cubic Method.
    
    Args:
        weight_lbs: Grain weight in pounds
        lovibond: Grain lovibond rating
        volume: Volume in gallons
        
    Returns:
        MCU value
    """
    if volume <= 0 or weight_lbs <= 0:
        return 0.0
    mcu = (weight_lbs * lovibond) / volume
    return round(mcu, 2)


def mcu_to_srm(mcu: float) -> float:
    """
    Convert MCU to SRM using Morey equation.
    
    Args:
        mcu: MCU value
        
    Returns:
        SRM value
    """
    if mcu <= 0:
        return 1.0
    if mcu < 1.0:
        return 1.0
    srm = 1.4922 * (mcu ** 0.6859)
    return round(srm, 1)


# ============================================================================
# Carbonation Functions
# ============================================================================

def calc_carbonation_volumes(
    co2_grams: float,
    volume: float
) -> float:
    """
    Calculate CO2 volumes from grams per liter.
    
    Args:
        co2_grams: CO2 in grams per liter
        volume: Volume in liters
        
    Returns:
        CO2 volumes
    """
    if volume <= 0:
        return 0.0
    volumes = (co2_grams * volume) / volume * 0.5
    volumes = co2_grams * 0.5
    return round(volumes, 2)


def grams_per_liter_to_volumes(grams: float) -> float:
    """
    Convert CO2 grams per liter to volumes.
    
    Args:
        grams: CO2 grams per liter
        
    Returns:
        CO2 volumes
    """
    return round(grams * 0.5, 2)


def volumes_to_grams_per_liter(volumes: float) -> float:
    """
    Convert CO2 volumes to grams per liter.
    
    Args:
        volumes: CO2 volumes
        
    Returns:
        CO2 grams per liter
    """
    return round(volumes * 2, 2)


def calc_priming_sugar(
    volume: float,
    target_volumes: float,
    current_volumes: float = 0.0,
    sugar_type: str = "corn_sugar"
) -> float:
    """
    Calculate priming sugar needed for bottle conditioning.
    
    Args:
        volume: Volume in liters
        target_volumes: Target CO2 volumes
        current_volumes: Current CO2 volumes in beer
        sugar_type: Sugar type ("corn_sugar", "table_sugar", "dme")
        
    Returns:
        Grams of priming sugar needed
        
    Example:
        >>> round(calc_priming_sugar(19, 2.5, 0), 1)
        122.4
    """
    co2_needed = target_volumes - current_volumes
    if co2_needed <= 0:
        return 0.0
    
    # CO2 yield per gram of sugar (in volumes for 1 liter)
    # yield = (target_volumes * volume) / grams, so for 120g in 19L at 2.5 vol:
    # yield = (2.5 * 19) / 120 = 0.3958
    yields = {
        "corn_sugar": 0.3958,
        "table_sugar": 0.4203,
        "dme": 0.2105,  # ~227g for 19L at 2.5 volumes
        "honey": 0.4500,
    }
    
    sugar_yield = yields.get(sugar_type, yields["corn_sugar"])
    grams_needed = (co2_needed * volume) / sugar_yield
    
    return round(grams_needed, 1)


def carbonation_style_correction(
    altitude_ft: float = 0,
    style_volumes: float = 2.5
) -> float:
    """
    Adjust carbonation for altitude (pressure changes).
    
    Args:
        altitude_ft: Altitude in feet
        style_volumes: Target volumes at sea level
        
    Returns:
        Adjusted target volumes
    """
    if altitude_ft <= 0:
        return style_volumes
    
    # Approximately 0.2 volumes less per 1000ft above 5000ft
    if altitude_ft < 5000:
        return style_volumes
    
    adjustment = (altitude_ft - 5000) / 1000 * 0.2
    return round(max(0.5, style_volumes - adjustment), 1)


# ============================================================================
# Mash & Boil Calculations
# ============================================================================

def calc_mash_thickness(grain_lbs: float, water_gal: float) -> float:
    """
    Calculate mash thickness (quarts per pound).
    
    Args:
        grain_lbs: Grain weight in pounds
        water_gal: Water volume in gallons
        
    Returns:
        Mash thickness in quarts per pound
    """
    if grain_lbs <= 0:
        return 0.0
    quarts_per_lb = (water_gal * 4) / grain_lbs
    return round(quarts_per_lb, 2)


def calc_strike_temperature(
    target_temp: float,
    grain_temp: float,
    grain_weight: float,
    water_volume: float,
    mash_thickness: float = 2.0
) -> float:
    """
    Calculate strike water temperature.
    
    Args:
        target_temp: Target mash temperature (F)
        grain_temp: Grain temperature (F)
        grain_weight: Grain weight in pounds
        water_volume: Water volume in quarts
        mash_thickness: Mash thickness (quarts/lb)
        
    Returns:
        Strike water temperature (F)
    """
    if grain_weight <= 0:
        return target_temp
    
    # Ratio of water to grain
    r = water_volume / grain_weight
    strike_temp = (target_temp - grain_temp) / r + target_temp
    return round(strike_temp, 1)


def calc_boil_off(
    start_volume: float,
    start_gravity: float,
    end_volume: float
) -> Dict[str, float]:
    """
    Calculate boil-off rate and evaporation.
    
    Args:
        start_volume: Starting volume (gallons)
        start_gravity: Starting gravity (OG)
        end_volume: Ending volume (gallons)
        
    Returns:
        Dictionary with boil-off details
    """
    if end_volume >= start_volume or start_volume <= 0:
        return {"evaporation_percent": 0.0, "evaporation_gallons": 0.0, "final_gravity": start_gravity}
    
    evaporation_gal = start_volume - end_volume
    evaporation_percent = (evaporation_gal / start_volume) * 100
    
    # Concentrate the wort
    concentration = start_volume / end_volume
    final_gravity = 1 + (start_gravity - 1) * concentration
    
    return {
        "evaporation_percent": round(evaporation_percent, 1),
        "evaporation_gallons": round(evaporation_gal, 2),
        "final_gravity": round(final_gravity, 3),
        "concentration_factor": round(concentration, 3),
    }


def calc_evaporation_rate(
    volume_start: float,
    time_start: float,
    volume_end: float,
    time_end: float
) -> float:
    """
    Calculate hourly boil-off evaporation rate.
    
    Args:
        volume_start: Starting volume (gallons)
        time_start: Start time (minutes)
        volume_end: Ending volume (gallons)
        time_end: End time (minutes)
        
    Returns:
        Evaporation rate in gallons per hour
    """
    if time_end <= time_start:
        return 0.0
    
    volume_lost = volume_start - volume_end
    hours = (time_end - time_start) / 60
    
    if hours <= 0:
        return 0.0
    
    return round(volume_lost / hours, 2)


# ============================================================================
# Recipe Scaling
# ============================================================================

def scale_recipe(
    original_volume: float,
    target_volume: float,
    original_grain_bill: Dict[str, float]
) -> Dict[str, float]:
    """
    Scale grain bill for different batch size.
    
    Args:
        original_volume: Original batch volume (gallons)
        target_volume: Target batch volume (gallons)
        original_grain_bill: Dict of {grain_name: weight_lbs}
        
    Returns:
        Scaled grain bill dictionary
        
    Example:
        >>> scale_recipe(5, 10, {"pilsner": 5, "crystal": 1})
        {'pilsner': 10.0, 'crystal': 2.0}
    """
    if original_volume <= 0 or target_volume <= 0:
        return original_grain_bill
    
    scale_factor = target_volume / original_volume
    scaled = {grain: round(weight * scale_factor, 2) for grain, weight in original_grain_bill.items()}
    return scaled


def scale_hops(
    original_volume: float,
    target_volume: float,
    original_hops: List[Dict],
    og_adjustment: float = 1.0
) -> List[Dict]:
    """
    Scale hop additions for new batch size.
    
    Args:
        original_volume: Original volume (gallons)
        target_volume: Target volume (gallons)
        original_hops: List of hop dicts with "weight", "alpha", "time"
        og_adjustment: OG adjustment factor
        
    Returns:
        List of scaled hop additions
    """
    if original_volume <= 0 or target_volume <= 0:
        return original_hops
    
    scale_factor = target_volume / original_volume
    adjusted_factor = scale_factor * og_adjustment
    
    scaled = []
    for hop in original_hops:
        scaled.append({
            "weight": round(hop["weight"] * adjusted_factor, 2),
            "alpha": hop["alpha"],
            "time": hop["time"],
        })
    
    return scaled


def calc_ibu_for_scaled_recipe(
    original_ibu: float,
    original_volume: float,
    target_volume: float,
    original_og: float,
    target_og: float
) -> float:
    """
    Estimate IBU for scaled recipe.
    
    Args:
        original_ibu: Original IBU
        original_volume: Original volume (gallons)
        target_volume: Target volume (gallons)
        original_og: Original OG
        target_og: Target OG
        
    Returns:
        Estimated IBU for scaled recipe
    """
    if original_volume <= 0 or target_volume <= 0:
        return original_ibu
    
    volume_factor = original_volume / target_volume
    gravity_factor = (target_og - 1.0) / (original_og - 1.0) if original_og > 1.0 else 1.0
    
    new_ibu = original_ibu * volume_factor * gravity_factor
    return round(new_ibu, 1)


# ============================================================================
# Efficiency & Yield Functions
# ============================================================================

def calc_extract_potential(grain_lovibond: float) -> float:
    """
    Calculate grain extract potential (points per pound per gallon).
    
    Args:
        grain_lovibond: Grain color in degrees Lovibond
        
    Returns:
        Extract potential in PPG
    """
    return round(46.0 - (grain_lovibond * 0.6), 1)


def calc_yield_percent(grain_lovibond: float) -> float:
    """
    Calculate grain yield percentage.
    
    Args:
        grain_lovibond: Grain color in degrees Lovibond
        
    Returns:
        Yield percentage
    """
    potential_ppg = calc_extract_potential(grain_lovibond)
    return round((potential_ppg / 46.0) * 100, 1)


def calc_mash_efficiency(
    actual_og: float,
    target_og: float,
    grain_lbs: float,
    volume_gal: float
) -> float:
    """
    Calculate mash efficiency percentage.
    
    Args:
        actual_og: Actual Original Gravity
        target_og: Target Original Gravity
        grain_lbs: Total grain weight (lbs)
        volume_gal: Volume in gallons
        
    Returns:
        Efficiency percentage
    """
    if actual_og <= 1.0 or target_og <= 1.0 or grain_lbs <= 0 or volume_gal <= 0:
        return 0.0
    
    actual_points = (actual_og - 1.0) * 1000
    target_points = (target_og - 1.0) * 1000
    
    return round((actual_points / target_points) * 100, 1)


def calc_lauter_efficiency(grain_lbs: float, runoff_volume: float, runoff_sg: float) -> float:
    """
    Calculate lautering efficiency.
    
    Args:
        grain_lbs: Grain weight in pounds
        runoff_volume: Runoff volume in gallons
        runoff_sg: Runoff specific gravity
        
    Returns:
        Efficiency percentage
    """
    if grain_lbs <= 0 or runoff_volume <= 0 or runoff_sg <= 1.0:
        return 0.0
    
    extract = (runoff_sg - 1.0) * 1000 * runoff_volume
    max_extract = grain_lbs * 46.0
    
    return round((extract / max_extract) * 100, 1)


# ============================================================================
# Equipment & Process Functions
# ============================================================================

def calc_keg_pressure(
    volume: float,
    temperature: float,
    style_volumes: float = 2.5,
    temperature_unit: str = "F"
) -> float:
    """
    Calculate required CO2 pressure for force carbonation.
    
    Args:
        volume: Target CO2 volumes
        temperature: Temperature
        style_volumes: Target volumes
        temperature_unit: "F" or "C"
        
    Returns:
        Required PSI
    """
    if temperature_unit == "C":
        temp_f = temperature * 9 / 5 + 32
    else:
        temp_f = temperature
    
    # Rough estimate using Henry's law approximation
    base_psi = volume * 5.0
    
    # Temperature correction (rough)
    if temp_f > 40:
        temp_factor = 1 + (temp_f - 40) * 0.02
    else:
        temp_factor = 1.0
    
    target_psi = (style_volumes - volume) * 5.0 * temp_factor
    return round(max(0, target_psi), 1)


def calc_batch_gravity(
    volume: float,
    gravity_points: List[Tuple[float, float]]
) -> float:
    """
    Calculate blended batch gravity.
    
    Args:
        volume: Total volume
        gravity_points: List of (volume, gravity-1.000) tuples
        
    Returns:
        Final specific gravity
    """
    if volume <= 0 or not gravity_points:
        return 1.0
    
    total_points = sum(v * gp for v, gp in gravity_points)
    avg_points = total_points / volume
    
    return round(1.0 + avg_points, 3)


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Constants
    "WATER_SG",
    "CARBONATION_STYLES",
    "SRM_COLORS",
    # Gravity & ABV
    "calc_abv",
    "calc_abv_from_plato",
    "sg_to_plato",
    "plato_to_sg",
    "calc_attenuation",
    "calc_real_attenuation",
    "calc_fg_from_attenuation",
    # Hop & IBU
    "calc_ibu",
    "calc_hop_utilization",
    "ibu_category",
    # Color & SRM
    "calc_srm",
    "srm_to_rgb",
    "srm_to_hex",
    "srm_to_style",
    "calc_color_mcu",
    "mcu_to_srm",
    # Carbonation
    "calc_carbonation_volumes",
    "grams_per_liter_to_volumes",
    "volumes_to_grams_per_liter",
    "calc_priming_sugar",
    "carbonation_style_correction",
    # Mash & Boil
    "calc_mash_thickness",
    "calc_strike_temperature",
    "calc_boil_off",
    "calc_evaporation_rate",
    # Recipe Scaling
    "scale_recipe",
    "scale_hops",
    "calc_ibu_for_scaled_recipe",
    # Efficiency & Yield
    "calc_extract_potential",
    "calc_yield_percent",
    "calc_mash_efficiency",
    "calc_lauter_efficiency",
    # Equipment
    "calc_keg_pressure",
    "calc_batch_gravity",
]