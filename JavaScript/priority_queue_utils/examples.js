/**
 * Examples for Priority Queue Utils
 * 
 * Run with: node examples.js
 */

const { PriorityQueue, IndexedPriorityQueue } = require('./mod.js');

console.log('=== Priority Queue Utils Examples ===\n');

// Example 1: Basic Min-Heap Usage
console.log('--- Example 1: Basic Min-Heap ---');
const minHeap = new PriorityQueue();
minHeap.enqueue(5);
minHeap.enqueue(1);
minHeap.enqueue(3);
minHeap.enqueue(2);
minHeap.enqueue(4);

console.log('Enqueued: 5, 1, 3, 2, 4');
console.log('Dequeue order:', minHeap.toSortedArray());
// Output: [1, 2, 3, 4, 5]

// Example 2: Max-Heap Usage
console.log('\n--- Example 2: Max-Heap ---');
const maxHeap = PriorityQueue.maxHeap([5, 1, 3, 2, 4]);
console.log('Max-heap order:', maxHeap.toSortedArray());
// Output: [5, 4, 3, 2, 1]

// Example 3: Task Scheduler
console.log('\n--- Example 3: Task Scheduler ---');
const tasks = new PriorityQueue((a, b) => a.priority - b.priority);

tasks.enqueue({ name: 'Write tests', priority: 2 });
tasks.enqueue({ name: 'Fix critical bug', priority: 1 });
tasks.enqueue({ name: 'Refactor code', priority: 3 });
tasks.enqueue({ name: 'Review PR', priority: 2 });

console.log('Task execution order:');
while (!tasks.isEmpty()) {
  const task = tasks.dequeue();
  console.log(`  Priority ${task.priority}: ${task.name}`);
}

// Example 4: Dijkstra's Algorithm Helper
console.log('\n--- Example 4: Dijkstra\'s Shortest Path ---');

// Graph: adjacency list
const graph = {
  'A': { 'B': 4, 'C': 2 },
  'B': { 'A': 4, 'C': 1, 'D': 5 },
  'C': { 'A': 2, 'B': 1, 'D': 8, 'E': 10 },
  'D': { 'B': 5, 'C': 8, 'E': 2, 'F': 6 },
  'E': { 'C': 10, 'D': 2, 'F': 3 },
  'F': { 'D': 6, 'E': 3 }
};

function dijkstra(graph, start) {
  const distances = {};
  const pq = new PriorityQueue((a, b) => a.distance - b.distance);
  
  // Initialize
  for (const node of Object.keys(graph)) {
    distances[node] = Infinity;
  }
  distances[start] = 0;
  pq.enqueue({ node: start, distance: 0 });
  
  while (!pq.isEmpty()) {
    const { node: current, distance: dist } = pq.dequeue();
    
    if (dist > distances[current]) continue;
    
    for (const [neighbor, weight] of Object.entries(graph[current])) {
      const newDist = distances[current] + weight;
      if (newDist < distances[neighbor]) {
        distances[neighbor] = newDist;
        pq.enqueue({ node: neighbor, distance: newDist });
      }
    }
  }
  
  return distances;
}

const distances = dijkstra(graph, 'A');
console.log('Shortest distances from A:');
for (const [node, dist] of Object.entries(distances)) {
  console.log(`  ${node}: ${dist}`);
}

// Example 5: Merge K Sorted Arrays
console.log('\n--- Example 5: Merge K Sorted Arrays ---');
function mergeKSortedArrays(arrays) {
  const result = [];
  const pq = new PriorityQueue((a, b) => a.value - b.value);
  
  // Add first element from each array
  arrays.forEach((arr, arrIndex) => {
    if (arr.length > 0) {
      pq.enqueue({
        value: arr[0],
        arrIndex,
        elemIndex: 0
      });
    }
  });
  
  while (!pq.isEmpty()) {
    const { value, arrIndex, elemIndex } = pq.dequeue();
    result.push(value);
    
    // Add next element from the same array
    if (elemIndex + 1 < arrays[arrIndex].length) {
      pq.enqueue({
        value: arrays[arrIndex][elemIndex + 1],
        arrIndex,
        elemIndex: elemIndex + 1
      });
    }
  }
  
  return result;
}

const arrays = [
  [1, 4, 7, 10],
  [2, 5, 8],
  [0, 3, 6, 9, 12]
];
console.log('Input arrays:', arrays);
console.log('Merged:', mergeKSortedArrays(arrays));

