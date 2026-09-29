"""
Gera a imagem de preview (Open Graph) usada quando o link do site
é compartilhado no WhatsApp, Instagram, Facebook, etc.
Tamanho recomendado: 1200x630px.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630

# Brand colors (matching styles.css)
NAVY_900 = (11, 33, 56)
NAVY_700 = (18, 58, 107)
BLUE_600 = (30, 95, 168)
GOLD_600 = (201, 162, 39)
GOLD_400 = (240, 213, 119)
WHITE = (255, 255, 255)

img = Image.new('RGB', (W, H), NAVY_900)
draw = ImageDraw.Draw(img)

# Diagonal gradient background (navy -> blue), approximated with horizontal bands
for x in range(W):
    t = x / W
    r = int(NAVY_900[0] + (BLUE_600[0] - NAVY_900[0]) * t * 0.7)
    g = int(NAVY_900[1] + (BLUE_600[1] - NAVY_900[1]) * t * 0.7)
    b = int(NAVY_900[2] + (BLUE_600[2] - NAVY_900[2]) * t * 0.7)
    draw.line([(x, 0), (x, H)], fill=(r, g, b))

# Soft gold glow circles, symmetric on both top corners (subtle, behind content)
glow = Image.new('RGBA', (500, 500), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
glow_draw.ellipse([0, 0, 500, 500], fill=(*GOLD_400, 45))
img_rgba = img.convert('RGBA')
img_rgba.paste(glow, (W - 320, -280), glow)
img_rgba.paste(glow, (-180, -280), glow)
img = img_rgba.convert('RGB')
draw = ImageDraw.Draw(img)

# Fonts - try common Windows fonts, fallback to default
def load_font(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

title_font = load_font([
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
], 54)
subtitle_font = load_font([
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
], 28)
tag_font = load_font([
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
], 24)

def text_w(text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]

# --- Everything centered horizontally within a "safe zone" (WhatsApp/FB often
# crop the sides of a 1200x630 image, so keep all content inside the central
# ~85% width to avoid text getting cut off) ---
center_x = W // 2

# Logo (centered)
logo_h = 150
try:
    logo = Image.open('logo-novo.png').convert('RGBA')
    ratio = logo_h / logo.size[1]
    logo_w = int(logo.size[0] * ratio)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
    logo_y = 60
    img.paste(logo, (center_x - logo_w // 2, logo_y), logo)
    content_top = logo_y + logo_h + 40
except Exception as e:
    print('Logo paste skipped:', e)
    content_top = 140

# Title text (each line centered)
title_lines = ["Formalize seu negócio.", "Organize sua contabilidade."]
y = content_top
line_height = 64
for line in title_lines:
    tw = text_w(line, title_font)
    draw.text((center_x - tw // 2, y), line, font=title_font, fill=WHITE)
    y += line_height

# Subtitle (centered)
subtitle = "Assessoria e Consultoria Contábil para MEI, CNPJ e Empresas"
sw = text_w(subtitle, subtitle_font)
draw.text((center_x - sw // 2, y + 18), subtitle, font=subtitle_font, fill=(220, 228, 238))
y += 18 + 40

# Gold pill badge (centered)
badge_text = "formalizeeorganize.com.br"
bbox = draw.textbbox((0, 0), badge_text, font=tag_font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
pad_x, pad_y = 26, 14
badge_w = tw + pad_x * 2
badge_h = th + pad_y * 2
badge_x = center_x - badge_w // 2
badge_y = y + 22
draw.rounded_rectangle(
    [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
    radius=badge_h // 2, fill=GOLD_600
)
draw.text((badge_x + pad_x, badge_y + pad_y - 2), badge_text, font=tag_font, fill=NAVY_900)

img.save('og-image.jpg', quality=90)
print('Saved og-image.jpg, size:', img.size)
