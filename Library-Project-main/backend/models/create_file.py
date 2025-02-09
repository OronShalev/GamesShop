import pandas as pd
import random

# Sample game names
game_names = [
    "Chess", "Monopoly", "Scrabble", "Risk", "Catan", "Carcassonne", "Clue", "Ticket to Ride",
    "Pandemic", "Dixit", "Codenames", "7 Wonders", "Azul", "Splendor", "Dominion", "Gloomhaven",
    "Terraforming Mars", "Eldritch Horror", "Betrayal at House on the Hill", "Small World",
    "Twilight Struggle", "Agricola", "Puerto Rico", "Power Grid", "Stone Age", "Great Western Trail",
    "Wingspan", "Brass: Birmingham", "Scythe", "Tzolk'in", "Patchwork", "King of Tokyo",
    "The Resistance", "Love Letter", "Hanabi", "Arkham Horror", "Magic: The Gathering", "Blood Rage",
    "Dune: Imperium", "Star Wars Rebellion", "Terraforming Mars: Ares Expedition", "Lost Ruins of Arnak",
    "Raiders of the North Sea", "The Crew", "Parks", "Root", "Spirit Island", "Hive", "Calico", "Onitama"
]

# Ensure we don't request more than available
num_games = min(50, len(game_names))

# Generate random games data
games_data = [
    {"name": name, "price": round(random.uniform(10, 100), 2), "quantity": random.randint(1, 20)}
    for name in random.sample(game_names, num_games)
]

# Create DataFrame
df = pd.DataFrame(games_data)

# Save to Excel
with pd.ExcelWriter("games.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, index=False)

print("games.xlsx file created successfully!")