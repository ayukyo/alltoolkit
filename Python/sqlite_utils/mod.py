"""
AllToolkit - Python SQLite Utilities

A zero-dependency, production-ready SQLite database utility module.
Supports connection management, query building, CRUD operations, transactions,
schema management, and data export/import. Built entirely with Python standard library.

Author: AllToolkit
License: MIT
"""

import sqlite3
import os
import json
import csv
import threading
from typing import Optional, Dict, List, Tuple, Any, Union, Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


# =============================================================================
# Configuration
# =============================================================================

class SQLiteConfig:
    """Configuration for SQLite operations."""
    
    default_timeout: float = 30.0
    default_isolation_level: Optional[str] = "DEFERRED"
    max_connections: int = 10
    enable_foreign_keys: bool = True
    enable_wal_mode: bool = True
    
    def __init__(
        self,
        timeout: float = 30.0,
        isolation_level: Optional[str] = "DEFERRED",
        enable_foreign_keys: bool = True,
        enable_wal_mode: bool = True
    ):
        self.timeout = timeout
        self.isolation_level = isolation_level
        self.enable_foreign_keys = enable_foreign_keys
        self.enable_wal_mode = enable_wal_mode


# =============================================================================
# Exceptions
# =============================================================================

class SQLiteError(Exception):
    """Base exception for SQLite errors."""
    pass


class SQLiteConnectionError(SQLiteError):
    """Raised when connection fails."""
    pass


class SQLiteQueryError(SQLiteError):
    """Raised when query execution fails."""
    pass


class SQLiteValidationError(SQLiteError):
    """Raised when validation fails."""
    pass


class SQLiteTransactionError(SQLiteError):
    """Raised when transaction fails."""
    pass


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class Column:
    """Represents a database column definition."""
    name: str
    type: str
    nullable: bool = True
    primary_key: bool = False
    unique: bool = False
    default: Optional[Any] = None
    references: Optional[str] = None  # "table(column)" for foreign keys
    check: Optional[str] = None  # Check constraint
    
    def to_sql(self) -> str:
        """Convert column to SQL definition."""
        parts = [f'"{self.name}"', self.type.upper()]
        
        if self.primary_key:
            parts.append("PRIMARY KEY")
            if self.type.upper() == "INTEGER":
                parts.append("AUTOINCREMENT")
        
        if not self.nullable and not self.primary_key:
            parts.append("NOT NULL")
        
        if self.unique and not self.primary_key:
            parts.append("UNIQUE")
        
        if self.default is not None:
            if isinstance(self.default, str):
                parts.append(f"DEFAULT '{self.default}'")
            else:
                parts.append(f"DEFAULT {self.default}")
        
        if self.references:
            parts.append(f"REFERENCES {self.references}")
        
        if self.check:
            parts.append(f"CHECK ({self.check})")
        
        return " ".join(parts)


@dataclass
class Table:
    """Represents a database table definition."""
    name: str
    columns: List[Column]
    indexes: List[str] = field(default_factory=list)
    unique_constraints: List[List[str]] = field(default_factory=list)
    
    def to_sql(self) -> str:
        """Convert table to CREATE TABLE SQL."""
        col_defs = [col.to_sql() for col in self.columns]
        
        # Add unique constraints
        for cols in self.unique_constraints:
            col_names = ", ".join(f'"{c}"' for c in cols)
            col_defs.append(f"UNIQUE ({col_names})")
        
        cols_sql = ",\n    ".join(col_defs)
        sql = f'CREATE TABLE IF NOT EXISTS "{self.name}" (\n    {cols_sql}\n)'
        
        return sql
    
    def add_index_sql(self, index_name: str, columns: List[str], unique: bool = False) -> str:
        """Generate CREATE INDEX SQL."""
        unique_str = "UNIQUE " if unique else ""
        col_names = ", ".join(f'"{c}"' for c in columns)
        return f'CREATE {unique_str}INDEX IF NOT EXISTS "{index_name}" ON "{self.name}" ({col_names})'


@dataclass
class QueryResult:
    """Represents a query result with metadata."""
    rows: List[Tuple]
    columns: List[str]
    row_count: int
    execution_time: float
    
    def to_dicts(self) -> List[Dict[str, Any]]:
        """Convert rows to list of dictionaries."""
        return [dict(zip(self.columns, row)) for row in self.rows]
    
    def to_json(self, indent: int = 2) -> str:
        """Convert result to JSON string."""
        return json.dumps(self.to_dicts(), indent=indent, default=str)


