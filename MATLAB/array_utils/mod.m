classdef mod < handle
    %ARRAY_UTILS Comprehensive array manipulation utilities for MATLAB
    %   Provides array operations, matrix transformations, set operations,
    %   array analysis, and utility functions for scientific computing.
    %
    %   Author: AllToolkit
    %   Version: 1.0.0
    %   License: MIT
    
    methods (Static)
        %% Array Creation and Generation
        
        function arr = range(start, stop, step)
            %RANGE Generate a range of values from start to stop with step
            %   arr = range(start, stop, step) - Generate values from start to stop
            %   arr = range(start, stop) - Default step = 1
            %
            %   Example:
            %       arr = range(1, 10, 2)  % Returns [1, 3, 5, 7, 9]
            %       arr = range(0, 1, 0.2) % Returns [0, 0.2, 0.4, 0.6, 0.8, 1]
            
            if nargin < 3
                step = 1;
            end
            arr = start:step:stop;
        end
        
        function arr = linspace(start, stop, n)
            %LINSPACE Generate n linearly spaced values between start and stop
            %   arr = linspace(start, stop, n) - Generate n values
            %   arr = linspace(start, stop) - Default n = 100
            %
            %   Example:
            %       arr = linspace(0, 1, 5)  % Returns [0, 0.25, 0.5, 0.75, 1]
            
            if nargin < 3
                n = 100;
            end
            arr = linspace(start, stop, n);
        end
        
        function arr = logspace(start, stop, n)
            %LOGSPACE Generate n logarithmically spaced values
            %   arr = logspace(start, stop, n) - Generate n values from 10^start to 10^stop
            %   arr = logspace(start, stop) - Default n = 50
            %
            %   Example:
            %       arr = logspace(0, 2, 3)  % Returns [1, 10, 100]
            
            if nargin < 3
                n = 50;
            end
            arr = logspace(start, stop, n);
        end
        
        function arr = repeat(value, count)
            %REPEAT Create an array by repeating a value
            %   arr = repeat(value, count) - Repeat value count times
            %
            %   Example:
            %       arr = repeat(5, 3)  % Returns [5, 5, 5]
            %       arr = repeat('a', 4) % Returns 'aaaa'
            
            % Validate count parameter
            if ~isnumeric(count) || ~isscalar(count) || count < 0 || count ~= floor(count)
                error('count must be a non-negative integer');
            end
            
            if count == 0
                arr = [];
                return;
            end
            
            if isnumeric(value)
                arr = repmat(value, 1, count);
            else
                arr = repmat({value}, 1, count);
            end
        end
        
        function arr = zeros_like(arr)
            %ZEROS_LIKE Create an array of zeros with the same size as input
            %   result = zeros_like(arr) - Create zeros array matching size
            %
            %   Example:
            %       a = [1, 2, 3; 4, 5, 6];
            %       z = zeros_like(a)  % Returns 2x3 zeros matrix
            
            arr = zeros(size(arr));
        end
        
        function arr = ones_like(arr)
            %ONES_LIKE Create an array of ones with the same size as input
            %   result = ones_like(arr) - Create ones array matching size
            %
            %   Example:
            %       a = [1, 2, 3; 4, 5, 6];
            %       o = ones_like(a)  % Returns 2x3 ones matrix
            
            arr = ones(size(arr));
        end
        
        %% Array Information and Analysis
        
        function s = size(arr, dim)
            %SIZE Get the size of an array
            %   s = size(arr) - Get size vector
            %   s = size(arr, dim) - Get size of specific dimension
            %
            %   Example:
            %       s = size([1, 2, 3; 4, 5, 6])  % Returns [2, 3]
            %       s = size([1, 2, 3], 2)        % Returns 3
            
            if nargin < 2
                s = size(arr);
            else
                s = size(arr, dim);
            end
        end
        
        function n = length(arr)
            %LENGTH Get the length of the largest array dimension
            %   n = length(arr) - Get maximum dimension length
            %
            %   Example:
            %       n = length([1, 2, 3, 4, 5])  % Returns 5
            %       n = length([1, 2; 3, 4; 5, 6]) % Returns 3
            
            n = length(arr);
        end
        
        function n = numel(arr)
            %NUMEL Get the number of elements in an array
            %   n = numel(arr) - Count total elements
            %
            %   Example:
            %       n = numel([1, 2, 3; 4, 5, 6])  % Returns 6
            
            n = numel(arr);
        end
        
        function d = ndims(arr)
            %NDIMS Get the number of dimensions in an array
            %   d = ndims(arr) - Count dimensions
            %
            %   Example:
            %       d = ndims([1, 2, 3])     % Returns 2 (treated as 1xN)
            %       d = ndims(ones(2, 3, 4)) % Returns 3
            
            d = ndims(arr);
        end
        
        function tf = is_empty(arr)
            %IS_EMPTY Check if an array is empty
            %   tf = is_empty(arr) - Returns true if array has no elements
            %
            %   Example:
            %       tf = is_empty([])        % Returns true
            %       tf = is_empty([1, 2, 3]) % Returns false
            
            tf = isempty(arr);
        end
        
        function tf = is_vector(arr)
            %IS_VECTOR Check if an array is a vector (1D)
            %   tf = is_vector(arr) - Returns true for row or column vectors
            %
            %   Example:
            %       tf = is_vector([1, 2, 3])     % Returns true
            %       tf = is_vector([1; 2; 3])     % Returns true
            %       tf = is_vector([1, 2; 3, 4])  % Returns false
            
            tf = isvector(arr);
        end
        
        function tf = is_matrix(arr)
            %IS_MATRIX Check if an array is a matrix (2D)
            %   tf = is_matrix(arr) - Returns true for 2D arrays
            %
            %   Example:
            %       tf = is_matrix([1, 2; 3, 4])  % Returns true
            %       tf = is_matrix(ones(2, 3, 4)) % Returns false
            
            tf = ismatrix(arr);
        end
        
        function tf = is_scalar(arr)
            %IS_SCALAR Check if an array is a scalar (single element)
            %   tf = is_scalar(arr) - Returns true for 1x1 arrays
            %
            %   Example:
            %       tf = is_scalar(5)        % Returns true
            %       tf = is_scalar([5])      % Returns true
            %       tf = is_scalar([1, 2])   % Returns false
            
            tf = isscalar(arr);
        end
        
        function idx = find_nonzero(arr)
            %FIND_NONZERO Find indices of non-zero elements
            %   idx = find_nonzero(arr) - Find all non-zero indices
            %
            %   Example:
            %       idx = find_nonzero([0, 1, 0, 3, 0])  % Returns [2, 4]
            
            idx = find(arr ~= 0);
        end
        
        function [min_val, min_idx] = min_element(arr)
            %MIN_ELEMENT Find the minimum element and its index
            %   min_val = min_element(arr) - Get minimum value
            %   [min_val, min_idx] = min_element(arr) - Get value and index
            %
            %   Example:
            %       [val, idx] = min_element([3, 1, 4, 1, 5])  % Returns 1, 2
            
            [min_val, min_idx] = min(arr(:));
        end
        
        function [max_val, max_idx] = max_element(arr)
            %MAX_ELEMENT Find the maximum element and its index
            %   max_val = max_element(arr) - Get maximum value
            %   [max_val, max_idx] = max_element(arr) - Get value and index
            %
            %   Example:
            %       [val, idx] = max_element([3, 1, 4, 1, 5])  % Returns 5, 5
            
            [max_val, max_idx] = max(arr(:));
        end
        
        %% Array Manipulation
        
        function arr = flatten(arr)
            %FLATTEN Flatten a multi-dimensional array to a column vector
            %   result = flatten(arr) - Reshape to Nx1 column vector
            %
            %   Example:
            %       arr = flatten([1, 2; 3, 4])  % Returns [1; 3; 2; 4]
            
            arr = arr(:);
        end
        
        function arr = reshape(arr, varargin)
            %RESHAPE Reshape an array to specified dimensions
            %   result = reshape(arr, m, n) - Reshape to m x n
            %   result = reshape(arr, [m, n, p]) - Reshape to m x n x p
            %
            %   Example:
            %       arr = reshape(1:6, 2, 3)  % Returns [1, 3, 5; 2, 4, 6]
            
            arr = reshape(arr, varargin{:});
        end
        
        function arr = transpose(arr)
            %TRANSPOSE Transpose a matrix (non-conjugate)
            %   result = transpose(arr) - Swap rows and columns
            %
            %   Example:
            %       arr = transpose([1, 2, 3; 4, 5, 6])  % Returns 3x2 matrix
            
            arr = arr.';
        end
        
        function arr = reverse(arr, dim)
            %REVERSE Reverse the order of elements in an array
            %   result = reverse(arr) - Reverse along first non-singleton dimension
            %   result = reverse(arr, dim) - Reverse along specified dimension
            %
            %   Example:
            %       arr = reverse([1, 2, 3, 4, 5])  % Returns [5, 4, 3, 2, 1]
            %       arr = reverse([1, 2; 3, 4], 1)  % Returns [3, 4; 1, 2]
            
            if nargin < 2
                arr = flip(arr);
            else
                arr = flip(arr, dim);
            end
        end
        
        function arr = rotate(arr, k)
            %ROTATE Circularly shift array elements
            %   result = rotate(arr, k) - Rotate by k positions
            %
            %   Example:
            %       arr = rotate([1, 2, 3, 4, 5], 2)  % Returns [4, 5, 1, 2, 3]
            %       arr = rotate([1, 2, 3, 4, 5], -1) % Returns [2, 3, 4, 5, 1]
            
            if nargin < 2
                k = 1;
            end
            arr = circshift(arr, k);
        end
        
        function arr = pad(arr, pad_size, pad_value)
            %PAD Pad an array with a specified value
            %   result = pad(arr, pad_size, pad_value) - Pad array borders
            %
            %   Example:
            %       arr = pad([1, 2; 3, 4], 1, 0)  % Add 1 zero border
            
            if nargin < 3
                pad_value = 0;
            end
            
            % Validate inputs
            if ~isnumeric(pad_size) || ~isscalar(pad_size) || pad_size < 0 || pad_size ~= floor(pad_size)
                error('pad_size must be a non-negative integer');
            end
            
            if pad_size == 0
                return;
            end
            
            arr = padarray(arr, pad_size * ones(1, ndims(arr)), pad_value);
        end
        
        function arr = trim(arr, trim_size)
            %TRIM Remove elements from the borders of an array
            %   result = trim(arr, trim_size) - Remove trim_size from each border
            %
            %   Example:
            %       arr = trim([0, 0, 0; 0, 1, 0; 0, 0, 0], 1)  % Returns [1]
            
            % Validate trim_size
            if ~isnumeric(trim_size) || ~isscalar(trim_size) || trim_size < 0 || trim_size ~= floor(trim_size)
                error('trim_size must be a non-negative integer');
            end
            
            if trim_size == 0
                return;
            end
            
            sz = size(arr);
            nd = ndims(arr);
            
            % Check if trim would result in empty array
            if any(sz <= 2 * trim_size)
                arr = [];
                return;
            end
            
            idx = cell(1, nd);
            for i = 1:nd
                idx{i} = (trim_size + 1):(sz(i) - trim_size);
            end
            arr = arr(idx{:});
        end
        
        function arr = unique_elements(arr)
            %UNIQUE_ELEMENTS Get unique elements in an array
            %   result = unique_elements(arr) - Return sorted unique values
            %
            %   Example:
            %       arr = unique_elements([1, 2, 2, 3, 3, 3])  % Returns [1, 2, 3]
            
            arr = unique(arr);
        end
        
        function arr = sort_elements(arr, order)
            %SORT_ELEMENTS Sort array elements
            %   result = sort_elements(arr) - Sort in ascending order
            %   result = sort_elements(arr, 'descend') - Sort descending
            %
            %   Example:
            %       arr = sort_elements([3, 1, 4, 1, 5])  % Returns [1, 1, 3, 4, 5]
            
            if nargin < 2
                order = 'ascend';
            end
            arr = sort(arr(:), order);
        end
        
        %% Set Operations
        
        function arr = union_sets(a, b)
            %UNION_SETS Compute the union of two arrays
            %   result = union_sets(a, b) - Elements in either a or b
            %
            %   Example:
            %       arr = union_sets([1, 2, 3], [2, 3, 4])  % Returns [1, 2, 3, 4]
            
            arr = union(a, b);
        end
        
        function arr = intersect_sets(a, b)
            %INTERSECT_SETS Compute the intersection of two arrays
            %   result = intersect_sets(a, b) - Elements in both a and b
            %
            %   Example:
            %       arr = intersect_sets([1, 2, 3], [2, 3, 4])  % Returns [2, 3]
            
            arr = intersect(a, b);
        end
        
        function arr = set_difference(a, b)
            %SET_DIFFERENCE Compute the set difference (a - b)
            %   result = set_difference(a, b) - Elements in a but not in b
            %
            %   Example:
            %       arr = set_difference([1, 2, 3], [2, 3, 4])  % Returns [1]
            
            arr = setdiff(a, b);
        end
        
        function arr = set_xor(a, b)
            %SET_XOR Compute the symmetric difference of two arrays
            %   result = set_xor(a, b) - Elements in exactly one of a or b
            %
            %   Example:
            %       arr = set_xor([1, 2, 3], [2, 3, 4])  % Returns [1, 4]
            
            arr = setxor(a, b);
        end
        
        function tf = is_member(element, arr)
            %IS_MEMBER Check if elements are members of a set
            %   tf = is_member(element, arr) - Returns logical array
            %
            %   Example:
            %       tf = is_member([1, 5], [1, 2, 3, 4])  % Returns [true, false]
            
            tf = ismember(element, arr);
        end
        
        %% Array Mathematics
        
        function s = sum_elements(arr, dim)
            %SUM_ELEMENTS Sum of array elements
            %   s = sum_elements(arr) - Sum all elements
            %   s = sum_elements(arr, dim) - Sum along dimension
            %
            %   Example:
            %       s = sum_elements([1, 2, 3, 4, 5])  % Returns 15
            %       s = sum_elements([1, 2; 3, 4], 1)  % Returns [4, 6]
            
            if nargin < 2
                s = sum(arr(:));
            else
                s = sum(arr, dim);
            end
        end
        
        function p = prod_elements(arr, dim)
            %PROD_ELEMENTS Product of array elements
            %   p = prod_elements(arr) - Product of all elements
            %   p = prod_elements(arr, dim) - Product along dimension
            %
            %   Example:
            %       p = prod_elements([1, 2, 3, 4])  % Returns 24
            
            if nargin < 2
                p = prod(arr(:));
            else
                p = prod(arr, dim);
            end
        end
        
        function m = mean_elements(arr, dim)
            %MEAN_ELEMENTS Mean of array elements
            %   m = mean_elements(arr) - Mean of all elements
            %   m = mean_elements(arr, dim) - Mean along dimension
            %
            %   Example:
            %       m = mean_elements([1, 2, 3, 4, 5])  % Returns 3
            
            if nargin < 2
                m = mean(arr(:));
            else
                m = mean(arr, dim);
            end
        end
        
        function s = std_elements(arr, dim)
            %STD_ELEMENTS Standard deviation of array elements
            %   s = std_elements(arr) - Std dev of all elements
            %   s = std_elements(arr, dim) - Std dev along dimension
            %
            %   Example:
            %       s = std_elements([1, 2, 3, 4, 5])  % Returns 1.5811
            
            if nargin < 2
                s = std(arr(:));
            else
                s = std(arr, 0, dim);
            end
        end
        
        function v = var_elements(arr, dim)
            %VAR_ELEMENTS Variance of array elements
            %   v = var_elements(arr) - Variance of all elements
            %   v = var_elements(arr, dim) - Variance along dimension
            %
            %   Example:
            %       v = var_elements([1, 2, 3, 4, 5])  % Returns 2.5
            
            if nargin < 2
                v = var(arr(:));
            else
                v = var(arr, 0, dim);
            end
        end
        
        function c = cumsum_elements(arr, dim)
            %CUMSUM_ELEMENTS Cumulative sum of elements
            %   c = cumsum_elements(arr) - Cumulative sum
            %   c = cumsum_elements(arr, dim) - Cumulative sum along dimension
            %
            %   Example:
            %       c = cumsum_elements([1, 2, 3, 4])  % Returns [1, 3, 6, 10]
            
            if nargin < 2
                c = cumsum(arr(:));
            else
                c = cumsum(arr, dim);
            end
        end
        
        function c = cumprod_elements(arr, dim)
            %CUMPROD_ELEMENTS Cumulative product of elements
            %   c = cumprod_elements(arr) - Cumulative product
            %   c = cumprod_elements(arr, dim) - Cumulative product along dimension
            %
            %   Example:
            %       c = cumprod_elements([1, 2, 3, 4])  % Returns [1, 2, 6, 24]
            
            if nargin < 2
                c = cumprod(arr(:));
            else
                c = cumprod(arr, dim);
            end
        end
        
        function arr = diff_elements(arr, dim)
            %DIFF_ELEMENTS Differences between adjacent elements
            %   result = diff_elements(arr) - First-order differences
            %   result = diff_elements(arr, dim) - Differences along dimension
            %
            %   Example:
            %       arr = diff_elements([1, 3, 6, 10])  % Returns [2, 3, 4]
            
            if nargin < 2
                arr = diff(arr(:));
            else
                arr = diff(arr, 1, dim);
            end
        end
        
        %% Array Comparison
        
        function tf = all_elements(arr, dim)
            %ALL_ELEMENTS Test if all elements are non-zero or true
            %   tf = all_elements(arr) - Test all elements
            %   tf = all_elements(arr, dim) - Test along dimension
            %
            %   Example:
            %       tf = all_elements([1, 1, 1])  % Returns true
            %       tf = all_elements([1, 0, 1])  % Returns false
            
            if nargin < 2
                tf = all(arr(:));
            else
                tf = all(arr, dim);
            end
        end
        
        function tf = any_elements(arr, dim)
            %ANY_ELEMENTS Test if any element is non-zero or true
            %   tf = any_elements(arr) - Test any element
            %   tf = any_elements(arr, dim) - Test along dimension
            %
            %   Example:
            %       tf = any_elements([0, 0, 1])  % Returns true
            %       tf = any_elements([0, 0, 0])  % Returns false
            
            if nargin < 2
                tf = any(arr(:));
            else
                tf = any(arr, dim);
            end
        end
        
        function tf = is_equal(a, b, tolerance)
            %IS_EQUAL Check if two arrays are equal
            %   tf = is_equal(a, b) - Exact equality check
            %   tf = is_equal(a, b, tolerance) - Equality within tolerance
            %
            %   Example:
            %       tf = is_equal([1, 2, 3], [1, 2, 3])  % Returns true
            %       tf = is_equal([1.0, 2.0], [1.0, 2.0001], 0.001)  % Returns true
            
            if nargin < 3
                tf = isequal(a, b);
            else
                tf = all(abs(a(:) - b(:)) <= tolerance);
            end
        end
        
        %% Array Concatenation and Splitting
        
        function arr = concatenate(varargin)
            %CONCATENATE Concatenate arrays along a specified dimension
            %   result = concatenate(dim, arr1, arr2, ...) - Concatenate along dim
            %
            %   Example:
            %       arr = concatenate(1, [1, 2], [3, 4])  % Returns [1, 2; 3, 4]
            %       arr = concatenate(2, [1; 2], [3; 4])  % Returns [1, 3; 2, 4]
            
            dim = varargin{1};
            arrays = varargin(2:end);
            arr = cat(dim, arrays{:});
        end
        
        function arr = stack(arrays, dim)
            %STACK Stack arrays along a new dimension
            %   result = stack(arrays, dim) - Stack arrays
            %
            %   Example:
            %       arr = stack({[1, 2], [3, 4]}, 1)  % Returns 2x2 matrix
            
            if nargin < 2
                dim = 1;
            end
            arr = cat(dim, arrays{:});
        end
        
        function arrays = split(arr, dim, indices)
            %SPLIT Split an array into multiple arrays along a dimension
            %   arrays = split(arr, dim, indices) - Split at specified indices
            %
            %   Example:
            %       arrays = split([1, 2, 3, 4, 5], 2, [2, 4])
            %       % Returns {[1, 2], [3, 4], [5]}
            
            if nargin < 3
                indices = floor(size(arr, dim) / 2);
            end
            
            arrays = cell(1, length(indices) + 1);
            start_idx = 1;
            
            for i = 1:length(indices)
                idx = cell(1, ndims(arr));
                for d = 1:ndims(arr)
                    if d == dim
                        idx{d} = start_idx:indices(i);
                    else
                        idx{d} = ':';
                    end
                end
                arrays{i} = arr(idx{:});
                start_idx = indices(i) + 1;
            end
            
            % Last piece
            idx = cell(1, ndims(arr));
            for d = 1:ndims(arr)
                if d == dim
                    idx{d} = start_idx:size(arr, dim);
                else
                    idx{d} = ':';
                end
            end
            arrays{end} = arr(idx{:});
        end
        
        function arr = tile(arr, reps)
            %TILE Replicate and tile an array
            %   result = tile(arr, reps) - Tile array reps times
            %
            %   Example:
            %       arr = tile([1, 2], [2, 3])  % Returns 2x6 matrix
            
            arr = repmat(arr, reps);
        end
        
        %% Array Indexing and Selection
        
        function arr = slice(arr, varargin)
            %SLICE Extract a slice from an array
            %   result = slice(arr, idx1, idx2, ...) - Extract slice
            %
            %   Example:
            %       arr = slice([1, 2, 3; 4, 5, 6], 1, 2:3)  % Returns [2, 3]
            
            arr = arr(varargin{:});
        end
        
        function arr = select(arr, indices)
            %SELECT Select elements by linear indices
            %   result = select(arr, indices) - Select elements
            %
            %   Example:
            %       arr = select([10, 20, 30, 40], [1, 3])  % Returns [10, 30]
            
            arr = arr(indices);
        end
        
        function arr = where(condition, true_val, false_val)
            %WHERE Select elements based on a condition
            %   result = where(condition, true_val, false_val)
            %
            %   Example:
            %       arr = where([1, 2, 3] > 2, 100, 0)  % Returns [0, 0, 100]
            
            arr = false_val;
            arr(condition) = true_val(condition);
        end
        
        %% Array Statistics
        
        function m = median_elements(arr, dim)
            %MEDIAN_ELEMENTS Median of array elements
            %   m = median_elements(arr) - Median of all elements
            %   m = median_elements(arr, dim) - Median along dimension
            %
            %   Example:
            %       m = median_elements([1, 2, 3, 4, 5])  % Returns 3
            
            if nargin < 2
                m = median(arr(:));
            else
                m = median(arr, dim);
            end
        end
        
        function r = range_elements(arr, dim)
            %RANGE_ELEMENTS Range (max - min) of array elements
            %   r = range_elements(arr) - Range of all elements
            %   r = range_elements(arr, dim) - Range along dimension
            %
            %   Example:
            %       r = range_elements([1, 3, 5, 7, 9])  % Returns 8
            
            if nargin < 2
                r = max(arr(:)) - min(arr(:));
            else
                r = max(arr, [], dim) - min(arr, [], dim);
            end
        end
        
        function q = quantile_elements(arr, p, dim)
            %QUANTILE_ELEMENTS Quantiles of array elements
            %   q = quantile_elements(arr, p) - Compute p-th quantile
            %   q = quantile_elements(arr, p, dim) - Quantile along dimension
            %
            %   Example:
            %       q = quantile_elements([1, 2, 3, 4, 5], 0.5)  % Returns 3 (median)
            
            if nargin < 3
                q = quantile(arr(:), p);
            else
                q = quantile(arr, p, dim);
            end
        end
        
        %% Array Normalization
        
        function arr = normalize_minmax(arr, dim)
            %NORMALIZE_MINMAX Normalize array to [0, 1] range
            %   result = normalize_minmax(arr) - Normalize all elements
            %   result = normalize_minmax(arr, dim) - Normalize along dimension
            %
            %   Example:
            %       arr = normalize_minmax([1, 2, 3, 4, 5])  % Returns [0, 0.25, 0.5, 0.75, 1]
            
            if nargin < 2
                min_val = min(arr(:));
                max_val = max(arr(:));
                range_val = max_val - min_val;
                if range_val == 0
                    arr = zeros(size(arr));
                else
                    arr = (arr - min_val) / range_val;
                end
            else
                min_val = min(arr, [], dim);
                max_val = max(arr, [], dim);
                range_val = max_val - min_val;
                arr = (arr - min_val) ./ range_val;
            end
        end
        
        function arr = normalize_zscore(arr, dim)
            %NORMALIZE_ZSCORE Z-score normalize array (zero mean, unit variance)
            %   result = normalize_zscore(arr) - Z-score normalize
            %   result = normalize_zscore(arr, dim) - Normalize along dimension
            %
            %   Example:
            %       arr = normalize_zscore([1, 2, 3, 4, 5])
            %       % Returns approximately [-1.26, -0.63, 0, 0.63, 1.26]
            
            if nargin < 2
                m = mean(arr(:));
                s = std(arr(:));
                if s == 0
                    arr = zeros(size(arr));
                else
                    arr = (arr - m) / s;
                end
            else
                m = mean(arr, dim);
                s = std(arr, 0, dim);
                arr = (arr - m) ./ s;
            end
        end
        
        %% Array Clipping and Thresholding
        
        function arr = clip(arr, min_val, max_val)
            %CLIP Clip array values to a specified range
            %   result = clip(arr, min_val, max_val) - Clip to [min_val, max_val]
            %
            %   Example:
            %       arr = clip([-1, 0, 5, 10, 15], 0, 10)  % Returns [0, 0, 5, 10, 10]
            
            arr = max(min(arr, max_val), min_val);
        end
        
        function arr = threshold(arr, thresh, value)
            %THRESHOLD Apply threshold to array
            %   result = threshold(arr, thresh) - Set values below thresh to 0
            %   result = threshold(arr, thresh, value) - Set to specified value
            %
            %   Example:
            %       arr = threshold([1, 5, 10, 15], 8)  % Returns [0, 0, 10, 15]
            
            if nargin < 3
                value = 0;
            end
            arr(arr < thresh) = value;
        end
        
        %% Array Filling
        
        function arr = fill_missing(arr, method)
            %FILL_MISSING Fill missing values (NaN) in an array
            %   result = fill_missing(arr, method) - Fill using specified method
            %   Methods: 'linear', 'nearest', 'next', 'previous', 'mean', 'median'
            %
            %   Example:
            %       arr = fill_missing([1, NaN, 3, NaN, 5], 'linear')
            %       % Returns [1, 2, 3, 4, 5]
            
            if nargin < 2
                method = 'linear';
            end
            
            nan_idx = isnan(arr);
            if ~any(nan_idx)
                return;
            end
            
            switch lower(method)
                case 'linear'
                    arr = fillmissing(arr, 'linear');
                case 'nearest'
                    arr = fillmissing(arr, 'nearest');
                case 'next'
                    arr = fillmissing(arr, 'next');
                case 'previous'
                    arr = fillmissing(arr, 'previous');
                case 'mean'
                    arr(nan_idx) = mean(arr(~nan_idx));
                case 'median'
                    arr(nan_idx) = median(arr(~nan_idx));
                otherwise
                    arr = fillmissing(arr, 'linear');
            end
        end
        
        function arr = replace_value(arr, old_val, new_val)
            %REPLACE_VALUE Replace all occurrences of a value
            %   result = replace_value(arr, old_val, new_val)
            %
            %   Example:
            %       arr = replace_value([1, 2, 1, 3, 1], 1, 0)  % Returns [0, 2, 0, 3, 0]
            
            arr(arr == old_val) = new_val;
        end
        
        %% Array Search
        
        function idx = find_first(arr, val)
            %FIND_FIRST Find the first occurrence of a value
            %   idx = find_first(arr, val) - Return linear index
            %
            %   Example:
            %       idx = find_first([1, 2, 3, 2, 1], 2)  % Returns 2
            
            idx = find(arr == val, 1, 'first');
            if isempty(idx)
                idx = 0;
            end
        end
        
        function idx = find_last(arr, val)
            %FIND_LAST Find the last occurrence of a value
            %   idx = find_last(arr, val) - Return linear index
            %
            %   Example:
            %       idx = find_last([1, 2, 3, 2, 1], 2)  % Returns 4
            
            idx = find(arr == val, 1, 'last');
            if isempty(idx)
                idx = 0;
            end
        end
        
        function count = count_value(arr, val)
            %COUNT_VALUE Count occurrences of a value
            %   count = count_value(arr, val)
            %
            %   Example:
            %       count = count_value([1, 2, 1, 3, 1], 1)  % Returns 3
            
            count = sum(arr == val);
        end
        
        %% Array Reshaping Utilities
        
        function arr = expand_dims(arr, dim)
            %EXPAND_DIMS Expand the shape of an array by inserting a new axis
            %   result = expand_dims(arr, dim) - Insert axis at specified dimension
            %
            %   Example:
            %       arr = expand_dims([1, 2, 3], 1)  % Returns 1x3 row vector
            %       arr = expand_dims([1, 2, 3], 2)  % Returns 3x1 column vector
            
            sz = size(arr);
            new_sz = [sz(1:dim-1), 1, sz(dim:end)];
            arr = reshape(arr, new_sz);
        end
        
        function arr = squeeze_dims(arr)
            %SQUEEZE_DIMS Remove singleton dimensions from an array
            %   result = squeeze_dims(arr)
            %
            %   Example:
            %       arr = squeeze_dims(ones(1, 3, 1, 4))  % Returns 3x4 matrix
            
            arr = squeeze(arr);
        end
        
        %% Array Type Checking
        
        function tf = is_numeric(arr)
            %IS_NUMERIC Check if array is numeric
            %   tf = is_numeric(arr)
            
            tf = isnumeric(arr);
        end
        
        function tf = is_integer(arr)
            %IS_INTEGER Check if array contains only integers
            %   tf = is_integer(arr)
            
            tf = all(arr == floor(arr));
        end
        
        function tf = is_finite(arr)
            %IS_FINITE Check if all elements are finite
            %   tf = is_finite(arr)
            
            tf = all(isfinite(arr(:)));
        end
        
        function tf = has_nan(arr)
            %HAS_NAN Check if array contains any NaN values
            %   tf = has_nan(arr)
            
            tf = any(isnan(arr(:)));
        end
        
        function tf = has_inf(arr)
            %HAS_INF Check if array contains any Inf values
            %   tf = has_inf(arr)
            
            tf = any(isinf(arr(:)));
        end
    end
end
