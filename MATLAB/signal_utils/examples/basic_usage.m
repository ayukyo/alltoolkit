% BASIC_USAGE - Basic signal processing examples
% Demonstrates core functionality of signal_utils module

fprintf('=== Signal Utils Basic Examples ===\n\n');

%% 1. Signal Generation
fprintf('1. Signal Generation\n');
fprintf('-------------------\n');

% Sine wave
fs = 1000;
sig_sine = mod.sine_wave(fs, 1, 50);
fprintf('  Sine wave: 50 Hz, 1 second, fs=%d Hz\n', fs);
fprintf('  Length: %d samples\n', length(sig_sine));

% Square wave
sig_square = mod.square_wave(fs, 1, 10, 50);
fprintf('  Square wave: 10 Hz, 50%% duty cycle\n');

% Sawtooth wave
sig_sawtooth = mod.sawtooth_wave(fs, 1, 20);
fprintf('  Sawtooth wave: 20 Hz\n');

% Chirp signal
sig_chirp = mod.chirp(fs, 2, 10, 100, 'linear');
fprintf('  Linear chirp: 10 Hz to 100 Hz over 2 seconds\n');

fprintf('\n');

%% 2. Noise Generation
fprintf('2. Noise Generation\n');
fprintf('-------------------\n');

% White noise
noise_white = mod.white_noise(1000);
fprintf('  White noise: length=%d, range=[%.2f, %.2f]\n', length(noise_white), min(noise_white), max(noise_white));

% Gaussian noise
noise_gaussian = mod.gaussian_noise(10000, 0, 1);
fprintf('  Gaussian noise: mean=%.3f, std=%.3f\n', mean(noise_gaussian), std(noise_gaussian));

% Pink noise
noise_pink = mod.pink_noise(1000);
fprintf('  Pink noise: normalized to [-1, 1]\n');

fprintf('\n');

%% 3. Spectral Analysis
fprintf('3. Spectral Analysis\n');
fprintf('-------------------\n');

% Generate composite signal
sig1 = mod.sine_wave(fs, 1, 50);
sig2 = mod.sine_wave(fs, 1, 120);
composite = mod.add_signals(sig1, sig2);

% FFT spectrum
[spectrum, freq] = mod.fft_spectrum(composite, fs);
[~, idx] = max(spectrum);
fprintf('  Composite signal (50 Hz + 120 Hz)\n');
fprintf('  FFT peak frequency: %.2f Hz\n', freq(idx));

% Dominant frequency
dom_freq = mod.dominant_frequency(composite, fs);
fprintf('  Dominant frequency: %.2f Hz\n', dom_freq);

% Signal metrics
fprintf('  Signal energy: %.4f\n', mod.signal_energy(composite));
fprintf('  Signal power: %.4f\n', mod.signal_power(composite));
fprintf('  Signal RMS: %.4f\n', mod.signal_rms(composite));

fprintf('\n');

%% 4. Window Functions
fprintf('4. Window Functions\n');
fprintf('-------------------\n');

window_len = 256;

% Various windows
w_hanning = mod.window_hanning(window_len);
w_hamming = mod.window_hamming(window_len);
w_blackman = mod.window_blackman(window_len);
w_kaiser = mod.window_kaiser(window_len, 5);

fprintf('  Hanning window: endpoints = %.4f, %.4f\n', w_hanning(1), w_hanning(end));
fprintf('  Hamming window: endpoints = %.4f, %.4f\n', w_hamming(1), w_hamming(end));
fprintf('  Blackman window: endpoints = %.4f, %.4f\n', w_blackman(1), w_blackman(end));
fprintf('  Kaiser window (beta=5): center = %.4f\n', w_kaiser(window_len/2));

fprintf('\n');

%% 5. Signal Operations
fprintf('5. Signal Operations\n');
fprintf('-------------------\n');

% Signal mixing
s1 = mod.sine_wave(fs, 1, 50);
s2 = mod.sine_wave(fs, 1, 100);
mixed = mod.mix_signals(s1, s2, 0.3);  % 30% s1, 70% s2
fprintf('  Mixed signal: 30%% of 50 Hz + 70%% of 100 Hz\n');

