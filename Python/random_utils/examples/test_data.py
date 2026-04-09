#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Test Data Generation Examples

Demonstrates generating mock/test data for development and testing.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    random_string, random_password, random_uuid, random_email,
    random_phone, random_ipv4, random_color, random_datetime,
    random_date, random_int, random_choice, random_vector,
    random_id, random_slug
)
from datetime import datetime


def generate_user(index: int) -> dict:
    """Generate a mock user record."""
    first_names = ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana', 'Eve', 'Frank']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
    
    first_name = random_choice(first_names)
    last_name = random_choice(last_names)
    
    return {
        'id': random_id('user', length=8),
        'username': f"{first_name.lower()}{last_name.lower()}{random_int(1, 999)}",
        'email': random_email('example.com'),
        'phone': random_phone(),
        'first_name': first_name,
        'last_name': last_name,
        'password_hash': random_string(64, charset='0123456789abcdef'),
        'created_at': random_date(2020, 2024).isoformat(),
        'avatar_color': random_color('hex'),
        'is_active': random_int(0, 1) == 1,
    }


def generate_product(index: int) -> dict:
    """Generate a mock product record."""
    categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports', 'Toys']
    adjectives = ['Premium', 'Basic', 'Pro', 'Ultra', 'Mini', 'Max', 'Lite']
    nouns = ['Widget', 'Gadget', 'Device', 'Tool', 'Kit', 'Set', 'Pack']
    
    name = f"{random_choice(adjectives)} {random_choice(nouns)} {random_int(100, 999)}"
    
    return {
        'id': random_id('prod', length=8),
        'sku': random_slug(3, '-').upper(),
        'name': name,
        'category': random_choice(categories),
        'price': round(random_int(100, 10000) / 100, 2),
        'stock': random_int(0, 1000),
        'color': random_color('hex'),
        'created_at': random_date(2022, 2024).isoformat(),
    }


def generate_order(index: int) -> dict:
    """Generate a mock order record."""
    statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    
    return {
        'id': random_id('order', length=8),
        'order_number': f"ORD-{random_int(10000, 99999)}",
        'user_id': random_id('user', length=8),
        'status': random_choice(statuses),
        'total': round(random_int(1000, 50000) / 100, 2),
        'items_count': random_int(1, 10),
        'created_at': random_datetime(
            datetime(2024, 1, 1),
            datetime(2024, 12, 31)
        ).isoformat(),
        'shipping_ip': random_ipv4(),
    }


def generate_log_entry(index: int) -> dict:
    """Generate a mock log entry."""
    levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    services = ['api', 'web', 'worker', 'scheduler', 'database']
    
    return {
        'id': random_uuid(),
        'level': random_choice(levels),
        'service': random_choice(services),
        'message': f"Log message #{index}",
        'timestamp': random_datetime(
            datetime(2024, 1, 1),
            datetime.now()
        ).isoformat(),
        'request_id': random_id('req', length=16),
        'user_id': random_id('user', length=8) if random_int(0, 1) else None,
        'ip_address': random_ipv4(),
    }


def generate_vector_data(count: int, dimensions: int) -> list:
    """Generate random vector data for ML testing."""
    return [random_vector(dimensions) for _ in range(count)]


def main():
    print("="*60)
    print("Test Data Generation Examples")
    print("="*60)
    
    # Users
    print("\n1. User Records")
    print("-"*40)
    users = [generate_user(i) for i in range(5)]
    for i, user in enumerate(users, 1):
        print(f"\n   User {i}:")
        print(f"     ID: {user['id']}")
        print(f"     Username: {user['username']}")
        print(f"     Email: {user['email']}")
        print(f"     Name: {user['first_name']} {user['last_name']}")
        print(f"     Created: {user['created_at']}")
    
    # Products
    print("\n2. Product Records")
    print("-"*40)
    products = [generate_product(i) for i in range(5)]
    for i, product in enumerate(products, 1):
        print(f"\n   Product {i}:")
        print(f"     SKU: {product['sku']}")
        print(f"     Name: {product['name']}")
        print(f"     Category: {product['category']}")
        print(f"     Price: ${product['price']}")
        print(f"     Stock: {product['stock']}")
    
    # Orders
    print("\n3. Order Records")
    print("-"*40)
    orders = [generate_order(i) for i in range(5)]
    for i, order in enumerate(orders, 1):
        print(f"\n   Order {i}:")
        print(f"     Order #: {order['order_number']}")
        print(f"     Status: {order['status']}")
        print(f"     Total: ${order['total']}")
        print(f"     Items: {order['items_count']}")
    
    # Log Entries
    print("\n4. Log Entries")
    print("-"*40)
    logs = [generate_log_entry(i) for i in range(5)]
    for i, log in enumerate(logs, 1):
        print(f"\n   Log {i}:")
        print(f"     Level: {log['level']}")
        print(f"     Service: {log['service']}")
        print(f"     Message: {log['message']}")
        print(f"     Timestamp: {log['timestamp']}")
    
    # Vector Data
    print("\n5. Vector Data (for ML)")
    print("-"*40)
    vectors = generate_vector_data(5, 128)
    for i, vec in enumerate(vectors, 1):
        print(f"   Vector {i}: [{vec[0]:.4f}, {vec[1]:.4f}, ..., {vec[-1]:.4f}] (dim={len(vec)})")
    
    # CSV Export Example
    print("\n6. CSV Export Example")
    print("-"*40)
    print("   Users CSV:")
    print("   id,username,email,created_at")
    for user in users[:3]:
        print(f"   {user['id']},{user['username']},{user['email']},{user['created_at']}")
    
    print("\n" + "="*60)
    print("Test data generation completed!")
    print("="*60)


if __name__ == "__main__":
    main()
