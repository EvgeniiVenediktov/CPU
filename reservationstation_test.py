import unittest
from reservationstation import Entry, ReservationStation, LoadBuffer
from cdb import CentralDataBus
from funit import FunctionalUnit, MemoryLoadFunctionalUnit
from utils import TYPE_INT_ADDER,TYPE_DEC_ADDER,TYPE_DEC_MULTP,TYPE_MEMORY_LOAD,TYPE_MEMORY_STORE
from utils import IssuedInstruction
from memory import Memory

class TestRS(unittest.TestCase):

    def setUp(self) -> None:        
        # ADDD ready instr
        self.addd_instr = IssuedInstruction()
        self.addd_instr.id = 1
        self.addd_instr.op = 'Add.d'
        self.addd_instr.val_left = 3.0
        self.addd_instr.val_right = 3.0
        self.addd_instr.assigned_dest = 'ROB1'
        self.addd_instr_expected_value = 6.0
        # SUBD ready instr
        self.subd_instr = IssuedInstruction()
        self.subd_instr.id = 2
        self.subd_instr.op = 'Sub.d'
        self.subd_instr.val_left = 3.0
        self.subd_instr.val_right = 3.0
        self.subd_instr.assigned_dest = 'ROB2'
        self.subd_instr_expected_value = 0.0
        # MEM VALUES
        self.mem_addr_1 = 3
        self.mem_addr_2 = 4
        self.mem_addr_1_val = 10
        self.mem_addr_2_val = 12
        # LD1 ready instr
        self.ld1_instr = IssuedInstruction()
        self.ld1_instr.id = 3
        self.ld1_instr.op = 'LD'
        self.ld1_instr.val_left = self.mem_addr_1
        self.ld1_instr.assigned_dest = 'ROB3'
        self.ld1_instr.offset = 3
        self.ld1_instr_expected_value = self.mem_addr_1_val
        # LD2 ready instr
        self.ld2_instr = IssuedInstruction()
        self.ld2_instr.id = 4
        self.ld2_instr.op = 'LD'
        self.ld2_instr.val_left = self.mem_addr_2
        self.ld2_instr.assigned_dest = 'ROB4'
        self.ld2_instr.offset = 3
        self.ld2_instr_expected_value = self.mem_addr_2_val

   
    def test_entry_update(self):
        # Arrange
        e_int = Entry()
        e_float = Entry()
        attrs_int = {'busy':True,'in_progress':False,'op':"addi",'id':1, 'rob':"F1", 'val1':int(2),'val2':int(3), 'dep1':"",'dep2':"",'result':None,'offset':0}
        attrs_float = {'busy':True,'in_progress':False,'op':"addd",'id':2, 'rob':"F2", 'val1':float(2),'val2':float(3), 'dep1':"",'dep2':"",'result':None,'offset':0}
        # Action
        e_int.update(busy=True,op="addi",rob="F1",id=1,val1=2,val2=3)
        e_float.update(busy=True,op="addd",rob="F2",id=2,val1=2.0,val2=3.0)
        # Assert
        d = vars(e_int)
        for field in d:
            val = d[field]
            self.assertEqual(val, attrs_int[field], field)

        d = vars(e_float)
        for field in d:
            val = d[field]
            self.assertEqual(val, attrs_float[field], field)

    def test_execute_arithmetic(self):
        # Arrange
        cdb = CentralDataBus()
        fu = FunctionalUnit(TYPE_DEC_ADDER, cdb)
        rs = ReservationStation(cdb, fu)

        rs.add_instruction(self.addd_instr)
        rs.add_instruction(self.subd_instr)

        expected_time_before_exec_next = 3
        expected_next_exec_id = self.subd_instr.id
        # Action 
        exec_id = rs.try_execute()
        
        # Assert
        self.assertEqual(exec_id, self.addd_instr.id)
        clock = 0
        next_exec_id = None
        produced_id = None
        while next_exec_id == None and produced_id == None:
            rs.read_cdb()
            produced_id = fu.produce_result()
            next_exec_id = rs.try_execute()
            clock+=1
        self.assertIsNotNone(produced_id)
        self.assertIsNotNone(next_exec_id)
        self.assertEqual(clock, expected_time_before_exec_next)
        self.assertEqual(next_exec_id, expected_next_exec_id)
    
    def test_execute_loads(self):
        # Arrange
        cdb = CentralDataBus()
        mem = Memory('', 10)
        mem.store(self.mem_addr_1, self.mem_addr_1_val)
        mem.store(self.mem_addr_2, self.mem_addr_2_val)
        fu = MemoryLoadFunctionalUnit(TYPE_MEMORY_LOAD, cdb, mem)
        rs = LoadBuffer(cdb, fu)

        rs.add_instruction(self.ld1_instr)
        rs.add_instruction(self.ld2_instr)

        expected_time_before_exec_next = 4
        expected_next_exec_id = self.ld2_instr.id
        # Action 
        exec_id = rs.try_execute()
        
        # Assert
        self.assertEqual(exec_id, self.ld1_instr.id)
        clock = 0
        next_exec_id = None
        produced_id = None
        while next_exec_id == None and produced_id == None:
            rs.read_cdb()
            produced_id = fu.produce_result()
            next_exec_id = rs.try_execute()
            clock+=1
        self.assertIsNotNone(produced_id)
        self.assertIsNotNone(next_exec_id)
        self.assertEqual(clock, expected_time_before_exec_next)
        self.assertEqual(next_exec_id, expected_next_exec_id)

if __name__ == '__main__':
    unittest.main()
