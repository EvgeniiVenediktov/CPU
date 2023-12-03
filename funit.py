# Functional units: Adders, Multipliers
from cdb import CentralDataBus, FunctionResult
from memory import Memory as HardMemory
from utils import number, IssuedInstruction
from decoder import Instruction as DecodedInstruction
#from reservationstation import StoreBuffer
from utils import TYPE_INT_ADDER,TYPE_DEC_ADDER,TYPE_DEC_MULTP,TYPE_MEMORY_LOAD,TYPE_MEMORY_STORE,TYPE_MEMORY_FORWARDING

# Project description values
"""LATENCIES = {
    TYPE_INT_ADDER: 1,
    TYPE_DEC_ADDER: 3,
    TYPE_DEC_MULTP: 20,
    TYPE_MEMORY_LOAD: 4,
    TYPE_MEMORY_STORE: 4,
}"""
# Demo values
LATENCIES = {
    TYPE_INT_ADDER: 1,
    TYPE_DEC_ADDER: 4,
    TYPE_DEC_MULTP: 15,
    TYPE_MEMORY_LOAD: 5,
    TYPE_MEMORY_STORE: 5,
    TYPE_MEMORY_FORWARDING: 1,
}

def subi(v1, v2):
    return int(v1-v2)
def addi(v1, v2):
    return int(v1+v2)
def subd(v1, v2):
    return float(v1-v2)
def addd(v1, v2):
    return float(v1+v2)
def mul(v1, v2):
    return float(v1*v2)

OP_FUNC_MAPPING:dict[str] = {
    "Add":addi,
    "Addi":addi,
    "Add.d":addd,
    "Sub":subi,
    "Sub.d":subd,
    "Mult.d":mul,
}

class FunctionalUnit:
    def __init__(self, unit_type:str, cdb:CentralDataBus) -> None:
        self.cdb:CentralDataBus = cdb
        self.unit_type:str = unit_type
        self.latency:int = LATENCIES[unit_type]
        self.busy:bool = False

        self.func:function = None
        self.id:int = None
        self.rob:str = None
        self.v1:number = None
        self.v2:number = None
        self.op:str = None

        self.ready:bool = False
        self.current_counter:int = 0

        self.used_at_this_cycle = False

    def is_free(self) -> bool:
        return not self.busy and not self.used_at_this_cycle
    
    def produce_result(self) -> None|int:
        if not self.busy:
            return None
        self.current_counter -= 1
        if self.current_counter <= 0:
            self.ready = True
        if self.ready:
            val = self.func(self.v1, self.v2)
            result = FunctionResult(self.id, self.rob, val, self.op, self.unit_type)
            self.cdb.write(result)
            self.busy = False
            self.ready = False

            self.func = None
            self.id = None
            self.rob = None
            self.v1 = None
            self.v2 = None
            self.op = None

            self.used_at_this_cycle = True

            return result.id

        return None

    def execute(self, id:int, rob:str, op:str, v1:number, v2:number) -> tuple[bool, bool]:
        is_the_result_ready = False
        if self.busy or self.used_at_this_cycle:
            return False, is_the_result_ready
        
        if op not in OP_FUNC_MAPPING:
            raise Exception("Not supported instruction:", op, "FuncUnit:",self.unit_type)
        func = OP_FUNC_MAPPING[op]

        self.current_counter = self.latency-1
        self.busy = True
        self.ready = False

        self.id = id
        self.rob = rob
        self.v1 = v1
        self.v2 = v2
        self.op = op
        self.func = func

        if self.current_counter == 0:
            is_the_result_ready = True

        return True, is_the_result_ready
    
    def release_at_the_end_of_cycle(self):
        self.used_at_this_cycle = False


class MemoryLoadFunctionalUnit(FunctionalUnit):
    def __init__(self, unit_type: str, cdb: CentralDataBus, mem:HardMemory, sd_buffer) -> None:
        super().__init__(unit_type, cdb)
        self.mem = mem
        self.sd_buffer = sd_buffer

    def execute(self, id: int, rob: str, op: str, v1: number, v2: number) -> bool:
        if self.busy or self.used_at_this_cycle:
            return False
        if op not in OP_FUNC_MAPPING and op != "LD":
            raise Exception("Not supported instruction:", op, "FuncUnit:",self.unit_type)
        
        def wrap_load(v1, v2):
            return self.mem.load(int(v1//4))
        func = wrap_load
        self.current_counter = self.latency-1
        
        ### Store forwarding ###
        # Check SD queue for a matching entry:
        forwarded_result = None
        for se in self.sd_buffer.entries:
            if not se.busy:
                continue
            if se.id <= id and se.val2+se.offset == v1:
                forwarded_result = se.val1
                def wrap_forwarding_from_a_store(v1, v2):
                    return forwarded_result
                func = wrap_forwarding_from_a_store
                self.current_counter = LATENCIES[TYPE_MEMORY_FORWARDING]-1
                break

        self.busy = True
        self.ready = False

        self.id = id
        self.rob = rob
        self.v1 = v1 # addr+offset
        self.v2 = v2 # None
        self.op = op
        self.func = func

        return True
    
class MemoryStoreFunctionalUnit(FunctionalUnit):
    def __init__(self, unit_type: str, cdb: CentralDataBus, mem: HardMemory) -> None:
        super().__init__(unit_type, cdb)
        self.mem = mem

    def execute(self, id: int, rob: str, op: str, v1: number, v2: number) -> bool:
        if self.busy or self.used_at_this_cycle:
            return False
        
        if op not in OP_FUNC_MAPPING and op != "SD":
            raise Exception("Not supported instruction:", op, "FuncUnit:",self.unit_type)
        
        def wrap_store(v1, v2):
            return self.mem.store(int(v2//4), v1)

        func = wrap_store
        
        self.current_counter = self.latency-1
        self.busy = True
        self.ready = False

        self.id = id
        self.rob = rob
        self.v1 = v1 # value
        self.v2 = v2 # addr+offset
        self.op = op
        self.func = func

        return True
    

class AddressResolver:
    """Handles address resolving for LD, SD"""
    def __init__(self) -> None:
        self.latency:int = 1
        self.current_clock:int = 0
        self.busy:bool = False

        self.inst:DecodedInstruction = None

    def resolve_address(self, insrt:DecodedInstruction) -> None|int:
        if self.busy:
            return None
        # Check for dependency in address: # TODO wrong
        """if str(insrt.operands[1]).find('R') != -1:
            return None"""
        self.current_clock = self.latency -1
        self.busy = True
        self.inst = insrt
        return insrt.id
    
    def produce_address(self) -> None|DecodedInstruction:
        """Will return the same thing until called `address_was_processed`"""
        if self.busy and self.current_clock == 0:
            return self.inst
        self.current_clock -=1

    def address_was_processed(self) -> None:
        self.busy = False