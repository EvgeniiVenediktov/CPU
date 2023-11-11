# CPU simulation
from memory import Memory


### Create instances of all modules: ###

# Monitor - TODO

# Input Module
## Input Decoder - TODO - 🛠️ in progress
## Instruction Buffer - TODO - 🛠️ in progress

# CDB - DONE ✔️

# Register Module:
## Register Alias Table - TODO
## Architecture Register Files - TODO

# Reorder Module:
## Reorder Buffer - TODO
## Renaming Module - TODO

# Branch predictor - TODO

# Execution Module
## Functional Modules (Adders, Multipliers) - TODO
## Functional Module Buffers (Int buffer, Float buffer) - TODO - store values here if CDB is ocuppied
## Reservation Stations - TODO

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
    
    ### WRITEBACK Stage

    ### MEMORY Stage

    ### EXECUTION Stage

    ### ISSUE Stage
  
    pass 

### Create Output TimeTable: ###
# TODO