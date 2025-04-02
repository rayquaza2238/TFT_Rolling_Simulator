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
from TeamPlaner import TeamPlaner
import webbrowser
from Sound_App import SoundController
import pygame
# Pygame initialisieren
pygame.mixer.init()

class GameWindow(Toplevel):
    def __init__(self, parent, game, shop, bank, field):
        super().__init__(parent)
        self.master = parent
        self.title("Game Fenster")
        self.width = 1600
        self.height = 1000
        self.geometry(f"{str(self.width)}x{str(self.height)}")
        self.trait_images = []
        # Speichere die Objekte als Instanzvariablen
        self.game = game
        self.shop = shop
        self.bank = bank
        self.field = field
        self.team_planer = shared_data.team_list
        self.traits_folder = "downloaded_origins"
        self.sound_controller = SoundController(self)

        # Pygame initialisieren & Musik starten
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/background.wav")
        pygame.mixer.music.play(-1)  # Endlos-Schleife
        
        # Verschiebungen von Label und Maus
        self.verschiebung_bank_x = - 0.023
        self.verschiebung_bank_y = - 0.035
        self.verschiebung_field_x = -0.027
        self.verschiebung_field_y = -0.031
        #Weitere Eigenschaften, die im Laufe der Simulation geändert werden
        self.shop_slots = []
        self.field_slots = []
        self.field_slots_canvas = []
        self.star_labels_bank = []
        self.star_labels_field = []
        self.shop_slots = []
        self.trait_img_label = []
        self.trait_labels = []
        self.shown_labels = 0
        self.bank_slots = []  # Felder der Bank, wo Champions abgelegt werden
        self.champions_in_bank = [None] * 9  # Platz für 9 Champions auf der Bank

        # Erstelle das Hintergrundbild
        self.create_background()
        
        # Erstelle Bank mit Feldern
        self.create_widgets()
        self.create_bank()
        self.create_field()
        self.add_teamplaner_button()
        self.create_shop_slots()
        #self.add_axis_labels()
        # Ändere die Labels
        for lbl in self.bank_slots:  # Falls labels eine Liste ist
            lbl.config(font=("Arial", 18, "bold"), bg=self["bg"])

        for lbl in self.field_slots:  # Falls labels eine Liste ist
            lbl.config(font=("Arial", 18, "bold"), bg=self["bg"])

        # Wenn das Fenster geschlossen wird, soll `on_close` ausgeführt werden
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    
    def add_axis_labels(self):
        """Fügt Prozentwerte für x- und y-Achsen in 5%-Schritten hinzu."""
        # x-Achse (Prozentwerte)
        for i in range(21):  # 0% bis 100% in 5%-Schritten (daher 21 Schritte)
            x = 50 + (i * (self.width - 50) // 20)  # Berechnung der x-Koordinate für 5%-Schritte
            label = Label(self, text=f"{i * 5}%", font=("Arial", 10), bg="white", fg="black")
            label.place(x=x, y=self.height - 30)

        # y-Achse (Prozentwerte)
        for i in range(21):  # 0% bis 100% in 5%-Schritten
            y = self.height - 30 - (i * (self.height - 30) // 20)  # Berechnung der y-Koordinate für 5%-Schritte
            label = Label(self, text=f"{i * 5}%", font=("Arial", 10), bg="white", fg="black")
            label.place(x=30, y=y)

    
        
    def create_background(self):
        """Setzt ein Bild als Hintergrund."""
        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=True)

        # Bild laden (PNG, JPG, GIF)
        image_path = "niki-wichman-elderwoodtft.jpg"  # Pfad zu deinem Bild
        image = Image.open(image_path)
        image = image.resize((self.width, self.height), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(image)  # Referenz speichern!

        # Bild auf das Canvas zeichnen
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Falls du weitere Widgets auf dem Canvas platzieren willst:
        self.canvas.create_text(500, 50, text="Willkommen zum Spiel!", font=("Arial", 20), fill="white")
    
    def reset_highlight_deprec(self):
        """Setzt die Farben der Felder zurück"""
        for lbl in self.field_slots:
            lbl.config(bg=self["bg"])
        for lbl in self.bank_slots:
            lbl.config(bg=self["bg"])

    def reset_highlight(self):
        """Setzt die Farben der Felder zurück"""
        for hexagon in self.field_slots_canvas:  # Nur das Hexagon ändern
            self.canvas.itemconfig(hexagon, fill="white")  # Zur ursprünglichen Farbe zurücksetzen
    
        for lbl in self.bank_slots:
            lbl.config(bg=self["bg"])

    def create_shop_slots(self):
        self.shop.reroll_shop(self.game.level, self.game.stage)
        self.game.gold = self.game.gold + 2
        for i in range(5):
            canvas = self.create_shop_traits(self.shop.slots[i])
            canvas.place(relx=0.23 + (0.11 * i), rely=0.83, width=0.11 * self.width, height=0.18 * self.height)
            canvas.bind("<Button-1>", lambda event, index=i: self.buy_label(index))
            self.shop_slots.append(canvas)
            
    def place_labels(self, traits):
        
        for lbl in self.trait_labels:
            lbl.destroy()
        self.trait_labels.clear()

        for lbl in self. trait_img_label:
            lbl.destroy()
        self.trait_img_label.clear()
        
        unique_traits = list(traits.keys())
        y = 0
        for i in range(self.shown_labels, min(self.shown_labels + 9, len(unique_traits))):
            key = unique_traits[i]
            value = traits[key]
            new_label = Label(self, text = f"{key}: {value}", font=("Arial", 10, "bold"),fg = "black", bg="#D3D3D3")
            new_label.place(relx = 0.05, rely = 0.25 + (y * 0.03), width = 0.09 * self.width, height = 0.03 * self.height)
            im_label = Label(self, text = "")
            im_label.place(relx = 0.01, rely = 0.25 + (y * 0.03), width = 0.03 * self.width, height = 0.03 * self.height)
            self.after(50, self.update_label_image, im_label, key)
            y = y+1
            self.trait_labels.append(new_label)
            self.trait_img_label.append(im_label)
        if len(unique_traits) > 9:
            self.btn_next.place(relx = 0.05, rely = 0.3 + (y * 0.03), width = 0.05 * self.width, height = 0.05 * self.height)
        else:
            self.btn_next.pack_forget()

    
    def update_label_image(self, new_label, key):
        trait_im = f"downloaded_origins/{key}.png"
    
        # Prüfen, ob die Datei existiert
        if not os.path.exists(trait_im):
            print(f"Warnung: Bild {trait_im} nicht gefunden!")
            return
    
        # Bild laden und skalieren
        image = Image.open(trait_im)
        image = image.resize((int(0.03 * self.width), int(0.03 * self.height)), Image.LANCZOS)
        
        img = ImageTk.PhotoImage(image)
    
        # Label mit dem Bild updaten
        new_label.config(image=img, bg="grey")
        new_label.image = img  # Wichtig! Sonst wird das Bild gelöscht
    
    def toggle_labels(self):
        """Wechselt zwischen den Gruppen von Labels."""
        self.shown_labels = 9 if self.shown_labels == 0 else 0  # Zwischen den ersten 5 und den restlichen wechseln
        traits = self.get_unique_traits()
        self.place_labels(traits)

    
    def determine_labels(self, unique_traits):
        """Zeigt Labels basierend auf dem aktuellen Index an."""
        # Alte Labels entfernen
        for lbl in self.trait_labels:
            lbl.destroy()
        self.trait_labels.clear()

        unique_traits = list(unique_traits.keys())
        # Neue Labels anzeigen (maximal 5 ab aktuellem Index)
        for i in range(len(unique_traits)):
            lbl =  Label(self, text=f"{key}: {value}")
            self.trait_labels.append(lbl)
    
    

        
    
    def create_bank(self):
        """Erstelle Felder auf der Bank"""
        for i in range(9):
            bank_label = Label(self, text=f"Slot {i+1}", width=10, height=4, bg="red", relief="solid")
            bank_label.place(relx=0.23 + (i * 0.064), rely=0.73, width = int(0.058 * self.width), height = int(0.066 * self.height))
            
            # Events für Drag & Drop binden
            bank_label.bind("<Button-1>", lambda event, i=i: self.drag_start(event, i))
            bank_label.bind("<B1-Motion>", self.drag_motion)
            bank_label.bind("<ButtonRelease-1>", self.drop)
            # Rechtsklick -> Champion verkaufen
            #bank_label.bind("<Button-3>", lambda event, index=i: self.bank_sell(index))
            
            self.bank_slots.append(bank_label)

            star_label = Label(self, text="", font=("Arial", 10, "bold"), fg="black", bg="grey")
            star_label.place(relx=0.233 + (i * 0.064) + 0.04, rely=0.73, width= 0.015 * self.width, height=0.015 * self.height)
    
            self.star_labels_bank.append(star_label)

    def check_bank_slot(self, x, y):
        for i in range(9):
            x_start = (0.23 + self.verschiebung_bank_x + (i * 0.064)) * self.width
            x_end = x_start + 0.064 * self.width
            y_start = (0.73 + self.verschiebung_bank_y) * self.height
            y_end = y_start + 0.053 * self.height
            if x_start <= x <= x_end and y_start <= y <= y_end:
                return i
        #print("Sonst nicht im Feld!")
        return None

    def create_field(self):
        """Erstelle die Felder auf dem Feld"""
        hex_size = 50  # Größe der Sechsecke (Radius der Umkreisenden)
        spacing_x = math.sqrt(3) * hex_size  # Horizontaler Abstand (angepasst für Wabenstruktur)
        spacing_y = 1.5 * hex_size  # Vertikaler Abstand
        offset_x = 160  # Verschiebe nach rechts
        offset_y = 140
        for i in range(4):
            for j in range(8):
                if i % 2 == 1:
                    offset_x2 = offset_x + 0.5 * spacing_x  # Verschiebung für zweite Zeile
                else:
                    offset_x2 = offset_x  + 0  # Keine Verschiebung für andere Zeilen
                index = (i * 8) + j

                x = 0.2 * self.width + (j * spacing_x) + offset_x2
                y = 0.3 * self.height + (i * spacing_y) + offset_y
                x_rel = x / self.width
                y_rel = y / self.height
                field_label = Label(self, text=f"Slot {i+1} {j+1}", bg="white", relief="solid")
                #field_label.place(relx = 0.26 + (j * 0.067), rely = 0.5 + (i * 0.05), width=int(0.067 * self.width), height=int(0.05*self.height))
                field_label.place(relx = x_rel - 0.027, rely = y_rel - 0.03, width=int(0.053 * self.width), height=int(0.067*self.height))
                field_label.bind("<Button-1>", lambda event, index=index: self.drag_start_field(event, index))
                field_label.bind("<B1-Motion>", self.drag_motion)
                field_label.bind("<ButtonRelease-1>", self.drop_field)
                field_label.lower()
                self.field_slots.append(field_label)

                star_label = Label(self, text="", font=("Arial", 6, "bold"), fg="black", bg="grey")
                star_label.place(relx=x_rel - 0.027, rely=y_rel - 0.03, 
                             width=15, height=15)
        
                self.star_labels_field.append(star_label)


                # Bilden der Wabenstruktur
                points = self.calculate_hexagon_points(x, y, hex_size)
                # Sechseck zeichnen
                hexagon = self.canvas.create_polygon(points, fill="white", outline="black", width=2)
                text = self.canvas.create_text(x, y, text=f"Slot {i+1} {j+1}", font=("Arial", 8))
                self.field_slots_canvas.append(hexagon)
        print(self.field_slots)


    def check_field_slot(self, x, y):
        """Bestimmt die Feld-Indizes (j, i) basierend auf den gegebenen x, y-Koordinaten"""
        hex_size = 50  # Größe der Sechsecke (Radius der Umkreisenden)
        spacing_x = math.sqrt(3) * hex_size  # Horizontaler Abstand (angepasst für Wabenstruktur)
        spacing_y = 1.5 * hex_size  # Vertikaler Abstand
        offset_x = 110  # Verschiebe nach rechts
        offset_y = 110
    
        for i in range(4):  # Zeilen
            for j in range(8):  # Spalten
                # Berechne den horizontalen Versatz für ungerade Zeilen
                if i % 2 == 1:
                    offset_x2 = offset_x + 0.5 * spacing_x  # Verschiebung für zweite Zeile
                else:
                    offset_x2 = offset_x  + 0  # Keine Verschiebung für andere Zeilen
    
                # Berechne die Position des Feldes
                x_start = int(0.2 * self.width + (j * spacing_x) + offset_x2 - hex_size)
                x_end = x_start + int(2 * hex_size)  # Breite des Sechsecks
                y_start = int(0.3 * self.height + (i * spacing_y) + offset_y - hex_size)
                y_end = y_start + int(2 * hex_size)  # Höhe des Sechsecks
    
                # Prüfe, ob die gegebenen Koordinaten in diesem Bereich liegen
                if x_start <= x <= x_end and y_start <= y <= y_end:
                    index = (i * 8) + j
                    return index  # Gib die Indizes zurück
    
        return None  # Falls kein Feld gefunden wurde
        
    def calculate_hexagon_points(self, x, y, size):
        """Berechnet die sechs Ecken eines gleichseitigen Sechsecks (flache Oberseite)."""
        points = []
        for i in range(6):
            angle = math.radians(30 + 60 * i)  # Starte bei 30° für flache Seiten
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            points.extend([px, py])
        return points


    def check_field_slot_deprecated(self, x,y):
        """Bestimmt die Feld-Indizes (j, i) basierend auf den gegebenen x, y-Koordinaten"""
        for i in range(4):
            for j in range(8):
                # Berechne die Position des Feldes
                x_start = int((0.26 + self.verschiebung_field_x + (j * 0.067)) * self.width)
                x_end = x_start + int(0.067 * self.width)
                y_start = int((0.5 + self.verschiebung_field_y + (i * 0.05)) * self.height)
                y_end = y_start + int(0.05 * self.height)
    
                # Prüfe, ob die gegebenen Koordinaten in diesem Bereich liegen
                if x_start <= x <= x_end and y_start <= y <= y_end:
                    index = (i * 8) + j
                    return index # Gib die Indizes zurück
        #print("Nicht im Feld!")  # Falls kein Feld gefunden wurde
        return None

                
    def bank_sell(self, index):
        if self.bank.slots[index] is None:
            print("Kein Champ zum verkaufen!")
        else:
            print(f"{self.bank.slots[index].name} wurde verkauft!")
            self.bank.sell_champion(index)
            self.update_bank()
            self.update_gold_display()

    def field_sell(self, index):
        if self.field.slots[index] is None:
            print("Kein Champ zum verkaufen!")
        else:
            print(f"{self.field.slots[index].name} wurde verkauft!")
            self.field.sell_champion(index)
            self.update_field()
            self.update_gold_display()
            
    def drag_start_field(self, event, index):
        """Speichert die Startposition des Widgets beim Ziehen."""
        self.touched_object = self.field.slots[index] # Move Objekt
        self.touched_index = index
        self.touched_widget = event.widget
        self.touched_widget.startX = event.x_root
        self.touched_widget.startY = event.y_root
        print(f"{self.touched_widget.startX} und {self.touched_widget.startY}")

    def drop_field(self, event):
        widget_x, widget_y = self.touched_widget.winfo_x(), self.touched_widget.winfo_y()
        if 0 < widget_y < 0.70 * self.height:
            # Feldbereich: Auf andere Posi setzen wenn leer, oder posi mit unit tauschen
            index = self.check_field_slot(widget_x, widget_y)
            if index is not None: 
                slot_other_field = self.field.slots[index]
                self.field.slots[self.touched_index] = slot_other_field
                self.field.slots[index] = self.touched_object
                self.update_field()
        elif 0.80 * self.height < widget_y < self.height:
            # Unit wird verkauft
            print("Unit wird verkauft, entferne das Objekt")
            self.field_sell(self.touched_index)
            self.update_gold_display()
        elif 0.70* self.height < widget_y < 0.87 * self.height:
            # Unit auf Bank, oder Swap wenn nicht leer
            print("Tausche slot mit Bank")
            index = self.check_bank_slot(widget_x, widget_y)
            if index is not None:
                slot_bank = self.bank.slots[index]
                self.field.slots[self.touched_index] = slot_bank
                self.bank.slots[index] = self.touched_object
                self.update_field()
                self.update_bank()
        else: 
            print("Kein gültiger Bereich!")
            text = "Kein gültiger Bereich!"
            self.show_error_message(text)
        self.touched_widget.place(x=0, y=0)
        self.touched_widget = None  # Dragging abschließen
        self.reset_highlight()
    
    def drag_start(self, event, index):
        """Speichert die Startposition des Widgets beim Ziehen."""
        self.touched_object = self.bank.slots[index] # Move Objekt
        self.touched_index = index
        self.touched_widget = event.widget
        self.touched_widget.startX = event.x_root
        self.touched_widget.startY = event.y_root
        print(f"{self.touched_widget.startX} und {self.touched_widget.startY}")
    
    def drag_motion(self, event):
        """Bewegt das Widget mit der Maus."""
        x = event.x_root - self.touched_widget.startX
        y = event.y_root - self.touched_widget.startY
        widget_x, widget_y = self.touched_widget.winfo_x(), self.touched_widget.winfo_y()
        self.touched_widget.place(x=x, y=y)
        result_field = self.check_field_slot(widget_x, widget_y)
        result_bank = self.check_bank_slot(widget_x, widget_y)
        self.reset_highlight()
        if result_field is not None:
            index = result_field  # Entpacke Zeile und Spalte
            self.canvas.itemconfig(self.field_slots_canvas[index], fill="yellow")
        if result_bank is not None:
            index = result_bank
            self.bank_slots[index].config(bg = "yellow")
        
    def drop(self, event):
        """Von Bank aus"""
        widget_x, widget_y = self.touched_widget.winfo_x(), self.touched_widget.winfo_y()
        # Prüfe, ob die aktuelle Position des Widgets im Zielbereich des Frames liegt
        if 0 < widget_y < 0.70 * self.height:
            print("Unit auf Feld gesetzt!")
            # Widget innerhalb des Frames ablegen
            index = self.check_field_slot(widget_x, widget_y)
            if index is not None:
                # Check, ob da bereits ein Champ ist
                if self.field.slots[index] is not None:
                    print("Feld Slot besetzt. Bank und Feld Champ werden geswitched")
                    champ_bank = self.bank.slots[self.touched_index]
                    champ_field = self.field.slots[index]
                    self.field.slots[index]  = champ_bank
                    print(self.field.slots)
                    self.bank.slots[self.touched_index] = champ_field
                    self.update_bank()
                    self.update_field()
                else:
                    non_none_count = len([x for x in self.field.slots if x is not None])
                    print(f"{non_none_count} und {self.game.level}")
                    if non_none_count < self.game.level:    
                        champ = self.bank.slots[self.touched_index]
                        print(champ)
                        self.field.slots[index]  = champ
                        print(self.field.slots[index].name)
                        self.bank.slots[self.touched_index] = None
                        self.update_bank()
                        self.update_field()
                    else: 
                        text = "Board Cap was reached!!"
                        self.show_error_message(text)
                        print(text)
        elif 0.80 * self.height < widget_y < self.height:
            print("Unit wird verkauft, entferne das Objekt")
            self.bank_sell(self.touched_index)
            self.update_gold_display()
        elif 0.70 * self.height < widget_y < 0.87 * self.height:
            print("Auf Bank, tausche mit Slot auf Bank!")
            index = self.check_bank_slot(widget_x, widget_y)
            if index is not None:
                slot_bank = self.bank.slots[index]
                self.bank.slots[self.touched_index] = slot_bank
                self.bank.slots[index] = self.touched_object
                self.update_bank()
        else:
            print("Unit wieder auf Bank!")
            # Widget zurück an den Ursprungsort setzen
            # Evtl noch hier einfügen, dass man Champion Positionen auf der Bank tauschen kann
        self.touched_widget.place(x=0, y=0)
        self.touched_widget = None  # Dragging abschließen
        self.reset_highlight()
            
    def on_e_key(self, event):
        # Diese Funktion wird durch das Drücken der E-Taste ausgelöst
        self.refresh_slots()

    def refresh_slot_after_opening_game(self):
        self.shop.reroll_shop(self.game.level, self.game.stage)
        self.game.gold = self.game.gold + 2
        print(self.shop.slots)
        for i in range(len(self.shop.slots)):
            image = Image.open(self.shop.slots[i].png)
            print(self.shop_slots[i].winfo_width(), self.shop_slots[i].winfo_height())
            image = image.resize((200, 200), Image.LANCZOS)
            img = ImageTk.PhotoImage(image)
            self.shop_slots[i].config(image=img)
            self.shop_slots[i].config(text = "test")
            self.shop_slots[i].image = img
            tier = self.shop.slots[i].tier
            border_color = self.shop.slots[i].tier_colors.get(tier, "gray")
            self.shop_slots[i].config(image=img, bd=4, relief="solid", highlightthickness=4, highlightbackground=border_color)
            self.shop_slots[i].config(image=img)

    def create_shop_traits(self, champ):
        # Canvas erstellen
        tier = champ.tier
        border_color = champ.tier_colors.get(tier, "gray")
        canvas = Canvas(self,  width = 0.11 * self.width, height = 0.18 * self.height, bg = border_color)
        
        # Bild 1
        image3 = Image.open(f"downloaded_images/{champ.name}.png")
        image3 = image3.resize((int(0.09 * self.width), int(0.09* self.width)), Image.LANCZOS)
        photo3 = ImageTk.PhotoImage(image3)
        canvas.create_image(20, 0, image = photo3, anchor = "nw")
        canvas.create_text(100, 160, text = f"{champ.name}", font = ("Arial", 14, "bold"), fill = "black")
        canvas.image3 = photo3
        for i in range(len(champ.traits)):  
            traits = champ.traits
            image = Image.open(f"downloaded_origins/{traits[i]}.png")
            image = image.resize((int(0.015 * self.width), int(0.015* self.width)), Image.LANCZOS)
            img = ImageTk.PhotoImage(image)
            canvas.create_image(20, 90 + (i * 20), image = img, anchor = "nw")
            canvas.create_text(90, 100 + (20 * i), text = champ.traits[i], font = ("Arial", 12, "bold"), fill = "white")
            self.trait_images.append(img)
        return canvas

    
    def refresh_slots(self):
        self.team_planer = shared_data.team_list
        """Aktualisiere den Text von allen 5 Labels"""
        self.shop.reroll_shop(self.game.level, self.game.stage)
        self.update_gold_display()
        for i, label in enumerate(self.shop_slots):
            self.sound_controller.play_sound("Reroll")
            canvas = self.shop_slots[i]

            image = Image.open(self.shop.slots[i].png)
            image = image.resize((int(0.09 * self.width), int(0.09* self.width)), Image.LANCZOS)
            img = ImageTk.PhotoImage(image)

            tier = self.shop.slots[i].tier
            border_color = self.shop.slots[i].tier_colors.get(tier, "gray")

            canvas.delete("all")

            canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), 
                                fill=border_color, outline=border_color, width=4)
            canvas.create_image(20, 0, image = img, anchor = "nw")
            canvas.create_text(100, 160, text = f"{self.shop.slots[i].name}", font = ("Arial", 14, "bold"), fill = "black")
            canvas.image = img
            traits = self.shop.slots[i].traits
            for j in range(len(traits)):  
                print(traits)
                image = Image.open(f"downloaded_origins/{traits[j]}.png")
                image = image.resize((int(0.015 * self.width), int(0.015* self.width)), Image.LANCZOS)
                img = ImageTk.PhotoImage(image)
                canvas.create_image(20, 80 + (j * 20), image = img, anchor = "nw")
                canvas.create_text(90, 90 + (20 * j), text = traits[j], font = ("Arial", 12, "bold"), fill = "white")
                self.trait_images.append(img)
            if self.shop.slots[i] is not None:
                exists = any(t is not None and t.__dict__ == self.shop.slots[i].__dict__ for t in self.team_planer)
            else:
                exists = any(t is None for t in self.team_planer)  # Prüfe, ob `None` in der Liste existiert
            border_color = "gold" if exists else border_color
            thickness = 3 if exists else 2
            canvas.create_rectangle(
                thickness, thickness, 
                canvas.winfo_width() - thickness, canvas.winfo_height() - thickness, 
                outline=border_color, width=thickness
            )
            print("Gefunden" if exists else "Nicht gefunden")
        
    def buy_label(self, slot):
        "Kauft den Champ in diesem Label und ändert labelnamen"
        champion = self.shop.slots[slot]
        try: # Wenn bank ist noch nicht voll, 
            index_of_first_none = self.bank.slots.index(None)
            self.shop.buy_slot(slot)
            if self.shop.slots[slot] is not None:
                text = "You are missing gold or bank space! Unit can not be afforded"
                print("You are missing gold or bank space! Unit can not be afforded")
                self.show_error_message(text)
                #print(f"Champion in Slot {slot_index + 1} ({self.shop.slots[slot].name} wurde nicht gekauft!)")
            else:
                # Kopie der alten Liste speichern
                canvas = self.shop_slots[slot]  # Hole das Canvas-Objekt für den Slot
                canvas.delete("all")
                canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill="gray", outline="black")
                canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, 
                       text="leer", font=("Arial", 12), fill="white")
                self.sound_controller.play_sound("Buy")
                self.update_bank()
                self.update_field()
                self.update_gold_display()
        except ValueError:
            text = "Bank is full!"
            self.show_error_message(text)
            print("Bank ist voll!")


    def update_field(self):
        print(len(self.field_slots))
        for i in range(32):
            if self.field.slots[i] is None:
                self.field_slots[i].config(text = "leer")
                self.field_slots[i].config(bg="gray", image='')
                self.star_labels_field[i].config(text = "")
                self.field_slots[i].lower()
            else:
                # Bild des Champions als Hintergrund laden
                image = Image.open(self.field.slots[i].png)
                image = image.resize((self.field_slots[i].winfo_width(), self.field_slots[i].winfo_height()), Image.LANCZOS)
                img = ImageTk.PhotoImage(image)
                #self.field_slots[i].config(image=img, bg="white", bd=4, relief="solid", highlightthickness=4, highlightbackground="red")

                self.field_slots[i].config(image=img, bg="white")
                self.field_slots[i].config(image=img)
                self.field_slots[i].image = img
                self.star_labels_field[i].config(text = f"{self.field.slots[i].star_level} ★")
                self.field_slots[i].lift()
                self.star_labels_field[i].lift()
                #self.field_slots[i].config(text = f"{self.field.slots[i].name} {self.field.slots[i].star_level}")
        traits = self.get_unique_traits()
        if not traits:
            print("Keine Units auf dem Feld!")
        else:
            print(traits)
            self.place_labels(traits)
        
    def update_bank(self):
        for i in range(len(self.bank.slots)):
            if self.bank.slots[i] is None:
                self.bank_slots[i].config(text = "leer")
                self.bank_slots[i].config(bg="gray", image='')
                self.star_labels_bank[i].config(text = "")
                

            else:
                image = Image.open(self.bank.slots[i].png)
                image = image.resize((self.bank_slots[i].winfo_width(), self.bank_slots[i].winfo_height()), Image.LANCZOS)
                img = ImageTk.PhotoImage(image)
                self.bank_slots[i].config(image=img, bg="white")
                self.bank_slots[i].config(image=img)
                self.bank_slots[i].image = img
                self.star_labels_bank[i].config(text = f"{self.bank.slots[i].star_level} ★")
                self.star_labels_bank[i].lift()
                #self.bank_slots[i].config(text = f"{self.bank.slots[i].name} {self.bank.slots[i].star_level}")
    
    def get_unique_traits(self):
        if all(slot is None for slot in self.field.slots):
            print("Warnung: Keine Champions in den Slots!")
            return {}
        # Dictionary für einzigartige Champions
        unique_champions = {}
        print(self.field.slots)
        for champ in self.field.slots:
            if champ is None:  # Falls der Champion None ist, überspringe ihn
                continue
            key = (champ.name, tuple(sorted(champ.traits)))  # Eindeutige Kombination aus Name + Traits
            print(key)
            if key not in unique_champions:
                unique_champions[key] = champ  # Champion zur Dictionary hinzufügen


        trait_count = {}
    
        # Durchlaufe die einzigartigen Champions und zähle die Traits
        for champ in unique_champions.values():
            for trait in champ.traits:
                if trait in trait_count:
                    trait_count[trait] += 1
                else:
                    trait_count[trait] = 1
                    
        sorted_traits = dict(sorted(trait_count.items(), key=lambda item: item[1], reverse=True))
        print(sorted_traits)
        # Ergebnis anzeigen
        return sorted_traits

    
    def update_gold_display(self):
    # Ändere den Text des Labels
        self.gold_show_label.config(text=f"{int(self.game.gold)} 🟡")
    
    def create_widgets(self):
        self.field_frame = Frame(self, width=1*self.width, height=0.69*self.height, bg="brown")
        self.field_frame.place(relx=0, rely=0)
        self.field_frame.lower()

        self.shop_frame = Frame(self, width=1*self.width, height=0.13*self.height, bg="yellow")
        self.shop_frame.place(relx=0, rely=0.82)
        self.shop_frame.lower()

        self.bank_frame = Frame(self, width=1*self.width, height=0.17*self.height, bg="blue")
        self.bank_frame.place(relx=0, rely=0.71)#
        self.bank_frame.lower()

        self.gold_show_label = Label(self, text = f"{int(self.game.gold)} 🟡", font=("Arial", 16))
        self.gold_show_label.place(relx = 0.45, rely = 0.80, )

        # Display level odds
        colors = ["gray", "green", "blue", "purple", "gold"]  # Farben für jede Zahl
        self.level_odds_frame = Frame(self, height = self.height * 0.025, width = self.width * 0.15, bg = "darkgrey")
        self.level_odds_frame.place(relx = 0.23, rely = 0.8)
        # Werte aus der ersten Spalte holen und farbige Labels erstellen
        for i, value in enumerate(self.game.odds.iloc[:-1, self.game.level-1]):
            color = colors[i % len(colors)]
            label = Label(self.level_odds_frame, text=f"{int(value * 100)}%", bg = "darkgrey",fg=color, font=("Arial", 16))
            label.pack(side=LEFT, padx=5)
        
        # Koordinaten für das Rechteck (x1, y1, x2, y2)
        x1, y1, x2, y2 = 0.07 * self.width, 0.8 * self.height, 0.23 * self.width, 1* self.height  # Beispielwerte
        
        # Rechteck mit dunkelgrauer Farbe erstellen
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="darkgray", outline="black")
        
        # Text in die Mitte des Rechtecks setzen
        self.canvas.create_text((0.15 * self.width, 0.86 * self.height), text=f"Lvl {self.game.level}", font=("Arial", 14), fill="white")
        
        rr_btn = Button(self, text = "Reroll Shop", font=("Arial", 16), command = self.refresh_slots)
        rr_btn.place(relx = 0.1, rely = 0.9)
        self.master.bind('<e>', self.on_e_key)
        self.btn_next = Button(self, text="+", command=self.toggle_labels)

        # Ouput Label
        self.error_label = Label(self, text="", fg="red", font=("Arial", 16))
        self.error_label.place(relx = 0.4, rely = 0.5, )
        self.error_label.lift()
        self.error_label.update_idletasks()

        #Soundcontroll Button
        # Button zum Öffnen der SoundController-App
        self.sound_control_button = Button(self, text="🔊 Sound Settings", command=self.open_sound_controller)
        self.sound_control_button.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)  # Oben rechts

        # Donation Label
        self.donation_button = Button(self, text="Donate", command=self.open_link, fg="blue", font = ("Arial", 12))
        self.donation_button.place(relx = 0.02, rely = 0.02)
        self.donation_label = Label(self, text ="If you would like to support my work! \nThe Simulator will still be free. \nI would appreciate every support!")
        self.donation_label.place(relx = 0.02, rely = 0.05)
        

    def open_sound_controller(self):
        """ Öffnet das SoundController-Fenster, falls es noch nicht existiert """
        if hasattr(self, 'sound_window') and self.sound_window.winfo_exists():
            self.sound_controller.lift()  # Falls das Fenster minimiert ist, nach vorne holen
        else:
            self.sound_controller = SoundController(self)  # Neues Fenster erstellen

    
    def show_error_message(self, text):
        self.error_label.config(text=f"Error: {text}", fg="red")
        self.error_label.lift()
        self.error_label.update_idletasks()
        print("Fehler geprintet")
        self.after(3000, self.clear_error_message)

    def clear_error_message(self):
        self.error_label.config(text="")
    
    def add_teamplaner_button(self):
        open_button = Button(self, text="Teamplaner",font = ("Arial", 16, "bold"), command=self.open_team_planer)
        open_button.place(relx=0.8, rely=0.0,)  # Oben rechts

    def open_team_planer(self):
        team_planer= TeamPlaner(self, self.game)

    def open_link(self):
        webbrowser.open("https://paypal.me/duytamvu?country.x=DE&locale.x=de_DE")
        
    
    def on_close(self):
        """ Wird aufgerufen, wenn das Fenster geschlossen wird """
        pygame.mixer.music.stop()
        self.destroy()  
       



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
    self.sound_controller = SoundController()
    GameWindow(root, game, shop, bank, field, self.sound_controller)