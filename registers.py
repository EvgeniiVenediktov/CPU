# Registers package: Registers Alias Table and Architected Register File
from reordering import IssuedInstruction
from cpu import number


class ArchitectedRegisterFile:
    def __init__(self, length=7) -> None:
        self.entries:dict[str, number] = {}
        for i in range(length):
            name = f'R{i}'
            self.entries[name] = 0
    
    def get_value(self, name:str) -> number:
        return self.entries[name]
    
    def set_value(self, name:str, val:number) -> None:
        self.entries[name] = val
    
    def __str__(self) -> str:
        return str(self.entries)
    

class Entry:
    def __init__(self, name, default_value) -> None:
        self.name = name
        self.default_value = default_value
        self.value = default_value

    def reset_value(self) -> None:
        self.value = self.default_value


class RegistersAliasTable:
    def __init__(self, arf:ArchitectedRegisterFile, length=7) -> None:
        self.arf = arf
        self.entries:dict[str, Entry] = {}
        for i in range(length):
            name = f'R{i}'
            self.entries[name] = Entry(name=name, default_value=name) 
    
    def does_entry_match_name(self, orig_name:str, assigned_name:str) -> bool:
        if self.entries[orig_name].name == assigned_name:
            return True
        return False

    def reserve_alias(self, instr:IssuedInstruction) -> None:
        self.entries[instr.original_dest] = instr.assigned_dest
    
    def free_alias(self, orig_name:str) -> None:
        self.entries[orig_name].reset_value()
    
    def get_reg_value(self, name:str) -> number:
        return self.arf.get_value(name)
    
    def set_reg_value(self, name:str, value:number) -> None:
        self.arf.set_value(name, value)
