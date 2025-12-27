# drone_altitude_analysis.py
# Amaç: CSV'den dronun tipik uçuş yüksekliğini (median vs mean) bulmak + grafikleri çizmek.
import sys
from dataclasses import dataclass
from typing import Optional,Tuple
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = Path(
    "//home//emrahtek//Schreibtisch//CodeLab//Optischmesstechnik_1//A_04_b_//data.csv"
) 

@dataclass
class Stats:
    n: int
    mean: float
    std: float
    sem: float
    q1: float
    q3: float
    iqr: float
    mad: float # median absolute deviation ( robust yayilim )

def pick_time_column(df: pd.DataFrame) -> Optional[str]:
    """Muhtemel zaman sütunlarini dene."""
    candidates = ["Time", "Timestamp", "time", "timestamp", "DataTime", "datatime"]
    for c in candidates:
        if c in df.columns:
            return c
    return None

def pick_altitude_column(df: pd.DataFrame) -> str:
    """
    Yükseklik için en olası sütunu seç.
    Öncelik: RelativeAlt -> AltitudeLocal -> AltitudeAmsl -> Altitude
    """
    for c in ["RelativeAlt", "AltitudeLocal", "AltitudeAmsl", "Altitude", "alt", "height"]:
        if c in df.columns:
            return c
    raise ValueError(f"Yükseklik sütunu bulunamadı. Mevcut sütunlar: {list(df.columns)}")

def to_altitude_meters(series: pd.Series, colname: str) -> pd.Series:
    """
    Yüksekliği metreye çevir.
    - RelativeAlt çoğu log'ta mm olabilir (5000 -> 5 m). Otomatik sezdir.
    - AltitudeLocal/AltitudeAmsl çoğunlukla zaten metre olur.
    """
    s =pd.to_numeric(series, errors="coerce")

    # Eğer RelativeAlt ise ve değerler büyükse mm olma ihtimali yüksek:
    if colname.lower() == "relativealt".lower():
        # Tipik mm ölçeği: binler. Metrede tipik: 0-100 arası.
        # Basit sezgi: medyan > 200 ise mm kabul et.
        med = np.nanmedian(s.values)
        if med > 200:
            return s / 1000.0 # mm -> m
        return s # zaten metre olabilir
    # Diger sütunlar: cogu zaman metre, dokunma
    return s

def fill_short_gaps(mask: np.ndarray, max_gap: int) -> np.ndarray:
    """
    True bölgeleri içindeki kısa False boşlukları doldur (uçuş sırasında kısa drop-out için).
    max_gap: kaç örnekliğe kadar boşluğu kapatacağımız.
    """
    m = mask.copy()
    n = len(m)
    i = 0
    while i < n:
        if m[i]:
            i += 1
            continue
        # False bloğu başı
        j = i
        while j < n and (not m[j]):
            j += 1
        gap_len = j - i
        # Eğer iki yanında True varsa ve boşluk kısaysa doldur
        left_true = (i - 1 >= 0 and m[i - 1])
        right_true = (j < n and m[j])
        if left_true and right_true and gap_len <= max_gap:
            m[i:j] = True
        i = j
    return m

def longest_true_segment(mask: np.ndarray) -> Tuple[int, int]:
    """Mask içindeki en uzun True segmentin (start, end) indeksini döndür (end hariç)."""
    best = (0, 0)
    n = len(mask)
    i = 0
    while i < n:
        if not mask[i]:
            i += 1
            continue
        j = i
        while j < n and mask[j]:
            j += 1
        if (j - i) > (best[1] - best[0]):
            best = (i, j)
        i = j
    return best

def robust_stats(x: np.ndarray) -> Stats:
    x = x[np.isfinite(x)]
    n = len(x)
    mean = float(np.mean(x)) if n else float("nan")
    median = float(np.median(x)) if n else float("nan")
    std = float(np.std(x, ddof=1)) if n > 1 else float("nan")
    sem = float(std / np.sqrt(n)) if n > 1 else float("nan")
    q1 = float(np.quantile(x, 0.25)) if n else float("nan")
    q3 = float(np.quantile(x, 0.75)) if n else float("nan")
    iqr = float(q3 - q1) if n else float("nan")
    mad = float(np.median(np.abs(x - median))) if n else float("nan")
    return Stats(n, mean, median, std, sem, q1, q3, iqr, mad)


