#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit Database Utils - Usage Examples
============================================
Demonstrates common use cases for the database utilities module.
"""

import sys
import os
import tempfile

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from mod import (
    SQLiteDatabase, CSVDatabase, JSONDatabase,
    export_to_csv, import_from_csv,
    export_to_json, import_from_json,
    convert_csv_to_json, convert_json_to_csv,
    sqlite_connect, csv_connect, json_connect
)


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def example_sqlite_basic() -> None:
    """Example: Basic SQLite Operations"""
    print_section("SQLite Basic Operations")
    
    # Create database
    db_path = tempfile.mktemp(suffix=".db")
    db = SQLiteDatabase(db_path)
    
    try:
        # Create table
        print("Creating 'users' table...")
        db.create_table("users", {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE",
            "age": "INTEGER",
            "city": "TEXT"
        })
        
        # Insert single row
        print("\nInserting single user...")
        user_id = db.insert("users", {
            "name": "Alice",
            "email": "alice@example.com",
            "age": 30,
            "city": "New York"
        })
        print(f"  Inserted user with ID: {user_id}")
        
        # Insert multiple rows
        print("\nInserting multiple users...")
        users = [
            {"name": "Bob", "email": "bob@example.com", "age": 25, "city": "London"},
            {"name": "Charlie", "email": "charlie@example.com", "age": 35, "city": "Paris"},
            {"name": "Diana", "email": "diana@example.com", "age": 28, "city": "Tokyo"}
        ]
        count = db.insert_many("users", users)
        print(f"  Inserted {count} users")
        
        # Query all
        print("\nQuerying all users...")
        all_users = db.query("users")
        for user in all_users:
            print(f"  - {user['name']} ({user['age']}): {user['city']}")
        
        # Query with filter
        print("\nQuerying users older than 28...")
        senior_users = [u for u in all_users if u['age'] > 28]
        for user in senior_users:
            print(f"  - {user['name']} ({user['age']})")
        
        # Update
        print("\nUpdating Alice's age...")
        db.update("users", {"age": 31}, where={"name": "Alice"})
        alice = db.query("users", where={"name": "Alice"})[0]
        print(f"  Alice is now {alice['age']} years old")
        
        # Delete
        print("\nDeleting Diana...")
        db.delete("users", where={"name": "Diana"})
        remaining = db.query("users")
        print(f"  {len(remaining)} users remaining")
        
        # Get table info
        print("\nTable schema:")
        info = db.get_table_info("users")
        for col in info:
            pk = " [PK]" if col['pk'] else ""
            nn = " NOT NULL" if col['notnull'] else ""
            print(f"  - {col['name']}: {col['type']}{nn}{pk}")
        
    finally:
        db.close()
        if os.path.exists(db_path):
            os.remove(db_path)


def example_sqlite_transaction() -> None:
    """Example: SQLite Transactions"""
    print_section("SQLite Transactions")
    
    db_path = tempfile.mktemp(suffix=".db")
    db = SQLiteDatabase(db_path)
    
    try:
        db.create_table("accounts", {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "balance": "REAL"
        })
        
        # Initial data
        db.insert_many("accounts", [
            {"name": "Alice", "balance": 1000.0},
            {"name": "Bob", "balance": 500.0}
        ])
        
        print("Initial balances:")
        for acc in db.query("accounts"):
            print(f"  {acc['name']}: ${acc['balance']:.2f}")
        
        # Transfer with transaction
        print("\nTransferring $200 from Alice to Bob...")
        try:
            with db.transaction() as conn:
                # Deduct from Alice
                db.update("accounts", 
                         {"balance": 800.0}, 
                         where={"name": "Alice"}, 
                         _conn=conn)
                # Add to Bob
                db.update("accounts", 
                         {"balance": 700.0}, 
                         where={"name": "Bob"}, 
                         _conn=conn)
            print("  ✓ Transaction committed")
        except Exception as e:
            print(f"  ✗ Transaction rolled back: {e}")
        
        print("\nFinal balances:")
        for acc in db.query("accounts"):
            print(f"  {acc['name']}: ${acc['balance']:.2f}")
        
    finally:
        db.close()
        if os.path.exists(db_path):
            os.remove(db_path)


def example_csv_operations() -> None:
    """Example: CSV Operations"""
    print_section("CSV Operations")
    
    csv_path = tempfile.mktemp(suffix=".csv")
    csv_db = CSVDatabase(csv_path)
    
    try:
        # Write data
        print("Writing data to CSV...")
        data = [
            {"product": "Laptop", "price": "999.99", "stock": "50"},
            {"product": "Mouse", "price": "29.99", "stock": "200"},
            {"product": "Keyboard", "price": "79.99", "stock": "150"},
            {"product": "Monitor", "price": "299.99", "stock": "75"}
        ]
        csv_db.write(data)
        print(f"  Written {len(data)} products")
        
        # Read all
        print("\nAll products:")
        all_products = csv_db.read()
        for p in all_products:
            print(f"  - {p['product']}: ${p['price']} (Stock: {p['stock']})")
        
        # Query with filter
        print("\nProducts under $100:")
        cheap = [p for p in csv_db.query() if float(p['price']) < 100]
        for p in cheap:
            print(f"  - {p['product']}: ${p['price']}")
        
        # Append
        print("\nAdding new product...")
        csv_db.append({"product": "Webcam", "price": "59.99", "stock": "100"})
        print(f"  Total products: {len(csv_db.read())}")
        
        # Update
        print("\nUpdating Mouse price...")
        csv_db.update({"price": "24.99"}, where={"product": "Mouse"})
        mouse = csv_db.query(where={"product": "Mouse"})[0]
        print(f"  Mouse is now ${mouse['price']}")
        
    finally:
        csv_db.close()
        if os.path.exists(csv_path):
            os.remove(csv_path)


def example_json_operations() -> None:
    """Example: JSON Operations"""
    print_section("JSON Operations")
    
    json_path = tempfile.mktemp(suffix=".json")
    json_db = JSONDatabase(json_path)
    
    try:
        # Write data
        print("Writing data to JSON...")
        config = {
            "app_name": "MyApp",
            "version": "1.0.0",
            "settings": {
                "debug": True,
                "max_connections": 100,
                "timeout": 30
            },
            "features": ["auth", "logging", "caching"]
        }
        json_db.write(config)
        print("  Configuration saved")
        
        # Read back
        print("\nReading configuration...")
        loaded = json_db.read()
        print(f"  App: {loaded['app_name']} v{loaded['version']}")
        print(f"  Debug mode: {loaded['settings']['debug']}")
        
        # Array data
        print("\nWorking with array data...")
        users = [
            {"id": 1, "name": "Alice", "active": True},
            {"id": 2, "name": "Bob", "active": False},
            {"id": 3, "name": "Charlie", "active": True}
        ]
        json_db.write(users)
        
        # Query
        active_users = json_db.query(where={"active": "True"})
        print(f"  Active users: {len(active_users)}")
        for u in active_users:
            print(f"    - {u['name']}")
        
        # Insert
        print("\nAdding new user...")
        json_db.insert({"id": 4, "name": "Diana", "active": True})
        print(f"  Total users: {len(json_db.read())}")
        
    finally:
        json_db.close()
        if os.path.exists(json_path):
            os.remove(json_path)


def example_format_conversion() -> None:
    """Example: Format Conversion"""
    print_section("Format Conversion")
    
    csv_path = tempfile.mktemp(suffix=".csv")
    json_path = tempfile.mktemp(suffix=".json")
    converted_json = tempfile.mktemp(suffix="_converted.json")
    converted_csv = tempfile.mktemp(suffix="_converted.csv")
    
    try:
        # Create sample CSV
        data = [
            {"name": "Alice", "age": "30", "city": "New York"},
            {"name": "Bob", "age": "25", "city": "London"},
            {"name": "Charlie", "age": "35", "city": "Paris"}
        ]
        export_to_csv(data, csv_path)
        print(f"Created CSV: {csv_path}")
        
        # Convert CSV to JSON
        print("\nConverting CSV to JSON...")
        convert_csv_to_json(csv_path, converted_json)
        print(f"Created JSON: {converted_json}")
        
        # Read and display
        json_data = import_from_json(converted_json)
        print("  JSON content:")
        for item in json_data:
            print(f"    {item}")
        
        # Convert back to CSV
        print("\nConverting JSON back to CSV...")
        convert_json_to_csv(converted_json, converted_csv)
        print(f"Created CSV: {converted_csv}")
        
        csv_data = import_from_csv(converted_csv)
        print(f"  CSV has {len(csv_data)} rows")
        
    finally:
        for path in [csv_path, json_path, converted_json, converted_csv]:
            if os.path.exists(path):
                os.remove(path)


def example_real_world_scenarios() -> None:
    """Example: Real-World Scenarios"""
    print_section("Real-World Scenarios")
    
    # Scenario 1: Simple caching
    print("\n📦 Scenario 1: JSON-based Cache")
    cache_path = tempfile.mktemp(suffix=".json")
    cache = JSONDatabase(cache_path)
    
    # Store cached data
    cache.write({
        "api_response": {"status": "ok", "data": [1, 2, 3]},
        "timestamp": "2024-01-01T00:00:00Z",
        "ttl": 3600
    })
    print("  Cached API response")
    
    # Retrieve cached data
    cached = cache.read()
    print(f"  Cache TTL: {cached.get('ttl')} seconds")
    
    # Cleanup
    cache.close()
    os.remove(cache_path)
    
    # Scenario 2: Configuration management
    print("\n⚙️  Scenario 2: Configuration Management")
    config_path = tempfile.mktemp(suffix=".json")
    config = JSONDatabase(config_path)
    
    config.write({
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "myapp"
        },
        "logging": {
            "level": "INFO",
            "file": "/var/log/app.log"
        }
    })
    print("  Saved configuration")
    
    # Update specific setting
    current = config.read()
    current["logging"]["level"] = "DEBUG"
    config.write(current)
    print("  Updated log level to DEBUG")
    
    config.close()
    os.remove(config_path)
    
    # Scenario 3: Event logging
    print("\n📝 Scenario 3: CSV Event Logging")
    log_path = tempfile.mktemp(suffix=".csv")
    log_db = CSVDatabase(log_path)
    
    events = [
        {"timestamp": "2024-01-01 10:00:00", "level": "INFO", "message": "App started"},
        {"timestamp": "2024-01-01 10:05:00", "level": "WARNING", "message": "High memory usage"},
        {"timestamp": "2024-01-01 10:10:00", "level": "ERROR", "message": "Connection failed"}
    ]
    log_db.append(events)
    print(f"  Logged {len(events)} events")
    
    # Query errors
    errors = log_db.query(where={"level": "ERROR"})
    print(f"  Found {len(errors)} error(s)")
    
    log_db.close()
    os.remove(log_path)
    
    # Scenario 4: SQLite for structured data
    print("\n🗄️  Scenario 4: SQLite for Product Inventory")
    db_path = tempfile.mktemp(suffix=".db")
    db = SQLiteDatabase(db_path)
    
    db.create_table("products", {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "sku": "TEXT UNIQUE",
        "name": "TEXT",
        "price": "REAL",
        "quantity": "INTEGER"
    })
    
    products = [
        {"sku": "LAPTOP-001", "name": "Gaming Laptop", "price": 1299.99, "quantity": 10},
        {"sku": "MOUSE-001", "name": "Wireless Mouse", "price": 49.99, "quantity": 100},
        {"sku": "KB-001", "name": "Mechanical Keyboard", "price": 129.99, "quantity": 50}
    ]
    db.insert_many("products", products)
    print(f"  Added {len(products)} products")
    
    # Find low stock
    low_stock = db.execute(
        "SELECT name, quantity FROM products WHERE quantity < 50"
    )
    print("  Low stock items:")
    for item in low_stock:
        print(f"    - {item['name']}: {item['quantity']} units")
    
    db.close()
    os.remove(db_path)


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("  AllToolkit Database Utils - Usage Examples")
    print("="*60)
    
    example_sqlite_basic()
    example_sqlite_transaction()
    example_csv_operations()
    example_json_operations()
    example_format_conversion()
    example_real_world_scenarios()
    
    print("\n" + "="*60)
    print("  Examples completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
