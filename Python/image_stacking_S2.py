import os
import numpy as np
from astropy.io import fits
import astroalign as aa
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage

# -------------------------------------------------
# 1. OUTPUT MAP (DESKTOP)
# -------------------------------------------------
import os

output_dir = "/Users/ilkatonnaer/Desktop/astro_output"
os.makedirs(output_dir, exist_ok=True)

fits_path = os.path.join(output_dir, "stack_S2.fits")

# -------------------------------------------------
# 2. INPUT DATA
# -------------------------------------------------
map_fits = '/Users/ilkatonnaer/Documents/AA Uni/jaar 1 (2nd edition)/Eerstejaarsproject/reduced_data/O3'

alle_fits = sorted([
    os.path.join(map_fits, f)
    for f in os.listdir(map_fits)
    if f.lower().endswith('.fits')
])

print("Aantal frames gevonden:", len(alle_fits))

# -------------------------------------------------
# 3. REFERENCE FRAME
# -------------------------------------------------
reference = np.array(fits.getdata(alle_fits[14]), dtype=np.float32)
ref_clean = ndimage.median_filter(reference, size=3)

# -------------------------------------------------
# 4. ALIGNMENT
# -------------------------------------------------
aligned_images = []

print("\nStart alignment...")

for i, f in enumerate(alle_fits):
    try:
        data = np.array(fits.getdata(f), dtype=np.float32)
        data_clean = ndimage.median_filter(data, size=3)

        aligned, footprint = aa.register(data_clean, ref_clean)

        aligned_images.append(aligned)

        print(f"{i+1}/{len(alle_fits)} OK")

    except Exception as e:
        print(f"{i+1}/{len(alle_fits)} SKIP: {e}")

print("\nAligned frames:", len(aligned_images))

if len(aligned_images) == 0:
    raise RuntimeError("Geen enkele frame kon worden uitgelijnd.")

# -------------------------------------------------
# 5. STACK
# -------------------------------------------------
print("Stacking...")

stack = np.zeros_like(aligned_images[0], dtype=np.float32)

for img in aligned_images:
    stack += img

stack /= len(aligned_images)

stack = np.nan_to_num(stack)

# -------------------------------------------------
# 6. BACKGROUND REMOVAL
# -------------------------------------------------
background = np.median(stack)
stack = stack - background
stack[stack < 0] = 0

# -------------------------------------------------
# 7. ROTATIE (PAS DIT AAN ALS NODIG)
# -------------------------------------------------
ROTATE = True   # zet op False als niet nodig
K = 1           # 1 = 90° CCW, -1 = CW, 2 = 180°

if ROTATE:
    stack = np.rot90(stack, k=K)

# -------------------------------------------------
# 8. STRETCH FOR VISUALIZATION
# -------------------------------------------------
stack_img = np.arcsinh(stack)
stack_img = np.nan_to_num(stack_img)

# -------------------------------------------------
# 9. SAVE FITS
# -------------------------------------------------
fits_path = os.path.join(output_dir, "crab_stack_SII.fits")

hdu = fits.PrimaryHDU(stack.astype(np.float32))
hdu.writeto(fits_path, overwrite=True)

print("FITS saved:", fits_path)

# -------------------------------------------------
# 10. SAVE PNG
# -------------------------------------------------
png_path = os.path.join(output_dir, "crab_stack_SII.png")

vmin = np.percentile(stack_img, 5)
vmax = np.percentile(stack_img, 99.7)

plt.figure(figsize=(10, 10))
plt.imshow(stack_img, cmap='gray', vmin=vmin, vmax=vmax)
plt.axis("off")
plt.title("SIICrab Nebula")

plt.savefig(png_path, dpi=300, bbox_inches='tight', pad_inches=0)
plt.close()

print("PNG saved:", png_path)

print("\nDONE ✔")