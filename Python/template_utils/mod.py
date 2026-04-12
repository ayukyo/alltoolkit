"""
AllToolkit - Python Template Utilities

A zero-dependency, production-ready string templating utility module.
Supports variable substitution, conditionals, loops, template inheritance,
and safe rendering. Built entirely with Python standard library.

Author: AllToolkit
License: MIT
"""

import re
from typing import Optional, Any, Dict, List, Callable, Tuple


class TemplateConfig:
    """Configuration for template rendering."""
    
    def __init__(
        self,
        var_start: str = "{{",
        var_end: str = "}}",
        block_start: str = "{%",
        block_end: str = "%}",
        max_render_depth: int = 50,
        max_loop_iterations: int = 1000
    ):
        self.var_start = var_start
        self.var_end = var_end
        self.block_start = block_start
        self.block_end = block_end
        self.max_render_depth = max_render_depth
        self.max_loop_iterations = max_loop_iterations


class TemplateError(Exception):
    pass


class TemplateSyntaxError(TemplateError):
    pass


class TemplateRenderError(TemplateError):
    pass


class TemplateNotFoundError(TemplateError):
    pass


class TemplateEngine:
    """Template engine with variable substitution, conditionals, loops, and inheritance."""
    
    BUILTIN_FILTERS = {
        'upper': lambda x: str(x).upper(),
        'lower': lambda x: str(x).lower(),
        'capitalize': lambda x: str(x).capitalize(),
        'title': lambda x: str(x).title(),
        'strip': lambda x: str(x).strip(),
        'length': lambda x: len(x) if x else 0,
        'int': lambda x: int(x),
        'float': lambda x: float(x),
        'str': lambda x: str(x),
        'bool': lambda x: bool(x),
        'list': lambda x: list(x) if x else [],
        'join': lambda x: ''.join(str(i) for i in x) if x else '',
        'first': lambda x: x[0] if x else '',
        'last': lambda x: x[-1] if x else '',
        'reverse': lambda x: list(reversed(x)) if x else [],
        'sort': lambda x: sorted(x) if x else [],
        'escape': lambda x: str(x).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;'),
        'escapejs': lambda x: str(x).replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n'),
        'default': lambda x, default='': x if x else default,
        'truncate': lambda x: str(x)[:50] + '...' if len(str(x)) > 50 else str(x),
    }
    
    def __init__(self, loader=None, autoescape=False):
        self.loader = loader or (lambda name: (_ for _ in ()).throw(TemplateNotFoundError(f"Template not found: {name}")))
        self.autoescape = autoescape
        self.filters = dict(self.BUILTIN_FILTERS)
        self._globals = {}
    
    def register_filter(self, name, func):
        self.filters[name] = func
    
    def set_globals(self, **kwargs):
        self._globals.update(kwargs)
    
    def set_loader(self, loader):
        self.loader = loader
    
    def _get_value(self, name, context):
        name = name.strip()
        if name in self._globals:
            return self._globals[name]
        if name in context:
            return context[name]
        if '.' in name:
            parts = name.split('.')
            value = context.get(parts[0])
            for part in parts[1:]:
                if value is None:
                    break
                if isinstance(value, dict):
                    value = value.get(part)
                elif hasattr(value, part):
                    value = getattr(value, part)
                else:
                    value = None
            return value
        return None
    
    def _resolve_value(self, expr, context):
        expr = expr.strip()
        if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
        try:
            return float(expr) if '.' in expr else int(expr)
        except ValueError:
            pass
        if expr.lower() == 'true':
            return True
        if expr.lower() == 'false':
            return False
        if expr.lower() == 'none':
            return None
        return self._get_value(expr, context)
    
    def _apply_filter(self, value, filter_expr):
        filter_expr = filter_expr.strip()
        if ':' in filter_expr:
            filter_name, filter_arg = filter_expr.split(':', 1)
            filter_name = filter_name.strip()
            filter_arg = filter_arg.strip().strip("'\"")
            if filter_name not in self.filters:
                raise TemplateRenderError(f"Unknown filter: {filter_name}")
            try:
                return self.filters[filter_name](value, int(filter_arg))
            except (TypeError, ValueError):
                return self.filters[filter_name](value, filter_arg)
        if filter_expr not in self.filters:
            raise TemplateRenderError(f"Unknown filter: {filter_expr}")
        return self.filters[filter_expr](value)
    
    def _resolve_variable(self, expr, context):
        parts = [p.strip() for p in expr.split('|')]
        value = self._get_value(parts[0], context)
        for f in parts[1:]:
            value = self._apply_filter(value, f)
        return value
    
    def _eval_condition(self, cond, context):
        cond = cond.strip()
        if cond.startswith('not '):
            return not self._eval_condition(cond[4:], context)
        if ' or ' in cond:
            parts = cond.split(' or ', 1)
            return self._eval_condition(parts[0], context) or self._eval_condition(parts[1], context)
        if ' and ' in cond:
            parts = cond.split(' and ', 1)
            return self._eval_condition(parts[0], context) and self._eval_condition(parts[1], context)
        if ' in ' in cond:
            parts = cond.split(' in ', 1)
            return self._resolve_value(parts[0].strip(), context) in self._resolve_value(parts[1].strip(), context)
        for op in ['==', '!=', '>=', '<=', '>', '<']:
            if op in cond:
                parts = cond.split(op, 1)
                left = self._resolve_value(parts[0].strip(), context)
                right = self._resolve_value(parts[1].strip(), context)
                if left is None or right is None:
                    return (left == right) if op == '==' else (left != right) if op == '!=' else False
                try:
                    left, right = float(left), float(right)
                except (TypeError, ValueError):
                    pass
                if op == '==': return left == right
                if op == '!=': return left != right
                if op == '>=': return left >= right
                if op == '<=': return left <= right
                if op == '>': return left > right
                if op == '<': return left < right
        return bool(self._resolve_value(cond, context))
    
    def _find_matching_end(self, content, pos, start_tag, end_tag):
        """Returns (start_of_end_tag, end_after_tag) tuple."""
        depth = 1
        bs, be = "{%", "%}"
        while pos < len(content) and depth > 0:
            start = content.find(bs, pos)
            if start == -1:
                return (-1, -1)
            end = content.find(be, start)
            if end == -1:
                return (-1, -1)
            tag = content[start+2:end].strip()
            if tag.startswith(start_tag + ' ') or tag == start_tag:
                depth += 1
            elif tag.startswith(end_tag):
                depth -= 1
                if depth == 0:
                    return (start, end + 2)  # (start of {% endfor %}, position after %})
            pos = end + 2
        return (-1, -1)
    
    def _render(self, content, context, depth=0):
        if depth > 50:
            raise TemplateRenderError("Max render depth exceeded")
        
        result = []
        pos = 0
        bs, be = "{%", "%}"
        vs, ve = "{{", "}}"
        
        while pos < len(content):
            # Find next block or variable tag
            block_pos = content.find(bs, pos)
            var_pos = content.find(vs, pos)
            
            # Determine which comes first
            if block_pos == -1 and var_pos == -1:
                # No more tags, process remaining text
                result.append(self._process_vars(content[pos:], context))
                break
            
            if block_pos == -1:
                next_pos = var_pos
            elif var_pos == -1:
                next_pos = block_pos
            else:
                next_pos = min(block_pos, var_pos)
            
            # Add text before the tag
            if next_pos > pos:
                result.append(self._process_vars(content[pos:next_pos], context))
            
            if next_pos == var_pos:
                # Process variable
                end = content.find(ve, var_pos)
                if end == -1:
                    result.append(content[var_pos:])
                    break
                expr = content[var_pos+2:end]
                value = self._resolve_variable(expr, context)
                if value is not None:
                    if self.autoescape:
                        value = str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
                    result.append(str(value))
                pos = end + 2
            
            elif next_pos == block_pos:
                # Process block tag
                end = content.find(be, block_pos)
                if end == -1:
                    result.append(content[block_pos:])
                    break
                tag = content[block_pos+2:end].strip()
                
                if tag.startswith('if '):
                    cond = tag[3:].strip()
                    body_start = end + 2
                    
                    # Find all branches
                    branches = []  # (condition, content)
                    current_pos = body_start
                    branch_depth = 1
                    scan_pos = body_start
                    
                    while scan_pos < len(content) and branch_depth > 0:
                        s = content.find(bs, scan_pos)
                        if s == -1:
                            raise TemplateSyntaxError(f"Unclosed if at {block_pos}")
                        e = content.find(be, s)
                        if e == -1:
                            raise TemplateSyntaxError(f"Unclosed tag at {s}")
                        t = content[s+2:e].strip()
                        
                        if t.startswith('if '):
                            branch_depth += 1
                        elif t == 'endif':
                            branch_depth -= 1
                            if branch_depth == 0:
                                # Update last branch with final content
                                if branches:
                                    branches[-1] = (branches[-1][0], content[current_pos:s])
                                else:
                                    branches.append((cond, content[current_pos:s]))
                                scan_pos = e + 2  # Move past endif
                                break
                        elif branch_depth == 1:
                            if t.startswith('elif '):
                                # Update the last branch with its content
                                if branches:
                                    branches[-1] = (branches[-1][0], content[current_pos:s])
                                else:
                                    branches.append((cond, content[current_pos:s]))
                                # Add new elif branch
                                branches.append((t[5:].strip(), ''))
                                current_pos = e + 2
                            elif t == 'else':
                                # Update the last branch with its content
                                if branches:
                                    branches[-1] = (branches[-1][0], content[current_pos:s])
                                else:
                                    branches.append((cond, content[current_pos:s]))
                                # Add else branch
                                branches.append((None, ''))
                                current_pos = e + 2
                        scan_pos = e + 2
                    
                    # Render matching branch
                    rendered = ""
                    for b_cond, b_content in branches:
                        if b_cond is None or self._eval_condition(b_cond, context):
                            rendered = self._render(b_content, context, depth + 1)
                            break
                    result.append(rendered)
                    pos = scan_pos
                
                elif tag.startswith('for '):
                    # Parse: for var in iterable
                    match = re.match(r'(\w+(?:\s*,\s*\w+)?)\s+in\s+(.+)', tag[4:])
                    if not match:
                        raise TemplateSyntaxError(f"Invalid for: {tag}")
                    loop_vars, iterable_expr = match.groups()
                    body_start = end + 2
                    
                    # Find matching endfor
                    endfor_start, endfor_end = self._find_matching_end(content, body_start, 'for', 'endfor')
                    if endfor_start == -1:
                        raise TemplateSyntaxError(f"Unclosed for at {block_pos}")
                    
                    loop_body = content[body_start:endfor_start]
                    iterable = self._resolve_value(iterable_expr.strip(), context)
                    
                    if iterable:
                        if isinstance(iterable, dict):
                            iterable = list(iterable.items())
                        elif not isinstance(iterable, (list, tuple)):
                            iterable = list(iterable) if hasattr(iterable, '__iter__') else []
                        
                        var_parts = [v.strip() for v in loop_vars.split(',')] if ',' in loop_vars else [loop_vars.strip()]
                        
                        for idx, item in enumerate(iterable):
                            if idx >= 1000:
                                raise TemplateRenderError("Max loop iterations exceeded")
                            loop_ctx = dict(context)
                            if len(var_parts) == 1:
                                loop_ctx[var_parts[0]] = item
                            elif isinstance(item, (tuple, list)) and len(item) >= len(var_parts):
                                for k, v in enumerate(var_parts):
                                    loop_ctx[v] = item[k]
                            else:
                                loop_ctx[var_parts[0]] = item
                            loop_ctx['loop'] = {'index': idx+1, 'index0': idx, 'first': idx==0, 'last': idx==len(iterable)-1, 'length': len(iterable)}
                            result.append(self._render(loop_body, loop_ctx, depth + 1))
                    
                    pos = endfor_end
                
                elif tag.startswith('include '):
                    include_name = tag[8:].strip().strip("'\"")
                    try:
                        included = self.loader(include_name)
                        result.append(self._render(included, context, depth + 1))
                    except TemplateNotFoundError:
                        pass
                    pos = end + 2
                
                else:
                    pos = end + 2
        
        return ''.join(result)
    
    def _process_vars(self, content, context):
        vs, ve = "{{", "}}"
        pattern = re.compile(r'\{\{\s*(.+?)\s*\}\}')
        def repl(m):
            value = self._resolve_variable(m.group(1), context)
            if value is None:
                return ""
            if self.autoescape:
                value = str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
            return str(value)
        return pattern.sub(repl, content)
    
    def _parse_blocks(self, content):
        blocks = {}
        pattern = re.compile(r'\{%\s*block\s+(\w+)\s*%\}')
        result = []
        pos = 0
        
        while pos < len(content):
            m = pattern.search(content, pos)
            if not m:
                result.append(content[pos:])
                break
            result.append(content[pos:m.start()])
            block_name = m.group(1)
            body_start = m.end()
            endblock_start, endblock_end = self._find_matching_end(content, body_start, 'block', 'endblock')
            if endblock_start == -1:
                raise TemplateSyntaxError(f"Unclosed block: {block_name}")
            blocks[block_name] = content[body_start:endblock_start]
            result.append(f"<!-- BLOCK:{block_name} -->")
            pos = endblock_end
        
        return blocks, ''.join(result)
    
    def render(self, template, context=None):
        context = dict(context or {})
        context.update(self._globals)
        
        # Check for extends
        match = re.search(r'\{%\s*extends\s+["\'](.+?)["\']\s*%\}', template)
        if match:
            base = self.loader(match.group(1))
            child_blocks, _ = self._parse_blocks(template)
            base_blocks, base_content = self._parse_blocks(base)
            merged = {**base_blocks, **child_blocks}
            for name, content in merged.items():
                base_content = base_content.replace(f"<!-- BLOCK:{name} -->", content)
            template = base_content
        
        return self._render(template, context)
    
    def render_file(self, name, context=None):
        return self.render(self.loader(name), context)


# Module-level functions
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = TemplateEngine()
    return _engine

def render(template, context=None):
    return get_engine().render(template, context)

def render_file(name, context=None):
    return get_engine().render_file(name, context)

def register_filter(name, func):
    get_engine().register_filter(name, func)

def set_globals(**kwargs):
    get_engine().set_globals(**kwargs)

def set_loader(loader):
    get_engine().set_loader(loader)

def set_autoescape(enabled=True):
    get_engine().autoescape = enabled
