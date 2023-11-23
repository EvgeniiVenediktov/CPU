# Memory Unit
from utils import number

class Memory:
    """
    Memory unit does Load and Store.
    With `MEM_SIZE`==64 It simulates memory with the size of 256 Bytes.
    For this project we support Int32 and Float32, so each one of them takes 32 Bits = 4 Bytes.
    Each section of `mem_array` can contain a number.

    Memory initializes with zeros in all the cells. To init it with some information, it
    should be passed as an argument in .txt format, where each line conveys to this style:
    ```
        _______________________
        |  (int)  | (int/float)| 
        |_________|____________|
        |mem_addr ,   value    |
        |______________________|
        |   12    ,    144     |
        |   33    ,    10.5    |
        |______________________|
    ```

"""
    def __init_from_file(self, init_file_name:str):
        with open(init_file_name) as f:
            lines = f.readlines()
            for line in lines:
                line = line.removesuffix("\n")
                tokens = line.split(',')
                addr = int(tokens[0])//4
                value = 0
                if tokens[1].find('.') != -1:
                    value = float(tokens[1])
                else: 
                    value = int(tokens[1])
                self._mem_array[addr] = value
            f.close()
    
    def __init__(self, init_file_name:str='', mem_size:int=256):
        self._mem_array = [0 for _ in range(mem_size//4)]
        if len(init_file_name) != 0:
            self.__init_from_file(init_file_name)
        
    def memory_dump(self, output_file_name='dump_memory.txt'):
        with open(output_file_name, mode="w", encoding="utf-8") as f:
            f.write('┌──────┬───────────┐\n')
            f.write('|-cell-|---value---|\n')
            f.write("├──────┴───────────┤\n")
            for i, val in enumerate(self._mem_array):
                if val == 0:
                    continue
                s = '|{:>6}|{:^11}|\n'.format(i*4, val)
                f.write(s)
            f.write('└──────┴───────────┘')
            f.close()


    def get_mem_array(self):
        return self._mem_array
    
    def load(self, address:int) -> number:
        return self._mem_array[int(address)]
    
    def store(self, address:int, value:number) -> bool:
        self._mem_array[int(address)] = value










