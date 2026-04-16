const std = @import("std");
const temp_conv = @import("temperature_converter");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("\n=== Temperature Converter Demo ===\n\n", .{});

    // Basic conversions
    std.debug.print("--- Basic Conversions ---\n", .{});
    std.debug.print("0°C = {d:.1}°F (Freezing point of water)\n", .{temp_conv.celsiusToFahrenheit(0.0)});
    std.debug.print("100°C = {d:.1}°F (Boiling point of water)\n", .{temp_conv.celsiusToFahrenheit(100.0)});
    std.debug.print("37°C = {d:.1}°F (Human body temperature)\n", .{temp_conv.celsiusToFahrenheit(37.0)});
    std.debug.print("25°C = {d:.1}°K (Room temperature)\n", .{temp_conv.celsiusToKelvin(25.0)});
    std.debug.print("\n", .{});

    // Universal convert function
    std.debug.print("--- Universal Convert Function ---\n", .{});
    std.debug.print("Convert 0°C to Fahrenheit: {d:.1}°F\n", .{temp_conv.convert(0.0, .Celsius, .Fahrenheit)});
    std.debug.print("Convert 0°C to Kelvin: {d:.1}K\n", .{temp_conv.convert(0.0, .Celsius, .Kelvin)});
    std.debug.print("Convert 212°F to Celsius: {d:.1}°C\n", .{temp_conv.convert(212.0, .Fahrenheit, .Celsius)});
    std.debug.print("Convert 273.15K to Fahrenheit: {d:.1}°F\n", .{temp_conv.convert(273.15, .Kelvin, .Fahrenheit)});
    std.debug.print("\n", .{});

    // Temperature parsing
    std.debug.print("--- Temperature Parsing ---\n", .{});
    const examples = [_][]const u8{ "25°C", "77°F", "300K", "-10 celsius", "0F" };
    for (examples) |str| {
        if (temp_conv.parseTemperature(str)) |parsed| {
            const formatted = try temp_conv.formatTemperature(allocator, parsed.value, parsed.unit, 1);
            defer allocator.free(formatted);
            std.debug.print("Parsed '{s}' -> {s}\n", .{ str, formatted });
        } else {
            std.debug.print("Failed to parse '{s}'\n", .{str});
        }
    }
    std.debug.print("\n", .{});

    // Temperature classification
    std.debug.print("--- Temperature Classification ---\n", .{});
    const temps = [_]f64{ -5.0, 5.0, 15.0, 22.0, 28.0, 35.0, 42.0, 50.0 };
    for (temps) |t| {
        const category = temp_conv.classifyCelsius(t);
        const f = temp_conv.celsiusToFahrenheit(t);
        std.debug.print("{d:.0}°C ({d:.0}°F) -> {s}: {s}\n", .{
            t, f,
            @tagName(category),
            category.description(),
        });
    }
    std.debug.print("\n", .{});

    // Temperature range
    std.debug.print("--- Temperature Range ---\n", .{});
    const comfort_range = temp_conv.TemperatureRange.init(18.0, 26.0, .Celsius);
    std.debug.print("Comfort range: {d:.0}°C to {d:.0}°C\n", .{ comfort_range.min, comfort_range.max });

    const f_range = comfort_range.toUnit(.Fahrenheit);
    std.debug.print("In Fahrenheit: {d:.0}°F to {d:.0}°F\n", .{ f_range.min, f_range.max });

    std.debug.print("Is 20°C comfortable? {}\n", .{comfort_range.contains(20.0)});
    std.debug.print("Is 30°C comfortable? {}\n", .{comfort_range.contains(30.0)});
    std.debug.print("\n", .{});

    // Temperature arithmetic
    std.debug.print("--- Temperature Arithmetic ---\n", .{});
    const avg = temp_conv.average(&[_]f64{ 18.0, 22.0, 24.0, 20.0 }, .Celsius);
    std.debug.print("Average of [18,22,24,20]°C: {d:.1}°C\n", .{avg});

    const sum = temp_conv.add(10.0, .Celsius, 5.0, .Celsius);
    std.debug.print("10°C + 5°C = {d:.0}°C\n", .{sum});

    // Mixed units
    const mixed = temp_conv.add(0.0, .Celsius, 32.0, .Fahrenheit);
    std.debug.print("0°C + 32°F (in Celsius) = {d:.0}°C\n", .{mixed});
    std.debug.print("\n", .{});

    // Wind chill
    std.debug.print("--- Wind Chill ---\n", .{});
    const wc = temp_conv.windChillFahrenheit(30.0, 15.0);
    if (wc) |value| {
        std.debug.print("At 30°F with 15 mph wind, feels like: {d:.1}°F\n", .{value});
    }

    const wc_c = temp_conv.windChillCelsius(-10.0, 25.0);
    if (wc_c) |value| {
        std.debug.print("At -10°C with 25 km/h wind, feels like: {d:.1}°C\n", .{value});
    }
    std.debug.print("\n", .{});

    // Heat index
    std.debug.print("--- Heat Index ---\n", .{});
    const hi = temp_conv.heatIndexFahrenheit(90.0, 70.0);
    if (hi) |value| {
        std.debug.print("At 90°F with 70% humidity, feels like: {d:.1}°F\n", .{value});
    }

    const hi_c = temp_conv.heatIndexCelsius(35.0, 80.0);
    if (hi_c) |value| {
        std.debug.print("At 35°C with 80% humidity, feels like: {d:.1}°C\n", .{value});
    }
    std.debug.print("\n", .{});

    // Temperature comparison
    std.debug.print("--- Temperature Comparison ---\n", .{});
    const cmp1 = temp_conv.compare(0.0, .Celsius, 32.0, .Fahrenheit);
    std.debug.print("0°C vs 32°F: {} (should be 0, equal)\n", .{cmp1});

    const cmp2 = temp_conv.compare(100.0, .Celsius, 0.0, .Fahrenheit);
    std.debug.print("100°C vs 0°F: {} (should be 1, greater)\n", .{cmp2});

    const cmp3 = temp_conv.compare(0.0, .Celsius, 100.0, .Celsius);
    std.debug.print("0°C vs 100°C: {} (should be -1, less)\n", .{cmp3});
    std.debug.print("\n", .{});

    // Safe conversion
    std.debug.print("--- Safe Conversion ---\n", .{});
    const safe1 = temp_conv.convertSafe(25.0, .Celsius, .Fahrenheit);
    std.debug.print("Safe conversion of 25°C: ", .{});
    if (safe1) |val| {
        std.debug.print("{d:.1}°F\n", .{val});
    } else |err| {
        std.debug.print("Error: {}\n", .{err});
    }

    const safe2 = temp_conv.convertSafe(-300.0, .Celsius, .Fahrenheit);
    std.debug.print("Safe conversion of -300°C: ", .{});
    if (safe2) |val| {
        std.debug.print("{d:.1}°F\n", .{val});
    } else |err| {
        std.debug.print("Error: {} (below absolute zero)\n", .{err});
    }
    std.debug.print("\n", .{});

    // Constants
    std.debug.print("--- Temperature Constants ---\n", .{});
    std.debug.print("Absolute zero: {d:.2}°C, {d:.2}°F, {d:.2}K\n", .{
        temp_conv.temperatures.absolute_zero_celsius,
        temp_conv.temperatures.absolute_zero_fahrenheit,
        temp_conv.temperatures.absolute_zero_kelvin,
    });
    std.debug.print("Water freezing: {d:.0}°C, {d:.0}°F, {d:.2}K\n", .{
        temp_conv.temperatures.water_freezing_celsius,
        temp_conv.temperatures.water_freezing_fahrenheit,
        temp_conv.temperatures.water_freezing_kelvin,
    });
    std.debug.print("Water boiling: {d:.0}°C, {d:.0}°F, {d:.2}K\n", .{
        temp_conv.temperatures.water_boiling_celsius,
        temp_conv.temperatures.water_boiling_fahrenheit,
        temp_conv.temperatures.water_boiling_kelvin,
    });
    std.debug.print("Human body: {d:.0}°C, {d:.1}°F, {d:.2}K\n", .{
        temp_conv.temperatures.human_body_celsius,
        temp_conv.temperatures.human_body_fahrenheit,
        temp_conv.temperatures.human_body_kelvin,
    });

    std.debug.print("\n=== Demo Complete ===\n", .{});
}