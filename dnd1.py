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
