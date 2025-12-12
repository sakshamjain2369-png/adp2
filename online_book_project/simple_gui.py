"""
Saksham's Reading Room - SIMPLE WORKING VERSION
Stripped-down GUI focused on making add/delete work reliably
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from storage.storage import BookStorage
from backend.book_manager import BookManager


class SimpleLibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Saksham's Reading Room")
        self.root.geometry("900x600")
        
        # Initialize backend
        self.storage = BookStorage("media.json")
        self.storage.load_data()
        self.manager = BookManager(self.storage)
        
        # Create UI
        self.create_widgets()
        self.refresh_display()
    
    def create_widgets(self):
        """Create all UI elements"""
        # Top frame for buttons
        top = tk.Frame(self.root)
        top.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(top, text="Saksham's Reading Room", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        tk.Button(top, text="ADD BOOK", bg="green", fg="white", font=("Arial", 10, "bold"),
                 command=self.add_book_simple, padx=15, pady=5).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(top, text="REFRESH", bg="blue", fg="white", font=("Arial", 10),
                 command=self.refresh_display, padx=15, pady=5).pack(side=tk.RIGHT, padx=5)
        
        # Info frame
        info = tk.Frame(self.root)
        info.pack(fill=tk.X, padx=10, pady=5)
        
        self.info_label = tk.Label(info, text="", font=("Arial", 10))
        self.info_label.pack(side=tk.LEFT)
        
        # Table
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview
        columns = ("Title", "Author", "Year", "Category")
        self.tree = ttk.Treeview(table_frame, columns=columns, height=15, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bottom action frame
        bottom = tk.Frame(self.root)
        bottom.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(bottom, text="DELETE SELECTED", bg="red", fg="white", font=("Arial", 10, "bold"),
                 command=self.delete_book_simple, padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom, text="EDIT SELECTED", bg="orange", fg="white", font=("Arial", 10, "bold"),
                 command=self.edit_book_simple, padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(bottom, text="Ready", font=("Arial", 9), fg="gray")
        self.status_label.pack(side=tk.RIGHT)
    
    def add_book_simple(self):
        """Simple add book without complex dialogs"""
        print("[ADD] Button clicked")
        
        # Use simple input dialogs
        title = simpledialog.askstring("Add Book", "Book Title:")
        if not title:
            return
        
        author = simpledialog.askstring("Add Book", "Author Name:")
        if not author:
            return
        
        year = simpledialog.askstring("Add Book", "Publication Year:")
        if not year:
            return
        
        category = simpledialog.askstring("Add Book", "Category (Novel/Philosophy/Poetry):", initialvalue="Novel")
        if not category:
            category = "Novel"
        
        # Create book dict
        book = {
            "name": title.strip(),
            "author": author.strip(),
            "date": year.strip(),
            "category": category.strip()
        }
        
        print("[ADD] Adding book: {}".format(book))
        
        # Add via manager
        result = self.manager.add_book(book)
        print("[ADD] Manager returned: {}".format(result))
        
        if result:
            # Reload storage from disk
            self.storage.load_data()
            self.refresh_display()
            messagebox.showinfo("Success", "Book '{}' added successfully!".format(title))
            self.status_label.config(text="Added: {}".format(title))
        else:
            messagebox.showerror("Error", "Failed to add book")
    
    def delete_book_simple(self):
        """Simple delete selected book"""
        print("[DELETE] Button clicked")
        
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return
        
        item = selected[0]
        values = self.tree.item(item)["values"]
        title = values[0]
        
        print("[DELETE] Deleting: {}".format(title))
        
        if messagebox.askyesno("Confirm", "Delete '{}'?".format(title)):
            result = self.manager.delete_book(title)
            print("[DELETE] Manager returned: {}".format(result))
            
            if result:
                # Reload storage from disk
                self.storage.load_data()
                self.refresh_display()
                messagebox.showinfo("Success", "Book deleted!")
                self.status_label.config(text="Deleted: {}".format(title))
            else:
                messagebox.showerror("Error", "Failed to delete book")
    
    def edit_book_simple(self):
        """Simple edit selected book"""
        print("[EDIT] Button clicked")
        
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to edit")
            return
        
        item = selected[0]
        values = self.tree.item(item)["values"]
        old_title = values[0]
        old_author = values[1]
        old_year = values[2]
        old_category = values[3]
        
        print("[EDIT] Editing: {}".format(old_title))
        
        title = simpledialog.askstring("Edit Book", "Book Title:", initialvalue=old_title)
        if title is None:
            return
        
        author = simpledialog.askstring("Edit Book", "Author Name:", initialvalue=old_author)
        if author is None:
            return
        
        year = simpledialog.askstring("Edit Book", "Publication Year:", initialvalue=old_year)
        if year is None:
            return
        
        category = simpledialog.askstring("Edit Book", "Category:", initialvalue=old_category)
        if category is None:
            return
        
        # Create updated book dict
        updated_book = {
            "name": title.strip(),
            "author": author.strip(),
            "date": year.strip(),
            "category": category.strip()
        }
        
        print("[EDIT] Updating to: {}".format(updated_book))
        
        result = self.manager.update_book(old_title, updated_book)
        print("[EDIT] Manager returned: {}".format(result))
        
        if result:
            # Reload storage from disk
            self.storage.load_data()
            self.refresh_display()
            messagebox.showinfo("Success", "Book updated!")
            self.status_label.config(text="Updated: {}".format(title))
        else:
            messagebox.showerror("Error", "Failed to update book")
    
    def refresh_display(self):
        """Refresh the book list display"""
        print("[REFRESH] Refreshing display")
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load books
        books = self.manager.get_all_books()
        print("[REFRESH] Found {} books".format(len(books)))
        
        for book in books:
            self.tree.insert("", tk.END, values=(
                book.get("name", ""),
                book.get("author", ""),
                book.get("date", ""),
                book.get("category", "")
            ))
        
        # Update info
        self.info_label.config(text="Total Books: {} | Novels: {} | Philosophy: {} | Poetry: {}".format(
            len(books),
            len([b for b in books if b.get("category") == "Novel"]),
            len([b for b in books if b.get("category") == "Philosophy"]),
            len([b for b in books if b.get("category") == "Poetry"])
        ))


def main():
    root = tk.Tk()
    app = SimpleLibraryGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
