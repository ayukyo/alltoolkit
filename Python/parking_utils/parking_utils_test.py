"""
parking_utils_test.py - Unit Tests for Parking Utils Module

Run with: python parking_utils_test.py
"""

import sys
import unittest
from datetime import datetime, timedelta
import math

# Import the module
from mod import (
    VehicleType,
    ParkingSpaceType,
    ParkingStatus,
    PricingModel,
    ParkingSpace,
    Vehicle,
    ParkingLot,
    ParkingTransaction,
    ParkingManager,
    calculate_hourly_parking_fee,
    calculate_tiered_parking_fee,
    calculate_flat_rate_fee,
    calculate_free_first_hour_fee,
    format_duration,
    estimate_parking_duration,
    find_parking_optimization_score,
    generate_parking_report,
    simulate_parking_scenario,
    validate_vehicle_id,
    validate_space_id,
    validate_pricing_config,
    check_parking_capacity,
    estimate_wait_time,
    VEHICLE_SPACE_REQUIREMENTS,
    SPACE_HIERARCHY,
    PARKING_UTILS_VERSION,
)


class TestEnums(unittest.TestCase):
    """Test enum definitions."""
    
    def test_vehicle_types(self):
        """Test VehicleType enum values."""
        self.assertEqual(VehicleType.MOTORCYCLE.value, "motorcycle")
        self.assertEqual(VehicleType.COMPACT.value, "compact")
        self.assertEqual(VehicleType.STANDARD.value, "standard")
        self.assertEqual(VehicleType.LARGE.value, "large")
        self.assertEqual(VehicleType.OVERSIZED.value, "oversized")
    
    def test_parking_space_types(self):
        """Test ParkingSpaceType enum values."""
        self.assertEqual(ParkingSpaceType.MOTORCYCLE.value, "motorcycle")
        self.assertEqual(ParkingSpaceType.ELECTRIC.value, "electric")
        self.assertEqual(ParkingSpaceType.HANDICAP.value, "handicap")
    
    def test_parking_status(self):
        """Test ParkingStatus enum values."""
        self.assertEqual(ParkingStatus.AVAILABLE.value, "available")
        self.assertEqual(ParkingStatus.OCCUPIED.value, "occupied")
        self.assertEqual(ParkingStatus.RESERVED.value, "reserved")
        self.assertEqual(ParkingStatus.MAINTENANCE.value, "maintenance")
    
    def test_pricing_model(self):
        """Test PricingModel enum values."""
        self.assertEqual(PricingModel.HOURLY.value, "hourly")
        self.assertEqual(PricingModel.DAILY_MAX.value, "daily_max")
        self.assertEqual(PricingModel.FLAT_RATE.value, "flat_rate")


