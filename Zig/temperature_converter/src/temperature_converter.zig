const std = @import("std");

/// Temperature conversion errors
pub const TemperatureError = error{
    AbsoluteZeroViolation,
    InvalidTemperature,
    OverflowDetected,
};

/// Check if two strings are equal (case-insensitive, ASCII only)
fn equalIgnoreCase(a: []const u8, b: []const u8) bool {
    if (a.len != b.len) return false;
    for (a, b) |c1, c2| {
        const l1: u8 = if (c1 >= 'A' and c1 <= 'Z') c1 + 32 else c1;
        const l2: u8 = if (c2 >= 'A' and c2 <= 'Z') c2 + 32 else c2;
        if (l1 != l2) return false;
    }
    return true;
}

/// Temperature units supported by the converter
pub const TemperatureUnit = enum {
    Celsius,
    Fahrenheit,
    Kelvin,

    /// Get the symbol for this unit
    pub fn symbol(self: TemperatureUnit) []const u8 {
        return switch (self) {
            .Celsius => "°C",
            .Fahrenheit => "°F",
            .Kelvin => "K",
        };
    }

    /// Get the full name of this unit
    pub fn name(self: TemperatureUnit) []const u8 {
        return switch (self) {
            .Celsius => "Celsius",
            .Fahrenheit => "Fahrenheit",
            .Kelvin => "Kelvin",
        };
    }

    /// Parse from string (case-insensitive)
    pub fn parse(str: []const u8) ?TemperatureUnit {
        if (equalIgnoreCase(str, "C") or
            equalIgnoreCase(str, "celsius") or
            equalIgnoreCase(str, "°c") or
            equalIgnoreCase(str, "c°"))
        {
            return .Celsius;
        } else if (equalIgnoreCase(str, "F") or
            equalIgnoreCase(str, "fahrenheit") or
            equalIgnoreCase(str, "°f") or
            equalIgnoreCase(str, "f°"))
        {
            return .Fahrenheit;
        } else if (equalIgnoreCase(str, "K") or
            equalIgnoreCase(str, "kelvin"))
        {
            return .Kelvin;
        }
        return null;
    }
};

// ============================================================================
// Temperature Conversion Functions
// ============================================================================

/// Convert Celsius to Fahrenheit
pub fn celsiusToFahrenheit(celsius: f64) f64 {
    return celsius * 9.0 / 5.0 + 32.0;
}

/// Convert Celsius to Kelvin
pub fn celsiusToKelvin(celsius: f64) f64 {
    return celsius + 273.15;
}

/// Convert Fahrenheit to Celsius
pub fn fahrenheitToCelsius(fahrenheit: f64) f64 {
    return (fahrenheit - 32.0) * 5.0 / 9.0;
}

/// Convert Fahrenheit to Kelvin
pub fn fahrenheitToKelvin(fahrenheit: f64) f64 {
    return (fahrenheit - 32.0) * 5.0 / 9.0 + 273.15;
}

/// Convert Kelvin to Celsius
pub fn kelvinToCelsius(kelvin: f64) f64 {
    return kelvin - 273.15;
}

/// Convert Kelvin to Fahrenheit
pub fn kelvinToFahrenheit(kelvin: f64) f64 {
    return (kelvin - 273.15) * 9.0 / 5.0 + 32.0;
}

/// Convert any temperature to any other unit
pub fn convert(value: f64, from: TemperatureUnit, to: TemperatureUnit) f64 {
    if (from == to) return value;

    // First convert to Celsius as intermediate
    const celsius: f64 = switch (from) {
        .Celsius => value,
        .Fahrenheit => fahrenheitToCelsius(value),
        .Kelvin => kelvinToCelsius(value),
    };

    // Then convert from Celsius to target
    return switch (to) {
        .Celsius => celsius,
        .Fahrenheit => celsiusToFahrenheit(celsius),
        .Kelvin => celsiusToKelvin(celsius),
    };
}

