class Bank {
    constructor(game, field, slots = []) {
        this.game = game;
        this.field = field;
        this.slots = slots.length ? slots : Array(9).fill(null);
    }

    add_champ_to_bank(champ) {
        if (this.slots.includes(null)) {
            let index_of_first_null = this.slots.indexOf(null);
            this.slots[index_of_first_null] = champ;
            console.log('${champ.name} was bought!');
        }
        else {
            console.log('Bank is full!');
        }
    }

    sell_champion(slot) {
        let wanna_sell_champion = this.slots[slot];
        if (wanna_sell_champion == null) {
            console.log('No Unit here!');
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

    put_champ_on_field(slot_on_field, slot_bank) {
        let champ = this.slots[slot_bank];
        if (champ == null) {
            console.log("No unit here to be placed!");
        }
        else {
            let current_field_slot = this.field.slots[slot_on_field];
            this.field.slots[slot_on_field] = champ;
            console.log(`${champ.name} was put on the field: `, this.field.slots);
            this.slots[slot_bank] = current_field_slot;
        }
        
    }
}

