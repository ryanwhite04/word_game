# Word Game

## index.py

### main loop

The main loop of the program runs until the player chooses to stop playing
  A new game is created after prompting the user for the difficulty
  While the game hasn't ended
    The player is prompted to keep guessing
  Once the game has ended, the player is informed if they won or lost
  The player is then asked if they want to replay
    If not, the game ends
    

### Game class

A game accepts 3 inputs
  
- The number of words to choose from
- The number of guesses the player gets before losing
- The length of the words
  
From these inputs the following are created

- A list of the words the player can choose from
- The correct answer the player is trying to guess
- The number of guesses the player has left
- The answers the player has already selected (with their correspoinding matches)
- The length of the words
- Whether or not the game is over (starting false)

### game.prompt
From this game the program repeatedly prompts the player for a selection
This process is as follows:

1. Display the choices the player has
2. Get a selection from the player (a number corresponding to the choise
3. get the corresponding word matching their cohice
4. Reduce their remaining guesses by 1
5. Calculate the score of their choice
6. Store their score in the list of previous guesses
7. If their score is the same as the word length, store that the game has been won
8. If there are no guesses left, or the game has been won, set that the game is over

### game.getOption

The player is prompted for a selection from the list of words
If they haven't entered a number, ask them again
If they haven't entered a number corresponding to an option, ask them again
If they have entered a valid option but it was selected previously, ask them again
Otherwise return their choice

### game.displayChoices

1. Print the instructions for the player
2. For each word in the possible choices
  Print the word followed by the number of correct letters if it was selected previously
3. Print the number of remaining guesses

### Get choices

The wordlist hasn't been distributed yet, so the game loads a list of words from Diceware
The file is stripped so only the words remain as a list
The words are filtered to a desired length passed into the function
The number of words passed to the function are chosen randomly from the fitlered list and returned

### Match Words

Return the number of matching characters and positions of each letter in 2 words
The words are itereated by character and matching letters are filtered out
The length of these filtered characters is returned

### Get Settings

The user is prompted for their desired difficulty
If the response doesn't stat with E, e, M, m, H, or h, they are told to enter a new value
Based on their response, the number of choices and guesses for the game is returned
The choices and guesses corresponding to each difficulty setting are as follows from the assignment outline

- Easy: 7 Choices and 5 Guesses
- Medium: 8 Choices and 4 Guesses
- Hard: 9 Choices and 3 Guesses
