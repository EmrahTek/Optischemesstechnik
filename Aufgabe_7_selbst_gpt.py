import numpy as np
from sklearn.linear_model import LinearRegression

# Messdaten (ölçüm verileri)
x = np.array([1, 2, 3, 4, 5, 6, 7])   # Spannung (V)

# Drei Strom-Messreihen (üç farklı akım ölçüm serisi)
y1 = np.array([0.9, 2.1, 3.0, 4.1, 4.8, 6.0, 7.1])
y2 = np.array([0.7, 2.2, 3.1, 3.8, 4.8, 6.3, 7.2])
y3 = np.array([0.5, 2.4, 3.5, 3.9, 5.5, 5.8, 7.5])

def regression_and_r2(x,y):
    # polyfit berechnet die Regressionsgerade (polynomial fit)
    coeffs = np.polyfit(x,y,1) # 1 bedeutet lineare Regression
    slope,intercept = coeffs # Steigung und Achsenabschnitt

    # y_fit = vorhersage Werte mit der Regressionsgerade 
    # (yfit regresyon doğrusu ile tahmin edilen değerler)
    yfit = slope*x + intercept
    #Residuen: unterschied zwischen gemessenen und vorhergesagten werten 
    #(ölçülen ve tahmin edilen arasındaki fark)
    yresid = y - yfit

    # SSresid: Summe der quadrierten Residuen (hata kareleri toplamı)
    SSresid = np.sum(yresid**2)

    # SStotal: Gesamtvarianz der Daten (verilerin toplam varyansı)
    SStotal = len(y)*np.var(y)
    # R^2: Determinationskoeffizient (modelin açıklama gücü)
    rsq = 1 - SSresid / SStotal
    return slope,intercept,rsq

# Ergebnisse für alle drei Messungen (her üç ölçüm için sonuçlar)
for i, y in enumerate([y1, y2, y3], start=1):
    slope, intercept, rsq = regression_and_r2(x, y)
    print(f"Messreihe {i}: Steigung = {slope:.3f}, Achsenabschnitt = {intercept:.3f}, R^2 = {rsq:.4f}")
