import numpy as np
import matplotlib.pyplot as plt

# Veriler (1σ belirsizlik)
l0, dl = 1.00, 0.05   # m
T0, dT = 2.0, 0.2     # s

def g_pendel(l, T):
    return 4 * np.pi**2 * l / (T**2)

# Monte-Carlo
N = 200_000
rng = np.random.default_rng(0)

L  = rng.normal(l0, dl, N)
TT = rng.normal(T0, dT, N)

g = g_pendel(L, TT)

g_mean = g.mean()
g_std  = g.std(ddof=1)          # 1σ
p2_5, p97_5 = np.percentile(g, [2.5, 97.5])

print(f"g = {g_mean:.3f} ± {g_std:.3f} m/s^2 (1σ)")
print(f"95% Intervall: [{p2_5:.3f}, {p97_5:.3f}] m/s^2")

# Histogram
plt.figure()
plt.hist(g, bins=60, density=True)
plt.axvline(g_mean, linestyle="--", label="mean")
plt.axvline(g_mean - g_std, linestyle=":", label="mean ± 1σ")
plt.axvline(g_mean + g_std, linestyle=":")
plt.xlabel("g [m/s²]")
plt.ylabel("Dichte")
plt.title("Monte-Carlo Verteilung von g")
plt.legend()
plt.show()
