import json
import os
import sys
import tempfile
import pytest

# Add online_book_project to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'online_book_project'))

from storage.storage import BookStorage


class TestBookStorageLoadSave:
    """Backend Storage Test: Verify BookStorage can load and save books correctly"""
    
    def test_load_and_save_books(self, tmp_path):
        """Test that BookStorage can load and save books correctly"""
        print("\n[RUNNING] test_storage.py - Testing BookStorage load/save functionality")
        # Create test JSON with books
        data = [
            {"name": "Ancient Book", "author": "Unknown", "date": "875", "category": "Novel"},
            {"name": "Modern Book", "author": "John Doe", "date": "2020", "category": "Philosophy"},
            {"name": "Victorian Era", "author": "Jane Austen", "date": "1850", "category": "Poetry"}
        ]
        fname = str(tmp_path / "media.json")
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        # Load storage
        storage = BookStorage(fname)
        storage.load_data()
        
        # Verify books loaded
        books = storage.get_books()
        assert len(books) == 3
        assert books[0]["name"] == "Ancient Book"
        assert books[1]["name"] == "Modern Book"
        assert books[2]["name"] == "Victorian Era"
        
        # Add a new book and save
        books.append({"name": "New Book", "author": "Test Author", "date": "2024", "category": "Novel"})
        storage.set_books(books)
        storage.save_data()
        
        # Read back and verify
        with open(fname, "r", encoding="utf-8") as f:
            updated = json.load(f)
        
        assert len(updated) == 4
        assert updated[3]["name"] == "New Book"
        print("[PASSED] test_storage.py - All storage tests completed successfully ✅")
