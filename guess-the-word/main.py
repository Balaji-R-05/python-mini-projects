import random
import time


word_bank = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew"]

def play_game():
    start_time = time.time()
    word = random.choice(word_bank)
    guessed_word = ['_'] * len(word)
    guessed_letters = set()
    wrong_guesses = set()
    attempts = 10

    print("🎉 Welcome to the Word Guessing Game!")
    print("Try to guess the word letter by letter.")
    print("The word has", len(word), "letters.")

    while attempts > 0:
        print("\n🔤 Current word: " + ' '.join(guessed_word))
        print("📉 Attempts left:", attempts)
        print("📚 Guessed letters:", ' '.join(sorted(guessed_letters | wrong_guesses)))

        guess = input("Enter a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("⚠️ Please enter a single letter.")
            continue

        if guess in guessed_letters or guess in wrong_guesses:
            print("❗ You already guessed that letter.")
            continue

        if guess in word:
            guessed_letters.add(guess)
            for i, char in enumerate(word):
                if char == guess:
                    guessed_word[i] = guess
            print("✅ Nice guess!")
        else:
            wrong_guesses.add(guess)
            attempts -= 1
            print("❌ Wrong guess!")

        if '_' not in guessed_word:
            elapsed_time = round(time.time() - start_time, 2)
            print(f"⏱️ You took {int(elapsed_time)} seconds!")
            print("\n🎉 Congratulations!! You guessed the word: " + word)
            break
    else:
        elapsed_time = round(time.time() - start_time, 2)
        print(f"⏱️ You took {int(elapsed_time)} seconds!")
        print("\n💀 You've run out of attempts! The word was: " + word)

# Main loop for replay option
while True:
    play_game()

    again = input("\n🔁 Do you want to play again? (y/n): ").strip().lower()
    if again not in ('yes', 'y'):
        print("👋 Thanks for playing! Goodbye!")
        break