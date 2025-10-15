import random
from collections import Counter


def get_word_list():
    # список разрешённых слов (все в нижнем регистре, длина 5)
    return [
        'лотос', 'весна', 'комод', 'пирог', 'ручка',
        'книга', 'домик', 'дрова', 'берег', 'банан',
        'актер', 'авеню', 'варяг', 'жилье', 'заряд',
        'изъян', 'ладья', 'шляпа', 'тезка', 'упрек'
    ]


def choose_random(word_list):
    #cлучайно выбирает загаданное слово из списка
    return random.choice(word_list)


def get_user_guess(attempt):
    """Запрашивает у пользователя догадку — 5-буквенное слово.

    Валидирует ввод: длина 5, все символы — буквы.
    Возвращает ввод в нижнем регистре.
    """
    while True:
        guess = input(f"Попытка {attempt}: ").strip().lower()
        if len(guess) != 5:
            print("Ошибка: введите слово ровно из 5 букв.")
            continue
        if not guess.isalpha():
            print("Ошибка: слово должно содержать только буквы.")
            continue
        return guess


def get_feedback(secret, guess):
    """Возвращает строку с подсказкой в формате:
    [x] — буква угадана и стоит на той же позиции;
    (x) — буква есть в слове, но на другой позиции;
    x   — буквы нет в слове.

    Корректно обрабатывает повторяющиеся буквы.
    """
    # Результат по позициям (None — ещё не определено)
    result = [None] * 5

    # Считаем сколько каждой буквы есть в секрете
    secret_counts = Counter(secret)

    # 1) помечаем точные совпадения и уменьшаем счетчики
    for i, (s, g) in enumerate(zip(secret, guess)):
        if g == s:
            result[i] = f"[{g}]"
            secret_counts[g] -= 1

    # 2)  для остальных позиций проверяем, есть ли буква в секрете (с учётом оставшихся счетчиков)
    for i, g in enumerate(guess):
        if result[i] is not None:
            continue  # уже помечено как точное совпадение
        if secret_counts.get(g, 0) > 0:
            result[i] = f"({g})"
            secret_counts[g] -= 1
        else:
            result[i] = g

    # Соединяем с пробелами для читаемости
    return " ".join(result)


def play_round(word_list):
    secret = choose_random(word_list)
    print("Загадано слово из 5 букв. У вас 6 попыток.")

    for attempt in range(1, 7):
        guess = get_user_guess(attempt)
        feedback = get_feedback(secret, guess)
        print("Результат:", feedback)

        if guess == secret:
            print(f'Вы угадали слово "{secret}" за {attempt} попыток!')
            return

    # Если дошли сюда — попытки закончились
    print(f"К сожалению, вы не угадали. Загаданное слово: {secret}")


def main():
    word_list = get_word_list()

    while True:
        play_round(word_list)
        again = input("Хотите сыграть ещё? (да/нет): ").strip().lower()
        if again not in ("да", "yes", "y", "д"):
            break


if __name__ == "__main__":
    main()
