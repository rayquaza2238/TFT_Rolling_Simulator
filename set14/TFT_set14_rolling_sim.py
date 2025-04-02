import random
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math
import numpy as np
from matplotlib.widgets import Slider
from tft_class import *
from tkinter import Toplevel, Label, Button, Frame , Canvas, PhotoImage
from PIL import Image, ImageTk
from collections import defaultdict
import copy
import os
import shared_data
import json
from TeamPlaner import TeamPlaner
from GameWindow import GameWindow
from Sound_App import SoundController

import sys


def start_game():
    gold = int(entry_gold.get())
    level = int(level_scale.get())
    stage = float(stage_scale.get())
    out_of_pool = out_pool_slider.get()
    champion_pool = create_champion_pool()
    print(out_of_pool)
    
    odds = get_odds()
    champions_in_play = []
    
    global game, shop, bank, field, three_stared_list
    three_stared_list = []
    game = Game(gold, level, stage, champion_pool, odds, champions_in_play, three_stared_list = three_stared_list)
    if out_of_pool:
        champion_pool = game.remove_champs()
        game.champion_pool  = champion_pool
    field = Field(game_state = game, champion_pool = champion_pool, three_stared_list = three_stared_list)
    bank = Bank(game_state = game, field = field, champion_pool = champion_pool, three_stared_list = three_stared_list)
    shop = Shop(game_state = game, odds = odds, champion_pool = champion_pool, bank = bank, field = field, three_stared_list = three_stared_list)
    label_output.config(text=f"Game gestartet!\nLevel: {level}, Stage: {stage}, Gold: {gold}")
    GameWindow(root, game, shop, bank, field,)


# Tkinter-Hauptfenster
root = Tk()

# Level Slider (von 1 bis 10)
level_label = Label(root, text="Level:")
level_label.pack()
level_scale = Scale(root, from_=1, to=10, orient="horizontal")
level_scale.pack()

# Stage Slider (von 0.0 bis 10.0)
stage_label = Label(root, text="Stage:")
stage_label.pack()
stage_scale = Scale(root, from_=1.0, to=10.0, orient="horizontal", resolution=0.1)
stage_scale.pack()

# Gold
Label(root, text="Gold:").pack()
entry_gold = Entry(root)
entry_gold.pack()

# Champions aus dem Pool nehmen
out_pool_label = Label(root, text ="Wähle ja oder nein, wenn Champions aus dem Pool genommen werden sollen")
out_pool_slider = Scale(root, from_=0, to=1, orient="horizontal", length=50, showvalue=0)
out_pool_slider.config(label="Nein  Ja")
out_pool_label.pack()
out_pool_slider.pack()
# Start Knopf
start_label = Label(root, text = "Starte das Spiel!")
start_label.pack()
start_button = Button(root, text = "Start-Simulation!", command = start_game)
start_button.pack()

# Commands Interactive Simulation



# Output
label_output = Label(root, text="'Willkommen!", fg="blue")
label_output.pack()
# Tkinter-Event-Schleife starten
root.mainloop()
