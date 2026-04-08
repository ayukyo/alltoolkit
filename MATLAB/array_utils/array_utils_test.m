function array_utils_test()
    %ARRAY_UTILS_TEST Test suite for array_utils module
    fprintf('Running array_utils test suite...\n');
    fprintf('================================\n\n');
    
    test_count = 0; pass_count = 0; fail_count = 0;
    
    % Test range
    result = mod.range(1, 10, 2);
    expected = [1, 3, 5, 7, 9];
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'range', isequal(result, expected));
    
    % Test linspace
    result = mod.linspace(0, 1, 5);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'linspace', length(result) == 5);
    
    % Test zeros_like
    a = [1, 2, 3; 4, 5, 6];
    result = mod.zeros_like(a);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'zeros_like', isequal(size(result), size(a)));
    
    % Test is_empty
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'is_empty true', mod.is_empty([]));
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'is_empty false', ~mod.is_empty([1, 2, 3]));
    
    % Test flatten
    result = mod.flatten([1, 2; 3, 4]);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'flatten', length(result) == 4);
    
    % Test reverse
    result = mod.reverse([1, 2, 3, 4, 5]);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'reverse', isequal(result, [5, 4, 3, 2, 1]));
    
    % Test unique_elements
    result = mod.unique_elements([1, 2, 2, 3, 3, 3]);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'unique_elements', isequal(result, [1, 2, 3]));
    
    % Test sum_elements
    result = mod.sum_elements([1, 2, 3, 4, 5]);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'sum_elements', result == 15);
    
    % Test mean_elements
    result = mod.mean_elements([1, 2, 3, 4, 5]);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'mean_elements', result == 3);
    
    % Test clip
    result = mod.clip([-1, 0, 5, 10, 15], 0, 10);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'clip', isequal(result, [0, 0, 5, 10, 10]));
    
    % Test all_elements
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'all_elements true', mod.all_elements([1, 1, 1]));
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'all_elements false', ~mod.all_elements([1, 0, 1]));
    
    % Test is_equal
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'is_equal', mod.is_equal([1, 2, 3], [1, 2, 3]));
    
    % Test normalize_minmax
    result = mod.normalize_minmax([1, 2, 3, 4, 5]);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'normalize_minmax', result(1) == 0 && result(end) == 1);
    
    % Summary
    fprintf('\n================================\n');
    fprintf('Test Summary:\n');
    fprintf('  Total:  %d\n', test_count);
    fprintf('  Passed: %d\n', pass_count);
    fprintf('  Failed: %d\n', fail_count);
    fprintf('  Rate:   %.1f%%\n', 100 * pass_count / test_count);
    
    if fail_count == 0
        fprintf('\nAll tests passed!\n');
    else
        fprintf('\nSome tests failed.\n');
    end
end

function [tc, pc, fc] = run_test(tc, pc, fc, name, condition)
    tc = tc + 1;
    if condition
        pc = pc + 1;
        fprintf('  [PASS] %s\n', name);
    else
        fc = fc + 1;
        fprintf('  [FAIL] %s\n', name);
    end
end
