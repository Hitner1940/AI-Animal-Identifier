# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import wikipediaapi

# =================================================================================
#  Core Logic
#  This file handles the core business logic, such as loading the model,
#  preprocessing images, running predictions, and interacting with external APIs (like Wikipedia).
# =================================================================================

# --- Global variable to store the model ---
classification_model = None

def load_classification_model():
    """
    Loads the Keras MobileNetV2 classification model.
    This model will be downloaded from TensorFlow Hub if not cached locally.
    """
    global classification_model
    if classification_model:
        return True
    try:
        classification_model = tf.keras.applications.MobileNetV2(weights="imagenet")
        # Perform a "warm-up" prediction to avoid delay on the first real prediction.
        dummy_input = np.zeros((1, 224, 224, 3))
        classification_model.predict(dummy_input, verbose=0)
        print("Classification model loaded successfully.")
        return True
    except Exception as e:
        print(f"Error loading classification model: {e}")
        return False

def preprocess_image(pil_img):
    """
    Preprocesses a PIL Image object to meet the input requirements of MobileNetV2.
    - Resize to 224x224
    - Convert to a NumPy array
    - Expand dimensions to match the batch size
    - Perform model-specific preprocessing (e.g., scaling pixel values to -1 to 1)
    """
    img_resized = pil_img.resize((224, 224))
    img_array = np.array(img_resized)
    # If the image has an Alpha channel (transparency), remove it.
    if img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]
    img_array_expanded = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet_v2.preprocess_input(img_array_expanded)

def predict_classification(processed_image):
    """
    Uses the loaded classification model to make a prediction.
    Returns the top 3 most likely results.
    """
    if classification_model:
        try:
            predictions = classification_model.predict(processed_image, verbose=0)
            # Decode the prediction results to get a list of (id, label, score).
            return tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None
    return None

def fetch_wikipedia_summary(query, lang_code='en'):
    """
    Fetches a page summary from the specified language's Wikipedia.
    """
    try:
        wiki_api = wikipediaapi.Wikipedia(
            user_agent='AnimalIdentifier/1.0 (https://example.com/app)',
            language=lang_code,
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )
        page = wiki_api.page(query)
        if page.exists():
            # Return the page title and summary.
            return page.title, page.summary
    except Exception as e:
        print(f"Wikipedia search failed for query '{query}': {e}")
    # If it fails, return the original query and None.
    return query, None

def get_all_imagenet_labels():
    """
    Gets all 1000 ImageNet class names supported by MobileNetV2.
    """
    try:
        # Generate a dummy prediction distribution to trigger decode_predictions to get all labels.
        dummy_predictions = tf.zeros((1, 1000))
        decoded = tf.keras.applications.mobilenet_v2.decode_predictions(dummy_predictions.numpy(), top=1000)[0]
        # Clean up the label format (replace underscores with spaces, capitalize).
        return sorted([label.replace('_', ' ').capitalize() for (_, label, _) in decoded])
    except Exception as e:
        print(f"Could not retrieve ImageNet labels: {e}")
        return []
