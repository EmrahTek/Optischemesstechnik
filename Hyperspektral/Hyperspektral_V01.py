import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

IO_path = Path("/home/emrahtek/Schreibtisch/CodeLab/Optischmesstechnik_1/Hyperspektral/I0.txt")
IP_path = Path("/home/emrahtek/Schreibtisch/CodeLab/Optischmesstechnik_1/Hyperspektral/Ip.txt")


IO_data = np.loadtxt(IO_path,delimiter='\t',dtype=float)
Ip_data = np.loadtxt(IP_path,delimiter='\t',dtype=float)

IO_x_data = IO_data[:,0] 
Ip_x_data = Ip_data[:,0]

Ip_y_data = np.abs(IO_data[:,1])
IO_y_data = np.abs(IO_data[:,1])

fig,axs = plt.subplots(2,1)

axs[0].plot(IO_x_data, IO_y_data, ls = "-", c = "r")
axs[0].set_title("Hyperspektral I0 Plot")
axs[0].set_xlabel("I0 X Data")
axs[0].set_ylabel("I0 y Data")
axs[0].grid(True)


axs[1].plot(Ip_x_data, Ip_y_data, ls = "-", c = "b")
axs[1].set_title("Hyperspektral I0 Plot")
axs[1].set_xlabel("I0 X Data")
axs[1].set_ylabel("I0 y Data")
axs[1].grid(True)

plt.savefig("hyperspektral_plot.png", dpi=300)
print("Grafik kaydedildi: hyperspektral_plot.png")


plt.tight_layout()
plt.show()
