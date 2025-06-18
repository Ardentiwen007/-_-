import random
import json
import os

# === ПАРАМЕТРЫ ИГРЫ ===
CLASSES = {
    "воин": {"hp": 14, "armor": 16, "attack_bonus": 5},
    "маг": {"hp": 8, "armor": 12, "attack_bonus": 7},
    "лучник": {"hp": 10, "armor": 14, "attack_bonus": 6}
}

ITEMS = {
    "зелье здоровья": {"type": "consumable", "heal": 5},
    "меч": {"type": "melee", "attack_bonus": 2},
    "щит": {"type": "melee", "armor": 2},
    "кольчуга": {"type": "melee", "armor": 3},
    "лук": {"type": "ranged", "attack_bonus": 3},
    "магический посох": {"type": "magic", "attack_bonus": 4}
}

BOSS_LOOT = ["магический посох", "кольчуга", "зелье здоровья", "лук"]

CLASS_ALLOWED_ITEMS = {
    "воин": ["melee", "consumable"],
    "лучник": ["ranged", "consumable"],
    "маг": ["magic", "consumable"]
}

ITEM_PRICES = {
    "зелье здоровья": 10,
    "меч": 20,
    "щит": 15,
    "кольчуга": 25,
    "лук": 20,
    "магический посох": 30
}

NPCS = [
    {"name": "Старый странник", "quest": "убейте 1 врага", "reward_exp": 20, "reward_gold": 10},
    {"name": "Бродячий торговец", "quest": "найдите зелье здоровья", "reward_exp": 15, "reward_item": "зелье здоровья"},
    {"name": "Мистический дух", "quest": "не используйте предметы 1 бой", "reward_exp": 25, "reward_item": "магический посох"},
    {"name": "Тайный шпион", "quest": "пройдите уровень без боя", "reward_gold": 30}
]

ENEMIES = [
    {"name": "Гоблин", "hp": 8, "armor": 13, "attack_bonus": 4, "exp": 10, "gold": 5},
    {"name": "Скелет", "hp": 10, "armor": 14, "attack_bonus": 5, "exp": 15, "gold": 7},
    {"name": "Тролль", "hp": 16, "armor": 15, "attack_bonus": 6, "exp": 25, "gold": 10},
    {"name": "Большой паук", "hp": 12, "armor": 12, "attack_bonus": 5, "exp": 20, "gold": 8},
    {"name": "Зомби", "hp": 14, "armor": 13, "attack_bonus": 5, "exp": 18, "gold": 9},
    {"name": "Огр", "hp": 22, "armor": 16, "attack_bonus": 7, "exp": 35, "gold": 20},

    
    {"name": "Капитан Гоблинов", "hp": 30, "armor": 17, "attack_bonus": 8, "exp": 100, "gold": 50, "is_boss": True},
    {"name": "Лич", "hp": 40, "armor": 18, "attack_bonus": 9, "exp": 150, "gold": 100, "is_boss": True},
    {"name": "Дракон", "hp": 60, "armor": 20, "attack_bonus": 12, "exp": 300, "gold": 200, "is_boss": True}
]

DUNGEON_LEVELS = [
    [ENEMIES[0]],                         # Уровень 1
    [ENEMIES[0], ENEMIES[1]],             # Уровень 2
    [ENEMIES[1], ENEMIES[2]],             # Уровень 3
    [ENEMIES[2], ENEMIES[3]],             # Уровень 4
    [ENEMIES[5]],                         # Уровень 5 
    [ENEMIES[3], ENEMIES[4], ENEMIES[5]], # Уровень 6
    [ENEMIES[4], ENEMIES[5]],             # Уровень 7
    [ENEMIES[6]],                         # Уровень 8 
    [ENEMIES[6], ENEMIES[0], ENEMIES[1]], # Уровень 9
    [ENEMIES[7]]                          # Уровень 10 
]

SAVE_FILE = "save.json"
MAX_LEVEL = 10
# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===
def roll_d20():
    return random.randint(1, 20)


