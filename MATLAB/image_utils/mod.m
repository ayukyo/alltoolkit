function img_utils = mod()
%MOD Image Processing Utilities Module
%   A comprehensive image processing toolkit for MATLAB with zero dependencies.
%   All functions use only MATLAB standard library functions.
%
%   Usage:
%       utils = mod();
%       grayImg = utils.rgb2gray(img);
%       resized = utils.resize(img, [256, 256]);
%
%   Author: AllToolkit Contributors
%   Version: 1.0.0

    img_utils = struct();
    
    % Color Conversion Functions
    img_utils.rgb2gray = @rgb2gray_custom;
    img_utils.gray2rgb = @gray2rgb_custom;
    img_utils.rgb2hsv = @rgb2hsv_custom;
    img_utils.hsv2rgb = @hsv2rgb_custom;
    
    % Image Transformation Functions
    img_utils.resize = @resize_custom;
    img_utils.crop = @crop_custom;
    img_utils.rotate = @rotate_custom;
    img_utils.flip = @flip_custom;
    
    % Image Filtering Functions
    img_utils.blur = @blur_custom;
    img_utils.sharpen = @sharpen_custom;
    img_utils.edgeDetect = @edgeDetect_custom;
    img_utils.gaussianFilter = @gaussianFilter_custom;
    
    % Image Enhancement Functions
    img_utils.brightness = @brightness_custom;
    img_utils.contrast = @contrast_custom;
    img_utils.gamma = @gamma_custom;
    img_utils.equalizeHist = @equalizeHist_custom;
    
    % Image Analysis Functions
    img_utils.getSize = @getSize_custom;
    img_utils.getChannels = @getChannels_custom;
    img_utils.isGrayscale = @isGrayscale_custom;
    img_utils.getHistogram = @getHistogram_custom;
    
    % Utility Functions
    img_utils.padImage = @padImage_custom;
    img_utils.normalize = @normalize_custom;
    img_utils.invert = @invert_custom;
    img_utils.threshold = @threshold_custom;
    img_utils.blend = @blend_custom;
end

%% Color Conversion Functions

function gray = rgb2gray_custom(rgb)
%RGB2GRAY_CUSTOM Convert RGB image to grayscale using ITU-R BT.601 standard
    if ndims(rgb) ~= 3 || size(rgb, 3) ~= 3
        error('Input must be an RGB image with 3 channels');
    end
    rgb_d = im2double_safe(rgb);
    gray = 0.299 * rgb_d(:,:,1) + 0.587 * rgb_d(:,:,2) + 0.114 * rgb_d(:,:,3);
    gray = convertType(gray, class(rgb));
end

function rgb = gray2rgb_custom(gray)
%GRAY2RGB_CUSTOM Convert grayscale to RGB by replicating channels
    if ndims(gray) == 3 && size(gray, 3) == 3
        rgb = gray;
        return;
    end
    rgb = cat(3, gray, gray, gray);
end

function hsv = rgb2hsv_custom(rgb)
%RGB2HSV_CUSTOM Convert RGB to HSV color space
    if ndims(rgb) ~= 3 || size(rgb, 3) ~= 3
        error('Input must be an RGB image');
    end
    rgb_d = im2double_safe(rgb);
    [rows, cols, ~] = size(rgb_d);
    hsv = zeros(rows, cols, 3);
    for i = 1:rows
        for j = 1:cols
            r = rgb_d(i,j,1); g = rgb_d(i,j,2); b = rgb_d(i,j,3);
            maxVal = max([r, g, b]); minVal = min([r, g, b]);
            delta = maxVal - minVal;
            v = maxVal;
            if maxVal == 0, s = 0; else, s = delta / maxVal; end
            if delta == 0
                h = 0;
            elseif maxVal == r
                h = 60 * mod((g - b) / delta, 6);
            elseif maxVal == g
                h = 60 * ((b - r) / delta + 2);
            else
                h = 60 * ((r - g) / delta + 4);
            end
            hsv(i,j,:) = [h, s, v];
        end
    end
end

