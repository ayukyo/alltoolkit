function signal_utils_test()
    %SIGNAL_UTILS_TEST Test suite for signal_utils module
    fprintf('Running signal_utils test suite...\n');
    fprintf('================================\n\n');
    
    test_count = 0; pass_count = 0; fail_count = 0;
    
    %% Signal Generation Tests
    
    % Test sine_wave
    sig = mod.sine_wave(1000, 1, 50);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'sine_wave length', length(sig) == 1000);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'sine_wave range', max(abs(sig)) <= 1);
    
    % Test sine_wave with amplitude
    sig = mod.sine_wave(1000, 1, 50, 2, 0);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'sine_wave amplitude', max(abs(sig)) <= 2);
    
    % Test cosine_wave
    sig = mod.cosine_wave(1000, 1, 100);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'cosine_wave length', length(sig) == 1000);
    
    % Test square_wave
    sig = mod.square_wave(1000, 1, 10);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'square_wave length', length(sig) == 1000);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'square_wave values', max(sig) == 1 && min(sig) == -1);
    
    % Test sawtooth_wave
    sig = mod.sawtooth_wave(1000, 1, 20);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'sawtooth_wave length', length(sig) == 1000);
    
    % Test triangle wave (sawtooth with width=1)
    sig = mod.sawtooth_wave(1000, 1, 20, 1);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'triangle_wave range', max(sig) <= 1 && min(sig) >= -1);
    
    % Test chirp
    sig = mod.chirp(1000, 2, 10, 100);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'chirp length', length(sig) == 2000);
    
    % Test impulse
    sig = mod.impulse(100);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'impulse length', length(sig) == 100);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'impulse value', sig(1) == 1 && sum(sig) == 1);
    
    % Test impulse at different position
    sig = mod.impulse(100, 50, 2);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'impulse position', sig(50) == 2);
    
    % Test step
    sig = mod.step(100);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'step length', length(sig) == 100);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'step values', sig(1) == 1 && sum(sig) == 100);
    
    % Test ramp
    sig = mod.ramp(100, 0, 1);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'ramp length', length(sig) == 100);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'ramp range', sig(1) == 0 && sig(end) == 1);
    
    %% Noise Generation Tests
    
    % Test white_noise
    noise = mod.white_noise(1000);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'white_noise length', length(noise) == 1000);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'white_noise mean', abs(mean(noise)) < 0.1);
    
    % Test gaussian_noise
    noise = mod.gaussian_noise(10000);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'gaussian_noise length', length(noise) == 10000);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'gaussian_noise std', abs(std(noise) - 1) < 0.1);
    
    % Test gaussian_noise with parameters
    noise = mod.gaussian_noise(10000, 5, 2);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'gaussian_noise mean param', abs(mean(noise) - 5) < 0.2);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'gaussian_noise std param', abs(std(noise) - 2) < 0.2);
    
    % Test pink_noise
    noise = mod.pink_noise(1000);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'pink_noise length', length(noise) == 1000);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'pink_noise normalized', max(abs(noise)) <= 1);
    
    %% Window Function Tests
    
    % Test window_hanning
    w = mod.window_hanning(256);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'window_hanning length', length(w) == 256);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'window_hanning endpoints', w(1) == 0 && w(end) == 0);
    
    % Test window_hamming
    w = mod.window_hamming(256);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'window_hamming length', length(w) == 256);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'window_hamming endpoints', w(1) > 0 && w(end) > 0);
    
    % Test window_blackman
    w = mod.window_blackman(256);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'window_blackman length', length(w) == 256);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'window_blackman endpoints', w(1) == 0 && w(end) == 0);
    
    % Test window_bartlett
    w = mod.window_bartlett(256);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'window_bartlett length', length(w) == 256);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'window_bartlett triangular', max(w) == 1);
    
    % Test window_kaiser
    w = mod.window_kaiser(256, 5);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'window_kaiser length', length(w) == 256);
    
    % Test window_flattop
    w = mod.window_flattop(256);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'window_flattop length', length(w) == 256);
    
    % Test window_chebyshev
    w = mod.window_chebyshev(256, 60);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'window_chebyshev length', length(w) == 256);
    
    % Test window_gaussian
    w = mod.window_gaussian(256);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'window_gaussian length', length(w) == 256);
    
    %% Spectral Analysis Tests
    
    % Test fft_spectrum
    sig = mod.sine_wave(1000, 1, 50);
    [spec, freq] = mod.fft_spectrum(sig, 1000);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'fft_spectrum length', length(spec) == length(freq));
    [~, idx] = max(spec);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'fft_spectrum peak freq', abs(freq(idx) - 50) < 1);
    
    % Test dominant_frequency
    sig = mod.sine_wave(1000, 1, 100);
    f = mod.dominant_frequency(sig, 1000);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'dominant_frequency', abs(f - 100) < 1);
    
    % Test signal_energy
    sig = [1, 2, 3, 4, 5];
    e = mod.signal_energy(sig);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'signal_energy', e == 55);
    
    % Test signal_power
    sig = [1, 1, 1, 1, 1];
    p = mod.signal_power(sig);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'signal_power', p == 1);
    
    % Test signal_rms
    sig = [1, 1, 1, 1, 1];
    r = mod.signal_rms(sig);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'signal_rms', r == 1);
    
    sig = [3, 4];
    r = mod.signal_rms(sig);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'signal_rms 3-4', abs(r - 3.5) < 0.01);
    
    %% Filtering Tests
    
    % Test moving_average
    sig = [1, 2, 3, 4, 5];
    smooth = mod.moving_average(sig, 3);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'moving_average length', length(smooth) == length(sig));
    
    % Test gaussian_filter
    sig = mod.sine_wave(1000, 1, 50) + mod.gaussian_noise(1000, 0, 0.1);
    smooth = mod.gaussian_filter(sig, 2);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'gaussian_filter length', length(smooth) == length(sig));
    
    %% Convolution and Correlation Tests
    
    % Test convolve
    c = mod.convolve([1, 2, 3], [1, 1]);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'convolve full', length(c) == 4);
    
    c = mod.convolve([1, 2, 3], [1, 1], 'same');
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'convolve same', length(c) == 3);
    
    % Test correlate
    c = mod.correlate([1, 2, 3], [1, 2]);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'correlate length', length(c) == 4);
    
    % Test autocorrelate
    sig = [1, 2, 3, 4];
    ac = mod.autocorrelate(sig);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'autocorrelate length', length(ac) == 7);
    
    % Test correlation_lags
    lags = mod.correlation_lags(100, 50);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'correlation_lags', length(lags) == 149);
    
    %% Signal Operations Tests
    
    % Test add_signals
    s1 = [1, 2, 3];
    s2 = [4, 5, 6];
    result = mod.add_signals(s1, s2);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'add_signals', isequal(result, [5, 7, 9]));
    
    % Test multiply_signals
    s1 = [1, 2, 3];
    s2 = [2, 2, 2];
    result = mod.multiply_signals(s1, s2);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'multiply_signals', isequal(result, [2, 4, 6]));
    
    % Test mix_signals
    s1 = [10, 10, 10];
    s2 = [20, 20, 20];
    result = mod.mix_signals(s1, s2, 0.5);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'mix_signals', isequal(result, [15, 15, 15]));
    
    % Test normalize_signal (max)
    sig = [1, 2, 3, 4, 5];
    n = mod.normalize_signal(sig, 'max');
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'normalize_signal max', max(abs(n)) == 1);
    
    % Test normalize_signal (rms)
    sig = [1, 1, 1, 1, 1];
    n = mod.normalize_signal(sig, 'rms');
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'normalize_signal rms', abs(mod.signal_rms(n) - 1) < 0.01);
    
    % Test rescale_signal
    sig = [0, 1, 2, 3, 4];
    result = mod.rescale_signal(sig, 0, 100);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'rescale_signal', result(1) == 0 && result(end) == 100);
    
    % Test invert_signal
    sig = [1, 2, 3];
    result = mod.invert_signal(sig);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'invert_signal', isequal(result, [-1, -2, -3]));
    
    % Test rectify
    sig = [-1, 2, -3, 4];
    result = mod.rectify(sig);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'rectify', isequal(result, [1, 2, 3, 4]));
    
    % Test half_wave_rectify
    sig = [-1, 2, -3, 4];
    result = mod.half_wave_rectify(sig);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'half_wave_rectify', isequal(result, [0, 2, 0, 4]));
    
    %% Signal Analysis Tests
    
    % Test signal_to_noise_ratio
    signal = [10, 10, 10, 10, 10];
    noise = [1, 1, 1, 1, 1];
    snr = mod.signal_to_noise_ratio(signal, noise);
    expected_snr = 10 * log10(100 / 1);  % 20 dB
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'signal_to_noise_ratio', abs(snr - expected_snr) < 0.1);
    
    % Test crest_factor
    sig = [1, 1, 1, 1, 1];
    cf = mod.crest_factor(sig);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'crest_factor constant', cf == 1);
    
    % Test zero_crossing_rate
    sig = [1, -1, 1, -1, 1];
    zc = mod.zero_crossing_rate(sig);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'zero_crossing_rate', zc == 0.4);
    
    % Test dc_offset
    sig = [5, 6, 7, 8, 9];
    dc = mod.dc_offset(sig);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'dc_offset', dc == 7);
    
    % Test remove_dc
    sig = [5, 6, 7, 8, 9];
    result = mod.remove_dc(sig);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'remove_dc', mean(result) == 0);
    
    % Test duration
    sig = zeros(1, 1000);
    d = mod.duration(sig, 1000);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'duration', d == 1);
    
    % Test time_vector
    sig = zeros(1, 1000);
    t = mod.time_vector(sig, 1000);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'time_vector length', length(t) == 1000);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'time_vector range', t(end) == 0.999);
    
    %% Signal Statistics Tests
    
    % Test signal_statistics
    sig = [1, 2, 3, 4, 5];
    stats = mod.signal_statistics(sig);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'signal_statistics mean', stats.mean == 3);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'signal_statistics min', stats.min == 1);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'signal_statistics max', stats.max == 5);
    
    %% Decibel Operations Tests
    
    % Test to_decibel
    db = mod.to_decibel(10);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'to_decibel 10', abs(db - 20) < 0.01);
    
    db = mod.to_decibel(1);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'to_decibel 1', abs(db - 0) < 0.01);
    
    % Test from_decibel
    lin = mod.from_decibel(20);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'from_decibel 20', abs(lin - 10) < 0.01);
    
    lin = mod.from_decibel(0);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'from_decibel 0', abs(lin - 1) < 0.01);
    
    % Test power_to_decibel
    db = mod.power_to_decibel(100);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'power_to_decibel 100', abs(db - 20) < 0.01);
    
    % Test decibel_to_power
    p = mod.decibel_to_power(20);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'decibel_to_power 20', abs(p - 100) < 0.01);
    
    %% Downsampling and Upsampling Tests
    
    % Test downsample
    sig = [1, 2, 3, 4, 5, 6];
    result = mod.downsample(sig, 2);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'downsample', isequal(result, [1, 3, 5]));
    
    % Test upsample
    sig = [1, 2, 3];
    result = mod.upsample(sig, 2);
    [test_count, pass_count, fail_count] = run_test(test_count, pass_count, fail_count, 'upsample length', length(result) == 6);
    
    %% Summary
    fprintf('\n================================\n');
    fprintf('Test Summary:\n');
    fprintf('  Total:  %d\n', test_count);
    fprintf('  Passed: %d\n', pass_count);
    fprintf('  Failed: %d\n', fail_count);
    fprintf('  Rate:   %.1f%%\n', 100 * pass_count / test_count);
    
    if fail_count == 0
        fprintf('\nAll tests passed!\n');
    else
        fprintf('\nSome tests failed.\n');
    end
end

function [tc, pc, fc] = run_test(tc, pc, fc, name, condition)
    tc = tc + 1;
    if condition
        pc = pc + 1;
        fprintf('  [PASS] %s\n', name);
    else
        fc = fc + 1;
        fprintf('  [FAIL] %s\n', name);
    end
end