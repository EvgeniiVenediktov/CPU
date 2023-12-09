import unittest
from snapshooter import Snapshooter

class TestSnapshooter(unittest.TestCase):
    def test_success(self):
        # Arrange
        s = Snapshooter()
        data_set = [1, 2, 3]
        ids = [1, 1, 3]
        cycles = [11, 14, 16]
        recover_cycles = [13, 17, 19]

        # Action
        for i in range(len(ids)):
            s.create_snapshot(data_set[i], ids[i], cycles[i])

        self.assertEqual(len(s.snapshots), len(ids))

        for i in range(len(ids)-1, -1, -1): # Goind backwards
            # Assert
            actual_data = s.pop_last_matching_snapshot(ids[i], recover_cycles[i])
            self.assertEqual(actual_data, data_set[i])

    def test_deletes_more_recent_snapshots(self):
        # Arrange
        s = Snapshooter()
        data_set = [1, 2, 3]
        ids = [1, 1, 3]
        cycles = [11, 14, 16]
        recover_cycles = [13, 17, 19]
        expected_data = [1, None, None]
        for i in range(len(ids)):
            s.create_snapshot(data_set[i], ids[i], cycles[i])

        # Action
        for i in range(len(ids)): # Goind forward, the first pop removes all more recent shots
            actual_data = s.pop_last_matching_snapshot(ids[i], recover_cycles[i])
            # Assert
            self.assertEqual(actual_data, expected_data[i])





if __name__ == '__main__':
    unittest.main()
