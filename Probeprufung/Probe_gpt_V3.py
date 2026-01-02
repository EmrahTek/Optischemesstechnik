"""
(1) Plotten Sie T gegen λ. 
(2) Bestimmen Sie die Linienmitte λ0 als Position des Minimums. 
(3) Bestimmen Sie die Halbwertsbreite FWHM der Absorptionslinie über lineare Interpolation an der halben Tiefe. 
(4) Schätzen Sie aus FWHM eine Kohärenzlänge Lc ≈ λ0^2/∆λ und geben Sie Lc in mm an. 
(5) Bonus: Würden Sie bei einer optischen Wegdifferenz von 5 mm noch deutliche Interferenz erwarten? Begründen Sie kurz.

"""
import numpy as np
import matplotlib.pyplot as plt

lambda_nm = np.array([
1550.0, 1550.5, 1551.0, 1551.5, 1552.0, 1552.5, 1553.0, 1553.5, 1554.0,
1554.5, 1555.0
])

T = np.array([
1.004, 0.998, 0.999, 0.961, 0.846, 0.721, 0.787, 0.925, 0.990, 0.998,
1.003
])

# (2) Linienmitte (Minimum)
i0 = np.argmin(T)
lambda0 = lambda_nm[i0]
Tmin = T[i0]

# (3) FWHM via halbe Tiefe (baseline ~ max)
baseline = np.max(T)
depth = baseline - Tmin
half = Tmin + depth/2

# linke Halbwertstelle (Interpolation)
lambda_left = None
for i in range(i0, 0, -1):
    if T[i-1] > half and T[i] <= half:
        x1, x2 = lambda_nm[i-1], lambda_nm[i]
        y1, y2 = T[i-1], T[i]
        lambda_left = x1 + (half - y1) * (x2 - x1) / (y2 - y1)
        break

# rechte Halbwertstelle (Interpolation)
lambda_right = None
for i in range(i0, len(T)-1):
    if T[i] <= half and T[i+1] > half:
        x1, x2 = lambda_nm[i], lambda_nm[i+1]
        y1, y2 = T[i], T[i+1]
        lambda_right = x1 + (half - y1) * (x2 - x1) / (y2 - y1)
        break


FWHM = lambda_right - lambda_left

# (4) Kohärenzlänge Lc ~ lambda0^2 / Delta_lambda
Lc_m = (lambda0*1e-9)**2 / (FWHM*1e-9)
Lc_mm = 1e3 * Lc_m
print("lambda0 =", lambda0, "nm")
print("FWHM =", FWHM, "nm")
print("Lc =", Lc_mm, "mm")

# Plot
plt.figure()
plt.plot(lambda_nm, T, "o-", label="Messdaten")
plt.axvline(lambda0, linestyle="--", label="lambda0")
plt.axhline(half, linestyle=":", label="halbe Tiefe")
plt.axvline(lambda_left, linestyle=":")
plt.axvline(lambda_right, linestyle=":")
plt.xlabel("Wellenlänge lambda (nm)")
plt.ylabel("Transmission T")
plt.grid(True)
plt.legend()
plt.show()