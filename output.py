class Monitor():
    def __init__(self) -> None:
        self.instlist:list[MonitoredInstruction] = []

    def output(self):
        """Writes an output timetable to output.txt"""
        sorted_instrs = sorted(self.instlist, key= lambda instructions: instructions.id)
        with open('output.txt', 'w') as file:
            file.write("--Id--|--Issue--|--Exe--|--Mem--|--Wrbk--|--Commit--\n")
            for instr in sorted_instrs:
                file.write('{:^5} | {:^7} | {:^5} | {:^5} | {:^6} | {:^9}\n'.format(instr.id, instr.issue, instr.ex, instr.mem, instr.wb, instr.commit))
        file.close()

    def mark_issue(self, id, issue_cycle):
        instr = MonitoredInstruction(id,issue_cycle)
        self.instlist.append(instr)

    def mark_ex(self, id, exec_cycle):
        for inst in self.instlist:
            if inst.id == id:
                inst.ex = exec_cycle
    
    def mark_mem(self, id, mem_cycle):
        for inst in self.instlist:
            if inst.id == id:
                inst.mem = mem_cycle

    def mark_wb(self, id, wb_cycle):
        for inst in self.instlist:
            if inst.id == id:
                inst.wb = wb_cycle

    def mark_commit(self, id, commit_cycle):
        for inst in self.instlist:
            if inst.id == id:
                inst.commit = commit_cycle

class MonitoredInstruction():
    def __init__(self,id,issue) -> None:
        self.id = id
        self.issue = issue
        self.ex = 0
        self.mem = 0
        self.wb = 0
        self.commit = 0
    
    def __str__(self) -> str:
        strIns = f'{self.id} | {self.issue} |{self.ex} |{self.mem} |{self.wb} |{self.commit}'
        return(strIns)


"""   
monit = Monitor()
monit.mark_issue(0,1)
monit.mark_ex(0,10)
monit.mark_mem(0,11)
monit.mark_wb(0,12)
monit.mark_commit(0,22)
monit.mark_issue(1,20)
monit.mark_ex(1,21)
monit.mark_mem(1,22)
monit.mark_wb(1,32)
monit.mark_commit(1,34)
monit.mark_issue(2,30)
monit.mark_ex(2,31)
monit.mark_mem(2,32)
monit.mark_issue(3,59)
monit.mark_wb(3,99)
monit.mark_wb(2,98)
monit.mark_commit(2,44)
monit.output()
"""

