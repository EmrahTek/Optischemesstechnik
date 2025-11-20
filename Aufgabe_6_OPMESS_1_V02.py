import numpy as np
import matplotlib.pyplot as plt

# Messdate ( x= Spannung,  y = Strom)
# Measurement data: x = voltage, y = current

x = np.array([1,2,3,4,5,6,7])
y = np.array([0.9, 2.1,3.0,4.1,4.8,6.0, 7.1])

# Lineare Regression mit numpy.polyfit (degree = 1 => Gerade)
# (Linear regression with numpy.polyfit, degree = 1,means a straight line)
coeffs = np.polyfit(x,y,1) # coeffs[0] = slope(m)

slope, intercept = coeffs
print("Steigung m: ", slope) # Slope m -> Egim
print("Achsenabschnitt b: ", intercept) # Intercept b -> Y eksenini kesisim b

# Regressionsgrade bereechnen 
y_fit = slope*x + intercept

# Plot erstellen
plt.scatter(x,y, color = "blue", label = "Messwerte")
plt.plot(x,y_fit, color="red", label = "Regressionsgerade")
plt.xlabel("Spannung(V)")
plt.ylabel("Strom(A)")
plt.legend()
plt.grid(True)
plt.show()