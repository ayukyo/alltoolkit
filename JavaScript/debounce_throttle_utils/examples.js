/**
 * Examples for Debounce and Throttle Utilities
 * Run with: node examples.js
 */

const {
  Debounce,
  Throttle,
  AsyncDebounce,
  RateLimitedQueue,
  debounce,
  throttle
} = require('./debounce_throttle.js');

// Helper
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

console.log('=== Debounce Examples ===\n');

// Example 1: Basic debounce usage
console.log('1. Basic Debounce (Search Input Simulation):');
{
  const searchQuery = debounce((query) => {
    console.log(`  Searching for: "${query}"`);
  }, 300);

  // Simulate rapid typing
  console.log('  User types: "h", "he", "hel", "hell", "hello"');
  searchQuery('h');
  searchQuery('he');
  searchQuery('hel');
  searchQuery('hell');
  searchQuery('hello');
  console.log('  (Waiting 300ms...)');
}

// Example 2: Leading edge debounce
console.log('\n2. Leading Edge Debounce (Button Click):');
{
  const handleClick = debounce(
    () => console.log('  Button clicked! Form submitted.'),
    1000,
    { leading: true, trailing: false }
  );

  console.log('  User clicks button rapidly 3 times...');
  handleClick();
  handleClick();
  handleClick();
  console.log('  (Only the first click is processed)');
}

// Example 3: Debounce with flush
console.log('\n3. Debounce with Flush (Auto-save):');
{
  let saveCount = 0;
  const autoSave = debounce(() => {
    saveCount++;
    console.log(`  Document saved! (Save #${saveCount})`);
  }, 2000);

  console.log('  User types...');
  autoSave();
  console.log('  User types more...');
  autoSave();
  
  console.log('  User clicks "Save" button (flush)...');
  autoSave.flush(); // Immediate save
}

// Example 4: Debounce with maxWait
console.log('\n4. Debounce with maxWait (Live Preview):');
{
  let previewCount = 0;
  const updatePreview = debounce(
    () => {
      previewCount++;
      console.log(`  Preview updated! (Update #${previewCount})`);
    },
    500,
    { maxWait: 2000 }
  );

  console.log('  User keeps typing (simulated every 400ms)...');
  // In real scenario, this would force an update every 2 seconds max
  console.log('  (maxWait ensures preview updates at least every 2s)');
}

console.log('\n=== Throttle Examples ===\n');

// Example 5: Basic throttle usage
console.log('5. Basic Throttle (Scroll Handler):');
{
  const handleScroll = throttle((scrollY) => {
    console.log(`  Scroll position: ${scrollY}px`);
  }, 100);

  console.log('  Simulating scroll events every 20ms...');
  let scrollY = 0;
  const scrollInterval = setInterval(() => {
    scrollY += 10;
    handleScroll(scrollY);
  }, 20);

  setTimeout(() => {
    clearInterval(scrollInterval);
  }, 250);
}

// Example 6: Throttle with trailing
console.log('\n6. Throttle with Trailing (Window Resize):');
{
  const handleResize = throttle(
    (width, height) => {
      console.log(`  Window resized to: ${width}x${height}`);
    },
    200,
    { leading: true, trailing: true }
  );

  console.log('  Simulating resize events...');
  handleResize(800, 600);
  handleResize(820, 620);
  handleResize(850, 650);
  console.log('  (Leading call immediate, trailing captures final size)');
}

// Example 7: Throttle no leading
console.log('\n7. Throttle without Leading (Delayed Processing):');
{
  const processData = throttle(
    (data) => console.log(`  Processing: ${data}`),
    500,
    { leading: false, trailing: true }
  );

  console.log('  Calling throttle with leading: false...');
  processData('item1');
  console.log('  (First call delayed, not immediate)');
}

console.log('\n=== Async Debounce Examples ===\n');

