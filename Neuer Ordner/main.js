let game;
let shop;
let bank;
let field;


function start_game() {
    const gold = parseInt(document.getElementById("goldSlider").value);
    document.getElementById("goldValue").textContent = gold;
    const level = parseInt(document.getElementById("levelSlider").value);
    document.getElementById("levelValue").textContent = level;
    const stage = 3;
    const champion_pool = [
        new Champion("Garen", 1, ["Warden", "Demacia"], 1),
        new Champion("Ashe", 2, ["Freljord", "Ranger"], 2),
        new Champion("Katarina", 3, ["Noxus", "Assassin"], 3),
        new Champion("Morgana", 4, ["Shadow Isles", "Sorcerer"], 4),
        new Champion("Aatrox", 5, ["Darkin", "Slayer"], 5),
        new Champion("Yasuo", 3, ["Ionia", "Duelist"], 3),
        new Champion("Jinx", 2, ["Zaun", "Gunner"], 2),
        new Champion("Teemo", 1, ["Yordle", "Trickster"], 1),
        new Champion("Darius", 2, ["Noxus", "Juggernaut"], 2),
        new Champion("Garen", 1, ["Warden", "Demacia"], 1),
        new Champion("Ashe", 2, ["Freljord", "Ranger"], 2),
        new Champion("Katarina", 3, ["Noxus", "Assassin"], 3),
        new Champion("Morgana", 4, ["Shadow Isles", "Sorcerer"], 4),
        new Champion("Aatrox", 5, ["Darkin", "Slayer"], 5),
        new Champion("Yasuo", 3, ["Ionia", "Duelist"], 3),
        new Champion("Jinx", 2, ["Zaun", "Gunner"], 2),
        new Champion("Teemo", 1, ["Yordle", "Trickster"], 1),
        new Champion("Darius", 2, ["Noxus", "Juggernaut"], 2),
        new Champion("Garen", 1, ["Warden", "Demacia"], 1),
        new Champion("Ashe", 2, ["Freljord", "Ranger"], 2),
        new Champion("Katarina", 3, ["Noxus", "Assassin"], 3),
        new Champion("Morgana", 4, ["Shadow Isles", "Sorcerer"], 4),
        new Champion("Aatrox", 5, ["Darkin", "Slayer"], 5),
        new Champion("Yasuo", 3, ["Ionia", "Duelist"], 3),
        new Champion("Jinx", 2, ["Zaun", "Gunner"], 2),
        new Champion("Teemo", 1, ["Yordle", "Trickster"], 1),
        new Champion("Darius", 2, ["Noxus", "Juggernaut"], 2),
        new Champion("Garen", 1, ["Warden", "Demacia"], 1),
        new Champion("Ashe", 2, ["Freljord", "Ranger"], 2),
        new Champion("Katarina", 3, ["Noxus", "Assassin"], 3),
        new Champion("Morgana", 4, ["Shadow Isles", "Sorcerer"], 4),
        new Champion("Aatrox", 5, ["Darkin", "Slayer"], 5),
        new Champion("Yasuo", 3, ["Ionia", "Duelist"], 3),
        new Champion("Jinx", 2, ["Zaun", "Gunner"], 2),
        new Champion("Teemo", 1, ["Yordle", "Trickster"], 1),
        new Champion("Teemo", 1, ["Yordle", "Trickster"], 1),
        new Champion("Teemo", 1, ["Yordle", "Trickster"], 1),
        new Champion("Teemo", 1, ["Yordle", "Trickster"], 1),
        new Champion("Teemo", 1, ["Yordle", "Trickster"], 1),
        new Champion("Teemo", 1, ["Yordle", "Trickster"], 1),
        new Champion("Darius", 2, ["Noxus", "Juggernaut"], 2),
        new Champion("Garen", 1, ["Warden", "Demacia"], 1),
        new Champion("Ashe", 2, ["Freljord", "Ranger"], 2),
        new Champion("Katarina", 3, ["Noxus", "Assassin"], 3),
        new Champion("Morgana", 4, ["Shadow Isles", "Sorcerer"], 4),
        new Champion("Aatrox", 5, ["Darkin", "Slayer"], 5),
        new Champion("Yasuo", 3, ["Ionia", "Duelist"], 3),
        new Champion("Jinx", 2, ["Zaun", "Gunner"], 2),
        new Champion("Teemo", 1, ["Yordle", "Trickster"], 1),
        new Champion("Darius", 2, ["Noxus", "Juggernaut"], 2),
        new Champion("Garen", 1, ["Warden", "Demacia"], 1),
        new Champion("Ashe", 2, ["Freljord", "Ranger"], 2),
        new Champion("Katarina", 3, ["Noxus", "Assassin"], 3),
        new Champion("Morgana", 4, ["Shadow Isles", "Sorcerer"], 4),
        new Champion("Aatrox", 5, ["Darkin", "Slayer"], 5),
        new Champion("Yasuo", 3, ["Ionia", "Duelist"], 3),
        new Champion("Jinx", 2, ["Zaun", "Gunner"], 2),
        new Champion("Teemo", 1, ["Yordle", "Trickster"], 1),
        new Champion("Darius", 2, ["Noxus", "Juggernaut"], 2),
        new Champion("Garen", 1, ["Warden", "Demacia"], 1),
        new Champion("Ashe", 2, ["Freljord", "Ranger"], 2),
        new Champion("Katarina", 3, ["Noxus", "Assassin"], 3),
        new Champion("Morgana", 4, ["Shadow Isles", "Sorcerer"], 4),
        new Champion("Aatrox", 5, ["Darkin", "Slayer"], 5),
        new Champion("Yasuo", 3, ["Ionia", "Duelist"], 3),
        new Champion("Jinx", 2, ["Zaun", "Gunner"], 2),
        new Champion("Teemo", 1, ["Yordle", "Trickster"], 1),
        new Champion("Darius", 2, ["Noxus", "Juggernaut"], 2),
        new Champion("Garen", 1, ["Warden", "Demacia"], 1),
        new Champion("Ashe", 2, ["Freljord", "Ranger"], 2),
        new Champion("Katarina", 3, ["Noxus", "Assassin"], 3),
        new Champion("Morgana", 4, ["Shadow Isles", "Sorcerer"], 4),
        new Champion("Aatrox", 5, ["Darkin", "Slayer"], 5),
        new Champion("Yasuo", 3, ["Ionia", "Duelist"], 3),
        new Champion("Jinx", 2, ["Zaun", "Gunner"], 2),
        new Champion("Teemo", 1, ["Yordle", "Trickster"], 1),
        new Champion("Darius", 2, ["Noxus", "Juggernaut"], 2),
        new Champion("Ahri", 4, ["Ionia", "Invoker"], 4)
    ];
    let three_stared_list = [];
    game = new Game(gold, level, stage, champion_pool, three_stared_list);
    field = new Field(game,);
    bank = new Bank(game, field);
    shop = new Shop(game, bank, field, );
    field.setBank(bank);
    
    document.getElementById("mainMenu").style.display = "none";
    const gameUI = document.getElementById("gameUI");
    gameUI.style.display = "block";



    // Beispiel für den Event-Listener für den Reroll-Button
    document.getElementById("rerollButton").addEventListener('click', function () {
        // Logik für das Rerollen
        shop.reroll_shop();
    });
}

