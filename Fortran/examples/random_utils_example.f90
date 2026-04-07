!! random_utils_example.f90 - Usage examples for random_utils module
!!
!! Compile and run:
!!   cd Fortran/examples
!!   gfortran -o random_utils_example ../random_utils/mod.f90 random_utils_example.f90 && ./random_utils_example

program random_utils_example
  use random_utils
  implicit none
  
  integer :: i, val
  real(dp) :: r, x, y, z
  integer, allocatable :: arr(:), perm(:), sample(:)
  real(dp), allocatable :: rarr(:)
  integer :: r_color, g_color, b_color
  
  print *, "========================================"
  print *, "Random Utils Example Program"
  print *, "========================================"
  print *
  
  ! Example 1: Basic random number generation
  print *, "Example 1: Basic random numbers"
  print *, "----------------------------------------"
  call init_random_seed()  !! Initialize with system clock
  
  print *, "Random reals in [0, 1):"
  do i = 1, 5
    r = random_real()
    print *, "  ", r
  end do
  
  print *, "Random integers in [1, 100]:"
  do i = 1, 5
    val = random_int(1, 100)
    print *, "  ", val
  end do
  print *
  
  ! Example 2: Random numbers in specific range
  print *, "Example 2: Random numbers in range [10.0, 20.0)"
  print *, "----------------------------------------"
  do i = 1, 5
    r = random_real_range(10.0_dp, 20.0_dp)
    print *, "  ", r
  end do
  print *
  
  ! Example 3: Normal distribution
  print *, "Example 3: Normal distribution N(100, 15)"
  print *, "----------------------------------------"
  print *, "Values (simulating IQ scores):"
  do i = 1, 10
    r = random_normal_dist(100.0_dp, 15.0_dp)
    print *, "  ", r
  end do
  print *
  
  ! Example 4: Exponential distribution
  print *, "Example 4: Exponential distribution (lambda=0.5)"
  print *, "----------------------------------------"
  print *, "Values (simulating inter-arrival times):"
  do i = 1, 5
    r = random_exponential(0.5_dp)
    print *, "  ", r
  end do
  print *
  
  ! Example 5: Poisson distribution
  print *, "Example 5: Poisson distribution (lambda=4)"
  print *, "----------------------------------------"
  print *, "Values (simulating event counts):"
  do i = 1, 10
    val = random_poisson(4.0_dp)
    print *, "  ", val
  end do
  print *
  
  ! Example 6: Random boolean with probability
  print *, "Example 6: Random boolean with 70% true probability"
  print *, "----------------------------------------"
  print *, "Results (1=true, 0=false):"
  do i = 1, 10
    if (random_bool_prob(0.7_dp)) then
      print *, "  1"
    else
      print *, "  0"
    end if
  end do
  print *
  
  ! Example 7: Random array generation
  print *, "Example 7: Random real array"
  print *, "----------------------------------------"
  allocate(rarr(10))
  call random_real_array_range(rarr, 0.0_dp, 100.0_dp)
  print *, "Array values:"
  do i = 1, size(rarr)
    print *, "  rarr(", i, ") = ", rarr(i)
  end do
  deallocate(rarr)
  print *
  
  ! Example 8: Random integer array
  print *, "Example 8: Random integer array [1, 6] (dice rolls)"
  print *, "----------------------------------------"
  arr = random_int_array(10, 1, 6)
  print *, "Dice rolls:"
  do i = 1, size(arr)
    print *, "  Roll ", i, ": ", arr(i)
  end do
  deallocate(arr)
  print *
  
  ! Example 9: Shuffling
  print *, "Example 9: Shuffling an array"
  print *, "----------------------------------------"
  allocate(arr(10))
  do i = 1, 10
    arr(i) = i * 10  !! [10, 20, 30, ..., 100]
  end do
  print *, "Original: ", arr
  call shuffle_int(arr)
  print *, "Shuffled: ", arr
  deallocate(arr)
  print *
  
  ! Example 10: Random permutation
  print *, "Example 10: Random permutation of 1 to 8"
  print *, "----------------------------------------"
  perm = random_permutation(8)
  print *, "Permutation: ", perm
  deallocate(perm)
  print *
  
  ! Example 11: Random sample without replacement
  print *, "Example 11: Random sample of 5 from 1 to 20"
  print *, "----------------------------------------"
  sample = random_sample(20, 5)
  print *, "Sample: ", sample
  deallocate(sample)
  print *
  
  ! Example 12: Random choice from array
  print *, "Example 12: Random choice from array"
  print *, "----------------------------------------"
  allocate(arr(5))
  arr = [10, 20, 30, 40, 50]
  print *, "Array: ", arr
  print *, "Random choices:"
  do i = 1, 5
    val = random_choice_int(arr)
    print *, "  Choice ", i, ": ", val
  end do
  deallocate(arr)
  print *
  
  ! Example 13: Random point in circle
  print *, "Example 13: Random points in unit circle"
  print *, "----------------------------------------"
  do i = 1, 5
    call random_point_in_circle(x, y)
    print *, "  Point ", i, ": (", x, ", ", y, ")"
  end do
  print *
  
  ! Example 14: Random point on sphere
  print *, "Example 14: Random points on unit sphere"
  print *, "----------------------------------------"
  do i = 1, 5
    call random_point_on_sphere(x, y, z)
    print *, "  Point ", i, ": (", x, ", ", y, ", ", z, ")"
  end do
  print *
  
  ! Example 15: Random color
  print *, "Example 15: Random RGB colors"
  print *, "----------------------------------------"
  do i = 1, 5
    call random_color(r_color, g_color, b_color)
    print *, "  Color ", i, ": RGB(", r_color, ", ", g_color, ", ", b_color, ")"
  end do
  print *
  
  ! Example 16: Reproducible randomness
  print *, "Example 16: Reproducible randomness with seed"
  print *, "----------------------------------------"
  call set_seed(12345)
  print *, "First run with seed 12345:"
  do i = 1, 3
    print *, "  ", random_real()
  end do
  
  call set_seed(12345)
  print *, "Second run with same seed:"
  do i = 1, 3
    print *, "  ", random_real()
  end do
  print *, "(Values should be identical)"
  print *
  
  ! Example 17: Statistical simulation - estimate pi
  print *, "Example 17: Monte Carlo estimation of pi"
  print *, "----------------------------------------"
  block
    integer :: n_points = 100000
    integer :: inside_circle = 0
    real(dp) :: pi_estimate
    
    do i = 1, n_points
      call random_point_in_circle(x, y)
      if (x*x + y*y <= 1.0_dp) then
        inside_circle = inside_circle + 1
      end if
    end do
    
    pi_estimate = 4.0_dp * real(inside_circle, dp) / real(n_points, dp)
    print *, "Points: ", n_points
    print *, "Inside circle: ", inside_circle
    print *, "Estimated pi: ", pi_estimate
    print *, "Actual pi:    ", PI
    print *, "Error:        ", abs(pi_estimate - PI)
  end block
  print *
  
  print *, "========================================"
  print *, "Examples completed successfully!"
  print *, "========================================"

end program random_utils_example