def save_game(player):
    with open(SAVE_FILE, "w") as f:
        json.dump(player, f)
    print("Игра успешно сохранена!\n")


def load_game():
    if not os.path.exists(SAVE_FILE):
        print("Сохранённый файл не найден.\n")
        return None
    with open(SAVE_FILE, "r") as f:
        player = json.load(f)
    print("Игра загружена!")
    print(f"Класс: {player['class'].capitalize()}, HP: {player['current_hp']}/{player['max_hp']}, Уровень: {player['level']}\n")
    return player
# === СОЗДАНИЕ ПЕРСОНАЖА ===
def create_character():
    print("Выберите класс:")
    for cls in CLASSES:
        print(f"- {cls.capitalize()}")
    while True:
        choice = input("Ваш выбор: ").lower()
        if choice in CLASSES:
            stats = CLASSES[choice]
            player = {
                "class": choice,
                "max_hp": stats["hp"],
                "current_hp": stats["hp"],
                "armor": stats["armor"],
                "attack_bonus": stats["attack_bonus"],
                "gold": 0,
                "level": 1,
                "experience": 0,
                "inventory": []
            }
            print(f"\nВы выбрали {choice.capitalize()}!")
            print(f"HP: {player['current_hp']}, Броня: {player['armor']}, Атака: +{player['attack_bonus']}\n")
            return player
        else:
            print("Неверный класс. Попробуйте снова.")

# === БОЙ С ВРАГОМ ===
def combat(player, enemy):
    print(f"\nВы встретили {enemy['name']}!")
    if enemy.get("is_boss", False):
        print(f"⚠️ Это босс уровня {player['level']}! Приготовьтесь к тяжёлому бою.")

    while player["current_hp"] > 0 and enemy["hp"] > 0:
        # Показываем текущий статус
        print("\n--- БОЙ ---")
        print(f"{enemy['name']} — {enemy['hp']} HP | Вы — {player['current_hp']} HP")
        print("Что вы делаете?")
        print("1. Атаковать")
        print("2. Использовать предмет")
        print("3. Убежать")

        choice = input("Ваш выбор: ")

        if choice == "1":
            attack_roll = roll_d20() + player["attack_bonus"]
            print(f"\nВы бросаете кубик атаки: {attack_roll - player['attack_bonus']} + {player['attack_bonus']} = {attack_roll}")
            if attack_roll >= enemy["armor"]:
                dmg = random.randint(1, 6) + 1
                print(f"🎯 Вы попали! Нанесено {dmg} урона.")
                enemy["hp"] -= dmg
            else:
                print("❌ Промах!")

        elif choice == "2":
            use_item(player)
            continue

        elif choice == "3":
            print("Вы пытаетесь убежать...")
            if random.random() < 0.5:
                print("🎉 Вам удалось сбежать!")
                return False
            else:
                print("🛑 Не получилось убежать. Враг блокировал путь.")
                pass
        else:
            print("Неверный выбор. Попробуйте снова.")
            continue

        if enemy["hp"] <= 0:
            print(f"\n💀 {enemy['name']} повержен!")
            gain_exp(player, enemy["exp"])
            loot_gold(player, enemy)
            if enemy.get("is_boss"):
                print("🎉 Вы получили особую награду за победу над боссом!")
                special_boss_loot(player, enemy)
            return True

        # Ход врага
        attack_roll_enemy = roll_d20() + enemy["attack_bonus"]
        print(f"\n{enemy['name']} бросает атаку: {attack_roll_enemy - enemy['attack_bonus']} + {enemy['attack_bonus']} = {attack_roll_enemy}")
        if attack_roll_enemy >= player["armor"]:
            dmg = random.randint(1, 6)
            print(f"💥 {enemy['name']} ударил вас! Получено {dmg} урона.")
            player["current_hp"] -= dmg
        else:
            print(f"{enemy['name']} промахнулся!")

        if player["current_hp"] <= 0:
            print("☠️ Вы погибли... Игра окончена.")
            exit()

    return False
    
