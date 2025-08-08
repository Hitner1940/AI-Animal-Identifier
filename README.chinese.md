\<br\>

# FaunaLens 🐾

### 您的人工智慧動物王國之窗。

[](https://www.python.org/downloads/release/python-3110/)
[](https://opensource.org/licenses/MIT)
[](https://www.google.com/search?q=https://github.com/Hitner1940/AI-Animal-Identifier/releases/latest)

FaunaLens 是一款功能齊全、跨平台的桌面應用程式，旨在為動物識別提供無縫且直觀的體驗。它不僅是一個腳本，更是一個展示現代化應用程式架構、精良 UI/UX 設計以及機器學習力量的完整專案。

> **注意：** 強烈建議在此處放置一段您 App 運作的簡短 GIF 動圖。這是 README 中最能吸引人的部分。您可以使用像 [ScreenToGif](https://www.screentogif.com/) 這類的免費工具來錄製。

-----

## ✨ 核心功能 (Key Features)

  * **🧠 智慧分類 (Intelligent Classification):** 由強大的 **TensorFlow (Keras)** `MobileNetV2` 模型驅動，提供快速且準確的預測。
  * **🎨 現代化 UI/UX (Modern UI/UX):** 介面遵循蘋果人機介面指南 (Apple's Human Interface Guidelines) 的核心原則，提供：
      * **語意化色彩 (Semantic Colors):** 使用直觀的顏色進行操作（例如：紅色用於清除，綠色用於主要操作）。
      * **層次化佈局 (Hierarchical Layout):** 透過多層次背景創造視覺深度與焦點。
      * **完整的光暗模式 (Light & Dark Modes):** 完美適應任何使用環境。
  * **🌍 完整國際化 (Fully Internationalized - i18n):** 開箱即用，支援 7 種語言。所有翻譯由外部 `languages.json` 檔案管理，讓新增語言變得輕而易舉。
  * **🔗 深度整合維基百科 (Deep Wikipedia Integration):** 功能超越了單純的識別。只需輕輕一點，即可立即抓取並顯示任何預測結果的摘要，將 App 變成一個強大的學習工具。

-----

## 🚀 高效能架構 (High-Performance Architecture)

  * **⚡ 非同步載入 (Asynchronous Loading):** UI 介面可立即啟動，而較為沉重的 AI 模型則在獨立的執行緒 (thread) 中載入，確保了從頭到尾流暢不卡頓的使用者體驗。
  * **⚙️ 清晰的程式碼架構 (Clean Codebase):** 為了達到最佳的可維護性，程式碼經過專業重構，分為各司其職的模組：
      * `app.py`: 主要的 UI 控制器，管理應用程式狀態和使用者事件。
      * `core.py`: 處理後端核心邏輯，包含機器學習模型和維基百科服務。
      * `config.py`: 集中管理所有靜態設定資料，如主題、字體大小，讓客製化更容易。

-----

## 🚀 如何開始 (Getting Started)

### 給一般使用者 (推薦)

1.  前往 [**Releases 發佈頁面**](https://www.google.com/search?q=https://github.com/Hitner1940/AI-Animal-Identifier/releases)。
2.  下載最新的 `FaunaLens.exe` 執行檔。
3.  直接執行，無需安裝。

### 給開發者 (For Developers)

1.  **複製 (Clone) 專案庫：**
    ```bash
    git clone [https://github.com/Hitner1940/AI-Animal-Identifier.git]
    cd FaunaLens
    ```
2.  **安裝相依套件：**
    *(強烈建議在虛擬環境 (virtual environment) 中執行)*
    ```bash
    pip install -r requirements.txt
    ```
3.  **執行應用程式：**
    ```bash
    python app.py
    ```

-----

## 📜 授權條款 (License)

本專案採用 MIT 授權條款。詳情請見 `LICENSE` 檔案。
