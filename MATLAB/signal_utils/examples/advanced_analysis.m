% ADVANCED_ANALYSIS - Advanced signal processing examples
% Demonstrates spectral analysis, filtering, and signal analysis techniques

fprintf('=== Signal Utils Advanced Examples ===\n\n');

%% 1. Frequency Analysis of Composite Signals
fprintf('1. Frequency Analysis\n');
fprintf('--------------------\n');

fs = 1000;
duration = 2;

% Create a complex signal with multiple frequencies
sig_50 = mod.sine_wave(fs, duration, 50, 1, 0);
sig_100 = mod.sine_wave(fs, duration, 100, 0.5, pi/4);
sig_200 = mod.sine_wave(fs, duration, 200, 0.3, pi/2);
noise = mod.gaussian_noise(fs * duration, 0, 0.1);

complex_sig = mod.add_signals(sig_50, sig_100);
complex_sig = mod.add_signals(complex_sig, sig_200);
complex_sig = mod.add_signals(complex_sig, noise);

fprintf('  Created composite signal:\n');
fprintf('    50 Hz (amplitude=1.0)\n');
fprintf('    100 Hz (amplitude=0.5, phase=pi/4)\n');
fprintf('    200 Hz (amplitude=0.3, phase=pi/2)\n');
fprintf('    Gaussian noise (std=0.1)\n');

% Spectral analysis
[spectrum, freq] = mod.fft_spectrum(complex_sig, fs);

% Find peaks
peaks = [];
for i = 2:length(spectrum)-1
    if spectrum(i) > spectrum(i-1) && spectrum(i) > spectrum(i+1) && spectrum(i) > 0.05
        peaks = [peaks; freq(i), spectrum(i)];
    end
end

fprintf('  Detected frequency peaks:\n');
for i = 1:size(peaks, 1)
    fprintf('    %.1f Hz (magnitude=%.4f)\n', peaks(i, 1), peaks(i, 2));
end

% Power spectral density
[psd, psd_freq] = mod.power_spectral_density(complex_sig, fs, 512);
fprintf('  PSD computed with 512-point FFT\n');

fprintf('\n');

%% 2. Signal Filtering Pipeline
fprintf('2. Signal Filtering Pipeline\n');
fprintf('----------------------------\n');

% Create noisy test signal
test_sig = mod.sine_wave(fs, 1, 50);
test_noise = mod.gaussian_noise(fs, 0, 0.5);
test_noisy = mod.add_signals(test_sig, test_noise);

original_snr = mod.signal_to_noise_ratio(test_sig, test_noise);
fprintf('  Original signal: 50 Hz sine wave with Gaussian noise\n');
fprintf('  Initial SNR: %.2f dB\n', original_snr);

% Lowpass filter (keep frequencies below 100 Hz)
[b_lp, a_lp] = mod.lowpass_filter(4, 100, fs);
filtered_lp = filter(b_lp, a_lp, test_noisy);
noise_lp = filtered_lp - test_sig;
snr_lp = mod.signal_to_noise_ratio(test_sig, noise_lp);
fprintf('  After lowpass filter (cutoff=100 Hz): SNR = %.2f dB\n', snr_lp);

% Bandpass filter (keep 40-60 Hz)
[b_bp, a_bp] = mod.bandpass_filter(4, 40, 60, fs);
filtered_bp = filter(b_bp, a_bp, test_noisy);
noise_bp = filtered_bp - test_sig;
snr_bp = mod.signal_to_noise_ratio(test_sig, noise_bp);
fprintf('  After bandpass filter (40-60 Hz): SNR = %.2f dB\n', snr_bp);

% Moving average smoothing
smoothed = mod.moving_average(filtered_bp, 5);
noise_smoothed = smoothed - test_sig;
snr_smoothed = mod.signal_to_noise_ratio(test_sig, noise_smoothed);
fprintf('  After moving average (window=5): SNR = %.2f dB\n', snr_smoothed);

fprintf('\n');

%% 3. Noise Analysis
fprintf('3. Noise Analysis\n');
fprintf('-----------------\n');

% Generate different noise types and analyze
n_samples = 10000;

white = mod.white_noise(n_samples);
gaussian = mod.gaussian_noise(n_samples, 0, 1);
pink = mod.pink_noise(n_samples);

fprintf('  White noise statistics:\n');
fprintf('    Mean: %.4f, Std: %.4f\n', mean(white), std(white));
fprintf('    Range: [%.2f, %.2f]\n', min(white), max(white));

fprintf('  Gaussian noise statistics:\n');
fprintf('    Mean: %.4f, Std: %.4f\n', mean(gaussian), std(gaussian));
fprintf('    Theoretical: mean=0, std=1\n');

fprintf('  Pink noise statistics:\n');
fprintf('    Mean: %.4f, Std: %.4f\n', mean(pink), std(pink));
fprintf('    (1/f characteristic)\n');

fprintf('\n');

%% 4. Window Effects on Spectral Leakage
fprintf('4. Window Effects\n');
fprintf('-----------------\n');

% Generate signal
sig_window_test = mod.sine_wave(256, 1, 50, 1, 0);

