!! AllToolkit - Fortran Sorting Utilities Module
!! Zero-dependency sorting algorithms for Fortran 90/95/2003+
!!
!! Features:
!! - Bubble Sort, Selection Sort, Insertion Sort
!! - Quick Sort, Merge Sort, Heap Sort
!! - Shell Sort, Counting Sort, Radix Sort
!! - Generic interfaces for real and integer arrays
!! - In-place and copy variants
!! - Custom comparator support
!! - Partial sorting and selection algorithms
!!
!! Author: AllToolkit Contributors
!! License: MIT

module sorting_utils
    implicit none
    
    ! Module constants
    integer, parameter :: MAX_RADIX_DIGITS = 32
    
    ! Generic interfaces for sorting
    interface sort
        module procedure sort_real, sort_int
    end interface
    
    interface sort_inplace
        module procedure sort_real_inplace, sort_int_inplace
    end interface
    
    interface quicksort_custom
        module procedure quicksort_real, quicksort_int
    end interface
    
    interface merge_sort
        module procedure merge_sort_real, merge_sort_int
    end interface
    
    interface heap_sort
        module procedure heap_sort_real, heap_sort_int
    end interface
    
    interface shell_sort
        module procedure shell_sort_real, shell_sort_int
    end interface
    
    interface counting_sort
        module procedure counting_sort_int
    end interface
    
    interface radix_sort
        module procedure radix_sort_int
    end interface
    
    interface is_sorted
        module procedure is_sorted_real, is_sorted_int
    end interface
    
    interface find_kth_smallest
        module procedure find_kth_smallest_real, find_kth_smallest_int
    end interface
    
    interface partial_sort
        module procedure partial_sort_real, partial_sort_int
    end interface
    