const levelSlider = document.getElementById("levelSlider");
  const levelValue = document.getElementById("levelValue");

  levelSlider.addEventListener("input", () => {
    levelValue.textContent = levelSlider.value;
  });

  const goldSlider = document.getElementById("goldSlider");
  const goldValue = document.getElementById("goldValue");

  goldSlider.addEventListener("input", () => {
    goldValue.textContent = goldSlider.value;
  });

// Checkbox Zugriff
const checkbox = document.getElementById("activateOption");
checkbox.addEventListener("change", () => {
if (checkbox.checked) {
    console.log("Checkbox ist aktiviert");
} else {
    console.log("Checkbox ist deaktiviert");
}


});

function updateSlotDisplay() {
    if (!shop || !bank) return;

    const shopDisplay = document.getElementById("shopSlotsOutput");
    const bankDisplay = document.getElementById("bankSlotsOutput");
    const fieldDisplay = document.getElementById("fieldSlotsOutput");

    const formatChampion = (champ) => {
        if (!champ) return "🕳️ Empty";
        return `${champ.name} ⭐${champ.star_level} 🟡${champ.cost} (${champ.traits.join(", ")})`;
    };

    shopDisplay.textContent = shop.slots.map(formatChampion).join("\n");
    bankDisplay.textContent = bank.slots.map(formatChampion).join("\n");
    fieldDisplay.textContent = field.slots.map(formatChampion).join("\n");
}

document.getElementById("startGameButton").addEventListener('click', start_game);
