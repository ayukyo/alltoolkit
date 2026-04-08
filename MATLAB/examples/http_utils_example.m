function http_utils_example()
    %HTTP_UTILS_EXAMPLE Example usage of HTTP utilities
    %
    % Run: http_utils_example()

    fprintf('HTTP Utils Example\n');
    fprintf('===============\n\n');

    %% Example 1: URL Parsing
    fprintf('Example 1: URL Parsing\n');
    fprintf('----------------------\n');
    url = 'https://api.example.com:8080/v1/users?page=1#section';
    parsed = http_utils.parse_url(url);
    fprintf('URL: %s\n', url);
    fprintf('  Scheme: %s\n', parsed.scheme);
    fprintf('  Host: %s\n', parsed.host);
    fprintf('  Port: %s\n', parsed.port);
    fprintf('  Path: %s\n', parsed.path);
    fprintf('  Query: %s\n', parsed.query);
    fprintf('  Fragment: %s\n\n', parsed.fragment);

    %% Example 2: Build URL with parameters
    fprintf('Example 2: Build URL with parameters\n');
    fprintf('---------------------------------\n');
    params = struct('q', 'test query', 'page', 1;
    fprintf('  rework_count: %d\n', params.rework_count);
    fprintf('  ADD COLUMN IF NOT EXISTS current_rework_id';
    ADD COLUMN IF NOT EXISTS `rework_id` bigint(20) DEFAULT NULL COMMENT '当前返工记录ID';
