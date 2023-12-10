import unittest
from branchpredictor import BranchPredictor

class TestBTB(unittest.TestCase):
    def test_not_take(self):
        # Arrange
        bp = BranchPredictor()
        instr_id = 6 #11000 in bin after *4
        expected_dir = False
        expected_addr = 7 #11100

        # Action
        addr, dir = bp.predict_address(instr_id)

        # Assert
        self.assertEqual(expected_addr, addr)
        self.assertEqual(expected_dir, dir)
    
    def test_take(self):
        # Arrange
        bp = BranchPredictor()
        instr_id = 3      #001000 in bin after *4
        expected_addr = 7 #011100
        expected_dir = True

        bp.update_entry(instr_id, 7) # entry will have target addr == '111'
        self.assertEqual(bp.entries[instr_id%4].target_address, '111')
        # Action
        addr, dir = bp.predict_address(instr_id)

        # Assert
        self.assertEqual(expected_addr, addr)
        self.assertEqual(expected_dir, dir)

    def test_take_negative_offset(self):
        # Arrange
        bp = BranchPredictor()
        instr_id = 7      #011100
        expected_addr = 2 #001000 in bin after *4
        expected_dir = True

        bp.update_entry(instr_id, 2) # entry will have target addr == '010'
        self.assertEqual(bp.entries[instr_id%4].target_address, '010')
        # Action
        addr, dir = bp.predict_address(instr_id)

        # Assert
        self.assertEqual(expected_addr, addr)
        self.assertEqual(expected_dir, dir)



if __name__ == "__main__":
    unittest.main()