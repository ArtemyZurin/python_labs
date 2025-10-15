import json
import os
from typing import List, Optional


class Task:
    """Класс, представляющий одну задачу.

    Атрибуты:
        description (str): Текст описания задачи.
        _status (bool): protected атрибут — статус выполнения (True = выполнено).
        category (str): категория задачи (например, 'work', 'pstu').
        __id (int): приватный идентификатор задачи (name mangling).
    """

    def __init__(self, description: str, category: str = "general", task_id: Optional[int] = None):
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Описание задачи должно быть непустой строкой.")
        self.description = description.strip()
        self._status = False  # protected: используем _ для обозначения
        self.category = category.strip() if isinstance(category, str) and category.strip() else "general"
        # приватный id — не должен изменяться извне
        self.__id = task_id if task_id is not None else -1

    # --- свойства для доступа к приватному id ---
    @property
    def id(self) -> int:
        return self.__id

    def _set_id(self, new_id: int):
        """Внутренний метод для установки id (используется трекером)."""
        if not isinstance(new_id, int) or new_id < 0:
            raise ValueError("ID должен быть неотрицательным целым числом")
        self.__id = new_id

    # --- методы статуса ---
    def mark_done(self):
        """Отметить задачу как выполненную."""
        self._status = True

    def mark_undone(self):
        """Снять отметку о выполнении."""
        self._status = False

    def is_done(self) -> bool:
        return self._status

    # --- сериализация в/из словаря для JSON ---
    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "description": self.description,
            "status": self._status,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        task = cls(description=data.get("description", ""), category=data.get("category", "general"), task_id=data.get("id"))
        task._status = bool(data.get("status", False))
        return task

    # --- строковое представление ---
    def __str__(self) -> str:
        checkbox = "[x]" if self._status else "[ ]"
        return f"{checkbox} {self.description} #{self.category} (id={self.__id})"

    def __repr__(self) -> str:
        # официальный вид, пригодный для отладки
        return (
            f"Task(description={self.description!r}, category={self.category!r}, task_id={self.__id!r})"
        )


class TaskTracker:
    """Трекер задач. Хранит коллекцию Task и обеспечивает CRUD + поиск.

    Использует JSON-файл для сохранения/загрузки состояния.
    """

    def __init__(self, storage_path: str = "tasks.json"):
        self.storage_path = storage_path
        self._tasks: List[Task] = []  # protected список задач
        self.__next_id = 1  # приватный счётчик идентификаторов
        self.load()

    # --- внутренные утилиты ---
    def _recalculate_next_id(self):
        if not self._tasks:
            self.__next_id = 1
        else:
            self.__next_id = max(t.id for t in self._tasks) + 1

    def _find_by_id(self, task_id: int) -> Optional[Task]:
        for t in self._tasks:
            if t.id == task_id:
                return t
        return None

    # --- основное API ---
    def add_task(self, description: str, category: str = "general") -> Task:
        task = Task(description=description, category=category)
        task._set_id(self.__next_id)
        self.__next_id += 1
        self._tasks.append(task)
        return task

    def mark_task_done(self, task_id: int) -> bool:
        task = self._find_by_id(task_id)
        if task:
            task.mark_done()
            return True
        return False

    def mark_task_undone(self, task_id: int) -> bool:
        task = self._find_by_id(task_id)
        if task:
            task.mark_undone()
            return True
        return False

    def list_tasks(self) -> List[Task]:
        return list(self._tasks)

    def tasks_by_category(self, category: str) -> List[Task]:
        return [t for t in self._tasks if t.category.lower() == category.lower()]

    def search(self, query: str) -> List[Task]:
        q = query.lower()
        return [t for t in self._tasks if q in t.description.lower() or q in t.category.lower()]

    # --- сохранение/загрузка ---
    def save(self):
        data = [t.to_dict() for t in self._tasks]
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Не удалось сохранить задачи: {e}")

    def load(self):
        if not os.path.exists(self.storage_path):
            return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._tasks = [Task.from_dict(d) for d in data if isinstance(d, dict)]
            self._recalculate_next_id()
        except Exception as e:
            print(f"Не удалось загрузить данные из {self.storage_path}: {e}")
            self._tasks = []
            self.__next_id = 1

    # --- вспомогательные методы для удобства CLI ---
    def print_tasks(self, tasks: Optional[List[Task]] = None):
        tasks = tasks if tasks is not None else self._tasks
        if not tasks:
            print("Список задач пуст.")
            return
        for t in tasks:
            print(t)


def safe_input_int(prompt: str) -> Optional[int]:
    """Запрашивает у пользователя целое число; при пустом вводе возвращает None."""
    while True:
        s = input(prompt).strip()
        if s == "":
            return None
        if s.isdigit():
            return int(s)
        print("Ошибка: введите целое положительное число или нажмите Enter для отмены.")


def main():
    tracker = TaskTracker()

    MENU = (
        "\nМеню:\n"
        "1. Добавить задачу\n"
        "2. Отметить задачу как выполненную\n"
        "3. Снять отметку о выполнении\n"
        "4. Показать все задачи\n"
        "5. Показать задачи по категории\n"
        "6. Найти задачи (по описанию/категории)\n"
        "7. Сохранить и выйти"
    )

    while True:
        print(MENU)
        choice = input("Выберите действие (1-7): ").strip()

        if choice == "1":
            desc = input("Описание задачи: ").strip()
            if not desc:
                print("Описание не может быть пустым.")
                continue
            cat = input("Категория (нажмите Enter для 'general'): ").strip()
            task = tracker.add_task(desc, cat if cat else "general")
            tracker.save()
            print(f"Добавлено: {task}")

        elif choice == "2":
            tid = safe_input_int("ID задачи для отметки как выполненной (Enter для отмены): ")
            if tid is None:
                continue
            if tracker.mark_task_done(tid):
                tracker.save()
                print("Задача отмечена как выполненная.")
            else:
                print("Задача с таким ID не найдена.")

        elif choice == "3":
            tid = safe_input_int("ID задачи для снятия отметки (Enter для отмены): ")
            if tid is None:
                continue
            if tracker.mark_task_undone(tid):
                tracker.save()
                print("Отметка о выполнении снята4")
            else:
                print("Задача с таким ID не найдена")

        elif choice == "4":
            print("\nВсе задачи:")
            tracker.print_tasks()

        elif choice == "5":
            cat = input("Введите категорию для фильтрации: ").strip()
            if not cat:
                print("Категория не может быть пустой")
                continue
            tasks = tracker.tasks_by_category(cat)
            print(f"\nЗадачи в категории '{cat}':")
            tracker.print_tasks(tasks)

        elif choice == "6":
            q = input("Введите поисковый запрос (в описании или категории): ").strip()
            if not q:
                print("Пустой запрос")
                continue
            found = tracker.search(q)
            print(f"\nНайдено {len(found)} задач(ы):")
            tracker.print_tasks(found)

        elif choice == "7":
            tracker.save()
            print("Данные сохранены")
            break

        else:
            print("Неверный выбор. Введите число от 1 до 7.")


if __name__ == "__main__":
    main()
