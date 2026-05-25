% USAGE_EXAMPLES - Comprehensive Examples for unit_converter_utils
% Demonstrates all conversion categories with practical use cases
%
% Author: AllToolkit Auto-Generated
% Date: 2026-05-25

%% ===== EXAMPLE 1: Length Conversions =====
fprintf('\n=== Length Conversion Examples ===\n\n');

% Convert 100 km to miles
distance_km = 100;
distance_miles = unit_converter_utils(distance_km, 'km', 'miles', 'length');
fprintf('%.1f km = %.2f miles\n', distance_km, distance_miles);

% Convert height from feet/inches to centimeters
height_ft = 5;
height_in = 11;
height_cm = unit_converter_utils(height_ft * 12 + height_in, 'in', 'cm', 'length');
fprintf('Height: %d ft %d in = %.1f cm\n', height_ft, height_in, height_cm);

% Marathon distance
marathon_miles = unit_converter_utils(42.195, 'km', 'miles', 'length');
fprintf('Marathon: 42.195 km = %.2f miles\n', marathon_miles);

% Nautical miles to kilometers
nautical_distance = unit_converter_utils(100, 'nm', 'km', 'length');
fprintf('100 nautical miles = %.2f km\n', nautical_distance);

%% ===== EXAMPLE 2: Weight Conversions =====
fprintf('\n=== Weight Conversion Examples ===\n\n');

% Convert pounds to kilograms
weight_lb = 165;
weight_kg = unit_converter_utils(weight_lb, 'lb', 'kg', 'weight');
fprintf('%.0f lb = %.2f kg\n', weight_lb, weight_kg);

% Recipe: ounces to grams
flour_oz = 8;
flour_g = unit_converter_utils(flour_oz, 'oz', 'g', 'weight');
fprintf('%.0f oz flour = %.1f g\n', flour_oz, flour_g);

% Vehicle weight: tons to kg
vehicle_weight = unit_converter_utils(2.5, 'tons', 'kg', 'weight');
fprintf('Vehicle: 2.5 short tons = %.1f kg\n', vehicle_weight);

% Metric vs Imperial ton
metric_ton = unit_converter_utils(1, 'tonne', 'lb', 'weight');
fprintf('1 metric tonne = %.2f lb\n', metric_ton);

%% ===== EXAMPLE 3: Temperature Conversions =====
fprintf('\n=== Temperature Conversion Examples ===\n\n');

% Room temperature
temp_c = 22;
temp_f = unit_converter_utils(temp_c, 'celsius', 'fahrenheit', 'temperature');
fprintf('Room temp: %d°C = %.1f°F\n', temp_c, temp_f);

% Body temperature
body_temp_f = unit_converter_utils(37, 'c', 'f', 'temperature');
fprintf('Body temp: 37°C = %.1f°F\n', body_temp_f);

% Freezing and boiling points
fprintf('Water freezes at: %.1f°F\n', unit_converter_utils(0, 'c', 'f', 'temperature'));
fprintf('Water boils at: %.1f°F\n', unit_converter_utils(100, 'c', 'f', 'temperature'));

% Absolute zero in different scales
fprintf('Absolute zero: 0 K = %.2f°C = %.2f°F\n', ...
    unit_converter_utils(0, 'k', 'c', 'temperature'), ...
    unit_converter_utils(0, 'k', 'f', 'temperature'));

% Oven temperatures
oven_temp_c = [150, 180, 200, 220, 250];
fprintf('\nOven temperatures:\n');
for i = 1:length(oven_temp_c)
    fprintf('  %d°C = %.0f°F\n', oven_temp_c(i), ...
        unit_converter_utils(oven_temp_c(i), 'c', 'f', 'temperature'));
end

%% ===== EXAMPLE 4: Area Conversions =====
fprintf('\n=== Area Conversion Examples ===\n\n');

% Property size
acres = 0.5;
sq_meters = unit_converter_utils(acres, 'acre', 'm2', 'area');
sq_ft = unit_converter_utils(acres, 'acre', 'ft2', 'area');
fprintf('%.1f acre = %.0f m² = %.0f ft²\n', acres, sq_meters, sq_ft);

