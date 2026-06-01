#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Beer Brewing Utilities Usage Examples
==================================================
Practical examples demonstrating beer_utils module usage.
"""

from mod import (
    calc_abv, sg_to_plato, plato_to_sg,
    calc_ibu, calc_hop_utilization, ibu_category,
    calc_srm, srm_to_rgb, srm_to_style,
    grams_per_liter_to_volumes, calc_priming_sugar,
    calc_mash_thickness, calc_strike_temperature,
    scale_recipe, scale_hops,
    calc_mash_efficiency, CARBONATION_STYLES,
)


def example_basic_abv():
    """Calculate ABV for a standard APA."""
    og = 1.055
    fg = 1.012
    abv = calc_abv(og, fg)
    print(f"American Pale Ale:")
    print(f"  OG: {og}, FG: {fg}")
    print(f"  ABV: {abv}%")
    print(f"  Attenuation: {((og - fg) / (og - 1.0) * 100):.1f}%")


def example_plato_conversion():
    """Convert between SG and Plato."""
    print("\nSpecific Gravity <-> Plato Conversion:")
    for sg in [1.030, 1.040, 1.050, 1.060, 1.070, 1.080]:
        plato = sg_to_plato(sg)
        back_sg = plato_to_sg(plato)
        print(f"  {sg:.3f} SG -> {plato:.1f}°P -> {back_sg:.3f} SG")


def example_ibu_calculation():
    """Calculate IBU for a DIPA recipe."""
    print("\nDIPA Hop Schedule:")
    hops = [
        {"alpha": 12.0, "weight": 28, "time": 60, "name": "Cascade @ 60min"},
        {"alpha": 10.0, "weight": 28, "time": 30, "name": "Citra @ 30min"},
        {"alpha": 7.0, "weight": 28, "time": 15, "name": "Simcoe @ 15min"},
        {"alpha": 5.5, "weight": 57, "time": 5, "name": "Mosaic @ flameout"},
    ]
    
    total_ibu = 0
    og = 1.075
    volume = 19  # liters
    
    for hop in hops:
        ibu = calc_ibu(hop["alpha"], hop["weight"], hop["time"], og, volume)
        total_ibu += ibu
        print(f"  {hop['name']}: {ibu:.1f} IBU")
    
    print(f"  Total IBU: {total_ibu:.1f}")
    print(f"  Category: {ibu_category(total_ibu)}")


def example_color_beer_styles():
    """Show SRM colors for different beer styles."""
    print("\nBeer Style Colors:")
    styles = [
        ("Light Lager", 2),
        ("Pilsner", 4),
        ("Pale Ale", 6),
        ("IPA", 8),
        ("Amber Ale", 12),
        ("Brown Porter", 17),
        ("Schwarzbier", 25),
        ("Stout", 30),
        ("Imperial Stout", 35),
    ]
    
    for style, srm in styles:
        rgb = srm_to_rgb(srm)
        desc = srm_to_style(srm)
        print(f"  {style:20} SRM:{srm:2} RGB:{rgb} -> {desc}")


def example_carbonation():
    """Calculate carbonation for bottling."""
    print("\nBottle Conditioning:")
    volume = 19  # liters
    target = CARBONATION_STYLES["wheat_beer"]
    
    sugar = calc_priming_sugar(volume, target, 0, "corn_sugar")
    print(f"  Target: {target} volumes CO2 (wheat beer style)")
    print(f"  Corn sugar needed: {sugar:.1f}g")
    
    sugar_table = calc_priming_sugar(volume, target, 0, "table_sugar")
    print(f"  Table sugar needed: {sugar_table:.1f}g")


def example_mash_calculations():
    """Calculate mash parameters."""
    print("\nMash Parameters:")
    grain_lbs = 12
    water_gal = 6.5
    
    thickness = calc_mash_thickness(grain_lbs, water_gal)
    print(f"  Grain: {grain_lbs} lbs")
    print(f"  Water: {water_gal} gal")
    print(f"  Mash Thickness: {thickness} qt/lb")
    
    strike = calc_strike_temperature(152, 68, grain_lbs, 26)
    print(f"  Strike Temp: {strike:.1f}°F (target mash 152°F)")


def example_recipe_scaling():
    """Scale a grain bill from 5gal to 10gal batch."""
    print("\nRecipe Scaling (5gal -> 10gal):")
    original = {
        "Pilsner": 6.0,
        "Vienna": 1.5,
        "Caramel 60L": 0.5,
        "Saaz Hops": 1.0,
    }
    
    scaled = scale_recipe(5, 10, original)
    print("  Original (5 gal):")
    for grain, weight in original.items():
        print(f"    {grain}: {weight} lbs")
    
    print("  Scaled (10 gal):")
    for grain, weight in scaled.items():
        print(f"    {grain}: {weight} lbs")


def example_full_recipe_analysis():
    """Analyze a complete recipe."""
    print("\n" + "=" * 50)
    print("FULL RECIPE ANALYSIS: House IPA")
    print("=" * 50)
    
    # Recipe specs
    batch_size = 5.5  # gallons
    og = 1.064
    fg = 1.014
    boil_volume = 7.0
    boil_time = 60
    boil_end_volume = 5.5
    
    # Grain bill
    grain_bill = {
        "Pale 2-Row": 11.5,
        "Caramel 40L": 0.75,
        "Munich 10L": 0.5,
    }
    
    # Hop bill
    hops = [
        {"alpha": 6.5, "weight": 1.0, "time": 60},
        {"alpha": 5.0, "weight": 1.5, "time": 30},
        {"alpha": 4.0, "weight": 2.0, "time": 10},
        {"alpha": 3.0, "weight": 2.0, "time": 5},
    ]
    
    # Calculations
    abv = calc_abv(og, fg)
    ibu = sum(calc_ibu(h["alpha"], h["weight"], h["time"], og, batch_size) for h in hops)
    
    # Color estimation (simplified)
    total_lovibond = sum(grain_bill[grain] * 3.5 for grain in grain_bill)  # approximate
    color_mcu = (total_lovibond * 10) / batch_size
    srm = mcu_to_srm(color_mcu)
    
    efficiency = calc_mash_efficiency(og, 1.070, sum(grain_bill.values()), batch_size)
    
    # Output
    print(f"\nBatch Size: {batch_size} gal")
    print(f"OG: {og} | FG: {fg} | ABV: {abv}%")
    print(f"IBU: {ibu:.0f} ({ibu_category(ibu)})")
    print(f"Color: {srm:.0f} SRM ({srm_to_style(srm)})")
    print(f"Mash Efficiency: {efficiency:.0f}%")
    
    print("\nGrain Bill:")
    for grain, weight in grain_bill.items():
        print(f"  {grain}: {weight} lbs")
    
    print("\nHop Schedule:")
    for h in hops:
        print(f"  {h['weight']}oz @ {h['time']}min (alpha {h['alpha']}%)")


def example_unit_conversions():
    """Show common unit conversions."""
    print("\nUnit Conversions:")
    
    # Gallons to liters
    gal = 5
    liters = gal * 3.78541
    print(f"  {gal} gal = {liters:.2f} L")
    
    # Ounces to grams
    oz = 1
    grams = oz * 28.3495
    print(f"  {oz} oz = {grams:.1f} g")
    
    # Fahrenheit to Celsius
    for temp_f in [150, 160, 170, 180, 190, 200, 212]:
        temp_c = (temp_f - 32) * 5 / 9
        print(f"  {temp_f}°F = {temp_c:.1f}°C")


if __name__ == "__main__":
    example_basic_abv()
    example_plato_conversion()
    example_ibu_calculation()
    example_color_beer_styles()
    example_carbonation()
    example_mash_calculations()
    example_recipe_scaling()
    example_full_recipe_analysis()
    example_unit_conversions()