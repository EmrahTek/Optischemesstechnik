from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


Knife_Edge_PATH = Path("/home/emrahtek/Schreibtisch/CodeLab/Optischmesstechnik_1/A_24_Knife_Edge/KnifeEdgeMeasurement.txt")
print(Knife_Edge_PATH.exists(), Knife_Edge_PATH)
Knife_Edge_Data = np.loadtxt(Knife_Edge_PATH,delimiter=",", dtype=float)

# Define Variables
position = Knife_Edge_Data[:,0] # Verschiebung x
photoI = Knife_Edge_Data[:,1] # mA 

# Calculations
diffphotoI_ML = np.gradient(photoI) # use numpy.gradient instead of numpy.diff
plt.figure(1)
plt.plot(position, photoI, '-o')  # plot parameters
plt.xlabel('Distanz(mm)')  # labeling axis
plt.ylabel('Photostrom (mA)')  # labeling axis

#plt.show()
plt.figure(2)
plt.plot(position, diffphotoI_ML, '-o')  # plot parameters
plt.xlabel('Distanz(mm)')  # labeling axis
plt.ylabel('differenz. Photostrom (mA)')  # labeling axis
plt.show()




