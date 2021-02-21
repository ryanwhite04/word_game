import random


def getChoices(n, length):
    """
    Returns a list of 'n' random words of length 'length' from the diceware list
    
    The diceware test file first has the non word lines and the indexes removed
    The list is then filtered so only words of length "length" remain

        Parameters:
            n (int): number of words to return
            length (int): length of words to return
        Returns:
            (list): chosen words
    """
    text = open('diceware.wordlist.asc.txt', 'r').read().splitlines()
    words = [line[6:] for line in text[2:6**5+2] if len(line) is 6+length]
    return random.sample(words, k=n) 

def matchWords(a, b):
    """Return number of matching letters (same position and character)"""
    return len([i for i, letter in enumerate(a) if letter is b[i]]);
   
def getSettings(prompt):
    """
    Return user selected difficulty
    Keeps prompting user until they enter valid input

        Parameters:
            prompt (str): Message to prompt user for difficulty
        Returns:
            Dictionary with keys "choices" and "guesses"
    """
    while True:
        # By using only the first letter
        # this code also allows Easy, Medium or Hard
        option = input(prompt).lower()[0]
        if option not in "emh":
            print("Option must be E, M, or H")
            continue
        else:
            break
    return {
        # these were the values provided in the assignment outline
        "e": { "choices": 7, "guesses": 5 },
        "m": { "choices": 8, "guesses": 4 },
        "h": { "choices": 9, "guesses": 3 },
    }[option]

def main():
    again = True # Whether or not to play again
    while (again):
        game = Game(**getSettings("Choose [E]asy, [M]edium, or [Hard]: "))
        while not game.over:
            game.prompt()
        print("You Win") if game.won else print("You Lose")
        again = input("Play Again? (yes/no)").lower() in ["yes", "y"]

class Game:
    """A word game that can prompt the player for a guess until they win or lose

    Args:
        choices (int): How many choices of word to choose from
        guesses (int): How many guesses the player has
        length (int): character length of each choice. Defaults to 6
    
    Attributes:
        choices (list): Choices available to player
        answer (str): The password (answer)
        guesses (int): how many guesses the player has
        answers: (dictionary):
            keys are previously guesses options
            values are the number of correct characters for the chosen option
        length: length of words to use as choices (defaults to 6)
        over: whether or not the game is over
    """

    def __init__(self, choices, guesses, length=6):
        self.choices = getChoices(choices, length)
        self.answer = random.choice(self.choices)
        self.guesses = guesses
        self.answers = {}
        self.length = length
        self.over = False

    # Kevin: https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
    def getOption(self, prompt):
        while True:
            try:
                option = int(input(prompt)) - 1
            except ValueError:
                print("It has to be a number")
                continue
            if option < 0 or option >= len(self.choices):
                print(f'Please enter a value between 1 and {len(self.choices)}')
                continue
            elif self.choices[option] in self.answers:
                print("You selected this previously, try a new word")
                continue
            else:
                break
        return option

    def prompt(self):
        self.displayChoices()
        option = self.getOption("Enter your selection: ")
        choice = self.choices[int(option)]
        self.guesses -= 1
        score = matchWords(self.answer, choice)
        self.answers[choice] = score
        self.won = score is self.length
        self.over = self.guesses is 0 or self.won
    
    def displayChoices(self):
        print('Choose the correct word from')
        for i, choice in enumerate(self.choices):
            print(i+1, choice, self.answers[choice] if choice in self.answers else '')
        print(f'Guesses remaining: {self.guesses}') 
main()
