# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import wikipediaapi

# --- 全域變數來存放模型 ---
model = None

def load_model():
    """載入 MobileNetV2 模型"""
    global model
    try:
        model = tf.keras.applications.MobileNetV2(weights="imagenet")
        return True
    except Exception as e:
        print(f"模型載入失敗: {e}")
        return False

def preprocess_image(pil_img):
    """預處理圖片以符合模型輸入"""
    img_resized = pil_img.resize((224, 224))
    img_array = np.array(img_resized)
    if img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]
    img_array_expanded = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet_v2.preprocess_input(img_array_expanded)

def predict(processed_image):
    """使用已載入的模型進行預測"""
    if model:
        predictions = model.predict(processed_image, verbose=0)
        return tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
    return None

def fetch_wiki_summary(query, lang_code):
    """獲取維基百科摘要"""
    try:
        wiki_api = wikipediaapi.Wikipedia(
            user_agent='FaunaLens/1.2.1 (A student project)',
            language=lang_code,
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )
        page = wiki_api.page(query)
        if page.exists():
            return page.title, page.summary
    except Exception as e:
        print(f"維基百科搜尋失敗: {e}")
    return None, None
