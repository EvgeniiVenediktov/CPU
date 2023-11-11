# CDB Consumer super-class
from cdb import CentralDataBus, NameAndValue

class CDBConsumer():
    """
        CDB Consumer is a superclass.
        It's heirs are able to listen to CDB (Central Data Bus) 
        and check for the variables values they await at the moment.

    """
    def __init__(self, cdb: CentralDataBus) -> None:
        self.cdb = cdb
        self.variables_to_get = []
    
    def wait_for_variable(self, var_name) -> None:
        if var_name not in self.variables_to_get:
            self.variables_to_get.append(var_name)
    
    def fetch_from_cdb(self) -> list[NameAndValue]:
        contents = self.cdb.read()
        results = []
        for elem in contents:
            name, _ = elem.unpack()
            if name in self.variables_to_get:
                results.append(elem)

        return results
    





