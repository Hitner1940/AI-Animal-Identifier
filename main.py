# -*- coding: utf-8 -*-
import tkinter as tk
from app import AnimalIdentifierApp

# =================================================================================
#  Main Entry Point
#  This file is the starting point for the entire application.
#  Its sole responsibility is to create the main window and start our App controller.
# =================================================================================
if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    # Create and start the application
    app = AnimalIdentifierApp(root)
    # Enter the main event loop
    root.mainloop()
