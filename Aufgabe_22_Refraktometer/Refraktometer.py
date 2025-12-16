import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt  # (Plotting — Grafik çizimi)
from pathlib import Path 
# --- 1) Configure the CSV path (CSV yolunu ayarla)
# NOTE: Your screenshot shows the file name is `led_UI_3.csv` (not `led_U_I_3.csv`).
# (Not: Ekran görüntünüzde dosya adı `led_UI_3.csv` — `led_U_I_3.csv` değil.)
CSV_PATH = Path(r"")

# --- 2) Verify the file exists (Dosyanın varlığını doğrula)
if not CSV_PATH.exists():
    raise FileNotFoundError(f"CSV not found: {CSV_PATH}\n"
                            f"Tip: Right‑click in OneDrive → 'Always keep on this device'. ")

# --- 3) Try to read with standard float + semicolon and skip header (Standart okuma denemesi)
try:
    data = np.genfromtxt(
        CSV_PATH,
        delimiter=';',     # (Columns separated by ';' — Sütun ayıracı ';')
        skip_header=1,     # (Skip the header row — Başlık satırını atla)
        dtype=float,
        autostrip=True,
        encoding='utf-8'
    )
except ValueError:
    # If decimals use comma, convert on the fly (Ondalıklar virgüllüyse, anında dönüştür)
    conv = {
        0: lambda s: float(s.decode('utf-8').replace(',', '.')),
        1: lambda s: float(s.decode('utf-8').replace(',', '.')),
    }
    data = np.genfromtxt(
        CSV_PATH,
        delimiter=';',
        skip_header=1,
        dtype=float,
        autostrip=True,
        encoding='utf-8',
        converters=conv
    )

# --- 4) Slice columns (Sütunları ayır)
data[:, 0]           # (Voltage column — Gerilim sütunu)
strom_mA = data[:, 1]           # (Current column in mA — Akım sütunu mA)