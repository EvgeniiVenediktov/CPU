class Instruction:
    def __init__(self, optype, operands, id) -> None:
        self.inst_type = optype
        self.operands = operands
        self.id = id
    
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
                for i in range(len(arguments)):
                    if arguments[i].find('R') == -1:
                        arguments[i] = int(arguments[i])
                ins = Instruction(instruction, arguments, k)
                self.instances.append(ins)
                k = k + 1
        f.close()
        return(self.instances)

class InstBuff:
    def __init__(self,filename):
        self.buffer = []
        self.filename = filename
        self.index = 0

    def refill(self):
        deck = Decoder(self.filename)
        self.buffer = deck.run()
        
    def issue(self, i=None) -> Instruction:
        if self.index >= len(self.buffer) :
            return None

        if i == None:
            v = self.buffer[self.index]
            self.index += 1
            return(v)
        
        if len(self.buffer) >= i:
            return(self.buffer[i])

if __name__ == "__main__":
    lex = InstBuff('TestFile.txt')
    lex.refill()
    print(lex.issue())
    print(lex.issue())
    print(lex.issue())
    print(lex.issue())
    print(lex.issue())
    print(lex.issue())