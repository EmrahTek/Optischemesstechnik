import numpy as np
import matplotlib.pyplot as plt

Frequenz_Thz = np.array([0.80,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.90], float)

I0_ref = np.array([150, 149,149,148,148, 147,147,146,146,145,145], float)
Ip_prob = np.array([149, 146,141,125,92,78,105,130,140,143,144],float)

c = 3.0e8

T = Ip_prob / I0_ref 

A = 1 - T 

plt.figure(1)
plt.subplot(3,1,1)
plt.plot(Frequenz_Thz, Ip_prob, Frequenz_Thz, I0_ref)
#plt.xlabel('Frequenz (THz)')  # labeling axis
plt.ylabel('Intensität (arb.u.)')  # labeling axis
plt.legend(('Ip', 'I0'))  # Plot Legend from all Plots


plt.subplot(3,1,2)
plt.plot(Frequenz_Thz, T)
#plt.xlabel('Frequenz (THz)')  # labeling axis
plt.ylabel('Transmission')  # labeling axis
plt.ylim(-0.1, 1.1)


plt.subplot(3, 1, 3)
plt.plot(Frequenz_Thz, A)  # plot parameters
plt.xlabel('Frequenz (THz)')  # labeling axis
plt.ylabel('Absorption')  # labeling axis
plt.ylim(-0.1, 1.1)

plt.show()