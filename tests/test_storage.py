import json
import os
import tempfile
import pytest
from storage.storage import BookStorage


class TestBookStorageNormalizesYears:
    """Backend Storage Test: Verify 3-digit years are normalized to 4-digit historic years"""
    
    def test_normalize_and_sort_years(self, tmp_path):
        """Test that 3-digit years (e.g., 875) are converted to 1875 and sorted newest-first"""
        # Create test JSON with mixed year formats
        data = {
            "books": [
                {"title": "Ancient Book", "author": "Unknown", "year": 875},
                {"title": "Modern Book", "author": "John Doe", "year": 2020},
                {"title": "Victorian Era", "author": "Jane Austen", "year": 450}
            ]
        }
        fname = str(tmp_path / "media.json")
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        # Load storage and persist normalized data
        storage = BookStorage(fname)
        storage.load_data()
        storage.save_data()
        
        # Read back and verify
        with open(fname, "r", encoding="utf-8") as f:
            updated = json.load(f)
        
        books = updated["books"]
        # Verify sorting: newest first (2020, 1875, 1450)
        assert books[0]["title"] == "Modern Book"
        assert books[0]["year"] == 2020
        
        assert books[1]["title"] == "Ancient Book"
        assert books[1]["year"] == 1875  # 875 -> 1875
        
        assert books[2]["title"] == "Victorian Era"
        assert books[2]["year"] == 1450  # 450 -> 1450