function rgb = hsv2rgb_custom(hsv)
%HSV2RGB_CUSTOM Convert HSV to RGB color space
    if ndims(hsv) ~= 3 || size(hsv, 3) ~= 3
        error('Input must be an HSV image');
    end
    [rows, cols, ~] = size(hsv);
    rgb = zeros(rows, cols, 3);
    for i = 1:rows
        for j = 1:cols
            h = hsv(i,j,1); s = hsv(i,j,2); v = hsv(i,j,3);
            c = v * s;
            x = c * (1 - abs(mod(h / 60, 2) - 1));
            m = v - c;
            if h < 60, r = c; g = x; b = 0;
            elseif h < 120, r = x; g = c; b = 0;
            elseif h < 180, r = 0; g = c; b = x;
            elseif h < 240, r = 0; g = x; b = c;
            elseif h < 300, r = x; g = 0; b = c;
            else, r = c; g = 0; b = x; end
            rgb(i,j,:) = [r + m, g + m, b + m];
        end
    end
end

%% Image Transformation Functions

function resized = resize_custom(img, targetSize, method)
%RESIZE_CUSTOM Resize image to target size using bilinear or nearest interpolation
    if nargin < 3, method = 'bilinear'; end
    [origH, origW, channels] = size(img);
    targetH = targetSize(1); targetW = targetSize(2);
    rowScale = (origH - 1) / max(targetH - 1, 1);
    colScale = (origW - 1) / max(targetW - 1, 1);
    rows = (0:targetH-1) * rowScale + 1;
    cols = (0:targetW-1) * colScale + 1;
    resized = zeros(targetH, targetW, channels, class(img));
    for c = 1:channels
        resized(:,:,c) = interp2_custom(double(img(:,:,c)), cols, rows, method);
    end
    if ~isa(img, 'double')
        resized = convertType(resized, class(img));
    end
end

function cropped = crop_custom(img, rect)
%CROP_CUSTOM Crop image to specified rectangle [x, y, width, height]
    x = max(1, round(rect(1))); y = max(1, round(rect(2)));
    w = rect(3); h = rect(4);
    rowStart = y; rowEnd = min(y + h - 1, size(img, 1));
    colStart = x; colEnd = min(x + w - 1, size(img, 2));
    cropped = img(rowStart:rowEnd, colStart:colEnd, :);
end

function rotated = rotate_custom(img, angle, method)
%ROTATE_CUSTOM Rotate image by specified angle in degrees
    if nargin < 3, method = 'bilinear'; end
    [h, w, channels] = size(img);
    theta = deg2rad(-angle);
    cosT = cos(theta); sinT = sin(theta);
    cx = w/2; cy = h/2;
    rotated = zeros(h, w, channels, class(img));
    for i = 1:h
        for j = 1:w
            x = j - cx; y = i - cy;
            srcX = x * cosT - y * sinT + cx;
            srcY = x * sinT + y * cosT + cy;
            for c = 1:channels
                rotated(i,j,c) = samplePixel(img(:,:,c), srcY, srcX, method);
            end
        end
    end
end

function flipped = flip_custom(img, direction)
%FLIP_CUSTOM Flip image horizontally or vertically
    if nargin < 2, direction = 'horizontal'; end
    if strcmp(direction, 'horizontal')
        flipped = img(:, end:-1:1, :);
    else
        flipped = img(end:-1:1, :, :);
    end
end

%% Image Filtering Functions

function blurred = blur_custom(img, kernelSize)
%BLUR_CUSTOM Apply box blur to image
    if nargin < 2, kernelSize = 3; end
    if mod(kernelSize, 2) == 0, kernelSize = kernelSize + 1; end
    kernel = ones(kernelSize) / (kernelSize * kernelSize);
    blurred = convolve_custom(img, kernel);
end

function sharpened = sharpen_custom(img, amount)
%SHARPEN_CUSTOM Sharpen image using unsharp mask
    if nargin < 2, amount = 1.0; end
    kernel = [0, -1, 0; -1, 5, -1; 0, -1, 0];
    sharpened = convolve_custom(img, kernel);
    sharpened = img + amount * (sharpened - img);
    sharpened = clampImage(sharpened, class(img));
end

function edges = edgeDetect_custom(img, method)
%EDGEDETECT_CUSTOM Detect edges using Sobel or Prewitt operator
    if nargin < 2, method = 'sobel'; end
    img_gray = img;
    if ndims(img) == 3
        img_gray = rgb2gray_custom(img);
    end
    img_d = double(img_gray);
    
    if strcmp(method, 'sobel')
        gx = [-1, 0, 1; -2, 0, 2; -1, 0, 1];
        gy = [-1, -2, -1; 0, 0, 0; 1, 2, 1];
    else
        gx = [-1, 0, 1; -1, 0, 1; -1, 0, 1];
        gy = [-1, -1, -1; 0, 0, 0; 1, 1, 1];
    end
    
    edgesX = conv2(img_d, gx, 'same');
    edgesY = conv2(img_d, gy, 'same');
    edges = sqrt(edgesX.^2 + edgesY.^2);
    edges = uint8(min(255, edges));
