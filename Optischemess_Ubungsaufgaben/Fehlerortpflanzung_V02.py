import numpy as np
import matplotlib.pyplot as plt

# Given measurements (mean ± 1σ)
g_mean, g_std = 0.300, 0.002
b_mean, b_std = 0.450, 0.003

# a) Focal length
f_analytic = g_mean * b_mean / (g_mean + b_mean)

# b) Gaussian error propagation
df_dg = b_mean**2 / (g_mean + b_mean)**2
df_db = g_mean**2 / (g_mean + b_mean)**2
sigma_f_gauss = np.sqrt((df_dg * g_std)**2 + (df_db * b_std)**2)

# c) Monte Carlo
N = 200_000
rng = np.random.default_rng(0)

g_samples = rng.normal(g_mean, g_std, N)
b_samples = rng.normal(b_mean, b_std, N)

f_samples = g_samples * b_samples / (g_samples + b_samples)

f_mc_mean = f_samples.mean()
f_mc_std  = f_samples.std(ddof=1)

print(f"Analytic f      = {f_analytic:.6f} m  ({f_analytic*1000:.2f} mm)")
print(f"Gauss Δf        = {sigma_f_gauss:.6f} m  ({sigma_f_gauss*1000:.3f} mm)")
print(f"MC mean(f)      = {f_mc_mean:.6f} m  ({f_mc_mean*1000:.2f} mm)")
print(f"MC std(f)       = {f_mc_std:.6f} m  ({f_mc_std*1000:.3f} mm)")

# ---- Plot: Histogram of f (in mm) ----
f_mm = f_samples * 1000
plt.figure()
plt.hist(f_mm, bins=80, density=True)

# Vertical lines: analytic and MC mean
plt.axvline(f_analytic*1000, linestyle="--", label="Analytic f")
plt.axvline(f_mc_mean*1000, linestyle="-.", label="MC mean")

# ±1σ lines (MC)
plt.axvline((f_mc_mean - f_mc_std)*1000, linestyle=":", label="MC mean ± 1σ")
plt.axvline((f_mc_mean + f_mc_std)*1000, linestyle=":")

plt.xlabel("f [mm]")
plt.ylabel("Probability density")
plt.title("Monte Carlo distribution of focal length f")
plt.legend()
plt.show()
