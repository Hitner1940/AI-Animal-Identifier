# -*- coding: utf-8 -*-
# =================================================================================
#  Configuration
#  This file centrally manages all static settings for the application,
#  such as theme colors, fonts, etc. This keeps the main code cleaner
#  and makes it easier to modify the appearance.
# =================================================================================

# --- Color Themes ---
# Defines the colors for light and dark modes.
THEMES = {
    'light': {
        'systemBackground': "#f0f0f0",
        'secondarySystemBackground': "#ffffff",
        'tertiarySystemBackground': "#e5e5e5",
        'label': "#000000",
        'secondaryLabel': "#8a8a8e",
        'systemBlue': "#007aff",
        'systemGreen': "#34c759",
        'systemRed': "#ff3b30",
        'systemGreen_dark': "#2da44e",
        'systemRed_dark': "#d9342b",
        'buttonText': "#ffffff"
    },
    'dark': {
        'systemBackground': "#000000",
        'secondarySystemBackground': "#1c1c1e",
        'tertiarySystemBackground': "#2c2c2e",
        'label': "#ffffff",
        'secondaryLabel': "#8d8d92",
        'systemBlue': "#0a84ff",
        'systemGreen': "#30d158",
        'systemRed': "#ff453a",
        'systemGreen_dark': "#28a745",
        'systemRed_dark': "#e63946",
        'buttonText': "#ffffff"
    }
}

# --- Font Mapping ---
# Selects the most suitable UI font based on the language.
FONT_MAP = {
    'ja': 'Meiryo UI',
    'ko': 'Malgun Gothic',
    'zh-cn': 'Microsoft YaHei UI',
    'zh-tw': 'Microsoft JhengHei UI',
    'default': 'Segoe UI'  # A good default for English and other languages
}

# --- Supported File Types ---
# Moving the file type definitions here makes them easier to manage.
# The keys like 'images', 'videos', 'all' can be used to get translated strings.
FILE_TYPES_CONFIG = {
    'images': ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.webp'),
    'videos': ('*.mp4', '*.avi', '*.mov', '*.mkv'),
}
