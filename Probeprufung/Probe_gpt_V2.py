"""
-> Mit einem FTIR-Spektrometer wurde ein räumliches Interferogramm I(x) aufgenommen.

-> Die erste Spalte enthält die Spiegelposition x in µm (äquidistant), die zweite Spalte die Intensität in arb. Einheiten.

a) Wandeln Sie x in eine Zeitachse t um (t = 2x/c). Verwenden Sie c = 3.0·10^8 m/s.
b) Berechnen Sie das Betragsspektrum |I(ν)| mittels FFT (numpy.fft.fft).
c) Erstellen Sie eine Abbildung mit zwei horizontal angeordneten Plots: links I(t) gegen t, rechts |I(ν)| gegen ν (nur positive Frequenzen).
d) Beschriften Sie Achsen und fügen Sie jeweils eine Legende ein.


"""

import numpy as np
import matplotlib.pyplot as plt
x_um = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], float)
I = np.array([1.00,0.94,0.78,0.54,0.27,0.05,0.02,0.10,0.30,0.56,0.80,0.95,1.00,0.93,0.76,0.52], float)


c = 3.0e8
t = 2.0*(x_um*1e-6)
dt = t[1]-t[0]

Y = np.abs(np.fft.fft(I))
nu = np.fft.fftfreq(len(I), d=dt)
mask = nu >= 0

fig, ax = plt.subplots(1,2, figsize=(10,4))
ax[0].plot(t*1e15, I, 'o-', label = 'I(t)')
ax[0].set(xlabel='t (fs)', ylabel='Intensität (arb.u.)')
ax[0].legend(); ax[0].grid(True, alpha=0.3)
ax[1].plot(nu[mask]/1e12, Y[mask], 'o-', label='|I(ν)|')
ax[1].set(xlabel='ν (THz)', ylabel='Amplitude (arb.u.)')
ax[1].legend(); ax[1].grid(True, alpha=0.3)
plt.tight_layout(); plt.show()