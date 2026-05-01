%% matrix_utils 使用示例
% 演示 matrix_utils 的主要功能
% 作者: AllToolkit 自动生成
% 日期: 2026-05-01

fprintf('\n========================================\n');
fprintf('  matrix_utils 使用示例\n');
fprintf('========================================\n\n');

%% 示例 1: 图像处理中的旋转和翻转
fprintf('=== 示例 1: 图像处理 ===\n');

% 创建一个简单的"图像"矩阵
img = [0 0 0 0 0;
       0 1 1 1 0;
       0 1 0 1 0;
       0 1 1 1 0;
       0 0 0 0 0];

fprintf('原始图像 (5x5):\n');
disp(img);

fprintf('旋转90度:\n');
disp(matrix_utils.rotate90(img));

fprintf('水平翻转:\n');
disp(matrix_utils.flip_horizontal(img));

%% 示例 2: 分块处理大矩阵
fprintf('\n=== 示例 2: 分块处理 ===\n');

% 创建一个8x8的块状矩阵
block_a = ones(4, 4) * 1;
block_b = ones(4, 4) * 2;
big_matrix = [block_a, block_b; block_b, block_a];

fprintf('8x8块状矩阵:\n');
disp(big_matrix);

% 分成4x4的块
blocks = matrix_utils.block_split(big_matrix, [4, 4]);
fprintf('分割后的块数量: %d\n', numel(blocks));
fprintf('块(1,1):\n');
disp(blocks{1,1});

%% 示例 3: 矩阵填充
fprintf('\n=== 示例 3: 矩阵填充 ===\n');

small = [1 2; 3 4];
fprintf('原始矩阵:\n');
disp(small);

fprintf('Constant填充 (周围补0):\n');
padded = matrix_utils.pad_matrix(small, [2, 2, 2, 2]);
disp(padded);

fprintf('Replicate填充 (复制边界):\n');
padded = matrix_utils.pad_matrix(small, [1, 1, 1, 1], 'mode', 'replicate');
disp(padded);

%% 示例 4: 统计分析
fprintf('\n=== 示例 4: 统计分析 ===\n');

data = rand(100, 100);  % 100x100随机数据
stats = matrix_utils.matrix_stats(data);

fprintf('数据统计:\n');
fprintf('  最小值: %.4f\n', stats.min);
fprintf('  最大值: %.4f\n', stats.max);
fprintf('  均值: %.4f\n', stats.mean);
fprintf('  中位数: %.4f\n', stats.median);
fprintf('  标准差: %.4f\n', stats.std);
fprintf('  非零元素: %d\n', stats.nnz);

%% 示例 5: 滑动窗口处理
fprintf('\n=== 示例 5: 滑动窗口 ===\n');

% 创建测试矩阵
test = reshape(1:16, 4, 4);
fprintf('测试矩阵:\n');
disp(test);

% 3x3滑动窗口
windows = matrix_utils.sliding_window(test, [3, 3]);
fprintf('3x3滑动窗口数量: %d\n', numel(windows));
fprintf('第一个窗口:\n');
disp(windows{1,1});

%% 示例 6: 矩阵分解
fprintf('\n=== 示例 6: 矩阵分解 ===\n');

% 创建测试矩阵
test = [1 2 3; 4 5 6; 7 8 10];
fprintf('测试矩阵:\n');
disp(test);

% SVD分解
[U, S, V] = matrix_utils.svd_decompose(test);
fprintf('奇异值: ');
fprintf('%.4f ', diag(S)');
fprintf('\n');

% 特征值分解
[vals, vecs] = matrix_utils.eigen(test);
fprintf('特征值: ');
fprintf('%.4f ', vals);
fprintf('\n');

%% 示例 7: 数据标准化
fprintf('\n=== 示例 7: 数据标准化 ===\n');

% 创建测试数据
data = [100, 200, 300; 150, 250, 350; 200, 300, 400];
fprintf('原始数据:\n');
disp(data);

% Min-Max标准化
normalized = matrix_utils.normalize(data, 'method', 'minmax');
fprintf('MinMax标准化后:\n');
disp(normalized);
fprintf('范围: [%.4f, %.4f]\n', min(normalized(:)), max(normalized(:)));

% Z-score标准化
zscored = matrix_utils.normalize(data, 'method', 'zscore');
fprintf('Z-score标准化后:\n');
disp(zscored);
fprintf('均值: %.4f, 标准差: %.4f\n', mean(zscored(:)), std(zscored(:)));

%% 示例 8: 矩阵操作组合
fprintf('\n=== 示例 8: 组合操作 ===\n');

% 创建矩阵
A = reshape(1:9, 3, 3);
fprintf('原始矩阵:\n');
disp(A);

% 分块 -> 处理 -> 合并
blocks = matrix_utils.block_split(A, [2, 2]);
for i = 1:size(blocks, 1)
    for j = 1:size(blocks, 2)
        % 对每个块进行处理（如：乘以索引）
        blocks{i, j} = blocks{i, j} * (i + j);
    end
end
result = matrix_utils.block_merge(blocks);

fprintf('处理后的矩阵:\n');
disp(result);

fprintf('\n========================================\n');
fprintf('  示例演示完成！\n');
fprintf('========================================\n');