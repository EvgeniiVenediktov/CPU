import unittest
from reservationstation import Entry

class TestRS(unittest.TestCase):

    def test_entry_constructor(self):
        # Arrange
        entry = Entry()
        
        # Action
        d = vars(entry)

        # Assert
        for name in d:
            val = d[name]
            self.assertIsNotNone(val, name)
    
    def test_update(self):
        self.skipTest("TODO")
        # Arrange
        e = Entry()
        #attrs = {'busy':1,'op':op,'val1':val1,'val2':val2,'dep1':dep1,'dep2':dep2}
        # Action

        # Assert


if __name__ == '__main__':
    unittest.main()
