classdef matrix_utils
    % MATRIX_UTILS 矩阵操作工具集
    % 提供常用的矩阵操作函数，零外部依赖
    %
    % 作者: AllToolkit 自动生成
    % 日期: 2026-05-01
    % 版本: 1.0.0
    %
    % 主要功能:
    %   - 矩阵旋转 (rotate90, rotate180, rotate270)
    %   - 矩阵翻转 (flip_horizontal, flip_vertical)
    %   - 矩阵分块 (block_split, block_merge)
    %   - 矩阵填充 (pad_matrix)
    %   - 矩阵统计 (matrix_stats)
    %   - 矩阵切片 (slice_extract, slice_insert)
    %   - 矩阵卷积 (convolve2d)
    %   - 矩阵滑动窗口 (sliding_window)
    
    methods(Static)
        
        %% 矩阵旋转90度（顺时针）
        function B = rotate90(A)
            % ROTATE90 将矩阵顺时针旋转90度
            %   B = rotate90(A) 返回矩阵A顺时针旋转90度的结果
            %
            % 输入:
            %   A - 输入矩阵
            %
            % 输出:
            %   B - 旋转后的矩阵
            %
            % 示例:
            %   A = [1 2 3; 4 5 6];
            %   B = matrix_utils.rotate90(A)
            %   % B = [4 1; 5 2; 6 3]
            
            B = rot90(A, -1);
        end
        
        %% 矩阵旋转180度
        function B = rotate180(A)
            % ROTATE180 将矩阵旋转180度
            %   B = rotate180(A) 返回矩阵A旋转180度的结果
            %
            % 输入:
            %   A - 输入矩阵
            %
            % 输出:
            %   B - 旋转后的矩阵
            %
            % 示例:
            %   A = [1 2 3; 4 5 6];
            %   B = matrix_utils.rotate180(A)
            %   % B = [6 5 4; 3 2 1]
            
            B = rot90(A, 2);
        end
        
        %% 矩阵旋转270度（逆时针90度）
        function B = rotate270(A)
            % ROTATE270 将矩阵逆时针旋转90度（顺时针270度）
            %   B = rotate270(A) 返回矩阵A逆时针旋转90度的结果
            %
            % 输入:
            %   A - 输入矩阵
            %
            % 输出:
            %   B - 旋转后的矩阵
            %
            % 示例:
            %   A = [1 2 3; 4 5 6];
            %   B = matrix_utils.rotate270(A)
            %   % B = [3 6; 2 5; 1 4]
            
            B = rot90(A, 1);
        end
        
        %% 水平翻转
        function B = flip_horizontal(A)
            % FLIP_HORIZONTAL 水平翻转矩阵（左右镜像）
            %   B = flip_horizontal(A) 返回矩阵A水平翻转的结果
            %
            % 输入:
            %   A - 输入矩阵
            %
            % 输出:
            %   B - 翻转后的矩阵
            %
            % 示例:
            %   A = [1 2 3; 4 5 6];
            %   B = matrix_utils.flip_horizontal(A)
            %   % B = [3 2 1; 6 5 4]
            
            B = fliplr(A);
        end
        
        %% 垂直翻转
        function B = flip_vertical(A)
            % FLIP_VERTICAL 垂直翻转矩阵（上下镜像）
            %   B = flip_vertical(A) 返回矩阵A垂直翻转的结果
            %
            % 输入:
            %   A - 输入矩阵
            %
            % 输出:
            %   B - 翻转后的矩阵
            %
            % 示例:
            %   A = [1 2 3; 4 5 6];
            %   B = matrix_utils.flip_vertical(A)
            %   % B = [4 5 6; 1 2 3]
            
            B = flipud(A);
        end
        
        %% 矩阵分块
        function blocks = block_split(A, block_size)
            % BLOCK_SPLIT 将矩阵分割成小块
            %   blocks = block_split(A, block_size) 将矩阵A分割成指定大小的块
            %
            % 输入:
            %   A          - 输入矩阵
            %   block_size - [rows, cols] 块大小，默认 [2, 2]
            %
            % 输出:
            %   blocks - cell数组，包含所有块
            %
            % 示例:
            %   A = [1 2 3 4; 5 6 7 8; 9 10 11 12; 13 14 15 16];
            %   blocks = matrix_utils.block_split(A, [2, 2])
            %   % blocks{1,1} = [1 2; 5 6]
            %   % blocks{1,2} = [3 4; 7 8]
            %   % blocks{2,1} = [9 10; 13 14]
            %   % blocks{2,2} = [11 12; 15 16]
            
            if nargin < 2
                block_size = [2, 2];
            end
            
            [m, n] = size(A);
            br = block_size(1);
            bc = block_size(2);
            
            % 计算块的数量
            num_blocks_r = ceil(m / br);
            num_blocks_c = ceil(n / bc);
            
            blocks = cell(num_blocks_r, num_blocks_c);
            
            for i = 1:num_blocks_r
                for j = 1:num_blocks_c
                    r_start = (i-1) * br + 1;
                    r_end = min(i * br, m);
                    c_start = (j-1) * bc + 1;
                    c_end = min(j * bc, n);
                    blocks{i, j} = A(r_start:r_end, c_start:c_end);
                end
            end
        end
        
        %% 矩阵块合并
        function A = block_merge(blocks)
            % BLOCK_MERGE 将分块矩阵合并成完整矩阵
            %   A = block_merge(blocks) 将cell数组中的块合并成完整矩阵
            %
            % 输入:
            %   blocks - cell数组，包含所有块
            %
            % 输出:
            %   A - 合并后的矩阵
            %
            % 示例:
            %   blocks = {[1 2; 5 6], [3 4; 7 8]; [9 10; 13 14], [11 12; 15 16]};
            %   A = matrix_utils.block_merge(blocks)
            %   % A = [1 2 3 4; 5 6 7 8; 9 10 11 12; 13 14 15 16]
            
            [num_blocks_r, num_blocks_c] = size(blocks);
            
            % 获取每行每列的尺寸
            row_sizes = zeros(num_blocks_r, 1);
            col_sizes = zeros(num_blocks_c, 1);
            
            for i = 1:num_blocks_r
                row_sizes(i) = size(blocks{i, 1}, 1);
            end
            for j = 1:num_blocks_c
                col_sizes(j) = size(blocks{1, j}, 2);
            end
            
            % 构建完整矩阵
            A = zeros(sum(row_sizes), sum(col_sizes));
            
            r_start = 1;
            for i = 1:num_blocks_r
                c_start = 1;
                for j = 1:num_blocks_c
                    r_end = r_start + row_sizes(i) - 1;
                    c_end = c_start + col_sizes(j) - 1;
                    A(r_start:r_end, c_start:c_end) = blocks{i, j};
                    c_start = c_end + 1;
                end
                r_start = r_start + row_sizes(i);
            end
        end
        
        %% 矩阵填充
        function B = pad_matrix(A, pad_size, varargin)
            % PAD_MATRIX 对矩阵进行填充
            %   B = pad_matrix(A, pad_size) 用0填充矩阵
            %   B = pad_matrix(A, pad_size, 'value', v) 用指定值填充
            %   B = pad_matrix(A, pad_size, 'mode', mode) 指定填充模式
            %
            % 输入:
            %   A         - 输入矩阵
            %   pad_size  - [top, bottom, left, right] 填充大小
            %   varargin  - 可选参数:
            %               'value' - 填充值，默认0
            %               'mode'  - 填充模式: 'constant', 'replicate', 'symmetric'
            %
            % 输出:
            %   B - 填充后的矩阵
            %
            % 示例:
            %   A = [1 2; 3 4];
            %   B = matrix_utils.pad_matrix(A, [1, 1, 1, 1])
            %   % B = [0 0 0 0; 0 1 2 0; 0 3 4 0; 0 0 0 0]
            
            p = inputParser;
            addRequired(p, 'A');
            addRequired(p, 'pad_size');
            addParameter(p, 'value', 0);
            addParameter(p, 'mode', 'constant');
            parse(p, A, pad_size, varargin{:});
            
            [m, n] = size(A);
            top = pad_size(1);
            bottom = pad_size(2);
            left = pad_size(3);
            right = pad_size(4);
            
            new_m = m + top + bottom;
            new_n = n + left + right;
            
            switch p.Results.mode
                case 'constant'
                    B = ones(new_m, new_n) * p.Results.value;
                    B(top+1:top+m, left+1:left+n) = A;
                    
                case 'replicate'
                    B = zeros(new_m, new_n);
                    B(top+1:top+m, left+1:left+n) = A;
                    % 上边
                    if top > 0
                        B(1:top, left+1:left+n) = repmat(A(1, :), top, 1);
                    end
                    % 下边
                    if bottom > 0
                        B(top+m+1:end, left+1:left+n) = repmat(A(end, :), bottom, 1);
                    end
                    % 左边
                    if left > 0
                        B(:, 1:left) = repmat(B(:, left+1), 1, left);
                    end
                    % 右边
                    if right > 0
                        B(:, end-right+1:end) = repmat(B(:, end-right), 1, right);
                    end
                    
                case 'symmetric'
                    B = zeros(new_m, new_n);
                    B(top+1:top+m, left+1:left+n) = A;
                    % 上边
                    if top > 0
                        B(1:top, left+1:left+n) = flipud(A(1:top, :));
                    end
                    % 下边
                    if bottom > 0
                        B(top+m+1:end, left+1:left+n) = flipud(A(end-bottom+1:end, :));
                    end
                    % 左边
                    if left > 0
                        B(:, 1:left) = fliplr(B(:, left+1:left*2));
                    end
                    % 右边
                    if right > 0
                        B(:, end-right+1:end) = fliplr(B(:, end-right*2+1:end-right));
                    end
            end
        end
        
        %% 矩阵统计
        function stats = matrix_stats(A)
            % MATRIX_STATS 计算矩阵的各种统计信息
            %   stats = matrix_stats(A) 返回包含统计信息的结构体
            %
            % 输入:
            %   A - 输入矩阵
            %
            % 输出:
            %   stats - 统计信息结构体，包含:
            %           .min - 最小值
            %           .max - 最大值
            %           .mean - 均值
            %           .median - 中位数
            %           .std - 标准差
            %           .var - 方差
            %           .sum - 总和
            %           .prod - 乘积
            %           .range - 极差
            %           .nnz - 非零元素数
            %           .size - 矩阵尺寸
            %
            % 示例:
            %   A = [1 2 3; 4 5 6];
            %   stats = matrix_utils.matrix_stats(A)
            
            stats.min = min(A(:));
            stats.max = max(A(:));
            stats.mean = mean(A(:));
            stats.median = median(A(:));
            stats.std = std(A(:));
            stats.var = var(A(:));
            stats.sum = sum(A(:));
            stats.prod = prod(A(:));
            stats.range = stats.max - stats.min;
            stats.nnz = nnz(A);
            stats.size = size(A);
            stats.nrows = size(A, 1);
            stats.ncols = size(A, 2);
            stats.nelements = numel(A);
        end
        
        %% 切片提取
        function slice = slice_extract(A, start_pos, slice_size)
            % SLICE_EXTRACT 从矩阵中提取切片
            %   slice = slice_extract(A, start_pos, slice_size) 提取指定位置的切片
            %
            % 输入:
            %   A           - 输入矩阵
            %   start_pos   - [row, col] 起始位置（从1开始）
            %   slice_size  - [rows, cols] 切片大小
            %
            % 输出:
            %   slice - 提取的切片
            %
            % 示例:
            %   A = [1 2 3 4; 5 6 7 8; 9 10 11 12];
            %   slice = matrix_utils.slice_extract(A, [2, 2], [2, 3])
            %   % slice = [6 7 8; 10 11 12]
            
            [m, n] = size(A);
            r_start = start_pos(1);
            c_start = start_pos(2);
            r_size = slice_size(1);
            c_size = slice_size(2);
            
            r_end = min(r_start + r_size - 1, m);
            c_end = min(c_start + c_size - 1, n);
            
            slice = A(r_start:r_end, c_start:c_end);
        end
        
        %% 切片插入
        function B = slice_insert(A, slice, start_pos)
            % SLICE_INSERT 将切片插入到矩阵指定位置
            %   B = slice_insert(A, slice, start_pos) 将slice插入到A的指定位置
            %
            % 输入:
            %   A          - 输入矩阵
            %   slice      - 要插入的切片
            %   start_pos  - [row, col] 插入位置（从1开始）
            %
            % 输出:
            %   B - 插入后的矩阵
            %
            % 示例:
            %   A = [1 2 3; 4 5 6; 7 8 9];
            %   slice = [99 99; 99 99];
            %   B = matrix_utils.slice_insert(A, slice, [2, 2])
            %   % B = [1 2 3; 4 99 99; 7 99 99]
            
            B = A;
            [m, n] = size(A);
            [sr, sc] = size(slice);
            r_start = start_pos(1);
            c_start = start_pos(2);
            
            r_end = min(r_start + sr - 1, m);
            c_end = min(c_start + sc - 1, n);
            
            B(r_start:r_end, c_start:c_end) = slice(1:r_end-r_start+1, 1:c_end-c_start+1);
        end
        
        %% 二维卷积
        function C = convolve2d(A, kernel, varargin)
            % CONVOLVE2D 对矩阵进行二维卷积
            %   C = convolve2d(A, kernel) 执行二维卷积
            %   C = convolve2d(A, kernel, 'mode', mode) 指定卷积模式
            %
            % 输入:
            %   A       - 输入矩阵
            %   kernel  - 卷积核
            %   varargin - 可选参数:
            %              'mode' - 卷积模式: 'full', 'same', 'valid'
            %
            % 输出:
            %   C - 卷积结果
            %
            % 示例:
            %   A = [1 2 3; 4 5 6; 7 8 9];
            %   kernel = [1 0; 0 1];
            %   C = matrix_utils.convolve2d(A, kernel)
            %   % 使用MATLAB内置conv2函数实现
            
            p = inputParser;
            addRequired(p, 'A');
            addRequired(p, 'kernel');
            addParameter(p, 'mode', 'same');
            parse(p, A, kernel, varargin{:});
            
            C = conv2(A, kernel, p.Results.mode);
        end
        
        %% 滑动窗口
        function windows = sliding_window(A, window_size, varargin)
            % SLIDING_WINDOW 创建滑动窗口视图
            %   windows = sliding_window(A, window_size) 创建滑动窗口
            %   windows = sliding_window(A, window_size, 'stride', s) 指定步长
            %
            % 输入:
            %   A            - 输入矩阵
            %   window_size  - [rows, cols] 窗口大小
            %   varargin     - 可选参数:
            %                  'stride' - 步长，默认 [1, 1]
            %
            % 输出:
            %   windows - cell数组，包含所有窗口
            %
            % 示例:
            %   A = [1 2 3 4; 5 6 7 8; 9 10 11 12];
            %   windows = matrix_utils.sliding_window(A, [2, 2])
            %   % 返回所有 2x2 的滑动窗口
            
            p = inputParser;
            addRequired(p, 'A');
            addRequired(p, 'window_size');
            addParameter(p, 'stride', [1, 1]);
            parse(p, A, window_size, varargin{:});
            
            [m, n] = size(A);
            wr = window_size(1);
            wc = window_size(2);
            stride = p.Results.stride;
            sr = stride(1);
            sc = stride(2);
            
            % 计算窗口数量
            num_windows_r = floor((m - wr) / sr) + 1;
            num_windows_c = floor((n - wc) / sc) + 1;
            
            windows = cell(num_windows_r, num_windows_c);
            
            for i = 1:num_windows_r
                for j = 1:num_windows_c
                    r_start = (i-1) * sr + 1;
                    r_end = r_start + wr - 1;
                    c_start = (j-1) * sc + 1;
                    c_end = c_start + wc - 1;
                    windows{i, j} = A(r_start:r_end, c_start:c_end);
                end
            end
        end
        
        %% 矩阵主对角线元素提取
        function d = diagonal(A, k)
            % DIAGONAL 提取矩阵的对角线元素
            %   d = diagonal(A) 提取主对角线
            %   d = diagonal(A, k) 提取第k条对角线
            %
            % 输入:
            %   A - 输入矩阵
            %   k - 对角线索引（可选），默认0（主对角线）
            %       k > 0: 主对角线以上
            %       k < 0: 主对角线以下
            %
            % 输出:
            %   d - 对角线元素向量
            %
            % 示例:
            %   A = [1 2 3; 4 5 6; 7 8 9];
            %   d = matrix_utils.diagonal(A)      % [1, 5, 9]
            %   d = matrix_utils.diagonal(A, 1)   % [2, 6]
            %   d = matrix_utils.diagonal(A, -1)  % [4, 8]
            
            if nargin < 2
                k = 0;
            end
            d = diag(A, k);
        end
        
        %% 创建对角矩阵
        function D = diagonal_matrix(v, k)
            % DIAGONAL_MATRIX 从向量创建对角矩阵
            %   D = diagonal_matrix(v) 将向量v放在主对角线上
            %   D = diagonal_matrix(v, k) 将向量v放在第k条对角线上
            %
            % 输入:
            %   v - 输入向量
            %   k - 对角线索引（可选），默认0
            %
            % 输出:
            %   D - 对角矩阵
            %
            % 示例:
            %   D = matrix_utils.diagonal_matrix([1, 2, 3])
            %   % D = [1 0 0; 0 2 0; 0 0 3]
            
            if nargin < 2
                k = 0;
            end
            D = diag(v, k);
        end
        
        %% 矩阵行列式
        function det_val = determinant(A)
            % DETERMINANT 计算矩阵的行列式
            %   det_val = determinant(A) 返回矩阵A的行列式
            %
            % 输入:
            %   A - 方阵
            %
            % 输出:
            %   det_val - 行列式值
            %
            % 示例:
            %   A = [1 2; 3 4];
            %   d = matrix_utils.determinant(A)  % -2
            
            det_val = det(A);
        end
        
        %% 矩阵逆
        function inv_A = inverse(A)
            % INVERSE 计算矩阵的逆
            %   inv_A = inverse(A) 返回矩阵A的逆矩阵
            %
            % 输入:
            %   A - 可逆方阵
            %
            % 输出:
            %   inv_A - 逆矩阵
            %
            % 示例:
            %   A = [1 2; 3 4];
            %   inv_A = matrix_utils.inverse(A)
            
            inv_A = inv(A);
        end
        
        %% 矩阵伪逆
        function pinv_A = pseudo_inverse(A)
            % PSEUDO_INVERSE 计算矩阵的伪逆（Moore-Penrose逆）
            %   pinv_A = pseudo_inverse(A) 返回矩阵A的伪逆
            %
            % 输入:
            %   A - 任意矩阵
            %
            % 输出:
            %   pinv_A - 伪逆矩阵
            %
            % 示例:
            %   A = [1 2 3; 4 5 6];
            %   pinv_A = matrix_utils.pseudo_inverse(A)
            
            pinv_A = pinv(A);
        end
        
        %% 矩阵特征值和特征向量
        function [eigenvalues, eigenvectors] = eigen(A)
            % EIGEN 计算矩阵的特征值和特征向量
            %   eigenvalues = eigen(A) 仅返回特征值
            %   [eigenvalues, eigenvectors] = eigen(A) 返回特征值和特征向量
            %
            % 输入:
            %   A - 方阵
            %
            % 输出:
            %   eigenvalues  - 特征值向量
            %   eigenvectors - 特征向量矩阵
            %
            % 示例:
            %   A = [1 2; 3 4];
            %   [vals, vecs] = matrix_utils.eigen(A)
            
            [eigenvectors, eigenvalues] = eig(A);
            eigenvalues = diag(eigenvalues);
        end
        
        %% 矩阵SVD分解
        function [U, S, V] = svd_decompose(A)
            % SVD_DECOMPOSE 奇异值分解
            %   [U, S, V] = svd_decompose(A) 执行奇异值分解
            %
            % 输入:
            %   A - 输入矩阵
            %
            % 输出:
            %   U - 左奇异向量矩阵
            %   S - 奇异值对角矩阵
            %   V - 右奇异向量矩阵
            %
            % 示例:
            %   A = [1 2 3; 4 5 6];
            %   [U, S, V] = matrix_utils.svd_decompose(A)
            
            [U, S, V] = svd(A);
        end
        
        %% 矩阵QR分解
        function [Q, R] = qr_decompose(A)
            % QR_DECOMPOSE QR分解
            %   [Q, R] = qr_decompose(A) 执行QR分解
            %
            % 输入:
            %   A - 输入矩阵
            %
            % 输出:
            %   Q - 正交矩阵
            %   R - 上三角矩阵
            %
            % 示例:
            %   A = [1 2; 3 4; 5 6];
            %   [Q, R] = matrix_utils.qr_decompose(A)
            
            [Q, R] = qr(A);
        end
        
        %% 矩阵LU分解
        function [L, U, P] = lu_decompose(A)
            % LU_DECOMPOSE LU分解
            %   [L, U, P] = lu_decompose(A) 执行带置换的LU分解
            %
            % 输入:
            %   A - 方阵
            %
            % 输出:
            %   L - 下三角矩阵
            %   U - 上三角矩阵
            %   P - 置换矩阵
            %
            % 示例:
            %   A = [1 2 3; 4 5 6; 7 8 10];
            %   [L, U, P] = matrix_utils.lu_decompose(A)
            
            [L, U, P] = lu(A);
        end
        
        %% 矩阵秩
        function r = matrix_rank(A)
            % MATRIX_RANK 计算矩阵的秩
            %   r = matrix_rank(A) 返回矩阵A的秩
            %
            % 输入:
            %   A - 输入矩阵
            %
            % 输出:
            %   r - 矩阵秩
            %
            % 示例:
            %   A = [1 2 3; 4 5 6; 7 8 9];
            %   r = matrix_utils.matrix_rank(A)  % 2
            
            r = rank(A);
        end
        
        %% 矩阵范数
        function n = matrix_norm(A, varargin)
            % MATRIX_NORM 计算矩阵范数
            %   n = matrix_norm(A) 计算2-范数
            %   n = matrix_norm(A, 'type', type) 计算指定类型范数
            %
            % 输入:
            %   A       - 输入矩阵
            %   varargin - 可选参数:
            %              'type' - 范数类型: 1, 2, inf, 'fro'
            %
            % 输出:
            %   n - 范数值
            %
            % 示例:
            %   A = [1 2; 3 4];
            %   n = matrix_utils.matrix_norm(A)
            %   n = matrix_utils.matrix_norm(A, 'type', 'fro')
            
            p = inputParser;
            addRequired(p, 'A');
            addParameter(p, 'type', 2);
            parse(p, A, varargin{:});
            
            n = norm(A, p.Results.type);
        end
        
        %% 创建单位矩阵
        function I = identity(n, m)
            % IDENTITY 创建单位矩阵
            %   I = identity(n) 创建n×n单位矩阵
            %   I = identity(n, m) 创建n×m单位矩阵（对角线上为1）
            %
            % 输入:
            %   n - 行数
            %   m - 列数（可选）
            %
            % 输出:
            %   I - 单位矩阵
            %
            % 示例:
            %   I = matrix_utils.identity(3)
            %   % I = [1 0 0; 0 1 0; 0 0 1]
            
            if nargin < 2
                m = n;
            end
            I = eye(n, m);
        end
        
        %% 创建全零矩阵
        function Z = zeros_matrix(m, n)
            % ZEROS_MATRIX 创建全零矩阵
            %   Z = zeros_matrix(m, n) 创建m×n全零矩阵
            %
            % 输入:
            %   m - 行数
            %   n - 列数
            %
            % 输出:
            %   Z - 全零矩阵
            %
            % 示例:
            %   Z = matrix_utils.zeros_matrix(3, 4)
            
            Z = zeros(m, n);
        end
        
        %% 创建全一矩阵
        function O = ones_matrix(m, n)
            % ONES_MATRIX 创建全一矩阵
            %   O = ones_matrix(m, n) 创建m×n全一矩阵
            %
            % 输入:
            %   m - 行数
            %   n - 列数
            %
            % 输出:
            %   O - 全一矩阵
            %
            % 示例:
            %   O = matrix_utils.ones_matrix(3, 4)
            
            O = ones(m, n);
        end
        
        %% 创建随机矩阵
        function R = random_matrix(m, n, varargin)
            % RANDOM_MATRIX 创建随机矩阵
            %   R = random_matrix(m, n) 创建m×n [0,1]均匀分布随机矩阵
            %   R = random_matrix(m, n, 'type', type) 指定分布类型
            %
            % 输入:
            %   m, n    - 矩阵尺寸
            %   varargin - 可选参数:
            %              'type' - 分布类型: 'uniform'(默认), 'normal'
            %              'seed' - 随机种子
            %
            % 输出:
            %   R - 随机矩阵
            %
            % 示例:
            %   R = matrix_utils.random_matrix(3, 4)
            %   R = matrix_utils.random_matrix(3, 4, 'type', 'normal')
            
            p = inputParser;
            addParameter(p, 'type', 'uniform');
            addParameter(p, 'seed', []);
            parse(p, varargin{:});
            
            if ~isempty(p.Results.seed)
                rng(p.Results.seed);
            end
            
            switch p.Results.type
                case 'uniform'
                    R = rand(m, n);
                case 'normal'
                    R = randn(m, n);
            end
        end
        
        %% 矩阵广播加法
        function C = broadcast_add(A, v, dim)
            % BROADCAST_ADD 广播加法
            %   C = broadcast_add(A, v, dim) 将向量v广播到矩阵A的指定维度
            %
            % 输入:
            %   A   - 输入矩阵
            %   v   - 输入向量
            %   dim - 维度: 1=按行广播, 2=按列广播
            %
            % 输出:
            %   C - 广播加法结果
            %
            % 示例:
            %   A = [1 2 3; 4 5 6];
            %   v = [10; 20];
            %   C = matrix_utils.broadcast_add(A, v, 2)
            %   % C = [11 12 13; 24 25 26]
            
            if dim == 1
                C = A + v';
            else
                C = A + v;
            end
        end
        
        %% 矩阵标准化
        function B = normalize(A, varargin)
            % NORMALIZE 矩阵标准化
            %   B = normalize(A) 按列标准化（z-score）
            %   B = normalize(A, 'method', method) 指定标准化方法
            %
            % 输入:
            %   A       - 输入矩阵
            %   varargin - 可选参数:
            %              'method' - 标准化方法: 'zscore', 'minmax'
            %              'dim'    - 维度: 1=按列, 2=按行
            %
            % 输出:
            %   B - 标准化后的矩阵
            %
            % 示例:
            %   A = [1 2; 3 4; 5 6];
            %   B = matrix_utils.normalize(A)
            %   B = matrix_utils.normalize(A, 'method', 'minmax')
            
            p = inputParser;
            addParameter(p, 'method', 'zscore');
            addParameter(p, 'dim', 1);
            parse(p, varargin{:});
            
            method = p.Results.method;
            dim = p.Results.dim;
            
            switch method
                case 'zscore'
                    if dim == 1
                        B = (A - mean(A, 1)) ./ std(A, 0, 1);
                    else
                        B = (A - mean(A, 2)) ./ std(A, 0, 2);
                    end
                    
                case 'minmax'
                    if dim == 1
                        B = (A - min(A, [], 1)) ./ (max(A, [], 1) - min(A, [], 1));
                    else
                        B = (A - min(A, [], 2)) ./ (max(A, [], 2) - min(A, [], 2));
                    end
            end
            
            % 处理NaN（当std=0或max=min时）
            B(isnan(B)) = 0;
        end
        
        %% 矩阵打印（美化输出）
        function print_matrix(A, varargin)
            % PRINT_MATRIX 美化打印矩阵
            %   print_matrix(A) 打印矩阵
            %   print_matrix(A, 'precision', p) 设置精度
            %
            % 输入:
            %   A       - 输入矩阵
            %   varargin - 可选参数:
            %              'precision' - 小数精度，默认4
            %              'name'      - 矩阵名称
            %
            % 示例:
            %   A = rand(3, 3);
            %   matrix_utils.print_matrix(A, 'name', 'Random Matrix')
            
            p = inputParser;
            addParameter(p, 'precision', 4);
            addParameter(p, 'name', 'Matrix');
            parse(p, varargin{:});
            
            fprintf('\n%s (%dx%d):\n', p.Results.name, size(A, 1), size(A, 2));
            fprintf(repmat('-', 1, 40));
            fprintf('\n');
            
            format_str = sprintf('%%.%df\t', p.Results.precision);
            
            for i = 1:size(A, 1)
                for j = 1:size(A, 2)
                    fprintf(format_str, A(i, j));
                end
                fprintf('\n');
            end
            fprintf(repmat('-', 1, 40));
            fprintf('\n');
        end
        
    end
end