# core.py
# -*- coding: utf-8 -*-
"""
Core logic for the FaunaLens application.

This module is responsible for the main "business logic":
- Managing the machine learning model (loading and prediction).
- Interacting with external services (Wikipedia).
"""

import numpy as np
import wikipediaapi
import tensorflow as tf # Import moved to top; lazy loading is now handled by the ModelManager's state.

class ModelManager:
    """
    Manages the loading and execution of the TensorFlow MobileNetV2 model.
    This class encapsulates all machine learning logic.
    """
    def __init__(self):
        """Initializes the ModelManager."""
        self.model = None
        self.labels = []

    def load_model(self):
        """
        Loads the Keras MobileNetV2 model and its labels.
        Uses a "warm-up" prediction to make the first real prediction faster.
        """
        if self.model:
            print("Model is already loaded.")
            return True
        
        try:
            print("Loading classification model...")
            # Load the pre-trained MobileNetV2 model
            self.model = tf.keras.applications.MobileNetV2(weights="imagenet")
            
            # Perform a "warm-up" prediction to reduce latency on the first user call.
            dummy_input = np.zeros((1, 224, 224, 3))
            self.model.predict(dummy_input, verbose=0)
            
            # Load all 1000 ImageNet class names for the search feature
            self._load_imagenet_labels()
            
            print("Classification model and labels loaded successfully.")
            return True
        except Exception as e:
            print(f"FATAL: Error loading classification model: {e}")
            self.model = None
            return False

    def _load_imagenet_labels(self):
        """
        Retrieves all 1000 ImageNet class names by decoding a dummy tensor.
        This is a clever way to get the labels without an external file.
        """
        try:
            dummy_preds = tf.zeros((1, 1000))
            decoded = tf.keras.applications.mobilenet_v2.decode_predictions(dummy_preds.numpy(), top=1000)[0]
            # Format them nicely for display and searching
            self.labels = sorted([label.replace('_', ' ').capitalize() for (_, label, _) in decoded])
        except Exception as e:
            print(f"Could not retrieve ImageNet labels: {e}")
            self.labels = []
            
    def get_labels(self):
        """Returns the list of loaded ImageNet labels."""
        return self.labels

    def preprocess_image(self, pil_image):
        """
        Preprocesses a PIL Image object for MobileNetV2.
        - Resizes to 224x224
        - Converts to numpy array
        - Handles RGBA transparency
        - Applies model-specific preprocessing
        """
        img_resized = pil_image.resize((224, 224))
        img_array = np.array(img_resized)
        
        # Drop the alpha channel if the image is RGBA
        if img_array.shape[2] == 4:
            img_array = img_array[:, :, :3]
            
        img_array_expanded = np.expand_dims(img_array, axis=0)
        return tf.keras.applications.mobilenet_v2.preprocess_input(img_array_expanded)

    def predict(self, processed_image):
        """
        Uses the loaded model to make a prediction on a preprocessed image.
        
        Returns:
            A list of top 3 predictions or None if an error occurs.
        """
        if not self.model:
            print("Error: Prediction called before model was loaded.")
            return None
            
        try:
            predictions = self.model.predict(processed_image, verbose=0)
            # Decode the predictions into human-readable labels
            return tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None

class WikipediaService:
    """Handles all interactions with the Wikipedia API."""
    def __init__(self):
        """Initializes the Wikipedia service with a custom user agent."""
        self.wiki_api = wikipediaapi.Wikipedia(
            user_agent='FaunaLens/1.3 (https://github.com/your-repo)', # Good practice to set a user agent
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )

    def fetch_summary(self, query, lang_code='en'):
        """
        Fetches a page summary from Wikipedia for a given query and language.
        
        Returns:
            A tuple of (page_title, page_summary). Returns (query, None) on failure.
        """
        try:
            self.wiki_api.language = lang_code
            page = self.wiki_api.page(query)
            if page.exists():
                return page.title, page.summary
            else:
                return query, None # Return the original query if page doesn't exist
        except Exception as e:
            print(f"Wikipedia search failed for query '{query}' in lang '{lang_code}': {e}")
            return query, None
