# -*- coding: utf-8 -*-
import tkinter as tk
from app import AnimalIdentifierApp

# =================================================================================
#  主執行入口 (Main Entry Point)
#  這個檔案是整個應用程式的起點。
#  它的唯一職責就是：建立主視窗，並啟動我們的 App 控制器。
# =================================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalIdentifierApp(root)
    root.mainloop()