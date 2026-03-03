import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython import VideosSearch

from config import YOUTUBE_IMG_URL

os.makedirs("cache", exist_ok=True)


def truncate(text, length):
    return text[:length] + "..." if len(text) > length else text


async def get_thumb(videoid):
    try:
        if os.path.isfile(f"cache/{videoid}.png"):
            return f"cache/{videoid}.png"

        url = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(url, limit=1)

        for result in (await results.next())["result"]:
            title = result.get("title", "Unknown Title")
            duration = result.get("duration", "Unknown")
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            channel = result.get("channel", {}).get("name", "Unknown Artist")

        # Download thumbnail
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(f"cache/thumb{videoid}.png", "wb") as f:
                        await f.write(await resp.read())

        cover = Image.open(f"cache/thumb{videoid}.png").convert("RGBA")

        # -------- Background --------
        bg = cover.resize((1280, 720))
        bg = bg.filter(ImageFilter.GaussianBlur(40))
        bg = ImageEnhance.Brightness(bg).enhance(0.3)

        overlay = Image.new("RGBA", (1280, 720), (10, 20, 30, 200))
        bg = Image.alpha_composite(bg.convert("RGBA"), overlay)

        # -------- Left Cover --------
        cover_size = 420
        cover = cover.resize((cover_size, cover_size))

        mask = Image.new("L", (cover_size, cover_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle(
            [(0, 0), (cover_size, cover_size)], radius=35, fill=255
        )
        cover.putalpha(mask)

        cover_x = 120
        cover_y = (720 - cover_size) // 2
        bg.paste(cover, (cover_x, cover_y), cover)

        draw = ImageDraw.Draw(bg)

        # -------- Fonts --------
        try:
            font_small = ImageFont.truetype("arial.ttf", 40)
            font_title = ImageFont.truetype("arialbd.ttf", 75)
            font_artist = ImageFont.truetype("arial.ttf", 55)
            font_duration = ImageFont.truetype("arial.ttf", 45)
            font_watermark = ImageFont.truetype("arialbd.ttf", 40)
        except:
            font_small = font_title = font_artist = font_duration = font_watermark = ImageFont.load_default()

        # -------- Text Position --------
        text_x = cover_x + cover_size + 80
        start_y = 250

        title = truncate(title, 35)
        channel = truncate(channel, 30)

        # Playing
        draw.text((text_x, start_y - 90), "Playing", fill=(200, 200, 200), font=font_small)

        # Title
        draw.text((text_x, start_y), title, fill="white", font=font_title)

        # Artist
        draw.text((text_x, start_y + 110), channel, fill=(220, 220, 220), font=font_artist)

        # Duration
        draw.text((text_x, start_y + 190), f"Duration: {duration}", fill=(180, 180, 180), font=font_duration)

        # -------- Watermark (Glow Effect) --------
        watermark_text = "Powered by Perfect Music"
        text_width = draw.textlength(watermark_text, font=font_watermark)

        wm_x = 1280 - text_width - 40
        wm_y = 660

        # Glow shadow
        draw.text((wm_x - 2, wm_y - 2), watermark_text, fill=(0, 0, 0), font=font_watermark)

        # Main text
        draw.text((wm_x, wm_y), watermark_text, fill=(255, 255, 255), font=font_watermark)

        file_name = f"cache/{videoid}.png"
        bg.convert("RGB").save(file_name)

        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass

        return file_name

    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL


async def gen_thumb(videoid):
    return await get_thumb(videoid)
