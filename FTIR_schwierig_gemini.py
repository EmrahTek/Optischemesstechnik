import numpy as np
import matplotlib.pyplot as plt

# 1) Messdaten anlegen
x = np.array([-2.00, -1.80, -1.60, -1.40, -1.20, -1.00, -0.80, -0.60, -0.40, -0.20, 
               0.00,  0.20,  0.40,  0.60,  0.80,  1.00,  1.20,  1.40,  1.60,  1.80,  2.00])
T = np.array([0.000, 0.001, 0.004, 0.010, 0.023, 0.048, 0.091, 0.159, 0.252, 0.369, 
               0.500, 0.631, 0.748, 0.841, 0.909, 0.952, 0.977, 0.990, 0.996, 0.999, 1.000])

# 2) Intensitätsprofil I(x) berechnen (numerische Ableitung)
I = np.gradient(T, x)
I_norm = I / np.max(I)  # Normierung auf Maximum

# 3) Bestimmung von FWHM und 1/e^2-Durchmesser
# Näherungsweise Bestimmung der Breite bei halbem Maximum (FWHM)
mask = I_norm >= 0.5
fwhm = x[mask][-1] - x[mask][0]

# Berechnung des Strahlradius w und Durchmessers D
w = fwhm / np.sqrt(2 * np.log(2))
diameter = 2 * w

# 4) Visualisierung
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(x, T, 'bo-', label='Messdaten $T(x)$')
ax1.set_title('Transmission $T(x)$')
ax1.set_xlabel('Position $x$ (mm)')
ax1.grid(True)

ax2.plot(x, I_norm, 'ro-', label='Intensität $I(x)$')
ax2.axhline(0.5, color='black', linestyle='--', label='FWHM-Grenze')
ax2.set_title('Normiertes Intensitätsprofil $I(x)$')
ax2.set_xlabel('Position $x$ (mm)')
ax2.grid(True)

plt.tight_layout()
plt.show()

print(f"FWHM: {fwhm:.3f} mm")
print(f"1/e^2-Strahldurchmesser: {diameter:.3f} mm")