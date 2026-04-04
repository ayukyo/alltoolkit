%% JSON Utilities Example
%  Demonstrates the usage of JSON parsing and generation utilities
%  for MATLAB.
%
%  Run this script in MATLAB to see examples of:
%  - Parsing JSON strings
%  - Generating JSON from MATLAB data
%  - Working with nested structures
%  - File I/O operations
%  - Utility functions
%
%  Usage:
%      run('json_utils_example.m')

fprintf('========================================\n');
fprintf('  JSON Utilities Examples\n');
fprintf('========================================\n\n');

%% Initialize
utils = json_utils.mod();

%% Example 1: Parse a simple JSON object
fprintf('Example 1: Parse Simple JSON Object\n');
fprintf('------------------------------------\n');

jsonStr = '{"name": "John Doe", "age": 30, "city": "New York"}';
fprintf('Input: %s\n\n', jsonStr);

data = utils.parse(jsonStr);
fprintf('Parsed data:\n');
fprintf('  name: %s\n', data.name);
fprintf('  age: %d\n', data.age);
fprintf('  city: %s\n\n', data.city);

%% Example 2: Parse a nested JSON object
fprintf('Example 2: Parse Nested JSON Object\n');
fprintf('------------------------------------\n');

jsonStr = ['{\n', ...
           '  "user": {\n', ...
           '    "id": 12345,\n', ...
           '    "profile": {\n', ...
           '      "name": "Alice",\n', ...
           '      "email": "alice@example.com"\n', ...
           '    },\n', ...
           '    "roles": ["admin", "editor"]\n', ...
           '  }\n', ...
           '}'];
fprintf('Input:\n%s\n\n', jsonStr);

data = utils.parse(jsonStr);
fprintf('Accessing nested data:\n');
fprintf('  user.id: %d\n', data.user.id);
fprintf('  user.profile.name: %s\n', data.user.profile.name);
fprintf('  user.profile.email: %s\n', data.user.profile.email);
fprintf('  user.roles{1}: %s\n\n', data.user.roles{1});

%% Example 3: Parse JSON arrays
fprintf('Example 3: Parse JSON Arrays\n');
fprintf('------------------------------------\n');

% Array of numbers
jsonStr = '[1, 2, 3, 4, 5]';
numbers = utils.parse(jsonStr);
fprintf('Numbers array: ');
for i = 1:length(numbers)
    fprintf('%d ', numbers{i});
end
fprintf('\n');

% Array of strings
jsonStr = '["apple", "banana", "cherry"]';
fruits = utils.parse(jsonStr);
fprintf('Fruits array: ');
for i = 1:length(fruits)
    fprintf('%s ', fruits{i});
end
fprintf('\n\n');

%% Example 4: Parse special values
fprintf('Example 4: Parse Special Values\n');
fprintf('------------------------------------\n');

jsonStr = '{"active": true, "deleted": false, "data": null, "count": 0}';
data = utils.parse(jsonStr);
fprintf('active (boolean): %d\n', data.active);
fprintf('deleted (boolean): %d\n', data.deleted);
fprintf('data (null): %s\n', mat2str(data.data));
fprintf('count (zero): %d\n\n', data.count);

%% Example 5: Encode MATLAB struct to JSON
fprintf('Example 5: Encode Struct to JSON\n');
fprintf('------------------------------------\n');

person = struct();
person.name = 'Bob';
person.age = 25;
person.hobbies = {{'reading', 'gaming', 'coding'}};

json = utils.encode(person);
fprintf('Compact JSON:\n%s\n\n', json);

prettyJson = utils.encodePretty(person);
fprintf('Pretty JSON:\n%s\n\n', prettyJson);

%% Example 6: Encode cell array to JSON
fprintf('Example 6: Encode Cell Array to JSON\n');
fprintf('------------------------------------\n');

mixedArray = {42, 'hello', true, struct('x', 1, 'y', 2)};
json = utils.encode(mixedArray);
fprintf('Mixed array as JSON:\n%s\n\n', json);

