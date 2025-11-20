import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Messwerte
x = np.array([1, 2, 3, 4, 5, 6, 7]).reshape(-1, 1)
y = np.array([0.9, 2.1, 3.0, 4.1, 4.8, 6.0, 7.1])

# Modell erstellen
model = LinearRegression()
model.fit(x, y)

# Parameter
m = model.coef_[0]     # Steigung
b = model.intercept_   # Achsenabschnitt

print(f"Steigung m = {m:.2f}")
print(f"Achsenabschnitt b = {b:.2f}")

# Vorhersage für Gerade
x_fit = np.linspace(1, 7, 100).reshape(-1, 1)
y_fit = model.predict(x_fit)

# Plot
plt.scatter(x, y, color="blue", label="Messwerte")
plt.plot(x_fit, y_fit, color="red", label=f"Regression: y={m:.2f}x+{b:.2f}")
plt.xlabel("Spannung (V)")
plt.ylabel("Strom (A)")
plt.legend()
plt.grid()
plt.show()
