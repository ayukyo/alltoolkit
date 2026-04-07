!! random_utils.f90 - Random Number Generation Utilities
!! A comprehensive random number generation module for Fortran
!! providing various distributions and utility functions.
!!
!! Features:
!! - Uniform distribution (integer and real)
!! - Normal (Gaussian) distribution
!! - Exponential distribution
!! - Poisson distribution
!! - Random seed management
!! - Random permutation and shuffling
!! - Random choice from arrays
!!
!! Author: AllToolkit
!! License: MIT

module random_utils
  implicit none
  
  !! Module constants
  integer, parameter :: dp = kind(1.0d0)  !! Double precision kind
  real(dp), parameter :: PI = 3.14159265358979323846_dp
  
  !! Private variables for random state
  integer, private :: seed_initialized = 0
  
contains
  
  ! ============================================================================
  ! Seed Management
  ! ============================================================================
  
  !! Initialize random seed using system clock
  !! Should be called once at program start for non-reproducible randomness
  subroutine init_random_seed()
    integer :: i, n, clock
    integer, allocatable :: seed(:)
    
    call random_seed(size=n)
    allocate(seed(n))
    
    call system_clock(count=clock)
    seed = clock + 37 * [(i - 1, i = 1, n)]
    call random_seed(put=seed)
    
    deallocate(seed)
    seed_initialized = 1
  end subroutine init_random_seed
  
  !! Set a specific seed for reproducible randomness
  !! @param seed_value - The seed value to use
  subroutine set_seed(seed_value)
    integer, intent(in) :: seed_value
    integer :: i, n
    integer, allocatable :: seed(:)
    
    call random_seed(size=n)
    allocate(seed(n))
    seed = seed_value + 37 * [(i - 1, i = 1, n)]
    call random_seed(put=seed)
    seed_initialized = 1
  end subroutine set_seed
  
  !! Get current random seed
  !! @param seed - Array to store the seed values
  subroutine get_seed(seed)
    integer, allocatable, intent(out) :: seed(:)
    integer :: n
    
    call random_seed(size=n)
    allocate(seed(n))
    call random_seed(get=seed)
  end subroutine get_seed
  
  ! ============================================================================
  ! Uniform Distribution
  ! ============================================================================
  
  !! Generate a random real number in [0, 1)
  !! @return Random real number in [0, 1)
  function random_real() result(r)
    real(dp) :: r
    
    if (seed_initialized == 0) call init_random_seed()
    call random_number(r)
  end function random_real
  
  !! Generate a random real number in [min_val, max_val)
  !! @param min_val - Minimum value (inclusive)
  !! @param max_val - Maximum value (exclusive)
  !! @return Random real number in [min_val, max_val)
  function random_real_range(min_val, max_val) result(r)
    real(dp), intent(in) :: min_val, max_val
    real(dp) :: r
    
    r = min_val + random_real() * (max_val - min_val)
  end function random_real_range
  
  !! Generate a random integer in [min_val, max_val]
  !! @param min_val - Minimum value (inclusive)
  !! @param max_val - Maximum value (inclusive)
  !! @return Random integer in [min_val, max_val]
  function random_int(min_val, max_val) result(i)
    integer, intent(in) :: min_val, max_val
    integer :: i
    real(dp) :: r
    
    r = random_real()
    i = min_val + floor(r * (max_val - min_val + 1))
    i = max(min_val, min(max_val, i))  !! Ensure bounds
  end function random_int
  
  !! Generate a random logical value
  !! @return Random .true. or .false.
  function random_bool() result(b)
    logical :: b
    
    b = random_real() < 0.5_dp
  end function random_bool
  
  !! Generate a random logical value with custom probability
  !! @param probability - Probability of returning .true. (0.0 to 1.0)
  !! @return Random logical value
  function random_bool_prob(probability) result(b)
    real(dp), intent(in) :: probability
    logical :: b
    
    b = random_real() < probability
  end function random_bool_prob
  
  ! ============================================================================
  ! Normal (Gaussian) Distribution
  ! ============================================================================
  
  !! Generate a random number from standard normal distribution (mean=0, std=1)
  !! Uses Box-Muller transform
  !! @return Random number from N(0, 1)
  function random_normal() result(z)
    real(dp) :: z
    real(dp) :: u1, u2, r, theta
    
    u1 = random_real()
    u2 = random_real()
    !! Box-Muller transform
    r = sqrt(-2.0_dp * log(u1))
    theta = 2.0_dp * PI * u2
    z = r * cos(theta)
  end function random_normal
  
  !! Generate a random number from normal distribution
  !! @param mean - Mean of the distribution
  !! @param std_dev - Standard deviation
  !! @return Random number from N(mean, std_dev^2)
  function random_normal_dist(mean, std_dev) result(x)
    real(dp), intent(in) :: mean, std_dev
    real(dp) :: x
    
    x = mean + std_dev * random_normal()
  end function random_normal_dist
  
  ! ============================================================================
  ! Exponential Distribution
  ! ============================================================================
  
  !! Generate a random number from exponential distribution
  !! @param lambda - Rate parameter (mean = 1/lambda)
  !! @return Random number from Exp(lambda)
  function random_exponential(lambda) result(x)
    real(dp), intent(in) :: lambda
    real(dp) :: x
    real(dp) :: u
    
    u = random_real()
    !! Avoid log(0)
    if (u < 1.0e-10_dp) u = 1.0e-10_dp
    x = -log(u) / lambda
  end function random_exponential
  
  ! ============================================================================
  ! Poisson Distribution
  ! ============================================================================
  
  !! Generate a random integer from Poisson distribution
  !! Uses the simple method for small lambda, rejection for larger
  !! @param lambda - Mean of the distribution
  !! @return Random integer from Poisson(lambda)
  function random_poisson(lambda) result(k)
    real(dp), intent(in) :: lambda
    integer :: k
    real(dp) :: L, p, u
    
    if (lambda < 30.0_dp) then
      !! Simple method for small lambda
      L = exp(-lambda)
      k = 0
      p = 1.0_dp
      do while (p > L)
        k = k + 1
        u = random_real()
        p = p * u
      end do
      k = k - 1
    else
      !! Normal approximation for large lambda
      k = nint(random_normal_dist(lambda, sqrt(lambda)))
      if (k < 0) k = 0
    end if
  end function random_poisson
  
  ! ============================================================================
  ! Random Arrays
  ! ============================================================================
  
  !! Fill an array with random real numbers in [0, 1)
  !! @param arr - Array to fill (modified in place)
  subroutine random_real_array(arr)
    real(dp), intent(out) :: arr(:)
    
    if (seed_initialized == 0) call init_random_seed()
    call random_number(arr)
  end subroutine random_real_array
  
  !! Fill an array with random real numbers in [min_val, max_val)
  !! @param arr - Array to fill (modified in place)
  !! @param min_val - Minimum value
  !! @param max_val - Maximum value
  subroutine random_real_array_range(arr, min_val, max_val)
    real(dp), intent(out) :: arr(:)
    real(dp), intent(in) :: min_val, max_val
    
    call random_real_array(arr)
    arr = min_val + arr * (max_val - min_val)
  end subroutine random_real_array_range
  
  !! Generate array of random integers
  !! @param n - Size of array
  !! @param min_val - Minimum value
  !! @param max_val - Maximum value
  !! @return Array of random integers
  function random_int_array(n, min_val, max_val) result(arr)
    integer, intent(in) :: n, min_val, max_val
    integer :: arr(n)
    integer :: i
    
    do i = 1, n
      arr(i) = random_int(min_val, max_val)
    end do
  end function random_int_array
  
  ! ============================================================================
  ! Shuffling and Permutation
  ! ============================================================================
  
  !! Shuffle an array in place (Fisher-Yates algorithm)
  !! @param arr - Array to shuffle (modified in place)
  subroutine shuffle_int(arr)
    integer, intent(inout) :: arr(:)
    integer :: i, j, temp
    integer :: n
    
    n = size(arr)
    do i = n, 2, -1
      j = random_int(1, i)
      temp = arr(j)
      arr(j) = arr(i)
      arr(i) = temp
    end do
  end subroutine shuffle_int
  
  !! Shuffle a real array in place (Fisher-Yates algorithm)
  !! @param arr - Array to shuffle (modified in place)
  subroutine shuffle_real(arr)
    real(dp), intent(inout) :: arr(:)
    integer :: i, j
    real(dp) :: temp
    integer :: n
    
    n = size(arr)
    do i = n, 2, -1
      j = random_int(1, i)
      temp = arr(j)
      arr(j) = arr(i)
      arr(i) = temp
    end do
  end subroutine shuffle_real
  
  !! Generate a random permutation of integers 1 to n
  !! @param n - Size of permutation
  !! @return Array containing permutation
  function random_permutation(n) result(perm)
    integer, intent(in) :: n
    integer :: perm(n)
    integer :: i
    
    do i = 1, n
      perm(i) = i
    end do
    call shuffle_int(perm)
  end function random_permutation
  
  !! Generate a random sample without replacement
  !! @param n - Population size
  !! @param k - Sample size
  !! @return Array of k unique integers from 1 to n
  function random_sample(n, k) result(sample)
    integer, intent(in) :: n, k
    integer :: sample(k)
    integer :: i, j
    integer, allocatable :: pool(:)
    
    if (k > n) then
      sample = -1
      return
    end if
    
    allocate(pool(n))
    do i = 1, n
      pool(i) = i
    end do
    
    do i = 1, k
      j = random_int(i, n)
      sample(i) = pool(j)
      pool(j) = pool(i)
    end do
    
    deallocate(pool)
  end function random_sample
  
  ! ============================================================================
  ! Random Choice
  ! ============================================================================
  
  !! Select a random element from an integer array
  !! @param arr - Array to choose from
  !! @return Randomly selected element
  function random_choice_int(arr) result(choice)
    integer, intent(in) :: arr(:)
    integer :: choice
    integer :: idx
    
    idx = random_int(1, size(arr))
    choice = arr(idx)
  end function random_choice_int
  
  !! Select a random element from a real array
  !! @param arr - Array to choose from
  !! @return Randomly selected element
  function random_choice_real(arr) result(choice)
    real(dp), intent(in) :: arr(:)
    real(dp) :: choice
    integer :: idx
    
    idx = random_int(1, size(arr))
    choice = arr(idx)
  end function random_choice_real
  
  !! Select a random element from a string array
  !! @param arr - Array to choose from
  !! @return Randomly selected element
  function random_choice_string(arr) result(choice)
    character(len=*), intent(in) :: arr(:)
    character(len=len(arr)) :: choice
    integer :: idx
    
    idx = random_int(1, size(arr))
    choice = arr(idx)
  end function random_choice_string
  
  ! ============================================================================
  ! Utility Functions
  ! ============================================================================
  
  !! Generate a random angle in radians [0, 2*pi)
  !! @return Random angle in radians
  function random_angle() result(angle)
    real(dp) :: angle
    
    angle = random_real() * 2.0_dp * PI
  end function random_angle
  
  !! Generate a random point inside a unit circle
  !! Uses rejection sampling
  !! @param x - X coordinate (output)
  !! @param y - Y coordinate (output)
  subroutine random_point_in_circle(x, y)
    real(dp), intent(out) :: x, y
    real(dp) :: r, theta
    
    r = sqrt(random_real())
    theta = random_angle()
    x = r * cos(theta)
    y = r * sin(theta)
  end subroutine random_point_in_circle
  
  !! Generate a random point on a unit sphere surface
  !! @param x - X coordinate (output)
  !! @param y - Y coordinate (output)
  !! @param z - Z coordinate (output)
  subroutine random_point_on_sphere(x, y, z)
    real(dp), intent(out) :: x, y, z
    real(dp) :: theta, phi
    
    theta = random_angle()
    phi = acos(2.0_dp * random_real() - 1.0_dp)
    x = sin(phi) * cos(theta)
    y = sin(phi) * sin(theta)
    z = cos(phi)
  end subroutine random_point_on_sphere
  
  !! Generate a random RGB color
  !! @param r - Red component [0, 255]
  !! @param g - Green component [0, 255]
  !! @param b - Blue component [0, 255]
  subroutine random_color(r, g, b)
    integer, intent(out) :: r, g, b
    
    r = random_int(0, 255)
    g = random_int(0, 255)
    b = random_int(0, 255)
  end subroutine random_color
  
end module random_utils