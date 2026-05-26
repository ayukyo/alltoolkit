/**
 * Temperature Utils - 温度工具模块
 * 
 * 功能：
 * - 多种温度单位转换（摄氏、华氏、开尔文、兰氏、德利尔、牛顿、列氏、罗氏）
 * - 温度范围操作
 * - 人体舒适度评估
 * - 风寒指数和体感温度计算
 * - 特殊温度点常量
 * - 科学计算（声速、空气密度等）
 * 
 * 零外部依赖，纯 JavaScript 实现。
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

/**
 * 温度单位枚举
 */
const TemperatureUnit = {
    CELSIUS: 'C',
    FAHRENHEIT: 'F',
    KELVIN: 'K',
    RANKINE: 'R',
    DELISLE: 'De',
    NEWTON: 'N',
    REAUMUR: 'Re',
    ROMER: 'Ro'
};

/**
 * 温度单位信息映射
 */
const UnitInfo = {
    'C': { name: 'Celsius', symbol: '°C', fullName: 'Celsius', isAbsolute: false },
    'F': { name: 'Fahrenheit', symbol: '°F', fullName: 'Fahrenheit', isAbsolute: false },
    'K': { name: 'Kelvin', symbol: 'K', fullName: 'Kelvin', isAbsolute: true },
    'R': { name: 'Rankine', symbol: '°R', fullName: 'Rankine', isAbsolute: true },
    'De': { name: 'Delisle', symbol: '°De', fullName: 'Delisle', isAbsolute: false },
    'N': { name: 'Newton', symbol: '°N', fullName: 'Newton', isAbsolute: false },
    'Re': { name: 'Réaumur', symbol: '°Ré', fullName: 'Réaumur', isAbsolute: false },
    'Ro': { name: 'Rømer', symbol: '°Rø', fullName: 'Rømer', isAbsolute: false }
};

/**
 * 舒适度等级枚举
 */
const ComfortLevel = {
    FREEZING: { name: '极冷', emoji: '🥶' },
    COLD: { name: '寒冷', emoji: '❄️' },
    COOL: { name: '凉爽', emoji: '🌬️' },
    COMFORTABLE: { name: '舒适', emoji: '😊' },
    WARM: { name: '温暖', emoji: '🌤️' },
    HOT: { name: '炎热', emoji: '☀️' },
    VERY_HOT: { name: '酷热', emoji: '🥵' },
    EXTREMELY_HOT: { name: '极热', emoji: '🔥' }
};

/**
 * 天气分类枚举
 */
const WeatherCategory = {
    EXTREME_COLD: { name: '极寒', emoji: '🥶🥶🥶' },
    VERY_COLD: { name: '严寒', emoji: '🥶🥶' },
    COLD: { name: '寒冷', emoji: '🥶' },
    CHILLY: { name: '微寒', emoji: '❄️' },
    COOL: { name: '凉爽', emoji: '🌬️' },
    MILD: { name: '温和', emoji: '🌤️' },
    WARM: { name: '温暖', emoji: '☀️' },
    HOT: { name: '炎热', emoji: '🌡️' },
    VERY_HOT: { name: '酷热', emoji: '🔥' },
    EXTREME_HEAT: { name: '极热', emoji: '🔥🔥' }
};

/**
 * 温度类
 */
class Temperature {
    constructor(value, unit = TemperatureUnit.CELSIUS) {
        this.value = Number(value);
        this.unit = unit;
        
        // 验证
        if (isNaN(this.value)) {
            throw new Error(`Invalid temperature value: ${value}`);
        }
        if (!UnitInfo[this.unit]) {
            throw new Error(`Unknown temperature unit: ${unit}`);
        }
    }
    
    /**
     * 静态工厂方法
     */
    static celsius(value) {
        return new Temperature(value, TemperatureUnit.CELSIUS);
    }
    
    static fahrenheit(value) {
        return new Temperature(value, TemperatureUnit.FAHRENHEIT);
    }
    
    static kelvin(value) {
        return new Temperature(value, TemperatureUnit.KELVIN);
    }
    
    static rankine(value) {
        return new Temperature(value, TemperatureUnit.RANKINE);
    }
    
