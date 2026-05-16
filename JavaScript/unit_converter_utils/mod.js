/**
 * Unit Converter Utils
 * A comprehensive unit conversion library with zero external dependencies.
 * 
 * Supports: Temperature, Length, Weight, Volume, Area, Speed, Time, Data
 * 
 * @module unit_converter_utils
 */

// ============================================================================
// Temperature Conversion
// ============================================================================

/**
 * Temperature conversion factors and formulas
 */
const temperature = {
  celsius: {
    toFahrenheit: (c) => (c * 9/5) + 32,
    toKelvin: (c) => c + 273.15,
    toRankine: (c) => (c + 273.15) * 9/5,
  },
  fahrenheit: {
    toCelsius: (f) => (f - 32) * 5/9,
    toKelvin: (f) => (f - 32) * 5/9 + 273.15,
    toRankine: (f) => f + 459.67,
  },
  kelvin: {
    toCelsius: (k) => k - 273.15,
    toFahrenheit: (k) => (k - 273.15) * 9/5 + 32,
    toRankine: (k) => k * 9/5,
  },
  rankine: {
    toCelsius: (r) => (r - 491.67) * 5/9,
    toFahrenheit: (r) => r - 459.67,
    toKelvin: (r) => r * 5/9,
  },
};

/**
 * Convert temperature between units
 * @param {number} value - The value to convert
 * @param {string} from - Source unit (celsius, fahrenheit, kelvin, rankine)
 * @param {string} to - Target unit
 * @returns {number} Converted value
 */
function convertTemperature(value, from, to) {
  from = from.toLowerCase();
  to = to.toLowerCase();
  
  if (from === to) return value;
  
  // Convert to Celsius first, then to target
  let celsius;
  switch (from) {
    case 'celsius':
    case 'c':
      celsius = value;
      break;
    case 'fahrenheit':
    case 'f':
      celsius = temperature.fahrenheit.toCelsius(value);
      break;
    case 'kelvin':
    case 'k':
      celsius = temperature.kelvin.toCelsius(value);
      break;
    case 'rankine':
    case 'r':
      celsius = temperature.rankine.toCelsius(value);
      break;
    default:
      throw new Error(`Unknown temperature unit: ${from}`);
  }
  
  // Convert from Celsius to target
  switch (to) {
    case 'celsius':
    case 'c':
      return celsius;
    case 'fahrenheit':
    case 'f':
      return temperature.celsius.toFahrenheit(celsius);
    case 'kelvin':
    case 'k':
      return temperature.celsius.toKelvin(celsius);
    case 'rankine':
    case 'r':
      return temperature.celsius.toRankine(celsius);
    default:
      throw new Error(`Unknown temperature unit: ${to}`);
  }
}

// ============================================================================
// Length Conversion
// ============================================================================

/**
 * Length units in meters (base unit)
 */
const lengthUnits = {
  // Metric
  nanometer: 1e-9,
  micrometer: 1e-6,
  millimeter: 0.001,
  centimeter: 0.01,
  decimeter: 0.1,
  meter: 1,
  dekameter: 10,
  hectometer: 100,
  kilometer: 1000,
  // Imperial
  inch: 0.0254,
  foot: 0.3048,
  yard: 0.9144,
  mile: 1609.344,
  nautical_mile: 1852,
  // Astronomical
  astronomical_unit: 1.496e11,
  light_year: 9.461e15,
  parsec: 3.086e16,
  // Aliases
  nm: 1e-9,
  um: 1e-6,
  mm: 0.001,
  cm: 0.01,
  dm: 0.1,
  m: 1,
  dam: 10,
  hm: 100,
  km: 1000,
  in: 0.0254,
  ft: 0.3048,
  yd: 0.9144,
  mi: 1609.344,
  nmi: 1852,
  au: 1.496e11,
  ly: 9.461e15,
  pc: 3.086e16,
};

/**
 * Convert length between units
 * @param {number} value - The value to convert
 * @param {string} from - Source unit
 * @param {string} to - Target unit
 * @returns {number} Converted value
 */
