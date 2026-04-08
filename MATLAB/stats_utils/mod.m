function utils = mod()
%MOD Statistics utilities for MATLAB
%   A comprehensive statistics utility module providing descriptive statistics,
%   probability distributions, and statistical analysis functions.
%
%   Usage:
%       utils = mod();
%       mean_val = utils.mean([1, 2, 3, 4, 5]);
%       std_val = utils.std([1, 2, 3, 4, 5]);
%
%   Author: AllToolkit
%   Version: 1.0.0

    utils = struct();
    
    % Descriptive Statistics
    utils.mean = @mean_func;
    utils.median = @median_func;
    utils.mode = @mode_func;
    utils.variance = @variance_func;
    utils.std = @std_func;
    utils.range = @range_func;
    utils.min = @min_func;
    utils.max = @max_func;
    utils.sum = @sum_func;
    utils.product = @product_func;
    
    % Percentiles and Quartiles
    utils.percentile = @percentile_func;
    utils.quartile = @quartile_func;
    utils.iqr = @iqr_func;
    
    % Distribution Measures
    utils.skewness = @skewness_func;
    utils.kurtosis = @kurtosis_func;
    
    % Correlation and Covariance
    utils.covariance = @covariance_func;
    utils.correlation = @correlation_func;
    
    % Normalization and Scaling
    utils.zscore = @zscore_func;
    utils.minMaxScale = @minMaxScale_func;
    utils.standardize = @standardize_func;
    
    % Outlier Detection
    utils.isOutlier = @isOutlier_func;
    utils.removeOutliers = @removeOutliers_func;
    
    % Probability Distributions
    utils.normPdf = @normPdf_func;
    utils.normCdf = @normCdf_func;
    utils.normInv = @normInv_func;
    
    % Sampling
    utils.sample = @sample_func;
    utils.bootstrap = @bootstrap_func;
    
    % Summary Statistics
    utils.summary = @summary_func;
    utils.describe = @describe_func;
end

%% Descriptive Statistics Functions

function m = mean_func(data, dim)
    if nargin < 2, dim = 1; end
    data = removeNaN(data);
    if isempty(data), m = NaN; return; end
    m = mean(data, dim);
end

function m = median_func(data, dim)
    if nargin < 2, dim = 1; end
    data = removeNaN(data);
    if isempty(data), m = NaN; return; end
    m = median(data, dim);
end

function m = mode_func(data)
    data = removeNaN(data);
    if isempty(data), m = NaN; return; end
    if isvector(data)
        [uniqueVals, ~, idx] = unique(data);
        counts = accumarray(idx, 1);
        maxCount = max(counts);
        m = uniqueVals(counts == maxCount);
        if length(m) == length(uniqueVals), m = []; end
    else
        m = mode(data);
    end
end

function v = variance_func(data, dim, flag)
    if nargin < 2, dim = 1; end
    if nargin < 3, flag = 1; end
    data = removeNaN(data);
    if isempty(data), v = NaN; return; end
    v = var(data, 0, dim, flag);
end

function s = std_func(data, dim, flag)
    if nargin < 2, dim = 1; end
    if nargin < 3, flag = 1; end
    data = removeNaN(data);
    if isempty(data), s = NaN; return; end
    s = std(data, flag, dim);
end

function r = range_func(data, dim)
    if nargin < 2, dim = 1; end
    data = removeNaN(data);
    if isempty(data), r = NaN; return; end
    r = max(data, [], dim) - min(data, [], dim);
end

function m = min_func(data, dim)
    if nargin < 2, dim = 1; end
    data = removeNaN(data);
    if isempty(data), m = NaN; return; end
    m = min(data, [], dim);
end

function m = max_func(data, dim)
    if nargin < 2, dim = 1; end
    data = removeNaN(data);
    if isempty(data), m = NaN; return; end
    m = max(data, [], dim);
end

function s = sum_func(data, dim)
    if nargin < 2, dim = 1; end
    data = removeNaN(data);
    if isempty(data), s = 0; return; end
    s = sum(data, dim);
end

function p = product_func(data, dim)
    if nargin < 2, dim = 1; end
    data = removeNaN(data);
    if isempty(data), p = 1; return; end
    p = prod(data, dim);
end

%% Percentiles and Quartiles

