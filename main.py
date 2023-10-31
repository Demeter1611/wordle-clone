import linecache
import os
import random
from urllib import request
from colorama import Back, Style

random.seed()
NUMBER_OF_WORDS = 14855
NUMBER_OF_GUESSES_ALLOWED = 6
WORD_LENGTH = 5
VICTORY = True
if not os.path.isfile('valid-wordle-words.txt'):
    request.urlretrieve('https://gist.githubusercontent.com/dracos/dd0668f281e685bad51479e5acaadb93/raw/6bfa15d263d6d5b63840a8e5b64e04b382fdb079/valid-wordle-words.txt',
                        'valid-wordle-words.txt')


def main():
    running = True
    player_score = [0, 0]
    while running:
        interface = new_interface()
        target_word = get_random_word()
        current_guess = 0
        game_state = False

        while current_guess < NUMBER_OF_GUESSES_ALLOWED and game_state != VICTORY:
            read_interface(interface)
            input_word = check_answer(input_validation(), target_word)
            if input_word == input_word.upper():
                game_state = VICTORY
            for i in range(WORD_LENGTH):
                interface[current_guess][i] = input_word[i]
            current_guess += 1

        read_interface(interface)
        if game_state == VICTORY:
            print("\nYou won!")
            player_score[0] += 1
        else:
            print(f"\nYou lost! The word was {target_word}")
            player_score[1] += 1
        print(f"Player score: {player_score[0]}-{player_score[1]}")

        continue_game = ""
        while continue_game != 'y' and continue_game != 'n':
            continue_game = input("Continue? (y/n) ")
            if continue_game == 'n':
                running = False


def new_interface():
    """Returns a grid that is the interface of the game"""
    interface = []
    for i in range(NUMBER_OF_GUESSES_ALLOWED):
        line = []
        for j in range(WORD_LENGTH):
            line.append('-')
        interface.append(line)
    return interface


def read_interface(interface):
    """Takes the interface in the form of an array and turns it into a string"""
    for i in range(NUMBER_OF_GUESSES_ALLOWED):
        for j in range(WORD_LENGTH):
            if interface[i][j].isupper():
                print(Back.GREEN + interface[i][j], end="" + Style.RESET_ALL)
            else:
                print(interface[i][j].upper(), end="")
        print()


def get_random_word():
    """Reads a random word from the file of valid words"""
    random_line_number = random.randint(1, NUMBER_OF_WORDS)
    word = linecache.getline("valid-wordle-words.txt", random_line_number)
    return word


def check_answer(input_word: str, target_word: str):
    """Turns the letters that are found in target_word on the same position as in
        input_word to upper case letters"""
    input_after_validation = ""
    for i in range(len(input_word)):
        if input_word[i] == target_word[i]:
            input_after_validation += input_word[i].upper()
        else:
            input_after_validation += input_word[i]
    return input_after_validation


def input_validation():
    """Returns the input of the user if it's found in the list of valid words"""
    with open("valid-wordle-words.txt", encoding="utf-8") as f:
        got_input = False
        word_list = f.readlines()
        word_list = [i.strip('\n') for i in word_list]
        while not got_input:
            word = input(f"Insert a {WORD_LENGTH} letter word ")
            if word in word_list:
                got_input = True
    return word


if __name__ == "__main__":
    main()