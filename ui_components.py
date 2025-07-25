# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

# =================================================================================
#  v2.4: UI Components
#  This file contains all custom, reusable Tkinter components.
#  Separating them allows view.py to focus more on the overall layout.
# =================================================================================

class ResultRow(tk.Frame):
    """A row that displays a single prediction result, including name, progress bar, and score."""
    def __init__(self, parent, theme, font, result_data, search_callback):
        super().__init__(parent, bg=theme['secondarySystemBackground'])
        self.theme = theme
        self.font = font
        label_name, score = result_data
        
        self.grid_columnconfigure(1, weight=1)
        
        self.name_label = tk.Label(self, text=label_name, font=self.font, anchor='w', bg=self.theme['secondarySystemBackground'], fg=self.theme['label'])
        self.name_label.grid(row=0, column=0, sticky='w', padx=(15, 5), pady=8)
        
        # Configure progress bar style
        s = ttk.Style()
        s.configure('Result.Horizontal.TProgressbar', 
                    troughcolor=theme['tertiarySystemBackground'], 
                    background=theme['systemBlue'], 
                    thickness=8, 
                    bordercolor=theme['tertiarySystemBackground'])
                    
        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=100, mode='determinate', value=score * 100, style='Result.Horizontal.TProgressbar')
        self.progress_bar.grid(row=0, column=1, sticky='we', padx=5, pady=8)
        
        self.score_label = tk.Label(self, text=f"{score:.1%}", font=self.font, anchor='e', bg=self.theme['secondarySystemBackground'], fg=self.theme['secondaryLabel'])
        self.score_label.grid(row=0, column=2, sticky='e', padx=(5, 15), pady=8)
        
        # Bind events
        self.bind_all_children("<Button-1>", lambda e, l=label_name: search_callback(l))
        self.bind_all_children("<Enter>", self.on_enter)
        self.bind_all_children("<Leave>", self.on_leave)

    def bind_all_children(self, event, callback):
        """Binds an event to itself and all its child components."""
        self.bind(event, callback)
        for child in self.winfo_children():
            child.bind(event, callback)

    def on_enter(self, event):
        """Hover effect when the mouse enters."""
        self.config(bg=self.theme['tertiarySystemBackground'])
        for child in self.winfo_children():
            if not isinstance(child, ttk.Progressbar):
                child.config(bg=self.theme['tertiarySystemBackground'])

    def on_leave(self, event):
        """Restores the original appearance when the mouse leaves."""
        self.config(bg=self.theme['secondarySystemBackground'])
        for child in self.winfo_children():
            if not isinstance(child, ttk.Progressbar):
                child.config(bg=self.theme['secondarySystemBackground'])

class RoundedButton(tk.Canvas):
    """A rounded button drawn using a Canvas."""
    def __init__(self, parent, text, command, theme, font, type='primary'):
        self.theme = theme
        self.command = command
        self.text = text
        self.font = font
        self.type = type
        self.is_enabled = True
        self.update_colors()
        
        super().__init__(parent, height=50, highlightthickness=0, bg=theme['secondarySystemBackground'])
        
        self.tag_id = self.create_rounded_rectangle(0, 0, self.winfo_width(), 50, radius=25, fill=self.bg_color)
        self.text_id = self.create_text(0, 0, text=self.text, font=self.font, fill=self.theme['buttonText'])
        
        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def update_colors(self):
        """Updates colors based on the button type (primary/secondary)."""
        if self.type == 'primary':
            self.bg_color = self.theme['systemGreen']
            self.active_bg_color = self.theme['systemGreen_dark']
        else:
            self.bg_color = self.theme['systemRed']
            self.active_bg_color = self.theme['systemRed_dark']

    def update_theme(self, new_theme):
        """Called by the Controller to update the theme."""
        self.theme = new_theme
        self.update_colors()
        self.config(bg=self.theme['secondarySystemBackground'])
        self.itemconfig(self.tag_id, fill=self.bg_color if self.is_enabled else self.theme['tertiarySystemBackground'])
        self.itemconfig(self.text_id, fill=self.theme['buttonText'] if self.is_enabled else self.theme['secondaryLabel'])

    def on_resize(self, event):
        """Redraws the rounded rectangle and text when the component size changes."""
        self.delete(self.tag_id)
        self.tag_id = self.create_rounded_rectangle(0, 0, event.width, event.height, radius=25, fill=self.itemcget(self.tag_id, 'fill'))
        self.coords(self.text_id, event.width / 2, event.height / 2)
        self.tag_raise(self.text_id)

    def on_press(self, event):
        """Visual effect when the mouse is pressed."""
        if self.is_enabled:
            self.itemconfig(self.tag_id, fill=self.active_bg_color)

    def on_release(self, event):
        """Restores the original appearance and executes the command when the mouse is released."""
        if self.is_enabled:
            self.itemconfig(self.tag_id, fill=self.bg_color)
            if self.command:
                self.command()

    def set_text(self, text):
        """Sets the button text."""
        self.itemconfig(self.text_id, text=text)

    def set_state(self, state):
        """Sets the button state (enabled/disabled)."""
        self.is_enabled = (state == tk.NORMAL)
        if self.is_enabled:
            self.itemconfig(self.tag_id, fill=self.bg_color)
            self.itemconfig(self.text_id, fill=self.theme['buttonText'])
            self.bind("<Button-1>", self.on_press)
            self.bind("<ButtonRelease-1>", self.on_release)
        else:
            self.itemconfig(self.tag_id, fill=self.theme['tertiarySystemBackground'])
            self.itemconfig(self.text_id, fill=self.theme['secondaryLabel'])
            self.unbind("<Button-1>")
            self.unbind("<ButtonRelease-1>")

def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    """A helper function to draw a rounded rectangle on a Canvas."""
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return self.create_polygon(points, **kwargs, smooth=True)

# --- Monkey-patch a new method to the Canvas class ---
# This is a technique to dynamically add our function to Tkinter's Canvas class.
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle
