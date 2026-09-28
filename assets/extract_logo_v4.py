from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage

img = Image.open('logo2.png').convert('RGBA')
w, h = img.size
crop_bottom = int(h * 0.47)
cropped = img.crop((0, 0, w, crop_bottom))
cw, ch = cropped.size
arr = np.array(cropped).astype(np.float32)

r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
max_c = np.max(arr[:,:,:3], axis=2)
min_c = np.min(arr[:,:,:3], axis=2)
sat = max_c - min_c

# Same base mask as v1 (this one preserved the emblem shape correctly)
is_grayish = (sat < 35) & (max_c > 40) & (max_c < 210)
fg_mask = ~is_grayish  # foreground = NOT grayish background

# Clean up: remove small isolated foreground speckles (noise in the background area)
# A real speckle/noise blob is small; the real emblem is one large connected mass.
labeled, num_features = ndimage.label(fg_mask, structure=np.ones((3,3)))
sizes = ndimage.sum(fg_mask, labeled, range(1, num_features + 1))
# Keep only components larger than a threshold (removes small dust specks)
min_size = 40
keep_labels = np.where(sizes >= min_size)[0] + 1
fg_mask_clean = np.isin(labeled, keep_labels)

print(f'Components: {num_features}, kept: {len(keep_labels)}, fg pixels before: {fg_mask.sum()}, after: {fg_mask_clean.sum()}')

# Fill small holes inside the emblem (in case cleanup created gaps)
fg_mask_filled = ndimage.binary_fill_holes(fg_mask_clean)

# Slight morphological closing to smooth jagged edges from speckle removal
fg_mask_smooth = ndimage.binary_closing(fg_mask_filled, structure=np.ones((3,3)), iterations=1)

alpha = (fg_mask_smooth.astype(np.float32) * 255)

out = arr.copy()
out[:,:,3] = alpha
out = np.clip(out, 0, 255).astype(np.uint8)
result = Image.fromarray(out, 'RGBA')

# Feather the alpha edge slightly for smooth anti-aliasing
r2, g2, b2, a2 = result.split()
a2_smooth = a2.filter(ImageFilter.GaussianBlur(radius=1.0))
result = Image.merge('RGBA', (r2, g2, b2, a2_smooth))

result.save('logo2_v4_transparent.png')
print('Saved v4, size:', result.size)
