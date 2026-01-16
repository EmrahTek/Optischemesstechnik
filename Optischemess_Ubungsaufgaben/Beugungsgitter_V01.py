import numpy as np
import matplotlib.pyplot as plt

#---------Given parameters-----------
lines_per_mm = 1200 # grating density
m = 1               # diffraction order
lam0_nm = 633       # wavelength in nm
f_mm = 200          # focal length in mm
w_um_given = 30     # slit image width in micrometers

#-- Convert grating density to grating period d

d_mm = 1 / lines_per_mm # grating period in nm
lam0_nm = lam0_nm*1e-6  # convert nm -> d_mm


# (a) Littrow angle: m*λ = 2*d*sin(theta)
sin_theta = (m*lam0_nm) / (2*d_mm)
theta_rad = np.arcsin(sin_theta)
theta_deg = np.degrees(theta_rad)

# -----------------------------
# (b) Angular dispersion: dθ/dλ = m / (2*d*cosθ)
# Important: here λ is in mm, so result is rad/mm.
# Convert to rad/nm by dividing by 1e6 (because 1 mm = 1e6 nm).
# -----------------------------
dtheta_dlam_rad_per_mm = m / (2*d_mm*np.cos(theta_rad))
dtheta_dlam_rad_per_nm = dtheta_dlam_rad_per_mm / 1e6
dtheta_dlam_deg_per_nm = np.degrees(dtheta_dlam_rad_per_nm)

# -----------------------------
# (c) Linear dispersion: dx/dλ = f * dβ/dλ   (given in the task)
# Use f in mm -> dx/dλ will be mm/nm
# -----------------------------
dx_dlam_mm_per_nm = f_mm * dtheta_dlam_rad_per_nm


# Spectral resolution: Δλ = w / (dx/dλ)
w_mm_given = w_um_given / 1000.0 # um -> mm
delta_lam_nm_given = w_mm_given /dx_dlam_mm_per_nm

print(f"(a) Littrow angle theta = {theta_deg:.4f} deg")
print(f"(b) dβ/dλ = {dtheta_dlam_rad_per_nm:.6e} rad/nm  = {dtheta_dlam_deg_per_nm:.5f} deg/nm")
print(f"(c) dx/dλ = {dx_dlam_mm_per_nm:.6f} mm/nm = {dx_dlam_mm_per_nm*1000:.3f} µm/nm")
print(f"    For w = {w_um_given} µm: Δλ = {delta_lam_nm_given:.4f} nm")

# -----------------------------
# (d) Plot Δλ(w) for w = 10 ... 100 µm
# -----------------------------
w_um = np.linspace(10, 100, 200)
w_mm = w_um / 1000.0
delta_lam_nm = w_mm / dx_dlam_mm_per_nm

plt.figure()
plt.plot(w_um, delta_lam_nm)
plt.xlabel("Effective slit image width w (µm)")
plt.ylabel("Spectral resolution Δλ (nm)")
plt.title("Δλ(w) for Littrow grating spectrometer")
plt.grid(True)
plt.show()
