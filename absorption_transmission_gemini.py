import numpy as np
import matplotlib.pyplot as plt

# Gegebene Messdaten
lambda_nm = np.array([450,460,470,480,490,500,510,520,530,540,550,560,570], dtype=float)
I_dark   = np.array([12,12,12,12,12,12,12,12,12,12,12,12,12], dtype=float)
I_ref    = np.array([1020,1035,1048,1055,1050,1030,1010,990,980,975,980,995,1010], dtype=float)
I_sample = np.array([650,670,690,710,720,680,500,320,280,300,420,560,620], dtype=float)

epsilon = 1.8e4  # L/(mol*cm)
l_cm = 1.0       # cm

# Aufgabenbearbeitung:
# 1) Transmission T(lambda)
T = (I_sample - I_dark) / (I_ref - I_dark)

# 2) Absorbanz A(lambda)
A = -np.log10(T)

# 3) Wellenlänge lambda_max bei maximaler Absorbanz
idx_max = np.argmax(A)
lambda_max = lambda_nm[idx_max]
A_max = A[idx_max]

# 4) Konzentration c über Beer-Lambert: A = epsilon * c * l
c = A_max / (epsilon * l_cm)

# 5) Plotten von A(lambda)
plt.figure(figsize=(8, 5))
plt.plot(lambda_nm, A, 'gs-', label='Absorbanz $A(\lambda)$')
plt.plot(lambda_max, A_max, 'ro', label=f'$\lambda_{{max}}$ = {lambda_max} nm')

plt.xlabel('Wellenlänge $\lambda$ (nm)')
plt.ylabel('Absorbanz $A$')
plt.title('Absorptionsspektrum')
plt.legend()
plt.grid(True)
plt.show()

print(f"Ergebnisse der Spektralanalyse:")
print(f"Maximale Absorbanz A_max: {A_max:.4f} bei {lambda_max} nm")
print(f"Berechnete Konzentration: {c:.2e} mol/L")