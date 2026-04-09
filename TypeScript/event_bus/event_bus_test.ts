/**
 * AllToolkit - TypeScript Event Bus Tests
 *
 * Comprehensive test suite for the EventBus class.
 * Covers: subscription, emission, wildcards, once listeners,
 * priorities, filters, history, suspension, and edge cases.
 *
 * Run with: npx tsx event_bus_test.ts
 * Or: deno run --allow-read event_bus_test.ts
 * Or: bun run event_bus_test.ts
 */

import { EventBus, createTypedEventBus, defaultBus, EventData } from './mod.ts';

// Test runner utilities
let passed = 0;
let failed = 0;
const failures: string[] = [];

function assert(condition: boolean, message: string): void {
  if (condition) {
    passed++;
    console.log(`  ✓ ${message}`);
  } else {
    failed++;
    failures.push(message);
    console.log(`  ✗ ${message}`);
  }
}

function assertEquals<T>(actual: T, expected: T, message: string): void {
  const condition = JSON.stringify(actual) === JSON.stringify(expected);
  if (!condition) {
    console.log(`    Expected: ${JSON.stringify(expected)}`);
    console.log(`    Actual: ${JSON.stringify(actual)}`);
  }
  assert(condition, message);
}

function assertTrue(condition: boolean, message: string): void {
  assert(condition, message);
}

function assertFalse(condition: boolean, message: string): void {
  assert(!condition, message);
}

async function runTest(name: string, fn: () => void | Promise<void>): Promise<void> {
  console.log(`\n${name}`);
  try {
    await fn();
  } catch (error) {
    failed++;
    failures.push(`${name}: ${error}`);
    console.log(`  ✗ Error: ${error}`);
  }
}

