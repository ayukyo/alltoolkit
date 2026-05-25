% UNIT_CONVERTER_UTILS_TEST - Comprehensive test suite for unit_converter_utils
% Tests all conversion categories with various edge cases
%
% Run: unit_converter_utils_test
%
% Author: AllToolkit Auto-Generated
% Date: 2026-05-25

function unit_converter_utils_test()
    fprintf('========================================\n');
    fprintf('  Unit Converter Utils Test Suite\n');
    fprintf('========================================\n\n');
    
    passed = 0;
    failed = 0;
    total_tests = 0;
    
    % Run all test categories
    [p, f, t] = test_length_conversions();
    passed = passed + p; failed = failed + f; total_tests = total_tests + t;
    
    [p, f, t] = test_weight_conversions();
    passed = passed + p; failed = failed + f; total_tests = total_tests + t;
    
    [p, f, t] = test_temperature_conversions();
    passed = passed + p; failed = failed + f; total_tests = total_tests + t;
    
    [p, f, t] = test_area_conversions();
    passed = passed + p; failed = failed + f; total_tests = total_tests + t;
    
    [p, f, t] = test_volume_conversions();
    passed = passed + p; failed = failed + f; total_tests = total_tests + t;
    
    [p, f, t] = test_pressure_conversions();
    passed = passed + p; failed = failed + f; total_tests = total_tests + t;
    
    [p, f, t] = test_speed_conversions();
    passed = passed + p; failed = failed + f; total_tests = total_tests + t;
    
    [p, f, t] = test_time_conversions();
    passed = passed + p; failed = failed + f; total_tests = total_tests + t;
    
    [p, f, t] = test_data_conversions();
    passed = passed + p; failed = failed + f; total_tests = total_tests + t;
    
    [p, f, t] = test_angle_conversions();
    passed = passed + p; failed = failed + f; total_tests = total_tests + t;
    
    [p, f, t] = test_edge_cases();
    passed = passed + p; failed = failed + f; total_tests = total_tests + t;
    
    % Summary
    fprintf('\n========================================\n');
    fprintf('  Test Summary\n');
    fprintf('========================================\n');
    fprintf('Total Tests: %d\n', total_tests);
    fprintf('Passed: %d\n', passed);
    fprintf('Failed: %d\n', failed);
    
    if failed == 0
        fprintf('\n✓ ALL TESTS PASSED!\n');
    else
        fprintf('\n✗ Some tests failed.\n');
    end
end

%% LENGTH CONVERSION TESTS
function [passed, failed, total] = test_length_conversions()
    fprintf('--- Testing Length Conversions ---\n');
    passed = 0; failed = 0; total = 0;
    
    % Test meters to various units
    [p, f, t] = run_test(@() unit_converter_utils(1, 'm', 'm', 'length'), 1, 'm to m');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1000, 'm', 'km', 'length'), 1, 'm to km');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'km', 'm', 'length'), 1000, 'km to m');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test miles
    [p, f, t] = run_test(@() unit_converter_utils(1, 'mile', 'km', 'length'), 1.609344, 'mile to km');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test feet and inches
    [p, f, t] = run_test(@() unit_converter_utils(1, 'ft', 'in', 'length'), 12, 'ft to in');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'yd', 'ft', 'length'), 3, 'yd to ft');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test nautical miles
    [p, f, t] = run_test(@() unit_converter_utils(1, 'nm', 'km', 'length'), 1.852, 'nautical mile to km');
    passed = passed + p; failed = failed + f; total = total + t;
    
    fprintf('Length tests: %d passed, %d failed\n\n', passed, failed);
end

