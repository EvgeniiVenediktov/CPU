class Instruction:
    def __init__(self, optype:str, operands:list, id:int, offset:int=0) -> None:
        self.inst_type:str = optype
        self.operands:list = operands
        self.id:int = id
        self.offset:int = offset

        self.original_dest = None # Only to be used for LD instructions
    
    def __str__(self) -> str:
        return str(vars(self))


class Decoder:
    def __init__(self,filename):
        self.filename = filename
        self.instructions = []
        self.arguments = []
        self.instances = []
        self.original_raw_instructions:list[str] = []

    def split_by_space_in_two(self, l:str) -> tuple[str, str]:
        sr = l.split()
        if len(sr) == 1:
            return sr[0], ","
        return sr[0], sr[1]

    def run(self) -> list[Instruction]:
        k = 0
        with open (self.filename, "r") as f:
            for i, line in enumerate(f):
                #instruction,argument = line.split()
                self.original_raw_instructions.append(line) # for output
                instruction, argument = self.split_by_space_in_two(line)
                arguments = argument.split(',')
                offset = 0
                if instruction == "LD" or instruction == "SD":
                    for i, arg in enumerate(arguments):
                        if i == 0:
                            continue
                        lp = arg.find('(')
                        if lp == -1:
                            raise Exception(f"Wrong syntax for instruction #{i}: Couldn't find '('. {line}")
                        rp = arg.find(')')
                        offset = int(arg[:lp])
                        arguments[i] = arg[lp+1:rp]
                        pass

                for i in range(len(arguments)):
                    if arguments[i]=='':
                        continue
                    if arguments[i].find('R') == -1 and arguments[i].find('F') == -1:
                        arguments[i] = float(arguments[i])

                ins = Instruction(instruction, arguments, k, offset)
                self.instances.append(ins)
                k = k + 1
        f.close()
        return(self.instances)

    def get_original_lines(self) -> list[str]:
        return self.original_raw_instructions

class InstBuff:
    def __init__(self,filename):
        self.buffer = []
        self.filename = filename
        self.index = 0
        self.prev_index = 0
        self.decoder = None

    def refill(self):
        deck = Decoder(self.filename)
        self.buffer = deck.run()
        self.decoder = deck
        
    def issue(self, i=None) -> Instruction:
        if self.index >= len(self.buffer):
            return None

        if i == None:
            v = self.buffer[self.index]
            self.prev_index = self.index
            self.index += 1
            return(v)
        
        if len(self.buffer) >= i:
            self.prev_index = self.index
            self.index = i
            return(self.buffer[i])
        
    def return_to_prev_index(self) -> None:
        self.index = self.prev_index

    def get_original_lines(self) -> list[str]:
        return self.decoder.get_original_lines()

if __name__ == "__main__":
    lex = InstBuff('TestFile.txt')
    lex.refill()
    print(lex.issue())
    print(lex.issue())
    print(lex.issue())
    print(lex.issue())
    print(lex.issue())
    print(lex.issue())