async function runTests(): Promise<void> {
  console.log('='.repeat(60));
  console.log('EventBus Test Suite');
  console.log('='.repeat(60));

  // Test 1: Basic subscription and emission
  await runTest('Basic Subscription and Emission', () => {
    const bus = new EventBus();
    let received = false;
    let receivedData: any = null;

    bus.on('test:event', (data) => {
      received = true;
      receivedData = data;
    });

    bus.emit('test:event', { value: 42 });

    assertTrue(received, 'Listener should be called');
    assertEquals(receivedData?.value, 42, 'Data should be passed correctly');
  });

  // Test 2: Multiple listeners
  await runTest('Multiple Listeners', () => {
    const bus = new EventBus();
    let count = 0;

    bus.on('multi:event', () => count++);
    bus.on('multi:event', () => count++);
    bus.on('multi:event', () => count++);

    bus.emit('multi:event', {});

    assertEquals(count, 3, 'All three listeners should be called');
  });

  // Test 3: Once listener
  await runTest('Once Listener', () => {
    const bus = new EventBus();
    let count = 0;

    bus.once('once:event', () => count++);

    bus.emit('once:event', {});
    bus.emit('once:event', {});
    bus.emit('once:event', {});

    assertEquals(count, 1, 'Once listener should only be called once');
  });

  // Test 4: Unsubscribe
  await runTest('Unsubscribe', () => {
    const bus = new EventBus();
    let count = 0;

    const handler = () => count++;
    const unsubscribe = bus.on('unsubscribe:event', handler);

    bus.emit('unsubscribe:event', {});
    unsubscribe();
    bus.emit('unsubscribe:event', {});

    assertEquals(count, 1, 'Listener should not be called after unsubscribe');
  });

  // Test 5: Remove all listeners for event
  await runTest('Remove All Listeners for Event', () => {
    const bus = new EventBus();
    let count = 0;

    bus.on('remove:event', () => count++);
    bus.on('remove:event', () => count++);

    const removed = bus.off('remove:event');
    bus.emit('remove:event', {});

    assertEquals(removed, 2, 'Should remove 2 listeners');
    assertEquals(count, 0, 'No listeners should be called');
  });

  // Test 6: Remove all listeners
  await runTest('Remove All Listeners', () => {
    const bus = new EventBus();
    let count = 0;

    bus.on('event1', () => count++);
    bus.on('event2', () => count++);
    bus.on('event3', () => count++);

    const removed = bus.off();
    bus.emit('event1', {});
    bus.emit('event2', {});
    bus.emit('event3', {});

    assertEquals(removed, 3, 'Should remove all 3 listeners');
    assertEquals(count, 0, 'No listeners should be called');
  });

  // Test 7: Wildcard single level (*)
  await runTest('Wildcard Single Level (*)', () => {
    const bus = new EventBus();
    const events: string[] = [];

    bus.on('user:*', (data, eventName) => {
      events.push(eventName);
    });

    bus.emit('user:login', {});
    bus.emit('user:logout', {});
    bus.emit('user:created', {});
    bus.emit('admin:login', {});

    assertEquals(events.length, 3, 'Should match 3 user events');
    assertTrue(events.includes('user:login'), 'Should include user:login');
    assertTrue(events.includes('user:logout'), 'Should include user:logout');
    assertTrue(events.includes('user:created'), 'Should include user:created');
  });

  // Test 8: Wildcard multi level (**)
  await runTest('Wildcard Multi Level (**)', () => {
    const bus = new EventBus();
    const events: string[] = [];

    bus.on('app:**', (data, eventName) => {
      events.push(eventName);
    });

    bus.emit('app:start', {});
    bus.emit('app:user:login', {});
    bus.emit('app:user:profile:update', {});
    bus.emit('other:event', {});

    assertEquals(events.length, 3, 'Should match 3 app events at any depth');
  });

  // Test 9: Priority execution
  await runTest('Priority Execution', () => {
    const bus = new EventBus();
    const executionOrder: number[] = [];

    bus.on('priority:event', () => executionOrder.push(1), { priority: 1 });
    bus.on('priority:event', () => executionOrder.push(3), { priority: 3 });
    bus.on('priority:event', () => executionOrder.push(2), { priority: 2 });
    bus.on('priority:event', () => executionOrder.push(0), { priority: 0 });

    bus.emit('priority:event', {});

    assertEquals(executionOrder, [3, 2, 1, 0], 'Listeners should execute in priority order (highest first)');
  });

  // Test 10: Event filter
  await runTest('Event Filter', () => {
    const bus = new EventBus();
    let filteredCount = 0;
    let unfilteredCount = 0;

    bus.on('filtered:event', () => filteredCount++, {
      filter: (data) => data.value > 10,
    });

    bus.on('filtered:event', () => unfilteredCount++);

    bus.emit('filtered:event', { value: 5 });
    bus.emit('filtered:event', { value: 15 });
    bus.emit('filtered:event', { value: 20 });

    assertEquals(filteredCount, 2, 'Filtered listener should only be called for value > 10');
    assertEquals(unfilteredCount, 3, 'Unfiltered listener should be called for all events');
  });

  // Test 11: Event history
  await runTest('Event History', () => {
    const bus = new EventBus(10);

    for (let i = 0; i < 15; i++) {
      bus.emit('history:event', { index: i });
    }

    const history = bus.getHistory();
    assertEquals(history.length, 10, 'History should be limited to max size');
    assertEquals(history[0]?.data?.index, 5, 'Oldest event should be index 5');
    assertEquals(history[9]?.data?.index, 14, 'Newest event should be index 14');
  });

  // Test 12: History with limit
  await runTest('History with Limit', () => {
    const bus = new EventBus();

    for (let i = 0; i < 20; i++) {
      bus.emit('limited:event', { index: i });
    }

    const limited = bus.getHistory(5);
    assertEquals(limited.length, 5, 'Should return only 5 events');
    assertEquals(limited[0]?.data?.index, 15, 'Should return last 5 events');
  });

  // Test 13: History filtering
  await runTest('History Filtering', () => {
    const bus = new EventBus();

    bus.emit('type:a', { type: 'a' });
    bus.emit('type:b', { type: 'b' });
    bus.emit('type:a', { type: 'a' });
    bus.emit('type:c', { type: 'c' });

    const typeAEvents = bus.getHistory(undefined, 'type:a');
    assertEquals(typeAEvents.length, 2, 'Should return only type:a events');
  });

  // Test 14: Clear history
  await runTest('Clear History', () => {
    const bus = new EventBus();

    bus.emit('clear:event', {});
    bus.emit('clear:event', {});
    bus.emit('clear:event', {});

    assertEquals(bus.getHistory().length, 3, 'Should have 3 events');

    bus.clearHistory();
    assertEquals(bus.getHistory().length, 0, 'History should be cleared');
  });

  // Test 15: Clear history for specific event
  await runTest('Clear History for Specific Event', () => {
    const bus = new EventBus();

    bus.emit('keep:event', {});
    bus.emit('remove:event', {});
    bus.emit('keep:event', {});
    bus.emit('remove:event', {});

    bus.clearHistory('remove:event');

    const history = bus.getHistory();
    assertEquals(history.length, 2, 'Should only have keep:event events');
  });

  // Test 16: Suspend and resume
  await runTest('Suspend and Resume', async () => {
    const bus = new EventBus();
    let count = 0;

    bus.on('suspend:event', () => count++);

    bus.suspend();
    bus.emit('suspend:event', {});
    bus.emit('suspend:event', {});
    bus.emit('suspend:event', {});

    assertTrue(bus.isSuspended(), 'Bus should be suspended');
    assertEquals(count, 0, 'No events should be emitted while suspended');
    assertEquals(bus.getPendingCount(), 3, 'Should have 3 pending events');

    await bus.resume();
    assertFalse(bus.isSuspended(), 'Bus should not be suspended after resume');
    assertEquals(count, 3, 'All pending events should be emitted');
    assertEquals(bus.getPendingCount(), 0, 'No pending events after resume');
  });

  // Test 17: Suspend and clear pending
  await runTest('Suspend and Clear Pending', async () => {
    const bus = new EventBus();
    let count = 0;

    bus.on('clear:event', () => count++);

    bus.suspend();
    bus.emit('clear:event', {});
    bus.emit('clear:event', {});

    await bus.resume(true);
    assertEquals(count, 0, 'Pending events should be cleared');
  });

  // Test 18: Statistics
  await runTest('Statistics', () => {
    const bus = new EventBus();

    bus.on('stats:event1', () => {});
    bus.on('stats:event1', () => {});
    bus.on('stats:event2', () => {});

    bus.emit('stats:event1', {});
    bus.emit('stats:event1', {});
    bus.emit('stats:event2', {});

    const stats = bus.getStats();
    assertEquals(stats.totalListeners, 3, 'Should have 3 total listeners');
    assertEquals(stats.totalEvents, 3, 'Should have 3 total events');
    assertEquals(stats.eventsByType['stats:event1'], 2, 'Should have 2 event1 events');
    assertEquals(stats.eventsByType['stats:event2'], 1, 'Should have 1 event2 events');
    assertEquals(stats.activeListeners['stats:event1'], 2, 'Should have 2 listeners for event1');
  });

  // Test 19: Get listener count
  await runTest('Get Listener Count', () => {
    const bus = new EventBus();

    bus.on('count:event', () => {});
    bus.on('count:event', () => {});
    bus.on('count:event', () => {});

    assertEquals(bus.getListenerCount('count:event'), 3, 'Should have 3 listeners');
    assertEquals(bus.getListenerCount('other:event'), 0, 'Should have 0 listeners for non-existent event');
  });

  // Test 20: Get event names
  await runTest('Get Event Names', () => {
    const bus = new EventBus();

    bus.on('event:a', () => {});
    bus.on('event:b', () => {});
    bus.on('event:c', () => {});

    const names = bus.getEventNames();
    assertEquals(names.length, 3, 'Should have 3 event names');
    assertTrue(names.includes('event:a'), 'Should include event:a');
    assertTrue(names.includes('event:b'), 'Should include event:b');
    assertTrue(names.includes('event:c'), 'Should include event:c');
  });

  // Test 21: Has listeners
  await runTest('Has Listeners', () => {
    const bus = new EventBus();

    bus.on('exists:event', () => {});

    assertTrue(bus.hasListeners('exists:event'), 'Should have listeners for exists:event');
    assertFalse(bus.hasListeners('notexists:event'), 'Should not have listeners for notexists:event');
  });

  // Test 22: Destroy
  await runTest('Destroy', () => {
    const bus = new EventBus();
    let count = 0;

    bus.on('destroy:event', () => count++);
    bus.emit('destroy:event', {});

    assertEquals(bus.getHistory().length, 1, 'Should have 1 event before destroy');

    bus.destroy();

    assertEquals(count, 1, 'No events should be emitted after destroy');
    assertEquals(bus.getHistory().length, 0, 'History should be cleared after destroy');
    assertEquals(bus.getStats().totalListeners, 0, 'Stats should be reset');
  });

  // Test 23: Async listeners
  await runTest('Async Listeners', async () => {
    const bus = new EventBus();
    const results: number[] = [];

    bus.on('async:event', async (data) => {
      await new Promise((resolve) => setTimeout(resolve, 10));
      results.push(data.value);
    });

    await bus.emit('async:event', { value: 1 });
    await bus.emit('async:event', { value: 2 });
    await bus.emit('async:event', { value: 3 });

    assertEquals(results, [1, 2, 3], 'Async listeners should complete in order');
  });

  // Test 24: Event data structure
  await runTest('Event Data Structure', async () => {
    const bus = new EventBus();
    let capturedSource: string | undefined = undefined;

    bus.on('structure:event', (data, eventName, source) => {
      capturedSource = source;
    });

    await bus.emit('structure:event', { payload: 'test' }, 'test-source');

    assertTrue(capturedSource === 'test-source', 'Event source should be passed to listener');
  });

  // Test 25: Typed event bus
  await runTest('Typed Event Bus', () => {
    interface TestEvents {
      'user:login': { username: string; id: number };
      'user:logout': { id: number };
    }

    const bus = createTypedEventBus<TestEvents>();
    let loginData: { username: string; id: number } | null = null;

    bus.on('user:login', (data) => {
      loginData = data;
    });

    bus.emit('user:login', { username: 'testuser', id: 123 });

    assertTrue(loginData !== null, 'Login data should be captured');
    assertEquals(loginData?.username, 'testuser', 'Username should be correct');
    assertEquals(loginData?.id, 123, 'ID should be correct');
  });

  // Test 26: Default bus (singleton)
  await runTest('Default Bus (Singleton)', () => {
    const bus1 = defaultBus;
    const bus2 = defaultBus;

    assertTrue(bus1 === bus2, 'Default bus should be singleton');
  });

  // Test 27: Edge case - empty event name
  await runTest('Edge Case: Empty Event Name', () => {
    const bus = new EventBus();
    let called = false;

    bus.on('', () => {
      called = true;
    });

    bus.emit('', {});

    assertTrue(called, 'Empty event name should work');
  });

  // Test 28: Edge case - special characters in event name
  await runTest('Edge Case: Special Characters', () => {
    const bus = new EventBus();
    let called = false;

    bus.on('event:with-dashes_and_underscores.123', () => {
      called = true;
    });

    bus.emit('event:with-dashes_and_underscores.123', {});

    assertTrue(called, 'Special characters in event name should work');
  });

  // Test 29: Edge case - emit before subscribe
  await runTest('Edge Case: Emit Before Subscribe', () => {
    const bus = new EventBus();
    let called = false;

    bus.emit('early:event', {});

    bus.on('early:event', () => {
      called = true;
    });

    assertFalse(called, 'Listener should not be called for events emitted before subscription');
  });

  // Test 30: Error handling in listeners
  await runTest('Edge Case: Error in Listener', () => {
    const bus = new EventBus();
    let secondCalled = false;

    bus.on('error:event', () => {
      throw new Error('Test error');
    });

    bus.on('error:event', () => {
      secondCalled = true;
    });

    bus.emit('error:event', {});

    assertTrue(secondCalled, 'Other listeners should still be called after error');
  });

  // Test 31: Mixed sync and async listeners
  await runTest('Mixed Sync and Async Listeners', async () => {
    const bus = new EventBus();
    const order: string[] = [];

    bus.on('mixed:event', () => {
      order.push('sync1');
    });

    bus.on('mixed:event', async () => {
      await new Promise((resolve) => setTimeout(resolve, 5));
      order.push('async1');
    });

    bus.on('mixed:event', () => {
      order.push('sync2');
    });

    await bus.emit('mixed:event', {});

    assertEquals(order.slice(0, 2), ['sync1', 'sync2'], 'Sync listeners should execute first');
    assertTrue(order.includes('async1'), 'Async listener should complete');
  });

  // Test 32: Once with priority
  await runTest('Once with Priority', () => {
    const bus = new EventBus();
    const order: number[] = [];

    bus.once('once:priority', () => order.push(1), { priority: 1 });
    bus.once('once:priority', () => order.push(2), { priority: 2 });

    bus.emit('once:priority', {});
    bus.emit('once:priority', {});

    assertEquals(order, [2, 1], 'First emit should execute in priority order');
    assertEquals(order.length, 2, 'Second emit should not execute (once listeners removed)');
  });

  // Test 33: Filter with once
  await runTest('Filter with Once', () => {
    const bus = new EventBus();
    let count = 0;

    bus.once('filter:once', () => count++, {
      filter: (data) => data.value > 5,
    });

    bus.emit('filter:once', { value: 3 });
    bus.emit('filter:once', { value: 10 });
    bus.emit('filter:once', { value: 15 });

    assertEquals(count, 1, 'Should only be called once when filter passes');
  });

  // Test 34: Complex wildcard patterns
  await runTest('Complex Wildcard Patterns', () => {
    const bus = new EventBus();
    const events: string[] = [];

    bus.on('a:*:c', (data, name) => events.push(name));

    bus.emit('a:b:c', {});
    bus.emit('a:x:c', {});
    bus.emit('a:b:d', {});
    bus.emit('a:b:x:c', {});

    assertEquals(events.length, 2, 'Should match a:*:c pattern correctly');
  });

  // Test 35: Unsubscribe specific callback
  await runTest('Unsubscribe Specific Callback', () => {
    const bus = new EventBus();
    let count1 = 0;
    let count2 = 0;

    const handler1 = () => count1++;
    const handler2 = () => count2++;

    bus.on('specific:event', handler1);
    bus.on('specific:event', handler2);

    bus.off('specific:event', handler1);

    bus.emit('specific:event', {});

    assertEquals(count1, 0, 'Handler1 should not be called');
    assertEquals(count2, 1, 'Handler2 should be called');
  });

  // Print summary
  console.log('\n' + '='.repeat(60));
  console.log('Test Summary');
  console.log('='.repeat(60));
  console.log(`Passed: ${passed}`);
  console.log(`Failed: ${failed}`);
  console.log(`Total:  ${passed + failed}`);

  if (failures.length > 0) {
    console.log('\nFailures:');
    failures.forEach((f, i) => console.log(`  ${i + 1}. ${f}`));
  }

  console.log('='.repeat(60));

  if (failed > 0) {
    console.error('\n❌ Some tests failed');
    process.exit(1);
  } else {
    console.log('\n✅ All tests passed!');
  }
}

// Run tests
runTests().catch(console.error);
