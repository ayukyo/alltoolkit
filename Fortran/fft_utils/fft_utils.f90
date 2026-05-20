!===============================================================================
! FFT Utils - Fast Fourier Transform Utilities in Fortran
!===============================================================================
! A pure Fortran implementation of FFT algorithms with zero external dependencies.
! Includes:
!   - Cooley-Tukey radix-2 DIT FFT
!   - Inverse FFT
!   - Real FFT (using complex FFT)
!   - Frequency bin calculation
!   - Power spectrum computation
!   - Window functions (Hanning, Hamming, Blackman)
!
! Author: AllToolkit Auto-Generator
! Date: 2026-05-20
! License: MIT
!===============================================================================

module fft_utils
    implicit none
    private
    
    ! Constants
    real(8), parameter, public :: PI = 3.14159265358979323846d0
    real(8), parameter, public :: TWO_PI = 2.0d0 * PI
    
    ! Public procedures
    public :: fft
    public :: ifft
    public :: rfft
    public :: irfft
    public :: fft_freq
    public :: power_spectrum
    public :: next_power_of_two
    public :: hanning_window
    public :: hamming_window
    public :: blackman_window
    public :: apply_window
    public :: fft_shift
    public :: magnitude
    public :: phase
    
contains

    !---------------------------------------------------------------------------
    ! Bit reversal for FFT
    !---------------------------------------------------------------------------
    subroutine bit_reverse(data, n)
        complex(8), intent(inout) :: data(:)
        integer, intent(in) :: n
        
        integer :: i, j, k
        complex(8) :: temp
        
        j = 1
        do i = 1, n - 1
            if (i < j) then
                temp = data(j)
                data(j) = data(i)
                data(i) = temp
            end if
            k = n / 2
            do while (k < j)
                j = j - k
                k = k / 2
            end do
            j = j + k
        end do
    end subroutine bit_reverse

    !---------------------------------------------------------------------------
    ! Cooley-Tukey radix-2 DIT FFT
    ! Input: complex array, must have length that is a power of 2
    ! Output: FFT of input (in-place)
    !---------------------------------------------------------------------------
    subroutine fft(data, n)
        complex(8), intent(inout) :: data(:)
        integer, intent(in) :: n
        
        integer :: stage, butterfly_size, butterfly_count
        integer :: group, pair, idx1, idx2
        real(8) :: angle
        complex(8) :: w, w_step, temp
        
        ! Bit reversal
        call bit_reverse(data, n)
        
        ! Cooley-Tukey FFT
        butterfly_size = 2
        do while (butterfly_size <= n)
            angle = -TWO_PI / butterfly_size
            w_step = cmplx(cos(angle), sin(angle), 8)
            
            butterfly_count = n / butterfly_size
            do group = 0, butterfly_count - 1
                w = cmplx(1.0d0, 0.0d0, 8)
                do pair = 0, butterfly_size / 2 - 1
                    idx1 = group * butterfly_size + pair + 1
                    idx2 = idx1 + butterfly_size / 2
                    
                    temp = w * data(idx2)
                    data(idx2) = data(idx1) - temp
                    data(idx1) = data(idx1) + temp
                    
                    w = w * w_step
                end do
            end do
            
            butterfly_size = butterfly_size * 2
        end do
    end subroutine fft

    !---------------------------------------------------------------------------
    ! Inverse FFT
    !---------------------------------------------------------------------------
    subroutine ifft(data, n)
        complex(8), intent(inout) :: data(:)
        integer, intent(in) :: n
        
        integer :: i
        
        ! Conjugate
        do i = 1, n
            data(i) = conjg(data(i))
        end do
        
        ! Forward FFT
        call fft(data, n)
        
        ! Conjugate and scale
        do i = 1, n
            data(i) = conjg(data(i)) / real(n, 8)
        end do
    end subroutine ifft

    !---------------------------------------------------------------------------
    ! Real FFT - FFT of real-valued signal
    ! Returns N/2 + 1 complex values (positive frequencies only due to symmetry)
    !---------------------------------------------------------------------------
    subroutine rfft(real_data, complex_output, n, output_size)
        real(8), intent(in) :: real_data(:)
        complex(8), intent(out) :: complex_output(:)
        integer, intent(in) :: n
        integer, intent(out) :: output_size
        
        complex(8), allocatable :: temp(:)
        integer :: i
        
        ! Pad to power of 2 if necessary
        output_size = n / 2 + 1
        
        allocate(temp(n))
        
        ! Convert real to complex
        do i = 1, n
            temp(i) = cmplx(real_data(i), 0.0d0, 8)
        end do
        
        ! Perform FFT
        call fft(temp, n)
        
        ! Output only positive frequencies (Hermitian symmetry)
        do i = 1, output_size
            complex_output(i) = temp(i)
        end do
        
        deallocate(temp)
    end subroutine rfft

    !---------------------------------------------------------------------------
    ! Inverse Real FFT - reconstruct real signal from positive frequencies
    !---------------------------------------------------------------------------
    subroutine irfft(complex_input, real_output, input_size, n)
        complex(8), intent(in) :: complex_input(:)
        real(8), intent(out) :: real_output(:)
        integer, intent(in) :: input_size, n
        
        complex(8), allocatable :: temp(:)
        integer :: i
        
        allocate(temp(n))
        
        ! Copy positive frequencies
        do i = 1, input_size
            temp(i) = complex_input(i)
        end do
        
        ! Reconstruct negative frequencies (Hermitian symmetry)
        ! DC and Nyquist are purely real
        do i = input_size + 1, n
            temp(i) = conjg(temp(n - i + 2))
        end do
        
        ! Perform IFFT
        call ifft(temp, n)
        
        ! Extract real part
        do i = 1, n
            real_output(i) = real(temp(i), 8)
        end do
        
        deallocate(temp)
    end subroutine irfft

    !---------------------------------------------------------------------------
    ! Calculate frequency bins for FFT output
    !---------------------------------------------------------------------------
    subroutine fft_freq(freqs, n, sample_rate)
        real(8), intent(out) :: freqs(:)
        integer, intent(in) :: n
        real(8), intent(in) :: sample_rate
        
        integer :: i
        
        do i = 1, n
            freqs(i) = real(i - 1, 8) * sample_rate / real(n, 8)
        end do
    end subroutine fft_freq

    !---------------------------------------------------------------------------
    ! Compute power spectrum from FFT result
    !---------------------------------------------------------------------------
    subroutine power_spectrum(fft_data, power, n)
        complex(8), intent(in) :: fft_data(:)
        real(8), intent(out) :: power(:)
        integer, intent(in) :: n
        
        integer :: i
        
        do i = 1, n
            power(i) = real(fft_data(i) * conjg(fft_data(i)), 8)
        end do
    end subroutine power_spectrum

    !---------------------------------------------------------------------------
    ! Find next power of 2 >= n
    !---------------------------------------------------------------------------
    function next_power_of_two(n) result(p2)
        integer, intent(in) :: n
        integer :: p2
        
        p2 = 1
        do while (p2 < n)
            p2 = p2 * 2
        end do
    end function next_power_of_two

    !---------------------------------------------------------------------------
    ! Hanning window
    !---------------------------------------------------------------------------
    subroutine hanning_window(window, n)
        real(8), intent(out) :: window(:)
        integer, intent(in) :: n
        
        integer :: i
        
        do i = 1, n
            window(i) = 0.5d0 * (1.0d0 - cos(TWO_PI * real(i - 1, 8) / real(n - 1, 8)))
        end do
    end subroutine hanning_window

    !---------------------------------------------------------------------------
    ! Hamming window
    !---------------------------------------------------------------------------
    subroutine hamming_window(window, n)
        real(8), intent(out) :: window(:)
        integer, intent(in) :: n
        
        integer :: i
        real(8) :: alpha
        
        alpha = 0.54d0
        
        do i = 1, n
            window(i) = alpha - (1.0d0 - alpha) * cos(TWO_PI * real(i - 1, 8) / real(n - 1, 8))
        end do
    end subroutine hamming_window

    !---------------------------------------------------------------------------
    ! Blackman window
    !---------------------------------------------------------------------------
    subroutine blackman_window(window, n)
        real(8), intent(out) :: window(:)
        integer, intent(in) :: n
        
        integer :: i
        real(8) :: a0, a1, a2
        
        a0 = 0.42d0
        a1 = 0.5d0
        a2 = 0.08d0
        
        do i = 1, n
            window(i) = a0 - a1 * cos(TWO_PI * real(i - 1, 8) / real(n - 1, 8)) &
                              + a2 * cos(4.0d0 * PI * real(i - 1, 8) / real(n - 1, 8))
        end do
    end subroutine blackman_window

    !---------------------------------------------------------------------------
    ! Apply window function to signal
    !---------------------------------------------------------------------------
    subroutine apply_window(signal, window, output, n)
        real(8), intent(in) :: signal(:), window(:)
        real(8), intent(out) :: output(:)
        integer, intent(in) :: n
        
        integer :: i
        
        do i = 1, n
            output(i) = signal(i) * window(i)
        end do
    end subroutine apply_window

    !---------------------------------------------------------------------------
    ! FFT shift - reorder FFT output to center zero frequency
    !---------------------------------------------------------------------------
    subroutine fft_shift(data, n)
        complex(8), intent(inout) :: data(:)
        integer, intent(in) :: n
        
        integer :: half, i
        complex(8), allocatable :: temp(:)
        
        half = n / 2
        allocate(temp(half))
        
        ! Save first half
        do i = 1, half
            temp(i) = data(i)
        end do
        
        ! Move second half to beginning
        do i = 1, half
            data(i) = data(i + half)
        end do
        
        ! Move saved first half to end
        do i = 1, half
            data(i + half) = temp(i)
        end do
        
        deallocate(temp)
    end subroutine fft_shift

    !---------------------------------------------------------------------------
    ! Compute magnitude from complex FFT result
    !---------------------------------------------------------------------------
    subroutine magnitude(fft_data, mag, n)
        complex(8), intent(in) :: fft_data(:)
        real(8), intent(out) :: mag(:)
        integer, intent(in) :: n
        
        integer :: i
        
        do i = 1, n
            mag(i) = abs(fft_data(i))
        end do
    end subroutine magnitude

    !---------------------------------------------------------------------------
    ! Compute phase from complex FFT result
    !---------------------------------------------------------------------------
    subroutine phase(fft_data, ph, n)
        complex(8), intent(in) :: fft_data(:)
        real(8), intent(out) :: ph(:)
        integer, intent(in) :: n
        
        integer :: i
        
        do i = 1, n
            ph(i) = atan2(aimag(fft_data(i)), real(fft_data(i), 8))
        end do
    end subroutine phase

end module fft_utils