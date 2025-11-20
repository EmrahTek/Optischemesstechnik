# Programm:         Aufgabe 15 Optische Messtechnik
# Author:           Rieben Retus for Hannes Merbold, Ursin Solèr
# Organisation:     FHGR Photonics
# Version:          1.3
# Date:             20.11.2024
# History:          1.0 main
#                   1.1 Plot implementation
#                   1.2 Correction of plotindex (19.02.2020)
#                   1.3 Simplify masking, create movie, plotly html output

# Note: In Python it's important to add the librarytype before the coresponding function i.e. numpy.linspace

# include essential Mathematical libraries
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from mpl_toolkits.mplot3d import Axes3D
data_path = Path("C:\\Users\\emrah\\OneDrive\\Desktop\\Photonic Studium\\5. Semester 2025 - 2026\\Optischemesstechnik_1\\Aufgabe_Python\\Aufgabe_15\\Redye_demo_spektrum_vertical.txt")
data = np.loadtxt(data_path, skiprows=42)

x_start = 66
y_start = 11
x_end = 281
y_end = 102
x_n = x_end - x_start + 1
y_n = y_end - y_start + 1
wavelength = data[:, 0]
datacube = np.zeros((y_n, x_n, len(wavelength)))

for jj in range(0, y_n):
    for kk in range(0, len(wavelength)):
        datacube[jj, 0:x_n, kk] = data[kk, (jj * x_n + 1):(jj * x_n + x_n + 1)]

plotindex_1 = 82
plotindex_2 = 223
plt.figure(1)
plt.subplot(2,1,1)
plt.imshow(datacube[:,:,plotindex_1])
plt.title(f'{wavelength[plotindex_1]} nm')
plt.subplot(2,1,2)
plt.imshow(datacube[:,:,plotindex_2])
plt.title(f'{wavelength[plotindex_2]} nm')

plt.tight_layout()

Material1_LowerBound = 7000
Material1_HigherBound = 10000
Material1 = (Material1_LowerBound < datacube[:, :, plotindex_1]) & (datacube[:, :, plotindex_1] < Material1_HigherBound)
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


## create matplotlib 3D plot for visualization of the hypercube
#X, Y = np.meshgrid(range(0, x_n), range(0, y_n))
#fig = plt.figure()
#ax = fig.add_subplot(111, projection="3d")
#for kk in range(0, len(wavelength)-20, 10):
#    ax.contourf(X, Y, datacube[:,:,kk], 100, zdir='z', offset=wavelength[kk], alpha=0.1)
#ax.set_zlim((800,1800))
#plt.show()


## create plotly 3D plot for visualization of the hypercube as html
## ($ pip3 install plotly==5.24.1)
#import plotly.graph_objects as go
#q = 4  # reduze number of points along all axes by this factor (otherwise the html gets ~200MB)
#X, Y, Z = np.mgrid[x_start:x_end:(x_n*1j/q), y_start:y_end:(y_n*1j/q), wavelength[0]:wavelength[-1]:(len(wavelength)*1j/q)]
#values = np.swapaxes(datacube[::q, ::q, ::q], 0, 1)
#fig = go.Figure(data=go.Volume(
#    x=X.flatten(),
#    y=Y.flatten(),
#    z=Z.flatten(),
#    value=values.flatten(),
#    isomin=np.min(values),
#    isomax=np.max(values),
#    opacity=0.2, # needs to be small to see through all surfaces
#    surface_count=5, # needs to be a large number for good volume rendering
#    slices_z=dict(show=True, locations=[wavelength[plotindex_1], wavelength[plotindex_2]]),
#    colorscale="Viridis",
#    ))
##fig.show()
#fig.write_html("Redye_demo_spektrum_vertical.html")


## create a movie with wavelength as time axis (linux)
#import matplotlib.animation as animation
#fps = 30
#fig = plt.figure()
#im  = plt.imshow(datacube[:, :, 0], interpolation='none', aspect='auto', vmin=np.min(datacube), vmax=np.max(datacube))
#anim = animation.FuncAnimation(
#                               fig,
#                               lambda i: [im.set_array(datacube[:, :, i])],
#                               frames = len(wavelength),
#                               interval = 1000 / fps, # in ms
#                               )
#anim.save('Redye_demo_spektrum_vertical.mp4', fps=fps, extra_args=['-vcodec', 'libx264'])
