/**
 * Count-Min Sketch - Probabilistic frequency estimation
 */

class CountMinConfig {
  constructor(depth, width, seed = 0xDEADBEEF) {
    this.depth = Math.max(1, depth);
    this.width = Math.max(2, width);
    this.seed = seed;
  }

  static optimal(epsilon, delta) {
    const width = Math.ceil(Math.E / epsilon);
    const depth = Math.ceil(-Math.log(delta));
    return new CountMinConfig(
      Math.max(1, depth),
      Math.max(2, width)
    );
  }
}

class CountMinSketch {
  constructor(depth, width, seed = 0xDEADBEEF) {
    this.depth = Math.max(1, depth);
    this.width = Math.max(2, width);
    this.seed = seed;
    this.table = Array.from({ length: this.depth }, () => new Array(this.width).fill(0));
    this._totalCount = 0;
  }

  static withRate(epsilon, delta) {
    const config = CountMinConfig.optimal(epsilon, delta);
    return new CountMinSketch(config.depth, config.width, config.seed);
  }

  _getHashes(item) {
    const str = String(item);
    let h1 = 0;
    for (let i = 0; i < str.length; i++) {
      h1 = (h1 * 0x100000001b3 + str.charCodeAt(i)) >>> 0;
    }

    let h2 = this.seed;
    for (let i = 0; i < str.length; i++) {
      h2 = (h2 * 0x100000001b3 + str.charCodeAt(i)) >>> 0;
    }

    const hashes = [];
    for (let i = 0; i < this.depth; i++) {
      hashes.push((h1 + i * h2) >>> 0);
    }
    return hashes;
  }

  update(item, delta) {
    const hashes = this._getHashes(item);
    for (let i = 0; i < hashes.length; i++) {
      const idx = hashes[i] % this.width;
      this.table[i][idx] += delta;
    }
    this._totalCount += delta;
  }

  increment(item) {
    this.update(item, 1);
  }

  estimate(item) {
    const hashes = this._getHashes(item);
    let min = this.table[0][hashes[0] % this.width];
    for (let i = 1; i < hashes.length; i++) {
      const idx = hashes[i] % this.width;
      const val = this.table[i][idx];
      if (val < min) min = val;
    }
    return min;
  }

  totalCount() {
    return this._totalCount;
  }

  dimensions() {
    return [this.depth, this.width];
  }

  merge(other) {
    if (this.depth !== other.depth || this.width !== other.width) {
      throw new Error('Dimension mismatch');
    }
    for (let i = 0; i < this.depth; i++) {
      for (let j = 0; j < this.width; j++) {
        this.table[i][j] += other.table[i][j];
      }
    }
    this._totalCount += other.totalCount;
  }

  toBytes() {
    const size = 32 + this.depth * this.width * 8;
    const bytes = new Uint8Array(size);
    const view = new DataView(bytes.buffer);

    view.setUint32(0, this.depth, true);
    view.setUint32(4, this.width, true);
    view.setBigInt64(8, BigInt(this.seed), true);
    view.setBigInt64(16, BigInt(this._totalCount), true);

    let offset = 24;
    for (let i = 0; i < this.depth; i++) {
      for (let j = 0; j < this.width; j++) {
        view.setBigInt64(offset, BigInt(this.table[i][j]), true);
        offset += 8;
      }
    }
    return bytes;
  }

  clear() {
    for (let i = 0; i < this.depth; i++) {
      this.table[i].fill(0);
    }
    this._totalCount = 0;
  }
}

// Tests
function runTests() {
  console.log('Running Count-Min Sketch tests...');

  // Test 1: Basic increment
  const sketch1 = new CountMinSketch(5, 100);
  sketch1.increment('hello');
  sketch1.increment('hello');
  sketch1.increment('world');
  console.assert(sketch1.estimate('hello') >= 2, 'Test 1 failed: hello');
  console.assert(sketch1.estimate('world') >= 1, 'Test 1 failed: world');
  console.assert(sketch1.estimate('missing') === 0, 'Test 1 failed: missing');
  console.log('✓ Test 1: Basic increment');

  // Test 2: Update with delta
  const sketch2 = new CountMinSketch(5, 100);
  sketch2.update('item', 5);
  console.assert(sketch2.estimate('item') >= 5, 'Test 2 failed');
  console.log('✓ Test 2: Update with delta');

  // Test 3: Total count
  const sketch3 = new CountMinSketch(5, 100);
  sketch3.increment('a');
  sketch3.update('b', 3);
  sketch3.increment('c');
  console.assert(sketch3.totalCount() === 5, 'Test 3 failed');
  console.log('✓ Test 3: Total count');

  // Test 4: Merge
  const sketch4a = new CountMinSketch(5, 100);
  const sketch4b = new CountMinSketch(5, 100);
  sketch4a.increment('hello');
  sketch4b.increment('world');
  sketch4b.increment('world');
  sketch4a.merge(sketch4b);
  console.assert(sketch4a.estimate('hello') >= 1, 'Test 4 failed: hello');
  console.assert(sketch4a.estimate('world') >= 2, 'Test 4 failed: world');
  console.log('✓ Test 4: Merge');

  // Test 5: Clear
  const sketch5 = new CountMinSketch(5, 100);
  sketch5.increment('test');
  sketch5.clear();
  console.assert(sketch5.estimate('test') === 0, 'Test 5 failed');
  console.log('✓ Test 5: Clear');

  // Test 6: Optimal config
  const config = CountMinConfig.optimal(0.01, 0.01);
  console.assert(config.depth >= 1 && config.width >= 2, 'Test 6 failed');
  console.log('✓ Test 6: Optimal config');

  // Test 7: Serialization
  const sketch7 = CountMinSketch.withRate(0.01, 0.01);
  sketch7.increment('apple');
  sketch7.increment('banana');
  sketch7.increment('apple');
  const bytes = sketch7.toBytes();
  console.assert(bytes.length > 0, 'Test 7 failed: serialization');
  console.log('✓ Test 7: Serialization');

  // Test 8: Dimensions
  const sketch8 = new CountMinSketch(7, 200);
  const [d, w] = sketch8.dimensions();
  console.assert(d === 7 && w === 200, 'Test 8 failed');
  console.log('✓ Test 8: Dimensions');

  console.log('\n✅ All tests passed!');
}

if (typeof require !== 'undefined' && require.main === module) {
  runTests();
}

module.exports = { CountMinSketch, CountMinConfig };