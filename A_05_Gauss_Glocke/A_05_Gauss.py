import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0, 250, 251)
mu = 127
sigma1 = 7
Gauss1 = 1/(sigma1 * np.sqrt(2 * np.pi)) * \
np.exp(-(x-mu)**2 / (2 * sigma1 ** 2))
sigma2 = 3.5
Gauss2 = 1/(sigma2 * np.sqrt(2 * np.pi)) * \
np.exp(-(x-mu)**2 / (2 * sigma2 ** 2))
sigma3 = 14
Gauss3 = 1/(sigma3 * np.sqrt(2 * np.pi)) * \
np.exp(-(x-mu)**2 / (2 * sigma3 ** 2))
plt.plot(x, Gauss1, x, Gauss2, x, Gauss3, linewidth=2)
plt.xlabel('Blutdruck (mmHg)')
plt.ylabel('Verteilung')
plt.legend((r'$\sigma = 7$',r'$\sigma = 3.5$',r'$\sigma = 14$'))
plt.show()