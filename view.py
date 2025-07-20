# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

# =================================================================================
#  v2.3: UI 藍圖 (The View)
#  這個檔案只負責「畫」出介面，它本身沒有任何邏輯。
#  它像一個啞巴的建築師，只依照 Controller 的指示蓋房子。
# =================================================================================
class MainUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # --- 介面佈局 ---
        self.grid(row=0, column=0, sticky='nsew', padx=30, pady=30)
        self.grid_columnconfigure(0, weight=1)

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(fill=tk.X, pady=(10, 15))
        
        lang_options = sorted(list(self.controller.translations.keys()))
        self.lang_combo = ttk.Combobox(self.top_frame, textvariable=self.controller.current_lang, values=lang_options, state='readonly', width=8)
        self.lang_combo.pack(side=tk.RIGHT, padx=(10, 0))
        self.lang_combo.bind("<<ComboboxSelected>>", self.controller.change_language)
        
        self.theme_switch = ttk.Checkbutton(self.top_frame, text="🌙", style="Switch.TCheckbutton", command=self.controller.toggle_theme)
        self.theme_switch.pack(side=tk.RIGHT)
        
        self.title_label = tk.Label(self, font=self.controller.get_font('title'))
        self.title_label.pack(pady=(0, 20), anchor='w')
        
        self.image_canvas = tk.Canvas(self, width=450, height=350, highlightthickness=0)
        
        self.results_header_frame = tk.Frame(self)
        self.thumbnail_canvas = tk.Canvas(self.results_header_frame, width=60, height=60, highlightthickness=0)
        self.thumbnail_canvas.pack(side=tk.LEFT, padx=(0, 10))
        self.result_title_label = tk.Label(self.results_header_frame, font=self.controller.get_font('result_title'))
        self.result_title_label.pack(side=tk.LEFT, anchor='w')
        
        self.results_frame = tk.Frame(self)
        
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(fill=tk.X, pady=(10, 10))
        self.search_bg_canvas = tk.Canvas(self.search_frame, height=40, highlightthickness=0)
        self.search_bg_canvas.pack(fill=tk.X, expand=True)
        self.search_entry = tk.Entry(self.search_bg_canvas, relief='flat', font=self.controller.get_font())
        self.search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15)
        
        self.button_container = tk.Frame(self)
        self.button_container.pack(fill=tk.X, pady=(15, 10))
        self.button_container.grid_columnconfigure(0, weight=1)
        self.button_container.grid_columnconfigure(1, weight=1)

        self.clear_button = RoundedButton(self.button_container, "", self.controller.reset_to_initial_view, self.controller.themes[self.controller.theme_mode.get()], self.controller.get_font('button'), type='secondary')
        self.clear_button.grid(row=0, column=0, sticky='ew', padx=(0, 5))
        self.upload_button = RoundedButton(self.button_container, "", self.controller.upload_and_predict, self.controller.themes[self.controller.theme_mode.get()], self.controller.get_font('button'), type='primary')
        self.upload_button.grid(row=0, column=1, sticky='ew', padx=(5, 0))

    def update_theme(self, colors):
        """由 Controller 呼叫，用來更新所有元件的顏色"""
        self.config(bg=colors['secondarySystemBackground'])
        self.top_frame.config(bg=colors['secondarySystemBackground'])
        self.results_frame.config(bg=colors['secondarySystemBackground'])
        self.search_frame.config(bg=colors['secondarySystemBackground'])
        self.results_header_frame.config(bg=colors['secondarySystemBackground'])
        self.thumbnail_canvas.config(bg=colors['secondarySystemBackground'])
        self.button_container.config(bg=colors['secondarySystemBackground'])
        
        self.title_label.config(bg=colors['secondarySystemBackground'], fg=colors['label'])
        self.result_title_label.config(bg=colors['secondarySystemBackground'], fg=colors['label'])
        self.search_entry.config(bg=colors['tertiarySystemBackground'], fg=colors['label'], insertbackground=colors['label'])
        
        self.clear_button.update_theme(colors)
        self.upload_button.update_theme(colors)
        
        self.image_canvas.delete("all")
        self.image_canvas.create_rounded_rectangle(0, 0, 450, 350, radius=20, fill=colors['tertiarySystemBackground'])
        if hasattr(self.controller, 'photo'):
            self.image_canvas.create_image(225, 175, image=self.controller.photo)
        
        style = ttk.Style()
        style.configure("TCombobox", fieldbackground=colors['secondarySystemBackground'], foreground=colors['label'], arrowcolor=colors['label'])
        style.configure("Switch.TCheckbutton", background=colors['secondarySystemBackground'])
        self.theme_switch.config(text="☀️" if self.controller.theme_mode.get() == 'dark' else "🌙")

        self.search_bg_canvas.config(bg=colors['secondarySystemBackground'])
        self.search_bg_canvas.delete('all')
        self.search_bg_canvas.create_rounded_rectangle(0, 0, self.search_bg_canvas.winfo_width(), 40, radius=20, fill=colors['tertiarySystemBackground'])
        self.search_entry.place(in_=self.search_bg_canvas, relx=0, rely=0, relwidth=1, relheight=1)

