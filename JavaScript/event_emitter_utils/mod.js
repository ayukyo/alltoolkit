/**
 * EventEmitter Utils - A lightweight event-driven programming utility
 * 
 * Zero external dependencies - pure JavaScript implementation
 * Provides a simple, efficient event system for decoupling code
 * 
 * Features:
 * - Subscribe/unsubscribe to events
 * - One-time event listeners
 * - Event namespacing
 * - Wildcard event matching
 * - Listener priority
 * - Async event emission
 * - Event history/replay
 * - Memory leak prevention (max listeners)
 */

/**
 * @class EventEmitter
 * @description A flexible event emitter with advanced features
 */
class EventEmitter {
  /**
   * Creates a new EventEmitter instance
   * @param {Object} options - Configuration options
   * @param {number} options.maxListeners - Maximum listeners per event (default: 100)
   * @param {boolean} options.captureHistory - Whether to capture event history (default: false)
   * @param {number} options.historySize - Maximum events in history (default: 100)
   */
  constructor(options = {}) {
    this._events = new Map();
    this._maxListeners = options.maxListeners || 100;
    this._captureHistory = options.captureHistory || false;
    this._historySize = options.historySize || 100;
    this._history = [];
    this._onceEvents = new Set();
  }

  /**
   * Subscribe to an event
   * @param {string} eventName - The event name (supports namespacing with '.')
   * @param {Function} listener - The callback function
   * @param {Object} options - Additional options
   * @param {number} options.priority - Listener priority (higher = called first)
   * @param {boolean} options.prepend - Add to beginning of listeners array
   * @returns {Function} Unsubscribe function
   */
  on(eventName, listener, options = {}) {
    if (typeof listener !== 'function') {
      throw new TypeError('Listener must be a function');
    }

    if (!this._events.has(eventName)) {
      this._events.set(eventName, []);
    }

    const listeners = this._events.get(eventName);
    
    // Check max listeners
    if (listeners.length >= this._maxListeners) {
      console.warn(
        `EventEmitter: Possible memory leak. ${listeners.length} listeners for "${eventName}". ` +
        `Use setMaxListeners() to increase limit.`
      );
    }

    const listenerObj = {
      fn: listener,
      priority: options.priority || 0,
      once: false
    };

    if (options.prepend) {
      listeners.unshift(listenerObj);
    } else {
      listeners.push(listenerObj);
    }

    // Sort by priority (higher priority first)
    listeners.sort((a, b) => b.priority - a.priority);

    // Return unsubscribe function
    return () => this.off(eventName, listener);
  }

  /**
   * Subscribe to an event (alias for 'on')
   * @param {string} eventName - The event name
   * @param {Function} listener - The callback function
   * @param {Object} options - Additional options
   * @returns {Function} Unsubscribe function
   */
  addListener(eventName, listener, options = {}) {
    return this.on(eventName, listener, options);
  }

  /**
   * Subscribe to an event that fires only once
   * @param {string} eventName - The event name
   * @param {Function} listener - The callback function
   * @param {Object} options - Additional options
   * @returns {Function} Unsubscribe function
   */
  once(eventName, listener, options = {}) {
    if (typeof listener !== 'function') {
      throw new TypeError('Listener must be a function');
    }

    if (!this._events.has(eventName)) {
      this._events.set(eventName, []);
    }

    const listeners = this._events.get(eventName);
    
    const listenerObj = {
      fn: listener,
      priority: options.priority || 0,
      once: true
    };

    if (options.prepend) {
      listeners.unshift(listenerObj);
    } else {
      listeners.push(listenerObj);
    }

    listeners.sort((a, b) => b.priority - a.priority);

    return () => this.off(eventName, listener);
  }

  /**
   * Unsubscribe from an event
   * @param {string} eventName - The event name
   * @param {Function} listener - The callback function to remove
   * @returns {EventEmitter} This instance for chaining
   */
  off(eventName, listener) {
    if (!this._events.has(eventName)) {
      return this;
    }

    const listeners = this._events.get(eventName);
    const index = listeners.findIndex(obj => obj.fn === listener);
    
    if (index !== -1) {
      listeners.splice(index, 1);
    }

    if (listeners.length === 0) {
      this._events.delete(eventName);
    }

    return this;
  }

