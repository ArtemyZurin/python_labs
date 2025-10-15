# === Реестр плагинов ===
PluginRegistry = {}


class Plugin:
    """
    Базовый класс для всех плагинов.
    Каждый подкласс автоматически регистрируется при создании.
    """

    # Метод __init_subclass__ вызывается автоматически при создании любого подкласса.
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Проверяем, что у подкласса есть уникальный атрибут 'name'
        if not hasattr(cls, "name"):
            raise AttributeError(f"Класс {cls.__name__} должен иметь атрибут 'name'!")
        if cls.name in PluginRegistry:
            raise ValueError(f"Плагин с именем '{cls.name}' уже зарегистрирован!")
        # Добавляем класс в реестр
        PluginRegistry[cls.name] = cls

    def execute(self, data):
        """Метод, который должен быть реализован в подклассах."""
        raise NotImplementedError("Метод execute() должен быть реализован в плагине!")


# === Конкретные плагины ===

class UpperCasePlugin(Plugin):
    """Плагин, преобразующий строку в верхний регистр."""
    name = "upper"

    def execute(self, data: str) -> str:
        return data.upper()


class ReversePlugin(Plugin):
    """Плагин, переворачивающий строку."""
    name = "reverse"

    def execute(self, data: str) -> str:
        return data[::-1]


class ReplaceSpacesPlugin(Plugin):
    """Плагин, заменяющий пробелы на подчеркивания."""
    name = "replace_spaces"

    def execute(self, data: str) -> str:
        return data.replace(" ", "_")


# === Демонстрация работы ===
if __name__ == "__main__":
    print("Реестр плагинов:")
    print(PluginRegistry)

    # Выбираем плагин из реестра
    plugin = PluginRegistry["upper"]()
    print(plugin.execute("hello"))  # -> "HELLO WORLD"

    plugin2 = PluginRegistry["reverse"]()
    print(plugin2.execute("Program"))  # -> "nohtyP"

    plugin3 = PluginRegistry["replace_spaces"]()
    print(plugin3.execute("Привет всем"))  # -> "Привет_мир"
