from cdb import CentralDataBus
from cdbconsumer import CDBConsumer
class IssuedInstruction:
    def __init__(self) -> None:
        self.id = 0
        self.original_dest = ""
        self.assigned_dest = ""
        self.val_left = None
        self.val_right = None
        self.dep_left = None
        self.dep_right = None
    

class Entry:
    def __init__(self) -> None:
        self.busy = False
        pass # TODO


class ReorderBuffer(CDBConsumer):
    def __init__(self, cdb: CentralDataBus, len=10) -> None:
        super().__init__(cdb)
        self.entries = [Entry() for _ in range(len)]
        # TODO
    
    def entry_is_free(self) -> bool:
        for entry in self.entries:
            if not entry.busy:
                return True
        return False