# =============================================================================
# Query Builder
# =============================================================================

class QueryBuilder:
    """Fluent SQL query builder."""
    
    def __init__(self, table: str):
        self.table = table
        self._select_cols: List[str] = ["*"]
        self._where_clauses: List[str] = []
        self._where_params: List[Any] = []
        self._order_by: List[str] = []
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None
        self._group_by: List[str] = []
        self._having: List[str] = []
        self._having_params: List[Any] = []
        self._joins: List[str] = []
        self._join_params: List[Any] = []
    
    def select(self, *columns: str) -> 'QueryBuilder':
        """Set columns to select."""
        self._select_cols = list(columns) if columns else ["*"]
        return self
    
    def where(self, condition: str, *params: Any) -> 'QueryBuilder':
        """Add WHERE condition."""
        self._where_clauses.append(condition)
        self._where_params.extend(params)
        return self
    
    def where_eq(self, column: str, value: Any) -> 'QueryBuilder':
        """Add equality WHERE condition."""
        return self.where(f'"{column}" = ?', value)
    
    def where_in(self, column: str, values: List[Any]) -> 'QueryBuilder':
        """Add IN WHERE condition."""
        placeholders = ", ".join("?" for _ in values)
        return self.where(f'"{column}" IN ({placeholders})', *values)
    
    def where_between(self, column: str, start: Any, end: Any) -> 'QueryBuilder':
        """Add BETWEEN WHERE condition."""
        return self.where(f'"{column}" BETWEEN ? AND ?', start, end)
    
    def where_like(self, column: str, pattern: str) -> 'QueryBuilder':
        """Add LIKE WHERE condition."""
        return self.where(f'"{column}" LIKE ?', pattern)
    
    def order_by(self, column: str, desc: bool = False) -> 'QueryBuilder':
        """Add ORDER BY clause."""
        order = "DESC" if desc else "ASC"
        self._order_by.append(f'"{column}" {order}')
        return self
    
    def limit(self, limit: int) -> 'QueryBuilder':
        """Set LIMIT."""
        self._limit = limit
        return self
    
    def offset(self, offset: int) -> 'QueryBuilder':
        """Set OFFSET."""
        self._offset = offset
        return self
    
    def group_by(self, *columns: str) -> 'QueryBuilder':
        """Add GROUP BY clause."""
        self._group_by = list(columns)
        return self
    
    def having(self, condition: str, *params: Any) -> 'QueryBuilder':
        """Add HAVING condition."""
        self._having.append(condition)
        self._having_params.extend(params)
        return self
    
    def join(self, join_type: str, table: str, on: str, *params: Any) -> 'QueryBuilder':
        """Add JOIN clause."""
        self._joins.append(f'{join_type} JOIN "{table}" ON {on}')
        self._join_params.extend(params)
        return self
    
    def inner_join(self, table: str, on: str, *params: Any) -> 'QueryBuilder':
        """Add INNER JOIN."""
        return self.join("INNER", table, on, *params)
    
    def left_join(self, table: str, on: str, *params: Any) -> 'QueryBuilder':
        """Add LEFT JOIN."""
        return self.join("LEFT", table, on, *params)
    
    def build_select(self) -> Tuple[str, List[Any]]:
        """Build SELECT query."""
        cols = ", ".join(self._select_cols)
        sql = f'SELECT {cols} FROM "{self.table}"'
        params = list(self._join_params)
        
        if self._joins:
            sql += " " + " ".join(self._joins)
        
        if self._where_clauses:
            sql += " WHERE " + " AND ".join(self._where_clauses)
            params.extend(self._where_params)
        
        if self._group_by:
            sql += " GROUP BY " + ", ".join(self._group_by)
        
        if self._having:
            sql += " HAVING " + " AND ".join(self._having)
            params.extend(self._having_params)
        
        if self._order_by:
            sql += " ORDER BY " + ", ".join(self._order_by)
        
        if self._limit is not None:
            sql += f" LIMIT {self._limit}"
        
        if self._offset is not None:
            sql += f" OFFSET {self._offset}"
        
        return sql, params
    
    def build_count(self) -> Tuple[str, List[Any]]:
        """Build COUNT query."""
        original_cols = self._select_cols
        self._select_cols = ["COUNT(*) as count"]
        sql, params = self.build_select()
        self._select_cols = original_cols
        return sql, params
    
    def build_delete(self) -> Tuple[str, List[Any]]:
        """Build DELETE query."""
        sql = f'DELETE FROM "{self.table}"'
        params = list(self._where_params)
        
        if self._where_clauses:
            sql += " WHERE " + " AND ".join(self._where_clauses)
        
        return sql, params
    
    def build_update(self, data: Dict[str, Any]) -> Tuple[str, List[Any]]:
        """Build UPDATE query."""
        set_parts = []
        params = list(data.values())
        
        for col in data.keys():
            set_parts.append(f'"{col}" = ?')
        
        sql = f'UPDATE "{self.table}" SET {", ".join(set_parts)}'
        
        if self._where_clauses:
            sql += " WHERE " + " AND ".join(self._where_clauses)
            params.extend(self._where_params)
        
        return sql, params


