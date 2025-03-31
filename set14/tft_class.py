import requests
import json
import os
import re
import pandas as pd
import random
from collections import defaultdict
import copy
import champs_py_pool

def check_if_in_three_stared_list(champion, three_star_list):
        print(three_star_list)
        """Prüft, ob ein Champion mit dem gleichen Namen, Traits und Tier existiert."""
        if not three_star_list:  # Überprüft, ob die Liste leer ist
            return False  
        print(three_star_list)
        return any(
            champion.name == champ.name and
            champion.traits == champ.traits
            for champ in three_star_list
        )


def remove_champion(champion_to_remove, three_stared_list):
    print(f"vor raus tun {three_stared_list}")
    # Entfernt den Champion aus der Liste, wenn die Attribute übereinstimmen
    for champ in three_stared_list:
        if champ.name == champion_to_remove.name and champ.traits == champion_to_remove.traits:
            three_stared_list.remove(champ)
    print(f"Ich tu jetzt raus!{three_stared_list}")
    return three_stared_list


def create_champion_pool():
    data_rolling = champs_py_pool.champs_py_pool_dic
        
    pool_sizes = [30, 25, 18, 10, 9,]

    champions = [Champion(entry["name"], entry["cost"], entry["traits"], entry["tier"]) for entry in data_rolling]
    champion_pool_multiplicator = [pool_sizes[champ.get_cost() - 1] for champ in champions]
    
    # Erstelle für jedes Duplikat eine neue Instanz von Champion
    champion_pool = [
        Champion(champ.name, champ.cost, champ.traits, champ.tier)  # Neue Instanz wird hier erstellt
        for champ, size in zip(champions, champion_pool_multiplicator)
        for _ in range(size)
    ]
    return champion_pool

def get_odds():
    data = {
        1: ["100%", "75%", "55%", "45%", "30%", "19%", "18%", "15%", "5%", "1%"],
        2: ["0%", "25%", "30%", "33%", "40%", "30%", "25%", "20%", "10%", "2%"],
        3: ["0%", "0%", "15%", "20%", "25%", "40%", "32%", "25%", "20%", "12%"],
        4: ["0%", "0%", "0%", "2%", "5%", "10%", "22%", "30%", "40%", "50%"],
        5: ["0%", "0%", "0%", "0%", "0%", "1%", "3%", "10%", "25%", "35%"],
    }
    
    # DataFrame erstellen
    odds = pd.DataFrame(data)
    
    # Prozentwerte umwandeln: "0%" → 0 (int), andere Werte → float / 100
    for col in odds.columns[:]:  # Überspringt die "Level"-Spalte
        odds[col] = odds[col].apply(lambda x: 0 if x == "0%" else float(x.rstrip("%")) / 100)
    odds[6] = 0.00
    # DataFrame ausgeben
    odds = odds.T
    #print(odds)
    return odds


def create_nested_champs(champions):
    """Erstellt eine verschachtelte Liste nach Tier."""
    nested_champs = [[] for _ in range(6)]  # Liste mit 5 leeren Listen für Tiers 1-5
    
    # Verteilt die Champions in die entsprechenden Tier-Listen
    for champ in champions:
        if 1 <= champ.tier <= 6:  # Falls der Tier-Wert im Bereich 1-5 ist
            nested_champs[champ.tier - 1].append(champ)  # Index für Tier 1 ist 0, für Tier 2 ist 1, etc.
    
    return nested_champs

def check_triple(champions):
    # Filtern von None-Werten
    filtered_champions = [champ for champ in champions if champ is not None]
    
    for i, champ in enumerate(filtered_champions):
        count = filtered_champions.count(champ)  # Zählt, wie oft dieses Objekt in der gefilterten Liste vorkommt
        if count == 3:  # Wenn ein Champion 3-mal vorkommt
            print(f"Champion {champ.name} {champ.star_level} {champ.traits} wurde 3 mal gefunden!")
            return champ

