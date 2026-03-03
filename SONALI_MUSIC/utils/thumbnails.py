import math
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def get_thumb(cover_url, title, duration, channel):

    # -------- Download Cover --------
    try:
        response = requests.get(cover_url, timeout=10)
        response.raise_for_status()
        cover = Image.open(BytesIO(response.content)).convert("RGBA")
    except:
        cover = Image.new("RGBA", (500, 500), (220, 220, 220))

    # -------- Create White Background --------
    bg = Image.new("RGBA", (1280, 720), (245, 245, 245))
    draw = ImageDraw.Draw(bg)

    # -------- Hexagon Cover --------
    size = 420
    cover = cover.resize((size, size))

    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)

    points = []
    center = size // 2
    radius = size // 2

    for i in range(6):
        angle = math.radians(60 * i - 30)
        x = center + radius * math.cos(angle)
        y = center + radius * math.sin(angle)
        points.append((x, y))

    mask_draw.polygon(points, fill=255)
    cover.putalpha(mask)

    cover_x = 140
    cover_y = (720 - size) // 2

    bg.paste(cover, (cover_x, cover_y), cover)

    # -------- Fonts (Safe) --------
    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 55)
        font_info = ImageFont.truetype("DejaVuSans.ttf", 32)
    except:
        font_title = font_info = ImageFont.load_default()

    # -------- Right Side Text --------
    text_x = cover_x + size + 120
    start_y = 250

    # Title
    draw.text(
        (text_x, start_y),
        title[:40],
        fill=(0, 0, 0),
        font=font_title,
    )

    # Info lines
    draw.text(
        (text_x, start_y + 90),
        "YouTube  |  395M views",
        fill=(60, 60, 60),
        font=font_info,
    )

    draw.text(
        (text_x, start_y + 140),
        f"Duration  |  {duration}",
        fill=(70, 70, 70),
        font=font_info,
    )

    draw.text(
        (text_x, start_y + 190),
        f"Player  |  @{channel}",
        fill=(80, 80, 80),
        font=font_info,
    )

    # -------- Thin Progress Bar --------
    bar_x = text_x
    bar_y = start_y + 260
    bar_width = 480
    bar_height = 8

    # Background line
    draw.rectangle(
        [(bar_x, bar_y),
         (bar_x + bar_width, bar_y + bar_height)],
        fill=(200, 200, 200),
    )

    # Filled part (50%)
    progress_width = int(bar_width * 0.5)

    draw.rectangle(
        [(bar_x, bar_y),
         (bar_x + progress_width, bar_y + bar_height)],
        fill=(0, 0, 0),
    )

    # -------- Save --------
    output_path = "/tmp/thumb.png"
    bg.save(output_path)

    return output_path
