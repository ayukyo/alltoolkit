/**
 * AllToolkit - TypeScript Event Bus
 * Advanced Usage Examples
 *
 * This file demonstrates advanced patterns and real-world use cases.
 */

import { EventBus, createTypedEventBus, EventData } from '../mod.ts';

(async () => {
  console.log('='.repeat(60));
  console.log('EventBus Advanced Usage Examples');
  console.log('='.repeat(60));

// ============================================================================
// Example 1: Type-Safe Event Bus
// ============================================================================
console.log('\n1. Type-Safe Event Bus');
console.log('-'.repeat(60));

// Define event types
interface AppEvents {
  'user:login': { username: string; id: number; timestamp: Date };
  'user:logout': { id: number; duration: number };
  'order:created': { orderId: string; amount: number; items: string[] };
  'order:shipped': { orderId: string; trackingId: string };
  'notification:email': { to: string; subject: string; body: string };
}

const typedBus = createTypedEventBus<AppEvents>();

typedBus.on('user:login', (data) => {
  // TypeScript knows data is { username: string; id: number; timestamp: Date }
  console.log(`   User ${data.username} (ID: ${data.id}) logged in`);
  console.log(`   Timestamp: ${data.timestamp.toLocaleTimeString()}`);
});

typedBus.emit('user:login', {
  username: 'john_doe',
  id: 12345,
  timestamp: new Date()
});

// ============================================================================
// Example 2: Component Communication System
// ============================================================================
console.log('\n2. Component Communication System');
console.log('-'.repeat(60));

class Component {
  name: string;
  bus: EventBus;

  constructor(name: string, bus: EventBus) {
    this.name = name;
    this.bus = bus;
  }

  send(event: string, data: any) {
    console.log(`   [${this.name}] Sending: ${event}`);
    this.bus.emit(event, data, this.name);
  }

  receive(event: string, handler: Function) {
    this.bus.on(event, (data, source) => {
      console.log(`   [${this.name}] Received: ${event} (from: ${source || 'unknown'})`);
      handler(data);
    });
  }
}

const commBus = new EventBus();

const componentA = new Component('ComponentA', commBus);
const componentB = new Component('ComponentB', commBus);
const componentC = new Component('ComponentC', commBus);

// Set up communication
componentB.receive('component:message', (data) => {
  console.log(`   [${componentB.name}] Processing: ${data.content}`);
});

componentC.receive('component:message', (data) => {
  console.log(`   [${componentC.name}] Processing: ${data.content}`);
});

// Component A broadcasts to B and C
componentA.send('component:message', { content: 'Hello from A!' });

// ============================================================================
// Example 3: Event Sourcing / Audit Log
// ============================================================================
console.log('\n3. Event Sourcing / Audit Log');
console.log('-'.repeat(60));

class AuditLogger {
  private bus: EventBus;
  private logs: EventData[] = [];

  constructor() {
    this.bus = new EventBus(1000);
    
    // Log all events
    this.bus.on('**', (data, eventName) => {
      this.logs.push({
        name: eventName,
        data,
        timestamp: Date.now(),
        source: 'audit'
      });
      console.log(`   [AUDIT] ${eventName} at ${new Date().toLocaleTimeString()}`);
    });
  }

  emit(event: string, data: any, source?: string) {
    this.bus.emit(event, data, source);
  }

  getLogs(filter?: string): EventData[] {
    return this.bus.getHistory(undefined, filter);
  }

  replay(): void {
    console.log('   Replaying all events...');
    for (const log of this.logs) {
      console.log(`   → ${log.name}: ${JSON.stringify(log.data)}`);
    }
  }
}

const audit = new AuditLogger();

audit.emit('user:created', { id: 1, name: 'Alice' }, 'user-service');
audit.emit('order:placed', { orderId: 'ORD-001', amount: 99.99 }, 'order-service');
audit.emit('payment:processed', { orderId: 'ORD-001', status: 'success' }, 'payment-service');

console.log('   Audit logs captured:', audit.getLogs().length);

// ============================================================================
// Example 4: Plugin System
// ============================================================================
console.log('\n4. Plugin System');
console.log('-'.repeat(60));

interface Plugin {
  name: string;
  version: string;
  initialize: () => Promise<void>;
  shutdown: () => Promise<void>;
}

class PluginManager {
  private bus: EventBus;
  private plugins: Map<string, Plugin> = new Map();

  constructor() {
    this.bus = new EventBus();
    
    // Listen for plugin registration
    this.bus.on('plugin:registered', (data) => {
      console.log(`   Plugin registered: ${data.name} v${data.version}`);
      this.plugins.set(data.name, data.plugin);
    });
  }

  register(plugin: Plugin) {
    this.bus.emit('plugin:registered', { name: plugin.name, version: plugin.version, plugin });
  }

  async initializeAll() {
    console.log('   Initializing all plugins...');
    await this.bus.emit('system:initialize', {});
    
    for (const [name, plugin] of this.plugins) {
      await plugin.initialize();
      console.log(`   ✓ ${name} initialized`);
    }
  }

  async shutdownAll() {
    console.log('   Shutting down all plugins...');
    await this.bus.emit('system:shutdown', {});
    
    for (const [name, plugin] of this.plugins) {
      await plugin.shutdown();
      console.log(`   ✓ ${name} shutdown`);
    }
  }

  on(event: string, handler: Function) {
    return this.bus.on(event, handler);
  }

  emit(event: string, data: any) {
    return this.bus.emit(event, data);
  }
}

// Create plugin manager
const pluginManager = new PluginManager();

// Create sample plugins
const loggingPlugin: Plugin = {
  name: 'logging-plugin',
  version: '1.0.0',
  initialize: async () => console.log('   [LoggingPlugin] Initialized'),
  shutdown: async () => console.log('   [LoggingPlugin] Shutdown')
};

const metricsPlugin: Plugin = {
  name: 'metrics-plugin',
  version: '2.1.0',
  initialize: async () => console.log('   [MetricsPlugin] Initialized'),
  shutdown: async () => console.log('   [MetricsPlugin] Shutdown')
};

const cachePlugin: Plugin = {
  name: 'cache-plugin',
  version: '1.5.0',
  initialize: async () => console.log('   [CachePlugin] Initialized'),
  shutdown: async () => console.log('   [CachePlugin] Shutdown')
};

// Register plugins
pluginManager.register(loggingPlugin);
pluginManager.register(metricsPlugin);
pluginManager.register(cachePlugin);

// Initialize all plugins
await pluginManager.initializeAll();

// ============================================================================
// Example 5: State Management with Event Bus
// ============================================================================
console.log('\n5. State Management');
console.log('-'.repeat(60));

class Store<T extends Record<string, any>> {
  private state: T;
  private bus: EventBus;

  constructor(initialState: T) {
    this.state = initialState;
    this.bus = new EventBus();
  }

  getState<K extends keyof T>(key: K): T[K] {
    return this.state[key];
  }

  setState<K extends keyof T>(key: K, value: T[K]): void {
    const oldValue = this.state[key];
    this.state[key] = value;
    console.log(`   State updated: ${String(key)} = ${JSON.stringify(value)}`);
    this.bus.emit(`state:${String(key)}`, { oldValue, newValue: value });
  }

  subscribe<K extends keyof T>(key: K, callback: (value: T[K]) => void): () => void {
    return this.bus.on(`state:${String(key)}`, (data) => {
      callback(data.newValue);
    });
  }

  subscribeAll(callback: (key: string, value: any) => void): () => void {
    return this.bus.on('state:**', (data, eventName) => {
      const key = eventName.replace('state:', '');
      callback(key, data.newValue);
    });
  }
}

// Create store
const store = new Store({
  user: null as string | null,
  count: 0,
  theme: 'light' as 'light' | 'dark'
});

// Subscribe to state changes
store.subscribe('count', (value) => {
  console.log(`   [Subscriber] Count changed to: ${value}`);
});

store.subscribeAll((key, value) => {
  console.log(`   [Global Subscriber] ${key} changed to: ${JSON.stringify(value)}`);
});

// Update state
store.setState('count', 1);
store.setState('count', 2);
store.setState('theme', 'dark');
store.setState('user', 'alice');

// ============================================================================
// Example 6: Batch Processing with Suspend/Resume
// ============================================================================
console.log('\n6. Batch Processing');
console.log('-'.repeat(60));

const batchBus = new EventBus();
let processedCount = 0;

batchBus.on('item:processed', (data) => {
  processedCount++;
  console.log(`   Processed item ${data.id} (${processedCount}/10)`);
});

console.log('   Starting batch processing...');

// Suspend to queue events
batchBus.suspend();
console.log('   Bus suspended, queuing events...');

// Process items (events are queued)
for (let i = 1; i <= 10; i++) {
  batchBus.emit('item:processed', { id: i });
}

console.log(`   Queued ${batchBus.getPendingCount()} events`);
console.log('   Resuming batch processing...');

// Resume to process all at once
await batchBus.resume();
console.log(`   Batch complete! Total processed: ${processedCount}`);

// ============================================================================
// Example 7: Statistics and Monitoring
// ============================================================================
console.log('\n7. Statistics and Monitoring');
console.log('-'.repeat(60));

const monitorBus = new EventBus();

// Add some activity
monitorBus.on('request', () => {});
monitorBus.on('request', () => {});
monitorBus.on('response', () => {});
monitorBus.on('error', () => {});
monitorBus.on('error', () => {});
monitorBus.on('error', () => {});

// Emit events
for (let i = 0; i < 100; i++) {
  monitorBus.emit('request', { id: i });
}
for (let i = 0; i < 95; i++) {
  monitorBus.emit('response', { id: i });
}
for (let i = 0; i < 5; i++) {
  monitorBus.emit('error', { message: `Error ${i}` });
}

// Get statistics
const stats = monitorBus.getStats();
console.log('   Event Statistics:');
console.log(`   - Total Events: ${stats.totalEvents}`);
console.log(`   - Total Listeners: ${stats.totalListeners}`);
console.log('   - Events by Type:');
for (const [type, count] of Object.entries(stats.eventsByType)) {
  console.log(`     • ${type}: ${count}`);
}
console.log('   - Active Listeners:');
for (const [event, count] of Object.entries(stats.activeListeners)) {
  console.log(`     • ${event}: ${count}`);
}

// ============================================================================
// Example 8: Error Handling
// ============================================================================
console.log('\n8. Error Handling');
console.log('-'.repeat(60));

const errorBus = new EventBus();

errorBus.on('risky:event', () => {
  console.log('   First listener: OK');
});

errorBus.on('risky:event', () => {
  console.log('   Second listener: Throwing error...');
  throw new Error('Something went wrong!');
});

errorBus.on('risky:event', () => {
  console.log('   Third listener: Still called despite error!');
});

console.log('   Emitting event with error-throwing listener...');
errorBus.emit('risky:event', {});
console.log('   Event emission completed (other listeners still executed)');

// ============================================================================
// Summary
// ============================================================================
console.log('\n' + '='.repeat(60));
console.log('Advanced Examples Completed!');
console.log('='.repeat(60));
console.log('\nKey Takeaways:');
console.log('  ✓ Type-safe event buses with TypeScript');
console.log('  ✓ Component communication patterns');
console.log('  ✓ Event sourcing and audit logging');
console.log('  ✓ Plugin system architecture');
console.log('  ✓ State management with subscriptions');
console.log('  ✓ Batch processing with suspend/resume');
console.log('  ✓ Statistics and monitoring');
console.log('  ✓ Robust error handling');
console.log('='.repeat(60));
})();