class Champion:
    def __init__(self, name, cost, traits, tier ,star_level = 1, max_star_level = 3):
        self.name = name
        self.cost = cost
        self.traits = traits
        self.tier = tier
        self.star_level = star_level
        self.max_star_level = max_star_level
        self.png = f"downloaded_images/{self.name}.png"

        self.tier_colors = {
            1: "white",
            2: "green",
            3: "blue",
            4: "purple",
            5: "gold"
        }

        if not os.path.exists(self.png):
            print(f"Warnung: Bild für {self.name} fehlt!")

    def __repr__(self):
        return f"Champion(name={self.name}, cost={self.cost}, traits={self.traits}, star_level={self.star_level}, png={self.png})"

    
    
    def check_duplicates(self, lst):
        count = 0
        for champ in lst [0]:
            if champ is not None:  # Prüfen, ob champ kein None ist
                #print(champ)
                if champ.name == self.name and champ.star_level == self.star_level and champ.traits == self.traits:
                    count += 1
    
        if count >= 2:
            print("Es gibt mindestens zwei Objekte mit denselben Attributen.")
            return True
    

    def upgrade_level(self):
        """Erstellt eine neue Instanz mit höherem Star-Level, wenn möglich."""
        if self.star_level < self.max_star_level:
            print("Drei dieser Champs werden nun zu einer kombiniert!")
            new_star_level = self.star_level + 1
            new_cost = (3 * self.cost - 1) if self.tier > 1 else (3 * self.cost)
            upgraded_champ = Champion(
                    name=self.name,
                    cost=new_cost,
                    traits=self.traits,
                    tier=self.tier,
                    star_level=new_star_level
                )
                
            return upgraded_champ
        else:
            print("Max Star ist erreicht!")
            #entferne alle Champions mit den selben Attributen aus champion_pool
            return None  # Falls Max-Level erreicht ist, kein neues Objekt

    def __eq__(self, other):
        if isinstance(other, Champion):
            return (self.name == other.name and
                    self.cost == other.cost and
                    self.traits == other.traits and
                    self.star_level == other.star_level)
        return False  # Falls der andere nicht vom Typ Champion ist
    
    # get Methoden
    def get_name(self):
        return self.name
    def get_cost(self):
        return self.cost
    def get_traits(self):
        return self.traits

    

champions_in_play = []

class Game:
    def __init__(self,gold, level, stage, champion_pool, odds,  champions_in_play, three_stared_list):
        self.level = level
        self.stage = stage
        self.gold = gold
        self.champion_pool = champion_pool
        self.odds = odds
        self.champions_in_play = champions_in_play
        self.three_stared_list = three_stared_list
        self.removal_rules = {
            1: {1: 8,},  # Entferne 1x cost=2, 2x cost=4
            2: {1: 20, 2: 4},
            3: {1: 24, 2: 8, 3: 4},
            4: {1: 32, 2: 16, 3: 6,},
            5: {1: 64, 2: 30, 3: 12, 4: 2,},
            6: {1: 8*3*3, 2: 8*3*2, 3: 8*3*1, 4: 6},
            7: {1: 8*3*4, 2: 8*3*3, 3: 8*3*1, 4: 12, 5: 1},
            8: {1: 8*3*3, 2: 8*3*3, 3: 8*3*2, 4: 8*3, 5: 4},
            9: {1: 8*3*3, 2: 8*3*3, 3: 8*3*3, 4: 8*3*2, 5: 8},
            10: {1: 8*3*3, 2: 8*3*3, 3: 8*3*4, 4: 8*3*4, 5: 4*3}
        }
        
    def __repr__(self):
        return f"GameField(gold={self.gold}, level={self.level}, stage={self.stage})"

    def get_unique_champs(self):
        """
        Erstellt eine Liste mit einzigartigen Champions, basierend auf (name, cost, trait).
        """
        seen = set()  # Set für einzigartige Kombinationen
        unique_champs = []  # Ergebnisliste
    
        for champ in self.champion_pool:
            key = (champ.name, champ.cost, tuple(champ.traits), champ.tier)  # Tupel als eindeutiger Schlüssel
            if key not in seen:
                seen.add(key)
                unique_champs.append(copy.deepcopy(champ))  # Champion zur Liste hinzufügen
    
        return unique_champs  

    def remove_champs(self):
        """
        Entfernt basierend auf der gegebenen Zahl `num` eine bestimmte Anzahl von Champions
        mit bestimmten Kosten (cost-Wert).
        
        Args:
            champ_list (list): Liste mit Champ-Instanzen.
            num (int): Gibt an, wie viele Champions entfernt werden sollen.
        
        Returns:
            list: Gefilterte Liste ohne die entfernten Champions.
        """
        # Definiere, wie viele Champions pro cost-Wert entfernt werden sollen
        print(len(self.champion_pool))
        num = self.level
        # Zähle, wie viele Champions mit jeder `cost`-Stufe in der Liste sind
        champ_dict = defaultdict(list)
        for champ in self.champion_pool:
            champ_dict[champ.cost].append(champ)
    
        # Entferne basierend auf den Regeln
        for cost, remove_count in self.removal_rules[num].items():
            if cost in champ_dict and champ_dict[cost]:  # Falls Champions mit dieser cost existieren
                champ_dict[cost] = champ_dict[cost][remove_count:]  # Überschreibt die Liste ohne die ersten `remove_count` Elemente

        
        # Neue Liste aus den verbliebenen Champions erstellen
        filtered_list = [champ for champs in champ_dict.values() for champ in champs]
        print("Units wurden aus dem Pool genommen.")
        print(len(filtered_list))
        return filtered_list

