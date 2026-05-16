/**
 * Unit Converter Utils Tests
 * Comprehensive test suite for unit conversion functions
 */

const assert = require('assert');
const {
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
  convert,
  getUnitCategory,
  getAvailableUnits,
  getCategories,
  canConvert,
  formatNumber,
} = require('./mod.js');

// Test helper
function assertApprox(actual, expected, tolerance = 1e-6, message = '') {
  const diff = Math.abs(actual - expected);
  if (diff > tolerance) {
    throw new Error(
      `${message}\nExpected: ${expected}\nActual: ${actual}\nDifference: ${diff}`
    );
  }
}

// ============================================================================
// Temperature Tests
// ============================================================================

function testTemperatureConversions() {
  console.log('Testing temperature conversions...');
  
  // Celsius to Fahrenheit
  assertApprox(convertTemperature(0, 'celsius', 'fahrenheit'), 32);
  assertApprox(convertTemperature(100, 'celsius', 'fahrenheit'), 212);
  assertApprox(convertTemperature(-40, 'celsius', 'fahrenheit'), -40);
  
  // Fahrenheit to Celsius
  assertApprox(convertTemperature(32, 'fahrenheit', 'celsius'), 0);
  assertApprox(convertTemperature(212, 'fahrenheit', 'celsius'), 100);
  
  // Celsius to Kelvin
  assertApprox(convertTemperature(0, 'celsius', 'kelvin'), 273.15);
  assertApprox(convertTemperature(-273.15, 'celsius', 'kelvin'), 0);
  
  // Kelvin to Celsius
  assertApprox(convertTemperature(273.15, 'kelvin', 'celsius'), 0);
  assertApprox(convertTemperature(373.15, 'kelvin', 'celsius'), 100);
  
  // Short aliases
  assertApprox(convertTemperature(0, 'C', 'F'), 32);
  assertApprox(convertTemperature(100, 'C', 'K'), 373.15);
  assertApprox(convertTemperature(32, 'F', 'C'), 0);
  
  // Rankine
  assertApprox(convertTemperature(0, 'celsius', 'rankine'), 491.67, 0.01);
  assertApprox(convertTemperature(0, 'rankine', 'fahrenheit'), -459.67, 0.01);
  
  console.log('  ✓ Temperature conversions passed');
}

// ============================================================================
// Length Tests
// ============================================================================

function testLengthConversions() {
  console.log('Testing length conversions...');
  
  // Metric
  assertApprox(convertLength(1, 'meter', 'centimeter'), 100);
  assertApprox(convertLength(100, 'centimeter', 'meter'), 1);
  assertApprox(convertLength(1, 'kilometer', 'meter'), 1000);
  assertApprox(convertLength(1000, 'meter', 'kilometer'), 1);
  
  // Imperial
  assertApprox(convertLength(1, 'foot', 'inch'), 12);
  assertApprox(convertLength(3, 'foot', 'yard'), 1);
  assertApprox(convertLength(1, 'mile', 'foot'), 5280);
  
  // Cross-system
  assertApprox(convertLength(2.54, 'centimeter', 'inch'), 1);
  assertApprox(convertLength(1, 'inch', 'centimeter'), 2.54);
  assertApprox(convertLength(1, 'kilometer', 'mile'), 0.621371, 1e-5);
  
  // Short aliases
  assertApprox(convertLength(1, 'm', 'cm'), 100);
  assertApprox(convertLength(1, 'km', 'm'), 1000);
  assertApprox(convertLength(1, 'ft', 'in'), 12);
  
  // Astronomical
  assertApprox(convertLength(1, 'au', 'km'), 149600000, 1e6);
  
  console.log('  ✓ Length conversions passed');
}

// ============================================================================
// Weight Tests
// ============================================================================

function testWeightConversions() {
  console.log('Testing weight conversions...');
  
  // Metric
  assertApprox(convertWeight(1, 'kilogram', 'gram'), 1000);
  assertApprox(convertWeight(1000, 'gram', 'kilogram'), 1);
  assertApprox(convertWeight(1, 'metric_ton', 'kilogram'), 1000);
  
  // Imperial
  assertApprox(convertWeight(1, 'pound', 'ounce'), 16);
  assertApprox(convertWeight(14, 'pound', 'stone'), 1);
  
  // Cross-system
  assertApprox(convertWeight(1, 'kilogram', 'pound'), 2.2046226, 1e-5);
  assertApprox(convertWeight(1, 'pound', 'kilogram'), 0.45359237);
  
  // Short aliases
  assertApprox(convertWeight(1, 'kg', 'g'), 1000);
  assertApprox(convertWeight(1, 'lb', 'oz'), 16);
  assertApprox(convertWeight(1, 'lbs', 'kg'), 0.45359237);
  
  console.log('  ✓ Weight conversions passed');
}

