# Saksham's Reading Room

A professional book management application built with Python and Tkinter. This application allows users to manage a collection of books with features for adding, searching, filtering, and organizing books.

## Features

- **Add Books**: Add new books to the library with name, author, date, and category
- **Delete Books**: Remove books from the library with confirmation dialog
- **Search Functionality**: Search books by name in real-time
- **Category Filtering**: Filter books by category (Novel, Philosophy, Poetry, or All)
- **Sorting**: Sort books by date in descending order
- **Data Persistence**: All books are saved to `media.json` for persistent storage
- **Professional GUI**: Clean, organized user interface using Tkinter

## Project Structure

```
online_book_project/
├── main.py              # Main application file
├── media.json          # Book database (JSON format)
├── README.md           # This file
└── .gitignore          # Git ignore file
```

## Requirements

- Python 3.7+
- tkinter (usually comes with Python)
- json (built-in library)

## Installation

1. Clone or download the project:
   ```bash
   git clone <repository-url>
   cd online_book_project
   ```

2. No external dependencies needed - just Python 3.7+

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. **Adding a Book**:
   - Click the "New" button
   - Fill in the book details (Name, Author, Date, Category)
   - Click "Save"

3. **Searching for Books**:
   - Enter a book name in the search box
   - Results appear instantly as you type
   - Click "Erase" to clear the search

4. **Filtering by Category**:
   - Use the "Category" dropdown to filter by:
     - All (show all books)
     - Novel
     - Philosophy
     - Poetry

5. **Sorting**:
   - Click "Sort by Date ↓" to sort books in descending order by year

6. **Deleting Books**:
   - Select a book in the table
   - Click "Delete Selected" button
   - Confirm the deletion when prompted

7. **Right-click Menu**:
   - Right-click on a book to see context menu options

## Data Format

Books are stored in `media.json` with the following structure:

```json
{
    "name": "Book Title",
    "author": "Author Name",
    "date": "1990",
    "category": "Novel"
}
```

## Features Implemented

✅ GUI-based book management system
✅ Add new books with validation
✅ Delete books with confirmation
✅ Real-time search functionality
✅ Category filtering
✅ Sort by date
✅ JSON-based data persistence
✅ Professional UI with organized layout
✅ Context menu for additional options
✅ Responsive table display

## Technical Details

### Architecture
- **UI Framework**: Tkinter
- **Data Storage**: JSON file (media.json)
- **Language**: Python 3.7+

### Key Classes
- `OnlineLibraryApp`: Main application class handling all functionality

### Methods
- `load_data()`: Load books from JSON
- `save_data()`: Save books to JSON
- `refresh_tree()`: Update the display
- `filter_books()`: Filter by category
- `search_books()`: Search by name
- `sort_by_date()`: Sort books

## Version Control

This project uses Git for version control and is compatible with SourceTree.

Initialize repository:
```bash
git init
git add .
git commit -m "Initial commit: Online Library application"
```

## Tips for Best Performance

1. Keep the media.json file in the same directory as main.py
2. Do not manually edit the JSON file while the application is running
3. For large datasets, consider implementing pagination
4. Regular backups of media.json are recommended

## Future Enhancements

- Export to CSV/Excel
- Import from CSV/Excel
- Book rating system
- Reading history
- User accounts
- Database backend (SQLite/PostgreSQL)
- Advanced search filters
- Book cover images
- Multiple library support

## License

This project is created for educational purposes.

## Author

Created as part of an Advanced Programming course project.

---

**Version**: 1.0
**Last Updated**: 2025
**Status**: Complete and Functional