class Shop:
    def __init__(self,game_state, odds, champion_pool, bank, field, three_stared_list,  slots = None, ):
        if slots is None:
            slots = [None] * 5
        self.slots = slots
        self.field = field
        self.bank = bank
        self.odds = odds
        self.champion_pool = champion_pool
        self.game_state = game_state
        self.three_stared_list = three_stared_list

    def buy_xp(self):
        # kauft xp
        print("Kauft Xp")


    
    
    def reroll_champ_slot(self, level, stage):
        shop_odds = self.odds[level-1]
        cost_list = [1,2,3,4,5, 6]
        while True:
            shop_cost = random.choices(cost_list, weights=shop_odds, k=1)[0]
            cost_champs = [champ for champ in self.champion_pool if champ.cost == shop_cost]
    
            # Falls es Champions mit cost == x gibt, einen zufällig auswählen
            if cost_champs:
                chosen_champ = random.choice(cost_champs)
                print(f"Zufälliger Champion: {chosen_champ.name}")
                check_3_star = check_if_in_three_stared_list(chosen_champ, self.three_stared_list)
                print(check_3_star)
                if check_3_star:
                    print(f"{chosen_champ.name} hat bereits 3 Sterne. Wird übersprungen.")
                    # Champion bleibt im Pool, die Schleife geht weiter
                    continue
                else:
                    # Champion hat keine 3 Sterne, daher kann er entfernt werden
                    print(f"{chosen_champ.name} wird zum Shop hinzugefügt.")
                    self.champion_pool.remove(chosen_champ)
                    return chosen_champ
            else:
                print(f"Kein Champion mit cost == {shop_cost} gefunden.")
        

    def reroll_shop(self, level, stage):
        if self.game_state.gold < 2:
            print("Nicht genug Gold zum Rollen!")
        else:
            for champ in self.slots:
                if champ is not None:  # Falls ein Champion vorhanden ist
                    self.champion_pool.append(champ)
            
            for i in range(len(self.slots)):
                rolled_champ = self.reroll_champ_slot(level, stage)
                self.slots[i] = rolled_champ  # Direktes Ändern der Listenelemente

                #Wenn gekauft, überprüfe, ob es Duplikate auf dem Feld oder auf der Bank gibt
                list_bank_field = [self.field.slots + self.bank.slots]
                check_duplicated = rolled_champ.check_duplicates(list_bank_field)
                if check_duplicated:
                    print(f"Du hast ein Duplikat von {rolled_champ.name}!")
                    print(f"Highlighte {rolled_champ.name}!")
            self.game_state.gold = self.game_state.gold - 2
            return self.slots


    # Kaufe ein Champion, setze den gekauften Champ aus dem Slot zur Bank
    def buy_slot(self, slot):
        wanna_buy_slot = self.slots[slot]
        if wanna_buy_slot is None:
            print("Unit wurde bereits gekauft!")
        else:
            cost = wanna_buy_slot.cost
            if self.game_state.gold < cost:
                print("Du kannst diesen Champ nicht kaufen!")
            else:
                print(f"Der Champ {wanna_buy_slot.name} wird gekauft!")
                # Jedesmal, wenn ein Champ gekauft wird, dann soll champions_in_play aktualisiert werden
                list_bank_field = [self.field.slots + self.bank.slots]
                check_duplicated = wanna_buy_slot.check_duplicates(list_bank_field)
                if check_duplicated:
                    # löscht die duplikate, damit die zusammen kombiniert werden können
                    self.bank.slots = [
                            None if x and x.name == wanna_buy_slot.name and x.star_level == wanna_buy_slot.star_level and x.traits == wanna_buy_slot.traits else x
                            for x in self.bank.slots
                        ]

                    self.field.slots = [
                        None if x and x.name == wanna_buy_slot.name and x.star_level == wanna_buy_slot.star_level and x.traits == wanna_buy_slot.traits else x
                        for x in self.field.slots
                    ]

                    print(f"{wanna_buy_slot.name} wird upgegraded!")
                    wanna_buy_slot = wanna_buy_slot.upgrade_level()
                    #print(f"{self.bank.slots}")
                    self.bank.add_champ_to_bank(wanna_buy_slot)
                    self.game_state.gold = self.game_state.gold - wanna_buy_slot.cost
                    self.slots[slot] = None

                    # Zweiter Check für 3 star
                    list_bank_field = [self.field.slots + self.bank.slots]
                    check_tripled = check_triple(list_bank_field[0])
                    if check_tripled:
                        # löscht die duplikate, damit die zusammen kombiniert werden können
                        self.bank.slots = [
                                None if x and x.name == check_tripled.name and x.star_level == check_tripled.star_level and x.traits == check_tripled.traits else x
                                for x in self.bank.slots
                            ]
    
                        self.field.slots = [
                            None if x and x.name == check_tripled.name and x.star_level == check_tripled.star_level and x.traits == check_tripled.traits else x
                            for x in self.field.slots
                        ]
                        print(f"{check_tripled.name} wird zu 3 upgegraded!")
                        check_tripled = check_tripled.upgrade_level()
                        self.bank.add_champ_to_bank(check_tripled)
                        # Es ist nun ein 3 Star
                        self.three_stared_list.append(check_tripled)
                        print(self.three_stared_list)
                    return wanna_buy_slot
                else:
                    self.bank.add_champ_to_bank(wanna_buy_slot)
                    self.game_state.gold = self.game_state.gold - wanna_buy_slot.cost
                    self.slots[slot] = None


