import unittest
from os import system

class TestBIP39Validator(unittest.TestCase):
    def test_vip39validator_url(self):
        cmd = "bip39validator -q -d 1 https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt"
        self.assertEqual(system(cmd), 0)

    def test_vip39validator_file_d_u_l(self):
        cmd = "bip39validator -q -d 1 tests/english.txt"
        self.assertEqual(system(cmd), 0)

    def test_vip39validator_file_nd_nu_nl(self):
        cmd = "bip39validator -q -u 2 -l 6 tests/english.txt"
        self.assertEqual(system(cmd), 0)


if __name__ == '__main__':
    unittest.main()
