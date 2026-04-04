/**
 * Array Utilities - JavaScript 数组工具模块
 * 
 * 提供常用的数组操作函数，包括去重、分组、分块、排序、查找等
 * 零依赖，仅使用 JavaScript 标准库
 * 
 * @module array_utils
 * @version 1.0.0
 */

const ArrayUtils = {
  /**
   * 检查数组是否为空或 null/undefined
   * @param {*} arr - 要检查的数组
   * @returns {boolean} - 是否为空
   */
  isEmpty(arr) {
    return !arr || !Array.isArray(arr) || arr.length === 0;
  },

  /**
   * 检查数组是否非空
   * @param {*} arr - 要检查的数组
   * @returns {boolean} - 是否非空
   */
  isNotEmpty(arr) {
    return Array.isArray(arr) && arr.length > 0;
  },

  /**
   * 数组去重（保留原顺序）
   * @param {Array} arr - 输入数组
   * @returns {Array} - 去重后的数组
   */
  unique(arr) {
    if (!Array.isArray(arr)) return [];
    return [...new Set(arr)];
  },

  /**
   * 根据条件去重
   * @param {Array} arr - 输入数组
   * @param {Function} keyFn - 生成唯一键的函数
   * @returns {Array} - 去重后的数组
   */
  uniqueBy(arr, keyFn) {
    if (!Array.isArray(arr) || !keyFn) return [];
    const seen = new Set();
    return arr.filter(item => {
      const key = keyFn(item);
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  },

  /**
   * 数组分组
   * @param {Array} arr - 输入数组
   * @param {Function|string} keyFn - 分组键函数或属性名
   * @returns {Object} - 分组后的对象
   */
  groupBy(arr, keyFn) {
    if (!Array.isArray(arr)) return {};
    const getKey = typeof keyFn === 'function' 
      ? keyFn 
      : item => item?.[keyFn];
    
    return arr.reduce((groups, item) => {
      const key = getKey(item);
      if (!groups[key]) groups[key] = [];
      groups[key].push(item);
      return groups;
    }, {});
  },

  /**
   * 数组分块
   * @param {Array} arr - 输入数组
   * @param {number} size - 每块大小
   * @returns {Array[]} - 分块后的数组
   */
  chunk(arr, size) {
    if (!Array.isArray(arr) || size <= 0) return [];
    const chunks = [];
    for (let i = 0; i < arr.length; i += size) {
      chunks.push(arr.slice(i, i + size));
    }
    return chunks;
  },

  /**
   * 数组扁平化（一级）
   * @param {Array} arr - 输入数组
   * @returns {Array} - 扁平化后的数组
   */
  flatten(arr) {
    if (!Array.isArray(arr)) return [];
    return arr.flat();
  },

  /**
   * 深度扁平化
   * @param {Array} arr - 输入数组
   * @param {number} depth - 深度（默认 Infinity）
   * @returns {Array} - 扁平化后的数组
   */
  flattenDeep(arr, depth = Infinity) {
    if (!Array.isArray(arr)) return [];
    return arr.flat(depth);
  },

  /**
   * 获取数组交集
   * @param {Array} arr1 - 第一个数组
   * @param {Array} arr2 - 第二个数组
   * @returns {Array} - 交集数组
   */
  intersection(arr1, arr2) {
    if (!Array.isArray(arr1) || !Array.isArray(arr2)) return [];
    const set2 = new Set(arr2);
    return [...new Set(arr1.filter(item => set2.has(item)))];
  },

  /**
   * 获取数组并集
   * @param {Array} arr1 - 第一个数组
   * @param {Array} arr2 - 第二个数组
   * @returns {Array} - 并集数组
   */
  union(arr1, arr2) {
    if (!Array.isArray(arr1) || !Array.isArray(arr2)) return [];
    return [...new Set([...arr1, ...arr2])];
  },

  /**
   * 获取数组差集（在 arr1 中但不在 arr2 中）
   * @param {Array} arr1 - 第一个数组
   * @param {Array} arr2 - 第二个数组
   * @returns {Array} - 差集数组
   */
  difference(arr1, arr2) {
    if (!Array.isArray(arr1) || !Array.isArray(arr2)) return [];
    const set2 = new Set(arr2);
    return arr1.filter(item => !set2.has(item));
  },

  /**
   * 获取对称差集（只在其中一个数组中）
   * @param {Array} arr1 - 第一个数组
   * @param {Array} arr2 - 第二个数组
   * @returns {Array} - 对称差集数组
   */
  symmetricDifference(arr1, arr2) {
    if (!Array.isArray(arr1) || !Array.isArray(arr2)) return [];
    const set1 = new Set(arr1);
    const set2 = new Set(arr2);
    return [
      ...arr1.filter(item => !set2.has(item)),
      ...arr2.filter(item => !set1.has(item))
    ];
  },

  /**
   * 数组排序（支持多字段）
   * @param {Array} arr - 输入数组
   * @param {string|Function} key - 排序键或函数
   * @param {string} order - 排序方向 ('asc' 或 'desc')
   * @returns {Array} - 排序后的新数组
   */
  sortBy(arr, key, order = 'asc') {
    if (!Array.isArray(arr)) return [];
    const multiplier = order === 'desc' ? -1 : 1;
    const getValue = typeof key === 'function' 
      ? key 
      : item => item?.[key];
    
    return [...arr].sort((a, b) => {
      const valA = getValue(a);
      const valB = getValue(b);
      if (valA < valB) return -1 * multiplier;
      if (valA > valB) return 1 * multiplier;
      return 0;
    });
  },

  /**
   * 随机打乱数组（Fisher-Yates 算法）
   * @param {Array} arr - 输入数组
   * @returns {Array} - 打乱后的新数组
   */
  shuffle(arr) {
    if (!Array.isArray(arr)) return [];
    const result = [...arr];
    for (let i = result.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  },

  /**
   * 从数组中随机取样
   * @param {Array} arr - 输入数组
   * @param {number} count - 取样数量
   * @returns {Array} - 取样结果
   */
  sample(arr, count = 1) {
    if (!Array.isArray(arr) || count <= 0) return [];
    const shuffled = this.shuffle(arr);
    return shuffled.slice(0, Math.min(count, arr.length));
  },

  /**
   * 查找第一个匹配元素
   * @param {Array} arr - 输入数组
   * @param {Function} predicate - 匹配函数
   * @returns {*} - 匹配的元素或 undefined
   */
  find(arr, predicate) {
    if (!Array.isArray(arr) || typeof predicate !== 'function') return undefined;
    return arr.find(predicate);
  },

  /**
   * 查找所有匹配元素
   * @param {Array} arr - 输入数组
   * @param {Function} predicate - 匹配函数
   * @returns {Array} - 匹配的元素数组
   */
  filter(arr, predicate) {
    if (!Array.isArray(arr) || typeof predicate !== 'function') return [];
    return arr.filter(predicate);
  },

  /**
   * 查找元素索引
   * @param {Array} arr - 输入数组
   * @param {Function} predicate - 匹配函数
   * @returns {number} - 索引或 -1
   */
  findIndex(arr, predicate) {
    if (!Array.isArray(arr) || typeof predicate !== 'function') return -1;
    return arr.findIndex(predicate);
  },

  /**
   * 统计元素出现次数
   * @param {Array} arr - 输入数组
   * @returns {Object} - 统计结果对象
   */
  countBy(arr) {
    if (!Array.isArray(arr)) return {};
    return arr.reduce((counts, item) => {
      const key = String(item);
      counts[key] = (counts[key] || 0) + 1;
      return counts;
    }, {});
  },

  /**
   * 根据条件统计
   * @param {Array} arr - 输入数组
   * @param {Function} keyFn - 生成键的函数
   * @returns {Object} - 统计结果对象
   */
  countByFn(arr, keyFn) {
    if (!Array.isArray(arr) || typeof keyFn !== 'function') return {};
    return arr.reduce((counts, item) => {
      const key = keyFn(item);
      counts[key] = (counts[key] || 0) + 1;
      return counts;
    }, {});
  },

  /**
   * 获取最频繁出现的元素
   * @param {Array} arr - 输入数组
   * @returns {*} - 最频繁的元素
   */
  mostFrequent(arr) {
    if (!Array.isArray(arr) || arr.length === 0) return undefined;
    const counts = this.countBy(arr);
    let maxCount = 0;
    let result = arr[0];
    for (const [key, count] of Object.entries(counts)) {
      if (count > maxCount) {
        maxCount = count;
        result = arr.find(item => String(item) === key);
      }
    }
    return result;
  },

  /**
   * 数组分区（根据条件分成两组）
   * @param {Array} arr - 输入数组
   * @param {Function} predicate - 条件函数
   * @returns {Array[]} - [满足条件的数组, 不满足条件的数组]
   */
  partition(arr, predicate) {
    if (!Array.isArray(arr) || typeof predicate !== 'function') return [[], []];
    const pass = [];
    const fail = [];
    for (const item of arr) {
      if (predicate(item)) {
        pass.push(item);
      } else {
        fail.push(item);
      }
    }
    return [pass, fail];
  },

  /**
   * 获取数组中的最小值
   * @param {Array} arr - 输入数组
   * @param {Function} [keyFn] - 获取比较值的函数
   * @returns {*} - 最小值
   */
  min(arr, keyFn) {
    if (!Array.isArray(arr) || arr.length === 0) return undefined;
    if (keyFn) {
      return arr.reduce((min, item) => keyFn(item) < keyFn(min) ? item : min, arr[0]);
    }
    return Math.min(...arr);
  },

  /**
   * 获取数组中的最大值
   * @param {Array} arr - 输入数组
   * @param {Function} [keyFn] - 获取比较值的函数
   * @returns {*} - 最大值
   */
  max(arr, keyFn) {
    if (!Array.isArray(arr) || arr.length === 0) return undefined;
    if (keyFn) {
      return arr.reduce((max, item) => keyFn(item) > keyFn(max) ? item : max, arr[0]);
    }
    return Math.max(...arr);
  },

  /**
   * 计算数组总和
   * @param {Array} arr - 输入数组
   * @param {Function} [keyFn] - 获取数值的函数
   * @returns {number} - 总和
   */
  sum(arr, keyFn) {
    if (!Array.isArray(arr) || arr.length === 0) return 0;
    if (keyFn) {
      return arr.reduce((sum, item) => sum + keyFn(item), 0);
    }
    return arr.reduce((sum, item) => sum + (typeof item === 'number' ? item : 0), 0);
  },

  /**
   * 计算数组平均值
   * @param {Array} arr - 输入数组
   * @param {Function} [keyFn] - 获取数值的函数
   * @returns {number} - 平均值
   */
  average(arr, keyFn) {
    if (!Array.isArray(arr) || arr.length === 0) return 0;
    return this.sum(arr, keyFn) / arr.length;
  },

  /**
   * 获取数组第一个元素
   * @param {Array} arr - 输入数组
   * @param {*} [defaultValue] - 默认值
   * @returns {*} - 第一个元素或默认值
   */
  first(arr, defaultValue = undefined) {
    if (!Array.isArray(arr) || arr.length === 0) return defaultValue;
    return arr[0];
  },

  /**
   * 获取数组最后一个元素
   * @param {Array} arr - 输入数组
   * @param {*} [defaultValue] - 默认值
   * @returns {*} - 最后一个元素或默认值
   */
  last(arr, defaultValue = undefined) {
    if (!Array.isArray(arr) || arr.length === 0) return defaultValue;
    return arr[arr.length - 1];
  },

  /**
   * 获取数组前 N 个元素
   * @param {Array} arr - 输入数组
   * @param {number} n - 数量
   * @returns {Array} - 前 N 个元素
   */
  take(arr, n) {
    if (!Array.isArray(arr) || n <= 0) return [];
    return arr.slice(0, n);
  },

  /**
   * 跳过前 N 个元素
   * @param {Array} arr - 输入数组
   * @param {number} n - 数量
   * @returns {Array} - 剩余元素
   */
  skip(arr, n) {
    if (!Array.isArray(arr) || n <= 0) return [...arr];
    return arr.slice(n);
  },

  /**
   * 获取去掉首尾元素的数组
   * @param {Array} arr - 输入数组
   * @returns {Array} - 新数组
   */
  tail(arr) {
    if (!Array.isArray(arr) || arr.length <= 2) return [];
    return arr.slice(1, -1);
  },

  /**
   * 数组去重并保留出现顺序（稳定去重）
   * @param {Array} arr - 输入数组
   * @returns {Array} - 去重后的数组
   */
  stableUnique(arr) {
    if (!Array.isArray(arr)) return [];
    const seen = new Set();
    return arr.filter(item => {
      if (seen.has(item)) return false;
      seen.add(item);
      return true;
    });
  },

  /**
   * 比较两个数组是否相等（元素相同，顺序可不同）
   * @param {Array} arr1 - 第一个数组
   * @param {Array} arr2 - 第二个数组
   * @returns {boolean} - 是否相等
   */
  equalsIgnoreOrder(arr1, arr2) {
    if (!Array.isArray(arr1) || !Array.isArray(arr2)) return false;
    if (arr1.length !== arr2.length) return false;
    const sorted1 = [...arr1].sort();
    const sorted2 = [...arr2].sort();
    return sorted1.every((val, idx) => val === sorted2[idx]);
  },

  /**
   * 将数组转换为对象
   * @param {Array} arr - 输入数组
   * @param {Function|string} keyFn - 键生成函数或属性名
   * @param {Function|string} [valueFn] - 值生成函数或属性名
   * @returns {Object} - 转换后的对象
   */
  toObject(arr, keyFn, valueFn = null) {
    if (!Array.isArray(arr)) return {};
    const getKey = typeof keyFn === 'function' ? keyFn : item => item?.[keyFn];
    const getValue = valueFn 
      ? (typeof valueFn === 'function' ? valueFn : item => item?.[valueFn])
      : item => item;
    
    return arr.reduce((obj, item) => {
      obj[getKey(item)] = getValue(item);
      return obj;
    }, {});
  },

  /**
   * 将数组按大小分批处理
   * @param {Array} arr - 输入数组
   * @param {number} batchSize - 每批大小
   * @param {Function} callback - 处理每批的回调函数
   */
  async batchProcess(arr, batchSize, callback) {
    if (!Array.isArray(arr) || batchSize <= 0 || typeof callback !== 'function') return;
    const chunks = this.chunk(arr, batchSize);
    for (const batch of chunks) {
      await callback(batch);
    }
  },

  /**
   * 异步过滤
   * @param {Array} arr - 输入数组
   * @param {Function} asyncPredicate - 异步判断函数
   * @returns {Promise<Array>} - 过滤后的数组
   */
  async asyncFilter(arr, asyncPredicate) {
    if (!Array.isArray(arr) || typeof asyncPredicate !== 'function') return [];
    const results = await Promise.all(arr.map(asyncPredicate));
    return arr.filter((_, index) => results[index]);
  },

  /**
   * 异步映射
   * @param {Array} arr - 输入数组
   * @param {Function} asyncMapper - 异步映射函数
   * @returns {Promise<Array>} - 映射后的数组
   */
  async asyncMap(arr, asyncMapper) {
    if (!Array.isArray(arr) || typeof asyncMapper !== 'function') return [];
    return await Promise.all(arr.map(asyncMapper));
  },

  /**
   * 填充数组
   * @param {number} length - 数组长度
   * @param {*} value - 填充值
   * @returns {Array} - 填充后的数组
   */
  fill(length, value) {
    if (length <= 0) return [];
    return new Array(length).fill(value);
  },

  /**
   * 生成范围数组
   * @param {number} start - 开始值
   * @param {number} end - 结束值（不包含）
   * @param {number} [step=1] - 步长
   * @returns {Array} - 范围数组
   */
  range(start, end, step = 1) {
    if (step === 0) return [];
    const result = [];
    if (step > 0) {
      for (let i = start; i < end; i += step) {
        result.push(i);
      }
    } else {
      for (let i = start; i > end; i += step) {
        result.push(i);
      }
    }
    return result;
  },

  /**
   * 压缩多个数组（类似 Python zip）
   * @param {...Array} arrays - 要压缩的数组
   * @returns {Array} - 压缩后的数组
   */
  zip(...arrays) {
    if (arrays.length === 0) return [];
    const minLength = Math.min(...arrays.map(arr => arr?.length || 0));
    return Array.from({ length: minLength }, (_, i) => 
      arrays.map(arr => arr[i])
    );
  },

  /**
   * 解压数组
   * @param {Array} arr - 压缩后的数组
   * @returns {Array[]} - 解压后的数组
   */
  unzip(arr) {
    if (!Array.isArray(arr) || arr.length === 0) return [];
    const maxLength = arr[0]?.length || 0;
    return Array.from({ length: maxLength }, (_, i) => 
      arr.map(item => item?.[i])
    );
  },

  /**
   * 从数组中移除指定元素
   * @param {Array} arr - 输入数组
   * @param {*} value - 要移除的元素
   * @returns {Array} - 移除后的新数组
   */
  remove(arr, value) {
    if (!Array.isArray(arr)) return [];
    return arr.filter(item => item !== value);
  },

  /**
   * 从数组中移除指定索引的元素
   * @param {Array} arr - 输入数组
   * @param {number} index - 索引
   * @returns {Array} - 移除后的新数组
   */
  removeAt(arr, index) {
    if (!Array.isArray(arr) || index < 0 || index >= arr.length) return [...arr];
    return [...arr.slice(0, index), ...arr.slice(index + 1)];
  },

  /**
   * 在指定位置插入元素
   * @param {Array} arr - 输入数组
   * @param {number} index - 插入位置
   * @param {...*} items - 要插入的元素
   * @returns {Array} - 插入后的新数组
   */
  insertAt(arr, index, ...items) {
    if (!Array.isArray(arr)) return [];
    const safeIndex = Math.max(0, Math.min(index, arr.length));
    return [...arr.slice(0, safeIndex), ...items, ...arr.slice(safeIndex)];
  },

  /**
   * 移动数组中的元素
   * @param {Array} arr - 输入数组
   * @param {number} fromIndex - 源位置
   * @param {number} toIndex - 目标位置
   * @returns {Array} - 移动后的新数组
   */
  move(arr, fromIndex, toIndex) {
    if (!Array.isArray(arr) || fromIndex < 0 || fromIndex >= arr.length) return [...arr];
    if (toIndex < 0 || toIndex >= arr.length) return [...arr];
    const result = [...arr];
    const [removed] = result.splice(fromIndex, 1);
    result.splice(toIndex, 0, removed);
    return result;
  },

  /**
   * 交换数组中的两个元素
   * @param {Array} arr - 输入数组
   * @param {number} index1 - 第一个位置
   * @param {number} index2 - 第二个位置
   * @returns {Array} - 交换后的新数组
   */
  swap(arr, index1, index2) {
    if (!Array.isArray(arr)) return [];
    if (index1 < 0 || index1 >= arr.length) return [...arr];
    if (index2 < 0 || index2 >= arr.length) return [...arr];
    const result = [...arr];
    [result[index1], result[index2]] = [result[index2], result[index1]];
    return result;
  },

  /**
   * 检查数组是否包含所有指定值
   * @param {Array} arr - 输入数组
   * @param {...*} values - 要检查的值
   * @returns {boolean} - 是否全部包含
   */
  containsAll(arr, ...values) {
    if (!Array.isArray(arr)) return false;
    const set = new Set(arr);
    return values.every(val => set.has(val));
  },

  /**
   * 检查数组是否包含任意指定值
   * @param {Array} arr - 输入数组
   * @param {...*} values - 要检查的值
   * @returns {boolean} - 是否包含任意一个
   */
  containsAny(arr, ...values) {
    if (!Array.isArray(arr)) return false;
    const set = new Set(arr);
    return values.some(val => set.has(val));
  },

  /**
   * 获取数组的笛卡尔积
   * @param {Array} arr1 - 第一个数组
   * @param {Array} arr2 - 第二个数组
   * @returns {Array} - 笛卡尔积
   */
  cartesianProduct(arr1, arr2) {
    if (!Array.isArray(arr1) || !Array.isArray(arr2)) return [];
    return arr1.flatMap(a => arr2.map(b => [a, b]));
  },

  /**
   * 获取数组的所有排列
   * @param {Array} arr - 输入数组
   * @returns {Array} - 所有排列
   */
  permutations(arr) {
    if (!Array.isArray(arr)) return [];
    if (arr.length <= 1) return [arr];
    const result = [];
    for (let i = 0; i < arr.length; i++) {
      const current = arr[i];
      const remaining = [...arr.slice(0, i), ...arr.slice(i + 1)];
      const perms = this.permutations(remaining);
      for (const perm of perms) {
        result.push([current, ...perm]);
      }
    }
    return result;
  },

  /**
   * 获取数组的所有组合
   * @param {Array} arr - 输入数组
   * @param {number} size - 组合大小
   * @returns {Array} - 所有组合
   */
  combinations(arr, size) {
    if (!Array.isArray(arr) || size <= 0) return [];
    if (size > arr.length) return [];
    if (size === 1) return arr.map(item => [item]);
    const result = [];
    for (let i = 0; i <= arr.length - size; i++) {
      const current = arr[i];
      const remaining = this.combinations(arr.slice(i + 1), size - 1);
      for (const combo of remaining) {
        result.push([current, ...combo]);
      }
    }
    return result;
  },

  /**
   * 计算数组的中位数
   * @param {Array} arr - 输入数组
   * @param {Function} [keyFn] - 获取数值的函数
   * @returns {number} - 中位数
   */
  median(arr, keyFn) {
    if (!Array.isArray(arr) || arr.length === 0) return undefined;
    const values = keyFn ? arr.map(keyFn) : arr;
    const sorted = [...values].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    if (sorted.length % 2 === 0) {
      return (sorted[mid - 1] + sorted[mid]) / 2;
    }
    return sorted[mid];
  },

  /**
   * 计算数组的众数
   * @param {Array} arr - 输入数组
   * @returns {Array} - 众数数组
   */
  mode(arr) {
    if (!Array.isArray(arr) || arr.length === 0) return [];
    const counts = this.countBy(arr);
    const maxCount = Math.max(...Object.values(counts));
    return Object.entries(counts)
      .filter(([, count]) => count === maxCount)
      .map(([key]) => {
        const val = arr.find(item => String(item) === key);
        return val;
      });
  },

  /**
   * 计算数组的标准差
   * @param {Array} arr - 输入数组
   * @param {boolean} [sample=true] - 是否为样本标准差
   * @returns {number} - 标准差
   */
  stdDev(arr, sample = true) {
    if (!Array.isArray(arr) || arr.length === 0) return 0;
    const avg = this.average(arr);
    const squaredDiffs = arr.map(x => Math.pow(x - avg, 2));
    const variance = this.sum(squaredDiffs) / (arr.length - (sample ? 1 : 0));
    return Math.sqrt(variance);
  },

  /**
   * 计算数组的方差
   * @param {Array} arr - 输入数组
   * @param {boolean} [sample=true] - 是否为样本方差
   * @returns {number} - 方差
   */
  variance(arr, sample = true) {
    if (!Array.isArray(arr) || arr.length === 0) return 0;
    const avg = this.average(arr);
    const squaredDiffs = arr.map(x => Math.pow(x - avg, 2));
    return this.sum(squaredDiffs) / (arr.length - (sample ? 1 : 0));
  },

  /**
   * 归一化数组（缩放到 0-1 范围）
   * @param {Array} arr - 输入数组
   * @returns {Array} - 归一化后的数组
   */
  normalize(arr) {
    if (!Array.isArray(arr) || arr.length === 0) return [];
    const min = Math.min(...arr);
    const max = Math.max(...arr);
    if (max === min) return arr.map(() => 0);
    return arr.map(x => (x - min) / (max - min));
  },

  /**
   * 截断数组（限制长度）
   * @param {Array} arr - 输入数组
   * @param {number} maxLength - 最大长度
   * @returns {Array} - 截断后的数组
   */
  truncate(arr, maxLength) {
    if (!Array.isArray(arr)) return [];
    if (maxLength <= 0) return [];
    return arr.slice(0, maxLength);
  },

  /**
   * 分页获取数组
   * @param {Array} arr - 输入数组
   * @param {number} page - 页码（从 1 开始）
   * @param {number} pageSize - 每页大小
   * @returns {Object} - { data: 当前页数据, total: 总数, pages: 总页数, hasMore: 是否有更多 }
   */
  paginate(arr, page, pageSize) {
    if (!Array.isArray(arr)) {
      return { data: [], total: 0, pages: 0, hasMore: false };
    }
    const total = arr.length;
    const pages = Math.ceil(total / pageSize);
    const safePage = Math.max(1, Math.min(page, pages || 1));
    const start = (safePage - 1) * pageSize;
    const end = start + pageSize;
    return {
      data: arr.slice(start, end),
      total,
      pages,
      hasMore: safePage < pages
    };
  },

  /**
   * 递归扁平化嵌套数组
   * @param {Array} arr - 输入数组
   * @returns {Array} - 完全扁平化的数组
   */
  flattenRecursive(arr) {
    if (!Array.isArray(arr)) return [];
    const result = [];
    const flatten = (item) => {
      if (Array.isArray(item)) {
        item.forEach(flatten);
      } else {
        result.push(item);
      }
    };
    arr.forEach(flatten);
    return result;
  },

  /**
   * 安全地获取嵌套数组值
   * @param {Array} arr - 输入数组
   * @param {...(number|string)} path - 路径（索引或属性名）
 * @returns {*} - 获取的值或 undefined
   */
  getPath(arr, ...path) {
    if (!Array.isArray(arr)) return undefined;
    let current = arr;
    for (const key of path) {
      if (current === null || current === undefined) return undefined;
      current = current[key];
    }
    return current;
  },

  /**
   * 检查数组是否有重复元素
   * @param {Array} arr - 输入数组
   * @returns {boolean} - 是否有重复
   */
  hasDuplicates(arr) {
    if (!Array.isArray(arr)) return false;
    return new Set(arr).size !== arr.length;
  },

  /**
   * 获取数组中重复的元素
   * @param {Array} arr - 输入数组
   * @returns {Array} - 重复的元素数组
   */
  duplicates(arr) {
    if (!Array.isArray(arr)) return [];
    const seen = new Set();
    const dupes = new Set();
    for (const item of arr) {
      if (seen.has(item)) {
        dupes.add(item);
      } else {
        seen.add(item);
      }
    }
    return [...dupes];
  },

  /**
   * 比较两个数组（深度比较）
   * @param {Array} arr1 - 第一个数组
   * @param {Array} arr2 - 第二个数组
   * @returns {boolean} - 是否相等
   */
  deepEquals(arr1, arr2) {
    if (arr1 === arr2) return true;
    if (!Array.isArray(arr1) || !Array.isArray(arr2)) return false;
    if (arr1.length !== arr2.length) return false;
    for (let i = 0; i < arr1.length; i++) {
      if (Array.isArray(arr1[i]) && Array.isArray(arr2[i])) {
        if (!this.deepEquals(arr1[i], arr2[i])) return false;
      } else if (typeof arr1[i] === 'object' && typeof arr2[i] === 'object') {
        if (JSON.stringify(arr1[i]) !== JSON.stringify(arr2[i])) return false;
      } else if (arr1[i] !== arr2[i]) {
        return false;
      }
    }
    return true;
  },

  /**
   * 创建数组的浅拷贝
   * @param {Array} arr - 输入数组
   * @returns {Array} - 拷贝后的数组
   */
  clone(arr) {
    if (!Array.isArray(arr)) return [];
    return [...arr];
  },

  /**
   * 创建数组的深拷贝
   * @param {Array} arr - 输入数组
   * @returns {Array} - 深拷贝后的数组
   */
  deepClone(arr) {
    if (!Array.isArray(arr)) return [];
    return JSON.parse(JSON.stringify(arr));
  },

  /**
   * 将数组转换为 Set
   * @param {Array} arr - 输入数组
   * @returns {Set} - Set 对象
   */
  toSet(arr) {
    if (!Array.isArray(arr)) return new Set();
    return new Set(arr);
  },

  /**
   * 将 Set 转换为数组
   * @param {Set} set - Set 对象
   * @returns {Array} - 数组
   */
  fromSet(set) {
    if (!(set instanceof Set)) return [];
    return [...set];
  },

  /**
   * 将数组转换为 Map
   * @param {Array} arr - 输入数组
   * @param {Function} keyFn - 键生成函数
   * @param {Function} [valueFn] - 值生成函数
   * @returns {Map} - Map 对象
   */
  toMap(arr, keyFn, valueFn = null) {
    if (!Array.isArray(arr)) return new Map();
    const map = new Map();
    for (const item of arr) {
      const key = keyFn(item);
      const value = valueFn ? valueFn(item) : item;
      map.set(key, value);
    }
    return map;
  },

  /**
   * 将 Map 转换为数组
   * @param {Map} map - Map 对象
   * @returns {Array} - 数组
   */
  fromMap(map) {
    if (!(map instanceof Map)) return [];
    return Array.from(map.entries());
  },

  /**
   * 计算两个数组的相似度（Jaccard 系数）
   * @param {Array} arr1 - 第一个数组
   * @param {Array} arr2 - 第二个数组
   * @returns {number} - 相似度（0-1）
   */
  similarity(arr1, arr2) {
    if (!Array.isArray(arr1) || !Array.isArray(arr2)) return 0;
    const set1 = new Set(arr1);
    const set2 = new Set(arr2);
    const intersection = new Set([...set1].filter(x => set2.has(x)));
    const union = new Set([...set1, ...set2]);
    return union.size === 0 ? 1 : intersection.size / union.size;
  },

  /**
   * 计算两个数组的编辑距离（Levenshtein 距离）
   * @param {Array} arr1 - 第一个数组
   * @param {Array} arr2 - 第二个数组
   * @returns {number} - 编辑距离
   */
  editDistance(arr1, arr2) {
    if (!Array.isArray(arr1) || !Array.isArray(arr2)) return 0;
    const m = arr1.length;
    const n = arr2.length;
    const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
    
    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;
    
    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        if (arr1[i - 1] === arr2[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1];
        } else {
          dp[i][j] = Math.min(
            dp[i - 1][j] + 1,     // 删除
            dp[i][j - 1] + 1,     // 插入
            dp[i - 1][j - 1] + 1  // 替换
          );
        }
      }
    }
    return dp[m][n];
  },

  /**
   * 计算数组的累积和
   * @param {Array} arr - 输入数组
   * @returns {Array} - 累积和数组
   */
  cumulativeSum(arr) {
    if (!Array.isArray(arr)) return [];
    const result = [];
    let sum = 0;
    for (const item of arr) {
      sum += typeof item === 'number' ? item : 0;
      result.push(sum);
    }
    return result;
  },

  /**
   * 计算数组的滑动窗口平均值
   * @param {Array} arr - 输入数组
   * @param {number} windowSize - 窗口大小
   * @returns {Array} - 滑动平均数组
   */
  movingAverage(arr, windowSize) {
    if (!Array.isArray(arr) || windowSize <= 0) return [];
    const result = [];
    for (let i = 0; i <= arr.length - windowSize; i++) {
      const window = arr.slice(i, i + windowSize);
      const avg = window.reduce((sum, x) => sum + (typeof x === 'number' ? x : 0), 0) / windowSize;
      result.push(avg);
    }
    return result;
  },

  /**
   * 查找数组中的连续序列
   * @param {Array} arr - 输入数组
   * @param {Function} [predicate] - 判断函数（可选）
   * @returns {Array} - 连续序列数组
   */
  consecutive(arr, predicate = null) {
    if (!Array.isArray(arr) || arr.length === 0) return [];
    const sequences = [];
    let current = [arr[0]];
    
    for (let i = 1; i < arr.length; i++) {
      const isConsecutive = predicate 
        ? predicate(arr[i - 1], arr[i])
        : arr[i] === arr[i - 1] + 1;
      
      if (isConsecutive) {
        current.push(arr[i]);
      } else {
        sequences.push(current);
        current = [arr[i]];
      }
    }
    sequences.push(current);
    return sequences;
  },

  /**
   * 查找数组中的最长递增子序列
   * @param {Array} arr - 输入数组
   * @returns {Array} - 最长递增子序列
   */
  longestIncreasingSubsequence(arr) {
    if (!Array.isArray(arr) || arr.length === 0) return [];
    const tails = [];
    const prevIndices = [];
    
    for (let i = 0; i < arr.length; i++) {
      let left = 0, right = tails.length;
      while (left < right) {
        const mid = Math.floor((left + right) / 2);
        if (arr[tails[mid]] < arr[i]) {
          left = mid + 1;
        } else {
          right = mid;
        }
      }
      
      prevIndices[i] = tails[left - 1];
      tails[left] = i;
    }
    
    const result = [];
    let k = tails[tails.length - 1];
    while (k !== undefined) {
      result.unshift(arr[k]);
      k = prevIndices[k];
    }
    return result;
  },

  /**
   * 旋转数组
   * @param {Array} arr - 输入数组
   * @param {number} k - 旋转步数（正数向右，负数向左）
   * @returns {Array} - 旋转后的数组
   */
  rotate(arr, k) {
    if (!Array.isArray(arr) || arr.length === 0) return [];
    const n = arr.length;
    const steps = ((k % n) + n) % n;
    return [...arr.slice(-steps), ...arr.slice(0, -steps)];
  },

  /**
   * 反转数组
   * @param {Array} arr - 输入数组
   * @returns {Array} - 反转后的数组
   */
  reverse(arr) {
    if (!Array.isArray(arr)) return [];
    return [...arr].reverse();
  },

  /**
   * 交错合并多个数组
   * @param {...Array} arrays - 要合并的数组
   * @returns {Array} - 合并后的数组
   */
  interleave(...arrays) {
    if (arrays.length === 0) return [];
    const maxLength = Math.max(...arrays.map(arr => arr?.length || 0));
    const result = [];
    for (let i = 0; i < maxLength; i++) {
      for (const arr of arrays) {
        if (arr && i < arr.length) {
          result.push(arr[i]);
        }
      }
    }
    return result;
  },

  /**
   * 将数组分割为头和尾
   * @param {Array} arr - 输入数组
   * @param {number} n - 头部长度
   * @returns {Object} - { head: 前 n 个, tail: 剩余 }
   */
  headTail(arr, n = 1) {
    if (!Array.isArray(arr)) return { head: [], tail: [] };
    return {
      head: arr.slice(0, n),
      tail: arr.slice(n)
    };
  },

  /**
   * 将数组分割为初始和最后
   * @param {Array} arr - 输入数组
   * @param {number} n - 最后 n 个
   * @returns {Object} - { init: 初始部分, last: 最后 n 个 }
   */
  initLast(arr, n = 1) {
    if (!Array.isArray(arr)) return { init: [], last: [] };
    return {
      init: arr.slice(0, -n),
      last: arr.slice(-n)
    };
  },

  /**
   * 将数组按条件分割为多个组
   * @param {Array} arr - 输入数组
   * @param {Function} keyFn - 分组键函数
   * @returns {Map} - 分组 Map
   */
  classify(arr, keyFn) {
    if (!Array.isArray(arr) || typeof keyFn !== 'function') return new Map();
    const map = new Map();
    for (const item of arr) {
      const key = keyFn(item);
      if (!map.has(key)) {
        map.set(key, []);
      }
      map.get(key).push(item);
    }
    return map;
  },

  /**
   * 对数组进行分组并统计
   * @param {Array} arr - 输入数组
   * @param {Function} keyFn - 分组键函数
   * @returns {Object} - { groups: 分组对象, counts: 统计对象 }
   */
  groupAndCount(arr, keyFn) {
    if (!Array.isArray(arr) || typeof keyFn !== 'function') {
      return { groups: {}, counts: {} };
    }
    const groups = this.groupBy(arr, keyFn);
    const counts = {};
    for (const [key, items] of Object.entries(groups)) {
      counts[key] = items.length;
    }
    return { groups, counts };
  },

  /**
   * 对数组进行分桶
   * @param {Array} arr - 输入数组
   * @param {number} bucketCount - 桶数量
   * @param {Function} [keyFn] - 获取数值的函数
   * @returns {Array[]} - 分桶后的数组
   */
  bucketize(arr, bucketCount, keyFn = null) {
    if (!Array.isArray(arr) || bucketCount <= 0) return [];
    if (arr.length === 0) return Array.from({ length: bucketCount }, () => []);
    
    const values = keyFn ? arr.map(keyFn) : arr;
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;
    const bucketSize = range / bucketCount;
    
    const buckets = Array.from({ length: bucketCount }, () => []);
    for (let i = 0; i < arr.length; i++) {
      const value = values[i];
      const bucketIndex = Math.min(
        Math.floor((value - min) / bucketSize),
        bucketCount - 1
      );
      buckets[bucketIndex].push(arr[i]);
    }
    return buckets;
  },

  /**
   * 对数组进行采样（水塘抽样算法）
   * @param {Array} arr - 输入数组
   * @param {number} k - 采样数量
   * @returns {Array} - 采样结果
   */
  reservoirSample(arr, k) {
    if (!Array.isArray(arr) || k <= 0) return [];
    if (k >= arr.length) return [...arr];
    
    const result = arr.slice(0, k);
    for (let i = k; i < arr.length; i++) {
      const j = Math.floor(Math.random() * (i + 1));
      if (j < k) {
        result[j] = arr[i];
      }
    }
    return result;
  },

  /**
   * 对数组进行加权随机选择
   * @param {Array} arr - 输入数组
   * @param {Function} weightFn - 权重函数
   * @returns {*} - 选中的元素
   */
  weightedRandom(arr, weightFn) {
    if (!Array.isArray(arr) || arr.length === 0) return undefined;
    if (typeof weightFn !== 'function') return this.sample(arr, 1)[0];
    
    const weights = arr.map(weightFn);
    const totalWeight = weights.reduce((sum, w) => sum + w, 0);
    let random = Math.random() * totalWeight;
    
    for (let i = 0; i < arr.length; i++) {
      random -= weights[i];
      if (random <= 0) return arr[i];
    }
    return arr[arr.length - 1];
  },

  /**
   * 对数组进行漏斗筛选（逐步过滤）
   * @param {Array} arr - 输入数组
   * @param {...Function} predicates - 过滤函数
   * @returns {Array} - 筛选后的数组
   */
  funnel(arr, ...predicates) {
    if (!Array.isArray(arr)) return [];
    return predicates.reduce((result, predicate) => {
      if (typeof predicate !== 'function') return result;
      return result.filter(predicate);
    }, arr);
  },

  /**
   * 对数组进行流水线处理
   * @param {Array} arr - 输入数组
   * @param {...Function} transformers - 转换函数
   * @returns {*} - 最终结果
   */
  pipeline(arr, ...transformers) {
    if (!Array.isArray(arr)) return undefined;
    return transformers.reduce((result, transformer) => {
      if (typeof transformer !== 'function') return result;
      return transformer(result);
    }, arr);
  },

  /**
   * 对数组进行折叠（reduce 的别名）
   * @param {Array} arr - 输入数组
   * @param {Function} reducer - 折叠函数
   * @param {*} initialValue - 初始值
   * @returns {*} - 折叠结果
   */
  fold(arr, reducer, initialValue) {
    if (!Array.isArray(arr) || typeof reducer !== 'function') {
      return initialValue;
    }
    return arr.reduce(reducer, initialValue);
  },

  /**
   * 对数组进行扫描（返回所有中间结果）
   * @param {Array} arr - 输入数组
   * @param {Function} reducer - 扫描函数
   * @param {*} initialValue - 初始值
   * @returns {Array} - 扫描结果
   */
  scan(arr, reducer, initialValue) {
    if (!Array.isArray(arr) || typeof reducer !== 'function') return [];
    const result = [initialValue];
    let acc = initialValue;
    for (const item of arr) {
      acc = reducer(acc, item);
      result.push(acc);
    }
    return result;
  },

  /**
   * 对数组进行压缩（移除 falsy 值）
   * @param {Array} arr - 输入数组
   * @returns {Array} - 压缩后的数组
   */
  compact(arr) {
    if (!Array.isArray(arr)) return [];
    return arr.filter(Boolean);
  },

  /**
   * 对数组进行去空（移除 null 和 undefined）
   * @param {Array} arr - 输入数组
   * @returns {Array} - 去空后的数组
   */
  compactStrict(arr) {
    if (!Array.isArray(arr)) return [];
    return arr.filter(x => x !== null && x !== undefined);
  },

  /**
   * 对数组进行拍平（递归处理嵌套数组）
   * @param {Array} arr - 输入数组
   * @param {number} [depth=1] - 深度
   * @returns {Array} - 拍平后的数组
   */
  flat(arr, depth = 1) {
    if (!Array.isArray(arr)) return [];
    return arr.flat(depth);
  },

  /**
   * 对数组进行拍平并映射
   * @param {Array} arr - 输入数组
   * @param {Function} mapper - 映射函数
   * @returns {Array} - 结果数组
   */
  flatMap(arr, mapper) {
    if (!Array.isArray(arr) || typeof mapper !== 'function') return [];
    return arr.flatMap(mapper);
  },

  /**
   * 对数组进行分组折叠
   * @param {Array} arr - 输入数组
   * @param {Function} keyFn - 键函数
   * @param {Function} reducer - 折叠函数
   * @param {*} initialValue - 初始值
   * @returns {Object} - 结果对象
   */
  groupFold(arr, keyFn, reducer, initialValue) {
    if (!Array.isArray(arr) || typeof keyFn !== 'function' || typeof reducer !== 'function') {
      return {};
    }
    const groups = this.groupBy(arr, keyFn);
    const result = {};
    for (const [key, items] of Object.entries(groups)) {
      result[key] = items.reduce(reducer, initialValue);
    }
    return result;
  },

  /**
   * 对数组进行窗口滑动
   * @param {Array} arr - 输入数组
   * @param {number} size - 窗口大小
   * @param {number} [step=1] - 步长
   * @returns {Array[]} - 窗口数组
   */
  window(arr, size, step = 1) {
    if (!Array.isArray(arr) || size <= 0 || step <= 0) return [];
    const result = [];
    for (let i = 0; i <= arr.length - size; i += step) {
      result.push(arr.slice(i, i + size));
    }
    return result;
  },

  /**
   * 对数组进行成对处理
   * @param {Array} arr - 输入数组
   * @param {Function} fn - 处理函数
   * @returns {Array} - 结果数组
   */
  pairwise(arr, fn) {
    if (!Array.isArray(arr) || arr.length < 2 || typeof fn !== 'function') return [];
    const result = [];
    for (let i = 0; i < arr.length - 1; i++) {
      result.push(fn(arr[i], arr[i + 1]));
    }
    return result;
  },

  /**
   * 对数组进行相邻比较
   * @param {Array} arr - 输入数组
   * @param {Function} [comparator] - 比较函数
   * @returns {Array} - 比较结果
   */
  adjacent(arr, comparator = (a, b) => a === b) {
    if (!Array.isArray(arr) || arr.length < 2) return [];
    const result = [];
    for (let i = 0; i < arr.length - 1; i++) {
      result.push(comparator(arr[i], arr[i + 1]));
    }
    return result;
  },

  /**
   * 对数组进行去重并排序
   * @param {Array} arr - 输入数组
   * @param {Function} [comparator] - 比较函数
   * @returns {Array} - 结果数组
   */
  uniqueSort(arr, comparator) {
    if (!Array.isArray(arr)) return [];
    return [...new Set(arr)].sort(comparator);
  },

  /**
   * 对数组进行稳定排序
   * @param {Array} arr - 输入数组
   * @param {Function} comparator - 比较函数
   * @returns {Array} - 排序后的数组
   */
  stableSort(arr, comparator) {
    if (!Array.isArray(arr)) return [];
    return [...arr].map((item, index) => ({ item, index }))
      .sort((a, b) => {
        const result = comparator ? comparator(a.item, b.item) : (a.item < b.item ? -1 : 1);
        return result !== 0 ? result : a.index - b.index;
      })
      .map(({ item }) => item);
  },

  /**
   * 对数组进行自然排序
   * @param {Array} arr - 输入数组
   * @returns {Array} - 自然排序后的数组
   */
  naturalSort(arr) {
    if (!Array.isArray(arr)) return [];
    const collator = new Intl.Collator(undefined, { numeric: true, sensitivity: 'base' });
    return [...arr].sort((a, b) => collator.compare(String(a), String(b)));
  },

  /**
   * 对数组进行多字段排序
   * @param {Array} arr - 输入数组
   * @param {...Object} fields - 排序字段 { key: string, order: 'asc'|'desc' }
   * @returns {Array} - 排序后的数组
   */
  multiSort(arr, ...fields) {
    if (!Array.isArray(arr) || fields.length === 0) return [...arr];
    return [...arr].sort((a, b) => {
      for (const { key, order = 'asc' } of fields) {
        const valA = a[key];
        const valB = b[key];
        if (valA < valB) return order === 'asc' ? -1 : 1;
        if (valA > valB) return order === 'asc' ? 1 : -1;
      }
      return 0;
    });
  },

  /**
   * 对数组进行拓扑排序
   * @param {Array} items - 输入数组
   * @param {Function} getDeps - 获取依赖的函数
   * @returns {Array|null} - 排序后的数组，如果有环则返回 null
   */
  topologicalSort(items, getDeps) {
    if (!Array.isArray(items) || typeof getDeps !== 'function') return null;
    
    const inDegree = new Map();
    const graph = new Map();
    
    for (const item of items) {
      inDegree.set(item, 0);
      graph.set(item, []);
    }
    
    for (const item of items) {
      const deps = getDeps(item);
      for (const dep of deps) {
        if (graph.has(dep)) {
          graph.get(dep).push(item);
          inDegree.set(item, inDegree.get(item) + 1);
        }
      }
    }
    
    const queue = [];
    for (const [item, degree] of inDegree) {
      if (degree === 0) queue.push(item);
    }
    
    const result = [];
    while (queue.length > 0) {
      const item = queue.shift();
      result.push(item);
      for (const neighbor of graph.get(item)) {
        inDegree.set(neighbor, inDegree.get(neighbor) - 1);
        if (inDegree.get(neighbor) === 0) {
          queue.push(neighbor);
        }
      }
    }
    
    return result.length === items.length ? result : null;
  },

  /**
   * 对数组进行二分查找
   * @param {Array} arr - 已排序数组
   * @param {*} target - 目标值
   * @param {Function} [comparator] - 比较函数
   * @returns {number} - 索引，未找到返回 -1
   */
  binarySearch(arr, target, comparator) {
    if (!Array.isArray(arr)) return -1;
    let left = 0;
    let right = arr.length - 1;
    const compare = comparator || ((a, b) => (a < b ? -1 : a > b ? 1 : 0));
    
    while (left <= right) {
      const mid = Math.floor((left + right) / 2);
      const cmp = compare(arr[mid], target);
      if (cmp === 0) return mid;
      if (cmp < 0) left = mid + 1;
      else right = mid - 1;
    }
    return -1;
  },

  /**
   * 对数组进行二分查找（返回插入位置）
   * @param {Array} arr - 已排序数组
   * @param {*} target - 目标值
   * @param {Function} [comparator] - 比较函数
   * @returns {number} - 应该插入的位置
   */
  binarySearchLowerBound(arr, target, comparator) {
    if (!Array.isArray(arr)) return 0;
    let left = 0;
    let right = arr.length;
    const compare = comparator || ((a, b) => (a < b ? -1 : a > b ? 1 : 0));
    
    while (left < right) {
      const mid = Math.floor((left + right) / 2);
      if (compare(arr[mid], target) < 0) {
        left = mid + 1;
      } else {
        right = mid;
      }
    }
    return left;
  },

  /**
   * 对数组进行二分查找（返回上界）
   * @param {Array} arr - 已排序数组
   * @param {*} target - 目标值
   * @param {Function} [comparator] - 比较函数
   * @returns {number} - 上界位置
   */
  binarySearchUpperBound(arr, target, comparator) {
    if (!Array.isArray(arr)) return 0;
    let left = 0;
    let right = arr.length;
    const compare = comparator || ((a, b) => (a < b ? -1 : a > b ? 1 : 0));
    
    while (left < right) {
      const mid = Math.floor((left + right) / 2);
      if (compare(arr[mid], target) <= 0) {
        left = mid + 1;
      } else {
        right = mid;
      }
    }
    return left;
  }
};

// 导出模块
module.exports = ArrayUtils;