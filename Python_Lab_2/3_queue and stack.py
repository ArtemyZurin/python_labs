class Queue:
    """Класс Очередь (FIFO — First In, First Out)."""

    def __init__(self):
        # _items — защищённый атрибут, хранящий элементы очереди
        self._items = []

    def enqueue(self, item):
        """Добавление элемента в конец очереди."""
        self._items.append(item)

    def dequeue(self):
        """Удаление и возврат элемента из начала очереди."""
        if self.is_empty():
            raise IndexError("Очередь пуста — невозможно извлечь элемент.")
        return self._items.pop(0)

    def peek(self):
        """Просмотр первого элемента без удаления."""
        if self.is_empty():
            raise IndexError("Очередь пуста — нечего просматривать.")
        return self._items[0]

    def is_empty(self):
        """Проверка, пуста ли очередь."""
        return len(self._items) == 0

    def size(self):
        """Возвращает количество элементов в очереди."""
        return len(self._items)

    def __str__(self):
        return f"Queue({self._items})"

    def __repr__(self):
        return f"Queue(items={self._items!r})"


class Stack:
    """Класс Стек (LIFO — Last In, First Out)."""

    def __init__(self):
        # _items — защищённый атрибут, хранящий элементы стека
        self._items = []

    def push(self, item):
        """Добавление элемента на вершину стека."""
        self._items.append(item)

    def pop(self):
        """Удаление и возврат элемента с вершины стека."""
        if self.is_empty():
            raise IndexError("Стек пуст — невозможно извлечь элемент.")
        return self._items.pop()

    def peek(self):
        """Просмотр верхнего элемента без удаления."""
        if self.is_empty():
            raise IndexError("Стек пуст — нечего просматривать.")
        return self._items[-1]

    def is_empty(self):
        """Проверка, пуст ли стек."""
        return len(self._items) == 0

    def size(self):
        """Возвращает количество элементов в стеке."""
        return len(self._items)

    def __str__(self):
        return f"Stack({self._items})"

    def __repr__(self):
        return f"Stack(items={self._items!r})"


if __name__ == "__main__":
    # Демонстрация работы классов

    print("=== Демонстрация Queue ===")
    q = Queue()
    q.enqueue("первый")
    q.enqueue("второй")
    q.enqueue("третий")
    print("Очередь:", q)
    print("Первый элемент:", q.peek())
    print("Удалён элемент:", q.dequeue())
    print("После удаления:", q)
    print("Размер:", q.size())

    print("\n=== Демонстрация Stack ===")
    s = Stack()
    s.push("A")
    s.push("B")
    s.push("C")
    print("Стек:", s)
    print("Верхний элемент:", s.peek())
    print("Снято с вершины:", s.pop())
    print("После снятия:", s)
    print("Размер:", s.size())