function convertLength(value, from, to) {
  from = from.toLowerCase().replace(/[^a-z_]/g, '_');
  to = to.toLowerCase().replace(/[^a-z_]/g, '_');
  
  if (from === to) return value;
  
  const fromFactor = lengthUnits[from];
  const toFactor = lengthUnits[to];
  
  if (!fromFactor) throw new Error(`Unknown length unit: ${from}`);
  if (!toFactor) throw new Error(`Unknown length unit: ${to}`);
  
  // Convert to meters, then to target
  const meters = value * fromFactor;
  return meters / toFactor;
}

// ============================================================================
// Weight/Mass Conversion
// ============================================================================

/**
 * Weight units in kilograms (base unit)
 */
const weightUnits = {
  // Metric
  microgram: 1e-9,
  milligram: 1e-6,
  gram: 0.001,
  kilogram: 1,
  metric_ton: 1000,
  // Imperial
  ounce: 0.028349523125,
  pound: 0.45359237,
  stone: 6.35029318,
  short_ton: 907.18474,
  long_ton: 1016.0469088,
  // Aliases
  ug: 1e-9,
  mg: 1e-6,
  g: 0.001,
  kg: 1,
  t: 1000,
  oz: 0.028349523125,
  lb: 0.45359237,
  lbs: 0.45359237,
  st: 6.35029318,
};

/**
 * Convert weight/mass between units
 * @param {number} value - The value to convert
 * @param {string} from - Source unit
 * @param {string} to - Target unit
 * @returns {number} Converted value
 */
function convertWeight(value, from, to) {
  from = from.toLowerCase().replace(/[^a-z_]/g, '_');
  to = to.toLowerCase().replace(/[^a-z_]/g, '_');
  
  if (from === to) return value;
  
  const fromFactor = weightUnits[from];
  const toFactor = weightUnits[to];
  
  if (!fromFactor) throw new Error(`Unknown weight unit: ${from}`);
  if (!toFactor) throw new Error(`Unknown weight unit: ${to}`);
  
  const kilograms = value * fromFactor;
  return kilograms / toFactor;
}

// ============================================================================
// Volume Conversion
// ============================================================================

/**
 * Volume units in liters (base unit)
 */
const volumeUnits = {
  // Metric
  microliter: 1e-6,
  milliliter: 0.001,
  liter: 1,
  cubic_centimeter: 0.001,
  cubic_meter: 1000,
  // Imperial/US
  fluid_ounce_us: 0.0295735295625,
  fluid_ounce_uk: 0.0284130625,
  cup_us: 0.2365882365,
  pint_us: 0.473176473,
  quart_us: 0.946352946,
  gallon_us: 3.785411784,
  pint_uk: 0.56826125,
  quart_uk: 1.1365225,
  gallon_uk: 4.54609,
  // Cooking
  tablespoon: 0.01478676478125,
  teaspoon: 0.00492892159375,
  // Aliases
  ul: 1e-6,
  ml: 0.001,
  l: 1,
  cc: 0.001,
  cm3: 0.001,
  m3: 1000,
  floz_us: 0.0295735295625,
  floz_uk: 0.0284130625,
  cup: 0.2365882365,
  pt_us: 0.473176473,
  qt_us: 0.946352946,
  gal_us: 3.785411784,
  pt_uk: 0.56826125,
  qt_uk: 1.1365225,
  gal_uk: 4.54609,
  tbsp: 0.01478676478125,
  tsp: 0.00492892159375,
};

/**
 * Convert volume between units
 * @param {number} value - The value to convert
 * @param {string} from - Source unit
 * @param {string} to - Target unit
 * @returns {number} Converted value
 */
function convertVolume(value, from, to) {
  from = from.toLowerCase().replace(/[^a-z_0-9]/g, '_');
  to = to.toLowerCase().replace(/[^a-z_0-9]/g, '_');
  
  if (from === to) return value;
  
  const fromFactor = volumeUnits[from];
  const toFactor = volumeUnits[to];
  
  if (!fromFactor) throw new Error(`Unknown volume unit: ${from}`);
  if (!toFactor) throw new Error(`Unknown volume unit: ${to}`);
  
  const liters = value * fromFactor;
  return liters / toFactor;
}

// ============================================================================
// Area Conversion
// ============================================================================

/**
 * Area units in square meters (base unit)
 */