    // MARK: - 转换方法
    
    /**
     * 转换为摄氏温度
     */
    toCelsius() {
        switch (this.unit) {
            case TemperatureUnit.CELSIUS:
                return this;
            case TemperatureUnit.FAHRENHEIT:
                return Temperature.celsius((this.value - 32) * 5 / 9);
            case TemperatureUnit.KELVIN:
                return Temperature.celsius(this.value - 273.15);
            case TemperatureUnit.RANKINE:
                return Temperature.celsius((this.value - 491.67) * 5 / 9);
            case TemperatureUnit.DELISLE:
                return Temperature.celsius(100 - this.value * 2 / 3);
            case TemperatureUnit.NEWTON:
                return Temperature.celsius(this.value * 100 / 33);
            case TemperatureUnit.REAUMUR:
                return Temperature.celsius(this.value * 5 / 4);
            case TemperatureUnit.ROMER:
                return Temperature.celsius((this.value - 7.5) * 40 / 21);
            default:
                return this;
        }
    }
    
    /**
     * 转换为华氏温度
     */
    toFahrenheit() {
        const celsius = this.toCelsius().value;
        return Temperature.fahrenheit(celsius * 9 / 5 + 32);
    }
    
    /**
     * 转换为开尔文温度
     */
    toKelvin() {
        const celsius = this.toCelsius().value;
        return Temperature.kelvin(celsius + 273.15);
    }
    
    /**
     * 转换为兰氏温度
     */
    toRankine() {
        const celsius = this.toCelsius().value;
        return Temperature.rankine((celsius + 273.15) * 9 / 5);
    }
    
    /**
     * 转换为德利尔温度
     */
    toDelisle() {
        const celsius = this.toCelsius().value;
        return new Temperature((100 - celsius) * 3 / 2, TemperatureUnit.DELISLE);
    }
    
    /**
     * 转换为牛顿温度
     */
    toNewton() {
        const celsius = this.toCelsius().value;
        return new Temperature(celsius * 33 / 100, TemperatureUnit.NEWTON);
    }
    
    /**
     * 转换为列氏温度
     */
    toReaumur() {
        const celsius = this.toCelsius().value;
        return new Temperature(celsius * 4 / 5, TemperatureUnit.REAUMUR);
    }
    
    /**
     * 转换为罗氏温度
     */
    toRomer() {
        const celsius = this.toCelsius().value;
        return new Temperature(celsius * 21 / 40 + 7.5, TemperatureUnit.ROMER);
    }
    
    /**
     * 转换为指定单位
     */
    convertedTo(targetUnit) {
        switch (targetUnit) {
            case TemperatureUnit.CELSIUS: return this.toCelsius();
            case TemperatureUnit.FAHRENHEIT: return this.toFahrenheit();
            case TemperatureUnit.KELVIN: return this.toKelvin();
            case TemperatureUnit.RANKINE: return this.toRankine();
            case TemperatureUnit.DELISLE: return this.toDelisle();
            case TemperatureUnit.NEWTON: return this.toNewton();
            case TemperatureUnit.REAUMUR: return this.toReaumur();
            case TemperatureUnit.ROMER: return this.toRomer();
            default: throw new Error(`Unknown target unit: ${targetUnit}`);
        }
    }
    
    // MARK: - 属性
    
    /**
     * 获取单位信息
     */
    get unitInfo() {
        return UnitInfo[this.unit];
    }
    
    /**
     * 判断是否低于冰点
     */
    get isBelowFreezing() {
        return this.toCelsius().value < 0;
    }
    
    /**
     * 判断是否高于沸点
     */
    get isAboveBoiling() {
        return this.toCelsius().value > 100;
    }
    
    /**
     * 判断是否为负温度
     */
    get isNegative() {
        return this.value < 0;
    }
    
    /**
     * 判断是否为绝对零度或以下
     */
    get isAtOrBelowAbsoluteZero() {
        return this.toKelvin().value <= 0;
    }
    
    // MARK: - 格式化
    
    /**
     * 格式化输出
     */
    format(precision = 1) {
        return `${this.value.toFixed(precision)}${this.unitInfo.symbol}`;
    }
    
