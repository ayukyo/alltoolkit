# Fuel Consumption Utils Test

import sys
import os
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fuel_consumption_utils.mod import (
    mpg_to_liters_per_100km,
    liters_per_100km_to_mpg,
    km_per_liter_to_mpg,
    mpg_to_km_per_liter,
    calculate_consumption,
    calculate_trip_fuel,
    calculate_carbon_emission,
    estimate_range,
    compare_vehicles,
    get_consumption_rating,
    format_consumption,
    quick_mpg_convert,
    FuelConsumptionResult,
    TripFuelResult,
    CarbonEmissionResult,
    GALLONS_TO_LITERS,
    LITERS_TO_GALLONS,
    MILES_TO_KM,
    KM_TO_MILES,
    CO2_FACTORS,
    TREE_CO2_ABSORPTION_PER_YEAR,
)


class TestFuelConversion(unittest.TestCase):
    """Test fuel consumption unit conversions."""

    def test_mpg_to_liters_per_100km(self):
        """Test MPG to L/100km conversion."""
        self.assertAlmostEqual(mpg_to_liters_per_100km(30), 7.84, places=2)
        self.assertAlmostEqual(mpg_to_liters_per_100km(50), 4.70, places=2)
    
    def test_liters_per_100km_to_mpg(self):
        """Test L/100km to MPG conversion."""
        self.assertAlmostEqual(liters_per_100km_to_mpg(8), 29.40, places=2)
        self.assertAlmostEqual(liters_per_100km_to_mpg(5), 47.04, places=2)
    
    def test_km_per_liter_to_mpg(self):
        """Test km/L to MPG conversion."""
        result = km_per_liter_to_mpg(10)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)
    
    def test_mpg_to_km_per_liter(self):
        """Test MPG to km/L conversion."""
        result = mpg_to_km_per_liter(30)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)
    
    def test_quick_mpg_convert(self):
        """Test quick conversion utility."""
        self.assertAlmostEqual(quick_mpg_convert(30, 'mpg', 'l100km'), 7.84, places=2)
        self.assertAlmostEqual(quick_mpg_convert(8, 'l100km', 'mpg'), 29.40, places=2)
        self.assertEqual(quick_mpg_convert(30, 'mpg', 'mpg'), 30)


class TestFuelCalculation(unittest.TestCase):
    """Test fuel consumption calculation."""

    def test_calculate_consumption_miles_gallons(self):
        """Test consumption calculation with miles and gallons."""
        result = calculate_consumption(distance_miles=300, fuel_gallons=10)
        self.assertIsInstance(result, FuelConsumptionResult)
        self.assertEqual(result.mpg, 30.0)
    
    def test_calculate_consumption_km_liters(self):
        """Test consumption calculation with km and liters."""
        result = calculate_consumption(distance_km=500, fuel_liters=40)
        self.assertIsInstance(result, FuelConsumptionResult)
        self.assertGreater(result.liters_per_100km, 0)
    
    def test_calculate_consumption_invalid(self):
        """Test invalid input handling."""
        with self.assertRaises(ValueError):
            calculate_consumption()  # no distance provided
        with self.assertRaises(ValueError):
            calculate_consumption(distance_km=500)  # no fuel provided

    def test_format_consumption(self):
        """Test result formatting."""
        result = FuelConsumptionResult(mpg=30.0, liters_per_100km=7.84, km_per_liter=13.0)
        formatted = format_consumption(result)
        self.assertIn("MPG", formatted)
        self.assertIn("L/100km", formatted)


class TestTripFuel(unittest.TestCase):
    """Test trip fuel calculation."""

    def test_calculate_trip_fuel_basic(self):
        """Test basic trip fuel calculation."""
        result = calculate_trip_fuel(distance_km=500, consumption_liters_per_100km=8)
        self.assertIsInstance(result, TripFuelResult)
        self.assertEqual(result.fuel_needed_liters, 40.0)
        self.assertGreater(result.estimated_cost_local, 0)
    
    def test_calculate_trip_fuel_with_cost(self):
        """Test trip fuel with custom fuel price."""
        result = calculate_trip_fuel(
            distance_km=100,
            consumption_liters_per_100km=10,
            fuel_price_per_liter=8.0
        )
        self.assertEqual(result.fuel_needed_liters, 10.0)
        self.assertEqual(result.estimated_cost_local, 80.0)
    
    def test_calculate_trip_fuel_invalid(self):
        """Test invalid input handling."""
        with self.assertRaises(ValueError):
            calculate_trip_fuel(distance_km=0, consumption_liters_per_100km=8)
        with self.assertRaises(ValueError):
            calculate_trip_fuel(distance_km=500, consumption_liters_per_100km=0)


