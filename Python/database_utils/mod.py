#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Database Utilities Module
========================================
A comprehensive database utility module for Python with minimal external dependencies.

Features:
    - SQLite database operations (create, read, update, delete)
    - CSV file operations (read, write, append, query)
    - JSON file operations (read, write, update, query)
    - Unified query interface across data sources
    - Connection pooling for SQLite
    - Transaction support
    - Data export/import between formats
    - Schema introspection

Author: AllToolkit Contributors
License: MIT
"""

import sqlite3
import csv
import json
import os
from typing import Any, Dict, List, Optional, Union, Tuple, Iterator
from collections import OrderedDict
from contextlib import contextmanager
import threading


# ============================================================================
# Type Aliases
# ============================================================================

Row = Dict[str, Any]
Rows = List[Row]
QueryResult = Union[Rows, List[Tuple]]


# ============================================================================
# SQLite Database Utilities
# ============================================================================

class SQLiteDatabase:
    """
    SQLite database wrapper with connection pooling and transaction support.
    
    Example:
        >>> db = SQLiteDatabase("example.db")
        >>> db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "email": "TEXT"})
        >>> db.insert("users", {"name": "Alice", "email": "alice@example.com"})
        >>> users = db.query("users", where={"name": "Alice"})
        >>> db.close()
    """
    
    def __init__(self, db_path: str, pool_size: int = 5):
        """
        Initialize SQLite database connection.
        
        Args:
            db_path: Path to the SQLite database file
            pool_size: Connection pool size (default: 5)
        """
        self.db_path = db_path
        self.pool_size = pool_size
        self._pool: List[sqlite3.Connection] = []
        self._lock = threading.Lock()
        self._initialize_pool()
    
    def _initialize_pool(self) -> None:
        """Initialize connection pool."""
        for _ in range(self.pool_size):
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            self._pool.append(conn)
    
    @contextmanager
    def _get_connection(self) -> Iterator[sqlite3.Connection]:
        """Get a connection from the pool."""
        conn = None
        with self._lock:
            while not self._pool:
                pass  # Wait for available connection
            conn = self._pool.pop()
        try:
            yield conn
        finally:
            with self._lock:
                self._pool.append(conn)
    
    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        """
        Context manager for transaction support.
        
        Example:
            >>> with db.transaction() as conn:
            ...     db.insert("users", {"name": "Alice"}, _conn=conn)
            ...     db.insert("users", {"name": "Bob"}, _conn=conn)
            >>> # Automatically commits on success, rolls back on exception
        """
        with self._get_connection() as conn:
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
    
    def create_table(self, table_name: str, columns: Dict[str, str], 
                     if_not_exists: bool = True) -> bool:
        """
        Create a table with the specified columns.
        
        Args:
            table_name: Name of the table
            columns: Dictionary of column names to types
            if_not_exists: Whether to use IF NOT EXISTS clause
        
        Returns:
            True if successful
        
        Example:
            >>> db.create_table("users", {
            ...     "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            ...     "name": "TEXT NOT NULL",
            ...     "email": "TEXT UNIQUE"
            ... })
        """
        if_not_exists_clause = "IF NOT EXISTS" if if_not_exists else ""
        column_defs = ", ".join(f"{name} {dtype}" for name, dtype in columns.items())
        sql = f"CREATE TABLE {if_not_exists_clause} {table_name} ({column_defs})"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        return True
    
    def drop_table(self, table_name: str, if_exists: bool = True) -> bool:
        """
        Drop a table.
        
        Args:
            table_name: Name of the table
            if_exists: Whether to use IF EXISTS clause
        
        Returns:
            True if successful
        """
        if_exists_clause = "IF EXISTS" if if_exists else ""
        sql = f"DROP TABLE {if_exists_clause} {table_name}"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        return True
    
    def insert(self, table_name: str, data: Dict[str, Any], 
               _conn: Optional[sqlite3.Connection] = None) -> int:
        """
        Insert a single row into a table.
        
        Args:
            table_name: Name of the table
            data: Dictionary of column names to values
            _conn: Optional connection (for transactions)
        
        Returns:
            Last inserted row ID
        
        Example:
            >>> db.insert("users", {"name": "Alice", "email": "alice@example.com"})
            1
        """
        columns = list(data.keys())
        placeholders = ", ".join("?" for _ in columns)
        column_names = ", ".join(columns)
        sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        
        def _do_insert(conn: sqlite3.Connection) -> int:
            cursor = conn.cursor()
            cursor.execute(sql, list(data.values()))
            conn.commit()
            return cursor.lastrowid
        
        if _conn:
            return _do_insert(_conn)
        with self._get_connection() as conn:
            return _do_insert(conn)
    
    def insert_many(self, table_name: str, data_list: List[Dict[str, Any]], 
                    batch_size: int = 100) -> int:
        """
        Insert multiple rows into a table.
        
        Args:
            table_name: Name of the table
            data_list: List of dictionaries
            batch_size: Number of rows per batch
        
        Returns:
            Total number of rows inserted
        """
        if not data_list:
            return 0
        
        columns = list(data_list[0].keys())
        placeholders = ", ".join("?" for _ in columns)
        column_names = ", ".join(columns)
        sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        
        total_inserted = 0
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for i in range(0, len(data_list), batch_size):
                batch = data_list[i:i + batch_size]
                values = [[row.get(col) for col in columns] for row in batch]
                cursor.executemany(sql, values)
                total_inserted += len(batch)
            conn.commit()
        
        return total_inserted
    
    def query(self, table_name: str, 
              columns: Optional[List[str]] = None,
              where: Optional[Dict[str, Any]] = None,
              order_by: Optional[str] = None,
              limit: Optional[int] = None,
              offset: Optional[int] = None) -> Rows:
        """
        Query rows from a table.
        
        Args:
            table_name: Name of the table
            columns: List of columns to select (None for all)
            where: Dictionary of column-value conditions
            order_by: Order by clause (e.g., "name DESC")
            limit: Maximum number of rows
            offset: Number of rows to skip
        
        Returns:
            List of dictionaries representing rows
        
        Example:
            >>> db.query("users", columns=["name", "email"], where={"active": 1})
            [{'name': 'Alice', 'email': 'alice@example.com'}]
        """
        column_str = ", ".join(columns) if columns else "*"
        sql = f"SELECT {column_str} FROM {table_name}"
        params = []
        
        if where:
            conditions = []
            for col, val in where.items():
                if val is None:
                    conditions.append(f"{col} IS NULL")
                else:
                    conditions.append(f"{col} = ?")
                    params.append(val)
            sql += " WHERE " + " AND ".join(conditions)
        
        if order_by:
            sql += f" ORDER BY {order_by}"
        
        if limit is not None:
            sql += f" LIMIT {limit}"
        
        if offset is not None:
            sql += f" OFFSET {offset}"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def update(self, table_name: str, data: Dict[str, Any], 
               where: Dict[str, Any],
               _conn: Optional[sqlite3.Connection] = None) -> int:
        """
        Update rows in a table.
        
        Args:
            table_name: Name of the table
            data: Dictionary of column names to new values
            where: Dictionary of conditions
            _conn: Optional connection (for transactions)
        
        Returns:
            Number of rows updated
        
        Example:
            >>> db.update("users", {"email": "new@example.com"}, where={"id": 1})
            1
        """
        set_clause = ", ".join(f"{col} = ?" for col in data.keys())
        sql = f"UPDATE {table_name} SET {set_clause}"
        params = list(data.values())
        
        if where:
            conditions = []
            for col, val in where.items():
                if val is None:
                    conditions.append(f"{col} IS NULL")
                else:
                    conditions.append(f"{col} = ?")
                    params.append(val)
            sql += " WHERE " + " AND ".join(conditions)
        
        def _do_update(conn: sqlite3.Connection) -> int:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.rowcount
        
        if _conn:
            return _do_update(_conn)
        with self._get_connection() as conn:
            return _do_update(conn)
    
    def delete(self, table_name: str, where: Dict[str, Any],
               _conn: Optional[sqlite3.Connection] = None) -> int:
        """
        Delete rows from a table.
        
        Args:
            table_name: Name of the table
            where: Dictionary of conditions
            _conn: Optional connection (for transactions)
        
        Returns:
            Number of rows deleted
        
        Example:
            >>> db.delete("users", where={"id": 1})
            1
        """
        conditions = []
        params = []
        for col, val in where.items():
            if val is None:
                conditions.append(f"{col} IS NULL")
            else:
                conditions.append(f"{col} = ?")
                params.append(val)
        
        sql = f"DELETE FROM {table_name} WHERE " + " AND ".join(conditions)
        
        def _do_delete(conn: sqlite3.Connection) -> int:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.rowcount
        
        if _conn:
            return _do_delete(_conn)
        with self._get_connection() as conn:
            return _do_delete(conn)
    
    def execute(self, sql: str, params: Optional[Tuple] = None,
                _conn: Optional[sqlite3.Connection] = None) -> QueryResult:
        """
        Execute a raw SQL query.
        
        Args:
            sql: SQL query string
            params: Optional parameters
            _conn: Optional connection (for transactions)
        
        Returns:
            Query results
        
        Example:
            >>> db.execute("SELECT COUNT(*) FROM users")
            [(42,)]
        """
        def _do_execute(conn: sqlite3.Connection) -> QueryResult:
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            
            # Check if it's a SELECT query
            if sql.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                return [dict(row) if isinstance(row, sqlite3.Row) else row for row in rows]
            conn.commit()
            return cursor.rowcount
        
        if _conn:
            return _do_execute(_conn)
        with self._get_connection() as conn:
            return _do_execute(conn)
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get table schema information.
        
        Args:
            table_name: Name of the table
        
        Returns:
            List of column information dictionaries
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            return [
                {
                    "cid": col[0],
                    "name": col[1],
                    "type": col[2],
                    "notnull": bool(col[3]),
                    "default": col[4],
                    "pk": bool(col[5])
                }
                for col in columns
            ]
    
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
            return cursor.fetchone() is not None
    
    def get_tables(self) -> List[str]:
        """Get list of all tables."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            return [row[0] for row in cursor.fetchall()]
    
    def close(self) -> None:
        """Close all connections in the pool."""
        with self._lock:
            for conn in self._pool:
                conn.close()
            self._pool.clear()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


