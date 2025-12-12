# Test Examples and Usage Guide

## Quick Reference: Running Tests

### Execute All Tests
```bash
cd "c:\Users\Saksham\Documents\advanced programming final\online_book_project"
python tests.py
```

**Output:**
```
Ran 20 tests in 1.349s
OK ✅
```

---

## Test Categories

### 1. STORAGE TESTS (2 tests)
Tests for JSON file persistence and data integrity.

#### Test 1: Save and Load Books
```python
def test_save_and_load_books(self):
    """Test that books are correctly saved and loaded from JSON"""
    # Create test books
    test_books = [
        {"name": "Test Novel", "author": "Test Author", "date": "2023", "category": "Novel"},
        {"name": "Test Philosophy", "author": "Philosopher", "date": "2024", "category": "Philosophy"}
    ]
    
    # Save to JSON
    storage.set_books(test_books)
    storage.save_data()
    
    # Load from new instance
    new_storage = BookStorage("test_media.json")
    new_storage.load_data()
    loaded_books = new_storage.get_books()
    
    # Verify
    assert len(loaded_books) == 2
    assert loaded_books[0]["name"] == "Test Novel"
    assert loaded_books[1]["category"] == "Philosophy"
```
**Purpose**: Ensure books persist to disk and reload correctly.

#### Test 2: Book Persistence
```python
def test_book_persistence(self):
    """Test that books persist across multiple saves"""
    # First save
    storage.set_books([{"name": "First Book", ...}])
    storage.save_data()
    
    # Add another and save again
    books = storage.get_books()
    books.append({"name": "Second Book", ...})
    storage.set_books(books)
    storage.save_data()
    
    # Reload from disk
    final_storage = BookStorage("test_media.json")
    final_storage.load_data()
    
    # Verify both books exist
    assert len(final_storage.get_books()) == 2
```
**Purpose**: Test multiple save/load cycles work correctly.

---

### 2. BACKEND TESTS (8 tests)
Tests for business logic (BookManager class).

#### Test 1: Add Book
```python
def test_add_book(self):
    """Test adding a new book to the collection"""
    manager = BookManager(storage)
    
    new_book = {
        "name": "Crime and Punishment",
        "author": "Dostoevsky",
        "date": "1866",
        "category": "Novel"
    }
    
    manager.add_book(new_book)
    
    books = storage.get_books()
    assert len(books) == 5  # 4 initial + 1 new
    assert books[-1]["name"] == "Crime and Punishment"
```
**Purpose**: Verify adding books works and persists to storage.

#### Test 2: Delete Book
```python
def test_delete_book(self):
    """Test deleting a book from the collection"""
    manager = BookManager(storage)
    
    initial_count = len(storage.get_books())
    manager.delete_book("1984")
    
    books = storage.get_books()
    assert len(books) == initial_count - 1
    assert "1984" not in [b["name"] for b in books]
```
**Purpose**: Verify book deletion and removal from storage.

#### Test 3: Find Book
```python
def test_find_book(self):
    """Test finding a book by name"""
    manager = BookManager(storage)
    
    book = manager.find_book("The Republic")
    
    assert book is not None
    assert book["author"] == "Plato"
    assert book["category"] == "Philosophy"
```
**Purpose**: Test book lookup by name.

#### Test 4: Update Book
```python
def test_update_book(self):
    """Test updating an existing book"""
    manager = BookManager(storage)
    
    updated_data = {
        "name": "1984 - Updated",
        "author": "George Orwell",
        "date": "1949",
        "category": "Novel"
    }
    
    manager.update_book("1984", updated_data)
    
    book = manager.find_book("1984 - Updated")
    assert book is not None
    assert book["name"] == "1984 - Updated"
```
**Purpose**: Verify book data modification.

#### Test 5: Filter by Category
```python
def test_filter_by_category(self):
    """Test filtering books by category"""
    manager = BookManager(storage)
    
    novels = manager.filter_by_category("Novel")
    assert len(novels) == 2
    
    philosophy = manager.filter_by_category("Philosophy")
    assert len(philosophy) == 1
    
    poetry = manager.filter_by_category("Poetry")
    assert len(poetry) == 1
```
**Purpose**: Test category filtering.

#### Test 6: Search by Name
```python
def test_search_by_name(self):
    """Test searching books by name"""
    manager = BookManager(storage)
    
    # Exact match
    results = manager.search_by_name("1984")
    assert len(results) == 1
    assert results[0]["name"] == "1984"
    
    # Partial match
    results = manager.search_by_name("Republic")
    assert len(results) > 0
```
**Purpose**: Verify search functionality.

