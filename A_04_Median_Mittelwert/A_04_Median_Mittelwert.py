import numpy as np

Einkommen = np.array([150, 100,300000,50,200,225,125])*1e3

Mittelwert = np.mean(Einkommen)
Median = np.median(Einkommen)

print("Mittelwert: ", Mittelwert)
print("Median: ", Median)