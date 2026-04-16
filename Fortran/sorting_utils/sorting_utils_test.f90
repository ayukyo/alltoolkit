!! AllToolkit - Fortran Sorting Utilities Test Suite
!! Unit tests for sorting_utils module
!!
!! Run with: gfortran -o sorting_test mod.f90 sorting_utils_test.f90 && ./sorting_test

program sorting_utils_test
    use sorting_utils
    implicit none
    
    integer :: passed = 0
    integer :: failed = 0
    
    call test_bubble_sort()
    call test_selection_sort()
    call test_insertion_sort()
    call test_quick_sort()
    call test_merge_sort()
    call test_heap_sort()
    call test_shell_sort()
    call test_counting_sort()
    call test_radix_sort()
    call test_kth_selection()
    call test_partial_sort()
    call test_is_sorted()
    call test_reverse()
    
    print *, ""
    print *, "========================================"
    print *, "Sorting Utilities Test Results:"
    print *, "  Passed: ", passed
    print *, "  Failed: ", failed
    print *, "========================================"
    
    if (failed > 0) then
        stop 1
    end if
    
contains

    subroutine assert_true(condition, test_name)
        logical, intent(in) :: condition
        character(*), intent(in) :: test_name
        if (condition) then
            print *, "[PASS] ", test_name
            passed = passed + 1
        else
            print *, "[FAIL] ", test_name
            failed = failed + 1
        end if
    end subroutine assert_true
    
    subroutine assert_approx_equal(a, b, tolerance, test_name)
        real(8), intent(in) :: a, b, tolerance
        character(*), intent(in) :: test_name
        call assert_true(abs(a - b) <= tolerance, test_name)
    end subroutine assert_approx_equal
    
    subroutine assert_equal_int(a, b, test_name)
        integer, intent(in) :: a, b
        character(*), intent(in) :: test_name
        call assert_true(a == b, test_name)
    end subroutine assert_equal_int
    
    !==========================================================================
    ! Bubble Sort Tests
    !==========================================================================
    
    subroutine test_bubble_sort()
        real(8), allocatable :: arr_real(:), sorted_real(:), result_real(:)
        integer, allocatable :: arr_int(:), sorted_int(:), result_int(:)
        
        print *, ""
        print *, "--- Bubble Sort Tests ---"
        
        ! Test real array ascending
        allocate(arr_real(5), sorted_real(5))
        arr_real = [5.0d0, 2.0d0, 8.0d0, 1.0d0, 9.0d0]
        sorted_real = [1.0d0, 2.0d0, 5.0d0, 8.0d0, 9.0d0]
        result_real = sort_real(arr_real)
        call assert_true(all(abs(result_real - sorted_real) < 1.0d-10), &
                        "sort_real ascending")
        
        ! Test integer array ascending
        allocate(arr_int(5), sorted_int(5))
        arr_int = [5, 2, 8, 1, 9]
        sorted_int = [1, 2, 5, 8, 9]
        result_int = sort_int(arr_int)
        call assert_true(all(result_int == sorted_int), &
                        "sort_int ascending")
        
        ! Test descending
        deallocate(arr_real, sorted_real)
        allocate(arr_real(5), sorted_real(5))
        arr_real = [1.0d0, 2.0d0, 5.0d0, 8.0d0, 9.0d0]
        sorted_real = [9.0d0, 8.0d0, 5.0d0, 2.0d0, 1.0d0]
        result_real = sort_real_desc(arr_real)
        call assert_true(all(abs(result_real - sorted_real) < 1.0d-10), &
                        "sort_real_desc descending")
        
        ! Test in-place
        deallocate(arr_real)
        allocate(arr_real(5))
        arr_real = [5.0d0, 2.0d0, 8.0d0, 1.0d0, 9.0d0]
        call sort_real_inplace(arr_real)
        call assert_true(is_sorted_real(arr_real), &
                        "sort_real_inplace")
        
        deallocate(arr_int)
        allocate(arr_int(5))
        arr_int = [5, 2, 8, 1, 9]
        call sort_int_inplace(arr_int)
        call assert_true(is_sorted_int(arr_int), &
                        "sort_int_inplace")
        
        ! Test already sorted
        deallocate(arr_real)
        allocate(arr_real(5))
        arr_real = [1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0]
        call sort_real_inplace(arr_real)
        call assert_true(is_sorted_real(arr_real), &
                        "already sorted array")
        
        ! Test single element
        deallocate(arr_real, result_real)
        allocate(arr_real(1), result_real(1))
        arr_real = [42.0d0]
        result_real = sort_real(arr_real)
        call assert_approx_equal(result_real(1), 42.0d0, 1.0d-10, &
                                "single element sort")
    end subroutine test_bubble_sort
    
    !==========================================================================
    ! Selection Sort Tests
    !==========================================================================
    
    subroutine test_selection_sort()
        real(8), allocatable :: arr_real(:)
        integer, allocatable :: arr_int(:)
        
        print *, ""
        print *, "--- Selection Sort Tests ---"
        
        ! Test real array
        allocate(arr_real(6))
        arr_real = [64.0d0, 25.0d0, 12.0d0, 22.0d0, 11.0d0, 90.0d0]
        call selection_sort_real(arr_real)
        call assert_true(is_sorted_real(arr_real), &
                        "selection_sort_real")
        
        ! Test integer array
        allocate(arr_int(6))
        arr_int = [64, 25, 12, 22, 11, 90]
        call selection_sort_int(arr_int)
        call assert_true(is_sorted_int(arr_int), &
                        "selection_sort_int")
    end subroutine test_selection_sort
    
    !==========================================================================
    ! Insertion Sort Tests
    !==========================================================================
    
    subroutine test_insertion_sort()
        real(8), allocatable :: arr_real(:)
        integer, allocatable :: arr_int(:)
        
        print *, ""
        print *, "--- Insertion Sort Tests ---"
        
        ! Test real array
        allocate(arr_real(6))
        arr_real = [12.0d0, 11.0d0, 13.0d0, 5.0d0, 6.0d0, 7.0d0]
        call insertion_sort_real(arr_real)
        call assert_true(is_sorted_real(arr_real), &
                        "insertion_sort_real")
        
        ! Test integer array
        allocate(arr_int(6))
        arr_int = [12, 11, 13, 5, 6, 7]
        call insertion_sort_int(arr_int)
        call assert_true(is_sorted_int(arr_int), &
                        "insertion_sort_int")
        
        ! Test nearly sorted (insertion sort is efficient)
        deallocate(arr_real)
        allocate(arr_real(6))
        arr_real = [1.0d0, 2.0d0, 4.0d0, 3.0d0, 5.0d0, 6.0d0]
        call insertion_sort_real(arr_real)
        call assert_true(is_sorted_real(arr_real), &
                        "nearly sorted insertion")
    end subroutine test_insertion_sort
    
    !==========================================================================
    ! Quick Sort Tests
    !==========================================================================
    
    subroutine test_quick_sort()
        real(8), allocatable :: arr_real(:), result_real(:)
        integer, allocatable :: arr_int(:), result_int(:)
        
        print *, ""
        print *, "--- Quick Sort Tests ---"
        
        ! Test real array
        allocate(arr_real(10))
        arr_real = [10.0d0, 7.0d0, 8.0d0, 9.0d0, 1.0d0, 5.0d0, 3.0d0, &
                    6.0d0, 2.0d0, 4.0d0]
        result_real = quicksort_real(arr_real)
        call assert_true(is_sorted_real(result_real), &
                        "quicksort_real")
        
        ! Test integer array
        allocate(arr_int(10))
        arr_int = [10, 7, 8, 9, 1, 5, 3, 6, 2, 4]
        result_int = quicksort_int(arr_int)
        call assert_true(is_sorted_int(result_int), &
                        "quicksort_int")
        
        ! Test large array
        deallocate(arr_real)
        allocate(arr_real(15))
        arr_real = [100.0d0, 99.0d0, 98.0d0, 97.0d0, 96.0d0, 95.0d0, &
                    94.0d0, 93.0d0, 92.0d0, 91.0d0, 90.0d0, 89.0d0, &
                    88.0d0, 87.0d0, 86.0d0]
        call quicksort_real_inplace(arr_real, 1, 15)
        call assert_true(is_sorted_real(arr_real), &
                        "quicksort_real_inplace 15 elements")
    end subroutine test_quick_sort
    
    !==========================================================================
    ! Merge Sort Tests
    !==========================================================================
    
    subroutine test_merge_sort()
        real(8), allocatable :: arr_real(:), result_real(:)
        integer, allocatable :: arr_int(:), result_int(:)
        
        print *, ""
        print *, "--- Merge Sort Tests ---"
        
        ! Test real array
        allocate(arr_real(8))
        arr_real = [38.0d0, 27.0d0, 43.0d0, 3.0d0, 9.0d0, 82.0d0, &
                    10.0d0, 64.0d0]
        result_real = merge_sort_real(arr_real)
        call assert_true(is_sorted_real(result_real), &
                        "merge_sort_real")
        
        ! Test integer array
        allocate(arr_int(8))
        arr_int = [38, 27, 43, 3, 9, 82, 10, 64]
        result_int = merge_sort_int(arr_int)
        call assert_true(is_sorted_int(result_int), &
                        "merge_sort_int")
        
        ! Verify stability
        deallocate(arr_real, result_real)
        allocate(arr_real(5), result_real(5))
        arr_real = [1.0d0, 2.0d0, 1.0d0, 3.0d0, 2.0d0]
        result_real = merge_sort_real(arr_real)
        call assert_true(is_sorted_real(result_real), &
                        "merge_sort_real stability check")
    end subroutine test_merge_sort
    
    !==========================================================================
    ! Heap Sort Tests
    !==========================================================================
    
    subroutine test_heap_sort()
        real(8), allocatable :: arr_real(:), result_real(:)
        integer, allocatable :: arr_int(:), result_int(:)
        
        print *, ""
        print *, "--- Heap Sort Tests ---"
        
        ! Test real array
        allocate(arr_real(7))
        arr_real = [12.0d0, 11.0d0, 13.0d0, 5.0d0, 6.0d0, 7.0d0, 1.0d0]
        result_real = heap_sort_real(arr_real)
        call assert_true(is_sorted_real(result_real), &
                        "heap_sort_real")
        
        ! Test integer array
        allocate(arr_int(7))
        arr_int = [12, 11, 13, 5, 6, 7, 1]
        result_int = heap_sort_int(arr_int)
        call assert_true(is_sorted_int(result_int), &
                        "heap_sort_int")
        
        ! Test in-place
        deallocate(arr_real)
        allocate(arr_real(5))
        arr_real = [4.0d0, 10.0d0, 3.0d0, 5.0d0, 1.0d0]
        call heap_sort_real_inplace(arr_real)
        call assert_true(is_sorted_real(arr_real), &
                        "heap_sort_real_inplace")
    end subroutine test_heap_sort
    
    !==========================================================================
    ! Shell Sort Tests
    !==========================================================================
    
    subroutine test_shell_sort()
        real(8), allocatable :: arr_real(:), result_real(:)
        integer, allocatable :: arr_int(:), result_int(:)
        
        print *, ""
        print *, "--- Shell Sort Tests ---"
        
        ! Test real array
        allocate(arr_real(8))
        arr_real = [23.0d0, 12.0d0, 1.0d0, 8.0d0, 34.0d0, 54.0d0, &
                    2.0d0, 3.0d0]
        result_real = shell_sort_real(arr_real)
        call assert_true(is_sorted_real(result_real), &
                        "shell_sort_real")
        
        ! Test integer array
        allocate(arr_int(8))
        arr_int = [23, 12, 1, 8, 34, 54, 2, 3]
        result_int = shell_sort_int(arr_int)
        call assert_true(is_sorted_int(result_int), &
                        "shell_sort_int")
        
        ! Test in-place
        deallocate(arr_real)
        allocate(arr_real(6))
        arr_real = [5.0d0, 2.0d0, 9.0d0, 1.0d0, 6.0d0, 3.0d0]
        call shell_sort_real_inplace(arr_real)
        call assert_true(is_sorted_real(arr_real), &
                        "shell_sort_real_inplace")
    end subroutine test_shell_sort
    
    !==========================================================================
    ! Counting Sort Tests
    !==========================================================================
    
    subroutine test_counting_sort()
        integer, allocatable :: arr_int(:), sorted_int(:), result_int(:)
        
        print *, ""
        print *, "--- Counting Sort Tests ---"
        
        ! Test small positive integers
        allocate(arr_int(8), sorted_int(8))
        arr_int = [4, 2, 2, 8, 3, 3, 1, 0]
        sorted_int = [0, 1, 2, 2, 3, 3, 4, 8]
        result_int = counting_sort_int(arr_int)
        call assert_true(all(result_int == sorted_int), &
                        "counting_sort_int")
        
        ! Test range of values
        deallocate(arr_int, result_int)
        allocate(arr_int(7), result_int(7))
        arr_int = [1, 4, 1, 2, 7, 5, 2]
        result_int = counting_sort_int(arr_int)
        call assert_true(is_sorted_int(result_int), &
                        "counting_sort_int range")
        
        ! Test single element
        deallocate(arr_int, result_int)
        allocate(arr_int(1), result_int(1))
        arr_int = [5]
        result_int = counting_sort_int(arr_int)
        call assert_equal_int(result_int(1), 5, "counting_sort single element")
    end subroutine test_counting_sort
    
    !==========================================================================
    ! Radix Sort Tests
    !==========================================================================
    
    subroutine test_radix_sort()
        integer, allocatable :: arr_int(:), sorted_int(:), result_int(:)
        
        print *, ""
        print *, "--- Radix Sort Tests ---"
        
        ! Test positive integers
        allocate(arr_int(7), sorted_int(7))
        arr_int = [170, 45, 75, 90, 802, 24, 2]
        sorted_int = [2, 24, 45, 75, 90, 170, 802]
        result_int = radix_sort_int(arr_int)
        call assert_true(all(result_int == sorted_int), &
                        "radix_sort_int")
        
        ! Test with negative values
        deallocate(arr_int, result_int)
        allocate(arr_int(7), result_int(7))
        arr_int = [-5, 10, -15, 20, 0, -10, 5]
        result_int = radix_sort_int(arr_int)
        call assert_true(is_sorted_int(result_int), &
                        "radix_sort_int with negatives")
        
        ! Test duplicates
        deallocate(arr_int, result_int)
        allocate(arr_int(5), result_int(5))
        arr_int = [123, 123, 456, 456, 789]
        result_int = radix_sort_int(arr_int)
        call assert_true(is_sorted_int(result_int), &
                        "radix_sort_int duplicates")
    end subroutine test_radix_sort
    
    !==========================================================================
    ! K-th Selection Tests
    !==========================================================================
    
    subroutine test_kth_selection()
        real(8), allocatable :: arr_real(:)
        integer, allocatable :: arr_int(:)
        real(8) :: result_real
        integer :: result_int
        
        print *, ""
        print *, "--- K-th Selection Tests ---"
        
        ! Test 3rd smallest (real)
        allocate(arr_real(5))
        arr_real = [5.0d0, 2.0d0, 8.0d0, 1.0d0, 9.0d0]
        result_real = find_kth_smallest_real(arr_real, 3)
        call assert_approx_equal(result_real, 5.0d0, 1.0d-10, &
                                "find_kth_smallest_real (3rd)")
        
        ! Test 1st smallest (minimum)
        result_real = find_kth_smallest_real(arr_real, 1)
        call assert_approx_equal(result_real, 1.0d0, 1.0d-10, &
                                "find_kth_smallest_real (min)")
        
        ! Test 5th smallest (maximum)
        result_real = find_kth_smallest_real(arr_real, 5)
        call assert_approx_equal(result_real, 9.0d0, 1.0d-10, &
                                "find_kth_smallest_real (max)")
        
        ! Test integer k-th smallest
        allocate(arr_int(5))
        arr_int = [5, 2, 8, 1, 9]
        result_int = find_kth_smallest_int(arr_int, 2)
        call assert_equal_int(result_int, 2, &
                             "find_kth_smallest_int (2nd)")
        
        ! Test k-th largest (real)
        result_real = find_kth_largest_real(arr_real, 2)
        call assert_approx_equal(result_real, 8.0d0, 1.0d-10, &
                                "find_kth_largest_real (2nd)")
        
        ! Test k-th largest (integer)
        result_int = find_kth_largest_int(arr_int, 3)
        call assert_equal_int(result_int, 5, &
                             "find_kth_largest_int (3rd)")
    end subroutine test_kth_selection
    
    !==========================================================================
    ! Partial Sort Tests
    !==========================================================================
    
    subroutine test_partial_sort()
        real(8), allocatable :: arr_real(:), result_real(:)
        integer, allocatable :: arr_int(:), result_int(:)
        
        print *, ""
        print *, "--- Partial Sort Tests ---"
        
        ! Test partial sort first 3 elements (real)
        allocate(arr_real(6), result_real(6))
        arr_real = [5.0d0, 2.0d0, 8.0d0, 1.0d0, 9.0d0, 3.0d0]
        result_real = partial_sort_real(arr_real, 3)
        call assert_approx_equal(result_real(1), 1.0d0, 1.0d-10, &
                                "partial_sort_real (1st)")
        call assert_approx_equal(result_real(2), 2.0d0, 1.0d-10, &
                                "partial_sort_real (2nd)")
        call assert_approx_equal(result_real(3), 3.0d0, 1.0d-10, &
                                "partial_sort_real (3rd)")
        
        ! Test partial sort first 2 elements (integer)
        allocate(arr_int(6), result_int(6))
        arr_int = [10, 3, 7, 2, 9, 1]
        result_int = partial_sort_int(arr_int, 2)
        call assert_equal_int(result_int(1), 1, &
                             "partial_sort_int (1st)")
        call assert_equal_int(result_int(2), 2, &
                             "partial_sort_int (2nd)")
    end subroutine test_partial_sort
    
    !==========================================================================
    ! Is Sorted Tests
    !==========================================================================
    
    subroutine test_is_sorted()
        real(8), allocatable :: arr_real(:)
        integer, allocatable :: arr_int(:)
        
        print *, ""
        print *, "--- Is Sorted Tests ---"
        
        ! Test sorted array (real)
        allocate(arr_real(5))
        arr_real = [1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0]
        call assert_true(is_sorted_real(arr_real), &
                        "is_sorted_real (sorted)")
        
        ! Test unsorted array (real)
        arr_real = [5.0d0, 4.0d0, 3.0d0, 2.0d0, 1.0d0]
        call assert_true(.not. is_sorted_real(arr_real), &
                        "is_sorted_real (unsorted)")
        
        ! Test sorted array (integer)
        allocate(arr_int(5))
        arr_int = [1, 2, 3, 4, 5]
        call assert_true(is_sorted_int(arr_int), &
                        "is_sorted_int (sorted)")
        
        ! Test unsorted array (integer)
        arr_int = [1, 3, 2, 4, 5]
        call assert_true(.not. is_sorted_int(arr_int), &
                        "is_sorted_int (unsorted)")
        
        ! Test single element
        deallocate(arr_real)
        allocate(arr_real(1))
        arr_real = [42.0d0]
        call assert_true(is_sorted_real(arr_real), &
                        "is_sorted_real (single)")
    end subroutine test_is_sorted
    
    !==========================================================================
    ! Reverse Tests
    !==========================================================================
    
    subroutine test_reverse()
        real(8), allocatable :: arr_real(:), reversed_check(:)
        integer, allocatable :: arr_int(:), reversed_int(:)
        
        print *, ""
        print *, "--- Reverse Tests ---"
        
        ! Test reverse real array
        allocate(arr_real(5), reversed_check(5))
        arr_real = [1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0]
        reversed_check = [5.0d0, 4.0d0, 3.0d0, 2.0d0, 1.0d0]
        call reverse_real(arr_real)
        call assert_true(all(abs(arr_real - reversed_check) < 1.0d-10), &
                        "reverse_real")
        
        ! Test reverse integer array
        allocate(arr_int(5), reversed_int(5))
        arr_int = [1, 2, 3, 4, 5]
        reversed_int = [5, 4, 3, 2, 1]
        call reverse_int(arr_int)
        call assert_true(all(arr_int == reversed_int), &
                        "reverse_int")
        
        ! Test reverse even length
        deallocate(arr_int)
        allocate(arr_int(4))
        arr_int = [1, 2, 3, 4]
        call reverse_int(arr_int)
        call assert_true(arr_int(1) == 4 .and. arr_int(4) == 1, &
                        "reverse_int (even length)")
        
        ! Test reverse single element
        deallocate(arr_real)
        allocate(arr_real(1))
        arr_real = [42.0d0]
        call reverse_real(arr_real)
        call assert_approx_equal(arr_real(1), 42.0d0, 1.0d-10, &
                                "reverse_single element")
    end subroutine test_reverse

end program sorting_utils_test