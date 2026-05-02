#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fake_data_utils - Basic Examples

Basic usage examples for fake_data_utils module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fake_data_utils import mod as fake


def example_person_data():
    """Example: Person data generation."""
    print("=" * 50)
    print("Example: Person Data")
    print("=" * 50)
    
    # Generate English names
    for _ in range(5):
        name = fake.fake_name('en')
        gender = fake.fake_gender()
        age = fake.fake_age(20, 50)
        birthday = fake.fake_birthday(20, 50)
        print(f"  {name} | {gender} | Age: {age} | Birthday: {birthday}")
    
    print()
    
    # Generate Chinese names
    for _ in range(5):
        name = fake.fake_name('zh')
        gender = fake.fake_gender()
        age = fake.fake_age(20, 50)
        print(f"  {name} | {gender} | Age: {age}")


def example_contact_data():
    """Example: Contact data generation."""
    print("\n" + "=" * 50)
    print("Example: Contact Data")
    print("=" * 50)
    
    # Emails
    print("\nEmails:")
    for _ in range(5):
        email = fake.fake_email()
        print(f"  {email}")
    
    # Custom domain emails
    print("\nCustom domain emails:")
    for _ in range(5):
        email = fake.fake_email('mycompany.com')
        print(f"  {email}")
    
    # Phone numbers (different countries)
    print("\nPhone numbers:")
    print(f"  US: {fake.fake_phone('US')}")
    print(f"  CN: {fake.fake_phone('CN')}")
    print(f"  UK: {fake.fake_phone('UK')}")
    print(f"  DE: {fake.fake_phone('DE')}")
    
    # Addresses
    print("\nAddresses (English):")
    for _ in range(3):
        addr = fake.fake_address('en')
        print(f"  {addr['street']}")
        print(f"  {addr['city']}, {addr['state']} {addr['zipcode']}")
        print()
    
    print("\nAddresses (Chinese):")
    for _ in range(3):
        addr = fake.fake_address('zh')
        print(f"  {addr['street']}")
        print(f"  城市: {addr['city']}")
        print()


def example_internet_data():
    """Example: Internet data generation."""
    print("\n" + "=" * 50)
    print("Example: Internet Data")
    print("=" * 50)
    
    # URLs
    print("\nURLs:")
    for _ in range(5):
        print(f"  {fake.fake_url()}")
    
    # Domains
    print("\nDomains:")
    for _ in range(5):
        print(f"  {fake.fake_domain()}")
    
    # IP addresses
    print("\nIP Addresses:")
    print(f"  IPv4 (public):  {fake.fake_ipv4()}")
    print(f"  IPv4 (private): {fake.fake_ipv4(private=True)}")
    print(f"  IPv6:           {fake.fake_ipv6()}")
    print(f"  MAC:            {fake.fake_mac_address()}")
    
    # HTTP data
    print("\nHTTP Data:")
    print(f"  Method: {fake.fake_http_method()}")
    status, desc = fake.fake_http_status()
    print(f"  Status: {status} - {desc}")
    print(f"  Path:   {fake.fake_api_path()}")
    print(f"  UA:     {fake.fake_user_agent()[:50]}...")


def example_business_data():
    """Example: Business data generation."""
    print("\n" + "=" * 50)
    print("Example: Business Data")
    print("=" * 50)
    
    # Companies
    print("\nCompanies (English):")
    for _ in range(5):
        print(f"  {fake.fake_company('en')}")
    
    print("\nCompanies (Chinese):")
    for _ in range(5):
        print(f"  {fake.fake_company('zh')}")
    
    # Job data
    print("\nJob Information:")
    for _ in range(5):
        job = fake.fake_job_title()
        dept = fake.fake_department()
        salary = fake.fake_salary(50000, 150000)
        industry = fake.fake_industry()
        print(f"  {job} | {dept} | ${salary}/year | {industry}")


def example_product_data():
    """Example: Product data generation."""
    print("\n" + "=" * 50)
    print("Example: Product Data")
    print("=" * 50)
    
    # Products by category
    print("\nElectronics:")
    for _ in range(3):
        p = fake.fake_product('Electronics')
        print(f"  {p['name']} - ${p['price']} | SKU: {p['sku']}")
    
    print("\nClothing:")
    for _ in range(3):
        p = fake.fake_product('Clothing')
        print(f"  {p['name']} - ${p['price']} | In stock: {p['in_stock']}")
    
    print("\nBooks:")
    for _ in range(3):
        p = fake.fake_product('Books')
        print(f"  {p['name']} - ${p['price']} | Rating: {p['rating']}/5")
    
    # Price formatting
    print("\nPrice formats:")
    print(f"  USD: {fake.fake_price(10, 100, 'USD')}")
    print(f"  EUR: {fake.fake_price(10, 100, 'EUR')}")
    print(f"  GBP: {fake.fake_price(10, 100, 'GBP')}")
    print(f"  CNY: {fake.fake_price(10, 100, 'CNY')}")


