
# include essential Mathematical libraries
import numpy as np  # adds essential mathematical functions and handling with arrays like known from Matlab
import matplotlib.pyplot as plt  # adds 2D plot functions
from pathlib import Path

ref_path = Path("/home/emrahtek/Schreibtisch/CodeLab/Optischmesstechnik_1/A_16_Transmission_Absorption/I0.txt")
ref_data = np.loadtxt(ref_path)

sam_path = Path("/home/emrahtek/Schreibtisch/CodeLab/Optischmesstechnik_1/A_16_Transmission_Absorption/Ip.txt")
sam_data = np.loadtxt(sam_path)




# define variables
Frequenzachse = ref_data[:, 0]
I0 = ref_data[:, 1]
Ip = sam_data[:, 1]

# calculations
T = Ip / I0
A = 1 - T

plt.figure(1)
plt.subplot(3, 1, 1)
plt.plot(Frequenzachse, Ip, Frequenzachse, I0)  # plot parameters
#plt.xlabel('Frequenz (THz)')  # labeling axis
plt.ylabel('Intensität (arb.u.)')  # labeling axis
plt.legend(('Ip', 'I0'))  # Plot Legend from all Plots

plt.subplot(3, 1, 2)
plt.plot(Frequenzachse, T)  # plot parameters
#plt.xlabel('Frequenz (THz)')  # labeling axis
plt.ylabel('Transmission')  # labeling axis
plt.ylim(-0.1, 1.1)

plt.subplot(3, 1, 3)
plt.plot(Frequenzachse, A)  # plot parameters
plt.xlabel('Frequenz (THz)')  # labeling axis
plt.ylabel('Absorption')  # labeling axis
plt.ylim(-0.1, 1.1)

plt.show()
