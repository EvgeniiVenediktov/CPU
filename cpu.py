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
from funit import TYPE_INT_ADDER, TYPE_DEC_ADDER, TYPE_DEC_MULTP, TYPE_MEMORY_LOAD, TYPE_MEMORY_STORE
from utils import number

PROGRAM_FILENAME = ""

### Create instances of all modules: ###
# Monitor - DONE ✔️
monitor = Monitor()

# Input Module
## Input Decoder - DONE ✔️
## Instruction Buffer - DONE ✔️
instruction_buffer = InstBuff(PROGRAM_FILENAME)

# CDB - DONE ✔️
cdb = CentralDataBus()

# Register Module:
## Register Alias Table - DONE ✔️
## Architected Register File - DONE ✔️
REG_LEN = 7
arf = ArchitectedRegisterFile(REG_LEN)
rat = RegistersAliasTable(arf, REG_LEN)

# Reorder Module:
## Reorder Buffer - DONE ✔️
ROB_LEN = 10
rob = ReorderBuffer(cdb, len=ROB_LEN)

# Branch predictor - TODO - in the next iteration

# Execution Module
## Functional Modules (Adders, Multipliers) - DONE ✔️
## Functional Module Buffers (Int buffer, Float buffer) - DONE ✔️ - store values here if CDB is ocuppied
## Reservation Stations - DONE ✔️

adder_int = FunctionalUnit(TYPE_INT_ADDER, cdb)
adder_dec = FunctionalUnit(TYPE_DEC_ADDER, cdb)
multr_dec = FunctionalUnit(TYPE_DEC_MULTP, cdb)
memory_loader_fu = MemoryLoadFunctionalUnit(TYPE_MEMORY_LOAD, cdb)
memory_storer_fu = MemoryStoreFunctionalUnit(TYPE_MEMORY_STORE, cdb)

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
## Address Resolver - TODO
address_resolver = AddressResolver()
## Load/Store Buffers - TODO - 🛠️ in progress
LD_SD_BUF_LEN = 3
load_buffer = LoadBuffer(cdb, memory_loader_fu, LD_SD_BUF_LEN)
store_buffer = StoreBuffer(cdb, memory_storer_fu, LD_SD_BUF_LEN)
## Memory - TODO
MEM_SIZE = 256
mem_init_file = ""
hard_memory = Memory(mem_init_file, MEM_SIZE)


def issue_ld_sd_instruction(instr):
    # TODO
    pass

### Run for N clock cycles: ###
NUM_OF_CYCLES = 1000
for cycle in range(NUM_OF_CYCLES):
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
    for rs_name in res_stations:
        written_value_id = res_stations[rs_name].read_cdb()

    # TODO written_value_id = LD/SD.read_cdb()

    #2. If written anything - Monitor.mark_wb(ID, i)
    if written_value_id != None:
        monitor.mark_wb(written_value_id, cycle)
        
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
        id = res_stations[rs_type].try_execute()
        if id != None:
            monitor.mark_ex_start(id, cycle)
    
    #3. Try processing result from Address Resolver
    resolved_instruction = address_resolver.produce_address()
    if resolved_instruction != None:
        rs = None
        if resolved_instruction.op == "LD":
            rs = res_stations[LOAD_RS_TYPE]
        if resolved_instruction.op == "SD":
            rs = res_stations[STORE_RS_TYPE]    
        monitor.mark_ex_end(resolved_instruction.id, cycle)

        if rob.entry_is_free() and rs.entry_is_free():
            issued_instr = rob.add_instruction(instr)
            if issued_instr == None:
                raise Exception("failed to add instuction to ROB", str(issued_instr), str(rob))
            success = rs.add_instruction(issued_instr)
            if not success:
                raise Exception("failed to add instuction to a RS", str(issued_instr), str(rs))
        

    ### ISSUE Stage
    #1. Read inst from inst buffer
    instr = instruction_buffer.issue()
    if instr == None:
        print(f"Nothing issued, cycle {cycle}")
        continue
    rs_type = ""
    t = instr.inst_type
    if t == "LD" or "SD":
        #rs_type = LOAD_RS_TYPE
        operand_replacement = rat.get_value_or_alias(instr.operands[1])
        instr.operands[1] = operand_replacement
        #try sending it to Address Resolver
        ar_id = address_resolver.resolve_address(instr)
        if ar_id == None:
            instruction_buffer.return_to_prev_index()
            continue
        monitor.mark_ex_start(ar_id, cycle)
        continue
    elif t == "Addi" or "Sub":
        rs_type = INT_ADDER_RS_TYPE
    elif t == "Add.d" or "Sub.d":
        rs_type = DEC_ADDER_RS_TYPE
    elif t == "Mult.d":
        rs_type = DEC_MULTP_RS_TYPE
    # TODO add support of Branch instructions
    
    #2. Check if resources available - Appropriate RS entry or LD/SD buf entry
    matching_rs = res_stations[rs_type]
    if not matching_rs.entry_is_free():
        instruction_buffer.return_to_prev_index()
        continue
    #2.1. Check if resources available - ROB entry
    if not rob.entry_is_free():
        instruction_buffer.return_to_prev_index()
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

    pass 

### Create Output TimeTable: ###
monitor.output()

