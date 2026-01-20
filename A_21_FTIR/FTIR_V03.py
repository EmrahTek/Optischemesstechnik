"""
FTIR (Interferogramm -> Zeitachse -> FFT-Spektrum)
"""
import numpy as np
import matplotlib.pyplot as plt

x_pos_cm = np.array([0.00,0.02,0.04,0.06,0.08,0.10,0.12,0.14,0.16,0.18,0.20,0.22,0.24,0.26,0.28,0.30],dtype = float) # cm
I_x = np.array([6500,5000,3572,5000,6231,5000,4038,5000,5681,5000,4564,5000,5254,5000,4867,5000],dtype = float) # arb.u.

c = 3e8 # m/s 

# ----------------------
# (i) Zeitachse: t = 2x/c
# ----------------------

x_m = x_pos_cm*1e-2  # cm - > m
t_s = 2.0*x_m / c # seconds
t_ps = t_s*1e12 # ps (nur fürs Plotten)
# Optional (oft sinnvoll): DC-Anteil entfernen
I0 = I_x - np.mean(I_x)

# Zeitabstand (Sampling Intervall)
dt_s = t_s[1] - t_s[0]
N = len(t_s)

# ----------------------
# (ii) FFT (nur positiver Frequenzteil)
# ----------------------
# rfft: für reelle Signale, gibt nur 0..Nyquist zurück
s = np.fft.rfft(I0)
nu_hz = np.fft.rfftfreq(N,d=dt_s) # Frequenzachse in Hz
nu_thz = nu_hz / 1e12     # THz

s_mag = np.abs(s) # |I(nu)|

# ----------------------
# (iii) Plots (1x2)
# ----------------------
fig, ax = plt.subplots(1, 2, figsize=(10, 4))

# Links: I(t) gegen t (ps)
ax[0].plot(t_ps, I_x, "o-", label="Interferogramm I(t)")
ax[0].set_xlabel("t (ps)")
ax[0].set_ylabel("I(t) (arb. u.)")
ax[0].set_title("Interferogramm: I(t) gegen t")
ax[0].grid(True)
ax[0].legend()

# Rechts: |I(nu)| gegen nu (THz)
ax[1].plot(nu_thz, s_mag, "o-", label="|I(ν)| (FFT)")
ax[1].set_xlabel("ν (THz)")
ax[1].set_ylabel("|I(ν)| (arb. u.)")
ax[1].set_title("Spektrum: |I(ν)| gegen ν")
ax[1].grid(True)
ax[1].legend()

plt.tight_layout()
plt.show()