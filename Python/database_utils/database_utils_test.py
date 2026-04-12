#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Database Utilities Test Suite
============================================
Comprehensive tests for SQLite, CSV, and JSON database utilities.
"""

import sys
import os
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    SQLiteDatabase, CSVDatabase, JSONDatabase,
    export_to_csv, import_from_csv,
    export_to_json, import_from_json,
    convert_csv_to_json, convert_json_to_csv,
    sqlite_connect, csv_connect, json_connect,
    Row, Rows
)


class TestRunner:
    """Simple test runner."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.temp_dir = None
    
    def setup(self):
        """Create temporary directory for test files."""
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown(self):
        """Clean up temporary directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test(self, name: str, condition: bool) -> None:
        """Run a single test."""
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            print(f"  ✗ {name}")
    
    def report(self) -> bool:
        """Print test report."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}")
        if self.failed == 0:
            print("🎉 All tests passed!")
        else:
            print(f"⚠️  {self.failed} test(s) failed.")
        print('='*60)
        return self.failed == 0


def run_sqlite_tests(runner: TestRunner) -> None:
    """Run SQLite database tests."""
    print("\n" + "="*60)
    print("  SQLite Database Tests")
    print("="*60)
    
    db_path = os.path.join(runner.temp_dir, "test.db")
    db = SQLiteDatabase(db_path)
    
    try:
        # Table creation
        runner.test("create_table creates table", 
                    db.create_table("users", {
                        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                        "name": "TEXT NOT NULL",
                        "email": "TEXT UNIQUE",
                        "age": "INTEGER"
                    }))
        
        runner.test("table_exists returns True for existing table",
                    db.table_exists("users"))
        
        runner.test("table_exists returns False for non-existing table",
                    not db.table_exists("nonexistent"))
        
        runner.test("get_tables returns table list",
                    "users" in db.get_tables())
        
        # Insert operations
        user_id = db.insert("users", {"name": "Alice", "email": "alice@example.com", "age": 30})
        runner.test("insert returns row ID", user_id is not None and user_id > 0)
        
        inserted = db.insert_many("users", [
            {"name": "Bob", "email": "bob@example.com", "age": 25},
            {"name": "Charlie", "email": "charlie@example.com", "age": 35},
            {"name": "Diana", "email": "diana@example.com", "age": 28}
        ])
        runner.test("insert_many inserts multiple rows", inserted == 3)
        
        # Query operations
        all_users = db.query("users")
        runner.test("query returns all rows", len(all_users) == 4)
        
        alice = db.query("users", where={"name": "Alice"})
        runner.test("query with where clause", len(alice) == 1 and alice[0]["email"] == "alice@example.com")
        
        names_only = db.query("users", columns=["name", "age"])
        runner.test("query with column selection", "name" in names_only[0] and "email" not in names_only[0])
        
        ordered = db.query("users", order_by="age ASC")
        runner.test("query with order_by", ordered[0]["age"] <= ordered[-1]["age"])
        
        limited = db.query("users", limit=2)
        runner.test("query with limit", len(limited) == 2)
        
        # Update operations
        updated = db.update("users", {"age": 31}, where={"name": "Alice"})
        runner.test("update modifies rows", updated == 1)
        
        alice_updated = db.query("users", where={"name": "Alice"})
        runner.test("update persists changes", alice_updated[0]["age"] == 31)
        
        # Delete operations
        deleted = db.delete("users", where={"name": "Diana"})
        runner.test("delete removes rows", deleted == 1)
        
        remaining = db.query("users")
        runner.test("delete persists changes", len(remaining) == 3)
        
        # Table info
        info = db.get_table_info("users")
        runner.test("get_table_info returns columns", len(info) == 4)
        runner.test("get_table_info has column names", any(col["name"] == "name" for col in info))
        
        # Raw SQL
        count_result = db.execute("SELECT COUNT(*) as count FROM users")
        runner.test("execute SELECT query", len(count_result) == 1)
        
        # Transaction
        with db.transaction() as conn:
            db.insert("users", {"name": "Eve", "email": "eve@example.com", "age": 22}, _conn=conn)
            db.insert("users", {"name": "Frank", "email": "frank@example.com", "age": 33}, _conn=conn)
        
        runner.test("transaction commits on success", db.query("users", where={"name": "Eve"}))
        
        # Drop table
        runner.test("drop_table removes table", db.drop_table("users"))
        runner.test("table_exists after drop", not db.table_exists("users"))
        
    finally:
        db.close()


