import numpy as np
g, sg = 0.300, 0.002
b, sb = 0.450, 0.003
f = g*b/(g+b)
df_dg = b**2/(g+b)**2
df_db = g**2/(g+b)**2
sf = np.sqrt((df_dg*sg)**2 + (df_db*sb)**2)
print(f"f = {f:.6f} m")
print(f"∆f (Gauss) = {sf:.6f} m")
rng = np.random.default_rng(42)
M = 200000
g_s = rng.normal(g, sg, M)
b_s = rng.normal(b, sb, M)
f_s = g_s*b_s/(g_s+b_s)
print(f"f_MC mean = {f_s.mean():.6f} m")
print(f"f_MC std = {f_s.std(ddof=1):.6f} m")