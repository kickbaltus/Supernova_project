from pathlib import Path
import numpy as np
from astropy.io import fits

# ==========================================
# INSTELLINGEN
# ==========================================

light_folder = Path(
    r"C:\Documents\GitHub\Offline_bestanden_project\Ruwe_data\02-03-2026\SII"
)

master_dark_path = Path(
    r"C:\Documents\GitHub\Offline_bestanden_project\Ruwe_data\02-03-2026\Dark_60\Master_Dark.fits"
)

# ==========================================
# MASTER DARK INLEZEN
# ==========================================

print("Loading master dark...")

master_dark = fits.getdata(master_dark_path).astype(np.float32)

print("Master dark loaded")

# ==========================================
# LIGHT FILES ZOEKEN
# ==========================================

light_files = [
    f for f in light_folder.iterdir()
    if f.suffix.lower() in [".fit", ".fits"]
    and "corrected" not in f.name.lower()
]

print(f"{len(light_files)} light frames gevonden")

# ==========================================
# DARK CORRECTIE
# ==========================================

for f in light_files:

    print("\nProcessing:", f.name)

    data, header = fits.getdata(f, header=True)
    data = data.astype(np.float32)

    # STEP 1: dark subtractie
    dark_corrected = data - master_dark

    print("Median raw:", np.median(data))
    print("Median dark-corr:", np.median(dark_corrected))

    # ======================================
    # OPSLAAN
    # ======================================

    output_name = f.stem + "_darkcorrected.fits"
    output_path = light_folder / output_name

    fits.writeto(
        output_path,
        dark_corrected,
        header,
        overwrite=True
    )

    print("Saved:", output_name)

print("\nAlle lights dark-gecorrigeerd.")