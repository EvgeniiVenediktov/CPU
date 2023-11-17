# CDB - Central Data Bus module
from utils import number
from utils import TYPE_INT_ADDER,TYPE_DEC_ADDER,TYPE_DEC_MULTP,TYPE_MEMORY_LOAD,TYPE_MEMORY_STORE

class FunctionResult:
    def __init__(self, id:int, rob_dest: str, value:number, op:str, producer:str) -> None:
        self.id = id
        self.rob_dest = rob_dest
        self.value = value
        self.op = op
        self.producer = producer


class CentralDataBus:
    """ Central Data Bus holds current ready values
    """
    def __init__(self) -> None:
        self.current_value = None
        self.fu_buffs :dict[str, list[FunctionResult]] = {TYPE_INT_ADDER:[],TYPE_DEC_ADDER:[],TYPE_DEC_MULTP:[],TYPE_MEMORY_LOAD:[],TYPE_MEMORY_STORE:[]}

    def write(self, result:FunctionResult) -> None:
        if self.current_value == None:
            self.current_value = result
            return
        self.fu_buffs[result.producer].append(result)
        self.fu_buffs[result.producer] = sorted(self.fu_buffs[result.producer], key=lambda r: r.id)

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
        if new_current == None:
            return 
        # Remove selected
        del self.fu_buffs[function][0]

        # Record new current
        self.current_value = new_current