% Country size comparison
country_sq_km = 9596961;  % China area
country_sq_miles = unit_converter_utils(country_sq_km, 'km2', 'sqm', 'area') / 1e6;
fprintf('China area: %.0f km² ≈ %.0f million sq miles\n', country_sq_km, country_sq_miles * 1e6 / 2589988.110336);

% Hectares to acres
farm_ha = 100;
farm_acres = unit_converter_utils(farm_ha, 'ha', 'acre', 'area');
fprintf('Farm: %d hectares = %.2f acres\n', farm_ha, farm_acres);

% Room area
room_sqft = 200;
room_sqm = unit_converter_utils(room_sqft, 'ft2', 'm2', 'area');
fprintf('Room: %d ft² = %.2f m²\n', room_sqft, room_sqm);

%% ===== EXAMPLE 5: Volume Conversions =====
fprintf('\n=== Volume Conversion Examples ===\n\n');

% Fuel tank
tank_gal = 15;
tank_liters = unit_converter_utils(tank_gal, 'gal', 'l', 'volume');
fprintf('Fuel tank: %d gal = %.2f L\n', tank_gal, tank_liters);

% Swimming pool
pool_m3 = 50;
pool_liters = unit_converter_utils(pool_m3, 'm3', 'l', 'volume');
pool_gallons = unit_converter_utils(pool_m3, 'm3', 'gal', 'volume');
fprintf('Pool: %.0f m³ = %.0f L = %.0f gal\n', pool_m3, pool_liters, pool_gallons);

% Cooking measurements
fprintf('\nCooking conversions:\n');
fprintf('1 cup = %.0f mL\n', unit_converter_utils(1, 'cup', 'ml', 'volume'));
fprintf('1 tbsp = %.2f mL\n', unit_converter_utils(1, 'tbsp', 'ml', 'volume'));
fprintf('1 tsp = %.2f mL\n', unit_converter_utils(1, 'tsp', 'ml', 'volume'));
fprintf('1 fl oz = %.2f mL\n', unit_converter_utils(1, 'fl_oz', 'ml', 'volume'));

% Engine displacement
engine_cc = 2000;
engine_liters = unit_converter_utils(engine_cc, 'cm3', 'l', 'volume');
fprintf('\nEngine: %.0f cc = %.1f L\n', engine_cc, engine_liters);

%% ===== EXAMPLE 6: Pressure Conversions =====
fprintf('\n=== Pressure Conversion Examples ===\n\n');

% Tire pressure
tire_psi = 32;
tire_kpa = unit_converter_utils(tire_psi, 'psi', 'kpa', 'pressure');
tire_bar = unit_converter_utils(tire_psi, 'psi', 'bar', 'pressure');
fprintf('Tire pressure: %d psi = %.1f kPa = %.2f bar\n', tire_psi, tire_kpa, tire_bar);

% Atmospheric pressure
fprintf('Standard atmospheric pressure:\n');
fprintf('  1 atm = %.0f Pa = %.3f kPa\n', ...
    unit_converter_utils(1, 'atm', 'pa', 'pressure'), ...
    unit_converter_utils(1, 'atm', 'kpa', 'pressure'));
fprintf('  1 atm = %.2f bar\n', unit_converter_utils(1, 'atm', 'bar', 'pressure'));
fprintf('  1 atm = %.2f psi\n', unit_converter_utils(1, 'atm', 'psi', 'pressure'));

% Blood pressure (mmHg)
bp_systolic = 120;
bp_kpa = unit_converter_utils(bp_systolic, 'mmhg', 'kpa', 'pressure');
fprintf('\nBlood pressure: %d mmHg = %.2f kPa\n', bp_systolic, bp_kpa);

% Deep sea pressure
depth_m = 100;
pressure_atm = depth_m * 0.1019;  % Rough approximation
pressure_psi = unit_converter_utils(pressure_atm, 'atm', 'psi', 'pressure');
fprintf('At %d m depth: ~%.1f atm ≈ %.1f psi\n', depth_m, pressure_atm, pressure_psi);

