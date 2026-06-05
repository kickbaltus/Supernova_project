from pathlib import Path
import numpy as np
from ccdproc import CCDData, combine
import warnings
from astropy.utils.exceptions import AstropyWarning

warnings.simplefilter("ignore", AstropyWarning)
# ==========================================
# INSTELLINGEN
# ==========================================

folder_path = r"C:\Documents\GitHub\Offline_bestanden_project\Ruwe_data\05-03-2026\Dark_5"
frame_type = "dark"   # bias / dark / flat

folder = Path(folder_path)

# ==========================================
# BESTANDEN ZOEKEN (ROBUST)
# ==========================================

fits_files = [
    f for f in folder.iterdir()
    if frame_type in f.name.lower()
    and f.suffix.lower() in [".fit", ".fits"]
]

print(f"\n{len(fits_files)} {frame_type} files gevonden")

# Debug (handig!)
print("\nGevonden bestanden:")
for f in fits_files:
    print(" -", f.name)

# ==========================================
# VEILIGHEIDSCHECK
# ==========================================

if len(fits_files) == 0:
    raise ValueError(
        f"Geen {frame_type} bestanden gevonden. "
        f"Check naam of extensie (.fit/.fits)."
    )

# ==========================================
# INLEZEN
# ==========================================

ccd_list = [CCDData.read(f, unit="adu") for f in fits_files]

# ==========================================
# COMBINEREN (MEDIAN STACK)
# ==========================================

master_frame = combine(ccd_list, method="median")

# ==========================================
# STATISTIEK CHECK
# ==========================================

data = master_frame.data

print("\n=== CHECK MASTER FRAME ===")
print("Mediaan:", np.median(data))
print("Gemiddelde:", np.mean(data))
print("Min:", np.min(data))
print("Max:", np.max(data))

# ==========================================
# OPSLAAN
# ==========================================

output_file = folder / f"Master_{frame_type.capitalize()}.fits"

master_frame.write(output_file, overwrite=True)

print("\nSaved:", output_file)