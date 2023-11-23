class Monitor():
    def __init__(self) -> None:
        self.instlist:list[MonitoredInstruction] = []

    def output(self):
        """Writes an output timetable to output.txt"""
        sorted_instrs = sorted(self.instlist, key= lambda instructions: instructions.id)
        with open('output.txt', 'w', encoding="utf-8") as file:
            file.write("┌──────┬─────────┬─────────────┬─────────────┬────────┬──────────┐\n")
            file.write("|--Id--|--Issue--|-----Exe-----|-----Mem-----|--Wrbk--|--Commit--|\n")
            file.write("├──────┼─────────┼─────────────┼─────────────┼────────┼──────────┤\n")
            for instr in sorted_instrs:
                file.write('|{:^5} | {:^7} | {:^5}-{:^5} | {:^5}-{:^5} | {:^6} | {:^9}|\n'.format(
                    instr.id, instr.issue, instr.ex_start, instr.ex_end, instr.mem_start,instr.mem_end, instr.wb, instr.commit))
            file.write("└──────┴─────────┴─────────────┴─────────────┴────────┴──────────┘")
        file.close()

    def mark_issue(self, id, issue_cycle):
        instr = MonitoredInstruction(id,issue_cycle)
        self.instlist.append(instr)

    def mark_ex_start(self, id, exec_cycle):
        for inst in self.instlist:
            if inst.id == id:
                inst.ex_start = exec_cycle
                return
    
    def mark_ex_end(self, id, exec_cycle):
        for inst in self.instlist:
            if inst.id == id:
                inst.ex_end = exec_cycle
                return
    
    def mark_mem_start(self, id, mem_cycle):
        for inst in self.instlist:
            if inst.id == id:
                inst.mem_start = mem_cycle
                return

    def mark_mem_end(self, id, mem_cycle):
        for inst in self.instlist:
            if inst.id == id:
                inst.mem_end = mem_cycle
                return

    def mark_wb(self, id, wb_cycle):
        for inst in self.instlist:
            if inst.id == id:
                inst.wb = wb_cycle
                return

    def mark_commit(self, id, commit_cycle):
        for inst in self.instlist:
            if inst.id == id:
                inst.commit = commit_cycle
                return

class MonitoredInstruction():
    def __init__(self,id,issue) -> None:
        self.id = id
        self.issue = issue
        self.ex_start = 0
        self.ex_end = 0
        self.mem_start = 0
        self.mem_end = 0
        self.wb = 0
        self.commit = 0
    
    def __str__(self) -> str:
        strIns = f'{self.id} | {self.issue} |{self.ex_start}-{self.ex_end}|{self.mem_start} |{self.mem_end} |{self.wb} |{self.commit}'
        return(strIns)


if __name__ == "__main__":
    
    monit = Monitor()
    monit.mark_issue(0,1)
    monit.mark_ex_start(0,10)
    monit.mark_ex_end(0,10)
    monit.mark_mem_start(0,11)
    monit.mark_mem_end(0,14)
    monit.mark_wb(0,12)
    monit.mark_commit(0,22)
    monit.mark_issue(1,20)
    monit.mark_ex_start(1,21)
    monit.mark_ex_end(1,21)
    monit.mark_mem_start(1,22)
    monit.mark_mem_end(1,24)
    monit.mark_wb(1,32)
    monit.mark_commit(1,34)
    monit.mark_issue(2,30)
    monit.mark_ex_start(2,31)
    monit.mark_ex_end(2,31)
    monit.mark_mem_start(2,32)
    monit.mark_mem_end(2,34)
    monit.mark_issue(3,59)
    monit.mark_wb(3,99)
    monit.mark_wb(2,98)
    monit.mark_commit(2,44)
    monit.output()