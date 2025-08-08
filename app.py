# app.py
# -*- coding: utf-8 -*-
"""
Main application controller for the FaunaLens program.

This class follows the Controller pattern in MVC. It's responsible for:
- Initializing the main application window and managers.
- Managing the application's state (e.g., theme, language, predictions).
- Handling all user events from the View and coordinating actions between
  the View and the Model (core logic).
"""

import tkinter as tk
from tkinter import filedialog
from PIL import Image
import json
import threading

# Import our refactored modules
from view import MainView
from core import ModelManager, WikipediaService
from theme_manager import ThemeManager
from config import WINDOW_SIZE_MAP

class AppController:
    """The main controller for the Tkinter application."""
    def __init__(self, root):
        """
        Initialize the application.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        
        # --- State Management ---
        # These variables hold the current state of the application.
        self.last_prediction = None
        self.model_loaded = False
        self.all_labels = []

        # --- Initialize Managers and Services ---
        # The controller creates and owns all the major components.
        self.model_manager = ModelManager()
        self.wiki_service = WikipediaService()
        
        # --- Load Settings and Translations ---
        self._load_translations()
        self._setup_tkinter_variables()

        # Initialize the Theme Manager AFTER setting up Tkinter variables
        self.theme_manager = ThemeManager(self.theme_mode, self.text_size)
        
        # --- Initialize the Main View ---
        # The view is given a reference to the controller to send back user actions.
        self.view = MainView(root, self)
        
        # --- Final Setup ---
        self.apply_initial_settings()
        self._load_model_async()

    def _load_translations(self):
        """Loads language strings from the JSON file."""
        try:
            with open('languages.json', 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            # Fallback in case the JSON is missing
            self.translations = {"en": {"error_message": "Language file not found."}}
            print("Error: languages.json not found!")

    def _setup_tkinter_variables(self):
        """Sets up the Tkinter StringVars that will be used to track settings."""
        self.current_lang = tk.StringVar(value='en')
        self.theme_mode = tk.StringVar(value='light')
        self.text_size = tk.StringVar(value='Medium')
        self.window_size = tk.StringVar(value='Standard')

    def apply_initial_settings(self):
        """Applies the default settings when the app starts."""
        self.root.title(self.translations['en'].get('window_title', 'FaunaLens'))
        self.apply_window_size()
        self.change_language() # Apply default language

    def _load_model_async(self):
        """
        Loads the heavyweight TensorFlow model in a separate thread
        to prevent the UI from freezing on startup.
        """
        self.view.show_loading_view()
        
        def task():
            self.model_loaded = self.model_manager.load_model()
            self.all_labels = self.model_manager.get_labels()
            # Once loaded, update the UI from the main thread
            self.root.after(0, self.on_model_loaded)

        threading.Thread(target=task, daemon=True).start()

    def on_model_loaded(self):
        """Callback function executed after the model is loaded."""
        print("Model loading complete. UI is now active.")
        # Re-enable the upload button and refresh the view
        self.view.show_initial_view()
        self.view.refresh_ui()

    # --- Event Handlers from the View ---

    def show_frame(self, page_name):
        """Tells the view to raise a specific page (e.g., 'SettingsPage')."""
        self.view.show_frame(page_name)

    def upload_and_predict(self):
        """Handles the 'Select File' button click."""
        file_path = filedialog.askopenfilename(
            title=self.get_translation("file_dialog_title"),
            filetypes=[
                (self.get_translation("file_types_images"), "*.jpg *.jpeg *.png *.bmp"),
                (self.get_translation("file_types_all"), "*.*")
            ]
        )
        if not file_path:
            return

        try:
            pil_image = Image.open(file_path)
            processed_image = self.model_manager.preprocess_image(pil_image)
            predictions = self.model_manager.predict(processed_image)
            
            if predictions:
                self.last_prediction = predictions
                self.view.show_results_view(pil_image, predictions)
                self.view.refresh_ui()
            else:
                self.view.show_popup("Error", "Failed to get a prediction.")

        except Exception as e:
            print(f"Error processing file: {e}")
            self.view.show_popup("Error", f"Could not open or process the file:\n{e}")

    def reset_to_initial_view(self):
        """Handles the 'Clear' button click."""
        self.view.show_initial_view()
        self.view.refresh_ui()

    def search_wikipedia(self, query):
        """
        Handles clicks on result rows to search Wikipedia.
        This runs in a separate thread to keep the UI responsive.
        """
        lang = self.current_lang.get()
        self.view.set_search_result_text(self.get_translation("searching"), "gray")

        def task():
            title, summary = self.wiki_service.fetch_summary(query, lang)
            if summary:
                # Show popup from the main thread
                self.root.after(0, lambda: self.view.show_popup(title, summary))
                self.root.after(0, lambda: self.view.set_search_result_text("", "black"))
            else:
                # Show error from the main thread
                self.root.after(0, lambda: self.view.set_search_result_text(self.get_translation("page_not_found"), "red"))
        
        threading.Thread(target=task, daemon=True).start()

    def manual_search(self):
        """Handles a manual search from the entry box."""
        query = self.view.pages["AIPage"].search_entry.get()
        if query and query != self.get_translation("search_placeholder"):
            self.search_wikipedia(query)
        else:
            self.view.set_search_result_text(self.get_translation("search_enter_keyword"), "red")

    def search_labels(self, query):
        """Live search through the loaded ImageNet labels."""
        if not query:
            self.view.set_search_result_text("", "black")
            return
            
        matches = [label for label in self.all_labels if query.lower() in label.lower()]
        
        if matches:
            result_text = f"{self.get_translation('search_found')} {len(matches)} {self.get_translation('search_total')}"
            self.view.set_search_result_text(result_text, self.theme_manager.get_current_theme_colors()['systemGreen'])
        else:
            self.view.set_search_result_text(self.get_translation('search_not_found'), "red")

    # --- Settings Handlers ---

    def change_language(self, event=None):
        """Applies the selected language and refreshes the entire UI."""
        print(f"Language changed to: {self.current_lang.get()}")
        self.root.title(self.get_translation('window_title'))
        self.view.refresh_ui()

    def toggle_theme(self):
        """Switches between 'light' and 'dark' themes."""
        new_theme = 'dark' if self.theme_mode.get() == 'light' else 'light'
        self.theme_mode.set(new_theme)
        print(f"Theme changed to: {self.theme_mode.get()}")
        self.view.refresh_ui()

    def apply_text_size(self, event=None):
        """Applies the selected text size."""
        self.theme_manager.update_fonts()
        print(f"Text size changed to: {self.text_size.get()}")
        self.view.refresh_ui()

    def apply_window_size(self, event=None):
        """Applies the selected window size."""
        new_geometry = WINDOW_SIZE_MAP.get(self.window_size.get())
        if new_geometry:
            self.root.geometry(new_geometry)
            print(f"Window size changed to: {self.window_size.get()} ({new_geometry})")

    # --- Utility Methods ---

    def get_translation(self, key, default=""):
        """Safely gets a translated string for the current language."""
        return self.translations.get(self.current_lang.get(), {}).get(key, default)
