/**
 * AllToolkit - TypeScript Event Bus
 * Basic Usage Examples
 *
 * This file demonstrates the fundamental usage of the EventBus class.
 */

import { EventBus } from '../mod.ts';

console.log('='.repeat(50));
console.log('EventBus Basic Usage Examples');
console.log('='.repeat(50));

// Create a new EventBus instance
const bus = new EventBus();

// Example 1: Basic subscription and emission
console.log('\n1. Basic Subscription and Emission');
console.log('-'.repeat(40));

bus.on('greeting', (data) => {
  console.log(`   Received greeting: ${data.message}`);
});

bus.emit('greeting', { message: 'Hello, World!' });

// Example 2: Multiple listeners for the same event
console.log('\n2. Multiple Listeners');
console.log('-'.repeat(40));

bus.on('multi', () => console.log('   Listener 1 called'));
bus.on('multi', () => console.log('   Listener 2 called'));
bus.on('multi', () => console.log('   Listener 3 called'));

bus.emit('multi', {});

// Example 3: Once listener (auto-remove after first trigger)
console.log('\n3. Once Listener');
console.log('-'.repeat(40));

bus.once('once-event', () => {
  console.log('   This will only print once');
});

bus.emit('once-event', {});  // Will print
bus.emit('once-event', {});  // Won't print
bus.emit('once-event', {});  // Won't print

// Example 4: Unsubscribe
console.log('\n4. Unsubscribe');
console.log('-'.repeat(40));

let count = 0;
const handler = () => {
  count++;
  console.log(`   Handler called (count: ${count})`);
};

const unsubscribe = bus.on('unsubscribe-test', handler);

bus.emit('unsubscribe-test', {});  // count = 1
unsubscribe();                      // Remove listener
bus.emit('unsubscribe-test', {});  // count still = 1

console.log(`   Final count: ${count}`);

// Example 5: Wildcard matching
console.log('\n5. Wildcard Matching');
console.log('-'.repeat(40));

bus.on('user:*', (data, eventName) => {
  console.log(`   User event: ${eventName}`);
});

bus.emit('user:login', { user: 'Alice' });
bus.emit('user:logout', { user: 'Bob' });
bus.emit('user:register', { user: 'Charlie' });
bus.emit('admin:login', { user: 'Dave' });  // Won't match

// Example 6: Multi-level wildcard
console.log('\n6. Multi-level Wildcard (**)');
console.log('-'.repeat(40));

bus.on('app:**', (data, eventName) => {
  console.log(`   App event: ${eventName}`);
});

bus.emit('app:start', {});
bus.emit('app:user:login', {});
bus.emit('app:user:profile:update', {});
bus.emit('app:system:db:connect', {});

// Example 7: Priority execution
console.log('\n7. Priority Execution');
console.log('-'.repeat(40));

bus.on('priority', () => console.log('   Low priority (1)'), { priority: 1 });
bus.on('priority', () => console.log('   High priority (10)'), { priority: 10 });
bus.on('priority', () => console.log('   Medium priority (5)'), { priority: 5 });

bus.emit('priority', {});
console.log('   (Listeners execute in priority order: 10 → 5 → 1)');

// Example 8: Event filtering
console.log('\n8. Event Filtering');
console.log('-'.repeat(40));

bus.on('filtered', (data) => {
  console.log(`   Processed value: ${data.value}`);
}, {
  filter: (data) => data.value > 10
});

bus.emit('filtered', { value: 5 });   // Filtered out
bus.emit('filtered', { value: 15 });  // Processed
bus.emit('filtered', { value: 25 });  // Processed
bus.emit('filtered', { value: 8 });   // Filtered out

// Example 9: Event history
console.log('\n9. Event History');
console.log('-'.repeat(40));

const historyBus = new EventBus(10);

for (let i = 1; i <= 15; i++) {
  historyBus.emit('history', { index: i });
}

const history = historyBus.getHistory(5);
console.log(`   Last 5 events from history:`);
history.forEach(event => {
  console.log(`   - Event ${event.data.index} at ${new Date(event.timestamp).toLocaleTimeString()}`);
});

// Example 10: Suspend and resume
console.log('\n10. Suspend and Resume');
console.log('-'.repeat(40));

const suspendBus = new EventBus();
let suspendCount = 0;

suspendBus.on('suspend-test', () => {
  suspendCount++;
  console.log(`   Event processed (total: ${suspendCount})`);
});

console.log('   Suspending event bus...');
suspendBus.suspend();

console.log('   Emitting 3 events (queued)...');
suspendBus.emit('suspend-test', {});
suspendBus.emit('suspend-test', {});
suspendBus.emit('suspend-test', {});

console.log(`   Pending events: ${suspendBus.getPendingCount()}`);
console.log(`   Processed so far: ${suspendCount}`);

console.log('   Resuming event bus...');
suspendBus.resume().then(() => {
  console.log(`   Total processed after resume: ${suspendCount}`);
  
  // Print summary
  console.log('\n' + '='.repeat(50));
  console.log('Examples completed!');
  console.log('='.repeat(50));
});
