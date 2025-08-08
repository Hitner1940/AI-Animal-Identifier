# main.py
# -*- coding: utf-8 -*-
"""
Main entry point for the FaunaLens application.

This script's sole responsibility is to initialize the Tkinter root window,
create an instance of the main application controller (AppController),
and start the main event loop.
"""
import tkinter as tk
from app import AppController

if __name__ == "__main__":
    # Create the main Tkinter window
    root = tk.Tk()
    
    # Create and start the application by instantiating the controller
    app = AppController(root)
    
    # Enter the Tkinter main event loop to run the application
    root.mainloop()
