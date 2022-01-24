from tkinter import *
import pandas
import random
import shutil

BACKGROUND_COLOR = "#B1DDC6"

timer = None


# reading csv using pandas

def create_new_word_list():
    # copying and renaming base file
    original = r'data/french_words.csv'
    target = r'data/words_to_learn.csv'
    shutil.copyfile(original, target)


try:
    word_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError and pandas.errors.EmptyDataError:
    create_new_word_list()
    word_data = pandas.read_csv("data/words_to_learn.csv")

word_pairs_dict = word_data.to_dict(orient="records")
# print(word_pairs_dict)
random_word_pair_dict = random.choice(word_pairs_dict)


# ------------------ Yes-No-button ------------------------
def known_word():
    word_pairs_dict.remove(random_word_pair_dict)
    to_learn = pandas.DataFrame(word_pairs_dict)
    to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def next_card():
    global random_word_pair_dict, flip_timer
    window.after_cancel(flip_timer)
    random_word_pair_dict = random.choice(word_pairs_dict)
    canvas.itemconfig(card_word, text=f"{random_word_pair_dict['French']}", fill="black")
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_image, image=card_front)
    flip_timer = window.after(3000, card_flip)


def card_flip():
    global random_word_pair_dict
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(card_word, text=f"{random_word_pair_dict['English']}", fill="white")
    canvas.itemconfig(card_title, text="English", fill="white")


# def known_word():


window = Tk()
window.title("Flashy cards")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, card_flip)

card_back = PhotoImage(file="images/card_back.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_image = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

# create buttons
button_right = Button()
right_image = PhotoImage(file="images/right.png")
button_right.config(highlightthickness=0, image=right_image, command=known_word)
button_right.grid(column=1, row=1)

button_wrong = Button()
wrong_image = PhotoImage(file="images/wrong.png")
button_wrong.config(highlightthickness=0, image=wrong_image, command=next_card)
button_wrong.grid(column=0, row=1)

next_card()

window.mainloop()
