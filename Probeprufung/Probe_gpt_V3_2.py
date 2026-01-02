import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Given data
# -----------------------------
lambda_nm = np.array([
    1550.0, 1550.5, 1551.0, 1551.5, 1552.0, 1552.5, 1553.0, 1553.5, 1554.0,
    1554.5, 1555.0
])

T = np.array([
    1.004, 0.998, 0.999, 0.961, 0.846, 0.721, 0.787, 0.925, 0.990, 0.998,
    1.003
])

# -----------------------------
# (1) Plot T vs wavelength
# -----------------------------
plt.figure(figsize=(8, 4))
plt.plot(lambda_nm, T, "o-", label="Measured T(λ)")
plt.xlabel("Wavelength λ (nm)")
plt.ylabel("Transmission T (-)")
plt.title("Absorption line: T vs λ")
plt.grid(True)

# -----------------------------
# (2) Line center λ0 = minimum position
# -----------------------------
idx_min = np.argmin(T)
lambda0 = lambda_nm[idx_min]
T_min = T[idx_min]

# Mark the minimum
plt.plot(lambda0, T_min, "ro", label=f"Minimum at λ0={lambda0:.1f} nm")

# -----------------------------
# (3) FWHM via linear interpolation at half depth
# -----------------------------
# Continuum/baseline estimate (simple choice): maximum measured transmission
T_cont = np.max(T)

# Half depth level for an absorption dip
T_half = T_min + 0.5 * (T_cont - T_min)

plt.axhline(T_cont, linestyle="--", linewidth=1, label=f"Baseline T_cont={T_cont:.3f}")
plt.axhline(T_half, linestyle="--", linewidth=1, label=f"Half depth T_half={T_half:.4f}")

def linear_interp_x(x1, y1, x2, y2, y_target):
    """Return x at which the line through (x1,y1)-(x2,y2) reaches y_target."""
    return x1 + (y_target - y1) * (x2 - x1) / (y2 - y1)

# Find left crossing (search from minimum towards smaller wavelengths)
lambda_left = None
for i in range(idx_min - 1, -1, -1):
    y1, y2 = T[i], T[i + 1]
    if (y1 >= T_half and y2 <= T_half) or (y1 <= T_half and y2 >= T_half):
        lambda_left = linear_interp_x(lambda_nm[i], y1, lambda_nm[i + 1], y2, T_half)
        break

# Find right crossing (search from minimum towards larger wavelengths)
lambda_right = None
for i in range(idx_min, len(T) - 1):
    y1, y2 = T[i], T[i + 1]
    if (y1 <= T_half and y2 >= T_half) or (y1 >= T_half and y2 <= T_half):
        lambda_right = linear_interp_x(lambda_nm[i], y1, lambda_nm[i + 1], y2, T_half)
        break

if lambda_left is None or lambda_right is None:
    raise RuntimeError("Could not find both FWHM crossings. Check data / half-depth definition.")

FWHM_nm = lambda_right - lambda_left

# Draw vertical lines for FWHM points
plt.axvline(lambda_left, linestyle=":", linewidth=2, label=f"Left @ {lambda_left:.3f} nm")
plt.axvline(lambda_right, linestyle=":", linewidth=2, label=f"Right @ {lambda_right:.3f} nm")

# -----------------------------
# (4) Coherence length estimate
# Lc ≈ lambda0^2 / Δlambda
# Using nm -> result in nm; convert to mm (1 mm = 1e6 nm)
# -----------------------------
Lc_nm = (lambda0 ** 2) / FWHM_nm
Lc_mm = Lc_nm / 1e6

# -----------------------------
# (5) Bonus: Interference visibility for OPD = 5 mm
# Rule of thumb: clear interference if OPD is not larger than coherence length
# -----------------------------
OPD_mm = 5.0
expect_interference = OPD_mm <= Lc_mm

# Print results
print(f"Line center (minimum): lambda0 = {lambda0:.1f} nm, T_min = {T_min:.3f}")
print(f"Baseline (max):        T_cont = {T_cont:.3f}")
print(f"Half depth level:      T_half = {T_half:.4f}")
print(f"FWHM:                 Δlambda = {FWHM_nm:.3f} nm")
print(f"Coherence length:      Lc ≈ {Lc_mm:.3f} mm")

if expect_interference:
    print(f"Bonus: OPD={OPD_mm:.1f} mm <= Lc -> interference likely still visible.")
else:
    print(f"Bonus: OPD={OPD_mm:.1f} mm  > Lc -> interference contrast will be low (not clear).")

plt.legend(loc="best")
plt.tight_layout()
plt.show()
