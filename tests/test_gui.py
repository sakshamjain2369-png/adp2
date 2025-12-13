import json
import os
import sys
import tkinter as tk
import pytest

# Add online_book_project to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'online_book_project'))

from storage.storage import BookStorage
from backend.book_manager import BookManager
from frontend.gui import ModernLibraryGUI


class TestModernLibraryGUIDisplaysBooks:
    """Frontend GUI Test: Verify ModernLibraryGUI displays books in the interface"""
    
    def test_gui_displays_books_from_storage(self, tmp_path):
        """Test that GUI initializes and correctly displays books from storage"""
        # Prepare test JSON with sample books
        fname = str(tmp_path / "media.json")
        data = [
            {"name": "Python Crash Course", "author": "Eric Matthes", "date": "2015", "category": "Novel"},
            {"name": "Clean Code", "author": "Robert Martin", "date": "2008", "category": "Novel"}
        ]
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        # Initialize storage and manager
        storage = BookStorage(fname)
        storage.load_data()
        manager = BookManager(storage)
        
        # Create GUI
        root = tk.Tk()
        try:
            app = ModernLibraryGUI(root, manager, storage)
            root.update()  # Process pending events to render GUI
            
            # Verify that the book display widget contains our books
            if hasattr(app, "tree") and app.tree:
                items = app.tree.get_children()
                assert len(items) > 0, "Treeview should contain book items"
                
                # Verify at least one book is displayed
                found_books = []
                for item in items:
                    values = app.tree.item(item).get("values")
                    if values:
                        found_books.append(str(values))
                
                assert any("Python Crash Course" in str(b) or "Clean Code" in str(b) for b in found_books), \
                    "GUI should display at least one of the test books"
            else:
                pytest.skip("Treeview widget not found in GUI")
        finally:
            root.destroy()
