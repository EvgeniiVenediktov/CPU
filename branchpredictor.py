class BTBEntry:
    def __init__(self) -> None:
        self.direction_flag = False
        self.target_address = '000'

class BranchPredictor:
    """Branch Target Buffer, 1 bit history predictor"""
    def __init__(self, btb_len:int=4) -> None:
        self.entries = [BTBEntry() for _ in range(btb_len)]

    """Entries are indexed from 0 to 4 by bits #3,2 of the instruction"""
    def predict_address(self, instr_id:int) -> tuple[int, bool]: # addr, take/not_take
        """`instr_id` - word address, inside it will be transformed into bin (*4)"""
        # Get index of corresponding entry
        #index = instr_id//4
        index = instr_id%4

        e = self.entries[index]
        if not e.direction_flag:
            return instr_id+1, False
        
        b_pc = bin(instr_id*4)
        b_pc = [*b_pc]
        while len(b_pc)<34:
            b_pc.insert(2, '0')
        b_pc[-5:-2] = e.target_address

        s = ''
        s = s.join(b_pc)

        address = int(s[:-2], 2)
        return address, True
    
    def update_entry(self, instr_id:int, true_target:int) -> None:
        """To be called only if a branch was resolved to be taken"""
        # Get index of corresponding entry
        #index = instr_id//4
        index = instr_id%4

        b_pc = bin(true_target*4)
        b_pc = [*b_pc]
        while len(b_pc)<34:
            b_pc.insert(2, '0')
        
        s = ''
        s = s.join(b_pc[-5:-2])

        self.entries[index].direction_flag = True
        self.entries[index].target_address = s

