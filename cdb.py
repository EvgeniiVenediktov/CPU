# CDB - Central Data Bus module
from utils import number

class FunctionResult:
    def __init__(self, id:int, rob_dest: str, value:number, function:str) -> None:
        self.id = id
        self.rob_dest = rob_dest
        self.value = value
        self.function = function


INT_ADDER_NAME = "addi"
DEC_ADDER_NAME = "addd"
DEC_MULTR_NAME = "multd"


class CentralDataBus:
    """ Central Data Bus holds current ready values
    """
    def __init__(self) -> None:
        self.current_value = None
        self.fu_buffs :dict[str, list[FunctionResult]] = {INT_ADDER_NAME:[], DEC_ADDER_NAME:[], DEC_MULTR_NAME:[]}

    def write(self, result:FunctionResult) -> None:
        if self.current_value == None:
            self.current_value = result
            return
        self.fu_buffs[function].append(result)
        self.fu_buffs[function] = sorted(self.fu_buffs[function], key=lambda r: r.id)

    def read(self) -> FunctionResult:
        return self.current_value

    def flush_current_bump_buffered(self) -> None:
        # Select new current value
        new_current = None
        lowest = 999999999999999
        function = ""
        for func in self.fu_buffs:
            q = self.fu_buffs[func]
            if len(q) == 0:
                continue
            # CDB Arbiter
            result = q[0]
            if result.id < lowest:
                lowest = result.id
                new_current = result
                function = func
        # Remove selected
        del self.fu_buffs[function][0]

        # Record new current
        self.current_value = new_current