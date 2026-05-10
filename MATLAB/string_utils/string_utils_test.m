function string_utils_test()
    %STRING_UTILS_TEST Test suite for String Utilities
    %   Runs all tests for the string manipulation utilities.
    %
    %   Usage:
    %       string_utils_test()

    fprintf('Running String Utilities Test Suite...\n');
    fprintf('====================================\n\n');

    utils = string_utils.mod();
    passed = 0;
    failed = 0;

    %% Test 1: Trim whitespace
    try
        result = utils.trim('  hello  ');
        assert(strcmp(result, 'hello'), 'Trim test failed');
        fprintf('✓ Test 1: Trim whitespace\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 1: Trim whitespace - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 2: TrimLeft
    try
        result = utils.trimLeft('  hello  ');
        assert(strcmp(result, 'hello  '), 'TrimLeft test failed');
        fprintf('✓ Test 2: TrimLeft\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 2: TrimLeft - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 3: TrimRight
    try
        result = utils.trimRight('  hello  ');
        assert(strcmp(result, '  hello'), 'TrimRight test failed');
        fprintf('✓ Test 3: TrimRight\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 3: TrimRight - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 4: Strip characters
    try
        result = utils.strip('**hello**', '*');
        assert(strcmp(result, 'hello'), 'Strip test failed');
        fprintf('✓ Test 4: Strip characters\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 4: Strip characters - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 5: PadLeft
    try
        result = utils.padLeft('42', 5, '0');
        assert(strcmp(result, '00042'), 'PadLeft test failed');
        fprintf('✓ Test 5: PadLeft\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 5: PadLeft - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 6: PadRight
    try
        result = utils.padRight('hello', 10, '-');
        assert(strcmp(result, 'hello-----'), 'PadRight test failed');
        fprintf('✓ Test 6: PadRight\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 6: PadRight - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 7: PadCenter
    try
        result = utils.padCenter('hi', 6, '-');
        assert(strcmp(result, '--hi--'), 'PadCenter test failed');
        fprintf('✓ Test 7: PadCenter\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 7: PadCenter - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 8: toCamelCase
    try
        result = utils.toCamelCase('hello_world');
        assert(strcmp(result, 'helloWorld'), 'toCamelCase test failed');
        result = utils.toCamelCase('hello-world');
        assert(strcmp(result, 'helloWorld'), 'toCamelCase hyphen test failed');
        fprintf('✓ Test 8: toCamelCase\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 8: toCamelCase - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 9: toPascalCase
    try
        result = utils.toPascalCase('hello_world');
        assert(strcmp(result, 'HelloWorld'), 'toPascalCase test failed');
        fprintf('✓ Test 9: toPascalCase\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 9: toPascalCase - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 10: toSnakeCase
    try
        result = utils.toSnakeCase('helloWorld');
        assert(strcmp(result, 'hello_world'), 'toSnakeCase test failed');
        fprintf('✓ Test 10: toSnakeCase\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 10: toSnakeCase - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 11: toKebabCase
    try
        result = utils.toKebabCase('helloWorld');
        assert(strcmp(result, 'hello-world'), 'toKebabCase test failed');
        fprintf('✓ Test 11: toKebabCase\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 11: toKebabCase - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 12: toTitleCase
    try
        result = utils.toTitleCase('hello world');
        assert(strcmp(result, 'Hello World'), 'toTitleCase test failed');
        fprintf('✓ Test 12: toTitleCase\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 12: toTitleCase - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 13: Capitalize
    try
        result = utils.capitalize('hello');
        assert(strcmp(result, 'Hello'), 'Capitalize test failed');
        fprintf('✓ Test 13: Capitalize\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 13: Capitalize - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 14: Split
    try
        result = utils.split('a,b,c', ',');
        assert(length(result) == 3 && strcmp(result{2}, 'b'), 'Split test failed');
        fprintf('✓ Test 14: Split\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 14: Split - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 15: Join
    try
        result = utils.join({'a', 'b', 'c'}, '-');
        assert(strcmp(result, 'a-b-c'), 'Join test failed');
        fprintf('✓ Test 15: Join\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 15: Join - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 16: SplitLines
    try
        result = utils.splitLines('line1\nline2\nline3');
        assert(length(result) == 3 && strcmp(result{2}, 'line2'), 'SplitLines test failed');
        fprintf('✓ Test 16: SplitLines\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 16: SplitLines - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 17: Reverse
    try
        result = utils.reverse('hello');
        assert(strcmp(result, 'olleh'), 'Reverse test failed');
        fprintf('✓ Test 17: Reverse\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 17: Reverse - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 18: Repeat
    try
        result = utils.repeat('ab', 3);
        assert(strcmp(result, 'ababab'), 'Repeat test failed');
        fprintf('✓ Test 18: Repeat\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 18: Repeat - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 19: Truncate
    try
        result = utils.truncate('Hello World', 8);
        assert(strcmp(result, 'Hello...'), 'Truncate test failed');
        result = utils.truncate('Hello', 10);
        assert(strcmp(result, 'Hello'), 'Truncate no-cut test failed');
        fprintf('✓ Test 19: Truncate\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 19: Truncate - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 20: TruncateWords
    try
        result = utils.truncateWords('Hello beautiful world', 2);
        assert(strcmp(result, 'Hello beautiful...'), 'TruncateWords test failed');
        fprintf('✓ Test 20: TruncateWords\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 20: TruncateWords - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 21: StartsWith
    try
        assert(utils.startsWith('hello world', 'hello') == true, 'StartsWith true test failed');
        assert(utils.startsWith('hello world', 'world') == false, 'StartsWith false test failed');
        fprintf('✓ Test 21: StartsWith\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 21: StartsWith - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 22: EndsWith
    try
        assert(utils.endsWith('hello world', 'world') == true, 'EndsWith true test failed');
        assert(utils.endsWith('hello world', 'hello') == false, 'EndsWith false test failed');
        fprintf('✓ Test 22: EndsWith\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 22: EndsWith - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 23: Contains
    try
        assert(utils.contains('hello world', 'wor') == true, 'Contains true test failed');
        assert(utils.contains('hello world', 'xyz') == false, 'Contains false test failed');
        fprintf('✓ Test 23: Contains\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 23: Contains - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 24: isEmpty
    try
        assert(utils.isEmpty('   ') == true, 'isEmpty whitespace test failed');
        assert(utils.isEmpty('hello') == false, 'isEmpty non-empty test failed');
        fprintf('✓ Test 24: isEmpty\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 24: isEmpty - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 25: isNumeric
    try
        assert(utils.isNumeric('123.45') == true, 'isNumeric true test failed');
        assert(utils.isNumeric('abc') == false, 'isNumeric false test failed');
        fprintf('✓ Test 25: isNumeric\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 25: isNumeric - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 26: isAlpha
    try
        assert(utils.isAlpha('Hello') == true, 'isAlpha true test failed');
        assert(utils.isAlpha('Hello1') == false, 'isAlpha false test failed');
        fprintf('✓ Test 26: isAlpha\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 26: isAlpha - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 27: isAlphanumeric
    try
        assert(utils.isAlphanumeric('Hello123') == true, 'isAlphanumeric true test failed');
        assert(utils.isAlphanumeric('Hello!') == false, 'isAlphanumeric false test failed');
        fprintf('✓ Test 27: isAlphanumeric\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 27: isAlphanumeric - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 28: Count
    try
        result = utils.count('hello hello hello', 'hello');
        assert(result == 3, 'Count test failed');
        fprintf('✓ Test 28: Count\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 28: Count - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 29: CountWords
    try
        result = utils.countWords('Hello beautiful world');
        assert(result == 3, 'CountWords test failed');
        fprintf('✓ Test 29: CountWords\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 29: CountWords - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 30: Replace
    try
        result = utils.replace('hello world', 'world', 'MATLAB');
        assert(strcmp(result, 'hello MATLAB'), 'Replace test failed');
        fprintf('✓ Test 30: Replace\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 30: Replace - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 31: ReplaceFirst
    try
        result = utils.replaceFirst('aaa', 'a', 'b');
        assert(strcmp(result, 'baa'), 'ReplaceFirst test failed');
        fprintf('✓ Test 31: ReplaceFirst\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 31: ReplaceFirst - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 32: ReplaceLast
    try
        result = utils.replaceLast('aaa', 'a', 'b');
        assert(strcmp(result, 'aab'), 'ReplaceLast test failed');
        fprintf('✓ Test 32: ReplaceLast\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 32: ReplaceLast - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 33: Left
    try
        result = utils.left('hello world', 5);
        assert(strcmp(result, 'hello'), 'Left test failed');
        fprintf('✓ Test 33: Left\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 33: Left - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 34: Right
    try
        result = utils.right('hello world', 5);
        assert(strcmp(result, 'world'), 'Right test failed');
        fprintf('✓ Test 34: Right\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 34: Right - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 35: Mid
    try
        result = utils.mid('hello world', 3, 4);
        assert(strcmp(result, 'llo '), 'Mid test failed');
        fprintf('✓ Test 35: Mid\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 35: Mid - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 36: Format positional
    try
        result = utils.format('Hello {}!', 'World');
        assert(strcmp(result, 'Hello World!'), 'Format positional test failed');
        fprintf('✓ Test 36: Format positional\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 36: Format positional - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 37: Format indexed
    try
        result = utils.format('{1} {2}!', 'Hello', 'World');
        assert(strcmp(result, 'Hello World!'), 'Format indexed test failed');
        fprintf('✓ Test 37: Format indexed\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 37: Format indexed - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 38: Slugify
    try
        result = utils.slugify('Hello World!');
        assert(strcmp(result, 'hello-world'), 'Slugify test failed');
        result = utils.slugify('This  is  a  Test');
        assert(strcmp(result, 'this-is-a-test'), 'Slugify multiple spaces test failed');
        fprintf('✓ Test 38: Slugify\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 38: Slugify - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 39: Levenshtein distance
    try
        result = utils.levenshtein('kitten', 'sitting');
        assert(result == 3, 'Levenshtein test failed');
        fprintf('✓ Test 39: Levenshtein distance\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 39: Levenshtein distance - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 40: Similarity
    try
        result = utils.similarity('hello', 'hallo');
        assert(abs(result - 0.8) < 0.01, 'Similarity test failed');
        fprintf('✓ Test 40: Similarity\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 40: Similarity - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 41: Soundex
    try
        result1 = utils.soundex('Robert');
        result2 = utils.soundex('Rupert');
        assert(strcmp(result1, result2), 'Soundex test failed');
        fprintf('✓ Test 41: Soundex (Robert=Rupert)\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 41: Soundex - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 42: Chars
    try
        result = utils.chars('hello');
        assert(length(result) == 5 && strcmp(result{1}, 'h'), 'Chars test failed');
        fprintf('✓ Test 42: Chars\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 42: Chars - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 43: FromChars
    try
        result = utils.fromChars({'h', 'e', 'l', 'l', 'o'});
        assert(strcmp(result, 'hello'), 'FromChars test failed');
        fprintf('✓ Test 43: FromChars\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 43: FromChars - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 44: Insert
    try
        result = utils.insert('helloworld', 5, ' ');
        assert(strcmp(result, 'hello world'), 'Insert test failed');
        fprintf('✓ Test 44: Insert\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 44: Insert - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 45: RemoveWhitespace
    try
        result = utils.removeWhitespace('hello world');
        assert(strcmp(result, 'helloworld'), 'RemoveWhitespace test failed');
        fprintf('✓ Test 45: RemoveWhitespace\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 45: RemoveWhitespace - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 46: NormalizeWhitespace
    try
        result = utils.normalizeWhitespace('hello    world');
        assert(strcmp(result, 'hello world'), 'NormalizeWhitespace test failed');
        fprintf('✓ Test 46: NormalizeWhitespace\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 46: NormalizeWhitespace - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 47: Between
    try
        result = utils.between('Hello [world]!', '[', ']');
        assert(strcmp(result, 'world'), 'Between test failed');
        fprintf('✓ Test 47: Between\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 47: Between - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 48: AfterFirst
    try
        result = utils.afterFirst('a/b/c', '/');
        assert(strcmp(result, 'b/c'), 'AfterFirst test failed');
        fprintf('✓ Test 48: AfterFirst\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 48: AfterFirst - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 49: AfterLast
    try
        result = utils.afterLast('a/b/c', '/');
        assert(strcmp(result, 'c'), 'AfterLast test failed');
        fprintf('✓ Test 49: AfterLast\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 49: AfterLast - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 50: BeforeFirst
    try
        result = utils.beforeFirst('a/b/c', '/');
        assert(strcmp(result, 'a'), 'BeforeFirst test failed');
        fprintf('✓ Test 50: BeforeFirst\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 50: BeforeFirst - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 51: BeforeLast
    try
        result = utils.beforeLast('a/b/c', '/');
        assert(strcmp(result, 'a/b'), 'BeforeLast test failed');
        fprintf('✓ Test 51: BeforeLast\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 51: BeforeLast - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 52: Surround
    try
        result = utils.surround('hello', '**');
        assert(strcmp(result, '**hello**'), 'Surround test failed');
        fprintf('✓ Test 52: Surround\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 52: Surround - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 53: Quote
    try
        result = utils.quote('hello');
        assert(strcmp(result, '"hello"'), 'Quote test failed');
        fprintf('✓ Test 53: Quote\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 53: Quote - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 54: Unquote
    try
        result = utils.unquote('"hello"');
        assert(strcmp(result, 'hello'), 'Unquote double test failed');
        result = utils.unquote('''hello''');
        assert(strcmp(result, 'hello'), 'Unquote single test failed');
        fprintf('✓ Test 54: Unquote\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 54: Unquote - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 55: WordWrap
    try
        result = utils.wordWrap('Hello beautiful world', 10);
        lines = utils.splitLines(result);
        assert(strcmp(lines{1}, 'Hello') || strcmp(lines{1}, 'Hello beaut'), 'WordWrap test failed');
        fprintf('✓ Test 55: WordWrap\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 55: WordWrap - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 56: Static quickTrim
    try
        result = string_utils.mod.quickTrim('  hello  ');
        assert(strcmp(result, 'hello'), 'quickTrim test failed');
        fprintf('✓ Test 56: Static quickTrim\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 56: Static quickTrim - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 57: Static quickSlugify
    try
        result = string_utils.mod.quickSlugify('Hello World!');
        assert(strcmp(result, 'hello-world'), 'quickSlugify test failed');
        fprintf('✓ Test 57: Static quickSlugify\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 57: Static quickSlugify - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 58: Static quickCamelCase
    try
        result = string_utils.mod.quickCamelCase('hello_world');
        assert(strcmp(result, 'helloWorld'), 'quickCamelCase test failed');
        fprintf('✓ Test 58: Static quickCamelCase\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 58: Static quickCamelCase - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 59: Static quickFormat
    try
        result = string_utils.mod.quickFormat('Hello {}!', 'World');
        assert(strcmp(result, 'Hello World!'), 'quickFormat test failed');
        fprintf('✓ Test 59: Static quickFormat\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 59: Static quickFormat - %s\n', ME.message);
        failed = failed + 1;
    end

    %% Test 60: RemoveChars
    try
        result = utils.removeChars('hello world', 'lo');
        assert(strcmp(result, 'he wrd'), 'RemoveChars test failed');
        fprintf('✓ Test 60: RemoveChars\n');
        passed = passed + 1;
    catch ME
        fprintf('✗ Test 60: RemoveChars - %s\n', ME.message);
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