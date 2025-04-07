class Game {
    constructor(gold, level, stage, champion_pool, three_stared_list) {
        this.gold = gold;
        this.level = level;
        this.stage = stage;
        this.champion_pool = champion_pool;
        this.removal_rules = {
            1: { 1: 8 },
            2: { 1: 20, 2: 4 },
            3: { 1: 24, 2: 8, 3: 4 },
            4: { 1: 32, 2: 16, 3: 6 },
            5: { 1: 64, 2: 30, 3: 12, 4: 2 },
            6: { 1: 8 * 3 * 3, 2: 8 * 3 * 2, 3: 8 * 3 * 1, 4: 6 },
            7: { 1: 8 * 3 * 4, 2: 8 * 3 * 3, 3: 8 * 3 * 1, 4: 12, 5: 1 },
            8: { 1: 8 * 3 * 3, 2: 8 * 3 * 3, 3: 8 * 3 * 2, 4: 8 * 3, 5: 4 },
            9: { 1: 8 * 3 * 3, 2: 8 * 3 * 3, 3: 8 * 3 * 3, 4: 8 * 3 * 2, 5: 8 },
            10: { 1: 8 * 3 * 3, 2: 8 * 3 * 3, 3: 8 * 3 * 4, 4: 8 * 3 * 4, 5: 4 * 3 }
        };
        this.three_stared_list = three_stared_list;
        this.odds_data = {
            1: ["100%", "75%", "55%", "45%", "30%", "19%", "18%", "15%", "5%", "1%"],
            2: ["0%", "25%", "30%", "33%", "40%", "30%", "25%", "20%", "10%", "2%"],
            3: ["0%", "0%", "15%", "20%", "25%", "40%", "32%", "25%", "20%", "12%"],
            4: ["0%", "0%", "0%", "2%", "5%", "10%", "22%", "30%", "40%", "50%"],
            5: ["0%", "0%", "0%", "0%", "0%", "1%", "3%", "10%", "25%", "35%"]
        };
        this.odds = this.getOdds();
    }
    getOdds() {
        let odds = {};

        for (let level in this.odds_data) {
            odds[level] = this.odds_data[level].map(percentage => {
                if (percentage == "0%") {
                    return 0;
                } else {
                    return parseFloat(percentage.replace("%", "")) / 100;
                }
            });
        }

        odds[6] = Array(10).fill(0.00);

        let transposedOdds = this.transposeOdds(odds);
        return transposedOdds[this.level];
    }

    transposeOdds(odds) {
        let transposed = [];
        let numRows = Object.keys(odds).length;
        let numCols = odds[1].length;

        // Transponieren der Matrix
        for (let col = 0; col < numCols; col++) {
            let row = [];
            for (let level in odds) {
                row.push(odds[level][col]);
            }
            transposed.push(row);
        }

        return transposed;
    }

    check_if_in_three_stared_list(champion) {

    
        // Prüft, ob die Liste leer ist
        if (!this.three_stared_list || this.three_stared_list.length === 0) {
            console.log('leere liste');
            return false;
        }
    
        // Überprüft, ob ein Champion mit dem gleichen Namen, Traits und Tier existiert
        return this.three_stared_list.some(champ => 
            champion.name === champ.name &&
            JSON.stringify(champion.traits) === JSON.stringify(champ.traits)
        );
    }
    

    
}
