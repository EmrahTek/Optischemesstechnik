import numpy as np
import matplotlib.pyplot as plt

# ---- Parametreler ----
t_0 = 0
t_max = 10
N_t = 1000

# En az 3 sinüs: (Amplitude, Frekans, Faz)
A1, f1, phi1 = 1.0, 2.0, 0.0
A2, f2, phi2 = 0.6, 5.0, 0.4
A3, f3, phi3 = 0.3, 12.0, 1.0

# ---- Zaman dizisi ve sinyal ----
t = np.linspace(t_0, t_max, N_t)
y_t = (A1 * np.sin(2*np.pi*f1*t + phi1) +
       A2 * np.sin(2*np.pi*f2*t + phi2) +
       A3 * np.sin(2*np.pi*f3*t + phi3))

# ---- FFT (frekans domeni) ----
dt = t[1] - t[0]                  # örnekleme aralığı
Y = np.fft.rfft(y_t)              # real FFT
f = np.fft.rfftfreq(N_t, d=dt)    # doğru frekans ekseni

# Amplitüd spektrumu (tek taraflı)
A_f = (2.0 / N_t) * np.abs(Y)
A_f[0] /= 2.0                     # DC bileşeni düzeltme
if N_t % 2 == 0:
    A_f[-1] /= 2.0                # Nyquist bileşeni (N_t çiftse) düzeltme

# ---- Plot ----
plt.figure(1)

plt.subplot(2, 1, 1)
plt.plot(t, y_t)
plt.xlabel("Zeit (s)")
plt.ylabel("y(t)")
plt.title("Zeitbereich")

plt.subplot(2, 1, 2)
plt.plot(f, A_f)
plt.xlabel("Frequenz (Hz)")
plt.ylabel("|Y(f)| (Amplitude)")
plt.title("Frequenzbereich (FFT)")
plt.xlim(0, 30)   # sadece ilgilendiğin frekans aralığını göster
plt.tight_layout()

plt.show()