// ============================================================================
// Volume Tests
// ============================================================================

function testVolumeConversions() {
  console.log('Testing volume conversions...');
  
  // Metric
  assertApprox(convertVolume(1, 'liter', 'milliliter'), 1000);
  assertApprox(convertVolume(1000, 'milliliter', 'liter'), 1);
  assertApprox(convertVolume(1, 'cubic_meter', 'liter'), 1000);
  
  // US Customary
  assertApprox(convertVolume(1, 'gallon_us', 'quart_us'), 4);
  assertApprox(convertVolume(1, 'quart_us', 'pint_us'), 2);
  assertApprox(convertVolume(1, 'cup_us', 'tablespoon'), 16);
  assertApprox(convertVolume(1, 'tablespoon', 'teaspoon'), 3);
  
  // Cross-system
  assertApprox(convertVolume(1, 'liter', 'gallon_us'), 0.264172, 1e-5);
  
  // Short aliases
  assertApprox(convertVolume(1, 'l', 'ml'), 1000);
  assertApprox(convertVolume(1, 'gal_us', 'qt_us'), 4);
  
  console.log('  ✓ Volume conversions passed');
}

// ============================================================================
// Area Tests
// ============================================================================

function testAreaConversions() {
  console.log('Testing area conversions...');
  
  // Metric
  assertApprox(convertArea(1, 'square_meter', 'square_centimeter'), 10000);
  assertApprox(convertArea(1, 'hectare', 'square_meter'), 10000);
  assertApprox(convertArea(1, 'square_kilometer', 'hectare'), 100);
  
  // Imperial
  assertApprox(convertArea(1, 'square_foot', 'square_inch'), 144);
  assertApprox(convertArea(1, 'square_yard', 'square_foot'), 9);
  assertApprox(convertArea(1, 'acre', 'square_foot'), 43560, 1);
  
  // Cross-system
  assertApprox(convertArea(1, 'square_meter', 'square_foot'), 10.7639, 1e-3);
  
  // Short aliases
  assertApprox(convertArea(1, 'm2', 'cm2'), 10000);
  assertApprox(convertArea(1, 'ha', 'm2'), 10000);
  
  console.log('  ✓ Area conversions passed');
}

// ============================================================================
// Speed Tests
// ============================================================================

function testSpeedConversions() {
  console.log('Testing speed conversions...');
  
  // Basic
  assertApprox(convertSpeed(1, 'meters_per_second', 'kilometers_per_hour'), 3.6);
  assertApprox(convertSpeed(1, 'kilometers_per_hour', 'meters_per_second'), 1/3.6);
  
  // Imperial
  assertApprox(convertSpeed(60, 'miles_per_hour', 'kilometers_per_hour'), 96.5606, 1e-3);
  assertApprox(convertSpeed(1, 'miles_per_hour', 'feet_per_second'), 1.46667, 1e-4);
  
  // Nautical
  assertApprox(convertSpeed(1, 'knot', 'kilometers_per_hour'), 1.852, 1e-4);
  
  // Short aliases
  assertApprox(convertSpeed(1, 'mps', 'kmh'), 3.6);
  assertApprox(convertSpeed(1, 'mph', 'kmh'), 1.60934, 1e-4);
  assertApprox(convertSpeed(1, 'kn', 'kmh'), 1.852, 1e-4);
  
  console.log('  ✓ Speed conversions passed');
}

// ============================================================================
// Time Tests
// ============================================================================

function testTimeConversions() {
  console.log('Testing time conversions...');
  
  // Basic
  assertApprox(convertTime(1, 'minute', 'second'), 60);
  assertApprox(convertTime(1, 'hour', 'minute'), 60);
  assertApprox(convertTime(1, 'day', 'hour'), 24);
  assertApprox(convertTime(1, 'week', 'day'), 7);
  
  // Year
  assertApprox(convertTime(1, 'year', 'day'), 365.25, 1);
  
  // Small units
  assertApprox(convertTime(1, 'second', 'millisecond'), 1000);
  assertApprox(convertTime(1, 'millisecond', 'microsecond'), 1000);
  
  // Short aliases
  assertApprox(convertTime(1, 'h', 'min'), 60);
  assertApprox(convertTime(1, 'd', 'h'), 24);
  assertApprox(convertTime(1, 'y', 'd'), 365.25, 1);
  
  console.log('  ✓ Time conversions passed');
}

