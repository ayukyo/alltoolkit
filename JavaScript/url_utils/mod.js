/**
 * URL Utilities - URL parsing, manipulation, and validation
 * Zero external dependencies - pure JavaScript implementation
 * 
 * @module url_utils
 * @version 1.0.0
 */

'use strict';

/**
 * Parse a URL into its components
 * @param {string} url - The URL to parse
 * @returns {Object|null} Parsed URL components or null if invalid
 */
function parse(url) {
    if (typeof url !== 'string' || url.trim() === '') {
        return null;
    }

    try {
        const urlObj = new URL(url);
        return {
            protocol: urlObj.protocol.replace(':', ''),
            username: urlObj.username || null,
            password: urlObj.password || null,
            hostname: urlObj.hostname,
            port: urlObj.port || null,
            path: urlObj.pathname,
            query: parseQuery(urlObj.search),
            hash: urlObj.hash.replace('#', '') || null,
            origin: urlObj.origin,
            href: urlObj.href
        };
    } catch (e) {
        return null;
    }
}

/**
 * Parse query string into an object
 * @param {string} queryString - The query string (with or without leading ?)
 * @returns {Object} Parsed query parameters
 */
function parseQuery(queryString) {
    const params = {};
    
    if (!queryString) return params;
    
    // Remove leading ? if present
    const search = queryString.startsWith('?') ? queryString.slice(1) : queryString;
    
    if (!search) return params;
    
    const pairs = search.split('&');
    for (const pair of pairs) {
        if (!pair) continue;
        
        const eqIndex = pair.indexOf('=');
        let key, value;
        
        if (eqIndex === -1) {
            key = decodeURIComponent(pair);
            value = '';
        } else {
            key = decodeURIComponent(pair.slice(0, eqIndex));
            value = decodeURIComponent(pair.slice(eqIndex + 1));
        }
        
        // Handle array-like keys (key[])
        if (key.endsWith('[]')) {
            const arrayKey = key.slice(0, -2);
            if (!params[arrayKey]) {
                params[arrayKey] = [];
            }
            if (Array.isArray(params[arrayKey])) {
                params[arrayKey].push(value);
            }
        }
        // Handle duplicate keys (convert to array)
        else if (params.hasOwnProperty(key)) {
            if (!Array.isArray(params[key])) {
                params[key] = [params[key]];
            }
            params[key].push(value);
        }
        else {
            params[key] = value;
        }
    }
    
    return params;
}

/**
 * Build a query string from an object
 * @param {Object} params - Query parameters
 * @param {Object} options - Build options
 * @param {boolean} options.sort - Whether to sort keys (default: false)
 * @param {boolean} options.encode - Whether to encode values (default: true)
 * @param {string} options.prefix - Prefix for the query string (default: '?')
 * @returns {string} Query string
 */
function buildQuery(params, options = {}) {
    const { sort = false, encode = true, prefix = '?' } = options;
    
    if (!params || typeof params !== 'object' || Object.keys(params).length === 0) {
        return '';
    }
    
    const pairs = [];
    const keys = sort ? Object.keys(params).sort() : Object.keys(params);
    
    for (const key of keys) {
        const value = params[key];
        
        if (value === null || value === undefined) {
            continue;
        }
        
        const encodedKey = encode ? encodeURIComponent(key) : key;
        
        if (Array.isArray(value)) {
            for (const item of value) {
                if (item !== null && item !== undefined) {
                    const encodedValue = encode ? encodeURIComponent(String(item)) : String(item);
                    pairs.push(`${encodedKey}=${encodedValue}`);
                }
            }
        } else {
            const encodedValue = encode ? encodeURIComponent(String(value)) : String(value);
            pairs.push(`${encodedKey}=${encodedValue}`);
        }
    }
    
    return pairs.length > 0 ? prefix + pairs.join('&') : '';
}

/**
 * Build a URL from components
 * @param {Object} components - URL components
 * @returns {string} Built URL
 */
function build(components) {
    if (!components || typeof components !== 'object') {
        throw new Error('Components must be an object');
    }
    
    const {
        protocol = 'https',
        username,
        password,
        hostname,
        port,
        path = '/',
        query = {},
        hash
    } = components;
    
    if (!hostname) {
        throw new Error('Hostname is required');
    }
    
    let url = `${protocol}://`;
    
    // Add authentication if provided
    if (username) {
        url += encodeURIComponent(username);
        if (password) {
            url += ':' + encodeURIComponent(password);
        }
        url += '@';
    }
    
    url += hostname;
    
    // Add port if provided
    if (port) {
        url += ':' + port;
    }
    
    // Add path
    url += path.startsWith('/') ? path : '/' + path;
    
    // Add query string
    const queryString = buildQuery(query);
    if (queryString) {
        url += queryString;
    }
    
    // Add hash if provided
    if (hash) {
        url += '#' + (hash.startsWith('#') ? hash.slice(1) : hash);
    }
    
    return url;
}