  /**
   * Unsubscribe all listeners from an event (or all events)
   * @param {string} eventName - Optional event name. If omitted, removes all listeners.
   * @returns {EventEmitter} This instance for chaining
   */
  removeAllListeners(eventName) {
    if (eventName) {
      this._events.delete(eventName);
    } else {
      this._events.clear();
    }
    return this;
  }

  /**
   * Emit an event to all listeners
   * @param {string} eventName - The event name
   * @param {...any} args - Arguments to pass to listeners
   * @returns {boolean} True if event had listeners, false otherwise
   */
  emit(eventName, ...args) {
    // Capture history if enabled
    if (this._captureHistory) {
      this._history.push({
        event: eventName,
        args: args,
        timestamp: Date.now()
      });
      
      // Trim history if needed
      if (this._history.length > this._historySize) {
        this._history.shift();
      }
    }

    const listeners = this._getMatchingListeners(eventName);
    
    if (listeners.length === 0) {
      return false;
    }

    // Create a copy to prevent modification during iteration
    const listenersCopy = [...listeners];
    const toRemove = [];

    for (const listenerObj of listenersCopy) {
      try {
        listenerObj.fn(...args);
        if (listenerObj.once) {
          toRemove.push(listenerObj);
        }
      } catch (error) {
        console.error(`Error in event listener for "${eventName}":`, error);
      }
    }

    // Remove once listeners
    for (const listenerObj of toRemove) {
      this.off(eventName, listenerObj.fn);
    }

    return true;
  }

  /**
   * Emit an event asynchronously
   * @param {string} eventName - The event name
   * @param {...any} args - Arguments to pass to listeners
   * @returns {Promise<boolean>} Promise resolving to true if event had listeners
   */
  async emitAsync(eventName, ...args) {
    // Capture history if enabled
    if (this._captureHistory) {
      this._history.push({
        event: eventName,
        args: args,
        timestamp: Date.now()
      });
      
      if (this._history.length > this._historySize) {
        this._history.shift();
      }
    }

    const listeners = this._getMatchingListeners(eventName);
    
    if (listeners.length === 0) {
      return false;
    }

    const listenersCopy = [...listeners];
    const toRemove = [];

    for (const listenerObj of listenersCopy) {
      try {
        const result = listenerObj.fn(...args);
        if (result instanceof Promise) {
          await result;
        }
        if (listenerObj.once) {
          toRemove.push(listenerObj);
        }
      } catch (error) {
        console.error(`Error in async event listener for "${eventName}":`, error);
      }
    }

    for (const listenerObj of toRemove) {
      this.off(eventName, listenerObj.fn);
    }

    return true;
  }

  /**
   * Get all matching listeners for an event (supports wildcards)
   * @private
   * @param {string} eventName - The event name
   * @returns {Array} Array of listener objects
   */
  _getMatchingListeners(eventName) {
    const allListeners = [];
    
    // Direct match
    if (this._events.has(eventName)) {
      allListeners.push(...this._events.get(eventName));
    }

    // Wildcard matching for patterns like 'user:*' or 'user.*'
    for (const [pattern, listeners] of this._events) {
      if (pattern === eventName) continue;
      
      if (this._matchPattern(pattern, eventName)) {
        allListeners.push(...listeners);
      }
    }

    return allListeners;
  }

  /**
   * Check if an event name matches a pattern (wildcard support)
   * @private
   * @param {string} pattern - The pattern (may contain '*' or '**')
   * @param {string} eventName - The event name to check
   * @returns {boolean} True if matches
   */
  _matchPattern(pattern, eventName) {
    // Convert pattern to regex
    // '*' matches a single segment
    // '**' matches multiple segments
    const regexPattern = pattern
      .replace(/[.+?^${}()|[\]\\]/g, '\\$&')
      .replace(/\*\*/g, '<<<DOUBLE>>>')
      .replace(/\*/g, '[^.:]*')
      .replace(/<<<DOUBLE>>>/g, '.*');
    
    const regex = new RegExp(`^${regexPattern}$`);
    return regex.test(eventName);
  }

  /**
   * Get the number of listeners for an event
   * @param {string} eventName - The event name
   * @returns {number} Number of listeners
   */
  listenerCount(eventName) {
    if (!this._events.has(eventName)) {
      return 0;
    }
    return this._events.get(eventName).length;
  }

  /**
   * Get all event names that have listeners
   * @returns {Array<string>} Array of event names
   */
  eventNames() {
    return Array.from(this._events.keys());
  }

