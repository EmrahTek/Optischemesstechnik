# Programm:       Aufgabe 10 Optische Messtechnik
# Author:         Rieben Retus for Hannes Merbold, Ursin Solèr
# Organisation:   FHGR Photonics
# Version:        1.2
# Date:           29.09.2025
# History:        1.2 'numpy.int' is depreciated
#                 1.0 main

# Note: In Python it's important to add the librarytype before the coresponding function i.e. numpy.linspace

# include essential Mathematical libraries
import numpy as np  # adds essential mathematical functions and handling with arrays like known from Matlab
import matplotlib.pyplot as plt  # adds 2D plot functions

# define variables
nu_1 = 2
nu_2 = 5
nu_3 = 10
A_1 = 1
A_2 = .5
A_3 = .2
t_0 = 0
t_max = 10
N_t = 1000

# calculations
t = np.linspace(t_0, t_max, N_t)
y_t = A_1 * np.sin(2 * np.pi * nu_1 * t) + A_2 * np.sin(2 * np.pi * nu_2 * t) + A_3 * np.sin(2 * np.pi * nu_3 * t)

plt.figure(1)
plt.subplot(2, 1, 1)
plt.plot(t, y_t)  # plot parameters
plt.xlabel('Zeit (s)')  # labeling axis

y_f = np.fft.fft(y_t)
y_f = np.abs(y_f)
N_f = np.int64(N_t // 2 + 1)
y_f = y_f[0: N_f]
d_f = 1 / t_max
f = d_f * np.linspace(0, N_f - 1, N_f)
plt.subplot(2, 1, 2)
plt.plot(f, y_f)  # plot parameters
plt.xlabel('Frequenz (Hz)')  # labeling axis

plt.show()
