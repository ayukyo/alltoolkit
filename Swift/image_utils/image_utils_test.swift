/**
 * Image Utilities Test Suite
 *
 * Comprehensive tests for the ImageUtils module.
 * Run with: swift test (in a Swift Package Manager project)
 */

import XCTest
import CoreGraphics
@testable import ImageUtils

final class ImageUtilsTests: XCTestCase {

    var utils: ImageUtils!

    override func setUp() {
        super.setUp()
        utils = ImageUtils()
    }

    override func tearDown() {
        utils = nil
        super.tearDown()
    }

    // MARK: - Test Helpers

    func createTestImage(width: Int = 100, height: Int = 100) -> CGImage? {
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

        context.setFillColor(CGColor(red: 1.0, green: 0.0, blue: 0.0, alpha: 1.0))
        context.fill(CGRect(x: 0, y: 0, width: width, height: height))

        return context.makeImage()
    }

    // MARK: - Image Format Tests

    func testImageFormatProperties() {
        XCTAssertEqual(ImageFormat.png.mimeType, "image/png")
        XCTAssertEqual(ImageFormat.jpeg.mimeType, "image/jpeg")
        XCTAssertEqual(ImageFormat.png.fileExtension, "png")
        XCTAssertEqual(ImageFormat.jpeg.fileExtension, "jpg")
    }

    func testAllImageFormats() {
        let formats: [ImageFormat] = [.png, .jpeg, .tiff, .bmp, .gif]
        for format in formats {
            XCTAssertNotNil(format.utType)
            XCTAssertFalse(format.mimeType.isEmpty)
            XCTAssertFalse(format.fileExtension.isEmpty)
        }
    }

    // MARK: - Image Creation Tests

    func testCreateTestImage() {
        let image = createTestImage(width: 200, height: 150)
        XCTAssertNotNil(image)
        XCTAssertEqual(image?.width, 200)
        XCTAssertEqual(image?.height, 150)
    }

    func testCreateSolidImage() {
        let color = CGColor(red: 0.5, green: 0.5, blue: 0.5, alpha: 1.0)
        let image = utils.createSolidImage(width: 100, height: 100, color: color)
        XCTAssertNotNil(image)
        XCTAssertEqual(image?.width, 100)
        XCTAssertEqual(image?.height, 100)
    }

    func testCreatePlaceholderImage() {
        let image = utils.createPlaceholderImage(width: 200, height: 100, text: "Test")
        XCTAssertNotNil(image)
        XCTAssertEqual(image?.width, 200)
        XCTAssertEqual(image?.height, 100)
    }

    // MARK: - Image Info Tests

    func testGetImageInfo() {
        let image = createTestImage(width: 1920, height: 1080)
        XCTAssertNotNil(image)

        let info = utils.getInfo(image!)
        XCTAssertEqual(info.width, 1920)
        XCTAssertEqual(info.height, 1080)
        XCTAssertEqual(info.aspectRatio, 1920.0 / 1080.0, accuracy: 0.001)
        XCTAssertEqual(info.megapixels, 2.0736, accuracy: 0.001)
    }

    // MARK: - Image Resizing Tests

    func testResizeToSize() {
        let image = createTestImage(width: 200, height: 100)
        XCTAssertNotNil(image)

        let resized = utils.resizeToSize(image!, width: 100, height: 50)
        XCTAssertNotNil(resized)
        XCTAssertEqual(resized?.width, 100)
        XCTAssertEqual(resized?.height, 50)
    }

    func testResizeToWidth() {
        let image = createTestImage(width: 200, height: 100)
        XCTAssertNotNil(image)

        let resized = utils.resizeToWidth(image!, width: 100)
        XCTAssertNotNil(resized)
        XCTAssertEqual(resized?.width, 100)
        XCTAssertEqual(resized?.height, 50)
    }

    func testResizeToHeight() {
        let image = createTestImage(width: 200, height: 100)
        XCTAssertNotNil(image)

        let resized = utils.resizeToHeight(image!, height: 50)
        XCTAssertNotNil(resized)
        XCTAssertEqual(resized?.width, 100)
        XCTAssertEqual(resized?.height, 50)
    }

