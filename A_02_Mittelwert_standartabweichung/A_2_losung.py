import numpy as np

Blutdruck = [125,129,140,121,127]

P = np.mean(Blutdruck)

DeltaP = np.std(Blutdruck, ddof=1)

print("P ist: \n", P)

print("DeltaP ist: \n", DeltaP)

