import numpy as np
import matplotlib.pyplot as plt

class FTIRAnalyzer:
    def __init__(self, x_cm, I_x, c=3.0e8):
        self.x_cm = np.asarray(x_cm, dtype=float)
        self.I_x = np.asarray(I_x, dtype=float)
        self.c = c

        # cm -> m
        self.x_m = self.x_cm * 1e-2

        # t = 2x/c (s)
        self.t_s = 2.0 * self.x_m / self.c
        self.t_ps = self.t_s * 1e12

    def compute_spectrum(self, remove_dc=True):
        signal = self.I_x - np.mean(self.I_x) if remove_dc else self.I_x

        dt = self.t_s[1] - self.t_s[0]
        N = len(self.t_s)

        S = np.fft.rfft(signal)                 # positive frequencies
        nu_hz = np.fft.rfftfreq(N, d=dt)
        nu_thz = nu_hz / 1e12

        self.nu_thz = nu_thz
        self.S_mag = np.abs(S)

        return self.nu_thz, self.S_mag

    def plot_interferogram_and_spectrum(self):
        # ensure spectrum exists
        if not hasattr(self, "S_mag"):
            self.compute_spectrum(remove_dc=True)

        fig, ax = plt.subplots(1, 2, figsize=(10, 4))

        ax[0].plot(self.t_ps, self.I_x, "o-", label="I(t)")
        ax[0].set_xlabel("t (ps)")
        ax[0].set_ylabel("I(t) (arb. u.)")
        ax[0].set_title("Interferogramm")
        ax[0].grid(True)
        ax[0].legend()

        ax[1].plot(self.nu_thz, self.S_mag, "o-", label="|I(ν)|")
        ax[1].set_xlabel("ν (THz)")
        ax[1].set_ylabel("|I(ν)| (arb. u.)")
        ax[1].set_title("Spektrum (FFT)")
        ax[1].grid(True)
        ax[1].legend()

        plt.tight_layout()
        plt.show()


# ---------------- Example usage ----------------
x_cm = [0.00,0.02,0.04,0.06,0.08,0.10,0.12,0.14,0.16,0.18,0.20,0.22,0.24,0.26,0.28,0.30]
I_x  = [6500,5000,3572,5000,6231,5000,4038,5000,5681,5000,4564,5000,5254,5000,4867,5000]

analyzer = FTIRAnalyzer(x_cm, I_x)
analyzer.compute_spectrum(remove_dc=True)
analyzer.plot_interferogram_and_spectrum()
