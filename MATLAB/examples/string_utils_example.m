%% String Utilities Examples
% This script demonstrates the usage of string_utils.mod
% for various string manipulation operations.
%
% Author: AllToolkit
% Version: 1.0.0

fprintf('String Utilities Examples\n');
fprintf('=========================\n\n');

%% Initialize
utils = string_utils.mod();

%% Example 1: Trimming Operations
fprintf('=== Example 1: Trimming Operations ===\n');
str = '   hello world   ';
fprintf('Original: "%s"\n', str);
fprintf('Trim: "%s"\n', utils.trim(str));
fprintf('TrimLeft: "%s"\n', utils.trimLeft(str));
fprintf('TrimRight: "%s"\n', utils.trimRight(str));
fprintf('Strip "*" from "**hello**": "%s"\n', utils.strip('**hello**', '*'));
fprintf('\n');

%% Example 2: Padding Operations
fprintf('=== Example 2: Padding Operations ===\n');
fprintf('PadLeft("42", 5, "0"): "%s"\n', utils.padLeft('42', 5, '0'));
fprintf('PadRight("hello", 10, "-"): "%s"\n', utils.padRight('hello', 10, '-'));
fprintf('PadCenter("hi", 6, "-"): "%s"\n', utils.padCenter('hi', 6, '-'));
fprintf('\n');

%% Example 3: Case Conversion
fprintf('=== Example 3: Case Conversion ===\n');
fprintf('toCamelCase("hello_world"): "%s"\n', utils.toCamelCase('hello_world'));
fprintf('toPascalCase("hello_world"): "%s"\n', utils.toPascalCase('hello_world'));
fprintf('toSnakeCase("helloWorld"): "%s"\n', utils.toSnakeCase('helloWorld'));
fprintf('toKebabCase("helloWorld"): "%s"\n', utils.toKebabCase('helloWorld'));
fprintf('toTitleCase("hello world"): "%s"\n', utils.toTitleCase('hello world'));
fprintf('capitalize("hello"): "%s"\n', utils.capitalize('hello'));
fprintf('\n');

%% Example 4: Split and Join
fprintf('=== Example 4: Split and Join ===\n');
parts = utils.split('apple,banana,cherry', ',');
fprintf('Split "apple,banana,cherry" by ",": %s\n', strjoin(parts, ' | '));
fprintf('Join back: "%s"\n', utils.join(parts, '-'));
lines = utils.splitLines('Line 1\nLine 2\nLine 3');
fprintf('SplitLines count: %d\n', length(lines));
fprintf('\n');

%% Example 5: String Operations
fprintf('=== Example 5: String Operations ===\n');
fprintf('reverse("hello"): "%s"\n', utils.reverse('hello'));
fprintf('repeat("ab", 3): "%s"\n', utils.repeat('ab', 3));
fprintf('truncate("Hello World", 8): "%s"\n', utils.truncate('Hello World', 8));
fprintf('truncateWords("Hello beautiful world", 2): "%s"\n', utils.truncateWords('Hello beautiful world', 2));
fprintf('\n');

%% Example 6: Checking Methods
fprintf('=== Example 6: Checking Methods ===\n');
fprintf('startsWith("hello world", "hello"): %s\n', string(utils.startsWith('hello world', 'hello')));
fprintf('endsWith("hello world", "world"): %s\n', string(utils.endsWith('hello world', 'world')));
fprintf('contains("hello world", "wor"): %s\n', string(utils.contains('hello world', 'wor')));
fprintf('isEmpty("   "): %s\n', string(utils.isEmpty('   ')));
fprintf('isNumeric("123.45"): %s\n', string(utils.isNumeric('123.45')));
fprintf('isAlpha("Hello"): %s\n', string(utils.isAlpha('Hello')));
fprintf('isAlphanumeric("Hello123"): %s\n', string(utils.isAlphanumeric('Hello123')));
fprintf('\n');

%% Example 7: Counting Methods
fprintf('=== Example 7: Counting Methods ===\n');
fprintf('count("hello hello hello", "hello"): %d\n', utils.count('hello hello hello', 'hello'));
fprintf('countWords("Hello beautiful world"): %d\n', utils.countWords('Hello beautiful world'));
fprintf('length("hello"): %d\n', utils.length('hello'));
fprintf('charCount("hello", "l"): %d\n', utils.charCount('hello', 'l'));
fprintf('\n');

%% Example 8: Replace Methods
fprintf('=== Example 8: Replace Methods ===\n');
fprintf('replace("hello world", "world", "MATLAB"): "%s"\n', utils.replace('hello world', 'world', 'MATLAB'));
fprintf('replaceFirst("aaa", "a", "b"): "%s"\n', utils.replaceFirst('aaa', 'a', 'b'));
fprintf('replaceLast("aaa", "a", "b"): "%s"\n', utils.replaceLast('aaa', 'a', 'b'));
fprintf('\n');

