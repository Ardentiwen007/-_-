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
    [ENEMIES[0]],                         # Уровень 1 — Гоблин
    [ENEMIES[0], ENEMIES[1]],            # Уровень 2 — Гоблин, Скелет
    [ENEMIES[1], ENEMIES[2]],            # Уровень 3 — Скелет, Тролль
    [ENEMIES[2], ENEMIES[3]],            # Уровень 4 — Тролль, Паук
    [ENEMIES[6]],                        # Уровень 5 — Капитан Гоблинов (босс)
    [ENEMIES[3], ENEMIES[4], ENEMIES[5]],# Уровень 6 — Паук, Зомби, Огр
    [ENEMIES[4], ENEMIES[5]],           # Уровень 7 — Зомби, Огр
    [ENEMIES[5], ENEMIES[7]],           # Уровень 8 — Огр, Лич
    [ENEMIES[7]],                        # Уровень 9 — Лич
    [ENEMIES[8]]                         # Уровень 10 — Дракон (финальный босс)
]

SAVE_FILE = "save.json"
MAX_LEVEL = 10

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