// ============================================================================
// Data Tests
// ============================================================================

function testDataConversions() {
  console.log('Testing data conversions...');
  
  // Binary (IEC)
  assertApprox(convertData(1, 'kibibyte', 'byte'), 1024);
  assertApprox(convertData(1, 'mebibyte', 'kibibyte'), 1024);
  assertApprox(convertData(1, 'gibibyte', 'mebibyte'), 1024);
  
  // Decimal (SI)
  assertApprox(convertData(1, 'kilobyte', 'byte'), 1000);
  assertApprox(convertData(1, 'megabyte', 'kilobyte'), 1000);
  assertApprox(convertData(1, 'gigabyte', 'megabyte'), 1000);
  
  // Cross-standard
  assertApprox(convertData(1, 'mebibyte', 'megabyte'), 1.048576);
  
  // Bits
  assertApprox(convertData(1, 'byte', 'bit'), 8);
  assertApprox(convertData(1, 'megabit', 'megabyte'), 0.125);
  
  // Short aliases
  assertApprox(convertData(1, 'mib', 'kib'), 1024);
  assertApprox(convertData(1, 'mb', 'kb'), 1000);
  
  console.log('  ✓ Data conversions passed');
}

// ============================================================================
// Pressure Tests
// ============================================================================

function testPressureConversions() {
  console.log('Testing pressure conversions...');
  
  // Basic
  assertApprox(convertPressure(1, 'kilopascal', 'pascal'), 1000);
  assertApprox(convertPressure(1, 'bar', 'kilopascal'), 100);
  assertApprox(convertPressure(1, 'atmosphere', 'pascal'), 101325);
  
  // Common conversions
  assertApprox(convertPressure(1, 'atmosphere', 'psi'), 14.6959, 1e-3);
  assertApprox(convertPressure(1, 'bar', 'psi'), 14.5038, 1e-3);
  
  // Short aliases
  assertApprox(convertPressure(1, 'kpa', 'pa'), 1000);
  assertApprox(convertPressure(1, 'atm', 'pa'), 101325);
  
  console.log('  ✓ Pressure conversions passed');
}

// ============================================================================
// Angle Tests
// ============================================================================

function testAngleConversions() {
  console.log('Testing angle conversions...');
  
  // Degrees to Radians
  assertApprox(convertAngle(180, 'degree', 'radian'), Math.PI);
  assertApprox(convertAngle(90, 'degree', 'radian'), Math.PI / 2);
  assertApprox(convertAngle(45, 'degree', 'radian'), Math.PI / 4);
  
  // Radians to Degrees
  assertApprox(convertAngle(Math.PI, 'radian', 'degree'), 180);
  assertApprox(convertAngle(Math.PI / 2, 'radian', 'degree'), 90);
  
  // Gradians
  assertApprox(convertAngle(100, 'gradian', 'degree'), 90);
  assertApprox(convertAngle(400, 'gradian', 'degree'), 360);
  
  // Arcminutes and Arcseconds
  assertApprox(convertAngle(1, 'degree', 'arcminute'), 60);
  assertApprox(convertAngle(1, 'arcminute', 'arcsecond'), 60);
  assertApprox(convertAngle(1, 'degree', 'arcsecond'), 3600);
  
  // Short aliases
  assertApprox(convertAngle(180, 'deg', 'rad'), Math.PI);
  assertApprox(convertAngle(100, 'gon', 'deg'), 90);
  
  console.log('  ✓ Angle conversions passed');
}

// ============================================================================
// Fuel Tests
// ============================================================================

function testFuelConversions() {
  console.log('Testing fuel consumption conversions...');
  
  // km/L to L/100km (inverse)
  assertApprox(convertFuel(10, 'km_per_liter', 'liters_per_100km'), 10);
  assertApprox(convertFuel(5, 'km_per_liter', 'liters_per_100km'), 20);
  
  // L/100km to km/L
  assertApprox(convertFuel(10, 'liters_per_100km', 'km_per_liter'), 10);
  assertApprox(convertFuel(20, 'liters_per_100km', 'km_per_liter'), 5);
  
  // MPG (US)
  assertApprox(convertFuel(30, 'mpg_us', 'km_per_liter'), 12.754, 1e-2);
  
  // Short aliases
  assertApprox(convertFuel(10, 'kml', 'l_100km'), 10);
  
  console.log('  ✓ Fuel consumption conversions passed');
}

