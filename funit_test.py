import unittest
from cdb import CentralDataBus
from funit import FunctionalUnit, MemoryLoadFunctionalUnit, AddressResolver, LATENCIES
from utils import TYPE_INT_ADDER,TYPE_DEC_ADDER,TYPE_DEC_MULTP,TYPE_MEMORY_LOAD,TYPE_MEMORY_STORE,TYPE_MEMORY_FORWARDING, number
from memory import Memory
from decoder import Instruction as DecodedInstruction

class MockEntry():
    def __init__(self, id, v1, v2, offset) -> None:
        self.id = id
        self.val1 = v1
        self.val2 = v2
        self.offset = offset
        self.busy = True
        
class MockSDBuffer():
    def __init__(self) -> None:
        self.entries = []
        pass
    def add_sd_request(self, id:int, dest:int, value:number, offset:int) -> None:
        self.entries.append(MockEntry(id, value, dest, offset))


class TestFUs(unittest.TestCase):
    def test_finishAdddInCorrectTime(self):
        # Arrange
        cdb = CentralDataBus()

        id = 1
        rob = "ROB1"
        op = "Add.d"
        v1 = 2.3
        v2 = 3.3

        expected_id = id
        expected_value = float(5.6)
        expected_latency = 3

        actual_id = None

        clock = 0
        fu = FunctionalUnit(TYPE_DEC_ADDER, cdb)
        
        # Action
        started = fu.execute(id, rob, op, v1, v2)
        #clock+=1

        # Assert
        self.assertTrue(started)
        while actual_id == None:
            actual_id = fu.produce_result()
            clock+=1
        self.assertEqual(expected_latency, clock)
        self.assertEqual(expected_id, actual_id)
        self.assertEqual(expected_value, cdb.current_value.value)
    
    def test_finishAddiInCorrectTime(self):
        # Arrange
        cdb = CentralDataBus()

        id = 1
        rob = "ROB1"
        op = "Add"
        v1 = 2
        v2 = 3

        expected_id = id
        expected_value = int(5)
        expected_latency = 1

        actual_id = None

        clock = 0
        fu = FunctionalUnit(TYPE_INT_ADDER, cdb)
        
        # Action
        started = fu.execute(id, rob, op, v1, v2)

        # Assert
        self.assertTrue(started)
        while actual_id == None:
            actual_id = fu.produce_result()
            clock+=1
        self.assertEqual(expected_latency, clock)
        self.assertEqual(expected_id, actual_id)
        self.assertEqual(expected_value, cdb.current_value.value)

    def test_finishMultInCorrectTime(self):
        # Arrange
        cdb = CentralDataBus()
        id = 1
        rob = "ROB1"
        op = "Mult.d"
        v1 = 2
        v2 = 3

        expected_id = id
        expected_value = float(6)
        expected_latency = LATENCIES[TYPE_DEC_MULTP]-1 #20
        actual_id = None
        clock = 0
        fu = FunctionalUnit(TYPE_DEC_MULTP, cdb)
        
        # Action
        started = fu.execute(id, rob, op, v1, v2)

        # Assert
        self.assertTrue(started)
        while actual_id == None:
            actual_id = fu.produce_result()
            clock+=1
        self.assertEqual(expected_latency, clock)
        self.assertEqual(expected_id, actual_id)
        self.assertEqual(expected_value, cdb.current_value.value)
    
    def test_finishLoadInCorrectTime(self):
        # Arrange
        cdb = CentralDataBus()
        mem = Memory("", 10*4)

        id = 1
        rob = "ROB1"
        op = "LD"
        v1 = 2*4
        expected_value = float(6)
        mem.store(v1//4, expected_value)
        v2 = None

        expected_id = id
        expected_latency = 4
        actual_id = None
        clock = 0
        fu = MemoryLoadFunctionalUnit(TYPE_MEMORY_LOAD, cdb, mem, MockSDBuffer())
        
        # Action
        started = fu.execute(id, rob, op, v1, v2)

        # Assert
        self.assertTrue(started)
        while actual_id == None:
            actual_id = fu.produce_result()
            clock+=1
        self.assertEqual(expected_latency, clock)
        self.assertEqual(expected_id, actual_id)
        self.assertEqual(expected_value, cdb.current_value.value)

    def test_forwarding_from_a_store(self):
        # Arrange
        cdb = CentralDataBus()
        mem = Memory("", 10*4)
        sd_buff = MockSDBuffer()

        id = 1
        rob = "ROB1"
        op = "LD"
        v1 = 2*4
        expected_value = float(6)
        #mem.store(v1//4, expected_value)
        sd_buff.add_sd_request(1, v1, expected_value, 0)
        v2 = None

        expected_id = id
        expected_latency = LATENCIES[TYPE_MEMORY_FORWARDING]
        actual_id = None
        clock = 0
        fu = MemoryLoadFunctionalUnit(TYPE_MEMORY_LOAD, cdb, mem, sd_buff)
        
        # Action
        started = fu.execute(id, rob, op, v1, v2)

        # Assert
        self.assertTrue(started)
        while actual_id == None:
            actual_id = fu.produce_result()
            clock+=1
        self.assertEqual(expected_latency, clock)
        self.assertEqual(expected_id, actual_id)
        self.assertEqual(expected_value, cdb.current_value.value)

    def test_address_resolver(self):
        # Arrange
        ar = AddressResolver()
        ins = DecodedInstruction("LD", ['R1', 'R3'], 1, 2)

        expected_latency = 1

        # Action
        id = ar.resolve_address(ins)
        for clock in range(1,10):
            instr = ar.produce_address()
            if instr != None:
                break
        # Assert
        self.assertEqual(clock, expected_latency)
        self.assertEqual(id, ins.id)
    
    def test_address_resolver_compete(self):
        # Arrange
        ar = AddressResolver()
        ins1 = DecodedInstruction("LD", ['R1', 'R3'], 1, 2)
        ins2 = DecodedInstruction("LD", ['R2', 'R4'], 2, 3)

        expected_latency = 1
        clock = []
        # Action
        id = ar.resolve_address(ins1) #0 cycle
        self.assertIsNotNone(id)
        # Assert
        self.assertIsNone(ar.resolve_address(ins2))

        instr = ar.produce_address() # 1st cycle
        self.assertIsNotNone(instr)
        ar.address_was_processed()
        self.assertIsNotNone(ar.resolve_address(ins2))

        
        

if __name__ == "__main__":
    unittest.main()