const areaUnits = {
  // Metric
  square_millimeter: 1e-6,
  square_centimeter: 1e-4,
  square_meter: 1,
  square_kilometer: 1e6,
  hectare: 1e4,
  // Imperial
  square_inch: 0.00064516,
  square_foot: 0.09290304,
  square_yard: 0.83612736,
  square_mile: 2589988.110336,
  acre: 4046.8564224,
  // Aliases
  mm2: 1e-6,
  cm2: 1e-4,
  m2: 1,
  km2: 1e6,
  ha: 1e4,
  in2: 0.00064516,
  ft2: 0.09290304,
  yd2: 0.83612736,
  mi2: 2589988.110336,
};

/**
 * Convert area between units
 * @param {number} value - The value to convert
 * @param {string} from - Source unit
 * @param {string} to - Target unit
 * @returns {number} Converted value
 */
function convertArea(value, from, to) {
  from = from.toLowerCase().replace(/[^a-z_0-9]/g, '_');
  to = to.toLowerCase().replace(/[^a-z_0-9]/g, '_');
  
  if (from === to) return value;
  
  const fromFactor = areaUnits[from];
  const toFactor = areaUnits[to];
  
  if (!fromFactor) throw new Error(`Unknown area unit: ${from}`);
  if (!toFactor) throw new Error(`Unknown area unit: ${to}`);
  
  const squareMeters = value * fromFactor;
  return squareMeters / toFactor;
}

// ============================================================================
// Speed Conversion
// ============================================================================

/**
 * Speed units in meters per second (base unit)
 */
const speedUnits = {
  // Metric
  meters_per_second: 1,
  kilometers_per_hour: 1/3.6,
  // Imperial
  miles_per_hour: 0.44704,
  feet_per_second: 0.3048,
  knots: 0.514444,
  // Scientific
  mach: 340.29, // at sea level, 15°C
  speed_of_light: 299792458,
  // Aliases
  mps: 1,
  m_s: 1,
  kmh: 1/3.6,
  km_h: 1/3.6,
  mph: 0.44704,
  fps: 0.3048,
  ft_s: 0.3048,
  knot: 0.514444,
  kn: 0.514444,
  c: 299792458,
};

/**
 * Convert speed between units
 * @param {number} value - The value to convert
 * @param {string} from - Source unit
 * @param {string} to - Target unit
 * @returns {number} Converted value
 */
function convertSpeed(value, from, to) {
  from = from.toLowerCase().replace(/[^a-z_]/g, '_');
  to = to.toLowerCase().replace(/[^a-z_]/g, '_');
  
  if (from === to) return value;
  
  const fromFactor = speedUnits[from];
  const toFactor = speedUnits[to];
  
  if (!fromFactor) throw new Error(`Unknown speed unit: ${from}`);
  if (!toFactor) throw new Error(`Unknown speed unit: ${to}`);
  
  const metersPerSecond = value * fromFactor;
  return metersPerSecond / toFactor;
}

// ============================================================================
// Time Conversion
// ============================================================================

/**
 * Time units in seconds (base unit)
 */
const timeUnits = {
  nanosecond: 1e-9,
  microsecond: 1e-6,
  millisecond: 0.001,
  second: 1,
  minute: 60,
  hour: 3600,
  day: 86400,
  week: 604800,
  month: 2629746, // Average month (365.25/12 days)
  year: 31556952, // Tropical year
  decade: 315569520,
  century: 3155695200,
  // Aliases
  ns: 1e-9,
  us: 1e-6,
  ms: 0.001,
  s: 1,
  sec: 1,
  min: 60,
  h: 3600,
  hr: 3600,
  d: 86400,
  w: 604800,
  mo: 2629746,
  y: 31556952,
  yr: 31556952,
};

/**
 * Convert time between units
 * @param {number} value - The value to convert
 * @param {string} from - Source unit
 * @param {string} to - Target unit
 * @returns {number} Converted value
 */
function convertTime(value, from, to) {
  from = from.toLowerCase().replace(/[^a-z_]/g, '_');
  to = to.toLowerCase().replace(/[^a-z_]/g, '_');
  
  if (from === to) return value;
  
  const fromFactor = timeUnits[from];
  const toFactor = timeUnits[to];
  
  if (!fromFactor) throw new Error(`Unknown time unit: ${from}`);
  if (!toFactor) throw new Error(`Unknown time unit: ${to}`);
  
  const seconds = value * fromFactor;
  return seconds / toFactor;
}

