/**
 * Cache Utilities - JavaScript 缓存工具模块
 * 
 * 提供多种缓存实现，包括 LRU、LFU、TTL 缓存等
 * 零依赖，仅使用 JavaScript 标准库
 * 
 * @module cache_utils
 * @version 1.0.0
 */

// ============================================================================
// LRU Cache (Least Recently Used)
// ============================================================================

/**
 * LRU 缓存 - 最近最少使用淘汰策略
 * 当缓存满时，淘汰最久未使用的条目
 */
class LRUCache {
  /**
   * 创建 LRU 缓存实例
   * @param {number} capacity - 最大容量
   */
  constructor(capacity = 100) {
    if (capacity <= 0) {
      throw new Error('Capacity must be positive');
    }
    this.capacity = capacity;
    this.cache = new Map(); // 使用 Map 保持插入顺序
    this.hits = 0;
    this.misses = 0;
  }

  /**
   * 获取缓存值
   * @param {string} key - 键
   * @returns {*} - 值（不存在返回 undefined）
   */
  get(key) {
    if (!this.cache.has(key)) {
      this.misses++;
      return undefined;
    }
    // 删除并重新插入，使其成为最新
    const value = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, value);
    this.hits++;
    return value;
  }

  /**
   * 设置缓存值
   * @param {string} key - 键
   * @param {*} value - 值
   * @returns {boolean} - 是否成功
   */
  set(key, value) {
    // 如果已存在，先删除
    if (this.cache.has(key)) {
      this.cache.delete(key);
    }
    // 如果容量已满，删除最老的条目
    else if (this.cache.size >= this.capacity) {
      const oldestKey = this.cache.keys().next().value;
      this.cache.delete(oldestKey);
    }
    this.cache.set(key, value);
    return true;
  }

  /**
   * 检查键是否存在
   * @param {string} key - 键
   * @returns {boolean}
   */
  has(key) {
    return this.cache.has(key);
  }

  /**
   * 删除缓存条目
   * @param {string} key - 键
   * @returns {boolean} - 是否删除成功
   */
  delete(key) {
    return this.cache.delete(key);
  }

  /**
   * 清空缓存
   */
  clear() {
    this.cache.clear();
    this.hits = 0;
    this.misses = 0;
  }

  /**
   * 获取当前大小
   * @returns {number}
   */
  get size() {
    return this.cache.size;
  }

  /**
   * 获取所有键
   * @returns {Array}
   */
  keys() {
    return Array.from(this.cache.keys());
  }

  /**
   * 获取所有值
   * @returns {Array}
   */
  values() {
    return Array.from(this.cache.values());
  }

  /**
   * 获取命中率
   * @returns {number} - 命中率（0-1）
   */
  getHitRate() {
    const total = this.hits + this.misses;
    return total === 0 ? 0 : this.hits / total;
  }

  /**
   * 获取缓存统计信息
   * @returns {Object}
   */
  getStats() {
    return {
      size: this.cache.size,
      capacity: this.capacity,
      hits: this.hits,
      misses: this.misses,
      hitRate: this.getHitRate()
    };
  }
}

// ============================================================================
// LFU Cache (Least Frequently Used)
// ============================================================================

/**
 * LFU 缓存节点
 */
class LFUNode {
  constructor(key, value) {
    this.key = key;
    this.value = value;
    this.frequency = 1;
    this.timestamp = Date.now();
  }
}

/**
 * LFU 缓存 - 最不经常使用淘汰策略
 * 当缓存满时，淘汰访问频率最低的条目
 */
class LFUCache {
  /**
   * 创建 LFU 缓存实例
   * @param {number} capacity - 最大容量
   */
  constructor(capacity = 100) {
    if (capacity <= 0) {
      throw new Error('Capacity must be positive');
    }
    this.capacity = capacity;
    this.cache = new Map();
    this.minFrequency = 1;
    this.frequencyMap = new Map(); // frequency -> Set of keys
    this.hits = 0;
    this.misses = 0;
  }

