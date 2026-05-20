!===============================================================================
! Test Suite for FFT Utils
!===============================================================================
! Comprehensive tests for FFT, IFFT, windows, and spectral analysis
!===============================================================================

program test_fft_utils
    use fft_utils
    implicit none
    
    integer :: test_count, pass_count
    
    test_count = 0
    pass_count = 0
    
    print *, "=========================================="
    print *, "FFT Utils Test Suite"
    print *, "=========================================="
    print *, ""
    
    ! Run all tests
    call test_next_power_of_two(test_count, pass_count)
    call test_fft_roundtrip(test_count, pass_count)
    call test_fft_dc_component(test_count, pass_count)
    call test_fft_sine_wave(test_count, pass_count)
    call test_ifft(test_count, pass_count)
    call test_hanning_window(test_count, pass_count)
    call test_hamming_window(test_count, pass_count)
    call test_blackman_window(test_count, pass_count)
    call test_power_spectrum(test_count, pass_count)
    call test_fft_freq(test_count, pass_count)
    call test_magnitude_phase(test_count, pass_count)
    call test_fft_shift(test_count, pass_count)
    call test_rfft(test_count, pass_count)
    
    ! Summary
    print *, ""
    print *, "=========================================="
    print *, "Test Summary"
    print *, "=========================================="
    print '(A, I0, A, I0, A)', " Passed: ", pass_count, " / ", test_count, " tests"
    
    if (pass_count == test_count) then
        print *, "All tests passed!"
    else
        print *, "Some tests failed!"
    end if
    
end program test_fft_utils

!-------------------------------------------------------------------------------
! Test helper: compare two real values with tolerance
!-------------------------------------------------------------------------------
logical function approx_equal(a, b, tol)
    real(8), intent(in) :: a, b, tol
    
    approx_equal = abs(a - b) < tol
end function approx_equal

!-------------------------------------------------------------------------------
! Test: next_power_of_two
!-------------------------------------------------------------------------------
subroutine test_next_power_of_two(test_count, pass_count)
    use fft_utils
    implicit none
    integer, intent(inout) :: test_count, pass_count
    
    logical :: approx_equal
    real(8), parameter :: tol = 1.0d-10
    
    test_count = test_count + 1
    print '(A)', "Test: next_power_of_two..."
    
    if (next_power_of_two(1) == 1 .and. &
        next_power_of_two(5) == 8 .and. &
        next_power_of_two(16) == 16 .and. &
        next_power_of_two(17) == 32 .and. &
        next_power_of_two(100) == 128) then
        pass_count = pass_count + 1
        print '(A)', "  PASS"
    else
        print '(A)', "  FAIL"
    end if
end subroutine test_next_power_of_two

!-------------------------------------------------------------------------------
! Test: FFT roundtrip (FFT followed by IFFT should recover original)
!-------------------------------------------------------------------------------
subroutine test_fft_roundtrip(test_count, pass_count)
    use fft_utils
    implicit none
    integer, intent(inout) :: test_count, pass_count
    
    integer, parameter :: n = 8
    complex(8) :: data(n), original(n)
    integer :: i
    real(8) :: error
    logical :: approx_equal
    real(8), parameter :: tol = 1.0d-10
    
    test_count = test_count + 1
    print '(A)', "Test: FFT roundtrip..."
    
    ! Create test signal
    do i = 1, n
        original(i) = cmplx(real(i, 8), real(n - i + 1, 8), 8)
        data(i) = original(i)
    end do
    
    ! FFT then IFFT
    call fft(data, n)
    call ifft(data, n)
    
    ! Check error
    error = 0.0d0
    do i = 1, n
        error = error + abs(data(i) - original(i))
    end do
    
    if (error < tol) then
        pass_count = pass_count + 1
        print '(A)', "  PASS"
    else
        print '(A, E12.4)', "  FAIL, error: ", error
    end if
end subroutine test_fft_roundtrip

!-------------------------------------------------------------------------------
! Test: FFT of DC component
!-------------------------------------------------------------------------------
subroutine test_fft_dc_component(test_count, pass_count)
    use fft_utils
    implicit none
    integer, intent(inout) :: test_count, pass_count
    
    integer, parameter :: n = 8
    complex(8) :: data(n)
    real(8) :: dc_value
    integer :: i
    logical :: approx_equal
    real(8), parameter :: tol = 1.0d-10
    
    test_count = test_count + 1
    print '(A)', "Test: FFT DC component..."
    
    dc_value = 5.0d0
    
    ! All same value = DC signal
    do i = 1, n
        data(i) = cmplx(dc_value, 0.0d0, 8)
    end do
    
    call fft(data, n)
    
    ! DC component should be n * dc_value, others should be ~0
    if (approx_equal(real(data(1)), n * dc_value, tol) .and. &
        approx_equal(aimag(data(1)), 0.0d0, tol)) then
        pass_count = pass_count + 1
        print '(A)', "  PASS"
    else
        print '(A)', "  FAIL"
    end if
