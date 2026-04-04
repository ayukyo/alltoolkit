/**
 * Image Utilities - Swift Image Processing Toolkit
 *
 * A comprehensive image processing utility library for Swift.
 * Zero dependencies - uses only Apple Core Graphics and Foundation frameworks.
 *
 * Features:
 * - Image format conversion (PNG, JPEG, etc.)
 * - Image resizing and scaling
 * - Image cropping and rotation
 * - Color adjustments (brightness, contrast, saturation)
 * - Image filtering (blur, sharpen, edge detection)
 * - Image compositing and blending
 * - Base64 encoding/decoding for images
 * - Image metadata extraction
 *
 * Requirements: iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
 */

import Foundation
import CoreGraphics
import CoreImage
import UniformTypeIdentifiers

// MARK: - Image Format Enum

/**
 * Supported image formats for encoding/decoding
 */
public enum ImageFormat: String, CaseIterable {
    case png = "png"
    case jpeg = "jpg"
    case jpeg2000 = "jp2"
    case tiff = "tiff"
    case bmp = "bmp"
    case gif = "gif"
    case heic = "heic"

    public var utType: UTType? {
        switch self {
        case .png: return .png
        case .jpeg: return .jpeg
        case .jpeg2000: return .jpeg2000
        case .tiff: return .tiff
        case .bmp: return .bmp
        case .gif: return .gif
        case .heic: return .heic
        }
    }

    public var mimeType: String {
        switch self {
        case .png: return "image/png"
        case .jpeg: return "image/jpeg"
        case .jpeg2000: return "image/jp2"
        case .tiff: return "image/tiff"
        case .bmp: return "image/bmp"
        case .gif: return "image/gif"
        case .heic: return "image/heic"
        }
    }

    public var fileExtension: String {
        switch self {
        case .png: return "png"
        case .jpeg: return "jpg"
        case .jpeg2000: return "jp2"
        case .tiff: return "tiff"
        case .bmp: return "bmp"
        case .gif: return "gif"
        case .heic: return "heic"
        }
    }
}

// MARK: - Image Processing Error

public enum ImageProcessingError: Error, LocalizedError {
    case invalidImage
    case invalidData
    case unsupportedFormat
    case encodingFailed
    case decodingFailed
    case fileNotFound
    case saveFailed
    case invalidSize
    case filterApplicationFailed
    case cgContextCreationFailed

    public var errorDescription: String? {
        switch self {
        case .invalidImage: return "The image is invalid or corrupted"
        case .invalidData: return "The provided data is invalid"
        case .unsupportedFormat: return "The image format is not supported"
        case .encodingFailed: return "Failed to encode the image"
        case .decodingFailed: return "Failed to decode the image data"
        case .fileNotFound: return "The specified file was not found"
        case .saveFailed: return "Failed to save the image"
        case .invalidSize: return "The specified size is invalid"
        case .filterApplicationFailed: return "Failed to apply filter to image"
        case .cgContextCreationFailed: return "Failed to create graphics context"
        }
    }
}

// MARK: - ImageInfo

public struct ImageInfo {
    public let width: Int
    public let height: Int
    public let sizeInBytes: Int
    public let format: ImageFormat?
    public let hasAlpha: Bool
    public let bitsPerComponent: Int
    public let colorSpace: String?

    public var aspectRatio: Double {
        return Double(width) / Double(height)
    }

    public var megapixels: Double {
        return Double(width * height) / 1_000_000.0
    }
}

// MARK: - ResizeMode

public enum ResizeMode {
    case fit      // Fit within bounds, maintain aspect ratio
    case fill     // Fill bounds, maintain aspect ratio (may crop)
    case stretch  // Stretch to exact size
}

// MARK: - ImageUtils

public final class ImageUtils {

    public init() {}

    // MARK: - Image Loading

    public func load(from path: String) throws -> CGImage {
        guard FileManager.default.fileExists(atPath: path) else {
            throw ImageProcessingError.fileNotFound
        }

        guard let data = FileManager.default.contents(atPath: path),
              let image = createImage(from: data) else {
            throw ImageProcessingError.decodingFailed
        }

        return image
    }

    public func load(from url: URL) throws -> CGImage {
        guard let data = try? Data(contentsOf: url),
              let image = createImage(from: data) else {
            throw ImageProcessingError.decodingFailed
        }

        return image
    }