%% ===== EXAMPLE 7: Speed Conversions =====
fprintf('\n=== Speed Conversion Examples ===\n\n');

% Highway speed limits
fprintf('Highway speed limits:\n');
fprintf('  100 km/h = %.1f mph\n', unit_converter_utils(100, 'kmph', 'mph', 'speed'));
fprintf('  65 mph = %.1f km/h\n', unit_converter_utils(65, 'mph', 'kmph', 'speed'));

% Speed of sound
fprintf('\nSpeed of sound (Mach 1):\n');
fprintf('  %.0f m/s\n', unit_converter_utils(1, 'mach', 'mps', 'speed'));
fprintf('  %.1f km/h\n', unit_converter_utils(1, 'mach', 'kmph', 'speed'));
fprintf('  %.1f mph\n', unit_converter_utils(1, 'mach', 'mph', 'speed'));

% Aircraft speed
aircraft_mach = 0.85;
aircraft_kmph = unit_converter_utils(aircraft_mach, 'mach', 'kmph', 'speed');
fprintf('Cruising at Mach %.2f = %.0f km/h\n', aircraft_mach, aircraft_kmph);

% Knots for navigation
ship_knots = 20;
ship_kmph = unit_converter_utils(ship_knots, 'knots', 'kmph', 'speed');
fprintf('Ship speed: %d knots = %.1f km/h\n', ship_knots, ship_kmph);

% Speed of light
fprintf('\nSpeed of light:\n');
fprintf('  c = %.0f m/s\n', unit_converter_utils(1, 'c', 'mps', 'speed'));
fprintf('  c = %.0f km/h\n', unit_converter_utils(1, 'c', 'kmph', 'speed'));

%% ===== EXAMPLE 8: Time Conversions =====
fprintf('\n=== Time Conversion Examples ===\n\n');

% Age calculations
age_years = 30;
age_days = unit_converter_utils(age_years, 'years', 'days', 'time');
age_hours = unit_converter_utils(age_years, 'years', 'h', 'time');
fprintf('Age: %d years = %.0f days = %.0f hours\n', age_years, age_days, age_hours);

% Project duration
project_hours = 2000;
project_weeks = unit_converter_utils(project_hours, 'h', 'weeks', 'time');
project_months = unit_converter_utils(project_hours, 'h', 'months', 'time');
fprintf('Project: %d hours = %.1f weeks = %.1f months\n', project_hours, project_weeks, project_months);

% Computing time scales
fprintf('\nComputing time scales:\n');
fprintf('1 ms = %.0f μs = %.0f ns\n', ...
    unit_converter_utils(1, 'ms', 'us', 'time'), ...
    unit_converter_utils(1, 'ms', 'ns', 'time'));
fprintf('1 second = %.0f ms = %.0f μs\n', ...
    unit_converter_utils(1, 's', 'ms', 'time'), ...
    unit_converter_utils(1, 's', 'us', 'time'));

% Century breakdown
century_days = unit_converter_utils(1, 'century', 'days', 'time');
fprintf('1 century ≈ %.0f days\n', century_days);

%% ===== EXAMPLE 9: Data Conversions =====
fprintf('\n=== Data Conversion Examples ===\n\n');

% File sizes
file_mb = 150;
file_kb = unit_converter_utils(file_mb, 'mb', 'kb', 'data');
file_gb = unit_converter_utils(file_mb, 'mb', 'gb', 'data');
fprintf('File: %d MB = %.0f KB = %.2f GB\n', file_mb, file_kb, file_gb);

% Storage capacities
fprintf('\nStorage conversions:\n');
fprintf('1 TB = %.0f GB = %.0f MB\n', ...
    unit_converter_utils(1, 'tb', 'gb', 'data'), ...
    unit_converter_utils(1, 'tb', 'mb', 'data'));
fprintf('1 PB = %.0f TB\n', unit_converter_utils(1, 'pb', 'tb', 'data'));

