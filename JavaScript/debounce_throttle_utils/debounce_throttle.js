/**
 * Debounce and Throttle Utilities
 * Zero-dependency implementations for Node.js and browsers
 * 
 * Supports:
 * - Debounce (leading, trailing, or both)
 * - Throttle (leading, trailing, or both)
 * - Cancelable and flushable
 * - Async support with pending state
 */

// ============================================
// Debounce
// ============================================

/**
 * Debounce - Delays execution until after a pause in calls
 * Multiple calls reset the timer. Only the last call executes.
 */
class Debounce {
  /**
   * @param {Function} fn - Function to debounce
   * @param {Object} options
   * @param {number} options.wait - Delay in milliseconds
   * @param {boolean} [options.leading=false] - Execute on leading edge
   * @param {boolean} [options.trailing=true] - Execute on trailing edge
   * @param {number} [options.maxWait] - Maximum time to wait before executing
   */
  constructor(fn, { wait, leading = false, trailing = true, maxWait }) {
    if (typeof fn !== 'function') throw new Error('First argument must be a function');
    if (wait <= 0) throw new Error('Wait must be positive');

    this.fn = fn;
    this.wait = wait;
    this.leading = leading;
    this.trailing = trailing;
    this.maxWait = maxWait && maxWait > 0 ? maxWait : null;
    
    this.timerId = null;
    this.lastCallTime = 0;
    this.lastInvokeTime = 0;
    this.lastArgs = null;
    this.lastThis = null;
    this.result = undefined;
    this.invokeCount = 0;
  }

  /**
   * Invoke the debounced function
   * @private
   */
  _invoke(time) {
    const args = this.lastArgs;
    const thisArg = this.lastThis;
    
    this.lastArgs = null;
    this.lastThis = null;
    this.lastInvokeTime = time;
    this.invokeCount++;
    
    this.result = this.fn.apply(thisArg, args);
    return this.result;
  }

  /**
   * Should invoke on leading edge?
   * @private
   */
  _shouldInvoke(time) {
    const timeSinceLastCall = time - this.lastCallTime;
    const timeSinceLastInvoke = time - this.lastInvokeTime;
    
    return (
      this.lastCallTime === 0 ||
      timeSinceLastCall >= this.wait ||
      (this.maxWait && timeSinceLastInvoke >= this.maxWait)
    );
  }

  /**
   * Start the timer
   * @private
   */
  _startTimer(pendingFunc, wait) {
    this._clearTimer();
    this.timerId = setTimeout(pendingFunc, wait);
  }

  /**
   * Clear the timer
   * @private
   */
  _clearTimer() {
    if (this.timerId !== null) {
      clearTimeout(this.timerId);
      this.timerId = null;
    }
  }

  /**
   * Leading edge handler
   * @private
   */
  _leadingEdge(time) {
    this._startTimer(() => this._trailingEdge(time), this.wait);
    if (this.leading) {
      return this._invoke(time);
    }
    return this.result;
  }

  /**
   * Trailing edge handler
   * @private
   */
  _trailingEdge(time) {
    this.timerId = null;
    if (this.trailing && this.lastArgs) {
      return this._invoke(time);
    }
    this.lastArgs = null;
    this.lastThis = null;
    return this.result;
  }

  /**
   * Remaining wait time
   * @private
   */
  _remainingWait(time) {
    const timeSinceLastCall = time - this.lastCallTime;
    const timeSinceLastInvoke = time - this.lastInvokeTime;
    const timeWaiting = this.wait - timeSinceLastCall;
    
    if (this.maxWait) {
      return Math.min(timeWaiting, this.maxWait - timeSinceLastInvoke);
    }
    return timeWaiting;
  }

  /**
   * Call the debounced function
   * @param {...*} args - Arguments to pass to the original function
   * @returns {*} Result of the function
   */
  call(...args) {
    const time = Date.now();
    const isInvoking = this._shouldInvoke(time);
    
    this.lastArgs = args;
    this.lastThis = this;
    this.lastCallTime = time;
    
    if (isInvoking) {
      if (this.timerId === null) {
        return this._leadingEdge(time);
      }
      if (this.maxWait) {
        this._startTimer(() => this._trailingEdge(time), this._remainingWait(time));
        return this._invoke(time);
      }
    }
    
    if (this.timerId === null) {
      this._startTimer(() => this._trailingEdge(time), this.wait);
    }
    
    return this.result;
  }

