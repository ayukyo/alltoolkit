/**
 * SemVer Utils - 语义化版本工具模块
 * 
 * 功能：
 * - 版本解析与验证
 * - 版本比较与排序
 * - 版本范围匹配
 * - 版本递增/递减
 * - 预发布版本处理
 * - 版本约束解析
 * 
 * 遵循 Semantic Versioning 2.0.0 规范
 * 零外部依赖，纯 JavaScript 实现。
 */

/**
 * 语义化版本类
 */
class SemVer {
    /**
     * 创建语义化版本对象
     * @param {number} major - 主版本号
     * @param {number} minor - 次版本号
     * @param {number} patch - 修订版本号
     * @param {string[]} prerelease - 预发布标识
     * @param {string[]} build - 构建元数据
     */
    constructor(major = 0, minor = 0, patch = 0, prerelease = [], build = []) {
        this.major = parseInt(major) || 0;
        this.minor = parseInt(minor) || 0;
        this.patch = parseInt(patch) || 0;
        this.prerelease = Array.isArray(prerelease) ? prerelease : [];
        this.build = Array.isArray(build) ? build : [];
    }

    /**
     * 转换为字符串
     * @returns {string} 版本字符串
     */
    toString() {
        let version = `${this.major}.${this.minor}.${this.patch}`;
        
        if (this.prerelease.length > 0) {
            version += '-' + this.prerelease.join('.');
        }
        
        if (this.build.length > 0) {
            version += '+' + this.build.join('.');
        }
        
        return version;
    }

    /**
     * 转换为简洁字符串（不含构建元数据）
     * @returns {string} 简洁版本字符串
     */
    toCleanString() {
        let version = `${this.major}.${this.minor}.${this.patch}`;
        
        if (this.prerelease.length > 0) {
            version += '-' + this.prerelease.join('.');
        }
        
        return version;
    }

    /**
     * 转换为 JSON
     * @returns {Object} JSON 对象
     */
    toJSON() {
        return {
            major: this.major,
            minor: this.minor,
            patch: this.patch,
            prerelease: this.prerelease,
            build: this.build,
            version: this.toString()
        };
    }

    /**
     * 克隆版本对象
     * @returns {SemVer} 新的 SemVer 对象
     */
    clone() {
        return new SemVer(
            this.major,
            this.minor,
            this.patch,
            [...this.prerelease],
            [...this.build]
        );
    }

    /**
     * 是否为预发布版本
     * @returns {boolean}
     */
    isPrerelease() {
        return this.prerelease.length > 0;
    }

    /**
     * 是否为稳定版本
     * @returns {boolean}
     */
    isStable() {
        return this.major > 0 && !this.isPrerelease();
    }

    /**
     * 比较版本
     * @param {SemVer|string} other - 另一个版本
     * @returns {number} -1, 0, 1
     */
    compare(other) {
        if (typeof other === 'string') {
            other = SemVerUtils.parse(other);
        }

        // 比较主版本号
        if (this.major !== other.major) {
            return this.major > other.major ? 1 : -1;
        }

        // 比较次版本号
        if (this.minor !== other.minor) {
            return this.minor > other.minor ? 1 : -1;
        }

        // 比较修订版本号
        if (this.patch !== other.patch) {
            return this.patch > other.patch ? 1 : -1;
        }

        // 比较预发布版本
        if (this.prerelease.length === 0 && other.prerelease.length === 0) {
            return 0;
        }

        // 没有预发布标识的版本更大
        if (this.prerelease.length === 0) return 1;
        if (other.prerelease.length === 0) return -1;

        // 逐项比较预发布标识
        const maxLen = Math.max(this.prerelease.length, other.prerelease.length);
        for (let i = 0; i < maxLen; i++) {
            const a = this.prerelease[i];
            const b = other.prerelease[i];

            // 长度不同时，短的更小
            if (a === undefined) return -1;
            if (b === undefined) return 1;

            const aIsNum = /^\d+$/.test(a);
            const bIsNum = /^\d+$/.test(b);

            // 数字标识符小于字符串标识符
            if (aIsNum && !bIsNum) return -1;
            if (!aIsNum && bIsNum) return 1;

            if (aIsNum && bIsNum) {
                const numA = parseInt(a);
                const numB = parseInt(b);
                if (numA !== numB) {
                    return numA > numB ? 1 : -1;
                }
            } else {
                const cmp = a.localeCompare(b);
                if (cmp !== 0) return cmp;
            }
        }

        return 0;
    }

