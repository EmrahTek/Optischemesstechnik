import numpy as np
import matplotlib.pyplot as plt

x = np.array([1,2,3,4,5,6,7])
y = np.array([0.9,2.1,3.0,4.1,4.8,6.0,7.1])

coeffs = np.polyfit(x,y,1)
slope, intercept = coeffs

print("Steigung m: ", slope)
print("Achsenabschnitt b: ", intercept)

y_fit = slope*x + intercept

plt.scatter(x,y,color="blue", label = "Messwerte")
plt.plot(x,y_fit, color="red", label="Regressionsgerade")
plt.xlabel("Spannung (V)")   # (Voltage)
plt.ylabel("Strom (A)")      # (Current)
plt.legend()
plt.grid(True)
plt.show()