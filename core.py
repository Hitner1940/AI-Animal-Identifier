# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import wikipediaapi

# --- 全域變數來存放模型 ---
# THIS IS THE CRITICAL LINE THAT WAS MISSING OR INCORRECT.
# We define the variable at the module level so other files can see it.
classification_model = None

def load_classification_model():
    """載入 Keras MobileNetV2 分類模型"""
    global classification_model
    try:
        # This model is loaded directly from Keras, it's more reliable.
        classification_model = tf.keras.applications.MobileNetV2(weights="imagenet")
        return True
    except Exception as e:
        print(f"分類模型載入失敗: {e}")
        return False

def preprocess_image(pil_img):
    """預處理圖片以符合模型輸入"""
    img_resized = pil_img.resize((224, 224))
    img_array = np.array(img_resized)
    if img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]
    img_array_expanded = np.expand_dims(img_array, axis=0)
    # Use the correct preprocessing function for this model
    return tf.keras.applications.mobilenet_v2.preprocess_input(img_array_expanded)

def predict_classification(processed_image):
    """使用已載入的分類模型進行預測"""
    if classification_model:
        predictions = classification_model.predict(processed_image, verbose=0)
        return tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
    return None

def fetch_wiki_summary(query, lang_code):
    """獲取維基百科摘要"""
    try:
        wiki_api = wikipediaapi.Wikipedia(
            user_agent='FaunaLens/1.2.2', # Updated version
            language=lang_code,
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )
        page = wiki_api.page(query)
        if page.exists():
            return page.title, page.summary
    except Exception as e:
        print(f"維基百科搜尋失敗: {e}")
    return None, None