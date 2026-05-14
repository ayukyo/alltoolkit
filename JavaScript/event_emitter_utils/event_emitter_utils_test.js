/**
 * EventEmitter Utils Test Suite
 * 
 * Comprehensive tests for the EventEmitter utility
 */

const assert = require('assert');
const { EventEmitter, NamespacedEmitter, createEventEmitter, mixinEventEmitter } = require('./mod.js');

// Test helper
let testCount = 0;
let passCount = 0;
let failCount = 0;

function test(name, fn) {
  testCount++;
  try {
    fn();
    passCount++;
    console.log(`✓ ${name}`);
  } catch (error) {
    failCount++;
    console.log(`✗ ${name}`);
    console.log(`  Error: ${error.message}`);
  }
}

function suite(name, fn) {
  console.log(`\n${name}`);
  console.log('='.repeat(50));
  fn();
}

// ============================================
// Basic EventEmitter Tests
// ============================================

suite('Basic EventEmitter', () => {
  test('should create an EventEmitter instance', () => {
    const emitter = new EventEmitter();
    assert.ok(emitter instanceof EventEmitter);
  });

  test('should subscribe and emit events', () => {
    const emitter = new EventEmitter();
    let called = false;
    
    emitter.on('test', () => {
      called = true;
    });
    
    emitter.emit('test');
    assert.strictEqual(called, true);
  });

  test('should pass arguments to listeners', () => {
    const emitter = new EventEmitter();
    let received = null;
    
    emitter.on('test', (arg) => {
      received = arg;
    });
    
    emitter.emit('test', 'hello');
    assert.strictEqual(received, 'hello');
  });

  test('should pass multiple arguments to listeners', () => {
    const emitter = new EventEmitter();
    let received = null;
    
    emitter.on('test', (a, b, c) => {
      received = [a, b, c];
    });
    
    emitter.emit('test', 1, 2, 3);
    assert.deepStrictEqual(received, [1, 2, 3]);
  });

  test('should return true when event has listeners', () => {
    const emitter = new EventEmitter();
    emitter.on('test', () => {});
    
    const result = emitter.emit('test');
    assert.strictEqual(result, true);
  });

  test('should return false when event has no listeners', () => {
    const emitter = new EventEmitter();
    
    const result = emitter.emit('nonexistent');
    assert.strictEqual(result, false);
  });
});

// ============================================
// once() Tests
// ============================================

suite('once() method', () => {
  test('should fire only once', () => {
    const emitter = new EventEmitter();
    let count = 0;
    
    emitter.once('test', () => {
      count++;
    });
    
    emitter.emit('test');
    emitter.emit('test');
    
    assert.strictEqual(count, 1);
  });

  test('should receive correct arguments', () => {
    const emitter = new EventEmitter();
    let received = null;
    
    emitter.once('test', (arg) => {
      received = arg;
    });
    
    emitter.emit('test', 'data');
    assert.strictEqual(received, 'data');
  });

  test('should remove listener after first emit', () => {
    const emitter = new EventEmitter();
    
    emitter.once('test', () => {});
    
    assert.strictEqual(emitter.listenerCount('test'), 1);
    emitter.emit('test');
    assert.strictEqual(emitter.listenerCount('test'), 0);
  });
});

// ============================================
// off() Tests
// ============================================

suite('off() method', () => {
  test('should remove a specific listener', () => {
    const emitter = new EventEmitter();
    const handler = () => {};
    
    emitter.on('test', handler);
    assert.strictEqual(emitter.listenerCount('test'), 1);
    
    emitter.off('test', handler);
    assert.strictEqual(emitter.listenerCount('test'), 0);
  });

  test('should not remove other listeners', () => {
    const emitter = new EventEmitter();
    const handler1 = () => {};
    const handler2 = () => {};
    
    emitter.on('test', handler1);
    emitter.on('test', handler2);
    
    emitter.off('test', handler1);
    
    assert.strictEqual(emitter.listenerCount('test'), 1);
  });

  test('should do nothing for nonexistent event', () => {
    const emitter = new EventEmitter();
    
    // Should not throw
    emitter.off('nonexistent', () => {});
  });

  test('should return emitter for chaining', () => {
    const emitter = new EventEmitter();
    const result = emitter.off('test', () => {});
    
    assert.strictEqual(result, emitter);
  });
});

// ============================================
// removeAllListeners() Tests
// ============================================

