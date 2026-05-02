#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Fake Data Utilities Module

Generate realistic fake/mock data for testing and development.
Zero external dependencies - uses only Python stdlib.

Author: AllToolkit
License: MIT
"""

import random
import string
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple, Union

# =============================================================================
# Constants
# =============================================================================

# Chinese family names (common ones)
CHINESE_SURNAMES = [
    '王', '李', '张', '刘', '陈', '杨', '黄', '赵', '吴', '周',
    '徐', '孙', '马', '胡', '朱', '郭', '何', '林', '罗', '高',
    '郑', '梁', '谢', '宋', '唐', '许', '邓', '冯', '韩', '曹',
    '曾', '彭', '萧', '蔡', '潘', '田', '董', '袁', '于', '余',
    '叶', '蒋', '杜', '苏', '魏', '程', '吕', '丁', '沈', '任',
]

# Chinese given names (common characters with positive meanings)
CHINESE_GIVEN_NAMES = [
    '伟', '芳', '娜', '敏', '静', '丽', '强', '磊', '军', '洋',
    '勇', '艳', '杰', '娟', '涛', '明', '超', '秀英', '霞', '平',
    '刚', '桂英', '华', '玲', '红', '梅', '鑫', '燕', '辉', '林',
    '宇', '婷', '建', '浩', '雪', '飞', '亮', '欣', '颖', '昊',
    '思', '雨', '佳', '梦', '阳', '航', '逸', '晨', '睿', '泽',
    '文', '博', '晓', '乐', '怡', '嘉', '俊', '泽', '宸', '逸',
]

# English first names
ENGLISH_FIRST_NAMES_MALE = [
    'James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard',
    'Joseph', 'Thomas', 'Christopher', 'Charles', 'Daniel', 'Matthew',
    'Anthony', 'Mark', 'Donald', 'Steven', 'Paul', 'Andrew', 'Joshua',
    'Kenneth', 'Kevin', 'Brian', 'George', 'Timothy', 'Ronald', 'Edward',
    'Jason', 'Jeffrey', 'Ryan', 'Jacob', 'Gary', 'Nicholas', 'Eric',
    'Jonathan', 'Stephen', 'Larry', 'Justin', 'Scott', 'Brandon', 'Benjamin',
    'Samuel', 'Raymond', 'Gregory', 'Frank', 'Alexander', 'Patrick', 'Jack',
    'Dennis', 'Jerry', 'Tyler', 'Aaron', 'Jose', 'Adam', 'Nathan', 'Henry',
    'Douglas', 'Zachary', 'Peter', 'Kyle', 'Noah', 'Ethan', 'Wyatt', 'Oliver',
]

ENGLISH_FIRST_NAMES_FEMALE = [
    'Mary', 'Patricia', 'Jennifer', 'Linda', 'Barbara', 'Elizabeth',
    'Susan', 'Jessica', 'Sarah', 'Karen', 'Lisa', 'Nancy', 'Betty',
    'Margaret', 'Sandra', 'Ashley', 'Kimberly', 'Emily', 'Donna',
    'Michelle', 'Dorothy', 'Carol', 'Amanda', 'Melissa', 'Deborah',
    'Stephanie', 'Rebecca', 'Sharon', 'Laura', 'Cynthia', 'Kathleen',
    'Amy', 'Angela', 'Shirley', 'Anna', 'Brenda', 'Pamela', 'Emma',
    'Nicole', 'Helen', 'Samantha', 'Katherine', 'Christine', 'Debra',
    'Rachel', 'Carolyn', 'Janet', 'Catherine', 'Maria', 'Heather',
    'Diane', 'Ruth', 'Julie', 'Olivia', 'Joyce', 'Virginia', 'Victoria',
    'Kelly', 'Lauren', 'Christina', 'Joan', 'Evelyn', 'Julia', 'Megan',
]

# English last names
ENGLISH_LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
    'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
    'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
    'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark',
    'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King',
    'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green',
    'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
    'Carter', 'Roberts', 'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz',
    'Parker', 'Cruz', 'Edwards', 'Collins', 'Reyes', 'Stewart', 'Morris',
]

# Company names (prefixes, suffixes, types)
COMPANY_PREFIXES = [
    'Global', 'United', 'National', 'International', 'Pacific', 'Atlantic',
    'American', 'Euro', 'Asian', 'Tech', 'Smart', 'Digital', 'Cloud',
    'Cyber', 'Alpha', 'Beta', 'Omega', 'Prime', 'Elite', 'Pro', 'Advanced',
    'Modern', 'Future', 'Innovative', 'Creative', 'Dynamic', 'Apex', 'Core',
    'Green', 'Blue', 'Red', 'Silver', 'Golden', 'Phoenix', 'Dragon',
]

COMPANY_TYPES = [
    'Technologies', 'Solutions', 'Systems', 'Industries', 'Corporation',
    'Enterprises', 'Group', 'Holdings', 'Partners', 'Associates', 'Consulting',
    'Services', 'Software', 'Labs', 'Research', 'Development', 'Networks',
    'Communications', 'Electronics', 'Manufacturing', 'Engineering',
]

COMPANY_SUFFIXES = ['Inc.', 'LLC', 'Ltd.', 'Corp.', 'Co.', 'GmbH', 'AG', 'PLC']

# Street names
STREET_NAMES = [
    'Main', 'Oak', 'Pine', 'Maple', 'Cedar', 'Elm', 'Washington', 'Lake',
    'Hill', 'Park', 'First', 'Second', 'Third', 'Fourth', 'Fifth', 'River',
    'Valley', 'Forest', 'Meadow', 'Highland', 'Spring', 'View', 'Sunny',
    'Green', 'Blue', 'Red', 'White', 'Black', 'Brown', 'Church', 'School',
]

STREET_TYPES = ['St', 'Ave', 'Blvd', 'Rd', 'Ln', 'Dr', 'Way', 'Ct', 'Pl', 'Cir']

# City names
US_CITIES = [
    'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
    'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
    'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco', 'Indianapolis',
    'Seattle', 'Denver', 'Washington', 'Boston', 'El Paso', 'Detroit',
    'Nashville', 'Portland', 'Memphis', 'Oklahoma City', 'Las Vegas',
    'Louisville', 'Baltimore', 'Milwaukee', 'Albuquerque', 'Tucson', 'Fresno',
    'Sacramento', 'Kansas City', 'Long Beach', 'Mesa', 'Atlanta', 'Colorado Springs',
]

CHINESE_CITIES = [
    '北京', '上海', '广州', '深圳', '杭州', '南京', '苏州', '成都', '武汉', '西安',
    '重庆', '天津', '青岛', '大连', '宁波', '厦门', '长沙', '郑州', '沈阳', '哈尔滨',
    '济南', '福州', '昆明', '南宁', '合肥', '南昌', '贵阳', '太原', '石家庄', '兰州',
]

# Country codes
COUNTRY_CODES = ['US', 'CN', 'UK', 'DE', 'FR', 'JP', 'KR', 'AU', 'CA', 'IT', 'ES', 'BR', 'IN', 'RU', 'MX']

# Job titles
JOB_TITLES = [
    'Software Engineer', 'Data Scientist', 'Product Manager', 'Project Manager',
    'UX Designer', 'UI Designer', 'DevOps Engineer', 'Backend Developer',
    'Frontend Developer', 'Full Stack Developer', 'Mobile Developer', 'QA Engineer',
    'System Administrator', 'Database Administrator', 'Security Engineer',
    'Machine Learning Engineer', 'Cloud Architect', 'Technical Lead', 'CTO',
    'Engineering Manager', 'Scrum Master', 'Business Analyst', 'Consultant',
    'Marketing Manager', 'Sales Manager', 'HR Manager', 'Finance Manager',
    'Operations Manager', 'Executive Assistant', 'Customer Success Manager',
]

# Industries
INDUSTRIES = [
    'Technology', 'Finance', 'Healthcare', 'Education', 'Retail', 'Manufacturing',
    'Entertainment', 'Media', 'Real Estate', 'Transportation', 'Energy',
    'Telecommunications', 'Agriculture', 'Pharmaceuticals', 'Aerospace',
    'Automotive', 'Construction', 'Hospitality', 'Food & Beverage', 'Legal',
]

# Product categories and products
PRODUCT_CATEGORIES = {
    'Electronics': [
        ('Smartphone', 299, 1299),
        ('Laptop', 499, 2499),
        ('Tablet', 199, 999),
        ('Smart Watch', 99, 499),
        ('Wireless Earbuds', 29, 299),
        ('Bluetooth Speaker', 19, 199),
        ('Monitor', 149, 899),
        ('Keyboard', 29, 199),
        ('Mouse', 15, 99),
        ('USB Hub', 9, 49),
    ],
    'Clothing': [
        ('T-Shirt', 9, 49),
        ('Jeans', 29, 149),
        ('Dress', 39, 299),
        ('Jacket', 49, 399),
        ('Sweater', 29, 149),
        ('Shorts', 19, 79),
        ('Sneakers', 49, 249),
        ('Boots', 79, 399),
        ('Hat', 15, 59),
        ('Scf', 19, 89),
    ],
    'Home & Garden': [
        ('Desk Lamp', 19, 99),
        ('Chair', 49, 499),
        ('Table', 79, 599),
        ('Sofa', 299, 1999),
        ('Bed Frame', 149, 999),
        ('Mattress', 199, 1499),
        ('Rug', 29, 299),
        ('Plant Pot', 9, 49),
        ('Wall Art', 19, 199),
        ('Clock', 15, 79),
    ],
    'Books': [
        ('Fiction Novel', 9, 29),
        ('Textbook', 29, 199),
        ('Cookbook', 15, 49),
        ('Biography', 12, 35),
        ('Self-Help Book', 10, 29),
        ('Science Fiction', 9, 25),
        ('Mystery Novel', 9, 25),
        ('Children Book', 5, 19),
        ('Art Book', 25, 99),
        ('Travel Guide', 12, 29),
    ],
    'Sports': [
        ('Basketball', 15, 59),
        ('Football', 15, 49),
        ('Tennis Racket', 29, 249),
        ('Golf Club Set', 199, 1499),
        ('Yoga Mat', 15, 79),
        ('Dumbbells', 29, 199),
        ('Jump Rope', 5, 29),
        ('Water Bottle', 9, 49),
        ('Running Shoes', 59, 249),
        ('Fitness Tracker', 49, 299),
    ],
}

# Common file extensions by category
FILE_EXTENSIONS = {
    'image': ['.jpg', '.png', '.gif', '.webp', '.svg', '.bmp'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
    'spreadsheet': ['.xls', '.xlsx', '.csv', '.ods'],
    'presentation': ['.ppt', '.pptx', '.odp'],
    'video': ['.mp4', '.avi', '.mov', '.mkv', '.webm'],
    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
    'archive': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'code': ['.py', '.js', '.ts', '.java', '.cpp', '.go', '.rs', '.rb'],
    'data': ['.json', '.xml', '.yaml', '.yml', '.toml', '.ini'],
    'executable': ['.exe', '.msi', '.dmg', '.app', '.deb', '.rpm'],
}

# HTTP status codes with descriptions
HTTP_STATUS_CODES = {
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    204: 'No Content',
    301: 'Moved Permanently',
    302: 'Found',
    304: 'Not Modified',
    307: 'Temporary Redirect',
    308: 'Permanent Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    429: 'Too Many Requests',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
}

# User agents (common browsers)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
]

# Common HTTP methods
HTTP_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']

# Common API paths
API_PATHS = [
    '/api/users', '/api/users/{id}', '/api/posts', '/api/posts/{id}',
    '/api/comments', '/api/products', '/api/products/{id}', '/api/orders',
    '/api/auth/login', '/api/auth/register', '/api/auth/logout',
    '/api/profile', '/api/settings', '/api/search', '/api/upload',
]


# =============================================================================
# Internal Helpers
# =============================================================================

def _random_choice(seq):
    """Choose a random element from a sequence."""
    return random.choice(seq)

def _random_int(lower, upper):
    """Generate a random integer in [lower, upper]."""
    return random.randint(lower, upper)

def _random_float(lower, upper, decimals=2):
    """Generate a random float in [lower, upper] with specified decimals."""
    return round(random.uniform(lower, upper), decimals)

def _random_string(length, charset=None):
    """Generate a random string of specified length."""
    if charset is None:
        charset = string.ascii_lowercase + string.digits
    return ''.join(random.choice(charset) for _ in range(length))


# =============================================================================
# Person Data
# =============================================================================

def fake_name(lang: str = 'en', gender: str = None) -> str:
    """
    Generate a fake name.
    
    Args:
        lang: Language ('en' for English, 'zh' for Chinese)
        gender: Gender ('male' or 'female', None for random)
        
    Returns:
        Full name string
        
    Example:
        >>> name = fake_name()
        >>> len(name) > 0
        True
    """
    if gender is None:
        gender = _random_choice(['male', 'female'])
    
    if lang == 'zh':
        surname = _random_choice(CHINESE_SURNAMES)
        given = _random_choice(CHINESE_GIVEN_NAMES)
        return surname + given
    else:
        if gender == 'male':
            first = _random_choice(ENGLISH_FIRST_NAMES_MALE)
        else:
            first = _random_choice(ENGLISH_FIRST_NAMES_FEMALE)
        last = _random_choice(ENGLISH_LAST_NAMES)
        return f"{first} {last}"


def fake_first_name(lang: str = 'en', gender: str = None) -> str:
    """
    Generate a fake first name.
    
    Args:
        lang: Language ('en' or 'zh')
        gender: Gender ('male' or 'female', None for random)
        
    Returns:
        First name string
    """
    if gender is None:
        gender = _random_choice(['male', 'female'])
    
    if lang == 'zh':
        return _random_choice(CHINESE_GIVEN_NAMES)
    else:
        if gender == 'male':
            return _random_choice(ENGLISH_FIRST_NAMES_MALE)
        else:
            return _random_choice(ENGLISH_FIRST_NAMES_FEMALE)


def fake_last_name(lang: str = 'en') -> str:
    """
    Generate a fake last name.
    
    Args:
        lang: Language ('en' or 'zh')
        
    Returns:
        Last name string
    """
    if lang == 'zh':
        return _random_choice(CHINESE_SURNAMES)
    else:
        return _random_choice(ENGLISH_LAST_NAMES)


def fake_gender() -> str:
    """Generate a random gender."""
    return _random_choice(['male', 'female'])


def fake_age(min_age: int = 18, max_age: int = 80) -> int:
    """Generate a random age."""
    return _random_int(min_age, max_age)


def fake_birthday(min_age: int = 18, max_age: int = 80, format: str = '%Y-%m-%d') -> str:
    """
    Generate a fake birthday.
    
    Args:
        min_age: Minimum age
        max_age: Maximum age
        format: Date format string
        
    Returns:
        Birthday string
    """
    today = datetime.now()
    max_year = today.year - min_age
    min_year = today.year - max_age
    year = _random_int(min_year, max_year)
    month = _random_int(1, 12)
    
    # Handle days based on month
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = _random_int(1, 31)
    elif month in [4, 6, 9, 11]:
        day = _random_int(1, 30)
    else:
        # February - simplified
        day = _random_int(1, 28)
    
    return f"{year:04d}-{month:02d}-{day:02d}"


# =============================================================================
# Contact Data
# =============================================================================

def fake_email(domain: str = None, lang: str = 'en') -> str:
    """
    Generate a fake email address.
    
    Args:
        domain: Email domain (random if None)
        lang: Language for name part
        
    Returns:
        Email address string
    """
    common_domains = [
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
        'icloud.com', 'mail.com', 'protonmail.com', 'qq.com',
    ]
    
    if domain is None:
        domain = _random_choice(common_domains)
    
    name = fake_name(lang).lower().replace(' ', '.')
    random_suffix = _random_string(4, string.digits)
    return f"{name}{random_suffix}@{domain}"


def fake_phone(country: str = 'US') -> str:
    """
    Generate a fake phone number.
    
    Args:
        country: Country code ('US', 'CN', 'UK', etc.)
        
    Returns:
        Phone number string
    """
    if country == 'CN':
        # Chinese mobile number (starts with 1)
        prefix = _random_choice(['138', '139', '150', '151', '152', '158', '159', '186', '187', '188'])
        suffix = _random_string(8, string.digits)
        return f"{prefix}{suffix}"
    elif country == 'UK':
        # UK mobile (starts with 07)
        return f"07{_random_string(9, string.digits)}"
    elif country == 'DE':
        # German mobile
        return f"+49{_random_string(10, string.digits)}"
    else:
        # US phone number
        area_code = _random_int(200, 999)
        prefix = _random_int(100, 999)
        line = _random_int(1000, 9999)
        return f"({area_code}) {prefix}-{line}"


def fake_address(lang: str = 'en') -> Dict[str, str]:
    """
    Generate a fake address.
    
    Args:
        lang: Language ('en' or 'zh')
        
    Returns:
        Dictionary with address components
    """
    if lang == 'zh':
        city = _random_choice(CHINESE_CITIES)
        district = _random_string(3, string.digits) + '路'
        number = _random_int(1, 999)
        return {
            'street': f"{city}市{district}{number}号",
            'city': city,
            'zipcode': _random_string(6, string.digits),
            'country': '中国',
        }
    else:
        street_num = _random_int(1, 9999)
        street_name = _random_choice(STREET_NAMES)
        street_type = _random_choice(STREET_TYPES)
        city = _random_choice(US_CITIES)
        state = _random_string(2, string.ascii_uppercase)
        zipcode = _random_string(5, string.digits)
        
        return {
            'street': f"{street_num} {street_name} {street_type}",
            'city': city,
            'state': state,
            'zipcode': zipcode,
            'country': 'United States',
        }


def fake_full_address(lang: str = 'en') -> str:
    """Generate a complete address string."""
    addr = fake_address(lang)
    if lang == 'zh':
        return addr['street']
    else:
        return f"{addr['street']}, {addr['city']}, {addr['state']} {addr['zipcode']}"


# =============================================================================
# Internet Data
# =============================================================================

def fake_url(secure: bool = True, domain: str = None, path: str = None) -> str:
    """
    Generate a fake URL.
    
    Args:
        secure: Use HTTPS
        domain: Custom domain
        path: Custom path
        
    Returns:
        URL string
    """
    protocol = 'https' if secure else 'http'
    
    if domain is None:
        name = _random_string(_random_int(5, 12), string.ascii_lowercase)
        tld = _random_choice(['com', 'net', 'org', 'io', 'co', 'app', 'dev'])
        domain = f"{name}.{tld}"
    
    if path is None:
        path_parts = _random_int(0, 3)
        path = ''
        for _ in range(path_parts):
            path += '/' + _random_string(_random_int(3, 8), string.ascii_lowercase)
        if path_parts > 0 and random.random() > 0.5:
            path += '.' + _random_choice(['html', 'php', 'json', 'xml'])
    
    return f"{protocol}://{domain}{path if path else '/'}"


def fake_domain() -> str:
    """Generate a fake domain name."""
    name = _random_string(_random_int(5, 12), string.ascii_lowercase)
    tld = _random_choice(['com', 'net', 'org', 'io', 'co', 'app', 'dev', 'tech'])
    return f"{name}.{tld}"


def fake_ipv4(private: bool = False) -> str:
    """
    Generate a fake IPv4 address.
    
    Args:
        private: Generate private IP address
        
    Returns:
        IPv4 address string
    """
    if private:
        range_type = _random_int(1, 3)
        if range_type == 1:
            return f"10.{_random_int(0, 255)}.{_random_int(0, 255)}.{_random_int(1, 254)}"
        elif range_type == 2:
            return f"172.{_random_int(16, 31)}.{_random_int(0, 255)}.{_random_int(1, 254)}"
        else:
            return f"192.168.{_random_int(0, 255)}.{_random_int(1, 254)}"
    else:
        return f"{_random_int(1, 223)}.{_random_int(0, 255)}.{_random_int(0, 255)}.{_random_int(1, 254)}"


def fake_ipv6() -> str:
    """Generate a fake IPv6 address."""
    parts = [_random_string(4, string.hexdigits.lower()) for _ in range(8)]
    return ':'.join(parts)


def fake_mac_address() -> str:
    """Generate a fake MAC address."""
    parts = [_random_string(2, string.hexdigits.upper()) for _ in range(6)]
    return ':'.join(parts)


def fake_user_agent() -> str:
    """Generate a random user agent string."""
    return _random_choice(USER_AGENTS)


def fake_http_method() -> str:
    """Generate a random HTTP method."""
    return _random_choice(HTTP_METHODS)


def fake_http_status() -> Tuple[int, str]:
    """Generate a random HTTP status code with description."""
    code = _random_choice(list(HTTP_STATUS_CODES.keys()))
    return code, HTTP_STATUS_CODES[code]


def fake_api_path() -> str:
    """Generate a random API path."""
    path = _random_choice(API_PATHS)
    # Replace {id} with random value
    if '{id}' in path:
        path = path.replace('{id}', str(_random_int(1, 9999)))
    return path


# =============================================================================
# Business Data
# =============================================================================

def fake_company(lang: str = 'en') -> str:
    """
    Generate a fake company name.
    
    Args:
        lang: Language ('en' or 'zh')
        
    Returns:
        Company name string
    """
    if lang == 'zh':
        prefix = _random_choice(['华', '中', '大', '新', '国', '东方', '金山', '银河', '神州', '天创'])
        type_ = _random_choice(['科技', '网络', '信息', '电子', '软件', '数据', '云计算', '智能'])
        suffix = _random_choice(['有限公司', '股份有限公司', '集团', '公司'])
        return prefix + type_ + suffix
    else:
        prefix = _random_choice(COMPANY_PREFIXES)
        type_ = _random_choice(COMPANY_TYPES)
        suffix = _random_choice(COMPANY_SUFFIXES + [''])
        return f"{prefix} {type_} {suffix}".strip()


def fake_job_title() -> str:
    """Generate a fake job title."""
    return _random_choice(JOB_TITLES)


def fake_industry() -> str:
    """Generate a fake industry."""
    return _random_choice(INDUSTRIES)


def fake_salary(min_val: int = 30000, max_val: int = 200000) -> int:
    """
    Generate a fake annual salary.
    
    Args:
        min_val: Minimum salary
        max_val: Maximum salary
        
    Returns:
        Salary amount
    """
    # Round to nearest 1000
    return round(random.uniform(min_val, max_val) / 1000) * 1000


def fake_department() -> str:
    """Generate a fake department name."""
    departments = [
        'Engineering', 'Marketing', 'Sales', 'Human Resources', 'Finance',
        'Operations', 'Customer Support', 'Research', 'Development',
        'Quality Assurance', 'Legal', 'Administration', 'IT', 'Design',
        'Product Management', 'Business Development', 'Analytics',
    ]
    return _random_choice(departments)


# =============================================================================
# Product Data
# =============================================================================

def fake_product(category: str = None) -> Dict[str, Any]:
    """
    Generate a fake product.
    
    Args:
        category: Product category (random if None)
        
    Returns:
        Dictionary with product info
    """
    if category is None:
        category = _random_choice(list(PRODUCT_CATEGORIES.keys()))
    
    if category not in PRODUCT_CATEGORIES:
        category = _random_choice(list(PRODUCT_CATEGORIES.keys()))
    
    product_name, min_price, max_price = _random_choice(PRODUCT_CATEGORIES[category])
    price = _random_float(min_price, max_price)
    
    return {
        'name': product_name,
        'category': category,
        'price': price,
        'currency': 'USD',
        'sku': fake_sku(),
        'in_stock': random.random() > 0.2,
        'rating': _random_float(1.0, 5.0, 1),
        'reviews': _random_int(0, 10000),
    }


def fake_product_name(category: str = None) -> str:
    """Generate a fake product name."""
    product = fake_product(category)
    return product['name']


def fake_price(min_val: float = 1.0, max_val: float = 1000.0, currency: str = 'USD') -> str:
    """Generate a fake price string."""
    price = _random_float(min_val, max_val)
    symbols = {'USD': '$', 'EUR': '€', 'GBP': '£', 'CNY': '¥', 'JPY': '¥'}
    symbol = symbols.get(currency, currency + ' ')
    return f"{symbol}{price:.2f}"


def fake_sku(prefix: str = 'SKU') -> str:
    """Generate a fake SKU."""
    return f"{prefix}-{_random_string(8, string.ascii_uppercase + string.digits)}"


def fake_barcode() -> str:
    """Generate a fake barcode (EAN-13 format)."""
    return _random_string(13, string.digits)


# =============================================================================
# Date/Time Data
# =============================================================================

def fake_date(start_year: int = 2020, end_year: int = None) -> str:
    """
    Generate a fake date.
    
    Args:
        start_year: Start year
        end_year: End year (current year if None)
        
    Returns:
        Date string in YYYY-MM-DD format
    """
    if end_year is None:
        end_year = datetime.now().year
    
    year = _random_int(start_year, end_year)
    month = _random_int(1, 12)
    
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = _random_int(1, 31)
    elif month in [4, 6, 9, 11]:
        day = _random_int(1, 30)
    else:
        day = _random_int(1, 28)
    
    return f"{year:04d}-{month:02d}-{day:02d}"


def fake_time() -> str:
    """Generate a fake time string."""
    hour = _random_int(0, 23)
    minute = _random_int(0, 59)
    second = _random_int(0, 59)
    return f"{hour:02d}:{minute:02d}:{second:02d}"


def fake_datetime(start_year: int = 2020, end_year: int = None) -> str:
    """Generate a fake datetime string."""
    return f"{fake_date(start_year, end_year)} {fake_time()}"


def fake_timestamp(start_year: int = 2020, end_year: int = None) -> int:
    """Generate a fake Unix timestamp."""
    date_str = fake_date(start_year, end_year)
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return int(dt.timestamp())


def fake_timezone() -> str:
    """Generate a fake timezone."""
    timezones = [
        'UTC', 'America/New_York', 'America/Los_Angeles', 'America/Chicago',
        'Europe/London', 'Europe/Paris', 'Europe/Berlin', 'Asia/Tokyo',
        'Asia/Shanghai', 'Asia/Hong_Kong', 'Asia/Singapore', 'Australia/Sydney',
    ]
    return _random_choice(timezones)


# =============================================================================
# Text Data
# =============================================================================

def fake_sentence(min_words: int = 4, max_words: int = 10) -> str:
    """
    Generate a fake sentence.
    
    Args:
        min_words: Minimum words
        max_words: Maximum words
        
    Returns:
        Sentence string
    """
    words = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 
             'adipiscing', 'elit', 'sed', 'do', 'eiusmod', 'tempor', 
             'incididunt', 'ut', 'labore', 'et', 'dolore', 'magna', 
             'aliqua', 'enim', 'ad', 'minim', 'veniam', 'quis', 'nostrud',
             'exercitation', 'ullamco', 'laboris', 'nisi', 'aliquip', 'ex',
             'ea', 'commodo', 'consequat', 'duis', 'aute', 'irure', 'in',
             'reprehenderit', 'voluptate', 'velit', 'esse', 'cillum', 'fugiat',
             'nulla', 'pariatur', 'excepteur', 'sint', 'occaecat', 'cupidatat',
             'non', 'proident', 'sunt', 'culpa', 'qui', 'officia', 'deserunt',
             'mollit', 'anim', 'id', 'est', 'laborum']
    
    num_words = _random_int(min_words, max_words)
    sentence_words = [_random_choice(words) for _ in range(num_words)]
    sentence = ' '.join(sentence_words)
    return sentence.capitalize() + '.'


def fake_paragraph(min_sentences: int = 3, max_sentences: int = 7) -> str:
    """Generate a fake paragraph."""
    num_sentences = _random_int(min_sentences, max_sentences)
    sentences = [fake_sentence() for _ in range(num_sentences)]
    return ' '.join(sentences)


def fake_text(paragraphs: int = 3) -> str:
    """Generate fake text with multiple paragraphs."""
    return '\n\n'.join(fake_paragraph() for _ in range(paragraphs))


def fake_word() -> str:
    """Generate a fake word."""
    words = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 
             'adipiscing', 'elit', 'sed', 'do', 'eiusmod', 'tempor']
    return _random_choice(words)


def fake_title(min_words: int = 2, max_words: int = 6) -> str:
    """Generate a fake title."""
    num_words = _random_int(min_words, max_words)
    words = [fake_word() for _ in range(num_words)]
    return ' '.join(w.capitalize() for w in words)


def fake_chinese_sentence(min_chars: int = 10, max_chars: int = 30) -> str:
    """
    Generate a fake Chinese sentence.
    
    Args:
        min_chars: Minimum characters
        max_chars: Maximum characters
        
    Returns:
        Chinese sentence string
    """
    chars = '的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元权今院'
    num_chars = _random_int(min_chars, max_chars)
    sentence = ''.join(_random_choice(chars) for _ in range(num_chars))
    return sentence + '。'


# =============================================================================
# ID Data
# =============================================================================

def fake_uuid() -> str:
    """Generate a fake UUID."""
    import uuid
    return str(uuid.uuid4())


def fake_id(prefix: str = '', length: int = 8) -> str:
    """
    Generate a fake ID.
    
    Args:
        prefix: ID prefix
        length: Length of random part
        
    Returns:
        ID string
    """
    random_part = _random_string(length, string.ascii_uppercase + string.digits)
    if prefix:
        return f"{prefix}_{random_part}"
    return random_part


def fake_order_id() -> str:
    """Generate a fake order ID."""
    date_part = datetime.now().strftime('%Y%m%d')
    random_part = _random_string(8, string.ascii_uppercase + string.digits)
    return f"ORD-{date_part}-{random_part}"


def fake_transaction_id() -> str:
    """Generate a fake transaction ID."""
    return f"TXN-{_random_string(16, string.ascii_uppercase + string.digits)}"


def fake_tracking_number() -> str:
    """Generate a fake tracking number."""
    carriers = ['1Z', 'YT', 'JD', 'SF']
    carrier = _random_choice(carriers)
    return carrier + _random_string(14, string.ascii_uppercase + string.digits)


# =============================================================================
# File Data
# =============================================================================

def fake_filename(category: str = None, ext: str = None) -> str:
    """
    Generate a fake filename.
    
    Args:
        category: File category ('image', 'document', 'video', etc.)
        ext: Custom extension
        
    Returns:
        Filename string
    """
    name = _random_string(_random_int(5, 15), string.ascii_lowercase + '_-')
    
    if ext:
        extension = ext if ext.startswith('.') else f'.{ext}'
    elif category and category in FILE_EXTENSIONS:
        extension = _random_choice(FILE_EXTENSIONS[category])
    else:
        all_extensions = []
        for exts in FILE_EXTENSIONS.values():
            all_extensions.extend(exts)
        extension = _random_choice(all_extensions)
    
    return f"{name}{extension}"


def fake_file_size(min_kb: int = 1, max_kb: int = 10240) -> str:
    """
    Generate a fake file size string.
    
    Args:
        min_kb: Minimum size in KB
        max_kb: Maximum size in KB
        
    Returns:
        Human-readable file size string
    """
    size_kb = _random_int(min_kb, max_kb)
    
    if size_kb < 1024:
        return f"{size_kb} KB"
    elif size_kb < 1024 * 1024:
        return f"{size_kb / 1024:.1f} MB"
    else:
        return f"{size_kb / (1024 * 1024):.1f} GB"


def fake_file_path(depth: int = None, category: str = None) -> str:
    """
    Generate a fake file path.
    
    Args:
        depth: Directory depth (random if None)
        category: File category for extension
        
    Returns:
        File path string
    """
    if depth is None:
        depth = _random_int(1, 4)
    
    dirs = [_random_string(_random_int(3, 10), string.ascii_lowercase) for _ in range(depth)]
    filename = fake_filename(category)
    
    return '/' + '/'.join(dirs + [filename])


def fake_mime_type(category: str = None) -> str:
    """Generate a fake MIME type."""
    mime_types = {
        'image': ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'],
        'document': ['application/pdf', 'application/msword', 'text/plain', 'text/html'],
        'video': ['video/mp4', 'video/webm', 'video/quicktime', 'video/x-msvideo'],
        'audio': ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/aac'],
        'data': ['application/json', 'application/xml', 'text/csv', 'text/yaml'],
    }
    
    if category and category in mime_types:
        return _random_choice(mime_types[category])
    
    all_mimes = []
    for mimes in mime_types.values():
        all_mimes.extend(mimes)
    return _random_choice(all_mimes)


# =============================================================================
# JSON Data Generation
# =============================================================================

def fake_user(lang: str = 'en', country: str = None) -> Dict[str, Any]:
    """
    Generate a complete fake user profile.
    
    Args:
        lang: Language ('en' or 'zh')
        country: Country code for phone
        
    Returns:
        Dictionary with user data
    """
    gender = fake_gender()
    
    return {
        'id': fake_id('USR'),
        'name': fake_name(lang, gender),
        'first_name': fake_first_name(lang, gender),
        'last_name': fake_last_name(lang),
        'email': fake_email(lang=lang),
        'phone': fake_phone(country or ('CN' if lang == 'zh' else 'US')),
        'gender': gender,
        'age': fake_age(),
        'birthday': fake_birthday(),
        'address': fake_address(lang),
        'job_title': fake_job_title(),
        'company': fake_company(lang),
        'avatar': fake_url(domain='example.com', path=f'/avatars/{fake_uuid()}.jpg'),
        'created_at': fake_datetime(2020, 2024),
    }


def fake_product_full() -> Dict[str, Any]:
    """Generate a complete fake product."""
    product = fake_product()
    product.update({
        'id': fake_id('PRD'),
        'description': fake_paragraph(1, 2),
        'created_at': fake_date(2020, 2024),
    })
    return product


def fake_order(lang: str = 'en') -> Dict[str, Any]:
    """Generate a fake order."""
    num_items = _random_int(1, 5)
    items = [fake_product() for _ in range(num_items)]
    total = sum(item['price'] for item in items)
    
    statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    
    return {
        'order_id': fake_order_id(),
        'customer': fake_user(lang),
        'items': items,
        'total': round(total, 2),
        'currency': 'USD',
        'status': _random_choice(statuses),
        'shipping_address': fake_address(lang),
        'tracking_number': fake_tracking_number(),
        'created_at': fake_datetime(2023, 2024),
    }


def fake_api_response(status: int = 200, data: Any = None) -> Dict[str, Any]:
    """
    Generate a fake API response.
    
    Args:
        status: HTTP status code
        data: Response data
        
    Returns:
        Dictionary representing API response
    """
    response = {
        'status': status,
        'message': HTTP_STATUS_CODES.get(status, 'Unknown'),
        'timestamp': fake_timestamp(2024, 2024),
        'request_id': fake_id('REQ', 16),
    }
    
    if data is not None:
        response['data'] = data
    else:
        response['data'] = None
    
    return response


# =============================================================================
# Batch Generation
# =============================================================================

def fake_users(count: int = 10, lang: str = 'en') -> List[Dict[str, Any]]:
    """Generate multiple fake users."""
    return [fake_user(lang) for _ in range(count)]


def fake_products(count: int = 10) -> List[Dict[str, Any]]:
    """Generate multiple fake products."""
    return [fake_product_full() for _ in range(count)]


def fake_orders(count: int = 10, lang: str = 'en') -> List[Dict[str, Any]]:
    """Generate multiple fake orders."""
    return [fake_order(lang) for _ in range(count)]


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Fake Data Utilities - Demo")
    print("=" * 60)
    
    print("\n--- Person Data ---")
    print(f"Name (EN): {fake_name('en')}")
    print(f"Name (ZH): {fake_name('zh')}")
    print(f"First Name: {fake_first_name()}")
    print(f"Last Name: {fake_last_name()}")
    print(f"Gender: {fake_gender()}")
    print(f"Age: {fake_age()}")
    print(f"Birthday: {fake_birthday()}")
    
    print("\n--- Contact Data ---")
    print(f"Email: {fake_email()}")
    print(f"Phone (US): {fake_phone('US')}")
    print(f"Phone (CN): {fake_phone('CN')}")
    print(f"Address: {fake_full_address()}")
    
    print("\n--- Internet Data ---")
    print(f"URL: {fake_url()}")
    print(f"Domain: {fake_domain()}")
    print(f"IPv4: {fake_ipv4()}")
    print(f"IPv4 (private): {fake_ipv4(private=True)}")
    print(f"IPv6: {fake_ipv6()}")
    print(f"MAC: {fake_mac_address()}")
    print(f"User-Agent: {fake_user_agent()}")
    print(f"HTTP Status: {fake_http_status()}")
    print(f"API Path: {fake_api_path()}")
    
    print("\n--- Business Data ---")
    print(f"Company (EN): {fake_company('en')}")
    print(f"Company (ZH): {fake_company('zh')}")
    print(f"Job Title: {fake_job_title()}")
    print(f"Industry: {fake_industry()}")
    print(f"Salary: {fake_salary()}")
    print(f"Department: {fake_department()}")
    
    print("\n--- Product Data ---")
    product = fake_product()
    print(f"Product: {product['name']} - {product['price']} {product['currency']}")
    print(f"Product Name: {fake_product_name()}")
    print(f"Price: {fake_price()}")
    print(f"SKU: {fake_sku()}")
    print(f"Barcode: {fake_barcode()}")
    
    print("\n--- Date/Time Data ---")
    print(f"Date: {fake_date()}")
    print(f"Time: {fake_time()}")
    print(f"DateTime: {fake_datetime()}")
    print(f"Timestamp: {fake_timestamp()}")
    print(f"Timezone: {fake_timezone()}")
    
    print("\n--- Text Data ---")
    print(f"Sentence: {fake_sentence()}")
    print(f"Paragraph: {fake_paragraph()}")
    print(f"Title: {fake_title()}")
    print(f"Chinese: {fake_chinese_sentence()}")
    
    print("\n--- ID Data ---")
    print(f"UUID: {fake_uuid()}")
    print(f"ID: {fake_id('TEST')}")
    print(f"Order ID: {fake_order_id()}")
    print(f"Transaction ID: {fake_transaction_id()}")
    print(f"Tracking #: {fake_tracking_number()}")
    
    print("\n--- File Data ---")
    print(f"Filename: {fake_filename()}")
    print(f"Image Filename: {fake_filename('image')}")
    print(f"File Size: {fake_file_size()}")
    print(f"File Path: {fake_file_path()}")
    print(f"MIME Type: {fake_mime_type()}")
    
    print("\n--- Complete Objects ---")
    user = fake_user()
    print(f"User: {user['name']} ({user['email']})")
    
    order = fake_order()
    print(f"Order: {order['order_id']} - ${order['total']} ({order['status']})")
    
    response = fake_api_response(200, {'message': 'Success'})
    print(f"API Response: {response['status']} - {response['message']}")
    
    print("\n--- Batch Generation ---")
    users = fake_users(3)
    print(f"Generated {len(users)} users:")
    for u in users:
        print(f"  - {u['name']} ({u['email']})")
    
    print("\n" + "=" * 60)
    print("Demo completed!")