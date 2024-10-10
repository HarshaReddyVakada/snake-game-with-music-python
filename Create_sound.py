import numpy as np
from scipy.io.wavfile import write

# Parameters for the sound
sample_rate = 44100  # Samples per second
duration = 0.5  # seconds
frequency = 1000  # Hertz (1000 Hz is a higher pitch sound)

# Generate a time array
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate a sine wave
sound_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

# Convert to 16-bit PCM format
sound_wave_pcm = np.int16(sound_wave * 32767)

# Write to a WAV file
write('water_drop.wav', sample_rate, sound_wave_pcm)
