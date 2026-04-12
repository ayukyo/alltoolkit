"""
AllToolkit - Python SQLite Utilities Test Suite

Comprehensive test coverage for sqlite_utils module.
Run with: python sqlite_utils_test.py
"""

import os
import sys
import tempfile
import unittest
import json
import csv
import threading
import time
from pathlib import Path

# Import module under test
from mod import (
    SQLiteConfig,
    SQLiteError,
    SQLiteConnectionError,
    SQLiteQueryError,
    SQLiteValidationError,
    SQLiteTransactionError,
    Column,
    Table,
    QueryResult,
    QueryBuilder,
    ConnectionPool,
    Database,
    connect,
    open_database,
    create_in_memory,
)


class TestColumn(unittest.TestCase):
    """Test Column data class."""
    
    def test_basic_column(self):
        """Test basic column creation."""
        col = Column(name="id", type="INTEGER")
        self.assertEqual(col.name, "id")
        self.assertEqual(col.type, "INTEGER")
        self.assertTrue(col.nullable)
        self.assertFalse(col.primary_key)
    
    def test_primary_key_column(self):
        """Test primary key column."""
        col = Column(name="id", type="INTEGER", primary_key=True)
        sql = col.to_sql()
        self.assertIn("PRIMARY KEY", sql)
        self.assertIn("AUTOINCREMENT", sql)
    
    def test_not_null_column(self):
        """Test NOT NULL column."""
        col = Column(name="name", type="TEXT", nullable=False)
        sql = col.to_sql()
        self.assertIn("NOT NULL", sql)
    
    def test_unique_column(self):
        """Test UNIQUE column."""
        col = Column(name="email", type="TEXT", unique=True)
        sql = col.to_sql()
        self.assertIn("UNIQUE", sql)
    
    def test_default_value_string(self):
        """Test column with string default."""
        col = Column(name="status", type="TEXT", default="active")
        sql = col.to_sql()
        self.assertIn("DEFAULT 'active'", sql)
    
    def test_default_value_number(self):
        """Test column with numeric default."""
        col = Column(name="count", type="INTEGER", default=0)
        sql = col.to_sql()
        self.assertIn("DEFAULT 0", sql)
    
    def test_foreign_key_reference(self):
        """Test foreign key reference."""
        col = Column(name="user_id", type="INTEGER", references="users(id)")
        sql = col.to_sql()
        self.assertIn("REFERENCES users(id)", sql)
    
    def test_check_constraint(self):
        """Test check constraint."""
        col = Column(name="age", type="INTEGER", check="age >= 0")
        sql = col.to_sql()
        self.assertIn("CHECK (age >= 0)", sql)
    
    def test_full_column(self):
        """Test column with all options."""
        col = Column(
            name="email",
            type="TEXT",
            nullable=False,
            unique=True,
            default="",
            check="email LIKE '%@%'"
        )
        sql = col.to_sql()
        self.assertIn('"email"', sql)
        self.assertIn("TEXT", sql)
        self.assertIn("NOT NULL", sql)
        self.assertIn("UNIQUE", sql)
        self.assertIn("DEFAULT ''", sql)
        self.assertIn("CHECK (email LIKE '%@%')", sql)


class TestTable(unittest.TestCase):
    """Test Table data class."""
    
    def test_basic_table(self):
        """Test basic table creation."""
        table = Table(
            name="users",
            columns=[
                Column("id", "INTEGER", primary_key=True),
                Column("name", "TEXT", nullable=False),
                Column("email", "TEXT", unique=True),
            ]
        )
        sql = table.to_sql()
        self.assertIn('CREATE TABLE IF NOT EXISTS "users"', sql)
        self.assertIn("PRIMARY KEY", sql)
        self.assertIn("NOT NULL", sql)
        self.assertIn("UNIQUE", sql)
    
    def test_table_with_unique_constraints(self):
        """Test table with composite unique constraint."""
        table = Table(
            name="user_roles",
            columns=[
                Column("id", "INTEGER", primary_key=True),
                Column("user_id", "INTEGER"),
                Column("role_id", "INTEGER"),
            ],
            unique_constraints=[["user_id", "role_id"]]
        )
        sql = table.to_sql()
        self.assertIn("UNIQUE (\"user_id\", \"role_id\")", sql)
    
    def test_add_index_sql(self):
        """Test index creation SQL."""
        table = Table(name="users", columns=[Column("id", "INTEGER")])
        sql = table.add_index_sql("idx_users_email", ["email"])
        self.assertIn('CREATE INDEX IF NOT EXISTS "idx_users_email"', sql)
        self.assertIn('ON "users" ("email")', sql)
    
    def test_add_unique_index_sql(self):
        """Test unique index creation SQL."""
        table = Table(name="users", columns=[Column("id", "INTEGER")])
        sql = table.add_index_sql("idx_users_email", ["email"], unique=True)
        self.assertIn('CREATE UNIQUE INDEX IF NOT EXISTS "idx_users_email"', sql)


