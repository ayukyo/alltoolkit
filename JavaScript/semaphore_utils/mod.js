/**
 * Semaphore Utils - 并发控制信号量工具
 * 
 * 提供信号量、互斥锁、读写锁等并发控制机制
 * 零外部依赖，纯 JavaScript 实现
 * 
 * @module semaphore_utils
 */

/**
 * 信号量类 - 控制并发访问数量
 */
class Semaphore {
  /**
   * 创建一个信号量
   * @param {number} permits - 允许的并发数
   * @throws {Error} 如果 permits 不是正整数
   */
  constructor(permits) {
    if (!Number.isInteger(permits) || permits <= 0) {
      throw new Error('Permits must be a positive integer');
    }
    this._permits = permits;
    this._available = permits;
    this._queue = [];
  }

  /**
   * 获取当前可用的许可数
   * @returns {number}
   */
  get available() {
    return this._available;
  }

  /**
   * 获取总许可数
   * @returns {number}
   */
  get total() {
    return this._permits;
  }

  /**
   * 获取等待中的任务数
   * @returns {number}
   */
  get waiting() {
    return this._queue.length;
  }

  /**
   * 获取一个许可（异步）
   * @param {number} [timeout] - 超时时间（毫秒），可选
   * @returns {Promise<void>}
   */
  async acquire(timeout) {
    if (this._available > 0) {
      this._available--;
      return;
    }

    return new Promise((resolve, reject) => {
      const item = { resolve, reject };
      
      if (timeout !== undefined && timeout > 0) {
        item.timeoutId = setTimeout(() => {
          const index = this._queue.indexOf(item);
          if (index !== -1) {
            this._queue.splice(index, 1);
            reject(new Error(`Semaphore acquire timeout after ${timeout}ms`));
          }
        }, timeout);
      }
      
      this._queue.push(item);
    });
  }

  /**
   * 释放一个许可
   */
  release() {
    if (this._queue.length > 0) {
      const item = this._queue.shift();
      if (item.timeoutId) {
        clearTimeout(item.timeoutId);
      }
      item.resolve();
    } else {
      if (this._available >= this._permits) {
        throw new Error('Semaphore released more than acquired');
      }
      this._available++;
    }
  }

  /**
   * 尝试获取许可（非阻塞）
   * @returns {boolean} 是否成功获取
   */
  tryAcquire() {
    if (this._available > 0) {
      this._available--;
      return true;
    }
    return false;
  }

  /**
   * 使用信号量执行函数
   * @param {Function} fn - 要执行的函数
   * @param {number} [timeout] - 获取许可的超时时间
   * @returns {Promise<any>} 函数执行结果
   */
  async run(fn, timeout) {
    await this.acquire(timeout);
    try {
      return await fn();
    } finally {
      this.release();
    }
  }

  /**
   * 获取状态信息
   * @returns {Object}
   */
  getStatus() {
    return {
      total: this._permits,
      available: this._available,
      waiting: this._queue.length
    };
  }
}

/**
 * 互斥锁（Mutex）- 二进制信号量
 * 用于保护临界区，确保同一时间只有一个任务访问
 */
class Mutex {
  constructor() {
    this._locked = false;
    this._queue = [];
    this._owner = null;
  }

  /**
   * 是否已锁定
   * @returns {boolean}
   */
  get isLocked() {
    return this._locked;
  }

  /**
   * 获取锁
   * @param {number} [timeout] - 超时时间（毫秒）
   * @returns {Promise<void>}
   */
  async acquire(timeout) {
    if (!this._locked) {
      this._locked = true;
      this._owner = Symbol('mutex-owner');
      return this._owner;
    }

    return new Promise((resolve, reject) => {
      const item = { resolve, reject };
      
      if (timeout !== undefined && timeout > 0) {
        item.timeoutId = setTimeout(() => {
          const index = this._queue.indexOf(item);
          if (index !== -1) {
            this._queue.splice(index, 1);
            reject(new Error(`Mutex acquire timeout after ${timeout}ms`));
          }
        }, timeout);
      }
      
      this._queue.push(item);
    });
  }

  /**
   * 释放锁
   */
  release() {
    if (!this._locked) {
      throw new Error('Mutex is not locked');
    }

    if (this._queue.length > 0) {
      const item = this._queue.shift();
      if (item.timeoutId) {
        clearTimeout(item.timeoutId);
      }
      this._owner = Symbol('mutex-owner');
      item.resolve(this._owner);
    } else {
      this._locked = false;
      this._owner = null;
    }
  }

  /**
   * 尝试获取锁（非阻塞）
   * @returns {boolean} 是否成功获取
   */
  tryAcquire() {
    if (!this._locked) {
      this._locked = true;
      this._owner = Symbol('mutex-owner');
      return true;
    }
    return false;
  }

