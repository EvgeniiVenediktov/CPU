# CPU simulation
from memory import Memory


### Create instances of all modules: ###

# Monitor - TODO

# Input Module
## Input Decoder - TODO - 🛠️ in progress
## Instruction Buffer - TODO - 🛠️ in progress

# CDB - TODO

# Register Module:
## Register Alias Table - TODO
## Architecture Register Files - TODO

# Reorder Module:
## Reorder Buffer - TODO
## Renaming Module - TODO

# Execution Module
## Functioanal Modules (Adders, Multipliers) - TODO
## Reservation Stations - TODO

# Memory Module
## Address Resolver - TODO
## Load/Store Buffers - TODO
## Memory - DONE ✔️
mem_init_file = ""
hard_memory = Memory(mem_init_file)