class TestCarbonEmission(unittest.TestCase):
    """Test carbon emission calculation."""

    def test_calculate_carbon_gasoline(self):
        """Test carbon emission for gasoline."""
        result = calculate_carbon_emission(fuel_liters=40, fuel_type='gasoline')
        self.assertIsInstance(result, CarbonEmissionResult)
        self.assertEqual(result.co2_kg, 92.4)  # 40 * 2.31
        self.assertGreater(result.trees_needed, 0)
    
    def test_calculate_carbon_diesel(self):
        """Test carbon emission for diesel."""
        result = calculate_carbon_emission(fuel_liters=40, fuel_type='diesel')
        self.assertEqual(result.co2_kg, 107.2)  # 40 * 2.68
    
    def test_calculate_carbon_invalid_fuel(self):
        """Test invalid fuel type handling."""
        with self.assertRaises(ValueError):
            calculate_carbon_emission(fuel_liters=40, fuel_type='unknown')


class TestRangeEstimation(unittest.TestCase):
    """Test range estimation."""

    def test_estimate_range_full_tank(self):
        """Test range estimation with full tank."""
        km, miles = estimate_range(tank_capacity_liters=50, consumption_liters_per_100km=8)
        self.assertEqual(km, 625.0)
        self.assertGreater(miles, 0)
    
    def test_estimate_range_partial_tank(self):
        """Test range estimation with partial tank."""
        km, miles = estimate_range(tank_capacity_liters=50, consumption_liters_per_100km=8, current_fuel_percentage=50)
        self.assertEqual(km, 312.5)
    
    def test_estimate_range_invalid(self):
        """Test invalid input handling."""
        with self.assertRaises(ValueError):
            estimate_range(tank_capacity_liters=0, consumption_liters_per_100km=8)
        with self.assertRaises(ValueError):
            estimate_range(tank_capacity_liters=50, consumption_liters_per_100km=0)
        with self.assertRaises(ValueError):
            estimate_range(tank_capacity_liters=50, consumption_liters_per_100km=8, current_fuel_percentage=150)


class TestVehicleComparison(unittest.TestCase):
    """Test vehicle comparison."""

    def test_compare_vehicles(self):
        """Test vehicle comparison."""
        result = compare_vehicles(vehicle1_consumption=10, vehicle2_consumption=7)
        self.assertIn('vehicle1_cost', result)
        self.assertIn('vehicle2_cost', result)
        self.assertIn('annual_savings', result)
        self.assertEqual(result['better_vehicle'], 2)
    
    def test_compare_vehicles_same_consumption(self):
        """Test comparison with same consumption."""
        result = compare_vehicles(vehicle1_consumption=8, vehicle2_consumption=8)
        self.assertEqual(result['annual_savings'], 0)


class TestConsumptionRating(unittest.TestCase):
    """Test consumption rating."""

    def test_get_consumption_rating(self):
        """Test consumption rating."""
        rating = get_consumption_rating(5, 'car')
        self.assertEqual(rating, 'Excellent ⭐⭐⭐⭐⭐')
        
        rating = get_consumption_rating(12, 'car')
        self.assertEqual(rating, 'Poor ⭐⭐')


class TestConstants(unittest.TestCase):
    """Test module constants."""

    def test_conversion_constants(self):
        """Test conversion constants values."""
        self.assertAlmostEqual(MILES_TO_KM, 1.609344)
        self.assertAlmostEqual(KM_TO_MILES, 0.621371)
        self.assertAlmostEqual(GALLONS_TO_LITERS, 3.785411784)
        self.assertAlmostEqual(LITERS_TO_GALLONS, 0.264172)
    
    def test_co2_factors(self):
        """Test CO2 emission factors."""
        self.assertIn('gasoline', CO2_FACTORS)
        self.assertIn('diesel', CO2_FACTORS)
        self.assertGreater(CO2_FACTORS['diesel'], CO2_FACTORS['gasoline'])


if __name__ == '__main__':
    unittest.main()