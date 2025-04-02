
import pygame
from tkinter import *

class SoundController(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        """ Erstellt das Sound-Management-Fenster """
        self.master = master
        self.title("Sound Controller")
        self.geometry("300x800")
        
        # Pygame Mixer initialisieren (falls noch nicht geschehen)
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Sounds laden
        self.bg_music_path = "sounds/background_music.mp3"
        self.sound_effects = {
            "Reroll": pygame.mixer.Sound("sounds/reroll.wav"),
            "Buy": pygame.mixer.Sound("sounds/buy.wav"),
        }

        # Standardwerte für Lautstärken
        self.bg_volume = 1.0
        self.sfx_volume = 1.0
        self.bg_music_muted = False
        self.sound_effects_muted = False

        # GUI erstellen
        self.create_widgets()

    

    def toggle_bg_music(self):
        """ Schaltet die Hintergrundmusik an oder aus """
        if self.bg_music_muted:
            pygame.mixer.music.set_volume(self.bg_volume)
            self.bg_music_button.config(text="Mute BG Music 🎵")
        else:
            pygame.mixer.music.set_volume(0.0)
            self.bg_music_button.config(text="Unmute BG Music 🔇")
        self.bg_music_muted = not self.bg_music_muted

    def toggle_sound_effects(self):
        """ Schaltet die Soundeffekte an oder aus """
        if self.sound_effects_muted:
            for sound in self.sound_effects.values():
                sound.set_volume(self.sfx_volume)
            self.sound_effect_button.config(text="Mute Sound FX 🔊")
        else:
            for sound in self.sound_effects.values():
                sound.set_volume(0.0)
            self.sound_effect_button.config(text="Unmute Sound FX 🔇")
        self.sound_effects_muted = not self.sound_effects_muted

    def set_bg_volume(self, volume):
        """ Setzt die Lautstärke der Hintergrundmusik """
        self.bg_volume = float(volume)
        if not self.bg_music_muted:
            pygame.mixer.music.set_volume(self.bg_volume)

    def set_sfx_volume(self, volume):
        """ Setzt die Lautstärke der Soundeffekte """
        self.sfx_volume = float(volume)
        if not self.sound_effects_muted:
            for sound in self.sound_effects.values():
                sound.set_volume(self.sfx_volume)

    def play_sound(self, sound_name):
        """ Spielt den gewünschten Soundeffekt ab """
        if sound_name in self.sound_effects:
            self.sound_effects[sound_name].play()

    def create_widgets(self):
        """ Erstellt die GUI-Elemente (Buttons, Slider) """
        # Mute-Buttons
        self.bg_music_button = Button(self, text="Mute BG Music 🎵", command=self.toggle_bg_music, width=20)
        self.bg_music_button.pack(pady=5)

        self.sound_effect_button = Button(self, text="Mute Sound FX 🔊", command=self.toggle_sound_effects, width=20)
        self.sound_effect_button.pack(pady=5)

        self.bg_label = Label(self, text = "BG Volume").pack(pady=5)
        self.bg_slider = Scale(
            self, from_=0, to=1, resolution=0.01, orient="horizontal",
            length=200, label="BG Volume", command=self.set_bg_volume
        )
        self.bg_slider.set(self.bg_volume)  # Setzt den Slider auf die aktuelle Lautstärke
        self.bg_slider.pack(pady=10)

        self.sfx_label = Label(self, text = "SFX Volume").pack(pady=5)
        self.sfx_slider = Scale(
            self, from_=0, to=1, resolution=0.01, orient="horizontal",
            length=200, label="SFX Volume", command=self.set_sfx_volume
        )
        self.sfx_slider.set(self.sfx_volume)  # Setzt den Slider auf die aktuelle Lautstärke
        self.sfx_slider.pack(pady=10)

    def on_close(self):
        """ Wird aufgerufen, wenn das Fenster geschlossen wird """
        self.destroy()  # Fenster schließen, damit es erneut geöffnet werden kann