class Bank:
    def __init__(self, game_state, champion_pool, field, three_stared_list,  slots = None,):
        if slots is None:
            slots = [None] * 9
        self.slots = slots
        self.field = field
        self.game_state = game_state
        self.champion_pool = champion_pool
        self.three_stared_list = three_stared_list


    def add_champ_to_bank(self, champ):
        if None in self.slots:
            index_of_first_none = self.slots.index(None)
            self.slots[index_of_first_none] = champ
            print(f"{champ.name} wurde gekauft!")
        else:
            print("Bank ist voll, verkaufe eine Unit!")
            

    

    
    def sell_champion(self, slot):
        wanna_sell_champ = self.slots[slot]
        if wanna_sell_champ is None:
            print("Es gibt hier keine Unit zu verkaufen!")
        else:
            num_new_champs = 3 ** (wanna_sell_champ.star_level - 1)  # Potenzberechnung für neue Instanzen
            for _ in range(num_new_champs):  # Erstelle neue Instanzen
                self.champion_pool.append(Champion(name=wanna_sell_champ.name, traits=wanna_sell_champ.traits, star_level=1, cost=wanna_sell_champ.tier, tier = wanna_sell_champ.tier))
            print(f"{wanna_sell_champ.name} wurde verkauft!")
            if wanna_sell_champ.star_level == 3:
                new_list = remove_champion(wanna_sell_champ, self.three_stared_list)
                self.three_stared_list = new_list
                print(f"{wanna_sell_champ.name} ist wieder im Pool!")
            self.game_state.gold = self.game_state.gold + wanna_sell_champ.cost
            self.slots[slot] = None
            
    def put_champ_on_field(self, slot_on_field, slot_bank):
        champ = self.slots[slot_bank]
        self.field.slots[slot_on_field] = champ
        print(f"Die unit {champ.name} wurde auf das Feld mit slot {slot_on_field} gesetzt!")
        self.slots[slot_bank] = None


class Field:
    def __init__(self, game_state, champion_pool, three_stared_list,  bank = None, slots = None):
        if slots is None:
            slots = [None] * 32
        if bank is None:
            bank = []
        self.bank = bank
        self.game_state = game_state
        self.champion_pool = champion_pool
        self.three_stared_list = three_stared_list
        self.slots = slots

    def put_champ_on_bank(self, slot_on_field, slot_bank):
        champ = self.slots[slot_on_field]
        self.bank.slots[slot_bank] = champ
        print(f"Die unit {champ.name} wurde auf die Bank mit slot {slot_bank} gesetzt!")
        self.slots[slot_on_field] = None


    def sell(self):
        """Verkaufe den Champion und erstelle neue Instanzen basierend auf star_level."""
        print(f"{self.name} wurde verkauft!")
        new_champs = []
        for _ in range(self.star_level * 3):  # Erstelle neue Instanzen
            new_champs.append(Champion(name=self.name, traits=self.traits, star_level=1, cost=self.cost))
        return new_champs
        
    def sell_champion(self, slot):
        wanna_sell_champ = self.slots[slot]
        if wanna_sell_champ is None:
            print("Es gibt hier keine Unit zu verkaufen!")
        else:
            num_new_champs = 3 ** (wanna_sell_champ.star_level - 1)  # Potenzberechnung für neue Instanzen
            for _ in range(num_new_champs):  # Erstelle neue Instanzen
                self.champion_pool.append(Champion(name=wanna_sell_champ.name, traits=wanna_sell_champ.traits, star_level=1, cost=wanna_sell_champ.tier, tier = wanna_sell_champ.tier))
            # Wenn dieser Champ 3 Sterne war, dann muss dieser aus der three_stared_list raus
            if wanna_sell_champ.star_level == 3:
                self.three_stared_list.remove(wanna_sell_champ)
                print(f"direkt nach verkauf{self.three_stared_list}")
                print(f"{wanna_sell_champ.name} ist wieder im Pool!")
            print(f"{wanna_sell_champ.name} wurde verkauft!")
            self.game_state.gold = self.game_state.gold + wanna_sell_champ.cost
            self.slots[slot] = None

