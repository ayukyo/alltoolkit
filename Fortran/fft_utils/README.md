# FFT Utils - Fast Fourier Transform for Fortran

A pure Fortran implementation of FFT algorithms with zero external dependencies.

## Features

- **Cooley-Tukey radix-2 DIT FFT** - Efficient in-place FFT for power-of-2 sizes
- **Inverse FFT** - Perfect roundtrip reconstruction
- **Real FFT (RFFT)** - Optimized FFT for real-valued signals
- **Power Spectrum** - Compute spectral density
- **Frequency Bins** - Calculate frequency axis for plots
- **Window Functions** - Hanning, Hamming, Blackman windows
- **FFT Shift** - Center zero frequency for display
- **Magnitude & Phase** - Extract amplitude and phase from complex spectrum

## Quick Start

```fortran
program demo
    use fft_utils
    implicit none
    
    integer, parameter :: n = 64
    complex(8) :: data(n)
    real(8) :: freqs(n), mags(n), sample_rate
    integer :: i
    
    ! Generate a 5 Hz sine wave at 64 Hz sample rate
    sample_rate = 64.0d0
    do i = 1, n
        data(i) = cmplx(sin(TWO_PI * 5.0d0 * real(i - 1, 8) / sample_rate), 0.0d0, 8)
    end do
    
    ! Compute FFT
    call fft(data, n)
    
    ! Get frequency bins and magnitude
    call fft_freq(freqs, n, sample_rate)
    call magnitude(data, mags, n)
    
    ! Find peak frequency
    print *, "Peak frequency:", freqs(maxloc(mags(1:n/2+1), 1))
end program
```

## API Reference

### Core Functions

| Function | Description |
|----------|-------------|
| `fft(data, n)` | Forward FFT (in-place) |
| `ifft(data, n)` | Inverse FFT (in-place) |
| `rfft(real_data, complex_output, n, output_size)` | Real FFT |
| `irfft(complex_input, real_output, input_size, n)` | Inverse Real FFT |

### Analysis Functions

| Function | Description |
|----------|-------------|
| `fft_freq(freqs, n, sample_rate)` | Compute frequency bins |
| `power_spectrum(fft_data, power, n)` | Compute power spectrum |
| `magnitude(fft_data, mag, n)` | Compute magnitude |
| `phase(fft_data, ph, n)` | Compute phase |
| `fft_shift(data, n)` | Shift zero frequency to center |

### Utility Functions

| Function | Description |
|----------|-------------|
| `next_power_of_two(n)` | Find smallest power of 2 >= n |
| `hanning_window(window, n)` | Generate Hanning window |
| `hamming_window(window, n)` | Generate Hamming window |
| `blackman_window(window, n)` | Generate Blackman window |
| `apply_window(signal, window, output, n)` | Apply window to signal |

### Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `PI` | 3.14159... | π |
| `TWO_PI` | 2π | 2π |

## Building

### Using gfortran

```bash
# Compile the module
gfortran -c fft_utils.f90

# Compile test program
gfortran -c test_fft_utils.f90
gfortran fft_utils.o test_fft_utils.o -o test_fft

# Run tests
./test_fft
```

### Using Intel Fortran (ifort)

```bash
ifort -c fft_utils.f90
ifort fft_utils.o test_fft_utils.o -o test_fft
./test_fft
```

## Examples

See `examples/example_fft.f90` for complete examples including:
- Basic FFT/IFFT roundtrip
- Sine wave frequency analysis
- Window function comparison
- Power spectrum computation
- Real signal processing

## Algorithm Notes

### Cooley-Tukey FFT
Uses the classic radix-2 Decimation-In-Time (DIT) algorithm with:
- In-place computation (O(1) extra space)
- O(n log n) time complexity
- Bit-reversal permutation

### Real FFT Optimization
For real-valued signals, the FFT output is Hermitian symmetric:
- F(k) = conj(F(N-k))
- Only N/2 + 1 complex values need storage
- Reduces computation and memory by ~50%

## License

MIT License - Part of AllToolkit