// Example 6: Indexed Priority Queue - Dynamic Priority Updates
console.log('\n--- Example 6: Dynamic Priority Updates ---');
const ipq = new IndexedPriorityQueue();

ipq.set('user1', 100, { name: 'Alice' });
ipq.set('user2', 50, { name: 'Bob' });
ipq.set('user3', 75, { name: 'Charlie' });

console.log('Initial order:');
console.log('  1:', ipq.dequeue()); // user2 (priority 50)
console.log('  2:', ipq.dequeue()); // user3 (priority 75)

// Remaining: user1 with priority 100
console.log('  Remaining priority:', ipq.getPriority('user1'));

// Example 7: Streaming Data Processing
console.log('\n--- Example 7: Streaming Median ---');
class MedianFinder {
  constructor() {
    this.maxHeap = new PriorityQueue((a, b) => b - a); // Lower half
    this.minHeap = new PriorityQueue((a, b) => a - b); // Upper half
  }
  
  addNum(num) {
    if (this.maxHeap.isEmpty() || num <= this.maxHeap.peek()) {
      this.maxHeap.enqueue(num);
    } else {
      this.minHeap.enqueue(num);
    }
    
    // Balance heaps
    if (this.maxHeap.size > this.minHeap.size + 1) {
      this.minHeap.enqueue(this.maxHeap.dequeue());
    } else if (this.minHeap.size > this.maxHeap.size) {
      this.maxHeap.enqueue(this.minHeap.dequeue());
    }
  }
  
  getMedian() {
    if (this.maxHeap.isEmpty()) return null;
    
    if (this.maxHeap.size === this.minHeap.size) {
      return (this.maxHeap.peek() + this.minHeap.peek()) / 2;
    }
    return this.maxHeap.peek();
  }
}

const medianFinder = new MedianFinder();
[1, 2, 3, 4, 5, 6, 7, 8].forEach(n => {
  medianFinder.addNum(n);
  console.log(`After adding ${n}, median = ${medianFinder.getMedian()}`);
});

// Example 8: Huffman Coding Helper
console.log('\n--- Example 8: Huffman Coding Tree ---');
class HuffmanNode {
  constructor(char, freq) {
    this.char = char;
    this.freq = freq;
    this.left = null;
    this.right = null;
  }
}

function buildHuffmanTree(charFreqs) {
  const pq = new PriorityQueue((a, b) => a.freq - b.freq);
  
  // Create leaf nodes
  for (const [char, freq] of Object.entries(charFreqs)) {
    pq.enqueue(new HuffmanNode(char, freq));
  }
  
  // Build tree
  while (pq.size > 1) {
    const left = pq.dequeue();
    const right = pq.dequeue();
    
    const parent = new HuffmanNode(null, left.freq + right.freq);
    parent.left = left;
    parent.right = right;
    
    pq.enqueue(parent);
  }
  
  return pq.dequeue();
}

function generateCodes(node, prefix = '', codes = {}) {
  if (node.char !== null) {
    codes[node.char] = prefix || '0';
    return codes;
  }
  
  generateCodes(node.left, prefix + '0', codes);
  generateCodes(node.right, prefix + '1', codes);
  
  return codes;
}

const frequencies = { 'a': 5, 'b': 9, 'c': 12, 'd': 13, 'e': 16, 'f': 45 };
const huffmanTree = buildHuffmanTree(frequencies);
const huffmanCodes = generateCodes(huffmanTree);

console.log('Huffman Codes:');
for (const [char, code] of Object.entries(huffmanCodes)) {
  console.log(`  ${char}: ${code}`);
}

// Example 9: Event Simulation
console.log('\n--- Example 9: Discrete Event Simulation ---');
class EventSimulation {
  constructor() {
    this.events = new PriorityQueue((a, b) => a.time - b.time);
    this.currentTime = 0;
  }
  
  schedule(time, name, handler) {
    this.events.enqueue({ time, name, handler });
  }
  
  run(maxEvents = 100) {
    let count = 0;
    while (!this.events.isEmpty() && count < maxEvents) {
      const event = this.events.dequeue();
      this.currentTime = event.time;
      console.log(`Time ${this.currentTime}: ${event.name}`);
      event.handler(this);
      count++;
    }
  }
}

const sim = new EventSimulation();
sim.schedule(0, 'Start', (s) => {
  s.schedule(5, 'Process A', () => {});
  s.schedule(2, 'Process B', () => {});
});
sim.schedule(10, 'End', () => {});

console.log('Event simulation:');
sim.run();

console.log('\n=== All Examples Complete ===');