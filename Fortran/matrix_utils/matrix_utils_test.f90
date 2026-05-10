!> @file matrix_utils_test.f90
!> @brief Test program for matrix_utils module
!> @author AllToolkit Contributors
!> @version 1.0.0

program matrix_utils_test
  use matrix_utils
  implicit none
  
  integer :: test_count, pass_count
  real(dp) :: tolerance
  
  test_count = 0
  pass_count = 0
  tolerance = 1.0d-10
  
  print *, "============================================"
  print *, "    Matrix Utils Test Suite"
  print *, "============================================"
  print *, ""
  
  ! Test matrix creation
  call test_matrix_create()
  
  ! Test basic operations
  call test_matrix_addition()
  call test_matrix_subtraction()
  call test_matrix_multiplication()
  call test_matrix_scale()
  call test_matrix_transpose()
  
  ! Test matrix properties
  call test_matrix_trace()
  call test_matrix_determinant()
  call test_matrix_norm()
  
  ! Test matrix classification
  call test_is_symmetric()
  call test_is_diagonal()
  call test_is_identity()
  
  ! Test LU decomposition and linear system
  call test_lu_decomposition()
  call test_linear_system()
  call test_matrix_inverse()
  
  ! Test utility functions
  call test_get_diagonal()
  call test_get_row_column()
  call test_submatrix()
  
  ! Print summary
  print *, ""
  print *, "============================================"
  print '(A, I0, A, I0, A)', " Results: ", pass_count, "/", test_count, " tests passed"
  print *, "============================================"
  
  if (pass_count == test_count) then
    print *, "ALL TESTS PASSED!"
  else
    print *, "SOME TESTS FAILED!"
    stop 1
  end if

