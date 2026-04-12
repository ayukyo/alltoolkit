"""
AllToolkit - Template Utils Advanced Examples

Advanced examples demonstrating template inheritance, includes,
code generation, and complex scenarios.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import TemplateEngine, TemplateConfig, render


def demo_template_inheritance():
    """Demonstrate template inheritance with extends/block."""
    print("=" * 60)
    print("Template Inheritance Demo")
    print("=" * 60)
    print()
    
    engine = TemplateEngine()
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create base template
        base_path = os.path.join(temp_dir, "base.html")
        with open(base_path, 'w') as f:
            f.write("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}默认标题{% endblock %}</title>
    {% block head_extra %}{% endblock %}
</head>
<body>
    <header>
        <nav>
            <a href="/">首页</a>
            <a href="/about">关于</a>
            <a href="/contact">联系</a>
        </nav>
    </header>
    
    <main>
        {% block content %}
        <p>默认内容</p>
        {% endblock %}
    </main>
    
    <footer>
        <p>&copy; {{ year }} {{ site_name }}. All rights reserved.</p>
    </footer>
</body>
</html>""")
        
        # Create home page template
        home_path = os.path.join(temp_dir, "home.html")
        with open(home_path, 'w') as f:
            f.write("""{% extends "base.html" %}
{% block title %}首页 - {{ site_name }}{% endblock %}
{% block content %}
<h1>欢迎来到{{ site_name }}</h1>
<p>这是一个使用模板继承的示例页面。</p>
<div class="features">
    {% for feature in features %}
    <div class="feature">
        <h3>{{ feature.title }}</h3>
        <p>{{ feature.description }}</p>
    </div>
    {% endfor %}
</div>
{% endblock %}""")
        
        # Create about page template
        about_path = os.path.join(temp_dir, "about.html")
        with open(about_path, 'w') as f:
            f.write("""{% extends "base.html" %}
{% block title %}关于我们 - {{ site_name }}{% endblock %}
{% block content %}
<h1>关于{{ site_name }}</h1>
<p>{{ description }}</p>
<h2>团队成员</h2>
<ul>
{% for member in team %}
    <li>{{ member.name }} - {{ member.role }}</li>
{% endfor %}
</ul>
{% endblock %}""")
        
        # Set up loader
        engine.set_loader(lambda name: open(os.path.join(temp_dir, name)).read())
        
        # Render home page
        print("Home Page:")
        print("-" * 40)
        home_context = {
            "site_name": "我的网站",
            "year": 2024,
            "features": [
                {"title": "快速", "description": "极速加载"},
                {"title": "安全", "description": "数据加密"},
                {"title": "可靠", "description": "99.9% 可用性"}
            ]
        }
        result = engine.render_file("home.html", home_context)
        print(result[:500] + "..." if len(result) > 500 else result)
        print()
        
        # Render about page
        print("About Page:")
        print("-" * 40)
        about_context = {
            "site_name": "我的网站",
            "year": 2024,
            "description": "我们是一家专注于技术创新的公司。",
            "team": [
                {"name": "张三", "role": "CEO"},
                {"name": "李四", "role": "CTO"},
                {"name": "王五", "role": "设计师"}
            ]
        }
        result = engine.render_file("about.html", about_context)
        print(result[:500] + "..." if len(result) > 500 else result)
        print()
        
    finally:
        shutil.rmtree(temp_dir)


def demo_template_includes():
    """Demonstrate template includes."""
    print("=" * 60)
    print("Template Includes Demo")
    print("=" * 60)
    print()
    
    engine = TemplateEngine()
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create header partial
        with open(os.path.join(temp_dir, "header.html"), 'w') as f:
            f.write("""<header>
    <h1>{{ site_name }}</h1>
    <nav>
        {% for item in nav_items %}
        <a href="{{ item.url }}">{{ item.name }}</a>
        {% endfor %}
    </nav>
</header>""")
        
        # Create footer partial
        with open(os.path.join(temp_dir, "footer.html"), 'w') as f:
            f.write("""<footer>
    <p>&copy; {{ year }} {{ site_name }}</p>
    <p>Powered by AllToolkit</p>
</footer>""")
        
        # Create item card partial
        with open(os.path.join(temp_dir, "item_card.html"), 'w') as f:
            f.write("""<div class="card">
    <h3>{{ item.title }}</h3>
    <p>{{ item.description }}</p>
    <span class="price">{{ item.price | default:'N/A' }}</span>
</div>""")
        
        # Create main page
        with open(os.path.join(temp_dir, "page.html"), 'w') as f:
            f.write("""<!DOCTYPE html>
<html>
<body>
{% include 'header.html' %}

<main>
    <h2>产品列表</h2>
    <div class="grid">
        {% for item in products %}
        {% include 'item_card.html' %}
        {% endfor %}
    </div>
</main>

{% include 'footer.html' %}
</body>
</html>""")
        
        # Set up loader
        engine.set_loader(lambda name: open(os.path.join(temp_dir, name)).read())
        
        # Render page
        context = {
            "site_name": "商城",
            "year": 2024,
            "nav_items": [
                {"name": "首页", "url": "/"},
                {"name": "产品", "url": "/products"},
                {"name": "关于", "url": "/about"}
            ],
            "products": [
                {"title": "产品 A", "description": "描述 A", "price": "¥100"},
                {"title": "产品 B", "description": "描述 B", "price": "¥200"},
                {"title": "产品 C", "description": "描述 C"}  # No price
            ]
        }
        
        result = engine.render_file("page.html", context)
        print(result)
        print()
        
    finally:
        shutil.rmtree(temp_dir)