/// Convert any temperature to any other unit with validation
pub fn convertSafe(value: f64, from: TemperatureUnit, to: TemperatureUnit) TemperatureError!f64 {
    // Check for absolute zero violations
    const min_kelvin: f64 = switch (from) {
        .Celsius => celsiusToKelvin(value),
        .Fahrenheit => fahrenheitToKelvin(value),
        .Kelvin => value,
    };

    if (min_kelvin < 0) {
        return TemperatureError.AbsoluteZeroViolation;
    }

    // Check for NaN or Inf
    if (std.math.isNan(value) or std.math.isInf(value)) {
        return TemperatureError.InvalidTemperature;
    }

    return convert(value, from, to);
}

// ============================================================================
// Temperature Range Functions
// ============================================================================

/// Temperature range with min and max values
pub const TemperatureRange = struct {
    min: f64,
    max: f64,
    unit: TemperatureUnit,

    /// Create a new temperature range
    pub fn init(min: f64, max: f64, unit: TemperatureUnit) TemperatureRange {
        return .{ .min = min, .max = max, .unit = unit };
    }

    /// Convert range to another unit
    pub fn toUnit(self: TemperatureRange, target: TemperatureUnit) TemperatureRange {
        return .{
            .min = convert(self.min, self.unit, target),
            .max = convert(self.max, self.unit, target),
            .unit = target,
        };
    }

    /// Check if a temperature is within this range
    pub fn contains(self: TemperatureRange, temp: f64) bool {
        return temp >= self.min and temp <= self.max;
    }

    /// Get the midpoint of the range
    pub fn midpoint(self: TemperatureRange) f64 {
        return (self.min + self.max) / 2.0;
    }

    /// Get the size of the range
    pub fn size(self: TemperatureRange) f64 {
        return self.max - self.min;
    }
};

// ============================================================================
// Common Temperature Constants
// ============================================================================

/// Common temperature reference points
pub const temperatures = struct {
    /// Absolute zero in Kelvin
    pub const absolute_zero_kelvin: f64 = 0.0;
    /// Absolute zero in Celsius
    pub const absolute_zero_celsius: f64 = -273.15;
    /// Absolute zero in Fahrenheit
    pub const absolute_zero_fahrenheit: f64 = -459.67;

    /// Water freezing point in Celsius
    pub const water_freezing_celsius: f64 = 0.0;
    /// Water freezing point in Fahrenheit
    pub const water_freezing_fahrenheit: f64 = 32.0;
    /// Water freezing point in Kelvin
    pub const water_freezing_kelvin: f64 = 273.15;

    /// Water boiling point in Celsius
    pub const water_boiling_celsius: f64 = 100.0;
    /// Water boiling point in Fahrenheit
    pub const water_boiling_fahrenheit: f64 = 212.0;
    /// Water boiling point in Kelvin
    pub const water_boiling_kelvin: f64 = 373.15;

    /// Human body temperature (normal) in Celsius
    pub const human_body_celsius: f64 = 37.0;
    /// Human body temperature (normal) in Fahrenheit
    pub const human_body_fahrenheit: f64 = 98.6;
    /// Human body temperature (normal) in Kelvin
    pub const human_body_kelvin: f64 = 310.15;

    /// Room temperature in Celsius
    pub const room_temp_celsius: f64 = 20.0;
    /// Room temperature in Fahrenheit
    pub const room_temp_fahrenheit: f64 = 68.0;
    /// Room temperature in Kelvin
    pub const room_temp_kelvin: f64 = 293.15;
};

// ============================================================================
// Temperature Classification Functions
// ============================================================================

/// Temperature category based on human comfort
pub const TemperatureCategory = enum {
    Freezing,
    Cold,
    Cool,
    Comfortable,
    Warm,
    Hot,
    VeryHot,
    ExtremeHeat,

    /// Get a human-readable description
    pub fn description(self: TemperatureCategory) []const u8 {
        return switch (self) {
            .Freezing => "Below freezing, dress warmly!",
            .Cold => "Cold weather, wear layers",
            .Cool => "Cool, light jacket recommended",
            .Comfortable => "Comfortable room temperature",
            .Warm => "Warm weather",
            .Hot => "Hot, stay hydrated",
            .VeryHot => "Very hot, avoid prolonged sun exposure",
            .ExtremeHeat => "Extreme heat, stay indoors",
        };
    }
};

