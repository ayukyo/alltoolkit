!> @file usage_examples.f90
!> @brief Usage examples for matrix_utils module
!> @author AllToolkit Contributors
!> @version 1.0.0

program matrix_examples
  use matrix_utils
  implicit none
  
  print *, "============================================"
  print *, "    Matrix Utils - Usage Examples"
  print *, "============================================"
  print *, ""
  
  call example_matrix_creation()
  call example_basic_operations()
  call example_matrix_properties()
  call example_linear_algebra()
  call example_utility_functions()

contains

  subroutine example_matrix_creation()
    real(dp), allocatable :: mat(:,:), identity(:,:)
    integer, allocatable :: int_mat(:,:)
    
    print *, "--- Example 1: Matrix Creation ---"
    print *, ""
    
    ! Create a 3x4 matrix filled with zeros
    mat = matrix_create(3, 4)
    print *, "Created 3x4 zero matrix:"
    call print_matrix_dp(mat)
    print *, ""
    
    ! Create a matrix with initial value
    mat = matrix_create(2, 3, 7.5_dp)
    print *, "Created 2x3 matrix filled with 7.5:"
    call print_matrix_dp(mat)
    print *, ""
    
    ! Create identity matrix
    identity = matrix_identity(4)
    print *, "Created 4x4 identity matrix:"
    call print_matrix_dp(identity)
    print *, ""
    
    ! Create integer matrix
    int_mat = matrix_create_int(2, 2, 5)
    print *, "Created 2x2 integer matrix filled with 5:"
    call print_matrix_int(int_mat)
    print *, ""
  end subroutine example_matrix_creation

  subroutine example_basic_operations()
    real(dp), allocatable :: A(:,:), B(:,:), C(:,:)
    real(dp), allocatable :: vec(:), result_vec(:)
    
    print *, "--- Example 2: Basic Operations ---"
    print *, ""
    
    ! Matrix addition
    A = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp], [2, 2])
    B = reshape([5.0_dp, 6.0_dp, 7.0_dp, 8.0_dp], [2, 2])
    
    print *, "Matrix A:"
    call print_matrix_dp(A)
    print *, ""
    
    print *, "Matrix B:"
    call print_matrix_dp(B)
    print *, ""
    
    C = matrix_add(A, B)
    print *, "A + B:"
    call print_matrix_dp(C)
    print *, ""
    
    ! Matrix subtraction
    C = matrix_subtract(A, B)
    print *, "A - B:"
    call print_matrix_dp(C)
    print *, ""
    
    ! Matrix multiplication
    C = matrix_multiply(A, B)
    print *, "A * B:"
    call print_matrix_dp(C)
    print *, ""
    
    ! Scalar multiplication
    C = matrix_scale(A, 3.0_dp)
    print *, "A * 3.0:"
    call print_matrix_dp(C)
    print *, ""
    
    ! Transpose
    A = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 6.0_dp], [2, 3])
    print *, "Original 2x3 matrix:"
    call print_matrix_dp(A)
    print *, ""
    
    C = matrix_transpose(A)
    print *, "Transposed 3x2 matrix:"
    call print_matrix_dp(C)
    print *, ""
    
    ! Matrix-vector multiplication
    A = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 6.0_dp], [2, 3])
    allocate(vec(3))
    vec = [1.0_dp, 2.0_dp, 3.0_dp]
    
    print *, "Vector v:"
    call print_vector_dp(vec)
    print *, ""
    
    result_vec = matrix_vector_multiply(A, vec)
    print *, "A * v:"
    call print_vector_dp(result_vec)
    print *, ""
  end subroutine example_basic_operations

  subroutine example_matrix_properties()
    real(dp), allocatable :: A(:,:)
    real(dp) :: det, tr, norm_val
    real(dp), allocatable :: diag(:)
    
    print *, "--- Example 3: Matrix Properties ---"
    print *, ""
    
    A = reshape([1.0_dp, 2.0_dp, 3.0_dp, &
                4.0_dp, 5.0_dp, 6.0_dp, &
                7.0_dp, 8.0_dp, 10.0_dp], [3, 3])
    
    print *, "Matrix A:"
    call print_matrix_dp(A)
    print *, ""
    
    ! Trace
    tr = matrix_trace(A)
    print '(A, F8.2)', "Trace of A: ", tr
    print *, ""
    
    ! Determinant
    det = matrix_determinant(A)
    print '(A, F12.4)', "Determinant of A: ", det
    print *, ""
    
    ! Frobenius norm
    norm_val = matrix_norm(A)
    print '(A, F12.4)', "Frobenius norm of A: ", norm_val
    print *, ""
    
    ! Diagonal
    diag = get_diagonal(A)
    print *, "Diagonal elements:"
    call print_vector_dp(diag)
    print *, ""
    
    ! Matrix classification
    print *, "Matrix classification:"
    print '(A, L1)', "  Is symmetric: ", is_symmetric(A)
    print '(A, L1)', "  Is diagonal:  ", is_diagonal(A)
    print '(A, L1)', "  Is identity:  ", is_identity(A)
    print *, ""
    
    ! Symmetric matrix example
    A = reshape([1.0_dp, 2.0_dp, 3.0_dp, &
                 2.0_dp, 4.0_dp, 5.0_dp, &
                 3.0_dp, 5.0_dp, 6.0_dp], [3, 3])
    print *, "Symmetric matrix:"
    call print_matrix_dp(A)
    print '(A, L1)', "  Is symmetric: ", is_symmetric(A)
    print *, ""
  end subroutine example_matrix_properties

  subroutine example_linear_algebra()
    real(dp), allocatable :: A(:,:), L(:,:), U(:,:)
    real(dp), allocatable :: b(:), x(:), inv(:,:), product(:,:)
    logical :: success
    
    print *, "--- Example 4: Linear Algebra ---"
    print *, ""
    
    ! LU Decomposition
    A = reshape([2.0_dp, 1.0_dp, 1.0_dp, &
                 1.0_dp, 3.0_dp, 2.0_dp, &
                 1.0_dp, 0.0_dp, 2.0_dp], [3, 3])
    
    print *, "Matrix A for LU decomposition:"
    call print_matrix_dp(A)
    print *, ""
    
    success = lu_decompose(A, L, U)
    if (success) then
      print *, "L (Lower triangular):"
      call print_matrix_dp(L)
      print *, ""
      
      print *, "U (Upper triangular):"
      call print_matrix_dp(U)
      print *, ""
      
      product = matrix_multiply(L, U)
      print *, "L * U (should equal A):"
      call print_matrix_dp(product)
      print *, ""
    end if
    
    ! Solve linear system: Ax = b
    A = reshape([3.0_dp, 2.0_dp, -1.0_dp, &
                 2.0_dp, -2.0_dp, 4.0_dp, &
                 -1.0_dp, 0.5_dp, -1.0_dp], [3, 3])
    allocate(b(3))
    b = [1.0_dp, -2.0_dp, 0.0_dp]
    
    print *, "Solving Ax = b:"
    print *, "Matrix A:"
    call print_matrix_dp(A)
    print *, "Vector b:"
    call print_vector_dp(b)
    print *, ""
    
    x = solve_linear_system(A, b)
    print *, "Solution x:"
    call print_vector_dp(x)
    print *, ""
    
    ! Matrix inverse
    A = reshape([4.0_dp, 7.0_dp, 2.0_dp, 6.0_dp], [2, 2])
    print *, "Matrix A for inversion:"
    call print_matrix_dp(A)
    print *, ""
    
    inv = matrix_inverse(A)
    print *, "Inverse of A:"
    call print_matrix_dp(inv)
    print *, ""
    
    product = matrix_multiply(A, inv)
    print *, "A * A^-1 (should be identity):"
    call print_matrix_dp(product)
    print *, ""
  end subroutine example_linear_algebra

  subroutine example_utility_functions()
    real(dp), allocatable :: A(:,:), row(:), col(:), sub(:,:)
    real(dp), allocatable :: diag(:)
    
    print *, "--- Example 5: Utility Functions ---"
    print *, ""
    
    A = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, &
                 5.0_dp, 6.0_dp, 7.0_dp, 8.0_dp, &
                 9.0_dp, 10.0_dp, 11.0_dp, 12.0_dp], [3, 4])
    
    print *, "Matrix A (3x4):"
    call print_matrix_dp(A)
    print *, ""
    
    ! Get row
    row = get_row(A, 2)
    print *, "Row 2:"
    call print_vector_dp(row)
    print *, ""
    
    ! Get column
    col = get_column(A, 3)
    print *, "Column 3:"
    call print_vector_dp(col)
    print *, ""
    
    ! Get diagonal
    diag = get_diagonal(A)
    print *, "Diagonal elements:"
    call print_vector_dp(diag)
    print *, ""
    
    ! Set diagonal
    A = matrix_create(3, 3, 0.0_dp)
    call set_diagonal(A, [1.0_dp, 2.0_dp, 3.0_dp])
    print *, "Matrix after setting diagonal to [1, 2, 3]:"
    call print_matrix_dp(A)
    print *, ""
    
    ! Submatrix
    A = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, &
                 6.0_dp, 7.0_dp, 8.0_dp, 9.0_dp, 10.0_dp, &
                 11.0_dp, 12.0_dp, 13.0_dp, 14.0_dp, 15.0_dp, &
                 16.0_dp, 17.0_dp, 18.0_dp, 19.0_dp, 20.0_dp], [4, 5])
    
    print *, "Original 4x5 matrix:"
    call print_matrix_dp(A)
    print *, ""
    
    sub = submatrix(A, 2, 2, 3, 4)
    print *, "Submatrix from (2,2) to (3,4):"
    call print_matrix_dp(sub)
    print *, ""
    
    ! Matrix copy
    A = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp], [2, 2])
    sub = matrix_copy(A)
    print *, "Copy of matrix A:"
    call print_matrix_dp(sub)
    print *, ""
  end subroutine example_utility_functions

  subroutine print_matrix_dp(mat)
    real(dp), intent(in) :: mat(:,:)
    integer :: i, j
    
    do i = 1, size(mat, 1)
      do j = 1, size(mat, 2)
        write(*, '(F8.3)', advance='no') mat(i, j)
      end do
      print *, ""
    end do
  end subroutine print_matrix_dp
  
  subroutine print_matrix_int(mat)
    integer, intent(in) :: mat(:,:)
    integer :: i, j
    
    do i = 1, size(mat, 1)
      do j = 1, size(mat, 2)
        write(*, '(I5)', advance='no') mat(i, j)
      end do
      print *, ""
    end do
  end subroutine print_matrix_int
  
  subroutine print_vector_dp(vec)
    real(dp), intent(in) :: vec(:)
    integer :: i
    
    do i = 1, size(vec)
      write(*, '(F8.3)', advance='no') vec(i)
    end do
    print *, ""
  end subroutine print_vector_dp

end program matrix_examples