import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# GIVEN START CODE (use unchanged)
# -----------------------------
L = 1.2                 # cm (max OPD, double-sided)
N = 8192
delta = np.linspace(-L, L, N)      # OPD axis in cm
dd = delta[1] - delta[0]

sigma1, sigma2 = 1000.0, 1250.0    # cm^-1
a1, a2 = 1.0, 0.6

window = np.hanning(N)  # Hanning apodization
I = (a1*np.cos(2*np.pi*sigma1*delta) + a2*np.cos(2*np.pi*sigma2*delta)) * window

rng = np.random.default_rng(0)
I_noisy = I + rng.normal(0, 0.02, N)

# FFT -> frequency axis in cm^-1 (because delta is in cm)
spec = np.fft.fft(I_noisy)
freq = np.fft.fftfreq(N, d=dd)

pos = freq > 0
sigma = freq[pos]
S = np.abs(spec[pos])

# -----------------------------
# Helper functions (peak finding + FWHM)
# -----------------------------
def find_top_peaks(x, y, n_peaks=2):
    """
    Find the positions of the top n_peaks local maxima in y(x).
    Uses a simple neighbor comparison (no SciPy required).
    Returns peak indices sorted by peak height (descending).
    """
    # local maxima: y[i] > y[i-1] and y[i] > y[i+1]
    candidates = np.where((y[1:-1] > y[:-2]) & (y[1:-1] > y[2:]))[0] + 1
    if candidates.size == 0:
        return np.array([], dtype=int)

    # sort candidates by amplitude
    cand_sorted = candidates[np.argsort(y[candidates])[::-1]]
    return cand_sorted[:n_peaks]

def fwhm_single_peak(x, y, peak_idx, baseline_mode="median"):
    """
    Estimate FWHM around a chosen peak using half-maximum crossing points.
    baseline_mode:
      - "median": baseline = median of y (robust if most values are near baseline)
      - "zero": baseline = 0
    Returns (fwhm, x_left, x_right, half_level).
    """
    y_peak = y[peak_idx]

    if baseline_mode == "median":
        baseline = np.median(y)
    else:
        baseline = 0.0

    peak_height = y_peak - baseline
    if peak_height <= 0:
        return np.nan, np.nan, np.nan, np.nan

    half_level = baseline + 0.5 * peak_height

    # search left side
    i = peak_idx
    while i > 0 and y[i] > half_level:
        i -= 1
    if i == 0:
        return np.nan, np.nan, np.nan, np.nan

    # linear interpolation for left crossing between i and i+1
    x0, x1 = x[i], x[i+1]
    y0, y1 = y[i], y[i+1]
    x_left = x0 + (half_level - y0) * (x1 - x0) / (y1 - y0) if y1 != y0 else x0

    # search right side
    j = peak_idx
    while j < len(y)-1 and y[j] > half_level:
        j += 1
    if j == len(y)-1:
        return np.nan, np.nan, np.nan, np.nan

    # linear interpolation for right crossing between j-1 and j
    x0, x1 = x[j-1], x[j]
    y0, y1 = y[j-1], y[j]
    x_right = x0 + (half_level - y0) * (x1 - x0) / (y1 - y0) if y1 != y0 else x1

    return (x_right - x_left), x_left, x_right, half_level

# -----------------------------
# (a) Plot interferogram near delta=0 and spectrum in 900..1350 cm^-1
# -----------------------------
# Interferogram: show only a small window around 0 (e.g. +/- 0.05 cm)
win = 0.05
mask_d = np.abs(delta) <= win

plt.figure()
plt.plot(delta[mask_d], I_noisy[mask_d])
plt.xlabel("OPD δ (cm)")
plt.ylabel("Interferogram I_noisy(δ) (a.u.)")
plt.title("FTIR Interferogram (zoom around δ = 0)")
plt.grid(True)

# Spectrum: restrict to region of interest
roi = (sigma >= 900) & (sigma <= 1350)
sigma_roi = sigma[roi]
S_roi = S[roi]

plt.figure()
plt.plot(sigma_roi, S_roi)
plt.xlabel("Wavenumber σ (cm$^{-1}$)")
plt.ylabel("Magnitude spectrum S(σ) (a.u.)")
plt.title("Spectrum from FFT (900..1350 cm$^{-1}$)")
plt.grid(True)

# -----------------------------
# (b) Find peak positions
# -----------------------------
peak_idxs_roi = find_top_peaks(sigma_roi, S_roi, n_peaks=2)

if peak_idxs_roi.size < 2:
    print("Could not find 2 peaks reliably.")
else:
    # Sort peaks by wavenumber for nicer reporting (low -> high)
    peak_idxs_roi = peak_idxs_roi[np.argsort(sigma_roi[peak_idxs_roi])]
    sigma_peaks = sigma_roi[peak_idxs_roi]
    S_peaks = S_roi[peak_idxs_roi]

    print("(b) Peak positions (cm^-1):")
    for k in range(len(sigma_peaks)):
        print(f"    Peak {k+1}: sigma_peak = {sigma_peaks[k]:.3f} cm^-1")

    # Mark peaks on spectrum plot
    for sp in sigma_peaks:
        plt.axvline(sp, linestyle="--")
    plt.legend([f"Peak at {sp:.1f} cm$^{{-1}}$" for sp in sigma_peaks], loc="best")

# -----------------------------
# (c) Theoretical resolution and observed FWHM of one peak
# -----------------------------
delta_sigma_theo = 1.0 / (2.0 * L)   # cm^-1
print(f"\n(c) Theoretical resolution Δσ_theo = 1/(2L) = {delta_sigma_theo:.4f} cm^-1")

# Measure FWHM for the stronger peak (higher amplitude in ROI)
if peak_idxs_roi.size >= 1:
    strongest = peak_idxs_roi[np.argmax(S_roi[peak_idxs_roi])]
    fwhm, xL, xR, half_level = fwhm_single_peak(sigma_roi, S_roi, strongest, baseline_mode="median")

    print(f"    Observed FWHM (approx) = {fwhm:.4f} cm^-1")
    print(f"    Half-level crossings at σ = {xL:.3f} and {xR:.3f} cm^-1")

    # Add FWHM markers to spectrum plot (same figure as above)
    plt.axhline(half_level, linestyle=":")
    plt.axvline(xL, linestyle=":")
    plt.axvline(xR, linestyle=":")

plt.show()