# === СИСТЕМА ОПЫТА И УРОВНЕЙ ===
def gain_exp(player, amount):
    player["experience"] += amount
    print(f"Вы получили {amount} опыта.")
    level_up(player)


def level_up(player):
    exp_needed = player["level"] * 20
    while player["experience"] >= exp_needed:
        player["experience"] -= exp_needed
        player["level"] += 1
        player["max_hp"] += 2
        player["current_hp"] = player["max_hp"]
        player["attack_bonus"] += 1
        print(f"Вы достигли уровня {player['level']}!")
        print(f"HP увеличен до {player['max_hp']}, Атака: +{player['attack_bonus']}\n")
        if player["level"] >= MAX_LEVEL:
            print("Вы достигли максимального уровня! Подземелье побеждено!")
            input("Нажмите Enter для выхода...")
            exit()
        exp_needed = player["level"] * 20 

# === СУНДУКИ И ИНВЕНТАРЬ ===
def open_chest(player):
    allowed_types = CLASS_ALLOWED_ITEMS[player["class"]]
    possible_items = [name for name, data in ITEMS.items() if data["type"] in allowed_types]
    
    if not possible_items:
        print("Вы ничего не нашли — сундук пуст.")
        return

    item = random.choice(possible_items)
    print(f"Вы нашли: {item}!")
    if input("Взять? (да/нет): ").lower() == "да":
        player["inventory"].append(item)
        print(f"{item} добавлен в инвентарь.")


def use_item(player):
    if not player["inventory"]:
        print("Инвентарь пуст.")
        return

    allowed_types = CLASS_ALLOWED_ITEMS[player["class"]]
    print("Инвентарь:")
    valid_indices = []
    for i, item_name in enumerate(player["inventory"]):
        item_type = ITEMS[item_name]["type"]
        if item_type in allowed_types:
            print(f"{i+1}. {item_name} ({item_type})")
            valid_indices.append(i)
        else:
            print(f"{i+1}. {item_name} (заблокировано для вашего класса)")

    try:
        choice = int(input("Выберите номер предмета: ")) - 1
        if choice not in valid_indices:
            print("Вы не можете использовать этот предмет.")
            return

        item_name = player["inventory"][choice]
        item = ITEMS[item_name]

        if "heal" in item:
            healed = min(item["heal"], player["max_hp"] - player["current_hp"])
            player["current_hp"] += healed
            print(f"Вы восстановили {healed} HP.")

        if "attack_bonus" in item:
            player["attack_bonus"] += item["attack_bonus"]
            print(f"Атака увеличена на {item['attack_bonus']}.")

        if "armor" in item:
            player["armor"] += item["armor"]
            print(f"Броня увеличена на {item['armor']}.")

        print("Предмет использован.")
        player["inventory"].pop(choice)

    except (IndexError, ValueError):
        print("Неверный выбор.")

def loot_gold(player, enemy):
    gold = enemy.get("gold", 0)
    if gold > 0:
        print(f"{enemy['name']} оставил {gold} золотых.")
        player["gold"] += gold

def show_status(player):
    print(f"\n--- Статус персонажа ---")
    print(f"Класс: {player['class'].capitalize()}")
    print(f"HP: {player['current_hp']}/{player['max_hp']}")
    print(f"Броня: {player['armor']}")
    print(f"Атака: +{player['attack_bonus']}")
    print(f"Золото: {player['gold']} монет")
    print(f"Уровень: {player['level']} | Опыт: {player['experience']}")
    print("------------------------\n")

# === ЗАПУСК ИГРЫ ===
def main():
    print("=== Добро пожаловать в Подземелье ===\n")
    print("1. Начать новую игру")
    print("2. Загрузить игру")
    print("3. Выйти")
    choice = input("Ваш выбор: ")

    if choice == "1":
        player = create_character()
    elif choice == "2":
        player = load_game()
        if not player:
            player = create_character()
    elif choice == "3":
        print("Выход из игры.")
        return
    else:
        print("Неверный выбор.")
        return

    dungeon_adventure(player)


if __name__ == "__main__":
    main()
