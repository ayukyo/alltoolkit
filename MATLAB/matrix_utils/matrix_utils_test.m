%% matrix_utils 测试脚本
% 测试 matrix_utils 类的所有功能
% 作者: AllToolkit 自动生成
% 日期: 2026-05-01

fprintf('\n========================================\n');
fprintf('  matrix_utils 功能测试\n');
fprintf('========================================\n\n');

%% 测试计数器
total_tests = 0;
passed_tests = 0;

%% 辅助函数
function test_assert(condition, test_name, total, passed)
    total = total + 1;
    if condition
        fprintf('✓ %s: 通过\n', test_name);
        passed = passed + 1;
    else
        fprintf('✗ %s: 失败\n', test_name);
    end
end

%% 1. 测试旋转功能
fprintf('--- 测试矩阵旋转 ---\n');

A = [1 2 3; 4 5 6];
B = matrix_utils.rotate90(A);
expected = [4 1; 5 2; 6 3];
total_tests = total_tests + 1;
if isequal(B, expected)
    fprintf('✓ rotate90: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ rotate90: 失败\n');
end

B = matrix_utils.rotate180(A);
expected = [6 5 4; 3 2 1];
total_tests = total_tests + 1;
if isequal(B, expected)
    fprintf('✓ rotate180: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ rotate180: 失败\n');
end

B = matrix_utils.rotate270(A);
expected = [3 6; 2 5; 1 4];
total_tests = total_tests + 1;
if isequal(B, expected)
    fprintf('✓ rotate270: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ rotate270: 失败\n');
end

%% 2. 测试翻转功能
fprintf('\n--- 测试矩阵翻转 ---\n');

A = [1 2 3; 4 5 6];
B = matrix_utils.flip_horizontal(A);
expected = [3 2 1; 6 5 4];
total_tests = total_tests + 1;
if isequal(B, expected)
    fprintf('✓ flip_horizontal: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ flip_horizontal: 失败\n');
end

B = matrix_utils.flip_vertical(A);
expected = [4 5 6; 1 2 3];
total_tests = total_tests + 1;
if isequal(B, expected)
    fprintf('✓ flip_vertical: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ flip_vertical: 失败\n');
end

%% 3. 测试分块功能
fprintf('\n--- 测试矩阵分块 ---\n');

A = [1 2 3 4; 5 6 7 8; 9 10 11 12; 13 14 15 16];
blocks = matrix_utils.block_split(A, [2, 2]);
total_tests = total_tests + 1;
if isequal(blocks{1,1}, [1 2; 5 6]) && isequal(blocks{2,2}, [11 12; 15 16])
    fprintf('✓ block_split: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ block_split: 失败\n');
end

B = matrix_utils.block_merge(blocks);
total_tests = total_tests + 1;
if isequal(A, B)
    fprintf('✓ block_merge: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ block_merge: 失败\n');
end

%% 4. 测试填充功能
fprintf('\n--- 测试矩阵填充 ---\n');

A = [1 2; 3 4];
B = matrix_utils.pad_matrix(A, [1, 1, 1, 1]);
expected = [0 0 0 0; 0 1 2 0; 0 3 4 0; 0 0 0 0];
total_tests = total_tests + 1;
if isequal(B, expected)
    fprintf('✓ pad_matrix (constant): 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ pad_matrix (constant): 失败\n');
end

B = matrix_utils.pad_matrix(A, [1, 1, 1, 1], 'mode', 'replicate');
expected = [1 1 2 2; 1 1 2 2; 3 3 4 4; 3 3 4 4];
total_tests = total_tests + 1;
if isequal(B, expected)
    fprintf('✓ pad_matrix (replicate): 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ pad_matrix (replicate): 失败\n');
end

%% 5. 测试统计功能
fprintf('\n--- 测试矩阵统计 ---\n');

A = [1 2 3; 4 5 6];
stats = matrix_utils.matrix_stats(A);
total_tests = total_tests + 1;
if stats.min == 1 && stats.max == 6 && stats.sum == 21 && stats.nnz == 6
    fprintf('✓ matrix_stats: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ matrix_stats: 失败\n');
end

%% 6. 测试切片功能
fprintf('\n--- 测试矩阵切片 ---\n');

A = [1 2 3 4; 5 6 7 8; 9 10 11 12];
slice = matrix_utils.slice_extract(A, [2, 2], [2, 3]);
expected = [6 7 8; 10 11 12];
total_tests = total_tests + 1;
if isequal(slice, expected)
    fprintf('✓ slice_extract: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ slice_extract: 失败\n');
end

A = [1 2 3; 4 5 6; 7 8 9];
B = matrix_utils.slice_insert(A, [99 99; 99 99], [2, 2]);
expected = [1 2 3; 4 99 99; 7 99 99];
total_tests = total_tests + 1;
if isequal(B, expected)
    fprintf('✓ slice_insert: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ slice_insert: 失败\n');
end

%% 7. 测试滑动窗口
fprintf('\n--- 测试滑动窗口 ---\n');

A = [1 2 3 4; 5 6 7 8; 9 10 11 12];
windows = matrix_utils.sliding_window(A, [2, 2]);
total_tests = total_tests + 1;
if numel(windows) == 6 && isequal(windows{1,1}, [1 2; 5 6])
    fprintf('✓ sliding_window: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ sliding_window: 失败\n');
