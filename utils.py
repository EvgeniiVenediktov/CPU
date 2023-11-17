type number = int | float

class IssuedInstruction: # TODO
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
    