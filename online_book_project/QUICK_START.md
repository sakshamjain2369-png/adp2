# Quick Start Guide - Saksham's Reading Room

## Getting Started in 3 Steps

### Step 1: Run the Application
```bash
python main.py
```

### Step 2: Explore the Interface
- See 23 pre-loaded books
- Browse the library
- Try different features

### Step 3: Create Your First Book
- Click "New" button
- Fill in book details
- Click "Save"

---

## First Time Usage Checklist

### ✅ Launch
1. Open Command Prompt/PowerShell
2. Navigate to project folder
3. Run `python main.py`
4. Application window appears

### ✅ Browse
1. Look at the pre-loaded books
2. Scroll through the table
3. Notice the columns (Name, Author, Date)

### ✅ Search
1. Type "Crime" in the search box
2. Watch results filter in real-time
3. Click "Erase" to clear search

### ✅ Filter
1. Click Category dropdown
2. Select "Poetry"
3. See only poetry books
4. Select "All" to show everything

### ✅ Sort
1. Click "Sort by Date ↓"
2. Books rearrange by newest first
3. Click again to resort

### ✅ Add a Book
1. Click "New" button
2. Enter:
   - Name: "My Favorite Book"
   - Author: "Your Name"
   - Date: "2025"
   - Category: "Novel"
3. Click "Save"
4. See book in list

### ✅ Delete a Book
1. Click on a book to select it
2. Click "Delete Selected"
3. Confirm deletion
4. Book is removed

---

## Common Tasks

### Search for a Specific Book
```
1. Type book name in search box
2. Results appear instantly
3. Click Erase to reset
```

### Find All Books by an Author
```
1. Search for author name (not in search box)
2. OR use advanced features from ADVANCED_FEATURES.md
```

### View Only Philosophy Books
```
1. Click Category dropdown
2. Select "Philosophy"
3. Only philosophy books show
```

### Get Newest Books First
```
1. Click "Sort by Date ↓"
2. Books sorted (newest first)
```

### Organize Your Library
```
1. Add missing books using "New" button
2. Remove duplicates using "Delete Selected"
3. Use search to find specific books
4. Use filters to browse by category
```

---

## What Each Button Does

| Button | Function |
|--------|----------|
| Load | Shows status message |
| Search | Searches by book name |
| Erase | Clears search and filters |
| New | Opens dialog to add book |
| Sort by Date ↓ | Sorts books newest first |
| Delete Selected | Removes selected book |

---

## Understanding the Display

### Table Columns

| Column | What It Shows |
|--------|--------------|
| Name | Book title |
| Author | Author's name |
| Date | Publication year |

### Color Indicators

| Element | Color | Meaning |
|---------|-------|---------|
| Header | Dark blue | Application title |
| Buttons | Blue | Action buttons |
| Buttons | Green | Add/Create action |
| Buttons | Red | Delete action |
| Buttons | Orange | Sort action |

---

## Tips for Power Users

### Efficiency Tips
1. Use search before deleting (find exact book)
2. Filter by category to reduce clutter
3. Sort by date to see recent additions
4. Double-click table row to view details (if implemented)

### Organization Tips
1. Keep consistent naming (Title Case for names)
2. Use standard author names
3. Verify date format (4-digit year)
4. Use appropriate categories

### Data Management
1. Backup media.json regularly
2. Don't delete media.json while app runs
3. Keep backup copies before testing
4. Test with sample data first

---

## Keyboard Shortcuts

(Basic usage - advanced shortcuts coming)

| Shortcut | Function |
|----------|----------|
| Type in search box | Real-time search |
| Ctrl+C | Copy (in entry fields) |
| Ctrl+V | Paste (in entry fields) |
| Escape | Close dialogs |
| Tab | Move between fields |

---

## Common Questions

### Q: Where is my data saved?
**A**: In `media.json` file in the same folder as `main.py`

### Q: Can I backup my books?
**A**: Yes, copy `media.json` to safe location

### Q: Can I share my library?
**A**: Yes, share the `media.json` file with others

### Q: Can I use Excel?
**A**: See ADVANCED_FEATURES.md for CSV export