%% WEIGHT CONVERSION TESTS
function [passed, failed, total] = test_weight_conversions()
    fprintf('--- Testing Weight Conversions ---\n');
    passed = 0; failed = 0; total = 0;
    
    % Test kg to various units
    [p, f, t] = run_test(@() unit_converter_utils(1, 'kg', 'g', 'weight'), 1000, 'kg to g');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'kg', 'lb', 'weight'), 2.20462262185, 'kg to lb');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'lb', 'oz', 'weight'), 16, 'lb to oz');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test tonnes
    [p, f, t] = run_test(@() unit_converter_utils(1, 'tonne', 'kg', 'weight'), 1000, 'tonne to kg');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test short ton vs long ton
    [p, f, t] = run_test(@() unit_converter_utils(1, 'ton', 'kg', 'weight'), 907.18474, 'short ton to kg');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'long_ton', 'kg', 'weight'), 1016.0469088, 'long ton to kg');
    passed = passed + p; failed = failed + f; total = total + t;
    
    fprintf('Weight tests: %d passed, %d failed\n\n', passed, failed);
end

%% TEMPERATURE CONVERSION TESTS
function [passed, failed, total] = test_temperature_conversions()
    fprintf('--- Testing Temperature Conversions ---\n');
    passed = 0; failed = 0; total = 0;
    
    % Test Celsius to Fahrenheit
    [p, f, t] = run_test(@() unit_converter_utils(0, 'c', 'f', 'temperature'), 32, '0°C to °F');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(100, 'celsius', 'fahrenheit', 'temperature'), 212, '100°C to °F');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test Fahrenheit to Celsius
    [p, f, t] = run_test(@() unit_converter_utils(32, 'f', 'c', 'temperature'), 0, '32°F to °C');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test Celsius to Kelvin
    [p, f, t] = run_test(@() unit_converter_utils(0, 'c', 'k', 'temperature'), 273.15, '0°C to K');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test Kelvin to Celsius
    [p, f, t] = run_test(@() unit_converter_utils(273.15, 'k', 'c', 'temperature'), 0, '273.15K to °C');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test negative temperatures
    [p, f, t] = run_test(@() unit_converter_utils(-40, 'c', 'f', 'temperature'), -40, '-40°C to °F (should be same)');
    passed = passed + p; failed = failed + f; total = total + t;
    
    fprintf('Temperature tests: %d passed, %d failed\n\n', passed, failed);
end

%% AREA CONVERSION TESTS
function [passed, failed, total] = test_area_conversions()
    fprintf('--- Testing Area Conversions ---\n');
    passed = 0; failed = 0; total = 0;
    
    % Test m2 to various units
    [p, f, t] = run_test(@() unit_converter_utils(1, 'm2', 'cm2', 'area'), 10000, 'm2 to cm2');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'km2', 'm2', 'area'), 1e6, 'km2 to m2');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test hectares
    [p, f, t] = run_test(@() unit_converter_utils(1, 'ha', 'm2', 'area'), 10000, 'hectare to m2');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test acres
    [p, f, t] = run_test(@() unit_converter_utils(1, 'acre', 'm2', 'area'), 4046.8564224, 'acre to m2');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test square feet
    [p, f, t] = run_test(@() unit_converter_utils(1, 'ft2', 'in2', 'area'), 144, 'ft2 to in2');
    passed = passed + p; failed = failed + f; total = total + t;
    
    fprintf('Area tests: %d passed, %d failed\n\n', passed, failed);
end

%% VOLUME CONVERSION TESTS
function [passed, failed, total] = test_volume_conversions()
    fprintf('--- Testing Volume Conversions ---\n');
    passed = 0; failed = 0; total = 0;
    
    % Test liters
    [p, f, t] = run_test(@() unit_converter_utils(1, 'l', 'ml', 'volume'), 1000, 'L to mL');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'm3', 'l', 'volume'), 1000, 'm3 to L');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test gallons
    [p, f, t] = run_test(@() unit_converter_utils(1, 'gal', 'l', 'volume'), 3.785411784, 'gallon to L');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test quarts and pints
    [p, f, t] = run_test(@() unit_converter_utils(1, 'gal', 'qt', 'volume'), 4, 'gallon to quarts');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'qt', 'pt', 'volume'), 2, 'quart to pints');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test cooking units
    [p, f, t] = run_test(@() unit_converter_utils(1, 'cup', 'tbsp', 'volume'), 16, 'cup to tbsp');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'tbsp', 'tsp', 'volume'), 3, 'tbsp to tsp');
    passed = passed + p; failed = failed + f; total = total + t;
    
    fprintf('Volume tests: %d passed, %d failed\n\n', passed, failed);
