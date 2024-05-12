import numpy as np
from scipy.io.wavfile import write

# Sample rate
sample_rate = 44100  # Sample rate in Hz
max_16bit = 32767  # Maximum value for 16-bit integer

# List of tuples with (frequencies, magnitudes, duration)
segments = [
    ((440, 880, 1760), (0.5, 0.3, 0.2), 2.0),
    ((), (), 1.0),
    ((440, 880), (0.5, 0.5), 3.0),
    # Add more segments as needed
]


# Function to generate wave for a single segment
def generate_segment(frequencies, magnitudes, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.zeros_like(t)
    for freq, mag in zip(frequencies, magnitudes):
        wave += mag * np.sin(2 * np.pi * freq * t)
    return wave


# Generate full wave by concatenating waves from each segment
full_wave = np.concatenate([generate_segment(freqs, mags, dur) for freqs, mags, dur in segments])

# Normalize wave to 16-bit range
full_wave_int = np.int16(full_wave / np.max(np.abs(full_wave)) * max_16bit)

# Write to WAV file
write('../outputs/complex_tone.wav', sample_rate, full_wave_int)
