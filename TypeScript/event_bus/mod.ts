/**
 * AllToolkit - TypeScript Event Bus
 *
 * A zero-dependency, production-ready event bus implementation.
 * Supports synchronous and asynchronous event handling, wildcards,
 * once listeners, and typed events.
 *
 * Author: AllToolkit
 * License: MIT
 */

/**
 * Type definition for event callback
 * @param data - Event data
 * @param eventName - Name of the event
 * @param source - Optional source identifier
 */
export type EventCallback<T = any> = (data: T, eventName: string, source?: string) => void | Promise<void>;

/**
 * Type definition for event filter
 */
export type EventFilter<T = any> = (data: T, eventName: string) => boolean;

/**
 * Listener configuration
 */
export interface ListenerConfig {
  callback: EventCallback;
  filter?: EventFilter;
  once: boolean;
  priority: number;
}

/**
 * Event data structure
 */
export interface EventData<T = any> {
  name: string;
  data: T;
  timestamp: number;
  source?: string;
}

/**
 * Event Bus Statistics
 */
export interface EventBusStats {
  totalEvents: number;
  totalListeners: number;
  eventsByType: Record<string, number>;
  activeListeners: Record<string, number>;
}

/**
 * Event Bus Class
 *
 * A centralized event management system that allows components to communicate
 * through events. Supports:
 * - Synchronous and asynchronous event handling
 * - Wildcard event matching (*, **)
 * - Once listeners (auto-remove after first trigger)
 * - Priority-based listener execution
 * - Event filtering
 * - Typed events
 * - Event history
 * - Statistics tracking
 *
 * @example
 * ```typescript
 * const bus = new EventBus();
 *
 * // Subscribe to an event
 * bus.on('user:login', (data) => {
 *   console.log(`User ${data.username} logged in`);
 * });
 *
 * // Publish an event
 * bus.emit('user:login', { username: 'john', id: 123 });
 *
 * // Subscribe once
 * bus.once('user:logout', (data) => {
 *   console.log('User logged out');
 * });
 *
 * // Wildcard subscription
 * bus.on('user:*', (data, eventName) => {
 *   console.log(`User event: ${eventName}`);
 * });
 *
 * // Priority subscription
 * bus.on('order:created', handler, { priority: 10 });
 * ```
 */
export class EventBus {
  /** Map of event name to listeners */
  private listeners: Map<string, ListenerConfig[]>;

  /** Event history (last N events) */
  private history: EventData[];

  /** Maximum history size */
  private maxHistorySize: number;

  /** Statistics tracking */
  private stats: EventBusStats;

  /** Whether the bus is suspended */
  private suspended: boolean;

  /** Pending events when suspended */
  private pendingEvents: EventData[];

  /**
   * Create a new EventBus instance
   *
   * @param maxHistorySize - Maximum number of events to keep in history (default: 100)
   */
  constructor(maxHistorySize: number = 100) {
    this.listeners = new Map();
    this.history = [];
    this.maxHistorySize = maxHistorySize;
    this.suspended = false;
    this.pendingEvents = [];
    this.stats = {
      totalEvents: 0,
      totalListeners: 0,
      eventsByType: {},
      activeListeners: {},
    };
  }

  /**
   * Subscribe to an event
   *
   * @param eventName - Name of the event to subscribe to (supports wildcards: *, **)
   * @param callback - Callback function to execute when event is emitted
   * @param options - Optional configuration (priority, filter, once)
   * @returns Unsubscribe function
   *
   * @example
   * ```typescript
   * // Basic subscription
   * bus.on('user:created', (data) => {
   *   console.log(data);
   * });
   *
   * // With priority (higher priority executes first)
   * bus.on('user:created', handler, { priority: 10 });
   *
   * // With filter (only execute if filter returns true)
   * bus.on('order:created', handler, {
   *   filter: (data) => data.amount > 100
   * });
   *
   * // Get unsubscribe function
   * const unsubscribe = bus.on('event', handler);
   * unsubscribe(); // Remove this listener
   * ```
   */
  on<T = any>(
    eventName: string,
    callback: EventCallback<T>,
    options: { priority?: number; filter?: EventFilter<T>; once?: boolean } = {}
  ): () => void {
    const config: ListenerConfig = {
      callback,
      filter: options.filter,
      once: options.once || false,
      priority: options.priority || 0,
    };

    if (!this.listeners.has(eventName)) {
      this.listeners.set(eventName, []);
    }

    const listeners = this.listeners.get(eventName)!;
    listeners.push(config);

    // Sort by priority (descending)
    listeners.sort((a, b) => b.priority - a.priority);

    // Update stats
    this.stats.totalListeners++;
    this.stats.activeListeners[eventName] = listeners.length;

    // Return unsubscribe function
    return () => this.off(eventName, callback);
  }

