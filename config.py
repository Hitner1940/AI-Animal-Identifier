# config.py
# -*- coding: utf-8 -*-
"""
Central configuration file for the FaunaLens application.

This file holds all static configuration data, making it easy to update the
application's appearance and behavior without changing the core logic.
It centralizes theme colors, font sizes, and window dimensions.
"""

# --- Font and Sizing Configuration ---
# Defines different text size profiles for UI scalability.
# Each key ('Small', 'Medium', 'Large') corresponds to a user setting.
TEXT_SIZE_MAP = {
    "Small": {
        "default": 9,
        "button": 10,
        "result_row": 10,
        "result_title": 13,
        "title": 22
    },
    "Medium": {
        "default": 10,
        "button": 11,
        "result_row": 11,
        "result_title": 15,
        "title": 26
    },
    "Large": {
        "default": 12,
        "button": 13,
        "result_row": 13,
        "result_title": 18,
        "title": 30
    },
}

# Defines different window size profiles for user preference.
WINDOW_SIZE_MAP = {
    "Compact": "600x700",
    "Standard": "700x800",
    "Large": "850x900",
}

# --- Theme Colors ---
# A centralized dictionary for all color definitions. This allows for easy
# theme creation and modification. We have 'light' and 'dark' modes defined.
THEMES = {
    "light": {
        "systemBackground": "#f0f0f0",
        "secondarySystemBackground": "#ffffff",
        "tertiarySystemBackground": "#e5e5e5",
        "label": "#000000",
        "secondaryLabel": "#6c6c6c",
        "systemGreen": "#34c759",
        "systemGreen_dark": "#2aa148",
        "systemRed": "#ff3b30",
        "systemRed_dark": "#d9332a",
        "systemBlue": "#007aff",
        "buttonText": "#ffffff",
        "buttonBorder": "#d0d0d0",
        "buttonShadow": "#b0b0b0",
    },
    "dark": {
        "systemBackground": "#1c1c1e",
        "secondarySystemBackground": "#2c2c2e",
        "tertiarySystemBackground": "#3a3a3c",
        "label": "#ffffff",
        "secondaryLabel": "#8e8e93",
        "systemGreen": "#30d158",
        "systemGreen_dark": "#28b049",
        "systemRed": "#ff453a",
        "systemRed_dark": "#d93c32",
        "systemBlue": "#0a84ff",
        "buttonText": "#ffffff",
        "buttonBorder": "#4a4a4c",
        "buttonShadow": "#101010",
    }
}