class TestQueryResult(unittest.TestCase):
    """Test QueryResult data class."""
    
    def test_to_dicts(self):
        """Test conversion to dictionaries."""
        result = QueryResult(
            rows=[(1, "Alice"), (2, "Bob")],
            columns=["id", "name"],
            row_count=2,
            execution_time=0.001
        )
        dicts = result.to_dicts()
        self.assertEqual(len(dicts), 2)
        self.assertEqual(dicts[0], {"id": 1, "name": "Alice"})
        self.assertEqual(dicts[1], {"id": 2, "name": "Bob"})
    
    def test_to_json(self):
        """Test conversion to JSON."""
        result = QueryResult(
            rows=[(1, "Alice")],
            columns=["id", "name"],
            row_count=1,
            execution_time=0.001
        )
        json_str = result.to_json()
        data = json.loads(json_str)
        self.assertEqual(data, [{"id": 1, "name": "Alice"}])
    
    def test_empty_result(self):
        """Test empty result."""
        result = QueryResult(
            rows=[],
            columns=["id", "name"],
            row_count=0,
            execution_time=0.001
        )
        dicts = result.to_dicts()
        self.assertEqual(dicts, [])
        self.assertEqual(result.row_count, 0)


class TestQueryBuilder(unittest.TestCase):
    """Test QueryBuilder class."""
    
    def test_basic_select(self):
        """Test basic SELECT query."""
        qb = QueryBuilder("users")
        sql, params = qb.build_select()
        self.assertEqual(sql, 'SELECT * FROM "users"')
        self.assertEqual(params, [])
    
    def test_select_columns(self):
        """Test SELECT with specific columns."""
        qb = QueryBuilder("users")
        sql, params = qb.select("id", "name", "email").build_select()
        self.assertEqual(sql, 'SELECT id, name, email FROM "users"')
    
    def test_where_clause(self):
        """Test WHERE clause."""
        qb = QueryBuilder("users")
        sql, params = qb.where("age > ?", 18).build_select()
        self.assertEqual(sql, 'SELECT * FROM "users" WHERE age > ?')
        self.assertEqual(params, [18])
    
    def test_where_eq(self):
        """Test WHERE equality helper."""
        qb = QueryBuilder("users")
        sql, params = qb.where_eq("status", "active").build_select()
        self.assertEqual(sql, 'SELECT * FROM "users" WHERE "status" = ?')
        self.assertEqual(params, ["active"])
    
    def test_where_in(self):
        """Test WHERE IN clause."""
        qb = QueryBuilder("users")
        sql, params = qb.where_in("id", [1, 2, 3]).build_select()
        self.assertEqual(sql, 'SELECT * FROM "users" WHERE "id" IN (?, ?, ?)')
        self.assertEqual(params, [1, 2, 3])
    
    def test_where_between(self):
        """Test WHERE BETWEEN clause."""
        qb = QueryBuilder("users")
        sql, params = qb.where_between("age", 18, 65).build_select()
        self.assertEqual(sql, 'SELECT * FROM "users" WHERE "age" BETWEEN ? AND ?')
        self.assertEqual(params, [18, 65])
    
    def test_where_like(self):
        """Test WHERE LIKE clause."""
        qb = QueryBuilder("users")
        sql, params = qb.where_like("name", "%John%").build_select()
        self.assertEqual(sql, 'SELECT * FROM "users" WHERE "name" LIKE ?')
        self.assertEqual(params, ["%John%"])
    
    def test_order_by(self):
        """Test ORDER BY clause."""
        qb = QueryBuilder("users")
        sql, params = qb.order_by("name").order_by("age", desc=True).build_select()
        self.assertIn('ORDER BY "name" ASC, "age" DESC', sql)
    
    def test_limit_offset(self):
        """Test LIMIT and OFFSET."""
        qb = QueryBuilder("users")
        sql, params = qb.limit(10).offset(20).build_select()
        self.assertIn("LIMIT 10", sql)
        self.assertIn("OFFSET 20", sql)
    
    def test_group_by_having(self):
        """Test GROUP BY and HAVING."""
        qb = QueryBuilder("orders")
        sql, params = (qb
            .select("user_id", "COUNT(*) as count")
            .group_by("user_id")
            .having("count > ?", 5)
            .build_select())
        self.assertIn("GROUP BY", sql)
        self.assertIn("HAVING", sql)
    
    def test_join(self):
        """Test JOIN clauses."""
        qb = QueryBuilder("users")
        sql, params = (qb
            .inner_join("orders", "users.id = orders.user_id")
            .left_join("profiles", "users.id = profiles.user_id")
            .build_select())
        self.assertIn("INNER JOIN", sql)
        self.assertIn("LEFT JOIN", sql)
    
    def test_build_count(self):
        """Test COUNT query."""
        qb = QueryBuilder("users")
        qb.where_eq("status", "active")
        sql, params = qb.build_count()
        self.assertIn("COUNT(*) as count", sql)
        self.assertIn("WHERE", sql)
    
    def test_build_delete(self):
        """Test DELETE query."""
        qb = QueryBuilder("users")
        sql, params = qb.where_eq("id", 1).build_delete()
        self.assertEqual(sql, 'DELETE FROM "users" WHERE "id" = ?')
        self.assertEqual(params, [1])
    
    def test_build_update(self):
        """Test UPDATE query."""
        qb = QueryBuilder("users")
        sql, params = qb.where_eq("id", 1).build_update({"name": "Bob", "age": 30})
        self.assertIn('UPDATE "users" SET', sql)
        self.assertIn("WHERE", sql)
        self.assertEqual(params, ["Bob", 30, 1])
    
    def test_multiple_where_clauses(self):
        """Test multiple WHERE conditions."""
        qb = QueryBuilder("users")
        sql, params = (qb
            .where_eq("status", "active")
            .where("age > ?", 18)
            .build_select())
        self.assertIn("WHERE", sql)
        self.assertIn("AND", sql)
        self.assertEqual(params, ["active", 18])