    /**
     * 带单位全名的格式化输出
     */
    formatFullName(precision = 1) {
        return `${this.value.toFixed(precision)} ${this.unitInfo.fullName}`;
    }
    
    /**
     * 格式化输出为指定单位
     */
    formatTo(unit, precision = 1) {
        return this.convertedTo(unit).format(precision);
    }
    
    /**
     * 同时显示摄氏和华氏温度
     */
    get dualFormat() {
        return `${this.format(1)} (${this.toFahrenheit().format(1)})`;
    }
    
    // MARK: - 舒适度评估
    
    /**
     * 评估人体舒适度
     */
    get comfortLevel() {
        const celsius = this.toCelsius().value;
        if (celsius < -10) return ComfortLevel.FREEZING;
        if (celsius < 5) return ComfortLevel.COLD;
        if (celsius < 15) return ComfortLevel.COOL;
        if (celsius < 26) return ComfortLevel.COMFORTABLE;
        if (celsius < 32) return ComfortLevel.WARM;
        if (celsius < 38) return ComfortLevel.HOT;
        if (celsius < 45) return ComfortLevel.VERY_HOT;
        return ComfortLevel.EXTREMELY_HOT;
    }
    
    /**
     * 是否适合户外活动
     */
    get isSuitableForOutdoor() {
        const celsius = this.toCelsius().value;
        return celsius >= 10 && celsius <= 32;
    }
    
    /**
     * 是否需要保暖
     */
    get needsWarmClothing() {
        return this.toCelsius().value < 15;
    }
    
    /**
     * 是否需要防晒
     */
    get needsSunProtection() {
        return this.toCelsius().value > 25;
    }
    
    // MARK: - 风寒和体感温度
    
    /**
     * 计算风寒指数
     * 仅适用于气温 ≤ 10°C 且风速 > 4.8 km/h
     */
    windChill(windSpeed) {
        const celsius = this.toCelsius().value;
        if (celsius > 10 || windSpeed <= 4.8) {
            return Temperature.celsius(celsius);
        }
        const windChillValue = 13.12 + 0.6215 * celsius 
            - 11.37 * Math.pow(windSpeed, 0.16) 
            + 0.3965 * celsius * Math.pow(windSpeed, 0.16);
        return Temperature.celsius(windChillValue);
    }
    
    /**
     * 计算体感温度（Heat Index）
     * 仅适用于气温 ≥ 27°C 且相对湿度 ≥ 40%
     */
    heatIndex(humidity) {
        const celsius = this.toCelsius().value;
        if (celsius < 27 || humidity < 40) {
            return Temperature.celsius(celsius);
        }
        
        // 转换为华氏
        const T = celsius * 9 / 5 + 32;
        const R = humidity;
        
        // Rothfusz 回归方程
        let HI = -42.379 + 2.04901523 * T + 10.14333127 * R - 0.22475541 * T * R
            - 0.00683783 * T * T - 0.05481717 * R * R + 0.00122874 * T * T * R
            + 0.00085282 * T * R * R - 0.00000199 * T * T * R * R;
        
        // 调整项
        if (R < 13 && T >= 80 && T <= 112) {
            HI -= ((13 - R) / 4) * Math.sqrt((17 - Math.abs(T - 95)) / 17);
        } else if (R > 85 && T >= 80 && T <= 87) {
            HI += ((R - 85) / 10) * ((87 - T) / 5);
        }
        
        return Temperature.fahrenheit(HI).toCelsius();
    }
    
    /**
     * 综合体感温度
     */
    apparentTemperature(windSpeed = 0, humidity = 50) {
        const celsius = this.toCelsius().value;
        
        if (celsius <= 10 && windSpeed > 4.8) {
            return this.windChill(windSpeed);
        } else if (celsius >= 27 && humidity >= 40) {
            return this.heatIndex(humidity);
        }
        
        return Temperature.celsius(celsius);
    }
    
    // MARK: - 运算
    
    /**
     * 加上一个温度差值
     */
    add(delta) {
        return new Temperature(this.value + delta, this.unit);
    }
    
    /**
     * 减去一个温度差值
     */
    subtract(delta) {
        return new Temperature(this.value - delta, this.unit);
    }
    