  /**
   * 使用锁执行函数
   * @param {Function} fn - 要执行的函数
   * @param {number} [timeout] - 获取锁的超时时间
   * @returns {Promise<any>} 函数执行结果
   */
  async run(fn, timeout) {
    await this.acquire(timeout);
    try {
      return await fn();
    } finally {
      this.release();
    }
  }
}

/**
 * 读写锁（ReadWriteLock）
 * 允许多个读操作同时进行，但写操作独占
 */
class ReadWriteLock {
  constructor() {
    this._readers = 0;
    this._writers = 0;
    this._writeQueue = [];
    this._readQueue = [];
    this._writing = false;
  }

  /**
   * 获取读锁
   * @param {number} [timeout] - 超时时间（毫秒）
   * @returns {Promise<void>}
   */
  async acquireRead(timeout) {
    // 如果没有写操作等待且没有正在写，直接获取读锁
    if (!this._writing && this._writeQueue.length === 0) {
      this._readers++;
      return;
    }

    return new Promise((resolve, reject) => {
      const item = { resolve, reject };
      
      if (timeout !== undefined && timeout > 0) {
        item.timeoutId = setTimeout(() => {
          const index = this._readQueue.indexOf(item);
          if (index !== -1) {
            this._readQueue.splice(index, 1);
            reject(new Error(`Read lock acquire timeout after ${timeout}ms`));
          }
        }, timeout);
      }
      
      this._readQueue.push(item);
    });
  }

  /**
   * 释放读锁
   */
  releaseRead() {
    if (this._readers <= 0) {
      throw new Error('No read lock to release');
    }
    this._readers--;
    
    // 当所有读者完成后，唤醒一个写者
    if (this._readers === 0 && this._writeQueue.length > 0) {
      this._writing = true;
      const item = this._writeQueue.shift();
      if (item.timeoutId) {
        clearTimeout(item.timeoutId);
      }
      item.resolve();
    }
  }

  /**
   * 获取写锁
   * @param {number} [timeout] - 超时时间（毫秒）
   * @returns {Promise<void>}
   */
  async acquireWrite(timeout) {
    // 如果没有读者且没有正在写，直接获取写锁
    if (this._readers === 0 && !this._writing) {
      this._writing = true;
      this._writers++;
      return;
    }

    return new Promise((resolve, reject) => {
      const item = { resolve, reject };
      
      if (timeout !== undefined && timeout > 0) {
        item.timeoutId = setTimeout(() => {
          const index = this._writeQueue.indexOf(item);
          if (index !== -1) {
            this._writeQueue.splice(index, 1);
            reject(new Error(`Write lock acquire timeout after ${timeout}ms`));
          }
        }, timeout);
      }
      
      this._writeQueue.push(item);
    });
  }

  /**
   * 释放写锁
   */
  releaseWrite() {
    if (!this._writing) {
      throw new Error('No write lock to release');
    }
    
    this._writers--;
    this._writing = false;
    
    // 优先唤醒所有等待的读者
    if (this._writeQueue.length === 0) {
      while (this._readQueue.length > 0) {
        const item = this._readQueue.shift();
        if (item.timeoutId) {
          clearTimeout(item.timeoutId);
        }
        this._readers++;
        item.resolve();
      }
    } else if (this._readers === 0 && this._writeQueue.length > 0) {
      // 如果有等待的写者，唤醒一个
      this._writing = true;
      const item = this._writeQueue.shift();
      if (item.timeoutId) {
        clearTimeout(item.timeoutId);
      }
      item.resolve();
    }
  }

  /**
   * 使用读锁执行函数
   * @param {Function} fn - 要执行的函数
   * @param {number} [timeout] - 获取锁的超时时间
   * @returns {Promise<any>} 函数执行结果
   */
  async read(fn, timeout) {
    await this.acquireRead(timeout);
    try {
      return await fn();
    } finally {
      this.releaseRead();
    }
  }

  /**
   * 使用写锁执行函数
   * @param {Function} fn - 要执行的函数
   * @param {number} [timeout] - 获取锁的超时时间
   * @returns {Promise<any>} 函数执行结果
   */
  async write(fn, timeout) {
    await this.acquireWrite(timeout);
    try {
      return await fn();
    } finally {
      this.releaseWrite();
    }
  }

  /**
   * 获取状态信息
   * @returns {Object}
   */
  getStatus() {
    return {
      readers: this._readers,
      writers: this._writers,
      waitingReaders: this._readQueue.length,
      waitingWriters: this._writeQueue.length,
      isWriting: this._writing
    };
  }
}

/**
 * 倒数门闩（CountDownLatch）
 * 用于等待一组事件完成
 */
class CountDownLatch {
  /**
   * @param {number} count - 需要等待的事件数
   */
  constructor(count) {
    if (!Number.isInteger(count) || count < 0) {
      throw new Error('Count must be a non-negative integer');
    }
    this._count = count;
    this._resolvers = [];
  }

