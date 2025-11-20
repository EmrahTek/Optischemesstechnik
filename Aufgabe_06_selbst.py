# polyfit : Polinomun katsayilarini bulur. 
# polyval : O polinomun istedigin yerde hesaplar. 

import numpy as np
import matplotlib.pyplot as plt


x = np.array([1,2,3,4,5,6,7,]) # defined as array
y = np.array([0.9, 2.1, 3.0, 4.1, 4.8, 6.0, 7.1]) # defined as array

# calculations
p = np.polyfit(x,y,1)
yfit = np.polyval(p,x)

plt.figure()
plt.plot(x,y,'o') # plot parameters
plt.plot(x,yfit, 'r') # plot parameters
plt.xlabel('Spannung (V)') # labeling axis
plt.ylabel('Strom (A)') # labeling axis

plt.show() # displays plot
print('Steigung = ', p[0])