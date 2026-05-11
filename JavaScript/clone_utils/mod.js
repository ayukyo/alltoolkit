/**
 * Clone Utils - Deep/Shallow Clone, Deep Compare, Deep Merge Utilities
 * 
 * 零依赖，纯 JavaScript 实现
 * 
 * 功能：
 * - shallowClone: 浅克隆
 * - deepClone: 深克隆（支持循环引用、特殊对象）
 * - deepCompare: 深度比较（返回差异）
 * - deepMerge: 深度合并对象
 * - cloneJSON: JSON 安全克隆
 * - cloneWithCustomizer: 自定义克隆逻辑
 * - isDeepEqual: 深度相等判断
 * - structuralClone: 结构化克隆（现代 API）
 * - cloneWithDeps: 带依赖注入的克隆
 * 
 * @author AllToolkit
 * @date 2026-05-11
 */

/**
 * 获取值的类型
 * @param {*} value 
 * @returns {string}
 */
function getType(value) {
  if (value === null) return 'null';
  if (value === undefined) return 'undefined';
  
  const type = typeof value;
  if (type !== 'object') return type;
  
  // 特殊对象类型
  if (Array.isArray(value)) return 'array';
  if (value instanceof Date) return 'date';
  if (value instanceof RegExp) return 'regexp';
  if (value instanceof Map) return 'map';
  if (value instanceof Set) return 'set';
  if (value instanceof Error) return 'error';
  if (value instanceof ArrayBuffer) return 'arraybuffer';
  if (value instanceof DataView) return 'dataview'; // 必须在 typedarray 检测之前
  if (ArrayBuffer.isView(value)) return 'typedarray';
  if (value instanceof Promise) return 'promise';
  if (typeof value[Symbol.iterator] === 'function') return 'iterator';
  
  return 'object';
}

/**
 * 浅克隆
 * @param {*} value 
 * @returns {*}
 */
function shallowClone(value) {
  if (value === null || value === undefined) return value;
  
  const type = getType(value);
  
  switch (type) {
    case 'null':
    case 'undefined':
    case 'number':
    case 'string':
    case 'boolean':
    case 'bigint':
    case 'symbol':
    case 'function':
      return value;
      
    case 'array':
      return [...value];
      
    case 'object':
      return { ...value };
      
    case 'date':
      return new Date(value.getTime());
      
    case 'regexp':
      return new RegExp(value.source, value.flags);
      
    case 'map':
      return new Map(value);
      
    case 'set':
      return new Set(value);
      
    case 'error':
      const err = new value.constructor(value.message);
      err.stack = value.stack;
      err.name = value.name;
      err.cause = value.cause;
      return err;
      
    case 'arraybuffer':
      return value.slice(0);
      
    case 'typedarray':
      return new value.constructor(value);
      
    case 'dataview':
      return new DataView(value.buffer.slice(0), value.byteOffset, value.byteLength);
      
    default:
      // 无法浅克隆，返回原值
      return value;
  }
}

/**
 * 深克隆
 * @param {*} value - 要克隆的值
 * @param {Object} options - 选项
 * @param {WeakMap} options.cache - 内部缓存，用于处理循环引用
 * @param {number} options.depth - 最大深度，默认 Infinity
 * @param {Function} options.customizer - 自定义克隆函数
 * @returns {*}
 */
