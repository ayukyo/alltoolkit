function success = http_utils_test()
    %HTTP_UTILS_TEST Test suite for HTTP utilities
    fprintf('Running HTTP Utils Test Suite...\n');
    fprintf('================================\n\n');
    total_tests = 0; passed_tests = 0;

    %% Test Group: URL Parsing
    fprintf('Test Group: URL Parsing\n'); fprintf('-----------------------\n');
    total_tests = total_tests + 1;
    try
        parsed = http_utils.parse_url('https://api.example.com:8080/v1/users?page=1#section');
        assert(strcmp(parsed.scheme, 'https'));
        assert(strcmp(parsed.host, 'api.example.com'));
        fprintf('  [PASS] Test 1: Parse complete URL\n'); passed_tests = passed_tests + 1;
    catch ME
        fprintf('  [FAIL] Test 1: %s\n', ME.message);
    end

    total_tests = total_tests + 1;
    try
        parsed = http_utils.parse_url('https://example.com');
        assert(strcmp(parsed.scheme, 'https'));
        fprintf('  [PASS] Test 2: Parse simple URL\n'); passed_tests = passed_tests + 1;
    catch ME
        fprintf('  [FAIL] Test 2: %s\n', ME.message);
    end

    %% Test Group: URL Building
    fprintf('\nTest Group: URL Building\n'); fprintf('------------------------\n');
total_tests = total_tests + 1;
    try
        params = struct('q', 'hello world', 'page', 1);
        url = http_utils.build_url('https://api.example.com/search', params);
        assert(contains(url, 'q=hello%20world'));
        fprintf('  [PASS] Test 3: Build URL with params\n'); passed_tests = passed_tests + 1;
    catch ME
        fprintf('  [FAIL] Test 3: %s\n', ME.message);
    end

    %% Summary
    fprintf('\n================================\n');
    fprintf('Test Summary: %d/%d passed\n', passed_tests, total_tests);
    fprintf('================================\n');
    success = (passed_tests == total_tests);
end
