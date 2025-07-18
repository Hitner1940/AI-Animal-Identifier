# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import os
import cv2
import threading
import wikipediaapi

# --- 延遲引入 TensorFlow，避免啟動時卡頓 ---
# We'll import TensorFlow inside a thread to keep the UI responsive.
tf = None

# --- 輔助函數：為圖片加上圓角 ---
# Helper function to add rounded corners to a PIL Image object.
def round_corners(pil_image, radius):
    mask = Image.new('L', pil_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + pil_image.size, radius, fill=255)
    output = pil_image.copy()
    output.putalpha(mask)
    return output

# --- 圖片預處理函數 ---
# Preprocesses the image to the format required by the MobileNetV2 model.
def preprocess_pil_image(pil_img):
    img_resized = pil_img.resize((224, 224))
    img_array = np.array(img_resized)
    # Remove alpha channel if it exists (e.g., in PNGs)
    if img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]
    # Expand dimensions to create a batch of 1
    img_array_expanded = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet_v2.preprocess_input(img_array_expanded)

# --- 主應用程式 Class ---
# This class encapsulates the entire application.
class AnimalIdentifierApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("550x750") # 增加高度以容納搜尋框
        self.model = None # 模型初始為 None

        # --- 主題與顏色管理 (Theme and Color Management) ---
        self.theme_mode = tk.StringVar(value='light')
        self.themes = {
            'light': { 'BG': "#f0f0f0", 'TEXT': "#000000", 'ACCENT': "#007aff", 'FRAME_BG': "#ffffff", 'FRAME_BORDER': "#dcdcdc", 'BUTTON_TEXT': "#ffffff", 'SECONDARY_BG': "#e5e5ea" },
            'dark': { 'BG': "#1e1e1e", 'TEXT': "#e0e0e0", 'ACCENT': "#0a84ff", 'FRAME_BG': "#2c2c2e", 'FRAME_BORDER': "#404040", 'BUTTON_TEXT': "#ffffff", 'SECONDARY_BG': "#3a3a3c" }
        }

        # --- 多語言翻譯字典 (Multi-language Dictionary) ---
        self.translations = {
            'zh-tw': {
                'window_title': "動物識別器", 'main_title': "圖片或影片分析", 'result_placeholder': "辨識結果將會顯示在這裡",
                'select_button': "選擇檔案", 'result_title': "AI 分析結果 (點擊可搜尋):", 'prediction_prefix': "可能是:",
                'confidence': "信心度", 'error_message': "發生錯誤：", 'file_dialog_title': "選擇一個檔案",
                'file_types_images': "圖片檔案", 'file_types_videos': "影片檔案", 'file_types_all': "所有支援的檔案",
                'loading_model': "模型載入中，請稍候...", 'search_button': "搜尋維基百科", 'wiki_search_title': "維基百科搜尋結果",
                'page_not_found': "找不到相關的維基百科頁面。", 'searching': "搜尋中..."
            },
            'en': {
                'window_title': "Animal Identifier", 'main_title': "Image or Video Analysis", 'result_placeholder': "Prediction will be shown here",
                'select_button': "Select File", 'result_title': "AI Analysis (Click to search):", 'prediction_prefix': "Might be:",
                'confidence': "Confidence", 'error_message': "An error occurred:", 'file_dialog_title': "Select a file",
                'file_types_images': "Image Files", 'file_types_videos': "Video Files", 'file_types_all': "All Supported Files",
                'loading_model': "Loading model, please wait...", 'search_button': "Search Wikipedia", 'wiki_search_title': "Wikipedia Search Result",
                'page_not_found': "Could not find a matching Wikipedia page.", 'searching': "Searching..."
            }
        }
        self.current_lang = tk.StringVar(value='zh-tw')

        # --- 字體管理 (Font Management) ---
        self.FONT_TITLE = ("Segoe UI", 22, "bold")
        self.FONT_BODY_CH = ("微軟正黑體", 12)
        self.FONT_BUTTON_CH = ("微軟正黑體", 12, "bold")
        self.FONT_PREDICTION = ("Segoe UI", 11)

        # --- 介面佈局 (UI Layout) ---
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # 頂部控制列 (Top control bar)
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.X, pady=(0, 20))
        self.lang_combo = ttk.Combobox(self.top_frame, textvariable=self.current_lang, values=['zh-tw', 'en'], state='readonly', width=8)
        self.lang_combo.pack(side=tk.RIGHT, padx=(10, 0))
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)
        self.theme_switch = ttk.Checkbutton(self.top_frame, text="🌙", style="Switch.TCheckbutton", command=self.toggle_theme)
        self.theme_switch.pack(side=tk.RIGHT)
        
        # 標題 (Title)
        self.title_label = tk.Label(self.main_frame, font=self.FONT_TITLE)
        self.title_label.pack(pady=(0, 25), anchor='w')
        
        # 圖片顯示區 (Image display area)
        self.image_canvas = tk.Canvas(self.main_frame, width=450, height=350, highlightthickness=0)
        self.image_canvas.pack(pady=10)

        # 結果顯示區 (Results display area)
        self.result_title_label = tk.Label(self.main_frame, font=self.FONT_BODY_CH)
        self.result_title_label.pack(pady=(15, 5), anchor='w')
        self.results_frame = tk.Frame(self.main_frame)
        self.results_frame.pack(fill=tk.X)

        # 搜尋功能區 (Search area)
        self.search_frame = tk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.X, pady=(20, 10))
        self.search_entry = tk.Entry(self.search_frame, font=self.FONT_BODY_CH)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=5)
        self.search_button = tk.Button(self.search_frame, font=self.FONT_BUTTON_CH, relief='flat', borderwidth=0, command=self.manual_search)
        self.search_button.pack(side=tk.RIGHT, padx=(10, 0), ipady=5)

        # 上傳按鈕 (Upload button)
        self.upload_button = tk.Button(self.main_frame, font=self.FONT_BUTTON_CH, relief='flat', borderwidth=0, command=self.upload_and_predict, state=tk.DISABLED)
        self.upload_button.pack(pady=(10, 0), ipady=10, fill=tk.X)

        # --- 初始化 (Initialization) ---
        self.apply_theme()
        self.update_ui_text()
        threading.Thread(target=self.load_model_thread, daemon=True).start()

    def load_model_thread(self):
        """在背景執行緒中載入模型，避免 UI 卡頓"""
        global tf; import tensorflow; tf = tensorflow
        try:
            self.model = tf.keras.applications.MobileNetV2(weights="imagenet")
            self.root.after(0, self.on_model_loaded)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Model Error", f"Failed to load model: {e}"))
    
    def on_model_loaded(self):
        """模型載入完成後，在主執行緒中更新 UI"""
        self.upload_button.config(state=tk.NORMAL)
        self.update_ui_text()

    def create_clickable_predictions(self, predictions_data):
        """建立可點擊的預測結果按鈕"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        lang = self.current_lang.get()
        trans = self.translations[lang]
        self.result_title_label.config(text=trans['result_title'])

        for _, label, score in predictions_data:
            label_name = label.replace('_', ' ').capitalize()
            display_text = f"{label_name} ({score:.1%})"
            btn = tk.Button(self.results_frame, text=display_text, font=self.FONT_PREDICTION, relief='flat', 
                            command=lambda l=label_name: self.search_wikipedia(l))
            btn.pack(fill=tk.X, pady=2)
        
        self.apply_theme()

    def manual_search(self):
        """手動觸發搜尋"""
        query = self.search_entry.get()
        if query:
            self.search_wikipedia(query)

    def search_wikipedia(self, query):
        """執行維基百科搜尋 (在背景執行緒)"""
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, query)
        
        lang = self.current_lang.get(); trans = self.translations[lang]
        self.show_popup(trans['wiki_search_title'], trans['searching'])
        threading.Thread(target=self.fetch_wiki_summary, args=(query,), daemon=True).start()

    def fetch_wiki_summary(self, query):
        """獲取維基百科摘要"""
        lang_code = self.current_lang.get().split('-')[0]
        wiki_api = wikipediaapi.Wikipedia(
            user_agent='FaunaLens/1.0.2 (A student project)',
            language=lang_code,
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )
        page = wiki_api.page(query)
        
        lang = self.current_lang.get(); trans = self.translations[lang]
        
        if page.exists():
            self.root.after(0, self.show_popup, page.title, page.summary)
        else:
            self.root.after(0, self.show_popup, trans['wiki_search_title'], trans['page_not_found'])

    def show_popup(self, title, content):
        """顯示搜尋結果的彈出視窗"""
        if not hasattr(self, 'popup') or not self.popup.winfo_exists():
            self.popup = tk.Toplevel(self.root)
            self.popup_text = tk.Text(self.popup, wrap=tk.WORD, padx=15, pady=15, font=self.FONT_BODY_CH)
            self.popup_text.pack(expand=True, fill=tk.BOTH)
        
        self.popup.title(title)
        self.popup_text.config(state=tk.NORMAL)
        self.popup_text.delete(1.0, tk.END)
        self.popup_text.insert(tk.END, content)
        self.popup_text.config(state=tk.DISABLED)
        
        mode = self.theme_mode.get(); colors = self.themes[mode]
        self.popup.configure(bg=colors['BG'])
        self.popup_text.configure(bg=colors['FRAME_BG'], fg=colors['TEXT'])
        
        self.popup.deiconify(); self.popup.lift()

    def upload_and_predict(self):
        """處理檔案上傳、預測和結果顯示"""
        lang = self.current_lang.get(); trans = self.translations[lang]
        image_formats = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.webp')
        video_formats = ('*.mp4', '*.avi', '*.mov', '*.mkv')
        filetypes = [(trans['file_types_images'], ' '.join(image_formats)), (trans['file_types_videos'], ' '.join(video_formats)), (trans['file_types_all'], ' '.join(image_formats) + ' ' + ' '.join(video_formats))]
        file_path = filedialog.askopenfilename(title=trans['file_dialog_title'], filetypes=filetypes)
        if not file_path: return

        try:
            pil_image = self.get_pil_image_from_file(file_path)
            if pil_image:
                self.display_pil_image(pil_image)
                processed_image = preprocess_pil_image(pil_image)
                predictions = self.predict(processed_image)
                if predictions is not None:
                    self.last_prediction = predictions
                    self.create_clickable_predictions(predictions)
                    first_prediction_label = predictions[0][1].replace('_', ' ').capitalize()
                    self.search_wikipedia(first_prediction_label)
            else: raise ValueError("Unsupported file format or unable to read file.")
        except Exception as e:
            messagebox.showerror(trans['error_message'], str(e))

    def predict(self, processed_image):
        """使用已載入的模型進行預測"""
        if self.model:
            predictions = self.model.predict(processed_image, verbose=0)
            return tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
        return None

    def apply_theme(self):
        """根據當前選擇的主題更新所有UI元件的顏色和風格"""
        mode = self.theme_mode.get(); colors = self.themes[mode]
        self.root.configure(bg=colors['BG'])
        self.main_frame.configure(bg=colors['BG']); self.top_frame.configure(bg=colors['BG'])
        self.results_frame.configure(bg=colors['BG']); self.search_frame.configure(bg=colors['BG'])
        self.title_label.config(bg=colors['BG'], fg=colors['TEXT']); self.result_title_label.config(bg=colors['BG'], fg=colors['TEXT'])
        self.upload_button.config(bg=colors['ACCENT'], fg=colors['BUTTON_TEXT'], activebackground=self.themes['dark' if mode == 'light' else 'light']['ACCENT'], activeforeground=colors['BUTTON_TEXT'])
        self.search_button.config(bg=colors['SECONDARY_BG'], fg=colors['TEXT'], activebackground=colors['ACCENT'], activeforeground=colors['BUTTON_TEXT'])
        self.search_entry.config(bg=colors['FRAME_BG'], fg=colors['TEXT'], insertbackground=colors['TEXT'], relief='flat')
        self.image_canvas.delete("all"); self.image_canvas.create_rounded_rectangle(0, 0, 450, 350, radius=20, fill=colors['FRAME_BG'])
        if hasattr(self, 'photo'): self.image_canvas.create_image(225, 175, image=self.photo)
        style = ttk.Style(); style.configure("TCombobox", fieldbackground=colors['FRAME_BG'], background=colors['FRAME_BG'], foreground=colors['TEXT'], arrowcolor=colors['TEXT']); style.configure("Switch.TCheckbutton", background=colors['BG'])
        self.theme_switch.config(text="☀️" if mode == 'dark' else "🌙")
        for child in self.results_frame.winfo_children():
            if isinstance(child, tk.Button):
                child.config(bg=colors['SECONDARY_BG'], fg=colors['TEXT'], activebackground=colors['ACCENT'], activeforeground=colors['BUTTON_TEXT'])

    def toggle_theme(self): self.theme_mode.set('dark' if self.theme_mode.get() == 'light' else 'light'); self.apply_theme()
    
    def update_ui_text(self):
        lang = self.current_lang.get(); trans = self.translations[lang]
        self.root.title(trans['window_title']); self.title_label.config(text=trans['main_title'])
        if self.model is None: self.result_title_label.config(text=trans['loading_model'])
        else: self.result_title_label.config(text=trans['result_placeholder'])
        self.upload_button.config(text=trans['select_button']); self.search_button.config(text=trans['search_button'])
    
    def change_language(self, event=None):
        self.update_ui_text()
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
        pil_img.thumbnail((430, 330)); rounded_img = round_corners(pil_img, 18); self.photo = ImageTk.PhotoImage(rounded_img); self.apply_theme()

# --- 輔助函數：在 Canvas 上繪製圓角矩形 ---
def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius,y1, x1+radius,y1, x2-radius,y1, x2-radius,y1, x2,y1, x2,y1+radius, x2,y1+radius, x2,y2-radius, x2,y2-radius, x2,y2, x2-radius,y2, x2-radius,y2, x1+radius,y2, x1+radius,y2, x1,y2, x1,y2-radius, x1,y2-radius, x1,y1+radius, x1,y1+radius, x1,y1]
    return self.create_polygon(points, **kwargs, smooth=True)
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle

# --- 啟動應用程式 ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalIdentifierApp(root)
    root.mainloop()
