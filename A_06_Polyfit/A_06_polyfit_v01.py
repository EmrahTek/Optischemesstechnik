# Aufgabe 6: Lineare Regression in Python

import numpy as np
import matplotlib.pyplot as plt

x = np.array([1,2,3,4,5,6,7])
y = np.array([0.9,2.1,3.0,4.1,4.8,6.0,7.1])
p = np.polyfit(x,y,1)
yfit = p[0]*x + p[1] #yfit = np.polyval(p, x)

print("x Data: ", x)
print("y Data: ", y)
print("polyfit: " , p)
print("yfit: ", yfit)

plt.figure()
plt.plot(x,y,'o')
plt.plot(x,yfit,'r')
plt.xlabel('Spannung (V)')
plt.ylabel('Strom (A)')
Steigung = p[0]

print("Steigung: ", Steigung)
plt.show()
