# 🎵 Jay Chou Music Quiz 🎵

A fun and interactive quiz program to test your knowledge of Jay Chou's discography! This program generates random questions about which album each song belongs to, with comprehensive scoring and detailed feedback.

## Features

- **Random Test Generation**: Generate 1-20 questions per test
- **Multiple Choice Questions**: 4 answer choices per question (1 correct, 3 random wrong answers)
- **Comprehensive Scoring**: Score, percentage, and letter grade
- **Detailed Feedback**: Shows which questions were correct/incorrect with correct answers
- **🔄 Retake Wrong Questions**: Retake only the questions you got wrong with different answer choices
- **Progress Tracking**: See how much you improved on retake questions
- **📝 Personal Notes System**: Create notes to help remember which album each song belongs to
- **📀 Album Review**: Review any album and see all its songs with your personal notes
- **Easy Database Management**: Add, remove, and edit songs and albums easily
- **Extensible**: Easy to add new artists or different types of questions

## Files

- `jay_chou_quiz.py` - Main quiz program
- `database_manager.py` - Tool to manage the music database
- `notes_manager.py` - Tool to manage personal song notes
- `jay_chou_database.json` - Database containing all songs and albums
- `song_notes_database.json` - Database containing your personal notes
- `README.md` - This file

## How to Use

### Running the Quiz

1. Make sure you have Python 3.6+ installed
2. Run the main quiz program:
   ```bash
   python jay_chou_quiz.py
   ```
3. Choose how many questions you want (1-20)
4. Answer each question by selecting 1-4
5. View your results and detailed feedback
6. Optionally retake wrong questions
7. Optionally review albums
8. Choose to play again or exit

### Managing the Database

To add new songs, albums, or edit existing data:

1. Run the database manager:
   ```bash
   python database_manager.py
   ```

2. Choose from the following options:
   - **View all albums and songs** - See current database contents
   - **Add new album** - Create a new album with songs
   - **Add songs to existing album** - Add more songs to an existing album
   - **Remove song** - Remove a specific song from an album
   - **Remove album** - Remove an entire album
   - **Save and exit** - Save changes and exit
   - **Exit without saving** - Exit without saving changes

### Managing Personal Notes

To create, edit, or view your personal notes for songs:

1. Run the notes manager:
   ```bash
   python notes_manager.py
   ```

2. Choose from the following options:
   - **View all notes** - See all your personal notes
   - **Add new note** - Create a new note for a song
   - **Edit existing note** - Modify an existing note
   - **Remove note** - Delete a note
   - **Search notes** - Find notes containing specific text
   - **Save and exit** - Save changes and exit
   - **Exit without saving** - Exit without saving changes

## New Features

### 📝 Personal Notes System

- **Automatic Note Creation**: After getting a song correct on retake, you can create a note to help remember it
- **Note Display**: Your notes appear when reviewing albums
- **Persistent Storage**: Notes are saved in a separate database file
- **Easy Management**: Use the notes manager to add, edit, or remove notes

### 📀 Album Review

- **Browse Albums**: Select any album to review
- **Song Lists**: See all songs in the selected album
- **Note Integration**: Your personal notes appear next to songs
- **Learning Tool**: Perfect for studying and memorization

## Database Structure

The database is stored in JSON format for easy editing:

```json
{
  "albums": {
    "Album Name": [
      "Song 1",
      "Song 2",
      "Song 3"
    ]
  }
}
```

### Notes Database Structure

```json
{
  "notes": {
    "Song Name": "Your personal note to help remember the album"
  }
}
```

### Adding New Songs/Albums

#### Method 1: Using the Database Manager (Recommended)
1. Run `python database_manager.py`
2. Choose option 2 to add a new album or option 3 to add songs to existing albums
3. Follow the prompts to enter album and song names
4. Save your changes

#### Method 2: Direct JSON Editing
1. Open `jay_chou_database.json` in any text editor
2. Add new albums and songs following the existing format
3. Save the file

## Example Usage

