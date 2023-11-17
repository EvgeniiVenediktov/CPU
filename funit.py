# Functional units: Adders, Multipliers
from cdb import CentralDataBus, FunctionResult
from utils import number

TYPE_INT_ADDER = 'INT_ADDER'
TYPE_DEC_ADDER = 'DEC_ADDER'
TYPE_DEC_MULTP = 'DEC_MULTP'
TYPE_MEMORY = 'MEMORY'

LATENCIES = {
    TYPE_INT_ADDER: 1,
    TYPE_DEC_ADDER: 3,
    TYPE_DEC_MULTP: 20,
    TYPE_MEMORY: 4,
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

OP_FUNC_MAPPING:dict[str,function] = {
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
        self.result:FunctionResult = None
        self.ready:bool = False
        self.current_counter:int = 0

    def is_free(self) -> bool:
        return self.busy
    
    def produce_result(self) -> None:
        if not self.busy:
            return
        if self.current_counter == 0:
            self.ready == True
        if self.ready:
            self.cdb.write(self.result)#TODO
            self.busy = False
            self.ready = False
            return 
        self.current_counter -= 1

    def execute(self, id:int, rob:str, op:str, v1:number, v2:number) -> None:
        func = OP_FUNC_MAPPING[op]
        self.current_counter = self.latency
        self.buse = True
        self.ready = False
        value = func(v1, v2)

        self.result = FunctionResult(id, rob, value, op)