/// Classify a Celsius temperature
pub fn classifyCelsius(celsius: f64) TemperatureCategory {
    if (celsius < 0) return .Freezing;
    if (celsius < 10) return .Cold;
    if (celsius < 18) return .Cool;
    if (celsius < 24) return .Comfortable;
    if (celsius < 30) return .Warm;
    if (celsius < 38) return .Hot;
    if (celsius < 45) return .VeryHot;
    return .ExtremeHeat;
}

/// Classify a Fahrenheit temperature
pub fn classifyFahrenheit(fahrenheit: f64) TemperatureCategory {
    if (fahrenheit < 32) return .Freezing;
    if (fahrenheit < 50) return .Cold;
    if (fahrenheit < 64) return .Cool;
    if (fahrenheit < 75) return .Comfortable;
    if (fahrenheit < 86) return .Warm;
    if (fahrenheit < 100) return .Hot;
    if (fahrenheit < 113) return .VeryHot;
    return .ExtremeHeat;
}

/// Classify a Kelvin temperature
pub fn classifyKelvin(kelvin: f64) TemperatureCategory {
    return classifyCelsius(kelvinToCelsius(kelvin));
}

// ============================================================================
// Temperature Comparison Functions
// ============================================================================

/// Compare two temperatures (returns -1, 0, or 1)
pub fn compare(temp1: f64, unit1: TemperatureUnit, temp2: f64, unit2: TemperatureUnit) i8 {
    // Convert both to Kelvin for comparison
    const k1: f64 = switch (unit1) {
        .Celsius => celsiusToKelvin(temp1),
        .Fahrenheit => fahrenheitToKelvin(temp1),
        .Kelvin => temp1,
    };
    const k2: f64 = switch (unit2) {
        .Celsius => celsiusToKelvin(temp2),
        .Fahrenheit => fahrenheitToKelvin(temp2),
        .Kelvin => temp2,
    };

    if (k1 < k2) return -1;
    if (k1 > k2) return 1;
    return 0;
}

/// Check if two temperatures are equal (within tolerance)
pub fn equal(temp1: f64, unit1: TemperatureUnit, temp2: f64, unit2: TemperatureUnit, tolerance: f64) bool {
    const diff = @abs(convert(temp1, unit1, unit2) - temp2);
    return diff <= tolerance;
}

// ============================================================================
// Temperature String Formatting
// ============================================================================

/// Format temperature with unit (precision is fixed at 1 decimal place)
pub fn formatTemperature(allocator: std.mem.Allocator, value: f64, unit: TemperatureUnit, precision: usize) ![]u8 {
    _ = precision; // Precision is reserved for future use; currently fixed at 1 decimal
    var buf: [64]u8 = undefined;
    const formatted = switch (unit) {
        .Celsius => try std.fmt.bufPrint(&buf, "{d:.1}°C", .{value}),
        .Fahrenheit => try std.fmt.bufPrint(&buf, "{d:.1}°F", .{value}),
        .Kelvin => try std.fmt.bufPrint(&buf, "{d:.1} K", .{value}),
    };
    return allocator.dupe(u8, formatted);
}

