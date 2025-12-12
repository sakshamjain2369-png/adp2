import json
import pytest
from storage.storage import BookStorage
from backend.book_manager import BookManager


class TestBookManagerAddAndList:
    """Backend BookManager Test: Verify add_book and retrieval works correctly"""
    
    def test_add_book_and_list_books(self, tmp_path):
        """Test BookManager can add a book and retrieve it from the list"""
        fname = str(tmp_path / "media.json")
        
        # Initialize empty storage
        storage = BookStorage(fname)
        storage._data = {"books": []}
        storage.save_data()
        
        # Create book manager
        manager = BookManager(storage)
        
        # Add a new book
        new_book = {
            "title": "Test Driven Development",
            "author": "Kent Beck",
            "year": 2003,
            "genre": "Technology"
        }
        manager.add_book(new_book)
        
        # Retrieve and verify
        books = manager.get_books()
        assert len(books) > 0
        assert any(b.get("title") == "Test Driven Development" for b in books)
        
        # Verify the book has all expected fields
        added_book = [b for b in books if b.get("title") == "Test Driven Development"][0]
        assert added_book["author"] == "Kent Beck"
        assert added_book["year"] == 2003
