Advanced Acoustics & Audio Engineering Complete Reference
CHAPTER 1: GETTING STARTED WITH ACOUSTICS
Remarks
Acoustics is the science of sound, including its generation, transmission, and reception. Audio engineering applies these principles to recording, mixing, and reproduction. Key areas: Wave physics, psychoacoustics (how humans perceive sound), digital signal processing for audio, room acoustics, and spatial audio. Applications: Music production, architectural acoustics, noise control, virtual reality audio, hearing aids.
Tools: Python (NumPy, SciPy, Librosa, PyDub), MATLAB, Audacity, Reaper, Pro Tools, COMSOL (simulation).
Hello Audio
# hello_audio.py
"""
First audio program: Generate a simple sine wave and save as WAV.
"""
import numpy as np
import wave
import struct

def generate_sine_wave(freq=440, duration=1.0, sample_rate=44100):
    """Generate a sine wave tone."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave_data = np.sin(2 * np.pi * freq * t)
    # Normalize to 16-bit integer range
    wave_data = np.int16(wave_data * 32767)
    return wave_data, sample_rate

def save_wav(filename, data, sample_rate):
    """Save numpy array as WAV file."""
    nchannels = 1
    sampwidth = 2  # 16-bit
    framerate = sample_rate
    nframes = len(data)
    comptype = "NONE"
    compname = "not compressed"
    
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
        for s in data:
            wav_file.writeframes(struct.pack('h', s))

# Generate A4 note (440 Hz)
data, sr = generate_sine_wave(440, 1.0)
save_wav("a4_tone.wav", data, sr)
print("Generated a4_tone.wav")

Sound Wave Properties
# Frequency (Hz): Pitch. Human range: 20 Hz - 20 kHz.
# Amplitude: Loudness. Measured in dB (Decibels).
# Phase: Position in the cycle. Important for interference.
# Timbre: Quality of sound, determined by harmonic content.

Decibel Scale
# dB = 20 * log10(P / P_ref) for pressure/amplitude.
# dB = 10 * log10(Power / Power_ref) for power.
# Reference pressure (air): 20 µPa (threshold of hearing).

def amplitude_to_db(amplitude, ref=1.0):
    if amplitude == 0:
        return -np.inf
    return 20 * np.log10(amplitude / ref)

print(f"Amplitude 0.5: {amplitude_to_db(0.5):.2f} dB")
print(f"Amplitude 0.1: {amplitude_to_db(0.1):.2f} dB")

CHAPTER 2: DIGITAL AUDIO REPRESENTATION
Sampling and Quantization
# Nyquist-Shannon Theorem: Sample rate must be > 2 * max frequency.
# CD Quality: 44.1 kHz, 16-bit.
# High-Res: 96 kHz / 24-bit or 192 kHz / 24-bit.

# Aliasing: Frequencies above Nyquist fold back into audible range.
# Anti-aliasing filter: Low-pass filter before ADC.

Bit Depth and Dynamic Range
# Dynamic Range ≈ 6.02 * N + 1.76 dB, where N is bit depth.
# 16-bit: ~98 dB.
# 24-bit: ~146 dB.

Dithering
# Adding low-level noise to reduce quantization distortion during bit-depth reduction.

CHAPTER 3: PSYCHOACOUSTICS
Critical Bands
# The ear divides the spectrum into ~24 critical bands (Bark scale).
# Masking: A loud sound masks a quiet sound if they are in the same critical band.
# Used in MP3/AAC compression to discard inaudible data.

Fletcher-Munson Curves
# Human hearing sensitivity varies with frequency and loudness.
# Most sensitive at 2-5 kHz.
# Less sensitive at low frequencies at low volumes.

Spatial Hearing
# Interaural Time Difference (ITD): Time delay between ears.
# Interaural Level Difference (ILD): Volume difference between ears.
# Head-Related Transfer Function (HRTF): Spectral shaping by head/pinna.

CHAPTER 4: ROOM ACOUSTICS
Reverberation
# Reflections persist after source stops.
# RT60: Time for sound to decay by 60 dB.
# Sabine Formula: RT60 = 0.161 * V / A
# V: Volume (m³), A: Total absorption (m² sabins).

def calculate_rt60(volume_m3, absorption_coefficients, areas_m2):
    """Calculate RT60 using Sabine formula."""
    total_absorption = sum(a * s for a, s in zip(absorption_coefficients, areas_m2))
    if total_absorption == 0:
        return np.inf
    return 0.161 * volume_m3 / total_absorption

# Example: Small room 4x5x3 m
V = 4 * 5 * 3
# Walls, Floor, Ceiling areas
areas = [2*(4*3 + 5*3), 4*5, 4*5] 
# Absorption coeffs (approximate for concrete/plaster)
alphas = [0.05, 0.1, 0.1] 

rt60 = calculate_rt60(V, alphas, areas)
print(f"RT60: {rt60:.2f} seconds")

Standing Waves and Modes
# Resonances at specific frequencies determined by room dimensions.
# f = (c/2) * sqrt((nx/Lx)^2 + (ny/Ly)^2 + (nz/Lz)^2)
# Causes boomy bass or nulls.

Absorption Materials
# Porous absorbers (foam, fiberglass): Effective at high frequencies.
# Membrane absorbers: Effective at low frequencies.
# Helmholtz resonators: Tuned to specific frequencies.

CHAPTER 5: AUDIO SIGNAL PROCESSING
Filters in Audio
# EQ (Equalization): Adjusting frequency balance.
# Low-pass, High-pass, Band-pass, Notch.
# Parametric EQ: Control Frequency, Gain, Q (bandwidth).

import scipy.signal as signal

def apply_eq(audio_data, sample_rate, freq, gain_db, q=1.0, filter_type='peak'):
    """Apply a parametric EQ filter."""
    b, a = signal.iirpeak(freq, q, fs=sample_rate)
    # Apply gain
    if filter_type == 'peak':
        # Simple peak implementation requires more complex design
        # Using butterworth for demo
        b, a = signal.butter(2, [freq-10, freq+10], btype='band', fs=sample_rate)
    
    filtered_data = signal.lfilter(b, a, audio_data)
    return filtered_data

Compression
# Dynamic Range Compression: Reduces volume of loud sounds.
# Threshold: Level above which compression applies.
# Ratio: Amount of compression (e.g., 4:1).
# Attack/Release: Speed of response.

def simple_compressor(audio, threshold=0.5, ratio=4.0):
    """Simple downward compressor."""
    output = np.copy(audio)
    mask = np.abs(audio) > threshold
    output[mask] = np.sign(audio[mask]) * (threshold + (np.abs(audio[mask]) - threshold) / ratio)
    return output

Reverb Algorithms
# Convolution Reverb: Uses impulse response of real space. High quality, CPU intensive.
# Algorithmic Reverb: Uses delay lines and feedback networks (Schroeder, Moorer).
# Schroeder Reverb: Parallel comb filters + series all-pass filters.

CHAPTER 6: SPATIAL AUDIO
Stereo Panning
# Linear Panning: L = cos(theta), R = sin(theta).
# Constant Power Panning: L = cos(theta), R = sin(theta) with squared sum constant.

Ambisonics
# Full-sphere surround sound.
# B-Format: W (omni), X (front-back), Y (left-right), Z (up-down).
# Higher orders provide better resolution.

Binaural Rendering
# Using HRTFs to simulate 3D audio over headphones.
# Essential for VR/AR.

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Active Noise Control
# Destructive interference to cancel noise.
# Requires precise phase alignment.
# Used in headphones, car cabins.

Synthesis Techniques
# Subtractive: Filter rich source (sawtooth).
# Additive: Sum of sine waves.
# FM (Frequency Modulation): Complex spectra from simple oscillators.
# Granular: Tiny snippets of sound.

Machine Learning in Audio
# Source Separation: Spleeter, Demucs.
# Speech Synthesis: Tacotron, WaveNet.
# Music Generation: Jukebox, MusicLM.

Recommended Reading
# - "Mastering Audio: The Art and Science" by Bob Katz
# - "Acoustics and Psychoacoustics" by Howard and Angus
# - "Designing Audio Effect Plugins in C++" by Will Pirkle
# - Librosa Documentation: https://librosa.org/

# End of Advanced Acoustics Reference