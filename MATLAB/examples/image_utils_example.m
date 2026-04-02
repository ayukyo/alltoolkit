%% Image Utils Example
%   Demonstrates the usage of image_utils module functions
%   Run this script to see examples of all available functions

clear; clc;

% Initialize the module
utils = mod();
fprintf('Image Utils Example - MATLAB Image Processing Toolkit\n');
fprintf('=====================================================\n\n');

%% Example 1: Create a test image and convert to grayscale
fprintf('Example 1: RGB to Grayscale Conversion\n');
% Create a simple RGB test image
rgbImg = uint8(zeros(100, 100, 3));
rgbImg(:, :, 1) = 255;  % Red channel
rgbImg(:, :, 2) = 128;  % Green channel
rgbImg(:, :, 3) = 64;   % Blue channel

grayImg = utils.rgb2gray(rgbImg);
fprintf('  Original RGB size: %dx%dx%d\n', size(rgbImg, 1), size(rgbImg, 2), size(rgbImg, 3));
fprintf('  Grayscale size: %dx%d\n', size(grayImg, 1), size(grayImg, 2));
fprintf('\n');

%% Example 2: Image resizing
fprintf('Example 2: Image Resizing\n');
original = uint8(rand(200, 200, 3) * 255);
resized = utils.resize(original, [100, 100]);
fprintf('  Original size: %dx%d\n', size(original, 1), size(original, 2));
fprintf('  Resized to: %dx%d\n', size(resized, 1), size(resized, 2));
fprintf('\n');

%% Example 3: Image cropping
fprintf('Example 3: Image Cropping\n');
img = uint8(rand(300, 400, 3) * 255);
cropped = utils.crop(img, [50, 50, 200, 150]);
fprintf('  Original size: %dx%d\n', size(img, 1), size(img, 2));
fprintf('  Cropped region: [50, 50, 200, 150]\n');
fprintf('  Result size: %dx%d\n', size(cropped, 1), size(cropped, 2));
fprintf('\n');

%% Example 4: Image rotation
fprintf('Example 4: Image Rotation\n');
img = uint8(ones(100, 100, 3) * 200);
img(40:60, 40:60, :) = 100;  % Add a square
rotated = utils.rotate(img, 45);
fprintf('  Rotated image by 45 degrees\n');
fprintf('  Size preserved: %dx%d\n', size(rotated, 1), size(rotated, 2));
fprintf('\n');

%% Example 5: Image flipping
fprintf('Example 5: Image Flipping\n');
img = uint8(reshape(1:100, 10, 10));
flippedH = utils.flip(img, 'horizontal');
flippedV = utils.flip(img, 'vertical');
fprintf('  Original top-left: %d\n', img(1, 1));
fprintf('  Horizontal flip top-right: %d\n', flippedH(1, 10));
fprintf('  Vertical flip bottom-left: %d\n', flippedV(10, 1));
fprintf('\n');

%% Example 6: Blur filter
fprintf('Example 6: Box Blur Filter\n');
img = uint8(zeros(50, 50, 3));
img(20:30, 20:30, :) = 255;  % White square
blurred = utils.blur(img, 5);
fprintf('  Applied 5x5 box blur\n');
fprintf('  Original has sharp edges, blurred has soft edges\n');
fprintf('\n');

%% Example 7: Gaussian blur
fprintf('Example 7: Gaussian Blur Filter\n');
img = uint8(zeros(50, 50, 3));
img(25, 25, :) = 255;  % Single bright pixel
gaussian = utils.gaussianFilter(img, 2.0);
fprintf('  Applied Gaussian blur with sigma=2.0\n');
fprintf('  Single pixel spread into Gaussian distribution\n');
fprintf('\n');

%% Example 8: Edge detection
fprintf('Example 8: Edge Detection\n');
img = uint8(ones(50, 50) * 128);
img(20:30, :) = 0;     % Black stripe
img(31:40, :) = 255;   % White stripe
edges = utils.edgeDetect(img, 'sobel');
fprintf('  Detected edges using Sobel operator\n');
fprintf('  Edge image size: %dx%d\n', size(edges, 1), size(edges, 2));
fprintf('\n');

%% Example 9: Brightness adjustment
fprintf('Example 9: Brightness Adjustment\n');
img = uint8(ones(50, 50, 3) * 100);
brighter = utils.brightness(img, 0.3);
darker = utils.brightness(img, -0.3);
fprintf('  Original value: %d\n', img(1, 1, 1));
fprintf('  Brightened (+0.3): %d\n', brighter(1, 1, 1));
fprintf('  Darkened (-0.3): %d\n', darker(1, 1, 1));
fprintf('\n');

%% Example 10: Contrast adjustment
fprintf('Example 10: Contrast Adjustment\n');
img = uint8(ones(50, 50, 3) * 128);
highContrast = utils.contrast(img, 2.0);
lowContrast = utils.contrast(img, 0.5);
fprintf('  Applied contrast factors: 2.0 (high) and 0.5 (low)\n');
fprintf('\n');

%% Example 11: Gamma correction
fprintf('Example 11: Gamma Correction\n');
img = uint8(ones(50, 50, 3) * 128);
gamma1 = utils.gamma(img, 0.5);  % Brighten midtones
gamma2 = utils.gamma(img, 2.2);  % Darken midtones
fprintf('  Gamma 0.5: Brightens midtones\n');
fprintf('  Gamma 2.2: Darkens midtones (standard)\n');
fprintf('\n');