/// Parse temperature from string (e.g., "25°C", "77F", "300K")
pub fn parseTemperature(str: []const u8) ?struct { value: f64, unit: TemperatureUnit } {
    var start: usize = 0;
    var end: usize = str.len;

    // Skip leading whitespace
    while (start < end and (str[start] == ' ' or str[start] == '\t')) {
        start += 1;
    }

    // Skip trailing whitespace
    while (end > start and (str[end - 1] == ' ' or str[end - 1] == '\t')) {
        end -= 1;
    }

    // Skip leading +/-
    const negative = if (start < end and str[start] == '-') blk: {
        start += 1;
        break :blk true;
    } else false;

    if (start < end and str[start] == '+') {
        start += 1;
    }

    // Find where number ends
    var num_end: usize = start;
    while (num_end < end and ((str[num_end] >= '0' and str[num_end] <= '9') or str[num_end] == '.')) {
        num_end += 1;
    }

    if (num_end == start) return null;

    // Parse number
    const num_str = str[start..num_end];
    const value = std.fmt.parseFloat(f64, num_str) catch return null;
    const signed_value = if (negative) -value else value;

    // Skip degree symbol if present
    if (num_end < end and str[num_end] == '°') {
        num_end += 1;
    }

    // Skip whitespace before unit
    while (num_end < end and (str[num_end] == ' ' or str[num_end] == '\t')) {
        num_end += 1;
    }

    // Parse unit
    const unit_str = str[num_end..end];
    const unit = TemperatureUnit.parse(unit_str) orelse return null;

    return .{ .value = signed_value, .unit = unit };
}

// ============================================================================
// Temperature Arithmetic
// ============================================================================

/// Add temperatures (result in first temperature's unit)
pub fn add(temp1: f64, unit1: TemperatureUnit, temp2: f64, unit2: TemperatureUnit) f64 {
    const temp2_in_unit1 = convert(temp2, unit2, unit1);
    return temp1 + temp2_in_unit1;
}

/// Subtract temperatures (result in first temperature's unit)
pub fn subtract(temp1: f64, unit1: TemperatureUnit, temp2: f64, unit2: TemperatureUnit) f64 {
    const temp2_in_unit1 = convert(temp2, unit2, unit1);
    return temp1 - temp2_in_unit1;
}

/// Average of multiple temperatures (all must be in the same unit)
/// The unit parameter is for documentation purposes - callers should ensure all temps are in this unit
pub fn average(temps: []const f64, unit: TemperatureUnit) f64 {
    _ = unit; // Unit is for caller documentation - averaging doesn't change the unit
    if (temps.len == 0) return 0.0;
    var sum: f64 = 0.0;
    for (temps) |t| {
        sum += t;
    }
    return sum / @as(f64, @floatFromInt(temps.len));
}

/// Convert multiple temperatures to target unit
pub fn convertAll(allocator: std.mem.Allocator, temps: []const f64, from: TemperatureUnit, to: TemperatureUnit) ![]f64 {
    const result = try allocator.alloc(f64, temps.len);
    for (temps, 0..) |t, i| {
        result[i] = convert(t, from, to);
    }
    return result;
}

// ============================================================================
// Wind Chill and Heat Index
// ============================================================================

/// Calculate wind chill temperature (Celsius)
/// Valid for temperatures <= 10°C and wind speeds >= 4.8 km/h
pub fn windChillCelsius(temp_celsius: f64, wind_speed_kmh: f64) ?f64 {
    if (temp_celsius > 10.0 or wind_speed_kmh < 4.8) {
        return null; // Formula not valid outside these conditions
    }
    // North American wind chill formula
    return 13.12 + 0.6215 * temp_celsius - 11.37 * std.math.pow(f64, wind_speed_kmh, 0.16) + 0.3965 * temp_celsius * std.math.pow(f64, wind_speed_kmh, 0.16);
}

/// Calculate wind chill temperature (Fahrenheit)
/// Valid for temperatures <= 50°F and wind speeds >= 3 mph
pub fn windChillFahrenheit(temp_fahrenheit: f64, wind_speed_mph: f64) ?f64 {
    if (temp_fahrenheit > 50.0 or wind_speed_mph < 3.0) {
        return null;
    }
    return 35.74 + 0.6215 * temp_fahrenheit - 35.75 * std.math.pow(f64, wind_speed_mph, 0.16) + 0.4275 * temp_fahrenheit * std.math.pow(f64, wind_speed_mph, 0.16);
}

