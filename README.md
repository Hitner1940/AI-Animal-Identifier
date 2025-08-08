<div align="right">
<a href="README.chinese.md"><strong>Read in Chinese</strong></a>
</div>

FaunaLens 🐾
Your AI-powered window into the animal kingdom.
FaunaLens is a full-featured, cross-platform desktop application designed to provide a seamless and intuitive experience for animal identification. It showcases a modern application architecture, thoughtful UI/UX design, and the power of machine learning.

Note: A short GIF of your app in action would be perfect here. It's the most important part of a README. You can use a tool like ScreenToGif to record one.

✨ Key Features
🧠 Intelligent Classification: Powered by a robust TensorFlow (Keras) MobileNetV2 model for fast and accurate predictions.

🎨 Modern UI/UX: A clean, responsive interface built with Tkinter, featuring a polished design with full light and dark mode support.

🌍 Fully Internationalized (i18n): Supports 7 languages out-of-the-box, with an extensible architecture that makes adding new languages simple.

🔗 Deep Wikipedia Integration: Go beyond just identifying. Instantly fetch and display a summary for any prediction with a single click, turning the app into a powerful learning tool.

🚀 High-Performance Architecture: The UI launches instantly while the heavy AI model loads in a separate thread, ensuring a smooth, non-blocking user experience from the start. The codebase is professionally structured into app.py (UI Controller), core.py (Backend Logic), and config.py (Settings) for optimal maintainability.

🚀 Getting Started
For Users (Recommended)
Go to the Releases Page.

Download the latest FaunaLens.exe file.

Run it directly—no installation required.

For Developers
Clone the repository:

git clone https://github.com/Hitner1940/AI-Animal-Identifier.git
cd AI-Animal-Identifier

Install dependencies:
(It's highly recommended to use a virtual environment)

pip install -r requirements.txt

Run the application:

python main.py

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

---
