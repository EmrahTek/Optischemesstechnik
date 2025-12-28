import numpy as np
import math

data = np.array([125,129,140,121,127], dtype=float)
summe = 0.0

try:
    for wert in data:
        summe+=wert
    result = summe / len(data)
    print("Mittelwert : ", result)

except:
    print("Können Sie bitte richtig machen! ")
    
N = data.size
xbar = np.mean(data)
s=np.std(data,ddof=1)
se = s / np.sqrt(N)

print(f"N = {N}")
print(f"Mean (x) = {xbar:.3f} mmHG")
print(f"Sample std dev (deltaX) = {s:.3f} mmHg")
print(f"Standard error (deltaX) = {se:.3f} mmHg")

ratio = 0.10
N_needed = int(np.ceil((1/ratio**2)))
print(f"Measurements needed for Δx̄ = 10% of single-measurement error: N = {N_needed}")

