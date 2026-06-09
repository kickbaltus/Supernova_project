import numpy as np
from astropy.io import fits
import astroalign as aa
import matplotlib.pyplot as plt
import os
from scipy.ndimage import gaussian_filter

folder = "/Users/ilkatonnaer/Desktop/astro_output"

Ha  = np.array(fits.getdata(os.path.join(folder, "Ha_stack.fits")), dtype=np.float32)
SII = np.array(fits.getdata(os.path.join(folder, "S2_stack.fits")), dtype=np.float32)
OIII = np.array(fits.getdata(os.path.join(folder, "O3_stack.fits")), dtype=np.float32)

# -------------------------------------------------
# PREPROCESS (cruciaal voor astroalign)
# -------------------------------------------------
def prep(img):
    img = np.nan_to_num(img).astype(np.float32)

    img = img - np.median(img)
    img[img < 0] = 0

    img = gaussian_filter(img, sigma=2)

    return img

Ha  = prep(Ha)
SII = prep(SII)
OIII = prep(OIII)

ref = OIII

# -------------------------------------------------
# STABIELER ASTROALIGN
# -------------------------------------------------
aa.MAX_CONTROL_POINTS = 50

Ha_aligned, _  = aa.register(Ha, ref)
SII_aligned, _ = aa.register(SII, ref)
OIII_aligned = ref

# -------------------------------------------------
# NORMALIZE
# -------------------------------------------------
def norm(img):
    img = img - np.median(img)
    img = img / (np.std(img) + 1e-6)
    img = np.clip(img, -2, 5)
    return (img - img.min()) / (img.max() - img.min() + 1e-6)

R = norm(SII_aligned)
G = norm(Ha_aligned)
B = norm(OIII_aligned)

rgb = np.dstack([R, G, B])

# -------------------------------------------------
# STRETCH
# -------------------------------------------------
rgb = np.arcsinh(rgb * 3)
rgb = rgb / np.max(rgb)

# -------------------------------------------------
# SHOW
# -------------------------------------------------
plt.figure(figsize=(10,10))
plt.imshow(rgb)
plt.axis("off")
plt.title("SHO Crab Nebula")

plt.show()