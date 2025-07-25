# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import utils

# Import custom components from our UI components module
from ui_components import RoundedButton, ResultRow

# =================================================================================
#  v2.5: The View (UI Blueprint)
#  This file is only responsible for "drawing" the interface.
#  Update: Now loads embedded image data from utils.py instead of from files.
# =================================================================================
class MainUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        
        # Load image resources (from Base64 data)
        self.placeholder_icon = utils.get_image_from_data(utils.PLACEHOLDER_ICON_DATA, (100, 100))
        self.search_icon = utils.get_image_from_data(utils.SEARCH_ICON_DATA, (20, 20))

        # --- UI Layout ---
        self.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        self.grid_columnconfigure(0, weight=1)
        
        # --- Create all UI components ---
        self._create_widgets()
        self.show_initial_view()

    def _create_widgets(self):
        """Creates and places all UI components."""
        # --- Top frame (language and theme switch) ---
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(fill=tk.X, pady=(0, 15))
        
        lang_options = sorted(list(self.controller.translations.keys()))
        self.lang_combo = ttk.Combobox(self.top_frame, textvariable=self.controller.current_lang, values=lang_options, state='readonly', width=8)
        self.lang_combo.pack(side=tk.RIGHT, padx=(10, 0))
        self.lang_combo.bind("<<ComboboxSelected>>", self.controller.change_language)
        
        self.theme_switch = ttk.Checkbutton(self.top_frame, text="🌙", style="Switch.TCheckbutton", command=self.controller.toggle_theme)
        self.theme_switch.pack(side=tk.RIGHT)
        
        # --- Title ---
        self.title_label = tk.Label(self, font=self.controller.get_font('title'))
        self.title_label.pack(pady=(0, 20), anchor='w')
        
        # --- Content frame (switches between image and results) ---
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Initial screen (upload prompt)
        self.initial_canvas = tk.Canvas(self.content_frame, highlightthickness=0)
        
        # Results screen
        self.results_frame_container = tk.Frame(self.content_frame)
        self.results_header_frame = tk.Frame(self.results_frame_container)
        self.thumbnail_canvas = tk.Canvas(self.results_header_frame, width=60, height=60, highlightthickness=0)
        self.result_title_label = tk.Label(self.results_header_frame, font=self.controller.get_font('result_title'))
        
        self.results_scroll_frame = tk.Frame(self.results_frame_container)
        self.results_frame = tk.Frame(self.results_scroll_frame)

        # --- Search frame ---
        self.search_container = tk.Frame(self)
        self.search_container.pack(fill=tk.X, pady=(20, 10))
        self.search_container.grid_columnconfigure(0, weight=1)

        self.search_frame = tk.Frame(self.search_container)
        self.search_frame.grid(row=0, column=0, sticky='ew')
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = tk.Entry(self.search_frame, relief='flat', font=self.controller.get_font())
        self.search_entry.grid(row=0, column=0, sticky='ew', padx=(15, 40), pady=10)
        self.search_entry.bind('<Return>', lambda e: self.controller.manual_search())
        self.search_entry.bind('<KP_Enter>', lambda e: self.controller.manual_search())

        self.search_button = tk.Button(self.search_frame, image=self.search_icon, relief='flat', command=self.controller.manual_search)
        self.search_button.grid(row=0, column=0, sticky='e', padx=10)

        self.search_result_label = tk.Label(self.search_container, text='', font=self.controller.get_font(), wraplength=450, justify=tk.LEFT)
        self.search_result_label.grid(row=1, column=0, sticky='w', padx=15, pady=(2,0))
        
        # --- Button container ---
        self.button_container = tk.Frame(self)
        self.button_container.pack(fill=tk.X, pady=(10, 0))
        self.button_container.grid_columnconfigure(0, weight=1)
        self.button_container.grid_columnconfigure(1, weight=1)

        self.clear_button = RoundedButton(self.button_container, "", self.controller.reset_to_initial_view, self.controller.themes[self.controller.theme_mode.get()], self.controller.get_font('button'), type='secondary')
        self.clear_button.grid(row=0, column=0, sticky='ew', padx=(0, 5))
        self.upload_button = RoundedButton(self.button_container, "", self.controller.upload_and_predict, self.controller.themes[self.controller.theme_mode.get()], self.controller.get_font('button'), type='primary')
        self.upload_button.grid(row=0, column=1, sticky='ew', padx=(5, 0))
        # Disabled by default until the model is loaded
        self.upload_button.set_state(tk.DISABLED)

    def show_initial_view(self):
        """Shows the initial upload prompt screen."""
        self.results_frame_container.pack_forget()
        self.initial_canvas.pack(fill=tk.BOTH, expand=True)
        self.update_placeholder()

    def show_loading_view(self):
        """Shows the loading screen."""
        self.results_frame_container.pack_forget()
        self.initial_canvas.pack(fill=tk.BOTH, expand=True)
        self.initial_canvas.delete("all")
        colors = self.controller.themes[self.controller.theme_mode.get()]
        self.initial_canvas.create_rounded_rectangle(0, 0, 450, 350, radius=20, fill=colors['tertiarySystemBackground'], outline="")
        trans = self.controller.translations.get(self.controller.current_lang.get(), {})
        loading_text = trans.get('loading', 'Loading...')
        self.initial_canvas.create_text(225, 175, text=loading_text, font=self.controller.get_font('title'), fill=colors['secondaryLabel'])

    def show_results_view(self, pil_image, predictions):
        """Shows the image thumbnail and prediction results."""
        self.initial_canvas.pack_forget()
        self.results_frame_container.pack(fill=tk.BOTH, expand=True)
        
        self.results_header_frame.pack(fill=tk.X, pady=(0, 10), anchor='w')
        self.thumbnail_canvas.pack(side=tk.LEFT, padx=(0, 15))
        self.result_title_label.pack(side=tk.LEFT, anchor='w')
        
        self.results_scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        self.display_thumbnail(pil_image)
        self.create_clickable_predictions(predictions)

    def display_thumbnail(self, pil_image):
        """Displays the rounded thumbnail in the top-left corner."""
        thumb_img = pil_image.copy()
        thumb_img.thumbnail((60, 60), Image.Resampling.LANCZOS)
        rounded_thumb = utils.round_corners(thumb_img, 10)
        self.thumbnail_photo = ImageTk.PhotoImage(rounded_thumb)
        self.thumbnail_canvas.delete("all")
        self.thumbnail_canvas.create_image(0, 0, image=self.thumbnail_photo, anchor='nw')

    def create_clickable_predictions(self, predictions_data):
        """Creates the list of clickable prediction results."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        trans = self.controller.translations.get(self.controller.current_lang.get(), {})
        self.result_title_label.config(text=trans.get('result_title', 'AI Results:'))
        
        theme = self.controller.themes[self.controller.theme_mode.get()]
        font = self.controller.get_font('result_row')
        
        for _, label, score in predictions_data:
            label_name = label.replace('_', ' ').capitalize()
            result_data = (label_name, score)
            row = ResultRow(self.results_frame, theme, font, result_data, self.controller.search_wikipedia)
            row.pack(fill=tk.X, pady=2)

    def show_popup(self, title, content):
        """Displays a popup window with the Wikipedia summary."""
        if not hasattr(self, 'popup') or not self.popup.winfo_exists():
            self.popup = tk.Toplevel(self.parent)
            self.popup_text = tk.Text(self.popup, wrap=tk.WORD, padx=15, pady=15, relief='flat', borderwidth=0)
            self.popup_text.pack(expand=True, fill=tk.BOTH)
        
        self.popup.title(title)
        self.popup_text.config(state=tk.NORMAL, font=self.controller.get_font())
        self.popup_text.delete(1.0, tk.END)
        self.popup_text.insert(tk.END, content)
        self.popup_text.config(state=tk.DISABLED)
        
        mode = self.controller.theme_mode.get()
        colors = self.controller.themes[mode]
        self.popup.configure(bg=colors['systemBackground'])
        self.popup_text.configure(bg=colors['secondarySystemBackground'], fg=colors['label'])
        
        self.popup.deiconify()
        self.popup.lift()
        # Center the popup
        self.parent.update_idletasks()
        popup_width = 500
        popup_height = 400
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (popup_width // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (popup_height // 2)
        self.popup.geometry(f'{popup_width}x{popup_height}+{x}+{y}')

    def set_search_result_text(self, text, color):
        """Sets the text and color of the search result label."""
        self.search_result_label.config(text=text, fg=color)

    def update_language_dependent_text(self, trans):
        """Updates language-dependent text on the UI (e.g., placeholder text)."""
        self.update_placeholder(trans)
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, trans.get('search_placeholder', "Search Wikipedia or check labels..."))

    def update_placeholder(self, trans=None):
        """Updates the placeholder text and icon on the initial screen."""
        if trans is None:
            trans = self.controller.translations.get(self.controller.current_lang.get(), {})
        
        self.initial_canvas.delete("all")
        colors = self.controller.themes[self.controller.theme_mode.get()]
        self.initial_canvas.create_rounded_rectangle(0, 0, 450, 350, radius=20, fill=colors['tertiarySystemBackground'], outline="")
        self.initial_canvas.create_image(225, 140, image=self.placeholder_icon)
        placeholder_text = trans.get('initial_placeholder', "Select a file to start analysis")
        self.initial_canvas.create_text(225, 220, text=placeholder_text, font=self.controller.get_font('result_title'), fill=colors['secondaryLabel'], width=300)

    def update_theme(self, colors):
        """Called by the Controller to update the colors of all components."""
        self.config(bg=colors['systemBackground'])
        self.top_frame.config(bg=colors['systemBackground'])
        self.content_frame.config(bg=colors['systemBackground'])
        self.results_frame_container.config(bg=colors['systemBackground'])
        self.results_header_frame.config(bg=colors['systemBackground'])
        self.thumbnail_canvas.config(bg=colors['systemBackground'])
        self.results_scroll_frame.config(bg=colors['systemBackground'])
        self.results_frame.config(bg=colors['secondarySystemBackground'])
        self.search_container.config(bg=colors['systemBackground'])
        self.button_container.config(bg=colors['systemBackground'])
        
        self.title_label.config(bg=colors['systemBackground'], fg=colors['label'])
        self.result_title_label.config(bg=colors['secondarySystemBackground'], fg=colors['label'])
        self.search_result_label.config(bg=colors['systemBackground'])

        # Update search bar
        self.search_frame.config(bg=colors['tertiarySystemBackground'])
        self.search_entry.config(bg=colors['tertiarySystemBackground'], fg=colors['label'], insertbackground=colors['label'])
        self.search_button.config(bg=colors['tertiarySystemBackground'], activebackground=colors['secondarySystemBackground'])
        
        # Update custom buttons
        self.clear_button.update_theme(colors)
        self.upload_button.update_theme(colors)
        
        # Update initial canvas
        if self.initial_canvas.winfo_ismapped():
            self.update_placeholder()
        
        # Update result rows if they exist
        for child in self.results_frame.winfo_children():
            if isinstance(child, ResultRow):
                child.config(bg=colors['secondarySystemBackground'])
                child.name_label.config(bg=colors['secondarySystemBackground'], fg=colors['label'])
                child.score_label.config(bg=colors['secondarySystemBackground'], fg=colors['secondaryLabel'])

        # Update ttk styles
        style = ttk.Style()
        style.map('TCombobox', fieldbackground=[('readonly', colors['secondarySystemBackground'])])
        style.map('TCombobox', selectbackground=[('readonly', colors['secondarySystemBackground'])])
        style.map('TCombobox', selectforeground=[('readonly', colors['label'])])
        style.configure("TCombobox", foreground=colors['label'], arrowcolor=colors['label'])
        style.configure("Switch.TCheckbutton", background=colors['systemBackground'], foreground=colors['label'])
        self.theme_switch.config(text="☀️" if self.controller.theme_mode.get() == 'dark' else "🌙")
