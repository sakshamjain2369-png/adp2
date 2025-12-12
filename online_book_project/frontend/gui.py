"""
Frontend Module - Modern GUI for Saksham's Reading Room using Tkinter
Professional minimalist design with sidebar and clean layout
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class ModernLibraryGUI:
    """Modern professional GUI interface for Saksham's Reading Room"""
    
    def __init__(self, root, book_manager, storage):
        """Initialize modern GUI with references to backend and storage"""
        self.root = root
        self.book_manager = book_manager
        self.storage = storage
        self.books = storage.get_books()
        
        # Setup window
        self.root.title("Saksham's Reading Room")
        self.root.geometry("1400x750")
        self.root.configure(bg="#f5f5f5")
        
        # Define modern color scheme
        self.colors = {
            "sidebar_bg": "#1e3a5f",
            "sidebar_hover": "#2d5a8c",
            "primary": "#27ae60",
            "primary_hover": "#229954",
            "header_bg": "#ffffff",
            "text_dark": "#2c3e50",
            "text_light": "#7f8c8d",
            "border": "#e0e0e0",
            "background": "#f5f5f5"
        }
        
        # Create UI
        self.create_ui()
        self.load_books()
    
    def create_ui(self):
        """Create the modern user interface"""
        # Main container with sidebar
        main_container = tk.Frame(self.root, bg=self.colors["background"])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # ===== SIDEBAR =====
        sidebar = tk.Frame(main_container, bg=self.colors["sidebar_bg"], width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Logo/Title
        logo_frame = tk.Frame(sidebar, bg=self.colors["sidebar_bg"])
        logo_frame.pack(fill=tk.X, padx=15, pady=20)
        
        logo_label = tk.Label(logo_frame, text="BOOKS", font=("Arial", 32, "bold"), bg=self.colors["sidebar_bg"], fg="white")
        logo_label.pack()
        
        title_label = tk.Label(logo_frame, text="Reading Room", font=("Arial", 10, "bold"), 
                               bg=self.colors["sidebar_bg"], fg="white")
        title_label.pack(pady=5)
        
        # Separator
        separator = tk.Frame(sidebar, bg=self.colors["sidebar_hover"], height=1)
        separator.pack(fill=tk.X, padx=10, pady=10)
        
        # Navigation items
        nav_items = [
            ("All Books", "All"),
            ("Novels", "Novel"),
            ("Philosophy", "Philosophy"),
            ("Poetry", "Poetry"),
        ]
        
        self.nav_buttons = {}
        for label, category in nav_items:
            btn = tk.Button(sidebar, text=label, font=("Arial", 10), 
                           bg=self.colors["sidebar_bg"], fg="white",
                           border=0, padx=15, pady=12, justify=tk.LEFT,
                           command=lambda cat=category: self.filter_by_sidebar(cat))
            btn.pack(fill=tk.X, padx=5, pady=3)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors["sidebar_hover"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors["sidebar_bg"]))
            self.nav_buttons[label] = btn
        
        # ===== MAIN CONTENT AREA =====
        content = tk.Frame(main_container, bg=self.colors["background"])
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Header section
        header = tk.Frame(content, bg=self.colors["header_bg"], height=120)
        header.pack(fill=tk.X, padx=20, pady=(15, 10))
        header.pack_propagate(False)
        
        # Main title
        title = tk.Label(header, text="Saksham's Reading Room", 
                        font=("Arial", 28, "bold"), bg=self.colors["header_bg"],
                        fg=self.colors["text_dark"])
        title.pack(anchor=tk.W, pady=(10, 0))
        
        # Subtitle
        subtitle = tk.Label(header, text="A curated space for great books, philosophy & poetry",
                           font=("Arial", 11), bg=self.colors["header_bg"],
                           fg=self.colors["text_light"])
        subtitle.pack(anchor=tk.W, padx=0, pady=(0, 15))
        
        # ===== SEARCH AND ACTION BAR =====
        action_frame = tk.Frame(content, bg=self.colors["background"])
        action_frame.pack(fill=tk.X, padx=20, pady=(0, 15))

        # Search bar (persistent at top)
        self.search_var = tk.StringVar()
        search_container = tk.Frame(action_frame, bg=self.colors["header_bg"],
                       highlightthickness=1, highlightbackground=self.colors["border"])
        search_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        search_icon = tk.Label(search_container, text="Search", font=("Arial", 10),
                      bg=self.colors["header_bg"], fg=self.colors["text_light"])
        search_icon.pack(side=tk.LEFT, padx=10, pady=8)

        self.search_entry = tk.Entry(search_container, textvariable=self.search_var,
                       font=("Arial", 10), border=0, bg=self.colors["header_bg"],
                       fg=self.colors["text_dark"])
        self.search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=8)
        self.search_entry.insert(0, "Search books...")
        self.search_entry.bind("<FocusIn>", lambda e: self.search_entry.delete(0, tk.END) if self.search_entry.get() == "Search books..." else None)
        self.search_entry.bind("<FocusOut>", lambda e: self.search_entry.insert(0, "Search books...") if self.search_entry.get() == "" else None)
        self.search_var.trace_add("write", self.search_books)

        # New button (Primary action)
        new_btn = tk.Button(action_frame, text="+ New Book", font=("Arial", 10, "bold"),
               bg=self.colors["primary"], fg="white", border=0,
               padx=20, pady=8, command=self.show_new_book_modal)
        new_btn.pack(side=tk.RIGHT)
        new_btn.bind("<Enter>", lambda e: new_btn.config(bg=self.colors["primary_hover"]))
        new_btn.bind("<Leave>", lambda e: new_btn.config(bg=self.colors["primary"]))

        # ===== INLINE ADD FORM =====
        self.inline_frame = tk.Frame(content, bg=self.colors["background"])
        # create but hide by default; will be shown when + New Book is clicked
        self.inline_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        self.inline_frame.pack_forget()

        # (Persistent top search already present in the header area)
        # Inline frame will only contain the add form fields; search is kept at top for consistency

        # Compact labels + entries for quick add
        tk.Label(self.inline_frame, text="Title:", bg=self.colors["background"], fg=self.colors["text_dark"]).pack(side=tk.LEFT, padx=(0,6))
        self.form_title = tk.Entry(self.inline_frame, font=("Arial", 10))
        self.form_title.pack(side=tk.LEFT, padx=(0,12))

        tk.Label(self.inline_frame, text="Author:", bg=self.colors["background"], fg=self.colors["text_dark"]).pack(side=tk.LEFT, padx=(0,6))
        self.form_author = tk.Entry(self.inline_frame, font=("Arial", 10))
        self.form_author.pack(side=tk.LEFT, padx=(0,12))

        tk.Label(self.inline_frame, text="Year:", bg=self.colors["background"], fg=self.colors["text_dark"]).pack(side=tk.LEFT, padx=(0,6))
        self.form_year = tk.Entry(self.inline_frame, font=("Arial", 10), width=8)
        self.form_year.pack(side=tk.LEFT, padx=(0,12))

        tk.Label(self.inline_frame, text="Category:", bg=self.colors["background"], fg=self.colors["text_dark"]).pack(side=tk.LEFT, padx=(0,6))
        self.form_category = ttk.Combobox(self.inline_frame, values=["Novel", "Philosophy", "Poetry"], state="readonly", width=14)
        self.form_category.set("Novel")
        self.form_category.pack(side=tk.LEFT, padx=(0,12))

        add_inline_btn = tk.Button(self.inline_frame, text="Add", bg=self.colors["primary"], fg="white", border=0, padx=12, command=self.add_book_from_form)
        add_inline_btn.pack(side=tk.LEFT, padx=(6,4))

        clear_inline_btn = tk.Button(self.inline_frame, text="Clear", bg="#bdc3c7", fg="white", border=0, padx=12, command=self.clear_form)
        clear_inline_btn.pack(side=tk.LEFT)

        # Save and Delete buttons in the New Book inline area (persist and remove in same place)
        save_inline_btn = tk.Button(self.inline_frame, text="Save", bg="#2ecc71", fg="white", border=0, padx=12, command=self.save_book_from_form)
        save_inline_btn.pack(side=tk.LEFT, padx=(8,4))

        delete_inline_btn = tk.Button(self.inline_frame, text="Delete", bg="#e74c3c", fg="white", border=0, padx=12, command=self.delete_book_from_form)
        delete_inline_btn.pack(side=tk.LEFT)
        
        # ===== FILTER AND SORT BAR =====
        filter_frame = tk.Frame(content, bg=self.colors["background"])
        filter_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Category selector
        self.category_var_filter = tk.StringVar(value="All")
        category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var_filter,
                          values=["All", "Novel", "Philosophy", "Poetry"],
                          state="readonly", font=("Arial", 9))
        category_combo.pack(side=tk.LEFT, padx=(0, 10))
        category_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_by_sidebar(self.category_var_filter.get()))

        self.sort_var = tk.StringVar(value="Newest First")
        sort_combo = ttk.Combobox(filter_frame, textvariable=self.sort_var,
                      values=["Newest First", "Oldest First"],
                      state="readonly", font=("Arial", 9), width=14)
        sort_combo.pack(side=tk.LEFT, padx=(0, 10))
        sort_combo.bind("<<ComboboxSelected>>", self.sort_by_selection)
        
        # Book counter
        self.counter_label = tk.Label(filter_frame, text="", font=("Arial", 9, "bold"),
                                     fg=self.colors["text_light"], bg=self.colors["background"])
        self.counter_label.pack(side=tk.RIGHT)
        
        # ===== TABLE/TREEVIEW =====
        table_frame = tk.Frame(content, bg=self.colors["header_bg"], highlightthickness=0)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create Treeview with modern styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background=self.colors["header_bg"],
                       foreground=self.colors["text_dark"], rowheight=35,
                       fieldbackground=self.colors["header_bg"], borderwidth=0)
        style.configure("Treeview.Heading", background=self.colors["background"],
                       foreground=self.colors["text_dark"], borderwidth=0)
        style.map('Treeview', background=[('selected', '#e8f5e9')])
        
        columns = ("Title", "Author", "Year", "Category")
        self.tree = ttk.Treeview(table_frame, columns=columns, height=15, show="headings")
        
        # Configure columns
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Category", text="Category")
        
        self.tree.column("Title", width=350, anchor=tk.W)
        self.tree.column("Author", width=250, anchor=tk.W)
        self.tree.column("Year", width=100, anchor=tk.CENTER)
        self.tree.column("Category", width=120, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right-click context menu
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        # ===== BOTTOM ACTION BAR =====
        bottom_bar = tk.Frame(content, bg=self.colors["background"])
        bottom_bar.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Action buttons
        edit_btn = tk.Button(bottom_bar, text="Edit", font=("Arial", 10),
                            bg="#3498db", fg="white", border=0, padx=15, pady=6,
                            command=self.edit_selected)
        edit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        delete_btn = tk.Button(bottom_bar, text="Delete", font=("Arial", 10),
                              bg="#e74c3c", fg="white", border=0, padx=15, pady=6,
                              command=self.delete_selected)
        delete_btn.pack(side=tk.LEFT)
        
        # Save button
        save_btn = tk.Button(bottom_bar, text="Save", font=("Arial", 10),
                             bg="#2ecc71", fg="white", border=0, padx=15, pady=6,
                             command=self.save_now)
        save_btn.pack(side=tk.LEFT, padx=(10, 0))

        # Status info
        self.status_label = tk.Label(bottom_bar, text="Ready", font=("Arial", 9),
                                    fg=self.colors["text_light"], bg=self.colors["background"])
        self.status_label.pack(side=tk.RIGHT)
        
        self.update_counter()
    
    def load_books(self):
        """Load books into the treeview"""
        books = self.book_manager.get_all_books()
        self.refresh_tree(books)
    
    def refresh_tree(self, books_list):
        """Refresh the treeview with a list of books"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for book in books_list:
            self.tree.insert("", tk.END, values=(
                book["name"], 
                book["author"], 
                book["date"],
                book.get("category", "Novel")
            ))
    
    def filter_by_sidebar(self, category):
        """Filter books by sidebar category"""
        if category == "All":
            books = self.book_manager.get_all_books()
            self.refresh_tree(books)
        else:
            filtered = self.book_manager.filter_by_category(category)
            self.refresh_tree(filtered)
        self.status_label.config(text="Filtered by: {}".format(category))
    
    def search_books(self, *args):
        """Search books by name"""
        try:
            search_term = self.search_var.get()
            if search_term and search_term != "Search books...":
                filtered = self.book_manager.search_by_name(search_term)
                self.refresh_tree(filtered)
                self.status_label.config(text="Search: {} results".format(len(filtered)))
            else:
                books = self.book_manager.get_all_books()
                self.refresh_tree(books)
                self.status_label.config(text="Ready")
        except tk.TclError:
            pass
    
    def sort_by_selection(self, event=None):
        """Sort books based on selection in sort combobox"""
        choice = self.sort_var.get()
        if choice == "Newest First":
            sorted_books = self.book_manager.sort_by_date(descending=True)
            self.status_label.config(text="Sorted by year (newest first)")
        else:
            sorted_books = self.book_manager.sort_by_date(descending=False)
            self.status_label.config(text="Sorted by year (oldest first)")

        cat = self.category_var_filter.get() if hasattr(self, 'category_var_filter') else "All"
        if cat and cat != "All":
            filtered = [b for b in sorted_books if b.get("category") == cat]
            self.refresh_tree(filtered)
        else:
            self.refresh_tree(sorted_books)
    
    def show_new_book_dialog(self):
        """Show dialog to add a new book using simple dialogs"""
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
        
        book = {
            "name": title.strip(),
            "author": author.strip(),
            "date": year.strip(),
            "category": category.strip()
        }
        
        success = self.book_manager.add_book(book)
        if success:
            self.storage.load_data()
            self.load_books()
            self.update_counter()
            self.status_label.config(text="Added: {}".format(title))
            messagebox.showinfo("Success", "Book '{}' added successfully!".format(title))
        else:
            messagebox.showerror("Error", "Failed to add book")

    def add_book_from_form(self):
        """Add a book using the inline form fields"""
        try:
            name = self.form_title.get().strip()
            author = self.form_author.get().strip()
            year = self.form_year.get().strip()
            category = self.form_category.get().strip() if hasattr(self, 'form_category') else 'Novel'

            if not name or not author or not year:
                messagebox.showerror("Error", "Please fill Title, Author and Year")
                return

            new_book = {"name": name, "author": author, "date": year, "category": category}
            success = self.book_manager.add_book(new_book)
            if success:
                self.storage.load_data()
                self.load_books()
                self.update_counter()
                self.status_label.config(text="Added: {}".format(name))
                messagebox.showinfo("Success", "Book '{}' added!".format(name))
                # After adding, populate the top search and focus it so the new book is visible
                try:
                    self.search_var.set(name)
                    self.search_entry.focus()
                    # Trigger search to filter to the newly added book
                    self.search_books()
                except Exception:
                    pass
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to add book")
        except Exception as e:
            messagebox.showerror("Error", "Error adding book: {}".format(e))

    def clear_form(self):
        """Clear inline add form fields"""
        try:
            self.form_title.delete(0, tk.END)
            self.form_author.delete(0, tk.END)
            self.form_year.delete(0, tk.END)
            if hasattr(self, 'form_category'):
                self.form_category.set('Novel')
        except Exception:
            pass

    def toggle_inline_form(self):
        """Show or hide the inline add form placed under the New Book area"""
        try:
            if hasattr(self, 'inline_frame'):
                if self.inline_frame.winfo_manager():
                    # currently packed/visible -> hide
                    self.inline_frame.pack_forget()
                    self.status_label.config(text="Ready")
                else:
                    # not visible -> show and focus the title entry
                    # insert it just below the action/filter area (it was created in create_ui)
                    self.inline_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
                    try:
                        self.form_title.focus()
                    except Exception:
                        pass
        except Exception as e:
            print("toggle_inline_form error:", e)

    def show_new_book_modal(self):
        """Open a modal dialog for New Book add/update/delete with fields and action buttons."""
        try:
            modal = tk.Toplevel(self.root)
            modal.title("New Book")
            modal.transient(self.root)
            modal.grab_set()
            modal.geometry("520x220")

            # Center modal relative to root
            try:
                x = self.root.winfo_rootx() + (self.root.winfo_width() // 2) - 260
                y = self.root.winfo_rooty() + (self.root.winfo_height() // 2) - 110
                modal.geometry(f"+{x}+{y}")
            except Exception:
                pass

            frame = tk.Frame(modal, bg=self.colors["header_bg"], padx=12, pady=12)
            frame.pack(fill=tk.BOTH, expand=True)

            # Title
            tk.Label(frame, text="Title:", bg=self.colors["header_bg"], fg=self.colors["text_dark"]).grid(row=0, column=0, sticky=tk.W, pady=(0,6))
            title_entry = tk.Entry(frame, font=("Arial", 10), width=40)
            title_entry.grid(row=0, column=1, columnspan=3, sticky=tk.W)

            # Author
            tk.Label(frame, text="Author:", bg=self.colors["header_bg"], fg=self.colors["text_dark"]).grid(row=1, column=0, sticky=tk.W, pady=(8,6))
            author_entry = tk.Entry(frame, font=("Arial", 10), width=30)
            author_entry.grid(row=1, column=1, sticky=tk.W)

            # Year
            tk.Label(frame, text="Year:", bg=self.colors["header_bg"], fg=self.colors["text_dark"]).grid(row=1, column=2, sticky=tk.W, padx=(8,0))
            year_entry = tk.Entry(frame, font=("Arial", 10), width=10)
            year_entry.grid(row=1, column=3, sticky=tk.W)

            # Category
            tk.Label(frame, text="Category:", bg=self.colors["header_bg"], fg=self.colors["text_dark"]).grid(row=2, column=0, sticky=tk.W, pady=(8,6))
            category_select = ttk.Combobox(frame, values=["Novel", "Philosophy", "Poetry"], state="readonly", width=20)
            category_select.set("Novel")
            category_select.grid(row=2, column=1, sticky=tk.W)

            # Action buttons
            def _add():
                t = title_entry.get().strip()
                a = author_entry.get().strip()
                y = year_entry.get().strip()
                c = category_select.get().strip() or 'Novel'
                if not t or not a or not y:
                    messagebox.showerror("Error", "Please fill Title, Author and Year")
                    return
                new_book = {"name": t, "author": a, "date": y, "category": c}
                if self.book_manager.add_book(new_book):
                    self.storage.load_data()
                    self.load_books()
                    self.update_counter()
                    self.status_label.config(text="Added: {}".format(t))
                    messagebox.showinfo("Success", "Book '{}' added!".format(t))
                    try:
                        self.search_var.set(t)
                        self.search_entry.focus()
                        self.search_books()
                    except Exception:
                        pass
                else:
                    messagebox.showerror("Error", "Failed to add book")

            def _save():
                t = title_entry.get().strip()
                a = author_entry.get().strip()
                y = year_entry.get().strip()
                c = category_select.get().strip() or 'Novel'
                if not t or not a or not y:
                    messagebox.showwarning("Warning", "Please fill Title, Author and Year before saving")
                    return
                existing = self.book_manager.find_book(t)
                book_obj = {"name": t, "author": a, "date": y, "category": c}
                if existing:
                    if self.book_manager.update_book(t, book_obj):
                        self.storage.load_data()
                        self.load_books()
                        self.update_counter()
                        self.status_label.config(text="Updated: {}".format(t))
                        messagebox.showinfo("Saved", "Updated '{}'".format(t))
                else:
                    if self.book_manager.add_book(book_obj):
                        self.storage.load_data()
                        self.load_books()
                        self.update_counter()
                        self.status_label.config(text="Added: {}".format(t))
                        messagebox.showinfo("Saved", "Added '{}'".format(t))
                try:
                    self.storage.save_data()
                except Exception:
                    pass
                try:
                    self.search_var.set(t)
                    self.search_entry.focus()
                    self.search_books()
                except Exception:
                    pass

            def _delete():
                t = title_entry.get().strip()
                if not t:
                    messagebox.showwarning("Warning", "Enter the Title of the book to delete")
                    return
                if not messagebox.askyesno("Confirm", "Delete '{}' from library?".format(t)):
                    return
                if self.book_manager.delete_book(t):
                    self.storage.load_data()
                    self.load_books()
                    self.update_counter()
                    self.status_label.config(text="Deleted: {}".format(t))
                    messagebox.showinfo("Success", "Book deleted!")
                    try:
                        self.search_var.set("")
                        self.search_entry.focus()
                    except Exception:
                        pass
                    title_entry.delete(0, tk.END)
                    author_entry.delete(0, tk.END)
                    year_entry.delete(0, tk.END)
                    category_select.set('Novel')
                else:
                    messagebox.showerror("Error", "Book '{}' not found or delete failed".format(t))

            def _clear():
                title_entry.delete(0, tk.END)
                author_entry.delete(0, tk.END)
                year_entry.delete(0, tk.END)
                category_select.set('Novel')

            btn_frame = tk.Frame(frame, bg=self.colors["header_bg"], pady=8)
            btn_frame.grid(row=3, column=0, columnspan=4)
            add_btn = tk.Button(btn_frame, text="Add", bg=self.colors["primary"], fg="white", command=_add)
            add_btn.pack(side=tk.LEFT, padx=6)
            save_btn = tk.Button(btn_frame, text="Save", bg="#2ecc71", fg="white", command=_save)
            save_btn.pack(side=tk.LEFT, padx=6)
            delete_btn = tk.Button(btn_frame, text="Delete", bg="#e74c3c", fg="white", command=_delete)
            delete_btn.pack(side=tk.LEFT, padx=6)
            clear_btn = tk.Button(btn_frame, text="Clear", bg="#bdc3c7", fg="white", command=_clear)
            clear_btn.pack(side=tk.LEFT, padx=6)

            # Pre-fill inline form if user had it open and values present
            try:
                if hasattr(self, 'form_title') and self.form_title.get().strip():
                    title_entry.insert(0, self.form_title.get().strip())
                if hasattr(self, 'form_author') and self.form_author.get().strip():
                    author_entry.insert(0, self.form_author.get().strip())
                if hasattr(self, 'form_year') and self.form_year.get().strip():
                    year_entry.insert(0, self.form_year.get().strip())
                if hasattr(self, 'form_category') and self.form_category.get().strip():
                    category_select.set(self.form_category.get().strip())
            except Exception:
                pass

            # Bind Enter key to Save for convenience
            modal.bind('<Return>', lambda e: _save())

        except Exception as e:
            print("show_new_book_modal error:", e)
    
    def delete_selected(self):
        """Delete the selected book"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return
        
        item = selected[0]
        values = self.tree.item(item)["values"]
        book_name = values[0]
        
        if messagebox.askyesno("Confirm", "Delete '{}'?".format(book_name)):
            success = self.book_manager.delete_book(book_name)
            if success:
                self.storage.load_data()
                self.load_books()
                self.update_counter()
                self.status_label.config(text="Deleted: {}".format(book_name))
                messagebox.showinfo("Success", "Book deleted!")
            else:
                messagebox.showerror("Error", "Failed to delete book")

    def delete_book_from_form(self):
        """Delete the book named in the inline form (if present in storage)"""
        try:
            title = self.form_title.get().strip()
            if not title:
                messagebox.showwarning("Warning", "Enter the Title of the book to delete")
                return
            if not messagebox.askyesno("Confirm", "Delete '{}' from library?".format(title)):
                return
            success = self.book_manager.delete_book(title)
            if success:
                self.storage.load_data()
                self.load_books()
                self.update_counter()
                self.status_label.config(text="Deleted: {}".format(title))
                messagebox.showinfo("Success", "Book deleted!")
                self.clear_form()
            else:
                messagebox.showerror("Error", "Book '{}' not found or delete failed".format(title))
        except Exception as e:
            messagebox.showerror("Error", "Error deleting book: {}".format(e))

    def save_book_from_form(self):
        """Explicit save action for the inline form – ensures storage flushed to disk and shows success"""
        try:
            title = self.form_title.get().strip()
            author = self.form_author.get().strip()
            year = self.form_year.get().strip()
            category = self.form_category.get().strip() if hasattr(self, 'form_category') else 'Novel'

            if not title or not author or not year:
                messagebox.showwarning("Warning", "Please fill Title, Author and Year before saving")
                return

            existing = self.book_manager.find_book(title)
            book_obj = {"name": title, "author": author, "date": year, "category": category}

            if existing:
                # Update existing book
                updated = self.book_manager.update_book(title, book_obj)
                if updated:
                    self.storage.load_data()
                    self.load_books()
                    self.update_counter()
                    self.status_label.config(text="Updated: {}".format(title))
                    messagebox.showinfo("Saved", "Updated '{}'".format(title))
                else:
                    messagebox.showerror("Error", "Failed to update '{}'".format(title))
            else:
                # Add as new
                added = self.book_manager.add_book(book_obj)
                if added:
                    self.storage.load_data()
                    self.load_books()
                    self.update_counter()
                    self.status_label.config(text="Added: {}".format(title))
                    messagebox.showinfo("Saved", "Added '{}'".format(title))
                else:
                    messagebox.showerror("Error", "Failed to add '{}'".format(title))

            # Persist to disk explicitly and focus search to show the book
            try:
                self.storage.save_data()
            except Exception:
                pass
            try:
                self.search_var.set(title)
                self.search_entry.focus()
                self.search_books()
            except Exception:
                pass

        except Exception as e:
            self.status_label.config(text="Save error")
            messagebox.showerror("Save Error", "Error saving/updating: {}".format(e))
    
    def edit_selected(self):
        """Edit the selected book"""
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
        
        updated_book = {
            "name": title.strip(),
            "author": author.strip(),
            "date": year.strip(),
            "category": category.strip()
        }
        
        success = self.book_manager.update_book(old_title, updated_book)
        if success:
            self.storage.load_data()
            self.load_books()
            self.update_counter()
            self.status_label.config(text="Updated: {}".format(title))
            messagebox.showinfo("Success", "Book updated!")
        else:
            messagebox.showerror("Error", "Failed to update book")
    
    def update_counter(self):
        """Update the book counter display"""
        stats = self.book_manager.get_statistics()
        counter_text = "Total: {} | Novels: {} | Philosophy: {} | Poetry: {}".format(
            stats['total'], stats['novels'], stats['philosophy'], stats['poetry'])
        self.counter_label.config(text=counter_text)
    
    def save_now(self):
        """Explicitly save current storage to disk"""
        try:
            saved = self.storage.save_data()
            if saved:
                self.status_label.config(text="Saved")
                messagebox.showinfo("Save", "Library saved to disk.")
            else:
                self.status_label.config(text="Save failed")
                messagebox.showerror("Save Error", "Failed to save library to disk.")
        except Exception as e:
            self.status_label.config(text="Save error")
            messagebox.showerror("Save Error", "Error saving: {}".format(e))
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        item = self.tree.selection()
        if item:
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Edit", command=self.edit_selected)
            menu.add_command(label="Delete", command=self.delete_selected)
            menu.post(event.x_root, event.y_root)


LibraryGUI = ModernLibraryGUI
