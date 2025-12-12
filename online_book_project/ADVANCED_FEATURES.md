# Advanced Features Implementation Guide

## Optional Enhancements

This file contains code snippets for potential enhancements to take your project to the next level.

## 1. Add Book Rating Feature

### Code Addition to main.py

```python
# In OnlineLibraryApp class, update show_new_book_dialog method:

def show_new_book_dialog(self):
    """Show dialog to add a new book with rating"""
    dialog = tk.Toplevel(self.root)
    dialog.title("Add New Book")
    dialog.geometry("400x300")
    dialog.configure(bg="white")
    
    # ... existing code ...
    
    # Add rating field
    tk.Label(dialog, text="Rating (1-5)", bg="white", font=("Arial", 10)).pack(anchor=tk.W, padx=20, pady=5)
    rating_combo = ttk.Combobox(dialog, values=["1", "2", "3", "4", "5"], state="readonly", width=27)
    rating_combo.pack(padx=20, pady=5)
    rating_combo.set("5")
    
    def save_book():
        # ... existing validation ...
        new_book = {
            "name": name,
            "author": author,
            "date": date,
            "category": category,
            "rating": rating_combo.get()  # Add rating
        }
        # ... rest of method ...
```

### In media.json, add rating field:

```json
{
    "name": "Book Title",
    "author": "Author Name",
    "date": "1990",
    "category": "Novel",
    "rating": "5"
}
```

---

## 2. Add Reading Status (Read/Unread)

### Enhancement Implementation

```python
# Add to data model:
{
    "name": str,
    "author": str,
    "date": str,
    "category": str,
    "status": "read" | "unread",  # New field
    "last_read": str              # Optional date
}

# Add method to toggle read status:
def toggle_read_status(self):
    """Toggle book read status"""
    selected = self.tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a book")
        return
    
    item = selected[0]
    values = self.tree.item(item)["values"]
    book_name = values[0]
    
    # Find and toggle status
    for book in self.books:
        if book["name"] == book_name:
            book["status"] = "read" if book.get("status") == "unread" else "unread"
            self.save_data()
            self.load_books()
            break
```

---

## 3. Export to CSV

### Add Export Functionality

```python
import csv

def export_to_csv(self):
    """Export books to CSV file"""
    try:
        filename = "books_export.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'author', 'date', 'category'])
            writer.writeheader()
            writer.writerows(self.books)
        messagebox.showinfo("Success", f"Books exported to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed: {str(e)}")

# Add button to UI:
export_btn = tk.Button(control_frame, text="Export", bg="#9b59b6", fg="white",
                       font=("Arial", 10), command=self.export_to_csv, width=8)
export_btn.pack(side=tk.LEFT, padx=5)
```

---

## 4. Import from CSV

### Add Import Functionality

```python
def import_from_csv(self):
    """Import books from CSV file"""
    from tkinter import filedialog
    
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not filename:
        return
    
    try:
        imported_count = 0
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('name'):  # Validate
                    self.books.append({
                        'name': row['name'],
                        'author': row['author'],
                        'date': row['date'],
                        'category': row.get('category', 'Novel')
                    })
                    imported_count += 1
        
        self.save_data()
        self.load_books()
        messagebox.showinfo("Success", f"Imported {imported_count} books")
    except Exception as e:
        messagebox.showerror("Error", f"Import failed: {str(e)}")
```

---

## 5. Add Book Statistics Panel

### Create Statistics Widget

```python
def create_statistics_panel(self):
    """Create statistics display panel"""
    stats_frame = tk.Frame(self.root, bg="#ecf0f1", height=40)
    stats_frame.pack(fill=tk.X, padx=10, pady=5)
    
    total_books = len(self.books)
    categories = {}
    for book in self.books:
        cat = book.get('category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    stats_text = f"Total Books: {total_books} | "
    for cat, count in categories.items():
        stats_text += f"{cat}: {count} | "
    
    stats_label = tk.Label(stats_frame, text=stats_text, bg="#ecf0f1", 
                           font=("Arial", 9), justify=tk.LEFT)
    stats_label.pack(anchor=tk.W, padx=10)
```

---

## 6. Advanced Search with Filters

### Enhanced Search Method

```python
def advanced_search_dialog(self):
    """Show advanced search with multiple filters"""
    search_dialog = tk.Toplevel(self.root)
    search_dialog.title("Advanced Search")
    search_dialog.geometry("400x300")
    
    # Name search
    tk.Label(search_dialog, text="Book Name").pack(anchor=tk.W, padx=10, pady=5)
    name_var = tk.StringVar()
    tk.Entry(search_dialog, textvariable=name_var, width=40).pack(padx=10, pady=5)
    
    # Author search
    tk.Label(search_dialog, text="Author").pack(anchor=tk.W, padx=10, pady=5)
    author_var = tk.StringVar()
    tk.Entry(search_dialog, textvariable=author_var, width=40).pack(padx=10, pady=5)
    
    # Category filter
    tk.Label(search_dialog, text="Category").pack(anchor=tk.W, padx=10, pady=5)
    category_var = tk.StringVar(value="All")
    ttk.Combobox(search_dialog, textvariable=category_var,
                 values=["All", "Novel", "Philosophy", "Poetry"],
                 state="readonly", width=37).pack(padx=10, pady=5)
    
    def execute_search():
        results = self.books
        
        if name_var.get():
            results = [b for b in results if name_var.get().lower() in b["name"].lower()]
        
        if author_var.get():
            results = [b for b in results if author_var.get().lower() in b["author"].lower()]
        
        if category_var.get() != "All":
            results = [b for b in results if b.get("category") == category_var.get()]
        
        self.refresh_tree(results)
        search_dialog.destroy()
    
    tk.Button(search_dialog, text="Search", bg="#3498db", fg="white",
             command=execute_search).pack(pady=20)
```

