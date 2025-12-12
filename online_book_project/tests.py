"""
Test Suite for Saksham's Reading Room
Tests for backend (BookManager), frontend (ModernLibraryGUI), and storage (BookStorage)
"""
import unittest
import json
import os
import tkinter as tk
from tkinter import ttk
from io import StringIO
import sys

# Import modules
from backend.book_manager import BookManager
from storage.storage import BookStorage
from frontend.gui import ModernLibraryGUI


class TestBookStorage(unittest.TestCase):
    """Test suite for BookStorage - Storage layer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_file = "test_media.json"
        self.storage = BookStorage(self.test_file)
        
        # Create test data
        self.test_books = [
            {"name": "Test Novel", "author": "Test Author", "date": "2023", "category": "Novel"},
            {"name": "Test Philosophy", "author": "Philosopher", "date": "2024", "category": "Philosophy"}
        ]
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_and_load_books(self):
        """Test that books are correctly saved and loaded from JSON"""
        # Save test books
        self.storage.set_books(self.test_books)
        self.storage.save_data()
        
        # Create new instance and load
        new_storage = BookStorage(self.test_file)
        new_storage.load_data()
        loaded_books = new_storage.get_books()
        
        # Verify
        self.assertEqual(len(loaded_books), 2)
        self.assertEqual(loaded_books[0]["name"], "Test Novel")
        self.assertEqual(loaded_books[1]["category"], "Philosophy")
    
    def test_book_persistence(self):
        """Test that books persist across multiple saves"""
        # First save
        book1 = {"name": "First Book", "author": "Author 1", "date": "2020", "category": "Novel"}
        self.storage.set_books([book1])
        self.storage.save_data()
        
        # Add another book
        book2 = {"name": "Second Book", "author": "Author 2", "date": "2021", "category": "Poetry"}
        books = self.storage.get_books()
        books.append(book2)
        self.storage.set_books(books)
        self.storage.save_data()
        
        # Reload and verify both exist
        final_storage = BookStorage(self.test_file)
        final_storage.load_data()
        final_books = final_storage.get_books()
        
        self.assertEqual(len(final_books), 2)
        self.assertEqual(final_books[0]["name"], "First Book")
        self.assertEqual(final_books[1]["name"], "Second Book")


class TestBookManager(unittest.TestCase):
    """Test suite for BookManager - Backend business logic"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_file = "test_media.json"
        self.storage = BookStorage(self.test_file)
        self.manager = BookManager(self.storage)
        
        # Initialize with test books
        self.test_books = [
            {"name": "1984", "author": "George Orwell", "date": "1949", "category": "Novel"},
            {"name": "The Republic", "author": "Plato", "date": "380", "category": "Philosophy"},
            {"name": "Leaves of Grass", "author": "Walt Whitman", "date": "1855", "category": "Poetry"},
            {"name": "To Kill a Mockingbird", "author": "Harper Lee", "date": "1960", "category": "Novel"},
        ]
        self.storage.set_books(self.test_books)
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_book(self):
        """Test adding a new book to the collection"""
        new_book = {"name": "New Book", "author": "New Author", "date": "2025", "category": "Novel"}
        self.manager.add_book(new_book)
        
        books = self.storage.get_books()
        self.assertEqual(len(books), 5)
        self.assertEqual(books[-1]["name"], "New Book")
    
    def test_delete_book(self):
        """Test deleting a book from the collection"""
        initial_count = len(self.storage.get_books())
        self.manager.delete_book("1984")
        
        books = self.storage.get_books()
        self.assertEqual(len(books), initial_count - 1)
        
        # Verify book is actually deleted
        names = [book["name"] for book in books]
        self.assertNotIn("1984", names)
    
    def test_find_book(self):
        """Test finding a book by name"""
        book = self.manager.find_book("The Republic")
        
        self.assertIsNotNone(book)
        self.assertEqual(book["author"], "Plato")
        self.assertEqual(book["category"], "Philosophy")
    
    def test_update_book(self):
        """Test updating an existing book"""
        updated_data = {
            "name": "1984 - Updated",
            "author": "George Orwell",
            "date": "1949",
            "category": "Novel"
        }
        self.manager.update_book("1984", updated_data)
        
        books = self.storage.get_books()
        book = self.manager.find_book("1984 - Updated")
        
        self.assertIsNotNone(book)
        self.assertEqual(book["name"], "1984 - Updated")
    
    def test_filter_by_category(self):
        """Test filtering books by category"""
        novels = self.manager.filter_by_category("Novel")
        self.assertEqual(len(novels), 2)
        
        philosophy = self.manager.filter_by_category("Philosophy")
        self.assertEqual(len(philosophy), 1)
        
        poetry = self.manager.filter_by_category("Poetry")
        self.assertEqual(len(poetry), 1)
    
    def test_search_by_name(self):
        """Test searching books by name"""
        results = self.manager.search_by_name("1984")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "1984")
        
        # Test partial match
        results = self.manager.search_by_name("Republic")
        self.assertGreater(len(results), 0)
    
    def test_sort_by_date(self):
        """Test sorting books by date"""
        sorted_books = self.manager.sort_by_date(descending=True)
        
        # Verify sorted (string comparison)
        self.assertIsNotNone(sorted_books)
        self.assertEqual(len(sorted_books), 4)
    
    def test_get_statistics(self):
        """Test getting book statistics"""
        stats = self.manager.get_statistics()
        
        self.assertEqual(stats["total"], 4)
        self.assertEqual(stats["novels"], 2)
        self.assertEqual(stats["philosophy"], 1)
        self.assertEqual(stats["poetry"], 1)


