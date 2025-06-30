import random, os
os.system('')

BLANK_ROW = "\033[107;30;1m ? \033[0m" * 5
ALPHABET = "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z"


def play_or_not(p_input):#decide whether to quit or start a game
    while p_input.lower() != "y" and p_input.lower() != "n":
        p_input = input("Wrong input! Try again: Y/N\n")
    if p_input.lower() == "n":
        quit()
    return True

def play_again(p_input):
    while p_input.lower() != "y" and p_input.lower() != "n":
        p_input = input("Wrong input! Try again: Y/N\n")
    if p_input.lower() == "n":
        quit()
    return True

def word_pick(): #picks a word out of a text file
    words_file_path = input("Enter path of file containing words: ")
    with open(words_file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        words = file_content.split(", ")
        return random.choice(words).lower()
    ###testword = "tests"
    ###return testword.lower()


def starting_board_view(): #displays an empty 5x6 board
    row = 0
    for row in range(6):
        print(BLANK_ROW)
    return


def check_validity(guess: str): #checks if your guessed word has 5 letters and contains only letters
    if len(guess) != 5:
        return False
    for index in guess:
        if index.isalpha() is False:
            return False
    return True


def find_index(sec_letter: str, guess: str, nonexistent_list: list): #returns a list containing indices matching current letter
    guess_index = 0
    guess_letter = ''
    match = []
    for guess_index, guess_letter in enumerate(guess):
        if guess_letter == sec_letter:
            match.append(guess_index)
        if guess_letter.upper() in nonexistent_list:
            nonexistent_list.remove(guess_letter.upper())
    return match


def check_guess(guess: str, secret: tuple, attempts: int, correct_list, wrong_list, nonexistent_list):
    current_index = 0
    target_indx = 0
    exacts = 0 # number of exactly matching letters in a guess
    matches = []
    guess_result = ['?'] * 5 #replace the slots with correct letters
    for current_index, secret_letter in enumerate(secret): ### 3, 'd'
        matches = find_index(secret_letter, guess, nonexistent_list) #gets a list of indices in guessed word, containing current secret letter
        if len(matches) != 0 and current_index not in matches: # letter exists and is not exact
            for target_indx in matches: # target_indx is the index in matches that we're going over SHOULD NOTHING HAPPEN
                if not(guess_result[target_indx].isupper()):
                    guess_result[target_indx] = secret_letter.lower()

        elif len(matches) != 0 and current_index in matches: # letter exists and is exact
            guess_result[current_index] = secret_letter.upper()
            exacts += 1

        else:
            pass
    attempts -= 1
    return correct_list, wrong_list, nonexistent_list, attempts, exacts, guess_result


def block_replace(guess_result: list):
    index = 0
    modified_results = []
    for index, letter in enumerate(guess_result):
        if letter.isupper():
            modified_results.append(f"\033[42;1m {letter} \033[0m") #green block
        elif letter == '?':
            modified_results.append(f"\033[41;1m ? \033[0m") #red block
        else:
            modified_results.append(f"\033[43;1m {letter.upper()} \033[0m") #yellow block
    return modified_results


def print_results(correct_list, wrong_list, nonexistent_list, guess_result: list, total_res: list, attempts: int):
    index = 0
    total_res.append(''.join(guess_result))
    print('----------\n' + '\n'.join(total_res) + ('\n' + BLANK_ROW) * attempts)
    print("\n" + "Unused letters: " + ", ".join(nonexistent_list) + "\n----------")
    return total_res

# uppercase letters will be correct spots, lowercase will be wrong spots!
def main():
    play_input = ""
    print("\033[45;1m Welcome to DaggersAhead's Wordle game! \033[0m")
    play_input = input("\033[44;1m Would you like to play? \033[0m Y/N\n")
    play_or_not(play_input)

    while True:
        attempts_left = 6
        secret_tup = ()
        correct_spots_list = []
        wrong_spots_list = []
        nonexistent_letters_list = ALPHABET.split(', ')
        guessed_result = []
        total_results = []  # list of strings that contain results so far
        guessed_word = ""
        secret_tup = tuple(word_pick())
        ###print(''.join(secret_tup)) #REMOVE IN FINAL
        starting_board_view() #Shows blank board
        guessed_word = input("\nEnter your guess: ").lower()
        while check_validity(guessed_word) is False:
            guessed_word = input("Not a 5 letter word! Try again: ")
        correct_spots_list, wrong_spots_list, nonexistent_letters_list, attempts_left, exact_matches, guessed_result = (
            check_guess(guessed_word, secret_tup, attempts_left,
                        correct_spots_list, wrong_spots_list, nonexistent_letters_list))
        # at this point: attempts_left = 5
        guessed_result = block_replace(guessed_result)
        total_results = print_results(correct_spots_list, wrong_spots_list, nonexistent_letters_list,
                                      guessed_result, total_results, attempts_left)

        while attempts_left > 0 and exact_matches < 5:
            guessed_word = input("Enter your guess: ").lower()
            while check_validity(guessed_word) is False:
                guessed_word = input("Not a 5 letter word! Try again: ")
            correct_spots_list, wrong_spots_list, nonexistent_letters_list, attempts_left, exact_matches, guessed_result = (
                check_guess(guessed_word, secret_tup, attempts_left,
                            correct_spots_list, wrong_spots_list, nonexistent_letters_list))
            guessed_result = block_replace(guessed_result)
            total_results = print_results(correct_spots_list, wrong_spots_list, nonexistent_letters_list,
                                          guessed_result, total_results, attempts_left)

        print(f"The word was {''.join(secret_tup).upper()}!")
        if exact_matches == 5:
            print("\033[42;1m You WIN! \033[0m\nI'm so proud...")
        if attempts_left == 0 and exact_matches < 5:
            print("\033[41;1m You LOSE! \033[0m\nGit gud...")
        play_input = input("\033[44;1m Would you like to play again? Y/N \033[0m\n")
        play_again(play_input)


main()
