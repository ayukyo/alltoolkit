classdef mod < handle
    %JSON_UTILS JSON parsing and generation utilities for MATLAB
    %   A zero-dependency JSON parser and generator for MATLAB.
    %   Supports parsing JSON strings to MATLAB structures/cell arrays,
    %   and generating JSON strings from MATLAB data types.
    %
    %   Features:
    %   - Parse JSON strings to MATLAB data structures
    %   - Generate JSON strings from MATLAB variables
    %   - Pretty print JSON with customizable indentation
    %   - Validate JSON syntax
    %   - Support for null, boolean, number, string, array, object types
    %   - Handle nested structures and arrays
    %   - Unicode escape sequence support (\uXXXX)
    %   - Type-safe access with default values
    %
    %   Example:
    %       utils = json_utils.mod();
    %       data = utils.parse('{"name": "John", "age": 30}');
    %       disp(data.name);  % "John"
    %       json = utils.encode(struct('x', 1, 'y', 2));
    %       disp(json);  % '{"x":1,"y":2}'
    %
    %   Author: AllToolkit
    %   Version: 1.0.0
    %   License: MIT

    properties (Access = private)
        % Parser state
        jsonStr
        pos
        len
    end

    methods
        function obj = mod()
            %MOD Constructor for JSON utilities
            %   Creates a new JSON utilities instance.
            %
            %   Example:
            %       utils = json_utils.mod();
        end

        %% Parsing Methods

        function result = parse(obj, jsonString)
            %PARSE Parse a JSON string into MATLAB data structure
            %   DATA = PARSE(JSONSTRING) parses the JSON string and returns
            %   the corresponding MATLAB data structure.
            %
            %   Input:
            %       jsonString - A string containing valid JSON
            %
            %   Output:
            %       result - Parsed data (struct, cell array, or primitive)
            %
            %   Example:
            %       utils = json_utils.mod();
            %       data = utils.parse('{"name": "test", "value": 123}');
            %       % Returns: struct with name='test', value=123
            %
            %   Throws:
            %       Error if JSON is invalid or malformed

            if ~ischar(jsonString) && ~isstring(jsonString)
                error('JSON:InvalidInput', 'Input must be a string');
            end

            obj.jsonStr = char(jsonString);
            obj.pos = 1;
            obj.len = length(obj.jsonStr);

            obj.skipWhitespace();
            result = obj.parseValue();
            obj.skipWhitespace();

            if obj.pos <= obj.len
                error('JSON:TrailingData', 'Unexpected data after JSON value at position %d', obj.pos);
            end
        end

        function result = parseOrNull(obj, jsonString)
            %PARSEORNULL Safely parse JSON, return empty on error
            %   DATA = PARSEORNULL(JSONSTRING) parses the JSON string and
            %   returns the data, or empty [] if parsing fails.
            %
            %   Input:
            %       jsonString - A string containing JSON
            %
            %   Output:
            %       result - Parsed data, or [] if invalid
            %
            %   Example:
            %       data = utils.parseOrNull('invalid');  % Returns []
            %       data = utils.parseOrNull('"valid"');  % Returns "valid"

            try
                result = obj.parse(jsonString);
            catch
                result = [];
            end
        end

        function result = parseFile(obj, filename)
            %PARSEFILE Parse JSON from a file
            %   DATA = PARSEFILE(FILENAME) reads the file and parses its
            %   contents as JSON.
            %
            %   Input:
            %       filename - Path to the JSON file
            %
            %   Output:
            %       result - Parsed data
            %
            %   Example:
            %       config = utils.parseFile('config.json');

            fid = fopen(filename, 'r', 'n', 'UTF-8');
            if fid == -1
                error('JSON:FileError', 'Cannot open file: %s', filename);
            end

            try
                content = fread(fid, '*char')';
                fclose(fid);
                result = obj.parse(content);
            catch ME
                fclose(fid);
                rethrow(ME);
            end
        end

        %% Encoding Methods

        function json = encode(obj, data)
            %ENCODE Encode MATLAB data to JSON string
            %   JSON = ENCODE(DATA) converts MATLAB data to a compact
            %   JSON string.
            %
            %   Input:
            %       data - MATLAB data (struct, cell, array, string, etc.)
            %
            %   Output:
            %       json - JSON string representation
            %
            %   Example:
            %       json = utils.encode(struct('x', 1, 'y', 2));
            %       % Returns: '{"x":1,"y":2}'

            json = obj.encodeValue(data, false);
        end

        function json = encodePretty(obj, data, indent)
            %ENCODEPRETTY Encode MATLAB data to pretty-printed JSON
            %   JSON = ENCODEPRETTY(DATA, INDENT) converts MATLAB data to
            %   a formatted JSON string with indentation.
            %
            %   Inputs:
            %       data   - MATLAB data to encode
            %       indent - Indentation string (default: '  ')
            %
            %   Output:
            %       json - Pretty-printed JSON string
            %
            %   Example:
            %       json = utils.encodePretty(struct('a', 1));
            %       % Returns: '{\n  "a": 1\n}'

            if nargin < 3
                indent = '  ';
            end
            json = obj.encodeValue(data, true, indent, 0);
        end

        %% Validation Methods

        function valid = isValid(obj, jsonString)
            %ISVALID Check if a string is valid JSON
            %   VALID = ISVALID(JSONSTRING) returns true if the string
            %   contains valid JSON, false otherwise.
            %
            %   Input:
            %       jsonString - String to validate
            %
            %   Output:
            %       valid - true if valid JSON, false otherwise
            %
            %   Example:
            %       if utils.isValid(jsonStr)
            %           data = utils.parse(jsonStr);
            %       end

            valid = ~isempty(obj.parseOrNull(jsonString));
        end

        function valid = isValidFile(obj, filename)
            %ISVALIDFILE Check if a file contains valid JSON
            %   VALID = ISVALIDFILE(FILENAME) returns true if the file
            %   exists and contains valid JSON.
            %
            %   Input:
            %       filename - Path to file
            %
            %   Output:
            %       valid - true if valid JSON file

            if ~exist(filename, 'file')
                valid = false;
                return;
            end
            try
                obj.parseFile(filename);
                valid = true;
            catch
                valid = false;
            end
        end

        %% Utility Methods

        function save(obj, filename, data, pretty)
            %SAVE Save data to a JSON file
            %   SAVE(FILENAME, DATA, PRETTY) writes data to a file as JSON.
            %
            %   Inputs:
            %       filename - Output file path
            %       data     - Data to save
            %       pretty   - If true, use pretty printing (default: false)
            %
            %   Example:
            %       utils.save('output.json', data, true);

            if nargin < 4
                pretty = false;
            end

            if pretty
                json = obj.encodePretty(data);
            else
                json = obj.encode(data);
            end

            fid = fopen(filename, 'w', 'n', 'UTF-8');
            if fid == -1
                error('JSON:FileError', 'Cannot create file: %s', filename);
            end

            fwrite(fid, json, 'char');
            fclose(fid);
        end

        function result = get(obj, data, key, defaultValue)
            %GET Safely get a value from parsed JSON with default
            %   VALUE = GET(DATA, KEY, DEFAULT) returns the value for KEY
            %   from DATA, or DEFAULT if KEY doesn't exist.
            %
            %   Inputs:
            %       data         - Parsed JSON data (struct)
            %       key          - Field name to access
            %       defaultValue - Value to return if key not found
            %
            %   Output:
            %       result - Value or default
            %
            %   Example:
            %       data = utils.parse('{"name": "test"}');
            %       name = utils.get(data, 'name', 'unknown');  % "test"
            %       age = utils.get(data, 'age', 0);            % 0

            if isstruct(data) && isfield(data, key)
                result = data.(key);
            else
                if nargin < 4
                    result = [];
                else
                    result = defaultValue;
                end
            end
        end

        function result = getPath(obj, data, path, defaultValue)
            %GETPATH Get a nested value using dot-notation path
            %   VALUE = GETPATH(DATA, PATH, DEFAULT) navigates through
            %   nested structures using dot notation.
            %
            %   Inputs:
            %       data         - Parsed JSON data
            %       path         - Dot-separated path (e.g., 'user.address.city')
            %       defaultValue - Value to return if path not found
            %
            %   Output:
            %       result - Value at path or default
            %
            %   Example:
            %       data = utils.parse('{\n            %         "user": {\n            %           "address": {\n            %             "city": "Beijing"\n            %           }\n            %         }\n            %       }');
            %       city = utils.getPath(data, 'user.address.city', 'Unknown');
            %       % Returns: "Beijing"

            parts = strsplit(path, '.');
            result = data;

            for i = 1:length(parts)
                if isstruct(result) && isfield(result, parts{i})
                    result = result.(parts{i});
                elseif iscell(result) && isnumeric(str2double(parts{i}))
                    idx = str2double(parts{i});
                    if idx > 0 && idx <= length(result)
                        result = result{idx};
                    else
                        if nargin < 4
                            result = [];
                        else
                            result = defaultValue;
                        end
                        return;
                    end
                else
                    if nargin < 4
                        result = [];
                    else
                        result = defaultValue;
                    end
                    return;
                end
            end
        end

        function result = minify(obj, jsonString)
            %MINIFY Remove all unnecessary whitespace from JSON
            %   MINIFIED = MINIFY(JSONSTRING) returns a compact version
            %   of the JSON string with all non-essential whitespace removed.
            %
            %   Input:
            %       jsonString - JSON string to minify
            %
            %   Output:
            %       result - Minified JSON string
            %
            %   Example:
            %       minified = utils.minify('{ "a": 1, \n  "b": 2 }');
            %       % Returns: '{"a":1,"b":2}'

            data = obj.parse(jsonString);
            result = obj.encode(data);
        end
    end

    methods (Access = private)
        %% Parser Implementation

        function skipWhitespace(obj)
            while obj.pos <= obj.len
                c = obj.jsonStr(obj.pos);
                if c == ' ' || c == '\t' || c == '\n' || c == '\r'
                    obj.pos = obj.pos + 1;
                else
                    break;
                end
            end
        end

        function value = parseValue(obj)
            obj.skipWhitespace();

            if obj.pos > obj.len
                error('JSON:UnexpectedEnd', 'Unexpected end of JSON');
            end

            c = obj.jsonStr(obj.pos);

            switch c
                case '{'
                    value = obj.parseObject();
                case '['
                    value = obj.parseArray();
                case '"'
                    value = obj.parseString();
                case 't'
                    value = obj.parseLiteral('true', true);
                case 'f'
                    value = obj.parseLiteral('false', false);
                case 'n'
                    value = obj.parseLiteral('null', []);
                otherwise
                    if c == '-' || (c >= '0' && c <= '9')
                        value = obj.parseNumber();
                    else
                        error('JSON:UnexpectedChar', 'Unexpected character ''%s'' at position %d', c, obj.pos);
                    end
            end
        end

        function obj_struct = parseObject(obj)
            obj.expectChar('{');
            obj_struct = struct();

            obj.skipWhitespace();
            if obj.peekChar() == '}'
                obj.pos = obj.pos + 1;
                return;
            end

            while true
                obj.skipWhitespace();
                key = obj.parseString();

                obj.skipWhitespace();
                obj.expectChar(':');

                value = obj.parseValue();

                % Sanitize key for MATLAB field name
                safeKey = obj.makeValidFieldName(key);
                obj_struct.(safeKey) = value;

                obj.skipWhitespace();
                c = obj.jsonStr(obj.pos);
                obj.pos = obj.pos + 1;

                if c == '}'
                    break;
                elseif c ~= ','
                    error('JSON:ExpectedComma', 'Expected '','' or ''}'' at position %d', obj.pos - 1);
                end
            end
        end

        function arr = parseArray(obj)
            obj.expectChar('[');
            arr = {};

            obj.skipWhitespace();
            if obj.peekChar() == ']'
                obj.pos = obj.pos + 1;
                return;
            end

            while true
                value = obj.parseValue();
                arr{end + 1} = value;  %#ok<AGROW>

                obj.skipWhitespace();
                c = obj.jsonStr(obj.pos);
                obj.pos = obj.pos + 1;

                if c == ']'
                    break;
                elseif c ~= ','
                    error('JSON:ExpectedComma', 'Expected '','' or '']'' at position %d', obj.pos - 1);
                end
            end
        end

        function str = parseString(obj)
            obj.expectChar('"');
            startPos = obj.pos;

            while obj.pos <= obj.len
                c = obj.jsonStr(obj.pos);

                if c == '"'
                    str = obj.jsonStr(startPos:obj.pos - 1);
                    obj.pos = obj.pos + 1;
                    str = obj.unescapeString(str);
                    return;
                elseif c == '\\'
                    obj.pos = obj.pos + 2;
                elseif c < 32
                    error('JSON:ControlChar', 'Control character in string at position %d', obj.pos);
                else
                    obj.pos = obj.pos + 1;
                end
            end

            error('JSON:UnterminatedString', 'Unterminated string starting at position %d', startPos - 1);
        end

        function num = parseNumber(obj)
            startPos = obj.pos;

            % Optional minus
            if obj.jsonStr(obj.pos) == '-'
                obj.pos = obj.pos + 1;
            end

            % Integer part
            if obj.pos > obj.len
                error('JSON:InvalidNumber', 'Invalid number at position %d', startPos);
            end

            c = obj.jsonStr(obj.pos);
            if c == '0'
                obj.pos = obj.pos + 1;
            elseif c >= '1' && c <= '9'
                obj.pos = obj.pos + 1;
                while obj.pos <= obj.len
                    c = obj.jsonStr(obj.pos);
                    if c >= '0' && c <= '9'
                        obj.pos = obj.pos + 1;
                    else
                        break;
                    end
                end
            else
                error('JSON:InvalidNumber', 'Invalid number at position %d', startPos);
            end

            % Fractional part
            if obj.pos <= obj.len && obj.jsonStr(obj.pos) == '.'
                obj.pos = obj.pos + 1;
                fracStart = obj.pos;
                while obj.pos <= obj.len
                    c = obj.jsonStr(obj.pos);
                    if c >= '0' && c <= '9'
                        obj.pos = obj.pos + 1;
                    else
                        break;
                    end
                end
                if obj.pos == fracStart
                    error('JSON:InvalidNumber', 'Invalid number at position %d', startPos);
                end
            end

            % Exponent part
            if obj.pos <= obj.len
                c = obj.jsonStr(obj.pos);
                if c == 'e' || c == 'E'
                    obj.pos = obj.pos + 1;
                    if obj.pos <= obj.len
                        c = obj.jsonStr(obj.pos);
                        if c == '+' || c == '-'
                            obj.pos = obj.pos + 1;
                        end
                    end
                    expStart = obj.pos;
                    while obj.pos <= obj.len
                        c = obj.jsonStr(obj.pos);
                        if c >= '0' && c <= '9'
                            obj.pos = obj.pos + 1;
                        else
                            break;
                        end
                    end
                    if obj.pos == expStart
                        error('JSON:InvalidNumber', 'Invalid number at position %d', startPos);
                    end
                end
            end

            numStr = obj.jsonStr(startPos:obj.pos - 1);
            num = str2double(numStr);

            % Convert to integer if it's a whole number
            if num == floor(num) && abs(num) < 2^53
                num = int64(num);
            end
        end

        function value = parseLiteral(obj, literal, returnValue)
            endPos = obj.pos + length(literal) - 1;
            if endPos > obj.len || ~strcmpi(obj.jsonStr(obj.pos:endPos), literal)
                error('JSON:InvalidLiteral', 'Expected ''%s'' at position %d', literal, obj.pos);
            end
            obj.pos = endPos + 1;
            value = returnValue;
        end

        function expectChar(obj, expected)
            if obj.pos > obj.len || obj.jsonStr(obj.pos) ~= expected
                error('JSON:ExpectedChar', 'Expected ''%s'' at position %d', expected, obj.pos);
            end
            obj.pos = obj.pos + 1;
        end

        function c = peekChar(obj)
            if obj.pos <= obj.len
                c = obj.jsonStr(obj.pos);
            else
                c = char(0);
            end
        end

        function str = unescapeString(~, str)
            % Handle escape sequences
            str = strrep(str, '\\', '\');
            str = strrep(str, '\"', '"');
            str = strrep(str, '\/', '/');
            str = strrep(str, '\b', sprintf('\b'));
            str = strrep(str, '\f', sprintf('\f'));
            str = strrep(str, '\n', sprintf('\n'));
            str = strrep(str, '\r', sprintf('\r'));
            str = strrep(str, '\t', sprintf('\t'));

            % Handle \uXXXX sequences
            idx = 1;
            while idx <= length(str) - 5
                if str(idx) == '\' && str(idx + 1) == 'u'
                    hexStr = str(idx + 2:idx + 5);
                    try
                        codePoint = hex2dec(hexStr);
                        if codePoint < 128
                            replacement = char(codePoint);
                        else
                            % For non-ASCII, keep as is for now
                            replacement = native2unicode(codePoint, 'UTF-8');
                        end
                        str = [str(1:idx - 1), replacement, str(idx + 6:end)];  %#ok<AGROW>
                        idx = idx + 1;
                    catch
                        idx = idx + 1;
                    end
                else
                    idx = idx + 1;
                end
            end
        end

        function name = makeValidFieldName(~, name)
            % Convert JSON key to valid MATLAB field name
            % Replace invalid characters with underscores

            if isempty(name)
                name = 'x';
                return;
            end

            % Check if it starts with a letter
            if ~isletter(name(1))
                name = ['f', name];
            end

            % Replace invalid characters
            for i = 2:length(name)
                if ~isletter(name(i)) && ~isstrprop(name(i), 'digit') && name(i) ~= '_'
                    name(i) = '_';
                end
            end

            % Handle MATLAB reserved words
            reserved = {'case', 'catch', 'classdef', 'continue', 'else', 'elseif', ...
                        'end', 'for', 'function', 'global', 'if', 'otherwise', ...
                        'parfor', 'persistent', 'return', 'spmd', 'switch', ...
                        'try', 'while'};

            if ismember(name, reserved)
                name = [name, '_'];
            end
        end

        %% Encoder Implementation

        function json = encodeValue(obj, value, pretty, indent, depth)
            if nargin < 5
                depth = 0;
            end

            if isstruct(value)
                json = obj.encodeStruct(value, pretty, indent, depth);
            elseif iscell(value)
                json = obj.encodeCell(value, pretty, indent, depth);
            elseif ischar(value) || isstring(value)
                json = obj.encodeString(char(value));
            elseif isnumeric(value)
                if isempty(value)
                    json = '[]';
                elseif numel(value) == 1
                    if isinf(value)
                        if value > 0
                            json = 'Infinity';
                        else
                            json = '-Infinity';
                        end
                    elseif isnan(value)
                        json = 'NaN';
                    else
                        json = num2str(value, 17);
                    end
                else
                    % Array - encode as nested array
                    json = obj.encodeNumericArray(value, pretty, indent, depth);
                end
            elseif islogical(value)
                if value
                    json = 'true';
                else
                    json = 'false';
                end
            elseif isempty(value)
                json = 'null';
            else
                json = 'null';
            end
        end

        function json = encodeStruct(obj, s, pretty, indent, depth)
            fields = fieldnames(s);

            if isempty(fields)
                json = '{}';
                return;
            end

            if pretty
                innerIndent = repmat(indent, 1, depth + 1);
                lineEnd = sprintf('\n');
                separator = ',';
            else
                innerIndent = '';
                lineEnd = '';
                separator = ',';
            end

            parts = {};
            for i = 1:length(fields)
                key = fields{i};
                val = s.(key);

                if pretty
                    parts{end + 1} = sprintf('%s"%s": %s', innerIndent, key, ...
                        obj.encodeValue(val, pretty, indent, depth + 1));  %#ok<AGROW>
                else
                    parts{end + 1} = sprintf('"%s":%s', key, ...
                        obj.encodeValue(val, pretty, indent, depth + 1));  %#ok<AGROW>
                end
            end

            if pretty
                outerIndent = repmat(indent, 1, depth);
                json = ['{', lineEnd, strjoin(parts, [separator, lineEnd]), lineEnd, outerIndent, '}'];
            else
                json = ['{', strjoin(parts, separator), '}'];
            end
        end

        function json = encodeCell(obj, c, pretty, indent, depth)
            if isempty(c)
                json = '[]';
                return;
            end

            if pretty
                innerIndent = repmat(indent, 1, depth + 1);
                lineEnd = sprintf('\n');
                separator = ',';
            else
                innerIndent = '';
                lineEnd = '';
                separator = ',';
            end

            parts = {};
            for i = 1:length(c)
                parts{end + 1} = [innerIndent, obj.encodeValue(c{i}, pretty, indent, depth + 1)];  %#ok<AGROW>
            end

            if pretty
                outerIndent = repmat(indent, 1, depth);
                json = ['[', lineEnd, strjoin(parts, [separator, lineEnd]), lineEnd, outerIndent, ']'];
            else
                json = ['[', strjoin(parts, separator), ']'];
            end
        end

        function json = encodeNumericArray(obj, arr, pretty, indent, depth)
            sz = size(arr);

            if length(sz) == 2 && (sz(1) == 1 || sz(2) == 1)
                % 1D array
                parts = cell(length(arr), 1);
                for i = 1:length(arr)
                    parts{i} = obj.encodeValue(arr(i), false, '', 0);
                end
                json = ['[', strjoin(parts, ','), ']'];
            else
                % 2D array - encode as array of arrays
                parts = {};
                for i = 1:sz(1)
                    rowParts = cell(sz(2), 1);
                    for j = 1:sz(2)
                        rowParts{j} = obj.encodeValue(arr(i, j), false, '', 0);
                    end
                    parts{end + 1} = ['[', strjoin(rowParts, ','), ']'];  %#ok<AGROW>
                end
                json = ['[', strjoin(parts, ','), ']'];
            end
        end

        function json = encodeString(~, str)
            % Escape special characters
            str = strrep(str, '\', '\\');
            str = strrep(str, '"', '\"');
            str = strrep(str, sprintf('\b'), '\b');
            str = strrep(str, sprintf('\f'), '\f');
            str = strrep(str, sprintf('\n'), '\n');
            str = strrep(str, sprintf('\r'), '\r');
            str = strrep(str, sprintf('\t'), '\t');

            json = ['"', str, '"'];
        end
    end

    methods (Static)
        function result = quickParse(jsonString)
            %QUICKPARSE Static method to parse JSON without creating instance
            %   DATA = QUICKPARSE(JSONSTRING) parses JSON string directly.
            %
            %   Example:
            %       data = json_utils.mod.quickParse('{"x": 1}');

            utils = json_utils.mod();
            result = utils.parse(jsonString);
        end

        function json = quickEncode(data, pretty)
            %QUICKENCODE Static method to encode data without creating instance
            %   JSON = QUICKENCODE(DATA, PRETTY) encodes data to JSON.
            %
            %   Example:
            %       json = json_utils.mod.quickEncode(struct('x', 1));

            if nargin < 2
                pretty = false;
            end
            utils = json_utils.mod();
            if pretty
                json = utils.encodePretty(data);
            else
                json = utils.encode(data);
            end
        end
    end
end
