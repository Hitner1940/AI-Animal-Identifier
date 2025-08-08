# theme_manager.py
# -*- coding: utf-8 -*-
"""
Manages the application's appearance including themes, fonts, and styles.

This module decouples the view from the raw configuration data, providing
a clean API for accessing theme-aware colors and fonts.
"""
from tkinter import font as tkFont
from config import THEMES, TEXT_SIZE_MAP

class ThemeManager:
    """
    Handles theme colors and font scaling based on user settings.
    It acts as the single source of truth for all styling.
    """
    def __init__(self, theme_mode_var, text_size_var):
        """
        Initializes the ThemeManager.

        Args:
            theme_mode_var (tk.StringVar): Tkinter variable holding the current theme ('light' or 'dark').
            text_size_var (tk.StringVar): Tkinter variable holding the current text size ('Small', 'Medium', 'Large').
        """
        self.theme_mode = theme_mode_var
        self.text_size = text_size_var
        self.fonts = {}
        self.update_fonts()

    def get_current_theme_colors(self):
        """Returns the dictionary of colors for the currently selected theme."""
        return THEMES.get(self.theme_mode.get(), THEMES['light']) # Default to light theme if key is invalid

    def update_fonts(self):
        """
        Re-creates all font objects based on the current text size setting.
        This should be called whenever the text size changes.
        """
        size_profile = TEXT_SIZE_MAP.get(self.text_size.get(), TEXT_SIZE_MAP['Medium'])
        self.fonts = {
            # Create a font object for each type defined in the size profile
            key: tkFont.Font(family="Segoe UI", size=size)
            for key, size in size_profile.items()
        }
        print(f"Fonts updated for text size '{self.text_size.get()}'")

    def get_font(self, name="default"):
        """
        Gets a specific font object by its logical name (e.g., 'title', 'button').
        """
        return self.fonts.get(name, self.fonts['default'])

    def get_button_colors(self, button_type, parent_bg_key=None):
        """
        Generates the complete color configuration for a button, simplifying UI code.

        Args:
            button_type (str): 'primary', 'secondary', or 'icon'.
            parent_bg_key (str, optional): The theme key for the parent widget's
                                           background. Required for 'icon' buttons
                                           to ensure they blend in.

        Returns:
            dict: A dictionary of color properties for the CustomButton widget.
        """
        colors = self.get_current_theme_colors()
        
        if button_type == 'icon':
            # Icon buttons blend with their parent and change color on press
            bg_normal = colors.get(parent_bg_key)
            bg_active = colors.get('tertiarySystemBackground')
            fg = colors['label']
        else:
            # Text buttons have a primary (green) or secondary (red) role
            color_map = {
                'primary': ('systemGreen', 'systemGreen_dark'),
                'secondary': ('systemRed', 'systemRed_dark')
            }
            bg_key, active_bg_key = color_map[button_type]
            bg_normal = colors[bg_key]
            bg_active = colors[active_bg_key]
            fg = colors['buttonText']

        return {
            'bg_normal': bg_normal,
            'bg_active': bg_active,
            'bg_disabled': colors['tertiarySystemBackground'],
            'fg_normal': fg,
            'fg_disabled': colors['secondaryLabel'],
            'border': colors.get('buttonBorder'),
            'shadow': colors.get('buttonShadow')
        }