# =============================================================================
# Database Connection Pool
# =============================================================================

class ConnectionPool:
    """Thread-safe connection pool for SQLite."""
    
    def __init__(self, db_path: str, max_connections: int = 10, config: Optional[SQLiteConfig] = None):
        self.db_path = db_path
        self.max_connections = max_connections
        self.config = config or SQLiteConfig()
        self._pool: List[sqlite3.Connection] = []
        self._in_use: set = set()
        self._lock = threading.Lock()
        self._created_count = 0
    
    def _create_connection(self) -> sqlite3.Connection:
        """Create a new database connection."""
        conn = sqlite3.connect(
            self.db_path,
            timeout=self.config.timeout,
            isolation_level=self.config.isolation_level,
            check_same_thread=False
        )
        conn.row_factory = sqlite3.Row
        
        if self.config.enable_foreign_keys:
            conn.execute("PRAGMA foreign_keys = ON")
        
        if self.config.enable_wal_mode:
            conn.execute("PRAGMA journal_mode = WAL")
        
        return conn
    
    def acquire(self) -> sqlite3.Connection:
        """Acquire a connection from the pool."""
        with self._lock:
            # Try to get an available connection
            for conn in self._pool:
                if id(conn) not in self._in_use:
                    self._in_use.add(id(conn))
                    return conn
            
            # Create new connection if under limit
            if self._created_count < self.max_connections:
                conn = self._create_connection()
                self._pool.append(conn)
                self._in_use.add(id(conn))
                self._created_count += 1
                return conn
            
            # Pool exhausted, wait for available connection
            raise SQLiteConnectionError(
                f"Connection pool exhausted (max={self.max_connections})"
            )
    
    def release(self, conn: sqlite3.Connection) -> None:
        """Release a connection back to the pool."""
        with self._lock:
            self._in_use.discard(id(conn))
    
    def close_all(self) -> None:
        """Close all connections in the pool."""
        with self._lock:
            for conn in self._pool:
                conn.close()
            self._pool.clear()
            self._in_use.clear()
            self._created_count = 0
    
    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        """Context manager for connection acquisition."""
        conn = self.acquire()
        try:
            yield conn
        finally:
            self.release(conn)


# =============================================================================
# Main Database Class
# =============================================================================