% Binary vs decimal (GiB vs GB)
fprintf('\nBinary vs Decimal:\n');
fprintf('1 GiB = %.2f GB\n', unit_converter_utils(1, 'gib', 'gb', 'data'));
fprintf('1 TiB = %.2f TB\n', unit_converter_utils(1, 'tib', 'tb', 'data'));

% Network speeds (bits to bytes)
download_mbps = 100;  % Megabits per second
download_mBs = unit_converter_utils(download_mbps, 'mbit', 'mb', 'data');
fprintf('\nNetwork: %d Mbps = %.2f MB/s theoretical max\n', download_mbps, download_mBs);

%% ===== EXAMPLE 10: Angle Conversions =====
fprintf('\n=== Angle Conversion Examples ===\n\n');

% Common angles
fprintf('Common angles:\n');
fprintf('45° = %.4f rad = %.0f grad\n', ...
    unit_converter_utils(45, 'deg', 'rad', 'angle'), ...
    unit_converter_utils(45, 'deg', 'grad', 'angle'));
fprintf('90° = %.4f rad = %.0f grad\n', ...
    unit_converter_utils(90, 'deg', 'rad', 'angle'), ...
    unit_converter_utils(90, 'deg', 'grad', 'angle'));

% Full circle
fprintf('360° = %.4f rad = %.0f grad = %.0f arcmin\n', ...
    unit_converter_utils(360, 'deg', 'rad', 'angle'), ...
    unit_converter_utils(360, 'deg', 'grad', 'angle'), ...
    unit_converter_utils(360, 'deg', 'arcmin', 'angle'));

% Small angles (astronomy/navigation)
fprintf('\nPrecision angles:\n');
angle_deg = 0.5;
fprintf('%.1f° = %.0f arcmin = %.0f arcsec\n', angle_deg, ...
    unit_converter_utils(angle_deg, 'deg', 'arcmin', 'angle'), ...
    unit_converter_utils(angle_deg, 'deg', 'arcsec', 'angle'));

% Pi values
fprintf('\nπ multiples:\n');
fprintf('π rad = %.0f°\n', unit_converter_utils(pi, 'rad', 'deg', 'angle'));
fprintf('2π rad = %.0f° = %.0f turns\n', ...
    unit_converter_utils(2*pi, 'rad', 'deg', 'angle'), ...
    unit_converter_utils(2*pi, 'rad', 'turn', 'angle'));

%% ===== PRACTICAL APPLICATION: Unit Converter GUI Helper =====
fprintf('\n=== Practical Application: Multi-step Conversion ===\n\n');

% Fuel efficiency comparison
fprintf('Fuel efficiency comparison:\n');
miles = 100;
km = unit_converter_utils(miles, 'miles', 'km', 'length');
gallons = 3;
liters = unit_converter_utils(gallons, 'gal', 'l', 'volume');

mpg = miles / gallons;  % miles per gallon
kml = km / liters;       % km per liter
lp100km = 100 / kml;    % liters per 100 km

fprintf('  %.0f miles / %.0f gallons = %.1f MPG\n', miles, gallons, mpg);
fprintf('  %.1f km / %.1f L = %.1f km/L\n', km, liters, kml);
fprintf('  Equivalent to %.1f L/100km\n', lp100km);

% Body Mass Index (BMI) with unit conversion
fprintf('\nBMI calculation with conversions:\n');
weight_lb = 165;
height_ft = 5;
height_in = 11;

weight_kg = unit_converter_utils(weight_lb, 'lb', 'kg', 'weight');
height_m = unit_converter_utils(height_ft * 12 + height_in, 'in', 'm', 'length');
bmi = weight_kg / height_m^2;

fprintf('  Weight: %.0f lb = %.2f kg\n', weight_lb, weight_kg);
fprintf('  Height: %d\'%d" = %.3f m\n', height_ft, height_in, height_m);
fprintf('  BMI: %.1f\n', bmi);

fprintf('\n=== All Examples Complete ===\n');