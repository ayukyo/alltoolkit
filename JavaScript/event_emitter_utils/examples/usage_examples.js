/**
 * EventEmitter Utils - Usage Examples
 * 
 * This file demonstrates the various features and use cases
 * for the EventEmitter utility.
 */

const { EventEmitter, createEventEmitter, mixinEventEmitter } = require('../mod.js');

// ============================================
// Example 1: Basic Usage
// ============================================

console.log('\n=== Example 1: Basic Usage ===\n');

const emitter = new EventEmitter();

// Subscribe to an event
emitter.on('greeting', (name) => {
  console.log(`Hello, ${name}!`);
});

// Emit the event
emitter.emit('greeting', 'World');
// Output: Hello, World!

// ============================================
// Example 2: One-time Listeners
// ============================================

console.log('\n=== Example 2: One-time Listeners ===\n');

const onceEmitter = new EventEmitter();

onceEmitter.once('init', () => {
  console.log('This will only run once!');
});

onceEmitter.emit('init'); // Runs
onceEmitter.emit('init'); // Does not run (listener removed)

// ============================================
// Example 3: Multiple Arguments
// ============================================

console.log('\n=== Example 3: Multiple Arguments ===\n');

const multiEmitter = new EventEmitter();

multiEmitter.on('user-action', (action, userId, timestamp) => {
  console.log(`Action: ${action}`);
  console.log(`User: ${userId}`);
  console.log(`Time: ${new Date(timestamp).toISOString()}`);
});

multiEmitter.emit('user-action', 'login', 'user123', Date.now());

// ============================================
// Example 4: Listener Priority
// ============================================

console.log('\n=== Example 4: Listener Priority ===\n');

const priorityEmitter = new EventEmitter();

priorityEmitter.on('process', () => console.log('Low priority (default)'), { priority: 1 });
priorityEmitter.on('process', () => console.log('High priority'), { priority: 10 });
priorityEmitter.on('process', () => console.log('Medium priority'), { priority: 5 });

priorityEmitter.emit('process');
// Output order: High priority, Medium priority, Low priority

// ============================================
// Example 5: Unsubscribing
// ============================================

console.log('\n=== Example 5: Unsubscribing ===\n');

const unsubEmitter = new EventEmitter();

const handler = () => console.log('Handler called');
const unsubscribe = unsubEmitter.on('test', handler);

unsubEmitter.emit('test'); // Handler called
console.log('Unsubscribing...');
unsubscribe();
unsubEmitter.emit('test'); // Not called

// ============================================
// Example 6: Remove All Listeners
// ============================================

console.log('\n=== Example 6: Remove All Listeners ===\n');

const clearEmitter = new EventEmitter();

clearEmitter.on('event1', () => console.log('Event 1'));
clearEmitter.on('event2', () => console.log('Event 2'));

console.log('Events before clear:', clearEmitter.eventNames());
clearEmitter.removeAllListeners();
console.log('Events after clear:', clearEmitter.eventNames());

// ============================================
// Example 7: Wildcard Matching
// ============================================

console.log('\n=== Example 7: Wildcard Matching ===\n');

const wildcardEmitter = new EventEmitter();

// Single segment wildcard
wildcardEmitter.on('user.*', (action) => {
  console.log(`User event: ${action}`);
});

// Multi-segment wildcard
wildcardEmitter.on('system.**', (data) => {
  console.log(`System event: ${JSON.stringify(data)}`);
});

wildcardEmitter.emit('user.created', 'created');
wildcardEmitter.emit('user.deleted', 'deleted');
wildcardEmitter.emit('system.db.connected', { status: 'ok' });
wildcardEmitter.emit('system.cache.redis.flush', { key: 'all' });

// ============================================
// Example 8: Event Namespacing
// ============================================

console.log('\n=== Example 8: Event Namespacing ===\n');

const appEmitter = new EventEmitter();

// Create namespaced emitters
const userEvents = appEmitter.namespace('user');
const orderEvents = appEmitter.namespace('order');

userEvents.on('created', (user) => {
  console.log(`User created: ${user.name}`);
});

orderEvents.on('placed', (order) => {
  console.log(`Order placed: ${order.id}`);
});

userEvents.emit('created', { name: 'Alice' });
orderEvents.emit('placed', { id: 'ORD-001' });

console.log('All events:', appEmitter.eventNames());

// ============================================
// Example 9: Async Event Handling
// ============================================

console.log('\n=== Example 9: Async Event Handling ===\n');

async function asyncExample() {
  const asyncEmitter = new EventEmitter();

  asyncEmitter.on('fetch', async (url) => {
    console.log(`Fetching: ${url}`);
    // Simulate async operation
    await new Promise(resolve => setTimeout(resolve, 100));
    console.log(`Fetched: ${url}`);
  });

  asyncEmitter.on('fetch', (url) => {
    console.log(`Logging fetch: ${url}`);
  });

  console.log('Starting async emit...');
  await asyncEmitter.emitAsync('fetch', 'https://api.example.com/data');
  console.log('Async emit completed');
}

asyncExample();

// ============================================
// Example 10: Event History & Replay
// ============================================

console.log('\n=== Example 10: Event History & Replay ===\n');

const historyEmitter = new EventEmitter({ 
  captureHistory: true, 
  historySize: 10 
});