/// Calculate heat index (Fahrenheit)
/// Valid for temperatures >= 80°F and relative humidity >= 40%
pub fn heatIndexFahrenheit(temp_fahrenheit: f64, relative_humidity: f64) ?f64 {
    if (temp_fahrenheit < 80.0 or relative_humidity < 40.0) {
        return null;
    }
    // Simplified heat index formula
    const tf = temp_fahrenheit;
    const rh = relative_humidity;

    const hi = -42.379 + 2.04901523 * tf + 10.14333127 * rh -
        0.22475541 * tf * rh - 0.00683783 * tf * tf -
        0.05481717 * rh * rh + 0.00122874 * tf * tf * rh +
        0.00085282 * tf * rh * rh - 0.00000199 * tf * tf * rh * rh;

    return hi;
}

/// Calculate heat index (Celsius)
pub fn heatIndexCelsius(temp_celsius: f64, relative_humidity: f64) ?f64 {
    const temp_f = celsiusToFahrenheit(temp_celsius);
    const hi_f = heatIndexFahrenheit(temp_f, relative_humidity) orelse return null;
    return fahrenheitToCelsius(hi_f);
}

// ============================================================================
// Tests
// ============================================================================

test "TemperatureUnit symbol and name" {
    try std.testing.expectEqualStrings("°C", TemperatureUnit.Celsius.symbol());
    try std.testing.expectEqualStrings("°F", TemperatureUnit.Fahrenheit.symbol());
    try std.testing.expectEqualStrings("K", TemperatureUnit.Kelvin.symbol());

    try std.testing.expectEqualStrings("Celsius", TemperatureUnit.Celsius.name());
    try std.testing.expectEqualStrings("Fahrenheit", TemperatureUnit.Fahrenheit.name());
    try std.testing.expectEqualStrings("Kelvin", TemperatureUnit.Kelvin.name());
}

test "TemperatureUnit parse" {
    try std.testing.expectEqual(TemperatureUnit.Celsius, TemperatureUnit.parse("C").?);
    try std.testing.expectEqual(TemperatureUnit.Celsius, TemperatureUnit.parse("celsius").?);
    try std.testing.expectEqual(TemperatureUnit.Celsius, TemperatureUnit.parse("°C").?);

    try std.testing.expectEqual(TemperatureUnit.Fahrenheit, TemperatureUnit.parse("F").?);
    try std.testing.expectEqual(TemperatureUnit.Fahrenheit, TemperatureUnit.parse("fahrenheit").?);

    try std.testing.expectEqual(TemperatureUnit.Kelvin, TemperatureUnit.parse("K").?);
    try std.testing.expectEqual(TemperatureUnit.Kelvin, TemperatureUnit.parse("kelvin").?);

    try std.testing.expect(TemperatureUnit.parse("invalid") == null);
}

test "Celsius to Fahrenheit" {
    try std.testing.expectApproxEqAbs(@as(f64, 32.0), celsiusToFahrenheit(0.0), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 212.0), celsiusToFahrenheit(100.0), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 98.6), celsiusToFahrenheit(37.0), 0.1);
}

test "Celsius to Kelvin" {
    try std.testing.expectApproxEqAbs(@as(f64, 273.15), celsiusToKelvin(0.0), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 373.15), celsiusToKelvin(100.0), 0.001);
}

test "Fahrenheit to Celsius" {
    try std.testing.expectApproxEqAbs(@as(f64, 0.0), fahrenheitToCelsius(32.0), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 100.0), fahrenheitToCelsius(212.0), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, -17.7778), fahrenheitToCelsius(0.0), 0.01);
}

test "Fahrenheit to Kelvin" {
    try std.testing.expectApproxEqAbs(@as(f64, 273.15), fahrenheitToKelvin(32.0), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 373.15), fahrenheitToKelvin(212.0), 0.001);
}

test "Kelvin to Celsius" {
    try std.testing.expectApproxEqAbs(@as(f64, 0.0), kelvinToCelsius(273.15), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 100.0), kelvinToCelsius(373.15), 0.001);
}

test "Kelvin to Fahrenheit" {
    try std.testing.expectApproxEqAbs(@as(f64, 32.0), kelvinToFahrenheit(273.15), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 212.0), kelvinToFahrenheit(373.15), 0.001);
}

