import pandas
from tkinter import *

import random
import time


BACKGROUND_COLOR = "#B1DDC6"
LANG_FONT = ("Ariel", 25, "italic")
WORD_FONT = ("Ariel", 55, "bold")
CORRECT = 2
INCORRECT = 1

#-------------- get data for Spanish/English words -------------#

data = pandas.read_csv("spanish_words.csv", encoding='latin1')

spanish_list = data.spanish.to_list()
english_list = data.english.to_list()
translator_dict = {}
unanswered = spanish_list



for item in spanish_list:
    position = spanish_list.index(item)
    translator_dict[unanswered[position]] = english_list[position]


#---------------------------- UI Setup --------------------------#

window = Tk()
window.title("Flash Card App")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flash_card = Canvas(width=800, height=526, highlightthickness=0)
back_flash_card = Canvas(width=800, height=526, highlightthickness=0)

front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
wrong_img = PhotoImage(file="images/wrong.png")
right_img = PhotoImage(file="images/right.png")


flash_card.create_image(400, 265, image=front_card)
flash_card.config(bg=BACKGROUND_COLOR)
title_front = flash_card.create_text(400, 150, font=LANG_FONT, text=f"")
word_front = flash_card.create_text(400, 263, font=WORD_FONT, text=f"")


back_flash_card.create_image(400, 265, image=back_card)
back_flash_card.config(bg=BACKGROUND_COLOR)
title_back = back_flash_card.create_text(400, 150, font=LANG_FONT, text=f"")
word_back = back_flash_card.create_text(400, 263, font=WORD_FONT, text=f"")

#------------------------- App logic--------------------------#

chosen_word_translated = ""
indx = 0


def start(point):
    global chosen_word_translated, indx
    try:
        if point == 0:
            print("first time")
            back_flash_card.grid_remove()
            dice = random.randint(0, len(unanswered))
            choice = unanswered[dice]
            indx = unanswered.index(choice)
            flash_card.itemconfigure(title_front, text="Spanish")
            flash_card.itemconfigure(word_front, text=f"{choice}")
            flash_card.grid(column=0, row=0, columnspan=2)
            chosen_word_translated = choice

        if point != 0 and point % 2 == 0:
            print(f"Old length of Spanish list: {len(unanswered)}")
            try:
                spanish_list.remove(spanish_list[indx])
                print(f"Word removed!\nNew length of Spanish list: {len(unanswered)}")
            except IndexError:
                try:
                    spanish_list.remove(spanish_list[indx - 1])
                except IndexError:
                    print("end of list")
            finally:
                back_flash_card.grid_remove()
                dice = random.randint(0, len(unanswered))
                choice = unanswered[dice]
                flash_card.itemconfigure(title_front, text="Spanish")
                flash_card.itemconfigure(word_front, text=f"{choice}")
                flash_card.grid(column=0, row=0, columnspan=2)
                chosen_word_translated = choice

        elif point != 0 and point % 2 != 0:
            back_flash_card.grid_remove()
            dice = random.randint(0, len(spanish_list))
            choice = spanish_list[dice]
            flash_card.itemconfigure(title_front, text="Spanish")
            flash_card.itemconfigure(word_front, text=f"{choice}")
            flash_card.grid(column=0, row=0, columnspan=2)
            chosen_word_translated = choice
    except IndexError:
        if point == 0:
            print("first time")
            back_flash_card.grid_remove()
            dice = random.randint(0, len(spanish_list))
            choice = spanish_list[dice]
            indx = spanish_list.index(choice)
            flash_card.itemconfigure(title_front, text="Spanish")
            flash_card.itemconfigure(word_front, text=f"{choice}")
            flash_card.grid(column=0, row=0, columnspan=2)
            chosen_word_translated = choice

        if point != 0 and point % 2 == 0:
            print(f"Old length of Spanish list: {len(spanish_list)}")
            try:
                spanish_list.remove(spanish_list[indx])
                print(f"Word removed!\nNew length of Spanish list: {len(spanish_list)}")
            except IndexError:
                try:
                    spanish_list.remove(spanish_list[indx - 1])
                except IndexError:
                    print("end of list")
            finally:
                back_flash_card.grid_remove()
                dice = random.randint(0, len(spanish_list))
                choice = spanish_list[dice]
                flash_card.itemconfigure(title_front, text="Spanish")
                flash_card.itemconfigure(word_front, text=f"{choice}")
                flash_card.grid(column=0, row=0, columnspan=2)
                chosen_word_translated = choice

        elif point != 0 and point % 2 != 0:
            back_flash_card.grid_remove()
            dice = random.randint(0, len(spanish_list))
            choice = spanish_list[dice]
            flash_card.itemconfigure(title_front, text="Spanish")
            flash_card.itemconfigure(word_front, text=f"{choice}")
            flash_card.grid(column=0, row=0, columnspan=2)
            chosen_word_translated = choice

    window.after(3000, reveal)


def reveal():
    global chosen_word_translated
    flash_card.grid_remove()
    back_flash_card.itemconfigure(title_back, text="English", fill="white")
    back_flash_card.itemconfigure(word_back, text=f"{translator_dict[chosen_word_translated]}", fill="white")
    back_flash_card.grid(column=0, row=0, columnspan=2)
    back_flash_card.update()
    back_flash_card.grid(column=0, row=0, columnspan=2)


start(point=0)
wrong_button = Button(image=wrong_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=lambda: start(INCORRECT))
right_button = Button(image=right_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=lambda: start(CORRECT))
wrong_button.grid(column=0, row=1, padx=50, pady=50)
right_button.grid(column=1, row=1, padx=50, pady=50)

window.mainloop()

