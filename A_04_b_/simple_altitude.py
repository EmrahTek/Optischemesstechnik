from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1) CSV yolu (ister sabit ver, ister terminalden parametreyle çalıştır)
CSV_PATH = Path("/home/emrahtek/Schreibtisch/CodeLab/Optischmesstechnik_1/A_04_b_/data.csv")

# 2) CSV oku
df = pd.read_csv(CSV_PATH)

# 3) Yükseklik sütununu seç (en sık: RelativeAlt)
if "RelativeAlt" in df.columns:
    alt = pd.to_numeric(df["RelativeAlt"], errors="coerce") / 1000.0  # mm -> m
    alt_name = "RelativeAlt (m)"
elif "AltitudeLocal" in df.columns:
    alt = pd.to_numeric(df["AltitudeLocal"], errors="coerce")         # zaten m olabilir
    alt_name = "AltitudeLocal (m)"
else:
    raise ValueError(f"Yükseklik sütunu yok. Sütunlar: {list(df.columns)}")

# 4) NaN temizle
alt = alt.dropna().reset_index(drop=True)

# 5) (Opsiyonel) “uçuş” verisi: yerdekileri at
alt_flight = alt[alt > 1.0]   # 1 metreden büyük olanları uçuş kabul ediyoruz

# 6) İstatistikler
def mean_median(x: pd.Series):
    return float(x.mean()), float(x.median()), int(x.shape[0])

mean_all, median_all, n_all = mean_median(alt)
mean_f, median_f, n_f = mean_median(alt_flight)

print("\n--- Tüm veri (ground + uçuş) ---")
print(f"n={n_all}, mean={mean_all:.3f} m, median={median_all:.3f} m")

print("\n--- Uçuş verisi (alt > 1 m) ---")
print(f"n={n_f}, mean={mean_f:.3f} m, median={median_f:.3f} m")

# 7) Çıktıları CSV’nin bulunduğu klasöre kaydet
out_dir = CSV_PATH.parent

# Grafik 1: zaman yerine index ile yükseklik
plt.figure()
plt.plot(alt.values, linewidth=1)
plt.title(f"Altitude vs Index ({alt_name})")
plt.xlabel("Sample index")
plt.ylabel("Altitude [m]")
plt.tight_layout()
plt.savefig(out_dir / "altitude_timeseries.png", dpi=160)

# Grafik 2: uçuş verisi histogram (mean vs median)
plt.figure()
plt.hist(alt_flight.values, bins=40)
plt.axvline(mean_f, linestyle="--", linewidth=2, label=f"mean={mean_f:.2f} m")
plt.axvline(median_f, linestyle="-", linewidth=2, label=f"median={median_f:.2f} m")
plt.title("Flight Altitude Histogram (alt > 1 m)")
plt.xlabel("Altitude [m]")
plt.ylabel("Count")
plt.legend()
plt.tight_layout()
plt.savefig(out_dir / "altitude_hist.png", dpi=160)

print("\nKaydedilen dosyalar:")
print(out_dir / "altitude_timeseries.png")
print(out_dir / "altitude_hist.png")
