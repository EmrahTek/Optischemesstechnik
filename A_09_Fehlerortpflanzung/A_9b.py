# Programm:         Aufgabe 9.b Optische Messtechnik
# Author:           Ursin Solèr
# Organisation:     FHGR Photonics
# Version:          1.0
# Date:             30.09.2025
# History:          1.0 main

# include essential Mathematical libraries
import numpy as np
import matplotlib.pylab as plt

l = np.random.normal(1.00, 0.05, size=10000)
T = np.random.normal(2.0,  0.2,  size=10000)

g = 4 * np.pi**2 * l / (T**2)
print(f"Erdbeschleunigung: {np.mean(g)}+/-{np.sqrt(np.var(g))}")

plt.hist(g)
plt.show()


from mcerp import N

l = N(1.00, 0.05)  # l = 1.00+/-0.05
T = N(2.0, 0.2)    # T = 2.0+/-0.2

g = 4 * np.pi**2 * l / (T**2)
print(f"Erdbeschleunigung: {g.mean}+/-{g.std}")
g.describe()  # Skewness ~1 bedeutet, dass es keine Normalverteilung mehr ist

#g.plot()
#plt.show()