// ============================================================================
// Data Conversion
// ============================================================================

/**
 * Data units in bytes (base unit)
 */
const dataUnits = {
  // Binary (IEC)
  byte: 1,
  kibibyte: 1024,
  mebibyte: 1048576,
  gibibyte: 1073741824,
  tebibyte: 1099511627776,
  pebibyte: 1125899906842624,
  // Decimal (SI)
  kilobyte: 1000,
  megabyte: 1e6,
  gigabyte: 1e9,
  terabyte: 1e12,
  petabyte: 1e15,
  // Bits
  bit: 0.125,
  kilobit: 125,
  megabit: 125000,
  gigabit: 125000000,
  // Aliases
  b: 1,
  kib: 1024,
  mib: 1048576,
  gib: 1073741824,
  tib: 1099511627776,
  pib: 1125899906842624,
  kb: 1000,
  mb: 1e6,
  gb: 1e9,
  tb: 1e12,
  pb: 1e15,
};

/**
 * Convert data between units
 * @param {number} value - The value to convert
 * @param {string} from - Source unit
 * @param {string} to - Target unit
 * @returns {number} Converted value
 */
function convertData(value, from, to) {
  from = from.toLowerCase().replace(/[^a-z_]/g, '_');
  to = to.toLowerCase().replace(/[^a-z_]/g, '_');
  
  if (from === to) return value;
  
  const fromFactor = dataUnits[from];
  const toFactor = dataUnits[to];
  
  if (!fromFactor) throw new Error(`Unknown data unit: ${from}`);
  if (!toFactor) throw new Error(`Unknown data unit: ${to}`);
  
  const bytes = value * fromFactor;
  return bytes / toFactor;
}

// ============================================================================
// Pressure Conversion
// ============================================================================

/**
 * Pressure units in pascals (base unit)
 */
const pressureUnits = {
  pascal: 1,
  kilopascal: 1000,
  megapascal: 1e6,
  bar: 100000,
  millibar: 100,
  psi: 6894.757293168,
  atmosphere: 101325,
  torr: 133.3223684211,
  mmhg: 133.3223684211,
  // Aliases
  pa: 1,
  kpa: 1000,
  mpa: 1e6,
  bar: 100000,
  mbar: 100,
  atm: 101325,
};

/**
 * Convert pressure between units
 * @param {number} value - The value to convert
 * @param {string} from - Source unit
 * @param {string} to - Target unit
 * @returns {number} Converted value
 */
function convertPressure(value, from, to) {
  from = from.toLowerCase().replace(/[^a-z_]/g, '_');
  to = to.toLowerCase().replace(/[^a-z_]/g, '_');
  
  if (from === to) return value;
  
  const fromFactor = pressureUnits[from];
  const toFactor = pressureUnits[to];
  
  if (!fromFactor) throw new Error(`Unknown pressure unit: ${from}`);
  if (!toFactor) throw new Error(`Unknown pressure unit: ${to}`);
  
  const pascals = value * fromFactor;
  return pascals / toFactor;
}

// ============================================================================
// Angle Conversion
// ============================================================================

/**
 * Convert angle between units
 * @param {number} value - The value to convert
 * @param {string} from - Source unit (degree, radian, gradian, arcminute, arcsecond)
 * @param {string} to - Target unit
 * @returns {number} Converted value
 */
