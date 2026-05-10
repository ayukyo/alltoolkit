classdef mod < handle
    %STRING_UTILS String manipulation utilities for MATLAB
    %   A comprehensive collection of string manipulation functions with
    %   zero external dependencies. Provides trimming, padding, case
    %   conversion, splitting, joining, and many other utilities.
    %
    %   Features:
    %   - Trim, strip, and truncate strings
    %   - Pad strings (left, right, center)
    %   - Case conversion (camel, snake, kebab, pascal, title)
    %   - Split and join operations
    %   - String reversal and repetition
    %   - Start/end checking and counting
    %   - Levenshtein distance and similarity
    %   - Word manipulation (capitalize, title case)
    %   - Template string formatting
    %   - URL slug generation
    %   - Character and substring operations
    %
    %   Example:
    %       s = string_utils.mod();
    %       trimmed = s.trim('  hello  ');  % 'hello'
    %       camel = s.toCamelCase('hello_world');  % 'helloWorld'
    %       slug = s.slugify('Hello World!');  % 'hello-world'
    %
    %   Author: AllToolkit
    %   Version: 1.0.0
    %   License: MIT

    methods
        function obj = mod()
            %MOD Constructor for string utilities
            %   Creates a new string utilities instance.
        end

        %% Trimming Methods

        function result = trim(~, str)
            %TRIM Remove leading and trailing whitespace
            %   RESULT = TRIM(STR) removes whitespace from both ends.
            %
            %   Input:
            %       str - Input string
            %
            %   Output:
            %       result - Trimmed string
            %
            %   Example:
            %       s.trim('  hello  ')  % Returns: 'hello'

            result = strtrim(str);
        end

        function result = trimLeft(~, str)
            %TRIMLEFT Remove leading whitespace
            %   RESULT = TRIMLEFT(STR) removes whitespace from start.
            %
            %   Example:
            %       s.trimLeft('  hello  ')  % Returns: 'hello  '

            str = char(str);
            result = str;
            for i = 1:length(str)
                if ~isspace(str(i))
                    result = str(i:end);
                    return;
                end
            end
            result = '';
        end

        function result = trimRight(~, str)
            %TRIMRIGHT Remove trailing whitespace
            %   RESULT = TRIMRIGHT(STR) removes whitespace from end.
            %
            %   Example:
            %       s.trimRight('  hello  ')  % Returns: '  hello'

            str = char(str);
            for i = length(str):-1:1
                if ~isspace(str(i))
                    result = str(1:i);
                    return;
                end
            end
            result = '';
        end

        function result = strip(~, str, chars)
            %STRIP Remove specified characters from both ends
            %   RESULT = STRIP(STR, CHARS) removes all chars from both ends.
            %
            %   Inputs:
            %       str   - Input string
            %       chars - Characters to remove (default: whitespace)
            %
            %   Example:
            %       s.strip('**hello**', '*')  % Returns: 'hello'

            if nargin < 3
                chars = ' ';
            end
            result = obj.stripLeft(obj.stripRight(str, chars), chars);
        end

        function result = stripLeft(~, str, chars)
            %STRIPLEFT Remove specified characters from start
            %   RESULT = STRIPLEFT(STR, CHARS) removes chars from start.

            if nargin < 3
                chars = ' ';
            end
            str = char(str);
            chars = char(chars);
            idx = 1;
            while idx <= length(str) && contains(chars, str(idx))
                idx = idx + 1;
            end
            result = str(idx:end);
        end

        function result = stripRight(~, str, chars)
            %STRIPRIGHT Remove specified characters from end
            %   RESULT = STRIPRIGHT(STR, CHARS) removes chars from end.

            if nargin < 3
                chars = ' ';
            end
            str = char(str);
            chars = char(chars);
            idx = length(str);
            while idx > 0 && contains(chars, str(idx))
                idx = idx - 1;
            end
            result = str(1:idx);
        end

        %% Padding Methods

        function result = padLeft(~, str, length, padChar)
            %PADLEFT Pad string on the left
            %   RESULT = PADLEFT(STR, LENGTH, PADCHAR) pads string to length.
            %
            %   Inputs:
            %       str     - Input string
            %       length  - Target length
            %       padChar - Padding character (default: ' ')
            %
            %   Example:
            %       s.padLeft('42', 5, '0')  % Returns: '00042'

            if nargin < 4
                padChar = ' ';
            end
            str = char(str);
            if length(str) >= length
                result = str;
                return;
            end
            padding = repmat(char(padChar), 1, length - length(str));
            result = [padding, str];
        end

        function result = padRight(~, str, length, padChar)
            %PADRIGHT Pad string on the right
            %   RESULT = PADRIGHT(STR, LENGTH, PADCHAR) pads string to length.
            %
            %   Example:
            %       s.padRight('hello', 10, '-')  % Returns: 'hello-----'

            if nargin < 4
                padChar = ' ';
            end
            str = char(str);
            if length(str) >= length
                result = str;
                return;
            end
            padding = repmat(char(padChar), 1, length - length(str));
            result = [str, padding];
        end

        function result = padCenter(~, str, length, padChar)
            %PADCENTER Center string with padding
            %   RESULT = PADCENTER(STR, LENGTH, PADCHAR) centers the string.
            %
            %   Example:
            %       s.padCenter('hi', 6, '-')  % Returns: '--hi--'

            if nargin < 4
                padChar = ' ';
            end
            str = char(str);
            if length(str) >= length
                result = str;
                return;
            end
            totalPad = length - length(str);
            leftPad = floor(totalPad / 2);
            rightPad = totalPad - leftPad;
            left = repmat(char(padChar), 1, leftPad);
            right = repmat(char(padChar), 1, rightPad);
            result = [left, str, right];
        end

        %% Case Conversion Methods

        function result = toCamelCase(~, str)
            %TOCAMELCASE Convert to camelCase
            %   RESULT = TOCAMELCASE(STR) converts string to camelCase.
            %
            %   Example:
            %       s.toCamelCase('hello_world')  % Returns: 'helloWorld'
            %       s.toCamelCase('hello-world')  % Returns: 'helloWorld'
            %       s.toCamelCase('HelloWorld')   % Returns: 'helloWorld'

            str = char(str);
            % Replace common separators with spaces
            str = regexprep(str, '[_\-\s]+', ' ');
            words = strsplit(strtrim(str), ' ');
            if isempty(words{1})
                result = '';
                return;
            end
            words{1} = lower(words{1});
            for i = 2:length(words)
                if ~isempty(words{i})
                    words{i} = [upper(words{i}(1)), lower(words{i}(2:end))];
                end
            end
            result = strjoin(words, '');
        end

        function result = toPascalCase(~, str)
            %TOPASCALCASE Convert to PascalCase
            %   RESULT = TOPASCALCASE(STR) converts string to PascalCase.
            %
            %   Example:
            %       s.toPascalCase('hello_world')  % Returns: 'HelloWorld'
            %       s.toPascalCase('hello-world')  % Returns: 'HelloWorld'

            str = char(str);
            str = regexprep(str, '[_\-\s]+', ' ');
            words = strsplit(strtrim(str), ' ');
            for i = 1:length(words)
                if ~isempty(words{i})
                    words{i} = [upper(words{i}(1)), lower(words{i}(2:end))];
                end
            end
            result = strjoin(words, '');
        end

        function result = toSnakeCase(~, str)
            %TOSNAKECASE Convert to snake_case
            %   RESULT = TOSNAKECASE(STR) converts string to snake_case.
            %
            %   Example:
            %       s.toSnakeCase('helloWorld')  % Returns: 'hello_world'
            %       s.toSnakeCase('HelloWorld') % Returns: 'hello_world'

            str = char(str);
            % Insert underscore before uppercase letters
            str = regexprep(str, '([a-z0-9])([A-Z])', '$1_$2');
            % Replace spaces and hyphens with underscores
            str = regexprep(str, '[\-\s]+', '_');
            result = lower(str);
        end

        function result = toKebabCase(~, str)
            %TOKEBABCASE Convert to kebab-case
            %   RESULT = TOKEBABCASE(STR) converts string to kebab-case.
            %
            %   Example:
            %       s.toKebabCase('helloWorld')  % Returns: 'hello-world'
            %       s.toKebabCase('HelloWorld')  % Returns: 'hello-world'

            str = char(str);
            str = regexprep(str, '([a-z0-9])([A-Z])', '$1-$2');
            str = regexprep(str, '[_\s]+', '-');
            result = lower(str);
        end

        function result = toTitleCase(~, str)
            %TOTITLECASE Convert to Title Case
            %   RESULT = TOTITLECASE(STR) capitalizes each word.
            %
            %   Example:
            %       s.toTitleCase('hello world')  % Returns: 'Hello World'

            str = char(str);
            words = strsplit(str, ' ');
            for i = 1:length(words)
                if ~isempty(words{i})
                    words{i} = [upper(words{i}(1)), lower(words{i}(2:end))];
                end
            end
            result = strjoin(words, ' ');
        end

        function result = capitalize(~, str)
            %CAPITALIZE Capitalize first character
            %   RESULT = CAPITALIZE(STR) capitalizes only the first character.
            %
            %   Example:
            %       s.capitalize('hello')  % Returns: 'Hello'

            str = char(str);
            if isempty(str)
                result = '';
                return;
            end
            result = [upper(str(1)), lower(str(2:end))];
        end

        function result = capitalizeWords(~, str)
            %CAPITALIZEWORDS Capitalize each word
            %   RESULT = CAPITALIZEWORDS(STR) capitalizes first letter of each word.
            %
            %   Example:
            %       s.capitalizeWords('hello world')  % Returns: 'Hello World'

            str = char(str);
            words = strsplit(str, ' ');
            for i = 1:length(words)
                if ~isempty(words{i})
                    words{i} = [upper(words{i}(1)), words{i}(2:end)];
                end
            end
            result = strjoin(words, ' ');
        end

        %% Split and Join Methods

        function result = split(~, str, delimiter)
            %SPLIT Split string by delimiter
            %   RESULT = SPLIT(STR, DELIMITER) splits string into cell array.
            %
            %   Inputs:
            %       str       - Input string
            %       delimiter - Split delimiter (default: whitespace)
            %
            %   Example:
            %       s.split('a,b,c', ',')  % Returns: {'a', 'b', 'c'}

            if nargin < 3
                delimiter = ' ';
            end
            str = char(str);
            delimiter = char(delimiter);
            if isempty(delimiter)
                result = cellstr(str)';
                return;
            end
            result = strsplit(str, delimiter);
        end

        function result = splitLines(~, str)
            %SPLITLINES Split string into lines
            %   RESULT = SPLITLINES(STR) splits by newlines.
            %
            %   Example:
            %       s.splitLines('line1\nline2')  % Returns: {'line1', 'line2'}

            str = char(str);
            % Handle different line endings
            str = strrep(str, sprintf('\r\n'), sprintf('\n'));
            str = strrep(str, sprintf('\r'), sprintf('\n'));
            result = strsplit(str, sprintf('\n'));
        end

        function result = join(~, parts, delimiter)
            %JOIN Join string array with delimiter
            %   RESULT = JOIN(PARTS, DELIMITER) joins cell array of strings.
            %
            %   Inputs:
            %       parts     - Cell array of strings
            %       delimiter - Join delimiter (default: ' ')
            %
            %   Example:
            %       s.join({'a', 'b', 'c'}, '-')  % Returns: 'a-b-c'

            if nargin < 3
                delimiter = ' ';
            end
            result = strjoin(parts, delimiter);
        end

        function result = lines(~, str)
            %LINES Split string into lines (alias for splitLines)
            %   RESULT = LINES(STR) returns cell array of lines.

            result = obj.splitLines(str);
        end

        %% String Operations

        function result = reverse(~, str)
            %REVERSE Reverse a string
            %   RESULT = REVERSE(STR) returns reversed string.
            %
            %   Example:
            %       s.reverse('hello')  % Returns: 'olleh'

            str = char(str);
            result = str(end:-1:1);
        end

        function result = repeat(~, str, count)
            %REPEAT Repeat string multiple times
            %   RESULT = REPEAT(STR, COUNT) repeats the string.
            %
            %   Example:
            %       s.repeat('ab', 3)  % Returns: 'ababab'

            str = char(str);
            if count <= 0
                result = '';
                return;
            end
            result = repmat(str, [1, count]);
        end

        function result = truncate(~, str, maxLength, suffix)
            %TRUNCATE Truncate string with suffix
            %   RESULT = TRUNCATE(STR, MAXLENGTH, SUFFIX) truncates string.
            %
            %   Inputs:
            %       str       - Input string
            %       maxLength - Maximum length
            %       suffix    - Suffix for truncated strings (default: '...')
            %
            %   Example:
            %       s.truncate('Hello World', 8)  % Returns: 'Hello...'
            %       s.truncate('Hello', 10)       % Returns: 'Hello'

            if nargin < 4
                suffix = '...';
            end
            str = char(str);
            if length(str) <= maxLength
                result = str;
                return;
            end
            if length(suffix) >= maxLength
                result = suffix(1:maxLength);
                return;
            end
            result = [str(1:maxLength-length(suffix)), suffix];
        end

        function result = truncateWords(~, str, maxWords, suffix)
            %TRUNCATEWORDS Truncate to specified number of words
            %   RESULT = TRUNCATEWORDS(STR, MAXWORDS, SUFFIX) truncates by words.
            %
            %   Example:
            %       s.truncateWords('Hello beautiful world', 2)  % Returns: 'Hello beautiful...'

            if nargin < 4
                suffix = '...';
            end
            str = char(str);
            words = strsplit(strtrim(str));
            if length(words) <= maxWords
                result = str;
                return;
            end
            result = [strjoin(words(1:maxWords), ' '), suffix];
        end

        %% Checking Methods

        function result = startsWith(~, str, prefix)
            %STARTSWITH Check if string starts with prefix
            %   RESULT = STARTSWITH(STR, PREFIX) returns true if starts with prefix.
            %
            %   Example:
            %       s.startsWith('hello world', 'hello')  % Returns: true

            str = char(str);
            prefix = char(prefix);
            result = length(str) >= length(prefix) && ...
                     strcmp(str(1:length(prefix)), prefix);
        end

        function result = endsWith(~, str, suffix)
            %ENDSWITH Check if string ends with suffix
            %   RESULT = ENDSWITH(STR, SUFFIX) returns true if ends with suffix.
            %
            %   Example:
            %       s.endsWith('hello world', 'world')  % Returns: true

            str = char(str);
            suffix = char(suffix);
            result = length(str) >= length(suffix) && ...
                     strcmp(str(end-length(suffix)+1:end), suffix);
        end

        function result = contains(~, str, substring)
            %CONTAINS Check if string contains substring
            %   RESULT = CONTAINS(STR, SUBSTRING) returns true if contains.
            %
            %   Example:
            %       s.contains('hello world', 'wor')  % Returns: true

            result = contains(char(str), char(substring));
        end

        function result = isEmpty(~, str)
            %ISEMPTY Check if string is empty or whitespace only
            %   RESULT = ISEMPTY(STR) returns true if empty or whitespace.
            %
            %   Example:
            %       s.isEmpty('   ')  % Returns: true

            str = char(str);
            result = isempty(str) || isempty(strtrim(str));
        end

        function result = isNumeric(~, str)
            %ISNUMERIC Check if string represents a number
            %   RESULT = ISNUMERIC(STR) returns true if string is numeric.
            %
            %   Example:
            %       s.isNumeric('123.45')  % Returns: true
            %       s.isNumeric('abc')     % Returns: false

            str = strtrim(char(str));
            if isempty(str)
                result = false;
                return;
            end
            num = str2double(str);
            result = ~isnan(num);
        end

        function result = isAlpha(~, str)
            %ISALPHA Check if string contains only letters
            %   RESULT = ISALPHA(STR) returns true if only alphabetic chars.
            %
            %   Example:
            %       s.isAlpha('Hello')  % Returns: true
            %       s.isAlpha('Hello1') % Returns: false

            str = char(str);
            if isempty(str)
                result = false;
                return;
            end
            result = all(isletter(str));
        end

        function result = isAlphanumeric(~, str)
            %ISALPHANUMERIC Check if string contains only letters and digits
            %   RESULT = ISALPHANUMERIC(STR) returns true if only alphanumeric.
            %
            %   Example:
            %       s.isAlphanumeric('Hello123')  % Returns: true
            %       s.isAlphanumeric('Hello!')    % Returns: false

            str = char(str);
            if isempty(str)
                result = false;
                return;
            end
            result = all(isletter(str) | isstrprop(str, 'digit'));
        end

        %% Counting Methods

        function result = count(~, str, substring)
            %COUNT Count occurrences of substring
            %   RESULT = COUNT(STR, SUBSTRING) returns count of occurrences.
            %
            %   Example:
            %       s.count('hello hello hello', 'hello')  % Returns: 3

            str = char(str);
            substring = char(substring);
            if isempty(substring)
                result = 0;
                return;
            end
            result = length(strfind(str, substring));
        end

        function result = countWords(~, str)
            %COUNTWORDS Count number of words
            %   RESULT = COUNTWORDS(STR) returns number of words.
            %
            %   Example:
            %       s.countWords('Hello beautiful world')  % Returns: 3

            str = strtrim(char(str));
            if isempty(str)
                result = 0;
                return;
            end
            words = strsplit(str);
            result = length(words);
        end

        function result = length(~, str)
            %LENGTH Get string length
            %   RESULT = LENGTH(STR) returns number of characters.
            %
            %   Example:
            %       s.length('hello')  % Returns: 5

            result = length(char(str));
        end

        function result = charCount(~, str, char)
            %CHARCOUNT Count occurrences of a specific character
            %   RESULT = CHARCOUNT(STR, CHAR) returns count of specific char.
            %
            %   Example:
            %       s.charCount('hello', 'l')  % Returns: 2

            str = char(str);
            if isempty(char)
                result = 0;
                return;
            end
            result = sum(str == char(1));
        end

        %% Replace Methods

        function result = replace(~, str, search, replaceStr)
            %REPLACE Replace all occurrences
            %   RESULT = REPLACE(STR, SEARCH, REPLACESTR) replaces all occurrences.
            %
            %   Example:
            %       s.replace('hello world', 'world', 'MATLAB')  % Returns: 'hello MATLAB'

            result = strrep(char(str), char(search), char(replaceStr));
        end

        function result = replaceFirst(~, str, search, replaceStr)
            %REPLACEFIRST Replace first occurrence
            %   RESULT = REPLACEFIRST(STR, SEARCH, REPLACESTR) replaces first match.
            %
            %   Example:
            %       s.replaceFirst('aaa', 'a', 'b')  % Returns: 'baa'

            str = char(str);
            search = char(search);
            replaceStr = char(replaceStr);
            idx = strfind(str, search);
            if isempty(idx)
                result = str;
                return;
            end
            pos = idx(1);
            result = [str(1:pos-1), replaceStr, str(pos+length(search):end)];
        end

        function result = replaceLast(~, str, search, replaceStr)
            %REPLACELAST Replace last occurrence
            %   RESULT = REPLACELAST(STR, SEARCH, REPLACESTR) replaces last match.
            %
            %   Example:
            %       s.replaceLast('aaa', 'a', 'b')  % Returns: 'aab'

            str = char(str);
            search = char(search);
            replaceStr = char(replaceStr);
            idx = strfind(str, search);
            if isempty(idx)
                result = str;
                return;
            end
            pos = idx(end);
            result = [str(1:pos-1), replaceStr, str(pos+length(search):end)];
        end

        %% Substring Methods

        function result = substring(~, str, startIdx, endIdx)
            %SUBSTRING Extract substring by indices
            %   RESULT = SUBSTRING(STR, STARTIDX, ENDIDX) extracts substring.
            %
            %   Inputs:
            %       str      - Input string
            %       startIdx - Start index (1-based, inclusive)
            %       endIdx   - End index (inclusive, optional)
            %
            %   Example:
            %       s.substring('hello world', 1, 5)  % Returns: 'hello'
            %       s.substring('hello world', 7)     % Returns: 'world'

            str = char(str);
            if nargin < 4
                endIdx = length(str);
            end
            if startIdx < 1
                startIdx = 1;
            end
            if endIdx > length(str)
                endIdx = length(str);
            end
            result = str(startIdx:endIdx);
        end

        function result = left(~, str, n)
            %LEFT Get leftmost n characters
            %   RESULT = LEFT(STR, N) returns first n characters.
            %
            %   Example:
            %       s.left('hello world', 5)  % Returns: 'hello'

            str = char(str);
            if n <= 0
                result = '';
                return;
            end
            if n >= length(str)
                result = str;
                return;
            end
            result = str(1:n);
        end

        function result = right(~, str, n)
            %RIGHT Get rightmost n characters
            %   RESULT = RIGHT(STR, N) returns last n characters.
            %
            %   Example:
            %       s.right('hello world', 5)  % Returns: 'world'

            str = char(str);
            if n <= 0
                result = '';
                return;
            end
            if n >= length(str)
                result = str;
                return;
            end
            result = str(end-n+1:end);
        end

        function result = mid(~, str, start, length)
            %MID Get substring from position with length
            %   RESULT = MID(STR, START, LENGTH) extracts from position.
            %
            %   Example:
            %       s.mid('hello world', 3, 4)  % Returns: 'llo '

            str = char(str);
            if start < 1
                start = 1;
            end
            if start > length(str)
                result = '';
                return;
            end
            endIdx = min(start + length - 1, length(str));
            result = str(start:endIdx);
        end

        %% Template and Format Methods

        function result = format(~, template, varargin)
            %FORMAT Format string with placeholders
            %   RESULT = FORMAT(TEMPLATE, ...) substitutes placeholders.
            %
            %   Placeholders:
            %       {}   - Positional argument
            %       {n}  - Indexed argument (1-based)
            %       {name} - Named argument (using struct)
            %
            %   Example:
            %       s.format('Hello {}!', 'World')  % Returns: 'Hello World!'
            %       s.format('{1} {2}!', 'Hello', 'World')  % Returns: 'Hello World!'

            template = char(template);
            result = template;
            
            if isempty(varargin)
                return;
            end
            
            % Handle struct for named placeholders
            if nargin == 3 && isstruct(varargin{1})
                data = varargin{1};
                fields = fieldnames(data);
                for i = 1:length(fields)
                    result = strrep(result, ['{', fields{i}, '}'], char(data.(fields{i})));
                end
                return;
            end
            
            % Handle indexed placeholders first
            idx = regexp(result, '\{(\d+)\}', 'tokens');
            for i = 1:length(idx)
                num = str2double(idx{i}{1});
                if num >= 1 && num <= length(varargin)
                    result = strrep(result, ['{', idx{i}{1}, '}'], char(varargin{num}));
                end
            end
            
            % Handle positional placeholders
            pos = 1;
            while ~isempty(regexp(result, '\{\}', 'once'))
                if pos > length(varargin)
                    break;
                end
                result = regexprep(result, '\{\}', char(varargin{pos}), 'once');
                pos = pos + 1;
            end
        end

        %% Slugify Method

        function result = slugify(~, str)
            %SLUGIFY Convert string to URL-friendly slug
            %   RESULT = SLUGIFY(STR) creates URL-safe string.
            %
            %   Example:
            %       s.slugify('Hello World!')   % Returns: 'hello-world'
            %       s.slugify('This is a Test') % Returns: 'this-is-a-test'

            str = char(str);
            % Convert to lowercase
            result = lower(str);
            % Replace spaces and common separators with hyphens
            result = regexprep(result, '[\s_]+', '-');
            % Remove non-alphanumeric characters except hyphens
            result = regexprep(result, '[^a-z0-9\-]', '');
            % Remove consecutive hyphens
            result = regexprep(result, '-+', '-');
            % Remove leading/trailing hyphens
            result = regexprep(result, '^-|-$', '');
        end

        %% Similarity Methods

        function result = levenshtein(~, str1, str2)
            %LEVENSHTEIN Calculate Levenshtein distance
            %   RESULT = LEVENSHTEIN(STR1, STR2) returns edit distance.
            %
            %   Example:
            %       s.levenshtein('kitten', 'sitting')  % Returns: 3

            str1 = char(str1);
            str2 = char(str2);
            
            m = length(str1);
            n = length(str2);
            
            if m == 0
                result = n;
                return;
            end
            if n == 0
                result = m;
                return;
            end
            
            % Create distance matrix
            d = zeros(m + 1, n + 1);
            
            for i = 0:m
                d(i + 1, 1) = i;
            end
            for j = 0:n
                d(1, j + 1) = j;
            end
            
            for i = 1:m
                for j = 1:n
                    if str1(i) == str2(j)
                        cost = 0;
                    else
                        cost = 1;
                    end
                    d(i + 1, j + 1) = min([d(i, j + 1) + 1, ...
                                          d(i + 1, j) + 1, ...
                                          d(i, j) + cost]);
                end
            end
            
            result = d(m + 1, n + 1);
        end

        function result = similarity(~, str1, str2)
            %SIMILARITY Calculate similarity ratio (0 to 1)
            %   RESULT = SIMILARITY(STR1, STR2) returns similarity ratio.
            %
            %   Example:
            %       s.similarity('hello', 'hallo')  % Returns: 0.8

            str1 = char(str1);
            str2 = char(str2);
            
            if isempty(str1) && isempty(str2)
                result = 1.0;
                return;
            end
            
            maxLen = max(length(str1), length(str2));
            if maxLen == 0
                result = 1.0;
                return;
            end
            
            dist = obj.levenshtein(str1, str2);
            result = 1.0 - (dist / maxLen);
        end

        function result = soundex(~, str)
            %SOUNDEX Calculate Soundex code for phonetic matching
            %   RESULT = SOUNDEX(STR) returns 4-character Soundex code.
            %
            %   Example:
            %       s.soundex('Robert')  % Returns: 'R163'
            %       s.soundex('Rupert')  % Returns: 'R163'

            str = upper(char(str));
            if isempty(str)
                result = '0000';
                return;
            end
            
            % Soundex letter mapping
            mapping = containers.Map(...
                {'B', 'F', 'P', 'V', 'C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z', ...
                 'D', 'T', 'L', 'M', 'N', 'R', 'A', 'E', 'I', 'O', 'U', 'H', 'W', 'Y'}, ...
                {'1', '1', '1', '1', '2', '2', '2', '2', '2', '2', '2', '2', ...
                 '3', '3', '4', '5', '5', '6', '0', '0', '0', '0', '0', '0', '0', '0'});
            
            % Keep first letter
            result = str(1);
            prevCode = '0';
            
            if isKey(mapping, str(1))
                prevCode = mapping(str(1));
            end
            
            for i = 2:length(str)
                if isKey(mapping, str(i))
                    code = mapping(str(i));
                    if ~strcmp(code, '0') && ~strcmp(code, prevCode)
                        result = [result, code];
                        if length(result) >= 4
                            break;
                        end
                    end
                    prevCode = code;
                else
                    prevCode = '0';
                end
            end
            
            % Pad or truncate to 4 characters
            while length(result) < 4
                result = [result, '0'];
            end
            result = result(1:4);
        end

        %% Utility Methods

        function result = chars(~, str)
            %CHARS Convert string to cell array of characters
            %   RESULT = CHARS(STR) returns each character in a cell.
            %
            %   Example:
            %       s.chars('hello')  % Returns: {'h', 'e', 'l', 'l', 'o'}

            str = char(str);
            result = cellstr(num2cell(str))';
        end

        function result = fromChars(~, charArray)
            %FROMCHARS Convert cell array of chars to string
            %   RESULT = FROMCHARS(CHARARRAY) joins characters.
            %
            %   Example:
            %       s.fromChars({'h', 'e', 'l', 'l', 'o'})  % Returns: 'hello'

            result = strjoin(charArray, '');
        end

        function result = insert(~, str, index, insertStr)
            %INSERT Insert string at position
            %   RESULT = INSERT(STR, INDEX, INSERTSTR) inserts at index.
            %
            %   Example:
            %       s.insert('helloworld', 5, ' ')  % Returns: 'hello world'

            str = char(str);
            insertStr = char(insertStr);
            
            if index < 1
                index = 1;
            elseif index > length(str)
                index = length(str) + 1;
            end
            
            result = [str(1:index-1), insertStr, str(index:end)];
        end

        function result = remove(~, str, startIdx, length)
            %REMOVE Remove substring from string
            %   RESULT = REMOVE(STR, STARTIDX, LENGTH) removes characters.
            %
            %   Example:
            %       s.remove('hello world', 6, 1)  % Returns: 'helloworld'

            str = char(str);
            
            if startIdx < 1 || startIdx > length(str)
                result = str;
                return;
            end
            
            endIdx = min(startIdx + length - 1, length(str));
            result = [str(1:startIdx-1), str(endIdx+1:end)];
        end

        function result = removeChars(~, str, chars)
            %REMOVECHARS Remove specific characters
            %   RESULT = REMOVECHARS(STR, CHARS) removes all specified chars.
            %
            %   Example:
            %       s.removeChars('hello world', 'lo')  % Returns: 'he wrd'

            str = char(str);
            chars = char(chars);
            result = str;
            for i = 1:length(chars)
                result = strrep(result, chars(i), '');
            end
        end

        function result = removeWhitespace(~, str)
            %REMOVEWHITESPACE Remove all whitespace
            %   RESULT = REMOVEWHITESPACE(STR) removes all whitespace chars.
            %
            %   Example:
            %       s.removeWhitespace('hello world')  % Returns: 'helloworld'

            str = char(str);
            result = regexprep(str, '\s+', '');
        end

        function result = normalizeWhitespace(~, str)
            %NORMALIZEWHITESPACE Normalize whitespace to single spaces
            %   RESULT = NORMALIZEWHITESPACE(STR) collapses multiple spaces.
            %
            %   Example:
            %       s.normalizeWhitespace('hello    world')  % Returns: 'hello world'

            str = char(str);
            result = regexprep(strtrim(str), '\s+', ' ');
        end

        function result = escapeRegex(~, str)
            %ESCAPEREGEX Escape special regex characters
            %   RESULT = ESCAPEREGEX(STR) escapes regex metacharacters.
            %
            %   Example:
            %       s.escapeRegex('a.b*c')  % Returns: 'a\.b\*c'

            str = char(str);
            special = '\.^$*+?()[]{}|';
            result = str;
            for i = 1:length(special)
                result = strrep(result, special(i), ['\', special(i)]);
            end
        end

        function result = ellipsize(~, str, maxLength, ellipse)
            %ELLIPSIZE Truncate with ellipsis character
            %   RESULT = ELLIPSIZE(STR, MAXLENGTH, ELLIPSE) truncates nicely.
            %
            %   Inputs:
            %       str       - Input string
            %       maxLength - Maximum length
            %       ellipse   - Ellipsis string (default: '...')
            %
            %   Example:
            %       s.ellipsize('Hello World', 8)  % Returns: 'Hello...'

            if nargin < 4
                ellipse = '...';
            end
            str = char(str);
            
            if length(str) <= maxLength
                result = str;
                return;
            end
            
            result = [str(1:maxLength-length(ellipse)), ellipse];
        end

        function result = wordWrap(~, str, width)
            %WORDWRAP Wrap text at specified width
            %   RESULT = WORDWRAP(STR, WIDTH) wraps text at width characters.
            %
            %   Example:
            %       s.wordWrap('Hello beautiful world', 10)
            %       % Returns: 'Hello\nbeautiful\nworld'

            str = char(str);
            words = strsplit(str);
            result = '';
            currentLine = '';
            
            for i = 1:length(words)
                word = words{i};
                if isempty(currentLine)
                    if length(word) > width
                        % Word is longer than width, need to break it
                        while length(word) > width
                            if ~isempty(result)
                                result = [result, sprintf('\n')];
                            end
                            result = [result, word(1:width)];
                            word = word(width+1:end);
                        end
                        if ~isempty(word)
                            currentLine = word;
                        end
                    else
                        currentLine = word;
                    end
                elseif length(currentLine) + 1 + length(word) <= width
                    currentLine = [currentLine, ' ', word];
                else
                    if ~isempty(result)
                        result = [result, sprintf('\n')];
                    end
                    result = [result, currentLine];
                    currentLine = word;
                end
            end
            
            if ~isempty(currentLine)
                if ~isempty(result)
                    result = [result, sprintf('\n')];
                end
                result = [result, currentLine];
            end
        end

        function result = between(~, str, startDelim, endDelim)
            %BETWEEN Extract substring between delimiters
            %   RESULT = BETWEEN(STR, STARTDELIM, ENDDELIM) extracts content.
            %
            %   Example:
            %       s.between('Hello [world]!', '[', ']')  % Returns: 'world'

            str = char(str);
            startIdx = strfind(str, startDelim);
            if isempty(startIdx)
                result = '';
                return;
            end
            startIdx = startIdx(1) + length(startDelim);
            
            endIdx = strfind(str(startIdx:end), endDelim);
            if isempty(endIdx)
                result = '';
                return;
            end
            endIdx = startIdx + endIdx(1) - 2;
            
            result = str(startIdx:endIdx);
        end

        function result = afterFirst(~, str, delimiter)
            %AFTERFIRST Get substring after first occurrence
            %   RESULT = AFTERFIRST(STR, DELIMITER) returns text after delimiter.
            %
            %   Example:
            %       s.afterFirst('a/b/c', '/')  % Returns: 'b/c'

            str = char(str);
            delimiter = char(delimiter);
            idx = strfind(str, delimiter);
            if isempty(idx)
                result = '';
                return;
            end
            result = str(idx(1) + length(delimiter):end);
        end

        function result = afterLast(~, str, delimiter)
            %AFTERLAST Get substring after last occurrence
            %   RESULT = AFTERLAST(STR, DELIMITER) returns text after last delimiter.
            %
            %   Example:
            %       s.afterLast('a/b/c', '/')  % Returns: 'c'

            str = char(str);
            delimiter = char(delimiter);
            idx = strfind(str, delimiter);
            if isempty(idx)
                result = '';
                return;
            end
            result = str(idx(end) + length(delimiter):end);
        end

        function result = beforeFirst(~, str, delimiter)
            %BEFOREFIRST Get substring before first occurrence
            %   RESULT = BEFOREFIRST(STR, DELIMITER) returns text before delimiter.
            %
            %   Example:
            %       s.beforeFirst('a/b/c', '/')  % Returns: 'a'

            str = char(str);
            delimiter = char(delimiter);
            idx = strfind(str, delimiter);
            if isempty(idx)
                result = str;
                return;
            end
            result = str(1:idx(1)-1);
        end

        function result = beforeLast(~, str, delimiter)
            %BEFORELAST Get substring before last occurrence
            %   RESULT = BEFORELAST(STR, DELIMITER) returns text before last delimiter.
            %
            %   Example:
            %       s.beforeLast('a/b/c', '/')  % Returns: 'a/b'

            str = char(str);
            delimiter = char(delimiter);
            idx = strfind(str, delimiter);
            if isempty(idx)
                result = str;
                return;
            end
            result = str(1:idx(end)-1);
        end

        function result = surround(~, str, wrapper)
            %SURROUND Wrap string with prefix and suffix
            %   RESULT = SURROUND(STR, WRAPPER) wraps with same string on both sides.
            %
            %   Example:
            %       s.surround('hello', '**')  % Returns: '**hello**'

            str = char(str);
            wrapper = char(wrapper);
            result = [wrapper, str, wrapper];
        end

        function result = quote(~, str)
            %QUOTE Wrap string in double quotes
            %   RESULT = QUOTE(STR) wraps string in quotes.
            %
            %   Example:
            %       s.quote('hello')  % Returns: '"hello"'

            result = ['"', char(str), '"'];
        end

        function result = singleQuote(~, str)
            %SINGLEQUOTE Wrap string in single quotes
            %   RESULT = SINGLEQUOTE(STR) wraps string in single quotes.
            %
            %   Example:
            %       s.singleQuote('hello')  % Returns: '''hello'''

            result = ['''', char(str), ''''];
        end

        function result = unquote(~, str)
            %UNQUOTE Remove surrounding quotes
            %   RESULT = UNQUOTE(STR) removes surrounding quotes.
            %
            %   Example:
            %       s.unquote('"hello"')  % Returns: 'hello'
            %       s.unquote('''hello''')  % Returns: 'hello'

            str = char(str);
            if isempty(str)
                result = '';
                return;
            end
            
            if (str(1) == '"' && str(end) == '"') || ...
               (str(1) == '''' && str(end) == '''')
                result = str(2:end-1);
            else
                result = str;
            end
        end
    end

    methods (Static)
        function result = quickTrim(str)
            %QUICKTRIM Static method for trim
            %   RESULT = QUICKTRIM(STR) trims whitespace.

            utils = string_utils.mod();
            result = utils.trim(str);
        end

        function result = quickSlugify(str)
            %QUICKSLUGIFY Static method for slugify
            %   RESULT = QUICKSLUGIFY(STR) creates URL slug.

            utils = string_utils.mod();
            result = utils.slugify(str);
        end

        function result = quickCamelCase(str)
            %QUICKCAMELCASE Static method for camelCase conversion
            %   RESULT = QUICKCAMELCASE(STR) converts to camelCase.

            utils = string_utils.mod();
            result = utils.toCamelCase(str);
        end

        function result = quickFormat(template, varargin)
            %QUICKFORMAT Static method for format
            %   RESULT = QUICKFORMAT(TEMPLATE, ...) formats string.

            utils = string_utils.mod();
            result = utils.format(template, varargin{:});
        end
    end
end