import os
import numpy as np
from astropy.io import fits
import astroalign as aa
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage

# 1. Map en bestanden inladen
map_fits = '/Users/ilkatonnaer/Documents/AA Uni/jaar 1 (2nd edition)/Eerstejaarsproject/reduced_data/Ha 2'

alle_fits = sorted([
    os.path.join(map_fits, f)
    for f in os.listdir(map_fits)
    if f.lower().endswith('.fits')
])

print("Aantal frames gevonden:", len(alle_fits))

# 2. Referentieframe
reference = np.array(fits.getdata(alle_fits[14]), dtype=np.float32)
ref_clean = ndimage.median_filter(reference, size=3)

aligned_images = []

print("\nStarten met uitlijnen...")
for i, f in enumerate(alle_fits):
    try:
        data = np.array(fits.getdata(f), dtype=np.float32)

        # hot pixel removal
        data_clean = ndimage.median_filter(data, size=3)

        aligned, footprint = aa.register(data_clean, ref_clean)

        aligned_images.append(aligned)
        print(f"{i+1}/{len(alle_fits)} OK")

    except Exception as e:
        print(f"{i+1}/{len(alle_fits)} SKIP: {e}")

print("\nAantal succesvol uitgelijnde frames:", len(aligned_images))

if len(aligned_images) == 0:
    raise RuntimeError("Geen frames uitgelijnd.")

# 3. MEMORY-FRIENDLY STACK (belangrijk fix!)
print("Beelden stacken...")

stack = np.zeros_like(aligned_images[0], dtype=np.float32)

for img in aligned_images:
    stack += img

stack /= len(aligned_images)

stack = np.nan_to_num(stack)

# 4. Achtergrondcorrectie
background = np.median(stack)
stack = stack - background
stack[stack < 0] = 0

# 5. Stretch voor zichtbaarheid
stack_img = np.arcsinh(stack)
stack_img = np.nan_to_num(stack_img)

# 7. PNG EXPORT (VISUAL)
vmin = np.percentile(stack_img, 5)
vmax = np.percentile(stack_img, 99.7)

plt.figure(figsize=(10, 10))
plt.imshow(stack_img, cmap='gray', vmin=vmin, vmax=vmax)
plt.title("H-alpha Crab Nebula")
plt.colorbar(label="Intensity (arcsinh)")
plt.show()