import numpy as np

# Data sind from File
data = np.array([125,129,140,121,127], dtype=float)
# Number of measurements N
N = data.size

# Mean value x̄ = (1/N) * sum(x_i)
xbar = np.mean(data)

# Sample standard deviation (formula with N-1 in the denominator)
# Δx = sqrt( (1/(N-1)) * Σ (x_i - x̄)^2 ) 
s = np.std(data, ddof=1) # standatabweichungen

# Standard error of the mean: Δx̄ = Δx / sqrt(N)
se = s / np.sqrt(N)

print(f"N = {N}")
print(f"Mean (x) = {xbar:.3f} mmHG")
print(f"Sample std dev (deltaX) = {s:.3f} mmHg")
print(f"Standard error (deltaX) = {se:.3f} mmHg")


# --- Part 2: How many measurements are needed so that the standard error is 10% of a single-measurement error? ---
# We assume the single-measurement error is characterized by Δx (the standard deviation).
# Requirement: Δx̄ = 0.1 * Δx ⇒ Δx / sqrt(N_needed) = 0.1 * Δx ⇒ 1/sqrt(N_needed) = 0.1
# Therefore: sqrt(N_needed) = 10 ⇒ N_needed = 100
ratio = 0.10
N_needed = int(np.ceil((1/ratio**2)))
print(f"Measurements needed for Δx̄ = 10% of single-measurement error: N = {N_needed}")
# np.ceil()  --> her eleman icin yukariya dogru yuvarlanmis deger. 
