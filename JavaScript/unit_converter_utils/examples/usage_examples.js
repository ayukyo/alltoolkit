/**
 * Unit Converter Utils - Usage Examples
 * 
 * This file demonstrates how to use the unit_converter_utils module.
 * Run with: node examples/usage_examples.js
 */

const {
  // Specific converters
  convertTemperature,
  convertLength,
  convertWeight,
  convertVolume,
  convertArea,
  convertSpeed,
  convertTime,
  convertData,
  convertPressure,
  convertAngle,
  convertFuel,
  
  // Generic converter
  convert,
  
  // Utilities
  getUnitCategory,
  getAvailableUnits,
  getCategories,
  canConvert,
  formatNumber,
} = require('../mod.js');

console.log('========================================');
console.log('  Unit Converter Utils - Examples');
console.log('========================================\n');

// ============================================================================
// Temperature Examples
// ============================================================================

console.log('--- Temperature ---');
console.log(`0°C to Fahrenheit: ${convertTemperature(0, 'celsius', 'fahrenheit')}°F`);
console.log(`100°C to Fahrenheit: ${convertTemperature(100, 'celsius', 'fahrenheit')}°F`);
console.log(`32°F to Celsius: ${convertTemperature(32, 'fahrenheit', 'celsius')}°C`);
console.log(`0°C to Kelvin: ${convertTemperature(0, 'celsius', 'kelvin')}K`);
console.log(`Absolute zero: ${convertTemperature(-273.15, 'celsius', 'kelvin')}K\n`);

// ============================================================================
// Length Examples
// ============================================================================

console.log('--- Length ---');
console.log(`1 meter to cm: ${convertLength(1, 'meter', 'centimeter')} cm`);
console.log(`1 km to miles: ${formatNumber(convertLength(1, 'kilometer', 'mile'))} miles`);
console.log(`1 mile to km: ${formatNumber(convertLength(1, 'mile', 'kilometer'))} km`);
console.log(`1 foot to inches: ${convertLength(1, 'foot', 'inch')} inches`);
console.log(`1 inch to cm: ${convertLength(1, 'inch', 'centimeter')} cm`);
console.log(`Marathon (26.2 miles) to km: ${formatNumber(convertLength(26.2, 'mile', 'kilometer'))} km\n`);

// ============================================================================
// Weight Examples
// ============================================================================

console.log('--- Weight ---');
console.log(`1 kg to pounds: ${formatNumber(convertWeight(1, 'kilogram', 'pound'))} lbs`);
console.log(`1 pound to kg: ${formatNumber(convertWeight(1, 'pound', 'kilogram'))} kg`);
console.log(`1 kg to grams: ${convertWeight(1, 'kilogram', 'gram')} g`);
console.log(`100 kg to stones: ${formatNumber(convertWeight(100, 'kilogram', 'stone'))} st`);
console.log(`1 metric ton to lbs: ${formatNumber(convertWeight(1, 'metric_ton', 'pound'))} lbs\n`);

// ============================================================================
// Volume Examples
// ============================================================================

console.log('--- Volume ---');
console.log(`1 liter to ml: ${convertVolume(1, 'liter', 'milliliter')} ml`);
console.log(`1 gallon (US) to liters: ${formatNumber(convertVolume(1, 'gallon_us', 'liter'))} L`);
console.log(`1 gallon (UK) to liters: ${formatNumber(convertVolume(1, 'gallon_uk', 'liter'))} L`);
console.log(`1 cup to tablespoons: ${convertVolume(1, 'cup_us', 'tablespoon')} tbsp`);
console.log(`1 cubic meter to liters: ${convertVolume(1, 'cubic_meter', 'liter')} L\n`);

// ============================================================================
// Area Examples
// ============================================================================

console.log('--- Area ---');
console.log(`1 square meter to sq ft: ${formatNumber(convertArea(1, 'square_meter', 'square_foot'))} ft²`);
console.log(`1 hectare to acres: ${formatNumber(convertArea(1, 'hectare', 'acre'))} acres`);
console.log(`1 acre to sq ft: ${convertArea(1, 'acre', 'square_foot')} ft²`);
console.log(`1 sq km to hectares: ${convertArea(1, 'square_kilometer', 'hectare')} ha\n`);

// ============================================================================
// Speed Examples
// ============================================================================

console.log('--- Speed ---');
console.log(`100 km/h to mph: ${formatNumber(convertSpeed(100, 'kilometers_per_hour', 'miles_per_hour'))} mph`);
console.log(`60 mph to km/h: ${formatNumber(convertSpeed(60, 'miles_per_hour', 'kilometers_per_hour'))} km/h`);
console.log(`1 m/s to km/h: ${convertSpeed(1, 'meters_per_second', 'kilometers_per_hour')} km/h`);
console.log(`Speed of sound (Mach 1) to km/h: ${formatNumber(convertSpeed(1, 'mach', 'kilometers_per_hour'))} km/h`);
console.log(`1 knot to km/h: ${formatNumber(convertSpeed(1, 'knot', 'kilometers_per_hour'))} km/h\n`);

