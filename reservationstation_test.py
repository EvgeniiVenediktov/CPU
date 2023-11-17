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
            if name == 'result':
                self.assertIsNone(val, name)
                continue
            self.assertIsNotNone(val, name)
    
    def test_update(self):
        # Arrange
        e_int = Entry()
        e_float = Entry()
        attrs_int = {'busy':True,'op':"addi",'id':1, 'rob':"F1", 'val1':int(2),'val2':int(3), 'dep1':"",'dep2':"",'result':None}
        attrs_float = {'busy':True,'op':"addd",'id':1, 'rob':"F2", 'val1':float(2),'val2':float(3), 'dep1':"",'dep2':"",'result':None}
        # Action
        e_int.update(busy=1,op="addi",rob="F1",val1=2,val2=3)
        e_float.update(busy=1,op="addd",rob="F2",val1=2.0,val2=3.0)
        # Assert
        d = vars(e_int)
        for field in d:
            val = d[field]
            self.assertEqual(val, attrs_int[field], field)

        d = vars(e_float)
        for field in d:
            val = d[field]
            self.assertEqual(val, attrs_float[field], field)


if __name__ == '__main__':
    unittest.main()
