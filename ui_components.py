# ui_components.py
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

class CustomButton(tk.Canvas):
    """A custom, theme-aware, rounded button with a border and shadow."""
    def __init__(self, parent, **kwargs):
        self.command = kwargs.pop('command', None)
        self.text = kwargs.pop('text', '')
        self.font = kwargs.pop('font', ('Segoe UI', 12))
        self.radius = kwargs.pop('radius', 25)
        self.colors = kwargs.pop('colors', {})
        self.parent_bg = kwargs.pop('parent_bg', '#ffffff')
        self._state = kwargs.pop('state', tk.NORMAL)
        self.shadow_offset = 2

        super().__init__(parent, height=kwargs.pop('height', 45),
                         highlightthickness=0, bg=self.parent_bg, **kwargs)

        self.bind("<Configure>", self._on_resize)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

        self._draw()

    def _draw(self, event_state='normal'):
        """Draws the button components."""
        self.delete("all")
        width, height = self.winfo_width(), self.winfo_height()

        if width <= 1 or height <= 1: return

        bg_color, fg_color, border_color, shadow_color = self._get_current_colors(event_state)

        offset_x, offset_y = (0, 0) if event_state == 'active' else (self.shadow_offset, self.shadow_offset)

        if event_state != 'active' and self._state != tk.DISABLED:
            self.create_rounded_rectangle(offset_x, offset_y, width, height,
                                          radius=self.radius, fill=shadow_color, outline="")

        self.create_rounded_rectangle(0, 0, width - offset_x, height - offset_y,
                                      radius=self.radius, fill=bg_color, outline=border_color, width=1.5)

        self.create_text((width - offset_x) / 2, (height - offset_y) / 2, text=self.text, font=self.font,
                         fill=fg_color, anchor="center")

    def _get_current_colors(self, event_state):
        """Determines the correct colors based on the button's state."""
        if self._state == tk.DISABLED:
            return (self.colors.get('bg_disabled'), self.colors.get('fg_disabled'),
                    self.colors.get('border'), self.colors.get('shadow'))
        if event_state == 'active':
            return (self.colors.get('bg_active'), self.colors.get('fg_normal'),
                    self.colors.get('border'), self.colors.get('shadow'))
        return (self.colors.get('bg_normal'), self.colors.get('fg_normal'),
                self.colors.get('border'), self.colors.get('shadow'))

    def _on_resize(self, event): self._draw()
    def _on_press(self, event):
        if self._state == tk.NORMAL: self._draw('active')
    def _on_release(self, event):
        if self._state == tk.NORMAL:
            self._draw('normal')
            if 0 < event.x < self.winfo_width() and 0 < event.y < self.winfo_height() and self.command:
                self.command()

    def configure(self, **kwargs):
        if 'state' in kwargs:
            self._state = kwargs.pop('state')
            self._draw()
        super().configure(**kwargs)

