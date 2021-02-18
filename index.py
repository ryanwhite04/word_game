import random

def getChoices(n, length):
    text = open('diceware.wordlist.asc.txt', 'r').read().splitlines()
    words = [line[6:] for line in text[2:6**5+2] if len(line) is 6+length]
    return random.sample(words, k=n) 

def matchWords(a, b):
    return len([i for i, letter in enumerate(a) if letter is b[i]]);
    
def main():

    again = True # Whether or not to play again

    while (again):
        print("Please select difficulty from the following:")
        for option in ["Easy", "Medium", "Hard"]:
            print(f'- {option} {option[0]}')

        selection = input().lower()
        while (selection not in ["e", "m", "h"]):
            print("Please enter e, m, or h")
            selection = input().lower()
        
        difficulty = {
            "e": { "choices": 7, "guesses": 5 },
            "m": { "choices": 8, "guesses": 4 },
            "h": { "choices": 9, "guesses": 3 },
        }[selection]

        game = Game(**difficulty)
        print("You Win") if game.begin() else print("You Lose")
        print("Play Again?")
        again = input().lower() in ["yes", "y", "sure", "why not", "absolutely", "yes please"]

class Game:

    def __init__(self, choices, guesses):
        self.choices = getChoices(choices, 6)
        self.answer = random.choice(self.choices)
        self.guesses = guesses
        self.answers = {}

    def checkOption(self, option):
        return option.isnumeric() and int(option) >= 1 and int(option) <= len(self.choices)

    def begin(self):
        win = False
        while (self.guesses and not win):
            print('Choose the correct word from')
            self.displayChoices()
            print(f'Guesses remaining: {self.guesses}') 
            print('Enter Choice')
            option = input()
            while (not self.checkOption(option)):
                print(f'Please enter a value between 1 and {len(self.choices)}')
                option = input()
            choice = self.choices[int(option) - 1]
            score = self.guess(choice)
            self.answers[choice] = score
            win = score is 6
        return win
    
    def guess(self, choice):
        self.guesses = self.guesses - 1
        return matchWords(self.answer, choice)

    def displayChoices(self):
        for i, choice in enumerate(self.choices):
            print(i+1, choice, self.answers[choice] if choice in self.answers else '')
main()
