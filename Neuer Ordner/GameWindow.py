import streamlit as st

class GameWindow:
    def __init__(self, game):
        self.game = game
        self.create_window()

    def create_window(self):
        st.subheader("Spielstatus")
        
        # Aktuelle Level-, Stage- und Gold-Daten anzeigen
        st.write(f"Level: {self.game.level}")
        st.write(f"Stage: {self.game.stage}")
        st.write(f"Gold: {self.game.gold}")
        
        # Zeige die Champions im aktuellen Team
        st.write("Aktuelle Champions im Team:")
        if self.game.champions_in_play:
            for champ in self.game.champions_in_play:
                st.write(f"- {champ.name} (Level: {champ.level})")
        else:
            st.write("Keine Champions im Team")
        
        # Zeige den aktuellen Bankstatus an
        st.write("Bankstatus:")
        st.write(f"Gold in der Bank: {self.game.gold}")
        
        # Shop-Button: Beispiel für eine Interaktion im Fenster
        if st.button("Shop öffnen"):
            self.open_shop()

        # Weitere Funktionen und Interaktionen hinzufügen
        if st.button("Simuliere nächsten Kampf"):
            self.simulate_battle()

    def open_shop(self):
        st.write("Willkommen im Shop! Hier kannst du Champions kaufen.")
        # Hier könntest du Logik hinzufügen, um Champions zu kaufen

    def simulate_battle(self):
        st.write("Der Kampf wird simuliert...")
        # Hier könnte Logik für den Kampf hinzugefügt werden
        # Zum Beispiel: Berechnung von Ergebnissen, Anzeige von Kampfergebnissen etc.
        st.write("Kampf abgeschlossen!")

# Beispielaufruf des GameWindow in deiner Hauptfunktion
# Angenommen, game ist ein bereits initialisiertes Spielobjekt
# GameWindow(game) würde dann in der Funktion `start_game()` nach dem Klick auf den Button aufgerufen werden
