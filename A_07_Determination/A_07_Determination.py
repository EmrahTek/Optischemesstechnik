import numpy as np
import matplotlib.pyplot as plt

def regressiongerade(x: np.ndarray, y: np.ndarray):
    """
    Lineare Regression: y = m*x + b
    Dönüş: (m, b, y_fit)

    Formül (Least Squares):
      m = sum((x-x̄)(y-ȳ)) / sum((x-x̄)^2)
      b = ȳ - m*x̄
    """

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    x_mean = x.mean()
    y_mean = y.mean()

    m = np.sum((x-x_mean)*(y-y_mean)) / np.sum((x-x_mean)**2)
    b = y_mean -m*x_mean

    y_fit = m*x + b

    return m,b,y_fit

def determination_koeffizient(y: np.ndarray, y_fit: np.ndarray):
    """
    R^2 = 1 - SSE/SST
      SSE = sum((y - y_fit)^2)          (Residual / hata kareleri toplamı)
      SST = sum((y - ȳ)^2)              (Toplam değişkenlik)
    """
    y = np.asarray(y,dtype=float)
    y_fit = np.asarray(y_fit, dtype=float)

    sse = np.sum((y - y_fit)**2)
    sst  = np.sum((y-y.mean())**2)

    # sst = 0 olursa (y sabitse) R^2 tanımsız olur; burada güvenli davranalım:
    if sst == 0:
        return np.nan
    r2  = 1- (sse / sst)
    return r2

def plot_fit(ax,x,y,m,b,r2,title=""):
    """
    Noktaları (scatter) ve fit doğrusunu çizer, eğim ve R^2'yi yazar.
    """
    x = np.asarray(x,dtype=float)
    y = np.asarray(y,dtype=float)

    x_line = np.linspace(x.min(), x.max(), 200)
    y_line = m*x_line + b

    ax.scatter(x,y)
    ax.plot(x_line,y_line)
    ax.set_xlabel("Spannung (V)")
    ax.set_ylabel("Strom (A)")
    ax.set_title(title)

    # Grafiğin içine yazı
    ax.text(
        0.55, 0.15,
        f"Steigung = {m:.4f}\n$R^2$ = {r2:.4f}",
        transform=ax.transAxes
    )

def main():
    # Veriler (tablodan)
    x = np.array([1, 2, 3, 4, 5, 6, 7])

    y1 = np.array([0.9, 2.1, 3.0, 4.1, 4.8, 6.0, 7.1])
    y2 = np.array([0.7, 2.2, 3.1, 3.8, 4.8, 6.3, 7.2])
    y3 = np.array([0.5, 2.4, 3.5, 3.9, 5.5, 5.8, 7.5])

    datasets = [("Messung 1", y1), ("Messung 2", y2), ("Messung 3", y3)]

    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(7, 12), sharex=True)

    for ax, (name, y) in zip(axes, datasets):
        m, b, y_fit = regressiongerade(x, y)
        r2 = determination_koeffizient(y, y_fit)

        plot_fit(ax, x, y, m, b, r2, title=name)

        # Konsola da yazdıralım
        print(f"{name}: m={m:.4f}, b={b:.4f}, R^2={r2:.4f}")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
