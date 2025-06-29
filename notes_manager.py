import json
import os
from typing import Dict, List

class NotesManager:
    def __init__(self, notes_file: str = "song_notes_billydatabase.json"):
        """Initialize the notes manager."""
        self.notes_file = notes_file
        self.notes = self.load_notes()
    
    def load_notes(self) -> Dict:
        """Load notes from JSON file."""
        try:
            with open(self.notes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Notes file '{self.notes_file}' not found. Creating new notes database...")
            return {"notes": {}}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in notes file '{self.notes_file}'!")
            return {"notes": {}}
    
    def save_notes(self) -> None:
        """Save notes to JSON file."""
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, ensure_ascii=False, indent=2)
            print(f"Notes saved successfully to '{self.notes_file}'")
        except Exception as e:
            print(f"Error saving notes: {e}")
    
    def add_note(self, song: str, note: str) -> None:
        """Add a note for a specific song."""
        if "notes" not in self.notes:
            self.notes["notes"] = {}
        
        self.notes["notes"][song] = note
        print(f"Note added for '{song}': {note}")
    
    def get_note(self, song: str) -> str:
        """Get the note for a specific song."""
        if "notes" not in self.notes:
            return ""
        return self.notes["notes"].get(song, "")
    
    def has_note(self, song: str) -> bool:
        """Check if a song has a note."""
        if "notes" not in self.notes:
            return False
        return song in self.notes["notes"]
    
    def remove_note(self, song: str) -> None:
        """Remove a note for a specific song."""
        if "notes" in self.notes and song in self.notes["notes"]:
            del self.notes["notes"][song]
            print(f"Note removed for '{song}'")
        else:
            print(f"No note found for '{song}'")
    
    def display_all_notes(self) -> None:
        """Display all notes."""
        print("\n" + "="*60)
        print("ALL SONG NOTES")
        print("="*60)
        
        if "notes" not in self.notes or not self.notes["notes"]:
            print("No notes found.")
            return
        
        for i, (song, note) in enumerate(self.notes["notes"].items(), 1):
            print(f"\n{i}. Song: {song}")
            print(f"   Note: {note}")
    
    def add_new_note(self) -> None:
        """Add a new note manually."""
        print("\n" + "="*60)
        print("ADD NEW NOTE")
        print("="*60)
        
        song = input("Enter song name: ").strip()
        if not song:
            print("Song name cannot be empty!")
            return
        
        if self.has_note(song):
            print(f"Note already exists for '{song}': {self.get_note(song)}")
            overwrite = input("Do you want to overwrite it? (y/n): ").strip().lower()
            if overwrite not in ['y', 'yes']:
                return
        
        note = input("Enter your note (to help remember which album this song belongs to): ").strip()
        if not note:
            print("Note cannot be empty!")
            return
        
        self.add_note(song, note)
    
    def edit_note(self) -> None:
        """Edit an existing note."""
        print("\n" + "="*60)
        print("EDIT NOTE")
        print("="*60)
        
        if "notes" not in self.notes or not self.notes["notes"]:
            print("No notes found to edit.")
            return
        
        # Display available songs
        print("Songs with notes:")
        songs = list(self.notes["notes"].keys())
        for i, song in enumerate(songs, 1):
            print(f"{i}. {song}")
        
        # Get song selection
        while True:
            try:
                choice = input(f"\nSelect song to edit (1-{len(songs)}): ").strip()
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(songs):
                    song = songs[choice_idx]
                    break
                else:
                    print("Invalid selection!")
            except ValueError:
                print("Please enter a valid number!")
        
        current_note = self.get_note(song)
        print(f"\nCurrent note for '{song}': {current_note}")
        
        new_note = input("Enter new note: ").strip()
        if not new_note:
            print("Note cannot be empty!")
            return
        
        self.add_note(song, new_note)
    
    def remove_note_manual(self) -> None:
        """Remove a note manually."""
        print("\n" + "="*60)
        print("REMOVE NOTE")
        print("="*60)
        
        if "notes" not in self.notes or not self.notes["notes"]:
            print("No notes found to remove.")
            return
        
        # Display available songs
        print("Songs with notes:")
        songs = list(self.notes["notes"].keys())
        for i, song in enumerate(songs, 1):
            print(f"{i}. {song}")
        
        # Get song selection
        while True:
            try:
                choice = input(f"\nSelect song to remove note (1-{len(songs)}): ").strip()
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(songs):
                    song = songs[choice_idx]
                    break
                else:
                    print("Invalid selection!")
            except ValueError:
                print("Please enter a valid number!")
        
        confirm = input(f"\nAre you sure you want to remove the note for '{song}'? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            self.remove_note(song)
        else:
            print("Removal cancelled.")
    
    def search_notes(self) -> None:
        """Search for notes containing specific text."""
        print("\n" + "="*60)
        print("SEARCH NOTES")
        print("="*60)
        
        if "notes" not in self.notes or not self.notes["notes"]:
            print("No notes found to search.")
            return
        
        search_term = input("Enter search term: ").strip().lower()
        if not search_term:
            print("Search term cannot be empty!")
            return
        
        found_notes = []
        for song, note in self.notes["notes"].items():
            if search_term in song.lower() or search_term in note.lower():
                found_notes.append((song, note))
        
        if found_notes:
            print(f"\nFound {len(found_notes)} matching notes:")
            for i, (song, note) in enumerate(found_notes, 1):
                print(f"\n{i}. Song: {song}")
                print(f"   Note: {note}")
        else:
            print("No notes found matching your search term.")
    
    def run_manager(self) -> None:
        """Run the notes manager interface."""
        while True:
            print("\n" + "="*60)
            print("SONG NOTES MANAGER")
            print("="*60)
            print("1. View all notes")
            print("2. Add new note")
            print("3. Edit existing note")
            print("4. Remove note")
            print("5. Search notes")
            print("6. Save and exit")
            print("7. Exit without saving")
            
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == "1":
                self.display_all_notes()
            elif choice == "2":
                self.add_new_note()
            elif choice == "3":
                self.edit_note()
            elif choice == "4":
                self.remove_note_manual()
            elif choice == "5":
                self.search_notes()
            elif choice == "6":
                self.save_notes()
                print("Goodbye!")
                break
            elif choice == "7":
                print("Exiting without saving changes...")
                break
            else:
                print("Invalid option! Please select 1-7.")

def main():
    """Main function to run the notes manager."""
    print("📝 SONG NOTES MANAGER 📝")
    print("Manage your notes to remember which album each song belongs to")
    
    manager = NotesManager()
    manager.run_manager()

if __name__ == "__main__":
    main() 