  /**
   * 更新条目的频率
   * @private
   */
  _updateFrequency(key) {
    const node = this.cache.get(key);
    if (!node) return;

    const oldFreq = node.frequency;
    node.frequency++;
    node.timestamp = Date.now();

    // 从旧频率集合中移除
    const oldFreqSet = this.frequencyMap.get(oldFreq);
    if (oldFreqSet) {
      oldFreqSet.delete(key);
      if (oldFreqSet.size === 0) {
        this.frequencyMap.delete(oldFreq);
        if (this.minFrequency === oldFreq) {
          this.minFrequency = node.frequency;
        }
      }
    }

    // 添加到新频率集合
    if (!this.frequencyMap.has(node.frequency)) {
      this.frequencyMap.set(node.frequency, new Set());
    }
    this.frequencyMap.get(node.frequency).add(key);
  }

  /**
   * 获取缓存值
   * @param {string} key - 键
   * @returns {*} - 值
   */
  get(key) {
    if (!this.cache.has(key)) {
      this.misses++;
      return undefined;
    }
    this._updateFrequency(key);
    this.hits++;
    return this.cache.get(key).value;
  }

  /**
   * 设置缓存值
   * @param {string} key - 键
   * @param {*} value - 值
   * @returns {boolean}
   */
  set(key, value) {
    if (this.cache.has(key)) {
      // 更新现有条目
      const node = this.cache.get(key);
      node.value = value;
      this._updateFrequency(key);
    } else {
      // 新条目
      if (this.cache.size >= this.capacity) {
        // 淘汰频率最低的条目
        this._evict();
      }

      const node = new LFUNode(key, value);
      this.cache.set(key, node);
      this.minFrequency = 1;

      if (!this.frequencyMap.has(1)) {
        this.frequencyMap.set(1, new Set());
      }
      this.frequencyMap.get(1).add(key);
    }
    return true;
  }

  /**
   * 淘汰条目
   * @private
   */
  _evict() {
    const minFreqSet = this.frequencyMap.get(this.minFrequency);
    if (!minFreqSet || minFreqSet.size === 0) return;

    // 找到最旧的条目（频率相同的情况下，淘汰最久未使用）
    let oldestKey = null;
    let oldestTime = Infinity;

    for (const key of minFreqSet) {
      const node = this.cache.get(key);
      if (node && node.timestamp < oldestTime) {
        oldestTime = node.timestamp;
        oldestKey = key;
      }
    }

    if (oldestKey) {
      this.cache.delete(oldestKey);
      minFreqSet.delete(oldestKey);
      if (minFreqSet.size === 0) {
        this.frequencyMap.delete(this.minFrequency);
      }
    }
  }

  /**
   * 检查键是否存在
   * @param {string} key - 键
   * @returns {boolean}
   */
  has(key) {
    return this.cache.has(key);
  }

  /**
   * 删除缓存条目
   * @param {string} key - 键
   * @returns {boolean}
   */
  delete(key) {
    if (!this.cache.has(key)) return false;

    const node = this.cache.get(key);
    const freq = node.frequency;
    
    const freqSet = this.frequencyMap.get(freq);
    if (freqSet) {
      freqSet.delete(key);
      if (freqSet.size === 0) {
        this.frequencyMap.delete(freq);
      }
    }

    return this.cache.delete(key);
  }

  /**
   * 清空缓存
   */
  clear() {
    this.cache.clear();
    this.frequencyMap.clear();
    this.minFrequency = 1;
    this.hits = 0;
    this.misses = 0;
  }

  /**
   * 获取当前大小
   * @returns {number}
   */
  get size() {
    return this.cache.size;
  }

  /**
   * 获取命中率
   * @returns {number}
   */
  getHitRate() {
    const total = this.hits + this.misses;
    return total === 0 ? 0 : this.hits / total;
  }

