import random

# Словарь правил: ключ бьет значения
RULES = {
    "ножницы": ["бумага", "ящерица"],
    "бумага": ["камень", "спок"],
    "камень": ["ножницы", "ящерица"],
    "ящерица": ["спок", "бумага"],
    "спок": ["ножницы", "камень"]
}

# Описания победных фраз
DESCRIPTIONS = {
    ("ножницы", "бумага"): "Ножницы режут бумагу.",
    ("бумага", "камень"): "Бумага накрывает камень.",
    ("камень", "ящерица"): "Камень давит ящерицу.",
    ("ящерица", "спок"): "Ящерица травит Спока.",
    ("спок", "ножницы"): "Спок ломает ножницы.",
    ("ножницы", "ящерица"): "Ножницы убивают ящерицу.",
    ("ящерица", "бумага"): "Ящерица ест бумагу.",
    ("бумага", "спок"): "Бумага подставляет Спока.",
    ("спок", "камень"): "Спок испаряет камень.",
    ("камень", "ножницы"): "Камень затупляет ножницы."
}

OPTIONS = list(RULES.keys())


def get_target_score():
    #зпрос у пользователя до скольки побед игра
    while True:
        user_input = input("До скольки побед играем? ").strip()
        if user_input.isdigit() and int(user_input) > 0:
            return int(user_input)
        print("Ошибка: введите положительное целое число.")


def get_user_choice():
    #запросить ход у пользователя (камень/ножницы/бумага/ящерица/спок)
    while True:
        choice = input("Ваш ход (камень/ножницы/бумага/ящерица/спок): ").strip().lower()
        if choice in OPTIONS:
            return choice
        print("Ошибка: некорректный выбор.")


def get_computer_choice():
    #cлучайный выбор компьютера
    return random.choice(OPTIONS)


def determine_winner(user, computer):
    #определяет результат раунда: user, computer или draw
    if user == computer:
        return "draw", None
    if computer in RULES[user]:
        return "user", DESCRIPTIONS[(user, computer)]
    else:
        return "computer", DESCRIPTIONS[(computer, user)]


def play_game():
    target_score = get_target_score()
    user_score = 0
    comp_score = 0

    while user_score < target_score and comp_score < target_score:
        user_choice = get_user_choice()
        comp_choice = get_computer_choice()

        winner, description = determine_winner(user_choice, comp_choice)

        print(f"Ход компьютера: {comp_choice}")
        if winner == "draw":
            print("Ничья!")
        elif winner == "user":
            print(f"{description} Вы победили!")
            user_score += 1
        else:
            print(f"{description} Компьютер победил!")
            comp_score += 1

        print(f"Счет: Вы - {user_score}, Компьютер - {comp_score}\n")

    # Итог игры
    if user_score > comp_score:
        print("Поздравляем! Вы выиграли матч!")
    else:
        print("К сожалению, вы проиграли")


if __name__ == "__main__":
    play_game()