%% Example 12: Histogram equalization
fprintf('Example 12: Histogram Equalization\n');
img = uint8(reshape(1:256, 16, 16));
equalized = utils.equalizeHist(img);
fprintf('  Applied histogram equalization\n');
fprintf('  Original range: %d to %d\n', min(img(:)), max(img(:)));
fprintf('  Equalized range: %d to %d\n', min(equalized(:)), max(equalized(:)));
fprintf('\n');

%% Example 13: Color space conversion (RGB <-> HSV)
fprintf('Example 13: RGB to HSV Conversion\n');
rgb = uint8(zeros(50, 50, 3));
rgb(:, :, 1) = 255;  % Pure red
hsv = utils.rgb2hsv(rgb);
rgb_back = utils.hsv2rgb(hsv);
fprintf('  Converted RGB to HSV and back\n');
fprintf('  HSV Hue (should be ~0 for red): %.1f\n', hsv(1, 1, 1));
fprintf('  HSV Saturation: %.2f\n', hsv(1, 1, 2));
fprintf('  HSV Value: %.2f\n', hsv(1, 1, 3));
fprintf('\n');

%% Example 14: Image thresholding
fprintf('Example 14: Image Thresholding\n');
img = uint8(reshape(1:100, 10, 10));
binary = utils.threshold(img, 50);
fprintf('  Applied threshold at 50\n');
fprintf('  Values <= 50: %d pixels\n', sum(binary(:) == 0));
fprintf('  Values > 50: %d pixels\n', sum(binary(:) == 1));
fprintf('\n');

%% Example 15: Image inversion
fprintf('Example 15: Image Inversion\n');
img = uint8(ones(50, 50, 3) * 200);
inverted = utils.invert(img);
fprintf('  Original value: %d\n', img(1, 1, 1));
fprintf('  Inverted value: %d\n', inverted(1, 1, 1));
fprintf('  Sum (should be 255): %d\n', img(1,1,1) + inverted(1,1,1));
fprintf('\n');

%% Example 16: Image blending
fprintf('Example 16: Image Blending\n');
img1 = uint8(ones(50, 50, 3) * 100);
img2 = uint8(ones(50, 50, 3) * 200);
blended1 = utils.blend(img1, img2, 0.5);  % 50-50 blend
blended2 = utils.blend(img1, img2, 0.8);  % 80-20 blend
fprintf('  Image 1 value: %d\n', img1(1, 1, 1));
fprintf('  Image 2 value: %d\n', img2(1, 1, 1));
fprintf('  50-50 blend: %d\n', blended1(1, 1, 1));
fprintf('  80-20 blend: %d\n', blended2(1, 1, 1));
fprintf('\n');

%% Example 17: Image analysis functions
fprintf('Example 17: Image Analysis\n');
img = uint8(rand(100, 200, 3) * 255);
sz = utils.getSize(img);
ch = utils.getChannels(img);
isGray = utils.isGrayscale(img);
fprintf('  Image size: %dx%dx%d\n', sz(1), sz(2), sz(3));
fprintf('  Number of channels: %d\n', ch);
fprintf('  Is grayscale: %d\n', isGray);
fprintf('\n');

%% Example 18: Histogram calculation
fprintf('Example 18: Histogram Calculation\n');
img = uint8(ones(100, 100) * 128);
img(1:50, :) = 64;
img(51:100, :) = 192;
hist = utils.getHistogram(img, 256);
fprintf('  Calculated histogram with 256 bins\n');
fprintf('  Bin 65 count: %d\n', hist(65));
fprintf('  Bin 129 count: %d\n', hist(129));
fprintf('  Bin 193 count: %d\n', hist(193));
fprintf('\n');

%% Example 19: Image padding
fprintf('Example 19: Image Padding\n');
img = uint8(ones(50, 50, 3) * 128);
padded = utils.padImage(img, [10, 10]);
fprintf('  Original size: %dx%d\n', size(img, 1), size(img, 2));
fprintf('  Padded size: %dx%d\n', size(padded, 1), size(padded, 2));
fprintf('\n');

%% Example 20: Image normalization
fprintf('Example 20: Image Normalization\n');
img = uint8([0, 64, 128, 192, 255]);
normalized = utils.normalize(img, 0, 1);
fprintf('  Original: [%d, %d, %d, %d, %d]\n', img);
fprintf('  Normalized: [%.2f, %.2f, %.2f, %.2f, %.2f]\n', normalized);
fprintf('\n');

%% Summary
fprintf('=====================================================\n');
fprintf('All examples completed successfully!\n');
fprintf('=====================================================\n');
fprintf('Available functions in image_utils:\n');
fprintf('  Color: rgb2gray, gray2rgb, rgb2hsv, hsv2rgb\n');
fprintf('  Transform: resize, crop, rotate, flip\n');
fprintf('  Filter: blur, sharpen, edgeDetect, gaussianFilter\n');
fprintf('  Enhance: brightness, contrast, gamma, equalizeHist\n');
fprintf('  Analysis: getSize, getChannels, isGrayscale, getHistogram\n');
fprintf('  Utility: padImage, normalize, invert, threshold, blend\n');
fprintf('\nFor more details, see mod.m source code.\n');