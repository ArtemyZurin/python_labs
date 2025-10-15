import json
import os
from typing import List, Optional


class Transaction:
    """Класс для одной финансовой операции."""

    def __init__(self, description: str, amount: float, t_type: str, category: str = "general", trans_id: Optional[int] = None):
        if not description.strip():
            raise ValueError("Описание не может быть пустым")
        if t_type.lower() not in ["доход", "расход"]:
            raise ValueError("Тип операции должен быть 'доход' или 'расход'")
        if not isinstance(amount, (int, float)):
            raise ValueError("Сумма должна быть числом")

        self.description = description.strip()
        self.amount = float(amount)
        self.type = t_type.lower()
        self.category = category.strip() if category.strip() else "general"
        self.__id = trans_id if trans_id is not None else -1

    @property
    def id(self) -> int:
        return self.__id

    def _set_id(self, new_id: int):
        if not isinstance(new_id, int) or new_id < 0:
            raise ValueError("ID должен быть неотрицательным числом")
        self.__id = new_id

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "description": self.description,
            "amount": self.amount,
            "type": self.type,
            "category": self.category
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        trans = cls(
            description=data.get("description", ""),
            amount=data.get("amount", 0),
            t_type=data.get("type", "доход"),
            category=data.get("category", "general"),
            trans_id=data.get("id")
        )
        return trans

    def __str__(self):
        sign = '+' if self.type == 'доход' else '-'
        return f"{sign}{self.amount:.2f} {self.description} #{self.category} (id={self.__id})"

    def __repr__(self):
        return f"Transaction(description={self.description!r}, amount={self.amount!r}, t_type={self.type!r}, category={self.category!r}, trans_id={self.__id!r})"


class BudgetTracker:

    def __init__(self, storage_path: str = "budget.json"):
        self.storage_path = storage_path
        self._transactions: List[Transaction] = []
        self.__next_id = 1
        self.load()

    def _recalculate_next_id(self):
        if not self._transactions:
            self.__next_id = 1
        else:
            self.__next_id = max(t.id for t in self._transactions) + 1

    def _find_by_id(self, trans_id: int) -> Optional[Transaction]:
        for t in self._transactions:
            if t.id == trans_id:
                return t
        return None

    def add_transaction(self, description: str, amount: float, t_type: str, category: str = "general") -> Transaction:
        trans = Transaction(description, amount, t_type, category)
        trans._set_id(self.__next_id)
        self.__next_id += 1
        self._transactions.append(trans)
        return trans

    def calculate_balance(self) -> float:
        balance = 0
        for t in self._transactions:
            if t.type == 'доход':
                balance += t.amount
            else:
                balance -= t.amount
        return balance

    def list_transactions(self) -> List[Transaction]:
        return list(self._transactions)

    def transactions_by_category(self, category: str) -> List[Transaction]:
        return [t for t in self._transactions if t.category.lower() == category.lower()]

    def save(self):
        data = [t.to_dict() for t in self._transactions]
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def load(self):
        if not os.path.exists(self.storage_path):
            return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._transactions = [Transaction.from_dict(d) for d in data if isinstance(d, dict)]
            self._recalculate_next_id()
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            self._transactions = []
            self.__next_id = 1

    def print_transactions(self, transactions: Optional[List[Transaction]] = None):
        transactions = transactions if transactions is not None else self._transactions
        if not transactions:
            print("Список операций пуст.")
            return
        for t in transactions:
            print(t)


def safe_input_float(prompt: str) -> Optional[float]:
    while True:
        s = input(prompt).strip()
        if s == "":
            return None
        try:
            return float(s)
        except ValueError:
            print("Ошибка: введите число или нажмите Enter для отмены.")


def main():
    tracker = BudgetTracker()

    MENU = (
        "\nМеню:\n"
        "1. Добавить операцию\n"
        "2. Показать баланс\n"
        "3. Показать все операции\n"
        "4. Показать операции по категории\n"
        "5. Сохранить и выйти"
    )

    while True:
        print(MENU)
        choice = input("Выберите действие (1-5): ").strip()

        if choice == "1":
            desc = input("Описание операции: ").strip()
            if not desc:
                print("Описание не может быть пустым.")
                continue
            amount = safe_input_float("Сумма: ")
            if amount is None:
                continue
            t_type = input("Тип (доход/расход): ").strip().lower()
            if t_type not in ["доход", "расход"]:
                print("Тип должен быть 'доход' или 'расход'.")
                continue
            cat = input("Категория (Enter для 'general'): ").strip()
            trans = tracker.add_transaction(desc, amount, t_type, cat if cat else "general")
            tracker.save()
            print(f"Добавлено: {trans}")

        elif choice == "2":
            balance = tracker.calculate_balance()
            print(f"Текущий баланс: {balance:.2f}")

        elif choice == "3":
            print("Все операции:")
            tracker.print_transactions()

        elif choice == "4":
            cat = input("Введите категорию: ").strip()
            if not cat:
                print("Категория не может быть пустой.")
                continue
            transactions = tracker.transactions_by_category(cat)
            print(f"Операции в категории '{cat}':")
            tracker.print_transactions(transactions)

        elif choice == "5":
            tracker.save()
            print("Данные сохранены. До свидания!")
            break

        else:
            print("Неверный выбор. Введите число от 1 до 5.")


if __name__ == "__main__":
    main()
