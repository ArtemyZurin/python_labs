import string
from collections import Counter


def get_text():
    #Запросить текст не менее 100 символов
    while True:
        text = input("Введите текст для анализа (не менее 100 символов):\n")
        if len(text) >= 100:
            return text
        print("Ошибка: текст слишком короткий, попробуйте снова.\n")


def preprocess_text(text):
    #привести к нижнему регистру и убрать знаки препинания
    text = text.lower()
    # удалить пунктуацию
    translator = str.maketrans('', '', string.punctuation + "—…“”«»")
    return text.translate(translator)


def analyze_text(text):
    # анализ текста и вернуть статистику
    total_chars = len(text)
    total_chars_no_space = len(text.replace(" ", ""))

    words = text.split()
    word_count = len(words)

    if word_count == 0:
        return None  # защита от пустого текста

    # Частотность слов
    freq_counter = Counter(words)
    most_common = freq_counter.most_common(5)

    # Длинные слова
    longest_words = sorted(set(words), key=lambda w: (-len(w), w))[:5]

    # Средняя длина
    avg_length = sum(len(w) for w in words) / word_count

    return {
        "total_chars": total_chars,
        "total_chars_no_space": total_chars_no_space,
        "word_count": word_count,
        "most_common": most_common,
        "longest_words": longest_words,
        "avg_length": avg_length
    }


def print_statistics(stats):
    #вывести результаты анализа текста
    print("\nРезультаты анализа:")
    print(f"Общее количество символов: {stats['total_chars']} (без пробелов: {stats['total_chars_no_space']})")
    print(f"Количество словоформ: {stats['word_count']}")

    print("Самые частые словоформы:")
    for word, freq in stats["most_common"]:
        print(f"- '{word}': {freq} раз(а)")

    print("Самые длинные словоформы:")
    for word in stats["longest_words"]:
        print(f"- '{word}' ({len(word)} букв)")

    print(f"Средняя длина словоформы: {stats['avg_length']:.1f} символа")


def main():
    text = get_text()
    clean_text = preprocess_text(text)
    stats = analyze_text(clean_text)

    if stats:
        print_statistics(stats)
    else:
        print("Текст не содержит слов для анализа.")


if __name__ == "__main__":
    main()
