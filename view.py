# view.py
# -*- coding: utf-8 -*-
"""
Handles all UI rendering for the FaunaLens application.

This module contains the MainView, which manages all pages, and the specific
page classes (AIPage, SettingsPage). The View is responsible only for
displaying widgets and forwarding user actions to the AppController.
It gets all its data and styling information from the controller.
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import utils
from config import WINDOW_SIZE_MAP, TEXT_SIZE_MAP
from ui_components import ResultRow, CustomButton, IconCustomButton

class MainView(tk.Frame):
    """The main container for all application pages."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        
        # Main container setup
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        container = tk.Frame(self.parent)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        # Create instances of all pages
        for PageClass in (AIPage, SettingsPage):
            page_name = PageClass.__name__
            page = PageClass(parent=container, controller=self.controller)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_frame("AIPage")

    def show_frame(self, page_name):
        """Raises the specified page to the top."""
        page = self.pages[page_name]
        page.tkraise()
        page.refresh_ui() # Refresh UI every time a page is shown

    def refresh_ui(self):
        """Refreshes the UI of all pages."""
        for page in self.pages.values():
            page.refresh_ui()

    def show_initial_view(self):
        self.pages["AIPage"].show_initial_view()

    def show_loading_view(self):
        self.pages["AIPage"].show_loading_view()

    def show_results_view(self, pil_image, predictions):
        self.pages["AIPage"].show_results_view(pil_image, predictions)

    def show_popup(self, title, content):
        self.pages["AIPage"].show_popup(title, content)

    def set_search_result_text(self, text, color):
        self.pages["AIPage"].set_search_result_text(text, color)

