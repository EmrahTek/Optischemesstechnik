import numpy as np
import matplotlib.pyplot as plt

x = np.array([1,2,3,4,5,6,7], dtype=float)

y1 = np.array([0.9, 2.1, 3.0, 4.1, 4.8, 6.0, 7.1], dtype=float)
y2 = np.array([0.7, 2.2, 3.1, 3.8, 4.8, 6.3, 7.2], dtype=float)
y3 = np.array([0.5, 2.4, 3.5, 3.9, 5.5, 5.8, 7.5], dtype=float)

datasets = [("Messung 1", y1), ("Messung 2", y2), ("Messung 3", y3)]

for name, y in datasets:
    m,b = np.polyfit(x,y,1)
    yfit = m*x + b

    yresid = y- yfit # her noktanin artigi (residual)
    SSresid = np.sum(yresid**2) # "Aciklanamayan" hata enerjisi
    SStotal = np.sum((y - y.mean())**2) # Verinin toplam degiskenligi
    rsq = 1 - SSresid/SStotal # R² degiskenin ne kadarini dogru acikladin 

    print(f"{name}: Steigung m={m:.4f}, Achsenabschnitt b={b:.4f}, R^2={rsq:.4f}")

    plt.figure()
    plt.scatter(x, y)
    plt.plot(x, yfit)
    plt.xlabel("Spannung (V)")
    plt.ylabel("Strom (A)")
    plt.title(name)
    plt.text(0.05, 0.95, f"Steigung={m:.4f}\n$R^2$={rsq:.4f}",
             transform=plt.gca().transAxes, va="top")
    plt.tight_layout()
    plt.show()