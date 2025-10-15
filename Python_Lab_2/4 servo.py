from __future__ import annotations
from typing import List, Tuple, Union
import copy


class Motor:
    """Базовый класс двигателя (уровень 1).

    Атрибуты (используем protected/ private соглашения):
      - _angle: текущий угол поворота в градусах (protected)
      - _speed: скорость вращения (deg/s) (protected)
      - _acceleration: ускорение (deg/s^2) (protected)
      - __serial: приватный серийный номер (name mangling)
    """

    def __init__(self, angle: float = 0.0, speed: float = 0.0, acceleration: float = 0.0, serial: str | None = None):
        self._angle = float(angle)
        self._speed = float(speed)
        self._acceleration = float(acceleration)
        self.__serial = serial if serial is not None else "unknown"

    # --- свойства для инкапсуляции ---
    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, value: float):
        try:
            self._angle = float(value)
        except (TypeError, ValueError):
            raise ValueError("angle must be a number")

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: float):
        try:
            self._speed = float(value)
        except (TypeError, ValueError):
            raise ValueError("speed must be a number")

    @property
    def acceleration(self) -> float:
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value: float):
        try:
            self._acceleration = float(value)
        except (TypeError, ValueError):
            raise ValueError("acceleration must be a number")

    @property
    def serial(self) -> str:
        return self.__serial

    def __str__(self) -> str:
        return f"Motor(serial={self.__serial}, angle={self._angle:.2f}deg)"

    def __repr__(self) -> str:
        return f"Motor(angle={self._angle!r}, speed={self._speed!r}, acceleration={self._acceleration!r}, serial={self.__serial!r})"


class RotaryMotor(Motor):
    """Вращательный двигатель (уровень 2).

    Добавляет атрибуты, связанные с вращением: диапазон углов и инерция.
    """

    def __init__(self, angle: float = 0.0, speed: float = 0.0, acceleration: float = 0.0,
                 min_angle: float = -180.0, max_angle: float = 180.0, inertia: float = 0.0, serial: str | None = None):
        super().__init__(angle, speed, acceleration, serial)
        self.min_angle = float(min_angle)
        self.max_angle = float(max_angle)
        self.inertia = float(inertia)

    def set_angle_clamped(self, angle: float):
        """Установить угол, соблюдая допустимый диапазон."""
        a = float(angle)
        if a < self.min_angle:
            self._angle = self.min_angle
        elif a > self.max_angle:
            self._angle = self.max_angle
        else:
            self._angle = a

    def __str__(self) -> str:
        return f"RotaryMotor(angle={self._angle:.2f}deg, range=[{self.min_angle},{self.max_angle}])"

    def __repr__(self) -> str:
        return (f"RotaryMotor(angle={self._angle!r}, speed={self._speed!r}, acceleration={self._acceleration!r},"
                f" min_angle={self.min_angle!r}, max_angle={self.max_angle!r}, inertia={self.inertia!r})")


class SynchroServo(RotaryMotor):
    """Синхронный сервопривод (уровень 3).

    Добавляет специфичные для сервопривода атрибуты: мощность и точность.
    Также перегружены операторы сравнения по мощности.
    """

    def __init__(self, angle: float = 0.0, speed: float = 0.0, acceleration: float = 0.0,
                 min_angle: float = -180.0, max_angle: float = 180.0, inertia: float = 0.0,
                 power: float = 10.0, precision: float = 0.1, serial: str | None = None):
        super().__init__(angle, speed, acceleration, min_angle, max_angle, inertia, serial)
        self.power = float(power)  # мощность в ваттах
        self.precision = float(precision)  # точность в градусах
        # приватный флаг состояния
        self.__enabled = True

    def enable(self):
        self.__enabled = True

    def disable(self):
        self.__enabled = False

    def is_enabled(self) -> bool:
        return self.__enabled

    # --- сравнение по мощности ---
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SynchroServo):
            return NotImplemented
        return self.power == other.power

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SynchroServo):
            return NotImplemented
        return self.power < other.power

    def __le__(self, other: object) -> bool:
        if not isinstance(other, SynchroServo):
            return NotImplemented
        return self.power <= other.power

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, SynchroServo):
            return NotImplemented
        return self.power > other.power

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, SynchroServo):
            return NotImplemented
        return self.power >= other.power

    def move_to(self, angle: float):
        """Плавное движение к углу с учётом точности и диапазона."""
        if not self.__enabled:
            raise RuntimeError("Сервопривод отключен")
        # учитываем точность: округляем до ближайшего разрешённого шага
        target = round(float(angle) / self.precision) * self.precision
        self.set_angle_clamped(target)

    def __str__(self) -> str:
        status = "on" if self.__enabled else "off"
        return f"SynchroServo(power={self.power}W, angle={self._angle:.2f}deg, {status})"

    def __repr__(self) -> str:
        return (f"SynchroServo(angle={self._angle!r}, power={self.power!r}, precision={self.precision!r},"
                f" min_angle={self.min_angle!r}, max_angle={self.max_angle!r})")


