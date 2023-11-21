import unittest
import os
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
        ins = Instruction(optype="MULT", operands=['R1', 'R3', 'R5'], id=2)
        self.assertEqual(str(ins),"{'inst_type': 'MULT', 'operands': ['R1', 'R3', 'R5'], 'id': 2, 'offset': 0}")


class testDecoder(unittest.TestCase):
    def setUp(self):
        self.offset_filename = "TestFile.txt"
        self.eof_fname = "test_eof.txt"
        with open(self.eof_fname, "w") as f:
            f.write("EOF")

    def tearDown(self) -> None:
        if os.path.exists(self.eof_fname):
            os.remove(self.eof_fname)

    def test_offset(self):
        # Arrange
        decoder = Decoder(filename=self.offset_filename)

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
    
    def test_eof(self):
        # Arrange
        decoder = Decoder(self.eof_fname)

        expected_type = "EOF"
        expected_ops = ['', '']
        expected_offset = 0

        # Action
        instrs = decoder.run()
        instr = instrs[0]

        # Assert
        self.assertEqual(len(instrs), 1)
        self.assertEqual(expected_type, instr.inst_type)
        self.assertEqual(expected_ops, instr.operands)
        self.assertEqual(expected_offset, instr.offset)


if __name__ == '__main__':
    unittest.main()