end

function filtered = gaussianFilter_custom(img, sigma)
%GAUSSIANFILTER_CUSTOM Apply Gaussian blur filter
    if nargin < 2, sigma = 1.0; end
    kernelSize = max(3, 2 * round(3 * sigma) + 1);
    kernel = gaussianKernel(kernelSize, sigma);
    filtered = convolve_custom(img, kernel);
end

%% Image Enhancement Functions

function brightened = brightness_custom(img, delta)
%BRIGHTNESS_CUSTOM Adjust image brightness
    if nargin < 2, delta = 0.2; end
    img_d = im2double_safe(img);
    brightened = img_d + delta;
    brightened = clampImage(brightened, class(img));
end

function adjusted = contrast_custom(img, factor)
%CONTRAST_CUSTOM Adjust image contrast
    if nargin < 2, factor = 1.5; end
    img_d = im2double_safe(img);
    adjusted = (img_d - 0.5) * factor + 0.5;
    adjusted = clampImage(adjusted, class(img));
end

function gammaCorrected = gamma_custom(img, gamma)
%GAMMA_CUSTOM Apply gamma correction
    if nargin < 2, gamma = 2.2; end
    img_d = im2double_safe(img);
    gammaCorrected = img_d .^ (1 / gamma);
    gammaCorrected = convertType(gammaCorrected, class(img));
end

function equalized = equalizeHist_custom(img)
%EQUALIZEHIST_CUSTOM Apply histogram equalization
    img_gray = img;
    if ndims(img) == 3
        img_gray = rgb2gray_custom(img);
    end
    [h, w] = size(img_gray);
    hist = getHistogram_custom(img_gray, 256);
    cdf = cumsum(hist) / (h * w);
    equalized = uint8(255 * cdf(double(img_gray) + 1));
    if ndims(img) == 3
        equalized = gray2rgb_custom(equalized);
    end
end

%% Image Analysis Functions

function sz = getSize_custom(img)
%GETSIZE_CUSTOM Get image dimensions [height, width, channels]
    sz = size(img);
    if ndims(img) == 2
        sz = [sz, 1];
    end
end

function ch = getChannels_custom(img)
%GETCHANNELS_CUSTOM Get number of channels
    if ndims(img) == 2
        ch = 1;
    else
        ch = size(img, 3);
    end
end

function flag = isGrayscale_custom(img)
%ISGRAYSCALE_CUSTOM Check if image is grayscale
    flag = ndims(img) == 2 || (ndims(img) == 3 && size(img, 3) == 1);
end

function hist = getHistogram_custom(img, bins)
%GETHISTOGRAM_CUSTOM Calculate image histogram
    if nargin < 2, bins = 256; end
    img_gray = img;
    if ndims(img) == 3
        img_gray = rgb2gray_custom(img);
    end
    hist = zeros(1, bins);
    img_flat = double(img_gray(:));
    img_flat = floor(img_flat * bins / 256);
    img_flat = max(0, min(bins-1, img_flat));
    for i = 1:length(img_flat)
        hist(img_flat(i) + 1) = hist(img_flat(i) + 1) + 1;
    end
end

%% Utility Functions

function padded = padImage_custom(img, padSize, mode)
%PADIMAGE_CUSTOM Pad image with specified mode
    if nargin < 3, mode = 'constant'; end
    if nargin < 2, padSize = 1; end
    if numel(padSize) == 1
        padSize = [padSize, padSize];
    end
    [h, w, ch] = size(img);
    newH = h + 2*padSize(1);
    newW = w + 2*padSize(2);
    padded = zeros(newH, newW, ch, class(img));
    padded(padSize(1)+1:padSize(1)+h, padSize(2)+1:padSize(2)+w, :) = img;
end

function normalized = normalize_custom(img, minVal, maxVal)
%NORMALIZE_CUSTOM Normalize image to specified range
    if nargin < 2, minVal = 0; end
    if nargin < 3, maxVal = 1; end
    img_d = double(img);
    img_min = min(img_d(:));
    img_max = max(img_d(:));
    if img_max == img_min
        normalized = ones(size(img)) * minVal;
    else
        normalized = (img_d - img_min) / (img_max - img_min) * (maxVal - minVal) + minVal;
    end
end