# ============================================================================
# CSV File Utilities
# ============================================================================

class CSVDatabase:
    """
    CSV file wrapper with query capabilities.
    
    Example:
        >>> csv_db = CSVDatabase("data.csv")
        >>> csv_db.write([{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}])
        >>> results = csv_db.query(where={"age": 30})
        >>> csv_db.close()
    """
    
    def __init__(self, file_path: str, delimiter: str = ",", encoding: str = "utf-8"):
        """
        Initialize CSV database.
        
        Args:
            file_path: Path to the CSV file
            delimiter: Field delimiter (default: ",")
            encoding: File encoding (default: "utf-8")
        """
        self.file_path = file_path
        self.delimiter = delimiter
        self.encoding = encoding
        self._lock = threading.Lock()
    
    def read(self) -> Rows:
        """
        Read all rows from the CSV file.
        
        Returns:
            List of dictionaries representing rows
        """
        if not os.path.exists(self.file_path):
            return []
        
        with self._lock:
            with open(self.file_path, 'r', encoding=self.encoding, newline='') as f:
                reader = csv.DictReader(f, delimiter=self.delimiter)
                return list(reader)
    
    def write(self, data: Rows, fieldnames: Optional[List[str]] = None) -> int:
        """
        Write rows to the CSV file (overwrites existing).
        
        Args:
            data: List of dictionaries
            fieldnames: Column names (auto-detected if None)
        
        Returns:
            Number of rows written
        """
        if not data:
            return 0
        
        if fieldnames is None:
            fieldnames = list(data[0].keys())
        
        with self._lock:
            with open(self.file_path, 'w', encoding=self.encoding, newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=self.delimiter)
                writer.writeheader()
                writer.writerows(data)
        
        return len(data)
    
    def append(self, data: Union[Row, Rows]) -> int:
        """
        Append rows to the CSV file.
        
        Args:
            data: Single dictionary or list of dictionaries
        
        Returns:
            Number of rows appended
        """
        if isinstance(data, dict):
            data = [data]
        
        if not data:
            return 0
        
        fieldnames = list(data[0].keys())
        file_exists = os.path.exists(self.file_path)
        
        with self._lock:
            with open(self.file_path, 'a', encoding=self.encoding, newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=self.delimiter)
                if not file_exists:
                    writer.writeheader()
                writer.writerows(data)
        
        return len(data)
    
    def query(self, columns: Optional[List[str]] = None,
              where: Optional[Dict[str, Any]] = None,
              order_by: Optional[str] = None,
              limit: Optional[int] = None) -> Rows:
        """
        Query rows from the CSV file.
        
        Args:
            columns: List of columns to select
            where: Dictionary of conditions
            order_by: Column name to sort by
            limit: Maximum number of rows
        
        Returns:
            List of matching rows
        """
        rows = self.read()
        
        # Filter
        if where:
            filtered = []
            for row in rows:
                match = True
                for col, val in where.items():
                    row_val = row.get(col)
                    # Try numeric comparison
                    try:
                        if str(row_val) != str(val):
                            match = False
                            break
                    except:
                        if row_val != val:
                            match = False
                            break
                if match:
                    filtered.append(row)
            rows = filtered
        
        # Select columns
        if columns:
            rows = [{col: row.get(col) for col in columns} for row in rows]
        
        # Sort
        if order_by:
            reverse = order_by.startswith("-")
            order_by = order_by.lstrip("-")
            rows = sorted(rows, key=lambda x: x.get(order_by, ""), reverse=reverse)
        
        # Limit
        if limit is not None:
            rows = rows[:limit]
        
        return rows
    
    def update(self, data: Dict[str, Any], where: Dict[str, Any]) -> int:
        """
        Update rows matching conditions.
        
        Args:
            data: New values
            where: Conditions
        
        Returns:
            Number of rows updated
        """
        rows = self.read()
        updated = 0
        
        for row in rows:
            match = all(str(row.get(k)) == str(v) for k, v in where.items())
            if match:
                row.update(data)
                updated += 1
        
        if updated > 0:
            self.write(rows)
        
        return updated
    
    def delete(self, where: Dict[str, Any]) -> int:
        """
        Delete rows matching conditions.
        
        Args:
            where: Conditions
        
        Returns:
            Number of rows deleted
        """
        rows = self.read()
        original_count = len(rows)
        
        rows = [
            row for row in rows
            if not all(str(row.get(k)) == str(v) for k, v in where.items())
        ]
        
        deleted = original_count - len(rows)
        if deleted > 0:
            self.write(rows)
        
        return deleted
    
    def close(self) -> None:
        """Close the CSV file (no-op for CSV)."""
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


