from PIL import Image
import numpy as np
from scipy import ndimage

img = Image.open('logo2_v4_transparent.png')
arr = np.array(img)
alpha = arr[:,:,3]

# Remove any remaining small disconnected alpha blobs (like the corner smudges)
# Keep only the single largest connected component (the emblem itself)
mask = alpha > 30
labeled, num = ndimage.label(mask, structure=np.ones((3,3)))
if num > 0:
    sizes = ndimage.sum(mask, labeled, range(1, num + 1))
    largest_label = np.argmax(sizes) + 1
    main_mask = labeled == largest_label
    print(f'Total components: {num}, largest size: {sizes.max()}, total fg before: {mask.sum()}')

    # Zero out alpha for everything not part of the main emblem blob
    new_alpha = alpha.copy()
    new_alpha[~main_mask] = 0
    arr[:,:,3] = new_alpha

result = Image.fromarray(arr, 'RGBA')

# Trim to bounding box with small margin
bbox = result.getbbox()
trimmed = result.crop(bbox)
w, h = trimmed.size
margin = int(w * 0.035)
final_img = Image.new('RGBA', (w + margin*2, h + margin*2), (0,0,0,0))
final_img.paste(trimmed, (margin, margin), trimmed)
final_img.save('logo2_final_clean.png')
print('Final clean size:', final_img.size)