function deepClone(value, options = {}) {
  const { cache = new WeakMap(), depth = Infinity, customizer } = options;
  const currentDepth = options._currentDepth || 0;
  
  // 处理 null 和 undefined
  if (value === null || value === undefined) return value;
  
  // 原始类型直接返回
  const type = getType(value);
  if (['number', 'string', 'boolean', 'bigint', 'symbol', 'function', 'undefined', 'null'].includes(type)) {
    return value;
  }
  
  // 调用自定义克隆器
  if (customizer) {
    const customResult = customizer(value, type);
    if (customResult !== undefined) return customResult;
  }
  
  // 深度限制
  if (currentDepth >= depth) return shallowClone(value);
  
  // 检查循环引用
  if (cache.has(value)) return cache.get(value);
  
  let cloned;
  
  switch (type) {
    case 'array':
      cloned = [];
      cache.set(value, cloned);
      for (let i = 0; i < value.length; i++) {
        cloned[i] = deepClone(value[i], { cache, depth, customizer, _currentDepth: currentDepth + 1 });
      }
      break;
      
    case 'object':
      cloned = {};
      cache.set(value, cloned);
      // 复制 Symbol 属性
      const keys = [...Object.keys(value), ...Object.getOwnPropertySymbols(value)];
      for (const key of keys) {
        cloned[key] = deepClone(value[key], { cache, depth, customizer, _currentDepth: currentDepth + 1 });
      }
      // 复制原型
      Object.setPrototypeOf(cloned, Object.getPrototypeOf(value));
      break;
      
    case 'date':
      cloned = new Date(value.getTime());
      cache.set(value, cloned);
      break;
      
    case 'regexp':
      cloned = new RegExp(value.source, value.flags);
      cloned.lastIndex = value.lastIndex;
      cache.set(value, cloned);
      break;
      
    case 'map':
      cloned = new Map();
      cache.set(value, cloned);
      for (const [k, v] of value) {
        cloned.set(
          deepClone(k, { cache, depth, customizer, _currentDepth: currentDepth + 1 }),
          deepClone(v, { cache, depth, customizer, _currentDepth: currentDepth + 1 })
        );
      }
      break;
      
    case 'set':
      cloned = new Set();
      cache.set(value, cloned);
      for (const v of value) {
        cloned.add(deepClone(v, { cache, depth, customizer, _currentDepth: currentDepth + 1 }));
      }
      break;
      
    case 'error':
      cloned = new value.constructor(value.message);
      cloned.stack = value.stack;
      cloned.name = value.name;
      cloned.cause = value.cause;
      cache.set(value, cloned);
      break;
      
    case 'arraybuffer':
      cloned = value.slice(0);
      cache.set(value, cloned);
      break;
      
    case 'typedarray':
      cloned = new value.constructor(value);
      cache.set(value, cloned);
      break;
      
    case 'dataview':
      const buffer = deepClone(value.buffer, { cache, depth, customizer, _currentDepth: currentDepth + 1 });
      cloned = new DataView(buffer, value.byteOffset, value.byteLength);
      cache.set(value, cloned);
      break;
      
    case 'promise':
      // Promise 无法真正克隆，返回原值
      cloned = value;
      break;
      
    case 'iterator':
      // 迭代器转换为数组
      cloned = [...value].map(v => 
        deepClone(v, { cache, depth, customizer, _currentDepth: currentDepth + 1 })
      );
      break;
      
    default:
      cloned = value;
  }
  
  return cloned;
}

/**
 * 深度比较两个值
 * @param {*} a 
 * @param {*} b 
 * @param {Object} options 
 * @param {number} options.depth - 最大深度
 * @param {boolean} options.strict - 是否严格模式（区分 -0 和 0，区分 NaN）
 * @param {boolean} options.ignoreFunctions - 是否忽略函数比较
 * @returns {Object} { equal: boolean, differences: Array, path: string }
 */
