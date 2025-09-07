import numpy as np
import matplotlib.pyplot as plt
import librosa

# Load MP3 file
filename = "nightcore.mp3"  # replace with your mp3 path
data, fs = librosa.load(filename, sr=None, mono=True)  # sr=None = keep original sample rate

# Length of signal
N = len(data)

# FFT computation
fft_vals = np.fft.fft(data)
fft_vals = np.abs(fft_vals[:N//2]) / N  # single-sided spectrum
fft_vals[1:-1] *= 2  # account for symmetry

# Frequency axis
freqs = np.fft.fftfreq(N, 1/fs)[:N//2]

# Plot
plt.figure(figsize=(10,6))
plt.plot(freqs, fft_vals)
plt.title("Single-Sided Amplitude Spectrum")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

