#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Fake Data Utilities Test Suite

Comprehensive tests for fake_data_utils module.
Run from AllToolkit/Python directory: python3 fake_data_utils/fake_data_utils_test.py
"""

import sys
import os

# Add the parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import module
from fake_data_utils.mod import (
    fake_name, fake_first_name, fake_last_name, fake_gender, fake_age, fake_birthday,
    fake_email, fake_phone, fake_address, fake_full_address,
    fake_url, fake_domain, fake_ipv4, fake_ipv6, fake_mac_address,
    fake_user_agent, fake_http_method, fake_http_status, fake_api_path,
    fake_company, fake_job_title, fake_industry, fake_salary, fake_department,
    fake_product, fake_product_name, fake_price, fake_sku, fake_barcode,
    fake_date, fake_time, fake_datetime, fake_timestamp, fake_timezone,
    fake_sentence, fake_paragraph, fake_text, fake_word, fake_title, fake_chinese_sentence,
    fake_uuid, fake_id, fake_order_id, fake_transaction_id, fake_tracking_number,
    fake_filename, fake_file_size, fake_file_path, fake_mime_type,
    fake_user, fake_product_full, fake_order, fake_api_response,
    fake_users, fake_products, fake_orders,
)


def test_person_data():
    """Test person-related data generation."""
    print("Testing person data...")
    
    # Name generation
    name_en = fake_name('en')
    assert len(name_en) > 0
    assert ' ' in name_en  # English names have space between first and last
    
    name_zh = fake_name('zh')
    assert len(name_zh) >= 2  # Chinese names have at least 2 characters
    
    # Gender-specific names
    name_male = fake_name('en', 'male')
    assert len(name_male) > 0
    
    name_female = fake_name('en', 'female')
    assert len(name_female) > 0
    
    # First and last names
    first_name = fake_first_name('en')
    assert len(first_name) > 0
    
    last_name = fake_last_name('en')
    assert len(last_name) > 0
    
    # Gender
    gender = fake_gender()
    assert gender in ['male', 'female']
    
    # Age
    age = fake_age(18, 80)
    assert 18 <= age <= 80
    
    # Birthday
    birthday = fake_birthday(20, 60)
    assert len(birthday) == 10  # YYYY-MM-DD format
    assert '-' in birthday
    
    print("  ✓ All person data tests passed")


def test_contact_data():
    """Test contact-related data generation."""
    print("Testing contact data...")
    
    # Email
    email = fake_email()
    assert '@' in email
    assert '.' in email.split('@')[1]
    
    email_custom = fake_email('custom.com')
    assert email_custom.endswith('custom.com')
    
    # Phone numbers
    phone_us = fake_phone('US')
    assert '(' in phone_us  # US format: (XXX) XXX-XXXX
    
    phone_cn = fake_phone('CN')
    assert len(phone_cn) >= 11  # Chinese mobile numbers are 11 digits
    
    phone_uk = fake_phone('UK')
    assert phone_uk.startswith('07')
    
    # Address
    addr_en = fake_address('en')
    assert 'street' in addr_en
    assert 'city' in addr_en
    assert 'zipcode' in addr_en
    
    addr_zh = fake_address('zh')
    assert 'street' in addr_zh
    assert 'city' in addr_zh
    
    # Full address
    full_addr = fake_full_address()
    assert ',' in full_addr
    
    print("  ✓ All contact data tests passed")


def test_internet_data():
    """Test internet-related data generation."""
    print("Testing internet data...")
    
    # URL
    url_secure = fake_url(secure=True)
    assert url_secure.startswith('https://')
    
    url_insecure = fake_url(secure=False)
    assert url_insecure.startswith('http://')
    
    url_custom = fake_url(domain='example.com', path='/api/test')
    assert 'example.com' in url_custom
    assert '/api/test' in url_custom
    
    # Domain
    domain = fake_domain()
    assert '.' in domain
    
    # IPv4
    ipv4 = fake_ipv4()
    parts = ipv4.split('.')
    assert len(parts) == 4
    assert all(0 <= int(p) <= 255 for p in parts)
    
    ipv4_private = fake_ipv4(private=True)
    private_parts = ipv4_private.split('.')
    assert len(private_parts) == 4
    # Private IP ranges: 10.x.x.x, 172.16-31.x.x, 192.168.x.x
    first_octet = int(private_parts[0])
    assert first_octet in [10, 172, 192]
    
    # IPv6
    ipv6 = fake_ipv6()
    parts = ipv6.split(':')
    assert len(parts) == 8
    
    # MAC address
    mac = fake_mac_address()
    parts = mac.split(':')
    assert len(parts) == 6
    assert all(len(p) == 2 for p in parts)
    
    # User agent
    ua = fake_user_agent()
    assert 'Mozilla' in ua
    
    # HTTP method
    method = fake_http_method()
    assert method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']
    
    # HTTP status
    status, desc = fake_http_status()
    assert status in [200, 201, 400, 401, 403, 404, 500, 502, 503]
    assert len(desc) > 0
    
    # API path
    path = fake_api_path()
    assert path.startswith('/api/')
    
    print("  ✓ All internet data tests passed")


def test_business_data():
    """Test business-related data generation."""
    print("Testing business data...")
    
    # Company
    company_en = fake_company('en')
    assert len(company_en) > 0
    
    company_zh = fake_company('zh')
    assert len(company_zh) > 0
    
    # Job title
    job = fake_job_title()
    assert len(job) > 0
    
    # Industry
    industry = fake_industry()
    assert len(industry) > 0
    
    # Salary
    salary = fake_salary(30000, 100000)
    assert 30000 <= salary <= 100000
    assert salary % 1000 == 0  # Should be rounded to nearest 1000
    
    # Department
    dept = fake_department()
    assert len(dept) > 0
    
    print("  ✓ All business data tests passed")


def test_product_data():
    """Test product-related data generation."""
    print("Testing product data...")
    
    # Product
    product = fake_product()
    assert 'name' in product
    assert 'category' in product
    assert 'price' in product
    assert 'sku' in product
    assert product['price'] > 0
    
    # Product by category
    electronics = fake_product('Electronics')
    assert electronics['category'] == 'Electronics'
    
    # Product name
    name = fake_product_name()
    assert len(name) > 0
    
    # Price
    price_str = fake_price(10, 100)
    assert '$' in price_str
    
    price_eur = fake_price(10, 100, 'EUR')
    assert '€' in price_eur
    
    # SKU
    sku = fake_sku()
    assert 'SKU-' in sku
    
    sku_custom = fake_sku('PRD')
    assert 'PRD-' in sku_custom
    
    # Barcode
    barcode = fake_barcode()
    assert len(barcode) == 13
    assert barcode.isdigit()
    
    print("  ✓ All product data tests passed")


def test_datetime_data():
    """Test datetime-related data generation."""
    print("Testing datetime data...")
    
    # Date
    date = fake_date(2020, 2024)
    assert len(date) == 10  # YYYY-MM-DD
    year = int(date.split('-')[0])
    assert 2020 <= year <= 2024
    
    # Time
    time = fake_time()
    assert len(time) == 8  # HH:MM:SS
    parts = time.split(':')
    assert len(parts) == 3
    assert 0 <= int(parts[0]) <= 23
    assert 0 <= int(parts[1]) <= 59
    assert 0 <= int(parts[2]) <= 59
    
    # DateTime
    datetime = fake_datetime(2020, 2024)
    assert len(datetime) == 19  # YYYY-MM-DD HH:MM:SS
    
    # Timestamp
    ts = fake_timestamp(2020, 2024)
    assert ts > 0
    assert isinstance(ts, int)
    
    # Timezone
    tz = fake_timezone()
    assert '/' in tz or tz == 'UTC'
    
    print("  ✓ All datetime data tests passed")


def test_text_data():
    """Test text-related data generation."""
    print("Testing text data...")
    
    # Sentence
    sentence = fake_sentence(5, 10)
    assert len(sentence) > 0
    assert sentence.endswith('.')
    
    # Paragraph
    paragraph = fake_paragraph(2, 5)
    assert len(paragraph) > 0
    assert '.' in paragraph
    
    # Text
    text = fake_text(2)
    paragraphs = text.split('\n\n')
    assert len(paragraphs) == 2
    
    # Word
    word = fake_word()
    assert len(word) > 0
    
    # Title
    title = fake_title(3, 6)
    assert len(title) > 0
    
    # Chinese sentence
    zh_sentence = fake_chinese_sentence(10, 20)
    assert zh_sentence.endswith('。')
    
    print("  ✓ All text data tests passed")


def test_id_data():
    """Test ID-related data generation."""
    print("Testing ID data...")
    
    # UUID
    uuid = fake_uuid()
    assert len(uuid) == 36  # Format: 8-4-4-4-12
    assert uuid.count('-') == 4
    
    # Custom ID
    id_custom = fake_id('USR', 8)
    assert 'USR_' in id_custom
    random_part = id_custom.split('_')[1]
    assert len(random_part) == 8
    
    # Order ID
    order_id = fake_order_id()
    assert 'ORD-' in order_id
    
    # Transaction ID
    txn_id = fake_transaction_id()
    assert 'TXN-' in txn_id
    
    # Tracking number
    tracking = fake_tracking_number()
    assert len(tracking) > 0
    
    print("  ✓ All ID data tests passed")


def test_file_data():
    """Test file-related data generation."""
    print("Testing file data...")
    
    # Filename
    filename = fake_filename()
    assert '.' in filename
    
    # Image filename
    img_filename = fake_filename('image')
    ext = img_filename.split('.')[-1]
    assert ext in ['jpg', 'png', 'gif', 'webp', 'svg', 'bmp']
    
    # Custom extension
    custom_ext = fake_filename(ext='.pdf')
    assert custom_ext.endswith('.pdf')
    
    # File size
    size_kb = fake_file_size(1, 100)
    assert 'KB' in size_kb
    
    size_mb = fake_file_size(1024, 10240)
    assert 'MB' in size_mb
    
    # File path
    path = fake_file_path()
    assert path.startswith('/')
    assert '.' in path  # Has extension
    
    # MIME type
    mime = fake_mime_type()
    assert '/' in mime
    
    mime_image = fake_mime_type('image')
    assert mime_image.startswith('image/')
    
    print("  ✓ All file data tests passed")


def test_complete_objects():
    """Test complete object generation."""
    print("Testing complete objects...")
    
    # User
    user = fake_user('en')
    assert 'id' in user
    assert 'name' in user
    assert 'email' in user
    assert 'phone' in user
    assert 'address' in user
    assert '@' in user['email']
    
    user_zh = fake_user('zh')
    assert 'name' in user_zh
    assert 'email' in user_zh
    
    # Product full
    product = fake_product_full()
    assert 'id' in product
    assert 'description' in product
    assert 'created_at' in product
    
    # Order
    order = fake_order('en')
    assert 'order_id' in order
    assert 'customer' in order
    assert 'items' in order
    assert 'total' in order
    assert 'status' in order
    assert order['total'] > 0
    assert len(order['items']) > 0
    
    # API Response
    response = fake_api_response(200, {'data': 'test'})
    assert response['status'] == 200
    assert 'message' in response
    assert 'timestamp' in response
    assert 'request_id' in response
    
    print("  ✓ All complete object tests passed")


def test_batch_generation():
    """Test batch generation functions."""
    print("Testing batch generation...")
    
    # Users batch
    users = fake_users(5, 'en')
    assert len(users) == 5
    assert all('name' in u for u in users)
    assert all('email' in u for u in users)
    
    # Products batch
    products = fake_products(5)
    assert len(products) == 5
    assert all('name' in p for p in products)
    assert all('price' in p for p in products)
    
    # Orders batch
    orders = fake_orders(5, 'en')
    assert len(orders) == 5
    assert all('order_id' in o for o in orders)
    assert all('items' in o for o in orders)
    
    print("  ✓ All batch generation tests passed")


def test_consistency():
    """Test data consistency and validity."""
    print("Testing consistency...")
    
    # Generate multiple values and check they're different
    names = [fake_name() for _ in range(10)]
    assert len(set(names)) > 1  # Should have some variation
    
    emails = [fake_email() for _ in range(10)]
    assert len(set(emails)) > 1
    
    # Check ranges are respected
    ages = [fake_age(25, 35) for _ in range(20)]
    assert all(25 <= age <= 35 for age in ages)
    
    prices = [fake_price(10, 100) for _ in range(20)]
    # Parse prices (strip $ and convert to float)
    price_values = [float(p.replace('$', '')) for p in prices]
    assert all(10 <= pv <= 100 for pv in price_values)
    
    print("  ✓ All consistency tests passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Fake Data Utilities - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_person_data,
        test_contact_data,
        test_internet_data,
        test_business_data,
        test_product_data,
        test_datetime_data,
        test_text_data,
        test_id_data,
        test_file_data,
        test_complete_objects,
        test_batch_generation,
        test_consistency,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)