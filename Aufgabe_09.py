import numpy as np

l, Dl = 1.00, 0.05   # m
T, DT = 2.0, 0.2     # s

g = 4*np.pi**2 * l / T**2

dg_dl = 4*np.pi**2 / T**2
dg_dT = -8*np.pi**2 * l / T**3

Dg = np.sqrt((dg_dl*Dl)**2 + (dg_dT*DT)**2)

print(f"g = {g:.3f} ± {Dg:.3f} m/s^2")  # -> 9.870 ± 2.035