    /**
     * 计算与另一个温度的差值（返回摄氏度差值）
     */
    difference(other) {
        return this.toCelsius().value - other.toCelsius().value;
    }
    
    /**
     * 乘以一个系数
     */
    multiply(factor) {
        return new Temperature(this.value * factor, this.unit);
    }
    
    /**
     * 除以一个系数
     */
    divide(factor) {
        if (factor === 0) return this;
        return new Temperature(this.value / factor, this.unit);
    }
    
    // MARK: - 比较
    
    /**
     * 判断是否等于另一个温度（考虑单位转换）
     */
    equals(other, tolerance = 0.01) {
        const diff = Math.abs(this.toCelsius().value - other.toCelsius().value);
        return diff <= tolerance;
    }
    
    /**
     * 判断是否小于另一个温度
     */
    lessThan(other) {
        return this.toCelsius().value < other.toCelsius().value;
    }
    
    /**
     * 判断是否大于另一个温度
     */
    greaterThan(other) {
        return this.toCelsius().value > other.toCelsius().value;
    }
    
    /**
     * 判断是否小于等于另一个温度
     */
    lessThanOrEqual(other) {
        return this.toCelsius().value <= other.toCelsius().value;
    }
    
    /**
     * 判断是否大于等于另一个温度
     */
    greaterThanOrEqual(other) {
        return this.toCelsius().value >= other.toCelsius().value;
    }
}

/**
 * 温度范围类
 */
class TemperatureRange {
    constructor(lower, upper) {
        const lowerCelsius = lower.toCelsius().value;
        const upperCelsius = upper.toCelsius().value;
        
        this.lower = lowerCelsius <= upperCelsius ? lower : upper;
        this.upper = lowerCelsius <= upperCelsius ? upper : lower;
    }
    
    /**
     * 从摄氏度创建范围
     */
    static fromCelsius(lower, upper) {
        return new TemperatureRange(
            Temperature.celsius(lower),
            Temperature.celsius(upper)
        );
    }
    
    /**
     * 范围宽度
     */
    get width() {
        return Temperature.celsius(this.upper.toCelsius().value - this.lower.toCelsius().value);
    }
    
    /**
     * 范围中点
     */
    get midpoint() {
        const avg = (this.lower.toCelsius().value + this.upper.toCelsius().value) / 2;
        return Temperature.celsius(avg);
    }
    
    /**
     * 检查温度是否在范围内
     */
    contains(temperature) {
        const lowerCelsius = this.lower.toCelsius().value;
        const upperCelsius = this.upper.toCelsius().value;
        const tempCelsius = temperature.toCelsius().value;
        return tempCelsius >= lowerCelsius && tempCelsius <= upperCelsius;
    }
    
    /**
     * 转换为指定单位
     */
    convertedTo(unit) {
        return new TemperatureRange(
            this.lower.convertedTo(unit),
            this.upper.convertedTo(unit)
        );
    }
    
    /**
     * 与另一个范围合并
     */
    union(other) {
        const lowerCelsius = Math.min(this.lower.toCelsius().value, other.lower.toCelsius().value);
        const upperCelsius = Math.max(this.upper.toCelsius().value, other.upper.toCelsius().value);
        return TemperatureRange.fromCelsius(lowerCelsius, upperCelsius);
    }
    
    /**
     * 与另一个范围的交集
     */
    intersection(other) {
        const lowerCelsius = Math.max(this.lower.toCelsius().value, other.lower.toCelsius().value);
        const upperCelsius = Math.min(this.upper.toCelsius().value, other.upper.toCelsius().value);
        if (lowerCelsius > upperCelsius) return null;
        return TemperatureRange.fromCelsius(lowerCelsius, upperCelsius);
    }
    
    /**
     * 格式化输出
     */
    format(precision = 1) {
        return `${this.lower.format(precision)} ~ ${this.upper.format(precision)}`;
    }
}

/**
 * 温度工具类
 */
class TemperatureUtils {
    // MARK: - 物理常数
    
