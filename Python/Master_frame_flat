from pathlib import Path
import numpy as np
from astropy.io import fits
from ccdproc import CCDData, combine

# ==========================================
# INSTELLINGEN
# ==========================================

base_folder = Path(
    r"C:\Documents\GitHub\Offline_bestanden_project\Ruwe_data\02-03-2026"
)

# subfolders per filter
flat_folders = {
    "Ha": base_folder / "Flat_Ha",
    "OIII": base_folder / "Flat_OIII",
    "SII": base_folder / "Flat_SII",
}

# ==========================================
# FUNCTIE: MASTER FLAT MAKEN
# ==========================================

def make_master_flat(folder: Path, filter_name: str):

    print(f"\n=== Processing {filter_name} ===")
    print("Folder:", folder)

    # 1. corrected flats zoeken
    flat_files = [
        f for f in folder.iterdir()
        if "corrected" in f.name.lower()
        and f.suffix.lower() in [".fit", ".fits"]
    ]

    print(f"{len(flat_files)} corrected flats gevonden")

    if len(flat_files) == 0:
        raise ValueError(f"Geen flats gevonden voor {filter_name}")

    ccd_list = []

    # 2. normaliseren per flat
    for f in flat_files:

        data = fits.getdata(f).astype(np.float32)

        med = np.median(data)

        if med == 0:
            print(f"Skipping {f.name} (median = 0)")
            continue

        norm_data = data / med

        print(f"{f.name} | median = {med:.2f}")

        ccd_list.append(
            CCDData(norm_data, unit="adu")
        )

    # 3. combineren
    master_flat = combine(ccd_list, method="median")

    # 4. output
    output_path = folder / f"Master_Flat_{filter_name}.fits"

    fits.writeto(
        output_path,
        master_flat.data,
        overwrite=True
    )

    print("\nSaved:", output_path)


# ==========================================
# RUN VOOR ALLE FILTERS
# ==========================================

for name, folder in flat_folders.items():
    make_master_flat(folder, name)

print("\nAlle master flats gemaakt.")