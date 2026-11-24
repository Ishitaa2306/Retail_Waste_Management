"""
Texture Generator for Photorealistic Supermarket.
Generates genuine retail product label textures, wooden crate textures, floor tile textures,
cereal box art, soda can graphics, produce crate patterns, snack bag patterns, and packaging artwork.
"""

import os
from PIL import Image, ImageDraw, ImageFont

TEX_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "textures")
os.makedirs(TEX_DIR, exist_ok=True)

def generate_floor_tile():
    """Generates grey matte architectural porcelain tile texture matching reference image."""
    img = Image.new("RGB", (1024, 1024), color=(140, 138, 134))
    draw = ImageDraw.Draw(img)
    import random
    random.seed(42)
    # Subtle stone noise
    pixels = img.load()
    for y in range(1024):
        for x in range(1024):
            n = random.randint(-12, 12)
            r = min(255, max(0, 140 + n))
            g = min(255, max(0, 138 + n))
            b = min(255, max(0, 134 + n))
            pixels[x, y] = (r, g, b)
    # Subtle grout grid lines (4 tiles in 1024)
    grout_color = (95, 93, 90)
    for i in [0, 512, 1023]:
        draw.line([(0, i), (1024, i)], fill=grout_color, width=3)
        draw.line([(i, 0), (i, 1024)], fill=grout_color, width=3)
    path = os.path.join(TEX_DIR, "floor_porcelain_tile.png")
    img.save(path)
    return path

def generate_wood_texture():
    """Warm oak wood texture for produce display tables, headers and endcaps."""
    img = Image.new("RGB", (512, 512), color=(175, 130, 85))
    draw = ImageDraw.Draw(img)
    import random
    random.seed(42)
    # Wood grain streaks
    for y in range(512):
        shade = 175 + int(20 * math.sin(y * 0.08)) + random.randint(-8, 8)
        r = min(255, max(0, shade))
        g = min(255, max(0, int(shade * 0.75)))
        b = min(255, max(0, int(shade * 0.5)))
        draw.line([(0, y), (512, y)], fill=(r, g, b))
    path = os.path.join(TEX_DIR, "warm_oak_wood.png")
    img.save(path)
    return path

import math

def generate_package_texture(name, base_color, text_title, subtitle, accent_color=(255, 255, 255)):
    """Generates vibrant commercial supermarket shelf package textures."""
    img = Image.new("RGB", (512, 512), color=base_color)
    draw = ImageDraw.Draw(img)
    
    # Top banner stripe
    draw.rectangle([0, 0, 512, 90], fill=accent_color)
    # Bottom details band
    draw.rectangle([0, 430, 512, 512], fill=(30, 30, 35))
    
    # Center badge
    draw.ellipse([80, 130, 432, 380], fill=(255, 255, 255))
    draw.ellipse([95, 145, 417, 365], fill=base_color)
    
    # Text
    draw.text((30, 30), text_title[:16].upper(), fill=(20, 20, 25))
    draw.text((120, 230), text_title[:14], fill=(255, 255, 255))
    draw.text((150, 280), subtitle[:18], fill=accent_color)
    draw.text((30, 460), "100% ORGANIC & FRESH", fill=(240, 240, 240))
    
    # Nutritional / barcode box
    draw.rectangle([360, 440, 490, 500], fill=(255, 255, 255))
    for x in range(370, 480, 6):
        draw.line([(x, 445), (x, 495)], fill=(0, 0, 0), width=2)
        
    path = os.path.join(TEX_DIR, f"{name}.png")
    img.save(path)
    return path

def generate_all_textures():
    print("[Textures] Generating high-resolution retail textures...")
    generate_floor_tile()
    generate_wood_texture()
    
    # Package labels matching the vibrant reference image
    generate_package_texture("tex_cereal_yellow", (230, 170, 20), "CRUNCH OATS", "Morning Vitality", (240, 80, 40))
    generate_package_texture("tex_snack_red", (210, 35, 30), "PAPRIKA CHIPS", "Crispy Roasted", (255, 215, 0))
    generate_package_texture("tex_snack_green", (40, 160, 60), "SOUR CREAM", "Herb & Chive", (255, 255, 255))
    generate_package_texture("tex_beverage_blue", (25, 90, 200), "MINERAL WATER", "Pure Mountain", (255, 255, 255))
    generate_package_texture("tex_beverage_orange", (240, 120, 20), "CITRUS BURST", "100% Real Juice", (255, 240, 100))
    generate_package_texture("tex_pasta_gold", (220, 150, 40), "PENNE RIGATE", "Artisan Durum", (180, 30, 30))
    generate_package_texture("tex_cleaner_purple", (120, 40, 160), "LAVENDER PRO", "Disinfectant Clean", (255, 255, 255))
    generate_package_texture("tex_produce_sign", (30, 110, 45), "FRESH PRODUCE", "Farm to Shelf Daily", (255, 220, 50))
    generate_package_texture("tex_price_tags", (235, 235, 235), "$3.49 / EA", "Special Offer", (200, 30, 30))
    print("[Textures] Done!")

if __name__ == "__main__":
    generate_all_textures()
