# Registers package: Registers Alias Table and Architected Register File
from utils import number, IssuedInstruction

def parse_register_init_values(fname:str) -> dict:
    r = {}
    with open(fname) as f:
        lines = f.readlines()
        for line in lines:
            line = line.removesuffix("\n")
            tokens = line.split(',')
            addr = tokens[0]
            value = 0
            if tokens[1].find('.') != -1:
                value = float(tokens[1])
            else: 
                value = int(tokens[1])
            r[addr] = value
        f.close()
    return r

class ArchitectedRegisterFile:
    def __init__(self, initial_values={}, length_r=32, length_f=32) -> None:
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
        for name in initial_values:
            if name in self.rnames or name in self.fnames:
                self.entries[name] = initial_values[name]
    
    def get_value(self, name:str) -> number:
        return self.entries[name]
    
    def set_value(self, name:str, val:number) -> None:
        if name == "R0": # Hardwire R0 to zero
            val = 0
        self.entries[name] = val
    
    def __str__(self) -> str:
        s  = "┌──────┬───────┐\n"
        s += "|-name-|-value-|\n"
        s += "├──────┴───────┤\n"
        for n in self.rnames:
            if self.entries[n]!=0:
                s += "|{:^6}|{:^7}|\n".format(n,self.entries[n])
        for n in self.fnames:
            if self.entries[n]!=0:
                s += "|{:^6}|{:^7}|\n".format(n,self.entries[n])
        s += "└──────┴───────┘"
        return s
    

class Entry:
    def __init__(self, name, default_value) -> None:
        self.name = name
        self.value = default_value
        self.default_value = default_value

    def reset_value(self) -> None:
        self.value = self.default_value
    def __str__(self) -> str:
        return str("|{:^6}|{:^7}|".format(self.name,self.value))

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
        s  = "┌──────┬───────┐\n"
        s += "|-name-|-value-|\n"
        s += "├──────┴───────┤\n"
        for en in self.entries:
            entry = self.entries[en]
            s+=str(entry)+"\n"
        s += "└──────┴───────┘"
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