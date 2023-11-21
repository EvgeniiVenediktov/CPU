import unittest
from decoder import Instruction
from decoder import Decoder
from decoder import InstBuff

class testInstruction(unittest.TestCase):
    def test_InstructionConstructor(self):
        ins = Instruction(optype="SUB", operands=['R1', 'R2', 'R3'], id=0)
        self.assertEqual(ins.inst_type, "SUB")
        self.assertEqual(ins.operands, ['R1', 'R2', 'R3'])
        self.assertEqual(ins.id, 0)
        
    def test_str(self):
        ins = Instruction(optype="MULTI", operands=['R1', 'R3', 'R5'], id=2)
        self.assertEqual(str(ins),"{'inst_type': 'MULTI', 'operands': ['R1', 'R3', 'R5'], 'id': 2, 'offset': 0}")


class testDecoder(unittest.TestCase):
    def setUp(self):
        self.filename = "TestFile.txt"

    def test_offset(self):
        # Arrange
        decoder = Decoder(filename=self.filename)

        expected_offset = int(2)
        expected_instr_type = "LD"
        expected_args = ["R7","R2"]

        # Action
        instrs = decoder.run()
        instr = instrs[0]

        # Assert
        self.assertEqual(expected_offset, instr.offset)
        self.assertEqual(expected_instr_type, instr.inst_type)
        self.assertEqual(expected_args, instr.operands)

if __name__ == '__main__':
    unittest.main()