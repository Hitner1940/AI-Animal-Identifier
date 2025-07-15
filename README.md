🐾 FaunaLens: AI Animal Identifier
A smart, modern desktop application built with Python and TensorFlow to identify animals from images and videos. This project showcases a complete development cycle from concept to a feature-rich, user-friendly tool.

(Pro-tip: Record a short GIF of your app working and replace the link above. It makes your project look 10x more professional. You can use a tool like ScreenToGif.)

✨ Core Features
🧠 AI-Powered Identification: Leverages the pre-trained MobileNetV2 deep learning model for accurate and fast classification.

📂 Multi-File Support: Analyze animals from a wide range of file types, including images (.jpg, .png, .webp) and videos (.mp4, .avi).

🎨 Sleek, Modern UI: A beautiful, Apple-inspired user interface built from the ground up, featuring both a light and a dark mode for comfortable viewing.

🌐 Multi-Language Ready: Easily switch between English and Traditional Chinese on the fly.

⚡ High-Performance Loading: The UI launches instantly while the heavy AI model loads in the background, ensuring a smooth user experience without long startup waits.

🛠️ Tech Stack
Backend & Core Logic: Python

AI & Machine Learning: TensorFlow (Keras)

Video Processing: OpenCV

GUI Framework: Tkinter (with ttk for modern styling)

Image Handling: Pillow (PIL)

🚀 Getting Started
There are two ways to get this application running.

1. For Everyone (Recommended)
Simply download the latest AnimalIdentifier.exe file from the Releases Page. No installation needed. Just double-click and run.

2. For Developers
If you want to poke around the code or contribute, you'll need to run it from the source.

Clone the repository:

git clone https://github.com/[Your-Username]/[Your-Repo-Name].git
cd [Your-Repo-Name]

Set up a virtual environment (optional but recommended):

python -m venv venv
venv\Scripts\activate  # On Windows

Install dependencies:

pip install -r requirements.txt

Run the application:

python your_script_name.py

(Remember to replace your_script_name.py with your actual file name)

📖 How to Use
Launch the application.

Click the "Select File" button.

Choose an image or video file containing an animal.

The app will display the image/frame and provide the top 3 predictions from the AI model.

Use the toggles in the top-right to switch between languages and themes.

🔮 Future Improvements
This project has a solid foundation, but here's where it could go next:

[ ] Object Detection: Upgrade from classification to object detection (using YOLO or SSD) to draw bounding boxes around multiple animals in a single frame.

[ ] Live Webcam Feed: Implement real-time identification using a live webcam stream.

[ ] Wikipedia API Integration: Fetch and display a short summary of the identified animal from Wikipedia.

[ ] Custom Model Training: Fine-tune the model on a specific dataset (e.g., bird species, dog breeds) for specialized, high-accuracy identification.

This project was built as a learning exercise to cover the full lifecycle of a modern desktop AI application.
