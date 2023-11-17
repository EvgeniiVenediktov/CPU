from cdb import CentralDataBus
from cdbconsumer import CDBConsumer
from cpu import number
from registers import RegistersAliasTable
from decoder import Instruction as DecodedInstruction

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
    
    def __str__(self) -> str:
        return str(vars(self))
    

class Entry:
    def __init__(self, name:str) -> None:
        self.entry_name:str = name
        self.busy:bool = False
        self.id:int = 0
        self.type:str = ""
        self.dest:str = ""
        self.value:number = None
        self.is_ready:bool = False
        pass # TODO


class ReorderBuffer(CDBConsumer):
    def __init__(self, cdb: CentralDataBus, rat:RegistersAliasTable, len=10) -> None:
        super().__init__(cdb)
        self.entries = [Entry(f'ROB{i}') for i in range(len)]
        self.head = 0
        self.rat = rat
        # TODO
    
    def entry_is_free(self) -> bool:
        for entry in self.entries:
            if not entry.busy:
                return True
        return False
    
    def add_instruction(self, instr:DecodedInstruction) -> IssuedInstruction:
        """fetch available values, reserve an Alias, create a ROB entry"""
        def __process(entry:Entry, instr:DecodedInstruction) -> IssuedInstruction:
            if entry.busy:
                return None
            orig_dest = instr.operands[0]
            entry.busy = True
            entry.type = instr.inst_type
            entry.dest = orig_dest
            entry.id = instr.id

            self.wait_for_variable(entry.entry_name)

            vals = [None, None]
            deps = [None, None]

            for i in range(1,len(instr.operands)): # start from 1 bc [0] - destination
                op = instr.operands[i]
                if isinstance(op, str):
                    deps[i] = op
                else:
                    vals[i] = op

            for dep in deps:
                if dep == None:
                    continue
                if self.rat.does_entry_match_name(dep, dep):
                    dep = self.rat.get_reg_value(dep)
                else:
                    dep = self.rat.get_alias_for_reg(dep)

            issi = IssuedInstruction()
            issi.id = instr.id
            issi.op = instr.inst_type
            issi.original_dest = orig_dest
            issi.assigned_dest = entry.entry_name
            issi.val_left = vals[0]
            issi.val_right = vals[1] 
            issi.dep_left = deps[0]
            issi.dep_right = deps[1]

            self.rat.reserve_alias(issi)

            entry.busy = True
            entry.dest = orig_dest
            entry.type = instr.inst_type

            return issi

        # start looking from the head down
        for i in range(self.head, len(self.entries)):
            entry = self.entries[i]
            res = __process(entry, instr)
            if res != None:
                return res
        # continue looking from 0 to head
        for i in range(0, self.head):
            entry = self.entries[i]
            res = __process(entry, instr)
            if res != None:
                return res
        return None
    
    def read_cdb(self) -> int|None:
        result = self.fetch_from_cdb()
        if result == None:
            return None
        for entry in self.entries:
            if entry.entry_name == result.rob_dest:
                entry.is_ready = True
                entry.value = result.value
                return entry.id
        return None
            
    def commit(self) -> int|None:
        """ Returns committed id or None
        1. Write value to ARF
        2. Check if RAT has the entry name:
            YES: free the RAT entry
            NO: do nothing          """        
        entry = self.entries[self.head]
        if entry.is_ready:
            entry.busy = False
            self.rat.set_reg_value(entry.dest, entry.value)
            if self.rat.does_entry_match_name(entry.dest, entry.entry_name):
                self.rat.free_alias(entry.dest)
            return entry.id
        return None
        