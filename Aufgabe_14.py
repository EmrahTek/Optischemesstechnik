import numpy as np

lamda = 650e-9 #m
g_gitter = 500 # linien/mm
theta_einfalls = 23 # grad
ablenk_theta = 10

def ablenk_winkel(lamda, g_gitter, theta_einfalls)-> float:
    return np.arcsin(lamda/g_gitter +np.sin(theta_einfalls))

winkel = ablenk_winkel(lamda, g_gitter,theta_einfalls)

print(winkel)