# --- 這些自訂元件也屬於 View 的一部分 ---
class ResultRow(tk.Frame):
    def __init__(self, parent, theme, font, result_data, search_callback):
        super().__init__(parent, bg=theme['secondarySystemBackground'])
        self.theme = theme; self.font = font
        label_name, score = result_data
        self.grid_columnconfigure(1, weight=1)
        self.name_label = tk.Label(self, text=label_name, font=self.font, anchor='w', bg=self.theme['secondarySystemBackground'], fg=self.theme['label'])
        self.name_label.grid(row=0, column=0, sticky='w', padx=(15, 5), pady=8)
        s = ttk.Style(); s.configure('Result.Horizontal.TProgressbar', troughcolor=theme['tertiarySystemBackground'], background=theme['systemBlue'], thickness=8, bordercolor=theme['tertiarySystemBackground'])
        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=100, mode='determinate', value=score * 100, style='Result.Horizontal.TProgressbar')
        self.progress_bar.grid(row=0, column=1, sticky='we', padx=5, pady=8)
        self.score_label = tk.Label(self, text=f"{score:.1%}", font=self.font, anchor='e', bg=self.theme['secondarySystemBackground'], fg=self.theme['secondaryLabel'])
        self.score_label.grid(row=0, column=2, sticky='e', padx=(5, 15), pady=8)
        self.bind_all_children("<Button-1>", lambda e, l=label_name: search_callback(l)); self.bind_all_children("<Enter>", self.on_enter); self.bind_all_children("<Leave>", self.on_leave)
    def bind_all_children(self, event, callback): self.bind(event, callback); [child.bind(event, callback) for child in self.winfo_children()]
    def on_enter(self, event):
        self.config(bg=self.theme['tertiarySystemBackground'])
        for child in self.winfo_children():
            if not isinstance(child, ttk.Progressbar): child.config(bg=self.theme['tertiarySystemBackground'])
    def on_leave(self, event):
        self.config(bg=self.theme['secondarySystemBackground'])
        for child in self.winfo_children():
            if not isinstance(child, ttk.Progressbar): child.config(bg=self.theme['secondarySystemBackground'])

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, theme, font, type='primary'):
        self.theme = theme; self.command = command; self.text = text; self.font = font; self.type = type
        self.update_colors()
        super().__init__(parent, height=50, highlightthickness=0, bg=theme['secondarySystemBackground'])
        self.tag_id = self.create_rounded_rectangle(0, 0, self.winfo_width(), 50, radius=25, fill=self.bg_color)
        self.text_id = self.create_text(0, 0, text=self.text, font=self.font, fill=self.theme['buttonText'])
        self.bind("<Configure>", self.on_resize); self.bind("<Button-1>", self.on_press); self.bind("<ButtonRelease-1>", self.on_release)
    def update_colors(self):
        if self.type == 'primary': self.bg_color = self.theme['systemGreen']; self.active_bg_color = self.theme['systemGreen_dark']
        else: self.bg_color = self.theme['systemRed']; self.active_bg_color = self.theme['systemRed_dark']
    def update_theme(self, new_theme):
        self.theme = new_theme; self.update_colors()
        self.config(bg=self.theme['secondarySystemBackground']); self.itemconfig(self.tag_id, fill=self.bg_color); self.itemconfig(self.text_id, fill=self.theme['buttonText'])
    def on_resize(self, event):
        self.delete(self.tag_id); self.tag_id = self.create_rounded_rectangle(0, 0, event.width, event.height, radius=25, fill=self.bg_color)
        self.coords(self.text_id, event.width / 2, event.height / 2); self.tag_raise(self.text_id)
    def on_press(self, event): self.itemconfig(self.tag_id, fill=self.active_bg_color)
    def on_release(self, event): self.itemconfig(self.tag_id, fill=self.bg_color); self.command() if self.command else None
    def set_text(self, text): self.itemconfig(self.text_id, text=text)
    def set_state(self, state):
        if state == tk.DISABLED:
            self.itemconfig(self.tag_id, fill=self.theme['tertiarySystemBackground']); self.itemconfig(self.text_id, fill=self.theme['secondaryLabel'])
            self.unbind("<Button-1>"); self.unbind("<ButtonRelease-1>")
        else:
            self.itemconfig(self.tag_id, fill=self.bg_color); self.itemconfig(self.text_id, fill=self.theme['buttonText'])
            self.bind("<Button-1>", self.on_press); self.bind("<ButtonRelease-1>", self.on_release)

def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius,y1, x1+radius,y1, x2-radius,y1, x2-radius,y1, x2,y1, x2,y1+radius, x2,y1+radius, x2,y2-radius, x2,y2-radius, x2,y2, x2-radius,y2, x2-radius,y2, x1+radius,y2, x1+radius,y2, x1,y2, x1,y2-radius, x1,y2-radius, x1,y1+radius, x1,y1+radius, x1,y1]
    return self.create_polygon(points, **kwargs, smooth=True)
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle
