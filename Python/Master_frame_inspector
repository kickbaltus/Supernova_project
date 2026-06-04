from pathlib import Path
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

# ==========================================
# PAD NAAR JE DATA
# ==========================================

folder_path = r"C:\Documents\GitHub\Offline_bestanden_project\Ruwe_data\02-03-2026\Bias"

folder = Path(folder_path)

# ==========================================
# ALLEEN MASTER FILES LADEN
# ==========================================

master_files = [
    f for f in folder.iterdir()
    if "master" in f.name.lower()
    and f.suffix.lower() in [".fit", ".fits"]
]

print(f"\n{len(master_files)} master files gevonden")

for f in master_files:
    print(" -", f.name)

# ==========================================
# PLOT ELKE MASTER FILE
# ==========================================

for file in master_files:

    data = fits.getdata(file)

    print("\n=== INFO ===")
    print(file.name)
    print("Shape:", data.shape)
    print("Min:", np.min(data))
    print("Max:", np.max(data))
    print("Mean:", np.mean(data))
    print("Median:", np.median(data))

    plt.figure(figsize=(6, 5))

    img = plt.imshow(
        data,
        cmap="gray",
        origin="lower",
        vmin=0,
        vmax=65535   # 16-bit schaal
    )

    plt.title(file.name)
    plt.colorbar(img, label="Pixel value (ADU)")

    plt.show()