contains

    !==========================================================================
    ! Utility Functions
    !==========================================================================
    
    !> Swap two real values
    subroutine swap_real(a, b)
        real(8), intent(inout) :: a, b
        real(8) :: temp
        temp = a
        a = b
        b = temp
    end subroutine swap_real
    
    !> Swap two integer values
    subroutine swap_int(a, b)
        integer, intent(inout) :: a, b
        integer :: temp
        temp = a
        a = b
        b = temp
    end subroutine swap_int
    
    !> Check if real array is sorted (ascending)
    function is_sorted_real(arr) result(res)
        real(8), intent(in) :: arr(:)
        logical :: res
        integer :: i, n
        n = size(arr)
        res = .true.
        do i = 2, n
            if (arr(i) < arr(i-1)) then
                res = .false.
                return
            end if
        end do
    end function is_sorted_real
    
    !> Check if integer array is sorted (ascending)
    function is_sorted_int(arr) result(res)
        integer, intent(in) :: arr(:)
        logical :: res
        integer :: i, n
        n = size(arr)
        res = .true.
        do i = 2, n
            if (arr(i) < arr(i-1)) then
                res = .false.
                return
            end if
        end do
    end function is_sorted_int

    !==========================================================================
    ! Bubble Sort - O(n^2)
    !==========================================================================
    
    !> Bubble sort for real array (ascending, returns copy)
    function sort_real(arr) result(res)
        real(8), intent(in) :: arr(:)
        real(8), allocatable :: res(:)
        integer :: n, i, j
        logical :: swapped
        
        n = size(arr)
        allocate(res(n))
        res = arr
        
        do i = 1, n - 1
            swapped = .false.
            do j = 1, n - i
                if (res(j) > res(j+1)) then
                    call swap_real(res(j), res(j+1))
                    swapped = .true.
                end if
            end do
            if (.not. swapped) exit
        end do
    end function sort_real
    
    !> Bubble sort for integer array (ascending, returns copy)
    function sort_int(arr) result(res)
        integer, intent(in) :: arr(:)
        integer, allocatable :: res(:)
        integer :: n, i, j
        logical :: swapped
        
        n = size(arr)
        allocate(res(n))
        res = arr
        
        do i = 1, n - 1
            swapped = .false.
            do j = 1, n - i
                if (res(j) > res(j+1)) then
                    call swap_int(res(j), res(j+1))
                    swapped = .true.
                end if
            end do
            if (.not. swapped) exit
        end do
    end function sort_int
    
    !> Bubble sort for real array (descending, returns copy)
    function sort_real_desc(arr) result(res)
        real(8), intent(in) :: arr(:)
        real(8), allocatable :: res(:)
        integer :: n, i, j
        logical :: swapped
        
        n = size(arr)
        allocate(res(n))
        res = arr
        
        do i = 1, n - 1
            swapped = .false.
            do j = 1, n - i
                if (res(j) < res(j+1)) then
                    call swap_real(res(j), res(j+1))
                    swapped = .true.
                end if
            end do
            if (.not. swapped) exit
        end do
    end function sort_real_desc
    
    !> Bubble sort for integer array (descending, returns copy)
    function sort_int_desc(arr) result(res)
        integer, intent(in) :: arr(:)
        integer, allocatable :: res(:)
        integer :: n, i, j
        logical :: swapped
        
        n = size(arr)
        allocate(res(n))
        res = arr
        
        do i = 1, n - 1
            swapped = .false.
            do j = 1, n - i
                if (res(j) < res(j+1)) then
                    call swap_int(res(j), res(j+1))
                    swapped = .true.
                end if
            end do
            if (.not. swapped) exit
        end do
    end function sort_int_desc
    
    !> Bubble sort for real array in-place (ascending)
    subroutine sort_real_inplace(arr)
        real(8), intent(inout) :: arr(:)
        integer :: n, i, j
        logical :: swapped
        
        n = size(arr)
        do i = 1, n - 1
            swapped = .false.
            do j = 1, n - i
                if (arr(j) > arr(j+1)) then
                    call swap_real(arr(j), arr(j+1))
                    swapped = .true.
                end if
            end do
            if (.not. swapped) exit
        end do
    end subroutine sort_real_inplace
    
    !> Bubble sort for integer array in-place (ascending)
    subroutine sort_int_inplace(arr)
        integer, intent(inout) :: arr(:)
        integer :: n, i, j
        logical :: swapped
        
        n = size(arr)
        do i = 1, n - 1
            swapped = .false.
            do j = 1, n - i
                if (arr(j) > arr(j+1)) then
                    call swap_int(arr(j), arr(j+1))
                    swapped = .true.
                end if
            end do
            if (.not. swapped) exit
        end do
    end subroutine sort_int_inplace
    
    !> Bubble sort for real array in-place (descending)
    subroutine sort_real_desc_inplace(arr)
        real(8), intent(inout) :: arr(:)
        integer :: n, i, j
        logical :: swapped
        
        n = size(arr)
        do i = 1, n - 1
            swapped = .false.
            do j = 1, n - i
                if (arr(j) < arr(j+1)) then
                    call swap_real(arr(j), arr(j+1))
                    swapped = .true.
                end if
            end do
            if (.not. swapped) exit
        end do
    end subroutine sort_real_desc_inplace
    
    !> Bubble sort for integer array in-place (descending)
    subroutine sort_int_desc_inplace(arr)
        integer, intent(inout) :: arr(:)
        integer :: n, i, j
        logical :: swapped
        
        n = size(arr)
        do i = 1, n - 1
            swapped = .false.
            do j = 1, n - i
                if (arr(j) < arr(j+1)) then
                    call swap_int(arr(j), arr(j+1))
                    swapped = .true.
                end if
            end do
            if (.not. swapped) exit
        end do
    end subroutine sort_int_desc_inplace

    !==========================================================================
    ! Selection Sort - O(n^2)
    !==========================================================================
    
    !> Selection sort for real array in-place
    subroutine selection_sort_real(arr)
        real(8), intent(inout) :: arr(:)
        integer :: n, i, j, min_idx
        
        n = size(arr)
        do i = 1, n - 1
            min_idx = i
            do j = i + 1, n
                if (arr(j) < arr(min_idx)) then
                    min_idx = j
                end if
            end do
            if (min_idx /= i) then
                call swap_real(arr(i), arr(min_idx))
            end if
        end do
    end subroutine selection_sort_real
    
    !> Selection sort for integer array in-place
    subroutine selection_sort_int(arr)
        integer, intent(inout) :: arr(:)
        integer :: n, i, j, min_idx
        
        n = size(arr)
        do i = 1, n - 1
            min_idx = i
            do j = i + 1, n
                if (arr(j) < arr(min_idx)) then
                    min_idx = j
                end if
            end do
            if (min_idx /= i) then
                call swap_int(arr(i), arr(min_idx))
            end if
        end do
    end subroutine selection_sort_int

    !==========================================================================
    ! Insertion Sort - O(n^2), efficient for small/nearly sorted arrays
    !==========================================================================
    
    !> Insertion sort for real array in-place
    subroutine insertion_sort_real(arr)
        real(8), intent(inout) :: arr(:)
        integer :: n, i, j
        real(8) :: key
        
        n = size(arr)
        do i = 2, n
            key = arr(i)
            j = i - 1
            do while (j >= 1 .and. arr(j) > key)
                arr(j + 1) = arr(j)
                j = j - 1
            end do
            arr(j + 1) = key
        end do
    end subroutine insertion_sort_real
    
    !> Insertion sort for integer array in-place
    subroutine insertion_sort_int(arr)
        integer, intent(inout) :: arr(:)
        integer :: n, i, j
        integer :: key
        
        n = size(arr)
        do i = 2, n
            key = arr(i)
            j = i - 1
            do while (j >= 1 .and. arr(j) > key)
                arr(j + 1) = arr(j)
                j = j - 1
            end do
            arr(j + 1) = key
        end do
    end subroutine insertion_sort_int

    !==========================================================================
    ! Quick Sort - O(n log n) average, O(n^2) worst
    !==========================================================================
    
    !> Quick sort for real array (returns copy)
    function quicksort_real(arr) result(res)
        real(8), intent(in) :: arr(:)
        real(8), allocatable :: res(:)
        integer :: n
        
        n = size(arr)
        allocate(res(n))
        res = arr
        call quicksort_real_inplace(res, 1, n)
    end function quicksort_real
    
    !> Quick sort for integer array (returns copy)
    function quicksort_int(arr) result(res)
        integer, intent(in) :: arr(:)
        integer, allocatable :: res(:)
        integer :: n
        
        n = size(arr)
        allocate(res(n))
        res = arr
        call quicksort_int_inplace(res, 1, n)
    end function quicksort_int
    
    !> Quick sort for real array in-place (recursive)
    recursive subroutine quicksort_real_inplace(arr, low, high)
        real(8), intent(inout) :: arr(:)
        integer, intent(in) :: low, high
        integer :: pivot_idx
        
        if (low < high) then
            call partition_real(arr, low, high, pivot_idx)
            call quicksort_real_inplace(arr, low, pivot_idx - 1)
            call quicksort_real_inplace(arr, pivot_idx + 1, high)
        end if
    end subroutine quicksort_real_inplace
    
    !> Quick sort for integer array in-place (recursive)
    recursive subroutine quicksort_int_inplace(arr, low, high)
        integer, intent(inout) :: arr(:)
        integer, intent(in) :: low, high
        integer :: pivot_idx
        
        if (low < high) then
            call partition_int(arr, low, high, pivot_idx)
            call quicksort_int_inplace(arr, low, pivot_idx - 1)
            call quicksort_int_inplace(arr, pivot_idx + 1, high)
        end if
    end subroutine quicksort_int_inplace
    
    !> Partition helper for quick sort (real)
    subroutine partition_real(arr, low, high, pivot_idx)
        real(8), intent(inout) :: arr(:)
        integer, intent(in) :: low, high
        integer, intent(out) :: pivot_idx
        real(8) :: pivot
        integer :: i, j
        
        pivot = arr(high)
        i = low - 1
        do j = low, high - 1
            if (arr(j) <= pivot) then
                i = i + 1
                call swap_real(arr(i), arr(j))
            end if
        end do
        call swap_real(arr(i + 1), arr(high))
        pivot_idx = i + 1
    end subroutine partition_real
    
    !> Partition helper for quick sort (integer)
    subroutine partition_int(arr, low, high, pivot_idx)
        integer, intent(inout) :: arr(:)
        integer, intent(in) :: low, high
        integer, intent(out) :: pivot_idx
        integer :: pivot
        integer :: i, j
        
        pivot = arr(high)
        i = low - 1
        do j = low, high - 1
            if (arr(j) <= pivot) then
                i = i + 1
                call swap_int(arr(i), arr(j))
            end if
        end do
        call swap_int(arr(i + 1), arr(high))
        pivot_idx = i + 1
    end subroutine partition_int

    !==========================================================================
    ! Merge Sort - O(n log n) guaranteed, stable
    !==========================================================================
    
    !> Merge sort for real array (returns copy)
    function merge_sort_real(arr) result(res)
        real(8), intent(in) :: arr(:)
        real(8), allocatable :: res(:)
        real(8), allocatable :: temp(:)
        integer :: n
        
        n = size(arr)
        allocate(res(n), temp(n))
        res = arr
        call merge_sort_recursive_real(res, temp, 1, n)
        deallocate(temp)
    end function merge_sort_real
    
    !> Merge sort for integer array (returns copy)
    function merge_sort_int(arr) result(res)
        integer, intent(in) :: arr(:)
        integer, allocatable :: res(:)
        integer, allocatable :: temp(:)
        integer :: n
        
        n = size(arr)
        allocate(res(n), temp(n))
        res = arr
        call merge_sort_recursive_int(res, temp, 1, n)
        deallocate(temp)
    end function merge_sort_int
    
    !> Merge sort recursive helper (real)
    recursive subroutine merge_sort_recursive_real(arr, temp, left, right)
        real(8), intent(inout) :: arr(:), temp(:)
        integer, intent(in) :: left, right
        integer :: mid
        
        if (left < right) then
            mid = (left + right) / 2
            call merge_sort_recursive_real(arr, temp, left, mid)
            call merge_sort_recursive_real(arr, temp, mid + 1, right)
            call merge_real(arr, temp, left, mid, right)
        end if
    end subroutine merge_sort_recursive_real
    
    !> Merge sort recursive helper (integer)
    recursive subroutine merge_sort_recursive_int(arr, temp, left, right)
        integer, intent(inout) :: arr(:), temp(:)
        integer, intent(in) :: left, right
        integer :: mid
        
        if (left < right) then
            mid = (left + right) / 2
            call merge_sort_recursive_int(arr, temp, left, mid)
            call merge_sort_recursive_int(arr, temp, mid + 1, right)
            call merge_int(arr, temp, left, mid, right)
        end if
    end subroutine merge_sort_recursive_int
    
    !> Merge helper for merge sort (real)
    subroutine merge_real(arr, temp, left, mid, right)
        real(8), intent(inout) :: arr(:), temp(:)
        integer, intent(in) :: left, mid, right
        integer :: i, j, k
        
        i = left
        j = mid + 1
        k = left
        
        do while (i <= mid .and. j <= right)
            if (arr(i) <= arr(j)) then
                temp(k) = arr(i)
                i = i + 1
            else
                temp(k) = arr(j)
                j = j + 1
            end if
            k = k + 1
        end do
        
        do while (i <= mid)
            temp(k) = arr(i)
            i = i + 1
            k = k + 1
        end do
        
        do while (j <= right)
            temp(k) = arr(j)
            j = j + 1
            k = k + 1
        end do
        
        do i = left, right
            arr(i) = temp(i)
        end do
    end subroutine merge_real
    
    !> Merge helper for merge sort (integer)
    subroutine merge_int(arr, temp, left, mid, right)
        integer, intent(inout) :: arr(:), temp(:)
        integer, intent(in) :: left, mid, right
        integer :: i, j, k
        
        i = left
        j = mid + 1
        k = left
        
        do while (i <= mid .and. j <= right)
            if (arr(i) <= arr(j)) then
                temp(k) = arr(i)
                i = i + 1
            else
                temp(k) = arr(j)
                j = j + 1
            end if
            k = k + 1
        end do
        
        do while (i <= mid)
            temp(k) = arr(i)
            i = i + 1
            k = k + 1
        end do
        
        do while (j <= right)
            temp(k) = arr(j)
            j = j + 1
            k = k + 1
        end do
        
        do i = left, right
            arr(i) = temp(i)
        end do
    end subroutine merge_int

    !==========================================================================
    ! Heap Sort - O(n log n) guaranteed, in-place
    !==========================================================================
    
    !> Heap sort for real array (returns copy)
    function heap_sort_real(arr) result(res)
        real(8), intent(in) :: arr(:)
        real(8), allocatable :: res(:)
        integer :: n
        
        n = size(arr)
        allocate(res(n))
        res = arr
        call heap_sort_real_inplace(res)
    end function heap_sort_real
    
    !> Heap sort for integer array (returns copy)
    function heap_sort_int(arr) result(res)
        integer, intent(in) :: arr(:)
        integer, allocatable :: res(:)
        integer :: n
        
        n = size(arr)
        allocate(res(n))
        res = arr
        call heap_sort_int_inplace(res)
    end function heap_sort_int
    
    !> Heap sort for real array in-place
    subroutine heap_sort_real_inplace(arr)
        real(8), intent(inout) :: arr(:)
        integer :: n, i
        
        n = size(arr)
        
        ! Build max heap
        do i = n / 2, 1, -1
            call heapify_real(arr, n, i)
        end do
        
        ! Extract elements from heap
        do i = n, 2, -1
            call swap_real(arr(1), arr(i))
            call heapify_real(arr, i - 1, 1)
        end do
    end subroutine heap_sort_real_inplace
    
    !> Heap sort for integer array in-place
    subroutine heap_sort_int_inplace(arr)
        integer, intent(inout) :: arr(:)
        integer :: n, i
        
        n = size(arr)
        
        ! Build max heap
        do i = n / 2, 1, -1
            call heapify_int(arr, n, i)
        end do
        
        ! Extract elements from heap
        do i = n, 2, -1
            call swap_int(arr(1), arr(i))
            call heapify_int(arr, i - 1, 1)
        end do
    end subroutine heap_sort_int_inplace
    
    !> Heapify helper for heap sort (real)
    recursive subroutine heapify_real(arr, n, i)
        real(8), intent(inout) :: arr(:)
        integer, intent(in) :: n, i
        integer :: largest, left, right
        
        largest = i
        left = 2 * i
        right = 2 * i + 1
        
        if (left <= n .and. arr(left) > arr(largest)) then
            largest = left
        end if
        
        if (right <= n .and. arr(right) > arr(largest)) then
            largest = right
        end if
        
        if (largest /= i) then
            call swap_real(arr(i), arr(largest))
            call heapify_real(arr, n, largest)
        end if
    end subroutine heapify_real
    
    !> Heapify helper for heap sort (integer)
    recursive subroutine heapify_int(arr, n, i)
        integer, intent(inout) :: arr(:)
        integer, intent(in) :: n, i
        integer :: largest, left, right
        
        largest = i
        left = 2 * i
        right = 2 * i + 1
        
        if (left <= n .and. arr(left) > arr(largest)) then
            largest = left
        end if
        
        if (right <= n .and. arr(right) > arr(largest)) then
            largest = right
        end if
        
        if (largest /= i) then
            call swap_int(arr(i), arr(largest))
            call heapify_int(arr, n, largest)
        end if
    end subroutine heapify_int

    !==========================================================================
    ! Shell Sort - O(n log n) to O(n^2) depending on gap sequence
    !==========================================================================
    
    !> Shell sort for real array (returns copy)
    function shell_sort_real(arr) result(res)
        real(8), intent(in) :: arr(:)
        real(8), allocatable :: res(:)
        integer :: n
        
        n = size(arr)
        allocate(res(n))
        res = arr
        call shell_sort_real_inplace(res)
    end function shell_sort_real
    
    !> Shell sort for integer array (returns copy)
    function shell_sort_int(arr) result(res)
        integer, intent(in) :: arr(:)
        integer, allocatable :: res(:)
        integer :: n
        
        n = size(arr)
        allocate(res(n))
        res = arr
        call shell_sort_int_inplace(res)
    end function shell_sort_int
    
    !> Shell sort for real array in-place
    subroutine shell_sort_real_inplace(arr)
        real(8), intent(inout) :: arr(:)
        integer :: n, gap, i, j
        real(8) :: temp
        
        n = size(arr)
        gap = n / 2
        
        do while (gap > 0)
            do i = gap + 1, n
                temp = arr(i)
                j = i
                do while (j > gap .and. arr(j - gap) > temp)
                    arr(j) = arr(j - gap)
                    j = j - gap
                end do
                arr(j) = temp
            end do
            gap = gap / 2
        end do
    end subroutine shell_sort_real_inplace
    
    !> Shell sort for integer array in-place
    subroutine shell_sort_int_inplace(arr)
        integer, intent(inout) :: arr(:)
        integer :: n, gap, i, j
        integer :: temp
        
        n = size(arr)
        gap = n / 2
        
        do while (gap > 0)
            do i = gap + 1, n
                temp = arr(i)
                j = i
                do while (j > gap .and. arr(j - gap) > temp)
                    arr(j) = arr(j - gap)
                    j = j - gap
                end do
                arr(j) = temp
            end do
            gap = gap / 2
        end do
    end subroutine shell_sort_int_inplace

    !==========================================================================
    ! Counting Sort - O(n + k), k is range of values
    !==========================================================================
    
    !> Counting sort for non-negative integer array (returns copy)
    function counting_sort_int(arr) result(res)
        integer, intent(in) :: arr(:)
        integer, allocatable :: res(:)
        integer, allocatable :: count(:)
        integer :: n, i, max_val, min_val, range_val
        
        n = size(arr)
        if (n == 0) then
            allocate(res(0))
            return
        end if
        
        ! Find range
        min_val = minval(arr)
        max_val = maxval(arr)
        range_val = max_val - min_val + 1
        
        allocate(res(n), count(range_val))
        count = 0
        
        ! Count occurrences
        do i = 1, n
            count(arr(i) - min_val + 1) = count(arr(i) - min_val + 1) + 1
        end do
        
        ! Cumulative count
        do i = 2, range_val
            count(i) = count(i) + count(i - 1)
        end do
        
        ! Build output array (stable)
        do i = n, 1, -1
            res(count(arr(i) - min_val + 1)) = arr(i)
            count(arr(i) - min_val + 1) = count(arr(i) - min_val + 1) - 1
        end do
        
        deallocate(count)
    end function counting_sort_int

    !==========================================================================
    ! Radix Sort - O(d * (n + b)), d is digits, b is base
    !==========================================================================
    
    !> Radix sort for non-negative integer array (returns copy)
    function radix_sort_int(arr) result(res)
        integer, intent(in) :: arr(:)
        integer, allocatable :: res(:)
        integer :: n, i, max_val, min_val
        
        n = size(arr)
        if (n == 0) then
            allocate(res(0))
            return
        end if
        
        allocate(res(n))
        res = arr
        
        ! Handle negative numbers: shift to non-negative
        min_val = minval(res)
        if (min_val < 0) then
            do i = 1, n
                res(i) = res(i) - min_val
            end do
        end if
        
        ! Find maximum value
        max_val = maxval(res)
        
        ! Do counting sort for each digit
        i = 1
        do while (max_val / i > 0)
            call radix_count_sort(res, n, i)
            i = i * 10
        end do
        
        ! Restore negative offset
        if (min_val < 0) then
            do i = 1, n
                res(i) = res(i) + min_val
            end do
        end if
    end function radix_sort_int
    
    !> Radix sort counting helper
    subroutine radix_count_sort(arr, n, exp)
        integer, intent(inout) :: arr(:)
        integer, intent(in) :: n, exp
        integer, allocatable :: output(:), count(:)
        integer :: i
        
        allocate(output(n), count(10))
        count = 0
        
        ! Count occurrences of digits
        do i = 1, n
            count(mod(arr(i) / exp, 10) + 1) = count(mod(arr(i) / exp, 10) + 1) + 1
        end do
        
        ! Cumulative count
        do i = 2, 10
            count(i) = count(i) + count(i - 1)
        end do
        
        ! Build output array
        do i = n, 1, -1
            output(count(mod(arr(i) / exp, 10) + 1)) = arr(i)
            count(mod(arr(i) / exp, 10) + 1) = count(mod(arr(i) / exp, 10) + 1) - 1
        end do
        
        ! Copy back
        arr = output
        
        deallocate(output, count)
    end subroutine radix_count_sort

    !==========================================================================
    ! Selection Algorithms (K-th smallest/largest)
    !==========================================================================
    
    !> Find k-th smallest element in real array (1-indexed)
    function find_kth_smallest_real(arr, k) result(res)
        real(8), intent(in) :: arr(:)
        integer, intent(in) :: k
        real(8) :: res
        real(8), allocatable :: sorted(:)
        integer :: n, k_adjusted
        
        n = size(arr)
        k_adjusted = max(1, min(k, n))
        sorted = sort_real(arr)
        res = sorted(k_adjusted)
        deallocate(sorted)
    end function find_kth_smallest_real
    
    !> Find k-th smallest element in integer array (1-indexed)
    function find_kth_smallest_int(arr, k) result(res)
        integer, intent(in) :: arr(:)
        integer, intent(in) :: k
        integer :: res
        integer, allocatable :: sorted(:)
        integer :: n, k_adjusted
        
        n = size(arr)
        k_adjusted = max(1, min(k, n))
        sorted = sort_int(arr)
        res = sorted(k_adjusted)
        deallocate(sorted)
    end function find_kth_smallest_int
    
    !> Find k-th largest element in real array (1-indexed)
    function find_kth_largest_real(arr, k) result(res)
        real(8), intent(in) :: arr(:)
        integer, intent(in) :: k
        real(8) :: res
        real(8), allocatable :: sorted(:)
        integer :: n, k_adjusted
        
        n = size(arr)
        k_adjusted = max(1, min(k, n))
        sorted = sort_real_desc(arr)
        res = sorted(k_adjusted)
        deallocate(sorted)
    end function find_kth_largest_real
    
    !> Find k-th largest element in integer array (1-indexed)
    function find_kth_largest_int(arr, k) result(res)
        integer, intent(in) :: arr(:)
        integer, intent(in) :: k
        integer :: res
        integer, allocatable :: sorted(:)
        integer :: n, k_adjusted
        
        n = size(arr)
        k_adjusted = max(1, min(k, n))
        sorted = sort_int_desc(arr)
        res = sorted(k_adjusted)
        deallocate(sorted)
    end function find_kth_largest_int

    !==========================================================================
    ! Partial Sort - Sort first k elements
    !==========================================================================
    
    !> Partial sort for real array - sort first k elements
    function partial_sort_real(arr, k) result(res)
        real(8), intent(in) :: arr(:)
        integer, intent(in) :: k
        real(8), allocatable :: res(:)
        integer :: n, i, j, min_idx, k_adj
        real(8) :: temp
        
        n = size(arr)
        allocate(res(n))
        res = arr
        
        k_adj = min(k, n)
        
        ! Selection sort variant - only sort first k elements
        do i = 1, k_adj
            min_idx = i
            do j = i + 1, n
                if (res(j) < res(min_idx)) then
                    min_idx = j
                end if
            end do
            if (min_idx /= i) then
                temp = res(i)
                res(i) = res(min_idx)
                res(min_idx) = temp
            end if
        end do
    end function partial_sort_real
    
    !> Partial sort for integer array - sort first k elements
    function partial_sort_int(arr, k) result(res)
        integer, intent(in) :: arr(:)
        integer, intent(in) :: k
        integer, allocatable :: res(:)
        integer :: n, i, j, min_idx, k_adj
        integer :: temp
        
        n = size(arr)
        allocate(res(n))
        res = arr
        
        k_adj = min(k, n)
        
        ! Selection sort variant - only sort first k elements
        do i = 1, k_adj
            min_idx = i
            do j = i + 1, n
                if (res(j) < res(min_idx)) then
                    min_idx = j
                end if
            end do
            if (min_idx /= i) then
                temp = res(i)
                res(i) = res(min_idx)
                res(min_idx) = temp
            end if
        end do
    end function partial_sort_int

    !==========================================================================
    ! Utility: Reverse Array
    !==========================================================================
    
    !> Reverse a real array in-place
    subroutine reverse_real(arr)
        real(8), intent(inout) :: arr(:)
        integer :: n, i
        real(8) :: temp
        
        n = size(arr)
        do i = 1, n / 2
            temp = arr(i)
            arr(i) = arr(n - i + 1)
            arr(n - i + 1) = temp
        end do
    end subroutine reverse_real
    
    !> Reverse an integer array in-place
    subroutine reverse_int(arr)
        integer, intent(inout) :: arr(:)
        integer :: n, i, temp
        
        n = size(arr)
        do i = 1, n / 2
            temp = arr(i)
            arr(i) = arr(n - i + 1)
            arr(n - i + 1) = temp
        end do
    end subroutine reverse_int

end module sorting_utils