# Programm:       Aufgabe 24 Optische Messtechnik
# Author:         Rieben Retus for Hannes Merbold, Ursin Solèr
# Organisation:   FHGR Photonics
# Version:        1.2
# Date:           09.12.2024
# History:        1.0 main
#                 1.1 use numpy.gradient instead of numpy.diff

# Note: In Python it's important to add the librarytype before the coresponding function i.e. numpy.linspace

# include essential Mathematical libraries
import numpy as np  # adds essential mathematical functions and handling with arrays like known from Matlab
import matplotlib.pyplot as plt  # adds 2D plot functions

# import data
data = np.loadtxt("KnifeEdgeMeasurement.txt", delimiter=',')

# define variables
position = data[:, 0]
photoI = data[:, 1]

# calculations
diffphotoI_ML = np.gradient(photoI)

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