class TestParkingSpace(unittest.TestCase):
    """Test ParkingSpace class."""
    
    def setUp(self):
        """Create a test parking space."""
        self.space = ParkingSpace(
            space_id="TEST-S001",
            space_type=ParkingSpaceType.STANDARD,
            level=0,
            row=5,
            column=10
        )
    
    def test_initial_state(self):
        """Test initial parking space state."""
        self.assertEqual(self.space.space_id, "TEST-S001")
        self.assertEqual(self.space.space_type, ParkingSpaceType.STANDARD)
        self.assertEqual(self.space.status, ParkingStatus.AVAILABLE)
        self.assertIsNone(self.space.vehicle_id)
        self.assertIsNone(self.space.entry_time)
    
    def test_is_available(self):
        """Test is_available method."""
        self.assertTrue(self.space.is_available())
        self.space.status = ParkingStatus.OCCUPIED
        self.assertFalse(self.space.is_available())
    
    def test_can_fit_vehicle(self):
        """Test can_fit_vehicle method."""
        # Standard space can fit standard, compact, motorcycle
        self.assertTrue(self.space.can_fit_vehicle(VehicleType.STANDARD))
        self.assertTrue(self.space.can_fit_vehicle(VehicleType.COMPACT))
        self.assertTrue(self.space.can_fit_vehicle(VehicleType.MOTORCYCLE))
        # But not large or oversized
        self.assertFalse(self.space.can_fit_vehicle(VehicleType.LARGE))
    
    def test_occupy(self):
        """Test occupy method."""
        entry_time = datetime.now()
        result = self.space.occupy("VEH-001", entry_time)
        self.assertTrue(result)
        self.assertEqual(self.space.status, ParkingStatus.OCCUPIED)
        self.assertEqual(self.space.vehicle_id, "VEH-001")
        self.assertEqual(self.space.entry_time, entry_time)
        
        # Cannot occupy again
        result2 = self.space.occupy("VEH-002", entry_time)
        self.assertFalse(result2)
    
    def test_vacate(self):
        """Test vacate method."""
        entry_time = datetime.now()
        self.space.occupy("VEH-001", entry_time)
        
        result = self.space.vacate()
        self.assertIsNotNone(result)
        self.assertEqual(self.space.status, ParkingStatus.AVAILABLE)
        self.assertIsNone(self.space.vehicle_id)
        
        # Cannot vacate available space
        result2 = self.space.vacate()
        self.assertIsNone(result2)
    
    def test_reserve(self):
        """Test reserve method."""
        until = datetime.now() + timedelta(hours=2)
        result = self.space.reserve(until)
        self.assertTrue(result)
        self.assertEqual(self.space.status, ParkingStatus.RESERVED)
        self.assertEqual(self.space.reserved_until, until)
    
    def test_maintenance(self):
        """Test maintenance methods."""
        result = self.space.set_maintenance()
        self.assertTrue(result)
        self.assertEqual(self.space.status, ParkingStatus.MAINTENANCE)
        
        result2 = self.space.end_maintenance()
        self.assertTrue(result2)
        self.assertEqual(self.space.status, ParkingStatus.AVAILABLE)
    
    def test_distance_calculation(self):
        """Test distance from entrance calculation."""
        distance = self.space.get_distance_from_entrance(0, 0, 0)
        self.assertEqual(distance, 15)  # 0 + 5 + 10
    
    def test_to_dict(self):
        """Test to_dict method."""
        data = self.space.to_dict()
        self.assertEqual(data["space_id"], "TEST-S001")
        self.assertEqual(data["space_type"], "standard")
        self.assertEqual(data["status"], "available")


class TestVehicle(unittest.TestCase):
    """Test Vehicle class."""
    
    def test_vehicle_creation(self):
        """Test vehicle creation."""
        vehicle = Vehicle(
            vehicle_id="VEH-001",
            vehicle_type=VehicleType.COMPACT,
            license_plate="ABC123",
            is_handicap_permitted=True
        )
        self.assertEqual(vehicle.vehicle_id, "VEH-001")
        self.assertEqual(vehicle.vehicle_type, VehicleType.COMPACT)
        self.assertTrue(vehicle.is_handicap_permitted)
    
    def test_get_required_space_types(self):
        """Test get_required_space_types method."""
        motorcycle = Vehicle("M-001", VehicleType.MOTORCYCLE)
        types = motorcycle.get_required_space_types()
        self.assertEqual(len(types), 5)  # All types can fit motorcycle
        self.assertEqual(types[0], ParkingSpaceType.MOTORCYCLE)
        
        standard = Vehicle("S-001", VehicleType.STANDARD)
        types2 = standard.get_required_space_types()
        self.assertEqual(len(types2), 3)  # Standard, large, oversized
        self.assertEqual(types2[0], ParkingSpaceType.STANDARD)
    
    def test_can_use_space(self):
        """Test can_use_space method."""
        # Regular vehicle
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        space = ParkingSpace("S-001", ParkingSpaceType.STANDARD)
        self.assertTrue(vehicle.can_use_space(space))
        
        # Handicap vehicle with handicap space
        handicap_vehicle = Vehicle("HV-001", VehicleType.STANDARD, is_handicap_permitted=True)
        handicap_space = ParkingSpace("HS-001", ParkingSpaceType.STANDARD, is_handicap=True)
        self.assertTrue(handicap_vehicle.can_use_space(handicap_space))
        
        # Non-handicap vehicle cannot use handicap space
        regular_vehicle = Vehicle("RV-001", VehicleType.STANDARD)
        self.assertFalse(regular_vehicle.can_use_space(handicap_space))
        
        # EV vehicle needs EV charger
        ev_vehicle = Vehicle("EV-001", VehicleType.STANDARD, needs_ev_charging=True)
        regular_space = ParkingSpace("RS-001", ParkingSpaceType.STANDARD)
        self.assertFalse(ev_vehicle.can_use_space(regular_space))


