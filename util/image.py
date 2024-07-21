import base64
import os
from io import BytesIO
from PIL import Image
import zlib

from PIL import ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont
from StreamDeck.ImageHelpers import PILHelper
from pathlib import Path

# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(Path(__file__).parents[1], "resources")


def load_image_to_base64(icon_filename):
    icon_path = os.path.join(ASSETS_PATH, icon_filename)
    with open(icon_path, "rb") as image_file:
        data = zlib.compress(base64.b64encode(image_file.read()))
    return data


def load_default_font_to_base64(ttf):
    font = os.path.join(ASSETS_PATH, ttf)
    with open(font, "rb") as font_file:
        data = zlib.compress(base64.b64encode(font_file.read()))
    return data


def get_image_from_base64(encoded) -> Image:
    return Image.open(BytesIO(base64.b64decode(zlib.decompress(encoded))))


def get_font_from_base64(encoded) -> FreeTypeFont:
    return ImageFont.truetype(BytesIO(base64.b64decode(zlib.decompress(encoded))), 14)


def get_empty_image(deck) -> Image:
    return Image.new("RGB", deck.key_image_format()['size'], 'black')


def render_key_image(deck, key, pressed):
    compressed_image = key.image_label.pressed_image if pressed else key.image_label.image
    if compressed_image is None:
        image = get_empty_image(deck)
    else:
        icon = get_image_from_base64(compressed_image)
        margins = [5, 5, 25, 5] if pressed else [0, 0, 20, 0]
        image = PILHelper.create_scaled_key_image(deck, icon, margins=margins)

    compressed_font = key.image_label.font.font
    if compressed_font is None:
        return PILHelper.to_native_key_format(deck, image)

    font = get_font_from_base64(compressed_font)

    draw = ImageDraw.Draw(image)

    label = key.image_label.pressed_label if pressed else key.image_label.label
    if label is None:
        return PILHelper.to_native_key_format(deck, image)

    render_label(draw, font, image, label, pressed)

    return PILHelper.to_native_key_format(deck, image)


def render_label(draw, font, image, label, pressed):
    # nice to have: add DB level font fill and stroke fill (both can be rgb hex to int values)
    height_offset = 5 if not pressed else 10
    draw.text((image.width / 2, image.height - height_offset),
              text=label,
              font=font,
              anchor="ms",
              fill="white",
              stroke_width=2,
              stroke_fill='black')
