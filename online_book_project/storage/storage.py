"""
Storage Module - Handles JSON data persistence for the Online Library
"""
import json
import os


class BookStorage:
    """Handle loading and saving book data to JSON file"""
    
    def __init__(self, data_file="media.json"):
        """Initialize storage with path to data file"""
        # Resolve relative paths to project root so reads/writes are consistent
        if not os.path.isabs(data_file):
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            self.data_file = os.path.join(project_root, data_file)
        else:
            self.data_file = data_file
        self.books = []
    
    def load_data(self):
        """Load books from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.books = json.load(f)
                    return True
            except Exception as e:
                print(f"Error loading data: {e}")
                self.books = []
                return False
        else:
            self.books = []
            return False
    
    def save_data(self):
        """Save books to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.books, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def get_books(self):
        """Return all books"""
        return self.books
    
    def set_books(self, books):
        """Update books list"""
        self.books = books
