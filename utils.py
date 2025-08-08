# utils.py
# -*- coding: utf-8 -*-
"""
General utility functions for the FaunaLens application.
This module provides helper functions for image processing and small embedded icons.
"""
import base64
import io
from PIL import Image, ImageDraw, ImageTk

# --- Embedded icon data (base64). Using empty strings as safe fallbacks ---
# If these are empty or invalid, get_image_from_data will return a blank image.
PLACEHOLDER_ICON_DATA = ""
SEARCH_ICON_LIGHT_THEME_DATA = ""
SEARCH_ICON_DARK_THEME_DATA = ""
SETTINGS_ICON_LIGHT_THEME_DATA = ""
SETTINGS_ICON_DARK_THEME_DATA = ""


def get_image_from_data(base64_data, size):
    """
    Decodes a base64 string into a PhotoImage object.

    Args:
        base64_data (str): The base64 encoded image string.
        size (tuple): The desired (width, height) of the image.

    Returns:
        ImageTk.PhotoImage: The decoded and resized image object.
    """
    try:
        image_data = base64.b64decode(base64_data)
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error decoding image: {e}")
        # Return a blank image on error
        return ImageTk.PhotoImage(Image.new('RGB', size, 'white'))


def round_corners(pil_image, radius):
    """
    Rounds the corners of a PIL Image.

    Args:
        pil_image (PIL.Image): The image to process.
        radius (int): The radius for the corners.

    Returns:
        PIL.Image: The image with rounded corners.
    """
    mask = Image.new('L', pil_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + pil_image.size, radius, fill=255)

    output = pil_image.copy()
    output.putalpha(mask)
    return output
