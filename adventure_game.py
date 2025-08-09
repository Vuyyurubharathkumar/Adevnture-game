import random
from datetime import date
# This is a game script for an adventure game 
# where the player navigates through a forest, solves riddles, and faces challenges to find a legendary treasure.

def get_name():
    print("Welcome to the first game of the year! You are an adventurer seeking a legendary treasure hidden deep within an ancient forest full of forked paths, tricky riddles, and mysterious guardians.")
    while True:
        player_name = input("Before we begin, please enter your name: ")
        if player_name.isalpha():
            print(f"Hello {player_name}, Welcome to this adventure! Your quest for the legendary treasure begins at the edge of the Whispering Woods.")
            return player_name
        else:
            print("Please enter a valid name using only letters.")

def get_age():
    while True:
        try:
            print("To begin with first lets verify if you are old enough to embark on this adventure.")
            year = int(input("Enter your birth year (e.g., 2005): "))
            month = int(input("Enter your birth month (1-12): "))
            day = int(input("Enter your birth day (1-31): "))
            born = date(year, month, day)
            today = date.today()
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            if age >= 18:
                print("Great! You are old enough to play the game.")
                return age
            else:
                print("Sorry, you must be at least 18 years old to play this game.")
                return None
        except ValueError:
            print("That doesn't look like a valid date. Please try again.")

# Inventory and Health (global for simplicity)
player_inventory = set()
player_health = 10  # Starting health points

# Define scenes as before, but some with new integration hints
scenes = {
    'start': {'text': "You stand at the edge of the Whispering Woods. Two paths: 'left' into thicket or 'right' to clearing.", 'choices': {'left': 'thicket', 'right': 'clearing'}},
    'thicket': {'text': "Branches claw your clothes. Path splits: 'straight' to river or 'down' into hollow log.", 'choices': {'straight': 'river', 'down': 'log'}},
    'clearing': {'text': "A masked fox blocks you. 'solve' its riddle or 'retreat'?", 'choices': {'solve': 'riddle', 'retreat': 'start'}},
    'riddle': {'text': "Fox asks a riddle: 'I speak without a mouth, hear without ears, come alive with wind. What am I?'", 'choices': {'echo': 'stones', 'other': 'start'}},
    'river': {'text': "Rickety bridge over wild river. 'cross' bridge or 'search' for another way?", 'choices': {'cross': 'bridge', 'search': 'stones'}},
    'log': {'text': "Inside hollow log, find lever. 'pull' lever or 'out' crawl back?", 'choices': {'pull': 'trap', 'out': 'thicket'}},
    'trap': {'text': "Trapdoor opens! You fall and get hurt badly.", 'choices': {'restart': 'start'}},
    'bridge': {'text': "Plank snaps halfway on bridge! 'jump' ahead or 'hold' tight?", 'choices': {'jump': 'final', 'hold': 'trap'}},
    'stones': {
        'text': "Found stepping-stones. 'risk' stepping stones, 'back' to river, or 'deeper' to venture further into the forest?",
        'choices': {'risk': 'stone_crossing', 'back': 'river', 'deeper': 'forest_path'}
    },
    'stone_crossing': {'text': "You attempt to risk crossing the slippery stones...", 'choices': {'continue': 'final'}},
    'final': {'text': ("Treasure chest gleams ahead! You have crossed treacherous paths and solved ancient riddles. "
                      "Your bravery and wisdom have earned you the legendary treasure. Your quest ends in triumph — congratulations, adventurer!"), 'choices': {}},

    # Expanded scenes with some requiring inventory or offering items
    'forest_path': {'text': "You venture deeper into the forest. The path is dimly lit by glowing mushrooms. Do you 'follow' the faint light or 'ignore' it and stay on the path?", 'choices': {'follow': 'glowing_mushrooms', 'ignore': 'dark_clearing'}},
    'glowing_mushrooms': {'text': "The glowing mushrooms lead you to a serene pond. A singing mermaid appears and offers a hint: 'Seek the stone that sings under the moon.' Do you 'thank' her and continue or 'ignore' the hint and move on?", 'choices': {'thank': 'moon_stone', 'ignore': 'dark_clearing'}},
    'dark_clearing': {'text': "You find yourself in a dark clearing where an old lantern hangs from a tree. It flickers mysteriously. Do you 'take' the lantern or 'leave' it?", 'choices': {'take': 'lantern_path', 'leave': 'forest_attack'}},
    'lantern_path': {'text': "With the lantern lighting your way, you notice strange symbols etched on trees. One symbol looks like a key. Do you 'touch' the symbol or 'move' on?", 'choices': {'touch': 'secret_gate', 'move': 'forest_attack'}},
    'secret_gate': {'text': "Touching the symbol opens a hidden gate revealing a mysterious garden. The air is filled with the scent of magic. Do you 'explore' the garden or 'rest'?", 'choices': {'explore': 'garden_treasure', 'rest': 'ambush'}},
    'garden_treasure': {'text': "In the garden, you discover an ancient chest with a glowing lock. It whispers: 'Solve my puzzle to claim your prize.' Do you 'solve' the puzzle or 'leave'?", 'choices': {'solve': 'treasure_room', 'leave': 'ambush'}},
    'treasure_room': {'text': ("The chest opens, revealing a trove of treasures and the final clue: 'The greatest treasure lies where the sun meets the sea.' "
                               "Your long and challenging journey has come to a rewarding conclusion!"), 'choices': {}},
    'ambush': {'text': "Suddenly, forest bandits jump out! You must 'fight' or 'flee'.", 'choices': {'fight': 'fight_battle', 'flee': 'start'}},
    'fight_battle': {'text': "You bravely fight off the bandits and survive. A hidden path appears. Do you 'follow' it or 'return' to the forest edge?", 'choices': {'follow': 'final', 'return': 'start'}},
    'moon_stone': {'text': "At night, under moonlight, a stone you found starts singing softly. Do you 'listen' carefully or 'ignore' it?", 'choices': {'listen': 'final', 'ignore': 'ambush'}},
    'forest_attack': {'text': "Without a light, you stumble into a nest of angry forest spiders! Do you 'run' or 'face' them?", 'choices': {'run': 'start', 'face': 'trap'}}
}

