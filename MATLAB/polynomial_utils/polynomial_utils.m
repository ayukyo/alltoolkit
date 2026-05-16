classdef polynomial_utils
    % POLYNOMIAL_UTILS 多项式工具库
    % 提供多项式拟合、插值、求值、求导、积分、求根和运算等功能
    %
    % 主要功能:
    %   拟合: polyfit_least_squares, polyfit_weighted, polyfit_robust
    %   插值: polyfit_interpolation, spline_interpolation, lagrange_interpolation
    %   求值: polyval_safe, polyval_multi, polyval_batch
    %   求导: polyder_n, polyder_all, poly_derivative_at
    %   积分: polyint_n, polyint_definite, poly_antiderivative
    %   求根: polyroots_safe, polyroots_real, polyroots_bounds
    %   运算: polyadd, polysub, polymul_safe, polydiv_safe
    %   工具: polyfrom_roots, polyfrom_points, poly_normalize, poly_shift
    
    properties (Constant)
        VERSION = '1.0.0'
        MAX_DEGREE = 50  % 最大支持多项式次数
        EPSILON = 1e-10  % 数值精度阈值
    end
    
    methods (Static)
        %% ==================== 拟合函数 ====================
        
        function coeffs = polyfit_least_squares(x, y, degree, varargin)
            % POLYFIT_LEAST_SQUARES 最小二乘多项式拟合
            %   coeffs = polyfit_least_squares(x, y, degree)
            %   coeffs = polyfit_least_squares(x, y, degree, 'Options', opts)
            %
            % 输入:
            %   x, y - 数据点坐标
            %   degree - 多项式次数
            %   Options - 可选参数结构体
            %     .CenterScale - 是否中心化和缩放 (默认: true)
            %     .Regularization - 正则化参数 (默认: 0)
            %
            % 输出:
            %   coeffs - 多项式系数 [最高次项, ..., 常数项]
            
            % 参数验证
            arguments
                x (:,1) double
                y (:,1) double
                degree (1,1) double {mustBeNonnegative, mustBeInteger}
                varargin
            end
            
            opts = polynomial_utils.parse_options(varargin, ...
                'CenterScale', true, ...
                'Regularization', 0);
            
            % 检查数据
            if length(x) ~= length(y)
                error('polynomial_utils:DimensionMismatch', ...
                    'x and y must have the same length');
            end
            
            n = length(x);
            if n < degree + 1
                error('polynomial_utils:InsufficientData', ...
                    'Need at least %d points for degree %d polynomial', ...
                    degree + 1, degree);
            end
            
            % 中心化和缩放以提高数值稳定性
            if opts.CenterScale && n > 1
                x_mean = mean(x);
                x_std = std(x);
                if x_std < polynomial_utils.EPSILON
                    x_std = 1;
                end
                x_scaled = (x - x_mean) / x_std;
                
                % 构建 Vandermonde 矩阵
                V = zeros(n, degree + 1);
                for j = 0:degree
                    V(:, degree + 1 - j) = x_scaled .^ j;
                end
                
                % 正则化
                if opts.Regularization > 0
                    lambda = opts.Regularization * eye(degree + 1);
                    coeffs_scaled = (V' * V + lambda) \ (V' * y);
                else
                    coeffs_scaled = V \ y;
                end
                
                % 转换回原始尺度
                coeffs = polynomial_utils.unscale_coeffs(coeffs_scaled, x_mean, x_std);
            else
                % 直接拟合
                V = zeros(n, degree + 1);
                for j = 0:degree
                    V(:, degree + 1 - j) = x .^ j;
                end
                
                if opts.Regularization > 0
                    lambda = opts.Regularization * eye(degree + 1);
                    coeffs = (V' * V + lambda) \ (V' * y);
                else
                    coeffs = V \ y;
                end
            end
        end
        
        function coeffs = polyfit_weighted(x, y, weights, degree)
            % POLYFIT_WEIGHTED 加权最小二乘多项式拟合
            %
            % 输入:
            %   x, y - 数据点坐标
            %   weights - 各数据点的权重
            %   degree - 多项式次数
            
            arguments
                x (:,1) double
                y (:,1) double
                weights (:,1) double
                degree (1,1) double {mustBeNonnegative, mustBeInteger}
            end
            
            n = length(x);
            if n ~= length(y) || n ~= length(weights)
                error('polynomial_utils:DimensionMismatch', ...
                    'x, y, and weights must have the same length');
            end
            
            % 构建加权 Vandermonde 矩阵
            W = diag(sqrt(weights));
            V = zeros(n, degree + 1);
            for j = 0:degree
                V(:, degree + 1 - j) = x .^ j;
            end
            
            WV = W * V;
            Wy = W * y;
            
            coeffs = (WV' * WV) \ (WV' * Wy);
        end
        
        function [coeffs, info] = polyfit_robust(x, y, degree, varargin)
            % POLYFIT_ROBUST 鲁棒多项式拟合（迭代加权最小二乘）
            %
            % 输入:
            %   x, y - 数据点坐标
            %   degree - 多项式次数
            %   MaxIterations - 最大迭代次数 (默认: 10)
            %   Tolerance - 收敛容差 (默认: 1e-6)
            %
            % 输出:
            %   coeffs - 多项式系数
            %   info - 拟合信息结构体
            
            opts = polynomial_utils.parse_options(varargin, ...
                'MaxIterations', 10, ...
                'Tolerance', 1e-6);
            
            n = length(x);
            
            % 初始拟合
            coeffs = polynomial_utils.polyfit_least_squares(x, y, degree);
            
            for iter = 1:opts.MaxIterations
                % 计算残差
                y_pred = polynomial_utils.polyval_safe(x, coeffs);
                residuals = abs(y - y_pred);
                
                % Huber 权重函数
                scale = 1.345 * median(residuals);
                if scale < polynomial_utils.EPSILON
                    scale = 1;
                end
                
                weights = zeros(n, 1);
                for i = 1:n
                    if residuals(i) <= scale
                        weights(i) = 1;
                    else
                        weights(i) = scale / residuals(i);
                    end
                end
                
                % 加权拟合
                coeffs_new = polynomial_utils.polyfit_weighted(x, y, weights, degree);
                
                % 检查收敛
                if max(abs(coeffs_new - coeffs)) < opts.Tolerance
                    coeffs = coeffs_new;
                    break;
                end
                coeffs = coeffs_new;
            end
            
            % 返回拟合信息
            y_pred = polynomial_utils.polyval_safe(x, coeffs);
            info.iterations = iter;
            info.rmse = sqrt(mean((y - y_pred).^2));
            info.mae = mean(abs(y - y_pred));
            info.r_squared = 1 - sum((y - y_pred).^2) / sum((y - mean(y)).^2);
        end
        
        %% ==================== 插值函数 ====================
        
        function coeffs = polyfit_interpolation(x, y)
            % POLYFIT_INTERPOLATION 多项式插值（拉格朗日插值）
            %
            % 输入:
            %   x, y - 插值节点（n个点确定 n-1 次多项式）
            %
            % 输出:
            %   coeffs - 插值多项式系数
            
            arguments
                x (:,1) double
                y (:,1) double
            end
            
            n = length(x);
            if n ~= length(y)
                error('polynomial_utils:DimensionMismatch', ...
                    'x and y must have the same length');
            end
            
            % 使用牛顿形式计算插值多项式
            coeffs = y(1);
            
            for k = 1:n-1
                % 计算差商
                dd = y(k+1);
                for j = 1:k
                    dd = (dd - polynomial_utils.polyval_safe(x(j), coeffs)) / ...
                         (x(k+1) - x(j));
                end
                
                % 更新系数（牛顿形式转换）
                new_coeff = zeros(1, k + 1);
                new_coeff(1) = dd;
                for j = 1:k
                    new_coeff(j + 1) = -dd * x(j);
                end
                for j = 1:k
                    new_coeff(j + 1) = new_coeff(j + 1) + coeffs(j);
                end
                coeffs = new_coeff;
            end
            
            % 转换为标准形式
            coeffs = polynomial_utils.poly_from_newton(x, y);
        end
        
        function pp = spline_interpolation(x, y, varargin)
            % SPLINE_INTERPOLATION 三次样条插值
            %
            % 输入:
            %   x, y - 插值节点
            %   EndConditions - 端点条件: 'natural', 'clamped', 'not-a-knot'
            %   EndSlopes - 端点斜率 [dy0, dyn]（仅 clamped 条件）
            %
            % 输出:
            %   pp - 分段多项式结构体
            
            opts = polynomial_utils.parse_options(varargin, ...
                'EndConditions', 'natural', ...
                'EndSlopes', []);
            
            n = length(x);
            if n ~= length(y)
                error('polynomial_utils:DimensionMismatch', ...
                    'x and y must have the same length');
            end
            
            % 检查 x 是否单调递增
            if ~all(diff(x) > 0)
                error('polynomial_utils:InvalidX', ...
                    'x must be strictly increasing');
            end
            
            h = diff(x);
            
            % 构建三对角系统
            A = zeros(n, n);
            b = zeros(n, 1);
            
            % 内部节点
            for i = 2:n-1
                A(i, i-1) = h(i-1);
                A(i, i) = 2 * (h(i-1) + h(i));
                A(i, i+1) = h(i);
                b(i) = 3 * ((y(i+1) - y(i)) / h(i) - ...
                            (y(i) - y(i-1)) / h(i-1));
            end
            
            % 边界条件
            switch lower(opts.EndConditions)
                case 'natural'
                    A(1, 1) = 1;
                    A(n, n) = 1;
                case 'clamped'
                    if isempty(opts.EndSlopes) || length(opts.EndSlopes) ~= 2
                        error('polynomial_utils:MissingEndSlopes', ...
                            'Clamped spline requires EndSlopes [dy0, dyn]');
                    end
                    A(1, 1) = 2 * h(1);
                    A(1, 2) = h(1);
                    b(1) = 3 * ((y(2) - y(1)) / h(1) - opts.EndSlopes(1));
                    
                    A(n, n-1) = h(n-1);
                    A(n, n) = 2 * h(n-1);
                    b(n) = 3 * (opts.EndSlopes(2) - (y(n) - y(n-1)) / h(n-1));
                case 'not-a-knot'
                    A(1, 1) = h(2);
                    A(1, 2) = -(h(1) + h(2));
                    A(1, 3) = h(1);
                    A(n, n-2) = h(n-1);
                    A(n, n-1) = -(h(n-2) + h(n-1));
                    A(n, n) = h(n-2);
                otherwise
                    error('polynomial_utils:UnknownEndCondition', ...
                        'Unknown end condition: %s', opts.EndConditions);
            end
            
            % 求解
            M = A \ b;
            
            % 构建分段多项式
            pp.breaks = x(:)';
            pp.coefs = zeros(n-1, 4);
            pp.pieces = n - 1;
            pp.order = 4;
            pp.dim = 1;
            
            for i = 1:n-1
                a = y(i);
                b_coef = (y(i+1) - y(i)) / h(i) - h(i) * (2*M(i) + M(i+1)) / 3;
                c = M(i) / 2;
                d = (M(i+1) - M(i)) / (3 * h(i));
                
                pp.coefs(i, :) = [d, c, b_coef, a];
            end
        end
        
        function y = lagrange_interpolation(x_data, y_data, x_eval)
            % LAGRANGE_INTERPOLATION 拉格朗日插值
            %
            % 输入:
            %   x_data, y_data - 插值节点
            %   x_eval - 求值点
            %
            % 输出:
            %   y - 插值结果
            
            n = length(x_data);
            y = zeros(size(x_eval));
            
            for i = 1:n
                % 计算 Lagrange 基函数
                Li = ones(size(x_eval));
                for j = 1:n
                    if j ~= i
                        Li = Li .* (x_eval - x_data(j)) / (x_data(i) - x_data(j));
                    end
                end
                y = y + y_data(i) * Li;
            end
        end
        
        %% ==================== 求值函数 ====================
        
        function y = polyval_safe(x, coeffs, varargin)
            % POLYVAL_SAFE 安全多项式求值（Horner 方法）
            %
            % 输入:
            %   x - 求值点（标量或向量）
            %   coeffs - 多项式系数 [最高次项, ..., 常数项]
            %
            % 输出:
            %   y - 多项式值
            
            arguments
                x double
                coeffs (1,:) double
                varargin
            end
            
            % 处理空系数
            if isempty(coeffs)
                y = zeros(size(x));
                return;
            end
            
            % 去除前导零
            coeffs = coeffs(:)';
            while length(coeffs) > 1 && abs(coeffs(1)) < polynomial_utils.EPSILON
                coeffs(1) = [];
            end
            
            % Horner 方法求值
            y = coeffs(1) * ones(size(x));
            for i = 2:length(coeffs)
                y = y .* x + coeffs(i);
            end
        end
        
        function y = polyval_multi(x, coeffs_matrix)
            % POLYVAL_MULTI 批量求值多个多项式
            %
            % 输入:
            %   x - 求值点
            %   coeffs_matrix - 多项式系数矩阵（每行一个多项式）
            %
            % 输出:
            %   y - 求值结果矩阵
            
            n_polys = size(coeffs_matrix, 1);
            y = zeros(length(x), n_polys);
            
            for i = 1:n_polys
                y(:, i) = polynomial_utils.polyval_safe(x, coeffs_matrix(i, :));
            end
        end
        
        function [y, dy] = polyval_batch(x, coeffs)
            % POLYVAL_BATCH 批量求值多项式及其导数
            %
            % 输入:
            %   x - 求值点
            %   coeffs - 多项式系数
            %
            % 输出:
            %   y - 多项式值
            %   dy - 导数值
            
            n = length(coeffs);
            y = coeffs(1) * ones(size(x));
            dy = zeros(size(x));
            
            for i = 2:n
                dy = dy .* x + y;
                y = y .* x + coeffs(i);
            end
        end
        
        %% ==================== 求导函数 ====================
        
        function deriv = polyder_n(coeffs, n)
            % POLYDER_N 计算多项式的 n 阶导数
            %
            % 输入:
            %   coeffs - 多项式系数
            %   n - 导数阶数（默认: 1）
            
            arguments
                coeffs (1,:) double
                n (1,1) double {mustBeNonnegative, mustBeInteger} = 1
            end
            
            deriv = coeffs(:)';
            
            for k = 1:n
                if length(deriv) <= 1
                    deriv = 0;
                    return;
                end
                deriv = deriv(1:end-1) .* (length(deriv)-1:-1:1);
            end
        end
        
        function derivs = polyder_all(coeffs)
            % POLYDER_ALL 计算多项式的所有阶导数
            %
            % 输入:
            %   coeffs - 多项式系数
            %
            % 输出:
            %   derivs - cell 数组，包含原多项式及各阶导数
            
            derivs = cell(1, length(coeffs));
            derivs{1} = coeffs;
            
            for i = 2:length(coeffs)
                derivs{i} = polynomial_utils.polyder_n(coeffs, i-1);
            end
        end
        
        function dy = poly_derivative_at(x, coeffs, n)
            % POLY_DERIVATIVE_AT 计算多项式在某点的 n 阶导数值
            %
            % 输入:
            %   x - 求值点
            %   coeffs - 多项式系数
            %   n - 导数阶数
            
            arguments
                x double
                coeffs (1,:) double
                n (1,1) double {mustBeNonnegative, mustBeInteger} = 1
            end
            
            deriv_coeffs = polynomial_utils.polyder_n(coeffs, n);
            dy = polynomial_utils.polyval_safe(x, deriv_coeffs);
        end
        
        %% ==================== 积分函数 ====================
        
        function integ = polyint_n(coeffs, n, C)
            % POLYINT_N 计算多项式的 n 阶不定积分
            %
            % 输入:
            %   coeffs - 多项式系数
            %   n - 积分阶数（默认: 1）
            %   C - 积分常数（向量，长度为 n）
            
            arguments
                coeffs (1,:) double
                n (1,1) double {mustBeNonnegative, mustBeInteger} = 1
                C (1,:) double {mustBeLength(n)} = zeros(1, n)
            end
            
            integ = coeffs(:)';
            
            for k = 1:n
                d = length(integ) + 1;
                integ = [integ ./ (d-1:-1:1), C(k)];
            end
        end
        
        function I = polyint_definite(coeffs, a, b)
            % POLYINT_DEFINITE 计算多项式在 [a, b] 上的定积分
            %
            % 输入:
            %   coeffs - 多项式系数
            %   a, b - 积分区间
            
            arguments
                coeffs (1,:) double
                a (1,1) double
                b (1,1) double
            end
            
            integ = polynomial_utils.polyint_n(coeffs, 1, 0);
            I = polynomial_utils.polyval_safe(b, integ) - ...
                polynomial_utils.polyval_safe(a, integ);
        end
        
        function antideriv = poly_antiderivative(coeffs, x0, y0)
            % POLY_ANTIDERIVATIVE 计算满足初值条件的不定积分
            %
            % 输入:
            %   coeffs - 多项式系数
            %   x0, y0 - 初值条件 F(x0) = y0
            
            arguments
                coeffs (1,:) double
                x0 (1,1) double
                y0 (1,1) double
            end
            
            integ = polynomial_utils.polyint_n(coeffs, 1, 0);
            F_x0 = polynomial_utils.polyval_safe(x0, integ);
            C = y0 - F_x0;
            antideriv = [integ(1:end-1), integ(end) + C];
        end
        
        %% ==================== 求根函数 ====================
        
        function roots_arr = polyroots_safe(coeffs, varargin)
            % POLYROOTS_SAFE 安全多项式求根（带预处理）
            %
            % 输入:
            %   coeffs - 多项式系数
            %   MaxIterations - 最大迭代次数
            %   Tolerance - 收敛容差
            %
            % 输出:
            %   roots_arr - 多项式的根
            
            opts = polynomial_utils.parse_options(varargin, ...
                'MaxIterations', 100, ...
                'Tolerance', 1e-10);
            
            % 去除前导零
            coeffs = coeffs(:)';
            while length(coeffs) > 1 && abs(coeffs(1)) < opts.Tolerance
                coeffs(1) = [];
            end
            
            if length(coeffs) == 1
                roots_arr = [];
                return;
            end
            
            % 使用伴侣矩阵法求根
            n = length(coeffs) - 1;
            
            % 归一化
            coeffs = coeffs / coeffs(1);
            
            % 构建伴侣矩阵
            A = diag(ones(n-1, 1), -1);
            A(1, :) = -coeffs(2:end);
            
            roots_arr = eig(A);
        end
        
        function real_roots = polyroots_real(coeffs, varargin)
            % POLYROOTS_REAL 求多项式的实根
            %
            % 输入:
            %   coeffs - 多项式系数
            %   Tolerance - 实部判定阈值
            
            opts = polynomial_utils.parse_options(varargin, ...
                'Tolerance', 1e-10);
            
            all_roots = polynomial_utils.polyroots_safe(coeffs);
            
            % 筛选实根
            real_roots = real(all_roots(abs(imag(all_roots)) < opts.Tolerance));
        end
        
        function roots_in_bounds = polyroots_bounds(coeffs, bounds, varargin)
            % POLYROOTS_BOUNDS 求多项式在指定区间内的根
            %
            % 输入:
            %   coeffs - 多项式系数
            %   bounds - 区间 [a, b]
            %   Tolerance - 容差
            
            opts = polynomial_utils.parse_options(varargin, ...
                'Tolerance', 1e-10);
            
            real_roots = polynomial_utils.polyroots_real(coeffs, ...
                'Tolerance', opts.Tolerance);
            
            % 筛选区间内的根
            roots_in_bounds = real_roots(real_roots >= bounds(1) - opts.Tolerance & ...
                                         real_roots <= bounds(2) + opts.Tolerance);
        end
        
        %% ==================== 运算函数 ====================
        
        function sum_coeffs = polyadd(coeffs1, coeffs2)
            % POLYADD 多项式加法
            
            % 对齐长度
            len1 = length(coeffs1);
            len2 = length(coeffs2);
            max_len = max(len1, len2);
            
            p1 = [zeros(1, max_len - len1), coeffs1];
            p2 = [zeros(1, max_len - len2), coeffs2];
            
            sum_coeffs = p1 + p2;
            
            % 去除前导零
            while length(sum_coeffs) > 1 && abs(sum_coeffs(1)) < polynomial_utils.EPSILON
                sum_coeffs(1) = [];
            end
        end
        
        function diff_coeffs = polysub(coeffs1, coeffs2)
            % POLYSUB 多项式减法
            
            diff_coeffs = polynomial_utils.polyadd(coeffs1, -coeffs2);
        end
        
        function prod_coeffs = polymul_safe(coeffs1, coeffs2)
            % POLYMUL_SAFE 安全多项式乘法
            
            % 处理特殊情况
            if isempty(coeffs1) || isempty(coeffs2)
                prod_coeffs = [];
                return;
            end
            
            if abs(coeffs1(1)) < polynomial_utils.EPSILON
                prod_coeffs = 0;
                return;
            end
            
            if abs(coeffs2(1)) < polynomial_utils.EPSILON
                prod_coeffs = 0;
                return;
            end
            
            % 使用卷积计算
            prod_coeffs = conv(coeffs1, coeffs2);
        end
        
        function [quotient, remainder] = polydiv_safe(coeffs1, coeffs2)
            % POLYDIV_SAFE 安全多项式除法
            %
            % 输出:
            %   quotient - 商
            %   remainder - 余式
            
            arguments
                coeffs1 (1,:) double
                coeffs2 (1,:) double
            end
            
            % 检查除数是否为零
            if all(abs(coeffs2) < polynomial_utils.EPSILON)
                error('polynomial_utils:DivisionByZero', ...
                    'Cannot divide by zero polynomial');
            end
            
            % 去除前导零
            while length(coeffs1) > 1 && abs(coeffs1(1)) < polynomial_utils.EPSILON
                coeffs1(1) = [];
            end
            while length(coeffs2) > 1 && abs(coeffs2(1)) < polynomial_utils.EPSILON
                coeffs2(1) = [];
            end
            
            n1 = length(coeffs1) - 1;
            n2 = length(coeffs2) - 1;
            
            if n1 < n2
                quotient = 0;
                remainder = coeffs1;
                return;
            end
            
            quotient = zeros(1, n1 - n2 + 1);
            remainder = coeffs1;
            
            for i = 0:n1-n2
                if length(remainder) < n2 + 1
                    break;
                end
                
                factor = remainder(1) / coeffs2(1);
                quotient(i + 1) = factor;
                
                for j = 1:length(coeffs2)
                    remainder(j) = remainder(j) - factor * coeffs2(j);
                end
                
                remainder(1) = [];
                
                % 去除前导零
                while length(remainder) > 1 && abs(remainder(1)) < polynomial_utils.EPSILON
                    remainder(1) = [];
                end
            end
        end
        
        function coeffs = polyfrom_roots(roots_arr)
            % POLYFROM_ROOTS 从根构造多项式
            
            arguments
                roots_arr (:,1) double
            end
            
            if isempty(roots_arr)
                coeffs = 1;
                return;
            end
            
            coeffs = 1;
            for r = roots_arr'
                coeffs = polynomial_utils.polymul_safe(coeffs, [1, -r]);
            end
        end
        
        function coeffs = polyfrom_points(x_data, y_data)
            % POLYFROM_POINTS 从点集构造多项式
            
            arguments
                x_data (:,1) double
                y_data (:,1) double
            end
            
            coeffs = polynomial_utils.polyfit_interpolation(x_data, y_data);
        end
        
        function coeffs = poly_normalize(coeffs)
            % POLY_NORMALIZE 多项式归一化（使最高次系数为 1）
            
            coeffs = coeffs(:)';
            
            while length(coeffs) > 1 && abs(coeffs(1)) < polynomial_utils.EPSILON
                coeffs(1) = [];
            end
            
            if ~isempty(coeffs) && abs(coeffs(1)) > polynomial_utils.EPSILON
                coeffs = coeffs / coeffs(1);
            end
            
        end
        
        function shifted = poly_shift(coeffs, a)
            % POLY_SHIFT 多项式平移 P(x) -> P(x-a)
            %
            % 输入:
            %   coeffs - 多项式系数
            %   a - 平移量
            
            n = length(coeffs) - 1;
            shifted = zeros(1, n + 1);
            
            % 使用二项式展开
            for k = 0:n
                for j = 0:k
                    % P(x-a) = sum_k sum_j C(k,j) * (-a)^(k-j) * c_k * x^j
                    shifted(n + 1 - j) = shifted(n + 1 - j) + ...
                        coeffs(n + 1 - k) * nchoosek(k, j) * (-a)^(k - j);
                end
            end
        end
        
        %% ==================== 工具函数 ====================
        
        function info = poly_info(coeffs)
            % POLY_INFO 返回多项式信息
            
            coeffs = coeffs(:)';
            while length(coeffs) > 1 && abs(coeffs(1)) < polynomial_utils.EPSILON
                coeffs(1) = [];
            end
            
            info.degree = length(coeffs) - 1;
            info.coeffs = coeffs;
            info.leading = coeffs(1);
            info.constant = coeffs(end);
            info.num_terms = sum(abs(coeffs) > polynomial_utils.EPSILON);
            
            roots_arr = polynomial_utils.polyroots_safe(coeffs);
            info.roots = roots_arr;
            info.real_roots = polynomial_utils.polyroots_real(coeffs);
        end
        
        function str = poly_to_string(coeffs, varargin)
            % POLY_TO_STRING 多项式转字符串表示
            
            opts = polynomial_utils.parse_options(varargin, ...
                'Variable', 'x', ...
                'Precision', 4);
            
            coeffs = coeffs(:)';
            n = length(coeffs) - 1;
            
            terms = {};
            for i = 1:length(coeffs)
                c = coeffs(i);
                power = n - i + 1;
                
                if abs(c) < polynomial_utils.EPSILON
                    continue;
                end
                
                if power == 0
                    if abs(c - round(c)) < polynomial_utils.EPSILON
                        term = sprintf('%d', round(c));
                    else
                        term = sprintf('%.*f', opts.Precision, c);
                    end
                elseif power == 1
                    if abs(abs(c) - 1) < polynomial_utils.EPSILON
                        if c > 0
                            term = opts.Variable;
                        else
                            term = ['-' opts.Variable];
                        end
                    else
                        if abs(c - round(c)) < polynomial_utils.EPSILON
                            term = sprintf('%d%s', round(c), opts.Variable);
                        else
                            term = sprintf('%.*f%s', opts.Precision, c, opts.Variable);
                        end
                    end
                else
                    if abs(abs(c) - 1) < polynomial_utils.EPSILON
                        if c > 0
                            term = sprintf('%s^%d', opts.Variable, power);
                        else
                            term = sprintf('-%s^%d', opts.Variable, power);
                        end
                    else
                        if abs(c - round(c)) < polynomial_utils.EPSILON
                            term = sprintf('%d%s^%d', round(c), opts.Variable, power);
                        else
                            term = sprintf('%.*f%s^%d', opts.Precision, c, opts.Variable, power);
                        end
                    end
                end
                
                terms{end+1} = term;
            end
            
            if isempty(terms)
                str = '0';
            else
                str = terms{1};
                for i = 2:length(terms)
                    if terms{i}(1) == '-'
                        str = [str ' ' terms{i}];
                    else
                        str = [str ' + ' terms{i}];
                    end
                end
            end
        end
        
        function stats = poly_stats(coeffs, x_range, num_points)
            % POLY_STATS 计算多项式在区间上的统计信息
            
            arguments
                coeffs (1,:) double
                x_range (1,2) double
                num_points (1,1) double = 1000
            end
            
            x = linspace(x_range(1), x_range(2), num_points);
            y = polynomial_utils.polyval_safe(x, coeffs);
            
            stats.min = min(y);
            stats.max = max(y);
            stats.mean = mean(y);
            stats.std = std(y);
            stats.x_min = x(y == stats.min);
            stats.x_max = x(y == stats.max);
            
            % 定积分
            stats.integral = polynomial_utils.polyint_definite(coeffs, x_range(1), x_range(2));
            
            % 求导
            deriv = polynomial_utils.polyder_n(coeffs, 1);
            stats.roots = polynomial_utils.polyroots_real(coeffs);
            stats.critical_points = polynomial_utils.polyroots_real(deriv);
        end
    end
    
    methods (Static, Access = private)
        function opts = parse_options(args, varargin)
            % 解析选项参数
            
            opts = struct();
            for i = 1:2:length(varargin)
                opts.(varargin{i}) = varargin{i+1};
            end
            
            for i = 1:2:length(args)
                if ischar(args{i})
                    opts.(args{i}) = args{i+1};
                end
            end
        end
        
        function coeffs = unscale_coeffs(coeffs_scaled, x_mean, x_std)
            % 将缩放后的系数转换回原始尺度
            
            n = length(coeffs_scaled) - 1;
            coeffs = zeros(1, n + 1);
            
            % 二项式展开
            for i = 0:n
                for j = 0:i
                    c = coeffs_scaled(n + 1 - i) * nchoosek(i, j) * ...
                        (x_mean / x_std)^(i - j) / (x_std^j);
                    coeffs(n + 1 - j) = coeffs(n + 1 - j) + c;
                end
            end
        end
        
        function coeffs = poly_from_newton(x, y)
            % 从牛顿插值形式转换到标准形式
            
            n = length(x) - 1;
            
            % 计算差商表
            dd = zeros(n + 1, n + 1);
            dd(:, 1) = y(:);
            
            for j = 2:n + 1
                for i = 1:n + 2 - j
                    dd(i, j) = (dd(i + 1, j - 1) - dd(i, j - 1)) / ...
                               (x(i + j - 1) - x(i));
                end
            end
            
            % 构建多项式
            coeffs = dd(1, 1);
            product = [1];
            
            for i = 1:n
                product = polynomial_utils.polymul_safe(product, [1, -x(i)]);
                term = dd(1, i + 1) * product;
                coeffs = polynomial_utils.polyadd(coeffs, term);
            end
        end
    end
end