class TestParkingLot(unittest.TestCase):
    """Test ParkingLot class."""
    
    def setUp(self):
        """Create a test parking lot."""
        self.lot = ParkingLot(
            lot_id="LOT-001",
            name="Test Parking Lot",
            levels=2,
            rows_per_level=5,
            columns_per_row=10
        )
    
    def test_lot_creation(self):
        """Test parking lot creation."""
        self.assertEqual(self.lot.lot_id, "LOT-001")
        self.assertEqual(self.lot.name, "Test Parking Lot")
        self.assertEqual(self.lot.levels, 2)
        self.assertTrue(len(self.lot.spaces) > 0)
    
    def test_get_available_spaces(self):
        """Test get_available_spaces method."""
        available = self.lot.get_available_spaces()
        self.assertTrue(len(available) > 0)
        for space in available:
            self.assertEqual(space.status, ParkingStatus.AVAILABLE)
    
    def test_get_available_spaces_for_vehicle(self):
        """Test get_available_spaces_for_vehicle method."""
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        spaces = self.lot.get_available_spaces_for_vehicle(vehicle)
        self.assertTrue(len(spaces) > 0)
    
    def test_find_best_space(self):
        """Test find_best_space method."""
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        
        # Closest strategy
        space = self.lot.find_best_space(vehicle, "closest")
        self.assertIsNotNone(space)
        
        # Smallest strategy
        space2 = self.lot.find_best_space(vehicle, "smallest")
        self.assertIsNotNone(space2)
        
        # Largest strategy
        space3 = self.lot.find_best_space(vehicle, "largest")
        self.assertIsNotNone(space3)
    
    def test_park_vehicle(self):
        """Test park_vehicle method."""
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        entry_time = datetime.now()
        
        space_id = self.lot.park_vehicle(vehicle, entry_time)
        self.assertIsNotNone(space_id)
        
        # Verify space is occupied
        space = self.lot.spaces[space_id]
        self.assertEqual(space.status, ParkingStatus.OCCUPIED)
        self.assertEqual(space.vehicle_id, "V-001")
    
    def test_unpark_vehicle(self):
        """Test unpark_vehicle method."""
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        entry_time = datetime.now()
        
        space_id = self.lot.park_vehicle(vehicle, entry_time)
        result = self.lot.unpark_vehicle("V-001")
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "V-001")
        
        # Verify space is available again
        space = self.lot.spaces[space_id]
        self.assertEqual(space.status, ParkingStatus.AVAILABLE)
    
    def test_get_space_by_vehicle(self):
        """Test get_space_by_vehicle method."""
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        entry_time = datetime.now()
        
        space_id = self.lot.park_vehicle(vehicle, entry_time)
        found_space = self.lot.get_space_by_vehicle("V-001")
        
        self.assertIsNotNone(found_space)
        self.assertEqual(found_space.space_id, space_id)
    
    def test_occupancy_stats(self):
        """Test get_occupancy_stats method."""
        stats = self.lot.get_occupancy_stats()
        
        self.assertIn("total_spaces", stats)
        self.assertIn("occupied", stats)
        self.assertIn("available", stats)
        self.assertIn("occupancy_rate", stats)
        
        self.assertEqual(stats["occupied"], 0)
        self.assertEqual(stats["occupancy_rate"], 0)
    
    def test_space_type_stats(self):
        """Test get_space_type_stats method."""
        stats = self.lot.get_space_type_stats()
        
        self.assertIn(ParkingSpaceType.STANDARD, stats)
        self.assertIn("total", stats[ParkingSpaceType.STANDARD])
        self.assertIn("occupancy_rate", stats[ParkingSpaceType.STANDARD])
    
    def test_reserve_space(self):
        """Test reserve_space method."""
        available_space = self.lot.get_available_spaces()[0]
        until = datetime.now() + timedelta(hours=2)
        
        result = self.lot.reserve_space(available_space.space_id, until)
        self.assertTrue(result)
        
        space = self.lot.spaces[available_space.space_id]
        self.assertEqual(space.status, ParkingStatus.RESERVED)
    
    def test_maintenance_operations(self):
        """Test maintenance operations."""
        available_space = self.lot.get_available_spaces()[0]
        
        result = self.lot.set_maintenance(available_space.space_id)
        self.assertTrue(result)
        
        space = self.lot.spaces[available_space.space_id]
        self.assertEqual(space.status, ParkingStatus.MAINTENANCE)
        
        result2 = self.lot.end_maintenance(available_space.space_id)
        self.assertTrue(result2)
        self.assertEqual(space.status, ParkingStatus.AVAILABLE)
    
    def test_calculate_parking_fee(self):
        """Test calculate_parking_fee method."""
        entry = datetime(2024, 1, 1, 10, 0)
        exit = datetime(2024, 1, 1, 12, 0)  # 2 hours
        
        fee = self.lot.calculate_parking_fee(
            entry, exit, VehicleType.STANDARD, ParkingSpaceType.STANDARD
        )
        self.assertTrue(fee > 0)
        
        # Handicap discount
        fee_handicap = self.lot.calculate_parking_fee(
            entry, exit, VehicleType.STANDARD, ParkingSpaceType.STANDARD, is_handicap=True
        )
        self.assertEqual(fee_handicap, fee * 0.5)
    
    def test_to_dict(self):
        """Test to_dict method."""
        data = self.lot.to_dict()
        self.assertEqual(data["lot_id"], "LOT-001")
        self.assertEqual(data["name"], "Test Parking Lot")
        self.assertIn("occupancy_stats", data)


