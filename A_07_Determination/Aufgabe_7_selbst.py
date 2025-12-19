# Regression, veriler arasında ilişkiyi kurup tahmin yapmaya yarayan yöntemdir.
import numpy as np
from sklearn.linear_model import LinearRegression

# Daten
x = np.array([1,2,3,4,5,6,7]).reshape(-1,1)
y_sets =  [
    [0.9, 2.1, 3.0, 4.1, 4.8, 6.0, 7.1],
    [0.7, 2.2, 3.1, 3.8, 4.5, 6.3, 7.2],
    [0.5, 2.4, 3.5, 3.9, 5.5, 5.8, 7.5]
    ]

# Ergebnisse speichern
for i,y in enumerate(y_sets, start=1):
    model = LinearRegression()
    model.fit(x,y) # Verilere regresyon dogrusunu uydurur. 
    m = model.coef_[0] # Egim[regresyon katsayisi.]
    b = model.intercept_ # Y-eksenini kestigi nokta
    r2 = model.score(x,y) # Determinant koeffizient r**2 hesaplar
    print(f"Messreihe {i}: y = {m:.2f}x + {b:.2f}, R^2 = {r2:.3f}")


