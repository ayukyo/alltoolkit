function json_utils_test()
    %JSON_UTILS_TEST Test suite for JSON Utilities
    %   Runs all tests for the JSON parsing and generation utilities.
    %
    %   Usage:
    %       json_utils_test()

    fprintf('Running JSON Utilities Test Suite...\n');
    fprintf('====================================\n\n');

    utils = json_utils.mod();
    passed = 0;
    failed = 0;

    %% Test 1: Parse empty object
    try
        result = utils.parse('{}');
        assert(isstruct(result) && isempty(fieldnames(result)), 'Empty object test failed');
        fprintf('✓ Test 1: Parse empty object\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 1: Parse empty object - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 2: Parse empty array
    try
        result = utils.parse('[]');
        assert(iscell(result) && isempty(result), 'Empty array test failed');
        fprintf('✓ Test 2: Parse empty array\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 2: Parse empty array - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 3: Parse simple object
    try
        result = utils.parse('{"name": "John", "age": 30}');
        assert(strcmp(result.name, 'John') && result.age == 30, 'Simple object test failed');
        fprintf('✓ Test 3: Parse simple object\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 3: Parse simple object - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 4: Parse nested object
    try
        result = utils.parse('{"user": {"name": "Alice", "id": 123}}');
        assert(strcmp(result.user.name, 'Alice') && result.user.id == 123, 'Nested object test failed');
        fprintf('✓ Test 4: Parse nested object\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 4: Parse nested object - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 5: Parse array of numbers
    try
        result = utils.parse('[1, 2, 3, 4, 5]');
        assert(iscell(result) && length(result) == 5 && result{3} == 3, 'Number array test failed');
        fprintf('✓ Test 5: Parse array of numbers\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 5: Parse array of numbers - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 6: Parse array of strings
    try
        result = utils.parse('["apple", "banana", "cherry"]');
        assert(iscell(result) && strcmp(result{2}, 'banana'), 'String array test failed');
        fprintf('✓ Test 6: Parse array of strings\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 6: Parse array of strings - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 7: Parse mixed array
    try
        result = utils.parse('[1, "two", true, null]');
        assert(result{1} == 1 && strcmp(result{2}, 'two') && islogical(result{3}) && isempty(result{4}), ...
               'Mixed array test failed');
        fprintf('✓ Test 7: Parse mixed array\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 7: Parse mixed array - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 8: Parse true/false/null
    try
        result = utils.parse('{"active": true, "deleted": false, "data": null}');
        assert(result.active == true && result.deleted == false && isempty(result.data), ...
               'Boolean/null test failed');
        fprintf('✓ Test 8: Parse true/false/null\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 8: Parse true/false/null - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 9: Parse numbers (integer and float)
    try
        result = utils.parse('{"int": 42, "float": 3.14, "negative": -10, "exp": 1.5e10}');
        assert(result.int == 42 && abs(result.float - 3.14) < 0.001 && result.negative == -10, ...
               'Number parsing test failed');
        fprintf('✓ Test 9: Parse numbers\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 9: Parse numbers - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 10: Parse string with escapes
    try
        result = utils.parse('{"text": "Line 1\\nLine 2\\tTabbed"}');;
        assert(contains(result.text, sprintf('\n')) && contains(result.text, sprintf('\t')), ...
               'String escape test failed');
        fprintf('✓ Test 10: Parse string with escapes\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 10: Parse string with escapes - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 11: Encode simple struct
    try
        data = struct('name', 'Test', 'value', 123);
        json = utils.encode(data);
        assert(contains(json, '"name":"Test"') && contains(json, '"value":123'), ...
               'Encode struct test failed');
        fprintf('✓ Test 11: Encode simple struct\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 11: Encode simple struct - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 12: Encode cell array
    try
        data = {1, 'two', true};
        json = utils.encode(data);
        assert(strcmp(json, '[1,"two",true]'), 'Encode cell array test failed');
        fprintf('✓ Test 12: Encode cell array\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 12: Encode cell array - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 13: Encode pretty print
    try
        data = struct('a', 1, 'b', 2);
        json = utils.encodePretty(data);
        assert(contains(json, sprintf('\n')) && contains(json, '  '), ...
               'Pretty print test failed');
        fprintf('✓ Test 13: Encode pretty print\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 13: Encode pretty print - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 14: Round-trip test
    try
        original = struct('name', 'Test', 'items', {{1, 2, 3}}, 'active', true);
        json = utils.encode(original);
        result = utils.parse(json);
        assert(strcmp(result.name, 'Test') && result.active == true, ...
               'Round-trip test failed');
        fprintf('✓ Test 14: Round-trip encode/decode\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 14: Round-trip encode/decode - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 15: isValid with valid JSON
    try
        assert(utils.isValid('{"valid": true}') == true, 'isValid true test failed');
        fprintf('✓ Test 15: isValid with valid JSON\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 15: isValid with valid JSON - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 16: isValid with invalid JSON
    try
        assert(utils.isValid('invalid json') == false, 'isValid false test failed');
        fprintf('✓ Test 16: isValid with invalid JSON\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 16: isValid with invalid JSON - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 17: parseOrNull with valid JSON
    try
        result = utils.parseOrNull('{"key": "value"}');
        assert(strcmp(result.key, 'value'), 'parseOrNull valid test failed');
        fprintf('✓ Test 17: parseOrNull with valid JSON\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 17: parseOrNull with valid JSON - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 18: parseOrNull with invalid JSON
    try
        result = utils.parseOrNull('not json');
        assert(isempty(result), 'parseOrNull invalid test failed');
        fprintf('✓ Test 18: parseOrNull with invalid JSON\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 18: parseOrNull with invalid JSON - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 19: Get with default value
    try
        data = struct('existing', 'value');
        result = utils.get(data, 'existing', 'default');
        assert(strcmp(result, 'value'), 'Get existing test failed');
        result = utils.get(data, 'missing', 'default');
        assert(strcmp(result, 'default'), 'Get default test failed');
        fprintf('✓ Test 19: Get with default value\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 19: Get with default value - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 20: GetPath nested access
    try
        data = struct('level1', struct('level2', struct('value', 'deep')));
        result = utils.getPath(data, 'level1.level2.value', 'default');
        assert(strcmp(result, 'deep'), 'GetPath test failed');
        result = utils.getPath(data, 'level1.missing.value', 'default');
        assert(strcmp(result, 'default'), 'GetPath default test failed');
        fprintf('✓ Test 20: GetPath nested access\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 20: GetPath nested access - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 21: Minify JSON
    try
        minified = utils.minify('{  "a"  :  1  ,  "b"  :  2  }');
        assert(strcmp(minified, '{"a":1,"b":2}'), 'Minify test failed');
        fprintf('✓ Test 21: Minify JSON\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 21: Minify JSON - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 22: Static quickParse
    try
        result = json_utils.mod.quickParse('{"static": true}');
        assert(result.static == true, 'Static quickParse test failed');
        fprintf('✓ Test 22: Static quickParse\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 22: Static quickParse - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 23: Static quickEncode
    try
        json = json_utils.mod.quickEncode(struct('quick', 'test'));
        assert(contains(json, '"quick":"test"'), 'Static quickEncode test failed');
        fprintf('✓ Test 23: Static quickEncode\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 23: Static quickEncode - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 24: Parse array of objects
    try
        result = utils.parse('[{"id": 1}, {"id": 2}, {"id": 3}]');
        assert(iscell(result) && length(result) == 3 && result{2}.id == 2, ...
               'Array of objects test failed');
        fprintf('✓ Test 24: Parse array of objects\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 24: Parse array of objects - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 25: Encode empty struct
    try
        json = utils.encode(struct());
        assert(strcmp(json, '{}'), 'Encode empty struct test failed');
        fprintf('✓ Test 25: Encode empty struct\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 25: Encode empty struct - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Summary
    fprintf('\n====================================\n');
    fprintf('Test Results: %d passed, %d failed\n', passed, failed);

    if failed == 0
        fprintf('All tests passed! ✓\n');
    else
        fprintf('Some tests failed. ✗\n');
    end
end