    /**
     * 等于
     * @param {SemVer|string} other - 另一个版本
     * @returns {boolean}
     */
    eq(other) {
        return this.compare(other) === 0;
    }

    /**
     * 不等于
     * @param {SemVer|string} other - 另一个版本
     * @returns {boolean}
     */
    neq(other) {
        return this.compare(other) !== 0;
    }

    /**
     * 大于
     * @param {SemVer|string} other - 另一个版本
     * @returns {boolean}
     */
    gt(other) {
        return this.compare(other) > 0;
    }

    /**
     * 大于等于
     * @param {SemVer|string} other - 另一个版本
     * @returns {boolean}
     */
    gte(other) {
        return this.compare(other) >= 0;
    }

    /**
     * 小于
     * @param {SemVer|string} other - 另一个版本
     * @returns {boolean}
     */
    lt(other) {
        return this.compare(other) < 0;
    }

    /**
     * 小于等于
     * @param {SemVer|string} other - 另一个版本
     * @returns {boolean}
     */
    lte(other) {
        return this.compare(other) <= 0;
    }
}

/**
 * 语义化版本工具类
 */
class SemVerUtils {
    // ============== 解析与验证 ==============

    /**
     * 解析版本字符串
     * @param {string} version - 版本字符串
     * @returns {SemVer|null} SemVer 对象或 null
     */
    static parse(version) {
        if (!version || typeof version !== 'string') {
            return null;
        }

        version = version.trim();

        // 移除前缀 'v' 或 'V'
        if (version.startsWith('v') || version.startsWith('V')) {
            version = version.slice(1);
        }

        // 正则匹配
        const pattern = /^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.-]+))?(?:\+([a-zA-Z0-9.-]+))?$/;
        const match = version.match(pattern);

        if (!match) {
            return null;
        }

        const [, major, minor, patch, prerelease, build] = match;

        // 解析预发布标识
        const prereleaseArr = prerelease ? prerelease.split('.').filter(Boolean) : [];

        // 解析构建元数据
        const buildArr = build ? build.split('.').filter(Boolean) : [];

        return new SemVer(
            parseInt(major),
            parseInt(minor),
            parseInt(patch),
            prereleaseArr,
            buildArr
        );
    }

    /**
     * 尝试解析版本，失败返回默认版本
     * @param {string} version - 版本字符串
     * @param {string} defaultVersion - 默认版本
     * @returns {SemVer} SemVer 对象
     */
    static tryParse(version, defaultVersion = '0.0.0') {
        const parsed = SemVerUtils.parse(version);
        return parsed || SemVerUtils.parse(defaultVersion);
    }

    /**
     * 验证版本字符串
     * @param {string} version - 版本字符串
     * @returns {boolean} 是否有效
     */
    static isValid(version) {
        return SemVerUtils.parse(version) !== null;
    }

    /**
     * 清理版本字符串
     * @param {string} version - 版本字符串
     * @returns {string} 清理后的版本字符串
     */
    static clean(version) {
        const parsed = SemVerUtils.parse(version);
        return parsed ? parsed.toCleanString() : null;
    }

    // ============== 比较操作 ==============

    /**
     * 比较两个版本
     * @param {string|SemVer} v1 - 版本1
     * @param {string|SemVer} v2 - 版本2
     * @returns {number} -1, 0, 1
     */
    static compare(v1, v2) {
        if (typeof v1 === 'string') {
            v1 = SemVerUtils.parse(v1);
        }
        if (typeof v2 === 'string') {
            v2 = SemVerUtils.parse(v2);
        }

        if (!v1 || !v2) {
            throw new Error('Invalid version');
        }

        return v1.compare(v2);
    }

    /**
     * 比较主版本号
     * @param {string|SemVer} v1 - 版本1
     * @param {string|SemVer} v2 - 版本2
     * @returns {number} -1, 0, 1
     */
    static compareMain(v1, v2) {
        if (typeof v1 === 'string') {
            v1 = SemVerUtils.parse(v1);
        }
        if (typeof v2 === 'string') {
            v2 = SemVerUtils.parse(v2);
        }

        if (v1.major !== v2.major) {
            return v1.major > v2.major ? 1 : -1;
        }

        if (v1.minor !== v2.minor) {
            return v1.minor > v2.minor ? 1 : -1;
        }

        return 0;
    }

    /**
     * 相等比较
     * @param {string|SemVer} v1 - 版本1
     * @param {string|SemVer} v2 - 版本2
     * @returns {boolean}
     */
    static eq(v1, v2) {
        return SemVerUtils.compare(v1, v2) === 0;
    }

    /**
     * 不等比较
     * @param {string|SemVer} v1 - 版本1
     * @param {string|SemVer} v2 - 版本2
     * @returns {boolean}
     */
    static neq(v1, v2) {
        return SemVerUtils.compare(v1, v2) !== 0;
    }

    /**
     * 大于比较
     * @param {string|SemVer} v1 - 版本1
     * @param {string|SemVer} v2 - 版本2
     * @returns {boolean}
     */
    static gt(v1, v2) {
        return SemVerUtils.compare(v1, v2) > 0;
    }

    /**
     * 大于等于比较
     * @param {string|SemVer} v1 - 版本1
     * @param {string|SemVer} v2 - 版本2
     * @returns {boolean}
     */
    static gte(v1, v2) {
        return SemVerUtils.compare(v1, v2) >= 0;
    }

    /**
     * 小于比较
     * @param {string|SemVer} v1 - 版本1
     * @param {string|SemVer} v2 - 版本2
     * @returns {boolean}
     */
    static lt(v1, v2) {
        return SemVerUtils.compare(v1, v2) < 0;
    }

    /**
     * 小于等于比较
     * @param {string|SemVer} v1 - 版本1
     * @param {string|SemVer} v2 - 版本2
     * @returns {boolean}
     */
    static lte(v1, v2) {
        return SemVerUtils.compare(v1, v2) <= 0;
    }

    /**
     * 检查是否为兼容版本（相同主版本号）
     * @param {string|SemVer} v1 - 版本1
     * @param {string|SemVer} v2 - 版本2
     * @returns {boolean}
     */
    static isCompatible(v1, v2) {
        if (typeof v1 === 'string') {
            v1 = SemVerUtils.parse(v1);
        }
        if (typeof v2 === 'string') {
            v2 = SemVerUtils.parse(v2);
        }

        // 主版本号为 0 时，不认为兼容
        if (v1.major === 0 || v2.major === 0) {
            return v1.major === v2.major && v1.minor === v2.minor;
        }

        return v1.major === v2.major;
    }

    // ============== 版本递增/递减 ==============

    /**
     * 递增主版本号
     * @param {string|SemVer} version - 版本
     * @param {Object} options - 选项
     * @returns {SemVer} 新版本
     */
    static incMajor(version, options = {}) {
        const v = typeof version === 'string' ? SemVerUtils.parse(version) : version.clone();
        v.major++;
        v.minor = 0;
        v.patch = 0;
        if (!options.keepPrerelease) {
            v.prerelease = [];
        }
        v.build = [];
        return v;
    }

    /**
     * 递增次版本号
     * @param {string|SemVer} version - 版本
     * @param {Object} options - 选项
     * @returns {SemVer} 新版本
     */
    static incMinor(version, options = {}) {
        const v = typeof version === 'string' ? SemVerUtils.parse(version) : version.clone();
        v.minor++;
        v.patch = 0;
        if (!options.keepPrerelease) {
            v.prerelease = [];
        }
        v.build = [];
        return v;
    }

    /**
     * 递增修订版本号
     * @param {string|SemVer} version - 版本
     * @param {Object} options - 选项
     * @returns {SemVer} 新版本
     */
    static incPatch(version, options = {}) {
        const v = typeof version === 'string' ? SemVerUtils.parse(version) : version.clone();
        v.patch++;
        if (!options.keepPrerelease) {
            v.prerelease = [];
        }
        v.build = [];
        return v;
    }

    /**
     * 递增预发布版本
     * @param {string|SemVer} version - 版本
     * @param {string} identifier - 预发布标识符
     * @returns {SemVer} 新版本
     */
    static incPrerelease(version, identifier = 'alpha') {
        const v = typeof version === 'string' ? SemVerUtils.parse(version) : version.clone();

        if (v.prerelease.length === 0) {
            v.prerelease = [identifier, 1];
        } else {
            const last = v.prerelease[v.prerelease.length - 1];
            if (/^\d+$/.test(last)) {
                v.prerelease[v.prerelease.length - 1] = String(parseInt(last) + 1);
            } else {
                v.prerelease.push(1);
            }
        }

        v.build = [];
        return v;
    }

    /**
     * 设置预发布版本
     * @param {string|SemVer} version - 版本
     * @param {string} prerelease - 预发布标识
     * @returns {SemVer} 新版本
     */
    static setPrerelease(version, prerelease) {
        const v = typeof version === 'string' ? SemVerUtils.parse(version) : version.clone();
        v.prerelease = prerelease ? prerelease.split('.').filter(Boolean) : [];
        v.build = [];
        return v;
    }

    /**
     * 设置构建元数据
     * @param {string|SemVer} version - 版本
     * @param {string} build - 构建元数据
     * @returns {SemVer} 新版本
     */
    static setBuild(version, build) {
        const v = typeof version === 'string' ? SemVerUtils.parse(version) : version.clone();
        v.build = build ? build.split('.').filter(Boolean) : [];
        return v;
    }

    // ============== 版本范围 ==============

    /**
     * 解析版本范围字符串
     * @param {string} range - 范围字符串
     * @returns {Object|null} 范围对象
     */
    static parseRange(range) {
        if (!range || typeof range !== 'string') {
            return null;
        }

        range = range.trim();

        // 精确版本
        if (/^\d/.test(range) || range.startsWith('v')) {
            const v = SemVerUtils.parse(range);
            if (v) {
                return { type: 'exact', version: v };
            }
        }

        // 范围运算符
        const rangePatterns = [
            // ^1.2.3 - 兼容版本
            {
                pattern: /^\^(\d+)(?:\.(\d+))?(?:\.(\d+))?(.*)$/,
                type: 'caret'
            },
            // ~1.2.3 - 大约版本
            {
                pattern: /^~(\d+)(?:\.(\d+))?(?:\.(\d+))?(.*)$/,
                type: 'tilde'
            },
            // >=1.2.3 <2.0.0 - 范围区间
            {
                pattern: /^(>=?|<=?)\s*(\d+(?:\.\d+)?(?:\.\d+)?(?:-[a-zA-Z0-9.-]+)?(?:\+[a-zA-Z0-9.-]+)?)\s*(.*?)$/,
                type: 'comparator'
            },
            // 1.2.3 - 2.3.4 - 连字符范围
            {
                pattern: /^(\d+(?:\.\d+)?(?:\.\d+)?(?:-[a-zA-Z0-9.-]+)?)\s*-\s*(\d+(?:\.\d+)?(?:\.\d+)?(?:-[a-zA-Z0-9.-]+)?)$/,
                type: 'hyphen'
            },
            // * 或 x - 任意版本
            {
                pattern: /^[*xX]$/,
                type: 'any'
            },
            // 1.x 或 1.* - 主版本通配
            {
                pattern: /^(\d+)[.][*xX]$/,
                type: 'majorWildcard'
            },
            // 1.2.x 或 1.2.* - 次版本通配
            {
                pattern: /^(\d+)\.(\d+)[.][*xX]$/,
                type: 'minorWildcard'
            }
        ];

        for (const { pattern, type } of rangePatterns) {
            const match = range.match(pattern);
            if (match) {
                return { type, match, raw: range };
            }
        }

        return null;
    }

    /**
     * 检查版本是否满足范围
     * @param {string|SemVer} version - 版本
     * @param {string} range - 范围字符串
     * @returns {boolean}
     */
    static satisfies(version, range) {
        if (typeof version === 'string') {
            version = SemVerUtils.parse(version);
        }

        if (!version) return false;

        const rangeObj = SemVerUtils.parseRange(range);
        if (!rangeObj) return false;

        switch (rangeObj.type) {
            case 'exact':
                return version.eq(rangeObj.version);

            case 'caret':
                return SemVerUtils._satisfiesCaret(version, rangeObj.match);
            case 'tilde':
                return SemVerUtils._satisfiesTilde(version, rangeObj.match);
            case 'comparator':
                return SemVerUtils._satisfiesComparator(version, rangeObj.match);
            case 'hyphen':
                return SemVerUtils._satisfiesHyphen(version, rangeObj.match);
            case 'any':
                return true;
            case 'majorWildcard':
                return version.major === parseInt(rangeObj.match[1]);
            case 'minorWildcard':
                return version.major === parseInt(rangeObj.match[1]) &&
                       version.minor === parseInt(rangeObj.match[2]);

            default:
                return false;
        }
    }

    /**
     * 插入符号范围 (^) 匹配
     * @private
     */
    static _satisfiesCaret(version, match) {
        const [, major, minor, patch, prerelease] = match;
        const majorNum = parseInt(major);
        const minorNum = minor ? parseInt(minor) : 0;
        const patchNum = patch ? parseInt(patch) : 0;

        // 构建最小版本
        const minVersion = new SemVer(majorNum, minorNum, patchNum);

        // 构建最大版本
        let maxVersion;
        if (majorNum === 0) {
            if (minorNum === 0) {
                if (patchNum === 0) {
                    // ^0.0.0 精确匹配
                    return version.major === 0 && version.minor === 0 && version.patch === 0;
                }
                // ^0.0.x 允许 patch 变化但不超过 patchNum
                // 实际上应该精确匹配，因为 0.0.x 没有兼容性保证
                maxVersion = new SemVer(0, 0, patchNum + 1);
            } else {
                // ^0.x.y 允许 patch 变化
                maxVersion = new SemVer(0, minorNum + 1, 0);
            }
        } else {
            // ^x.y.z 允许 minor 和 patch 变化
            maxVersion = new SemVer(majorNum + 1, 0, 0);
        }

        return version.gte(minVersion) && version.lt(maxVersion);
    }

    /**
     * 波浪号范围 (~) 匹配
     * @private
     */
    static _satisfiesTilde(version, match) {
        const [, major, minor, patch, prerelease] = match;
        const majorNum = parseInt(major);
        const minorNum = minor ? parseInt(minor) : 0;
        const patchNum = patch ? parseInt(patch) : 0;

        // 构建最小版本
        const minVersion = new SemVer(majorNum, minorNum, patchNum);

        // 构建最大版本（允许 patch 变化）
        const maxVersion = new SemVer(majorNum, minorNum + 1, 0);

        return version.gte(minVersion) && version.lt(maxVersion);
    }

    /**
     * 比较符范围匹配
     * @private
     */
    static _satisfiesComparator(version, match) {
        const [, op, ver, rest] = match;
        const target = SemVerUtils.parse(ver);
        if (!target) return false;

        let result = false;
        switch (op) {
            case '>': result = version.gt(target); break;
            case '>=': result = version.gte(target); break;
            case '<': result = version.lt(target); break;
            case '<=': result = version.lte(target); break;
            case '=': result = version.eq(target); break;
        }

        // 处理复合条件
        if (result && rest) {
            return SemVerUtils.satisfies(version, rest.trim());
        }

        return result;
    }

    /**
     * 连字符范围匹配
     * @private
     */
    static _satisfiesHyphen(version, match) {
        const [, min, max] = match;
        const minVersion = SemVerUtils.parse(min);
        const maxVersion = SemVerUtils.parse(max);

        if (!minVersion || !maxVersion) return false;

        return version.gte(minVersion) && version.lte(maxVersion);
    }

    // ============== 排序与过滤 ==============

    /**
     * 排序版本列表
     * @param {Array<string|SemVer>} versions - 版本列表
     * @param {Object} options - 选项
     * @returns {Array<SemVer>} 排序后的版本列表
     */
    static sort(versions, options = {}) {
        const parsed = versions
            .map(v => typeof v === 'string' ? SemVerUtils.parse(v) : v)
            .filter(v => v !== null);

        parsed.sort((a, b) => a.compare(b));

        if (options.desc) {
            parsed.reverse();
        }

        return parsed;
    }

    /**
     * 获取最大版本
     * @param {Array<string|SemVer>} versions - 版本列表
     * @returns {SemVer|null} 最大版本
     */
    static maxSatisfying(versions) {
        const sorted = SemVerUtils.sort(versions, { desc: true });
        return sorted.length > 0 ? sorted[0] : null;
    }

    /**
     * 获取最小版本
     * @param {Array<string|SemVer>} versions - 版本列表
     * @returns {SemVer|null} 最小版本
     */
    static minSatisfying(versions) {
        const sorted = SemVerUtils.sort(versions);
        return sorted.length > 0 ? sorted[0] : null;
    }

    /**
     * 过滤满足范围的版本
     * @param {Array<string|SemVer>} versions - 版本列表
     * @param {string} range - 范围字符串
     * @returns {Array<SemVer>} 满足范围的版本列表
     */
    static filterSatisfying(versions, range) {
        return versions
            .map(v => typeof v === 'string' ? SemVerUtils.parse(v) : v)
            .filter(v => v !== null && SemVerUtils.satisfies(v, range));
    }

    /**
     * 获取范围内最大版本
     * @param {Array<string|SemVer>} versions - 版本列表
     * @param {string} range - 范围字符串
     * @returns {SemVer|null} 最大版本
     */
    static maxSatisfyingInRange(versions, range) {
        const satisfying = SemVerUtils.filterSatisfying(versions, range);
        return SemVerUtils.maxSatisfying(satisfying);
    }

    // ============== 工具方法 ==============

    /**
     * 计算两个版本的差异类型
     * @param {string|SemVer} v1 - 版本1
     * @param {string|SemVer} v2 - 版本2
     * @returns {string|null} 'major', 'minor', 'patch', 'prerelease', null
     */
    static diff(v1, v2) {
        if (typeof v1 === 'string') {
            v1 = SemVerUtils.parse(v1);
        }
        if (typeof v2 === 'string') {
            v2 = SemVerUtils.parse(v2);
        }

        if (!v1 || !v2) return null;

        if (v1.major !== v2.major) return 'major';
        if (v1.minor !== v2.minor) return 'minor';
        if (v1.patch !== v2.patch) return 'patch';

        const pre1 = v1.prerelease.join('.');
        const pre2 = v2.prerelease.join('.');
        if (pre1 !== pre2) return 'prerelease';

        return null;
    }

    /**
     * 获取版本变更类型
     * @param {string|SemVer} from - 起始版本
     * @param {string|SemVer} to - 目标版本
     * @returns {Object} 变更信息
     */
    static getChangeType(from, to) {
        if (typeof from === 'string') {
            from = SemVerUtils.parse(from);
        }
        if (typeof to === 'string') {
            to = SemVerUtils.parse(to);
        }

        if (!from || !to) {
            return { type: 'invalid', direction: null };
        }

        const cmp = from.compare(to);
        const direction = cmp < 0 ? 'upgrade' : cmp > 0 ? 'downgrade' : 'same';

        const type = SemVerUtils.diff(from, to);

        return { type, direction };
    }

    /**
     * 解析版本并提取信息
     * @param {string} version - 版本字符串
     * @returns {Object|null} 版本信息
     */
    static analyze(version) {
        const v = SemVerUtils.parse(version);
        if (!v) return null;

        return {
            raw: version,
            clean: v.toCleanString(),
            full: v.toString(),
            major: v.major,
            minor: v.minor,
            patch: v.patch,
            prerelease: v.prerelease.length > 0 ? v.prerelease : null,
            build: v.build.length > 0 ? v.build : null,
            isPrerelease: v.isPrerelease(),
            isStable: v.isStable(),
            level: v.major === 0 ? 'experimental' : v.major < 1 ? 'alpha' : 'stable'
        };
    }

    /**
     * 批量验证版本
     * @param {Array<string>} versions - 版本列表
     * @returns {Object} 验证结果
     */
    static validateAll(versions) {
        const results = {
            valid: [],
            invalid: [],
            stable: [],
            prerelease: []
        };

        for (const v of versions) {
            const parsed = SemVerUtils.parse(v);
            if (parsed) {
                results.valid.push({ raw: v, version: parsed });
                if (parsed.isStable()) {
                    results.stable.push(parsed.toString());
                }
                if (parsed.isPrerelease()) {
                    results.prerelease.push(parsed.toString());
                }
            } else {
                results.invalid.push(v);
            }
        }

        return results;
    }
}

// 导出
module.exports = {
    SemVer,
    SemVerUtils
};