    public func load(from data: Data) throws -> CGImage {
        guard let image = createImage(from: data) else {
            throw ImageProcessingError.decodingFailed
        }

        return image
    }

    private func createImage(from data: Data) -> CGImage? {
        guard let source = CGImageSourceCreateWithData(data as CFData, nil) else {
            return nil
        }
        return CGImageSourceCreateImageAtIndex(source, 0, nil)
    }

    // MARK: - Image Saving

    public func save(_ image: CGImage, to path: String, format: ImageFormat = .png, quality: Double = 0.9) throws {
        let url = URL(fileURLWithPath: path)
        try save(image, to: url, format: format, quality: quality)
    }

    public func save(_ image: CGImage, to url: URL, format: ImageFormat = .png, quality: Double = 0.9) throws {
        guard let data = encode(image, format: format, quality: quality) else {
            throw ImageProcessingError.encodingFailed
        }

        do {
            try data.write(to: url)
        } catch {
            throw ImageProcessingError.saveFailed
        }
    }

    public func encode(_ image: CGImage, format: ImageFormat = .png, quality: Double = 0.9) -> Data? {
        let utType = format.utType?.identifier ?? UTType.png.identifier

        guard let mutableData = CFDataCreateMutable(nil, 0),
              let destination = CGImageDestinationCreateWithData(mutableData, utType as CFString, 1, nil) else {
            return nil
        }

        if format == .jpeg {
            let properties = [
                kCGImageDestinationLossyCompressionQuality: max(0.0, min(1.0, quality))
            ] as CFDictionary
            CGImageDestinationSetProperties(destination, properties)
        }

        CGImageDestinationAddImage(destination, image, nil)

        guard CGImageDestinationFinalize(destination) else {
            return nil
        }

        return mutableData as Data
    }

    // MARK: - Image Information

    public func getInfo(_ image: CGImage, data: Data? = nil) -> ImageInfo {
        return ImageInfo(
            width: image.width,
            height: image.height,
            sizeInBytes: data?.count ?? 0,
            format: nil,
            hasAlpha: image.alphaInfo != .none,
            bitsPerComponent: image.bitsPerComponent,
            colorSpace: image.colorSpace?.name as String?
        )
    }

    public func getInfo(from path: String) throws -> ImageInfo {
        guard FileManager.default.fileExists(atPath: path) else {
            throw ImageProcessingError.fileNotFound
        }

        let data = FileManager.default.contents(atPath: path) ?? Data()
        let image = try load(from: path)
        return getInfo(image, data: data)
    }

    // MARK: - Image Resizing

    public func resize(_ image: CGImage, width: Int, height: Int, mode: ResizeMode = .fit) -> CGImage? {
        let originalWidth = CGFloat(image.width)
        let originalHeight = CGFloat(image.height)
        let targetWidth = CGFloat(width)
        let targetHeight = CGFloat(height)

        var newWidth = targetWidth
        var newHeight = targetHeight

        switch mode {
        case .fit:
            let scale = min(targetWidth / originalWidth, targetHeight / originalHeight)
            newWidth = originalWidth * scale
            newHeight = originalHeight * scale
        case .fill:
            let scale = max(targetWidth / originalWidth, targetHeight / originalHeight)
            newWidth = originalWidth * scale
            newHeight = originalHeight * scale
        case .stretch:
            break
        }

        return resizeToSize(image, width: Int(newWidth), height: Int(newHeight))
    }

    public func resizeToWidth(_ image: CGImage, width: Int) -> CGImage? {
        let scale = CGFloat(width) / CGFloat(image.width)
        let height = Int(CGFloat(image.height) * scale)
        return resizeToSize(image, width: width, height: height)
    }

    public func resizeToHeight(_ image: CGImage, height: Int) -> CGImage? {
        let scale = CGFloat(height) / CGFloat(image.height)
        let width = Int(CGFloat(image.width) * scale)
        return resizeToSize(image, width: width, height: height)
    }

    public func resizeToSize(_ image: CGImage, width: Int, height: Int) -> CGImage? {
        guard width > 0, height > 0 else { return nil }

        let colorSpace = image.colorSpace ?? CGColorSpaceCreateDeviceRGB()
        let bitmapInfo = CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedLast.rawValue)