class TestParkingTransaction(unittest.TestCase):
    """Test ParkingTransaction class."""
    
    def test_transaction_creation(self):
        """Test transaction creation."""
        space = ParkingSpace("S-001", ParkingSpaceType.STANDARD)
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        entry_time = datetime.now()
        
        transaction = ParkingTransaction(
            transaction_id="TX-001",
            vehicle=vehicle,
            space=space,
            entry_time=entry_time
        )
        
        self.assertEqual(transaction.transaction_id, "TX-001")
        self.assertTrue(transaction.is_active)
        self.assertIsNone(transaction.fee)
    
    def test_complete_transaction(self):
        """Test complete method."""
        space = ParkingSpace("S-001", ParkingSpaceType.STANDARD)
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        entry_time = datetime.now()
        
        transaction = ParkingTransaction(
            transaction_id="TX-001",
            vehicle=vehicle,
            space=space,
            entry_time=entry_time
        )
        
        exit_time = entry_time + timedelta(hours=2)
        transaction.complete(exit_time, 10.0)
        
        self.assertFalse(transaction.is_active)
        self.assertEqual(transaction.fee, 10.0)
        self.assertEqual(transaction.exit_time, exit_time)
    
    def test_get_duration_hours(self):
        """Test get_duration_hours method."""
        space = ParkingSpace("S-001", ParkingSpaceType.STANDARD)
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        entry_time = datetime.now()
        
        transaction = ParkingTransaction(
            transaction_id="TX-001",
            vehicle=vehicle,
            space=space,
            entry_time=entry_time
        )
        
        exit_time = entry_time + timedelta(hours=3)
        transaction.exit_time = exit_time
        
        duration = transaction.get_duration_hours()
        self.assertEqual(duration, 3.0)
    
    def test_to_dict(self):
        """Test to_dict method."""
        space = ParkingSpace("S-001", ParkingSpaceType.STANDARD)
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        entry_time = datetime.now()
        
        transaction = ParkingTransaction(
            transaction_id="TX-001",
            vehicle=vehicle,
            space=space,
            entry_time=entry_time
        )
        
        data = transaction.to_dict()
        self.assertEqual(data["transaction_id"], "TX-001")
        self.assertEqual(data["vehicle_id"], "V-001")
        self.assertTrue(data["is_active"])