  /**
   * 获取当前计数
   * @returns {number}
   */
  get count() {
    return this._count;
  }

  /**
   * 计数减一
   */
  countDown() {
    if (this._count <= 0) {
      return;
    }
    this._count--;
    if (this._count === 0) {
      this._resolvers.forEach(item => {
        if (item.timeoutId) {
          clearTimeout(item.timeoutId);
        }
        item.resolve();
      });
      this._resolvers = [];
    }
  }

  /**
   * 等待计数归零
   * @param {number} [timeout] - 超时时间（毫秒）
   * @returns {Promise<void>}
   */
  async wait(timeout) {
    if (this._count === 0) {
      return;
    }

    return new Promise((resolve, reject) => {
      const item = { resolve };
      
      if (timeout !== undefined && timeout > 0) {
        item.timeoutId = setTimeout(() => {
          const index = this._resolvers.indexOf(item);
          if (index !== -1) {
            this._resolvers.splice(index, 1);
            reject(new Error(`CountDownLatch wait timeout after ${timeout}ms`));
          }
        }, timeout);
      }
      
      this._resolvers.push(item);
    });
  }
}

/**
 * 循环屏障（CyclicBarrier）
 * 允许一组线程互相等待，直到所有线程都到达一个屏障点
 */
class CyclicBarrier {
  /**
   * @param {number} parties - 参与者数量
   */
  constructor(parties) {
    if (!Number.isInteger(parties) || parties <= 0) {
      throw new Error('Parties must be a positive integer');
    }
    this._parties = parties;
    this._count = 0;
    this._resolvers = [];
    this._generation = 0;
    this._broken = false;
  }

  /**
   * 获取参与者数量
   * @returns {number}
   */
  get parties() {
    return this._parties;
  }

  /**
   * 获取当前等待数量
   * @returns {number}
   */
  get waiting() {
    return this._count;
  }

  /**
   * 是否已损坏
   * @returns {boolean}
   */
  get isBroken() {
    return this._broken;
  }

  /**
   * 到达屏障并等待其他参与者
   * @param {number} [timeout] - 超时时间（毫秒）
   * @returns {Promise<number>} 当前参与者的索引
   */
  async await(timeout) {
    if (this._broken) {
      throw new Error('Barrier is broken');
    }

    const index = this._count;
    this._count++;
    const generation = this._generation;

    if (this._count === this._parties) {
      // 最后一个到达，触发释放
      this._count = 0;
      this._generation++;
      this._resolvers.forEach(item => {
        if (item.timeoutId) {
          clearTimeout(item.timeoutId);
        }
        item.resolve(index);
      });
      this._resolvers = [];
      return index;
    }

    return new Promise((resolve, reject) => {
      const item = { resolve, reject, generation };
      
      if (timeout !== undefined && timeout > 0) {
        item.timeoutId = setTimeout(() => {
          this._broken = true;
          this._resolvers.forEach(i => {
            if (i !== item) {
              i.reject(new Error('Barrier broken due to timeout'));
            }
          });
          this._resolvers = [];
          reject(new Error(`CyclicBarrier await timeout after ${timeout}ms`));
        }, timeout);
      }
      
      this._resolvers.push(item);
    });
  }

  /**
   * 重置屏障
   */
  reset() {
    this._count = 0;
    this._broken = false;
    this._generation++;
    this._resolvers.forEach(item => {
      if (item.timeoutId) {
        clearTimeout(item.timeoutId);
      }
      item.reject(new Error('Barrier reset'));
    });
    this._resolvers = [];
  }
}

/**
 * 有界信号量池
 * 可以动态调整容量的信号量池
 */
class SemaphorePool {
  constructor(initialPermits = 10) {
    this._semaphore = new Semaphore(initialPermits);
    this._totalPermits = initialPermits;
  }

  /**
   * 获取一个许可
   * @param {number} [timeout] - 超时时间
   * @returns {Promise<void>}
   */
  async acquire(timeout) {
    return this._semaphore.acquire(timeout);
  }

  /**
   * 释放一个许可
   */
  release() {
    this._semaphore.release();
  }

  /**
   * 扩容（增加许可）
   * @param {number} count - 增加的数量
   */
  expand(count) {
    if (!Number.isInteger(count) || count <= 0) {
      throw new Error('Count must be a positive integer');
    }
    this._totalPermits += count;
    for (let i = 0; i < count; i++) {
      this._semaphore.release();
    }
  }

  /**
   * 获取状态
   * @returns {Object}
   */
  getStatus() {
    return {
      ...this._semaphore.getStatus(),
      totalPermits: this._totalPermits
    };
  }
}

// 导出所有类
module.exports = {
  Semaphore,
  Mutex,
  ReadWriteLock,
  CountDownLatch,
  CyclicBarrier,
  SemaphorePool
};