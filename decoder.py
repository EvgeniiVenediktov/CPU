class Instruction:
    def __init__(self, optype:str, operands:list, id:int, offset:int) -> None:
        self.inst_type:str = optype
        self.operands:list = operands
        self.id:int = id
        self.offset:int = offset
    
    def __str__(self) -> str:
        return str(vars(self))


class Decoder:
    def __init__(self,filename):
        self.filename = filename
        self.instructions = []
        self.arguments = []
        self.instances = []

    def run(self) -> list[Instruction]:
        k = 0
        with open (self.filename, "r") as f:
            for line in f:
                instruction,argument = line.split()
                arguments = argument.split(',')
                offset = 0
                if instruction == "LD" or instruction == "SD":
                    for i, arg in enumerate(arguments):
                        lp = arg.find('(')
                        if lp == -1:
                            continue
                        rp = arg.find(')')
                        offset = int(arg[lp+1:rp])
                        arguments[i] = arg[:lp] + arg[rp+1:]
                        pass

                for i in range(len(arguments)):
                    if arguments[i].find('R') == -1:
                        arguments[i] = int(arguments[i])
                ins = Instruction(instruction, arguments, k, offset)
                self.instances.append(ins)
                k = k + 1
        f.close()
        return(self.instances)

class InstBuff:
    def __init__(self,filename):
        self.buffer = []
        self.filename = filename
        self.index = 0
        self.prev_index = 0

    def refill(self):
        deck = Decoder(self.filename)
        self.buffer = deck.run()
        
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

if __name__ == "__main__":
    lex = InstBuff('TestFile.txt')
    lex.refill()
    print(lex.issue())
    print(lex.issue())
    print(lex.issue())
    print(lex.issue())
    print(lex.issue())
    print(lex.issue())