class TestParkingManager(unittest.TestCase):
    """Test ParkingManager class."""
    
    def setUp(self):
        """Create test manager and lot."""
        self.manager = ParkingManager()
        self.lot = ParkingLot("LOT-001", "Test Lot", levels=1, rows_per_level=5, columns_per_row=10)
        self.manager.add_lot(self.lot)
    
    def test_add_remove_lot(self):
        """Test add and remove lot."""
        self.assertEqual(len(self.manager.lots), 1)
        
        lot2 = ParkingLot("LOT-002", "Second Lot")
        self.manager.add_lot(lot2)
        self.assertEqual(len(self.manager.lots), 2)
        
        result = self.manager.remove_lot("LOT-002")
        self.assertTrue(result)
        self.assertEqual(len(self.manager.lots), 1)
    
    def test_register_vehicle(self):
        """Test register_vehicle method."""
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        self.manager.register_vehicle(vehicle)
        
        self.assertEqual(len(self.manager.vehicles), 1)
        self.assertIn("V-001", self.manager.vehicles)
        
        result = self.manager.unregister_vehicle("V-001")
        self.assertTrue(result)
        self.assertEqual(len(self.manager.vehicles), 0)
    
    def test_park_unpark_flow(self):
        """Test complete park/unpark flow."""
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        self.manager.register_vehicle(vehicle)
        
        # Use specific times to avoid overnight fee issues
        entry_time = datetime(2024, 1, 1, 10, 0)  # 10 AM
        transaction_id = self.manager.park_vehicle("LOT-001", "V-001", entry_time)
        
        self.assertIsNotNone(transaction_id)
        self.assertIn("V-001", self.manager.active_transactions)
        
        # Get location
        location = self.manager.get_vehicle_location("V-001")
        self.assertIsNotNone(location)
        
        # Unpark
        exit_time = entry_time + timedelta(hours=2)  # 12 PM
        result = self.manager.unpark_vehicle("V-001", exit_time)
        
        self.assertIsNotNone(result)
        # Fee should be 2 hours * 3.0 rate = 6.0
        self.assertEqual(result.fee, 6.0)
        self.assertNotIn("V-001", self.manager.active_transactions)
    
    def test_double_park_prevention(self):
        """Test that double parking is prevented."""
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        self.manager.register_vehicle(vehicle)
        
        entry_time = datetime.now()
        tid1 = self.manager.park_vehicle("LOT-001", "V-001", entry_time)
        
        # Try to park again
        tid2 = self.manager.park_vehicle("LOT-001", "V-001", entry_time + timedelta(minutes=30))
        
        self.assertIsNotNone(tid1)
        self.assertIsNone(tid2)
    
    def test_get_lot_availability(self):
        """Test get_lot_availability method."""
        availability = self.manager.get_lot_availability("LOT-001")
        
        self.assertIsNotNone(availability)
        self.assertEqual(availability["lot_id"], "LOT-001")
        self.assertIn("occupancy_stats", availability)
        self.assertIn("space_type_stats", availability)
    
    def test_find_available_lot(self):
        """Test find_available_lot_for_vehicle method."""
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        lot_id = self.manager.find_available_lot_for_vehicle(vehicle)
        
        self.assertIsNotNone(lot_id)
        self.assertEqual(lot_id, "LOT-001")
    
    def test_revenue_stats(self):
        """Test get_revenue_stats method."""
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        self.manager.register_vehicle(vehicle)
        
        # Use specific times to avoid overnight fee issues
        entry_time = datetime(2024, 1, 1, 10, 0)
        self.manager.park_vehicle("LOT-001", "V-001", entry_time)
        
        exit_time = entry_time + timedelta(hours=2)
        self.manager.unpark_vehicle("V-001", exit_time)
        
        stats = self.manager.get_revenue_stats()
        
        self.assertEqual(stats["total_transactions"], 1)
        self.assertTrue(stats["total_revenue"] > 0)
        self.assertEqual(stats["active_transactions"], 0)
    
    def test_all_occupancy(self):
        """Test get_all_occupancy method."""
        occupancy = self.manager.get_all_occupancy()
        
        self.assertIn("LOT-001", occupancy)
        self.assertEqual(occupancy["LOT-001"]["total_spaces"], len(self.lot.spaces))


