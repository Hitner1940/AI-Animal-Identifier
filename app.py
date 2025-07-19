# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import os
import cv2
import threading
import json

# --- 從我們的模組引入功能 ---
import core
import utils

class AnimalIdentifierApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("550x750")
        self.translations = {}
        self.load_translations()

        # --- 主題與顏色管理 ---
        self.theme_mode = tk.StringVar(value='light')
        self.themes = {
            'light': { 'BG': "#f0f0f0", 'TEXT': "#000000", 'ACCENT': "#007aff", 'FRAME_BG': "#ffffff", 'FRAME_BORDER': "#dcdcdc", 'BUTTON_TEXT': "#ffffff", 'SECONDARY_BG': "#e5e5ea" },
            'dark': { 'BG': "#1e1e1e", 'TEXT': "#e0e0e0", 'ACCENT': "#0a84ff", 'FRAME_BG': "#2c2c2e", 'FRAME_BORDER': "#404040", 'BUTTON_TEXT': "#ffffff", 'SECONDARY_BG': "#3a3a3c" }
        }

        # --- 語言與字體管理 ---
        self.current_lang = tk.StringVar(value='zh-tw' if 'zh-tw' in self.translations else 'en')
        self.font_map = {
            'ja': 'Meiryo UI', 'ko': 'Malgun Gothic', 'zh-cn': 'Microsoft YaHei UI',
            'zh-tw': 'Microsoft JhengHei UI', 'default': 'Segoe UI'
        }

        # --- 介面佈局 ---
        self.main_frame = tk.Frame(root); self.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        self.top_frame = tk.Frame(self.main_frame); self.top_frame.pack(fill=tk.X, pady=(0, 20))
        lang_options = sorted(list(self.translations.keys()))
        self.lang_combo = ttk.Combobox(self.top_frame, textvariable=self.current_lang, values=lang_options, state='readonly', width=8)
        self.lang_combo.pack(side=tk.RIGHT, padx=(10, 0)); self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)
        self.theme_switch = ttk.Checkbutton(self.top_frame, text="🌙", style="Switch.TCheckbutton", command=self.toggle_theme)
        self.theme_switch.pack(side=tk.RIGHT)
        self.title_label = tk.Label(self.main_frame); self.title_label.pack(pady=(0, 25), anchor='w')
        self.image_canvas = tk.Canvas(self.main_frame, width=450, height=350, highlightthickness=0); self.image_canvas.pack(pady=10)
        self.result_title_label = tk.Label(self.main_frame); self.result_title_label.pack(pady=(15, 5), anchor='w')
        self.results_frame = tk.Frame(self.main_frame); self.results_frame.pack(fill=tk.X)
        self.search_frame = tk.Frame(self.main_frame); self.search_frame.pack(fill=tk.X, pady=(20, 10))
        self.search_entry = tk.Entry(self.search_frame); self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=5)
        self.search_button = tk.Button(self.search_frame, relief='flat', borderwidth=0, command=self.manual_search); self.search_button.pack(side=tk.RIGHT, padx=(10, 0), ipady=5)
        self.upload_button = tk.Button(self.main_frame, relief='flat', borderwidth=0, command=self.upload_and_predict, state=tk.DISABLED); self.upload_button.pack(pady=(10, 0), ipady=10, fill=tk.X)

        self.apply_theme()
        self.update_ui_text()
        threading.Thread(target=self.load_model_thread, daemon=True).start()

    def get_font(self, font_type='body'):
        lang = self.current_lang.get()
        base_font = self.font_map.get(lang, self.font_map['default'])
        if font_type == 'title': return (base_font, 22, "bold")
        if font_type == 'button': return (base_font, 12, "bold")
        if font_type == 'prediction': return (base_font, 11)
        return (base_font, 12)

    def load_translations(self):
        locales_dir = utils.resource_path('locales')
        if not os.path.isdir(locales_dir):
            messagebox.showerror("Fatal Error", f"Could not find the 'locales' directory.")
            self.root.destroy()
            return
        for filename in os.listdir(locales_dir):
            if filename.endswith('.json'):
                lang_code = filename.split('.')[0]
                try:
                    with open(os.path.join(locales_dir, filename), 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

    def load_model_thread(self):
        if core.load_model():
            self.root.after(0, self.on_model_loaded)
        else:
            self.root.after(0, lambda: messagebox.showerror("Model Error", "Failed to load model."))
    
    def on_model_loaded(self):
        self.upload_button.config(state=tk.NORMAL)
        self.update_ui_text()

    def create_clickable_predictions(self, predictions_data):
        for widget in self.results_frame.winfo_children(): widget.destroy()
        lang = self.current_lang.get(); trans = self.translations.get(lang, {})
        self.result_title_label.config(text=trans.get('result_title', 'AI Results:'))
        for _, label, score in predictions_data:
            label_name = label.replace('_', ' ').capitalize()
            display_text = f"{label_name} ({score:.1%})"
            btn = tk.Button(self.results_frame, text=display_text, relief='flat', command=lambda l=label_name: self.search_wikipedia(l))
            btn.pack(fill=tk.X, pady=2)
        self.apply_theme()

    def manual_search(self):
        query = self.search_entry.get()
        if query: self.search_wikipedia(query)

    def search_wikipedia(self, query):
        self.search_entry.delete(0, tk.END); self.search_entry.insert(0, query)
        lang = self.current_lang.get(); trans = self.translations.get(lang, {})
        self.show_popup(trans.get('wiki_search_title', 'Search'), trans.get('searching', 'Searching...'))
        threading.Thread(target=self.fetch_wiki_summary_thread, args=(query,), daemon=True).start()

    def fetch_wiki_summary_thread(self, query):
        lang_code = self.current_lang.get().split('-')[0]
        title, summary = core.fetch_wiki_summary(query, lang_code)
        lang = self.current_lang.get(); trans = self.translations.get(lang, {})
        if summary:
            self.root.after(0, self.show_popup, title, summary)
        else:
            self.root.after(0, self.show_popup, trans.get('wiki_search_title', 'Search'), trans.get('page_not_found', 'Page not found.'))

    def show_popup(self, title, content):
        if not hasattr(self, 'popup') or not self.popup.winfo_exists():
            self.popup = tk.Toplevel(self.root)
            self.popup_text = tk.Text(self.popup, wrap=tk.WORD, padx=15, pady=15)
            self.popup_text.pack(expand=True, fill=tk.BOTH)
        self.popup.title(title)
        self.popup_text.config(state=tk.NORMAL, font=self.get_font())
        self.popup_text.delete(1.0, tk.END); self.popup_text.insert(tk.END, content)
        self.popup_text.config(state=tk.DISABLED)
        mode = self.theme_mode.get(); colors = self.themes[mode]
        self.popup.configure(bg=colors['BG']); self.popup_text.configure(bg=colors['FRAME_BG'], fg=colors['TEXT'])
        self.popup.deiconify(); self.popup.lift()

    def upload_and_predict(self):
        lang = self.current_lang.get(); trans = self.translations.get(lang, {})
        filetypes = [(trans.get('file_types_images', 'Images'), '*.jpg *.jpeg *.png *.bmp *.gif *.webp'), (trans.get('file_types_videos', 'Videos'), '*.mp4 *.avi *.mov *.mkv'), (trans.get('file_types_all', 'All'), '*.*')]
        file_path = filedialog.askopenfilename(title=trans.get('file_dialog_title', 'Select File'), filetypes=filetypes)
        if not file_path: return
        try:
            pil_image = self.get_pil_image_from_file(file_path)
            if pil_image:
                self.display_pil_image(pil_image)
                processed_image = core.preprocess_image(pil_image)
                predictions = core.predict(processed_image)
                if predictions is not None:
                    self.last_prediction = predictions
                    self.create_clickable_predictions(predictions)
                    first_prediction_label = predictions[0][1].replace('_', ' ').capitalize()
                    self.search_wikipedia(first_prediction_label)
            else: raise ValueError("Unsupported file format or unable to read file.")
        except Exception as e: messagebox.showerror(trans.get('error_message', 'Error'), str(e))

    def apply_theme(self):
        mode = self.theme_mode.get(); colors = self.themes[mode]
        self.root.configure(bg=colors['BG'])
        self.main_frame.configure(bg=colors['BG']); self.top_frame.configure(bg=colors['BG'])
        self.results_frame.configure(bg=colors['BG']); self.search_frame.configure(bg=colors['BG'])
        self.title_label.config(bg=colors['BG'], fg=colors['TEXT'], font=self.get_font('title'))
        self.result_title_label.config(bg=colors['BG'], fg=colors['TEXT'], font=self.get_font())
        self.search_entry.config(bg=colors['FRAME_BG'], fg=colors['TEXT'], insertbackground=colors['TEXT'], relief='flat', font=self.get_font())
        self.upload_button.config(bg=colors['ACCENT'], fg=colors['BUTTON_TEXT'], activebackground=self.themes['dark' if mode == 'light' else 'light']['ACCENT'], activeforeground=colors['BUTTON_TEXT'], font=self.get_font('button'))
        self.search_button.config(bg=colors['SECONDARY_BG'], fg=colors['TEXT'], activebackground=colors['ACCENT'], activeforeground=colors['BUTTON_TEXT'], font=self.get_font('button'))
        self.image_canvas.delete("all"); self.image_canvas.create_rounded_rectangle(0, 0, 450, 350, radius=20, fill=colors['FRAME_BG'])
        if hasattr(self, 'photo'): self.image_canvas.create_image(225, 175, image=self.photo)
        style = ttk.Style(); style.configure("TCombobox", fieldbackground=colors['FRAME_BG'], background=colors['FRAME_BG'], foreground=colors['TEXT'], arrowcolor=colors['TEXT']); style.configure("Switch.TCheckbutton", background=colors['BG'])
        self.theme_switch.config(text="☀️" if mode == 'dark' else "🌙")
        for child in self.results_frame.winfo_children():
            if isinstance(child, tk.Button):
                child.config(bg=colors['SECONDARY_BG'], fg=colors['TEXT'], activebackground=colors['ACCENT'], activeforeground=colors['BUTTON_TEXT'], font=self.get_font('prediction'))

    def toggle_theme(self): self.theme_mode.set('dark' if self.theme_mode.get() == 'light' else 'light'); self.apply_theme()
    
    def update_ui_text(self):
        lang = self.current_lang.get(); trans = self.translations.get(lang, {})
        self.root.title(trans.get('window_title', 'Identifier'))
        self.title_label.config(text=trans.get('main_title', 'Analysis'))
        if core.model is None: self.result_title_label.config(text=trans.get('loading_model', 'Loading...'))
        else: self.result_title_label.config(text=trans.get('result_placeholder', 'Results here'))
        self.upload_button.config(text=trans.get('select_button', 'Select')); self.search_button.config(text=trans.get('search_button', 'Search'))
    
    def change_language(self, event=None):
        self.apply_theme(); self.update_ui_text()
        if hasattr(self, 'last_prediction'): self.create_clickable_predictions(self.last_prediction)
    
    def get_pil_image_from_file(self, file_path):
        file_ext = os.path.splitext(file_path)[1].lower()
        image_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']; video_exts = ['.mp4', '.avi', '.mov', '.mkv']
        if any(file_ext.endswith(ext) for ext in image_exts): return Image.open(file_path).convert('RGB')
        elif any(file_ext.endswith(ext) for ext in video_exts):
            cap = cv2.VideoCapture(file_path); cap.set(cv2.CAP_PROP_POS_MSEC, 1000); success, frame = cap.read(); cap.release()
            if success: return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return None
    
    def display_pil_image(self, pil_img):
        pil_img.thumbnail((430, 330)); rounded_img = utils.round_corners(pil_img, 18); self.photo = ImageTk.PhotoImage(rounded_img); self.apply_theme()

def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius,y1, x1+radius,y1, x2-radius,y1, x2-radius,y1, x2,y1, x2,y1+radius, x2,y1+radius, x2,y2-radius, x2,y2-radius, x2,y2, x2-radius,y2, x2-radius,y2, x1+radius,y2, x1+radius,y2, x1,y2, x1,y2-radius, x1,y2-radius, x1,y1+radius, x1,y1+radius, x1,y1]
    return self.create_polygon(points, **kwargs, smooth=True)
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalIdentifierApp(root)
    root.mainloop()