// ============================================================================
// Generic Convert Tests
// ============================================================================

function testGenericConvert() {
  console.log('Testing generic convert function...');
  
  // Auto-detect category and convert
  assertApprox(convert(100, 'celsius', 'fahrenheit'), 212);
  assertApprox(convert(1, 'km', 'mile'), 0.621371, 1e-5);
  assertApprox(convert(1, 'kg', 'lb'), 2.2046226, 1e-5);
  assertApprox(convert(1, 'l', 'ml'), 1000);
  assertApprox(convert(1, 'h', 'min'), 60);
  
  // Same unit
  assertApprox(convert(100, 'meter', 'meter'), 100);
  
  console.log('  ✓ Generic convert function passed');
}

// ============================================================================
// Utility Function Tests
// ============================================================================

function testUtilityFunctions() {
  console.log('Testing utility functions...');
  
  // getUnitCategory
  assert.strictEqual(getUnitCategory('meter'), 'length');
  assert.strictEqual(getUnitCategory('kg'), 'weight');
  assert.strictEqual(getUnitCategory('celsius'), 'temperature');
  assert.strictEqual(getUnitCategory('unknown'), null);
  
  // getAvailableUnits
  const tempUnits = getAvailableUnits('temperature');
  assert.ok(Array.isArray(tempUnits));
  assert.ok(tempUnits.includes('celsius'));
  assert.ok(tempUnits.includes('fahrenheit'));
  
  // getCategories
  const categories = getCategories();
  assert.ok(Array.isArray(categories));
  assert.ok(categories.includes('length'));
  assert.ok(categories.includes('weight'));
  assert.ok(categories.includes('temperature'));
  
  // canConvert
  assert.strictEqual(canConvert('meter', 'foot'), true);
  assert.strictEqual(canConvert('kilogram', 'pound'), true);
  assert.strictEqual(canConvert('meter', 'kilogram'), false);
  assert.strictEqual(canConvert('unknown', 'meter'), false);
  
  // formatNumber
  assert.strictEqual(formatNumber(3.14159, 2), '3.14');
  assert.strictEqual(formatNumber(3.1, 4), '3.1'); // Trailing zeros removed
  assert.strictEqual(formatNumber(10000000000, 2), '1.00e+10'); // Scientific notation
  
  console.log('  ✓ Utility functions passed');
}

// ============================================================================
// Error Handling Tests
// ============================================================================

function testErrorHandling() {
  console.log('Testing error handling...');
  
  // Invalid units
  assert.throws(() => convertTemperature(0, 'celsius', 'invalid'), /Unknown temperature unit/);
  assert.throws(() => convertLength(1, 'meter', 'invalid'), /Unknown length unit/);
  assert.throws(() => convertWeight(1, 'kg', 'invalid'), /Unknown weight unit/);
  
  // Cross-category conversion
  assert.throws(() => convert(1, 'meter', 'kilogram'), /Cannot convert between/);
  
  // Zero fuel consumption
  assert.throws(() => convertFuel(0, 'liters_per_100km', 'km_per_liter'), /Cannot convert zero/);
  assert.throws(() => convertFuel(0, 'km_per_liter', 'liters_per_100km'), /Cannot convert zero/);
  
  // Invalid formatNumber
  assert.throws(() => formatNumber('not a number'), /must be a valid number/);
  assert.throws(() => formatNumber(NaN), /must be a valid number/);
  
  console.log('  ✓ Error handling passed');
}

// ============================================================================
// Run All Tests
// ============================================================================

function runAllTests() {
  console.log('\n=== Unit Converter Utils Tests ===\n');
  
  try {
    testTemperatureConversions();
    testLengthConversions();
    testWeightConversions();
    testVolumeConversions();
    testAreaConversions();
    testSpeedConversions();
    testTimeConversions();
    testDataConversions();
    testPressureConversions();
    testAngleConversions();
    testFuelConversions();
    testGenericConvert();
    testUtilityFunctions();
    testErrorHandling();
    
    console.log('\n✅ All tests passed!\n');
    return true;
  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    console.error(error.stack);
    return false;
  }
}

// Run tests if executed directly
if (require.main === module) {
  const success = runAllTests();
  process.exit(success ? 0 : 1);
}

module.exports = { runAllTests };