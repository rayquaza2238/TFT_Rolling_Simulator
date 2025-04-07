class Champion{
    constructor(name, cost, traits, tier, star_level = 1, max_star_level = 3) {
        this.name = name;
        this.cost = cost;
        this.traits = traits;
        this.tier = tier;
        this.star_level = star_level;
        this.max_star_level = max_star_level;
        this.tier_colors = {
            1: "white",
            2: "green",
            3: "blue",
            4: "purple",
            5: "gold",
        }
    }

    check_duplicated_name(unit) {
        console.log('Name gleich:' + this.name == unit.name);
        return this.name == unit.name;
    }

    check_duplicated_traits(unit) {
        console.log('traits gleich:' + this.traits == unit.traits);
        return this.traits == unit.traits;
    }

    check_duplicated_cost(unit) {
        console.log('cost gleich:' + this.cost == unit.cost);
        return this.cost == unit.cost;
    }

    check_duplicates(liste) {
        let count = 0;
        for (let champ of liste) {
            if (champ != null) {
                if (
                    this.name == champ.name && 
                    JSON.stringify(this.traits) === JSON.stringify(champ.traits) &&
                    this.cost == champ.cost
                ) {
                    count ++;
                }
            }
        }
        return count >=2;
    }

    upgrade_level(){
        if (this.star_level < this.max_star_level) {
            let new_star_level = this.star_level + 1;
            let new_cost = (this.tier > 1) ? (3 * this.cost - 1) : (3 * this.cost);
            let upgraded_unit = new Champion(this.name, 
                new_cost, 
                this.traits, 
                this.tier, 
                new_star_level);
            return upgraded_unit;
        }
        else {
            console.log("Max Star was reached!");
            return null;
        }

    }
}

