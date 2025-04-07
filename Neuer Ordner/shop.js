class Shop {
    constructor(game, bank, field, slots = []) {
        this.game = game;
        this.bank = bank;
        this.field = field;
        this.slots = slots.length ? slots : Array(5).fill(null);
    }

    reroll_unit_slot(){
        let shop_odds = this.game.odds;
        let cost_list = [1,2,3,4,5, 6];
        while (true){
            let shop_cost = this.weightedRandomChoice(cost_list, shop_odds);
            console.log(shop_cost);
            //console.log("shop_cost", shop_cost);
            let cost_units = this.game.champion_pool.filter(unit => unit.cost === shop_cost);
            console.log(cost_units);
            //console.log(cost_units, "const_units");
            if (cost_units) {
                let chosen_unit = this.getRandomChoice(cost_units);
                console.log(chosen_unit);
                let check_3_star = this.game.check_if_in_three_stared_list(chosen_unit);
                console.log("three_stared_list", check_3_star);
                if (check_3_star) {
                    continue;
                }
                else {
                    let index = this.game.champion_pool.indexOf(chosen_unit);
                    if (index > -1) {
                        this.game.champion_pool.splice(index, 1);  // Entfernt das Element an der Position index
                    }
                    return chosen_unit;
                }
            }
        }
    }

    getRandomChoice(array) {
        const randomIndex = Math.floor(Math.random() * array.length);
        return array[randomIndex];
    }
     
    weightedRandomChoice(costList, shopOdds) {
        // Erstelle ein Array mit den kumulierten Wahrscheinlichkeiten
        let cumulativeWeights = [];
        let cumulativeSum = 0;
    
        // Berechne die kumulierten Gewichte
        for (let i = 0; i < shopOdds.length; i++) {
            cumulativeSum += shopOdds[i];
            cumulativeWeights.push(cumulativeSum);
        }
    
        // Generiere eine Zufallszahl im Bereich [0, 1)
        let randomValue = Math.random() * cumulativeSum;
    
        // Finde den Index, der der Zufallszahl entspricht
        for (let i = 0; i < cumulativeWeights.length; i++) {
            if (randomValue < cumulativeWeights[i]) {
                return costList[i]; // Rückgabe des Werts an der entsprechenden Index-Position
            }
        }
    }
    
    check_triple(champions){
        const filtered_champions = champions.filter(champ => champ !== null);

        for (let i = 0; i < filtered_champions.length; i++) {
            const champ = filtered_champions[i];

            // Zählt, wie oft ein Champion (nach name, traits, cost) vorkommt
            let count = 0;
            for (let j = 0; j < filtered_champions.length; j++) {
                const other = filtered_champions[j];
                if (
                    champ.name === other.name &&
                    champ.cost === other.cost &&
                    JSON.stringify(champ.traits) === JSON.stringify(other.traits)
                ) {
                    count++;
                }
            }

            if (count === 3) {
                console.log(`Champion ${champ.name} ${champ.star_level} ${champ.traits} wurde 3 mal gefunden!`);
                return champ;
            }
        }

        return null; // Falls keiner 3-mal vorkommt
    }

    reroll_shop() {

        if (this.game.gold < 2) {
            console.log("Nicht genug Gold zum Rollen!");
        }
        else {
            //Every Slot will be put into the pool before refreshing the shop
            for (let champ of this.slots) {
                if (champ != null) {
                    this.game.champion_pool.push(champ);
                }
            }
            for (let i = 0; i < this.slots.length; i++) {
                let rolled_champ = this.reroll_unit_slot();
                this.slots[i] = rolled_champ;
                //If bought, check, if there are duplicates to upgrade
                let list_bank_field = this.field.slots.concat(this.bank.slots);
                let check_duplicated = rolled_champ.check_duplicates(list_bank_field);
                console.log('duplicated_champ', rolled_champ.name, check_duplicated);

                if (check_duplicated == true) {
                    console.log("You have two copies, Highlight Champ!");
                }
            }
            this.game.gold = this.game.gold - 2;
            return this.slots;
        }
    }


    buy_slots(slot) {
        let wanna_buy_slot = this.slots[slot];
        console.log(wanna_buy_slot);
        if (wanna_buy_slot == null) {
            console.log("Unit already bought!");
        }
        else {
            let cost = wanna_buy_slot.cost;
            if (this.game.gold < cost) {
                console.log("Not enough gold!");
            }
            else {
                console.log(`Unit ${wanna_buy_slot.name} will be bought!`);
                let list_bank_field = this.field.slots.concat(this.bank.slots);
                let check_duplicated = wanna_buy_slot.check_duplicates(list_bank_field);
                console.log('duplicated_champ', wanna_buy_slot.name, check_duplicated);
                if (check_duplicated == true) {
                    //delete the duplicates, so you can buy unit!
                    this.bank.slots = this.bank.slots.map(x => {
                        if (
                            x && 
                            x.name === wanna_buy_slot.name &&
                            x.star_level === wanna_buy_slot.star_level &&
                            JSON.stringify(x.traits) === JSON.stringify(wanna_buy_slot.traits)
                        ) {
                            return null;
                        }
                        else {
                            return x;
                        }
                    });
                    this.field.slots = this.field.slots.map(x => {
                        if (
                            x && 
                            x.name === wanna_buy_slot.name &&
                            x.star_level === wanna_buy_slot.star_level &&
                            JSON.stringify(x.traits) === JSON.stringify(wanna_buy_slot.traits)
                        ) {
                            return null;
                        }
                        else {
                            return x;
                        }
                    });
                    console.log(`Unit ${wanna_buy_slot.name} will be upgraded!`);
                    wanna_buy_slot = wanna_buy_slot.upgrade_level();
                    this.bank.add_champ_to_bank(wanna_buy_slot);
                    this.game.gold = this.game.gold - wanna_buy_slot.cost;
                    this.slots[slot] = null;

                    //Second Check for three star
                    let list_bank_field = this.bank.slots.concat(this.field.slots);
                    let check_tripled = this.check_triple(list_bank_field);
                    if (check_tripled) {
                        //hier kommt die funktion hin, der die Duplikate aus dem fEld und bank löscht!
                        this.bank.slots = this.bank.slots.map(x => {
                            if (
                                x && 
                                x.name === check_tripled.name &&
                                x.star_level === check_tripled.star_level &&
                                JSON.stringify(x.traits) === JSON.stringify(check_tripled.traits)
                            ) {
                                return null;
                            }
                            else {
                                return x;
                            }
                        });
                        this.field.slots = this.field.slots.map(x => {
                            if (
                                x && 
                                x.name === wanna_buy_slot.name &&
                                x.star_level === wanna_buy_slot.star_level &&
                                JSON.stringify(x.traits) === JSON.stringify(wanna_buy_slot.traits)
                            ) {
                                return null;
                            }
                            else {
                                return x;
                            }
                        });

                        console.log(`${check_tripled.name} to 3 star!`);
                        check_tripled = check_tripled.upgrade_level();
                        this.bank.add_champ_to_bank(check_tripled);
                        console.log(this.game.three_stared_list);
                        this.game.three_stared_list.push(check_tripled);

                    }
                    return wanna_buy_slot;
                }
                else {
                    this.bank.add_champ_to_bank(wanna_buy_slot);
                    this.game.gold = this.game.gold - wanna_buy_slot.cost;
                    this.slots[slot] = null;
                }
            }
        }
    }
}


