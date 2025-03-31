import random
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math
import numpy as np
from matplotlib.widgets import Slider
from tft_class import Game, Shop, Bank, Field, create_champion_pool, get_odds, check_triple, create_nested_champs
from tkinter import Toplevel, Label, Button, Frame , Canvas, PhotoImage
from PIL import Image, ImageTk
from collections import defaultdict
import copy
import os
import shared_data
import json

class TeamPlaner(Toplevel):
    def __init__(self, master, game):
        super().__init__(master)
        self.title("TeamPlaner")
        self.width = 1200
        self.height = 600
        self.geometry(f"{str(self.width)}x{str(self.height)}")
        
        # Attribute
        self.game = game
        self.unique_champions = self.game.get_unique_champs()  # Annahme: Diese Methode gibt eine Liste von Champions zurück
        self.selected_champions = [None] * 10
        self.plan_labels = []
        container = Frame(self)
        container.pack(fill="both", expand=True)
        
        # Linker Bereich (mit Scrollbar)
        left_frame = Frame(container, bg="lightblue")
        left_frame.grid(row=0, column=0, sticky="nswe")  # Füllt die ganze Spalte
        
        canvas = Canvas(left_frame)
        scrollbar = Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)
        
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Champion abbilden
        self.create_label_for_every_champ()
        
        # Rechter Bereich (statischer Text)
        right_frame = Frame(container, bg="lightgray", width=200)
        right_frame.grid(row=0, column=1, sticky="nswe")
        # Teamplaner abbilden
        self.create_planer(right_frame)

        
        
        # Spalten gleichmäßig wachsen lassen
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=2)
        container.grid_rowconfigure(0, weight=1)
        

    
    def create_label_for_every_champ(self):
        """Erstellt ein Label für jeden Champion in der verschachtelten Liste."""
        row = 0  # Zeilenindex
        col = 0  # Spaltenindex
        i = 1
        nested_champs = create_nested_champs(self.unique_champions)
        print(nested_champs)
        for tier_list in nested_champs:
            # Tier-Label erstellen
            tier_label = Label(self.scrollable_frame, text=f"Tier {i}", font=("Arial", 12, "bold"),)
            #tier_label.place(relx=0.01, rely=0.01 + (row * 0.07))  # Tier-Label einfügen
            tier_label.grid(row = row, column = col, padx = 5, pady = 5, sticky = "w")
            row += 1  # Zeile nach Tier-Label weiter verschieben
    
            # Erstelle für jeden Champion ein Label
            for champ in tier_list:
                champ_label = Label(self.scrollable_frame, text=f"{champ.name} (Tier {champ.tier})", font=("Arial", 10), width=int(0.08 * self.width), height=int(0.08 * self.width))
                champ_label.grid(row = row, column = col, padx = 5, pady = 5, sticky = "w")
                #champ_label.place(relx=0.01 + (col * 0.23), rely=0.01 + (row * 0.1), width=int(0.2 * self.width), height=int(0.1 * self.height))  # Platzierung des Labels
                print(f"Platzieren des Labels für {champ.name} bei Zeile {row}, Spalte {col}")
                # Bild für Champion laden
                image = Image.open(champ.png)
                image = image.resize((int(0.08 * self.width), int(0.08 * self.width)), Image.LANCZOS)
                img = ImageTk.PhotoImage(image)
                champ_label.config(image=img, bg="white", bd=4, relief="solid", highlightthickness=1, highlightbackground="gray")
                champ_label.image = img
                champ_label.bind("<Button-1>", lambda event, champ=champ: self.add_champ_to_list(champ))

                # Aktualisiere Spalte
                col += 1
                if col == 4:  # Nach 4 Labels eine neue Zeile beginnen
                    col = 0
                    row += 1
            
            # Spalte und Zeile nach einem Tier-Block zurücksetzen
            col = 0
            row += 1
            i += 1
    


                    
    def add_champ_to_list(self, champ):
        champ_copy = copy.deepcopy(champ)
    
        # Überprüfe, ob der Champion bereits in der Liste ist
        if champ_copy in self.selected_champions:
            print(f"Champion {champ_copy.name} ist bereits in der Liste.")
            return
    
        # Prüfe, ob es noch einen None-Wert in der Liste gibt
        if None in self.selected_champions:
            index = self.selected_champions.index(None)  # Finde das erste None
            self.selected_champions[index] = champ_copy  # Ersetze es durch den Champ
            print(f"Champion {champ_copy.name} wurde zur Liste an Position {index} hinzugefügt.")
            print(self.selected_champions)
            #self.save_team_list()
            self.update_planer()
        else:
            print("Kein Platz mehr in der Liste, Champion kann nicht hinzugefügt werden.")


        
    def create_planer(self, fixed_frame):
        """Fügt 10 Labels in der rechten Seite (fixed_frame) hinzu, 2 Gruppen mit 5 Labels."""
        # Erste Gruppe mit 5 Labels

        for i in range(2):
            for j in range(5):
                planer_label = Label(fixed_frame, text="", font=("Arial", 10), bg = "lightgray")
                planer_label.grid(row=i + 1, column=j, padx=5, pady=5, sticky="w")
                index = (i * 5) + j
                self.plan_labels.append(planer_label)
                planer_label.bind("<Button-1>", lambda event, index=index: self.remove_champ(event, index))
                # Button zum clearen der Liste
        #clear_btn = Button(right_frame, text = "Clear", command = self.clear_planer)
        #clear_btn.grid(col = 1, row = 0)
        self.update_planer()
                #self.update_planer()

    def update_planer(self):
        for i in range(len(self.selected_champions)):
            if self.selected_champions[i] is None:
                print("Nichts ist hier!")
                self.plan_labels[i].config(bg = "lightgray", image = "")
            else:
                image = Image.open(self.selected_champions[i].png)
                image = image.resize((100, 100), Image.LANCZOS)
                img = ImageTk.PhotoImage(image)
                self.plan_labels[i].config(image=img)
                self.plan_labels[i].image = img
        shared_data.team_list = self.selected_champions
        print(f"Hier {shared_data.team_list}")

    def remove_champ(self,event, index):
        self.selected_champions[index] = None
        #self.save_team_list()
        self.update_planer()
        
    
    def clear_planer(self):
        self.selected_champions = [None] * 10
        #self.save_team_list()
        self.update_planer()
        