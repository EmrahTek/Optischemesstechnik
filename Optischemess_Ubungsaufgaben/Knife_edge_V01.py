import numpy as np
import matplotlib.pyplot as plt
import math

# -----------------------------
# START CODE (keep unchanged)
# -----------------------------
rng = np.random.default_rng(7)

x_mm = np.linspace(-1.0, 1.0, 41)  # knife-edge position in mm

w_true = 0.42   # mm (1/e^2 radius, only for data generation)
x0_true = 0.15  # mm
P0 = 1.0

P = 0.5*P0*(1 + np.array([math.erf(math.sqrt(2)*(x-x0_true)/w_true) for x in x_mm]))
P_meas = P + rng.normal(0, 0.01, x_mm.size)  # measurement noise

# -----------------------------
# (a) Normalize P_meas to [0, 1]
# -----------------------------
P_min, P_max = P_meas.min(), P_meas.max()
P_norm = (P_meas - P_min) / (P_max - P_min)

# -----------------------------
# (b) Intensity profile I(x) ∝ dP/dx (numerical derivative)
# Use np.gradient for a stable numerical derivative.
# Optional: smooth a bit to reduce noise.
# -----------------------------
I_raw = np.gradient(P_norm, x_mm)  # dP/dx

def moving_average(y, k=5):
    """Simple moving average smoothing (odd k recommended)."""
    k = int(k)
    pad = k // 2
    ypad = np.pad(y, (pad, pad), mode="edge")
    return np.convolve(ypad, np.ones(k)/k, mode="valid")

I_smooth = moving_average(I_raw, k=5)  # you can set k=1 to disable smoothing

# Make sure intensity is positive for log-fit (noise can create tiny negatives)
I_pos = np.clip(I_smooth, 1e-12, None)

# -----------------------------
# (c) Estimate beam center x0 from maximum of I(x)
# Then fit I(x) = I0 * exp(-2*(x-x0)^2 / w^2)
#
# Without SciPy, we do:
#  - grid search for x0 around the estimate
#  - for each x0, fit ln(I) = ln(I0) + b*(x-x0)^2  (linear in z=(x-x0)^2)
#    where b = -2/w^2  =>  w = sqrt(-2/b)
# -----------------------------
x0_est = x_mm[np.argmax(I_pos)]

# Use only points near the peak (avoid log of very small values dominated by noise)
threshold = 0.2 * I_pos.max()
mask = I_pos > threshold

def fit_for_x0(x0):
    """Return (rss, I0, w, x0, I_fit) for a given x0. Lower rss is better."""
    z = (x_mm[mask] - x0)**2
    y = np.log(I_pos[mask])

    A = np.column_stack([np.ones_like(z), z])  # y ≈ a + b*z
    (a, b), *_ = np.linalg.lstsq(A, y, rcond=None)

    if b >= 0:  # should be negative for a Gaussian
        return None

    w = math.sqrt(-2.0 / b)
    I0 = math.exp(a)

    I_fit = I0 * np.exp(-2.0 * (x_mm - x0)**2 / (w**2))
    rss = np.mean((I_pos - I_fit)**2)
    return rss, I0, w, x0, I_fit

# Grid search around x0_est
x0_grid = np.linspace(x0_est - 0.2, x0_est + 0.2, 801)
best = None
for x0 in x0_grid:
    res = fit_for_x0(x0)
    if res is None:
        continue
    if best is None or res[0] < best[0]:
        best = res

rss, I0_fit, w_fit, x0_fit, I_fit = best

# -----------------------------
# (d) 1/e^2 diameter and FWHM
# Given in task: FWHM = w * sqrt(2 ln 2)
# (This is the FULL width at half maximum.)
# -----------------------------
diam_1e2 = 2.0 * w_fit
FWHM = w_fit * math.sqrt(2.0 * math.log(2.0))

print(f"Estimated beam center x0 = {x0_fit:.4f} mm")
print(f"Estimated 1/e^2 radius w  = {w_fit:.4f} mm")
print(f"1/e^2 diameter (2w)       = {diam_1e2:.4f} mm")
print(f"FWHM                      = {FWHM:.4f} mm")

# -----------------------------
# (e) Plot P(x) and I(x)
# -----------------------------
plt.figure(figsize=(9, 4))

# Left: P(x)
plt.subplot(1, 2, 1)
plt.plot(x_mm, P_meas, "o", label="P_meas")
plt.plot(x_mm, P_norm, "-", label="P_norm [0..1]")
plt.xlabel("Knife-edge position x (mm)")
plt.ylabel("Power P(x) (a.u.)")
plt.title("Knife-edge cumulative power")
plt.grid(True)
plt.legend()

# Right: I(x)
plt.subplot(1, 2, 2)
plt.plot(x_mm, I_raw, "o-", label="dP/dx (raw)")
plt.plot(x_mm, I_pos, "-", label="dP/dx (smoothed, clipped)")
plt.plot(x_mm, I_fit, "--", label="Gaussian fit")
plt.axvline(x0_fit, linestyle=":", label=f"x0 = {x0_fit:.3f} mm")
plt.xlabel("Position x (mm)")
plt.ylabel("Intensity proxy I(x) (a.u.)")
plt.title(f"Intensity profile (w={w_fit:.3f} mm, FWHM={FWHM:.3f} mm)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
