!> @file mod.f90
!> @brief Array manipulation utilities for Fortran
!> @details Comprehensive array operations including sorting, searching,
!>          statistics, transformations, and utility functions
!> @author AllToolkit Contributors
!> @version 1.0.0
!> @license MIT

module array_utils
  implicit none
  
  ! Module constants
  integer, parameter :: dp = kind(1.0d0)  ! Double precision kind
  integer, parameter :: sp = kind(1.0)    ! Single precision kind
  real(dp), parameter :: EPSILON_DP = 1.0d-10  ! Small value for comparisons
  
  !> @brief Generic interface for array sorting
  interface sort
    module procedure sort_real_dp
    module procedure sort_int
  end interface sort
  
  !> @brief Generic interface for array reversing
  interface reverse
    module procedure reverse_real_dp
    module procedure reverse_int
  end interface reverse
  
  !> @brief Generic interface for array sum
  interface array_sum
    module procedure array_sum_real_dp
    module procedure array_sum_int
  end interface array_sum
  
  !> @brief Generic interface for array product
  interface array_product
    module procedure array_product_real_dp
    module procedure array_product_int
  end interface array_product
  
  !> @brief Generic interface for finding minimum
  interface array_min
    module procedure array_min_real_dp
    module procedure array_min_int
  end interface array_min
  
  !> @brief Generic interface for finding maximum
  interface array_max
    module procedure array_max_real_dp
    module procedure array_max_int
  end interface array_max
  
  !> @brief Generic interface for finding index of minimum
  interface argmin
    module procedure argmin_real_dp
    module procedure argmin_int
  end interface argmin
  
  !> @brief Generic interface for finding index of maximum
  interface argmax
    module procedure argmax_real_dp
    module procedure argmax_int
  end interface argmax
  
  !> @brief Generic interface for unique elements
  interface unique
    module procedure unique_real_dp
    module procedure unique_int
  end interface unique
  
  !> @brief Generic interface for element-wise addition
  interface add_arrays
    module procedure add_arrays_real_dp
    module procedure add_arrays_int
  end interface add_arrays
  
  !> @brief Generic interface for element-wise subtraction
  interface subtract_arrays
    module procedure subtract_arrays_real_dp
    module procedure subtract_arrays_int
  end interface subtract_arrays
  
  !> @brief Generic interface for element-wise multiplication
  interface multiply_arrays
    module procedure multiply_arrays_real_dp
    module procedure multiply_arrays_int
  end interface multiply_arrays
  
  !> @brief Generic interface for element-wise division
  interface divide_arrays
    module procedure divide_arrays_real_dp
  end interface divide_arrays
  
  !> @brief Generic interface for dot product
  interface dot_product_safe
    module procedure dot_product_real_dp
    module procedure dot_product_int
  end interface dot_product_safe
  
contains

  ! ============================================================================
  ! Sorting Functions
  ! ============================================================================
  
  !> @brief Sort a real(dp) array in ascending order using quicksort
  !> @param[inout] arr Array to sort
  subroutine sort_real_dp(arr)
    real(dp), intent(inout) :: arr(:)
    integer :: n
    if (size(arr) > 1) then
      n = size(arr)
      call quicksort_dp(arr, 1, n)
    end if
  end subroutine sort_real_dp
  
  !> @brief Recursive quicksort for real(dp)
  recursive subroutine quicksort_dp(arr, low, high)
    real(dp), intent(inout) :: arr(:)
    integer, intent(in) :: low, high
    integer :: pivot_index
    if (low < high) then
      pivot_index = partition_dp(arr, low, high)
      call quicksort_dp(arr, low, pivot_index - 1)
      call quicksort_dp(arr, pivot_index + 1, high)
    end if
  end subroutine quicksort_dp
  
  !> @brief Partition function for quicksort (real(dp))
  function partition_dp(arr, low, high) result(pivot_index)
    real(dp), intent(inout) :: arr(:)
    integer, intent(in) :: low, high
    integer :: pivot_index, i, j
    real(dp) :: pivot, temp
    pivot = arr(high)
    i = low - 1
    do j = low, high - 1
      if (arr(j) <= pivot) then
        i = i + 1
        temp = arr(i)
        arr(i) = arr(j)
        arr(j) = temp
      end if
    end do
    temp = arr(i + 1)
    arr(i + 1) = arr(high)
    arr(high) = temp
    pivot_index = i + 1
  end function partition_dp
  
  !> @brief Sort an integer array in ascending order using quicksort
  !> @param[inout] arr Array to sort
  subroutine sort_int(arr)
    integer, intent(inout) :: arr(:)
    integer :: n
    if (size(arr) > 1) then
      n = size(arr)
      call quicksort_int(arr, 1, n)
    end if
  end subroutine sort_int
  
  !> @brief Recursive quicksort for integer
  recursive subroutine quicksort_int(arr, low, high)
    integer, intent(inout) :: arr(:)
    integer, intent(in) :: low, high
    integer :: pivot_index
    if (low < high) then
      pivot_index = partition_int(arr, low, high)
      call quicksort_int(arr, low, pivot_index - 1)
      call quicksort_int(arr, pivot_index + 1, high)
    end if
  end subroutine quicksort_int
  
  !> @brief Partition function for quicksort (integer)
  function partition_int(arr, low, high) result(pivot_index)
    integer, intent(inout) :: arr(:)
    integer, intent(in) :: low, high
    integer :: pivot_index, i, j, pivot, temp
    pivot = arr(high)
    i = low - 1
    do j = low, high - 1
      if (arr(j) <= pivot) then
        i = i + 1
        temp = arr(i)
        arr(i) = arr(j)
        arr(j) = temp
      end if
    end do
    temp = arr(i + 1)
    arr(i + 1) = arr(high)
    arr(high) = temp
    pivot_index = i + 1
  end function partition_int
  
  ! ============================================================================
  ! Search Functions
  ! ============================================================================
  
  !> @brief Linear search for a value in a real(dp) array
  !> @param[in] arr Array to search
  !> @param[in] value Value to find
  !> @return Index of value (0 if not found)
  function linear_search_dp(arr, value) result(index)
    real(dp), intent(in) :: arr(:)
    real(dp), intent(in) :: value
    integer :: index, i
    index = 0
    do i = 1, size(arr)
      if (abs(arr(i) - value) < EPSILON_DP) then
        index = i
        return
      end if
    end do
  end function linear_search_dp
  
  !> @brief Linear search for a value in an integer array
  !> @param[in] arr Array to search
  !> @param[in] value Value to find
  !> @return Index of value (0 if not found)
  function linear_search_int(arr, value) result(index)
    integer, intent(in) :: arr(:)
    integer, intent(in) :: value
    integer :: index, i
    index = 0
    do i = 1, size(arr)
      if (arr(i) == value) then
        index = i
        return
      end if
    end do
  end function linear_search_int
  
  !> @brief Binary search for a value in a sorted real(dp) array
  !> @param[in] arr Sorted array to search
  !> @param[in] value Value to find
  !> @return Index of value (0 if not found)
  function binary_search_dp(arr, value) result(index)
    real(dp), intent(in) :: arr(:)
    real(dp), intent(in) :: value
    integer :: index, left, right, mid
    index = 0
    left = 1
    right = size(arr)
    do while (left <= right)
      mid = (left + right) / 2
      if (abs(arr(mid) - value) < EPSILON_DP) then
        index = mid
        return
      else if (arr(mid) < value) then
        left = mid + 1
      else
        right = mid - 1
      end if
    end do
  end function binary_search_dp
  
  !> @brief Binary search for a value in a sorted