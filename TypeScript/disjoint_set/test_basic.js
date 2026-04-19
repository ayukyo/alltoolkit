/**
 * Disjoint Set (Union-Find) Data Structure - JavaScript Implementation
 * 
 * Run with: node test_basic.js
 */

// ========== DisjointSet Class ==========
class DisjointSet {
  constructor(n) {
    this.parent = Array.from({ length: n }, (_, i) => i);
    this.rank = new Array(n).fill(0);
    this._count = n;
  }

  find(x) {
    if (x < 0 || x >= this.parent.length) return -1;
    if (this.parent[x] !== x) {
      this.parent[x] = this.find(this.parent[x]);
    }
    return this.parent[x];
  }

  union(x, y) {
    const rootX = this.find(x);
    const rootY = this.find(y);
    if (rootX === -1 || rootY === -1) return false;
    if (rootX === rootY) return false;

    if (this.rank[rootX] < this.rank[rootY]) {
      this.parent[rootX] = rootY;
    } else if (this.rank[rootX] > this.rank[rootY]) {
      this.parent[rootY] = rootX;
    } else {
      this.parent[rootY] = rootX;
      this.rank[rootX]++;
    }
    this._count--;
    return true;
  }

  connected(x, y) {
    return this.find(x) === this.find(y) && this.find(x) !== -1;
  }

  get count() { return this._count; }
  get size() { return this.parent.length; }

  setSize(x) {
    const root = this.find(x);
    if (root === -1) return 0;
    let size = 0;
    for (let i = 0; i < this.parent.length; i++) {
      if (this.find(i) === root) size++;
    }
    return size;
  }

  sets() {
    const sets = new Map();
    for (let i = 0; i < this.parent.length; i++) {
      const root = this.find(i);
      if (!sets.has(root)) sets.set(root, []);
      sets.get(root).push(i);
    }
    return sets;
  }

  reset() {
    for (let i = 0; i < this.parent.length; i++) {
      this.parent[i] = i;
      this.rank[i] = 0;
    }
    this._count = this.parent.length;
  }

  elements(x) {
    const root = this.find(x);
    if (root === -1) return [];
    const result = [];
    for (let i = 0; i < this.parent.length; i++) {
      if (this.find(i) === root) result.push(i);
    }
    return result;
  }
}

// ========== WeightedDisjointSet Class ==========
class WeightedDisjointSet {
  constructor(n) {
    this.parent = Array.from({ length: n }, (_, i) => i);
    this.size = new Array(n).fill(1);
    this._count = n;
  }

  find(x) {
    if (x < 0 || x >= this.parent.length) return -1;
    if (this.parent[x] !== x) {
      this.parent[x] = this.find(this.parent[x]);
    }
    return this.parent[x];
  }

  union(x, y) {
    const rootX = this.find(x);
    const rootY = this.find(y);
    if (rootX === -1 || rootY === -1) return false;
    if (rootX === rootY) return false;

    if (this.size[rootX] < this.size[rootY]) {
      this.parent[rootX] = rootY;
      this.size[rootY] += this.size[rootX];
    } else {
      this.parent[rootY] = rootX;
      this.size[rootX] += this.size[rootY];
    }
    this._count--;
    return true;
  }

  connected(x, y) {
    return this.find(x) === this.find(y) && this.find(x) !== -1;
  }

  setSize(x) {
    const root = this.find(x);
    return root === -1 ? 0 : this.size[root];
  }

  get count() { return this._count; }
}

// ========== Utility Functions ==========
function countComponents(n, edges) {
  const ds = new DisjointSet(n);
  for (const [u, v] of edges) ds.union(u, v);
  return ds.count;
}

function findRedundantConnection(n, edges) {
  const ds = new DisjointSet(n + 1);
  for (const [u, v] of edges) {
    if (ds.connected(u, v)) return [u, v];
    ds.union(u, v);
  }
  return null;
}

function isBipartite(graph) {
  const n = graph.length;
  const ds = new DisjointSet(2 * n);
  for (let i = 0; i < n; i++) {
    for (const neighbor of graph[i]) {
      if (ds.connected(i, neighbor)) return false;
      ds.union(i, neighbor + n);
      ds.union(i + n, neighbor);
    }
  }
  return true;
}

function mstKruskal(n, edges) {
  const sorted = [...edges].sort((a, b) => a.weight - b.weight);
  const ds = new DisjointSet(n);
  let totalWeight = 0;
  const mstEdges = [];

  for (const edge of sorted) {
    if (ds.union(edge.from, edge.to)) {
      totalWeight += edge.weight;
      mstEdges.push(edge);
      if (mstEdges.length === n - 1) break;
    }
  }
  return { totalWeight, mstEdges };
}

// ========== Test Runner ==========
let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (e) {
    console.log(`❌ ${name}: ${e.message}`);
    failed++;
  }
}