end

%% PRESSURE CONVERSION TESTS
function [passed, failed, total] = test_pressure_conversions()
    fprintf('--- Testing Pressure Conversions ---\n');
    passed = 0; failed = 0; total = 0;
    
    % Test kPa
    [p, f, t] = run_test(@() unit_converter_utils(1, 'kpa', 'pa', 'pressure'), 1000, 'kPa to Pa');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test bar
    [p, f, t] = run_test(@() unit_converter_utils(1, 'bar', 'pa', 'pressure'), 1e5, 'bar to Pa');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test atm
    [p, f, t] = run_test(@() unit_converter_utils(1, 'atm', 'pa', 'pressure'), 101325, 'atm to Pa');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test psi
    [p, f, t] = run_test(@() unit_converter_utils(1, 'atm', 'psi', 'pressure'), 14.6959, 'atm to psi', 0.01);
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test mmHg
    [p, f, t] = run_test(@() unit_converter_utils(760, 'mmhg', 'atm', 'pressure'), 1, '760 mmHg to atm', 0.01);
    passed = passed + p; failed = failed + f; total = total + t;
    
    fprintf('Pressure tests: %d passed, %d failed\n\n', passed, failed);
end

%% SPEED CONVERSION TESTS
function [passed, failed, total] = test_speed_conversions()
    fprintf('--- Testing Speed Conversions ---\n');
    passed = 0; failed = 0; total = 0;
    
    % Test km/h to m/s
    [p, f, t] = run_test(@() unit_converter_utils(3.6, 'kmph', 'mps', 'speed'), 1, '3.6 km/h to m/s');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test mph
    [p, f, t] = run_test(@() unit_converter_utils(60, 'mph', 'kmph', 'speed'), 96.56064, '60 mph to km/h');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test knots
    [p, f, t] = run_test(@() unit_converter_utils(1, 'knot', 'kmph', 'speed'), 1.852, '1 knot to km/h');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test Mach
    [p, f, t] = run_test(@() unit_converter_utils(1, 'mach', 'mps', 'speed'), 340.29, 'Mach 1 to m/s');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test speed of light
    [p, f, t] = run_test(@() unit_converter_utils(1, 'c', 'mps', 'speed'), 299792458, 'speed of light to m/s');
    passed = passed + p; failed = failed + f; total = total + t;
    
    fprintf('Speed tests: %d passed, %d failed\n\n', passed, failed);
end

%% TIME CONVERSION TESTS
function [passed, failed, total] = test_time_conversions()
    fprintf('--- Testing Time Conversions ---\n');
    passed = 0; failed = 0; total = 0;
    
    % Test basic conversions
    [p, f, t] = run_test(@() unit_converter_utils(1, 'min', 's', 'time'), 60, 'min to s');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'h', 'min', 'time'), 60, 'hour to min');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'day', 'h', 'time'), 24, 'day to hours');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'week', 'day', 'time'), 7, 'week to days');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test milliseconds
    [p, f, t] = run_test(@() unit_converter_utils(1000, 'ms', 's', 'time'), 1, '1000 ms to s');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test nanoseconds
    [p, f, t] = run_test(@() unit_converter_utils(1e9, 'ns', 's', 'time'), 1, '1e9 ns to s');
    passed = passed + p; failed = failed + f; total = total + t;
    
    fprintf('Time tests: %d passed, %d failed\n\n', passed, failed);
end

