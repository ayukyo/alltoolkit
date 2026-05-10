!> @file mod.f90
!> @brief Matrix operations utilities for Fortran
!> @details Comprehensive matrix operations including creation, manipulation,
!          linear algebra operations, decomposition, and utility functions
!> @author AllToolkit Contributors
!> @version 1.0.0
!> @license MIT

module matrix_utils
  implicit none
  
  ! Module constants
  integer, parameter :: dp = kind(1.0d0)  ! Double precision kind
  integer, parameter :: sp = kind(1.0)    ! Single precision kind
  real(dp), parameter :: EPSILON_DP = 1.0d-12  ! Small value for comparisons
  
  !> @brief Matrix creation with initial value (real)
  interface matrix_create
    module procedure matrix_create_dp
  end interface matrix_create
  
  !> @brief Matrix creation with initial value (integer)
  interface matrix_create_int
    module procedure matrix_create_int
  end interface matrix_create_int
  
  !> @brief Matrix identity
  interface matrix_identity
    module procedure matrix_identity_dp
  end interface matrix_identity
  
  !> @brief Matrix transpose
  interface matrix_transpose
    module procedure matrix_transpose_dp
  end interface matrix_transpose
  
  !> @brief Matrix addition
  interface matrix_add
    module procedure matrix_add_dp
  end interface matrix_add
  
  !> @brief Matrix addition (integer)
  interface matrix_add_int
    module procedure matrix_add_int
  end interface matrix_add_int
  
  !> @brief Matrix subtraction
  interface matrix_subtract
    module procedure matrix_subtract_dp
  end interface matrix_subtract
  
  !> @brief Matrix subtraction (integer)
  interface matrix_subtract_int
    module procedure matrix_subtract_int
  end interface matrix_subtract_int
  
  !> @brief Matrix multiplication
  interface matrix_multiply
    module procedure matrix_multiply_dp
  end interface matrix_multiply
  
  !> @brief Matrix multiplication (integer)
  interface matrix_multiply_int
    module procedure matrix_multiply_int
  end interface matrix_multiply_int
  
  !> @brief Scalar multiplication
  interface matrix_scale
    module procedure matrix_scale_dp
  end interface matrix_scale
  
  !> @brief Scalar multiplication (integer)
  interface matrix_scale_int
    module procedure matrix_scale_int
  end interface matrix_scale_int
  
  !> @brief Matrix-vector multiplication
  interface matrix_vector_multiply
    module procedure matrix_vector_multiply_dp
  end interface matrix_vector_multiply
  
  !> @brief Matrix determinant
  interface matrix_determinant
    module procedure matrix_determinant_dp
  end interface matrix_determinant
  
  !> @brief Matrix trace
  interface matrix_trace
    module procedure matrix_trace_dp
  end interface matrix_trace
  
  !> @brief Matrix trace (integer)
  interface matrix_trace_int
    module procedure matrix_trace_int
  end interface matrix_trace_int
  
  !> @brief Matrix norm
  interface matrix_norm
    module procedure matrix_frobenius_norm
  end interface matrix_norm
  
  !> @brief LU decomposition
  interface lu_decompose
    module procedure lu_decompose_dp
  end interface lu_decompose
  
  !> @brief Solve linear system
  interface solve_linear_system
    module procedure solve_linear_system_dp
  end interface solve_linear_system
  
  !> @brief Matrix inverse
  interface matrix_inverse
    module procedure matrix_inverse_dp
  end interface matrix_inverse
  
  !> @brief Check if matrix is symmetric
  interface is_symmetric
    module procedure is_symmetric_dp
  end interface is_symmetric
  
  !> @brief Check if matrix is diagonal
  interface is_diagonal
    module procedure is_diagonal_dp
  end interface is_diagonal
  
  !> @brief Check if matrix is identity
  interface is_identity
    module procedure is_identity_dp
  end interface is_identity
  
  !> @brief Matrix copy
  interface matrix_copy
    module procedure matrix_copy_dp
  end interface matrix_copy
  
  !> @brief Matrix copy (integer)
  interface matrix_copy_int
    module procedure matrix_copy_int
  end interface matrix_copy_int
  
  !> @brief Get diagonal elements
  interface get_diagonal
    module procedure get_diagonal_dp
  end interface get_diagonal
  
  !> @brief Set diagonal elements
  interface set_diagonal
    module procedure set_diagonal_dp
  end interface set_diagonal
  
  !> @brief Get row
  interface get_row
    module procedure get_row_dp
  end interface get_row
  
  !> @brief Get column
  interface get_column
    module procedure get_column_dp
  end interface get_column
  
  !> @brief Submatrix extraction
  interface submatrix
    module procedure submatrix_dp
  end interface submatrix

