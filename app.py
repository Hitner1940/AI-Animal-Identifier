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

# =================================================================================
#  v2.2 新增：自訂圓角按鈕 (Custom Rounded Button)
# =================================================================================
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, theme, font, type='primary'):
        self.theme = theme
        self.command = command
        self.text = text
        self.font = font
        self.type = type
        
        self.update_colors() # 初始化顏色
            
        super().__init__(parent, height=50, highlightthickness=0, bg=self.theme['secondarySystemBackground'])
        
        self.tag_id = self.create_rounded_rectangle(0, 0, self.winfo_width(), 50, radius=25, fill=self.bg_color)
        self.text_id = self.create_text(0, 0, text=self.text, font=self.font, fill=self.theme['buttonText'])
        
        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def update_colors(self):
        """根據按鈕類型選擇顏色"""
        if self.type == 'primary':
            self.bg_color = self.theme['systemGreen']
            self.active_bg_color = self.theme['systemGreen_dark']
        else: # secondary (e.g., Clear button)
            self.bg_color = self.theme['systemRed']
            self.active_bg_color = self.theme['systemRed_dark']

    def update_theme(self, new_theme):
        """接收新的主題並更新自身外觀"""
        self.theme = new_theme
        self.update_colors()
        self.config(bg=self.theme['secondarySystemBackground'])
        self.itemconfig(self.tag_id, fill=self.bg_color)
        self.itemconfig(self.text_id, fill=self.theme['buttonText'])


    def on_resize(self, event):
        self.delete(self.tag_id)
        self.tag_id = self.create_rounded_rectangle(0, 0, event.width, event.height, radius=25, fill=self.bg_color)
        self.coords(self.text_id, event.width / 2, event.height / 2)
        self.tag_raise(self.text_id)

    def on_press(self, event):
        self.itemconfig(self.tag_id, fill=self.active_bg_color)

    def on_release(self, event):
        self.itemconfig(self.tag_id, fill=self.bg_color)
        if self.command:
            self.command()
            
    def set_text(self, text):
        self.itemconfig(self.text_id, text=text)

    def set_state(self, state):
        if state == tk.DISABLED:
            self.itemconfig(self.tag_id, fill=self.theme['tertiarySystemBackground'])
            self.itemconfig(self.text_id, fill=self.theme['secondaryLabel'])
            self.unbind("<Button-1>")
            self.unbind("<ButtonRelease-1>")
        else: # tk.NORMAL
            self.itemconfig(self.tag_id, fill=self.bg_color)
            self.itemconfig(self.text_id, fill=self.theme['buttonText'])
            self.bind("<Button-1>", self.on_press)
            self.bind("<ButtonRelease-1>", self.on_release)

# =================================================================================
#  v2.1: 自訂 UI 元件 (HIG-Compliant)
# =================================================================================
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
    def bind_all_children(self, event, callback):
        self.bind(event, callback)
        for child in self.winfo_children(): child.bind(event, callback)
    def on_enter(self, event):
        self.config(bg=self.theme['tertiarySystemBackground'])
        for child in self.winfo_children():
            if not isinstance(child, ttk.Progressbar): child.config(bg=self.theme['tertiarySystemBackground'])
    def on_leave(self, event):
        self.config(bg=self.theme['secondarySystemBackground'])
        for child in self.winfo_children():
            if not isinstance(child, ttk.Progressbar): child.config(bg=self.theme['secondarySystemBackground'])