function inverted = invert_custom(img)
%INVERT_CUSTOM Invert image colors
    if isa(img, 'uint8')
        inverted = 255 - img;
    elseif isa(img, 'uint16')
        inverted = 65535 - img;
    else
        inverted = 1 - img;
    end
end

function binary = threshold_custom(img, thresh)
%THRESHOLD_CUSTOM Apply threshold to create binary image
    if nargin < 2
        img_gray = img;
        if ndims(img) == 3
            img_gray = rgb2gray_custom(img);
        end
        thresh = mean(double(img_gray(:)));
    end
    img_gray = img;
    if ndims(img) == 3
        img_gray = rgb2gray_custom(img);
    end
    binary = img_gray > thresh;
end

function blended = blend_custom(img1, img2, alpha)
%BLEND_CUSTOM Blend two images with alpha
    if nargin < 3, alpha = 0.5; end
    img1_d = im2double_safe(img1);
    img2_d = im2double_safe(img2);
    blended = img1_d * alpha + img2_d * (1 - alpha);
    blended = convertType(blended, class(img1));
end

%% Helper Functions

function img_d = im2double_safe(img)
%IM2DOUBLE_SAFE Convert image to double in range [0, 1]
    if isa(img, 'uint8')
        img_d = double(img) / 255;
    elseif isa(img, 'uint16')
        img_d = double(img) / 65535;
    elseif isa(img, 'single')
        img_d = double(img);
    else
        img_d = img;
    end
end

function img_out = convertType(img, type)
%CONVERTTYPE Convert image to specified data type
    switch type
        case 'uint8'
            img_out = uint8(max(0, min(1, img)) * 255);
        case 'uint16'
            img_out = uint16(max(0, min(1, img)) * 65535);
        case 'single'
            img_out = single(img);
        otherwise
            img_out = img;
    end
end

function img_out = clampImage(img, type)
%CLAMPIMAGE Clamp image values to valid range
    if strcmp(type, 'uint8')
        img_out = uint8(max(0, min(255, img)));
    elseif strcmp(type, 'uint16')
        img_out = uint16(max(0, min(65535, img)));
    else
        img_out = max(0, min(1, img));
    end
end

function val = samplePixel(img, row, col, method)
%SAMPLEPIXEL Sample pixel value with interpolation
    [h, w] = size(img);
    if strcmp(method, 'nearest')
        r = round(row); c = round(col);
        r = max(1, min(h, r)); c = max(1, min(w, c));
        val = img(r, c);
    else
        r1 = floor(row); r2 = ceil(row);
        c1 = floor(col); c2 = ceil(col);
        r1 = max(1, min(h, r1)); r2 = max(1, min(h, r2));
        c1 = max(1, min(w, c1)); c2 = max(1, min(w, c2));
        dr = row - r1; dc = col - c1;
        val = (1-dr)*(1-dc)*img(r1,c1) + (1-dr)*dc*img(r1,c2) + ...
              dr*(1-dc)*img(r2,c1) + dr*dc*img(r2,c2);
    end
end

function result = interp2_custom(img, cols, rows, method)
%INTERP2_CUSTOM 2D interpolation
    [h, w] = size(img);
    result = zeros(length(rows), length(cols));
    for i = 1:length(rows)
        for j = 1:length(cols)
            result(i,j) = samplePixel(img, rows(i), cols(j), method);
        end
    end
end

function result = convolve_custom(img, kernel)
%CONVOLVE_CUSTOM Convolve image with kernel
    [kh, kw] = size(kernel);
    padH = floor(kh/2); padW = floor(kw/2);
    [h, w, ch] = size(img);
    result = zeros(h, w, ch);
    for c = 1:ch
        padded = padarray(img(:,:,c), [padH, padW], 'replicate');
        for i = 1:h
            for j = 1:w
                patch = padded(i:i+kh-1, j:j+kw-1);
                result(i,j,c) = sum(sum(double(patch) .* kernel));
            end
        end
    end
    result = convertType(result, class(img));
end

function kernel = gaussianKernel(size, sigma)
%GAUSSIANKERNEL Generate Gaussian kernel
    if mod(size, 2) == 0, size = size + 1; end
    center = floor(size/2);
    kernel = zeros(size);
    for i = 1:size
        for j = 1:size
            x = i - center - 1;
            y = j - center - 1;
            kernel(i,j) = exp(-(x^2 + y^2) / (2 * sigma^2));
        end
    end
    kernel = kernel / sum(kernel(:));
end
