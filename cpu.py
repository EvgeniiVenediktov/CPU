# CPU simulation
from memory import Memory


### Create instances of all modules: ###

# Monitor - TODO - 🛠️ in progress

# Input Module
## Input Decoder - DONE ✔️
## Instruction Buffer - DONE ✔️

# CDB - DONE ✔️

# Register Module:
## Register Alias Table - TODO
## Architected Register File - TODO

# Reorder Module:
## Reorder Buffer - TODO

# Branch predictor - TODO - in the next iteration

# Execution Module
## Functional Modules (Adders, Multipliers) - TODO
## Functional Module Buffers (Int buffer, Float buffer) - TODO - store values here if CDB is ocuppied
## Reservation Stations - TODO - 🛠️ in progress

# Memory Module
## Address Resolver - TODO
## Load/Store Buffers - TODO - 🛠️ in progress
## Memory - DONE ✔️
mem_init_file = ""
hard_memory = Memory(mem_init_file)


### Run for N clock cycles: ###
NUM_OF_CYCLES = 1000
for cycle in range(NUM_OF_CYCLES):
    ### COMMIT Stage
    """
    Commit a ready instruction from ROB:
        1. Write to ARF
        2. Empty commited entry
        3. Update head pointer
        4. Monitor.mark_commit(ID, i)
    """
    
    ### WRITEBACK Stage
    """
    1. Check CDB and update values by all consumers:
        - ROB
        - Reservation Stations
        - LD/SD buffer
    2. If written anything:
        - Monitor.mark_wb(ID, i)
    3. Clear current values
    4. Write a value from buffer to current
    """

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
    """
    1. Read inst from inst buffer
    2. Check if resources available:
        - Appropriate RS entry
        - ROB entry
        or
        - LD/ST buffer entry
        ! Stall issue if any needed resource not available !
    3. Read RAT, read (available) sources, update RAT
    4. Write to RS and ROB --- ! OR call AddressResolver, write to LD/SD buffer
    5. Monitor.mark_issue(ID, i)
    """
    pass 

### Create Output TimeTable: ###
# TODO