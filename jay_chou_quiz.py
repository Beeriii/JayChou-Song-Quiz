import json
import random
import os
from typing import List, Dict, Tuple

# Import the NotesManager
from notes_manager import NotesManager

class JayChouQuiz:
    def __init__(self, database_file: str = "jay_chou_database.json"):
        """Initialize the quiz with the database file."""
        self.database_file = database_file
        self.data = self.load_database()
        self.song_to_album = self.create_song_mapping()
        # Initialize notes manager
        self.notes_manager = NotesManager()
        
    def load_database(self) -> Dict:
        """Load the database from JSON file."""
        try:
            with open(self.database_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Database file '{self.database_file}' not found!")
            return {"albums": {}}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in database file '{self.database_file}'!")
            return {"albums": {}}
    
    def create_song_mapping(self) -> Dict[str, str]:
        """Create a mapping from song names to album names."""
        song_mapping = {}
        for album_name, songs in self.data["albums"].items():
            for song in songs:
                song_mapping[song] = album_name
        return song_mapping
    
    def get_all_albums(self) -> List[str]:
        """Get all album names."""
        return list(self.data["albums"].keys())
    
    def get_all_songs(self) -> List[str]:
        """Get all song names."""
        return list(self.song_to_album.keys())
    
    def generate_question(self) -> Tuple[str, str, List[str]]:
        """Generate a single question with 4 answer choices."""
        # Randomly select a song
        song = random.choice(self.get_all_songs())
        correct_album = self.song_to_album[song]
        
        # Get 3 wrong albums (excluding the correct one)
        all_albums = self.get_all_albums()
        wrong_albums = [album for album in all_albums if album != correct_album]
        wrong_choices = random.sample(wrong_albums, 3)
        
        # Create answer choices and shuffle them
        answer_choices = wrong_choices + [correct_album]
        random.shuffle(answer_choices)
        
        return song, correct_album, answer_choices
    
    def generate_test(self, num_questions: int) -> List[Dict]:
        """Generate a complete test with the specified number of questions."""
        if num_questions > len(self.get_all_songs()):
            print(f"Warning: Requested {num_questions} questions but only {len(self.get_all_songs())} songs available.")
            num_questions = len(self.get_all_songs())
        
        test_questions = []
        used_songs = set()
        
        while len(test_questions) < num_questions:
            song, correct_album, answer_choices = self.generate_question()
            
            # Avoid duplicate songs in the same test
            if song not in used_songs:
                test_questions.append({
                    'song': song,
                    'correct_album': correct_album,
                    'answer_choices': answer_choices,
                    'user_answer': None,
                    'is_correct': None
                })
                used_songs.add(song)
        
        return test_questions
    
    def generate_retake_test(self, wrong_questions: List[Dict]) -> List[Dict]:
        """Generate a retake test with only the questions that were answered incorrectly."""
        retake_questions = []
        
        for wrong_question in wrong_questions:
            # Create new answer choices for the same song
            song = wrong_question['song']
            correct_album = wrong_question['correct_answer']
            
            # Get 3 wrong albums (excluding the correct one)
            all_albums = self.get_all_albums()
            wrong_albums = [album for album in all_albums if album != correct_album]
            wrong_choices = random.sample(wrong_albums, 3)
            
            # Create answer choices and shuffle them
            answer_choices = wrong_choices + [correct_album]
            random.shuffle(answer_choices)
            
            retake_questions.append({
                'song': song,
                'correct_album': correct_album,
                'answer_choices': answer_choices,
                'user_answer': None,
                'is_correct': None,
                'original_wrong_answer': wrong_question['user_answer']  # Keep track of original wrong answer
            })
        
        return retake_questions
    
    def display_question(self, question: Dict, question_num: int, is_retake: bool = False) -> None:
        """Display a single question to the user."""
        print(f"\n{'='*60}")
        print(f"Question {question_num}:")
        print(f"Which album does the song '{question['song']}' belong to?")
        
        if is_retake and 'original_wrong_answer' in question:
            print(f"⚠️  You previously answered: {question['original_wrong_answer']}")
        
        print()
        
        for i, choice in enumerate(question['answer_choices'], 1):
            print(f"{i}. {choice}")
        
        print(f"{'='*60}")
    
    def get_user_answer(self, question: Dict) -> str:
        """Get and validate user's answer."""
        while True:
            try:
                choice = input("Enter your answer (1-4): ").strip()
                if choice in ['1', '2', '3', '4']:
                    choice_index = int(choice) - 1
                    return question['answer_choices'][choice_index]
                else:
                    print("Please enter a number between 1 and 4.")
            except (ValueError, IndexError):
                print("Please enter a valid number between 1 and 4.")
    
    def offer_note_creation(self, song: str, album: str) -> None:
        """Offer to create a note for a song after getting it correct on retake."""
        if not self.notes_manager.has_note(song):
            print(f"\n📝 You got '{song}' correct! This song belongs to '{album}'.")
            create_note = input("Would you like to create a note to help remember this? (y/n): ").strip().lower()
            
            if create_note in ['y', 'yes']:
                note = input("Enter your note (to help remember which album this song belongs to): ").strip()
                if note:
                    self.notes_manager.add_note(song, note)
                    print(f"✅ Note saved for '{song}'!")
                else:
                    print("Note creation cancelled.")
        else:
            # Show existing note
            existing_note = self.notes_manager.get_note(song)
            print(f"\n📝 You got '{song}' correct! This song belongs to '{album}'.")
            print(f"💡 Your note: {existing_note}")
    
    def grade_test(self, test_questions: List[Dict]) -> Dict:
        """Grade the test and return results."""
        correct_count = 0
        results = []
        wrong_questions = []
        
        for question in test_questions:
            is_correct = question['user_answer'] == question['correct_album']
            if is_correct:
                correct_count += 1
            else:
                # Store wrong questions for potential retake
                wrong_questions.append({
                    'song': question['song'],
                    'user_answer': question['user_answer'],
                    'correct_answer': question['correct_album'],
                    'is_correct': is_correct
                })
            
            results.append({
                'song': question['song'],
                'user_answer': question['user_answer'],
                'correct_answer': question['correct_album'],
                'is_correct': is_correct
            })
        
        total_questions = len(test_questions)
        percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        
        return {
            'total_questions': total_questions,
            'correct_count': correct_count,
            'percentage': percentage,
            'results': results,
            'wrong_questions': wrong_questions
        }
    
    def display_results(self, results: Dict) -> None:
        """Display test results with detailed feedback."""
        print(f"\n{'='*60}")
        print("TEST RESULTS")
        print(f"{'='*60}")
        print(f"Score: {results['correct_count']}/{results['total_questions']}")
        print(f"Percentage: {results['percentage']:.1f}%")
        
        # Determine grade
        if results['percentage'] >= 90:
            grade = "A+"
        elif results['percentage'] >= 80:
            grade = "A"
        elif results['percentage'] >= 70:
            grade = "B"
        elif results['percentage'] >= 60:
            grade = "C"
        elif results['percentage'] >= 50:
            grade = "D"
        else:
            grade = "F"
        
        print(f"Grade: {grade}")
        
        # Show retake option if there are wrong questions
        if results['wrong_questions']:
            print(f"\n📝 You got {len(results['wrong_questions'])} questions wrong.")
            print("You can retake the test with only the questions you missed!")
        
        print(f"\n{'='*60}")
        print("DETAILED RESULTS")
        print(f"{'='*60}")
        
        for i, result in enumerate(results['results'], 1):
            status = "✓ CORRECT" if result['is_correct'] else "✗ WRONG"
            print(f"\n{i}. {result['song']}")
            print(f"   Your answer: {result['user_answer']}")
            
            if not result['is_correct']:
                print(f"   Correct answer: {result['correct_answer']}")
            
            print(f"   Status: {status}")
    
    def run_retake_quiz(self, wrong_questions: List[Dict]) -> None:
        """Run a retake quiz with only the questions that were answered incorrectly."""
        if not wrong_questions:
            print("No wrong questions to retake!")
            return
        
        print(f"\n{'='*60}")
        print("🔄 RETAKE QUIZ - WRONG QUESTIONS ONLY")
        print(f"{'='*60}")
        print(f"You will retake {len(wrong_questions)} questions that you got wrong.")
        print("This time, the answer choices will be different!")
        print("\nPress Enter to start the retake...")
        input()
        
        # Generate retake questions
        retake_questions = self.generate_retake_test(wrong_questions)
        
        # Run the retake test
        for i, question in enumerate(retake_questions, 1):
            self.display_question(question, i, is_retake=True)
            question['user_answer'] = self.get_user_answer(question)
            
            # Offer note creation for correct answers
            if question['user_answer'] == question['correct_album']:
                self.offer_note_creation(question['song'], question['correct_album'])
        
        # Grade and display retake results
        retake_results = self.grade_test(retake_questions)
        
        print(f"\n{'='*60}")
        print("🔄 RETAKE RESULTS")
        print(f"{'='*60}")
        print(f"Score: {retake_results['correct_count']}/{retake_results['total_questions']}")
        print(f"Percentage: {retake_results['percentage']:.1f}%")
        
        # Show improvement
        original_wrong = len(wrong_questions)
        still_wrong = len(retake_results['wrong_questions'])
        improved = original_wrong - still_wrong
        
        if improved > 0:
            print(f"🎉 You improved on {improved} questions!")
        elif improved == 0:
            print(f"📊 You got the same number of questions wrong.")
        else:
            print(f"📉 You got {abs(improved)} more questions wrong this time.")
        
        # Show detailed retake results
        print(f"\n{'='*60}")
        print("RETAKE DETAILED RESULTS")
        print(f"{'='*60}")
        
        for i, result in enumerate(retake_results['results'], 1):
            status = "✓ CORRECT" if result['is_correct'] else "✗ WRONG"
            print(f"\n{i}. {result['song']}")
            print(f"   Your answer: {result['user_answer']}")
            
            if not result['is_correct']:
                print(f"   Correct answer: {result['correct_answer']}")
            
            print(f"   Status: {status}")
    
    def review_album(self) -> None:
        """Allow user to review a specific album and its songs."""
        print(f"\n{'='*60}")
        print("📀 ALBUM REVIEW")
        print(f"{'='*60}")
        
        # Display available albums
        albums = self.get_all_albums()
        print("Available albums:")
        for i, album in enumerate(albums, 1):
            song_count = len(self.data["albums"][album])
            print(f"{i}. {album} ({song_count} songs)")
        
        # Get album selection
        while True:
            try:
                choice = input(f"\nSelect album to review (1-{len(albums)}): ").strip()
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(albums):
                    selected_album = albums[choice_idx]
                    break
                else:
                    print("Invalid selection!")
            except ValueError:
                print("Please enter a valid number!")
        
        # Display album details
        songs = self.data["albums"][selected_album]
        print(f"\n{'='*60}")
        print(f"📀 {selected_album} - {len(songs)} songs")
        print(f"{'='*60}")
        
        for i, song in enumerate(songs, 1):
            note = self.notes_manager.get_note(song)
            if note:
                print(f"{i:2d}. {song} 💡 {note}")
            else:
                print(f"{i:2d}. {song}")
        
        print(f"\n{'='*60}")
        print("Album review complete!")
    
    def run_quiz(self) -> None:
        """Run the complete quiz interface."""
        print("🎵 JAY CHOU MUSIC QUIZ 🎵")
        print("Test your knowledge of Jay Chou's discography!")
        print()
        
        # Get number of questions
        while True:
            try:
                num_questions = input("How many questions would you like? (1-20): ").strip()
                num_questions = int(num_questions)
                if 1 <= num_questions <= 20:
                    break
                else:
                    print("Please enter a number between 1 and 20.")
            except ValueError:
                print("Please enter a valid number.")
        
        print(f"\nGenerating {num_questions} questions...")
        test_questions = self.generate_test(num_questions)
        
        print(f"\nTest ready! You will be asked to identify which album each song belongs to.")
        print("Press Enter to start the test...")
        input()
        
        # Run the test
        for i, question in enumerate(test_questions, 1):
            self.display_question(question, i)
            question['user_answer'] = self.get_user_answer(question)
        
        # Grade and display results
        results = self.grade_test(test_questions)
        self.display_results(results)
        
        # Ask if user wants to retake wrong questions
        if results['wrong_questions']:
            print(f"\n{'='*60}")
            retake_choice = input("Would you like to retake the questions you got wrong? (y/n): ").strip().lower()
            if retake_choice in ['y', 'yes']:
                self.run_retake_quiz(results['wrong_questions'])
        
        # Ask if user wants to review an album
        print(f"\n{'='*60}")
        review_choice = input("Would you like to review an album? (y/n): ").strip().lower()
        if review_choice in ['y', 'yes']:
            self.review_album()
        
        # Ask if user wants to play again
        print(f"\n{'='*60}")
        play_again = input("Would you like to take another test? (y/n): ").strip().lower()
        if play_again in ['y', 'yes']:
            print("\n" + "="*60)
            self.run_quiz()
        else:
            print("\nThanks for playing! 🎵")

def main():
    """Main function to run the quiz."""
    quiz = JayChouQuiz()
    
    if not quiz.data["albums"]:
        print("Error: No album data found. Please check the database file.")
        return
    
    print(f"Database loaded successfully!")
    print(f"Total albums: {len(quiz.get_all_albums())}")
    print(f"Total songs: {len(quiz.get_all_songs())}")
    print()
    
    quiz.run_quiz()

if __name__ == "__main__":
    main()