// ============================================================================
// Time Examples
// ============================================================================

console.log('--- Time ---');
console.log(`1 hour to minutes: ${convertTime(1, 'hour', 'minute')} min`);
console.log(`1 day to seconds: ${convertTime(1, 'day', 'second')} sec`);
console.log(`1 year to days: ${formatNumber(convertTime(1, 'year', 'day'))} days`);
console.log(`1 century to years: ${formatNumber(convertTime(1, 'century', 'year'))} years`);
console.log(`86400 seconds to hours: ${convertTime(86400, 'second', 'hour')} hours\n`);

// ============================================================================
// Data Examples
// ============================================================================

console.log('--- Data ---');
console.log(`1 GiB to MiB: ${convertData(1, 'gibibyte', 'mebibyte')} MiB`);
console.log(`1 GB to MB: ${convertData(1, 'gigabyte', 'megabyte')} MB`);
console.log(`1 GiB to GB: ${formatNumber(convertData(1, 'gibibyte', 'gigabyte'))} GB`);
console.log(`1 MB to bytes: ${formatNumber(convertData(1, 'megabyte', 'byte'))} bytes`);
console.log(`100 Mbps to MB/s: ${convertData(100, 'megabit', 'megabyte')} MB/s\n`);

// ============================================================================
// Pressure Examples
// ============================================================================

console.log('--- Pressure ---');
console.log(`1 atm to psi: ${formatNumber(convertPressure(1, 'atmosphere', 'psi'))} psi`);
console.log(`1 bar to kPa: ${convertPressure(1, 'bar', 'kilopascal')} kPa`);
console.log(`1 atm to Pa: ${convertPressure(1, 'atmosphere', 'pascal')} Pa`);
console.log(`Tire pressure (32 psi) to kPa: ${formatNumber(convertPressure(32, 'psi', 'kilopascal'))} kPa\n`);

// ============================================================================
// Angle Examples
// ============================================================================

console.log('--- Angle ---');
console.log(`180° to radians: ${convertAngle(180, 'degree', 'radian')} rad (π)`);
console.log(`π rad to degrees: ${convertAngle(Math.PI, 'radian', 'degree')}°`);
console.log(`90° to gradians: ${convertAngle(90, 'degree', 'gradian')} gon`);
console.log(`1° to arcminutes: ${convertAngle(1, 'degree', 'arcminute')}'`);
console.log(`1° to arcseconds: ${convertAngle(1, 'degree', 'arcsecond')}"\n`);

// ============================================================================
// Fuel Consumption Examples
// ============================================================================

console.log('--- Fuel Consumption ---');
console.log(`10 km/L to L/100km: ${convertFuel(10, 'km_per_liter', 'liters_per_100km')} L/100km`);
console.log(`8 L/100km to km/L: ${formatNumber(convertFuel(8, 'liters_per_100km', 'km_per_liter'))} km/L`);
console.log(`30 MPG (US) to L/100km: ${formatNumber(convertFuel(30, 'mpg_us', 'liters_per_100km'))} L/100km`);
console.log(`30 MPG (US) to km/L: ${formatNumber(convertFuel(30, 'mpg_us', 'km_per_liter'))} km/L\n`);

// ============================================================================
// Generic Convert Examples
// ============================================================================

console.log('--- Generic Convert (Auto-detect) ---');
console.log(`100°C to °F: ${convert(100, 'celsius', 'fahrenheit')}°F`);
console.log(`1 km to miles: ${formatNumber(convert(1, 'km', 'mile'))} miles`);
console.log(`1 kg to lbs: ${formatNumber(convert(1, 'kg', 'lb'))} lbs`);
console.log(`1 hour to minutes: ${convert(1, 'hour', 'minute')} min`);
console.log(`1 GiB to MiB: ${convert(1, 'gibibyte', 'mebibyte')} MiB\n`);

// ============================================================================
// Utility Function Examples
// ============================================================================

console.log('--- Utility Functions ---');
console.log(`Unit category of 'meter': ${getUnitCategory('meter')}`);
console.log(`Unit category of 'kilogram': ${getUnitCategory('kilogram')}`);
console.log(`Unit category of 'celsius': ${getUnitCategory('celsius')}`);

console.log('\nAvailable categories:', getCategories().join(', '));

console.log('\nTemperature units:', getAvailableUnits('temperature').join(', '));

console.log(`\nCan convert 'meter' to 'foot': ${canConvert('meter', 'foot')}`);
console.log(`Can convert 'meter' to 'kilogram': ${canConvert('meter', 'kilogram')}`);

console.log('\nFormatted numbers:');
console.log(`  ${formatNumber(3.14159265, 2)} (π with 2 decimals)`);
console.log(`  ${formatNumber(10000000000, 2)} (10 billion in scientific notation)`);
console.log(`  ${formatNumber(0.000001, 6)} (1 micro)`);

console.log('\n========================================');
console.log('  End of Examples');
console.log('========================================\n');