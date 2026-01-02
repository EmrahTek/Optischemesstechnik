"""
Mit einem FTIR-Spektrometer wurde ein räumliches Interferogramm I(x) aufgenommen.
Die erste Spalte enthält die Spiegelposition x in µm (äquidistant), die zweite Spalte die Intensität in arb. Einheiten.


a) Wandeln Sie x in eine Zeitachse t um (t = 2x/c). Verwenden Sie c = 3.0·10^8 m/s.
b) Berechnen Sie das Betragsspektrum |I(ν)| mittels FFT (numpy.fft.fft).
c) Erstellen Sie eine Abbildung mit zwei horizontal angeordneten Plots: links I(t) gegen t, rechts |I(ν)| gegen ν (nur positive Frequenzen).
d) Beschriften Sie Achsen und fügen Sie jeweils eine Legende ein.


"""

# The task:
# 1) Convert mirror position x (in µm) to time axis t using t = 2x/c
# 2) Compute the magnitude spectrum |I(nu)| using FFT
# 3) Plot I(t) vs t and |I(nu)| vs nu (positive frequencies only) side-by-side

import numpy as np
import matplotlib.pyplot as plt

def main() -> None:
    # -----------------------------
    # Given measurement data (table)
    # -----------------------------
    # x positions in micrometers (µm), equidistant
    x_um = np.arange(0, 16, 1)

    # Interferogram intensity I(x) in arbitrary units
    I = np.array([
        1.00, 0.94, 0.78, 0.54,
        0.27, 0.05, 0.02, 0.10,
        0.30, 0.56, 0.80, 0.95,
        1.00, 0.93, 0.76, 0.52
    ], dtype=float)

    # -----------------------------
    # (a) Convert x -> t: t = 2x / c
    # -----------------------------
    c = 3.0e8  # speed of light [m/s]

    # Convert µm to meters
    x_m = x_um * 1e-6  # [m]

    # Time axis [s]
    t = 2.0 * x_m / c  # [s]

    # Sampling interval in time domain (must be constant for FFT frequency axis)
    dt = t[1] - t[0]  # [s]

    # -----------------------------
    # (b) FFT and magnitude spectrum
    # -----------------------------
    # FFT of the signal
    I_fft = np.fft.fft(I)

    # Magnitude spectrum |I(nu)|
    mag = np.abs(I_fft)

    # Frequency axis (nu) corresponding to FFT bins
    # np.fft.fftfreq returns frequencies in Hz (cycles per second)
    nu = np.fft.fftfreq(len(I), d=dt)  # [Hz]

    # Keep only positive frequencies (as requested)
    pos_mask = nu > 0
    nu_pos = nu[pos_mask]
    mag_pos = mag[pos_mask]

    # -----------------------------
    # (c) Plot: two horizontal subplots
    # -----------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Left plot: I(t) vs t
    axes[0].plot(t, I, marker="o", label="Interferogram I(t)")
    axes[0].set_xlabel("Time t [s]")
    axes[0].set_ylabel("Intensity I(t) [arb. u.]")
    axes[0].legend()
    axes[0].grid(True)

    # Right plot: |I(nu)| vs nu (positive frequencies only)
    axes[1].plot(nu_pos, mag_pos, marker="o", label="Magnitude |I(ν)|")
    axes[1].set_xlabel("Frequency ν [Hz]")
    axes[1].set_ylabel("Magnitude |I(ν)| [arb. u.]")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()