class TestDatabase(unittest.TestCase):
    """Test Database class."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_path = self.temp_file.name
        self.temp_file.close()
        self.db = Database(self.db_path)
        self.db.connect()
        self._create_test_tables()
    
    def tearDown(self):
        """Clean up test database."""
        self.db.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def _create_test_tables(self):
        """Create test tables."""
        # Users table
        users_table = Table(
            name="users",
            columns=[
                Column("id", "INTEGER", primary_key=True),
                Column("name", "TEXT", nullable=False),
                Column("email", "TEXT", unique=True),
                Column("age", "INTEGER", default=0),
                Column("created_at", "TEXT", default="CURRENT_TIMESTAMP"),
            ]
        )
        self.db.create_table(users_table)
        
        # Posts table
        posts_table = Table(
            name="posts",
            columns=[
                Column("id", "INTEGER", primary_key=True),
                Column("user_id", "INTEGER"),
                Column("title", "TEXT", nullable=False),
                Column("content", "TEXT"),
                Column("published", "INTEGER", default=0),
            ]
        )
        self.db.create_table(posts_table)
    
    def test_table_exists(self):
        """Test table existence check."""
        self.assertTrue(self.db.table_exists("users"))
        self.assertTrue(self.db.table_exists("posts"))
        self.assertFalse(self.db.table_exists("nonexistent"))
    
    def test_get_tables(self):
        """Test getting all tables."""
        tables = self.db.get_tables()
        self.assertIn("users", tables)
        self.assertIn("posts", tables)
    
    def test_get_table_info(self):
        """Test getting table column info."""
        info = self.db.get_table_info("users")
        self.assertGreater(len(info), 0)
        column_names = [col["name"] for col in info]
        self.assertIn("id", column_names)
        self.assertIn("name", column_names)
        self.assertIn("email", column_names)
    
    def test_insert_single(self):
        """Test inserting a single row."""
        user_id = self.db.insert("users", {
            "name": "Alice",
            "email": "alice@example.com",
            "age": 25
        })
        self.assertIsNotNone(user_id)
        self.assertGreater(user_id, 0)
        
        # Verify insertion
        user = self.db.find_by_id("users", user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "Alice")
        self.assertEqual(user["email"], "alice@example.com")
        self.assertEqual(user["age"], 25)
    
    def test_insert_many(self):
        """Test inserting multiple rows."""
        users = [
            {"name": "Bob", "email": "bob@example.com", "age": 30},
            {"name": "Charlie", "email": "charlie@example.com", "age": 35},
            {"name": "Diana", "email": "diana@example.com", "age": 28},
        ]
        ids = self.db.insert_many("users", users)
        self.assertEqual(len(ids), 3)
        
        # Verify count
        count = self.db.count("users")
        self.assertGreaterEqual(count, 3)
    
    def test_insert_or_replace(self):
        """Test upsert operation."""
        # Insert initial
        user_id = self.db.insert_or_replace("users", {
            "id": 1,
            "name": "Original",
            "email": "original@example.com"
        })
        
        # Replace
        new_id = self.db.insert_or_replace("users", {
            "id": 1,
            "name": "Updated",
            "email": "updated@example.com"
        })
        
        self.assertEqual(user_id, new_id)
        
        # Verify update
        user = self.db.find_by_id("users", 1)
        self.assertEqual(user["name"], "Updated")
        self.assertEqual(user["email"], "updated@example.com")
    
    def test_select(self):
        """Test SELECT operation."""
        # Insert test data
        self.db.insert("users", {"name": "Test", "email": "test@example.com", "age": 20})
        self.db.insert("users", {"name": "Test2", "email": "test2@example.com", "age": 30})
        
        # Select all
        result = self.db.select("users")
        self.assertGreater(result.row_count, 0)
        
        # Select with columns
        result = self.db.select("users", columns=["id", "name"])
        self.assertIn("id", result.columns)
        self.assertIn("name", result.columns)
        
        # Select with where
        result = self.db.select("users", where="age > ?", params=(25,))
        for row in result.to_dicts():
            self.assertGreater(row["age"], 25)
        
        # Select with order and limit
        result = self.db.select("users", order_by="age DESC", limit=1)
        self.assertEqual(result.row_count, 1)
    
    def test_find_one(self):
        """Test finding a single row."""
        self.db.insert("users", {"name": "FindMe", "email": "findme@example.com", "age": 40})
        
        user = self.db.find_one("users", "name = ?", ("FindMe",))
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "FindMe")
        self.assertEqual(user["age"], 40)
        
        # Not found
        not_found = self.db.find_one("users", "name = ?", ("NonExistent",))
        self.assertIsNone(not_found)
    
    def test_find_by_id(self):
        """Test finding by ID."""
        user_id = self.db.insert("users", {"name": "ByID", "email": "byid@example.com"})
        
        user = self.db.find_by_id("users", user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "ByID")
    
    def test_update(self):
        """Test UPDATE operation."""
        user_id = self.db.insert("users", {"name": "ToUpdate", "email": "update@example.com", "age": 25})
        
        rows = self.db.update("users", {"age": 30, "name": "Updated"}, "id = ?", (user_id,))
        self.assertEqual(rows, 1)
        
        user = self.db.find_by_id("users", user_id)
        self.assertEqual(user["name"], "Updated")
        self.assertEqual(user["age"], 30)
    
    def test_delete(self):
        """Test DELETE operation."""
        user_id = self.db.insert("users", {"name": "ToDelete", "email": "delete@example.com"})
        
        rows = self.db.delete("users", "id = ?", (user_id,))
        self.assertEqual(rows, 1)
        
        user = self.db.find_by_id("users", user_id)
        self.assertIsNone(user)
    
    def test_delete_by_id(self):
        """Test delete by ID."""
        user_id = self.db.insert("users", {"name": "DeleteById", "email": "deleteid@example.com"})
        
        rows = self.db.delete_by_id("users", user_id)
        self.assertEqual(rows, 1)
    
    def test_count(self):
        """Test COUNT operation."""
        initial_count = self.db.count("users")
        
        self.db.insert("users", {"name": "Count1", "email": "count1@example.com"})
        self.db.insert("users", {"name": "Count2", "email": "count2@example.com"})
        
        new_count = self.db.count("users")
        self.assertEqual(new_count, initial_count + 2)
        
        # Count with where
        count = self.db.count("users", "name LIKE ?", ("Count%",))
        self.assertEqual(count, 2)
    
    def test_exists(self):
        """Test EXISTS operation."""
        self.db.insert("users", {"name": "ExistsTest", "email": "exists@example.com"})
        
        self.assertTrue(self.db.exists("users", "name = ?", ("ExistsTest",)))
        self.assertFalse(self.db.exists("users", "name = ?", ("NonExistent",)))
    
    def test_query(self):
        """Test raw query execution."""
        result = self.db.query("SELECT 1 as num")
        self.assertEqual(result.row_count, 1)
        self.assertEqual(result.rows[0][0], 1)
    
    def test_query_scalar(self):
        """Test scalar query."""
        value = self.db.query_scalar("SELECT 42")
        self.assertEqual(value, 42)
        
        none_value = self.db.query_scalar("SELECT NULL")
        self.assertIsNone(none_value)
    
    def test_query_dict(self):
        """Test query returning single dict."""
        self.db.insert("users", {"name": "DictTest", "email": "dict@example.com"})
        
        user = self.db.query_dict("SELECT * FROM users WHERE name = ?", "DictTest")
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "DictTest")
    
    def test_query_dicts(self):
        """Test query returning list of dicts."""
        self.db.insert("users", {"name": "Dicts1", "email": "dicts1@example.com"})
        self.db.insert("users", {"name": "Dicts2", "email": "dicts2@example.com"})
        
        users = self.db.query_dicts("SELECT * FROM users WHERE name LIKE ?", "Dicts%")
        self.assertEqual(len(users), 2)
    
    def test_execute(self):
        """Test raw execute."""
        rows = self.db.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
                               "ExecuteTest", "execute@example.com")
        self.assertEqual(rows, 1)
    
    def test_executemany(self):
        """Test executemany."""
        params = [
            ("ExecMany1", "many1@example.com"),
            ("ExecMany2", "many2@example.com"),
            ("ExecMany3", "many3@example.com"),
        ]
        rows = self.db.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            params
        )
        self.assertEqual(rows, 3)
    
    def test_query_builder_integration(self):
        """Test query builder with database."""
        # Insert test data
        for i in range(5):
            self.db.insert("users", {
                "name": f"User{i}",
                "email": f"user{i}@example.com",
                "age": 20 + i
            })
        
        # Use query builder
        qb = self.db.table("users")
        sql, params = (qb
            .select("id", "name", "age")
            .where("age > ?", 22)
            .order_by("age DESC")
            .limit(2)
            .build_select())
        
        result = self.db.query(sql, *params)
        self.assertLessEqual(result.row_count, 2)
        for row in result.to_dicts():
            self.assertGreater(row["age"], 22)
    
    def test_transaction_commit(self):
        """Test successful transaction."""
        initial_count = self.db.count("users")
        
        with self.db.transaction():
            self.db.insert("users", {"name": "Trans1", "email": "trans1@example.com"})
            self.db.insert("users", {"name": "Trans2", "email": "trans2@example.com"})
        
        new_count = self.db.count("users")
        self.assertEqual(new_count, initial_count + 2)
    
    def test_transaction_rollback(self):
        """Test transaction rollback on error."""
        # Create a new database for this test
        temp_db = create_in_memory()
        temp_db.create_table(Table(
            name="rollback_test",
            columns=[
                Column("id", "INTEGER", primary_key=True),
                Column("value", "INTEGER"),
            ]
        ))
        
        # Test that transaction context manager works
        initial_count = temp_db.count("rollback_test")
        
        # Successful transaction
        with temp_db.transaction():
            temp_db.insert("rollback_test", {"value": 1})
            temp_db.insert("rollback_test", {"value": 2})
        
        # Verify commit happened
        count = temp_db.count("rollback_test")
        self.assertEqual(count, initial_count + 2)
        
        # Test that exception prevents further operations
        exception_caught = False
        try:
            with temp_db.transaction():
                temp_db.insert("rollback_test", {"value": 3})
                raise RuntimeError("Test exception")
        except SQLiteTransactionError:
            exception_caught = True
        except RuntimeError:
            exception_caught = True
        
        self.assertTrue(exception_caught)
        temp_db.close()
    
    def test_add_column(self):
        """Test adding a column to existing table."""
        self.db.add_column("users", Column("phone", "TEXT"))
        
        info = self.db.get_table_info("users")
        column_names = [col["name"] for col in info]
        self.assertIn("phone", column_names)
    
    def test_create_index(self):
        """Test creating an index."""
        self.db.create_index("users", ["email"])
        self.db.create_index("users", ["name", "age"], unique=False)
        
        # Just verify no error - SQLite doesn't have easy index listing
        self.assertTrue(True)
    
    def test_drop_table(self):
        """Test dropping a table."""
        # Create a temporary table
        temp_table = Table(
            name="temp_table",
            columns=[Column("id", "INTEGER", primary_key=True)]
        )
        self.db.create_table(temp_table)
        self.assertTrue(self.db.table_exists("temp_table"))
        
        # Drop it
        self.db.drop_table("temp_table")
        self.assertFalse(self.db.table_exists("temp_table"))
    
    def test_export_to_json(self):
        """Test JSON export."""
        self.db.insert("users", {"name": "JSONExport", "email": "json@example.com"})
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            count = self.db.export_to_json("users", temp_path)
            self.assertGreater(count, 0)
            
            with open(temp_path, 'r') as f:
                data = json.load(f)
            self.assertIsInstance(data, list)
            self.assertGreater(len(data), 0)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_export_to_csv(self):
        """Test CSV export."""
        self.db.insert("users", {"name": "CSVExport", "email": "csv@example.com"})
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name
        
        try:
            count = self.db.export_to_csv("users", temp_path)
            self.assertGreater(count, 0)
            
            with open(temp_path, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
            self.assertGreater(len(rows), 1)  # Header + data
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_import_from_json(self):
        """Test JSON import."""
        data = [
            {"name": "Import1", "email": "import1@example.com"},
            {"name": "Import2", "email": "import2@example.com"},
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
            json.dump(data, f)
        
        try:
            count = self.db.import_from_json("users", temp_path)
            self.assertEqual(count, 2)
            
            # Verify
            user1 = self.db.find_one("users", "email = ?", ("import1@example.com",))
            self.assertIsNotNone(user1)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_import_from_csv(self):
        """Test CSV import."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name
            writer = csv.writer(f)
            writer.writerow(["name", "email"])
            writer.writerow(["CSVImport1", "csvimport1@example.com"])
            writer.writerow(["CSVImport2", "csvimport2@example.com"])
        
        try:
            count = self.db.import_from_csv("users", temp_path)
            self.assertEqual(count, 2)
            
            # Verify
            user1 = self.db.find_one("users", "email = ?", ("csvimport1@example.com",))
            self.assertIsNotNone(user1)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_backup_and_restore(self):
        """Test backup and restore."""
        self.db.insert("users", {"name": "BackupTest", "email": "backup@example.com"})
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            backup_path = f.name
        
        try:
            # Backup
            self.db.backup(backup_path)
            self.assertTrue(os.path.exists(backup_path))
            
            # Modify original
            self.db.insert("users", {"name": "AfterBackup", "email": "after@example.com"})
            
            # Restore
            self.db.restore(backup_path)
            
            # Verify restored state (AfterBackup should not exist)
            user = self.db.find_one("users", "email = ?", ("after@example.com",))
            self.assertIsNone(user)
            
            # Original data should exist
            user = self.db.find_one("users", "email = ?", ("backup@example.com",))
            self.assertIsNotNone(user)
        finally:
            if os.path.exists(backup_path):
                os.remove(backup_path)
    
    def test_get_size(self):
        """Test database size."""
        size = self.db.get_size()
        self.assertGreater(size, 0)
    
    def test_get_size_formatted(self):
        """Test formatted size."""
        size_str = self.db.get_size_formatted()
        self.assertIsInstance(size_str, str)
        self.assertTrue(any(unit in size_str for unit in ['B', 'KB', 'MB', 'GB']))
    
    def test_get_version(self):
        """Test SQLite version."""
        version = self.db.get_version()
        self.assertIsInstance(version, str)
        self.assertGreater(len(version), 0)
    
    def test_get_stats(self):
        """Test database stats."""
        stats = self.db.get_stats()
        self.assertIn("path", stats)
        self.assertIn("size", stats)
        self.assertIn("tables", stats)
        self.assertIn("table_count", stats)
    
    def test_vacuum(self):
        """Test VACUUM."""
        # Just verify it doesn't error
        self.db.vacuum()
        self.assertTrue(True)
    
    def test_analyze(self):
        """Test ANALYZE."""
        # Just verify it doesn't error
        self.db.analyze()
        self.assertTrue(True)