end subroutine test_fft_dc_component

!-------------------------------------------------------------------------------
! Test: FFT of sine wave
!-------------------------------------------------------------------------------
subroutine test_fft_sine_wave(test_count, pass_count)
    use fft_utils
    implicit none
    integer, intent(inout) :: test_count, pass_count
    
    integer, parameter :: n = 16
    complex(8) :: data(n)
    real(8) :: freq, sample_rate, max_mag, mag
    integer :: i, max_idx
    logical :: approx_equal
    real(8), parameter :: tol = 1.0d-10
    
    test_count = test_count + 1
    print '(A)', "Test: FFT sine wave..."
    
    freq = 2.0d0  ! 2 cycles in the window
    sample_rate = real(n, 8)
    
    ! Generate sine wave
    do i = 1, n
        data(i) = cmplx(sin(TWO_PI * freq * real(i - 1, 8) / sample_rate), 0.0d0, 8)
    end do
    
    call fft(data, n)
    
    ! Find peak frequency bin
    max_mag = 0.0d0
    max_idx = 1
    do i = 1, n/2 + 1
        mag = abs(data(i))
        if (mag > max_mag) then
            max_mag = mag
            max_idx = i
        end if
    end do
    
    ! Peak should be at bin 3 (index = freq + 1)
    if (max_idx == int(freq) + 1) then
        pass_count = pass_count + 1
        print '(A)', "  PASS"
    else
        print '(A, I0, A, I0)', "  FAIL, expected bin ", int(freq) + 1, ", got ", max_idx
    end if
end subroutine test_fft_sine_wave

!-------------------------------------------------------------------------------
! Test: IFFT correctness
!-------------------------------------------------------------------------------
subroutine test_ifft(test_count, pass_count)
    use fft_utils
    implicit none
    integer, intent(inout) :: test_count, pass_count
    
    integer, parameter :: n = 8
    complex(8) :: data(n), recovered(n)
    integer :: i
    real(8) :: error
    logical :: approx_equal
    real(8), parameter :: tol = 1.0d-10
    
    test_count = test_count + 1
    print '(A)', "Test: IFFT..."
    
    ! Create impulse in frequency domain
    data = cmplx(0.0d0, 0.0d0, 8)
    data(1) = cmplx(1.0d0, 0.0d0, 8)  ! DC
    
    call ifft(data, n)
    
    ! Should recover constant signal
    error = 0.0d0
    do i = 1, n
        error = error + abs(data(i) - cmplx(1.0d0/real(n, 8), 0.0d0, 8))
    end do
    
    if (error < tol) then
        pass_count = pass_count + 1
        print '(A)', "  PASS"
    else
        print '(A, E12.4)', "  FAIL, error: ", error
    end if
end subroutine test_ifft

!-------------------------------------------------------------------------------
! Test: Hanning window
!-------------------------------------------------------------------------------
subroutine test_hanning_window(test_count, pass_count)
    use fft_utils
    implicit none
    integer, intent(inout) :: test_count, pass_count
    
    integer, parameter :: n = 17  ! Odd size for exact peak at center
    real(8) :: window(n)
    integer :: i
    logical :: approx_equal
    real(8), parameter :: tol = 1.0d-6
    
    test_count = test_count + 1
    print '(A)', "Test: Hanning window..."
    
    call hanning_window(window, n)
    
    ! For odd n: w[1]=0, w[n]=0, w[(n+1)/2]=1 exactly
    if (approx_equal(window(1), 0.0d0, tol) .and. &
        approx_equal(window(n), 0.0d0, tol) .and. &
        approx_equal(window((n+1)/2), 1.0d0, tol)) then
        pass_count = pass_count + 1
        print '(A)', "  PASS"
    else
        print '(A)', "  FAIL"
        print '(A, F10.6)', "  window(1) = ", window(1)
        print '(A, F10.6)', "  window(n) = ", window(n)
        print '(A, F10.6)', "  window(mid) = ", window((n+1)/2)
    end if
