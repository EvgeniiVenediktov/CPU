# RS 
from cdb import CentralDataBus
from cdbconsumer import CDBConsumer

class Entry():
    """```
    Busy - is it busy     - `busy`  
    Op   - operation type - `op`    
    Vj   - value 1        - `val1`  
    Vk   - value 2        - `val2`  
    Qj   - dependency 1   - `dep1`  
    Qk   - dependency 2   - `dep1`  
    A    - result         - `result`
    ```
    """
    def flush(self) -> None:
        self.busy = 0
        self.op = ""
        self.val1 = 0
        self.val2 = 0
        self.dep1 = ""
        self.dep2 = ""
        self.result = 0

    def __init__(self) -> None:
        self.flush()

    #def new(self, instr: Instruction) -> None: # TODO

    def update(self, 
               busy = None,
               op = None,
               val1 = None,
               val2 = None,
               dep1 = None,
               dep2 = None,
               result = None
               ) -> None:
        args = {'busy':busy,'op':op,'val1':val1,'val2':val2,'dep1':dep1,'dep2':dep2,'result':result}
        for arg in args:
            val = args[arg]
            if val == None:
                continue
            setattr(self, arg, val)
        

class ReservationStation(CDBConsumer):
    """Reservation Station holds a list of `Entry`'s.
    \nCDB consumer.
    """
    def __init__(self, cdb: CentralDataBus, len=5,) -> None:
        super().__init__(cdb)
        self.entries = [Entry() for _ in range(len)]
    
    def add_instruction(self, instr) -> bool:
        for entry in self.entries:
            if entry.busy == 0:
                entry.new(instr)
                return True
        return False
    
