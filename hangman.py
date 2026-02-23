import random

welcome_msg = ('Welcome to the game Hangman')

draw = (r'''
 | |  | |
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \\
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |
                     |___/''')

HANGMAN_ASCII_ART = welcome_msg + "\n" + draw
MAX_TRIES = 6

# מילון הממפה בין מספר הטעויות לייצוג הויזואלי של האיש התלוי
HANGMAN_PHOTOS = {
    0: """    x-------x""",
    1: """    x-------x
    |
    |
    |
    |
    |""",
    2: """    x-------x
    |       |
    |       0
    |
    |
    |""",
    3: """    x-------x
    |       |
    |       0
    |       |
    |
    |""",
    4: """    x-------x
    |       |
    |       0
    |      /|\\
    |
    |""",
    5: """    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |""",
    6: """    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |"""
}


def check_valid_input(letter_guessed, old_letters_guessed):
    """Checks if the guessed letter is a single English character and hasn't been guessed before.
        :param letter_guessed: The character entered by the user
        :param old_letters_guessed: List of characters already guessed
        :type letter_guessed: str
        :type old_letters_guessed: list
        :return: True if input is valid and new, False otherwise
        :rtype: bool
        """
    letter_guessed = letter_guessed.lower()
    # בדיקה שהקלט הוא באורך 1, מכיל רק אותיות ולא נוחש בעבר
    if len(letter_guessed) != 1 or not letter_guessed.isalpha() or letter_guessed in old_letters_guessed:
        return False
    return True


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """Updates the guessed letters list or notifies the user if the input is invalid.
        :param letter_guessed: The character entered by the user
        :param old_letters_guessed: List of characters already guessed
        :type letter_guessed: str
        :type old_letters_guessed: list
        :return: True if the letter was added to the list, False otherwise
        :rtype: bool
        """
    letter_guessed = letter_guessed.lower()
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed)
        return True
    else:
        # הדפסת X ורשימת האותיות שנבחרו כבר במקרה של קלט לא תקין
        print('X')
        sorted_list = sorted(old_letters_guessed)
        output = " -> ".join(sorted_list)
        print(output)
        return False


def show_hidden_word(secret_word, old_letters_guessed):
    """Creates a string representing the secret word with guessed letters and underscores.
        :param secret_word: The word to be guessed
        :param old_letters_guessed: List of characters already guessed
        :type secret_word: str
        :type old_letters_guessed: list
        :return: A string of letters and underscores separated by spaces
        :rtype: str
        """
    result = ""
    for x in secret_word:
        # בונה את המחרוזת המוצגת למשתמש - אותיות שנחשפו או קווים תחתונים
        if x in old_letters_guessed:
            result += (x + " ")
        else:
            result += ('_' + " ")
    return result.strip()


def check_win(secret_word, old_letters_guessed):
    """Checks if the player has guessed all the letters in the secret word.
        :param secret_word: The word the player needs to guess
        :param old_letters_guessed: The list of letters already guessed
        :type secret_word: str
        :type old_letters_guessed: list
        :return: True if all letters are guessed, False otherwise
        :rtype: bool
        """
    secret_word = secret_word.lower()
    for letter in secret_word:
        # אם יש אות אחת במילה הסודית שלא נמצאת ברשימת הניחושים - אין עדיין ניצחון
        if letter not in old_letters_guessed:
            return False
    return True


def choose_word(file_path, index):
    """Selects a secret word from a file based on a given index.
        :param file_path: Path to the text file containing words
        :param index: Position of the word in the file
        :type file_path: str
        :type index: int
        :return: A tuple containing the number of unique words and the chosen secret word
        :rtype: tuple
        """
    try:
        with open(file_path, "r") as f:
            words = f.read().split()
        num_unique = len(set(words))  # חישוב כמות המילים הייחודיות בעזרת set
        # חישוב האינדקס במעגל למקרה שהאינדקס שהוזן גדול מכמות המילים
        target_index = (index - 1) % len(words)
        secret_word = words[target_index]
        return (num_unique, secret_word)
    except FileNotFoundError:
        # טיפול במקרה שהקובץ לא קיים בנתיב שניתן
        print(f"Error: The file {file_path} was not found.")
        exit()


def main():
    print(HANGMAN_ASCII_ART)
    var = input("enter a file :")
    var_2 = input("enter index :")
    try:
        # המרת הקלט של האינדקס למספר שלם
        var_2 = int(var_2)
    except ValueError:
        # טיפול במקרה שהמשתמש הכניס טקסט במקום מספר
        print("Error: Index must be a number!")
        exit()
    print(var)
    print(var_2)
    num_words, secret_word = choose_word(var, var_2)
    secret_word = secret_word.lower()  # נרמול המילה לאותיות קטנות למניעת באגים
    old_letters_guessed = []
    num_of_tries = 0

    # לולאת המשחק המרכזית - רצה כל עוד לא נגמרו הניסיונות ולא היה ניצחון
    while (num_of_tries < (MAX_TRIES)) and (not check_win(secret_word, old_letters_guessed)):
        print(HANGMAN_PHOTOS[num_of_tries])
        print(show_hidden_word(secret_word, old_letters_guessed))
        guess_letter = input("Guess a letter: ")
        var_3 = try_update_letter_guessed(guess_letter, old_letters_guessed)
        # אם הניחוש תקין אך האות לא קיימת במילה - מעלים את מונה הטעויות
        if var_3 and guess_letter not in secret_word:
            num_of_tries += 1

    if check_win(secret_word, old_letters_guessed) == True:
        print('WIN')
    else:
        # הדפסת הודעת הפסד במקרה שהלולאה הסתיימה עקב כמות טעויות
        print("LOSE):")


# קוד עזר ליצירת קובץ הבדיקה במידה ואינו קיים בסביבת העבודה
words_content = "hangman computer python israel apple banana orange"
with open("words.txt", "w") as f:
    f.write(words_content)
print("File 'words.txt' created successfully!")

if __name__ == "__main__":
    main()