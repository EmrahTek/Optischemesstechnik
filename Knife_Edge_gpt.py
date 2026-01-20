"""
Der folgende Python-Code (NumPy + Matplotlib) ruft die Knife-Edge-Daten ab, 
zeichnet T(x), berechnet das normalisierte Strahlprofil aus I(x) ∝ dT/dx und 
berechnet den Strahldurchmesser (2w) mit FWHM und 1/e², den er dann in die Konsole schreibt.

Autor: Emrah Tekin


"""


import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# 1) Measurement data (x in mm, T dimensionless)
# ---------------------------
x_mm = np.array([
    -2.00, -1.80, -1.60, -1.40, -1.20, -1.00, -0.80, -0.60, -0.40, -0.20,
     0.00,  0.20,  0.40,  0.60,  0.80,  1.00,  1.20,  1.40,  1.60,  1.80,  2.00
], dtype=float)

T = np.array([
    0.000, 0.001, 0.004, 0.010, 0.023, 0.048, 0.091, 0.159, 0.252, 0.369,
    0.500, 0.631, 0.748, 0.841, 0.909, 0.952, 0.977, 0.990, 0.996, 0.999, 1.000
], dtype=float)

# ---------------------------
# 2) Intensity profile from numerical derivative: I(x) ∝ dT/dx
#    Units: dT/dx -> 1/mm (because T is dimensionless, x in mm)
# ---------------------------
dTdx = np.gradient(T,x_mm)      # derivative wrt x [1/mm]
I_raw = np.clip(dTdx, 0.0, None) # avoid tiny negative values from numerics
I = I_raw / I_raw.max()         # normalize to max = 1(dimensionless)

# ---------------------------
# Helper: FWHM from half-maximum crossings (linear interpolation)
# ---------------------------
def fwhm_from_profile(x,y,half = 0.5):
    """
    x: position array (mm)
    y: normalized profile (max ~ 1)
    returns: (FWHM, x_left, x_right) in mm
    """
    # indices where y >= half
    idx = np.where (y >= half)[0]
    if idx.size < 2:
        raise ValueError("Half -maximum not crossed properly; cannot compute FWHM.")
    
    i_left = idx[0]
    i_right = idx[-1]

    #Left crossing between i_left - 1 and i_left (if possible)
    if i_left == 0:
        x_left = x[0]
    else:
        x1, y1 = x[i_left - 1], y[i_left - 1]
        x2, y2 = x[i_left],     y[i_left]
        x_left = x1 + (half - y1) * (x2 - x1) / (y2 - y1)

    # Right crossing between i_right and i_right+1 (if possible)
    if i_right == len(x) - 1:
        x_right = x[-1]
    else:
        x1, y1 = x[i_right],     y[i_right]
        x2, y2 = x[i_right + 1], y[i_right + 1]
        x_right = x1 + (half - y1) * (x2 - x1) / (y2 - y1)

    return (x_right - x_left), x_left, x_right

# ---------------------------
# 3) Compute FWHM and 1/e^2 diameter (Gaussian assumption)
#    Given: I(x) = I0 * exp(-2 x^2 / w^2)
#           FWHM = w * sqrt(2 ln 2)
#           diameter (1/e^2) = 2w
# ---------------------------

FWHM_mm ,xL_mm, xR_mm = fwhm_from_profile(x_mm, I, half = 0.5)

w_mm = FWHM_mm / np.sqrt(2.0*np.log(2.0))
diameter_mm = 2.0*w_mm

print(f"FWHM ≈ {FWHM_mm:.4f} mm")
print(f"1/e^2 beam diameter (2w) ≈ {diameter_mm:.4f} mm")

# ---------------------------
# 4) Plot: two horizontal subplots
# ---------------------------
fig, ax = plt.subplots(1, 2, figsize=(11, 4), sharex=False)

# Left: T(x) vs x
ax[0].plot(x_mm, T, marker="o", label="T(x)")
ax[0].set_xlabel("x [mm]")
ax[0].set_ylabel("T [–]")
ax[0].set_title("Knife-edge transmission")
ax[0].grid(True)
ax[0].legend()

# Right: normalized intensity profile I(x)
ax[1].plot(x_mm, I, marker="o", label="I(x) ∝ dT/dx (norm.)")
ax[1].axhline(0.5, linestyle="--", label="Half max (0.5)")
ax[1].axvline(xL_mm, linestyle="--")
ax[1].axvline(xR_mm, linestyle="--")

ax[1].set_xlabel("x [mm]")
ax[1].set_ylabel("I [–] (normalized)")
ax[1].set_title("Reconstructed beam profile")
ax[1].grid(True)
ax[1].legend()

plt.tight_layout()
plt.show()