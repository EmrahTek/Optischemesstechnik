import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Given / constants (SI units!)
# -----------------------------
c = 3.00e8          # speed of light [m/s]
nu1 = 3.0e13        # frequency 1 [Hz]
nu2 = 4.5e13        # frequency 2 [Hz]

x_max = 2.0e-3      # 2.0 mm -> [m]
dx = 2.0e-6         # 2 µm  -> [m]

sigma = 0.05        # Gaussian noise std dev (dimensionless intensity)

# -----------------------------
# (a) Create x, t and I(t)
# -----------------------------
x = np.arange(0, x_max + dx/2, dx)   # [m], include endpoint safely
t = 2.0 * x / c                      # [s]  (given: t = 2x/c)
dt = t[1] - t[0]                     # [s]

rng = np.random.default_rng(0)       # reproducible noise
noise = rng.normal(0.0, sigma, size=x.size)

I = np.cos(2*np.pi*nu1*t) + 0.6*np.cos(2*np.pi*nu2*t) + noise

# Plot interferogram
plt.figure()
plt.plot(x * 1e3, I)                 # x in mm for readability
plt.xlabel("x [mm]")
plt.ylabel("I(t) [a.u.]")
plt.title("Synthetic interferogram I(t) with noise")
plt.grid(True)
plt.tight_layout()

# -----------------------------
# (b) FFT + frequency axis
# -----------------------------
# Remove DC offset (helps peak detection)
I0 = I - np.mean(I)

# Optional window to reduce spectral leakage (still NumPy-only)
window = np.hanning(I0.size)
Iw = I0 * window

Y = np.fft.fft(Iw)
nu = np.fft.fftfreq(Iw.size, d=dt)   # frequency axis [Hz]

# Take only nu >= 0
mask_pos = nu >= 0
nu_pos = nu[mask_pos]
A_pos = np.abs(Y[mask_pos]) / Iw.size   # simple magnitude normalization

# Plot spectrum
plt.figure()
plt.plot(nu_pos * 1e-12, A_pos)       # Hz -> THz
plt.xlabel("ν [THz]")
plt.ylabel("|I(ν)| [a.u.]")
plt.title("Magnitude spectrum (ν ≥ 0)")
plt.grid(True)
plt.tight_layout()

# -----------------------------
# (c) Find 2 dominant frequencies (excluding ν=0) + wavelengths
# -----------------------------
# Nyquist check
fs = 1.0 / dt
nu_nyq = fs / 2.0
if nu2 > nu_nyq:
    # alias to [0, fs/2] using modulo wrapping
    nu2_alias = abs(((nu2 + fs/2) % fs) - fs/2)
    print(f"WARNING: ν2={nu2:.3e} Hz > Nyquist={nu_nyq:.3e} Hz -> aliasing expected.")
    print(f"         Expected alias frequency for ν2 is about {nu2_alias:.3e} Hz.")

# Exclude DC bin (ν=0)
mask_nonzero = nu_pos > 0
nu_nz = nu_pos[mask_nonzero]
A_nz = A_pos[mask_nonzero]

# Simple local-maximum peak finding (NumPy-only)
is_peak = (A_nz[1:-1] > A_nz[:-2]) & (A_nz[1:-1] > A_nz[2:])
peak_idx = np.where(is_peak)[0] + 1  # shift because of slicing

# If noise is very low/high, peak_idx can be small; fall back to global sort
if peak_idx.size < 2:
    top2_idx = np.argsort(A_nz)[-2:]
else:
    top2_idx = peak_idx[np.argsort(A_nz[peak_idx])[-2:]]

# Sort results by frequency
nu_peaks = np.sort(nu_nz[top2_idx])          # [Hz]
lambda_peaks = c / nu_peaks                  # [m]

print("\nDominant frequencies from FFT (excluding ν=0):")
for k, (f, lam) in enumerate(zip(nu_peaks, lambda_peaks), start=1):
    print(f"  Peak {k}: ν = {f:.3e} Hz  ->  λ = {lam*1e6:.3f} µm")




plt.show()