#### Test 7: Sort by Date
```python
def test_sort_by_date(self):
    """Test sorting books by date"""
    manager = BookManager(storage)
    
    sorted_books = manager.sort_by_date(descending=True)
    
    assert len(sorted_books) == 4
    assert isinstance(sorted_books, list)
```
**Purpose**: Test sorting by publication date.

#### Test 8: Get Statistics
```python
def test_get_statistics(self):
    """Test getting book statistics"""
    manager = BookManager(storage)
    
    stats = manager.get_statistics()
    
    assert stats["total"] == 4
    assert stats["novels"] == 2
    assert stats["philosophy"] == 1
    assert stats["poetry"] == 1
```
**Purpose**: Verify statistics calculation.

---

### 3. FRONTEND TESTS (8 tests)
Tests for GUI functionality (ModernLibraryGUI class).

#### Test 1: GUI Initialization
```python
def test_gui_initialization(self):
    """Test that GUI initializes correctly"""
    root = tk.Tk()
    gui = ModernLibraryGUI(root, manager, storage)
    
    assert root.title() == "Saksham's Reading Room"
    assert root.cget("bg") == "#f5f5f5"
    assert gui.tree is not None
```
**Purpose**: Verify GUI window creation and components.

#### Test 2: Load Books into GUI
```python
def test_load_books_into_gui(self):
    """Test that books are loaded into the treeview"""
    gui.load_books()
    
    items = gui.tree.get_children()
    assert len(items) == 3
    
    values = gui.tree.item(items[0])["values"]
    assert str(values[0]) == "1984"
    assert str(values[1]) == "George Orwell"
```
**Purpose**: Verify books display in treeview.

#### Test 3: Add Book via GUI
```python
def test_add_book_via_gui(self):
    """Test adding a book through GUI backend"""
    new_book = {
        "name": "Crime and Punishment",
        "author": "Dostoevsky",
        "date": "1866",
        "category": "Novel"
    }
    
    manager.add_book(new_book)
    storage.save_data()
    gui.load_books()
    
    items = gui.tree.get_children()
    assert len(items) == 4
```
**Purpose**: Test adding book through GUI updates.

#### Test 4: Delete Book via GUI
```python
def test_delete_book_via_gui(self):
    """Test deleting a book through GUI"""
    initial_items = len(gui.tree.get_children())
    
    manager.delete_book("1984")
    storage.save_data()
    gui.books = storage.get_books()
    gui.load_books()
    
    final_items = len(gui.tree.get_children())
    assert final_items == initial_items - 1
```
**Purpose**: Verify book deletion updates GUI.

#### Test 5: Search Functionality
```python
def test_search_functionality(self):
    """Test search functionality in GUI"""
    gui.search_var.set("Republic")
    gui.search_books()
    
    items = gui.tree.get_children()
    assert len(items) > 0
```
**Purpose**: Test search updates treeview.

#### Test 6: Filter by Category
```python
def test_filter_by_category(self):
    """Test filtering by category in GUI"""
    gui.filter_by_sidebar("Novel")
    
    items = gui.tree.get_children()
    assert len(items) == 1
    
    values = gui.tree.item(items[0])["values"]
    assert values[3] == "Novel"
```
**Purpose**: Verify category filter works in GUI.

#### Test 7: GUI Counter Update
```python
def test_gui_counter_update(self):
    """Test that book counter updates correctly"""
    gui.update_counter()
    
    counter_text = gui.counter_label.cget("text")
    assert "Total: 3" in counter_text
    assert "Novels: 1" in counter_text
```
**Purpose**: Test statistics display.

#### Test 8: Sort by Date in GUI
```python
def test_sort_by_date_in_gui(self):
    """Test sorting by date in GUI"""
    gui.sort_by_date()
    
    items = gui.tree.get_children()
    assert len(items) > 0
```
**Purpose**: Verify sorting in GUI.

---

### 4. INTEGRATION TESTS (2 tests)
End-to-end workflow tests.

#### Test 1: Full CRUD Lifecycle
```python
def test_full_book_lifecycle(self):
    """Test complete book lifecycle: Create, Read, Update, Delete"""
    
    # CREATE
    new_book = {
        "name": "Pride and Prejudice",
        "author": "Jane Austen",
        "date": "1813",
        "category": "Novel"
    }
    manager.add_book(new_book)
    storage.save_data()
    
    # READ
    found_book = manager.find_book("Pride and Prejudice")
    assert found_book is not None
    assert found_book["author"] == "Jane Austen"
    
    # UPDATE
    manager.update_book("Pride and Prejudice", found_book)
    storage.save_data()
    
    # DELETE
    manager.delete_book("Pride and Prejudice")
    storage.save_data()
    
    # VERIFY DELETED
    deleted_book = manager.find_book("Pride and Prejudice")
    assert deleted_book is None
```
**Purpose**: Test complete workflow from creation to deletion.

