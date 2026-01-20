import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Given measurement data
# -----------------------------
lambda_nm = np.array([450,460,470,480,490,500,510,520,530,540,550,560,570], dtype=float)

I_dark   = np.array([12,12,12,12,12,12,12,12,12,12,12,12,12], dtype=float)
I_ref    = np.array([1020,1035,1048,1055,1050,1030,1010,990,980,975,980,995,1010], dtype=float)
I_sample = np.array([650,670,690,710,720,680,500,320,280,300,420,560,620], dtype=float)

# Beer-Lambert parameters
epsilon = 1.8e4   # molar decadic extinction coefficient [L/(mol*cm)]
l_cm = 1.0        # path length [cm]

# -----------------------------
# 1) Transmission T(lambda)
#    T is dimensionless
# -----------------------------
den = (I_ref - I_dark) # denominator (payda)
num = (I_sample - I_dark) # numerator (pay)

# Safety: avoid division by zero (shouldn't happen with given data)
if np.any(den <= 0): # bir dizideki koşulun en az bir eleman için True olup olmadığını kontrol eder
    raise ValueError("Invalid reference data: (I_ref - I_dark) must be > 0 for all wavelengths.")

T = num / den

# Safety: Transmission must be > 0 for log10
if np.any(T <= 0):
    raise ValueError("Invalid transmission: T(λ) must be > 0 to compute absorbance.")

# -----------------------------
# 2) Absorbance A(lambda) = -log10(T)
#    A is dimensionless
# -----------------------------
A = -np.log10(T)

# -----------------------------
# 3) Find lambda_max and A_max
# -----------------------------
idx_max = np.argmax(A)
lambda_max_nm = lambda_nm[idx_max]   # [nm]
A_max = A[idx_max]                   # [-]

# -----------------------------
# 4) Estimate concentration via Beer-Lambert: A = ε * c * l
#    ε: [L/(mol*cm)], l: [cm]  => c: [mol/L]
# -----------------------------
c_mol_per_L = A_max / (epsilon * l_cm)

print(f"lambda_max = {lambda_max_nm:.1f} nm")
print(f"A_max      = {A_max:.4f} (-)")
print(f"Estimated concentration c = {c_mol_per_L:.3e} mol/L")

# -----------------------------
# 5) Plot A(lambda) and mark lambda_max
# -----------------------------
plt.figure()
plt.plot(lambda_nm, A, marker="o", label="A(λ) = -log10(T(λ))")
plt.axvline(lambda_max_nm, linestyle="--", label=f"λ_max = {lambda_max_nm:.0f} nm")
plt.scatter([lambda_max_nm], [A_max], zorder=3, label=f"A_max = {A_max:.3f}")

plt.xlabel("Wavelength λ [nm]")
plt.ylabel("Absorbance A [–]")
plt.title("Absorption spectrum")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
