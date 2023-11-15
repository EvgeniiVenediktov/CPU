# Load/Store Buffer
from cdb import CentralDataBus
from cdbconsumer import CDBConsumer
from queue import Queue

class LdStConfig:
    def __init__(self, load_buffer_len, store_buffer_len) -> None:
        self.load_buffer_len = load_buffer_len
        self.store_buffer_len = store_buffer_len

class _MemBuffer: 
    def __init__(self, size: int) -> None:
        self.q = Queue(size)

    def pop(self) -> tuple[str, int, int]:
        """
            Returns the oldest element, and removes it from the queue
        """
        return self.q.get()
    
    def put(self, instr) -> bool:
        """
            Puts an instruction into queue, returns True on success.
            If the queue is full, returns False
        """
        if not self.q.full:
            self.q.put(instr)
            return True
        return False
    

class LoadStoreBuffer(CDBConsumer):
    """
        Load/Store Buffer.
        Stores LD,SD instructions with their known source and destination adderesses.
    """
    def __init__(self, cdb: CentralDataBus, cfg: LdStConfig) -> None:
        super().__init__(cdb)
        self.load_buffer = _MemBuffer(cfg.load_buffer_len)
        self.store_buffer = _MemBuffer(cfg.store_buffer_len)

    def store(self, instruction) -> bool:
        """
            Puts an instruction into STORE queue, returns True on success.
            If the queue is full, returns False
        """
        return self.store_buffer.put(instruction)
    
    def load(self, instruction) -> bool:
        """
            Puts an instruction into LOAD queue, returns True on success.
            If the queue is full, returns False
        """
        return self.load_buffer.put(instruction)