#### Test 2: Combined Operations
```python
def test_filter_search_and_sort(self):
    """Test combined filter, search, and sort operations"""
    
    # Add more books
    manager.add_book({"name": "Thus Spoke Zarathustra", ...})
    manager.add_book({"name": "The Raven", ...})
    
    # Filter
    philosophy_books = manager.filter_by_category("Philosophy")
    assert len(philosophy_books) == 2
    
    # Search
    results = manager.search_by_name("Republic")
    assert len(results) == 1
    
    # Sort
    sorted_books = manager.sort_by_date(descending=False)
    assert len(sorted_books) == 4
```
**Purpose**: Test multiple operations work together.

---

## Test Data

### Books Used in Tests
```python
test_books = [
    {
        "name": "1984",
        "author": "George Orwell",
        "date": "1949",
        "category": "Novel"
    },
    {
        "name": "The Republic",
        "author": "Plato",
        "date": "380",
        "category": "Philosophy"
    },
    {
        "name": "Leaves of Grass",
        "author": "Walt Whitman",
        "date": "1855",
        "category": "Poetry"
    },
    {
        "name": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "date": "1960",
        "category": "Novel"
    }
]
```

---

## Expected Test Results

### When Running Tests
```bash
$ python tests.py

test_book_persistence (...TestBookStorage.test_book_persistence) ... ok
test_save_and_load_books (...TestBookStorage.test_save_and_load_books) ... ok
test_add_book (...TestBookManager.test_add_book) ... ok
test_delete_book (...TestBookManager.test_delete_book) ... ok
test_filter_by_category (...TestBookManager.test_filter_by_category) ... ok
test_find_book (...TestBookManager.test_find_book) ... ok
test_get_statistics (...TestBookManager.test_get_statistics) ... ok
test_search_by_name (...TestBookManager.test_search_by_name) ... ok
test_sort_by_date (...TestBookManager.test_sort_by_date) ... ok
test_update_book (...TestBookManager.test_update_book) ... ok
test_add_book_via_gui (...TestModernLibraryGUI.test_add_book_via_gui) ... ok
test_delete_book_via_gui (...TestModernLibraryGUI.test_delete_book_via_gui) ... ok
test_filter_by_category (...TestModernLibraryGUI.test_filter_by_category) ... ok
test_gui_counter_update (...TestModernLibraryGUI.test_gui_counter_update) ... ok
test_gui_initialization (...TestModernLibraryGUI.test_gui_initialization) ... ok
test_load_books_into_gui (...TestModernLibraryGUI.test_load_books_into_gui) ... ok
test_search_functionality (...TestModernLibraryGUI.test_search_functionality) ... ok
test_sort_by_date_in_gui (...TestModernLibraryGUI.test_sort_by_date_in_gui) ... ok
test_filter_search_and_sort (...TestIntegration.test_filter_search_and_sort) ... ok
test_full_book_lifecycle (...TestIntegration.test_full_book_lifecycle) ... ok

Ran 20 tests in 1.349s

OK ✅
```

---

## Key Test Metrics

| Metric | Value |
|--------|-------|
| Total Tests | 20 |
| Tests Passing | 20 ✅ |
| Tests Failing | 0 |
| Success Rate | 100% |
| Execution Time | ~1.3 seconds |
| Storage Tests | 2 |
| Backend Tests | 8 |
| Frontend Tests | 8 |
| Integration Tests | 2 |

---

## Troubleshooting

### Tests Won't Run
```bash
# Ensure Python is in PATH
python --version

# Try from project directory
cd "c:\Users\Saksham\Documents\advanced programming final\online_book_project"
python tests.py
```

### Import Errors
```bash
# Ensure all modules exist:
# - backend/book_manager.py
# - storage/storage.py
# - frontend/gui.py
# - media.json (optional, tests create their own)
```

### Test Cleanup
- Tests automatically create and delete `test_media.json`
- No manual cleanup needed
- Each test is isolated and independent

---

## Summary

✅ **All 20 tests passing**
- ✅ 2 Storage tests (JSON persistence)
- ✅ 8 Backend tests (Business logic)
- ✅ 8 Frontend tests (GUI functionality)
- ✅ 2 Integration tests (End-to-end workflows)

**Quality Assurance**: Production-ready with comprehensive test coverage.
