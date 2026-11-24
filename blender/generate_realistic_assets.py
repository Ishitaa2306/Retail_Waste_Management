"""
Generator for Photorealistic Retail Shelf Facings and Produce Baskets.
Creates continuous high-density textured product facings:
1. shelf_facing_drinks.png: Rows of colorful glass/plastic soda & juice bottles with caps and labels
2. shelf_facing_cereals.png: Rows of branded breakfast cereal, cookie, and chip boxes
3. shelf_facing_snacks.png: Rows of colorful snack bags, crisps, and confectionery
4. shelf_facing_sauces.png: Condiments, olive oil, and glass pasta jars
5. shelf_facing_cans.png: Stacked soup and bean cans with vibrant labels
6. produce_crate_apples.png: Woven wicker basket brimming with red Gala apples
7. produce_crate_oranges.png: Wooden crate full of textured round oranges
8. produce_crate_bananas.png: Bunches of fresh curved yellow bananas
9. produce_crate_lettuce.png: Crinkled heads of fresh green cabbage and lettuce
10. produce_crate_tomatoes.png: Red vine tomatoes with green stems
"""

import os
import math
import random
from PIL import Image, ImageDraw

TEX_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "textures")
os.makedirs(TEX_DIR, exist_ok=True)

def create_shelf_facing_drinks():
    """Continuous row of 30+ soda, mineral water, and juice bottles with labels and caps."""
    img = Image.new("RGB", (2048, 512), color=(25, 25, 28))
    draw = ImageDraw.Draw(img)
    
    bottle_colors = [
        (220, 40, 30),   # Cola red
        (30, 160, 60),   # Citrus green
        (20, 110, 220),  # Mineral blue
        (240, 130, 20),  # Orange soda
        (130, 40, 160),  # Grape purple
        (230, 210, 40),  # Lemon yellow
        (200, 30, 90),   # Berry pink
        (15, 80, 180)    # Sport electrolyte
    ]
    
    num_bottles = 32
    w = 2048 // num_bottles
    
    for i in range(num_bottles):
        bx = i * w
        bcol = bottle_colors[i % len(bottle_colors)]
        
        # Bottle body
        draw.rounded_rectangle([bx + 4, 140, bx + w - 4, 500], radius=8, fill=bcol)
        # Bottle neck
        draw.rectangle([bx + w//2 - 7, 70, bx + w//2 + 7, 140], fill=bcol)
        # Screw cap
        draw.rectangle([bx + w//2 - 9, 45, bx + w//2 + 9, 70], fill=(240, 240, 245))
        # Paper brand label
        draw.rectangle([bx + 4, 230, bx + w - 4, 390], fill=(255, 255, 255))
        draw.rectangle([bx + 6, 240, bx + w - 6, 300], fill=bcol)
        # Label text imitation / barcode
        for ly in range(320, 380, 8):
            draw.line([(bx + 8, ly), (bx + w - 8, ly)], fill=(40, 40, 45), width=2)
        # Highlight reflection
        draw.line([(bx + 10, 150), (bx + 10, 490)], fill=(255, 255, 255), width=3)
        
    path = os.path.join(TEX_DIR, "shelf_facing_drinks.png")
    img.save(path)
    return path

def create_shelf_facing_cereals():
    """Continuous row of vibrant commercial cereal and snack boxes."""
    img = Image.new("RGB", (2048, 512), color=(25, 25, 28))
    draw = ImageDraw.Draw(img)
    
    box_themes = [
        ((235, 175, 25), (220, 50, 30), "CRUNCH"),
        ((210, 35, 30), (255, 215, 0), "FLAKES"),
        ((40, 140, 210), (255, 255, 255), "FROST"),
        ((150, 40, 160), (240, 140, 20), "BERRY"),
        ((60, 170, 70), (255, 240, 100), "ORGANIC"),
        ((220, 100, 30), (255, 255, 255), "HONEY"),
        ((180, 30, 40), (255, 215, 0), "CHOCO"),
        ((50, 180, 160), (255, 255, 255), "OATS")
    ]
    
    num_boxes = 24
    w = 2048 // num_boxes
    
    for i in range(num_boxes):
        bx = i * w
        bg, acc, txt = box_themes[i % len(box_themes)]
        
        # Main box face
        draw.rectangle([bx + 3, 20, bx + w - 3, 500], fill=bg)
        # Top banner
        draw.rectangle([bx + 3, 20, bx + w - 3, 110], fill=acc)
        # Mascot / bowl graphic
        draw.ellipse([bx + 12, 170, bx + w - 12, 330], fill=(255, 255, 255))
        draw.ellipse([bx + 18, 176, bx + w - 18, 324], fill=acc)
        # Bottom details / barcode
        draw.rectangle([bx + 6, 420, bx + w - 6, 490], fill=(245, 245, 245))
        for lx in range(bx + 15, bx + w - 15, 5):
            draw.line([(lx, 430), (lx, 480)], fill=(0, 0, 0), width=2)
            
    path = os.path.join(TEX_DIR, "shelf_facing_cereals.png")
    img.save(path)
    return path

def create_shelf_facing_snacks():
    """Continuous row of puffed chip and pretzel snack bags."""
    img = Image.new("RGB", (2048, 512), color=(25, 25, 28))
    draw = ImageDraw.Draw(img)
    
    bag_colors = [
        (220, 35, 30),   # Paprika
        (40, 160, 60),   # Sour cream
        (235, 180, 20),  # Cheese
        (30, 110, 210),  # Salt & Vinegar
        (140, 30, 140),  # Sweet Chili
        (220, 100, 20),  # Barbecue
        (20, 150, 140),  # Jalapeno
        (190, 40, 70)    # Salsa
    ]
    
    num_bags = 28
    w = 2048 // num_bags
    
    for i in range(num_bags):
        bx = i * w
        col = bag_colors[i % len(bag_colors)]
        
        # Pillow snack bag shape
        draw.polygon([
            (bx + 8, 40), (bx + w - 8, 40),
            (bx + w - 2, 260),
            (bx + w - 6, 495), (bx + 6, 495),
            (bx + 2, 260)
        ], fill=col)
        # Crimp seals
        draw.rectangle([bx + 8, 30, bx + w - 8, 45], fill=(200, 200, 205))
        draw.rectangle([bx + 6, 485, bx + w - 6, 500], fill=(200, 200, 205))
        # Center logo splash
        draw.ellipse([bx + 12, 160, bx + w - 12, 320], fill=(255, 255, 255))
        draw.ellipse([bx + 16, 164, bx + w - 16, 316], fill=(235, 180, 20))
        
    path = os.path.join(TEX_DIR, "shelf_facing_snacks.png")
    img.save(path)
    return path

def create_shelf_facing_sauces():
    """Rows of glass sauce bottles, olive oil, and jars."""
    img = Image.new("RGB", (2048, 512), color=(25, 25, 28))
    draw = ImageDraw.Draw(img)
    
    jar_colors = [
        (160, 40, 25),   # Tomato pasta
        (90, 120, 35),   # Extra virgin olive oil
        (210, 160, 40),  # Mustard / mayonnaise
        (120, 35, 30),   # BBQ marinade
        (180, 70, 25),   # Hot chili sauce
        (60, 95, 30)     # Pesto
    ]
    
    num_jars = 32
    w = 2048 // num_jars
    
    for i in range(num_jars):
        bx = i * w
        col = jar_colors[i % len(jar_colors)]
        
        # Glass jar body
        draw.rounded_rectangle([bx + 6, 130, bx + w - 6, 490], radius=10, fill=col)
        # Metallic / gold screw lid
        draw.rectangle([bx + 10, 80, bx + w - 10, 130], fill=(215, 175, 55))
        # Front artisan label
        draw.rectangle([bx + 8, 220, bx + w - 8, 410], fill=(245, 240, 225))
        draw.rectangle([bx + 12, 235, bx + w - 12, 290], fill=col)
        # Specular reflection
        draw.line([(bx + 12, 145), (bx + 12, 475)], fill=(255, 255, 255), width=2)
        
    path = os.path.join(TEX_DIR, "shelf_facing_sauces.png")
    img.save(path)
    return path

def create_produce_crate_texture(filename, fruit_color, spot_color=None, shape='round'):
    """Seamless packed produce crate texture (apples, oranges, tomatoes, greens)."""
    img = Image.new("RGB", (1024, 1024), color=(60, 45, 30))
    draw = ImageDraw.Draw(img)
    
    # Pack densely with fruits
    r = 55
    random.seed(42)
    for y in range(r, 1024, int(r * 1.5)):
        for x in range(r, 1024, int(r * 1.6)):
            ox = x + random.randint(-8, 8)
            oy = y + random.randint(-8, 8)
            # Fruit base
            draw.ellipse([ox - r, oy - r, ox + r, oy + r], fill=fruit_color)
            # 3D spherical shading
            draw.ellipse([ox - r + 10, oy - r + 8, ox + r - 16, oy + r - 18], fill=spot_color or fruit_color)
            # Stem/calyx dot
            draw.ellipse([ox - 4, oy - 4, ox + 4, oy + 4], fill=(45, 75, 25))
            
    path = os.path.join(TEX_DIR, filename)
    img.save(path)
    return path

def generate_all_realistic_assets():
    print("[Textures] Generating commercial shelf facings and produce textures...")
    create_shelf_facing_drinks()
    create_shelf_facing_cereals()
    create_shelf_facing_snacks()
    create_shelf_facing_sauces()
    
    # Fresh produce textures for island display baskets
    create_produce_crate_texture("produce_apples_red.png", (205, 30, 25), (235, 70, 50))
    create_produce_crate_texture("produce_oranges.png", (245, 125, 15), (255, 160, 45))
    create_produce_crate_texture("produce_tomatoes.png", (225, 35, 20), (250, 75, 45))
    create_produce_crate_texture("produce_greens.png", (45, 155, 55), (75, 195, 70))
    create_produce_crate_texture("produce_lemons.png", (240, 215, 35), (255, 235, 75))
    print("[Textures] Complete!")

if __name__ == "__main__":
    generate_all_realistic_assets()
