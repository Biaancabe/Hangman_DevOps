from hangman_game import HangmanGame

WORD_LIST = [
    "python", "algorithm", "variable", "keyboard",
    "planet", "mountain", "chocolate", "governance"
]

def ask_secret_word():
    print("===== HANGMAN OOP EDITION =====")
    print("Tip: einfach Enter drücken für ein zufälliges Wort.")
    while True:
        secret = input("Eigenes geheimes Wort (oder Enter für Zufall): ").strip()
        if secret == "":
            return None
        if secret.isalpha():
            return secret
        print("Nur Buchstaben A–Z, bitte.")

def choose_lives(default=6):
    choice = input("Schwierigkeitsgrad [E]asy=7, [N]ormal=6, [H]ard=5 (Enter=N): ").strip().lower()
    return {"e":7, "n":6, "h":5}.get(choice, default)

def main():
    while True:
        secret = ask_secret_word()
        lives = choose_lives()
        game = HangmanGame(WORD_LIST, max_lives=lives, secret_word=secret)
        game.play()
        if not game.ui.ask_replay():
            print("Danke fürs Spielen! 👋")
            break

if __name__ == "__main__":
    main()
