import numpy as np
import math 

Blutdruck_mmHG = [125,129,140,121,127]
summe = 0.0

try:
    for wert in Blutdruck_mmHG:  
        summe += wert
    result = summe / len(Blutdruck_mmHG)
    print("Mittelwert : ", result)


except:
    print("Können Sie bitte richtig machen! ")
#*****************oben meine alte version unten relativ lang*********
mean = sum(Blutdruck_mmHG) / len(Blutdruck_mmHG)
# 2. Quadratische Abweichungen summieren
abweichungen = [(x - mean)**2 for x in Blutdruck_mmHG]
summe = sum(abweichungen)
# 3. Durch (N-1) teilen
N = len(Blutdruck_mmHG)
varianz = summe / (N-1)

# 4. Wurzel ziehen
standardabweichung = math.sqrt(varianz)
print("mittelwert:", mean)
print("standardabweichung:" , standardabweichung)
print("Ende das Programs")

#*****************kurzere version************

"""
In Python gibt mean und std (standardabweichugen)
np.mean
np.std

in std gibt ddof = 1 ddof ist ein N-1 1
"""

print("Numpy std(ddof=1): ", np.std(Blutdruck_mmHG,ddof=1))

#*************** am beste version ***********

daten = [125,129,140,121,127]

mean = np.mean(daten)
std = np.std(daten, ddof = 1) # ddof = 1 --> Stichprobe
print("***********am beste***************")
print("Mittelwert: " , mean)
print("Standardabweichung: ", std)