function deepCompare(a, b, options = {}) {
  const { depth = Infinity, strict = false, ignoreFunctions = false } = options;
  
  function compare(x, y, path = '', currentDepth = 0) {
    const xType = getType(x);
    const yType = getType(y);
    
    // 类型不同
    if (xType !== yType) {
      return {
        equal: false,
        differences: [{ path, typeA: xType, typeB: yType, valueA: x, valueB: y }]
      };
    }
    
    // 原始类型
    if (['number', 'string', 'boolean', 'bigint', 'symbol', 'undefined', 'null'].includes(xType)) {
      if (strict) {
        if (Object.is(x, y)) {
          return { equal: true, differences: [] };
        } else {
          return {
            equal: false,
            differences: [{ path, typeA: xType, typeB: yType, valueA: x, valueB: y }]
          };
        }
      } else {
        if (x === y || (Number.isNaN(x) && Number.isNaN(y))) {
          return { equal: true, differences: [] };
        } else {
          return {
            equal: false,
            differences: [{ path, typeA: xType, typeB: yType, valueA: x, valueB: y }]
          };
        }
      }
    }
    
    // 函数
    if (xType === 'function') {
      if (ignoreFunctions) {
        return { equal: true, differences: [] };
      }
      return {
        equal: false,
        differences: [{ path, typeA: 'function', typeB: 'function', valueA: '[Function]', valueB: '[Function]' }]
      };
    }
    
    // 深度限制
    if (currentDepth >= depth) {
      return { equal: true, differences: [] };
    }
    
    const differences = [];
    
    switch (xType) {
      case 'array':
        if (x.length !== y.length) {
          differences.push({ path: `${path}.length`, typeA: 'number', typeB: 'number', valueA: x.length, valueB: y.length });
        }
        const maxLen = Math.max(x.length, y.length);
        for (let i = 0; i < maxLen; i++) {
          const result = compare(x[i], y[i], `${path}[${i}]`, currentDepth + 1);
          differences.push(...result.differences);
        }
        break;
        
      case 'object':
        const xKeys = [...Object.keys(x), ...Object.getOwnPropertySymbols(x)];
        const yKeys = [...Object.keys(y), ...Object.getOwnPropertySymbols(y)];
        const allKeys = new Set([...xKeys, ...yKeys]);
        
        for (const key of allKeys) {
          const keyPath = typeof key === 'symbol' ? `${path}[Symbol(${key.description})]` : `${path}.${key}`;
          if (!(key in x)) {
            differences.push({ path: keyPath, typeA: 'undefined', typeB: getType(y[key]), valueA: undefined, valueB: y[key] });
          } else if (!(key in y)) {
            differences.push({ path: keyPath, typeA: getType(x[key]), typeB: 'undefined', valueA: x[key], valueB: undefined });
          } else {
            const result = compare(x[key], y[key], keyPath, currentDepth + 1);
            differences.push(...result.differences);
          }
        }
        break;
        
      case 'date':
        if (x.getTime() !== y.getTime()) {
          differences.push({ path, typeA: 'date', typeB: 'date', valueA: x.toISOString(), valueB: y.toISOString() });
        }
        break;
        
      case 'regexp':
        if (x.source !== y.source || x.flags !== y.flags) {
          differences.push({ path, typeA: 'regexp', typeB: 'regexp', valueA: x.toString(), valueB: y.toString() });
        }
        break;
        
      case 'map':
        if (x.size !== y.size) {
          differences.push({ path: `${path}.size`, typeA: 'number', typeB: 'number', valueA: x.size, valueB: y.size });
        }
        for (const [key, val] of x) {
          if (!y.has(key)) {
            differences.push({ path: `${path}[Map(${key})]`, typeA: getType(val), typeB: 'undefined', valueA: val, valueB: undefined });
          } else {
            const result = compare(val, y.get(key), `${path}[Map(${key})]`, currentDepth + 1);
            differences.push(...result.differences);
          }
        }
        for (const [key, val] of y) {
          if (!x.has(key)) {
            differences.push({ path: `${path}[Map(${key})]`, typeA: 'undefined', typeB: getType(val), valueA: undefined, valueB: val });
          }
        }
        break;
        
      case 'set':
        if (x.size !== y.size) {
          differences.push({ path: `${path}.size`, typeA: 'number', typeB: 'number', valueA: x.size, valueB: y.size });
        }
        for (const val of x) {
          if (!y.has(val)) {
            differences.push({ path: `${path}[Set(${val})]`, typeA: getType(val), typeB: 'undefined', valueA: val, valueB: undefined });
          }
        }
        for (const val of y) {
          if (!x.has(val)) {
            differences.push({ path: `${path}[Set(${val})]`, typeA: 'undefined', typeB: getType(val), valueA: undefined, valueB: val });
          }
        }
        break;
        
      case 'arraybuffer':
        const xView = new Uint8Array(x);
        const yView = new Uint8Array(y);
        if (x.byteLength !== y.byteLength) {
          differences.push({ path, typeA: 'arraybuffer', typeB: 'arraybuffer', valueA: `size:${x.byteLength}`, valueB: `size:${y.byteLength}` });
        } else {
          for (let i = 0; i < x.byteLength; i++) {
            if (xView[i] !== yView[i]) {
              differences.push({ path: `${path}[${i}]`, typeA: 'number', typeB: 'number', valueA: xView[i], valueB: yView[i] });
            }
          }
        }
        break;
        
      case 'typedarray':
        if (x.length !== y.length || x.constructor !== y.constructor) {
          differences.push({ path, typeA: xType, typeB: yType, valueA: `length:${x.length}`, valueB: `length:${y.length}` });
        } else {
          for (let i = 0; i < x.length; i++) {
            if (x[i] !== y[i]) {
              differences.push({ path: `${path}[${i}]`, typeA: 'number', typeB: 'number', valueA: x[i], valueB: y[i] });
            }
          }
        }
        break;
        
      default:
        // 其他类型直接比较
        if (x !== y) {
          differences.push({ path, typeA: xType, typeB: yType, valueA: String(x), valueB: String(y) });
        }
    }
    
    return { equal: differences.length === 0, differences };
  }
  
  return compare(a, b);
}

/**
 * 深度合并对象
 * @param {*} target - 目标对象
 * @param {...*} sources - 源对象
 * @returns {*}
 */
