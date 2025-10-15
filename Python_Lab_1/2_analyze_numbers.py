# Задание 2: Анализатор чисел

def get_positive_integer():
    #запрос у пользователя целое число N > 0
    while True:
        user_input = input("Введите целое число больше 0: ").strip()
        if user_input.isdigit():
            n = int(user_input)
            if n > 0:
                return n
        print("Ошибка: нужно ввести положительное целое число.")


def find_divisors(n):
    # все делители числа n
    divisors = []
    for i in range(1, n + 1):
        if n % i == 0:
            divisors.append(i)
    return divisors


def is_prime(n):
    # является ли число n простым
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def is_perfect(n, divisors):
    # является ли число n совершенным
    return sum(divisors[:-1]) == n


def main():
    n = get_positive_integer()
    divisors = find_divisors(n)

    print(f"Делители числа {n}: {divisors}")

    if is_prime(n):
        print(f"Число {n} является простым")
    else:
        print(f"Число {n} не является простым")

    if is_perfect(n, divisors):
        # красивое отображение суммы делителей
        expression = "+".join(str(d) for d in divisors[:-1])
        print(f"Число {n} является совершенным ({expression}={n})")
    else:
        print(f"Число {n} не является совершенным")


if __name__ == "__main__":
    main()
