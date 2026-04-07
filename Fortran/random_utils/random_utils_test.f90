!! random_utils_test.f90 - Unit tests for random_utils module
!!
!! Run tests:
!!   cd Fortran/random_utils
!!   gfortran -o random_utils_test mod.f90 random_utils_test.f90 && ./random_utils_test

program random_utils_test
  use random_utils
  implicit none
  
  integer :: passed = 0
  integer :: failed = 0
  integer :: i
  real(dp) :: r
  integer :: val
  integer, allocatable :: arr(:), perm(:), sample(:)
  real(dp), allocatable :: rarr(:)
  
  print *, "========================================"
  print *, "Random Utils Test Suite"
  print *, "========================================"
  print *
  
  ! Test 1: Seed management
  print *, "Test 1: Seed management"
  call set_seed(12345)
  call assert_true(seed_initialized == 1, "Seed should be initialized")
  call set_seed(54321)
  call assert_true(seed_initialized == 1, "Seed should remain initialized")
  print *, "  PASSED"
  print *
  
  ! Test 2: Random real in [0, 1)
  print *, "Test 2: Random real in [0, 1)"
  call set_seed(42)
  do i = 1, 100
    r = random_real()
    call assert_true(r >= 0.0_dp .and. r < 1.0_dp, "Value should be in [0, 1)")
  end do
  print *, "  PASSED (100 values checked)"
  print *
  
  ! Test 3: Random real in range
  print *, "Test 3: Random real in range [5.0, 10.0)"
  do i = 1, 100
    r = random_real_range(5.0_dp, 10.0_dp)
    call assert_true(r >= 5.0_dp .and. r < 10.0_dp, "Value should be in [5, 10)")
  end do
  print *, "  PASSED (100 values checked)"
  print *
  
  ! Test 4: Random integer in range
  print *, "Test 4: Random integer in range [1, 10]"
  do i = 1, 100
    val = random_int(1, 10)
    call assert_true(val >= 1 .and. val <= 10, "Value should be in [1, 10]")
  end do
  print *, "  PASSED (100 values checked)"
  print *
  
  ! Test 5: Random bool
  print *, "Test 5: Random bool"
  do i = 1, 100
    call random_bool()
  end do
  print *, "  PASSED (100 calls)"
  print *
  
  ! Test 6: Random bool with probability
  print *, "Test 6: Random bool with probability 0.0 and 1.0"
  do i = 1, 10
    call assert_true(.not. random_bool_prob(0.0_dp), "Probability 0 should always be false")
    call assert_true(random_bool_prob(1.0_dp), "Probability 1 should always be true")
  end do
  print *, "  PASSED"
  print *
  
  ! Test 7: Normal distribution
  print *, "Test 7: Normal distribution"
  do i = 1, 100
    r = random_normal()
    call assert_true(abs(r) < 10.0_dp, "Normal values should be reasonable")
  end do
  print *, "  PASSED (100 values checked)"
  print *
  
  ! Test 8: Normal with custom parameters
  print *, "Test 8: Normal distribution N(100, 15)"
  do i = 1, 100
    r = random_normal_dist(100.0_dp, 15.0_dp)
    call assert_true(r > 50.0_dp .and. r < 150.0_dp, "Values should be in reasonable range")
  end do
  print *, "  PASSED (100 values checked)"
  print *
  
  ! Test 9: Exponential distribution
  print *, "Test 9: Exponential distribution"
  do i = 1, 100
    r = random_exponential(1.0_dp)
    call assert_true(r >= 0.0_dp, "Exponential values should be non-negative")
  end do
  print *, "  PASSED (100 values checked)"
  print *
  
  ! Test 10: Poisson distribution
  print *, "Test 10: Poisson distribution"
  do i = 1, 100
    val = random_poisson(5.0_dp)
    call assert_true(val >= 0, "Poisson values should be non-negative")
  end do
  print *, "  PASSED (100 values checked)"
  print *
  
  ! Test 11: Random real array
  print *, "Test 11: Random real array"
  allocate(rarr(50))
  call random_real_array(rarr)
  do i = 1, size(rarr)
    call assert_true(rarr(i) >= 0.0_dp .and. rarr(i) < 1.0_dp, "Array values should be in [0, 1)")
  end do
  deallocate(rarr)
  print *, "  PASSED (50 values checked)"
  print *
  
  ! Test 12: Random int array
  print *, "Test 12: Random int array"
  arr = random_int_array(50, 1, 100)
  call assert_true(size(arr) == 50, "Array size should be 50")
  do i = 1, size(arr)
    call assert_true(arr(i) >= 1 .and. arr(i) <= 100, "Values should be in [1, 100]")
  end do
  print *, "  PASSED (50 values checked)"
  print *
  
  ! Test 13: Shuffle integer array
  print *, "Test 13: Shuffle integer array"
  allocate(arr(10))
  do i = 1, 10
    arr(i) = i
  end do
  call shuffle_int(arr)
  call assert_true(size(arr) == 10, "Size should remain 10")
  print *, "  PASSED"
  deallocate(arr)
  print *
  
  ! Test 14: Shuffle real array
  print *, "Test 14: Shuffle real array"
  allocate(rarr(10))
  do i = 1, 10
    rarr(i) = real(i, dp)
  end do
  call shuffle_real(rarr)
  call assert_true(size(rarr) == 10, "Size should remain 10")
  print *, "  PASSED"
  deallocate(rarr)
  print *
  
  ! Test 15: Random permutation
  print *, "Test 15: Random permutation"
  perm = random_permutation(20)
  call assert_true(size(perm) == 20, "Permutation size should be 20")
  print *, "  PASSED"
  deallocate(perm)
  print *
  
  ! Test 16: Random sample
  print *, "Test 16: Random sample without replacement"
  sample = random_sample(100, 10)
  call assert_true(size(sample) == 10, "Sample size should be 10")
  do i = 1, size(sample)
    call assert_true(sample(i) >= 1 .and. sample(i) <= 100, "Sample values should be in range")
  end do
  deallocate(sample)
  print *, "  PASSED"
  print *
  
  ! Test 17: Random choice from int array
  print *, "Test 17: Random choice from int array"
  allocate(arr(5))
  arr = [10, 20, 30, 40, 50]
  do i = 1, 20
    val = random_choice_int(arr)
    call assert_true(any(arr == val), "Choice should be from array")
  end do
  deallocate(arr)
  print *, "  PASSED (20 choices checked)"
  print *
  
  ! Test 18: Random choice from real array
  print *, "Test 18: Random choice from real array"
  allocate(rarr(5))
  rarr = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp]
  do i = 1, 20
    r = random_choice_real(rarr)
    call assert_true(any(abs(rarr - r) < 1.0e-10_dp), "Choice should be from array")
  end do
  deallocate(rarr)
  print *, "  PASSED (20 choices checked)"
  print *
  
  ! Test 19: Random angle
  print *, "Test 19: Random angle"
  do i = 1, 50
    r = random_angle()
    call assert_true(r >= 0.0_dp .and. r < 2.0_dp * PI, "Angle should be in [0, 2*pi)")
  end do
  print *, "  PASSED (50 angles checked)"
  print *
  
  ! Test 20: Random point in circle
  print *, "Test 20: Random point in circle"
  block
    real(dp) :: x, y, dist
    do i = 1, 50
      call random_point_in_circle(x, y)
      dist = sqrt(x*x + y*y)
      call assert_true(dist <= 1.0_dp + 1.0e-10_dp, "Point should be inside unit circle")
    end do
  end block
  print *, "  PASSED (50 points checked)"
  print *
  
  ! Test 21: Random point on sphere
  print *, "Test 21: Random point on sphere"
  block
    real(dp) :: x, y, z, dist
    do i = 1, 50
      call random_point_on_sphere(x, y, z)
      dist = sqrt(x*x + y*y + z*z)
      call assert_true(abs(dist - 1.0_dp) < 1.0e-10_dp, "Point should be on unit sphere")
    end do
  end block
  print *, "  PASSED (50 points checked)"
  print *
  
  ! Test 22: Random color
  print *, "Test 22: Random color"
  block
    integer :: rc, gc, bc
    do i = 1, 20
      call random_color(rc, gc, bc)
      call assert_true(rc >= 0 .and. rc <= 255, "Red should be in [0, 255]")
      call assert_true(gc >= 0 .and. gc <= 255, "Green should be in [0, 255]")
      call assert_true(bc >= 0 .and. bc <= 255, "Blue should be in [0, 255]")
    end do
  end block
  print *, "  PASSED (20 colors checked)"
  print *
  
  ! Test 23: Reproducibility
  print *, "Test 23: Reproducibility with same seed"
  block
    real(dp) :: r1, r2
    call set_seed(99999)
    r1 = random_real()
    call set_seed(99999)
    r2 = random_real()
    call assert_true(abs(r1 - r2) < 1.0e-10_dp, "Same seed should produce same value")
  end block
  print *, "  PASSED"
  print *
  
  ! Summary
  print *, "========================================"
  print *, "Test Summary"
  print *, "========================================"
  print *, "Passed:", passed
  print *, "Failed:", failed
  print *, "Total:  ", passed + failed
  print *, "========================================"
  
  if (failed > 0) then
    stop 1
  end if

contains

  !! Assert that condition is true
  subroutine assert_true(condition, message)
    logical, intent(in) :: condition
    character(len=*), intent(in) :: message
    
    if (condition) then
      passed = passed + 1
    else
      failed = failed + 1
      print *, "  FAILED:", message
    end if
  end subroutine assert_true

end program random_utils_test