class BasePage(tk.Frame):
    """Base class for all pages, containing common functionality."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Use the ThemeManager from the controller for all styling
        self.theme_manager = controller.theme_manager
        self.grid_columnconfigure(0, weight=1)

    def refresh_ui(self):
        """Destroys all current widgets and rebuilds the UI."""
        for widget in self.winfo_children():
            widget.destroy()
        self._build_ui()

    def _build_ui(self):
        """Placeholder for UI building logic in child classes."""
        raise NotImplementedError

class AIPage(BasePage):
    """The main analysis page of the application."""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        # Load theme-aware icons
        self.placeholder_icon = utils.get_image_from_data(utils.PLACEHOLDER_ICON_DATA, (100, 100))
        self._load_theme_icons()

        # State flags for this page
        self.is_initial_view = True
        self.is_loading = False
        self._current_pil_image = None
        
    def _load_theme_icons(self):
        """Loads the correct icons based on the current theme."""
        theme = self.controller.theme_mode.get()
        search_data = utils.SEARCH_ICON_DARK_THEME_DATA if theme == 'dark' else utils.SEARCH_ICON_LIGHT_THEME_DATA
        settings_data = utils.SETTINGS_ICON_DARK_THEME_DATA if theme == 'dark' else utils.SETTINGS_ICON_LIGHT_THEME_DATA
        self.search_icon = utils.get_image_from_data(search_data, (20, 20))
        self.settings_icon = utils.get_image_from_data(settings_data, (22, 22))

    def _build_ui(self):
        """Builds all widgets for the AI page based on the current state."""
        self._load_theme_icons() # Reload icons in case theme changed
        colors = self.theme_manager.get_current_theme_colors()
        self.config(bg=colors['systemBackground'])
        
        main_container = tk.Frame(self, bg=colors['systemBackground'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=1)

        self._build_header(main_container)
        self._build_content_area(main_container)
        self._build_footer(main_container)

    def _build_header(self, parent):
        colors = self.theme_manager.get_current_theme_colors()
        
        top_frame = tk.Frame(parent, bg=colors['systemBackground'])
        top_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        
        title_label = tk.Label(top_frame, text=self.controller.get_translation('main_title'),
                               font=self.theme_manager.get_font('title'),
                               bg=colors['systemBackground'], fg=colors['label'])
        title_label.pack(side=tk.LEFT, anchor='w')
        
        settings_button = IconCustomButton(top_frame, image=self.settings_icon,
                                           parent_bg=colors['systemBackground'],
                                           colors=self.theme_manager.get_button_colors('icon', parent_bg_key='systemBackground'),
                                           command=lambda: self.controller.show_frame("SettingsPage"))
        settings_button.pack(side=tk.RIGHT)

    def _build_content_area(self, parent):
        colors = self.theme_manager.get_current_theme_colors()
        content_frame = tk.Frame(parent, bg=colors['systemBackground'])
        content_frame.grid(row=1, column=0, sticky='nsew')
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        if self.is_initial_view:
            self._build_initial_view(content_frame)
        else:
            self._build_results_view(content_frame)

    def _build_initial_view(self, parent):
        colors = self.theme_manager.get_current_theme_colors()
        
        canvas = tk.Canvas(parent, highlightthickness=0, bg=colors['secondarySystemBackground'])
        canvas.grid(row=0, column=0, sticky='nsew')
        
        def draw_content(event=None):
            canvas.delete("all")
            width, height = canvas.winfo_width(), canvas.winfo_height()
            if self.is_loading:
                text = self.controller.get_translation('loading_model')
                canvas.create_text(width/2, height/2, text=text, font=self.theme_manager.get_font('title'), fill=colors['secondaryLabel'])
            else:
                canvas.create_image(width/2, height/2 - 40, image=self.placeholder_icon)
                text = self.controller.get_translation('initial_placeholder')
                canvas.create_text(width/2, height/2 + 40, text=text, font=self.theme_manager.get_font('result_title'), fill=colors['secondaryLabel'], width=300, justify='center')
        
        # Defer drawing until the canvas has a size
        canvas.bind("<Configure>", draw_content)

    def _build_results_view(self, parent):
        colors = self.theme_manager.get_current_theme_colors()
        
        results_frame_container = tk.Frame(parent, bg=colors['systemBackground'])
        results_frame_container.grid(row=0, column=0, sticky='nsew')
        
        results_header_frame = tk.Frame(results_frame_container, bg=colors['systemBackground'])
        results_header_frame.pack(fill=tk.X, pady=(0, 10), anchor='w')
        
        thumbnail_canvas = tk.Canvas(results_header_frame, width=60, height=60, highlightthickness=0, bg=colors['systemBackground'])
        thumbnail_canvas.pack(side=tk.LEFT, padx=(0, 15))
        self.display_thumbnail(thumbnail_canvas, self._current_pil_image)
        
        result_title_label = tk.Label(results_header_frame, text=self.controller.get_translation('result_title'),
                                          font=self.theme_manager.get_font('result_title'),
                                          bg=colors['systemBackground'], fg=colors['label'])
        result_title_label.pack(side=tk.LEFT, anchor='w')
        
        results_scroll_frame = tk.Frame(results_frame_container, bg=colors['secondarySystemBackground'])
        results_scroll_frame.pack(fill=tk.BOTH, expand=True)
        self.create_clickable_predictions(results_scroll_frame, self.controller.last_prediction)

    def _build_footer(self, parent):
        colors = self.theme_manager.get_current_theme_colors()
        footer_container = tk.Frame(parent, bg=colors['systemBackground'])
        footer_container.grid(row=2, column=0, sticky='ew', pady=(20, 0))
        footer_container.grid_columnconfigure(0, weight=1)
        
        self._build_search_bar(footer_container)
        self._build_action_buttons(footer_container)

    def _build_search_bar(self, parent):
        colors = self.theme_manager.get_current_theme_colors()
        
        search_container = tk.Frame(parent, bg=colors['systemBackground'])
        search_container.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        search_container.grid_columnconfigure(0, weight=1)
        
        search_frame = tk.Frame(search_container, bg=colors['tertiarySystemBackground'], height=50)
        search_frame.grid(row=0, column=0, sticky='ew')
        search_frame.grid_propagate(False)
        search_frame.grid_columnconfigure(0, weight=1)
        search_frame.grid_rowconfigure(0, weight=1)
        
        placeholder = self.controller.get_translation('search_placeholder')
        self.search_entry = tk.Entry(search_frame, relief='flat', font=self.theme_manager.get_font(),
                                     bg=colors['tertiarySystemBackground'], fg=colors['label'],
                                     insertbackground=colors['label'])
        self.search_entry.grid(row=0, column=0, sticky='ew', padx=(15, 50), pady=5)
        self.search_entry.insert(0, placeholder)
        self.search_entry.bind('<FocusIn>', lambda e, p=placeholder: self.search_entry.delete(0, tk.END) if self.search_entry.get() == p else None)
        self.search_entry.bind('<FocusOut>', lambda e, p=placeholder: self.search_entry.insert(0, p) if not self.search_entry.get() else None)
        self.search_entry.bind('<Return>', lambda e: self.controller.manual_search())
        self.search_entry.bind('<KeyRelease>', self.on_search_key_release)

        search_button = IconCustomButton(search_frame, image=self.search_icon,
                                         colors=self.theme_manager.get_button_colors('icon', parent_bg_key='tertiarySystemBackground'),
                                         command=self.controller.manual_search)
        search_button.grid(row=0, column=0, sticky='e', padx=(0, 8))
        
        self.search_result_label = tk.Label(search_container, text='', wraplength=450, justify=tk.LEFT,
                                            font=self.theme_manager.get_font(), bg=colors['systemBackground'], fg=colors['label'])
        self.search_result_label.grid(row=1, column=0, sticky='w', padx=15, pady=(2,0))

    def _build_action_buttons(self, parent):
        colors = self.theme_manager.get_current_theme_colors()
        button_container = tk.Frame(parent, bg=colors['systemBackground'])
        button_container.grid(row=1, column=0, sticky='ew', pady=(10, 0))
        button_container.grid_columnconfigure(0, weight=1)
        button_container.grid_columnconfigure(1, weight=1)

        self.clear_button = CustomButton(button_container, text=self.controller.get_translation('clear_button'),
                                         font=self.theme_manager.get_font('button'),
                                         colors=self.theme_manager.get_button_colors(button_type='secondary'),
                                         parent_bg=colors['systemBackground'],
                                         command=self.controller.reset_to_initial_view)
        self.clear_button.grid(row=0, column=0, sticky='ewns', padx=(0, 5))
        
        button_state = tk.NORMAL if self.controller.model_loaded else tk.DISABLED
        self.upload_button = CustomButton(button_container, text=self.controller.get_translation('select_button'),
                                          font=self.theme_manager.get_font('button'),
                                          colors=self.theme_manager.get_button_colors(button_type='primary'),
                                          parent_bg=colors['systemBackground'],
                                          state=button_state,
                                          command=self.controller.upload_and_predict)
        self.upload_button.grid(row=0, column=1, sticky='ewns', padx=(5, 0))

    def on_search_key_release(self, event):
        if event.keysym in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
            return
        query = self.search_entry.get()
        self.controller.search_labels(query)

    def show_initial_view(self):
        self.is_initial_view = True
        self.is_loading = False
        self.controller.last_prediction = None

    def show_loading_view(self):
        self.is_initial_view = True
        self.is_loading = True
        self.refresh_ui()

    def show_results_view(self, pil_image, predictions):
        self.is_initial_view = False
        self.is_loading = False
        self._current_pil_image = pil_image
        self.controller.last_prediction = predictions

    def display_thumbnail(self, canvas, pil_image):
        thumb_img = pil_image.copy()
        thumb_img.thumbnail((60, 60), Image.Resampling.LANCZOS)
        self.thumbnail_photo = ImageTk.PhotoImage(utils.round_corners(thumb_img, 10))
        canvas.delete("all")
        canvas.create_image(0, 0, image=self.thumbnail_photo, anchor='nw')

    def create_clickable_predictions(self, container, predictions_data):
        for widget in container.winfo_children(): widget.destroy()
        colors = self.theme_manager.get_current_theme_colors()
        font = self.theme_manager.get_font('result_row')
        for _, label, score in predictions_data:
            row = ResultRow(container, colors, font, (label.replace('_', ' ').capitalize(), score), self.controller.search_wikipedia)
            row.pack(fill=tk.X, pady=2)

    def show_popup(self, title, content):
        if not hasattr(self, 'popup') or not self.popup.winfo_exists():
            self.popup = tk.Toplevel(self.controller.root)
            self.popup.transient(self.controller.root) # Keep popup on top
            self.popup_text = tk.Text(self.popup, wrap=tk.WORD, padx=15, pady=15, relief='flat', borderwidth=0)
            self.popup_text.pack(expand=True, fill=tk.BOTH)
        
        self.popup.title(title)
        self.popup_text.config(state=tk.NORMAL, font=self.theme_manager.get_font())
        self.popup_text.delete(1.0, tk.END)
        self.popup_text.insert(tk.END, content)
        self.popup_text.config(state=tk.DISABLED)
        
        colors = self.theme_manager.get_current_theme_colors()
        self.popup.configure(bg=colors['systemBackground'])
        self.popup_text.configure(bg=colors['secondarySystemBackground'], fg=colors['label'])
        self.popup.deiconify()
        self.popup.lift()
        
        self.controller.root.update_idletasks()
        popup_width, popup_height = 500, 400
        x = self.controller.root.winfo_x() + (self.controller.root.winfo_width() // 2) - (popup_width // 2)
        y = self.controller.root.winfo_y() + (self.controller.root.winfo_height() // 2) - (popup_height // 2)
        self.popup.geometry(f'{popup_width}x{popup_height}+{x}+{y}')

    def set_search_result_text(self, text, color):
        self.search_result_label.config(text=text, fg=color)

class SettingsPage(BasePage):
    """The settings page of the application."""
    def _build_ui(self):
        """Builds all widgets for the Settings page."""
        colors = self.theme_manager.get_current_theme_colors()
        self.config(bg=colors['systemBackground'])
        
        main_container = tk.Frame(self, bg=colors['systemBackground'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        self._build_header(main_container)
        self._build_appearance_section(main_container)
        self._style_ttk_widgets()

    def _build_header(self, parent):
        colors = self.theme_manager.get_current_theme_colors()
        header_frame = tk.Frame(parent, bg=colors['systemBackground'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        title_label = tk.Label(header_frame, text=self.controller.get_translation('settings_title'),
                               font=self.theme_manager.get_font('title'),
                               bg=colors['systemBackground'], fg=colors['label'])
        title_label.pack(side=tk.LEFT, anchor='w')
        back_button = CustomButton(header_frame, text=self.controller.get_translation('back_button'),
                                   width=120, font=self.theme_manager.get_font('button'),
                                   colors=self.theme_manager.get_button_colors('primary'),
                                   parent_bg=colors['systemBackground'],
                                   command=lambda: self.controller.show_frame("AIPage"))
        back_button.pack(side=tk.RIGHT)

    def _build_appearance_section(self, parent):
        colors = self.theme_manager.get_current_theme_colors()
        appearance_label = tk.Label(parent, text=self.controller.get_translation('appearance_section'),
                                    font=self.theme_manager.get_font('result_title'),
                                    bg=colors['systemBackground'], fg=colors['label'])
        appearance_label.pack(anchor='w', pady=(10, 5))
        
        self._create_setting_row(parent, self.controller.get_translation('language_label'), self._build_lang_combo)
        self._create_setting_row(parent, self.controller.get_translation('theme_label'), self._build_theme_switch)
        self._create_setting_row(parent, self.controller.get_translation('text_size_label'), self._build_text_size_combo)
        self._create_setting_row(parent, self.controller.get_translation('window_size_label'), self._build_window_size_combo)

    def _style_ttk_widgets(self):
        colors = self.theme_manager.get_current_theme_colors()
        style = ttk.Style()
        style.map('TCombobox', fieldbackground=[('readonly', colors['secondarySystemBackground'])],
                  selectbackground=[('readonly', colors['secondarySystemBackground'])],
                  selectforeground=[('readonly', colors['label'])])
        style.configure("TCombobox", foreground=colors['label'], arrowcolor=colors['label'])
        style.configure("Switch.TCheckbutton", background=colors['systemBackground'], foreground=colors['label'])

    def _create_setting_row(self, parent, label_text, widget_builder):
        colors = self.theme_manager.get_current_theme_colors()
        frame = tk.Frame(parent, bg=colors['systemBackground'])
        frame.pack(fill=tk.X, pady=8)
        
        label = tk.Label(frame, text=label_text, font=self.theme_manager.get_font(),
                         bg=colors['systemBackground'], fg=colors['label'])
        label.pack(side=tk.LEFT, padx=(0, 10))
        
        widget_builder(frame)

    def _build_lang_combo(self, parent):
        lang_options = sorted(list(self.controller.translations.keys()))
        combo = ttk.Combobox(parent, textvariable=self.controller.current_lang, values=lang_options, state='readonly', width=15)
        combo.pack(side=tk.RIGHT)
        combo.bind("<<ComboboxSelected>>", self.controller.change_language)

    def _build_theme_switch(self, parent):
        is_dark = self.controller.theme_mode.get() == 'dark'
        switch = ttk.Checkbutton(parent, style="Switch.TCheckbutton", command=self.controller.toggle_theme,
                                 text="☀️" if is_dark else "🌙")
        switch.state(('selected',) if is_dark else ('!selected',))
        switch.pack(side=tk.RIGHT)

    def _build_text_size_combo(self, parent):
        options = list(self.controller.theme_manager.fonts.keys())
        combo = ttk.Combobox(parent, textvariable=self.controller.text_size, values=options, state='readonly', width=15)
        combo.pack(side=tk.RIGHT)
        combo.bind("<<ComboboxSelected>>", self.controller.apply_text_size)

    def _build_window_size_combo(self, parent):
        options = list(WINDOW_SIZE_MAP.keys())
        combo = ttk.Combobox(parent, textvariable=self.controller.window_size, values=options, state='readonly', width=15)
        combo.pack(side=tk.RIGHT)
        combo.bind("<<ComboboxSelected>>", self.controller.apply_window_size)
