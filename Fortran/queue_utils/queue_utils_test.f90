! AllToolkit - Queue Utilities Test Suite
! Comprehensive tests for integer, string, and double precision queues

program queue_utils_test
    use queue_utils
    implicit none
    
    integer :: tests_passed, tests_failed
    
    tests_passed = 0
    tests_failed = 0
    
    print *, "========================================"
    print *, "  Queue Utilities Test Suite"
    print *, "========================================"
    print *, ""
    
    call test_int_queue_basic()
    call test_int_queue_operations()
    call test_str_queue_basic()
    call test_str_queue_operations()
    call test_double_queue_basic()
    call test_double_queue_operations()
    
    print *, ""
    print *, "========================================"
    print *, "  Test Summary"
    print *, "========================================"
    print *, "Tests Passed: ", tests_passed
    print *, "Tests Failed: ", tests_failed
    
    if (tests_failed == 0) then
        print *, ""
        print *, "All tests passed!"
    else
        print *, ""
        print *, "Some tests failed!"
    end if
    
contains

    subroutine test_int_queue_basic()
        type(int_queue_t) :: q
        integer :: val
        logical :: success
        
        print *, "Testing Integer Queue Basic..."
        
        call int_queue_init(q)
        call assert_true(int_queue_is_empty(q), "Queue empty after init")
        call assert_equals_int(int_queue_size(q), 0, "Size 0 after init")
        
        call int_queue_enqueue(q, 10)
        call assert_false(int_queue_is_empty(q), "Queue not empty after enqueue")
        call assert_equals_int(int_queue_size(q), 1, "Size 1")
        
        success = int_queue_dequeue(q, val)
        call assert_true(success, "Dequeue succeeds")
        call assert_equals_int(val, 10, "Dequeued 10")
        call assert_true(int_queue_is_empty(q), "Empty after dequeue")
        
        ! Test FIFO
        call int_queue_enqueue(q, 1)
        call int_queue_enqueue(q, 2)
        call int_queue_enqueue(q, 3)
        
        success = int_queue_dequeue(q, val)
        call assert_equals_int(val, 1, "First dequeue 1")
        success = int_queue_dequeue(q, val)
        call assert_equals_int(val, 2, "Second dequeue 2")
        success = int_queue_dequeue(q, val)
        call assert_equals_int(val, 3, "Third dequeue 3")
        
        call int_queue_destroy(q)
        print *, "Integer Queue Basic: OK"
    end subroutine test_int_queue_basic
    
    subroutine test_int_queue_operations()
        type(int_queue_t) :: q
        integer :: val
        logical :: success
        
        print *, "Testing Integer Queue Operations..."
        
        call int_queue_init(q, 4)
        
        call int_queue_enqueue(q, 42)
        call int_queue_enqueue(q, 99)
        
        ! Peek
        success = int_queue_peek(q, val)
        call assert_true(success, "Peek succeeds")
        call assert_equals_int(val, 42, "Peek value 42")
        call assert_equals_int(int_queue_size(q), 2, "Size unchanged after peek")
        
        ! Peek back
        success = int_queue_peek_back(q, val)
        call assert_equals_int(val, 99, "Peek back 99")
        
        ! Contains
        call assert_true(int_queue_contains(q, 42), "Contains 42")
        call assert_true(int_queue_contains(q, 99), "Contains 99")
        call assert_false(int_queue_contains(q, 50), "Not contains 50")
        
        ! Remove
        success = int_queue_remove(q, 99)
        call assert_true(success, "Remove succeeds")
        call assert_equals_int(int_queue_size(q), 1, "Size 1 after remove")
        call assert_false(int_queue_contains(q, 99), "Not contains 99")
        
        ! Reverse
        call int_queue_clear(q)
        call int_queue_enqueue(q, 1)
        call int_queue_enqueue(q, 2)
        call int_queue_enqueue(q, 3)
        call int_queue_reverse(q)
        
        success = int_queue_dequeue(q, val)
        call assert_equals_int(val, 3, "Reversed first 3")
        success = int_queue_dequeue(q, val)
        call assert_equals_int(val, 2, "Reversed second 2")
        success = int_queue_dequeue(q, val)
        call assert_equals_int(val, 1, "Reversed third 1")
        
        call int_queue_destroy(q)
        print *, "Integer Queue Operations: OK"
    end subroutine test_int_queue_operations
    
    subroutine test_str_queue_basic()
        type(str_queue_t) :: q
        character(len=256) :: val
        logical :: success
        
        print *, "Testing String Queue Basic..."
        
        call str_queue_init(q)
        call assert_true(str_queue_is_empty(q), "String queue empty after init")
        call assert_equals_int(str_queue_size(q), 0, "String queue size 0")
        
        call str_queue_enqueue(q, "Hello")
        call str_queue_enqueue(q, "World")
        call str_queue_enqueue(q, "Fortran")
        
        call assert_equals_int(str_queue_size(q), 3, "Size 3")
        
        success = str_queue_dequeue(q, val)
        call assert_true(success, "Dequeue succeeds")
        call assert_equals_str(val, "Hello", "First Hello")
        
        success = str_queue_dequeue(q, val)
        call assert_equals_str(val, "World", "Second World")
        
        success = str_queue_dequeue(q, val)
        call assert_equals_str(val, "Fortran", "Third Fortran")
        
        call str_queue_destroy(q)
        print *, "String Queue Basic: OK"
    end subroutine test_str_queue_basic
    
    subroutine test_str_queue_operations()
        type(str_queue_t) :: q
        character(len=256) :: val
        logical :: success
        
        print *, "Testing String Queue Operations..."
        
        call str_queue_init(q)
        
        call str_queue_enqueue(q, "First")
        call str_queue_enqueue(q, "Second")
        
        ! Peek
        success = str_queue_peek(q, val)
        call assert_equals_str(val, "First", "Peek First")
        
        success = str_queue_peek_back(q, val)
        call assert_equals_str(val, "Second", "Peek back Second")
        
        ! Contains
        call assert_true(str_queue_contains(q, "First"), "Contains First")
        call assert_true(str_queue_contains(q, "Second"), "Contains Second")
        call assert_false(str_queue_contains(q, "Third"), "Not contains Third")
        
        ! Remove
        success = str_queue_remove(q, "First")
        call assert_true(success, "Remove succeeds")
        call assert_equals_int(str_queue_size(q), 1, "Size 1 after remove")
        
        ! Reverse
        call str_queue_clear(q)
        call str_queue_enqueue(q, "A")
        call str_queue_enqueue(q, "B")
        call str_queue_enqueue(q, "C")
        call str_queue_reverse(q)
        
        success = str_queue_dequeue(q, val)
        call assert_equals_str(val, "C", "Reversed first C")
        success = str_queue_dequeue(q, val)
        call assert_equals_str(val, "B", "Reversed second B")
        success = str_queue_dequeue(q, val)
        call assert_equals_str(val, "A", "Reversed third A")
        
        call str_queue_destroy(q)
        print *, "String Queue Operations: OK"
    end subroutine test_str_queue_operations
    
    subroutine test_double_queue_basic()
        type(double_queue_t) :: q
        double precision :: val
        logical :: success
        
        print *, "Testing Double Queue Basic..."
        
        call double_queue_init(q)
        call assert_true(double_queue_is_empty(q), "Double queue empty after init")
        call assert_equals_int(double_queue_size(q), 0, "Double queue size 0")
        
        call double_queue_enqueue(q, 1.5d0)
        call double_queue_enqueue(q, 2.7d0)
        call double_queue_enqueue(q, 3.14159d0)
        
        call assert_equals_int(double_queue_size(q), 3, "Size 3")
        
        success = double_queue_dequeue(q, val)
        call assert_true(success, "Dequeue succeeds")
        call assert_equals_double(val, 1.5d0, "First 1.5")
        
        success = double_queue_dequeue(q, val)
        call assert_equals_double(val, 2.7d0, "Second 2.7")
        
        success = double_queue_dequeue(q, val)
        call assert_equals_double(val, 3.14159d0, "Third 3.14159")
        
        call double_queue_destroy(q)
        print *, "Double Queue Basic: OK"
    end subroutine test_double_queue_basic
    
    subroutine test_double_queue_operations()
        type(double_queue_t) :: q
        double precision :: val
        logical :: success
        
        print *, "Testing Double Queue Operations..."
        
        call double_queue_init(q)
        
        call double_queue_enqueue(q, 1.23d0)
        call double_queue_enqueue(q, 4.56d0)
        
        success = double_queue_peek(q, val)
        call assert_equals_double(val, 1.23d0, "Peek 1.23")
        
        success = double_queue_peek_back(q, val)
        call assert_equals_double(val, 4.56d0, "Peek back 4.56")
        
        call assert_true(double_queue_contains(q, 1.23d0), "Contains 1.23")
        call assert_true(double_queue_contains(q, 4.56d0), "Contains 4.56")
        
        success = double_queue_remove(q, 1.23d0)
        call assert_true(success, "Remove succeeds")
        call assert_equals_int(double_queue_size(q), 1, "Size 1 after remove")
        
        call double_queue_clear(q)
        call double_queue_enqueue(q, 1.0d0)
        call double_queue_enqueue(q, 2.0d0)
        call double_queue_enqueue(q, 3.0d0)
        call double_queue_reverse(q)
        
        success = double_queue_dequeue(q, val)
        call assert_equals_double(val, 3.0d0, "Reversed first 3.0")
        success = double_queue_dequeue(q, val)
        call assert_equals_double(val, 2.0d0, "Reversed second 2.0")
        success = double_queue_dequeue(q, val)
        call assert_equals_double(val, 1.0d0, "Reversed third 1.0")
        
        call double_queue_destroy(q)
        print *, "Double Queue Operations: OK"
    end subroutine test_double_queue_operations
    
    ! Assertion helpers
    subroutine assert_true(condition, message)
        logical, intent(in) :: condition
        character(len=*), intent(in) :: message
        
        if (condition) then
            tests_passed = tests_passed + 1
        else
            tests_failed = tests_failed + 1
            print *, "FAILED: ", message
        end if
    end subroutine assert_true
    
    subroutine assert_false(condition, message)
        logical, intent(in) :: condition
        character(len=*), intent(in) :: message
        
        if (.not. condition) then
            tests_passed = tests_passed + 1
        else
            tests_failed = tests_failed + 1
            print *, "FAILED: ", message
        end if
    end subroutine assert_false
    
    subroutine assert_equals_int(actual, expected, message)
        integer, intent(in) :: actual, expected
        character(len=*), intent(in) :: message
        
        if (actual == expected) then
            tests_passed = tests_passed + 1
        else
            tests_failed = tests_failed + 1
            print *, "FAILED: ", message
        end if
    end subroutine assert_equals_int
    
    subroutine assert_equals_str(actual, expected, message)
        character(len=*), intent(in) :: actual, expected
        character(len=*), intent(in) :: message
        
        if (trim(actual) == trim(expected)) then
            tests_passed = tests_passed + 1
        else
            tests_failed = tests_failed + 1
            print *, "FAILED: ", message
        end if
    end subroutine assert_equals_str
    
    subroutine assert_equals_double(actual, expected, message)
        double precision, intent(in) :: actual, expected
        character(len=*), intent(in) :: message
        
        if (abs(actual - expected) < 1.0d-10) then
            tests_passed = tests_passed + 1
        else
            tests_failed = tests_failed + 1
            print *, "FAILED: ", message
        end if
    end subroutine assert_equals_double

end program queue_utils_test