  /**
   * 获取缓存统计信息
   * @returns {Object}
   */
  getStats() {
    return {
      size: this.cache.size,
      capacity: this.capacity,
      hits: this.hits,
      misses: this.misses,
      hitRate: this.getHitRate(),
      minFrequency: this.minFrequency
    };
  }
}

// ============================================================================
// TTL Cache (Time To Live)
// ============================================================================

/**
 * TTL 缓存条目
 */
class TTLEntry {
  constructor(key, value, ttl) {
    this.key = key;
    this.value = value;
    this.expiresAt = ttl > 0 ? Date.now() + ttl : Infinity;
    this.ttl = ttl;
  }

  isExpired() {
    return Date.now() > this.expiresAt;
  }
}

/**
 * TTL 缓存 - 带过期时间的缓存
 * 条目在指定时间后自动过期
 */
class TTLCache {
  /**
   * 创建 TTL 缓存实例
   * @param {Object} options - 配置选项
   * @param {number} options.defaultTTL - 默认过期时间（毫秒）
   * @param {number} options.maxSize - 最大容量（可选）
   * @param {number} options.cleanupInterval - 清理间隔（毫秒，可选）
   */
  constructor(options = {}) {
    this.cache = new Map();
    this.defaultTTL = options.defaultTTL || 60000; // 默认 1 分钟
    this.maxSize = options.maxSize || Infinity;
    this.cleanupInterval = options.cleanupInterval;
    this.cleanupTimer = null;
    this.hits = 0;
    this.misses = 0;
    this.expirations = 0;

    if (this.cleanupInterval) {
      this._startCleanup();
    }
  }

  /**
   * 启动自动清理
   * @private
   */
  _startCleanup() {
    this.cleanupTimer = setInterval(() => {
      this.cleanup();
    }, this.cleanupInterval);
  }

  /**
   * 停止自动清理
   */
  stopCleanup() {
    if (this.cleanupTimer) {
      clearInterval(this.cleanupTimer);
      this.cleanupTimer = null;
    }
  }

  /**
   * 清理过期条目
   * @returns {number} - 清理的条目数
   */
  cleanup() {
    let cleaned = 0;
    for (const [key, entry] of this.cache) {
      if (entry.isExpired()) {
        this.cache.delete(key);
        cleaned++;
        this.expirations++;
      }
    }
    return cleaned;
  }

  /**
   * 获取缓存值
   * @param {string} key - 键
   * @returns {*} - 值
   */
  get(key) {
    const entry = this.cache.get(key);
    
    if (!entry) {
      this.misses++;
      return undefined;
    }

    if (entry.isExpired()) {
      this.cache.delete(key);
      this.misses++;
      this.expirations++;
      return undefined;
    }

    this.hits++;
    return entry.value;
  }

  /**
   * 设置缓存值
   * @param {string} key - 键
   * @param {*} value - 值
   * @param {number} ttl - 过期时间（毫秒，可选，使用默认值）
   * @returns {boolean}
   */
  set(key, value, ttl) {
    // 如果容量已满，先清理过期条目
    if (this.cache.size >= this.maxSize) {
      this.cleanup();
      // 如果还是满的，删除最老的条目
      if (this.cache.size >= this.maxSize) {
        const firstKey = this.cache.keys().next().value;
        this.cache.delete(firstKey);
      }
    }

    const actualTTL = ttl !== undefined ? ttl : this.defaultTTL;
    this.cache.set(key, new TTLEntry(key, value, actualTTL));
    return true;
  }

  /**
   * 检查键是否存在且未过期
   * @param {string} key - 键
   * @returns {boolean}
   */
  has(key) {
    const entry = this.cache.get(key);
    if (!entry) return false;
    if (entry.isExpired()) {
      this.cache.delete(key);
      return false;
    }
    return true;
  }

  /**
   * 删除缓存条目
   * @param {string} key - 键
   * @returns {boolean}
   */
  delete(key) {
    return this.cache.delete(key);
  }

  /**
   * 清空缓存
   */
  clear() {
    this.cache.clear();
    this.hits = 0;
    this.misses = 0;
    this.expirations = 0;
  }

