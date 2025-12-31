import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D

data_path = Path("C:\\Users\\emrah\\OneDrive\\Desktop\\Photonic Studium\\5. Semester 2025 - 2026\\Optischemesstechnik_1\\Aufgabe_Python\\Aufgabe_15\\Redye_demo_spektrum_vertical.txt")
data = np.loadtxt(data_path,skiprows=42)

x_start = 66
y_start = 11
x_end = 281
y_end = 102
x_n = x_end - x_start + 1
y_n = y_end - y_start + 1
wavelength = data[:,0]
datacube = np.zeros((y_n,x_n,len(wavelength)))

for jj in range(0, y_n):
    for kk in range(0, len(wavelength)):
        datacube[jj, 0:x_n, kk] = data[kk, (jj*x_n+1):(jj*x_n+x_n+1)]

plotindex_1 = 82
plotindex_2 = 223
plt.figure(1)
plt.subplot(2,1,1)
plt.imshow(datacube[:,:,plotindex_1])
plt.title(f'{wavelength[plotindex_2]} nm')

plt.tight_layout()

Material1_LowerBound = 7000
Material1_HigherBound = 10000
Material1 = (Material1_LowerBound < datacube[:,:,plotindex_1]) & (datacube[:,:,plotindex_1] < Material1_HigherBound)
plt.figure(2)
plt.subplot(2,1,1)
plt.imshow(Material1)
plt.title(f'{wavelength[plotindex_1]} nm')

Material2_LowerBound = 4000
Material2_HigherBound = 6000
Material2 = (Material2_LowerBound < datacube[:, :, plotindex_2]) & (datacube[:, :, plotindex_2] < Material2_HigherBound)
plt.figure(2)
plt.subplot(2,1,2)
plt.imshow(Material2)
plt.title(f'{wavelength[plotindex_2]} nm')

plt.tight_layout()
plt.show()
