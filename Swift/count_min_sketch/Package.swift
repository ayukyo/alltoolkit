// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "CountMinSketch",
    targets: [.target(name: "CountMinSketch", dependencies: [], path: "Sources")],
    swiftLanguageVersions: [.v5]
)