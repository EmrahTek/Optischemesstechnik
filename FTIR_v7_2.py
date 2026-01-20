import numpy as np
import matplotlib.pyplot as plt

# --- Konstanten und Parameter ---
c = 3.00e8              # Lichtgeschwindigkeit in m/s
nu1 = 3.0e13            # Frequenz 1 in Hz
nu2 = 4.5e13            # Frequenz 2 in Hz
dx = 2e-6               # Schrittweite in m (2 µm)
x_max = 2.0e-3          # Endposition in m (2.0 mm)
sigma = 0.05            # Rausch-Standardabweichung

# a) Erzeugen von x, t und I(t)
x = np.arange(0, x_max + dx, dx)  # Raumachse
t = 2 * x / c                     # Zeitachse (t = 2x/c)

# Erzeugung des Signals mit Gauß-Rauschen
noise = np.random.normal(0, sigma, len(t))
I_t = np.cos(2 * np.pi * nu1 * t) + 0.6 * np.cos(2 * np.pi * nu2 * t) + noise

# Plot des Interferogramms
plt.figure(figsize=(10, 4))
plt.plot(x * 1e3, I_t, lw=0.5)
plt.title("Synthetisches Interferogramm $I(t)$")
plt.xlabel("Spiegelweg $x$ (mm)")
plt.ylabel("Intensität (a.u.)")
plt.grid(True)
#plt.show()

# b) Spektrum berechnen (FFT)
n = len(I_t)
dt = 2 * dx / c                   # Zeitlicher Probenabstand
freqs = np.fft.fftfreq(n, d=dt)   # Frequenzachse erzeugen
I_nu = np.fft.fft(I_t)            # FFT berechnen

# Nur positive Frequenzen betrachten (nu >= 0)
pos_mask = freqs >= 0
freqs_pos = freqs[pos_mask]
amplitude_pos = np.abs(I_nu[pos_mask])

# Plot des Spektrums
plt.figure(figsize=(10, 4))
plt.plot(freqs_pos / 1e12, amplitude_pos)
plt.title("Spektrum $|I(\\nu)|$")
plt.xlabel("Frequenz $\\nu$ (THz)")
plt.ylabel("Amplitude")
plt.xlim(0, 60) # Fokus auf relevanten Bereich
plt.grid(True)
plt.show()

# c) Dominante Frequenzen bestimmen
# Wir ignorieren nu=0 (DC-Anteil)
mask_no_dc = freqs_pos > 0
f_search = freqs_pos[mask_no_dc]
a_search = amplitude_pos[mask_no_dc]

# Finde die Indizes der zwei höchsten Peaks
# (Hinweis: Bei dx=2µm liegt nu2 oberhalb der Nyquist-Grenze -> Aliasing!)
indices = np.argsort(a_search)[-2:] 
peak_freqs = f_search[indices]
peak_freqs = np.sort(peak_freqs) # Sortieren für die Ausgabe

print("-" * 30)
for i, f in enumerate(peak_freqs):
    lam = c / f
    print(f"Peak {i+1}: Frequenz = {f:.2e} Hz | Wellenlänge = {lam*1e6:.2f} µm")
print("-" * 30)