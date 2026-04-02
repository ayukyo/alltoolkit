function image_utils_test()
%IMAGE_UTILS_TEST Test suite for image_utils module
%   Run all tests and display results

    fprintf('========================================\n');
    fprintf('Image Utils Test Suite\n');
    fprintf('========================================\n\n');
    
    utils = mod();
    passed = 0;
    failed = 0;
    
    % Test 1: RGB to Grayscale conversion
    try
        rgb = uint8(ones(10, 10, 3) * 128);
        gray = utils.rgb2gray(rgb);
        assert(size(gray, 3) == 1, 'Grayscale should have 1 channel');
        assert(size(gray, 1) == 10 && size(gray, 2) == 10, 'Size should be preserved');
        fprintf('✓ Test 1: RGB to Grayscale - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 1: RGB to Grayscale - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 2: Grayscale to RGB conversion
    try
        gray = uint8(ones(10, 10) * 128);
        rgb = utils.gray2rgb(gray);
        assert(size(rgb, 3) == 3, 'RGB should have 3 channels');
        fprintf('✓ Test 2: Grayscale to RGB - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 2: Grayscale to RGB - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 3: Image resize
    try
        img = uint8(ones(100, 100, 3) * 128);
        resized = utils.resize(img, [50, 50]);
        assert(size(resized, 1) == 50 && size(resized, 2) == 50, 'Size should be 50x50');
        assert(size(resized, 3) == 3, 'Channels should be preserved');
        fprintf('✓ Test 3: Image Resize - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 3: Image Resize - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 4: Image crop
    try
        img = uint8(ones(100, 100, 3) * 128);
        cropped = utils.crop(img, [10, 10, 50, 50]);
        assert(size(cropped, 1) == 50 && size(cropped, 2) == 50, 'Size should be 50x50');
        fprintf('✓ Test 4: Image Crop - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 4: Image Crop - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 5: Image flip
    try
        img = uint8(reshape(1:100, 10, 10));
        flipped = utils.flip(img, 'horizontal');
        assert(flipped(1,1) == img(1,10), 'Horizontal flip failed');
        flipped = utils.flip(img, 'vertical');
        assert(flipped(1,1) == img(10,1), 'Vertical flip failed');
        fprintf('✓ Test 5: Image Flip - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 5: Image Flip - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 6: Box blur
    try
        img = uint8(zeros(10, 10, 3));
        img(5, 5, :) = 255;
        blurred = utils.blur(img, 3);
        assert(size(blurred) == size(img), 'Size should be preserved');
        fprintf('✓ Test 6: Box Blur - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 6: Box Blur - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 7: Edge detection
    try
        img = uint8(ones(20, 20) * 128);
        img(1:10, :) = 0; img(11:20, :) = 255;
        edges = utils.edgeDetect(img, 'sobel');
        assert(size(edges, 1) == 20 && size(edges, 2) == 20, 'Size should be preserved');
        fprintf('✓ Test 7: Edge Detection - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 7: Edge Detection - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 8: Brightness adjustment
    try
        img = uint8(ones(10, 10, 3) * 100);
        brightened = utils.brightness(img, 0.5);
        assert(all(brightened(:) > 100), 'Brightness should increase');
        fprintf('✓ Test 8: Brightness Adjustment - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 8: Brightness Adjustment - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 9: Contrast adjustment
    try
        img = uint8(ones(10, 10, 3) * 128);
        adjusted = utils.contrast(img, 2.0);
        assert(size(adjusted) == size(img), 'Size should be preserved');
        fprintf('✓ Test 9: Contrast Adjustment - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 9: Contrast Adjustment - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 10: Gamma correction
    try
        img = uint8(ones(10, 10, 3) * 128);
        gamma = utils.gamma(img, 2.2);
        assert(size(gamma) == size(img), 'Size should be preserved');
        fprintf('✓ Test 10: Gamma Correction - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 10: Gamma Correction - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 11: Get image size
    try
        img = uint8(ones(50, 100, 3));
        sz = utils.getSize(img);
        assert(sz(1) == 50 && sz(2) == 100 && sz(3) == 3, 'Size mismatch');
        fprintf('✓ Test 11: Get Image Size - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 11: Get Image Size - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 12: Get channels
    try
        gray = uint8(ones(10, 10));
        rgb = uint8(ones(10, 10, 3));
        assert(utils.getChannels(gray) == 1, 'Grayscale should have 1 channel');
        assert(utils.getChannels(rgb) == 3, 'RGB should have 3 channels');
        fprintf('✓ Test 12: Get Channels - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 12: Get Channels - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 13: Is grayscale
    try
        gray = uint8(ones(10, 10));
        rgb = uint8(ones(10, 10, 3));
        assert(utils.isGrayscale(gray) == true, 'Should be grayscale');
        assert(utils.isGrayscale(rgb) == false, 'Should not be grayscale');
        fprintf('✓ Test 13: Is Grayscale - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 13: Is Grayscale - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 14: Histogram
    try
        img = uint8(ones(10, 10) * 128);
        hist = utils.getHistogram(img, 256);
        assert(length(hist) == 256, 'Histogram should have 256 bins');
        assert(hist(129) == 100, 'Histogram value mismatch');
        fprintf('✓ Test 14: Histogram - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 14: Histogram - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 15: Image inversion
    try
        img = uint8(ones(10, 10, 3) * 200);
        inverted = utils.invert(img);
        assert(all(inverted(:) == 55), 'Inversion failed');
        fprintf('✓ Test 15: Image Inversion - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 15: Image Inversion - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 16: Threshold
    try
        img = uint8(reshape(1:100, 10, 10));
        binary = utils.threshold(img, 50);
        assert(islogical(binary), 'Output should be logical');
        fprintf('✓ Test 16: Threshold - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 16: Threshold - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 17: Image blend
    try
        img1 = uint8(ones(10, 10, 3) * 100);
        img2 = uint8(ones(10, 10, 3) * 200);
        blended = utils.blend(img1, img2, 0.5);
        assert(size(blended) == size(img1), 'Size should be preserved');
        fprintf('✓ Test 17: Image Blend - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 17: Image Blend - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 18: RGB to HSV and back
    try
        rgb = uint8(ones(10, 10, 3) * 128);
        hsv = utils.rgb2hsv(rgb);
        rgb_back = utils.hsv2rgb(hsv);
        assert(size(hsv, 3) == 3, 'HSV should have 3 channels');
        fprintf('✓ Test 18: RGB-HSV Conversion - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 18: RGB-HSV Conversion - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 19: Gaussian filter
    try
        img = uint8(ones(10, 10, 3) * 128);
        filtered = utils.gaussianFilter(img, 1.5);
        assert(size(filtered) == size(img), 'Size should be preserved');
        fprintf('✓ Test 19: Gaussian Filter - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 19: Gaussian Filter - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 20: Image rotation
    try
        img = uint8(ones(20, 20, 3) * 128);
        rotated = utils.rotate(img, 90);
        assert(size(rotated, 1) == 20 && size(rotated, 2) == 20, 'Size should be preserved');
        fprintf('✓ Test 20: Image Rotation - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 20: Image Rotation - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 21: Histogram equalization
    try
        img = uint8(reshape(1:256, 16, 16));
        equalized = utils.equalizeHist(img);
        assert(size(equalized) == size(img), 'Size should be preserved');
        fprintf('✓ Test 21: Histogram Equalization - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 21: Histogram Equalization - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 22: Image padding
    try
        img = uint8(ones(10, 10, 3) * 128);
        padded = utils.padImage(img, [5, 5]);
        assert(size(padded, 1) == 20 && size(padded, 2) == 20, 'Size should be 20x20');
        fprintf('✓ Test 22: Image Padding - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 22: Image Padding - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 23: Image normalization
    try
        img = uint8([0, 50, 100, 150, 200, 255]);
        normalized = utils.normalize(img, 0, 1);
        assert(abs(min(normalized(:))) < 0.01, 'Min should be 0');
        assert(abs(max(normalized(:)) - 1) < 0.01, 'Max should be 1');
        fprintf('✓ Test 23: Normalization - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 23: Normalization - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 24: Sharpen
    try
        img = uint8(ones(10, 10, 3) * 128);
        sharpened = utils.sharpen(img, 1.0);
        assert(size(sharpened) == size(img), 'Size should be preserved');
        fprintf('✓ Test 24: Sharpen - PASSED\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 24: Sharpen - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Test 25: Error handling - invalid RGB input
    try
        try
            gray = utils.rgb2gray(uint8(ones(10, 10)));
            fprintf('✗ Test 25: Error Handling - FAILED: Should have thrown error\n');
            failed = failed + 1;
        catch
            fprintf('✓ Test 25: Error Handling - PASSED\n');
            passed = passed + 1;
        end
    catch ME
        fprintf('✗ Test 25: Error Handling - FAILED: %s\n', ME.message);
        failed = failed + 1;
    end
    
    % Summary
    fprintf('\n========================================\n');
    fprintf('Test Summary: %d passed, %d failed\n', passed, failed);
    fprintf('========================================\n');
    
    if failed == 0
        fprintf('All tests passed! ✓\n');
    else
        fprintf('Some tests failed. ✗\n');
    end
end