# ============================================================================
# JSON File Utilities
# ============================================================================

class JSONDatabase:
    """
    JSON file wrapper with query capabilities.
    
    Example:
        >>> json_db = JSONDatabase("data.json")
        >>> json_db.write([{"name": "Alice", "age": 30}])
        >>> results = json_db.query(where={"age": 30})
        >>> json_db.close()
    """
    
    def __init__(self, file_path: str, encoding: str = "utf-8", indent: int = 2):
        """
        Initialize JSON database.
        
        Args:
            file_path: Path to the JSON file
            encoding: File encoding (default: "utf-8")
            indent: JSON indentation (default: 2)
        """
        self.file_path = file_path
        self.encoding = encoding
        self.indent = indent
        self._lock = threading.Lock()
    
    def read(self) -> Union[Rows, Dict]:
        """
        Read data from the JSON file.
        
        Returns:
            Parsed JSON data (list or dict)
        """
        if not os.path.exists(self.file_path):
            return []
        
        with self._lock:
            with open(self.file_path, 'r', encoding=self.encoding) as f:
                return json.load(f)
    
    def write(self, data: Union[Rows, Dict]) -> bool:
        """
        Write data to the JSON file.
        
        Args:
            data: Data to write (list or dict)
        
        Returns:
            True if successful
        """
        with self._lock:
            with open(self.file_path, 'w', encoding=self.encoding) as f:
                json.dump(data, f, indent=self.indent, ensure_ascii=False)
        return True
    
    def query(self, where: Optional[Dict[str, Any]] = None,
              limit: Optional[int] = None) -> Rows:
        """
        Query data from the JSON file.
        
        Args:
            where: Dictionary of conditions
            limit: Maximum number of results
        
        Returns:
            List of matching items
        """
        data = self.read()
        
        if not isinstance(data, list):
            data = [data]
        
        if where:
            results = []
            for item in data:
                if isinstance(item, dict):
                    match = all(
                        str(item.get(k)) == str(v) 
                        for k, v in where.items()
                    )
                    if match:
                        results.append(item)
            data = results
        
        if limit is not None:
            data = data[:limit]
        
        return data
    
    def insert(self, data: Union[Row, Rows]) -> int:
        """
        Insert data into the JSON file.
        
        Args:
            data: Single item or list of items
        
        Returns:
            Number of items inserted
        """
        if isinstance(data, dict):
            data = [data]
        
        existing = self.read()
        if not isinstance(existing, list):
            existing = []
        
        existing.extend(data)
        self.write(existing)
        
        return len(data)
    
    def update(self, data: Dict[str, Any], where: Dict[str, Any]) -> int:
        """
        Update items matching conditions.
        
        Args:
            data: New values
            where: Conditions
        
        Returns:
            Number of items updated
        """
        items = self.read()
        if not isinstance(items, list):
            items = [items]
        
        updated = 0
        for item in items:
            if isinstance(item, dict):
                match = all(str(item.get(k)) == str(v) for k, v in where.items())
                if match:
                    item.update(data)
                    updated += 1
        
        if updated > 0:
            self.write(items)
        
        return updated
    
    def delete(self, where: Dict[str, Any]) -> int:
        """
        Delete items matching conditions.
        
        Args:
            where: Conditions
        
        Returns:
            Number of items deleted
        """
        items = self.read()
        if not isinstance(items, list):
            items = [items]
        
        original_count = len(items)
        items = [
            item for item in items
            if not (isinstance(item, dict) and 
                    all(str(item.get(k)) == str(v) for k, v in where.items()))
        ]
        
        deleted = original_count - len(items)
        if deleted > 0:
            self.write(items)
        
        return deleted
    
    def close(self) -> None:
        """Close the JSON file (no-op)."""
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