def demo_code_generation():
    """Demonstrate code generation use case."""
    print("=" * 60)
    print("Code Generation Demo")
    print("=" * 60)
    print()
    
    # Python class generator template
    class_template = """
class {{ class_name }}:
    \"\"\"{{ docstring }}\"\"\"
    
    def __init__(self{% for param in params %}, {{ param.name }}{% if param.default %}={{ param.default }}{% endif %}{% endfor %}):
{% for param in params %}
        self.{{ param.name }} = {{ param.name }}
{% endfor %}
    
{% for method in methods %}
    def {{ method.name }}(self{% for p in method.params %}, {{ p.name }}{% endfor %}){% if method.return_type %} -> {{ method.return_type }}{% endif %}:
        \"\"\"{{ method.doc }}\"\"\"
{% if method.body %}
{{ method.body | indent:8 }}
{% else %}
        pass
{% endif %}

{% endfor %}
""".strip()
    
    context = {
        "class_name": "UserService",
        "docstring": "用户服务类，处理用户相关的业务逻辑",
        "params": [
            {"name": "db", "default": "None"},
            {"name": "cache", "default": "None"}
        ],
        "methods": [
            {
                "name": "get_user",
                "params": [{"name": "user_id"}],
                "return_type": "Optional[User]",
                "doc": "根据 ID 获取用户",
                "body": "        if self.cache:\n            cached = self.cache.get(user_id)\n            if cached:\n                return cached\n        return self.db.query(user_id) if self.db else None"
            },
            {
                "name": "create_user",
                "params": [{"name": "data"}],
                "return_type": "User",
                "doc": "创建新用户",
                "body": "        user = User(**data)\n        if self.db:\n            self.db.save(user)\n        return user"
            },
            {
                "name": "delete_user",
                "params": [{"name": "user_id"}],
                "return_type": "bool",
                "doc": "删除用户",
                "body": None
            }
        ]
    }
    
    result = render(class_template, context)
    print("Generated Python Class:")
    print("-" * 40)
    print(result)
    print()


def demo_html_table():
    """Demonstrate HTML table generation."""
    print("=" * 60)
    print("HTML Table Generation Demo")
    print("=" * 60)
    print()
    
    table_template = """
<table class="data-table">
<thead>
    <tr>
        {% for header in headers %}
        <th>{{ header }}</th>
        {% endfor %}
    </tr>
</thead>
<tbody>
    {% for row in rows %}
    <tr class="{% if loop.index0 % 2 == 0 %}even{% else %}odd{% endif %}">
        {% for cell in row %}
        <td>{{ cell }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
</tbody>
<tfoot>
    <tr>
        <td colspan="{{ headers | length }}">共 {{ rows | length }} 条记录</td>
    </tr>
</tfoot>
</table>
""".strip()
    
    context = {
        "headers": ["姓名", "年龄", "城市", "职业"],
        "rows": [
            ["张三", 28, "北京", "工程师"],
            ["李四", 32, "上海", "设计师"],
            ["王五", 25, "广州", "产品经理"],
            ["赵六", 35, "深圳", "数据科学家"],
            ["钱七", 30, "杭州", "前端开发"]
        ]
    }
    
    result = render(table_template, context)
    print(result)
    print()


def demo_config_generation():
    """Demonstrate configuration file generation."""
    print("=" * 60)
    print("Configuration File Generation Demo")
    print("=" * 60)
    print()
    
    # Nginx config template
    nginx_template = """
# Auto-generated Nginx configuration
# Generated by AllToolkit Template Utils

upstream backend {
{% for server in servers %}
    server {{ server.host }}:{{ server.port }} weight={{ server.weight | default:1 }};
{% endfor %}
}

server {
    listen {{ port }};
    server_name {{ domain }};
    
{% if ssl_enabled %}
    ssl_certificate {{ ssl_cert }};
    ssl_certificate_key {{ ssl_key }};
{% endif %}
    
    root {{ root_path }};
    index index.html index.htm;
    
    # Logging
    access_log {{ log_path }}/access.log;
    error_log {{ log_path }}/error.log;
    
{% for location in locations %}
    location {{ location.path }} {
{% if location.proxy_pass %}
        proxy_pass {{ location.proxy_pass }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
{% endif %}
{% if location.root %}
        root {{ location.root }};
{% endif %}
{% if location.try_files %}
        try_files {{ location.try_files }};
{% endif %}
    }
{% endfor %}
}
""".strip()
    
    context = {
        "port": 80,
        "domain": "example.com",
        "ssl_enabled": True,
        "ssl_cert": "/etc/ssl/certs/example.crt",
        "ssl_key": "/etc/ssl/private/example.key",
        "root_path": "/var/www/html",
        "log_path": "/var/log/nginx",
        "servers": [
            {"host": "127.0.0.1", "port": 8000, "weight": 3},
            {"host": "127.0.0.1", "port": 8001, "weight": 2},
            {"host": "127.0.0.1", "port": 8002, "weight": 1}
        ],
        "locations": [
            {"path": "/", "try_files": "$uri $uri/ /index.html"},
            {"path": "/api", "proxy_pass": "http://backend"},
            {"path": "/static", "root": "/var/www/static"}
        ]
    }
    
    result = render(nginx_template, context)
    print(result)
    print()


