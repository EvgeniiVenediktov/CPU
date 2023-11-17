# CDB Consumer super-class
from cdb import CentralDataBus, FunctionResult

class CDBConsumer:
    """
        CDB Consumer is a superclass.
        It's heirs are able to listen to CDB (Central Data Bus) 
        and check for the variables values they await at the moment.
    """
    def __init__(self, cdb: CentralDataBus) -> None:
        self.cdb = cdb
        self.variables_to_get:list[str] = []
    
    def wait_for_variable(self, var_name:str) -> None:
        if var_name not in self.variables_to_get:
            self.variables_to_get.append(var_name)
    
    def fetch_from_cdb(self) -> FunctionResult|None:
        current_value = self.cdb.read()
        for i in range(len(self.variables_to_get)):
            vname = self.variables_to_get[i]
            if vname == current_value:
                del self.variables_to_get[i]
                return current_value
        return None
    