% Test different windows
windows = struct();
windows.hanning = mod.window_hanning(256);
windows.hamming = mod.window_hamming(256);
windows.blackman = mod.window_blackman(256);
windows.flattop = mod.window_flattop(256);

fprintf('  Window sidelobe attenuation comparison:\n');
fprintf('    Hanning: ~31 dB\n');
fprintf('    Hamming: ~42 dB\n');
fprintf('    Blackman: ~58 dB\n');
fprintf('    Flat Top: ~44 dB (flat passband)\n');

% Apply windows and check spectral characteristics
for field = fieldnames(windows)'
    w = windows.(field{1});
    windowed_sig = sig_window_test .* w;
    [spec, ~] = mod.fft_spectrum(windowed_sig, 50);
    [~, peak_idx] = max(spec);
    fprintf('  %s window: main lobe width affects frequency resolution\n', field{1});
end

fprintf('\n');

%% 5. Signal Quality Metrics
fprintf('5. Signal Quality Metrics\n');
fprintf('-------------------------\n');

% Create test signals with different characteristics
fs = 1000;

% Pure sine wave
pure_sine = mod.sine_wave(fs, 1, 50);
pure_stats = mod.signal_statistics(pure_sine);
fprintf('  Pure sine wave:\n');
fprintf('    RMS: %.4f (expected ~0.707)\n', pure_stats.rms);
fprintf('    Crest factor: %.4f (expected ~1.414)\n', pure_stats.crest_factor);

% Clipped sine wave
clipped_sine = mod.clip(pure_sine, -0.5, 0.5);
clipped_stats = mod.signal_statistics(clipped_sine);
fprintf('  Clipped sine wave:\n');
fprintf('    Crest factor: %.4f (increased due to clipping)\n', clipped_stats.crest_factor);

% Signal with DC offset
dc_sig = pure_sine + 0.5;
dc_value = mod.dc_offset(dc_sig);
fprintf('  Signal with DC offset:\n');
fprintf('    DC component: %.4f\n', dc_value);

% Remove DC
no_dc_sig = mod.remove_dc(dc_sig);
fprintf('    After DC removal: mean = %.6f\n', mean(no_dc_sig));

fprintf('\n');

%% 6. Correlation Analysis
fprintf('6. Correlation Analysis\n');
fprintf('----------------------\n');

% Create signals for correlation
sig_a = mod.sine_wave(100, 1, 5);
sig_b = mod.sine_wave(100, 1, 5, 1, pi/6);  % Same frequency, phase shifted

% Cross-correlation
xcorr_result = mod.correlate(sig_a, sig_b);
[~, peak_idx] = max(xcorr_result);
fprintf('  Cross-correlation peak at lag: %d\n', peak_idx - length(sig_a));

% Autocorrelation
auto_result = mod.autocorrelate(sig_a);
fprintf('  Autocorrelation peak at center (lag=0)\n');
fprintf('  Autocorrelation length: %d\n', length(auto_result));

fprintf('\n');

%% 7. THD and Signal Distortion
fprintf('7. THD Analysis\n');
fprintf('---------------\n');

% Create a distorted sine wave (with harmonics)
fs = 1000;
fundamental_freq = 50;
fundamental = mod.sine_wave(fs, 1, fundamental_freq);
harmonic2 = mod.sine_wave(fs, 1, fundamental_freq * 2, 0.1, 0);
harmonic3 = mod.sine_wave(fs, 1, fundamental_freq * 3, 0.05, 0);

distorted_sig = mod.add_signals(fundamental, harmonic2);
distorted_sig = mod.add_signals(distorted_sig, harmonic3);

fprintf('  Created distorted signal:\n');
fprintf('    Fundamental: 50 Hz (amplitude=1)\n');
fprintf('    2nd harmonic: 100 Hz (amplitude=0.1)\n');
fprintf('    3rd harmonic: 150 Hz (amplitude=0.05)\n');

% Calculate THD
thd = mod.total_harmonic_distortion(distorted_sig, fs, fundamental_freq, 5);
fprintf('  Total Harmonic Distortion: %.4f (%.2f%%)\n', thd, thd * 100);
fprintf('  Theoretical THD: sqrt(0.1^2 + 0.05^2) = %.4f\n', sqrt(0.1^2 + 0.05^2));

fprintf('\n');

%% 8. Bandwidth Analysis
fprintf('8. Bandwidth Analysis\n');
fprintf('--------------------\n');

% Create bandlimited signal
fs = 1000;
% Use a chirp to simulate a signal with specific bandwidth
chirp_sig = mod.chirp(fs, 0.5, 50, 100, 'linear');

bw_3db = mod.bandwidth(chirp_sig, fs, -3);
bw_6db = mod.bandwidth(chirp_sig, fs, -6);

fprintf('  Chirp signal (50 Hz to 100 Hz)\n');
fprintf('    -3 dB bandwidth: %.2f Hz\n', bw_3db);
fprintf('    -6 dB bandwidth: %.2f Hz\n', bw_6db);

% Center frequency
center_freq = mod.center_frequency(chirp_sig, fs);
fprintf('    Spectral center frequency: %.2f Hz\n', center_freq);

fprintf('\n=== End of Advanced Examples ===\n');