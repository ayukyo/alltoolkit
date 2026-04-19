/**
 * Disjoint Set (Union-Find) Data Structure
 * 
 * A high-performance implementation with path compression and union by rank
 * optimizations for efficient set operations.
 * 
 * Time Complexity:
 * - Find: O(α(n)) amortized, where α is the inverse Ackermann function
 * - Union: O(α(n)) amortized
 * - Connected: O(α(n)) amortized
 * 
 * Space Complexity: O(n)
 */

export class DisjointSet {
  private parent: number[];
  private rank: number[];
  private _count: number;

  /**
   * Creates a new DisjointSet with n elements (0 to n-1).
   * Initially, each element is in its own set.
   */
  constructor(n: number) {
    this.parent = Array.from({ length: n }, (_, i) => i);
    this.rank = new Array(n).fill(0);
    this._count = n;
  }

  /**
   * Finds the root (representative) of the set containing element x.
   * Uses path compression for efficiency.
   */
  find(x: number): number {
    if (x < 0 || x >= this.parent.length) {
      return -1; // invalid element
    }
    if (this.parent[x] !== x) {
      this.parent[x] = this.find(this.parent[x]); // path compression
    }
    return this.parent[x];
  }

  /**
   * Merges the sets containing elements x and y.
   * Uses union by rank to keep trees flat.
   * Returns true if the sets were merged, false if they were already in the same set.
   */
  union(x: number, y: number): boolean {
    const rootX = this.find(x);
    const rootY = this.find(y);

    if (rootX === -1 || rootY === -1) {
      return false;
    }

    if (rootX === rootY) {
      return false; // already in the same set
    }

    // Union by rank
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

  /**
   * Checks if elements x and y are in the same set.
   */
  connected(x: number, y: number): boolean {
    return this.find(x) === this.find(y) && this.find(x) !== -1;
  }

  /**
   * Returns the number of disjoint sets.
   */
  get count(): number {
    return this._count;
  }

  /**
   * Returns the total number of elements.
   */
  get size(): number {
    return this.parent.length;
  }

  /**
   * Returns the size of the set containing element x.
   */
  setSize(x: number): number {
    const root = this.find(x);
    if (root === -1) return 0;
    
    let size = 0;
    for (let i = 0; i < this.parent.length; i++) {
      if (this.find(i) === root) size++;
    }
    return size;
  }

  /**
   * Returns all disjoint sets as a Map from root to array of elements.
   */
  sets(): Map<number, number[]> {
    const sets = new Map<number, number[]>();
    for (let i = 0; i < this.parent.length; i++) {
      const root = this.find(i);
      if (!sets.has(root)) {
        sets.set(root, []);
      }
      sets.get(root)!.push(i);
    }
    return sets;
  }

  /**
   * Resets the disjoint set to its initial state where each element
   * is in its own set.
   */
  reset(): void {
    for (let i = 0; i < this.parent.length; i++) {
      this.parent[i] = i;
      this.rank[i] = 0;
    }
    this._count = this.parent.length;
  }

  /**
   * Returns all elements in the set containing element x.
   */
  elements(x: number): number[] {
    const root = this.find(x);
    if (root === -1) return [];
    
    const elements: number[] = [];
    for (let i = 0; i < this.parent.length; i++) {
      if (this.find(i) === root) {
        elements.push(i);
      }
    }
    return elements;
  }
}

/**
 * Weighted Disjoint Set with size tracking for each set.
 * Uses union by size instead of union by rank.
 */
export class WeightedDisjointSet {
  private parent: number[];
  private size: number[];
  private _count: number;

  constructor(n: number) {
    this.parent = Array.from({ length: n }, (_, i) => i);
    this.size = new Array(n).fill(1);
    this._count = n;
  }

  find(x: number): number {
    if (x < 0 || x >= this.parent.length) {
      return -1;
    }
    if (this.parent[x] !== x) {
      this.parent[x] = this.find(this.parent[x]);
    }
    return this.parent[x];
  }

  union(x: number, y: number): boolean {
    const rootX = this.find(x);
    const rootY = this.find(y);

    if (rootX === -1 || rootY === -1) return false;
    if (rootX === rootY) return false;

    // Union by size - attach smaller tree under larger tree
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

  connected(x: number, y: number): boolean {
    return this.find(x) === this.find(y) && this.find(x) !== -1;
  }

  setSize(x: number): number {
    const root = this.find(x);
    return root === -1 ? 0 : this.size[root];
  }

