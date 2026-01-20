import numpy as np
import matplotlib.pyplot as plt

# 1) Messdaten als Arrays anlegen
x = np.array([-2.00, -1.80, -1.60, -1.40, -1.20, -1.00, -0.80, -0.60, -0.40, -0.20, 
               0.00,  0.20,  0.40,  0.60,  0.80,  1.00,  1.20,  1.40,  1.60,  1.80,  2.00], dtype=float)

T = np.array([0.000, 0.001, 0.004, 0.010, 0.023, 0.048, 0.091, 0.159, 0.252, 0.369, 
               0.500, 0.631, 0.748, 0.841, 0.909, 0.952, 0.977, 0.990, 0.996, 0.999, 1.000], dtype=float)

# 2) Berechnung des Intensitätsprofils I(x)
# Die Intensität ist proportional zur Ableitung der Transmission: I(x) ~ dT/dx
I_raw = np.gradient(T,x)
I_norm = I_raw / np.max(I_raw) # Normierung auf 1


# 3) Bestimmung von FWHM und 1/e^2-Strahldurchmesser
# FWHM näherungsweise bestimmen (Breite bei halbem Maximum)
indices_above_half = np.where(I_norm >= 0.5)[0]
fwhm = x[indices_above_half[-1]] - x[indices_above_half[0]]

# Berechnung des Strahlradius w und Durchmessers D basierend auf Gauß-Annahme
# Formeln laut Hinweis: FWHM = w * sqrt(2 * ln 2)
w = fwhm / np.sqrt(2*np.log(2))
diameter = 2*w

# 4) Visualisierung und Ausgabe
fig, (ax1,ax2) = plt.subplots(1,2, figsize=(12,5))

# Linker Plot: Transmission T(x)
ax1.plot(x, T, 'bo-', label='Messdaten $T(x)$')
ax1.set_xlabel('Position $x$ (mm)')
ax1.set_ylabel('Normierte Transmission $T$ (-)')
ax1.set_title('Knife-Edge Transmission')
ax1.grid(True)
ax1.legend()

# Rechter Plot: Intensitätsprofil I(x)
ax2.plot(x, I_norm, 'ro-', label='Intensität $I(x) \propto dT/dx$')
ax2.axhline(0.5, color='black', linestyle='--', label='Halbwertsbreite (0.5)')
ax2.set_xlabel('Position $x$ (mm)')
ax2.set_ylabel('Normierte Intensität $I$ (-)')
ax2.set_title('Berechnetes Strahlprofil')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()

# Ausgabe der Ergebnisse in der Konsole
print(f"--- Strahlprofil-Auswertung ---")
print(f"FWHM:         {fwhm:.3f} mm")
print(f"Radius w:     {w:.3f} mm")
print(f"Durchmesser:  {diameter:.3f} mm")