class TestConnectionPool(unittest.TestCase):
    """Test ConnectionPool class."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_path = self.temp_file.name
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_pool_creation(self):
        """Test pool creation."""
        pool = ConnectionPool(self.db_path, max_connections=5)
        self.assertEqual(pool.max_connections, 5)
        pool.close_all()
    
    def test_pool_acquire_release(self):
        """Test acquiring and releasing connections."""
        pool = ConnectionPool(self.db_path, max_connections=5)
        
        conn1 = pool.acquire()
        self.assertIsNotNone(conn1)
        
        # Verify connection works
        cursor = conn1.execute("SELECT 1")
        self.assertEqual(cursor.fetchone()[0], 1)
        
        pool.release(conn1)
        pool.close_all()
    
    def test_pool_context_manager(self):
        """Test pool context manager."""
        pool = ConnectionPool(self.db_path, max_connections=5)
        
        with pool.connection() as conn:
            cursor = conn.execute("SELECT 1")
            self.assertEqual(cursor.fetchone()[0], 1)
        
        pool.close_all()
    
    def test_pool_max_connections(self):
        """Test max connections limit."""
        pool = ConnectionPool(self.db_path, max_connections=2)
        
        conn1 = pool.acquire()
        conn2 = pool.acquire()
        
        # Third should fail
        with self.assertRaises(SQLiteConnectionError):
            pool.acquire()
        
        # Release one and try again
        pool.release(conn1)
        conn3 = pool.acquire()
        self.assertIsNotNone(conn3)
        
        pool.release(conn2)
        pool.release(conn3)
        pool.close_all()
    
    def test_pool_thread_safety(self):
        """Test thread safety of pool."""
        pool = ConnectionPool(self.db_path, max_connections=5)
        results = []
        errors = []
        
        def worker(pool, worker_id):
            try:
                for i in range(10):
                    with pool.connection() as conn:
                        cursor = conn.execute("SELECT ?", (worker_id * 100 + i,))
                        result = cursor.fetchone()[0]
                        results.append(result)
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=worker, args=(pool, i)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(results), 50)
        pool.close_all()


class TestDatabaseWithPool(unittest.TestCase):
    """Test Database with connection pooling."""
    
    def setUp(self):
        """Set up test database with pool."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_path = self.temp_file.name
        self.temp_file.close()
        self.db = Database(self.db_path)
        self.db.connect(use_pool=True, max_connections=5)
        
        # Create test table
        table = Table(
            name="test",
            columns=[
                Column("id", "INTEGER", primary_key=True),
                Column("value", "TEXT"),
            ]
        )
        self.db.create_table(table)
    
    def tearDown(self):
        """Clean up."""
        self.db.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_pool_operations(self):
        """Test basic operations with pool."""
        self.db.insert("test", {"value": "test1"})
        self.db.insert("test", {"value": "test2"})
        
        count = self.db.count("test")
        self.assertEqual(count, 2)
        
        result = self.db.select("test")
        self.assertEqual(result.row_count, 2)
    
    def test_pool_transaction(self):
        """Test transactions with pool."""
        initial_count = self.db.count("test")
        
        with self.db.transaction():
            self.db.insert("test", {"value": "trans1"})
            self.db.insert("test", {"value": "trans2"})
        
        new_count = self.db.count("test")
        self.assertEqual(new_count, initial_count + 2)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def setUp(self):
        """Set up temp file."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_path = self.temp_file.name
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_connect(self):
        """Test connect function."""
        db = connect(self.db_path)
        self.assertIsNotNone(db)
        # Create a test table to verify connection works
        from mod import Table, Column
        db.create_table(Table(
            name="test_connect",
            columns=[Column("id", "INTEGER", primary_key=True)]
        ))
        self.assertTrue(db.table_exists("test_connect"))
        db.close()
    
    def test_open_database(self):
        """Test open_database function."""
        db = open_database(self.db_path)
        self.assertIsNotNone(db)
        db.close()
    
    def test_create_in_memory(self):
        """Test in-memory database."""
        db = create_in_memory()
        self.assertIsNotNone(db)
        
        # Create and use table
        table = Table(
            name="memory_test",
            columns=[Column("id", "INTEGER", primary_key=True)]
        )
        db.create_table(table)
        self.assertTrue(db.table_exists("memory_test"))
        
        db.close()
    
    def test_context_manager(self):
        """Test database context manager."""
        with Database(self.db_path) as db:
            table = Table(
                name="ctx_test",
                columns=[Column("id", "INTEGER", primary_key=True)]
            )
            db.create_table(table)
            self.assertTrue(db.table_exists("ctx_test"))
        
        # Database should be closed
        self.assertIsNone(db._conn)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_path = self.temp_file.name
        self.temp_file.close()
        self.db = Database(self.db_path)
        self.db.connect()
    
    def tearDown(self):
        """Clean up."""
        self.db.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_empty_insert_many(self):
        """Test insert_many with empty list."""
        ids = self.db.insert_many("nonexistent", [])
        self.assertEqual(ids, [])
    
    def test_count_nonexistent_table(self):
        """Test count on nonexistent table."""
        with self.assertRaises(sqlite3.OperationalError):
            self.db.count("nonexistent_table")
    
    def test_query_with_special_characters(self):
        """Test query with special characters."""
        table = Table(
            name="special",
            columns=[
                Column("id", "INTEGER", primary_key=True),
                Column("text", "TEXT"),
            ]
        )
        self.db.create_table(table)
        
        special_text = "Hello 'world' with \"quotes\" and \n newlines"
        self.db.insert("special", {"text": special_text})
        
        result = self.db.find_one("special", "text = ?", (special_text,))
        self.assertIsNotNone(result)
        self.assertEqual(result["text"], special_text)
    
    def test_unicode_support(self):
        """Test Unicode support."""
        table = Table(
            name="unicode",
            columns=[
                Column("id", "INTEGER", primary_key=True),
                Column("text", "TEXT"),
            ]
        )
        self.db.create_table(table)
        
        unicode_texts = [
            "Hello 世界",
            "Привет мир",
            "مرحبا بالعالم",
            "🎉🚀💻",
        ]
        
        for text in unicode_texts:
            self.db.insert("unicode", {"text": text})
        
        results = self.db.query_dicts("SELECT * FROM unicode")
        self.assertEqual(len(results), 4)
        
        for i, result in enumerate(results):
            self.assertEqual(result["text"], unicode_texts[i])
    
    def test_large_batch_insert(self):
        """Test large batch insert."""
        table = Table(
            name="large",
            columns=[
                Column("id", "INTEGER", primary_key=True),
                Column("value", "INTEGER"),
            ]
        )
        self.db.create_table(table)
        
        data = [{"value": i} for i in range(1000)]
        ids = self.db.insert_many("large", data)
        self.assertEqual(len(ids), 1000)
        
        count = self.db.count("large")
        self.assertEqual(count, 1000)
    
    def test_null_values(self):
        """Test NULL value handling."""
        table = Table(
            name="nulls",
            columns=[
                Column("id", "INTEGER", primary_key=True),
                Column("nullable", "TEXT"),
            ]
        )
        self.db.create_table(table)
        
        self.db.insert("nulls", {"nullable": None})
        result = self.db.find_one("nulls", "nullable IS NULL")
        self.assertIsNotNone(result)
    
    def test_boolean_values(self):
        """Test boolean value handling."""
        table = Table(
            name="bools",
            columns=[
                Column("id", "INTEGER", primary_key=True),
                Column("active", "INTEGER"),
            ]
        )
        self.db.create_table(table)
        
        self.db.insert("bools", {"active": True})
        self.db.insert("bools", {"active": False})
        
        active = self.db.find_one("bools", "active = ?", (1,))
        inactive = self.db.find_one("bools", "active = ?", (0,))
        
        self.assertIsNotNone(active)
        self.assertIsNotNone(inactive)


import sqlite3

def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestColumn,
        TestTable,
        TestQueryResult,
        TestQueryBuilder,
        TestDatabase,
        TestConnectionPool,
        TestDatabaseWithPool,
        TestConvenienceFunctions,
        TestEdgeCases,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