    static get ABSOLUTE_ZERO() { return Temperature.kelvin(0); }
    static get WATER_FREEZING_POINT() { return Temperature.celsius(0); }
    static get WATER_BOILING_POINT() { return Temperature.celsius(100); }
    static get NORMAL_BODY_TEMPERATURE() { return Temperature.celsius(37); }
    static get ROOM_TEMPERATURE() { return Temperature.celsius(20); }
    
    // MARK: - 常用温度范围
    
    static CommonRanges = {
        freezer: TemperatureRange.fromCelsius(-18, -15),
        refrigerator: TemperatureRange.fromCelsius(2, 5),
        roomTemperature: TemperatureRange.fromCelsius(18, 24),
        comfortableIndoor: TemperatureRange.fromCelsius(20, 26),
        sauna: TemperatureRange.fromCelsius(70, 100),
        hotWater: TemperatureRange.fromCelsius(40, 50),
        baking: TemperatureRange.fromCelsius(150, 250)
    };
    
    // MARK: - 特殊温度点
    
    static SpecialPoints = {
        absoluteZero: Temperature.kelvin(0),
        liquidNitrogen: Temperature.celsius(-196),
        dryIce: Temperature.celsius(-78.5),
        waterFreezing: Temperature.celsius(0),
        comfortableRoom: Temperature.celsius(22),
        humanBody: Temperature.celsius(37),
        fever: Temperature.celsius(38),
        highFever: Temperature.celsius(39),
        waterBoiling: Temperature.celsius(100),
        ovenLow: Temperature.celsius(150),
        ovenHigh: Temperature.celsius(250),
        sunSurface: Temperature.celsius(5500)
    };
    
    // MARK: - 肉类安全烹饪温度
    
    static MeatSafetyTemps = {
        chickenBreast: Temperature.celsius(74),
        groundBeef: Temperature.celsius(71),
        steakMedium: Temperature.celsius(63),
        pork: Temperature.celsius(63),
        fish: Temperature.celsius(63),
        eggs: Temperature.celsius(71),
        leftovers: Temperature.celsius(74)
    };
    
    // MARK: - 单位转换
    
    /**
     * 快速转换温度
     */
    static convert(value, fromUnit, toUnit) {
        return new Temperature(value, fromUnit).convertedTo(toUnit).value;
    }
    
    /**
     * 批量转换温度
     */
    static convertAll(value, fromUnit) {
        const temp = new Temperature(value, fromUnit);
        const result = {};
        for (const unit of Object.values(TemperatureUnit)) {
            result[unit] = temp.convertedTo(unit).value;
        }
        return result;
    }
    
    // MARK: - 统计计算
    
    /**
     * 计算多个温度的平均值
     */
    static average(temperatures) {
        if (temperatures.length === 0) return null;
        const sum = temperatures.reduce((acc, t) => acc + t.toCelsius().value, 0);
        return Temperature.celsius(sum / temperatures.length);
    }
    
    /**
     * 计算多个温度的中位数
     */
    static median(temperatures) {
        if (temperatures.length === 0) return null;
        const sorted = temperatures.map(t => t.toCelsius().value).sort((a, b) => a - b);
        const count = sorted.length;
        if (count % 2 === 0) {
            return Temperature.celsius((sorted[count / 2 - 1] + sorted[count / 2]) / 2);
        } else {
            return Temperature.celsius(sorted[Math.floor(count / 2)]);
        }
    }
    
    /**
     * 计算温度范围
     */
    static range(temperatures) {
        if (temperatures.length === 0) return null;
        const celsiusValues = temperatures.map(t => t.toCelsius().value);
        const min = Math.min(...celsiusValues);
        const max = Math.max(...celsiusValues);
        return TemperatureRange.fromCelsius(min, max);
    }
    
    /**
     * 找出最高温度
     */
    static max(temperatures) {
        if (temperatures.length === 0) return null;
        return temperatures.reduce((max, t) => t.greaterThan(max) ? t : max, temperatures[0]);
    }
    
    /**
     * 找出最低温度
     */
    static min(temperatures) {
        if (temperatures.length === 0) return null;
        return temperatures.reduce((min, t) => t.lessThan(min) ? t : min, temperatures[0]);
    }
    
    // MARK: - 验证
    
