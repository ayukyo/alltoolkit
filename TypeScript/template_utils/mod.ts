/**
 * TypeScript Template Engine Utilities
 * A lightweight, zero-dependency template engine with variable interpolation,
 * conditionals, loops, and filters.
 */

// Types and Interfaces
export type TemplateContext = Record<string, any>;
export type Partials = Record<string, string>;
export type FilterFunction = (value: any, ...args: any[]) => any;

export interface TemplateEngineOptions {
    filters?: Record<string, FilterFunction>;
    defaults?: TemplateContext;
    strict?: boolean;
}

// Built-in Filters
export const BuiltInFilters: Record<string, FilterFunction> = {
    upper: (value: any): string => String(value).toUpperCase(),
    lower: (value: any): string => String(value).toLowerCase(),
    capitalize: (value: any): string => {
        const str = String(value);
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    },
    title: (value: any): string => {
        return String(value).split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');
    },
    trim: (value: any): string => String(value).trim(),
    reverse: (value: any): string => String(value).split('').reverse().join(''),
    escape: (value: any): string => {
        return String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    },
    join: (value: any, separator: string = ','): string => {
        if (Array.isArray(value)) return value.join(separator);
        return String(value);
    },
    first: (value: any): any => Array.isArray(value) && value.length > 0 ? value[0] : value,
    last: (value: any): any => Array.isArray(value) && value.length > 0 ? value[value.length - 1] : value,
    size: (value: any): number => {
        if (Array.isArray(value) || typeof value === 'string') return value.length;
        if (value && typeof value === 'object') return Object.keys(value).length;
        return 0;
    },
    sort: (value: any): any[] => Array.isArray(value) ? [...value].sort() : value,
    reverse_array: (value: any): any[] => Array.isArray(value) ? [...value].reverse() : value,
    round: (value: any, decimals: number = 0): number => {
        const num = parseFloat(value);
        if (isNaN(num)) return 0;
        return Math.round(num * Math.pow(10, decimals)) / Math.pow(10, decimals);
    },
    abs: (value: any): number => {
        const num = parseFloat(value);
        return isNaN(num) ? 0 : Math.abs(num);
    },
    default: (value: any, defaultValue: string = ''): any => value === undefined || value === null || value === '' ? defaultValue : value,
    truncate: (value: any, length: number = 50, suffix: string = '...'): string => {
        const str = String(value);
        return str.length <= length ? str : str.substring(0, length - suffix.length) + suffix;
    },
    replace: (value: any, search: string, replacement: string = ''): string => String(value).replace(new RegExp(search, 'g'), replacement),
    url_encode: (value: any): string => encodeURIComponent(String(value)),
    url_decode: (value: any): string => decodeURIComponent(String(value)),
};

// Template Engine Class
export class TemplateEngine {
    private filters: Map<string, FilterFunction>;
    private defaults: TemplateContext;
    private strict: boolean;

    constructor(options: TemplateEngineOptions = {}) {
        this.filters = new Map(Object.entries(BuiltInFilters));
        this.defaults = options.defaults || {};
        this.strict = options.strict || false;
        if (options.filters) {
            for (const [name, fn] of Object.entries(options.filters)) {
                this.registerFilter(name, fn);
            }
        }
    }

    registerFilter(name: string, fn: FilterFunction): TemplateEngine {
        this.filters.set(name, fn);
        return this;
    }

    getFilter(name: string): FilterFunction | undefined {
        return this.filters.get(name);
    }

    render(template: string, context: TemplateContext = {}, partials: Partials = {}): string {
        const mergedContext = { ...this.defaults, ...context };
        return this.processTemplate(template, mergedContext, partials);
    }

    private processTemplate(template: string, context: TemplateContext, partials: Partials): string {
        let result = template;
        result = this.processIncludes(result, context, partials);
        result = this.processConditionals(result, context, partials);
        result = this.processLoops(result, context, partials);
        result = this.processVariables(result, context);
        result = this.processComments(result);
        return result;
    }

    private processIncludes(template: string, context: TemplateContext, partials: Partials): string {
        const includeRegex = /{%\s*include\s+["']([^"']+)["']\s*%}/g;
        return template.replace(includeRegex, (match, partialName) => {
            const partial = partials[partialName];
            if (partial === undefined) return this.strict ? `[Missing partial: ${partialName}]` : '';
            return this.processTemplate(partial, context, partials);
        });
    }