def lose_health(amount=1):
    global player_health
    player_health -= amount
    print(f"--- You lost {amount} health point(s). Current health: {player_health} ---")
    if player_health <= 0:
        print("You have lost all your health. Your adventure ends here.")
        exit(0)

def game_setup(current_scene):
    global player_inventory
    scene = scenes[current_scene]
    print("\n" + scene['text'])

    # Special logic for some scenes involving inventory or random events

    if current_scene == 'trap':
        # Player takes damage and falls back to start
        lose_health(3)
        print("You are back at the forest edge.")
        game_setup('start')
        return

    if current_scene == 'stone_crossing':
        # Random chance outcome - 70% success, 30% slip losing health
        chance = random.random()
        if chance <= 0.7:
            print("You carefully cross the slippery stones safely.")
            game_setup('final')
        else:
            print("Oh no! You slipped on the stones and hurt yourself.")
            lose_health(2)
            if player_health > 0:
                # Back to stones to try again or go back
                game_setup('stones')
        return

    if current_scene == 'dark_clearing':
        if 'lantern' in player_inventory:
            print("Your lantern lights up the clearing, safe passage ahead.")
            # Player can move on safely, let's auto move to lantern_path or give choice
            game_setup('lantern_path')
            return

    if current_scene == 'dark_clearing' and 'lantern' not in player_inventory:
        # Normal prompt handled below
        pass

    if current_scene == 'take_lantern':
        # Add lantern item to inventory
        print("You take the lantern and add it to your inventory.")
        player_inventory.add('lantern')
        game_setup('lantern_path')
        return

    if current_scene == 'ambush':
        # Random fighting chance and health loss if fight
        # Handled in input choices
        pass

    if not scene['choices']:
        print("\nThank you for playing your adventure! Farewell.\n")
        exit(0)

    while True:
        choice = input(f"What would you like to do? ({', '.join(scene['choices'].keys())}): ").strip().lower() #this wil 

        # Special cases based on current scene
        if current_scene == 'riddle':
            if choice == 'echo':
                print("Correct! The fox lets you pass.")
                next_scene = scene['choices']['echo']
                game_setup(next_scene)
                break
            else:
                print("Wrong answer! The fox sends you back to the start.")
                next_scene = scene['choices']['other']
                game_setup(next_scene)
                break

        elif current_scene == 'dark_clearing':
            if choice == 'take':
                print("You take the lantern and add it to your inventory.")
                player_inventory.add('lantern')
                next_scene = scene['choices'][choice]
                game_setup(next_scene)
                break
            elif choice == 'leave':
                next_scene = scene['choices'][choice]
                game_setup(next_scene)
                break
            else:
                print("Choose 'take' or 'leave'.")

        elif current_scene == 'ambush':
            if choice == 'fight':
                # Random outcome fight: 60% win (progress), 40% lose some health and retry or flee
                outcome = random.random()
                if outcome <= 0.6:
                    print("You bravely fight off the bandits and survive!")
                    next_scene = scene['choices']['fight']
                    game_setup(next_scene)
                else:
                    print("The bandits hurt you badly!")
                    lose_health(3)
                    if player_health > 0:
                        # Give choice to fight or flee again:
                        print("You can still fight or flee. Make your choice carefully.")
                        # Re-loop or recurse to allow retry
                    else:
                        print("You have fallen. Your adventure ends here.")
                        exit(0)
                break
            elif choice == 'flee':
                next_scene = scene['choices']['flee']
                game_setup(next_scene)
                break
            else:
                print("Please choose 'fight' or 'flee'.")

        elif current_scene == 'stones' and choice == 'risk':
            # Redirect to stone_crossing scene (random event handled above)
            game_setup('stone_crossing')
            break

        elif choice in scene['choices']:
            next_scene = scene['choices'][choice]
            game_setup(next_scene)
            break

        else:
            print("Please choose a valid option:", ", ".join(scene['choices'].keys()))


def main():
    global player_inventory, player_health
    player_inventory = set()  # empty inventory at start
    player_health = 10        # reset health every new game
    player_name = get_name()
    player_age = get_age()
    if player_age and player_age >= 18:
        print(f"\nStarting game with health: {player_health}\n")
        game_setup('start')
    else:
        print("Sorry, you must be at least 18 to play this game. Exiting.")

if __name__ == "__main__":
    main()