suite('removeAllListeners() method', () => {
  test('should remove all listeners for specific event', () => {
    const emitter = new EventEmitter();
    
    emitter.on('test', () => {});
    emitter.on('test', () => {});
    emitter.on('other', () => {});
    
    emitter.removeAllListeners('test');
    
    assert.strictEqual(emitter.listenerCount('test'), 0);
    assert.strictEqual(emitter.listenerCount('other'), 1);
  });

  test('should remove all listeners when no event specified', () => {
    const emitter = new EventEmitter();
    
    emitter.on('test1', () => {});
    emitter.on('test2', () => {});
    emitter.on('test3', () => {});
    
    emitter.removeAllListeners();
    
    assert.deepStrictEqual(emitter.eventNames(), []);
  });
});

// ============================================
// Priority Tests
// ============================================

suite('Listener priority', () => {
  test('should call listeners in priority order', () => {
    const emitter = new EventEmitter();
    const order = [];
    
    emitter.on('test', () => order.push('low'), { priority: 1 });
    emitter.on('test', () => order.push('high'), { priority: 10 });
    emitter.on('test', () => order.push('medium'), { priority: 5 });
    
    emitter.emit('test');
    
    assert.deepStrictEqual(order, ['high', 'medium', 'low']);
  });

  test('should handle equal priorities', () => {
    const emitter = new EventEmitter();
    const order = [];
    
    emitter.on('test', () => order.push(1), { priority: 5 });
    emitter.on('test', () => order.push(2), { priority: 5 });
    emitter.on('test', () => order.push(3), { priority: 5 });
    
    emitter.emit('test');
    
    assert.strictEqual(order.length, 3);
  });
});

// ============================================
// Wildcard Tests
// ============================================

suite('Wildcard matching', () => {
  test('should match single segment wildcards', () => {
    const emitter = new EventEmitter();
    let matched = false;
    
    emitter.on('user.*', () => {
      matched = true;
    });
    
    emitter.emit('user.created');
    assert.strictEqual(matched, true);
  });

  test('should match multiple segment wildcards', () => {
    const emitter = new EventEmitter();
    const matched = [];
    
    emitter.on('user.**', () => {
      matched.push(true);
    });
    
    emitter.emit('user.created');
    emitter.emit('user.profile.updated');
    emitter.emit('user.settings.theme.changed');
    
    assert.strictEqual(matched.length, 3);
  });

  test('should not match incorrect patterns', () => {
    const emitter = new EventEmitter();
    let matched = false;
    
    emitter.on('user.created', () => {
      matched = true;
    });
    
    emitter.emit('user.updated');
    assert.strictEqual(matched, false);
  });
});

// ============================================
// Async Tests
// ============================================

suite('Async emit', () => {
  test('should handle async emit', async () => {
    const emitter = new EventEmitter();
    let called = false;
    
    emitter.on('test', async () => {
      await new Promise(resolve => setTimeout(resolve, 10));
      called = true;
    });
    
    await emitter.emitAsync('test');
    assert.strictEqual(called, true);
  });

  test('should handle sync listeners in async emit', async () => {
    const emitter = new EventEmitter();
    let called = false;
    
    emitter.on('test', () => {
      called = true;
    });
    
    await emitter.emitAsync('test');
    assert.strictEqual(called, true);
  });

  test('should handle mixed sync and async listeners', async () => {
    const emitter = new EventEmitter();
    const order = [];
    
    emitter.on('test', () => order.push(1));
    emitter.on('test', async () => {
      await new Promise(resolve => setTimeout(resolve, 5));
      order.push(2);
    });
    emitter.on('test', () => order.push(3));
    
    await emitter.emitAsync('test');
    
    assert.deepStrictEqual(order, [1, 2, 3]);
  });
});

// ============================================
// History Tests
// ============================================

