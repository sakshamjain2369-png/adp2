import sys
import os
import time
import json

# Make sure project root is importable
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
sys.path.insert(0, PROJECT_ROOT)

from storage.storage import BookStorage
from backend.book_manager import BookManager

media_path = os.path.join(PROJECT_ROOT, 'media.json')

print(f"Using media.json at: {media_path}")

storage = BookStorage(media_path)
storage.load_data()
manager = BookManager(storage)

initial_books = storage.get_books()
print(f"Initial book count: {len(initial_books)}")

# Create a unique test book
timestamp = int(time.time())
book_name = f"LIVE TEST BOOK {timestamp}"
test_book = {
    "name": book_name,
    "author": "Copilot Test",
    "date": 2025,
    "category": "Test"
}

print(f"Adding test book: {book_name}")
added = manager.add_book(test_book)
# Persist changes
storage.save_data()
print(f"Add returned: {added}")

# Read file to confirm
with open(media_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

found = any(b.get('name') == book_name for b in data)
print(f"Book present after add: {found}")
print(f"Count after add: {len(data)}")

# Allow a short pause for GUI reactions
time.sleep(1)

print(f"Now deleting test book: {book_name}")
deleted = manager.delete_book(book_name)
# Persist changes
storage.save_data()
print(f"Delete returned: {deleted}")

with open(media_path, 'r', encoding='utf-8') as f:
    data_after = json.load(f)

found_after = any(b.get('name') == book_name for b in data_after)
print(f"Book present after delete: {found_after}")
print(f"Count after delete: {len(data_after)}")

print("Live add/delete test completed.")