def run_csv_tests(runner: TestRunner) -> None:
    """Run CSV database tests."""
    print("\n" + "="*60)
    print("  CSV Database Tests")
    print("="*60)
    
    csv_path = os.path.join(runner.temp_dir, "test.csv")
    csv_db = CSVDatabase(csv_path)
    
    try:
        # Write operations
        data = [
            {"name": "Alice", "age": "30", "city": "New York"},
            {"name": "Bob", "age": "25", "city": "London"},
            {"name": "Charlie", "age": "35", "city": "Paris"}
        ]
        written = csv_db.write(data)
        runner.test("write creates file", written == 3 and os.path.exists(csv_path))
        
        # Read operations
        read_data = csv_db.read()
        runner.test("read returns data", len(read_data) == 3)
        runner.test("read preserves fields", read_data[0]["name"] == "Alice")
        
        # Query operations
        alice = csv_db.query(where={"name": "Alice"})
        runner.test("query with where", len(alice) == 1)
        
        names_only = csv_db.query(columns=["name", "city"])
        runner.test("query with columns", "name" in names_only[0] and "age" not in names_only[0])
        
        sorted_data = csv_db.query(order_by="-age")
        runner.test("query with sort descending", sorted_data[0]["age"] >= sorted_data[-1]["age"])
        
        limited = csv_db.query(limit=2)
        runner.test("query with limit", len(limited) == 2)
        
        # Append operations
        appended = csv_db.append({"name": "Diana", "age": "28", "city": "Tokyo"})
        runner.test("append adds row", appended == 1)
        
        all_data = csv_db.read()
        runner.test("append persists", len(all_data) == 4)
        
        # Update operations
        updated = csv_db.update({"age": "31"}, where={"name": "Alice"})
        runner.test("update modifies rows", updated == 1)
        
        # Delete operations
        deleted = csv_db.delete(where={"name": "Diana"})
        runner.test("delete removes rows", deleted == 1)
        
        remaining = csv_db.read()
        runner.test("delete persists", len(remaining) == 3)
        
    finally:
        csv_db.close()


def run_json_tests(runner: TestRunner) -> None:
    """Run JSON database tests."""
    print("\n" + "="*60)
    print("  JSON Database Tests")
    print("="*60)
    
    json_path = os.path.join(runner.temp_dir, "test.json")
    json_db = JSONDatabase(json_path)
    
    try:
        # Write operations
        data = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "London"},
            {"name": "Charlie", "age": 35, "city": "Paris"}
        ]
        runner.test("write creates file", json_db.write(data))
        runner.test("file exists", os.path.exists(json_path))
        
        # Read operations
        read_data = json_db.read()
        runner.test("read returns data", len(read_data) == 3)
        runner.test("read preserves types", read_data[0]["age"] == 30)
        
        # Query operations
        alice = json_db.query(where={"name": "Alice"})
        runner.test("query with where", len(alice) == 1)
        
        limited = json_db.query(limit=2)
        runner.test("query with limit", len(limited) == 2)
        
        # Insert operations
        inserted = json_db.insert({"name": "Diana", "age": 28, "city": "Tokyo"})
        runner.test("insert adds item", inserted == 1)
        
        all_data = json_db.read()
        runner.test("insert persists", len(all_data) == 4)
        
        # Update operations
        updated = json_db.update({"age": 31}, where={"name": "Alice"})
        runner.test("update modifies items", updated == 1)
        
        # Delete operations
        deleted = json_db.delete(where={"name": "Diana"})
        runner.test("delete removes items", deleted == 1)
        
        remaining = json_db.read()
        runner.test("delete persists", len(remaining) == 3)
        
    finally:
        json_db.close()


