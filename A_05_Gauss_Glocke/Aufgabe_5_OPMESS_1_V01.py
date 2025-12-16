import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Parameters
mu = 127   # mean (ortalama)
sigma = 7  # standard deviation (standart sapma)

# x-axis from 0 to 250
x = np.linspace(0, 250, 1000)

# Normal distribution PDF
pdf = norm.pdf(x, mu, sigma)

# Plot original curve
plt.plot(x, pdf, label=f"σ = {sigma}", color="blue")

# Plot when sigma is halved
pdf_half = norm.pdf(x, mu, sigma/2)
plt.plot(x, pdf_half, label=f"σ = {sigma/2}", color="red")

# Plot when sigma is doubled
pdf_double = norm.pdf(x, mu, sigma*2)
plt.plot(x, pdf_double, label=f"σ = {sigma*2}", color="green")

# Mark probability at x=140
value = 140
probability = norm.pdf(value, mu, sigma)
plt.scatter(value, probability, color="black", zorder=5)
plt.text(value+2, probability, f"P(140)={probability:.5f}", fontsize=9)

# Plot settings
plt.title("Gaussian (Normal) Distribution")
plt.xlabel("Blood Pressure (mmHg)")
plt.ylabel("Probability Density")
plt.legend()
plt.grid()
plt.show()
