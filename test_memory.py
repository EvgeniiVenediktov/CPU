import unittest
import memory
import os


class ValidAddressesAndValues(unittest.TestCase):
    def setUp(self) -> None:
        self.init_file_name = 'test_init_mem_file.txt'

    def tearDown(self) -> None:
        if os.path.exists(self.init_file_name):
            os.remove(self.init_file_name)

    def test_all_zeros(self):
        # Arrange
        expected = [0 for _ in range(memory.MEM_SIZE)]

        # Action
        mem_array = memory.Memory().get_mem_array()

        # Assert
        self.assertEqual(expected, mem_array)

    def test_init_from_file_int(self):
        # Arrange
        init_vals = []
        for i in range(memory.MEM_SIZE):
            init_vals.append(i*2)
        
        with open(self.init_file_name, mode="w") as init_file:
            for i in range(memory.MEM_SIZE):
                init_file.write(f"{i},{init_vals[i]}\n")
            init_file.close()

        # Action
        mem = memory.Memory(self.init_file_name)
        mem_array = mem.get_mem_array()

        # Assert
        self.assertEqual(len(init_vals), len(mem_array))
        self.assertEqual(init_vals, mem_array)

    def test_init_from_file_mixed(self):
        # Arrange
        init_vals = []
        for i in range(memory.MEM_SIZE):
            v = int(i*2)
            if i%2 == 0:
                v += 0.1
            init_vals.append(v)
        
        with open(self.init_file_name, mode="w") as init_file:
            for i in range(memory.MEM_SIZE):
                init_file.write(f"{i},{init_vals[i]}\n")
            init_file.close()

        # Action
        mem = memory.Memory(self.init_file_name)
        mem_array = mem.get_mem_array()

        # Assert
        self.assertEqual(len(init_vals), len(mem_array))
        self.assertEqual(init_vals, mem_array)
    
    def test_load_store(self):
        # Arrange
        vals = [(0, 12), (4, 22), (63, 0.77)]

        # Action
        mem = memory.Memory()
        for i, v in vals:
            mem.store(i, v)

        # Assert
        for i, expected_val in vals:
            actual_val = mem.load(i)
            self.assertEqual(expected_val, actual_val)

if __name__ == '__main__':
    unittest.main()
