classdef mod < handle
    % HTTP_UTILS - HTTP Client Utilities for MATLAB
    %
    % A comprehensive HTTP client utility providing HTTP methods, URL manipulation,
    % query string handling, and response processing with zero dependencies.
    %
    % Uses only MATLAB built-in functions (webread, webwrite, weboptions, urlencode, urldecode)
    %
    % Example:
    %   % GET request
    %   response = http_utils.get('https://api.example.com/users');
    %   disp(response.body);
    %
    %   % POST JSON
    %   data = struct('name', 'John', 'age', 30);
    %   response = http_utils.post_json('https://api.example.com/users', data);
    %
    %   % URL manipulation
    %   url = http_utils.build_url('https://api.example.com/search', struct('q', 'hello', 'page', 1));
    %
    % Author: AllToolkit
    % Version: 1.0.0

    methods (Static = true)
        %% HTTP Methods

        function response = get(url, options)
            %GET Send HTTP GET request
            %   response = http_utils.get(url) sends GET request to URL
            %   response = http_utils.get(url, options) with custom options
            %
            %   Options struct fields:
            %       headers     - Struct with header key-value pairs
            %       timeout     - Timeout in seconds (default: 30)
            %       username    - Username for basic auth
            %       password    - Password for basic auth
            %
            %   Response struct fields:
            %       status_code - HTTP status code
            %       status_text - HTTP status text
            %       body        - Response body as string
            %       headers     - Response headers struct
            %       url         - Final URL after redirects
            %       success     - Boolean, true if status 200-299
            %       response_time - Response time in seconds

            if nargin < 2
                options = struct();
            end
            response = mod.request('GET', url, [], [], options);
        end

        function response = post(url, body, content_type, options)
            %POST Send HTTP POST request
            %   response = http_utils.post(url, body, content_type)
            %   response = http_utils.post(url, body, content_type, options)

            if nargin < 3
                content_type = 'application/x-www-form-urlencoded';
            end
            if nargin < 4
                options = struct();
            end
            response = mod.request('POST', url, body, content_type, options);
        end

        function response = post_json(url, data, options)
            %POST_JSON Send HTTP POST request with JSON body
            %   response = http_utils.post_json(url, data)
            %   response = http_utils.post_json(url, data, options)

            if nargin < 3
                options = struct();
            end
            json_body = mod.to_json(data);
            response = mod.request('POST', url, json_body, 'application/json', options);
        end

        function response = put(url, body, content_type, options)
            %PUT Send HTTP PUT request
            if nargin < 3
                content_type = 'application/x-www-form-urlencoded';
            end
            if nargin < 4
                options = struct();
            end
            response = mod.request('PUT', url, body, content_type, options);
        end

        function response = put_json(url, data, options)
            %PUT_JSON Send HTTP PUT request with JSON body
            if nargin < 3
                options = struct();
            end
            json_body = mod.to_json(data);
            response = mod.request('PUT', url, json_body, 'application/json', options);
        end

        function response = delete_req(url, options)
            %DELETE_REQ Send HTTP DELETE request
            %   Note: Named delete_req to avoid conflict with MATLAB delete keyword
            if nargin < 2
                options = struct();
            end
            response = mod.request('DELETE', url, [], [], options);
        end

        function response = patch(url, body, content_type, options)
            %PATCH Send HTTP PATCH request
            if nargin < 3
                content_type = 'application/x-www-form-urlencoded';
            end
            if nargin < 4
                options = struct();
            end
            response = mod.request('PATCH', url, body, content_type, options);
        end

        function response = head(url, options)
            %HEAD Send HTTP HEAD request
            if nargin < 2
                options = struct();
            end
            response = mod.request('HEAD', url, [], [], options);
        end

        %% URL Utilities

        function url = build_url(base_url, params)
            %BUILD_URL Build URL with query parameters
            %   url = http_utils.build_url(base_url, params)
            %
            %   Example:
            %       params = struct('q', 'hello world', 'page', 1);
            %       url = http_utils.build_url('https://api.example.com/search', params);
            %       % Returns: 'https://api.example.com/search?q=hello%20world&page=1'

            if isempty(params) || ~isstruct(params)
                url = base_url;
                return;
            end

            query_string = mod.build_query_string(params);
            if isempty(query_string)
                url = base_url;
            elseif contains(base_url, '?')
                url = [base_url '&' query_string];
            else
                url = [base_url '?' query_string];
            end
        end

        function query_string = build_query_string(params)
            %BUILD_QUERY_STRING Build URL-encoded query string from struct
            %   query_string = http_utils.build_query_string(params)
            %
            %   Example:
            %       params = struct('q', 'hello world', 'page', 1);
            %       qs = http_utils.build_query_string(params);
            %       % Returns: 'q=hello%20world&page=1'

            if isempty(params) || ~isstruct(params)
                query_string = '';
                return;
            end

            fields = fieldnames(params);
            parts = {};

            for i = 1:length(fields)
                key = fields{i};
                value = params.(key);

                % Convert value to string
                if isnumeric(value)
                    value_str = num2str(value);
                elseif islogical(value)
                    value_str = char(string(value));
                elseif ischar(value) || isstring(value)
                    value_str = char(value);
                else
                    value_str = char(string(value));
                end

                % URL encode key and value
                encoded_key = urlencode(key);
                encoded_value = urlencode(value_str);
                parts{end+1} = [encoded_key '=' encoded_value];
            end

            query_string = strjoin(parts, '&');
        end

        function params = parse_query_string(query_string)
            %PARSE_QUERY_STRING Parse URL query string into struct
            %   params = http_utils.parse_query_string(query_string)
            %
            %   Example:
            %       params = http_utils.parse_query_string('q=hello%20world&page=1');
            %       % Returns: struct('q', 'hello world', 'page', '1')

            params = struct();
            if isempty(query_string)
                return;
            end

            % Remove leading ? if present
            if startsWith(query_string, '?')
                query_string = query_string(2:end);
            end
            if isempty(query_string)
                return;
            end

            % Split by &
            pairs = strsplit(query_string, '&');

            for i = 1:length(pairs)
                pair = pairs{i};
                if isempty(pair)
                    continue;
                end

                % Split by =
                kv = strsplit(pair, '=');
                if length(kv) >= 2
                    key = urldecode(kv{1});
                    value = urldecode(kv{2});
                    params.(key) = value;
                elseif length(kv) == 1
                    key = urldecode(kv{1});
                    params.(key) = '';
                end
            end
        end

        function encoded = url_encode(str)
            %URL_ENCODE URL encode a string
            %   encoded = http_utils.url_encode(str)
            %
            %   Example:
            %       encoded = http_utils.url_encode('hello world!');
            %       % Returns: 'hello%20world%21'
            encoded = urlencode(str);
        end

        function decoded = url_decode(str)
            %URL_DECODE URL decode a string
            %   decoded = http_utils.url_decode(str)
            %
            %   Example:
            %       decoded = http_utils.url_decode('hello%20world');
            %       % Returns: 'hello world'
            decoded = urldecode(str);
        end

        function parsed = parse_url(url)
            %PARSE_URL Parse URL into components
            %   parsed = http_utils.parse_url(url)
            %
            %   Returns struct with fields:
            %       scheme   - URL scheme (http, https, etc.)
            %       host     - Hostname
            %       port     - Port number (empty if default)
            %       path     - URL path
            %       query    - Query string (without leading ?)
            %       fragment - Fragment (without leading #)
            %
            %   Example:
            %       parsed = http_utils.parse_url('https://api.example.com:8080/v1/users?page=1');

            parsed = struct();
            parsed.scheme = '';
            parsed.host = '';
            parsed.port = '';
            parsed.path = '';
            parsed.query = '';
            parsed.fragment = '';

            if isempty(url)
                return;
            end

            % Extract fragment
            fragment_parts = strsplit(url, '#');
            if length(fragment_parts) > 1
                parsed.fragment = fragment_parts{2};
                url = fragment_parts{1};
            end

            % Extract query string
            query_parts = strsplit(url, '?');
            if length(query_parts) > 1
                parsed.query = query_parts{2};
                url = query_parts{1};
            end

            % Extract scheme
            scheme_parts = strsplit(url, '://');
            if length(scheme_parts) > 1
                parsed.scheme = lower(scheme_parts{1});
                url = scheme_parts{2};
            end

            % Extract path
            path_idx = find(url == '/', 1);
            if ~isempty(path_idx)
                parsed.path = url(path_idx:end);
                url = url(1:path_idx-1);
            end

            % Extract port and host
            port_idx = find(url == ':', 1);
            if ~isempty(port_idx)
                parsed.port = url(port_idx+1:end);
                parsed.host = url(1:port_idx-1);
            else
                parsed.host = url;
            end
        end

        function is_valid = is_valid_url(url)
            %IS_VALID_URL Check if string is a valid URL
            %   is_valid = http_utils.is_valid_url(url)
            %
            %   Returns true if URL starts with http:// or https://
            if ~ischar(url) && ~isstring(url)
                is_valid = false;
                return;
            end
            url = char(url);
            is_valid = startsWith(lower(url), 'http://') || ...
                       startsWith(lower(url), 'https://');
        end

        function domain = get_domain(url)
            %GET_DOMAIN Extract domain from URL
            %   domain = http_utils.get_domain(url)
            %
            %   Example:
            %       domain = http_utils.get_domain('https://api.example.com/v1/users');
            %       % Returns: 'api.example.com'
            parsed = mod.parse_url(url);
            domain = parsed.host;
        end

        function path = get_path(url)
            %GET_PATH Extract path from URL
            %   path = http_utils.get_path(url)
            %
            %   Example:
            %       path = http_utils.get_path('https://api.example.com/v1/users');
            %       % Returns: '/v1/users'
            parsed = mod.parse_url(url);
            path = parsed.path;
            if isempty(path)
                path = '/';
            end
        end

        function url = add_query_params(url, params)
            %ADD_QUERY_PARAMS Add query parameters to URL
            %   url = http_utils.add_query_params(url, params)
            %
            %   Example:
            %       url = http_utils.add_query_params('https://api.com/search?q=test', struct('page', 2));
            %       % Returns: 'https://api.com/search?q=test&page=2'
            if isempty(params) || ~isstruct(params)
                return;
            end

            new_query = mod.build_query_string(params);
            if isempty(new_query)
                return;
            end

            if contains(url, '?')
                url = [url '&' new_query];
            else
                url = [url '?' new_query];
            end
        end

        %% JSON Utilities

        function json_str = to_json(data)
            %TO_JSON Convert MATLAB data to JSON string
            %   json_str = http_utils.to_json(data)
            %
            %   Converts struct, cell array, or other MATLAB data to JSON
            %
            %   Example:
            %       data = struct('name', 'John', 'age', 30);
            %       json_str = http_utils.to_json(data);
            %       % Returns: '{"name":"John","age":30}'

            if isstruct(data)
                json_str = mod.struct_to_json(data);
            elseif iscell(data)
                json_str = mod.cell_to_json(data);
            elseif isnumeric(data)
                if isscalar(data)
                    json_str = num2str(data);
                else
                    json_str = mod.array_to_json(data);
                end
            elseif islogical(data)
                if data
                    json_str = 'true';
                else
                    json_str = 'false';
                end
            elseif ischar(data) || isstring(data)
                json_str = ['"' mod.escape_json_string(char(data)) '"'];
            else
                json_str = ['"' char(string(data)) '"'];
            end
        end

        function data = from_json(json_str)
            %FROM_JSON Parse JSON string to MATLAB data
            %   data = http_utils.from_json(json_str)
            %
            %   Parses JSON string into MATLAB struct or cell array
            %
            %   Example:
            %       data = http_utils.from_json('{"name":"John","age":30}');
            %       % Returns: struct('name', 'John', 'age', 30)

            try
                data = jsondecode(json_str);
            catch
                data = [];
            end
        end

        function is_valid = is_valid_json(str)
            %IS_VALID_JSON Check if string is valid JSON
            %   is_valid = http_utils.is_valid_json(str)
            try
                jsondecode(str);
                is_valid = true;
            catch
                is_valid = false;
            end
        end

        %% HTTP Status Code Utilities

        function status_text = status_text(code)
            %STATUS_TEXT Get HTTP status text for status code
            %   status_text = http_utils.status_text(code)
            %
            %   Example:
            %       text = http_utils.status_text(200);  % Returns: 'OK'
            %       text = http_utils.status_text(404);  % Returns: 'Not Found'

            status_map = containers.Map({200, 201, 204, 301, 302, 304, 400, 401, 403, 404, 405, 500, 502, 503}, ...
                                        {'OK', 'Created', 'No Content', 'Moved Permanently', 'Found', 'Not Modified', ...
                                         'Bad Request', 'Unauthorized', 'Forbidden', 'Not Found', 'Method Not Allowed', ...
                                         'Internal Server Error', 'Bad Gateway', 'Service Unavailable'});

            if isKey(status_map, code)
                status_text = status_map(code);
            else
                status_text = 'Unknown';
            end
        end

        function success = is_success_status(code)
            %IS_SUCCESS_STATUS Check if status code indicates success (200-299)
            %   success = http_utils.is_success_status(code)
            success = code >= 200 && code < 300;
        end
    end

    methods (Static = true, Access = private)
        %% Private helper methods

        function response = request(method, url, body, content_type, options)
            %REQUEST Internal method to make HTTP requests

            % Initialize response struct
            response = struct();
            response.status_code = 0;
            response.status_text = '';
            response.body = '';
            response.headers = struct();
            response.url = url;
            response.success = false;
            response.response_time = 0;

            % Validate URL
            if isempty(url)
                response.body = 'Error: URL is empty';
                return;
            end

            % Build weboptions
            web_opts = weboptions('RequestMethod', method);

            % Set timeout
            if isfield(options, 'timeout') && ~isempty(options.timeout)
                web_opts.Timeout = options.timeout;
            else
                web_opts.Timeout = 30;
            end

            % Set headers
            if isfield(options, 'headers') && isstruct(options.headers)
                header_fields = fieldnames(options.headers);
                for i = 1:length(header_fields)
                    field = header_fields{i};
                    web_opts.(field) = options.headers.(field);
                end
            end

            % Set authentication
            if isfield(options, 'username') && ~isempty(options.username)
                web_opts.Username = options.username;
                if isfield(options, 'password') && ~isempty(options.password)
                    web_opts.Password = options.password;
                end
            end

            % Record start time
            start_time = tic;

            try
                % Make request based on method
                switch upper(method)
                    case 'GET'
                        [data, status] = webread(url, web_opts);
                        response.body = mod.data_to_string(data);
                        response.status_code = status.StatusCode;

                    case {'POST', 'PUT', 'PATCH'}
                        if ~isempty(content_type)
                            web_opts.MediaType = content_type;
                        end
                        if ~isempty(body)
                            [data, status] = webwrite(url, body, web_opts);
                        else
                            [data, status] = webread(url, web_opts);
                        end
                        response.body = mod.data_to_string(data);
                        response.status_code = status.StatusCode;

                    case 'DELETE'
                        % For DELETE, use webread with DELETE method
                        [data, status] = webread(url, web_opts);
                        response.body = mod.data_to_string(data);
                        response.status_code = status.StatusCode;

                    case 'HEAD'
                        % HEAD request - get headers only
                        [~, status] = webread(url, web_opts);
                        response.status_code = status.StatusCode;
                        response.body = '';

                    otherwise
                        response.body = ['Error: Unsupported HTTP method: ' method];
                        return;
                end

                % Get status text
                response.status_text = mod.status_text(response.status_code);
                response.success = mod.is_success_status(response.status_code);
                response.response_time = toc(start_time);

            catch ME
                response.response_time = toc(start_time);
                response.body = ['Error: ' ME.message];

                % Try to extract status code from error
                if contains(ME.message, '404')
                    response.status_code = 404;
                    response.status_text = 'Not Found';
                elseif contains(ME.message, '500')
                    response.status_code = 500;
                    response.status_text = 'Internal Server Error';
                elseif contains(ME.message, '401')
                    response.status_code = 401;
                    response.status_text = 'Unauthorized';
                elseif contains(ME.message, '403')
                    response.status_code = 403;
                    response.status_text = 'Forbidden';
                elseif contains(ME.message, 'timeout')
                    response.status_code = 408;
                    response.status_text = 'Request Timeout';
                end
            end
        end

        function str = data_to_string(data)
            %DATA_TO_STRING Convert response data to string
            if ischar(data)
                str = data;
            elseif isstring(data)
                str = char(data);
            elseif isstruct(data) || iscell(data)
                try
                    str = jsonencode(data);
                catch
                    str = char(string(data));
                end
            else
                str = char(string(data));
            end
        end

        function json_str = struct_to_json(s)
            %STRUCT_TO_JSON Convert struct to JSON string
            fields = fieldnames(s);
            parts = {};

            for i = 1:length(fields)
                field = fields{i};
                value = s.(field);
                json_value = mod.to_json(value);
                parts{end+1} = ['"' field '":' json_value];
            end

            json_str = ['{' strjoin(parts, ',') '}'];
        end

        function json_str = cell_to_json(c)
            %CELL_TO_JSON Convert cell array to JSON array string
            parts = {};
            for i = 1:length(c)
                parts{end+1} = mod.to_json(c{i});
            end
            json_str = ['[' strjoin(parts, ',') ']'];
        end

        function json_str = array_to_json(arr)
            %ARRAY_TO_JSON Convert numeric array to JSON array string
            if isvector(arr)
                parts = {};
                for i = 1:length(arr)
                    parts{end+1} = num2str(arr(i));
                end
                json_str = ['[' strjoin(parts, ',') ']'];
            else
                % 2D array - convert to array of arrays
                [rows, cols] = size(arr);
                row_parts = {};
                for r = 1:rows
                    col_parts = {};
                    for c = 1:cols
                        col_parts{end+1} = num2str(arr(r, c));
                    end
                    row_parts{end+1} = ['[' strjoin(col_parts, ',') ']'];
                end
                json_str = ['[' strjoin(row_parts, ',') ']'];
            end
        end

        function escaped = escape_json_string(str)
            %ESCAPE_JSON_STRING Escape special characters for JSON
            escaped = str;
            escaped = strrep(escaped, '\', '\\');
            escaped = strrep(escaped, '"', '\"');
            escaped = strrep(escaped, sprintf('\n'), '\n');
            escaped = strrep(escaped, sprintf('\r'), '\r');
            escaped = strrep(escaped, sprintf('\t'), '\t');
        end
    end
end
