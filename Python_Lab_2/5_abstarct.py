from abc import ABC, abstractmethod


class Vehicle(ABC):
    """Абстрактный базовый класс для всех транспортных средств."""

    @abstractmethod
    def get_max_speed(self) -> float:
        """Возвращает максимальную скорость (км/ч)."""
        pass

    @abstractmethod
    def get_vehicle_type(self) -> str:
        """Возвращает тип транспортного средства (строка)."""
        pass


class RoadVehicle(Vehicle):
    """Абстрактный подкласс для наземных транспортных средств."""

    @abstractmethod
    def get_engine_type(self) -> str:
        """Возвращает тип двигателя."""
        pass


class Car(RoadVehicle):
    """Класс, представляющий автомобиль."""

    def __init__(self, brand: str, max_speed: float, engine_type: str):
        if engine_type not in ("бензиновый", "электрический"):
            raise ValueError("Тип двигателя должен быть 'бензиновый' или 'электрический'")
        self.brand = brand
        self._max_speed = float(max_speed)
        self._engine_type = engine_type

    def get_max_speed(self) -> float:
        return self._max_speed

    def get_vehicle_type(self) -> str:
        return "Автомобиль"

    def get_engine_type(self) -> str:
        return self._engine_type

    def __str__(self) -> str:
        return f"Car(марка={self.brand}, скорость={self._max_speed} км/ч, двигатель={self._engine_type})"

    def __repr__(self) -> str:
        return f"Car(brand={self.brand!r}, max_speed={self._max_speed!r}, engine_type={self._engine_type!r})"


class Bicycle(RoadVehicle):
    """Класс, представляющий велосипед."""

    def __init__(self, brand: str, max_speed: float):
        self.brand = brand
        self._max_speed = float(max_speed)
        self._engine_type = "мускульная сила"

    def get_max_speed(self) -> float:
        return self._max_speed

    def get_vehicle_type(self) -> str:
        return "Велосипед"

    def get_engine_type(self) -> str:
        return self._engine_type

    def __str__(self) -> str:
        return f"Bicycle(марка={self.brand}, скорость={self._max_speed} км/ч, двигатель={self._engine_type})"

    def __repr__(self) -> str:
        return f"Bicycle(brand={self.brand!r}, max_speed={self._max_speed!r})"


# --- демонстрация ---
if __name__ == "__main__":
    car = Car("Tesla", 250, "электрический")
    bike = Bicycle("Stels", 40)

    print(car)
    print(bike)

    print("Тип car:", car.get_vehicle_type())
    print("Тип bike:", bike.get_vehicle_type())
    print("Двигатель car:", car.get_engine_type())
    print("Двигатель bike:", bike.get_engine_type())