# -*- coding: utf-8 -*-
import os
import sys
from PIL import Image, ImageDraw

# This file requires no changes from v1.2.1.
# The resource_path function is still essential for finding the 'locales' folder.

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def round_corners(pil_image, radius):
    """為 PIL Image 物件加上圓角"""
    mask = Image.new('L', pil_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + pil_image.size, radius, fill=255)
    output = pil_image.copy()
    output.putalpha(mask)
    return output
