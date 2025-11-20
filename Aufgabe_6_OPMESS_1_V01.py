import numpy as np
import matplotlib.pyplot as plt

# Messdaten (x = Spannung, y = Strom)
# (Measurement data: x = voltage, y = current) (Ölçüm verileri: x = voltaj, y = akım)
x = np.array([1, 2, 3, 4, 5, 6, 7])
y = np.array([0.9, 2.1, 3.0, 4.1, 4.8, 6.0, 7.1])

# Lineare Regression mit numpy.polyfit (degree=1 => Gerade)
# (Linear regression with numpy.polyfit, degree=1 means a straight line)
# (Doğrusal regresyon numpy.polyfit ile yapılır, derece=1 doğrusal denklem demek)
coeffs = np.polyfit(x, y, 1)   # coeffs[0] = slope (m), coeffs[1] = intercept (b)

slope, intercept = coeffs
print("Steigung m:", slope)       # (Slope m) (Eğim m)
print("Achsenabschnitt b:", intercept)  # (Intercept b) (Y eksenini kesişim b)

# Regressionsgerade berechnen
# (Calculate regression line) (Regresyon doğrusunu hesapla)
y_fit = slope * x + intercept

# Plot erstellen
plt.scatter(x, y, color="blue", label="Messwerte")  # (scatter plot of measured values)
plt.plot(x, y_fit, color="red", label="Regressionsgerade")  # (fitted line)
plt.xlabel("Spannung (V)")   # (Voltage)
plt.ylabel("Strom (A)")      # (Current)
plt.legend()
plt.grid(True)
plt.show()
