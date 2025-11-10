import random
from typing import Set, List, Optional


class HangmanUI:
    """Handles display and user input for the Hangman game."""
    HANGMAN_PICS = [
        r"""
         +---+
         |   |
             |
             |
             |
             |
        =========""",
        r"""
         +---+
         |   |
         O   |
             |
             |
             |
        =========""",
        r"""
         +---+
         |   |
         O   |
         |   |
             |
             |
        =========""",
        r"""
         +---+
         |   |
         O   |
        /|   |
             |
             |
        =========""",
        r"""
         +---+
         |   |
         O   |
        /|\  |
             |
             |
        =========""",
        r"""
         +---+
         |   |
         O   |
        /|\  |
        /    |
             |
        =========""",
        r"""
         +---+
         |   |
         O   |
        /|\  |
        / \  |
             |
        ========="""
    ]

    def display_state(self, word_display: str, wrong_guesses: Set[str], lives_used: int, max_lives: int):
        stage = min(lives_used, len(self.HANGMAN_PICS) - 1)
        print(self.HANGMAN_PICS[stage])
        print(f"\nWord:  {word_display}")
        print(f"Miss:  {' '.join(sorted(letter.upper() for letter in wrong_guesses)) if wrong_guesses else '-'}")
        print(f"Lives: {max_lives - lives_used}/{max_lives}\n")

    def get_guess(self, previous_guesses: Set[str]) -> str:
        while True:
            guess = input("Guess a letter or word: ").strip()
            if not guess:
                print("Please enter something.")
                continue
            if not guess.isalpha():
                print("Only letters A–Z are allowed.")
                continue
            guess = guess.lower()
            if len(guess) == 1 and guess in previous_guesses:
                print("You already tried that letter.")
                continue
            return guess

    def show_result(self, won: bool, secret_word: str):
        if won:
            print(f"🎉 You won! The word was '{secret_word.upper()}'.\n")
        else:
            print(f"💀 You lost. The word was '{secret_word.upper()}'.\n")


class HangmanGame:
    def __init__(self, words: List[str], max_lives: int = 6, secret_word: Optional[str] = None):
        self.words = words
        self.max_lives = max_lives
        self.ui = HangmanUI()
        self.secret_word = (secret_word or random.choice(self.words)).lower()
        self.guessed_letters: Set[str] = set()
        self.wrong_guesses: Set[str] = set()
        self.lives_used = 0

    def get_word_display(self) -> str:
        return " ".join(ch.upper() if ch in self.guessed_letters else "_" for ch in self.secret_word)

    def make_guess(self, guess: str) -> bool:
        if len(guess) > 1:  # full-word guess
            if guess == self.secret_word:
                self.guessed_letters.update(self.secret_word)
                return True
            self.lives_used += 1
            print(f"'{guess.upper()}' is not the correct word.")
            return False

        # single-letter guess
        if guess in self.secret_word:
            if guess not in self.guessed_letters:
                self.guessed_letters.add(guess)
                print(f"✅ Good job! '{guess.upper()}' is in the word.")
            return True
        else:
            if guess not in self.wrong_guesses:
                self.wrong_guesses.add(guess)
                self.lives_used += 1
            print(f"❌ Nope! '{guess.upper()}' is not in the word.")
            return False

    def is_won(self) -> bool:
        return all(ch in self.guessed_letters for ch in self.secret_word)

    def is_lost(self) -> bool:
        return self.lives_used >= self.max_lives

    def play(self):
        while not (self.is_won() or self.is_lost()):
            word_display = self.get_word_display()
            self.ui.display_state(word_display, self.wrong_guesses, self.lives_used, self.max_lives)
            guess = self.ui.get_guess(self.guessed_letters | self.wrong_guesses)
            self.make_guess(guess)

        self.ui.display_state(self.get_word_display(), self.wrong_guesses, self.lives_used, self.max_lives)
        self.ui.show_result(self.is_won(), self.secret_word)