  /**
   * 获取当前大小
   * @returns {number}
   */
  get size() {
    return this.cache.size;
  }

  /**
   * 获取条目的剩余时间
   * @param {string} key - 键
   * @returns {number} - 剩余时间（毫秒），不存在或已过期返回 0
   */
  getRemainingTTL(key) {
    const entry = this.cache.get(key);
    if (!entry || entry.isExpired()) return 0;
    return Math.max(0, entry.expiresAt - Date.now());
  }

  /**
   * 刷新条目的过期时间
   * @param {string} key - 键
   * @param {number} ttl - 新的过期时间（毫秒，可选）
   * @returns {boolean}
   */
  refresh(key, ttl) {
    const entry = this.cache.get(key);
    if (!entry || entry.isExpired()) return false;

    const actualTTL = ttl !== undefined ? ttl : entry.ttl;
    entry.expiresAt = actualTTL > 0 ? Date.now() + actualTTL : Infinity;
    return true;
  }

  /**
   * 获取命中率
   * @returns {number}
   */
  getHitRate() {
    const total = this.hits + this.misses;
    return total === 0 ? 0 : this.hits / total;
  }

  /**
   * 获取缓存统计信息
   * @returns {Object}
   */
  getStats() {
    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      hits: this.hits,
      misses: this.misses,
      expirations: this.expirations,
      hitRate: this.getHitRate()
    };
  }
}

// ============================================================================
// Memory Cache (Simple In-Memory Cache)
// ============================================================================

/**
 * 简单内存缓存
 * 提供基本的缓存功能，支持过期时间和最大容量
 */
class MemoryCache {
  /**
   * 创建内存缓存实例
   * @param {Object} options - 配置选项
   */
  constructor(options = {}) {
    this.cache = new Map();
    this.maxSize = options.maxSize || 1000;
    this.defaultTTL = options.defaultTTL || 0; // 0 表示永不过期
    this.hits = 0;
    this.misses = 0;
  }

  /**
   * 获取缓存值
   * @param {string} key - 键
   * @param {*} defaultValue - 默认值（可选）
   * @returns {*}
   */
  get(key, defaultValue = undefined) {
    const entry = this.cache.get(key);
    
    if (!entry) {
      this.misses++;
      return defaultValue;
    }

    // 检查是否过期
    if (entry.expiresAt && Date.now() > entry.expiresAt) {
      this.cache.delete(key);
      this.misses++;
      return defaultValue;
    }

    this.hits++;
    return entry.value;
  }

  /**
   * 设置缓存值
   * @param {string} key - 键
   * @param {*} value - 值
   * @param {number} ttl - 过期时间（毫秒，可选）
   * @returns {boolean}
   */
  set(key, value, ttl) {
    // 如果达到最大容量，删除最旧的条目
    if (this.cache.size >= this.maxSize && !this.cache.has(key)) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }

    const actualTTL = ttl !== undefined ? ttl : this.defaultTTL;
    this.cache.set(key, {
      value,
      expiresAt: actualTTL > 0 ? Date.now() + actualTTL : null,
      createdAt: Date.now()
    });
    
