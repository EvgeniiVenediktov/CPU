# CDB Receiver super-class
from cdb import CentralDataBus, NameAndValue

class CDBReceiver():
    """
        CDB Receiver is a superclass.
        It's heirs are able to listen to CDB (Central Data Bus) 
        and check for the variables values they await at the moment.

    """
    def __init__(self, cdb: CentralDataBus) -> None:
        self.cdb = cdb
        self.variables_to_get = []
    
    def fetch_from_cdb(self) -> list[NameAndValue]:
        contents = self.cdb.read()
        results = []
        for elem in contents:
            name, _ = elem.unpack()
            if name in self.variables_to_get:
                results.append(elem)

        return results
    