suite('Event history', () => {
  test('should capture history when enabled', () => {
    const emitter = new EventEmitter({ captureHistory: true });
    
    emitter.emit('test', 'data1');
    emitter.emit('test', 'data2');
    emitter.emit('other', 'data3');
    
    const history = emitter.getHistory();
    
    assert.strictEqual(history.length, 3);
    assert.strictEqual(history[0].event, 'test');
    assert.deepStrictEqual(history[0].args, ['data1']);
  });

  test('should not capture history when disabled', () => {
    const emitter = new EventEmitter({ captureHistory: false });
    
    emitter.emit('test', 'data');
    
    const history = emitter.getHistory();
    assert.strictEqual(history.length, 0);
  });

  test('should filter history by event name', () => {
    const emitter = new EventEmitter({ captureHistory: true });
    
    emitter.emit('test', 'data1');
    emitter.emit('other', 'data2');
    emitter.emit('test', 'data3');
    
    const history = emitter.getHistory('test');
    assert.strictEqual(history.length, 2);
  });

  test('should limit history size', () => {
    const emitter = new EventEmitter({ captureHistory: true, historySize: 5 });
    
    for (let i = 0; i < 10; i++) {
      emitter.emit('test', i);
    }
    
    const history = emitter.getHistory();
    assert.strictEqual(history.length, 5);
    assert.strictEqual(history[0].args[0], 5); // First kept event
    assert.strictEqual(history[4].args[0], 9); // Last event
  });

  test('should replay historical event', () => {
    const emitter = new EventEmitter({ captureHistory: true });
    const results = [];
    
    emitter.on('test', (data) => results.push(data));
    
    emitter.emit('test', 'original');
    
    // Remove the listener and add a new one
    emitter.removeAllListeners('test');
    emitter.on('test', (data) => results.push(`replayed: ${data}`));
    
    emitter.replay(0);
    
    assert.deepStrictEqual(results, ['original', 'replayed: original']);
  });

  test('should clear history', () => {
    const emitter = new EventEmitter({ captureHistory: true });
    
    emitter.emit('test', 'data');
    emitter.clearHistory();
    
    const history = emitter.getHistory();
    assert.strictEqual(history.length, 0);
  });
});

// ============================================
// Namespace Tests
// ============================================

suite('Namespaced emitter', () => {
  test('should prefix event names with namespace', () => {
    const emitter = new EventEmitter();
    const ns = emitter.namespace('user');
    let received = null;
    
    ns.on('created', (data) => {
      received = data;
    });
    
    ns.emit('created', 'test data');
    
    assert.strictEqual(received, 'test data');
    assert.strictEqual(emitter.listenerCount('user.created'), 1);
  });

  test('should work with once', () => {
    const emitter = new EventEmitter();
    const ns = emitter.namespace('app');
    let count = 0;
    
    ns.once('init', () => count++);
    
    ns.emit('init');
    ns.emit('init');
    
    assert.strictEqual(count, 1);
  });

  test('should work with off', () => {
    const emitter = new EventEmitter();
    const ns = emitter.namespace('app');
    const handler = () => {};
    
    ns.on('test', handler);
    assert.strictEqual(ns.listenerCount('test'), 1);
    
    ns.off('test', handler);
    assert.strictEqual(ns.listenerCount('test'), 0);
  });
});

// ============================================
// Mixin Tests
// ============================================

suite('mixinEventEmitter', () => {
  test('should add EventEmitter methods to object', () => {
    const obj = {};
    mixinEventEmitter(obj);
    
    assert.ok(typeof obj.on === 'function');
    assert.ok(typeof obj.off === 'function');
    assert.ok(typeof obj.emit === 'function');
    assert.ok(typeof obj.once === 'function');
  });

  test('should allow object to emit events', () => {
    const obj = { name: 'test' };
    mixinEventEmitter(obj);
    
    let received = null;
    obj.on('change', (data) => {
      received = data;
    });
    
    obj.emit('change', 'updated');
    
    assert.strictEqual(received, 'updated');
  });
});

// ============================================
// createEventEmitter Tests
// ============================================

suite('createEventEmitter', () => {
  test('should create EventEmitter instance', () => {
    const emitter = createEventEmitter();
    assert.ok(emitter instanceof EventEmitter);
  });

  test('should accept options', () => {
    const emitter = createEventEmitter({ maxListeners: 50 });
    assert.strictEqual(emitter.getMaxListeners(), 50);
  });
});

// ============================================
// Error Handling Tests
// ============================================

suite('Error handling', () => {
  test('should handle errors in listeners gracefully', () => {
    const emitter = new EventEmitter();
    let secondCalled = false;
    
    emitter.on('test', () => {
      throw new Error('Test error');
    });
    
    emitter.on('test', () => {
      secondCalled = true;
    });
    
    // Should not throw
    emitter.emit('test');
    
    // Second listener should still be called
    assert.strictEqual(secondCalled, true);
  });

  test('should throw for non-function listener', () => {
    const emitter = new EventEmitter();
    
    assert.throws(() => {
      emitter.on('test', 'not a function');
    }, TypeError);
  });

  test('should throw for non-function once listener', () => {
    const emitter = new EventEmitter();
    
    assert.throws(() => {
      emitter.once('test', {});
    }, TypeError);
  });
});

