# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import cv2
import threading
import json

# --- 從我們的模組引入功能 ---
import core
import utils
from view import MainUI, ResultRow # 從 view.py 引入我們的 UI 藍圖

# =================================================================================
#  v2.3: 總控制器 (The Controller)
#  這個檔案是 App 的大腦。它掌管所有狀態和邏輯，並命令 View 去更新畫面。
# =================================================================================
class AnimalIdentifierApp:
    def __init__(self, root):
        self.root = root
        self.translations = {}
        self.load_translations()

        self.theme_mode = tk.StringVar(value='light')
        self.themes = {
            'light': {
                'systemBackground': "#f0f0f0", 'secondarySystemBackground': "#ffffff", 'tertiarySystemBackground': "#f0f0f0",
                'label': "#000000", 'secondaryLabel': "#8a8a8e",
                'systemBlue': "#007aff", 'systemGreen': "#34c759", 'systemRed': "#ff3b30",
                'systemGreen_dark': "#2da44e", 'systemRed_dark': "#d9342b", 'buttonText': "#ffffff"
            },
            'dark': {
                'systemBackground': "#000000", 'secondarySystemBackground': "#1c1c1e", 'tertiarySystemBackground': "#2c2c2e",
                'label': "#ffffff", 'secondaryLabel': "#8d8d92",
                'systemBlue': "#0a84ff", 'systemGreen': "#30d158", 'systemRed': "#ff453a",
                'systemGreen_dark': "#28a745", 'systemRed_dark': "#e63946", 'buttonText': "#ffffff"
            }
        }

        self.current_lang = tk.StringVar(value='zh-tw' if 'zh-tw' in self.translations else 'en')
        self.font_map = {'ja': 'Meiryo UI', 'ko': 'Malgun Gothic', 'zh-cn': 'Microsoft YaHei UI', 'zh-tw': 'Microsoft JhengHei UI', 'default': 'Segoe UI'}

        # --- 建立 UI 實例 ---
        self.ui = MainUI(root, self)

        self.apply_theme()
        self.update_ui_text()
        threading.Thread(target=self.load_model_thread, daemon=True).start()

    def get_font(self, font_type='body'):
        lang = self.current_lang.get(); base_font = self.font_map.get(lang, self.font_map['default'])
        if font_type == 'title': return (base_font, 26, "bold")
        if font_type == 'button': return (base_font, 14, "bold")
        if font_type == 'result_title': return (base_font, 15, "bold")
        if font_type == 'result_row': return (base_font, 13)
        return (base_font, 13)

    def load_translations(self):
        locales_dir = utils.resource_path('locales')
        if not os.path.isdir(locales_dir):
            messagebox.showerror("Fatal Error", "Could not find 'locales' directory."); self.root.destroy(); return
        for filename in os.listdir(locales_dir):
            if filename.endswith('.json'):
                lang_code = filename.split('.')[0]
                try:
                    with open(os.path.join(locales_dir, filename), 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
                except Exception as e: print(f"Error loading {filename}: {e}")

    def load_model_thread(self):
        if core.load_classification_model(): self.root.after(0, self.on_model_loaded)
        else: self.root.after(0, lambda: messagebox.showerror("Model Error", "Failed to load classification model."))
    
    def on_model_loaded(self):
        self.ui.upload_button.set_state(tk.NORMAL); self.update_ui_text()

    def apply_theme(self):
        colors = self.themes[self.theme_mode.get()]
        self.root.configure(bg=colors['systemBackground'])
        self.ui.update_theme(colors)

    def reset_to_initial_view(self):
        self.ui.results_header_frame.pack_forget(); self.ui.results_frame.pack_forget()
        self.ui.image_canvas.pack(pady=10); self.last_prediction = None
        self.update_ui_text()

    def show_results_view(self, pil_image):
        self.ui.image_canvas.pack_forget()
        self.ui.results_header_frame.pack(fill=tk.X, pady=(25, 10), anchor='w')
        self.display_thumbnail(pil_image)
        self.ui.results_frame.pack(fill=tk.X, pady=(0, 20))

    def display_thumbnail(self, pil_image):
        thumb_img = pil_image.copy(); thumb_img.thumbnail((60, 60))
        rounded_thumb = utils.round_corners(thumb_img, 10)
        self.thumbnail_photo = ImageTk.PhotoImage(rounded_thumb)
        self.ui.thumbnail_canvas.delete("all"); self.ui.thumbnail_canvas.create_image(0, 0, image=self.thumbnail_photo, anchor='nw')

    def upload_and_predict(self):
        lang = self.current_lang.get(); trans = self.translations.get(lang, {})
        filetypes = [(trans.get('file_types_images', 'Images'), '*.jpg *.jpeg *.png *.bmp *.gif *.webp'), (trans.get('file_types_videos', 'Videos'), '*.mp4 *.avi *.mov *.mkv'), (trans.get('file_types_all', 'All'), '*.*')]
        file_path = filedialog.askopenfilename(title=trans.get('file_dialog_title', 'Select File'), filetypes=filetypes)
        if not file_path: return
        try:
            pil_image = self.get_pil_image_from_file(file_path)
            if pil_image:
                self.display_pil_image(pil_image)
                threading.Thread(target=self.run_prediction_thread, args=(pil_image,), daemon=True).start()
            else: raise ValueError("Unsupported file format or unable to read file.")
        except Exception as e: messagebox.showerror(trans.get('error_message', 'Error'), str(e))

    def run_prediction_thread(self, pil_image):
        processed_image = core.preprocess_image(pil_image)
        predictions = core.predict_classification(processed_image)
        if predictions is not None: self.root.after(0, self.display_prediction_results, pil_image, predictions)

    def display_prediction_results(self, pil_image, predictions):
        self.last_prediction = predictions; self.show_results_view(pil_image)
        self.create_clickable_predictions(predictions)
        first_prediction_label = predictions[0][1].replace('_', ' ').capitalize()
        self.search_wikipedia(first_prediction_label)

    def create_clickable_predictions(self, predictions_data):
        for widget in self.ui.results_frame.winfo_children(): widget.destroy()
        lang = self.current_lang.get(); trans = self.translations.get(lang, {})
        self.ui.result_title_label.config(text=trans.get('result_title', 'AI Results:'))
        theme = self.themes[self.theme_mode.get()]; font = self.get_font('result_row')
        for _, label, score in predictions_data:
            label_name = label.replace('_', ' ').capitalize(); result_data = (label_name, score)
            row = ResultRow(self.ui.results_frame, theme, font, result_data, self.search_wikipedia)
            row.pack(fill=tk.X, pady=2)

    def manual_search(self): query = self.ui.search_entry.get(); self.search_wikipedia(query) if query else None
    
    def search_wikipedia(self, query):
        self.ui.search_entry.delete(0, tk.END); self.ui.search_entry.insert(0, query)
        lang = self.current_lang.get(); trans = self.translations.get(lang, {})
        self.show_popup(trans.get('wiki_search_title', 'Search'), trans.get('searching', 'Searching...'))
        threading.Thread(target=self.fetch_wiki_summary_thread, args=(query,), daemon=True).start()

    def fetch_wiki_summary_thread(self, query):
        lang_code = self.current_lang.get().split('-')[0]; title, summary = core.fetch_wiki_summary(query, lang_code)
        lang = self.current_lang.get(); trans = self.translations.get(lang, {})
        if summary: self.root.after(0, self.show_popup, title, summary)
        else: self.root.after(0, self.show_popup, trans.get('wiki_search_title', 'Search'), trans.get('page_not_found', 'Page not found.'))

    def show_popup(self, title, content):
        if not hasattr(self, 'popup') or not self.popup.winfo_exists():
            self.popup = tk.Toplevel(self.root); self.popup_text = tk.Text(self.popup, wrap=tk.WORD, padx=15, pady=15, relief='flat')
            self.popup_text.pack(expand=True, fill=tk.BOTH)
        self.popup.title(title); self.popup_text.config(state=tk.NORMAL, font=self.get_font()); self.popup_text.delete(1.0, tk.END); self.popup_text.insert(tk.END, content)
        self.popup_text.config(state=tk.DISABLED); mode = self.theme_mode.get(); colors = self.themes[mode]
        self.popup.configure(bg=colors['systemBackground']); self.popup_text.configure(bg=colors['secondarySystemBackground'], fg=colors['label'])
        self.popup.deiconify(); self.popup.lift()

    def toggle_theme(self): self.theme_mode.set('dark' if self.theme_mode.get() == 'light' else 'light'); self.apply_theme()
    
    def update_ui_text(self):
        lang = self.current_lang.get(); trans = self.translations.get(lang, {})
        self.root.title(trans.get('window_title', 'Identifier'))
        self.ui.title_label.config(text=trans.get('main_title', 'Analysis'))
        if core.classification_model is None: self.ui.result_title_label.config(text=trans.get('loading_model', 'Loading...'))
        elif self.last_prediction is None: self.ui.result_title_label.config(text=trans.get('result_placeholder', 'Results here'))
        self.ui.upload_button.set_text(trans.get('select_button', 'Select')); self.ui.clear_button.set_text(trans.get('clear_button', 'Clear'))
    
    def change_language(self, event=None):
        self.apply_theme(); self.update_ui_text()
        if hasattr(self, 'last_prediction') and self.last_prediction: self.create_clickable_predictions(self.last_prediction)
    
    def get_pil_image_from_file(self, file_path):
        file_ext = os.path.splitext(file_path)[1].lower(); image_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']; video_exts = ['.mp4', '.avi', '.mov', '.mkv']
        if any(file_ext.endswith(ext) for ext in image_exts): return Image.open(file_path).convert('RGB')
        elif any(file_ext.endswith(ext) for ext in video_exts):
            cap = cv2.VideoCapture(file_path); cap.set(cv2.CAP_PROP_POS_MSEC, 1000); success, frame = cap.read(); cap.release()
            if success: return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return None
    
    def display_pil_image(self, pil_image):
        img_copy = pil_image.copy(); img_copy.thumbnail((450, 350)); rounded_img = utils.round_corners(img_copy, 20)
        self.photo = ImageTk.PhotoImage(rounded_img); self.ui.image_canvas.delete("all")
        self.ui.image_canvas.create_rounded_rectangle(0, 0, 450, 350, radius=20, fill=self.themes[self.theme_mode.get()]['tertiarySystemBackground'])
        self.ui.image_canvas.create_image(225, 175, image=self.photo)