    /**
     * 验证温度是否在合理范围内
     */
    static isValidTemperature(temperature) {
        const kelvin = temperature.toKelvin().value;
        return kelvin >= 0 && kelvin <= 6000;
    }
    
    /**
     * 验证是否为正常人体体温
     */
    static isNormalBodyTemperature(temperature) {
        const celsius = temperature.toCelsius().value;
        return celsius >= 36.1 && celsius <= 37.2;
    }
    
    /**
     * 验证是否为发烧
     */
    static isFever(temperature) {
        return temperature.toCelsius().value > 37.5;
    }
    
    /**
     * 验证是否为高烧
     */
    static isHighFever(temperature) {
        return temperature.toCelsius().value >= 39;
    }
    
    /**
     * 验证是否为低温症
     */
    static isHypothermia(temperature) {
        return temperature.toCelsius().value < 35;
    }
    
    // MARK: - 比较
    
    /**
     * 比较两个温度是否在指定误差范围内相等
     */
    static approximatelyEqual(lhs, rhs, tolerance = 0.01) {
        const diff = Math.abs(lhs.toCelsius().value - rhs.toCelsius().value);
        return diff <= tolerance;
    }
    
    /**
     * 获取两个温度中较暖的一个
     */
    static warmer(lhs, rhs) {
        return lhs.greaterThan(rhs) ? lhs : rhs;
    }
    
    /**
     * 获取两个温度中较冷的一个
     */
    static colder(lhs, rhs) {
        return lhs.lessThan(rhs) ? lhs : rhs;
    }
    
    // MARK: - 天气分类
    
    /**
     * 获取天气分类
     */
    static weatherCategory(temperature) {
        const celsius = temperature.toCelsius().value;
        if (celsius < -20) return WeatherCategory.EXTREME_COLD;
        if (celsius < -10) return WeatherCategory.VERY_COLD;
        if (celsius < 0) return WeatherCategory.COLD;
        if (celsius < 10) return WeatherCategory.CHILLY;
        if (celsius < 18) return WeatherCategory.COOL;
        if (celsius < 24) return WeatherCategory.MILD;
        if (celsius < 30) return WeatherCategory.WARM;
        if (celsius < 38) return WeatherCategory.HOT;
        if (celsius < 45) return WeatherCategory.VERY_HOT;
        return WeatherCategory.EXTREME_HEAT;
    }
    
    // MARK: - 科学计算
    
    /**
     * 计算平均动能（基于温度，单位：焦耳）
     */
    static averageKineticEnergy(temperature) {
        const kelvin = temperature.toKelvin().value;
        const boltzmannConstant = 1.380649e-23; // J/K
        return 1.5 * boltzmannConstant * kelvin;
    }
    
    /**
     * 从动能计算温度
     */
    static temperatureFromKineticEnergy(energy) {
        const boltzmannConstant = 1.380649e-23; // J/K
        const kelvin = (2.0 / 3.0) * energy / boltzmannConstant;
        return Temperature.kelvin(kelvin);
    }
    
    /**
     * 计算声速（在空气中，单位：m/s）
     */
    static speedOfSoundInAir(temperature) {
        const celsius = temperature.toCelsius().value;
        return 331.3 + 0.606 * celsius;
    }
    
    /**
     * 计算空气密度（海平面，单位：kg/m³）
     */
    static airDensity(temperature, pressure = 101325) {
        const kelvin = temperature.toKelvin().value;
        const R = 287.058; // J/(kg·K) 空气的气体常数
        return pressure / (R * kelvin);
    }
}

// 便捷函数
function celsius(value) { return Temperature.celsius(value); }
function fahrenheit(value) { return Temperature.fahrenheit(value); }
function kelvin(value) { return Temperature.kelvin(value); }
function convert(value, from, to) { return TemperatureUtils.convert(value, from, to); }
function convertAll(value, from) { return TemperatureUtils.convertAll(value, from); }

// 导出
module.exports = {
    // 枚举/常量
    TemperatureUnit,
    UnitInfo,
    ComfortLevel,
    WeatherCategory,
    
    // 类
    Temperature,
    TemperatureRange,
    TemperatureUtils,
    
    // 便捷函数
    celsius,
    fahrenheit,
    kelvin,
    convert,
    convertAll
};