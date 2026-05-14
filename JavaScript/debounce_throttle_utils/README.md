# Debounce & Throttle Utilities

Zero-dependency debounce and throttle implementations for Node.js and browsers.

## Features

- **Debounce** - Delay execution until after a pause in calls
- **Throttle** - Limit execution to once per time period
- **Leading/Trailing options** - Control when execution happens
- **Cancelable & Flushable** - Cancel pending or execute immediately
- **Async Support** - Special async debounce for promises
- **Rate Limited Queue** - Process items with rate limiting
- **Zero Dependencies** - Works in Node.js and browsers

## Installation

```javascript
// Copy debounce_throttle.js to your project
const { debounce, throttle, Debounce, Throttle } = require('./debounce_throttle.js');
```

## Quick Start

### Debounce

Delays execution until after a pause in calls. Multiple calls reset the timer.

```javascript
const { debounce } = require('./debounce_throttle.js');

// Basic usage - only execute after 300ms pause
const searchQuery = debounce((query) => {
  console.log('Searching:', query);
}, 300);

// User types quickly
searchQuery('h');
searchQuery('he');
searchQuery('hello'); // Only this executes (after 300ms)
```

### Throttle

Limits execution to once per time period.

```javascript
const { throttle } = require('./throttle');

// Execute at most once every 100ms
const handleScroll = throttle((scrollY) => {
  console.log('Scroll position:', scrollY);
}, 100);

// Rapid scroll events
window.addEventListener('scroll', () => {
  handleScroll(window.scrollY);
});
```

## API Reference

### debounce(fn, wait, options?)

Creates a debounced function.

| Parameter | Type | Description |
|-----------|------|-------------|
| `fn` | Function | Function to debounce |
| `wait` | number | Delay in milliseconds |
| `options.leading` | boolean | Execute on leading edge (default: false) |
| `options.trailing` | boolean | Execute on trailing edge (default: true) |
| `options.maxWait` | number | Maximum wait before forcing execution |

**Returns:** Debounced function with `.cancel()`, `.flush()`, `.pending()` methods.

```javascript
const debounced = debounce(fn, 300);

debounced();           // Call the function
debounced.cancel();    // Cancel pending execution
debounced.flush();     // Execute immediately if pending
debounced.pending();   // Check if execution is pending
```

### throttle(fn, limit, options?)

Creates a throttled function.

| Parameter | Type | Description |
|-----------|------|-------------|
| `fn` | Function | Function to throttle |
| `limit` | number | Minimum time between calls (ms) |
| `options.leading` | boolean | Execute on leading edge (default: true) |
| `options.trailing` | boolean | Execute on trailing edge (default: true) |

**Returns:** Throttled function with `.cancel()`, `.flush()`, `.pending()` methods.

```javascript
const throttled = throttle(fn, 100);

throttled();           // Call the function
throttled.cancel();    // Cancel pending trailing call
throttled.flush();     // Execute pending trailing call immediately
throttled.pending();   // Check if there's a pending call
```

### Debounce Class

For advanced use cases with more control.

```javascript
const { Debounce } = require('./debounce_throttle.js');

const debounced = new Debounce(fn, {
  wait: 300,
  leading: false,
  trailing: true,
  maxWait: 2000
});

debounced.call(...args);        // Invoke debounced
debounced.cancel();             // Cancel pending
debounced.flush();              // Execute immediately
debounced.pending();            // Check pending state
debounced.result;               // Last result
debounced.getInvokeCount();     // Number of invocations
```

### Throttle Class

For advanced use cases with more control.

```javascript
const { Throttle } = require('./debounce_throttle.js');

const throttled = new Throttle(fn, {
  limit: 100,
  leading: true,
  trailing: true
});

throttled.call(...args);        // Invoke throttled
throttled.cancel();             // Cancel pending
throttled.flush();              // Execute immediately
throttled.pending();            // Check pending state
throttled.result;               // Last result
throttled.getInvokeCount();     // Number of invocations
```

### AsyncDebounce Class

For async functions with proper promise handling.

```javascript
const { AsyncDebounce } = require('./debounce_throttle.js');

const debouncedFetch = new AsyncDebounce(
  async (query) => {
    const response = await fetch(`/api/search?q=${query}`);
    return response.json();
  },
  { wait: 300 }
);

// All concurrent calls share the same promise
const result1 = debouncedFetch.call('hello');
const result2 = debouncedFetch.call('hello');
const result3 = debouncedFetch.call('world');

// result1 and result2 resolve to same value
// result3 is from the last call
const data = await result3;
```

### RateLimitedQueue Class

Process items with rate limiting.

```javascript
const { RateLimitedQueue } = require('./debounce_throttle.js');

const queue = new RateLimitedQueue(
  async (item) => {
    // Process item (e.g., API call)
    return await api.process(item);
  },
  { 
    interval: 100,    // Min time between calls
    concurrency: 3,   // Max concurrent
    autoStart: true   // Auto-process on add
  }
);

// Add items to queue
const result1 = queue.add(item1);
const result2 = queue.add(item2);

// Wait for results
const [r1, r2] = await Promise.all([result1, result2]);

// Queue management
queue.size();      // Items waiting
queue.isEmpty();   // Check if empty
queue.clear();     // Clear queue
```

## Common Use Cases

### Search Input

```javascript
const searchInput = document.querySelector('#search');
const search = debounce(async (query) => {
  const results = await fetch(`/api/search?q=${query}`);
  displayResults(results);
}, 300);

searchInput.addEventListener('input', (e) => {
  search(e.target.value);
});
```

### Button Click Prevention

```javascript
const submitForm = debounce(
  async (data) => {
    await api.submit(data);
    showToast('Saved!');
  },
  1000,
  { leading: true, trailing: false }
);

// Only first click in each 1s window is processed
saveButton.addEventListener('click', () => submitForm(formData));
```

### Scroll Handler

```javascript
const handleScroll = throttle(() => {
  updateUI(window.scrollY);
  checkLazyLoad();
}, 100);

window.addEventListener('scroll', handleScroll);
```

### Window Resize

```javascript
const handleResize = throttle(
  (width, height) => {
    recalculateLayout(width, height);
  },
  200,
  { leading: true, trailing: true }
);

window.addEventListener('resize', () => {
  handleResize(window.innerWidth, window.innerHeight);
});
```

### API Rate Limiting

```javascript
const apiQueue = new RateLimitedQueue(
  async (endpoint) => {
    return fetch(endpoint).then(r => r.json());
  },
  { interval: 100 }  // Max 10 requests per second
);

// Enqueue API calls
const results = await Promise.all([
  apiQueue.add('/api/users'),
  apiQueue.add('/api/posts'),
  apiQueue.add('/api/comments')
]);
```

### Auto-save with Max Wait

```javascript
const autoSave = debounce(
  (content) => saveToServer(content),
  2000,
  { maxWait: 10000 }  // Save at least every 10s
);

editor.addEventListener('change', () => {
  autoSave(editor.content);
});

// Manual save
saveButton.addEventListener('click', () => autoSave.flush());
```

## Running Tests

```bash
node debounce_throttle.test.js
```

## Running Examples

```bash
node examples.js
```

## License

MIT