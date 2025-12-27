import numpy as np
import matplotlib.pyplot as plt

#Veriler
x = np.array([1,2,3,4,5,6,7], dtype=float)
y1 = np.array([0.9, 2.1, 3.0, 4.1, 4.8, 6.0, 7.1], dtype=float)
y2 = np.array([0.7, 2.2, 3.1, 3.8, 4.8, 6.3, 7.2], dtype=float)
y3 = np.array([0.5, 2.4, 3.5, 3.9, 5.5, 5.8, 7.5], dtype=float)

datasets = [("Messung 1", y1), ("Messung 2", y2), ("Messung 3", y3)]

fig,axes = plt.subplots(3,1,figsize=(7,12),sharex = True)

for ax, (name,y) in zip(axes,datasets):
    # 1) lineer fit: y = m*x + b
    m,b = np.polyfit(x,y,1)
    yfit = m*x + b

    # 2) R²
    ss_res = np.sum((y-yfit)**2)
    ss_tot = np.sum((y-y.mean())**2)
    r2 = 1 - ss_res / ss_tot

    # 3) plot 
    ax.scatter(x,y)
    ax.plot(x,yfit)
    ax.set_title(name)
    ax.set_ylabel("Strom (A)")
    ax.text(0.55, 0.15, f"Steigung = {m:.4f}\n$R^2$ = {r2:.4f}", transform=ax.transAxes)

    print(f"{name}: m={m:.4f}, b={b:.4f}, R^2={r2:.4f}")

axes[-1].set_xlabel("Spannung (V)")
plt.tight_layout()
plt.show()