        guard let context = CGContext(
            data: nil,
            width: width,
            height: height,
            bitsPerComponent: 8,
            bytesPerRow: 0,
            space: colorSpace,
            bitmapInfo: bitmapInfo.rawValue
        ) else {
            return nil
        }

        context.interpolationQuality = .high
        context.draw(image, in: CGRect(x: 0, y: 0, width: width, height: height))

        return context.makeImage()
    }

    // MARK: - Image Cropping

    public func crop(_ image: CGImage, rect: CGRect) -> CGImage? {
        return image.cropping(to: rect)
    }

    public func crop(_ image: CGImage, x: Int, y: Int, width: Int, height: Int) -> CGImage? {
        let rect = CGRect(x: x, y: y, width: width, height: height)
        return crop(image, rect: rect)
    }

    public func cropToSquare(_ image: CGImage) -> CGImage? {
        let size = min(image.width, image.height)
        let x = (image.width - size) / 2
        let y = (image.height - size) / 2
        return crop(image, x: x, y: y, width: size, height: size)
    }

    // MARK: - Image Rotation

    public func rotate(_ image: CGImage, degrees: Double) -> CGImage? {
        let radians = degrees * .pi / 180.0
        return rotate(image, radians: radians)
    }

    public func rotate(_ image: CGImage, radians: Double) -> CGImage? {
        let width = image.width
        let height = image.height

        let colorSpace = image.colorSpace ?? CGColorSpaceCreateDeviceRGB()
        let bitmapInfo = CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedLast.rawValue)

        guard let context = CGContext(
            data: nil,
            width: width,
            height: height,
            bitsPerComponent: 8,
            bytesPerRow: 0,
            space: colorSpace,
            bitmapInfo: bitmapInfo.rawValue
        ) else {
            return nil
        }

        context.translateBy(x: CGFloat(width) / 2, y: CGFloat(height) / 2)
        context.rotate(by: CGFloat(radians))
        context.translateBy(x: -CGFloat(width) / 2, y: -CGFloat(height) / 2)
        context.draw(image, in: CGRect(x: 0, y: 0, width: width, height: height))

        return context.makeImage()
    }

    public func flipHorizontal(_ image: CGImage) -> CGImage? {
        return flip(image, horizontally: true, vertically: false)
    }

    public func flipVertical(_ image: CGImage) -> CGImage? {
        return flip(image, horizontally: false, vertically: true)
    }

    private func flip(_ image: CGImage, horizontally: Bool, vertically: Bool) -> CGImage? {
        let width = image.width
        let height = image.height

        let colorSpace = image.colorSpace ?? CGColorSpaceCreateDeviceRGB()
        let bitmapInfo = CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedLast.rawValue)

        guard let context = CGContext(
            data: nil,
            width: width,
            height: height,
            bitsPerComponent: 8,
            bytesPerRow: 0,
            space: colorSpace,
            bitmapInfo: bitmapInfo.rawValue
        ) else {
            return nil
        }

        context.translateBy(x: horizontally ? CGFloat(width) : 0, y: vertically ? CGFloat(height) : 0)
        context.scaleBy(x: horizontally ? -1 : 1, y: vertically ? -1 : 1)
        context.draw(image, in: CGRect(x: 0, y: 0, width: width, height: height))

        return context.makeImage()
    }

    // MARK: - Image Filters

    public func applyBlur(_ image: CGImage, radius: Double) -> CGImage? {
        guard let ciImage = CIImage(cgImage: image) else { return nil }

        let filter = CIFilter(name: "CIGaussianBlur")
        filter?.setValue(ciImage, forKey: kCIInputImageKey)
        filter?.setValue(radius, forKey: kCIInputRadiusKey)

        guard let outputImage = filter?.outputImage,
              let cgImage = CIContext().createCGImage(outputImage, from: outputImage.extent) else {
            return nil
        }

        return cgImage
    }

    public func applySharpen(_ image: CGImage, intensity: Double = 0.5) -> CGImage? {
        guard let ciImage = CIImage(cgImage: image) else { return nil }

        let filter = CIFilter(name: "CISharpenLuminance")
        filter?.setValue(ciImage, forKey: kCIInputImageKey)
        filter?.setValue(intensity, forKey: kCIInputSharpnessKey)

        guard let outputImage = filter?.outputImage,
              let cgImage = CIContext().createCGImage(outputImage, from: outputImage.extent) else {
            return nil
        }

        return cgImage
    }

    public func adjustBrightness(_ image: CGImage, amount: Double) -> CGImage? {
        guard let ciImage = CIImage(cgImage: image) else { return nil }

        let filter = CIFilter(name: "CIExposureAdjust")
        filter?.setValue(ciImage, forKey: kCIInputImageKey)
        filter?.setValue(amount, forKey: kCIInputEVKey)

        guard let outputImage = filter?.outputImage,
              let cgImage = CIContext().createCGImage(outputImage, from: outputImage.extent) else {
            return nil
        }

        return cgImage
    }

    public func adjustContrast(_ image: CGImage, amount: Double) -> CGImage? {
        guard let ciImage = CIImage(cgImage: image) else { return nil }

        let filter = CIFilter(name: "CIColorControls")
        filter?.setValue(ciImage, forKey: kCIInputImageKey)
        filter?.setValue(amount, forKey: kCIInputContrastKey)

        guard let outputImage = filter?.outputImage,
              let cgImage = CIContext().createCGImage(outputImage, from: outputImage.extent) else {
            return nil
        }

        return cgImage
    }

    public func adjustSaturation(_ image: CGImage, amount: Double) -> CGImage? {
        guard let ciImage = CIImage(cgImage: image) else { return nil }

        let filter = CIFilter(name: "CIColorControls")
        filter?.setValue(ciImage, forKey: kCIInputImageKey)
        filter?.setValue(amount, forKey: kCIInputSaturationKey)

        guard let outputImage = filter?.outputImage,
              let cgImage = CIContext().createCGImage(outputImage, from: outputImage.extent) else {
            return nil
        }

        return cgImage
    }

    public func applyGrayscale(_ image: CGImage) -> CGImage? {
        guard let ciImage = CIImage(cgImage: image) else { return nil }

        let filter = CIFilter(name: "CIPhotoEffectMono")
        filter?.setValue(ciImage, forKey: kCIInputImageKey)

        guard let outputImage = filter?.outputImage,
              let cgImage = CIContext().createCGImage(outputImage, from: outputImage.extent) else {
            return nil
        }

        return cgImage
    }

    public func applySepia(_ image: CGImage, intensity: Double = 1.0) -> CGImage? {
        guard let ciImage = CIImage(cgImage: image) else { return nil }

        let filter = CIFilter(name: "CISepiaTone")
        filter?.setValue(ciImage, forKey: kCIInputImageKey)
        filter?.setValue(intensity, forKey: kCIInputIntensityKey)

        guard let outputImage = filter?.outputImage,
              let cgImage = CIContext().createCGImage(outputImage, from: outputImage.extent) else {
            return nil
        }

        return cgImage
    }

    // MARK: - Image Composition

    public func composite(_ baseImage: CGImage, with overlayImage: CGImage, at point: CGPoint) -> CGImage? {
        let width = baseImage.width
        let height = baseImage.height

        let colorSpace = baseImage.colorSpace ?? CGColorSpaceCreateDeviceRGB()
        let bitmapInfo = CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedLast.rawValue)

        guard let context = CGContext(
            data: nil,
            width: width,
            height: height,
            bitsPerComponent: 8,
            bytesPerRow: 0,
            space: colorSpace,
            bitmapInfo: bitmapInfo.rawValue
        ) else {
            return nil
        }

        context.draw(baseImage, in: CGRect(x: 0, y: 0, width: width, height: height))
        context.draw(overlayImage, in: CGRect(x: Int(point.x), y: Int(point.y), width: overlayImage.width, height: overlayImage.height))

        return context.makeImage()
    }

    public func createThumbnail(_ image: CGImage, size: Int) -> CGImage? {
        return resize(image, width: size, height: size, mode: .fill)
    }

    // MARK: - Base64 Encoding

    public func toBase64(_ image: CGImage, format: ImageFormat = .png, quality: Double = 0.9) -> String? {
        guard let data = encode(image, format: format, quality: quality) else {
            return nil
        }
        return data.base64EncodedString()
    }

    public func fromBase64(_ base64String: String) -> CGImage? {
        guard let data = Data(base64Encoded: base64String) else {
            return nil
        }
        return createImage(from: data)
    }

    // MARK: - Image Comparison

    public func isSameSize(_ image1: CGImage, _ image2: CGImage) -> Bool {
        return image1.width == image2.width && image1.height == image2.height
    }

    public func calculateSimilarity(_ image1: CGImage, _ image2: CGImage) -> Double? {
        guard isSameSize(image1, image2) else { return nil }

        let width = image1.width
        let height = image1.height

        guard let data1 = image1.dataProvider?.data as Data?,
              let data2 = image2.dataProvider?.data as Data? else {
            return nil
        }

        let bytes1 = [UInt8](data1)
        let bytes2 = [UInt8](data2)

        guard bytes1.count == bytes2.count else { return nil }

        var diff: Double = 0
        for i in 0..<min(bytes1.count, bytes2.count) {
            diff += Double(abs(Int(bytes1[i]) - Int(bytes2[i])))
        }

        let maxDiff = Double(bytes1.count * 255)
        return 1.0 - (diff / maxDiff)
    }

    // MARK: - Utility Functions

    public func createSolidImage(width: Int, height: Int, color: CGColor) -> CGImage? {
        let colorSpace = CGColorSpaceCreateDeviceRGB()
        let bitmapInfo = CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedLast.rawValue)

        guard let context = CGContext(
            data: nil,
            width: width,
            height: height,
            bitsPerComponent: 8,
            bytesPerRow: 0,
            space: colorSpace,
            bitmapInfo: bitmapInfo.rawValue
        ) else {
            return nil
        }

        context.setFillColor(color)
        context.fill(CGRect(x: 0, y: 0, width: width, height: height))

        return context.makeImage()
    }

    public func createPlaceholderImage(width: Int, height: Int, text: String = "\(width)x\(height)") -> CGImage? {
        let colorSpace = CGColorSpaceCreateDeviceRGB()
        let bitmapInfo = CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedLast.rawValue)

        guard let context = CGContext(
            data: nil,
            width: width,
            height: height,
            bitsPerComponent: 8,
            bytesPerRow: 0,
            space: colorSpace,
            bitmapInfo: bitmapInfo.rawValue
        ) else {
            return nil
        }

        // Draw gray background
        context.setFillColor(CGColor(red: 0.9, green: 0.9, blue: 0.9, alpha: 1.0))
        context.fill(CGRect(x: 0, y: 0, width: width, height: height))

        // Draw border
        context.setStrokeColor(CGColor(red: 0.7, green: 0.7, blue: 0.7, alpha: 1.0))
        context.setLineWidth(2)
        context.stroke(CGRect(x: 1, y: 1, width: width - 2, height: height - 2))

        return context.makeImage()
    }
}

