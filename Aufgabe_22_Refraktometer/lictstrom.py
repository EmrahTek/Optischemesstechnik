import numpy as np
import matplotlib.pyplot as plt


def funkt_A(r):
    return(r * 3.5) **2 




width_data = [10, 17,31, 57, 77] #mm


r = np.array([35., 60., 120., 180., 240.]) # mm

fig = plt.figure()
plt.plot(r, funkt_A(r), marker = 'o', linestyle = '-')
plt.title("A - widht")
plt.xlabel("Width_data")
plt.ylabel("A_data")
plt.grid(True)
plt.tight_layout()
plt.savefig("A -width", dpi=300)
