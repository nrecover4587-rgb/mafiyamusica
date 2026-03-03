# -------- Background --------
bg = cover.resize((1280, 720))
bg = bg.filter(ImageFilter.GaussianBlur(35))
bg = ImageEnhance.Brightness(bg).enhance(0.35)

# Dark blue overlay
overlay = Image.new("RGBA", (1280, 720), (8, 25, 40, 220))
bg = Image.alpha_composite(bg.convert("RGBA"), overlay)

draw = ImageDraw.Draw(bg)

# -------- Left Cover --------
cover_size = 420
cover = cover.resize((cover_size, cover_size))

mask = Image.new("L", (cover_size, cover_size), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.rounded_rectangle(
    [(0, 0), (cover_size, cover_size)], radius=40, fill=255
)
cover.putalpha(mask)

cover_x = 120
cover_y = (720 - cover_size) // 2
bg.paste(cover, (cover_x, cover_y), cover)

# -------- Fonts --------
try:
    font_playing = ImageFont.truetype("arial.ttf", 45)
    font_title = ImageFont.truetype("arialbd.ttf", 95)
    font_artist = ImageFont.truetype("arialbd.ttf", 60)
    font_duration = ImageFont.truetype("arial.ttf", 50)
    font_watermark = ImageFont.truetype("arial.ttf", 38)
except:
    font_playing = font_title = font_artist = font_duration = font_watermark = ImageFont.load_default()

# -------- Text --------
text_x = cover_x + cover_size + 100
start_y = 230

title = truncate(title, 28)
channel = truncate(channel, 25)

# Playing
draw.text((text_x, start_y - 90),
          "Playing",
          fill=(180, 190, 200),
          font=font_playing)

# Title
draw.text((text_x, start_y),
          title,
          fill=(255, 255, 255),
          font=font_title)

# Artist
draw.text((text_x, start_y + 120),
          channel,
          fill=(200, 210, 220),
          font=font_artist)

# Duration
draw.text((text_x, start_y + 210),
          f"Duration: {duration}",
          fill=(170, 180, 190),
          font=font_duration)

# -------- Watermark --------
watermark_text = "Powered by 𝞄⃕𝖋𝖋 𝑚𝑟 𝑚𝑒𝑛𝑡𝑎𝑙"
text_width = draw.textlength(watermark_text, font=font_watermark)

wm_x = 1280 - text_width - 60
wm_y = 650

draw.text((wm_x, wm_y),
          watermark_text,
          fill=(160, 170, 180),
          font=font_watermark)
