# CPU simulation
from memory import Memory
from decoder import InstBuff
from cdb import CentralDataBus
from reservationstation import ReservationStation, LoadBuffer, StoreBuffer
from reservationstation import INT_ADDER_RS_TYPE, DEC_ADDER_RS_TYPE, DEC_MULTP_RS_TYPE, LOAD_RS_TYPE, STORE_RS_TYPE
from output import Monitor
from reordering import ReorderBuffer
from registers import ArchitectedRegisterFile, RegistersAliasTable
from funit import FunctionalUnit, AddressResolver, MemoryLoadFunctionalUnit, MemoryStoreFunctionalUnit
from utils import TYPE_INT_ADDER,TYPE_DEC_ADDER,TYPE_DEC_MULTP,TYPE_MEMORY_LOAD,TYPE_MEMORY_STORE
from utils import number

#PROGRAM_FILENAME = "./TestBench/Add.txt"
#PROGRAM_FILENAME = "./TestBench/Hazards copy.txt"
#PROGRAM_FILENAME = "./TestBench/Hazards.txt" # Checked ✔️
#PROGRAM_FILENAME = "./TestBench/Multi.d.txt"
#PROGRAM_FILENAME = "./TestBench/RSFull.txt"
PROGRAM_FILENAME = "./TestBench/ForwardingStore.txt"

### Create instances of all modules: ###
# Monitor - DONE ✔️
monitor = Monitor()

# Input Module
## Input Decoder - DONE ✔️
## Instruction Buffer - DONE ✔️
instruction_buffer = InstBuff(PROGRAM_FILENAME)
instruction_buffer.refill()

# CDB - DONE ✔️
cdb = CentralDataBus()

# Register Module:
## Register Alias Table - DONE ✔️
## Architected Register File - DONE ✔️
REG_LEN = 32
arf = ArchitectedRegisterFile(REG_LEN)
rat = RegistersAliasTable(arf, REG_LEN)

# Reorder Module:
## Reorder Buffer - DONE ✔️
ROB_LEN = 10
rob = ReorderBuffer(cdb, rat, len=ROB_LEN)

# Branch predictor - TODO - in the next iteration

# Execution Module
## Functional Modules (Adders, Multipliers) - DONE ✔️
## Functional Module Buffers (Int buffer, Float buffer) - DONE ✔️ - store values here if CDB is ocuppied
## Reservation Stations - DONE ✔️

adder_int = FunctionalUnit(TYPE_INT_ADDER, cdb)
adder_dec = FunctionalUnit(TYPE_DEC_ADDER, cdb)
multr_dec = FunctionalUnit(TYPE_DEC_MULTP, cdb)

## Memory - DONE ✔️
MEM_SIZE = 256
mem_init_file = ""
hard_memory = Memory(mem_init_file, MEM_SIZE)

memory_loader_fu = MemoryLoadFunctionalUnit(TYPE_MEMORY_LOAD, cdb, hard_memory)
memory_storer_fu = MemoryStoreFunctionalUnit(TYPE_MEMORY_STORE, cdb, hard_memory)

func_units = [adder_int, adder_dec, multr_dec]

INT_ADDER_RS_LEN = 2
DEC_ADDER_RS_LEN = 3
DEC_MULTP_RS_LEN = 2

res_stations = {
    INT_ADDER_RS_TYPE:ReservationStation(cdb=cdb, funit=adder_int, len=INT_ADDER_RS_LEN),
    DEC_ADDER_RS_TYPE:ReservationStation(cdb=cdb,funit=adder_dec, len=DEC_ADDER_RS_LEN),
    DEC_MULTP_RS_TYPE:ReservationStation(cdb=cdb,funit=multr_dec, len=DEC_MULTP_RS_LEN),
}

# Memory Module
## Address Resolver - DONE ✔️
address_resolver = AddressResolver()
## Load/Store Buffers - DONE ✔️
LD_SD_BUF_LEN = 3
load_buffer = LoadBuffer(cdb, memory_loader_fu, LD_SD_BUF_LEN)
store_buffer = StoreBuffer(cdb, memory_storer_fu, LD_SD_BUF_LEN)


