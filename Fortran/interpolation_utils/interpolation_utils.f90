! interpolation_utils.f90
! Numerical Interpolation Utilities Module
! Provides various interpolation methods with zero external dependencies
!
! Features:
!   - Linear interpolation
!   - Lagrange interpolation
!   - Newton interpolation (divided differences)
!   - Cubic spline interpolation (natural spline)
!   - Bilinear interpolation (2D)
!
! Author: AllToolkit
! Date: 2026-05-18

module interpolation_utils
    implicit none
    private
    
    ! Public interfaces
    public :: linear_interp
    public :: linear_interp_array
    public :: lagrange_interp
    public :: newton_interp
    public :: newton_coefficients
    public :: cubic_spline_init
    public :: cubic_spline_interp
    public :: bilinear_interp
    
    ! Derived type for cubic spline
    type, public :: cubic_spline
        real(8), allocatable :: x(:)      ! x data points
        real(8), allocatable :: y(:)      ! y data points
        real(8), allocatable :: m(:)      ! second derivatives
        integer :: n = 0                   ! number of points
        logical :: initialized = .false.
    contains
        procedure :: init => spline_init
        procedure :: interp => spline_interp_value
        procedure :: free => spline_free
    end type cubic_spline
    
contains

    !===========================================================================
    ! Linear Interpolation
    !===========================================================================
    
    ! Single point linear interpolation
    ! x0, y0, x1, y1: known points
    ! x: target x value
    ! Returns: interpolated y value
    function linear_interp(x0, y0, x1, y1, x) result(y)
        real(8), intent(in) :: x0, y0, x1, y1, x
        real(8) :: y
        
        if (abs(x1 - x0) < 1.0d-15) then
            y = y0
        else
            y = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        end if
    end function linear_interp
    
    ! Array-based linear interpolation
    ! x_data, y_data: known data points (must be sorted by x)
    ! x: target x values array
    ! Returns: interpolated y values array
    function linear_interp_array(x_data, y_data, x) result(y)
        real(8), intent(in) :: x_data(:), y_data(:), x(:)
        real(8), allocatable :: y(:)
        integer :: i, j, n_data, n_x
        integer :: idx
        
        n_data = size(x_data)
        n_x = size(x)
        allocate(y(n_x))
        
        if (n_data < 2) then
            y = y_data(1)
            return
        end if
        
        do i = 1, n_x
            ! Find interval
            if (x(i) <= x_data(1)) then
                ! Extrapolate left
                y(i) = linear_interp(x_data(1), y_data(1), x_data(2), y_data(2), x(i))
            else if (x(i) >= x_data(n_data)) then
                ! Extrapolate right
                y(i) = linear_interp(x_data(n_data-1), y_data(n_data-1), &
                                     x_data(n_data), y_data(n_data), x(i))
            else
                ! Find the interval
                idx = 1
                do j = 2, n_data
                    if (x(i) < x_data(j)) then
                        idx = j - 1
                        exit
                    end if
                end do
                y(i) = linear_interp(x_data(idx), y_data(idx), &
                                     x_data(idx+1), y_data(idx+1), x(i))
            end if
        end do
    end function linear_interp_array
    
    !===========================================================================
    ! Lagrange Interpolation
    !===========================================================================
    
    ! Lagrange polynomial interpolation
    ! x_data, y_data: known data points
    ! x: target x value
    ! Returns: interpolated y value
    function lagrange_interp(x_data, y_data, x) result(y)
        real(8), intent(in) :: x_data(:), y_data(:), x
        real(8) :: y
        real(8) :: term, denom
        integer :: i, j, n
        
        n = size(x_data)
        y = 0.0d0
        
        do i = 1, n
            term = y_data(i)
            do j = 1, n
                if (j /= i) then
                    denom = x_data(i) - x_data(j)
                    if (abs(denom) > 1.0d-15) then
                        term = term * (x - x_data(j)) / denom
                    end if
                end if
            end do
            y = y + term
        end do
    end function lagrange_interp
    
    !===========================================================================
    ! Newton Interpolation (Divided Differences)
    !===========================================================================
    
    ! Compute Newton divided difference coefficients
    ! x_data, y_data: known data points
    ! Returns: coefficient array
    function newton_coefficients(x_data, y_data) result(coeffs)
        real(8), intent(in) :: x_data(:), y_data(:)
        real(8), allocatable :: coeffs(:)
        real(8), allocatable :: table(:,:)
        integer :: n, i, j
        
        n = size(x_data)
        allocate(coeffs(n))
        allocate(table(n, n))
        
        ! Initialize first column with y values
        table(:, 1) = y_data
        
        ! Compute divided differences
        do j = 2, n
            do i = 1, n - j + 1
                table(i, j) = (table(i+1, j-1) - table(i, j-1)) / &
                              (x_data(i+j-1) - x_data(i))
            end do
        end do
        
        ! Extract coefficients (first row)
        coeffs = table(1, :)
        deallocate(table)
    end function newton_coefficients
    
    ! Newton polynomial interpolation
    ! x_data, y_data: known data points
    ! x: target x value
    ! Returns: interpolated y value
    function newton_interp(x_data, y_data, x) result(y)
        real(8), intent(in) :: x_data(:), y_data(:), x
        real(8) :: y
        real(8), allocatable :: coeffs(:)
        real(8) :: term
        integer :: n, i, j
        
        coeffs = newton_coefficients(x_data, y_data)
        n = size(x_data)
        
        y = coeffs(1)
        do i = 2, n
            term = coeffs(i)
            do j = 1, i - 1
                term = term * (x - x_data(j))
            end do
            y = y + term
        end do
        
        deallocate(coeffs)
    end function newton_interp
    
    !===========================================================================
    ! Cubic Spline Interpolation
    !===========================================================================
    
    ! Initialize cubic spline
    subroutine spline_init(this, x_data, y_data)
        class(cubic_spline), intent(inout) :: this
        real(8), intent(in) :: x_data(:), y_data(:)
        real(8), allocatable :: h(:), alpha(:), l(:), mu(:), z(:)
        integer :: n, i
        
        n = size(x_data)
        this%n = n
        
        ! Allocate arrays
        if (allocated(this%x)) deallocate(this%x)
        if (allocated(this%y)) deallocate(this%y)
        if (allocated(this%m)) deallocate(this%m)
        
        allocate(this%x(n), this%y(n), this%m(n))
        allocate(h(n-1), alpha(n), l(n), mu(n), z(n))
        
        this%x = x_data
        this%y = y_data
        
        ! Compute step sizes
        do i = 1, n - 1
            h(i) = x_data(i+1) - x_data(i)
        end do
        
        ! Compute alpha values
        alpha(1) = 0.0d0
        alpha(n) = 0.0d0
        do i = 2, n - 1
            alpha(i) = 3.0d0 * ((y_data(i+1) - y_data(i)) / h(i) - &
                                 (y_data(i) - y_data(i-1)) / h(i-1)) / &
                       (h(i-1) + h(i))
        end do
        
        ! Thomas algorithm for tridiagonal system
        l(1) = 1.0d0
        mu(1) = 0.0d0
        z(1) = 0.0d0
        
        do i = 2, n - 1
            l(i) = 2.0d0 * (x_data(i+1) - x_data(i-1)) - h(i-1) * mu(i-1)
            if (abs(l(i)) > 1.0d-15) then
                mu(i) = h(i) / l(i)
            else
                mu(i) = 0.0d0
            end if
            z(i) = (alpha(i) - h(i-1) * z(i-1)) / l(i)
        end do
        
        l(n) = 1.0d0
        z(n) = 0.0d0
        this%m(n) = 0.0d0
        
        ! Back substitution
        do i = n - 1, 1, -1
            this%m(i) = z(i) - mu(i) * this%m(i+1)
        end do
        
        deallocate(h, alpha, l, mu, z)
        this%initialized = .true.
    end subroutine spline_init
    
    ! Interpolate at a single point
    function spline_interp_value(this, x) result(y)
        class(cubic_spline), intent(in) :: this
        real(8), intent(in) :: x
        real(8) :: y
        integer :: i, n
        real(8) :: h, a, b, c, d
        
        if (.not. this%initialized) then
            y = 0.0d0
            return
        end if
        
        n = this%n
        
        ! Find interval
        if (x <= this%x(1)) then
            i = 1
        else if (x >= this%x(n)) then
            i = n - 1
        else
            do i = 1, n - 1
                if (x < this%x(i+1)) exit
            end do
        end if
        
        ! Evaluate cubic polynomial
        h = this%x(i+1) - this%x(i)
        a = this%y(i)
        b = (this%y(i+1) - this%y(i)) / h - h * (this%m(i+1) + 2.0d0 * this%m(i)) / 6.0d0
        c = this%m(i) / 2.0d0
        d = (this%m(i+1) - this%m(i)) / (6.0d0 * h)
        
        y = a + b * (x - this%x(i)) + c * (x - this%x(i))**2 + d * (x - this%x(i))**3
    end function spline_interp_value
    
    ! Free spline memory
    subroutine spline_free(this)
        class(cubic_spline), intent(inout) :: this
        
        if (allocated(this%x)) deallocate(this%x)
        if (allocated(this%y)) deallocate(this%y)
        if (allocated(this%m)) deallocate(this%m)
        this%n = 0
        this%initialized = .false.
    end subroutine spline_free
    
    ! Functional interface for cubic spline (creates temporary spline)
    function cubic_spline_init(x_data, y_data) result(spline)
        real(8), intent(in) :: x_data(:), y_data(:)
        type(cubic_spline) :: spline
        
        call spline%init(x_data, y_data)
    end function cubic_spline_init
    
    ! Functional interface for cubic spline interpolation
    function cubic_spline_interp(spline, x) result(y)
        type(cubic_spline), intent(in) :: spline
        real(8), intent(in) :: x
        real(8) :: y
        
        y = spline%interp(x)
    end function cubic_spline_interp
    
    !===========================================================================
    ! Bilinear Interpolation (2D)
    !===========================================================================
    
    ! Bilinear interpolation for 2D grids
    ! x1, x2: x coordinates of the grid cell
    ! y1, y2: y coordinates of the grid cell
    ! z11, z12, z21, z22: function values at corners
    !   z11 = f(x1, y1), z12 = f(x1, y2)
    !   z21 = f(x2, y1), z22 = f(x2, y2)
    ! x, y: target point
    ! Returns: interpolated value
    function bilinear_interp(x1, x2, y1, y2, z11, z12, z21, z22, x, y) result(z)
        real(8), intent(in) :: x1, x2, y1, y2
        real(8), intent(in) :: z11, z12, z21, z22
        real(8), intent(in) :: x, y
        real(8) :: z
        real(8) :: dx, dy, t1, t2
        
        dx = x2 - x1
        dy = y2 - y1
        
        if (abs(dx) < 1.0d-15 .or. abs(dy) < 1.0d-15) then
            z = z11
        else
            t1 = (x2 - x) / dx
            t2 = (x - x1) / dx
            
            z = t1 * ((y2 - y) / dy * z11 + (y - y1) / dy * z12) + &
                t2 * ((y2 - y) / dy * z21 + (y - y1) / dy * z22)
        end if
    end function bilinear_interp

end module interpolation_utils