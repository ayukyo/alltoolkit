/**
 * XOR Filter Utils - Usage Examples
 */

import {
  XorFilter,
  FuseXorFilter,
  XorFilter8,
  XorFilter16,
  createXorFilter,
  compareWithBloomFilter,
} from '../mod';

/**
 * Example 1: Basic Set Membership Detection
 */
function basicExample(): void {
  console.log('=== Basic XOR Filter Example ===\n');

  // Create a filter from string elements
  const filter = XorFilter.fromElements(['apple', 'banana', 'cherry', 'date']);

  console.log('Filter info:', filter.toString());
  console.log('Bits per element:', filter.bitsPerElement.toFixed(2));
  console.log('False positive rate:', (filter.falsePositiveRate() * 100).toFixed(2) + '%');

  // Test membership
  const testItems = ['apple', 'grape', 'cherry', 'elderberry'];
  for (const item of testItems) {
    console.log(`  "${item}" in filter: ${filter.contains(item)}`);
  }
}

/**
 * Example 2: Large Scale Membership Detection
 */
function largeScaleExample(): void {
  console.log('\n=== Large Scale Example ===\n');

  // Simulate a large dataset (e.g., blocked IPs, banned usernames)
  const blockedIPs = Array.from({ length: 10000 }, (_, i) => `192.168.${Math.floor(i / 256)}.${i % 256}`);

  const filter = XorFilter.fromElements(blockedIPs);
  console.log('Blocked IPs filter:', filter.toString());

  // Test some IPs
  const testIPs = ['192.168.1.1', '10.0.0.1', '192.168.50.100'];
  for (const ip of testIPs) {
    const result = filter.contains(ip);
    console.log(`  ${ip}: ${result ? 'blocked (may be false positive)' : 'not blocked'}`);
  }
}

/**
 * Example 3: Fuse XOR Filter
 */
function fuseExample(): void {
  console.log('\n=== FuseXorFilter Example ===\n');

  const fxf = FuseXorFilter.fromElements(['alpha', 'beta', 'gamma', 'delta']);

  console.log('Fuse filter:', fxf.toString());

  const items = ['alpha', 'omega', 'beta', 'sigma'];
  for (const item of items) {
    console.log(`  "${item}" in filter: ${fxf.contains(item)}`);
  }
}

/**
 * Example 4: Serialization (Persistent Storage)
 */
function serializationExample(): void {
  console.log('\n=== Serialization Example ===\n');

  // Create and populate a filter
  const original = XorFilter.fromElements(['persistent', 'data', 'filter']);

  // Serialize to bytes
  const bytes = original.toBytes();
  console.log(`Serialized size: ${bytes.length} bytes`);

  // Later... restore from bytes
  const restored = XorFilter.fromBytes(bytes);
  console.log('Restored filter:', restored.toString());

  // Verify contents
  for (const item of ['persistent', 'data', 'filter']) {
    console.log(`  Contains "${item}": ${restored.contains(item)}`);
  }
}

/**
 * Example 5: Compare with Bloom Filter
 */
function comparisonExample(): void {
  console.log('\n=== Bloom Filter Comparison ===\n');

  const testSizes = [1000, 10000, 100000, 1000000];
  const targetFpp = 0.001; // 0.1% false positive rate

  console.log(`Target false positive rate: ${(targetFpp * 100).toFixed(2)}%\n`);

  for (const size of testSizes) {
    const comparison = compareWithBloomFilter(size, targetFpp);

    console.log(`${size.toLocaleString()} elements:`);
    console.log(`  XOR Filter:  ${comparison.xorFilter.bitsPerElement.toFixed(2)} bits/elem (${comparison.xorFilter.totalBytes.toFixed(0)} bytes)`);
    console.log(`  Bloom Filter: ${comparison.bloomFilter.bitsPerElement.toFixed(2)} bits/elem (${comparison.bloomFilter.totalBytes.toFixed(0)} bytes)`);
    console.log(`  Space savings: ${comparison.spaceSavingsPercent.toFixed(2)}%`);
  }
}

/**
 * Example 6: Number Elements
 */
function numberExample(): void {
  console.log('\n=== Number Elements Example ===\n');

  // Useful for checking if an ID exists without storing all IDs
  const userIds = Array.from({ length: 5000 }, (_, i) => 10000 + i * 7);

  const filter = XorFilter.fromElements(userIds);
  console.log('User IDs filter:', filter.toString());

  // Test some IDs
  const testIds = [10000, 99999, 10100, 50000];
  for (const id of testIds) {
    console.log(`  User ID ${id}: ${filter.contains(id) ? 'found' : 'not found'}`);
  }
}

// Run all examples
console.log('XOR Filter Utils - Usage Examples\n' + '='.repeat(50));

basicExample();
largeScaleExample();
fuseExample();
serializationExample();
comparisonExample();
numberExample();

console.log('\n' + '='.repeat(50));
console.log('All examples completed!');