def run_export_import_tests(runner: TestRunner) -> None:
    """Run export/import tests."""
    print("\n" + "="*60)
    print("  Export/Import Tests")
    print("="*60)
    
    data = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "London"}
    ]
    
    # CSV export/import
    csv_path = os.path.join(runner.temp_dir, "export.csv")
    exported = export_to_csv(data, csv_path)
    runner.test("export_to_csv writes file", exported == 2)
    
    imported = import_from_csv(csv_path)
    runner.test("import_from_csv reads data", len(imported) == 2)
    
    # JSON export/import
    json_path = os.path.join(runner.temp_dir, "export.json")
    runner.test("export_to_json writes file", export_to_json(data, json_path))
    
    imported_json = import_from_json(json_path)
    runner.test("import_from_json reads data", len(imported_json) == 2)
    
    # Format conversion
    csv_to_json_path = os.path.join(runner.temp_dir, "converted.json")
    runner.test("convert_csv_to_json", convert_csv_to_json(csv_path, csv_to_json_path))
    
    json_to_csv_path = os.path.join(runner.temp_dir, "converted.csv")
    converted_rows = convert_json_to_csv(json_path, json_to_csv_path)
    runner.test("convert_json_to_csv", converted_rows == 2)


def run_convenience_tests(runner: TestRunner) -> None:
    """Run convenience function tests."""
    print("\n" + "="*60)
    print("  Convenience Function Tests")
    print("="*60)
    
    # SQLite convenience
    db_path = os.path.join(runner.temp_dir, "convenience.db")
    db = sqlite_connect(db_path)
    runner.test("sqlite_connect creates instance", isinstance(db, SQLiteDatabase))
    db.create_table("test", {"id": "INTEGER PRIMARY KEY", "value": "TEXT"})
    runner.test("sqlite_connect instance works", db.table_exists("test"))
    db.close()
    
    # CSV convenience
    csv_path = os.path.join(runner.temp_dir, "convenience.csv")
    csv_db = csv_connect(csv_path)
    runner.test("csv_connect creates instance", isinstance(csv_db, CSVDatabase))
    csv_db.close()
    
    # JSON convenience
    json_path = os.path.join(runner.temp_dir, "convenience.json")
    json_db = json_connect(json_path)
    runner.test("json_connect creates instance", isinstance(json_db, JSONDatabase))
    json_db.close()


def run_edge_case_tests(runner: TestRunner) -> None:
    """Run edge case tests."""
    print("\n" + "="*60)
    print("  Edge Case Tests")
    print("="*60)
    
    # Empty data
    csv_path = os.path.join(runner.temp_dir, "empty.csv")
    csv_db = CSVDatabase(csv_path)
    runner.test("CSV write empty data", csv_db.write([]) == 0)
    runner.test("CSV read non-existent", csv_db.read() == [])
    csv_db.close()
    
    json_path = os.path.join(runner.temp_dir, "empty.json")
    json_db = JSONDatabase(json_path)
    runner.test("JSON read non-existent", json_db.read() == [])
    json_db.close()
    
    # SQLite with special characters
    db_path = os.path.join(runner.temp_dir, "special.db")
    db = SQLiteDatabase(db_path)
    db.create_table("special", {"id": "INTEGER PRIMARY KEY", "text": "TEXT"})
    db.insert("special", {"text": "Hello 'World' with \"quotes\""})
    result = db.query("special")
    runner.test("SQLite handles quotes", len(result) == 1)
    db.close()
    
    # Unicode support
    json_path = os.path.join(runner.temp_dir, "unicode.json")
    unicode_data = [{"name": "张三", "city": "北京"}, {"name": "李四", "city": "上海"}]
    json_db = JSONDatabase(json_path)
    runner.test("JSON unicode write", json_db.write(unicode_data))
    read_back = json_db.read()
    runner.test("JSON unicode read", read_back[0]["name"] == "张三")
    json_db.close()


def run_tests() -> bool:
    """Run all tests."""
    runner = TestRunner()
    
    try:
        runner.setup()
        
        run_sqlite_tests(runner)
        run_csv_tests(runner)
        run_json_tests(runner)
        run_export_import_tests(runner)
        run_convenience_tests(runner)
        run_edge_case_tests(runner)
        
        return runner.report()
    
    finally:
        runner.teardown()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
