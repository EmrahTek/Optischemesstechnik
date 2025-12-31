import pandas as pd
import numpy as np

n_quartz = 1.458

# 1) CSV oku
df = pd.read_csv("/home/emrahtek/Schreibtisch/CodeLab/Optischmesstechnik_1/Aufgabe_22_Refraktometer/ICUMSA_Brix_Table.csv")

# 2) "Brix" sütununu sayıya çevir, sayı olmayan satırları (mesela "...") at
df["Brix_num"] = pd.to_numeric(df["Brix"], errors="coerce")
df = df.dropna(subset=["Brix_num"]).copy()
df["Brix_num"] = df["Brix_num"].astype(int)

# 3) Tabloyu "uzun form"a çevir: (Brix, decimal, n) -> (brix_total, n)
decimal_cols = [c for c in df.columns if c not in ["Brix", "Brix_num"]]
long = df.melt(id_vars=["Brix_num"], value_vars=decimal_cols,
               var_name="dec", value_name="n")

long["dec"] = long["dec"].astype(float)          # "0.1" -> 0.1
long["brix_total"] = long["Brix_num"] + long["dec"]
long = long.dropna(subset=["n"]).sort_values("brix_total")

# 4) İstenen Brix değerleri
targets = np.arange(0, 81, 10)  # 0,10,...,80

# 5) n(brix) değerlerini al (tam eşleşme yoksa lineer interpolasyon)
n_interp = np.interp(targets, long["brix_total"], long["n"])

# 6) Kritik açı hesabı (n_solution < n_quartz ise)
ratio = n_interp / n_quartz
theta_c = np.degrees(np.arcsin(np.clip(ratio, -1, 1)))

# 7) Sonuç tablosu + TIR mümkün mü?
result = pd.DataFrame({
    "Brix_%": targets,
    "n_solution": n_interp,
    "TIR_possible": n_interp < n_quartz,
    "theta_c_deg": np.where(n_interp < n_quartz, theta_c, np.nan)
})

print(result.to_string(index=False))
