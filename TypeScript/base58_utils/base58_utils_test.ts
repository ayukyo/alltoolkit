/**
 * Base58 工具模块测试
 */

import {
    Base58Encoder,
    base58,
    base58Flickr,
    base58Ripple,
    encodeBase58,
    decodeBase58,
    encodeBase58String,
    decodeBase58String,
    encodeBase58Hex,
    decodeBase58ToHex,
    isValidBase58,
    randomBase58,
    bigIntToBase58,
    base58ToBigInt,
    encodeWithChecksum,
    decodeWithChecksum,
} from './mod';

// 测试辅助函数
function assertEqual<T>(actual: T, expected: T, message: string): void {
    if (actual !== expected) {
        throw new Error(`${message}\n  Expected: ${expected}\n  Actual: ${actual}`);
    }
}

function assertArrayEqual(actual: Uint8Array, expected: number[], message: string): void {
    if (actual.length !== expected.length) {
        throw new Error(`${message}\n  Length mismatch: ${actual.length} vs ${expected.length}`);
    }
    for (let i = 0; i < actual.length; i++) {
        if (actual[i] !== expected[i]) {
            throw new Error(`${message}\n  Mismatch at index ${i}: ${actual[i]} vs ${expected[i]}`);
        }
    }
}

function test(name: string, fn: () => void): void {
    try {
        fn();
        console.log(`✓ ${name}`);
    } catch (e) {
        console.error(`✗ ${name}`);
        throw e;
    }
}

// 标准测试向量（来自 bs58 库验证）
const TEST_VECTORS: Array<[number[], string]> = [
    [[], ''],
    [[0x61], '2g'],
    [[0x62, 0x62, 0x62], 'a3gV'],
    [[0x63, 0x63, 0x63], 'aPEr'],
    [[0x73, 0x69, 0x6d, 0x70, 0x6c, 0x79, 0x20, 0x61, 0x20, 0x6c, 0x6f, 0x6e, 0x67, 0x20, 0x73, 0x74, 0x72, 0x69, 0x6e, 0x67], '2cFupjhnEsSn59qHXstmK2ffpLv2'],
    [[0x51, 0x6b, 0x6f, 0xcd, 0x0f], 'ABnLTmg'],
    [[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], '1111111111'],
    [[0xff, 0xff, 0xff, 0xff, 0xff], 'VtB5VXc'],
];

console.log('\n=== Base58 工具模块测试 ===\n');

// 测试编码
test('编码测试向量', () => {
    for (const [bytes, expected] of TEST_VECTORS) {
        const result = encodeBase58(new Uint8Array(bytes));
        assertEqual(result, expected, `编码 ${JSON.stringify(bytes)}`);
    }
});

// 测试解码
test('解码测试向量', () => {
    for (const [expectedBytes, b58] of TEST_VECTORS) {
        if (b58 === '' && expectedBytes.length === 0) continue;
        const result = decodeBase58(b58);
        assertArrayEqual(result, expectedBytes, `解码 ${b58}`);
    }
});

// 测试字符串编码解码
test('字符串编码解码', () => {
    const testStrings = [
        'Hello, World!',
        '测试中文',
        'The quick brown fox',
        '12345',
        '',
    ];

    for (const str of testStrings) {
        const encoded = encodeBase58String(str);
        const decoded = decodeBase58String(encoded);
        assertEqual(decoded, str, `字符串编解码: ${str}`);
    }
});

// 测试十六进制编码解码
test('十六进制编码解码', () => {
    const testCases = [
        'deadbeef',
        '00',
        'ff',
        '1234567890abcdef',
        '00000001',
    ];

    for (const hex of testCases) {
        const encoded = encodeBase58Hex(hex);
        const decoded = decodeBase58ToHex(encoded);
        assertEqual(decoded.toLowerCase(), hex.toLowerCase(), `十六进制编解码: ${hex}`);
    }
});

// 测试有效性验证
test('Base58 有效性验证', () => {
    assertEqual(isValidBase58('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'), true, '所有有效字符');
    
    assertEqual(isValidBase58('0'), false, '包含 0');
    assertEqual(isValidBase58('O'), false, '包含 O');
    assertEqual(isValidBase58('I'), false, '包含 I');
    assertEqual(isValidBase58('l'), false, '包含 l');
    assertEqual(isValidBase58('+'), false, '包含 +');
    assertEqual(isValidBase58('/'), false, '包含 /');
    
    assertEqual(isValidBase58(''), true, '空字符串');
});

// 测试不同字母表
test('Flickr 字母表', () => {
    const encoder = base58Flickr;
    const bytes = new Uint8Array([0xde, 0xad, 0xbe, 0xef]);
    const encoded = encoder.encode(bytes);
    const decoded = encoder.decode(encoded);
    assertArrayEqual(decoded, [0xde, 0xad, 0xbe, 0xef], 'Flickr 字母表编解码');
});

test('Ripple 字母表', () => {
    const encoder = base58Ripple;
    const bytes = new Uint8Array([0xde, 0xad, 0xbe, 0xef]);
    const encoded = encoder.encode(bytes);
    const decoded = encoder.decode(encoded);
    assertArrayEqual(decoded, [0xde, 0xad, 0xbe, 0xef], 'Ripple 字母表编解码');
});