  /**
   * Cancel any pending execution
   */
  cancel() {
    this._clearTimer();
    this.lastArgs = null;
    this.lastThis = null;
    this.lastCallTime = 0;
    this.lastInvokeTime = 0;
  }

  /**
   * Immediately execute if pending
   * @returns {*} Result of the function
   */
  flush() {
    if (this.timerId !== null) {
      this._clearTimer();
      if (this.trailing && this.lastArgs) {
        return this._invoke(Date.now());
      }
    }
    return this.result;
  }

  /**
   * Check if there's a pending execution
   * @returns {boolean}
   */
  pending() {
    return this.timerId !== null;
  }

  /**
   * Get the number of times the function has been invoked
   * @returns {number}
   */
  getInvokeCount() {
    return this.invokeCount;
  }
}

// ============================================
// Throttle
// ============================================

/**
 * Throttle - Limits execution to once per time period
 * Calls during the period are ignored (or queued for trailing)
 */
class Throttle {
  /**
   * @param {Function} fn - Function to throttle
   * @param {Object} options
   * @param {number} options.limit - Minimum time between calls in milliseconds
   * @param {boolean} [options.leading=true] - Execute on leading edge
   * @param {boolean} [options.trailing=true] - Execute on trailing edge
   */
  constructor(fn, { limit, leading = true, trailing = true }) {
    if (typeof fn !== 'function') throw new Error('First argument must be a function');
    if (limit <= 0) throw new Error('Limit must be positive');

    this.fn = fn;
    this.limit = limit;
    this.leading = leading;
    this.trailing = trailing;
    
    this.timerId = null;
    this.lastCallTime = 0;
    this.lastInvokeTime = 0;
    this.lastArgs = null;
    this.lastThis = null;
    this.result = undefined;
    this.invokeCount = 0;
  }

  /**
   * Invoke the throttled function
   * @private
   */
  _invoke(time) {
    const args = this.lastArgs;
    const thisArg = this.lastThis;
    
    this.lastArgs = null;
    this.lastThis = null;
    this.lastInvokeTime = time;
    this.invokeCount++;
    
    this.result = this.fn.apply(thisArg, args);
    return this.result;
  }

  /**
   * Should invoke?
   * @private
   */
  _shouldInvoke(time) {
    const timeSinceLastInvoke = time - this.lastInvokeTime;
    return timeSinceLastInvoke >= this.limit;
  }

  /**
   * Start the timer
   * @private
   */
  _startTimer(pendingFunc, wait) {
    this._clearTimer();
    this.timerId = setTimeout(pendingFunc, wait);
  }

  /**
   * Clear the timer
   * @private
   */
  _clearTimer() {
    if (this.timerId !== null) {
      clearTimeout(this.timerId);
      this.timerId = null;
    }
  }

  /**
   * Trailing edge handler
   * @private
   */
  _trailingEdge() {
    this.timerId = null;
    if (this.trailing && this.lastArgs) {
      return this._invoke(Date.now());
    }
    this.lastArgs = null;
    this.lastThis = null;
    return this.result;
  }

  /**
   * Remaining time
   * @private
   */
  _remainingWait(time) {
    return this.limit - (time - this.lastInvokeTime);
  }

  /**
   * Call the throttled function
   * @param {...*} args - Arguments to pass to the original function
   * @returns {*} Result of the function
   */
  call(...args) {
    const time = Date.now();
    const isInvoking = this._shouldInvoke(time);
    
    this.lastArgs = args;
    this.lastThis = this;
    this.lastCallTime = time;
    
    if (isInvoking) {
      if (this.timerId !== null) {
        this._clearTimer();
      }
      if (this.leading) {
        return this._invoke(time);
      }
    }
    
    if (this.timerId === null && this.trailing) {
      this._startTimer(() => this._trailingEdge(), this._remainingWait(time));
    }
    
    return this.result;
  }