### Taking a Quiz with Notes
```
🎵 JAY CHOU MUSIC QUIZ 🎵
Test your knowledge of Jay Chou's discography!

Database loaded successfully!
Total albums: 14
Total songs: 140

How many questions would you like? (1-20): 5

Generating 5 questions...

Test ready! You will be asked to identify which album each song belongs to.
Press Enter to start the test...

============================================================
Question 1:
Which album does the song '晴天' belong to?

1. 范特西
2. 葉惠美
3. 八度空間
4. 七里香
============================================================
Enter your answer (1-4): 2

============================================================
TEST RESULTS
============================================================
Score: 4/5
Percentage: 80.0%
Grade: A

📝 You got 1 questions wrong.
You can retake the test with only the questions you missed!

============================================================
Would you like to retake the questions you got wrong? (y/n): y

============================================================
🔄 RETAKE QUIZ - WRONG QUESTIONS ONLY
============================================================
You will retake 1 questions that you got wrong.
This time, the answer choices will be different!

Press Enter to start the retake...

============================================================
Question 1:
Which album does the song '夜曲' belong to?
⚠️  You previously answered: 范特西

1. 11月的蕭邦
2. 我很忙
3. 魔杰座
4. 跨時代
============================================================
Enter your answer (1-4): 1

📝 You got '夜曲' correct! This song belongs to '11月的蕭邦'.
Would you like to create a note to help remember this? (y/n): y
Enter your note (to help remember which album this song belongs to): Classic piano ballad, very emotional
✅ Note saved for '夜曲'!

============================================================
🔄 RETAKE RESULTS
============================================================
Score: 1/1
Percentage: 100.0%

🎉 You improved on 1 questions!

============================================================
Would you like to review an album? (y/n): y

============================================================
📀 ALBUM REVIEW
============================================================
Available albums:
1. Jay (10 songs)
2. 范特西 (10 songs)
3. 八度空间 (10 songs)
4. 葉惠美 (10 songs)
5. 七里香 (10 songs)
6. 11月的萧邦 (10 songs)
7. 依然范特西 (10 songs)
8. 我很忙 (10 songs)
9. 魔杰座 (10 songs)
10. 跨時代 (10 songs)
11. 驚嘆號 (11 songs)
12. 十二新作 (12 songs)
13. 哎呦，不錯哦 (10 songs)
14. 周杰倫的床邊故事 (10 songs)

Select album to review (1-14): 6

============================================================
📀 11月的萧邦 - 10 songs
============================================================
 1. 夜曲 💡 Classic piano ballad, very emotional
 2. 蓝色风暴
 3. 发如雪
 4. 黑色毛衣
 5. 四面楚歌
 6. 枫
 7. 浪漫手机
 8. 逆鳞
 9. 麦芽糖
10. 珊瑚海

============================================================
Album review complete!
```

## Current Database

The program comes pre-loaded with Jay Chou's complete discography including:

- **Jay** (2000) - 10 songs
- **范特西** (2001) - 10 songs  
- **八度空間** (2002) - 10 songs
- **葉惠美** (2003) - 10 songs
- **七里香** (2004) - 10 songs
- **11月的蕭邦** (2005) - 10 songs
- **依然范特西** (2006) - 10 songs
- **我很忙** (2007) - 10 songs
- **魔杰座** (2008) - 10 songs
- **跨時代** (2010) - 10 songs
- **驚嘆號** (2011) - 11 songs
- **十二新作** (2012) - 12 songs
- **哎呦，不錯哦** (2014) - 10 songs
- **周杰倫的床邊故事** (2016) - 10 songs

**Total: 14 albums, 143 songs**

## Extending the Program

This program is designed to be easily extensible:

1. **Add New Artists**: Create new JSON files for different artists
2. **Different Question Types**: Modify the quiz logic for different question formats
3. **Statistics Tracking**: Add features to track high scores and progress
4. **GUI Interface**: Convert to a graphical user interface
5. **Multiple Languages**: Add support for different languages
6. **Note Categories**: Add different types of notes (lyrics, trivia, etc.)

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## Troubleshooting

### Common Issues

1. **"Database file not found"**: Make sure `jay_chou_database.json` is in the same directory as the Python files
2. **"Notes file not found"**: The program will create `song_notes_database.json` automatically
3. **Encoding issues**: The program uses UTF-8 encoding for Chinese characters
4. **Invalid JSON**: If the database file is corrupted, you can delete it and the program will create a new one

### Getting Help

If you encounter any issues:
1. Check that all files are in the same directory
2. Ensure Python 3.6+ is installed
3. Try running the database manager to check if the database is valid
4. Try running the notes manager to check if the notes database is valid

## License

This project is open source and available for personal and educational use.

---

**Enjoy testing your Jay Chou knowledge! 🎵**