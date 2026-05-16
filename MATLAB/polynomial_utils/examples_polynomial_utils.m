%% POLYNOMIAL_UTILS 使用示例
% 演示 polynomial_utils 工具库的主要功能
% 运行方式: 在 MATLAB 中执行 examples_polynomial_utils

function examples_polynomial_utils()
    fprintf('\n========================================\n');
    fprintf('  POLYNOMIAL_UTILS 使用示例\n');
    fprintf('========================================\n\n');
    
    %% ==================== 示例 1: 数据拟合 ====================
    fprintf('【示例 1】数据拟合 - 最小二乘法\n');
    fprintf('----------------------------------------\n');
    
    % 生成带有噪声的数据
    x_data = linspace(0, 5, 20)';
    y_true = 0.5 * x_data.^2 - 2 * x_data + 3;
    y_data = y_true + 0.5 * randn(20, 1);
    
    % 二次多项式拟合
    coeffs = polynomial_utils.polyfit_least_squares(x_data, y_data, 2);
    y_fit = polynomial_utils.polyval_safe(x_data, coeffs);
    
    % 计算拟合质量
    rmse = sqrt(mean((y_data - y_fit).^2));
    
    fprintf('拟合多项式: ');
    str = polynomial_utils.poly_to_string(coeffs);
    fprintf('%s\n', str);
    fprintf('RMSE: %.4f\n', rmse);
    fprintf('\n');
    
    %% ==================== 示例 2: 鲁棒拟合 ====================
    fprintf('【示例 2】鲁棒拟合 - 处理离群点\n');
    fprintf('----------------------------------------\n');
    
    % 添加离群点
    y_with_outliers = y_data;
    y_with_outliers(5) = y_with_outliers(5) + 10;
    y_with_outliers(15) = y_with_outliers(15) - 8;
    
    % 鲁棒拟合
    [coeffs_robust, info] = polynomial_utils.polyfit_robust(x_data, y_with_outliers, 2);
    y_robust = polynomial_utils.polyval_safe(x_data, coeffs_robust);
    
    fprintf('鲁棒拟合多项式: ');
    str = polynomial_utils.poly_to_string(coeffs_robust);
    fprintf('%s\n', str);
    fprintf('迭代次数: %d\n', info.iterations);
    fprintf('R²: %.4f\n', info.r_squared);
    fprintf('\n');
    
    %% ==================== 示例 3: 插值 ====================
    fprintf('【示例 3】多项式插值\n');
    fprintf('----------------------------------------\n');
    
    % 定义插值节点
    x_interp = [0; 1; 2; 3; 4];
    y_interp = [1; 0; 4; 3; 2];
    
    % 多项式插值
    coeffs_interp = polynomial_utils.polyfit_interpolation(x_interp, y_interp);
    
    % 拉格朗日插值验证
    x_test = linspace(0, 4, 100)';
    y_lagrange = polynomial_utils.lagrange_interpolation(x_interp, y_interp, x_test);
    y_poly = polynomial_utils.polyval_safe(x_test, coeffs_interp);
    
    fprintf('插值节点数: %d\n', length(x_interp));
    fprintf('插值多项式次数: %d\n', polynomial_utils.poly_info(coeffs_interp).degree);
    fprintf('拉格朗日与多项式插值一致性: %s\n', ...
        max(abs(y_lagrange - y_poly)) < 1e-10 ? '通过' : '失败');
    fprintf('\n');
    
    %% ==================== 示例 4: 样条插值 ====================
    fprintf('【示例 4】三次样条插值\n');
    fprintf('----------------------------------------\n');
    
    % 自然样条
    pp_natural = polynomial_utils.spline_interpolation(x_interp, y_interp, ...
        'EndConditions', 'natural');
    
    % clamped 样条
    pp_clamped = polynomial_utils.spline_interpolation(x_interp, y_interp, ...
        'EndConditions', 'clamped', 'EndSlopes', [-1, 2]);
    
    fprintf('自然样条段数: %d\n', pp_natural.pieces);
    fprintf('Clamped 样条段数: %d\n', pp_clamped.pieces);
    fprintf('\n');
    
    %% ==================== 示例 5: 求导 ====================
    fprintf('【示例 5】多项式求导\n');
    fprintf('----------------------------------------\n');
    
    % 定义多项式: x^4 - 2x^3 + 3x^2 - 4x + 5
    coeffs = [1, -2, 3, -4, 5];
    fprintf('原多项式: %s\n', polynomial_utils.poly_to_string(coeffs));
    
    % 各阶导数
    deriv1 = polynomial_utils.polyder_n(coeffs, 1);
    fprintf('一阶导数: %s\n', polynomial_utils.poly_to_string(deriv1));
    
    deriv2 = polynomial_utils.polyder_n(coeffs, 2);
    fprintf('二阶导数: %s\n', polynomial_utils.poly_to_string(deriv2));
    
    deriv3 = polynomial_utils.polyder_n(coeffs, 3);
    fprintf('三阶导数: %s\n', polynomial_utils.poly_to_string(deriv3));
    
    % 指定点导数值
    x_point = 2;
    dy = polynomial_utils.poly_derivative_at(x_point, coeffs, 1);
    fprintf('在 x=%d 处的一阶导数值: %.2f\n', x_point, dy);
    fprintf('\n');
    
    %% ==================== 示例 6: 积分 ====================
    fprintf('【示例 6】多项式积分\n');
    fprintf('----------------------------------------\n');
    
    % 定义多项式: 3x^2 + 2x + 1
    coeffs = [3, 2, 1];
    fprintf('原多项式: %s\n', polynomial_utils.poly_to_string(coeffs));
    
    % 不定积分
    integ1 = polynomial_utils.polyint_n(coeffs, 1);
    fprintf('不定积分: %s\n', polynomial_utils.poly_to_string(integ1));
    
    % 定积分
    a = 0; b = 2;
    I = polynomial_utils.polyint_definite(coeffs, a, b);
    fprintf('定积分 I[%g, %g]: %.4f\n', a, b, I);
    
    % 带初值的不定积分
    antideriv = polynomial_utils.poly_antiderivative(coeffs, 1, 2);
    fprintf('满足 F(1)=2 的不定积分: %s\n', polynomial_utils.poly_to_string(antideriv));
    fprintf('验证 F(1): %.4f\n', polynomial_utils.polyval_safe(1, antideriv));
    fprintf('\n');
    
    %% ==================== 示例 7: 求根 ====================
    fprintf('【示例 7】多项式求根\n');
    fprintf('----------------------------------------\n');
    
    % (x-1)(x-2)(x-3) = x^3 - 6x^2 + 11x - 6
    coeffs = [1, -6, 11, -6];
    fprintf('多项式: %s\n', polynomial_utils.poly_to_string(coeffs));
    
    % 求所有根
    all_roots = polynomial_utils.polyroots_safe(coeffs);
    fprintf('所有根: ');
    for i = 1:length(all_roots)
        fprintf('%g', all_roots(i));
        if i < length(all_roots), fprintf(', '); end
    end
    fprintf('\n');
    
    % 求实根
    real_roots = polynomial_utils.polyroots_real(coeffs);
    fprintf('实根: ');
    for i = 1:length(real_roots)
        fprintf('%g', real_roots(i));
        if i < length(real_roots), fprintf(', '); end
    end
    fprintf('\n');
    
    % 区间内求根
    roots_in_range = polynomial_utils.polyroots_bounds(coeffs, [1.5, 2.5]);
    fprintf('[1.5, 2.5] 内的根: ');
    for i = 1:length(roots_in_range)
        fprintf('%g', roots_in_range(i));
        if i < length(roots_in_range), fprintf(', '); end
    end
    fprintf('\n\n');
    
    %% ==================== 示例 8: 多项式运算 ====================
    fprintf('【示例 8】多项式运算\n');
    fprintf('----------------------------------------\n');
    
    % 定义两个多项式
    p1 = [1, -3, 2];  % (x-1)(x-2)
    p2 = [1, -4, 4];  % (x-2)^2
    
    fprintf('p1: %s\n', polynomial_utils.poly_to_string(p1));
    fprintf('p2: %s\n', polynomial_utils.poly_to_string(p2));
    
    % 加法
    sum_p = polynomial_utils.polyadd(p1, p2);
    fprintf('p1 + p2: %s\n', polynomial_utils.poly_to_string(sum_p));
    
    % 减法
    diff_p = polynomial_utils.polysub(p1, p2);
    fprintf('p1 - p2: %s\n', polynomial_utils.poly_to_string(diff_p));
    
    % 乘法
    prod_p = polynomial_utils.polymul_safe(p1, p2);
    fprintf('p1 * p2: %s\n', polynomial_utils.poly_to_string(prod_p));
    
    % 除法
    [quotient, remainder] = polynomial_utils.polydiv_safe(prod_p, p2);
    fprintf('p1*p2 / p2: %s (余式: %s)\n', ...
        polynomial_utils.poly_to_string(quotient), ...
        polynomial_utils.poly_to_string([remainder]));
    fprintf('\n');
    
    %% ==================== 示例 9: 从根构造多项式 ====================
    fprintf('【示例 9】从根构造多项式\n');
    fprintf('----------------------------------------\n');
    
    roots_arr = [1; -1; 2; -2];
    coeffs_from_roots = polynomial_utils.polyfrom_roots(roots_arr);
    
    fprintf('根: ');
    for i = 1:length(roots_arr)
        fprintf('%g', roots_arr(i));
        if i < length(roots_arr), fprintf(', '); end
    end
    fprintf('\n');
    fprintf('构造的多项式: %s\n', polynomial_utils.poly_to_string(coeffs_from_roots));
    
    % 验证
    fprintf('验证各根处的值:\n');
    for i = 1:length(roots_arr)
        y = polynomial_utils.polyval_safe(roots_arr(i), coeffs_from_roots);
        fprintf('  P(%g) = %.10f\n', roots_arr(i), y);
    end
    fprintf('\n');
    
    %% ==================== 示例 10: 多项式平移 ====================
    fprintf('【示例 10】多项式平移\n');
    fprintf('----------------------------------------\n');
    
    coeffs = [1, 0, 0];  % x^2
    fprintf('原多项式: %s\n', polynomial_utils.poly_to_string(coeffs));
    
    % 平移 P(x) -> P(x-1)
    shifted = polynomial_utils.poly_shift(coeffs, 1);
    fprintf('P(x-1): %s\n', polynomial_utils.poly_to_string(shifted));
    
    % 平移 P(x) -> P(x+2)
    shifted2 = polynomial_utils.poly_shift(coeffs, -2);
    fprintf('P(x+2): %s\n', polynomial_utils.poly_to_string(shifted2));
    fprintf('\n');
    
    %% ==================== 示例 11: 多项式统计 ====================
    fprintf('【示例 11】多项式统计信息\n');
    fprintf('----------------------------------------\n');
    
    coeffs = [1, -3, 2];  % x^2 - 3x + 2 = (x-1)(x-2)
    stats = polynomial_utils.poly_stats(coeffs, [-2, 4]);
    
    fprintf('多项式: %s\n', polynomial_utils.poly_to_string(coeffs));
    fprintf('区间: [-2, 4]\n');
    fprintf('最小值: %.4f (在 x=%.2f)\n', stats.min, stats.x_min);
    fprintf('最大值: %.4f (在 x=%.2f)\n', stats.max, stats.x_max);
    fprintf('平均值: %.4f\n', stats.mean);
    fprintf('定积分: %.4f\n', stats.integral);
    fprintf('根: ');
    for i = 1:length(stats.roots)
        fprintf('%g', stats.roots(i));
        if i < length(stats.roots), fprintf(', '); end
    end
    fprintf('\n');
    fprintf('极值点: ');
    for i = 1:length(stats.critical_points)
        fprintf('%g', stats.critical_points(i));
        if i < length(stats.critical_points), fprintf(', '); end
    end
    fprintf('\n\n');
    
    %% ==================== 示例 12: 实际应用 - 曲线拟合 ====================
    fprintf('【示例 12】实际应用 - 温度数据拟合\n');
    fprintf('----------------------------------------\n');
    
    % 模拟温度数据（一天的温度变化）
    hours = [0; 4; 8; 12; 16; 20; 24];
    temps = [15; 14; 18; 28; 26; 20; 15];
    
    % 三次多项式拟合
    coeffs = polynomial_utils.polyfit_least_squares(hours, temps, 3);
    
    % 预测任意时间的温度
    hours_predict = linspace(0, 24, 100)';
    temps_predict = polynomial_utils.polyval_safe(hours_predict, coeffs);
    
    fprintf('拟合多项式: %s\n', polynomial_utils.poly_to_string(coeffs));
    fprintf('最高温度预测: %.1f°C (约 %.1f 点)\n', ...
        max(temps_predict), hours_predict(temps_predict == max(temps_predict)));
    
    % 计算平均温度
    avg_temp = polynomial_utils.polyint_definite(coeffs, 0, 24) / 24;
    fprintf('日均温度: %.1f°C\n', avg_temp);
    
    % 找温度变化最快的时间点
    deriv = polynomial_utils.polyder_n(coeffs, 1);
    critical = polynomial_utils.polyroots_real(deriv);
    fprintf('温度变化极值时间点: ');
    for i = 1:length(critical)
        if critical(i) >= 0 && critical(i) <= 24
            fprintf('%.1f 点 ', critical(i));
        end
    end
    fprintf('\n\n');
    
    %% ==================== 示例 13: 实际应用 - 信号处理 ====================
    fprintf('【示例 13】实际应用 - 信号平滑\n');
    fprintf('----------------------------------------\n');
    
    % 模拟带噪声的信号
    t = linspace(0, 2*pi, 50)';
    signal_true = sin(t) + 0.3*cos(2*t);
    signal_noise = signal_true + 0.2*randn(50, 1);
    
    % 多项式拟合平滑
    coeffs = polynomial_utils.polyfit_least_squares(t, signal_noise, 6);
    signal_smooth = polynomial_utils.polyval_safe(t, coeffs);
    
    % 计算平滑效果
    noise_before = std(signal_noise - signal_true);
    noise_after = std(signal_smooth - signal_true);
    
    fprintf('拟合次数: 6\n');
    fprintf('原始噪声标准差: %.4f\n', noise_before);
    fprintf('平滑后误差标准差: %.4f\n', noise_after);
    fprintf('噪声降低: %.1f%%\n', 100*(noise_before - noise_after)/noise_before);
    fprintf('\n');
    
    %% ==================== 示例 14: 加权拟合 ====================
    fprintf('【示例 14】加权拟合 - 不等精度数据\n');
    fprintf('----------------------------------------\n');
    
    % 不同精度的测量数据
    x = [1; 2; 3; 4; 5];
    y = [2.1; 3.8; 6.2; 7.9; 10.1];
    weights = [10; 5; 8; 3; 10];  % 测量精度权重
    
    % 加权拟合
    coeffs_weighted = polynomial_utils.polyfit_weighted(x, y, weights, 1);
    
    % 普通拟合对比
    coeffs_normal = polynomial_utils.polyfit_least_squares(x, y, 1);
    
    fprintf('加权拟合: y = %.4fx + %.4f\n', coeffs_weighted(1), coeffs_weighted(2));
    fprintf('普通拟合: y = %.4fx + %.4f\n', coeffs_normal(1), coeffs_normal(2));
    fprintf('\n');
    
    %% ==================== 示例 15: 复数多项式 ====================
    fprintf('【示例 15】处理复数系数\n');
    fprintf('----------------------------------------\n');
    
    % x^2 + 1 (有复数根)
    coeffs = [1, 0, 1];
    fprintf('多项式: %s\n', polynomial_utils.poly_to_string(coeffs));
    
    roots_arr = polynomial_utils.polyroots_safe(coeffs);
    fprintf('根: ');
    for i = 1:length(roots_arr)
        fprintf('%g + %gi', real(roots_arr(i)), imag(roots_arr(i)));
        if i < length(roots_arr), fprintf(', '); end
    end
    fprintf('\n');
    
    % 验证根
    fprintf('验证:\n');
    for i = 1:length(roots_arr)
        y = polynomial_utils.polyval_safe(roots_arr(i), coeffs);
        fprintf('  P(%g + %gi) = %.10f + %.10fi\n', ...
            real(roots_arr(i)), imag(roots_arr(i)), real(y), imag(y));
    end
    fprintf('\n');
    
    fprintf('========================================\n');
    fprintf('  示例演示完成\n');
    fprintf('========================================\n\n');
end