import numpy as np
import matplotlib.pyplot as plt

# Parametreler
lam0_nm = 532.0         # merkez dalga boyu (nm)
dlam_nm = 0.02          # iki mod aralığı (nm)
phi_i_deg = 0.0         # giriş açısı
f_mm = 100.0            # odak uzaklığı (mm)
grooves = [300, 600, 1200, 1800]  # çizgi/mm seçenekleri

phi_i = np.deg2rad(phi_i_deg)
lam = lam0_nm * 1e-9

def phi_and_dispersion(lines_per_mm, lam_m):
    g = 1e-3 / lines_per_mm          # m/oluk
    s = lam_m / g + np.sin(phi_i)
    s = np.clip(s, -1, 1)
    phi = np.arcsin(s)
    D = 1.0 / (g * np.cos(phi))      # dphi/dlam (rad/m)
    return phi, D

f = f_mm / 1000.0

print("lines/mm | phi(deg) | dphi/dlam (rad/nm) | delta_x (um) for dlam=%.3f nm" % dlam_nm)
for L in grooves:
    phi, D = phi_and_dispersion(L, lam)
    D_nm = D * 1e-9
    dx_m = f * D_nm * dlam_nm
    print(f"{L:7d} | {np.degrees(phi):8.3f} | {D_nm:15.6e} | {dx_m*1e6:10.3f}")

# Dispersiyon grafiği
lams = np.linspace(lam0_nm-1, lam0_nm+1, 400)*1e-9
plt.figure()
for L in grooves:
    phis = [phi_and_dispersion(L, Lm)[0] for Lm in lams]
    plt.plot(lams*1e9, np.degrees(phis), label=f"{L} l/mm")
plt.xlabel("Dalga boyu (nm)")
plt.ylabel("Kırınım açısı φ (deg)")
plt.title("1. Mertebe: φ(λ) — Gitter denklemi")
plt.legend(); plt.tight_layout(); plt.show()
