import json
import os
from typing import Dict, List

class DatabaseManager:
    def __init__(self, database_file: str = "jay_chou_database.json"):
        """Initialize the database manager."""
        self.database_file = database_file
        self.data = self.load_database()
    
    def load_database(self) -> Dict:
        """Load the database from JSON file."""
        try:
            with open(self.database_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Database file '{self.database_file}' not found. Creating new database...")
            return {"albums": {}}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in database file '{self.database_file}'!")
            return {"albums": {}}
    
    def save_database(self) -> None:
        """Save the database to JSON file."""
        try:
            with open(self.database_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print(f"Database saved successfully to '{self.database_file}'")
        except Exception as e:
            print(f"Error saving database: {e}")
    
    def display_all_albums(self) -> None:
        """Display all albums and their songs."""
        print("\n" + "="*60)
        print("CURRENT DATABASE")
        print("="*60)
        
        if not self.data["albums"]:
            print("No albums in database.")
            return
        
        for album_name, songs in self.data["albums"].items():
            print(f"\n📀 {album_name} ({len(songs)} songs):")
            for i, song in enumerate(songs, 1):
                print(f"   {i:2d}. {song}")
    
    def add_new_album(self) -> None:
        """Add a new album to the database."""
        print("\n" + "="*60)
        print("ADD NEW ALBUM")
        print("="*60)
        
        album_name = input("Enter album name: ").strip()
        if not album_name:
            print("Album name cannot be empty!")
            return
        
        if album_name in self.data["albums"]:
            print(f"Album '{album_name}' already exists!")
            return
        
        songs = []
        print(f"\nEnter songs for '{album_name}' (press Enter twice to finish):")
        
        while True:
            song = input(f"Song {len(songs) + 1}: ").strip()
            if not song:
                if len(songs) == 0:
                    print("You must add at least one song!")
                    continue
                break
            
            if song in songs:
                print("This song is already in the album!")
                continue
            
            songs.append(song)
        
        self.data["albums"][album_name] = songs
        print(f"\nAlbum '{album_name}' added with {len(songs)} songs!")
    
    def add_songs_to_existing_album(self) -> None:
        """Add songs to an existing album."""
        print("\n" + "="*60)
        print("ADD SONGS TO EXISTING ALBUM")
        print("="*60)
        
        if not self.data["albums"]:
            print("No albums in database. Please add an album first.")
            return
        
        # Display available albums
        print("Available albums:")
        for i, album_name in enumerate(self.data["albums"].keys(), 1):
            print(f"{i}. {album_name}")
        
        # Get album selection
        while True:
            try:
                choice = input(f"\nSelect album (1-{len(self.data['albums'])}): ").strip()
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(self.data["albums"]):
                    album_name = list(self.data["albums"].keys())[choice_idx]
                    break
                else:
                    print("Invalid selection!")
            except ValueError:
                print("Please enter a valid number!")
        
        print(f"\nAdding songs to '{album_name}'...")
        existing_songs = set(self.data["albums"][album_name])
        
        while True:
            song = input("Enter song name (or press Enter to finish): ").strip()
            if not song:
                break
            
            if song in existing_songs:
                print("This song is already in the album!")
                continue
            
            self.data["albums"][album_name].append(song)
            existing_songs.add(song)
            print(f"Added '{song}' to '{album_name}'")
        
        print(f"\nFinished adding songs to '{album_name}'")
    
    def remove_song(self) -> None:
        """Remove a song from an album."""
        print("\n" + "="*60)
        print("REMOVE SONG")
        print("="*60)
        
        if not self.data["albums"]:
            print("No albums in database.")
            return
        
        # Display all songs with their albums
        all_songs = []
        for album_name, songs in self.data["albums"].items():
            for song in songs:
                all_songs.append((song, album_name))
        
        print("All songs in database:")
        for i, (song, album) in enumerate(all_songs, 1):
            print(f"{i:2d}. {song} (from {album})")
        
        # Get song selection
        while True:
            try:
                choice = input(f"\nSelect song to remove (1-{len(all_songs)}): ").strip()
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(all_songs):
                    song_to_remove, album_name = all_songs[choice_idx]
                    break
                else:
                    print("Invalid selection!")
            except ValueError:
                print("Please enter a valid number!")
        
        # Confirm removal
        confirm = input(f"\nAre you sure you want to remove '{song_to_remove}' from '{album_name}'? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            self.data["albums"][album_name].remove(song_to_remove)
            print(f"Removed '{song_to_remove}' from '{album_name}'")
        else:
            print("Removal cancelled.")
    
    def remove_album(self) -> None:
        """Remove an entire album."""
        print("\n" + "="*60)
        print("REMOVE ALBUM")
        print("="*60)
        
        if not self.data["albums"]:
            print("No albums in database.")
            return
        
        # Display available albums
        print("Available albums:")
        for i, album_name in enumerate(self.data["albums"].keys(), 1):
            song_count = len(self.data["albums"][album_name])
            print(f"{i}. {album_name} ({song_count} songs)")
        
        # Get album selection
        while True:
            try:
                choice = input(f"\nSelect album to remove (1-{len(self.data['albums'])}): ").strip()
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(self.data["albums"]):
                    album_name = list(self.data["albums"].keys())[choice_idx]
                    break
                else:
                    print("Invalid selection!")
            except ValueError:
                print("Please enter a valid number!")
        
        # Confirm removal
        song_count = len(self.data["albums"][album_name])
        confirm = input(f"\nAre you sure you want to remove '{album_name}' with {song_count} songs? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            del self.data["albums"][album_name]
            print(f"Removed album '{album_name}'")
        else:
            print("Removal cancelled.")
    
    def run_manager(self) -> None:
        """Run the database manager interface."""
        while True:
            print("\n" + "="*60)
            print("DATABASE MANAGER")
            print("="*60)
            print("1. View all albums and songs")
            print("2. Add new album")
            print("3. Add songs to existing album")
            print("4. Remove song")
            print("5. Remove album")
            print("6. Save and exit")
            print("7. Exit without saving")
            
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == "1":
                self.display_all_albums()
            elif choice == "2":
                self.add_new_album()
            elif choice == "3":
                self.add_songs_to_existing_album()
            elif choice == "4":
                self.remove_song()
            elif choice == "5":
                self.remove_album()
            elif choice == "6":
                self.save_database()
                print("Goodbye!")
                break
            elif choice == "7":
                print("Exiting without saving changes...")
                break
            else:
                print("Invalid option! Please select 1-7.")

def main():
    """Main function to run the database manager."""
    print("🎵 JAY CHOU DATABASE MANAGER 🎵")
    print("Manage your Jay Chou music database")
    
    manager = DatabaseManager()
    manager.run_manager()

if __name__ == "__main__":
    main()