  /**
   * Subscribe to an event once (auto-remove after first trigger)
   *
   * @param eventName - Name of the event
   * @param callback - Callback function
   * @param options - Optional configuration (priority, filter)
   * @returns Unsubscribe function
   *
   * @example
   * ```typescript
   * bus.once('user:login', (data) => {
   *   console.log('First login event received');
   * });
   * ```
   */
  once<T = any>(
    eventName: string,
    callback: EventCallback<T>,
    options: { priority?: number; filter?: EventFilter<T> } = {}
  ): () => void {
    return this.on(eventName, callback, { ...options, once: true });
  }

  /**
   * Unsubscribe from an event
   *
   * @param eventName - Name of the event
   * @param callback - The callback to remove (if not provided, removes all listeners)
   * @returns Number of listeners removed
   *
   * @example
   * ```typescript
   * // Remove specific listener
   * bus.off('user:created', handler);
   *
   * // Remove all listeners for an event
   * bus.off('user:created');
   *
   * // Remove all listeners
   * bus.off();
   * ```
   */
  off(eventName?: string, callback?: EventCallback): number {
    let removed = 0;

    if (!eventName) {
      // Remove all listeners
      for (const [name, listeners] of this.listeners.entries()) {
        removed += listeners.length;
        this.stats.totalListeners -= listeners.length;
      }
      this.listeners.clear();
      this.stats.activeListeners = {};
      return removed;
    }

    const listeners = this.listeners.get(eventName);
    if (!listeners) return 0;

    if (!callback) {
      // Remove all listeners for this event
      removed = listeners.length;
      this.stats.totalListeners -= removed;
      this.listeners.delete(eventName);
      this.stats.activeListeners[eventName] = 0;
    } else {
      // Remove specific listener
      const index = listeners.findIndex((l) => l.callback === callback);
      if (index !== -1) {
        listeners.splice(index, 1);
        removed = 1;
        this.stats.totalListeners--;
        this.stats.activeListeners[eventName] = listeners.length;
        if (listeners.length === 0) {
          this.listeners.delete(eventName);
        }
      }
    }

    return removed;
  }

  /**
   * Emit an event
   *
   * @param eventName - Name of the event to emit
   * @param data - Data to pass to listeners
   * @param source - Optional source identifier
   * @returns Promise that resolves when all listeners have been executed
   *
   * @example
   * ```typescript
   * // Synchronous emit
   * bus.emit('user:login', { username: 'john' });
   *
   * // With source tracking
   * bus.emit('order:created', orderData, 'order-service');
   *
   * // Wait for async listeners
   * await bus.emit('async:event', data);
   * ```
   */
  async emit<T = any>(eventName: string, data: T, source?: string): Promise<void> {
    const eventData: EventData<T> = {
      name: eventName,
      data,
      timestamp: Date.now(),
      source,
    };

    // Update stats
    this.stats.totalEvents++;
    this.stats.eventsByType[eventName] = (this.stats.eventsByType[eventName] || 0) + 1;

    // Add to history
    this.addToHistory(eventData);

    // If suspended, queue the event
    if (this.suspended) {
      this.pendingEvents.push(eventData);
      return;
    }

    // Find all matching listeners (including wildcards)
    const matchingListeners = this.findMatchingListeners(eventName);

    // Execute all listeners
    const promises: Promise<void>[] = [];

    for (const { event, config } of matchingListeners) {
      // Apply filter if present
      if (config.filter && !config.filter(data, eventName)) {
        continue;
      }

      try {
        const result = config.callback(data, eventName, source);
        if (result instanceof Promise) {
          promises.push(result.then(() => {
            // Remove once listeners after execution
            if (config.once) {
              this.off(event, config.callback);
            }
          }));
        } else {
          // Remove once listeners after execution
          if (config.once) {
            this.off(event, config.callback);
          }
        }
      } catch (error) {
        console.error(`Error in event listener for "${eventName}":`, error);
      }
    }

    // Wait for all async listeners
    await Promise.all(promises);
  }

