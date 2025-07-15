# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import os
import cv2
import threading # 引入 threading 函式庫

# --- 延遲引入 TensorFlow，避免啟動時卡頓 ---
tf = None

# --- 輔助函數：為圖片加上圓角 ---
def round_corners(pil_image, radius):
    """為 PIL Image 物件加上圓角"""
    mask = Image.new('L', pil_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + pil_image.size, radius, fill=255)
    output = pil_image.copy()
    output.putalpha(mask)
    return output

# --- 圖片預處理函數 (與之前相同) ---
def preprocess_pil_image(pil_img):
    img_resized = pil_img.resize((224, 224))
    img_array = np.array(img_resized)
    if img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]
    img_array_expanded = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet_v2.preprocess_input(img_array_expanded)

# --- 4. 圖形化使用者介面 (GUI) - 精緻 Apple 風格 ---
class AnimalIdentifierApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("550x680")
        self.model = None # 模型初始為 None

        # --- 主題與顏色管理 ---
        self.theme_mode = tk.StringVar(value='light')
        self.themes = {
            'light': { 'BG': "#f0f0f0", 'TEXT': "#000000", 'ACCENT': "#007aff", 'FRAME_BG': "#ffffff", 'FRAME_BORDER': "#dcdcdc", 'BUTTON_TEXT': "#ffffff" },
            'dark': { 'BG': "#1e1e1e", 'TEXT': "#e0e0e0", 'ACCENT': "#0a84ff", 'FRAME_BG': "#2c2c2e", 'FRAME_BORDER': "#404040", 'BUTTON_TEXT': "#ffffff" }
        }

        # --- 多語言翻譯字典 ---
        self.translations = {
            'zh-tw': {
                'window_title': "動物識別器", 'main_title': "圖片或影片分析", 'result_placeholder': "辨識結果將會顯示在這裡",
                'select_button': "選擇檔案", 'result_title': "分析結果：", 'prediction_prefix': "可能是:",
                'confidence': "信心度", 'error_message': "發生錯誤：", 'file_dialog_title': "選擇一個檔案",
                'file_types_images': "圖片檔案", 'file_types_videos': "影片檔案", 'file_types_all': "所有支援的檔案",
                'loading_model': "模型載入中，請稍候..."
            },
            'en': {
                'window_title': "Animal Identifier", 'main_title': "Image or Video Analysis", 'result_placeholder': "Prediction will be shown here",
                'select_button': "Select File", 'result_title': "Analysis Result:", 'prediction_prefix': "Might be:",
                'confidence': "Confidence", 'error_message': "An error occurred:", 'file_dialog_title': "Select a file",
                'file_types_images': "Image Files", 'file_types_videos': "Video Files", 'file_types_all': "All Supported Files",
                'loading_model': "Loading model, please wait..."
            }
        }
        self.current_lang = tk.StringVar(value='zh-tw')

        # --- 字體管理 (已縮小字體) ---
        self.FONT_TITLE = ("Segoe UI", 22, "bold")
        self.FONT_BODY = ("Segoe UI", 12)
        self.FONT_BODY_CH = ("微軟正黑體", 12)
        self.FONT_BUTTON = ("Segoe UI", 12, "bold")
        self.FONT_BUTTON_CH = ("微軟正黑體", 12, "bold")

        # --- 介面佈局 ---
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.X, pady=(0, 20))
        self.lang_combo = ttk.Combobox(self.top_frame, textvariable=self.current_lang, values=['zh-tw', 'en'], state='readonly', width=8)
        self.lang_combo.pack(side=tk.RIGHT, padx=(10, 0))
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)
        self.theme_switch = ttk.Checkbutton(self.top_frame, text="🌙", style="Switch.TCheckbutton", command=self.toggle_theme)
        self.theme_switch.pack(side=tk.RIGHT)
        self.title_label = tk.Label(self.main_frame, font=self.FONT_TITLE)
        self.title_label.pack(pady=(0, 25), anchor='w')
        self.image_canvas = tk.Canvas(self.main_frame, width=450, height=350, highlightthickness=0)
        self.image_canvas.pack(pady=10)
        self.result_label = tk.Label(self.main_frame, font=self.FONT_BODY_CH, wraplength=450, justify='center')
        self.result_label.pack(pady=(15, 15))
        self.upload_button = tk.Button(self.main_frame, font=self.FONT_BUTTON_CH, relief='flat', borderwidth=0, command=self.upload_and_predict)
        self.upload_button.pack(pady=(10, 20), ipady=10, fill=tk.X)

        # --- 初始化 ---
        self.apply_theme()
        self.update_ui_text()
        
        # --- 在背景載入模型 ---
        self.upload_button.config(state=tk.DISABLED) # 禁用按鈕
        threading.Thread(target=self.load_model_thread, daemon=True).start()

    def load_model_thread(self):
        """在背景執行緒中載入模型"""
        global tf
        import tensorflow
        tf = tensorflow
        
        try:
            self.model = tf.keras.applications.MobileNetV2(weights="imagenet")
            # 模型載入成功後，通知主執行緒更新 UI
            self.root.after(0, self.on_model_loaded)
        except Exception as e:
            print(f"無法下載或載入模型: {e}")
            # 可以在此處更新 UI 顯示錯誤訊息
            self.root.after(0, lambda: self.result_label.config(text=f"模型載入失敗:\n{e}"))

    def on_model_loaded(self):
        """模型載入完成後，在主執行緒中更新 UI"""
        self.upload_button.config(state=tk.NORMAL) # 啟用按鈕
        self.update_ui_text() # 恢復正常的提示文字

    def predict(self, processed_image):
        """使用已載入的模型進行預測"""
        if self.model:
            predictions = self.model.predict(processed_image)
            return tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
        return None

    def apply_theme(self):
        mode = self.theme_mode.get()
        colors = self.themes[mode]
        self.root.configure(bg=colors['BG'])
        self.main_frame.configure(bg=colors['BG'])
        self.top_frame.configure(bg=colors['BG'])
        self.title_label.config(bg=colors['BG'], fg=colors['TEXT'])
        self.result_label.config(bg=colors['BG'], fg=colors['TEXT'])
        self.upload_button.config(bg=colors['ACCENT'], fg=colors['BUTTON_TEXT'], activebackground=self.themes['dark' if mode == 'light' else 'light']['ACCENT'], activeforeground=colors['BUTTON_TEXT'])
        self.image_canvas.delete("all")
        self.image_canvas.create_rounded_rectangle(0, 0, 450, 350, radius=20, fill=colors['FRAME_BG'])
        if hasattr(self, 'photo'):
             self.image_canvas.create_image(225, 175, image=self.photo)
        style = ttk.Style()
        style.configure("TCombobox", fieldbackground=colors['FRAME_BG'], background=colors['FRAME_BG'], foreground=colors['TEXT'], arrowcolor=colors['TEXT'])
        style.configure("Switch.TCheckbutton", background=colors['BG'])
        self.theme_switch.config(text="☀️" if mode == 'dark' else "🌙")

    def toggle_theme(self):
        self.theme_mode.set('dark' if self.theme_mode.get() == 'light' else 'light')
        self.apply_theme()

    def update_ui_text(self):
        lang = self.current_lang.get()
        trans = self.translations[lang]
        self.root.title(trans['window_title'])
        self.title_label.config(text=trans['main_title'])
        # 根據模型是否載入完成來決定顯示的文字
        if self.model is None:
            self.result_label.config(text=trans['loading_model'])
        elif self.result_label.cget("text") in [self.translations['zh-tw']['result_placeholder'], self.translations['en']['result_placeholder'], self.translations['zh-tw']['loading_model'], self.translations['en']['loading_model']]:
            self.result_label.config(text=trans['result_placeholder'])
        self.upload_button.config(text=trans['select_button'])

    def change_language(self, event=None):
        self.update_ui_text()
        if hasattr(self, 'last_prediction'):
            self.format_and_display_prediction(self.last_prediction)

    def upload_and_predict(self):
        lang = self.current_lang.get()
        trans = self.translations[lang]
        image_formats = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.webp')
        video_formats = ('*.mp4', '*.avi', '*.mov', '*.mkv')
        filetypes = [(trans['file_types_images'], ' '.join(image_formats)), (trans['file_types_videos'], ' '.join(video_formats)), (trans['file_types_all'], ' '.join(image_formats) + ' ' + ' '.join(video_formats))]
        file_path = filedialog.askopenfilename(title=trans['file_dialog_title'], filetypes=filetypes)
        if not file_path: return

        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            pil_image = None
            image_exts = [ext.replace('*', '') for ext in image_formats]
            video_exts = [ext.replace('*', '') for ext in video_formats]
            if any(file_ext.endswith(ext) for ext in image_exts):
                pil_image = Image.open(file_path).convert('RGB')
            elif any(file_ext.endswith(ext) for ext in video_exts):
                cap = cv2.VideoCapture(file_path)
                cap.set(cv2.CAP_PROP_POS_MSEC, 1000)
                success, frame = cap.read()
                cap.release()
                if success: pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            if pil_image:
                self.display_pil_image(pil_image)
                processed_image = preprocess_pil_image(pil_image)
                predictions = self.predict(processed_image)
                if predictions:
                    self.last_prediction = predictions
                    self.format_and_display_prediction(predictions)
            else: raise ValueError("Unsupported file format or unable to read file")
        except Exception as e:
            self.result_label.config(text=f"{trans['error_message']}\n{e}")

    def format_and_display_prediction(self, predictions):
        lang = self.current_lang.get()
        trans = self.translations[lang]
        result_text = f"{trans['result_title']}\n"
        for _, label, score in predictions:
            label_name = label.replace('_', ' ').capitalize()
            result_text += f"{trans['prediction_prefix']} {label_name} ({trans['confidence']}: {score:.2%})\n"
        self.result_label.config(text=result_text.strip())

    def display_pil_image(self, pil_img):
        pil_img.thumbnail((430, 330))
        rounded_img = round_corners(pil_img, 18)
        self.photo = ImageTk.PhotoImage(rounded_img)
        self.apply_theme()

# --- 輔助函數：在 Canvas 上繪製圓角矩形 ---
def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius, x2, y1 + radius, x2, y2 - radius, x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2, x1 + radius, y2, x1 + radius, y2, x1, y2, x1, y2 - radius, x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1]
    return self.create_polygon(points, **kwargs, smooth=True)
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle

# --- 5. 啟動應用程式 ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalIdentifierApp(root)
    root.mainloop()