end subroutine test_hanning_window

!-------------------------------------------------------------------------------
! Test: Hamming window
!-------------------------------------------------------------------------------
subroutine test_hamming_window(test_count, pass_count)
    use fft_utils
    implicit none
    integer, intent(inout) :: test_count, pass_count
    
    integer, parameter :: n = 17  ! Odd size
    real(8) :: window(n)
    real(8) :: sum_val
    logical :: approx_equal
    real(8), parameter :: tol = 1.0d-6
    
    test_count = test_count + 1
    print '(A)', "Test: Hamming window..."
    
    call hamming_window(window, n)
    
    ! Hamming: peak at center, endpoints ~0.08
    ! w[(n+1)/2] = alpha - (1-alpha)*cos(pi) = 0.54 + 0.46 = 1.0
    sum_val = sum(window)
    if (approx_equal(window((n+1)/2), 1.0d0, tol) .and. &
        window(1) > 0.07d0 .and. window(1) < 0.1d0 .and. &
        sum_val > 0.0d0) then
        pass_count = pass_count + 1
        print '(A)', "  PASS"
    else
        print '(A)', "  FAIL"
        print '(A, F10.6)', "  window(1) = ", window(1)
        print '(A, F10.6)', "  window(mid) = ", window((n+1)/2)
    end if
end subroutine test_hamming_window

!-------------------------------------------------------------------------------
! Test: Blackman window
!-------------------------------------------------------------------------------
subroutine test_blackman_window(test_count, pass_count)
    use fft_utils
    implicit none
    integer, intent(inout) :: test_count, pass_count
    
    integer, parameter :: n = 17  ! Odd size
    real(8) :: window(n)
    real(8) :: sum_val
    logical :: approx_equal
    real(8), parameter :: tol = 1.0d-6
    
    test_count = test_count + 1
    print '(A)', "Test: Blackman window..."
    
    call blackman_window(window, n)
    
    ! Blackman: endpoints near 0, peak at center = 1.0 for odd n
    sum_val = sum(window)
    if (approx_equal(abs(window(1)), 0.0d0, tol) .and. &
        approx_equal(abs(window(n)), 0.0d0, tol) .and. &
        approx_equal(window((n+1)/2), 1.0d0, tol) .and. &
        sum_val > 0.0d0) then
        pass_count = pass_count + 1
        print '(A)', "  PASS"
    else
        print '(A)', "  FAIL"
        print '(A, F10.6)', "  window(1) = ", window(1)
        print '(A, F10.6)', "  window(n) = ", window(n)
        print '(A, F10.6)', "  window(mid) = ", window((n+1)/2)
    end if
end subroutine test_blackman_window

!-------------------------------------------------------------------------------
! Test: Power spectrum
!-------------------------------------------------------------------------------
subroutine test_power_spectrum(test_count, pass_count)
    use fft_utils
    implicit none
    integer, intent(inout) :: test_count, pass_count
    
    integer, parameter :: n = 8
    complex(8) :: fft_data(n)
    real(8) :: power(n)
    integer :: i
    logical :: approx_equal
    real(8), parameter :: tol = 1.0d-8
    
    test_count = test_count + 1
    print '(A)', "Test: Power spectrum..."
    
    ! Create simple FFT output
    do i = 1, n
        fft_data(i) = cmplx(real(i, 8), real(i, 8), 8)
    end do
    
    call power_spectrum(fft_data, power, n)
    
    ! Power = |z|^2 = a^2 + b^2 for z = a + bi
    ! For z = i + i*j, power = i^2 + i^2 = 2*i^2
    if (approx_equal(power(1), 2.0d0, tol) .and. &
        approx_equal(power(4), 32.0d0, tol)) then
        pass_count = pass_count + 1
        print '(A)', "  PASS"
    else
        print '(A)', "  FAIL"
    end if
end subroutine test_power_spectrum

!-------------------------------------------------------------------------------
! Test: FFT frequency bins
!-------------------------------------------------------------------------------
subroutine test_fft_freq(test_count, pass_count)
    use fft_utils
    implicit none
    integer, intent(inout) :: test_count, pass_count
    
    integer, parameter :: n = 8
    real(8) :: freqs(n)
    real(8) :: sample_rate
    logical :: approx_equal
    real(8), parameter :: tol = 1.0d-10
    
    test_count = test_count + 1
    print '(A)', "Test: FFT frequency bins..."
    
    sample_rate = 1000.0d0  ! 1 kHz
    
    call fft_freq(freqs, n, sample_rate)
    
    ! Check frequency resolution
    if (approx_equal(freqs(1), 0.0d0, tol) .and. &
        approx_equal(freqs(2), sample_rate / n, tol) .and. &
        approx_equal(freqs(n), sample_rate * (n-1) / n, tol)) then
        pass_count = pass_count + 1
        print '(A)', "  PASS"
    else
        print '(A)', "  FAIL"
    end if