  /**
   * Emit an event synchronously (does not wait for async listeners)
   *
   * @param eventName - Name of the event
   * @param data - Data to pass to listeners
   * @param source - Optional source identifier
   *
   * @deprecated Use emit() instead for proper async handling
   */
  emitSync<T = any>(eventName: string, data: T, source?: string): void {
    this.emit(eventName, data, source).catch(console.error);
  }

  /**
   * Find all matching listeners for an event (including wildcards)
   *
   * @param eventName - The event name to match
   * @returns Array of matching event-listener pairs
   */
  private findMatchingListeners(eventName: string): Array<{ event: string; config: ListenerConfig }> {
    const results: Array<{ event: string; config: ListenerConfig }> = [];
    const parts = eventName.split(':');

    for (const [pattern, listeners] of this.listeners.entries()) {
      if (this.matchesPattern(eventName, pattern, parts)) {
        for (const config of listeners) {
          results.push({ event: pattern, config });
        }
      }
    }

    return results;
  }

  /**
   * Check if an event name matches a pattern (supports wildcards)
   *
   * @param eventName - The full event name
   * @param pattern - The pattern to match against (may contain * or **)
   * @param parts - Pre-split event name parts
   * @returns True if the event matches the pattern
   *
   * @example
   * ```typescript
   * matchesPattern('user:created', 'user:*') // true
   * matchesPattern('user:admin:created', 'user:**') // true
   * matchesPattern('user:created', 'user:created') // true
   * ```
   */
  private matchesPattern(eventName: string, pattern: string, parts: string[]): boolean {
    // Exact match
    if (eventName === pattern) {
      return true;
    }

    const patternParts = pattern.split(':');

    // Wildcard matching
    for (let i = 0; i < patternParts.length; i++) {
      const patternPart = patternParts[i];

      // ** matches any remaining parts
      if (patternPart === '**') {
        return true;
      }

      // * matches single part
      if (patternPart === '*') {
        if (i >= parts.length) {
          return false;
        }
        continue;
      }

      // Exact part match
      if (i >= parts.length || patternPart !== parts[i]) {
        return false;
      }
    }

    // Pattern must match all parts
    return patternParts.length === parts.length;
  }

  /**
   * Add event to history
   *
   * @param eventData - The event data to store
   */
  private addToHistory(eventData: EventData): void {
    this.history.push(eventData);

    // Trim history if exceeds max size
    while (this.history.length > this.maxHistorySize) {
      this.history.shift();
    }
  }

  /**
   * Get event history
   *
   * @param limit - Maximum number of events to return (default: all)
   * @param eventName - Filter by event name (optional)
   * @returns Array of historical events
   *
   * @example
   * ```typescript
   * // Get all history
   * const history = bus.getHistory();
   *
   * // Get last 10 events
   * const recent = bus.getHistory(10);
   *
   * // Get history for specific event
   * const userEvents = bus.getHistory(100, 'user:*');
   * ```
   */
  getHistory(limit?: number, eventName?: string): EventData[] {
    let history = [...this.history];

    if (eventName) {
      const parts = eventName.split(':');
      history = history.filter((e) => this.matchesPattern(e.name, eventName, e.name.split(':')));
    }

    if (limit !== undefined && limit > 0) {
      history = history.slice(-limit);
    }

    return history;
  }