function p = percentile_func(data, pct, dim)
    if nargin < 3, dim = 1; end
    data = removeNaN(data);
    if isempty(data), p = NaN; return; end
    p = prctile(data, pct, dim);
end

function q = quartile_func(data, whichQ, dim)
    if nargin < 2, whichQ = 0; end
    if nargin < 3, dim = 1; end
    data = removeNaN(data);
    if isempty(data), q = NaN; return; end
    switch whichQ
        case 0
            q = prctile(data, [0, 25, 50, 75, 100], dim);
        case 1
            q = prctile(data, 25, dim);
        case 2
            q = prctile(data, 50, dim);
        case 3
            q = prctile(data, 75, dim);
        otherwise
            q = prctile(data, whichQ * 25, dim);
    end
end

function i = iqr_func(data, dim)
    if nargin < 2, dim = 1; end
    data = removeNaN(data);
    if isempty(data), i = NaN; return; end
    q = prctile(data, [25, 75], dim);
    if size(q, 1) == 2
        i = q(2,:) - q(1,:);
    else
        i = diff(q, 1, dim);
    end
end

%% Distribution Measures

function s = skewness_func(data, dim, flag)
    if nargin < 2, dim = 1; end
    if nargin < 3, flag = 1; end
    data = removeNaN(data);
    if isempty(data), s = NaN; return; end
    s = skewness(data, flag, dim);
end

function k = kurtosis_func(data, dim, flag)
    if nargin < 2, dim = 1; end
    if nargin < 3, flag = 1; end
    data = removeNaN(data);
    if isempty(data), k = NaN; return; end
    k = kurtosis(data, flag, dim);
end

%% Correlation and Covariance

function c = covariance_func(x, y)
    if nargin < 2
        x = removeNaN(x);
        if isempty(x), c = NaN; return; end
        c = cov(x);
    else
        mask = ~isnan(x) & ~isnan(y);
        x = x(mask); y = y(mask);
        if isempty(x), c = NaN; return; end
        c = cov(x, y);
    end
end

function r = correlation_func(x, y)
    if nargin < 2
        x = removeNaN(x);
        if isempty(x), r = NaN; return; end
        r = corrcoef(x);
    else
        mask = ~isnan(x) & ~isnan(y);
        x = x(mask); y = y(mask);
        if isempty(x), r = NaN; return; end
        r = corrcoef(x, y);
        r = r(1,2);
    end
end

%% Normalization and Scaling

function z = zscore_func(data, dim)
    if nargin < 2, dim = 1; end
    data = removeNaN(data);
    if isempty(data), z = []; return; end
    mu = mean(data, dim);
    sigma = std(data, 0, dim);
    z = (data - mu) ./ sigma;
end

function n = normalize_func(data, dim)
    if nargin < 2, dim = 1; end
    data = removeNaN(data);
    if isempty(data), n = []; return; end
    n = data ./ sum(data, dim);
end

function s = minMaxScale_func(data, newMin, newMax, dim)
    if nargin < 2, newMin = 0; end
    if nargin < 3, newMax = 1; end
    if nargin < 4, dim = 1; end
    data = removeNaN(data);
    if isempty(data), s = []; return; end
    oldMin = min(data, [], dim);
    oldMax = max(data, [], dim);
    s = (data - oldMin) ./ (oldMax - oldMin) .* (newMax - newMin) + newMin;
end

function s = standardize_func(data, dim)
    s = zscore_func(data, dim);
end

%% Outlier Detection

function idx = isOutlier_func(data, method, threshold)
    if nargin < 2, method = 'iqr'; end
    if nargin < 3, threshold = 1.5; end
    data = removeNaN(data);
    if isempty(data), idx = false(size(data)); return; end
    
    switch lower(method)
        case 'iqr'
            q = prctile(data, [25, 75]);
            iqr_val = q(2) - q(1);
            lower = q(1) - threshold * iqr_val;
            upper = q(2) + threshold * iqr_val;
            idx = data < lower | data > upper;
        case 'zscore'
            z = abs(zscore_func(data));
            idx = z > threshold;
        case 'mad'
            med = median(data);
            mad_val = median(abs(data - med));
            idx = abs(data - med) > threshold * mad_val;
        otherwise
            idx = false(size(data));
    end
end

function filtered = removeOutliers_func(data, method, threshold)
    if nargin < 2, method
