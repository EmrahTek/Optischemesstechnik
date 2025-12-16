import numpy as np
import matplotlib.pyplot as plt
import mplcursors

x = np.linspace(0,250,251)

mu = 127
sigma_1 = 7
sigma_2 = 4.5
sigma_3 = 1.5

gaus_1 = (1 / (sigma_1* np.sqrt(2*np.pi))) * (np.exp(-(x - mu)**2 / (2*sigma_1**2) ))
gaus_2 = (1 / (sigma_2* np.sqrt(2*np.pi))) * (np.exp(-(x - mu)**2 / (2*sigma_2**2) ))
gaus_3 = (1 / (sigma_3* np.sqrt(2*np.pi))) * (np.exp(-(x - mu)**2 / (2*sigma_3**2) ))



fig,ax = plt.subplots()
fig.tight_layout()


plt.plot(x,gaus_1,x,gaus_2,x,gaus_3, linewidth  = 2)
plt.title("Normal Verteilung Gauss")
plt.xlabel("0-250 mmHG")
plt.ylabel("Gaus funktion")
plt.grid()
plt.legend()
#lines = ax.plot(x,gaus_1,x,gaus_2,x,gaus_3, linewidth  = 2)
#mplcursors.cursor(lines)

plt.show()