from practice import to_learn  # Not used in the code, consider removing

from tkinter import *  # Importing everything can lead to conflicts, consider importing only what's needed
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}  # Dictionary to store the current flashcard set later

# Load the CSV file
try:
    df = pd.read_csv("data/words_to_learn.csv")  # Attempt to load saved progress
except FileNotFoundError:
    df_ = pd.read_csv("data/french_words.csv")  # Load default word list if save file is missing
    to_learn = df_.to_dict(orient="records")  # Convert dataframe to a list of dictionaries
else:
    to_learn = df.to_dict(orient="records")

flip_timer = None  # Stores timer reference for auto-flipping cards

# Create the main window
windows = Tk()
windows.title("Flashy")  # App title
windows.config(padx=50, pady=50, bg=BACKGROUND_COLOR)  # Padding and background color

# Create canvas for flashcards
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")  # Front image
card_back_img = PhotoImage(file="images/card_back.png")  # Back image
canvas_image = canvas.create_image(400, 263, image=card_front_img)  # Place front image
canvas.grid(column=0, row=0, columnspan=2)  # Center canvas
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

# Function to flip the card
def flip_card():
    global current_card  # Ensure global scope
    current_card = random.choice(to_learn)  # Choose a random word
    canvas.itemconfig(card_title, text="English")  # Switch title to English
    canvas.itemconfig(card_word, text=current_card["English"])  # Display translation
    canvas.itemconfig(canvas_image, image=card_back_img)  # Flip card image

# Text elements for flashcard
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 40, "bold"), fill="black")

# Function to show the next card
def next_card():
    global flip_timer, current_card  # Ensure global scope
    if flip_timer:
        windows.after_cancel(flip_timer)  # Cancel previous timer if active

    current_card = random.choice(to_learn)  # Choose new word
    canvas.itemconfig(card_title, text="French")  # Display in French
    canvas.itemconfig(card_word, text=current_card["French"])  # Show word
    canvas.itemconfig(canvas_image, image=card_front_img)  # Show front image
    flip_timer = windows.after(3000, func=flip_card)  # Auto-flip after 3 seconds

# Function when the user knows a word
def right_button_clicked():
    to_learn.remove(current_card)  # Remove known word
    data = pd.DataFrame(to_learn)  # Convert updated list to dataframe
    data.to_csv("data/words_to_learn.csv", index=False)  # Save progress
    print(len(to_learn))  # Debugging: print remaining words
    next_card()  # Move to the next word

# Button images and placement
wrong_image = PhotoImage(file="images/wrong.png")  # Load 'wrong' button image
wrong_button = Button(command=next_card, image=wrong_image, highlightthickness=0)  # Clicking shows next card
wrong_button.grid(row=1, column=0)  # Position button

right_image = PhotoImage(file="images/right.png")  # Load 'right' button image
right_button = Button(command=right_button_clicked, image=right_image, highlightthickness=0)  # Clicking removes known card
right_button.grid(row=1, column=1)  # Position button

next_card()  # Start app with a word
windows.mainloop()  # Run Tkinter event loop