// ============================================
// Max Listeners Tests
// ============================================

suite('Max listeners', () => {
  test('should warn when exceeding max listeners', () => {
    const warnings = [];
    const originalWarn = console.warn;
    console.warn = (msg) => warnings.push(msg);
    
    const emitter = new EventEmitter({ maxListeners: 2 });
    
    emitter.on('test', () => {});
    emitter.on('test', () => {});
    emitter.on('test', () => {}); // Should trigger warning
    
    console.warn = originalWarn;
    
    assert.strictEqual(warnings.length, 1);
    assert.ok(warnings[0].includes('memory leak'));
  });

  test('should allow setting max listeners', () => {
    const emitter = new EventEmitter();
    
    emitter.setMaxListeners(50);
    
    assert.strictEqual(emitter.getMaxListeners(), 50);
  });
});

// ============================================
// Edge Cases
// ============================================

suite('Edge cases', () => {
  test('should handle removing listener during iteration', () => {
    const emitter = new EventEmitter();
    const order = [];
    
    const handler1 = () => {
      order.push(1);
      emitter.off('test', handler2);
    };
    const handler2 = () => order.push(2);
    
    emitter.on('test', handler1);
    emitter.on('test', handler2);
    
    emitter.emit('test');
    
    assert.deepStrictEqual(order, [1, 2]);
  });

  test('should handle self-removing listener', () => {
    const emitter = new EventEmitter();
    const handler = () => {
      emitter.off('test', handler);
    };
    
    emitter.on('test', handler);
    
    emitter.emit('test');
    emitter.emit('test');
    
    assert.strictEqual(emitter.listenerCount('test'), 0);
  });

  test('should return unsubscribe function from on()', () => {
    const emitter = new EventEmitter();
    let count = 0;
    
    const unsubscribe = emitter.on('test', () => count++);
    
    emitter.emit('test');
    assert.strictEqual(count, 1);
    
    unsubscribe();
    emitter.emit('test');
    assert.strictEqual(count, 1); // Still 1, listener removed
  });

  test('should return unsubscribe function from once()', () => {
    const emitter = new EventEmitter();
    let count = 0;
    
    const unsubscribe = emitter.once('test', () => count++);
    
    unsubscribe();
    emitter.emit('test');
    
    assert.strictEqual(count, 0);
  });

  test('should handle empty event names', () => {
    const emitter = new EventEmitter();
    let called = false;
    
    emitter.on('', () => called = true);
    emitter.emit('');
    
    assert.strictEqual(called, true);
  });

  test('should handle special characters in event names', () => {
    const emitter = new EventEmitter();
    let called = false;
    
    emitter.on('user:action/created', () => called = true);
    emitter.emit('user:action/created');
    
    assert.strictEqual(called, true);
  });
});

// ============================================
// Performance Tests
// ============================================

suite('Performance', () => {
  test('should handle many listeners efficiently', () => {
    const emitter = new EventEmitter({ maxListeners: 10000 });
    const start = Date.now();
    
    for (let i = 0; i < 1000; i++) {
      emitter.on('test', () => {});
    }
    
    const elapsed = Date.now() - start;
    assert.ok(elapsed < 100, `Adding 1000 listeners took ${elapsed}ms`);
    
    emitter.removeAllListeners('test');
    assert.strictEqual(emitter.listenerCount('test'), 0);
  });

  test('should emit to many listeners efficiently', () => {
    const emitter = new EventEmitter({ maxListeners: 10000 });
    let count = 0;
    
    for (let i = 0; i < 100; i++) {
      emitter.on('test', () => count++);
    }
    
    const start = Date.now();
    emitter.emit('test');
    const elapsed = Date.now() - start;
    
    assert.strictEqual(count, 100);
    assert.ok(elapsed < 10, `Emitting to 100 listeners took ${elapsed}ms`);
  });
});

// ============================================
// Print Summary
// ============================================

console.log('\n' + '='.repeat(50));
console.log(`Tests: ${testCount}`);
console.log(`Passed: ${passCount}`);
console.log(`Failed: ${failCount}`);
console.log('='.repeat(50));

if (failCount === 0) {
  console.log('\n✓ All tests passed!\n');
  process.exit(0);
} else {
  console.log('\n✗ Some tests failed.\n');
  process.exit(1);
}