    func testResizeWithFitMode() {
        let image = createTestImage(width: 200, height: 100)
        XCTAssertNotNil(image)

        let resized = utils.resize(image!, width: 100, height: 100, mode: .fit)
        XCTAssertNotNil(resized)
        XCTAssertEqual(resized?.width, 100)
        XCTAssertEqual(resized?.height, 50)
    }

    func testResizeWithFillMode() {
        let image = createTestImage(width: 200, height: 100)
        XCTAssertNotNil(image)

        let resized = utils.resize(image!, width: 100, height: 100, mode: .fill)
        XCTAssertNotNil(resized)
        XCTAssertEqual(resized?.width, 200)
        XCTAssertEqual(resized?.height, 100)
    }

    func testResizeWithStretchMode() {
        let image = createTestImage(width: 200, height: 100)
        XCTAssertNotNil(image)

        let resized = utils.resize(image!, width: 100, height: 100, mode: .stretch)
        XCTAssertNotNil(resized)
        XCTAssertEqual(resized?.width, 100)
        XCTAssertEqual(resized?.height, 100)
    }

    func testResizeInvalidSize() {
        let image = createTestImage()
        XCTAssertNotNil(image)

        let resized = utils.resizeToSize(image!, width: 0, height: 100)
        XCTAssertNil(resized)
    }

    // MARK: - Image Cropping Tests

    func testCropImage() {
        let image = createTestImage(width: 200, height: 200)
        XCTAssertNotNil(image)

        let cropped = utils.crop(image!, x: 50, y: 50, width: 100, height: 100)
        XCTAssertNotNil(cropped)
        XCTAssertEqual(cropped?.width, 100)
        XCTAssertEqual(cropped?.height, 100)
    }

    func testCropToSquare() {
        let image = createTestImage(width: 200, height: 100)
        XCTAssertNotNil(image)

        let cropped = utils.cropToSquare(image!)
        XCTAssertNotNil(cropped)
        XCTAssertEqual(cropped?.width, 100)
        XCTAssertEqual(cropped?.height, 100)
    }

    func testCropWithRect() {
        let image = createTestImage(width: 200, height: 200)
        XCTAssertNotNil(image)

        let rect = CGRect(x: 25, y: 25, width: 50, height: 50)
        let cropped = utils.crop(image!, rect: rect)
        XCTAssertNotNil(cropped)
        XCTAssertEqual(cropped?.width, 50)
        XCTAssertEqual(cropped?.height, 50)
    }

    // MARK: - Image Rotation Tests

    func testRotateImage() {
        let image = createTestImage(width: 100, height: 100)
        XCTAssertNotNil(image)

        let rotated = utils.rotate(image!, degrees: 90)
        XCTAssertNotNil(rotated)
        XCTAssertEqual(rotated?.width, 100)
        XCTAssertEqual(rotated?.height, 100)
    }

    func testRotateImageRadians() {
        let image = createTestImage(width: 100, height: 100)
        XCTAssertNotNil(image)

        let rotated = utils.rotate(image!, radians: .pi / 2)
        XCTAssertNotNil(rotated)
    }

    func testFlipHorizontal() {
        let image = createTestImage()
        XCTAssertNotNil(image)

        let flipped = utils.flipHorizontal(image!)
        XCTAssertNotNil(flipped)
        XCTAssertEqual(flipped?.width, image?.width)
        XCTAssertEqual(flipped?.height, image?.height)
    }

    func testFlipVertical() {
        let image = createTestImage()
        XCTAssertNotNil(image)

        let flipped = utils.flipVertical(image!)
        XCTAssertNotNil(flipped)
        XCTAssertEqual(flipped?.width, image?.width)
        XCTAssertEqual(flipped?.height, image?.height)
    }

    // MARK: - Image Filter Tests

    func testApplyBlur() {
        let image = createTestImage()
        XCTAssertNotNil(image)

        let blurred = utils.applyBlur(image!, radius: 5.0)
        XCTAssertNotNil(blurred)