contains

  ! ============================================================================
  ! Matrix Creation Functions
  ! ============================================================================
  
  !> @brief Create a real(dp) matrix filled with initial value
  !> @param[in] rows Number of rows
  !> @param[in] cols Number of columns
  !> @param[in] init_value Initial value (default 0.0)
  !> @return Allocated matrix
  function matrix_create_dp(rows, cols, init_value) result(mat)
    integer, intent(in) :: rows, cols
    real(dp), intent(in), optional :: init_value
    real(dp), allocatable :: mat(:,:)
    real(dp) :: val
    
    val = 0.0_dp
    if (present(init_value)) val = init_value
    
    allocate(mat(rows, cols))
    mat = val
  end function matrix_create_dp
  
  !> @brief Create an integer matrix filled with initial value
  !> @param[in] rows Number of rows
  !> @param[in] cols Number of columns
  !> @param[in] init_value Initial value (default 0)
  !> @return Allocated matrix
  function matrix_create_int(rows, cols, init_value) result(mat)
    integer, intent(in) :: rows, cols
    integer, intent(in), optional :: init_value
    integer, allocatable :: mat(:,:)
    integer :: val
    
    val = 0
    if (present(init_value)) val = init_value
    
    allocate(mat(rows, cols))
    mat = val
  end function matrix_create_int
  
  !> @brief Create an identity matrix
  !> @param[in] n Size of the square matrix
  !> @return Identity matrix
  function matrix_identity_dp(n) result(mat)
    integer, intent(in) :: n
    real(dp), allocatable :: mat(:,:)
    integer :: i
    
    allocate(mat(n, n))
    mat = 0.0_dp
    do i = 1, n
      mat(i, i) = 1.0_dp
    end do
  end function matrix_identity_dp
  
  ! ============================================================================
  ! Basic Matrix Operations
  ! ============================================================================
  
  !> @brief Transpose a real(dp) matrix
  !> @param[in] mat Input matrix
  !> @return Transposed matrix
  function matrix_transpose_dp(mat) result(transposed)
    real(dp), intent(in) :: mat(:,:)
    real(dp), allocatable :: transposed(:,:)
    integer :: rows, cols, i, j
    
    rows = size(mat, 1)
    cols = size(mat, 2)
    
    allocate(transposed(cols, rows))
    
    do j = 1, cols
      do i = 1, rows
        transposed(j, i) = mat(i, j)
      end do
    end do
  end function matrix_transpose_dp
  
  !> @brief Add two real(dp) matrices
  !> @param[in] mat1 First matrix
  !> @param[in] mat2 Second matrix
  !> @return Sum of matrices
  function matrix_add_dp(mat1, mat2) result(result_mat)
    real(dp), intent(in) :: mat1(:,:), mat2(:,:)
    real(dp), allocatable :: result_mat(:,:)
    integer :: rows, cols
    
    rows = size(mat1, 1)
    cols = size(mat1, 2)
    
    if (size(mat2, 1) /= rows .or. size(mat2, 2) /= cols) then
      error stop "Matrix dimensions must match for addition"
    end if
    
    allocate(result_mat(rows, cols))
    result_mat = mat1 + mat2
  end function matrix_add_dp
  
  !> @brief Add two integer matrices
  !> @param[in] mat1 First matrix
  !> @param[in] mat2 Second matrix
  !> @return Sum of matrices
  function matrix_add_int(mat1, mat2) result(result_mat)
    integer, intent(in) :: mat1(:,:), mat2(:,:)
    integer, allocatable :: result_mat(:,:)
    integer :: rows, cols
    
    rows = size(mat1, 1)
    cols = size(mat1, 2)
    
    if (size(mat2, 1) /= rows .or. size(mat2, 2) /= cols) then
      error stop "Matrix dimensions must match for addition"
    end if
    
    allocate(result_mat(rows, cols))
    result_mat = mat1 + mat2
  end function matrix_add_int
  
  !> @brief Subtract two real(dp) matrices
  !> @param[in] mat1 First matrix
  !> @param[in] mat2 Second matrix
  !> @return Difference of matrices
  function matrix_subtract_dp(mat1, mat2) result(result_mat)
    real(dp), intent(in) :: mat1(:,:), mat2(:,:)
    real(dp), allocatable :: result_mat(:,:)
    integer :: rows, cols
    
    rows = size(mat1, 1)
    cols = size(mat1, 2)
    
    if (size(mat2, 1) /= rows .or. size(mat2, 2) /= cols) then
      error stop "Matrix dimensions must match for subtraction"
    end if
    
    allocate(result_mat(rows, cols))
    result_mat = mat1 - mat2
  end function matrix_subtract_dp
  
  !> @brief Subtract two integer matrices
  !> @param[in] mat1 First matrix
  !> @param[in] mat2 Second matrix
  !> @return Difference of matrices
  function matrix_subtract_int(mat1, mat2) result(result_mat)
    integer, intent(in) :: mat1(:,:), mat2(:,:)
    integer, allocatable :: result_mat(:,:)
    integer :: rows, cols
    
    rows = size(mat1, 1)
    cols = size(mat1, 2)
    
    if (size(mat2, 1) /= rows .or. size(mat2, 2) /= cols) then
      error stop "Matrix dimensions must match for subtraction"
    end if
    
    allocate(result_mat(rows, cols))
    result_mat = mat1 - mat2
  end function matrix_subtract_int
  
  !> @brief Multiply two real(dp) matrices
  !> @param[in] mat1 First matrix
  !> @param[in] mat2 Second matrix
  !> @return Product of matrices
  function matrix_multiply_dp(mat1, mat2) result(result_mat)
    real(dp), intent(in) :: mat1(:,:), mat2(:,:)
    real(dp), allocatable :: result_mat(:,:)
    integer :: m, n, p, i, j, k
    
    m = size(mat1, 1)
    n = size(mat1, 2)
    p = size(mat2, 2)
    
    if (size(mat2, 1) /= n) then
      error stop "Inner matrix dimensions must match for multiplication"
    end if
    
    allocate(result_mat(m, p))
    result_mat = 0.0_dp
    
    do j = 1, p
      do i = 1, m
        do k = 1, n
          result_mat(i, j) = result_mat(i, j) + mat1(i, k) * mat2(k, j)
        end do
      end do
    end do
  end function matrix_multiply_dp
  
  !> @brief Multiply two integer matrices
  !> @param[in] mat1 First matrix
  !> @param[in] mat2 Second matrix
  !> @return Product of matrices
  function matrix_multiply_int(mat1, mat2) result(result_mat)
    integer, intent(in) :: mat1(:,:), mat2(:,:)
    integer, allocatable :: result_mat(:,:)
    integer :: m, n, p, i, j, k
    
    m = size(mat1, 1)
    n = size(mat1, 2)
    p = size(mat2, 2)
    
    if (size(mat2, 1) /= n) then
      error stop "Inner matrix dimensions must match for multiplication"
    end if
    
    allocate(result_mat(m, p))
    result_mat = 0
    
    do j = 1, p
      do i = 1, m
        do k = 1, n
          result_mat(i, j) = result_mat(i, j) + mat1(i, k) * mat2(k, j)
        end do
      end do
    end do
  end function matrix_multiply_int
  
  !> @brief Scale a real(dp) matrix by a scalar
  !> @param[in] mat Input matrix
  !> @param[in] scalar Scalar value
  !> @return Scaled matrix
  function matrix_scale_dp(mat, scalar) result(result_mat)
    real(dp), intent(in) :: mat(:,:)
    real(dp), intent(in) :: scalar
    real(dp), allocatable :: result_mat(:,:)
    integer :: rows, cols
    
    rows = size(mat, 1)
    cols = size(mat, 2)
    
    allocate(result_mat(rows, cols))
    result_mat = mat * scalar
  end function matrix_scale_dp
  
  !> @brief Scale an integer matrix by a scalar
  !> @param[in] mat Input matrix
  !> @param[in] scalar Scalar value
  !> @return Scaled matrix
  function matrix_scale_int(mat, scalar) result(result_mat)
    integer, intent(in) :: mat(:,:)
    integer, intent(in) :: scalar
    integer, allocatable :: result_mat(:,:)
    integer :: rows, cols
    
    rows = size(mat, 1)
    cols = size(mat, 2)
    
    allocate(result_mat(rows, cols))
    result_mat = mat * scalar
  end function matrix_scale_int
  
  !> @brief Multiply a real(dp) matrix by a vector
  !> @param[in] mat Input matrix (m x n)
  !> @param[in] vec Input vector (n elements)
  !> @return Result vector (m elements)
  function matrix_vector_multiply_dp(mat, vec) result(result_vec)
    real(dp), intent(in) :: mat(:,:), vec(:)
    real(dp), allocatable :: result_vec(:)
    integer :: m, n, i, j
    
    m = size(mat, 1)
    n = size(mat, 2)
    
    if (size(vec) /= n) then
      error stop "Vector length must match matrix columns"
    end if
    
    allocate(result_vec(m))
    result_vec = 0.0_dp
    
    do i = 1, m
      do j = 1, n
        result_vec(i) = result_vec(i) + mat(i, j) * vec(j)
      end do
    end do
  end function matrix_vector_multiply_dp
  
  ! ============================================================================
  ! Matrix Properties
  ! ============================================================================
  
  !> @brief Calculate the determinant of a real(dp) matrix using LU decomposition
  !> @param[in] mat Input square matrix
  !> @return Determinant value
  function matrix_determinant_dp(mat) result(det)
    real(dp), intent(in) :: mat(:,:)
    real(dp) :: det
    real(dp), allocatable :: lu(:,:)
    integer, allocatable :: pivot(:)
    integer :: n, i, info, swap_count
    
    n = size(mat, 1)
    
    if (size(mat, 2) /= n) then
      error stop "Determinant requires a square matrix"
    end if
    
    ! Special case for small matrices
    if (n == 1) then
      det = mat(1, 1)
      return
    end if
    
    if (n == 2) then
      det = mat(1, 1) * mat(2, 2) - mat(1, 2) * mat(2, 1)
      return
    end if
    
    if (n == 3) then
      det = mat(1,1)*(mat(2,2)*mat(3,3) - mat(2,3)*mat(3,2)) &
          - mat(1,2)*(mat(2,1)*mat(3,3) - mat(2,3)*mat(3,1)) &
          + mat(1,3)*(mat(2,1)*mat(3,2) - mat(2,2)*mat(3,1))
      return
    end if
    
    ! For larger matrices, use LU decomposition
    allocate(lu(n, n), pivot(n))
    lu = mat
    
    call lu_factor(lu, pivot, info)
    
    if (info > 0) then
      det = 0.0_dp  ! Singular matrix
    else
      ! Determinant is product of diagonal elements
      det = 1.0_dp
      do i = 1, n
        det = det * lu(i, i)
      end do
      ! Adjust for row swaps: count total swaps
      swap_count = 0
      do i = 1, n
        if (pivot(i) /= i) then
          swap_count = swap_count + 1
        end if
      end do
      ! Each swap flips the sign
      if (mod(swap_count, 2) == 1) then
        det = -det
      end if
    end if
    
    deallocate(lu, pivot)
  end function matrix_determinant_dp
  
  !> @brief LU factorization helper
  subroutine lu_factor(a, pivot, info)
    real(dp), intent(inout) :: a(:,:)
    integer, intent(out) :: pivot(:)
    integer, intent(out) :: info
    integer :: n, i, j, k, max_idx, temp
    real(dp) :: max_val, swap_val
    
    n = size(a, 1)
    info = 0
    
    ! Initialize pivot array
    do i = 1, n
      pivot(i) = i
    end do
    
    do k = 1, n - 1
      ! Find pivot
      max_val = abs(a(k, k))
      max_idx = k
      do i = k + 1, n
        if (abs(a(i, k)) > max_val) then
          max_val = abs(a(i, k))
          max_idx = i
        end if
      end do
      
      ! Swap rows if needed
      if (max_idx /= k) then
        do j = 1, n
          swap_val = a(k, j)
          a(k, j) = a(max_idx, j)
          a(max_idx, j) = swap_val
        end do
        temp = pivot(k)
        pivot(k) = pivot(max_idx)
        pivot(max_idx) = temp
      end if
      
      ! Check for singularity
      if (abs(a(k, k)) < EPSILON_DP) then
        info = k
        return
      end if
      
      ! Elimination
      do i = k + 1, n
        a(i, k) = a(i, k) / a(k, k)
        do j = k + 1, n
          a(i, j) = a(i, j) - a(i, k) * a(k, j)
        end do
      end do
    end do
    
    if (abs(a(n, n)) < EPSILON_DP) then
      info = n
    end if
  end subroutine lu_factor
  
  !> @brief Calculate the trace of a real(dp) matrix (sum of diagonal)
  !> @param[in] mat Input matrix
  !> @return Trace value
  function matrix_trace_dp(mat) result(tr)
    real(dp), intent(in) :: mat(:,:)
    real(dp) :: tr
    integer :: i, n
    
    n = min(size(mat, 1), size(mat, 2))
    tr = 0.0_dp
    
    do i = 1, n
      tr = tr + mat(i, i)
    end do
  end function matrix_trace_dp
  
  !> @brief Calculate the trace of an integer matrix
  !> @param[in] mat Input matrix
  !> @return Trace value
  function matrix_trace_int(mat) result(tr)
    integer, intent(in) :: mat(:,:)
    integer :: tr
    integer :: i, n
    
    n = min(size(mat, 1), size(mat, 2))
    tr = 0
    
    do i = 1, n
      tr = tr + mat(i, i)
    end do
  end function matrix_trace_int
  
  !> @brief Calculate the Frobenius norm of a matrix
  !> @param[in] mat Input matrix
  !> @return Frobenius norm (sqrt of sum of squares)
  function matrix_frobenius_norm(mat) result(norm)
    real(dp), intent(in) :: mat(:,:)
    real(dp) :: norm
    integer :: i, j
    
    norm = 0.0_dp
    do j = 1, size(mat, 2)
      do i = 1, size(mat, 1)
        norm = norm + mat(i, j) ** 2
      end do
    end do
    norm = sqrt(norm)
  end function matrix_frobenius_norm
  
  ! ============================================================================
  ! Matrix Classification
  ! ============================================================================
  
  !> @brief Check if a matrix is symmetric
  !> @param[in] mat Input matrix
  !> @return True if symmetric
  function is_symmetric_dp(mat) result(symmetric)
    real(dp), intent(in) :: mat(:,:)
    logical :: symmetric
    integer :: i, j, n
    
    n = size(mat, 1)
    if (size(mat, 2) /= n) then
      symmetric = .false.
      return
    end if
    
    symmetric = .true.
    do j = 1, n
      do i = j + 1, n
        if (abs(mat(i, j) - mat(j, i)) > EPSILON_DP) then
          symmetric = .false.
          return
        end if
      end do
    end do
  end function is_symmetric_dp
  
  !> @brief Check if a matrix is diagonal
  !> @param[in] mat Input matrix
  !> @return True if diagonal
  function is_diagonal_dp(mat) result(diagonal)
    real(dp), intent(in) :: mat(:,:)
    logical :: diagonal
    integer :: i, j, rows, cols
    
    rows = size(mat, 1)
    cols = size(mat, 2)
    diagonal = .true.
    
    do j = 1, cols
      do i = 1, rows
        if (i /= j .and. abs(mat(i, j)) > EPSILON_DP) then
          diagonal = .false.
          return
        end if
      end do
    end do
  end function is_diagonal_dp
  
  !> @brief Check if a matrix is identity
  !> @param[in] mat Input matrix
  !> @return True if identity matrix
  function is_identity_dp(mat) result(identity)
    real(dp), intent(in) :: mat(:,:)
    logical :: identity
    integer :: i, j, n
    
    n = size(mat, 1)
    if (size(mat, 2) /= n) then
      identity = .false.
      return
    end if
    
    identity = .true.
    do j = 1, n
      do i = 1, n
        if (i == j) then
          if (abs(mat(i, j) - 1.0_dp) > EPSILON_DP) then
            identity = .false.
            return
          end if
        else
          if (abs(mat(i, j)) > EPSILON_DP) then
            identity = .false.
            return
          end if
        end if
      end do
    end do
  end function is_identity_dp
  
  ! ============================================================================
  ! LU Decomposition and Linear System Solving
  ! ============================================================================
  
  !> @brief Perform LU decomposition
  !> @param[in] mat Input matrix
  !> @param[out] L Lower triangular matrix
  !> @param[out] U Upper triangular matrix
  !> @return True if successful
  function lu_decompose_dp(mat, L, U) result(success)
    real(dp), intent(in) :: mat(:,:)
    real(dp), allocatable, intent(out) :: L(:,:), U(:,:)
    logical :: success
    integer :: n, i, j, k
    real(dp) :: sum_val
    
    n = size(mat, 1)
    if (size(mat, 2) /= n) then
      success = .false.
      return
    end if
    
    allocate(L(n, n), U(n, n))
    L = 0.0_dp
    U = 0.0_dp
    
    do i = 1, n
      ! Upper triangular
      do j = i, n
        sum_val = 0.0_dp
        do k = 1, i - 1
          sum_val = sum_val + L(i, k) * U(k, j)
        end do
        U(i, j) = mat(i, j) - sum_val
      end do
      
      ! Lower triangular
      L(i, i) = 1.0_dp
      do j = i + 1, n
        sum_val = 0.0_dp
        do k = 1, i - 1
          sum_val = sum_val + L(j, k) * U(k, i)
        end do
        if (abs(U(i, i)) < EPSILON_DP) then
          success = .false.
          return
        end if
        L(j, i) = (mat(j, i) - sum_val) / U(i, i)
      end do
    end do
    
    success = .true.
  end function lu_decompose_dp
  
  !> @brief Solve a linear system Ax = b
  !> @param[in] A Coefficient matrix
  !> @param[in] b Right-hand side vector
  !> @return Solution vector x
  function solve_linear_system_dp(A, b) result(x)
    real(dp), intent(in) :: A(:,:), b(:)
    real(dp), allocatable :: x(:)
    real(dp), allocatable :: L(:,:), U(:,:), y(:)
    integer :: n, i, j
    real(dp) :: sum_val
    logical :: success
    
    n = size(A, 1)
    
    if (size(A, 2) /= n .or. size(b) /= n) then
      error stop "Invalid dimensions for linear system"
    end if
    
    success = lu_decompose_dp(A, L, U)
    if (.not. success) then
      error stop "Failed to decompose matrix (possibly singular)"
    end if
    
    allocate(y(n), x(n))
    
    ! Forward substitution: Ly = b
    do i = 1, n
      sum_val = 0.0_dp
      do j = 1, i - 1
        sum_val = sum_val + L(i, j) * y(j)
      end do
      y(i) = b(i) - sum_val
    end do
    
    ! Back substitution: Ux = y
    do i = n, 1, -1
      sum_val = 0.0_dp
      do j = i + 1, n
        sum_val = sum_val + U(i, j) * x(j)
      end do
      if (abs(U(i, i)) < EPSILON_DP) then
        error stop "Matrix is singular"
      end if
      x(i) = (y(i) - sum_val) / U(i, i)
    end do
    
    deallocate(L, U, y)
  end function solve_linear_system_dp
  
  !> @brief Compute the inverse of a matrix
  !> @param[in] mat Input matrix
  !> @return Inverse matrix
  function matrix_inverse_dp(mat) result(inv)
    real(dp), intent(in) :: mat(:,:)
    real(dp), allocatable :: inv(:,:)
    real(dp), allocatable :: L(:,:), U(:,:), y(:), b(:)
    integer :: n, i, j, k
    real(dp) :: sum_val
    logical :: success
    
    n = size(mat, 1)
    if (size(mat, 2) /= n) then
      error stop "Inverse requires a square matrix"
    end if
    
    success = lu_decompose_dp(mat, L, U)
    if (.not. success) then
      error stop "Failed to decompose matrix for inversion"
    end if
    
    allocate(inv(n, n), y(n), b(n))
    
    ! Solve for each column of the inverse
    do k = 1, n
      ! Set up unit vector
      b = 0.0_dp
      b(k) = 1.0_dp
      
      ! Forward substitution: Ly = b
      do i = 1, n
        sum_val = 0.0_dp
        do j = 1, i - 1
          sum_val = sum_val + L(i, j) * y(j)
        end do
        y(i) = b(i) - sum_val
      end do
      
      ! Back substitution: Ux = y
      do i = n, 1, -1
        sum_val = 0.0_dp
        do j = i + 1, n
          sum_val = sum_val + U(i, j) * inv(j, k)
        end do
        if (abs(U(i, i)) < EPSILON_DP) then
          error stop "Matrix is singular"
        end if
        inv(i, k) = (y(i) - sum_val) / U(i, i)
      end do
    end do
    
    deallocate(L, U, y, b)
  end function matrix_inverse_dp
  
  ! ============================================================================
  ! Utility Functions
  ! ============================================================================
  
  !> @brief Copy a real(dp) matrix
  !> @param[in] mat Input matrix
  !> @return Copy of matrix
  function matrix_copy_dp(mat) result(copy)
    real(dp), intent(in) :: mat(:,:)
    real(dp), allocatable :: copy(:,:)
    integer :: rows, cols
    
    rows = size(mat, 1)
    cols = size(mat, 2)
    
    allocate(copy(rows, cols))
    copy = mat
  end function matrix_copy_dp
  
  !> @brief Copy an integer matrix
  !> @param[in] mat Input matrix
  !> @return Copy of matrix
  function matrix_copy_int(mat) result(copy)
    integer, intent(in) :: mat(:,:)
    integer, allocatable :: copy(:,:)
    integer :: rows, cols
    
    rows = size(mat, 1)
    cols = size(mat, 2)
    
    allocate(copy(rows, cols))
    copy = mat
  end function matrix_copy_int
  
  !> @brief Get diagonal elements of a matrix
  !> @param[in] mat Input matrix
  !> @return Vector of diagonal elements
  function get_diagonal_dp(mat) result(diag)
    real(dp), intent(in) :: mat(:,:)
    real(dp), allocatable :: diag(:)
    integer :: i, n
    
    n = min(size(mat, 1), size(mat, 2))
    allocate(diag(n))
    
    do i = 1, n
      diag(i) = mat(i, i)
    end do
  end function get_diagonal_dp
  
  !> @brief Set diagonal elements of a matrix
  !> @param[inout] mat Input matrix
  !> @param[in] diag Vector of diagonal values
  subroutine set_diagonal_dp(mat, diag)
    real(dp), intent(inout) :: mat(:,:)
    real(dp), intent(in) :: diag(:)
    integer :: i, n
    
    n = min(size(mat, 1), size(mat, 2), size(diag))
    
    do i = 1, n
      mat(i, i) = diag(i)
    end do
  end subroutine set_diagonal_dp
  
  !> @brief Extract a row from a matrix
  !> @param[in] mat Input matrix
  !> @param[in] row_idx Row index (1-based)
  !> @return Row vector
  function get_row_dp(mat, row_idx) result(row_vec)
    real(dp), intent(in) :: mat(:,:)
    integer, intent(in) :: row_idx
    real(dp), allocatable :: row_vec(:)
    
    if (row_idx < 1 .or. row_idx > size(mat, 1)) then
      error stop "Row index out of bounds"
    end if
    
    allocate(row_vec(size(mat, 2)))
    row_vec = mat(row_idx, :)
  end function get_row_dp
  
  !> @brief Extract a column from a matrix
  !> @param[in] mat Input matrix
  !> @param[in] col_idx Column index (1-based)
  !> @return Column vector
  function get_column_dp(mat, col_idx) result(col_vec)
    real(dp), intent(in) :: mat(:,:)
    integer, intent(in) :: col_idx
    real(dp), allocatable :: col_vec(:)
    
    if (col_idx < 1 .or. col_idx > size(mat, 2)) then
      error stop "Column index out of bounds"
    end if
    
    allocate(col_vec(size(mat, 1)))
    col_vec = mat(:, col_idx)
  end function get_column_dp
  
  !> @brief Extract a submatrix
  !> @param[in] mat Input matrix
  !> @param[in] start_row Starting row (1-based)
  !> @param[in] start_col Starting column (1-based)
  !> @param[in] end_row Ending row
  !> @param[in] end_col Ending column
  !> @return Submatrix
  function submatrix_dp(mat, start_row, start_col, end_row, end_col) result(sub)
    real(dp), intent(in) :: mat(:,:)
    integer, intent(in) :: start_row, start_col, end_row, end_col
    real(dp), allocatable :: sub(:,:)
    integer :: i, j, sub_rows, sub_cols
    
    if (start_row < 1 .or. start_col < 1) then
      error stop "Start indices must be >= 1"
    end if
    if (end_row > size(mat, 1) .or. end_col > size(mat, 2)) then
      error stop "End indices exceed matrix bounds"
    end if
    if (start_row > end_row .or. start_col > end_col) then
      error stop "Start indices must be <= end indices"
    end if
    
    sub_rows = end_row - start_row + 1
    sub_cols = end_col - start_col + 1
    allocate(sub(sub_rows, sub_cols))
    
    do j = start_col, end_col
      do i = start_row, end_row
        sub(i - start_row + 1, j - start_col + 1) = mat(i, j)
      end do
    end do
  end function submatrix_dp

end module matrix_utils