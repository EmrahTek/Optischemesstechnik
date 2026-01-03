import numpy as np
import matplotlib.pyplot as plt
f = np.array([0.80, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.90])
I0 = np.array([150, 149, 149, 148, 148, 147, 147, 146, 146, 145, 145])
Ip = np.array([149, 146, 141, 125, 92, 78, 105, 130, 140, 143, 144])
T = Ip / I0
A = 1 - T
plt.figure()
plt.subplot(1, 2, 1)
plt.plot(f, I0, marker='o')
plt.plot(f, Ip, marker='o')
plt.xlabel('Frequenz (THz)')
plt.ylabel('Intensität (arb.u.)')
plt.legend(['Referenzmessung', 'Probenmessung'])
plt.ylim([0.9 * min(Ip), 1.1 * max(I0)])
plt.subplot(1, 2, 2)
plt.plot(f, T, marker='o')
plt.plot(f, A, marker='o')
plt.xlabel('Frequenz (THz)')
plt.ylabel('Transmission / Absorption')
plt.legend(['Transmission T', 'Absorption A'])
plt.ylim([0, 1.2 * max(T)])
plt.tight_layout()
plt.show()