    private processConditionals(template: string, context: TemplateContext, partials: Partials): string {
        let result = template;
        const ifRegex = /{%\s*if\s+([^%}]+)%}([\s\S]*?){%\s*endif\s*%}/g;
        result = result.replace(ifRegex, (match, condition, content) => {
            const conditionResult = this.evaluateCondition(condition.trim(), context);
            const elseRegex = /{%\s*else\s*%}/;
            const parts = content.split(elseRegex);
            if (conditionResult) return this.processTemplate(parts[0], context, partials);
            else if (parts.length > 1) return this.processTemplate(parts[1], context, partials);
            return '';
        });
        return result;
    }

    private evaluateCondition(condition: string, context: TemplateContext): boolean {
        const notMatch = condition.match(/^not\s+(.+)$/);
        if (notMatch) return !this.evaluateCondition(notMatch[1].trim(), context);
        const operators = ['==', '!=', '>=', '<=', '>', '<'];
        for (const op of operators) {
            // 2026-06-21 优化: 使用 indexOf 找到操作符位置再 split，
            // 避免误拆（如 "count ==" 中把 "==" 拆成多个 ""）
            const opIdx = condition.indexOf(op);
            if (opIdx > 0 && opIdx < condition.length - op.length) {
                const left = this.resolveValue(condition.substring(0, opIdx).trim(), context);
                const right = this.resolveValue(condition.substring(opIdx + op.length).trim(), context);
                switch (op) {
                    case '==': return left == right;
                    case '!=': return left != right;
                    case '>=': return left >= right;
                    case '<=': return left <= right;
                    case '>': return left > right;
                    case '<': return left < right;
                }
            }
        }
        return !!this.resolveVariable(condition, context);
    }

    /**
     * 2026-06-21 优化: 解析字面量或变量
     * 支持数字 ("5", "3.14")、字符串 ("'hello'", '"world"')、布尔 ("true", "false")、null
     */
    private resolveValue(token: string, context: TemplateContext): any {
        // 字符串字面量
        if ((token.startsWith('"') && token.endsWith('"')) ||
            (token.startsWith("'") && token.endsWith("'"))) {
            return token.substring(1, token.length - 1);
        }
        // 数字字面量
        if (/^-?\d+(?:\.\d+)?$/.test(token)) {
            return Number(token);
        }
        // 布尔/null 字面量
        if (token === 'true') return true;
        if (token === 'false') return false;
        if (token === 'null') return null;
        // 否则按变量路径解析
        return this.resolveVariable(token, context);
    }

    private processLoops(template: string, context: TemplateContext, partials: Partials): string {
        const forRegex = /{%\s*for\s+(\w+)\s+in\s+([^%}]+)%}([\s\S]*?){%\s*endfor\s*%}/g;
        return template.replace(forRegex, (match, itemName, collectionName, content) => {
            const collection = this.resolveVariable(collectionName.trim(), context);
            if (!Array.isArray(collection)) return '';
            return collection.map((item, index) => {
                const loopContext = { ...context, [itemName]: item, loop: { index, index1: index + 1, first: index === 0, last: index === collection.length - 1 } };
                return this.processTemplate(content, loopContext, partials);
            }).join('');
        });
    }

    private processVariables(template: string, context: TemplateContext): string {
        const varRegex = /{{\s*([^|}]+)(?:\s*\|\s*([^}]+))?\s*}}/g;
        return template.replace(varRegex, (match, varName, filterChain) => {
            let value = this.resolveVariable(varName.trim(), context);
            if (filterChain) {
                const filters = filterChain.split('|').map(f => f.trim());
                for (const filterExpr of filters) {
                    const filterMatch = filterExpr.match(/^([^:]+)(?::(.+))?$/);
                    if (filterMatch) {
                        const filterName = filterMatch[1];
                        // 2026-06-21 优化: 解析 filter 参数为字面量或变量
                        // 支持带引号的字符串（可包含逗号）、数字、布尔、null、变量引用
                        const args: any[] = [];
                        if (filterMatch[2]) {
                            const argTokens = this.splitFilterArgs(filterMatch[2]);
                            for (const token of argTokens) {
                                args.push(this.parseFilterArg(token.trim(), context));
                            }
                        }
                        const filterFn = this.filters.get(filterName);
                        if (filterFn) {
                            value = filterFn(value, ...args);
                        }
                    }
                }
            }
            return String(value);
        });
    }

    /**
     * 2026-06-21 优化: 解析 filter 参数
     * 支持字符串字面量 ('value' / "value")、数字、布尔、null 和变量引用
     */
    private parseFilterArg(token: string, context: TemplateContext): any {
        if ((token.startsWith('"') && token.endsWith('"')) ||
            (token.startsWith("'") && token.endsWith("'"))) {
            return token.substring(1, token.length - 1);
        }
        if (/^-?\d+(?:\.\d+)?$/.test(token)) {
            return Number(token);
        }
        if (token === 'true') return true;
        if (token === 'false') return false;
        if (token === 'null') return null;
        if (token === 'undefined') return undefined;
        return this.resolveVariable(token, context);
    }

    /**
     * 2026-06-21 优化: 按顶层逗号切分 filter 参数
     * 字符串内的逗号不会被切分（如 "'a,b', c" → ["'a,b'", "c"]）
     */
    private splitFilterArgs(input: string): string[] {
        const args: string[] = [];
        let buf = '';
        let quote: string | null = null;
        for (let i = 0; i < input.length; i++) {
            const ch = input[i];
            if (quote) {
                buf += ch;
                if (ch === quote) quote = null;
            } else if (ch === '"' || ch === "'") {
                buf += ch;
                quote = ch;
            } else if (ch === ',') {
                args.push(buf);
                buf = '';
            } else {
                buf += ch;
            }
        }
        if (buf.length > 0 || args.length > 0) args.push(buf);
        return args;
    }

    private resolveVariable(path: string, context: TemplateContext): any {
        const parts = path.split('.');
        let value: any = context;
        for (const part of parts) {
            if (value === undefined || value === null) return '';
            value = value[part];
        }
        return value === undefined ? '' : value;
    }

    private processComments(template: string): string {
        return template.replace(/{#\s*[\s\S]*?\s*#}/g, '');
    }
}

// Convenience function
export function renderTemplate(template: string, context: TemplateContext = {}, partials: Partials = {}, options?: TemplateEngineOptions): string {
    const engine = new TemplateEngine(options);
    return engine.render(template, context, partials);
}

// Default export
export default TemplateEngine;
