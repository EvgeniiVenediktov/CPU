# CDB - Central Data Bus module
class NameAndValue:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    def value(self) -> float:
        return self.value
    def name(self) -> str:
        return self.name

class CentralDataBus:
    """ Central Data Bus holds current ready values
    """
    # TODO: ask if value can sit for multiple cycles
    def __init__(self) -> None:
        self.__current_values = []

    def write(self, destination: str, value) -> None:
        self.__current_values.append([destination, value])

    def read(self) -> list[NameAndValue]:
        return self.__current_values

    def flush(self) -> None:
        self.__current_values = []