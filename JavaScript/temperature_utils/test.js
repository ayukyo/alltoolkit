/**
 * Temperature Utils Tests - 温度工具测试
 * 
 * 测试所有功能的正确性。
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

const {
    TemperatureUnit,
    UnitInfo,
    ComfortLevel,
    WeatherCategory,
    Temperature,
    TemperatureRange,
    TemperatureUtils,
    celsius,
    fahrenheit,
    kelvin,
    convert,
    convertAll
} = require('./mod.js');

// 测试计数器
let passed = 0;
let failed = 0;

/**
 * 测试函数
 */
function test(name, condition) {
    if (condition) {
        console.log(`✅ PASS: ${name}`);
        passed++;
    } else {
        console.log(`❌ FAIL: ${name}`);
        failed++;
    }
}

/**
 * 测试近似相等
 */
function testApprox(name, value, expected, tolerance = 0.01) {
    const diff = Math.abs(value - expected);
    test(name, diff <= tolerance);
}

// 边界分隔符
function separator(title) {
    console.log('\n' + '='.repeat(60));
    console.log(title);
    console.log('='.repeat(60));
}

function subSeparator(title) {
    console.log('\n' + title);
    console.log('-'.repeat(40));
}

// 运行测试
function runTests() {
    separator('TemperatureUtils Tests');
    
    // MARK: - TemperatureUnit Tests
    
    subSeparator('TemperatureUnit Tests:');
    
    test('Celsius symbol', UnitInfo[TemperatureUnit.CELSIUS].symbol === '°C');
    test('Fahrenheit symbol', UnitInfo[TemperatureUnit.FAHRENHEIT].symbol === '°F');
    test('Kelvin symbol', UnitInfo[TemperatureUnit.KELVIN].symbol === 'K');
    test('Kelvin is absolute', UnitInfo[TemperatureUnit.KELVIN].isAbsolute === true);
    test('Celsius is not absolute', UnitInfo[TemperatureUnit.CELSIUS].isAbsolute === false);
    
    // MARK: - Temperature Creation Tests
    
    subSeparator('Temperature Creation Tests:');
    
    const tempCelsius = celsius(25);
    test('Celsius creation value', tempCelsius.value === 25);
    test('Celsius creation unit', tempCelsius.unit === TemperatureUnit.CELSIUS);
    
    const tempFahrenheit = fahrenheit(100);
    test('Fahrenheit creation value', tempFahrenheit.value === 100);
    test('Fahrenheit creation unit', tempFahrenheit.unit === TemperatureUnit.FAHRENHEIT);
    
    const tempKelvin = kelvin(300);
    test('Kelvin creation value', tempKelvin.value === 300);
    test('Kelvin creation unit', tempKelvin.unit === TemperatureUnit.KELVIN);
    
    // MARK: - Conversion Tests
    
    subSeparator('Conversion Tests:');
    
    // Celsius to Fahrenheit
    testApprox('0°C -> 32°F', celsius(0).toFahrenheit().value, 32);
    testApprox('100°C -> 212°F', celsius(100).toFahrenheit().value, 212);
    testApprox('-40°C -> -40°F', celsius(-40).toFahrenheit().value, -40);
    
    // Fahrenheit to Celsius
    testApprox('32°F -> 0°C', fahrenheit(32).toCelsius().value, 0);
    testApprox('212°F -> 100°C', fahrenheit(212).toCelsius().value, 100);
    
    // Celsius to Kelvin
    testApprox('0°C -> 273.15K', celsius(0).toKelvin().value, 273.15);
    testApprox('-273.15°C -> 0K', celsius(-273.15).toKelvin().value, 0);
    
    // Kelvin to Celsius
    testApprox('0K -> -273.15°C', kelvin(0).toCelsius().value, -273.15);
    testApprox('373.15K -> 100°C', kelvin(373.15).toCelsius().value, 100);
    
    // Celsius to Rankine
    testApprox('0°C -> 491.67°R', celsius(0).toRankine().value, 491.67);
    
    // Celsius to Delisle
    testApprox('100°C -> 0°De', celsius(100).toDelisle().value, 0);
    testApprox('0°C -> 150°De', celsius(0).toDelisle().value, 150);
    
    // Celsius to Newton
    test('0°C -> 0°N', celsius(0).toNewton().value === 0);
    testApprox('33°C -> 10.89°N', celsius(33).toNewton().value, 10.89);
    
    // Celsius to Réaumur
    test('0°C -> 0°Ré', celsius(0).toReaumur().value === 0);
    test('80°C -> 64°Ré', celsius(80).toReaumur().value === 64);
    
    // Celsius to Rømer
    test('0°C -> 7.5°Rø', celsius(0).toRomer().value === 7.5);
    
    // MARK: - Temperature Comparison Tests
    
    subSeparator('Temperature Comparison Tests:');
    
    const temp1 = celsius(20);
    const temp2 = celsius(30);
    
    test('20°C < 30°C', temp1.lessThan(temp2));
    test('30°C > 20°C', temp2.greaterThan(temp1));
    test('20°C equals 20°C', temp1.equals(celsius(20)));
    test('20°F equals 20°C', fahrenheit(68).equals(celsius(20)));
    
    // MARK: - Temperature Operations Tests
    
    subSeparator('Temperature Operations Tests:');
    
    const plusTest = celsius(20).add(5);
    test('20°C + 5 = 25°C', plusTest.value === 25);
    
    const minusTest = celsius(20).subtract(5);
    test('20°C - 5 = 15°C', minusTest.value === 15);
    
    const diffTest = celsius(30).difference(celsius(20));
    test('30°C - 20°C = 10°C diff', diffTest === 10);
    
    const multTest = celsius(20).multiply(2);
    test('20°C * 2 = 40°C', multTest.value === 40);
    
    const divTest = celsius(20).divide(2);
    test('20°C / 2 = 10°C', divTest.value === 10);
    
    // MARK: - Temperature Properties Tests
    
    subSeparator('Temperature Properties Tests:');
    
    test('-5°C is below freezing', celsius(-5).isBelowFreezing);
    test('5°C is not below freezing', !celsius(5).isBelowFreezing);
    test('105°C is above boiling', celsius(105).isAboveBoiling);
    test('95°C is not above boiling', !celsius(95).isAboveBoiling);
    test('-10°C is negative', celsius(-10).isNegative);
    test('10°C is not negative', !celsius(10).isNegative);
    test('0K is at absolute zero', kelvin(0).isAtOrBelowAbsoluteZero);
    test('-1K is below absolute zero', kelvin(-1).isAtOrBelowAbsoluteZero);
    
    // MARK: - Physical Constants Tests
    
    subSeparator('Physical Constants Tests:');
    
    test('Absolute zero', TemperatureUtils.ABSOLUTE_ZERO.toKelvin().value === 0);
    test('Water freezing point', TemperatureUtils.WATER_FREEZING_POINT.toCelsius().value === 0);
    test('Water boiling point', TemperatureUtils.WATER_BOILING_POINT.toCelsius().value === 100);
    test('Normal body temperature', TemperatureUtils.NORMAL_BODY_TEMPERATURE.toCelsius().value === 37);
    test('Room temperature', TemperatureUtils.ROOM_TEMPERATURE.toCelsius().value === 20);
    
    // MARK: - TemperatureRange Tests
    
    subSeparator('TemperatureRange Tests:');
    
    const range = new TemperatureRange(celsius(0), celsius(100));
    test('Range width', range.width.toCelsius().value === 100);
    test('Range midpoint', range.midpoint.toCelsius().value === 50);
    test('Range contains 50°C', range.contains(celsius(50)));
    test('Range contains 0°C', range.contains(celsius(0)));
    test('Range contains 100°C', range.contains(celsius(100)));
    test('Range does not contain -1°C', !range.contains(celsius(-1)));
    test('Range does not contain 101°C', !range.contains(celsius(101)));
    
    const range2 = new TemperatureRange(celsius(50), celsius(150));
    const union = range.union(range2);
    test('Union lower', union.lower.toCelsius().value === 0);
    test('Union upper', union.upper.toCelsius().value === 150);
    
    const intersection = range.intersection(range2);
    test('Intersection exists', intersection !== null);
    test('Intersection lower', intersection.lower.toCelsius().value === 50);
    test('Intersection upper', intersection.upper.toCelsius().value === 100);
    
    const noIntersection = new TemperatureRange(celsius(0), celsius(50))
        .intersection(new TemperatureRange(celsius(100), celsius(150)));
    test('No intersection', noIntersection === null);
    
    // MARK: - Format Tests
    
    subSeparator('Format Tests:');
    
    test('Formatted 25°C', celsius(25).format() === '25.0°C');
    test('Formatted 0°C precision 2', celsius(0).format(2) === '0.00°C');
    test('Dual format', celsius(25).dualFormat === '25.0°C (77.0°F)');
    test('Format full name', celsius(25).formatFullName() === '25.0 Celsius');
    
    // MARK: - Comfort Level Tests
    
    subSeparator('Comfort Level Tests:');
    
    test('0°C comfort level cold', celsius(0).comfortLevel === ComfortLevel.COLD);
    test('20°C comfort level comfortable', celsius(20).comfortLevel === ComfortLevel.COMFORTABLE);
    test('35°C comfort level hot', celsius(35).comfortLevel === ComfortLevel.HOT);
    test('15°C suitable for outdoor', celsius(15).isSuitableForOutdoor);
    test('5°C not suitable for outdoor', !celsius(5).isSuitableForOutdoor);
    test('10°C needs warm clothing', celsius(10).needsWarmClothing);
    test('25°C does not need warm clothing', !celsius(25).needsWarmClothing);
    test('30°C needs sun protection', celsius(30).needsSunProtection);
    
    // MARK: - Wind Chill Tests
    
    subSeparator('Wind Chill Tests:');
    
    // 公式适用于气温 ≤ 10°C 且风速 > 4.8 km/h
    const windChill1 = celsius(5).windChill(10);
    test('Wind chill reduces temperature', windChill1.toCelsius().value < 5);
    
    // 在高温或低风速下，风寒指数不适用
    const windChill2 = celsius(25).windChill(10);
    test('Wind chill not applied for hot temp', windChill2.toCelsius().value === 25);
    
    const windChill3 = celsius(5).windChill(3);
    test('Wind chill not applied for low wind', windChill3.toCelsius().value === 5);
    
    // MARK: - Heat Index Tests
    
    subSeparator('Heat Index Tests:');
    
    // 公式适用于气温 ≥ 27°C 且湿度 ≥ 40%
    const heatIndex1 = celsius(30).heatIndex(70);
    test('Heat index increases temperature', heatIndex1.toCelsius().value > 30);
    
    // 在低温或低湿度下，体感温度不适用
    const heatIndex2 = celsius(20).heatIndex(70);
    test('Heat index not applied for cold temp', heatIndex2.toCelsius().value === 20);
    
    const heatIndex3 = celsius(30).heatIndex(30);
    test('Heat index not applied for low humidity', heatIndex3.toCelsius().value === 30);
    
    // MARK: - TemperatureUtils Tests
    
    subSeparator('TemperatureUtils Tests:');
    
    // Conversion
    const converted = convert(100, TemperatureUnit.CELSIUS, TemperatureUnit.FAHRENHEIT);
    test('Convert 100°C to Fahrenheit', converted === 212);
    
    const allConversions = convertAll(0, TemperatureUnit.CELSIUS);
    test('All conversions Fahrenheit', allConversions[TemperatureUnit.FAHRENHEIT] === 32);
    testApprox('All conversions Kelvin', allConversions[TemperatureUnit.KELVIN], 273.15);
    
    // Average
    const temps = [celsius(20), celsius(30), celsius(40)];
    const avg = TemperatureUtils.average(temps);
    test('Average temperature', avg.toCelsius().value === 30);
    
    // Median
    const temps2 = [celsius(10), celsius(20), celsius(30)];
    const median = TemperatureUtils.median(temps2);
    test('Median temperature', median.toCelsius().value === 20);
    
    // Range
    const tempsRange = TemperatureUtils.range(temps);
    test('Range lower', tempsRange.lower.toCelsius().value === 20);
    test('Range upper', tempsRange.upper.toCelsius().value === 40);
    
    // Max/Min
    test('Max temperature', TemperatureUtils.max(temps).toCelsius().value === 40);
    test('Min temperature', TemperatureUtils.min(temps).toCelsius().value === 20);
    
    // Validation
    test('Valid temperature', TemperatureUtils.isValidTemperature(celsius(25)));
    test('Invalid temperature (below absolute zero)', !TemperatureUtils.isValidTemperature(kelvin(-100)));
    test('Normal body temperature', TemperatureUtils.isNormalBodyTemperature(celsius(37)));
    test('Abnormal body temperature', !TemperatureUtils.isNormalBodyTemperature(celsius(38)));
    test('Is fever', TemperatureUtils.isFever(celsius(38)));
    test('Not fever', !TemperatureUtils.isFever(celsius(37)));
    test('High fever', TemperatureUtils.isHighFever(celsius(39.5)));
    test('Hypothermia', TemperatureUtils.isHypothermia(celsius(34)));
    
    // Approximately equal
    test('Approximately equal', TemperatureUtils.approximatelyEqual(celsius(25.001), celsius(25.002)));
    test('Not approximately equal', !TemperatureUtils.approximatelyEqual(celsius(25), celsius(26)));
    
    // Warmer/Colder
    test('Warmer', TemperatureUtils.warmer(celsius(20), celsius(30)).toCelsius().value === 30);
    test('Colder', TemperatureUtils.colder(celsius(20), celsius(30)).toCelsius().value === 20);
    
    // Weather category
    test('Weather category cold', TemperatureUtils.weatherCategory(celsius(5)) === WeatherCategory.CHILLY);
    test('Weather category mild', TemperatureUtils.weatherCategory(celsius(20)) === WeatherCategory.MILD);
    test('Weather category hot', TemperatureUtils.weatherCategory(celsius(35)) === WeatherCategory.HOT);
    
    // MARK: - Scientific Calculations Tests
    
    subSeparator('Scientific Calculations Tests:');
    
    // Average kinetic energy at room temperature
    const energy = TemperatureUtils.averageKineticEnergy(celsius(25));
    test('Kinetic energy positive', energy > 0);
    
    // Speed of sound
    const speed0 = TemperatureUtils.speedOfSoundInAir(celsius(0));
    testApprox('Speed of sound at 0°C ~ 331 m/s', speed0, 331.3);
    
    const speed20 = TemperatureUtils.speedOfSoundInAir(celsius(20));
    testApprox('Speed of sound at 20°C ~ 343 m/s', speed20, 343.42);
    
    // Air density
    const density = TemperatureUtils.airDensity(celsius(25));
    test('Air density positive', density > 1.0 && density < 1.3);
    
    // MARK: - Common Ranges Tests
    
    subSeparator('Common Ranges Tests:');
    
    test('Freezer range contains -17°C', TemperatureUtils.CommonRanges.freezer.contains(celsius(-17)));
    test('Refrigerator range contains 3°C', TemperatureUtils.CommonRanges.refrigerator.contains(celsius(3)));
    test('Room temperature range contains 22°C', TemperatureUtils.CommonRanges.roomTemperature.contains(celsius(22)));
    test('Comfortable indoor range contains 23°C', TemperatureUtils.CommonRanges.comfortableIndoor.contains(celsius(23)));
    
    // MARK: - Special Points Tests
    
    subSeparator('Special Points Tests:');
    
    test('Liquid nitrogen temp', TemperatureUtils.SpecialPoints.liquidNitrogen.toCelsius().value === -196);
    test('Dry ice temp', TemperatureUtils.SpecialPoints.dryIce.toCelsius().value === -78.5);
    test('Fever temp', TemperatureUtils.SpecialPoints.fever.toCelsius().value === 38);
    test('High fever temp', TemperatureUtils.SpecialPoints.highFever.toCelsius().value === 39);
    
    // MARK: - Meat Safety Temps Tests
    
    subSeparator('Meat Safety Temps Tests:');
    
    test('Chicken Safety Temp', TemperatureUtils.MeatSafetyTemps.chickenBreast.toCelsius().value === 74);
    test('Ground Beef Safety Temp', TemperatureUtils.MeatSafetyTemps.groundBeef.toCelsius().value === 71);
    test('Steak Medium Temp', TemperatureUtils.MeatSafetyTemps.steakMedium.toCelsius().value === 63);
    
    // MARK: - Summary
    
    separator('Test Summary');
    console.log(`Total: ${passed + failed}`);
    console.log(`Passed: ${passed}`);
    console.log(`Failed: ${failed}`);
    
    if (failed === 0) {
        console.log('\n🎉 All tests passed!');
    } else {
        console.log('\n⚠️ Some tests failed. Please review the output above.');
    }
}

// 运行测试
runTests();