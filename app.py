# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import cv2
import threading
import json
# import tensorflow as tf # This is now imported lazily in core.py

# --- Import functions from our modules ---
# import core # This is now imported lazily
import utils
from view import MainUI
from config import THEMES, FONT_MAP, FILE_TYPES_CONFIG

# =================================================================================
#  v2.9: The Controller
#  Update: Implemented lazy loading for the 'core' module to ensure the UI
#  appears instantly, before heavy libraries are loaded.
# =================================================================================
class AnimalIdentifierApp:
    def __init__(self, root):
        self.root = root
        self.translations = {}
        self.load_translations()

        # --- Application State ---
        self.theme_mode = tk.StringVar(value='light')
        default_lang = 'zh-tw' if 'zh-tw' in self.translations else 'en'
        self.current_lang = tk.StringVar(value=default_lang)
        self.last_prediction = None
        self.themes = THEMES
        self.font_map = FONT_MAP
        self.label_list = []
        self.model_loaded = False # New flag to track model status

        # --- Create UI instance ---
        self.ui = MainUI(root, self)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # --- Initialization ---
        self.apply_theme()
        self.update_ui_text()
        
        # Load the model and labels in a background thread
        threading.Thread(target=self.load_model_and_labels_thread, daemon=True).start()

    def get_font(self, font_type='body'):
        """Gets the font based on type and current language."""
        lang = self.current_lang.get()
        base_font = self.font_map.get(lang, self.font_map['default'])
        if font_type == 'title': return (base_font, 26, "bold")
        if font_type == 'button': return (base_font, 14, "bold")
        if font_type == 'result_title': return (base_font, 15, "bold")
        if font_type == 'result_row': return (base_font, 13)
        return (base_font, 13)

    def load_translations(self):
        """Loads all language translations from a single languages.json file."""
        try:
            lang_file_path = utils.resource_path('languages.json')
            with open(lang_file_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except Exception as e:
            messagebox.showerror("Fatal Error", f"Could not find or read 'languages.json': {e}")
            self.translations = {'en': {'window_title': 'Identifier'}}

    def load_model_and_labels_thread(self):
        """Loads the TensorFlow model and ImageNet labels in a background thread."""
        import core # Lazy import
        self.model_loaded = core.load_classification_model()
        if self.model_loaded:
            self.label_list = core.get_all_imagenet_labels()
            self.root.after(0, self.on_model_loaded)
        else:
            self.root.after(0, lambda: messagebox.showerror("Model Error", "Failed to load classification model."))
    
    def on_model_loaded(self):
        """Updates the UI on the main thread after the model has loaded."""
        self.ui.upload_button.set_state(tk.NORMAL)
        self.update_ui_text()

    def apply_theme(self):
        """Applies the currently selected theme colors to all UI components."""
        colors = self.themes[self.theme_mode.get()]
        self.root.configure(bg=colors['systemBackground'])
        self.ui.update_theme(colors)

    def reset_to_initial_view(self):
        """Resets the UI back to the initial upload screen."""
        self.last_prediction = None
        self.ui.show_initial_view()
        self.update_ui_text()

    def upload_and_predict(self):
        """Handles file upload and initiates the prediction process."""
        lang = self.current_lang.get()
        trans = self.translations.get(lang, {})
        
        filetypes = [
            (trans.get('file_types_images', 'Images'), ' '.join(FILE_TYPES_CONFIG['images'])),
            (trans.get('file_types_videos', 'Videos'), ' '.join(FILE_TYPES_CONFIG['videos'])),
            (trans.get('file_types_all', 'All'), '*.*')
        ]
        
        file_path = filedialog.askopenfilename(title=trans.get('file_dialog_title', 'Select File'), filetypes=filetypes)
        if not file_path:
            return
            
        try:
            self.ui.show_loading_view()
            pil_image = self.get_pil_image_from_file(file_path)
            if pil_image:
                threading.Thread(target=self.run_prediction_thread, args=(pil_image,), daemon=True).start()
            else:
                file_ext = os.path.splitext(file_path)[1].lower()
                raise ValueError(f"Unsupported file format or unable to read file: {file_ext}")
        except Exception as e:
            messagebox.showerror(trans.get('error_message', 'Error'), str(e))
            self.reset_to_initial_view()

    def run_prediction_thread(self, pil_image):
        """Runs image preprocessing and model prediction in a background thread."""
        import core # Lazy import
        processed_image = core.preprocess_image(pil_image)
        predictions = core.predict_classification(processed_image)
        if predictions is not None:
            self.root.after(0, self.display_prediction_results, pil_image, predictions)

    def display_prediction_results(self, pil_image, predictions):
        """Displays the prediction results."""
        self.last_prediction = predictions
        self.ui.show_results_view(pil_image, predictions)
        first_prediction_label = predictions[0][1].replace('_', ' ').capitalize()
        self.search_wikipedia(first_prediction_label)

    def manual_search(self):
        """Manually triggers a Wikipedia search."""
        query = self.ui.search_entry.get()
        if query:
            self.search_wikipedia(query)
    
    def search_wikipedia(self, query):
        """Searches Wikipedia with the given query."""
        self.ui.search_entry.delete(0, tk.END)
        self.ui.search_entry.insert(0, query)
        lang = self.current_lang.get()
        trans = self.translations.get(lang, {})
        self.ui.show_popup(trans.get('wiki_search_title', 'Search'), trans.get('searching', 'Searching...'))
        threading.Thread(target=self.fetch_wiki_summary_thread, args=(query,), daemon=True).start()

    def fetch_wiki_summary_thread(self, query):
        """Fetches the Wikipedia summary in a background thread."""
        import core # Lazy import
        lang_code = self.current_lang.get().split('-')[0]
        title, summary = core.fetch_wikipedia_summary(query, lang_code)
        lang = self.current_lang.get()
        trans = self.translations.get(lang, {})
        if summary:
            self.root.after(0, self.ui.show_popup, title, summary)
        else:
            self.root.after(0, self.ui.show_popup, trans.get('wiki_search_title', 'Search'), trans.get('page_not_found', 'Page not found.'))

    def toggle_theme(self):
        """Toggles between light and dark themes."""
        self.theme_mode.set('dark' if self.theme_mode.get() == 'light' else 'light')
        self.apply_theme()
    
    def update_ui_text(self):
        """Updates all text elements in the UI based on the current language."""
        lang = self.current_lang.get()
        trans = self.translations.get(lang, {})
        self.root.title(trans.get('window_title', 'Identifier'))
        self.ui.title_label.config(text=trans.get('main_title', 'Analysis'))
        
        if not self.model_loaded:
            self.ui.result_title_label.config(text=trans.get('loading_model', 'Loading...'))
        elif self.last_prediction is None:
            self.ui.result_title_label.config(text=trans.get('result_placeholder', 'Results will appear here'))
        
        self.ui.upload_button.set_text(trans.get('select_button', 'Select File'))
        self.ui.clear_button.set_text(trans.get('clear_button', 'Clear'))
        self.ui.update_language_dependent_text(trans)
    
    def change_language(self, event=None):
        """Handles the language change event."""
        self.apply_theme()
        self.update_ui_text()
        if self.last_prediction:
            self.ui.create_clickable_predictions(self.last_prediction)
    
    def get_pil_image_from_file(self, file_path):
        """Reads an image or video frame from a file path and returns a PIL Image object."""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        image_exts = [ext.replace('*', '') for ext in FILE_TYPES_CONFIG['images']]
        video_exts = [ext.replace('*', '') for ext in FILE_TYPES_CONFIG['videos']]

        if file_ext in image_exts:
            return Image.open(file_path).convert('RGB')
        elif file_ext in video_exts:
            cap = cv2.VideoCapture(file_path)
            cap.set(cv2.CAP_PROP_POS_MSEC, 1000)
            success, frame = cap.read()
            cap.release()
            if success:
                return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return None

    def animal_label_search(self):
        """Searches for a keyword in the loaded ImageNet labels."""
        query = self.ui.search_entry.get().strip().lower()
        lang = self.current_lang.get()
        trans = self.translations.get(lang, {})
        
        if not query:
            self.ui.set_search_result_text(trans.get('search_enter_keyword', 'Please enter a keyword'), '#ff3b30')
            return
            
        if not self.label_list:
            self.ui.set_search_result_text(trans.get('search_loading', 'Labels loading...'), '#8a8a8e')
            return

        matches = [label for label in self.label_list if query in label.lower()]
        
        if matches:
            result_text = f"{trans.get('search_found', 'Found')} {len(matches)}: " + ', '.join(matches[:5])
            if len(matches) > 5:
                result_text += f" ... ({len(matches)} {trans.get('search_total', 'total')})"
            self.ui.set_search_result_text(result_text, '#34c759')
        else:
            self.ui.set_search_result_text(trans.get('search_not_found', 'No related animal names found'), '#ff3b30')