end subroutine test_fft_freq

!-------------------------------------------------------------------------------
! Test: Magnitude and phase
!-------------------------------------------------------------------------------
subroutine test_magnitude_phase(test_count, pass_count)
    use fft_utils
    implicit none
    integer, intent(inout) :: test_count, pass_count
    
    integer, parameter :: n = 4
    complex(8) :: data(n)
    real(8) :: mag(n), ph(n)
    logical :: approx_equal
    real(8), parameter :: tol = 1.0d-10
    
    test_count = test_count + 1
    print '(A)', "Test: Magnitude and phase..."
    
    ! Test data with known magnitude and phase
    data(1) = cmplx(1.0d0, 0.0d0, 8)   ! mag=1, phase=0
    data(2) = cmplx(0.0d0, 1.0d0, 8)   ! mag=1, phase=pi/2
    data(3) = cmplx(1.0d0, 1.0d0, 8)   ! mag=sqrt(2), phase=pi/4
    data(4) = cmplx(-1.0d0, 0.0d0, 8)  ! mag=1, phase=pi
    
    call magnitude(data, mag, n)
    call phase(data, ph, n)
    
    if (approx_equal(mag(1), 1.0d0, tol) .and. &
        approx_equal(mag(3), sqrt(2.0d0), tol) .and. &
        approx_equal(ph(1), 0.0d0, tol) .and. &
        approx_equal(ph(2), PI/2.0d0, tol) .and. &
        approx_equal(ph(4), PI, tol)) then
        pass_count = pass_count + 1
        print '(A)', "  PASS"
    else
        print '(A)', "  FAIL"
    end if
end subroutine test_magnitude_phase

!-------------------------------------------------------------------------------
! Test: FFT shift
!-------------------------------------------------------------------------------
subroutine test_fft_shift(test_count, pass_count)
    use fft_utils
    implicit none
    integer, intent(inout) :: test_count, pass_count
    
    integer, parameter :: n = 8
    complex(8) :: data(n)
    integer :: i
    logical :: approx_equal
    real(8), parameter :: tol = 1.0d-10
    
    test_count = test_count + 1
    print '(A)', "Test: FFT shift..."
    
    ! Create sequential data
    do i = 1, n
        data(i) = cmplx(real(i, 8), 0.0d0, 8)
    end do
    
    call fft_shift(data, n)
    
    ! After shift, first element should be what was in the middle
    if (approx_equal(real(data(1)), real(n/2 + 1, 8), tol)) then
        pass_count = pass_count + 1
        print '(A)', "  PASS"
    else
        print '(A)', "  FAIL"
    end if
end subroutine test_fft_shift

!-------------------------------------------------------------------------------
! Test: Real FFT
!-------------------------------------------------------------------------------
subroutine test_rfft(test_count, pass_count)
    use fft_utils
    implicit none
    integer, intent(inout) :: test_count, pass_count
    
    integer, parameter :: n = 8
    real(8) :: signal(n)
    complex(8) :: spectrum(n/2 + 1)
    real(8) :: recovered(n)
    integer :: i, output_size
    real(8) :: error
    logical :: approx_equal
    real(8), parameter :: tol = 1.0d-8
    
    test_count = test_count + 1
    print '(A)', "Test: Real FFT (rfft)..."
    
    ! Create real signal
    do i = 1, n
        signal(i) = sin(TWO_PI * 2.0d0 * real(i - 1, 8) / real(n, 8))
    end do
    
    ! Forward RFFT
    call rfft(signal, spectrum, n, output_size)
    
    ! Inverse RFFT
    call irfft(spectrum, recovered, output_size, n)
    
    ! Check reconstruction
    error = 0.0d0
    do i = 1, n
        error = error + abs(recovered(i) - signal(i))
    end do
    
    if (error < tol .and. output_size == n/2 + 1) then
        pass_count = pass_count + 1
        print '(A)', "  PASS"
    else
        print '(A, E12.4)', "  FAIL, error: ", error
    end if
end subroutine test_rfft