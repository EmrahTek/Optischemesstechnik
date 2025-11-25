from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


FTIR_PATH = Path("/home/emrahtek/Schreibtisch/CodeLab/Optischmesstechnik_1/Aufgabe_21_FTIR_Spektroskopie/FTIR_Daten.txt")

FTIR_Data = np.loadtxt(FTIR_PATH, delimiter='\t',dtype=float)

Raumachse = np.abs(FTIR_Data[:,0])
Intensitat = np.abs(FTIR_Data[:,1])

t = Raumachse

sp = np.fft.fft(np.sin(t))

freq = np.fft.fftfreq(t.shape[-1])

plt.plot(freq, sp.real, freq, sp.imag)
plt.title("Fourier Transformation FTIR")
plt.xlabel("Frequeans achse")
plt.ylabel("Amplitude")
plt.savefig("FTIR_Plot.png", dpi=300)
print("Plot 'FTIR_Plot_Fourier.png' dosyasına kaydedildi.")

#plt.show()

"""
fig = plt.figure()
plt.plot(Raumachse, Intensitat, linestyle = '-')
plt.title("Plot I(t) und I(v)")
plt.xlabel("Raumachse")
plt.ylabel("Intensitat")
plt.grid(True)

plt.tight_layout()
plt.savefig("FTIR_Plot.png", dpi=300)
print("Plot 'FTIR_Plot.png' dosyasına kaydedildi.")

#plt.show()
"""