    return true;
  }

  /**
   * 如果不存在则设置
   * @param {string} key - 键
   * @param {*} value - 值
   * @param {number} ttl - 过期时间（毫秒，可选）
   * @returns {boolean} - 是否设置成功（不存在时）
   */
  setNX(key, value, ttl) {
    if (this.has(key)) return false;
    return this.set(key, value, ttl);
  }

  /**
   * 获取并删除
   * @param {string} key - 键
   * @returns {*}
   */
  take(key) {
    const value = this.get(key);
    if (value !== undefined) {
      this.cache.delete(key);
    }
    return value;
  }

  /**
   * 检查键是否存在
   * @param {string} key - 键
   * @returns {boolean}
   */
  has(key) {
    const entry = this.cache.get(key);
    if (!entry) return false;
    
    // 检查是否过期
    if (entry.expiresAt && Date.now() > entry.expiresAt) {
      this.cache.delete(key);
      return false;
    }
    
    return true;
  }

  /**
   * 删除缓存条目
   * @param {string} key - 键
   * @returns {boolean}
   */
  delete(key) {
    return this.cache.delete(key);
  }

  /**
   * 清空缓存
   */
  clear() {
    this.cache.clear();
    this.hits = 0;
    this.misses = 0;
  }

  /**
   * 获取当前大小
   * @returns {number}
   */
  get size() {
    return this.cache.size;
  }

  /**
   * 获取所有键
   * @returns {Array}
   */
  keys() {
    return Array.from(this.cache.keys());
  }

  /**
   * 遍历缓存
   * @param {Function} callback - 回调函数 (value, key)
   */
  forEach(callback) {
    this.cache.forEach((entry, key) => {
      // 跳过过期条目
      if (!entry.expiresAt || Date.now() <= entry.expiresAt) {
        callback(entry.value, key);
      }
    });
  }

  /**
   * 获取命中率
   * @returns {number}
   */
  getHitRate() {
    const total = this.hits + this.misses;
    return total === 0 ? 0 : this.hits / total;
  }

  /**
   * 获取缓存统计信息
   * @returns {Object}
   */
  getStats() {
    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      hits: this.hits,
      misses: this.misses,
      hitRate: this.getHitRate()
    };
  }
}

// ============================================================================
// Two-Level Cache
// ============================================================================

/**
 * 两级缓存
 * L1 为快速小容量缓存，L2 为慢速大容量缓存
 */
class TwoLevelCache {
  /**
   * 创建两级缓存实例
   * @param {Object} options - 配置选项
   */
  constructor(options = {}) {
    this.l1 = new LRUCache(options.l1Capacity || 100);
    this.l2 = new TTLCache({
      maxSize: options.l2Capacity || 1000,
      defaultTTL: options.l2TTL || 300000 // 默认 5 分钟
    });
    this.hits = 0;
    this.misses = 0;
    this.l1Hits = 0;
    this.l2Hits = 0;
  }

  /**
   * 获取缓存值
   * @param {string} key - 键
   * @returns {*}
   */
  get(key) {
    // 先查 L1
    const l1Value = this.l1.get(key);
    if (l1Value !== undefined) {
      this.hits++;
      this.l1Hits++;
      return l1Value;
    }

    // 再查 L2
    const l2Value = this.l2.get(key);
    if (l2Value !== undefined) {
      // 回填到 L1
      this.l1.set(key, l2Value);
      this.hits++;
      this.l2Hits++;
      return l2Value;
    }

    this.misses++;
    return undefined;
  }

  /**
   * 设置缓存值
   * @param {string} key - 键
   * @param {*} value - 值
   * @param {number} ttl - L2 过期时间（毫秒，可选）
   * @returns {boolean}
   */
  set(key, value, ttl) {
    this.l1.set(key, value);
    this.l2.set(key, value, ttl);
    return true;
  }

  /**
   * 检查键是否存在
   * @param {string} key - 键
   * @returns {boolean}
   */
  has(key) {
    return this.l1.has(key) || this.l2.has(key);
  }

  /**
   * 删除缓存条目
   * @param {string} key - 键
   * @returns {boolean}
   */
  delete(key) {
    const l1Deleted = this.l1.delete(key);
    const l2Deleted = this.l2.delete(key);
    return l1Deleted || l2Deleted;
  }

  /**
   * 清空缓存
   */
  clear() {
    this.l1.clear();
    this.l2.clear();
    this.hits = 0;
    this.misses = 0;
    this.l1Hits = 0;
    this.l2Hits = 0;
  }

  /**
   * 获取命中率
   * @returns {number}
   */
  getHitRate() {
    const total = this.hits + this.misses;
    return total === 0 ? 0 : this.hits / total;
  }