def example_datetime_data():
    """Example: Date/time data generation."""
    print("\n" + "=" * 50)
    print("Example: Date/Time Data")
    print("=" * 50)
    
    # Dates
    print("\nDates:")
    for _ in range(5):
        print(f"  {fake.fake_date(2020, 2025)}")
    
    # Times
    print("\nTimes:")
    for _ in range(5):
        print(f"  {fake.fake_time()}")
    
    # Full datetime
    print("\nFull datetime:")
    for _ in range(5):
        print(f"  {fake.fake_datetime()}")
    
    # Timestamps
    print("\nTimestamps:")
    for _ in range(5):
        ts = fake.fake_timestamp(2024, 2024)
        print(f"  {ts}")
    
    # Timezones
    print("\nTimezones:")
    for _ in range(5):
        print(f"  {fake.fake_timezone()}")


def example_text_data():
    """Example: Text data generation."""
    print("\n" + "=" * 50)
    print("Example: Text Data")
    print("=" * 50)
    
    # Sentences
    print("\nSentences:")
    for _ in range(5):
        print(f"  {fake.fake_sentence()}")
    
    # Paragraph
    print("\nParagraph:")
    print(f"  {fake.fake_paragraph()}")
    
    # Title
    print("\nTitles:")
    for _ in range(5):
        print(f"  {fake.fake_title()}")
    
    # Chinese text
    print("\nChinese sentences:")
    for _ in range(3):
        print(f"  {fake.fake_chinese_sentence()}")


def example_file_data():
    """Example: File data generation."""
    print("\n" + "=" * 50)
    print("Example: File Data")
    print("=" * 50)
    
    # Filenames
    print("\nFilenames (random):")
    for _ in range(5):
        print(f"  {fake.fake_filename()}")
    
    print("\nFilenames (image):")
    for _ in range(5):
        print(f"  {fake.fake_filename('image')}")
    
    print("\nFilenames (document):")
    for _ in range(5):
        print(f"  {fake.fake_filename('document')}")
    
    # File sizes
    print("\nFile sizes:")
    print(f"  Small:  {fake.fake_file_size(1, 100)}")
    print(f"  Medium: {fake.fake_file_size(100, 1000)}")
    print(f"  Large:  {fake.fake_file_size(1000, 10000)}")
    
    # File paths
    print("\nFile paths:")
    for _ in range(5):
        print(f"  {fake.fake_file_path()}")
    
    # MIME types
    print("\nMIME types:")
    for _ in range(5):
        print(f"  {fake.fake_mime_type()}")


def example_complete_objects():
    """Example: Complete object generation."""
    print("\n" + "=" * 50)
    print("Example: Complete Objects")
    print("=" * 50)
    
    # User profiles
    print("\nUser profiles:")
    for _ in range(3):
        user = fake.fake_user()
        print(f"  ID: {user['id']}")
        print(f"  Name: {user['name']}")
        print(f"  Email: {user['email']}")
        print(f"  Job: {user['job_title']} at {user['company']}")
        print()
    
    # Orders
    print("\nOrders:")
    order = fake.fake_order()
    print(f"  Order ID: {order['order_id']}")
    print(f"  Customer: {order['customer']['name']}")
    print(f"  Items: {len(order['items'])}")
    for item in order['items']:
        print(f"    - {item['name']}: ${item['price']}")
    print(f"  Total: ${order['total']}")
    print(f"  Status: {order['status']}")


def example_batch_generation():
    """Example: Batch generation."""
    print("\n" + "=" * 50)
    print("Example: Batch Generation")
    print("=" * 50)
    
    # Generate multiple users
    print("\nGenerating 10 users:")
    users = fake.fake_users(10)
    for u in users[:5]:  # Show first 5
        print(f"  {u['name']} ({u['email']})")
    print(f"  ... and {len(users) - 5} more")
    
    # Generate multiple products
    print("\nGenerating 10 products:")
    products = fake.fake_products(10)
    for p in products[:5]:  # Show first 5
        print(f"  {p['name']} - ${p['price']}")
    print(f"  ... and {len(products) - 5} more")
    
    # Generate multiple orders
    print("\nGenerating 5 orders:")
    orders = fake.fake_orders(5)
    for o in orders:
        print(f"  {o['order_id']} - ${o['total']} ({len(o['items'])} items)")


def main():
    """Run all examples."""
    example_person_data()
    example_contact_data()
    example_internet_data()
    example_business_data()
    example_product_data()
    example_datetime_data()
    example_text_data()
    example_file_data()
    example_complete_objects()
    example_batch_generation()
    
    print("\n" + "=" * 50)
    print("All examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()