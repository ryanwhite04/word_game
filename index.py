import random

def getChoices(n, length):
    text = open('diceware.wordlist.asc.txt', 'r').read().splitlines()
    words = [line[6:] for line in text[2:6**5+2] if len(line) is 6+length]
    return random.sample(words, k=n) 

def matchWords(a, b):
    return len([i for i, letter in enumerate(a) if letter is b[i]]);
   
def getSettings(prompt):

    while True:
        option = input(prompt).lower()[0]
        if option not in "emh":
            print("Option must be E, M, or H")
            continue
        else:
            break
    return {
        "e": { "choices": 7, "guesses": 5 },
        "m": { "choices": 8, "guesses": 4 },
        "h": { "choices": 9, "guesses": 3 },
    }[option]

def main():
    again = True # Whether or not to play again
    while (again):
        game = Game(**getSettings("Choose [E]asy, [M]edium, or [Hard]: "), length=4)
        while not game.over:
            game.prompt()
        print("You Win") if game.won else print("You Lose")
        again = input("Play Again? (yes/no)").lower() in ["yes", "y"]

class Game:

    def __init__(self, choices, guesses, length):
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