function convertAngle(value, from, to) {
  from = from.toLowerCase();
  to = to.toLowerCase();
  
  if (from === to) return value;
  
  // Convert to degrees first
  let degrees;
  switch (from) {
    case 'degree':
    case 'deg':
    case '°':
      degrees = value;
      break;
    case 'radian':
    case 'rad':
      degrees = value * (180 / Math.PI);
      break;
    case 'gradian':
    case 'gon':
      degrees = value * 0.9;
      break;
    case 'arcminute':
    case 'arcmin':
    case "'":
      degrees = value / 60;
      break;
    case 'arcsecond':
    case 'arcsec':
    case '"':
      degrees = value / 3600;
      break;
    default:
      throw new Error(`Unknown angle unit: ${from}`);
  }
  
  // Convert from degrees to target
  switch (to) {
    case 'degree':
    case 'deg':
    case '°':
      return degrees;
    case 'radian':
    case 'rad':
      return degrees * (Math.PI / 180);
    case 'gradian':
    case 'gon':
      return degrees / 0.9;
    case 'arcminute':
    case 'arcmin':
    case "'":
      return degrees * 60;
    case 'arcsecond':
    case 'arcsec':
    case '"':
      return degrees * 3600;
    default:
      throw new Error(`Unknown angle unit: ${to}`);
  }
}

// ============================================================================
// Fuel Consumption Conversion
// ============================================================================

/**
 * Fuel consumption units in km/l (base unit)
 */
const fuelUnits = {
  km_per_liter: 1,
  liters_per_100km: 100, // Stored as inverse: 100 / (km/l)
  miles_per_gallon_us: 0.4251437074,
  miles_per_gallon_uk: 0.3540061899,
  // Aliases
  km_l: 1,
  kml: 1,
  l_100km: 100,
  mpg_us: 0.4251437074,
  mpg_uk: 0.3540061899,
  mpg: 0.4251437074, // Default to US
};

/**
 * Convert fuel consumption between units
 * @param {number} value - The value to convert
 * @param {string} from - Source unit
 * @param {string} to - Target unit
 * @returns {number} Converted value
 */
function convertFuel(value, from, to) {
  from = from.toLowerCase().replace(/[^a-z_0-9]/g, '_');
  to = to.toLowerCase().replace(/[^a-z_0-9]/g, '_');
  
  if (from === to) return value;
  
  // Special case for liters_per_100km (inverse relationship)
  if (from === 'liters_per_100km' || from === 'l_100km') {
    // Convert L/100km to km/L first
    if (value === 0) throw new Error('Cannot convert zero L/100km');
    const kmPerLiter = 100 / value;
    return convertFuel(kmPerLiter, 'km_per_liter', to);
  }
  
  if (to === 'liters_per_100km' || to === 'l_100km') {
    // Convert to L/100km from km/L
    if (value === 0) throw new Error('Cannot convert zero km/L to L/100km');
    const kmPerLiter = convertFuel(value, from, 'km_per_liter');
    return 100 / kmPerLiter;
  }
  
  const fromFactor = fuelUnits[from];
  const toFactor = fuelUnits[to];
  
  if (!fromFactor) throw new Error(`Unknown fuel unit: ${from}`);
  if (!toFactor) throw new Error(`Unknown fuel unit: ${to}`);
  
  const kmPerLiter = value * fromFactor;
  return kmPerLiter / toFactor;
}

// ============================================================================
// Generic Converter
// ============================================================================

/**
 * Get the category of a unit
 * @param {string} unit - Unit name
 * @returns {string|null} Category name or null if not found
 */
function getUnitCategory(unit) {
  unit = unit.toLowerCase().replace(/[^a-z_0-9]/g, '_');
  
  if (unit in lengthUnits) return 'length';
  if (unit in weightUnits) return 'weight';
  if (unit in volumeUnits) return 'volume';
  if (unit in areaUnits) return 'area';
  if (unit in speedUnits) return 'speed';
  if (unit in timeUnits) return 'time';
  if (unit in dataUnits) return 'data';
  if (unit in pressureUnits) return 'pressure';
  if (['celsius', 'fahrenheit', 'kelvin', 'rankine', 'c', 'f', 'k', 'r'].includes(unit)) return 'temperature';
  if (['degree', 'radian', 'gradian', 'deg', 'rad', 'gon'].includes(unit)) return 'angle';
  if (unit in fuelUnits) return 'fuel';
  
  return null;
}

/**
 * Generic unit conversion function
 * @param {number} value - The value to convert
 * @param {string} from - Source unit
 * @param {string} to - Target unit
 * @returns {number} Converted value
 */
