class Instruction:
    def __init__(self, optype, operands, num) -> None:
        self.inst_type = optype
        self.operands = operands
        self.number = num
    
    def __str__(self) -> str:
        return str(vars(self))


class Decoder:
    def __init__(self,filename):
        self.filename = filename
        self.instructions = []
        self.arguments = []
        self.instances = []

    def run(self):
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
        self.mem = []
        self.filename = filename
        self.index = 0

    def refill(self):
        deck = Decoder(self.filename)
        self.mem = deck.run()
        
    def issue(self, i=None):
        if self.index >= len(self.mem) :
            return None

        if i == None:
            v = self.mem[self.index]
            self.index += 1
            return(v)
        
        if len(self.mem) >= i:
            return(self.mem[i])

    
lex = InstBuff('TestFile.txt')
lex.refill()
print(lex.issue())
print(lex.issue())
print(lex.issue())
print(lex.issue())
print(lex.issue())
print(lex.issue())