historyEmitter.on('action', (data) => {
  console.log(`Action: ${data}`);
});

// Emit some events
historyEmitter.emit('action', 'click');
historyEmitter.emit('action', 'scroll');
historyEmitter.emit('action', 'submit');

console.log('\nEvent history:');
console.log(historyEmitter.getHistory('action').map(h => h.args[0]));

console.log('\nReplaying first event:');
historyEmitter.on('action', (data) => {
  console.log(`Replayed action: ${data}`);
});
historyEmitter.replay(0);

// ============================================
// Example 11: Mixin Pattern
// ============================================

console.log('\n=== Example 11: Mixin Pattern ===\n');

// Adding EventEmitter to any object
const userModel = {
  name: '',
  age: 0,
  
  setName(newName) {
    this.name = newName;
    this.emit('nameChanged', { oldName: this.name, newName });
  }
};

mixinEventEmitter(userModel);

userModel.on('nameChanged', ({ oldName, newName }) => {
  console.log(`Name changed from "${oldName}" to "${newName}"`);
});

userModel.setName('Alice');

// ============================================
// Example 12: Error Handling
// ============================================

console.log('\n=== Example 12: Error Handling ===\n');

const errorEmitter = new EventEmitter();

errorEmitter.on('process', () => {
  throw new Error('Something went wrong!');
});

errorEmitter.on('process', () => {
  console.log('This still runs after the error');
});

console.log('Emitting with error...');
errorEmitter.emit('process');

// ============================================
// Example 13: Real-world Use Case - Chat System
// ============================================

console.log('\n=== Example 13: Real-world - Chat System ===\n');

class ChatRoom {
  constructor(name) {
    this.name = name;
    this.emitter = new EventEmitter();
    this.users = new Map();
  }

  join(userId, username) {
    this.users.set(userId, username);
    this.emitter.emit('user-joined', { userId, username, room: this.name });
  }

  leave(userId) {
    const username = this.users.get(userId);
    this.users.delete(userId);
    this.emitter.emit('user-left', { userId, username, room: this.name });
  }

  sendMessage(userId, message) {
    const username = this.users.get(userId);
    this.emitter.emit('message', { userId, username, message, room: this.name });
  }

  on(event, handler) {
    return this.emitter.on(event, handler);
  }
}

const chat = new ChatRoom('General');

// Bot listens to all messages
chat.on('message', ({ username, message }) => {
  console.log(`[${chat.name}] ${username}: ${message}`);
});

// Welcome bot
chat.on('user-joined', ({ username }) => {
  console.log(`👋 Welcome ${username} to ${chat.name}!`);
});

chat.join('user1', 'Alice');
chat.join('user2', 'Bob');
chat.sendMessage('user1', 'Hello everyone!');
chat.sendMessage('user2', 'Hi Alice!');
chat.leave('user2');

// ============================================
// Example 14: Real-world Use Case - State Machine
// ============================================

console.log('\n=== Example 14: Real-world - State Machine ===\n');

class StateMachine {
  constructor(initialState) {
    this.state = initialState;
    this.emitter = new EventEmitter();
  }

  transition(newState) {
    const oldState = this.state;
    this.state = newState;
    this.emitter.emit('state-change', { from: oldState, to: newState });
    this.emitter.emit(`state:${newState}`, { from: oldState });
  }

  onState(state, handler) {
    return this.emitter.on(`state:${state}`, handler);
  }

  onChange(handler) {
    return this.emitter.on('state-change', handler);
  }
}

const machine = new StateMachine('idle');

machine.onChange(({ from, to }) => {
  console.log(`State changed: ${from} -> ${to}`);
});

machine.onState('running', () => {
  console.log('Machine is now running!');
});

machine.onState('stopped', () => {
  console.log('Machine has stopped.');
});

machine.transition('running');
machine.transition('stopped');

// ============================================
// Example 15: Real-world Use Case - Plugin System
// ============================================

console.log('\n=== Example 15: Real-world - Plugin System ===\n');

class PluginManager {
  constructor() {
    this.emitter = new EventEmitter();
    this.plugins = new Map();
  }

  register(name, plugin) {
    this.plugins.set(name, plugin);
    this.emitter.emit('plugin-registered', { name, plugin });
    
    // Call plugin's init if exists
    if (plugin.init) {
      plugin.init(this);
    }
  }

  unregister(name) {
    const plugin = this.plugins.get(name);
    if (plugin) {
      if (plugin.destroy) {
        plugin.destroy();
      }
      this.plugins.delete(name);
      this.emitter.emit('plugin-unregistered', { name });
    }
  }

  on(event, handler) {
    return this.emitter.on(event, handler);
  }

  emit(event, data) {
    return this.emitter.emit(event, data);
  }
}

const pluginManager = new PluginManager();

// Monitor plugin registration
pluginManager.on('plugin-registered', ({ name }) => {
  console.log(`Plugin registered: ${name}`);
});

// Define a logging plugin
const loggingPlugin = {
  name: 'logging',
  init(manager) {
    manager.on('*', (data) => {
      console.log(`[LOG] Event data:`, data);
    });
  },
  destroy() {
    console.log('Logging plugin destroyed');
  }
};

pluginManager.register('logging', loggingPlugin);
pluginManager.emit('custom-event', { message: 'Hello plugins!' });

console.log('\n=== Examples completed ===\n');