function deepMerge(target, ...sources) {
  const cache = new WeakMap();
  
  function merge(t, s, currentDepth = 0) {
    if (currentDepth > 100) return s; // 防止无限递归
    
    const tType = getType(t);
    const sType = getType(s);
    
    // 源为 null/undefined，保留目标
    if (s === null || s === undefined) return t;
    
    // 目标为 null/undefined 或类型不同，返回源
    if (t === null || t === undefined || tType !== sType) {
      return deepClone(s, { cache });
    }
    
    // 原始类型直接返回源
    if (!['object', 'array', 'map', 'set'].includes(tType)) {
      return s;
    }
    
    // 检查循环引用
    if (cache.has(s)) return cache.get(s);
    
    let result;
    
    switch (tType) {
      case 'object':
        result = deepClone(t, { cache });
        cache.set(s, result);
        const sKeys = [...Object.keys(s), ...Object.getOwnPropertySymbols(s)];
        for (const key of sKeys) {
          result[key] = merge(t[key], s[key], currentDepth + 1);
        }
        break;
        
      case 'array':
        result = deepClone(t, { cache });
        cache.set(s, result);
        for (let i = 0; i < s.length; i++) {
          result[i] = merge(t[i], s[i], currentDepth + 1);
        }
        break;
        
      case 'map':
        result = new Map(t);
        cache.set(s, result);
        for (const [k, v] of s) {
          result.set(k, merge(t.get(k), v, currentDepth + 1));
        }
        break;
        
      case 'set':
        // Set 直接用源的值
        result = deepClone(s, { cache });
        break;
        
      default:
        result = s;
    }
    
    return result;
  }
  
  let result = target;
  for (const source of sources) {
    result = merge(result, source);
  }
  
  return result;
}

/**
 * JSON 安全克隆
 * @param {*} value 
 * @returns {*}
 */
function cloneJSON(value) {
  return JSON.parse(JSON.stringify(value));
}

/**
 * 自定义克隆
 * @param {*} value 
 * @param {Object} customizers - 类型到克隆函数的映射
 * @returns {*}
 */
function cloneWithCustomizer(value, customizers = {}) {
  return deepClone(value, {
    customizer: (val, type) => {
      if (customizers[type]) {
        return customizers[type](val);
      }
      return undefined; // 使用默认行为
    }
  });
}

/**
 * 深度相等判断
 * @param {*} a 
 * @param {*} b 
 * @param {Object} options 
 * @returns {boolean}
 */
function isDeepEqual(a, b, options = {}) {
  return deepCompare(a, b, options).equal;
}

/**
 * 结构化克隆（使用现代 API）
 * 某些类型无法克隆：Function、Error、DOM 节点等
 * @param {*} value 
 * @returns {*}
 */
function structuralClone(value) {
  // Node.js 环境
  if (typeof structuredClone === 'function') {
    return structuredClone(value);
  }
  
  // 浏览器环境 fallback
  if (typeof window !== 'undefined') {
    // 使用 MessageChannel
    return new Promise((resolve, reject) => {
      const { port1, port2 } = new MessageChannel();
      port2.onmessage = (e) => resolve(e.data);
      port2.onmessageerror = (e) => reject(e);
      port1.postMessage(value);
    });
  }
  
  // 最终 fallback：JSON 克隆
  return cloneJSON(value);
}

/**
 * 带依赖注入的克隆
 * 允许替换特定值的引用
 * @param {*} value 
 * @param {Map} deps - 依赖映射
 * @param {Object} options 
 * @returns {*}
 */
function cloneWithDeps(value, deps = new Map(), options = {}) {
  // 使用自定义克隆器来替换依赖
  return deepClone(value, {
    cache: options.cache || new WeakMap(),
    depth: options.depth,
    customizer: (val, type) => {
      // 先检查依赖替换
      if (deps.has(val)) {
        return deps.get(val);
      }
      // 对于原始类型，返回 undefined 让默认处理
      if (['number', 'string', 'boolean', 'bigint', 'symbol', 'function', 'undefined', 'null'].includes(type)) {
        return undefined;
      }
      return undefined;
    }
  });
}

/**
 * 选择性克隆 - 只克隆指定属性
 * @param {*} value 
 * @param {Array} keys - 要克隆的属性名数组
 * @param {Object} options 
 * @returns {*}
 */
function clonePick(value, keys, options = {}) {
  if (getType(value) !== 'object') return value;
  
  const result = {};
  for (const key of keys) {
    if (key in value) {
      result[key] = deepClone(value[key], options);
    }
  }
  return result;
}

/**
 * 排除性克隆 - 排除指定属性
 * @param {*} value 
 * @param {Array} keys - 要排除的属性名数组
 * @param {Object} options 
 * @returns {*}
 */
function cloneOmit(value, keys, options = {}) {
  if (getType(value) !== 'object') return value;
  
  const keySet = new Set(keys);
  const result = {};
  for (const key of Object.keys(value)) {
    if (!keySet.has(key)) {
      result[key] = deepClone(value[key], options);
    }
  }
  // 处理 Symbol 属性
  for (const sym of Object.getOwnPropertySymbols(value)) {
    if (!keySet.has(sym)) {
      result[sym] = deepClone(value[sym], options);
    }
  }
  return result;
}

// 导出所有函数
module.exports = {
  getType,
  shallowClone,
  deepClone,
  deepCompare,
  deepMerge,
  cloneJSON,
  cloneWithCustomizer,
  isDeepEqual,
  structuralClone,
  cloneWithDeps,
  clonePick,
  cloneOmit
};