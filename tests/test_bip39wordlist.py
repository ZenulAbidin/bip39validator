from unittest import TestCase
from bip39validator import InvalidWordList, ValidationFailed
from bip39validator.BIP39WordList import BIP39WordList

valid_list = """abcdef
ghijkl
mnopqr
stuvwxyz"""

invalid_list = ["12345",
"@$^(*",
"ABCDE"]


class TestBIP39WordList(TestCase):
    def test_test_lowercase(self):
        try:
            bip39 = BIP39WordList("invalid_list", string="\n".join(invalid_list))
        except InvalidWordList as e:
            self.assertTrue(e.has_invalid_chars)
            self.assertFalse(e.has_2048_words)
            self.assertEqual(e.num_words, 3)
            self.assertEqual(e.err_lines, [])
        bip39 = BIP39WordList("valid_list", string=valid_list)
        res = bip39.test_lowercase()
        self.assertFalse(res.has_invalid_chars)
        self.assertFalse(res.has_2048_words)
        self.assertEqual(res.num_words, 4)
        self.assertEqual(res.err_lines, [])

        # We are going to load the english wordlist from the current folder
        # and also from the BIP Github repo.
        # Test fails if exceptions are thrown.
        with open('./tests/english.txt') as f:
            bip39 = BIP39WordList("file_list", handle=f)
        res = bip39.test_lowercase()

        # We only need to test this logic once.
        self.assertTrue(res.has_2048_words)
        self.assertEqual(res.num_words, 2048)

        bip39 = BIP39WordList("url_list", url="https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt")

        try:
            bip39 = BIP39WordList("no_list")    # This should not work!
            self.fail()
        except ValueError as e:
            pass
        except InvalidWordList as e:
            pass


    # Only test members part of the public API. For these return objects,
    # none of the members are public. Just the methods.
    def test_test_lev_distance(self):
        with open('./tests/english.txt') as f:
            bip39 = BIP39WordList("file_list", handle=f)
            try:
                bip39.test_lev_distance(2)
            except ValidationFailed as e:
                pass


    def test_test_initial_chars(self):
        with open('./tests/english.txt') as f:
            bip39 = BIP39WordList("file_list", handle=f)
            bip39.test_initial_chars(4)

    def test_test_max_length(self):
        with open('./tests/english.txt') as f:
            bip39 = BIP39WordList("file_list", handle=f)
            bip39.test_initial_chars(4)
