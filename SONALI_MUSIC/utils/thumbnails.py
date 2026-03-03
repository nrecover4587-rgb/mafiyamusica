from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math

# -------- Background --------
original_cover = cover.copy()

bg = original_cover.resize((1280, 720))
bg = bg.filter(ImageFilter.GaussianBlur(35))
bg = ImageEnhance.Brightness(bg).enhance(0.35)
bg = bg.convert("RGBA")

draw = ImageDraw.Draw(bg)

# -------- Hexagon Cover --------
hex_size = 420
cover_resized = original_cover.resize((hex_size, hex_size))

# Create hexagon mask
mask = Image.new("L", (hex_size, hex_size), 0)
mask_draw = ImageDraw.Draw(mask)

points = []
center = hex_size // 2
radius = hex_size // 2

for i in range(6):
    angle = math.radians(60 * i - 30)
    x = center + radius * math.cos(angle)
    y = center + radius * math.sin(angle)
    points.append((x, y))

mask_draw.polygon(points, fill=255)
cover_resized.putalpha(mask)

cover_x = 140
cover_y = (720 - hex_size) // 2

bg.paste(cover_resized, (cover_x, cover_y), cover_resized)

# -------- Fonts --------
try:
    font_title = ImageFont.truetype("arialbd.ttf", 60)
    font_info = ImageFont.truetype("arial.ttf", 35)
except:
    font_title = font_info = ImageFont.load_default()

# -------- Right Side Info --------
text_x = cover_x + hex_size + 120
start_y = 260

# Title
draw.text((text_x, start_y),
          title,
          fill=(20, 20, 20),
          font=font_title)

# Info Lines
draw.text((text_x, start_y + 90),
          "YouTube  |  395M views",
          fill=(40, 40, 40),
          font=font_info)

draw.text((text_x, start_y + 140),
          f"Duration  |  {duration}",
          fill=(50, 50, 50),
          font=font_info)

draw.text((text_x, start_y + 190),
          f"Player  |  @{channel}",
          fill=(60, 60, 60),
          font=font_info)

# -------- Progress Bar --------
bar_x = text_x
bar_y = start_y + 250
bar_width = 500
bar_height = 12

# Background bar
draw.rounded_rectangle(
    [(bar_x, bar_y),
     (bar_x + bar_width, bar_y + bar_height)],
    radius=10,
    fill=(200, 200, 200)
)

# Progress (example 50%)
progress = 0.5

draw.rounded_rectangle(
    [(bar_x, bar_y),
     (bar_x + int(bar_width * progress), bar_y + bar_height)],
    radius=10,
    fill=(0, 0, 0)
)

bg.save("hex_music_card.png")
