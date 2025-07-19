FaunaLens v2.2 🐾
Your AI-powered window to the animal kingdom.
This isn't just another Python script. FaunaLens is a fully-featured, cross-platform desktop application built from the ground up to provide a seamless and intuitive experience for animal identification. It's a showcase of modern application architecture, thoughtful UI/UX design, and the power of machine learning.

Note: Create a short GIF of your app in action and replace the link above. This is the most important part of your README. Use a tool like ScreenToGif.

✨ Key Features
🧠 Intelligent Classification: Powered by the robust TensorFlow (Keras) MobileNetV2 model for fast and accurate predictions.

🎨 True Apple HIG Design: The UI isn't just "inspired" by Apple; it's built on the core principles of the Human Interface Guidelines.

Semantic Colors: Red for destructive, Green for primary actions.

Hierarchical Layout: Layered backgrounds create depth and focus.

Light & Dark Modes: Fully adaptive themes for any environment.

🌍 Fully Internationalized (i18n): Supports 7 languages out of the box, with a scalable architecture that makes adding more a breeze. All translations are managed in external .json files.

⚡ Dynamic & Responsive UI:

The layout intelligently adapts after analysis, hiding the large image and showing a thumbnail to focus on the results.

Custom-built, fully-rounded widgets and interactive, hover-able result rows provide a premium feel.

🔗 Deep Wikipedia Integration: Go beyond identification. Instantly fetch and display summaries for any prediction with a single click, turning the app into a learning tool.

🚀 High-Performance Architecture:

The UI launches instantly while the heavy AI model loads in a separate thread.

The codebase is professionally refactored into app.py (UI), core.py (Engine), and utils.py (Toolbox) for maximum maintainability.

🛠️ Tech Stack & Architecture
Category

Technology / Principle

Backend

Python 3.11

AI/ML

TensorFlow (Keras)

GUI

Tkinter, ttk

Imaging

Pillow (PIL), OpenCV

Packaging

PyInstaller

Design

Apple Human Interface Guidelines, Semantic Coloring

Arch.

Multi-threading, Modular (Single Responsibility)

Project Structure
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


🚀 Getting Started
For Users (Recommended)
Go to the Releases Page.

Download the latest FaunaLens.exe file.

Run it. No installation needed.

For Developers
Clone the repository:

git clone https://github.com/Your-Username/Your-Repo-Name.git
cd FaunaLens


Install dependencies:

pip install -r requirements.txt


Run the application:

python app.py


📜 License
This project is licensed under the MIT License. See the LICENSE file for details.
