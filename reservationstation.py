# RS 
from cdb import CentralDataBus
from cdbconsumer import CDBConsumer
from reordering import IssuedInstruction
from cpu import number


INT_ADDER_RS_TYPE = "int_adder"
DEC_ADDER_RS_TYPE = "dec_adder"
DEC_MULTP_RS_TYPE = "dec_multp"
LD_STORE_RS_TYPE = "ld_st_rs_type"

class Entry:
    """```
    Busy - is it busy     - `busy`  
    ROD  - ROB entry      - `rob`
    Op   - operation type - `op`    
    Vj   - value 1        - `val1`  
    Vk   - value 2        - `val2`  
    Qj   - dependency 1   - `dep1`  
    Qk   - dependency 2   - `dep1`  
    A    - result         - `result`
    ```
    """
    def flush(self) -> None:
        self.busy = False
        self.op = ""
        self.rob = ""
        self.val1 = None
        self.val2 = None
        self.dep1 = ""
        self.dep2 = ""
        self.result = None

    def __init__(self) -> None:
        self.flush()

    def update(self, 
               busy:int = None,
               op:str = None,
               rob:str = None,
               val1:number = None,
               val2:number = None,
               dep1:str = None,
               dep2:str = None,
               result:number = None
               ) -> None:
        args = {'busy':busy,'op':op,'rob':rob,'val1':val1,'val2':val2,'dep1':dep1,'dep2':dep2,'result':result}
        for arg in args:
            val = args[arg]
            if val == None:
                continue
            setattr(self, arg, val)
        

class ReservationStation(CDBConsumer):
    """Reservation Station holds a list of `Entry`'s.
    \nCDB consumer.
    """
    def __init__(self, cdb: CentralDataBus, funit, len=3) -> None:
        super().__init__(cdb)
        self.entries = [Entry() for _ in range(len)]
        self.fu = funit # TODO

    def entry_is_free(self) -> bool:
        for entry in self.entries:
            if not entry.busy:
                return True
        return False
    
    def add_instruction(self, i: IssuedInstruction) -> bool:
        for entry in self.entries:
            if entry.busy == False:
                entry.update(
                    busy=True,
                    op = i.op,
                    rob=i.assigned_dest,
                    val1=i.val_left,
                    val2=i.val_right,
                    dep1=i.dep_left,
                    dep2=i.dep_right)
                
                self.wait_for_variable(i.assigned_dest)
                return True
        return False
    
    def read_cdb(self):
        pass # TODO

    def try_execute(self):
        pass # TODO
    