function assertEqual(actual, expected, msg = '') {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`${msg} Expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

function assertTrue(condition, msg = '') {
  if (!condition) throw new Error(`${msg} Expected true, got false`);
}

function assertFalse(condition, msg = '') {
  if (condition) throw new Error(`${msg} Expected false, got true`);
}

// ========== Tests ==========
console.log('=== Disjoint Set Tests ===\n');

test('Basic creation', () => {
  const ds = new DisjointSet(5);
  assertEqual(ds.size, 5);
  assertEqual(ds.count, 5);
});

test('Find returns element itself initially', () => {
  const ds = new DisjointSet(5);
  for (let i = 0; i < 5; i++) {
    assertEqual(ds.find(i), i);
  }
  assertEqual(ds.find(-1), -1);
  assertEqual(ds.find(100), -1);
});

test('Union and connected', () => {
  const ds = new DisjointSet(5);
  assertTrue(ds.union(0, 1));
  assertEqual(ds.count, 4);
  assertTrue(ds.connected(0, 1));
  assertFalse(ds.union(0, 1)); // already connected
  assertTrue(ds.union(1, 2));
  assertTrue(ds.connected(0, 2)); // transitive
  assertFalse(ds.connected(0, 3));
});

test('setSize', () => {
  const ds = new DisjointSet(5);
  assertEqual(ds.setSize(0), 1);
  ds.union(0, 1);
  ds.union(0, 2);
  assertEqual(ds.setSize(0), 3);
  assertEqual(ds.setSize(3), 1);
});

test('sets', () => {
  const ds = new DisjointSet(5);
  ds.union(0, 1);
  ds.union(2, 3);
  const sets = ds.sets();
  assertEqual(sets.size, 3);
});

test('elements', () => {
  const ds = new DisjointSet(5);
  ds.union(0, 1);
  ds.union(0, 2);
  const elements = ds.elements(0);
  assertEqual(elements.length, 3);
  assertTrue(elements.includes(0));
  assertTrue(elements.includes(1));
  assertTrue(elements.includes(2));
});

test('reset', () => {
  const ds = new DisjointSet(5);
  ds.union(0, 1);
  ds.union(2, 3);
  ds.reset();
  assertEqual(ds.count, 5);
  assertFalse(ds.connected(0, 1));
});

test('WeightedDisjointSet', () => {
  const wds = new WeightedDisjointSet(5);
  assertEqual(wds.setSize(0), 1);
  wds.union(0, 1);
  wds.union(0, 2);
  assertEqual(wds.setSize(0), 3);
  assertEqual(wds.count, 3);
});

test('countComponents - two components', () => {
  const edges = [[0, 1], [1, 2], [3, 4]];
  assertEqual(countComponents(5, edges), 2);
});

test('countComponents - all connected', () => {
  const edges = [[0, 1], [1, 2], [2, 3], [3, 4]];
  assertEqual(countComponents(5, edges), 1);
});

test('findRedundantConnection - finds cycle', () => {
  const edges = [[1, 2], [1, 3], [2, 3]];
  assertEqual(findRedundantConnection(3, edges), [2, 3]);
});

test('findRedundantConnection - no cycle', () => {
  const edges = [[0, 1], [1, 2]];
  assertEqual(findRedundantConnection(3, edges), null);
});

test('isBipartite - square is bipartite', () => {
  const graph = [[1, 3], [0, 2], [1, 3], [0, 2]];
  assertTrue(isBipartite(graph));
});

test('isBipartite - triangle is not bipartite', () => {
  const graph = [[1, 2], [0, 2], [0, 1]];
  assertFalse(isBipartite(graph));
});

test('mstKruskal - computes MST correctly', () => {
  // Graph: 4 nodes, MST should have weight 1+1+2 = 4
  // Edges sorted by weight: 0-2(1), 2-3(1), 0-1(2), 1-3(3)
  const edges = [
    { from: 0, to: 1, weight: 2 },
    { from: 0, to: 2, weight: 1 },
    { from: 1, to: 3, weight: 3 },
    { from: 2, to: 3, weight: 1 },
  ];
  const { totalWeight, mstEdges } = mstKruskal(4, edges);
  assertEqual(totalWeight, 4); // 1 + 1 + 2 = 4
  assertEqual(mstEdges.length, 3);
});

test('path compression works', () => {
  const ds = new DisjointSet(10);
  for (let i = 0; i < 9; i++) ds.union(i, i + 1);
  const root = ds.find(0);
  for (let i = 1; i < 10; i++) {
    assertEqual(ds.find(i), root);
  }
});

test('large scale operations', () => {
  const n = 1000;
  const ds = new DisjointSet(n);
  for (let i = 0; i < n - 1; i += 2) ds.union(i, i + 1);
  assertEqual(ds.count, n / 2);
  for (let i = 0; i < n - 1; i += 2) {
    assertTrue(ds.connected(i, i + 1));
  }
});

// Summary
console.log('\n' + '='.repeat(40));
console.log(`Tests: ${passed} passed, ${failed} failed, ${passed + failed} total`);

if (failed > 0) {
  process.exit(1);
}