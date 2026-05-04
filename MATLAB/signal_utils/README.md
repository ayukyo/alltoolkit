# Signal Utils - MATLAB Signal Processing Utilities

A comprehensive signal processing toolkit for MATLAB with zero external dependencies.

## Features

### Signal Generation
- **Sine/Cosine waves** - `sine_wave`, `cosine_wave`
- **Square/Sawtooth waves** - `square_wave`, `sawtooth_wave`
- **Frequency sweep** - `chirp` (linear, quadratic, logarithmic)
- **Impulse/Step signals** - `impulse`, `step`
- **Ramp signal** - `ramp`

### Noise Generation
- **White noise** - Uniform distribution
- **Gaussian noise** - Normal distribution with configurable mean/std
- **Pink noise** - 1/f noise using Voss-McCartney algorithm

### Window Functions
- **Hanning** - `window_hanning`
- **Hamming** - `window_hamming`
- **Blackman** - `window_blackman`
- **Bartlett (Triangular)** - `window_bartlett`
- **Kaiser** - `window_kaiser` (configurable beta)
- **Flat Top** - `window_flattop`
- **Chebyshev** - `window_chebyshev` (configurable sidelobe attenuation)
- **Gaussian** - `window_gaussian`

### Spectral Analysis
- **FFT Spectrum** - `fft_spectrum` (single-sided magnitude spectrum)
- **Power Spectral Density** - `power_spectral_density` (Welch's method)
- **Spectrogram** - `spectrogram_calc`
- **Dominant Frequency** - `dominant_frequency`
- **Signal Energy/Power/RMS** - `signal_energy`, `signal_power`, `signal_rms`

### Filtering
- **Lowpass Filter** - `lowpass_filter` (Butterworth)
- **Highpass Filter** - `highpass_filter`
- **Bandpass Filter** - `bandpass_filter`
- **Bandstop Filter** - `bandstop_filter`
- **Moving Average** - `moving_average`
- **Gaussian Filter** - `gaussian_filter`
- **Median Filter** - `median_filter`
- **Savitzky-Golay** - `savitzky_golay`
- **Wiener Filter** - `wiener_filter`

### Convolution & Correlation
- **Convolution** - `convolve` (full, same, valid modes)
- **Cross-correlation** - `correlate`
- **Autocorrelation** - `autocorrelate`
- **Correlation Lags** - `correlation_lags`

### Signal Operations
- **Add/Multiply/Mix** - Signal combination
- **Normalize** - Max, RMS, Energy, Z-score normalization
- **Rescale** - Custom range scaling
- **Invert/Rectify** - Signal inversion and rectification
- **DC Removal** - `remove_dc`

### Signal Analysis
- **SNR Calculation** - `signal_to_noise_ratio`
- **THD** - `total_harmonic_distortion`
- **Crest Factor** - `crest_factor`
- **Center Frequency** - `center_frequency`
- **Bandwidth** - `bandwidth`
- **Zero Crossing Rate** - `zero_crossing_rate`
- **Statistics** - `signal_statistics`

### Decibel Operations
- **Linear to dB** - `to_decibel`, `power_to_decibel`
- **dB to Linear** - `from_decibel`, `decibel_to_power`

### Sampling Operations
- **Downsample** - `downsample`
- **Upsample** - `upsample`
- **Resample** - `resample_signal`

## Usage Examples

### Generate and Analyze a Signal
```matlab
% Generate a 50 Hz sine wave
fs = 1000;  % Sampling frequency
duration = 1;  % Duration in seconds
frequency = 50;  % Signal frequency
sig = mod.sine_wave(fs, duration, frequency);

% Compute FFT spectrum
[spectrum, freq] = mod.fft_spectrum(sig, fs);

% Find dominant frequency
dominant_freq = mod.dominant_frequency(sig, fs);
fprintf('Dominant frequency: %.2f Hz\n', dominant_freq);
```

### Add Noise and Filter
```matlab
% Generate signal with noise
clean_sig = mod.sine_wave(1000, 1, 100);
noise = mod.gaussian_noise(1000, 0, 0.2);
noisy_sig = mod.add_signals(clean_sig, noise);

% Apply lowpass filter
[b, a] = mod.lowpass_filter(4, 150, 1000);
filtered_sig = filter(b, a, noisy_sig);

% Calculate SNR improvement
original_snr = mod.signal_to_noise_ratio(clean_sig, noise);
filtered_noise = filtered_sig - clean_sig;
new_snr = mod.signal_to_noise_ratio(clean_sig, filtered_noise);
fprintf('SNR improved from %.2f dB to %.2f dB\n', original_snr, new_snr);
```

### Apply Window and Spectral Analysis
```matlab
% Generate signal
sig = mod.sine_wave(1000, 1, 50);

% Apply Hanning window
window = mod.window_hanning(1000);
windowed_sig = sig .* window;

% Compute power spectral density
[psd, freq] = mod.power_spectral_density(windowed_sig, 1000, 512);
```

### Signal Statistics
```matlab
% Generate complex signal
sig1 = mod.sine_wave(1000, 1, 50);
sig2 = mod.sine_wave(1000, 1, 120);
sig = mod.mix_signals(sig1, sig2, 0.5);
sig = mod.add_signals(sig, mod.gaussian_noise(1000));

% Get statistics
stats = mod.signal_statistics(sig);
fprintf('RMS: %.4f, Crest Factor: %.4f\n', stats.rms, stats.crest_factor);
fprintf('Energy: %.4f, Power: %.4f\n', stats.energy, stats.power);
```

## Testing

Run the test suite:
```matlab
signal_utils_test
```

## Requirements

- MATLAB R2016b or later (for classdef with static methods)
- No external dependencies (uses only built-in MATLAB functions)

## License

MIT License - Part of AllToolkit Project