class Field {
    constructor(game, bank = null, slots = []) {
        this.game = game;
        if (bank == null){
            bank = [];
        }
        this.bank = bank;
        this.slots = slots.length ? slots : Array(24).fill(null);
    }

    setBank(bank) {
        this.bank = bank;
    }

    put_champ_on_bank(slot_on_field, slot_bank) {
        let champ = this.slots[slot_on_field];
        //Unit in this slot? 
        if (champ == null) {
            console.log('No Champ here to move!');
        }
        else {
            //
            console.log(this.bank.slots);
            let current_bank_slot = this.bank.slots[slot_bank];
            this.bank.slots[slot_bank] = champ;
            this.slots[slot_on_field] = current_bank_slot; 
        }
    }

    sell(slot) {
        let wanna_sell_champion = this.slots[slot];
        if (wanna_sell_champion == null) {
            console.log('No Champ here!');
        }
        else {
            let num_new_champs = 3 ** (wanna_sell_champion.star_level - 1);
            for (let i = 0; i < num_new_champs; i++) {
                this.game.champion_pool.push(new Champion(wanna_sell_champion.name, wanna_sell_champion.tier, wanna_sell_champion.traits, wanna_sell_champion.tier));
            }
            console.log('Unit was sold to the champion pool!');
            if (wanna_sell_champion.star_level  == 3) {
                this.game.three_stared_list = this.game.three_stared_list.filter(champ => {
                    return !(
                        champ.name == wanna_sell_champion.name &&
                        JSON.stringify(champ.traits) === JSON.stringify(wanna_sell_champion.traits)
                    );
                });
                console.log('${wanna_sell_champion.name} in the pool again!');
            }
            this.game.gold = this.game.gold + wanna_sell_champion.cost;
            this.slots[slot] = null;
        }
    }

}