  /**
   * Clear event history
   *
   * @param eventName - Clear history for specific event only (optional)
   */
  clearHistory(eventName?: string): void {
    if (!eventName) {
      this.history = [];
    } else {
      const parts = eventName.split(':');
      this.history = this.history.filter((e) => !this.matchesPattern(e.name, eventName, e.name.split(':')));
    }
  }

  /**
   * Suspend event emission (events will be queued)
   *
   * @example
   * ```typescript
   * bus.suspend();
   * // Events are queued but not emitted
   * bus.emit('event', data);
   *
   * // Later...
   * bus.resume(); // Queued events are emitted
   * ```
   */
  suspend(): void {
    this.suspended = true;
  }

  /**
   * Resume event emission (emit all queued events)
   *
   * @param clearPending - If true, discard pending events instead of emitting
   */
  async resume(clearPending: boolean = false): Promise<void> {
    this.suspended = false;

    if (clearPending) {
      this.pendingEvents = [];
      return;
    }

    // Emit all pending events in order
    const pending = [...this.pendingEvents];
    this.pendingEvents = [];

    for (const event of pending) {
      await this.emit(event.name, event.data, event.source);
    }
  }

  /**
   * Check if the bus is suspended
   *
   * @returns True if suspended
   */
  isSuspended(): boolean {
    return this.suspended;
  }

  /**
   * Get pending event count
   *
   * @returns Number of pending events
   */
  getPendingCount(): number {
    return this.pendingEvents.length;
  }

  /**
   * Get statistics
   *
   * @returns EventBus statistics
   *
   * @example
   * ```typescript
   * const stats = bus.getStats();
   * console.log(`Total events: ${stats.totalEvents}`);
   * console.log(`Total listeners: ${stats.totalListeners}`);
   * ```
   */
  getStats(): EventBusStats {
    return { ...this.stats };
  }

  /**
   * Get listener count for an event
   *
   * @param eventName - The event name
   * @returns Number of listeners
   */
  getListenerCount(eventName: string): number {
    const listeners = this.listeners.get(eventName);
    return listeners ? listeners.length : 0;
  }

  /**
   * Get all registered event names
   *
   * @returns Array of event names
   */
  getEventNames(): string[] {
    return Array.from(this.listeners.keys());
  }

  /**
   * Check if an event has listeners
   *
   * @param eventName - The event name to check
   * @returns True if there are listeners
   */
  hasListeners(eventName: string): boolean {
    return this.listeners.has(eventName);
  }

  /**
   * Remove all listeners and clear history
   *
   * @example
   * ```typescript
   * bus.destroy(); // Clean up
   * ```
   */
  destroy(): void {
    this.off();
    this.clearHistory();
    this.pendingEvents = [];
    this.stats = {
      totalEvents: 0,
      totalListeners: 0,
      eventsByType: {},
      activeListeners: {},
    };
  }
}

/**
 * Create a typed event bus
 *
 * @example
 * ```typescript
 * interface Events {
 *   'user:login': { username: string; id: number };
 *   'user:logout': { id: number };
 *   'order:created': { orderId: string; amount: number };
 * }
 *
 * const bus = createTypedEventBus<Events>();
 *
 * // Type-safe subscription
 * bus.on('user:login', (data) => {
 *   console.log(data.username); // TypeScript knows this is string
 * });
 *
 * // Type-safe emission
 * bus.emit('user:login', { username: 'john', id: 123 });
 * ```
 */
export function createTypedEventBus<T extends Record<string, any>>(
  maxHistorySize: number = 100
): EventBus {
  return new EventBus(maxHistorySize);
}

/**
 * Default EventBus instance (singleton)
 *
 * @example
 * ```typescript
 * import { defaultBus } from './mod';
 *
 * defaultBus.on('event', handler);
 * defaultBus.emit('event', data);
 * ```
 */
export const defaultBus = new EventBus();

// Export default
export default EventBus;
