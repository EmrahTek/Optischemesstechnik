"""Aufgabe 15 – simplified version

This script loads a hyperspectral text file, builds a 3D data cube
(y, x, wavelength) and shows two wavelength images and simple
threshold-based material masks.
(Bu betik, hiperspektral metin dosyasını yükler, 3B bir veri küpü
(y, x, dalga boyu) oluşturur ve iki dalga boyu görüntüsünü
ve basit eşik tabanlı malzeme maskelerini gösterir.)
"""

from pathlib import Path  # Handle file paths in an OS‑independent way (Dosya yollarını işletim sisteminden bağımsız şekilde yönetmek için)

import numpy as np  # Numerical computing (Sayısal hesaplamalar için)
import matplotlib.pyplot as plt  # Plotting library (Grafik çizimi için kütüphane)


# ---------------------------------------------------------------------------
# Configuration (Konfigürasyon ayarları)
# ---------------------------------------------------------------------------
DATA_PATH = Path(
    "C:/Users/emrah/OneDrive/Desktop/Photonic Studium/5. Semester 2025 - 2026/Optischemesstechnik_1/Aufgabe_Python/Aufgabe_15/Redye_demo_spektrum_vertical.txt"
)  # Path to the text file (Metin dosyasının yolu)

# Region of interest in the original camera image (Orijinal kamera görüntüsündeki ilgi bölgesi)
X_START = 66
Y_START = 11
X_END = 281
Y_END = 102

# Derived image size of the region of interest (İlgi bölgesinin türetilen görüntü boyutu)
X_N = X_END - X_START + 1
Y_N = Y_END - Y_START + 1

# Wavelength indices that we want to visualize (Görselleştirmek istediğimiz dalga boyu indeksleri)
PLOT_INDEX_1 = 82
PLOT_INDEX_2 = 223


# ---------------------------------------------------------------------------
# Data loading and cube construction (Veri yükleme ve küp oluşturma)
# ---------------------------------------------------------------------------

def load_hyperspectral_txt(path: Path):
    """Load the hyperspectral text file.

    Assumes:
      * First 42 rows are header/meta data.
      * First column is wavelength [nm].
      * Remaining columns are flattened image pixels.
    (Varsayımlar:
      * İlk 42 satır başlık/meta veridir.
      * İlk sütun dalga boyu [nm] bilgisidir.
      * Kalan sütunlar düzleştirilmiş görüntü pikselleridir.)
    """

    data = np.loadtxt(path, skiprows=42)  # Load numeric values (Sayısal değerleri yükle)
    wavelengths = data[:, 0]  # Wavelength axis [nm] (Dalga boyu ekseni [nm])
    flat_pixels = data[:, 1:]  # Flattened image pixels (Düzleştirilmiş görüntü pikselleri)
    return wavelengths, flat_pixels


def build_datacube(flat_pixels: np.ndarray, y_n: int, x_n: int) -> np.ndarray:
    """Convert flattened pixel matrix to a data cube (y, x, lambda).

    flat_pixels shape: (num_wavelengths, y_n * x_n)
    output shape:       (y_n, x_n, num_wavelengths)
    (flat_pixels şekli: (dalga_boyu_sayısı, y_n * x_n)
     çıktı şekli:       (y_n, x_n, dalga_boyu_sayısı))
    """

    num_wavelengths = flat_pixels.shape[0]  # Number of spectral bands (Spektral bant sayısı)

    # Reshape to (num_wavelengths, y_n, x_n) then reorder axes to (y_n, x_n, num_wavelengths)
    # (Önce (dalga_boyu_sayısı, y_n, x_n) şekline getir, sonra eksenleri (y_n, x_n, dalga_boyu_sayısı) olacak şekilde sırala)
    cube = flat_pixels.reshape(num_wavelengths, y_n, x_n).transpose(1, 2, 0)
    return cube


# ---------------------------------------------------------------------------
# Visualization helpers (Görselleştirme yardımcı fonksiyonları)
# ---------------------------------------------------------------------------

def plot_two_wavelength_slices(datacube: np.ndarray, wavelengths: np.ndarray,
                               idx1: int, idx2: int) -> None:
    """Show images at two wavelength indices.
    (İki dalga boyu indeksindeki görüntüleri göster.)
    """

    plt.figure(1)

    # First wavelength slice (İlk dalga boyu dilimi)
    plt.subplot(2, 1, 1)
    plt.imshow(datacube[:, :, idx1])
    plt.title(f"{wavelengths[idx1]:.1f} nm")

    # Second wavelength slice (İkinci dalga boyu dilimi)
    plt.subplot(2, 1, 2)
    plt.imshow(datacube[:, :, idx2])
    plt.title(f"{wavelengths[idx2]:.1f} nm")

    plt.tight_layout()  # Remove overlapping labels (Çakışan etiketleri azalt)


def create_mask(image_slice: np.ndarray, lower: float, upper: float) -> np.ndarray:
    """Create a boolean mask for pixels within [lower, upper].
    (Piksel değerleri [alt_sınır, üst_sınır] aralığında olanlar için mantıksal maske oluştur.)
    """

    return (lower < image_slice) & (image_slice < upper)


def plot_material_masks(datacube: np.ndarray, wavelengths: np.ndarray,
                        idx1: int, idx2: int) -> None:
    """Create and plot two material masks at two wavelengths.
    (İki dalga boyunda iki malzeme maskesi oluştur ve çiz.)
    """

    # Example thresholds – adapt to your data (Örnek eşik değerleri – kendi verine göre ayarla)
    material1_lower = 7000
    material1_upper = 10000
    material2_lower = 4000
    material2_upper = 6000

    mask1 = create_mask(datacube[:, :, idx1], material1_lower, material1_upper)
    mask2 = create_mask(datacube[:, :, idx2], material2_lower, material2_upper)

    plt.figure(2)

    plt.subplot(2, 1, 1)
    plt.imshow(mask1)
    plt.title(f"Mask @ {wavelengths[idx1]:.1f} nm")

    plt.subplot(2, 1, 2)
    plt.imshow(mask2)
    plt.title(f"Mask @ {wavelengths[idx2]:.1f} nm")

    plt.tight_layout()


# ---------------------------------------------------------------------------
# Main entry point (Ana giriş noktası)
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the full pipeline: load, build cube, plot images and masks.
    (Tüm hattı çalıştır: yükle, küp oluştur, görüntüleri ve maskeleri çiz.)
    """

    # Load wavelengths and flattened pixels from txt file (Dalga boylarını ve düzleştirilmiş pikselleri txt dosyasından yükle)
    wavelengths, flat_pixels = load_hyperspectral_txt(DATA_PATH)

    # Build 3D data cube (3B veri küpünü oluştur)
    datacube = build_datacube(flat_pixels, Y_N, X_N)

    # Show two spectral images (İki spektral görüntüyü göster)
    plot_two_wavelength_slices(datacube, wavelengths, PLOT_INDEX_1, PLOT_INDEX_2)

    # Show simple material masks (Basit malzeme maskelerini göster)
    plot_material_masks(datacube, wavelengths, PLOT_INDEX_1, PLOT_INDEX_2)

    # Finally display all figures (Son olarak tüm figürleri göster)
    plt.show()


if __name__ == "__main__":  # Run main only when executed directly (Betik doğrudan çalıştırıldığında main fonksiyonunu çalıştır)
    main()  # Start the program (Programı başlat)
