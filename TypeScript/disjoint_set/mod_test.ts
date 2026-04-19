import {
  DisjointSet,
  WeightedDisjointSet,
  countComponents,
  findRedundantConnection,
  isBipartite,
  mstKruskal,
  DisjointSetGeneric,
  Edge,
} from './mod.ts';
import { assertEquals, assert } from 'https://deno.land/std@0.208.0/assert/mod.ts';

// ========== DisjointSet Tests ==========

Deno.test('DisjointSet - basic creation', () => {
  const ds = new DisjointSet(5);
  assertEquals(ds.size, 5);
  assertEquals(ds.count, 5);
});

Deno.test('DisjointSet - find returns element itself initially', () => {
  const ds = new DisjointSet(5);
  for (let i = 0; i < 5; i++) {
    assertEquals(ds.find(i), i);
  }
  assertEquals(ds.find(-1), -1);
  assertEquals(ds.find(100), -1);
});

Deno.test('DisjointSet - union and connected', () => {
  const ds = new DisjointSet(5);
  
  assert(ds.union(0, 1));
  assertEquals(ds.count, 4);
  assert(ds.connected(0, 1));
  
  assert(!ds.union(0, 1)); // already connected
  
  assert(ds.union(1, 2));
  assert(ds.connected(0, 2)); // transitive
  assert(!ds.connected(0, 3));
});

Deno.test('DisjointSet - setSize', () => {
  const ds = new DisjointSet(5);
  assertEquals(ds.setSize(0), 1);
  
  ds.union(0, 1);
  ds.union(0, 2);
  
  assertEquals(ds.setSize(0), 3);
  assertEquals(ds.setSize(3), 1);
});

Deno.test('DisjointSet - sets', () => {
  const ds = new DisjointSet(5);
  ds.union(0, 1);
  ds.union(2, 3);
  
  const sets = ds.sets();
  assertEquals(sets.size, 3);
});

Deno.test('DisjointSet - elements', () => {
  const ds = new DisjointSet(5);
  ds.union(0, 1);
  ds.union(0, 2);
  
  const elements = ds.elements(0);
  assertEquals(elements.length, 3);
  assert(elements.includes(0));
  assert(elements.includes(1));
  assert(elements.includes(2));
});

Deno.test('DisjointSet - reset', () => {
  const ds = new DisjointSet(5);
  ds.union(0, 1);
  ds.union(2, 3);
  
  ds.reset();
  
  assertEquals(ds.count, 5);
  assert(!ds.connected(0, 1));
});

// ========== WeightedDisjointSet Tests ==========

Deno.test('WeightedDisjointSet - basic operations', () => {
  const wds = new WeightedDisjointSet(5);
  assertEquals(wds.setSize(0), 1);
  
  wds.union(0, 1);
  wds.union(0, 2);
  
  assertEquals(wds.setSize(0), 3);
  assertEquals(wds.count, 3);
});

// ========== Utility Functions Tests ==========

Deno.test('countComponents - two components', () => {
  const edges: [number, number][] = [[0, 1], [1, 2], [3, 4]];
  assertEquals(countComponents(5, edges), 2);
});

Deno.test('countComponents - all connected', () => {
  const edges: [number, number][] = [[0, 1], [1, 2], [2, 3], [3, 4]];
  assertEquals(countComponents(5, edges), 1);
});

Deno.test('findRedundantConnection - finds cycle', () => {
  const edges: [number, number][] = [
    [1, 2],
    [1, 3],
    [2, 3], // creates cycle
  ];
  
  const result = findRedundantConnection(3, edges);
  assertEquals(result, [2, 3]);
});

Deno.test('findRedundantConnection - no cycle', () => {
  const edges: [number, number][] = [[0, 1], [1, 2]];
  assertEquals(findRedundantConnection(3, edges), null);
});

Deno.test('isBipartite - square graph is bipartite', () => {
  const graph: number[][] = [
    [1, 3], // 0 connects to 1, 3
    [0, 2], // 1 connects to 0, 2
    [1, 3], // 2 connects to 1, 3
    [0, 2], // 3 connects to 0, 2
  ];
  
  assert(isBipartite(graph));
});

Deno.test('isBipartite - triangle is not bipartite', () => {
  const graph: number[][] = [
    [1, 2],
    [0, 2],
    [0, 1],
  ];
  
  assert(!isBipartite(graph));
});

Deno.test('mstKruskal - computes MST correctly', () => {
  // Graph: 4 nodes, MST weight = 1+1+2 = 4
  const edges: Edge[] = [
    { from: 0, to: 1, weight: 4 },
    { from: 0, to: 2, weight: 1 },
    { from: 1, to: 3, weight: 2 },
    { from: 2, to: 3, weight: 1 },
  ];
  
  const { totalWeight, mstEdges } = mstKruskal(4, edges);
  
  assertEquals(totalWeight, 4);
  assertEquals(mstEdges.length, 3);
});

// ========== DisjointSetGeneric Tests ==========

Deno.test('DisjointSetGeneric - string elements', () => {
  const ds = new DisjointSetGeneric<string>();
  
  ds.add('a');
  ds.add('b');
  ds.add('c');
  
  assertEquals(ds.count, 3);
  
  assert(ds.union('a', 'b'));
  assert(ds.connected('a', 'b'));
  assert(!ds.connected('a', 'c'));
  
  const elements = ds.elements('a');
  assertEquals(elements.length, 2);
  assert(elements.includes('a'));
  assert(elements.includes('b'));
});

Deno.test('DisjointSetGeneric - number elements', () => {
  const ds = new DisjointSetGeneric([1, 2, 3, 4, 5]);
  
  assertEquals(ds.count, 5);
  
  ds.union(1, 2);
  ds.union(3, 4);
  ds.union(1, 3);
  
  assert(ds.connected(1, 4));
  assert(!ds.connected(1, 5));
  assertEquals(ds.count, 2);
});

Deno.test('DisjointSetGeneric - object elements', () => {
  const obj1 = { id: 1 };
  const obj2 = { id: 2 };
  const obj3 = { id: 3 };
  
  const ds = new DisjointSetGeneric<typeof obj1>();
  
  ds.add(obj1);
  ds.add(obj2);
  ds.add(obj3);
  
  ds.union(obj1, obj2);
  
  assert(ds.connected(obj1, obj2));
  assert(!ds.connected(obj1, obj3));
});

// ========== Path Compression Tests ==========

Deno.test('DisjointSet - path compression works', () => {
  const ds = new DisjointSet(10);
  
  // Create a long chain
  for (let i = 0; i < 9; i++) {
    ds.union(i, i + 1);
  }
  
  // After path compression, all should have the same root
  const root = ds.find(0);
  for (let i = 1; i < 10; i++) {
    assertEquals(ds.find(i), root);
  }
});

// ========== Performance Tests ==========

Deno.test('DisjointSet - large scale operations', () => {
  const n = 1000;
  const ds = new DisjointSet(n);
  
  // Union adjacent pairs
  for (let i = 0; i < n - 1; i += 2) {
    ds.union(i, i + 1);
  }
  
  assertEquals(ds.count, n / 2);
  
  // Check each pair
  for (let i = 0; i < n - 1; i += 2) {
    assert(ds.connected(i, i + 1));
  }
});