class Manipulator:
    """Упрощённая модель шестизвенного манипулятора.

    Состоит из 6 сервоприводов (SynchroServo). Поддерживает сложение с вектором
    перемещения для упрощённого изменения углов звеньев через __add__.
    """

    def __init__(self, servos: List[SynchroServo] | None = None):
        if servos is None:
            # создаём 6 стандартных сервоприводов
            self._servos = [SynchroServo() for _ in range(6)]
        else:
            if len(servos) != 6:
                raise ValueError("Manipulator requires exactly 6 servos")
            self._servos = list(servos)

    def joints(self) -> List[SynchroServo]:
        return list(self._servos)

    def __str__(self) -> str:
        parts = [f"J{i+1}:{s._angle:.1f}deg" for i, s in enumerate(self._servos)]
        return "Manipulator(" + ", ".join(parts) + ")"

    def __repr__(self) -> str:
        return f"Manipulator(servos={self._servos!r})"

    def copy(self) -> Manipulator:
        # глубокая копия сервоприводов
        return Manipulator(servos=copy.deepcopy(self._servos))

    def move_joints(self, deltas: List[float]):
        """Изменить углы каждого звена на соответствующие приращения.

        deltas должно быть длины 6.
        """
        if len(deltas) != 6:
            raise ValueError("deltas must be list of 6 floats")
        for s, d in zip(self._servos, deltas):
            s.move_to(s.angle + float(d))

    def __add__(self, other: Union[Tuple[float, float, float], List[float], Tuple[float, ...]]):
        """Операция сложения: манипулятор + вектор.

        Поддерживаются два варианта:
          - если передан список/кортеж длины 6, он трактуется как приращения углов (deg).
          - если длина 3 — вектор перемещения (dx,dy,dz), который распределяется по суставам
            простым правилом: угол изменения для сустава i = factor_i * (dx+dy+dz).
        Возвращает НОВЫЙ объект Manipulator (иммутабельный стиль для оператора +).
        """
        new = self.copy()

        if not isinstance(other, (list, tuple)):
            raise TypeError("Can only add Manipulator with a sequence of numbers")

        if len(other) == 6:
            deltas = [float(x) for x in other]
            new.move_joints(deltas)
            return new

        if len(other) == 3:
            # очень упрощённая модель: распределяем сумму смещений по суставам с разными коэффициентами
            dx, dy, dz = (float(x) for x in other)
            total = dx + dy + dz
            # коэффициенты показывают, какой сустав больше реагирует
            factors = [0.2, 0.15, 0.15, 0.2, 0.15, 0.15]
            deltas = [total * f for f in factors]
            new.move_joints(deltas)
            return new

        raise ValueError("Unsupported vector length: must be 3 or 6")

    def __iadd__(self, other: Union[List[float], Tuple[float, ...]]):
        """Операция += изменяет текущий манипулятор."""
        result = self + other
        # заменяем сервоприводы на те, что в результате
        self._servos = result._servos
        return self


# --- демонстрация ---
if __name__ == "__main__":
    # создаём несколько сервоприводов с разной мощностью
    s1 = SynchroServo(angle=0, power=10.0, precision=0.5)
    s2 = SynchroServo(angle=10, power=15.0, precision=0.5)
    s3 = SynchroServo(angle=-5, power=12.0, precision=0.2)
    s4 = SynchroServo(angle=20, power=8.0, precision=0.1)
    s5 = SynchroServo(angle=5, power=11.0, precision=0.5)
    s6 = SynchroServo(angle=0, power=9.0, precision=0.5)

    manip = Manipulator(servos=[s1, s2, s3, s4, s5, s6])
    print("Исходный манипулятор:", manip)

    # сравнение сервоприводов по мощности
    print("s2 > s3?", s2 > s3)
    print("s4 < s1?", s4 < s1)

    # добавляем вектор приращений углов (6 значений)
    moved = manip + [5, -3, 2, 0, 1, -2]
    print("После приращений (новый объект):", moved)
    print("Оригинал остался:", manip)

    # применяем вектор перемещения (dx,dy,dz)
    moved2 = manip + (0.5, 0.0, -0.2)
    print("После вектора перемещения (новый объект):", moved2)

    # in-place
    manip += [1,1,1,1,1,1]
    print("Оригинал после += :", manip)