class TestPricingFunctions(unittest.TestCase):
    """Test pricing calculation functions."""
    
    def test_hourly_fee(self):
        """Test calculate_hourly_parking_fee."""
        fee = calculate_hourly_parking_fee(2, 5.0)
        self.assertEqual(fee, 10.0)
        
        # With daily max
        fee2 = calculate_hourly_parking_fee(5, 5.0, daily_max=20.0)
        self.assertEqual(fee2, 20.0)  # Capped at daily max
        
        # Handicap discount
        fee3 = calculate_hourly_parking_fee(2, 5.0, is_handicap=True)
        self.assertEqual(fee3, 5.0)
    
    def test_tiered_fee(self):
        """Test calculate_tiered_parking_fee."""
        tiers = [(1, 0), (3, 5), (24, 3)]
        
        # First hour free
        fee1 = calculate_tiered_parking_fee(0.5, tiers)
        self.assertEqual(fee1, 0.0)
        
        # 2 hours: first free, second at $5
        fee2 = calculate_tiered_parking_fee(2, tiers)
        self.assertEqual(fee2, 5.0)
        
        # 10 hours: first free, 2 hours at $5 (10), 7 hours at $3 (21)
        fee3 = calculate_tiered_parking_fee(10, tiers)
        self.assertEqual(fee3, 10 + 21)
    
    def test_flat_rate_fee(self):
        """Test calculate_flat_rate_fee."""
        fee = calculate_flat_rate_fee(15.0)
        self.assertEqual(fee, 15.0)
        
        fee_handicap = calculate_flat_rate_fee(15.0, is_handicap=True)
        self.assertEqual(fee_handicap, 7.5)
    
    def test_free_first_hour_fee(self):
        """Test calculate_free_first_hour_fee."""
        # Under 1 hour
        fee1 = calculate_free_first_hour_fee(0.5, 5.0)
        self.assertEqual(fee1, 0.0)
        
        # Over 1 hour
        fee2 = calculate_free_first_hour_fee(3, 5.0)
        self.assertEqual(fee2, 10.0)  # 2 hours at $5


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_format_duration(self):
        """Test format_duration."""
        self.assertEqual(format_duration(0.5), "30 minutes")
        self.assertEqual(format_duration(2), "2 hours")
        self.assertEqual(format_duration(24), "1 days")
        self.assertEqual(format_duration(26), "1 days, 2 hours")
    
    def test_estimate_parking_duration(self):
        """Test estimate_parking_duration."""
        entry = datetime.now()
        exit = entry + timedelta(hours=3)
        
        duration = estimate_parking_duration(entry, exit)
        self.assertEqual(duration, 3.0)
        
        # Default
        duration2 = estimate_parking_duration(entry)
        self.assertEqual(duration2, 2.0)
    
    def test_optimization_score(self):
        """Test find_parking_optimization_score."""
        space = ParkingSpace("S-001", ParkingSpaceType.STANDARD, level=0, row=5, column=10)
        vehicle = Vehicle("V-001", VehicleType.STANDARD)
        
        score = find_parking_optimization_score(
            space, vehicle, (0, 0, 0),
            weight_distance=0.5, weight_size=0.3, weight_features=0.2
        )
        
        self.assertTrue(score >= 0)
        self.assertTrue(score <= 1)
    
    def test_generate_parking_report(self):
        """Test generate_parking_report."""
        manager = ParkingManager()
        lot = ParkingLot("LOT-001", "Test Lot")
        manager.add_lot(lot)
        
        report = generate_parking_report(manager)
        
        self.assertIn("timestamp", report)
        self.assertEqual(report["total_lots"], 1)
        self.assertIn("revenue_stats", report)
    
    def test_simulate_parking_scenario(self):
        """Test simulate_parking_scenario."""
        lot = ParkingLot("LOT-001", "Test Lot", levels=1, rows_per_level=10, columns_per_row=20)
        
        result = simulate_parking_scenario(lot, vehicle_count=10)
        
        self.assertEqual(result["total_vehicles"], 10)
        self.assertTrue(result["successful_parks"] >= 0)
        self.assertTrue(result["success_rate"] >= 0)
        self.assertIn("total_revenue", result)


