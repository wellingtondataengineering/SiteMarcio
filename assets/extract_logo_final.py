from PIL import Image
import numpy as np

# Load the full image with background already removed by rembg
full = Image.open('logo2_rembg_v3_full.png').convert('RGBA')
w, h = full.size
print('Full transparent image size:', (w, h))

# Crop just the emblem (above the "FORMALIZE E ORGANIZE" text)
# Based on visual inspection, the emblem ends around y=0.47*h and text starts after
crop_bottom = int(h * 0.47)
emblem = full.crop((0, 0, w, crop_bottom))

# Trim to the actual bounding box of non-transparent pixels within this crop
bbox = emblem.getbbox()
print('Emblem bbox within crop:', bbox)
trimmed = emblem.crop(bbox)
tw, th = trimmed.size

# Add a small transparent margin
margin = int(tw * 0.03)
final_img = Image.new('RGBA', (tw + margin*2, th + margin*2), (0,0,0,0))
final_img.paste(trimmed, (margin, margin), trimmed)
final_img.save('logo2_final_v2.png')
print('Saved final logo, size:', final_img.size)