// 测试随机生成
test('随机 Base58 生成', () => {
    for (const length of [8, 16, 32, 64]) {
        const result = randomBase58(length);
        assertEqual(result.length, length, `随机长度 ${length}`);
        assertEqual(isValidBase58(result), true, `随机结果有效性 ${length}`);
    }
});

// 测试 BigInt 转换
test('BigInt 转换', () => {
    const testCases: bigint[] = [
        0n,
        1n,
        58n,
        123456789n,
        0xdeadbeefn,
        0xffffffffffffffffn,
    ];

    for (const value of testCases) {
        const encoded = bigIntToBase58(value);
        const decoded = base58ToBigInt(encoded);
        assertEqual(decoded, value, `BigInt 转换: ${value}`);
    }
});

test('BigInt 负数异常', () => {
    try {
        bigIntToBase58(-1n);
        throw new Error('应该抛出异常');
    } catch (e) {
        assertEqual((e as Error).message, 'Cannot encode negative BigInt', '负数异常');
    }
});

// 测试带校验和的编解码
test('带校验和的编解码', () => {
    const testData = [
        new Uint8Array([1, 2, 3, 4, 5]),
        new Uint8Array([0xde, 0xad, 0xbe, 0xef]),
        new TextEncoder().encode('Hello'),
    ];

    for (const data of testData) {
        const encoded = encodeWithChecksum(data);
        const decoded = decodeWithChecksum(encoded);
        
        if (decoded === null) {
            throw new Error('校验和解码失败');
        }
        
        assertArrayEqual(decoded, Array.from(data), '带校验和的编解码');
    }
});

test('校验和验证 - 篡改检测', () => {
    const data = new TextEncoder().encode('Test');
    const encoded = encodeWithChecksum(data);
    
    const tampered = encoded.slice(0, -1) + 'x';
    const decoded = decodeWithChecksum(tampered);
    
    assertEqual(decoded, null, '检测到篡改');
});

// 测试边界情况
test('边界情况 - 空数据', () => {
    const empty = new Uint8Array(0);
    assertEqual(encodeBase58(empty), '', '空数据编码');
    assertEqual(decodeBase58('').length, 0, '空字符串解码');
});

test('边界情况 - 全零', () => {
    const zeros = new Uint8Array([0, 0, 0, 0]);
    const encoded = encodeBase58(zeros);
    assertEqual(encoded, '1111', '全零编码');
    assertArrayEqual(decodeBase58('1111'), [0, 0, 0, 0], '全零解码');
});

test('边界情况 - 最大字节值', () => {
    const maxBytes = new Uint8Array([0xff, 0xff, 0xff, 0xff, 0xff]);
    const encoded = encodeBase58(maxBytes);
    assertEqual(encoded, 'VtB5VXc', '最大字节值编码');
    const decoded = decodeBase58('VtB5VXc');
    assertArrayEqual(decoded, [0xff, 0xff, 0xff, 0xff, 0xff], '最大字节值解码');
});

// 测试自定义字母表
test('自定义字母表', () => {
    const customAlphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz123456789';
    const encoder = new Base58Encoder(customAlphabet);
    
    const bytes = new Uint8Array([0xde, 0xad, 0xbe, 0xef]);
    const encoded = encoder.encode(bytes);
    const decoded = encoder.decode(encoded);
    
    assertArrayEqual(decoded, [0xde, 0xad, 0xbe, 0xef], '自定义字母表编解码');
});

test('无效字母表长度', () => {
    try {
        new Base58Encoder('abc');
        throw new Error('应该抛出异常');
    } catch (e) {
        assertEqual((e as Error).message, 'Base58 alphabet must contain exactly 58 characters', '字母表长度异常');
    }
});

// 测试无效字符解码
test('无效字符解码', () => {
    try {
        decodeBase58('abc0def');
        throw new Error('应该抛出异常');
    } catch (e) {
        assertEqual((e as Error).message.includes('Invalid Base58 character'), true, '无效字符异常');
    }
});

// 性能测试
test('性能测试 - 大数据编码', () => {
    const largeData = new Uint8Array(1024);
    for (let i = 0; i < 1024; i++) {
        largeData[i] = i % 256;
    }
    
    const start = Date.now();
    const encoded = encodeBase58(largeData);
    const elapsed = Date.now() - start;
    
    console.log(`  1KB 数据编码耗时: ${elapsed}ms`);
    assertEqual(encoded.length > 0, true, '大数据编码结果');
});

test('性能测试 - 大数据解码', () => {
    const largeData = new Uint8Array(1024);
    for (let i = 0; i < 1024; i++) {
        largeData[i] = i % 256;
    }
    
    const encoded = encodeBase58(largeData);
    
    const start = Date.now();
    const decoded = decodeBase58(encoded);
    const elapsed = Date.now() - start;
    
    console.log(`  1KB 数据解码耗时: ${elapsed}ms`);
    assertEqual(decoded.length, 1024, '大数据解码结果');
});

console.log('\n=== 测试完成 ===\n');