/**
 * Validate a URL
 * @param {string} url - The URL to validate
 * @param {Object} options - Validation options
 * @param {string[]} options.protocols - Allowed protocols (default: ['http', 'https'])
 * @param {boolean} options.requireProtocol - Require protocol (default: true)
 * @returns {boolean} Whether the URL is valid
 */
function isValid(url, options = {}) {
    const {
        protocols = ['http', 'https'],
        requireProtocol = true
    } = options;
    
    if (typeof url !== 'string' || url.trim() === '') {
        return false;
    }
    
    try {
        const parsed = new URL(url);
        const protocol = parsed.protocol.replace(':', '');
        return protocols.includes(protocol);
    } catch (e) {
        if (!requireProtocol) {
            // Try with a default protocol
            try {
                const parsed = new URL('https://' + url);
                return true;
            } catch (e2) {
                return false;
            }
        }
        return false;
    }
}

/**
 * Join URL paths
 * @param {...string} parts - Path parts to join
 * @returns {string} Joined path
 */
function joinPaths(...parts) {
    if (parts.length === 0) return '/';
    
    // Handle full URLs in the first part
    if (parts[0].includes('://')) {
        const url = parts[0];
        const parsed = parse(url);
        if (parsed) {
            const pathParts = [parsed.path, ...parts.slice(1)];
            const joinedPath = pathParts
                .filter(p => p)
                .join('/')
                .replace(/\/+/g, '/')
                .replace(/^(.+)\/$/, '$1');
            parsed.path = joinedPath || '/';
            return build(parsed);
        }
    }
    
    return parts
        .filter(p => p !== null && p !== undefined && p !== '')
        .join('/')
        .replace(/\/+/g, '/')
        .replace(/^(.+)\/$/, '$1') || '/';
}

/**
 * Resolve a URL against a base URL
 * @param {string} base - Base URL
 * @param {string} relative - Relative URL
 * @returns {string|null} Resolved URL or null if invalid
 */
function resolve(base, relative) {
    if (!base || !relative) return null;
    
    try {
        const baseUrl = new URL(base);
        const resolvedUrl = new URL(relative, baseUrl);
        return resolvedUrl.href;
    } catch (e) {
        return null;
    }
}

/**
 * Normalize a URL (remove default ports, trailing slashes, etc.)
 * @param {string} url - URL to normalize
 * @returns {string|null} Normalized URL or null if invalid
 */
function normalize(url) {
    const parsed = parse(url);
    if (!parsed) return null;
    
    // Remove default ports
    let port = parsed.port;
    if (parsed.protocol === 'http' && parsed.port === '80') {
        port = null;
    } else if (parsed.protocol === 'https' && parsed.port === '443') {
        port = null;
    }
    
    // Normalize path (remove trailing slash except for root)
    let path = parsed.path;
    if (path !== '/' && path.endsWith('/')) {
        path = path.slice(0, -1);
    }
    
    // Sort query parameters
    const sortedQuery = {};
    const sortedKeys = Object.keys(parsed.query).sort();
    for (const key of sortedKeys) {
        sortedQuery[key] = parsed.query[key];
    }
    
    return build({
        protocol: parsed.protocol,
        username: parsed.username,
        password: parsed.password,
        hostname: parsed.hostname.toLowerCase(),
        port: port,
        path: path,
        query: sortedQuery,
        hash: parsed.hash
    });
}

/**
 * Extract domain from URL
 * @param {string} url - URL to extract domain from
 * @returns {string|null} Domain or null if invalid
 */
function getDomain(url) {
    const parsed = parse(url);
    return parsed ? parsed.hostname : null;
}

/**
 * Extract top-level domain (TLD) from URL
 * @param {string} url - URL to extract TLD from
 * @returns {string|null} TLD or null if invalid
 */
function getTLD(url) {
    const domain = getDomain(url);
    if (!domain) return null;
    
    // Handle IP addresses
    if (/^\d+\.\d+\.\d+\.\d+$/.test(domain)) {
        return null;
    }
    
    // Handle localhost
    if (domain === 'localhost') {
        return null;
    }
    
    const parts = domain.split('.');
    if (parts.length < 2) return null;
    
    // Simple TLD extraction (doesn't handle multi-level TLDs like .co.uk)
    return parts[parts.length - 1];
}

/**
 * Extract subdomain from URL
 * @param {string} url - URL to extract subdomain from
 * @returns {string|null} Subdomain or null if invalid or no subdomain
 */
