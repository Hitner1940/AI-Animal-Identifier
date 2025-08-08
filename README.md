<div align="right">
<a href="README.chinese.md"><strong>Read in Chinese</strong></a>
</div>
<br\>

# FaunaLens 🐾

### Your AI-powered window into the animal kingdom.

[](https://www.python.org/downloads/release/python-3110/)
[](https://opensource.org/licenses/MIT)
[](https://www.google.com/search?q=https://github.com/Hitner1940/AI-Animal-Identifier/releases/latest)

FaunaLens is a full-featured, cross-platform desktop application designed to provide a seamless and intuitive experience for animal identification. It showcases a modern application architecture, thoughtful UI/UX design, and the power of machine learning.

> **Note:** A short GIF of your app in action would be perfect here. It's the most important part of a README. You can use a tool like [ScreenToGif](https://www.screentogif.com/) to record one.

-----

## ✨ Key Features

  * **🧠 Intelligent Classification:** Powered by the robust **TensorFlow (Keras)** `MobileNetV2` model for fast and accurate predictions.
  * **🎨 Modern UI & UX:** The interface is built on Apple's Human Interface Guidelines, featuring:
      * Semantic colors for intuitive actions (e.g., red for clearing, green for primary actions).
      * A hierarchical layout that uses layered backgrounds to create visual depth.
      * Fully adaptive light and dark modes for any environment.
  * **🌍 Fully Internationalized (i18n):** Comes with out-of-the-box support for 7 languages, managed by an external `languages.json` file for easy expansion.
  * **🔗 Deep Wikipedia Integration:** Instantly fetches and displays a summary for any prediction with a single click, turning the app into a powerful learning tool.

## 🚀 High-Performance Architecture

  * [cite\_start]**⚡ Asynchronous Loading:** The UI launches instantly while the heavy AI model loads in a separate thread, ensuring a smooth, non-blocking user experience[cite: 8].
  * **⚙️ Clean Codebase:** The code is professionally refactored into distinct modules for optimal maintainability:
      * [cite\_start]`app.py`: The main UI controller that manages application state and user events[cite: 8].
      * `core.py`: Handles the backend "business logic," including the ML model and Wikipedia service interaction.
      * [cite\_start]`config.py`: A central file for all static configuration data like themes and sizes, allowing for easy updates[cite: 1].

## 🚀 Getting Started

### For Users (Recommended)

1.  Go to the [**Releases Page**](https://www.google.com/search?q=https://github.com/Hitner1940/AI-Animal-Identifier/releases).
2.  Download the latest `FaunaLens.exe` file.
3.  Run it directly—no installation required.

### For Developers

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Hitner1940/AI-Animal-Identifier.git
    cd AI-Animal-Identifier
    ```

2.  **Install dependencies:**
    *(Using a virtual environment is highly recommended)*

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**

    ```bash
    python main.py
    ```

-----

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