  /**
   * 获取缓存统计信息
   * @returns {Object}
   */
  getStats() {
    return {
      l1Size: this.l1.size,
      l2Size: this.l2.size,
      hits: this.hits,
      misses: this.misses,
      l1Hits: this.l1Hits,
      l2Hits: this.l2Hits,
      hitRate: this.getHitRate()
    };
  }
}

// ============================================================================
// Decorator Functions
// ============================================================================

/**
 * 创建带缓存的函数
 * 自动缓存函数调用的结果
 * @param {Function} fn - 要缓存的函数
 * @param {Object} options - 缓存选项
 * @returns {Function}
 */
function memoize(fn, options = {}) {
  const cache = new TTLCache({
    defaultTTL: options.ttl || 60000,
    maxSize: options.maxSize || 100
  });

  const memoized = function(...args) {
    const key = options.keyFn 
      ? options.keyFn(...args) 
      : JSON.stringify(args);

    let result = cache.get(key);
    if (result === undefined) {
      result = fn.apply(this, args);
      cache.set(key, result);
    }

    return result;
  };

  // 添加缓存控制方法
  memoized.cache = cache;
  memoized.clear = () => cache.clear();
  memoized.getStats = () => cache.getStats();

  return memoized;
}

/**
 * 创建异步缓存装饰器
 * 对于异步函数，缓存 Promise 结果
 * @param {Function} fn - 异步函数
 * @param {Object} options - 缓存选项
 * @returns {Function}
 */
function memoizeAsync(fn, options = {}) {
  const cache = new TTLCache({
    defaultTTL: options.ttl || 60000,
    maxSize: options.maxSize || 100
  });
  const pending = new Map(); // 防止重复请求

  const memoized = async function(...args) {
    const key = options.keyFn 
      ? options.keyFn(...args) 
      : JSON.stringify(args);

    // 检查缓存
    const cached = cache.get(key);
    if (cached !== undefined) {
      return cached;
    }

    // 检查是否有进行中的请求
    if (pending.has(key)) {
      return pending.get(key);
    }

    // 发起新请求
    const promise = fn.apply(this, args)
      .then(result => {
        cache.set(key, result);
        pending.delete(key);
        return result;
      })
      .catch(error => {
        pending.delete(key);
        throw error;
      });

    pending.set(key, promise);
    return promise;
  };

  memoized.cache = cache;
  memoized.clear = () => cache.clear();
  memoized.getStats = () => cache.getStats();

  return memoized;
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * 创建缓存键
 * @param {...*} args - 参数
 * @returns {string}
 */
function createCacheKey(...args) {
  return args.map(arg => {
    if (arg === null) return 'null';
    if (arg === undefined) return 'undefined';
    if (typeof arg === 'object') return JSON.stringify(arg);
    return String(arg);
  }).join(':');
}

/**
 * 批量获取缓存值
 * @param {LRUCache|LFUCache|TTLCache|MemoryCache} cache - 缓存实例
 * @param {Array} keys - 键数组
 * @returns {Object} - 键值对对象
 */
function multiGet(cache, keys) {
  const result = {};
  for (const key of keys) {
    const value = cache.get(key);
    if (value !== undefined) {
      result[key] = value;
    }
  }
  return result;
}

/**
 * 批量设置缓存值
 * @param {LRUCache|LFUCache|TTLCache|MemoryCache} cache - 缓存实例
 * @param {Object} entries - 键值对对象
 * @param {number} ttl - 过期时间（仅对 TTLCache 有效）
 */
function multiSet(cache, entries, ttl) {
  for (const [key, value] of Object.entries(entries)) {
    cache.set(key, value, ttl);
  }
}

// ============================================================================
// Exports
// ============================================================================

module.exports = {
  // Cache classes
  LRUCache,
  LFUCache,
  TTLCache,
  MemoryCache,
  TwoLevelCache,
  
  // Decorator functions
  memoize,
  memoizeAsync,
  
  // Utility functions
  createCacheKey,
  multiGet,
  multiSet
};