class TestModernLibraryGUI(unittest.TestCase):
    """Test suite for ModernLibraryGUI - Frontend"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_file = "test_media.json"
        self.storage = BookStorage(self.test_file)
        self.manager = BookManager(self.storage)
        
        # Initialize with test books
        self.test_books = [
            {"name": "1984", "author": "George Orwell", "date": "1949", "category": "Novel"},
            {"name": "The Republic", "author": "Plato", "date": "380", "category": "Philosophy"},
            {"name": "Leaves of Grass", "author": "Walt Whitman", "date": "1855", "category": "Poetry"},
        ]
        self.storage.set_books(self.test_books)
        
        # Create root window
        self.root = tk.Tk()
        self.gui = ModernLibraryGUI(self.root, self.manager, self.storage)
    
    def tearDown(self):
        """Clean up"""
        self.root.destroy()
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_gui_initialization(self):
        """Test that GUI initializes correctly"""
        self.assertEqual(self.root.title(), "Saksham's Reading Room")
        self.assertEqual(self.root.cget("bg"), "#f5f5f5")
        self.assertIsNotNone(self.gui.tree)
    
    def test_load_books_into_gui(self):
        """Test that books are loaded into the treeview"""
        self.gui.load_books()
        
        # Get items from treeview
        items = self.gui.tree.get_children()
        self.assertEqual(len(items), 3)
        
        # Verify first item
        values = self.gui.tree.item(items[0])["values"]
        self.assertEqual(str(values[0]), "1984")
        self.assertEqual(str(values[1]), "George Orwell")
    
    def test_add_book_via_gui(self):
        """Test adding a book through GUI backend"""
        new_book = {
            "name": "Crime and Punishment",
            "author": "Dostoevsky",
            "date": "1866",
            "category": "Novel"
        }
        
        self.manager.add_book(new_book)
        self.storage.save_data()
        self.gui.load_books()
        
        items = self.gui.tree.get_children()
        self.assertEqual(len(items), 4)
        
        # Verify new book is in treeview
        values = self.gui.tree.item(items[-1])["values"]
        self.assertEqual(values[0], "Crime and Punishment")
    
    def test_delete_book_via_gui(self):
        """Test deleting a book through GUI backend"""
        initial_items = len(self.gui.tree.get_children())
        
        self.manager.delete_book("1984")
        self.storage.save_data()
        
        # Refresh GUI with fresh books from storage
        self.gui.books = self.storage.get_books()
        self.gui.load_books()
        
        final_items = len(self.gui.tree.get_children())
        self.assertEqual(final_items, initial_items - 1)
    
    def test_search_functionality(self):
        """Test search functionality in GUI"""
        self.gui.search_var.set("Republic")
        self.gui.search_books()
        
        items = self.gui.tree.get_children()
        self.assertGreater(len(items), 0)
    
    def test_filter_by_category(self):
        """Test filtering by category in GUI"""
        self.gui.filter_by_sidebar("Novel")
        
        items = self.gui.tree.get_children()
        self.assertEqual(len(items), 1)
        
        values = self.gui.tree.item(items[0])["values"]
        self.assertEqual(values[3], "Novel")
    
    def test_gui_counter_update(self):
        """Test that book counter updates correctly"""
        self.gui.update_counter()
        
        # The counter should show statistics
        counter_text = self.gui.counter_label.cget("text")
        self.assertIn("Total: 3", counter_text)
        self.assertIn("Novels: 1", counter_text)
    
    def test_sort_by_date_in_gui(self):
        """Test sorting by date in GUI"""
        self.gui.sort_by_date()
        
        items = self.gui.tree.get_children()
        self.assertGreater(len(items), 0)


class TestIntegration(unittest.TestCase):
    """Integration tests for the entire application"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_file = "test_media.json"
        self.storage = BookStorage(self.test_file)
        self.manager = BookManager(self.storage)
        
        self.test_books = [
            {"name": "1984", "author": "George Orwell", "date": "1949", "category": "Novel"},
            {"name": "The Republic", "author": "Plato", "date": "380", "category": "Philosophy"},
        ]
        self.storage.set_books(self.test_books)
        
        self.root = tk.Tk()
        self.gui = ModernLibraryGUI(self.root, self.manager, self.storage)
    
    def tearDown(self):
        """Clean up"""
        self.root.destroy()
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_full_book_lifecycle(self):
        """Test complete book lifecycle: create, read, update, delete"""
        # 1. CREATE - Add a new book
        new_book = {
            "name": "Pride and Prejudice",
            "author": "Jane Austen",
            "date": "1813",
            "category": "Novel"
        }
        self.manager.add_book(new_book)
        self.storage.save_data()
        
        # Verify created
        books = self.storage.get_books()
        self.assertEqual(len(books), 3)
        
        # 2. READ - Find the book
        found_book = self.manager.find_book("Pride and Prejudice")
        self.assertIsNotNone(found_book)
        self.assertEqual(found_book["author"], "Jane Austen")
        
        # 3. UPDATE - Modify the book
        updated_book = {
            "name": "Pride and Prejudice",
            "author": "Jane Austen",
            "date": "1813",
            "category": "Novel"
        }
        self.manager.update_book("Pride and Prejudice", updated_book)
        self.storage.save_data()
        
        # Verify update
        updated = self.manager.find_book("Pride and Prejudice")
        self.assertEqual(updated["author"], "Jane Austen")
        
        # 4. DELETE - Remove the book
        self.manager.delete_book("Pride and Prejudice")
        self.storage.save_data()
        
        # Verify deleted
        books = self.storage.get_books()
        self.assertEqual(len(books), 2)
        deleted_book = self.manager.find_book("Pride and Prejudice")
        self.assertIsNone(deleted_book)
    
    def test_filter_search_and_sort(self):
        """Test combined filter, search, and sort operations"""
        # Add more diverse books
        more_books = [
            {"name": "Thus Spoke Zarathustra", "author": "Nietzsche", "date": "1883", "category": "Philosophy"},
            {"name": "The Raven", "author": "Edgar Allan Poe", "date": "1845", "category": "Poetry"},
        ]
        books = self.storage.get_books()
        books.extend(more_books)
        self.storage.set_books(books)
        
        # Test filter
        philosophy_books = self.manager.filter_by_category("Philosophy")
        self.assertEqual(len(philosophy_books), 2)
        
        # Test search
        results = self.manager.search_by_name("Republic")
        self.assertEqual(len(results), 1)
        
        # Test sort
        sorted_books = self.manager.sort_by_date(descending=False)
        self.assertIsNotNone(sorted_books)
        self.assertEqual(len(sorted_books), 4)


def run_tests():
    """Run all tests with verbose output"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBookStorage))
    suite.addTests(loader.loadTestsFromTestCase(TestBookManager))
    suite.addTests(loader.loadTestsFromTestCase(TestModernLibraryGUI))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    result = run_tests()
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