  /**
   * Cancel any pending execution
   */
  cancel() {
    this._clearTimer();
    this.lastArgs = null;
    this.lastThis = null;
  }

  /**
   * Immediately execute if pending
   * @returns {*} Result of the function
   */
  flush() {
    if (this.timerId !== null) {
      this._clearTimer();
      if (this.trailing && this.lastArgs) {
        return this._invoke(Date.now());
      }
    }
    return this.result;
  }

  /**
   * Check if there's a pending execution
   * @returns {boolean}
   */
  pending() {
    return this.timerId !== null;
  }

  /**
   * Get the number of times the function has been invoked
   * @returns {number}
   */
  getInvokeCount() {
    return this.invokeCount;
  }
}

// ============================================
// Async Debounce
// ============================================

/**
 * Async Debounce - For async functions with proper promise handling
 */
class AsyncDebounce {
  /**
   * @param {Function} fn - Async function to debounce
   * @param {Object} options
   * @param {number} options.wait - Delay in milliseconds
   * @param {boolean} [options.leading=false] - Execute on leading edge
   * @param {boolean} [options.trailing=true] - Execute on trailing edge
   */
  constructor(fn, { wait, leading = false, trailing = true }) {
    if (typeof fn !== 'function') throw new Error('First argument must be a function');
    if (wait <= 0) throw new Error('Wait must be positive');

    this.fn = fn;
    this.wait = wait;
    this.leading = leading;
    this.trailing = trailing;
    
    this.timerId = null;
    this.lastCallTime = 0;
    this.lastArgs = null;
    this.lastThis = null;
    this.pendingPromise = null;
    this.resolveQueue = [];
    this.rejectQueue = [];
  }

  /**
   * Execute the async function
   * @private
   */
  async _execute() {
    const args = this.lastArgs;
    const thisArg = this.lastThis;
    
    this.lastArgs = null;
    this.lastThis = null;
    this.timerId = null;
    
    try {
      const result = await this.fn.apply(thisArg, args);
      this.resolveQueue.forEach(resolve => resolve(result));
    } catch (error) {
      this.rejectQueue.forEach(reject => reject(error));
    }
    
    this.resolveQueue = [];
    this.rejectQueue = [];
    this.pendingPromise = null;
  }

  /**
   * Call the debounced async function
   * @param {...*} args - Arguments to pass
   * @returns {Promise<*>} Promise resolving to the result
   */
  async call(...args) {
    this.lastArgs = args;
    this.lastThis = this;
    this.lastCallTime = Date.now();
    
    if (!this.pendingPromise) {
      this.pendingPromise = new Promise((resolve, reject) => {
        this.resolveQueue.push(resolve);
        this.rejectQueue.push(reject);
      });
    }
    
    if (this.timerId !== null) {
      clearTimeout(this.timerId);
    }
    
    if (this.leading && this.timerId === null) {
      this._execute();
    } else {
      this.timerId = setTimeout(() => {
        if (this.trailing) {
          this._execute();
        } else {
          this.timerId = null;
        }
      }, this.wait);
    }
    
    return this.pendingPromise;
  }

  /**
   * Cancel pending execution
   */
  cancel() {
    if (this.timerId !== null) {
      clearTimeout(this.timerId);
      this.timerId = null;
    }
    this.lastArgs = null;
    this.lastThis = null;
    
    if (this.pendingPromise) {
      this.rejectQueue.forEach(reject => reject(new Error('Debounced function canceled')));
      this.resolveQueue = [];
      this.rejectQueue = [];
      this.pendingPromise = null;
    }
  }

  /**
   * Check if there's a pending execution
   * @returns {boolean}
   */
  pending() {
    return this.timerId !== null || this.pendingPromise !== null;
  }
}

// ============================================
// Debounced Function Factory
// ============================================

/**
 * Create a debounced function (simpler API)
 * @param {Function} fn - Function to debounce
 * @param {number} wait - Delay in milliseconds
 * @param {Object} [options]
 * @param {boolean} [options.leading=false]
 * @param {boolean} [options.trailing=true]
 * @param {number} [options.maxWait]
 * @returns {Function} Debounced function with .cancel() and .flush() methods
 */
