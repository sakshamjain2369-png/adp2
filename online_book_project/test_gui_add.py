"""
Minimal test GUI to debug add/delete functionality
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from storage.storage import BookStorage
from backend.book_manager import BookManager


class TestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Add/Delete")
        self.root.geometry("600x400")
        
        # Initialize storage and manager
        self.storage = BookStorage("media.json")
        self.storage.load_data()
        self.manager = BookManager(self.storage)
        
        # Info label
        info = tk.Label(root, text="Testing Add/Delete", font=("Arial", 14, "bold"))
        info.pack(pady=10)
        
        # Current count
        self.count_label = tk.Label(root, text=f"Books: {len(self.storage.get_books())}", 
                                    font=("Arial", 12))
        self.count_label.pack(pady=5)
        
        # Add book button
        add_btn = tk.Button(root, text="ADD BOOK", bg="green", fg="white", font=("Arial", 12),
                           command=self.add_book, padx=20, pady=10)
        add_btn.pack(pady=10)
        
        # Delete book button
        del_btn = tk.Button(root, text="DELETE LAST BOOK", bg="red", fg="white", font=("Arial", 12),
                           command=self.delete_book, padx=20, pady=10)
        del_btn.pack(pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(root, text="REFRESH COUNT", font=("Arial", 12),
                               command=self.refresh_count, padx=20, pady=10)
        refresh_btn.pack(pady=10)
        
        # List books
        self.text = tk.Text(root, height=10, width=60)
        self.text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.show_books()
    
    def show_books(self):
        """Display all books"""
        self.text.delete(1.0, tk.END)
        books = self.storage.get_books()
        for i, b in enumerate(books, 1):
            self.text.insert(tk.END, f"{i}. {b.get('name')} by {b.get('author')} ({b.get('date')})\n")
    
    def add_book(self):
        """Add a simple test book"""
        import time
        name = f"New Book {int(time.time())}"
        book = {
            "name": name,
            "author": "Test Author",
            "date": "2025",
            "category": "Novel"
        }
        
        print(f"[ADD] Adding: {book}")
        result = self.manager.add_book(book)
        print(f"[ADD] Result: {result}")
        
        # Check file
        import json
        with open(self.storage.data_file, 'r') as f:
            file_data = json.load(f)
        print(f"[ADD] File now has {len(file_data)} books")
        
        self.refresh_count()
        messagebox.showinfo("Success", f"Added: {name}")
    
    def delete_book(self):
        """Delete the last book"""
        books = self.storage.get_books()
        if not books:
            messagebox.showwarning("Warning", "No books to delete")
            return
        
        last_book = books[-1]
        name = last_book.get("name")
        
        print(f"[DELETE] Deleting: {name}")
        result = self.manager.delete_book(name)
        print(f"[DELETE] Result: {result}")
        
        # Check file
        import json
        with open(self.storage.data_file, 'r') as f:
            file_data = json.load(f)
        print(f"[DELETE] File now has {len(file_data)} books")
        
        self.refresh_count()
        messagebox.showinfo("Success", f"Deleted: {name}")
    
    def refresh_count(self):
        """Reload and show updated count"""
        self.storage.load_data()
        count = len(self.storage.get_books())
        self.count_label.config(text=f"Books: {count}")
        self.show_books()


if __name__ == "__main__":
    root = tk.Tk()
    app = TestGUI(root)
    root.mainloop()
