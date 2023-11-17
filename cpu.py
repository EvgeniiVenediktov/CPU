# CPU simulation
from memory import Memory
from decoder import InstBuff
from cdb import CentralDataBus
from reservationstation import ReservationStation
from reservationstation import INT_ADDER_RS_TYPE, DEC_ADDER_RS_TYPE, DEC_MULTP_RS_TYPE, LD_STORE_RS_TYPE
from output import Monitor
from reordering import ReorderBuffer
from registers import ArchitectedRegisterFile, RegistersAliasTable

type number = int | float

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
## Functional Modules (Adders, Multipliers) - TODO
## Functional Module Buffers (Int buffer, Float buffer) - DONE ✔️ - store values here if CDB is ocuppied
## Reservation Stations - TODO - 🛠️ in progress
RS_LEN = 5
res_stations = {
    INT_ADDER_RS_TYPE:ReservationStation(cdb=cdb, len=RS_LEN),
    DEC_ADDER_RS_TYPE:ReservationStation(cdb=cdb, len=RS_LEN),
    DEC_MULTP_RS_TYPE:ReservationStation(cdb=cdb, len=RS_LEN),
    LD_STORE_RS_TYPE:ReservationStation(cdb=cdb, len=RS_LEN)
}

# Memory Module
## Address Resolver - TODO
## Load/Store Buffers - TODO - 🛠️ in progress
## Memory - DONE ✔️
mem_init_file = ""
hard_memory = Memory(mem_init_file)


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
    """
    1. Check CDB and update values by all consumers:
        - ROB
        - Reservation Stations
        - LD/SD buffer
    2. If written anything - Monitor.mark_wb(ID, i)
    3. Clear current value
    4. Write a value from buffer to current
    """
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

    ### ISSUE Stage
    #1. Read inst from inst buffer
    instr = instruction_buffer.issue()
    rs_type = ""
    t = instr.inst_type
    if t == "LD" or "SD":
        rs_type = LD_STORE_RS_TYPE
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
        continue
    #2.1. Check if resources available - ROB entry
    if not rob.entry_is_free():
        continue

    #3. Prepare operands, write to RS, ROB:
    """3. Read operands:
        3.1. Read RAT - get RegisterNum or RS_entry
        3.2. Read (available) sources: if RegNum - Take RegValue, if RS_entry - set dependency to it
        3.3. Update RAT - fill the corresponding entry with assigned RS_entry"""
    issued_instr = rob.add_instruction(instr)
    if issued_instr == None:
        continue

    #4. Write to RS:
    success = matching_rs.add_instruction(issued_instr)
    if not success:
        raise Exception("failed to add instuction to a RS", str(issued_instr), str(matching_rs))

    #5. Monitor.mark_issue(ID, i)
    monitor.mark_issue(instr.id, cycle)

    """
    4. TODO: call AddressResolver, write to LD/SD buffer
    """
    pass 

### Create Output TimeTable: ###
monitor.output()

