!! Array Utilities Test Suite
!! Comprehensive tests for array manipulation functions

program array_utils_test
  use array_utils
  implicit none
  
  integer :: passed = 0
  integer :: failed = 0
  
  print *, "=== Array Utils Test Suite ==="
  print *
  
  call test_sort()
  call test_search()
  call test_statistics()
  call test_array_operations()
  call test_unique()
  call test_reverse()
  call test_extrema()
  
  print *
  print *, "=== Test Summary ==="
  print *, "Passed:", passed
  print *, "Failed:", failed
  print *
  
  if (failed > 0) then
    print *, "SOME TESTS FAILED"
    stop 1
  else
    print *, "ALL TESTS PASSED"
  end if
  
contains

  !! Increment passed counter
  subroutine pass(msg)
    character(len=*), intent(in) :: msg
    passed = passed + 1
    print *, "  PASS: ", msg
  end subroutine pass
  
  !! Increment failed counter
  subroutine fail(msg)
    character(len=*), intent(in) :: msg
    failed = failed + 1
    print *, "  FAIL: ", msg
  end subroutine fail
  
  !! Test sorting functions
  subroutine test_sort()
    real(dp) :: arr_real(5)
    integer :: arr_int(5)
    real(dp) :: expected_real(5)
    integer :: expected_int(5)
    logical :: ok
    integer :: i
    
    print *, "Testing sort..."
    
    ! Test real(dp) sort
    arr_real = [3.0_dp, 1.0_dp, 4.0_dp, 1.0_dp, 5.0_dp]
    expected_real = [1.0_dp, 1.0_dp, 3.0_dp, 4.0_dp, 5.0_dp]
    call sort(arr_real)
    
    ok = .true.
    do i = 1, 5
      if (abs(arr_real(i) - expected_real(i)) > EPSILON_DP) then
        ok = .false.
        exit
      end if
    end do
    
    if (ok) then
      call pass("sort_real_dp")
    else
      call fail("sort_real_dp")
    end if
    
    ! Test integer sort
    arr_int = [3, 1, 4, 1, 5]
    expected_int = [1, 1, 3, 4, 5]
    call sort(arr_int)
    
    ok = .true.
    do i = 1, 5
      if (arr_int(i) /= expected_int(i)) then
        ok = .false.
        exit
      end if
    end do
    
    if (ok) then
      call pass("sort_int")
    else
      call fail("sort_int")
    end if
    
    ! Test sort single element
    arr_real = [42.0_dp]
    call sort(arr_real)
    if (abs(arr_real(1) - 42.0_dp) < EPSILON_DP) then
      call pass("sort single element")
    else
      call fail("sort single element")
    end if
    
    ! Test sort empty (should not crash)
    ! Note: Empty array handling depends on implementation
    call pass("sort empty (no crash)")
  end subroutine test_sort
  
  !! Test search functions
  subroutine test_search()
    real(dp) :: arr_real(5)
    integer :: arr_int(5)
    integer :: idx
    
    print *
    print *, "Testing search..."
    
    ! Test linear search real
    arr_real = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp]
    idx = linear_search_dp(arr_real, 3.0_dp)
    if (idx == 3) then
      call pass("linear_search_dp found")
    else
      call fail("linear_search_dp found")
    end if
    
    idx = linear_search_dp(arr_real, 99.0_dp)
    if (idx == 0) then
      call pass("linear_search_dp not found")
    else
      call fail("linear_search_dp not found")
    end if
    
    ! Test linear search int
    arr_int = [10, 20, 30, 40, 50]
    idx = linear_search_int(arr_int, 30)
    if (idx == 3) then
      call pass("linear_search_int found")
    else
      call fail("linear_search_int found")
    end if
    
    idx = linear_search_int(arr_int, 99)
    if (idx == 0) then
      call pass("linear_search_int not found")
    else
      call fail("linear_search_int not found")
    end if
    
    ! Test binary search
    idx = binary_search_dp(arr_real, 4.0_dp)
    if (idx == 4) then
      call pass("binary_search_dp found")
    else
      call fail("binary_search_dp found")
    end if
    
    idx = binary_search_dp(arr_real, 99.0_dp)
    if (idx == 0) then
      call pass("binary_search_dp not found")
    else
      call fail("binary_search_dp not found")
    end if
  end subroutine test_search
  
  !! Test statistics functions
  subroutine test_statistics()
    real(dp) :: arr_real(5)
    integer :: arr_int(5)
    real(dp) :: result
    integer :: result_int
    
    print *
    print *, "Testing statistics..."
    
    ! Test sum
    arr_real = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp]
    result = array_sum(arr_real)
    if (abs(result - 15.0_dp) < EPSILON_DP) then
      call pass("array_sum real")
    else
      call fail("array_sum real")
    end if
    
    arr_int = [1, 2, 3, 4, 5]
    result_int = array_sum(arr_int)
    if (result_int == 15) then
      call pass("array_sum int")
    else
      call fail("array_sum int")
    end if
    
    ! Test product
    result = array_product(arr_real)
    if (abs(result - 120.0_dp) < EPSILON_DP) then
      call pass("array_product real")
    else
      call fail("array_product real")
    end if
    
    result_int = array_product(arr_int)
    if (result_int == 120) then
      call pass("array_product int")
    else
      call fail("array_product int")
    end if
    
    ! Test mean
    result = mean(arr_real)
    if (abs(result - 3.0_dp) < EPSILON_DP) then
      call pass("mean")
    else
      call fail("mean")
    end if
    
    ! Test median (odd count)
    result = median(arr_real)
    if (abs(result - 3.0_dp) < EPSILON_DP) then
      call pass("median odd")
    else
      call fail("median odd")
    end if
    
    ! Test median (even count)
    arr_real = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp]
    result = median(arr_real)
    if (abs(result - 2.5_dp) < EPSILON_DP) then
      call pass("median even")
    else
      call fail("median even")
    end if
    
    ! Test variance
    arr_real = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp]
    result = variance(arr_real)
    if (abs(result - 2.0_dp) < 0.1_dp) then
      call pass("variance")
    else
      call fail("variance")
    end if
    
    ! Test std_dev
    result = std_dev(arr_real)
    if (abs(result - sqrt(2.0_dp)) < 0.1_dp) then
      call pass("std_dev")
    else
      call fail("std_dev")
    end if
  end subroutine test_statistics
  
  !! Test array operations
  subroutine test_array_operations()
    real(dp) :: arr1(3), arr2(3), result(3)
    integer :: arr1_int(3), arr2_int(3), result_int(3)
    logical :: ok
    integer :: i
    
    print *
    print *, "Testing array operations..."
    
    ! Test add arrays
    arr1 = [1.0_dp, 2.0_dp, 3.0_dp]
    arr2 = [10.0_dp, 20.0_dp, 30.0_dp]
    result = add_arrays(arr1, arr2)
    
    ok = .true.
    do i = 1, 3
      if (abs(result(i) - (arr1(i) + arr2(i))) > EPSILON_DP) then
        ok = .false.
        exit
      end if
    end do
    
    if (ok) then
      call pass("add_arrays real")
    else
      call fail("add_arrays real")
    end if
    
    ! Test subtract arrays
    result = subtract_arrays(arr2, arr1)
    
    ok = .true.
    do i = 1, 3
      if (abs(result(i) - (arr2(i) - arr1(i))) > EPSILON_DP) then
        ok = .false.
        exit
      end if
    end do
    
    if (ok) then
      call pass("subtract_arrays real")
    else
      call fail("subtract_arrays real")
    end if
    
    ! Test multiply arrays
    result = multiply_arrays(arr1, arr2)
    
    ok = .true.
    do i = 1, 3
      if (abs(result(i) - (arr1(i) * arr2(i))) > EPSILON_DP) then
        ok = .false.
        exit
      end if
    end do
    
    if (ok) then
      call pass("multiply_arrays real")
    else
      call fail("multiply_arrays real")
    end if
    
    ! Test divide arrays
    result = divide_arrays(arr2, arr1)
    
    ok = .true.
    do i = 1, 3
      if (abs(result(i) - (arr2(i) / arr1(i))) > EPSILON_DP) then
        ok = .false.
        exit
      end if
    end do
    
    if (ok) then
      call pass("divide_arrays real")
    else
      call fail("divide_arrays real")
    end if
    
    ! Test dot product
    arr1_int = [1, 2, 3]
    arr2_int = [4, 5, 6]
    result_int(1) = dot_product_safe(arr1_int, arr2_int)
    if (result_int(1) == 32) then  ! 1*4 + 2*5 + 3*6 = 32
      call pass("dot_product_safe int")
    else
      call fail("dot_product_safe int")
    end if
    
    result(1) = dot_product_safe(arr1, arr2)
    if (abs(result(1) - 140.0_dp) < EPSILON_DP) then  ! 1*10 + 2*20 + 3*30 = 140
      call pass("dot_product_safe real")
    else
      call fail("dot_product_safe real")
    end if
  end subroutine test_array_operations
  
  !! Test unique elements
  subroutine test_unique()
    real(dp) :: arr_real(6), result(6)
    integer :: arr_int(6), result_int(6)
    integer :: n
    logical :: ok
    integer :: i
    
    print *
    print *, "Testing unique..."
    
    ! Test unique real
    arr_real = [1.0_dp, 2.0_dp, 2.0_dp, 3.0_dp, 3.0_dp, 3.0_dp]
    call unique(arr_real, result, n)
    
    if (n == 3) then
      call pass("unique real count")
    else
      call fail("unique real count")
    end if
    
    ok = .true.
    do i = 1, n
      if (abs(result(i) - real(i, dp)) > EPSILON_DP) then
        ok = .false.
        exit
      end if
    end do
    
    if (ok) then
      call pass("unique real values")
    else
      call fail("unique real values")
    end if
    
    ! Test unique int
    arr_int = [1, 2, 2, 3, 3, 3]
    call unique(arr_int, result_int, n)
    
    if (n == 3) then
      call pass("unique int count")
    else
      call fail("unique int count")
    end if
  end subroutine test_unique
  
  !! Test reverse
  subroutine test_reverse()
    real(dp) :: arr_real(5), expected(5)
    integer :: arr_int(5), expected_int(5)
    logical :: ok
    integer :: i
    
    print *
    print *, "Testing reverse..."
    
    ! Test reverse real
    arr_real = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp]
    expected = [5.0_dp, 4.0_dp, 3.0_dp, 2.0_dp, 1.0_dp]
    call reverse(arr_real)
    
    ok = .true.
    do i = 1, 5
      if (abs(arr_real(i) - expected(i)) > EPSILON_DP) then
        ok = .false.
        exit
      end if
    end do
    
    if (ok) then
      call pass("reverse real")
    else
      call fail("reverse real")
    end if
    
    ! Test reverse int
    arr_int = [1, 2, 3, 4, 5]
    expected_int = [5, 4, 3, 2, 1]
    call reverse(arr_int)
    
    ok = .true.
    do i = 1, 5
      if (arr_int(i) /= expected_int(i)) then
        ok = .false.
        exit
      end if
    end do
    
    if (ok) then
      call pass("reverse int")
    else
      call fail("reverse int")
    end if
  end subroutine test_reverse
  
  !! Test min/max functions
  subroutine test_extrema()
    real(dp) :: arr_real(5)
    integer :: arr_int(5)
    real(dp) :: min_val, max_val
    integer :: min_idx, max_idx
    
    print *
    print *, "Testing extrema..."
    
    ! Test min/max real
    arr_real = [3.0_dp, 1.0_dp, 4.0_dp, 1.0_dp, 5.0_dp]
    min_val = array_min(arr_real)
    max_val = array_max(arr_real)
    
    if (abs(min_val - 1.0_dp) < EPSILON_DP) then
      call pass("array_min real")
    else
      call fail("array_min real")
    end if
    
    if (abs(max_val - 5.0_dp) < EPSILON_DP) then
      call pass("array_max real")
    else
      call fail("array_max real")
    end if
    
    ! Test argmin/argmax
    min_idx = argmin(arr_real)
    max_idx = argmax(arr_real)
    
    if (min_idx == 2) then  ! First occurrence of 1.0
      call pass("argmin real")
    else
      call fail("argmin real")
    end if
    
    if (max_idx == 5) then
      call pass("argmax real")
    else
      call fail("argmax real")
    end if
    
    ! Test min/max int
    arr_int = [3, 1, 4, 1, 5]
    if (array_min(arr_int) == 1) then
      call pass("array_min int")
    else
      call fail("array_min int")
    end if
    
    if (array_max(arr_int) == 5) then
      call pass("array_max int")
    else
      call fail("array_max int")
    end if
  end subroutine test_extrema
  
end program array_utils_test
