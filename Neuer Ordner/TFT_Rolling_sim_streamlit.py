import streamlit as st
import random
from tft_class import *
from GameWindow import GameWindow  # Falls du eine spezielle Klasse für das Fenster hast

# Funktion zum Starten des Spiels
def start_game():
    gold = st.session_state.gold
    level = st.session_state.level
    stage = st.session_state.stage
    out_of_pool = st.session_state.out_pool
    
    champion_pool = create_champion_pool()
    odds = get_odds()
    champions_in_play = []
    
    global game, shop, bank, field, three_stared_list
    three_stared_list = []
    game = Game(gold, level, stage, champion_pool, odds, champions_in_play, three_stared_list=three_stared_list)
    
    if out_of_pool:
        champion_pool = game.remove_champs()
        game.champion_pool = champion_pool
    
    field = Field(game_state=game, champion_pool=champion_pool, three_stared_list=game.three_stared_list)
    bank = Bank(game_state=game, field=field, champion_pool=champion_pool, three_stared_list=game.three_stared_list)
    shop = Shop(game_state=game, odds=odds, champion_pool=champion_pool, bank=bank, field=field, three_stared_list=game.three_stared_list)
    
    st.session_state.output = f"Game gestartet!\nLevel: {level}, Stage: {stage}, Gold: {gold}"

# Streamlit UI
st.title("TFT Game Simulation")

# Input für Level
level = st.slider("Level", min_value=1, max_value=10, value=5, step=1, key="level")

# Input für Stage
stage = st.slider("Stage", min_value=1.0, max_value=10.0, value=1.0, step=0.1, key="stage")

# Input für Gold
gold = st.number_input("Gold", min_value=0, max_value=100, value=50, step=1, key="gold")

# Auswahl für Champions aus dem Pool nehmen
out_of_pool = st.checkbox("Champions aus dem Pool entfernen", key="out_pool")

# Start-Button
if st.button("Start-Simulation!"):
    start_game()

# Output-Anzeige
if "output" in st.session_state:
    st.success(st.session_state.output)

# Wenn das Spiel gestartet wurde, öffne ein neues Fenster oder einen Abschnitt
if "output" in st.session_state and st.session_state.output.startswith("Game gestartet"):
    # Hier kannst du eine neue Ausgabe anzeigen oder einen Abschnitt einfügen
    st.subheader("Spielstatus")
    
    # Beispiel für eine dynamische Anzeige der Spielinformationen
    st.write(f"Level: {st.session_state.level}")
    st.write(f"Stage: {st.session_state.stage}")
    st.write(f"Gold: {st.session_state.gold}")
    
    # Du kannst auch eine eigene Fenster-Komponente einfügen, wie GameWindow, falls du eine solche Klasse hast
    if 'game_started' not in st.session_state:
        st.session_state.game_started = True

    # Beispiel für eine neue "GameWindow"-Anzeige, wenn du sie verwendest
    if st.session_state.game_started:
        # Ein Fenster mit weiteren Spieloptionen könnte hier eingebaut werden
        GameWindow(game)  # Wenn du eine GameWindow-Klasse hast, um das Spiel darzustellen
