"""
Saksham's Reading Room
Main entry point that orchestrates frontend, backend, and storage modules
"""
import tkinter as tk
import os
import sys

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frontend.gui import ModernLibraryGUI
from backend.book_manager import BookManager
from storage.storage import BookStorage


def main():
    """Initialize and run Saksham's Reading Room application"""
    
    # Initialize storage
    storage = BookStorage("media.json")
    storage.load_data()
    
    # Initialize book manager with storage
    book_manager = BookManager(storage)
    
    # Initialize and run GUI
    root = tk.Tk()
    app = ModernLibraryGUI(root, book_manager, storage)
    root.mainloop()


if __name__ == "__main__":
    main()
