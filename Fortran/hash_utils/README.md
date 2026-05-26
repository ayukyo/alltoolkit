# Hash Table Utils (Fortran)

A zero-dependency hash table (dictionary/map) implementation in Fortran. Provides efficient key-value storage with automatic resizing and collision handling.

## Features

- **String-to-String Hash Table**: Store and retrieve string values by string keys
- **Automatic Resizing**: Table grows automatically when load factor exceeds 70%
- **Linear Probing**: Collision resolution using open addressing
- **FNV-1a Hash Function**: Fast, well-distributed hash function
- **DJB2 Hash Function**: Alternative hash function option
- **CRUD Operations**: Full Create, Read, Update, Delete support
- **Iteration**: Get all keys, values, or entries
- **Zero External Dependencies**: Pure Fortran implementation

## Usage

### Basic Operations

```fortran
use hash_utils
implicit none

type(hash_table) :: table
character(len=:), allocatable :: value
integer :: status

! Initialize
call table%init()

! Insert
call table%insert("name", "Alice")
call table%insert("age", "30")

! Get
status = table%get("name", value)
if (status == HASH_SUCCESS) then
    print *, "name: ", value  ! Output: name: Alice
end if

! Check existence
if (table%contains("age")) then
    print *, "Key 'age' exists"
end if

! Update
call table%insert("age", "31")

! Delete
call table%remove("name")

! Clean up
call table%destroy()
```

### Configuration Storage Example

```fortran
type(hash_table) :: config

call config%init()

call config%insert("server.host", "localhost")
call config%insert("server.port", "8080")
call config%insert("db.url", "postgresql://localhost/mydb")

! Retrieve config
call config%get("server.port", value)
print *, "Port: ", value  ! Output: Port: 8080
```

### Word Counter Example

```fortran
type(hash_table) :: word_counts

call word_counts%init()

! Count words
call word_counts%insert("hello", "1")
call word_counts%insert("world", "1")
call word_counts%insert("hello", "2")  ! Updates existing

! Get all keys
call word_counts%keys(keys_array)
do i = 1, size(keys_array)
    print *, keys_array(i)
end do
```

## API Reference

### Type: `hash_table`

#### Initialization & Cleanup

| Method | Description |
|--------|-------------|
| `init([capacity])` | Initialize table with optional initial capacity |
| `destroy()` | Free all memory and reset table |

#### CRUD Operations

| Method | Description | Returns |
|--------|-------------|---------|
| `insert(key, value)` | Insert or update key-value pair | `HASH_SUCCESS` or error code |
| `get(key, value)` | Retrieve value by key | `HASH_SUCCESS` or `HASH_KEY_NOT_FOUND` |
| `contains(key)` | Check if key exists | `.true.` or `.false.` |
| `remove(key)` | Delete key-value pair | `HASH_SUCCESS` or error code |

#### Query Operations

| Method | Description | Returns |
|--------|-------------|---------|
| `size()` | Number of entries | Integer |
| `is_empty()` | Check if empty | `.true.` or `.false.` |
| `load_factor()` | Current load percentage | Real (0-100) |
| `get_capacity()` | Current table capacity | Integer |

#### Iteration

| Method | Description |
|--------|-------------|
| `keys(keys_array)` | Get all keys as array |
| `values(values_array)` | Get all values as array |
| `get_all_entries(entries)` | Get "key => value" strings |
| `to_string()` | Get JSON-like representation |

#### Advanced

| Method | Description |
|--------|-------------|
| `clear()` | Remove all entries |
| `rehash(new_capacity)` | Resize and rehash table |
| `from_pairs(keys, values, n)` | Create from parallel arrays |

### Hash Functions

| Function | Description |
|----------|-------------|
| `fnv1a_hash(string)` | FNV-1a 32-bit hash |
| `djb2_hash(string)` | DJB2 32-bit hash |
| `combine_hash(h1, h2)` | Combine two hash values |

### Error Codes

| Constant | Value | Description |
|----------|-------|-------------|
| `HASH_SUCCESS` | 0 | Operation successful |
| `HASH_KEY_NOT_FOUND` | -1 | Key not found |
| `HASH_TABLE_FULL` | -2 | Table full (shouldn't happen with resize) |
| `HASH_INVALID_INPUT` | -3 | Invalid input (empty key, etc.) |

## Compilation

### Using gfortran

```bash
# Compile module
gfortran -c mod.f90 -o hash_utils.o

# Compile and run tests
gfortran test_hash_utils.f90 hash_utils.o -o test_hash_utils
./test_hash_utils

# Compile and run examples
gfortran example_hash_utils.f90 hash_utils.o -o example_hash_utils
./example_hash_utils
```

### Using ifort (Intel Fortran)

```bash
# Compile module
ifort -c mod.f90 -o hash_utils.o

# Compile and run tests
ifort test_hash_utils.f90 hash_utils.o -o test_hash_utils
./test_hash_utils
```

## Implementation Details

### Hash Function

Uses **FNV-1a** (Fowler-Noll-Vo) hash function:
- Fast computation
- Good distribution
- Avalanche effect (small input changes → large output changes)

### Collision Resolution

Uses **Linear Probing**:
- Simple and cache-friendly
- Good performance for moderate load factors
- Automatic table resizing prevents clustering

### Memory Management

- Automatic allocation on `init()`
- Automatic deallocation on `destroy()`
- Resizes when load factor > 70%
- Capacity always a power of 2 for efficient modulo

## Files

| File | Description |
|------|-------------|
| `mod.f90` | Main module implementation |
| `test_hash_utils.f90` | Unit tests |
| `example_hash_utils.f90` | Usage examples |
| `README.md` | This documentation |

## License

MIT License - Part of AllToolkit

## Author

AllToolkit - 2026-05-26