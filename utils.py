type number = int | float

class IssuedInstruction:
    def __init__(self) -> None:
        self.id = 0
        self.op = ""
        self.original_dest = ""
        self.assigned_dest = ""
        self.val_left = None
        self.val_right = None
        self.dep_left = None
        self.dep_right = None
        self.offset = 0
    
    def __str__(self) -> str:
        return str(vars(self))
    

TYPE_INT_ADDER = 'INT_ADDER'
TYPE_DEC_ADDER = 'DEC_ADDER'
TYPE_DEC_MULTP = 'DEC_MULTP'
TYPE_MEMORY_LOAD = 'MEMORY_LOADER'
TYPE_MEMORY_STORE = 'MEMORY_STORER'
TYPE_MEMORY_FORWARDING = 'FOUND_STORE_FORWARDING'