%% Example 9: Substring Methods
fprintf('=== Example 9: Substring Methods ===\n');
fprintf('substring("hello world", 1, 5): "%s"\n', utils.substring('hello world', 1, 5));
fprintf('left("hello world", 5): "%s"\n', utils.left('hello world', 5));
fprintf('right("hello world", 5): "%s"\n', utils.right('hello world', 5));
fprintf('mid("hello world", 3, 4): "%s"\n', utils.mid('hello world', 3, 4));
fprintf('\n');

%% Example 10: Format and Slugify
fprintf('=== Example 10: Format and Slugify ===\n');
fprintf('format("Hello {}!", "World"): "%s"\n', utils.format('Hello {}!', 'World'));
fprintf('format("{1} {2}!", "Hello", "World"): "%s"\n', utils.format('{1} {2}!', 'Hello', 'World'));
fprintf('slugify("Hello World!"): "%s"\n', utils.slugify('Hello World!'));
fprintf('slugify("This  is  a  Test"): "%s"\n', utils.slugify('This  is  a  Test'));
fprintf('\n');

%% Example 11: Similarity
fprintf('=== Example 11: Similarity ===\n');
fprintf('levenshtein("kitten", "sitting"): %d\n', utils.levenshtein('kitten', 'sitting'));
fprintf('similarity("hello", "hallo"): %.2f\n', utils.similarity('hello', 'hallo'));
fprintf('soundex("Robert"): "%s"\n', utils.soundex('Robert'));
fprintf('soundex("Rupert"): "%s"\n', utils.soundex('Rupert'));
fprintf('Note: Robert and Rupert have same Soundex code!\n');
fprintf('\n');

%% Example 12: Utility Methods
fprintf('=== Example 12: Utility Methods ===\n');
fprintf('chars("hello"): %s\n', strjoin(utils.chars('hello'), ','));
fprintf('fromChars({"h","e","l","l","o"}): "%s"\n', utils.fromChars({'h','e','l','l','o'}));
fprintf('insert("helloworld", 5, " "): "%s"\n', utils.insert('helloworld', 5, ' '));
fprintf('removeWhitespace("hello world"): "%s"\n', utils.removeWhitespace('hello world'));
fprintf('normalizeWhitespace("hello    world"): "%s"\n', utils.normalizeWhitespace('hello    world'));
fprintf('\n');

%% Example 13: Between and Surround
fprintf('=== Example 13: Between and Surround ===\n');
fprintf('between("Hello [world]!", "[", "]"): "%s"\n', utils.between('Hello [world]!', '[', ']'));
fprintf('afterFirst("a/b/c", "/"): "%s"\n', utils.afterFirst('a/b/c', '/'));
fprintf('afterLast("a/b/c", "/"): "%s"\n', utils.afterLast('a/b/c', '/'));
fprintf('beforeFirst("a/b/c", "/"): "%s"\n', utils.beforeFirst('a/b/c', '/'));
fprintf('beforeLast("a/b/c", "/"): "%s"\n', utils.beforeLast('a/b/c', '/'));
fprintf('surround("hello", "**"): "%s"\n', utils.surround('hello', '**'));
fprintf('\n');

%% Example 14: Quote Methods
fprintf('=== Example 14: Quote Methods ===\n');
fprintf('quote("hello"): "%s"\n', utils.quote('hello'));
fprintf('singleQuote("hello"): "%s"\n', utils.singleQuote('hello'));
fprintf('unquote(\'"hello"\'): "%s"\n', utils.unquote('"hello"'));
fprintf('\n');

%% Example 15: WordWrap
fprintf('=== Example 15: WordWrap ===\n');
wrapped = utils.wordWrap('This is a long sentence that needs to be wrapped', 20);
fprintf('WordWrap at 20 chars:\n%s\n', wrapped);
fprintf('\n');

%% Example 16: Static Methods
fprintf('=== Example 16: Static Methods ===\n');
fprintf('quickTrim("  hello  "): "%s"\n', string_utils.mod.quickTrim('  hello  '));
fprintf('quickSlugify("Hello World!"): "%s"\n', string_utils.mod.quickSlugify('Hello World!'));
fprintf('quickCamelCase("hello_world"): "%s"\n', string_utils.mod.quickCamelCase('hello_world'));
fprintf('quickFormat("Hello {}!", "World"): "%s"\n', string_utils.mod.quickFormat('Hello {}!', 'World'));
fprintf('\n');

fprintf('Examples completed!\n');