% Normalization
raw_sig = [1, 2, 3, 4, 5];
norm_max = mod.normalize_signal(raw_sig, 'max');
norm_rms = mod.normalize_signal(raw_sig, 'rms');
fprintf('  Max normalization: [%.2f, %.2f, %.2f, %.2f, %.2f]\n', norm_max);
fprintf('  RMS normalization: RMS = %.4f\n', mod.signal_rms(norm_rms));

% Rectification
sig_neg = [-1, 2, -3, 4];
rect_full = mod.rectify(sig_neg);
rect_half = mod.half_wave_rectify(sig_neg);
fprintf('  Full-wave rectify: [%d, %d, %d, %d]\n', rect_full);
fprintf('  Half-wave rectify: [%d, %d, %d, %d]\n', rect_half);

fprintf('\n');

%% 6. Filtering
fprintf('6. Filtering\n');
fprintf('------------\n');

% Create noisy signal
clean = mod.sine_wave(fs, 1, 50);
noise = mod.gaussian_noise(fs, 0, 0.3);
noisy = mod.add_signals(clean, noise);

% Moving average smoothing
smoothed_ma = mod.moving_average(noisy, 10);
fprintf('  Moving average (window=10): smoothed noisy signal\n');

% Gaussian filter smoothing
smoothed_gauss = mod.gaussian_filter(noisy, 2);
fprintf('  Gaussian filter (sigma=2): smoothed noisy signal\n');

fprintf('\n');

%% 7. Convolution and Correlation
fprintf('7. Convolution and Correlation\n');
fprintf('----------------------------\n');

% Convolution
sig_a = [1, 2, 3];
sig_b = [1, 1];
conv_full = mod.convolve(sig_a, sig_b, 'full');
conv_same = mod.convolve(sig_a, sig_b, 'same');
fprintf('  Convolve [1,2,3] with [1,1]:\n');
fprintf('    Full: [%d, %d, %d, %d]\n', conv_full);
fprintf('    Same: [%d, %d, %d]\n', conv_same);

% Autocorrelation
auto_sig = [1, 2, 3, 4];
ac = mod.autocorrelate(auto_sig);
fprintf('  Autocorrelation length: %d\n', length(ac));

fprintf('\n');

%% 8. Decibel Operations
fprintf('8. Decibel Operations\n');
fprintf('--------------------\n');

% dB conversions
lin_val = 10;
db_val = mod.to_decibel(lin_val);
back_lin = mod.from_decibel(db_val);
fprintf('  Linear 10 -> dB: %.2f dB\n', db_val);
fprintf('  dB %.2f -> Linear: %.4f\n', db_val, back_lin);

% Power dB
power = 100;
power_db = mod.power_to_decibel(power);
fprintf('  Power 100 -> dB: %.2f dB\n', power_db);

fprintf('\n');

%% 9. Signal Analysis
fprintf('9. Signal Analysis\n');
fprintf('------------------\n');

% Signal statistics
sig = [1, 2, 3, 4, 5];
stats = mod.signal_statistics(sig);
fprintf('  Signal statistics for [1,2,3,4,5]:\n');
fprintf('    Mean: %.2f, Std: %.2f\n', stats.mean, stats.std);
fprintf('    Min: %.2f, Max: %.2f, Range: %.2f\n', stats.min, stats.max, stats.range);
fprintf('    RMS: %.4f, Energy: %.2f\n', stats.rms, stats.energy);

% Crest factor
sig_wave = mod.sine_wave(fs, 1, 50);
cf = mod.crest_factor(sig_wave);
fprintf('  Sine wave crest factor: %.4f (expected ~1.414)\n', cf);

% Zero crossing rate
zsig = [1, -1, 1, -1, 1];
zc = mod.zero_crossing_rate(zsig);
fprintf('  Zero crossing rate of [1,-1,1,-1,1]: %.2f\n', zc);

fprintf('\n');

%% 10. Sampling Operations
fprintf('10. Sampling Operations\n');
fprintf('----------------------\n');

% Downsample
original = [1, 2, 3, 4, 5, 6, 7, 8];
down = mod.downsample(original, 2);
fprintf('  Downsample by 2: [%d, %d, %d, %d, %d, %d, %d, %d] -> [%d, %d, %d, %d]\n', original, down);

% Upsample
up = mod.upsample([1, 2, 3], 2);
fprintf('  Upsample by 2: [1, 2, 3] -> length=%d\n', length(up));

fprintf('\n=== End of Examples ===\n');