// MARK: - Static Methods

public extension ImageUtils {

    static func load(from path: String) throws -> CGImage {
        return try ImageUtils().load(from: path)
    }

    static func load(from url: URL) throws -> CGImage {
        return try ImageUtils().load(from: url)
    }

    static func load(from data: Data) throws -> CGImage {
        return try ImageUtils().load(from: data)
    }

    static func save(_ image: CGImage, to path: String, format: ImageFormat = .png, quality: Double = 0.9) throws {
        try ImageUtils().save(image, to: path, format: format, quality: quality)
    }

    static func resize(_ image: CGImage, width: Int, height: Int, mode: ResizeMode = .fit) -> CGImage? {
        return ImageUtils().resize(image, width: width, height: height, mode: mode)
    }

    static func crop(_ image: CGImage, x: Int, y: Int, width: Int, height: Int) -> CGImage? {
        return ImageUtils().crop(image, x: x, y: y, width: width, height: height)
    }

    static func rotate(_ image: CGImage, degrees: Double) -> CGImage? {
        return ImageUtils().rotate(image, degrees: degrees)
    }

    static func toBase64(_ image: CGImage, format: ImageFormat = .png) -> String? {
        return ImageUtils().toBase64(image, format: format)
    }

    static func fromBase64(_ base64String: String) -> CGImage? {
        return ImageUtils().fromBase64(base64String)
    }
}