test "convert" {
    try std.testing.expectApproxEqAbs(@as(f64, 32.0), convert(0.0, .Celsius, .Fahrenheit), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 273.15), convert(0.0, .Celsius, .Kelvin), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 0.0), convert(32.0, .Fahrenheit, .Celsius), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 0.0), convert(273.15, .Kelvin, .Celsius), 0.001);

    // Same unit conversion
    try std.testing.expectApproxEqAbs(@as(f64, 25.0), convert(25.0, .Celsius, .Celsius), 0.001);
}

test "convertSafe" {
    // Valid conversions
    const result = try convertSafe(0.0, .Celsius, .Fahrenheit);
    try std.testing.expectApproxEqAbs(@as(f64, 32.0), result, 0.001);

    // Absolute zero violation
    const err_result = convertSafe(-300.0, .Celsius, .Fahrenheit);
    try std.testing.expectError(TemperatureError.AbsoluteZeroViolation, err_result);

    // Invalid (NaN)
    const nan_result = convertSafe(std.math.nan(f64), .Celsius, .Fahrenheit);
    try std.testing.expectError(TemperatureError.InvalidTemperature, nan_result);
}

test "TemperatureRange" {
    const range = TemperatureRange.init(0.0, 100.0, .Celsius);

    try std.testing.expect(range.contains(50.0));
    try std.testing.expect(range.contains(0.0));
    try std.testing.expect(range.contains(100.0));
    try std.testing.expect(!range.contains(-1.0));
    try std.testing.expect(!range.contains(101.0));

    try std.testing.expectApproxEqAbs(@as(f64, 50.0), range.midpoint(), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 100.0), range.size(), 0.001);

    const f_range = range.toUnit(.Fahrenheit);
    try std.testing.expectApproxEqAbs(@as(f64, 32.0), f_range.min, 0.1);
    try std.testing.expectApproxEqAbs(@as(f64, 212.0), f_range.max, 0.1);
}

test "classifyCelsius" {
    try std.testing.expectEqual(TemperatureCategory.Freezing, classifyCelsius(-10.0));
    try std.testing.expectEqual(TemperatureCategory.Cold, classifyCelsius(5.0));
    try std.testing.expectEqual(TemperatureCategory.Cool, classifyCelsius(15.0));
    try std.testing.expectEqual(TemperatureCategory.Comfortable, classifyCelsius(22.0));
    try std.testing.expectEqual(TemperatureCategory.Warm, classifyCelsius(28.0));
    try std.testing.expectEqual(TemperatureCategory.Hot, classifyCelsius(35.0));
    try std.testing.expectEqual(TemperatureCategory.VeryHot, classifyCelsius(42.0));
    try std.testing.expectEqual(TemperatureCategory.ExtremeHeat, classifyCelsius(50.0));
}

test "classifyFahrenheit" {
    try std.testing.expectEqual(TemperatureCategory.Freezing, classifyFahrenheit(20.0));
    try std.testing.expectEqual(TemperatureCategory.Comfortable, classifyFahrenheit(72.0));
    try std.testing.expectEqual(TemperatureCategory.Hot, classifyFahrenheit(95.0));
}

test "compare" {
    try std.testing.expectEqual(@as(i8, 0), compare(0.0, .Celsius, 32.0, .Fahrenheit));
    try std.testing.expectEqual(@as(i8, 0), compare(0.0, .Celsius, 273.15, .Kelvin));
    try std.testing.expectEqual(@as(i8, -1), compare(0.0, .Celsius, 100.0, .Celsius));
    try std.testing.expectEqual(@as(i8, 1), compare(100.0, .Celsius, 0.0, .Fahrenheit));
}

test "equal" {
    try std.testing.expect(equal(0.0, .Celsius, 32.0, .Fahrenheit, 0.01));
    try std.testing.expect(equal(0.0, .Celsius, 273.15, .Kelvin, 0.01));
    try std.testing.expect(!equal(0.0, .Celsius, 30.0, .Fahrenheit, 0.01));
}