%% DATA CONVERSION TESTS
function [passed, failed, total] = test_data_conversions()
    fprintf('--- Testing Data Conversions ---\n');
    passed = 0; failed = 0; total = 0;
    
    % Test bytes
    [p, f, t] = run_test(@() unit_converter_utils(1, 'kb', 'b', 'data'), 1000, 'KB to bytes');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test binary vs decimal
    [p, f, t] = run_test(@() unit_converter_utils(1, 'kib', 'b', 'data'), 1024, 'KiB to bytes');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'mib', 'kib', 'data'), 1024, 'MiB to KiB');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1024, 'mib', 'gib', 'data'), 1, '1024 MiB to GiB');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test bits
    [p, f, t] = run_test(@() unit_converter_utils(8, 'bit', 'b', 'data'), 1, '8 bits to byte');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'mbit', 'bit', 'data'), 1e6, '1 Mbit to bits');
    passed = passed + p; failed = failed + f; total = total + t;
    
    fprintf('Data tests: %d passed, %d failed\n\n', passed, failed);
end

%% ANGLE CONVERSION TESTS
function [passed, failed, total] = test_angle_conversions()
    fprintf('--- Testing Angle Conversions ---\n');
    passed = 0; failed = 0; total = 0;
    
    % Test degrees to radians
    [p, f, t] = run_test(@() unit_converter_utils(180, 'deg', 'rad', 'angle'), pi, '180° to rad');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(360, 'deg', 'rad', 'angle'), 2*pi, '360° to rad');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test radians to degrees
    [p, f, t] = run_test(@() unit_converter_utils(pi, 'rad', 'deg', 'angle'), 180, 'π rad to deg');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test gradians
    [p, f, t] = run_test(@() unit_converter_utils(400, 'grad', 'deg', 'angle'), 360, '400 grad to deg');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test arcminutes and arcseconds
    [p, f, t] = run_test(@() unit_converter_utils(1, 'deg', 'arcmin', 'angle'), 60, '1° to arcmin');
    passed = passed + p; failed = failed + f; total = total + t;
    
    [p, f, t] = run_test(@() unit_converter_utils(1, 'deg', 'arcsec', 'angle'), 3600, '1° to arcsec');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test turns
    [p, f, t] = run_test(@() unit_converter_utils(1, 'turn', 'deg', 'angle'), 360, '1 turn to deg');
    passed = passed + p; failed = failed + f; total = total + t;
    
    fprintf('Angle tests: %d passed, %d failed\n\n', passed, failed);
end

%% EDGE CASE TESTS
function [passed, failed, total] = test_edge_cases()
    fprintf('--- Testing Edge Cases ---\n');
    passed = 0; failed = 0; total = 0;
    
    % Test zero values
    [p, f, t] = run_test(@() unit_converter_utils(0, 'm', 'km', 'length'), 0, 'zero value');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test negative values
    [p, f, t] = run_test(@() unit_converter_utils(-100, 'kg', 'g', 'weight'), -100000, 'negative value');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test very large values
    [p, f, t] = run_test(@() unit_converter_utils(1e9, 'm', 'km', 'length'), 1e6, 'large value');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test very small values
    [p, f, t] = run_test(@() unit_converter_utils(1e-6, 'km', 'm', 'length'), 1e-3, 'small value');
    passed = passed + p; failed = failed + f; total = total + t;
    
    % Test same unit conversion
    [p, f, t] = run_test(@() unit_converter_utils(42, 'm', 'm', 'length'), 42, 'same unit');
    passed = passed + p; failed = failed + f; total = total + t;
    
    fprintf('Edge case tests: %d passed, %d failed\n\n', passed, failed);
end

%% HELPER FUNCTION
function [passed, failed, total] = run_test(test_func, expected, test_name, tolerance)
    if nargin < 4
        tolerance = 1e-6;
    end
    
    total = 1;
    passed = 0;
    failed = 0;
    
    try
        result = test_func();
        if abs(result - expected) <= tolerance * max(abs(expected), 1)
            fprintf('  ✓ %s: %.6g (expected: %.6g)\n', test_name, result, expected);
            passed = 1;
        else
            fprintf('  ✗ %s: %.6g (expected: %.6g)\n', test_name, result, expected);
            failed = 1;
        end
    catch ME
        fprintf('  ✗ %s: ERROR - %s\n', test_name, ME.message);
        failed = 1;
    end
end