class TestValidationFunctions(unittest.TestCase):
    """Test validation functions."""
    
    def test_validate_vehicle_id(self):
        """Test validate_vehicle_id."""
        self.assertTrue(validate_vehicle_id("ABC123"))
        self.assertTrue(validate_vehicle_id("VEH-001"))
        self.assertFalse(validate_vehicle_id(""))
        self.assertFalse(validate_vehicle_id("AB"))
        self.assertFalse(validate_vehicle_id("A" * 51))
        self.assertFalse(validate_vehicle_id("ABC@123"))
    
    def test_validate_space_id(self):
        """Test validate_space_id."""
        self.assertTrue(validate_space_id("S-001"))
        self.assertTrue(validate_space_id("LOT001S01"))
        self.assertFalse(validate_space_id(""))
        self.assertFalse(validate_space_id("S" * 21))
    
    def test_validate_pricing_config(self):
        """Test validate_pricing_config."""
        valid_config = {
            "hourly": {"standard": 5.0},
            "daily_max": 25.0
        }
        self.assertTrue(validate_pricing_config(valid_config))
        
        self.assertFalse(validate_pricing_config("invalid"))
        self.assertFalse(validate_pricing_config([]))
    
    def test_check_parking_capacity(self):
        """Test check_parking_capacity."""
        lot = ParkingLot("LOT-001", "Test Lot", levels=1, rows_per_level=5, columns_per_row=10)
        
        capacity = check_parking_capacity(lot, VehicleType.STANDARD)
        self.assertTrue(capacity > 0)
        
        capacity2 = check_parking_capacity(lot, VehicleType.MOTORCYCLE)
        self.assertTrue(capacity2 >= capacity)
    
    def test_estimate_wait_time(self):
        """Test estimate_wait_time."""
        lot = ParkingLot("LOT-001", "Test Lot", levels=1, rows_per_level=5, columns_per_row=10)
        
        wait = estimate_wait_time(lot, VehicleType.STANDARD, 0)
        self.assertEqual(wait, 0.0)  # Available spaces


class TestConstants(unittest.TestCase):
    """Test constants and mappings."""
    
    def test_vehicle_space_requirements(self):
        """Test VEHICLE_SPACE_REQUIREMENTS mapping."""
        self.assertEqual(
            VEHICLE_SPACE_REQUIREMENTS[VehicleType.MOTORCYCLE],
            ParkingSpaceType.MOTORCYCLE
        )
        self.assertEqual(
            VEHICLE_SPACE_REQUIREMENTS[VehicleType.STANDARD],
            ParkingSpaceType.STANDARD
        )
    
    def test_space_hierarchy(self):
        """Test SPACE_HIERARCHY ordering."""
        # Motorcycle is smallest
        self.assertEqual(SPACE_HIERARCHY[0], ParkingSpaceType.MOTORCYCLE)
        # Oversized is largest
        self.assertEqual(SPACE_HIERARCHY[-1], ParkingSpaceType.OVERSIZED)
    
    def test_version(self):
        """Test module version."""
        self.assertEqual(PARKING_UTILS_VERSION, "1.0.0")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_full_lot(self):
        """Test behavior when lot is full."""
        lot = ParkingLot("LOT-001", "Small Lot", levels=1, rows_per_level=1, columns_per_row=3)
        
        # Fill the lot
        vehicles = []
        entry_time = datetime.now()
        for i in range(20):  # More than available
            vehicle = Vehicle(f"V-{i}", VehicleType.MOTORCYCLE)
            lot.park_vehicle(vehicle, entry_time)
            vehicles.append(vehicle)
        
        # Check occupancy
        stats = lot.get_occupancy_stats()
        self.assertTrue(stats["occupancy_rate"] > 0)
    
    def test_invalid_lot_id(self):
        """Test behavior with invalid lot ID."""
        manager = ParkingManager()
        
        result = manager.park_vehicle("INVALID", "V-001", datetime.now())
        self.assertIsNone(result)
        
        availability = manager.get_lot_availability("INVALID")
        self.assertIsNone(availability)
    
    def test_invalid_vehicle_id(self):
        """Test behavior with invalid vehicle ID."""
        manager = ParkingManager()
        lot = ParkingLot("LOT-001", "Test Lot")
        manager.add_lot(lot)
        
        result = manager.park_vehicle("LOT-001", "INVALID_VEHICLE", datetime.now())
        self.assertIsNone(result)
        
        location = manager.get_vehicle_location("INVALID_VEHICLE")
        self.assertIsNone(location)
    
    def test_unpark_nonexistent(self):
        """Test unparking nonexistent vehicle."""
        manager = ParkingManager()
        lot = ParkingLot("LOT-001", "Test Lot")
        manager.add_lot(lot)
        
        result = manager.unpark_vehicle("NONEXISTENT", datetime.now())
        self.assertIsNone(result)


if __name__ == "__main__":
    # Run all tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed!")
        sys.exit(1)