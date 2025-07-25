# -*- coding: utf-8 -*-
import os
import sys
from PIL import Image, ImageDraw, ImageTk
import base64
import io

# =================================================================================
#  v2.5: Utilities
#  This file contains general-purpose helper functions.
#  Update: Image resources are now embedded as Base64 data, removing the dependency
#  on an external 'assets' folder.
# =================================================================================

# --- Embedded Image Data ---
# The images are converted to Base64 strings, so no external files are needed.
SEARCH_ICON_DATA = """
R0lGODlhFAAUAJECAAAAC/8A/wAAAAAAACH5BAEAAAIALAAAAAAUABQAAAJYjI+py+0Po5y02ouz
3rz7D4biSJbmiabqyrbuC8fyTNf2jef6zvf+DwwKh8Si8YhMKpfMpvMJjUqn1Kr1is1qt9yu9wsO
i8fksvmMTqvX7Lb7DY/L5/S6/Y7P6/f8vv8PGCg4SFhoeIiYqLjI2Oj4CBkpOUlZaXmJmam5yZlA
AAOw==
"""

PLACEHOLDER_ICON_DATA = """
R0lGODlhZABkAIABAAAAAP///yH5BAEKAAEALAAAAABkAGQAAAL+jI+py+0Po5y02ouz3rz7D4bi
SJbmiabqyrbuC8fyTNf2jef6zvf+DwwKh8Si8YhMKpfMpvMJjUqn1Kj1is1qt9yu9wsOi8fksvmM
TqvX7Lb7DY/L5/S6/Y7P6/f8vv8PGCg4SFhoeIiYqLjI2Oj4CBkpOUlZaXmJmam5ydnp+goaKjpK
Wmp6ipqqusra6voKGys7S1tre4ubq7vL2+v8DBwsPExcbHyMnKy8zNzs/AwdLT1NXW19jZ2tvc3d
7f0NHi4+Tl5ufo6err7O3u7+Dh8vP09fb3+Pn6+/z9/v/w8woMCBBAsaPAgwocKFDBs6fAgxosSJ
FCtavIgxY0YDAAA7
"""

def get_image_from_data(base64_data, size):
    """
    Decodes a Base64 encoded string and creates a PhotoImage object.
    """
    try:
        # Decode the Base64 string
        image_data = base64.b64decode(base64_data)
        # Read the image from the binary data
        image = Image.open(io.BytesIO(image_data))
        # Resize and return the PhotoImage
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Failed to load image from data: {e}")
        # If it fails, create a gray fallback image
        img = Image.new('RGB', size, 'grey')
        return ImageTk.PhotoImage(img)

def resource_path(relative_path):
    """
    Gets the absolute path to a resource, works for dev and for PyInstaller.
    (This function is still useful for the languages.json file)
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def round_corners(pil_image, radius):
    """
    Adds rounded corners to a PIL Image object.
    It creates a rounded rectangle mask and applies it to the image's alpha channel.
    """
    mask = Image.new('L', pil_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + pil_image.size, radius, fill=255)
    
    output = pil_image.copy()
    output.putalpha(mask)
    return output
