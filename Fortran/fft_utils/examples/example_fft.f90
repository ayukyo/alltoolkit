!===============================================================================
! Example: FFT Analysis of Signals
!===============================================================================
! Demonstrates:
!   - Basic FFT and IFFT
!   - Real FFT for signal processing
!   - Window functions
!   - Power spectrum computation
!   - Frequency analysis
!===============================================================================

program example_fft
    use fft_utils
    implicit none
    
    print *, "=========================================="
    print *, "FFT Utils - Examples"
    print *, "=========================================="
    print *, ""
    
    call example_basic_fft()
    call example_sine_analysis()
    call example_window_functions()
    call example_power_spectrum()
    call example_real_signal()
    
    print *, ""
    print *, "All examples completed!"

contains

    !---------------------------------------------------------------------------
    ! Example 1: Basic FFT and IFFT
    !---------------------------------------------------------------------------
    subroutine example_basic_fft()
        integer, parameter :: n = 8
        complex(8) :: data(n)
        integer :: i
        real(8) :: error
        
        print *, "----------------------------------------"
        print *, "Example 1: Basic FFT and IFFT"
        print *, "----------------------------------------"
        print *, ""
        
        ! Create a simple signal: impulse
        print *, "Original signal (impulse at t=0):"
        data = cmplx(0.0d0, 0.0d0, 8)
        data(1) = cmplx(1.0d0, 0.0d0, 8)
        
        do i = 1, n
            print '(A, I0, A, F8.4, A, F8.4)', "  data(", i, ") = ", &
                real(data(i)), " + ", aimag(data(i)), "j"
        end do
        print *, ""
        
        ! Forward FFT
        call fft(data, n)
        
        print *, "After FFT (constant magnitude across frequencies):"
        do i = 1, n
            print '(A, I0, A, F8.4, A, F8.4)', "  bin ", i-1, ": ", &
                real(data(i)), " + ", aimag(data(i)), "j"
            print '(A, F8.4)', "    magnitude = ", abs(data(i))
        end do
        print *, ""
        
        ! Inverse FFT
        call ifft(data, n)
        
        print *, "After IFFT (recovered impulse):"
        error = 0.0d0
        do i = 1, n
            error = error + abs(data(i))
            print '(A, I0, A, F10.6, A, F10.6)', "  data(", i, ") = ", &
                real(data(i)), " + ", aimag(data(i)), "j"
        end do
        
        print *, ""
        print '(A, F12.8)', "Reconstruction error: ", abs(error - 1.0d0)
        print *, ""
    end subroutine example_basic_fft

    !---------------------------------------------------------------------------
    ! Example 2: Analyzing a sine wave
    !---------------------------------------------------------------------------
    subroutine example_sine_analysis()
        integer, parameter :: n = 64
        complex(8) :: data(n)
        real(8) :: freqs(n), mags(n)
        real(8) :: signal_freq, sample_rate
        integer :: i, peak_bin
        
        print *, "----------------------------------------"
        print *, "Example 2: Sine Wave Analysis"
        print *, "----------------------------------------"
        print *, ""
        
        signal_freq = 5.0d0    ! 5 Hz
        sample_rate = 64.0d0  ! 64 samples/sec
        
        print '(A, F6.1, A)', "Signal frequency: ", signal_freq, " Hz"
        print '(A, F6.1, A)', "Sample rate: ", sample_rate, " Hz"
        print *, ""
        
        ! Generate sine wave
        do i = 1, n
            data(i) = cmplx(sin(TWO_PI * signal_freq * real(i - 1, 8) / sample_rate), 0.0d0, 8)
        end do
        
        ! FFT
        call fft(data, n)
        
        ! Frequency bins and magnitude
        call fft_freq(freqs, n, sample_rate)
        call magnitude(data, mags, n)
        
        ! Find peak
        peak_bin = 1
        do i = 2, n/2 + 1
            if (mags(i) > mags(peak_bin)) then
                peak_bin = i
            end if
        end do
        
        print *, "FFT Magnitude spectrum (positive frequencies):"
        print '(A)', "  Bin   Frequency(Hz)   Magnitude"
        do i = 1, n/2 + 1
            if (mags(i) > 0.1d0) then  ! Only show significant bins
                print '(I5, F12.1, F14.2)', i-1, freqs(i), mags(i)
            end if
        end do
        print *, ""
        
        print '(A, I0, A, F6.1, A)', "Peak detected at bin ", peak_bin-1, " (", freqs(peak_bin), " Hz)"
        print *, ""
    end subroutine example_sine_analysis

    !---------------------------------------------------------------------------
    ! Example 3: Window functions
    !---------------------------------------------------------------------------
    subroutine example_window_functions()
        integer, parameter :: n = 16
        real(8) :: hann(n), hamm(n), black(n)
        integer :: i
        
        print *, "----------------------------------------"
        print *, "Example 3: Window Functions"
        print *, "----------------------------------------"
        print *, ""
        
        call hanning_window(hann, n)
        call hamming_window(hamm, n)
        call blackman_window(black, n)
        
        print '(A)', "Comparison of window functions (n=16):"
        print '(A)', "  i    Hanning   Hamming   Blackman"
        print '(A)', "  -    -------   -------   --------"
        do i = 1, n
            print '(I3, F10.4, F10.4, F10.4)', i, hann(i), hamm(i), black(i)
        end do
        print *, ""
        
        print *, "Window characteristics:"
        print '(A)', "  Hanning: Good frequency resolution, moderate sidelobe suppression"
        print '(A)', "  Hamming: Better sidelobe suppression than Hanning"
        print '(A)', "  Blackman: Excellent sidelobe suppression, wider main lobe"
        print *, ""
    end subroutine example_window_functions

    !---------------------------------------------------------------------------
    ! Example 4: Power spectrum
    !---------------------------------------------------------------------------
    subroutine example_power_spectrum()
        integer, parameter :: n = 128
        complex(8) :: data(n)
        real(8) :: power(n), freqs(n)
        real(8) :: sample_rate, f1, f2
        integer :: i
        
        print *, "----------------------------------------"
        print *, "Example 4: Power Spectrum"
        print *, "----------------------------------------"
        print *, ""
        
        sample_rate = 128.0d0
        f1 = 10.0d0  ! 10 Hz component
        f2 = 25.0d0  ! 25 Hz component
        
        print '(A, F6.1, A, F6.1, A)', "Signal with two frequencies: ", f1, " Hz and ", f2, " Hz"
        print *, ""
        
        ! Generate composite signal
        do i = 1, n
            data(i) = cmplx( &
                sin(TWO_PI * f1 * real(i - 1, 8) / sample_rate) + &
                0.5d0 * sin(TWO_PI * f2 * real(i - 1, 8) / sample_rate), &
                0.0d0, 8)
        end do
        
        ! Apply window to reduce spectral leakage
        block
            real(8) :: window(n), windowed(n)
            call hanning_window(window, n)
            call apply_window(real(real(data), 8), window, windowed, n)
            do i = 1, n
                data(i) = cmplx(windowed(i), 0.0d0, 8)
            end do
        end block
        
        ! FFT and power spectrum
        call fft(data, n)
        call power_spectrum(data, power, n)
        call fft_freq(freqs, n, sample_rate)
        
        ! Normalize power
        power = power / real(n, 8)**2
        
        print *, "Power spectrum (showing significant peaks):"
        print '(A)', "  Freq(Hz)    Power"
        print '(A)', "  --------    -----"
        do i = 1, n/2 + 1
            if (power(i) > 0.001d0) then
                print '(F10.1, F10.6)', freqs(i), power(i)
            end if
        end do
        print *, ""
    end subroutine example_power_spectrum

    !---------------------------------------------------------------------------
    ! Example 5: Real signal processing
    !---------------------------------------------------------------------------
    subroutine example_real_signal()
        integer, parameter :: n = 32
        real(8) :: signal(n), recovered(n), window(n)
        complex(8) :: spectrum(n/2 + 1)
        integer :: i, output_size
        
        print *, "----------------------------------------"
        print *, "Example 5: Real Signal Processing"
        print *, "----------------------------------------"
        print *, ""
        
        ! Generate a real signal
        print *, "Generating real signal (combination of frequencies)..."
        do i = 1, n
            signal(i) = 2.0d0 * sin(TWO_PI * 3.0d0 * real(i - 1, 8) / real(n, 8)) + &
                        1.0d0 * cos(TWO_PI * 7.0d0 * real(i - 1, 8) / real(n, 8))
        end do
        
        ! Apply window
        call hanning_window(window, n)
        call apply_window(signal, window, signal, n)
        
        ! Real FFT (only positive frequencies)
        call rfft(signal, spectrum, n, output_size)
        
        print '(A, I0)', "RFFT output size: ", output_size
        print *, ""
        
        print *, "Positive frequency spectrum:"
        print '(A)', "  Bin   Real        Imag       Magnitude"
        do i = 1, output_size
            print '(I5, F10.4, F10.4, F12.4)', i-1, real(spectrum(i)), aimag(spectrum(i)), abs(spectrum(i))
        end do
        print *, ""
        
        ! Inverse RFFT
        call irfft(spectrum, recovered, output_size, n)
        
        print *, "Signal successfully processed!"
        print '(A)', "RFFT provides efficient storage for real signals (N/2+1 complex values instead of N)"
        print *, ""
    end subroutine example_real_signal

end program example_fft