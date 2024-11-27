# Author: Mark Ira Galang
# Date Created: 05/12/23
# Date Last Modified: 03/07/24
# File Name: Wordle.py

from tkinter import *    
import tkinter as tk 
import random

# grabs the list of words and converts it into a list
with open(".\words.txt") as f:
    Wordle_List = f.read().splitlines()

# max letters before the next guess
MAX_LETTER = 5

# global variables
row = 0
word = ""
randomized_word = Wordle_List[random.randint(0,len(Wordle_List))]
randomized_word_list = list(randomized_word)

chars = {}
for char in randomized_word:
    if char in chars:
        chars[char] += 1
    else:
        chars[char] = 1

# testing
# print(randomized_word)

# check word checks if word is the wordle, if not gives the user how close the word is
# also tells the user they have lost if everything is over
def check_word():
    global word, row

    counter = chars.copy()

    if word == randomized_word:
        for i in range(5):
            row_button = int(keyboard_list.index(word[i:i+1].upper()) / 9)
            column_button = int(keyboard_list.index(word[i:i+1].upper()) % 9)
            labels_for_words[row][i+2].configure(bg="light green")  
            buttons_for_keyboard[row_button][column_button].configure(bg="light green")
    else:
        for i in range(5):
            row_button = int(keyboard_list.index(word[i:i+1].upper()) / 9)
            column_button = int(keyboard_list.index(word[i:i+1].upper()) % 9)

            current_char = word[i:i+1]
            if current_char in randomized_word_list and counter.get(current_char, 0) >= 1:
                counter[current_char] -= 1
                if current_char == randomized_word_list[i]:
                    labels_for_words[row][i+2].configure(bg="light green")
                    buttons_for_keyboard[row_button][column_button].configure(bg="light green")
                else:
                    if buttons_for_keyboard[row_button][column_button]["bg"] != "light green":
                        labels_for_words[row][i+2].configure(bg="yellow")

                    if buttons_for_keyboard[row_button][column_button]["bg"] != "light green":
                        buttons_for_keyboard[row_button][column_button].configure(bg="yellow")
            else:
                labels_for_words[row][i+2].configure(bg="gray")

                if buttons_for_keyboard[row_button][column_button]["bg"] not in ("light green", "yellow"):
                    buttons_for_keyboard[row_button][column_button].configure(bg="gray")

        labelState.configure(text=f"{word} is not quite right! Try Again!")
        word = ""

    row += 1

    if word == randomized_word:
        labelState.configure(text="You Win! Press Reset to Try Again")
    elif row == 6:
        labelState.configure(text=f"You Lose! The Word is {randomized_word}. Press Reset to Try Again")


# add word adds words to the board
def add_word(char):
    global word
    global row

    # this adds both into the board and into word variable to check
    if (len(word) < MAX_LETTER):
        labels_for_words[row][len(word)+2].configure(text=char)
        word += char.lower() + ""

    if (len(word) == MAX_LETTER):
        # checks if the word is on the list
        if word in Wordle_List:
            check_word()
        
        # tells the user that word is invalid
        else:
            for i in range (5):
                labels_for_words[row][i+2].configure(bg="red")   

            temp = str(word) + " is not in the dictionary"
            labelState.configure(text=temp)

# removes a letter
def backSpace():
    global row
    global word
    
    # this removes both on the board and the word variable
    if len(word) > 0:
        labels_for_words[row][len(word) + 1].configure(text="__", bg="light gray")
        word = word[:-1]

# resets the game
# resets the game
def reset():
    global row, word, randomized_word, randomized_word_list, chars

    row = 0
    word = ""
    randomized_word = random.choice(Wordle_List)
    randomized_word_list = list(randomized_word)
    
    # Update chars with the new randomized_word
    chars = {}
    for char in randomized_word:
        if char in chars:
            chars[char] += 1
        else:
            chars[char] = 1

    for i in range(6):
        for j in range(10):
            if j < 2 or j > 6:
                continue
            else:
                labels_for_words[i][j].configure(text="__", bg="light gray")  
    
    for i in range(3):
        for j in range(9):
            buttons_for_keyboard[i][j].configure(bg="light gray")

    labelState.configure(text="Game has been Reset! Please enter a word.")
    
# main
root = tk.Tk()
root.title("Wordle Recreation")
root.geometry("930x750")
root.resizable(width=0, height=0)

# create a 2D array for the guess board
labels_for_words = [[] for i in range(6)]

# this for loop adds empty labels at the sides and the board in the middle
for i in range (6):
    for j in range (9):
        if j < 2 or j > 6:
            temp_label = tk.Label(root, text="     ", font="Georgia 50")
            labels_for_words[i].append(temp_label)
        else:
            temp_label = tk.Label(root, text="__", font="Georgia 50",bg="light gray")
            labels_for_words[i].append(temp_label)
        
# this for loops grids the board
for i in range(6):
    for j in range(9):
        labels_for_words[i][j].grid(row=i, column=j, sticky=NSEW)

# a list for the keyboard at the bottom
keyboard_list = ["Q","W","E","R","T","Y","U","I","O",
                 "A","S","D","F","G","H","J","K","P",
                 "L","Z","X","C","V","B","N","M","<<<"]

# 2D list for keyboard
buttons_for_keyboard = [[] for i in range(9)]

# count is to iterate through keyboard list
count = 0
for i in range (3):
    for j in range (9):
        temp_button = Button()

        # if it is a backspace, enter the backSpace function, otherwise it is a letter; add word function
        if keyboard_list[count] == "<<<":
            temp_button = tk.Button(root, text="<", command=lambda: backSpace())
        else:
            temp_button = tk.Button(root, text=keyboard_list[count], command=lambda i=keyboard_list[count]: add_word(i),padx=30)

        temp_button.configure(font="Georgia 20", bg="light gray")
        buttons_for_keyboard[i].append(temp_button)
        count += 1

count = 0
# this puts it into a grid at the bottom
for i in range(3):
    for j in range(9):
        if keyboard_list[count] == "<<<":
            buttons_for_keyboard[i][j].grid(row=i+6, column=j, columnspan=2,sticky=NSEW)
        else:
            buttons_for_keyboard[i][j].grid(row=i+6, column=j,sticky=NSEW)
        
# a label at the bottom to indicate the state of the game, if the word is valid, etc.
labelState = tk.Label(root, text="Welcome to wordle! Please enter a word.")
labelState.grid(row=10, columnspan=10)

# a button to reset the game
reset_button = Button(root, text="Reset Game Button", command=lambda: reset())
reset_button.grid(row=11, columnspan=10)

# main loop
root.mainloop()