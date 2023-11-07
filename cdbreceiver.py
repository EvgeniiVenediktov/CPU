# CDB Receiver super-class

class NameAndValue():
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value
    def unpack(self) -> tuple(str, float):
        return self.name, self.value
    def value(self) -> float:
        return self.value
    def name(self) -> str:
        return self.name


class CentralDataBus():
    """ TODO implement\n
        A Stub for CDB class
    """
    def __init__(self) -> None:
        self.__current_values = []
    
    def write(self, name: str, value) -> None:
        self.__current_values.append([name, value])
    
    def read(self) -> list[NameAndValue]:
        return self.__current_values
    
    def flush(self) -> None:
        self.__current_values = []


class CDBReceiver():
    """
        CDB Receiver is a superclass.
        It's heirs are able to listen to CDB (Central Data Bus) 
        and check for the variables values they await at the moment.

    """
    def __init__(self, cdb: CentralDataBus) -> None:
        self.cdb = cdb
        self.variables_to_get = []
    
    def fetch_from_cdb(self) -> list[NameAndValue]:
        contents = self.cdb.read()
        results = []
        for elem in contents:
            name, _ = elem.unpack()
            if name in self.variables_to_get:
                results.append(elem)

        return results
    





