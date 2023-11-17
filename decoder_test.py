import unittest
from decoder import Instruction
from decoder import Decoder
from decoder import InstBuff

class testInstruction(unittest.TestCase):
    def testInstructionConstructor(self):
        ins = Instruction(optype="SUB", operands=['R1', 'R2', 'R3'], id=0)
        self.assertEqual(ins.inst_type, "SUB")
        self.assertEqual(ins.operands, ['R1', 'R2', 'R3'])
        self.assertEqual(ins.id, 0)
        
    def teststr(self):
        ins = Instruction(optype="MULTI", operands=['R1', 'R3', 'R5'], id=2)
        self.assertEqual(str(ins),"{'inst_type': 'MULTI', 'operands': ['R1', 'R3', 'R5'], 'id': 2}")

class testDecoder:
    def setUp(self):
        self.filename = "TestFile.txt"

    def testDecoderConstructor(self):
        deck = Decoder(filename=self.filename)
        
#class testInstBuff:

if __name__ == '__main__':
    unittest.main()