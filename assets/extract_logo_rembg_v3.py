from PIL import Image
from rembg import remove, new_session

img = Image.open('logo2.png').convert('RGBA')

# Run rembg on the FULL original image (emblem + text + everything),
# giving the model maximum context to correctly segment the ring's edges.
session = new_session(model_name='isnet-general-use')
result = remove(img, session=session)
result.save('logo2_rembg_v3_full.png')
print('Full image bbox:', result.getbbox(), 'original size:', img.size)
