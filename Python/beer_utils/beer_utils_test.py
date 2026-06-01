#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Beer Brewing Utilities Test Suite
==============================================
Comprehensive tests for beer brewing utilities module.
"""

import unittest
from mod import (
    # Gravity & ABV
    calc_abv, calc_abv_from_plato,
    sg_to_plato, plato_to_sg,
    calc_attenuation, calc_real_attenuation,
    calc_fg_from_attenuation,
    # Hop & IBU
    calc_ibu, calc_hop_utilization, ibu_category,
    # Color & SRM
    calc_srm, srm_to_rgb, srm_to_hex, srm_to_style,
    calc_color_mcu, mcu_to_srm,
    # Carbonation
    calc_carbonation_volumes, grams_per_liter_to_volumes,
    volumes_to_grams_per_liter, calc_priming_sugar,
    carbonation_style_correction,
    # Mash & Boil
    calc_mash_thickness, calc_strike_temperature,
    calc_boil_off, calc_evaporation_rate,
    # Recipe Scaling
    scale_recipe, scale_hops, calc_ibu_for_scaled_recipe,
    # Efficiency & Yield
    calc_extract_potential, calc_yield_percent,
    calc_mash_efficiency, calc_lauter_efficiency,
    # Equipment
    calc_keg_pressure, calc_batch_gravity,
    SRM_COLORS, CARBONATION_STYLES,
)


class TestGravityAndABV(unittest.TestCase):
    """Test gravity and ABV calculations."""
    
    def test_calc_abv_standard(self):
        """Test standard ABV calculation."""
        abv = calc_abv(1.050, 1.010)
        self.assertAlmostEqual(abv, 5.3, places=1)
    
    def test_calc_abv_strong_beer(self):
        """Test ABV for strong beer."""
        abv = calc_abv(1.080, 1.015)
        self.assertAlmostEqual(abv, 8.5, places=1)
    
    def test_calc_abv_invalid(self):
        """Test ABV with invalid inputs."""
        self.assertEqual(calc_abv(1.010, 1.050), 0.0)
        self.assertEqual(calc_abv(1.0, 1.010), 0.0)
    
    def test_sg_to_plato(self):
        """Test SG to Plato conversion."""
        plato = sg_to_plato(1.050)
        self.assertAlmostEqual(plato, 12.4, places=1)
    
    def test_plato_to_sg(self):
        """Test Plato to SG conversion."""
        sg = plato_to_sg(12.0)
        self.assertAlmostEqual(sg, 1.048, places=2)
    
    def test_plato_sg_roundtrip(self):
        """Test Plato/SG roundtrip conversion."""
        original_plato = 15.0
        sg = plato_to_sg(original_plato)
        back_to_plato = sg_to_plato(sg)
        self.assertAlmostEqual(back_to_plato, original_plato, places=1)
    
    def test_calc_attenuation(self):
        """Test apparent attenuation calculation."""
        atten = calc_attenuation(1.050, 1.010)
        self.assertAlmostEqual(atten, 80.0, places=0)
    
    def test_calc_real_attenuation(self):
        """Test real attenuation calculation."""
        atten = calc_real_attenuation(1.050, 1.010)
        self.assertGreater(atten, 0)
        self.assertLess(atten, 100)
    
    def test_calc_fg_from_attenuation(self):
        """Test FG estimation from attenuation."""
        fg = calc_fg_from_attenuation(1.050, 75.0)
        self.assertAlmostEqual(fg, 1.013, places=2)


class TestHopAndIBU(unittest.TestCase):
    """Test hop and IBU calculations."""
    
    def test_calc_ibu_tinseth(self):
        """Test IBU calculation with Tinseth formula."""
        ibu = calc_ibu(5.5, 28, 60, 1.050, 20)
        self.assertGreater(ibu, 0)
        self.assertLess(ibu, 100)
    
    def test_calc_ibu_rager(self):
        """Test IBU calculation with Rager formula."""
        ibu = calc_ibu(5.5, 28, 60, 1.050, 20, method="rager")
        self.assertGreater(ibu, 0)
    
    def test_calc_ibu_invalid(self):
        """Test IBU with invalid inputs."""
        self.assertEqual(calc_ibu(0, 28, 60, 1.050, 20), 0.0)
        self.assertEqual(calc_ibu(5.5, -1, 60, 1.050, 20), 0.0)
        self.assertEqual(calc_ibu(5.5, 28, 0, 1.050, 20), 0.0)
    
    def test_calc_hop_utilization(self):
        """Test hop utilization calculation."""
        util = calc_hop_utilization(60, 1.050)
        self.assertGreater(util, 0)
        self.assertLess(util, 100)
    
    def test_ibu_category(self):
        """Test IBU category mapping."""
        self.assertEqual(ibu_category(5), "no perceived hop bitterness")
        self.assertEqual(ibu_category(15), "low hop bitterness")
        self.assertEqual(ibu_category(50), "strong hop bitterness")
        self.assertEqual(ibu_category(100), "extreme hop bitterness")


class TestColorAndSRM(unittest.TestCase):
    """Test color and SRM calculations."""
    
    def test_calc_srm(self):
        """Test Lovibond to SRM conversion."""
        srm = calc_srm(10.0)
        self.assertAlmostEqual(srm, 9.0, places=1)
    
    def test_calc_srm_minimum(self):
        """Test SRM minimum value."""
        srm = calc_srm(0.5)
        self.assertGreaterEqual(srm, 1.0)
    
    def test_srm_to_rgb(self):
        """Test SRM to RGB conversion."""
        r, g, b = srm_to_rgb(10.0)
        self.assertTrue(all(0 <= c <= 255 for c in (r, g, b)))
    
    def test_srm_to_hex(self):
        """Test SRM to HEX conversion."""
        hex_color = srm_to_hex(10.0)
        self.assertTrue(hex_color.startswith("#"))
        self.assertEqual(len(hex_color), 7)
    
    def test_srm_to_style(self):
        """Test SRM to style description."""
        self.assertEqual(srm_to_style(2.0), "yellow")
        self.assertEqual(srm_to_style(5.0), "amber")
        self.assertEqual(srm_to_style(15.0), "brown")
        self.assertEqual(srm_to_style(30.0), "black")
    
    def test_calc_color_mcu(self):
        """Test MCU color calculation."""
        mcu = calc_color_mcu(10.0, 10.0, 5.0)
        self.assertAlmostEqual(mcu, 20.0, places=1)
    
    def test_mcu_to_srm(self):
        """Test MCU to SRM conversion."""
        srm = mcu_to_srm(20.0)
        self.assertGreater(srm, 0)
    
    def test_srm_colors_complete(self):
        """Test SRM color lookup table."""
        for srm_val, rgb in SRM_COLORS.items():
            self.assertEqual(len(rgb), 3)
            self.assertTrue(all(0 <= c <= 255 for c in rgb))


class TestCarbonation(unittest.TestCase):
    """Test carbonation calculations."""
    
    def test_grams_to_volumes(self):
        """Test grams per liter to volumes conversion."""
        volumes = grams_per_liter_to_volumes(5.0)
        self.assertAlmostEqual(volumes, 2.5, places=2)
    
    def test_volumes_to_grams(self):
        """Test volumes to grams per liter conversion."""
        grams = volumes_to_grams_per_liter(2.5)
        self.assertAlmostEqual(grams, 5.0, places=2)
    
    def test_calc_priming_sugar(self):
        """Test priming sugar calculation."""
        sugar = calc_priming_sugar(19, 2.5, 0)
        self.assertGreater(sugar, 0)
        self.assertLess(sugar, 500)
    
    def test_calc_priming_sugar_corn_sugar(self):
        """Test priming sugar with corn sugar."""
        sugar = calc_priming_sugar(19, 2.5, 0, "corn_sugar")
        self.assertGreater(sugar, 0)
    
    def test_calc_priming_sugar_table_sugar(self):
        """Test priming sugar with table sugar."""
        sugar = calc_priming_sugar(19, 2.5, 0, "table_sugar")
        self.assertGreater(sugar, 0)
    
    def test_carbonation_styles(self):
        """Test carbonation style constants."""
        self.assertIn("american_ale", CARBONATION_STYLES)
        self.assertIn("wheat_beer", CARBONATION_STYLES)
        for style, vol in CARBONATION_STYLES.items():
            self.assertGreater(vol, 0)
            self.assertLess(vol, 5)
    
    def test_carbonation_style_correction(self):
        """Test altitude carbonation correction."""
        corrected = carbonation_style_correction(7000, 2.5)
        self.assertLess(corrected, 2.5)


class TestMashAndBoil(unittest.TestCase):
    """Test mash and boil calculations."""
    
    def test_calc_mash_thickness(self):
        """Test mash thickness calculation."""
        thickness = calc_mash_thickness(10.0, 5.0)
        self.assertAlmostEqual(thickness, 2.0, places=1)
    
    def test_calc_strike_temperature(self):
        """Test strike water temperature calculation."""
        strike = calc_strike_temperature(152, 70, 10, 20)
        self.assertGreater(strike, 152)
        self.assertLess(strike, 212)
    
    def test_calc_boil_off(self):
        """Test boil-off calculation."""
        result = calc_boil_off(7.0, 1.050, 5.5)
        self.assertIn("evaporation_percent", result)
        self.assertIn("evaporation_gallons", result)
        self.assertIn("final_gravity", result)
        self.assertGreater(result["evaporation_gallons"], 0)
        self.assertGreater(result["final_gravity"], 1.050)
    
    def test_calc_evaporation_rate(self):
        """Test evaporation rate calculation."""
        rate = calc_evaporation_rate(7.0, 0, 5.5, 60)
        self.assertAlmostEqual(rate, 1.5, places=1)


class TestRecipeScaling(unittest.TestCase):
    """Test recipe scaling functions."""
    
    def test_scale_recipe(self):
        """Test grain bill scaling."""
        scaled = scale_recipe(5, 10, {"pilsner": 5, "crystal": 1})
        self.assertAlmostEqual(scaled["pilsner"], 10.0, places=1)
        self.assertAlmostEqual(scaled["crystal"], 2.0, places=1)
    
    def test_scale_recipe_same_size(self):
        """Test recipe scaling with same size."""
        scaled = scale_recipe(5, 5, {"pilsner": 5})
        self.assertAlmostEqual(scaled["pilsner"], 5.0, places=1)
    
    def test_scale_hops(self):
        """Test hop scaling."""
        hops = [{"weight": 28, "alpha": 5.5, "time": 60}]
        scaled = scale_hops(5, 10, hops)
        self.assertEqual(len(scaled), 1)
        self.assertGreater(scaled[0]["weight"], 28)
    
    def test_calc_ibu_for_scaled_recipe(self):
        """Test IBU estimation for scaled recipe."""
        ibu = calc_ibu_for_scaled_recipe(40, 5, 10, 1.050, 1.050)
        self.assertAlmostEqual(ibu, 20.0, places=0)


class TestEfficiencyAndYield(unittest.TestCase):
    """Test efficiency and yield calculations."""
    
    def test_calc_extract_potential(self):
        """Test extract potential calculation."""
        potential = calc_extract_potential(2.0)
        self.assertAlmostEqual(potential, 44.8, places=1)
    
    def test_calc_yield_percent(self):
        """Test yield percentage calculation."""
        yield_pct = calc_yield_percent(2.0)
        self.assertGreater(yield_pct, 90)
        self.assertLess(yield_pct, 100)
    
    def test_calc_mash_efficiency(self):
        """Test mash efficiency calculation."""
        eff = calc_mash_efficiency(1.045, 1.050, 10, 5)
        self.assertGreater(eff, 0)
        self.assertLess(eff, 100)
    
    def test_calc_lauter_efficiency(self):
        """Test lautering efficiency calculation."""
        eff = calc_lauter_efficiency(10, 5, 1.040)
        self.assertGreater(eff, 0)
        self.assertLess(eff, 100)


class TestEquipmentAndProcess(unittest.TestCase):
    """Test equipment and process calculations."""
    
    def test_calc_keg_pressure_fahrenheit(self):
        """Test keg pressure calculation in Fahrenheit."""
        psi = calc_keg_pressure(2.5, 38, 2.5)
        self.assertGreaterEqual(psi, 0)
    
    def test_calc_keg_pressure_celsius(self):
        """Test keg pressure calculation in Celsius."""
        psi = calc_keg_pressure(2.5, 3, 2.5, "C")
        self.assertGreaterEqual(psi, 0)
    
    def test_calc_batch_gravity(self):
        """Test batch gravity blending."""
        points = [(5, 0.050), (5, 0.040)]
        sg = calc_batch_gravity(10, points)
        self.assertAlmostEqual(sg, 1.045, places=2)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_zero_volume_handling(self):
        """Test handling of zero volumes."""
        self.assertEqual(calc_mash_thickness(10, 0), 0.0)
        self.assertEqual(calc_batch_gravity(0, [(5, 1.050)]), 1.0)
    
    def test_negative_values(self):
        """Test handling of negative values."""
        self.assertEqual(calc_priming_sugar(19, 2.5, 3), 0.0)  # negative CO2 needed
    
    def test_empty_grain_bill(self):
        """Test scaling empty grain bill."""
        scaled = scale_recipe(5, 10, {})
        self.assertEqual(len(scaled), 0)


if __name__ == "__main__":
    unittest.main()