from reservationstation import number
# CDB - Central Data Bus module
class FunctionResult:
    def __init__(self, id:int, name: str, value:number, function:str) -> None:
        self.id = id
        self.name = name
        self.value = value
        self.function = function
    
    def name(self) -> str:
        return self.name
    def value(self) -> str:
        return self.value


INT_ADDER_NAME = "addi"
DEC_ADDER_NAME = "addd"
DEC_MULTR_NAME = "multd"


class CentralDataBus:
    """ Central Data Bus holds current ready values
    """
    def __init__(self) -> None:
        self.__current_value = None
        self.__fu_buffs :dict[str, list[FunctionResult]] = {INT_ADDER_NAME:[], DEC_ADDER_NAME:[], DEC_MULTR_NAME:[]}

    def write(self, id:int, name: str, value:number, function:str) -> None:
        result = FunctionResult(id, name, value, function)
        if self.__current_value == None:
            self.__current_value = result
            return
        self.__fu_buffs[function].append(result)
        self.__fu_buffs[function] = sorted(self.__fu_buffs[function], key=lambda r: r.id)

    def read(self) -> FunctionResult:
        return self.__current_value

    def flush_current_bump_buffered(self) -> None:
        # Select new current value
        new_current = None
        lowest = 999999999999999
        function = ""
        for func in self.__fu_buffs:
            q = self.__fu_buffs[func]
            if len(q) == 0:
                continue
            # CDB Arbiter
            result = q[0]
            if result.id < lowest:
                lowest = result.id
                new_current = result
                function = func
        # Remove selected
        del self.__fu_buffs[function][0]

        # Record new current
        self.__current_value = new_current