def demo_sql_generation():
    """Demonstrate SQL query generation."""
    print("=" * 60)
    print("SQL Query Generation Demo")
    print("=" * 60)
    print()
    
    select_template = """
SELECT
{% for column in columns %}
    {{ column }}{% if not loop.last %},{% endif %}
{% endfor %}
FROM {{ table }}
{% if where_conditions %}
WHERE
{% for cond in where_conditions %}
    {{ cond.field }} {{ cond.op }} {{ cond.value }}{% if not loop.last %} AND{% endif %}
{% endfor %}
{% endif %}
{% if order_by %}
ORDER BY {{ order_by }} {{ order_direction | default:'ASC' }}
{% endif %}
{% if limit %}
LIMIT {{ limit }}
{% endif %}
{% if offset %}
OFFSET {{ offset }}
{% endif %}
;
""".strip()
    
    context = {
        "columns": ["u.id", "u.name", "u.email", "o.total"],
        "table": "users u",
        "where_conditions": [
            {"field": "u.status", "op": "=", "value": "'active'"},
            {"field": "u.created_at", "op": ">=", "value": "'2024-01-01'"}
        ],
        "order_by": "o.total",
        "order_direction": "DESC",
        "limit": 100,
        "offset": 0
    }
    
    result = render(select_template, context)
    print("Generated SQL:")
    print("-" * 40)
    print(result)
    print()


def demo_report_generation():
    """Demonstrate report generation."""
    print("=" * 60)
    print("Report Generation Demo")
    print("=" * 60)
    print()
    
    report_template = """
# {{ report.title }}

**生成时间**: {{ report.date }}
**报告周期**: {{ report.period }}

---

## 执行摘要

{% if report.summary %}
{{ report.summary }}
{% else %}
暂无摘要
{% endif %}

## 关键指标

| 指标 | 当前值 | 目标值 | 完成率 |
|------|--------|--------|--------|
{% for metric in metrics %}
| {{ metric.name }} | {{ metric.current }} | {{ metric.target }} | {{ metric.rate }}% |
{% endfor %}

## 详细数据

{% for section in sections %}
### {{ section.title }}

{{ section.description }}

{% if section.data %}
| 项目 | 数值 | 占比 |
|------|------|------|
{% for item in section.data %}
| {{ item.name }} | {{ item.value }} | {{ item.percentage }}% |
{% endfor %}
{% endif %}

{% endfor %}

## 建议

{% for recommendation in recommendations %}
{{ loop.index }}. {{ recommendation }}
{% endfor %}

---

*本报告由 AllToolkit Template Utils 自动生成*
""".strip()
    
    context = {
        "report": {
            "title": "2024 年第一季度销售报告",
            "date": "2024-04-01",
            "period": "2024 Q1",
            "summary": "本季度销售额同比增长 25%，超额完成目标。主要增长来自华东地区和新产品线。"
        },
        "metrics": [
            {"name": "总销售额", "current": "¥1,250 万", "target": "¥1,000 万", "rate": 125},
            {"name": "新客户", "current": "350", "target": "300", "rate": 117},
            {"name": "转化率", "current": "3.2%", "target": "3.0%", "rate": 107}
        ],
        "sections": [
            {
                "title": "区域销售",
                "description": "各区域销售表现如下：",
                "data": [
                    {"name": "华东", "value": "¥500 万", "percentage": 40},
                    {"name": "华北", "value": "¥375 万", "percentage": 30},
                    {"name": "华南", "value": "¥250 万", "percentage": 20},
                    {"name": "其他", "value": "¥125 万", "percentage": 10}
                ]
            },
            {
                "title": "产品线",
                "description": "各产品线贡献：",
                "data": [
                    {"name": "产品 A", "value": "¥625 万", "percentage": 50},
                    {"name": "产品 B", "value": "¥375 万", "percentage": 30},
                    {"name": "产品 C", "value": "¥250 万", "percentage": 20}
                ]
            }
        ],
        "recommendations": [
            "继续加大华东地区市场投入",
            "加快产品 C 的推广力度",
            "优化销售流程，提高转化率",
            "建立客户回访机制，提高复购率"
        ]
    }
    
    result = render(report_template, context)
    print(result)
    print()


def main():
    """Run all demos."""
    demo_template_inheritance()
    demo_template_includes()
    demo_code_generation()
    demo_html_table()
    demo_config_generation()
    demo_sql_generation()
    demo_report_generation()
    
    print("=" * 60)
    print("All demos completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
