/**
 * Disjoint Set (Union-Find) Examples
 * 
 * Run with: deno run examples/basic_usage.ts
 */

import {
  DisjointSet,
  WeightedDisjointSet,
  countComponents,
  findRedundantConnection,
  isBipartite,
  mstKruskal,
  DisjointSetGeneric,
  Edge,
} from '../mod.ts';

console.log('=== Disjoint Set (Union-Find) Examples ===\n');

// Example 1: Basic Union-Find Operations
console.log('1. Basic Union-Find Operations');
console.log('-'.repeat(40));

const ds = new DisjointSet(10);
console.log(`Created disjoint set with 10 elements`);
console.log(`Initial count: ${ds.count} disjoint sets`);

ds.union(0, 1);
ds.union(2, 3);
ds.union(0, 2);
console.log(`After unions (0,1), (2,3), (0,2): ${ds.count} disjoint sets`);
console.log(`Are 0 and 3 connected? ${ds.connected(0, 3)}`);
console.log(`Are 0 and 5 connected? ${ds.connected(0, 5)}`);
console.log(`Set size containing 0: ${ds.setSize(0)}`);

// Show all sets
console.log('\nAll disjoint sets:');
const sets = ds.sets();
for (const [root, elements] of sets) {
  console.log(`  Set rooted at ${root}: [${elements.join(', ')}]`);
}
console.log();

// Example 2: Finding Connected Components
console.log('2. Counting Connected Components in a Graph');
console.log('-'.repeat(40));

// Graph:
//   0 --- 1 --- 2
//   |
//   3     4 --- 5
const edges: [number, number][] = [
  [0, 1], [1, 2], [0, 3], [4, 5],
];
const components = countComponents(6, edges);
console.log(`Graph with edges: ${JSON.stringify(edges)}`);
console.log(`Number of connected components: ${components}\n`);

// Example 3: Detecting Cycles / Finding Redundant Edge
console.log('3. Finding Redundant Connection (Cycle Detection)');
console.log('-'.repeat(40));

// Tree with extra edge creating a cycle
const redundantEdges: [number, number][] = [
  [1, 2], [1, 3], [2, 3], // Edge 2-3 creates cycle with 1-2-3
];
const redundant = findRedundantConnection(3, redundantEdges);
console.log(`Edges: ${JSON.stringify(redundantEdges)}`);
console.log(`Redundant edge: ${redundant ? `[${redundant.join(', ')}]` : 'none'}\n`);

// Example 4: Bipartite Graph Check
console.log('4. Checking if Graph is Bipartite');
console.log('-'.repeat(40));

// Bipartite graph (square)
const bipartiteGraph: number[][] = [
  [1, 3], // 0 connects to 1, 3
  [0, 2], // 1 connects to 0, 2
  [1, 3], // 2 connects to 1, 3
  [0, 2], // 3 connects to 0, 2
];
console.log(`Square graph is bipartite: ${isBipartite(bipartiteGraph)}`);

// Triangle (not bipartite)
const triangleGraph: number[][] = [
  [1, 2],
  [0, 2],
  [0, 1],
];
console.log(`Triangle graph is bipartite: ${isBipartite(triangleGraph)}\n`);

// Example 5: Minimum Spanning Tree (Kruskal's Algorithm)
console.log('5. Minimum Spanning Tree (Kruskal\'s Algorithm)');
console.log('-'.repeat(40));

// Weighted graph:
//       2
//   0 ----- 1
//   | \     |
// 4 |  \3   | 1
//   |   \   |
//   2 ----- 3
//       5
const mstEdges: Edge[] = [
  { from: 0, to: 1, weight: 4 },
  { from: 0, to: 2, weight: 1 },
  { from: 1, to: 3, weight: 2 },
  { from: 2, to: 3, weight: 1 },
];

const { totalWeight, mstEdges: mstResult } = mstKruskal(4, mstEdges);
console.log(`Graph edges: ${JSON.stringify(mstEdges)}`);
console.log(`MST total weight: ${totalWeight}`); // 1+1+2 = 4
console.log(`MST edges: ${JSON.stringify(mstResult)}\n`);

// Example 6: Weighted Disjoint Set
console.log('6. Weighted Disjoint Set (Union by Size)');
console.log('-'.repeat(40));

const wds = new WeightedDisjointSet(8);
wds.union(0, 1);
wds.union(2, 3);
wds.union(0, 2);
wds.union(4, 5);
wds.union(6, 7);
wds.union(4, 6);

console.log(`After unions, disjoint sets count: ${wds.count}`);
console.log(`Size of set containing 0: ${wds.setSize(0)}`);
console.log(`Size of set containing 4: ${wds.setSize(4)}`);
console.log(`Are 1 and 3 in same set? ${wds.connected(1, 3)}`);
console.log(`Are 0 and 4 in same set? ${wds.connected(0, 4)}\n`);

// Example 7: Generic Disjoint Set with Strings
console.log('7. Generic Disjoint Set with String Elements');
console.log('-'.repeat(40));

const stringDs = new DisjointSetGeneric<string>();
stringDs.add('apple');
stringDs.add('banana');
stringDs.add('cherry');
stringDs.add('date');

stringDs.union('apple', 'banana');
stringDs.union('cherry', 'date');

console.log(`String elements count: ${stringDs.count}`);
console.log(`'apple' connected to 'banana'? ${stringDs.connected('apple', 'banana')}`);
console.log(`'apple' connected to 'cherry'? ${stringDs.connected('apple', 'cherry')}`);
console.log(`Elements in 'apple's set: ${stringDs.elements('apple')}\n`);

// Example 8: Reset and Reuse
console.log('8. Reset and Reuse');
console.log('-'.repeat(40));

const ds2 = new DisjointSet(5);
ds2.union(0, 1);
ds2.union(2, 3);
console.log(`Before reset: ${ds2.count} sets`);

ds2.reset();
console.log(`After reset: ${ds2.count} sets`);
console.log(`Are 0 and 1 connected after reset? ${ds2.connected(0, 1)}`);

console.log('\n=== All Examples Complete ===');