contains

  subroutine assert_true(condition, test_name)
    logical, intent(in) :: condition
    character(*), intent(in) :: test_name
    
    test_count = test_count + 1
    if (condition) then
      pass_count = pass_count + 1
      print '(A, A)', "  [PASS] ", test_name
    else
      print '(A, A)', "  [FAIL] ", test_name
    end if
  end subroutine assert_true
  
  subroutine assert_near(val1, val2, test_name)
    real(dp), intent(in) :: val1, val2
    character(*), intent(in) :: test_name
    
    call assert_true(abs(val1 - val2) < tolerance, test_name)
  end subroutine assert_near

  subroutine test_matrix_create()
    real(dp), allocatable :: mat_dp(:,:)
    integer, allocatable :: mat_int(:,:)
    real(dp), allocatable :: identity(:,:)
    
    print *, ""
    print *, "--- Matrix Creation Tests ---"
    
    ! Test create real matrix
    mat_dp = matrix_create(3, 4, 5.0_dp)
    call assert_true(size(mat_dp, 1) == 3 .and. size(mat_dp, 2) == 4, &
                     "Create real matrix: correct dimensions")
    call assert_true(mat_dp(1,1) == 5.0_dp .and. mat_dp(3,4) == 5.0_dp, &
                     "Create real matrix: correct initial values")
    
    ! Test create integer matrix
    mat_int = matrix_create_int(2, 3, 7)
    call assert_true(size(mat_int, 1) == 2 .and. size(mat_int, 2) == 3, &
                     "Create integer matrix: correct dimensions")
    call assert_true(mat_int(1,1) == 7 .and. mat_int(2,3) == 7, &
                     "Create integer matrix: correct initial values")
    
    ! Test identity matrix
    identity = matrix_identity(4)
    call assert_true(size(identity, 1) == 4 .and. size(identity, 2) == 4, &
                     "Identity matrix: correct dimensions")
    call assert_true(identity(1,1) == 1.0_dp .and. identity(2,2) == 1.0_dp, &
                     "Identity matrix: diagonal is 1")
    call assert_true(identity(1,2) == 0.0_dp .and. identity(3,1) == 0.0_dp, &
                     "Identity matrix: off-diagonal is 0")
  end subroutine test_matrix_create

  subroutine test_matrix_addition()
    real(dp), allocatable :: mat1(:,:), mat2(:,:), result(:,:)
    integer, allocatable :: int1(:,:), int2(:,:), int_result(:,:)
    
    print *, ""
    print *, "--- Matrix Addition Tests ---"
    
    ! Test real matrix addition
    ! Fortran column-major: mat1 = [[1,3], [2,4]] in math notation
    mat1 = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp], [2, 2])
    mat2 = reshape([5.0_dp, 6.0_dp, 7.0_dp, 8.0_dp], [2, 2])
    result = matrix_add(mat1, mat2)
    
    call assert_near(result(1,1), 6.0_dp, "Real addition: (1,1)")
    call assert_near(result(1,2), 10.0_dp, "Real addition: (1,2)")
    call assert_near(result(2,1), 8.0_dp, "Real addition: (2,1)")
    call assert_near(result(2,2), 12.0_dp, "Real addition: (2,2)")
    
    ! Test integer matrix addition
    allocate(int1(2,2), int2(2,2))
    int1 = reshape([1, 2, 3, 4], [2, 2])
    int2 = reshape([10, 20, 30, 40], [2, 2])
    int_result = matrix_add_int(int1, int2)
    
    call assert_true(int_result(1,1) == 11, "Integer addition: (1,1)")
    call assert_true(int_result(2,2) == 44, "Integer addition: (2,2)")
  end subroutine test_matrix_addition

  subroutine test_matrix_subtraction()
    real(dp), allocatable :: mat1(:,:), mat2(:,:), result(:,:)
    
    print *, ""
    print *, "--- Matrix Subtraction Tests ---"
    
    mat1 = reshape([10.0_dp, 20.0_dp, 30.0_dp, 40.0_dp], [2, 2])
    mat2 = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp], [2, 2])
    result = matrix_subtract(mat1, mat2)
    
    call assert_near(result(1,1), 9.0_dp, "Subtraction: (1,1)")
    call assert_near(result(1,2), 27.0_dp, "Subtraction: (1,2)")
    call assert_near(result(2,1), 18.0_dp, "Subtraction: (2,1)")
    call assert_near(result(2,2), 36.0_dp, "Subtraction: (2,2)")
  end subroutine test_matrix_subtraction

  subroutine test_matrix_multiplication()
    real(dp), allocatable :: mat1(:,:), mat2(:,:), result(:,:)
    
    print *, ""
    print *, "--- Matrix Multiplication Tests ---"
    
    ! Test 2x2 multiplication
    ! In Fortran column-major:
    ! mat1 = [[1, 3], [2, 4]] in mathematical notation (row-major view)
    ! mat2 = [[5, 7], [6, 8]] in mathematical notation
    ! mat1 * mat2 = [[1*5+3*6, 1*7+3*8], [2*5+4*6, 2*7+4*8]]
    !             = [[23, 31], [34, 46]]
    mat1 = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp], [2, 2])
    mat2 = reshape([5.0_dp, 6.0_dp, 7.0_dp, 8.0_dp], [2, 2])
    result = matrix_multiply(mat1, mat2)
    
    call assert_near(result(1,1), 23.0_dp, "Multiplication: (1,1)")
    call assert_near(result(1,2), 31.0_dp, "Multiplication: (1,2)")
    call assert_near(result(2,1), 34.0_dp, "Multiplication: (2,1)")
    call assert_near(result(2,2), 46.0_dp, "Multiplication: (2,2)")
    
    ! Test identity multiplication
    mat1 = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp], [2, 2])
    mat2 = matrix_identity(2)
    result = matrix_multiply(mat1, mat2)
    
    call assert_true(all(abs(result - mat1) < tolerance), &
                     "Multiplication by identity preserves matrix")
  end subroutine test_matrix_multiplication

  subroutine test_matrix_scale()
    real(dp), allocatable :: mat(:,:), result(:,:)
    
    print *, ""
    print *, "--- Matrix Scale Tests ---"
    
    mat = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp], [2, 2])
    result = matrix_scale(mat, 3.0_dp)
    
    call assert_near(result(1,1), 3.0_dp, "Scale: (1,1)")
    call assert_near(result(1,2), 9.0_dp, "Scale: (1,2)")
    call assert_near(result(2,1), 6.0_dp, "Scale: (2,1)")
    call assert_near(result(2,2), 12.0_dp, "Scale: (2,2)")
  end subroutine test_matrix_scale

  subroutine test_matrix_transpose()
    real(dp), allocatable :: mat(:,:), result(:,:)
    
    print *, ""
    print *, "--- Matrix Transpose Tests ---"
    
    mat = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 6.0_dp], [2, 3])
    result = matrix_transpose(mat)
    
    call assert_true(size(result, 1) == 3 .and. size(result, 2) == 2, &
                     "Transpose: correct dimensions")
    call assert_near(result(1,1), 1.0_dp, "Transpose: (1,1)")
    call assert_near(result(1,2), 2.0_dp, "Transpose: (1,2)")
    call assert_near(result(3,2), 6.0_dp, "Transpose: (3,2)")
    
    ! Double transpose should return original
    result = matrix_transpose(result)
    call assert_true(all(abs(result - mat) < tolerance), &
                     "Double transpose returns original")
  end subroutine test_matrix_transpose

  subroutine test_matrix_trace()
    real(dp), allocatable :: mat(:,:)
    integer, allocatable :: mat_int(:,:)
    
    print *, ""
    print *, "--- Matrix Trace Tests ---"
    
    mat = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 6.0_dp, &
                   7.0_dp, 8.0_dp, 9.0_dp], [3, 3])
    call assert_near(matrix_trace(mat), 15.0_dp, "Trace of 3x3 matrix")
    
    ! Non-square matrix: mat = [[1, 3, 5], [2, 4, 6]] in math notation
    ! trace = mat(1,1) + mat(2,2) = 1 + 4 = 5
    mat = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 6.0_dp], [2, 3])
    call assert_near(matrix_trace(mat), 5.0_dp, "Trace of 2x3 matrix")
    
    ! Integer matrix
    allocate(mat_int(2,2))
    mat_int = reshape([1, 2, 3, 4], [2, 2])
    call assert_true(matrix_trace_int(mat_int) == 5, "Trace of integer matrix")
  end subroutine test_matrix_trace

  subroutine test_matrix_determinant()
    real(dp), allocatable :: mat(:,:)
    
    print *, ""
    print *, "--- Matrix Determinant Tests ---"
    
    ! 2x2 determinant: mat = [[1, 3], [2, 4]] in math notation
    ! In Fortran column-major: mat(1,1)=1, mat(2,1)=2, mat(1,2)=3, mat(2,2)=4
    ! determinant = 1*4 - 3*2 = -2
    mat = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp], [2, 2])
    call assert_near(matrix_determinant(mat), -2.0_dp, "Determinant of 2x2")
    
    ! 3x3 determinant: in column-major order
    ! mat = [[1, 0, 5], [2, 1, 6], [3, 4, 0]] in math notation
    ! det = 1*(1*0 - 6*4) - 0*(2*0 - 6*3) + 5*(2*4 - 1*3) 
    !     = 1*(-24) + 5*(5) = -24 + 25 = 1
    mat = reshape([1.0_dp, 2.0_dp, 3.0_dp, &
                   0.0_dp, 1.0_dp, 4.0_dp, &
                   5.0_dp, 6.0_dp, 0.0_dp], [3, 3])
    call assert_near(matrix_determinant(mat), 1.0_dp, "Determinant of 3x3")
    
    ! Identity matrix
    mat = matrix_identity(3)
    call assert_near(matrix_determinant(mat), 1.0_dp, "Determinant of identity")
    
    ! Singular matrix
    mat = reshape([1.0_dp, 2.0_dp, 2.0_dp, 4.0_dp], [2, 2])
    call assert_near(matrix_determinant(mat), 0.0_dp, "Determinant of singular matrix")
  end subroutine test_matrix_determinant

  subroutine test_matrix_norm()
    real(dp), allocatable :: mat(:,:)
    
    print *, ""
    print *, "--- Matrix Norm Tests ---"
    
    mat = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp], [2, 2])
    ! Frobenius norm = sqrt(1+4+9+16) = sqrt(30)
    call assert_near(matrix_norm(mat), sqrt(30.0_dp), "Frobenius norm")
    
    ! Zero matrix
    mat = matrix_create(2, 2, 0.0_dp)
    call assert_near(matrix_norm(mat), 0.0_dp, "Norm of zero matrix")
  end subroutine test_matrix_norm

  subroutine test_is_symmetric()
    real(dp), allocatable :: mat(:,:)
    
    print *, ""
    print *, "--- Is Symmetric Tests ---"
    
    ! Symmetric matrix
    mat = reshape([1.0_dp, 2.0_dp, 3.0_dp, &
                   2.0_dp, 4.0_dp, 5.0_dp, &
                   3.0_dp, 5.0_dp, 6.0_dp], [3, 3])
    call assert_true(is_symmetric(mat), "Detect symmetric matrix")
    
    ! Non-symmetric matrix
    mat = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp], [2, 2])
    call assert_true(.not. is_symmetric(mat), "Detect non-symmetric matrix")
    
    ! Identity is symmetric
    mat = matrix_identity(4)
    call assert_true(is_symmetric(mat), "Identity is symmetric")
  end subroutine test_is_symmetric

  subroutine test_is_diagonal()
    real(dp), allocatable :: mat(:,:)
    
    print *, ""
    print *, "--- Is Diagonal Tests ---"
    
    ! Diagonal matrix
    mat = reshape([5.0_dp, 0.0_dp, 0.0_dp, 3.0_dp], [2, 2])
    call assert_true(is_diagonal(mat), "Detect diagonal matrix")
    
    ! Non-diagonal matrix
    mat = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp], [2, 2])
    call assert_true(.not. is_diagonal(mat), "Detect non-diagonal matrix")
    
    ! Identity is diagonal
    mat = matrix_identity(3)
    call assert_true(is_diagonal(mat), "Identity is diagonal")
  end subroutine test_is_diagonal

  subroutine test_is_identity()
    real(dp), allocatable :: mat(:,:)
    
    print *, ""
    print *, "--- Is Identity Tests ---"
    
    ! Identity matrix
    mat = matrix_identity(3)
    call assert_true(is_identity(mat), "Detect identity matrix")
    
    ! Non-identity matrix
    mat = reshape([2.0_dp, 0.0_dp, 0.0_dp, 1.0_dp], [2, 2])
    call assert_true(.not. is_identity(mat), "Detect non-identity matrix")
  end subroutine test_is_identity

  subroutine test_lu_decomposition()
    real(dp), allocatable :: mat(:,:), L(:,:), U(:,:), product(:,:)
    logical :: success
    
    print *, ""
    print *, "--- LU Decomposition Tests ---"
    
    mat = reshape([4.0_dp, 3.0_dp, 6.0_dp, 3.0_dp], [2, 2])
    success = lu_decompose(mat, L, U)
    
    call assert_true(success, "LU decomposition succeeded")
    
    ! Verify L is lower triangular with 1s on diagonal
    call assert_true(abs(L(1,1) - 1.0_dp) < tolerance, "L has 1 on diagonal")
    call assert_true(abs(L(1,2)) < tolerance, "L upper element is 0")
    
    ! Verify L*U = original matrix
    product = matrix_multiply(L, U)
    call assert_true(all(abs(product - mat) < tolerance), "L*U equals original matrix")
  end subroutine test_lu_decomposition

  subroutine test_linear_system()
    real(dp), allocatable :: A(:,:), b(:), x(:), Ax(:)
    
    print *, ""
    print *, "--- Linear System Tests ---"
    
    ! Solve: 2x + y = 5
    !        x + 3y = 6
    ! Solution: x = 9/5 = 1.8, y = 7/5 = 1.4
    A = reshape([2.0_dp, 1.0_dp, 1.0_dp, 3.0_dp], [2, 2])
    allocate(b(2))
    b = [5.0_dp, 6.0_dp]
    
    x = solve_linear_system(A, b)
    
    call assert_near(x(1), 1.8_dp, "Linear system: x1")
    call assert_near(x(2), 1.4_dp, "Linear system: x2")
    
    ! Verify solution
    Ax = matrix_vector_multiply(A, x)
    call assert_near(Ax(1), b(1), "Verify: Ax(1) = b(1)")
    call assert_near(Ax(2), b(2), "Verify: Ax(2) = b(2)")
  end subroutine test_linear_system

  subroutine test_matrix_inverse()
    real(dp), allocatable :: mat(:,:), inv(:,:), product(:,:)
    
    print *, ""
    print *, "--- Matrix Inverse Tests ---"
    
    ! 2x2 matrix inverse
    mat = reshape([4.0_dp, 7.0_dp, 2.0_dp, 6.0_dp], [2, 2])
    inv = matrix_inverse(mat)
    
    ! Verify A * A^-1 = I
    product = matrix_multiply(mat, inv)
    call assert_true(is_identity(product), "A * A^-1 = I")
    
    ! Verify A^-1 * A = I
    product = matrix_multiply(inv, mat)
    call assert_true(is_identity(product), "A^-1 * A = I")
  end subroutine test_matrix_inverse

  subroutine test_get_diagonal()
    real(dp), allocatable :: mat(:,:), diag(:)
    
    print *, ""
    print *, "--- Get Diagonal Tests ---"
    
    mat = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 6.0_dp, &
                   7.0_dp, 8.0_dp, 9.0_dp], [3, 3])
    diag = get_diagonal(mat)
    
    call assert_true(size(diag) == 3, "Diagonal: correct size")
    call assert_near(diag(1), 1.0_dp, "Diagonal: element 1")
    call assert_near(diag(2), 5.0_dp, "Diagonal: element 2")
    call assert_near(diag(3), 9.0_dp, "Diagonal: element 3")
  end subroutine test_get_diagonal

  subroutine test_get_row_column()
    real(dp), allocatable :: mat(:,:), row(:), col(:)
    
    print *, ""
    print *, "--- Get Row/Column Tests ---"
    
    mat = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 6.0_dp], [2, 3])
    
    ! Get row
    row = get_row(mat, 1)
    call assert_true(size(row) == 3, "Get row: correct size")
    call assert_near(row(1), 1.0_dp, "Get row: element 1")
    call assert_near(row(2), 3.0_dp, "Get row: element 2")
    call assert_near(row(3), 5.0_dp, "Get row: element 3")
    
    ! Get column
    col = get_column(mat, 2)
    call assert_true(size(col) == 2, "Get column: correct size")
    call assert_near(col(1), 3.0_dp, "Get column: element 1")
    call assert_near(col(2), 4.0_dp, "Get column: element 2")
  end subroutine test_get_row_column

  subroutine test_submatrix()
    real(dp), allocatable :: mat(:,:), sub(:,:)
    
    print *, ""
    print *, "--- Submatrix Tests ---"
    
    mat = reshape([1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, &
                   5.0_dp, 6.0_dp, 7.0_dp, 8.0_dp, &
                   9.0_dp, 10.0_dp, 11.0_dp, 12.0_dp], [3, 4])
    
    ! Extract 2x2 submatrix from middle
    sub = submatrix(mat, 2, 2, 3, 3)
    
    call assert_true(size(sub, 1) == 2 .and. size(sub, 2) == 2, &
                     "Submatrix: correct dimensions")
    ! In Fortran column-major:
    ! Row 2: [2, 5, 8, 11], Row 3: [3, 6, 9, 12]
    ! So submatrix(2:3, 2:3) = [[5, 8], [6, 9]]
    call assert_near(sub(1,1), 5.0_dp, "Submatrix: (1,1)")
    call assert_near(sub(1,2), 8.0_dp, "Submatrix: (1,2)")
    call assert_near(sub(2,1), 6.0_dp, "Submatrix: (2,1)")
    call assert_near(sub(2,2), 9.0_dp, "Submatrix: (2,2)")
  end subroutine test_submatrix

end program matrix_utils_test