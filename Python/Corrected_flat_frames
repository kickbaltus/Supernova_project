from pathlib import Path
from astropy.io import fits
import numpy as np

# ==========================================
# INSTELLINGEN
# ==========================================

flat_folder = Path(
    r"C:\Documents\GitHub\Offline_bestanden_project\Ruwe_data\02-03-2026\Flat_OIII"
)

master_dark_path = Path(
    r"C:\Documents\GitHub\Offline_bestanden_project\Ruwe_data\02-03-2026\Dark_5\Master_Dark.fits"
)

# ==========================================
# MASTER DARK INLEZEN
# ==========================================

print("Master Dark laden...")

master_dark_data = fits.getdata(master_dark_path)

print("Master Dark shape:", master_dark_data.shape)

# ==========================================
# FLATS ZOEKEN
# ==========================================

flat_files = [
    f for f in flat_folder.iterdir()
    if "corrected" not in f.name.lower()
    and "flat" in f.name.lower()
    and f.suffix.lower() in [".fit", ".fits"]
]

print(f"\n{len(flat_files)} flats gevonden")

# ==========================================
# CORRECTIE UITVOEREN
# ==========================================

for flat_file in flat_files:

    print(f"\nVerwerken: {flat_file.name}")

    with fits.open(flat_file) as hdul:

        header = hdul[0].header
        flat_data = hdul[0].data.astype(np.float32)

    # Dark subtractie
    corrected_data = flat_data - master_dark_data

    print(
        f"Mediaan voor : {np.median(flat_data):.2f}"
    )

    print(
        f"Mediaan na   : {np.median(corrected_data):.2f}"
    )

    # Nieuwe naam maken
    output_name = (
        flat_file.stem + "_corrected" + flat_file.suffix
    )

    output_path = flat_folder / output_name

    fits.writeto(
        output_path,
        corrected_data,
        header,
        overwrite=True
    )

    print("Opgeslagen:", output_name)

print("\nAlle flats zijn gecorrigeerd.")