# SourceTree Setup Guide

## Setting Up with SourceTree

This project is ready to be used with Atlassian SourceTree for version control.

### Prerequisites
1. Install Git: https://git-scm.com/download/win
2. Install SourceTree: https://www.sourcetreeapp.com/

### Steps to Add to SourceTree

1. **Initialize Git Repository** (if not already done):
   - Open Command Prompt or PowerShell
   - Navigate to the project folder:
     ```
     cd "c:\Users\Saksham\Documents\advanced programming final\online_book_project"
     ```
   - Initialize git:
     ```
     git init
     git add .
     git commit -m "Initial commit: Online Library - Saksham application"
     ```

2. **Add Project to SourceTree**:
   - Open SourceTree
   - Click "File" → "Clone / New"
   - Select "Create Local Repository"
   - Choose the project folder: `c:\Users\Saksham\Documents\advanced programming final\online_book_project`
   - Click "Create"

3. **Make Your First Commit in SourceTree**:
   - The project will now appear in SourceTree
   - You'll see all files in the "Unstaged files" section
   - Click "Stage All" to stage all files
   - Add commit message: "Initial commit: Online Library application"
   - Click "Commit"

### Git Configuration
Before first commit, configure git:
```
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Project Workflow

After initial setup, use SourceTree for:
- **Staging changes**: Select files and click "Stage"
- **Committing**: Add message and click "Commit"
- **Pushing**: Push changes to remote repository
- **Branching**: Create feature branches for development
- **Merging**: Merge branches when features are complete

### Files Included for Git

- `.gitignore` - Specifies files to ignore in version control
- `README.md` - Project documentation
- `main.py` - Main application
- `media.json` - Book database
- `requirements.txt` - Python dependencies

### Example Commit Messages
- "Add new book feature"
- "Fix search functionality"
- "Update UI styling"
- "Add category filtering"
- "Implement delete confirmation"

### Branch Strategy (Recommended)

```
main (stable releases)
├── develop (integration branch)
    ├── feature/add-books
    ├── feature/search-functionality
    └── feature/export-feature
```

### Common SourceTree Tasks

1. **View History**: Click "Log" to see all commits
2. **View Changes**: Double-click a commit to see file changes
3. **Create Branch**: Right-click in branch list → "New Branch"
4. **Merge**: Right-click source branch → "Merge"
5. **Stash Changes**: "Stash" button to temporarily save changes
6. **Discard Changes**: Right-click file → "Discard"

---

**Note**: The .gitignore file is already configured to exclude Python cache files, virtual environments, and IDE settings.
