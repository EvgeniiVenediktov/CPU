# RS 
from cdb import CentralDataBus
from cdbconsumer import CDBConsumer
from reordering import IssuedInstruction
from funit import FunctionalUnit
from utils import number


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
        self.id = None
        self.rob = ""
        self.val1 = None
        self.val2 = None
        self.dep1 = ""
        self.dep2 = ""
        self.result = None

    def __init__(self) -> None:
        self.flush()
    def __str__(self) -> str:
        return str(vars(self))

    def update(self, 
               busy:int = None,
               op:str = None,
               id:int = None,
               rob:str = None,
               val1:number = None,
               val2:number = None,
               dep1:str = None,
               dep2:str = None,
               result:number = None
               ) -> None:
        args = {'busy':busy,'op':op,'id':id,'rob':rob,'val1':val1,'val2':val2,'dep1':dep1,'dep2':dep2,'result':result}
        for arg in args:
            val = args[arg]
            if val == None:
                continue
            setattr(self, arg, val)
        

class ReservationStation(CDBConsumer):
    """Reservation Station holds a list of `RS Entries`. CDB consumer.
    """
    def __init__(self, cdb: CentralDataBus, funit:FunctionalUnit, len=3) -> None:
        super().__init__(cdb)
        self.entries:list[Entry] = [Entry() for _ in range(len)]
        self.funit:FunctionalUnit = funit

    def __str__(self) -> str:
        return str(vars(self))

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
    
    def read_cdb(self) -> int|None:
        result = self.fetch_from_cdb()
        if result == None:
            return None
        for entry in self.entries:
            if entry.dep1 == result.rob_dest:
                entry.val1 = result.value
                entry.dep1 = None
            if entry.dep2 == result.rob_dest:
                entry.val2 = result.value
                entry.dep2 = None
            if entry.rob == result.rob_dest:
                entry.flush()
        return result.id

    def try_execute(self) -> None|int:
        if not self.funit.is_free():
            return None
        
        # Choose an instruction to execute

        #self.entries = sorted(self.entries, key=lambda e: e.id)
        for e in self.entries:
            if e.val1 != None and e.val2 != None:
                is_issued = self.funit.execute(e.id, e.rob, e.op, e.val1, e.val2)
                if is_issued:
                    return e.id
        return None

