from queue import Queue

class Instruction():
    def __init__(self, optype, operands) -> None:
        self.inst_type = optype
        self.operands_type = operands
    #TYPE OF INSTRUCTION AND OPERANDS 2 methods


class Decoder:
    count = 0
    def __init__(self,filename):
        self.filename = filename
        self.instructions = []
        self.arguments = []

    def run(self):
        with open (self.filename, "r") as f:
            for line in f:
                instruction,argument = line.split()
                arguments = argument.split(',')
                self.instructions.append(instruction)
                self.arguments.append(arguments)
                for i in range(len(arguments)):
                    if arguments[i].find('R') == -1:
                        arguments[i] = int(arguments[i])
        f.close()
                
    def issue(self):              
        Decoder.count = Decoder.count + 1 
        with open (self.filename, "r") as file:
            if len(file.readlines()) >= Decoder.count:
                file.close()
                Instruction
                #return(self.instructions[Decoder.count-1], self.arguments[Decoder.count-1])
            
class InstBuff:
    i = 0
    def __init__(self,filename):
        self.mem = Queue(100)
        self.dex = Decoder(filename)
        self.dex.run()

    def refill(self):
        self.mem.put(self.dex.issue())

    def pull(self):
        return(self.mem.get())
    
#deck = Decoder('TestFile.txt')
#deck.run()
lex = InstBuff('TestFile.txt')
lex.refill()
lex.refill()
lex.refill()
lex.refill()
print(lex.pull())
print(lex.pull())