# ============================================================================
# Data Export/Import Utilities
# ============================================================================

def export_to_csv(data: Rows, file_path: str, 
                  fieldnames: Optional[List[str]] = None,
                  delimiter: str = ",", encoding: str = "utf-8") -> int:
    """
    Export data to a CSV file.
    
    Args:
        data: List of dictionaries
        file_path: Output file path
        fieldnames: Column names
        delimiter: Field delimiter
        encoding: File encoding
    
    Returns:
        Number of rows exported
    """
    csv_db = CSVDatabase(file_path, delimiter, encoding)
    return csv_db.write(data, fieldnames)


def import_from_csv(file_path: str, 
                    delimiter: str = ",", encoding: str = "utf-8") -> Rows:
    """
    Import data from a CSV file.
    
    Args:
        file_path: Input file path
        delimiter: Field delimiter
        encoding: File encoding
    
    Returns:
        List of dictionaries
    """
    csv_db = CSVDatabase(file_path, delimiter, encoding)
    return csv_db.read()


def export_to_json(data: Union[Rows, Dict], file_path: str,
                   indent: int = 2, encoding: str = "utf-8") -> bool:
    """
    Export data to a JSON file.
    
    Args:
        data: Data to export
        file_path: Output file path
        indent: JSON indentation
        encoding: File encoding
    
    Returns:
        True if successful
    """
    json_db = JSONDatabase(file_path, encoding, indent)
    return json_db.write(data)


