"""
Backend Module - Business logic for book management
"""


class BookManager:
    """Handle book operations: filter, search, sort, add, delete, edit"""
    
    def __init__(self, storage):
        """Initialize with storage object"""
        self.storage = storage
    
    def get_all_books(self):
        """Return all books"""
        return self.storage.get_books()
    
    def filter_by_category(self, category):
        """Filter books by category"""
        books = self.storage.get_books()
        if category == "All":
            return books
        return [b for b in books if b.get("category") == category]
    
    def search_by_name(self, search_term):
        """Search books by name"""
        books = self.storage.get_books()
        if not search_term:
            return books
        search_lower = search_term.lower()
        return [b for b in books if search_lower in b["name"].lower()]
    
    def sort_by_date(self, descending=True):
        """Sort books by date (year)"""
        books = self.storage.get_books()
        # Handle years stored as strings; fall back to 0 for invalid/missing
        def year_key(x):
            try:
                return int(x.get("date") or 0)
            except Exception:
                return 0
        return sorted(books, key=year_key, reverse=descending)
    
    def add_book(self, book):
        """Add a new book"""
        if book and "name" in book and "author" in book and "date" in book:
            books = self.storage.get_books()
            books.append(book)
            self.storage.set_books(books)
            # Persist immediately
            try:
                self.storage.save_data()
            except Exception:
                pass
            return True
        return False
    
    def delete_book(self, book_name):
        """Delete a book by name"""
        books = self.storage.get_books()
        initial_count = len(books)
        filtered_books = [b for b in books if b["name"] != book_name]
        self.storage.set_books(filtered_books)
        # Persist immediately
        try:
            self.storage.save_data()
        except Exception:
            pass
        return len(filtered_books) < initial_count
    
    def find_book(self, book_name):
        """Find a book by name"""
        books = self.storage.get_books()
        for book in books:
            if book["name"] == book_name:
                return book
        return None
    
    def update_book(self, book_name, updated_book):
        """Update a book by name"""
        books = self.storage.get_books()
        for i, book in enumerate(books):
            if book["name"] == book_name:
                # If name changed, delete old entry and add new one to avoid duplicates
                if book_name != updated_book.get("name"):
                    # Remove old by name
                    books = [b for b in books if b["name"] != book_name]
                    # Add updated
                    books.append(updated_book)
                else:
                    # Name same, just update in place
                    books[i] = updated_book
                
                self.storage.set_books(books)
                # Persist immediately
                try:
                    self.storage.save_data()
                except Exception:
                    pass
                return True
        return False
    
    def get_statistics(self):
        """Get book statistics"""
        books = self.storage.get_books()
        total = len(books)
        novels = len([b for b in books if b.get("category") == "Novel"])
        philosophy = len([b for b in books if b.get("category") == "Philosophy"])
        poetry = len([b for b in books if b.get("category") == "Poetry"])
        
        return {
            "total": total,
            "novels": novels,
            "philosophy": philosophy,
            "poetry": poetry
        }
