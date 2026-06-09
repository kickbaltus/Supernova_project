import os
import numpy as np
from astropy.io import fits
import astroalign as aa
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage

# -------------------------------------------------
# 1. OUTPUT MAP (DESKTOP)
# -------------------------------------------------
output_dir = "/Users/ilkatonnaer/Desktop/astro_output"
os.makedirs(output_dir, exist_ok=True)

print("Output folder:", output_dir)

# -------------------------------------------------
# 2. FILTER SETUP
# -------------------------------------------------
filters = {
    "Ha": "/Users/ilkatonnaer/Documents/AA Uni/jaar 1 (2nd edition)/Eerstejaarsproject/reduced_data/Ha",
    "S2": "/Users/ilkatonnaer/Documents/AA Uni/jaar 1 (2nd edition)/Eerstejaarsproject/reduced_data/S2",
    "O3": "/Users/ilkatonnaer/Documents/AA Uni/jaar 1 (2nd edition)/Eerstejaarsproject/reduced_data/O3"
}

# -------------------------------------------------
# 3. PROCESS FUNCTION (IDENTIEK AAN JOUW CODE)
# -------------------------------------------------
def process_filter(name, map_fits):

    print(f"\n==============================")
    print(f"Processing {name}")
    print(f"==============================")

    alle_fits = sorted([
        os.path.join(map_fits, f)
        for f in os.listdir(map_fits)
        if f.lower().endswith('.fits')
    ])

    print("Aantal frames gevonden:", len(alle_fits))

    if len(alle_fits) == 0:
        print("Geen files → skip")
        return

    # -------------------------------------------------
    # REFERENCE FRAME
    # -------------------------------------------------
    reference = np.array(fits.getdata(alle_fits[14]), dtype=np.float32)
    ref_clean = ndimage.median_filter(reference, size=3)

    # -------------------------------------------------
    # ALIGNMENT
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
        print("Geen aligned frames → skip")
        return

    # -------------------------------------------------
    # STACK
    # -------------------------------------------------
    print("Stacking...")

    stack = np.zeros_like(aligned_images[0], dtype=np.float32)

    for img in aligned_images:
        stack += img

    stack /= len(aligned_images)
    stack = np.nan_to_num(stack)

    # -------------------------------------------------
    # BACKGROUND REMOVAL
    # -------------------------------------------------
    background = np.median(stack)
    stack = stack - background
    stack[stack < 0] = 0

    # -------------------------------------------------
    # STRETCH
    # -------------------------------------------------
    stack_img = np.arcsinh(stack)
    stack_img = np.nan_to_num(stack_img)

    # -------------------------------------------------
    # SAVE FITS
    # -------------------------------------------------
    fits_path = os.path.join(output_dir, f"{name}_stack.fits")

    hdu = fits.PrimaryHDU(stack.astype(np.float32))
    hdu.writeto(fits_path, overwrite=True)

    print("Saved FITS:", fits_path)

    # -------------------------------------------------
    # SAVE PNG
    # -------------------------------------------------
    png_path = os.path.join(output_dir, f"{name}_stack.png")

    vmin = np.percentile(stack_img, 5)
    vmax = np.percentile(stack_img, 99.7)

    plt.figure(figsize=(10, 10))
    plt.imshow(stack_img, cmap='gray', vmin=vmin, vmax=vmax)
    plt.axis("off")
    plt.title(f"{name} Crab Nebula")

    plt.savefig(png_path, dpi=300, bbox_inches='tight', pad_inches=0)

    print("Saved PNG:", png_path)

    plt.close()

    print(f"{name} DONE ✔")

# -------------------------------------------------
# 4. RUN ALL FILTERS (ONDER ELKAAR)
# -------------------------------------------------
for name, path in filters.items():
    process_filter(name, path)

print("\nALL FILTERS DONE ✔")