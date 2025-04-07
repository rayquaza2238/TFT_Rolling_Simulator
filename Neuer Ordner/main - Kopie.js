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

    // Beispielhafter Inhalt für das Spielfeld hinzufügen
    gameUI.innerHTML = `
        <h2>Spielfeld</h2>
        <p>Level: ${level}</p>
        <p>Gold: ${gold}</p>
        <button id="rerollButton">Reroll Shop</button>
        <div id="shopSlots"></div>
    `;


    console.log("Game started!");
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

// Event-Listener für den Reroll Button
document.getElementById("rerollButton").addEventListener('click', function() {
    shop.reroll_shop();
    updateSlotDisplay();
});

// Event-Listener für den Buy Slot Button
document.getElementById("buyButton").addEventListener('click', function() {
    const slotNumber = document.getElementById("slotNumber").value;
    if (slotNumber) {
        shop.buy_slots(slotNumber);
        updateSlotDisplay();
    } else {
        console.log("Bitte eine gültige Slot-Nummer eingeben.");
    }
});

// Event-Listener for sell Slot Button
document.getElementById("sellButton").addEventListener('click', function() {
    const slotNumber = document.getElementById("slotNumber_sell").value;
    if (slotNumber) {
        bank.sell_champion(slotNumber);
        updateSlotDisplay();
    } else {
        console.log("Bitte eine gültige Slot-Nummer eingeben.");
    }
});

// Event-Listener for to field slot button
document.getElementById("to_field_button").addEventListener('click', function() {
    const slotNumber = document.getElementById("slotNumber_to_field").value;
    const bank_to_field_slotNumber = document.getElementById("slotNumber_bank_to_field").value;
    if (slotNumber && bank_to_field_slotNumber) {
        console.log(slotNumber, bank_to_field_slotNumber);
        bank.put_champ_on_field(slotNumber, bank_to_field_slotNumber);
        updateSlotDisplay();
    } else {
        console.log("Please put in valid Slot Numbers!")
    }
});

// Event-Listener for field to bank slot button
document.getElementById("field_to_bank_button").addEventListener('click', function() {
    const field_to_bank_slotfield = document.getElementById("slotfield_field_to_bank").value;
    const field_to_bank_slotbank = document.getElementById("slotbank_field_to_bank").value;
    console.log(field_to_bank_slotfield, field_to_bank_slotbank);
    if (field_to_bank_slotfield && field_to_bank_slotbank) {
        field.put_champ_on_bank(field_to_bank_slotfield, field_to_bank_slotbank);
        updateSlotDisplay();
    } else {
        console.log("Please put in valid Slot Numbers!")
    }
});

// Event-Listener for field sell
document.getElementById("field_sellButton").addEventListener('click', function() {
    const field_sell_slot = document.getElementById("field_sell").value;
    if (field_sell_slot) {
        field.sell(field_sell_slot);
        updateSlotDisplay();
    } else {
        console.log("Please put in valid Slot Numbers!")
    }
});