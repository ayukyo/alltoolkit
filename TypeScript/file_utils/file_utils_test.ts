/**
 * File Utilities Test Suite
 * Comprehensive tests for file operations
 */

import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import {
  formatBytes,
  readTextFile,
  readBinaryFile,
  writeTextFile,
  writeBinaryFile,
  fileExists,
  isFile,
  isDirectory,
  ensureDirectory,
  listFiles,
  copyFile,
  moveFile,
  deleteFile,
  deleteDirectory,
  getFileInfo,
  calculateHash,
  getUniqueFilename,
  FileResult
} from './mod';

// Test utilities
function createTempDir(): string {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'file_utils_test_'));
}

function cleanupTempDir(dir: string): void {
  if (fs.existsSync(dir)) {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

// Test formatBytes
function testFormatBytes(): void {
  console.log('Testing formatBytes...');
  
  const tests = [
    { input: 0, expected: '0 Bytes' },
    { input: 1024, expected: '1 KB' },
    { input: 1024 * 1024, expected: '1 MB' },
    { input: 1536, expected: '1.5 KB' },
  ];
  
  for (const test of tests) {
    const result = formatBytes(test.input);
    if (!result.includes(test.expected.split(' ')[0])) {
      console.error(`  FAIL: formatBytes(${test.input}) = "${result}", expected to contain "${test.expected}"`);
    } else {
      console.log(`  PASS: formatBytes(${test.input}) = "${result}"`);
    }
  }
}

// Test readTextFile
function testReadTextFile(tempDir: string): void {
  console.log('\nTesting readTextFile...');
  
  // Test reading existing file
  const testFile = path.join(tempDir, 'test.txt');
  fs.writeFileSync(testFile, 'Hello, World!', 'utf-8');
  
  const result = readTextFile(testFile);
  if (!result.success || result.data !== 'Hello, World!') {
    console.error('  FAIL: readTextFile existing file');
  } else {
    console.log('  PASS: readTextFile existing file');
  }
  
  // Test reading non-existent file
  const nonExistent = path.join(tempDir, 'nonexistent.txt');
  const result2 = readTextFile(nonExistent);
  if (result2.success) {
    console.error('  FAIL: readTextFile should fail for non-existent file');
  } else {
    console.log('  PASS: readTextFile non-existent file returns error');
  }
  
  // Test with default value
  const result3 = readTextFile(nonExistent, { default: 'default content' });
  if (!result3.success || result3.data !== 'default content') {
    console.error('  FAIL: readTextFile with default value');
  } else {
    console.log('  PASS: readTextFile with default value');
  }
}

// Test writeTextFile
function testWriteTextFile(tempDir: string): void {
  console.log('\nTesting writeTextFile...');
  
  // Test writing new file
  const testFile = path.join(tempDir, 'write_test.txt');
  const result = writeTextFile(testFile, 'Test content');
  if (!result.success || !fs.existsSync(testFile)) {
    console.error('  FAIL: writeTextFile new file');
  } else {
    console.log('  PASS: writeTextFile new file');
  }
  
  // Test writing with createDirs
  const nestedFile = path.join(tempDir, 'nested', 'dir', 'file.txt');
  const result2 = writeTextFile(nestedFile, 'Nested content', { createDirs: true });
  if (!result2.success || !fs.existsSync(nestedFile)) {
    console.error('  FAIL: writeTextFile with createDirs');
  } else {
    console.log('  PASS: writeTextFile with createDirs');
  }
  
  // Test atomic write
  const atomicFile = path.join(tempDir, 'atomic.txt');
  const result3 = writeTextFile(atomicFile, 'Atomic content', { atomic: true });
  if (!result3.success || !fs.existsSync(atomicFile)) {
    console.error('  FAIL: writeTextFile atomic');
  } else {
    console.log('  PASS: writeTextFile atomic');
  }
}

// Test readBinaryFile and writeBinaryFile
function testBinaryFileOperations(tempDir: string): void {
  console.log('\nTesting binary file operations...');
  
  const binaryFile = path.join(tempDir, 'binary.bin');
  const content = Buffer.from([0x00, 0x01, 0x02, 0xFF, 0xFE]);
  
  // Write binary
  const writeResult = writeBinaryFile(binaryFile, content);
  if (!writeResult.success) {
    console.error('  FAIL: writeBinaryFile');
    return;
  }
  console.log('  PASS: writeBinaryFile');
  
  // Read binary
  const readResult = readBinaryFile(binaryFile);
  if (!readResult.success || !readResult.data) {
    console.error('  FAIL: readBinaryFile');
    return;
  }
  
  // Compare content
  if (readResult.data.equals(content)) {
    console.log('  PASS: readBinaryFile content matches');
  } else {
    console.error('  FAIL: readBinaryFile content does not match');
  }
}

// Test fileExists
function testFileExists(tempDir: string): void {
  console.log('\nTesting fileExists...');
  
  const existingFile = path.join(tempDir, 'exists.txt');
  fs.writeFileSync(existingFile, 'test');
  
  if (!fileExists(existingFile)) {
    console.error('  FAIL: fileExists should return true for existing file');
  } else {
    console.log('  PASS: fileExists existing file');
  }
  
  const nonExistent = path.join(tempDir, 'does_not_exist.txt');
  if (fileExists(nonExistent)) {
    console.error('  FAIL: fileExists should return false for non-existent file');
  } else {
    console.log('  PASS: fileExists non-existent file');
  }
}

// Test isFile and isDirectory
function testIsFileAndDirectory(tempDir: string): void {
  console.log('\nTesting isFile and isDirectory...');
  
  const file = path.join(tempDir, 'testfile.txt');
  const dir = path.join(tempDir, 'testdir');
  fs.writeFileSync(file, 'test');
  fs.mkdirSync(dir);
  
  // Test isFile
  const fileResult = isFile(file);
  if (!fileResult.success || !fileResult.data) {
    console.error('  FAIL: isFile should return true for file');
  } else {
    console.log('  PASS: isFile');
  }
  
  // Test isDirectory
  const dirResult = isDirectory(dir);
  if (!dirResult.success || !dirResult.data) {
    console.error('  FAIL: isDirectory should return true for directory');
  } else {
    console.log('  PASS: isDirectory');
  }
  
  // Test isFile on directory
  const fileOnDir = isFile(dir);
  if (!fileOnDir.success || fileOnDir.data) {
    console.error('  FAIL: isFile should return false for directory');
  } else {
    console.log('  PASS: isFile returns false for directory');
  }
}

// Test ensureDirectory
function testEnsureDirectory(tempDir: string): void {
  console.log('\nTesting ensureDirectory...');
  
  const newDir = path.join(tempDir, 'new', 'nested', 'directory');
  const result = ensureDirectory(newDir);
  
  if (!result.success || !fs.existsSync(newDir)) {
    console.error('  FAIL: ensureDirectory should create nested directories');
  } else {
    console.log('  PASS: ensureDirectory creates nested directories');
  }
  
  // Test on existing directory
  const result2 = ensureDirectory(newDir);
  if (!result2.success) {
    console.error('  FAIL: ensureDirectory should succeed for existing directory');
  } else {
    console.log('  PASS: ensureDirectory succeeds for existing directory');
  }
}

// Test listFiles
function testListFiles(tempDir: string): void {
  console.log('\nTesting listFiles...');
  
  // Create test files
  fs.writeFileSync(path.join(tempDir, 'file1.txt'), '1');
  fs.writeFileSync(path.join(tempDir, 'file2.js'), '2');
  fs.writeFileSync(path.join(tempDir, 'file3.txt'), '3');
  fs.mkdirSync(path.join(tempDir, 'subdir'));
  
  // Test basic listing
  const result = listFiles(tempDir);
  if (!result.success || !result.data || result.data.length < 3) {
    console.error('  FAIL: listFiles should return files');
  } else {
    console.log('  PASS: listFiles returns files');
  }
  
  // Test with pattern
  const result2 = listFiles(tempDir, { pattern: '*.txt' });
  if (!result2.success || !result2.data) {
    console.error('  FAIL: listFiles with pattern');
  } else {
    const txtFiles = result2.data.filter(f => f.endsWith('.txt'));
    if (txtFiles.length === 2) {
      console.log('  PASS: listFiles with pattern filter');
    } else {
      console.error(`  FAIL: listFiles pattern filter returned ${txtFiles.length} files, expected 2`);
    }
  }
}

// Test copyFile
function testCopyFile(tempDir: string): void {
  console.log('\nTesting copyFile...');
  
  const source = path.join(tempDir, 'source.txt');
  const dest = path.join(tempDir, 'dest.txt');
  fs.writeFileSync(source, 'Copy me!');
  
  const result = copyFile(source, dest);
  if (!result.success || !fs.existsSync(dest)) {
    console.error('  FAIL: copyFile should copy file');
  } else {
    const content = fs.readFileSync(dest, 'utf-8');
    if (content === 'Copy me!') {
      console.log('  PASS: copyFile copies content correctly');
    } else {
      console.error('  FAIL: copyFile content does not match');
    }
  }
}

// Test moveFile
function testMoveFile(tempDir: string): void {
  console.log('\nTesting moveFile...');
  
  const source = path.join(tempDir, 'move_source.txt');
  const dest = path.join(tempDir, 'move_dest.txt');
  fs.writeFileSync(source, 'Move me!');
  
  const result = moveFile(source, dest);
  if (!result.success || fs.existsSync(source) || !fs.existsSync(dest)) {
    console.error('  FAIL: moveFile should move file');
  } else {
    console.log('  PASS: moveFile moves file correctly');
  }
}

// Test deleteFile
function testDeleteFile(tempDir: string): void {
  console.log('\nTesting deleteFile...');
  
  const file = path.join(tempDir, 'delete_me.txt');
  fs.writeFileSync(file, 'Delete me!');
  
  const result = deleteFile(file);
  if (!result.success || fs.existsSync(file)) {
    console.error('  FAIL: deleteFile should delete file');
  } else {
    console.log('  PASS: deleteFile deletes file');
  }
  
  // Test delete non-existent with missing_ok
  const result2 = deleteFile(path.join(tempDir, 'nonexistent.txt'), { missingOk: true });
  if (!result2.success) {
    console.error('  FAIL: deleteFile with missingOk should succeed');
  } else {
    console.log('  PASS: deleteFile with missingOk');
  }
}

// Test getFileInfo
function testGetFileInfo(tempDir: string): void {
  console.log('\nTesting getFileInfo...');
  
  const file = path.join(tempDir, 'info_test.txt');
  fs.writeFileSync(file, 'Info test content');
  
  const result = getFileInfo(file);
  if (!result.success || !result.data) {
    console.error('  FAIL: getFileInfo should return file info');
  } else {
    const info = result.data;
    if (info.name === 'info_test.txt' && info.size > 0 && !info.isDirectory) {
      console.log('  PASS: getFileInfo returns correct info');
    } else {
      console.error('  FAIL: getFileInfo returned incorrect info');
    }
  }
}

// Test calculateHash
function testCalculateHash(tempDir: string): void {
  console.log('\nTesting calculateHash...');
  
  const file = path.join(tempDir, 'hash_test.txt');
  fs.writeFileSync(file, 'Hash test content');
  
  const result = calculateHash(file, 'sha256');
  if (!result.success || !result.data) {
    console.error('  FAIL: calculateHash should return hash');
  } else {
    if (result.data.length === 64) { // SHA256 hex length
      console.log('  PASS: calculateHash returns SHA256 hash');
    } else {
      console.error(`  FAIL: calculateHash returned hash of length ${result.data.length}`);
    }
  }
  
  // Test MD5
  const result2 = calculateHash(file, 'md5');
  if (!result2.success || !result2.data || result2.data.length !== 32) {
    console.error('  FAIL: calculateHash MD5');
  } else {
    console.log('  PASS: calculateHash returns MD5 hash');
  }
}

// Test getUniqueFilename
function testGetUniqueFilename(tempDir: string): void {
  console.log('\nTesting getUniqueFilename...');
  
  const file = path.join(tempDir, 'unique.txt');
  fs.writeFileSync(file, 'exists');
  
  const result = getUniqueFilename(file);
  if (!result.success || !result.data) {
    console.error('  FAIL: getUniqueFilename should return unique name');
  } else {
    if (result.data !== file && !fs.existsSync(result.data)) {
      console.log('  PASS: getUniqueFilename returns non-existent filename');
    } else {
      console.error('  FAIL: getUniqueFilename returned existing filename');
    }
  }
}

// Run all tests
function runTests(): void {
  console.log('=== File Utils Test Suite ===\n');
  
  const tempDir = createTempDir();
  console.log(`Using temp directory: ${tempDir}\n`);
  
  try {
    testFormatBytes();
    testReadTextFile(tempDir);
    testWriteTextFile(tempDir);
    testBinaryFileOperations(tempDir);
    testFileExists(tempDir);
    testIsFileAndDirectory(tempDir);
    testEnsureDirectory(tempDir);
    testListFiles(tempDir);
    testCopyFile(tempDir);
    testMoveFile(tempDir);
    testDeleteFile(tempDir);
    testGetFileInfo(tempDir);
    testCalculateHash(tempDir);
    testGetUniqueFilename(tempDir);
    
    console.log('\n=== All Tests Completed ===');
  } finally {
    cleanupTempDir(tempDir);
    console.log(`\nCleaned up temp directory`);
  }
}

// Run tests if this file is executed directly
if (require.main === module) {
  runTests();
}

export { runTests };