  /**
   * Get all listeners for an event
   * @param {string} eventName - The event name
   * @returns {Array<Function>} Array of listener functions
   */
  listeners(eventName) {
    if (!this._events.has(eventName)) {
      return [];
    }
    return this._events.get(eventName).map(obj => obj.fn);
  }

  /**
   * Set the maximum number of listeners per event
   * @param {number} max - Maximum number of listeners
   * @returns {EventEmitter} This instance for chaining
   */
  setMaxListeners(max) {
    this._maxListeners = max;
    return this;
  }

  /**
   * Get the maximum number of listeners per event
   * @returns {number} Maximum listeners
   */
  getMaxListeners() {
    return this._maxListeners;
  }

  /**
   * Enable or disable history capture
   * @param {boolean} enabled - Whether to capture history
   * @returns {EventEmitter} This instance for chaining
   */
  setCaptureHistory(enabled) {
    this._captureHistory = enabled;
    return this;
  }

  /**
   * Get event history
   * @param {string} eventName - Optional event name to filter
   * @returns {Array} Array of historical events
   */
  getHistory(eventName) {
    if (eventName) {
      return this._history.filter(e => e.event === eventName || this._matchPattern(eventName, e.event));
    }
    return [...this._history];
  }

  /**
   * Clear event history
   * @returns {EventEmitter} This instance for chaining
   */
  clearHistory() {
    this._history = [];
    return this;
  }

  /**
   * Replay a historical event
   * @param {number} index - Index in history to replay
   * @returns {boolean} True if event was replayed successfully
   */
  replay(index) {
    if (index < 0 || index >= this._history.length) {
      return false;
    }
    const event = this._history[index];
    return this.emit(event.event, ...event.args);
  }

  /**
   * Create a namespaced event emitter
   * @param {string} namespace - The namespace prefix
   * @returns {NamespacedEmitter} A namespaced emitter
   */
  namespace(namespace) {
    return new NamespacedEmitter(this, namespace);
  }
}

/**
 * @class NamespacedEmitter
 * @description A namespaced event emitter that prefixes all events
 */
class NamespacedEmitter {
  /**
   * Creates a namespaced emitter
   * @param {EventEmitter} emitter - The parent emitter
   * @param {string} namespace - The namespace prefix
   */
  constructor(emitter, namespace) {
    this._emitter = emitter;
    this._namespace = namespace;
  }

  /**
   * Get the full event name with namespace
   * @private
   * @param {string} eventName - The event name
   * @returns {string} Namespaced event name
   */
  _getEventName(eventName) {
    return `${this._namespace}.${eventName}`;
  }

  on(eventName, listener, options = {}) {
    return this._emitter.on(this._getEventName(eventName), listener, options);
  }

  once(eventName, listener, options = {}) {
    return this._emitter.once(this._getEventName(eventName), listener, options);
  }

  off(eventName, listener) {
    return this._emitter.off(this._getEventName(eventName), listener);
  }

  emit(eventName, ...args) {
    return this._emitter.emit(this._getEventName(eventName), ...args);
  }

  emitAsync(eventName, ...args) {
    return this._emitter.emitAsync(this._getEventName(eventName), ...args);
  }

  listenerCount(eventName) {
    return this._emitter.listenerCount(this._getEventName(eventName));
  }
}

/**
 * Create a new EventEmitter instance
 * @param {Object} options - Configuration options
 * @returns {EventEmitter} New EventEmitter instance
 */
function createEventEmitter(options = {}) {
  return new EventEmitter(options);
}

/**
 * Mixin EventEmitter methods into an object
 * @param {Object} target - The target object
 * @returns {Object} The target object with EventEmitter methods
 */
function mixinEventEmitter(target) {
  const emitter = new EventEmitter();
  
  target.on = emitter.on.bind(emitter);
  target.once = emitter.once.bind(emitter);
  target.off = emitter.off.bind(emitter);
  target.emit = emitter.emit.bind(emitter);
  target.emitAsync = emitter.emitAsync.bind(emitter);
  target.removeAllListeners = emitter.removeAllListeners.bind(emitter);
  target.listenerCount = emitter.listenerCount.bind(emitter);
  target.listeners = emitter.listeners.bind(emitter);
  target.eventNames = emitter.eventNames.bind(emitter);
  
  // Store reference for internal use
  target._eventEmitter = emitter;
  
  return target;
}

// Export classes and functions
module.exports = {
  EventEmitter,
  NamespacedEmitter,
  createEventEmitter,
  mixinEventEmitter
};