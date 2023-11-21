# Registers package: Registers Alias Table and Architected Register File
from utils import number, IssuedInstruction


class ArchitectedRegisterFile:
    def __init__(self, length_r=32, length_f=32) -> None:
        self.length_r=length_r
        self.length_f=length_f
        
        self.entries:dict[str, number] = {}
        # R regs
        self.rnames = []
        for i in range(self.length_r):
            name = f'R{i}'
            self.rnames.append(name)
            self.entries[name] = 0
        # F regs
        self.fnames = []
        for i in range(self.length_r):
            name = f'F{i}'
            self.fnames.append(name)
            self.entries[name] = 0
    
    def get_value(self, name:str) -> number:
        return self.entries[name]
    
    def set_value(self, name:str, val:number) -> None:
        self.entries[name] = val
    
    def __str__(self) -> str:
        s = ""
        for n in self.rnames:
            s += f"{n}: {self.entries[n]} "
        s += "\n"
        for n in self.fnames:
            s += f"{n}: {self.entries[n]} "
        return s
    

class Entry:
    def __init__(self, name, default_value) -> None:
        self.name = name
        self.value = default_value
        self.default_value = default_value

    def reset_value(self) -> None:
        self.value = self.default_value
    def __str__(self) -> str:
        return str(f"name:{self.name}, value:{self.value}")

class RegistersAliasTable:
    def __init__(self, arf:ArchitectedRegisterFile, length_r=32, length_f=32) -> None:
        self.arf = arf
        self.entries:dict = {}
        for i in range(length_r):
            name = f'R{i}'
            self.entries[name] = Entry(name=name, default_value=name) 
        for i in range(length_f):
            name = f'F{i}'
            self.entries[name] = Entry(name=name, default_value=name) 
    
    def __str__(self) -> str:
        s = ""
        for en in self.entries:
            entry = self.entries[en]
            s+=str(entry)+"\n"
        return s
    
    def does_entry_match_name(self, orig_name:str, assigned_name:str) -> bool:
        if orig_name not in self.entries:
            return False
        e = self.entries[orig_name]
        if e.value == assigned_name:
            return True
        return False

    def reserve_alias(self, instr:IssuedInstruction) -> None:
        self.entries[instr.original_dest].value = instr.assigned_dest

    def get_alias_for_reg(self, reg:str) -> str:
        return self.entries[reg].value

    def free_alias(self, orig_name:str) -> None:
        self.entries[orig_name].reset_value()
    
    def get_reg_value(self, name:str) -> number:
        return self.arf.get_value(name)
    
    def set_reg_value(self, name:str, value:number) -> None:
        if name[0] == "R":
            value = int(value)
        if name[0] == "F":
            value = float(value)
        self.arf.set_value(name, value)

    def get_value_or_alias(self, name:str) -> str|number:
        if str(name).isnumeric():
            return name
        if self.does_entry_match_name(name, name):
            return self.get_reg_value(name)
        return self.get_alias_for_reg(name)