# =================================================================================
#  主應用程式 Class (v2.2 - Rounded UI)
# =================================================================================
class AnimalIdentifierApp:
    def __init__(self, root):
        self.root = root; self.root.geometry("550x820"); self.translations = {}; self.load_translations()

        # --- v2.2: HIG 色彩系統 (新增按鈕深色) ---
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

        self.root.configure(bg=self.themes[self.theme_mode.get()]['systemBackground'])
        self.root.grid_rowconfigure(0, weight=1); self.root.grid_columnconfigure(0, weight=1)

        self.main_frame = tk.Frame(root); self.main_frame.grid(row=0, column=0, sticky='nsew', padx=30, pady=30)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.top_frame = tk.Frame(self.main_frame); self.top_frame.pack(fill=tk.X, pady=(10, 15))
        lang_options = sorted(list(self.translations.keys()))
        self.lang_combo = ttk.Combobox(self.top_frame, textvariable=self.current_lang, values=lang_options, state='readonly', width=8)
        self.lang_combo.pack(side=tk.RIGHT, padx=(10, 0)); self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)
        self.theme_switch = ttk.Checkbutton(self.top_frame, text="🌙", style="Switch.TCheckbutton", command=self.toggle_theme)
        self.theme_switch.pack(side=tk.RIGHT)
        
        self.title_label = tk.Label(self.main_frame); self.title_label.pack(pady=(0, 20), anchor='w')
        self.image_canvas = tk.Canvas(self.main_frame, width=450, height=350, highlightthickness=0);
        self.results_header_frame = tk.Frame(self.main_frame)
        self.thumbnail_canvas = tk.Canvas(self.results_header_frame, width=60, height=60, highlightthickness=0)
        self.thumbnail_canvas.pack(side=tk.LEFT, padx=(0, 10))
        self.result_title_label = tk.Label(self.results_header_frame); self.result_title_label.pack(side=tk.LEFT, anchor='w')
        self.results_frame = tk.Frame(self.main_frame)
        self.search_frame = tk.Frame(self.main_frame); self.search_frame.pack(fill=tk.X, pady=(10, 10))
        self.search_bg_canvas = tk.Canvas(self.search_frame, height=40, highlightthickness=0)
        self.search_bg_canvas.pack(fill=tk.X, expand=True)
        self.search_entry = tk.Entry(self.search_bg_canvas, relief='flat'); 
        self.search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15)
        
        self.button_container = tk.Frame(self.main_frame); self.button_container.pack(fill=tk.X, pady=(15, 10))
        self.button_container.grid_columnconfigure(0, weight=1); self.button_container.grid_columnconfigure(1, weight=1)

        theme = self.themes[self.theme_mode.get()]
        font = self.get_font('button')
        self.clear_button = RoundedButton(self.button_container, "", self.reset_to_initial_view, theme, font, type='secondary')
        self.clear_button.grid(row=0, column=0, sticky='ew', padx=(0, 5))
        self.upload_button = RoundedButton(self.button_container, "", self.upload_and_predict, theme, font, type='primary')
        self.upload_button.grid(row=0, column=1, sticky='ew', padx=(5, 0))

        self.reset_to_initial_view(); self.apply_theme(); self.update_ui_text()
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
        self.upload_button.set_state(tk.NORMAL); self.update_ui_text()

    def apply_theme(self):
        mode = self.theme_mode.get(); colors = self.themes[mode]
        self.root.configure(bg=colors['systemBackground'])
        self.main_frame.configure(bg=colors['secondarySystemBackground'])
        self.top_frame.configure(bg=colors['secondarySystemBackground'])
        self.results_frame.configure(bg=colors['secondarySystemBackground'])
        self.search_frame.configure(bg=colors['secondarySystemBackground'])
        self.results_header_frame.configure(bg=colors['secondarySystemBackground'])
        self.thumbnail_canvas.configure(bg=colors['secondarySystemBackground'])
        self.button_container.configure(bg=colors['secondarySystemBackground'])
        
        self.title_label.config(bg=colors['secondarySystemBackground'], fg=colors['label'], font=self.get_font('title'))
        self.result_title_label.config(bg=colors['secondarySystemBackground'], fg=colors['label'], font=self.get_font('result_title'))
        self.search_entry.config(bg=colors['tertiarySystemBackground'], fg=colors['label'], insertbackground=colors['label'])
        
        self.clear_button.update_theme(colors)
        self.upload_button.update_theme(colors)
        
        self.image_canvas.delete("all"); self.image_canvas.create_rounded_rectangle(0, 0, 450, 350, radius=20, fill=colors['tertiarySystemBackground'])
        if hasattr(self, 'photo'): self.image_canvas.create_image(225, 175, image=self.photo)
        
        style = ttk.Style()
        style.configure("TCombobox", fieldbackground=colors['secondarySystemBackground'], foreground=colors['label'], arrowcolor=colors['label'])
        style.configure("Switch.TCheckbutton", background=colors['secondarySystemBackground'])
        self.theme_switch.config(text="☀️" if mode == 'dark' else "🌙")

        self.search_bg_canvas.config(bg=colors['secondarySystemBackground']); self.search_bg_canvas.delete('all')
        self.search_bg_canvas.create_rounded_rectangle(0, 0, self.search_bg_canvas.winfo_width(), 40, radius=20, fill=colors['tertiarySystemBackground'])
        self.search_entry.place(in_=self.search_bg_canvas, relx=0, rely=0, relwidth=1, relheight=1)

    def reset_to_initial_view(self):
        self.results_header_frame.pack_forget(); self.results_frame.pack_forget()
        self.image_canvas.pack(pady=10); self.last_prediction = None
        self.update_ui_text()
    def show_results_view(self, pil_image):
        self.image_canvas.pack_forget()
        self.results_header_frame.pack(fill=tk.X, pady=(25, 10), anchor='w')
        self.display_thumbnail(pil_image)
        self.results_frame.pack(fill=tk.X, pady=(0, 20))
    def display_thumbnail(self, pil_image):
        thumb_img = pil_image.copy(); thumb_img.thumbnail((60, 60))
        rounded_thumb = utils.round_corners(thumb_img, 10)
        self.thumbnail_photo = ImageTk.PhotoImage(rounded_thumb)
        self.thumbnail_canvas.delete("all"); self.thumbnail_canvas.create_image(0, 0, image=self.thumbnail_photo, anchor='nw')
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
        for widget in self.results_frame.winfo_children(): widget.destroy()
        lang = self.current_lang.get(); trans = self.translations.get(lang, {})
        self.result_title_label.config(text=trans.get('result_title', 'AI Results:'))
        theme = self.themes[self.theme_mode.get()]; font = self.get_font('result_row')
        for _, label, score in predictions_data:
            label_name = label.replace('_', ' ').capitalize(); result_data = (label_name, score)
            row = ResultRow(self.results_frame, theme, font, result_data, self.search_wikipedia)
            row.pack(fill=tk.X, pady=2)
    def manual_search(self): query = self.search_entry.get(); self.search_wikipedia(query) if query else None
    def search_wikipedia(self, query):
        self.search_entry.delete(0, tk.END); self.search_entry.insert(0, query)
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
        self.root.title(trans.get('window_title', 'Identifier')); self.title_label.config(text=trans.get('main_title', 'Analysis'))
        if core.classification_model is None: self.result_title_label.config(text=trans.get('loading_model', 'Loading...'))
        elif self.last_prediction is None: self.result_title_label.config(text=trans.get('result_placeholder', 'Results here'))
        self.upload_button.set_text(trans.get('select_button', 'Select')); self.clear_button.set_text(trans.get('clear_button', 'Clear'))
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
        self.photo = ImageTk.PhotoImage(rounded_img); self.image_canvas.delete("all")
        self.image_canvas.create_rounded_rectangle(0, 0, 450, 350, radius=20, fill=self.themes[self.theme_mode.get()]['tertiarySystemBackground'])
        self.image_canvas.create_image(225, 175, image=self.photo)

def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius,y1, x1+radius,y1, x2-radius,y1, x2-radius,y1, x2,y1, x2,y1+radius, x2,y1+radius, x2,y2-radius, x2,y2-radius, x2,y2, x2-radius,y2, x2-radius,y2, x1+radius,y2, x1+radius,y2, x1,y2, x1,y2-radius, x1,y2-radius, x1,y1+radius, x1,y1+radius, x1,y1]
    return self.create_polygon(points, **kwargs, smooth=True)
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalIdentifierApp(root)
    root.mainloop()