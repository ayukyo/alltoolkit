classdef mod < handle
    %SIGNAL_UTILS Comprehensive signal processing utilities for MATLAB
    %   Provides signal generation, filtering, spectral analysis,
    %   windowing functions, and noise utilities for scientific computing.
    %
    %   Author: AllToolkit
    %   Version: 1.0.0
    %   License: MIT
    
    methods (Static)
        %% Signal Generation
        
        function signal = sine_wave(fs, duration, frequency, amplitude, phase)
            %SINE_WAVE Generate a sine wave signal
            %   signal = sine_wave(fs, duration, frequency) - Generate sine wave
            %   signal = sine_wave(fs, duration, frequency, amplitude, phase)
            %
            %   Inputs:
            %       fs        - Sampling frequency (Hz)
            %       duration  - Signal duration (seconds)
            %       frequency - Signal frequency (Hz)
            %       amplitude - Signal amplitude (default: 1)
            %       phase     - Initial phase in radians (default: 0)
            %
            %   Example:
            %       sig = mod.sine_wave(1000, 1, 50);  % 50 Hz sine wave
            %       sig = mod.sine_wave(1000, 1, 50, 2, pi/4);  % With amplitude and phase
            
            if nargin < 4, amplitude = 1; end
            if nargin < 5, phase = 0; end
            
            t = 0:1/fs:duration-1/fs;
            signal = amplitude * sin(2 * pi * frequency * t + phase);
        end
        
        function signal = cosine_wave(fs, duration, frequency, amplitude, phase)
            %COSINE_WAVE Generate a cosine wave signal
            %   signal = cosine_wave(fs, duration, frequency)
            %
            %   Example:
            %       sig = mod.cosine_wave(1000, 1, 100);  % 100 Hz cosine wave
            
            if nargin < 4, amplitude = 1; end
            if nargin < 5, phase = 0; end
            
            t = 0:1/fs:duration-1/fs;
            signal = amplitude * cos(2 * pi * frequency * t + phase);
        end
        
        function signal = square_wave(fs, duration, frequency, duty_cycle)
            %SQUARE_WAVE Generate a square wave signal
            %   signal = square_wave(fs, duration, frequency)
            %   signal = square_wave(fs, duration, frequency, duty_cycle)
            %
            %   Inputs:
            %       duty_cycle - Percentage of high state (default: 50)
            %
            %   Example:
            %       sig = mod.square_wave(1000, 1, 10);  % 10 Hz square wave
            %       sig = mod.square_wave(1000, 1, 10, 25);  % 25% duty cycle
            
            if nargin < 4, duty_cycle = 50; end
            
            t = 0:1/fs:duration-1/fs;
            signal = square(2 * pi * frequency * t, duty_cycle);
        end
        
        function signal = sawtooth_wave(fs, duration, frequency, width)
            %SAWTOOTH_WAVE Generate a sawtooth wave signal
            %   signal = sawtooth_wave(fs, duration, frequency)
            %   signal = sawtooth_wave(fs, duration, frequency, width)
            %
            %   Inputs:
            %       width - 0 for sawtooth, 1 for triangle (default: 0)
            %
            %   Example:
            %       sig = mod.sawtooth_wave(1000, 1, 20);  % Sawtooth
            %       sig = mod.sawtooth_wave(1000, 1, 20, 1);  % Triangle wave
            
            if nargin < 4, width = 0; end
            
            t = 0:1/fs:duration-1/fs;
            signal = sawtooth(2 * pi * frequency * t, width);
        end
        
        function signal = chirp(fs, duration, f0, f1, method)
            %CHIRP Generate a frequency-swept signal
            %   signal = chirp(fs, duration, f0, f1)
            %   signal = chirp(fs, duration, f0, f1, method)
            %
            %   Inputs:
            %       f0     - Start frequency (Hz)
            %       f1     - End frequency (Hz)
            %       method - 'linear', 'quadratic', 'logarithmic' (default: 'linear')
            %
            %   Example:
            %       sig = mod.chirp(1000, 2, 10, 100);  % 10Hz to 100Hz chirp
            
            if nargin < 5, method = 'linear'; end
            
            t = 0:1/fs:duration-1/fs;
            signal = chirp(t, f0, duration, f1, method);
        end
        
        function signal = impulse(length, position, amplitude)
            %IMPULSE Generate an impulse (delta) signal
            %   signal = impulse(length) - Unit impulse at position 1
            %   signal = impulse(length, position, amplitude)
            %
            %   Example:
            %       sig = mod.impulse(100);  % Unit impulse of length 100
            %       sig = mod.impulse(100, 50, 2);  % Impulse of amplitude 2 at position 50
            
            if nargin < 2, position = 1; end
            if nargin < 3, amplitude = 1; end
            
            signal = zeros(1, length);
            signal(position) = amplitude;
        end
        
        function signal = step(length, position, amplitude)
            %STEP Generate a step signal
            %   signal = step(length) - Unit step starting at position 1
            %   signal = step(length, position, amplitude)
            %
            %   Example:
            %       sig = mod.step(100);  % Unit step of length 100
            %       sig = mod.step(100, 20, 5);  % Step of amplitude 5 starting at 20
            
            if nargin < 2, position = 1; end
            if nargin < 3, amplitude = 1; end
            
            signal = zeros(1, length);
            signal(position:end) = amplitude;
        end
        
        function signal = ramp(length, start_val, end_val)
            %RAMP Generate a ramp (linearly increasing) signal
            %   signal = ramp(length, start_val, end_val)
            %
            %   Example:
            %       sig = mod.ramp(100, 0, 1);  % Linear ramp from 0 to 1
            
            signal = linspace(start_val, end_val, length);
        end
        
        %% Noise Generation
        
        function noise = white_noise(length, amplitude)
            %WHITE_NOISE Generate white noise (uniform distribution)
            %   noise = white_noise(length)
            %   noise = white_noise(length, amplitude)
            %
            %   Example:
            %       n = mod.white_noise(1000);  % White noise of length 1000
            %       n = mod.white_noise(1000, 0.5);  % Amplitude 0.5
            
            if nargin < 2, amplitude = 1; end
            
            noise = amplitude * (2 * rand(1, length) - 1);
        end
        
        function noise = gaussian_noise(length, mean_val, std_val)
            %GAUSSIAN_NOISE Generate Gaussian (normal) noise
            %   noise = gaussian_noise(length)
            %   noise = gaussian_noise(length, mean_val, std_val)
            %
            %   Example:
            %       n = mod.gaussian_noise(1000);  % Standard normal noise
            %       n = mod.gaussian_noise(1000, 0, 0.1);  % Mean 0, std 0.1
            
            if nargin < 2, mean_val = 0; end
            if nargin < 3, std_val = 1; end
            
            noise = mean_val + std_val * randn(1, length);
        end
        
        function noise = pink_noise(length)
            %PINK_NOISE Generate pink noise (1/f noise)
            %   noise = pink_noise(length)
            %
            %   Example:
            %       n = mod.pink_noise(10000);  % Pink noise of length 10000
            
            % Generate using Voss-McCartney algorithm
            num_rows = 16;
            array = zeros(num_rows, length);
            
            % Initialize
            for i = 1:num_rows
                array(i, 1) = randn();
            end
            
            % Generate
            for j = 2:length
                for i = 1:num_rows
                    if rand() < 1 / (2^(i-1))
                        array(i, j) = randn();
                    else
                        array(i, j) = array(i, j-1);
                    end
                end
            end
            
            noise = sum(array, 1);
            noise = noise - mean(noise);
            noise = noise / max(abs(noise));
        end
        
        %% Window Functions
        
        function w = window_hanning(length)
            %WINDOW_HANNING Generate a Hanning window
            %   w = window_hanning(length)
            %
            %   Example:
            %       w = mod.window_hanning(256);
            
            w = hann(length)';
        end
        
        function w = window_hamming(length)
            %WINDOW_HAMMING Generate a Hamming window
            %   w = window_hamming(length)
            %
            %   Example:
            %       w = mod.window_hamming(256);
            
            w = hamming(length)';
        end
        
        function w = window_blackman(length)
            %WINDOW_BLACKMAN Generate a Blackman window
            %   w = window_blackman(length)
            %
            %   Example:
            %       w = mod.window_blackman(256);
            
            w = blackman(length)';
        end
        
        function w = window_bartlett(length)
            %WINDOW_BARTLETT Generate a Bartlett (triangular) window
            %   w = window_bartlett(length)
            %
            %   Example:
            %       w = mod.window_bartlett(256);
            
            w = bartlett(length)';
        end
        
        function w = window_kaiser(length, beta)
            %WINDOW_KAISER Generate a Kaiser window
            %   w = window_kaiser(length, beta)
            %
            %   Inputs:
            %       beta - Shape parameter (higher = more sidelobe attenuation)
            %
            %   Example:
            %       w = mod.window_kaiser(256, 5);  % Moderate attenuation
            %       w = mod.window_kaiser(256, 10);  % High attenuation
            
            w = kaiser(length, beta)';
        end
        
        function w = window_flattop(length)
            %WINDOW_FLATTOP Generate a Flat Top window
            %   w = window_flattop(length)
            %
            %   Example:
            %       w = mod.window_flattop(256);
            
            w = flattopwin(length)';
        end
        
        function w = window_chebyshev(length, sidelobe_atten)
            %WINDOW_CHEBYSHEV Generate a Chebyshev window
            %   w = window_chebyshev(length, sidelobe_atten)
            %
            %   Inputs:
            %       sidelobe_atten - Sidelobe attenuation in dB (default: 50)
            %
            %   Example:
            %       w = mod.window_chebyshev(256, 60);  % 60 dB sidelobe attenuation
            
            if nargin < 2, sidelobe_atten = 50; end
            
            w = chebwin(length, sidelobe_atten)';
        end
        
        function w = window_gaussian(length, alpha)
            %WINDOW_GAUSSIAN Generate a Gaussian window
            %   w = window_gaussian(length)
            %   w = window_gaussian(length, alpha)
            %
            %   Inputs:
            %       alpha - Width parameter (default: 2.5)
            %
            %   Example:
            %       w = mod.window_gaussian(256);
            
            if nargin < 2, alpha = 2.5; end
            
            w = gausswin(length, alpha)';
        end
        
        %% Spectral Analysis
        
        function [spectrum, freq] = fft_spectrum(signal, fs)
            %FFT_SPECTRUM Compute the single-sided FFT spectrum
            %   [spectrum, freq] = fft_spectrum(signal, fs)
            %
            %   Inputs:
            %       signal - Input signal
            %       fs     - Sampling frequency (Hz)
            %
            %   Outputs:
            %       spectrum - Magnitude spectrum
            %       freq     - Frequency vector (Hz)
            %
            %   Example:
            %       [spec, f] = mod.fft_spectrum(sig, 1000);
            
            n = length(signal);
            yf = fft(signal);
            p2 = abs(yf / n);
            spectrum = p2(1:floor(n/2)+1);
            spectrum(2:end-1) = 2 * spectrum(2:end-1);
            freq = fs * (0:floor(n/2)) / n;
        end
        
        function [psd, freq] = power_spectral_density(signal, fs, nfft)
            %POWER_SPECTRAL_DENSITY Compute PSD using Welch's method
            %   [psd, freq] = power_spectral_density(signal, fs)
            %   [psd, freq] = power_spectral_density(signal, fs, nfft)
            %
            %   Example:
            %       [p, f] = mod.power_spectral_density(sig, 1000);
            
            if nargin < 3, nfft = min(256, length(signal)); end
            
            window = hamming(nfft)';
            noverlap = floor(nfft / 2);
            
            [psd, freq] = pwelch(signal, window, noverlap, nfft, fs);
        end
        
        function [spectrogram_data, freq, time] = spectrogram_calc(signal, fs, window_length, overlap)
            %SPECTROGRAM_CALC Compute spectrogram of signal
            %   [s, f, t] = spectrogram_calc(signal, fs, window_length, overlap)
            %
            %   Inputs:
            %       signal        - Input signal
            %       fs            - Sampling frequency (Hz)
            %       window_length - Window length in samples
            %       overlap       - Overlap in samples
            %
            %   Example:
            %       [s, f, t] = mod.spectrogram_calc(sig, 1000, 256, 128);
            
            if nargin < 4, overlap = floor(window_length / 2); end
            
            window = hamming(window_length);
            [spectrogram_data, freq, time] = spectrogram(signal, window, overlap, window_length, fs);
        end
        
        function dominant_freq = dominant_frequency(signal, fs)
            %DOMINANT_FREQUENCY Find the dominant frequency in a signal
            %   freq = dominant_frequency(signal, fs)
            %
            %   Example:
            %       f = mod.dominant_frequency(sig, 1000);
            
            [spectrum, freq] = mod.fft_spectrum(signal, fs);
            [~, idx] = max(spectrum);
            dominant_freq = freq(idx);
        end
        
        function energy = signal_energy(signal)
            %SIGNAL_ENERGY Compute the energy of a signal
            %   energy = signal_energy(signal)
            %
            %   Example:
            %       e = mod.signal_energy(sig);
            
            energy = sum(abs(signal(:)).^2);
        end
        
        function power = signal_power(signal)
            %SIGNAL_POWER Compute the average power of a signal
            %   power = signal_power(signal)
            %
            %   Example:
            %       p = mod.signal_power(sig);
            
            power = sum(abs(signal(:)).^2) / length(signal(:));
        end
        
        function rms = signal_rms(signal)
            %SIGNAL_RMS Compute the RMS value of a signal
            %   rms = signal_rms(signal)
            %
            %   Example:
            %       r = mod.signal_rms(sig);
            
            rms = sqrt(mean(abs(signal(:)).^2));
        end
        
        %% Filtering
        
        function [b, a] = lowpass_filter(order, cutoff, fs)
            %LOWPASS_FILTER Design a Butterworth lowpass filter
            %   [b, a] = lowpass_filter(order, cutoff, fs)
            %
            %   Inputs:
            %       order  - Filter order
            %       cutoff - Cutoff frequency (Hz)
            %       fs     - Sampling frequency (Hz)
            %
            %   Example:
            %       [b, a] = mod.lowpass_filter(4, 100, 1000);
            %       filtered = filter(b, a, signal);
            
            wn = cutoff / (fs / 2);
            [b, a] = butter(order, wn, 'low');
        end
        
        function [b, a] = highpass_filter(order, cutoff, fs)
            %HIGHPASS_FILTER Design a Butterworth highpass filter
            %   [b, a] = highpass_filter(order, cutoff, fs)
            %
            %   Example:
            %       [b, a] = mod.highpass_filter(4, 50, 1000);
            %       filtered = filter(b, a, signal);
            
            wn = cutoff / (fs / 2);
            [b, a] = butter(order, wn, 'high');
        end
        
        function [b, a] = bandpass_filter(order, low_cutoff, high_cutoff, fs)
            %BANDPASS_FILTER Design a Butterworth bandpass filter
            %   [b, a] = bandpass_filter(order, low_cutoff, high_cutoff, fs)
            %
            %   Example:
            %       [b, a] = mod.bandpass_filter(4, 50, 150, 1000);
            %       filtered = filter(b, a, signal);
            
            wn = [low_cutoff, high_cutoff] / (fs / 2);
            [b, a] = butter(order, wn, 'bandpass');
        end
        
        function [b, a] = bandstop_filter(order, low_cutoff, high_cutoff, fs)
            %BANDSTOP_FILTER Design a Butterworth bandstop (notch) filter
            %   [b, a] = bandstop_filter(order, low_cutoff, high_cutoff, fs)
            %
            %   Example:
            %       [b, a] = mod.bandstop_filter(4, 55, 65, 1000);  % Remove 60 Hz
            %       filtered = filter(b, a, signal);
            
            wn = [low_cutoff, high_cutoff] / (fs / 2);
            [b, a] = butter(order, wn, 'stop');
        end
        
        function filtered = moving_average(signal, window_size)
            %MOVING_AVERAGE Apply moving average smoothing
            %   filtered = moving_average(signal, window_size)
            %
            %   Example:
            %       smooth = mod.moving_average(sig, 10);
            
            kernel = ones(1, window_size) / window_size;
            filtered = conv(signal, kernel, 'same');
        end
        
        function filtered = gaussian_filter(signal, sigma)
            %GAUSSIAN_FILTER Apply Gaussian smoothing filter
            %   filtered = gaussian_filter(signal, sigma)
            %
            %   Example:
            %       smooth = mod.gaussian_filter(sig, 2);
            
            window_size = ceil(6 * sigma);
            if mod(window_size, 2) == 0
                window_size = window_size + 1;
            end
            
            t = linspace(-3*sigma, 3*sigma, window_size);
            kernel = exp(-t.^2 / (2*sigma^2));
            kernel = kernel / sum(kernel);
            
            filtered = conv(signal, kernel, 'same');
        end
        
        function filtered = median_filter(signal, window_size)
            %MEDIAN_FILTER Apply median filter for noise removal
            %   filtered = median_filter(signal, window_size)
            %
            %   Example:
            %       smooth = mod.median_filter(sig, 5);
            
            filtered = medfilt1(signal, window_size);
        end
        
        function filtered = savitzky_golay(signal, order, frame_length)
            %SAVITZKY_GOLAY Apply Savitzky-Golay smoothing filter
            %   filtered = savitzky_golay(signal, order, frame_length)
            %
            %   Inputs:
            %       order        - Polynomial order
            %       frame_length - Frame length (must be odd)
            %
            %   Example:
            %       smooth = mod.savitzky_golay(sig, 3, 11);
            
            filtered = sgolayfilt(signal, order, frame_length);
        end
        
        function filtered = wiener_filter(signal, window_size)
            %WIENER_FILTER Apply Wiener filter for noise reduction
            %   filtered = wiener_filter(signal, window_size)
            %
            %   Example:
            %       denoised = mod.wiener_filter(sig, 10);
            
            filtered = wiener2(signal, [window_size, window_size]);
        end
        
        %% Convolution and Correlation
        
        function result = convolve(signal1, signal2, mode)
            %CONVOLVE Convolve two signals
            %   result = convolve(signal1, signal2)
            %   result = convolve(signal1, signal2, mode)
            %
            %   Modes: 'full', 'same', 'valid' (default: 'full')
            %
            %   Example:
            %       c = mod.convolve([1, 2, 3], [1, 1]);
            %       c = mod.convolve([1, 2, 3], [1, 1], 'same');
            
            if nargin < 3, mode = 'full'; end
            
            result = conv(signal1, signal2, mode);
        end
        
        function result = correlate(signal1, signal2, mode)
            %CORRELATE Cross-correlate two signals
            %   result = correlate(signal1, signal2)
            %   result = correlate(signal1, signal2, mode)
            %
            %   Example:
            %       c = mod.correlate([1, 2, 3], [1, 2]);
            
            if nargin < 3, mode = 'full'; end
            
            result = xcorr(signal1, signal2, mode);
        end
        
        function result = autocorrelate(signal, max_lag)
            %AUTOCORRELATE Compute autocorrelation of a signal
            %   result = autocorrelate(signal)
            %   result = autocorrelate(signal, max_lag)
            %
            %   Example:
            %       ac = mod.autocorrelate(sig);
            %       ac = mod.autocorrelate(sig, 50);
            
            if nargin < 2
                result = xcorr(signal);
            else
                result = xcorr(signal, max_lag);
            end
        end
        
        function lags = correlation_lags(length1, length2)
            %CORRELATION_LAGS Generate lag indices for cross-correlation
            %   lags = correlation_lags(length1, length2)
            %
            %   Example:
            %       l = mod.correlation_lags(100, 50);
            
            lags = (-length2+1:length1-1)';
        end
        
        %% Signal Operations
        
        function signal = add_signals(signal1, signal2)
            %ADD_SIGNALS Add two signals with automatic length matching
            %   signal = add_signals(signal1, signal2)
            %
            %   Example:
            %       sum_sig = mod.add_signals(sig1, sig2);
            
            len1 = length(signal1);
            len2 = length(signal2);
            max_len = max(len1, len2);
            
            s1 = [signal1, zeros(1, max_len - len1)];
            s2 = [signal2, zeros(1, max_len - len2)];
            
            signal = s1 + s2;
        end
        
        function signal = multiply_signals(signal1, signal2)
            %MULTIPLY_SIGNALS Multiply two signals (amplitude modulation)
            %   signal = multiply_signals(signal1, signal2)
            %
            %   Example:
            %       modulated = mod.multiply_signals(carrier, envelope);
            
            len1 = length(signal1);
            len2 = length(signal2);
            min_len = min(len1, len2);
            
            signal = signal1(1:min_len) .* signal2(1:min_len);
        end
        
        function signal = mix_signals(signal1, signal2, mix_ratio)
            %MIX_SIGNALS Mix two signals with given ratio
            %   signal = mix_signals(signal1, signal2, mix_ratio)
            %
            %   Inputs:
            %       mix_ratio - Ratio of signal1 (0 to 1)
            %
            %   Example:
            %       mixed = mod.mix_signals(sig1, sig2, 0.5);  % Equal mix
            
            if nargin < 3, mix_ratio = 0.5; end
            
            len1 = length(signal1);
            len2 = length(signal2);
            max_len = max(len1, len2);
            
            s1 = [signal1, zeros(1, max_len - len1)];
            s2 = [signal2, zeros(1, max_len - len2)];
            
            signal = mix_ratio * s1 + (1 - mix_ratio) * s2;
        end
        
        function signal = normalize_signal(signal, method)
            %NORMALIZE_SIGNAL Normalize a signal
            %   signal = normalize_signal(signal)
            %   signal = normalize_signal(signal, method)
            %
            %   Methods: 'max', 'rms', 'energy', 'zscore' (default: 'max')
            %
            %   Example:
            %       n = mod.normalize_signal(sig);  % Max normalization
            %       n = mod.normalize_signal(sig, 'rms');  % RMS normalization
            
            if nargin < 2, method = 'max'; end
            
            switch lower(method)
                case 'max'
                    max_val = max(abs(signal));
                    if max_val > 0
                        signal = signal / max_val;
                    end
                case 'rms'
                    rms_val = sqrt(mean(signal.^2));
                    if rms_val > 0
                        signal = signal / rms_val;
                    end
                case 'energy'
                    energy = sum(signal.^2);
                    if energy > 0
                        signal = signal / sqrt(energy);
                    end
                case 'zscore'
                    signal = (signal - mean(signal)) / std(signal);
                otherwise
                    signal = signal / max(abs(signal));
            end
        end
        
        function signal = rescale_signal(signal, min_val, max_val)
            %RESCALE_SIGNAL Rescale signal to specified range
            %   signal = rescale_signal(signal, min_val, max_val)
            %
            %   Example:
            %       s = mod.rescale_signal(sig, -1, 1);
            %       s = mod.rescale_signal(sig, 0, 255);
            
            signal_min = min(signal);
            signal_max = max(signal);
            range_val = signal_max - signal_min;
            
            if range_val > 0
                signal = (signal - signal_min) / range_val * (max_val - min_val) + min_val;
            else
                signal = (min_val + max_val) / 2 * ones(size(signal));
            end
        end
        
        function signal = invert_signal(signal)
            %INVERT_SIGNAL Invert (negate) a signal
            %   signal = invert_signal(signal)
            %
            %   Example:
            %       inv = mod.invert_signal(sig);
            
            signal = -signal;
        end
        
        function signal = rectify(signal)
            %RECTIFY Full-wave rectification of a signal
            %   signal = rectify(signal)
            %
            %   Example:
            %       rect = mod.rectify(sig);
            
            signal = abs(signal);
        end
        
        function signal = half_wave_rectify(signal)
            %HALF_WAVE_RECTIFY Half-wave rectification of a signal
            %   signal = half_wave_rectify(signal)
            %
            %   Example:
            %       rect = mod.half_wave_rectify(sig);
            
            signal = max(signal, 0);
        end
        
        %% Signal Analysis
        
        function snr_db = signal_to_noise_ratio(signal, noise)
            %SIGNAL_TO_NOISE_RATIO Calculate SNR in dB
            %   snr_db = signal_to_noise_ratio(signal, noise)
            %
            %   Example:
            %       snr = mod.signal_to_noise_ratio(clean_sig, noise);
            
            signal_power = sum(signal.^2) / length(signal);
            noise_power = sum(noise.^2) / length(noise);
            snr_db = 10 * log10(signal_power / noise_power);
        end
        
        function thd = total_harmonic_distortion(signal, fs, fundamental_freq, num_harmonics)
            %TOTAL_HARMONIC_DISTORTION Calculate THD
            %   thd = total_harmonic_distortion(signal, fs, fundamental_freq)
            %   thd = total_harmonic_distortion(signal, fs, fundamental_freq, num_harmonics)
            %
            %   Example:
            %       thd = mod.total_harmonic_distortion(sig, 1000, 50);
            
            if nargin < 4, num_harmonics = 10; end
            
            [spectrum, freq] = mod.fft_spectrum(signal, fs);
            
            % Find fundamental and harmonics
            fundamental_power = 0;
            harmonic_power = 0;
            
            for h = 1:num_harmonics
                target_freq = fundamental_freq * h;
                [~, idx] = min(abs(freq - target_freq));
                
                if h == 1
                    fundamental_power = spectrum(idx)^2;
                else
                    harmonic_power = harmonic_power + spectrum(idx)^2;
                end
            end
            
            thd = sqrt(harmonic_power) / sqrt(fundamental_power);
        end
        
        function cre = crest_factor(signal)
            %CREST_FACTOR Calculate crest factor (peak-to-RMS ratio)
            %   cre = crest_factor(signal)
            %
            %   Example:
            %       cf = mod.crest_factor(sig);
            
            peak = max(abs(signal));
            rms_val = sqrt(mean(signal.^2));
            
            if rms_val > 0
                cre = peak / rms_val;
            else
                cre = Inf;
            end
        end
        
        function cf = center_frequency(signal, fs)
            %CENTER_FREQUENCY Calculate spectral center frequency
            %   cf = center_frequency(signal, fs)
            %
            %   Example:
            %       f_center = mod.center_frequency(sig, 1000);
            
            [spectrum, freq] = mod.fft_spectrum(signal, fs);
            spectrum = spectrum .^ 2;
            
            cf = sum(freq .* spectrum) / sum(spectrum);
        end
        
        function bw = bandwidth(signal, fs, threshold_db)
            %BANDWIDTH Calculate signal bandwidth
            %   bw = bandwidth(signal, fs)
            %   bw = bandwidth(signal, fs, threshold_db)
            %
            %   Inputs:
            %       threshold_db - Threshold in dB below peak (default: -3)
            %
            %   Example:
            %       bw = mod.bandwidth(sig, 1000);  % -3dB bandwidth
            %       bw = mod.bandwidth(sig, 1000, -6);  % -6dB bandwidth
            
            if nargin < 3, threshold_db = -3; end
            
            [spectrum, freq] = mod.fft_spectrum(signal, fs);
            spectrum_db = 20 * log10(spectrum + eps);
            max_db = max(spectrum_db);
            
            threshold = max_db + threshold_db;
            above_threshold = spectrum_db >= threshold;
            
            indices = find(above_threshold);
            
            if isempty(indices)
                bw = 0;
            else
                bw = freq(indices(end)) - freq(indices(1));
            end
        end
        
        function zc = zero_crossing_rate(signal)
            %ZERO_CROSSING_RATE Calculate zero crossing rate
            %   zc = zero_crossing_rate(signal)
            %
            %   Example:
            %       rate = mod.zero_crossing_rate(sig);
            
            zc = sum(abs(diff(sign(signal)))) / (2 * length(signal));
        end
        
        function dc = dc_offset(signal)
            %DC_OFFSET Calculate DC offset of signal
            %   dc = dc_offset(signal)
            %
            %   Example:
            %       offset = mod.dc_offset(sig);
            
            dc = mean(signal);
        end
        
        function signal = remove_dc(signal)
            %REMOVE_DC Remove DC offset from signal
            %   signal = remove_dc(signal)
            %
            %   Example:
            %       sig_no_dc = mod.remove_dc(sig);
            
            signal = signal - mean(signal);
        end
        
        function d = duration(signal, fs)
            %DURATION Calculate signal duration in seconds
            %   d = duration(signal, fs)
            %
            %   Example:
            %       dur = mod.duration(sig, 1000);  % fs = 1000 Hz
            
            d = length(signal) / fs;
        end
        
        function t = time_vector(signal, fs)
            %TIME_VECTOR Generate time vector for signal
            %   t = time_vector(signal, fs)
            %
            %   Example:
            %       t = mod.time_vector(sig, 1000);
            
            t = (0:length(signal)-1) / fs;
        end
        
        %% Signal Statistics
        
        function stats = signal_statistics(signal)
            %SIGNAL_STATISTICS Calculate comprehensive signal statistics
            %   stats = signal_statistics(signal)
            %
            %   Returns struct with: mean, std, var, min, max, range,
            %                       rms, energy, power, crest_factor
            %
            %   Example:
            %       s = mod.signal_statistics(sig);
            
            stats.mean = mean(signal);
            stats.std = std(signal);
            stats.var = var(signal);
            stats.min = min(signal);
            stats.max = max(signal);
            stats.range = stats.max - stats.min;
            stats.rms = sqrt(mean(signal.^2));
            stats.energy = sum(signal.^2);
            stats.power = stats.energy / length(signal);
            stats.crest_factor = stats.max / stats.rms;
        end
        
        %% Decibel Operations
        
        function db = to_decibel(linear)
            %TO_DECIBEL Convert linear value to dB
            %   db = to_decibel(linear)
            %
            %   Example:
            %       db = mod.to_decibel(100);  % Returns 20
            %       db = mod.to_decibel(0.01);  % Returns -20
            
            db = 20 * log10(abs(linear) + eps);
        end
        
        function linear = from_decibel(db)
            %FROM_DECIBEL Convert dB to linear value
            %   linear = from_decibel(db)
            %
            %   Example:
            %       lin = mod.from_decibel(20);  % Returns 10
            %       lin = mod.from_decibel(-6);  % Returns ~0.5
            
            linear = 10 .^ (db / 20);
        end
        
        function db = power_to_decibel(power)
            %POWER_TO_DECIBEL Convert power to dB
            %   db = power_to_decibel(power)
            %
            %   Example:
            %       db = mod.power_to_decibel(100);  % Returns 20
            
            db = 10 * log10(power + eps);
        end
        
        function power = decibel_to_power(db)
            %DECIBEL_TO_POWER Convert dB to power
            %   power = decibel_to_power(db)
            %
            %   Example:
            %       p = mod.decibel_to_power(20);  % Returns 100
            
            power = 10 .^ (db / 10);
        end
        
        %% Downsampling and Upsampling
        
        function signal = downsample(signal, factor)
            %DOWNSAMPLE Downsample a signal
            %   signal = downsample(signal, factor)
            %
            %   Example:
            %       down = mod.downsample(sig, 2);  % Reduce by factor of 2
            
            signal = signal(1:factor:end);
        end
        
        function signal = upsample(signal, factor)
            %UPSAMPLE Upsample a signal (zero insertion)
            %   signal = upsample(signal, factor)
            %
            %   Example:
            %       up = mod.upsample(sig, 2);  % Double sampling rate
            
            n = length(signal);
            signal = zeros(1, n * factor);
            signal(1:factor:end) = signal(1:factor:end) + signal;
        end
        
        function signal = resample_signal(signal, original_fs, target_fs)
            %RESAMPLE_SIGNAL Resample signal to new sampling rate
            %   signal = resample_signal(signal, original_fs, target_fs)
            %
            %   Example:
            %       new_sig = mod.resample_signal(sig, 44100, 48000);
            
            ratio = target_fs / original_fs;
            signal = resample(signal, ratio, 1);
        end
    end
end