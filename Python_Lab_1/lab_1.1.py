# Задание 1: Быки и коровы

import random


def get_number_length():
    #запрос длины числа 
    while True:
        choice = input("Выберите длину загадываемого числа (3, 4 или 5): ").strip()
        if choice.isdigit() and int(choice) in (3, 4, 5):
            return int(choice)
        print("Некорректный ввод. Введите 3, 4 или 5.")


def generate_random(length):
    #генерация случайного числа с уникальными цифрами заданной длины
    digits = list("0123456789")
    random.shuffle(digits)
    # первая цифра не должна быть нулем
    if digits[0] == "0":
        digits[0], digits[1] = digits[1], digits[0]
    return "".join(digits[:length])


def get_user_number(length):
    #запрос числа от пользователя заданной длины
    while True:
        guess = input(f"Введите число из {length} цифр: ").strip()
        if guess.isdigit() and len(guess) == length:
            return guess
        print("Ошибка: введите корректное число.")


def count_cows_and_bulls(secret, guess):
    #подсчет количества коров (точное совпадение) и быков (есть цифра, но в другой позиции)
    cows = sum(s == g for s, g in zip(secret, guess))
    bulls = sum(min(secret.count(d), guess.count(d)) for d in set(guess)) - cows
    return cows, bulls


def play_game():
    #одна игра: возвращает количество попыток
    length = get_number_length()
    secret = generate_random(length)
    attempts = 0

    print(f"Загадано число из {length} цифр.")

    while True:
        attempts += 1
        guess = get_user_number(length)
        cows, bulls = count_cows_and_bulls(secret, guess)

        if cows == length:
            print(f"Вы угадали число {secret} за {attempts} попыток!")
            return attempts
        else:
            print(f"Найдено {cows} коров и {bulls} быков.")


def main():
    stats = []

    while True:
        attempts = play_game()
        stats.append(attempts)

        again = input("Хотите сыграть еще? (да/нет): ").strip().lower()
        if again not in ("да", "yes", "y"):
            break

    if stats:
        print("\nСтатистика:")
        print(f"Всего игр сыграно: {len(stats)}")
        print(f"Лучший результат: {min(stats)} попыток")
        print(f"Худший результат: {max(stats)} попыток")
        print(f"Средний результат: {sum(stats) / len(stats):.1f} попыток")


if __name__ == "__main__":
    main()