end

%% 8. 测试对角线功能
fprintf('\n--- 测试对角线功能 ---\n');

A = [1 2 3; 4 5 6; 7 8 9];
d = matrix_utils.diagonal(A);
expected = [1; 5; 9];
total_tests = total_tests + 1;
if isequal(d, expected)
    fprintf('✓ diagonal: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ diagonal: 失败\n');
end

D = matrix_utils.diagonal_matrix([1, 2, 3]);
expected = [1 0 0; 0 2 0; 0 0 3];
total_tests = total_tests + 1;
if isequal(D, expected)
    fprintf('✓ diagonal_matrix: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ diagonal_matrix: 失败\n');
end

%% 9. 测试矩阵运算
fprintf('\n--- 测试矩阵运算 ---\n');

A = [1 2; 3 4];
det_val = matrix_utils.determinant(A);
total_tests = total_tests + 1;
if det_val == -2
    fprintf('✓ determinant: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ determinant: 失败\n');
end

inv_A = matrix_utils.inverse(A);
total_tests = total_tests + 1;
if isequal(round(A * inv_A), eye(2))
    fprintf('✓ inverse: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ inverse: 失败\n');
end

%% 10. 测试矩阵分解
fprintf('\n--- 测试矩阵分解 ---\n');

A = [1 2 3; 4 5 6; 7 8 10];
[U, S, V] = matrix_utils.svd_decompose(A);
total_tests = total_tests + 1;
if norm(A - U*S*V') < 1e-10
    fprintf('✓ svd_decompose: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ svd_decompose: 失败\n');
end

[Q, R] = matrix_utils.qr_decompose(A);
total_tests = total_tests + 1;
if norm(A - Q*R) < 1e-10
    fprintf('✓ qr_decompose: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ qr_decompose: 失败\n');
end

[L, U, P] = matrix_utils.lu_decompose(A);
total_tests = total_tests + 1;
if norm(P*A - L*U) < 1e-10
    fprintf('✓ lu_decompose: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ lu_decompose: 失败\n');
end

%% 11. 测试特征值
fprintf('\n--- 测试特征值 ---\n');

A = [2 1; 1 2];
[vals, vecs] = matrix_utils.eigen(A);
total_tests = total_tests + 1;
if abs(vals(1) - 3) < 1e-10 || abs(vals(2) - 3) < 1e-10
    fprintf('✓ eigen: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ eigen: 失败\n');
end

%% 12. 测试矩阵创建
fprintf('\n--- 测试矩阵创建 ---\n');

I = matrix_utils.identity(3);
total_tests = total_tests + 1;
if isequal(I, eye(3))
    fprintf('✓ identity: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ identity: 失败\n');
end

Z = matrix_utils.zeros_matrix(2, 3);
total_tests = total_tests + 1;
if isequal(Z, zeros(2, 3))
    fprintf('✓ zeros_matrix: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ zeros_matrix: 失败\n');
end

O = matrix_utils.ones_matrix(2, 3);
total_tests = total_tests + 1;
if isequal(O, ones(2, 3))
    fprintf('✓ ones_matrix: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ ones_matrix: 失败\n');
end

R = matrix_utils.random_matrix(3, 3, 'seed', 42);
total_tests = total_tests + 1;
if size(R, 1) == 3 && size(R, 2) == 3
    fprintf('✓ random_matrix: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ random_matrix: 失败\n');
end

%% 13. 测试广播和标准化
fprintf('\n--- 测试广播和标准化 ---\n');

A = [1 2 3; 4 5 6];
v = [10; 20];
C = matrix_utils.broadcast_add(A, v, 2);
expected = [11 12 13; 24 25 26];
total_tests = total_tests + 1;
if isequal(C, expected)
    fprintf('✓ broadcast_add: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ broadcast_add: 失败\n');
end

A = [1 2 3; 4 5 6; 7 8 9];
B = matrix_utils.normalize(A, 'method', 'minmax');
total_tests = total_tests + 1;
if min(B(:)) >= 0 && max(B(:)) <= 1
    fprintf('✓ normalize (minmax): 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ normalize (minmax): 失败\n');
end

%% 14. 测试矩阵范数和秩
fprintf('\n--- 测试矩阵范数和秩 ---\n');

A = [1 2 3; 4 5 6; 7 8 9];
r = matrix_utils.matrix_rank(A);
total_tests = total_tests + 1;
if r == 2
    fprintf('✓ matrix_rank: 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ matrix_rank: 失败\n');
end

A = [1 2; 3 4];
n = matrix_utils.matrix_norm(A, 'type', 'fro');
total_tests = total_tests + 1;
if abs(n - sqrt(30)) < 1e-10
    fprintf('✓ matrix_norm (fro): 通过\n');
    passed_tests = passed_tests + 1;
else
    fprintf('✗ matrix_norm (fro): 失败\n');
end

%% 测试结果汇总
fprintf('\n========================================\n');
fprintf('  测试结果: %d/%d 通过\n', passed_tests, total_tests);
fprintf('========================================\n\n');

if passed_tests == total_tests
    fprintf('🎉 所有测试通过！\n');
else
    fprintf('⚠️ 有 %d 个测试失败\n', total_tests - passed_tests);
end