"""
Complete end-to-end test: Add, Edit, Delete a book
Simulates exactly what the GUI does
"""
import sys
import os
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from storage.storage import BookStorage
from backend.book_manager import BookManager

print("="*60)
print("COMPLETE ADD/EDIT/DELETE TEST")
print("="*60)

# Initialize
storage = BookStorage("media.json")
storage.load_data()
manager = BookManager(storage)

initial_count = len(storage.get_books())
print("\n[STEP 1] Initial book count: {}".format(initial_count))

# --- ADD ---
print("\n[STEP 2] ADDING NEW BOOK...")
new_book = {
    "name": "The New Adventure",
    "author": "Jane Smith",
    "date": "2024",
    "category": "Novel"
}

add_result = manager.add_book(new_book)
print("  - add_book() returned: {}".format(add_result))

# Reload as GUI does
storage.load_data()
after_add = len(storage.get_books())
print("  - Books after add: {}".format(after_add))
print("  - File contains: {} books".format(after_add))

# Verify it's in the file
with open(storage.data_file, 'r', encoding='utf-8') as f:
    file_data = json.load(f)
found_add = any(b.get('name') == 'The New Adventure' for b in file_data)
if found_add:
    print("  - Found in media.json: YES [OK]")
else:
    print("  - Found in media.json: NO [FAIL]")

# --- EDIT ---
print("\n[STEP 3] EDITING BOOK...")
updated_book = {
    "name": "The Grand Adventure",  # Changed name
    "author": "Jane Smith",
    "date": "2024",
    "category": "Philosophy"  # Changed category
}

edit_result = manager.update_book("The New Adventure", updated_book)
print("  - update_book() returned: {}".format(edit_result))

# Reload as GUI does
storage.load_data()
after_edit = len(storage.get_books())
print("  - Books after edit: {}".format(after_edit))

# Verify the new name is in file
with open(storage.data_file, 'r', encoding='utf-8') as f:
    file_data = json.load(f)
found_new_name = any(b.get('name') == 'The Grand Adventure' for b in file_data)
old_name_gone = not any(b.get('name') == 'The New Adventure' for b in file_data)
if found_new_name:
    print("  - New name in file: YES [OK]")
else:
    print("  - New name in file: NO [FAIL]")
if old_name_gone:
    print("  - Old name removed: YES [OK]")
else:
    print("  - Old name removed: NO [FAIL]")

# --- DELETE ---
print("\n[STEP 4] DELETING BOOK...")
del_result = manager.delete_book("The Grand Adventure")
print("  - delete_book() returned: {}".format(del_result))

# Reload as GUI does
storage.load_data()
after_delete = len(storage.get_books())
print("  - Books after delete: {}".format(after_delete))
if after_delete == initial_count:
    print("  - Back to initial count: YES [OK]")
else:
    print("  - Back to initial count: NO [FAIL]")

# Verify it's gone from file
with open(storage.data_file, 'r', encoding='utf-8') as f:
    file_data = json.load(f)
deleted = not any(b.get('name') == 'The Grand Adventure' for b in file_data)
if deleted:
    print("  - Removed from file: YES [OK]")
else:
    print("  - Removed from file: NO [FAIL]")

print("\n" + "="*60)
if (after_add == initial_count + 1 and 
    after_edit == initial_count + 1 and 
    after_delete == initial_count and
    found_add and found_new_name and old_name_gone and deleted):
    print("ALL TESTS PASSED - Add/Edit/Delete working correctly!")
else:
    print("SOME TESTS FAILED - Check output above")
print("="*60 + "\n")