function debounce(fn, wait, options = {}) {
  const instance = new Debounce(fn, { wait, ...options });
  
  const debounced = function(...args) {
    return instance.call(...args);
  };
  
  debounced.cancel = () => instance.cancel();
  debounced.flush = () => instance.flush();
  debounced.pending = () => instance.pending();
  
  return debounced;
}

// ============================================
// Throttled Function Factory
// ============================================

/**
 * Create a throttled function (simpler API)
 * @param {Function} fn - Function to throttle
 * @param {number} limit - Minimum time between calls in milliseconds
 * @param {Object} [options]
 * @param {boolean} [options.leading=true]
 * @param {boolean} [options.trailing=true]
 * @returns {Function} Throttled function with .cancel() and .flush() methods
 */
function throttle(fn, limit, options = {}) {
  const instance = new Throttle(fn, { limit, ...options });
  
  const throttled = function(...args) {
    return instance.call(...args);
  };
  
  throttled.cancel = () => instance.cancel();
  throttled.flush = () => instance.flush();
  throttled.pending = () => instance.pending();
  
  return throttled;
}

// ============================================
// Rate Limited Queue
// ============================================

/**
 * Queue that processes items with rate limiting
 * Useful for API calls, animations, etc.
 */
class RateLimitedQueue {
  /**
   * @param {Function} processor - Async function to process each item
   * @param {Object} options
   * @param {number} options.interval - Minimum time between processing
   * @param {number} [options.concurrency=1] - Max concurrent processing
   * @param {boolean} [options.autoStart=true] - Start processing automatically
   */
  constructor(processor, { interval, concurrency = 1, autoStart = true }) {
    if (typeof processor !== 'function') throw new Error('Processor must be a function');
    if (interval <= 0) throw new Error('Interval must be positive');
    
    this.processor = processor;
    this.interval = interval;
    this.concurrency = concurrency;
    this.autoStart = autoStart;
    
    this.queue = [];
    this.active = 0;
    this.lastProcessTime = 0;
    this.timerId = null;
  }

  /**
   * Add item to queue
   * @param {*} item - Item to process
   * @returns {Promise<*>} Result of processing
   */
  add(item) {
    return new Promise((resolve, reject) => {
      this.queue.push({ item, resolve, reject });
      if (this.autoStart && this.active < this.concurrency) {
        this._processNext();
      }
    });
  }

  /**
   * Add multiple items
   * @param {Array} items - Items to process
   * @returns {Promise<Array>} Results in order
   */
  async addAll(items) {
    return Promise.all(items.map(item => this.add(item)));
  }

  /**
   * Process next item in queue
   * @private
   */
  async _processNext() {
    if (this.queue.length === 0 || this.active >= this.concurrency) {
      return;
    }
    
    const now = Date.now();
    const timeSinceLastProcess = now - this.lastProcessTime;
    const waitTime = Math.max(0, this.interval - timeSinceLastProcess);
    
    if (waitTime > 0) {
      this.timerId = setTimeout(() => this._processNext(), waitTime);
      return;
    }
    
    const { item, resolve, reject } = this.queue.shift();
    this.active++;
    this.lastProcessTime = Date.now();
    
    try {
      const result = await this.processor(item);
      resolve(result);
    } catch (error) {
      reject(error);
    } finally {
      this.active--;
      if (this.queue.length > 0 && this.active < this.concurrency) {
        this._processNext();
      }
    }
  }

  /**
   * Get queue length
   * @returns {number}
   */
  size() {
    return this.queue.length;
  }

  /**
   * Check if queue is empty
   * @returns {boolean}
   */
  isEmpty() {
    return this.queue.length === 0;
  }

  /**
   * Clear the queue
   */
  clear() {
    this.queue = [];
    if (this.timerId !== null) {
      clearTimeout(this.timerId);
      this.timerId = null;
    }
  }
}

// ============================================
// Exports
// ============================================

module.exports = {
  // Classes
  Debounce,
  Throttle,
  AsyncDebounce,
  RateLimitedQueue,
  
  // Factory functions (simpler API)
  debounce,
  throttle
};

// ES Module support
if (typeof module !== 'undefined' && module.exports) {
  module.exports.default = module.exports;
}