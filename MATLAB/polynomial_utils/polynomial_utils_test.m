%% POLYNOMIAL_UTILS 测试套件
% 完整测试 polynomial_utils 工具库的所有功能
% 运行方式: 在 MATLAB 中执行 polynomial_utils_test

function results = polynomial_utils_test()
    fprintf('\n========================================\n');
    fprintf('  POLYNOMIAL_UTILS 测试套件\n');
    fprintf('  版本: 1.0.0\n');
    fprintf('========================================\n\n');
    
    results = struct();
    results.total = 0;
    results.passed = 0;
    results.failed = 0;
    results.tests = {};
    
    %% ==================== 拟合函数测试 ====================
    fprintf('--- 拟合函数测试 ---\n');
    
    % 测试 1: 基本最小二乘拟合
    fprintf('测试 1: 基本最小二乘拟合... ');
    try
        x = [1; 2; 3; 4; 5];
        y = [2; 4; 6; 8; 10];
        coeffs = polynomial_utils.polyfit_least_squares(x, y, 1);
        expected = [2, 0];  % y = 2x
        assert(max(abs(coeffs - expected)) < 1e-6);
        fprintf('通过\n');
        results = record_result(results, 'polyfit_least_squares_基本', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyfit_least_squares_基本', false);
    end
    
    % 测试 2: 二次多项式拟合
    fprintf('测试 2: 二次多项式拟合... ');
    try
        x = [0; 1; 2; 3; 4];
        y = [0; 1; 4; 9; 16];  % y = x^2
        coeffs = polynomial_utils.polyfit_least_squares(x, y, 2);
        expected = [1, 0, 0];  % x^2
        assert(max(abs(coeffs - expected)) < 1e-6);
        fprintf('通过\n');
        results = record_result(results, 'polyfit_least_squares_二次', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyfit_least_squares_二次', false);
    end
    
    % 测试 3: 加权最小二乘拟合
    fprintf('测试 3: 加权最小二乘拟合... ');
    try
        x = [0; 1; 2; 3];
        y = [0; 1; 2; 10];  % 最后一个点是离群点
        weights = [1; 1; 1; 0.1];  % 降低离群点权重
        coeffs = polynomial_utils.polyfit_weighted(x, y, weights, 1);
        % 结果应该接近 y = x 而不是被离群点拉偏
        assert(abs(coeffs(1) - 1) < 0.5);
        fprintf('通过\n');
        results = record_result(results, 'polyfit_weighted', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyfit_weighted', false);
    end
    
    % 测试 4: 鲁棒拟合
    fprintf('测试 4: 鲁棒拟合... ');
    try
        x = linspace(0, 10, 20)';
        y_true = 2 * x + 1;
        y = y_true;
        y(5) = y(5) + 50;  % 添加离群点
        y(15) = y(15) - 30;
        [coeffs, info] = polynomial_utils.polyfit_robust(x, y, 1);
        assert(abs(coeffs(1) - 2) < 0.3);  % 斜率接近 2
        assert(info.r_squared > 0.9);
        fprintf('通过 (R²=%.4f)\n', info.r_squared);
        results = record_result(results, 'polyfit_robust', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyfit_robust', false);
    end
    
    %% ==================== 插值函数测试 ====================
    fprintf('\n--- 插值函数测试 ---\n');
    
    % 测试 5: 多项式插值
    fprintf('测试 5: 多项式插值... ');
    try
        x = [0; 1; 2; 3];
        y = [0; 1; 8; 27];  % y = x^3
        coeffs = polynomial_utils.polyfit_interpolation(x, y);
        expected = [1, 0, 0, 0];  % x^3
        assert(max(abs(coeffs - expected)) < 1e-6);
        fprintf('通过\n');
        results = record_result(results, 'polyfit_interpolation', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyfit_interpolation', false);
    end
    
    % 测试 6: 三次样条插值 - 自然边界
    fprintf('测试 6: 三次样条插值 (自然边界)... ');
    try
        x = [0; 1; 2; 3; 4];
        y = [0; 1; 4; 9; 16];
        pp = polynomial_utils.spline_interpolation(x, y, 'EndConditions', 'natural');
        assert(pp.pieces == 4);
        assert(pp.order == 4);
        fprintf('通过\n');
        results = record_result(results, 'spline_interpolation_natural', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'spline_interpolation_natural', false);
    end
    
    % 测试 7: 拉格朗日插值
    fprintf('测试 7: 拉格朗日插值... ');
    try
        x_data = [0; 1; 2];
        y_data = [1; 3; 2];
        x_eval = [0.5; 1.5];
        y = polynomial_utils.lagrange_interpolation(x_data, y_data, x_eval);
        % 验证插值点在节点上的值
        y_at_nodes = polynomial_utils.lagrange_interpolation(x_data, y_data, x_data);
        assert(max(abs(y_at_nodes - y_data)) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'lagrange_interpolation', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'lagrange_interpolation', false);
    end
    
    %% ==================== 求值函数测试 ====================
    fprintf('\n--- 求值函数测试 ---\n');
    
    % 测试 8: Horner 方法求值
    fprintf('测试 8: Horner 方法求值... ');
    try
        coeffs = [1, -6, 11, -6];  % (x-1)(x-2)(x-3) = x^3 - 6x^2 + 11x - 6
        x = [1; 2; 3];
        y = polynomial_utils.polyval_safe(x, coeffs);
        assert(max(abs(y)) < 1e-10);  % 在根处应为 0
        fprintf('通过\n');
        results = record_result(results, 'polyval_safe', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyval_safe', false);
    end
    
    % 测试 9: 批量多项式求值
    fprintf('测试 9: 批量多项式求值... ');
    try
        coeffs_matrix = [1, 0, 0; 1, 0, -1; 1, -3, 2];  % x^2, x^2-1, x^2-3x+2
        x = [1; 2; 3];
        y = polynomial_utils.polyval_multi(x, coeffs_matrix);
        assert(size(y, 2) == 3);
        assert(abs(y(1, 1) - 1) < 1e-10);  % x^2 at x=1
        assert(abs(y(1, 2) - 0) < 1e-10);  % x^2-1 at x=1
        fprintf('通过\n');
        results = record_result(results, 'polyval_multi', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyval_multi', false);
    end
    
    % 测试 10: 带导数的批量求值
    fprintf('测试 10: 带导数的批量求值... ');
    try
        coeffs = [3, 2, 1];  % 3x^2 + 2x + 1
        x = [1; 2; 3];
        [y, dy] = polynomial_utils.polyval_batch(x, coeffs);
        expected_y = [6; 17; 34];
        expected_dy = [8; 14; 20];  % 6x + 2
        assert(max(abs(y - expected_y)) < 1e-10);
        assert(max(abs(dy - expected_dy)) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'polyval_batch', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyval_batch', false);
    end
    
    %% ==================== 求导函数测试 ====================
    fprintf('\n--- 求导函数测试 ---\n');
    
    % 测试 11: 一阶导数
    fprintf('测试 11: 一阶导数... ');
    try
        coeffs = [3, 2, 1];  % 3x^2 + 2x + 1
        deriv = polynomial_utils.polyder_n(coeffs, 1);
        expected = [6, 2];  % 6x + 2
        assert(max(abs(deriv - expected)) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'polyder_n_一阶', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyder_n_一阶', false);
    end
    
    % 测试 12: 高阶导数
    fprintf('测试 12: 高阶导数... ');
    try
        coeffs = [1, 0, 0, 0, 0];  % x^4
        deriv2 = polynomial_utils.polyder_n(coeffs, 2);  % 12x^2
        deriv3 = polynomial_utils.polyder_n(coeffs, 3);  % 24x
        deriv4 = polynomial_utils.polyder_n(coeffs, 4);  % 24
        assert(max(abs(deriv2 - [12, 0, 0])) < 1e-10);
        assert(max(abs(deriv3 - [24, 0])) < 1e-10);
        assert(abs(deriv4 - 24) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'polyder_n_高阶', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyder_n_高阶', false);
    end
    
    % 测试 13: 所有阶导数
    fprintf('测试 13: 所有阶导数... ');
    try
        coeffs = [2, 0, 0, 1];  % 2x^3 + 1
        derivs = polynomial_utils.polyder_all(coeffs);
        assert(length(derivs) == 4);
        assert(max(abs(derivs{1} - coeffs)) < 1e-10);
        assert(max(abs(derivs{2} - [6, 0, 0])) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'polyder_all', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyder_all', false);
    end
    
    % 测试 14: 指定点导数值
    fprintf('测试 14: 指定点导数值... ');
    try
        coeffs = [1, 0, 0, 0];  % x^3
        dy = polynomial_utils.poly_derivative_at(2, coeffs, 1);  % 3x^2 at x=2
        assert(abs(dy - 12) < 1e-10);
        dy2 = polynomial_utils.poly_derivative_at(2, coeffs, 2);  % 6x at x=2
        assert(abs(dy2 - 12) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'poly_derivative_at', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'poly_derivative_at', false);
    end
    
    %% ==================== 积分函数测试 ====================
    fprintf('\n--- 积分函数测试 ---\n');
    
    % 测试 15: 不定积分
    fprintf('测试 15: 不定积分... ');
    try
        coeffs = [3, 2, 1];  % 3x^2 + 2x + 1
        integ = polynomial_utils.polyint_n(coeffs, 1);  % x^3 + x^2 + x + C
        expected = [1, 1, 1, 0];
        assert(max(abs(integ - expected)) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'polyint_n', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyint_n', false);
    end
    
    % 测试 16: 定积分
    fprintf('测试 16: 定积分... ');
    try
        coeffs = [1, 0, 0];  % x^2
        I = polynomial_utils.polyint_definite(coeffs, 0, 2);  % [x^3/3]_0^2 = 8/3
        expected = 8/3;
        assert(abs(I - expected) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'polyint_definite', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyint_definite', false);
    end
    
    % 测试 17: 带初值的不定积分
    fprintf('测试 17: 带初值的不定积分... ');
    try
        coeffs = [2, 0];  % 2x
        antideriv = polynomial_utils.poly_antiderivative(coeffs, 1, 5);  % F(1) = 5
        % F(x) = x^2 + C, F(1) = 1 + C = 5 => C = 4
        % F(x) = x^2 + 4
        y = polynomial_utils.polyval_safe(1, antideriv);
        assert(abs(y - 5) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'poly_antiderivative', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'poly_antiderivative', false);
    end
    
    %% ==================== 求根函数测试 ====================
    fprintf('\n--- 求根函数测试 ---\n');
    
    % 测试 18: 基本求根
    fprintf('测试 18: 基本求根... ');
    try
        coeffs = [1, -6, 11, -6];  % (x-1)(x-2)(x-3)
        roots_arr = polynomial_utils.polyroots_safe(coeffs);
        roots_sorted = sort(real(roots_arr(abs(imag(roots_arr)) < 1e-10)));
        expected = [1; 2; 3];
        assert(max(abs(roots_sorted - expected)) < 1e-6);
        fprintf('通过\n');
        results = record_result(results, 'polyroots_safe', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyroots_safe', false);
    end
    
    % 测试 19: 实根筛选
    fprintf('测试 19: 实根筛选... ');
    try
        coeffs = [1, 0, 1];  % x^2 + 1 (无实根)
        real_roots = polynomial_utils.polyroots_real(coeffs);
        assert(isempty(real_roots));
        fprintf('通过\n');
        results = record_result(results, 'polyroots_real_无实根', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyroots_real_无实根', false);
    end
    
    % 测试 20: 区间内求根
    fprintf('测试 20: 区间内求根... ');
    try
        coeffs = [1, -6, 11, -6];  % 根在 1, 2, 3
        roots_in = polynomial_utils.polyroots_bounds(coeffs, [1.5, 2.5]);
        assert(length(roots_in) == 1);
        assert(abs(roots_in(1) - 2) < 1e-6);
        fprintf('通过\n');
        results = record_result(results, 'polyroots_bounds', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyroots_bounds', false);
    end
    
    %% ==================== 运算函数测试 ====================
    fprintf('\n--- 运算函数测试 ---\n');
    
    % 测试 21: 多项式加法
    fprintf('测试 21: 多项式加法... ');
    try
        p1 = [1, 2, 3];  % x^2 + 2x + 3
        p2 = [2, 1];     % 2x + 1
        sum_p = polynomial_utils.polyadd(p1, p2);
        expected = [1, 4, 4];  % x^2 + 4x + 4
        assert(max(abs(sum_p - expected)) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'polyadd', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyadd', false);
    end
    
    % 测试 22: 多项式减法
    fprintf('测试 22: 多项式减法... ');
    try
        p1 = [1, 2, 3];
        p2 = [1, 1, 1];
        diff_p = polynomial_utils.polysub(p1, p2);
        expected = [0, 1, 2];  % 去除前导零后为 [1, 2]
        assert(abs(diff_p(1) - 1) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'polysub', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polysub', false);
    end
    
    % 测试 23: 多项式乘法
    fprintf('测试 23: 多项式乘法... ');
    try
        p1 = [1, -1];  % (x - 1)
        p2 = [1, -2];  % (x - 2)
        prod_p = polynomial_utils.polymul_safe(p1, p2);
        expected = [1, -3, 2];  % (x - 1)(x - 2) = x^2 - 3x + 2
        assert(max(abs(prod_p - expected)) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'polymul_safe', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polymul_safe', false);
    end
    
    % 测试 24: 多项式除法
    fprintf('测试 24: 多项式除法... ');
    try
        p1 = [1, -3, 2];  % x^2 - 3x + 2 = (x-1)(x-2)
        p2 = [1, -1];     % x - 1
        [quotient, remainder] = polynomial_utils.polydiv_safe(p1, p2);
        expected_q = [1, -2];  % x - 2
        assert(max(abs(quotient - expected_q)) < 1e-10);
        assert(abs(remainder) < 1e-10 || isempty(remainder));
        fprintf('通过\n');
        results = record_result(results, 'polydiv_safe', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polydiv_safe', false);
    end
    
    % 测试 25: 带余除法
    fprintf('测试 25: 带余除法... ');
    try
        p1 = [1, 0, 0, -1];  % x^3 - 1
        p2 = [1, -1];        % x - 1
        [quotient, remainder] = polynomial_utils.polydiv_safe(p1, p2);
        expected_q = [1, 1, 1];  % x^2 + x + 1
        assert(max(abs(quotient - expected_q)) < 1e-10);
        assert(abs(remainder) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'polydiv_safe_余式', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polydiv_safe_余式', false);
    end
    
    %% ==================== 工具函数测试 ====================
    fprintf('\n--- 工具函数测试 ---\n');
    
    % 测试 26: 从根构造多项式
    fprintf('测试 26: 从根构造多项式... ');
    try
        roots_arr = [1; 2; 3];
        coeffs = polynomial_utils.polyfrom_roots(roots_arr);
        expected = [1, -6, 11, -6];  % (x-1)(x-2)(x-3)
        assert(max(abs(coeffs - expected)) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'polyfrom_roots', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyfrom_roots', false);
    end
    
    % 测试 27: 从点构造多项式
    fprintf('测试 27: 从点构造多项式... ');
    try
        x_data = [0; 1; 2];
        y_data = [1; 2; 5];
        coeffs = polynomial_utils.polyfrom_points(x_data, y_data);
        y_test = polynomial_utils.polyval_safe(x_data, coeffs);
        assert(max(abs(y_test - y_data)) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'polyfrom_points', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyfrom_points', false);
    end
    
    % 测试 28: 多项式归一化
    fprintf('测试 28: 多项式归一化... ');
    try
        coeffs = [2, 4, 6];  % 2(x^2 + 2x + 3)
        normalized = polynomial_utils.poly_normalize(coeffs);
        expected = [1, 2, 3];
        assert(max(abs(normalized - expected)) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'poly_normalize', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'poly_normalize', false);
    end
    
    % 测试 29: 多项式平移
    fprintf('测试 29: 多项式平移... ');
    try
        coeffs = [1, 0, 0];  % x^2
        shifted = polynomial_utils.poly_shift(coeffs, 1);  % (x-1)^2
        expected = [1, -2, 1];
        assert(max(abs(shifted - expected)) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'poly_shift', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'poly_shift', false);
    end
    
    % 测试 30: 多项式信息
    fprintf('测试 30: 多项式信息... ');
    try
        coeffs = [1, -6, 11, -6];
        info = polynomial_utils.poly_info(coeffs);
        assert(info.degree == 3);
        assert(info.leading == 1);
        assert(info.constant == -6);
        fprintf('通过\n');
        results = record_result(results, 'poly_info', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'poly_info', false);
    end
    
    % 测试 31: 多项式转字符串
    fprintf('测试 31: 多项式转字符串... ');
    try
        coeffs = [1, -3, 2];  % x^2 - 3x + 2
        str = polynomial_utils.poly_to_string(coeffs);
        assert(contains(str, 'x'));
        fprintf('通过 (%s)\n', str);
        results = record_result(results, 'poly_to_string', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'poly_to_string', false);
    end
    
    % 测试 32: 多项式统计
    fprintf('测试 32: 多项式统计... ');
    try
        coeffs = [1, 0, 0];  % x^2
        stats = polynomial_utils.poly_stats(coeffs, [-2, 2]);
        assert(stats.min >= -0.01 && stats.min <= 0.01);  % 最小值接近 0
        assert(abs(stats.max - 4) < 0.01);  % 最大值接近 4
        fprintf('通过 (min=%.2f, max=%.2f)\n', stats.min, stats.max);
        results = record_result(results, 'poly_stats', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'poly_stats', false);
    end
    
    % 测试 33: 正则化拟合
    fprintf('测试 33: 正则化拟合... ');
    try
        x = linspace(0, 1, 10)';
        y = sin(2*pi*x) + 0.01*randn(10, 1);
        coeffs = polynomial_utils.polyfit_least_squares(x, y, 5, 'Regularization', 0.1);
        assert(length(coeffs) == 6);
        fprintf('通过\n');
        results = record_result(results, 'polyfit_regularization', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyfit_regularization', false);
    end
    
    % 测试 34: 高次多项式
    fprintf('测试 34: 高次多项式处理... ');
    try
        coeffs = polynomial_utils.polyfrom_roots((1:20)');
        roots_found = polynomial_utils.polyroots_safe(coeffs);
        roots_sorted = sort(real(roots_found(abs(imag(roots_found)) < 1e-6)));
        expected = (1:20)';
        assert(max(abs(roots_sorted - expected)) < 1e-4);
        fprintf('通过\n');
        results = record_result(results, 'high_degree_poly', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'high_degree_poly', false);
    end
    
    % 测试 35: 二阶不定积分
    fprintf('测试 35: 二阶不定积分... ');
    try
        coeffs = [1, 0, 0, 0];  % x^3
        integ = polynomial_utils.polyint_n(coeffs, 2, [0, 0]);
        expected = [1/20, 0, 0, 0, 0, 0];  % x^5/20
        assert(max(abs(integ - expected)) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'polyint_n_二阶', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'polyint_n_二阶', false);
    end
    
    %% ==================== 边界情况测试 ====================
    fprintf('\n--- 边界情况测试 ---\n');
    
    % 测试 36: 零多项式
    fprintf('测试 36: 零多项式处理... ');
    try
        coeffs = [0, 0, 0];
        y = polynomial_utils.polyval_safe(5, coeffs);
        assert(abs(y) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'zero_poly', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'zero_poly', false);
    end
    
    % 测试 37: 常数多项式
    fprintf('测试 37: 常数多项式处理... ');
    try
        coeffs = [5];
        y = polynomial_utils.polyval_safe([1, 2, 3], coeffs);
        assert(all(abs(y - 5) < 1e-10));
        deriv = polynomial_utils.polyder_n(coeffs, 1);
        assert(abs(deriv) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'constant_poly', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'constant_poly', false);
    end
    
    % 测试 38: 线性多项式
    fprintf('测试 38: 线性多项式根... ');
    try
        coeffs = [2, -6];  % 2x - 6
        roots_arr = polynomial_utils.polyroots_safe(coeffs);
        assert(abs(roots_arr(1) - 3) < 1e-10);
        fprintf('通过\n');
        results = record_result(results, 'linear_poly_root', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'linear_poly_root', false);
    end
    
    % 测试 39: 复数根验证
    fprintf('测试 39: 复数根验证... ');
    try
        coeffs = [1, 0, 0, 0, 0];  % x^4
        roots_arr = polynomial_utils.polyroots_safe(coeffs);
        assert(all(abs(roots_arr) < 1e-10));  % 所有根都是 0
        fprintf('通过\n');
        results = record_result(results, 'complex_roots', true);
    catch e
        fprintf('失败: %s\n', e.message);
        results = record_result(results, 'complex_roots', false);
    end
    
    % 测试 40: 错误处理
    fprintf('测试 40: 错误处理验证... ');
    try
        x = [1; 2];
        y = [1; 2; 3];  % 长度不匹配
        coeffs = polynomial_utils.polyfit_least_squares(x, y, 1);
        fprintf('失败: 应该抛出错误\n');
        results = record_result(results, 'error_handling', false);
    catch e
        if contains(e.identifier, 'polynomial_utils')
            fprintf('通过 (正确捕获错误)\n');
            results = record_result(results, 'error_handling', true);
        else
            fprintf('失败: 错误标识符不正确\n');
            results = record_result(results, 'error_handling', false);
        end
    end
    
    %% ==================== 汇总 ====================
    fprintf('\n========================================\n');
    fprintf('  测试结果汇总\n');
    fprintf('========================================\n');
    fprintf('总计: %d 个测试\n', results.total);
    fprintf('通过: %d 个 (%.1f%%)\n', results.passed, 100*results.passed/results.total);
    fprintf('失败: %d 个 (%.1f%%)\n', results.failed, 100*results.failed/results.total);
    fprintf('========================================\n\n');
    
    if results.failed > 0
        fprintf('失败的测试:\n');
        for i = 1:length(results.tests)
            if ~results.tests{i}.passed
                fprintf('  - %s\n', results.tests{i}.name);
            end
        end
        fprintf('\n');
    end
end

function results = record_result(results, name, passed)
    results.total = results.total + 1;
    if passed
        results.passed = results.passed + 1;
    else
        results.failed = results.failed + 1;
    end
    results.tests{end+1} = struct('name', name, 'passed', passed);
end