class Database:
    """
    High-level SQLite database interface.
    
    Provides comprehensive database operations including schema management,
    CRUD operations, transactions, query building, and data export/import.
    """
    
    def __init__(self, db_path: str, config: Optional[SQLiteConfig] = None):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
            config: Optional configuration
        """
        self.db_path = db_path
        self.config = config or SQLiteConfig()
        self._conn: Optional[sqlite3.Connection] = None
        self._pool: Optional[ConnectionPool] = None
        self._use_pool = False
    
    def connect(self, use_pool: bool = False, max_connections: int = 10) -> 'Database':
        """
        Establish database connection.
        
        Args:
            use_pool: Enable connection pooling
            max_connections: Maximum pool size
        
        Returns:
            Self for method chaining
        """
        if use_pool:
            self._pool = ConnectionPool(self.db_path, max_connections, self.config)
            self._use_pool = True
        else:
            self._conn = self._create_connection()
        return self
    
    def _create_connection(self) -> sqlite3.Connection:
        """Create a new database connection."""
        conn = sqlite3.connect(
            self.db_path,
            timeout=self.config.timeout,
            isolation_level=self.config.isolation_level
        )
        conn.row_factory = sqlite3.Row
        
        if self.config.enable_foreign_keys:
            conn.execute("PRAGMA foreign_keys = ON")
        
        if self.config.enable_wal_mode:
            conn.execute("PRAGMA journal_mode = WAL")
        
        return conn
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get current connection or from pool."""
        if self._use_pool and self._pool:
            return self._pool.acquire()
        elif self._conn:
            return self._conn
        else:
            return self._create_connection()
    
    def _release_connection(self, conn: sqlite3.Connection) -> None:
        """Release connection back to pool if using pooling."""
        if self._use_pool and self._pool:
            self._pool.release(conn)
    
    def close(self) -> None:
        """Close database connection."""
        if self._use_pool and self._pool:
            self._pool.close_all()
            self._pool = None
            self._use_pool = False
        elif self._conn:
            self._conn.close()
            self._conn = None
    
    def __enter__(self) -> 'Database':
        """Context manager entry."""
        if not self._conn and not self._use_pool:
            self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()
    
    # -------------------------------------------------------------------------
    # Schema Management
    # -------------------------------------------------------------------------
    
    def create_table(self, table: Table) -> None:
        """
        Create a table from Table definition.
        
        Args:
            table: Table definition object
        """
        conn = self._get_connection()
        try:
            conn.execute(table.to_sql())
            
            # Create indexes
            for i, index_cols in enumerate(table.unique_constraints):
                index_name = f"idx_{table.name}_{'_'.join(index_cols)}"
                sql = table.add_index_sql(index_name, index_cols, unique=True)
                conn.execute(sql)
            
            conn.commit()
        finally:
            self._release_connection(conn)
    
    def create_table_raw(self, sql: str) -> None:
        """
        Create a table from raw SQL.
        
        Args:
            sql: CREATE TABLE SQL statement
        """
        conn = self._get_connection()
        try:
            conn.execute(sql)
            conn.commit()
        finally:
            self._release_connection(conn)
    
    def drop_table(self, table_name: str, if_exists: bool = True) -> None:
        """
        Drop a table.
        
        Args:
            table_name: Name of table to drop
            if_exists: Add IF EXISTS clause
        """
        exists_clause = "IF EXISTS " if if_exists else ""
        sql = f'DROP TABLE {exists_clause}"{table_name}"'
        
        conn = self._get_connection()
        try:
            conn.execute(sql)
            conn.commit()
        finally:
            self._release_connection(conn)
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists.
        
        Args:
            table_name: Name of table to check
        
        Returns:
            True if table exists
        """
        sql = """
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """
        return self.query_scalar(sql, table_name) is not None
    
    def get_tables(self) -> List[str]:
        """
        Get list of all tables.
        
        Returns:
            List of table names
        """
        sql = """
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """
        result = self.query(sql)
        return [row[0] for row in result.rows]
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get column information for a table.
        
        Args:
            table_name: Name of table
        
        Returns:
            List of column info dictionaries
        """
        sql = f'PRAGMA table_info("{table_name}")'
        result = self.query(sql)
        return result.to_dicts()
    
    def add_column(self, table_name: str, column: Column) -> None:
        """
        Add a column to an existing table.
        
        Args:
            table_name: Name of table
            column: Column definition
        """
        sql = f'ALTER TABLE "{table_name}" ADD COLUMN {column.to_sql()}'
        
        conn = self._get_connection()
        try:
            conn.execute(sql)
            conn.commit()
        finally:
            self._release_connection(conn)
    
    def create_index(
        self, 
        table_name: str, 
        columns: List[str], 
        index_name: Optional[str] = None,
        unique: bool = False
    ) -> None:
        """
        Create an index on a table.
        
        Args:
            table_name: Name of table
            columns: Columns to index
            index_name: Optional index name (auto-generated if not provided)
            unique: Create unique index
        """
        if not index_name:
            index_name = f"idx_{table_name}_{'_'.join(columns)}"
        
        unique_str = "UNIQUE " if unique else ""
        col_names = ", ".join(f'"{c}"' for c in columns)
        sql = f'CREATE {unique_str}INDEX IF NOT EXISTS "{index_name}" ON "{table_name}" ({col_names})'
        
        conn = self._get_connection()
        try:
            conn.execute(sql)
            conn.commit()
        finally:
            self._release_connection(conn)
    
    # -------------------------------------------------------------------------
    # CRUD Operations
    # -------------------------------------------------------------------------
    
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """
        Insert a single row.
        
        Args:
            table: Table name
            data: Dictionary of column values
        
        Returns:
            ID of inserted row
        """
        columns = list(data.keys())
        placeholders = ", ".join("?" for _ in columns)
        col_names = ", ".join(f'"{c}"' for c in columns)
        
        sql = f'INSERT INTO "{table}" ({col_names}) VALUES ({placeholders})'
        params = [data[c] for c in columns]
        
        conn = self._get_connection()
        try:
            cursor = conn.execute(sql, params)
            conn.commit()
            return cursor.lastrowid
        finally:
            self._release_connection(conn)
    
    def insert_many(self, table: str, data_list: List[Dict[str, Any]]) -> List[int]:
        """
        Insert multiple rows.
        
        Args:
            table: Table name
            data_list: List of dictionaries
        
        Returns:
            List of inserted row IDs
        """
        if not data_list:
            return []
        
        columns = list(data_list[0].keys())
        placeholders = ", ".join("?" for _ in columns)
        col_names = ", ".join(f'"{c}"' for c in columns)
        
        sql = f'INSERT INTO "{table}" ({col_names}) VALUES ({placeholders})'
        
        conn = self._get_connection()
        try:
            ids = []
            for data in data_list:
                params = [data[c] for c in columns]
                cursor = conn.execute(sql, params)
                ids.append(cursor.lastrowid)
            conn.commit()
            return ids
        finally:
            self._release_connection(conn)
    
    def insert_or_replace(self, table: str, data: Dict[str, Any]) -> int:
        """
        Insert or replace a row (upsert).
        
        Args:
            table: Table name
            data: Dictionary of column values
        
        Returns:
            ID of inserted/replaced row
        """
        columns = list(data.keys())
        placeholders = ", ".join("?" for _ in columns)
        col_names = ", ".join(f'"{c}"' for c in columns)
        update_cols = ", ".join(f'"{c}" = excluded."{c}"' for c in columns if c != "id")
        
        sql = f'''
            INSERT INTO "{table}" ({col_names}) VALUES ({placeholders})
            ON CONFLICT(id) DO UPDATE SET {update_cols}
        '''
        params = [data[c] for c in columns]
        
        conn = self._get_connection()
        try:
            cursor = conn.execute(sql, params)
            conn.commit()
            return cursor.lastrowid
        finally:
            self._release_connection(conn)
    
    def select(
        self,
        table: str,
        columns: Optional[List[str]] = None,
        where: Optional[str] = None,
        params: Optional[Tuple] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> QueryResult:
        """
        Select rows from a table.
        
        Args:
            table: Table name
            columns: Columns to select (default: all)
            where: WHERE clause
            params: WHERE parameters
            order_by: ORDER BY clause
            limit: LIMIT clause
            offset: OFFSET clause
        
        Returns:
            QueryResult object
        """
        cols = ", ".join(columns) if columns else "*"
        sql = f'SELECT {cols} FROM "{table}"'
        sql_params = list(params) if params else []
        
        if where:
            sql += f" WHERE {where}"
        
        if order_by:
            sql += f" ORDER BY {order_by}"
        
        if limit:
            sql += f" LIMIT {limit}"
        
        if offset:
            sql += f" OFFSET {offset}"
        
        return self.query(sql, *sql_params)
    
    def find_one(
        self,
        table: str,
        where: str,
        params: Optional[Tuple] = None,
        columns: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Find a single row.
        
        Args:
            table: Table name
            where: WHERE clause
            params: WHERE parameters
            columns: Columns to select
        
        Returns:
            Dictionary or None if not found
        """
        result = self.select(table, columns, where, params, limit=1)
        if result.rows:
            return result.to_dicts()[0]
        return None
    
    def find_by_id(self, table: str, id_value: Any) -> Optional[Dict[str, Any]]:
        """
        Find a row by ID.
        
        Args:
            table: Table name
            id_value: ID value
        
        Returns:
            Dictionary or None if not found
        """
        return self.find_one(table, 'id = ?', (id_value,))
    
    def update(
        self,
        table: str,
        data: Dict[str, Any],
        where: str,
        params: Optional[Tuple] = None
    ) -> int:
        """
        Update rows.
        
        Args:
            table: Table name
            data: Dictionary of column values to update
            where: WHERE clause
            params: WHERE parameters
        
        Returns:
            Number of rows affected
        """
        set_parts = []
        update_params = list(data.values())
        
        for col in data.keys():
            set_parts.append(f'"{col}" = ?')
        
        sql = f'UPDATE "{table}" SET {", ".join(set_parts)} WHERE {where}'
        
        if params:
            update_params.extend(params)
        
        conn = self._get_connection()
        try:
            cursor = conn.execute(sql, update_params)
            conn.commit()
            return cursor.rowcount
        finally:
            self._release_connection(conn)
    
    def delete(
        self,
        table: str,
        where: str,
        params: Optional[Tuple] = None
    ) -> int:
        """
        Delete rows.
        
        Args:
            table: Table name
            where: WHERE clause
            params: WHERE parameters
        
        Returns:
            Number of rows deleted
        """
        sql = f'DELETE FROM "{table}" WHERE {where}'
        
        conn = self._get_connection()
        try:
            cursor = conn.execute(sql, params or ())
            conn.commit()
            return cursor.rowcount
        finally:
            self._release_connection(conn)
    
    def delete_by_id(self, table: str, id_value: Any) -> int:
        """
        Delete a row by ID.
        
        Args:
            table: Table name
            id_value: ID value
        
        Returns:
            Number of rows deleted (0 or 1)
        """
        return self.delete(table, 'id = ?', (id_value,))
    
    def count(self, table: str, where: Optional[str] = None, params: Optional[Tuple] = None) -> int:
        """
        Count rows in a table.
        
        Args:
            table: Table name
            where: Optional WHERE clause
            params: WHERE parameters
        
        Returns:
            Row count
        """
        sql = f'SELECT COUNT(*) FROM "{table}"'
        
        if where:
            sql += f" WHERE {where}"
        
        return self.query_scalar(sql, *(params or ())) or 0
    
    def exists(self, table: str, where: str, params: Optional[Tuple] = None) -> bool:
        """
        Check if any rows match the condition.
        
        Args:
            table: Table name
            where: WHERE clause
            params: WHERE parameters
        
        Returns:
            True if rows exist
        """
        sql = f'SELECT 1 FROM "{table}" WHERE {where} LIMIT 1'
        return self.query_scalar(sql, *(params or ())) is not None
    
    # -------------------------------------------------------------------------
    # Query Execution
    # -------------------------------------------------------------------------
    
    def query(self, sql: str, *params: Any) -> QueryResult:
        """
        Execute a SELECT query.
        
        Args:
            sql: SQL query
            params: Query parameters
        
        Returns:
            QueryResult object
        
        Note:
            优化版本：改进参数处理逻辑，
            增强边界检查和错误处理。
        """
        import time
        start_time = time.time()
        
        # 边界处理：空SQL
        if not sql or not isinstance(sql, str):
            return QueryResult(
                rows=[],
                columns=[],
                row_count=0,
                execution_time=0.0
            )
        
        conn = self._get_connection()
        try:
            # 改进参数处理逻辑：
            # 1. 单个tuple/list参数 -> 直接使用
            # 2. 多个参数 -> 组合成tuple
            # 3. 无参数 -> 空tuple
            if len(params) == 0:
                query_params = ()
            elif len(params) == 1:
                p = params[0]
                if isinstance(p, (tuple, list)):
                    query_params = tuple(p)  # 确保是tuple
                else:
                    query_params = (p,)
            else:
                query_params = tuple(params)
            
            cursor = conn.execute(sql, query_params)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            
            execution_time = time.time() - start_time
            
            return QueryResult(
                rows=rows,
                columns=columns,
                row_count=len(rows),
                execution_time=execution_time
            )
        finally:
            self._release_connection(conn)
    
    def query_scalar(self, sql: str, *params: Any) -> Optional[Any]:
        """
        Execute a query and return a single scalar value.
        
        Args:
            sql: SQL query
            params: Query parameters
        
        Returns:
            First column of first row, or None
        """
        conn = self._get_connection()
        try:
            cursor = conn.execute(sql, params)
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            self._release_connection(conn)
    
    def query_dict(self, sql: str, *params: Any) -> Optional[Dict[str, Any]]:
        """
        Execute a query and return a single row as dictionary.
        
        Args:
            sql: SQL query
            params: Query parameters
        
        Returns:
            Dictionary or None
        """
        result = self.query(sql, *params)
        if result.rows:
            return result.to_dicts()[0]
        return None
    
    def query_dicts(self, sql: str, *params: Any) -> List[Dict[str, Any]]:
        """
        Execute a query and return rows as list of dictionaries.
        
        Args:
            sql: SQL query
            params: Query parameters
        
        Returns:
            List of dictionaries
        """
        return self.query(sql, *params).to_dicts()
    
    def execute(self, sql: str, *params: Any) -> int:
        """
        Execute a non-SELECT query.
        
        Args:
            sql: SQL statement
            params: Statement parameters
        
        Returns:
            Number of rows affected
        """
        conn = self._get_connection()
        try:
            # Handle params correctly - if single tuple/list, use it directly
            if len(params) == 1 and isinstance(params[0], (tuple, list)):
                query_params = params[0]
            else:
                query_params = params
            
            cursor = conn.execute(sql, query_params)
            conn.commit()
            return cursor.rowcount
        finally:
            self._release_connection(conn)
    
    def executemany(self, sql: str, params_list: List[Tuple]) -> int:
        """
        Execute a statement with multiple parameter sets.
        
        Args:
            sql: SQL statement
            params_list: List of parameter tuples
        
        Returns:
            Total number of rows affected
        """
        conn = self._get_connection()
        try:
            cursor = conn.executemany(sql, params_list)
            conn.commit()
            return cursor.rowcount
        finally:
            self._release_connection(conn)
    
    # -------------------------------------------------------------------------
    # Query Builder
    # -------------------------------------------------------------------------
    
    def table(self, table_name: str) -> QueryBuilder:
        """
        Get a query builder for a table.
        
        Args:
            table_name: Table name
        
        Returns:
            QueryBuilder instance
        """
        return QueryBuilder(table_name)
    
    def query_builder(self, table_name: str) -> QueryBuilder:
        """
        Alias for table().
        
        Args:
            table_name: Table name
        
        Returns:
            QueryBuilder instance
        """
        return self.table(table_name)
    
    # -------------------------------------------------------------------------
    # Transactions
    # -------------------------------------------------------------------------
    
    @contextmanager
    def transaction(self):
        """
        Context manager for database transactions.
        
        Usage:
            with db.transaction():
                db.insert(...)
                db.update(...)
            # Automatically commits on success, rolls back on error
        
        Raises:
            SQLiteTransactionError: On transaction failure
        """
        conn = self._get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise SQLiteTransactionError(f"Transaction failed: {e}")
        finally:
            self._release_connection(conn)
    
    def begin(self) -> None:
        """Begin a manual transaction."""
        conn = self._get_connection()
        conn.execute("BEGIN")
    
    def commit(self) -> None:
        """Commit the current transaction."""
        conn = self._get_connection()
        conn.commit()
    
    def rollback(self) -> None:
        """Rollback the current transaction."""
        conn = self._get_connection()
        conn.rollback()
    
    # -------------------------------------------------------------------------
    # Data Export/Import
    # -------------------------------------------------------------------------
    
    def export_to_json(self, table: str, output_path: str, where: Optional[str] = None) -> int:
        """
        Export table data to JSON file.
        
        Args:
            table: Table name
            output_path: Output file path
            where: Optional WHERE clause
        
        Returns:
            Number of rows exported
        """
        sql = f'SELECT * FROM "{table}"'
        if where:
            sql += f" WHERE {where}"
        
        result = self.query(sql)
        data = result.to_dicts()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        
        return len(data)
    
    def export_to_csv(self, table: str, output_path: str, where: Optional[str] = None) -> int:
        """
        Export table data to CSV file.
        
        Args:
            table: Table name
            output_path: Output file path
            where: Optional WHERE clause
        
        Returns:
            Number of rows exported
        """
        sql = f'SELECT * FROM "{table}"'
        if where:
            sql += f" WHERE {where}"
        
        result = self.query(sql)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(result.columns)
            writer.writerows(result.rows)
        
        return result.row_count
    
    def import_from_json(self, table: str, input_path: str) -> int:
        """
        Import data from JSON file.
        
        Args:
            table: Table name
            input_path: Input file path
        
        Returns:
            Number of rows imported
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            data = [data]
        
        ids = self.insert_many(table, data)
        return len(ids)
    
    def import_from_csv(self, table: str, input_path: str, skip_header: bool = True) -> int:
        """
        Import data from CSV file.
        
        Args:
            table: Table name
            input_path: Input file path
            skip_header: Skip first row as header
        
        Returns:
            Number of rows imported
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            if skip_header:
                columns = next(reader)
            else:
                # Get columns from table
                info = self.get_table_info(table)
                columns = [col['name'] for col in info]
            
            rows = list(reader)
        
        data_list = []
        for row in rows:
            data = dict(zip(columns, row))
            data_list.append(data)
        
        ids = self.insert_many(table, data_list)
        return len(ids)
    
    # -------------------------------------------------------------------------
    # Backup & Restore
    # -------------------------------------------------------------------------
    
    def backup(self, backup_path: str) -> None:
        """
        Create a backup of the database.
        
        Args:
            backup_path: Path for backup file
        """
        import shutil
        
        # Ensure parent directory exists
        Path(backup_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Flush any pending writes
        conn = self._get_connection()
        try:
            conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        finally:
            self._release_connection(conn)
        
        # Use shutil.copy2 for reliable file copy
        shutil.copy2(self.db_path, backup_path)
    
    def restore(self, backup_path: str) -> None:
        """
        Restore database from backup.
        
        Args:
            backup_path: Path to backup file
        """
        if not os.path.exists(backup_path):
            raise SQLiteError(f"Backup file not found: {backup_path}")
        
        # Close current connection
        self.close()
        
        # Remove current database
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        
        # Copy backup to database location
        import shutil
        shutil.copy2(backup_path, self.db_path)
        
        # Reconnect
        self.connect()
    
    # -------------------------------------------------------------------------
    # Database Info
    # -------------------------------------------------------------------------
    
    def get_size(self) -> int:
        """
        Get database file size in bytes.
        
        Returns:
            File size in bytes
        """
        if os.path.exists(self.db_path):
            return os.path.getsize(self.db_path)
        return 0
    
    def get_size_formatted(self) -> str:
        """
        Get formatted database file size.
        
        Returns:
            Formatted size string (e.g., "1.5 MB")
        """
        size = self.get_size()
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    
    def get_version(self) -> str:
        """
        Get SQLite version.
        
        Returns:
            Version string
        """
        return self.query_scalar("SELECT sqlite_version()") or "unknown"
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary with database stats
        """
        return {
            "path": self.db_path,
            "size": self.get_size(),
            "size_formatted": self.get_size_formatted(),
            "version": self.get_version(),
            "tables": self.get_tables(),
            "table_count": len(self.get_tables())
        }
    
    def vacuum(self) -> None:
        """
        Reclaim unused space (VACUUM command).
        """
        self.execute("VACUUM")
    
    def analyze(self) -> None:
        """
        Update statistics for query optimizer (ANALYZE command).
        """
        self.execute("ANALYZE")


# =============================================================================
# Convenience Functions
# =============================================================================

def connect(db_path: str, **kwargs) -> Database:
    """
    Connect to a SQLite database.
    
    Args:
        db_path: Path to database file
        **kwargs: Additional arguments for Database
    
    Returns:
        Database instance (connected)
    """
    db = Database(db_path, **kwargs)
    db.connect()
    return db


def open_database(db_path: str, **kwargs) -> Database:
    """
    Open a SQLite database (alias for connect).
    
    Args:
        db_path: Path to database file
        **kwargs: Additional arguments
    
    Returns:
        Database instance (connected)
    """
    return connect(db_path, **kwargs)


def create_in_memory(**kwargs) -> Database:
    """
    Create an in-memory database.
    
    Args:
        **kwargs: Additional arguments
    
    Returns:
        Database instance (connected)
    """
    db = Database(":memory:", **kwargs)
    db.connect()
    return db


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Configuration
    'SQLiteConfig',
    
    # Exceptions
    'SQLiteError',
    'SQLiteConnectionError',
    'SQLiteQueryError',
    'SQLiteValidationError',
    'SQLiteTransactionError',
    
    # Data Classes
    'Column',
    'Table',
    'QueryResult',
    
    # Query Builder
    'QueryBuilder',
    
    # Connection Pool
    'ConnectionPool',
    
    # Main Database Class
    'Database',
    
    # Convenience Functions
    'connect',
    'open_database',
    'create_in_memory',
]
