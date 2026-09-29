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

# Soft gold glow circle top-right
glow = Image.new('RGBA', (600, 600), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
glow_draw.ellipse([0, 0, 600, 600], fill=(*GOLD_400, 60))
glow = glow.filter(Image.Image.filter.__get__(glow, Image)) if False else glow
img_rgba = img.convert('RGBA')
img_rgba.paste(glow, (W - 400, -250), glow)
img = img_rgba.convert('RGB')
draw = ImageDraw.Draw(img)

# Load logo emblem and paste it (top-left area)
try:
    logo = Image.open('logo-novo.png').convert('RGBA')
    logo_h = 180
    ratio = logo_h / logo.size[1]
    logo_w = int(logo.size[0] * ratio)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
    img.paste(logo, (80, 90), logo)
except Exception as e:
    print('Logo paste skipped:', e)

# Fonts - try common Windows fonts, fallback to default
def load_font(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

title_font = load_font([
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
], 58)
subtitle_font = load_font([
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
], 30)
tag_font = load_font([
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
], 24)

# Title text
title_lines = ["Formalize seu negócio.", "Organize sua contabilidade."]
y = 300
for line in title_lines:
    draw.text((80, y), line, font=title_font, fill=WHITE)
    y += 68

# Subtitle
draw.text((80, y + 20), "Assessoria e Consultoria Contábil para MEI, CNPJ e Empresas",
          font=subtitle_font, fill=(220, 228, 238))

# Gold pill badge
badge_text = "formalizeeorganize.com.br"
bbox = draw.textbbox((0, 0), badge_text, font=tag_font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
pad_x, pad_y = 24, 14
badge_w = tw + pad_x * 2
badge_h = th + pad_y * 2
badge_x, badge_y = 80, H - 100
draw.rounded_rectangle(
    [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
    radius=badge_h // 2, fill=GOLD_600
)
draw.text((badge_x + pad_x, badge_y + pad_y - 2), badge_text, font=tag_font, fill=NAVY_900)

img.save('og-image.jpg', quality=90)
print('Saved og-image.jpg, size:', img.size)
