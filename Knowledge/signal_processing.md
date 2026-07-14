Signal Processing & DSP Complete Reference
CHAPTER 1: GETTING STARTED WITH SIGNAL PROCESSING
Remarks
Signal processing analyzes, modifies, and synthesizes signals (sound, images, sensor data, communications). Two main domains: time-domain (samples over time) and frequency-domain (spectral components). Key techniques: Fourier transforms, filtering, convolution, sampling theory, wavelets. Applications: audio processing, image compression, telecommunications, radar, medical imaging, control systems.
Tools: Python (NumPy, SciPy, Matplotlib), MATLAB/Octave (industry standard), Audacity (audio), FFmpeg (multimedia), GNU Radio (SDR).
Hello Signal Processing
# hello_signal.py
"""
Generate, visualize, and analyze a simple signal.
"""
import numpy as np
import matplotlib.pyplot as plt

# Generate a simple signal: 440 Hz sine wave (A4 note)
fs = 44100  # Sampling frequency (Hz)
duration = 1.0  # seconds
t = np.arange(0, duration, 1/fs)
frequency = 440.0  # Hz
signal = np.sin(2 * np.pi * frequency * t)

# Add noise
noise = 0.1 * np.random.randn(len(t))
noisy_signal = signal + noise

# Plot
plt.figure(figsize=(14, 4))
plt.subplot(1, 2, 1)
plt.plot(t[:1000], noisy_signal[:1000])
plt.title('Noisy 440 Hz Signal (first 1000 samples)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(alpha=0.3)

# Compute FFT
from numpy.fft import fft, fftfreq
N = len(signal)
Y = fft(noisy_signal)
freqs = fftfreq(N, 1/fs)

# Only positive frequencies
pos_mask = freqs > 0
plt.subplot(1, 2, 2)
plt.plot(freqs[pos_mask], 2.0/N * np.abs(Y[pos_mask]))
plt.title('Frequency Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.xlim(0, 1000)
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('hello_signal.png', dpi=100)
plt.show()

print(f"Signal length: {N} samples")
print(f"Duration: {duration} s")
print(f"Sampling rate: {fs} Hz")
print(f"Peak frequency: {freqs[pos_mask][np.argmax(np.abs(Y[pos_mask]))]:.1f} Hz")

Fundamental Concepts
# Signal: function of one or more variables carrying information
# Continuous-time signal: x(t), defined for all real t
# Discrete-time signal: x[n], defined for integer n (sampled)

# Sampling: convert continuous → discrete
# Sampling rate fs: samples per second
# Nyquist theorem: fs > 2 * f_max (avoid aliasing)

# Signal types:
# - Deterministic: predictable (sine, square)
# - Stochastic: random (noise)
# - Periodic: x(t) = x(t + T)
# - Aperiodic: no period

# Key operations:
# - Addition, scaling, shifting, time-reversal
# - Convolution, correlation
# - Differentiation, integration
# - Sampling, quantization

import numpy as np

def generate_sine(freq, fs, duration, amplitude=1.0, phase=0.0):
    """Generate sine wave."""
    t = np.arange(0, duration, 1/fs)
    return amplitude * np.sin(2 * np.pi * freq * t + phase), t

def generate_square(freq, fs, duration, amplitude=1.0):
    """Generate square wave."""
    t = np.arange(0, duration, 1/fs)
    return amplitude * np.sign(np.sin(2 * np.pi * freq * t)), t

def generate_sawtooth(freq, fs, duration, amplitude=1.0):
    """Generate sawtooth wave."""
    t = np.arange(0, duration, 1/fs)
    return amplitude * (2 * (freq * t - np.floor(0.5 + freq * t))), t

def generate_triangle(freq, fs, duration, amplitude=1.0):
    """Generate triangle wave."""
    t = np.arange(0, duration, 1/fs)
    return amplitude * (2 * np.abs(2 * (freq * t - np.floor(0.5 + freq * t))) - 1), t

# Example: composite signal
s1, t = generate_sine(440, 44100, 1.0)
s2, _ = generate_sine(880, 44100, 1.0, amplitude=0.5)
s3, _ = generate_sine(1320, 44100, 1.0, amplitude=0.25)
composite = s1 + s2 + s3

print(f"Composite signal: 440 + 880 + 1320 Hz")
print(f"Peak amplitude: {np.max(np.abs(composite)):.3f}")

CHAPTER 2: FOURIER ANALYSIS
Discrete Fourier Transform (DFT)
# DFT: decompose signal into frequency components
# X[k] = Σ x[n] * e^{-j*2π*k*n/N} for n=0..N-1
# Inverse DFT: x[n] = (1/N) * Σ X[k] * e^{j*2π*k*n/N}

import numpy as np

def dft(x):
    """Compute DFT directly (O(N²), slow)."""
    N = len(x)
    n = np.arange(N)
    k = n.reshape((N, 1))
    W = np.exp(-2j * np.pi * k * n / N)
    return W @ x

def idft(X):
    """Compute inverse DFT."""
    N = len(X)
    n = np.arange(N)
    k = n.reshape((N, 1))
    W = np.exp(2j * np.pi * k * n / N)
    return (W @ X) / N

# Example: DFT of simple signal
x = np.array([1, 2, 1, -1, -2, -1, 1, 2])
X = dft(x)
x_reconstructed = idft(X)

print(f"Original: {x}")
print(f"DFT: {X}")
print(f"Reconstructed: {np.real(x_reconstructed).round(6)}")
print(f"Reconstruction error: {np.max(np.abs(x - x_reconstructed)):.2e}")

Fast Fourier Transform (FFT)
# FFT: efficient DFT algorithm (O(N log N))
# Cooley-Tukey algorithm: divide-and-conquer
# Most common: radix-2 FFT (N must be power of 2)

def fft_radix2(x):
    """Cooley-Tukey radix-2 FFT."""
    N = len(x)
    if N <= 1:
        return x
    
    if N % 2 != 0:
        raise ValueError("Size must be power of 2")
    
    # Divide into even and odd
    even = fft_radix2(x[0::2])
    odd = fft_radix2(x[1::2])
    
    # Combine (butterfly operation)
    T = np.exp(-2j * np.pi * np.arange(N) / N) * odd
    return np.concatenate([even + T[:N//2], even - T[:N//2]])

# Compare with NumPy FFT
x = np.random.randn(1024)
X_custom = fft_radix2(x)
X_numpy = np.fft.fft(x)

print(f"\nFFT comparison:")
print(f"Max difference: {np.max(np.abs(X_custom - X_numpy)):.2e}")

# Benchmark
import time

sizes = [2**i for i in range(8, 16)]
for N in sizes:
    x = np.random.randn(N)
    
    start = time.time()
    for _ in range(10):
        X_numpy = np.fft.fft(x)
    numpy_time = (time.time() - start) / 10
    
    print(f"N={N:6d}: NumPy FFT = {numpy_time*1000:.3f} ms")

Spectrogram and STFT
# STFT: Short-Time Fourier Transform
# Applies FFT to overlapping windows of signal
# Shows how frequency content changes over time

from scipy.signal import stft, spectrogram

def compute_spectrogram(signal, fs, window_size=1024, hop_size=256):
    """Compute spectrogram using STFT."""
    window = np.hanning(window_size)
    
    # Number of frames
    n_frames = 1 + (len(signal) - window_size) // hop_size
    
    # Allocate spectrogram matrix
    n_fft = window_size
    spec = np.zeros((n_fft // 2 + 1, n_frames))
    
    for i in range(n_frames):
        start = i * hop_size
        frame = signal[start:start + window_size] * window
        spectrum = np.fft.rfft(frame)
        spec[:, i] = np.abs(spectrum)
    
    return spec

# Example: chirp signal (frequency increases over time)
fs = 8000
duration = 2.0
t = np.arange(0, duration, 1/fs)
chirp = np.sin(2 * np.pi * (100 + 500 * t) * t)  # 100 → 1100 Hz

# Compute spectrogram
spec = compute_spectrogram(chirp, fs, window_size=512, hop_size=128)

# Plot
plt.figure(figsize=(10, 4))
plt.imshow(20 * np.log10(spec + 1e-10), aspect='auto', origin='lower',
           extent=[0, duration, 0, fs/2])
plt.title('Spectrogram of Chirp Signal')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.colorbar(label='Magnitude (dB)')
plt.tight_layout()
plt.show()

Power Spectral Density
# PSD: distribution of power over frequency
# Methods: periodogram, Welch's method, autocorrelation

from scipy.signal import welch

def estimate_psd(signal, fs, method='welch'):
    """Estimate power spectral density."""
    if method == 'welch':
        freqs, psd = welch(signal, fs, nperseg=1024)
    elif method == 'periodogram':
        from scipy.signal import periodogram
        freqs, psd = periodogram(signal, fs)
    else:
        raise ValueError(f"Unknown method: {method}")
    return freqs, psd

# Example: noisy signal with two tones
fs = 1000
t = np.arange(0, 2, 1/fs)
signal = (np.sin(2*np.pi*50*t) + 
          0.5*np.sin(2*np.pi*120*t) + 
          0.5*np.random.randn(len(t)))

freqs, psd = estimate_psd(signal, fs, 'welch')

plt.figure(figsize=(10, 4))
plt.semilogy(freqs, psd)
plt.title('Power Spectral Density (Welch)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD (V²/Hz)')
plt.grid(alpha=0.3)
plt.xlim(0, 200)
plt.tight_layout()
plt.show()

CHAPTER 3: FILTERING
Convolution
# Convolution: fundamental operation in signal processing
# y[n] = Σ x[k] * h[n-k] (discrete convolution)
# Represents filtering: output = input * impulse_response

import numpy as np

def convolve_direct(x, h):
    """Direct convolution (O(N*M))."""
    N = len(x)
    M = len(h)
    y = np.zeros(N + M - 1)
    
    for n in range(len(y)):
        for k in range(M):
            if 0 <= n - k < N:
                y[n] += x[n - k] * h[k]
    
    return y

# Compare with NumPy
x = np.random.randn(100)
h = np.array([0.25, 0.5, 0.25])  # Simple smoothing filter

y_direct = convolve_direct(x, h)
y_numpy = np.convolve(x, h, mode='full')

print(f"Convolution difference: {np.max(np.abs(y_direct - y_numpy)):.2e}")

# Convolution theorem: convolution in time = multiplication in frequency
# F{x * h} = F{x} · F{h}

def convolve_fft(x, h):
    """FFT-based convolution (O(N log N))."""
    N = len(x) + len(h) - 1
    N_fft = 2 ** int(np.ceil(np.log2(N)))  # Next power of 2
    
    X = np.fft.fft(x, N_fft)
    H = np.fft.fft(h, N_fft)
    Y = X * H
    y = np.fft.ifft(Y)[:N]
    
    return np.real(y)

# Benchmark
x = np.random.randn(10000)
h = np.random.randn(100)

t1 = time.time()
y1 = np.convolve(x, h)
t2 = time.time()
y2 = convolve_fft(x, h)
t3 = time.time()

print(f"\nConvolution of 10000 × 100:")
print(f"Direct: {(t2-t1)*1000:.2f} ms")
print(f"FFT:    {(t3-t2)*1000:.2f} ms")

FIR Filters
# FIR (Finite Impulse Response): always stable, linear phase
# y[n] = Σ b[k] * x[n-k] for k=0..M-1
# Designed using window method, Parks-McClellan, etc.

from scipy.signal import firwin, freqz, lfilter

def design_lowpass_fir(cutoff, fs, numtaps=101):
    """Design FIR lowpass filter using window method."""
    nyquist = fs / 2
    normalized_cutoff = cutoff / nyquist
    coeffs = firwin(numtaps, normalized_cutoff, window='hamming')
    return coeffs

def design_highpass_fir(cutoff, fs, numtaps=101):
    """Design FIR highpass filter."""
    nyquist = fs / 2
    normalized_cutoff = cutoff / nyquist
    coeffs = firwin(numtaps, normalized_cutoff, window='hamming', pass_zero=False)
    return coeffs

def design_bandpass_fir(low, high, fs, numtaps=101):
    """Design FIR bandpass filter."""
    nyquist = fs / 2
    coeffs = firwin(numtaps, [low/nyquist, high/nyquist], 
                    window='hamming', pass_zero=False)
    return coeffs

def design_bandstop_fir(low, high, fs, numtaps=101):
    """Design FIR bandstop (notch) filter."""
    nyquist = fs / 2
    coeffs = firwin(numtaps, [low/nyquist, high/nyquist], 
                    window='hamming')
    return coeffs

# Example: design and analyze lowpass filter
fs = 1000
cutoff = 100  # Hz
fir_coeffs = design_lowpass_fir(cutoff, fs, numtaps=101)

# Frequency response
w, h = freqz(fir_coeffs, worN=1024)
freq_response = np.abs(h)
freq_axis = w * fs / (2 * np.pi)

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.stem(range(len(fir_coeffs)), fir_coeffs, markerfmt=' ')
plt.title(f'FIR Lowpass Filter Coefficients (fc={cutoff} Hz)')
plt.xlabel('Tap')
plt.ylabel('Coefficient')
plt.grid(alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(freq_axis, 20 * np.log10(freq_response + 1e-10))
plt.title('Frequency Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.axvline(cutoff, color='r', linestyle='--', label='Cutoff')
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

# Apply filter to signal
t = np.arange(0, 1, 1/fs)
signal = (np.sin(2*np.pi*50*t) +      # 50 Hz (pass)
          np.sin(2*np.pi*200*t) +     # 200 Hz (reject)
          0.5*np.random.randn(len(t)))

filtered = lfilter(fir_coeffs, 1.0, signal)

plt.figure(figsize=(12, 4))
plt.plot(t[:500], signal[:500], label='Original', alpha=0.5)
plt.plot(t[:500], filtered[:500], label='Filtered', linewidth=2)
plt.title('FIR Lowpass Filter Applied')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

IIR Filters
# IIR (Infinite Impulse Response): feedback, more efficient
# y[n] = Σ b[k]*x[n-k] - Σ a[k]*y[n-k]
# Types: Butterworth, Chebyshev, Elliptic, Bessel

from scipy.signal import butter, cheby1, ellip, bessel

def design_butterworth(order, cutoff, fs, btype='low'):
    """Design Butterworth filter (maximally flat)."""
    nyquist = fs / 2
    normalized = cutoff / nyquist
    b, a = butter(order, normalized, btype=btype)
    return b, a

def design_chebyshev(order, ripple, cutoff, fs, btype='low'):
    """Design Chebyshev Type I filter (ripple in passband)."""
    nyquist = fs / 2
    normalized = cutoff / nyquist
    b, a = cheby1(order, ripple, normalized, btype=btype)
    return b, a

def design_elliptic(order, rp, rs, cutoff, fs, btype='low'):
    """Design elliptic filter (ripple in both bands)."""
    nyquist = fs / 2
    normalized = cutoff / nyquist
    b, a = ellip(order, rp, rs, normalized, btype=btype)
    return b, a

# Compare filter types
fs = 1000
cutoff = 100
order = 5

b_butter, a_butter = design_butterworth(order, cutoff, fs)
b_cheby, a_cheby = design_chebyshev(order, 1.0, cutoff, fs)  # 1 dB ripple
b_ellip, a_ellip = design_elliptic(order, 1.0, 40.0, cutoff, fs)

# Plot frequency responses
w, h_butter = freqz(b_butter, a_butter, worN=1024)
_, h_cheby = freqz(b_cheby, a_cheby, worN=1024)
_, h_ellip = freqz(b_ellip, a_ellip, worN=1024)

freq_axis = w * fs / (2 * np.pi)

plt.figure(figsize=(10, 5))
plt.plot(freq_axis, 20*np.log10(np.abs(h_butter)), label='Butterworth')
plt.plot(freq_axis, 20*np.log10(np.abs(h_cheby)), label='Chebyshev')
plt.plot(freq_axis, 20*np.log10(np.abs(h_ellip)), label='Elliptic')
plt.title(f'{order}th Order Lowpass Filters (fc={cutoff} Hz)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.axvline(cutoff, color='k', linestyle='--', alpha=0.5)
plt.grid(alpha=0.3)
plt.legend()
plt.ylim(-80, 5)
plt.xlim(0, 300)
plt.tight_layout()
plt.show()

Filter Application
from scipy.signal import filtfilt, sosfilt

def apply_filter(signal, b, a, method='lfilter'):
    """Apply IIR filter using different methods."""
    if method == 'lfilter':
        return lfilter(b, a, signal)
    elif method == 'filtfilt':
        # Zero-phase filtering (forward-backward)
        return filtfilt(b, a, signal)
    else:
        raise ValueError(f"Unknown method: {method}")

# Example: remove 60 Hz power line noise
fs = 1000
t = np.arange(0, 2, 1/fs)
signal = (np.sin(2*np.pi*5*t) +          # 5 Hz signal
          0.5*np.sin(2*np.pi*60*t) +      # 60 Hz noise
          0.2*np.random.randn(len(t)))    # Random noise

# Design notch filter at 60 Hz
notch_b, notch_a = design_bandstop_fir(58, 62, fs, numtaps=201)
filtered = apply_filter(signal, notch_b, notch_a, 'lfilter')

plt.figure(figsize=(12, 4))
plt.plot(t[:500], signal[:500], label='Noisy', alpha=0.5)
plt.plot(t[:500], filtered[:500], label='Filtered (60 Hz removed)', linewidth=2)
plt.title('Notch Filter at 60 Hz')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

CHAPTER 4: SAMPLING AND RECONSTRUCTION
Sampling Theorem
# Nyquist-Shannon: fs > 2 * f_max to avoid aliasing
# Aliasing: high frequencies appear as lower frequencies
# Anti-aliasing filter: lowpass before sampling

def demonstrate_aliasing():
    """Show aliasing effect."""
    fs = 100  # Sampling rate
    f_signal = 60  # Signal frequency (> fs/2 = 50)
    
    t_continuous = np.linspace(0, 1, 1000)
    y_continuous = np.sin(2 * np.pi * f_signal * t_continuous)
    
    # Sample at fs
    t_sampled = np.arange(0, 1, 1/fs)
    y_sampled = np.sin(2 * np.pi * f_signal * t_sampled)
    
    # Aliased frequency
    f_alias = abs(f_signal - fs)  # 60 - 100 = -40 → 40 Hz
    
    plt.figure(figsize=(10, 4))
    plt.plot(t_continuous, y_continuous, 'b-', label=f'Original ({f_signal} Hz)')
    plt.plot(t_sampled, y_sampled, 'ro', label=f'Sampled at {fs} Hz')
    plt.plot(t_continuous, np.sin(2*np.pi*f_alias*t_continuous), 
             'g--', label=f'Aliased ({f_alias} Hz)')
    plt.title(f'Aliasing: {f_signal} Hz signal sampled at {fs} Hz')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

demonstrate_aliasing()

Quantization
# Quantization: map continuous amplitude to discrete levels
# Quantization error: difference between original and quantized
# SNR ≈ 6.02 * N + 1.76 dB (N = number of bits)

def quantize(signal, bits):
    """Quantize signal to given bit depth."""
    levels = 2 ** bits
    max_val = np.max(np.abs(signal))
    
    # Normalize to [-1, 1]
    normalized = signal / max_val
    
    # Quantize
    quantized = np.round(normalized * (levels - 1) / 2) / ((levels - 1) / 2)
    
    # Denormalize
    return quantized * max_val

# Example: 8-bit vs 16-bit quantization
fs = 8000
t = np.arange(0, 0.1, 1/fs)
signal = np.sin(2 * np.pi * 440 * t)

q8 = quantize(signal, 8)
q16 = quantize(signal, 16)

# Compute SNR
def compute_snr(original, quantized):
    noise = original - quantized
    signal_power = np.mean(original ** 2)
    noise_power = np.mean(noise ** 2)
    return 10 * np.log10(signal_power / noise_power)

print(f"8-bit SNR: {compute_snr(signal, q8):.1f} dB (theoretical: 49.8 dB)")
print(f"16-bit SNR: {compute_snr(signal, q16):.1f} dB (theoretical: 98.1 dB)")

Interpolation and Resampling
from scipy.signal import resample, resample_poly, decimate, interp

def resample_signal(signal, original_fs, target_fs):
    """Resample signal to new sampling rate."""
    ratio = target_fs / original_fs
    new_length = int(len(signal) * ratio)
    return resample(signal, new_length)

# Example: upsample and downsample
fs_original = 1000
fs_target = 4000
t = np.arange(0, 1, 1/fs_original)
signal = np.sin(2 * np.pi * 50 * t)

# Upsample
signal_up = resample_signal(signal, fs_original, fs_target)

# Downsample (with anti-aliasing)
signal_down = decimate(signal, 4)  # Factor of 4

print(f"Original: {len(signal)} samples at {fs_original} Hz")
print(f"Upsampled: {len(signal_up)} samples at {fs_target} Hz")
print(f"Downsampled: {len(signal_down)} samples at {fs_original//4} Hz")

CHAPTER 5: AUDIO PROCESSING
Audio I/O
import soundfile as sf
import librosa

def load_audio(filename, sr=None):
    """Load audio file."""
    signal, fs = librosa.load(filename, sr=sr, mono=True)
    return signal, fs

def save_audio(filename, signal, fs):
    """Save audio to file."""
    sf.write(filename, signal, fs)

# Generate test tone
def generate_tone(freq, duration, fs, amplitude=0.5):
    """Generate sine wave tone."""
    t = np.arange(0, duration, 1/fs)
    return amplitude * np.sin(2 * np.pi * freq * t)

# Save test tone
tone = generate_tone(440, 2.0, 44100)
# save_audio('test_tone.wav', tone, 44100)

Audio Effects
def apply_reverb(signal, fs, decay=0.5, delay_ms=50):
    """Simple reverb using comb filter."""
    delay_samples = int(fs * delay_ms / 1000)
    reverb = np.zeros(len(signal) + delay_samples)
    
    for i in range(len(signal)):
        reverb[i] += signal[i]
        if i >= delay_samples:
            reverb[i] += decay * reverb[i - delay_samples]
    
    return reverb[:len(signal)]

def apply_echo(signal, fs, delay_ms=300, decay=0.6, num_echoes=3):
    """Multi-tap echo effect."""
    delay_samples = int(fs * delay_ms / 1000)
    output = signal.copy()
    
    for i in range(1, num_echoes + 1):
        delay = delay_samples * i
        attenuation = decay ** i
        if delay < len(signal):
            output[delay:] += attenuation * signal[:-delay]
    
    return output

def apply_distortion(signal, threshold=0.5, gain=2.0):
    """Soft-clipping distortion."""
    amplified = signal * gain
    return np.tanh(amplified / threshold) * threshold

def apply_chorus(signal, fs, depth_ms=10, rate_hz=1.0):
    """Chorus effect using modulated delay."""
    depth_samples = int(fs * depth_ms / 1000)
    output = signal.copy()
    
    t = np.arange(len(signal)) / fs
    modulation = depth_samples * np.sin(2 * np.pi * rate_hz * t)
    
    for i in range(len(signal)):
        delay = int(modulation[i])
        if i - delay >= 0:
            output[i] += 0.5 * signal[i - delay]
    
    return output

# Example: apply effects to test tone
fs = 44100
duration = 2.0
t = np.arange(0, duration, 1/fs)
test_signal = np.sin(2 * np.pi * 440 * t) * 0.5

reverb_signal = apply_reverb(test_signal, fs, decay=0.4, delay_ms=30)
echo_signal = apply_echo(test_signal, fs, delay_ms=200, decay=0.5, num_echoes=3)
distorted = apply_distortion(test_signal, threshold=0.3, gain=3.0)

# save_audio('reverb.wav', reverb_signal, fs)
# save_audio('echo.wav', echo_signal, fs)
# save_audio('distorted.wav', distorted, fs)

Pitch Detection
def detect_pitch_autocorrelation(signal, fs, min_freq=50, max_freq=1000):
    """Detect pitch using autocorrelation."""
    # Autocorrelation
    corr = np.correlate(signal, signal, mode='full')
    corr = corr[len(corr)//2:]
    
    # Find first peak after initial decay
    min_lag = int(fs / max_freq)
    max_lag = int(fs / min_freq)
    
    search_region = corr[min_lag:max_lag]
    peak_idx = np.argmax(search_region) + min_lag
    
    pitch = fs / peak_idx
    return pitch

def detect_pitch_yin(signal, fs, threshold=0.1):
    """YIN pitch detection algorithm."""
    frame_size = 2048
    tau_max = frame_size // 2
    
    # Compute difference function
    diff = np.zeros(tau_max)
    for tau in range(1, tau_max):
        diff[tau] = np.sum((signal[:frame_size-tau] - signal[tau:frame_size])**2)
    
    # Cumulative mean normalized difference
    cmnd = np.zeros(tau_max)
    cmnd[0] = 1
    running_sum = 0
    for tau in range(1, tau_max):
        running_sum += diff[tau]
        cmnd[tau] = diff[tau] * tau / running_sum if running_sum > 0 else 1
    
    # Find pitch
    for tau in range(2, tau_max):
        if cmnd[tau] < threshold:
            while tau + 1 < tau_max and cmnd[tau+1] < cmnd[tau]:
                tau += 1
            return fs / tau
    
    return 0

# Example: detect pitch of 440 Hz tone
fs = 44100
t = np.arange(0, 0.1, 1/fs)
test_tone = np.sin(2 * np.pi * 440 * t)

pitch_ac = detect_pitch_autocorrelation(test_tone, fs)
pitch_yin = detect_pitch_yin(test_tone, fs)

print(f"Autocorrelation pitch: {pitch_ac:.1f} Hz")
print(f"YIN pitch: {pitch_yin:.1f} Hz")

CHAPTER 6: IMAGE PROCESSING
2D Fourier Transform
# 2D DFT for images: F[u,v] = ΣΣ f[x,y] * e^{-j*2π*(ux/M + vy/N)}
# Used for frequency analysis, filtering, compression

from numpy.fft import fft2, ifft2, fftshift

def analyze_image_frequency(image):
    """Compute 2D FFT of image."""
    # 2D FFT
    F = fft2(image)
    F_shifted = fftshift(F)  # Center zero frequency
    
    # Magnitude spectrum (log scale)
    magnitude = np.log(1 + np.abs(F_shifted))
    
    # Phase spectrum
    phase = np.angle(F_shifted)
    
    return magnitude, phase

# Example: create test image
x = np.arange(256)
y = np.arange(256)
X, Y = np.meshgrid(x, y)

# Image with multiple frequencies
image = (np.sin(2*np.pi*10*X/256) + 
         np.sin(2*np.pi*30*Y/256) + 
         np.sin(2*np.pi*20*(X+Y)/256))

magnitude, phase = analyze_image_frequency(image)

plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.subplot(1, 3, 2)
plt.imshow(magnitude, cmap='viridis')
plt.title('Magnitude Spectrum')
plt.subplot(1, 3, 3)
plt.imshow(phase, cmap='gray')
plt.title('Phase Spectrum')
plt.tight_layout()
plt.show()

2D Filtering
from scipy.ndimage import convolve2d, gaussian_filter, median_filter

def apply_lowpass_2d(image, kernel_size=5):
    """2D lowpass filter (averaging)."""
    kernel = np.ones((kernel_size, kernel_size)) / (kernel_size ** 2)
    return convolve2d(image, kernel, mode='same', boundary='wrap')

def apply_highpass_2d(image):
    """2D highpass filter (Laplacian)."""
    kernel = np.array([[0, -1, 0],
                       [-1, 4, -1],
                       [0, -1, 0]])
    return convolve2d(image, kernel, mode='same', boundary='wrap')

def apply_gaussian_2d(image, sigma=2.0):
    """2D Gaussian blur."""
    return gaussian_filter(image, sigma=sigma)

def apply_median_2d(image, size=3):
    """2D median filter (removes salt-and-pepper noise)."""
    return median_filter(image, size=size)

# Example: image with noise
image_clean = np.zeros((100, 100))
image_clean[30:70, 30:70] = 1.0

# Add noise
noisy = image_clean + 0.3 * np.random.randn(100, 100)
noisy = np.clip(noisy, 0, 1)

# Apply filters
blurred = apply_gaussian_2d(noisy, sigma=1.5)
median_filtered = apply_median_2d(noisy, size=3)
edge_detected = apply_highpass_2d(image_clean)

plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.imshow(noisy, cmap='gray')
plt.title('Noisy Image')
plt.subplot(2, 2, 2)
plt.imshow(blurred, cmap='gray')
plt.title('Gaussian Blur')
plt.subplot(2, 2, 3)
plt.imshow(median_filtered, cmap='gray')
plt.title('Median Filter')
plt.subplot(2, 2, 4)
plt.imshow(edge_detected, cmap='gray')
plt.title('Edge Detection (Laplacian)')
plt.tight_layout()
plt.show()

Image Compression (JPEG-like)
from scipy.fft import dct, idct

def compress_block(block, quality=50):
    """Compress 8x8 block using DCT."""
    # DCT
    dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
    
    # Quantization matrix (simplified)
    quant_matrix = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ])
    
    # Scale quantization by quality
    scale = max(1, (100 - quality) / 5)
    quant_matrix = quant_matrix * scale
    
    # Quantize
    quantized = np.round(dct_block / quant_matrix)
    
    return quantized, quant_matrix

def decompress_block(quantized, quant_matrix):
    """Decompress 8x8 block."""
    # Dequantize
    dct_block = quantized * quant_matrix
    
    # Inverse DCT
    block = idct(idct(dct_block.T, norm='ortho').T, norm='ortho')
    
    return block

# Example: compress and decompress image patch
np.random.seed(42)
image_patch = np.random.rand(8, 8) * 255

quantized, qm = compress_block(image_patch, quality=50)
reconstructed = decompress_block(quantized, qm)

error = np.mean((image_patch - reconstructed) ** 2)
compression_ratio = 64 / np.count_nonzero(quantized)

print(f"MSE: {error:.2f}")
print(f"Compression ratio: {compression_ratio:.2f}x")
print(f"Non-zero coefficients: {np.count_nonzero(quantized)}/64")

CHAPTER 7: WAVELET TRANSFORMS
Continuous Wavelet Transform
# Wavelets: localized oscillations (unlike infinite sinusoids)
# CWT: W(a,b) = (1/√a) * ∫ x(t) * ψ*((t-b)/a) dt
# a = scale (frequency), b = translation (time)

def morlet_wavelet(t, omega0=5.0):
    """Morlet wavelet (complex)."""
    return np.pi**(-0.25) * np.exp(1j*omega0*t) * np.exp(-t**2/2)

def continuous_wavelet_transform(signal, scales, fs):
    """Compute CWT using Morlet wavelet."""
    n = len(signal)
    n_scales = len(scales)
    cwt = np.zeros((n_scales, n), dtype=complex)
    
    t = np.arange(-4*max(scales), 4*max(scales)+1) / fs
    
    for i, scale in enumerate(scales):
        # Scaled wavelet
        wavelet = morlet_wavelet(t / scale) / np.sqrt(scale)
        
        # Convolve with signal
        cwt[i, :] = np.convolve(signal, wavelet, mode='same')
    
    return cwt

# Example: analyze chirp signal
fs = 1000
duration = 2.0
t = np.arange(0, duration, 1/fs)
chirp = np.sin(2 * np.pi * (10 + 50 * t) * t)  # 10 → 110 Hz

scales = np.arange(1, 100)
cwt_result = continuous_wavelet_transform(chirp, scales, fs)

# Plot scalogram
plt.figure(figsize=(10, 5))
plt.imshow(np.abs(cwt_result), aspect='auto', cmap='viridis',
           extent=[0, duration, scales[-1], scales[0]])
plt.title('Wavelet Scalogram (Morlet)')
plt.xlabel('Time (s)')
plt.ylabel('Scale')
plt.colorbar(label='Magnitude')
plt.tight_layout()
plt.show()

Discrete Wavelet Transform (DWT)
# DWT: multi-resolution analysis
# Decomposes signal into approximation and detail coefficients
# Uses filter banks (lowpass + highpass)

from pywt import dwt, idwt, wavedec, waverec

def wavelet_decomposition(signal, wavelet='db4', level=3):
    """Multi-level wavelet decomposition."""
    coeffs = wavedec(signal, wavelet, level=level)
    return coeffs

def wavelet_reconstruction(coeffs, wavelet='db4'):
    """Reconstruct signal from wavelet coefficients."""
    return waverec(coeffs, wavelet)

def wavelet_denoise(signal, wavelet='db4', level=3, threshold=None):
    """Denoise signal using wavelet thresholding."""
    coeffs = wavedec(signal, wavelet, level=level)
    
    # Estimate noise from finest detail coefficients
    if threshold is None:
        sigma = np.median(np.abs(coeffs[-1])) / 0.6745
        threshold = sigma * np.sqrt(2 * np.log(len(signal)))
    
    # Soft thresholding
    import pywt
    denoised_coeffs = [coeffs[0]]  # Keep approximation
    for c in coeffs[1:]:
        denoised_coeffs.append(pywt.threshold(c, threshold, mode='soft'))
    
    return waverec(denoised_coeffs, wavelet)

# Example: denoise noisy signal
fs = 1000
t = np.arange(0, 1, 1/fs)
clean = np.sin(2 * np.pi * 10 * t)
noisy = clean + 0.5 * np.random.randn(len(t))

denoised = wavelet_denoise(noisy, wavelet='db4', level=4)

plt.figure(figsize=(12, 6))
plt.subplot(3, 1, 1)
plt.plot(t, clean)
plt.title('Clean Signal')
plt.ylabel('Amplitude')
plt.grid(alpha=0.3)

plt.subplot(3, 1, 2)
plt.plot(t, noisy, alpha=0.7)
plt.title('Noisy Signal')
plt.ylabel('Amplitude')
plt.grid(alpha=0.3)

plt.subplot(3, 1, 3)
plt.plot(t, denoised, color='green')
plt.title('Wavelet Denoised')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# Compute SNR improvement
snr_before = compute_snr(clean, noisy)
snr_after = compute_snr(clean, denoised)
print(f"SNR before: {snr_before:.1f} dB")
print(f"SNR after: {snr_after:.1f} dB")
print(f"Improvement: {snr_after - snr_before:.1f} dB")

CHAPTER 8: STATISTICAL SIGNAL PROCESSING
Autocorrelation and Cross-Correlation
def autocorrelation(signal, max_lag=None):
    """Compute autocorrelation function."""
    if max_lag is None:
        max_lag = len(signal) // 2
    
    signal = signal - np.mean(signal)  # Remove mean
    var = np.var(signal)
    
    acf = np.zeros(max_lag)
    for lag in range(max_lag):
        acf[lag] = np.correlate(signal, signal, mode='full')[len(signal)-1+lag] / (var * len(signal))
    
    return acf

def cross_correlation(x, y, max_lag=None):
    """Compute cross-correlation between two signals."""
    if max_lag is None:
        max_lag = len(x) // 2
    
    x = x - np.mean(x)
    y = y - np.mean(y)
    
    ccf = np.correlate(x, y, mode='full')
    ccf = ccf[len(ccf)//2 - max_lag : len(ccf)//2 + max_lag + 1]
    ccf /= (np.std(x) * np.std(y) * len(x))
    
    return ccf

# Example: find time delay between signals
fs = 1000
t = np.arange(0, 1, 1/fs)
signal1 = np.sin(2 * np.pi * 10 * t)
delay_samples = 50
signal2 = np.roll(signal1, delay_samples)

ccf = cross_correlation(signal1, signal2, max_lag=200)
lags = np.arange(-200, 201)
peak_lag = lags[np.argmax(ccf)]

print(f"True delay: {delay_samples} samples")
print(f"Detected delay: {peak_lag} samples")

Power Spectrum Estimation
def periodogram(signal, fs):
    """Compute periodogram (simple PSD estimate)."""
    N = len(signal)
    X = np.fft.fft(signal)
    psd = np.abs(X[:N//2])**2 / (fs * N)
    freqs = np.fft.fftfreq(N, 1/fs)[:N//2]
    return freqs, psd

def welch_psd(signal, fs, nperseg=256, noverlap=None):
    """Welch's method for PSD estimation."""
    if noverlap is None:
        noverlap = nperseg // 2
    
    # Segment signal
    step = nperseg - noverlap
    n_segments = (len(signal) - nperseg) // step + 1
    
    # Window
    window = np.hanning(nperseg)
    
    # Compute periodogram for each segment
    psd_sum = np.zeros(nperseg // 2 + 1)
    for i in range(n_segments):
        segment = signal[i*step : i*step + nperseg] * window
        psd_sum += np.abs(np.fft.rfft(segment))**2
    
    # Average and normalize
    psd = psd_sum / (n_segments * fs * np.sum(window**2))
    freqs = np.fft.rfftfreq(nperseg, 1/fs)
    
    return freqs, psd

# Example: compare methods
fs = 1000
t = np.arange(0, 5, 1/fs)
signal = (np.sin(2*np.pi*50*t) + 
          0.5*np.sin(2*np.pi*120*t) + 
          np.random.randn(len(t)))

freqs_per, psd_per = periodogram(signal, fs)
freqs_welch, psd_welch = welch_psd(signal, fs, nperseg=512)

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.semilogy(freqs_per, psd_per)
plt.title('Periodogram')
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD')
plt.xlim(0, 200)
plt.grid(alpha=0.3)

plt.subplot(1, 2, 2)
plt.semilogy(freqs_welch, psd_welch)
plt.title('Welch Method')
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD')
plt.xlim(0, 200)
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

Adaptive Filtering (LMS)
def lms_filter(desired, input_signal, num_taps=32, mu=0.01):
    """Least Mean Squares adaptive filter."""
    n = len(desired)
    weights = np.zeros(num_taps)
    output = np.zeros(n)
    error = np.zeros(n)
    
    for i in range(num_taps, n):
        # Input vector
        x = input_signal[i : i-num_taps : -1]
        
        # Filter output
        output[i] = np.dot(weights, x)
        
        # Error
        error[i] = desired[i] - output[i]
        
        # Update weights
        weights += mu * error[i] * x
    
    return output, error, weights

# Example: noise cancellation
fs = 1000
t = np.arange(0, 2, 1/fs)
desired = np.sin(2 * np.pi * 10 * t)  # Signal of interest
noise = 0.5 * np.sin(2 * np.pi * 60 * t)  # Interfering noise
input_signal = desired + noise

# Reference noise (correlated with interference)
reference = 0.5 * np.sin(2 * np.pi * 60 * t + 0.1)

output, error, weights = lms_filter(desired, reference, num_taps=64, mu=0.01)

plt.figure(figsize=(12, 6))
plt.subplot(3, 1, 1)
plt.plot(t, desired)
plt.title('Desired Signal')
plt.ylabel('Amplitude')
plt.grid(alpha=0.3)

plt.subplot(3, 1, 2)
plt.plot(t, input_signal)
plt.title('Noisy Input')
plt.ylabel('Amplitude')
plt.grid(alpha=0.3)

plt.subplot(3, 1, 3)
plt.plot(t, error, color='green')
plt.title('LMS Filter Output (Noise Cancelled)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

CHAPTER 9: COMMUNICATIONS SIGNAL PROCESSING
Modulation and Demodulation
def am_modulate(signal, carrier_freq, fs, modulation_index=0.8):
    """Amplitude Modulation."""
    t = np.arange(len(signal)) / fs
    carrier = np.cos(2 * np.pi * carrier_freq * t)
    modulated = (1 + modulation_index * signal) * carrier
    return modulated

def am_demodulate(modulated, carrier_freq, fs):
    """AM demodulation using envelope detection."""
    # Rectify
    rectified = np.abs(modulated)
    
    # Lowpass filter
    from scipy.signal import butter, filtfilt
    nyquist = fs / 2
    cutoff = min(1000, nyquist * 0.9)  # Keep audio frequencies
    b, a = butter(4, cutoff / nyquist, btype='low')
    demodulated = filtfilt(b, a, rectified)
    
    # Remove DC
    demodulated -= np.mean(demodulated)
    
    return demodulated

def fm_modulate(signal, carrier_freq, fs, frequency_deviation=5000):
    """Frequency Modulation."""
    t = np.arange(len(signal)) / fs
    
    # Instantaneous frequency
    instantaneous_freq = carrier_freq + frequency_deviation * signal
    
    # Phase (integral of frequency)
    phase = 2 * np.pi * np.cumsum(instantaneous_freq) / fs
    
    modulated = np.cos(phase)
    return modulated

# Example: AM modulation
fs = 44100
t = np.arange(0, 0.1, 1/fs)
message = np.sin(2 * np.pi * 440 * t)  # 440 Hz audio
carrier_freq = 10000  # 10 kHz carrier

am_signal = am_modulate(message, carrier_freq, fs, modulation_index=0.8)
demodulated = am_demodulate(am_signal, carrier_freq, fs)

# Align signals (compensate for filter delay)
delay = 50
demodulated_aligned = demodulated[delay:delay+len(message)]

plt.figure(figsize=(12, 6))
plt.subplot(3, 1, 1)
plt.plot(t, message)
plt.title('Message Signal (440 Hz)')
plt.ylabel('Amplitude')
plt.grid(alpha=0.3)

plt.subplot(3, 1, 2)
plt.plot(t, am_signal)
plt.title('AM Modulated Signal')
plt.ylabel('Amplitude')
plt.grid(alpha=0.3)

plt.subplot(3, 1, 3)
plt.plot(t[:len(demodulated_aligned)], demodulated_aligned)
plt.title('Demodulated Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

Digital Communication
def bpsk_modulate(bits):
    """Binary Phase Shift Keying modulation."""
    symbols = 2 * bits - 1  # Map 0→-1, 1→+1
    return symbols

def bpsk_demodulate(symbols):
    """BPSK demodulation."""
    bits = (symbols > 0).astype(int)
    return bits

def add_awgn(signal, snr_db):
    """Add AWGN noise for given SNR."""
    signal_power = np.mean(signal**2)
    snr_linear = 10**(snr_db/10)
    noise_power = signal_power / snr_linear
    noise = np.sqrt(noise_power) * np.randn(len(signal))
    return signal + noise

def compute_ber(transmitted, received):
    """Compute Bit Error Rate."""
    errors = np.sum(transmitted != received)
    return errors / len(transmitted)

# Example: BPSK over AWGN channel
np.random.seed(42)
n_bits = 10000
bits = np.random.randint(0, 2, n_bits)

# Modulate
symbols = bpsk_modulate(bits)

# Add noise at different SNR levels
snr_values = np.arange(0, 15, 2)
ber_values = []

for snr in snr_values:
    noisy_symbols = add_awgn(symbols, snr)
    received_bits = bpsk_demodulate(noisy_symbols)
    ber = compute_ber(bits, received_bits)
    ber_values.append(ber)
    print(f"SNR = {snr:2d} dB: BER = {ber:.6f}")

# Plot BER curve
plt.figure(figsize=(8, 5))
plt.semilogy(snr_values, ber_values, 'bo-', linewidth=2)
plt.title('BPSK BER vs SNR')
plt.xlabel('SNR (dB)')
plt.ylabel('Bit Error Rate')
plt.grid(alpha=0.3, which='both')
plt.tight_layout()
plt.show()

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Compressed Sensing
# Compressed sensing: reconstruct sparse signals from few measurements
# y = Φx, where Φ is measurement matrix (M×N, M << N)
# Reconstruction via L1 minimization (basis pursuit)

def compressed_sensing_demo():
    """Demonstrate compressed sensing."""
    from scipy.optimize import linprog
    
    # Sparse signal
    N = 100
    x = np.zeros(N)
    x[10] = 1.0
    x[50] = -0.7
    x[80] = 0.5
    
    # Measurement matrix (random Gaussian)
    M = 30  # Number of measurements
    Phi = np.random.randn(M, N) / np.sqrt(M)
    
    # Measurements
    y = Phi @ x
    
    # Reconstruct using L1 minimization (simplified)
    # min ||z||_1 s.t. Phi @ z = y
    # Split z = z+ - z- where z+, z- >= 0
    
    c = np.concatenate([np.ones(N), np.ones(N)])
    A_eq = np.hstack([Phi, -Phi])
    b_eq = y
    
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=(0, None))
    z = result.x
    x_reconstructed = z[:N] - z[N:]
    
    print(f"Reconstruction error: {np.max(np.abs(x - x_reconstructed)):.4f}")
    
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.stem(x)
    plt.title('Original Sparse Signal')
    plt.subplot(1, 3, 2)
    plt.stem(y)
    plt.title(f'Measurements (M={M})')
    plt.subplot(1, 3, 3)
    plt.stem(x_reconstructed)
    plt.title('Reconstructed')
    plt.tight_layout()
    plt.show()

compressed_sensing_demo()

Kalman Filtering
class KalmanFilter:
    """Simple 1D Kalman filter."""
    
    def __init__(self, process_noise=0.01, measurement_noise=0.1):
        self.Q = process_noise  # Process noise covariance
        self.R = measurement_noise  # Measurement noise covariance
        
        # State estimate
        self.x = 0.0  # State
        self.P = 1.0  # Error covariance
    
    def predict(self, u=0.0):
        """Predict step (time update)."""
        # State prediction: x = x + u
        self.x = self.x + u
        
        # Covariance prediction: P = P + Q
        self.P = self.P + self.Q
        
        return self.x
    
    def update(self, z):
        """Update step (measurement update)."""
        # Kalman gain: K = P / (P + R)
        K = self.P / (self.P + self.R)
        
        # State update: x = x + K * (z - x)
        self.x = self.x + K * (z - self.x)
        
        # Covariance update: P = (1 - K) * P
        self.P = (1 - K) * self.P
        
        return self.x
    
    def filter(self, measurements):
        """Filter entire sequence."""
        estimates = []
        for z in measurements:
            self.predict()
            estimate = self.update(z)
            estimates.append(estimate)
        return np.array(estimates)

# Example: track noisy position
np.random.seed(42)
true_position = np.cumsum(np.random.randn(100) * 0.1)
measurements = true_position + np.random.randn(100) * 0.5

kf = KalmanFilter(process_noise=0.01, measurement_noise=0.25)
estimated = kf.filter(measurements)

plt.figure(figsize=(10, 5))
plt.plot(true_position, 'g-', label='True', linewidth=2)
plt.plot(measurements, 'b.', label='Measurements', alpha=0.5)
plt.plot(estimated, 'r-', label='Kalman Estimate', linewidth=2)
plt.title('Kalman Filter Tracking')
plt.xlabel('Time Step')
plt.ylabel('Position')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Compute RMSE
rmse_measurements = np.sqrt(np.mean((measurements - true_position)**2))
rmse_kalman = np.sqrt(np.mean((estimated - true_position)**2))
print(f"RMSE (measurements): {rmse_measurements:.3f}")
print(f"RMSE (Kalman): {rmse_kalman:.3f}")

Machine Learning for Signal Processing
# Deep learning approaches:
# - CNNs for audio/image classification
# - RNNs/LSTMs for sequence modeling
# - Autoencoders for denoising/compression
# - Transformers for speech/music generation

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

def extract_features(signal, fs):
    """Extract features for classification."""
    # Spectral features
    spectrum = np.abs(np.fft.rfft(signal))
    spectral_centroid = np.sum(spectrum * np.arange(len(spectrum))) / np.sum(spectrum)
    spectral_rolloff = np.where(np.cumsum(spectrum) > 0.85 * np.sum(spectrum))[0][0]
    
    # Statistical features
    rms = np.sqrt(np.mean(signal**2))
    zcr = np.sum(np.abs(np.diff(np.sign(signal)))) / 2 / len(signal)
    
    return [spectral_centroid, spectral_rolloff, rms, zcr]

# Example: classify different waveforms
np.random.seed(42)
n_samples = 100

# Generate training data
X = []
y = []

for i in range(n_samples):
    # Sine wave (class 0)
    t = np.linspace(0, 1, 1000)
    signal = np.sin(2 * np.pi * (5 + np.random.rand()) * t)
    X.append(extract_features(signal, 1000))
    y.append(0)
    
    # Square wave (class 1)
    signal = np.sign(np.sin(2 * np.pi * (5 + np.random.rand()) * t))
    X.append(extract_features(signal, 1000))
    y.append(1)
    
    # Sawtooth (class 2)
    signal = 2 * (t * (5 + np.random.rand()) - np.floor(0.5 + t * (5 + np.random.rand())))
    X.append(extract_features(signal, 1000))
    y.append(2)

X = np.array(X)
y = np.array(y)

# Train classifier
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

clf = MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=500)
clf.fit(X_scaled, y)

accuracy = clf.score(X_scaled, y)
print(f"Training accuracy: {accuracy:.2%}")

Recommended Reading
# - "Digital Signal Processing" by Proakis & Manolakis
# - "The Scientist and Engineer's Guide to DSP" by Steven Smith (free online)
# - "Think DSP" by Allen Downey (free online)
# - "Understanding Digital Signal Processing" by Richard Lyons
# - "Discrete-Time Signal Processing" by Oppenheim & Schafer

# Online Resources
# - scipy.signal documentation: https://docs.scipy.org/doc/scipy/reference/signal.html
# - librosa (audio analysis): https://librosa.org/
# - PyWavelets: https://pywavelets.readthedocs.io/
# - CCMA (MATLAB-style DSP): https://www.dsprelated.com/
# - DSPRelated forums: https://www.dsprelated.com/

# End of Signal Processing Reference