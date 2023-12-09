import unittest
from registers import RegistersAliasTable, ArchitectedRegisterFile
from utils import IssuedInstruction

class TestRegs(unittest.TestCase):
    def test_snapshot_works(self):
        # Arrange
        l = 5
        arf = ArchitectedRegisterFile(length_f=l, length_r=l)
        rat = RegistersAliasTable(arf, length_f=l, length_r=l)

        # Create snapshoot of a clean RAT
        instr_id = 111  
        cyc = 150
        rat.create_snapshot(instr_id, cyc)
        orig_data = rat.entries

        
        # Introduce changes
        i = IssuedInstruction()
        i.assigned_dest = "ROB1"
        i.original_dest = "R1"
        rat.reserve_alias(i)
        i.assigned_dest = "ROB3"
        i.original_dest = "R3"
        rat.reserve_alias(i)
        
        # Make shure entries were renamed
        self.assertFalse(rat.does_entry_match_name("R1", "R1"))
        self.assertFalse(rat.does_entry_match_name("R3", "R3"))

        # Action
        rat.recover_from_snapshot(instr_id, cyc+5)

        # Assert
        for reg_name in orig_data:
            expected_data = orig_data[reg_name]
            actual_data = rat.entries[reg_name]
            self.assertEqual(expected_data, actual_data)


if __name__ == '__main__':
    unittest.main()