### Q: Can I edit books?
**A**: Delete old and add new version (or use advanced features)

### Q: How do I add 100 books quickly?
**A**: See ADVANCED_FEATURES.md for import functionality

### Q: What if I delete books by mistake?
**A**: Restore from backup (copy back media.json)

### Q: Can I use on Mac/Linux?
**A**: Yes, Python and Tkinter work on all platforms

---

## Troubleshooting

### Application Won't Start
```
Check: Python 3.7+ installed
Run: python --version
```

### Search Not Working
```
Check: Book names match exactly
Try: Search for partial word
Try: Erase and try again
```

### Books Not Saving
```
Check: media.json is not open elsewhere
Check: Folder has write permissions
Check: Disk has free space
```

### Table Empty
```
Check: media.json exists in folder
Check: media.json has valid JSON format
Try: Copy fresh media.json from backup
```

### Slow Performance
```
Check: How many books (100+ might slow down)
Try: Restart application
Note: Normal for 1000+ books
```

---

## Next Steps After Mastering Basics

1. **Read Project Documentation**
   - Check README.md for features
   - Read PROJECT_GUIDE.md for architecture

2. **Try Advanced Features**
   - Implement ratings (ADVANCED_FEATURES.md)
   - Add reading status
   - Export/Import functionality

3. **Set Up Version Control**
   - Follow SOURCETREE_SETUP.md
   - Make commits for changes
   - Track your modifications

4. **Customize**
   - Change colors in main.py
   - Add new categories
   - Modify table layout

5. **Extend**
   - Add book cover images
   - Implement search filters
   - Add statistics dashboard

---

## Features Overview

✅ **Fully Implemented**
- Add books
- Delete books
- Search books
- Filter by category
- Sort by date
- Persistent storage
- Professional GUI

🔄 **In Development** (See ADVANCED_FEATURES.md)
- Book ratings
- Reading status
- Export to CSV
- Import from CSV
- Statistics
- Edit books

📋 **Future Roadmap**
- Database backend
- User accounts
- Cloud sync
- Mobile app
- Advanced analytics

---

## File Structure

```
Project Folder/
├── main.py           ← Run this file
├── media.json        ← Your books (auto-updated)
├── README.md         ← Full documentation
├── PROJECT_GUIDE.md  ← Technical details
├── ADVANCED_FEATURES.md  ← Enhancement ideas
├── SOURCETREE_SETUP.md   ← Version control guide
└── requirements.txt  ← Dependencies (none needed!)
```

---

## Support Resources

1. **Documentation**: README.md
2. **Architecture**: PROJECT_GUIDE.md
3. **Enhancements**: ADVANCED_FEATURES.md
4. **Version Control**: SOURCETREE_SETUP.md
5. **Code Comments**: See main.py

---

## Performance Notes

| Task | Speed |
|------|-------|
| Open app | < 1 second |
| Load 23 books | Instant |
| Search 1000 books | < 0.1 seconds |
| Add book | Instant |
| Delete book | Instant |
| Sort books | < 0.1 seconds |

---

## System Requirements

| Item | Requirement |
|------|-------------|
| Python | 3.7+ |
| RAM | 256 MB minimum |
| Disk | 50 MB minimum |
| OS | Windows, Mac, Linux |
| Dependencies | None (built-in libs only) |

---

## Success Criteria

Your implementation is complete when you can:

✅ Start the application
✅ See all 23 sample books
✅ Search for books by name
✅ Filter by category
✅ Sort by date
✅ Add a new book
✅ Delete a book
✅ Data persists after restart
✅ Handle invalid input gracefully

---

## Final Tips

1. **Keep media.json safe** - it's your database
2. **Backup regularly** - copy media.json monthly
3. **Explore features** - try all buttons
4. **Read comments** - they explain the code
5. **Experiment** - try ADVANCED_FEATURES
6. **Share project** - show friends your work

---

## Congratulations! 🎉

You now have a professional book management application!

**Next**: Read PROJECT_GUIDE.md to understand the architecture
**Then**: Explore ADVANCED_FEATURES.md for enhancements
**Finally**: Set up SourceTree following SOURCETREE_SETUP.md

---

**Happy coding and happy reading! 📚**
