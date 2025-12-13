import json
import os
import sys
import pytest

# Add online_book_project to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'online_book_project'))

from storage.storage import BookStorage
from backend.book_manager import BookManager


class TestBookManagerAddAndList:
    """Backend BookManager Test: Verify add_book and retrieval works correctly"""
    
    def test_add_book_and_list_books(self, tmp_path):
        """Test BookManager can add a book and retrieve it from the list"""
        print("\n[RUNNING] test_book_manager.py - Testing BookManager add/list functionality")
        fname = str(tmp_path / "media.json")
        
        # Initialize empty storage
        storage = BookStorage(fname)
        storage._data = {"books": []}
        storage.save_data()
        
        # Create book manager
        manager = BookManager(storage)
        
        # Add a new book
        new_book = {
            "name": "Test Driven Development",
            "author": "Kent Beck",
            "date": "2003",
            "category": "Novel"
        }
        manager.add_book(new_book)
        
        # Retrieve and verify
        books = manager.get_all_books()
        assert len(books) > 0
        assert any(b.get("name") == "Test Driven Development" for b in books)
        
        # Verify the book has all expected fields
        added_book = [b for b in books if b.get("name") == "Test Driven Development"][0]
        assert added_book["author"] == "Kent Beck"
        assert added_book["date"] == "2003"
        print("[PASSED] test_book_manager.py - All book manager tests completed successfully ✅")