function convert(value, from, to) {
  const fromCategory = getUnitCategory(from);
  const toCategory = getUnitCategory(to);
  
  if (!fromCategory) throw new Error(`Unknown unit: ${from}`);
  if (!toCategory) throw new Error(`Unknown unit: ${to}`);
  if (fromCategory !== toCategory) {
    throw new Error(`Cannot convert between ${fromCategory} and ${toCategory}`);
  }
  
  switch (fromCategory) {
    case 'temperature':
      return convertTemperature(value, from, to);
    case 'length':
      return convertLength(value, from, to);
    case 'weight':
      return convertWeight(value, from, to);
    case 'volume':
      return convertVolume(value, from, to);
    case 'area':
      return convertArea(value, from, to);
    case 'speed':
      return convertSpeed(value, from, to);
    case 'time':
      return convertTime(value, from, to);
    case 'data':
      return convertData(value, from, to);
    case 'pressure':
      return convertPressure(value, from, to);
    case 'angle':
      return convertAngle(value, from, to);
    case 'fuel':
      return convertFuel(value, from, to);
    default:
      throw new Error(`Unknown category: ${fromCategory}`);
  }
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Format a number with appropriate precision
 * @param {number} value - The number to format
 * @param {number} [decimals=4] - Maximum decimal places
 * @returns {string} Formatted number string
 */
function formatNumber(value, decimals = 4) {
  if (typeof value !== 'number' || isNaN(value)) {
    throw new Error('Value must be a valid number');
  }
  
  // Use scientific notation for very large or very small numbers
  if (Math.abs(value) >= 1e10 || (Math.abs(value) < 1e-6 && value !== 0)) {
    return value.toExponential(decimals);
  }
  
  // Round to specified decimals, removing trailing zeros
  const rounded = Number(value.toFixed(decimals));
  return rounded.toString();
}

/**
 * Get all available units for a category
 * @param {string} category - Category name
 * @returns {string[]} Array of unit names
 */
function getAvailableUnits(category) {
  category = category.toLowerCase();
  
  const unitMaps = {
    temperature: ['celsius', 'fahrenheit', 'kelvin', 'rankine'],
    length: [...new Set(Object.keys(lengthUnits))],
    weight: [...new Set(Object.keys(weightUnits))],
    volume: [...new Set(Object.keys(volumeUnits))],
    area: [...new Set(Object.keys(areaUnits))],
    speed: [...new Set(Object.keys(speedUnits))],
    time: [...new Set(Object.keys(timeUnits))],
    data: [...new Set(Object.keys(dataUnits))],
    pressure: [...new Set(Object.keys(pressureUnits))],
    angle: ['degree', 'radian', 'gradian', 'arcminute', 'arcsecond'],
    fuel: [...new Set(Object.keys(fuelUnits))],
  };
  
  return unitMaps[category] || [];
}

/**
 * Get all categories
 * @returns {string[]} Array of category names
 */
function getCategories() {
  return [
    'temperature',
    'length',
    'weight',
    'volume',
    'area',
    'speed',
    'time',
    'data',
    'pressure',
    'angle',
    'fuel',
  ];
}

/**
 * Check if a conversion is valid
 * @param {string} from - Source unit
 * @param {string} to - Target unit
 * @returns {boolean} True if conversion is valid
 */
function canConvert(from, to) {
  try {
    const fromCategory = getUnitCategory(from);
    const toCategory = getUnitCategory(to);
    return fromCategory !== null && toCategory !== null && fromCategory === toCategory;
  } catch {
    return false;
  }
}

// ============================================================================
// Exports
// ============================================================================

module.exports = {
  // Temperature
  convertTemperature,
  
  // Length
  convertLength,
  
  // Weight
  convertWeight,
  
  // Volume
  convertVolume,
  
  // Area
  convertArea,
  
  // Speed
  convertSpeed,
  
  // Time
  convertTime,
  
  // Data
  convertData,
  
  // Pressure
  convertPressure,
  
  // Angle
  convertAngle,
  
  // Fuel
  convertFuel,
  
  // Generic
  convert,
  getUnitCategory,
  getAvailableUnits,
  getCategories,
  canConvert,
  
  // Utilities
  formatNumber,
  
  // Unit definitions (for advanced use)
  lengthUnits,
  weightUnits,
  volumeUnits,
  areaUnits,
  speedUnits,
  timeUnits,
  dataUnits,
  pressureUnits,
  fuelUnits,
};