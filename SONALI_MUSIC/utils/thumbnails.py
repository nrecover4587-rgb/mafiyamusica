
import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def get_thumb(videoid):
    try:
        os.makedirs("cache", exist_ok=True)

        thumb_url = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumb_url) as resp:
                if resp.status != 200:
                    return thumb_url
                content = await resp.read()

        temp_path = f"cache/temp_{videoid}.jpg"

        async with aiofiles.open(temp_path, "wb") as f:
            await f.write(content)

        youtube = Image.open(temp_path).convert("RGB")

        background = changeImageSize(1280, 720, youtube)
        background = background.filter(ImageFilter.GaussianBlur(25))
        background = ImageEnhance.Brightness(background).enhance(0.5)

        main_thumb = youtube.resize((800, 450))

        mask = Image.new("L", main_thumb.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle(
            [(0, 0), main_thumb.size],
            radius=25,
            fill=255
        )
        main_thumb.putalpha(mask)

        background.paste(main_thumb, (240, 120), main_thumb)

        draw = ImageDraw.Draw(background)

        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()

        title = " 𝞄⃕𝖋𝖋 𝑚𝑟 𝑚𝑒𝑛𝑡𝑎�"
        w = draw.textlength(title, font=font)

        draw.text(
            ((1280 - w) / 2, 600),
            title,
            fill="white",
            font=font
        )

        final_path = f"cache/{videoid}.png"
        background.save(final_path)

        try:
            os.remove(temp_path)
        except:
            pass

        return final_path

    except Exception as e:
        print("Thumbnail Error:", e)
        # Fallback to direct YouTube thumb (panel kabhi gayab nahi hoga)
        return f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"


async def get_qthumb(videoid):
    return f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
