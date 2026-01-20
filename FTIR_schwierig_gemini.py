import numpy as np
import matplotlib.pyplot as plt

# --- Parameter ---
dx_mirror = 2e-6           # Spiegel-Schrittweite [m]
# NOT: 3000 cm^-1 görmek için dx_mirror < 0.8e-6 olmalıdır.
N = 4096                   
sigma1 = 3030.0 * 100      
sigma2 = 2900.0 * 100      

# a) OPD-Achse
x = (np.arange(N) - N/2) * dx_mirror
delta = 2.0 * x
d_delta = delta[1] - delta[0]

# Nyquist kontrolü (Konsola bilgi yazdırır)
sigma_max_cm = (1 / (2 * d_delta)) / 100
print(f"Maksimum ölçülebilir dalga sayısı (Nyquist): {sigma_max_cm:.1f} cm^-1")

# b) Interferogramm
I = np.cos(2 * np.pi * sigma1 * delta) + 0.6 * np.cos(2 * np.pi * sigma2 * delta)
I += 0.02 * np.random.randn(N)

# c) DC ve Pencereleme
I_ac = I - np.mean(I)
I_windowed = I_ac * np.hanning(N)
spectrum = np.abs(np.fft.rfft(I_windowed))

# d) Wellenzahlachse
freqs_m = np.fft.rfftfreq(N, d_delta)
wavenumbers_cm = freqs_m / 100

# e) Peak bulma (Hata korumalı)
mask = (wavenumbers_cm >= 2500) & (wavenumbers_cm <= 3500)
search_range_wn = wavenumbers_cm[mask]
search_range_spec = spectrum[mask]

if len(search_range_spec) > 0:
    peak_indices = np.argsort(search_range_spec)[-2:]
    found_peaks = np.sort(search_range_wn[peak_indices])
    print(f"Gefundene Peak-Lagen: {found_peaks[0]:.1f} cm^-1 und {found_peaks[1]:.1f} cm^-1")
else:
    found_peaks = []
    print("UYARI: Belirtilen aralıkta (2500-3500) peak bulunamadı! Nyquist limitini kontrol edin.")

# f) Plotten (Raw strings 'r' kullanılarak SyntaxWarning giderildi)
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(delta * 1e3, I)
plt.xlabel(r"OPD $\delta$ (mm)")
plt.ylabel("Intensität")

plt.subplot(2, 1, 2)
plt.plot(wavenumbers_cm, spectrum)
plt.xlabel(r"Wellenzahl $\sigma$ ($cm^{-1}$)")
plt.ylabel("Amplitude")
# Tüm spektrumu görmek için xlim'i Nyquist'e kadar ayarlayalım
plt.xlim(0, max(wavenumbers_cm)) 

plt.tight_layout()
plt.show()