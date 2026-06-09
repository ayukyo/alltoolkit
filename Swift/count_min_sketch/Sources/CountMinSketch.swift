// CountMinSketch.swift
// A probabilistic data structure for frequency estimation

import Foundation

public struct CountMinConfig {
    public let depth: Int
    public let width: Int
    public let seed: UInt64
    
    public init(depth: Int, width: Int, seed: UInt64 = 0xDEADBEEF) {
        self.depth = max(1, depth)
        self.width = max(2, width)
        self.seed = seed
    }
    
    // Create optimal config based on error rate and confidence
    public static func optimal(epsilon: Double, delta: Double) -> CountMinConfig {
        let width = Int Darwin.ceil(M_E / epsilon)
        let depth = Int Darwin.ceil(-Darwin.log(delta))
        return CountMinConfig(depth: max(1, depth), width: max(2, width))
    }
}

public final class CountMinSketch<T: Hashable> {
    private var table: [[UInt64]]
    private let config: CountMinConfig
    private var totalCount: UInt64
    
    public init(config: CountMinConfig) {
        self.config = config
        self.table = Array(repeating: Array(repeating: 0, count: config.width), count: config.depth)
        self.totalCount = 0
    }
    
    public convenience init(depth: Int, width: Int) {
        self.init(config: CountMinConfig(depth: depth, width: width))
    }
    
    public convenience init(epsilon: Double, delta: Double) {
        self.init(config: CountMinConfig(depth: 5, width: 100))
        let optimal = CountMinConfig.optimal(epsilon: epsilon, delta: delta)
        self.table = Array(repeating: Array(repeating: 0, count: optimal.width), count: optimal.depth)
    }
    
    public static func withRate(epsilon: Double, delta: Double) -> CountMinSketch<T> {
        let config = CountMinConfig.optimal(epsilon: epsilon, delta: delta)
        return CountMinSketch<T>(config: config)
    }
    
    // Update count for item by delta
    public func update(_ item: T, delta: UInt64) {
        let hashes = getHashes(item)
        for (i, h) in hashes.enumerated() {
            let idx = Int(h) % config.width
            table[i][idx] += delta
        }
        totalCount += delta
    }
    
    // Increment count by 1
    public func increment(_ item: T) {
        update(item, delta: 1)
    }
    
    // Estimate count (upper bound)
    public func estimate(_ item: T) -> UInt64 {
        let hashes = getHashes(item)
        var minVal: UInt64 = 0
        for (i, h) in hashes.enumerated() {
            let idx = Int(h) % config.width
            let val = table[i][idx]
            if i == 0 || val < minVal {
                minVal = val
            }
        }
        return minVal
    }
    
    public func totalCount() -> UInt64 {
        return totalCount
    }
    
    public func dimensions() -> (depth: Int, width: Int) {
        return (config.depth, config.width)
    }
    
    public func merge(other: CountMinSketch<T>) throws {
        guard config.depth == other.config.depth && config.width == other.config.width else {
            throw CMSError.dimensionMismatch
        }
        for i in 0..<config.depth {
            for j in 0..<config.width {
                table[i][j] += other.table[i][j]
            }
        }
        totalCount += other.totalCount
    }
    
    public func toBytes() -> [UInt8] {
        let size = 32 + config.depth * config.width * 8
        var bytes = [UInt8](repeating: 0, count: size)
        
        var offset = 0
        withUnsafeBytes(of: UInt64(config.depth).littleEndian) { bytes[offset..<offset+8] = $0; offset += 8 }
        withUnsafeBytes(of: UInt64(config.width).littleEndian) { bytes[offset..<offset+8] = $0; offset += 8 }
        withUnsafeBytes(of: config.seed.littleEndian) { bytes[offset..<offset+8] = $0; offset += 8 }
        withUnsafeBytes(of: totalCount.littleEndian) { bytes[offset..<offset+8] = $0; offset += 8 }
        
        for i in 0..<config.depth {
            for j in 0..<config.width {
                withUnsafeBytes(of: table[i][j].littleEndian) { bytes[offset..<offset+8] = $0; offset += 8 }
            }
        }
        return bytes
    }
    
    public static func fromBytes(_ bytes: [UInt8]) throws -> CountMinSketch<String> {
        guard bytes.count >= 32 else { throw CMSError.tooShort }
        
        let depth = Int(UInt64(littleEndian: bytes[0..<8].withUnsafeBytes { $0.load(as: UInt64.self) }))
        let width = Int(UInt64(littleEndian: bytes[8..<16].withUnsafeBytes { $0.load(as: UInt64.self) }))
        let seed = UInt64(littleEndian: bytes[16..<24].withUnsafeBytes { $0.load(as: UInt64.self) })
        let totalCount = UInt64(littleEndian: bytes[24..<32].withUnsafeBytes { $0.load(as: UInt64.self) })
        
        let expectedLen = 32 + depth * width * 8
        guard bytes.count >= expectedLen else { throw CMSError.invalidLength }
        
        let config = CountMinConfig(depth: depth, width: width, seed: seed)
        let sketch = CountMinSketch<String>(config: config)
        
        var offset = 32
        for i in 0..<depth {
            for j in 0..<width {
                let val = UInt64(littleEndian: bytes[offset..<offset+8].withUnsafeBytes { $0.load(as: UInt64.self) })
                sketch.table[i][j] = val
                offset += 8
            }
        }
        return sketch
    }
    
    public func clear() {
        for i in 0..<config.depth {
            for j in 0..<config.width {
                table[i][j] = 0
            }
        }
        totalCount = 0
    }
    
    private func getHashes(_ item: T) -> [UInt64] {
        var h1 = FNVHasher()
        h1.hash(item)
        let sum1 = h1.finalize()
        
        var h2 = FNVHasher()
        h2.hash(config.seed)
        h2.hash(item)
        let sum2 = h2.finalize()
        
        return (0..<config.depth).map { i in sum1 &+ UInt64(i) &* sum2 }
    }
}

public enum CMSError: Error {
    case dimensionMismatch
    case tooShort
    case invalidLength
}

import simd

struct FNVHasher {
    private var state: UInt64 = 0xcbf29ce484222325
    
    mutating func hash<H: Hashable>(_ value: H) {
        var hasher = _FNVHasher(state: &state)
        hasher.combine(value)
    }
    
    mutating func finalize() -> UInt64 {
        return state
    }
}

struct _FNVHasher {
    var state: UnsafeMutablePointer<UInt64>
    
    mutating func combine<T: Hashable>(_ value: T) {
        let bytes = withUnsafeBytes(of: ObjectIdentifier(String(describing: value))) { Array($0) }
        for byte in bytes {
            state.pointee = state.pointee &* 0x100000001b3 &+ UInt64(byte)
        }
    }
}