import numpy as np
import matplotlib.pyplot as plt
 
d_mm = np.array([25.12,25.08,25.15,25.10,25.09,25.13,25.11,25.07,25.16, 25.12,25.14,25.09,15.10,25.11,25.08, 
                 25.13,25.12,25.09,25.15,25.10], float)

# Mittelwert, Standartabweichung(ddof=1), Standardfehler

N = len(d_mm)
d_mean = np.mean(d_mm)
d_s = np.std(d_mm,ddof=1) # Standardabweichung

se = d_s / np.sqrt(N) # Standardfehler


t = 2.093 # t_(0.975, 19)
ci_low = d_mean - t*se
ci_high = d_mean + t*se

print(f"N = {N}")
print(f"Mean (x) = {d_mean:.3f} mm")
print(f"Sample std dev (deltaX) = {d_s:.3f} mm")
print(f"Standard error (deltaX) = {se:.3f} mm")
print(f"95% CI = [{ci_low:.3f}, {ci_high:.3f}] mm")


plt.hist(d_mm, bins=8)
plt.axvline(d_mean, linestyle='--', label='mean')
plt.axvline(ci_low, linestyle=':', label='95% CI')
plt.axvline(ci_high, linestyle=':')
plt.xlabel("d [mm]")
plt.ylabel("count")
plt.legend()
plt.show()