---

## 7. Add Edit Book Functionality

### Edit Existing Book

```python
def edit_selected_book(self):
    """Edit selected book"""
    selected = self.tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a book to edit")
        return
    
    item = selected[0]
    values = self.tree.item(item)["values"]
    book_name = values[0]
    
    # Find the book
    book = None
    for b in self.books:
        if b["name"] == book_name:
            book = b
            break
    
    if not book:
        return
    
    # Create edit dialog
    dialog = tk.Toplevel(self.root)
    dialog.title("Edit Book")
    dialog.geometry("400x250")
    
    tk.Label(dialog, text="Name").pack(anchor=tk.W, padx=20, pady=5)
    name_entry = tk.Entry(dialog, width=30)
    name_entry.insert(0, book["name"])
    name_entry.pack(padx=20, pady=5)
    
    tk.Label(dialog, text="Author").pack(anchor=tk.W, padx=20, pady=5)
    author_entry = tk.Entry(dialog, width=30)
    author_entry.insert(0, book["author"])
    author_entry.pack(padx=20, pady=5)
    
    tk.Label(dialog, text="Date").pack(anchor=tk.W, padx=20, pady=5)
    date_entry = tk.Entry(dialog, width=30)
    date_entry.insert(0, book["date"])
    date_entry.pack(padx=20, pady=5)
    
    def save_changes():
        book["name"] = name_entry.get()
        book["author"] = author_entry.get()
        book["date"] = date_entry.get()
        self.save_data()
        self.load_books()
        messagebox.showinfo("Success", "Book updated successfully")
        dialog.destroy()
    
    tk.Button(dialog, text="Save", bg="#27ae60", fg="white",
             command=save_changes, width=10).pack(pady=20)
```

---

## 8. Book Statistics Dashboard

### Visual Statistics Implementation

```python
def show_statistics(self):
    """Show book statistics"""
    stats_window = tk.Toplevel(self.root)
    stats_window.title("Library Statistics")
    stats_window.geometry("400x300")
    
    # Total books
    total = len(self.books)
    tk.Label(stats_window, text=f"Total Books: {total}", 
            font=("Arial", 14, "bold")).pack(pady=10)
    
    # By category
    categories = {}
    for book in self.books:
        cat = book.get("category", "Other")
        categories[cat] = categories.get(cat, 0) + 1
    
    tk.Label(stats_window, text="Books by Category:", 
            font=("Arial", 12, "bold")).pack()
    
    for cat, count in sorted(categories.items()):
        percentage = (count / total * 100) if total > 0 else 0
        tk.Label(stats_window, text=f"{cat}: {count} ({percentage:.1f}%)",
                font=("Arial", 10)).pack()
    
    # Most recent
    if self.books:
        latest = max(self.books, key=lambda x: int(x.get("date", 0)))
        tk.Label(stats_window, text=f"Latest Book: {latest['name']} ({latest['date']})",
                font=("Arial", 10), fg="blue").pack(pady=10)
```

---

## 9. Backup and Restore

### Data Backup Functionality

```python
import shutil
from datetime import datetime

def backup_data(self):
    """Create backup of media.json"""
    try:
        backup_file = f"media_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        shutil.copy(self.data_file, backup_file)
        messagebox.showinfo("Success", f"Backup created: {backup_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Backup failed: {str(e)}")

def restore_backup(self):
    """Restore from backup"""
    from tkinter import filedialog
    
    filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not filename:
        return
    
    if messagebox.askyesno("Confirm", "Replace current library with backup?"):
        try:
            shutil.copy(filename, self.data_file)
            self.load_data()
            self.load_books()
            messagebox.showinfo("Success", "Library restored successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Restore failed: {str(e)}")
```

---

## 10. Dark Mode Implementation

### Add Dark Mode Theme

```python
def apply_dark_mode(self):
    """Apply dark theme to application"""
    dark_bg = "#1e1e1e"
    dark_fg = "#ffffff"
    
    self.root.configure(bg=dark_bg)
    
    # Update all widgets to dark theme
    # Note: Would require updating all widget configurations
    messagebox.showinfo("Theme", "Dark mode activated (requires restart for full effect)")

def apply_light_mode(self):
    """Apply light theme to application"""
    self.root.configure(bg="#f0f0f0")
    messagebox.showinfo("Theme", "Light mode activated")
```

---

## Implementation Priority

1. **High Priority** (Easy, High Value):
   - Book ratings
   - Export to CSV
   - Statistics panel
   - Edit book functionality

2. **Medium Priority** (Moderate Difficulty):
   - Import from CSV
   - Advanced search
   - Reading status
   - Backup/restore

3. **Lower Priority** (Complex, Special Use):
   - Database backend
   - User accounts
   - Cloud sync
   - Dark mode

---

## Notes

- Each enhancement can be added independently
- Test thoroughly after each addition
- Update media.json schema as needed
- Consider backward compatibility
- Add user documentation for new features
- Update PROJECT_GUIDE.md with new features

## Testing the Enhancements

After implementing any enhancement:

1. Test with sample data
2. Test with empty library
3. Test with large dataset (100+ books)
4. Verify data persists after restart
5. Check error handling
6. Ensure UI remains responsive

---

**Keep learning and improving your project!**