// Example 8: Async debounce for API calls
console.log('8. Async Debounce (API Call Simulation):');
async function asyncDebounceExample() {
  const fetchSuggestions = async (query) => {
    console.log(`  API called with: "${query}"`);
    await sleep(100); // Simulate API delay
    return [`suggestion1 for ${query}`, `suggestion2 for ${query}`];
  };

  const debouncedFetch = new AsyncDebounce(fetchSuggestions, { wait: 300 });

  // Simulate rapid typing
  console.log('  User types quickly...');
  const promise1 = debouncedFetch.call('h');
  const promise2 = debouncedFetch.call('he');
  const promise3 = debouncedFetch.call('hello');

  // All promises resolve to same result
  const results = await Promise.all([promise1, promise2, promise3]);
  console.log(`  Results: ${JSON.stringify(results[0])}`);
  console.log('  (Only one API call made for final query)');
}
asyncDebounceExample();

console.log('\n=== Rate Limited Queue Examples ===\n');

// Example 9: Rate limited queue for API calls
console.log('9. Rate Limited Queue (API Rate Limiting):');
async function queueExample() {
  const queue = new RateLimitedQueue(
    async (item) => {
      console.log(`  Processing item ${item}...`);
      await sleep(50); // Simulate processing
      return `processed-${item}`;
    },
    { interval: 100, autoStart: true }
  );

  console.log('  Adding items to queue...');
  queue.add(1).then(r => console.log(`    Got: ${r}`));
  queue.add(2).then(r => console.log(`    Got: ${r}`));
  queue.add(3).then(r => console.log(`    Got: ${r}`));
  
  console.log(`  Queue size: ${queue.size()}`);
  
  await sleep(500);
  console.log('  All items processed');
}
queueExample();

// Example 10: Debounce class usage
console.log('\n10. Debounce Class (Advanced Usage):');
{
  const debounced = new Debounce((msg) => {
    console.log(`  Executed: ${msg}`);
    return msg.toUpperCase();
  }, { wait: 100 });

  console.log('  Calling with "hello"...');
  debounced.call('hello');
  console.log(`  Pending: ${debounced.pending()}`);
  
  setTimeout(() => {
    console.log(`  Result: ${debounced.result}`);
    console.log(`  Invoke count: ${debounced.getInvokeCount()}`);
  }, 150);
}

// Wait for async examples to complete
setTimeout(() => {
  console.log('\n=== Practical Use Cases ===\n');
  
  // Example 11: Form validation
  console.log('11. Form Validation Pattern:');
  {
    const validateEmail = debounce((email) => {
      const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
      console.log(`  Email "${email}" is ${isValid ? 'valid ✓' : 'invalid ✗'}`);
    }, 300);

    validateEmail('test');
    validateEmail('test@');
    validateEmail('test@example');
    validateEmail('test@example.com');
    console.log('  (Only final valid email checked)');
  }

  // Example 12: Mouse movement tracking
  console.log('\n12. Mouse Movement Tracking:');
  {
    const trackMouse = throttle((x, y) => {
      console.log(`  Mouse at: (${x}, ${y})`);
    }, 100);

    console.log('  Simulating rapid mouse movements...');
    trackMouse(10, 20);
    trackMouse(50, 80);
    trackMouse(100, 150);
    trackMouse(150, 200);
    trackMouse(200, 250);
  }

  // Example 13: Batch processing with throttle
  console.log('\n13. Batch Processing Pattern:');
  {
    let batch = [];
    const processBatch = throttle(() => {
      if (batch.length > 0) {
        console.log(`  Processing batch of ${batch.length} items: [${batch.join(', ')}]`);
        batch = [];
      }
    }, 200);

    batch.push(1);
    batch.push(2);
    batch.push(3);
    processBatch();
    
    setTimeout(() => {
      batch.push(4);
      batch.push(5);
      processBatch();
    }, 250);
  }

  // Example 14: Game loop with throttle
  console.log('\n14. Game Loop Pattern:');
  {
    let position = 0;
    const render = throttle(() => {
      console.log(`  Rendering at position: ${position}`);
    }, 50);

    console.log('  Simulating game loop (60fps, but render throttled to 20fps)...');
    for (let i = 0; i < 10; i++) {
      position += 5;
      render();
    }
  }

  console.log('\n=== Examples Complete ===\n');
}, 1000);