def import_from_json(file_path: str, encoding: str = "utf-8") -> Union[Rows, Dict]:
    """
    Import data from a JSON file.
    
    Args:
        file_path: Input file path
        encoding: File encoding
    
    Returns:
        Parsed JSON data
    """
    json_db = JSONDatabase(file_path, encoding)
    return json_db.read()


def convert_csv_to_json(csv_path: str, json_path: str, indent: int = 2) -> bool:
    """
    Convert a CSV file to JSON format.
    
    Args:
        csv_path: Input CSV file path
        json_path: Output JSON file path
        indent: JSON indentation
    
    Returns:
        True if successful
    """
    data = import_from_csv(csv_path)
    return export_to_json(data, json_path, indent)


def convert_json_to_csv(json_path: str, csv_path: str) -> int:
    """
    Convert a JSON file to CSV format.
    
    Args:
        json_path: Input JSON file path
        csv_path: Output CSV file path
    
    Returns:
        Number of rows exported
    """
    data = import_from_json(json_path)
    if not isinstance(data, list):
        data = [data]
    return export_to_csv(data, csv_path)


# ============================================================================
# Convenience Functions
# ============================================================================

def sqlite_connect(db_path: str, pool_size: int = 5) -> SQLiteDatabase:
    """
    Create a SQLite database connection.
    
    Args:
        db_path: Path to the database file
        pool_size: Connection pool size
    
    Returns:
        SQLiteDatabase instance
    """
    return SQLiteDatabase(db_path, pool_size)


def csv_connect(file_path: str, delimiter: str = ",", 
                encoding: str = "utf-8") -> CSVDatabase:
    """
    Create a CSV database connection.
    
    Args:
        file_path: Path to the CSV file
        delimiter: Field delimiter
        encoding: File encoding
    
    Returns:
        CSVDatabase instance
    """
    return CSVDatabase(file_path, delimiter, encoding)


def json_connect(file_path: str, encoding: str = "utf-8",
                 indent: int = 2) -> JSONDatabase:
    """
    Create a JSON database connection.
    
    Args:
        file_path: Path to the JSON file
        encoding: File encoding
        indent: JSON indentation
    
    Returns:
        JSONDatabase instance
    """
    return JSONDatabase(file_path, encoding, indent)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Classes
    'SQLiteDatabase',
    'CSVDatabase',
    'JSONDatabase',
    
    # Export/Import functions
    'export_to_csv',
    'import_from_csv',
    'export_to_json',
    'import_from_json',
    'convert_csv_to_json',
    'convert_json_to_csv',
    
    # Convenience functions
    'sqlite_connect',
    'csv_connect',
    'json_connect',
    
    # Type aliases
    'Row',
    'Rows',
    'QueryResult',
]
