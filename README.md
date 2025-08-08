<div align="right">
<a href="README.chinese.md"><strong>Read in Chinese</strong></a>
</div>

# FaunaLens v1.2.3 🐾

### Your AI-powered window to the animal kingdom.

[![Python Version](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/github/v/release/Your-Username/Your-Repo-Name)](https://github.com/Your-Username/Your-Repo-Name/releases/latest)

This isn't just another Python script. FaunaLens is a fully-featured, cross-platform desktop application built from the ground up to provide a seamless and intuitive experience for animal identification. It's a showcase of modern application architecture, thoughtful UI/UX design, and the power of machine learning.

![FaunaLens Demo GIF](https://i.imgur.com/your-demo-gif.gif)
> **Note:** Create a short GIF of your app in action and replace the link above. This is the most important part of your README. Use a tool like [ScreenToGif](https://www.screentogif.com/).

---

## ✨ Key Features

* **🧠 Intelligent Classification:** Powered by the robust **TensorFlow (Keras)** `MobileNetV2` model for fast and accurate predictions.
* **🎨 True Apple HIG Design:** The UI isn't just "inspired" by Apple; it's built on the core principles of the Human Interface Guidelines.
    * **Semantic Colors:** Red for destructive, Green for primary actions.
    * **Hierarchical Layout:** Layered backgrounds create depth and focus.
    * **Light & Dark Modes:** Fully adaptive themes for any environment.
* **🌍 Fully Internationalized (i18n):** Supports 7 languages out of the box, with a scalable architecture that makes adding more a breeze. All translations are managed in external `.json` files.
* **⚡ Dynamic & Responsive UI:**
    * The layout intelligently **hides the large image and shows a thumbnail** after analysis to focus on the results.
    * **Custom-built, fully-rounded buttons** and interactive, hover-able result rows provide a premium feel.
* **🔗 Deep Wikipedia Integration:** Go beyond identification. Instantly fetch and display summaries for any prediction with a single click, turning the app into a learning tool.
* **🚀 High-Performance Architecture:**
    * The UI launches instantly while the heavy AI model loads in a separate thread.
    * The codebase is professionally refactored into `app.py` (UI), `core.py` (Engine), and `utils.py` (Toolbox) for maximum maintainability.

## 🛠️ Tech Stack & Architecture

| Category      | Technology / Principle                               |
| :------------ | :--------------------------------------------------- |
| **Backend** | Python 3.11                                          |
| **AI/ML** | TensorFlow (Keras)                                   |
| **GUI** | Tkinter, `ttk`                                       |
| **Imaging** | Pillow (PIL), OpenCV                                 |
| **Packaging** | PyInstaller                                          |
| **Design** | Apple Human Interface Guidelines, Semantic Coloring  |
| **Arch.** | Multi-threading, Modular (Single Responsibility)     |

### Project Structure

The project is structured for scalability and maintainability, separating concerns into distinct modules.

FaunaLens/
│
├── app.py              # Main application logic, UI, and event handling
├── core.py             # Handles AI model, predictions, and API calls
├── utils.py            # Helper functions (e.g., resource paths, image manipulation)
│
├── locales/            # Internationalization (i18n) files
│   ├── en.json
│   └── ... (7+ languages)
│
├── README.md           # You are here
├── requirements.txt    # Project dependencies
└── LICENSE             # MIT License


## 🚀 Getting Started

### For Users (Recommended)

1.  Go to the [**Releases Page**](https://github.com/Your-Username/Your-Repo-Name/releases/latest).
2.  Download the latest `FaunaLens.exe` file.
3.  Run it. No installation needed.

### For Developers

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Hitner1940/AI-Animal-Identifier.git]
    cd FaunaLens
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application:**
    ```bash
    python app.py
    ```

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
