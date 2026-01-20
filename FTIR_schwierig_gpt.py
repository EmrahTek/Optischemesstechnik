import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters (units!)
# -----------------------------
dx_mirror = 2e-6   # mirror step [m]
N = 4096           # number of samples

# Wavenumbers given in cm^-1 -> convert to m^-1 (1 cm^-1 = 100 m^-1)
sigma1 = 3030.0 * 100.0   # [1/m]
sigma2 = 2900.0 * 100.0   # [1/m]

noise_sigma = 0.02        # interferogram noise amplitude [a.u.]

# -----------------------------
# (a) OPD axis δ (m), symmetric around 0
# OPD: δ = 2*x, with x being mirror position
# Step in OPD: dδ = 2*dx_mirror
# -----------------------------
d_delta = 2.0 * dx_mirror                 # [m]
delta = (np.arange(N) - N/2) * d_delta    # [m], symmetric around 0 (center at index N/2)

# -----------------------------
# (b) Simulate interferogram I(δ)
# I(δ) = cos(2πσ1δ) + 0.6 cos(2πσ2δ) + noise
# -----------------------------
rng = np.random.default_rng(0)  # reproducible
I = np.cos(2*np.pi*sigma1*delta) + 0.6*np.cos(2*np.pi*sigma2*delta)
I += noise_sigma * rng.standard_normal(N)

# -----------------------------
# (c) Remove DC, apply Hann window, rFFT magnitude
# Note: shifting the interferogram in δ only changes PHASE, not magnitude.
# -----------------------------
I_dc_removed = I - np.mean(I)
window = np.hanning(N)                 # Hann window (same idea as Hanning)
I_win = I_dc_removed * window

S = np.fft.rfft(I_win)                # rFFT (positive wavenumbers only)
S_mag = np.abs(S) / N                 # magnitude (simple normalization)

# -----------------------------
# (d) Wavenumber axis (cm^-1)
# rfftfreq gives frequencies in cycles per meter [1/m] because d is in meters.
# Convert 1/m -> cm^-1 by dividing by 100.
# -----------------------------
sigma_axis_m = np.fft.rfftfreq(N, d=d_delta)   # [1/m]
sigma_axis_cm = sigma_axis_m / 100.0           # [cm^-1]

# -----------------------------
# (e) Find two largest peaks in 2500-3500 cm^-1 (exclude sigma=0)
# -----------------------------
roi = (sigma_axis_cm >= 2500) & (sigma_axis_cm <= 3500) & (sigma_axis_cm > 0)
sigma_roi = sigma_axis_cm[roi]
S_roi = S_mag[roi]

# Peak picking (NumPy-only): use local maxima; fallback to global sort if needed
is_peak = (S_roi[1:-1] > S_roi[:-2]) & (S_roi[1:-1] > S_roi[2:])
peak_idx = np.where(is_peak)[0] + 1

if peak_idx.size >= 2:
    top2 = peak_idx[np.argsort(S_roi[peak_idx])[-2:]]
else:
    top2 = np.argsort(S_roi)[-2:]  # fallback

# Convert to actual peak values, sort by wavenumber
peak_sigmas = sigma_roi[top2]
peak_amps = S_roi[top2]
order = np.argsort(peak_sigmas)
peak_sigmas = peak_sigmas[order]
peak_amps = peak_amps[order]

print("Top-2 Peaks in 2500–3500 cm^-1:")
for k, (s_cm, amp) in enumerate(zip(peak_sigmas, peak_amps), start=1):
    print(f"  Peak {k}: σ = {s_cm:.2f} cm^-1, |S| = {amp:.4g}")

# -----------------------------
# (f) Plot interferogram and spectrum
# -----------------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 4))

# Interferogram: use δ in mm for readability
ax[0].plot(delta * 1e3, I, lw=1)
ax[0].set_xlabel("OPD δ [mm]")
ax[0].set_ylabel("I(δ) [a.u.]")
ax[0].set_title("Interferogram")
ax[0].grid(True)

# Spectrum: show range around interest (e.g., 0–5000 cm^-1)
ax[1].plot(sigma_axis_cm, S_mag, lw=1, label="|S(σ)| (rFFT)")
ax[1].set_xlim(0, 5000)
ax[1].set_xlabel("Wellenzahl σ [cm⁻¹]")
ax[1].set_ylabel("|S(σ)| [a.u.]")
ax[1].set_title("Spectrum (magnitude)")
ax[1].grid(True)

# Mark peaks
for s_cm in peak_sigmas:
    ax[1].axvline(s_cm, linestyle="--")
    ax[1].text(s_cm, ax[1].get_ylim()[1]*0.85, f"{s_cm:.0f}", rotation=90,
               va="top", ha="center")

ax[1].legend()
plt.tight_layout()
plt.show()
