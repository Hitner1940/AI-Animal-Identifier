# -*- mode: python ; coding: utf-8 -*-
import numpy as np
import wikipediaapi

# =================================================================================
#  Core Logic
#  Update: Implemented lazy loading for TensorFlow to speed up initial app launch.
#  The 'tensorflow' import is now inside functions instead of at the top level.
# =================================================================================

# --- Global variable to store the model ---
classification_model = None

def load_classification_model():
    """
    Loads the Keras MobileNetV2 classification model.
    """
    global classification_model
    if classification_model:
        return True
    
    import tensorflow as tf # Lazy import
    
    try:
        classification_model = tf.keras.applications.MobileNetV2(weights="imagenet")
        # Perform a "warm-up" prediction.
        dummy_input = np.zeros((1, 224, 224, 3))
        classification_model.predict(dummy_input, verbose=0)
        print("Classification model loaded successfully.")
        return True
    except Exception as e:
        print(f"Error loading classification model: {e}")
        return False

def preprocess_image(pil_img):
    """
    Preprocesses a PIL Image object for MobileNetV2.
    """
    import tensorflow as tf # Lazy import

    img_resized = pil_img.resize((224, 224))
    img_array = np.array(img_resized)
    if img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]
    img_array_expanded = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet_v2.preprocess_input(img_array_expanded)

def predict_classification(processed_image):
    """
    Uses the loaded model to make a prediction.
    """
    import tensorflow as tf # Lazy import

    if classification_model:
        try:
            predictions = classification_model.predict(processed_image, verbose=0)
            return tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None
    return None

def fetch_wikipedia_summary(query, lang_code='en'):
    """
    Fetches a page summary from Wikipedia.
    """
    try:
        wiki_api = wikipediaapi.Wikipedia(
            user_agent='AnimalIdentifier/1.0 (https://example.com/app)',
            language=lang_code,
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )
        page = wiki_api.page(query)
        if page.exists():
            return page.title, page.summary
    except Exception as e:
        print(f"Wikipedia search failed for query '{query}': {e}")
    return query, None

def get_all_imagenet_labels():
    """
    Gets all 1000 ImageNet class names.
    """
    import tensorflow as tf # Lazy import
    
    try:
        dummy_predictions = tf.zeros((1, 1000))
        decoded = tf.keras.applications.mobilenet_v2.decode_predictions(dummy_predictions.numpy(), top=1000)[0]
        return sorted([label.replace('_', ' ').capitalize() for (_, label, _) in decoded])
    except Exception as e:
        print(f"Could not retrieve ImageNet labels: {e}")
        return []