class IconCustomButton(tk.Canvas):
    """A rounded button that displays an icon image centered, theme-aware."""
    def __init__(self, parent, **kwargs):
        self.command = kwargs.pop('command', None)
        self.image = kwargs.pop('image', None)  # expects a PhotoImage
        self.radius = kwargs.pop('radius', 18)
        self.colors = kwargs.pop('colors', {})
        self.parent_bg = kwargs.pop('parent_bg', '#ffffff')
        self._state = kwargs.pop('state', tk.NORMAL)
        self.shadow_offset = 2

        super().__init__(parent, width=36, height=36, highlightthickness=0, bg=self.parent_bg, **kwargs)

        self.bind("<Configure>", self._on_resize)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

        self._draw()

    def _draw(self, event_state='normal'):
        self.delete("all")
        width, height = self.winfo_width(), self.winfo_height()
        if width <= 1 or height <= 1: return

        bg_color, fg_color, border_color, shadow_color = self._get_current_colors(event_state)
        offset_x, offset_y = (0, 0) if event_state == 'active' else (self.shadow_offset, self.shadow_offset)

        if event_state != 'active' and self._state != tk.DISABLED:
            self.create_rounded_rectangle(offset_x, offset_y, width, height,
                                          radius=self.radius, fill=shadow_color, outline="")

        self.create_rounded_rectangle(0, 0, width - offset_x, height - offset_y,
                                      radius=self.radius, fill=bg_color, outline=border_color, width=1.5)

        if self.image is not None:
            # Keep a reference to avoid garbage collection
            self._img_ref = self.image
            self.create_image((width - offset_x) / 2, (height - offset_y) / 2, image=self._img_ref)

    def _get_current_colors(self, event_state):
        if self._state == tk.DISABLED:
            return (self.colors.get('bg_disabled'), self.colors.get('fg_disabled'),
                    self.colors.get('border'), self.colors.get('shadow'))
        if event_state == 'active':
            return (self.colors.get('bg_active'), self.colors.get('fg_normal'),
                    self.colors.get('border'), self.colors.get('shadow'))
        return (self.colors.get('bg_normal'), self.colors.get('fg_normal'),
                self.colors.get('border'), self.colors.get('shadow'))

    def _on_resize(self, event): self._draw()
    def _on_press(self, event):
        if self._state == tk.NORMAL: self._draw('active')
    def _on_release(self, event):
        if self._state == tk.NORMAL:
            self._draw('normal')
            if 0 < event.x < self.winfo_width() and 0 < event.y < self.winfo_height() and self.command:
                self.command()

class ResultRow(tk.Frame):
    """A row that displays a single prediction result."""
    def __init__(self, parent, colors, font, result_data, search_callback):
        super().__init__(parent, bg=colors['secondarySystemBackground'])
        self.colors = colors
        self.font = font
        label_name, score = result_data

        self.grid_columnconfigure(1, weight=1)

        self.name_label = tk.Label(self, text=label_name, font=self.font, anchor='w', bg=self.colors['secondarySystemBackground'], fg=self.colors['label'])
        self.name_label.grid(row=0, column=0, sticky='w', padx=(15, 5), pady=8)

        s = ttk.Style()
        s.configure('Result.Horizontal.TProgressbar', troughcolor=colors['tertiarySystemBackground'], background=colors['systemBlue'], thickness=8, bordercolor=colors['tertiarySystemBackground'])

        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=100, mode='determinate', value=score * 100, style='Result.Horizontal.TProgressbar')
        self.progress_bar.grid(row=0, column=1, sticky='we', padx=5, pady=8)

        self.score_label = tk.Label(self, text=f"{score:.1%}", font=self.font, anchor='e', bg=self.colors['secondarySystemBackground'], fg=self.colors['secondaryLabel'])
        self.score_label.grid(row=0, column=2, sticky='e', padx=(5, 15), pady=8)

        self.bind_all_children("<Button-1>", lambda e, l=label_name: search_callback(l))
        self.bind_all_children("<Enter>", self.on_enter)
        self.bind_all_children("<Leave>", self.on_leave)

    def bind_all_children(self, event, callback):
        self.bind(event, callback)
        for child in self.winfo_children():
            child.bind(event, callback)

    def on_enter(self, event):
        self.config(bg=self.colors['tertiarySystemBackground'])
        for child in self.winfo_children():
            if not isinstance(child, ttk.Progressbar):
                child.config(bg=self.colors['tertiarySystemBackground'])

    def on_leave(self, event):
        self.config(bg=self.colors['secondarySystemBackground'])
        for child in self.winfo_children():
            if not isinstance(child, ttk.Progressbar):
                child.config(bg=self.colors['secondarySystemBackground'])

def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    """Helper function to draw a rounded rectangle on a Canvas."""
    points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
    return self.create_polygon(points, **kwargs, smooth=True)

tk.Canvas.create_rounded_rectangle = create_rounded_rectangle
