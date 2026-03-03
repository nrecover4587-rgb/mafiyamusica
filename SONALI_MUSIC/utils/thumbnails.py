import os
import math
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance


# -------- Helper: Download or Open Cover --------
def load_cover(cover_source):
    if cover_source.startswith("http"):
        response = requests.get(cover_source, timeout=10)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert("RGBA")
    else:
        return Image.open(cover_source).convert("RGBA")


# -------- Main Thumbnail Function --------
def get_thumb(
    cover_source,
    title="Unknown Title",
    duration="0:00",
    channel="Unknown",
    views="",
    progress=0.4,
):
    """
    cover_source = image url or local path
    progress = float between 0 and 1
    """

    cover = load_cover(cover_source)
    original_cover = cover.copy()

    # -------- Background --------
    bg = original_cover.resize((1280, 720))
    bg = bg.filter(ImageFilter.GaussianBlur(35))
    bg = ImageEnhance.Brightness(bg).enhance(0.35)
    bg = bg.convert("RGBA")

    draw = ImageDraw.Draw(bg)

    # -------- Hexagon Cover --------
    hex_size = 420
    cover_resized = original_cover.resize((hex_size, hex_size))

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
    draw.text(
        (text_x, start_y),
        title[:40],
        fill=(20, 20, 20),
        font=font_title,
    )

    # Info Lines
    info_text = f"YouTube  |  {views}" if views else "YouTube"
    draw.text(
        (text_x, start_y + 90),
        info_text,
        fill=(40, 40, 40),
        font=font_info,
    )

    draw.text(
        (text_x, start_y + 140),
        f"Duration  |  {duration}",
        fill=(50, 50, 50),
        font=font_info,
    )

    draw.text(
        (text_x, start_y + 190),
        f"Player  |  @{channel}",
        fill=(60, 60, 60),
        font=font_info,
    )

    # -------- Progress Bar --------
    bar_x = text_x
    bar_y = start_y + 250
    bar_width = 500
    bar_height = 12

    # Background
    draw.rounded_rectangle(
        [(bar_x, bar_y),
         (bar_x + bar_width, bar_y + bar_height)],
        radius=10,
        fill=(200, 200, 200),
    )

    # Progress Fill
    progress = max(0, min(progress, 1))
    draw.rounded_rectangle(
        [(bar_x, bar_y),
         (bar_x + int(bar_width * progress), bar_y + bar_height)],
        radius=10,
        fill=(0, 0, 0),
    )

    # -------- Save File --------
    output_path = "thumb.png"
    bg.save(output_path)

    return output_path