%% Example 7: Round-trip (parse then encode)
fprintf('Example 7: Round-trip Test\n');
fprintf('------------------------------------\n');

original = struct();
original.product = 'Laptop';
original.price = 999.99;
original.inStock = true;
original.specs = struct();
original.specs.cpu = 'Intel i7';
original.specs.ram = '16GB';

json = utils.encode(original);
fprintf('Original encoded:\n%s\n\n', json);

restored = utils.parse(json);
fprintf('Restored data:\n');
fprintf('  product: %s\n', restored.product);
fprintf('  price: %.2f\n', restored.price);
fprintf('  inStock: %d\n', restored.inStock);
fprintf('  specs.cpu: %s\n', restored.specs.cpu);
fprintf('  specs.ram: %s\n\n', restored.specs.ram);

%% Example 8: Using get with default values
fprintf('Example 8: Safe Access with Defaults\n');
fprintf('------------------------------------\n');

config = utils.parse('{"host": "localhost", "port": 8080}');

% Existing key
host = utils.get(config, 'host', '127.0.0.1');
fprintf('host (exists): %s\n', host);

% Missing key with default
timeout = utils.get(config, 'timeout', 30);
fprintf('timeout (default): %d\n\n', timeout);

%% Example 9: Using getPath for nested access
fprintf('Example 9: Nested Path Access\n');
fprintf('------------------------------------\n');

jsonStr = ['{\n', ...
           '  "database": {\n', ...
           '    "connection": {\n', ...
           '      "host": "db.example.com",\n', ...
           '      "port": 5432\n', ...
           '    }\n', ...
           '  }\n', ...
           '}'];

data = utils.parse(jsonStr);

% Access nested value
host = utils.getPath(data, 'database.connection.host', 'localhost');
port = utils.getPath(data, 'database.connection.port', 3306);
missing = utils.getPath(data, 'database.connection.ssl', false);

fprintf('database.connection.host: %s\n', host);
fprintf('database.connection.port: %d\n', port);
fprintf('database.connection.ssl (default): %d\n\n', missing);

%% Example 10: Validation
fprintf('Example 10: JSON Validation\n');
fprintf('------------------------------------\n');

validJson = '{"valid": true}';
invalidJson = 'this is not json';

fprintf('Is ''%s'' valid? %d\n', validJson, utils.isValid(validJson));
fprintf('Is ''%s'' valid? %d\n\n', invalidJson, utils.isValid(invalidJson));

%% Example 11: Safe parsing with parseOrNull
fprintf('Example 11: Safe Parsing\n');
fprintf('------------------------------------\n');

% This will succeed
data = utils.parseOrNull('{"success": true}');
if ~isempty(data)
    fprintf('Parsed successfully: success=%d\n', data.success);
end

% This will return empty without throwing
data = utils.parseOrNull('not valid json');
if isempty(data)
    fprintf('Invalid JSON handled gracefully\n');
end
fprintf('\n');

%% Example 12: Minify JSON
fprintf('Example 12: Minify JSON\n');
fprintf('------------------------------------\n');

prettyJson = ['{\n', ...
              '  "name": "Test",\n', ...
              '  "items": [\n', ...
              '    1,\n', ...
              '    2,\n', ...
              '    3\n', ...
              '  ]\n', ...
              '}'];

minified = utils.minify(prettyJson);
fprintf('Before:\n%s\n\n', prettyJson);
fprintf('After minification:\n%s\n\n', minified);

%% Example 13: Static methods
fprintf('Example 13: Static Quick Methods\n');
fprintf('------------------------------------\n');

% Quick parse without creating instance
data = json_utils.mod.quickParse('{"quick": "parse"}');
fprintf('quickParse result: %s\n', data.quick);

% Quick encode without creating instance
json = json_utils.mod.quickEncode(struct('quick', 'encode'), true);
fprintf('quickEncode result:\n%s\n\n', json);

%% Summary
fprintf('========================================\n');
fprintf('  Examples completed!\n');
fprintf('========================================\n');
