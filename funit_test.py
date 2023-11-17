import unittest
from cdb import CentralDataBus
from funit import FunctionalUnit, MemoryLoadFunctionalUnit
from funit import TYPE_INT_ADDER, TYPE_DEC_ADDER, TYPE_DEC_MULTP, TYPE_MEMORY_LOAD
from memory import Memory

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
        expected_latency = 20
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
        mem = Memory("", 10)

        id = 1
        rob = "ROB1"
        op = "LD"
        v1 = 2
        expected_value = float(6)
        mem.store(v1, expected_value)
        v2 = None

        expected_id = id
        expected_latency = 4
        actual_id = None
        clock = 0
        fu = MemoryLoadFunctionalUnit(TYPE_MEMORY_LOAD, cdb, mem)
        
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


if __name__ == "__main__":
    unittest.main()