<br>

<details>
<summary><strong>點擊以展開中文版本 (Click to Expand Chinese Version)</strong></summary>

# FaunaLens v1.2.3 🐾

### 你的人工智慧動物王國之窗。

[![Python Version](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/github/v/release/Your-Username/Your-Repo-Name)](https://github.com/Your-Username/Your-Repo-Name/releases/latest)

這不只是一個 Python 腳本。FaunaLens 是一個功能齊全、跨平台的桌面應用程式，從零開始打造，旨在為動物識別提供無縫且直觀的體驗。它展示了現代化的應用程式架構、深思熟慮的 UI/UX 設計以及機器學習的力量。

> **注意：** 錄製一段你 App 運作的簡短 GIF 動圖，並替換上面的連結。這是你 README 中最重要的一部分。你可以使用像 [ScreenToGif](https://www.screentogif.com/) 這樣的工具。

## ✨ 核心功能 (Key Features)

* **🧠 智慧分類 (Intelligent Classification):** 由強大的 **TensorFlow (Keras)** `MobileNetV2` 模型驅動，提供快速且準確的預測。
* **🎨 純正 Apple HIG 設計 (True Apple HIG Design):** UI 不僅是「受到啟發」，而是建立在蘋果人機介面指南 (Human Interface Guidelines) 的核心原則之上。
    * **語意色彩 (Semantic Colors):** 紅色用於清除，綠色用於主要操作，藍色用於互動元素。
    * **層次化佈局 (Hierarchical Layout):** 使用多層次的背景 (`systemBackground`, `secondarySystemBackground`) 創造深度和視覺焦點。
    * **明暗模式 (Light & Dark Modes):** 完全自適應的主題，適用於任何環境。
* **🌍 完全國際化 (Fully Internationalized - i18n):** 開箱即用支援 7 種語言，其可擴展的架構讓未來新增更多語言變得輕而易舉。所有翻譯都由外部 `.json` 檔案管理。
* **⚡ 動態與響應式 UI (Dynamic & Responsive UI):**
    * 佈局在分析後會智慧地**隱藏大圖並顯示縮圖**，將焦點集中在結果上。
    * **自訂打造的全圓角按鈕**和可互動的懸停結果列，提供了優質的觸感。
* **🔗 深度維基百科整合 (Deep Wikipedia Integration):** 超越識別。只需輕輕一點，即可立即抓取並顯示任何預測結果的摘要，將 App 變成一個學習工具。
* **🚀 高效能架構 (High-Performance Architecture):**
    * UI 介面可立即啟動，而沉重的 AI 模型則在獨立的執行緒中載入，確保了流暢的使用者體驗。
    * 程式碼庫經過專業重構，分為 `app.py` (UI)、`core.py` (引擎) 和 `utils.py` (工具箱)，以實現最佳的可維護性。

## 🚀 如何開始 (Getting Started)

### 給一般使用者 (For Users - 推薦)

1.  Go to the [**Releases Page**]([https://github.com/Hitner1940/AI-Animal-Identifier/tags).
1.  前往 [**Releases 頁面**]()。
2.  下載最新的 `FaunaLens.exe` 檔案。
3.  直接執行，無需安裝。

### 給開發者 (For Developers)

1.  **Clone 倉庫：**
    ```bash
    git clone [https://github.com/Hitner1940/AI-Animal-Identifier.git]
    cd FaunaLens
    ```
2.  **安裝依賴套件：**
    ```bash
    pip install -r requirements.txt
    ```
3.  **執行應用程式：**
    ```bash
    python app.py
    ```

## 📜 授權條款 (License)

本專案採用 MIT 授權條款。詳情請見 [LICENSE](LICENSE) 檔案。

</details>