def main(DATA_PATH: str):
    df = pd.read_csv(DATA_PATH)

    time_col = pick_time_column(df)
    alt_col = pick_altitude_column(df)

    # Zaman ekseni: varsa parse etmeye çalış, yoksa index kullan
    if time_col is not None:
        t = pd.to_datetime(df[time_col], errors="coerce")
        # parse başarısızsa fallback
        if t.isna().all():
            t = pd.Series(np.arange(len(df)), name="index")
            time_label = "Sample index"
        else:
            time_label = time_col
    else:
        t = pd.Series(np.arange(len(df)), name="index")
        time_label = "Sample index"

    alt_m = to_altitude_meters(df[alt_col], alt_col)

    # Temizle
    valid = np.isfinite(alt_m.values)
    alt_m = alt_m[valid].reset_index(drop=True)
    t = t[valid].reset_index(drop=True)

    # Uçuşu ayırmak için basit eşik: 1 m üstü "havada" sayalım
    in_air = (alt_m.values > 1.0)

    # Kısa veri boşluklarını kapat: örnekleme aralığını bilmiyorsak 5 örneklik boşluğu kapat
    in_air_filled = fill_short_gaps(in_air, max_gap=5)

    # En uzun "havada" segmenti al: bu genelde görev uçuşu (stabil bölüm) oluyor
    s, e = longest_true_segment(in_air_filled)

    if e - s < 10:
        print("Uyarı: Uçuş segmenti çok kısa bulundu. Eşik (1.0 m) uygun olmayabilir.")
        print("Alt kolon:", alt_col, "İlk değer örnekleri:", alt_m.head(10).to_list())

    # Segment verisi
    alt_all = alt_m.values
    alt_seg = alt_m.values[s:e]

    # İniş-kalkış etkisini azaltmak için (opsiyonel): segmentin içinden IQR ile outlier kırp
    seg_stats0 = robust_stats(alt_seg)
    lower = seg_stats0.q1 - 1.5 * seg_stats0.iqr
    upper = seg_stats0.q3 + 1.5 * seg_stats0.iqr
    alt_seg_clean = alt_seg[(alt_seg >= lower) & (alt_seg <= upper)]

    stats_all = robust_stats(alt_all)
    stats_seg = robust_stats(alt_seg)
    stats_clean = robust_stats(alt_seg_clean)

    # ---- Sonuçları yazdır ----
    print("\n=== Sütunlar ===")
    print(f"Yükseklik sütunu: {alt_col}  -> metreye çevrildi: evet")
    print(f"Toplam örnek sayısı: {len(alt_all)}")
    print(f"Seçilen uçuş segmenti: [{s}:{e}] (n={len(alt_seg)})")

    print("\n=== Tüm veri (ground + uçuş) ===")
    print(f"Mean   = {stats_all.mean:.3f} m")
    print(f"Median = {stats_all.median:.3f} m")

    print("\n=== Uçuş segmenti (en uzun havada bölüm) ===")
    print(f"Mean   = {stats_seg.mean:.3f} m")
    print(f"Median = {stats_seg.median:.3f} m")
    print(f"IQR    = {stats_seg.iqr:.3f} m  | MAD = {stats_seg.mad:.3f} m")

    print("\n=== Uçuş segmenti (IQR-outlier temizliği sonrası) ===")
    print(f"Mean   = {stats_clean.mean:.3f} m")
    print(f"Median = {stats_clean.median:.3f} m")
    print(f"Std    = {stats_clean.std:.3f} m  | SEM = {stats_clean.sem:.3f} m")

    # Görev raporu için öneri:
    # "Tipik uçuş yüksekliği" = median(clean) ve yayılım = IQR/2 veya MAD
    print("\n>>> Önerilen 'tipik uçuş yüksekliği' (robust):")
    print(f"h_typ ≈ {stats_clean.median:.2f} m  (robust yayılım ~ MAD={stats_clean.mad:.2f} m veya IQR={stats_clean.iqr:.2f} m)")

    # ---- Grafikler ----
    # 1) Zaman serisi
    plt.figure()
    plt.plot(t, alt_m, linewidth=1)
    plt.axvspan(t.iloc[s], t.iloc[e-1], alpha=0.2, label="seçilen uçuş segmenti")
    plt.title("Yükseklik (metre) - zaman")
    plt.xlabel(time_label)
    plt.ylabel("Altitude [m]")
    plt.legend()
    plt.tight_layout()
    plt.savefig("altitude_timeseries.png", dpi=160)

    # 2) Segment histogramı: mean vs median farkı görünür
    plt.figure()
    plt.hist(alt_seg, bins=40)
    plt.axvline(stats_seg.mean, linestyle="--", linewidth=2, label=f"mean={stats_seg.mean:.2f} m")
    plt.axvline(stats_seg.median, linestyle="-", linewidth=2, label=f"median={stats_seg.median:.2f} m")
    plt.title("Uçuş segmenti yükseklik dağılımı")
    plt.xlabel("Altitude [m]")
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()
    plt.savefig("altitude_segment_hist.png", dpi=160)

    print("\nGrafikler kaydedildi: altitude_timeseries.png, altitude_segment_hist.png")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python drone_altitude_analysis.py data.csv")
        sys.exit(1)
    main(sys.argv[1])