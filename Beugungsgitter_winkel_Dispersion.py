import numpy as np
import matplotlib.pyplot as plt

# Given parameters (nm,degrees)
lam1 = 633.0
lam2 = 633.2
phi_i_list_deg = [0.0, 20.0]

# Grating constant range ( nm)
g = np.linspace(800.0,4000.0,2000)

plt.figure()

for phi_i_deg in  phi_i_list_deg:
    phi_i = np.deg2rad(phi_i_deg)

    # arcsin argument; valid only where <= 1
    arg1 = lam1 / g + np.sin(phi_i)
    arg2 = lam2 / g + np.sin(phi_i)
    valid = (arg1 <= 1.0) & (arg2 <= 1.0)

    phi1 = np.full_like(g, np.nan, dtype=float)
    phi2 = np.full_like(g, np.nan, dtype=float)
    phi1[valid] = np.arcsin(arg1[valid])
    phi2[valid] = np.arcsin(arg2[valid])

    dphi_deg = np.rad2deg(phi2 - phi1)

    plt.semilogy(g[valid], dphi_deg[valid], label=f"phi_i = {phi_i_deg:.0f}°")
    # Task d) (only for phi_i = 20°)
    if abs(phi_i_deg - 20.0) < 1e-9:
        mask = valid & (dphi_deg >= 0.02)
        g_min = g[mask][0] if np.any(mask) else np.nan
        print(f"Minimum g for Δphi >= 0.02° at phi_i=20°: {g_min:.1f} nm")
plt.xlabel("g (nm)")
plt.ylabel("Δphi (deg)")
plt.legend()
plt.tight_layout()
plt.show()