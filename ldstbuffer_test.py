import unittest
from ldstbuffer import LoadStoreBuffer, LdStConfig
from cdb import CentralDataBus

class TestLdStBuffer(unittest.TestCase):

    def setUp(self) -> None:
        self.cdb = CentralDataBus()
        n = 10
        cfg = LdStConfig(n, n)
        self.buf = LoadStoreBuffer(cdb=self.cdb, cfg=cfg)
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_add_few(self):
        # Arrange
        instrs = [ ["LD", [22, 22]] for _ in range(8)]

        # Action

        # Assert