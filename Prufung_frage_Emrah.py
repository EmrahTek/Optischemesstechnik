import numpy as np
import matplotlib.pyplot  as plt


Brix_data = np.array([0.0,5.0,1.0,15.0,20.0,30.0,40.0], dtype=float)
Drehwinkel_data = np.array([0,3.2,5.5,9.3,11.8,17.2,25.7], dtype=float)

p = np.polyfit(Brix_data,Drehwinkel_data,1)
yfit = p[0]*Brix_data + p[1] #yfit = np.polyval(p, x)


print("Brix data Data: ", Brix_data)
print("Drehwinkel Data: ", Drehwinkel_data)
print("polyfit: " , p)
print("yfit: ", yfit)

plt.figure()
plt.plot(Brix_data,Drehwinkel_data,'o')
plt.plot(Brix_data,yfit,'r')
plt.xlabel('Brix Data')
plt.ylabel('Drehwinkel')
Steigung = p[0]

print("Steigung: ", Steigung)

Brix_15 = (yfit - p[1])/Brix_data

print("Brix",Brix_15)

plt.show()
