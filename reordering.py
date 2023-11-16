
class IssuedInstruction:
    def __init__(self) -> None:
        self.id = 0
        self.original_dest = ""
        self.assigned_dest = ""
        self.val_left = None
        self.val_right = None
        self.dep_left = None
        self.dep_right = None
    