def end_cycle():
    for fu in func_units:
        fu.release_at_the_end_of_cycle()
    memory_loader_fu.release_at_the_end_of_cycle()
    memory_storer_fu.release_at_the_end_of_cycle()

    for rs_type in res_stations:
        rs = res_stations[rs_type]
        rs.end_cycle()
    load_buffer.end_cycle()
    store_buffer.end_cycle()

### Run for N clock cycles: ###
NUM_OF_CYCLES = 300
for cycle in range(1,NUM_OF_CYCLES):
    ### COMMIT Stage
    """
    Commit a ready instruction from ROB:
        1. Write to ARF
        1.1. Maybe free RAT entry
        2. Empty commited entry
        3. Update head pointer
        4. Monitor.mark_commit(ID, i)
    """
    #1. Commit a ready one from ROB
    comitted_id = rob.commit()
    if comitted_id != None:
        #2. Monitor.mark_commit(ID, i)
        monitor.mark_commit(comitted_id, cycle)

    ### WRITEBACK Stage
    #1. Check CDB and update values by all consumers:
    written_value_id = None
    written_value_id = rob.read_cdb()
    if written_value_id != None:
        monitor.mark_wb(written_value_id, cycle)
    for rs_name in res_stations:
        rs = res_stations[rs_name]
        written_value_id = rs.read_cdb()
        if written_value_id != None:
            monitor.mark_wb(written_value_id, cycle)

    written_value_id = load_buffer.read_cdb()
    if written_value_id != None:
        monitor.mark_wb(written_value_id, cycle)
    written_value_id = store_buffer.read_cdb()
    if written_value_id != None:
        monitor.mark_wb(written_value_id, cycle)

    #2. If written anything - Monitor.mark_wb(ID, i)
        
    #3. Clear current CDB value and Write a value from buffer to current
    cdb.flush_current_bump_buffered()

    ### MEMORY Stage
    """
    1. If memory is busy: 
        1.1. decrement busy counter
        1.2. If busy_counter became 0:
                - Write result to CDB
                - Now the memory is Free 
                - Monitor.mark_mem(ID, i)
        1.3. skip MEM stage
    2. Start loading/storing from the LD/SD buffer
    3. Set mem_busy_counter = specific num of CC
    """
    #1. Try producing result to CDB from Loader and Storer
    id = memory_loader_fu.produce_result()
    if id != None:
        monitor.mark_mem_end(id, cycle)
    id = None
    id = memory_storer_fu.produce_result()
    if id != None:
        monitor.mark_mem_end(id, cycle)
    #2. If rob.head - Store instruction, start executing it
    rob_head = rob.show_head_entry()
    if rob_head.type == "SD":
        sd_buf_head = store_buffer.show_head()
        if not rob_head.in_progress and sd_buf_head != None:
            if rob_head.id == sd_buf_head.id:
                id = store_buffer.try_execute()
                if id != None:
                    monitor.mark_mem_start(id, cycle)
                    rob_head.in_progress = True
    #3. Try exec Load:
    id = load_buffer.try_execute()
    if id != None:
        monitor.mark_mem_start(id, cycle)

    ### EXECUTION Stage
    """ FU - functional unit
    [1] For each FU:
        1. If FU is busy:
            1.1. Decrement busy_counter
            1.2. If busy_counter became 0:
                - Write result to CDB
                - Now the FU is Free 

    [2] For each Reservation Station:
        1. If operands not resolved - skip EXE stage
        2. If FU is free:
            2.1. Set busy_counter = specific num of CC
            2.2. Monitor.mark_execution(ID, i)
    """
    #1. Try producing result to CDB from each FunctionalUnit:
    for fu in func_units:
        id = fu.produce_result()
        if id != None:
            monitor.mark_ex_end(id, cycle)
        

    #2. Try starting execution from each of RS:
    for rs_type in res_stations:
        rs = res_stations[rs_type]
        id, result_is_ready = rs.try_execute()
        if id != None:
            monitor.mark_ex_start(id, cycle)
            if result_is_ready:
                fu = rs.funit
                id = fu.produce_result()
                if id != None:
                    monitor.mark_ex_end(id, cycle)
    
    #3. Try processing result from Address Resolver
    resolved_instruction = address_resolver.produce_address()
    if resolved_instruction != None:
        rs = None
        if resolved_instruction.inst_type == "LD":
            rs = load_buffer
        if resolved_instruction.inst_type == "SD":
            rs = store_buffer
        monitor.mark_ex_start(resolved_instruction.id, cycle)
        monitor.mark_ex_end(resolved_instruction.id, cycle)

        if rob.entry_is_free() and rs.entry_is_free():
            issued_instr = rob.add_instruction(resolved_instruction)
            if issued_instr == None:
                raise Exception("failed to add instuction to ROB", str(issued_instr), str(rob))
            success = rs.add_instruction(issued_instr)
            if not success:
                raise Exception("failed to add instuction to a RS", str(issued_instr), str(rs))
            address_resolver.address_was_processed()


    ### ISSUE Stage
    #1. Read inst from inst buffer
    instr = instruction_buffer.issue()
    if instr == None:
        print(f"Nothing issued, cycle {cycle}")
        end_cycle()
        continue
    rs_type = ""
    t = instr.inst_type
    if t == "EOF":
        print(f"EOF, finish of simulation. Cycle #{cycle}")
        break
    if t == "LD" or t == "SD": 
        # Syntax: SD F2,10(R3) // F2 - value, 10+R3 - source
        # Syntax: LD F2,10(R3) // F2 - dest, 10+R3 - source
        #rs_type = LOAD_RS_TYPE
        if t == "LD":
            instr.original_dest = instr.operands[0]
        if t == "SD":
            operand_replacement = rat.get_value_or_alias(instr.operands[0])
            instr.operands[0] = operand_replacement
        operand_replacement = rat.get_value_or_alias(instr.operands[1])
        instr.operands[1] = operand_replacement
        #try sending it to Address Resolver
        ar_id = address_resolver.resolve_address(instr)

        if ar_id == None:
            instruction_buffer.return_to_prev_index()
            end_cycle()
            continue
        monitor.mark_issue(ar_id, cycle)
        end_cycle()
        continue
    elif t == "Add" or t == "Addi" or t == "Sub":
        rs_type = INT_ADDER_RS_TYPE
    elif t == "Add.d" or t == "Sub.d":
        rs_type = DEC_ADDER_RS_TYPE
    elif t == "Mult.d":
        rs_type = DEC_MULTP_RS_TYPE
    # TODO add support of Branch instructions
    
    #2. Check if resources available - Appropriate RS entry or LD/SD buf entry
    matching_rs = res_stations[rs_type]
    if not matching_rs.entry_is_free():
        instruction_buffer.return_to_prev_index()
        end_cycle()
        continue
    #2.1. Check if resources available - ROB entry
    if not rob.entry_is_free():
        instruction_buffer.return_to_prev_index()
        end_cycle()
        continue

    #3. Prepare operands, write to RS, ROB:
    """3. Read operands:
        3.1. Read RAT - get RegisterNum or RS_entry
        3.2. Read (available) sources: if RegNum - Take RegValue, if RS_entry - set dependency to it
        3.3. Update RAT - fill the corresponding entry with assigned RS_entry"""
    issued_instr = rob.add_instruction(instr)
    if issued_instr == None:
        raise Exception("failed to add instuction to ROB", str(issued_instr), str(rob))

    #4. Write to RS:
    success = matching_rs.add_instruction(issued_instr)
    if not success:
        raise Exception("failed to add instuction to a RS", str(issued_instr), str(matching_rs))

    #5. Monitor.mark_issue(ID, i)
    monitor.mark_issue(instr.id, cycle)

    # Release all FUs
    end_cycle()
    pass 

### Create Output TimeTable: ###
monitor.output()

with open("regs.txt", "w") as f:
    f.write(str(arf))
with open("rat.txt", "w") as f:
    f.write(str(rat))