  get count(): number {
    return this._count;
  }
}

/**
 * Represents a weighted edge in a graph.
 */
export interface Edge {
  from: number;
  to: number;
  weight: number;
}

/**
 * Counts the number of connected components in a graph.
 */
export function countComponents(n: number, edges: [number, number][]): number {
  const ds = new DisjointSet(n);
  for (const [u, v] of edges) {
    ds.union(u, v);
  }
  return ds.count;
}

/**
 * Finds a redundant edge in an undirected graph that, if removed,
 * would make the graph a tree.
 * Returns the edge that can be removed, or null if no redundant edge exists.
 */
export function findRedundantConnection(
  n: number,
  edges: [number, number][]
): [number, number] | null {
  const ds = new DisjointSet(n + 1); // 1-indexed
  for (const [u, v] of edges) {
    if (ds.connected(u, v)) {
      return [u, v];
    }
    ds.union(u, v);
  }
  return null;
}

/**
 * Checks if a graph is bipartite using disjoint set.
 * graph[i] contains the neighbors of node i.
 */
export function isBipartite(graph: number[][]): boolean {
  const n = graph.length;
  const ds = new DisjointSet(2 * n); // Each node has two "sides"

  for (let i = 0; i < n; i++) {
    for (const neighbor of graph[i]) {
      // If i and neighbor are in the same set, not bipartite
      if (ds.connected(i, neighbor)) {
        return false;
      }
      // Put i and neighbor in opposite groups
      ds.union(i, neighbor + n);
      ds.union(i + n, neighbor);
    }
  }
  return true;
}

/**
 * Computes the minimum spanning tree using Kruskal's algorithm.
 * Returns the total weight and the edges in the MST.
 */
export function mstKruskal(n: number, edges: Edge[]): { totalWeight: number; mstEdges: Edge[] } {
  // Sort edges by weight
  const sortedEdges = [...edges].sort((a, b) => a.weight - b.weight);

  const ds = new DisjointSet(n);
  let totalWeight = 0;
  const mstEdges: Edge[] = [];

  for (const edge of sortedEdges) {
    if (ds.union(edge.from, edge.to)) {
      totalWeight += edge.weight;
      mstEdges.push(edge);
      if (mstEdges.length === n - 1) break;
    }
  }

  return { totalWeight, mstEdges };
}

/**
 * Generic Disjoint Set that can work with any type of elements.
 */
export class DisjointSetGeneric<T> {
  private parent: Map<T, T>;
  private rank: Map<T, number>;
  private _count: number;

  constructor(elements?: T[]) {
    this.parent = new Map();
    this.rank = new Map();
    this._count = 0;

    if (elements) {
      for (const elem of elements) {
        this.add(elem);
      }
    }
  }

  /**
   * Adds a new element to the disjoint set.
   */
  add(element: T): void {
    if (!this.parent.has(element)) {
      this.parent.set(element, element);
      this.rank.set(element, 0);
      this._count++;
    }
  }

  /**
   * Finds the root of the set containing the element.
   */
  find(element: T): T | undefined {
    if (!this.parent.has(element)) return undefined;

    if (this.parent.get(element) !== element) {
      this.parent.set(element, this.find(this.parent.get(element)!)!);
    }
    return this.parent.get(element);
  }

  /**
   * Unions the sets containing elements x and y.
   */
  union(x: T, y: T): boolean {
    const rootX = this.find(x);
    const rootY = this.find(y);

    if (rootX === undefined || rootY === undefined) return false;
    if (rootX === rootY) return false;

    const rankX = this.rank.get(rootX)!;
    const rankY = this.rank.get(rootY)!;

    if (rankX < rankY) {
      this.parent.set(rootX, rootY);
    } else if (rankX > rankY) {
      this.parent.set(rootY, rootX);
    } else {
      this.parent.set(rootY, rootX);
      this.rank.set(rootX, rankX + 1);
    }

    this._count--;
    return true;
  }

  /**
   * Checks if elements x and y are in the same set.
   */
  connected(x: T, y: T): boolean {
    const rootX = this.find(x);
    const rootY = this.find(y);
    return rootX !== undefined && rootX === rootY;
  }

  get count(): number {
    return this._count;
  }

  /**
   * Returns all elements in the set containing the given element.
   */
  elements(element: T): T[] {
    const root = this.find(element);
    if (root === undefined) return [];

    const result: T[] = [];
    for (const [elem] of this.parent) {
      if (this.find(elem) === root) {
        result.push(elem);
      }
    }
    return result;
  }
}