test "parseTemperature" {
    const result1 = parseTemperature("25°C").?;
    try std.testing.expectApproxEqAbs(@as(f64, 25.0), result1.value, 0.001);
    try std.testing.expectEqual(TemperatureUnit.Celsius, result1.unit);

    const result2 = parseTemperature("77 F").?;
    try std.testing.expectApproxEqAbs(@as(f64, 77.0), result2.value, 0.001);
    try std.testing.expectEqual(TemperatureUnit.Fahrenheit, result2.unit);

    const result3 = parseTemperature("300K").?;
    try std.testing.expectApproxEqAbs(@as(f64, 300.0), result3.value, 0.001);
    try std.testing.expectEqual(TemperatureUnit.Kelvin, result3.unit);

    const result4 = parseTemperature("-10 celsius").?;
    try std.testing.expectApproxEqAbs(@as(f64, -10.0), result4.value, 0.001);
    try std.testing.expectEqual(TemperatureUnit.Celsius, result4.unit);

    try std.testing.expect(parseTemperature("invalid") == null);
}

test "add and subtract" {
    const result1 = add(10.0, .Celsius, 20.0, .Celsius);
    try std.testing.expectApproxEqAbs(@as(f64, 30.0), result1, 0.001);

    const result2 = subtract(30.0, .Celsius, 10.0, .Celsius);
    try std.testing.expectApproxEqAbs(@as(f64, 20.0), result2, 0.001);

    // Mixed units
    const result3 = add(0.0, .Celsius, 32.0, .Fahrenheit);
    try std.testing.expectApproxEqAbs(@as(f64, 0.0), result3, 0.001);
}

test "average" {
    const temps = [_]f64{ 20.0, 22.0, 24.0, 26.0 };
    const avg = average(&temps, .Celsius);
    try std.testing.expectApproxEqAbs(@as(f64, 23.0), avg, 0.001);
}

test "windChillFahrenheit" {
    // Wind chill should be lower than actual temperature
    const wc = windChillFahrenheit(30.0, 15.0).?;
    try std.testing.expect(wc < 30.0);

    // Invalid conditions return null
    try std.testing.expect(windChillFahrenheit(60.0, 15.0) == null);
    try std.testing.expect(windChillFahrenheit(30.0, 2.0) == null);
}

test "heatIndexFahrenheit" {
    // Heat index should be higher than actual temperature
    const hi = heatIndexFahrenheit(90.0, 70.0).?;
    try std.testing.expect(hi > 90.0);

    // Invalid conditions return null
    try std.testing.expect(heatIndexFahrenheit(70.0, 50.0) == null);
    try std.testing.expect(heatIndexFahrenheit(90.0, 30.0) == null);
}

test "temperatures constants" {
    try std.testing.expectApproxEqAbs(@as(f64, -273.15), temperatures.absolute_zero_celsius, 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, -459.67), temperatures.absolute_zero_fahrenheit, 0.01);
    try std.testing.expectApproxEqAbs(@as(f64, 0.0), temperatures.water_freezing_celsius, 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 100.0), temperatures.water_boiling_celsius, 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 37.0), temperatures.human_body_celsius, 0.001);
}

test "formatTemperature" {
    const allocator = std.testing.allocator;

    const result1 = try formatTemperature(allocator, 25.5, .Celsius, 1);
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("25.5°C", result1);

    const result2 = try formatTemperature(allocator, 77.0, .Fahrenheit, 1);
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("77.0°F", result2);

    const result3 = try formatTemperature(allocator, 300.0, .Kelvin, 1);
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("300.0 K", result3);
}

test "convertAll" {
    const allocator = std.testing.allocator;

    const temps = [_]f64{ 0.0, 100.0, 37.0 };
    const converted = try convertAll(allocator, &temps, .Celsius, .Fahrenheit);
    defer allocator.free(converted);

    try std.testing.expectApproxEqAbs(@as(f64, 32.0), converted[0], 0.1);
    try std.testing.expectApproxEqAbs(@as(f64, 212.0), converted[1], 0.1);
    try std.testing.expectApproxEqAbs(@as(f64, 98.6), converted[2], 0.1);
}