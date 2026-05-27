// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "LRUCache",
    targets: [
        .target(
            name: "LRUCache",
            path: ".",
            exclude: ["LRUCacheTests.swift", "main.swift"],
            sources: ["LRUCache.swift"]
        ),
        .testTarget(
            name: "LRUCacheTests",
            dependencies: ["LRUCache"],
            path: ".",
            exclude: ["LRUCache.swift", "main.swift", "README.md"],
            sources: ["LRUCacheTests.swift"]
        ),
        .executableTarget(
            name: "LRUCacheExample",
            dependencies: ["LRUCache"],
            path: ".",
            exclude: ["LRUCache.swift", "LRUCacheTests.swift", "README.md"],
            sources: ["main.swift"]
        )
    ]
)