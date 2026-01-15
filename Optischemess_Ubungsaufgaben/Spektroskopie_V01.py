import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# START CODE (keep unchanged)
# -----------------------------
lam_nm = np.linspace(400, 800, 2001) # Wellenlaenge in nm
I0 = np.exp(-0.5*((lam_nm-550)/120)**2) + 0.15 # Referenzspektrum (Lampe + Offset)

depth = 0.35
sigma = 18
T_true = 1 - depth*np.exp(-0.5*((lam_nm-630)/sigma)**2) # "Absorptionsband" als Dip in T

rng = np.random.default_rng(1)
I = I0*T_true + rng.normal(0, 0.003, lam_nm.size) # gemessenes Spektrum (mit Rauschen)

# -----------------------------
# a) Transmission and Absorbance
# -----------------------------
# Transmission: T = I / I0

T = I / I0

# Because of noise, T can become <= 0 at some points -> log10 would fail.
# We clip T to a tiny positive value to keep A finite.
eps = 1e-12
T_clipped = np.clip(T,eps,None)

# Absorbance: A= -log10(T)
A = -np.log10(T_clipped)

# -----------------------------
# b) Find lambda_max and FWHM in A(lambda)
# -----------------------------
# 1) Find the peak (maximum absorbance)
idx_peak = np.argmax(A)
lambda_max = lam_nm[idx_peak]
A_max = A[idx_peak]

# 2) Estimate a baseline (outside the absorption band) to make FWHM more robust.
#    Here we exclude a region around the band (roughly 580...680 nm).

band_mask = (lam_nm > 580) &(lam_nm < 680)
baseline_mask = ~band_mask
baseline = np.median(A[baseline_mask])

# Peak height above baseline:
A_peak_height = A_max - baseline

# Half-maximum level (relative to baseline):
half_level = baseline + 0.5 * A_peak_height

# 3) Find left and right crossings with the half_level using linear interpolation.
#    We search only on each side of the peak.
A_left = A[:idx_peak+1]
lam_left = lam_nm[:idx_peak+1]
A_right = A[idx_peak:]
lam_right = lam_nm[idx_peak:]

def crossing_wavelength(lam,y,level,side="left"):
    diff = y - level
    sign = np.sign(diff)

    # Find indices where sign changes between consecutive samples:
    changes = np.where(sign[:-1] * sign[1:] <= 0)[0]

    if len(changes) == 0:
        return np.nan

    # For the left side, we want the last crossing; for the right side, the first crossing.
    i = changes[-1] if side == "left" else changes[0]

    # Linear interpolation between (lam[i], y[i]) and (lam[i+1], y[i+1])
    x0, x1 = lam[i], lam[i+1]
    y0, y1 = y[i], y[i+1]

    # Avoid division by zero if y1 == y0
    if y1 == y0:
        return x0

    return x0 + (level - y0) * (x1 - x0) / (y1 - y0)

# Left crossing (search from start up to peak)
lambda_left = crossing_wavelength(lam_left, A_left, half_level, side="left")

# Right crossing (search from peak to end)
# For "right", we use the first crossing after the peak.
lambda_right = crossing_wavelength(lam_right, A_right, half_level, side="right")

FWHM = lambda_right - lambda_left

# -----------------------------
# c) Plot results
# -----------------------------
print(f"lambda_max = {lambda_max:.2f} nm")
print(f"A_max      = {A_max:.4f}")
print(f"FWHM       = {FWHM:.2f} nm (half level = {half_level:.4f})")

# Plot 1: I0 and I
plt.figure()
plt.plot(lam_nm, I0, label="I0 (reference)")
plt.plot(lam_nm, I, label="I (measured)", linewidth=1)
plt.xlabel("Wavelength λ (nm)")
plt.ylabel("Intensity (arb. units)")
plt.title("Reference spectrum I0 and measured spectrum I")
plt.legend()
plt.grid(True)

# Plot 2: Absorbance A(lambda) + annotations
plt.figure()
plt.plot(lam_nm, A, label="A(λ) = -log10(I/I0)")
plt.axvline(lambda_max, linestyle="--", label=f"λ_max = {lambda_max:.1f} nm")
plt.axhline(half_level, linestyle="--", label=f"Half level = {half_level:.4f}")

# Mark FWHM points
plt.axvline(lambda_left, linestyle=":", label=f"λ_left = {lambda_left:.1f} nm")
plt.axvline(lambda_right, linestyle=":", label=f"λ_right = {lambda_right:.1f} nm")

plt.xlabel("Wavelength λ (nm)")
plt.ylabel("Absorbance A (a.u.)")
plt.title(f"Absorbance spectrum (FWHM ≈ {FWHM:.1f} nm)")
plt.legend()
plt.grid(True)
plt.show()