! test_hash_utils.f90 - Unit tests for hash_utils module
! Author: AllToolkit
! Date: 2026-05-26

program test_hash_utils
    use hash_utils
    implicit none
    
    integer :: test_count, pass_count
    
    test_count = 0
    pass_count = 0
    
    print *, "========================================"
    print *, "  Hash Table Utils - Unit Tests"
    print *, "========================================"
    print *, ""
    
    ! Run all tests
    call test_hash_functions()
    call test_basic_operations()
    call test_collision_handling()
    call test_resize()
    call test_delete_operations()
    call test_iteration()
    call test_edge_cases()
    call test_from_pairs()
    
    ! Print summary
    print *, ""
    print *, "========================================"
    print *, "  Test Summary"
    print *, "========================================"
    write(*, '(A, I0, A, I0, A)') "  Tests: ", pass_count, "/", test_count, " passed"
    
    if (pass_count == test_count) then
        print *, "  Status: ALL TESTS PASSED!"
    else
        print *, "  Status: SOME TESTS FAILED"
        stop 1
    end if

contains

    subroutine test_hash_functions()
        print *, "--- Testing Hash Functions ---"
        
        ! Test FNV-1a consistency
        call assert(fnv1a_hash("hello") == fnv1a_hash("hello"), &
                    "FNV-1a hash consistency")
        
        ! Test FNV-1a different values
        call assert(fnv1a_hash("hello") /= fnv1a_hash("world"), &
                    "FNV-1a hash different strings")
        
        ! Test DJB2 consistency
        call assert(djb2_hash("test") == djb2_hash("test"), &
                    "DJB2 hash consistency")
        
        ! Test DJB2 different values
        call assert(djb2_hash("test") /= djb2_hash("test2"), &
                    "DJB2 hash different strings")
        
        ! Test combine_hash
        call assert(combine_hash(123, 456) /= 0, &
                    "Combine hash returns non-zero")
        
        print *, ""
    end subroutine test_hash_functions

    subroutine test_basic_operations()
        type(hash_table) :: table
        character(len=:), allocatable :: value
        integer :: status
        
        print *, "--- Testing Basic Operations ---"
        
        ! Test initialization
        call table%init()
        call assert(table%size() == 0, "Empty table size is 0")
        call assert(table%is_empty(), "New table is empty")
        call assert(table%get_capacity() == 16, "Default capacity is 16")
        
        ! Test insert and get
        call table%insert("name", "Alice")
        call assert(table%size() == 1, "Size after insert is 1")
        call assert(.not. table%is_empty(), "Table not empty after insert")
        
        call table%get("name", value, status)
        call assert(status == HASH_SUCCESS, "Get returns success")
        call assert(value == "Alice", "Get returns correct value")
        
        ! Test contains
        call assert(table%contains("name"), "Contains finds key")
        call assert(.not. table%contains("unknown"), "Contains returns false for missing key")
        
        ! Test update
        call table%insert("name", "Bob")
        call assert(table%size() == 1, "Size unchanged after update")
        
        call table%get("name", value, status)
        call assert(value == "Bob", "Update changes value")
        
        ! Test multiple inserts
        call table%insert("age", "30")
        call table%insert("city", "Tokyo")
        call assert(table%size() == 3, "Size after multiple inserts")
        
        ! Test get for multiple keys
        call table%get("age", value, status)
        call assert(value == "30", "Get age value")
        
        call table%get("city", value, status)
        call assert(value == "Tokyo", "Get city value")
        
        ! Test get non-existent key
        call table%get("country", value, status)
        call assert(status == HASH_KEY_NOT_FOUND, "Get missing key returns not found")
        
        call table%destroy()
        print *, ""
    end subroutine test_basic_operations

    subroutine test_collision_handling()
        type(hash_table) :: table
        character(len=:), allocatable :: value
        integer :: i, status
        character(len=10) :: key
        character(len=20) :: val
        
        print *, "--- Testing Collision Handling ---"
        
        ! Small table to force collisions
        call table%init(4)
        
        ! Insert multiple items
        do i = 1, 10
            write(key, '(A,I0)') "key", i
            write(val, '(A,I0)') "value", i
            call table%insert(key, trim(val))
        end do
        
        call assert(table%size() == 10, "All inserts succeed with collisions")
        
        ! Verify all can be retrieved
        do i = 1, 10
            write(key, '(A,I0)') "key", i
            call assert(table%contains(key), "Contains finds key after collision")
        end do
        
        call table%destroy()
        print *, ""
    end subroutine test_collision_handling

    subroutine test_resize()
        type(hash_table) :: table
        integer :: i
        character(len=10) :: key
        real :: lf
        
        print *, "--- Testing Resize ---"
        
        call table%init(4)
        call assert(table%get_capacity() >= 4, "Initial capacity is at least 4")
        
        ! Insert many items to trigger resize
        do i = 1, 20
            write(key, '(A,I0)') "key", i
            call table%insert(key, "value")
        end do
        
        call assert(table%get_capacity() > 4, "Capacity increased after resize")
        call assert(table%size() == 20, "All items preserved after resize")
        
        ! Verify load factor
        lf = table%load_factor()
        call assert(lf >= 0.0 .and. lf <= 100.0, "Load factor in valid range")
        
        call table%destroy()
        print *, ""
    end subroutine test_resize

    subroutine test_delete_operations()
        type(hash_table) :: table
        character(len=:), allocatable :: value
        integer :: status
        
        print *, "--- Testing Delete Operations ---"
        
        call table%init()
        
        ! Insert and delete
        call table%insert("a", "1")
        call table%insert("b", "2")
        call table%insert("c", "3")
        
        call assert(table%size() == 3, "Size before delete")
        
        ! Delete middle
        call table%remove("b", status)
        call assert(status == HASH_SUCCESS, "Remove returns success")
        call assert(table%size() == 2, "Size after delete")
        call assert(.not. table%contains("b"), "Deleted key not found")
        
        ! Verify others still accessible
        call table%get("a", value, status)
        call assert(value == "1", "Other keys still accessible")
        
        call table%get("c", value, status)
        call assert(value == "3", "Other keys still accessible")
        
        ! Delete non-existent
        call table%remove("unknown", status)
        call assert(status == HASH_KEY_NOT_FOUND, "Remove missing key returns not found")
        
        ! Delete same key twice
        call table%remove("a", status)
        call assert(status == HASH_SUCCESS, "First delete succeeds")
        call table%remove("a", status)
        call assert(status == HASH_KEY_NOT_FOUND, "Second delete fails")
        
        call table%destroy()
        print *, ""
    end subroutine test_delete_operations

    subroutine test_iteration()
        type(hash_table) :: table
        character(len=:), allocatable :: keys(:)
        character(len=:), allocatable :: values(:)
        character(len=:), allocatable :: entries(:)
        character(len=:), allocatable :: str
        
        print *, "--- Testing Iteration ---"
        
        call table%init()
        call table%insert("x", "1")
        call table%insert("y", "2")
        call table%insert("z", "3")
        
        ! Test keys
        call table%keys(keys)
        call assert(size(keys) == 3, "Keys array has correct size")
        
        ! Test values
        call table%values(values)
        call assert(size(values) == 3, "Values array has correct size")
        
        ! Test entries
        call table%get_all_entries(entries)
        call assert(size(entries) == 3, "Entries array has correct size")
        
        ! Test to_string
        str = table%to_string()
        call assert(len(str) > 0, "to_string returns non-empty string")
        call assert(str(1:1) == "{", "to_string starts with {")
        
        call table%destroy()
        print *, ""
    end subroutine test_iteration

    subroutine test_edge_cases()
        type(hash_table) :: table
        character(len=:), allocatable :: value
        integer :: status
        
        print *, "--- Testing Edge Cases ---"
        
        ! Test with uninitialized table
        call assert(table%size() == 0, "Uninitialized table size is 0")
        call assert(table%is_empty(), "Uninitialized table is empty")
        
        ! Test empty key (insert should fail silently or just not add)
        call table%insert("", "value")
        call assert(table%size() == 0, "Empty key rejected")
        
        ! Test get with empty key
        call table%get("", value, status)
        call assert(status == HASH_INVALID_INPUT, "Get empty key rejected")
        
        ! Test remove with empty key
        call table%remove("", status)
        call assert(status == HASH_INVALID_INPUT, "Remove empty key rejected")
        
        ! Test clear
        call table%init()
        call table%insert("a", "1")
        call table%insert("b", "2")
        call table%clear()
        call assert(table%size() == 0, "Clear empties table")
        call assert(table%is_empty(), "Clear makes table empty")
        
        call table%destroy()
        print *, ""
    end subroutine test_edge_cases

    subroutine test_from_pairs()
        type(hash_table) :: table
        character(len=20) :: keys_arr(3)
        character(len=20) :: values_arr(3)
        character(len=:), allocatable :: val
        integer :: status
        
        print *, "--- Testing From Pairs ---"
        
        keys_arr = ["first ", "second", "third "]
        values_arr = ["value1", "value2", "value3"]
        
        call table%from_pairs(keys_arr, values_arr, 3)
        
        call assert(table%size() == 3, "From pairs creates correct size")
        call assert(table%contains("first"), "Contains first key")
        call assert(table%contains("second"), "Contains second key")
        call assert(table%contains("third"), "Contains third key")
        
        call table%get("first", val, status)
        call assert(val == "value1", "First value correct")
        
        call table%destroy()
        print *, ""
    end subroutine test_from_pairs

    subroutine assert(condition, description)
        logical, intent(in) :: condition
        character(len=*), intent(in) :: description
        
        test_count = test_count + 1
        
        if (condition) then
            write(*, '(A,A)') "  [PASS] ", description
            pass_count = pass_count + 1
        else
            write(*, '(A,A)') "  [FAIL] ", description
        end if
    end subroutine assert

end program test_hash_utils