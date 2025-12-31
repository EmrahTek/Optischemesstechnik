import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


FTIR_PATH = Path("/home/emrahtek/Schreibtisch/CodeLab/Optischmesstechnik_1/Aufgabe_21_FTIR_Spektroskopie/FTIR_Daten.txt")

FTIR_Data = np.loadtxt(FTIR_PATH, delimiter='\t',dtype=float)

Raumachse = (FTIR_Data[:,0])
Intensitaet = (FTIR_Data[:,1])

c = 2.998e8
Zeitachse = 2*Raumachse/c 
plt.figure(1)
plt.plot(Zeitachse,Intensitaet)
plt.xlabel('Zeit (s)')
plt.ylabel('Intensität (arb.u.)')
Spektrum = np.fft.fft(Intensitaet)
DeltaT = Zeitachse[2] - Zeitachse[1]
N = len(Zeitachse)
DeltaNu = 1 / (DeltaT*N)
Frequenzachse = DeltaNu*np.linspace(0,N//2 + 1, N//2) # floor division demek.
Spektrum = np.abs(Spektrum[0: N // 2])
plt.figure(2)
plt.plot(Frequenzachse,Spektrum)
plt.xlabel('Frequenz(Hz)')
plt.ylabel('Intensität(arb.u.)')
plt.show()
