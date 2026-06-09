/**
 * Count-Min Sketch Implementation
 * Probabilistic data structure for frequency estimation
 */

export interface CountMinConfig {
  depth: number;
  width: number;
  seed: number;
}

export class CountMinSketch<T> {
  private table: number[][];
  private depth: number;
  private width: number;
  private seed: number;
  private total: number;

  constructor(depth: number, width: number, seed: number = 0xDEADBEEF) {
    this.depth = Math.max(1, depth);
    this.width = Math.max(2, width);
    this.seed = seed;
    this.table = Array.from({ length: this.depth }, () => new Array(this.width).fill(0));
    this.total = 0;
  }

  static optimal(epsilon: number, delta: number): CountMinConfig {
    const width = Math.ceil(Math.E / epsilon);
    const depth = Math.ceil(-Math.log(delta));
    return {
      depth: Math.max(1, depth),
      width: Math.max(2, width),
      seed: 0xDEADBEEF,
    };
  }

  static withRate<T>(epsilon: number, delta: number): CountMinSketch<T> {
    const config = CountMinSketch.optimal(epsilon, delta);
    return new CountMinSketch<T>(config.depth, config.width, config.seed);
  }

  update(item: T, delta: number): void {
    const hashes = this.getHashes(item);
    for (let i = 0; i < hashes.length; i++) {
      const idx = hashes[i] % this.width;
      this.table[i][idx] += delta;
    }
    this.total += delta;
  }

  increment(item: T): void {
    this.update(item, 1);
  }

  estimate(item: T): number {
    const hashes = this.getHashes(item);
    let min = this.table[0][hashes[0] % this.width];
    for (let i = 1; i < hashes.length; i++) {
      const idx = hashes[i] % this.width;
      const val = this.table[i][idx];
      if (val < min) min = val;
    }
    return min;
  }

  totalCount(): number {
    return this.total;
  }

  dimensions(): [number, number] {
    return [this.depth, this.width];
  }

  merge(other: CountMinSketch<T>): void {
    if (this.depth !== other.depth || this.width !== other.width) {
      throw new Error('Dimension mismatch');
    }
    for (let i = 0; i < this.depth; i++) {
      for (let j = 0; j < this.width; j++) {
        this.table[i][j] += other.table[i][j];
      }
    }
    this.total += other.total;
  }

  toBytes(): Uint8Array {
    const size = 32 + this.depth * this.width * 8;
    const bytes = new Uint8Array(size);
    const view = new DataView(bytes.buffer);

    view.setUint32(0, this.depth, true);
    view.setUint32(4, this.width, true);
    view.setBigUint64(8, BigInt(this.seed), true);
    view.setBigUint64(16, BigInt(this.total), true);

    let offset = 24;
    for (let i = 0; i < this.depth; i++) {
      for (let j = 0; j < this.width; j++) {
        view.setBigUint64(offset, BigInt(this.table[i][j]), true);
        offset += 8;
      }
    }
    return bytes;
  }

  clear(): void {
    for (let i = 0; i < this.depth; i++) {
      this.table[i].fill(0);
    }
    this.total = 0;
  }

  private getHashes(item: T): number[] {
    const str = String(item);
    let h1 = 0;
    for (let i = 0; i < str.length; i++) {
      h1 = (h1 * 0x100000001b3 + str.charCodeAt(i)) >>> 0;
    }

    let h2 = this.seed;
    for (let i = 0; i < str.length; i++) {
      h2 = (h2 * 0x100000001b3 + str.charCodeAt(i)) >>> 0;
    }

    const hashes: number[] = [];
    for (let i = 0; i < this.depth; i++) {
      hashes.push((h1 + i * h2) >>> 0);
    }
    return hashes;
  }
}

// Test suite
export function runTests(): void {
  console.log('Running Count-Min Sketch tests...');

  const sketch1 = new CountMinSketch<string>(5, 100);
  sketch1.increment('hello');
  sketch1.increment('hello');
  sketch1.increment('world');
  console.assert(sketch1.estimate('hello') >= 2, 'Test 1 failed');
  console.assert(sketch1.estimate('world') >= 1, 'Test 1 failed');
  console.assert(sketch1.estimate('missing') === 0, 'Test 1 failed');
  console.log('✓ Test 1: Basic increment');

  const sketch2 = new CountMinSketch<string>(5, 100);
  sketch2.update('item', 5);
  console.assert(sketch2.estimate('item') >= 5, 'Test 2 failed');
  console.log('✓ Test 2: Update with delta');

  const sketch3 = new CountMinSketch<string>(5, 100);
  sketch3.increment('a');
  sketch3.update('b', 3);
  sketch3.increment('c');
  console.assert(sketch3.totalCount() === 5, 'Test 3 failed');
  console.log('✓ Test 3: Total count');

  const sketch4a = new CountMinSketch<string>(5, 100);
  const sketch4b = new CountMinSketch<string>(5, 100);
  sketch4a.increment('hello');
  sketch4b.increment('world');
  sketch4b.increment('world');
  sketch4a.merge(sketch4b);
  console.assert(sketch4a.estimate('hello') >= 1, 'Test 4 failed');
  console.assert(sketch4a.estimate('world') >= 2, 'Test 4 failed');
  console.log('✓ Test 4: Merge');

  const sketch5 = new CountMinSketch<string>(5, 100);
  sketch5.increment('test');
  sketch5.clear();
  console.assert(sketch5.estimate('test') === 0, 'Test 5 failed');
  console.log('✓ Test 5: Clear');

  const config = CountMinSketch.optimal(0.01, 0.01);
  console.assert(config.depth >= 1 && config.width >= 2, 'Test 6 failed');
  console.log('✓ Test 6: Optimal config');

  const sketch7 = CountMinSketch.withRate<string>(0.01, 0.01);
  sketch7.increment('apple');
  sketch7.increment('banana');
  sketch7.increment('apple');
  const bytes = sketch7.toBytes();
  console.assert(bytes.length > 0, 'Test 7 failed');
  console.log('✓ Test 7: Serialization');

  const sketch8 = new CountMinSketch<string>(7, 200);
  const [d, w] = sketch8.dimensions();
  console.assert(d === 7 && w === 200, 'Test 8 failed');
  console.log('✓ Test 8: Dimensions');

  console.log('\n✅ All tests passed!');
}

if (require.main === module) {
  runTests();
}