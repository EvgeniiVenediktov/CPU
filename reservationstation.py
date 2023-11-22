# RS 
from cdb import CentralDataBus
from cdbconsumer import CDBConsumer
from funit import FunctionalUnit, AddressResolver
from utils import number, IssuedInstruction


INT_ADDER_RS_TYPE = "int_adder"
DEC_ADDER_RS_TYPE = "dec_adder"
DEC_MULTP_RS_TYPE = "dec_multp"
LOAD_RS_TYPE = "ld_rs_type"
STORE_RS_TYPE = "sd_rs_type"

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
        self.in_progress = False
        self.op = ""
        self.id = None
        self.rob = ""
        self.val1 = None
        self.val2 = None
        self.dep1 = ""
        self.dep2 = ""
        self.result = None
        self.offset = 0

    def __init__(self) -> None:
        self.flush()
    def __str__(self) -> str:
        return str(vars(self))

    def update(self, 
               busy:bool = None,
               in_progress:bool = None,
               op:str = None,
               id:int = None,
               rob:str = None,
               val1:number = None,
               val2:number = None,
               dep1:str = None,
               dep2:str = None,
               result:number = None,
               offset:int = None
               ) -> None:
        args = {'busy':busy,'in_progress':in_progress,'op':op,'id':id,'rob':rob,'val1':val1,'val2':val2,'dep1':dep1,'dep2':dep2,'result':result,'offset':offset}
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
        self.busy_this_cycle = []

    def __str__(self) -> str:
        return str(vars(self))

    def entry_is_free(self) -> bool:
        for entry in self.entries:
            if not entry.busy:
                return True
        return False
    
    def end_cycle(self) -> None:
        self.busy_this_cycle = []
    
    def add_instruction(self, i: IssuedInstruction) -> bool:
        for entry in self.entries:
            if entry.busy == False:
                entry.update(
                    busy=True,
                    in_progress=False,
                    id = i.id,
                    op = i.op,
                    rob=i.assigned_dest,
                    val1=i.val_left,
                    val2=i.val_right,
                    dep1=i.dep_left,
                    dep2=i.dep_right,
                    offset=i.offset)
                
                self.wait_for_variables([i.assigned_dest, i.dep_left, i.dep_right])
                return True
        return False
    
    def read_cdb(self) -> int|None: # TODO TEST
        result = self.fetch_from_cdb()
        if result == None:
            return None
        affected = []
        for i, entry in enumerate(self.entries):
            if entry.dep1 == result.rob_dest:
                entry.val1 = result.value
                entry.dep1 = None
                affected.append(i)
            if entry.dep2 == result.rob_dest:
                entry.val2 = result.value
                entry.dep2 = None
                if i not in affected:
                    affected.append(i)
            if entry.rob == result.rob_dest:
                entry.flush()
        self.busy_this_cycle = affected
        return result.id

    def try_execute(self) -> None|int:
        if not self.funit.is_free():
            return None
        
        # Choose an instruction to execute

        #self.entries = sorted(self.entries, key=lambda e: e.id)
        for i, e in enumerate(self.entries):
            if e.val1 != None and e.val2 != None and not e.in_progress and i not in self.busy_this_cycle:
                is_issued = self.funit.execute(e.id, e.rob, e.op, e.val1, e.val2)
                if is_issued:
                    e.in_progress = True
                    return e.id
        return None


class LoadBuffer(ReservationStation):
    def __init__(self, cdb: CentralDataBus, funit: FunctionalUnit, len=3) -> None:
        super().__init__(cdb, funit, len)
        self.address_resolver = AddressResolver()
    
    def try_execute(self) -> None|int:
        if not self.funit.is_free():
            return None
        
        # Choose an instruction to execute
        #self.entries = sorted(self.entries, key=lambda e: e.id)
        for i, e in enumerate(self.entries):
            if e.val1 != None and not e.in_progress and i not in self.busy_this_cycle:
                is_issued = self.funit.execute(e.id, e.rob, e.op, e.val1+e.offset, e.val2)
                if is_issued:
                    e.in_progress = True
                    return e.id
        return None


class StoreBuffer(ReservationStation):
    def __init__(self, cdb: CentralDataBus, funit: FunctionalUnit, len=3) -> None:
        super().__init__(cdb, funit, len)
        # TODO

    def show_head(self) -> Entry|None:
        if len(self.entries) == 0:
            return None
        
        def skey(e:Entry) -> int:
            if e.id == None:
                return int(99999999999999999999999)
            return e.id

        self.entries = sorted(self.entries, key=lambda e: skey(e))
        return self.entries[0]

    def try_execute(self) -> None|int:
        if not self.funit.is_free():
            return None
        if len(self.entries) == 0:
            return None
        e = self.entries[0]
        if e.val1 != None and not e.in_progress and 0 not in self.busy_this_cycle:
            is_issued = self.funit.execute(e.id, e.rob, e.op, e.val1, e.val2+e.offset)
            if is_issued:
                e.in_progress = True
                return e.id
        return None