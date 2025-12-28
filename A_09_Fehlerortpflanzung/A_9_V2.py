import numpy as np
from uncertainties import ufloat

# Veriler (1σ belirsizlik)
l0, dl = 1.00, 0.05   # m
T0, dT = 2.0, 0.2     # s

# Model
def g_pendel(l, T):
    return 4 * np.pi**2 * l / (T**2)

# --- Gauss (lineer) hata yayılımı: uncertainties ---
l = ufloat(l0, dl)
T = ufloat(T0, dT)
g_u = g_pendel(l, T)
print("Gauss/uncertainties:", g_u)        # örn: 9.87+/-2.04
print(f"g = {g_u:.3f} m/s^2 (1σ)")

# --- Monte-Carlo (mcerp yerine) ---
N = 200_000
rng = np.random.default_rng(0)

L = rng.normal(l0, dl, N)
TT = rng.normal(T0, dT, N)

g_mc = g_pendel(L, TT)

print(f"MC mean = {g_mc.mean():.3f} m/s^2")
print(f"MC std  = {g_mc.std(ddof=1):.3f} m/s^2 (1σ)")
p2_5, p97_5 = np.percentile(g_mc, [2.5, 97.5])
print(f"MC 95% interval = [{p2_5:.3f}, {p97_5:.3f}] m/s^2")
