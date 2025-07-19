FaunaLens v2.2 🐾你的人工智慧動物王國之窗。這不只是一個 Python 腳本。FaunaLens 是一個功能齊全、跨平台的桌面應用程式，從零開始打造，旨在為動物識別提供無縫且直觀的體驗。它展示了現代化的應用程式架構、深思熟慮的 UI/UX 設計以及機器學習的力量。注意： 錄製一段你 App 運作的簡短 GIF 動圖，並替換上面的連結。這是你 README 中最重要的一部分。你可以使用像 ScreenToGif 這樣的工具。✨ 核心功能 (Key Features)🧠 智慧分類 (Intelligent Classification): 由強大的 TensorFlow (Keras) MobileNetV2 模型驅動，提供快速且準確的預測。🎨 純正 Apple HIG 設計 (True Apple HIG Design): UI 不僅是「受到啟發」，而是建立在蘋果人機介面指南 (Human Interface Guidelines) 的核心原則之上。語意色彩 (Semantic Colors): 紅色用於清除，綠色用於主要操作，藍色用於互動元素。層次化佈局 (Hierarchical Layout): 使用多層次的背景 (systemBackground, secondarySystemBackground) 創造深度和視覺焦點。明暗模式 (Light & Dark Modes): 完全自適應的主題，適用於任何環境。🌍 完全國際化 (Fully Internationalized - i18n): 開箱即用支援 7 種語言，其可擴展的架構讓未來新增更多語言變得輕而易舉。所有翻譯都由外部 .json 檔案管理。⚡ 動態與響應式 UI (Dynamic & Responsive UI):佈局在分析後會智慧地隱藏大圖並顯示縮圖，將焦點集中在結果上。自訂打造的全圓角按鈕和可互動的懸停結果列，提供了優質的觸感。🔗 深度維基百科整合 (Deep Wikipedia Integration): 超越識別。只需輕輕一點，即可立即抓取並顯示任何預測結果的摘要，將 App 變成一個學習工具。🚀 高效能架構 (High-Performance Architecture):UI 介面可立即啟動，而沉重的 AI 模型則在獨立的執行緒中載入，確保了流暢的使用者體驗。程式碼庫經過專業重構，分為 app.py (UI)、core.py (引擎) 和 utils.py (工具箱)，以實現最佳的可維護性。🛠️ 技術堆疊與架構 (Tech Stack & Architecture)類別 (Category)技術 / 原則 (Technology / Principle)後端 (Backend)Python 3.11AI/MLTensorFlow (Keras)GUITkinter, ttk影像處理 (Imaging)Pillow (PIL), OpenCV打包 (Packaging)PyInstaller設計 (Design)Apple Human Interface Guidelines, Semantic Coloring架構 (Arch.)Multi-threading, Modular (Single Responsibility)專案結構 (Project Structure)專案的結構是為了可擴展性和可維護性而設計的，將不同的關注點分離到獨立的模組中。FaunaLens/
│
├── app.py              # 主應用程式邏輯、UI 和事件處理
├── core.py             # 處理 AI 模型、預測和 API 呼叫
├── utils.py            # 輔助函式 (例如：資源路徑、影像處理)
│
├── locales/            # 國際化 (i18n) 檔案
│   ├── en.json
│   └── ... (7+ 種語言)
│
├── README.md           # 你正在閱讀的檔案
├── requirements.txt    # 專案依賴
└── LICENSE             # MIT 授權條款
🚀 如何開始 (Getting Started)給一般使用者 (For Users - 推薦)前往 Releases 頁面。下載最新的 FaunaLens.exe 檔案。直接執行，無需安裝。給開發者 (For Developers)Clone 倉庫：git clone https://github.com/Your-Username/Your-Repo-Name.git
cd FaunaLens
安裝依賴套件：pip install -r requirements.txt
執行應用程式：python app.py
📜 授權條款 (License)本專案採用 MIT 授權條款。詳情請見 LICENSE 檔案。<br><details><summary><strong>Click to view English Version</strong></summary>FaunaLens v2.2 🐾Your AI-powered window to the animal kingdom.This isn't just another Python script. FaunaLens is a fully-featured, cross-platform desktop application built from the ground up to provide a seamless and intuitive experience for animal identification. It's a showcase of modern application architecture, thoughtful UI/UX design, and the power of machine learning.Note: Create a short GIF of your app in action and replace the link above. This is the most important part of your README. Use a tool like ScreenToGif.✨ Key Features🧠 Intelligent Classification: Powered by the robust TensorFlow (Keras) MobileNetV2 model for fast and accurate predictions.🎨 True Apple HIG Design: The UI isn't just "inspired" by Apple; it's built on the core principles of the Human Interface Guidelines.Semantic Colors: Red for destructive, Green for primary actions.Hierarchical Layout: Layered backgrounds create depth and focus.Light & Dark Modes: Fully adaptive themes for any environment.🌍 Fully Internationalized (i18n): Supports 7 languages out of the box, with a scalable architecture that makes adding more a breeze. All translations are managed in external .json files.⚡ Dynamic & Responsive UI:The layout intelligently hides the large image and shows a thumbnail after analysis to focus on the results.Custom-built, fully-rounded buttons and interactive, hover-able result rows provide a premium feel.🔗 Deep Wikipedia Integration: Go beyond identification. Instantly fetch and display summaries for any prediction with a single click, turning the app into a learning tool.🚀 High-Performance Architecture:The UI launches instantly while the heavy AI model loads in a separate thread.The codebase is professionally refactored into app.py (UI), core.py (Engine), and utils.py (Toolbox) for maximum maintainability.🛠️ Tech Stack & ArchitectureCategoryTechnology / PrincipleBackendPython 3.11AI/MLTensorFlow (Keras)GUITkinter, ttkImagingPillow (PIL), OpenCVPackagingPyInstallerDesignApple Human Interface Guidelines, Semantic ColoringArch.Multi-threading, Modular (Single Responsibility)Project StructureThe project is structured for scalability and maintainability, separating concerns into distinct modules.FaunaLens/
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
🚀 Getting StartedFor Users (Recommended)Go to the Releases Page.Download the latest FaunaLens.exe file.Run it. No installation needed.For DevelopersClone the repository:git clone https://github.com/Your-Username/Your-Repo-Name.git
cd FaunaLens
Install dependencies:pip install -r requirements.txt
Run the application:python app.py
📜 LicenseThis project is licensed under the MIT License. See the LICENSE file for details.</details>