function getSubdomain(url) {
    const domain = getDomain(url);
    if (!domain) return null;
    
    // Handle IP addresses and localhost
    if (/^\d+\.\d+\.\d+\.\d+$/.test(domain) || domain === 'localhost') {
        return null;
    }
    
    const parts = domain.split('.');
    if (parts.length < 3) return null;
    
    return parts.slice(0, -2).join('.');
}

/**
 * Check if URL is absolute
 * @param {string} url - URL to check
 * @returns {boolean} Whether the URL is absolute
 */
function isAbsolute(url) {
    if (typeof url !== 'string') return false;
    // Matches protocol-relative URLs (//example.com) or full URLs (https://example.com)
    return /^(?:[a-z][a-z0-9+.-]*:|\/\/)/i.test(url);
}

/**
 * Check if URL is relative
 * @param {string} url - URL to check
 * @returns {boolean} Whether the URL is relative
 */
function isRelative(url) {
    return !isAbsolute(url);
}

/**
 * Add or update query parameters
 * @param {string} url - URL to modify
 * @param {Object} params - Query parameters to add/update
 * @returns {string|null} Modified URL or null if invalid
 */
function addQuery(url, params) {
    const parsed = parse(url);
    if (!parsed) return null;
    
    const newQuery = { ...parsed.query, ...params };
    return build({ ...parsed, query: newQuery });
}

/**
 * Remove query parameters from URL
 * @param {string} url - URL to modify
 * @param {string[]} keys - Keys to remove
 * @returns {string|null} Modified URL or null if invalid
 */
function removeQuery(url, keys) {
    const parsed = parse(url);
    if (!parsed) return null;
    
    const newQuery = { ...parsed.query };
    for (const key of keys) {
        delete newQuery[key];
    }
    
    return build({ ...parsed, query: newQuery });
}

/**
 * Extract file extension from URL path
 * @param {string} url - URL to extract extension from
 * @returns {string|null} File extension (without dot) or null
 */
function getExtension(url) {
    const parsed = parse(url);
    if (!parsed) return null;
    
    const match = parsed.path.match(/\.([a-z0-9]+)$/i);
    return match ? match[1].toLowerCase() : null;
}

/**
 * Extract filename from URL path
 * @param {string} url - URL to extract filename from
 * @returns {string|null} Filename or null
 */
function getFilename(url) {
    const parsed = parse(url);
    if (!parsed) return null;
    
    const parts = parsed.path.split('/');
    const filename = parts[parts.length - 1];
    return filename || null;
}

/**
 * Convert relative URL to absolute
 * @param {string} relative - Relative URL
 * @param {string} base - Base URL
 * @returns {string|null} Absolute URL or null if invalid
 */
function toAbsolute(relative, base) {
    if (isAbsolute(relative)) return relative;
    return resolve(base, relative);
}

/**
 * Check if two URLs are equivalent (after normalization)
 * @param {string} url1 - First URL
 * @param {string} url2 - Second URL
 * @returns {boolean} Whether the URLs are equivalent
 */
function areEquivalent(url1, url2) {
    const normalized1 = normalize(url1);
    const normalized2 = normalize(url2);
    return normalized1 === normalized2;
}

/**
 * Extract path segments from URL
 * @param {string} url - URL to extract segments from
 * @returns {string[]} Path segments
 */
function getPathSegments(url) {
    const parsed = parse(url);
    if (!parsed) return [];
    
    return parsed.path
        .split('/')
        .filter(segment => segment !== '');
}

/**
 * Build URL from template with parameters
 * @param {string} template - URL template with :param placeholders
 * @param {Object} params - Parameters to substitute
 * @returns {string} URL with substituted parameters
 */
function fromTemplate(template, params = {}) {
    let result = template;
    
    for (const [key, value] of Object.entries(params)) {
        const placeholder = ':' + key;
        result = result.replace(placeholder, encodeURIComponent(value));
    }
    
    return result;
}

/**
 * Parse URL template to extract parameter names
 * @param {string} template - URL template with :param placeholders
 * @returns {string[]} Parameter names
 */
function parseTemplate(template) {
    const matches = template.match(/:(\w+)/g) || [];
    return matches.map(m => m.slice(1));
}

// Export all functions
module.exports = {
    parse,
    parseQuery,
    buildQuery,
    build,
    isValid,
    joinPaths,
    resolve,
    normalize,
    getDomain,
    getTLD,
    getSubdomain,
    isAbsolute,
    isRelative,
    addQuery,
    removeQuery,
    getExtension,
    getFilename,
    toAbsolute,
    areEquivalent,
    getPathSegments,
    fromTemplate,
    parseTemplate
};