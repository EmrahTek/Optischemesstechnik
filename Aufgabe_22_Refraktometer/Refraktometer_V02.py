import numpy as np
import matplotlib.pyplot as plt

n_Deckplatte = 1.458

SaccharoseAnteil = np.linspace(0, 80, 9)
n_Saccharose = np.array([1.33299, 1.34783,
1.36384, 1.38115, 1.39986, 1.42009, 1.44193,
1.46546, 1.49071])
theta_c = 180 / np.pi * np.arcsin(
np.clip(n_Saccharose / n_Deckplatte, 0, 1))

plt.figure(1)
plt.plot(SaccharoseAnteil, theta_c, '-o', linewidth = 2)
plt.xlabel('Saccharose Anteil (%)')
plt.ylabel('kritischer Winkel (deg)')
plt.show() 